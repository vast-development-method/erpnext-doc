# Inventory and warehouses · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase receipt

[Record definition](../../../../data/record-types/purchase_receipt.json)

<a id="op-97ac5d5e253124"></a>
### Purchase Receipt.get po qty and warehouse

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_get_purchase_order_quantity_and_warehouse`

**Inputs** self, po\_detail.

**Record and data access** read “Purchase Order Item” via get\_value.

**Explicit results** tuple(po\_qty, po\_warehouse).

**Local steps**

- Set tuple(po\_qty, po\_warehouse) from Platform.db.get\_value(“Purchase Order Item”, po\_detail, list(“qty”, “warehouse”)).
- Return tuple(po\_qty, po\_warehouse).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0774.json#L6445) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L197)

<a id="op-632d49db0c6260"></a>
### Purchase Receipt.on submit

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Authorization Control” via get\_cached\_doc.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate super().on\_submit().
- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(self.doctype, self.company, self.base\_grand\_total).
- Evaluate self.update\_prevdoc\_status().
- If flt(self.per\_billed) &lt; 100.
  - Evaluate self.update\_billing\_status().
- Otherwise.
  - Evaluate self.db\_set(“status”, “Completed”).
- Evaluate self.make\_bundle\_for\_sales\_purchase\_return().
- Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields().
- Evaluate self.update\_stock\_ledger().
- Evaluate self.make\_gl\_entries().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.set\_consumed\_qty\_in\_subcontract\_order().
- Evaluate self.reserve\_stock().
- Evaluate self.update\_received\_qty\_if\_from\_pp().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update prevdoc status](operations-043.md#op-be53edd129efe6), [update billing status](operations-045.md#op-0b88afb7b5cf84), [reserve stock](operations-045.md#op-05df8401f23bf6), [update received qty if from pp](operations-044.md#op-23c370b0795741).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L201)

<a id="op-23c370b0795741"></a>
### Purchase Receipt.update received qty if from pp

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_update_received_quantity_if_from_production_plan`

**Inputs** self.

**Record and data access** read “Production Plan Sub Assembly Item” via get\_all.

**State and service calls** request set\_value on “Production Plan Sub Assembly Item” · request set\_value on “Production Plan”.

**Local steps**

- Bind dependencies Coalesce, Sum.
- Set items\_from\_po from list of item.purchase\_order\_item for item drawn from self.items where item.purchase\_order\_item.
  - Draw item from self.items, keep a combination only if (item.purchase\_order\_item).
- If items\_from\_po.
  - Set table from Platform.qb.DocType(“Purchase Order Item”).
  - Set subquery from nested operand in the contract(nested operand in the contract).select(table.production\_plan\_sub\_assembly\_item).distinct().where((table.name.isin(items\_from\_po) bitwise and Coalesce(table.production\_plan\_su ….
  - Set result from subquery.run(as\_dict = true).
  - If result.
    - Set result from list of item.production\_plan\_sub\_assembly\_item for item drawn from result.
      - Draw item from result.
    - Set production\_plan\_names from set(Platform.db.get\_all(“Production Plan Sub Assembly Item”, filters = mapping(“name” → tuple(“in”, result)), pluck = “parent”)).
    - Set query from nested operand in the contract(nested operand in the contract).select(table.production\_plan\_sub\_assembly\_item, nested operand in the contract.as\_(“received\_qty”)).where(table.production\_plan\_sub\_assembly\_i ….
    - For each row in query.run(as\_dict = true).
      - Evaluate Platform.db.set\_value(“Production Plan Sub Assembly Item”, row.production\_plan\_sub\_assembly\_item, “received\_qty”, row.received\_qty).
    - For each production\_plan\_name in production\_plan\_names.
      - Evaluate Platform.db.set\_value(“Production Plan”, production\_plan\_name, mapping(“modified” → now(), “modified\_by” → Platform.session.user), update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L206)

<a id="op-2786649dfeed62"></a>
### Purchase Receipt.on cancel

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().on\_cancel().
- Evaluate self.check\_purchase\_order\_on\_hold\_or\_close(“purchase\_order”).
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.update\_billing\_status().
- Evaluate self.update\_stock\_ledger().
- Evaluate self.make\_gl\_entries\_on\_cancel().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Serial and Batch Bundle”, …).
- Evaluate self.delete\_auto\_created\_batches().
- Evaluate self.set\_consumed\_qty\_in\_subcontract\_order().
- Evaluate self.update\_received\_qty\_if\_from\_pp().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update prevdoc status](operations-043.md#op-be53edd129efe6), [update billing status](operations-045.md#op-0b88afb7b5cf84), [update received qty if from pp](operations-044.md#op-23c370b0795741).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L200)

<a id="op-b32cf47ff1d412"></a>
### Purchase Receipt.before cancel

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().before\_cancel().
- Evaluate self.remove\_amount\_difference\_with\_purchase\_invoice().
- Evaluate self.cancel\_stock\_reservations\_made\_by\_receipt().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove amount difference with purchase invoice](operations-044.md#op-3b256ac9c54ba3), [cancel stock reservations made by receipt](operations-044.md#op-9b970c6017b061).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L192)

<a id="op-9b970c6017b061"></a>
### Purchase Receipt.cancel stock reservations made by receipt

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_cancel_stock_reservations_made_by_receipt`

**Inputs** self.

**Local steps**

- Bind dependencies cancel\_stock\_reservation\_entries.
- Evaluate cancel\_stock\_reservation\_entries(from\_voucher\_type = “Purchase Receipt”, from\_voucher\_no = self.name, notify = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1012) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L509)

<a id="op-3b256ac9c54ba3"></a>
### Purchase Receipt.remove amount difference with purchase invoice

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_remove_amount_difference_with_purchase_invoice`

**Inputs** self.

**Local steps**

- For each item in self.items.
  - Set item.amount\_difference\_with\_purchase\_invoice from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0775.json#L1056) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L203)

<a id="op-5f6ca9f17825e8"></a>
### Purchase Receipt.get gl entries

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map = no value, via\_landed\_cost\_voucher = false.

**Explicit results** process\_gl\_map(gl\_entries, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Local steps**

- Bind dependencies process\_gl\_map.
- Set gl\_entries from list().
- Evaluate self.make\_item\_gl\_entries(gl\_entries, inventory\_account\_map = inventory\_account\_map).
- Evaluate self.make\_tax\_gl\_entries(gl\_entries, via\_landed\_cost\_voucher).
- Evaluate self.set\_gl\_entry\_for\_purchase\_expense(gl\_entries).
- Evaluate update\_regional\_gl\_entries(gl\_entries, self).
- Return process\_gl\_map(gl\_entries, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Methods declared on this owner** [make item gl entries](operations-044.md#op-1549a068d301cd), [make tax gl entries](operations-044.md#op-017979b0d6cc6a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L196)

<a id="op-423052c35c28c4"></a>
### Purchase Receipt.is rejected material valued

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_is_rejected_material_valued`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** true · bool(Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”)).

**Local steps**

- If self.is\_internal\_transfer().
  - Return true.
- Return bool(Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1018) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L515)

<a id="op-22b9009f80ff07"></a>
### Purchase Receipt.has booked rejected material

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_has_booked_rejected_material`

**Inputs** self, item.

**Declared result** bool.

**Explicit results** false · not (item.from\_warehouse and item.rejected\_warehouse equals item.from\_warehouse).

**Local steps**

- If not (flt(item.rejected\_qty) and self.is\_rejected\_material\_valued()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(item.rejected\_qty) → self.is\_rejected\_material\_valued().
  - Return false.
- Return not (item.from\_warehouse and item.rejected\_warehouse equals item.from\_warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.from\_warehouse → item.rejected\_warehouse equals item.from\_warehouse.

**Methods declared on this owner** [is rejected material valued](operations-044.md#op-423052c35c28c4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1017) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L514)

<a id="op-1549a068d301cd"></a>
### Purchase Receipt.make item gl entries

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries`

**Inputs** self, gl\_entries, inventory\_account\_map = no value.

**Record and data access** read “Company” via get\_value · resolve a document from “Warehouse” via get\_cached\_doc.

**State and service calls** msgprint with ((translated “No accounting entries for the following warehouses” + “: \\n”) + whitespace '\\n'.join(warehouse\_with\_no\_account)).

**Local steps**

- Bind dependencies get\_purchase\_document\_details.
- Bind dependencies get\_custom\_dimension\_overrides.
- Set provisional\_accounting\_for\_non\_stock\_items from cint(Platform.db.get\_value(“Company”, self.company, “enable\_provisional\_accounting\_for\_non\_stock\_items”)).
- Set tuple(exchange\_rate\_map, net\_rate\_map) from get\_purchase\_document\_details(self).
- Bind local operation validate\_account for subsequent calls.
- Bind local operation make\_item\_asset\_inward\_gl\_entry for subsequent calls.
- Bind local operation make\_stock\_received\_but\_not\_billed\_entry for subsequent calls.
- Bind local operation make\_landed\_cost\_gl\_entries for subsequent calls.
- Bind local operation make\_expenses\_added\_to\_stock\_entries for subsequent calls.
- Bind local operation make\_amount\_difference\_entry for subsequent calls.
- Bind local operation make\_sub\_contracting\_gl\_entries for subsequent calls.
- Bind local operation make\_divisional\_loss\_gl\_entry for subsequent calls.
- Set stock\_items from self.get\_stock\_items().
- Set perpetual\_inventory from Enterprise.is\_perpetual\_inventory\_enabled(self.company).
- Set warehouse\_with\_no\_account from list().
- For each d in self.get(“items”).
  - Set remarks from (self.get(“remarks”) or translated “Accounting Entry for {0}”.format(“Asset” when d.is\_fixed\_asset, otherwise “Stock”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for {0}”.format(“Asset” when d.is\_fixed\_asset, otherwise “Stock”).
    - Value choice on d.is\_fixed\_asset — true gives “Asset”, false gives “Stock”.
  - Set stock\_value\_diff from 0.
  - If (perpetual\_inventory and d.item\_code belongs to stock\_items and flt(d.qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in perpetual\_inventory → d.item\_code belongs to stock\_items → flt(d.qty).
    - Set stock\_value\_diff from get\_stock\_value\_difference(self.name, d.name, d.warehouse).
  - If (provisional\_accounting\_for\_non\_stock\_items and d.item\_code does not belong to stock\_items and flt(d.qty) and d.get(“provisional\_expense\_account”) and not d.is\_fixed\_asset).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in provisional\_accounting\_for\_non\_stock\_items → d.item\_code does not belong to stock\_items → flt(d.qty) → d.get(“provisional\_expense\_account”) → not d.is\_fixed\_asset.
    - Evaluate self.add\_provisional\_gl\_entry(d, gl\_entries, self.posting\_date, d.get(“provisional\_expense\_account”)).
  - Otherwise.
    - If (flt(d.qty) and (flt(d.valuation\_rate) or flt(stock\_value\_diff) or self.is\_return)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(d.qty) → (flt(d.valuation\_rate) or flt(stock\_value\_diff) or self.is\_return).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.valuation\_rate) → flt(stock\_value\_diff) → self.is\_return.
      - If not ((perpetual\_inventory and d.item\_code belongs to stock\_items) or (d.is\_fixed\_asset and not d.purchase\_invoice)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (perpetual\_inventory and d.item\_code belongs to stock\_items) → (d.is\_fixed\_asset and not d.purchase\_invoice).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in perpetual\_inventory → d.item\_code belongs to stock\_items.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_fixed\_asset → not d.purchase\_invoice.
        - Continue with the next iteration or loop test.
      - Set stock\_asset\_rbnb from self.get\_company\_default(“asset\_received\_but\_not\_billed”) when d.is\_fixed\_asset, otherwise self.get\_company\_default(“stock\_received\_but\_not\_billed”).
        - Value choice on d.is\_fixed\_asset — true gives self.get\_company\_default(“asset\_received\_but\_not\_billed”), false gives self.get\_company\_default(“stock\_received\_but\_not\_billed”).
      - Set landed\_cost\_entries from self.get\_item\_account\_wise\_lcv\_entries().
      - If d.is\_fixed\_asset.
        - Set stock\_asset\_account\_name from d.expense\_account.
        - Set stock\_value\_diff from ((flt(d.base\_net\_amount) + flt(d.item\_tax\_amount)) + flt(d.landed\_cost\_voucher\_amount)).
      - Otherwise.
        - If inventory\_account bound to self.get\_inventory\_account\_dict(d, inventory\_account\_map).
          - Set stock\_asset\_account\_name from inventory\_account at “account”.
          - Set supplier\_warehouse\_account from no value.
          - Set supplier\_warehouse\_account\_currency from no value.
          - If self.supplier\_warehouse.
            - Set supplier\_warehouse\_account from get\_warehouse\_account(Platform.get\_cached\_doc(“Warehouse”, self.supplier\_warehouse), raise\_error = bool(flt(d.rm\_supp\_cost))).
            - If supplier\_warehouse\_account.
              - Set supplier\_warehouse\_account\_currency from get\_account\_currency(supplier\_warehouse\_account).
          - If (flt(stock\_value\_diff) equals flt(d.rm\_supp\_cost) and supplier\_warehouse\_account and stock\_asset\_account\_name equals supplier\_warehouse\_account).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(stock\_value\_diff) equals flt(d.rm\_supp\_cost) → supplier\_warehouse\_account → stock\_asset\_account\_name equals supplier\_warehouse\_account.
            - Continue with the next iteration or loop test.
      - Evaluate make\_item\_asset\_inward\_gl\_entry(d, stock\_value\_diff, stock\_asset\_account\_name).
      - Set outgoing\_amount from make\_stock\_received\_but\_not\_billed\_entry(d).
      - Evaluate make\_landed\_cost\_gl\_entries(d).
      - Evaluate make\_expenses\_added\_to\_stock\_entries(d).
      - Evaluate make\_amount\_difference\_entry(d).
      - Evaluate make\_sub\_contracting\_gl\_entries(d).
      - Evaluate make\_divisional\_loss\_gl\_entry(d, outgoing\_amount).
    - Otherwise.
      - If ((d.warehouse and d.qty and d.warehouse does not belong to warehouse\_with\_no\_account) or (not self.is\_rejected\_material\_valued() and d.rejected\_warehouse and d.rejected\_warehouse does not belong to warehou ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (d.warehouse and d.qty and d.warehouse does not belong to warehouse\_with\_no\_account) → (not self.is\_rejected\_material\_valued() and d.rejected\_warehouse and d.rejected\_warehouse does not belong to warehouse\_with\_no\_account).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.warehouse → d.qty → d.warehouse does not belong to warehouse\_with\_no\_account.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_rejected\_material\_valued() → d.rejected\_warehouse → d.rejected\_warehouse does not belong to warehouse\_with\_no\_account.
        - Evaluate warehouse\_with\_no\_account.append((d.warehouse or d.rejected\_warehouse)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.warehouse → d.rejected\_warehouse.
  - If (d.is\_fixed\_asset and d.landed\_cost\_voucher\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_fixed\_asset → d.landed\_cost\_voucher\_amount.
    - Evaluate self.update\_assets(d, d.valuation\_rate).
  - If (d.item\_code belongs to stock\_items and self.has\_booked\_rejected\_material(d)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code belongs to stock\_items → self.has\_booked\_rejected\_material(d).
    - Set stock\_asset\_rbnb from self.get\_company\_default(“asset\_received\_but\_not\_billed”) when d.is\_fixed\_asset, otherwise self.get\_company\_default(“stock\_received\_but\_not\_billed”).
      - Value choice on d.is\_fixed\_asset — true gives self.get\_company\_default(“asset\_received\_but\_not\_billed”), false gives self.get\_company\_default(“stock\_received\_but\_not\_billed”).
    - Set stock\_value\_diff from get\_stock\_value\_difference(self.name, d.name, d.rejected\_warehouse).
    - Set \_inv\_dict from self.get\_inventory\_account\_dict(d, inventory\_account\_map, “rejected\_warehouse”).
    - Set stock\_asset\_account\_name from \_inv\_dict at “account”.
    - Evaluate make\_item\_asset\_inward\_gl\_entry(d, stock\_value\_diff, stock\_asset\_account\_name).
    - If not d.qty.
      - Evaluate make\_stock\_received\_but\_not\_billed\_entry(d).
- If warehouse\_with\_no\_account.
  - Evaluate Platform.msgprint(((translated “No accounting entries for the following warehouses” + “: \\n”) + whitespace '\\n'.join(warehouse\_with\_no\_account))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add provisional gl entry](operations-044.md#op-57a6ff5b4c77e1), [is rejected material valued](operations-044.md#op-423052c35c28c4), [update assets](operations-044.md#op-839fb731569a7e), [has booked rejected material](operations-044.md#op-22b9009f80ff07).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Warehouse”, self.supplier\_warehouse).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1019) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L516)

<a id="op-12ad11dd4f41fc"></a>
### Purchase Receipt.make item gl entries.validate account

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_validate_account`

**Inputs** account\_type.

**Explicit failure paths** validation helper — translated “{0} account not found while submitting purchase receipt”.format(account\_type).

**Local steps**

- Call the validation error handler Platform.throw(translated “{0} account not found while submitting purchase receipt”.format(account\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1027) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L524)

<a id="op-985fe503dd20f8"></a>
### Purchase Receipt.make item gl entries.make item asset inward gl entry

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_make_item_asset_inward_gl_entry`

**Inputs** item, stock\_value\_diff, stock\_asset\_account\_name.

**Local steps**

- Set account\_currency from get\_account\_currency(stock\_asset\_account\_name).
- If not stock\_asset\_account\_name.
  - Evaluate validate\_account(“Asset or warehouse account”).
- Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = stock\_asset\_account\_name, cost\_center = d.cost\_center, debit = stock\_value\_diff, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1023) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L520)

<a id="op-7011bc402144f1"></a>
### Purchase Receipt.make item gl entries.make stock received but not billed entry

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_make_stock_received_but_not_billed_entry`

**Inputs** item.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** 0.0 · outgoing\_amount.

**Local steps**

- If (self.get(“is\_return”) and item.return\_qty\_from\_rejected\_warehouse and not self.is\_internal\_transfer() and not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → item.return\_qty\_from\_rejected\_warehouse → not self.is\_internal\_transfer() → not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).
  - Return 0.0.
- Set account from stock\_asset\_rbnb.
- If item.from\_warehouse.
  - Set \_inv\_dict from self.get\_inventory\_account\_dict(item, inventory\_account\_map, “from\_warehouse”).
  - Set account from \_inv\_dict at “account”.
- Set account\_currency from get\_account\_currency(account).
- Set credit\_amount from flt(item.base\_net\_amount, item.precision(“base\_net\_amount”)) when account\_currency equals self.company\_currency, otherwise flt(item.net\_amount, item.precision(“net\_amount”)).
  - Value choice on account\_currency equals self.company\_currency — true gives flt(item.base\_net\_amount, item.precision(“base\_net\_amount”)), false gives flt(item.net\_amount, item.precision(“net\_amount”)).
- Set outgoing\_amount from item.base\_net\_amount.
- If (self.is\_internal\_transfer() and item.valuation\_rate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → item.valuation\_rate.
  - Set outgoing\_amount from (negative 1 × flt(get\_stock\_value\_difference(self.name, item.name, item.from\_warehouse))).
  - Set credit\_amount from outgoing\_amount.
- If (item.get(“rejected\_qty”) and item.item\_code belongs to stock\_items and not self.is\_internal\_transfer() and Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“rejected\_qty”) → item.item\_code belongs to stock\_items → not self.is\_internal\_transfer() → Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).
  - Update outgoing\_amount using + get\_stock\_value\_difference(self.name, item.name, item.rejected\_warehouse).
  - If not flt(item.qty).
    - Update outgoing\_amount using − flt(item.item\_tax\_amount).
  - Set credit\_amount from outgoing\_amount.
- If credit\_amount.
  - If not account.
    - Evaluate validate\_account(“Stock or Asset Received But Not Billed”).
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = account, cost\_center = item.cost\_center, debit = (negative 1 × flt(outgoing\_amount, item.precision(“base\_net\_amount”))), …).
  - If d.get(“purchase\_invoice”).
    - If (exchange\_rate\_map at item.purchase\_invoice and self.conversion\_rate differs from exchange\_rate\_map at item.purchase\_invoice and item.net\_rate equals net\_rate\_map at item.purchase\_invoice\_item).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in exchange\_rate\_map at item.purchase\_invoice → self.conversion\_rate differs from exchange\_rate\_map at item.purchase\_invoice → item.net\_rate equals net\_rate\_map at item.purchase\_invoice\_item.
      - Set discrepancy\_caused\_by\_exchange\_rate\_difference from flt(((item.qty × item.net\_rate) × (exchange\_rate\_map at item.purchase\_invoice − self.conversion\_rate)), item.precision(“base\_net\_amount”)).
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = account, cost\_center = item.cost\_center, debit = 0.0, …).
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = self.get\_company\_default(“exchange\_gain\_loss\_account”), cost\_center = d.cost\_center, debit = discrepancy\_caused\_by\_exchange\_rate\_difference, …).
- Return outgoing\_amount.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1025) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L522)

<a id="op-a26757f69c9e77"></a>
### Purchase Receipt.make item gl entries.make landed cost gl entries

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_make_landed_cost_gl_entries`

**Inputs** item.

**Explicit results** no value.

**Local steps**

- If not (item.landed\_cost\_voucher\_amount and landed\_cost\_entries).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.landed\_cost\_voucher\_amount → landed\_cost\_entries.
  - Return no value.
- For each entry in landed\_cost\_entries.get(tuple(item.item\_code, item.name), list()).
  - If not (entry.amount or entry.base\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.amount → entry.base\_amount.
    - Continue with the next iteration or loop test.
  - Set account from entry.expense\_account.
  - If not account.
    - Evaluate validate\_account(“Landed Cost Account”).
  - Set account\_currency from get\_account\_currency(account).
  - Set credit\_amount from flt(entry.base\_amount) when (entry.base\_amount or account\_currency differs from self.company\_currency), otherwise flt(entry.amount).
    - Value choice on (entry.base\_amount or account\_currency differs from self.company\_currency) — true gives flt(entry.base\_amount), false gives flt(entry.amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.base\_amount → account\_currency differs from self.company\_currency.
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = account, cost\_center = (entry.dimensions.cost\_center or item.cost\_center), debit = 0.0, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.cost\_center → item.cost\_center.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.project → item.project.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1024) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L521)

<a id="op-cea7da335e2a21"></a>
### Purchase Receipt.make item gl entries.make expenses added to stock entries

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_make_expenses_added_to_stock_entries`

**Inputs** item.

**Explicit results** no value.

**Local steps**

- If not self.book\_stock\_expense\_enabled().
  - Return no value.
- Set amount from flt(item.landed\_cost\_voucher\_amount, item.precision(“base\_net\_amount”)).
- If (amount and not item.is\_fixed\_asset).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in amount → not item.is\_fixed\_asset.
  - Evaluate self.append\_expenses\_added\_to\_stock\_pair(gl\_entries, item.item\_code, amount, item).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1022) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L519)

<a id="op-03cb1517553b64"></a>
### Purchase Receipt.make item gl entries.make amount difference entry

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_make_amount_difference_entry`

**Inputs** item.

**Local steps**

- If (item.amount\_difference\_with\_purchase\_invoice and stock\_asset\_rbnb).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.amount\_difference\_with\_purchase\_invoice → stock\_asset\_rbnb.
  - Set account\_currency from get\_account\_currency(stock\_asset\_rbnb).
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = stock\_asset\_rbnb, cost\_center = item.cost\_center, debit = 0.0, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1020) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L517)

<a id="op-9d69893f70cecd"></a>
### Purchase Receipt.make item gl entries.make sub contracting gl entries

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_make_sub_contracting_gl_entries`

**Inputs** item.

**Local steps**

- If (flt(item.rm\_supp\_cost) and supplier\_warehouse\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(item.rm\_supp\_cost) → supplier\_warehouse\_account.
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = supplier\_warehouse\_account, cost\_center = item.cost\_center, debit = 0.0, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1026) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L523)

<a id="op-ac1618c1d26930"></a>
### Purchase Receipt.make item gl entries.make divisional loss gl entry

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_item_gl_entries_make_divisional_loss_gl_entry`

**Inputs** item, outgoing\_amount.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If item.is\_fixed\_asset.
  - Return no value.
- Set valuation\_amount\_as\_per\_doc from ((((flt(outgoing\_amount, nested operand in the contract.precision(“base\_net\_amount”)) + flt(item.landed\_cost\_voucher\_amount)) + flt(item.rm\_supp\_cost)) + flt(item.item\_tax\_amount)) + flt(item.amount\_differ ….
- Set divisional\_loss from flt((valuation\_amount\_as\_per\_doc − flt(stock\_value\_diff)), item.precision(“base\_net\_amount”)).
- If self.has\_booked\_rejected\_material(item).
  - Set rejected\_item\_cost from get\_stock\_value\_difference(self.name, item.name, item.rejected\_warehouse).
  - Update divisional\_loss using − rejected\_item\_cost.
- If divisional\_loss.
  - Set loss\_account from (self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true) or stock\_asset\_rbnb).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true) → stock\_asset\_rbnb.
  - If (self.is\_return and item.expense\_account and item.expense\_account differs from stock\_asset\_rbnb).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → item.expense\_account → item.expense\_account differs from stock\_asset\_rbnb.
    - Set loss\_account from item.expense\_account.
  - Set cost\_center from (item.cost\_center or Platform.get\_cached\_value(“Company”, self.company, “cost\_center”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.cost\_center → Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).
  - Set account\_currency from get\_account\_currency(loss\_account).
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = loss\_account, cost\_center = cost\_center, debit = divisional\_loss, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1021) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L518)

<a id="op-57a6ff5b4c77e1"></a>
### Purchase Receipt.add provisional gl entry

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_add_provisional_general_ledger_entry`

**Inputs** self, item, gl\_entries, posting\_date, provisional\_account, reverse = 0, item\_amount = no value.

**Local steps**

- Evaluate post\_provisional\_gl\_entry(self, item, gl\_entries, posting\_date, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L191)

<a id="op-6d0c39dda39c55"></a>
### Purchase Receipt.is landed cost booked for any item

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_is_landed_cost_booked_for_any_item`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- For each x in self.items.
  - <a id="op-6d0c39dda39c55-guard-3"></a>If x.landed\_cost\_voucher\_amount differs from 0.
    - Return true.
- Return false.

**Derived branch illustrations**

- At the comparison x.landed\_cost\_voucher\_amount differs from 0, x.landed\_cost\_voucher\_amount = 1 selects the branch that returns true. With x.landed\_cost\_voucher\_amount = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6d0c39dda39c55-guard-3)

[Applicable decision contract](../../../enterprise-decision-contracts/part-0775.json#L1358) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L199)

<a id="op-017979b0d6cc6a"></a>
### Purchase Receipt.make tax gl entries

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_make_tax_gl_entries`

**Inputs** self, gl\_entries, via\_landed\_cost\_voucher = false.

**Explicit failure paths** validation helper — translated “Cost Center is required in row {0} in Taxes table for type {1}”.format(tax.idx, translated tax.category).

**Local steps**

- Set negative\_expense\_to\_be\_booked from sum(list of flt(d.item\_tax\_amount) for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
- Set capitalized\_valuation\_tax from self.get\_capitalized\_valuation\_tax().
- Set valuation\_tax from mapping().
- For each tax in self.get(“taxes”).
  - If (tax.category belongs to tuple(“Valuation”, “Valuation and Total”) and flt(tax.base\_tax\_amount\_after\_discount\_amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.category belongs to tuple(“Valuation”, “Valuation and Total”) → flt(tax.base\_tax\_amount\_after\_discount\_amount).
    - If not tax.cost\_center.
      - Call the validation error handler Platform.throw(translated “Cost Center is required in row {0} in Taxes table for type {1}”.format(tax.idx, translated tax.category)).
    - Set valuation\_tax at tax.name from capitalized\_valuation\_tax.get(tax.name, 0.0).
- If (negative\_expense\_to\_be\_booked and valuation\_tax).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in negative\_expense\_to\_be\_booked → valuation\_tax.
  - Set against\_accounts from “, ”.join(list of d.account for d drawn from gl\_entries where flt(d.debit) &gt; 0).
    - Draw d from gl\_entries, keep a combination only if (flt(d.debit) &gt; 0).
  - Set total\_valuation\_amount from sum(valuation\_tax.values()).
  - Set amount\_including\_divisional\_loss from negative\_expense\_to\_be\_booked.
  - Set i from 1.
  - For each tax in self.get(“taxes”).
    - If valuation\_tax.get(tax.name).
      - Set account from tax.account\_head.
      - If i equals len(valuation\_tax).
        - Set applicable\_amount from amount\_including\_divisional\_loss.
      - Otherwise.
        - Set applicable\_amount from (negative\_expense\_to\_be\_booked × (valuation\_tax at tax.name ÷ total\_valuation\_amount)).
        - Update amount\_including\_divisional\_loss using − applicable\_amount.
      - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = account, cost\_center = tax.cost\_center, debit = 0.0, …).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.remarks → translated “Accounting Entry for Stock”.
      - Update i using + 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1028) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L525)

<a id="op-839fb731569a7e"></a>
### Purchase Receipt.update assets

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_update_assets`

**Inputs** self, item, valuation\_rate.

**Record and data access** read “Asset” via get\_all.

**State and service calls** request set\_value on “Asset”.

**Local steps**

- Set assets from Platform.db.get\_all(“Asset”, filters = mapping(“purchase\_receipt” → self.name, “item\_code” → item.item\_code, “purchase\_receipt\_item” → tuple(“in”, list(item.name, empty text))), fields = list(“name”, “asse ….
- For each asset in assets.
  - Set purchase\_amount from ((flt(valuation\_rate) × flt((item.conversion\_factor or 1))) × asset.asset\_quantity).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.
  - Evaluate Platform.db.set\_value(“Asset”, asset.name, mapping(“net\_purchase\_amount” → purchase\_amount, “purchase\_amount” → purchase\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L204)

<a id="op-35252d5728ad6e"></a>
### Purchase Receipt.update status

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_update_status`

**Inputs** self, status.

**Local steps**

- Evaluate self.set\_status(update = true, status = status).
- Evaluate self.notify\_update().
- Evaluate clear\_doctype\_notifications(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L207)
