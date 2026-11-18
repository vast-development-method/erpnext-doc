# Inventory and warehouses · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Price list

[Record definition](../../../../data/record-types/price_list.json)

<a id="op-a9c78b923b53f4"></a>
### Price List.delete price list details key

`operation_enterprise_stock_record_definitions_price_list_business_behavior_price_list_delete_price_list_details_key`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache().hdel(“price\_list\_details”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0773.json#L1311) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L179)

<a id="op-fe07ce57a4cfe1"></a>
### Get price list details

`operation_enterprise_stock_record_definitions_price_list_business_behavior_get_price_list_details`

**Inputs** price\_list.

**Record and data access** read “Price List” via get\_cached\_value.

**Explicit results** (price\_list\_details or mapping()).

**Local steps**

- Set price\_list\_details from Platform.cache().hget(“price\_list\_details”, price\_list).
- If not price\_list\_details.
  - Set price\_list\_details from Platform.get\_cached\_value(“Price List”, price\_list, list(“currency”, “price\_not\_uom\_dependent”, “enabled”), as\_dict = 1).
  - If (not price\_list\_details or not price\_list\_details.get(“enabled”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not price\_list\_details → not price\_list\_details.get(“enabled”).
    - Evaluate throw(translated “Price List {0} is disabled or does not exist”.format(price\_list)).
  - Evaluate Platform.cache().hset(“price\_list\_details”, price\_list, price\_list\_details).
- Return (price\_list\_details or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in price\_list\_details → mapping().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, list(“currency”, “price\_not\_uom\_dependent”, “enabled”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0773.json#L1391) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L177)

<a id="op-52e5841c2e79c0"></a>
### Is price list enabled

`operation_enterprise_stock_record_definitions_price_list_business_behavior_is_price_list_enabled`

**Inputs** price\_list.

**Declared result** bool.

**Record and data access** read “Price List” via get\_cached\_value.

**Explicit results** (bool(price\_list) and bool(Platform.get\_cached\_value(“Price List”, price\_list, “enabled”))).

**Local steps**

- Return (bool(price\_list) and bool(Platform.get\_cached\_value(“Price List”, price\_list, “enabled”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(price\_list) → bool(Platform.get\_cached\_value(“Price List”, price\_list, “enabled”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, “enabled”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0773.json#L1729) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L178)

<a id="op-eab2df3d266a47"></a>
### Validate default price list side

`operation_enterprise_binding_enterprise_stock_doctype_price_list_price_list_validate_default_price_list_side`

**Inputs** price\_list, side.

**Record and data access** read “Price List” via get\_cached\_value.

**Local steps**

- If (price\_list and not cint(Platform.get\_cached\_value(“Price List”, price\_list, side))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in price\_list → not cint(Platform.get\_cached\_value(“Price List”, price\_list, side)).
  - Evaluate throw(translated “Default Price List {0} is not applicable for {1}”.format(Platform.bold(price\_list), get\_price\_list\_side\_label(side))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, side).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L971) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L468)

<a id="op-e94dc00be796b6"></a>
### Get price list side label

`operation_enterprise_binding_enterprise_stock_doctype_price_list_price_list_get_price_list_side_label`

**Inputs** side.

**Explicit results** translated “Selling” when side equals “selling”, otherwise translated “Buying”.

**Local steps**

- Return translated “Selling” when side equals “selling”, otherwise translated “Buying”.
  - Value choice on side equals “selling” — true gives translated “Selling”, false gives translated “Buying”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L219) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L967) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L464)

<a id="op-7d96d98e3aaf43"></a>
### Validate price list country

`operation_enterprise_binding_enterprise_stock_doctype_price_list_price_list_validate_price_list_country`

**Inputs** price\_list, country.

**Record and data access** read “Price List Country” via get\_all.

**Explicit results** no value.

**Local steps**

- If (not price\_list or not country).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not price\_list → not country.
  - Return no value.
- Set countries from Platform.get\_all(“Price List Country”, filters = mapping(“parent” → price\_list, “parenttype” → “Price List”), pluck = “country”).
- If (countries and country does not belong to countries).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in countries → country does not belong to countries.
  - Evaluate throw(translated “Price List {0} is not applicable for country {1}”.format(Platform.bold(price\_list), Platform.bold(country))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L469)

## Report · Product bundle balance

<a id="op-d8d5de44464d38"></a>
### Execute

`operation_enterprise_stock_report_product_bundle_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- If not filters.
  - Set filters from Platform.\_dict().
- Set columns from get\_columns().
- Set tuple(item\_details, pb\_details, parent\_items, child\_items) from get\_items(filters).
- Set stock\_balance from get\_stock\_balance(filters, child\_items).
- Set data from list().
- For each parent\_item in parent\_items.
  - Set parent\_item\_detail from item\_details at parent\_item.
  - Set required\_items from pb\_details at parent\_item.
  - Set warehouse\_company\_map from mapping().
  - For each child\_item in required\_items.
    - Set child\_item\_balance from stock\_balance.get(child\_item.item\_code, Platform.\_dict()).
    - For each tuple(warehouse, sle) in child\_item\_balance.items().
      - If flt(sle.qty\_after\_transaction) &gt; 0.
        - Set warehouse\_company\_map at warehouse from sle.company.
  - For each tuple(warehouse, company) in warehouse\_company\_map.items().
    - Set parent\_row from mapping(“indent” → 0, “item\_code” → parent\_item, “item\_name” → parent\_item\_detail.item\_name, “item\_group” → parent\_item\_detail.item\_group, …).
    - Set child\_rows from list().
    - For each child\_item\_detail in required\_items.
      - Set child\_item\_balance from stock\_balance.get(child\_item\_detail.item\_code, Platform.\_dict()).get(warehouse, Platform.\_dict()).
      - Set child\_row from mapping(“indent” → 1, “parent\_item” → parent\_item, “item\_code” → child\_item\_detail.item\_code, “item\_name” → child\_item\_detail.item\_name, …).
      - Set child\_row at “bundle\_qty” from max(0, (child\_row at “actual\_qty” floor divide child\_row at “minimum\_qty”)).
      - Evaluate child\_rows.append(child\_row).
    - Set min\_bundle\_qty from min(map(deferred anonymous expression, child\_rows)).
    - Set parent\_row at “bundle\_qty” from min\_bundle\_qty.
    - Evaluate data.append(parent\_row).
    - Update data using + child\_rows.
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L243)

<a id="op-310dc663c92d2d"></a>
### Get columns

`operation_enterprise_stock_report_product_bundle_balance_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “item\_code”, “label” → translated “Item”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “warehouse”, “label” → translated “Warehouse”, “fieldtype” → “Link”, ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0899.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L244)

<a id="op-d004ac5bd35f74"></a>
### Get items

`operation_enterprise_stock_report_product_bundle_balance_business_behavior_get_items`

**Inputs** filters.

**Explicit results** tuple(item\_details, pb\_details, parent\_items, child\_items).

**Local steps**

- Set pb\_details from Platform.\_dict().
- Set item\_details from Platform.\_dict().
- Set item from Platform.qb.DocType(“Item”).
- Set pb from Platform.qb.DocType(“Product Bundle”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.new\_item\_code equals nested operand in the contract.name).select(item.name.as\_(“item\_code”), item.item\_name, ….
- If item\_code bound to filters.get(“item\_code”).
  - Set query from query.where(item.item\_code equals item\_code).
- Otherwise.
  - If brand bound to filters.get(“brand”).
    - Set query from query.where(item.brand equals brand).
  - If item\_group bound to filters.get(“item\_group”).
    - If conditions bound to get\_item\_group\_condition(item\_group, item).
      - Set query from query.where(conditions).
- Set parent\_item\_details from query.run(as\_dict = true).
- Set parent\_items from list().
- For each d in parent\_item\_details.
  - Evaluate parent\_items.append(d.item\_code).
  - Set item\_details at d.item\_code from d.
- Set child\_item\_details from list().
- If parent\_items.
  - Set item from Platform.qb.DocType(“Item”).
  - Set pb from Platform.qb.DocType(“Product Bundle”).
  - Set pbi from Platform.qb.DocType(“Product Bundle Item”).
  - Set child\_item\_details from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“parent\_item”), pbi.item\_code, item.item\_name, pbi.description, …).where(pb.new\_item\_code.isin(paren ….
- Set child\_items from set().
- For each d in child\_item\_details.
  - If d.item\_code differs from d.parent\_item.
    - Evaluate pb\_details.setdefault(d.parent\_item, list()).append(d).
    - Evaluate child\_items.add(d.item\_code).
    - Set item\_details at d.item\_code from d.
- Set child\_items from list(child\_items).
- Return tuple(item\_details, pb\_details, parent\_items, child\_items).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L246)

<a id="op-435b6da009a230"></a>
### Get stock balance

`operation_enterprise_stock_report_product_bundle_balance_business_behavior_get_stock_balance`

**Inputs** filters, items.

**Explicit results** stock\_balance.

**Local steps**

- Set sle from get\_stock\_ledger\_entries(filters, items).
- Set stock\_balance from Platform.\_dict().
- For each d in sle.
  - Set stock\_balance.setdefault(d.item\_code, Platform.\_dict()) at d.warehouse from d.
- Return stock\_balance.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0899.json#L2595) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L247)

<a id="op-8192676e4bfb27"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_product_bundle_balance_business_behavior_get_stock_ledger_entries`

**Inputs** filters, items.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- If not items.
  - Return list().
- Set max\_posting\_datetime\_query from get\_item\_wise\_max\_posting\_datetime(filters, items).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.item\_code, sle.warehouse, sle.qty\_after\_transaction, sle.company).where(sle.is\_cancelled equals 0).orderby(sle.creation).
- If filters.get(“warehouse”).
  - Set warehouse\_details from Platform.db.get\_value(“Warehouse”, filters.get(“warehouse”), list(“lft”, “rgt”), as\_dict = 1).
  - If warehouse\_details.
    - Set wh from Platform.qb.DocType(“Warehouse”).
    - Set query from query.where(sle.warehouse.isin(nested operand in the contract(nested operand in the contract).select(wh.name).where((wh.lft ≥ warehouse\_details.lft bitwise and wh.rgt ≤ warehouse\_details.rgt)))).
- If filters.get(“company”).
  - Set query from query.where(sle.company equals filters.get(“company”)).
- If filters.get(“date”).
  - Set query from query.where(sle.posting\_date ≤ filters.get(“date”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L248)

<a id="op-38233245022023"></a>
### Get item wise max posting datetime

`operation_enterprise_stock_report_product_bundle_balance_business_behavior_get_item_wise_maximum_posting_datetime`

**Inputs** filters, items.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** query.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.item\_code, sle.warehouse, sle.name, nested operand in the contract.as\_(“posting\_datetime”)).where((nested operand in the contract.i ….
- If filters.get(“warehouse”).
  - Set warehouse\_details from Platform.db.get\_value(“Warehouse”, filters.get(“warehouse”), list(“lft”, “rgt”), as\_dict = 1).
  - If warehouse\_details.
    - Set wh from Platform.qb.DocType(“Warehouse”).
    - Set query from query.where(sle.warehouse.isin(nested operand in the contract(nested operand in the contract).select(wh.name).where((wh.lft ≥ warehouse\_details.lft bitwise and wh.rgt ≤ warehouse\_details.rgt)))).
- If filters.get(“company”).
  - Set query from query.where(sle.company equals filters.get(“company”)).
- If filters.get(“date”).
  - Set query from query.where(sle.posting\_date ≤ filters.get(“date”)).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L245)

## Record · Purchase receipt

[Record definition](../../../../data/record-types/purchase_receipt.json)

<a id="op-c4db21f8e90c16"></a>
### Purchase Receipt.initialize

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“target\_dt” → “Purchase Order Item”, “join\_field” → “purchase\_order\_item”, “target\_field” → “received\_qty”, “target\_parent\_dt” → “Purchase Order”, …), mapping(“source\_dt” → “Purchase Receipt I ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L198)

<a id="op-be53edd129efe6"></a>
### Purchase Receipt.update prevdoc status

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_update_prevdoc_status`

**Inputs** self.

**Local steps**

- If cint(self.is\_return).
  - Evaluate self.status\_updater.extend(self.get\_return\_status\_updaters()).
- Evaluate super().update\_prevdoc\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get return status updaters](operations-043.md#op-e1efb59f3534f0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1032) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L529)

<a id="op-e1efb59f3534f0"></a>
### Purchase Receipt.get return status updaters

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_get_return_status_updaters`

**Inputs** self.

**Explicit results** list(mapping(“source\_dt” → “Purchase Receipt Item”, “target\_dt” → “Purchase Order Item”, “join\_field” → “purchase\_order\_item”, “target\_field” → “returned\_qty”, …), mapping(“source\_dt” → “Purchase Receipt I ….

**Local steps**

- Return list(mapping(“source\_dt” → “Purchase Receipt Item”, “target\_dt” → “Purchase Order Item”, “join\_field” → “purchase\_order\_item”, “target\_field” → “returned\_qty”, …), mapping(“source\_dt” → “Purchase Receipt I ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1015) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L512)

<a id="op-d112749571e935"></a>
### Purchase Receipt.before validate

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_before_validate`

**Inputs** self.

**Local steps**

- Bind dependencies \_apply\_putaway\_rule.
- If (self.get(“items”) and self.apply\_putaway\_rule and not self.get(“is\_return”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“items”) → self.apply\_putaway\_rule → not self.get(“is\_return”).
  - Evaluate \_apply\_putaway\_rule(self.doctype, self.get(“items”), self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L193)

<a id="op-313c559dd55dad"></a>
### Purchase Receipt.validate

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_posting\_time().
- Evaluate self.validate\_posting\_date\_with\_po().
- Evaluate super().validate().
- If self.\_action differs from “submit”.
  - Evaluate self.set\_status().
- Evaluate self.po\_required().
- Evaluate self.validate\_items\_quality\_inspection().
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.validate\_uom\_is\_integer().
- Evaluate self.validate\_cwip\_accounts().
- Evaluate self.validate\_provisional\_expense\_account().
- Evaluate self.check\_purchase\_order\_on\_hold\_or\_close(“purchase\_order”).
- If (self.subcontracting\_receipt and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_receipt → not self.is\_return.
  - Evaluate validate\_single\_purchase\_receipt(self.subcontracting\_receipt, self.name).
- If getdate(self.posting\_date) &gt; getdate(nowdate()).
  - Evaluate throw(translated “Posting Date cannot be future date”).
- Evaluate self.get\_current\_stock().
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).
- Evaluate self.reset\_default\_field\_value(“rejected\_warehouse”, “items”, “rejected\_warehouse”).
- Evaluate self.reset\_default\_field\_value(“set\_from\_warehouse”, “items”, “from\_warehouse”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [po required](operations-043.md#op-c231b21980b50d), [validate items quality inspection](operations-043.md#op-444f8c390c0d87), [validate with previous doc](operations-043.md#op-985f9aaf2dfe9a), [validate uom is integer](operations-043.md#op-56938c3686947c), [validate cwip accounts](operations-043.md#op-d090ba1d72011d), [validate provisional expense account](operations-043.md#op-a6e7597ef9867b).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L208)

<a id="op-56938c3686947c"></a>
### Purchase Receipt.validate uom is integer

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_validate_unit_of_measure_is_integer`

**Inputs** self.

**Local steps**

- Evaluate super().validate\_uom\_is\_integer(“uom”, list(“qty”, “received\_qty”), “Purchase Receipt Item”).
- Evaluate super().validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”, “Purchase Receipt Item”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0774.json#L4690) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L211)

<a id="op-d090ba1d72011d"></a>
### Purchase Receipt.validate cwip accounts

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_validate_cwip_accounts`

**Inputs** self.

**Local steps**

- For each item in self.get(“items”).
  - If (item.is\_fixed\_asset and is\_cwip\_accounting\_enabled(item.asset\_category)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_fixed\_asset → is\_cwip\_accounting\_enabled(item.asset\_category).
    - Evaluate self.get\_company\_default(“asset\_received\_but\_not\_billed”).
    - Evaluate get\_asset\_account(“capital\_work\_in\_progress\_account”, asset\_category = item.asset\_category, company = self.company).
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0774.json#L4839) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L209)

<a id="op-a6e7597ef9867b"></a>
### Purchase Receipt.validate provisional expense account

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_purchasereceipt_validate_provisional_expense_account`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Explicit results** no value.

**Local steps**

- Set provisional\_accounting\_for\_non\_stock\_items from cint(Platform.db.get\_value(“Company”, self.company, “enable\_provisional\_accounting\_for\_non\_stock\_items”)).
- If not provisional\_accounting\_for\_non\_stock\_items.
  - Return no value.
- Set default\_provisional\_account from self.get\_company\_default(“default\_provisional\_account”).
- For each item in self.get(“items”).
  - If not item.get(“provisional\_expense\_account”).
    - Set item.provisional\_expense\_account from default\_provisional\_account.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1033) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L530)

<a id="op-985f9aaf2dfe9a"></a>
### Purchase Receipt.validate with previous doc

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_validate_with_previous_record`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Purchase Order” → mapping(“ref\_dn\_field” → “purchase\_order”, “compare\_fields” → list(list(“supplier”, “=”), list(“company”, “=”), list(“currency”, “=”))), “Purch ….
- If (cint(Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”)) and not self.is\_return and not self.is\_internal\_supplier).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”)) → not self.is\_return → not self.is\_internal\_supplier.
  - Evaluate self.validate\_rate\_with\_reference\_doc(list(list(“Purchase Order”, “purchase\_order”, “purchase\_order\_item”))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0774.json#L5035) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L212)

<a id="op-c231b21980b50d"></a>
### Purchase Receipt.po required

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_purchase_order_required`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Purchase Order number required for Item {0}”.format(d.item\_code).

**Local steps**

- If (Platform.db.get\_single\_value(“Buying Settings”, “po\_required”) equals “Yes” and not self.is\_return and not self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Buying Settings”, “po\_required”) equals “Yes” → not self.is\_return → not self.is\_internal\_transfer().
  - For each d in self.get(“items”).
    - If not d.purchase\_order.
      - Call the validation error handler Platform.throw(translated “Purchase Order number required for Item {0}”.format(d.item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “po\_required”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L202)

<a id="op-444f8c390c0d87"></a>
### Purchase Receipt.validate items quality inspection

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_validate_items_quality_inspection`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_qi\_reference.
- For each item in self.get(“items”).
  - Evaluate validate\_qi\_reference(self, item).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L210)

<a id="op-fdc7341d62383d"></a>
### Purchase Receipt.get already received qty

`operation_enterprise_stock_record_definitions_purchase_receipt_business_behavior_purchase_receipt_get_already_received_quantity`

**Inputs** self, po, po\_detail.

**Record and data access** execute query text (SELECT, Purchase Receipt Item).

**Explicit results** ((qty and flt(qty at 0 at 0)) or 0.0).

**Local steps**

- Set qty from Platform.db.sql(query text (SELECT, Purchase Receipt Item), tuple(po\_detail, po, self.name)).
- Return ((qty and flt(qty at 0 at 0)) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (qty and flt(qty at 0 at 0)) → 0.0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty → flt(qty at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L195)
