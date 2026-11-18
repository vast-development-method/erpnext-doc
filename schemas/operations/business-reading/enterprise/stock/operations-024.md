# Inventory and warehouses · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Item

[Record definition](../../../../data/record-types/item.json)

<a id="op-335392f35a57df"></a>
### Get default warehouse for opening stock

`operation_enterprise_stock_record_definitions_item_business_behavior_get_default_warehouse_for_opening_stock`

**Inputs** item, company, warehouse.

**Record and data access** read “Company” via get\_cached\_value · read “Warehouse” via get\_value.

**Explicit results** warehouse · default.default\_warehouse · company\_warehouse · stores\_warehouse.

**Explicit failure paths** validation helper — translated “No warehouse found for company {0}. Please set a Default Warehouse in Item Defaults or Company.”.format(Platform.bold(company)).

**Local steps**

- If warehouse.
  - Return warehouse.
- For each default in item.item\_defaults.
  - If (default.company equals company and default.default\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in default.company equals company → default.default\_warehouse.
    - Return default.default\_warehouse.
- If company\_warehouse bound to Platform.get\_cached\_value(“Company”, company, “default\_warehouse”).
  - Return company\_warehouse.
- Set stores\_warehouse from Platform.db.get\_value(“Warehouse”, mapping(“warehouse\_name” → translated “Stores”, “company” → company)).
- If stores\_warehouse.
  - Return stores\_warehouse.
- Call the validation error handler Platform.throw(translated “No warehouse found for company {0}. Please set a Default Warehouse in Item Defaults or Company.”.format(Platform.bold(company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_warehouse”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0735.json#L2176) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1076)

<a id="op-3d63f717747907"></a>
### Get data

`operation_enterprise_stock_record_definitions_item_item_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“heatmap” → true, “heatmap\_message” → translated “This is based on stock movement. See {0} for details”.format(((text in the contract + translated “Stock Ledger”) + “&lt;/a&gt;”)), “fieldname” → “item\_co ….

**Local steps**

- Return mapping(“heatmap” → true, “heatmap\_message” → translated “This is based on stock movement. See {0} for details”.format(((text in the contract + translated “Stock Ledger”) + “&lt;/a&gt;”)), “fieldname” → “item\_co ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1149)

<a id="op-e546715a01357d"></a>
### Has trigram tokenizer

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_has_trigram_tokenizer`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** sqlite3.sqlite\_version\_info ≥ MINIMUM\_SQLITE\_VERSION.

**Local steps**

- Return sqlite3.sqlite\_version\_info ≥ MINIMUM\_SQLITE\_VERSION.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L800) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L297)

<a id="op-11b6b4e07f846e"></a>
### Fold text

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_fold_text`

**Inputs** text.

**Declared result** str.

**Explicit results** empty text.join(generator of fold\_digit(char) for char drawn from decomposed where not unicodedata.combining(char)).

**Local steps**

- Set decomposed from unicodedata.normalize(“NFKD”, text).translate(KATAKANA\_TO\_HIRAGANA).translate(SMALL\_KANA\_TO\_FULL\_SIZE).
- Return empty text.join(generator of fold\_digit(char) for char drawn from decomposed where not unicodedata.combining(char)).
  - Draw char from decomposed, keep a combination only if (not unicodedata.combining(char)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L796) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L293)

<a id="op-82513fc9d9be45"></a>
### Fold digit

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_fold_digit`

**Inputs** char.

**Declared result** str.

**Explicit results** char when digit is identical to no value, otherwise str(digit).

**Local steps**

- Set digit from unicodedata.digit(char, no value).
- Return char when digit is identical to no value, otherwise str(digit).
  - Value choice on digit is identical to no value — true gives char, false gives str(digit).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L795) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L292)

<a id="op-4f40ded950297c"></a>
### Validate sqlite version

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_validate_sqlite_version`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** no parameters.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L315)

<a id="op-63dd1216419401"></a>
### Get searched fieldnames

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_get_searched_fieldnames`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list of f for f drawn from list(expanded searchfields, expanded extras) where f belongs to db\_fieldnames.

**Local steps**

- Set meta from Platform.get\_meta(“Item”, cached = true).
- Set searchfields from meta.get\_search\_fields().
- Set extras from list of f for f drawn from tuple(“item\_code”, “item\_group”, “item\_name”) where f does not belong to searchfields.
  - Draw f from tuple(“item\_code”, “item\_group”, “item\_name”), keep a combination only if (f does not belong to searchfields).
- Set db\_fieldnames from set of field.fieldname for field drawn from meta.fields.
  - Draw field from meta.fields.
- Return list of f for f drawn from list(expanded searchfields, expanded extras) where f belongs to db\_fieldnames.
  - Draw f from list(expanded searchfields, expanded extras), keep a combination only if (f belongs to db\_fieldnames).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L799) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L296)

<a id="op-34a7b12d803c39"></a>
### Item Search.initialize

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_init`

**Inputs** self, db\_name = no value.

**Local steps**

- Set fieldnames from get\_searched\_fieldnames().
- Set mapped from mapping(“title” → “item\_code”, “content” → “item\_name”).
- Set plain from list of f for f drawn from dict.fromkeys(list(“name”, expanded fieldnames)) where f does not belong to mapped.values().
  - Draw f from dict.fromkeys(list(“name”, expanded fieldnames)), keep a combination only if (f does not belong to mapped.values()).
- Set self.INDEXABLE\_DOCTYPES from mapping(“Item” → mapping(“fields” → list(expanded plain, mapped), “filters” → mapping(“disabled” → 0, “has\_variants” → 0))).
- Set self.INDEX\_SCHEMA from mapping(“tokenizer” → “trigram”, “text\_fields” → list(“title”, “content”, BARCODE\_COLUMN, expanded self.\_extra\_text\_fields(fieldnames))).
- Set self.indexed\_fieldnames from set(“name”, expanded fieldnames).
- Set self.\_barcodes from mapping().
- Evaluate super().\_\_init\_\_(db\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [extra text fields](operations-024.md#op-96cf92376cee33).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L306)

<a id="op-96cf92376cee33"></a>
### Item Search.extra text fields

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_extra_text_fields`

**Inputs** fieldnames.

**Wrappers, in declaration order** staticmethod.

**Declared result** list at str.

**Explicit results** list of f for f drawn from fieldnames where f does not belong to tuple(“item\_code”, “item\_name”).

**Local steps**

- Return list of f for f drawn from fieldnames where f does not belong to tuple(“item\_code”, “item\_name”).
  - Draw f from fieldnames, keep a combination only if (f does not belong to tuple(“item\_code”, “item\_name”)).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L801) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L298)

<a id="op-11f2e3cd13bee4"></a>
### Item Search.index exists

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_index_exists`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · set(self.schema at “text\_fields”) ≤ self.get\_index\_columns().

**Local steps**

- If not os.path.exists(self.db\_path).
  - Return false.
- Return set(self.schema at “text\_fields”) ≤ self.get\_index\_columns().

**Methods declared on this owner** [get index columns](operations-024.md#op-9f8466b7e33bf4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L305)

<a id="op-9f8466b7e33bf4"></a>
### Item Search.get index columns

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_get_index_columns`

**Inputs** self.

**Declared result** set at str.

**Explicit results** set() · set of row at “name” for row drawn from connection.execute(“PRAGMA table\_info(search\_fts)”).

**Local steps**

- Attempt the following.
  - Set connection from self.\_get\_connection(read\_only = true).
- On failure (SQLiteSearchIndexMissingError).
  - Return set().
- Attempt the following.
  - Return set of row at “name” for row drawn from connection.execute(“PRAGMA table\_info(search\_fts)”).
    - Draw row from connection.execute(“PRAGMA table\_info(search\_fts)”).
- On failure (sqlite3.Error).
  - Return set().
- On exit, including pending return or failure.
  - Evaluate connection.close().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L805) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L302)

<a id="op-1682857900a3f9"></a>
### Item Search.get documents paginated

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_get_documents_paginated`

**Inputs** self, doctype, remaining positional values args, remaining named values kwargs.

**Explicit results** documents.

**Local steps**

- Set documents from super().get\_documents\_paginated(doctype, expanded args, expanded names kwargs).
- Set self.\_barcodes from get\_barcodes\_by\_item(list of document.name for document drawn from documents).
  - Draw document from documents.
- Return documents.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L804) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L301)

<a id="op-6316fe730e3553"></a>
### Item Search.index documents by name

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_index_documents_by_name`

**Inputs** self, doctype, names.

**Local steps**

- Set self.\_barcodes from get\_barcodes\_by\_item(names).
- Evaluate super().index\_documents\_by\_name(doctype, names).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L807) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L304)

<a id="op-a42a1ab271cae0"></a>
### Item Search.prepare document

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_prepare_document`

**Inputs** self, doc.

**Explicit results** no value · document.

**Local steps**

- Set document from super().prepare\_document(doc).
- If document is identical to no value.
  - Return no value.
- Set document at BARCODE\_COLUMN from fold\_text(self.get\_barcode\_text(doc.name)).
- Return document.

**Methods declared on this owner** [get barcode text](operations-024.md#op-6b10040e017212).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L308)

<a id="op-7b44a519c24fe0"></a>
### Item Search.process content

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_process_content`

**Inputs** self, content.

**Explicit results** empty text when content is identical to no value, otherwise fold\_text(str(content)).

**Local steps**

- Return empty text when content is identical to no value, otherwise fold\_text(str(content)).
  - Value choice on content is identical to no value — true gives empty text, false gives fold\_text(str(content)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L309)

<a id="op-6b10040e017212"></a>
### Item Search.get barcode text

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_get_barcode_text`

**Inputs** self, item\_code.

**Declared result** str.

**Explicit results** self.\_barcodes at item\_code · get\_barcodes\_by\_item(list(item\_code)).get(item\_code, empty text).

**Local steps**

- If item\_code belongs to self.\_barcodes.
  - Return self.\_barcodes at item\_code.
- Return get\_barcodes\_by\_item(list(item\_code)).get(item\_code, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L802) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L299)

<a id="op-a316a64fcbbdd1"></a>
### Item Search.is search enabled

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_is_search_enabled`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Global Defaults” via get\_single\_value.

**Explicit results** (has\_trigram\_tokenizer() and bool(Platform.get\_single\_value(“Global Defaults”, “enable\_item\_search\_index”))).

**Local steps**

- Return (has\_trigram\_tokenizer() and bool(Platform.get\_single\_value(“Global Defaults”, “enable\_item\_search\_index”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_trigram\_tokenizer() → bool(Platform.get\_single\_value(“Global Defaults”, “enable\_item\_search\_index”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Global Defaults”, “enable\_item\_search\_index”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L810) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L307)

<a id="op-cd28d6ec33d0dc"></a>
### Item Search.get search filters

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_get_search_filters`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping().

**Local steps**

- Return mapping().

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L806) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L303)

<a id="op-94dff90c125940"></a>
### Item Search.get candidate item codes

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_get_candidate_item_codes`

**Inputs** self, txt, searched\_fields.

**Declared result** (list at str bitwise or no value).

**Explicit results** no value · names.

**Local steps**

- If (not self.is\_search\_enabled() or not self.index\_exists()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_search\_enabled() → not self.index\_exists().
  - Return no value.
- If not set(searched\_fields) ≤ self.indexed\_fieldnames.
  - Return no value.
- Set match\_query from build\_match\_query(txt).
- If match\_query is identical to no value.
  - Return no value.
- Set names from self.run\_match(match\_query).
- If (names is identical to no value or len(names) ≥ CANDIDATE\_LIMIT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in names is identical to no value → len(names) ≥ CANDIDATE\_LIMIT.
  - Return no value.
- Return names.

**Methods declared on this owner** [is search enabled](operations-024.md#op-a316a64fcbbdd1), [index exists](operations-024.md#op-11f2e3cd13bee4), [run match](operations-024.md#op-bbd85d9e24b602).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L803) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L300)

<a id="op-bbd85d9e24b602"></a>
### Item Search.run match

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_itemsearch_run_match`

**Inputs** self, match\_query.

**Declared result** (list at str bitwise or no value).

**Explicit results** no value · list of row at “name” for row drawn from matched.

**Local steps**

- Set connection from self.\_get\_connection(read\_only = true).
- Attempt the following.
  - Set matched from connection.execute(query text (SELECT), tuple(match\_query, CANDIDATE\_LIMIT)).fetchall().
- On failure (sqlite3.Error).
  - Evaluate Platform.log\_error(“Item search index lookup failed”).
  - Return no value.
- On exit, including pending return or failure.
  - Evaluate connection.close().
- Return list of row at “name” for row drawn from matched.
  - Draw row from matched.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L310)

<a id="op-a503e167275c14"></a>
### Build match query

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_build_match_query`

**Inputs** txt.

**Declared result** (str bitwise or no value).

**Explicit results** no value · “ AND ”.join(generator of quote\_fragment(fragment) for fragment drawn from usable).

**Local steps**

- If “\\” belongs to txt.
  - Return no value.
- Set fragments from list of fold\_text(fragment).strip() for fragment drawn from re.split(LIKE\_WILDCARDS, txt).
  - Draw fragment from re.split(LIKE\_WILDCARDS, txt).
- Set usable from list of fragment for fragment drawn from fragments where len(fragment) ≥ MINIMUM\_TERM\_LENGTH.
  - Draw fragment from fragments, keep a combination only if (len(fragment) ≥ MINIMUM\_TERM\_LENGTH).
- If not usable.
  - Return no value.
- Return “ AND ”.join(generator of quote\_fragment(fragment) for fragment drawn from usable).
  - Draw fragment from usable.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L794) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L291)

<a id="op-5ad11f25b5ce99"></a>
### Quote fragment

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_quote_fragment`

**Inputs** fragment.

**Declared result** str.

**Explicit results** formatted text "{escaped}".

**Local steps**

- Set escaped from fragment.replace(“"”, “""”).
- Return formatted text "{escaped}".

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L312)

<a id="op-70798f0711c9ab"></a>
### Get barcodes by item

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_get_barcodes_by_item`

**Inputs** item\_codes.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Item Barcode” via get\_all.

**Explicit results** mapping() · barcodes.

**Local steps**

- If not item\_codes.
  - Return mapping().
- Set rows from Platform.get\_all(“Item Barcode”, filters = mapping(“parent” → tuple(“in”, item\_codes), “parentfield” → BARCODE\_COLUMN), fields = list(“parent”, “barcode”)).
- Set barcodes from dict.fromkeys(item\_codes, empty text).
- For each row in rows.
  - Set barcodes at row.parent from formatted text {barcodes.get(row.parent, empty text)} {row.barcode}.strip().
- Return barcodes.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L797) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L294)

<a id="op-2a207d629bde36"></a>
### Reindex item

`operation_enterprise_binding_enterprise_stock_doctype_item_item_search_reindex_item`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate queue\_item(doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L313)
