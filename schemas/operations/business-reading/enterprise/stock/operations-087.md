# Inventory and warehouses · operations 87

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock entry type

[Record definition](../../../../data/record-types/stock_entry_type.json)

<a id="op-e060c868541907"></a>
### Manufacture Entry.prepare source warehouse

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_prepare_source_warehouse`

**Inputs** self.

**Record and data access** read “Job Card Item” via get\_all.

**Local steps**

- Set self.source\_wh from mapping().
- If self.skip\_material\_transfer.
  - If not self.backflush\_from\_wip\_warehouse.
    - Set self.source\_wh from Platform.\_dict(Platform.get\_all(“Job Card Item”, filters = mapping(“parent” → self.job\_card), fields = list(“item\_code”, “source\_warehouse”), as\_list = 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L416) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L31) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L962)

<a id="op-7ffb3eb1e42640"></a>
### Manufacture Entry.add raw materials

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_add_raw_materials`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value · read “BOM” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Consumed quantity of item {0} exceeds transferred quantity.”.format(item\_code).

**Local steps**

- Bind dependencies set\_previous\_operation\_serial\_batch.
- If self.job\_card.
  - Set item\_dict from mapping().
  - If not item\_dict.
    - Set item\_dict from self.get\_items\_from\_job\_card().
  - Set backflush\_based\_on from Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”).
  - If self.bom\_no.
    - If based\_on bound to Platform.get\_cached\_value(“BOM”, self.bom\_no, “backflush\_based\_on”).
      - Set backflush\_based\_on from based\_on.
  - Set available\_serial\_batches from Platform.\_dict(mapping()).
  - If backflush\_based\_on differs from “BOM”.
    - Set available\_serial\_batches from self.get\_transferred\_serial\_batches().
  - Set production\_share from self.get\_production\_share().
  - Set items\_to\_remove from list().
  - For each tuple(item\_code, \_dict) in item\_dict.items().
    - Set \_dict.from\_warehouse from (self.source\_wh.get(item\_code) or self.wip\_warehouse).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.source\_wh.get(item\_code) → self.wip\_warehouse.
    - Set \_dict.to\_warehouse from empty text.
    - If (backflush\_based\_on differs from “BOM” and not self.skip\_material\_transfer).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in backflush\_based\_on differs from “BOM” → not self.skip\_material\_transfer.
      - Set calculated\_qty from (flt(\_dict.transferred\_qty) − flt(\_dict.consumed\_qty)).
      - <a id="op-7ffb3eb1e42640-guard-29"></a>If calculated\_qty &lt; 0.
        - Call the validation error handler Platform.throw(translated “Consumed quantity of item {0} exceeds transferred quantity.”.format(item\_code)).
      - Set \_dict.qty from calculated\_qty.
      - Evaluate self.update\_available\_serial\_batches(\_dict, available\_serial\_batches).
    - Otherwise.
      - Set remaining\_qty from max((flt(\_dict.qty) − flt(\_dict.consumed\_qty)), 0).
      - Set \_dict.qty from min((flt(\_dict.qty) × production\_share), remaining\_qty).
      - If not \_dict.qty.
        - Evaluate items\_to\_remove.append(item\_code).
        - Continue with the next iteration or loop test.
      - If self.skip\_material\_transfer.
        - Evaluate set\_previous\_operation\_serial\_batch(self.stock\_entry, \_dict).
  - For each item\_code in items\_to\_remove.
    - Evaluate item\_dict.pop(item\_code).
  - Evaluate self.stock\_entry.add\_to\_stock\_entry\_detail(item\_dict).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison calculated\_qty &lt; 0, calculated\_qty = -1 selects the branch that calls the validation-error handler with translated “Consumed quantity of item {0} exceeds transferred quantity.”.format(item\_code). With calculated\_qty = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7ffb3eb1e42640-guard-29)

**Methods declared on this owner** [get items from job card](operations-087.md#op-3b149afd554f77), [get transferred serial batches](operations-087.md#op-5081aaea3f5f0d), [get production share](operations-087.md#op-30336bcc8411b6), [update available serial batches](operations-087.md#op-884afc0b72df03).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “backflush\_raw\_materials\_based\_on”), Platform.get\_cached\_value(“BOM”, self.bom\_no, “backflush\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L23) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L954)

<a id="op-30336bcc8411b6"></a>
### Manufacture Entry.get production share

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_get_production_share`

**Inputs** self.

**Record and data access** read “Job Card” via get\_value.

**Explicit results** 1 · min((flt(self.for\_quantity) ÷ for\_quantity), 1).

**Local steps**

- Set for\_quantity from flt(Platform.db.get\_value(“Job Card”, self.job\_card, “for\_quantity”)).
- If not for\_quantity.
  - Return 1.
- Return min((flt(self.for\_quantity) ÷ for\_quantity), 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L25) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L956)

<a id="op-f0baaac0ec6ff4"></a>
### Manufacture Entry.parse available serial batches

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_parse_available_serial_batches`

**Inputs** self, item\_dict, available\_serial\_batches.

**Explicit results** tuple(list(), mapping()) · tuple(serial\_nos, batches).

**Local steps**

- Set key from tuple(item\_dict.item\_code, item\_dict.from\_warehouse).
- If key does not belong to available\_serial\_batches.
  - Return tuple(list(), mapping()).
- Set \_avl\_dict from available\_serial\_batches at key.
- Set qty from item\_dict.qty.
- Set serial\_nos from list().
- Set batches from Platform.\_dict().
- If \_avl\_dict.serial\_nos.
  - Set serial\_nos from \_avl\_dict.serial\_nos at slice no value to cint(qty).
  - Update qty using − len(serial\_nos).
  - For each sn in serial\_nos.
    - Evaluate \_avl\_dict.serial\_nos.remove(sn).
- Otherwise.
  - If \_avl\_dict.batches.
    - Set batches from Platform.\_dict().
    - For each tuple(batch\_no, batch\_qty) in \_avl\_dict.batches.items().
      - <a id="op-f0baaac0ec6ff4-guard-21"></a>If qty ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - If batch\_qty ≤ qty.
        - Set batches at batch\_no from batch\_qty.
        - Update qty using − batch\_qty.
      - Otherwise.
        - Set batches at batch\_no from qty.
        - Set qty from 0.
    - For each \_used\_batch\_no in batches.
      - Update \_avl\_dict.batches at \_used\_batch\_no using − batches at \_used\_batch\_no.
      - If \_avl\_dict.batches at \_used\_batch\_no ≤ 0.
        - Remove \_avl\_dict.batches at \_used\_batch\_no.
- Return tuple(serial\_nos, batches).

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f0baaac0ec6ff4-guard-21)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L1783) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L30) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L961)

<a id="op-884afc0b72df03"></a>
### Manufacture Entry.update available serial batches

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_update_available_serial_batches`

**Inputs** self, item\_dict, available\_serial\_batches.

**Local steps**

- Set tuple(serial\_nos, batches) from self.parse\_available\_serial\_batches(item\_dict, available\_serial\_batches).
- If (serial\_nos or batches).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_nos → batches.
  - Set sabb from SerialBatchCreation(mapping(“item\_code” → item\_dict.item\_code, “warehouse” → item\_dict.from\_warehouse, “posting\_datetime” → get\_combine\_datetime(nested operand in the contract.stock\_entry.posting\_date, nes …().
  - Set item\_dict.serial\_and\_batch\_bundle from sabb.name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [parse available serial batches](operations-087.md#op-f0baaac0ec6ff4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L2408) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L32) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L963)

<a id="op-f0fa35dc490a3a"></a>
### Manufacture Entry.get stock entry data

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_get_stock_entry_data`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….

**Local steps**

- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set stock\_entry\_detail from Platform.qb.DocType(“Stock Entry Detail”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L2791) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L26) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L957)

<a id="op-5081aaea3f5f0d"></a>
### Manufacture Entry.get transferred serial batches

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_get_transferred_serial_batches`

**Inputs** self.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** available\_serial\_batches.

**Local steps**

- Set available\_serial\_batches from Platform.\_dict(mapping()).
- Set stock\_entry\_data from self.get\_stock\_entry\_data().
- For each row in stock\_entry\_data.
  - Set warehouse from row.t\_warehouse when row.purpose equals “Material Transfer for Manufacture”, otherwise row.s\_warehouse.
    - Value choice on row.purpose equals “Material Transfer for Manufacture” — true gives row.t\_warehouse, false gives row.s\_warehouse.
  - Set key from tuple(row.item\_code, warehouse).
  - If key does not belong to available\_serial\_batches.
    - Set available\_serial\_batches at key from Platform.\_dict(mapping(“batches” → defaultdict(float), “serial\_nos” → list())).
  - Set \_avl\_dict from available\_serial\_batches at key.
  - Set sabb\_data from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → row.serial\_and\_batch\_bundle), fields = list(“serial\_no”, “batch\_no”, “qty”)).
  - For each entry in sabb\_data.
    - If entry.serial\_no.
      - If entry.qty &gt; 0.
        - Evaluate \_avl\_dict.serial\_nos.append(entry.serial\_no).
      - Otherwise.
        - Evaluate \_avl\_dict.serial\_nos.remove(entry.serial\_no).
    - If entry.batch\_no.
      - Update \_avl\_dict.batches at entry.batch\_no using + (flt(entry.qty) × negative 1 when row.purpose equals “Material Transfer for Manufacture”, otherwise 1).
        - Value choice on row.purpose equals “Material Transfer for Manufacture” — true gives negative 1, false gives 1.
- Return available\_serial\_batches.

**Methods declared on this owner** [get stock entry data](operations-087.md#op-f0fa35dc490a3a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L3215) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L27) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L958)

<a id="op-3b149afd554f77"></a>
### Manufacture Entry.get items from job card

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_get_items_from_job_card`

**Inputs** self.

**Record and data access** read “Job Card Item” via get\_all · read d at 0 via get\_value · read “Company” via get\_cached\_value.

**Explicit results** item\_dict.

**Local steps**

- Set item\_dict from mapping().
- Set items from Platform.get\_all(“Job Card Item”, fields = list(“name as job\_card\_item”, “item\_code”, “source\_warehouse”, “required\_qty as qty”, …), filters = mapping(“parent” → self.job\_card)).
- For each item in items.
  - Set key from item.item\_code.
  - If key belongs to item\_dict.
    - Update item\_dict at key at “qty” using + flt(item.qty).
  - Otherwise.
    - Set item\_dict at key from item.
- For each tuple(item, item\_details) in item\_dict.items().
  - For each d in list(list(“Account”, “expense\_account”, “stock\_adjustment\_account”), list(“Cost Center”, “cost\_center”, “cost\_center”), list(“Warehouse”, “default\_warehouse”, empty text)).
    - Set company\_in\_record from Platform.db.get\_value(d at 0, item\_details.get(d at 1), “company”).
    - If (not item\_details.get(d at 1) or (company\_in\_record and self.company differs from company\_in\_record)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_details.get(d at 1) → (company\_in\_record and self.company differs from company\_in\_record).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_in\_record → self.company differs from company\_in\_record.
      - Set item\_dict at item at d at 1 from Platform.get\_cached\_value(“Company”, self.company, d at 2) when d at 2, otherwise no value.
        - Value choice on d at 2 — true gives Platform.get\_cached\_value(“Company”, self.company, d at 2), false gives no value.
- Return item\_dict.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, d at 2).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L3840) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L24) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L955)

<a id="op-25059de1e35abb"></a>
### Manufacture Entry.add finished good

`operation_enterprise_stock_record_definitions_stock_entry_type_business_behavior_manufacture_entry_add_finished_good`

**Inputs** self.

**Local steps**

- Bind dependencies get\_item\_defaults.
- Set item from get\_item\_defaults(self.production\_item, self.company).
- Set args from mapping(“to\_warehouse” → self.fg\_warehouse, “from\_warehouse” → empty text, “qty” → (self.for\_quantity − self.process\_loss\_qty), “item\_name” → item.item\_name, …).
- Evaluate self.stock\_entry.add\_to\_stock\_entry\_detail(mapping(self.production\_item → args), bom\_no = self.bom\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L22) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L953)

## Report · Stock ledger

<a id="op-fe45452b5d1971"></a>
### Execute

`operation_enterprise_stock_report_stock_ledger_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** tuple(columns, list()) · tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Evaluate is\_reposting\_item\_valuation\_in\_progress().
- Set include\_uom from filters.get(“include\_uom”).
- Set columns from get\_columns(filters).
- Set items from get\_items(filters).
- If (items equals list() or not apply\_permitted\_warehouses(filters)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in items equals list() → not apply\_permitted\_warehouses(filters).
  - Return tuple(columns, list()).
- Set sl\_entries from get\_stock\_ledger\_entries(filters, items).
- Set item\_details from get\_item\_details(items, sl\_entries, include\_uom).
- Set inv\_dimension\_key from list().
- Set inv\_dimension\_wise\_value from get\_inv\_dimension\_wise\_value(filters).
- If inv\_dimension\_wise\_value.
  - For each key in inv\_dimension\_wise\_value.
    - Set value from inv\_dimension\_wise\_value at key.
    - If isinstance(value, list).
      - Evaluate inv\_dimension\_key.extend(value).
    - Otherwise.
      - Evaluate inv\_dimension\_key.append(value).
- Set inv\_dimension\_opening from list().
- If filters.get(“batch\_no”).
  - Set opening\_row from get\_opening\_balance\_from\_batch(filters, columns, sl\_entries).
- Otherwise.
  - If inv\_dimension\_wise\_value.
    - Set inv\_dimension\_opening from get\_opening\_balance\_for\_inv\_dimension(filters, inv\_dimension\_wise\_value, items).
    - Set opening\_row from get\_inv\_dimension\_opening\_row(inv\_dimension\_opening).
  - Otherwise.
    - Set opening\_row from get\_opening\_balance(filters, columns, sl\_entries, inv\_dimension\_wise\_value).
- Set precision from cint(Platform.db.get\_single\_value(“System Settings”, “float\_precision”)).
- Set bundle\_details from mapping().
- If (filters.get(“segregate\_serial\_batch\_bundle”) or filters.get(“batch\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“segregate\_serial\_batch\_bundle”) → filters.get(“batch\_no”).
  - Set bundle\_details from get\_serial\_batch\_bundle\_details(sl\_entries, filters).
- Set data from list().
- Set conversion\_factors from list().
- Set opening\_rows from opening\_row when isinstance(opening\_row, list), otherwise list(opening\_row) when opening\_row, otherwise list().
  - Value choice on isinstance(opening\_row, list) — true gives opening\_row, false gives list(opening\_row) when opening\_row, otherwise list().
  - Value choice on opening\_row — true gives list(opening\_row), false gives list().
- Set opening\_conversion\_factor from get\_opening\_conversion\_factor(filters, item\_details) when include\_uom, otherwise 0.
  - Value choice on include\_uom — true gives get\_opening\_conversion\_factor(filters, item\_details), false gives 0.
- For each row in opening\_rows.
  - Evaluate data.append(row).
  - Evaluate conversion\_factors.append(opening\_conversion\_factor).
- Set actual\_qty, stock\_value from 0.
- If opening\_rows.
  - Set actual\_qty from opening\_rows at 0.get(“qty\_after\_transaction”, 0).
  - Set stock\_value from opening\_rows at 0.get(“stock\_value”, 0).
- Set batch\_balance\_dict from Platform.\_dict(mapping()).
- If (actual\_qty and filters.get(“batch\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in actual\_qty → filters.get(“batch\_no”).
  - Set batch\_balance\_dict at filters.batch\_no from list(actual\_qty, stock\_value).
- Set inv\_dimension\_wise\_dict from Platform.\_dict(mapping()).
- Evaluate set\_opening\_row\_for\_inv\_dimension(inv\_dimension\_wise\_dict, inv\_dimension\_key, inv\_dimension\_opening).
- Set item\_wh\_wise\_prev\_sle from mapping().
- For each sle in sl\_entries.
  - Set item\_detail from item\_details at sle.item\_code.
  - Evaluate sle.update(item\_detail).
  - Set bundle\_info from bundle\_details.get(sle.serial\_and\_batch\_bundle).
  - If (bundle\_info and not filters.get(“segregate\_serial\_batch\_bundle”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bundle\_info → not filters.get(“segregate\_serial\_batch\_bundle”).
    - Evaluate set\_bundle\_qty\_and\_value(sle, bundle\_info).
  - Otherwise.
    - If bundle\_info.
      - Set segregated\_entries from get\_segregated\_bundle\_entries(sle, bundle\_info, batch\_balance\_dict, filters).
      - Evaluate data.extend(segregated\_entries).
      - If include\_uom.
        - Evaluate conversion\_factors.extend((list(item\_detail.conversion\_factor) × len(segregated\_entries))).
      - Continue with the next iteration or loop test.
  - If inv\_dimension\_key.
    - Evaluate set\_balance\_value\_for\_inv\_dimesion(inv\_dimension\_key, inv\_dimension\_wise\_dict, sle).
  - If filters.get(“batch\_no”).
    - Update actual\_qty using + flt(sle.actual\_qty, precision).
    - Update stock\_value using + sle.stock\_value\_difference.
    - If sle.batch\_no.
      - If not batch\_balance\_dict.get(sle.batch\_no).
        - Set batch\_balance\_dict at sle.batch\_no from list(0, 0).
      - Update batch\_balance\_dict at sle.batch\_no at 0 using + sle.actual\_qty.
      - Update batch\_balance\_dict at sle.batch\_no at 1 using + sle.stock\_value\_difference.
    - If filters.get(“segregate\_serial\_batch\_bundle”).
      - Set actual\_qty from batch\_balance\_dict at sle.batch\_no at 0.
    - If (sle.voucher\_type equals “Stock Reconciliation” and not sle.actual\_qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Reconciliation” → not sle.actual\_qty.
      - Set actual\_qty from sle.qty\_after\_transaction.
      - Set stock\_value from sle.stock\_value.
    - Evaluate sle.update(mapping(“qty\_after\_transaction” → actual\_qty, “stock\_value” → stock\_value, “valuation\_rate” → (flt(stock\_value) ÷ flt(actual\_qty)) when actual\_qty, otherwise 0)).
      - Value choice on actual\_qty — true gives (flt(stock\_value) ÷ flt(actual\_qty)), false gives 0.
  - Evaluate sle.update(mapping(“in\_qty” → max(sle.actual\_qty, 0), “out\_qty” → min(sle.actual\_qty, 0))).
  - If sle.actual\_qty &lt; 0.
    - Set sle at “in\_out\_rate” from flt((sle.stock\_value\_difference ÷ sle.actual\_qty), precision).
    - Set sle at “incoming\_rate” from 0.
  - Otherwise.
    - If (sle.voucher\_type equals “Stock Reconciliation” and sle.actual\_qty &lt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Reconciliation” → sle.actual\_qty &lt; 0.
      - Set sle at “in\_out\_rate” from sle.valuation\_rate.
  - If (sle.voucher\_type equals “Stock Reconciliation” and not sle.in\_qty and not sle.out\_qty and not sle.actual\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Reconciliation” → not sle.in\_qty → not sle.out\_qty → not sle.actual\_qty.
    - Evaluate set\_reconciliation\_in\_out\_qty(sle, item\_wh\_wise\_prev\_sle.get(tuple(sle.item\_code, sle.warehouse))).
  - Set item\_wh\_wise\_prev\_sle at tuple(sle.item\_code, sle.warehouse) from sle.
  - Evaluate data.append(sle).
  - If include\_uom.
    - Evaluate conversion\_factors.append(item\_detail.conversion\_factor).
- Evaluate update\_included\_uom\_in\_report(columns, data, include\_uom, conversion\_factors).
- Return tuple(columns, data).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L504)

<a id="op-6106b711a083d0"></a>
### Set bundle qty and value

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_stock_ledger_set_bundle_qty_and_value`

**Inputs** sle, bundle\_info.

**Local steps**

- Set sle.actual\_qty from sum(generator of flt(row.qty) for row drawn from bundle\_info).
  - Draw row from bundle\_info.
- Set sle.stock\_value\_difference from sum(generator of flt(row.stock\_value\_difference) for row drawn from bundle\_info).
  - Draw row from bundle\_info.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1054)

<a id="op-a92bce119ea499"></a>
### Set reconciliation in out qty

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_stock_ledger_set_reconciliation_in_out_qty`

**Inputs** sle, prev\_sle.

**Local steps**

- Set bal\_qty from prev\_sle.get(“qty\_after\_transaction”, 0) when prev\_sle, otherwise get\_qty\_before\_entry(sle).
  - Value choice on prev\_sle — true gives prev\_sle.get(“qty\_after\_transaction”, 0), false gives get\_qty\_before\_entry(sle).
- Set qty from (sle.qty\_after\_transaction − flt(bal\_qty)).
- If qty &gt; 0.
  - Set sle.in\_qty from qty.
- Otherwise.
  - If qty &lt; 0.
    - Set sle.out\_qty from qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1055)

<a id="op-e3f7dd9fc0aa45"></a>
### Get qty before entry

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_stock_ledger_get_qty_before_entry`

**Inputs** entry.

**Explicit results** result at 0 at 0 when result, otherwise 0.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set result from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(sle.creation, order = Order.desc).limit(1).run().
- Return result at 0 at 0 when result, otherwise 0.
  - Value choice on result — true gives result at 0 at 0, false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1053)

<a id="op-6e973d2d76b399"></a>
### Get opening conversion factor

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_stock_ledger_get_opening_conversion_factor`

**Inputs** filters, item\_details.

**Explicit results** 0 · (item\_details at item\_codes at 0.get(“conversion\_factor”) or 0).

**Local steps**

- Set item\_codes from (filters.get(“item\_code”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“item\_code”) → list().
- If (len(item\_codes) differs from 1 or item\_codes at 0 does not belong to item\_details).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(item\_codes) differs from 1 → item\_codes at 0 does not belong to item\_details.
  - Return 0.
- Return (item\_details at item\_codes at 0.get(“conversion\_factor”) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details at item\_codes at 0.get(“conversion\_factor”) → 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1052)

<a id="op-d5696a19ad6efc"></a>
### Set opening row for inv dimension

`operation_enterprise_stock_report_stock_ledger_business_behavior_set_opening_row_for_invoice_dimension`

**Inputs** inv\_dimension\_wise\_dict, inv\_dimension\_key, inv\_dimension\_opening.

**Local steps**

- For each row in (inv\_dimension\_opening or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in inv\_dimension\_opening → list().
  - Set opening\_key from tuple(list(expanded inv\_dimension\_key, row.item\_code, row.warehouse)).
  - Set inv\_dimension\_wise\_dict at opening\_key from mapping(“qty\_after\_transaction” → flt(row.qty\_after\_transaction), “dimension\_stock\_value” → flt(row.stock\_value)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L522)

<a id="op-50831fce61fb8d"></a>
### Set balance value for inv dimesion

`operation_enterprise_stock_report_stock_ledger_business_behavior_set_balance_value_for_invoice_dimesion`

**Inputs** inv\_dimension\_key, inv\_dimension\_wise\_dict, sle.

**Local steps**

- Set new\_key from copy.deepcopy(inv\_dimension\_key).
- Evaluate new\_key.extend(list(sle.item\_code, sle.warehouse)).
- Set new\_key from tuple(new\_key).
- If new\_key does not belong to inv\_dimension\_wise\_dict.
  - Set inv\_dimension\_wise\_dict at new\_key from mapping(“qty\_after\_transaction” → 0, “dimension\_stock\_value” → 0).
- Set inv\_dimesion\_value from inv\_dimension\_wise\_dict at new\_key.
- Update inv\_dimesion\_value at “qty\_after\_transaction” using + sle.actual\_qty.
- Update inv\_dimesion\_value at “dimension\_stock\_value” using + sle.stock\_value\_difference.
- Evaluate sle.update(mapping(“qty\_after\_transaction” → inv\_dimesion\_value at “qty\_after\_transaction”, “stock\_value” → inv\_dimesion\_value at “dimension\_stock\_value”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0916.json#L2975) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L521)

<a id="op-6c6ed24eecebf1"></a>
### Get segregated bundle entries

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_segregated_bundle_entries`

**Inputs** sle, bundle\_details, batch\_balance\_dict, filters.

**Explicit results** segregated\_entries.

**Local steps**

- Set segregated\_entries from list().
- Set qty\_before\_transaction from (sle.qty\_after\_transaction − sle.actual\_qty).
- Set stock\_value\_before\_transaction from (sle.stock\_value − sle.stock\_value\_difference).
- For each row in bundle\_details.
  - Set new\_sle from copy.deepcopy(sle).
  - Evaluate new\_sle.update(row).
  - Evaluate new\_sle.update(mapping(“in\_out\_rate” → flt((new\_sle.stock\_value\_difference ÷ row.qty)) when row.qty &lt; 0, otherwise 0, “in\_qty” → row.qty when row.qty &gt; 0, otherwise 0, “out\_qty” → row.qty when row.qty &lt; 0, ….
    - Value choice on row.qty &lt; 0 — true gives flt((new\_sle.stock\_value\_difference ÷ row.qty)), false gives 0.
    - Value choice on row.qty &gt; 0 — true gives row.qty, false gives 0.
    - Value choice on row.qty &lt; 0 — true gives row.qty, false gives 0.
    - Value choice on row.qty &gt; 0 — true gives row.incoming\_rate, false gives 0.
  - If (filters.get(“batch\_no”) and row.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“batch\_no”) → row.batch\_no.
    - If not batch\_balance\_dict.get(row.batch\_no).
      - Set batch\_balance\_dict at row.batch\_no from list(0, 0).
    - Update batch\_balance\_dict at row.batch\_no at 0 using + row.qty.
    - Update batch\_balance\_dict at row.batch\_no at 1 using + row.stock\_value\_difference.
    - Evaluate new\_sle.update(mapping(“qty\_after\_transaction” → batch\_balance\_dict at row.batch\_no at 0, “stock\_value” → batch\_balance\_dict at row.batch\_no at 1)).
  - Update qty\_before\_transaction using + row.qty.
  - Update stock\_value\_before\_transaction using + new\_sle.stock\_value\_difference.
  - Set new\_sle.valuation\_rate from (flt(new\_sle.stock\_value) ÷ flt(new\_sle.qty\_after\_transaction)) when new\_sle.qty\_after\_transaction, otherwise 0.
    - Value choice on new\_sle.qty\_after\_transaction — true gives (flt(new\_sle.stock\_value) ÷ flt(new\_sle.qty\_after\_transaction)), false gives 0.
  - Evaluate segregated\_entries.append(new\_sle).
- Return segregated\_entries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L910) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L515)

<a id="op-5be0c74f3fe7f5"></a>
### Get serial batch bundle details

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_serial_batch_bundle_details`

**Inputs** sl\_entries, filters = no value.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** Platform.\_dict(mapping()) · \_bundle\_details.

**Local steps**

- Set bundle\_details from list().
- For each sle in sl\_entries.
  - If sle.serial\_and\_batch\_bundle.
    - Evaluate bundle\_details.append(sle.serial\_and\_batch\_bundle).
- If not bundle\_details.
  - Return Platform.\_dict(mapping()).
- Set query\_filers from mapping(“parent” → tuple(“in”, bundle\_details)).
- If filters.get(“batch\_no”).
  - Set query\_filers at “batch\_no” from filters.batch\_no.
- Set \_bundle\_details from Platform.\_dict(mapping()).
- Set batch\_entries from Platform.get\_all(“Serial and Batch Entry”, filters = query\_filers, fields = list(“parent”, “qty”, “incoming\_rate”, “stock\_value\_difference”, …), order\_by = “parent, idx”).
- For each entry in batch\_entries.
  - Evaluate \_bundle\_details.setdefault(entry.parent, list()).append(entry).
- Return \_bundle\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0916.json#L4225) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L912) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L517)

<a id="op-a2017cdab5e6a5"></a>
### Get columns

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Datetime”, “width” → 150), mapping(“label” → translated “Item”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “ ….
- For each dimension in get\_inventory\_dimensions().
  - Evaluate columns.append(mapping(“label” → translated dimension.doctype, “fieldname” → dimension.fieldname, “fieldtype” → “Link”, “options” → dimension.doctype, …)).
- Evaluate columns.extend(list(mapping(“label” → translated “In Qty”, “fieldname” → “in\_qty”, “fieldtype” → “Float”, “width” → 80, …), mapping(“label” → translated “Out Qty”, “fieldname” → “out\_qty”, “fieldtype” → “F ….
  - Value choice on filters.valuation\_field\_type equals “Currency” — true gives “Company:company:default\_currency”, false gives no value.
  - Value choice on filters.valuation\_field\_type equals “Currency” — true gives “Company:company:default\_currency”, false gives no value.
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L505)

<a id="op-bbfed6e50eca26"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_stock_ledger_entries`

**Inputs** filters, items.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set from\_date from get\_datetime((filters.from\_date + “ 00:00:00”)).
- Set to\_date from get\_datetime((filters.to\_date + “ 23:59:59.999999”)).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Set inventory\_dimension\_fields from get\_inventory\_dimension\_fields().
- If inventory\_dimension\_fields.
  - For each fieldname in inventory\_dimension\_fields.
    - Set query from query.select(fieldname).
    - If values bound to filters.get(fieldname).
      - Set query from query.where(sle at fieldname.isin(list(values) when isinstance(values, str), otherwise values)).
        - Value choice on isinstance(values, str) — true gives list(values), false gives values.
- If items.
  - Set query from query.where(sle.item\_code.isin(items)).
- For each field in list(“voucher\_no”, “project”, “company”).
  - If (filters.get(field) and field does not belong to inventory\_dimension\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(field) → field does not belong to inventory\_dimension\_fields.
    - Set query from query.where(sle at field equals filters.get(field)).
- If filters.get(“batch\_no”).
  - Set bundles from get\_serial\_and\_batch\_bundles(filters).
  - If bundles.
    - Set query from query.where((sle.serial\_and\_batch\_bundle.isin(bundles) bitwise or sle.batch\_no equals filters.batch\_no)).
  - Otherwise.
    - Set query from query.where(sle.batch\_no equals filters.batch\_no).
- Set query from apply\_warehouse\_filter(query, sle, filters).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L913) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L518)

<a id="op-58f7bd41334a11"></a>
### Get serial and batch bundles

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_serial_and_batch_bundles`

**Inputs** filters.

**Explicit results** query.run(pluck = SBE.parent).

**Local steps**

- Set SBB from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set SBE from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(SBE.parent).where((((SBB.docstatus equals 1 bitwis ….
- Return query.run(pluck = SBE.parent).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0917.json#L3969) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L911) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L516)

<a id="op-7b37a98a602e3f"></a>
### Get inventory dimension fields

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_inventory_dimension_fields`

**Inputs** no declared parameters.

**Explicit results** list of dimension.fieldname for dimension drawn from get\_inventory\_dimensions().

**Local steps**

- Return list of dimension.fieldname for dimension drawn from get\_inventory\_dimensions().
  - Draw dimension from get\_inventory\_dimensions().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0917.json#L4327) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L506)

<a id="op-f4ce758df14eef"></a>
### Get items

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_items`

**Inputs** filters.

**Explicit results** items.

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set query from Platform.qb.get\_query(“Item”, fields = list(“name”), ignore\_permissions = false).
- Set conditions from list().
- If item\_codes bound to filters.get(“item\_code”).
  - Evaluate conditions.append(item.name.isin(item\_codes)).
- Otherwise.
  - If brand bound to filters.get(“brand”).
    - Set condition from item.brand.isin(brand) when isinstance(brand, list), otherwise item.brand equals brand.
      - Value choice on isinstance(brand, list) — true gives item.brand.isin(brand), false gives item.brand equals brand.
    - Evaluate conditions.append(condition).
  - If (filters.get(“item\_group”) and condition bound to get\_item\_group\_condition(filters.get(“item\_group”), item)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“item\_group”) → condition bound to get\_item\_group\_condition(filters.get(“item\_group”), item).
    - Evaluate conditions.append(condition).
- Set items from no value.
- If conditions.
  - For each condition in conditions.
    - Set query from query.where(condition).
  - Set items from list of r at 0 for r drawn from query.run().
    - Draw r from query.run().
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L510)

<a id="op-7001e5662fc1a0"></a>
### Get item details

`operation_enterprise_stock_report_stock_ledger_business_behavior_get_item_details`

**Inputs** items, sl\_entries, include\_uom.

**Explicit results** item\_details.

**Local steps**

- Set item\_details from mapping().
- If not items.
  - Set items from list(set(generator of d.item\_code for d drawn from sl\_entries)).
    - Draw d from sl\_entries.
- If not items.
  - Return item\_details.
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(item).select(item.name, item.item\_name, item.description, item.item\_group, …).where(item.name.isin(items)).
- If include\_uom.
  - Set ucd from Platform.qb.DocType(“UOM Conversion Detail”).
  - Set query from query.left\_join(ucd).on((ucd.parent equals item.name bitwise and ucd.uom equals include\_uom)).select(ucd.conversion\_factor).
- Set res from query.run(as\_dict = true).
- For each item in res.
  - Evaluate item\_details.setdefault(item.name, item).
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0917.json#L4915) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L508)
