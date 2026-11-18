# Forms, reports and navigation · operations 58

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Workspace · Setup wizard

<a id="op-65daba7da278c8"></a>
### Prettify args

`operation_foundation_desk_page_setup_wizard_business_behavior_prettify_arguments`

**Inputs** args.

**Explicit results** pretty\_args.

**Local steps**

- For each tuple(key, val) in args.items().
  - If (isinstance(val, str) and “data:image” belongs to val).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(val, str) → “data:image” belongs to val.
    - Set filename from val.split(“data:image”, 1) at 0.strip(“, ”).
    - Set size from round((((len(val) × 3) ÷ 4) ÷ 1048576.0), 2).
    - Set args at key from formatted text Image Attached: '{filename}' of size {size} MB.
- Set pretty\_args from list().
- Evaluate pretty\_args.extend(generator of formatted text {key} = {args at key} for key drawn from sorted(args)).
  - Draw key from sorted(args).
- Return pretty\_args.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L4114) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L357)

<a id="op-20e69393e7739a"></a>
### Email setup wizard exception

`operation_foundation_desk_page_setup_wizard_business_behavior_email_setup_wizard_exception`

**Inputs** traceback, args.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- If not Platform.conf.setup\_wizard\_exception\_email.
  - Return no value.
- Set pretty\_args from prettify\_args(args).
- Set message from multiline text in the contract.format(site = Platform.local.site, traceback = traceback, args = whitespace '\\n'.join(pretty\_args), user = Platform.session.user, …).
  - Value choice on Platform.request — true gives Platform.request.headers, false gives “&#91;no request&#93;”.
- Evaluate Platform.sendmail(recipients = Platform.conf.setup\_wizard\_exception\_email, sender = Platform.session.user, subject = formatted text Setup failed: {Platform.local.site}, message = message, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = Platform.conf.setup\_wizard\_exception\_email, sender = Platform.session.user, subject = formatted text Setup failed: {Platform.local.site}, message = message, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L4511) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L339)

<a id="op-45f6db1280bdd7"></a>
### Log setup wizard exception

`operation_foundation_desk_page_setup_wizard_business_behavior_log_setup_wizard_exception`

**Inputs** traceback, args.

**Local steps**

- Within open(“../logs/setup-wizard.log”, “w+”) bound as setup\_log.
  - Evaluate setup\_log.write(traceback).
  - Evaluate setup\_log.write(json.dumps(args)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L4834) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L353)

<a id="op-e6d5f84aab942e"></a>
### Get language code

`operation_foundation_desk_page_setup_wizard_business_behavior_get_language_code`

**Inputs** lang.

**Record and data access** read “Language” via get\_value.

**Explicit results** Platform.db.get\_value(“Language”, mapping(“language\_name” → lang)).

**Local steps**

- Return Platform.db.get\_value(“Language”, mapping(“language\_name” → lang)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L4967) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L343)

<a id="op-4355f3027d7265"></a>
### Enable twofactor all roles

`operation_foundation_desk_page_setup_wizard_business_behavior_enable_twofactor_all_roles`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L5051) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L341)

<a id="op-09964bdaf062e7"></a>
### Make records

`operation_foundation_desk_page_setup_wizard_business_behavior_make_records`

**Inputs** records, debug = false.

**State and service calls** request new\_doc for doctype · savepoint savepoint · call insert on doc · rollback.

**Local steps**

- Bind dependencies \_dict.
- Bind dependencies scrub.
- If debug.
  - Evaluate print(“make\_records: in DEBUG mode”).
- For each record in records.
  - Set doctype from record.get(“doctype”).
  - Set condition from record.get(“\_\_condition”).
  - If (condition and not condition()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in condition → not condition().
    - Continue with the next iteration or loop test.
  - Set doc from Platform.new\_doc(doctype).
  - Evaluate doc.update(record).
  - Set parent\_link\_field from (“parent\_” + scrub(doc.doctype)).
  - If (doc.meta.get\_field(parent\_link\_field) and not doc.get(parent\_link\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.get\_field(parent\_link\_field) → not doc.get(parent\_link\_field).
    - Set doc.flags.ignore\_mandatory from true.
  - Set savepoint from “setup\_fixtures\_creation”.
  - Attempt the following.
    - Evaluate Platform.db.savepoint(savepoint).
    - Evaluate doc.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).
  - On failure (Exception) bound to e.
    - Evaluate Platform.clear\_last\_message().
    - Evaluate Platform.db.rollback(save\_point = savepoint).
    - Set exception from record.get(“\_\_exception”).
    - If exception.
      - Set config from \_dict(exception).
      - If isinstance(e, config.exception).
        - Evaluate config.handler().
      - Otherwise.
        - Evaluate show\_document\_insert\_error().
    - Otherwise.
      - Evaluate show\_document\_insert\_error().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L5176) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L355)

<a id="op-6a3201592171ac"></a>
### Show document insert error

`operation_foundation_desk_page_setup_wizard_business_behavior_show_document_insert_error`

**Inputs** no declared parameters.

**Local steps**

- Evaluate print(“Document Insert Error”).
- Evaluate print(Platform.get\_traceback()).
- Evaluate Platform.log\_error(“Exception during Setup”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L5841) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L365)

## Record · Sidebar

[Record definition](../../../../data/record-types/sidebar.json)

<a id="op-28d60050e056a2"></a>
### Apps with old fixtures

`operation_foundation_desk_record_definitions_sidebar_convert_fixtures_business_behavior_apps_with_old_fixtures`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, int).

**Explicit results** counts.

**Local steps**

- Set counts from mapping().
- For each app in Platform.get\_installed\_apps().
  - Set files from list of path for path drawn from get\_app\_level\_files(OLD\_FIXTURE\_FOLDER, app) where path.endswith(“.json”).
    - Draw path from get\_app\_level\_files(OLD\_FIXTURE\_FOLDER, app), keep a combination only if (path.endswith(“.json”)).
  - If files.
    - Set counts at app from len(files).
- Return counts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0180.json#L7638) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1048)

<a id="op-e5a0222bd75961"></a>
### Read fixtures

`operation_foundation_desk_record_definitions_sidebar_convert_fixtures_business_behavior_read_fixtures`

**Inputs** app.

**Declared result** list at Platform.\_dict.

**Explicit results** sources.

**Local steps**

- Set sources from list().
- For each path in sorted(get\_app\_level\_files(OLD\_FIXTURE\_FOLDER, app)).
  - If not path.endswith(“.json”).
    - Continue with the next iteration or loop test.
  - Within open(path) bound as f.
    - Set fixture from Platform.parse\_json(f.read()).
  - If isinstance(fixture, list).
    - Set fixture from fixture at 0 when fixture, otherwise no value.
      - Value choice on fixture — true gives fixture at 0, false gives no value.
  - If (not fixture or fixture.get(“for\_user”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fixture → fixture.get(“for\_user”).
    - Continue with the next iteration or loop test.
  - Set rows from list of Platform.\_dict(row) for row drawn from (fixture.get(“items”) or list()).
    - Draw row from (fixture.get(“items”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fixture.get(“items”) → list().
  - If not rows.
    - Continue with the next iteration or loop test.
  - For each row in rows.
    - Evaluate options\_as\_filters(row).
  - Evaluate sources.append(Platform.\_dict(mapping(“name” → (fixture.get(“name”) or fixture.get(“title”)), “title” → fixture.get(“title”), “icon” → fixture.get(“header\_icon”), “module” → fixture.get(“module”), …))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fixture.get(“name”) → fixture.get(“title”).
- Return sources.

**Boundaries to resolve** callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L34) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1051)

<a id="op-4be9fa112ffa86"></a>
### Convert app

`operation_foundation_desk_record_definitions_sidebar_convert_fixtures_business_behavior_convert_application`

**Inputs** app, dry\_run = false.

**Declared result** list at dict.

**Explicit results** results.

**Local steps**

- Set by\_module from mapping().
- Set unresolved from list().
- For each source in read\_fixtures(app).
  - Set module from (source.module or majority\_module\_of(source.rows)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.module → majority\_module\_of(source.rows).
  - If not module.
    - Evaluate unresolved.append(source.path).
    - Continue with the next iteration or loop test.
  - Evaluate by\_module.setdefault(module, list()).append(source).
- Set results from list of mapping(“module” → no value, “path” → path, “state” → “no module”) for path drawn from unresolved.
  - Draw path from unresolved.
- For each module in sorted(by\_module).
  - Set plan from build\_sidebar(module, by\_module at module).
  - Attempt the following.
    - Set path from export\_path(module, plan at “title”).
  - On failure (tuple(Platform.DoesNotExistError, ImportError)).
    - Evaluate Platform.clear\_last\_message().
    - Evaluate results.append(mapping(“module” → module, “path” → no value, “state” → “no folder”)).
    - Continue with the next iteration or loop test.
  - Set existing from next(generator of p for p drawn from tuple(path, export\_path(module)) where os.path.exists(p), no value).
    - Draw p from tuple(path, export\_path(module)), keep a combination only if (os.path.exists(p)).
  - If existing.
    - Evaluate results.append(mapping(“module” → module, “path” → existing, “state” → “already converted”)).
    - Continue with the next iteration or loop test.
  - Evaluate results.append(mapping(“module” → module, “path” → path, “state” → “converted”, “sources” → len(by\_module at module), …)).
  - If not dry\_run.
    - Evaluate write\_export(path, module, plan, app).
- Return results.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L698) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1049)

<a id="op-9157c90f11e58c"></a>
### Export path

`operation_foundation_desk_record_definitions_sidebar_convert_fixtures_business_behavior_export_path`

**Inputs** module, title = no value.

**Declared result** str.

**Explicit results** os.path.join(Platform.get\_module\_path(module), “sidebar”, scrubbed, formatted text {scrubbed}.json).

**Local steps**

- Set scrubbed from Platform.scrub((title or module)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → module.
- Return os.path.join(Platform.get\_module\_path(module), “sidebar”, scrubbed, formatted text {scrubbed}.json).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L1640) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1050)

<a id="op-c32905c66d7c11"></a>
### Write export

`operation_foundation_desk_record_definitions_sidebar_convert_fixtures_business_behavior_write_export`

**Inputs** path, module, plan, app.

**Declared result** no value.

**Local steps**

- Evaluate os.makedirs(os.path.dirname(path), exist\_ok = true).
- Set doc from mapping(“doctype” → “Sidebar”, “name” → plan at “title”, “module” → module, “title” → plan at “title”, …).
  - Draw tuple(idx, item) from enumerate(plan at “items”, start = 1).
  - Draw field from SIDEBAR\_ITEM\_FIELDS, keep a combination only if (item.get(field) is distinct from no value).
- Within open(path, “w”) bound as f.
  - Evaluate f.write((json.dumps(doc, indent = 1, sort\_keys = true) + whitespace '\\n')).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L1819) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1052)

<a id="op-b5d8bb24f573ef"></a>
### Shell slug

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shell_slug`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** name.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L744)

<a id="op-19b1399385eaec"></a>
### Unroutable characters

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_unroutable_characters`

**Inputs** title.

**Declared result** list at str.

**Explicit results** sorted(set of character for character drawn from UNROUTABLE\_IN\_A\_TITLE where character belongs to (title or empty text)).

**Local steps**

- Return sorted(set of character for character drawn from UNROUTABLE\_IN\_A\_TITLE where character belongs to (title or empty text)).
  - Draw character from UNROUTABLE\_IN\_A\_TITLE, keep a combination only if (character belongs to (title or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L755)

<a id="op-6f06949567db50"></a>
### Shell holding slug

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shell_holding_slug`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** title, name, module.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L743)

<a id="op-c944b851ece070"></a>
### Routable title

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_routable_title`

**Inputs** title, module, name = no value.

**Declared result** str.

**Explicit results** next(generator of candidate for candidate drawn from candidates where (candidate and not shell\_holding\_slug(candidate, name = name, module = module))).

**Local steps**

- Set cleaned from one space.join(re.sub(formatted text &#91;{nested operand in the contract.escape(UNROUTABLE\_IN\_A\_TITLE)}&#93;, one space, (title or empty text)).split()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → empty text.
- Set base from one space.join(re.sub(formatted text &#91;{nested operand in the contract.escape(UNROUTABLE\_IN\_A\_TITLE)}&#93;, one space, module).split()).
- Set candidates from chain(tuple(cleaned, base), generator of formatted text {base} {n} for n drawn from count(2)).
  - Draw n from count(2).
- Return next(generator of candidate for candidate drawn from candidates where (candidate and not shell\_holding\_slug(candidate, name = name, module = module))).
  - Draw candidate from candidates, keep a combination only if ((candidate and not shell\_holding\_slug(candidate, name = name, module = module))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in candidate → not shell\_holding\_slug(candidate, name = name, module = module).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L742)

<a id="op-c364586e19af3b"></a>
### Sidebar.before naming

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_before_naming`

**Inputs** self.

**Local steps**

- Evaluate self.set\_default\_title().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default title](operations-058.md#op-cbcbf925bb5e6b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L2442) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1030)

<a id="op-7133b815413277"></a>
### Sidebar.validate

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_app\_content().
- Evaluate self.set\_default\_title().
- Evaluate self.validate\_title\_is\_its\_own().
- Evaluate self.validate\_title\_is\_routable().
- Evaluate self.validate\_title\_has\_its\_own\_url().
- Evaluate self.validate\_standard().
- Evaluate self.validate\_item\_routes().
- Evaluate self.clear\_stored\_keys().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate app content](operations-059.md#op-e0ac2515bac919), [set default title](operations-058.md#op-cbcbf925bb5e6b), [validate title is its own](operations-058.md#op-580ffc0f5871dd), [validate title is routable](operations-058.md#op-f218ab6e916f1e), [validate title has its own url](operations-058.md#op-3523a3a86f8c7f), [validate standard](operations-059.md#op-5fc5c1f7f68123), [validate item routes](operations-059.md#op-cbfbf5f7a542c2), [clear stored keys](operations-059.md#op-b09da82ad70cca).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L33) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1042)

<a id="op-b539ac0b6ee8c6"></a>
### Sidebar.before save

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.rename\_to\_title().

If control reaches the end, it returns no value.

**Methods declared on this owner** [rename to title](operations-058.md#op-42d5c780b9e555).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L2624) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1031)

<a id="op-cbcbf925bb5e6b"></a>
### Sidebar.set default title

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_set_default_title`

**Inputs** self.

**Local steps**

- If not self.title.
  - Set self.title from self.module.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L2675) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1041)

<a id="op-580ffc0f5871dd"></a>
### Sidebar.validate title is its own

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_validate_title_is_its_own`

**Inputs** self.

**Record and data access** read “Module Def” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is another module's name, and a sidebar's title is what the desk calls it by.”.format(Platform.bold(self.title)).

**Local steps**

- If self.title equals self.module.
  - Return no value.
- If Platform.db.exists(“Module Def”, self.title, cache = true).
  - Call the validation error handler Platform.throw(translated “{0} is another module's name, and a sidebar's title is what the desk calls it by.”.format(Platform.bold(self.title)), title = translated “Pick another title”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L2744) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1045)

<a id="op-f218ab6e916f1e"></a>
### Sidebar.validate title is routable

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_sidebar_validate_title_is_routable`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A sidebar's name is part of its desk URL, so it cannot contain {0}.”.format(Platform.bold(one space.join(bad))).

**Local steps**

- Set bad from unroutable\_characters(self.title).
- If not bad.
  - Return no value.
- Call the validation error handler Platform.throw(translated “A sidebar's name is part of its desk URL, so it cannot contain {0}.”.format(Platform.bold(one space.join(bad))), title = translated “Pick another title”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L754)

<a id="op-3523a3a86f8c7f"></a>
### Sidebar.validate title has its own url

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_sidebar_validate_title_has_its_own_url`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} already answers to the URL {1}, and two shells cannot share one.”.format(Platform.bold(clash), Platform.bold(formatted text /desk/{shell\_slug(self.title)})).

**Local steps**

- Set clash from shell\_holding\_slug(self.title, name = self.name, module = self.module).
- If not clash.
  - Return no value.
- Call the validation error handler Platform.throw(translated “{0} already answers to the URL {1}, and two shells cannot share one.”.format(Platform.bold(clash), Platform.bold(formatted text /desk/{shell\_slug(self.title)})), title = translat ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L753)

<a id="op-42d5c780b9e555"></a>
### Sidebar.rename to title

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_rename_to_title`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_import or self.is\_new() or not self.title or self.title equals self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → self.is\_new() → not self.title → self.title equals self.name.
  - Return no value.
- Evaluate rename\_doc(self.doctype, self.name, self.title, ignore\_permissions = true, rebuild\_search = false).
- Set self.name from self.title.
- Evaluate self.set\_parent\_in\_children().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L2966) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1040)
