# Shared transaction rules · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock controller

<a id="op-a502a5681ce9b7"></a>
### Stock Controller.rebuild subcontracting transfers

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_rebuild_subcontracting_transfers`

**Inputs** self, sre\_lists.

**Record and data access** resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_update on entry · call db\_update on sre\_doc.

**Local steps**

- Set transfers from self.get\_subcontracting\_transfers(list(sre\_lists)).
- For each tuple(sco\_rm\_detail, sre\_list) in sre\_lists.items().
  - Set sre\_docs from list of Platform.get\_doc(“Stock Reservation Entry”, sre) for sre drawn from sre\_list.
    - Draw sre from sre\_list.
  - For each sre\_doc in sre\_docs.
    - Set sre\_doc.transferred\_qty from 0.
    - For each entry in sre\_doc.sb\_entries.
      - Set entry.delivered\_qty from 0.
  - For each transfer in transfers.get(sco\_rm\_detail, list()).
    - For each sre\_doc in sre\_docs.
      - If sre\_doc.creation &lt; transfer.submitted\_at.
        - Evaluate add\_transfer\_to\_reservation(sre\_doc, transfer).
  - For each sre\_doc in sre\_docs.
    - For each entry in sre\_doc.sb\_entries.
      - Evaluate entry.db\_update().
    - Evaluate sre\_doc.db\_update().
    - Evaluate sre\_doc.update\_reserved\_qty\_in\_voucher().
    - Evaluate sre\_doc.update\_status().
    - Evaluate sre\_doc.update\_reserved\_stock\_in\_bin().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get subcontracting transfers](operations-027.md#op-d44a778fe8c836).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1161) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L401)

<a id="op-d44a778fe8c836"></a>
### Stock Controller.get subcontracting transfers

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_subcontracting_transfers`

**Inputs** self, sco\_rm\_details.

**Declared result** dict at tuple(str, list).

**Explicit results** mapping of row → list(row\_transfers.values()) for tuple(row, row\_transfers) drawn from transfers.items().

**Local steps**

- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set detail from Platform.qb.DocType(“Stock Entry Detail”).
- Set ledger\_entry from Platform.qb.DocType(“Stock Ledger Entry”).
- Set bundle\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set submitted\_at from nested operand in the contract(nested operand in the contract).select(Min(nested operand in the contract.creation)).where(ledger\_entry.voucher\_detail\_no equals detail.name).as\_(“submitted\_at”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Set transfers from defaultdict(dict).
- For each row in rows.
  - Set transfer from transfers at row.sco\_rm\_detail.get(row.name).
  - If not transfer.
    - Set transfer, transfers at row.sco\_rm\_detail at row.name from new\_reservation\_transfer().
    - Set tuple(transfer.qty, transfer.submitted\_at) from tuple(flt(row.transfer\_qty), row.submitted\_at).
  - If row.serial\_no.
    - Evaluate transfer.serial\_nos.add(row.serial\_no).
  - If row.batch\_no.
    - Update transfer.batch\_qty at row.batch\_no using + abs(flt(row.qty)).
- Return mapping of row → list(row\_transfers.values()) for tuple(row, row\_transfers) drawn from transfers.items().
  - Draw tuple(row, row\_transfers) from transfers.items().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L389)

<a id="op-8f04ec8cb1b7f7"></a>
### Stock Controller.check for on hold or closed status

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_check_for_on_hold_or_closed_status`

**Inputs** self, ref\_doctype, ref\_fieldname, exclude\_if\_field = no value.

**Declared result** no value.

**Record and data access** read ref\_doctype via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — text in the contract.join(errors).

**Local steps**

- Bind local operation \_include for subsequent calls.
- Set included from list of tuple(d, d.get(ref\_fieldname)) for d drawn from self.get(“items”) where \_include(d).
  - Draw d from self.get(“items”), keep a combination only if (\_include(d)).
- If not included.
  - Return no value.
- Set status\_map from mapping of r.name → r.status for r drawn from Platform.get\_all(ref\_doctype, filters = mapping(“name” → list(“in”, set of name for tuple(\_, name) drawn from included)), fields = list(“name”, “status”)).
  - Draw r from Platform.get\_all(ref\_doctype, filters = mapping(“name” → list(“in”, set of name for tuple(\_, name) drawn from included)), fields = list(“name”, “status”)).
  - Draw tuple(\_, name) from included.
- Set errors from list().
- Set seen from set().
- For each tuple(\_d, ref\_name) in included.
  - If ref\_name belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(ref\_name).
  - If status bound to status\_map.get(ref\_name) belongs to tuple(“Closed”, “On Hold”).
    - Evaluate errors.append(translated “{ref\_doctype} {ref\_name} status is {status}.”.format(ref\_doctype = Platform.bold(translated ref\_doctype), ref\_name = Platform.bold(ref\_name), status = Platform.bold(translated status))).
- If errors.
  - Call the validation error handler Platform.throw(text in the contract.join(errors), Platform.InvalidStatusError).

If control reaches the end, it returns no value.

**Derived worked case from the contract** Rows referencing a held A twice and a closed B once raise one combined error containing A and B once each.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0442.json#L441) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L631) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-fa11258f8513e4"></a>
### Stock Controller.check for on hold or closed status.include

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_check_for_on_hold_or_closed_status_include`

**Inputs** d.

**Explicit results** (d.get(ref\_fieldname) and not (exclude\_if\_field and d.get(exclude\_if\_field))).

**Local steps**

- Return (d.get(ref\_fieldname) and not (exclude\_if\_field and d.get(exclude\_if\_field))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(ref\_fieldname) → not (exclude\_if\_field and d.get(exclude\_if\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in exclude\_if\_field → d.get(exclude\_if\_field).

**Derived worked case from the contract** An item with purchase order A and exclusion flag 1 is skipped when that exclusion field is configured.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0442.json#L506) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L632) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-3f4355705f3ea1"></a>
### Show accounting ledger preview

`operation_enterprise_controllers_stock_controller_business_behavior_show_accounting_ledger_preview`

**Inputs** company, doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** rollback.

**Explicit results** mapping(“gl\_columns” → gl\_columns, “gl\_data” → gl\_data).

**Local steps**

- Set filters from Platform.\_dict(company = company, include\_dimensions = 1).
- Set doc from Platform.get\_lazy\_doc(doctype, docname).
- Evaluate doc.check\_permission(“read”).
- Evaluate Platform.has\_permission(“GL Entry”, “read”, throw = true).
- Evaluate doc.run\_method(“before\_gl\_preview”).
- Set tuple(gl\_columns, gl\_data) from get\_accounting\_ledger\_preview(doc, filters).
- Evaluate Platform.db.rollback().
- Return mapping(“gl\_columns” → gl\_columns, “gl\_data” → gl\_data).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”), Platform.has\_permission(“GL Entry”, “read”, throw = true) · selected callable from doc.run\_method(“before\_gl\_preview”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L628)

<a id="op-ac74e45bcb0389"></a>
### Show stock ledger preview

`operation_enterprise_controllers_stock_controller_business_behavior_show_stock_ledger_preview`

**Inputs** company, doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** rollback.

**Explicit results** mapping(“sl\_columns” → sl\_columns, “sl\_data” → sl\_data).

**Local steps**

- Set filters from Platform.\_dict(company = company, valuation\_field\_type = “Currency”).
- Set doc from Platform.get\_lazy\_doc(doctype, docname).
- Evaluate doc.check\_permission(“read”).
- Evaluate Platform.has\_permission(“Stock Ledger Entry”, “read”, throw = true).
- Evaluate doc.run\_method(“before\_sl\_preview”).
- Set tuple(sl\_columns, sl\_data) from get\_stock\_ledger\_preview(doc, filters).
- Evaluate Platform.db.rollback().
- Return mapping(“sl\_columns” → sl\_columns, “sl\_data” → sl\_data).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”), Platform.has\_permission(“Stock Ledger Entry”, “read”, throw = true) · selected callable from doc.run\_method(“before\_sl\_preview”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L950) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L629)

<a id="op-7bd8d3b46cc07c"></a>
### Get accounting ledger preview

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_accounting_ledger_preview`

**Inputs** doc, filters.

**Explicit results** tuple(gl\_columns, gl\_data).

**Local steps**

- Bind dependencies get\_gl\_columns.
- Set tuple(gl\_columns, gl\_data) from tuple(list(), list()).
- Set fields from list(“posting\_date”, “account”, “debit”, “credit”, …).
- Set doc.docstatus from 1.
- If (doc.get(“update\_stock”) or doc.doctype belongs to tuple(“Purchase Receipt”, “Delivery Note”, “Stock Entry”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“update\_stock”) → doc.doctype belongs to tuple(“Purchase Receipt”, “Delivery Note”, “Stock Entry”).
  - Evaluate make\_serial\_and\_batch\_bundles\_for\_preview(doc).
  - Evaluate doc.update\_stock\_ledger().
- Evaluate doc.make\_gl\_entries().
- Set columns from get\_gl\_columns(filters).
- Set masked\_fields from Platform.get\_meta(“GL Entry”).get\_masked\_fields().
- Set gl\_entries from mask\_dict\_results(get\_gl\_entries\_for\_preview(doc.doctype, doc.name, fields), masked\_fields).
- Set gl\_columns from get\_columns(columns, fields, Enterprise.get\_company\_currency(filters.company), masked\_fields).
- Set gl\_data from get\_data(fields, gl\_entries).
- Return tuple(gl\_columns, gl\_data).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L355)

<a id="op-6e57e5dd4cfbf3"></a>
### Get stock ledger preview

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_stock_ledger_preview`

**Inputs** doc, filters.

**Explicit results** tuple(sl\_columns, sl\_data).

**Local steps**

- Bind dependencies get\_sl\_columns.
- Set tuple(sl\_columns, sl\_data) from tuple(list(), list()).
- Set fields from list(“item\_code”, “stock\_uom”, “actual\_qty”, “qty\_after\_transaction”, …).
- Set columns\_fields from list(“item\_code”, “stock\_uom”, “in\_qty”, “out\_qty”, …).
- If (doc.get(“update\_stock”) or doc.doctype belongs to tuple(“Purchase Receipt”, “Delivery Note”, “Stock Entry”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“update\_stock”) → doc.doctype belongs to tuple(“Purchase Receipt”, “Delivery Note”, “Stock Entry”).
  - Set doc.docstatus from 1.
  - Evaluate make\_serial\_and\_batch\_bundles\_for\_preview(doc).
  - Evaluate doc.update\_stock\_ledger().
  - Set columns from get\_sl\_columns(filters).
  - Set masked\_fields from Platform.get\_meta(“Stock Ledger Entry”).get\_masked\_fields().
  - Set sl\_entries from mask\_dict\_results(get\_sl\_entries\_for\_preview(doc.doctype, doc.name, fields), masked\_fields).
  - Set sl\_columns from get\_columns(columns, columns\_fields, Enterprise.get\_company\_currency(filters.company), masked\_fields).
  - Set sl\_data from get\_data(columns\_fields, sl\_entries).
- Return tuple(sl\_columns, sl\_data).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L361)

<a id="op-4fc20216857b96"></a>
### Make serial and batch bundles for preview

`operation_enterprise_binding_enterprise_controllers_stock_controller_make_serial_and_batch_bundles_for_preview`

**Inputs** doc.

**Local steps**

- For each table\_name in tuple(“items”, “packed\_items”).
  - If doc.get(table\_name).
    - Evaluate doc.make\_bundle\_for\_sales\_purchase\_return(table\_name).
    - Evaluate doc.make\_bundle\_using\_old\_serial\_batch\_fields(table\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L364)

<a id="op-cb7abc47ffb9bc"></a>
### Get sl entries for preview

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_sl_entries_for_preview`

**Inputs** doctype, docname, fields.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** sl\_entries.

**Local steps**

- Set sl\_entries from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → doctype, “voucher\_no” → docname), fields = fields).
- For each entry in sl\_entries.
  - If entry.actual\_qty &gt; 0.
    - Set entry at “in\_qty” from entry.actual\_qty.
    - Set entry at “out\_qty” from 0.
  - Otherwise.
    - Set entry at “out\_qty” from abs(entry.actual\_qty).
    - Set entry at “in\_qty” from 0.
  - If entry.actual\_qty &lt; 0.
    - Set entry at “in\_out\_rate” from (entry.stock\_value\_difference ÷ entry.actual\_qty).
- Return sl\_entries.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L360)

<a id="op-9c6b13cfd325d8"></a>
### Get gl entries for preview

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_gl_entries_for_preview`

**Inputs** doctype, docname, fields.

**Record and data access** read “GL Entry” via get\_all.

**Explicit results** Platform.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → doctype, “voucher\_no” → docname), fields = fields).

**Local steps**

- Return Platform.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → doctype, “voucher\_no” → docname), fields = fields).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L359)

<a id="op-ab1477b9de35f8"></a>
### Get columns

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_columns`

**Inputs** raw\_columns, fields, currency, masked\_fields.

**Explicit results** columns.

**Local steps**

- Set masked\_fieldnames from set of df.fieldname for df drawn from masked\_fields.
  - Draw df from masked\_fields.
- Set columns from list().
- For each source\_column in raw\_columns.
  - Set fieldname from source\_column.get(“fieldname”).
  - If (source\_column.get(“hidden”) or fieldname does not belong to fields).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_column.get(“hidden”) → fieldname does not belong to fields.
    - Continue with the next iteration or loop test.
  - Set column from mapping(“name” → source\_column.get(“label”), “editable” → false, “width” → 110, “fieldtype” → “Data” when fieldname belongs to masked\_fieldnames, otherwise source\_column.get(“fieldtype”)).
    - Value choice on fieldname belongs to masked\_fieldnames — true gives “Data”, false gives source\_column.get(“fieldtype”).
  - If column at “fieldtype” equals “Currency”.
    - Set column at “options” from currency.
  - Evaluate columns.append(column).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L356)

<a id="op-5242e6fe828552"></a>
### Get data

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_data`

**Inputs** raw\_columns, raw\_data.

**Explicit results** datatable\_data.

**Local steps**

- Set datatable\_data from list().
- For each row in raw\_data.
  - Set data\_row from list().
  - For each column in raw\_columns.
    - Evaluate data\_row.append((row.get(column) or empty text)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(column) → empty text.
  - Evaluate datatable\_data.append(data\_row).
- Return datatable\_data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L357)

<a id="op-984e6a8f0a3b58"></a>
### Repost required for queue

`operation_enterprise_controllers_stock_controller_business_behavior_repost_required_for_queue`

**Inputs** doc.

**Declared result** bool.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** false · true.

**Local steps**

- Set consuming\_sles from Platform.db.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → doc.doctype, “voucher\_no” → doc.name, “actual\_qty” → tuple(“&lt;”, 0), “is\_cancelled” → 0), fields = list(“item\_code”, “warehouse”, ….
- Set item\_warehouses from list of tuple(sle.item\_code, sle.warehouse) for sle drawn from consuming\_sles.
  - Draw sle from consuming\_sles.
- Set unique\_item\_warehouses from set(item\_warehouses).
- If len(unique\_item\_warehouses) equals len(item\_warehouses).
  - Return false.
- For each sle in consuming\_sles.
  - If sle.stock\_queue differs from “&#91;&#93;”.
    - Return true.
- Return false.

**Derived worked case from the contract** Two outgoing A/W entries with empty queues plus one outgoing B/W entry with a populated queue return true; three distinct pairs return false regardless of queue contents.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0443.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L948) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L627) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-446fe4a1c02cd0"></a>
### Check item quality inspection

`operation_enterprise_controllers_stock_controller_business_behavior_check_item_quality_inspection`

**Inputs** doctype, docstatus, items.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** items when doctype equals “Stock Entry”, otherwise list() · items · list of item for item drawn from items where item.get(“item\_code”) belongs to inspection\_required\_items.

**Local steps**

- If isinstance(items, str).
  - Set items from json.loads(items).
- Set inspection\_fieldname\_map from mapping(“Purchase Receipt” → “inspection\_required\_before\_purchase”, “Purchase Invoice” → “inspection\_required\_before\_purchase”, “Subcontracting Receipt” → “inspection\_required\_before\_purchase”, “Sales Invo ….
- Set inspection\_fieldname from inspection\_fieldname\_map.get(doctype).
- If inspection\_fieldname is identical to no value.
  - Return items when doctype equals “Stock Entry”, otherwise list().
    - Value choice on doctype equals “Stock Entry” — true gives items, false gives list().
- Set allow\_after\_transaction from (cint(docstatus) equals 1 and Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(docstatus) equals 1 → Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).
- If allow\_after\_transaction.
  - Return items.
- Set item\_codes from list(set of item.get(“item\_code”) for item drawn from items).
  - Draw item from items.
- Set Item from Platform.qb.DocType(“Item”).
- Set results from nested operand in the contract(nested operand in the contract).select(Item.name).where((nested operand in the contract.name.isin(item\_codes) bitwise and Item at inspection\_fieldname equals 1)).run(as\_dict = true).
- Set inspection\_required\_items from set of row.name for row drawn from results.
  - Draw row from results.
- Return list of item for item drawn from items where item.get(“item\_code”) belongs to inspection\_required\_items.
  - Draw item from items, keep a combination only if (item.get(“item\_code”) belongs to inspection\_required\_items).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L936) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L615)

<a id="op-6dc61f32a75492"></a>
### Make quality inspections

`operation_enterprise_controllers_stock_controller_business_behavior_make_quality_inspections`

**Inputs** company, doctype, docname, items, inspection\_type.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“company” → company, “doctype” → “Quality Inspection”, “inspection\_type” → inspection\_type, “inspected\_by” → Platform.session.user, …) via get\_doc.

**State and service calls** call save on quality\_inspection.

**Explicit results** inspections.

**Explicit failure paths** validation helper — translated “{item\_name}'s Sample Size ({sample\_size}) cannot be greater than the Accepted Quantity ({accepted\_quantity})”.format(item\_name = item.get(“item\_name”), sample\_size = item.get(“sample\_size”), ac ….

**Local steps**

- If isinstance(items, str).
  - Set items from json.loads(items).
- Set inspections from list().
- For each item in items.
  - If flt(item.get(“sample\_size”)) &gt; flt(item.get(“qty”)).
    - Call the validation error handler Platform.throw(translated “{item\_name}'s Sample Size ({sample\_size}) cannot be greater than the Accepted Quantity ({accepted\_quantity})”.format(item\_name = item.get(“item\_name”), sample\_size = item.get(“sa ….
  - Set quality\_inspection from Platform.get\_doc(mapping(“company” → company, “doctype” → “Quality Inspection”, “inspection\_type” → inspection\_type, “inspected\_by” → Platform.session.user, …)).
    - Value choice on item.get(“serial\_no”) — true gives item.get(“serial\_no”).split(whitespace '\\n') at 0, false gives no value.
  - Evaluate quality\_inspection.save().
  - Evaluate inspections.append(quality\_inspection.name).
- Return inspections.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L626)

<a id="op-646881565e1803"></a>
### Is reposting pending

`operation_enterprise_controllers_stock_controller_business_behavior_is_reposting_pending`

**Inputs** no declared parameters.

**Record and data access** read “Repost Item Valuation” via exists.

**Explicit results** Platform.db.exists(“Repost Item Valuation”, mapping(“docstatus” → 1, “status” → list(“in”, list(“Queued”, “In Progress”)))).

**Local steps**

- Return Platform.db.exists(“Repost Item Valuation”, mapping(“docstatus” → 1, “status” → list(“in”, list(“Queued”, “In Progress”)))).

**Derived worked case from the contract** A completed submitted repost and a draft queued repost alone leave this check falsey. A submitted queued repost makes it truthy.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0443.json#L238) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L945) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L624) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-6f866bf0df147a"></a>
### Invalidate future sle cache

`operation_enterprise_controllers_stock_controller_business_behavior_invalidate_future_stock_ledger_entry_cache`

**Inputs** voucher\_type, voucher\_no.

**Local steps**

- If hasattr(Platform.local, “future\_sle”).
  - Evaluate Platform.local.future\_sle.pop(tuple(voucher\_type, voucher\_no), no value).

If control reaches the end, it returns no value.

**Derived worked case from the contract** Evicting Delivery Note / A keeps Stock Entry / A cached. Repeating the eviction completes without error.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0443.json#L256) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L944) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L623) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-ea5151e6a2bc44"></a>
### Future sle exists

`operation_enterprise_controllers_stock_controller_business_behavior_future_stock_ledger_entry_exists`

**Inputs** args, sl\_entries = no value, for\_update = false.

**Explicit results** false · true · no value · len(data).

**Local steps**

- Bind dependencies get\_combine\_datetime.
- Set key from tuple(args.voucher\_type, args.voucher\_no).
- If not hasattr(Platform.local, “future\_sle”).
  - Set Platform.local.future\_sle from mapping().
- If not for\_update.
  - If validate\_future\_sle\_not\_exists(args, key, sl\_entries).
    - Return false.
  - Otherwise.
    - If get\_cached\_data(args, key).
      - Return true.
- If not sl\_entries.
  - Set sl\_entries from get\_sle\_entries\_against\_voucher(args).
  - If not sl\_entries.
    - Return no value.
- Set or\_conditions from get\_conditions\_to\_validate\_future\_sle(sl\_entries).
- Set args at “posting\_datetime” from get\_combine\_datetime(args at “posting\_date”, args at “posting\_time”).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.item\_code, sle.warehouse, nested operand in the contract.as\_(“total\_row”)).where((((nested operand in the contract(nested operand i ….
- If (for\_update and Platform.db.db\_type equals “mariadb”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_update → Platform.db.db\_type equals “mariadb”.
  - Set query from query.for\_update().
- Set data from query.run(as\_dict = 1).
- If not for\_update.
  - For each d in data.
    - Set Platform.local.future\_sle at key at tuple(d.item\_code, d.warehouse) from d.total\_row.
- Return len(data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L939) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L618)

<a id="op-ea07d6d6b71390"></a>
### Validate future sle not exists

`operation_enterprise_controllers_stock_controller_business_behavior_validate_future_stock_ledger_entry_not_exists`

**Inputs** args, key, sl\_entries = no value.

**Explicit results** false · true.

**Local steps**

- Set item\_key from empty text.
- If args.get(“item\_code”).
  - Set item\_key from tuple(args.get(“item\_code”), args.get(“warehouse”)).
- If (not sl\_entries and hasattr(Platform.local, “future\_sle”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sl\_entries → hasattr(Platform.local, “future\_sle”).
  - If key does not belong to Platform.local.future\_sle.
    - Return false.
  - If (not Platform.local.future\_sle.get(key) or (item\_key and item\_key does not belong to nested operand in the contract.local.future\_sle.get(key))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.local.future\_sle.get(key) → (item\_key and item\_key does not belong to Platform.local.future\_sle.get(key)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_key → item\_key does not belong to Platform.local.future\_sle.get(key).
    - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L775) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L989) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L666)

<a id="op-9cd51ba12ff564"></a>
### Get cached data

`operation_enterprise_controllers_stock_controller_business_behavior_get_cached_data`

**Inputs** args, key.

**Explicit results** true when (count or count equals 0), otherwise false · Platform.local.future\_sle at key.

**Local steps**

- If key does not belong to Platform.local.future\_sle.
  - Set Platform.local.future\_sle at key from Platform.\_dict(mapping()).
- If args.get(“item\_code”).
  - Set item\_key from tuple(args.get(“item\_code”), args.get(“warehouse”)).
  - Set count from Platform.local.future\_sle at key.get(item\_key).
  - Return true when (count or count equals 0), otherwise false.
    - Value choice on (count or count equals 0) — true gives true, false gives false.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in count → count equals 0.
- Otherwise.
  - Return Platform.local.future\_sle at key.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L1110) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L619)

<a id="op-faea00cde9635b"></a>
### Get sle entries against voucher

`operation_enterprise_controllers_stock_controller_business_behavior_get_stock_ledger_entry_entries_against_voucher`

**Inputs** args.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → args.voucher\_type, “voucher\_no” → args.voucher\_no), fields = list(“item\_code”, “warehouse”), order\_by = “creation asc”).

**Local steps**

- Return Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → args.voucher\_type, “voucher\_no” → args.voucher\_no), fields = list(“item\_code”, “warehouse”), order\_by = “creation asc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L1422) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L943) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L622)

<a id="op-99640a7c8de1e1"></a>
### Get conditions to validate future sle

`operation_enterprise_controllers_stock_controller_business_behavior_get_conditions_to_validate_future_stock_ledger_entry`

**Inputs** sl\_entries.

**Explicit results** or\_conditions.

**Local steps**

- Set warehouse\_items\_map from mapping().
- For each entry in sl\_entries.
  - If entry.warehouse does not belong to warehouse\_items\_map.
    - Set warehouse\_items\_map at entry.warehouse from set().
  - Evaluate warehouse\_items\_map at entry.warehouse.add(entry.item\_code).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set or\_conditions from list().
- For each tuple(warehouse, items) in warehouse\_items\_map.items().
  - Evaluate or\_conditions.append((sle.warehouse equals warehouse bitwise and sle.item\_code.isin(list(items)))).
- Return or\_conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L1571) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L620)

<a id="op-8325cf47bde424"></a>
### Create repost item valuation entry

`operation_enterprise_controllers_stock_controller_business_behavior_create_repost_item_valuation_entry`

**Inputs** args.

**State and service calls** request new\_doc for “Repost Item Valuation” · call save on repost\_entry · call submit on repost\_entry.

**Local steps**

- Set args from Platform.\_dict(args).
- Set repost\_entry from Platform.new\_doc(“Repost Item Valuation”).
- Set repost\_entry.based\_on from args.based\_on.
- If not args.based\_on.
  - Set repost\_entry.based\_on from “Transaction” when args.voucher\_no, otherwise “Item and Warehouse”.
    - Value choice on args.voucher\_no — true gives “Transaction”, false gives “Item and Warehouse”.
- Set repost\_entry.voucher\_type from args.voucher\_type.
- Set repost\_entry.voucher\_no from args.voucher\_no.
- Set repost\_entry.item\_code from args.item\_code.
- Set repost\_entry.warehouse from args.warehouse.
- Set repost\_entry.posting\_date from args.posting\_date.
- Set repost\_entry.posting\_time from args.posting\_time.
- Set repost\_entry.company from args.company.
- Set repost\_entry.allow\_zero\_rate from args.allow\_zero\_rate.
- Set repost\_entry.flags.ignore\_links from true.
- Set repost\_entry.flags.ignore\_permissions from true.
- Set repost\_entry.via\_landed\_cost\_voucher from args.via\_landed\_cost\_voucher.
- Evaluate repost\_entry.save().
- Evaluate repost\_entry.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L1897) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L938) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L617)
