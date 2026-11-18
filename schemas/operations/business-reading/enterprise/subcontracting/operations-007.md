# Subcontracting · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subcontracting receipt

[Record definition](../../../../data/record-types/subcontracting_receipt.json)

<a id="op-43dd9061671415"></a>
### Subcontracting Receipt.get rm wise required qty

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_get_rm_wise_required_qty`

**Inputs** self, precision.

**Declared result** dict.

**Record and data access** read “BOM” via get\_value.

**Explicit results** rm\_dict.

**Local steps**

- Set rm\_dict from mapping().
- For each row in self.items.
  - If Platform.db.get\_value(“BOM”, row.bom, “allow\_alternative\_item”).
    - Continue with the next iteration or loop test.
  - For each bom\_item in self.\_get\_materials\_from\_bom(row.item\_code, row.bom, row.get(“include\_exploded\_items”)).
    - Set required from rm\_dict.setdefault(bom\_item.rm\_item\_code, Platform.\_dict(qty = 0.0, stock\_uom = bom\_item.stock\_uom)).
    - Update required.qty using + flt(((bom\_item.qty\_consumed\_per\_unit × self.get\_qty\_for\_costing(row)) × row.conversion\_factor), precision).
- Return rm\_dict.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1215)

<a id="op-74fe63ebf38677"></a>
### Subcontracting Receipt.get rm wise consumed qty

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_get_raw_material_wise_consumed_quantity`

**Inputs** self.

**Explicit results** rm\_dict.

**Local steps**

- Set rm\_dict from defaultdict(float).
- For each row in self.supplied\_items.
  - Update rm\_dict at row.rm\_item\_code using + row.consumed\_qty.
- Return rm\_dict.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L3714) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1032)

<a id="op-09996a35284aef"></a>
### Subcontracting Receipt.update status updater args

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_update_status_updater_arguments`

**Inputs** self.

**Local steps**

- If cint(self.is\_return).
  - Evaluate self.status\_updater.extend(list(mapping(“source\_dt” → “Subcontracting Receipt Item”, “target\_dt” → “Subcontracting Order Item”, “join\_field” → “subcontracting\_order\_item”, “target\_field” → “returned\_qty”,  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L3825) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1057)

<a id="op-3dafd9dce08074"></a>
### Subcontracting Receipt.update status

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_update_status`

**Inputs** self, status = no value, update\_modified = false.

**Record and data access** resolve a document from “Subcontracting Receipt” via get\_doc.

**State and service calls** request set\_value on “Subcontracting Receipt”.

**Local steps**

- If not status.
  - If self.docstatus equals 0.
    - Set status from “Draft”.
  - Otherwise.
    - If self.docstatus equals 1.
      - Set status from “Completed”.
      - If self.is\_return.
        - Set status from “Return”.
      - Otherwise.
        - If self.per\_returned equals 100.
          - Set status from “Return Issued”.
    - Otherwise.
      - If self.docstatus equals 2.
        - Set status from “Cancelled”.
  - If self.is\_return.
    - Evaluate Platform.get\_doc(“Subcontracting Receipt”, self.return\_against).update\_status(update\_modified = update\_modified).
- If status.
  - Evaluate Platform.db.set\_value(“Subcontracting Receipt”, self.name, “status”, status, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L4219) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1056)

<a id="op-8665d0cb3a87f3"></a>
### Subcontracting Receipt.get gl entries

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map = no value.

**Explicit results** list() · process\_gl\_map(gl\_entries, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Local steps**

- Bind dependencies process\_gl\_map.
- If not Enterprise.is\_perpetual\_inventory\_enabled(self.company).
  - Return list().
- Set gl\_entries from list().
- Evaluate self.make\_item\_gl\_entries(gl\_entries, inventory\_account\_map).
- Evaluate self.make\_item\_gl\_entries\_for\_lcv(gl\_entries, inventory\_account\_map).
- Return process\_gl\_map(gl\_entries, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Methods declared on this owner** [make item gl entries](operations-007.md#op-ec7c3e6db978cb), [make item gl entries for lcv](operations-007.md#op-25489d4bde1961).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1029)

<a id="op-ec7c3e6db978cb"></a>
### Subcontracting Receipt.make item gl entries

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_make_item_gl_entries`

**Inputs** self, gl\_entries, inventory\_account\_map = no value.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**State and service calls** msgprint with ((translated “No accounting entries for the following warehouses” + “: \\n”) + whitespace '\\n'.join(warehouse\_with\_no\_account)).

**Local steps**

- Set warehouse\_with\_no\_account from list().
- Set remarks from (self.get(“remarks”) or translated “Accounting Entry for Stock”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
- Set supplied\_items\_details from Platform.\_dict().
- For each item in self.supplied\_items.
  - Evaluate supplied\_items\_details.setdefault(item.reference\_name, list()).append(Platform.\_dict(mapping(“item\_code” → item.rm\_item\_code, “amount” → item.amount, “expense\_account” → item.expense\_account, “cost\_center” ….
- For each item in self.items.
  - If (flt(item.rate) and flt(item.qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(item.rate) → flt(item.qty).
    - Set \_inv\_dict from self.get\_inventory\_account\_dict(item, inventory\_account\_map).
    - If \_inv\_dict.get(“account”).
      - Set stock\_value\_diff from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_type” → “Subcontracting Receipt”, “voucher\_no” → self.name, “voucher\_detail\_no” → item.name, “warehouse” → item.warehouse, …), “stock\_value\_difference”).
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = \_inv\_dict at “account”, cost\_center = item.cost\_center, debit = stock\_value\_diff, …).
      - Set service\_cost from flt((flt(item.service\_cost\_per\_qty) × flt(item.qty)), item.precision(“amount”)).
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = item.expense\_account, cost\_center = item.cost\_center, debit = 0.0, …).
      - Set service\_account from (item.service\_expense\_account or item.expense\_account).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.service\_expense\_account → item.expense\_account.
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = service\_account, cost\_center = item.cost\_center, debit = 0.0, …).
      - If divisional\_loss bound to flt((item.amount − stock\_value\_diff), item.precision(“amount”)).
        - Set loss\_account from self.get\_company\_default(“stock\_adjustment\_account”, ignore\_validation = true).
        - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = loss\_account, cost\_center = item.cost\_center, debit = 0.0, …).
        - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = item.expense\_account, cost\_center = item.cost\_center, debit = divisional\_loss, …).
    - Otherwise.
      - If (item.warehouse does not belong to warehouse\_with\_no\_account or item.rejected\_warehouse does not belong to warehouse\_with\_no\_account).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.warehouse does not belong to warehouse\_with\_no\_account → item.rejected\_warehouse does not belong to warehouse\_with\_no\_account.
        - Evaluate warehouse\_with\_no\_account.append(item.warehouse).
  - Evaluate self.\_make\_supplied\_items\_gl\_entries(gl\_entries, item, supplied\_items\_details.get(item.name, list()), inventory\_account\_map, …).
  - If item.additional\_cost\_per\_qty.
    - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = item.expense\_account, cost\_center = (self.cost\_center or self.get\_company\_default(“cost\_center”)), debit = (flt(item.received\_qty) × item.additional\_cos ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → self.get\_company\_default(“cost\_center”).
- For each row in self.additional\_costs.
  - Set credit\_amount from flt(row.base\_amount) when (row.base\_amount or row.account\_currency differs from self.company\_currency), otherwise flt(row.amount).
    - Value choice on (row.base\_amount or row.account\_currency differs from self.company\_currency) — true gives flt(row.base\_amount), false gives flt(row.amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.base\_amount → row.account\_currency differs from self.company\_currency.
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = row.expense\_account, cost\_center = (self.cost\_center or self.get\_company\_default(“cost\_center”)), debit = 0.0, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → self.get\_company\_default(“cost\_center”).
- If warehouse\_with\_no\_account.
  - Evaluate Platform.msgprint(((translated “No accounting entries for the following warehouses” + “: \\n”) + whitespace '\\n'.join(warehouse\_with\_no\_account))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make supplied items gl entries](operations-007.md#op-fceba247a2b8ac).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1218)

<a id="op-fceba247a2b8ac"></a>
### Subcontracting Receipt.make supplied items gl entries

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_make_supplied_items_gl_entries`

**Inputs** self, gl\_entries, item, supplied\_items, inventory\_account\_map, remarks.

**Declared result** no value.

**Local steps**

- For each rm\_item in supplied\_items.
  - If not flt(rm\_item.amount).
    - Continue with the next iteration or loop test.
  - Set \_inv\_dict from self.get\_inventory\_account\_dict(rm\_item, inventory\_account\_map, “supplier\_warehouse”).
  - Set expense\_account from (rm\_item.expense\_account or item.expense\_account).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in rm\_item.expense\_account → item.expense\_account.
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = \_inv\_dict.get(“account”), cost\_center = (rm\_item.cost\_center or item.cost\_center), debit = 0.0, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in rm\_item.cost\_center → item.cost\_center.
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = expense\_account, cost\_center = (rm\_item.cost\_center or item.cost\_center), debit = flt(rm\_item.amount), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in rm\_item.cost\_center → item.cost\_center.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1220)

<a id="op-25489d4bde1961"></a>
### Subcontracting Receipt.make item gl entries for lcv

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_make_item_gl_entries_for_lcv`

**Inputs** self, gl\_entries, inventory\_account\_map.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_custom\_dimension\_overrides.
- Set landed\_cost\_entries from self.get\_item\_account\_wise\_lcv\_entries().
- If not landed\_cost\_entries.
  - Return no value.
- For each item in self.items.
  - Set item\_entries from landed\_cost\_entries.get(tuple(item.item\_code, item.name), list()).
  - If (item.landed\_cost\_voucher\_amount and item\_entries).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.landed\_cost\_voucher\_amount → item\_entries.
    - Set remarks from translated “Accounting Entry for Landed Cost Voucher for SCR {0}”.format(self.name).
    - Set \_inv\_dict from self.get\_inventory\_account\_dict(item, inventory\_account\_map).
    - For each entry in item\_entries.
      - If not (entry.amount or entry.base\_amount).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.amount → entry.base\_amount.
        - Continue with the next iteration or loop test.
      - Set account\_currency from get\_account\_currency(entry.expense\_account).
      - Set credit\_amount from flt(entry.base\_amount) when (entry.base\_amount or account\_currency differs from self.company\_currency), otherwise flt(entry.amount).
        - Value choice on (entry.base\_amount or account\_currency differs from self.company\_currency) — true gives flt(entry.base\_amount), false gives flt(entry.amount).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.base\_amount → account\_currency differs from self.company\_currency.
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = entry.expense\_account, cost\_center = (entry.dimensions.cost\_center or item.cost\_center), debit = 0.0, …).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.cost\_center → item.cost\_center.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.project → item.project.
      - Set account\_currency from get\_account\_currency(item.expense\_account).
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = item.expense\_account, cost\_center = item.cost\_center, debit = 0.0, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1219)

<a id="op-4c25a788a31724"></a>
### Subcontracting Receipt.auto create purchase receipt

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_auto_create_purchase_receipt`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- If Platform.db.get\_single\_value(“Buying Settings”, “auto\_create\_purchase\_receipt”).
  - Evaluate make\_purchase\_receipt(self, save = true, notify = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “auto\_create\_purchase\_receipt”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L4705) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1025)

<a id="op-9d662a22d621b9"></a>
### Subcontracting Receipt.has reserved stock

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_has_reserved_stock`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- Bind dependencies get\_sre\_details\_for\_voucher.
- For each item in self.supplied\_items.
  - If get\_sre\_details\_for\_voucher(“Subcontracting Order”, item.subcontracting\_order).
    - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L4823) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1036)

<a id="op-ed05b8d49d24d3"></a>
### Make subcontract return against rejected warehouse

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_make_subcontract_return_against_rejected_warehouse`

**Inputs** source\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“Subcontracting Receipt”, source\_name, return\_against\_rejected\_qty = true).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“Subcontracting Receipt”, source\_name, return\_against\_rejected\_qty = true).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1209)

<a id="op-cbd5c548a6b2f9"></a>
### Make subcontract return

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_make_subcontract_return`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“Subcontracting Receipt”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“Subcontracting Receipt”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1208)

<a id="op-1d839f488292bd"></a>
### Make purchase receipt

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_make_purchase_receipt`

**Inputs** source\_name, target\_doc = no value, save = false, submit = false, notify = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Subcontracting Receipt” via get\_doc.

**State and service calls** call save on target\_doc · call submit on target\_doc · msgprint with translated “Purchase Receipt {0} created.”.format(get\_link\_to\_form(target\_doc.doctype, target\_doc.name)).

**Explicit results** no value · target\_doc.

**Explicit failure paths** validation helper — translated “Purchase Order Item reference is missing in Subcontracting Receipt {0}”.format(source\_doc.name) · validation helper — get\_uncombinable\_orders\_message(purchase\_orders).

**Local steps**

- If isinstance(source\_name, str).
  - Set source\_doc from Platform.get\_doc(“Subcontracting Receipt”, source\_name).
- Otherwise.
  - Set source\_doc from source\_name.
- If source\_doc.is\_return.
  - Return no value.
- Evaluate validate\_no\_purchase\_receipt\_made(source\_doc).
- Set po\_sr\_items from defaultdict(list).
- For each item in source\_doc.items.
  - If item.purchase\_order.
    - Evaluate po\_sr\_items at item.purchase\_order\_item.append(item).
- Set purchase\_orders from get\_purchase\_orders(source\_doc).
- If not purchase\_orders.
  - Call the validation error handler Platform.throw(translated “Purchase Order Item reference is missing in Subcontracting Receipt {0}”.format(source\_doc.name)).
- If not can\_combine\_purchase\_orders(purchase\_orders).
  - Call the validation error handler Platform.throw(get\_uncombinable\_orders\_message(purchase\_orders), title = translated “Cannot Combine Orders”).
- Bind local operation update\_item for subsequent calls.
- Bind local operation post\_process for subsequent calls.
- Set target\_doc from no value.
- Set first\_order\_charges from 0.
- For each po\_name in purchase\_orders.
  - Set is\_first\_order from target\_doc is identical to no value.
  - Set charges\_before from len(target\_doc.taxes) when target\_doc, otherwise 0.
    - Value choice on target\_doc — true gives len(target\_doc.taxes), false gives 0.
  - Set target\_doc from get\_mapped\_doc(“Purchase Order”, po\_name, mapping(“Purchase Order” → mapping(“doctype” → “Purchase Receipt”, “field\_map” → mapping(“supplier\_warehouse” → “supplier\_warehouse”), “validation” → mapping(“docs ….
  - If is\_first\_order.
    - Set first\_order\_charges from len(target\_doc.taxes).
  - Otherwise.
    - Evaluate merge\_order\_charges(target\_doc, first\_order\_charges, charges\_before).
- Evaluate target\_doc.calculate\_taxes\_and\_totals().
- If not target\_doc.get(“items”).
  - Evaluate add\_po\_items\_to\_pr(source\_doc, target\_doc).
- If ((save or submit) and Platform.has\_permission(target\_doc.doctype, “create”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (save or submit) → Platform.has\_permission(target\_doc.doctype, “create”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in save → submit.
  - Evaluate target\_doc.save().
  - If (submit and Platform.has\_permission(target\_doc.doctype, “submit”, target\_doc)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in submit → Platform.has\_permission(target\_doc.doctype, “submit”, target\_doc).
    - Attempt the following.
      - Evaluate target\_doc.submit().
    - On failure (Exception) bound to e.
      - Evaluate target\_doc.add\_comment(“Comment”, ((translated “Submit Action Failed” + text in the contract) + str(e))).
  - If notify.
    - Evaluate Platform.msgprint(translated “Purchase Receipt {0} created.”.format(get\_link\_to\_form(target\_doc.doctype, target\_doc.name)), indicator = “green”, alert = true).
- Return target\_doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(target\_doc.doctype, “create”), Platform.has\_permission(target\_doc.doctype, “submit”, target\_doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1205)

<a id="op-7e1ce33056e8a0"></a>
### Make purchase receipt.update item

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_make_purchase_receipt_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set sr\_items from po\_sr\_items at obj.name.
- Set ratio from (flt(obj.qty) ÷ flt(obj.fg\_item\_qty)).
- Evaluate target.update(mapping(“qty” → (ratio × sum(generator of flt(nested operand in the contract.qty) for item drawn from sr\_items)), “rejected\_qty” → (ratio × sum(generator of flt(nested operand in the contract ….
  - Draw item from sr\_items.
  - Draw item from sr\_items.
  - Draw item from sr\_items, keep a combination only if (item.rejected\_warehouse).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1207)

<a id="op-e9461294dbd0f9"></a>
### Make purchase receipt.post process

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_make_purchase_receipt_post_process`

**Inputs** source, target.

**Local steps**

- Evaluate target.set\_missing\_values().
- Evaluate target.update(mapping(“posting\_date” → source\_doc.posting\_date, “posting\_time” → source\_doc.posting\_time, “subcontracting\_receipt” → source\_doc.name, “supplier\_warehouse” → source\_doc.supplier\_warehouse, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1206)

<a id="op-a485050b780909"></a>
### Merge order charges

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_merge_order_charges`

**Inputs** target\_doc, first\_order\_charges, order\_charges\_start.

**Local steps**

- Set key\_fields from get\_charge\_key\_fields().
- Bind local operation get\_charge\_key for subsequent calls.
- Set first\_order\_rows from defaultdict(list).
- For each row in target\_doc.taxes at slice no value to first\_order\_charges.
  - If row.charge\_type equals “Actual”.
    - Evaluate first\_order\_rows at get\_charge\_key(row).append(row).
- For each row in target\_doc.taxes at slice order\_charges\_start to no value.
  - If matching\_rows bound to first\_order\_rows.get(get\_charge\_key(row)).
    - Set first\_row from matching\_rows.pop(0).
    - Set first\_row.tax\_amount from (flt(first\_row.tax\_amount) + flt(row.tax\_amount)).
    - Evaluate target\_doc.remove(row).
- For each tuple(idx, row) in enumerate(target\_doc.taxes, 1).
  - Set row.idx from idx.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1210)

<a id="op-d57c50126adf07"></a>
### Merge order charges.get charge key

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_merge_order_charges_get_charge_key`

**Inputs** row.

**Declared result** tuple.

**Explicit results** tuple(generator of row.get(field) for field drawn from key\_fields).

**Local steps**

- Return tuple(generator of row.get(field) for field drawn from key\_fields).
  - Draw field from key\_fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1211)

<a id="op-e1616287b65e0e"></a>
### Validate no purchase receipt made

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_validate_no_purchase_receipt_made`

**Inputs** scr\_doc.

**Explicit failure paths** validation helper — translated “Submit Subcontracting Receipt {0} before making a Purchase Receipt”.format(scr\_doc.name).

**Local steps**

- <a id="op-e1616287b65e0e-guard-2"></a>If scr\_doc.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Submit Subcontracting Receipt {0} before making a Purchase Receipt”.format(scr\_doc.name)).
- Evaluate validate\_single\_purchase\_receipt(scr\_doc.name).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison scr\_doc.docstatus differs from 1, scr\_doc.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Submit Subcontracting Receipt {0} before making a Purchase Receipt”.format(scr\_doc.name). With scr\_doc.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e1616287b65e0e-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1232)

<a id="op-7c0c8e1581d122"></a>
### Validate single purchase receipt

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_validate_single_purchase_receipt`

**Inputs** subcontracting\_receipt, purchase\_receipt = no value.

**Record and data access** read “Purchase Receipt” via get\_value.

**Explicit failure paths** validation helper — translated “Purchase Receipt {0} is already made against Subcontracting Receipt {1}”.format(get\_link\_to\_form(“Purchase Receipt”, existing), subcontracting\_receipt).

**Local steps**

- If existing bound to Platform.db.get\_value(“Purchase Receipt”, mapping(“subcontracting\_receipt” → subcontracting\_receipt, “is\_return” → 0, “docstatus” → tuple(“&lt;”, 2), “name” → tuple(“!=”, (purchase\_receipt or empty text)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in purchase\_receipt → empty text.
  - Call the validation error handler Platform.throw(translated “Purchase Receipt {0} is already made against Subcontracting Receipt {1}”.format(get\_link\_to\_form(“Purchase Receipt”, existing), subcontracting\_receipt)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1233)

<a id="op-ebe9c2f01dd9b4"></a>
### Get purchase orders

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_get_purchase_orders`

**Inputs** scr\_doc.

**Declared result** list at str.

**Explicit results** list(dict.fromkeys(generator of item.purchase\_order for item drawn from scr\_doc.items where item.purchase\_order)).

**Local steps**

- Return list(dict.fromkeys(generator of item.purchase\_order for item drawn from scr\_doc.items where item.purchase\_order)).
  - Draw item from scr\_doc.items, keep a combination only if (item.purchase\_order).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1202)

<a id="op-43877e6d4c3387"></a>
### Can combine purchase orders

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_can_combine_purchase_orders`

**Inputs** purchase\_orders.

**Declared result** bool.

**Explicit results** (len(purchase\_orders) &lt; 2 or len(get\_purchase\_order\_terms(purchase\_orders)) equals 1).

**Local steps**

- Return (len(purchase\_orders) &lt; 2 or len(get\_purchase\_order\_terms(purchase\_orders)) equals 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(purchase\_orders) &lt; 2 → len(get\_purchase\_order\_terms(purchase\_orders)) equals 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1197)

<a id="op-33eae6762ba515"></a>
### Get purchase order terms

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_get_purchase_order_terms`

**Inputs** purchase\_orders.

**Declared result** set at tuple.

**Record and data access** read “Purchase Order” via get\_all.

**Explicit results** set of tuple(order.currency, get\_tax\_terms(taxes at order.name, key\_fields), get\_discount\_terms(order)) for order drawn from Platform.get\_all(“Purchase Order”, filters = mapping(“name” → list(“in”, purchas ….

**Local steps**

- Set key\_fields from get\_charge\_key\_fields().
- Set taxes from get\_purchase\_order\_taxes(purchase\_orders, key\_fields).
- Return set of tuple(order.currency, get\_tax\_terms(taxes at order.name, key\_fields), get\_discount\_terms(order)) for order drawn from Platform.get\_all(“Purchase Order”, filters = mapping(“name” → list(“in”, purchas ….
  - Draw order from Platform.get\_all(“Purchase Order”, filters = mapping(“name” → list(“in”, purchase\_orders)), fields = list(“name”, “currency”, “apply\_discount\_on”, “additional\_discount\_percentage”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1201)

<a id="op-583a1ae61fff74"></a>
### Get purchase order taxes

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_get_purchase_order_taxes`

**Inputs** purchase\_orders, key\_fields.

**Declared result** dict at tuple(str, list).

**Record and data access** read “Purchase Taxes and Charges” via get\_all.

**Explicit results** taxes.

**Local steps**

- Set taxes from defaultdict(list).
- For each row in Platform.get\_all(“Purchase Taxes and Charges”, filters = mapping(“parenttype” → “Purchase Order”, “parent” → list(“in”, purchase\_orders), “is\_tax\_withholding\_account” → 0), fields = list(“parent”, “charge\_ ….
  - Evaluate taxes at row.parent.append(row).
- Return taxes.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1200)

<a id="op-def89e627912e9"></a>
### Get discount terms

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_get_discount_terms`

**Inputs** order.

**Declared result** tuple.

**Explicit results** tuple(order.apply\_discount\_on, flt(order.additional\_discount\_percentage)) · tuple(order.name) · tuple().

**Local steps**

- If flt(order.additional\_discount\_percentage).
  - Return tuple(order.apply\_discount\_on, flt(order.additional\_discount\_percentage)).
- If flt(order.discount\_amount).
  - Return tuple(order.name).
- Return tuple().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1199)
