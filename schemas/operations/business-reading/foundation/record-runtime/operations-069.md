# Record lifecycle and persistence · operations 69

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Page

[Record definition](../../../../data/record-types/page.json)

<a id="op-c3be235312309a"></a>
### Page.get folder path

`operation_foundation_core_record_definitions_page_business_behavior_page_get_folder_path`

**Inputs** self.

**Declared result** str.

**Explicit results** os.path.join(get\_module\_path(self.module), “page”, Platform.scrub(self.name)).

**Local steps**

- Return os.path.join(get\_module\_path(self.module), “page”, Platform.scrub(self.name)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L2215) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1735)

<a id="op-4aabe24c60915d"></a>
### Page.get permission log options

`operation_foundation_core_record_definitions_page_business_behavior_page_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L2329) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1737)

<a id="op-599a9a3231f213"></a>
### Page.on update

`operation_foundation_core_record_definitions_page_business_behavior_page_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.do\_not\_update\_json.
  - Return no value.
- Bind dependencies make\_module\_and\_roles.
- Evaluate make\_module\_and\_roles(self, “roles”).
- Bind dependencies export\_module\_json.
- Set path from export\_module\_json(self, self.standard equals “Yes”, self.module).
- If not path.
  - Return no value.
- If self.type equals “Platform UI”.
  - If not self.island.
    - Evaluate self.write\_island\_boilerplate(path).
- Otherwise.
  - If not os.path.exists((path + “.js”)).
    - Within open((path + “.js”), “w”) bound as f.
      - Evaluate f.write(formatted text Platform.pages&#91;'{self.name}'&#93;.on\_page\_load = function(wrapper) {  var page = Platform.ui.make\_app\_page({  parent: wrapper,  title: '{self.title}',  ).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write island boilerplate](operations-069.md#op-d9963f31689755).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L86) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1741)

<a id="op-d9963f31689755"></a>
### Page.write island boilerplate

`operation_foundation_core_record_definitions_page_business_behavior_page_write_island_boilerplate`

**Inputs** self, path.

**Local steps**

- Set title from (self.title or self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.title → self.name.
- If not os.path.exists((path + “.island.js”)).
  - Within open((path + “.island.js”), “w”) bound as f.
    - Evaluate f.write(ISLAND\_ENTRY.replace(“\_\_VUE\_FILE\_\_”, (os.path.basename(path) + “.vue”))).
- If not os.path.exists((path + “.vue”)).
  - Within open((path + “.vue”), “w”) bound as f.
    - Evaluate f.write(ISLAND\_COMPONENT.replace(“\_\_TITLE\_\_”, as\_js\_string(title))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L2794) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1744)

<a id="op-a3fa17c3845eb5"></a>
### Page.as dict

`operation_foundation_core_record_definitions_page_business_behavior_page_as_mapping`

**Inputs** self, remaining named values kwargs.

**Explicit results** d.

**Local steps**

- Set d from super().as\_dict(expanded names kwargs).
- For each key in tuple(“script”, “style”, “content”).
  - Set d at key from self.get(key).
- If self.get(“\_island”).
  - Set d at “island” from self.\_island.
- Return d.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L83) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1731)

<a id="op-d98964fe8a7a0a"></a>
### Page.get island name

`operation_foundation_core_record_definitions_page_business_behavior_page_get_island_name`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** self.island · page\_island\_name(app, self.name) when app, otherwise no value.

**Local steps**

- Bind dependencies page\_island\_name.
- If self.island.
  - Return self.island.
- Set app from Platform.local.module\_app.get(Platform.scrub(self.module)).
- Return page\_island\_name(app, self.name) when app, otherwise no value.
  - Value choice on app — true gives page\_island\_name(app, self.name), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L84) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1736)

<a id="op-5456fdd88e2348"></a>
### Page.clear cache

`operation_foundation_core_record_definitions_page_business_behavior_page_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Bind dependencies clear\_computed\_base\_for.
- Evaluate clear\_computed\_base\_for(self).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L3525) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1733)

<a id="op-72c9f9657be997"></a>
### Page.on trash

`operation_foundation_core_record_definitions_page_business_behavior_page_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Deletion of this document is only permitted in developer mode.”.

**Local steps**

- If (not Platform.conf.developer\_mode and not Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.flags.in\_migrate.
  - Call the validation error handler Platform.throw(translated “Deletion of this document is only permitted in developer mode.”).
- Evaluate delete\_custom\_role(“page”, self.name).
- If Platform.conf.developer\_mode.
  - Evaluate Platform.db.after\_commit(self.delete\_folder\_with\_contents).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L3610) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1740)

<a id="op-18421a0c6e9562"></a>
### Page.delete folder with contents

`operation_foundation_core_record_definitions_page_business_behavior_page_delete_folder_with_contents`

**Inputs** self.

**Local steps**

- Attempt the following.
  - Set module\_path from get\_module\_path(self.module).
  - Set dir\_path from os.path.join(module\_path, “page”, Platform.scrub(self.name)).
  - If os.path.exists(dir\_path).
    - Evaluate shutil.rmtree(dir\_path, ignore\_errors = true).
- On failure (Platform.DoesNotExistError) bound to e.
  - Evaluate Platform.log(e).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L3810) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1734)

<a id="op-2d9327e29b96bd"></a>
### Page.is permitted

`operation_foundation_core_record_definitions_page_business_behavior_page_is_permitted`

**Inputs** self.

**Record and data access** read “Has Role” via get\_all.

**Explicit results** true.

**Local steps**

- Bind dependencies has\_common.
- Set allowed from list of d.role for d drawn from Platform.get\_all(“Has Role”, fields = list(“role”), filters = mapping(“parent” → self.name)).
  - Draw d from Platform.get\_all(“Has Role”, fields = list(“role”), filters = mapping(“parent” → self.name)).
- Set custom\_roles from get\_custom\_allowed\_roles(“page”, self.name).
- Evaluate allowed.extend(custom\_roles).
- If not allowed.
  - Return true.
- Set roles from Platform.get\_roles().
- If has\_common(roles, allowed).
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L4053) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1738)

<a id="op-56566035948011"></a>
### Page.load assets

`operation_foundation_core_record_definitions_page_business_behavior_page_load_assets`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies os.
- Bind dependencies html\_to\_js\_template.
- Bind dependencies get\_module\_path, scrub.
- Set self.script from empty text.
- If self.type equals “Platform UI”.
  - Set self.\_island from self.get\_island\_name().
  - Return no value.
- Set page\_name from scrub(self.name).
- Set path from os.path.join(get\_module\_path(self.module), “page”, page\_name).
- Set fpath from os.path.join(path, (page\_name + “.js”)).
- If os.path.exists(fpath).
  - Within open(fpath) bound as f.
    - Set self.script from render\_include(f.read()).
    - Update self.script using + formatted text   //# sourceURL={page\_name}.js.
- Set fpath from os.path.join(path, (page\_name + “.css”)).
- If os.path.exists(fpath).
  - Within open(fpath) bound as f.
    - Set self.style from safe\_decode(f.read()).
- For each fname in os.listdir(path).
  - If fname.endswith(“.html”).
    - Within open(os.path.join(path, fname)) bound as f.
      - Set template from f.read().
      - If “&lt;!-- jinja --&gt;” belongs to template.
        - Set context from Platform.\_dict(mapping()).
        - Attempt the following.
          - Set out from Platform.get\_attr(“{app}.{module}.page.{page}.{page}.get\_context”.format(app = Platform.local.module\_app at scrub(self.module), module = scrub(self.module), page = page\_name))(context).
          - If out.
            - Set context from out.
        - On failure (tuple(AttributeError, ImportError)).
          - Take no action here.
        - Set template from Platform.render\_template(template, context).
      - Set self.script from (html\_to\_js\_template(fname, template) + self.script).
      - Set self.\_dynamic\_page from true.
- For each path in get\_code\_files\_via\_hooks(“page\_js”, self.name).
  - Set js from get\_js(path).
  - If js.
    - Update self.script using + (whitespace '\\n\\n' + js).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get island name](operations-069.md#op-d98964fe8a7a0a).

**Values supplied outside this operation** selected callable from Platform.get\_attr(“{app}.{module}.page.{page}.{page}.get\_context”.format(app = Platform.local.module\_app at scrub(self.module), module = scrub(self.module), page = page\_name)).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L85) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1801) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1739)

<a id="op-0b9e19ebddac14"></a>
### Delete custom role

`operation_foundation_core_record_definitions_page_business_behavior_delete_custom_role`

**Inputs** field, docname.

**Record and data access** read “Custom Role” via get\_value.

**State and service calls** request delete\_doc for “Custom Role”.

**Local steps**

- Set name from Platform.db.get\_value(“Custom Role”, mapping(field → docname), “name”).
- If name.
  - Evaluate Platform.delete\_doc(“Custom Role”, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L5473) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1730)

<a id="op-7c6a8a2867883c"></a>
### As js string

`operation_foundation_core_record_definitions_page_business_behavior_as_client_script_string`

**Inputs** value.

**Declared result** str.

**Explicit results** json.dumps(value).replace(“&lt;”, “\\u003c”).

**Local steps**

- Return json.dumps(value).replace(“&lt;”, “\\u003c”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0091.json#L5619) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1729)

## Record · Patch log

[Record definition](../../../../data/record-types/patch_log.json)

<a id="op-0ef70c394d6804"></a>
### Before migrate

`operation_foundation_core_record_definitions_patch_log_business_behavior_before_migrate`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.reload\_doc(“core”, “doctype”, “patch\_log”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L1491) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L9)

## Record · Permission inspector

[Record definition](../../../../data/record-types/permission_inspector.json)

<a id="op-4914c82b94016f"></a>
### Permission Inspector.onload

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_onload`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L1552) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L18)

<a id="op-cfea0eaec5a343"></a>
### Permission Inspector.debug

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_debug`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L1627) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L12)

<a id="op-7537e3dadddf75"></a>
### Permission Inspector.load from db

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_load_from_database`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L89) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L17)

<a id="op-ca460ef48915ac"></a>
### Permission Inspector.db insert

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_database_insert`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, args, kwargs.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L1988) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L10)

<a id="op-4f4452b3187fc1"></a>
### Permission Inspector.db update

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_database_update`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L2034) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L11)

<a id="op-9998c2d0713ca7"></a>
### Permission Inspector.get list

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_get_list`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L2070) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L15)

<a id="op-21f53e37efa725"></a>
### Permission Inspector.get count

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_get_count`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L2103) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L14)

<a id="op-9eefd2365c1a76"></a>
### Permission Inspector.get stats

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_get_stats`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L2136) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L16)

<a id="op-36a1ef815f2ae4"></a>
### Permission Inspector.delete

`operation_foundation_core_record_definitions_permission_inspector_business_behavior_permission_inspector_delete`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L2169) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L13)

## Record · Permission log

[Record definition](../../../../data/record-types/permission_log.json)

<a id="op-7732927b0c490e"></a>
### Permission Log.changed at

`operation_foundation_core_record_definitions_permission_log_business_behavior_permission_log_changed_at`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0092.json#L2205) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L25)
