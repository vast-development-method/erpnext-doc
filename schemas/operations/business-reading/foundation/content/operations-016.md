# Web content and issued documents · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Translate

<a id="op-3a2eae4243a5bb"></a>
### Get messages from file

`operation_foundation_translate_business_behavior_get_messages_from_file`

**Inputs** path.

**Declared result** list at tuple at tuple(str, str, (str bitwise or no value), int).

**Explicit results** list() · list of tuple(os.path.relpath(path, bench\_path), message, context, line) for tuple(line, message, context) drawn from messages.

**Local steps**

- Bind dependencies extract\_messages\_from\_code.
- Evaluate Platform.flags.setdefault(“scanned\_files”, set()).
- If path belongs to Platform.flags.scanned\_files.
  - Return list().
- Evaluate Platform.flags.scanned\_files.add(path).
- Set bench\_path from get\_bench\_path().
- If not os.path.exists(path).
  - Return list().
- Within open(path) bound as sourcefile.
  - Attempt the following.
    - Set file\_contents from sourcefile.read().
  - On failure (Exception).
    - Evaluate print(formatted text Could not scan file for translation: {path}).
    - Return list().
  - Set messages from list().
  - If path.lower().endswith(“.py”).
    - Update messages using + extract\_messages\_from\_python\_code(file\_contents).
  - Otherwise.
    - Update messages using + extract\_messages\_from\_code(file\_contents).
  - If path.lower().endswith(“.js”).
    - Update messages using + extract\_messages\_from\_javascript\_code(file\_contents).
  - Return list of tuple(os.path.relpath(path, bench\_path), message, context, line) for tuple(line, message, context) drawn from messages.
    - Draw tuple(line, message, context) from messages.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L2979) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1354)

<a id="op-7edb68c5045fa9"></a>
### Extract messages from python code

`operation_foundation_translate_business_behavior_extract_messages_from_implementation_language_code`

**Inputs** code.

**Declared result** list at tuple at tuple(int, str, (str bitwise or no value)).

**Explicit results** messages.

**Local steps**

- Bind dependencies extract\_python.
- Set messages from list().
- For each message in extract\_python(io.BytesIO(code.encode()), keywords = list(“\_”, “\_lt”, “N\_”), comment\_tags = tuple(), options = mapping()).
  - Set tuple(lineno, \_func, args, \_comments) from message.
  - If (not args or not args at 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not args → not args at 0.
    - Continue with the next iteration or loop test.
  - Set source\_text from args at 0 when isinstance(args, tuple), otherwise args.
    - Value choice on isinstance(args, tuple) — true gives args at 0, false gives args.
  - Set context from args at 1 when len(args) equals 2, otherwise no value.
    - Value choice on len(args) equals 2 — true gives args at 1, false gives no value.
  - Evaluate messages.append(tuple(lineno, source\_text, context)).
- Return messages.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L3597) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1342)

<a id="op-c785afdee5f3f3"></a>
### Extract messages from javascript code

`operation_foundation_translate_business_behavior_extract_messages_from_client_language_code`

**Inputs** code.

**Declared result** list at tuple at tuple(int, str, (str bitwise or no value)).

**Explicit results** messages.

**Local steps**

- Set messages from list().
- Bind dependencies extract\_javascript.
- For each message in extract\_javascript(code).
  - Set tuple(lineno, \_func, args) from message.
  - If (not args or not args at 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not args → not args at 0.
    - Continue with the next iteration or loop test.
  - Set source\_text from args at 0 when isinstance(args, tuple), otherwise args.
    - Value choice on isinstance(args, tuple) — true gives args at 0, false gives args.
  - Set context from no value.
  - If (isinstance(args, tuple) and len(args) equals 3 and isinstance(args at 2, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(args, tuple) → len(args) equals 3 → isinstance(args at 2, str).
    - Set context from args at 2.
  - Evaluate messages.append(tuple(lineno, source\_text, context)).
- Return messages.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L4003) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1341)

<a id="op-68f25d80c22d58"></a>
### Read csv file

`operation_foundation_translate_business_behavior_read_comma_separated_values_file`

**Inputs** path.

**Explicit results** newdata.

**Local steps**

- Within open(path, encoding = “utf-8”, newline = empty text) bound as msgfile.
  - Set data from reader(msgfile).
  - Set newdata from list of list of val for val drawn from row for row drawn from data.
    - Draw row from data.
    - Draw val from row.
- Return newdata.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L4400) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1377)

<a id="op-2b04339a879e02"></a>
### Write csv file

`operation_foundation_translate_business_behavior_write_comma_separated_values_file`

**Inputs** path, app\_messages, lang\_dict.

**Local steps**

- Evaluate app\_messages.sort(key = deferred anonymous expression).
- Within open(path, “w”, newline = empty text) bound as msgfile.
  - Set w from writer(msgfile, lineterminator = whitespace '\\n').
  - For each app\_message in app\_messages.
    - Set context from no value.
    - If len(app\_message) equals 2.
      - Set tuple(path, message) from app\_message.
    - Otherwise.
      - If len(app\_message) equals 3.
        - Set tuple(path, message, \_lineno) from app\_message.
      - Otherwise.
        - If len(app\_message) equals 4.
          - Set tuple(path, message, context, \_lineno) from app\_message.
        - Otherwise.
          - Continue with the next iteration or loop test.
    - Set t from lang\_dict.get(message, empty text).
    - Set translated\_string from CSV\_STRIP\_WHITESPACE\_PATTERN.sub(“{\\g&lt;1&gt;}”, t).
    - If translated\_string.
      - Evaluate w.writerow(list(message, translated\_string, context)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L4561) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1384)

<a id="op-dfa97181f118b7"></a>
### Get untranslated

`operation_foundation_translate_business_behavior_get_untranslated`

**Inputs** lang, untranslated\_file, get\_all = false, app = “\_ALL\_APPS”.

**Explicit results** no value.

**Local steps**

- Evaluate clear\_cache().
- Set apps from Platform.get\_all\_apps(true).
- If app differs from “\_ALL\_APPS”.
  - If app does not belong to apps.
    - Evaluate print(formatted text Application {app} not found!).
    - Return no value.
  - Set apps from list(app).
- Set messages from list().
- Set untranslated from list().
- For each app\_name in apps.
  - Evaluate messages.extend(get\_messages\_for\_app(app\_name)).
- Set messages from deduplicate\_messages(messages).
- Bind local operation escape\_newlines for subsequent calls.
- If get\_all.
  - Evaluate print((str(len(messages)) + “ messages”)).
  - Within open(untranslated\_file, “wb”) bound as f.
    - For each m in messages.
      - Evaluate f.write((escape\_newlines(m at 1) + os.linesep).encode(“utf-8”)).
- Otherwise.
  - Set full\_dict from get\_all\_translations(lang).
  - For each m in messages.
    - If not full\_dict.get(m at 1).
      - Evaluate untranslated.append(m at 1).
  - If untranslated.
    - Evaluate print(((str(len(untranslated)) + “ missing translations of ”) + str(len(messages)))).
    - Within open(untranslated\_file, “wb”) bound as f.
      - For each m in untranslated.
        - Evaluate f.write((escape\_newlines(m) + os.linesep).encode(“utf-8”)).
  - Otherwise.
    - Evaluate print(“all translated!”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L5055) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1369)

<a id="op-6b035cf5556854"></a>
### Get untranslated.escape newlines

`operation_foundation_translate_business_behavior_get_untranslated_escape_newlines`

**Inputs** s.

**Explicit results** s.replace(“\\\\n”, “\|\|\|\|\|”).replace(“\\n”, “\|\|\|\|”).replace(whitespace '\\n', “\|\|\|”).

**Local steps**

- Return s.replace(“\\\\n”, “\|\|\|\|\|”).replace(“\\n”, “\|\|\|\|”).replace(whitespace '\\n', “\|\|\|”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L5964) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1370)

<a id="op-d423df90adf8e6"></a>
### Update translations

`operation_foundation_translate_business_behavior_update_translations`

**Inputs** lang, untranslated\_file, translated\_file, app = “\_ALL\_APPS”.

**Explicit results** no value.

**Local steps**

- Evaluate clear\_cache().
- Set full\_dict from get\_all\_translations(lang).
- Bind local operation restore\_newlines for subsequent calls.
- Set translation\_dict from mapping().
- For each tuple(key, value) in zip(Platform.get\_file\_items(untranslated\_file, ignore\_empty\_lines = false), Platform.get\_file\_items(translated\_file, ignore\_empty\_lines = false), strict = false).
  - Set translation\_dict at restore\_newlines(key) from restore\_newlines(value).
- Evaluate full\_dict.update(translation\_dict).
- Set apps from Platform.get\_all\_apps(true).
- If app differs from “\_ALL\_APPS”.
  - If app does not belong to apps.
    - Evaluate print(formatted text Application {app} not found!).
    - Return no value.
  - Set apps from list(app).
- For each app\_name in apps.
  - Evaluate write\_translations\_file(app\_name, lang, full\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L6061) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1381)

<a id="op-55165978d4dfa3"></a>
### Update translations.restore newlines

`operation_foundation_translate_business_behavior_update_translations_restore_newlines`

**Inputs** s.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract).replace(“\| \| \| \|”, “\\n”).replace(“\|\|\|”, whitespace '\\n').replace(“\| \| \|”, whitespace '\\n').

**Local steps**

- Return nested operand in the contract(nested operand in the contract, nested operand in the contract).replace(“\| \| \| \|”, “\\n”).replace(“\|\|\|”, whitespace '\\n').replace(“\| \| \|”, whitespace '\\n').

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L6665) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1383)

<a id="op-e55b2027d20860"></a>
### Import translations

`operation_foundation_translate_business_behavior_import_translations`

**Inputs** lang, path.

**Local steps**

- Evaluate clear\_cache().
- Set full\_dict from get\_all\_translations(lang).
- Evaluate full\_dict.update(get\_translation\_dict\_from\_file(path, lang, “import”)).
- For each app in Platform.get\_all\_apps(true).
  - Evaluate write\_translations\_file(app, lang, full\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L6819) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1374)

<a id="op-a2c8bcf4fc6c46"></a>
### Migrate translations

`operation_foundation_translate_business_behavior_migrate_translations`

**Inputs** source\_app, target\_app.

**Local steps**

- Set strings\_in\_source\_app from list of m at 1 for m drawn from Platform.translate.get\_messages\_for\_app(source\_app).
  - Draw m from Platform.translate.get\_messages\_for\_app(source\_app).
- Set strings\_in\_target\_app from list of m at 1 for m drawn from Platform.translate.get\_messages\_for\_app(target\_app).
  - Draw m from Platform.translate.get\_messages\_for\_app(target\_app).
- Set strings\_in\_target\_app\_but\_not\_in\_source\_app from list((set(strings\_in\_target\_app) − set(strings\_in\_source\_app))).
- Set languages from Platform.translate.get\_all\_languages().
- Set source\_app\_translations\_dir from Platform.get\_app\_path(source\_app, “translations”).
- Set target\_app\_translations\_dir from Platform.get\_app\_path(target\_app, “translations”).
- If not os.path.exists(target\_app\_translations\_dir).
  - Evaluate os.makedirs(target\_app\_translations\_dir).
- For each lang in languages.
  - Set source\_csv from os.path.join(source\_app\_translations\_dir, (lang + “.csv”)).
  - If not os.path.exists(source\_csv).
    - Continue with the next iteration or loop test.
  - Set target\_csv from os.path.join(target\_app\_translations\_dir, (lang + “.csv”)).
  - Set temp\_csv from os.path.join(source\_app\_translations\_dir, “\_temp.csv”).
  - Within open(source\_csv) bound as s, open(target\_csv, “a+”) bound as t, open(temp\_csv, “a+”) bound as temp.
    - Set source\_reader from reader(s, lineterminator = whitespace '\\n').
    - Set target\_writer from writer(t, lineterminator = whitespace '\\n').
    - Set temp\_writer from writer(temp, lineterminator = whitespace '\\n').
    - For each row in source\_reader.
      - If row at 0 belongs to strings\_in\_target\_app\_but\_not\_in\_source\_app.
        - Evaluate target\_writer.writerow(row).
      - Otherwise.
        - Evaluate temp\_writer.writerow(row).
  - If not os.path.getsize(target\_csv).
    - Evaluate os.remove(target\_csv).
  - Evaluate os.remove(source\_csv).
  - Evaluate os.rename(temp\_csv, source\_csv).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1375)

<a id="op-6d82e92148a7e3"></a>
### Rebuild all translation files

`operation_foundation_translate_business_behavior_rebuild_all_translation_files`

**Inputs** no declared parameters.

**Local steps**

- For each lang in get\_all\_languages().
  - For each app in Platform.get\_all\_apps().
    - Evaluate write\_translations\_file(app, lang).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L929) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1378)

<a id="op-c781f585f2bfa2"></a>
### Write translations file

`operation_foundation_translate_business_behavior_write_translations_file`

**Inputs** app, lang, full\_dict = no value, app\_messages = no value.

**Explicit results** no value.

**Local steps**

- If not app\_messages.
  - Set app\_messages from get\_messages\_for\_app(app).
- If not app\_messages.
  - Return no value.
- Set tpath from Platform.get\_app\_path(app, “translations”).
- Evaluate Platform.create\_folder(tpath).
- Evaluate write\_csv\_file(os.path.join(tpath, (lang + “.csv”)), app\_messages, (full\_dict or get\_all\_translations(lang))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in full\_dict → get\_all\_translations(lang).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L1028) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1385)

<a id="op-3aad8bc8cd5154"></a>
### Send translations

`operation_foundation_translate_business_behavior_send_translations`

**Inputs** translation\_dict.

**Local steps**

- If “\_\_messages” does not belong to Platform.local.response.
  - Set Platform.local.response at “\_\_messages” from mapping().
- Evaluate Platform.local.response at “\_\_messages”.update(translation\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L1289) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1379)

<a id="op-39802be0ca7955"></a>
### Deduplicate messages

`operation_foundation_translate_business_behavior_deduplicate_messages`

**Inputs** messages.

**Explicit results** list of next(g) for tuple(k, g) drawn from itertools.groupby(messages, op).

**Local steps**

- Set op from operator.itemgetter(1).
- Set messages from sorted(messages, key = op).
- Return list of next(g) for tuple(k, g) drawn from itertools.groupby(messages, op).
  - Draw tuple(k, g) from itertools.groupby(messages, op).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L1416) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1340)

<a id="op-216d7f88be4ab9"></a>
### Update translations for source

`operation_foundation_translate_business_behavior_update_translations_for_source`

**Inputs** source = no value, translation\_dict = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Translation” via get\_values · resolve a document from “Translation” via get\_doc.

**State and service calls** call save on doc · request delete\_doc for “Translation” · request new\_doc for “Translation”.

**Explicit results** no value · translation\_records.

**Local steps**

- If not (source and translation\_dict).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source → translation\_dict.
  - Return no value.
- Set translation\_dict from json.loads(translation\_dict).
- If is\_html(source).
  - Set source from strip\_html\_tags(source).
- Set translation\_records from Platform.db.get\_values(“Translation”, mapping(“source\_text” → source), list(“name”, “language”), as\_dict = 1).
- For each d in translation\_records.
  - If translation\_dict.get(d.language, no value).
    - Set doc from Platform.get\_doc(“Translation”, d.name).
    - Set doc.translated\_text from translation\_dict.get(d.language).
    - Evaluate doc.save().
    - Evaluate translation\_dict.pop(d.language).
  - Otherwise.
    - Evaluate Platform.delete\_doc(“Translation”, d.name).
- For each tuple(lang, translated\_text) in translation\_dict.items().
  - Set doc from Platform.new\_doc(“Translation”).
  - Set doc.language from lang.
  - Set doc.source\_text from source.
  - Set doc.translated\_text from translated\_text.
  - Evaluate doc.save().
- Return translation\_records.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L54) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1382)

<a id="op-fda9520a3be411"></a>
### Get all languages

`operation_foundation_translate_business_behavior_get_all_languages`

**Inputs** with\_language\_name = false.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Declared result** list.

**Record and data access** read “Language” via get\_all.

**Explicit results** Platform.cache.get\_value(“languages\_with\_name”, get\_all\_language\_with\_name) · languages.

**Local steps**

- Bind local operation get\_all\_language\_with\_name for subsequent calls.
- If with\_language\_name.
  - Return Platform.cache.get\_value(“languages\_with\_name”, get\_all\_language\_with\_name).
- Otherwise.
  - Set languages from Platform.client\_cache.get\_value(“languages”).
  - If not languages.
    - Set languages from Platform.get\_all(“Language”, filters = mapping(“enabled” → 1), pluck = “name”).
    - Evaluate Platform.client\_cache.set\_value(“languages”, languages).
  - Return languages.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L2236) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1343)

<a id="op-8ad0ba8f738c03"></a>
### Get all languages.get all language with name

`operation_foundation_translate_business_behavior_get_all_languages_get_all_language_with_name`

**Inputs** no declared parameters.

**Record and data access** read “Language” via get\_all.

**Explicit results** Platform.get\_all(“Language”, list(“language\_code”, “language\_name”), mapping(“enabled” → 1)).

**Local steps**

- Return Platform.get\_all(“Language”, list(“language\_code”, “language\_name”), mapping(“enabled” → 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L2594) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1344)

<a id="op-4ec7b631a3e371"></a>
### Get preferred language cookie

`operation_foundation_translate_business_behavior_get_preferred_language_cookie`

**Inputs** no declared parameters.

**Explicit results** Platform.request.cookies.get(“preferred\_language”).

**Local steps**

- Return Platform.request.cookies.get(“preferred\_language”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L2691) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1363)

<a id="op-31e1ef4bb78bda"></a>
### Get translated doctypes

`operation_foundation_translate_business_behavior_get_translated_record_types`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all · read “Property Setter” via get\_all.

**Explicit results** unique((dts + custom\_dts)).

**Local steps**

- Set dts from Platform.get\_all(“DocType”, mapping(“translated\_doctype” → 1), pluck = “name”).
- Set custom\_dts from Platform.get\_all(“Property Setter”, mapping(“property” → “translated\_doctype”, “value” → “1”), pluck = “doc\_type”).
- Return unique((dts + custom\_dts)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L52) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1365)

<a id="op-28e5650a174f57"></a>
### Print language

`operation_foundation_translate_business_behavior_print_language`

**Inputs** language.

**Wrappers, in declaration order** contextmanager.

**Explicit results** no value.

**Local steps**

- Set job from getattr(Platform.local, “job”, no value).
- If (job is distinct from no value and not job.lang\_resolved).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in job is distinct from no value → not job.lang\_resolved.
  - Evaluate Platform.set\_user\_lang(job.user).
  - Set job.lang\_resolved from true.
- If (not language or language equals Platform.local.lang).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not language → language equals Platform.local.lang.
  - yield no value.
  - Return no value.
- Set \_lang from Platform.local.lang.
- Set \_jenv\_restricted from getattr(Platform.local, “jenv\_restricted”, no value).
- Set \_jenv\_unrestricted from getattr(Platform.local, “jenv\_unrestricted”, no value).
- Set Platform.local.lang from language.
- Set Platform.local.jenv\_restricted from no value.
- Set Platform.local.jenv\_unrestricted from no value.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Set Platform.local.lang from \_lang.
  - Set Platform.local.jenv\_restricted from \_jenv\_restricted.
  - Set Platform.local.jenv\_unrestricted from \_jenv\_unrestricted.

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “job”, no value), getattr(Platform.local, “jenv\_restricted”, no value) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L53) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1376)

## Service · Utils

<a id="op-ac69692f27a061"></a>
### Extract messages from code

`operation_foundation_gettext_extractors_utils_business_behavior_extract_messages_from_code`

**Inputs** code.

**Explicit results** add\_line\_number(messages, code).

**Local steps**

- Bind dependencies TemplateError.
- Bind dependencies InvalidIncludePath, render\_include.
- Attempt the following.
  - Set code from Platform.as\_unicode(render\_include(code)).
- On failure (tuple(TemplateError, ImportError, InvalidIncludePath, OSError)) bound to e.
  - If (isinstance(e, InvalidIncludePath) and hasattr(Platform.local, “message\_log”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(e, InvalidIncludePath) → hasattr(Platform.local, “message\_log”).
    - Evaluate Platform.clear\_last\_message().
- On failure (RuntimeError).
  - Take no action here.
- Set messages from list().
- For each m in TRANSLATE\_PATTERN.finditer(code).
  - Set message from m.group(“message”).
  - Set context from (m.group(“py\_context”) or m.group(“js\_context”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in m.group(“py\_context”) → m.group(“js\_context”).
  - Set pos from m.start().
  - If is\_translatable(message).
    - Evaluate messages.append(list(pos, message, context)).
- Return add\_line\_number(messages, code).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L6212) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1607) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L372)

<a id="op-0fe485ee8589d8"></a>
### Is translatable

`operation_foundation_gettext_extractors_utils_business_behavior_is_translatable`

**Inputs** m.

**Explicit results** bool((re.search(“&#91;a-zA-Z&#93;”, m) and not m.startswith(“fa fa-”) and not m.endswith(“px”) and not m.startswith(“eval:”))).

**Local steps**

- Return bool((re.search(“&#91;a-zA-Z&#93;”, m) and not m.startswith(“fa fa-”) and not m.endswith(“px”) and not m.startswith(“eval:”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in re.search(“&#91;a-zA-Z&#93;”, m) → not m.startswith(“fa fa-”) → not m.endswith(“px”) → not m.startswith(“eval:”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L6677) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L375)

<a id="op-6a4e088d40360a"></a>
### Add line number

`operation_foundation_gettext_extractors_utils_business_behavior_add_line_number`

**Inputs** messages, code.

**Explicit results** ret.

**Local steps**

- Set ret from list().
- Set messages from sorted(messages, key = deferred anonymous expression).
- Set newlines from list of m.start() for m drawn from re.compile(“\\n”).finditer(code).
  - Draw m from re.compile(“\\n”).finditer(code).
- Set line from 1.
- Set newline\_i from 0.
- For each tuple(pos, message, context) in messages.
  - While (newline\_i &lt; len(newlines) and pos &gt; newlines at newline\_i).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in newline\_i &lt; len(newlines) → pos &gt; newlines at newline\_i.
    - Update line using + 1.
    - Update newline\_i using + 1.
  - Evaluate ret.append(list(line, message, context)).
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0241.json#L6824) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L371)
