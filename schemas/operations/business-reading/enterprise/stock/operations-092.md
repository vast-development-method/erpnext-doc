# Inventory and warehouses · operations 92

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock ledger

<a id="op-48749af69859a4"></a>
### Update entries after.update rate on delivery and sales return

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_rate_on_delivery_and_sales_return`

**Inputs** self, sle, outgoing\_rate.

**Record and data access** read (sle.voucher\_type + “ Item”) via get\_value.

**State and service calls** request set\_value on (sle.voucher\_type + “ Item”) · request set\_value on “Packed Item”.

**Local steps**

- Set item\_code from Platform.db.get\_value((sle.voucher\_type + “ Item”), sle.voucher\_detail\_no, “item\_code”).
- If item\_code equals sle.item\_code.
  - Evaluate Platform.db.set\_value((sle.voucher\_type + “ Item”), sle.voucher\_detail\_no, “incoming\_rate”, outgoing\_rate).
- Otherwise.
  - Bind dependencies get\_location\_filters.
  - Set filters from mapping(“parent\_detail\_docname” → sle.voucher\_detail\_no, “item\_code” → sle.item\_code).
  - Evaluate Platform.db.set\_value(“Packed Item”, (filters bitwise or get\_location\_filters(sle)), “incoming\_rate”, outgoing\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L788)

<a id="op-39049f20682a52"></a>
### Update entries after.update rate on purchase receipt

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_rate_on_purchase_receipt`

**Inputs** self, sle, outgoing\_rate.

**Record and data access** read (sle.voucher\_type + “ Item”) via exists · read sle.voucher\_type via get\_cached\_value.

**State and service calls** request set\_value on formatted text {sle.voucher\_type} Item · request set\_value on “Purchase Receipt Item Supplied” · call db\_update on d.

**Local steps**

- If Platform.db.exists((sle.voucher\_type + “ Item”), sle.voucher\_detail\_no).
  - If sle.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”).
    - Set details from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, list(“is\_internal\_supplier”, “is\_return”, “return\_against”), as\_dict = true).
    - If (details.is\_internal\_supplier or (details.is\_return and not details.return\_against)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in details.is\_internal\_supplier → (details.is\_return and not details.return\_against).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in details.is\_return → not details.return\_against.
      - Set rate from outgoing\_rate when details.is\_return, otherwise sle.outgoing\_rate.
        - Value choice on details.is\_return — true gives outgoing\_rate, false gives sle.outgoing\_rate.
      - Evaluate Platform.db.set\_value(formatted text {sle.voucher\_type} Item, sle.voucher\_detail\_no, “valuation\_rate”, rate).
- Otherwise.
  - Evaluate Platform.db.set\_value(“Purchase Receipt Item Supplied”, sle.voucher\_detail\_no, “rate”, outgoing\_rate).
- If Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “is\_subcontracted”).
  - Set doc from Platform.get\_lazy\_doc(sle.voucher\_type, sle.voucher\_no).
  - Evaluate doc.update\_valuation\_rate(reset\_outgoing\_rate = false).
  - For each d in (doc.items + doc.supplied\_items).
    - Evaluate d.db\_update().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, list(“is\_internal\_supplier”, “is\_return”, “return\_against”), as\_dict = true), Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “is\_subcontracted”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0939.json#L5539) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L789)

<a id="op-b815f6e7ceacb4"></a>
### Update entries after.update rate on subcontracting receipt

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_rate_on_subcontracting_receipt`

**Inputs** self, sle, outgoing\_rate.

**Record and data access** read “Subcontracting Receipt Item” via exists.

**State and service calls** request set\_value on “Subcontracting Receipt Item” · request set\_value on “Subcontracting Receipt Supplied Item” · call db\_update on scr · call db\_update on d.

**Local steps**

- If Platform.db.exists(“Subcontracting Receipt Item”, sle.voucher\_detail\_no).
  - Evaluate Platform.db.set\_value(“Subcontracting Receipt Item”, sle.voucher\_detail\_no, “rate”, outgoing\_rate).
- Otherwise.
  - Set amount from flt((negative flt(sle.actual\_qty) × outgoing\_rate), Platform.get\_precision(“Subcontracting Receipt Supplied Item”, “amount”)).
  - Evaluate Platform.db.set\_value(“Subcontracting Receipt Supplied Item”, sle.voucher\_detail\_no, mapping(“rate” → outgoing\_rate, “amount” → amount)).
- Set scr from Platform.get\_lazy\_doc(“Subcontracting Receipt”, sle.voucher\_no, for\_update = true).
- Evaluate scr.calculate\_items\_qty\_and\_amount().
- Evaluate scr.db\_update().
- For each d in scr.items.
  - Evaluate d.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L792)

<a id="op-4fa7a84d022feb"></a>
### Update entries after.update rate on stock reconciliation

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_rate_on_stock_reconciliation`

**Inputs** self, sle.

**Local steps**

- Evaluate Platform.get\_lazy\_doc(“Stock Reconciliation”, sle.voucher\_no, for\_update = true).recalculate\_difference\_amount\_from\_ledger(sle.voucher\_detail\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L791)

<a id="op-3e443c8fa20140"></a>
### Update entries after.get incoming value for serial nos

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_incoming_value_for_serial_numbers`

**Inputs** self, sle, serial\_nos.

**Record and data access** read “Serial No” via get\_all · execute query text (SELECT, Stock Ledger Entry).

**Explicit results** incoming\_values.

**Local steps**

- Set all\_serial\_nos from Platform.get\_all(“Serial No”, fields = list(“purchase\_rate”, “name”, “company”), filters = mapping(“name” → tuple(“in”, serial\_nos))).
- Set incoming\_values from sum(generator of flt(d.purchase\_rate) for d drawn from all\_serial\_nos where d.company equals sle.company).
  - Draw d from all\_serial\_nos, keep a combination only if (d.company equals sle.company).
- Set invalid\_serial\_nos from list of d.name for d drawn from all\_serial\_nos where d.company differs from sle.company.
  - Draw d from all\_serial\_nos, keep a combination only if (d.company differs from sle.company).
- For each serial\_no in invalid\_serial\_nos.
  - Set incoming\_rate from Platform.db.sql(query text (SELECT, Stock Ledger Entry), tuple(sle.company, serial\_no, (serial\_no + “\\n%”), (“%\\n” + serial\_no), …)).
  - Update incoming\_values using + flt(incoming\_rate at 0 at 0) when incoming\_rate, otherwise 0.
    - Value choice on incoming\_rate — true gives flt(incoming\_rate at 0 at 0), false gives 0.
- Return incoming\_values.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L753)

<a id="op-622b9691585cd9"></a>
### Update entries after.get moving average values

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_moving_average_values`

**Inputs** self, sle.

**Local steps**

- Set actual\_qty from flt(sle.actual\_qty).
- Set new\_stock\_qty from (flt(self.wh\_data.qty\_after\_transaction) + actual\_qty).
- If new\_stock\_qty ≥ 0.
  - If actual\_qty &gt; 0.
    - If flt(self.wh\_data.qty\_after\_transaction) ≤ 0.
      - Set self.wh\_data.valuation\_rate from sle.incoming\_rate.
    - Otherwise.
      - Set new\_stock\_value from ((self.wh\_data.qty\_after\_transaction × self.wh\_data.valuation\_rate) + (actual\_qty × sle.incoming\_rate)).
      - Set self.wh\_data.valuation\_rate from (new\_stock\_value ÷ new\_stock\_qty).
  - Otherwise.
    - If sle.outgoing\_rate.
      - If new\_stock\_qty.
        - Set new\_stock\_value from ((self.wh\_data.qty\_after\_transaction × self.wh\_data.valuation\_rate) + (actual\_qty × sle.outgoing\_rate)).
        - Set self.wh\_data.valuation\_rate from (new\_stock\_value ÷ new\_stock\_qty).
      - Otherwise.
        - Set self.wh\_data.valuation\_rate from sle.outgoing\_rate.
- Otherwise.
  - If (flt(self.wh\_data.qty\_after\_transaction) ≥ 0 and sle.outgoing\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.wh\_data.qty\_after\_transaction) ≥ 0 → sle.outgoing\_rate.
    - Set self.wh\_data.valuation\_rate from sle.outgoing\_rate.
  - If (not self.wh\_data.valuation\_rate and actual\_qty &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.wh\_data.valuation\_rate → actual\_qty &gt; 0.
    - Set self.wh\_data.valuation\_rate from sle.incoming\_rate.
  - If (not self.wh\_data.valuation\_rate and sle.voucher\_detail\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.wh\_data.valuation\_rate → sle.voucher\_detail\_no.
    - Set allow\_zero\_valuation\_rate from self.check\_if\_allow\_zero\_valuation\_rate(sle.voucher\_type, sle.voucher\_detail\_no).
    - If not allow\_zero\_valuation\_rate.
      - Set self.wh\_data.valuation\_rate from self.get\_fallback\_rate(sle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if allow zero valuation rate](operations-092.md#op-bd33fbdbf3b4f2), [get fallback rate](operations-092.md#op-c1ee762e31f9b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0940.json#L917) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L756)

<a id="op-a3554f03c91f3c"></a>
### Update entries after.update queue values

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_queue_values`

**Inputs** self, sle.

**Local steps**

- Set incoming\_rate from flt(sle.incoming\_rate).
- Set actual\_qty from flt(sle.actual\_qty).
- Set outgoing\_rate from flt(sle.outgoing\_rate).
- Set self.wh\_data.qty\_after\_transaction from round\_off\_if\_near\_zero((self.wh\_data.qty\_after\_transaction + actual\_qty)).
- If self.valuation\_method equals “LIFO”.
  - Set stock\_queue from LIFOValuation(self.wh\_data.stock\_queue).
- Otherwise.
  - Set stock\_queue from FIFOValuation(self.wh\_data.stock\_queue).
- Set tuple(\_prev\_qty, prev\_stock\_value) from stock\_queue.get\_total\_stock\_and\_value().
- If actual\_qty &gt; 0.
  - Evaluate stock\_queue.add\_stock(qty = actual\_qty, rate = incoming\_rate).
- Otherwise.
  - Bind local operation rate\_generator for subsequent calls.
  - Evaluate stock\_queue.remove\_stock(qty = abs(actual\_qty), outgoing\_rate = outgoing\_rate, rate\_generator = rate\_generator, is\_return\_purchase\_entry = self.is\_return\_purchase\_entry(sle)).
- Set tuple(\_qty, stock\_value) from stock\_queue.get\_total\_stock\_and\_value().
- Set stock\_value\_difference from (stock\_value − prev\_stock\_value).
- Set self.wh\_data.stock\_queue from stock\_queue.state.
- Set self.wh\_data.stock\_value from round\_off\_if\_near\_zero((self.wh\_data.stock\_value + stock\_value\_difference)).
- If not self.wh\_data.stock\_queue.
  - Evaluate self.wh\_data.stock\_queue.append(list(0, (sle.incoming\_rate or sle.outgoing\_rate or self.wh\_data.valuation\_rate))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.incoming\_rate → sle.outgoing\_rate → self.wh\_data.valuation\_rate.
- If flt(self.wh\_data.qty\_after\_transaction, self.flt\_precision).
  - Set self.wh\_data.valuation\_rate from (self.wh\_data.stock\_value ÷ self.wh\_data.qty\_after\_transaction).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is return purchase entry](operations-092.md#op-d4a4c2c161b1e5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L786)

<a id="op-e0e763de48b4e8"></a>
### Update entries after.update queue values.rate generator

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_queue_values_rate_generator`

**Inputs** no declared parameters.

**Declared result** float.

**Explicit results** self.get\_fallback\_rate(sle) · 0.0.

**Local steps**

- Set allow\_zero\_valuation\_rate from self.check\_if\_allow\_zero\_valuation\_rate(sle.voucher\_type, sle.voucher\_detail\_no).
- If not allow\_zero\_valuation\_rate.
  - Return self.get\_fallback\_rate(sle).
- Otherwise.
  - Return 0.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0995.json#L1339) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L787)

<a id="op-d4a4c2c161b1e5"></a>
### Update entries after.is return purchase entry

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_is_return_purchase_entry`

**Inputs** self, sle.

**Record and data access** read sle.voucher\_type via get\_cached\_value.

**Explicit results** false · Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”).

**Local steps**

- If self.skip\_serial\_batch\_valuation.
  - Return false.
- If sle.voucher\_type belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
  - Return Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”).
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “is\_return”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L768)

<a id="op-d7b590ac92fe50"></a>
### Update entries after.update batched values

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_batched_values`

**Inputs** self, sle.

**Local steps**

- Bind dependencies BatchNoValuation.
- Set incoming\_rate from flt(sle.incoming\_rate).
- Set actual\_qty from flt(sle.actual\_qty).
- Set self.wh\_data.qty\_after\_transaction from round\_off\_if\_near\_zero((self.wh\_data.qty\_after\_transaction + actual\_qty)).
- If actual\_qty &gt; 0.
  - Set stock\_value\_difference from (incoming\_rate × actual\_qty).
- Otherwise.
  - Set new\_sle from copy.deepcopy(sle).
  - Set new\_sle.qty from new\_sle.actual\_qty.
  - Set new\_sle.batch\_nos from Platform.\_dict(mapping(new\_sle.batch\_no → new\_sle)).
  - Set batch\_obj from BatchNoValuation(sle = new\_sle, warehouse = new\_sle.get(“warehouse”), item\_code = new\_sle.get(“item\_code”)).
  - Set outgoing\_rate from batch\_obj.get\_incoming\_rate().
  - If outgoing\_rate is identical to no value.
    - Set outgoing\_rate from self.get\_fallback\_rate(sle).
  - Set stock\_value\_difference from (outgoing\_rate × actual\_qty).
- Set self.wh\_data.stock\_value from round\_off\_if\_near\_zero((self.wh\_data.stock\_value + stock\_value\_difference)).
- If self.wh\_data.qty\_after\_transaction.
  - Set self.wh\_data.valuation\_rate from (self.wh\_data.stock\_value ÷ self.wh\_data.qty\_after\_transaction).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get fallback rate](operations-092.md#op-c1ee762e31f9b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0940.json#L2603) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L781)

<a id="op-bd33fbdbf3b4f2"></a>
### Update entries after.check if allow zero valuation rate

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_check_if_allow_zero_valuation_rate`

**Inputs** self, voucher\_type, voucher\_detail\_no.

**Record and data access** read ref\_item\_dt via get\_value.

**Explicit results** Platform.db.get\_value(ref\_item\_dt, voucher\_detail\_no, “allow\_zero\_valuation\_rate”) · 0.

**Local steps**

- Set ref\_item\_dt from empty text.
- If voucher\_type equals “Stock Entry”.
  - Set ref\_item\_dt from (voucher\_type + “ Detail”).
- Otherwise.
  - If voucher\_type belongs to list(“Purchase Invoice”, “Sales Invoice”, “Delivery Note”, “Purchase Receipt”).
    - Set ref\_item\_dt from (voucher\_type + “ Item”).
- If ref\_item\_dt.
  - Return Platform.db.get\_value(ref\_item\_dt, voucher\_detail\_no, “allow\_zero\_valuation\_rate”).
- Otherwise.
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0940.json#L3208) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L746)

<a id="op-c1ee762e31f9b4"></a>
### Update entries after.get fallback rate

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_fallback_rate`

**Inputs** self, sle.

**Declared result** float.

**Explicit results** get\_valuation\_rate(sle.item\_code, sle.warehouse, sle.voucher\_type, sle.voucher\_no, currency = Enterprise.get\_company\_currency(sle.company), company = sle.company, posting\_datetime = sle.posting\_datetime, c ….

**Local steps**

- Return get\_valuation\_rate(sle.item\_code, sle.warehouse, sle.voucher\_type, sle.voucher\_no, currency = Enterprise.get\_company\_currency(sle.company), company = sle.company, posting\_datetime = sle.posting\_datetime, c ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L748)

<a id="op-98d043981c45f9"></a>
### Update entries after.get sle before datetime

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_stock_ledger_entry_before_datetime`

**Inputs** self, args.

**Explicit results** sle.

**Local steps**

- Set sle from get\_stock\_ledger\_entries(args, “&lt;”, “desc”, “limit 1”, for\_update = false).
- Set sle from sle at 0 when sle, otherwise Platform.\_dict().
  - Value choice on sle — true gives sle at 0, false gives Platform.\_dict().
- Return sle.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0940.json#L3597) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L761)

<a id="op-d73225efb22102"></a>
### Update entries after.get sle after datetime

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_get_stock_ledger_entry_after_datetime`

**Inputs** self, args.

**Explicit results** get\_stock\_ledger\_entries(args, “&gt;”, “asc”, for\_update = true, check\_serial\_no = false).

**Local steps**

- Return get\_stock\_ledger\_entries(args, “&gt;”, “asc”, for\_update = true, check\_serial\_no = false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0940.json#L3735) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L760)

<a id="op-b6e382dbba0f4c"></a>
### Update entries after.raise exceptions

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_raise_exceptions`

**Inputs** self.

**Explicit failure paths** validation helper with NegativeStockError — message · NegativeStockError(message).

**Local steps**

- Set msg\_list from list().
- For each tuple(warehouse, exceptions) in self.exceptions.items().
  - Set deficiency from min(generator of e at “diff” for e drawn from exceptions).
    - Draw e from exceptions.
  - If tuple(exceptions at 0 at “voucher\_type”, exceptions at 0 at “voucher\_no”) belongs to Platform.local.flags.currently\_saving.
    - Set msg from translated “{0} units of {1} needed in {2} to complete this transaction.”.format(Platform.bold(abs(deficiency)), Platform.get\_desk\_link(“Item”, exceptions at 0 at “item\_code”, show\_title\_with\_name = true), ….
  - Otherwise.
    - Set msg from translated “{0} units of {1} needed in {2} on {3} {4} for {5} to complete this transaction.”.format(Platform.bold(abs(deficiency)), Platform.get\_desk\_link(“Item”, exceptions at 0 at “item\_code”, show\_title ….
  - If msg.
    - Set reserved\_stock from self.get\_reserved\_stock(exceptions at 0 at “item\_code”, warehouse).
    - If reserved\_stock.
      - Set allowed\_qty from flt((abs(exceptions at 0 at “actual\_qty”) − abs(exceptions at 0 at “diff”)), self.flt\_precision).
      - If allowed\_qty &gt; 0.
        - Set msg from translated “{0} As {1} units are reserved for other sales orders, you are allowed to consume only {2} units.”.format(msg, Platform.bold(reserved\_stock), Platform.bold(allowed\_qty)).
      - Otherwise.
        - Set msg from translated “{0} As the full stock is reserved for other transactions, you're not allowed to consume the stock.”.format(msg).
    - Evaluate msg\_list.append(msg).
- If msg\_list.
  - Set message from whitespace '\\n\\n'.join(msg\_list).
  - If self.verbose.
    - Call the validation error handler Platform.throw(message, NegativeStockError, title = translated “Insufficient Stock”).
  - Otherwise.
    - Raise NegativeStockError(message).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reserved stock](operations-089.md#op-c1d0e0e037b732).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L772)

<a id="op-2cd859f7459ed8"></a>
### Update entries after.update bin data

`operation_enterprise_binding_enterprise_stock_stock_ledger_update_entries_after_update_bin_data`

**Inputs** self, sle.

**State and service calls** request set\_value on “Bin”.

**Local steps**

- Set bin\_name from get\_or\_make\_bin(sle.item\_code, sle.warehouse).
- Set values\_to\_update from mapping(“actual\_qty” → sle.qty\_after\_transaction, “stock\_value” → sle.stock\_value).
- If sle.valuation\_rate is distinct from no value.
  - Set values\_to\_update at “valuation\_rate” from sle.valuation\_rate.
- Evaluate Platform.db.set\_value(“Bin”, bin\_name, values\_to\_update).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1127)

<a id="op-c5fac748dec1e2"></a>
### Update entries after.update bin

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_update_bin`

**Inputs** self.

**Local steps**

- For each tuple(tuple(item\_code, warehouse), data) in self.prev\_sle\_dict.items().
  - Set bin\_name from get\_or\_make\_bin(item\_code, warehouse).
  - Set updated\_values from mapping(“actual\_qty” → flt(data.qty\_after\_transaction), “stock\_value” → flt(data.stock\_value)).
  - If data.valuation\_rate is distinct from no value.
    - Set updated\_values at “valuation\_rate” from flt(data.valuation\_rate).
  - Evaluate update\_bin\_columns(bin\_name, updated\_values).
- Evaluate self.reset\_bin\_without\_stock\_ledger\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset bin without stock ledger entries](operations-092.md#op-ce3668e76a474e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L782)

<a id="op-ce3668e76a474e"></a>
### Update entries after.reset bin without stock ledger entries

`operation_enterprise_stock_stock_ledger_business_behavior_update_entries_after_reset_bin_without_stock_ledger_entries`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via exists · read “Bin” via get\_value.

**Explicit results** no value.

**Local steps**

- Set tuple(item\_code, warehouse) from tuple(self.args.get(“item\_code”), self.args.get(“warehouse”)).
- If (not item\_code or not warehouse or tuple(item\_code, warehouse) belongs to self.prev\_sle\_dict).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_code → not warehouse → tuple(item\_code, warehouse) belongs to self.prev\_sle\_dict.
  - Return no value.
- If Platform.db.exists(“Stock Ledger Entry”, mapping(“item\_code” → item\_code, “warehouse” → warehouse, “is\_cancelled” → 0)).
  - Return no value.
- Set bin\_name from Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse)).
- If not bin\_name.
  - Return no value.
- Evaluate update\_bin\_columns(bin\_name, mapping(“actual\_qty” → 0.0, “stock\_value” → 0.0, “valuation\_rate” → 0.0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L776)

<a id="op-6cec410a9f2a9d"></a>
### Get sle against current voucher

`operation_enterprise_stock_stock_ledger_business_behavior_get_stock_ledger_entry_against_current_voucher`

**Inputs** kwargs.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- If (kwargs.get(“name”) and not kwargs.get(“posting\_datetime”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.get(“name”) → not kwargs.get(“posting\_datetime”).
  - Set kwargs at “posting\_datetime” from Platform.db.get\_value(“Stock Ledger Entry”, kwargs.get(“name”), “posting\_datetime”).
- If not kwargs.get(“posting\_datetime”).
  - Set kwargs at “posting\_datetime” from get\_combine\_datetime(kwargs.posting\_date, kwargs.posting\_time).
- Set doctype from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op …().
- If not kwargs.get(“cancelled”).
  - Set query from query.where(doctype.creation equals kwargs.creation).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L728)

<a id="op-51f6e777b6e3a0"></a>
### Get previous sle of current voucher

`operation_enterprise_stock_stock_ledger_business_behavior_get_previous_stock_ledger_entry_of_current_voucher`

**Inputs** args, operator = “&lt;”, exclude\_current\_voucher = false.

**Explicit results** sle at 0 when sle, otherwise Platform.\_dict().

**Explicit failure paths** validation helper — translated “Invalid operator {0}”.format(operator).

**Local steps**

- If not args.get(“posting\_date”).
  - Set args at “posting\_datetime” from “1900-01-01 00:00:00”.
- If not args.get(“posting\_datetime”).
  - Set args at “posting\_datetime” from get\_combine\_datetime(args at “posting\_date”, args at “posting\_time”).
- Set sle\_doctype from Platform.qb.DocType(“Stock Ledger Entry”).
- Set posting\_datetime from args.get(“posting\_datetime”).
- Set datetime\_conditions from mapping(“&lt;” → sle\_doctype.posting\_datetime &lt; posting\_datetime, “&lt;=” → sle\_doctype.posting\_datetime ≤ posting\_datetime, “&gt;” → sle\_doctype.posting\_datetime &gt; posting\_datetime, “&gt;=” → sle\_doctype.posting\_date ….
- If operator does not belong to datetime\_conditions.
  - Call the validation error handler Platform.throw(translated “Invalid operator {0}”.format(operator)).
- Set datetime\_condition from datetime\_conditions at operator.
- Set query from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(sle\_doctype.creation, order = Order.desc).limit(1).for\_update().
- If exclude\_current\_voucher.
  - Set query from query.where(sle\_doctype.voucher\_no differs from args.get(“voucher\_no”)).
- Otherwise.
  - If (operator equals “&lt;” and args.get(“creation”) and args.get(“sle\_id”) and not args.get(“cancelled”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in operator equals “&lt;” → args.get(“creation”) → args.get(“sle\_id”) → not args.get(“cancelled”).
    - Set datetime\_condition from (sle\_doctype.posting\_datetime &lt; posting\_datetime bitwise or (sle\_doctype.posting\_datetime equals posting\_datetime bitwise and sle\_doctype.creation &lt; args.get(“creation”))).
- Set sle from query.where(datetime\_condition).run(as\_dict = true).
- Return sle at 0 when sle, otherwise Platform.\_dict().
  - Value choice on sle — true gives sle at 0, false gives Platform.\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L723)

<a id="op-c253527ddcadc6"></a>
### Get previous sle

`operation_enterprise_stock_stock_ledger_business_behavior_get_previous_stock_ledger_entry`

**Inputs** args, for\_update = false, extra\_cond = no value, for\_report = false.

**Explicit results** ((sle and sle at 0) or mapping()).

**Local steps**

- Set args at “name” from (args.get(“sle”, no value) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“sle”, no value) → empty text.
- Set sle from get\_stock\_ledger\_entries(args, “&lt;=”, “desc”, “limit 1”, for\_update = for\_update, extra\_cond = extra\_cond, for\_report = for\_report).
- Return ((sle and sle at 0) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (sle and sle at 0) → mapping().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle → sle at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0940.json#L6842) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L722)

<a id="op-f4568b973b08e2"></a>
### Get stock ledger entries

`operation_enterprise_stock_stock_ledger_business_behavior_get_stock_ledger_entries`

**Inputs** previous\_sle, operator = no value, order = “desc”, limit = no value, for\_update = false, debug = false, check\_serial\_no = true, extra\_cond = no value, for\_report = false, fields = no value.

**Record and data access** execute query text (SELECT, Stock Ledger Entry).format(select\_fields = select\_fields, conditions = conditions, limit = (limit or empty text), for\_update = ((for\_update and “for update”) or empty text), …).

**Explicit results** Platform.db.sql(query text (SELECT, Stock Ledger Entry).format(select\_fields = select\_fields, conditions = conditions, limit = (limit or empty text), for\_update = ((for\_update and “for update”) or empty te ….

**Local steps**

- Set conditions from formatted text  and posting\_datetime {operator} %(posting\_datetime)s.
- If item\_code bound to previous\_sle.get(“item\_code”).
  - If isinstance(item\_code, (list bitwise or tuple)).
    - Update conditions using + “ and item\_code in %(item\_code)s”.
  - Otherwise.
    - Update conditions using + “ and item\_code = %(item\_code)s”.
- If warehouse bound to previous\_sle.get(“warehouse”).
  - If isinstance(warehouse, (list bitwise or tuple)).
    - Update conditions using + “ and warehouse in %(warehouse)s”.
  - Otherwise.
    - Update conditions using + “ and warehouse = %(warehouse)s”.
- If (check\_serial\_no and previous\_sle.get(“serial\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in check\_serial\_no → previous\_sle.get(“serial\_no”).
  - Set serial\_no from previous\_sle.get(“serial\_no”).
  - Update conditions using + multiline text in the contract.format(Platform.db.escape(serial\_no), Platform.db.escape(formatted text {serial\_no} %), Platform.db.escape(formatted text % {serial\_no}), Platform.db.escape(formatted text %  ….
- If not previous\_sle.get(“posting\_datetime”).
  - If not previous\_sle.get(“posting\_date”).
    - Set previous\_sle at “posting\_datetime” from “1900-01-01 00:00:00”.
  - Otherwise.
    - Set posting\_time from previous\_sle.get(“posting\_time”).
    - If not posting\_time.
      - Set posting\_time from “00:00:00”.
    - Set previous\_sle at “posting\_datetime” from get\_combine\_datetime(previous\_sle at “posting\_date”, posting\_time).
- If (operator belongs to tuple(“&gt;”, “&lt;=”) and previous\_sle.get(“name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in operator belongs to tuple(“&gt;”, “&lt;=”) → previous\_sle.get(“name”).
  - Update conditions using + “ and name!=%(name)s”.
- If extra\_cond.
  - Update conditions using + formatted text {extra\_cond}.
- If (for\_report and previous\_sle.get(“project”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_report → previous\_sle.get(“project”).
  - Update conditions using + “ and project = %(project)s”.
- Set select\_fields from “, ”.join(generator of formatted text ′{field}′ for field drawn from fields) when fields, otherwise “\*”.
  - Value choice on fields — true gives “, ”.join(generator of formatted text ′{field}′ for field drawn from fields), false gives “\*”.
  - Draw field from fields.
- Return Platform.db.sql(query text (SELECT, Stock Ledger Entry).format(select\_fields = select\_fields, conditions = conditions, limit = (limit or empty text), for\_update = ((for\_update and “for update”) or empty te ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in limit → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (for\_update and “for update”) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_update → “for update”.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L727)

<a id="op-39105fcc40c874"></a>
### Get sle entries by names

`operation_enterprise_binding_enterprise_stock_stock_ledger_get_sle_entries_by_names`

**Inputs** names.

**Record and data access** execute query text (SELECT, Stock Ledger Entry).

**Explicit results** list() · Platform.db.sql(query text (SELECT, Stock Ledger Entry), mapping(“names” → names), as\_dict = 1).

**Local steps**

- If not names.
  - Return list().
- Return Platform.db.sql(query text (SELECT, Stock Ledger Entry), mapping(“names” → names), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1091)

<a id="op-416d447740cd4c"></a>
### Get sle by voucher detail no

`operation_enterprise_stock_stock_ledger_business_behavior_get_stock_ledger_entry_by_voucher_detail_number`

**Inputs** voucher\_detail\_no.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_detail\_no” → voucher\_detail\_no, “is\_cancelled” → 0, “dependant\_sle\_voucher\_detail\_no” → tuple(“is”, “not set”)), fields = list(“item\_code”, ….

**Local steps**

- Return Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_detail\_no” → voucher\_detail\_no, “is\_cancelled” → 0, “dependant\_sle\_voucher\_detail\_no” → tuple(“is”, “not set”)), fields = list(“item\_code”, ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0941.json#L1133) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L729)
