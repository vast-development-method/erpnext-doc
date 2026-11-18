# Site operations and diagnostics · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-593be544a86607"></a>
### Setup chrome

`operation_foundation_commands_utils_business_behavior_setup_chrome`

**Inputs** no declared parameters.

**Wrappers, in declaration order** click.command(“setup-chrome”).

**Local steps**

- Bind dependencies setup\_chromium.
- Evaluate setup\_chromium().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L149) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L762)

<a id="op-9caf400f7bbc2c"></a>
### Export module json

`operation_foundation_modules_utils_business_behavior_export_module_structured_data`

**Inputs** doc, is\_standard, module.

**Declared result** (str bitwise or no value).

**Explicit results** os.path.join(Platform.get\_module\_path(module), scrub(doc.doctype), scrub(doc.name), scrub(doc.name)).

**Local steps**

- If (not Platform.flags.in\_import and is\_standard and Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.in\_import → is\_standard → Platform.conf.developer\_mode.
  - Bind dependencies export\_to\_files.
  - Evaluate export\_to\_files(record\_list = list(list(doc.doctype, doc.name)), record\_module = module, create\_init = is\_standard).
  - Return os.path.join(Platform.get\_module\_path(module), scrub(doc.doctype), scrub(doc.name), scrub(doc.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L28) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1408)

<a id="op-f9b406e587adcb"></a>
### Get doc module

`operation_foundation_modules_utils_business_behavior_get_record_module`

**Inputs** module, doctype, name.

**Declared result** “ModuleType”.

**Explicit results** Platform.get\_module(module\_name).

**Local steps**

- Set module\_name from “{app}.{module}.{doctype}.{name}.{name}”.format(app = Platform.local.module\_app at scrub(module), doctype = scrub(doctype), module = scrub(module), name = scrub(name)).
- Return Platform.get\_module(module\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L30) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1415)

<a id="op-1d9842fb3b7c0c"></a>
### Export customizations

`operation_foundation_modules_utils_business_behavior_export_customizations`

**Inputs** module, doctype, sync\_on\_migrate = false, with\_permissions = false, apply\_module\_export\_filter = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Custom Field” via get\_all · read “Property Setter” via get\_all · read “DocType Link” via get\_all · read “Custom DocPerm” via get\_all.

**State and service calls** msgprint with translated “Customizations for &lt;b&gt;{0}&lt;/b&gt; exported to:&lt;br&gt;{1}”.format(doctype, path).

**Explicit results** path.

**Explicit failure paths** validation helper — translated “Only allowed to export customizations in developer mode”.

**Local steps**

- Set sync\_on\_migrate from cint(sync\_on\_migrate).
- Set with\_permissions from cint(with\_permissions).
- Set apply\_module\_export\_filter from cint(apply\_module\_export\_filter).
- Set cf\_filters from mapping(“dt” → doctype).
- Set ps\_filters from mapping(“doc\_type” → doctype).
- If apply\_module\_export\_filter.
  - Set cf\_filters at “module” from module.
  - Set ps\_filters at “module” from module.
- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Only allowed to export customizations in developer mode”).
- Set custom from mapping(“custom\_fields” → Platform.get\_all(“Custom Field”, fields = “\*”, filters = cf\_filters, order\_by = “name”), “property\_setters” → Platform.get\_all(“Property Setter”, fields = “\*”, filters = ps\_filter ….
- If with\_permissions.
  - Set custom at “custom\_perms” from Platform.get\_all(“Custom DocPerm”, fields = “\*”, filters = mapping(“parent” → doctype), order\_by = “name”).
- For each d in Platform.get\_meta(doctype).get\_table\_fields().
  - Evaluate export\_customizations(module, d.options, sync\_on\_migrate, with\_permissions, …).
- If (custom at “custom\_fields” or custom at “property\_setters” or custom at “custom\_perms”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in custom at “custom\_fields” → custom at “property\_setters” → custom at “custom\_perms”.
  - Set folder\_path from os.path.join(get\_module\_path(module), “custom”).
  - If not os.path.exists(folder\_path).
    - Evaluate os.makedirs(folder\_path).
  - Set path from os.path.join(folder\_path, (scrub(doctype) + “.json”)).
  - Within open(path, “w”) bound as f.
    - Evaluate f.write(Platform.as\_json(custom)).
  - Evaluate Platform.msgprint(translated “Customizations for &lt;b&gt;{0}&lt;/b&gt; exported to:&lt;br&gt;{1}”.format(doctype, path)).
  - Return path.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L5635) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1407)

<a id="op-7262802ae4280a"></a>
### Sync customizations

`operation_foundation_modules_utils_business_behavior_sync_customizations`

**Inputs** app = no value.

**Local steps**

- If app.
  - Set apps from list(app).
- Otherwise.
  - Set apps from Platform.get\_installed\_apps().
- For each app\_name in apps.
  - For each module\_name in (Platform.local.app\_modules.get(app\_name) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.app\_modules.get(app\_name) → list().
    - Set folder from Platform.get\_app\_path(app\_name, module\_name, “custom”).
    - If os.path.exists(folder).
      - For each fname in os.listdir(folder).
        - If fname.endswith(“.json”).
          - Within open(os.path.join(folder, fname)) bound as f.
            - Set data from json.loads(f.read()).
          - If data.get(“sync\_on\_migrate”).
            - Evaluate sync\_customizations\_for\_doctype(data, folder, fname).
          - Otherwise.
            - If (Platform.flags.in\_install and app).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_install → app.
              - Evaluate sync\_customizations\_for\_doctype(data, folder, fname).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L33) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1423)

<a id="op-5f7f209ad12b8c"></a>
### Sync customizations for doctype

`operation_foundation_modules_utils_business_behavior_sync_customizations_for_record_type`

**Inputs** data, folder, filename = empty text.

**Record and data access** read “DocType” via exists · read “DocType” via get\_value.

**Explicit results** no value.

**Local steps**

- Bind dependencies validate\_fields\_for\_doctype.
- Set doctype from data at “doctype”.
- Set update\_schema from false.
- Bind local operation sync for subsequent calls.
- If not Platform.db.exists(“DocType”, doctype).
  - Evaluate print(translated “DocType {0} does not exist.”.format(doctype)).
  - Evaluate print(translated “Skipping fixture syncing for doctype {0} from file {1}”.format(doctype, filename)).
  - Return no value.
- If data at “custom\_fields”.
  - Evaluate sync(“custom\_fields”, “Custom Field”, “dt”).
  - Set update\_schema from true.
- If data.get(“links”, false).
  - Evaluate sync(“links”, “DocType Link”, “parent”).
- If data at “property\_setters”.
  - Evaluate sync(“property\_setters”, “Property Setter”, “doc\_type”).
- Evaluate print(formatted text Updating customizations for {doctype}).
- If data.get(“custom\_perms”).
  - Evaluate sync(“custom\_perms”, “Custom DocPerm”, “parent”).
- Evaluate validate\_fields\_for\_doctype(doctype).
- If (update\_schema and not Platform.db.get\_value(“DocType”, doctype, “issingle”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_schema → not Platform.db.get\_value(“DocType”, doctype, “issingle”).
  - Evaluate Platform.db.updatedb(doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1424)

<a id="op-8ccfeaf44a21b8"></a>
### Sync customizations for doctype.sync

`operation_foundation_modules_utils_business_behavior_sync_customizations_for_record_type_sync`

**Inputs** key, custom\_doctype, doctype\_fieldname.

**Local steps**

- Set doctypes from list(set(map(deferred anonymous expression, data at key))).
- Bind local operation sync\_single\_doctype for subsequent calls.
- For each doc\_type in doctypes.
  - If (doc\_type equals doctype or not os.path.exists(os.path.join(folder, (scrub(doc\_type) + “.json”)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc\_type equals doctype → not os.path.exists(os.path.join(folder, (scrub(doc\_type) + “.json”))).
    - Evaluate sync\_single\_doctype(doc\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L1999) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1425)

<a id="op-07f90f989a0539"></a>
### Sync customizations for doctype.sync.sync single doctype

`operation_foundation_modules_utils_business_behavior_sync_customizations_for_record_type_sync_sync_single_record_type`

**Inputs** doc\_type.

**Record and data access** read “Custom Field” via get\_value · resolve a document from “Custom Field” via get\_doc · read “DocType Link” via get\_value · resolve a document from “DocType Link” via get\_doc · resolve a document from d via get\_doc.

**State and service calls** call db\_update on custom\_field · call db\_update on doc\_link · call insert on doc · request delete on “Custom DocPerm”.

**Local steps**

- Bind local operation \_insert for subsequent calls.
- Select the first matching pattern against custom\_doctype.
  - Pattern “Custom Field”.
    - For each d in data at key.
      - Set field from Platform.db.get\_value(“Custom Field”, mapping(“dt” → doc\_type, “fieldname” → d at “fieldname”)).
      - If not field.
        - Set d at “owner” from “Administrator”.
        - Evaluate \_insert(d).
      - Otherwise.
        - Set custom\_field from Platform.get\_doc(“Custom Field”, field).
        - Set custom\_field.flags.ignore\_validate from true.
        - Evaluate custom\_field.update(d).
        - Evaluate custom\_field.db\_update().
  - Pattern “DocType Link”.
    - For each d in data at key.
      - Set link from Platform.db.get\_value(“DocType Link”, mapping(“parent” → doc\_type, “link\_doctype” → d.get(“link\_doctype”), “link\_fieldname” → d.get(“link\_fieldname”))).
      - If not link.
        - Set d at “owner” from “Administrator”.
        - Evaluate \_insert(d).
      - Otherwise.
        - Set doc\_link from Platform.get\_doc(“DocType Link”, link).
        - Set doc\_link.flags.ignore\_validate from true.
        - Evaluate doc\_link.update(d).
        - Evaluate doc\_link.db\_update().
  - Pattern “Property Setter”.
    - For each d in data at key.
      - If d.get(“doc\_type”) equals doc\_type.
        - Set d at “doctype” from “Property Setter”.
        - Set doc from Platform.get\_doc(d).
        - Set doc.flags.validate\_fields\_for\_doctype from false.
        - Evaluate doc.insert().
  - Pattern “Custom DocPerm”.
    - Evaluate Platform.db.delete(“Custom DocPerm”, mapping(“parent” → doc\_type)).
    - For each d in data at key.
      - Evaluate \_insert(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L3341) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1426)

<a id="op-ff9f182b2debd5"></a>
### Sync customizations for doctype.sync.sync single doctype.insert

`operation_foundation_modules_utils_business_behavior_sync_customizations_for_record_type_sync_sync_single_record_type_insert`

**Inputs** data.

**Record and data access** resolve a document from data via get\_doc.

**State and service calls** call db\_insert on doc.

**Local steps**

- If data.get(doctype\_fieldname) equals doc\_type.
  - Set data at “doctype” from custom\_doctype.
  - Set doc from Platform.get\_doc(data).
  - Evaluate doc.db\_insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L4426) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1427)

<a id="op-7d2ef44a89fd6a"></a>
### Scrub dt dn

`operation_foundation_modules_utils_business_behavior_scrub_record_type_record_name`

**Inputs** dt, dn.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(scrub(dt), scrub(dn)).

**Local steps**

- Return tuple(scrub(dt), scrub(dn)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L4567) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1422)

<a id="op-47daac24bad3a4"></a>
### Get doc path

`operation_foundation_modules_utils_business_behavior_get_record_path`

**Inputs** module, doctype, name.

**Declared result** str.

**Explicit results** path.resolve().

**Explicit failure paths** ValueError(translated “Path {0} is not within module {1}”.format(path, module)).

**Local steps**

- Set module\_path from Path(get\_module\_path(module)).
- Set path from (module\_path ÷ Path(expanded scrub\_dt\_dn(doctype, name))).
- If not path.resolve().is\_relative\_to(module\_path.resolve()).
  - Raise ValueError(translated “Path {0} is not within module {1}”.format(path, module)).
- Return path.resolve().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L4675) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1416)

<a id="op-207e807a10e08a"></a>
### Reload doc

`operation_foundation_modules_utils_business_behavior_reload_record`

**Inputs** module, dt = no value, dn = no value, force = false, reset\_permissions = false.

**Explicit results** import\_files(module, dt, dn, force = force, reset\_permissions = reset\_permissions).

**Local steps**

- Bind dependencies import\_files.
- Return import\_files(module, dt, dn, force = force, reset\_permissions = reset\_permissions).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L4957) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1421)

<a id="op-01e2048bf9a916"></a>
### Export doc

`operation_foundation_modules_utils_business_behavior_export_record`

**Inputs** doctype, name, module = no value.

**Record and data access** read “DocType” via get\_value · resolve a document from doctype via get\_doc.

**Local steps**

- Bind dependencies write\_document\_file.
- Evaluate print(formatted text Exporting Document {doctype} {name}).
- Set module from (module or Platform.db.get\_value(“DocType”, name, “module”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in module → Platform.db.get\_value(“DocType”, name, “module”).
- Evaluate write\_document\_file(Platform.get\_doc(doctype, name), module).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L5127) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1409)

<a id="op-43925c3e336646"></a>
### Get doctype module

`operation_foundation_modules_utils_business_behavior_get_record_type_module`

**Inputs** doctype.

**Declared result** str.

**Explicit results** module\_name.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “DocType {} not found”.format(doctype).

**Local steps**

- Set doctype\_module\_map from Platform.cache.get\_value(“doctype\_modules”, generator = deferred anonymous expression).
- If module\_name bound to doctype\_module\_map.get(doctype).
  - Return module\_name.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “DocType {} not found”.format(doctype), exc = Platform.DoesNotExistError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L5339) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1418)

<a id="op-4b3ac892fb212c"></a>
### Load doctype module

`operation_foundation_modules_utils_business_behavior_load_record_type_module`

**Inputs** doctype, module = no value, prefix = empty text, suffix = empty text.

**Explicit results** doctype\_python\_modules at key.

**Explicit failure paths** ImportError(msg).

**Local steps**

- Set module from (module or get\_doctype\_module(doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in module → get\_doctype\_module(doctype).
- Set app from get\_module\_app(module).
- Set key from tuple(app, doctype, prefix, suffix).
- Set module\_name from get\_module\_name(doctype, module, prefix, suffix, …).
- If key does not belong to doctype\_python\_modules.
  - Attempt the following.
    - Set doctype\_python\_modules at key from Platform.get\_module(module\_name).
  - On failure (ImportError) bound to e.
    - Set msg from formatted text Module import failed for {doctype}, the DocType you're trying to open might be deleted..
    - Update msg using + formatted text  Error: {e}.
    - Raise ImportError(msg) with cause e.
- Return doctype\_python\_modules at key.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L31) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1419)

<a id="op-1da5168e3dab5d"></a>
### Get module name

`operation_foundation_modules_utils_business_behavior_get_module_name`

**Inputs** doctype, module, prefix = empty text, suffix = empty text, app = no value.

**Explicit results** formatted text {app}.{module}.doctype.{doctype}.{prefix}{doctype}{suffix}.

**Local steps**

- Set app from scrub((app or get\_module\_app(module))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app → get\_module\_app(module).
- Set module from scrub(module).
- Set doctype from scrub(doctype).
- Return formatted text {app}.{module}.doctype.{doctype}.{prefix}{doctype}{suffix}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L5991) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1414)

<a id="op-ac9dfb06188ba8"></a>
### Get module app

`operation_foundation_modules_utils_business_behavior_get_module_application`

**Inputs** module.

**Declared result** str.

**Explicit results** app.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Module {} not found”.format(module).

**Local steps**

- Set app from Platform.local.module\_app.get(scrub(module)).
- If app is identical to no value.
  - Call the validation error handler Platform.throw(translated “Module {} not found”.format(module), exc = Platform.DoesNotExistError).
- Return app.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L6283) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1413)

<a id="op-36b2f65237f747"></a>
### Get doctype app map

`operation_foundation_modules_utils_business_behavior_get_record_type_application_map`

**Inputs** no declared parameters.

**Wrappers, in declaration order** site\_cache.

**Explicit results** dict(nested operand in the contract.on(nested operand in the contract equals nested operand in the contract).select(DocType.name, Module.app\_name).run()).

**Local steps**

- Set DocType from Platform.qb.DocType(“DocType”).
- Set Module from Platform.qb.DocType(“Module Def”).
- Return dict(nested operand in the contract.on(nested operand in the contract equals nested operand in the contract).select(DocType.name, Module.app\_name).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0296.json#L6471) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1417)

<a id="op-303bf337e58b92"></a>
### Get app publisher

`operation_foundation_modules_utils_business_behavior_get_application_publisher`

**Inputs** module.

**Declared result** str.

**Explicit results** Platform.get\_hooks(hook = “app\_publisher”, app\_name = app) at 0.

**Explicit failure paths** validation helper — translated “App not found for module: {0}”.format(module).

**Local steps**

- Set app from get\_module\_app(module).
- If not app.
  - Call the validation error handler Platform.throw(translated “App not found for module: {0}”.format(module)).
- Return Platform.get\_hooks(hook = “app\_publisher”, app\_name = app) at 0.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(hook = “app\_publisher”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1412)

<a id="op-cf186f0fcaed34"></a>
### Make boilerplate

`operation_foundation_modules_utils_business_behavior_make_boilerplate`

**Inputs** template, doc, opts = no value.

**Explicit results** no value.

**Local steps**

- Set target\_path from get\_doc\_path(doc.module, doc.doctype, doc.name).
- Set template\_name from template.replace(“controller”, scrub(doc.name)).
- If template\_name.endswith(“.\_py”).
  - Set template\_name from (template\_name at slice no value to negative 4 + “.py”).
- Set target\_file\_path from os.path.join(target\_path, template\_name).
- Set template\_file\_path from os.path.join(get\_module\_path(“core”), “doctype”, scrub(doc.doctype), “boilerplate”, …).
- If os.path.exists(target\_file\_path).
  - Evaluate print(formatted text {target\_file\_path} already exists, skipping...).
  - Return no value.
- Set doc from (doc or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → Platform.\_dict().
- Set opts from (opts or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in opts → Platform.\_dict().
- Set app\_publisher from get\_app\_publisher(doc.module).
- Set base\_class from “Document”.
- Set base\_class\_import from “from Platform.model.document import Document”.
- Set controller\_body from “pass”.
- If doc.get(“is\_tree”).
  - Set base\_class from “NestedSet”.
  - Set base\_class\_import from “from Platform.utils.nestedset import NestedSet”.
- If doc.get(“is\_virtual”).
  - Set controller\_body from multiline text in the contract.
  - If not doc.get(“istable”).
    - Update controller\_body using + multiline text in the contract.
  - Set controller\_body from indent(dedent(controller\_body), whitespace '\\t').
- Within open(target\_file\_path, “w”) bound as target, open(template\_file\_path) bound as source.
  - Set template from source.read().
  - Set controller\_file\_content from cstr(template).format(app\_publisher = app\_publisher, year = now\_datetime().year, classname = doc.name.replace(one space, empty text).replace(“-”, empty text), base\_class\_import = base\_class\_import, …).
  - Evaluate target.write(Platform.as\_unicode(controller\_file\_content)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L32) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1420)

<a id="op-bdc8af00696495"></a>
### Create directory on app path

`operation_foundation_modules_utils_business_behavior_create_directory_on_application_path`

**Inputs** folder\_name, app\_name.

**Explicit results** folder\_path.

**Local steps**

- Set app\_path from Platform.get\_app\_path(app\_name).
- Set folder\_path from os.path.join(app\_path, folder\_name).
- If not os.path.exists(folder\_path).
  - Evaluate Platform.create\_folder(folder\_path).
- Return folder\_path.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L27) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1405)

<a id="op-afd64a71572455"></a>
### Get app level directory path

`operation_foundation_modules_utils_business_behavior_get_application_level_directory_path`

**Inputs** folder\_name, app\_name.

**Explicit results** path.

**Local steps**

- Set app\_path from Platform.get\_app\_path(app\_name).
- Set path from os.path.join(app\_path, folder\_name).
- Return path.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L29) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1410)

<a id="op-fc7b9109d14ba7"></a>
### Get app level files

`operation_foundation_modules_utils_business_behavior_get_application_level_files`

**Inputs** folder\_name, app\_name.

**Explicit results** list() · list of os.path.join(path, filename) for filename drawn from os.listdir(path).

**Local steps**

- Set path from get\_app\_level\_directory\_path(folder\_name, app\_name).
- If not os.path.exists(path).
  - Return list().
- Return list of os.path.join(path, filename) for filename drawn from os.listdir(path).
  - Draw filename from os.listdir(path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L1894) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1411)

<a id="op-9253f857d28fd4"></a>
### Delete app level folder

`operation_foundation_modules_utils_business_behavior_delete_application_level_folder`

**Inputs** folder\_name, app\_name.

**Local steps**

- Set path from get\_app\_level\_directory\_path(folder\_name, app\_name).
- Evaluate shutil.rmtree(path, ignore\_errors = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L2070) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1406)
