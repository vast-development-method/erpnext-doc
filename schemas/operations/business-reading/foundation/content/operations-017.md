# Web content and issued documents · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-88c9e46157fe10"></a>
### Get line number

`operation_foundation_binding_foundation_gettext_extractors_utils_get_line_number`

**Inputs** text, key, value.

**Declared result** (int bitwise or no value).

**Explicit results** (text.count(whitespace '\\n', 0, index) + 1) when index ≥ 0, otherwise no value.

**Local steps**

- Set index from text.find(formatted text {json.dumps(key)}: {json.dumps(value)}).
- Return (text.count(whitespace '\\n', 0, index) + 1) when index ≥ 0, otherwise no value.
  - Value choice on index ≥ 0 — true gives (text.count(whitespace '\\n', 0, index) + 1), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1457)

<a id="op-0c40c5e2378737"></a>
### Extract messages from docfield

`operation_foundation_gettext_extractors_utils_business_behavior_extract_messages_from_record_field`

**Inputs** doctype, field, text.

**Local steps**

- Set fieldtype from field.get(“fieldtype”).
- Set fieldname from field.get(“fieldname”).
- Set label from field.get(“label”).
- If label.
  - yield tuple(get\_line\_number(text, “label”, label), label, formatted text Label of the {fieldname} ({fieldtype}) field in DocType '{doctype}').
  - Set \_label from label.
- Otherwise.
  - Set \_label from fieldname.
- If description bound to field.get(“description”).
  - yield tuple(get\_line\_number(text, “description”, description), description, formatted text Description of the '{\_label}' ({fieldtype}) field in DocType '{doctype}').
- If message bound to field.get(“options”).
  - Set lineno from get\_line\_number(text, “options”, message).
  - If (fieldtype equals “Select” and fieldname does not belong to EXCLUDE\_SELECT\_OPTIONS).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Select” → fieldname does not belong to EXCLUDE\_SELECT\_OPTIONS.
    - Set select\_options from list of option for option drawn from message.split(whitespace '\\n') where (option and not option.isdigit()).
      - Draw option from message.split(whitespace '\\n'), keep a combination only if ((option and not option.isdigit())).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in option → not option.isdigit().
    - yield values from generator of tuple(lineno, option, formatted text Option for the '{\_label}' ({fieldtype}) field in DocType '{doctype}') for option drawn from select\_options.
      - Draw option from select\_options.
  - Otherwise.
    - If fieldtype equals “HTML”.
      - yield tuple(lineno, message, formatted text Content of the '{\_label}' ({fieldtype}) field in DocType '{doctype}').

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L7) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1609) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L374)

<a id="op-ccb27e567f7b70"></a>
### Extract messages from links

`operation_foundation_gettext_extractors_utils_business_behavior_extract_messages_from_links`

**Inputs** doctype, links, text.

**Local steps**

- For each link in links.
  - If group bound to link.get(“group”).
    - yield tuple(get\_line\_number(text, “group”, group), group, formatted text Group in {doctype}'s connections).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1608) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L373)

<a id="op-444689201a1e3e"></a>
### Delete page cache

`operation_foundation_website_utils_business_behavior_delete_page_cache`

**Inputs** path = no value.

**Local steps**

- If path.
  - Evaluate Platform.cache.delete\_value(formatted text {WEBSITE\_PAGE\_CACHE\_PREFIX}{path}).
- Otherwise.
  - Evaluate Platform.cache.delete\_keys(WEBSITE\_PAGE\_CACHE\_PREFIX).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L5098) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L603) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1547)

<a id="op-f8dbdd7b26a331"></a>
### Find first image

`operation_foundation_website_utils_business_behavior_find_first_image`

**Inputs** html.

**Explicit results** next(m).groups() at 0 · no value.

**Local steps**

- Set m from IMAGE\_TAG\_PATTERN.finditer(html).
- Attempt the following.
  - Return next(m).groups() at 0.
- On failure (StopIteration).
  - Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L5220) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1550)

<a id="op-af4b0d65829ce0"></a>
### Can cache

`operation_foundation_website_utils_business_behavior_can_cache`

**Inputs** no\_cache = false.

**Explicit results** true · false · not no\_cache.

**Local steps**

- If Platform.flags.force\_website\_cache.
  - Return true.
- If (Platform.conf.disable\_website\_cache or Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.disable\_website\_cache → Platform.conf.developer\_mode.
  - Return false.
- If getattr(Platform.local, “no\_cache”, false).
  - Return false.
- If (Platform.request and Platform.request.query\_string).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.request → Platform.request.query\_string.
  - Return false.
- Return not no\_cache.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “no\_cache”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L5343) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1542)

<a id="op-2a12350a3081e8"></a>
### Get comment list

`operation_foundation_website_utils_business_behavior_get_comment_list`

**Inputs** doctype, name.

**Record and data access** read “Comment” via get\_all · read “Communication” via get\_all.

**Explicit results** sorted((comments + communications), key = deferred anonymous expression, reverse = true).

**Local steps**

- Set comments from Platform.get\_all(“Comment”, fields = list(“name”, “creation”, “owner”, “comment\_email”, …), filters = dict(reference\_doctype = doctype, reference\_name = name, comment\_type = “Comment”), or\_filters = list(l ….
- Set communications from Platform.get\_all(“Communication”, fields = list(“name”, “creation”, “owner”, “owner as comment\_email”, …), filters = dict(reference\_doctype = doctype, reference\_name = name), or\_filters = list(list(“recipi ….
- Return sorted((comments + communications), key = deferred anonymous expression, reverse = true).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0538.json#L5537) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L609) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1553)

<a id="op-0994c0f812eca1"></a>
### Get home page

`operation_foundation_website_utils_business_behavior_get_home_page`

**Inputs** no declared parameters.

**Explicit results** Platform.local.flags.home\_page · \_get\_home\_page() · Platform.cache.hget(“home\_page”, Platform.session.user, \_get\_home\_page).

**Local steps**

- If (Platform.local.flags.home\_page and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.flags.home\_page → not Platform.in\_test.
  - Return Platform.local.flags.home\_page.
- Bind local operation \_get\_home\_page for subsequent calls.
- If Platform.\_dev\_server.
  - Return \_get\_home\_page().
- Return Platform.cache.hget(“home\_page”, Platform.session.user, \_get\_home\_page).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L63) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L614) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1558)

<a id="op-dee93482038a28"></a>
### Get home page.get home page

`operation_foundation_website_utils_business_behavior_get_home_page_get_home_page`

**Inputs** no declared parameters.

**Record and data access** read “Role” via get\_value · read “Portal Settings” via get\_single\_value · read “Website Settings” via get\_single\_value.

**Explicit results** home\_page.

**Local steps**

- Set home\_page from no value.
- If Platform.session.user differs from “Guest”.
  - For each role in Platform.get\_roles().
    - Set home\_page from Platform.db.get\_value(“Role”, role, “home\_page”).
    - If home\_page.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If not home\_page.
    - Set home\_page from Platform.db.get\_single\_value(“Portal Settings”, “default\_portal\_home”).
- If not home\_page.
  - Set home\_page from get\_home\_page\_via\_hooks().
- If not home\_page.
  - Set home\_page from Platform.db.get\_single\_value(“Website Settings”, “home\_page”).
- If not home\_page.
  - Set home\_page from “login” when Platform.session.user equals “Guest”, otherwise “me”.
    - Value choice on Platform.session.user equals “Guest” — true gives “login”, false gives “me”.
- Set home\_page from home\_page.strip(“/”).
- If (home\_page equals “me” and Platform.session.data.user\_type equals “System User”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in home\_page equals “me” → Platform.session.data.user\_type equals “System User”.
  - Set home\_page from “desk”.
- If (home\_page equals “me” and is\_portal\_user()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in home\_page equals “me” → is\_portal\_user().
  - Set home\_page from “portal”.
- Set default\_workspace from Platform.get\_user().load\_user().default\_workspace.
- If default\_workspace.
  - Set home\_page from get\_url\_to\_workspace(default\_workspace at “name”, default\_workspace at “public”).
  - Return home\_page.
- Return home\_page.

**Values supplied outside this operation** effective access from Platform.get\_roles() · configured or stored value from Platform.db.get\_single\_value(“Portal Settings”, “default\_portal\_home”), Platform.db.get\_single\_value(“Website Settings”, “home\_page”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L64) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L615) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1559)

<a id="op-edaca2f24f4e37"></a>
### Get home page via hooks

`operation_foundation_website_utils_business_behavior_get_home_page_via_hooks`

**Inputs** no declared parameters.

**Explicit results** home\_page.

**Local steps**

- Set home\_page from no value.
- Set home\_page\_method from Platform.get\_hooks(“get\_website\_user\_home\_page”).
- If home\_page\_method.
  - Set home\_page from Platform.get\_attr(home\_page\_method at negative 1)(Platform.session.user).
- Otherwise.
  - If Platform.get\_hooks(“website\_user\_home\_page”).
    - Set home\_page from Platform.get\_hooks(“website\_user\_home\_page”) at negative 1.
- If not home\_page.
  - Set role\_home\_page from Platform.get\_hooks(“role\_home\_page”).
  - If role\_home\_page.
    - For each role in Platform.get\_roles().
      - If role belongs to role\_home\_page.
        - Set home\_page from role\_home\_page at role at negative 1.
        - Leave the innermost loop without its normal-exhaustion alternative.
- If not home\_page.
  - Set home\_page from Platform.get\_hooks(“home\_page”).
  - If home\_page.
    - Set home\_page from home\_page at negative 1.
- If home\_page.
  - Set home\_page from home\_page.strip(“/”).
- Return home\_page.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“get\_website\_user\_home\_page”), Platform.get\_attr(home\_page\_method at negative 1) and 3 further calls · effective access from Platform.get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L616) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1560)

<a id="op-01a388cee315c0"></a>
### Get boot data

`operation_foundation_website_utils_business_behavior_get_boot_data`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_cached\_value.

**Explicit results** mapping(“lang” → (Platform.local.lang or “en”), “apps\_data” → mapping(“apps” → (apps or list()), “is\_desk\_apps” → 1 when bool(is\_desk\_apps(apps)), otherwise 0, “default\_path” → (get\_default\_path() or empty ….

**Local steps**

- Bind dependencies is\_fc\_site.
- Bind dependencies get\_date\_format, get\_first\_day\_of\_the\_week, get\_number\_format, get\_time\_format.
- Set apps from get\_apps().
- Return mapping(“lang” → (Platform.local.lang or “en”), “apps\_data” → mapping(“apps” → (apps or list()), “is\_desk\_apps” → 1 when bool(is\_desk\_apps(apps)), otherwise 0, “default\_path” → (get\_default\_path() or empty ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → “en”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in apps → list().
  - Value choice on bool(is\_desk\_apps(apps)) — true gives 1, false gives 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_default\_path() → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.get\_system\_settings(“float\_precision”)) → 3.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“User”, Platform.session.user, “time\_zone”) → get\_system\_timezone().
  - Value choice on is\_fc\_site() — true gives 1, false gives 0.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“float\_precision”), Platform.get\_system\_settings(“currency\_precision”) and 3 further calls.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L62) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L608) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1552)

<a id="op-6e1df7716cae6a"></a>
### Is signup disabled

`operation_foundation_website_utils_business_behavior_is_signup_disabled`

**Inputs** no declared parameters.

**Explicit results** Platform.get\_website\_settings(“disable\_signup”).

**Local steps**

- Return Platform.get\_website\_settings(“disable\_signup”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L1181) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L625) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1569)

<a id="op-29f67e9a1f2116"></a>
### Cleanup page name

`operation_foundation_website_utils_business_behavior_cleanup_page_name`

**Inputs** title.

**Declared result** str.

**Explicit results** empty text · name at slice no value to 140.

**Local steps**

- If not title.
  - Return empty text.
- Set name from title.lower().
- Set name from CLEANUP\_PATTERN\_1.sub(empty text, name).
- Set name from CLEANUP\_PATTERN\_2.sub(“-”, name).
- Set name from “-”.join(name.split()).
- Set name from CLEANUP\_PATTERN\_3.sub(“\\1”, name).
- Return name at slice no value to 140.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L1234) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1544)

<a id="op-2a3f1c06606ff1"></a>
### Abs url

`operation_foundation_website_utils_business_behavior_abs_resource_address`

**Inputs** path.

**Explicit results** no value · path.

**Local steps**

- If not path.
  - Return no value.
- If (path.startswith(text in the contract) or path.startswith(text in the contract)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path.startswith(text in the contract) → path.startswith(text in the contract).
  - Return path.
- If path.startswith(“tel:”).
  - Return path.
- If path.startswith(“data:”).
  - Return path.
- If not path.startswith(“/”).
  - Set path from (“/” + path).
- Return path.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L1479) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1537)

<a id="op-3a71d273c02eb8"></a>
### Get toc

`operation_foundation_website_utils_business_behavior_get_toc`

**Inputs** route, url\_prefix = no value, app = no value.

**Explicit results** Platform.get\_template(“templates/includes/full\_index.html”).render(mapping(“full\_index” → full\_index, “url\_prefix” → (url\_prefix or “/”), “route” → route.rstrip(“/”))).

**Local steps**

- Set full\_index from get\_full\_index(app = app).
- Return Platform.get\_template(“templates/includes/full\_index.html”).render(mapping(“full\_index” → full\_index, “url\_prefix” → (url\_prefix or “/”), “route” → route.rstrip(“/”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in url\_prefix → “/”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L1709) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1567)

<a id="op-77905076a9e4af"></a>
### Get next link

`operation_foundation_website_utils_business_behavior_get_next_link`

**Inputs** route, url\_prefix = no value, app = no value.

**Explicit results** ((text in the contract + Platform.\_(“Next”)) + “: &lt;a class="btn-next" href="{url\_prefix}{route}"&gt;{title}&lt;/a&gt;&lt;/p&gt;”).format(expanded names next\_item) · empty text.

**Local steps**

- Set next\_item from no value.
- Set route from route.rstrip(“/”).
- Set children\_map from get\_full\_index(app = app).
- Set parent\_route from os.path.dirname(route).
- Set children from children\_map.get(parent\_route, no value).
- If (parent\_route and children).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_route → children.
  - For each tuple(i, c) in enumerate(children).
    - If (c.route equals route and i &lt; (len(children) − 1)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in c.route equals route → i &lt; (len(children) − 1).
      - Set next\_item from children at (i + 1).
      - Set next\_item.url\_prefix from (url\_prefix or “/”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in url\_prefix → “/”.
- If next\_item.
  - If (next\_item.route and next\_item.title).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in next\_item.route → next\_item.title.
    - Return ((text in the contract + Platform.\_(“Next”)) + “: &lt;a class="btn-next" href="{url\_prefix}{route}"&gt;{title}&lt;/a&gt;&lt;/p&gt;”).format(expanded names next\_item).
- Return empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L1900) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L617) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1561)

<a id="op-40f01cac40e9f6"></a>
### Get full index

`operation_foundation_website_utils_business_behavior_get_full_index`

**Inputs** route = no value, app = no value.

**Explicit results** Platform.local.flags.children\_map.

**Local steps**

- Bind dependencies get\_pages.
- If not Platform.local.flags.children\_map.
  - Bind local operation \_build for subsequent calls.
  - Set children\_map from Platform.cache.get\_value(“website\_full\_index”, \_build).
  - Set Platform.local.flags.children\_map from children\_map.
- Return Platform.local.flags.children\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L2376) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1556)

<a id="op-ae154d83355519"></a>
### Get full index.build

`operation_foundation_website_utils_business_behavior_get_full_index_build`

**Inputs** no declared parameters.

**Explicit results** children\_map.

**Local steps**

- Set children\_map from mapping().
- Set added from list().
- Set pages from get\_pages(app = app).
- For each tuple(route, page\_info) in pages.items().
  - Set parent\_route from os.path.dirname(route).
  - If parent\_route does not belong to added.
    - Evaluate children\_map.setdefault(parent\_route, list()).append(page\_info).
- For each tuple(route, children) in children\_map.items().
  - If route does not belong to pages.
    - Continue with the next iteration or loop test.
  - Set page\_info from pages at route.
  - If (page\_info.index or “index” belongs to page\_info.template).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_info.index → “index” belongs to page\_info.template.
    - Set new\_children from list().
    - Set page\_info.extn from empty text.
    - For each name in (page\_info.index or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_info.index → list().
      - Set child\_route from ((page\_info.route + “/”) + name).
      - If child\_route belongs to pages.
        - If child\_route does not belong to added.
          - Evaluate new\_children.append(pages at child\_route).
          - Evaluate added.append(child\_route).
    - Set \_children from sorted(children, key = deferred anonymous expression).
    - For each child\_route in \_children.
      - If child\_route does not belong to new\_children.
        - If child\_route does not belong to added.
          - Evaluate new\_children.append(child\_route).
          - Evaluate added.append(child\_route).
    - Set children\_map at route from new\_children.
- Return children\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L1332) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1557)

<a id="op-6825dfb40b5ed1"></a>
### Extract title

`operation_foundation_website_utils_business_behavior_extract_title`

**Inputs** source, path.

**Explicit results** title.

**Local steps**

- Set title from extract\_comment\_tag(source, “title”).
- If (not title and text in the contract belongs to source).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not title → text in the contract belongs to source.
  - Set match from H1\_TAG\_PATTERN.search(source).group().
  - Set title\_content from match.strip() at slice no value to 300.
  - If “{{” does not belong to title\_content.
    - Set title from title\_content.
- If not title.
  - Set title from nested operand in the contract(nested operand in the contract).replace(“\_”, one space).replace(“-”, one space).title().
- Return title.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L3250) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L605) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1549)

<a id="op-03c7ccd4b37a03"></a>
### Extract comment tag

`operation_foundation_website_utils_business_behavior_extract_comment_tag`

**Inputs** source, tag.

**Explicit results** matched\_pattern.groups() at 0.strip() when matched\_pattern, otherwise no value.

**Local steps**

- Set matched\_pattern from re.search(formatted text &lt;!-- {tag}:(&#91;^&gt;&#93;\*) --&gt;, source).
- Return matched\_pattern.groups() at 0.strip() when matched\_pattern, otherwise no value.
  - Value choice on matched\_pattern — true gives matched\_pattern.groups() at 0.strip(), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L3619) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L604) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1548)

<a id="op-d1d3fc9869cfa8"></a>
### Get html content based on type

`operation_foundation_website_utils_business_behavior_get_document_markup_content_based_on_type`

**Inputs** doc, fieldname, content\_type.

**Explicit results** content.

**Local steps**

- Set content from doc.get(fieldname).
- If content\_type equals “Markdown”.
  - Set content from md\_to\_html(doc.get((fieldname + “\_md”))).
- Otherwise.
  - If content\_type equals “HTML”.
    - Set content from doc.get((fieldname + “\_html”)).
- If content is identical to no value.
  - Set content from empty text.
- Return content.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L3766) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1554)

<a id="op-29d89f70085aa6"></a>
### Clear cache

`operation_foundation_website_utils_business_behavior_clear_cache`

**Inputs** path = no value.

**Local steps**

- Bind dependencies clear\_routing\_cache.
- Evaluate clear\_routing\_cache().
- Set keys from list(“website\_generator\_routes”, “website\_pages”, “website\_full\_index”, “languages\_with\_name”, …).
- If path.
  - Evaluate Platform.cache.hdel(“website\_redirects”, path).
  - Evaluate delete\_page\_cache(path).
- Otherwise.
  - Evaluate Platform.clear\_cache(“Guest”).
  - Evaluate delete\_page\_cache().
  - Update keys using + list(“portal\_menu\_items”, “home\_page”, “website\_route\_rules”, “doctypes\_with\_web\_view”, …).
- Evaluate Platform.cache.delete\_value(keys).
- For each method in Platform.get\_hooks(“website\_clear\_cache”).
  - Evaluate Platform.get\_attr(method)(path).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“website\_clear\_cache”), Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L4013) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1545)

<a id="op-2a86a310a948c2"></a>
### Clear website cache

`operation_foundation_website_utils_business_behavior_clear_website_cache`

**Inputs** path = no value.

**Local steps**

- Evaluate clear\_cache(path).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L4344) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L602) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1546)

<a id="op-bd4e1c427b2251"></a>
### Get frontmatter

`operation_foundation_website_utils_business_behavior_get_frontmatter`

**Inputs** string.

**Explicit results** mapping(“attributes” → yaml.safe\_load(frontmatter) when frontmatter, otherwise empty text, “body” → body).

**Local steps**

- Set frontmatter from empty text.
- Set body from empty text.
- Set result from FRONTMATTER\_PATTERN.search(string).
- If result.
  - Set frontmatter from result.group(1).
  - Set body from result.group(2).
- Return mapping(“attributes” → yaml.safe\_load(frontmatter) when frontmatter, otherwise empty text, “body” → body).
  - Value choice on frontmatter — true gives yaml.safe\_load(frontmatter), false gives empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0539.json#L4399) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1555)
