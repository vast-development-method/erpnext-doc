# Shared value and file services · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Jinja

<a id="op-68d51c812dc598"></a>
### Get email from template

`operation_foundation_utils_template_evaluation_business_behavior_get_email_from_template`

**Inputs** name, args.

**Explicit results** tuple(message, text\_content).

**Explicit failure paths** e.

**Local steps**

- Bind dependencies TemplateNotFound.
- Set args from (args or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → mapping().
- Attempt the following.
  - Set message from get\_template(((“templates/emails/” + name) + “.html”)).render(args).
- On failure (TemplateNotFound) bound to e.
  - Raise e.
- Attempt the following.
  - Set text\_content from get\_template(((“templates/emails/” + name) + “.txt”)).render(args).
- On failure (TemplateNotFound).
  - Set text\_content from no value.
- Return tuple(message, text\_content).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L1126) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2035) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L801)

<a id="op-32a808aa28662c"></a>
### Validate template

`operation_foundation_utils_template_evaluation_business_behavior_validate_template`

**Inputs** html, restrict\_globals = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — formatted text Syntax error in template as line {e.lineno}: {e.message}.

**Local steps**

- Bind dependencies TemplateSyntaxError.
- Bind dependencies Platform.
- If not html.
  - Return no value.
- Set jenv from get\_jenv(restrict\_globals = restrict\_globals).
- Attempt the following.
  - Evaluate jenv.from\_string(html).
- On failure (TemplateSyntaxError) bound to e.
  - Call the validation error handler Platform.throw(formatted text Syntax error in template as line {e.lineno}: {e.message}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L1394) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2046) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L812)

<a id="op-daa84d4f5a7c1c"></a>
### Render template

`operation_foundation_utils_template_evaluation_business_behavior_render_template`

**Inputs** template, context = no value, is\_path = no value, safe\_render = true, restrict\_globals (named only, default no value).

**Explicit results** empty text · compiled\_template.render(context).

**Local steps**

- If not template.
  - Return empty text.
- Bind dependencies TemplateError.
- Bind dependencies SandboxedEnvironment.
- Bind dependencies \_, throw.
- If context is identical to no value.
  - Set context from mapping().
- Attempt the following.
  - If (is\_path or guess\_is\_path(template)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_path → guess\_is\_path(template).
    - Set is\_path from true.
    - Set compiled\_template from get\_template(template).
  - Otherwise.
    - Set jenv from get\_jenv(restrict\_globals = restrict\_globals).
    - If (safe\_render and “.\_\_” belongs to template).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in safe\_render → “.\_\_” belongs to template.
      - Evaluate throw(translated “Illegal template”).
    - Set compiled\_template from jenv.from\_string(template).
- On failure (TemplateError).
  - Evaluate \_throw\_render\_error(translated “Jinja Template Error”, template = template).
- Bind dependencies time.
- Bind dependencies get\_logger.
- Set logger from get\_logger(“render-template”).
- Attempt the following.
  - Set start\_time from time.monotonic().
  - Within safe\_render\_flags().
    - Return compiled\_template.render(context).
- On failure (Exception) bound to e.
  - Evaluate \_throw\_render\_error(translated “Context Error”, exc = e).
- On exit, including pending return or failure.
  - If is\_path.
    - Evaluate logger.debug(formatted text Rendering time: {(time.monotonic() − start\_time)} seconds ({template})).
  - Otherwise.
    - Evaluate logger.debug(formatted text Rendering time: {(time.monotonic() − start\_time)} seconds).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L83) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2043) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L809)

<a id="op-46a3d5215856b9"></a>
### Throw render error

`operation_foundation_binding_foundation_utils_jinja_throw_render_error`

**Inputs** title, template = no value, exc = Platform.ValidationError.

**Explicit failure paths** validation helper with exc — msg.

**Local steps**

- Bind dependencies html.
- Bind dependencies get\_logger.
- Bind dependencies is\_traceback\_allowed.
- Set traceback from Platform.get\_traceback().
- If is\_traceback\_allowed().
  - Set source from formatted text &lt;pre&gt;{html.escape(template)}&lt;/pre&gt; when template, otherwise empty text.
    - Value choice on template — true gives formatted text &lt;pre&gt;{html.escape(template)}&lt;/pre&gt;, false gives empty text.
  - Set msg from formatted text {source}&lt;pre&gt;{html.escape(traceback)}&lt;/pre&gt;.
- Otherwise.
  - Evaluate get\_logger(“render-template”).error(formatted text {title} {traceback}).
  - Set msg from Platform.\_(“There was an error while rendering this template.”).
- Call the validation error handler Platform.throw(msg, title = title, exc = exc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L59) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L217)

<a id="op-23850812615e42"></a>
### Guess is path

`operation_foundation_utils_template_evaluation_business_behavior_guess_is_path`

**Inputs** template.

**Explicit results** true · false.

**Local steps**

- If (whitespace '\\n' does not belong to template and “.” belongs to template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in whitespace '\\n' does not belong to template → “.” belongs to template.
  - Set extn from template.rsplit(“.”) at negative 1.
  - If extn belongs to tuple(“html”, “css”, “scss”, “py”, …).
    - Return true.
- Return false.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L2490) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2042) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L808)

<a id="op-efe34d7800bd10"></a>
### Get jloader

`operation_foundation_utils_template_evaluation_business_behavior_get_jloader`

**Inputs** no declared parameters.

**Explicit results** jloader.

**Local steps**

- Set jloader from \_get\_jloader().
- Set Platform.local.jloader from jloader.
- Return jloader.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L2698) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2039) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L805)

<a id="op-35de77b4131e55"></a>
### Get jloader

`operation_foundation_utils_template_evaluation_business_behavior_get_jloader_2`

**Inputs** no declared parameters.

**Wrappers, in declaration order** site\_cache(ttl = (10 × 60), maxsize = 8).

**Explicit results** jloader.

**Local steps**

- Bind dependencies ChoiceLoader, PackageLoader, PrefixLoader.
- Bind dependencies Platform.
- Set apps from Platform.get\_hooks(“template\_apps”).
- If not apps.
  - Set apps from list(reversed(Platform.get\_installed\_apps(\_ensure\_on\_bench = true))).
- If “Platform” does not belong to apps.
  - Evaluate apps.append(“Platform”).
- Set jloader from ChoiceLoader((list(PrefixLoader(mapping of app → PackageLoader(app, “.”) for app drawn from apps)) + list of PackageLoader(app, “.”) for app drawn from apps)).
  - Draw app from apps.
  - Draw app from apps.
- Return jloader.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“template\_apps”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L82) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2040) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L806)

<a id="op-5604cea508d7b6"></a>
### Set filters

`operation_foundation_utils_template_evaluation_business_behavior_set_filters`

**Inputs** jenv.

**Local steps**

- Bind dependencies Platform.
- Bind dependencies cint, cstr, flt.
- Evaluate jenv.filters.update(mapping(“json” → Platform.as\_json, “len” → len, “int” → cint, “str” → cstr, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L3140) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2045) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L811)

<a id="op-68f2f859cb7b1c"></a>
### Get jinja hooks

`operation_foundation_utils_template_evaluation_business_behavior_get_document_template_hooks`

**Inputs** no declared parameters.

**Explicit results** tuple(no value, no value) · tuple(method\_dict, filter\_dict).

**Local steps**

- Bind dependencies Platform.
- If not getattr(Platform.local, “site”, no value).
  - Return tuple(no value, no value).
- Bind dependencies getmembers, isfunction.
- Bind dependencies FunctionType, ModuleType.
- Bind local operation get\_obj\_dict\_from\_paths for subsequent calls.
- Set values from Platform.get\_hooks(“jinja”).
- Set tuple(methods, filters) from tuple(values.get(“methods”, list()), values.get(“filters”, list())).
- Set method\_dict from get\_obj\_dict\_from\_paths(methods).
- Set filter\_dict from get\_obj\_dict\_from\_paths(filters).
- Return tuple(method\_dict, filter\_dict).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “site”, no value), Platform.get\_hooks(“jinja”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L80) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2033) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L799)

<a id="op-0d4bf8ea8f7e82"></a>
### Get jinja hooks.get obj dict from paths

`operation_foundation_utils_template_evaluation_business_behavior_get_document_template_hooks_get_obj_mapping_from_paths`

**Inputs** object\_paths.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- For each obj\_path in object\_paths.
  - Attempt the following.
    - Set obj from Platform.get\_module(obj\_path).
  - On failure (ModuleNotFoundError).
    - Set obj from Platform.get\_attr(obj\_path).
  - If isinstance(obj, ModuleType).
    - Set functions from getmembers(obj, isfunction).
    - For each tuple(function\_name, function) in functions.
      - If function.\_\_module\_\_ equals obj.\_\_name\_\_.
        - Set out at function\_name from function.
  - Otherwise.
    - If isinstance(obj, FunctionType).
      - Set function\_name from obj.\_\_name\_\_.
      - Set out at function\_name from obj.
- Return out.

**Values supplied outside this operation** selected callable from Platform.get\_attr(obj\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L81) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2034) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L800)

<a id="op-bdb79c08e3c5d9"></a>
### Safe render flags

`operation_foundation_utils_template_evaluation_business_behavior_safe_render_flags`

**Inputs** no declared parameters.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- If Platform.flags.in\_render\_safe\_exec is identical to no value.
  - Set Platform.flags.in\_render\_safe\_exec from 0.
- Update Platform.flags.in\_render\_safe\_exec using + 1.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Update Platform.flags.in\_render\_safe\_exec using − 1.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L84) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2044) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L810)

## Service · Jinja globals

<a id="op-b9e14a7294b754"></a>
### Resolve class

`operation_foundation_utils_template_evaluation_globals_business_behavior_resolve_class`

**Inputs** remaining positional values classes.

**Explicit results** empty text · one space.join(generator of resolve\_class(c) for c drawn from classes).strip() · one space.join(generator of classname for classname drawn from classes where classes at classname).strip() · classes.

**Local steps**

- If (classes and len(classes) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in classes → len(classes) equals 1.
  - Set classes from classes at 0.
- If classes is identical to no value.
  - Return empty text.
- If classes is identical to false.
  - Return empty text.
- If isinstance(classes, (list bitwise or tuple)).
  - Return one space.join(generator of resolve\_class(c) for c drawn from classes).strip().
    - Draw c from classes.
- If isinstance(classes, dict).
  - Return one space.join(generator of classname for classname drawn from classes where classes at classname).strip().
    - Draw classname from classes, keep a combination only if (classes at classname).
- Return classes.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L4343) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2054) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L820)

<a id="op-2af35ee61ec904"></a>
### Inspect

`operation_foundation_utils_template_evaluation_globals_business_behavior_inspect`

**Inputs** var, render = true.

**Explicit results** empty text · get\_jenv().from\_string(html).render(context).

**Local steps**

- Bind dependencies get\_jenv.
- Set context from mapping(“var” → var).
- If render.
  - Set html from text in the contract.
- Otherwise.
  - Return empty text.
- Return get\_jenv().from\_string(html).render(context).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L4688) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2052) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L818)

<a id="op-383faeefaa0931"></a>
### Web block

`operation_foundation_utils_template_evaluation_globals_business_behavior_web_block`

**Inputs** template, values = no value, remaining named values kwargs.

**Explicit results** web\_blocks(list(options)).

**Local steps**

- Set options from mapping(“template” → template, “values” → values).
- Evaluate options.update(kwargs).
- Return web\_blocks(list(options)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L4842) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2055) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L821)

<a id="op-bf4c863e60d26b"></a>
### Web blocks

`operation_foundation_utils_template_evaluation_globals_business_behavior_web_blocks`

**Inputs** blocks.

**Explicit results** html.

**Local steps**

- Bind dependencies Platform.
- Bind dependencies \_, \_dict, throw.
- Bind dependencies get\_web\_blocks\_html.
- Set web\_blocks from list().
- For each block in blocks.
  - If not block.get(“template”).
    - Evaluate throw(translated “Web Template is not specified”).
  - Set doc from \_dict(mapping(“doctype” → “Web Page Block”, “web\_template” → block at “template”, “web\_template\_values” → block.get(“values”, mapping()), “add\_top\_padding” → 1, …)).
  - Evaluate doc.update(block).
  - Evaluate web\_blocks.append(doc).
- Set out from get\_web\_blocks\_html(web\_blocks).
- Set html from out.html.
- If not Platform.flags.web\_block\_scripts.
  - Set Platform.flags.web\_block\_scripts from mapping().
  - Set Platform.flags.web\_block\_styles from mapping().
- For each tuple(template, scripts) in out.scripts.items().
  - If template does not belong to Platform.flags.web\_block\_scripts.
    - For each script in scripts.
      - Update html using + formatted text &lt;script data-web-template='{template}'&gt;{script}&lt;/script&gt;.
    - Set Platform.flags.web\_block\_scripts at template from true.
- For each tuple(template, styles) in out.styles.items().
  - If template does not belong to Platform.flags.web\_block\_styles.
    - For each style in styles.
      - Update html using + formatted text &lt;style data-web-template='{template}'&gt;{style}&lt;/style&gt;.
    - Set Platform.flags.web\_block\_styles at template from true.
- Return html.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L4979) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2056) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L822)

<a id="op-1198c8b65807b9"></a>
### Get dom id

`operation_foundation_utils_template_evaluation_globals_business_behavior_get_dom_identifier`

**Inputs** seed = no value.

**Explicit results** (“id-” + generate\_hash(12)).

**Local steps**

- Bind dependencies generate\_hash.
- Return (“id-” + generate\_hash(12)).

**Values supplied outside this operation** clock or generated value from generate\_hash(12).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L5811) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2048) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L814)

<a id="op-882edb788ce94d"></a>
### Include script

`operation_foundation_utils_template_evaluation_globals_business_behavior_include_script`

**Inputs** path, preload = true.

**Explicit results** formatted text &lt;script type="text/javascript" src="{path}"&gt;&lt;/script&gt;.

**Local steps**

- Set path from bundled\_asset(path).
- If preload.
  - Bind dependencies Platform.
  - Evaluate Platform.local.preload\_assets at “script”.append(path).
- Return formatted text &lt;script type="text/javascript" src="{path}"&gt;&lt;/script&gt;.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L5882) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2050) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L816)

<a id="op-2b0b8b1c450b9a"></a>
### Include icons

`operation_foundation_utils_template_evaluation_globals_business_behavior_include_icons`

**Inputs** path, preload = true.

**Explicit results** ((text in the contract + path) + “?v=${window.\_version\_number}′, {credentials: "same-origin"}).then((r) =&gt; r.text()).then((svg) =&gt; {let c = do …”).

**Local steps**

- Set path from bundled\_asset(path).
- If preload.
  - Bind dependencies Platform.
  - Evaluate Platform.local.preload\_assets at “icons”.append(path).
- Return ((text in the contract + path) + “?v=${window.\_version\_number}′, {credentials: "same-origin"}).then((r) =&gt; r.text()).then((svg) =&gt; {let c = do …”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L6042) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2049) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L815)

<a id="op-df59f39e419e08"></a>
### Include style

`operation_foundation_utils_template_evaluation_globals_business_behavior_include_style`

**Inputs** path, rtl = no value, preload = true.

**Explicit results** formatted text &lt;link type="text/css" rel="stylesheet" href="{path}"&gt;.

**Local steps**

- Set path from bundled\_asset(path).
- If preload.
  - Bind dependencies Platform.
  - Evaluate Platform.local.preload\_assets at “style”.append(path).
- Return formatted text &lt;link type="text/css" rel="stylesheet" href="{path}"&gt;.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L6193) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2051) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L817)

<a id="op-ef54f21008f1c1"></a>
### Bundled asset

`operation_foundation_utils_template_evaluation_globals_business_behavior_bundled_asset`

**Inputs** path, rtl = no value.

**Explicit results** abs\_url(path).

**Local steps**

- Bind dependencies get\_assets\_json.
- Bind dependencies abs\_url.
- If (“.bundle.” belongs to path and not path.startswith(“/assets”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “.bundle.” belongs to path → not path.startswith(“/assets”).
  - Set bundled\_assets from get\_assets\_json().
  - If (path.endswith(“.css”) and is\_rtl(rtl)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in path.endswith(“.css”) → is\_rtl(rtl).
    - Set path from formatted text rtl\_{path}.
  - Set path from (bundled\_assets.get(path) or path).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundled\_assets.get(path) → path.
- Return abs\_url(path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L6363) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2047) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L813)

<a id="op-db28121de569f8"></a>
### Is rtl

`operation_foundation_utils_template_evaluation_globals_business_behavior_is_rtl`

**Inputs** rtl = no value.

**Explicit results** local.lang belongs to list(“ar”, “he”, “fa”, “ps”) · rtl.

**Local steps**

- Bind dependencies local.
- If rtl is identical to no value.
  - Return local.lang belongs to list(“ar”, “he”, “fa”, “ps”).
- Return rtl.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L85) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2053) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L819)

## Service · Lazy loader

<a id="op-492d33568338a1"></a>
### Lazy import

`operation_foundation_utils_lazy_loader_business_behavior_lazy_import`

**Inputs** name, package = no value.

**Explicit results** sys.modules at name · module.

**Explicit failure paths** ImportError(formatted text Module {name} Not found.).

**Local steps**

- If name belongs to sys.modules.
  - Return sys.modules at name.
- Set spec from importlib.util.find\_spec(name, package).
- If not spec.
  - Raise ImportError(formatted text Module {name} Not found.).
- Set loader from importlib.util.LazyLoader(spec.loader).
- Set spec.loader from loader.
- Set module from importlib.util.module\_from\_spec(spec).
- Set sys.modules at name from module.
- Evaluate loader.exec\_module(module).
- Return module.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L6857) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L311)

## Service · Legacy gravatar cleanup

<a id="op-369f4343068650"></a>
### Get gravatar image fields

`operation_foundation_utils_legacy_gravatar_cleanup_business_behavior_get_gravatar_image_fields`

**Inputs** no declared parameters.

**Explicit results** fields.

**Local steps**

- Set fields from list(BASE\_GRAVATAR\_IMAGE\_FIELDS).
- If “Enterprise” belongs to Platform.get\_installed\_apps().
  - Evaluate fields.extend(Enterprise\_GRAVATAR\_IMAGE\_FIELDS).
- Return fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L7178) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L313)

<a id="op-47311b46ce35a8"></a>
### Should show gravatar deletion prompt

`operation_foundation_utils_legacy_gravatar_cleanup_business_behavior_should_show_gravatar_deletion_prompt`

**Inputs** no declared parameters.

**Explicit results** false · has\_gravatar\_image\_urls().

**Local steps**

- If “System Manager” does not belong to Platform.get\_roles().
  - Return false.
- If cint(Platform.defaults.get\_global\_default(SKIP\_GRAVATAR\_DELETION\_PROMPT)).
  - Return false.
- If is\_job\_enqueued(GRAVATAR\_DELETION\_JOB\_ID).
  - Return false.
- Return has\_gravatar\_image\_urls().

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L7289) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L315)
