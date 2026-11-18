# Shared transaction rules · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Buying controller

<a id="op-c3e0ab01f83f40"></a>
### Buying Controller.set rate for standalone debit note

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_rate_for_standalone_debit_note`

**Inputs** self.

**Local steps**

- If (self.get(“is\_return”) and self.get(“update\_stock”) and not self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → self.get(“update\_stock”) → not self.return\_against.
  - For each row in self.items.
    - If row.rate ≤ 0.
      - Set row.rate from \_get\_incoming\_rate(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “posting\_date” → self.get(“posting\_date”), “posting\_time” → self.get(“posting\_time”), …), raise\_error\_if\_no\_rate = false).
      - Set row.discount\_percentage from 0.0.
      - Set row.discount\_amount from 0.0.
      - Set row.margin\_rate\_or\_amount from 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L432)

<a id="op-2c9ecf20bbb56a"></a>
### Buying Controller.set missing values

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_missing_values`

**Inputs** self, for\_validate = false.

**Local steps**

- Evaluate super().set\_missing\_values(for\_validate).
- Evaluate self.set\_supplier\_from\_item\_default().
- Evaluate self.set\_price\_list\_currency(“Buying”).
- If getattr(self, “supplier”, no value).
  - Evaluate self.update\_if\_missing(\_get\_party\_details(self.supplier, party\_type = “Supplier”, doctype = self.doctype, company = self.company, party\_address = self.get(“supplier\_address”), …)).
- Evaluate self.set\_missing\_item\_details(for\_validate).
- If (self.doctype equals “Purchase Receipt” or self.get(“update\_stock”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → self.get(“update\_stock”).
  - Bind dependencies ReturnChargesService.
  - Evaluate ReturnChargesService(self).set\_returned\_valuation\_charges().
- If self.meta.get\_field(“taxes”).
  - If (self.get(“taxes\_and\_charges”) and not self.get(“taxes”) and not for\_validate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“taxes\_and\_charges”) → not self.get(“taxes”) → not for\_validate.
    - Set taxes from \_get\_taxes\_and\_charges(“Purchase Taxes and Charges Template”, self.taxes\_and\_charges).
    - For each tax in taxes.
      - Evaluate self.append(“taxes”, tax).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set supplier from item default](operations-012.md#op-691fdf830c979f).

**Values supplied outside this operation** selected callable from getattr(self, “supplier”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L430)

<a id="op-79f0a3e850fceb"></a>
### Buying Controller.set transaction date exchange rate

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_set_transaction_date_exchange_rate`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not (self.currency and Platform.db.get\_single\_value(“Buying Settings”, “use\_transaction\_date\_exchange\_rate”) and not any(generator of (nested operand in the contract(nested operand in the contract) or nested o ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency → Platform.db.get\_single\_value(“Buying Settings”, “use\_transaction\_date\_exchange\_rate”) → not any(generator of (item.get(“purchase\_receipt”) or item.get(“purchase\_invoice”)) for item drawn from self.items).
  - Draw item from self.items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“purchase\_receipt”) → item.get(“purchase\_invoice”).
  - Return no value.
- Set self.use\_transaction\_date\_exchange\_rate from 1.
- Set self.conversion\_rate from get\_exchange\_rate(self.currency, self.company\_currency, self.posting\_date, “for\_buying”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “use\_transaction\_date\_exchange\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1067) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L307)

<a id="op-691fdf830c979f"></a>
### Buying Controller.set supplier from item default

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_supplier_from_item_default`

**Inputs** self.

**Record and data access** read “Item Default” via get\_value · read “Item” via get\_value.

**Local steps**

- If (self.meta.get\_field(“supplier”) and not self.supplier).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(“supplier”) → not self.supplier.
  - For each d in self.get(“items”).
    - Set supplier from Platform.db.get\_value(“Item Default”, mapping(“parent” → d.item\_code, “company” → self.company), “default\_supplier”).
    - If supplier.
      - Set self.supplier from supplier.
    - Otherwise.
      - Set item\_group from Platform.db.get\_value(“Item”, d.item\_code, “item\_group”).
      - Set supplier from Platform.db.get\_value(“Item Default”, mapping(“parent” → item\_group, “company” → self.company), “default\_supplier”).
      - If supplier.
        - Set self.supplier from supplier.
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L631) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L435)

<a id="op-015fe9ad21d130"></a>
### Buying Controller.validate stock or nonstock items

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_stock_or_nonstock_items`

**Inputs** self.

**Local steps**

- If (self.meta.get\_field(“taxes”) and not self.get\_stock\_items() and not self.get\_asset\_items()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(“taxes”) → not self.get\_stock\_items() → not self.get\_asset\_items().
  - Set msg from translated “Tax Category has been changed to "Total" because all the Items are non-stock items”.
  - Evaluate self.update\_tax\_category(msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get asset items](operations-012.md#op-84a2b4acb31810), [update tax category](operations-012.md#op-451c3504eeb7c3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L1042) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L454)

<a id="op-6ad3e58515b45a"></a>
### Buying Controller.validate deduct with valuation taxes

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_validate_deduct_with_valuation_taxes`

**Inputs** self.

**Local steps**

- Set taxes from list of tax for tax drawn from (self.get(“taxes”) or list()) where is\_deduct\_with\_valuation(tax).
  - Draw tax from (self.get(“taxes”) or list()), keep a combination only if (is\_deduct\_with\_valuation(tax)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“taxes”) → list().
- If taxes.
  - Evaluate validate\_deduct\_with\_valuation\_category(taxes, self.get\_deduct\_with\_valuation\_heads\_from\_source()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get deduct with valuation heads from source](operations-012.md#op-fb176c7abd82b8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1070) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L310)

<a id="op-b5008048137cce"></a>
### Buying Controller.get deduct with valuation source names

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_deduct_with_valuation_source_names`

**Inputs** self.

**Declared result** set.

**Record and data access** read “Auto Repeat” via get\_value.

**Explicit results** (source\_names − set(no value, empty text)).

**Local steps**

- Set source\_fields from tuple(“purchase\_order”, “purchase\_receipt”, “purchase\_invoice”, “supplier\_quotation”).
- Set source\_names from set of item.get(field) for item drawn from self.get(“items”), then field drawn from source\_fields.
  - Draw item from self.get(“items”).
  - Draw field from source\_fields.
- Evaluate source\_names.update(tuple(self.get(“amended\_from”), self.get(“return\_against”))).
- If self.get(“auto\_repeat”).
  - Evaluate source\_names.add(Platform.db.get\_value(“Auto Repeat”, self.auto\_repeat, “reference\_document”)).
- Return (source\_names − set(no value, empty text)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1041) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L281)

<a id="op-fb176c7abd82b8"></a>
### Buying Controller.get deduct with valuation heads from source

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_deduct_with_valuation_heads_from_source`

**Inputs** self.

**Declared result** set.

**Explicit results** set() · set(account\_heads).

**Local steps**

- Set source\_names from self.get\_deduct\_with\_valuation\_source\_names().
- If not source\_names.
  - Return set().
- Set taxes from Platform.qb.DocType(“Purchase Taxes and Charges”).
- Set account\_heads from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract differs from nes ….
- Return set(account\_heads).

**Methods declared on this owner** [get deduct with valuation source names](operations-012.md#op-b5008048137cce).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1040) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L280)

<a id="op-451c3504eeb7c3"></a>
### Buying Controller.update tax category

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_update_tax_category`

**Inputs** self, msg.

**Local steps**

- Set tax\_for\_valuation from list of d for d drawn from self.get(“taxes”) where d.category belongs to list(“Valuation”, “Valuation and Total”).
  - Draw d from self.get(“taxes”), keep a combination only if (d.category belongs to list(“Valuation”, “Valuation and Total”)).
- If tax\_for\_valuation.
  - For each d in tax\_for\_valuation.
    - Set d.category from “Total”.
  - Evaluate msgprint(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L1207) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L442)

<a id="op-f6182ed95ebe7a"></a>
### Buying Controller.validate asset return

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_asset_return`

**Inputs** self.

**Record and data access** read “Asset” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} has submitted assets linked to it. You need to cancel the assets to create purchase return.”.format(self.return\_against).

**Local steps**

- If (self.doctype does not belong to list(“Purchase Receipt”, “Purchase Invoice”) or not self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype does not belong to list(“Purchase Receipt”, “Purchase Invoice”) → not self.is\_return.
  - Return no value.
- Set purchase\_doc\_field from “purchase\_receipt” when self.doctype equals “Purchase Receipt”, otherwise “purchase\_invoice”.
  - Value choice on self.doctype equals “Purchase Receipt” — true gives “purchase\_receipt”, false gives “purchase\_invoice”.
- Set detail\_field from (purchase\_doc\_field + “\_item”).
- Set asset\_filters from mapping(purchase\_doc\_field → self.return\_against, “docstatus” → 1).
- If ((self.doctype equals “Purchase Receipt” or self.get(“update\_stock”)) and all(generator of row.get(detail\_field) for row drawn from self.items where row.is\_fixed\_asset)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.doctype equals “Purchase Receipt” or self.get(“update\_stock”)) → all(generator of row.get(detail\_field) for row drawn from self.items where row.is\_fixed\_asset).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → self.get(“update\_stock”).
  - Draw row from self.items, keep a combination only if (row.is\_fixed\_asset).
  - Set asset\_filters at detail\_field from tuple(“is”, “not set”).
- If (self.return\_against and Platform.db.exists(“Asset”, asset\_filters)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.return\_against → Platform.db.exists(“Asset”, asset\_filters).
  - Call the validation error handler Platform.throw(translated “{0} has submitted assets linked to it. You need to cancel the assets to create purchase return.”.format(self.return\_against), title = translated “Not Allowed”).
- Evaluate self.validate\_assets\_left\_after\_return().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate assets left after return](operations-012.md#op-92de57b42cfeea).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L446)

<a id="op-92de57b42cfeea"></a>
### Buying Controller.validate assets left after return

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_validate_assets_left_after_return`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: {1} assets of {2} are linked to {3}, which keeps only {4} after this return. Cancel the extra subm …”.format(rows at detail.idx, flt(asset\_qty), Platform.bold(rows at detail.item\_code ….

**Local steps**

- If (self.doctype equals “Purchase Invoice” and not self.get(“update\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → not self.get(“update\_stock”).
  - Return no value.
- Set detail\_field from “purchase\_receipt\_item” when self.doctype equals “Purchase Receipt”, otherwise “purchase\_invoice\_item”.
  - Value choice on self.doctype equals “Purchase Receipt” — true gives “purchase\_receipt\_item”, false gives “purchase\_invoice\_item”.
- Set tuple(returned\_qty, rows) from self.get\_returned\_asset\_qty(detail\_field).
- If not returned\_qty.
  - Return no value.
- Set kept\_qty from self.get\_qty\_kept\_after\_return(detail\_field, returned\_qty).
- For each tuple(detail, asset\_qty) in get\_linked\_asset\_qty(detail\_field, list(returned\_qty)).items().
  - If flt(asset\_qty) &gt; kept\_qty at detail.
    - Call the validation error handler Platform.throw(translated “Row #{0}: {1} assets of {2} are linked to {3}, which keeps only {4} after this return. Cancel the extra subm …”.format(rows at detail.idx, flt(asset\_qty), Platform.bold(rows at d ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get returned asset qty](operations-012.md#op-a739ddb6b8b106), [get qty kept after return](operations-012.md#op-1721962d4f06f0).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1069) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L309)

<a id="op-a739ddb6b8b106"></a>
### Buying Controller.get returned asset qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_returned_asset_qty`

**Inputs** self, detail\_field.

**Explicit results** tuple(returned\_qty, rows).

**Local steps**

- Set tuple(returned\_qty, rows) from tuple(mapping(), mapping()).
- For each d in self.items.
  - If (d.is\_fixed\_asset and d.get(detail\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_fixed\_asset → d.get(detail\_field).
    - Set returned\_qty at d.get(detail\_field) from (returned\_qty.get(d.get(detail\_field), 0) + abs(flt(d.qty))).
    - Evaluate rows.setdefault(d.get(detail\_field), d).
- Return tuple(returned\_qty, rows).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1054) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L294)

<a id="op-1721962d4f06f0"></a>
### Buying Controller.get qty kept after return

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_qty_kept_after_return`

**Inputs** self, detail\_field, returned\_qty.

**Record and data access** read item\_doctype via get\_all.

**Explicit results** mapping of detail → (flt(kept\_qty.get(detail)) − qty) for tuple(detail, qty) drawn from returned\_qty.items().

**Local steps**

- Set item\_doctype from formatted text {self.doctype} Item.
- Set kept\_qty from dict(Platform.get\_all(item\_doctype, filters = mapping(“name” → tuple(“in”, list(returned\_qty))), fields = list(“name”, “qty”), as\_list = 1)).
- Set tuple(parent, child) from tuple(Platform.qb.DocType(self.doctype), Platform.qb.DocType(item\_doctype)).
- Set earlier\_returns from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….run().
- For each tuple(detail, qty) in earlier\_returns.
  - Set kept\_qty at detail from (flt(kept\_qty.get(detail)) − flt(qty)).
- Return mapping of detail → (flt(kept\_qty.get(detail)) − qty) for tuple(detail, qty) drawn from returned\_qty.items().
  - Draw tuple(detail, qty) from returned\_qty.items().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1047) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L287)

<a id="op-84a2b4acb31810"></a>
### Buying Controller.get asset items

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_get_asset_items`

**Inputs** self.

**Explicit results** list() · list of d.item\_code for d drawn from self.items where d.is\_fixed\_asset.

**Local steps**

- If self.doctype does not belong to list(“Purchase Order”, “Purchase Invoice”, “Purchase Receipt”).
  - Return list().
- Return list of d.item\_code for d drawn from self.items where d.is\_fixed\_asset.
  - Draw d from self.items, keep a combination only if (d.is\_fixed\_asset).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L1791) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L417)

<a id="op-106884628087fb"></a>
### Buying Controller.validate from warehouse

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_from_warehouse`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{idx}: {from\_warehouse\_field} and {to\_warehouse\_field} cannot be same.”.format(idx = item.idx, from\_warehouse\_field = translated item.meta.get\_label(“from\_warehouse”), to\_warehouse\_field = … · validation helper — translated “Row #{idx}: Cannot select Supplier Warehouse while suppling raw materials to subcontractor.”.format(idx = item.idx).

**Local steps**

- For each item in self.get(“items”).
  - If (item.get(“from\_warehouse”) and item.get(“from\_warehouse”) equals item.get(“warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“from\_warehouse”) → item.get(“from\_warehouse”) equals item.get(“warehouse”).
    - Call the validation error handler Platform.throw(translated “Row #{idx}: {from\_warehouse\_field} and {to\_warehouse\_field} cannot be same.”.format(idx = item.idx, from\_warehouse\_field = translated item.meta.get\_label(“from\_warehouse”), to\_wa ….
  - If (item.get(“from\_warehouse”) and self.get(“is\_subcontracted”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“from\_warehouse”) → self.get(“is\_subcontracted”).
    - Call the validation error handler Platform.throw(translated “Row #{idx}: Cannot select Supplier Warehouse while suppling raw materials to subcontractor.”.format(idx = item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L448)

<a id="op-993535efe00882"></a>
### Buying Controller.set supplier address

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_supplier_address`

**Inputs** self.

**Local steps**

- Set address\_dict from mapping(“supplier\_address” → “address\_display”, “shipping\_address” → “shipping\_address\_display”, “dispatch\_address” → “dispatch\_address\_display”, “billing\_address” → “billing\_address\_display”).
- For each tuple(address\_field, address\_display\_field) in address\_dict.items().
  - If self.get(address\_field).
    - Evaluate self.set(address\_display\_field, render\_address(self.get(address\_field), check\_permissions = false)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L2341) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L434)

<a id="op-47b3124b7705ca"></a>
### Buying Controller.get validated purchase expense details

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_get_validated_purchase_expense_details`

**Inputs** self, item\_code.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** details.

**Explicit failure paths** validation helper — translated “Please set {0} in Company {1} or in the Item Defaults of Item {2}”.format(Platform.bold(translated Platform.unscrub(field)), self.company, item\_code).

**Local steps**

- Set fields from tuple(“purchase\_expense\_account”, “purchase\_expense\_contra\_account”).
- Set details from get\_purchase\_expense\_account(item\_code, self.company).
- For each field in fields.
  - If not details.get(field).
    - Set details at field from Platform.get\_cached\_value(“Company”, self.company, field).
- For each field in fields.
  - If not details.get(field).
    - Call the validation error handler Platform.throw(translated “Please set {0} in Company {1} or in the Item Defaults of Item {2}”.format(Platform.bold(translated Platform.unscrub(field)), self.company, item\_code)).
- Return details.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L2599) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L422)

<a id="op-15d89838cac18c"></a>
### Buying Controller.set gl entry for purchase expense

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_general_ledger_entry_for_purchase_expense`

**Inputs** self, gl\_entries.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Account” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not cint(Platform.db.get\_single\_value(“Accounts Settings”, “book\_stock\_expense\_gl\_entries”)).
  - Return no value.
- If (self.doctype equals “Purchase Invoice” and not self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → not self.update\_stock.
  - Return no value.
- Set stock\_items from self.get\_stock\_items().
- For each row in self.items.
  - If row.item\_code does not belong to stock\_items.
    - Continue with the next iteration or loop test.
  - Set details from self.get\_validated\_purchase\_expense\_details(row.item\_code).
  - If not details.
    - Continue with the next iteration or loop test.
  - Set amount from flt((row.valuation\_rate × row.stock\_qty), row.precision(“base\_amount”)).
  - If row.landed\_cost\_voucher\_amount.
    - Update amount using − flt(row.landed\_cost\_voucher\_amount, row.precision(“base\_amount”)).
  - If not amount.
    - Continue with the next iteration or loop test.
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = details.purchase\_expense\_account, cost\_center = row.cost\_center, debit = amount, …).
  - Evaluate self.add\_gl\_entry(gl\_entries = gl\_entries, account = details.purchase\_expense\_contra\_account, cost\_center = row.cost\_center, debit = 0.0, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get validated purchase expense details](operations-012.md#op-47b3124b7705ca).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “book\_stock\_expense\_gl\_entries”), Platform.get\_cached\_value(“Account”, details.purchase\_expense\_account, “account\_currency”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L2970) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L428)

<a id="op-3ea9ee09b06f38"></a>
### Buying Controller.set total in words

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_set_total_in_words`

**Inputs** self.

**Local steps**

- Bind dependencies money\_in\_words.
- If self.meta.get\_field(“base\_in\_words”).
  - If (self.meta.get\_field(“base\_rounded\_total”) and not self.is\_rounded\_total\_disabled()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(“base\_rounded\_total”) → not self.is\_rounded\_total\_disabled().
    - Set amount from abs(flt(self.base\_rounded\_total)).
  - Otherwise.
    - Set amount from abs(flt(self.base\_grand\_total)).
  - Set self.base\_in\_words from money\_in\_words(amount, self.company\_currency).
- If self.meta.get\_field(“in\_words”).
  - If (self.meta.get\_field(“rounded\_total”) and not self.is\_rounded\_total\_disabled()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(“rounded\_total”) → not self.is\_rounded\_total\_disabled().
    - Set amount from abs(flt(self.rounded\_total)).
  - Otherwise.
    - Set amount from abs(flt(self.grand\_total)).
  - Set self.in\_words from money\_in\_words(amount, self.currency).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0372.json#L3768) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L436)

<a id="op-a70f2c1e5a7dfa"></a>
### Buying Controller.update valuation rate

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_update_valuation_rate`

**Inputs** self, reset\_outgoing\_rate = true.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- Set stock\_and\_asset\_items from list().
- Set stock\_and\_asset\_items from (self.get\_stock\_items() + self.get\_asset\_items()).
- Set tuple(tax\_accounts, total\_valuation\_amount, all\_item\_charges, stock\_item\_charges) from self.get\_tax\_details().
- Set actual\_charge\_per\_item from self.distribute\_actual\_tax\_amount(stock\_and\_asset\_items, all\_item\_charges, stock\_item\_charges).
- Set last\_item\_idx from max(generator of d.idx for d drawn from self.get(“items”), default = 1).
  - Draw d from self.get(“items”).
- For each tuple(i, item) in enumerate(self.get(“items”)).
  - If (item.item\_code and (item.qty or item.get(“rejected\_qty”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code → (item.qty or item.get(“rejected\_qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.qty → item.get(“rejected\_qty”).
    - If i equals (last\_item\_idx − 1).
      - Set item\_tax\_amount from total\_valuation\_amount.
    - Otherwise.
      - Set item\_tax\_amount from self.get\_item\_tax\_amount(item, tax\_accounts).
      - Update total\_valuation\_amount using − item\_tax\_amount.
    - If item.item\_code does not belong to stock\_and\_asset\_items.
      - Set item.valuation\_rate from 0.0.
      - Continue with the next iteration or loop test.
    - Set item.item\_tax\_amount from flt((item\_tax\_amount + actual\_charge\_per\_item.get(item.idx, 0.0)), self.precision(“item\_tax\_amount”, item)).
    - Evaluate self.round\_floats\_in(item, do\_not\_round\_fields = list(“conversion\_factor”)).
    - If flt(item.conversion\_factor) equals 0.0.
      - Set item.conversion\_factor from (get\_conversion\_factor(item.item\_code, item.uom).get(“conversion\_factor”) or 1.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_conversion\_factor(item.item\_code, item.uom).get(“conversion\_factor”) → 1.0.
    - Set net\_rate from item.base\_net\_amount.
    - If item.sales\_incoming\_rate.
      - Set net\_rate from get\_transit\_amount(item, self.get\_internal\_transfer\_qty(item)).
    - If (not net\_rate and item.get(“rejected\_qty”) and Platform.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not net\_rate → item.get(“rejected\_qty”) → Platform.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).
      - Set net\_rate from (item.rejected\_qty × item.base\_net\_rate).
    - Set qty\_in\_stock\_uom from (self.get\_valued\_stock\_qty(item) or get\_stock\_qty(item, item.rejected\_qty) or (flt(item.qty) × flt(item.conversion\_factor))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_valued\_stock\_qty(item) → get\_stock\_qty(item, item.rejected\_qty) → (flt(item.qty) × flt(item.conversion\_factor)).
    - If self.get(“is\_old\_subcontracting\_flow”).
      - Set item.rm\_supp\_cost from self.get\_supplied\_items\_cost(item.name, reset\_outgoing\_rate).
      - Set item.valuation\_rate from ((((net\_rate + item.item\_tax\_amount) + item.rm\_supp\_cost) + flt(item.landed\_cost\_voucher\_amount)) ÷ qty\_in\_stock\_uom).
    - Otherwise.
      - Set item.valuation\_rate from ((((net\_rate + item.item\_tax\_amount) + flt(item.landed\_cost\_voucher\_amount)) + flt(item.get(“amount\_difference\_with\_purchase\_invoice”))) ÷ qty\_in\_stock\_uom).
  - Otherwise.
    - Set item.valuation\_rate from 0.0.
- Evaluate update\_regional\_item\_valuation\_rate(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get asset items](operations-012.md#op-84a2b4acb31810), [get tax details](operations-012.md#op-20170300f75616), [distribute actual tax amount](operations-013.md#op-0df5b030c2ab5a), [get item tax amount](operations-012.md#op-898e1a310a81af), [get internal transfer qty](operations-013.md#op-46d9cccbba42e7), [get valued stock qty](operations-012.md#op-7fc11c66a16530).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L443)

<a id="op-82ec83dc6384d7"></a>
### Buying Controller.get rejected valuation rate

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_rejected_valuation_rate`

**Inputs** self, row.

**Declared result** float.

**Explicit results** 0.0 · flt(row.valuation\_rate) · (flt(row.base\_net\_rate) ÷ (flt(row.conversion\_factor) or 1.0)).

**Local steps**

- If not is\_rejected\_material\_valued(self.doctype, row.name).
  - Return 0.0.
- If (self.is\_internal\_transfer() or not flt(row.qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_internal\_transfer() → not flt(row.qty).
  - Return flt(row.valuation\_rate).
- Return (flt(row.base\_net\_rate) ÷ (flt(row.conversion\_factor) or 1.0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.conversion\_factor) → 1.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1053) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L293)

<a id="op-7fc11c66a16530"></a>
### Buying Controller.get valued stock qty

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_valued_stock_qty`

**Inputs** self, row.

**Explicit results** get\_stock\_qty(row, row.qty) · (get\_stock\_qty(row, row.qty) + get\_stock\_qty(row, row.rejected\_qty)).

**Local steps**

- If (not flt(row.get(“rejected\_qty”)) or not bills\_rejected\_quantity(self)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not flt(row.get(“rejected\_qty”)) → not bills\_rejected\_quantity(self).
  - Return get\_stock\_qty(row, row.qty).
- Return (get\_stock\_qty(row, row.qty) + get\_stock\_qty(row, row.rejected\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1061) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L301)

<a id="op-20170300f75616"></a>
### Buying Controller.get tax details

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_get_tax_details`

**Inputs** self.

**Explicit results** tuple(tax\_accounts, total\_valuation\_amount, all\_item\_charges, stock\_item\_charges).

**Local steps**

- Set tax\_accounts from list().
- Set total\_valuation\_amount from 0.0.
- Set all\_item\_charges from list().
- Set stock\_item\_charges from list().
- For each d in self.get(“taxes”).
  - If d.category does not belong to list(“Valuation”, “Valuation and Total”).
    - Continue with the next iteration or loop test.
  - Set multiplier from negative 1 when d.get(“add\_deduct\_tax”) equals “Deduct”, otherwise 1.
    - Value choice on d.get(“add\_deduct\_tax”) equals “Deduct” — true gives negative 1, false gives 1.
  - Set amount from (flt(d.base\_tax\_amount\_after\_discount\_amount) × multiplier).
  - If d.charge\_type equals “On Net Total”.
    - Update total\_valuation\_amount using + amount.
    - Evaluate tax\_accounts.append(tuple(d.account\_head, multiplier)).
  - Otherwise.
    - If (d.charge\_type equals “Actual” and d.get(“allocate\_full\_amount\_to\_stock\_items”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.charge\_type equals “Actual” → d.get(“allocate\_full\_amount\_to\_stock\_items”).
      - Evaluate stock\_item\_charges.append(amount).
    - Otherwise.
      - If d.charge\_type differs from “On Item Quantity”.
        - Evaluate all\_item\_charges.append(amount).
- Return tuple(tax\_accounts, total\_valuation\_amount, all\_item\_charges, stock\_item\_charges).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L421)

<a id="op-898e1a310a81af"></a>
### Buying Controller.get item tax amount

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_get_item_tax_amount`

**Inputs** self, item, tax\_accounts.

**Explicit results** item\_tax\_amount.

**Local steps**

- Set item\_tax\_amount from 0.0.
- If item.item\_tax\_rate.
  - Set tax\_details from json.loads(item.item\_tax\_rate).
  - For each tuple(account, multiplier) in tax\_accounts.
    - Set rate from tax\_details.get(account, 0).
    - If rate equals NOT\_APPLICABLE\_TAX.
      - Continue with the next iteration or loop test.
    - Set net\_rate from item.base\_net\_amount.
    - If item.sales\_incoming\_rate.
      - Set net\_rate from (item.qty × item.sales\_incoming\_rate).
    - Update item\_tax\_amount using + (((flt(net\_rate) × flt(rate)) ÷ 100) × multiplier).
- Return item\_tax\_amount.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L419)
