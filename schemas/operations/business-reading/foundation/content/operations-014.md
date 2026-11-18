# Web content and issued documents · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Translate

<a id="op-2eca4eda9e8051"></a>
### Get po dir

`operation_foundation_gettext_translate_business_behavior_get_purchase_order_directory`

**Inputs** app.

**Declared result** Path.

**Explicit results** (Path(Platform.get\_app\_path(app)) ÷ PO\_DIR).

**Local steps**

- Return (Path(Platform.get\_app\_path(app)) ÷ PO\_DIR).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L6520) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L401)

<a id="op-11614cf36d404f"></a>
### Get locale dir

`operation_foundation_gettext_translate_business_behavior_get_locale_directory`

**Inputs** no declared parameters.

**Declared result** Path.

**Explicit results** (((Path(get\_bench\_path()) ÷ “sites”) ÷ “assets”) ÷ “locale”).

**Local steps**

- Return (((Path(get\_bench\_path()) ÷ “sites”) ÷ “assets”) ÷ “locale”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L6601) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L396)

<a id="op-b2e12fae7de8a2"></a>
### Get locales

`operation_foundation_gettext_translate_business_behavior_get_locales`

**Inputs** app.

**Declared result** list at str.

**Explicit results** list() · list of locale.stem for locale drawn from po\_dir.iterdir() where locale.suffix equals “.po”.

**Local steps**

- Set po\_dir from get\_po\_dir(app).
- If not po\_dir.exists().
  - Return list().
- Return list of locale.stem for locale drawn from po\_dir.iterdir() where locale.suffix equals “.po”.
  - Draw locale from po\_dir.iterdir(), keep a combination only if (locale.suffix equals “.po”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L6684) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L397)

<a id="op-21db256cce8431"></a>
### Get po path

`operation_foundation_gettext_translate_business_behavior_get_purchase_order_path`

**Inputs** app, locale = no value.

**Declared result** Path.

**Explicit results** (get\_po\_dir(app) ÷ formatted text {locale}.po).

**Local steps**

- Return (get\_po\_dir(app) ÷ formatted text {locale}.po).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L6853) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L402)

<a id="op-873684e1a56081"></a>
### Get mo path

`operation_foundation_gettext_translate_business_behavior_get_mo_path`

**Inputs** app, locale = no value.

**Declared result** Path.

**Explicit results** (((get\_locale\_dir() ÷ locale) ÷ “LC\_MESSAGES”) ÷ formatted text {app}.mo).

**Local steps**

- Return (((get\_locale\_dir() ÷ locale) ÷ “LC\_MESSAGES”) ÷ formatted text {app}.mo).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L6959) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L399)

<a id="op-54abfc7f0b3b5e"></a>
### Get pot path

`operation_foundation_gettext_translate_business_behavior_get_pot_path`

**Inputs** app.

**Declared result** Path.

**Explicit results** (get\_po\_dir(app) ÷ POT\_FILE).

**Local steps**

- Return (get\_po\_dir(app) ÷ POT\_FILE).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L7076) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L400)

<a id="op-7c98de7e69f2b3"></a>
### Get catalog

`operation_foundation_gettext_translate_business_behavior_get_catalog`

**Inputs** app, locale = no value.

**Declared result** Catalog.

**Explicit results** new\_catalog(app, locale) · read\_po(f).

**Local steps**

- Set po\_path from get\_po\_path(app, locale) when locale, otherwise get\_pot\_path(app).
  - Value choice on locale — true gives get\_po\_path(app, locale), false gives get\_pot\_path(app).
- If not po\_path.exists().
  - Return new\_catalog(app, locale).
- Within open(po\_path, “rb”) bound as f.
  - Return read\_po(f).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L7143) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L392)

<a id="op-b0a66e01f6dd4c"></a>
### Write catalog

`operation_foundation_gettext_translate_business_behavior_write_catalog`

**Inputs** app, catalog, locale = no value.

**Declared result** Path.

**Explicit results** po\_path.

**Local steps**

- Set po\_path from get\_po\_path(app, locale) when locale, otherwise get\_pot\_path(app).
  - Value choice on locale — true gives get\_po\_path(app, locale), false gives get\_pot\_path(app).
- If not po\_path.parent.exists().
  - Evaluate po\_path.parent.mkdir(parents = true).
- Within open(po\_path, “wb”) bound as f.
  - Evaluate write\_po(f, catalog, sort\_output = true, ignore\_obsolete = true, width = no value).
- Return po\_path.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L7364) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L410)

<a id="op-ff7012a636ddcc"></a>
### Write binary

`operation_foundation_gettext_translate_business_behavior_write_binary`

**Inputs** app, catalog, locale.

**Declared result** Path.

**Explicit results** mo\_path.

**Local steps**

- Set mo\_path from get\_mo\_path(app, locale).
- If not mo\_path.parent.exists().
  - Evaluate mo\_path.parent.mkdir(parents = true).
- Within open(mo\_path, “wb”) bound as mo\_file.
  - Evaluate write\_mo(mo\_file, catalog).
- Return mo\_path.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0242.json#L7650) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L409)

<a id="op-ab05fdaffcc269"></a>
### Get method map

`operation_foundation_gettext_translate_business_behavior_get_method_map`

**Inputs** app.

**Explicit results** list of tuple(row at 0, row at 1) for row drawn from reader · list().

**Local steps**

- Set file\_path from (Path(Platform.get\_app\_path(app)).parent ÷ “babel\_extractors.csv”).
- If file\_path.exists().
  - Within open(file\_path) bound as f.
    - Set reader from csv.reader(f).
    - Return list of tuple(row at 0, row at 1) for row drawn from reader.
      - Draw row from reader.
- Return list().

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L398)

<a id="op-f05e4d8a9a4030"></a>
### Generate pot

`operation_foundation_gettext_translate_business_behavior_generate_pot`

**Inputs** target\_app = no value.

**Local steps**

- Set is\_gitignored from get\_is\_gitignored\_function\_for\_app(target\_app).
- Bind local operation directory\_filter for subsequent calls.
- Set apps from list(target\_app) when target\_app, otherwise Platform.get\_all\_apps(true).
  - Value choice on target\_app — true gives list(target\_app), false gives Platform.get\_all\_apps(true).
- Set default\_method\_map from get\_method\_map(“Platform”).
- For each app in apps.
  - Set app\_path from Platform.get\_pymodule\_path(app, “..”).
  - Set catalog from new\_catalog(app).
  - Set ignored\_strings from \_get\_ignored\_strings(app).
  - Set method\_map from list() when app equals “Platform”, otherwise get\_method\_map(app).
    - Value choice on app equals “Platform” — true gives list(), false gives get\_method\_map(app).
  - Evaluate method\_map.extend(default\_method\_map).
  - For each tuple(filename, lineno, message, comments, …) in extract\_from\_dir(app\_path, method\_map, directory\_filter = directory\_filter, keywords = PYTHON\_KEYWORDS).
    - If not message.
      - Continue with the next iteration or loop test.
    - If tuple(message, context) belongs to ignored\_strings.
      - Continue with the next iteration or loop test.
    - Evaluate catalog.add(message, locations = list(tuple(filename, lineno)), auto\_comments = comments, context = context).
  - Set pot\_path from write\_catalog(app, catalog).
  - Evaluate print(formatted text POT file created at {pot\_path}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L232) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L390)

<a id="op-6099132b707b53"></a>
### Generate pot.directory filter

`operation_foundation_gettext_translate_business_behavior_generate_pot_directory_filter`

**Inputs** dirpath.

**Declared result** bool.

**Explicit results** false · not (subdir.startswith(“.”) or subdir.startswith(“\_”)).

**Local steps**

- If is\_gitignored(str(dirpath)).
  - Return false.
- Set subdir from os.path.basename(dirpath).
- Return not (subdir.startswith(“.”) or subdir.startswith(“\_”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in subdir.startswith(“.”) → subdir.startswith(“\_”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L974) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L391)

<a id="op-35dd3cc3e785b8"></a>
### Get ignored strings

`operation_foundation_gettext_translate_business_behavior_get_ignored_strings`

**Inputs** app.

**Declared result** set at tuple at tuple(str, (str bitwise or no value)).

**Explicit results** ignored\_strings.

**Explicit failure paths** ValueError(formatted text Invalid configuration: App '{app}' cannot ignore its own translatable strings. Remove '{app}' from the 'ignore\_translatable\_strings\_from' hook in {app).

**Local steps**

- Set ignored\_strings from set().
- For each ignore\_app in Platform.get\_hooks(“ignore\_translatable\_strings\_from”, list(), app\_name = app).
  - If ignore\_app equals app.
    - Raise ValueError(formatted text Invalid configuration: App '{app}' cannot ignore its own translatable strings. Remove '{app}' from the 'ignore\_translatable\_strings\_from' hook in {app).
  - Attempt the following.
    - Set catalog from get\_catalog(ignore\_app).
  - On failure (ModuleNotFoundError).
    - Evaluate secho(formatted text App '{ignore\_app}' specified in '{app}/hooks.py' 'ignore\_translatable\_strings\_from' hook is not installed. Skipping, err = true, fg = “yellow”).
    - Continue with the next iteration or loop test.
  - On failure (ImportError).
    - Evaluate secho(formatted text App '{ignore\_app}' specified in '{app}/hooks.py' 'ignore\_translatable\_strings\_from' hook could not be imported. Skipping, err = true, fg = “yellow”).
    - Continue with the next iteration or loop test.
  - On failure (AttributeError).
    - Evaluate secho(formatted text Site not initialized. Cannot load app '{ignore\_app}' specified in '{app}/hooks.py' 'ignore\_translatable\_strings\_from' hook. Skipping, err = true, fg = “yellow”).
    - Continue with the next iteration or loop test.
  - For each message in catalog.
    - Evaluate ignored\_strings.add(tuple(message.id, message.context)).
- Return ignored\_strings.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“ignore\_translatable\_strings\_from”, list(), app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L1158) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L393)

<a id="op-1cc0ac52b457cb"></a>
### Get is gitignored function for app

`operation_foundation_gettext_translate_business_behavior_get_is_gitignored_function_for_application`

**Inputs** app.

**Explicit results** deferred anonymous expression · \_check\_gitignore.

**Local steps**

- Bind dependencies git.
- If not app.
  - Return deferred anonymous expression.
- Set repo from git.Repo(Platform.get\_app\_source\_path(app), search\_parent\_directories = true).
- Bind local operation \_check\_gitignore for subsequent calls.
- Return \_check\_gitignore.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L1749) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L394)

<a id="op-150224346ce537"></a>
### Get is gitignored function for app.check gitignore

`operation_foundation_gettext_translate_business_behavior_get_is_gitignored_function_for_application_check_gitignore`

**Inputs** d.

**Explicit results** true · false.

**Local steps**

- Set d from d.rstrip(“/”).
- If repo.ignored(list(d)).
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L2006) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L395)

<a id="op-ad69aeaba8b253"></a>
### New po

`operation_foundation_gettext_translate_business_behavior_new_purchase_order`

**Inputs** locale, target\_app = no value.

**Local steps**

- Set apps from list(target\_app) when target\_app, otherwise Platform.get\_all\_apps(true).
  - Value choice on target\_app — true gives list(target\_app), false gives Platform.get\_all\_apps(true).
- For each app in apps.
  - Set po\_path from get\_po\_path(app, locale).
  - If os.path.exists(po\_path).
    - Evaluate print(formatted text {po\_path} exists. Skipping).
    - Continue with the next iteration or loop test.
  - Set pot\_catalog from get\_catalog(app).
  - Set pot\_catalog.locale from locale.
  - Set po\_path from write\_catalog(app, pot\_catalog, locale).
  - Evaluate print(formatted text PO file created\_at {po\_path}).
  - Evaluate print(“You will need to add the language in Platform/geo/languages.csv, if you haven't done it already.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L2116) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L407)

<a id="op-264fc73ee2b30b"></a>
### Compile translations

`operation_foundation_gettext_translate_business_behavior_compile_translations`

**Inputs** target\_app = no value, locale = no value, force = false.

**Local steps**

- Set apps from list(target\_app) when target\_app, otherwise Platform.get\_all\_apps(true).
  - Value choice on target\_app — true gives list(target\_app), false gives Platform.get\_all\_apps(true).
- Set tasks from list().
- For each app in apps.
  - Set locales from list(locale) when locale, otherwise get\_locales(app).
    - Value choice on locale — true gives list(locale), false gives get\_locales(app).
  - For each current\_locale in locales.
    - Evaluate tasks.append(tuple(app, current\_locale, force)).
- Set executer from multiprocessing.Pool(processes = 4).
- Evaluate executer.starmap(\_compile\_translation, tasks).
- Evaluate executer.close().
- Evaluate executer.join().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L13) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L389)

<a id="op-3fc57703e182fa"></a>
### Compile translation

`operation_foundation_gettext_translate_business_behavior_compile_translation`

**Inputs** app, locale, force = false.

**Explicit results** no value.

**Local steps**

- Set po\_path from get\_po\_path(app, locale).
- Set mo\_path from get\_mo\_path(app, locale).
- If not po\_path.exists().
  - Return no value.
- If (mo\_path.exists() and po\_path.stat().st\_mtime &lt; mo\_path.stat().st\_mtime and not force).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in mo\_path.exists() → po\_path.stat().st\_mtime &lt; mo\_path.stat().st\_mtime → not force.
  - Evaluate print(formatted text MO file already up to date at {mo\_path}).
  - Return no value.
- Within open(po\_path, “rb”) bound as f.
  - Set catalog from read\_po(f).
- Set mo\_path from write\_binary(app, catalog, locale).
- Evaluate print(formatted text MO file created at {mo\_path}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L12) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L388)

<a id="op-5c92d121d43f8d"></a>
### Update po

`operation_foundation_gettext_translate_business_behavior_update_purchase_order`

**Inputs** target\_app = no value, locale = no value.

**Local steps**

- Set apps from list(target\_app) when target\_app, otherwise Platform.get\_all\_apps(true).
  - Value choice on target\_app — true gives list(target\_app), false gives Platform.get\_all\_apps(true).
- For each app in apps.
  - Set locales from list(locale) when locale, otherwise get\_locales(app).
    - Value choice on locale — true gives list(locale), false gives get\_locales(app).
  - Set pot\_catalog from get\_catalog(app).
  - For each locale in locales.
    - Set po\_catalog from get\_catalog(app, locale).
    - Evaluate po\_catalog.update(pot\_catalog, no\_fuzzy\_matching = true).
    - Set po\_path from write\_catalog(app, po\_catalog, locale).
    - Evaluate print(formatted text PO file modified at {po\_path}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L3246) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L408)

<a id="op-6b2940b224bd06"></a>
### Migrate

`operation_foundation_gettext_translate_business_behavior_migrate`

**Inputs** app = no value, locale = no value.

**Local steps**

- Set apps from list(app) when app, otherwise Platform.get\_all\_apps(true).
  - Value choice on app — true gives list(app), false gives Platform.get\_all\_apps(true).
- For each app in apps.
  - Set app\_path from Path(Platform.get\_app\_path(app)).
  - For each filename in sorted((app\_path ÷ “translations”).glob(“\*.csv”)).
    - If (locale and nested operand in the contract.stem.replace(“-”, “\_”).lower() differs from locale.replace(“-”, “\_”).lower()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in locale → filename.stem.replace(“-”, “\_”).lower() differs from locale.replace(“-”, “\_”).lower().
      - Continue with the next iteration or loop test.
    - Evaluate csv\_to\_po(app, filename).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L14) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L404)

<a id="op-80f955cb25c033"></a>
### Csv to po

`operation_foundation_gettext_translate_business_behavior_comma_separated_values_to_purchase_order`

**Inputs** app, csv\_file.

**Local steps**

- Set tuple(language, \_, region) from csv\_file.stem.replace(“-”, “\_”).partition(“\_”).
- Set locale from formatted text {language}\_{region.upper()} when region, otherwise language.
  - Value choice on region — true gives formatted text {language}\_{region.upper()}, false gives language.
- Set catalog from get\_catalog(app, locale).
- Evaluate catalog.update(get\_catalog(app), no\_fuzzy\_matching = true).
- Set msgid\_context\_map from defaultdict(list).
- For each message in catalog.
  - Evaluate msgid\_context\_map at message.id.append(message.context).
- Within open(csv\_file) bound as f.
  - For each row in csv.reader(f).
    - If len(row) &lt; 2.
      - Continue with the next iteration or loop test.
    - Set msgid from row at 0.
    - Set msgstr from row at 1.
    - Set msgctxt from row at 2 when len(row) ≥ 3, otherwise no value.
      - Value choice on len(row) ≥ 3 — true gives row at 2, false gives no value.
    - If not msgctxt.
      - For each context in msgid\_context\_map.get(msgid, list()).
        - If message bound to catalog.get(msgid, context).
          - If not message.string.
            - Set message.string from msgstr.
    - Otherwise.
      - If message bound to catalog.get(msgid, msgctxt).
        - If not message.string.
          - Set message.string from msgstr.
- Set po\_path from write\_catalog(app, catalog, locale).
- Evaluate print(formatted text PO file created at {po\_path}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L11) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L387)

<a id="op-ef60f993bba3c9"></a>
### Get translations from mo

`operation_foundation_gettext_translate_business_behavior_get_translations_from_mo`

**Inputs** lang, app.

**Explicit results** mapping() · translations.

**Local steps**

- If (not lang or not app).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not lang → not app.
  - Return mapping().
- Set translations from mapping().
- Set lang from lang.replace(“-”, “\_”).
- Set mo\_file from get\_mo\_path(app, lang).
- If not mo\_file.exists().
  - Return translations.
- Within open(mo\_file, “rb”) bound as f.
  - Set catalog from read\_mo(f).
  - For each m in catalog.
    - If not m.id.
      - Continue with the next iteration or loop test.
    - Set key from m.id.
    - If m.context.
      - Set context from m.context.decode().
      - Set translations at formatted text {key}:{context} from m.string.
    - Otherwise.
      - Set translations at m.id from m.string.
- Return translations.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L4649) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L403)

<a id="op-99479910c19c0e"></a>
### Get language

`operation_foundation_translate_business_behavior_get_language`

**Inputs** lang\_list = no value.

**Declared result** str.

**Explicit results** language · Platform.local.lang · preferred\_language\_cookie · parent\_language · (Platform.get\_system\_settings(“language”) or “en”).

**Local steps**

- Set is\_logged\_in from Platform.session.user differs from “Guest”.
- If Platform.form\_dict.\_lang.
  - Set language from get\_lang\_code((Platform.form\_dict.\_lang or get\_parent\_language(Platform.form\_dict.\_lang))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.\_lang → get\_parent\_language(Platform.form\_dict.\_lang).
  - If language.
    - Return language.
- If is\_logged\_in.
  - Return Platform.local.lang.
- Set lang\_set from set((lang\_list or get\_all\_languages() or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lang\_list → get\_all\_languages() → list().
- Set preferred\_language\_cookie from get\_preferred\_language\_cookie().
- If preferred\_language\_cookie.
  - If preferred\_language\_cookie belongs to lang\_set.
    - Return preferred\_language\_cookie.
  - Set parent\_language from get\_parent\_language(preferred\_language\_cookie).
  - If parent\_language belongs to lang\_set.
    - Return parent\_language.
- Set accept\_language from list(Platform.request.accept\_languages.values()).
- For each language in accept\_language.
  - If language belongs to lang\_set.
    - Return language.
  - Set parent\_language from get\_parent\_language(language).
  - If parent\_language belongs to lang\_set.
    - Return parent\_language.
- Return (Platform.get\_system\_settings(“language”) or “en”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“language”) → “en”.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“language”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0453.json#L6044) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1348)

<a id="op-90464ecdd3810d"></a>
### Get parent language

`operation_foundation_translate_business_behavior_get_parent_language`

**Inputs** lang.

**Wrappers, in declaration order** functools.lru\_cache.

**Declared result** str.

**Explicit results** lang.split(sep) at 0.

**Local steps**

- For each sep in tuple(“\_”, “-”).
  - If sep belongs to lang.
    - Return lang.split(sep) at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0453.json#L6599) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1362)
