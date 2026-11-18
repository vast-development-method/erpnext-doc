# Forms, reports and navigation · operations 81

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Watch

<a id="op-f3015fcb9f549b"></a>
### Studio Sync Handler.restart timer

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_restart_timer`

**Inputs** self.

**State and service calls** call cancel on self.timer.

**Local steps**

- If self.timer.
  - Evaluate self.timer.cancel().
- Set self.timer from threading.Timer(DEBOUNCE\_SECONDS, self.flush).
- Set self.timer.daemon from true.
- Evaluate self.timer.start().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L44) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L114) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L202)

<a id="op-2b1687c1bd96be"></a>
### Studio Sync Handler.flush

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_flush`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Within self.lock.
  - Set tuple(paths, self.pending) from tuple(self.pending, set()).
- Attempt the following.
  - Evaluate Platform.init(self.site).
  - If is\_migrating().
    - Evaluate Platform.destroy().
    - Evaluate self.requeue(paths).
    - Return no value.
  - Evaluate Platform.connect().
- On failure (Exception).
  - Evaluate Platform.destroy().
  - Evaluate self.requeue(paths).
  - Evaluate print(formatted text &#91;watch-studio&#93; could not connect, will retry {traceback.format\_exc()}).
  - Return no value.
- Attempt the following.
  - For each path in sorted(paths).
    - Evaluate self.sync(path).
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Methods declared on this owner** [requeue](operations-081.md#op-54e7fa9505d014), [sync](operations-081.md#op-99359bd96fd73d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L37) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L195)

<a id="op-54e7fa9505d014"></a>
### Studio Sync Handler.requeue

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_requeue`

**Inputs** self, paths.

**Local steps**

- Within self.lock.
  - Update self.pending using bitwise or paths.
  - Evaluate self.restart\_timer().

If control reaches the end, it returns no value.

**Methods declared on this owner** [restart timer](operations-081.md#op-f3015fcb9f549b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L43) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L113) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L201)

<a id="op-99359bd96fd73d"></a>
### Studio Sync Handler.sync

`operation_foundation_binding_foundation_studio_watch_studiosynchandler_sync`

**Inputs** self, path.

**State and service calls** commit · rollback.

**Local steps**

- Attempt the following.
  - If info bound to sync\_file(path).
    - Evaluate Platform.db.commit().
    - Evaluate print(formatted text &#91;watch-studio&#93; synced {info at “doctype”} from {os.path.basename(path)}).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate print(formatted text &#91;watch-studio&#93; failed to sync {path} {Platform.get\_traceback()}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L45) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L115) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L203)

<a id="op-c63518787b2c98"></a>
### Is migrating

`operation_foundation_binding_foundation_studio_watch_is_migrating`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Attempt the following.
  - Within FileLock(Platform.get\_site\_path(LOCKS\_DIR, “bench\_migrate.lock”), timeout = 0).
    - Return false.
- On failure (Timeout).
  - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L35) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L193)

## Service · Website script

<a id="op-151d0e7f0da871"></a>
### Get context

`operation_foundation_public_pages_website_script_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “Website Script” via get\_cached\_doc.

**Local steps**

- Set should\_cache from not\_modified\_recently(Platform.get\_website\_settings(“modified”)).
- Set website\_script from Platform.get\_cached\_doc(“Website Script”).
- Set context.javascript from (website\_script.javascript or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in website\_script.javascript → empty text.
- Update should\_cache using bitwise and not\_modified\_recently(website\_script.modified).
- If theme bound to get\_active\_theme().
  - Set js from strip((theme.js or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in theme.js → empty text.
  - If js.
    - Update context.javascript using + (whitespace '\\n' + js).
  - Update should\_cache using bitwise and not\_modified\_recently(theme.modified).
- If not Platform.conf.developer\_mode.
  - Set context at “google\_analytics\_id” from get\_setting(“google\_analytics\_id”).
  - Set context at “google\_analytics\_anonymize\_ip” from get\_setting(“google\_analytics\_anonymize\_ip”).
- If should\_cache.
  - Evaluate Platform.local.response\_headers.update(cache\_headers).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Website Script”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L3129) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L102)

<a id="op-3380762f61302f"></a>
### Not modified recently

`operation_foundation_public_pages_website_script_business_behavior_not_modified_recently`

**Inputs** timestamp.

**Explicit results** ten\_minutes\_ago &gt; get\_datetime(timestamp).

**Local steps**

- Set ten\_minutes\_ago from add\_to\_date(minutes = negative 10, as\_datetime = true, as\_string = false).
- Return ten\_minutes\_ago &gt; get\_datetime(timestamp).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L3597) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L104)

<a id="op-7f4b05960872fb"></a>
### Get setting

`operation_foundation_public_pages_website_script_business_behavior_get_setting`

**Inputs** field\_name.

**Explicit results** (website\_settings or conf).

**Local steps**

- Set website\_settings from Platform.get\_website\_settings(field\_name).
- Set conf from Platform.conf.get(field\_name).
- Return (website\_settings or conf).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in website\_settings → conf.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L3714) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L103)

## Service · Website search

<a id="op-13fe9a0cdc8c7f"></a>
### Website Search.get schema

`operation_foundation_search_website_search_business_behavior_website_search_get_schema`

**Inputs** self.

**Explicit results** Schema(title = TEXT(stored = true), path = ID(stored = true), content = TEXT(stored = true)).

**Local steps**

- Return Schema(title = TEXT(stored = true), path = ID(stored = true), content = TEXT(stored = true)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L6825) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L552)

<a id="op-4d629f19753660"></a>
### Website Search.get fields to search

`operation_foundation_search_website_search_business_behavior_website_search_get_fields_to_search`

**Inputs** self.

**Explicit results** list(“title”, “content”).

**Local steps**

- Return list(“title”, “content”).

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L6948) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L549)

<a id="op-0195929ed74de9"></a>
### Website Search.get id

`operation_foundation_search_website_search_business_behavior_website_search_get_identifier`

**Inputs** self.

**Explicit results** “path”.

**Local steps**

- Return “path”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L7004) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L550)

<a id="op-e47c4ca69daec0"></a>
### Website Search.get items to index

`operation_foundation_search_website_search_business_behavior_website_search_get_items_to_index`

**Inputs** self.

**Explicit results** self.\_items\_to\_index · self.get\_items\_to\_index().

**Local steps**

- If getattr(self, “\_items\_to\_index”, no value) is distinct from no value.
  - Return self.\_items\_to\_index.
- Set self.\_items\_to\_index from list().
- Set routes from (get\_static\_pages\_from\_all\_apps() + slugs\_with\_web\_view(self.\_items\_to\_index)).
- For each tuple(i, route) in enumerate(routes).
  - Evaluate update\_progress\_bar(“Retrieving Routes”, i, len(routes)).
  - Update self.\_items\_to\_index using + list(self.get\_document\_to\_index(route)).
- Evaluate print().
- Return self.get\_items\_to\_index().

**Methods declared on this owner** [get document to index](operations-081.md#op-60091cec48b49e).

**Values supplied outside this operation** selected callable from getattr(self, “\_items\_to\_index”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L7046) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L551)

<a id="op-60091cec48b49e"></a>
### Website Search.get document to index

`operation_foundation_search_website_search_business_behavior_website_search_get_document_to_index`

**Inputs** self, route.

**Declared result** (Platform.\_dict bitwise or no value).

**Explicit results** Platform.\_dict(title = title, content = text\_content, path = route).

**Local steps**

- Evaluate Platform.set\_user(“Guest”).
- Set Platform.local.no\_cache from true.
- Attempt the following.
  - Evaluate set\_request(method = “GET”, path = route).
  - Set content from get\_response\_content(route).
  - Set soup from BeautifulSoup(content, “html.parser”).
  - Set page\_content from soup.find(class\_ = “page\_content”).
  - Set text\_content from page\_content.text when page\_content, otherwise empty text.
    - Value choice on page\_content — true gives page\_content.text, false gives empty text.
  - Set title from soup.title.text.strip() when soup.title, otherwise route.
    - Value choice on soup.title — true gives soup.title.text.strip(), false gives route.
  - Return Platform.\_dict(title = title, content = text\_content, path = route).
- On failure (Exception).
  - Take no action here.
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(“Administrator”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L548)

<a id="op-f8ae98537462a9"></a>
### Website Search.parse result

`operation_foundation_search_website_search_business_behavior_website_search_parse_result`

**Inputs** self, result.

**Explicit results** Platform.\_dict(title = result at “title”, path = result at “path”, title\_highlights = title\_highlights, content\_highlights = content\_highlights).

**Local steps**

- Set title\_highlights from result.highlights(“title”).
- Set content\_highlights from result.highlights(“content”).
- Return Platform.\_dict(title = result at “title”, path = result at “path”, title\_highlights = title\_highlights, content\_highlights = content\_highlights).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L400) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L553)

<a id="op-61d86149260bef"></a>
### Slugs with web view

`operation_foundation_search_website_search_business_behavior_slugs_with_web_view`

**Inputs** \_items\_to\_index.

**Record and data access** read “DocType” via get\_all · read doctype.name via get\_all.

**Explicit results** all\_routes.

**Local steps**

- Set all\_routes from list().
- Set filters from mapping(“has\_web\_view” → 1, “allow\_guest\_to\_view” → 1, “index\_web\_pages\_for\_search” → 1).
- Set fields from list(“name”, “is\_published\_field”, “website\_search\_field”).
- Set doctype\_with\_web\_views from Platform.get\_all(“DocType”, filters = filters, fields = fields).
- For each doctype in doctype\_with\_web\_views.
  - If doctype.is\_published\_field.
    - Set fields from list(“route”, doctype.website\_search\_field).
    - Set filters from mapping(doctype.is\_published\_field → 1).
    - If doctype.website\_search\_field.
      - Set docs from Platform.get\_all(doctype.name, filters = filters, fields = list(expanded fields, “title”)).
      - For each doc in docs.
        - Set content from Platform.utils.md\_to\_html(getattr(doc, doctype.website\_search\_field)).
        - Set soup from BeautifulSoup(content, “html.parser”).
        - Set text\_content from soup.text when soup, otherwise empty text.
          - Value choice on soup — true gives soup.text, false gives empty text.
        - Update \_items\_to\_index using + list(Platform.\_dict(title = doc.title, content = text\_content, path = doc.route)).
    - Otherwise.
      - Set docs from Platform.get\_all(doctype.name, filters = filters, fields = fields).
      - Update all\_routes using + list of route.route for route drawn from docs.
        - Draw route from docs.
- Return all\_routes.

**Values supplied outside this operation** selected callable from getattr(doc, doctype.website\_search\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L584) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L546)

<a id="op-e3d4d1f7253087"></a>
### Get static pages from all apps

`operation_foundation_search_website_search_business_behavior_get_static_pages_from_all_apps`

**Inputs** no declared parameters.

**Explicit results** routes\_to\_index.

**Local steps**

- Bind dependencies glob.
- Set apps from Platform.get\_installed\_apps().
- Set routes\_to\_index from list().
- For each app in apps.
  - Set path\_to\_index from Platform.get\_app\_path(app, “www”).
  - Set files\_to\_index from glob((path\_to\_index + “/\*\*/\*.html”), recursive = true).
  - Evaluate files\_to\_index.extend(glob((path\_to\_index + “/\*\*/\*.md”), recursive = true)).
  - For each file in files\_to\_index.
    - Set route from os.path.relpath(file, path\_to\_index).split(“.”, maxsplit = 1) at 0.
    - If route.endswith(“index”).
      - Set route from route.rsplit(“index”, 1) at 0.
    - Evaluate routes\_to\_index.append(route).
- Return routes\_to\_index.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L25) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L544)

<a id="op-0257548e0bd216"></a>
### Update index for path

`operation_foundation_search_website_search_business_behavior_update_index_for_path`

**Inputs** path.

**Explicit results** ws.update\_index\_by\_name(path).

**Local steps**

- Set ws from WebsiteSearch(INDEX\_NAME).
- Return ws.update\_index\_by\_name(path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L1654) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L547)

<a id="op-315acabe65a3eb"></a>
### Remove document from index

`operation_foundation_search_website_search_business_behavior_remove_document_from_index`

**Inputs** path.

**Explicit results** ws.remove\_document\_from\_index(path).

**Local steps**

- Set ws from WebsiteSearch(INDEX\_NAME).
- Return ws.remove\_document\_from\_index(path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L1733) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L545)

<a id="op-541435d3a1f4a6"></a>
### Build index for all routes

`operation_foundation_search_website_search_business_behavior_build_index_for_all_routes`

**Inputs** no declared parameters.

**Explicit results** ws.build().

**Local steps**

- Bind dependencies filelock.
- Within filelock(“building\_website\_search”).
  - Set ws from WebsiteSearch(INDEX\_NAME).
  - Return ws.build().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L1812) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L543)

## Record · Workspace

[Record definition](../../../../data/record-types/workspace.json)

<a id="op-b62314db9ea151"></a>
### Workspace.before validate

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_before_validate`

**Inputs** self.

**Local steps**

- Set self.content from sanitize\_content(self.content).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L1507) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1329)

<a id="op-92f2cac2051279"></a>
### Workspace.validate

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_validate`

**Inputs** self.

**Record and data access** read “Report” via get\_value.

**Explicit failure paths** validation helper — translated “You need to be Workspace Manager to edit this document” · propagate active failure · validation helper — translated “Content data shoud be a list” · validation helper — translated “Standard workspaces can't be edited directly. Your changes are saved as a customization.”.

**Local steps**

- Set self.title from strip\_html(self.title).
- If (self.public and not self.flags.with\_module and not is\_workspace\_manager() and not disable\_saving\_as\_public()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.public → not self.flags.with\_module → not is\_workspace\_manager() → not disable\_saving\_as\_public().
  - Call the validation error handler Platform.throw(translated “You need to be Workspace Manager to edit this document”).
- If self.has\_value\_changed(“title”).
  - Evaluate validate\_route\_conflict(self.doctype, self.title).
- Otherwise.
  - Evaluate validate\_route\_conflict(self.doctype, self.name).
- Attempt the following.
  - If not isinstance(loads(self.content), list).
    - Propagate the active failure.
- On failure (Exception).
  - Call the validation error handler Platform.throw(translated “Content data shoud be a list”).
- If (self.standard and not self.is\_new() and self.has\_value\_changed(“content”) and not Platform.conf.developer\_mode and not disable\_saving\_as\_public()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.standard → not self.is\_new() → self.has\_value\_changed(“content”) → not Platform.conf.developer\_mode → not disable\_saving\_as\_public().
  - Call the validation error handler Platform.throw(translated “Standard workspaces can't be edited directly. Your changes are saved as a customization.”).
- For each d in self.get(“links”).
  - If (d.link\_type equals “Report” and d.is\_query\_report differs from 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.link\_type equals “Report” → d.is\_query\_report differs from 1.
    - Set d.report\_ref\_doctype from Platform.get\_value(“Report”, d.link\_to, “ref\_doctype”).
- For each shortcut in self.get(“shortcuts”).
  - If shortcut.type equals “Report”.
    - Set shortcut.report\_ref\_doctype from Platform.get\_value(“Report”, shortcut.link\_to, “ref\_doctype”).
- Evaluate self.validate\_duplicate\_widget\_labels().
- Evaluate self.validate\_shared\_page\_has\_a\_module().
- Evaluate self.validate\_private\_page\_is\_yours().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate widget labels](operations-082.md#op-26ad5983b32cc0), [validate shared page has a module](operations-081.md#op-b544c7dabec2d5), [validate private page is yours](operations-081.md#op-4f3e0e36f43694).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L48) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1340)

<a id="op-4f3e0e36f43694"></a>
### Workspace.validate private page is yours

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_validate_private_page_is_yours`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You can only create a private workspace for yourself.”.

**Local steps**

- If (self.public or not self.for\_user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.public → not self.for\_user.
  - Return no value.
- If (self.for\_user equals Platform.session.user or is\_workspace\_manager()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.for\_user equals Platform.session.user → is\_workspace\_manager().
  - Return no value.
- If any(generator of Platform.flags.get(flag) for flag drawn from tuple(“in\_install”, “in\_migrate”, “in\_patch”, “in\_import”, …)).
  - Draw flag from tuple(“in\_install”, “in\_migrate”, “in\_patch”, “in\_import”, …).
  - Return no value.
- Call the validation error handler Platform.throw(translated “You can only create a private workspace for yourself.”, Platform.PermissionError, title = translated “Not your workspace”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L764)

<a id="op-b544c7dabec2d5"></a>
### Workspace.validate shared page has a module

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_validate_shared_page_has_a_module`

**Inputs** self.

**Explicit failure paths** validation helper — translated “A shared workspace needs a module other than {0}.”.format(translated PRIVATE\_MODULE).

**Local steps**

- If (self.public and self.module equals PRIVATE\_MODULE).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.public → self.module equals PRIVATE\_MODULE.
  - Call the validation error handler Platform.throw(translated “A shared workspace needs a module other than {0}.”.format(translated PRIVATE\_MODULE), title = translated “Pick a module”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L765)

<a id="op-85a24cb1a018e3"></a>
### Workspace.get widget label counts

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_get_widget_label_counts`

**Inputs** doc, parentfield.

**Wrappers, in declaration order** staticmethod.

**Declared result** Counter.

**Explicit results** counts.

**Local steps**

- Set rows from (doc.get(parentfield) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(parentfield) → list().
- If parentfield equals “links”.
  - Set rows from list of row for row drawn from rows where row.type equals “Card Break”.
    - Draw row from rows, keep a combination only if (row.type equals “Card Break”).
- Set counts from Counter().
- For each row in rows.
  - If label bound to (row.label or empty text).strip().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.label → empty text.
    - Update counts at label using + 1.
- Return counts.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L2386) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1335)
