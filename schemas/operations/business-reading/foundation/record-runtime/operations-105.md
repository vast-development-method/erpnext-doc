# Record lifecycle and persistence · operations 105

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-aff9c88294b640"></a>
### Find all

`operation_foundation_core_utils_business_behavior_find_all`

**Inputs** list\_of\_dict, match\_function.

**Explicit results** list of entry for entry drawn from list\_of\_dict where match\_function(entry).

**Local steps**

- Return list of entry for entry drawn from list\_of\_dict where match\_function(entry).
  - Draw entry from list\_of\_dict, keep a combination only if (match\_function(entry)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L6951) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L918)

<a id="op-bc5020f10c5e27"></a>
### Ljust list

`operation_foundation_core_utils_business_behavior_ljust_list`

**Inputs** \_list, length, fill\_word = no value.

**Explicit results** \_list.

**Local steps**

- Set \_list from list(\_list).
- Set fill\_length from (length − len(\_list)).
- If fill\_length &gt; 0.
  - Evaluate \_list.extend((list(fill\_word) × fill\_length)).
- Return \_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L7031) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L920)

<a id="op-3f3c409b1e8e9f"></a>
### Html2text

`operation_foundation_core_utils_business_behavior_document_markup_2_text`

**Inputs** html, strip\_links = false, wrap = true.

**Declared result** str.

**Explicit results** md(html, heading\_style = “ATX”, strip = strip, wrap = wrap).

**Local steps**

- Bind dependencies md.
- Set strip from list(“a”) when strip\_links, otherwise no value.
  - Value choice on strip\_links — true gives list(“a”), false gives no value.
- Return md(html, heading\_style = “ATX”, strip = strip, wrap = wrap).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0121.json#L7202) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L915)

<a id="op-6564b094e2ab6d"></a>
### Html to plain text

`operation_foundation_core_utils_business_behavior_document_markup_to_plain_text`

**Inputs** html.

**Declared result** str.

**Explicit results** empty text · whitespace '\\n'.join(cleaned).strip().

**Local steps**

- If not html.
  - Return empty text.
- Bind dependencies BeautifulSoup.
- Set soup from BeautifulSoup(html, “html.parser”).
- For each element in soup(list(“script”, “style”)).
  - Evaluate element.decompose().
- For each br in soup.find\_all(“br”).
  - Evaluate br.replace\_with(whitespace '\\n').
- For each block in soup.find\_all(list(“p”, “div”, “tr”, “li”, …)).
  - Evaluate block.append(whitespace '\\n').
- Set text from soup.get\_text(separator = one space).
- Set lines from list of line.strip() for line drawn from text.splitlines().
  - Draw line from text.splitlines().
- Set cleaned from list().
- Set previous\_blank from false.
- For each line in lines.
  - If line.
    - Evaluate cleaned.append(line).
    - Set previous\_blank from false.
  - Otherwise.
    - If not previous\_blank.
      - Evaluate cleaned.append(empty text).
    - Set previous\_blank from true.
- Return whitespace '\\n'.join(cleaned).strip().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L916)

<a id="op-15d539fbe690ce"></a>
### Convert backtick identifiers

`operation_foundation_database_utils_business_behavior_convert_backtick_identifiers`

**Inputs** query.

**Declared result** str.

**Explicit results** query · SKIPPED\_SPAN\_PATTERN.sub(translate, query).

**Local steps**

- If “′” does not belong to query.
  - Return query.
- Bind local operation translate for subsequent calls.
- Return SKIPPED\_SPAN\_PATTERN.sub(translate, query).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L4533) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1526)

<a id="op-2ac480f544759e"></a>
### Convert backtick identifiers.translate

`operation_foundation_database_utils_business_behavior_convert_backtick_identifiers_translate`

**Inputs** match.

**Declared result** str.

**Explicit results** span · “"{}"”.format(name.replace(“"”, “""”)).

**Local steps**

- Set span from match.group().
- If not span.startswith(“′”).
  - Return span.
- Set name from span at slice 1 to negative 1.replace(“′′”, “′”).
- Return “"{}"”.format(name.replace(“"”, “""”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L4807) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1527)

<a id="op-0ecf0ff2d9567c"></a>
### Convert to value

`operation_foundation_database_utils_business_behavior_convert_to_value`

**Inputs** o.

**Explicit results** int(o) · Platform.as\_json(o) · tuple(generator of convert\_to\_value(item) for item drawn from o) · o.

**Local steps**

- If isinstance(o, bool).
  - Return int(o).
- Otherwise.
  - If isinstance(o, dict).
    - Return Platform.as\_json(o).
  - Otherwise.
    - If isinstance(o, tuple(KeysView, ValuesView)).
      - Return tuple(generator of convert\_to\_value(item) for item drawn from o).
        - Draw item from o.
- Return o.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L5003) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1528)

<a id="op-16a6145266db75"></a>
### Get query type

`operation_foundation_database_utils_business_behavior_get_query_type`

**Inputs** query.

**Declared result** str.

**Explicit results** QUERY\_TYPE\_PATTERN.match(query) at 1.lower().

**Local steps**

- Return QUERY\_TYPE\_PATTERN.match(query) at 1.lower().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L5585) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1532)

<a id="op-700895aa41b921"></a>
### Is query type

`operation_foundation_database_utils_business_behavior_is_query_type`

**Inputs** query, query\_type.

**Declared result** bool.

**Explicit results** get\_query\_type(query).startswith(query\_type).

**Local steps**

- Return get\_query\_type(query).startswith(query\_type).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L5664) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1536)

<a id="op-9af77a801501f8"></a>
### Is pypika function object

`operation_foundation_database_utils_business_behavior_is_query_builder_function_object`

**Inputs** field.

**Declared result** bool.

**Explicit results** (getattr(field, “\_\_module\_\_”, no value) equals “pypika.functions” or isinstance(field, Function)).

**Local steps**

- Return (getattr(field, “\_\_module\_\_”, no value) equals “pypika.functions” or isinstance(field, Function)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(field, “\_\_module\_\_”, no value) equals “pypika.functions” → isinstance(field, Function).

**Values supplied outside this operation** selected callable from getattr(field, “\_\_module\_\_”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L5779) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1535)

<a id="op-26c9c9abfb638b"></a>
### Get doctype name

`operation_foundation_database_utils_business_behavior_get_record_type_name`

**Inputs** table\_name.

**Declared result** str.

**Explicit results** table\_name.replace(“"”, empty text).

**Local steps**

- If table\_name.startswith(tuple(“tab”, “′tab”, “"tab”)).
  - Set table\_name from table\_name.replace(“tab”, empty text, 1).
- Set table\_name from table\_name.replace(“′”, empty text).
- Return table\_name.replace(“"”, empty text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L5881) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1533)

<a id="op-3c9fa37d4efd7c"></a>
### Get doctype sort info

`operation_foundation_database_utils_business_behavior_get_record_type_sort_info`

**Inputs** doctype.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(“creation”, “DESC”) · tuple((meta.sort\_field or “creation”), (meta.sort\_order or “DESC”)).

**Local steps**

- Bind dependencies CORE\_DOCTYPES.
- If doctype belongs to CORE\_DOCTYPES.
  - Return tuple(“creation”, “DESC”).
- Attempt the following.
  - Set meta from Platform.get\_meta(doctype).
  - Return tuple((meta.sort\_field or “creation”), (meta.sort\_order or “DESC”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.sort\_field → “creation”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.sort\_order → “DESC”.
- On failure (Platform.DoesNotExistError).
  - Return tuple(“creation”, “DESC”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L6053) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1534)

<a id="op-c8e9642a8dea48"></a>
### Lazy String.setup

`operation_foundation_database_utils_business_behavior_lazy_string_setup`

**Inputs** self.

**Declared result** str.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L6793) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1542)

<a id="op-453661ba030b18"></a>
### Lazy String.value

`operation_foundation_database_utils_business_behavior_lazy_string_value`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** str.

**Explicit results** self.\_setup().

**Local steps**

- Return self.\_setup().

**Methods declared on this owner** [setup](operations-105.md#op-c8e9642a8dea48).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L6837) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1544)

<a id="op-d21fb10bd4f964"></a>
### Lazy String.str

`operation_foundation_database_utils_business_behavior_lazy_string_text`

**Inputs** self.

**Declared result** str.

**Explicit results** self.value.

**Local steps**

- Return self.value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L6895) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1543)

<a id="op-d308ab4415fd4b"></a>
### Lazy String.repr

`operation_foundation_database_utils_business_behavior_lazy_string_representation`

**Inputs** self.

**Declared result** str.

**Explicit results** formatted text '{self.value}'.

**Local steps**

- Return formatted text '{self.value}'.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L6938) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1541)

<a id="op-adf76d6595555c"></a>
### Lazy Decode.initialize

`operation_foundation_database_utils_business_behavior_lazy_decode_initialize`

**Inputs** self, value.

**Declared result** no value.

**Local steps**

- Set self.\_value from value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L7001) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1537)

<a id="op-4760a9642c6e33"></a>
### Lazy Decode.setup

`operation_foundation_database_utils_business_behavior_lazy_decode_setup`

**Inputs** self.

**Declared result** str.

**Explicit results** self.\_value.decode().

**Local steps**

- Return self.\_value.decode().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L7060) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1538)

<a id="op-d7ec7b96c39f46"></a>
### Lazy Mogrify.initialize

`operation_foundation_database_utils_business_behavior_lazy_mogrify_initialize`

**Inputs** self, query, values.

**Declared result** no value.

**Local steps**

- Set self.query from query.
- Set self.values from values.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L7115) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1539)

<a id="op-2fba9a8642221e"></a>
### Lazy Mogrify.setup

`operation_foundation_database_utils_business_behavior_lazy_mogrify_setup`

**Inputs** self.

**Declared result** str.

**Explicit results** Platform.db.mogrify(self.query, self.values).

**Local steps**

- Return Platform.db.mogrify(self.query, self.values).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L7193) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1540)

<a id="op-83198765e44070"></a>
### Dangerously reconnect on connection abort

`operation_foundation_database_utils_business_behavior_dangerously_reconnect_on_connection_abort`

**Inputs** func.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L7265) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1529)

<a id="op-ade0ee650cf320"></a>
### Dangerously reconnect on connection abort.wrapper

`operation_foundation_database_utils_business_behavior_dangerously_reconnect_on_connection_abort_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** func(expanded args, expanded names kwargs).

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Return func(expanded args, expanded names kwargs).
- On failure (Exception) bound to e.
  - If (Platform.db.is\_interface\_error(e) or isinstance(e, Platform.db.OperationalError)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.is\_interface\_error(e) → isinstance(e, Platform.db.OperationalError).
    - Evaluate Platform.db.connect().
    - Return func(expanded args, expanded names kwargs).
  - Propagate the active failure.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L7518) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1530)

<a id="op-0aa5d02321da24"></a>
### Commit After Response Manager.run

`operation_foundation_database_utils_business_behavior_commit_after_response_manager_run`

**Inputs** self.

**Local steps**

- Set db from getattr(Platform.local, “db”, no value).
- If not db.
  - Evaluate Platform.connect(set\_admin\_as\_user = false).
  - Set db from Platform.local.db.
- Set savepoint\_name from “commit\_after\_response”.
- While self.\_functions.
  - Set \_func from self.\_functions.popleft().
  - Attempt the following.
    - Evaluate db.savepoint(savepoint\_name).
    - Evaluate \_func().
  - On failure (Exception).
    - Evaluate db.rollback(save\_point = savepoint\_name).
    - Evaluate Platform.log\_error(title = “Error executing commit\_after\_response callback”).
- Evaluate db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “db”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L7747) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1525)

<a id="op-f1f59a0062ad49"></a>
### Commit after response

`operation_foundation_database_utils_business_behavior_commit_after_response`

**Inputs** func.

**Explicit results** no value.

**Local steps**

- Set request from getattr(Platform.local, “request”, false).
- If (not request or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not request → Platform.in\_test.
  - Evaluate func().
  - Return no value.
- Set callback\_manager from getattr(request, “commit\_after\_response”, no value).
- If callback\_manager is identical to no value.
  - Set callback\_manager from CommitAfterResponseManager().
  - Set request.commit\_after\_response from callback\_manager.
  - Evaluate request.after\_response.add(callback\_manager.run).
- Evaluate callback\_manager.add(func).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request”, false), getattr(request, “commit\_after\_response”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1524)
