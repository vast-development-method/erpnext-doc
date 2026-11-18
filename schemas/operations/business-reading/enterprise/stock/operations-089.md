# Inventory and warehouses · operations 89

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock ledger

<a id="op-c413ecb125a379"></a>
### Validate cancellation

`operation_enterprise_stock_stock_ledger_business_behavior_validate_cancellation`

**Inputs** kargs.

**Record and data access** read “Repost Item Valuation” via get\_value · resolve a document from “Repost Item Valuation” via get\_doc.

**State and service calls** call cancel on doc.

**Explicit failure paths** validation helper — translated “Cannot cancel the transaction. Reposting of item valuation on submission is not completed yet.”.

**Local steps**

- If kargs at 0.get(“is\_cancelled”).
  - Set repost\_entry from Platform.db.get\_value(“Repost Item Valuation”, mapping(“voucher\_type” → kargs at 0.voucher\_type, “voucher\_no” → kargs at 0.voucher\_no, “docstatus” → 1, “recreate\_stock\_ledgers” → 0), list(“name”, “status”) ….
  - If repost\_entry.
    - If repost\_entry.status equals “In Progress”.
      - Call the validation error handler Platform.throw(translated “Cannot cancel the transaction. Reposting of item valuation on submission is not completed yet.”).
    - If repost\_entry.status equals “Queued”.
      - Set doc from Platform.get\_doc(“Repost Item Valuation”, repost\_entry.name).
      - Set doc.status from “Skipped”.
      - Set doc.flags.ignore\_permissions from true.
      - Evaluate doc.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0936.json#L2415) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L797)

<a id="op-d78b9af89abffa"></a>
### Set as cancel

`operation_enterprise_stock_stock_ledger_business_behavior_set_as_cancel`

**Inputs** voucher\_type, voucher\_no.

**State and service calls** execute a supplied database query.

**Local steps**

- Evaluate Platform.db.sql(“update ′tabStock Ledger Entry′ set is\_cancelled=1,\\n\\t\\tmodified=%s, modified\_by=%s\\n\\t\\twhere voucher\_type= …”, tuple(now(), Platform.session.user, voucher\_type, voucher\_no)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L742)

<a id="op-10361bc50b9bfd"></a>
### Make entry

`operation_enterprise_stock_stock_ledger_business_behavior_make_entry`

**Inputs** args, allow\_negative\_stock = false, via\_landed\_cost\_voucher = false, defer\_future\_dimension\_check = false.

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call submit on sle · call db\_set on sle.

**Explicit results** sle.

**Local steps**

- Set args at “doctype” from “Stock Ledger Entry”.
- Set sle from Platform.get\_doc(args).
- Set sle.flags.ignore\_permissions from 1.
- Set sle.flags.defer\_future\_dimension\_check from defer\_future\_dimension\_check.
- Set sle.allow\_negative\_stock from allow\_negative\_stock.
- Set sle.via\_landed\_cost\_voucher from via\_landed\_cost\_voucher.
- Evaluate sle.submit().
- If (args.get(“creation\_time”) and args.get(“voucher\_type”) equals “Stock Reconciliation”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“creation\_time”) → args.get(“voucher\_type”) equals “Stock Reconciliation”.
  - Evaluate sle.db\_set(“creation”, args.get(“creation\_time”)).
- Return sle.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L738)

<a id="op-98d544e00e4d3b"></a>
### Repost future sle

`operation_enterprise_stock_stock_ledger_business_behavior_repost_future_stock_ledger_entry`

**Inputs** items\_to\_be\_repost = no value, voucher\_type = no value, voucher\_no = no value, allow\_negative\_stock = no value, via\_landed\_cost\_voucher = false, doc = no value, allow\_zero\_rate = false.

**Explicit results** no value.

**Local steps**

- Set reposting\_data from mapping().
- If not items\_to\_be\_repost.
  - Set items\_to\_be\_repost from get\_items\_to\_be\_repost(voucher\_type = voucher\_type, voucher\_no = voucher\_no, doc = doc, reposting\_data = reposting\_data).
- If (doc and doc.reposting\_data\_file).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.reposting\_data\_file.
  - Set reposting\_data from get\_reposting\_data(doc.reposting\_data\_file).
- Set repost\_affected\_transaction from (get\_affected\_transactions(doc, reposting\_data) or set()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_affected\_transactions(doc, reposting\_data) → set().
- Set resume\_item\_wh\_wise\_last\_posted\_sle from (get\_item\_wh\_wise\_last\_posted\_sle\_from\_reposting\_data(doc, reposting\_data) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_wh\_wise\_last\_posted\_sle\_from\_reposting\_data(doc, reposting\_data) → mapping().
- If not items\_to\_be\_repost.
  - Return no value.
- Set is\_merged from is\_merged\_repost(doc, items\_to\_be\_repost).
- Set pending\_item\_wh from get\_pending\_item\_wh(reposting\_data, items\_to\_be\_repost) when is\_merged, otherwise list().
  - Value choice on is\_merged — true gives get\_pending\_item\_wh(reposting\_data, items\_to\_be\_repost), false gives list().
- Set index from (get\_current\_index(doc) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_current\_index(doc) → 0.
- While index &lt; len(items\_to\_be\_repost).
  - Evaluate validate\_item\_warehouse(items\_to\_be\_repost at index).
  - Set obj from update\_entries\_after(mapping(“item\_code” → items\_to\_be\_repost at index.get(“item\_code”), “warehouse” → items\_to\_be\_repost at index.get(“warehouse”), “posting\_date” → items\_to\_be\_repost at index.get(“postin ….
  - Set index from len(items\_to\_be\_repost) when is\_merged, otherwise (index + 1).
    - Value choice on is\_merged — true gives len(items\_to\_be\_repost), false gives (index + 1).
  - Set resume\_item\_wh\_wise\_last\_posted\_sle from mapping().
  - Evaluate repost\_affected\_transaction.update(obj.repost\_affected\_transaction).
  - Evaluate skip\_reposts\_covered\_by\_dependant\_repost(doc, obj.reposted\_dependant\_item\_wh).
  - Evaluate update\_args\_in\_repost\_item\_valuation(doc, index, items\_to\_be\_repost, repost\_affected\_transaction).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L741)

<a id="op-b340e725d1de83"></a>
### Is merged repost

`operation_enterprise_binding_enterprise_stock_stock_ledger_is_merged_repost`

**Inputs** doc, items\_to\_be\_repost.

**Explicit results** bool((doc and doc.based\_on equals “Item and Warehouse” and len(items\_to\_be\_repost) &gt; 1)).

**Local steps**

- Return bool((doc and doc.based\_on equals “Item and Warehouse” and len(items\_to\_be\_repost) &gt; 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.based\_on equals “Item and Warehouse” → len(items\_to\_be\_repost) &gt; 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1097)

<a id="op-ef0648c7724742"></a>
### Get pending item wh

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_pending_item_wh`

**Inputs** reposting\_data, items\_to\_be\_repost.

**Explicit results** list of Platform.\_dict(row) for row drawn from reposting\_data.pending\_item\_wh · list of Platform.\_dict(row) for row drawn from items\_to\_be\_repost at slice 1 to no value.

**Local steps**

- If (reposting\_data and “pending\_item\_wh” belongs to reposting\_data).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reposting\_data → “pending\_item\_wh” belongs to reposting\_data.
  - Return list of Platform.\_dict(row) for row drawn from reposting\_data.pending\_item\_wh.
    - Draw row from reposting\_data.pending\_item\_wh.
- Return list of Platform.\_dict(row) for row drawn from items\_to\_be\_repost at slice 1 to no value.
  - Draw row from items\_to\_be\_repost at slice 1 to no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1089)

<a id="op-219d40bb21a857"></a>
### Skip reposts covered by dependant repost

`operation_enterprise_binding_enterprise_stock_stock_ledger_skip_reposts_covered_by_dependant_repost`

**Inputs** doc, reposted\_dependant\_item\_wh.

**Explicit results** no value.

**Local steps**

- If (not doc or not reposted\_dependant\_item\_wh).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc → not reposted\_dependant\_item\_wh.
  - Return no value.
- Set riv from Platform.qb.DocType(“Repost Item Valuation”).
- For each tuple(tuple(item\_code, warehouse), posting\_datetime) in reposted\_dependant\_item\_wh.items().
  - If not posting\_datetime.
    - Continue with the next iteration or loop test.
  - Evaluate nested operand in the contract(nested operand in the contract).set(riv.status, “Skipped”).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in  ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1109)

<a id="op-d0e051d4442ab8"></a>
### Release reposting memory

`operation_enterprise_binding_enterprise_stock_stock_ledger_release_reposting_memory`

**Inputs** no declared parameters.

**Local steps**

- Set local\_cache from getattr(Platform.local, “cache”, no value).
- If isinstance(local\_cache, dict).
  - For each key in list of key for key drawn from local\_cache where byte value belongs to Platform.safe\_encode(key).
    - Draw key from local\_cache, keep a combination only if (byte value belongs to Platform.safe\_encode(key)).
    - Evaluate local\_cache.pop(key, no value).
- Set message\_log from getattr(Platform.local, “message\_log”, no value).
- If (message\_log and len(message\_log) &gt; REPOST\_MESSAGE\_LOG\_LIMIT).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in message\_log → len(message\_log) &gt; REPOST\_MESSAGE\_LOG\_LIMIT.
  - Set Platform.local.message\_log from message\_log at slice negative REPOST\_MESSAGE\_LOG\_LIMIT to no value.
- Evaluate gc.collect().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “cache”, no value), getattr(Platform.local, “message\_log”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1100)

<a id="op-6005f7b4f6ed95"></a>
### Update args in repost item valuation

`operation_enterprise_stock_stock_ledger_business_behavior_update_arguments_in_repost_item_valuation`

**Inputs** doc, index, items\_to\_be\_repost, repost\_affected\_transaction, item\_wh\_wise\_last\_posted\_sle = no value, pending\_item\_wh = no value.

**State and service calls** call db\_set on doc · commit · publish realtime with “item\_reposting\_progress”.

**Local steps**

- Set file\_name from empty text.
- If not item\_wh\_wise\_last\_posted\_sle.
  - Set item\_wh\_wise\_last\_posted\_sle from mapping().
- If doc.reposting\_data\_file.
  - Set file\_name from get\_reposting\_file\_name(doc.doctype, doc.name).
- Set doc.reposting\_data\_file from create\_json\_gz\_file(mapping(“repost\_affected\_transaction” → repost\_affected\_transaction, “item\_wh\_wise\_last\_posted\_sle” → (mapping of str(k) → v for tuple(k, v) drawn from item\_wh\_wise\_last\_posted\_sle.item ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in mapping of str(k) → v for tuple(k, v) drawn from item\_wh\_wise\_last\_posted\_sle.items() → mapping().
  - Draw tuple(k, v) from item\_wh\_wise\_last\_posted\_sle.items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pending\_item\_wh → list().
- Evaluate doc.db\_set(mapping(“current\_index” → index, “items\_to\_be\_repost” → Platform.as\_json(items\_to\_be\_repost), “total\_reposting\_count” → len(items\_to\_be\_repost), “reposting\_data\_file” → doc.reposting\_data\_file)).
- If not Platform.in\_test.
  - Evaluate Platform.db.commit().
- Evaluate Platform.publish\_realtime(“item\_reposting\_progress”, mapping(“name” → doc.name, “current\_index” → index, “total\_reposting\_count” → len(items\_to\_be\_repost)), doctype = doc.doctype, docname = doc.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“item\_reposting\_progress”, mapping(“name” → doc.name, “current\_index” → index, “total\_reposting\_count” → len(items\_to\_be\_repost)), doctype = doc.doctype, docname = doc.name).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L743)

<a id="op-1277013563f634"></a>
### Get reposting file name

`operation_enterprise_stock_stock_ledger_business_behavior_get_reposting_file_name`

**Inputs** dt, dn.

**Record and data access** read “File” via get\_value.

**Explicit results** Platform.db.get\_value(“File”, mapping(“attached\_to\_doctype” → dt, “attached\_to\_name” → dn, “attached\_to\_field” → “reposting\_data\_file”), “name”).

**Local steps**

- Return Platform.db.get\_value(“File”, mapping(“attached\_to\_doctype” → dt, “attached\_to\_name” → dn, “attached\_to\_field” → “reposting\_data\_file”), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0936.json#L5460) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L725)

<a id="op-32229674eaa289"></a>
### Create json gz file

`operation_enterprise_stock_stock_ledger_business_behavior_create_structured_data_gz_file`

**Inputs** data, doc, file\_name = no value.

**Declared result** str.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** create\_file(doc, compressed\_content) · doc.reposting\_data\_file.

**Local steps**

- Set encoded\_content from Platform.safe\_encode(Platform.as\_json(data)).
- Set compressed\_content from gzip.compress(encoded\_content).
- If not file\_name.
  - Return create\_file(doc, compressed\_content).
- Otherwise.
  - Set file\_doc from Platform.get\_doc(“File”, file\_name).
  - If “/Platform\_s3\_attachment.” belongs to file\_doc.file\_url.
    - Evaluate file\_doc.delete().
    - Return create\_file(doc, compressed\_content).
  - Set path from file\_doc.get\_full\_path().
  - Within open(path, “wb”) bound as f.
    - Evaluate f.write(compressed\_content).
  - Return doc.reposting\_data\_file.

**Boundaries to resolve** stored data, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0936.json#L5597) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L709)

<a id="op-2b3aefd9e7a1d0"></a>
### Create file

`operation_enterprise_stock_stock_ledger_business_behavior_create_file`

**Inputs** doc, compressed\_content.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → json\_filename, “attached\_to\_doctype” → doc.doctype, “attached\_to\_name” → doc.name, …) via get\_doc.

**State and service calls** call save on \_file.

**Explicit results** \_file.file\_url.

**Local steps**

- Set json\_filename from formatted text {scrub(doc.doctype)}-{scrub(doc.name)}.json.gz.
- Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → json\_filename, “attached\_to\_doctype” → doc.doctype, “attached\_to\_name” → doc.name, …)).
- Evaluate \_file.save(ignore\_permissions = true).
- Return \_file.file\_url.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0936.json#L5964) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L708)

<a id="op-4ac9ae2b89dca4"></a>
### Validate item warehouse

`operation_enterprise_stock_stock_ledger_business_behavior_validate_item_warehouse`

**Inputs** args.

**Explicit failure paths** validation helper — translated validation\_msg.

**Local steps**

- For each field in list(“item\_code”, “warehouse”, “posting\_date”, “posting\_time”).
  - If args.get(field) belongs to list(no value, empty text).
    - Set validation\_msg from formatted text The field {Platform.unscrub(field)} is required for the reposting.
    - Call the validation error handler Platform.throw(translated validation\_msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L798)

<a id="op-253119b389a6ee"></a>
### Get items to be repost

`operation_enterprise_stock_stock_ledger_business_behavior_get_items_to_be_repost`

**Inputs** voucher\_type = no value, voucher\_no = no value, doc = no value, reposting\_data = no value.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** reposting\_data.items\_to\_be\_repost · (items\_to\_be\_repost or list()).

**Local steps**

- If (reposting\_data and reposting\_data.items\_to\_be\_repost).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reposting\_data → reposting\_data.items\_to\_be\_repost.
  - Return reposting\_data.items\_to\_be\_repost.
- Set items\_to\_be\_repost from list().
- If (doc and doc.items\_to\_be\_repost).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.items\_to\_be\_repost.
  - Set items\_to\_be\_repost from json.loads(doc.items\_to\_be\_repost).
- If (not items\_to\_be\_repost and voucher\_type and voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not items\_to\_be\_repost → voucher\_type → voucher\_no.
  - Set items\_to\_be\_repost from Platform.db.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no), fields = list(“item\_code”, “warehouse”, “posting\_date”, “posting\_time”, …), order\_by = ….
- Return (items\_to\_be\_repost or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in items\_to\_be\_repost → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L719)

<a id="op-2e452797c337fb"></a>
### Get affected transactions

`operation_enterprise_stock_stock_ledger_business_behavior_get_affected_transactions`

**Inputs** doc, reposting\_data = no value.

**Declared result** set at tuple at tuple(str, str).

**Explicit results** set of tuple(transaction) for transaction drawn from reposting\_data.repost\_affected\_transaction · set().

**Local steps**

- If (not reposting\_data and doc and doc.reposting\_data\_file).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not reposting\_data → doc → doc.reposting\_data\_file.
  - Set reposting\_data from get\_reposting\_data(doc.reposting\_data\_file).
- If (reposting\_data and reposting\_data.repost\_affected\_transaction).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reposting\_data → reposting\_data.repost\_affected\_transaction.
  - Return set of tuple(transaction) for transaction drawn from reposting\_data.repost\_affected\_transaction.
    - Draw transaction from reposting\_data.repost\_affected\_transaction.
- Return set().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L710)

<a id="op-9f42c15367e011"></a>
### Get item wh wise last posted sle from reposting data

`operation_enterprise_stock_stock_ledger_business_behavior_get_item_warehouse_wise_last_posted_stock_ledger_entry_from_reposting_data`

**Inputs** doc, reposting\_data = no value.

**Explicit results** Platform.\_dict(reposting\_data.item\_wh\_wise\_last\_posted\_sle) · Platform.\_dict().

**Local steps**

- If (not reposting\_data and doc and doc.reposting\_data\_file).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not reposting\_data → doc → doc.reposting\_data\_file.
  - Set reposting\_data from get\_reposting\_data(doc.reposting\_data\_file).
- If (reposting\_data and reposting\_data.item\_wh\_wise\_last\_posted\_sle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reposting\_data → reposting\_data.item\_wh\_wise\_last\_posted\_sle.
  - Return Platform.\_dict(reposting\_data.item\_wh\_wise\_last\_posted\_sle).
- Return Platform.\_dict().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L718)

<a id="op-3d355798326657"></a>
### Get reposting data

`operation_enterprise_stock_stock_ledger_business_behavior_get_reposting_data`

**Inputs** file\_path.

**Declared result** dict.

**Record and data access** read “File” via get\_value · resolve a document from “File” via get\_doc.

**Explicit results** Platform.\_dict() · parse\_json(data).

**Local steps**

- Set file\_name from Platform.db.get\_value(“File”, mapping(“file\_url” → file\_path, “attached\_to\_field” → “reposting\_data\_file”), “name”).
- If not file\_name.
  - Return Platform.\_dict().
- Set attached\_file from Platform.get\_doc(“File”, file\_name).
- Set content from attached\_file.get\_content(encodings = tuple()).
- If isinstance(content, str).
  - Set content from content.encode(“utf-8”).
- Attempt the following.
  - Set data from gzip.decompress(content).
- On failure (Exception).
  - Return Platform.\_dict().
- If data bound to json.loads(data.decode(“utf-8”)).
  - Set data from data.
- Return parse\_json(data).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L724)

<a id="op-881069f156cfff"></a>
### Get current index

`operation_enterprise_stock_stock_ledger_business_behavior_get_current_index`

**Inputs** doc = no value.

**Explicit results** doc.current\_index.

**Local steps**

- If (doc and doc.current\_index).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.current\_index.
  - Return doc.current\_index.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L1019) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L712)

<a id="op-1a3c2e884457a4"></a>
### Update entries after.initialize

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_initialize`

**Inputs** self, args, allow\_zero\_rate = false, allow\_negative\_stock = no value, via\_landed\_cost\_voucher = false, verbose = 1.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Local steps**

- Set self.exceptions from mapping().
- Set self.verbose from verbose.
- Set self.allow\_zero\_rate from allow\_zero\_rate.
- Set self.via\_landed\_cost\_voucher from via\_landed\_cost\_voucher.
- Set self.item\_code from args.get(“item\_code”).
- Set self.stock\_ledgers\_to\_repost from list().
- Set self.current\_idx from args.get(“current\_idx”, 0).
- Set self.repost\_doc from (args.get(“repost\_doc”) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“repost\_doc”) → no value.
- Set self.items\_to\_be\_repost from (args.get(“items\_to\_be\_repost”) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“items\_to\_be\_repost”) → no value.
- Set self.force\_negative\_stock from allow\_negative\_stock.
- Set self.args from Platform.\_dict(args).
- If self.args.sle\_id.
  - Set self.args at “name” from self.args.sle\_id.
- Set self.prev\_sle\_dict from Platform.\_dict(mapping()).
- Set self.company from Platform.get\_cached\_value(“Warehouse”, self.args.warehouse, “company”).
- Evaluate self.set\_precision().
- Evaluate self.set\_item\_settings(self.item\_code).
- Set self.repost\_affected\_transaction from (args.get(“repost\_affected\_transaction”) or set()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“repost\_affected\_transaction”) → set().
- Set self.new\_items\_found from false.
- Set self.reposted\_dependant\_item\_wh from mapping().
- Set self.recalculated\_stock\_entries from set().
- Set self.reserved\_stock from mapping().
- Set self.data from Platform.\_dict().
- If ((not self.repost\_doc or not self.args.get(“item\_wh\_wise\_last\_posted\_sle”)) and not self.args.get(“cancelled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not self.repost\_doc or not self.args.get(“item\_wh\_wise\_last\_posted\_sle”)) → not self.args.get(“cancelled”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.repost\_doc → not self.args.get(“item\_wh\_wise\_last\_posted\_sle”).
  - Evaluate self.initialize\_previous\_data(self.args).
- Evaluate self.build().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set precision](operations-089.md#op-8ce3165924917a), [set item settings](operations-089.md#op-1fa6c84a31bec4), [initialize previous data](operations-089.md#op-e5022846c02f01), [build](operations-089.md#op-c5753537303c71).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, self.args.warehouse, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L765)

<a id="op-1fa6c84a31bec4"></a>
### Update entries after.set item settings

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_set_item_settings`

**Inputs** self, item\_code.

**Local steps**

- Set self.valuation\_method from get\_valuation\_method(item\_code, self.company).
- Set self.skip\_serial\_batch\_valuation from is\_serial\_no\_wise\_valuation\_disabled(item\_code).
- Set self.allow\_negative\_stock from (self.force\_negative\_stock or is\_negative\_stock\_allowed(item\_code = item\_code)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.force\_negative\_stock → is\_negative\_stock\_allowed(item\_code = item\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1125)

<a id="op-c1d0e0e037b732"></a>
### Update entries after.get reserved stock

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_reserved_stock`

**Inputs** self, item\_code, warehouse.

**Explicit results** self.reserved\_stock at tuple(item\_code, warehouse).

**Local steps**

- If tuple(item\_code, warehouse) belongs to self.reserved\_stock.
  - Return self.reserved\_stock at tuple(item\_code, warehouse).
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set posting\_datetime from get\_combine\_datetime(self.args.posting\_date, self.args.posting\_time).
- Set query from nested operand in the contract(nested operand in the contract).select((nested operand in the contract(nested operand in the contract) − (nested operand in the contract + nested operand in the contract))).w ….run().
- Set self.reserved\_stock at tuple(item\_code, warehouse) from flt(query at 0 at 0) when query, otherwise 0.0.
  - Value choice on query — true gives flt(query at 0 at 0), false gives 0.0.
- Return self.reserved\_stock at tuple(item\_code, warehouse).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L758)

<a id="op-8ce3165924917a"></a>
### Update entries after.set precision

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_set_precision`

**Inputs** self.

**Local steps**

- Set self.flt\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set self.currency\_precision from get\_field\_precision(Platform.get\_meta(“Stock Ledger Entry”).get\_field(“stock\_value”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L2426) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1270) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L779)

<a id="op-e5022846c02f01"></a>
### Update entries after.initialize previous data

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_initialize_previous_data`

**Inputs** self, args.

**Explicit results** no value.

**Local steps**

- Evaluate self.data.setdefault(args.warehouse, Platform.\_dict()).
- Set warehouse\_dict from self.data at args.warehouse.
- If self.stock\_ledgers\_to\_repost.
  - Return no value.
- Set previous\_sle from get\_previous\_sle\_of\_current\_voucher(args).
- If previous\_sle.
  - Set self.prev\_sle\_dict at tuple(args.get(“item\_code”), args.get(“warehouse”)) from previous\_sle.
- Set warehouse\_dict.previous\_sle from previous\_sle.
- For each key in tuple(“qty\_after\_transaction”, “valuation\_rate”, “stock\_value”).
  - Evaluate setattr(warehouse\_dict, key, flt(previous\_sle.get(key))).
- Evaluate warehouse\_dict.update(mapping(“prev\_stock\_value” → (previous\_sle.stock\_value or 0.0), “stock\_queue” → json.loads((previous\_sle.stock\_queue or “&#91;&#93;”)), “stock\_value\_difference” → 0.0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_sle.stock\_value → 0.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_sle.stock\_queue → “&#91;&#93;”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L2597) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L766)

<a id="op-c5753537303c71"></a>
### Update entries after.build

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_build`

**Inputs** self.

**Local steps**

- Bind dependencies future\_sle\_exists.
- If self.args.get(“sle\_id”).
  - Evaluate self.process\_sle\_against\_current\_timestamp().
  - If not future\_sle\_exists(self.args).
    - Evaluate self.update\_bin().
- Otherwise.
  - Set self.item\_wh\_wise\_last\_posted\_sle from self.get\_item\_wh\_wise\_last\_posted\_sle().
  - Set item\_wh\_sles from self.sort\_sles(self.item\_wh\_wise\_last\_posted\_sle.values()).
  - Evaluate self.initialize\_reposting().
  - Evaluate self.repost\_stock\_ledgers(item\_wh\_sles).
  - Evaluate self.update\_bin().
  - Evaluate self.reset\_vouchers\_and\_idx().
  - Evaluate self.update\_data\_in\_repost().
- If self.exceptions.
  - Evaluate self.raise\_exceptions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [process sle against current timestamp](operations-090.md#op-31e8ca5a4a1ad3), [update bin](operations-092.md#op-c5fac748dec1e2), [get item wh wise last posted sle](operations-090.md#op-435610859d0a07), [sort sles](operations-090.md#op-5c39223d127579), [initialize reposting](operations-090.md#op-a5278f4a553f43), [repost stock ledgers](operations-090.md#op-593540cd75c01d), [reset vouchers and idx](operations-090.md#op-5c392ed17aa5f6), [update data in repost](operations-090.md#op-eb4dadf43af862), [raise exceptions](operations-092.md#op-b6e382dbba0f4c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0937.json#L3067) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L744)
