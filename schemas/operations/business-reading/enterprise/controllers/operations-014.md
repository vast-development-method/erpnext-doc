# Shared transaction rules · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Buying controller

<a id="op-9c0d0cc37040ea"></a>
### Buying Controller.get submitted package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_submitted_package`

**Inputs** self, row, warehouse.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → row.name, “warehouse” → warehouse, “is\_cancelled” → 0), “serial\_and\_batch\_bundle”).

**Local steps**

- Return Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → row.name, “warehouse” → warehouse, “is\_cancelled” → 0), “serial\_and\_batch\_bundle”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1059) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L299)

<a id="op-e843fd92925cdb"></a>
### Buying Controller.get source warehouse reversal package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_source_warehouse_reversal_package`

**Inputs** self, row, package, source\_qty.

**Explicit results** package · existing\_package · self.get\_package\_for\_target\_warehouse(row, row.from\_warehouse, “Inward”) · self.get\_returned\_source\_package(row, source\_qty).

**Local steps**

- If not (self.is\_internal\_transfer() and self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → self.is\_return.
  - Return package.
- If existing\_package bound to self.get\_package\_of\_source\_warehouse(row).
  - Return existing\_package.
- If not row.get(“rejected\_serial\_and\_batch\_bundle”).
  - Return self.get\_package\_for\_target\_warehouse(row, row.from\_warehouse, “Inward”).
- Return self.get\_returned\_source\_package(row, source\_qty).

**Methods declared on this owner** [get package of source warehouse](operations-014.md#op-38b8c1e89cb47c), [get package for target warehouse](operations-014.md#op-21788b9431aeee), [get returned source package](operations-014.md#op-ea37470cdb54b9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1058) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L298)

<a id="op-096b36f960e31a"></a>
### Buying Controller.get source warehouse package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_source_warehouse_package`

**Inputs** self, row, package, source\_qty.

**Explicit results** package · existing\_package · self.make\_package\_for\_transfer(row.rejected\_serial\_and\_batch\_bundle, row.from\_warehouse, type\_of\_transaction = “Outward”) · self.make\_package\_for\_transfer(package, row.from\_warehouse, type\_of\_transaction = “Outward”, include\_bundle = row.rejected\_serial\_and\_batch\_bundle, total\_qty = source\_qty).

**Local steps**

- If not (row.get(“rejected\_serial\_and\_batch\_bundle”) and self.is\_internal\_receipt()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“rejected\_serial\_and\_batch\_bundle”) → self.is\_internal\_receipt().
  - Return package.
- If existing\_package bound to self.get\_package\_of\_source\_warehouse(row).
  - Return existing\_package.
- If not package.
  - Return self.make\_package\_for\_transfer(row.rejected\_serial\_and\_batch\_bundle, row.from\_warehouse, type\_of\_transaction = “Outward”).
- Return self.make\_package\_for\_transfer(package, row.from\_warehouse, type\_of\_transaction = “Outward”, include\_bundle = row.rejected\_serial\_and\_batch\_bundle, total\_qty = source\_qty).

**Methods declared on this owner** [is internal receipt](operations-013.md#op-df2f3b164c398c), [get package of source warehouse](operations-014.md#op-38b8c1e89cb47c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1056) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L296)

<a id="op-38b8c1e89cb47c"></a>
### Buying Controller.get package of source warehouse

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_package_of_source_warehouse`

**Inputs** self, row.

**Declared result** (str bitwise or no value).

**Record and data access** read “Serial and Batch Bundle” via get\_value.

**Explicit results** Platform.db.get\_value(“Serial and Batch Bundle”, mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “voucher\_detail\_no” → row.name, “warehouse” → row.from\_warehouse, …), “name”).

**Local steps**

- Return Platform.db.get\_value(“Serial and Batch Bundle”, mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “voucher\_detail\_no” → row.name, “warehouse” → row.from\_warehouse, …), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1045) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L285)

<a id="op-ea37470cdb54b9"></a>
### Buying Controller.get returned source package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_returned_source_package`

**Inputs** self, row, source\_qty.

**Explicit results** self.make\_package\_for\_transfer(row.serial\_and\_batch\_bundle, row.from\_warehouse, type\_of\_transaction = “Inward”, include\_bundle = row.rejected\_serial\_and\_batch\_bundle, total\_qty = source\_qty).

**Local steps**

- Return self.make\_package\_for\_transfer(row.serial\_and\_batch\_bundle, row.from\_warehouse, type\_of\_transaction = “Inward”, include\_bundle = row.rejected\_serial\_and\_batch\_bundle, total\_qty = source\_qty).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1055) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L295)

<a id="op-a1e77e5ee37067"></a>
### Buying Controller.update stock ledger

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_update_stock_ledger`

**Inputs** self, allow\_negative\_stock = false, via\_landed\_cost\_voucher = false.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Local steps**

- Evaluate self.update\_ordered\_and\_reserved\_qty().
- Set sl\_entries from list().
- Set stock\_items from self.get\_stock\_items().
- For each d in self.get(“items”).
  - If d.item\_code does not belong to stock\_items.
    - Continue with the next iteration or loop test.
  - Set source\_reversal\_sle from no value.
  - Set pr\_qty from get\_stock\_qty(d, d.qty).
  - Set source\_qty from self.get\_source\_warehouse\_qty(d, pr\_qty).
  - If (source\_qty and (d.warehouse or not pr\_qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_qty → (d.warehouse or not pr\_qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.warehouse → not pr\_qty.
    - If (d.from\_warehouse and ((not cint(self.is\_return) and self.docstatus equals 1) or (cint(self.is\_return) and self.docstatus equals 2))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.from\_warehouse → ((not cint(self.is\_return) and self.docstatus equals 1) or (cint(self.is\_return) and self.docstatus equals 2)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not cint(self.is\_return) and self.docstatus equals 1) → (cint(self.is\_return) and self.docstatus equals 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.is\_return) → self.docstatus equals 1.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.docstatus equals 2.
      - Set serial\_and\_batch\_bundle from d.get(“serial\_and\_batch\_bundle”).
      - If (self.is\_internal\_transfer() and self.is\_return and self.docstatus equals 2).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → self.is\_return → self.docstatus equals 2.
        - Set serial\_and\_batch\_bundle from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → d.name, “warehouse” → d.from\_warehouse), “serial\_and\_batch\_bundle”).
      - Set from\_warehouse\_sle from self.get\_sl\_entries(d, mapping(“actual\_qty” → (negative 1 × source\_qty), “warehouse” → d.from\_warehouse, “outgoing\_rate” → d.rate, “recalculate\_rate” → 1, …)).
      - Evaluate sl\_entries.append(from\_warehouse\_sle).
    - Set type\_of\_transaction from “Inward”.
    - If self.docstatus equals 2.
      - Set type\_of\_transaction from “Outward”.
    - Set sle from self.get\_sl\_entries(d, mapping(“actual\_qty” → flt(pr\_qty), “serial\_and\_batch\_bundle” → self.get\_accepted\_warehouse\_package(d, type\_of\_transaction, via\_landed\_cost\_voucher))).
    - If self.is\_return.
      - Set outgoing\_rate from 0.0.
      - If not is\_serial\_no\_wise\_valuation\_disabled(d.item\_code).
        - Set outgoing\_rate from get\_rate\_for\_return(self.doctype, self.name, d.item\_code, self.return\_against, item\_row = d).
      - Evaluate sle.update(mapping(“outgoing\_rate” → outgoing\_rate, “recalculate\_rate” → 1, “serial\_and\_batch\_bundle” → d.serial\_and\_batch\_bundle)).
      - If d.from\_warehouse.
        - Set sle.dependant\_sle\_voucher\_detail\_no from d.name.
    - Otherwise.
      - Evaluate sle.update(mapping(“incoming\_rate” → d.valuation\_rate, “recalculate\_rate” → 1 when ((self.is\_subcontracted and (nested operand in the contract.bom or nested operand in the contract(nested operand in the co ….
        - Value choice on ((self.is\_subcontracted and (d.bom or d.get(“fg\_item”))) or d.from\_warehouse) — true gives 1, false gives 0.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.is\_subcontracted and (d.bom or d.get(“fg\_item”))) → d.from\_warehouse.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_subcontracted → (d.bom or d.get(“fg\_item”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.bom → d.get(“fg\_item”).
    - Evaluate sl\_entries.append(sle).
    - If (d.from\_warehouse and ((not cint(self.is\_return) and self.docstatus equals 2) or (cint(self.is\_return) and self.docstatus equals 1))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.from\_warehouse → ((not cint(self.is\_return) and self.docstatus equals 2) or (cint(self.is\_return) and self.docstatus equals 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not cint(self.is\_return) and self.docstatus equals 2) → (cint(self.is\_return) and self.docstatus equals 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.is\_return) → self.docstatus equals 2.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.docstatus equals 1.
      - Set serial\_and\_batch\_bundle from no value.
      - If (self.is\_internal\_transfer() and self.docstatus equals 2).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → self.docstatus equals 2.
        - Set reversed\_warehouse from d.from\_warehouse when d.get(“rejected\_serial\_and\_batch\_bundle”), otherwise d.warehouse.
          - Value choice on d.get(“rejected\_serial\_and\_batch\_bundle”) — true gives d.from\_warehouse, false gives d.warehouse.
        - Set serial\_and\_batch\_bundle from self.get\_submitted\_package(d, reversed\_warehouse).
      - Set from\_warehouse\_sle from self.get\_sl\_entries(d, mapping(“actual\_qty” → (negative 1 × source\_qty), “warehouse” → d.from\_warehouse, “recalculate\_rate” → 1, “serial\_and\_batch\_bundle” → self.get\_source\_warehouse\_reversal\_package(d, se ….
      - If (self.is\_internal\_transfer() and self.is\_return).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → self.is\_return.
        - Set from\_warehouse\_sle.incoming\_rate from get\_rate\_for\_return(self.doctype, self.name, d.item\_code, self.return\_against, item\_row = d).
      - Set source\_reversal\_sle from from\_warehouse\_sle.
  - If flt(d.rejected\_qty) differs from 0.
    - Set valuation\_rate\_for\_rejected\_item from self.get\_rejected\_valuation\_rate(d).
    - Evaluate sl\_entries.append(self.get\_sl\_entries(d, mapping(“warehouse” → d.rejected\_warehouse, “actual\_qty” → get\_stock\_qty(d, d.rejected\_qty), “incoming\_rate” → valuation\_rate\_for\_rejected\_item when not self.is\_ret ….
      - Value choice on not self.is\_return — true gives valuation\_rate\_for\_rejected\_item, false gives 0.0.
      - Value choice on self.is\_return — true gives valuation\_rate\_for\_rejected\_item, false gives 0.0.
  - If source\_reversal\_sle.
    - Evaluate sl\_entries.append(source\_reversal\_sle).
- If self.get(“is\_old\_subcontracting\_flow”).
  - Evaluate self.make\_sl\_entries\_for\_supplier\_warehouse(sl\_entries).
- Evaluate self.make\_sl\_entries(sl\_entries, allow\_negative\_stock = allow\_negative\_stock, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update ordered and reserved qty](operations-014.md#op-fdbc9194e3cfe8), [get source warehouse qty](operations-013.md#op-488a852092ff4d), [get source warehouse package](operations-014.md#op-096b36f960e31a), [get accepted warehouse package](operations-013.md#op-a5566fe049aad7), [get submitted package](operations-014.md#op-9c0d0cc37040ea), [get source warehouse reversal package](operations-014.md#op-e843fd92925cdb), [get rejected valuation rate](operations-012.md#op-82ec83dc6384d7).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L441)

<a id="op-21788b9431aeee"></a>
### Buying Controller.get package for target warehouse

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_get_package_for_target_warehouse`

**Inputs** self, item, warehouse = no value, type\_of\_transaction = no value, via\_landed\_cost\_voucher = no value.

**Declared result** str.

**Record and data access** read “Serial and Batch Bundle” via get\_value.

**Explicit results** sabb · empty text · self.make\_package\_for\_transfer(item.serial\_and\_batch\_bundle, warehouse, type\_of\_transaction = type\_of\_transaction).

**Local steps**

- If (via\_landed\_cost\_voucher and item.get(“warehouse”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in via\_landed\_cost\_voucher → item.get(“warehouse”).
  - If sabb bound to Platform.db.get\_value(“Serial and Batch Bundle”, mapping(“voucher\_detail\_no” → item.name, “warehouse” → item.get(“warehouse”), “docstatus” → 1, “is\_cancelled” → 0), “name”).
    - Return sabb.
- If not item.serial\_and\_batch\_bundle.
  - Return empty text.
- If not warehouse.
  - Set warehouse from item.warehouse.
- Return self.make\_package\_for\_transfer(item.serial\_and\_batch\_bundle, warehouse, type\_of\_transaction = type\_of\_transaction).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0373.json#L5945) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L420)

<a id="op-20931e51204800"></a>
### Buying Controller.check purchase order on hold or close

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_check_purchase_order_on_hold_or_close`

**Inputs** self, ref\_fieldname, exclude\_if\_field = no value.

**Explicit results** no value.

**Local steps**

- If self.get(“is\_return”).
  - Return no value.
- Evaluate self.check\_for\_on\_hold\_or\_closed\_status(“Purchase Order”, ref\_fieldname, exclude\_if\_field = exclude\_if\_field).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0373.json#L6306) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L413)

<a id="op-fdbc9194e3cfe8"></a>
### Buying Controller.update ordered and reserved qty

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_update_ordered_and_reserved_quantity`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “{doctype} {name} is cancelled or closed.”.format(doctype = Platform.bold(translated “Purchase Order”), name = Platform.bold(po)).

**Local steps**

- Set po\_map from mapping().
- For each d in self.get(“items”).
  - If (self.doctype equals “Purchase Receipt” and d.purchase\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → d.purchase\_order.
    - Evaluate po\_map.setdefault(d.purchase\_order, list()).append(d.purchase\_order\_item).
  - Otherwise.
    - If (self.doctype equals “Purchase Invoice” and d.purchase\_order and d.po\_detail).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → d.purchase\_order → d.po\_detail.
      - Evaluate po\_map.setdefault(d.purchase\_order, list()).append(d.po\_detail).
- For each tuple(po, po\_item\_rows) in po\_map.items().
  - If (po and po\_item\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in po → po\_item\_rows.
    - Set po\_obj from Platform.get\_lazy\_doc(“Purchase Order”, po).
    - If (po\_obj.status equals “Cancelled” or (po\_obj.status equals “Closed” and not self.get(“is\_return”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in po\_obj.status equals “Cancelled” → (po\_obj.status equals “Closed” and not self.get(“is\_return”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in po\_obj.status equals “Closed” → not self.get(“is\_return”).
      - Call the validation error handler Platform.throw(translated “{doctype} {name} is cancelled or closed.”.format(doctype = Platform.bold(translated “Purchase Order”), name = Platform.bold(po)), Platform.InvalidStatusError).
    - Evaluate po\_obj.update\_ordered\_qty(po\_item\_rows).
    - If self.get(“is\_old\_subcontracting\_flow”).
      - Evaluate po\_obj.update\_reserved\_qty\_for\_subcontract().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L440)

<a id="op-ab7854ba986b88"></a>
### Buying Controller.on submit

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_on_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.get(“is\_return”).
  - Return no value.
- If self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”).
  - Evaluate self.process\_fixed\_asset().
- If self.doctype belongs to list(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”).
  - Evaluate update\_last\_purchase\_rate(self, is\_submit = 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [process fixed asset](operations-014.md#op-fb429a4fbcdbd9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L425)

<a id="op-0e6a33f07e6ba5"></a>
### Buying Controller.on cancel

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_on_cancel`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate super().on\_cancel().
- If self.get(“is\_return”).
  - Return no value.
- If self.doctype belongs to list(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”).
  - Evaluate update\_last\_purchase\_rate(self, is\_submit = 0).
- If self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”).
  - Set field from “purchase\_invoice” when self.doctype equals “Purchase Invoice”, otherwise “purchase\_receipt”.
    - Value choice on self.doctype equals “Purchase Invoice” — true gives “purchase\_invoice”, false gives “purchase\_receipt”.
  - Evaluate self.delete\_linked\_asset().
  - Evaluate self.update\_fixed\_asset(field, delete\_asset = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete linked asset](operations-014.md#op-eea841079fb91c), [update fixed asset](operations-014.md#op-59ac917ef9bedc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L424)

<a id="op-187c2872c6b5cf"></a>
### Buying Controller.validate budget

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_budget`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- If not Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_budget\_controller”).
  - Bind dependencies BudgetValidation.
  - Set val from BudgetValidation(doc = self).
  - Evaluate val.validate().
- Otherwise.
  - If self.docstatus equals 1.
    - For each data in self.get(“items”).
      - Set args from data.as\_dict().
      - Evaluate args.update(mapping(“doctype” → self.doctype, “company” → self.company, “posting\_date” → self.schedule\_date when self.doctype equals “Material Request”, otherwise self.transaction\_date)).
        - Value choice on self.doctype equals “Material Request” — true gives self.schedule\_date, false gives self.transaction\_date.
      - Evaluate validate\_expense\_against\_budget(args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “use\_legacy\_budget\_controller”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0374.json#L1270) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L447)

<a id="op-fb429a4fbcdbd9"></a>
### Buying Controller.process fixed asset

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_process_fixed_asset`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.doctype equals “Purchase Invoice” and not self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → not self.update\_stock.
  - Return no value.
- Set asset\_items from self.get\_asset\_items().
- If asset\_items.
  - Evaluate self.auto\_make\_assets(asset\_items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get asset items](operations-012.md#op-84a2b4acb31810), [auto make assets](operations-014.md#op-4a18675a23a724).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0374.json#L1632) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L427)

<a id="op-4a18675a23a724"></a>
### Buying Controller.auto make assets

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_auto_make_assets`

**Inputs** self, asset\_items.

**State and service calls** msgprint with message.

**Explicit failure paths** validation helper — translated “Row {idx}: Asset Naming Series is mandatory for the auto creation of assets for item {item\_code}.”.format(idx = d.idx, item\_code = Platform.bold(d.item\_code)).

**Local steps**

- Set items\_data from get\_asset\_item\_details(asset\_items).
- Set messages from list().
- Set alert from false.
- Set accounting\_dimensions from get\_dimensions(with\_cost\_center\_and\_project = true).
- For each d in self.items.
  - If d.is\_fixed\_asset.
    - Set item\_data from items\_data.get(d.item\_code).
    - If item\_data.get(“auto\_create\_assets”).
      - If item\_data.get(“asset\_naming\_series”).
        - Set created\_assets from list().
        - If item\_data.get(“is\_grouped\_asset”).
          - Set asset from self.make\_asset(d, accounting\_dimensions, is\_grouped\_asset = true).
          - Evaluate created\_assets.append(asset).
        - Otherwise.
          - For each \_qty in range(cint(d.qty)).
            - Set asset from self.make\_asset(d, accounting\_dimensions).
            - Evaluate created\_assets.append(asset).
        - If len(created\_assets) &gt; 5.
          - Evaluate messages.append(translated “{count} Assets created for {item\_code}”.format(count = len(created\_assets), item\_code = Platform.bold(d.item\_code))).
        - Otherwise.
          - Set assets\_link from list(map(deferred anonymous expression, created\_assets)).
          - Set assets\_link from Platform.bold(“,”.join(assets\_link)).
          - If len(created\_assets) equals 1.
            - Set msg from translated “Asset {assets\_link} created for {item\_code}”.format(assets\_link = assets\_link, item\_code = Platform.bold(d.item\_code)).
          - Otherwise.
            - Set msg from translated “Assets {assets\_link} created for {item\_code}”.format(assets\_link = assets\_link, item\_code = Platform.bold(d.item\_code)).
          - Evaluate messages.append(msg).
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Row {idx}: Asset Naming Series is mandatory for the auto creation of assets for item {item\_code}.”.format(idx = d.idx, item\_code = Platform.bold(d.item\_code))).
    - Otherwise.
      - Evaluate messages.append(translated “Assets not created for {item\_code}. You will have to create asset manually.”.format(item\_code = Platform.bold(d.item\_code))).
      - Set alert from true.
- For each message in messages.
  - Evaluate Platform.msgprint(message, title = “Success”, indicator = “green”, alert = alert).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make asset](operations-014.md#op-565e6cb08cef45).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0374.json#L1779) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L412)

<a id="op-565e6cb08cef45"></a>
### Buying Controller.make asset

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_make_asset`

**Inputs** self, row, accounting\_dimensions, is\_grouped\_asset = false.

**Record and data access** read “Item” via get\_cached\_value · resolve a document from mapping(“doctype” → “Asset”, “item\_code” → row.item\_code, “asset\_name” → row.item\_name, “naming\_series” → (item\_data.get(“asset\_naming\_series”) or “AST”), …) via get\_doc.

**State and service calls** call db\_insert on asset.

**Explicit results** asset.name.

**Explicit failure paths** validation helper — translated “Row #{idx}: Please enter a location for the asset item {item\_code}.”.format(idx = row.idx, item\_code = Platform.bold(row.item\_code)).

**Local steps**

- If not row.asset\_location.
  - Call the validation error handler Platform.throw(translated “Row #{idx}: Please enter a location for the asset item {item\_code}.”.format(idx = row.idx, item\_code = Platform.bold(row.item\_code))).
- Set item\_data from Platform.get\_cached\_value(“Item”, row.item\_code, list(“asset\_naming\_series”, “asset\_category”), as\_dict = 1).
- Set asset\_quantity from row.qty when is\_grouped\_asset, otherwise 1.
  - Value choice on is\_grouped\_asset — true gives row.qty, false gives 1.
- Set purchase\_amount from ((flt(row.valuation\_rate) × flt((row.conversion\_factor or 1))) × asset\_quantity).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.conversion\_factor → 1.
- Set asset from Platform.get\_doc(mapping(“doctype” → “Asset”, “item\_code” → row.item\_code, “asset\_name” → row.item\_name, “naming\_series” → (item\_data.get(“asset\_naming\_series”) or “AST”), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_data.get(“asset\_naming\_series”) → “AST”.
  - Value choice on self.doctype equals “Purchase Receipt” — true gives self.name, false gives no value.
  - Value choice on self.doctype equals “Purchase Invoice” — true gives self.name, false gives no value.
  - Value choice on self.doctype equals “Purchase Receipt” — true gives row.name, false gives no value.
  - Value choice on self.doctype equals “Purchase Invoice” — true gives row.name, false gives no value.
- For each dimension in accounting\_dimensions at 0.
  - Set fieldname from dimension at “fieldname”.
  - Set default\_dimension from accounting\_dimensions at 1.get(self.company, mapping()).get(fieldname).
  - If not asset.get(fieldname).
    - Evaluate asset.update(mapping(fieldname → (row.get(fieldname) or self.get(fieldname) or default\_dimension))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(fieldname) → self.get(fieldname) → default\_dimension.
- Set asset.flags.ignore\_validate from true.
- Set asset.flags.ignore\_mandatory from true.
- Evaluate asset.set\_missing\_values().
- Evaluate asset.db\_insert().
- Return asset.name.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, list(“asset\_naming\_series”, “asset\_category”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L423)

<a id="op-59ac917ef9bedc"></a>
### Buying Controller.update fixed asset

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_update_fixed_asset`

**Inputs** self, field, delete\_asset = false.

**Record and data access** read “Item” via get\_value · read “Asset” via get\_all · resolve a document from “Asset” via get\_doc · execute query text (SELECT, Asset Movement).

**State and service calls** request delete\_doc for “Asset Movement” · request delete\_doc for “Asset” · call save on asset.

**Explicit failure paths** validation helper — translated “Cannot cancel this document as it is linked with the submitted asset {asset\_link}. Please cancel the asset t …”.format(asset\_link = Platform.utils.get\_link\_to\_form(“Asset”, asset.name)).

**Local steps**

- For each d in self.get(“items”).
  - If d.is\_fixed\_asset.
    - Set is\_auto\_create\_enabled from Platform.db.get\_value(“Item”, d.item\_code, “auto\_create\_assets”).
    - Set assets from Platform.db.get\_all(“Asset”, filters = mapping(field → self.name, “item\_code” → d.item\_code)).
    - For each asset in assets.
      - Set asset from Platform.get\_doc(“Asset”, asset.name).
      - If (delete\_asset and is\_auto\_create\_enabled).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in delete\_asset → is\_auto\_create\_enabled.
        - Set movements from Platform.db.sql(query text (SELECT, Asset Movement), asset.name, as\_dict = 1).
        - For each movement in movements.
          - Evaluate Platform.delete\_doc(“Asset Movement”, movement.name, force = 1).
        - Evaluate Platform.delete\_doc(“Asset”, asset.name, force = 1).
        - Continue with the next iteration or loop test.
      - If self.docstatus equals 2.
        - <a id="op-59ac917ef9bedc-guard-24"></a>If asset.docstatus equals 2.
          - Continue with the next iteration or loop test.
        - If asset.docstatus equals 0.
          - Evaluate asset.set(field, no value).
          - Set asset.supplier from no value.
        - If (asset.docstatus equals 1 and delete\_asset).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in asset.docstatus equals 1 → delete\_asset.
          - Call the validation error handler Platform.throw(translated “Cannot cancel this document as it is linked with the submitted asset {asset\_link}. Please cancel the asset t …”.format(asset\_link = Platform.utils.get\_link\_to\_form(“Asset”, asset.name))).
      - Set asset.flags.ignore\_validate\_update\_after\_submit from true.
      - Set asset.flags.ignore\_mandatory from true.
      - If asset.docstatus equals 0.
        - Set asset.flags.ignore\_validate from true.
      - Evaluate asset.save().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison asset.docstatus equals 2, asset.docstatus = 2 (cancelled) selects the branch that continues with the next loop iteration. With asset.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-59ac917ef9bedc-guard-24)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L439)

<a id="op-eea841079fb91c"></a>
### Buying Controller.delete linked asset

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_delete_linked_asset`

**Inputs** self.

**Record and data access** read “Asset Movement” via get\_value.

**State and service calls** request delete\_doc for “Asset Movement”.

**Explicit results** no value.

**Local steps**

- If (self.doctype equals “Purchase Invoice” and not self.get(“update\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → not self.get(“update\_stock”).
  - Return no value.
- Set asset\_movement from Platform.db.get\_value(“Asset Movement”, mapping(“reference\_name” → self.name), “name”).
- Evaluate Platform.delete\_doc(“Asset Movement”, asset\_movement, force = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0374.json#L5040) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L415)

<a id="op-369e5e21021eae"></a>
### Buying Controller.validate schedule date

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_schedule_date`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{idx}: {schedule\_date} cannot be before {transaction\_date}.”.format(idx = d.idx, schedule\_date = translated self.meta.get\_label(“schedule\_date”), transaction\_date = translated self.meta.ge … · validation helper — translated “Please enter the {schedule\_date}.”.format(schedule\_date = translated self.meta.get\_label(“schedule\_date”)).

**Local steps**

- If not self.get(“items”).
  - Return no value.
- If any(generator of d.schedule\_date for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
  - Set self.schedule\_date from min(generator of d.schedule\_date for d drawn from self.get(“items”) where d.schedule\_date is distinct from no value).
    - Draw d from self.get(“items”), keep a combination only if (d.schedule\_date is distinct from no value).
- If self.schedule\_date.
  - For each d in self.get(“items”).
    - If not d.schedule\_date.
      - Set d.schedule\_date from self.schedule\_date.
    - If (d.schedule\_date and self.transaction\_date and getdate(d.schedule\_date) &lt; getdate(self.transaction\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.schedule\_date → self.transaction\_date → getdate(d.schedule\_date) &lt; getdate(self.transaction\_date).
      - Call the validation error handler Platform.throw(translated “Row #{idx}: {schedule\_date} cannot be before {transaction\_date}.”.format(idx = d.idx, schedule\_date = translated self.meta.get\_label(“schedule\_date”), transaction\_date = translat ….
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Please enter the {schedule\_date}.”.format(schedule\_date = translated self.meta.get\_label(“schedule\_date”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L453)

<a id="op-d06f798f24a326"></a>
### Buying Controller.validate items

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_items`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.doctype equals “Material Request”.
  - Return no value.
- If self.get(“is\_old\_subcontracting\_flow”).
  - Evaluate validate\_item\_type(self, “is\_sub\_contracted\_item”, “subcontracted”).
- Otherwise.
  - Evaluate validate\_item\_type(self, “is\_purchase\_item”, “purchase”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L449)

<a id="op-d960679f16499b"></a>
### Get asset item details

`operation_enterprise_controllers_buying_controller_business_behavior_get_asset_item_details`

**Inputs** asset\_items.

**Record and data access** read “Item” via get\_all.

**Explicit results** asset\_items\_data.

**Local steps**

- Set asset\_items\_data from mapping().
- For each d in Platform.get\_all(“Item”, fields = list(“name”, “auto\_create\_assets”, “asset\_naming\_series”, “is\_grouped\_asset”), filters = mapping(“name” → tuple(“in”, asset\_items))).
  - Evaluate asset\_items\_data.setdefault(d.name, d).
- Return asset\_items\_data.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0374.json#L5975) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L455)

<a id="op-af2111eb1a97ba"></a>
### Validate item type

`operation_enterprise_controllers_buying_controller_business_behavior_validate_item_type`

**Inputs** doc, fieldname, message.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Explicit failure paths** validation helper — error\_message.

**Local steps**

- Set items from list of d.item\_code for d drawn from doc.items where d.item\_code.
  - Draw d from doc.items, keep a combination only if (d.item\_code).
- If not items.
  - Return no value.
- Set item\_list from “, ”.join(list of (“%s” modulo or format Platform.db.escape(d)) for d drawn from items).
  - Draw d from items.
- Set invalid\_items from list of d at 0 for d drawn from Platform.db.sql(formatted text   select item\_code from tabItem where name in ({item\_list}) and {fieldname}=0  , as\_list = true).
  - Draw d from Platform.db.sql(formatted text   select item\_code from tabItem where name in ({item\_list}) and {fieldname}=0  , as\_list = true).
- If invalid\_items.
  - Set items from “, ”.join(list of d for d drawn from invalid\_items).
    - Draw d from invalid\_items.
  - If len(invalid\_items) &gt; 1.
    - Set error\_message from translated “The items {items} are not marked as {type\_of} item. You can enable them as {type\_of} item from their Item masters.”.format(items = items, type\_of = message).
  - Otherwise.
    - Set error\_message from translated “The item {item} is not marked as {type\_of} item. You can enable it as {type\_of} item from its Item master.”.format(item = items, type\_of = message).
  - Call the validation error handler Platform.throw(error\_message).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L458)

<a id="op-cb12b42487a06a"></a>
### Update regional item valuation rate

`operation_enterprise_controllers_buying_controller_business_behavior_update_regional_item_valuation_rate`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0375.json#L455) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L457)

<a id="op-8bb48e8afbee9b"></a>
### Get linked asset qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_get_linked_asset_qty`

**Inputs** detail\_field, details, exclude\_asset = no value.

**Explicit results** dict(query.run()).

**Local steps**

- Set asset from Platform.qb.DocType(“Asset”).
- Set query from nested operand in the contract(nested operand in the contract).select(asset at detail\_field, Sum(nested operand in the contract.asset\_quantity)).where((nested operand in the contract at nested operand in t ….
- If exclude\_asset.
  - Set query from query.where(asset.name differs from exclude\_asset).
- Return dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1072) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L312)

<a id="op-d97f9865e00448"></a>
### Get purchase expense account

`operation_enterprise_controllers_buying_controller_business_behavior_get_purchase_expense_account`

**Inputs** item\_code, company.

**Wrappers, in declaration order** Platform.request\_cache.

**Explicit results** Platform.\_dict(mapping of field → details.get(field) for field drawn from tuple(“purchase\_expense\_account”, “purchase\_expense\_contra\_account”)).

**Local steps**

- Bind dependencies get\_brand\_defaults.
- Bind dependencies get\_item\_group\_defaults.
- Set defaults from get\_item\_defaults(item\_code, company).
- Set details from Platform.\_dict(mapping(“purchase\_expense\_account” → defaults.get(“purchase\_expense\_account”), “purchase\_expense\_contra\_account” → defaults.get(“purchase\_expense\_contra\_account”))).
- If not details.purchase\_expense\_account.
  - Set details from get\_item\_group\_defaults(item\_code, company).
- If not details.purchase\_expense\_account.
  - Set details from get\_brand\_defaults(item\_code, company).
- Return Platform.\_dict(mapping of field → details.get(field) for field drawn from tuple(“purchase\_expense\_account”, “purchase\_expense\_contra\_account”)).
  - Draw field from tuple(“purchase\_expense\_account”, “purchase\_expense\_contra\_account”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L456)
