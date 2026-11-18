# Shared value and file services · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Inplacevar

<a id="op-c65a3151fcd491"></a>
### Irshift

`operation_foundation_utils_inplacevar_business_behavior_irshift`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using shift right y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2878) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L294)

<a id="op-dcfb8a7162b398"></a>
### Iand

`operation_foundation_utils_inplacevar_business_behavior_iand`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using bitwise and y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2934) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L286)

<a id="op-b80febf6c5f750"></a>
### Ixor

`operation_foundation_utils_inplacevar_business_behavior_ixor`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using exclusive or y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L2990) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L296)

<a id="op-dad14e11834077"></a>
### Ior

`operation_foundation_utils_inplacevar_business_behavior_ior`

**Inputs** x, y.

**Explicit results** x.

**Local steps**

- Update x using bitwise or y.
- Return x.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L3046) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L292)

<a id="op-cedc97a1db7719"></a>
### Protected inplacevar

`operation_foundation_utils_inplacevar_business_behavior_protected_inplacevar`

**Inputs** op, var, expr.

**Explicit results** inplace\_ops at op(var, expr).

**Explicit failure paths** TypeError((“Augmented assignment to %s objects is not allowed in untrusted code” modulo or format cls.\_\_name\_\_)).

**Local steps**

- If (hasattr(var, inplace\_slots at op) and not isinstance(var, valid\_inplace\_types)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(var, inplace\_slots at op) → not isinstance(var, valid\_inplace\_types).
  - Attempt the following.
    - Set cls from var.\_\_class\_\_.
  - On failure (AttributeError).
    - Set cls from type(var).
  - Raise TypeError((“Augmented assignment to %s objects is not allowed in untrusted code” modulo or format cls.\_\_name\_\_)).
- Return inplace\_ops at op(var, expr).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L3102) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L297)

## Service · Install

<a id="op-29e278c89201b2"></a>
### Before install

`operation_foundation_utils_install_business_behavior_before_install`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.reload\_doc(“core”, “doctype”, “doctype\_state”).
- Evaluate Platform.reload\_doc(“core”, “doctype”, “docfield”).
- Evaluate Platform.reload\_doc(“core”, “doctype”, “docperm”).
- Evaluate Platform.reload\_doc(“core”, “doctype”, “doctype\_action”).
- Evaluate Platform.reload\_doc(“core”, “doctype”, “doctype\_link”).
- Evaluate Platform.reload\_doc(“desk”, “doctype”, “form\_tour\_step”).
- Evaluate Platform.reload\_doc(“desk”, “doctype”, “form\_tour”).
- Evaluate Platform.reload\_doc(“core”, “doctype”, “doctype”).
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L3338) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L300)

<a id="op-92d50bd99a2a53"></a>
### After install

`operation_foundation_utils_install_business_behavior_after_install`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Print Settings” via get\_doc · resolve a document from “User” via get\_doc · read “Role” via get\_all.

**State and service calls** call save on print\_settings · commit.

**Local steps**

- Evaluate create\_user\_type().
- Evaluate install\_basic\_docs().
- Bind dependencies make\_home\_folder.
- Bind dependencies sync\_languages.
- Evaluate make\_home\_folder().
- Evaluate import\_country\_and\_currency().
- Evaluate sync\_languages().
- Set print\_settings from Platform.get\_doc(“Print Settings”).
- Evaluate print\_settings.save().
- Evaluate Platform.get\_doc(“User”, “Administrator”).add\_roles(expanded Platform.get\_all(“Role”, pluck = “name”)).
- Evaluate update\_password(“Administrator”, get\_admin\_password()).
- If not Platform.conf.skip\_setup\_wizard.
  - If not Platform.db.get\_default(“desktop:home\_page”).
    - Evaluate Platform.db.set\_default(“desktop:home\_page”, “setup-wizard”).
- Bind dependencies \_clear\_test\_log.
- Evaluate \_clear\_test\_log().
- Evaluate add\_standard\_navbar\_items().
- Evaluate install\_notification\_types().
- Evaluate install\_notification\_templates().
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L3687) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L299)

<a id="op-2360c82979c310"></a>
### Create user type

`operation_foundation_utils_install_business_behavior_create_user_type`

**Inputs** no declared parameters.

**Record and data access** read “User Type” via exists · resolve a document from mapping(“doctype” → “User Type”, “name” → user\_type, “is\_standard” → 1) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “User Type”, “name” → user\_type, “is\_standard” → 1)).

**Local steps**

- For each user\_type in list(“System User”, “Website User”).
  - If not Platform.db.exists(“User Type”, user\_type).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “User Type”, “name” → user\_type, “is\_standard” → 1)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L4162) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L304)

<a id="op-38d3c9afc77e7a"></a>
### Install basic docs

`operation_foundation_utils_install_business_behavior_install_basic_records`

**Inputs** no declared parameters.

**Record and data access** resolve a document from d via get\_doc.

**State and service calls** call insert on Platform.get\_doc(d).

**Local steps**

- Set install\_docs from list(mapping(“doctype” → “User”, “name” → “Administrator”, “first\_name” → “Administrator”, “email” → “admin@example.com”, …), mapping(“doctype” → “User”, “name” → “Guest”, “first\_name” → “Guest”, “email” → ….
- For each d in install\_docs.
  - Attempt the following.
    - Evaluate Platform.get\_doc(d).insert(ignore\_if\_duplicate = true).
  - On failure (Platform.NameError).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L4350) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L307)

<a id="op-a53709048e37ab"></a>
### Get admin password

`operation_foundation_utils_install_business_behavior_get_admin_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L5163) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L306)

<a id="op-c0981c9106ce33"></a>
### Before tests

`operation_foundation_utils_install_business_behavior_before_tests`

**Inputs** no declared parameters.

**State and service calls** request truncate on “Custom Field” · request truncate on “Event” · request set\_single\_value on “Website Settings” · commit.

**Explicit results** no value.

**Local steps**

- If len(Platform.get\_installed\_apps()) &gt; 1.
  - Return no value.
- Evaluate Platform.db.truncate(“Custom Field”).
- Evaluate Platform.db.truncate(“Event”).
- Evaluate Platform.clear\_cache().
- If not Platform.is\_setup\_complete().
  - Evaluate complete\_setup\_wizard().
- Evaluate Platform.db.set\_single\_value(“Website Settings”, “disable\_signup”, 0).
- Evaluate Platform.db.commit().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L5239) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L301)

<a id="op-40c58537aa2a58"></a>
### Complete setup wizard

`operation_foundation_utils_install_business_behavior_complete_setup_wizard`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies setup\_complete.
- Evaluate setup\_complete(mapping(“language” → “English”, “email” → “test@Enterprise.com”, “full\_name” → “Test User”, “password” → “test”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L5522) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L302)

<a id="op-50cfc8c09c27b6"></a>
### Add standard navbar items

`operation_foundation_utils_install_business_behavior_add_standard_navbar_items`

**Inputs** no declared parameters.

**Record and data access** read “Navbar Settings” via get\_single.

**State and service calls** call save on navbar\_settings.

**Explicit results** no value.

**Local steps**

- Set navbar\_settings from Platform.get\_single(“Navbar Settings”).
- If (navbar\_settings.settings\_dropdown and navbar\_settings.help\_dropdown).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in navbar\_settings.settings\_dropdown → navbar\_settings.help\_dropdown.
  - Return no value.
- Set navbar\_settings.settings\_dropdown from list().
- Set navbar\_settings.help\_dropdown from list().
- For each item in Platform.get\_hooks(“standard\_navbar\_items”).
  - Evaluate navbar\_settings.append(“settings\_dropdown”, item).
- For each item in Platform.get\_hooks(“standard\_help\_items”).
  - Evaluate navbar\_settings.append(“help\_dropdown”, item).
- Evaluate navbar\_settings.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“standard\_navbar\_items”), Platform.get\_hooks(“standard\_help\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L5744) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L298)

<a id="op-3e8add003d6c64"></a>
### Create desktop icons for app

`operation_foundation_utils_install_business_behavior_create_desktop_icons_for_application`

**Inputs** app\_name = no value.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- Bind dependencies is\_desktop\_icons\_page.
- If not is\_desktop\_icons\_page().
  - Return no value.
- Bind dependencies create\_desktop\_icons.
- Attempt the following.
  - Evaluate create\_desktop\_icons().
  - Evaluate Platform.db.commit().
- On failure (Exception) bound to e.
  - Evaluate print(formatted text Error creating desktop icons: {e}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L6016) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L303)

<a id="op-a87788d6d5ee97"></a>
### Delete desktop icons for app

`operation_foundation_utils_install_business_behavior_delete_desktop_icons_for_application`

**Inputs** app\_name, dry\_run = false.

**Record and data access** read “Desktop Icon” via get\_all.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- If dry\_run.
  - Return no value.
- Set app\_title from (Platform.get\_hooks(“app\_title”, app\_name = app\_name) or list(no value)) at 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = app\_name) → list(no value).
- If not app\_title.
  - Return no value.
- Set icons\_to\_delete from Platform.get\_all(“Desktop Icon”, pluck = “name”, or\_filters = list(list(“Desktop Icon”, “name”, “=”, app\_title), list(“Desktop Icon”, “parent\_icon”, “=”, app\_title))).
- For each icon in icons\_to\_delete.
  - Evaluate Platform.delete\_doc\_if\_exists(“Desktop Icon”, icon).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”, app\_name = app\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L6188) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L305)

## Service · Island

<a id="op-246f7388412299"></a>
### Page island name

`operation_foundation_utils_island_business_behavior_page_island_name`

**Inputs** app, page.

**Declared result** str.

**Explicit results** formatted text {app}.{PAGE\_ISLAND\_INFIX}.{page}.

**Local steps**

- Return formatted text {app}.{PAGE\_ISLAND\_INFIX}.{page}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0484.json#L6522) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L310)

<a id="op-cf32bd566e55fe"></a>
### Get ui islands

`operation_foundation_utils_island_business_behavior_get_user_interface_islands`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** sorted(generator of name for tuple(key, url) drawn from get\_assets\_json().items() where (name bound to island\_name(key) and island\_app(name, url) belongs to installed)).

**Local steps**

- Set installed from set(Platform.get\_installed\_apps()).
- Return sorted(generator of name for tuple(key, url) drawn from get\_assets\_json().items() where (name bound to island\_name(key) and island\_app(name, url) belongs to installed)).
  - Draw tuple(key, url) from get\_assets\_json().items(), keep a combination only if ((name bound to island\_name(key) and island\_app(name, url) belongs to installed)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name bound to island\_name(key) → island\_app(name, url) belongs to installed.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L136) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L309)

<a id="op-a2b1eeca08313f"></a>
### Island name

`operation_foundation_binding_foundation_utils_island_island_name`

**Inputs** asset\_key.

**Declared result** (str bitwise or no value).

**Explicit results** asset\_key.removesuffix(ISLAND\_JS\_SUFFIX).

**Local steps**

- If asset\_key.endswith(ISLAND\_JS\_SUFFIX).
  - Return asset\_key.removesuffix(ISLAND\_JS\_SUFFIX).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L58) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L216)

<a id="op-db073ed389db78"></a>
### Island app

`operation_foundation_binding_foundation_utils_island_island_app`

**Inputs** name, url.

**Declared result** (str bitwise or no value).

**Explicit results** app · match.group(1).

**Local steps**

- Set tuple(app, infix, \_page) from name.partition(formatted text .{PAGE\_ISLAND\_INFIX}.).
- If infix.
  - Return app.
- If match bound to ASSET\_APP.match(url).
  - Return match.group(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L57) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L215)

<a id="op-ecadd8fb874bbb"></a>
### Get island assets

`operation_foundation_utils_island_business_behavior_get_island_assets`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“js” → js, “css” → (assets\_json.get((name + ISLAND\_CSS\_SUFFIX)) or no value)).

**Explicit failure paths** validation helper — translated “Island "{0}" is not on this site. Build the app that ships it.”.format(name).

**Local steps**

- Set assets\_json from get\_assets\_json().
- Set js from assets\_json.get((name + ISLAND\_JS\_SUFFIX)) when name belongs to get\_ui\_islands(), otherwise no value.
  - Value choice on name belongs to get\_ui\_islands() — true gives assets\_json.get((name + ISLAND\_JS\_SUFFIX)), false gives no value.
- If not js.
  - Call the validation error handler Platform.throw(translated “Island "{0}" is not on this site. Build the app that ships it.”.format(name)).
- Return mapping(“js” → js, “css” → (assets\_json.get((name + ISLAND\_CSS\_SUFFIX)) or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in assets\_json.get((name + ISLAND\_CSS\_SUFFIX)) → no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L135) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L308)

## Service · Jinja

<a id="op-523efcb91115dd"></a>
### Get jenv

`operation_foundation_utils_template_evaluation_business_behavior_get_jenv`

**Inputs** restrict\_globals (named only, default no value).

**Explicit results** jenv.

**Local steps**

- Bind dependencies Platform.
- Bind dependencies get\_safe\_globals, is\_render\_exec\_enabled, render\_safe\_globals.
- If restrict\_globals is identical to no value.
  - Set restrict\_globals from is\_render\_exec\_enabled().
- Set local\_key from “jenv\_restricted” when restrict\_globals, otherwise “jenv\_unrestricted”.
  - Value choice on restrict\_globals — true gives “jenv\_restricted”, false gives “jenv\_unrestricted”.
- If jenv bound to getattr(Platform.local, local\_key, no value).
  - Return jenv.
- Set default\_jenv from \_get\_jenv().
- Set jenv from default\_jenv.overlay().
- If not Platform.\_dev\_server.
  - Set jenv.cache from default\_jenv.cache.
- Set jenv.globals from default\_jenv.globals.copy().
- Set jenv.filters from default\_jenv.filters.copy().
- If restrict\_globals.
  - Evaluate jenv.globals.update(render\_safe\_globals()).
- Otherwise.
  - Evaluate jenv.globals.update(get\_safe\_globals()).
- Set tuple(methods, filters) from get\_jinja\_hooks().
- Evaluate jenv.globals.update((methods or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in methods → mapping().
- Evaluate jenv.filters.update((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Evaluate setattr(Platform.local, local\_key, jenv).
- Return jenv.

**Values supplied outside this operation** selected callable from getattr(Platform.local, local\_key, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2036) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L802)

<a id="op-c84482ff3de701"></a>
### Get jenv

`operation_foundation_utils_template_evaluation_business_behavior_get_jenv_2`

**Inputs** no declared parameters.

**Wrappers, in declaration order** site\_cache(ttl = (10 × 60), maxsize = 4).

**Explicit results** jenv.

**Local steps**

- Bind dependencies DebugUndefined.
- Bind dependencies SandboxedEnvironment.
- Bind dependencies UNSAFE\_ATTRIBUTES.
- Set UNSAFE\_ATTRIBUTES from (UNSAFE\_ATTRIBUTES − set(“format”, “format\_map”)).
- Bind local type PlatformSandboxedEnvironment (class body executes during definition).
- Set jenv from PlatformSandboxedEnvironment(loader = get\_jloader(), undefined = DebugUndefined, cache\_size = 32).
- Evaluate set\_filters(jenv).
- Return jenv.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L550) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2037) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L803)

<a id="op-fab3cb81e87ca2"></a>
### Get jenv.Platform Sandboxed Environment.is safe attribute

`operation_foundation_utils_template_evaluation_business_behavior_get_jenv_foundation_sandboxed_environment_is_safe_attribute`

**Inputs** self, obj, attr, remaining positional values args, remaining named values kwargs.

**Explicit results** false · super().is\_safe\_attribute(obj, attr, expanded args, expanded names kwargs).

**Local steps**

- If attr belongs to UNSAFE\_ATTRIBUTES.
  - Return false.
- Return super().is\_safe\_attribute(obj, attr, expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L901) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2038) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L804)

<a id="op-4626fef91eb833"></a>
### Get template

`operation_foundation_utils_template_evaluation_business_behavior_get_template`

**Inputs** path.

**Explicit results** jenv.get\_template(path, globals = jenv.globals).

**Local steps**

- Set jenv from get\_jenv().
- Return jenv.get\_template(path, globals = jenv.globals).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L1035) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2041) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L807)
