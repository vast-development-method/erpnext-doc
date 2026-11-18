# Forms, reports and navigation · operations 62

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sidebar

[Record definition](../../../../data/record-types/sidebar.json)

<a id="op-fdb789fd23d629"></a>
### Shell Index.resolve

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_shellindex_resolve`

**Inputs** self, kind, entity, module.

**Declared result** (str bitwise or no value).

**Explicit results** own · heir · listed at 0 · heirs at 0 when heirs, otherwise own.

**Local steps**

- Set listed from list of shell for shell drawn from self.listed\_in(kind, entity) where shell differs from PRIVATE\_MODULE.
  - Draw shell from self.listed\_in(kind, entity), keep a combination only if (shell differs from PRIVATE\_MODULE).
- Set own from self.shell\_of(module).
- If (own and own belongs to listed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in own → own belongs to listed.
  - Return own.
- If (own and own belongs to self.computed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in own → own belongs to self.computed.
  - Return own.
- Set heirs from (self.heirs.get(module) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.heirs.get(module) → list().
- For each heir in heirs.
  - If heir belongs to listed.
    - Return heir.
- If listed.
  - Return listed at 0.
- Return heirs at 0 when heirs, otherwise own.
  - Value choice on heirs — true gives heirs at 0, false gives own.

**Methods declared on this owner** [listed in](operations-061.md#op-bb63836d421930), [shell of](operations-061.md#op-c1d989bf0e2886).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L747)

<a id="op-83e10f1bfce145"></a>
### Routable entities

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_routable_entities`

**Inputs** perm\_ctx.

**Declared result** dict at tuple(str, dict at tuple(str, str)).

**Record and data access** read “DocType” via get\_all.

**Explicit results** mapping(“DocType” → doctypes, “Report” → mapping of name → row.get(“module”) for tuple(name, row) drawn from (perm\_ctx.allowed\_reports or mapping()).items(), “Page” → mapping of name → row.get(“module”) fo ….

**Local steps**

- Set readable from set((perm\_ctx.can\_read or tuple())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in perm\_ctx.can\_read → tuple().
- Set doctypes from mapping of row.name → row.module for row drawn from Platform.get\_all(“DocType”, filters = mapping(“istable” → 0), fields = list(“name”, “module”)) where row.name belongs to readable.
  - Draw row from Platform.get\_all(“DocType”, filters = mapping(“istable” → 0), fields = list(“name”, “module”)), keep a combination only if (row.name belongs to readable).
- Return mapping(“DocType” → doctypes, “Report” → mapping of name → row.get(“module”) for tuple(name, row) drawn from (perm\_ctx.allowed\_reports or mapping()).items(), “Page” → mapping of name → row.get(“module”) fo ….
  - Draw tuple(name, row) from (perm\_ctx.allowed\_reports or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in perm\_ctx.allowed\_reports → mapping().
  - Draw tuple(name, row) from (perm\_ctx.allowed\_pages or mapping()).items(), keep a combination only if (not row.get(“system\_page”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in perm\_ctx.allowed\_pages → mapping().
  - Draw row from perm\_ctx.get\_allowed\_dashboards(cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L741)

## Record · Sidebar item group

<a id="op-3efe7dc2631861"></a>
### Get reports

`operation_foundation_binding_foundation_desk_doctype_sidebar_item_group_sidebar_item_group_get_reports`

**Inputs** module\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Sidebar Item Group” via get\_doc.

**Explicit results** reports\_info.

**Local steps**

- Set reports\_info from list().
- If module\_name.
  - Set sidebar\_group from Platform.get\_doc(“Sidebar Item Group”, module\_name).
  - For each report\_links in sidebar\_group.links.
    - Set allowed\_reports from DeskViews.get\_allowed\_reports().
    - If report\_links.report belongs to allowed\_reports.
      - Evaluate reports\_info.append(allowed\_reports at report\_links.report).
  - Return reports\_info.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L733)

## Service · Sitemap

<a id="op-9ba2c283eee12f"></a>
### Get context

`operation_foundation_public_pages_sitemap_business_behavior_get_context`

**Inputs** context.

**Record and data access** read settings via get\_single\_value.

**Explicit results** mapping(“links” → links).

**Local steps**

- Set disabled\_controllers from set of controller for tuple(controller, settings) drawn from mapping(“Platform.www.about” → “About Us Settings”, “Platform.www.contact” → “Contact Us Settings”).items() where Platform.get\_single\_value(sett ….
  - Draw tuple(controller, settings) from mapping(“Platform.www.about” → “About Us Settings”, “Platform.www.contact” → “Contact Us Settings”).items(), keep a combination only if (Platform.get\_single\_value(settings, “is\_disabled”)).
- Set links from list of mapping(“loc” → get\_url(quote(nested operand in the contract.name.encode(“utf-8”))), “lastmod” → nowdate()) for tuple(route, page) drawn from get\_pages().items() where (page.sitemap and page.contro ….
  - Draw tuple(route, page) from get\_pages().items(), keep a combination only if ((page.sitemap and page.controller does not belong to disabled\_controllers)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in page.sitemap → page.controller does not belong to disabled\_controllers.
- Evaluate links.extend(generator of mapping(“loc” → get\_url(quote(nested operand in the contract.encode(“utf-8”))), “lastmod” → formatted text {data at “modified”}) for tuple(route, data) drawn from get\_public\_pages ….
  - Draw tuple(route, data) from get\_public\_pages\_from\_doctypes().items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in route → empty text.
- Return mapping(“links” → links).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(settings, “is\_disabled”) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L85) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L89)

<a id="op-df38fde2253a9e"></a>
### Get public pages from doctypes

`operation_foundation_public_pages_sitemap_business_behavior_get_public_pages_from_record_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** redis\_cache(ttl = ((6 × 60) × 60)).

**Record and data access** read “Website Settings” via get\_single\_value · read doctype via get\_all.

**Explicit results** routes.

**Explicit failure paths** e.

**Local steps**

- Set routes from mapping().
- Set doctypes\_with\_web\_view from get\_doctypes\_with\_web\_view().
- Set robot\_parser\_instance from no value.
- If robots\_txt bound to Platform.get\_single\_value(“Website Settings”, “robots\_txt”).
  - Set robot\_parser\_instance from robotparser.RobotFileParser().
  - Evaluate robot\_parser\_instance.parse(robots\_txt.splitlines()).
- For each doctype in doctypes\_with\_web\_view.
  - Set controller from get\_controller(doctype).
  - Set meta from Platform.get\_meta(doctype).
  - If not meta.allow\_guest\_to\_view.
    - Continue with the next iteration or loop test.
  - Set condition\_field from (meta.is\_published\_field or controller.website.condition\_field).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.is\_published\_field → controller.website.condition\_field.
  - If not condition\_field.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set res from Platform.get\_all(doctype, fields = list(“route”, “name”, “modified”), filters = mapping(condition\_field → true)).
  - On failure (Exception) bound to e.
    - If not Platform.db.is\_missing\_column(e).
      - Raise e.
  - For each r in res.
    - If (not r.route or is\_dynamic\_route(r.route)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not r.route → is\_dynamic\_route(r.route).
      - Continue with the next iteration or loop test.
    - If (robot\_parser\_instance and not robot\_parser\_instance.can\_fetch(“\*”, formatted text /{r.route})).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in robot\_parser\_instance → not robot\_parser\_instance.can\_fetch(“\*”, formatted text /{r.route}).
      - Continue with the next iteration or loop test.
    - Set routes at r.route from mapping(“doctype” → doctype, “name” → r.name, “modified” → r.modified).
- Return routes.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Website Settings”, “robots\_txt”) · selected callable from get\_controller(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L1003) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L90)

<a id="op-dfc92aefcbc91c"></a>
### Is dynamic route

`operation_foundation_public_pages_sitemap_business_behavior_is_dynamic_route`

**Inputs** route.

**Declared result** bool.

**Explicit results** (“&lt;” belongs to route or any(generator of part.startswith(“:”) for part drawn from route.split(“/”))).

**Local steps**

- Return (“&lt;” belongs to route or any(generator of part.startswith(“:”) for part drawn from route.split(“/”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “&lt;” belongs to route → any(generator of part.startswith(“:”) for part drawn from route.split(“/”)).
  - Draw part from route.split(“/”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L1743) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L91)

## Service · Sqlite search

<a id="op-46fb1d5b6cddda"></a>
### Strip surrogates

`operation_foundation_search_sqlite_search_business_behavior_strip_surrogates`

**Inputs** value.

**Explicit results** value · nested operand in the contract(nested operand in the contract, nested operand in the contract).decode(“utf-16-le”, “surrogatepass”).encode(“utf-8”, “ignore”).decode(“utf-8”).

**Local steps**

- If (not isinstance(value, str) or not SURROGATE\_RE.search(value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(value, str) → not SURROGATE\_RE.search(value).
  - Return value.
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract).decode(“utf-16-le”, “surrogatepass”).encode(“utf-8”, “ignore”).decode(“utf-8”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L4853) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L458)

<a id="op-997a533ddf19f3"></a>
### Index Warning.str

`operation_foundation_search_sqlite_search_business_behavior_index_warning_text`

**Inputs** self.

**Explicit results** self.message.

**Local steps**

- Return self.message.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L5033) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L457)

<a id="op-b59a3501611853"></a>
### SQLite Search.scoring function

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_scoring_function`

**Inputs** func.

**Wrappers, in declaration order** staticmethod.

**Explicit results** func.

**Local steps**

- Set func.\_is\_scoring\_function from true.
- Return func.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L5074) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L514)

<a id="op-be4dd1bfa7e761"></a>
### SQLite Search.initialize

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_initialize`

**Inputs** self, db\_name = no value.

**Explicit failure paths** ValueError(“INDEX\_SCHEMA must be defined as a class-level variable”) · ValueError(“INDEXABLE\_DOCTYPES must be defined as a class-level variable”).

**Local steps**

- If db\_name is identical to no value.
  - Set db\_name from getattr(self, “INDEX\_NAME”, “search.db”).
- Set self.db\_name from db\_name.
- Set self.db\_path from self.\_get\_db\_path().
- If not hasattr(self, “INDEX\_SCHEMA”).
  - Raise ValueError(“INDEX\_SCHEMA must be defined as a class-level variable”).
- If not hasattr(self, “INDEXABLE\_DOCTYPES”).
  - Raise ValueError(“INDEXABLE\_DOCTYPES must be defined as a class-level variable”).
- Set self.doc\_configs from self.\_build\_doc\_configs().
- Set self.warnings from list().
- Set self.schema from self.\_get\_schema().
- Evaluate self.\_validate\_config().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get db path](operations-064.md#op-8beb4b31c64d76), [build doc configs](operations-062.md#op-40169e323f6e0a), [get schema](operations-062.md#op-71db8438f518df), [validate config](operations-064.md#op-a841abed69d226).

**Values supplied outside this operation** selected callable from getattr(self, “INDEX\_NAME”, “search.db”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L5133) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L496)

<a id="op-216b2b971f75c4"></a>
### SQLite Search.parse doctype fields

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_parse_record_type_fields`

**Inputs** self, doctype, config.

**Explicit results** tuple(parsed\_fields, field\_mappings).

**Explicit failure paths** ValueError(formatted text Missing 'fields' in configuration for doctype '{doctype}') · ValueError(formatted text Invalid field definition: {field\_def}).

**Local steps**

- If “fields” does not belong to config.
  - Raise ValueError(formatted text Missing 'fields' in configuration for doctype '{doctype}').
- Set parsed\_fields from list().
- Set field\_mappings from mapping().
- For each field\_def in config at “fields”.
  - If isinstance(field\_def, str).
    - Evaluate parsed\_fields.append(field\_def).
  - Otherwise.
    - If isinstance(field\_def, dict).
      - For each tuple(schema\_field, doctype\_field) in field\_def.items().
        - Evaluate parsed\_fields.append(doctype\_field).
        - Set field\_mappings at schema\_field from doctype\_field.
    - Otherwise.
      - Raise ValueError(formatted text Invalid field definition: {field\_def}).
- Return tuple(parsed\_fields, field\_mappings).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L5479) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L506)

<a id="op-40169e323f6e0a"></a>
### SQLite Search.build doc configs

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_build_record_configurations`

**Inputs** self.

**Explicit results** doc\_configs.

**Explicit failure paths** ValueError(formatted text Content field must be present in fields list or explicitly mapped for '{doctype}').

**Local steps**

- Set doc\_configs from mapping().
- For each tuple(doctype, config) in self.INDEXABLE\_DOCTYPES.items().
  - Set tuple(parsed\_fields, field\_mappings) from self.\_parse\_doctype\_fields(doctype, config).
  - Set content\_field from field\_mappings.get(“content”).
  - If not content\_field.
    - If “content” belongs to parsed\_fields.
      - Set content\_field from “content”.
    - Otherwise.
      - Raise ValueError(formatted text Content field must be present in fields list or explicitly mapped for '{doctype}').
  - Set title\_field from field\_mappings.get(“title”).
  - If (not title\_field and “title” belongs to parsed\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not title\_field → “title” belongs to parsed\_fields.
    - Set title\_field from “title”.
  - Set doc\_configs at doctype from mapping(“fields” → parsed\_fields, “field\_mappings” → field\_mappings, “content\_field” → content\_field, “title\_field” → title\_field, …).
- Return doc\_configs.

**Methods declared on this owner** [parse doctype fields](operations-062.md#op-216b2b971f75c4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L5856) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L463)

<a id="op-71db8438f518df"></a>
### SQLite Search.get schema

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_schema`

**Inputs** self.

**Explicit results** schema.

**Explicit failure paths** ValueError(“INDEX\_SCHEMA must be defined as a class-level variable”).

**Local steps**

- If not hasattr(self, “INDEX\_SCHEMA”).
  - Raise ValueError(“INDEX\_SCHEMA must be defined as a class-level variable”).
- Set schema from self.INDEX\_SCHEMA.copy().
- Evaluate schema.setdefault(“text\_fields”, list(“title”, “content”)).
- Evaluate schema.setdefault(“tokenizer”, “unicode61 remove\_diacritics 2”).
- Set metadata\_fields from schema.setdefault(“metadata\_fields”, list()).
- Set required\_fields from list(“doctype”, “name”).
- For each field in required\_fields.
  - If field does not belong to metadata\_fields.
    - Evaluate metadata\_fields.append(field).
- Set is\_modified\_in\_schema from “modified” belongs to self.INDEX\_SCHEMA.get(“metadata\_fields”, list()).
- Set is\_modified\_in\_doctypes from any(generator of (“modified” belongs to config.get(“field\_mappings”, mapping()) or “modified” belongs to config.get(“fields”, list())) for config drawn from self.doc\_configs.values()).
  - Draw config from self.doc\_configs.values().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “modified” belongs to config.get(“field\_mappings”, mapping()) → “modified” belongs to config.get(“fields”, list()).
- If ((is\_modified\_in\_schema or is\_modified\_in\_doctypes) and “modified” does not belong to metadata\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (is\_modified\_in\_schema or is\_modified\_in\_doctypes) → “modified” does not belong to metadata\_fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_modified\_in\_schema → is\_modified\_in\_doctypes.
  - Evaluate metadata\_fields.append(“modified”).
- Set schema at “metadata\_fields” from metadata\_fields.
- Return schema.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L6377) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L486)

<a id="op-f563066859cf64"></a>
### SQLite Search.get search filters

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_search_filters`

**Inputs** self.

**Wrappers, in declaration order** abstractmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L6987) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L488)

<a id="op-9924d8ed39210a"></a>
### SQLite Search.search

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_search`

**Inputs** self, query, title\_only = false, filters = no value.

**Explicit results** self.\_empty\_search\_result(title\_only, filters) · mapping(“results” → processed\_results, “summary” → mapping(“duration” → round(duration, 3), “total\_matches” → total\_matches, “returned\_matches” → total\_matches, “corrected\_words” → corrections, …)).

**Local steps**

- If not self.is\_search\_enabled().
  - Return self.\_empty\_search\_result(title\_only, filters).
- Evaluate self.raise\_if\_not\_indexed().
- If not query.
  - Return self.\_empty\_search\_result(title\_only, filters).
- Set start\_time from time.time().
- Set filters from (filters or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set permission\_filters from self.get\_search\_filters().
- Set all\_filters from mapping(expand filters, expand permission\_filters).
- Set tuple(expanded\_query, corrections) from self.\_expand\_query\_with\_corrections(query).
- Set fts\_query from self.\_prepare\_fts\_query(expanded\_query).
- Attempt the following.
  - Set raw\_results from self.\_execute\_search\_query(fts\_query, title\_only, all\_filters).
  - Set total\_matches from len(raw\_results).
- On failure (sqlite3.Error) bound to e.
  - Evaluate Platform.log\_error(formatted text Search query failed: {e}).
  - Set raw\_results from list().
  - Set total\_matches from 0.
- Set processed\_results from self.\_process\_search\_results(raw\_results, query).
- Set duration from (time.time() − start\_time).
- Return mapping(“results” → processed\_results, “summary” → mapping(“duration” → round(duration, 3), “total\_matches” → total\_matches, “returned\_matches” → total\_matches, “corrected\_words” → corrections, …)).
  - Value choice on corrections — true gives expanded\_query, false gives no value.

**Methods declared on this owner** [is search enabled](operations-063.md#op-4ac038433379a7), [empty search result](operations-064.md#op-bc0359069fdc9d), [raise if not indexed](operations-063.md#op-a2bfedee778786), [get search filters](operations-062.md#op-f563066859cf64), [expand query with corrections](operations-064.md#op-a221af3b0587db), [prepare fts query](operations-064.md#op-c374de2d0959d7), [execute search query](operations-063.md#op-fc0ae34ca80dca), [process search results](operations-063.md#op-65afda86ba561f).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L7025) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L515)

<a id="op-65103bae6d0b96"></a>
### SQLite Search.build index

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_build_index`

**Inputs** self, batch\_size = 1000, is\_continuation = false.

**Explicit results** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- If not self.is\_search\_enabled().
  - Return no value.
- Set temp\_db\_path from no value.
- Set original\_db\_path from self.db\_path.
- If (not is\_continuation and not self.index\_exists()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_continuation → not self.index\_exists().
  - Set temp\_db\_path from self.\_get\_db\_path(is\_temp = true).
  - If os.path.exists(temp\_db\_path).
    - Evaluate os.unlink(temp\_db\_path).
  - Set self.db\_path from temp\_db\_path.
- Otherwise.
  - If is\_continuation.
    - Set potential\_temp\_path from self.\_get\_db\_path(is\_temp = true).
    - If os.path.exists(potential\_temp\_path).
      - Set temp\_db\_path from potential\_temp\_path.
      - Set self.db\_path from temp\_db\_path.
      - Evaluate print(formatted text Continuation: Using temporary database {temp\_db\_path}).
    - Otherwise.
      - Evaluate print(formatted text Continuation: Using regular database {self.db\_path}).
- If temp\_db\_path.
  - Evaluate print(formatted text Working with temporary database: {self.db\_path}).
- Otherwise.
  - Evaluate print(formatted text Working with regular database: {self.db\_path}).
- Attempt the following.
  - If (not is\_continuation or (temp\_db\_path and not self.\_tables\_exist())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_continuation → (temp\_db\_path and not self.\_tables\_exist()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in temp\_db\_path → not self.\_tables\_exist().
    - Evaluate self.\_update\_progress(“Setting up search tables”, 0, 100, absolute = true).
    - Evaluate self.\_ensure\_fts\_table().
    - If (temp\_db\_path and not is\_continuation).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in temp\_db\_path → not is\_continuation.
      - Evaluate self.\_with\_connection(deferred anonymous expression).
    - If not is\_continuation.
      - Evaluate self.\_initialize\_index\_progress().
  - Set progress from self.\_get\_index\_progress().
  - Set started\_at from self.\_build\_started\_at(is\_continuation, progress).
  - If self.\_is\_indexing\_complete().
    - Evaluate self.\_update\_progress(“Search index already complete”, 100, 100, absolute = true).
    - Return no value.
  - Set total\_doctypes from len(self.doc\_configs).
  - Set processed\_doctypes from 0.
  - For each doctype in self.doc\_configs.keys().
    - Set doctype\_progress from progress.get(doctype, mapping()).
    - If doctype\_progress.get(“is\_complete”).
      - Update processed\_doctypes using + 1.
      - Continue with the next iteration or loop test.
    - Evaluate self.\_update\_progress(formatted text Indexing {doctype}, (20 + ((processed\_doctypes × 60) floor divide total\_doctypes)), 100, absolute = true).
    - Set last\_indexed\_modified from doctype\_progress.get(“last\_indexed\_modified”).
    - Set last\_indexed\_name from doctype\_progress.get(“last\_indexed\_name”).
    - Set progress\_field from “creation”.
    - Set batch\_count from 0.
    - While true.
      - Set docs from self.get\_documents\_paginated(doctype, limit = batch\_size, last\_indexed\_modified = last\_indexed\_modified, last\_indexed\_name = last\_indexed\_name).
      - If not docs.
        - Evaluate self.\_mark\_doctype\_complete(doctype).
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Set documents from list().
      - For each doc in docs.
        - Set document from self.prepare\_document(doc).
        - If document.
          - Evaluate documents.append(document).
      - If documents.
        - Evaluate self.\_index\_documents(documents).
      - Set last\_doc\_modified from (docs at negative 1.get(progress\_field) or docs at negative 1.get(“modified”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in docs at negative 1.get(progress\_field) → docs at negative 1.get(“modified”).
      - Set last\_doc\_name from docs at negative 1 at “name”.
      - Evaluate self.\_update\_index\_progress(doctype, last\_doc\_name, last\_doc\_modified, len(documents)).
      - Set last\_indexed\_modified from last\_doc\_modified.
      - Set last\_indexed\_name from last\_doc\_name.
      - Update batch\_count using + 1.
      - Set tuple(indexed\_docs, total\_docs) from self.\_get\_indexing\_progress().
      - If total\_docs &gt; 0.
        - Set progress\_percent from (20 + ((indexed\_docs × 60) floor divide total\_docs)).
        - Evaluate self.\_update\_progress(formatted text Indexing {doctype} {indexed\_docs}/{total\_docs}, progress\_percent, 100, absolute = true).
    - Update processed\_doctypes using + 1.
  - If not self.\_is\_vocabulary\_built\_needed().
    - If self.BUILD\_VOCABULARY.
      - Evaluate self.\_update\_progress(“All documents indexed, building vocabulary”, 80, 100, absolute = true).
      - Evaluate self.\_build\_vocabulary\_incremental().
    - Evaluate self.\_mark\_vocabulary\_built().
  - If (temp\_db\_path and os.path.exists(temp\_db\_path)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in temp\_db\_path → os.path.exists(temp\_db\_path).
    - If os.path.exists(original\_db\_path).
      - Evaluate os.unlink(original\_db\_path).
    - Evaluate os.rename(temp\_db\_path, original\_db\_path).
  - Evaluate self.\_update\_progress(“Search index build complete”, 100, 100, absolute = true).
  - Evaluate self.\_print\_warning\_summary().
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(title = “Search Index Build Error”, message = formatted text Error during search index build: {e}).
  - Propagate the active failure.
- On exit, including pending return or failure.
  - If temp\_db\_path.
    - Set self.db\_path from original\_db\_path.
- Evaluate self.index\_documents\_changed\_during\_build(started\_at).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is search enabled](operations-063.md#op-4ac038433379a7), [index exists](operations-063.md#op-85f92f011f4cf6), [get db path](operations-064.md#op-8beb4b31c64d76), [tables exist](operations-063.md#op-8f55ea74f8f63e), [update progress](operations-064.md#op-e65a7521912fc6), [ensure fts table](operations-064.md#op-d44c483891f8ab), [with connection](operations-064.md#op-e830239468f74c), [initialize index progress](operations-063.md#op-91cfd471fbecb7), [get index progress](operations-063.md#op-be713d777f7bb0), [build started at](operations-062.md#op-272a433628d045), [is indexing complete](operations-063.md#op-d4283f37e664db), [get documents paginated](operations-063.md#op-772603ba9cdcd1), [mark doctype complete](operations-063.md#op-cfeceadb16b4b7), [prepare document](operations-064.md#op-6673d531411397), [index documents](operations-064.md#op-f1390aa983b0e9), [update index progress](operations-063.md#op-9fca457ee949d9), [get indexing progress](operations-063.md#op-04ceac472c8f55), [is vocabulary built needed](operations-062.md#op-334667e6cfba7b), [build vocabulary incremental](operations-062.md#op-2931cd9772c42a), [mark vocabulary built](operations-063.md#op-17e7e74cf9d42a), [print warning summary](operations-065.md#op-271bcb767a3f92), [index documents changed during build](operations-062.md#op-61d968b7512b51).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L16) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L462)

<a id="op-272a433628d045"></a>
### SQLite Search.build started at

`operation_foundation_binding_foundation_search_sqlite_search_sqlitesearch_build_started_at`

**Inputs** self, is\_continuation, progress.

**Explicit results** convert\_utc\_to\_system\_timezone(get\_datetime(min(stamps))).replace(tzinfo = no value) · now\_datetime().

**Local steps**

- If is\_continuation.
  - Set stamps from list of row at “started\_at” for row drawn from progress.values() where row.get(“started\_at”).
    - Draw row from progress.values(), keep a combination only if (row.get(“started\_at”)).
  - If stamps.
    - Return convert\_utc\_to\_system\_timezone(get\_datetime(min(stamps))).replace(tzinfo = no value).
- Return now\_datetime().

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L47) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1710)

<a id="op-61d968b7512b51"></a>
### SQLite Search.index documents changed during build

`operation_foundation_binding_foundation_search_sqlite_search_sqlitesearch_index_documents_changed_during_build`

**Inputs** self, started\_at, batch\_size = 1000.

**Record and data access** read doctype via get\_all.

**Explicit results** no value.

**Local steps**

- If not self.index\_exists().
  - Return no value.
- For each tuple(doctype, config) in self.doc\_configs.items().
  - Set filters from dict((config.get(“filters”) or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in config.get(“filters”) → mapping().
  - Set filters at “modified” from tuple(“&gt;=”, started\_at).
  - Set names from Platform.get\_all(doctype, filters = filters, pluck = “name”).
  - For each start in range(0, len(names), batch\_size).
    - Evaluate self.index\_documents\_by\_name(doctype, names at slice start to (start + batch\_size)).
  - Evaluate self.remove\_documents\_deleted\_during\_build(doctype, started\_at).

If control reaches the end, it returns no value.

**Methods declared on this owner** [index exists](operations-063.md#op-85f92f011f4cf6), [index documents by name](operations-062.md#op-fde62305aabe66), [remove documents deleted during build](operations-062.md#op-dd09da3e45644d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L49) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1712)

<a id="op-fde62305aabe66"></a>
### SQLite Search.index documents by name

`operation_foundation_binding_foundation_search_sqlite_search_sqlitesearch_index_documents_by_name`

**Inputs** self, doctype, names.

**Explicit results** no value.

**Local steps**

- If not names.
  - Return no value.
- Set config from self.doc\_configs at doctype.
- Set fields from list(config at “fields”).
- For each required in tuple(“name”, “modified”).
  - If required does not belong to fields.
    - Evaluate fields.append(required).
- Set docs from Platform.qb.get\_query(doctype, fields = fields, filters = mapping(“name” → tuple(“in”, names))).run(as\_dict = true).
- Set documents from list().
- For each doc in docs.
  - Set doc.doctype from doctype.
  - If config at “modified\_field” differs from “modified”.
    - Set doc.modified from (getattr(doc, config at “modified\_field”, no value) or doc.modified).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(doc, config at “modified\_field”, no value) → doc.modified.
  - Set document from self.prepare\_document(doc).
  - If document.
    - Evaluate documents.append(document).
- If documents.
  - Evaluate self.\_index\_documents(documents).

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare document](operations-064.md#op-6673d531411397), [index documents](operations-064.md#op-f1390aa983b0e9).

**Values supplied outside this operation** selected callable from getattr(doc, config at “modified\_field”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L48) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1711)

<a id="op-dd09da3e45644d"></a>
### SQLite Search.remove documents deleted during build

`operation_foundation_binding_foundation_search_sqlite_search_sqlitesearch_remove_documents_deleted_during_build`

**Inputs** self, doctype, started\_at.

**Record and data access** read “Deleted Document” via get\_all.

**Local steps**

- Set deleted from Platform.get\_all(“Deleted Document”, filters = mapping(“deleted\_doctype” → doctype, “creation” → tuple(“&gt;=”, started\_at)), pluck = “deleted\_name”).
- For each name in deleted.
  - Evaluate self.remove\_doc(doctype, name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove doc](operations-064.md#op-2a36c53f9b71e7).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L50) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1713)

<a id="op-8ca9f9133c4dc2"></a>
### SQLite Search.get incomplete count

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_incomplete_count`

**Inputs** self, where\_clause.

**Explicit results** result at 0 at “incomplete\_count” · negative 1.

**Local steps**

- Attempt the following.
  - Set result from self.sql(formatted text   SELECT COUNT(\*) as incomplete\_count  FROM search\_index\_progress  WHERE {where\_clause}  , read\_only = true).
  - Return result at 0 at “incomplete\_count”.
- On failure (sqlite3.Error).
  - Return negative 1.

**Methods declared on this owner** [sql](operations-064.md#op-98c6c287adfbb9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L2234) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L482)

<a id="op-334667e6cfba7b"></a>
### SQLite Search.is vocabulary built needed

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_is_vocabulary_built_needed`

**Inputs** self.

**Explicit results** count &gt; 0 when count ≥ 0, otherwise true.

**Local steps**

- Set count from self.\_get\_incomplete\_count(“is\_complete = 0”).
- Return count &gt; 0 when count ≥ 0, otherwise true.
  - Value choice on count ≥ 0 — true gives count &gt; 0, false gives true.

**Methods declared on this owner** [get incomplete count](operations-062.md#op-8ca9f9133c4dc2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L2424) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L501)

<a id="op-2931cd9772c42a"></a>
### SQLite Search.build vocabulary incremental

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_build_vocabulary_incremental`

**Inputs** self.

**Local steps**

- Bind dependencies re.
- Set word\_freq from defaultdict(int).
- Set word\_regex from re.compile(“\\w+”).
- Set batch\_size from 1000.
- Set offset from 0.
- While true.
  - Attempt the following.
    - Set documents from self.sql(formatted text   SELECT title, content  FROM search\_fts  LIMIT {batch\_size} OFFSET {offset}  , read\_only = true).
    - If not documents.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - For each tuple(i, doc) in enumerate(documents).
      - If ((offset + i) modulo or format 1000) equals 0.
        - Evaluate self.\_update\_progress(formatted text Processing vocabulary ({(offset + i)} docs), 85, 100, absolute = true).
      - Set combined\_text from one space.join(list((doc at “title” or empty text).lower(), (doc at “content” or empty text).lower())).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc at “title” → empty text.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc at “content” → empty text.
      - Set words from word\_regex.findall(combined\_text).
      - For each word in words.
        - If (len(word) &gt; (MIN\_WORD\_LENGTH − 1) and word.isalpha()).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(word) &gt; (MIN\_WORD\_LENGTH − 1) → word.isalpha().
          - Update word\_freq at word using + 1.
    - Update offset using + batch\_size.
  - On failure (sqlite3.Error).
    - Leave the innermost loop without its normal-exhaustion alternative.
- If word\_freq.
  - Bind local operation clear\_vocabulary for subsequent calls.
  - Evaluate self.\_with\_connection(clear\_vocabulary).
  - Set vocab\_data from list().
  - Set trigram\_data from list().
  - Set trigram\_set from set().
  - For each tuple(word, freq) in word\_freq.items().
    - Evaluate vocab\_data.append(tuple(word, freq, len(word))).
    - Set trigrams from self.\_generate\_trigrams(word).
    - For each trigram in trigrams.
      - Set trigram\_key from tuple(trigram, word).
      - If trigram\_key does not belong to trigram\_set.
        - Evaluate trigram\_set.add(trigram\_key).
        - Evaluate trigram\_data.append(trigram\_key).
  - Bind local operation insert\_vocabulary for subsequent calls.
  - Evaluate self.\_with\_connection(insert\_vocabulary).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sql](operations-064.md#op-98c6c287adfbb9), [update progress](operations-064.md#op-e65a7521912fc6), [with connection](operations-064.md#op-e830239468f74c), [generate trigrams](operations-065.md#op-3228b89b8ea7e0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L2528) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L464)

<a id="op-9a2160a4933812"></a>
### SQLite Search.build vocabulary incremental.clear vocabulary

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_build_vocabulary_incremental_clear_vocabulary`

**Inputs** cursor.

**Local steps**

- Evaluate cursor.execute(query text (DELETE)).
- Evaluate cursor.execute(query text (DELETE)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L7536) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L465)
