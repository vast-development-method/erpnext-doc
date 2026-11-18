# Web content and issued documents · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Translate

<a id="op-f8ea73452399b6"></a>
### Get user lang

`operation_foundation_translate_business_behavior_get_user_language`

**Inputs** user = no value.

**Declared result** str.

**Record and data access** read “User” via get\_cached\_value.

**Explicit results** (Platform.get\_cached\_value(“User”, user, “language”) or Platform.get\_system\_settings(“language”) or Platform.local.lang or “en”).

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Return (Platform.get\_cached\_value(“User”, user, “language”) or Platform.get\_system\_settings(“language”) or Platform.local.lang or “en”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“User”, user, “language”) → Platform.get\_system\_settings(“language”) → Platform.local.lang → “en”.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, user, “language”), Platform.get\_system\_settings(“language”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0453.json#L6722) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1371)

<a id="op-e9625e05b4c7a9"></a>
### Get lang code

`operation_foundation_translate_business_behavior_get_language_code`

**Inputs** lang.

**Declared result** (str bitwise or no value).

**Record and data access** read “Language” via get\_value.

**Explicit results** (Platform.db.get\_value(“Language”, mapping(“name” → lang)) or Platform.db.get\_value(“Language”, mapping(“language\_name” → lang))).

**Local steps**

- Return (Platform.db.get\_value(“Language”, mapping(“name” → lang)) or Platform.db.get\_value(“Language”, mapping(“language\_name” → lang))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Language”, mapping(“name” → lang)) → Platform.db.get\_value(“Language”, mapping(“language\_name” → lang)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0453.json#L6890) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1349)

<a id="op-c37ff444250e00"></a>
### Set default language

`operation_foundation_translate_business_behavior_set_default_language`

**Inputs** lang.

**Local steps**

- If Platform.db.get\_default(“lang”) differs from lang.
  - Evaluate Platform.db.set\_default(“lang”, lang).
- Set Platform.local.lang from lang.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0453.json#L7044) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1380)

<a id="op-0988bca0dbc976"></a>
### Get lang dict

`operation_foundation_translate_business_behavior_get_language_mapping`

**Inputs** no declared parameters.

**Record and data access** read “Language” via get\_all.

**Explicit results** dict(Platform.get\_all(“Language”, fields = list(“language\_name”, “name”), order\_by = “creation”, as\_list = true)).

**Local steps**

- Return dict(Platform.get\_all(“Language”, fields = list(“language\_name”, “name”), order\_by = “creation”, as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0453.json#L7169) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1350)

<a id="op-37409ce5b9082d"></a>
### Get messages for boot

`operation_foundation_translate_business_behavior_get_messages_for_boot`

**Inputs** no declared parameters.

**Explicit results** get\_all\_translations(Platform.local.lang).

**Local steps**

- Return get\_all\_translations(Platform.local.lang).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0453.json#L7287) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1352)

<a id="op-735ff44d0bbbad"></a>
### Get all translations

`operation_foundation_translate_business_behavior_get_all_translations`

**Inputs** lang.

**Declared result** dict at tuple(str, str).

**Explicit results** mapping() · Platform.cache.hget(MERGED\_TRANSLATION\_KEY, lang, generator = \_merge\_translations).

**Local steps**

- If not lang.
  - Return mapping().
- Bind local operation \_merge\_translations for subsequent calls.
- Attempt the following.
  - Return Platform.cache.hget(MERGED\_TRANSLATION\_KEY, lang, generator = \_merge\_translations).
- On failure (Exception).
  - Evaluate Platform.logger().error(“Unable to load translations”, exc\_info = true).
  - Return mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1346)

<a id="op-27850c56738353"></a>
### Get all translations.merge translations

`operation_foundation_translate_business_behavior_get_all_translations_merge_translations`

**Inputs** no declared parameters.

**Explicit results** all\_translations.

**Local steps**

- Bind dependencies get\_translated\_countries.
- Set parent\_lang from get\_parent\_language(lang).
- Set all\_translations from get\_translations\_from\_apps(parent\_lang).copy() when parent\_lang, otherwise mapping().
  - Value choice on parent\_lang — true gives get\_translations\_from\_apps(parent\_lang).copy(), false gives mapping().
- Evaluate all\_translations.update(get\_translations\_from\_apps(lang)).
- Within suppress(Exception).
  - Evaluate all\_translations.update(get\_user\_translations(parent\_lang) when parent\_lang, otherwise mapping()).
    - Value choice on parent\_lang — true gives get\_user\_translations(parent\_lang), false gives mapping().
  - Evaluate all\_translations.update(get\_user\_translations(lang)).
  - Evaluate all\_translations.update(get\_translated\_countries()).
- Return all\_translations.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L473) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1347)

<a id="op-4d462171829d2d"></a>
### Get translations from apps

`operation_foundation_translate_business_behavior_get_translations_from_apps`

**Inputs** lang, apps = no value.

**Explicit results** parent\_translations · translations.

**Local steps**

- Set translations from mapping().
- Bind dependencies get\_translations\_from\_mo.
- For each app in (apps or Platform.get\_installed\_apps(\_ensure\_on\_bench = true)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in apps → Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
  - Evaluate translations.update((get\_translations\_from\_csv(lang, app) or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_translations\_from\_csv(lang, app) → mapping().
  - Evaluate translations.update((get\_translations\_from\_mo(lang, app) or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_translations\_from\_mo(lang, app) → mapping().
- If parent bound to get\_parent\_language(lang).
  - Set parent\_translations from get\_translations\_from\_apps(parent, apps).
  - Evaluate parent\_translations.update(translations).
  - Return parent\_translations.
- Return translations.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L766) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1367)

<a id="op-38b17140306f5d"></a>
### Get translations from csv

`operation_foundation_translate_business_behavior_get_translations_from_comma_separated_values`

**Inputs** lang, app.

**Explicit results** get\_translation\_dict\_from\_file(os.path.join(Platform.get\_app\_path(app, “translations”), (lang + “.csv”)), lang, app).

**Local steps**

- Return get\_translation\_dict\_from\_file(os.path.join(Platform.get\_app\_path(app, “translations”), (lang + “.csv”)), lang, app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L1075) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1368)

<a id="op-a23bf22b58f60f"></a>
### Get translation dict from file

`operation_foundation_translate_business_behavior_get_translation_mapping_from_file`

**Inputs** path, lang, app, throw = false.

**Declared result** dict at tuple(str, str).

**Explicit results** translation\_map.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set translation\_map from mapping().
- If os.path.exists(path).
  - Set csv\_content from read\_csv\_file(path).
  - For each item in csv\_content.
    - If len(item) belongs to list(2, 3).
      - Set item at 0 from item at 0.replace(“\\n”, whitespace '\\n').
      - Set item at 1 from item at 1.replace(“\\n”, whitespace '\\n').
    - If (len(item) equals 3 and item at 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(item) equals 3 → item at 2.
      - Set key from ((item at 0 + “:”) + item at 2).
      - Set translation\_map at key from strip(item at 1).
    - Otherwise.
      - If len(item) belongs to list(2, 3).
        - Set translation\_map at item at 0 from strip(item at 1).
      - Otherwise.
        - If item.
          - Set msg from formatted text Bad translation in '{app}' for language '{lang}': {cstr(item)}.
          - Evaluate Platform.log\_error(message = msg, title = “Error in translation file”).
          - If throw.
            - Call the validation error handler Platform.throw(msg, title = “Error in translation file”).
- Return translation\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L1195) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1366)

<a id="op-b384cfa45feee9"></a>
### Get user translations

`operation_foundation_translate_business_behavior_get_user_translations`

**Inputs** lang.

**Explicit results** Platform.cache.hget(USER\_TRANSLATION\_KEY, lang, generator = \_read\_from\_db).

**Local steps**

- Bind local operation \_read\_from\_db for subsequent calls.
- Return Platform.cache.hget(USER\_TRANSLATION\_KEY, lang, generator = \_read\_from\_db).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L1888) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1372)

<a id="op-85781613b297f0"></a>
### Get user translations.read from db

`operation_foundation_translate_business_behavior_get_user_translations_read_from_database`

**Inputs** no declared parameters.

**Record and data access** read “Translation” via get\_all.

**Explicit results** user\_translations.

**Local steps**

- Set user\_translations from mapping().
- Set translations from Platform.get\_all(“Translation”, fields = list(“source\_text”, “translated\_text”, “context”), filters = mapping(“language” → lang)).
- For each t in translations.
  - Set key from t.source\_text.
  - Set value from t.translated\_text.
  - If t.context.
    - Update key using + (“:” + t.context).
  - Set user\_translations at key from value.
- Return user\_translations.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L2197) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1373)

<a id="op-07745a2155cc0a"></a>
### Clear cache

`operation_foundation_translate_business_behavior_clear_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.cache.delete\_value(keys = list(“bootinfo”, USER\_TRANSLATION\_KEY, MERGED\_TRANSLATION\_KEY)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L50) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1339)

<a id="op-8027b46a5470b4"></a>
### Get messages for app

`operation_foundation_translate_business_behavior_get_messages_for_application`

**Inputs** app, deduplicate = true.

**Explicit results** messages.

**Explicit failure paths** Exception.

**Local steps**

- Set messages from list().
- Set modules from list of Platform.unscrub(m) for m drawn from Platform.local.app\_modules at app.
  - Draw m from Platform.local.app\_modules at app.
- If modules.
  - If isinstance(modules, str).
    - Set modules from list(modules).
  - Set filtered\_doctypes from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(modules)).select(“name”).run(pluck = true).
  - For each name in filtered\_doctypes.
    - Evaluate messages.extend(get\_messages\_from\_doctype(name)).
  - Set filtered\_pages from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(modules)).select(“name”, “title”).run().
  - For each tuple(name, title) in filtered\_pages.
    - Evaluate messages.append(tuple(no value, (title or name))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → name.
    - Evaluate messages.extend(get\_messages\_from\_page(name)).
  - Set report from DocType(“Report”).
  - Set doctype from DocType(“DocType”).
  - Set names from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract(nested operand in the c ….
  - For each name in names.
    - Evaluate messages.append(tuple(no value, name)).
    - Evaluate messages.extend(get\_messages\_from\_report(name)).
    - For each i in messages.
      - If not isinstance(i, tuple).
        - Raise Exception.
- Evaluate messages.extend(get\_messages\_from\_workflow(app\_name = app)).
- Evaluate messages.extend(get\_messages\_from\_custom\_fields(app\_name = app)).
- Evaluate messages.extend(get\_all\_messages\_from\_js\_files(app)).
- Evaluate messages.extend(get\_server\_messages(app)).
- Evaluate messages.extend(get\_messages\_from\_navbar()).
- If deduplicate.
  - Set messages from deduplicate\_messages(messages).
- Return messages.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L2802) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1351)

<a id="op-48ba795c4580b5"></a>
### Get messages from navbar

`operation_foundation_translate_business_behavior_get_messages_from_navbar`

**Inputs** no declared parameters.

**Record and data access** read “Navbar Item” via get\_all.

**Explicit results** list of tuple(“Navbar:”, label, “Label of a Navbar Item”) for label drawn from labels.

**Local steps**

- Set labels from Platform.get\_all(“Navbar Item”, filters = mapping(“item\_label” → tuple(“is”, “set”)), pluck = “item\_label”).
- Return list of tuple(“Navbar:”, label, “Label of a Navbar Item”) for label drawn from labels.
  - Draw label from labels.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L3965) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1356)

<a id="op-6400c208e85fa4"></a>
### Get messages from doctype

`operation_foundation_translate_business_behavior_get_messages_from_record_type`

**Inputs** name.

**Explicit results** messages.

**Local steps**

- Bind dependencies is\_translatable.
- Set messages from list().
- Set meta from Platform.get\_meta(name).
- Set messages from list(meta.name, meta.module).
- If meta.description.
  - Evaluate messages.append(meta.description).
- For each d in meta.get(“fields”).
  - Evaluate messages.extend(list(d.label, d.description)).
  - If (d.fieldtype equals “Select” and d.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype equals “Select” → d.options.
    - Set options from d.options.split(whitespace '\\n').
    - If (d.fieldname equals “icon” and name equals “Workflow State”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldname equals “icon” → name equals “Workflow State”.
      - Continue with the next iteration or loop test.
    - If “icon” does not belong to options at 0.
      - Evaluate messages.extend(options).
  - If (d.fieldtype equals “HTML” and d.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype equals “HTML” → d.options.
    - Evaluate messages.append(d.options).
- Evaluate messages.extend(generator of d.role for d drawn from meta.get(“permissions”) where d.role).
  - Draw d from meta.get(“permissions”), keep a combination only if (d.role).
- Set messages from list of message for message drawn from messages where message.
  - Draw message from messages, keep a combination only if (message).
- Set messages from list of tuple((“DocType: ” + name), message) for message drawn from messages where is\_translatable(message).
  - Draw message from messages, keep a combination only if (is\_translatable(message)).
- If not meta.custom.
  - Set doctype\_file\_path from Platform.get\_module\_path(meta.module, “doctype”, meta.name, meta.name).
  - Evaluate messages.extend(get\_messages\_from\_file((doctype\_file\_path + “.js”))).
  - Evaluate messages.extend(get\_messages\_from\_file((doctype\_file\_path + “\_list.js”))).
  - Evaluate messages.extend(get\_messages\_from\_file((doctype\_file\_path + “\_list.html”))).
  - Evaluate messages.extend(get\_messages\_from\_file((doctype\_file\_path + “\_calendar.js”))).
  - Evaluate messages.extend(get\_messages\_from\_file((doctype\_file\_path + “\_dashboard.html”))).
- Evaluate messages.extend(get\_messages\_from\_workflow(doctype = name)).
- Return messages.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0454.json#L4112) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1359)

<a id="op-71e7924081bae3"></a>
### Get messages from workflow

`operation_foundation_translate_business_behavior_get_messages_from_workflow`

**Inputs** doctype = no value, app\_name = no value.

**Record and data access** read “Workflow” via get\_all · read document\_state via get\_values · read “Workflow Transition” via get\_values.

**Explicit results** messages.

**Local steps**

- Require (doctype or app\_name) or report “doctype or app\_name should be provided”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → app\_name.
- Bind dependencies is\_translatable.
- Set workflows from list().
- If doctype.
  - Set workflows from Platform.get\_all(“Workflow”, filters = mapping(“document\_type” → doctype)).
- Otherwise.
  - Set fixtures from (Platform.get\_hooks(“fixtures”, app\_name = app\_name) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“fixtures”, app\_name = app\_name) → list().
  - For each fixture in fixtures.
    - If (isinstance(fixture, str) and fixture equals “Workflow”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fixture, str) → fixture equals “Workflow”.
      - Set workflows from Platform.get\_all(“Workflow”).
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Otherwise.
      - If (isinstance(fixture, dict) and fixture.get(“dt”, fixture.get(“doctype”)) equals “Workflow”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fixture, dict) → fixture.get(“dt”, fixture.get(“doctype”)) equals “Workflow”.
        - Evaluate workflows.extend(Platform.get\_all(“Workflow”, filters = fixture.get(“filters”))).
- Set messages from list().
- Set document\_state from DocType(“Workflow Document State”).
- For each w in workflows.
  - Set states from Platform.db.get\_values(document\_state, filters = document\_state.parent equals w at “name”, fieldname = “state”, distinct = true, as\_dict = true, …).
  - Evaluate messages.extend(list of tuple((“Workflow: ” + w at “name”), state at “state”) for state drawn from states where is\_translatable(state at “state”)).
    - Draw state from states, keep a combination only if (is\_translatable(state at “state”)).
  - Set states from Platform.db.get\_values(document\_state, filters = (document\_state.parent equals w at “name” bitwise and document\_state.message.isnotnull()), fieldname = “message”, distinct = true, order\_by = no value, …).
  - Evaluate messages.extend(list of tuple((“Workflow: ” + w at “name”), state at “message”) for state drawn from states where is\_translatable(state at “message”)).
    - Draw state from states, keep a combination only if (is\_translatable(state at “message”)).
  - Set actions from Platform.db.get\_values(“Workflow Transition”, filters = mapping(“parent” → w at “name”), fieldname = “action”, as\_dict = true, distinct = true, …).
  - Evaluate messages.extend(list of tuple((“Workflow: ” + w at “name”), action at “action”) for action drawn from actions where is\_translatable(action at “action”)).
    - Draw action from actions, keep a combination only if (is\_translatable(action at “action”)).
- Return messages.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“fixtures”, app\_name = app\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L51) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1361)

<a id="op-d6b1197cc1a7d7"></a>
### Get messages from custom fields

`operation_foundation_translate_business_behavior_get_messages_from_custom_fields`

**Inputs** app\_name.

**Record and data access** read “Custom Field” via get\_all.

**Explicit results** messages.

**Local steps**

- Bind dependencies is\_translatable.
- Set fixtures from (Platform.get\_hooks(“fixtures”, app\_name = app\_name) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“fixtures”, app\_name = app\_name) → list().
- Set custom\_fields from list().
- For each fixture in fixtures.
  - If (isinstance(fixture, str) and fixture equals “Custom Field”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fixture, str) → fixture equals “Custom Field”.
    - Set custom\_fields from Platform.get\_all(“Custom Field”, fields = list(“name”, “label”, “description”, “fieldtype”, …)).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Otherwise.
    - If (isinstance(fixture, dict) and fixture.get(“dt”, fixture.get(“doctype”)) equals “Custom Field”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fixture, dict) → fixture.get(“dt”, fixture.get(“doctype”)) equals “Custom Field”.
      - Evaluate custom\_fields.extend(Platform.get\_all(“Custom Field”, filters = fixture.get(“filters”), fields = list(“name”, “label”, “description”, “fieldtype”, …))).
- Set messages from list().
- For each cf in custom\_fields.
  - For each prop in tuple(“label”, “description”).
    - If (not cf.get(prop) or not is\_translatable(cf at prop)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cf.get(prop) → not is\_translatable(cf at prop).
      - Continue with the next iteration or loop test.
    - Evaluate messages.append(tuple(“Custom Field - {}: {}”.format(prop, cf at “name”), cf at prop)).
  - If (cf at “fieldtype” equals “Selection” and cf.get(“options”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cf at “fieldtype” equals “Selection” → cf.get(“options”).
    - Evaluate messages.extend(generator of tuple((“Custom Field - Description: ” + cf at “name”), option) for option drawn from cf at “options”.split(whitespace '\\n') where (option and “icon” does not belong to option a ….
      - Draw option from cf at “options”.split(whitespace '\\n'), keep a combination only if ((option and “icon” does not belong to option and is\_translatable(option))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in option → “icon” does not belong to option → is\_translatable(option).
- Return messages.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“fixtures”, app\_name = app\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1353)

<a id="op-e372bc0e36789d"></a>
### Get messages from page

`operation_foundation_translate_business_behavior_get_messages_from_page`

**Inputs** name.

**Explicit results** \_get\_messages\_from\_page\_or\_report(“Page”, name).

**Local steps**

- Return \_get\_messages\_from\_page\_or\_report(“Page”, name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L919) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1357)

<a id="op-d619d0521fccab"></a>
### Get messages from report

`operation_foundation_translate_business_behavior_get_messages_from_report`

**Inputs** name.

**Record and data access** resolve a document from “Report” via get\_doc · read “DocType” via get\_value.

**Explicit results** messages.

**Local steps**

- Bind dependencies is\_translatable.
- Set report from Platform.get\_doc(“Report”, name).
- Set messages from \_get\_messages\_from\_page\_or\_report(“Report”, name, Platform.db.get\_value(“DocType”, report.ref\_doctype, “module”)).
- If report.columns.
  - Set context from “Column of report '{}'”.format(report.name).
  - Evaluate messages.extend(list of tuple(no value, report\_column.label, context) for report\_column drawn from report.columns).
    - Draw report\_column from report.columns.
- If report.filters.
  - Evaluate messages.extend(list of tuple(no value, report\_filter.label) for report\_filter drawn from report.filters).
    - Draw report\_filter from report.filters.
- If report.query.
  - Evaluate messages.extend(list of tuple(no value, message) for message drawn from REPORT\_TRANSLATE\_PATTERN.findall(report.query) where is\_translatable(message)).
    - Draw message from REPORT\_TRANSLATE\_PATTERN.findall(report.query), keep a combination only if (is\_translatable(message)).
- Evaluate messages.append(tuple(no value, report.report\_name)).
- Return messages.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L980) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1360)

<a id="op-1381a2c8ae0177"></a>
### Get messages from page or report

`operation_foundation_translate_business_behavior_get_messages_from_page_or_report`

**Inputs** doctype, name, module = no value.

**Record and data access** read doctype via get\_value.

**Explicit results** messages.

**Local steps**

- If not module.
  - Set module from Platform.db.get\_value(doctype, name, “module”).
- Set doc\_path from Platform.get\_module\_path(module, doctype, name).
- Set messages from get\_messages\_from\_file(os.path.join(doc\_path, (Platform.scrub(name) + “.py”))).
- If os.path.exists(doc\_path).
  - For each filename in os.listdir(doc\_path).
    - If (filename.endswith(“.js”) or filename.endswith(“.html”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filename.endswith(“.js”) → filename.endswith(“.html”).
      - Update messages using + get\_messages\_from\_file(os.path.join(doc\_path, filename)).
- Return messages.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L1463) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1358)

<a id="op-b72469eb0119eb"></a>
### Get server messages

`operation_foundation_translate_business_behavior_get_server_messages`

**Inputs** app.

**Explicit results** messages.

**Local steps**

- Set messages from list().
- Set file\_extensions from tuple(“.py”, “.html”, “.js”, “.vue”).
- Set app\_walk from os.walk(Platform.get\_app\_path(app)).
- For each tuple(basepath, folders, files) in app\_walk.
  - Set folders at slice no value to no value from list of folder for folder drawn from folders where folder does not belong to set(“.git”, “\_\_pycache\_\_”).
    - Draw folder from folders, keep a combination only if (folder does not belong to set(“.git”, “\_\_pycache\_\_”)).
  - If “public/dist” belongs to basepath.
    - Continue with the next iteration or loop test.
  - For each f in files.
    - Set f from Platform.as\_unicode(f).
    - If f.endswith(file\_extensions).
      - Evaluate messages.extend(get\_messages\_from\_file(os.path.join(basepath, f))).
- Return messages.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L1853) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1364)

<a id="op-c4105d4f364cb7"></a>
### Get messages from include files

`operation_foundation_translate_business_behavior_get_messages_from_include_files`

**Inputs** app\_name = no value.

**Explicit results** messages.

**Local steps**

- Bind dependencies bundled\_asset.
- Set messages from list().
- Set app\_include\_js from (Platform.get\_hooks(“app\_include\_js”, app\_name = app\_name) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_include\_js”, app\_name = app\_name) → list().
- Set web\_include\_js from (Platform.get\_hooks(“web\_include\_js”, app\_name = app\_name) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“web\_include\_js”, app\_name = app\_name) → list().
- Set include\_js from (app\_include\_js + web\_include\_js).
- For each js\_path in include\_js.
  - Set file\_path from bundled\_asset(js\_path).
  - Set relative\_path from os.path.join(Platform.local.sites\_path, file\_path.lstrip(“/”)).
  - Set messages\_from\_file from get\_messages\_from\_file(relative\_path).
  - Evaluate messages.extend(messages\_from\_file).
- Return messages.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_include\_js”, app\_name = app\_name), Platform.get\_hooks(“web\_include\_js”, app\_name = app\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L2238) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1355)

<a id="op-aec270c7735169"></a>
### Get all messages from js files

`operation_foundation_translate_business_behavior_get_all_messages_from_client_script_files`

**Inputs** app\_name = no value.

**Explicit results** messages.

**Local steps**

- Set messages from list().
- For each app in list(app\_name) when app\_name, otherwise Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
  - Value choice on app\_name — true gives list(app\_name), false gives Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
  - If os.path.exists(Platform.get\_app\_path(app, “public”)).
    - For each tuple(basepath, folders, files) in os.walk(Platform.get\_app\_path(app, “public”)).
      - If “Platform/public/js/lib” belongs to basepath.
        - Continue with the next iteration or loop test.
      - For each fname in files.
        - If (fname.endswith(“.js”) or fname.endswith(“.html”) or fname.endswith(“.vue”)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in fname.endswith(“.js”) → fname.endswith(“.html”) → fname.endswith(“.vue”).
          - Evaluate messages.extend(get\_messages\_from\_file(os.path.join(basepath, fname))).
- Return messages.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0455.json#L2578) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1345)
