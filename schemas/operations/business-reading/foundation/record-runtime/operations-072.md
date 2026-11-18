# Record lifecycle and persistence · operations 72

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Platform

<a id="op-c869f36e99e194"></a>
### Whitelist.innerfn

`operation_foundation_initialize_business_behavior_whitelist_innerfn`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** fn.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L34) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L503)

<a id="op-c64d4f9dce65b9"></a>
### Is whitelisted

`operation_foundation_initialize_business_behavior_is_whitelisted`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** method.

**Locally raised failures** SessionExpired.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L24) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L477)

<a id="op-3d895e8a6d47ee"></a>
### Read only

`operation_foundation_initialize_business_behavior_read_only`

**Inputs** no declared parameters.

**Explicit results** innfn.

**Local steps**

- Bind local operation innfn for subsequent calls.
- Return innfn.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L27) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L488)

<a id="op-9d2e41e5ab098f"></a>
### Read only.innfn

`operation_foundation_initialize_business_behavior_read_only_innfn`

**Inputs** fn.

**Explicit results** wrapper\_fn.

**Local steps**

- Bind local operation wrapper\_fn for subsequent calls.
- Set wrapper\_fn.read\_only from true.
- Return wrapper\_fn.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L28) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L489)

<a id="op-28662c398f9ee9"></a>
### Read only.innfn.wrapper fn

`operation_foundation_initialize_business_behavior_read_only_innfn_wrapper_function`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(fn).

**Explicit results** retval.

**Local steps**

- Set switched\_connection from false.
- If conf.read\_from\_replica.
  - Set switched\_connection from connect\_replica().
- Attempt the following.
  - Set retval from fn(expanded args, expanded names get\_newargs(fn, kwargs)).
- On exit, including pending return or failure.
  - If (switched\_connection and hasattr(local, “primary\_db”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in switched\_connection → hasattr(local, “primary\_db”).
    - Evaluate local.db.close().
    - Set local.db from local.primary\_db.
- Return retval.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L7244) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L490)

<a id="op-15a79263eaec90"></a>
### Write only

`operation_foundation_initialize_business_behavior_write_only`

**Inputs** no declared parameters.

**Explicit results** innfn.

**Local steps**

- Bind local operation innfn for subsequent calls.
- Return innfn.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L7500) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L504)

<a id="op-75bb5e7e0b422b"></a>
### Write only.innfn

`operation_foundation_initialize_business_behavior_write_only_innfn`

**Inputs** fn.

**Explicit results** wrapper\_fn.

**Local steps**

- Bind local operation wrapper\_fn for subsequent calls.
- Return wrapper\_fn.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L7852) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L505)

<a id="op-748946abcf6796"></a>
### Write only.innfn.wrapper fn

`operation_foundation_initialize_business_behavior_write_only_innfn_wrapper_function`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(fn).

**Explicit results** retval.

**Local steps**

- Set primary\_db from getattr(local, “primary\_db”, no value).
- Set replica\_db from getattr(local, “replica\_db”, no value).
- Set in\_read\_only from getattr(local, “db”, no value) differs from primary\_db.
- If (in\_read\_only and primary\_db).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_read\_only → primary\_db.
  - Set local.db from local.primary\_db.
- Attempt the following.
  - Set retval from fn(expanded args, expanded names get\_newargs(fn, kwargs)).
- On exit, including pending return or failure.
  - If (in\_read\_only and replica\_db).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_read\_only → replica\_db.
    - Set local.db from replica\_db.
- Return retval.

**Values supplied outside this operation** selected callable from getattr(local, “primary\_db”, no value), getattr(local, “replica\_db”, no value) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L506)

<a id="op-6683934b17a928"></a>
### Only for

`operation_foundation_initialize_business_behavior_only_for`

**Inputs** roles, message = false.

**Explicit results** no value.

**Explicit failure paths** PermissionError.

**Local steps**

- If local.session.user equals “Administrator”.
  - Return no value.
- If isinstance(roles, str).
  - Set roles from tuple(roles).
- If set(roles).isdisjoint(get\_roles()).
  - If not message.
    - Raise PermissionError.
  - Evaluate throw(translated “This action is only allowed for {}”.format(“, ”.join(generator of bold(translated role) for role drawn from roles)), PermissionError, translated “Not Permitted”).
    - Draw role from roles.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L318) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L483)

<a id="op-95904a1e6600ce"></a>
### Get domain data

`operation_foundation_initialize_business_behavior_get_domain_data`

**Inputs** module.

**Explicit results** \_dict(get\_attr((get\_hooks(“domains”) at module at 0 + “.data”))) · \_dict().

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Set domain\_data from get\_hooks(“domains”).
  - If module belongs to domain\_data.
    - Return \_dict(get\_attr((get\_hooks(“domains”) at module at 0 + “.data”))).
  - Otherwise.
    - Return \_dict().
- On failure (ImportError).
  - If in\_test.
    - Return \_dict().
  - Otherwise.
    - Propagate the active failure.

**Values supplied outside this operation** selected callable from get\_hooks(“domains”), get\_attr((get\_hooks(“domains”) at module at 0 + “.data”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L19) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L453)

<a id="op-c89b4e801913bd"></a>
### Only has select perm

`operation_foundation_initialize_business_behavior_only_has_select_permission`

**Inputs** doctype, user = no value, ignore\_permissions = false.

**Explicit results** false · (permissions.get(“select”) and not permissions.get(“read”)).

**Local steps**

- If ignore\_permissions.
  - Return false.
- Bind dependencies get\_role\_permissions.
- Set user from (user or local.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → local.session.user.
- Set permissions from get\_role\_permissions(doctype, user = user).
- Return (permissions.get(“select”) and not permissions.get(“read”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in permissions.get(“select”) → not permissions.get(“read”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L918) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L484)

<a id="op-6e89ee3794045d"></a>
### Has permission

`operation_foundation_initialize_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, ptype, doc, user, throw, parent\_doctype, debug, ignore\_share\_permissions.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** PermissionError.

**Observed service boundaries** effective access lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L1125) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L467)

<a id="op-1c8e9488438533"></a>
### Has website permission

`operation_foundation_initialize_business_behavior_has_website_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, verbose, doctype.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Local structure** 7 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L21) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L468)

<a id="op-8fba134045bb2b"></a>
### Is table

`operation_foundation_initialize_business_behavior_is_table`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** doctype belongs to tables.

**Local steps**

- Set key from “is\_table”.
- Set tables from client\_cache.get\_value(key).
- If tables is identical to no value.
  - Set tables from db.get\_values(“DocType”, filters = mapping(“istable” → 1), order\_by = no value, pluck = true).
  - Evaluate client\_cache.set\_value(key, tables).
- Return doctype belongs to tables.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L2106) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L476)

<a id="op-33bc7e48d30565"></a>
### Get precision

`operation_foundation_initialize_business_behavior_get_precision`

**Inputs** doctype, fieldname, currency = no value, doc = no value.

**Declared result** int.

**Explicit results** get\_field\_precision(get\_meta(doctype).get\_field(fieldname), doc, currency).

**Local steps**

- Bind dependencies get\_field\_precision.
- Return get\_field\_precision(get\_meta(doctype).get\_field(fieldname), doc, currency).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L20) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L458)

<a id="op-6ca733c4de1f4e"></a>
### Generate hash

`operation_foundation_initialize_business_behavior_generate_hash`

**Inputs** txt = no value, length = 56.

**Declared result** str.

**Explicit results** secrets.token\_hex(math.ceil((length ÷ 2))) at slice no value to length.

**Local steps**

- Bind dependencies math.
- Bind dependencies secrets.
- If txt.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
- Return secrets.token\_hex(math.ceil((length ÷ 2))) at slice no value to length.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L2499) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L448)

<a id="op-c2dfe35ee75afb"></a>
### Set value

`operation_foundation_initialize_business_behavior_set_value`

**Inputs** doctype, docname, fieldname, value = no value.

**Explicit results** Platform.client.set\_value(doctype, docname, fieldname, value).

**Local steps**

- Bind dependencies Platform.client.
- Return Platform.client.set\_value(doctype, docname, fieldname, value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L2694) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L496)

<a id="op-a4593984a03ad1"></a>
### Get meta module

`operation_foundation_initialize_business_behavior_get_meta_module`

**Inputs** doctype.

**Explicit results** Platform.modules.load\_doctype\_module(doctype).

**Local steps**

- Bind dependencies Platform.modules.
- Return Platform.modules.load\_doctype\_module(doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L2798) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L456)

<a id="op-8e3bf4c91f7064"></a>
### Delete doc

`operation_foundation_initialize_business_behavior_delete_record`

**Inputs** doctype = no value, name = no value, force = false, ignore\_doctypes = no value, for\_reload = false, ignore\_permissions = false, flags = no value, ignore\_on\_trash = false, ignore\_missing = true, delete\_permanently = false.

**State and service calls** call delete\_doc on Platform.model.delete\_doc.

**Explicit results** Platform.model.delete\_doc.delete\_doc(doctype, name, force, ignore\_doctypes, …).

**Local steps**

- Bind dependencies Platform.model.delete\_doc.
- Return Platform.model.delete\_doc.delete\_doc(doctype, name, force, ignore\_doctypes, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L2866) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1702) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L445)

<a id="op-1e94ab8a809e87"></a>
### Reload doctype

`operation_foundation_initialize_business_behavior_reload_record_type`

**Inputs** doctype, force = false, reset\_permissions = false.

**Local steps**

- Evaluate reload\_doc(scrub(db.get\_value(“DocType”, doctype, “module”)), “doctype”, scrub(doctype), force = force, reset\_permissions = reset\_permissions).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L3175) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L493)

<a id="op-9e1939fe773705"></a>
### Reload doc

`operation_foundation_initialize_business_behavior_reload_record`

**Inputs** module, dt = no value, dn = no value, force = false, reset\_permissions = false.

**Explicit results** Platform.modules.reload\_doc(module, dt, dn, force = force, reset\_permissions = reset\_permissions).

**Local steps**

- Bind dependencies Platform.modules.
- Return Platform.modules.reload\_doc(module, dt, dn, force = force, reset\_permissions = reset\_permissions).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L3345) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L492)

<a id="op-d5889d9a5f9ed3"></a>
### Rename doc

`operation_foundation_initialize_business_behavior_rename_record`

**Inputs** doctype, old, new, force = false, merge = false, ignore\_if\_exists (named only, default false), show\_alert (named only, default true), rebuild\_search (named only, default true).

**Wrappers, in declaration order** whitelist(methods = list(“POST”, “PUT”)).

**Declared result** str.

**Explicit results** rename\_doc(doctype = doctype, old = old, new = new, force = force, …).

**Local steps**

- Bind dependencies rename\_doc.
- Return rename\_doc(doctype = doctype, old = old, new = new, force = force, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L3523) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L494)

<a id="op-ad3ee90c798d84"></a>
### Get module

`operation_foundation_binding_foundation_init_get_module`

**Inputs** modulename.

**Explicit results** importlib.import\_module(modulename).

**Local steps**

- Return importlib.import\_module(modulename).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L33) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1465)

<a id="op-944b3657e50784"></a>
### Scrub

`operation_foundation_binding_foundation_init_scrub`

**Inputs** txt.

**Declared result** str.

**Explicit results** nested operand in the contract(nested operand in the contract).replace(one space, “\_”).replace(“-”, “\_”).lower().

**Local steps**

- Return nested operand in the contract(nested operand in the contract).replace(one space, “\_”).replace(“-”, “\_”).lower().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1473)
