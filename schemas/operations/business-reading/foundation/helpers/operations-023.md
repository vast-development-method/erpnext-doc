# Shared value and file services · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Global search

<a id="op-02a99f945907d4"></a>
### Get doctypes with global search.get

`operation_foundation_utils_global_search_business_behavior_get_record_types_with_global_search_get`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all.

**Explicit results** doctypes.

**Local steps**

- Set global\_search\_doctypes from list().
- Set filters from mapping().
- If not with\_child\_tables.
  - Set filters from mapping(“istable” → list(“!=”, 1), “issingle” → list(“!=”, 1)).
- For each d in Platform.get\_all(“DocType”, fields = list(“name”, “module”), filters = filters).
  - Set meta from Platform.get\_meta(d.name).
  - If len(meta.get\_global\_search\_fields()) &gt; 0.
    - Evaluate global\_search\_doctypes.append(d).
- Set installed\_apps from Platform.get\_installed\_apps().
- Set module\_app from Platform.local.module\_app.
- Set doctypes from list of d.name for d drawn from global\_search\_doctypes where (module\_app.get(Platform.scrub(d.module)) and module\_app at Platform.scrub(d.module) belongs to installed\_apps).
  - Draw d from global\_search\_doctypes, keep a combination only if ((module\_app.get(Platform.scrub(d.module)) and module\_app at Platform.scrub(d.module) belongs to installed\_apps)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in module\_app.get(Platform.scrub(d.module)) → module\_app at Platform.scrub(d.module) belongs to installed\_apps.
- Return doctypes.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L116) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L158)

<a id="op-3fd8bf126c2222"></a>
### Rebuild for doctype

`operation_foundation_utils_global_search_business_behavior_rebuild_for_record_type`

**Inputs** doctype.

**Record and data access** read “DocField” via get\_all · read doctype via get\_all · resolve a document from doctype via get\_doc.

**Explicit results** no value.

**Local steps**

- If Platform.local.conf.get(“disable\_global\_search”).
  - Return no value.
- Bind local operation \_get\_filters for subsequent calls.
- Set meta from Platform.get\_meta(doctype).
- If cint(meta.issingle) equals 1.
  - Return no value.
- If cint(meta.istable) equals 1.
  - Set parent\_doctypes from Platform.get\_all(“DocField”, fields = “parent”, filters = mapping(“fieldtype” → list(“in”, Platform.model.table\_fields), “options” → doctype)).
  - For each p in parent\_doctypes.
    - Evaluate rebuild\_for\_doctype(p.parent).
  - Return no value.
- Evaluate delete\_global\_search\_records\_for\_doctype(doctype).
- Set parent\_search\_fields from meta.get\_global\_search\_fields().
- Set fieldnames from get\_selected\_fields(meta, parent\_search\_fields).
- Set all\_records from Platform.get\_all(doctype, fields = fieldnames, filters = \_get\_filters()).
- Set tuple(all\_children, child\_search\_fields) from get\_children\_data(doctype, meta).
- Set all\_contents from list().
- For each doc in all\_records.
  - Set content from list().
  - For each field in parent\_search\_fields.
    - Set value from doc.get(field.fieldname).
    - If value.
      - Evaluate content.append(get\_formatted\_value(value, field)).
  - For each tuple(child\_doctype, records) in all\_children.get(doc.name, mapping()).items().
    - For each field in child\_search\_fields.get(child\_doctype).
      - For each r in records.
        - If r.get(field.fieldname).
          - Evaluate content.append(get\_formatted\_value(r.get(field.fieldname), field)).
  - If content.
    - Set published from 0.
    - Set tuple(title, route) from tuple(empty text, empty text).
    - Attempt the following.
      - If (hasattr(get\_controller(doctype), “is\_website\_published”) and meta.allow\_guest\_to\_view).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(get\_controller(doctype), “is\_website\_published”) → meta.allow\_guest\_to\_view.
        - Set d from Platform.get\_doc(doctype, doc.name).
        - Set published from 1 when d.is\_website\_published(), otherwise 0.
          - Value choice on d.is\_website\_published() — true gives 1, false gives 0.
        - Set title from d.get\_title().
        - Set route from d.get(“route”).
    - On failure (ImportError).
      - Take no action here.
    - Evaluate all\_contents.append(mapping(“doctype” → Platform.db.escape(doctype), “name” → Platform.db.escape(doc.name), “content” → Platform.db.escape(“ \|\|\| ”.join((content or empty text))), “published” → published, …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → empty text.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → empty text.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in route → empty text.
- If all\_contents.
  - Evaluate insert\_values\_for\_multiple\_docs(all\_contents).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L162)

<a id="op-6f1b3b52769d6b"></a>
### Rebuild for doctype.get filters

`operation_foundation_utils_global_search_business_behavior_rebuild_for_record_type_get_filters`

**Inputs** no declared parameters.

**Explicit results** filters.

**Local steps**

- Set filters from Platform.\_dict(mapping(“docstatus” → list(“!=”, 2))).
- If meta.has\_field(“enabled”).
  - Set filters.enabled from 1.
- If meta.has\_field(“disabled”).
  - Set filters.disabled from 0.
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L1658) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L163)

<a id="op-38f77cf9ec2d04"></a>
### Delete global search records for doctype

`operation_foundation_utils_global_search_business_behavior_delete_global_search_records_for_record_type`

**Inputs** doctype.

**State and service calls** request delete on “\_\_global\_search”.

**Local steps**

- Evaluate Platform.db.delete(“\_\_global\_search”, mapping(“doctype” → doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L1838) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L152)

<a id="op-0aa66ea0fbea25"></a>
### Get selected fields

`operation_foundation_utils_global_search_business_behavior_get_selected_fields`

**Inputs** meta, global\_search\_fields.

**Explicit results** fieldnames.

**Local steps**

- Set fieldnames from list of df.fieldname for df drawn from global\_search\_fields.
  - Draw df from global\_search\_fields.
- If meta.istable equals 1.
  - Evaluate fieldnames.append(“parent”).
- Otherwise.
  - If “name” does not belong to fieldnames.
    - Evaluate fieldnames.append(“name”).
- If meta.has\_field(“is\_website\_published”).
  - Evaluate fieldnames.append(“is\_website\_published”).
- Return fieldnames.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L118) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L160)

<a id="op-cb29e19857cf9a"></a>
### Get children data

`operation_foundation_utils_global_search_business_behavior_get_children_data`

**Inputs** doctype, meta.

**Record and data access** read child.options via get\_all.

**Explicit results** tuple(all\_children, child\_search\_fields).

**Local steps**

- Set all\_children from Platform.\_dict().
- Set child\_search\_fields from Platform.\_dict().
- For each child in meta.get\_table\_fields().
  - Set child\_meta from Platform.get\_meta(child.options).
  - Set search\_fields from child\_meta.get\_global\_search\_fields().
  - If search\_fields.
    - Evaluate child\_search\_fields.setdefault(child.options, search\_fields).
    - Set child\_fieldnames from get\_selected\_fields(child\_meta, search\_fields).
    - Set child\_records from Platform.get\_all(child.options, fields = child\_fieldnames, filters = mapping(“docstatus” → list(“!=”, 2), “parenttype” → doctype)).
    - For each record in child\_records.
      - Evaluate all\_children.setdefault(record.parent, nested operand in the contract.\_dict()).setdefault(child.options, list()).append(record).
- Return tuple(all\_children, child\_search\_fields).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L2166) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L153)

<a id="op-5ab6c6c66e3ac7"></a>
### Insert values for multiple docs

`operation_foundation_utils_global_search_business_behavior_insert_values_for_multiple_records`

**Inputs** all\_contents.

**Local steps**

- Set values from list of “({doctype}, {name}, {content}, {published}, {title}, {route})”.format(expanded names content) for content drawn from all\_contents.
  - Draw content from all\_contents.
- Set batch\_size from 50000.
- For each i in range(0, len(values), batch\_size).
  - Set batch\_values from values at slice i to (i + batch\_size).
  - Evaluate Platform.db.multisql(mapping(“mariadb” → query text (INSERT).format(“, ”.join(batch\_values)), “postgres” → query text (INSERT).format(“, ”.join(batch\_values)), “sqlite” → “INSERT OR IGNORE INTO ′\_\_global\_s ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L2617) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L161)

<a id="op-f7a64dd4e1c6d1"></a>
### Update global search

`operation_foundation_utils_global_search_business_behavior_update_global_search`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If Platform.local.conf.get(“disable\_global\_search”).
  - Return no value.
- If (doc.docstatus &gt; 1 or (doc.meta.has\_field(“enabled”) and not doc.get(“enabled”)) or doc.get(“disabled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.docstatus &gt; 1 → (doc.meta.has\_field(“enabled”) and not doc.get(“enabled”)) → doc.get(“disabled”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.has\_field(“enabled”) → not doc.get(“enabled”).
  - Return no value.
- Set content from list of get\_formatted\_value(doc.get(field.fieldname), field) for field drawn from doc.meta.get\_global\_search\_fields() where (doc.get(field.fieldname) and field.fieldtype does not belong to Platform.model.t ….
  - Draw field from doc.meta.get\_global\_search\_fields(), keep a combination only if ((doc.get(field.fieldname) and field.fieldtype does not belong to Platform.model.table\_fields)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(field.fieldname) → field.fieldtype does not belong to Platform.model.table\_fields.
- For each child in doc.meta.get\_table\_fields().
  - For each d in doc.get(child.fieldname).
    - If d.parent equals doc.name.
      - Evaluate content.extend(generator of get\_formatted\_value(d.get(field.fieldname), field) for field drawn from d.meta.get\_global\_search\_fields() where d.get(field.fieldname)).
        - Draw field from d.meta.get\_global\_search\_fields(), keep a combination only if (d.get(field.fieldname)).
- If content.
  - Set published from 0.
  - If (hasattr(doc, “is\_website\_published”) and doc.meta.allow\_guest\_to\_view).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(doc, “is\_website\_published”) → doc.meta.allow\_guest\_to\_view.
    - Set published from 1 when doc.is\_website\_published(), otherwise 0.
      - Value choice on doc.is\_website\_published() — true gives 1, false gives 0.
  - Set title from (cstr(doc.get\_title()) or empty text) at slice no value to int(Platform.db.VARCHAR\_LEN).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(doc.get\_title()) → empty text.
  - Set route from doc.get(“route”) when doc, otherwise empty text.
    - Value choice on doc — true gives doc.get(“route”), false gives empty text.
  - Set value from dict(doctype = doc.doctype, name = doc.name, content = “ \|\|\| ”.join((content or empty text)), published = published, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in content → empty text.
  - Evaluate sync\_value\_in\_queue(value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L3047) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L172)

<a id="op-3bd858925b3693"></a>
### Update global search for all web pages

`operation_foundation_utils_global_search_business_behavior_update_global_search_for_all_web_pages`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If Platform.conf.get(“disable\_global\_search”).
  - Return no value.
- Evaluate print(“Update global search for all web pages...”).
- Set routes\_to\_index from get\_routes\_to\_index().
- For each route in routes\_to\_index.
  - Evaluate add\_route\_to\_global\_search(route).
- Evaluate sync\_global\_search().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L3963) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L173)

<a id="op-7e02a9d6550857"></a>
### Get routes to index

`operation_foundation_utils_global_search_business_behavior_get_routes_to_index`

**Inputs** no declared parameters.

**Explicit results** routes\_to\_index.

**Local steps**

- Set apps from Platform.get\_installed\_apps().
- Set routes\_to\_index from list().
- For each app in apps.
  - Set base from Platform.get\_app\_path(app, “www”).
  - Set path\_to\_index from Platform.get\_app\_path(app, “www”).
  - For each tuple(dirpath, \_, filenames) in os.walk(path\_to\_index, topdown = true).
    - For each f in filenames.
      - If f.endswith(tuple(“.md”, “.html”)).
        - Set filepath from os.path.join(dirpath, f).
        - Set route from os.path.relpath(filepath, base).
        - Set route from route.split(“.”, 1) at 0.
        - If route.endswith(“index”).
          - Set route from route.rsplit(“index”, 1) at 0.
        - Evaluate routes\_to\_index.append(route).
- Return routes\_to\_index.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L117) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L159)

<a id="op-09fd0e5830864b"></a>
### Add route to global search

`operation_foundation_utils_global_search_business_behavior_add_route_to_global_search`

**Inputs** route.

**Local steps**

- Bind dependencies BeautifulSoup.
- Bind dependencies set\_request.
- Bind dependencies get\_response\_content.
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
  - Set value from dict(doctype = “Static Web Page”, name = route, content = text\_content, published = 1, …).
  - Evaluate sync\_value\_in\_queue(value).
- On failure (Exception).
  - Take no action here.
- Evaluate Platform.set\_user(“Administrator”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L4580) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L150)

<a id="op-871303871e3ac8"></a>
### Get formatted value

`operation_foundation_utils_global_search_business_behavior_get_formatted_value`

**Inputs** value, field.

**Explicit results** ((field.label + “ : ”) + strip\_html\_tags(str(value))).

**Local steps**

- If getattr(field, “fieldtype”, no value) belongs to list(“Text”, “Text Editor”).
  - Set value from unescape\_html(Platform.safe\_decode(value)).
  - Set value from HTML\_TAGS\_PATTERN.subn(empty text, str(value)) at 0.
  - Set value from one space.join(value.split()).
- Return ((field.label + “ : ”) + strip\_html\_tags(str(value))).

**Values supplied outside this operation** selected callable from getattr(field, “fieldtype”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L5027) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L156)

<a id="op-4b640b4dd8091a"></a>
### Sync global search

`operation_foundation_utils_global_search_business_behavior_sync_global_search`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies islice.
- Bind local operation get\_search\_queue\_item\_generator for subsequent calls.
- Set item\_generator from get\_search\_queue\_item\_generator().
- While search\_items bound to tuple(islice(item\_generator, 1000)).
  - Set values from \_get\_deduped\_search\_item\_values(search\_items).
  - Evaluate sync\_values(values).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L5310) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L167)

<a id="op-a169e65eed3d50"></a>
### Sync global search.get search queue item generator

`operation_foundation_utils_global_search_business_behavior_sync_global_search_get_search_queue_item_generator`

**Inputs** no declared parameters.

**Local steps**

- While value bound to Platform.cache.rpop(“global\_search\_queue”).
  - yield value.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L5515) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L168)

<a id="op-3586b6866f6cdb"></a>
### Get deduped search item values

`operation_foundation_utils_global_search_business_behavior_get_deduped_search_item_values`

**Inputs** items.

**Explicit results** values\_dict.values().

**Local steps**

- Bind dependencies OrderedDict.
- Set values\_dict from OrderedDict().
- For each item in items.
  - Set item\_json from item.decode(“utf-8”).
  - Set item\_dict from json.loads(item\_json).
  - Set key from tuple(item\_dict at “doctype”, item\_dict at “name”).
  - Set values\_dict at key from tuple(item\_dict.values()).
- Return values\_dict.values().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L114) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L154)

<a id="op-ff10ffe6ccb6e0"></a>
### Sync values

`operation_foundation_utils_global_search_business_behavior_sync_values`

**Inputs** values.

**State and service calls** call insert on Platform.qb.into(GlobalSearch).columns(list(“doctype”, “name”, expanded conflict\_fields)).

**Explicit failure paths** NotImplementedError.

**Local steps**

- Bind dependencies Values.
- Set GlobalSearch from Platform.qb.Table(“\_\_global\_search”).
- Set conflict\_fields from list(“content”, “published”, “title”, “route”).
- Set query from nested operand in the contract.qb.into(GlobalSearch).columns(list(“doctype”, “name”, expanded conflict\_fields)).insert(expanded values).
- If Platform.db.db\_type equals “postgres”.
  - Set query from query.on\_conflict(GlobalSearch.doctype, GlobalSearch.name).
- For each field in conflict\_fields.
  - If Platform.db.db\_type equals “mariadb”.
    - Set query from query.on\_duplicate\_key\_update(GlobalSearch at field, Values(field)).
  - Otherwise.
    - If Platform.db.db\_type equals “postgres”.
      - Set query from query.do\_update(GlobalSearch at field).
    - Otherwise.
      - Raise NotImplementedError.
- Evaluate query.run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L5873) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L171)

<a id="op-ffd0bd8a6e1c32"></a>
### Sync value in queue

`operation_foundation_utils_global_search_business_behavior_sync_value_in_queue`

**Inputs** value.

**Local steps**

- Attempt the following.
  - Evaluate Platform.cache.lpush(“global\_search\_queue”, json.dumps(value)).
- On failure (redis.exceptions.ConnectionError).
  - Require not Platform.flags.in\_test or report “Should not fail silently in tests”.
  - Evaluate sync\_value(value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L6364) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L170)

<a id="op-37a8a08bece58a"></a>
### Sync value

`operation_foundation_utils_global_search_business_behavior_sync_value`

**Inputs** value.

**Local steps**

- Evaluate Platform.db.multisql(mapping(“mariadb” → query text (INSERT), “postgres” → query text (INSERT), “sqlite” → multiline text in the contract), value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L6516) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L169)

<a id="op-be51a3ddd00e64"></a>
### Delete for document

`operation_foundation_utils_global_search_business_behavior_delete_for_document`

**Inputs** doc.

**State and service calls** request delete on “\_\_global\_search”.

**Local steps**

- Evaluate Platform.db.delete(“\_\_global\_search”, mapping(“doctype” → doc.doctype, “name” → doc.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0482.json#L6968) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L151)

<a id="op-a70e4c951e37a8"></a>
### Search

`operation_foundation_utils_global_search_business_behavior_search`

**Inputs** text, start = 0, limit = 20, doctype = empty text.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list() · sorted\_results.

**Local steps**

- Bind dependencies get\_doctypes\_for\_global\_search.
- Bind dependencies Match.
- Set results from list().
- Set sorted\_results from list().
- Set allowed\_doctypes from (set(get\_doctypes\_for\_global\_search()) bitwise and set(Platform.get\_user().get\_can\_read())).
- If (not allowed\_doctypes or (doctype and doctype does not belong to allowed\_doctypes)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not allowed\_doctypes → (doctype and doctype does not belong to allowed\_doctypes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → doctype does not belong to allowed\_doctypes.
  - Return list().
- For each word in set(text.split(“&amp;”)).
  - Set word from word.strip().
  - If not word.
    - Continue with the next iteration or loop test.
  - Set global\_search from Platform.qb.Table(“\_\_global\_search”).
  - Set rank from Match(global\_search.content).Against(word).
  - Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(rank).orderby(“rank”, order = Platform.q …(limit).
  - If doctype.
    - Set query from query.where(global\_search.doctype equals doctype).
  - Otherwise.
    - Set query from query.where(global\_search.doctype.isin(allowed\_doctypes)).
  - If cint(start) &gt; 0.
    - Set query from query.offset(start).
  - Set result from query.run(as\_dict = true).
  - Evaluate results.extend(result).
- For each doctype in allowed\_doctypes.
  - For each r in results.
    - If (r.doctype equals doctype and r.rank &gt; 0.0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in r.doctype equals doctype → r.rank &gt; 0.0.
      - Attempt the following.
        - Set meta from Platform.get\_meta(r.doctype).
        - Set doc from Platform.get\_lazy\_doc(r.doctype, r.name).
        - If meta.image\_field.
          - Set r.image from doc.get(meta.image\_field).
        - If meta.title\_field.
          - Set r.title from doc.get(meta.title\_field).
        - If Platform.has\_permission(r.doctype, doc = doc).
          - Evaluate sorted\_results.append(r).
      - On failure (Exception).
        - Evaluate Platform.clear\_messages().
- Return sorted\_results.

**Values supplied outside this operation** effective access from Platform.has\_permission(r.doctype, doc = doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L119) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L165)

<a id="op-ffda00a453c8a1"></a>
### Web search

`operation_foundation_utils_global_search_business_behavior_web_search`

**Inputs** text, scope = no value, start = 0, limit = 20.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Explicit results** results at slice no value to WEB\_SEARCH\_MAX\_LIMIT.

**Local steps**

- Set limit from max(0, min(cint(limit), WEB\_SEARCH\_MAX\_LIMIT)).
- Set start from max(0, cint(start)).
- Set text from (text or empty text) at slice no value to WEB\_SEARCH\_MAX\_TEXT\_LENGTH.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in text → empty text.
- Set results from list().
- Set texts from list(dict.fromkeys(generator of t for t drawn from text.split(“&amp;”) where t.strip())) at slice no value to WEB\_SEARCH\_MAX\_SEGMENTS.
  - Draw t from text.split(“&amp;”), keep a combination only if (t.strip()).
- For each text in texts.
  - Set common\_query from query text (SELECT).
  - Set scope\_condition from “′route′ like %(scope)s AND ” when scope, otherwise empty text.
    - Value choice on scope — true gives “′route′ like %(scope)s AND ”, false gives empty text.
  - Set published\_condition from “′published′ = 1 AND ”.
  - Set mariadb\_conditions, postgres\_conditions from one space.join(list(published\_condition, scope\_condition)).
  - Update mariadb\_conditions using + “MATCH(′content′) AGAINST ({} IN BOOLEAN MODE)”.format(Platform.db.escape(((“+” + text) + “\*”))).
  - Update postgres\_conditions using + formatted text TO\_TSVECTOR("content") @@ PLAINTO\_TSQUERY({Platform.db.escape(text)}).
  - Set values from mapping(“scope” → empty text.join(list(scope, “%”)) when scope, otherwise empty text, “limit” → limit, “start” → start).
    - Value choice on scope — true gives empty text.join(list(scope, “%”)), false gives empty text.
  - Set result from Platform.db.multisql(mapping(“mariadb” → common\_query.format(conditions = mariadb\_conditions), “postgres” → common\_query.format(conditions = postgres\_conditions)), values = values, as\_dict = true).
  - Set tmp\_result from list().
  - For each i in result.
    - If (i belongs to results or not results).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in i belongs to results → not results.
      - Evaluate tmp\_result.append(i).
  - Update results using + tmp\_result.
- Set words from set(get\_distinct\_words(text)).
- For each r in results.
  - Set title\_words from set(get\_distinct\_words(r.title)).
  - Set words\_match from len(words.intersection(title\_words)).
  - Set r.relevance from words\_match.
- Set results from sorted(results, key = deferred anonymous expression, reverse = true).
- Return results at slice no value to WEB\_SEARCH\_MAX\_LIMIT.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L120) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L174)

<a id="op-903c1bb71f0512"></a>
### Get distinct words

`operation_foundation_utils_global_search_business_behavior_get_distinct_words`

**Inputs** text.

**Explicit results** list of w.strip().lower() for w drawn from text.split(one space).

**Local steps**

- Set text from text.replace(“"”, empty text).
- Set text from text.replace(“'”, empty text).
- Return list of w.strip().lower() for w drawn from text.split(one space).
  - Draw w from text.split(one space).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0483.json#L2165) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L155)

## Service · Goal

<a id="op-9c10d9913e6e07"></a>
### Get monthly results

`operation_foundation_utils_goal_business_behavior_get_monthly_results`

**Inputs** goal\_doctype, goal\_field, date\_col, filters, aggregation = “sum”.

**Declared result** dict.

**Explicit results** dict(nested operand in the contract.get\_query(table = goal\_doctype, fields = list(nested operand in the contract, nested operand in the contract), filters = filters, ignore\_permissions = false).groupby(“month\_y …).

**Explicit failure paths** validation helper — formatted text Invalid aggregation type: {aggregation} · validation helper — formatted text Invalid goal field: {goal\_field} · validation helper — formatted text Invalid date field: {date\_col}.

**Local steps**

- If aggregation.lower() does not belong to set(“sum”, “avg”, “count”, “min”, …).
  - Call the validation error handler Platform.throw(formatted text Invalid aggregation type: {aggregation}).
- Set valid\_fields from Platform.get\_meta(goal\_doctype).get\_valid\_fields().
- If goal\_field does not belong to valid\_fields.
  - Call the validation error handler Platform.throw(formatted text Invalid goal field: {goal\_field}).
- If date\_col does not belong to valid\_fields.
  - Call the validation error handler Platform.throw(formatted text Invalid date field: {date\_col}).
- Set Table from DocType(goal\_doctype).
- Set date\_format from “%m-%Y” when Platform.db.db\_type differs from “postgres”, otherwise “MM-YYYY”.
  - Value choice on Platform.db.db\_type differs from “postgres” — true gives “%m-%Y”, false gives “MM-YYYY”.
- Return dict(nested operand in the contract.get\_query(table = goal\_doctype, fields = list(nested operand in the contract, nested operand in the contract), filters = filters, ignore\_permissions = false).groupby(“month\_y …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L122) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L176)

<a id="op-76bf9c9c1c261d"></a>
### Get monthly goal graph data

`operation_foundation_utils_goal_business_behavior_get_monthly_goal_graph_data`

**Inputs** title, doctype, docname, goal\_value\_field, goal\_total\_field, goal\_history\_field, goal\_doctype, goal\_doctype\_link, goal\_field, date\_field, aggregation = “sum”, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call insert on month\_labels · call insert on dataset\_values · call insert on values\_formatted.

**Explicit results** mapping(“title” → title, “fieldtype” → total\_df.fieldtype, “currency” → get\_field\_currency(total\_df, doc), “data” → mapping(“datasets” → list(mapping(“values” → dataset\_values, “formatted” → values\_formatt ….

**Local steps**

- Set doc from Platform.get\_doc(doctype, docname).
- Evaluate doc.check\_permission().
- Set meta from doc.meta.
- Set goal from doc.get(goal\_value\_field).
- Set today\_date from now\_datetime().date().
- Set current\_month\_value from doc.get(goal\_total\_field).
- Set current\_month\_year from today\_date.strftime(“%m-%Y”).
- Set formatted\_value from format\_value(current\_month\_value, meta.get\_field(goal\_total\_field), doc).
- Set history from doc.get(goal\_history\_field).
- Set month\_to\_value\_dict from no value.
- If (history and “{” belongs to cstr(history)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in history → “{” belongs to cstr(history).
  - Within suppress(ValueError).
    - Set month\_to\_value\_dict from Platform.parse\_json(history).
- If month\_to\_value\_dict is identical to no value.
  - Set doc\_filter from mapping().
  - Within suppress(ValueError).
    - Set doc\_filter from Platform.parse\_json((filters or “{}”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → “{}”.
  - If doctype differs from goal\_doctype.
    - Set doc\_filter at goal\_doctype\_link from docname.
  - Set month\_to\_value\_dict from get\_monthly\_results(goal\_doctype, goal\_field, date\_field, doc\_filter, …).
- Set month\_to\_value\_dict at current\_month\_year from current\_month\_value.
- Set month\_labels from list().
- Set dataset\_values from list().
- Set values\_formatted from list().
- Set y\_markers from mapping().
- Set summary\_values from list(mapping(“title” → translated “This month”, “color” → “#ffa00a”, “value” → formatted\_value)).
- If flt(goal) &gt; 0.
  - Set formatted\_goal from format\_value(goal, meta.get\_field(goal\_value\_field), doc).
  - Update summary\_values using + list(mapping(“title” → translated “Goal”, “color” → “#5e64ff”, “value” → formatted\_goal), mapping(“title” → translated “Completed”, “color” → “#28a745”, “value” → formatted text {round(((nested operand in  ….
  - Set y\_markers from mapping(“yMarkers” → list(mapping(“label” → translated “Goal”, “lineType” → “dashed”, “value” → flt(goal)))).
- For each i in range(12).
  - Set date\_value from add\_to\_date(today\_date, months = negative i, as\_datetime = true).
  - Set month\_word from date\_value.strftime(“%b %y”).
  - Evaluate month\_labels.insert(0, month\_word).
  - Set month\_value from date\_value.strftime(“%m-%Y”).
  - Set val from month\_to\_value\_dict.get(month\_value, 0).
  - Evaluate dataset\_values.insert(0, val).
  - Evaluate values\_formatted.insert(0, format\_value(val, meta.get\_field(goal\_total\_field), doc)).
- Set total\_df from (meta.get\_field(goal\_total\_field) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_field(goal\_total\_field) → Platform.\_dict().
- Return mapping(“title” → title, “fieldtype” → total\_df.fieldtype, “currency” → get\_field\_currency(total\_df, doc), “data” → mapping(“datasets” → list(mapping(“values” → dataset\_values, “formatted” → values\_formatt ….

**Values supplied outside this operation** effective access from doc.check\_permission() · clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L121) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L175)
