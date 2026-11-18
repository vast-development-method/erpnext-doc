# Record lifecycle and persistence · operations 73

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Platform

<a id="op-b894eb6a219bb8"></a>
### Unscrub

`operation_foundation_binding_foundation_init_unscrub`

**Inputs** txt.

**Declared result** str.

**Explicit results** txt.replace(“\_”, one space).replace(“-”, one space).title().

**Local steps**

- Return txt.replace(“\_”, one space).replace(“-”, one space).title().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1474)

<a id="op-154f9d842d2d1b"></a>
### Get module path

`operation_foundation_binding_foundation_init_get_module_path`

**Inputs** module, remaining positional values joins.

**Explicit results** get\_pymodule\_path(((app + “.”) + scrub(module)), expanded joins).

**Local steps**

- Bind dependencies get\_module\_app.
- Set app from get\_module\_app(module).
- Return get\_pymodule\_path(((app + “.”) + scrub(module)), expanded joins).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L35) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1467)

<a id="op-698877d2be4ed2"></a>
### Get app path

`operation_foundation_binding_foundation_init_get_app_path`

**Inputs** app\_name, remaining positional values joins.

**Explicit results** get\_pymodule\_path(app\_name, expanded joins).

**Local steps**

- Return get\_pymodule\_path(app\_name, expanded joins).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1459)

<a id="op-703adad0d68a33"></a>
### Get app source path

`operation_foundation_binding_foundation_init_get_app_source_path`

**Inputs** app\_name, remaining positional values joins.

**Explicit results** get\_app\_path(app\_name, “..”, expanded joins).

**Local steps**

- Return get\_app\_path(app\_name, “..”, expanded joins).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1460)

<a id="op-88df459a1e8b8f"></a>
### Get site path

`operation_foundation_binding_foundation_init_get_site_path`

**Inputs** remaining positional values joins.

**Explicit results** join(local.site\_path, expanded joins).

**Local steps**

- Bind dependencies join.
- Return join(local.site\_path, expanded joins).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L37) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1469)

<a id="op-41d24222085aa1"></a>
### Get pymodule path

`operation_foundation_binding_foundation_init_get_pymodule_path`

**Inputs** modulename, remaining positional values joins.

**Explicit results** abspath(join(dirname((get\_module(nested operand in the contract(nested operand in the contract)).\_\_file\_\_ or empty text)), expanded joins)).

**Local steps**

- Bind dependencies abspath, dirname, join.
- If “public” does not belong to joins.
  - Set joins from list of scrub(part) for part drawn from joins.
    - Draw part from joins.
- Return abspath(join(dirname((get\_module(nested operand in the contract(nested operand in the contract)).\_\_file\_\_ or empty text)), expanded joins)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_module(scrub(modulename)).\_\_file\_\_ → empty text.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L36) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1468)

<a id="op-6394ccbae8bf9f"></a>
### Get module list

`operation_foundation_binding_foundation_init_get_module_list`

**Inputs** app\_name.

**Explicit results** get\_file\_items(get\_app\_path(app\_name, “modules.txt”)).

**Local steps**

- Return get\_file\_items(get\_app\_path(app\_name, “modules.txt”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1466)

<a id="op-57bb7bb488fb31"></a>
### Get all apps

`operation_foundation_binding_foundation_init_get_all_apps`

**Inputs** with\_internal\_apps = true, sites\_path = no value.

**State and service calls** call insert on apps.

**Explicit results** apps.

**Local steps**

- If not sites\_path.
  - Set sites\_path from local.sites\_path.
- Set apps from get\_file\_items(os.path.join(sites\_path, “apps.txt”), raise\_not\_found = true).
- If with\_internal\_apps.
  - For each app in get\_file\_items(os.path.join(local.site\_path, “apps.txt”)).
    - If app does not belong to apps.
      - Evaluate apps.append(app).
- If “Platform” belongs to apps.
  - Evaluate apps.remove(“Platform”).
- Evaluate apps.insert(0, “Platform”).
- Return apps.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1458)

<a id="op-4ae8e1eae34a6b"></a>
### Get installed apps

`operation_foundation_binding_foundation_init_get_installed_apps`

**Inputs** \_ensure\_on\_bench (named only, default false).

**Wrappers, in declaration order** request\_cache.

**Declared result** list at str.

**Explicit results** list() · installed.

**Local steps**

- If getattr(flags, “in\_install\_db”, true).
  - Return list().
- If not db.
  - Evaluate connect().
- Set installed from orjson.loads((db.get\_global(“installed\_apps”) or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in db.get\_global(“installed\_apps”) → “&#91;&#93;”.
- If \_ensure\_on\_bench.
  - Set all\_apps from cache.get\_value(“all\_apps”, get\_all\_apps).
  - Set installed from list of app for app drawn from installed where app belongs to all\_apps.
    - Draw app from installed, keep a combination only if (app belongs to all\_apps).
- Return installed.

**Values supplied outside this operation** selected callable from getattr(flags, “in\_install\_db”, true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1464)

<a id="op-cd747d6c8143ad"></a>
### Get doc hooks

`operation_foundation_initialize_business_behavior_get_record_hooks`

**Inputs** no declared parameters.

**Explicit results** local.doc\_events\_hooks.

**Local steps**

- If not getattr(local, “doc\_events\_hooks”, no value).
  - Set hooks from get\_hooks(“doc\_events”, mapping()).
  - Set out from mapping().
  - For each tuple(key, value) in hooks.items().
    - If isinstance(key, tuple).
      - For each doctype in key.
        - Evaluate append\_hook(out, doctype, value).
    - Otherwise.
      - Evaluate append\_hook(out, key, value).
  - Set local.doc\_events\_hooks from out.
- Return local.doc\_events\_hooks.

**Values supplied outside this operation** selected callable from getattr(local, “doc\_events\_hooks”, no value), get\_hooks(“doc\_events”, mapping()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L3802) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L459)

<a id="op-ef154d4e431c9a"></a>
### Load app hooks

`operation_foundation_initialize_business_behavior_load_application_hooks`

**Inputs** app\_name = no value.

**Explicit results** hooks.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies types.
- Set hooks from mapping().
- Set apps from list(app\_name) when app\_name, otherwise get\_installed\_apps(\_ensure\_on\_bench = true).
  - Value choice on app\_name — true gives list(app\_name), false gives get\_installed\_apps(\_ensure\_on\_bench = true).
- For each app in apps.
  - Attempt the following.
    - Set app\_hooks from get\_module(formatted text {app}.hooks).
  - On failure (ImportError) bound to e.
    - Evaluate print(formatted text Could not find app "{app}":  {e}).
    - Propagate the active failure.
  - Bind local operation \_is\_valid\_hook for subsequent calls.
  - For each tuple(key, value) in inspect.getmembers(app\_hooks, predicate = \_is\_valid\_hook).
    - If not key.startswith(“\_”).
      - Evaluate append\_hook(hooks, key, value).
- Return hooks.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L25) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L478)

<a id="op-e3268db57b450f"></a>
### Load app hooks.is valid hook

`operation_foundation_initialize_business_behavior_load_application_hooks_is_valid_hook`

**Inputs** obj.

**Explicit results** not isinstance(obj, ((types.ModuleType bitwise or types.FunctionType) bitwise or type)).

**Local steps**

- Return not isinstance(obj, ((types.ModuleType bitwise or types.FunctionType) bitwise or type)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L3827) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L479)

<a id="op-9f18304267fadb"></a>
### Get hooks

`operation_foundation_initialize_business_behavior_get_hooks`

**Inputs** hook = no value, default = “\_KEEP\_DEFAULT\_LIST”, app\_name = no value.

**Declared result** \_dict.

**Explicit results** hooks.get(hook, list() when default equals “\_KEEP\_DEFAULT\_LIST”, otherwise default) · \_dict(hooks).

**Local steps**

- If app\_name.
  - Set hooks from \_request\_cached\_load\_app\_hooks(app\_name).
- Otherwise.
  - If local.conf.developer\_mode.
    - Set hooks from \_site\_cached\_load\_app\_hooks().
  - Otherwise.
    - Set hooks from client\_cache.get\_value(“app\_hooks”).
    - If hooks is identical to no value.
      - Set hooks from \_load\_app\_hooks().
      - Evaluate client\_cache.set\_value(“app\_hooks”, hooks).
- If hook.
  - Return hooks.get(hook, list() when default equals “\_KEEP\_DEFAULT\_LIST”, otherwise default).
    - Value choice on default equals “\_KEEP\_DEFAULT\_LIST” — true gives list(), false gives default.
- Return \_dict(hooks).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L4544) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L454)

<a id="op-8079ced5e1f175"></a>
### Append hook

`operation_foundation_initialize_business_behavior_append_hook`

**Inputs** target, key, value.

**Local steps**

- If isinstance(value, dict).
  - Evaluate target.setdefault(key, mapping()).
  - For each inkey in value.
    - Evaluate append\_hook(target at key, inkey, value at inkey).
- Otherwise.
  - Evaluate target.setdefault(key, list()).
  - If not isinstance(value, list).
    - Set value from list(value).
  - Evaluate target at key.extend(value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L4894) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L438)

<a id="op-dcc187bb6789fe"></a>
### Setup module map

`operation_foundation_initialize_business_behavior_setup_module_map`

**Inputs** include\_all\_apps = true.

**Declared result** no value.

**Local steps**

- If include\_all\_apps.
  - Set app\_modules from cache.get\_value(“app\_modules”).
- Otherwise.
  - Set app\_modules from client\_cache.get\_value(“installed\_app\_modules”).
- If not app\_modules.
  - Set app\_modules from mapping().
  - If include\_all\_apps.
    - Set apps from get\_all\_apps(with\_internal\_apps = true).
  - Otherwise.
    - Set apps from get\_installed\_apps(\_ensure\_on\_bench = true).
  - For each app in apps.
    - Evaluate app\_modules.setdefault(app, list()).
    - For each module in get\_module\_list(app).
      - Set module from scrub(module).
      - Evaluate app\_modules at app.append(module).
  - If include\_all\_apps.
    - Evaluate cache.set\_value(“app\_modules”, app\_modules).
  - Otherwise.
    - Evaluate client\_cache.set\_value(“installed\_app\_modules”, app\_modules).
- Set module\_app from mapping().
- For each tuple(app, modules) in app\_modules.items().
  - For each module in modules.
    - If module belongs to module\_app.
      - Evaluate warnings.warn(formatted text WARNING: module ′{module}′ found in apps ′{module\_app at module}′ and ′{app}′, stacklevel = 1).
    - Set module\_app at module from app.
- Set local.app\_modules from app\_modules.
- Set local.module\_app from module\_app.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L29) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L498)

<a id="op-8a498dc39f9d6c"></a>
### Get file items

`operation_foundation_binding_foundation_init_get_file_items`

**Inputs** path, raise\_not\_found = false, ignore\_empty\_lines = true.

**Explicit results** list of p.strip() for p drawn from content.splitlines() where (not ignore\_empty\_lines or (p.strip() and not p.startswith(“#”))) · list().

**Local steps**

- Bind dependencies Platform.utils.
- Set content from read\_file(path, raise\_not\_found = raise\_not\_found).
- If content.
  - Set content from Platform.utils.strip(content).
  - Return list of p.strip() for p drawn from content.splitlines() where (not ignore\_empty\_lines or (p.strip() and not p.startswith(“#”))).
    - Draw p from content.splitlines(), keep a combination only if ((not ignore\_empty\_lines or (p.strip() and not p.startswith(“#”)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ignore\_empty\_lines → (p.strip() and not p.startswith(“#”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in p.strip() → not p.startswith(“#”).
- Otherwise.
  - Return list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1462)

<a id="op-2a2ccd098db93f"></a>
### Get file json

`operation_foundation_binding_foundation_init_get_file_json`

**Inputs** path.

**Explicit results** json.load(f).

**Local steps**

- Within open(path) bound as f.
  - Return json.load(f).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1463)

<a id="op-59fa183e9a4b11"></a>
### Read file

`operation_foundation_binding_foundation_init_read_file`

**Inputs** path, raise\_not\_found = false, as\_base64 = false.

**Explicit results** base64.b64encode(content).decode(“utf-8”) · as\_unicode(content) · no value.

**Explicit failure paths** OSError(formatted text {path} Not Found).

**Local steps**

- If isinstance(path, str).
  - Set path from path.encode(“utf-8”).
- If os.path.exists(path).
  - If as\_base64.
    - Bind dependencies base64.
    - Within open(path, “rb”) bound as f.
      - Set content from f.read().
      - Return base64.b64encode(content).decode(“utf-8”).
  - Otherwise.
    - Within open(path) bound as f.
      - Set content from f.read().
      - Return as\_unicode(content).
- Otherwise.
  - If raise\_not\_found.
    - Raise OSError(formatted text {path} Not Found).
  - Otherwise.
    - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L38) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1470)

<a id="op-a31935f3bafaa5"></a>
### Get attr

`operation_foundation_binding_foundation_init_get_attr`

**Inputs** method\_string.

**Declared result** Any.

**Explicit results** getattr(get\_module(modulename), methodname).

**Local steps**

- Set app\_name from method\_string.split(“.”, 1) at 0.
- If (not local.flags.in\_uninstall and not local.flags.in\_install and app\_name does not belong to get\_installed\_apps()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not local.flags.in\_uninstall → not local.flags.in\_install → app\_name does not belong to get\_installed\_apps().
  - Evaluate throw(translated “App {0} is not installed”.format(app\_name), AppNotInstalledError).
- Set modulename from “.”.join(method\_string.split(“.”) at slice no value to negative 1).
- Set methodname from method\_string.split(“.”) at negative 1.
- Return getattr(get\_module(modulename), methodname).

**Values supplied outside this operation** selected callable from getattr(get\_module(modulename), methodname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1461)

<a id="op-4142c242c2d6c5"></a>
### Call

`operation_foundation_initialize_business_behavior_call`

**Inputs** fn, remaining positional values args, remaining named values kwargs.

**Explicit results** fn(expanded args, expanded names newargs).

**Local steps**

- If isinstance(fn, str).
  - Set fn from get\_attr(fn).
- Set newargs from get\_newargs(fn, kwargs).
- Return fn(expanded args, expanded names newargs).

**Values supplied outside this operation** selected callable from get\_attr(fn).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L17) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L442)

<a id="op-81bf2e94d7e7a0"></a>
### Get cached signature params

`operation_foundation_initialize_business_behavior_get_cached_signature_parameters`

**Inputs** fn.

**Wrappers, in declaration order** functools.lru\_cache.

**Declared result** tuple at tuple(dict at tuple(str, Any), bool).

**Explicit results** tuple(dict(signature.parameters), variable\_kwargs\_exist).

**Local steps**

- Set signature from inspect.signature(fn).
- Set variable\_kwargs\_exist from any(generator of parameter.kind equals inspect.Parameter.VAR\_KEYWORD for parameter drawn from signature.parameters.values()).
  - Draw parameter from signature.parameters.values().
- Return tuple(dict(signature.parameters), variable\_kwargs\_exist).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L5987) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L451)

<a id="op-b22e569b1d6805"></a>
### Get newargs

`operation_foundation_initialize_business_behavior_get_newargs`

**Inputs** fn, kwargs.

**Declared result** dict at tuple(str, Any).

**Explicit results** newargs.

**Local steps**

- Set tuple(parameters, variable\_kwargs\_exist) from \_get\_cached\_signature\_params(fn).
- Set newargs from kwargs.copy() when variable\_kwargs\_exist, otherwise mapping of key → value for tuple(key, value) drawn from kwargs.items() where key belongs to parameters.
  - Value choice on variable\_kwargs\_exist — true gives kwargs.copy(), false gives mapping of key → value for tuple(key, value) drawn from kwargs.items() where key belongs to parameters.
  - Draw tuple(key, value) from kwargs.items(), keep a combination only if (key belongs to parameters).
- Evaluate newargs.pop(“ignore\_permissions”, no value).
- Evaluate newargs.pop(“flags”, no value).
- Return newargs.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L6207) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L457)

<a id="op-2727db9a119e55"></a>
### Make property setter

`operation_foundation_initialize_business_behavior_make_property_setter`

**Inputs** args, ignore\_validate = false, validate\_fields\_for\_doctype = true, is\_system\_generated = true, module (named only, default no value).

**State and service calls** call insert on ps.

**Local steps**

- Set args from \_dict(args).
- If not args.doctype\_or\_field.
  - Set args.doctype\_or\_field from “DocField”.
  - If not args.property\_type.
    - Set args.property\_type from (db.get\_value(“DocField”, mapping(“parent” → “DocField”, “fieldname” → args.property), “fieldtype”) or “Data”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in db.get\_value(“DocField”, mapping(“parent” → “DocField”, “fieldname” → args.property), “fieldtype”) → “Data”.
- If not args.doctype.
  - Set DocField\_doctype from qb.DocType(“DocField”).
  - Set doctype\_list from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.fieldname equals nested operand in the contract.fieldname).distinct().run(pluck = true).
- Otherwise.
  - Set doctype\_list from list(args.doctype).
- For each doctype in doctype\_list.
  - If not args.property\_type.
    - Set args.property\_type from (db.get\_value(“DocField”, mapping(“parent” → doctype, “fieldname” → args.fieldname), “fieldtype”) or “Data”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in db.get\_value(“DocField”, mapping(“parent” → doctype, “fieldname” → args.fieldname), “fieldtype”) → “Data”.
  - Set ps from get\_doc(mapping(“doctype” → “Property Setter”, “doctype\_or\_field” → args.doctype\_or\_field, “doc\_type” → doctype, “module” → module, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.property\_type → “Data”.
  - Set ps.flags.ignore\_validate from ignore\_validate.
  - Set ps.flags.validate\_fields\_for\_doctype from validate\_fields\_for\_doctype.
  - Evaluate ps.validate\_fieldtype\_change().
  - Evaluate ps.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L26) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L482)

<a id="op-861b96558b27e9"></a>
### Import doc

`operation_foundation_initialize_business_behavior_import_record`

**Inputs** path.

**Local steps**

- Bind dependencies import\_doc.
- Evaluate import\_doc(path).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0003.json#L7384) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L469)
