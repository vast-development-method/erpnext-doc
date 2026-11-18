# Shared transaction rules · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Selling controller

<a id="op-54005c77ee891f"></a>
### Selling Controller.fetch product bundle items

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_fetch_product_bundle_items`

**Inputs** self, item\_code.

**Record and data access** read “Product Bundle” via get\_all.

**Local steps**

- Set product\_bundle\_items from self.\_product\_bundle\_items.
- Set items\_to\_fetch from set of row.item\_code for row drawn from self.items where row.item\_code does not belong to product\_bundle\_items.
  - Draw row from self.items, keep a combination only if (row.item\_code does not belong to product\_bundle\_items).
- Evaluate items\_to\_fetch.add(item\_code).
- Set items\_with\_product\_bundle from set of row.new\_item\_code for row drawn from Platform.get\_all(“Product Bundle”, filters = mapping(“new\_item\_code” → tuple(“in”, items\_to\_fetch), “disabled” → 0), fields = “new\_item\_code”).
  - Draw row from Platform.get\_all(“Product Bundle”, filters = mapping(“new\_item\_code” → tuple(“in”, items\_to\_fetch), “disabled” → 0), fields = “new\_item\_code”).
- For each item\_code in items\_to\_fetch.
  - Set product\_bundle\_items at item\_code from item\_code belongs to items\_with\_product\_bundle.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L874) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L555)

<a id="op-a158d527481a35"></a>
### Selling Controller.get already delivered qty

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_get_already_delivered_quantity`

**Inputs** self, current\_docname, so, so\_detail.

**Record and data access** execute query text (SELECT, Delivery Note Item) · execute query text (SELECT, Sales Invoice Item).

**Explicit results** total\_delivered\_qty.

**Local steps**

- Set delivered\_via\_dn from Platform.db.sql(query text (SELECT, Delivery Note Item), tuple(so\_detail, so, current\_docname)).
- Set delivered\_via\_si from Platform.db.sql(query text (SELECT, Sales Invoice Item), tuple(so\_detail, so, current\_docname)).
- Set total\_delivered\_qty from (flt(delivered\_via\_dn at 0 at 0) when delivered\_via\_dn, otherwise 0 + flt(delivered\_via\_si at 0 at 0) when delivered\_via\_si, otherwise 0).
  - Value choice on delivered\_via\_dn — true gives flt(delivered\_via\_dn at 0 at 0), false gives 0.
  - Value choice on delivered\_via\_si — true gives flt(delivered\_via\_si at 0 at 0), false gives 0.
- Return total\_delivered\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L875) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L556)

<a id="op-e51be19c99b7fc"></a>
### Selling Controller.get so qty and warehouse

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_get_sales_order_quantity_and_warehouse`

**Inputs** self, so\_detail.

**Record and data access** execute query text (SELECT, Sales).

**Explicit results** tuple(so\_qty, so\_warehouse).

**Local steps**

- Set so\_item from Platform.db.sql(query text (SELECT, Sales), so\_detail, as\_dict = 1).
- Set so\_qty from ((so\_item and flt(so\_item at 0 at “qty”)) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (so\_item and flt(so\_item at 0 at “qty”)) → 0.0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in so\_item → flt(so\_item at 0 at “qty”).
- Set so\_warehouse from ((so\_item and so\_item at 0 at “warehouse”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (so\_item and so\_item at 0 at “warehouse”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in so\_item → so\_item at 0 at “warehouse”.
- Return tuple(so\_qty, so\_warehouse).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L559)

<a id="op-6e2d05a614df44"></a>
### Selling Controller.ensure customer is not blocked

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_ensure_customer_is_not_blocked`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is blocked so this transaction cannot proceed”.format(self.customer).

**Local steps**

- If (self.doctype equals “Quotation” or self.get(“is\_consolidated”) or self.get(“is\_return”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Quotation” → self.get(“is\_consolidated”) → self.get(“is\_return”).
  - Return no value.
- If (self.customer and is\_customer\_blocked(self.customer)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.customer → is\_customer\_blocked(self.customer).
  - Call the validation error handler Platform.throw(translated “{0} is blocked so this transaction cannot proceed”.format(self.customer)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L344)

<a id="op-2198b85c071d42"></a>
### Selling Controller.check sales order on hold or close

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_check_sales_order_on_hold_or_close`

**Inputs** self, ref\_fieldname.

**Explicit results** no value.

**Local steps**

- If self.is\_return.
  - Return no value.
- Evaluate self.check\_for\_on\_hold\_or\_closed\_status(“Sales Order”, ref\_fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0387.json#L4570) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L873) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L554)

<a id="op-cc218e788f0cd5"></a>
### Selling Controller.update reserved qty

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_update_reserved_quantity`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “{0} {1} is cancelled or closed”.format(translated “Sales Order”, so).

**Local steps**

- Set so\_map from mapping().
- For each d in self.get(“items”).
  - If d.so\_detail.
    - If (self.doctype equals “Delivery Note” and d.against\_sales\_order).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Delivery Note” → d.against\_sales\_order.
      - Evaluate so\_map.setdefault(d.against\_sales\_order, list()).append(d.so\_detail).
    - Otherwise.
      - If (self.doctype equals “Sales Invoice” and d.sales\_order and self.update\_stock).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → d.sales\_order → self.update\_stock.
        - Evaluate so\_map.setdefault(d.sales\_order, list()).append(d.so\_detail).
- For each tuple(so, so\_item\_rows) in so\_map.items().
  - If (so and so\_item\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in so → so\_item\_rows.
    - Set sales\_order from Platform.get\_lazy\_doc(“Sales Order”, so).
    - If ((sales\_order.status equals “Closed” and not self.is\_return) or sales\_order.status belongs to list(“Cancelled”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (sales\_order.status equals “Closed” and not self.is\_return) → sales\_order.status belongs to list(“Cancelled”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_order.status equals “Closed” → not self.is\_return.
      - Call the validation error handler Platform.throw(translated “{0} {1} is cancelled or closed”.format(translated “Sales Order”, so), Platform.InvalidStatusError).
    - Evaluate sales\_order.update\_reserved\_qty(so\_item\_rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0387.json#L4660) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L581)

<a id="op-32a0507db69acd"></a>
### Selling Controller.set incoming rate

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_incoming_rate`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_cached\_value · read “Selling Settings” via get\_single\_value · read “Item” via get\_cached\_value.

**State and service calls** msgprint with translated “Row {0}: Item rate has been updated as per valuation rate since its an internal stock transfer”.format(d.idx).

**Explicit results** no value.

**Local steps**

- Bind local operation reset\_incoming\_rate for subsequent calls.
- Set is\_standalone from (self.get(“is\_return”) and not self.get(“return\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → not self.get(“return\_against”).
- If (self.doctype does not belong to tuple(“Delivery Note”, “Sales Invoice”) and not (self.doctype equals “POS Invoice” and is\_standalone)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype does not belong to tuple(“Delivery Note”, “Sales Invoice”) → not (self.doctype equals “POS Invoice” and is\_standalone).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “POS Invoice” → is\_standalone.
  - Return no value.
- If (self.doctype belongs to tuple(“Sales Invoice”, “POS Invoice”) and not self.update\_stock and not self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to tuple(“Sales Invoice”, “POS Invoice”) → not self.update\_stock → not self.is\_internal\_transfer().
  - Return no value.
- Bind dependencies get\_batch\_nos, get\_serial\_nos.
- Set allow\_at\_arms\_length\_price from Platform.get\_cached\_value(“Stock Settings”, no value, “allow\_internal\_transfer\_at\_arms\_length\_price”).
- Set set\_zero\_rate\_for\_expired\_batch from Platform.db.get\_single\_value(“Selling Settings”, “set\_zero\_rate\_for\_expired\_batch”).
- Set old\_doc from self.get\_doc\_before\_save().
- Set items from (self.get(“items”) + (self.get(“packed\_items”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“packed\_items”) → list().
- For each d in items.
  - If not Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”).
    - Continue with the next iteration or loop test.
  - Set item\_details from Platform.get\_cached\_value(“Item”, d.item\_code, list(“has\_serial\_no”, “has\_batch\_no”, “has\_expiry\_date”), as\_dict = 1).
  - If (set\_zero\_rate\_for\_expired\_batch and item\_details.has\_batch\_no and item\_details.has\_expiry\_date and self.get(“is\_return”) and not self.get(“return\_against”) and is\_batch\_expired(d.batch\_no, self.get(“posti ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in set\_zero\_rate\_for\_expired\_batch → item\_details.has\_batch\_no → item\_details.has\_expiry\_date → self.get(“is\_return”) → not self.get(“return\_against”) → is\_batch\_expired(d.batch\_no, self.get(“posting\_date”)).
    - Set d.incoming\_rate from 0.
  - Otherwise.
    - If (not self.get(“return\_against”) or (get\_valuation\_method(d.item\_code, self.company) equals “Moving Average” and self.get(“is\_return”) and not item\_details.has\_serial\_no and not item\_details.has\_batch\_no)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“return\_against”) → (get\_valuation\_method(d.item\_code, self.company) equals “Moving Average” and self.get(“is\_return”) and not item\_details.has\_serial\_no and not item\_details.has\_batch\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in get\_valuation\_method(d.item\_code, self.company) equals “Moving Average” → self.get(“is\_return”) → not item\_details.has\_serial\_no → not item\_details.has\_batch\_no.
      - Set qty from flt((d.get(“stock\_qty”) or d.get(“actual\_qty”) or d.get(“qty”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“stock\_qty”) → d.get(“actual\_qty”) → d.get(“qty”).
      - If old\_doc.
        - Evaluate reset\_incoming\_rate().
      - If (not d.incoming\_rate or (self.is\_new() and not is\_standalone) or self.is\_internal\_transfer() or (get\_valuation\_method(d.item\_code, self.company) equals “Moving Average” and self.get(“is\_return”) and not is ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.incoming\_rate → (self.is\_new() and not is\_standalone) → self.is\_internal\_transfer() → (get\_valuation\_method(d.item\_code, self.company) equals “Moving Average” and self.get(“is\_return”) and not is\_standalone).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not is\_standalone.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in get\_valuation\_method(d.item\_code, self.company) equals “Moving Average” → self.get(“is\_return”) → not is\_standalone.
        - Set d.incoming\_rate from \_get\_incoming\_rate(mapping(“item\_code” → d.item\_code, “warehouse” → d.warehouse, “posting\_date” → (self.get(“posting\_date”) or self.get(“transaction\_date”)), “posting\_time” → (self.get(“posting\_time”) or n ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“posting\_date”) → self.get(“transaction\_date”).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“posting\_time”) → nowtime().
          - Value choice on cint(self.get(“is\_return”)) — true gives qty, false gives (negative 1 × qty).
      - If (not d.incoming\_rate and self.get(“return\_against”) and self.get(“is\_return”) and get\_valuation\_method(d.item\_code, self.company) equals “Moving Average”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.incoming\_rate → self.get(“return\_against”) → self.get(“is\_return”) → get\_valuation\_method(d.item\_code, self.company) equals “Moving Average”.
        - Set d.incoming\_rate from get\_rate\_for\_return(self.doctype, self.name, d.item\_code, self.return\_against, item\_row = d).
      - If (self.get(“is\_return”) and not d.incoming\_rate and not self.get(“return\_against”) and not self.is\_internal\_transfer() and not d.get(“allow\_zero\_valuation\_rate”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → not d.incoming\_rate → not self.get(“return\_against”) → not self.is\_internal\_transfer() → not d.get(“allow\_zero\_valuation\_rate”).
        - Set d.incoming\_rate from d.rate.
      - If self.is\_internal\_transfer().
        - If (self.doctype equals “Delivery Note” or self.get(“update\_stock”)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Delivery Note” → self.get(“update\_stock”).
          - If d.doctype equals “Packed Item”.
            - Set incoming\_rate from flt((flt(d.incoming\_rate, d.precision(“incoming\_rate”)) × d.conversion\_factor), d.precision(“incoming\_rate”)).
            - If d.incoming\_rate differs from incoming\_rate.
              - Set d.incoming\_rate from incoming\_rate.
          - Otherwise.
            - If allow\_at\_arms\_length\_price.
              - Continue with the next iteration or loop test.
            - Set rate from flt((flt(d.incoming\_rate) × flt((d.conversion\_factor or 1.0)))).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.conversion\_factor → 1.0.
            - If flt(d.rate, d.precision(“incoming\_rate”)) differs from flt(rate, d.precision(“incoming\_rate”)).
              - Set d.rate from rate.
              - Evaluate Platform.msgprint(translated “Row {0}: Item rate has been updated as per valuation rate since its an internal stock transfer”.format(d.idx), alert = 1).
            - Set d.discount\_percentage from 0.0.
            - Set d.discount\_amount from 0.0.
            - Set d.margin\_rate\_or\_amount from 0.0.
    - Otherwise.
      - If self.get(“return\_against”).
        - Set d.incoming\_rate from get\_rate\_for\_return(self.doctype, self.name, d.item\_code, self.return\_against, item\_row = d).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Settings”, no value, “allow\_internal\_transfer\_at\_arms\_length\_price”), Platform.db.get\_single\_value(“Selling Settings”, “set\_zero\_rate\_for\_expired\_batch”) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L887) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L568)

<a id="op-5f82aba15aa391"></a>
### Selling Controller.set incoming rate.reset incoming rate

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_incoming_rate_reset_incoming_rate`

**Inputs** no declared parameters.

**Local steps**

- Set old\_item from next(generator of item for item drawn from (old\_doc.get(“items”) + (old\_doc.get(“packed\_items”) or list())) where item.name equals d.name, no value).
  - Draw item from (old\_doc.get(“items”) + (old\_doc.get(“packed\_items”) or list())), keep a combination only if (item.name equals d.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in old\_doc.get(“packed\_items”) → list().
- If old\_item.
  - Set old\_qty from flt((old\_item.get(“stock\_qty”) or old\_item.get(“actual\_qty”) or old\_item.get(“qty”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in old\_item.get(“stock\_qty”) → old\_item.get(“actual\_qty”) → old\_item.get(“qty”).
  - If (old\_item.item\_code differs from d.item\_code or old\_item.warehouse differs from d.warehouse or old\_qty differs from qty or old\_item.serial\_no differs from d.serial\_no or get\_serial\_nos(old\_item.serial\_and\_ ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in old\_item.item\_code differs from d.item\_code → old\_item.warehouse differs from d.warehouse → old\_qty differs from qty → old\_item.serial\_no differs from d.serial\_no → get\_serial\_nos(old\_item.serial\_and\_batch\_bundle) differs from get\_serial\_nos(d.serial\_and\_batch\_bundle) → old\_item.batch\_no differs from d.batch\_no → get\_batch\_nos(old\_item.serial\_and\_batch\_bundle) differs from get\_batch\_nos(d.serial\_and\_batch\_bundle).
    - Set d.incoming\_rate from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0388.json#L3067) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L888) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L569)

<a id="op-91c2f2ccccc099"></a>
### Selling Controller.update stock ledger

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_update_stock_ledger`

**Inputs** self, allow\_negative\_stock = false.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Evaluate self.update\_reserved\_qty().
- Evaluate self.make\_packed\_item\_bundles().
- Set sl\_entries from list().
- For each d in self.get\_item\_list().
  - If (Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”) equals 1 and flt(d.qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”) equals 1 → flt(d.qty).
    - If flt(d.conversion\_factor) equals 0.0.
      - Set d.conversion\_factor from (get\_conversion\_factor(d.item\_code, d.uom).get(“conversion\_factor”) or 1.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_conversion\_factor(d.item\_code, d.uom).get(“conversion\_factor”) → 1.0.
    - If (d.warehouse and ((not cint(self.is\_return) and self.docstatus equals 1) or (cint(self.is\_return) and self.docstatus equals 2))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.warehouse → ((not cint(self.is\_return) and self.docstatus equals 1) or (cint(self.is\_return) and self.docstatus equals 2)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not cint(self.is\_return) and self.docstatus equals 1) → (cint(self.is\_return) and self.docstatus equals 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.is\_return) → self.docstatus equals 1.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.docstatus equals 2.
      - Evaluate sl\_entries.append(self.get\_sle\_for\_source\_warehouse(d)).
    - If d.target\_warehouse.
      - Evaluate sl\_entries.append(self.get\_sle\_for\_target\_warehouse(d)).
    - If (d.warehouse and ((not cint(self.is\_return) and self.docstatus equals 2) or (cint(self.is\_return) and self.docstatus equals 1))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.warehouse → ((not cint(self.is\_return) and self.docstatus equals 2) or (cint(self.is\_return) and self.docstatus equals 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not cint(self.is\_return) and self.docstatus equals 2) → (cint(self.is\_return) and self.docstatus equals 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.is\_return) → self.docstatus equals 2.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.docstatus equals 1.
      - Evaluate sl\_entries.append(self.get\_sle\_for\_source\_warehouse(d)).
- Evaluate self.make\_sl\_entries(sl\_entries, allow\_negative\_stock = allow\_negative\_stock).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reserved qty](operations-021.md#op-cc218e788f0cd5), [make packed item bundles](operations-020.md#op-9a88f8932cc987), [get item list](operations-020.md#op-17458b31ca2d3b), [get sle for source warehouse](operations-021.md#op-9eb34e9b20a3d5), [get sle for target warehouse](operations-021.md#op-f1164d72a96a69).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L582)

<a id="op-9eb34e9b20a3d5"></a>
### Selling Controller.get sle for source warehouse

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_get_stock_ledger_entry_for_source_warehouse`

**Inputs** self, item\_row.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** sle.

**Local steps**

- Set serial\_and\_batch\_bundle from item\_row.serial\_and\_batch\_bundle when (not self.is\_internal\_transfer() or self.docstatus equals 1), otherwise no value.
  - Value choice on (not self.is\_internal\_transfer() or self.docstatus equals 1) — true gives item\_row.serial\_and\_batch\_bundle, false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_internal\_transfer() → self.docstatus equals 1.
- If self.is\_internal\_transfer().
  - If (serial\_and\_batch\_bundle and self.docstatus equals 1 and self.is\_return).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial\_and\_batch\_bundle → self.docstatus equals 1 → self.is\_return.
    - Set serial\_and\_batch\_bundle from self.make\_package\_for\_transfer(serial\_and\_batch\_bundle, item\_row.warehouse, type\_of\_transaction = “Inward”).
  - Otherwise.
    - If not serial\_and\_batch\_bundle.
      - Set serial\_and\_batch\_bundle from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → item\_row.name, “warehouse” → item\_row.warehouse), “serial\_and\_batch\_bundle”).
- Set sle from self.get\_sl\_entries(item\_row, mapping(“actual\_qty” → (negative 1 × get\_ledger\_qty(item\_row.qty)), “incoming\_rate” → item\_row.incoming\_rate, “recalculate\_rate” → cint(self.is\_return), “serial\_and\_batch\_bund ….
- If (item\_row.target\_warehouse and not cint(self.is\_return)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_row.target\_warehouse → not cint(self.is\_return).
  - Set sle.dependant\_sle\_voucher\_detail\_no from item\_row.name.
- Return sle.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L560)

<a id="op-f1164d72a96a69"></a>
### Selling Controller.get sle for target warehouse

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_get_stock_ledger_entry_for_target_warehouse`

**Inputs** self, item\_row.

**Explicit results** sle.

**Local steps**

- Set sle from self.get\_sl\_entries(item\_row, mapping(“actual\_qty” → get\_ledger\_qty(item\_row.qty), “warehouse” → item\_row.target\_warehouse)).
- If self.docstatus equals 1.
  - If not cint(self.is\_return).
    - Evaluate sle.update(mapping(“incoming\_rate” → item\_row.incoming\_rate, “recalculate\_rate” → 1)).
  - Otherwise.
    - Evaluate sle.update(mapping(“outgoing\_rate” → item\_row.incoming\_rate)).
    - If item\_row.warehouse.
      - Set sle.dependant\_sle\_voucher\_detail\_no from item\_row.name.
  - If (item\_row.serial\_and\_batch\_bundle and not cint(self.is\_return)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_row.serial\_and\_batch\_bundle → not cint(self.is\_return).
    - Set type\_of\_transaction from “Inward”.
    - If cint(self.is\_return).
      - Set type\_of\_transaction from “Outward”.
    - Set sle at “serial\_and\_batch\_bundle” from self.make\_package\_for\_transfer(item\_row.serial\_and\_batch\_bundle, item\_row.target\_warehouse, type\_of\_transaction = type\_of\_transaction).
- Return sle.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L880) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L561)

<a id="op-6a3eac4009bf7e"></a>
### Selling Controller.set po nos

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_purchase_order_numbers`

**Inputs** self, for\_validate = false.

**Explicit results** no value.

**Local steps**

- If (self.doctype equals “Sales Invoice” and hasattr(self, “items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → hasattr(self, “items”).
  - If (for\_validate and self.po\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → self.po\_no.
    - Return no value.
  - Evaluate self.set\_pos\_for\_sales\_invoice().
- If (self.doctype equals “Delivery Note” and hasattr(self, “items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Delivery Note” → hasattr(self, “items”).
  - If (for\_validate and self.po\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → self.po\_no.
    - Return no value.
  - Evaluate self.set\_pos\_for\_delivery\_note().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set pos for sales invoice](operations-021.md#op-8cf52be091b306), [set pos for delivery note](operations-021.md#op-44049fa1d57eab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0388.json#L5346) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L894) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L575)

<a id="op-8cf52be091b306"></a>
### Selling Controller.set pos for sales invoice

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_point_of_sale_for_sales_invoice`

**Inputs** self.

**Local steps**

- Set po\_nos from list().
- If self.po\_no.
  - Evaluate po\_nos.append(self.po\_no).
- Evaluate self.get\_po\_nos(“Sales Order”, “sales\_order”, po\_nos).
- Evaluate self.get\_po\_nos(“Delivery Note”, “delivery\_note”, po\_nos).
- Set self.po\_no from “, ”.join(list(set(generator of x.strip() for x drawn from nested operand in the contract(nested operand in the contract).split(“,”)))).
  - Draw x from “,”.join(po\_nos).split(“,”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get po nos](operations-021.md#op-77d4847c156581).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0388.json#L5612) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L892) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L573)

<a id="op-44049fa1d57eab"></a>
### Selling Controller.set pos for delivery note

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_point_of_sale_for_delivery_note`

**Inputs** self.

**Local steps**

- Set po\_nos from list().
- If self.po\_no.
  - Evaluate po\_nos.append(self.po\_no).
- Evaluate self.get\_po\_nos(“Sales Order”, “against\_sales\_order”, po\_nos).
- Evaluate self.get\_po\_nos(“Sales Invoice”, “against\_sales\_invoice”, po\_nos).
- Set self.po\_no from “, ”.join(list(set(generator of x.strip() for x drawn from nested operand in the contract(nested operand in the contract).split(“,”)))).
  - Draw x from “,”.join(po\_nos).split(“,”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get po nos](operations-021.md#op-77d4847c156581).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0388.json#L5900) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L572)

<a id="op-77d4847c156581"></a>
### Selling Controller.get po nos

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_get_purchase_order_numbers`

**Inputs** self, ref\_doctype, ref\_fieldname, po\_nos.

**Record and data access** read ref\_doctype via get\_all.

**Local steps**

- Set doc\_list from list(set(generator of d.get(ref\_fieldname) for d drawn from self.items where d.get(ref\_fieldname))).
  - Draw d from self.items, keep a combination only if (d.get(ref\_fieldname)).
- If doc\_list.
  - Update po\_nos using + list of d.po\_no for d drawn from Platform.get\_all(ref\_doctype, “po\_no”, filters = mapping(“name” → tuple(“in”, doc\_list))) where d.get(“po\_no”).
    - Draw d from Platform.get\_all(ref\_doctype, “po\_no”, filters = mapping(“name” → tuple(“in”, doc\_list))), keep a combination only if (d.get(“po\_no”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0389.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L877) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L558)

<a id="op-8959895d51ba01"></a>
### Selling Controller.set gross profit

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_gross_profit`

**Inputs** self.

**Local steps**

- If self.doctype belongs to list(“Sales Order”, “Quotation”).
  - For each item in self.items.
    - Set item.gross\_profit from flt(((flt(item.stock\_uom\_rate) − flt(item.valuation\_rate)) × item.stock\_qty), self.precision(“amount”, item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0389.json#L286) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L886) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L567)

<a id="op-75382fc12e443d"></a>
### Selling Controller.set customer address

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_customer_address`

**Inputs** self.

**Local steps**

- Set address\_dict from mapping(“customer\_address” → “address\_display”, “shipping\_address\_name” → “shipping\_address”, “company\_address” → “company\_address\_display”, “dispatch\_address\_name” → “dispatch\_address”).
- For each tuple(address\_field, address\_display\_field) in address\_dict.items().
  - If self.get(address\_field).
    - Evaluate self.set(address\_display\_field, render\_address(self.get(address\_field), check\_permissions = false)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0389.json#L489) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L885) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L566)

<a id="op-f67870d74644dd"></a>
### Selling Controller.validate for duplicate items

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_for_duplicate_items`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — duplicate\_items\_msg.

**Local steps**

- Set tuple(check\_list, chk\_dupl\_itm) from tuple(list(), list()).
- If cint(Platform.get\_single\_value(“Selling Settings”, “allow\_multiple\_items”)).
  - Return no value.
- If (self.doctype equals “Sales Invoice” and self.is\_consolidated).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_consolidated.
  - Return no value.
- If self.doctype equals “POS Invoice”.
  - Return no value.
- Set items from list of item.item\_code for item drawn from self.get(“items”).
  - Draw item from self.get(“items”).
- Set item\_stock\_map from Platform.\_dict(Platform.get\_all(“Item”, filters = mapping(“item\_code” → list(“in”, items)), fields = list(“item\_code”, “is\_stock\_item”), as\_list = true)).
- For each d in self.get(“items”).
  - If self.doctype equals “Sales Invoice”.
    - Set stock\_items from list(d.item\_code, d.description, d.warehouse, (d.sales\_order or d.delivery\_note), …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.sales\_order → d.delivery\_note.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.batch\_no → empty text.
    - Set non\_stock\_items from list(d.item\_code, d.description, (d.sales\_order or d.delivery\_note)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.sales\_order → d.delivery\_note.
  - Otherwise.
    - If self.doctype equals “Delivery Note”.
      - Set stock\_items from list(d.item\_code, d.description, d.warehouse, (d.against\_sales\_order or d.against\_sales\_invoice), …).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.against\_sales\_order → d.against\_sales\_invoice.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.batch\_no → empty text.
      - Set non\_stock\_items from list(d.item\_code, d.description, (d.against\_sales\_order or d.against\_sales\_invoice)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.against\_sales\_order → d.against\_sales\_invoice.
    - Otherwise.
      - If self.doctype belongs to list(“Sales Order”, “Quotation”).
        - Set stock\_items from list(d.item\_code, d.description, d.warehouse, empty text).
        - Set non\_stock\_items from list(d.item\_code, d.description).
  - Set duplicate\_items\_msg from translated “Item {0} entered multiple times.”.format(Platform.bold(d.item\_code)).
  - Update duplicate\_items\_msg using + text in the contract.
  - Update duplicate\_items\_msg using + translated “Please enable {} in {} to allow same item in multiple rows”.format(Platform.bold(translated “Allow Item to Be Added Multiple Times in a Transaction”), get\_link\_to\_form(“Selling Settings”, “Sell ….
  - If item\_stock\_map.get(d.item\_code).
    - If stock\_items belongs to check\_list.
      - Call the validation error handler Platform.throw(duplicate\_items\_msg).
    - Otherwise.
      - Evaluate check\_list.append(stock\_items).
  - Otherwise.
    - If non\_stock\_items belongs to chk\_dupl\_itm.
      - Call the validation error handler Platform.throw(duplicate\_items\_msg).
    - Otherwise.
      - Evaluate chk\_dupl\_itm.append(non\_stock\_items).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_multiple\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L585)

<a id="op-24f79a8603b2cb"></a>
### Selling Controller.validate target warehouse

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_target_warehouse`

**Inputs** self.

**State and service calls** msgprint with msg.

**Explicit failure paths** validation helper — translated “Row {0}: Delivery Warehouse ({1}) and Customer Warehouse ({2}) can not be same”.format(d.idx, warehouse, warehouse).

**Local steps**

- Set items from (self.get(“items”) + (self.get(“packed\_items”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“packed\_items”) → list().
- For each d in items.
  - If (d.get(“target\_warehouse”) and d.get(“warehouse”) equals d.get(“target\_warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“target\_warehouse”) → d.get(“warehouse”) equals d.get(“target\_warehouse”).
    - Set warehouse from Platform.bold(d.get(“target\_warehouse”)).
    - Call the validation error handler Platform.throw(translated “Row {0}: Delivery Warehouse ({1}) and Customer Warehouse ({2}) can not be same”.format(d.idx, warehouse, warehouse)).
- If (not self.get(“is\_internal\_customer”) and any(generator of d.get(“target\_warehouse”) for d drawn from items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“is\_internal\_customer”) → any(generator of d.get(“target\_warehouse”) for d drawn from items).
  - Draw d from items.
  - Set msg from translated “Target Warehouse is set for some items but the customer is not an internal customer.”.
  - Update msg using + (one space + translated “This {} will be treated as material transfer.”.format(translated self.doctype)).
  - Evaluate Platform.msgprint(msg, title = “Internal Transfer”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L912) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L593)

<a id="op-25c89517d04706"></a>
### Selling Controller.validate items

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_items`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_item\_type.
- Evaluate validate\_item\_type(self, “is\_sales\_item”, “sales”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0389.json#L2529) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L586)

<a id="op-876c1bf60e8eee"></a>
### Selling Controller.validate sample retention warehouse

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_sample_retention_warehouse`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Cannot sell item {1} from Sample Retention Warehouse {2}”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(sample\_retention\_warehouse)).

**Local steps**

- If self.get(“is\_return”).
  - Return no value.
- Set sample\_retention\_warehouse from Platform.get\_cached\_value(“Company”, self.company, “sample\_retention\_warehouse”).
- If not sample\_retention\_warehouse.
  - Return no value.
- Set items from (self.get(“items”) + self.get(“packed\_items”)).
- For each item in items.
  - If item.get(“warehouse”) equals sample\_retention\_warehouse.
    - Call the validation error handler Platform.throw(translated “Row {0}: Cannot sell item {1} from Sample Retention Warehouse {2}”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(sample\_retention\_warehouse)), title = translated  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “sample\_retention\_warehouse”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0389.json#L2602) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L589)

<a id="op-36359238e7aff2"></a>
### Selling Controller.validate produced serial nos against reservation

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_validate_produced_serial_nos_against_reservation`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Sales Order Item” via get\_all · read rows at 0.doctype via get\_all · read “Serial and Batch Entry” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Delivery of Item {1} is ensured by produced Serial No, but no Serial No is reserved against Sales  …”.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.get(so\_field))) · validation helper — translated “Row #{0}: Serial No {1} is not reserved against Sales Order {2}. Deliver only the Serial Nos produced and re …”.format(row.idx, Platform.bold(“, ”.join(invalid\_serial\_nos)), Platform.bold(row.g ….

**Local steps**

- Bind dependencies get\_serial\_nos.
- Bind dependencies get\_sre\_reserved\_serial\_nos\_for\_voucher\_detail\_nos.
- If (self.is\_return or not Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → not Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Return no value.
- Set so\_field from “sales\_order” when self.doctype equals “Sales Invoice”, otherwise “against\_sales\_order”.
  - Value choice on self.doctype equals “Sales Invoice” — true gives “sales\_order”, false gives “against\_sales\_order”.
- Set rows from list of d for d drawn from self.items where (d.get(so\_field) and d.so\_detail).
  - Draw d from self.items, keep a combination only if ((d.get(so\_field) and d.so\_detail)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(so\_field) → d.so\_detail.
- If not rows.
  - Return no value.
- Set flagged\_so\_details from Platform.get\_all(“Sales Order Item”, filters = mapping(“name” → tuple(“in”, list of d.so\_detail for d drawn from rows), “ensure\_delivery\_based\_on\_produced\_serial\_no” → 1), pluck = “name”).
  - Draw d from rows.
- Set rows from list of d for d drawn from rows where d.so\_detail belongs to flagged\_so\_details.
  - Draw d from rows, keep a combination only if (d.so\_detail belongs to flagged\_so\_details).
- If not rows.
  - Return no value.
- Set reserved\_serial\_nos from get\_sre\_reserved\_serial\_nos\_for\_voucher\_detail\_nos(“Sales Order”, flagged\_so\_details).
- Set bundle\_map from dict(Platform.get\_all(rows at 0.doctype, filters = mapping(“name” → tuple(“in”, list of d.name for d drawn from rows)), fields = list(“name”, “serial\_and\_batch\_bundle”), as\_list = true)).
  - Draw d from rows.
- Set bundle\_serial\_nos from Platform.\_dict().
- If bundles bound to list of b for b drawn from bundle\_map.values() where b.
  - Draw b from bundle\_map.values(), keep a combination only if (b).
  - For each entry in Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, bundles), “serial\_no” → tuple(“is”, “set”)), fields = list(“parent”, “serial\_no”)).
    - Evaluate bundle\_serial\_nos.setdefault(entry.parent, list()).append(entry.serial\_no).
- For each row in rows.
  - If not reserved\_serial\_nos.get(row.so\_detail).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery of Item {1} is ensured by produced Serial No, but no Serial No is reserved against Sales  …”.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.ge ….
  - Set bundle from bundle\_map.get(row.name).
  - Set serial\_nos from bundle\_serial\_nos.get(bundle, list()) when bundle, otherwise get\_serial\_nos(row.serial\_no).
    - Value choice on bundle — true gives bundle\_serial\_nos.get(bundle, list()), false gives get\_serial\_nos(row.serial\_no).
  - If invalid\_serial\_nos bound to list of sn for sn drawn from serial\_nos where sn does not belong to reserved\_serial\_nos at row.so\_detail.
    - Draw sn from serial\_nos, keep a combination only if (sn does not belong to reserved\_serial\_nos at row.so\_detail).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Serial No {1} is not reserved against Sales Order {2}. Deliver only the Serial Nos produced and re …”.format(row.idx, Platform.bold(“, ”.join(invalid\_serial\_nos)), Plat ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L351)

<a id="op-141b9c99f77527"></a>
### Selling Controller.update stock reservation entries

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_update_stock_reservation_entries`

**Inputs** self.

**Declared result** no value.

**Record and data access** resolve a document from “Stock Reservation Entry” via get\_doc · read “Stock Reservation Entry” via get\_all · resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call db\_update on entry · call db\_update on sre\_doc.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_order\_packed\_item\_pairs.
- Bind dependencies get\_qty\_to\_undeliver, get\_qty\_up\_to\_rounding.
- If self.is\_return.
  - Return no value.
- Set so\_field from “sales\_order” when self.doctype equals “Sales Invoice”, otherwise “against\_sales\_order”.
  - Value choice on self.doctype equals “Sales Invoice” — true gives “sales\_order”, false gives “against\_sales\_order”.
- Set bundle\_rows from set of packed\_item.parent\_detail\_docname for packed\_item drawn from self.packed\_items.
  - Draw packed\_item from self.packed\_items.
- Set items from list of item for item drawn from self.items where item.name does not belong to bundle\_rows.
  - Draw item from self.items, keep a combination only if (item.name does not belong to bundle\_rows).
- Set items\_by\_name from mapping of item.name → item for item drawn from self.items.
  - Draw item from self.items.
- For each tuple(packed\_item, so\_packed\_item) in get\_order\_packed\_item\_pairs(self).
  - Evaluate packed\_item.set(so\_field, items\_by\_name at packed\_item.parent\_detail\_docname.get(so\_field)).
  - Set packed\_item.so\_detail from so\_packed\_item.name.
  - Evaluate items.append(packed\_item).
- If self.\_action equals “submit”.
  - For each item in items.
    - If (not item.get(so\_field) or not item.so\_detail).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(so\_field) → not item.so\_detail.
      - Continue with the next iteration or loop test.
    - Set table from Platform.qb.DocType(“Stock Reservation Entry”).
    - Set query from nested operand in the contract(nested operand in the contract).select(table.name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the cont ….
    - Set sre\_list from query.run(pluck = “name”).
    - If not sre\_list.
      - Continue with the next iteration or loop test.
    - Set qty\_to\_deliver from (item.get(“stock\_qty”) or item.qty).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“stock\_qty”) → item.qty.
    - For each sre in sre\_list.
      - <a id="op-141b9c99f77527-guard-53"></a>If qty\_to\_deliver ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Set sre\_doc from Platform.get\_doc(“Stock Reservation Entry”, sre).
      - Set qty\_can\_be\_deliver from 0.
      - If sre\_doc.reservation\_based\_on equals “Serial and Batch”.
        - Set tuple(delivered\_serial\_nos, delivered\_batch\_qty) from get\_delivered\_serial\_batch\_for\_reservation(item).
        - If sre\_doc.has\_serial\_no.
          - For each entry in sre\_doc.sb\_entries.
            - If entry.serial\_no belongs to delivered\_serial\_nos.
              - Set entry.delivered\_qty from 1.
              - Evaluate entry.db\_update().
              - Update qty\_can\_be\_deliver using + 1.
              - Evaluate delivered\_serial\_nos.remove(entry.serial\_no).
        - Otherwise.
          - For each entry in sre\_doc.sb\_entries.
            - Set available\_batch\_qty from delivered\_batch\_qty.get(entry.batch\_no, 0).
            - If available\_batch\_qty &gt; 0.
              - Set pending\_qty from (entry.qty − entry.delivered\_qty).
              - Set delivered\_qty from get\_qty\_up\_to\_rounding(min(pending\_qty, available\_batch\_qty), pending\_qty).
              - Update entry.delivered\_qty using + delivered\_qty.
              - Evaluate entry.db\_update().
              - Update qty\_can\_be\_deliver using + delivered\_qty.
              - Set delivered\_batch\_qty at entry.batch\_no from (available\_batch\_qty − delivered\_qty).
      - Otherwise.
        - Set qty\_can\_be\_deliver from min((sre\_doc.reserved\_qty − sre\_doc.delivered\_qty), qty\_to\_deliver).
      - Update sre\_doc.delivered\_qty using + qty\_can\_be\_deliver.
      - Evaluate sre\_doc.db\_update().
      - Evaluate sre\_doc.update\_status().
      - Evaluate sre\_doc.update\_reserved\_stock\_in\_bin().
      - Evaluate sre\_doc.update\_reserved\_qty\_in\_voucher(update\_modified = false).
      - Update qty\_to\_deliver using − qty\_can\_be\_deliver.
- If self.\_action equals “cancel”.
  - For each item in items.
    - If (not item.get(so\_field) or not item.so\_detail).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(so\_field) → not item.so\_detail.
      - Continue with the next iteration or loop test.
    - Set sre\_list from Platform.db.get\_all(“Stock Reservation Entry”, mapping(“docstatus” → 1, “voucher\_type” → “Sales Order”, “voucher\_no” → item.get(so\_field), “voucher\_detail\_no” → item.so\_detail, …), order\_by = “creation”).
    - If not sre\_list.
      - Continue with the next iteration or loop test.
    - Set qty\_to\_undelivered from (item.get(“stock\_qty”) or item.qty).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“stock\_qty”) → item.qty.
    - For each sre in sre\_list.
      - <a id="op-141b9c99f77527-guard-129"></a>If qty\_to\_undelivered ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Set sre\_doc from Platform.get\_doc(“Stock Reservation Entry”, sre).
      - Set qty\_can\_be\_undelivered from 0.
      - If sre\_doc.reservation\_based\_on equals “Serial and Batch”.
        - Set sbb from Platform.get\_doc(“Serial and Batch Bundle”, item.serial\_and\_batch\_bundle).
        - If sre\_doc.has\_serial\_no.
          - Set serial\_nos\_to\_undelivered from list of d.serial\_no for d drawn from sbb.entries.
            - Draw d from sbb.entries.
          - For each entry in sre\_doc.sb\_entries.
            - If entry.serial\_no belongs to serial\_nos\_to\_undelivered.
              - Set entry.delivered\_qty from 0.
              - Evaluate entry.db\_update().
              - Update qty\_can\_be\_undelivered using + 1.
              - Evaluate serial\_nos\_to\_undelivered.remove(entry.serial\_no).
        - Otherwise.
          - Set batch\_qty\_to\_undelivered from mapping of d.batch\_no → (negative 1 × d.qty) for d drawn from sbb.entries.
            - Draw d from sbb.entries.
          - For each entry in sre\_doc.sb\_entries.
            - If batch\_qty\_to\_undelivered.get(entry.batch\_no, 0) &gt; 0.
              - Set undelivered\_qty from get\_qty\_to\_undeliver(entry.delivered\_qty, batch\_qty\_to\_undelivered at entry.batch\_no).
              - Update entry.delivered\_qty using − undelivered\_qty.
              - Evaluate entry.db\_update().
              - Update qty\_can\_be\_undelivered using + undelivered\_qty.
              - Update batch\_qty\_to\_undelivered at entry.batch\_no using − undelivered\_qty.
      - Otherwise.
        - Set qty\_can\_be\_undelivered from min(sre\_doc.delivered\_qty, qty\_to\_undelivered).
      - Update sre\_doc.delivered\_qty using − qty\_can\_be\_undelivered.
      - Evaluate sre\_doc.db\_update().
      - Evaluate sre\_doc.update\_status().
      - Evaluate sre\_doc.update\_reserved\_stock\_in\_bin().
      - Evaluate sre\_doc.update\_reserved\_qty\_in\_voucher(update\_modified = false).
      - Update qty\_to\_undelivered using − qty\_can\_be\_undelivered.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty\_to\_deliver ≤ 0, qty\_to\_deliver = 0 selects the branch that exits the enclosing loop. With qty\_to\_deliver = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-141b9c99f77527-guard-53)
- At the comparison qty\_to\_undelivered ≤ 0, qty\_to\_undelivered = 0 selects the branch that exits the enclosing loop. With qty\_to\_undelivered = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-141b9c99f77527-guard-129)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L583)

<a id="op-cf3d29be0906c9"></a>
### Selling Controller.set serial and batch bundle from pick list

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_serial_and_batch_bundle_from_pick_list`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_value.

**State and service calls** call save on package.

**Local steps**

- Bind dependencies SerialBatchCreation.
- For each item in self.items.
  - If (item.use\_serial\_batch\_fields or not item.against\_pick\_list or not self.get(“update\_stock”, 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.use\_serial\_batch\_fields → not item.against\_pick\_list → not self.get(“update\_stock”, 1).
    - Continue with the next iteration or loop test.
  - If (item.pick\_list\_item and not item.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.pick\_list\_item → not item.serial\_and\_batch\_bundle.
    - Set filters from mapping(“item\_code” → item.item\_code, “voucher\_type” → “Pick List”, “voucher\_no” → item.against\_pick\_list, “voucher\_detail\_no” → item.pick\_list\_item).
    - Set bundle\_id from Platform.db.get\_value(“Serial and Batch Bundle”, filters, “name”).
    - If bundle\_id.
      - Set package from SerialBatchCreation(mapping(“type\_of\_transaction” → “Outward”, “serial\_and\_batch\_bundle” → bundle\_id, “item\_code” → item.get(“item\_code”), “warehouse” → item.get(“warehouse”), …)).duplicate\_package().
      - Evaluate remove\_delivered\_entries(package, item.pick\_list\_item).
      - Evaluate package.save().
      - Set item.serial\_and\_batch\_bundle from package.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L896) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L577)
