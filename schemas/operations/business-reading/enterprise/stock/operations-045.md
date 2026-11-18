# Inventory and warehouses · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase receipt

[Record definition](../../../../data/record-types/purchase_receipt.json)

<a id="op-0b88afb7b5cf84"></a>
### Purchase Receipt.update billing status

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_update_billing_status`

**Inputs** self, update\_modified = true.

**State and service calls** call db\_set on d.

**Local steps**

- Set updated\_pr from list(self.name).
- Set po\_details from list().
- For each d in self.get(“items”).
  - If (d.get(“purchase\_invoice”) and d.get(“purchase\_invoice\_item”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“purchase\_invoice”) → d.get(“purchase\_invoice\_item”).
    - Evaluate d.db\_set(“billed\_amt”, d.amount, update\_modified = update\_modified).
  - Otherwise.
    - If d.purchase\_order\_item.
      - Evaluate po\_details.append(d.purchase\_order\_item).
- If po\_details.
  - Update updated\_pr using + update\_billed\_amount\_based\_on\_po(po\_details, update\_modified, self).
- For each pr in set(updated\_pr).
  - Set pr\_doc from self when pr equals self.name, otherwise Platform.get\_lazy\_doc(“Purchase Receipt”, pr).
    - Value choice on pr equals self.name — true gives self, false gives Platform.get\_lazy\_doc(“Purchase Receipt”, pr).
  - Evaluate update\_billing\_percentage(pr\_doc, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L205)

<a id="op-05df8401f23bf6"></a>
### Purchase Receipt.reserve stock

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_reserve_stock`

**Inputs** self.

**Local steps**

- Evaluate self.reserve\_stock\_for\_sales\_order().
- Evaluate self.reserve\_stock\_for\_production\_plan().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reserve stock for sales order](operations-045.md#op-2434a0cb1aa93e), [reserve stock for production plan](operations-045.md#op-c1bf4d00fa6f7b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1029) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L526)

<a id="op-2434a0cb1aa93e"></a>
### Purchase Receipt.reserve stock for sales order

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_reserve_stock_for_sales_order`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Cannot create Stock Reservation Entries for future dated Purchase Receipts.”.

**Explicit results** no value · Platform.msgprint(translated “Cannot create Stock Reservation Entries for future dated Purchase Receipts.”).

**Local steps**

- If (self.is\_return or not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”) or not Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock\_for\_sales\_order\_on\_purchase”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”) → not Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock\_for\_sales\_order\_on\_purchase”).
  - Return no value.
- Evaluate self.reload().
- Set so\_items\_details\_map from mapping().
- For each item in self.items.
  - If (item.sales\_order and item.sales\_order\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.sales\_order → item.sales\_order\_item.
    - Set item\_details from mapping(“sales\_order\_item” → item.sales\_order\_item, “item\_code” → item.item\_code, “warehouse” → item.warehouse, “qty\_to\_reserve” → item.stock\_qty, …).
    - Evaluate so\_items\_details\_map.setdefault(item.sales\_order, list()).append(item\_details).
- If so\_items\_details\_map.
  - If get\_datetime(formatted text {self.posting\_date} {self.posting\_time}) &gt; get\_datetime().
    - Return Platform.msgprint(translated “Cannot create Stock Reservation Entries for future dated Purchase Receipts.”).
  - For each tuple(so, items\_details) in so\_items\_details\_map.items().
    - Set so\_doc from Platform.get\_lazy\_doc(“Sales Order”, so).
    - Evaluate so\_doc.\_create\_stock\_reservation\_entries(items\_details = items\_details, from\_voucher\_type = “Purchase Receipt”, notify = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”), Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock\_for\_sales\_order\_on\_purchase”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1031) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L528)

<a id="op-c1bf4d00fa6f7b"></a>
### Purchase Receipt.reserve stock for production plan

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_reserve_stock_for_production_plan`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If (self.is\_return or not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Return no value.
- Set production\_plan\_references from self.get\_production\_plan\_references().
- If not production\_plan\_references.
  - Return no value.
- Set reservable\_plans from self.get\_reservable\_production\_plans(production\_plan\_references).
- If not reservable\_plans.
  - Return no value.
- Set production\_plan\_items from list().
- Evaluate self.reload().
- Set unreserved\_qty from self.get\_unreserved\_qty\_for\_production\_plans(reservable\_plans).
- Set docnames from list().
- For each row in self.items.
  - If (row.material\_request\_item and row.material\_request\_item belongs to production\_plan\_references).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.material\_request\_item → row.material\_request\_item belongs to production\_plan\_references.
    - Set \_ref from production\_plan\_references at row.material\_request\_item.
    - If \_ref.production\_plan does not belong to reservable\_plans.
      - Continue with the next iteration or loop test.
    - Set key from tuple(\_ref.production\_plan, row.item\_code).
    - Set qty\_to\_reserve from flt(min(row.stock\_qty, unreserved\_qty at key), row.precision(“stock\_qty”)).
    - <a id="op-c1bf4d00fa6f7b-guard-26"></a>If qty\_to\_reserve ≤ 0.
      - Continue with the next iteration or loop test.
    - Update unreserved\_qty at key using − qty\_to\_reserve.
    - Evaluate docnames.append(\_ref.production\_plan).
    - Set item from row.as\_dict().
    - Evaluate item.update(mapping(“stock\_qty” → qty\_to\_reserve, “voucher\_type” → “Production Plan”, “voucher\_no” → \_ref.production\_plan, “voucher\_detail\_no” → \_ref.material\_request\_plan\_item, …)).
    - Evaluate production\_plan\_items.append(item).
- If not production\_plan\_items.
  - Return no value.
- Set sre from StockReservation(doc = self, items = production\_plan\_items).
- Evaluate sre.make\_stock\_reservation\_entries().
- If docnames.
  - Evaluate sre.transfer\_reservation\_entries\_to(docnames, from\_doctype = “Production Plan”, to\_doctype = “Work Order”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty\_to\_reserve ≤ 0, qty\_to\_reserve = 0 selects the branch that continues with the next loop iteration. With qty\_to\_reserve = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c1bf4d00fa6f7b-guard-26)

**Methods declared on this owner** [get production plan references](operations-045.md#op-79c2ca047bb38f), [get reservable production plans](operations-045.md#op-c233e2b8f203d0), [get unreserved qty for production plans](operations-045.md#op-fbd2a8289874ee).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1030) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L527)

<a id="op-fbd2a8289874ee"></a>
### Purchase Receipt.get unreserved qty for production plans

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_get_unreserved_qty_for_production_plans`

**Inputs** self, plans.

**Declared result** defaultdict.

**Explicit results** unreserved\_qty.

**Local steps**

- Set unreserved\_qty from defaultdict(float).
- Set mr\_item from Platform.qb.DocType(“Material Request Plan Item”).
- Set required from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(nested operand in the contract(neste ….run().
- For each tuple(plan, item\_code, qty) in required.
  - Update unreserved\_qty at tuple(plan, item\_code) using + flt(qty).
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set reserved from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….run().
- For each tuple(plan, item\_code, qty) in reserved.
  - Update unreserved\_qty at tuple(plan, item\_code) using − flt(qty).
- Return unreserved\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1016) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L513)

<a id="op-c233e2b8f203d0"></a>
### Purchase Receipt.get reservable production plans

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_get_reservable_production_plans`

**Inputs** self, production\_plan\_references.

**Declared result** set.

**Record and data access** read “Production Plan” via get\_all.

**Explicit results** set of p.name for p drawn from Platform.get\_all(“Production Plan”, filters = mapping(“name” → list(“in”, list(plan\_names))), fields = list(“name”, “reserve\_stock”)) where p.reserve\_stock.

**Local steps**

- Set plan\_names from set of ref.production\_plan for ref drawn from production\_plan\_references.values().
  - Draw ref from production\_plan\_references.values().
- Return set of p.name for p drawn from Platform.get\_all(“Production Plan”, filters = mapping(“name” → list(“in”, list(plan\_names))), fields = list(“name”, “reserve\_stock”)) where p.reserve\_stock.
  - Draw p from Platform.get\_all(“Production Plan”, filters = mapping(“name” → list(“in”, list(plan\_names))), fields = list(“name”, “reserve\_stock”)), keep a combination only if (p.reserve\_stock).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1014) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L511)

<a id="op-79c2ca047bb38f"></a>
### Purchase Receipt.get production plan references

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_get_production_plan_references`

**Inputs** self.

**Record and data access** read “Material Request Item” via get\_all.

**Explicit results** Platform.\_dict() · production\_plan\_references.

**Local steps**

- Set production\_plan\_references from Platform.\_dict().
- Set material\_request\_items from list().
- For each row in self.items.
  - If row.material\_request\_item.
    - Evaluate material\_request\_items.append(row.material\_request\_item).
- If not material\_request\_items.
  - Return Platform.\_dict().
- Set items from Platform.get\_all(“Material Request Item”, fields = list(“material\_request\_plan\_item”, “production\_plan”, “name”), filters = mapping(“name” → list(“in”, material\_request\_items), “docstatus” → 1)).
- For each item in items.
  - If not item.production\_plan.
    - Continue with the next iteration or loop test.
  - Evaluate production\_plan\_references.setdefault(item.name, item).
- Return production\_plan\_references.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1013) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L510)

<a id="op-ec38c5ca9e0b86"></a>
### Purchase Receipt.enable recalculate rate in sles

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_enable_recalculate_rate_in_stock_ledger_entries`

**Inputs** self.

**Record and data access** read “Purchase Receipt Item” via get\_all.

**Local steps**

- Set rejected\_warehouses from Platform.get\_all(“Purchase Receipt Item”, filters = mapping(“parent” → self.name), pluck = “rejected\_warehouse”).
- Set sle\_table from Platform.qb.DocType(“Stock Ledger Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.voucher\_type equals “Purchase Receipt”).where(sle\_table.warehouse.notin(rejected\_warehouses)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0775.json#L2096) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L194)

<a id="op-1ca0606d7a9b7c"></a>
### Get stock value difference

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_get_stock_value_difference`

**Inputs** voucher\_no, voucher\_detail\_no, warehouse.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** flt(Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_type” → “Purchase Receipt”, “voucher\_no” → voucher\_no, “voucher\_detail\_no” → voucher\_detail\_no, “warehouse” → warehouse, …), list(mapping(“SUM”  …).

**Local steps**

- Return flt(Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_type” → “Purchase Receipt”, “voucher\_no” → voucher\_no, “voucher\_detail\_no” → voucher\_detail\_no, “warehouse” → warehouse, …), list(mapping(“SUM”  …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L189)

<a id="op-ff4f96cf4f90a6"></a>
### Update billed amount based on po

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_update_billed_amount_based_on_po`

**Inputs** po\_details, update\_modified = true, pr\_doc = no value.

**State and service calls** call db\_set on pr\_item · request set\_value on “Purchase Receipt Item”.

**Explicit results** updated\_pr.

**Local steps**

- Set po\_billed\_amt\_details from get\_billed\_amount\_against\_po(po\_details).
- Set pr\_details from get\_purchase\_receipts\_against\_po\_details(po\_details).
- Set pr\_items from list of pr\_detail.name for pr\_detail drawn from pr\_details.
  - Draw pr\_detail from pr\_details.
- Set pr\_items\_billed\_amount from get\_billed\_amount\_against\_pr(pr\_items).
- Evaluate set\_qty\_and\_amount\_net\_of\_returns(pr\_details).
- Set updated\_pr from list().
- For each pr\_item in pr\_details.
  - Set tuple(billed\_amt\_against\_po, billed\_qty\_against\_po) from tuple(0, 0).
  - If billed\_details bound to po\_billed\_amt\_details.get(pr\_item.purchase\_order\_item).
    - Set billed\_amt\_against\_po from flt(billed\_details at “billed\_amt”).
    - Set billed\_qty\_against\_po from flt(billed\_details at “billed\_qty”).
  - Set billed\_amt\_against\_pr from flt(pr\_items\_billed\_amount.get(pr\_item.name, 0)).
  - If (billed\_amt\_against\_po and billed\_amt\_against\_pr &lt; pr\_item.net\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in billed\_amt\_against\_po → billed\_amt\_against\_pr &lt; pr\_item.net\_amount.
    - If (not billed\_amt\_against\_pr and billed\_qty\_against\_po and billed\_qty\_against\_po &gt; pr\_item.net\_qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not billed\_amt\_against\_pr → billed\_qty\_against\_po → billed\_qty\_against\_po &gt; pr\_item.net\_qty.
      - Set billed\_amt\_against\_pr from (flt((flt(billed\_amt\_against\_po) × flt(pr\_item.net\_qty))) ÷ flt(billed\_qty\_against\_po)).
      - Set po\_billed\_amt\_details at pr\_item.purchase\_order\_item at “billed\_amt” from (billed\_amt\_against\_po − billed\_amt\_against\_pr).
      - Set po\_billed\_amt\_details at pr\_item.purchase\_order\_item at “billed\_qty” from (billed\_qty\_against\_po − pr\_item.net\_qty).
    - Otherwise.
      - Set pending\_to\_bill from (flt(pr\_item.net\_amount) − billed\_amt\_against\_pr).
      - Set consumed\_amt\_against\_po from min(pending\_to\_bill, billed\_amt\_against\_po).
      - Update billed\_amt\_against\_pr using + consumed\_amt\_against\_po.
      - Set po\_billed\_amt\_details at pr\_item.purchase\_order\_item at “billed\_amt” from (billed\_amt\_against\_po − consumed\_amt\_against\_po).
      - Set po\_billed\_amt\_details at pr\_item.purchase\_order\_item at “billed\_qty” from (billed\_qty\_against\_po × (1 − (consumed\_amt\_against\_po ÷ billed\_amt\_against\_po))).
  - If pr\_item.billed\_amt differs from billed\_amt\_against\_pr.
    - If (pr\_doc and pr\_item.parent equals pr\_doc.name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pr\_doc → pr\_item.parent equals pr\_doc.name.
      - Set pr\_item from next(generator of item for item drawn from pr\_doc.items where item.name equals pr\_item.name, no value).
        - Draw item from pr\_doc.items, keep a combination only if (item.name equals pr\_item.name).
      - Evaluate pr\_item.db\_set(“billed\_amt”, billed\_amt\_against\_pr, update\_modified = update\_modified).
    - Otherwise.
      - Evaluate Platform.db.set\_value(“Purchase Receipt Item”, pr\_item.name, “billed\_amt”, billed\_amt\_against\_pr, update\_modified = update\_modified).
    - Evaluate updated\_pr.append(pr\_item.parent).
- Return updated\_pr.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1036) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L533)

<a id="op-f101345e1db642"></a>
### Set qty and amount net of returns

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_set_qty_and_amount_net_of_returns`

**Inputs** pr\_details.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- Set returned\_qty\_map from mapping().
- If not Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”).
  - Set returned\_qty\_map from get\_returned\_qty\_of\_rows(list of pr\_detail.name for pr\_detail drawn from pr\_details).
    - Draw pr\_detail from pr\_details.
- For each pr\_detail in pr\_details.
  - Set returned\_qty from flt(returned\_qty\_map.get(pr\_detail.name)).
  - Set pr\_detail.net\_qty from (flt(pr\_detail.qty) − returned\_qty).
  - Set pr\_detail.net\_amount from (flt(pr\_detail.amount) − (returned\_qty × flt(pr\_detail.rate))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1035) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L532)

<a id="op-defb5467a38d7d"></a>
### Get purchase receipts against po details

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_purchase_receipts_against_po_details`

**Inputs** po\_details.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set purchase\_receipt from Platform.qb.DocType(“Purchase Receipt”).
- Set purchase\_receipt\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L989) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L486)

<a id="op-c53d8ae6f68d45"></a>
### Get billed amount against pr

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_billed_amount_against_pr`

**Inputs** pr\_items.

**Explicit results** mapping() · mapping of d.pr\_detail → flt(d.billed\_amt) for d drawn from query.

**Local steps**

- If not pr\_items.
  - Return mapping().
- Set purchase\_invoice\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contra ….
- Return mapping of d.pr\_detail → flt(d.billed\_amt) for d drawn from query.
  - Draw d from query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L976) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L473)

<a id="op-be1159790ed62b"></a>
### Get billed amount against po

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_billed_amount_against_po`

**Inputs** po\_items.

**Explicit results** mapping() · mapping of d.po\_detail → mapping(“billed\_amt” → flt(d.billed\_amt), “billed\_qty” → flt(d.qty)) for d drawn from query.

**Local steps**

- If not po\_items.
  - Return mapping().
- Set purchase\_invoice from Platform.qb.DocType(“Purchase Invoice”).
- Set purchase\_invoice\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- Return mapping of d.po\_detail → mapping(“billed\_amt” → flt(d.billed\_amt), “billed\_qty” → flt(d.qty)) for d drawn from query.
  - Draw d from query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L472)

<a id="op-1be82dd2ecc6cf"></a>
### Update billing percentage

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_update_billing_percentage`

**Inputs** pr\_doc, update\_modified = true, adjust\_incoming\_rate = false.

**Record and data access** read “Buying Settings” via get\_single · read “Accounts Settings” via get\_single\_value.

**State and service calls** call db\_set on item · call db\_set on pr\_doc.

**Explicit failure paths** validation helper — translated “Over Billing Allowance exceeded for Purchase Receipt Item {0} ({1}) by {2}%”.format(item.name, Platform.bold(item.item\_code), flt((per\_over\_billed − over\_billing\_allowance), 2)).

**Local steps**

- Set buying\_settings from Platform.get\_single(“Buying Settings”).
- Set tuple(over\_billing\_allowance, role\_allowed\_to\_over\_bill) from Platform.get\_single\_value(“Accounts Settings”, list(“over\_billing\_allowance”, “role\_allowed\_to\_over\_bill”)).
- Set tuple(total\_amount, total\_billed\_amount, pi\_landed\_cost\_amount) from tuple(0, 0, 0).
- Set item\_wise\_returned\_qty from get\_item\_wise\_returned\_qty(pr\_doc).
- Set billed\_qty\_amt from Platform.\_dict().
- If adjust\_incoming\_rate.
  - Set billed\_qty\_amt from get\_billed\_qty\_amount\_against\_purchase\_receipt(pr\_doc).
  - Set billed\_qty\_amt\_based\_on\_po from get\_billed\_qty\_amount\_against\_purchase\_order(pr\_doc).
- For each item in pr\_doc.items.
  - Set returned\_qty from flt(item\_wise\_returned\_qty.get(item.name)).
  - Set returned\_amount from (flt(returned\_qty) × flt(item.rate)).
  - Set pending\_amount from (flt(item.amount) − returned\_amount).
  - Set rejected\_amount from 0.0.
  - If buying\_settings.bill\_for\_rejected\_quantity\_in\_purchase\_invoice.
    - Set rejected\_amount from flt((item.rejected\_qty × item.rate), item.precision(“amount”)).
    - Set pending\_amount from (flt(item.amount) + rejected\_amount).
  - Set total\_billable\_amount from abs((flt(item.amount) + rejected\_amount)).
  - If pending\_amount &gt; 0.
    - Set total\_billable\_amount from pending\_amount when item.billed\_amt ≤ pending\_amount, otherwise item.billed\_amt.
      - Value choice on item.billed\_amt ≤ pending\_amount — true gives pending\_amount, false gives item.billed\_amt.
  - Update total\_amount using + total\_billable\_amount.
  - Update total\_billed\_amount using + abs(flt(item.billed\_amt)).
  - If (pr\_doc.get(“is\_return”) and not total\_amount and total\_billed\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pr\_doc.get(“is\_return”) → not total\_amount → total\_billed\_amount.
    - Set total\_amount from total\_billed\_amount.
  - Set amount from (flt(item.amount) + rejected\_amount).
  - If adjust\_incoming\_rate.
    - Set adjusted\_amt from 0.0.
    - If (item.billed\_amt is distinct from no value and item.amount is distinct from no value and (billed\_qty\_amt.get(item.name) or billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.billed\_amt is distinct from no value → item.amount is distinct from no value → (billed\_qty\_amt.get(item.name) or billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in billed\_qty\_amt.get(item.name) → billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item).
      - Set qty from no value.
      - If billed\_qty\_amt.get(item.name).
        - Set qty from billed\_qty\_amt.get(item.name).get(“qty”).
      - If (not qty and billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not qty → billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item).
        - If item.qty &lt; billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item) at “qty”.
          - Set qty from item.qty.
        - Otherwise.
          - Set qty from billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item) at “qty”.
        - Update billed\_qty\_amt\_based\_on\_po at item.purchase\_order\_item at “qty” using − qty.
      - Set billed\_amt from item.billed\_amt.
      - If billed\_qty\_amt.get(item.name).
        - Set billed\_amt from flt(billed\_qty\_amt.get(item.name).get(“amount”)).
      - Otherwise.
        - If billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item).
          - Set total\_billed\_qty from (billed\_qty\_amt\_based\_on\_po.get(item.purchase\_order\_item).get(“qty”) + qty).
          - If total\_billed\_qty.
            - Set billed\_amt from flt((flt(nested operand in the contract.get(nested operand in the contract.purchase\_order\_item).get(“amount”)) × (qty ÷ total\_billed\_qty))).
          - Otherwise.
            - Set billed\_amt from 0.0.
          - Update billed\_qty\_amt\_based\_on\_po at item.purchase\_order\_item at “amount” using − billed\_amt.
      - If qty.
        - Set adjusted\_amt from ((flt((billed\_amt ÷ qty)) × item.qty) − flt(item.base\_net\_amount)).
    - Set adjusted\_amt from flt(adjusted\_amt, item.precision(“amount”)).
    - Update pi\_landed\_cost\_amount using + adjusted\_amt.
    - Evaluate item.db\_set(“amount\_difference\_with\_purchase\_invoice”, adjusted\_amt, update\_modified = false).
  - Otherwise.
    - If (amount and item.billed\_amt &gt; amount).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in amount → item.billed\_amt &gt; amount.
      - Set per\_over\_billed from flt((((item.billed\_amt ÷ amount) × 100) − 100), 2).
      - If (per\_over\_billed &gt; over\_billing\_allowance and role\_allowed\_to\_over\_bill does not belong to Platform.get\_roles()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in per\_over\_billed &gt; over\_billing\_allowance → role\_allowed\_to\_over\_bill does not belong to Platform.get\_roles().
        - Call the validation error handler Platform.throw(translated “Over Billing Allowance exceeded for Purchase Receipt Item {0} ({1}) by {2}%”.format(item.name, Platform.bold(item.item\_code), flt((per\_over\_billed − over\_billing\_allowance), 2))).
- If pi\_landed\_cost\_amount &lt; 0.
  - Update total\_billed\_amount using + abs(pi\_landed\_cost\_amount).
- Set percent\_billed from round((100 × (total\_billed\_amount ÷ (total\_amount or 1))), 6).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in total\_amount → 1.
- Evaluate pr\_doc.db\_set(“per\_billed”, percent\_billed).
- If update\_modified.
  - Evaluate pr\_doc.set\_status(update = true).
  - Evaluate pr\_doc.notify\_update().
- If adjust\_incoming\_rate.
  - Evaluate adjust\_incoming\_rate\_for\_pr(pr\_doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, list(“over\_billing\_allowance”, “role\_allowed\_to\_over\_bill”)) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1037) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L534)

<a id="op-a527ded7a951bf"></a>
### Get billed qty amount against purchase receipt

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_billed_qty_amount_against_purchase_receipt`

**Inputs** pr\_doc.

**Explicit results** Platform.\_dict() · billed\_qty\_amt.

**Local steps**

- Set pr\_names from list of d.name for d drawn from pr\_doc.items.
  - Draw d from pr\_doc.items.
- Set parent\_table from Platform.qb.DocType(“Purchase Invoice”).
- Set table from Platform.qb.DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(table.pr\_detail, nested operand in the contract.as\_(“amount”), nested operand in the contract.as\_(“qty”)).where((nested operand in the  ….
- Set invoice\_data from query.run(as\_dict = 1).
- If not invoice\_data.
  - Return Platform.\_dict().
- Set billed\_qty\_amt from Platform.\_dict().
- For each row in invoice\_data.
  - If row.pr\_detail does not belong to billed\_qty\_amt.
    - Set billed\_qty\_amt at row.pr\_detail from mapping(“amount” → 0, “qty” → 0).
  - Update billed\_qty\_amt at row.pr\_detail at “amount” using + flt(row.amount).
  - Update billed\_qty\_amt at row.pr\_detail at “qty” using + flt(row.qty).
- Return billed\_qty\_amt.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L475)

<a id="op-48549843cfee53"></a>
### Get billed qty amount against purchase order

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_billed_qty_amount_against_purchase_order`

**Inputs** pr\_doc.

**Explicit results** Platform.\_dict() · invoice\_data\_po\_based.

**Local steps**

- Set po\_names from list(set(list of d.purchase\_order\_item for d drawn from pr\_doc.items where (d.purchase\_order\_item and not d.purchase\_invoice\_item))).
  - Draw d from pr\_doc.items, keep a combination only if ((d.purchase\_order\_item and not d.purchase\_invoice\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.purchase\_order\_item → not d.purchase\_invoice\_item.
- Set invoice\_data\_po\_based from Platform.\_dict().
- If po\_names.
  - Set parent\_table from Platform.qb.DocType(“Purchase Invoice”).
  - Set table from Platform.qb.DocType(“Purchase Invoice Item”).
  - Set query from nested operand in the contract(nested operand in the contract).select(table.po\_detail, nested operand in the contract.as\_(“qty”), nested operand in the contract.as\_(“amount”)).where(((nested operand in the ….
  - Set invoice\_data from query.run(as\_dict = 1).
  - If not invoice\_data.
    - Return Platform.\_dict().
  - For each row in invoice\_data.
    - If row.po\_detail does not belong to invoice\_data\_po\_based.
      - Set invoice\_data\_po\_based at row.po\_detail from mapping(“amount” → 0, “qty” → 0).
    - Update invoice\_data\_po\_based at row.po\_detail at “amount” using + flt(row.amount).
    - Update invoice\_data\_po\_based at row.po\_detail at “qty” using + flt(row.qty).
- Return invoice\_data\_po\_based.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L474)

<a id="op-0c63b8866fd64c"></a>
### Adjust incoming rate for pr

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_adjust_incoming_rate_for_pr`

**Inputs** doc.

**State and service calls** call db\_update on item.

**Local steps**

- Evaluate doc.update\_valuation\_rate(reset\_outgoing\_rate = false).
- For each item in doc.get(“items”).
  - Evaluate item.db\_update().
- If doc.doctype equals “Purchase Receipt”.
  - Evaluate doc.enable\_recalculate\_rate\_in\_sles().
- Evaluate doc.repost\_future\_sle\_and\_gle(force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L973) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L470)

<a id="op-5d19fe6050f590"></a>
### Get item wise returned qty

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_item_wise_returned_qty`

**Inputs** pr\_doc.

**Explicit results** get\_returned\_qty\_of\_rows(list of d.name for d drawn from pr\_doc.items).

**Local steps**

- Return get\_returned\_qty\_of\_rows(list of d.name for d drawn from pr\_doc.items).
  - Draw d from pr\_doc.items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L981) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L478)

<a id="op-ea0d2aab28f280"></a>
### Get returned qty of rows

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_returned_qty_of_rows`

**Inputs** items.

**Record and data access** read “Purchase Receipt” via get\_all.

**Explicit results** Platform.\_dict() · Platform.\_dict(Platform.get\_all(“Purchase Receipt”, fields = list(“′tabPurchase Receipt Item′.purchase\_receipt\_item”, mapping(“SUM” → list(mapping(“ABS” → “′tabPurchase Receipt Item′.qty”)), “as” → “qty”)) ….

**Local steps**

- If not items.
  - Return Platform.\_dict().
- Return Platform.\_dict(Platform.get\_all(“Purchase Receipt”, fields = list(“′tabPurchase Receipt Item′.purchase\_receipt\_item”, mapping(“SUM” → list(mapping(“ABS” → “′tabPurchase Receipt Item′.qty”)), “as” → “qty”)) ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L491)

<a id="op-d72d6a904e0c48"></a>
### Make purchase invoice

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_purchase_invoice`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Purchase Receipt” via get\_doc.

**Explicit results** doclist.

**Explicit failure paths** validation helper — translated “Purchase Receipt {0} is closed and cannot be invoiced”.format(Platform.bold(doc.name)).

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Bind dependencies get\_payment\_terms\_template.
- Set doc from Platform.get\_doc(“Purchase Receipt”, source\_name).
- If doc.status equals “Closed”.
  - Call the validation error handler Platform.throw(translated “Purchase Receipt {0} is closed and cannot be invoiced”.format(Platform.bold(doc.name))).
- Set returned\_qty\_map from get\_returned\_qty\_map(source\_name).
- Set invoiced\_qty\_map from get\_invoiced\_qty\_map(source\_name).
- For each tuple(ref, qty) in get\_qty\_already\_mapped(target\_doc, “pr\_detail”).items().
  - Set invoiced\_qty\_map at ref from (invoiced\_qty\_map.get(ref, 0) + qty).
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation get\_pending\_qty for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Purchase Receipt”, source\_name, mapping(“Purchase Receipt” → mapping(“doctype” → “Purchase Invoice”, “field\_map” → mapping(“supplier\_warehouse” → “supplier\_warehouse”, “is\_return” → “is\_ret ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args → args.get(“merge\_taxes”).
  - Value choice on args — true gives args.get(“merge\_taxes”), false gives 0.
- Return doclist.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1001) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L498)

<a id="op-18887831280d3a"></a>
### Make purchase invoice.set missing values

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_purchase_invoice_set_missing_values`

**Inputs** source, target.

**Record and data access** resolve a document from target via get\_doc.

**Explicit failure paths** validation helper — translated “All items have already been Invoiced/Returned”.

**Local steps**

- <a id="op-18887831280d3a-guard-2"></a>If len(target.get(“items”)) equals 0.
  - Call the validation error handler Platform.throw(translated “All items have already been Invoiced/Returned”).
- Set doc from Platform.get\_doc(target).
- Set doc.payment\_terms\_template from get\_payment\_terms\_template(source.supplier, “Supplier”, source.company).
- Evaluate doc.run\_method(“onload”).
- Evaluate doc.run\_method(“set\_missing\_values”).
- If (args and args.get(“merge\_taxes”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args → args.get(“merge\_taxes”).
  - Evaluate merge\_taxes(source, doc).
- Evaluate doc.run\_method(“calculate\_taxes\_and\_totals”).
- Evaluate doc.set\_payment\_schedule().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(target.get(“items”)) equals 0, length of target.items = 0 selects the branch that calls the validation-error handler with translated “All items have already been Invoiced/Returned”. With length of target.items = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-18887831280d3a-guard-2)

**Values supplied outside this operation** selected callable from doc.run\_method(“onload”), doc.run\_method(“set\_missing\_values”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1004) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L501)

<a id="op-9a578414e11fae"></a>
### Make purchase invoice.update item

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_purchase_invoice_update_item`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Set tuple(target\_doc.qty, returned\_qty) from get\_pending\_qty(source\_doc).
- Set target\_doc.rejected\_qty from 0.
- Set target\_doc.stock\_qty from (flt(target\_doc.qty) × flt(target\_doc.conversion\_factor, target\_doc.precision(“conversion\_factor”))).
- Set returned\_qty\_map at source\_doc.name from returned\_qty.
- Set target\_doc.\_old\_name from source\_doc.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1005) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L502)

<a id="op-a1881ac03f80c9"></a>
### Make purchase invoice.get pending qty

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_make_purchase_invoice_get_pending_qty`

**Inputs** item\_row.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** tuple(pending\_qty, 0) · tuple(pending\_qty, returned\_qty).

**Local steps**

- Set qty from item\_row.qty.
- If Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”).
  - Set qty from item\_row.received\_qty.
- Set pending\_qty from (qty − invoiced\_qty\_map.get(item\_row.name, 0)).
- If Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”).
  - Return tuple(pending\_qty, 0).
- Set returned\_qty from flt(returned\_qty\_map.get(item\_row.name, 0)).
- If returned\_qty.
  - If returned\_qty ≥ pending\_qty.
    - Set pending\_qty from 0.
    - Update returned\_qty using − pending\_qty.
  - Otherwise.
    - Update pending\_qty using − returned\_qty.
    - Set returned\_qty from 0.
- Return tuple(pending\_qty, returned\_qty).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1002) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L499)
