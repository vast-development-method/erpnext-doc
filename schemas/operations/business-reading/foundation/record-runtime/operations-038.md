# Record lifecycle and persistence · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Doctype

<a id="op-6e6068df64aca0"></a>
### Get fields not allowed in list view

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_get_fields_not_allowed_in_list_view`

**Inputs** meta.

**Declared result** list at str.

**Explicit results** not\_allowed\_in\_list\_view.

**Local steps**

- Set not\_allowed\_in\_list\_view from list(copy.copy(no\_value\_fields)).
- If meta.istable.
  - Evaluate not\_allowed\_in\_list\_view.remove(“Button”).
  - Evaluate not\_allowed\_in\_list\_view.remove(“HTML”).
- Return not\_allowed\_in\_list\_view.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L2864) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L140)

<a id="op-c95b74cf1295aa"></a>
### Validate permissions for doctype

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_for_record_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, for\_remove, alert.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L3014) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L29) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L237)

<a id="op-01c49906aa268a"></a>
### Clear permissions cache

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_clear_permissions_cache`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L3223) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L138)

<a id="op-4039f1e6a45bf5"></a>
### Validate permissions

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, for\_remove, alert.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L4) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L22) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L230)

<a id="op-92c164807ba55b"></a>
### Validate permissions.get txt

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_get_text_resource`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L30) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L238)

<a id="op-1f678fcadd527e"></a>
### Validate permissions.check atleast one set

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_check_atleast_one_set`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L109) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L23) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L231)

<a id="op-3f523bff4639aa"></a>
### Validate permissions.check double

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_check_double`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Observed service boundaries** validation or user-notification service.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L294) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L24) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L232)

<a id="op-52653d27fd8bdd"></a>
### Validate permissions.check level zero is set

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_check_level_zero_is_set`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L602) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L27) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L235)

<a id="op-0f78902c5c79a6"></a>
### Validate permissions.check permission dependency

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_check_permission_dependency`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L7) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L28) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L236)

<a id="op-6da88caf258880"></a>
### Validate permissions.remove rights for single

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_remove_rights_for_single`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L8) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L31) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L239)

<a id="op-cf9219a738024b"></a>
### Validate permissions.check if submittable

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_check_if_submittable`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L26) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L234)

<a id="op-054e0355609a80"></a>
### Validate permissions.check if importable

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_check_if_importable`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L5) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L25) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L233)

<a id="op-c428bc25264236"></a>
### Validate permissions.validate permission for all role

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_permissions_validate_permission_for_all_role`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** d.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L9) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L32) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L240)

<a id="op-9f4917f96992f8"></a>
### Make module and roles

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_make_module_and_roles`

**Inputs** doc, perm\_fieldname = “permissions”.

**Record and data access** read “Domain” via exists · resolve a document from “Domain” via get\_doc · read “Module Def” via exists · resolve a document from mapping(“doctype” → “Module Def”, “module\_name” → doc.module) via get\_doc · read “Role” via exists.

**State and service calls** call insert on Platform.get\_doc(doctype = “Domain”, domain = doc.restrict\_to\_domain) · call insert on m · request new\_doc for “Role” · call insert on r.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - If (hasattr(doc, “restrict\_to\_domain”) and doc.restrict\_to\_domain and not Platform.db.exists(“Domain”, doc.restrict\_to\_domain)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(doc, “restrict\_to\_domain”) → doc.restrict\_to\_domain → not Platform.db.exists(“Domain”, doc.restrict\_to\_domain).
    - Evaluate Platform.get\_doc(doctype = “Domain”, domain = doc.restrict\_to\_domain).insert().
  - If “tabModule Def” belongs to Platform.db.get\_tables().
    - Bind dependencies reclaim\_module\_name\_for\_its\_app.
    - Evaluate reclaim\_module\_name\_for\_its\_app(doc.module).
    - If not Platform.db.exists(“Module Def”, doc.module).
      - Set m from Platform.get\_doc(mapping(“doctype” → “Module Def”, “module\_name” → doc.module)).
      - If Platform.scrub(doc.module) belongs to Platform.local.module\_app.
        - Set m.app\_name from Platform.local.module\_app at Platform.scrub(doc.module).
      - Otherwise.
        - Set m.app\_name from “Platform”.
      - Set m.flags.ignore\_mandatory, m.flags.ignore\_permissions from true.
      - If Platform.flags.package.
        - Set m.package from Platform.flags.package.name.
        - Set m.custom from 1.
      - Evaluate m.insert().
  - Set roles from (list of p.role for p drawn from (doc.get(“permissions”) or list()) + list(AUTOMATIC\_ROLES)).
    - Draw p from (doc.get(“permissions”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“permissions”) → list().
  - For each role in list(set(roles)).
    - If (Platform.db.table\_exists(“Role”, cached = false) and not Platform.db.exists(“Role”, role)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.table\_exists(“Role”, cached = false) → not Platform.db.exists(“Role”, role).
      - Set r from Platform.new\_doc(“Role”).
      - Set r.role\_name from role.
      - Set r.desk\_access from 1.
      - Set r.flags.ignore\_mandatory, r.flags.ignore\_permissions from true.
      - Evaluate r.insert().
- On failure (Platform.DoesNotExistError).
  - Take no action here.
- On failure (Platform.db.ProgrammingError) bound to e.
  - If Platform.db.is\_table\_missing(e).
    - Take no action here.
  - Otherwise.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L2747) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L142)

<a id="op-0e15cf8e9e6f02"></a>
### Check fieldname conflicts

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_check_fieldname_conflicts`

**Inputs** docfield.

**Record and data access** resolve a document from mapping(“doctype” → docfield.dt) via get\_doc.

**State and service calls** msgprint with msg.

**Local steps**

- Set doc from Platform.get\_doc(mapping(“doctype” → docfield.dt)).
- Set available\_objects from list of x for x drawn from dir(doc) where isinstance(x, str).
  - Draw x from dir(doc), keep a combination only if (isinstance(x, str)).
- Set property\_list from list of x for x drawn from available\_objects where is\_a\_property(getattr(type(doc), x, no value)).
  - Draw x from available\_objects, keep a combination only if (is\_a\_property(getattr(type(doc), x, no value))).
- Set method\_list from list of x for x drawn from available\_objects where (x does not belong to property\_list and callable(getattr(doc, x))).
  - Draw x from available\_objects, keep a combination only if ((x does not belong to property\_list and callable(getattr(doc, x)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in x does not belong to property\_list → callable(getattr(doc, x)).
- Set msg from translated “Fieldname {0} conflicting with meta object”.format(docfield.fieldname).
- If docfield.fieldname belongs to (method\_list + property\_list).
  - Evaluate Platform.msgprint(msg, raise\_exception = not docfield.is\_virtual).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(type(doc), x, no value), getattr(doc, x).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L109) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L136)

<a id="op-824b730e6a1de7"></a>
### Clear linked doctype cache

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_clear_linked_record_type_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.cache.delete\_value(“linked\_doctypes\_without\_ignore\_user\_permissions\_enabled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L4247) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L137)

<a id="op-1bf766a0b1bc08"></a>
### Check email append to

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_check_email_append_to`

**Inputs** doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated query text (SELECT) · validation helper — translated “Subject Field type should be Data, Text, Long Text, Small Text, Text Editor” · validation helper — translated “Sender Field should have Email in options”.

**Local steps**

- If (not hasattr(doc, “email\_append\_to”) or not doc.email\_append\_to).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(doc, “email\_append\_to”) → not doc.email\_append\_to.
  - Return no value.
- Set doc.subject\_field from doc.subject\_field.strip() when doc.subject\_field, otherwise no value.
  - Value choice on doc.subject\_field — true gives doc.subject\_field.strip(), false gives no value.
- Set subject\_field from get\_field(doc, doc.subject\_field).
- If (doc.subject\_field and not subject\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.subject\_field → not subject\_field.
  - Call the validation error handler Platform.throw(translated query text (SELECT)).
- If (subject\_field and subject\_field.fieldtype does not belong to list(“Data”, “Text”, “Long Text”, “Small Text”, …)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in subject\_field → subject\_field.fieldtype does not belong to list(“Data”, “Text”, “Long Text”, “Small Text”, …).
  - Call the validation error handler Platform.throw(translated “Subject Field type should be Data, Text, Long Text, Small Text, Text Editor”).
- Set doc.sender\_field from doc.sender\_field.strip() when doc.sender\_field, otherwise no value.
  - Value choice on doc.sender\_field — true gives doc.sender\_field.strip(), false gives no value.
- Set sender\_field from get\_field(doc, doc.sender\_field).
- If (doc.sender\_field and not sender\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sender\_field → not sender\_field.
  - Call the validation error handler Platform.throw(translated query text (SELECT)).
- If sender\_field.options differs from “Email”.
  - Call the validation error handler Platform.throw(translated “Sender Field should have Email in options”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L4297) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L135)

<a id="op-ce343cd00ffbcb"></a>
### Get field

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_get_field`

**Inputs** doc, fieldname.

**Explicit results** no value · field.

**Local steps**

- If not (doc or fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → fieldname.
  - Return no value.
- For each field in doc.fields.
  - If field.fieldname equals fieldname.
    - Return field.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L4912) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L139)

<a id="op-8b775d043670e9"></a>
### Get row size utilization

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_get_row_size_utilization`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Explicit results** flt(((Platform.db.get\_row\_size(doctype) ÷ Platform.db.MAX\_ROW\_SIZE\_LIMIT) × 100), 2) · 0.0.

**Local steps**

- Evaluate Platform.has\_permission(“DocType”, throw = true).
- Attempt the following.
  - Return flt(((Platform.db.get\_row\_size(doctype) ÷ Platform.db.MAX\_ROW\_SIZE\_LIMIT) × 100), 2).
- On failure (Exception).
  - Return 0.0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“DocType”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0069.json#L5031) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L141)

## Record · Doctype settings map

<a id="op-47314810924f1c"></a>
### Doc Type Settings Map.before naming

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_before_naming`

**Inputs** self.

**Local steps**

- Evaluate self.\_set\_default\_module().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default module](operations-038.md#op-fb3d353317b980).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L1677) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L291)

<a id="op-fb3d353317b980"></a>
### Doc Type Settings Map.set default module

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_set_default_module`

**Inputs** self.

**Record and data access** read “DocType” via get\_value.

**Local steps**

- If (self.is\_standard and not self.module).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → not self.module.
  - Set self.module from Platform.db.get\_value(“DocType”, self.applies\_to\_doctype, “module”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L1728) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L299)

<a id="op-a1d7f12aea42a1"></a>
### Doc Type Settings Map.autoname

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_autoname`

**Inputs** self.

**Local steps**

- Set self.name from self.applies\_to\_doctype.
- If self.is\_standard.
  - Set self.name from formatted text {self.applies\_to\_doctype} - {self.module}.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L1850) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L290)

<a id="op-2710faf96c25a6"></a>
### Doc Type Settings Map.validate

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_validate`

**Inputs** self.

**Local steps**

- Evaluate self.\_guard\_standard().
- Evaluate self.\_set\_default\_module().
- Evaluate self.\_validate\_unique\_per\_doctype().

If control reaches the end, it returns no value.

**Methods declared on this owner** [guard standard](operations-039.md#op-de86846acdf21f), [set default module](operations-038.md#op-fb3d353317b980), [validate unique per doctype](operations-039.md#op-07ad2c57c76446).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L1971) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L115) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L301)

<a id="op-1a03e94bce9ed3"></a>
### Doc Type Settings Map.on update

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.\_enforce\_single\_active().
- Evaluate self.export\_doc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [enforce single active](operations-039.md#op-efe753e3a8a84d), [export doc](operations-039.md#op-883f798454d362).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L2062) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L298)
