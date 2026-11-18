# Site operations and diagnostics · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Environment

<a id="op-1a10e565279e50"></a>
### Initialize test environment

`operation_foundation_testing_environment_business_behavior_initialize_test_environment`

**Inputs** site, config.

**Wrappers, in declaration order** debug\_timer.

**Explicit failure paths** TestRunnerError(formatted text Failed to connect to the database: {e}).

**Local steps**

- Evaluate logger.debug(formatted text Initializing test environment for site: {site}).
- Evaluate Platform.init(site).
- If not Platform.db.
  - Evaluate Platform.connect().
- Attempt the following.
  - Evaluate \_disable\_scheduler\_if\_needed().
  - Evaluate Platform.clear\_cache().
- On failure (Exception) bound to e.
  - Evaluate logger.error(formatted text Error connecting to the database: {e}).
  - Raise TestRunnerError(formatted text Failed to connect to the database: {e}) with cause e.
- Evaluate toggle\_test\_mode(true).
- Set Platform.flags.print\_messages from logger.getEffectiveLevel() &lt; logging.INFO.
- Set Platform.flags.tests\_verbose from logger.getEffectiveLevel() &lt; logging.INFO.
- Evaluate \_decorate\_all\_methods\_and\_functions\_with\_type\_checker().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L45) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L603)

<a id="op-780baa50d36fe3"></a>
### Cleanup after tests

`operation_foundation_testing_environment_business_behavior_cleanup_after_tests`

**Inputs** no declared parameters.

**State and service calls** commit.

**Local steps**

- Use module bindings scheduler\_disabled\_by\_user.
- If not scheduler\_disabled\_by\_user.
  - Evaluate Platform.utils.scheduler.enable\_scheduler().
- If Platform.db.
  - Evaluate Platform.db.commit().
  - Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L4490) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L601)

<a id="op-3a458baf52e5c7"></a>
### Disable scheduler if needed

`operation_foundation_testing_environment_business_behavior_disable_scheduler_if_needed`

**Inputs** no declared parameters.

**Local steps**

- Use module bindings scheduler\_disabled\_by\_user.
- Set scheduler\_disabled\_by\_user from Platform.utils.scheduler.is\_scheduler\_disabled(verbose = false).
- If not scheduler\_disabled\_by\_user.
  - Evaluate Platform.utils.scheduler.disable\_scheduler().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L4614) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L602)

<a id="op-dd67b17a524057"></a>
### Decorate all methods and functions with type checker

`operation_foundation_binding_foundation_testing_environment_decorate_all_methods_and_functions_with_type_checker`

**Inputs** no declared parameters.

**Wrappers, in declaration order** debug\_timer.

**Local steps**

- Bind dependencies validate\_argument\_types.
- Bind local operation \_get\_config\_from\_pyproject for subsequent calls.
- Bind local operation \_decorate\_callable for subsequent calls.
- Bind local operation \_decorate\_module for subsequent calls.
- For each app in apps bound to Platform.get\_installed\_apps().
  - Set config from \_get\_config\_from\_pyproject(Platform.get\_app\_source\_path(app)).
  - Set max\_depth from config.get(“max\_module\_depth”, 0).
  - Set skip\_namespaces from config.get(“skip\_namespaces”, list()).
  - Evaluate logger.info(formatted text Adding type validator in {app} (up to level {max\_depth})...).
  - Set pkg from Platform.get\_module(app).
  - Evaluate \_decorate\_module(app, pkg, apps, 1, …).
  - For each tuple(\_, submodule\_name, \_) in pkgutil.walk\_packages(path = pkg.\_\_path\_\_, prefix = (pkg.\_\_name\_\_ + “.”)).
    - Set current\_depth from len(submodule\_name.split(“.”)).
    - If current\_depth &gt; max\_depth.
      - Continue with the next iteration or loop test.
    - If any(generator of submodule\_name.startswith(n) for n drawn from skip\_namespaces).
      - Draw n from skip\_namespaces.
      - Continue with the next iteration or loop test.
    - Set submodule from Platform.get\_module(submodule\_name).
    - Evaluate \_decorate\_module(app, submodule, apps, current\_depth, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L47) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L117) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L205)

<a id="op-e7de709d0cf99f"></a>
### Decorate all methods and functions with type checker.get config from pyproject

`operation_foundation_binding_foundation_testing_environment_decorate_all_methods_and_functions_with_type_checker_get_config_from_pyproject`

**Inputs** app\_path.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract).get(“Platform”, mapping()).get(“testing”, mapping()).get(“function\_type\_validation”, mapping()) · mapping().

**Local steps**

- Attempt the following.
  - Within open(formatted text {app\_path}/pyproject.toml, “rb”) bound as f.
    - Set config from tomllib.load(f).
    - Return nested operand in the contract(nested operand in the contract, nested operand in the contract).get(“Platform”, mapping()).get(“testing”, mapping()).get(“function\_type\_validation”, mapping()).
- On failure (FileNotFoundError).
  - Return mapping().
- On failure (tomllib.TOMLDecodeError).
  - Evaluate logger.warning(formatted text Failed to parse pyproject.toml for app {app\_path}).
  - Return mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L51) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L209)

<a id="op-a917a3f9709aa5"></a>
### Decorate all methods and functions with type checker.decorate callable

`operation_foundation_binding_foundation_testing_environment_decorate_all_methods_and_functions_with_type_checker_decorate_callable`

**Inputs** obj, parent\_module.

**Explicit results** obj · wrapper.

**Local steps**

- If getattr(obj, “\_\_func\_\_”, obj) belongs to Platform.whitelisted.
  - Return obj.
- Otherwise.
  - If hasattr(obj, “\_is\_decorated\_for\_validate\_argument\_types”).
    - Return obj.
  - Otherwise.
    - If module bound to getattr(obj, “\_\_module\_\_”, empty text).
      - Set app from module.split(“.”, 1) at 0.
      - Set config from \_get\_config\_from\_pyproject(Platform.get\_app\_source\_path(app)).
      - Set skip\_namespaces from config.get(“skip\_namespaces”, list()).
      - If any(generator of module.startswith(n) for n drawn from skip\_namespaces).
        - Draw n from skip\_namespaces.
        - Return obj.
- Bind local operation wrapper for subsequent calls.
- Set wrapper.\_is\_decorated\_for\_validate\_argument\_types from true.
- If obj.\_\_module\_\_ differs from parent\_module.\_\_name\_\_.
  - Evaluate logger.debug(formatted text ... patching {obj.\_\_module\_\_}.{obj.\_\_name\_\_} (inside {parent\_module.\_\_name\_\_})).
- Otherwise.
  - Evaluate logger.debug(formatted text ... patching {obj.\_\_module\_\_}.{obj.\_\_name\_\_}).
- Return wrapper.

**Values supplied outside this operation** selected callable from getattr(obj, “\_\_func\_\_”, obj), getattr(obj, “\_\_module\_\_”, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L48) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L206)

<a id="op-3883a42a082c99"></a>
### Decorate all methods and functions with type checker.decorate callable.wrapper

`operation_foundation_binding_foundation_testing_environment_decorate_all_methods_and_functions_with_type_checker_decorate_callable_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(obj).

**Explicit results** validate\_argument\_types(obj)(expanded args, expanded names kwargs).

**Local steps**

- Return validate\_argument\_types(obj)(expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L49) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L207)

<a id="op-314e4b8209657d"></a>
### Decorate all methods and functions with type checker.decorate module

`operation_foundation_binding_foundation_testing_environment_decorate_all_methods_and_functions_with_type_checker_decorate_module`

**Inputs** app, module, apps, current\_depth, max\_depth.

**Explicit results** no value.

**Local steps**

- If current\_depth &gt; max\_depth.
  - Return no value.
- For each name in dir(module).
  - Set obj from getattr(module, name).
  - If inspect.isfunction(obj).
    - If not getattr(obj, “\_\_annotations\_\_”, no value).
      - Continue with the next iteration or loop test.
    - If obj.\_\_module\_\_.split(“.”, 1) at 0 does not belong to apps.
      - Continue with the next iteration or loop test.
    - Evaluate setattr(module, name, \_decorate\_callable(obj, module)).
  - Otherwise.
    - If inspect.ismodule(obj).
      - If obj.\_\_name\_\_.split(“.”, 1) at 0 differs from app.
        - Continue with the next iteration or loop test.
      - If hasattr(obj, “\_is\_decorated\_for\_validate\_argument\_types”).
        - Continue with the next iteration or loop test.
      - Set obj.\_is\_decorated\_for\_validate\_argument\_types from true.
      - Evaluate \_decorate\_module(app, obj, apps, (current\_depth + 1), …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(module, name), getattr(obj, “\_\_annotations\_\_”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L50) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L208)

<a id="op-92bc66cf7c7e50"></a>
### Integration Test Preparation.initialize

`operation_foundation_testing_environment_business_behavior_integration_test_preparation_initialize`

**Inputs** self, cfg.

**Local steps**

- Set self.cfg from cfg.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L4726) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L606)

<a id="op-3369157bb26a79"></a>
### Integration Test Preparation.invoke

`operation_foundation_testing_environment_business_behavior_integration_test_preparation_call`

**Inputs** self, suite, app, category.

**Declared result** no value.

**Local steps**

- If not self.cfg.skip\_before\_tests.
  - Evaluate self.\_run\_before\_test\_hooks(app, category).
- Otherwise.
  - Evaluate logger.debug(“Skipping before\_tests hooks: Explicitly skipped”).
- Evaluate self.\_create\_global\_test\_record\_dependencies(app, category).

If control reaches the end, it returns no value.

**Methods declared on this owner** [run before test hooks](operations-004.md#op-e4bf0dc30ed772), [create global test record dependencies](operations-004.md#op-0ab25a11449187).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L4780) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L604)

<a id="op-e4bf0dc30ed772"></a>
### Integration Test Preparation.run before test hooks

`operation_foundation_testing_environment_business_behavior_integration_test_preparation_run_before_test_hooks`

**Inputs** app, category.

**Wrappers, in declaration order** staticmethod, debug\_timer.

**Local steps**

- Evaluate logger.info(formatted text Running "before\_tests" hooks for {category} tests on app: {app}).
- For each hook\_function in Platform.get\_hooks(“before\_tests”, app\_name = app).
  - Evaluate logger.info(formatted text Running "before\_tests" hook function {hook\_function}).
  - Evaluate Platform.get\_attr(hook\_function)().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“before\_tests”, app\_name = app), Platform.get\_attr(hook\_function).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L4952) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L607)

<a id="op-0ab25a11449187"></a>
### Integration Test Preparation.create global test record dependencies

`operation_foundation_testing_environment_business_behavior_integration_test_preparation_create_global_test_record_dependencies`

**Inputs** app, category.

**Wrappers, in declaration order** staticmethod, debug\_timer.

**Local steps**

- Attempt the following.
  - Set test\_module from Platform.get\_module(formatted text {app}.tests).
  - If hasattr(test\_module, “global\_test\_dependencies”).
    - Evaluate logger.info(formatted text Creating global test record dependencies for {category} tests on {app} ...).
    - For each doctype in test\_module.global\_test\_dependencies.
      - Evaluate logger.debug(formatted text Creating global test records for {doctype}).
      - Evaluate make\_test\_records(doctype, commit = true).
- On failure (ModuleNotFoundError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L5172) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1931) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L605)

## Service · Exceptions

<a id="op-ecb000533b5d09"></a>
### Site Not Specified Error.initialize

`operation_foundation_exceptions_business_behavior_site_not_specified_error_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set self.message from “Please specify --site sitename”.
- Evaluate super(Exception, self).\_\_init\_\_(self.message).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L1416) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L309)

<a id="op-37104c43e45072"></a>
### Does Not Exist Error.initialize

`operation_foundation_exceptions_business_behavior_does_not_exist_error_initialize`

**Inputs** self, remaining positional values args, doctype (named only, default no value).

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args).
- Set self.doctype from doctype.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L1517) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L306)

<a id="op-f34c04387ace97"></a>
### Redirect.initialize

`operation_foundation_exceptions_business_behavior_redirect_initialize`

**Inputs** self, http\_status\_code = 301.

**Local steps**

- Set self.http\_status\_code from http\_status\_code.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L1613) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L308)

<a id="op-d8dfa08e4509f5"></a>
### Improper DBConfiguration Error.initialize

`operation_foundation_exceptions_business_behavior_improper_database_configuration_error_initialize`

**Inputs** self, reason, msg = no value.

**Local steps**

- If not msg.
  - Set msg from “MariaDb is not properly configured”.
- Evaluate super().\_\_init\_\_(msg).
- Set self.reason from reason.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L1676) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L307)

<a id="op-4ed3f0a258df94"></a>
### Command Failed Error.initialize

`operation_foundation_exceptions_business_behavior_command_failed_error_initialize`

**Inputs** self, message, out, err.

**Local steps**

- Evaluate super().\_\_init\_\_(message).
- Set self.out from out.
- Set self.err from err.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L1798) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L305)

## Service · Export file

<a id="op-94c26baba7760f"></a>
### Export doc

`operation_foundation_modules_export_file_business_behavior_export_record`

**Inputs** doc.

**Local steps**

- Evaluate write\_document\_file(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L546) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1373)

<a id="op-ff8dfe861ecd98"></a>
### Export to files

`operation_foundation_modules_export_file_business_behavior_export_to_files`

**Inputs** record\_list = no value, record\_module = no value, verbose = 0, create\_init = no value, record\_app = no value.

**Record and data access** resolve a document from record at 0 via get\_doc.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_import.
  - Return no value.
- If record\_list.
  - For each record in record\_list.
    - Set folder\_name from record at 2 when len(record) equals 3, otherwise no value.
      - Value choice on len(record) equals 3 — true gives record at 2, false gives no value.
    - Evaluate write\_document\_file(Platform.get\_doc(record at 0, record at 1), record\_module, create\_init = create\_init, folder\_name = folder\_name, record\_app = record\_app).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L598) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1375)

<a id="op-bd913fa3cbf458"></a>
### Write document file

`operation_foundation_modules_export_file_business_behavior_write_document_file`

**Inputs** doc, record\_module = no value, create\_init = true, folder\_name = no value, record\_app = no value.

**Record and data access** read “Module Def” via get\_value.

**Explicit failure paths** validation helper — (“Invalid export path: ” + Path(path).as\_posix()).

**Local steps**

- Set doc\_export from doc.as\_dict(no\_nulls = true, ignore\_computed\_child\_tables = true).
- Evaluate doc.run\_method(“before\_export”, doc\_export).
- Set doc\_export from strip\_default\_fields(doc, doc\_export).
- Set module from no value when record\_app, otherwise (record\_module or get\_module\_name(doc)).
  - Value choice on record\_app — true gives no value, false gives (record\_module or get\_module\_name(doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in record\_module → get\_module\_name(doc).
- Set is\_custom\_module from Platform.db.get\_value(“Module Def”, module, “custom”) when module, otherwise no value.
  - Value choice on module — true gives Platform.db.get\_value(“Module Def”, module, “custom”), false gives no value.
- If folder\_name.
  - Set folder from create\_folder(module, folder\_name, doc.name, create\_init, …).
- Otherwise.
  - Set folder from create\_folder(module, doc.doctype, doc.name, create\_init, …).
- Set fname from scrub(doc.name).
- Evaluate write\_code\_files(folder, fname, doc, doc\_export).
- Set path from os.path.join(folder, formatted text {fname}.json).
- If (is\_custom\_module and not nested operand in the contract(nested operand in the contract).resolve().is\_relative\_to(Path(nested operand in the contract()).resolve())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_custom\_module → not Path(path).resolve().is\_relative\_to(Path(nested operand in the contract.get\_site\_path()).resolve()).
  - Call the validation error handler Platform.throw((“Invalid export path: ” + Path(path).as\_posix())).
- Within open(path, “w+”) bound as txtfile.
  - Evaluate txtfile.write((Platform.as\_json(doc\_export) + whitespace '\\n')).
- Evaluate print(formatted text Wrote document file for {doc.doctype} {doc.name} at {path}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“before\_export”, doc\_export).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L867) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L801) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1382)

<a id="op-479a213f58b661"></a>
### Strip default fields

`operation_foundation_modules_export_file_business_behavior_strip_default_fields`

**Inputs** doc, doc\_export.

**Explicit results** doc\_export.

**Local steps**

- If (doc.doctype equals “DocType” and doc.migration\_hash).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “DocType” → doc.migration\_hash.
  - Remove doc\_export at “migration\_hash”.
- For each df in doc.meta.get\_table\_fields().
  - For each d in doc\_export.get(df.fieldname).
    - For each fieldname in (Platform.model.default\_fields + Platform.model.child\_table\_fields).
      - If fieldname belongs to d.
        - Remove d at fieldname.
- Return doc\_export.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L1692) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1380)

<a id="op-aa4664fc7737ae"></a>
### Write code files

`operation_foundation_modules_export_file_business_behavior_write_code_files`

**Inputs** folder, fname, doc, doc\_export.

**Explicit failure paths** validation helper — (“Invalid export path: ” + Path(path).as\_posix()).

**Local steps**

- If hasattr(doc, “get\_code\_fields”).
  - For each tuple(key, extn) in doc.get\_code\_fields().items().
    - If doc.get(key).
      - Set path from os.path.join(folder, ((fname + “.”) + extn)).
      - If not Path(path).resolve().is\_relative\_to(Path(nested operand in the contract.get\_site\_path()).resolve()).
        - Call the validation error handler Platform.throw((“Invalid export path: ” + Path(path).as\_posix())).
      - Within open(path, “w+”) bound as txtfile.
        - Evaluate txtfile.write(doc.get(key)).
      - Remove doc\_export at key.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L1945) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1381)

<a id="op-4544b0d5965cbd"></a>
### Get module name

`operation_foundation_modules_export_file_business_behavior_get_module_name`

**Inputs** doc.

**Record and data access** read “DocType” via get\_value.

**Explicit results** module.

**Local steps**

- If doc.doctype equals “Module Def”.
  - Set module from doc.name.
- Otherwise.
  - If doc.doctype equals “Workflow”.
    - Set module from Platform.db.get\_value(“DocType”, doc.document\_type, “module”).
  - Otherwise.
    - If hasattr(doc, “module”).
      - Set module from doc.module.
    - Otherwise.
      - Set module from Platform.db.get\_value(“DocType”, doc.doctype, “module”).
- Return module.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L2374) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1378)

<a id="op-06fdd683c1971d"></a>
### Export root

`operation_foundation_modules_export_file_business_behavior_export_root`

**Inputs** module = no value, is\_custom\_module = no value, record\_app = no value.

**Declared result** str.

**Explicit results** Platform.get\_app\_path(record\_app) · get\_custom\_module\_path(module) · get\_module\_path(module).

**Local steps**

- If record\_app.
  - Return Platform.get\_app\_path(record\_app).
- If is\_custom\_module.
  - Return get\_custom\_module\_path(module).
- Return get\_module\_path(module).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L2653) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1374)
