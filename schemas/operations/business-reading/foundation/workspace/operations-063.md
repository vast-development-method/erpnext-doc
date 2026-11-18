# Forms, reports and navigation · operations 63

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Sqlite search

<a id="op-92497c95ddf86f"></a>
### SQLite Search.build vocabulary incremental.insert vocabulary

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_build_vocabulary_incremental_insert_vocabulary`

**Inputs** cursor.

**Local steps**

- Evaluate cursor.executemany(query text (INSERT), vocab\_data).
- Evaluate cursor.executemany(query text (INSERT), trigram\_data).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L466)

<a id="op-f4b6faff3f30c6"></a>
### SQLite Search.table exists

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_table_exists`

**Inputs** self, table\_name.

**Explicit results** bool(result) · false.

**Local steps**

- Attempt the following.
  - Set result from self.sql(formatted text SELECT name FROM sqlite\_master WHERE type='table' AND name='{table\_name}', read\_only = true).
  - Return bool(result).
- On failure (sqlite3.Error).
  - Return false.

**Methods declared on this owner** [sql](operations-064.md#op-98c6c287adfbb9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L3774) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1843) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L517)

<a id="op-85f92f011f4cf6"></a>
### SQLite Search.index exists

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_index_exists`

**Inputs** self.

**Explicit results** false · self.\_table\_exists(“search\_fts”).

**Local steps**

- If not os.path.exists(self.db\_path).
  - Return false.
- Return self.\_table\_exists(“search\_fts”).

**Methods declared on this owner** [table exists](operations-063.md#op-f4b6faff3f30c6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L3976) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L494)

<a id="op-df37473738f041"></a>
### SQLite Search.drop index

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_drop_index`

**Inputs** self.

**Explicit failure paths** propagate active failure.

**Local steps**

- If os.path.exists(self.db\_path).
  - Attempt the following.
    - Evaluate os.unlink(self.db\_path).
  - On failure (OSError) bound to e.
    - Evaluate Platform.log\_error(formatted text Failed to remove search index file {self.db\_path}: {e}).
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L4078) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L469)

<a id="op-4ac038433379a7"></a>
### SQLite Search.is search enabled

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_is_search_enabled`

**Inputs** self.

**Explicit results** true.

**Local steps**

- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L4259) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L500)

<a id="op-a2bfedee778786"></a>
### SQLite Search.raise if not indexed

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_raise_if_not_indexed`

**Inputs** self.

**Explicit failure paths** SQLiteSearchIndexMissingError(“Search index does not exist. Please build the index first.”).

**Local steps**

- If not self.index\_exists().
  - Raise SQLiteSearchIndexMissingError(“Search index does not exist. Please build the index first.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [index exists](operations-063.md#op-85f92f011f4cf6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L4296) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L512)

<a id="op-d184e4d72ef40e"></a>
### SQLite Search.get documents

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_documents`

**Inputs** self.

**Explicit results** records.

**Local steps**

- Set records from list().
- For each tuple(doctype, config) in self.doc\_configs.items().
  - Set docs from Platform.qb.get\_query(doctype, fields = config at “fields”, filters = config.get(“filters”, mapping())).run(as\_dict = true).
  - For each doc in docs.
    - Set doc.doctype from doctype.
    - If config at “modified\_field” differs from “modified”.
      - Set doc.modified from (getattr(doc, config at “modified\_field”, no value) or doc.modified).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(doc, config at “modified\_field”, no value) → doc.modified.
    - Evaluate records.append(doc).
- Return records.

**Values supplied outside this operation** selected callable from getattr(doc, config at “modified\_field”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L4379) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L480)

<a id="op-772603ba9cdcd1"></a>
### SQLite Search.get documents paginated

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_documents_paginated`

**Inputs** self, doctype, limit = 1000, last\_indexed\_modified = no value, last\_indexed\_name = no value.

**Explicit results** list() · docs.

**Local steps**

- Set config from self.doc\_configs.get(doctype).
- If not config.
  - Return list().
- Set filters from config.get(“filters”, mapping()).copy().
- Set sort\_field from “creation”.
- Set fields from config at “fields”.copy().
- If sort\_field does not belong to fields.
  - Evaluate fields.append(sort\_field).
- If “modified” does not belong to fields.
  - Evaluate fields.append(“modified”).
- If “name” does not belong to fields.
  - Evaluate fields.append(“name”).
- Set query from Platform.qb.get\_query(doctype, fields = fields, filters = filters, order\_by = formatted text {sort\_field} ASC, name ASC, limit = limit).
- If last\_indexed\_modified.
  - Set Table from Platform.qb.DocType(doctype).
  - Set sort\_column from getattr(Table, sort\_field).
  - If last\_indexed\_name.
    - Set query from query.where((sort\_column &gt; last\_indexed\_modified bitwise or (sort\_column equals last\_indexed\_modified bitwise and Table.name &gt; last\_indexed\_name))).
  - Otherwise.
    - Set query from query.where(sort\_column &gt; last\_indexed\_modified).
- Set docs from query.run(as\_dict = true).
- For each doc in docs.
  - Set doc.doctype from doctype.
- Return docs.

**Values supplied outside this operation** selected callable from getattr(Table, sort\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L4729) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L481)

<a id="op-be713d777f7bb0"></a>
### SQLite Search.get index progress

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_index_progress`

**Inputs** self.

**Explicit results** progress · mapping().

**Local steps**

- Attempt the following.
  - Set result from self.sql(query text (SELECT), read\_only = true).
  - Set progress from mapping().
  - For each row in result.
    - Set progress at row at “doctype” from dict(row).
  - Return progress.
- On failure (sqlite3.Error).
  - Return mapping().

**Methods declared on this owner** [sql](operations-064.md#op-98c6c287adfbb9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L5476) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L483)

<a id="op-91cfd471fbecb7"></a>
### SQLite Search.initialize index progress

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_initialize_index_progress`

**Inputs** self.

**Local steps**

- Bind local operation init\_progress for subsequent calls.
- Evaluate self.\_with\_connection(init\_progress).

If control reaches the end, it returns no value.

**Methods declared on this owner** [with connection](operations-064.md#op-e830239468f74c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L20) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L497)

<a id="op-8d14984746e2c9"></a>
### SQLite Search.initialize index progress.init progress

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_initialize_index_progress_initialize_progress`

**Inputs** cursor.

**Local steps**

- Evaluate cursor.execute(query text (DELETE)).
- For each doctype in self.doc\_configs.keys().
  - Set config from self.doc\_configs at doctype.
  - Set total\_count from nested operand in the contract.qb.get\_query(doctype, filters = nested operand in the contract.get(“filters”, mapping()), fields = list(mapping(nested operand in the contract → nested operand in the contrac ….
  - Evaluate cursor.execute(query text (INSERT), tuple(doctype, total\_count)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L21) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L498)

<a id="op-9fca457ee949d9"></a>
### SQLite Search.update index progress

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_update_index_progress`

**Inputs** self, doctype, last\_indexed\_name, last\_indexed\_modified, indexed\_count.

**Local steps**

- Bind local operation update\_progress for subsequent calls.
- Evaluate self.\_with\_connection(update\_progress).

If control reaches the end, it returns no value.

**Methods declared on this owner** [with connection](operations-064.md#op-e830239468f74c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L6706) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L519)

<a id="op-a2535c96be3168"></a>
### SQLite Search.update index progress.update progress

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_update_index_progress_update_progress`

**Inputs** cursor.

**Local steps**

- Evaluate cursor.execute(query text (UPDATE), tuple(last\_indexed\_name, last\_indexed\_modified, indexed\_count, doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L6857) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L520)

<a id="op-cfeceadb16b4b7"></a>
### SQLite Search.mark doctype complete

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_mark_record_type_complete`

**Inputs** self, doctype.

**Local steps**

- Bind local operation mark\_complete for subsequent calls.
- Evaluate self.\_with\_connection(mark\_complete).

If control reaches the end, it returns no value.

**Methods declared on this owner** [with connection](operations-064.md#op-e830239468f74c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L6937) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L502)

<a id="op-22a8830607de30"></a>
### SQLite Search.mark doctype complete.mark complete

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_mark_record_type_complete_mark_complete`

**Inputs** cursor.

**Local steps**

- Evaluate cursor.execute(query text (UPDATE), tuple(doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0328.json#L7112) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L503)

<a id="op-17e7e74cf9d42a"></a>
### SQLite Search.mark vocabulary built

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_mark_vocabulary_built`

**Inputs** self.

**Local steps**

- Bind local operation mark\_built for subsequent calls.
- Evaluate self.\_with\_connection(mark\_built).

If control reaches the end, it returns no value.

**Methods declared on this owner** [with connection](operations-064.md#op-e830239468f74c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L504)

<a id="op-1e06690e6dc58c"></a>
### SQLite Search.mark vocabulary built.mark built

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_mark_vocabulary_built_mark_built`

**Inputs** cursor.

**Local steps**

- Evaluate cursor.execute(query text (UPDATE)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L151) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L505)

<a id="op-d4283f37e664db"></a>
### SQLite Search.is indexing complete

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_is_indexing_complete`

**Inputs** self.

**Explicit results** count equals 0 when count ≥ 0, otherwise false.

**Local steps**

- Set count from self.\_get\_incomplete\_count(“is\_complete = 0 OR vocabulary\_built = 0”).
- Return count equals 0 when count ≥ 0, otherwise false.
  - Value choice on count ≥ 0 — true gives count equals 0, false gives false.

**Methods declared on this owner** [get incomplete count](operations-062.md#op-8ca9f9133c4dc2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L253) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L499)

<a id="op-04ceac472c8f55"></a>
### SQLite Search.get indexing progress

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_indexing_progress`

**Inputs** self.

**Explicit results** tuple(indexed\_docs, total\_docs) · tuple(0, 0).

**Local steps**

- Attempt the following.
  - Set result from self.sql(query text (SELECT), read\_only = true).
  - If (result and result at 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in result → result at 0.
    - Set total\_docs from (result at 0 at “total\_docs” or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0 at “total\_docs” → 0.
    - Set indexed\_docs from (result at 0 at “indexed\_docs” or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0 at “indexed\_docs” → 0.
    - Return tuple(indexed\_docs, total\_docs).
  - Return tuple(0, 0).
- On failure (sqlite3.Error).
  - Return tuple(0, 0).

**Methods declared on this owner** [sql](operations-064.md#op-98c6c287adfbb9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L357) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L484)

<a id="op-8f55ea74f8f63e"></a>
### SQLite Search.tables exist

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_tables_exist`

**Inputs** self.

**Explicit results** self.\_table\_exists(“search\_fts”).

**Local steps**

- Return self.\_table\_exists(“search\_fts”).

**Methods declared on this owner** [table exists](operations-063.md#op-f4b6faff3f30c6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L658) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L518)

<a id="op-fc0ae34ca80dca"></a>
### SQLite Search.execute search query

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_execute_search_query`

**Inputs** self, fts\_query, title\_only, filters.

**Explicit results** self.sql(sql, tuple(fts\_query, fts\_query, expanded filter\_params, candidate\_limit), read\_only = true) · self.sql(sql, params, read\_only = true).

**Local steps**

- Set filter\_conditions from list().
- Set filter\_params from list().
- If filters.
  - For each tuple(field, values) in filters.items().
    - If (not values and isinstance(values, list)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not values → isinstance(values, list).
      - Evaluate filter\_conditions.append(“1=0”).
      - Continue with the next iteration or loop test.
    - If not values.
      - Continue with the next iteration or loop test.
    - If (isinstance(values, list) and len(values) equals 2 and values at 0 equals “LIKE”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(values, list) → len(values) equals 2 → values at 0 equals “LIKE”.
      - Set like\_values from values at 1.
      - If isinstance(like\_values, list).
        - Set like\_conditions from list().
        - For each like\_val in like\_values.
          - Evaluate like\_conditions.append(formatted text {field} LIKE ?).
          - Evaluate filter\_params.append(formatted text %{like\_val}%).
        - Evaluate filter\_conditions.append(formatted text ({“ OR ”.join(like\_conditions)})).
      - Otherwise.
        - Evaluate filter\_conditions.append(formatted text {field} LIKE ?).
        - Evaluate filter\_params.append(formatted text %{like\_values}%).
    - Otherwise.
      - If isinstance(values, list).
        - If len(values) equals 1.
          - Evaluate filter\_conditions.append(formatted text {field} = ?).
          - Evaluate filter\_params.append(values at 0).
        - Otherwise.
          - Set placeholders from “,”.join(list of “?” for \_ drawn from values).
            - Draw \_ from values.
          - Evaluate filter\_conditions.append(formatted text {field} IN ({placeholders})).
          - Evaluate filter\_params.extend(values).
      - Otherwise.
        - Evaluate filter\_conditions.append(formatted text {field} = ?).
        - Evaluate filter\_params.append(values).
- Set filter\_clause from empty text.
- If filter\_conditions.
  - Set filter\_clause from (“AND ” + “ AND ”.join(filter\_conditions)).
- Set text\_fields from self.schema at “text\_fields”.
- Set metadata\_fields from self.schema at “metadata\_fields”.
- Set select\_fields from list().
- Set title\_field from “title” when “title” belongs to text\_fields, otherwise text\_fields at 0 when text\_fields, otherwise “doc\_id”.
  - Value choice on “title” belongs to text\_fields — true gives “title”, false gives text\_fields at 0 when text\_fields, otherwise “doc\_id”.
  - Value choice on text\_fields — true gives text\_fields at 0, false gives “doc\_id”.
- Set title\_column\_index from self.\_get\_text\_field\_column\_index(title\_field).
- If title\_column\_index is distinct from no value.
  - Evaluate select\_fields.append(formatted text highlight(search\_fts, {title\_column\_index}, '&lt;mark&gt;', '&lt;/mark&gt;') as title).
- Otherwise.
  - Evaluate select\_fields.append(formatted text {title\_field} as title).
- If (not title\_only and “content” belongs to text\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not title\_only → “content” belongs to text\_fields.
  - Set content\_index from self.\_get\_text\_field\_column\_index(“content”).
  - Evaluate select\_fields.append(formatted text snippet(search\_fts, {content\_index}, '&lt;mark&gt;', '&lt;/mark&gt;', '...', ?) as content).
- Otherwise.
  - If “content” belongs to text\_fields.
    - Evaluate select\_fields.append(“content”).
- For each field in metadata\_fields.
  - If field differs from “doc\_id”.
    - Evaluate select\_fields.append(field).
- Evaluate select\_fields.extend(list(“bm25(search\_fts) as bm25\_score”, formatted text {title\_field} as original\_title)).
- Set select\_clause from “,\\n                    ”.join(select\_fields).
- Set candidate\_limit from max(MAX\_SEARCH\_RESULTS, MAX\_RERANK\_CANDIDATES).
- If title\_only.
  - Set sql from formatted text                  SELECT                     doc\_id,                     {select\_clause}                 FROM search\_fts                 WHERE search\_f.
  - Return self.sql(sql, tuple(fts\_query, fts\_query, expanded filter\_params, candidate\_limit), read\_only = true).
- Otherwise.
  - Set params from list().
  - If “content” belongs to text\_fields.
    - Evaluate params.append(SNIPPET\_LENGTH).
  - Evaluate params.extend(list(fts\_query, expanded filter\_params, candidate\_limit)).
  - Set sql from formatted text                  SELECT                     doc\_id,                     {select\_clause}                 FROM search\_fts                 WHERE search\_f.
  - Return self.sql(sql, params, read\_only = true).

**Methods declared on this owner** [get text field column index](operations-064.md#op-1300bb918c8540), [sql](operations-064.md#op-98c6c287adfbb9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L714) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L473)

<a id="op-65afda86ba561f"></a>
### SQLite Search.process search results

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_process_search_results`

**Inputs** self, raw\_results, query.

**Explicit results** processed\_results at slice no value to MAX\_SEARCH\_RESULTS.

**Local steps**

- Set processed\_results from list().
- Set query\_words from query.split().
- Set text\_fields from self.schema at “text\_fields”.
- Set metadata\_fields from self.schema at “metadata\_fields”.
- For each tuple(original\_rank, row) in enumerate(raw\_results, 1).
  - Set score from self.\_calculate\_advanced\_score(row, query, query\_words).
  - Set result from mapping(“id” → row at “doc\_id”, “score” → score, “original\_rank” → original\_rank, “bm25\_score” → row at “bm25\_score”).
  - For each field in text\_fields.
    - Set result at field from row at field when field belongs to row.keys(), otherwise empty text.
      - Value choice on field belongs to row.keys() — true gives row at field, false gives empty text.
  - For each field in metadata\_fields.
    - If field equals “owner”.
      - Set result at “author” from row at “owner” when “owner” belongs to row.keys(), otherwise empty text.
        - Value choice on “owner” belongs to row.keys() — true gives row at “owner”, false gives empty text.
    - Otherwise.
      - Set result at field from row at field when field belongs to row.keys(), otherwise no value.
        - Value choice on field belongs to row.keys() — true gives row at field, false gives no value.
  - Evaluate processed\_results.append(result).
- Evaluate processed\_results.sort(key = deferred anonymous expression).
- For each tuple(i, result) in enumerate(processed\_results).
  - Set result at “modified\_rank” from (i + 1).
- Return processed\_results at slice no value to MAX\_SEARCH\_RESULTS.

**Methods declared on this owner** [calculate advanced score](operations-063.md#op-40a7572cab9564).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L2585) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L511)

<a id="op-551f4ce2b2e7bc"></a>
### SQLite Search.get scoring pipeline

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_scoring_pipeline`

**Inputs** self.

**Explicit results** pipeline.

**Local steps**

- Set pipeline from list(self.\_get\_base\_score, self.\_get\_title\_boost).
- If “modified” belongs to self.schema at “metadata\_fields”.
  - Evaluate pipeline.append(self.\_get\_recency\_boost).
- For each attr\_name in dir(self).
  - Set attr from getattr(self, attr\_name).
  - If (callable(attr) and hasattr(attr, “\_is\_scoring\_function”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in callable(attr) → hasattr(attr, “\_is\_scoring\_function”).
    - Evaluate pipeline.append(attr).
- Return pipeline.

**Values supplied outside this operation** selected callable from getattr(self, attr\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L3363) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L487)

<a id="op-40a7572cab9564"></a>
### SQLite Search.calculate advanced score

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_calculate_advanced_score`

**Inputs** self, row, query, query\_words.

**Explicit results** final\_score.

**Local steps**

- Set pipeline from self.get\_scoring\_pipeline().
- Set final\_score from 1.0.
- For each scoring\_method in pipeline.
  - Set sig from inspect.signature(scoring\_method).
  - Set params from list(sig.parameters.keys()).
  - If (params and params at 0 equals “self”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in params → params at 0 equals “self”.
    - Set params from params at slice 1 to no value.
  - If (len(params) ≥ 3 or “query\_words” belongs to params).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(params) ≥ 3 → “query\_words” belongs to params.
    - Update final\_score using × scoring\_method(row, query, query\_words).
  - Otherwise.
    - Update final\_score using × scoring\_method(row, query).
- Return final\_score.

**Methods declared on this owner** [get scoring pipeline](operations-063.md#op-551f4ce2b2e7bc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L3622) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L467)
