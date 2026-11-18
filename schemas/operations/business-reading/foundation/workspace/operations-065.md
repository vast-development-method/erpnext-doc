# Forms, reports and navigation · operations 65

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Sqlite search

<a id="op-251a425a075bf1"></a>
### SQLite Search.add metadata fields to document

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_add_metadata_fields_to_document`

**Inputs** self, document, doc, config.

**Local steps**

- Set metadata\_fields from self.schema at “metadata\_fields”.
- For each field in metadata\_fields.
  - If field belongs to document.
    - Continue with the next iteration or loop test.
  - If field equals “modified”.
    - Set modified\_field from config at “modified\_field”.
    - Set modified\_value from getattr(doc, modified\_field, no value).
    - If modified\_value.
      - If not isinstance(modified\_value, datetime.datetime).
        - Set modified\_value from Platform.utils.get\_datetime(modified\_value).
      - Set document at “modified” from modified\_value.timestamp().
    - Continue with the next iteration or loop test.
  - Set field\_mappings from config.get(“field\_mappings”, mapping()).
  - Set actual\_field from field\_mappings.get(field, field).
  - Set value from getattr(doc, actual\_field, no value).
  - If (value is distinct from no value and hasattr(value, “\_mock\_name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is distinct from no value → hasattr(value, “\_mock\_name”).
    - Set value from str(value).
  - Set document at field from value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, modified\_field, no value), getattr(doc, actual\_field, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L5609) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L459)

<a id="op-963cf5763d45d7"></a>
### SQLite Search.process content

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_process_content`

**Inputs** self, content.

**Explicit results** empty text · text.

**Local steps**

- If not content.
  - Return empty text.
- Bind dependencies BeautifulSoup.
- Set content from str(content).
- Set soup from BeautifulSoup(content, “html.parser”).
- For each link in soup.find\_all(“a”).
  - Set link\_text from link.get\_text().strip().
  - If link\_text.
    - Evaluate link.replace\_with(link\_text).
  - Otherwise.
    - Evaluate link.replace\_with(“&#91;link&#93;”).
- Set text from soup.get\_text(separator = one space).strip().
- Set text from re.sub(“https?://&#91;^\\s&#93;+”, “&#91;link&#93;”, text).
- Set text from re.sub(“\\s+”, one space, text).strip().
- Set text from strip\_surrogates(text).
- Return text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L6112) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L510)

<a id="op-3228b89b8ea7e0"></a>
### SQLite Search.generate trigrams

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_generate_trigrams`

**Inputs** self, word.

**Explicit results** list of word at slice i to (i + 3) for i drawn from range((len(word) − 2)).

**Local steps**

- Set word from formatted text   {word.lower()}.
- Return list of word at slice i to (i + 3) for i drawn from range((len(word) − 2)).
  - Draw i from range((len(word) − 2)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L6519) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L476)

<a id="op-271bcb767a3f92"></a>
### SQLite Search.print warning summary

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_print_warning_summary`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.warnings.
  - Return no value.
- Evaluate print((whitespace '\\n' + (“=” × 60))).
- Evaluate print(“SEARCH INDEX BUILD WARNINGS”).
- Evaluate print((“=” × 60)).
- Set warning\_groups from mapping().
- For each warning in self.warnings.
  - Evaluate warning\_groups.setdefault(warning.type, list()).append(warning).
- Set type\_display\_names from mapping(WarningType.INVALID\_DOCUMENT → “Invalid Documents”, WarningType.MISSING\_TEXT\_FIELDS → “Missing Text Fields”, WarningType.MISSING\_CONTENT\_FIELD → “Missing Content Field”, WarningType.MISSING\_TITLE\_F ….
- For each tuple(warning\_type, warnings) in warning\_groups.items().
  - Set display\_name from type\_display\_names.get(warning\_type, warning\_type.value.title()).
  - Evaluate print(formatted text  {display\_name} ({len(warnings)} warnings):).
  - Evaluate print((“-” × 50)).
  - For each warning in warnings at slice no value to 5.
    - Evaluate print(formatted text   • {warning.message}).
  - If len(warnings) &gt; 5.
    - Evaluate print(formatted text   ... and {(len(warnings) − 5)} more).
- Evaluate print(formatted text  Total warnings: {len(self.warnings)}).
- Evaluate print((“=” × 60)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L6683) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L509)

<a id="op-f2e085e70a05aa"></a>
### SQLite Search.add warning

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_add_warning`

**Inputs** self, warning\_type, message, remaining named values kwargs.

**Local steps**

- Set warning from IndexWarning(type = warning\_type, message = message, expanded names kwargs).
- Evaluate self.warnings.append(warning).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L7423) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L461)

<a id="op-c76d9b97ee374a"></a>
### SQLite Search.warn invalid document

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_warn_invalid_document`

**Inputs** self, doc, reason.

**Local steps**

- Evaluate self.\_add\_warning(WarningType.INVALID\_DOCUMENT, formatted text Skipping document with {reason}: {doc}, doctype = doc.get(“doctype”), docname = doc.get(“name”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add warning](operations-065.md#op-f2e085e70a05aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L524)

<a id="op-c35b906aa28ebe"></a>
### SQLite Search.warn missing text fields

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_warn_missing_text_fields`

**Inputs** self, doctype, docname, missing\_fields.

**Local steps**

- Evaluate self.\_add\_warning(WarningType.MISSING\_TEXT\_FIELDS, formatted text Document {doctype}:{docname} missing text fields: {missing\_fields}, doctype = doctype, docname = docname, missing\_fields = missing\_fields).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add warning](operations-065.md#op-f2e085e70a05aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L186) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L528)

<a id="op-7be9b72bd69c90"></a>
### SQLite Search.warn missing content field

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_warn_missing_content_field`

**Inputs** self, doctype, docname, field.

**Local steps**

- Evaluate self.\_add\_warning(WarningType.MISSING\_CONTENT\_FIELD, formatted text Document {doctype}:{docname} missing content field '{field}', doctype = doctype, docname = docname, field = field).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add warning](operations-065.md#op-f2e085e70a05aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L360) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L525)

<a id="op-57f07feb9dc90b"></a>
### SQLite Search.warn missing title field

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_warn_missing_title_field`

**Inputs** self, doctype, docname, field.

**Local steps**

- Evaluate self.\_add\_warning(WarningType.MISSING\_TITLE\_FIELD, formatted text Document {doctype}:{docname} missing title field '{field}', doctype = doctype, docname = docname, field = field).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add warning](operations-065.md#op-f2e085e70a05aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L538) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L529)

<a id="op-7162677edc258e"></a>
### SQLite Search.warn missing doctype

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_warn_missing_record_type`

**Inputs** self, doc.

**Local steps**

- Evaluate self.\_add\_warning(WarningType.MISSING\_DOCTYPE, formatted text Document missing doctype: {doc}, docname = getattr(doc, “name”, no value)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add warning](operations-065.md#op-f2e085e70a05aa).

**Values supplied outside this operation** selected callable from getattr(doc, “name”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L716) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L527)

<a id="op-363f1f596bdd01"></a>
### SQLite Search.warn missing name

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_warn_missing_name`

**Inputs** self, doctype.

**Local steps**

- Evaluate self.\_add\_warning(WarningType.MISSING\_NAME, formatted text Document missing name: {doctype}, doctype = doctype).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add warning](operations-065.md#op-f2e085e70a05aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L843) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L526)

<a id="op-60fcfce6b52426"></a>
### SQLite Search.get warning statistics

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_warning_statistics`

**Inputs** self.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“total” → 0, “by\_type” → mapping()) · stats.

**Local steps**

- If not self.warnings.
  - Return mapping(“total” → 0, “by\_type” → mapping()).
- Set stats from mapping(“total” → len(self.warnings), “by\_type” → mapping()).
- For each warning in self.warnings.
  - Set warning\_type from warning.type.value.
  - If warning\_type does not belong to stats at “by\_type”.
    - Set stats at “by\_type” at warning\_type from mapping(“count” → 0, “examples” → list()).
  - Update stats at “by\_type” at warning\_type at “count” using + 1.
  - If len(stats at “by\_type” at warning\_type at “examples”) &lt; 3.
    - Evaluate stats at “by\_type” at warning\_type at “examples”.append(mapping(“message” → warning.message, “doctype” → warning.doctype, “docname” → warning.docname, “field” → warning.field, …)).
- Return stats.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L945) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L491)

<a id="op-9a5cdaa459f8c6"></a>
### Build index if not exists

`operation_foundation_search_sqlite_search_business_behavior_build_index_if_not_exists`

**Inputs** no declared parameters.

**Local steps**

- Set search\_classes from get\_search\_classes().
- For each SearchClass in search\_classes.
  - Set search from SearchClass().
  - If not search.is\_search\_enabled().
    - Continue with the next iteration or loop test.
  - Set temp\_db\_path from search.\_get\_db\_path(is\_temp = true).
  - If os.path.exists(temp\_db\_path).
    - Evaluate print(formatted text {SearchClass.\_\_name\_\_}: Found temp DB, continuing build...).
    - Evaluate build\_index(SearchClass, force = true, is\_continuation = true).
  - Otherwise.
    - If not search.index\_exists().
      - Evaluate print(formatted text {SearchClass.\_\_name\_\_}: No index exists, starting fresh build...).
      - Evaluate build\_index(SearchClass, force = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L1466) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L452)

<a id="op-11fe2e1d7ce13e"></a>
### Build index

`operation_foundation_search_sqlite_search_business_behavior_build_index`

**Inputs** SearchClass = no value, search\_class\_path = no value, force = false, is\_continuation = false.

**Explicit results** no value.

**Explicit failure paths** ValueError(“Either SearchClass or search\_class\_path must be provided”).

**Local steps**

- If (not SearchClass and not search\_class\_path).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not SearchClass → not search\_class\_path.
  - Raise ValueError(“Either SearchClass or search\_class\_path must be provided”).
- If search\_class\_path.
  - Set SearchClass from Platform.get\_attr(search\_class\_path).
- Set search from SearchClass().
- If not search.is\_search\_enabled().
  - Return no value.
- If (search.index\_exists() and not force).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in search.index\_exists() → not force.
  - Return no value.
- If is\_continuation.
  - Evaluate print(formatted text {SearchClass.\_\_name\_\_}: Continuing incremental index build...).
- Otherwise.
  - Evaluate print(formatted text {SearchClass.\_\_name\_\_}: Index does not exist or force=True, building...).
- Attempt the following.
  - Within filelock(\_build\_lock\_name(SearchClass), timeout = 0).
    - Evaluate search.build\_index(is\_continuation = is\_continuation).
- On failure (LockTimeoutError).
  - Evaluate print(formatted text {SearchClass.\_\_name\_\_}: another build is already running, skipping.).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(search\_class\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L14) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L451)

<a id="op-a2e05265fc7e84"></a>
### Build lock name

`operation_foundation_binding_foundation_search_sqlite_search_build_lock_name`

**Inputs** SearchClass.

**Declared result** str.

**Explicit results** formatted text search\_index\_{SearchClass.\_\_module\_\_}.{SearchClass.\_\_name\_\_}.

**Local steps**

- Return formatted text search\_index\_{SearchClass.\_\_module\_\_}.{SearchClass.\_\_name\_\_}.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1709)

<a id="op-67f482cd62592a"></a>
### Enqueue index job

`operation_foundation_search_sqlite_search_business_behavior_enqueue_index_job`

**Inputs** search\_class\_path, is\_continuation = false.

**State and service calls** enqueue with “Platform.search.sqlite\_search.build\_index”.

**Local steps**

- Set job\_id from formatted text {search\_class\_path}\_continuation when is\_continuation, otherwise search\_class\_path.
  - Value choice on is\_continuation — true gives formatted text {search\_class\_path}\_continuation, false gives search\_class\_path.
- Set job\_type from “continuation” when is\_continuation, otherwise “fresh build”.
  - Value choice on is\_continuation — true gives “continuation”, false gives “fresh build”.
- Evaluate print(formatted text Enqueuing {job\_type} for {search\_class\_path}.build\_index).
- Set timeout from (((2 × 60) × 60) + (10 × 60)).
- Set enqueue\_kwargs from mapping(“queue” → “long”, “job\_id” → job\_id, “deduplicate” → true, “search\_class\_path” → search\_class\_path, …).
- Evaluate Platform.enqueue(“Platform.search.sqlite\_search.build\_index”, expanded names enqueue\_kwargs).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.search.sqlite\_search.build\_index”, expanded names enqueue\_kwargs).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L2246) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L455)

<a id="op-ca80409f5d7edb"></a>
### Build index in background

`operation_foundation_search_sqlite_search_business_behavior_build_index_in_background`

**Inputs** no declared parameters.

**Local steps**

- Set search\_classes from get\_search\_classes().
- For each SearchClass in search\_classes.
  - Set search from SearchClass().
  - If not search.is\_search\_enabled().
    - Continue with the next iteration or loop test.
  - Set search\_class\_path from formatted text {SearchClass.\_\_module\_\_}.{SearchClass.\_\_name\_\_}.
  - Set temp\_db\_path from search.\_get\_db\_path(is\_temp = true).
  - If os.path.exists(temp\_db\_path).
    - Evaluate \_enqueue\_index\_job(search\_class\_path, is\_continuation = true).
  - Otherwise.
    - If not search.index\_exists().
      - Evaluate \_enqueue\_index\_job(search\_class\_path, is\_continuation = false).
    - Otherwise.
      - Evaluate print(formatted text Index for {search\_class\_path} already exists).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L2649) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L453)

<a id="op-12b26e83c5bced"></a>
### Update doc index

`operation_foundation_search_sqlite_search_business_behavior_update_record_index`

**Inputs** doc, method = no value.

**Local steps**

- Set search\_classes from get\_search\_classes().
- For each SearchClass in search\_classes.
  - Set search from SearchClass().
  - If not (search.is\_search\_enabled() and search.index\_exists()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in search.is\_search\_enabled() → search.index\_exists().
    - Continue with the next iteration or loop test.
  - For each tuple(doctype, config) in search.doc\_configs.items().
    - If doc.doctype equals doctype.
      - Set fields from config.get(“fields”, list()).
      - If not fields.
        - Continue with the next iteration or loop test.
      - Set any\_field\_changed from any(generator of doc.has\_value\_changed(field) for field drawn from fields).
        - Draw field from fields.
      - If any\_field\_changed.
        - Attempt the following.
          - Evaluate search.index\_doc(doctype, doc.name).
        - On failure (Exception).
          - Evaluate Platform.log\_error(title = “SQLite Search Index Update Error”, message = formatted text Failed to update index for {doctype}:{doc.name} in {search.\_\_class\_\_.\_\_name\_\_}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L24) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L531)

<a id="op-9cdb0d76dea2fe"></a>
### Delete doc index

`operation_foundation_search_sqlite_search_business_behavior_delete_record_index`

**Inputs** doc, method = no value.

**Local steps**

- Set search\_classes from get\_search\_classes().
- For each SearchClass in search\_classes.
  - Set search from SearchClass().
  - If not (search.is\_search\_enabled() and search.index\_exists()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in search.is\_search\_enabled() → search.index\_exists().
    - Continue with the next iteration or loop test.
  - For each tuple(doctype, config) in search.doc\_configs.items().
    - If doc.doctype equals doctype.
      - Set fields from config.get(“fields”, list()).
      - If not fields.
        - Continue with the next iteration or loop test.
      - Attempt the following.
        - Evaluate search.remove\_doc(doctype, doc.name).
      - On failure (Exception).
        - Evaluate Platform.log\_error(title = “SQLite Search Index Delete Error”, message = formatted text Failed to remove index for {doctype}:{doc.name} in {search.\_\_class\_\_.\_\_name\_\_}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L15) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L454)

<a id="op-6d812c7307c459"></a>
### Get search classes

`operation_foundation_search_sqlite_search_business_behavior_get_search_classes`

**Inputs** no declared parameters.

**Declared result** list at type at SQLiteSearch.

**Explicit results** search\_classes.

**Explicit failure paths** TypeError(formatted text Search class {search\_class.\_\_name\_\_} must extend SQLiteSearch).

**Local steps**

- Set module\_paths from Platform.get\_hooks(“sqlite\_search”).
- Set search\_classes from list of Platform.get\_attr(path) for path drawn from module\_paths.
  - Draw path from module\_paths.
- For each search\_class in search\_classes.
  - If not issubclass(search\_class, SQLiteSearch).
    - Raise TypeError(formatted text Search class {search\_class.\_\_name\_\_} must extend SQLiteSearch).
- Return search\_classes.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“sqlite\_search”), Platform.get\_attr(path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0331.json#L3920) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L456)

## Service · Studio

<a id="op-58bc52a4c0c2c5"></a>
### Get context

`operation_foundation_binding_foundation_www_studio_get_context`

**Inputs** context.

**State and service calls** commit.

**Local steps**

- Set csrf\_token from Platform.sessions.get\_csrf\_token().
- Evaluate Platform.db.commit().
- Set context.csrf\_token from csrf\_token.
- Set context.site\_url from get\_site\_url().
- Set context.site\_name from Platform.local.site.
- Set context.socketio\_port from cint(Platform.conf.socketio\_port).
- Set context.is\_developer\_mode from cint(Platform.conf.developer\_mode).
- Set context.assets from get\_editor\_assets(“index.html”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L89) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L482)

<a id="op-55a7b5db89d601"></a>
### Get context for dev

`operation_foundation_binding_foundation_www_studio_get_context_for_dev`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”), allow\_guest = true).

**Explicit results** Platform.\_dict(mapping(“site\_url” → get\_site\_url(), “site\_name” → Platform.local.site, “socketio\_port” → cint(Platform.conf.socketio\_port), “is\_developer\_mode” → cint(Platform.conf.developer\_mode))).

**Explicit failure paths** validation helper — Platform.\_(“This method is only meant for developer mode”).

**Local steps**

- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(Platform.\_(“This method is only meant for developer mode”)).
- Return Platform.\_dict(mapping(“site\_url” → get\_site\_url(), “site\_name” → Platform.local.site, “socketio\_port” → cint(Platform.conf.socketio\_port), “is\_developer\_mode” → cint(Platform.conf.developer\_mode))).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L90) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L483)

<a id="op-1595feb3dfe0c1"></a>
### Get site url

`operation_foundation_binding_foundation_www_studio_get_site_url`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** Platform.utils.get\_site\_url(Platform.local.site).

**Local steps**

- Return Platform.utils.get\_site\_url(Platform.local.site).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L91) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L484)

## Record · Studio ai session

<a id="op-e58dc762f30857"></a>
### Studio AISession.on trash

`operation_foundation_binding_foundation_studio_doctype_studio_ai_session_studio_ai_session_studioaisession_on_trash`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L36) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1930)
