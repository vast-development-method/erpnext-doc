# Site operations and diagnostics · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Export file

<a id="op-f3cc064ccc2f50"></a>
### Exported file path

`operation_foundation_modules_export_file_business_behavior_exported_file_path`

**Inputs** root, dt, dn.

**Declared result** str.

**Explicit results** os.path.join(root, dt, dn, formatted text {dn}.json).

**Local steps**

- Set tuple(dt, dn) from scrub\_dt\_dn(dt, dn).
- Return os.path.join(root, dt, dn, formatted text {dn}.json).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L2795) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1376)

<a id="op-fd166d0def0547"></a>
### Delete folder

`operation_foundation_modules_export_file_business_behavior_delete_folder`

**Inputs** module, dt, dn, record\_app = no value.

**Record and data access** read “Module Def” via get\_value.

**Local steps**

- Set is\_custom\_module from Platform.db.get\_value(“Module Def”, module, “custom”) when module, otherwise no value.
  - Value choice on module — true gives Platform.db.get\_value(“Module Def”, module, “custom”), false gives no value.
- Set root from export\_root(module, is\_custom\_module, record\_app).
- Set folder from os.path.dirname(exported\_file\_path(root, dt, dn)).
- If os.path.exists(folder).
  - Evaluate shutil.rmtree(folder).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L2953) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1372)

<a id="op-d41c5971cb2836"></a>
### Create folder

`operation_foundation_modules_export_file_business_behavior_create_folder`

**Inputs** module, dt, dn, create\_init, is\_custom\_module, record\_app = no value.

**Explicit results** folder.

**Local steps**

- Set root from export\_root(module, is\_custom\_module, record\_app).
- Set folder from os.path.dirname(exported\_file\_path(root, dt, dn)).
- Evaluate Platform.create\_folder(folder).
- If create\_init.
  - Evaluate create\_init\_py(root, expanded scrub\_dt\_dn(dt, dn)).
- Return folder.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L3213) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1369)

<a id="op-03f9d6e90be143"></a>
### Get custom module path

`operation_foundation_modules_export_file_business_behavior_get_custom_module_path`

**Inputs** module.

**Record and data access** read “Module Def” via get\_value.

**Explicit results** path.

**Explicit failure paths** validation helper — formatted text Package must be set for custom Module &lt;b&gt;{module}&lt;/b&gt; · validation helper — (“Invalid module path: ” + Path(path).as\_posix()).

**Local steps**

- Set package from Platform.db.get\_value(“Module Def”, module, “package”).
- If not package.
  - Call the validation error handler Platform.throw(formatted text Package must be set for custom Module &lt;b&gt;{module}&lt;/b&gt;).
- Set path from os.path.join(get\_package\_path(package), scrub(module)).
- If not Path(path).resolve().is\_relative\_to(Path(nested operand in the contract.get\_site\_path()).resolve()).
  - Call the validation error handler Platform.throw((“Invalid module path: ” + Path(path).as\_posix())).
- If not os.path.exists(path).
  - Evaluate os.makedirs(path).
- Return path.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L3459) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1377)

<a id="op-e462324bf4cadd"></a>
### Get package path

`operation_foundation_modules_export_file_business_behavior_get_package_path`

**Inputs** package.

**Record and data access** read “Package” via get\_value.

**Explicit results** path.

**Local steps**

- Set path from os.path.join(Platform.get\_site\_path(“packages”), Platform.db.get\_value(“Package”, package, “package\_name”)).
- If not os.path.exists(path).
  - Evaluate os.makedirs(path).
- Return path.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L3865) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1379)

<a id="op-2239941479a531"></a>
### Create init py

`operation_foundation_modules_export_file_business_behavior_create_initialize_business_behavior`

**Inputs** module\_path, dt, dn.

**Local steps**

- Bind local operation create\_if\_not\_exists for subsequent calls.
- Evaluate create\_if\_not\_exists(os.path.join(module\_path)).
- Evaluate create\_if\_not\_exists(os.path.join(module\_path, dt)).
- Evaluate create\_if\_not\_exists(os.path.join(module\_path, dt, dn)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L4051) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1370)

<a id="op-27fe36f135dbb9"></a>
### Create init py.create if not exists

`operation_foundation_modules_export_file_business_behavior_create_initialize_business_behavior_create_if_not_exists`

**Inputs** path.

**Local steps**

- Set initpy from os.path.join(path, “\_\_init\_\_.py”).
- If not os.path.exists(initpy).
  - Evaluate open(initpy, “w”).close().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L4349) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1371)

## Service · Gettext

<a id="op-fc8b4572ae8545"></a>
### Generate pot file

`operation_foundation_commands_gettext_business_behavior_generate_pot_file`

**Inputs** context, app = no value.

**Wrappers, in declaration order** click.command(“generate-pot-file”, help = “Translation: generate POT file”), click.option(“--app”, help = “Only generate for this app. eg: Platform”), pass\_context.

**Local steps**

- Bind dependencies generate\_pot.
- If not app.
  - Evaluate connect\_to\_site(context.sites at 0 when context.sites, otherwise no value).
    - Value choice on context.sites — true gives context.sites at 0, false gives no value.
- Evaluate generate\_pot(app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L5973) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L576)

<a id="op-db6bcb7a4ce152"></a>
### Compile translations

`operation_foundation_commands_gettext_business_behavior_compile_translations`

**Inputs** context, app = no value, locale = no value, force = false.

**Wrappers, in declaration order** click.command(“compile-po-to-mo”, help = “Translation: compile PO files to MO files”), click.option(“--app”, help = “Only compile for this app. eg: Platform”), click.option(“--force”, is\_flag = true, default = false, help = “Force compile even if there are no changes to PO files”), click.option(“--locale”, help = “Compile transaltions only for this locale. eg: de”), pass\_context.

**Local steps**

- Bind dependencies \_compile\_translations.
- If not app.
  - Evaluate connect\_to\_site(context.sites at 0 when context.sites, otherwise no value).
    - Value choice on context.sites — true gives context.sites at 0, false gives no value.
- Evaluate \_compile\_translations(app, locale, force = force).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L6187) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L573)

<a id="op-f75c7a70f291ee"></a>
### Csv to po

`operation_foundation_commands_gettext_business_behavior_comma_separated_values_to_purchase_order`

**Inputs** context, app = no value, locale = no value.

**Wrappers, in declaration order** click.command(“migrate-csv-to-po”, help = “Translation: migrate from CSV files (old) to PO files (new)”), click.option(“--app”, help = “Only migrate for this app. eg: Platform”), click.option(“--locale”, help = “Compile translations only for this locale. eg: de”), pass\_context.

**Local steps**

- Bind dependencies migrate.
- If not app.
  - Evaluate connect\_to\_site(context.sites at 0 when context.sites, otherwise no value).
    - Value choice on context.sites — true gives context.sites at 0, false gives no value.
- Evaluate migrate(app, locale).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L6525) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L572)

<a id="op-293668281227f8"></a>
### Update po files

`operation_foundation_commands_gettext_business_behavior_update_purchase_order_files`

**Inputs** context, app = no value, locale = no value.

**Wrappers, in declaration order** click.command(“update-po-files”, help = “Translation: sync PO files with POT file.\\nYou might want to run generate-pot-file first.”), click.option(“--app”, help = “Only update for this app. eg: Platform”), click.option(“--locale”, help = “Update PO files only for this locale. eg: de”), pass\_context.

**Local steps**

- Bind dependencies update\_po.
- If not app.
  - Evaluate connect\_to\_site(context.sites at 0 when context.sites, otherwise no value).
    - Value choice on context.sites — true gives context.sites at 0, false gives no value.
- Evaluate update\_po(app, locale = locale).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L6795) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L577)

<a id="op-930ba73012c64f"></a>
### Create po file

`operation_foundation_commands_gettext_business_behavior_create_purchase_order_file`

**Inputs** context, locale, app = no value.

**Wrappers, in declaration order** click.command(“create-po-file”, help = “Translation: create a new PO file for a locale”), click.argument(“locale”, nargs = 1), click.option(“--app”, help = “Only create for this app. eg: Platform”), pass\_context.

**Local steps**

- Bind dependencies new\_po.
- If not app.
  - Evaluate connect\_to\_site(context.sites at 0 when context.sites, otherwise no value).
    - Value choice on context.sites — true gives context.sites at 0, false gives no value.
- Evaluate new\_po(locale, app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L7071) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L575)

<a id="op-8799cbdb679414"></a>
### Connect to site

`operation_foundation_commands_gettext_business_behavior_connect_to_site`

**Inputs** site.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies connect.
- If not site.
  - Raise SiteNotSpecifiedError.
- Evaluate connect(site = site).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L7331) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L574)

## Service · Import file

<a id="op-ce97d7c06619a3"></a>
### Calculate hash

`operation_foundation_modules_import_file_business_behavior_calculate_hash`

**Inputs** path.

**Declared result** str.

**Explicit results** hash\_md5.hexdigest().

**Local steps**

- Set hash\_md5 from hashlib.md5(usedforsecurity = false).
- Within open(path, “rb”) bound as f.
  - For each chunk in iter(deferred anonymous expression, byte value).
    - Evaluate hash\_md5.update(chunk).
- Return hash\_md5.hexdigest().

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L4485) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1383)

<a id="op-759ba5444b0850"></a>
### Import files

`operation_foundation_modules_import_file_business_behavior_import_files`

**Inputs** module, dt = no value, dn = no value, force = false, pre\_process = no value, reset\_permissions = false.

**Explicit results** list of import\_file(m at 0, m at 1, m at 2, force = force, pre\_process = pre\_process, reset\_permissions = reset\_permissions) for m drawn from module · import\_file(module, dt, dn, force = force, pre\_process = pre\_process, reset\_permissions = reset\_permissions).

**Local steps**

- If isinstance(module, list).
  - Return list of import\_file(m at 0, m at 1, m at 2, force = force, pre\_process = pre\_process, reset\_permissions = reset\_permissions) for m drawn from module.
    - Draw m from module.
- Otherwise.
  - Return import\_file(module, dt, dn, force = force, pre\_process = pre\_process, reset\_permissions = reset\_permissions).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L4683) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1388)

<a id="op-8d03f6a9c4e546"></a>
### Import file

`operation_foundation_modules_import_file_business_behavior_import_file`

**Inputs** module, dt, dn, force = false, pre\_process = no value, reset\_permissions = false.

**Explicit results** import\_file\_by\_path(path, force, pre\_process = pre\_process, reset\_permissions = reset\_permissions).

**Local steps**

- Set path from get\_file\_path(module, dt, dn).
- Return import\_file\_by\_path(path, force, pre\_process = pre\_process, reset\_permissions = reset\_permissions).

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L4952) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1386)

<a id="op-5b0f586175a277"></a>
### Get file path

`operation_foundation_modules_import_file_business_behavior_get_file_path`

**Inputs** module, dt, dn.

**Explicit results** path.

**Local steps**

- Set tuple(dt, dn) from scrub\_dt\_dn(dt, dn).
- Set path from os.path.join(get\_module\_path(module), os.path.join(dt, dn, formatted text {dn}.json)).
- Return path.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L5110) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1385)

<a id="op-fc91294ae7e44a"></a>
### Import file by path

`operation_foundation_modules_import_file_business_behavior_import_file_by_path`

**Inputs** path, force = false, data\_import = false, pre\_process = no value, ignore\_version = no value, reset\_permissions = false.

**Declared result** bool.

**Record and data access** read doc at “doctype” via get\_value · read “Kanban Board” via get\_value.

**Explicit results** false · imported.

**Local steps**

- Attempt the following.
  - Set docs from read\_doc\_from\_file(path).
- On failure (OSError).
  - Evaluate print(formatted text {path} missing).
  - Return false.
- Set calculated\_hash from calculate\_hash(path).
- Set imported from false.
- If docs.
  - If not isinstance(docs, list).
    - Set docs from list(docs).
  - For each doc in docs.
    - Set db\_modified\_timestamp from Platform.db.get\_value(doc at “doctype”, doc at “name”, “modified”).
    - Set is\_db\_timestamp\_latest from (db\_modified\_timestamp and get\_datetime(doc.get(“modified”)) ≤ get\_datetime(db\_modified\_timestamp)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in db\_modified\_timestamp → get\_datetime(doc.get(“modified”)) ≤ get\_datetime(db\_modified\_timestamp).
    - If (not force and doc at “doctype” equals “Kanban Board” and db\_modified\_timestamp and Platform.db.get\_value(“Kanban Board”, doc at “name”, “is\_standard”) differs from “Yes”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not force → doc at “doctype” equals “Kanban Board” → db\_modified\_timestamp → Platform.db.get\_value(“Kanban Board”, doc at “name”, “is\_standard”) differs from “Yes”.
      - Evaluate print(formatted text Skipping {path}: a Kanban Board named {doc at “name”} already exists on this site).
      - Continue with the next iteration or loop test.
    - If (not force and db\_modified\_timestamp).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not force → db\_modified\_timestamp.
      - Set stored\_hash from no value.
      - If doc at “doctype” equals “DocType”.
        - Attempt the following.
          - Set stored\_hash from Platform.db.get\_value(doc at “doctype”, doc at “name”, “migration\_hash”).
        - On failure (Exception).
          - Take no action here.
      - If (stored\_hash and stored\_hash equals calculated\_hash).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in stored\_hash → stored\_hash equals calculated\_hash.
        - Continue with the next iteration or loop test.
      - If (is\_db\_timestamp\_latest and doc at “doctype” differs from “DocType”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_db\_timestamp\_latest → doc at “doctype” differs from “DocType”.
        - Continue with the next iteration or loop test.
    - Evaluate import\_doc(docdict = doc, data\_import = data\_import, pre\_process = pre\_process, ignore\_version = ignore\_version, …).
    - Set imported from true.
    - If doc at “doctype” equals “DocType”.
      - Set doctype\_table from DocType(“DocType”).
      - Evaluate nested operand in the contract(nested operand in the contract).set(doctype\_table.migration\_hash, calculated\_hash).where(doctype\_table.name equals doc at “name”).run().
    - Set new\_modified\_timestamp from doc.get(“modified”).
    - If (is\_db\_timestamp\_latest and doc at “doctype” equals “DocType”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_db\_timestamp\_latest → doc at “doctype” equals “DocType”.
      - Set new\_modified\_timestamp from now().
    - If new\_modified\_timestamp.
      - Evaluate update\_modified(new\_modified\_timestamp, doc).
- Return imported.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L23) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1387)

<a id="op-976e0f0f603d4f"></a>
### Read doc from file

`operation_foundation_modules_import_file_business_behavior_read_record_from_file`

**Inputs** path.

**Explicit results** doc.

**Explicit failure paths** propagate active failure · OSError(“{} missing”.format(path)).

**Local steps**

- Set doc from no value.
- If os.path.exists(path).
  - Within open(path, encoding = “utf-8”) bound as f.
    - Attempt the following.
      - Set doc from orjson.loads(f.read()).
    - On failure (ValueError).
      - Evaluate print(formatted text bad json: {path}).
      - Propagate the active failure.
- Otherwise.
  - Raise OSError(“{} missing”.format(path)).
- Return doc.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L6441) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1391)

<a id="op-e07938ddf48099"></a>
### Update modified

`operation_foundation_modules_import_file_business_behavior_update_modified`

**Inputs** original\_modified, doc.

**Local steps**

- If (doc at “doctype” equals doc at “name” and doc at “name” differs from “DocType”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc at “doctype” equals doc at “name” → doc at “name” differs from “DocType”.
  - Set singles\_table from DocType(“Singles”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract at nested operand in the contract equals “modified”).where(singles\_table. ….run().
- Otherwise.
  - Set doctype\_table from DocType(doc at “doctype”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(doctype\_table.modified, original\_modified).where(doctype\_table.name equals doc at “name”).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0294.json#L6708) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1393)

<a id="op-3499f65b45a0df"></a>
### Import doc

`operation_foundation_modules_import_file_business_behavior_import_record`

**Inputs** docdict, data\_import = false, pre\_process = no value, ignore\_version = no value, reset\_permissions = false, path = no value.

**Record and data access** resolve a document from docdict via get\_doc · read doc.doctype via exists.

**State and service calls** call insert on doc.

**Explicit results** doc.

**Local steps**

- Set Platform.flags.in\_import from true.
- Set docdict at “\_\_islocal” from 1.
- Set controller from get\_controller(docdict at “doctype”).
- If (controller and hasattr(controller, “prepare\_for\_import”) and callable(controller.prepare\_for\_import)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in controller → hasattr(controller, “prepare\_for\_import”) → callable(controller.prepare\_for\_import).
  - Evaluate controller.prepare\_for\_import(docdict).
- Set doc from Platform.get\_doc(docdict).
- Evaluate reset\_tree\_properties(doc).
- Evaluate load\_code\_properties(doc, path).
- Evaluate doc.run\_method(“before\_import”).
- Set doc.flags.ignore\_version from ignore\_version.
- If pre\_process.
  - Evaluate pre\_process(doc).
- If Platform.db.exists(doc.doctype, doc.name).
  - Evaluate delete\_old\_doc(doc, reset\_permissions).
- Set doc.flags.ignore\_links from true.
- If not data\_import.
  - Set doc.flags.ignore\_validate from true.
  - Set doc.flags.ignore\_permissions from true.
  - Set doc.flags.ignore\_mandatory from true.
- Evaluate doc.insert().
- Set Platform.flags.in\_import from false.
- Return doc.

**Values supplied outside this operation** selected callable from get\_controller(docdict at “doctype”), doc.run\_method(“before\_import”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1389)

<a id="op-ce75755d7eca31"></a>
### Load code properties

`operation_foundation_modules_import_file_business_behavior_load_code_properties`

**Inputs** doc, path.

**Local steps**

- If path.
  - If hasattr(doc, “get\_code\_fields”).
    - Set tuple(dirname, filename) from os.path.split(path).
    - For each tuple(key, extn) in doc.get\_code\_fields().items().
      - Set codefile from os.path.join(dirname, ((filename at slice no value to nested operand in the contract.rfind(“.”) + “.”) + extn)).
      - If os.path.exists(codefile).
        - Within open(codefile) bound as txtfile.
          - Evaluate doc.set(key, txtfile.read()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L610) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1390)

<a id="op-a1b454e2f0c222"></a>
### Delete old doc

`operation_foundation_modules_import_file_business_behavior_delete_old_record`

**Inputs** doc, reset\_permissions.

**Record and data access** resolve a document from doc.doctype via get\_doc.

**State and service calls** request delete\_doc for doc.doctype.

**Local steps**

- Set ignore from list().
- Set old\_doc from Platform.get\_doc(doc.doctype, doc.name).
- If doc.doctype belongs to ignore\_values.
  - For each key in (ignore\_values.get(doc.doctype) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_values.get(doc.doctype) → list().
    - Evaluate doc.set(key, old\_doc.get(key)).
- For each df in doc.meta.get\_table\_fields().
  - If (df.options belongs to ignore\_doctypes and not reset\_permissions).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.options belongs to ignore\_doctypes → not reset\_permissions.
    - Evaluate doc.set(df.fieldname, list()).
    - Evaluate ignore.append(df.options).
- Evaluate Platform.delete\_doc(doc.doctype, doc.name, force = 1, ignore\_doctypes = ignore, for\_reload = true).
- Set doc.flags.ignore\_children\_type from ignore.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L955) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1384)

<a id="op-62df4a9c2e4f69"></a>
### Reset tree properties

`operation_foundation_modules_import_file_business_behavior_reset_tree_properties`

**Inputs** doc.

**Local steps**

- If (getattr(doc.meta, “is\_tree”, no value) and any(list(doc.lft, doc.rgt))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(doc.meta, “is\_tree”, no value) → any(list(doc.lft, doc.rgt)).
  - Evaluate print(formatted text Ignoring values of ′lft′ and ′rgt′ for {doc.doctype} "{doc.name}").
  - Set doc.lft from no value.
  - Set doc.rgt from no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc.meta, “is\_tree”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L1382) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1392)
