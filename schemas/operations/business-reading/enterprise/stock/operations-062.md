# Inventory and warehouses · operations 62

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Serial batch bundle

<a id="op-12bea2b3b6259c"></a>
### Serial No Valuation.get serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_get_serial_numbers`

**Inputs** self.

**Explicit results** self.sle.serial\_nos · get\_serial\_nos(self.sle.serial\_and\_batch\_bundle).

**Local steps**

- If self.sle.get(“serial\_nos”).
  - Return self.sle.serial\_nos.
- Return get\_serial\_nos(self.sle.serial\_and\_batch\_bundle).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L5932) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L690)

<a id="op-78e7365005d604"></a>
### Serial No Valuation.calculate valuation rate

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_calculate_valuation_rate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not hasattr(self, “wh\_data”).
  - Return no value.
- Set new\_stock\_qty from (self.wh\_data.qty\_after\_transaction + self.sle.actual\_qty).
- If new\_stock\_qty &gt; 0.
  - Set new\_stock\_value from ((self.wh\_data.qty\_after\_transaction × self.wh\_data.valuation\_rate) + self.stock\_value\_change).
  - If new\_stock\_value ≥ 0.
    - Set self.wh\_data.valuation\_rate from (new\_stock\_value ÷ new\_stock\_qty).
- If (not self.wh\_data.valuation\_rate and self.sle.voucher\_detail\_no and not self.is\_rejected\_entry()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.wh\_data.valuation\_rate → self.sle.voucher\_detail\_no → not self.is\_rejected\_entry().
  - Set allow\_zero\_rate from self.sle\_self.check\_if\_allow\_zero\_valuation\_rate(self.sle.voucher\_type, self.sle.voucher\_detail\_no).
  - If not allow\_zero\_rate.
    - Set self.wh\_data.valuation\_rate from self.sle\_self.get\_fallback\_rate(self.sle).
- Update self.wh\_data.qty\_after\_transaction using + self.sle.actual\_qty.
- Set self.wh\_data.stock\_value from (flt(self.wh\_data.qty\_after\_transaction) × flt(self.wh\_data.valuation\_rate)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is rejected entry](operations-062.md#op-1db9ee52550164).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L6038) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L686)

<a id="op-1db9ee52550164"></a>
### Serial No Valuation.is rejected entry

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_is_rejected_entry`

**Inputs** self.

**Explicit results** is\_rejected(self.sle.voucher\_type, self.sle.voucher\_detail\_no, self.sle.warehouse).

**Local steps**

- Return is\_rejected(self.sle.voucher\_type, self.sle.voucher\_detail\_no, self.sle.warehouse).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L6534) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L692)

<a id="op-12e634955701c1"></a>
### Serial No Valuation.get incoming rate

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_get_incoming_rate`

**Inputs** self.

**Explicit results** 0.0 · abs((flt(self.stock\_value\_change) ÷ flt(self.sle.actual\_qty))).

**Local steps**

- If (not self.sle.actual\_qty and self.sle.voucher\_type equals “Stock Reconciliation”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sle.actual\_qty → self.sle.voucher\_type equals “Stock Reconciliation”.
  - Return 0.0.
- Return abs((flt(self.stock\_value\_change) ÷ flt(self.sle.actual\_qty))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L6618) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L687)

<a id="op-a0a401714eeb06"></a>
### Serial No Valuation.get incoming rate of serial no

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_get_incoming_rate_of_serial_number`

**Inputs** self, serial\_no.

**Explicit results** self.serial\_no\_incoming\_rate.get(serial\_no, 0.0).

**Local steps**

- Return self.serial\_no\_incoming\_rate.get(serial\_no, 0.0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L6775) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L688)

<a id="op-33a9a40164203a"></a>
### Is rejected

`operation_enterprise_stock_serial_batch_bundle_business_behavior_is_rejected`

**Inputs** voucher\_type, voucher\_detail\_no, warehouse.

**Record and data access** read (voucher\_type + “ Item”) via get\_cached\_value.

**Explicit results** warehouse equals Platform.get\_cached\_value((voucher\_type + “ Item”), voucher\_detail\_no, “rejected\_warehouse”) · false.

**Local steps**

- If voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”).
  - Return warehouse equals Platform.get\_cached\_value((voucher\_type + “ Item”), voucher\_detail\_no, “rejected\_warehouse”).
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value((voucher\_type + “ Item”), voucher\_detail\_no, “rejected\_warehouse”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1068) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L640)

<a id="op-deb8458e1f9562"></a>
### Batch No Valuation.initialize

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_initialize`

**Inputs** self, remaining named values kwargs.

**Local steps**

- For each tuple(key, value) in kwargs.items().
  - Evaluate setattr(self, key, value).
- Set self.total\_qty from defaultdict(float).
- Set self.stock\_queue from list().
- Set self.batch\_nos from self.get\_batch\_nos().
- Evaluate self.prepare\_batches().
- Evaluate self.calculate\_avg\_rate().
- Evaluate self.calculate\_valuation\_rate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get batch nos](operations-062.md#op-424b8b2140aced), [prepare batches](operations-062.md#op-6cdaea1da5eefb), [calculate avg rate](operations-062.md#op-03ef0bd388329a), [calculate valuation rate](operations-062.md#op-9d9e943a0f1af9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L6993) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1049) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L621)

<a id="op-03ef0bd388329a"></a>
### Batch No Valuation.calculate avg rate

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_calculate_average_rate`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value.

**Local steps**

- If flt(self.sle.actual\_qty) &gt; 0.
  - Set self.stock\_value\_change from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “total\_amount”).
- Otherwise.
  - Set self.stock\_value\_change from 0.0.
  - Set self.batch\_avg\_rate from defaultdict(float).
  - Set self.available\_qty from defaultdict(float).
  - Set self.stock\_value\_differece from defaultdict(float).
  - Evaluate self.seed\_from\_stock\_closing\_balance().
  - For each ledger in self.get\_batch\_stock\_before\_date().
    - Update self.stock\_value\_differece at ledger.batch\_no using + flt(ledger.incoming\_rate).
    - Update self.available\_qty at ledger.batch\_no using + flt(ledger.qty).
  - Evaluate self.calculate\_avg\_rate\_from\_deprecarated\_ledgers().
  - Evaluate self.calculate\_avg\_rate\_for\_non\_batchwise\_valuation().
  - Evaluate self.set\_stock\_value\_difference().

If control reaches the end, it returns no value.

**Methods declared on this owner** [seed from stock closing balance](operations-062.md#op-cabe5c32f24f04), [get batch stock before date](operations-062.md#op-76c68dc136bb59), [set stock value difference](operations-062.md#op-db10a3ee8cae06).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “total\_amount”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1041) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L613)

<a id="op-cabe5c32f24f04"></a>
### Batch No Valuation.seed from stock closing balance

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_seed_from_stock_closing_balance`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.stock\_closing\_from\_datetime from no value.
- Set closing\_entry from self.get\_closing\_entry\_for\_seeding().
- If not closing\_entry.
  - Return no value.
- Bind dependencies get\_combine\_datetime.
- Set self.stock\_closing\_from\_datetime from get\_combine\_datetime(add\_days(closing\_entry.to\_date, 1), “00:00:00”).
- For each row in self.get\_stock\_closing\_balance\_entries(closing\_entry.name).
  - Update self.stock\_value\_differece at row.batch\_no using + flt(row.stock\_value\_difference).
  - Update self.available\_qty at row.batch\_no using + flt(row.actual\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get closing entry for seeding](operations-062.md#op-bfcafd2f1c5e79), [get stock closing balance entries](operations-062.md#op-90391e33a52c0d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L522) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1051) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L623)

<a id="op-bfcafd2f1c5e79"></a>
### Batch No Valuation.get closing entry for seeding

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_get_closing_entry_for_seeding`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_cached\_value.

**Explicit results** no value · closing\_entry.

**Local steps**

- Bind dependencies get\_closing\_entry\_for\_closed\_period.
- If (not self.batchwise\_valuation\_batches or not self.sle.posting\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.batchwise\_valuation\_batches → not self.sle.posting\_date.
  - Return no value.
- Set company from (self.sle.company or Platform.get\_cached\_value(“Warehouse”, self.sle.warehouse, “company”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.sle.company → Platform.get\_cached\_value(“Warehouse”, self.sle.warehouse, “company”).
- Set closing\_entry from get\_closing\_entry\_for\_closed\_period(company).
- If (not closing\_entry or getdate(self.sle.posting\_date) ≤ getdate(closing\_entry.to\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not closing\_entry → getdate(self.sle.posting\_date) ≤ getdate(closing\_entry.to\_date).
  - Return no value.
- Return closing\_entry.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, self.sle.warehouse, “company”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L805) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1046) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L618)

<a id="op-90391e33a52c0d"></a>
### Batch No Valuation.get stock closing balance entries

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_get_stock_closing_balance_entries`

**Inputs** self, closing\_entry.

**Explicit results** nested operand in the contract(nested operand in the contract).select(table.batch\_no, table.actual\_qty, table.stock\_value\_difference).where(((((nested operand in the contract bitwise and nested operand in  ….

**Local steps**

- Set table from Platform.qb.DocType(“Stock Closing Balance”).
- Return nested operand in the contract(nested operand in the contract).select(table.batch\_no, table.actual\_qty, table.stock\_value\_difference).where(((((nested operand in the contract bitwise and nested operand in  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L1079) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1048) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L620)

<a id="op-76c68dc136bb59"></a>
### Batch No Valuation.get batch stock before date

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_get_batch_stock_before_date`

**Inputs** self.

**Declared result** list at dict.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- If not self.batchwise\_valuation\_batches.
  - Return list().
- Set child from Platform.qb.DocType(“Serial and Batch Entry”).
- Set sle\_creation from self.sle.creation when self.sle.get(“name”), otherwise no value.
  - Value choice on self.sle.get(“name”) — true gives self.sle.creation, false gives no value.
- If (not self.sle.get(“name”) and self.sle.get(“serial\_and\_batch\_bundle”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sle.get(“name”) → self.sle.get(“serial\_and\_batch\_bundle”).
  - Set sle\_creation from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“serial\_and\_batch\_bundle” → self.sle.serial\_and\_batch\_bundle, “is\_cancelled” → 0), “creation”).
- Set timestamp\_condition from empty text.
- If self.sle.posting\_datetime.
  - Set timestamp\_condition from child.posting\_datetime &lt; self.sle.posting\_datetime.
  - Set sle\_table from Platform.qb.DocType(“Stock Ledger Entry”).
  - If sle\_creation.
    - Set tie\_condition from ExistsCriterion(nested operand in the contract.from\_(sle\_table).select(sle\_table.name).where(((sle\_table.serial\_and\_batch\_bundle equals child.parent bitwise and sle\_table.is\_cancelled equals 0) bitwise and ….
  - Otherwise.
    - Set tie\_condition from ExistsCriterion(nested operand in the contract.from\_(sle\_table).select(sle\_table.name).where((sle\_table.serial\_and\_batch\_bundle equals child.parent bitwise and sle\_table.is\_cancelled equals 0))).
  - Update timestamp\_condition using bitwise or (child.posting\_datetime equals self.sle.posting\_datetime bitwise and tie\_condition).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- If self.sle.voucher\_detail\_no.
  - Set query from query.where(child.voucher\_detail\_no differs from self.sle.voucher\_detail\_no).
- Otherwise.
  - If self.sle.voucher\_no.
    - Set query from query.where(child.voucher\_no differs from self.sle.voucher\_no).
- Set query from query.where(child.voucher\_type differs from “Pick List”).
- If timestamp\_condition.
  - Set query from query.where(timestamp\_condition).
- If self.stock\_closing\_from\_datetime.
  - Set query from query.where(child.posting\_datetime ≥ self.stock\_closing\_from\_datetime).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1045) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L617)

<a id="op-6cdaea1da5eefb"></a>
### Batch No Valuation.prepare batches

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_prepare_batches`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Batch” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_valuation\_method.
- Set self.batches from self.batch\_nos.
- If isinstance(self.batch\_nos, dict).
  - Set self.batches from list(self.batch\_nos.keys()).
- Set self.batchwise\_valuation\_batches from list().
- Set self.non\_batchwise\_valuation\_batches from list().
- If batchwise\_batches bound to self.sle.get(“batchwise\_valuation\_batches”).
  - Set self.batchwise\_valuation\_batches from list(batchwise\_batches).
  - Set self.non\_batchwise\_valuation\_batches from list((set(self.batches) − set(batchwise\_batches))).
  - Return no value.
- If (get\_valuation\_method(self.sle.item\_code, self.sle.company) equals “Moving Average” and Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in get\_valuation\_method(self.sle.item\_code, self.sle.company) equals “Moving Average” → Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).
  - Set self.non\_batchwise\_valuation\_batches from self.batches.
  - Return no value.
- Set batches from Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, self.batches), “use\_batchwise\_valuation” → 1), fields = list(“name”)).
- For each batch in batches.
  - Evaluate self.batchwise\_valuation\_batches.append(batch.name).
- Set self.non\_batchwise\_valuation\_batches from list((set(self.batches) − set(self.batchwise\_valuation\_batches))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L2832) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1050) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L622)

<a id="op-424b8b2140aced"></a>
### Batch No Valuation.get batch nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_get_batch_numbers`

**Inputs** self.

**Declared result** list.

**Explicit results** self.sle.batch\_nos · get\_batch\_nos(self.sle.serial\_and\_batch\_bundle).

**Local steps**

- If self.sle.get(“batch\_nos”).
  - Return self.sle.batch\_nos.
- Return get\_batch\_nos(self.sle.serial\_and\_batch\_bundle).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L3483) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1044) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L616)

<a id="op-db10a3ee8cae06"></a>
### Batch No Valuation.set stock value difference

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_set_stock_value_difference`

**Inputs** self.

**Local steps**

- For each tuple(batch\_no, ledger) in self.batch\_nos.items().
  - If batch\_no belongs to self.non\_batchwise\_valuation\_batches.
    - Continue with the next iteration or loop test.
  - If not self.available\_qty at batch\_no.
    - Continue with the next iteration or loop test.
  - Set self.batch\_avg\_rate at batch\_no from (self.stock\_value\_differece at batch\_no ÷ self.available\_qty at batch\_no).
  - Set stock\_value\_change from (self.batch\_avg\_rate at batch\_no × ledger.qty).
  - Update self.stock\_value\_change using + stock\_value\_change.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L3591) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1052) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L624)

<a id="op-9d9e943a0f1af9"></a>
### Batch No Valuation.calculate valuation rate

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_calculate_valuation_rate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not hasattr(self, “wh\_data”).
  - Return no value.
- Set self.wh\_data.stock\_value from round\_off\_if\_near\_zero((self.wh\_data.stock\_value + self.stock\_value\_change)).
- Update self.wh\_data.qty\_after\_transaction using + self.sle.actual\_qty.
- If self.wh\_data.qty\_after\_transaction.
  - Set self.wh\_data.valuation\_rate from (self.wh\_data.stock\_value ÷ self.wh\_data.qty\_after\_transaction).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L3830) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1042) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L614)

<a id="op-96905cf83255ea"></a>
### Batch No Valuation.get incoming rate

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_get_incoming_rate`

**Inputs** self.

**Explicit results** 0.0 · abs((flt(self.stock\_value\_change) ÷ flt(self.sle.actual\_qty))).

**Local steps**

- If not self.sle.actual\_qty.
  - Set self.sle.actual\_qty from self.get\_actual\_qty().
- If not self.sle.actual\_qty.
  - Return 0.0.
- Return abs((flt(self.stock\_value\_change) ÷ flt(self.sle.actual\_qty))).

**Methods declared on this owner** [get actual qty](operations-062.md#op-833104fec9fb1e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L4044) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1047) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L619)

<a id="op-833104fec9fb1e"></a>
### Batch No Valuation.get actual qty

`operation_enterprise_stock_serial_batch_bundle_business_behavior_batch_number_valuation_get_actual_quantity`

**Inputs** self.

**Explicit results** total\_qty.

**Local steps**

- Set total\_qty from 0.0.
- For each batch\_no in self.available\_qty.
  - Update total\_qty using + self.available\_qty at batch\_no.
- Return total\_qty.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L4223) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1043) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L615)

<a id="op-3801505840d41e"></a>
### Get batch nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_batch_numbers`

**Inputs** serial\_and\_batch\_bundle.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** Platform.\_dict(mapping()) · mapping of d.batch\_no → d for d drawn from entries.

**Local steps**

- If not serial\_and\_batch\_bundle.
  - Return Platform.\_dict(mapping()).
- Set entries from Platform.get\_all(“Serial and Batch Entry”, fields = list(“batch\_no”, mapping(“SUM” → “qty”, “as” → “qty”)), filters = mapping(“parent” → serial\_and\_batch\_bundle, “batch\_no” → tuple(“is”, “set”)), order\_by  ….
- If not entries.
  - Return Platform.\_dict(mapping()).
- Return mapping of d.batch\_no → d for d drawn from entries.
  - Draw d from entries.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L4315) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1054) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L626)

<a id="op-35c1209fdcd6da"></a>
### Get empty batches based work order

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_empty_batches_based_work_order`

**Inputs** work\_order, item\_code.

**Explicit results** batches.

**Local steps**

- Set batches from get\_batches\_from\_work\_order(work\_order, item\_code).
- If not batches.
  - Return batches.
- Set entries from get\_batches\_from\_stock\_entries(work\_order, item\_code).
- If not entries.
  - Return batches.
- Set ids from list of d.serial\_and\_batch\_bundle for d drawn from entries where d.serial\_and\_batch\_bundle.
  - Draw d from entries, keep a combination only if (d.serial\_and\_batch\_bundle).
- If ids.
  - Evaluate set\_batch\_details\_from\_package(ids, batches).
- For each d in entries.
  - If not d.batch\_no.
    - Continue with the next iteration or loop test.
  - Update batches at d.batch\_no using − d.qty.
- Return batches.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L4625) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1059) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L631)

<a id="op-bcba42d77e5dfb"></a>
### Get batches from work order

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_batches_from_work_order`

**Inputs** work\_order, item\_code.

**Record and data access** read “Batch” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Batch”, fields = list(“name”, “qty\_to\_produce”), filters = mapping(“reference\_name” → work\_order, “item” → item\_code), as\_list = 1)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(“Batch”, fields = list(“name”, “qty\_to\_produce”), filters = mapping(“reference\_name” → work\_order, “item” → item\_code), as\_list = 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L4922) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1057) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L629)

<a id="op-04c91e58a3430a"></a>
### Get batches from stock entries

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_batches_from_stock_entries`

**Inputs** work\_order, item\_code.

**Record and data access** read “Stock Entry” via get\_all · read “Stock Entry Detail” via get\_all.

**Explicit results** Platform.get\_all(“Stock Entry Detail”, fields = list(“batch\_no”, “qty”, “serial\_and\_batch\_bundle”), filters = mapping(“parent” → tuple(“in”, list of d.name for d drawn from entries), “is\_finished\_item” → 1 ….

**Local steps**

- Set entries from Platform.get\_all(“Stock Entry”, filters = mapping(“work\_order” → work\_order, “docstatus” → 1, “purpose” → “Manufacture”), fields = list(“name”)).
- Return Platform.get\_all(“Stock Entry Detail”, fields = list(“batch\_no”, “qty”, “serial\_and\_batch\_bundle”), filters = mapping(“parent” → tuple(“in”, list of d.name for d drawn from entries), “is\_finished\_item” → 1 ….
  - Draw d from entries.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L5087) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1056) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L628)

<a id="op-cdceccf107b304"></a>
### Set batch details from package

`operation_enterprise_stock_serial_batch_bundle_business_behavior_set_batch_details_from_package`

**Inputs** ids, batches.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Local steps**

- Set entries from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, ids), “is\_outward” → 0), fields = list(“batch\_no”, “qty”)).
- For each d in entries.
  - Update batches at d.batch\_no using − d.qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L5397) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L693)

<a id="op-74fed4f395dd6c"></a>
### Serial Batch Creation.initialize

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_initialize`

**Inputs** self, args.

**Local steps**

- Evaluate self.set(args).
- Evaluate self.set\_item\_details().
- Evaluate self.set\_other\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set](operations-063.md#op-c31a07270ab07e), [set item details](operations-063.md#op-068dccff5aa91d), [set other details](operations-063.md#op-52eaa15a42aab1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L5599) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L672)
