# Record lifecycle and persistence · operations 71

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Permission type

[Record definition](../../../../data/record-types/permission_type.json)

<a id="op-9e146398da41bd"></a>
### Permission Type.on trash

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_on_trash`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L6701) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L35)

<a id="op-44c9afde9cbc15"></a>
### Permission Type.delete custom field

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_delete_custom_field`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, target.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L6975) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L33)

<a id="op-f392cca7087b40"></a>
### Permission Type.custom field exists

`operation_foundation_core_record_definitions_permission_type_business_behavior_permission_type_custom_field_exists`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, target.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L32)

<a id="op-cd2e869536d7b9"></a>
### Get doctype ptype map

`operation_foundation_core_record_definitions_permission_type_business_behavior_get_record_type_ptype_map`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0093.json#L119) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L26)

## Report · Permitted documents for user

<a id="op-ac0d2c8d74f311"></a>
### Execute

`operation_foundation_core_report_permitted_documents_for_user_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read doctype via get\_list · resolve a document from doctype via get\_doc.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set tuple(user, doctype, show\_permissions) from tuple(filters.get(“user”), filters.get(“doctype”), filters.get(“show\_permissions”)).
- Set tuple(columns, fields) from get\_columns\_and\_fields(doctype).
- Set data from Platform.get\_list(doctype, fields = fields, as\_list = true, user = user).
- If show\_permissions.
  - Set rights from get\_rights(doctype).
  - Set columns from (columns + list of (Platform.unscrub(right) + “:Check:80”) for right drawn from rights).
    - Draw right from rights.
  - Set data from list(data).
  - For each tuple(i, doc) in enumerate(data).
    - Set permission from Platform.permissions.get\_doc\_permissions(Platform.get\_doc(doctype, doc at 0), user).
    - Set data at i from (doc + tuple(generator of permission.get(right) for right drawn from rights)).
      - Draw right from rights.
- Return tuple(columns, data).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L3613) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L904)

<a id="op-f2d16c3b347f63"></a>
### Get columns and fields

`operation_foundation_core_report_permitted_documents_for_user_business_behavior_get_columns_and_fields`

**Inputs** doctype.

**Explicit results** tuple(columns, fields).

**Local steps**

- Set columns from list(formatted text Name:Link/{doctype}:200).
- Set fields from list(“name”).
- For each df in Platform.get\_meta(doctype).fields.
  - If (df.in\_list\_view and df.fieldtype belongs to data\_fieldtypes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.in\_list\_view → df.fieldtype belongs to data\_fieldtypes.
    - Evaluate fields.append(formatted text ′{df.fieldname}′).
    - Set fieldtype from formatted text Link/{df.options} when df.fieldtype equals “Link”, otherwise df.fieldtype.
      - Value choice on df.fieldtype equals “Link” — true gives formatted text Link/{df.options}, false gives df.fieldtype.
    - Evaluate columns.append(formatted text {df.label}:{fieldtype}:{(df.width or 100)}).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.width → 100.
- Return tuple(columns, fields).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L4174) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L905)

<a id="op-258959bd000e65"></a>
### Query doctypes

`operation_foundation_core_report_permitted_documents_for_user_business_behavior_query_record_types`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “DocType” via get\_values.

**Explicit results** list of list(dt) for dt drawn from can\_read where (nested operand in the contract.lower().replace(“%”, empty text) belongs to nested operand in the contract.\_(dt).lower() and (include\_single\_doctypes or dt ….

**Local steps**

- Set user from filters.get(“user”).
- Set user\_perms from Platform.utils.user.UserPermissions(user).
- Evaluate user\_perms.build\_permissions().
- Set can\_read from user\_perms.can\_read.
- Set include\_single\_doctypes from filters.get(“include\_single\_doctypes”).
- Set single\_doctypes from list of d at 0 for d drawn from Platform.db.get\_values(“DocType”, mapping(“issingle” → 1)).
  - Draw d from Platform.db.get\_values(“DocType”, mapping(“issingle” → 1)).
- Return list of list(dt) for dt drawn from can\_read where (nested operand in the contract.lower().replace(“%”, empty text) belongs to nested operand in the contract.\_(dt).lower() and (include\_single\_doctypes or dt ….
  - Draw dt from can\_read, keep a combination only if ((txt.lower().replace(“%”, empty text) belongs to Platform.\_(dt).lower() and (include\_single\_doctypes or dt does not belong to single\_doctypes))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in txt.lower().replace(“%”, empty text) belongs to Platform.\_(dt).lower() → (include\_single\_doctypes or dt does not belong to single\_doctypes).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in include\_single\_doctypes → dt does not belong to single\_doctypes.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0120.json#L4551) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L906)

## Service · Platform

<a id="op-c244531bbd9ded"></a>
### Init

`operation_foundation_initialize_business_behavior_initialize`

**Inputs** site, sites\_path = “.”, new\_site = false, force = false, is\_request (named only, default false), is\_job (named only, default false).

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** ValueError(formatted text Invalid site name ′{site}′).

**Local steps**

- If force.
  - Evaluate release\_local(local).
- If getattr(local, “initialised”, no value).
  - Return no value.
- If (site and not SITE\_NAME\_PATTERN.match(site)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in site → not SITE\_NAME\_PATTERN.match(site).
  - Raise ValueError(formatted text Invalid site name ′{site}′).
- Set local.error\_log from list().
- Set local.message\_log from list().
- Set local.debug\_log from list().
- Set local.flags from \_dict(mapping(“currently\_saving” → list(), “redirect\_location” → empty text, “in\_install\_db” → false, “in\_import” → false, …)).
- Set local.locked\_documents from list().
- Set local.test\_objects from defaultdict(list).
- Set local.site from site.
- Set local.site\_name from site.
- Set local.sites\_path from sites\_path.
- Set site\_path from os.path.join(sites\_path, site).
- Set local.site\_path from site\_path.
- Set local.all\_apps from no value.
- Set local.request\_ip from no value.
- Set local.response from \_dict(mapping(“docs” → list())).
- Set local.response\_headers from Headers().
- Set local.task\_id from no value.
- Set local.conf from get\_site\_config(sites\_path = sites\_path, site\_path = site\_path, cached = is\_request).
- Set local.lang from (local.conf.lang or “en”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in local.conf.lang → “en”.
- Set local.module\_app from no value.
- Set local.app\_modules from no value.
- Set local.user from no value.
- Set local.user\_perms from no value.
- Set local.role\_permissions from mapping().
- Set local.valid\_columns from mapping().
- Set local.new\_doc\_templates from mapping().
- Set local.request\_cache from defaultdict(dict).
- Set local.jenv\_restricted from no value.
- Set local.jenv\_unrestricted from no value.
- Set local.jloader from no value.
- Set local.cache from mapping().
- Set local.form\_dict from \_dict().
- Set local.preload\_assets from mapping(“style” → list(), “script” → list(), “icons” → list()).
- Set local.session from \_dict(user = “Guest”, data = \_dict()).
- Set local.dev\_server from \_dev\_server.
- Set local.qb from get\_query\_builder(local.conf.db\_type).
- If (not cache or not client\_cache).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cache → not client\_cache.
  - Evaluate setup\_redis\_cache\_connection().
- Evaluate setup\_module\_map(include\_all\_apps = not (is\_request or is\_job or Platform.flags.in\_migrate)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_request → is\_job → Platform.flags.in\_migrate.
- Set local.initialised from true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(local, “initialised”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L22) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L471)

<a id="op-d3a344e24f76b0"></a>
### Connect

`operation_foundation_initialize_business_behavior_connect`

**Inputs** site = no value, db\_name = no value, set\_admin\_as\_user = true.

**Declared result** no value.

**Local steps**

- Bind dependencies get\_db.
- If site.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
  - Evaluate init(site).
- If db\_name.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
- Set conf from local.conf.
- Set db\_user from (conf.db\_user or db\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.db\_user → db\_name.
- Set db\_name\_ from (conf.db\_name or db\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.db\_name → db\_name.
- Set db\_password from conf.db\_password.
- Require db\_name\_ or report “site must be fully initialized, db\_name missing”.
- If Platform.conf.db\_type belongs to tuple(“mariadb”, “postgres”).
  - Require db\_user or report “site must be fully initialized, db\_user missing”.
  - Require db\_password or report “site must be fully initialized, db\_password missing”.
- Set local.db from get\_db(socket = conf.db\_socket, host = conf.db\_host, port = conf.db\_port, user = db\_user, …).
- If set\_admin\_as\_user.
  - Evaluate set\_user(“Administrator”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L2961) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L443)

<a id="op-bb868f10eb0cd6"></a>
### Connect replica

`operation_foundation_initialize_business_behavior_connect_replica`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Bind dependencies get\_db.
- If (hasattr(local, “replica\_db”) and hasattr(local, “primary\_db”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(local, “replica\_db”) → hasattr(local, “primary\_db”).
  - Return false.
- Set user from local.conf.db\_user.
- Set password from local.conf.db\_password.
- Set port from local.conf.replica\_db\_port.
- If local.conf.different\_credentials\_for\_replica.
  - Set user from (local.conf.replica\_db\_user or local.conf.replica\_db\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in local.conf.replica\_db\_user → local.conf.replica\_db\_name.
  - Set password from local.conf.replica\_db\_password.
- Set local.replica\_db from get\_db(socket = no value, host = local.conf.replica\_host, port = port, user = user, …).
- Set local.primary\_db from local.db.
- Set local.db from local.replica\_db.
- If hasattr(Platform.local, “\_recorder”).
  - Evaluate Platform.local.\_recorder.\_patch\_sql(local.db).
- Return true.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L3467) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L444)

<a id="op-c927320de835de"></a>
### Init site.initialize

`operation_foundation_initialize_business_behavior_initialize_site_initialize`

**Inputs** self, site = no value.

**Local steps**

- Set self.site from (site or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → empty text.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L3908) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L474)

<a id="op-7c04eddae2c664"></a>
### Init site.enter context

`operation_foundation_initialize_business_behavior_initialize_site_enter`

**Inputs** self.

**Explicit results** local.

**Local steps**

- Evaluate init(self.site).
- Return local.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L3975) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L472)

<a id="op-4eaa7b86b27b35"></a>
### Init site.exit context

`operation_foundation_initialize_business_behavior_initialize_site_exit`

**Inputs** self, type, value, traceback.

**Local steps**

- Evaluate destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4038) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L473)

<a id="op-7b95d92cfab2e2"></a>
### Destroy

`operation_foundation_initialize_business_behavior_destroy`

**Inputs** no declared parameters.

**Local steps**

- Attempt the following.
  - If db.
    - Evaluate db.close().
- On exit, including pending return or failure.
  - Evaluate release\_local(local).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4106) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L446)

<a id="op-0a83b7d3ce9559"></a>
### Setup redis cache connection

`operation_foundation_initialize_business_behavior_setup_cache_service_cache_connection`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies ClientCache, setup\_cache.
- Use module bindings cache.
- Use module bindings client\_cache.
- Within \_redis\_init\_lock.
  - If not cache.
    - Set cache from setup\_cache().
    - Set client\_cache from ClientCache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4189) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L497)

<a id="op-e92bc544a4a933"></a>
### Errprint

`operation_foundation_initialize_business_behavior_errprint`

**Inputs** msg.

**Declared result** no value.

**Local steps**

- Set msg from as\_unicode(msg).
- If (not request or “cmd” does not belong to local.form\_dict or conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not request → “cmd” does not belong to local.form\_dict → conf.developer\_mode.
  - Evaluate print(msg).
- Evaluate error\_log.append(mapping(“exc” → msg)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4311) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L447)

<a id="op-248f12442ca0c6"></a>
### Print sql

`operation_foundation_initialize_business_behavior_print_database_query`

**Inputs** enable = true.

**Declared result** no value.

**Explicit failure paths** validation helper — “′Platform.print\_sql′ only works with ′allow\_tests′ site config enabled.”.

**Local steps**

- If not local.conf.allow\_tests.
  - Call the validation error handler Platform.throw(“′Platform.print\_sql′ only works with ′allow\_tests′ site config enabled.”).
- Evaluate client\_cache.set\_value(“flag\_print\_sql”, enable).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4482) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L487)

<a id="op-8c15cd4f9ef9f6"></a>
### Log

`operation_foundation_initialize_business_behavior_log`

**Inputs** msg.

**Declared result** no value.

**Local steps**

- Evaluate print(msg, file = sys.stderr).
- Evaluate debug\_log.append(as\_unicode(msg)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4599) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L480)

<a id="op-f482909cf5872d"></a>
### Set user

`operation_foundation_initialize_business_behavior_set_user`

**Inputs** username.

**Local steps**

- Set local.session.user from username.
- Set local.session.sid from username.
- Set local.cache from mapping().
- Set local.form\_dict from \_dict().
- Set local.jenv\_restricted from no value.
- Set local.jenv\_unrestricted from no value.
- Set local.session.data from \_dict().
- Set local.role\_permissions from mapping().
- Set local.new\_doc\_templates from mapping().
- Set local.user\_perms from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4706) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L495)

<a id="op-73acdd3bf27c4c"></a>
### Get user

`operation_foundation_initialize_business_behavior_get_user`

**Inputs** no declared parameters.

**Explicit results** local.user\_perms.

**Local steps**

- Bind dependencies UserPermissions.
- If not local.user\_perms.
  - Set local.user\_perms from UserPermissions(local.session.user).
- Return local.user\_perms.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L4934) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L464)

<a id="op-d1f13ba03005bd"></a>
### Get roles

`operation_foundation_initialize_business_behavior_get_roles`

**Inputs** username = no value.

**Declared result** list at str.

**Explicit results** list(“Guest”) · Platform.permissions.get\_roles((username or local.session.user)).

**Local steps**

- If (not local.session or not local.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not local.session → not local.session.user.
  - Return list(“Guest”).
- Bind dependencies Platform.permissions.
- Return Platform.permissions.get\_roles((username or local.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in username → local.session.user.

**Values supplied outside this operation** effective access from Platform.permissions.get\_roles((username or local.session.user)).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L5033) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L463)

<a id="op-1e9739f12317f9"></a>
### Get request header

`operation_foundation_initialize_business_behavior_get_request_header`

**Inputs** key, default = no value.

**Explicit results** request.headers.get(key, default).

**Local steps**

- Return request.headers.get(key, default).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L5186) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L462)

<a id="op-90c93050f3f36d"></a>
### In request or test

`operation_foundation_initialize_business_behavior_in_request_or_test`

**Inputs** no declared parameters.

**Explicit results** (getattr(local, “request”, no value) or in\_test).

**Local steps**

- Return (getattr(local, “request”, no value) or in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(local, “request”, no value) → in\_test.

**Values supplied outside this operation** selected callable from getattr(local, “request”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0002.json#L5258) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L470)

<a id="op-a7f7a459a27fe7"></a>
### Whitelist

`operation_foundation_initialize_business_behavior_whitelist`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** allow\_guest, xss\_safe, methods.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L33) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L502)
