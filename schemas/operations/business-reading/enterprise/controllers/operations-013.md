# Shared transaction rules · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Buying controller

<a id="op-0df5b030c2ab5a"></a>
### Buying Controller.distribute actual tax amount

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_distribute_actual_tax_amount`

**Inputs** self, stock\_and\_asset\_items, all\_item\_charges, stock\_item\_charges.

**Explicit results** charge\_per\_item.

**Local steps**

- Set all\_items from list of d for d drawn from self.get(“items”) where d.item\_code.
  - Draw d from self.get(“items”), keep a combination only if (d.item\_code).
- Set stock\_items from list of d for d drawn from all\_items where d.item\_code belongs to stock\_and\_asset\_items.
  - Draw d from all\_items, keep a combination only if (d.item\_code belongs to stock\_and\_asset\_items).
- Set charge\_per\_item from mapping().
- For each charge in all\_item\_charges.
  - Evaluate self.\_spread\_charge\_over\_items(charge\_per\_item, charge, all\_items).
- For each charge in stock\_item\_charges.
  - Evaluate self.\_spread\_charge\_over\_items(charge\_per\_item, charge, stock\_items).
- For each tax in self.get(“taxes”).
  - If (tax.charge\_type equals “On Item Quantity” and tax.category belongs to tuple(“Valuation”, “Valuation and Total”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “On Item Quantity” → tax.category belongs to tuple(“Valuation”, “Valuation and Total”).
    - For each tuple(item\_idx, amount) in self.get\_quantity\_based\_tax\_amounts(tax).items().
      - Set charge\_per\_item at item\_idx from (charge\_per\_item.get(item\_idx, 0.0) + amount).
- Return charge\_per\_item.

**Methods declared on this owner** [spread charge over items](operations-013.md#op-93c85f54d9d504), [get quantity based tax amounts](operations-013.md#op-bd128c38853814).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L416)

<a id="op-bd128c38853814"></a>
### Buying Controller.get quantity based tax amounts

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_quantity_based_tax_amounts`

**Inputs** self, tax.

**Explicit results** mapping of row.item.idx → flt(row.amount) for row drawn from self.get(“\_item\_wise\_tax\_details”) where row.tax.idx equals tax.idx · mapping of item\_indices at row.item\_row → flt(row.amount) for row drawn from (self.get(“item\_wise\_tax\_details”) or list()) where row.tax\_row equals tax.name.

**Local steps**

- If self.get(“\_item\_wise\_tax\_details”).
  - Return mapping of row.item.idx → flt(row.amount) for row drawn from self.get(“\_item\_wise\_tax\_details”) where row.tax.idx equals tax.idx.
    - Draw row from self.get(“\_item\_wise\_tax\_details”), keep a combination only if (row.tax.idx equals tax.idx).
- Set item\_indices from mapping of item.name → item.idx for item drawn from self.get(“items”).
  - Draw item from self.get(“items”).
- Return mapping of item\_indices at row.item\_row → flt(row.amount) for row drawn from (self.get(“item\_wise\_tax\_details”) or list()) where row.tax\_row equals tax.name.
  - Draw row from (self.get(“item\_wise\_tax\_details”) or list()), keep a combination only if (row.tax\_row equals tax.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“item\_wise\_tax\_details”) → list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1050) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L290)

<a id="op-93c85f54d9d504"></a>
### Buying Controller.spread charge over items

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_spread_charge_over_items`

**Inputs** self, charge\_per\_item, total\_charge, items.

**Explicit results** no value.

**Local steps**

- If (not total\_charge or not items).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not total\_charge → not items.
  - Return no value.
- Set basis from mapping of d.idx → flt(d.base\_net\_amount) for d drawn from items.
  - Draw d from items.
- If not sum(basis.values()).
  - Set basis from self.get\_chargeable\_qty(items).
- Set total\_basis from sum(basis.values()).
- If not total\_basis.
  - Return no value.
- Set items\_with\_share from list of d for d drawn from items where basis at d.idx.
  - Draw d from items, keep a combination only if (basis at d.idx).
- Set remaining from total\_charge.
- For each d in items\_with\_share at slice no value to negative 1.
  - Set charge from flt(((basis at d.idx ÷ total\_basis) × total\_charge), self.precision(“item\_tax\_amount”, d)).
  - Set charge\_per\_item at d.idx from (charge\_per\_item.get(d.idx, 0.0) + charge).
  - Update remaining using − charge.
- Set last from items\_with\_share at negative 1.
- Set charge\_per\_item at last.idx from (charge\_per\_item.get(last.idx, 0.0) + flt(remaining, self.precision(“item\_tax\_amount”, last))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get chargeable qty](operations-013.md#op-9f67527515cbb0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L438)

<a id="op-9f67527515cbb0"></a>
### Buying Controller.get chargeable qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_chargeable_qty`

**Inputs** self, items.

**Declared result** dict.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** chargeable\_qty.

**Local steps**

- Set chargeable\_qty from mapping of d.idx → flt(d.qty) for d drawn from items.
  - Draw d from items.
- If (self.doctype differs from “Purchase Receipt” or self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype differs from “Purchase Receipt” → self.is\_internal\_transfer().
  - Return chargeable\_qty.
- If not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).
  - Return chargeable\_qty.
- Set rejected\_rows from list of d for d drawn from items where not flt(d.qty).
  - Draw d from items, keep a combination only if (not flt(d.qty)).
- Set uncharged\_rows from self.get\_uncharged\_receipt\_rows(rejected\_rows) when self.is\_return, otherwise tuple().
  - Value choice on self.is\_return — true gives self.get\_uncharged\_receipt\_rows(rejected\_rows), false gives tuple().
- For each d in rejected\_rows.
  - If d.purchase\_receipt\_item does not belong to uncharged\_rows.
    - Set chargeable\_qty at d.idx from flt(d.rejected\_qty).
- Return chargeable\_qty.

**Methods declared on this owner** [get uncharged receipt rows](operations-013.md#op-6133495320b2d0).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1037) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L277)

<a id="op-6133495320b2d0"></a>
### Buying Controller.get uncharged receipt rows

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_uncharged_receipt_rows`

**Inputs** self, rows.

**Declared result** set.

**Record and data access** read “Purchase Receipt Item” via get\_all.

**Explicit results** set of d.name for d drawn from receipt\_rows where (flt(d.qty) or not flt(d.item\_tax\_amount)).

**Local steps**

- Set receipt\_rows from Platform.get\_all(“Purchase Receipt Item”, filters = mapping(“name” → list(“in”, list of d.purchase\_receipt\_item for d drawn from rows where d.purchase\_receipt\_item)), fields = list(“name”, “qty”, “item\_tax\_amount”)).
  - Draw d from rows, keep a combination only if (d.purchase\_receipt\_item).
- Return set of d.name for d drawn from receipt\_rows where (flt(d.qty) or not flt(d.item\_tax\_amount)).
  - Draw d from receipt\_rows, keep a combination only if ((flt(d.qty) or not flt(d.item\_tax\_amount))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.qty) → not flt(d.item\_tax\_amount).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1060) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L300)

<a id="op-0774e11aaf2838"></a>
### Buying Controller.get capitalized valuation tax

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_get_capitalized_valuation_tax`

**Inputs** self.

**Explicit results** capitalized.

**Local steps**

- Set stock\_and\_asset\_items from (self.get\_stock\_items() + self.get\_asset\_items()).
- Set all\_items from list of d for d drawn from self.get(“items”) where d.item\_code.
  - Draw d from self.get(“items”), keep a combination only if (d.item\_code).
- Set stock\_item\_idx from set of d.idx for d drawn from all\_items where d.item\_code belongs to stock\_and\_asset\_items.
  - Draw d from all\_items, keep a combination only if (d.item\_code belongs to stock\_and\_asset\_items).
- Set capitalized from mapping().
- For each tax in self.get(“taxes”).
  - If tax.category does not belong to tuple(“Valuation”, “Valuation and Total”).
    - Continue with the next iteration or loop test.
  - Set amount from (flt(tax.base\_tax\_amount\_after\_discount\_amount) × negative 1 when tax.get(“add\_deduct\_tax”) equals “Deduct”, otherwise 1).
    - Value choice on tax.get(“add\_deduct\_tax”) equals “Deduct” — true gives negative 1, false gives 1.
  - If not amount.
    - Continue with the next iteration or loop test.
  - If tax.charge\_type equals “On Item Quantity”.
    - Set amount from sum(generator of charge for tuple(item\_idx, charge) drawn from self.get\_quantity\_based\_tax\_amounts(tax).items() where item\_idx belongs to stock\_item\_idx).
      - Draw tuple(item\_idx, charge) from self.get\_quantity\_based\_tax\_amounts(tax).items(), keep a combination only if (item\_idx belongs to stock\_item\_idx).
  - Otherwise.
    - If (tax.charge\_type equals “Actual” and not tax.get(“allocate\_full\_amount\_to\_stock\_items”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “Actual” → not tax.get(“allocate\_full\_amount\_to\_stock\_items”).
      - Set charge\_per\_item from mapping().
      - Evaluate self.\_spread\_charge\_over\_items(charge\_per\_item, amount, all\_items).
      - Set amount from sum(generator of charge for tuple(item\_idx, charge) drawn from charge\_per\_item.items() where item\_idx belongs to stock\_item\_idx).
        - Draw tuple(item\_idx, charge) from charge\_per\_item.items(), keep a combination only if (item\_idx belongs to stock\_item\_idx).
  - Set capitalized at tax.name from amount.
- Return capitalized.

**Methods declared on this owner** [get asset items](operations-012.md#op-84a2b4acb31810), [get quantity based tax amounts](operations-013.md#op-bd128c38853814), [spread charge over items](operations-013.md#op-93c85f54d9d504).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L418)

<a id="op-2125f3b1495fe6"></a>
### Buying Controller.set incoming rate

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_incoming_rate`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_cached\_value.

**State and service calls** msgprint with translated “Row #{idx}: Item rate has been updated as per valuation rate since its an internal stock transfer.”.format(idx = d.idx).

**Explicit results** no value.

**Local steps**

- If self.doctype does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”).
  - Return no value.
- If not (self.doctype equals “Purchase Receipt” or self.get(“update\_stock”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → self.get(“update\_stock”).
  - Return no value.
- If cint(self.get(“is\_return”)).
  - If self.is\_internal\_transfer().
    - Evaluate self.set\_sales\_incoming\_rate\_for\_internal\_transfer().
  - Return no value.
- If not self.is\_internal\_transfer().
  - Return no value.
- Evaluate self.set\_sales\_incoming\_rate\_for\_internal\_transfer().
- Set allow\_at\_arms\_length\_price from Platform.get\_cached\_value(“Stock Settings”, no value, “allow\_internal\_transfer\_at\_arms\_length\_price”).
- If allow\_at\_arms\_length\_price.
  - Return no value.
- For each d in self.get(“items”).
  - Set d.discount\_percentage from 0.0.
  - Set d.discount\_amount from 0.0.
  - Set d.margin\_rate\_or\_amount from 0.0.
  - If d.rate equals d.sales\_incoming\_rate.
    - Continue with the next iteration or loop test.
  - Set d.rate from d.sales\_incoming\_rate.
  - Evaluate Platform.msgprint(translated “Row #{idx}: Item rate has been updated as per valuation rate since its an internal stock transfer.”.format(idx = d.idx), alert = 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set sales incoming rate for internal transfer](operations-013.md#op-1db9c0400a2adf).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Settings”, no value, “allow\_internal\_transfer\_at\_arms\_length\_price”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L429)

<a id="op-1db9c0400a2adf"></a>
### Buying Controller.set sales incoming rate for internal transfer

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_sales_incoming_rate_for_internal_transfer`

**Inputs** self.

**Record and data access** read (self.doctype + “ Item”) via get\_value · read ref\_doctype via get\_value.

**Local steps**

- Set ref\_doctype\_map from mapping(“Purchase Receipt” → “Delivery Note Item”, “Purchase Invoice” → “Sales Invoice Item”).
- Set ref\_doctype from ref\_doctype\_map.get(self.doctype).
- Set returned\_field from (Platform.scrub(self.doctype) + “\_item”).
- Set component\_rates from self.get\_component\_incoming\_rates().
- For each d in self.get(“items”).
  - If (self.get(“is\_return”) and d.get(returned\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → d.get(returned\_field).
    - Set d.sales\_incoming\_rate from flt(Platform.db.get\_value((self.doctype + “ Item”), d.get(returned\_field), “sales\_incoming\_rate”)).
  - Otherwise.
    - If d.get(“delivery\_note\_packed\_item”) belongs to component\_rates.
      - Set d.sales\_incoming\_rate from flt((component\_rates at d.delivery\_note\_packed\_item × (d.conversion\_factor or 1))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.conversion\_factor → 1.
    - Otherwise.
      - If not d.get(Platform.scrub(ref\_doctype)).
        - Set posting\_time from self.get(“posting\_time”).
        - If not posting\_time.
          - Set posting\_time from nowtime().
        - Set outgoing\_rate from \_get\_incoming\_rate(mapping(“item\_code” → d.item\_code, “warehouse” → d.get(“from\_warehouse”), “posting\_date” → (self.get(“posting\_date”) or self.get(“transaction\_date”)), “posting\_time” → posting\_time, …),  ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“posting\_date”) → self.get(“transaction\_date”).
        - Set d.sales\_incoming\_rate from flt((outgoing\_rate × (d.conversion\_factor or 1))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.conversion\_factor → 1.
      - Otherwise.
        - Set field from “incoming\_rate” when self.get(“is\_internal\_supplier”), otherwise “rate”.
          - Value choice on self.get(“is\_internal\_supplier”) — true gives “incoming\_rate”, false gives “rate”.
        - Set d.sales\_incoming\_rate from flt((Platform.db.get\_value(ref\_doctype, d.get(Platform.scrub(ref\_doctype)), field) × (d.conversion\_factor or 1))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.conversion\_factor → 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get component incoming rates](operations-011.md#op-2b38da3b8e273b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L433)

<a id="op-f4838850312b46"></a>
### Buying Controller.validate for subcontracting

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_validate_for_subcontracting`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{field\_label} is mandatory for sub-contracted {doctype}.”.format(field\_label = translated self.meta.get\_label(“supplier\_warehouse”), doctype = translated self.doctype) · validation helper — translated “Please select BOM in BOM field for Item {item\_code}.”.format(item\_code = Platform.bold(item.item\_code)) · validation helper — translated “Reserved Warehouse is mandatory for the Item {item\_code} in Raw Materials supplied.”.format(item\_code = Platform.bold(row.rm\_item\_code)).

**Local steps**

- If (self.is\_subcontracted and self.get(“is\_old\_subcontracting\_flow”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_subcontracted → self.get(“is\_old\_subcontracting\_flow”).
  - If (self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”) and not self.supplier\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”) → not self.supplier\_warehouse.
    - Call the validation error handler Platform.throw(translated “{field\_label} is mandatory for sub-contracted {doctype}.”.format(field\_label = translated self.meta.get\_label(“supplier\_warehouse”), doctype = translated self.doctype)).
  - For each item in self.get(“items”).
    - If (item belongs to self.sub\_contracted\_items and not item.bom).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item belongs to self.sub\_contracted\_items → not item.bom.
      - Call the validation error handler Platform.throw(translated “Please select BOM in BOM field for Item {item\_code}.”.format(item\_code = Platform.bold(item.item\_code))).
  - If self.doctype differs from “Purchase Order”.
    - Return no value.
  - For each row in self.get(“supplied\_items”).
    - If not row.reserve\_warehouse.
      - Call the validation error handler Platform.throw(translated “Reserved Warehouse is mandatory for the Item {item\_code} in Raw Materials supplied.”.format(item\_code = Platform.bold(row.rm\_item\_code))).
- Otherwise.
  - For each item in self.get(“items”).
    - If item.get(“bom”).
      - Set item.bom from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1071) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L311)

<a id="op-253a0adebafa0b"></a>
### Buying Controller.set qty as per stock uom

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_quantity_as_per_stock_unit_of_measure`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Row #{idx}: {field\_label} is mandatory.”.format(idx = d.idx, field\_label = translated d.meta.get\_label(“conversion\_factor”)).

**Local steps**

- Set allow\_to\_edit\_stock\_qty from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”).
- Set whole\_number\_uoms from get\_whole\_number\_uoms(generator of d.get(“stock\_uom”) for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
- For each d in self.get(“items”).
  - If d.meta.get\_field(“stock\_qty”).
    - If (not d.conversion\_factor and d.item\_code).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.conversion\_factor → d.item\_code.
      - Call the validation error handler Platform.throw(translated “Row #{idx}: {field\_label} is mandatory.”.format(idx = d.idx, field\_label = translated d.meta.get\_label(“conversion\_factor”))).
    - Set d.stock\_qty from (flt(d.qty) × flt(d.conversion\_factor)).
    - If (self.doctype equals “Purchase Receipt” and d.meta.get\_field(“received\_stock\_qty”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → d.meta.get\_field(“received\_stock\_qty”).
      - Set d.received\_stock\_qty from (flt(d.received\_qty) × flt(d.conversion\_factor, d.precision(“conversion\_factor”))).
    - If (allow\_to\_edit\_stock\_qty or d.get(“stock\_uom”) belongs to whole\_number\_uoms).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in allow\_to\_edit\_stock\_qty → d.get(“stock\_uom”) belongs to whole\_number\_uoms.
      - Set d.stock\_qty from flt(d.stock\_qty, d.precision(“stock\_qty”)).
      - If (d.get(“received\_stock\_qty”) and d.meta.get\_field(“received\_stock\_qty”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“received\_stock\_qty”) → d.meta.get\_field(“received\_stock\_qty”).
        - Set d.received\_stock\_qty from flt(d.received\_stock\_qty, d.precision(“received\_stock\_qty”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L431)

<a id="op-aeca9a901a720e"></a>
### Buying Controller.validate purchase return

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_purchase_return`

**Inputs** self.

**Local steps**

- For each d in self.get(“items”).
  - If (self.is\_return and not flt(d.rejected\_qty) and d.rejected\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not flt(d.rejected\_qty) → d.rejected\_warehouse.
    - Set d.rejected\_warehouse from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0373.json#L2688) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L452)

<a id="op-86c4a0e5bae100"></a>
### Buying Controller.validate accepted rejected qty

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_accepted_rejected_quantity`

**Inputs** self.

**Explicit failure paths** validation helper with QtyMismatchError.

**Local steps**

- For each d in self.get(“items”).
  - Evaluate self.validate\_negative\_quantity(d, list(“received\_qty”, “qty”, “rejected\_qty”)).
  - If (not flt(d.received\_qty) and (flt(d.qty) or flt(d.rejected\_qty))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(d.received\_qty) → (flt(d.qty) or flt(d.rejected\_qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.qty) → flt(d.rejected\_qty).
    - Set d.received\_qty from (flt(d.qty) + flt(d.rejected\_qty)).
  - Set val from (flt(d.qty) + flt(d.rejected\_qty)).
  - If flt(val, d.precision(“received\_qty”)) differs from flt(d.received\_qty, d.precision(“received\_qty”)).
    - Set message from translated “Row #{idx}: Received Qty must be equal to Accepted + Rejected Qty for Item {item\_code}.”.format(idx = d.idx, item\_code = Platform.bold(d.item\_code)).
    - Call the validation error handler Platform.throw(msg = message, title = translated “Mismatch”, exc = QtyMismatchError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate negative quantity](operations-013.md#op-537e9c5ef4bce7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0373.json#L2823) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L445)

<a id="op-537e9c5ef4bce7"></a>
### Buying Controller.validate negative quantity

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_negative_quantity`

**Inputs** self, item\_row, field\_list.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{idx}: {field\_label} can not be negative for item {item\_code}.”.format(idx = item\_row at “idx”, field\_label = Platform.get\_meta(item\_row.doctype).get\_label(fieldname), item\_code = Platform ….

**Local steps**

- If self.is\_return.
  - Return no value.
- Set item\_row from item\_row.as\_dict().
- For each fieldname in field\_list.
  - If flt(item\_row at fieldname) &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{idx}: {field\_label} can not be negative for item {item\_code}.”.format(idx = item\_row at “idx”, field\_label = Platform.get\_meta(item\_row.doctype).get\_label(fieldname), item\_ ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L450)

<a id="op-46d9cccbba42e7"></a>
### Buying Controller.get internal transfer qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_internal_transfer_qty`

**Inputs** self, row.

**Declared result** float.

**Explicit results** flt(row.qty) · flt(row.rejected\_qty).

**Local steps**

- If (flt(row.qty) or not self.is\_internal\_receipt()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.qty) → not self.is\_internal\_receipt().
  - Return flt(row.qty).
- Return flt(row.rejected\_qty).

**Methods declared on this owner** [is internal receipt](operations-013.md#op-df2f3b164c398c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1043) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L283)

<a id="op-df2f3b164c398c"></a>
### Buying Controller.is internal receipt

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_is_internal_receipt`

**Inputs** self.

**Declared result** bool.

**Explicit results** (self.is\_internal\_transfer() and self.is\_stock\_receipt()).

**Local steps**

- Return (self.is\_internal\_transfer() and self.is\_stock\_receipt()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → self.is\_stock\_receipt().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1064) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L304)

<a id="op-7619219c6072c9"></a>
### Buying Controller.has rejected stock

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_has_rejected_stock`

**Inputs** self, row.

**Declared result** bool.

**Explicit results** (self.is\_internal\_receipt() and bool(get\_stock\_qty(row, row.rejected\_qty))).

**Local steps**

- Return (self.is\_internal\_receipt() and bool(get\_stock\_qty(row, row.rejected\_qty))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_receipt() → bool(get\_stock\_qty(row, row.rejected\_qty)).

**Methods declared on this owner** [is internal receipt](operations-013.md#op-df2f3b164c398c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1062) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L302)

<a id="op-488a852092ff4d"></a>
### Buying Controller.get source warehouse qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_source_warehouse_qty`

**Inputs** self, row, accepted\_qty.

**Explicit results** qty · (negative flt(self.get\_posted\_qty(row.name, row.from\_warehouse, outward = not self.is\_return)) or qty) · max(qty, negative qty\_left) when flt(qty\_left) &gt; 0, otherwise qty · min(qty, qty\_left) when flt(qty\_left) &gt; 0, otherwise qty.

**Local steps**

- Set qty from self.get\_received\_stock\_qty(row, accepted\_qty).
- If not self.is\_capped\_in\_transit(row).
  - Return qty.
- If self.docstatus equals 2.
  - Return (negative flt(self.get\_posted\_qty(row.name, row.from\_warehouse, outward = not self.is\_return)) or qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in negative flt(self.get\_posted\_qty(row.name, row.from\_warehouse, outward = not self.is\_return)) → qty.
- If self.is\_return.
  - Set qty\_left from self.get\_qty\_left\_to\_return(row).
  - Return max(qty, negative qty\_left) when flt(qty\_left) &gt; 0, otherwise qty.
    - Value choice on flt(qty\_left) &gt; 0 — true gives max(qty, negative qty\_left), false gives qty.
- Set qty\_left from self.get\_qty\_left\_in\_transit(row).
- Return min(qty, qty\_left) when flt(qty\_left) &gt; 0, otherwise qty.
  - Value choice on flt(qty\_left) &gt; 0 — true gives min(qty, qty\_left), false gives qty.

**Methods declared on this owner** [get received stock qty](operations-013.md#op-6d0bd7d86356a4), [is capped in transit](operations-013.md#op-6e85798343d126), [get posted qty](operations-013.md#op-426926759721a9), [get qty left to return](operations-013.md#op-6602ec615bad93), [get qty left in transit](operations-013.md#op-4ffce1b42758c6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1057) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L297)

<a id="op-6e85798343d126"></a>
### Buying Controller.is capped in transit

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_is_capped_in_transit`

**Inputs** self, row.

**Declared result** bool.

**Explicit results** false · bool(row.get(“purchase\_receipt\_item”) when self.is\_return, otherwise row.get(“delivery\_note\_item”)).

**Local steps**

- If not self.is\_internal\_receipt().
  - Return false.
- If (row.get(“serial\_and\_batch\_bundle”) or row.get(“rejected\_serial\_and\_batch\_bundle”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“serial\_and\_batch\_bundle”) → row.get(“rejected\_serial\_and\_batch\_bundle”).
  - Return false.
- Return bool(row.get(“purchase\_receipt\_item”) when self.is\_return, otherwise row.get(“delivery\_note\_item”)).
  - Value choice on self.is\_return — true gives row.get(“purchase\_receipt\_item”), false gives row.get(“delivery\_note\_item”).

**Methods declared on this owner** [is internal receipt](operations-013.md#op-df2f3b164c398c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1063) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L303)

<a id="op-6602ec615bad93"></a>
### Buying Controller.get qty left to return

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_qty_left_to_return`

**Inputs** self, row.

**Declared result** float.

**Explicit results** negative flt(moved\_qty, row.precision(“stock\_qty”)).

**Local steps**

- Set receipt\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set other\_returns from nested operand in the contract.qb.from\_(receipt\_item).select(receipt\_item.name).where((receipt\_item.purchase\_receipt\_item equals row.purchase\_receipt\_item bitwise and receipt\_item.parent differs from self.name)).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set moved\_qty from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise or nest … at 0.
- Return negative flt(moved\_qty, row.precision(“stock\_qty”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1049) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L289)

<a id="op-4ffce1b42758c6"></a>
### Buying Controller.get qty left in transit

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_qty_left_in_transit`

**Inputs** self, row.

**Declared result** (float bitwise or no value).

**Explicit results** no value · flt((delivered\_qty + taken\_qty), precision).

**Local steps**

- Set delivered\_qty from self.get\_posted\_qty(row.delivery\_note\_item, row.from\_warehouse, outward = false).
- If not delivered\_qty.
  - Return no value.
- Set tuple(received\_qty, taken\_qty) from self.get\_other\_receipts\_of\_delivered\_row(row).
- Update received\_qty using + ((flt(row.qty) + flt(row.rejected\_qty)) × flt(row.conversion\_factor)).
- Set precision from row.precision(“stock\_qty”).
- If flt(received\_qty, precision) &gt; delivered\_qty.
  - Return no value.
- Return flt((delivered\_qty + taken\_qty), precision).

**Methods declared on this owner** [get posted qty](operations-013.md#op-426926759721a9), [get other receipts of delivered row](operations-013.md#op-6d29156a837c3d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1048) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L288)

<a id="op-6d29156a837c3d"></a>
### Buying Controller.get other receipts of delivered row

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_other_receipts_of_delivered_row`

**Inputs** self, row.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(0.0, 0.0) · tuple(sum(generator of flt(d.qty) for d drawn from rows), flt(taken\_qty)).

**Local steps**

- Set receipt\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set other\_receipt\_rows from nested operand in the contract.qb.from\_(receipt\_item).select(receipt\_item.name).where((receipt\_item.delivery\_note\_item equals row.delivery\_note\_item bitwise and receipt\_item.parent differs from self.name)).
- Set rows from nested operand in the contract(nested operand in the contract).select(receipt\_item.name, nested operand in the contract.as\_(“qty”)).where((receipt\_item.docstatus equals 1 bitwise and (nested operand in the ….
- If not rows.
  - Return tuple(0.0, 0.0).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set taken\_qty from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract(nested operand i … at 0.
  - Draw d from rows.
- Return tuple(sum(generator of flt(d.qty) for d drawn from rows), flt(taken\_qty)).
  - Draw d from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1044) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L284)

<a id="op-426926759721a9"></a>
### Buying Controller.get posted qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_posted_qty`

**Inputs** self, voucher\_detail\_no, warehouse, outward.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → voucher\_detail\_no, “warehouse” → warehouse, “is\_cancelled” → 0, “actual\_qty” → tuple(“&lt;”, 0) when outward, otherwise tuple(“&gt;”, 0)) ….

**Local steps**

- Return Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → voucher\_detail\_no, “warehouse” → warehouse, “is\_cancelled” → 0, “actual\_qty” → tuple(“&lt;”, 0) when outward, otherwise tuple(“&gt;”, 0)) ….
  - Value choice on outward — true gives tuple(“&lt;”, 0), false gives tuple(“&gt;”, 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1046) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L286)

<a id="op-6d0bd7d86356a4"></a>
### Buying Controller.get received stock qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_received_stock_qty`

**Inputs** self, row, accepted\_qty.

**Explicit results** accepted\_qty · get\_stock\_qty(row, (flt(row.qty) + flt(row.rejected\_qty))).

**Local steps**

- If not self.has\_rejected\_stock(row).
  - Return accepted\_qty.
- If (row.get(“serial\_and\_batch\_bundle”) and not row.get(“rejected\_serial\_and\_batch\_bundle”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“serial\_and\_batch\_bundle”) → not row.get(“rejected\_serial\_and\_batch\_bundle”).
  - Return accepted\_qty.
- Return get\_stock\_qty(row, (flt(row.qty) + flt(row.rejected\_qty))).

**Methods declared on this owner** [has rejected stock](operations-013.md#op-7619219c6072c9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1051) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L291)

<a id="op-a5566fe049aad7"></a>
### Buying Controller.get accepted warehouse package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_accepted_warehouse_package`

**Inputs** self, row, type\_of\_transaction, via\_landed\_cost\_voucher.

**Explicit results** row.serial\_and\_batch\_bundle · self.get\_package\_for\_target\_warehouse(row, type\_of\_transaction = type\_of\_transaction, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).

**Local steps**

- If (self.has\_rejected\_stock(row) and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_rejected\_stock(row) → not self.is\_return.
  - Return row.serial\_and\_batch\_bundle.
- If (self.is\_internal\_transfer() and not self.is\_return and self.docstatus differs from 2).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → not self.is\_return → self.docstatus differs from 2.
  - Return self.get\_package\_for\_target\_warehouse(row, type\_of\_transaction = type\_of\_transaction, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).
- Return row.serial\_and\_batch\_bundle.

**Methods declared on this owner** [has rejected stock](operations-013.md#op-7619219c6072c9), [get package for target warehouse](operations-014.md#op-21788b9431aeee).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1036) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L276)
