# Inventory and warehouses · operations 46

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase receipt

[Record definition](../../../../data/record-types/purchase_receipt.json)

<a id="op-54dd06ba4d3bd3"></a>
### Make purchase invoice.select item

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_purchase_invoice_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1003) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L500)

<a id="op-137b0d250794d9"></a>
### Get invoiced qty map

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_invoiced_qty_map`

**Inputs** purchase\_receipt.

**Record and data access** execute query text (SELECT, Purchase Invoice Item).

**Explicit results** invoiced\_qty\_map.

**Local steps**

- Set invoiced\_qty\_map from mapping().
- For each tuple(pr\_detail, qty) in Platform.db.sql(query text (SELECT, Purchase Invoice Item), purchase\_receipt).
  - If not invoiced\_qty\_map.get(pr\_detail).
    - Set invoiced\_qty\_map at pr\_detail from 0.
  - Update invoiced\_qty\_map at pr\_detail using + qty.
- Return invoiced\_qty\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L980) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L477)

<a id="op-9b1756e694230e"></a>
### Get returned qty map

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_returned_qty_map`

**Inputs** purchase\_receipt.

**Explicit results** Platform.\_dict(query) when query, otherwise Platform.\_dict().

**Local steps**

- Set pr from Platform.qb.DocType(“Purchase Receipt”).
- Set pr\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- Return Platform.\_dict(query) when query, otherwise Platform.\_dict().
  - Value choice on query — true gives Platform.\_dict(query), false gives Platform.\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L993) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L490)

<a id="op-963b054d446fd4"></a>
### Make purchase return against rejected warehouse

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_purchase_return_against_rejected_warehouse`

**Inputs** source\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“Purchase Receipt”, source\_name, return\_against\_rejected\_qty = true).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“Purchase Receipt”, source\_name, return\_against\_rejected\_qty = true).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1007) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L504)

<a id="op-455ba49eb8df57"></a>
### Make purchase return

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_purchase_return`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“Purchase Receipt”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“Purchase Receipt”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1006) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L503)

<a id="op-f4fda6b9abd9bc"></a>
### Update purchase receipt status

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_update_purchase_receipt_status`

**Inputs** docname, status.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — translated “Only a submitted Purchase Receipt can be closed or reopened”.

**Local steps**

- Set pr from Platform.get\_lazy\_doc(“Purchase Receipt”, docname, check\_permission = “submit”).
- <a id="op-f4fda6b9abd9bc-guard-3"></a>If pr.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Purchase Receipt can be closed or reopened”).
- Evaluate pr.update\_status(status).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison pr.docstatus differs from 1, pr.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Purchase Receipt can be closed or reopened”. With pr.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f4fda6b9abd9bc-guard-3)

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L213)

<a id="op-61d41dd1a3a878"></a>
### Make stock entry

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_stock_entry`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Purchase Receipt”, source\_name, mapping(“Purchase Receipt” → mapping(“doctype” → “Stock Entry”), “Purchase Receipt Item” → mapping(“doctype” → “Stock Entry Detail”, “field\_map” → mapping(“w ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1008) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L505)

<a id="op-93a7e54ab11934"></a>
### Make stock entry.set missing values

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_stock_entry_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.stock\_entry\_type from “Material Transfer”.
- Set target.purpose from “Material Transfer”.
- Evaluate target.set\_missing\_values().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L506)

<a id="op-b884645f22a1e1"></a>
### Make stock entry.update item

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_stock_entry_update_item`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- If source\_doc.serial\_and\_batch\_bundle.
  - Set serial\_nos from get\_serial\_nos\_from\_bundle(source\_doc.serial\_and\_batch\_bundle).
  - If serial\_nos.
    - Set serial\_nos from whitespace '\\n'.join(serial\_nos).
  - Set batches from get\_batches\_from\_bundle(source\_doc.serial\_and\_batch\_bundle).
  - If batches.
    - If len(batches) equals 1.
      - Set target\_doc.use\_serial\_batch\_fields from 1.
      - Set target\_doc.batch\_no from next(iter(batches)).
    - Otherwise.
      - If not serial\_nos.
        - Set cls\_obj from SerialBatchCreation(mapping(“type\_of\_transaction” → “Outward”, “serial\_and\_batch\_bundle” → source\_doc.serial\_and\_batch\_bundle, “item\_code” → source\_doc.item\_code, “warehouse” → source\_doc.warehouse)).
        - Evaluate cls\_obj.duplicate\_package().
        - Set target\_doc.serial\_and\_batch\_bundle from cls\_obj.serial\_and\_batch\_bundle.
  - If serial\_nos.
    - Set target\_doc.use\_serial\_batch\_fields from 1.
    - Set target\_doc.serial\_no from serial\_nos.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L507)

<a id="op-ea5f96c6e237d4"></a>
### Make inter company delivery note

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_inter_company_delivery_note`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_inter\_company\_transaction(“Purchase Receipt”, source\_name, target\_doc).

**Local steps**

- Return make\_inter\_company\_transaction(“Purchase Receipt”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1000) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L497)

<a id="op-0d067741415dcf"></a>
### Update regional gl entries

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_update_regional_general_ledger_entries`

**Inputs** gl\_list, doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** no value.

**Local steps**

- Return no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0775.json#L2739) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L214)

<a id="op-ff68cb7387b722"></a>
### Make lcv

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_make_landed_cost_voucher`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_value.

**State and service calls** request new\_doc for “Landed Cost Voucher”.

**Explicit results** landed\_cost\_voucher.as\_dict().

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid document type”.

**Local steps**

- If doctype does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”).
  - Call the validation error handler Platform.throw(translated “Invalid document type”, Platform.PermissionError).
- Evaluate Platform.has\_permission(doctype, doc = docname, throw = true).
- Set landed\_cost\_voucher from Platform.new\_doc(“Landed Cost Voucher”).
- Set details from Platform.db.get\_value(doctype, docname, list(“supplier”, “company”, “base\_grand\_total”), as\_dict = 1).
- Set landed\_cost\_voucher.company from details.company.
- Evaluate landed\_cost\_voucher.append(“purchase\_receipts”, mapping(“receipt\_document\_type” → doctype, “receipt\_document” → docname, “grand\_total” → details.base\_grand\_total, “supplier” → details.supplier)).
- Evaluate landed\_cost\_voucher.get\_items\_from\_purchase\_receipts().
- Return landed\_cost\_voucher.as\_dict().

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L190)

<a id="op-c0a5d4e3183c3a"></a>
### Post provisional gl entry

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_post_provisional_gl_entry`

**Inputs** doc, item, gl\_entries, posting\_date, provisional\_account, reverse = 0, item\_amount = no value, pr\_detail = no value.

**Record and data access** read “Purchase Receipt Item” via get\_value.

**Local steps**

- Set credit\_currency from get\_account\_currency(provisional\_account).
- Set expense\_account from item.expense\_account.
- Set debit\_currency from get\_account\_currency(item.expense\_account).
- Set remarks from (doc.get(“remarks”) or translated “Accounting Entry for Service”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“remarks”) → translated “Accounting Entry for Service”.
- Set multiplication\_factor from 1.
- Set amount from item.base\_amount.
- If reverse.
  - Set multiplication\_factor from negative 1.
  - Set amount from item\_amount.
  - Set expense\_account from Platform.db.get\_value(“Purchase Receipt Item”, mapping(“name” → (pr\_detail or item.get(“pr\_detail”))), list(“expense\_account”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pr\_detail → item.get(“pr\_detail”).
- Evaluate doc.add\_gl\_entry(gl\_entries = gl\_entries, account = provisional\_account, cost\_center = item.cost\_center, debit = 0.0, …).
- Evaluate doc.add\_gl\_entry(gl\_entries = gl\_entries, account = expense\_account, cost\_center = item.cost\_center, debit = (multiplication\_factor × amount), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L508)

<a id="op-87e106aaa4cdc3"></a>
### Get order billing provisional reversals

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_order_billing_provisional_reversals`

**Inputs** invoice.

**Declared result** dict.

**Explicit results** mapping() · reversals.

**Local steps**

- Set items from list of d for d drawn from invoice.items where (d.po\_detail and not d.pr\_detail).
  - Draw d from invoice.items, keep a combination only if ((d.po\_detail and not d.pr\_detail)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.po\_detail → not d.pr\_detail.
- If not items.
  - Return mapping().
- Set receipt\_rows from get\_provisional\_receipt\_rows(invoice.company, set of d.po\_detail for d drawn from items).
  - Draw d from items.
- If not receipt\_rows.
  - Return mapping().
- Set unreversed\_qty from get\_unreversed\_receipt\_qty(receipt\_rows, invoice).
- Set posted from get\_posted\_provision(receipt\_rows, invoice).
- Set factors from get\_posted\_to\_replayed\_factors(receipt\_rows, unreversed\_qty, posted).
- Set reversals from mapping().
- For each item in items.
  - Set rows from receipt\_rows.get(item.po\_detail).
  - If not rows.
    - Continue with the next iteration or loop test.
  - If flt(item.qty) &lt; 0.
    - Set allocations from release\_receipt\_rows(rows, unreversed\_qty, negative flt(item.qty)).
    - Set factor from get\_restore\_factor(item, allocations, posted, factors at item.po\_detail).
  - Otherwise.
    - Set allocations from allocate\_receipt\_rows(rows, unreversed\_qty, flt(item.qty)).
    - Set factor from factors at item.po\_detail.open.
  - Set reversals at item.name from list of tuple(row, (qty × factor)) for tuple(row, qty) drawn from allocations where flt((qty × factor), 9).
    - Draw tuple(row, qty) from allocations, keep a combination only if (flt((qty × factor), 9)).
- Return reversals.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L479)

<a id="op-a9ec9743e20ddd"></a>
### Get posted to replayed factors

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_posted_to_replayed_factors`

**Inputs** receipt\_rows, unreversed\_qty, posted.

**Declared result** dict.

**Explicit results** factors.

**Local steps**

- Set factors from mapping().
- For each tuple(po\_detail, rows) in receipt\_rows.items().
  - Set replayed\_open from sum(generator of (max(unreversed\_qty at row.name, 0) × get\_unit\_amount(row)) for row drawn from rows).
    - Draw row from rows.
  - Set replayed\_reversal from sum(generator of ((flt(row.kept\_qty) − unreversed\_qty at row.name) × get\_unit\_amount(row)) for row drawn from rows).
    - Draw row from rows.
  - Set reversed\_amount from flt(posted.reversed.get(po\_detail)).
  - Set factors at po\_detail from Platform.\_dict(open = get\_ratio((flt(nested operand in the contract.booked.get(po\_detail)) − reversed\_amount), replayed\_open), reversed = get\_ratio(reversed\_amount, replayed\_reversal)).
- Return factors.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L986) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L483)

<a id="op-c4c06d94707ee5"></a>
### Get restore factor

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_restore_factor`

**Inputs** item, allocations, posted, factors.

**Declared result** float.

**Explicit results** factors.reversed · get\_ratio((original.reversed × returned\_share), negative get\_reversal\_amount(allocations)).

**Local steps**

- Set original from posted.invoice\_rows.get(item.purchase\_invoice\_item).
- If (not original or not flt(original.qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not original → not flt(original.qty).
  - Return factors.reversed.
- Set returned\_share from min(1, (negative flt(item.qty) ÷ flt(original.qty))).
- Return get\_ratio((original.reversed × returned\_share), negative get\_reversal\_amount(allocations)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L992) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L489)

<a id="op-f5d4d0c2187d8c"></a>
### Get ratio

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_ratio`

**Inputs** posted\_amount, replayed\_amount.

**Declared result** float.

**Explicit results** 0.0 · flt((posted\_amount ÷ replayed\_amount), 9).

**Local steps**

- If (flt(posted\_amount, 9) ≤ 0 or flt(replayed\_amount, 9) ≤ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(posted\_amount, 9) ≤ 0 → flt(replayed\_amount, 9) ≤ 0.
  - Return 0.0.
- Return flt((posted\_amount ÷ replayed\_amount), 9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L990) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L487)

<a id="op-45f71e455cf10e"></a>
### Get unit amount

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_unit_amount`

**Inputs** row.

**Declared result** float.

**Explicit results** (flt(row.rate) × flt(row.conversion\_rate)).

**Local steps**

- Return (flt(row.rate) × flt(row.conversion\_rate)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L997) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L494)

<a id="op-53ecce6e65d3a6"></a>
### Get reversal amount

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_reversal_amount`

**Inputs** allocations.

**Declared result** float.

**Explicit results** sum(generator of (flt(qty) × get\_unit\_amount(row)) for tuple(row, qty) drawn from allocations).

**Local steps**

- Return sum(generator of (flt(qty) × get\_unit\_amount(row)) for tuple(row, qty) drawn from allocations).
  - Draw tuple(row, qty) from allocations.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L493)

<a id="op-adb02d90ce5bf0"></a>
### Get posted provision

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_posted_provision`

**Inputs** receipt\_rows, invoice.

**Declared result** Platform.\_dict.

**Explicit results** posted.

**Local steps**

- Set booking\_rows from mapping of row.name → po\_detail for tuple(po\_detail, rows) drawn from receipt\_rows.items(), then row drawn from rows.
  - Draw tuple(po\_detail, rows) from receipt\_rows.items().
  - Draw row from rows.
- Evaluate booking\_rows.update(get\_receipt\_return\_rows(booking\_rows)).
- Set other\_rows from get\_other\_invoice\_rows(booking\_rows, invoice).
- Evaluate booking\_rows.update(mapping of name → row.po\_detail for tuple(name, row) drawn from other\_rows.items() where row.pr\_detail).
  - Draw tuple(name, row) from other\_rows.items(), keep a combination only if (row.pr\_detail).
- Set invoice\_rows from mapping of name → row for tuple(name, row) drawn from other\_rows.items() where not row.pr\_detail.
  - Draw tuple(name, row) from other\_rows.items(), keep a combination only if (not row.pr\_detail).
- Set accounts from set of row.provisional\_expense\_account for rows drawn from receipt\_rows.values(), then row drawn from rows.
  - Draw rows from receipt\_rows.values().
  - Draw row from rows.
- Set balances from get\_provisional\_balances(list(expanded booking\_rows, expanded invoice\_rows), accounts, invoice).
- Set posted from Platform.\_dict(booked = mapping(), reversed = mapping(), invoice\_rows = invoice\_rows).
- For each tuple(name, po\_detail) in booking\_rows.items().
  - Set posted.booked at po\_detail from (flt(posted.booked.get(po\_detail)) + flt(balances.get(name))).
- For each tuple(po\_detail, amount) in get\_own\_receipt\_row\_reversals(invoice, receipt\_rows).items().
  - Set posted.booked at po\_detail from (flt(posted.booked.get(po\_detail)) − amount).
- For each tuple(name, row) in invoice\_rows.items().
  - Set row.reversed from negative flt(balances.get(name)).
  - Set posted.reversed at row.po\_detail from (flt(posted.reversed.get(row.po\_detail)) + row.reversed).
- Return posted.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L482)

<a id="op-5d330e96eb5f94"></a>
### Get own receipt row reversals

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_own_receipt_row_reversals`

**Inputs** invoice, receipt\_rows.

**Declared result** dict.

**Explicit results** mapping() · reversals.

**Local steps**

- If cint(invoice.docstatus) differs from 1.
  - Return mapping().
- Set rows from mapping of row.name → tuple(po\_detail, row) for tuple(po\_detail, po\_rows) drawn from receipt\_rows.items(), then row drawn from po\_rows.
  - Draw tuple(po\_detail, po\_rows) from receipt\_rows.items().
  - Draw row from po\_rows.
- Set reversals from mapping().
- For each item in invoice.items.
  - If item.pr\_detail does not belong to rows.
    - Continue with the next iteration or loop test.
  - Set tuple(po\_detail, row) from rows at item.pr\_detail.
  - Set amount from (min(flt(item.qty), flt(row.qty)) × get\_unit\_amount(row)).
  - Set reversals at po\_detail from (flt(reversals.get(po\_detail)) + amount).
- Return reversals.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L984) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L481)

<a id="op-a6456047a0b3b7"></a>
### Get receipt return rows

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_receipt_return_rows`

**Inputs** booking\_rows.

**Declared result** dict.

**Record and data access** read “Purchase Receipt Item” via get\_all.

**Explicit results** mapping of row.name → booking\_rows at row.purchase\_receipt\_item for row drawn from return\_rows.

**Local steps**

- Set return\_rows from Platform.get\_all(“Purchase Receipt Item”, filters = mapping(“purchase\_receipt\_item” → tuple(“in”, list(booking\_rows)), “docstatus” → 1), fields = list(“name”, “purchase\_receipt\_item”)).
- Return mapping of row.name → booking\_rows at row.purchase\_receipt\_item for row drawn from return\_rows.
  - Draw row from return\_rows.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L991) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L488)

<a id="op-9118c694d5799d"></a>
### Get other invoice rows

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_other_invoice_rows`

**Inputs** booking\_rows, invoice.

**Declared result** dict.

**Explicit results** mapping of row.name → row for row drawn from rows.

**Local steps**

- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set rows from nested operand in the contract(nested operand in the contract).select(pi\_item.name, pi\_item.qty, pi\_item.pr\_detail, pi\_item.po\_detail).where(((nested operand in the contract.docstatus equals 1 bitwise and  ….
- For each row in rows.
  - Set row.po\_detail from (booking\_rows.get(row.pr\_detail) or row.po\_detail).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in booking\_rows.get(row.pr\_detail) → row.po\_detail.
- Return mapping of row.name → row for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L480)

<a id="op-a794b8299d7926"></a>
### Get provisional balances

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_provisional_balances`

**Inputs** names, accounts, invoice.

**Declared result** dict.

**Explicit results** Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(gle.voucher\_detail\_no).run()).

**Local steps**

- Set gle from Platform.qb.DocType(“GL Entry”).
- Return Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(gle.voucher\_detail\_no).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L987) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L484)
