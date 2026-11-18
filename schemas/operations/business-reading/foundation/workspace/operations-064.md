# Forms, reports and navigation · operations 64

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Sqlite search

<a id="op-be3eec70816d10"></a>
### SQLite Search.get base score

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_base_score`

**Inputs** self, row, query.

**Explicit results** 0.5 · 1.0 · (1.0 ÷ (1.0 + bm25\_score)).

**Local steps**

- Set bm25\_score from row at “bm25\_score”.
- If bm25\_score is identical to no value.
  - Return 0.5.
- If bm25\_score ≤ 0.
  - Return 1.0.
- Return (1.0 ÷ (1.0 + bm25\_score)).

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L3989) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L477)

<a id="op-26cb57fd9689ea"></a>
### SQLite Search.get title boost

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_title_boost`

**Inputs** self, row, query, query\_words.

**Explicit results** TITLE\_EXACT\_MATCH\_BOOST · 1.0 · boost.

**Local steps**

- Set original\_title from (row at “original\_title” or empty text).lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “original\_title” → empty text.
- Set query\_lower from query.lower().
- Set title\_tokens from set(re.findall(“\\w+”, original\_title)).
- If query\_lower belongs to original\_title.
  - Return TITLE\_EXACT\_MATCH\_BOOST.
- If not query\_words.
  - Return 1.0.
- Set matched\_words from 0.
- For each word in query\_words.
  - If word.lower() belongs to title\_tokens.
    - Update matched\_words using + 1.
- If matched\_words equals 0.
  - Return 1.0.
- Set match\_percentage from (matched\_words ÷ len(query\_words)).
- Set min\_boost from TITLE\_PARTIAL\_MATCH\_BOOST.
- Set max\_boost from TITLE\_EXACT\_MATCH\_BOOST.
- Set boost from (min\_boost + ((max\_boost − min\_boost) × match\_percentage)).
- Return boost.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L4133) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L490)

<a id="op-01e77ed8e58862"></a>
### SQLite Search.get recency boost

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_recency_boost`

**Inputs** self, row, query.

**Explicit results** 1.0 · RECENT\_HOURS\_BOOST · RECENT\_WEEK\_BOOST · RECENT\_MONTH\_BOOST · RECENT\_QUARTER\_BOOST · 1 additional forms in the steps below.

**Local steps**

- If (“modified” does not belong to row or row at “modified” is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “modified” does not belong to row → row at “modified” is identical to no value.
  - Return 1.0.
- Set current\_time from time.time().
- Set doc\_timestamp from row at “modified”.
- Set hours\_old from ((current\_time − doc\_timestamp) ÷ 3600).
- Set days\_old from (hours\_old ÷ 24).
- If hours\_old ≤ 24.
  - Return RECENT\_HOURS\_BOOST.
- If days\_old ≤ 7.
  - Return RECENT\_WEEK\_BOOST.
- If days\_old ≤ 30.
  - Return RECENT\_MONTH\_BOOST.
- If days\_old ≤ 90.
  - Return RECENT\_QUARTER\_BOOST.
- Set days\_beyond\_90 from (days\_old − 90).
- Return max(MIN\_RECENCY\_BOOST, (RECENT\_QUARTER\_BOOST − (days\_beyond\_90 × RECENCY\_DECAY\_RATE))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L4550) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L485)

<a id="op-1300bb918c8540"></a>
### SQLite Search.get text field column index

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_text_field_column_index`

**Inputs** self, field\_name.

**Explicit results** (1 + self.schema at “text\_fields”.index(field\_name)) · no value.

**Local steps**

- Attempt the following.
  - Return (1 + self.schema at “text\_fields”.index(field\_name)).
- On failure (ValueError).
  - Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L4937) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L489)

<a id="op-a221af3b0587db"></a>
### SQLite Search.expand query with corrections

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_expand_query_with_corrections`

**Inputs** self, query.

**Explicit results** tuple(expanded\_query, corrections when corrections, otherwise no value).

**Local steps**

- Set words from query.strip().split().
- Set expanded\_terms from list().
- Set corrections from mapping().
- For each word in words.
  - Set similar\_words from self.\_find\_similar\_words(word).
  - If (similar\_words and similar\_words at 0 differs from word).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in similar\_words → similar\_words at 0 differs from word.
    - Set corrected\_word from similar\_words at 0.
    - Evaluate expanded\_terms.append(corrected\_word).
    - Set corrections at word from corrected\_word.
  - Otherwise.
    - Evaluate expanded\_terms.append(word).
- Set expanded\_query from one space.join(expanded\_terms).
- Return tuple(expanded\_query, corrections when corrections, otherwise no value).
  - Value choice on corrections — true gives corrections, false gives no value.

**Methods declared on this owner** [find similar words](operations-064.md#op-bd0ec2e33c72ae).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L5043) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L474)

<a id="op-bd0ec2e33c72ae"></a>
### SQLite Search.find similar words

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_find_similar_words`

**Inputs** self, word, max\_suggestions = MAX\_SPELLING\_SUGGESTIONS, min\_similarity = MIN\_SIMILARITY\_THRESHOLD.

**Explicit results** list() · list of word for tuple(word, score) drawn from similarities at slice no value to max\_suggestions.

**Local steps**

- Bind dependencies difflib.
- Set word from word.lower().
- If len(word) &lt; MIN\_WORD\_LENGTH.
  - Return list().
- Set word\_trigrams from self.\_generate\_trigrams(word).
- Set word\_length from len(word).
- Attempt the following.
  - Set placeholders from “,”.join((“?” × len(word\_trigrams))).
  - Set candidates from self.sql(formatted text                  SELECT t.word, v.frequency, v.length, COUNT(\*) as shared\_trigrams                 FROM search\_trigrams t                 JOIN search\_, tuple(expanded word\_trigrams, ….
- On failure (sqlite3.Error).
  - Return list().
- Set similarities from list().
- Set word\_trigram\_set from set(word\_trigrams).
- For each tuple(candidate\_word, freq, candidate\_length, \_) in candidates.
  - If abs((candidate\_length − word\_length)) &gt; MAX\_EDIT\_DISTANCE.
    - Continue with the next iteration or loop test.
  - Set candidate\_trigrams from set(self.\_generate\_trigrams(candidate\_word)).
  - Set intersection from len((word\_trigram\_set bitwise and candidate\_trigrams)).
  - Set union from len((word\_trigram\_set bitwise or candidate\_trigrams)).
  - Set trigram\_similarity from (intersection ÷ union) when union &gt; 0, otherwise 0.
    - Value choice on union &gt; 0 — true gives (intersection ÷ union), false gives 0.
  - If trigram\_similarity &lt; 0.3.
    - Continue with the next iteration or loop test.
  - Set seq\_similarity from difflib.SequenceMatcher(no value, word, candidate\_word).ratio().
  - Set combined\_similarity from ((trigram\_similarity × SIMILARITY\_TRIGRAM\_WEIGHT) + (seq\_similarity × SIMILARITY\_SEQUENCE\_WEIGHT)).
  - Set frequency\_boost from min(MAX\_FREQUENCY\_BOOST, (1.0 + (freq ÷ FREQUENCY\_BOOST\_FACTOR))).
  - Set final\_score from (combined\_similarity × frequency\_boost).
  - If final\_score ≥ min\_similarity.
    - Evaluate similarities.append(tuple(candidate\_word, final\_score)).
- Evaluate similarities.sort(key = deferred anonymous expression, reverse = true).
- Return list of word for tuple(word, score) drawn from similarities at slice no value to max\_suggestions.
  - Draw tuple(word, score) from similarities at slice no value to max\_suggestions.

**Methods declared on this owner** [generate trigrams](operations-065.md#op-3228b89b8ea7e0), [sql](operations-064.md#op-98c6c287adfbb9).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L5369) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1801) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L475)

<a id="op-14564fd1bbcbd1"></a>
### SQLite Search.get connection

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_connection`

**Inputs** self, read\_only = false.

**Explicit results** conn.

**Explicit failure paths** SQLiteSearchIndexMissingError(formatted text Search database connection failed: {e}).

**Local steps**

- Attempt the following.
  - Set conn from sqlite3.connect(self.db\_path).
  - Set conn.row\_factory from sqlite3.Row.
  - Set cursor from conn.cursor().
  - Evaluate self.\_set\_pragmas(cursor, read\_only).
  - Evaluate cursor.execute(“SELECT 1”).
  - Return conn.
- On failure (sqlite3.Error) bound to e.
  - Evaluate Platform.log\_error(formatted text Failed to connect to search database: {e}).
  - Raise SQLiteSearchIndexMissingError(formatted text Search database connection failed: {e}) with cause e.

**Methods declared on this owner** [set pragmas](operations-064.md#op-eaa803cf201998).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L6420) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L478)

<a id="op-eaa803cf201998"></a>
### SQLite Search.set pragmas

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_set_pragmas`

**Inputs** self, cursor, is\_read = false.

**Local steps**

- Evaluate cursor.execute(“PRAGMA journal\_mode = WAL;”).
- Evaluate cursor.execute(“PRAGMA synchronous = NORMAL;”).
- Evaluate cursor.execute(“PRAGMA cache\_size = -8192;”).
- Evaluate cursor.execute(“PRAGMA temp\_store = MEMORY;”).
- If is\_read.
  - Evaluate cursor.execute(“PRAGMA query\_only = 1;”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L23) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L516)

<a id="op-e830239468f74c"></a>
### SQLite Search.with connection

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_with_connection`

**Inputs** self, callback, read\_only = false.

**Explicit results** result.

**Local steps**

- Set conn from self.\_get\_connection(read\_only = read\_only).
- Attempt the following.
  - Set cursor from conn.cursor().
  - Set result from callback(cursor).
  - If not read\_only.
    - Evaluate conn.commit().
  - Return result.
- On exit, including pending return or failure.
  - Evaluate conn.close().

**Methods declared on this owner** [get connection](operations-064.md#op-14564fd1bbcbd1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0329.json#L6896) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L530)

<a id="op-d44c483891f8ab"></a>
### SQLite Search.ensure fts table

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_ensure_fts_table`

**Inputs** self.

**Local steps**

- Set text\_fields from self.schema at “text\_fields”.
- Set metadata\_fields from self.schema at “metadata\_fields”.
- Set tokenizer from self.schema at “tokenizer”.
- Bind local operation create\_tables for subsequent calls.
- Evaluate self.\_with\_connection(create\_tables).

If control reaches the end, it returns no value.

**Methods declared on this owner** [with connection](operations-064.md#op-e830239468f74c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L17) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L471)

<a id="op-d3402c0cd4dbfa"></a>
### SQLite Search.ensure fts table.create tables

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_ensure_fts_table_create_tables`

**Inputs** cursor.

**Local steps**

- Evaluate cursor.execute(formatted text                  CREATE VIRTUAL TABLE IF NOT EXISTS search\_fts USING fts5(                     doc\_id UNINDEXED,                     {“, ”.join(list o).
  - Draw field from text\_fields.
  - Draw field from metadata\_fields.
- Evaluate cursor.execute(query text (CREATE)).
- Evaluate cursor.execute(query text (CREATE)).
- Evaluate cursor.execute(query text (CREATE)).
- Evaluate cursor.execute(“\\n                CREATE INDEX IF NOT EXISTS idx\_trigram\_lookup ON search\_trigrams(trigram)\\n            ”).
- Evaluate cursor.execute(“\\n                CREATE INDEX IF NOT EXISTS idx\_progress\_doctype ON search\_index\_progress(doctype)\\n            ”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L18) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L472)

<a id="op-f1390aa983b0e9"></a>
### SQLite Search.index documents

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_index_documents`

**Inputs** self, documents.

**Explicit results** no value.

**Local steps**

- If not documents.
  - Return no value.
- Set text\_fields from self.schema at “text\_fields”.
- Set metadata\_fields from self.schema at “metadata\_fields”.
- Set all\_fields from list(“doc\_id”, expanded text\_fields, expanded metadata\_fields).
- Set placeholders from “,”.join(list of “?” for \_ drawn from all\_fields).
  - Draw \_ from all\_fields.
- Set field\_names from “,”.join(all\_fields).
- Set insert\_sql from formatted text              INSERT INTO search\_fts ({field\_names})             VALUES ({placeholders}).
- Set chunk\_size from 1000.
- Bind local operation index\_chunks for subsequent calls.
- Evaluate self.\_with\_connection(index\_chunks).

If control reaches the end, it returns no value.

**Methods declared on this owner** [with connection](operations-064.md#op-e830239468f74c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L492)

<a id="op-e3ba09631799d2"></a>
### SQLite Search.index documents.index chunks

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_index_documents_index_chunks`

**Inputs** cursor.

**Local steps**

- For each i in range(0, len(documents), chunk\_size).
  - Set chunk from documents at slice i to (i + chunk\_size).
  - Set doc\_ids\_to\_delete from list().
  - Set values\_to\_insert from list().
  - For each doc in chunk.
    - If (not doc.get(“doctype”) or not doc.get(“name”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.get(“doctype”) → not doc.get(“name”).
      - Evaluate self.\_warn\_invalid\_document(doc, “missing doctype/name”).
      - Continue with the next iteration or loop test.
    - Set missing\_text\_fields from list().
    - For each field in text\_fields.
      - If (field does not belong to doc or doc at field is identical to no value).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in field does not belong to doc → doc at field is identical to no value.
        - Evaluate missing\_text\_fields.append(field).
    - If missing\_text\_fields.
      - Evaluate self.\_warn\_missing\_text\_fields(doc.get(“doctype”, empty text), doc.get(“name”, empty text), missing\_text\_fields).
      - Continue with the next iteration or loop test.
    - Set values from list().
    - Set doc\_id from no value.
    - For each field in all\_fields.
      - If field equals “doc\_id”.
        - Set doc\_id from (doc.get(“id”) or formatted text {doc.get(“doctype”, empty text)}:{doc.get(“name”, empty text)}).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“id”) → formatted text {doc.get(“doctype”, empty text)}:{doc.get(“name”, empty text)}.
        - Evaluate values.append(doc\_id).
      - Otherwise.
        - Evaluate values.append(strip\_surrogates(doc.get(field, empty text))).
    - Evaluate doc\_ids\_to\_delete.append(doc\_id).
    - Evaluate values\_to\_insert.append(tuple(values)).
  - If doc\_ids\_to\_delete.
    - Set placeholders\_for\_delete from “,”.join(list of “?” for \_ drawn from doc\_ids\_to\_delete).
      - Draw \_ from doc\_ids\_to\_delete.
    - Set delete\_sql from formatted text DELETE FROM search\_fts WHERE doc\_id IN ({placeholders\_for\_delete}).
    - Evaluate cursor.execute(delete\_sql, doc\_ids\_to\_delete).
  - If values\_to\_insert.
    - Evaluate cursor.executemany(insert\_sql, values\_to\_insert).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L1254) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L493)

<a id="op-14b9f241bc5479"></a>
### SQLite Search.index doc

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_index_record`

**Inputs** self, doctype, docname.

**Record and data access** resolve a document from doctype via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(doctype, docname).
- Evaluate self.raise\_if\_not\_indexed().
- Set document from self.prepare\_document(doc).
- If document.
  - Evaluate self.\_index\_documents(list(document)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [raise if not indexed](operations-063.md#op-a2bfedee778786), [prepare document](operations-064.md#op-6673d531411397), [index documents](operations-064.md#op-f1390aa983b0e9).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L19) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L495)

<a id="op-2a36c53f9b71e7"></a>
### SQLite Search.remove doc

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_remove_record`

**Inputs** self, doctype, docname.

**Local steps**

- Evaluate self.raise\_if\_not\_indexed().
- Set doc\_id from formatted text {doctype}:{docname}.
- Evaluate self.sql(query text (DELETE), tuple(doc\_id), commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [raise if not indexed](operations-063.md#op-a2bfedee778786), [sql](operations-064.md#op-98c6c287adfbb9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L22) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L513)

<a id="op-e65a7521912fc6"></a>
### SQLite Search.update progress

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_update_progress`

**Inputs** self, message, progress, total = 100, absolute = true.

**Local steps**

- If (not hasattr(Platform.local, “request”) and not Platform.flags.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not hasattr(Platform.local, “request”) → not Platform.flags.in\_test.
  - Evaluate update\_progress\_bar(message, progress, total, absolute = absolute).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L2703) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L521)

<a id="op-a841abed69d226"></a>
### SQLite Search.validate config

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_validate_configuration`

**Inputs** self.

**Explicit failure paths** ValueError(formatted text {field\_key.replace(“\_”, one space).title()} '{field\_value}' not found in 'fields' list for Doctype '{doctype}').

**Local steps**

- Set metadata\_fields from self.schema at “metadata\_fields”.
- For each tuple(doctype, config) in self.doc\_configs.items().
  - Set fields\_to\_check from list(“content\_field”, “title\_field”).
  - If “modified” belongs to metadata\_fields.
    - Evaluate fields\_to\_check.append(“modified\_field”).
  - For each field\_key in fields\_to\_check.
    - Set field\_value from config.get(field\_key).
    - If (field\_value and field\_value does not belong to config at “fields”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in field\_value → field\_value does not belong to config at “fields”.
      - Raise ValueError(formatted text {field\_key.replace(“\_”, one space).title()} '{field\_value}' not found in 'fields' list for Doctype '{doctype}').

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L2867) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L522)

<a id="op-bc0359069fdc9d"></a>
### SQLite Search.empty search result

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_empty_search_result`

**Inputs** self, title\_only = false, filters = no value.

**Explicit results** mapping(“results” → list(), “summary” → mapping(“total\_matches” → 0, “filtered\_matches” → 0, “duration” → 0, “returned\_matches” → 0, …)).

**Local steps**

- Return mapping(“results” → list(), “summary” → mapping(“total\_matches” → 0, “filtered\_matches” → 0, “duration” → 0, “returned\_matches” → 0, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L3227) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L470)

<a id="op-8beb4b31c64d76"></a>
### SQLite Search.get db path

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_get_database_path`

**Inputs** self, is\_temp = false.

**Explicit results** db\_path.replace(“.db”, “.temp.db”) · db\_path.

**Local steps**

- Set site\_path from Platform.get\_site\_path().
- Set db\_path from os.path.join(site\_path, self.db\_name).
- If is\_temp.
  - Return db\_path.replace(“.db”, “.temp.db”).
- Return db\_path.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L3415) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L479)

<a id="op-c374de2d0959d7"></a>
### SQLite Search.prepare fts query

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_prepare_fts_query`

**Inputs** self, query.

**Explicit results** empty text · one space.join(fts\_terms).

**Local steps**

- Set query from query.strip().
- If not query.
  - Return empty text.
- Set terms from query.split().
- Set fts\_terms from list().
- For each term in terms.
  - Set term from term.replace(“"”, “""”).
  - If len(term) &gt; (MIN\_WORD\_LENGTH − 1).
    - Evaluate fts\_terms.append(formatted text "{term}"\*).
  - Otherwise.
    - Evaluate fts\_terms.append(formatted text "{term}").
- Return one space.join(fts\_terms).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L3566) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L508)

<a id="op-98c6c287adfbb9"></a>
### SQLite Search.sql

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_database_query`

**Inputs** self, query, params = no value, read\_only = false, commit = false.

**Explicit results** cursor.fetchall() · cursor.

**Local steps**

- Set conn from self.\_get\_connection(read\_only = read\_only).
- Attempt the following.
  - Set cursor from conn.cursor().
  - Evaluate cursor.execute(query, (params or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in params → list().
  - If read\_only.
    - Return cursor.fetchall().
  - If commit.
    - Evaluate conn.commit().
  - Return cursor.
- On exit, including pending return or failure.
  - Evaluate conn.close().

**Methods declared on this owner** [get connection](operations-064.md#op-14564fd1bbcbd1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L3885) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L468)

<a id="op-6673d531411397"></a>
### SQLite Search.prepare document

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_prepare_document`

**Inputs** self, doc.

**Explicit results** no value · document.

**Local steps**

- Set tuple(is\_valid, config) from self.\_validate\_document\_for\_indexing(doc).
- If not is\_valid.
  - Return no value.
- Set document from mapping(“id” → formatted text {doc.doctype}:{doc.name}, “doctype” → doc.doctype, “name” → doc.name).
- Evaluate self.\_add\_text\_fields\_to\_document(document, doc, config).
- Evaluate self.\_add\_metadata\_fields\_to\_document(document, doc, config).
- Return document.

**Methods declared on this owner** [validate document for indexing](operations-064.md#op-ab2b27bee5a4b7), [add text fields to document](operations-064.md#op-caf89bf22b74f0), [add metadata fields to document](operations-065.md#op-251a425a075bf1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L4145) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L507)

<a id="op-ab2b27bee5a4b7"></a>
### SQLite Search.validate document for indexing

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_validate_document_for_indexing`

**Inputs** self, doc.

**Explicit results** tuple(false, no value) · tuple(true, config).

**Local steps**

- If (not hasattr(doc, “doctype”) or not doc.doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(doc, “doctype”) → not doc.doctype.
  - Evaluate self.\_warn\_missing\_doctype(doc).
  - Return tuple(false, no value).
- If (not hasattr(doc, “name”) or not doc.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(doc, “name”) → not doc.name.
  - Evaluate self.\_warn\_missing\_name(doc.doctype).
  - Return tuple(false, no value).
- Set config from self.doc\_configs.get(doc.doctype).
- If not config.
  - Return tuple(false, no value).
- Set text\_fields from self.schema at “text\_fields”.
- If “title” belongs to text\_fields.
  - Set title\_field from config.get(“title\_field”).
  - If (title\_field and (not hasattr(doc, title\_field) or getattr(doc, title\_field, no value) is identical to no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in title\_field → (not hasattr(doc, title\_field) or getattr(doc, title\_field, no value) is identical to no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(doc, title\_field) → getattr(doc, title\_field, no value) is identical to no value.
    - Evaluate self.\_warn\_missing\_title\_field(doc.doctype, doc.name, title\_field).
    - Return tuple(false, no value).
- If “content” belongs to text\_fields.
  - Set content\_field from config at “content\_field”.
  - If (not hasattr(doc, content\_field) or getattr(doc, content\_field, no value) is identical to no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(doc, content\_field) → getattr(doc, content\_field, no value) is identical to no value.
    - Evaluate self.\_warn\_missing\_content\_field(doc.doctype, doc.name, content\_field).
    - Return tuple(false, no value).
- Return tuple(true, config).

**Methods declared on this owner** [warn missing doctype](operations-065.md#op-7162677edc258e), [warn missing name](operations-065.md#op-363f1f596bdd01), [warn missing title field](operations-065.md#op-57f07feb9dc90b), [warn missing content field](operations-065.md#op-7be9b72bd69c90).

**Values supplied outside this operation** selected callable from getattr(doc, title\_field, no value), getattr(doc, content\_field, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L4425) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L523)

<a id="op-caf89bf22b74f0"></a>
### SQLite Search.add text fields to document

`operation_foundation_search_sqlite_search_business_behavior_supplier_quotation_lite_search_add_text_fields_to_document`

**Inputs** self, document, doc, config.

**Local steps**

- Set text\_fields from self.schema at “text\_fields”.
- Set title\_field from config.get(“title\_field”).
- Set content\_field from config at “content\_field”.
- For each field in text\_fields.
  - If field equals “title”.
    - If title\_field.
      - Set raw\_title from (getattr(doc, title\_field, empty text) or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(doc, title\_field, empty text) → empty text.
      - Set document at “title” from self.\_process\_content(raw\_title).
    - Otherwise.
      - Set document at “title” from empty text.
  - Otherwise.
    - If field equals “content”.
      - Set raw\_content from (getattr(doc, content\_field, empty text) or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(doc, content\_field, empty text) → empty text.
      - Set document at “content” from self.\_process\_content(raw\_content).
    - Otherwise.
      - Set raw\_text from getattr(doc, field, empty text).
      - Set document at field from self.\_process\_content(raw\_text).

If control reaches the end, it returns no value.

**Methods declared on this owner** [process content](operations-065.md#op-963cf5763d45d7).

**Values supplied outside this operation** selected callable from getattr(doc, title\_field, empty text), getattr(doc, content\_field, empty text) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0330.json#L5132) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L460)
