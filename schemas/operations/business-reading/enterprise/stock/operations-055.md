# Inventory and warehouses · operations 55

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Serial and batch bundle

[Record definition](../../../../data/record-types/serial_and_batch_bundle.json)

<a id="op-bcbf7e69a1d3e5"></a>
### Serialand Batch Bundle.get return against

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_return_against`

**Inputs** self, parent = no value.

**Record and data access** read self.voucher\_type via get\_value.

**Explicit results** parent.get(“return\_against”) · voucher\_details.get(“return\_against”) · return\_against.

**Local steps**

- Set return\_against from no value.
- If (parent and parent.get(“is\_return”) and parent.get(“return\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent → parent.get(“is\_return”) → parent.get(“return\_against”).
  - Return parent.get(“return\_against”).
- If (self.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”, “Purchase Invoice”, “Purchase Receipt”, …) and self.voucher\_type and self.voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”, “Purchase Invoice”, “Purchase Receipt”, …) → self.voucher\_type → self.voucher\_no.
  - Set voucher\_details from Platform.db.get\_value(self.voucher\_type, self.voucher\_no, list(“is\_return”, “return\_against”), as\_dict = true).
  - If (voucher\_details and voucher\_details.get(“is\_return”) and voucher\_details.get(“return\_against”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_details → voucher\_details.get(“is\_return”) → voucher\_details.get(“return\_against”).
    - Return voucher\_details.get(“return\_against”).
- Return return\_against.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0806.json#L449) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L572)

<a id="op-fa1d7426b159cc"></a>
### Serialand Batch Bundle.set incoming rate for inward transaction

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_incoming_rate_for_inward_transaction`

**Inputs** self, row = no value, save = false, prev\_sle = no value.

**Record and data access** read “Subcontracting Receipt Supplied Item” via exists · read child\_table via get\_value · read “Packed Item” via get\_value · read “Batch” via get\_all.

**State and service calls** call db\_set on d.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_valuation\_method.
- Set valuation\_method from get\_valuation\_method(self.item\_code, self.company).
- Set valuation\_field from “valuation\_rate”.
- If self.voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”, “Quotation”).
  - Set valuation\_field from “incoming\_rate”.
- If self.voucher\_type equals “POS Invoice”.
  - Set valuation\_field from “rate”.
- Set rate from row.get(valuation\_field) when row, otherwise 0.0.
  - Value choice on row — true gives row.get(valuation\_field), false gives 0.0.
- Set child\_table from self.child\_table.
- If self.voucher\_type equals “Subcontracting Receipt”.
  - If not self.voucher\_detail\_no.
    - Return no value.
  - Otherwise.
    - If Platform.db.exists(“Subcontracting Receipt Supplied Item”, self.voucher\_detail\_no).
      - Set valuation\_field from “rate”.
      - Set child\_table from “Subcontracting Receipt Supplied Item”.
    - Otherwise.
      - Set valuation\_field from “rate”.
      - Set child\_table from “Subcontracting Receipt Item”.
- If (not rate and self.voucher\_detail\_no and self.voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not rate → self.voucher\_detail\_no → self.voucher\_no.
  - Set rate from Platform.db.get\_value(child\_table, self.voucher\_detail\_no, valuation\_field).
- Set is\_packed\_item from false.
- If (rate is identical to no value and child\_table belongs to list(“Delivery Note Item”, “Sales Invoice Item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rate is identical to no value → child\_table belongs to list(“Delivery Note Item”, “Sales Invoice Item”).
  - Set rate from Platform.db.get\_value(“Packed Item”, mapping(“parent\_detail\_docname” → self.voucher\_detail\_no, “item\_code” → self.item\_code), “incoming\_rate”).
  - If rate is identical to no value.
    - Set rate from Platform.db.get\_value(“Packed Item”, self.voucher\_detail\_no, “incoming\_rate”).
  - If rate is distinct from no value.
    - Set is\_packed\_item from true.
- Set stock\_queue from list().
- Set batches from Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, list of d.batch\_no for d drawn from self.entries where d.batch\_no), “use\_batchwise\_valuation” → 0), pluck = “name”).
  - Draw d from self.entries, keep a combination only if (d.batch\_no).
- If (prev\_sle and prev\_sle.stock\_queue and parse\_json(prev\_sle.stock\_queue)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in prev\_sle → prev\_sle.stock\_queue → parse\_json(prev\_sle.stock\_queue).
  - If (batches and valuation\_method belongs to tuple(“FIFO”, “LIFO”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in batches → valuation\_method belongs to tuple(“FIFO”, “LIFO”).
    - Set stock\_queue from parse\_json(prev\_sle.stock\_queue).
- Set values\_rejected\_material from (self.voucher\_type differs from “Subcontracting Receipt” and is\_rejected\_material\_valued(self.voucher\_type, self.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type differs from “Subcontracting Receipt” → is\_rejected\_material\_valued(self.voucher\_type, self.voucher\_detail\_no).
- If (self.is\_rejected and is\_material\_from\_in\_transit\_warehouse(self.voucher\_type, self.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_rejected → is\_material\_from\_in\_transit\_warehouse(self.voucher\_type, self.voucher\_detail\_no).
  - Set rate from (flt(self.get\_transit\_rate(row)) or rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.get\_transit\_rate(row)) → rate.
- Set entry\_rates from (self.get\_transfer\_rates() or self.get\_subcontracting\_return\_rates()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_transfer\_rates() → self.get\_subcontracting\_return\_rates().
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “incoming\_rate”).
- For each d in self.entries.
  - Set is\_queue\_valued from (valuation\_method belongs to tuple(“FIFO”, “LIFO”) and d.batch\_no belongs to batches).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in valuation\_method belongs to tuple(“FIFO”, “LIFO”) → d.batch\_no belongs to batches.
  - Set entry\_rate from entry\_rates.get(tuple(d.serial\_no, d.batch\_no), rate).
  - If (self.is\_rejected and not values\_rejected\_material).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_rejected → not values\_rejected\_material.
    - Set entry\_rate from 0.0.
  - Otherwise.
    - If (flt(d.incoming\_rate, precision) equals flt(entry\_rate, precision) and not stock\_queue and not is\_queue\_valued and d.qty and d.stock\_value\_difference).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(d.incoming\_rate, precision) equals flt(entry\_rate, precision) → not stock\_queue → not is\_queue\_valued → d.qty → d.stock\_value\_difference.
      - Continue with the next iteration or loop test.
  - If (is\_packed\_item and d.incoming\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_packed\_item → d.incoming\_rate.
    - Set entry\_rate from d.incoming\_rate.
  - Set d.incoming\_rate from flt(entry\_rate).
  - If d.qty.
    - Set d.stock\_value\_difference from (flt(d.qty) × d.incoming\_rate).
  - If (is\_queue\_valued and d.incoming\_rate is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_queue\_valued → d.incoming\_rate is distinct from no value.
    - Evaluate stock\_queue.append(list(d.qty, d.incoming\_rate)).
    - Set d.stock\_queue from json.dumps(stock\_queue).
  - If save.
    - Evaluate d.db\_set(mapping(“incoming\_rate” → d.incoming\_rate, “stock\_value\_difference” → d.stock\_value\_difference, “stock\_queue” → d.get(“stock\_queue”))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get transit rate](operations-055.md#op-31ece2be62ab3b), [get transfer rates](operations-055.md#op-17e0b0a1e2ad9f), [get subcontracting return rates](operations-055.md#op-e91d2c657a7dcc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L945) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L589)

<a id="op-fe4c67006a8d4a"></a>
### Serialand Batch Bundle.set serial and batch values

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_serial_and_batch_values`

**Inputs** self, parent, row, qty\_field = no value.

**State and service calls** call db\_set on self · request set\_value on “Serial and Batch Entry”.

**Local steps**

- Evaluate self.validate\_not\_linked\_to\_another\_draft(parent, row).
- Set values\_to\_set from mapping(“is\_cancelled” → 0).
- If (not self.voucher\_no or self.voucher\_no differs from row.parent).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.voucher\_no → self.voucher\_no differs from row.parent.
  - Set values\_to\_set at “voucher\_no” from row.parent.
- If self.voucher\_type differs from parent.doctype.
  - Set values\_to\_set at “voucher\_type” from parent.doctype.
- If (not self.voucher\_detail\_no or self.voucher\_detail\_no differs from row.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.voucher\_detail\_no → self.voucher\_detail\_no differs from row.name.
  - Set values\_to\_set at “voucher\_detail\_no” from row.name.
- If (row.get(“doctype”) equals “Packed Item” and row.get(“parent\_detail\_docname”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“doctype”) equals “Packed Item” → row.get(“parent\_detail\_docname”).
  - Set values\_to\_set at “voucher\_detail\_no” from row.get(“parent\_detail\_docname”).
- If (parent.get(“posting\_date”) and parent.get(“posting\_time”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.get(“posting\_date”) → parent.get(“posting\_time”).
  - Set posting\_datetime from combine\_datetime(parent.posting\_date, parent.posting\_time).
  - If (not self.posting\_datetime or self.posting\_datetime differs from posting\_datetime).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.posting\_datetime → self.posting\_datetime differs from posting\_datetime.
    - Set values\_to\_set at “posting\_datetime” from posting\_datetime.
- If (parent.doctype belongs to list(“Delivery Note”, “Purchase Receipt”, “Purchase Invoice”, “Sales Invoice”) and parent.get(“is\_return”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.doctype belongs to list(“Delivery Note”, “Purchase Receipt”, “Purchase Invoice”, “Sales Invoice”) → parent.get(“is\_return”).
  - Set return\_ref\_field from (Platform.scrub(parent.doctype) + “\_item”).
  - If parent.doctype equals “Delivery Note”.
    - Set return\_ref\_field from “dn\_detail”.
  - If row.get(return\_ref\_field).
    - Set values\_to\_set at “returned\_against” from row.get(return\_ref\_field).
- Evaluate self.db\_set(values\_to\_set).
- Evaluate values\_to\_set.pop(“returned\_against”, no value).
- Evaluate Platform.db.set\_value(“Serial and Batch Entry”, mapping(“parent” → self.name), values\_to\_set, update\_modified = false).
- Evaluate self.calculate\_total\_qty(save = true).
- If (self.docstatus equals 0 and self.type\_of\_transaction equals “Inward”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 0 → self.type\_of\_transaction equals “Inward”.
  - Evaluate self.set\_incoming\_rate(parent = parent, row = row, save = true).
- If (self.docstatus equals 0 and parent.get(“is\_return”) and parent.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 0 → parent.get(“is\_return”) → parent.is\_new().
  - Evaluate self.reset\_qty(row, qty\_field = qty\_field).
- Evaluate self.calculate\_qty\_and\_amount(save = true).
- Evaluate self.validate\_quantity(row, qty\_field = qty\_field).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate not linked to another draft](operations-055.md#op-6c03e5abcc9485), [calculate total qty](operations-054.md#op-6b200e57dfcd7e), [set incoming rate](operations-054.md#op-25f1bfa19f8d54), [reset qty](operations-055.md#op-d1358fe33319de), [calculate qty and amount](operations-055.md#op-156485bd00687a), [validate quantity](operations-055.md#op-24df5cb0189a5c).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L948) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L592)

<a id="op-6c03e5abcc9485"></a>
### Serialand Batch Bundle.validate not linked to another draft

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_validate_not_linked_to_another_draft`

**Inputs** self, parent, row.

**Record and data access** read self.voucher\_type via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Serial and Batch Bundle {1} belongs to {2} {3}. Select or create another bundle.”.format(row.idx, bold(self.name), self.voucher\_type, get\_link\_to\_form(self.voucher\_type, self.voucher\_no)).

**Local steps**

- If not (self.voucher\_type and self.voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type → self.voucher\_no.
  - Return no value.
- If (self.voucher\_type equals parent.doctype and self.voucher\_no equals row.parent).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals parent.doctype → self.voucher\_no equals row.parent.
  - Return no value.
- If Platform.db.get\_value(self.voucher\_type, self.voucher\_no, “docstatus”) differs from 0.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Row #{0}: Serial and Batch Bundle {1} belongs to {2} {3}. Select or create another bundle.”.format(row.idx, bold(self.name), self.voucher\_type, get\_link\_to\_form(self.voucher\_type ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1093) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L590)

<a id="op-75e9b7aa0e3e14"></a>
### Serialand Batch Bundle.validate voucher no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_voucher_number`

**Inputs** self.

**Record and data access** read self.voucher\_type via exists · read self.voucher\_type via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not (self.voucher\_type and self.voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type → self.voucher\_no.
  - Return no value.
- If (self.docstatus equals 1 and self.voucher\_no and not Platform.db.exists(self.voucher\_type, self.voucher\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.voucher\_no → not Platform.db.exists(self.voucher\_type, self.voucher\_no).
  - Evaluate self.throw\_error\_message(translated “The {0} # {1} does not exist”.format(self.voucher\_type, self.voucher\_no)).
- If self.flags.ignore\_voucher\_validation.
  - Return no value.
- If (self.docstatus equals 1 and Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “docstatus”) differs from 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “docstatus”) differs from 1.
  - Evaluate self.throw\_error\_message(translated “The {0} # {1} should be submitted first.”.format(self.voucher\_type, self.voucher\_no)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw error message](operations-054.md#op-2c6f3f95226244).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “docstatus”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L619)

<a id="op-04fc2eda12163a"></a>
### Serialand Batch Bundle.check future entries exists

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_check_future_entries_exists`

**Inputs** self, is\_cancelled = false.

**Explicit results** no value.

**Explicit failure paths** validation helper with SerialNoExistsInFutureTransactionError — msg.

**Local steps**

- Bind dependencies is\_adjustment\_voucher.
- If (self.flags and self.flags.via\_landed\_cost\_voucher).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags → self.flags.via\_landed\_cost\_voucher.
  - Return no value.
- If is\_adjustment\_voucher(self.voucher\_type, self.voucher\_no).
  - Return no value.
- Set serial\_nos from list().
- Set batches from list().
- If self.voucher\_type equals “Stock Reconciliation”.
  - Set tuple(serial\_nos, batches) from self.get\_serial\_nos\_for\_validate(is\_cancelled = is\_cancelled).
- Otherwise.
  - Set batches from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
    - Draw d from self.entries, keep a combination only if (d.batch\_no).
- If (self.voucher\_type differs from “Stock Reconciliation” and not self.flags.ignore\_validate\_serial\_batch and self.has\_serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type differs from “Stock Reconciliation” → not self.flags.ignore\_validate\_serial\_batch → self.has\_serial\_no.
  - Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
    - Draw d from self.entries, keep a combination only if (d.serial\_no).
- If (self.has\_batch\_no and not self.has\_serial\_no and not batches).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_batch\_no → not self.has\_serial\_no → not batches.
  - Return no value.
- Set child from Platform.qb.DocType(“Serial and Batch Entry”).
- Set timestamp\_condition from child.posting\_datetime &gt; self.posting\_datetime.
- Set future\_entries from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).distinct().where(((((nested operand in the con ….
- If (self.has\_batch\_no and not self.has\_serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_batch\_no → not self.has\_serial\_no.
  - Set future\_entries from future\_entries.where(child.voucher\_type equals “Stock Reconciliation”).
- If serial\_nos.
  - Set future\_entries from future\_entries.where((child.serial\_no.isin(serial\_nos) bitwise or (child.warehouse equals self.warehouse bitwise and child.voucher\_type equals “Stock Reconciliation”))).
- Otherwise.
  - If self.has\_serial\_no.
    - Set future\_entries from future\_entries.where((child.warehouse equals self.warehouse bitwise and child.voucher\_type equals “Stock Reconciliation”)).
  - Otherwise.
    - If batches.
      - Set future\_entries from future\_entries.where((child.batch\_no.isin(batches) bitwise and child.warehouse equals self.warehouse)).
- Set future\_entries from future\_entries.run(as\_dict = true).
- If future\_entries.
  - If self.has\_serial\_no.
    - Set title from translated “Serial No Exists In Future Transaction(s)”.
  - Otherwise.
    - Set title from translated “Batches Exists In Future Transaction(s)”.
  - Set msg from translated “Since the stock reconciliation exists for future dates, cancel it first. For Serial/Batch, if you want to ma …”.
  - Update msg using + text in the contract.
  - For each d in future\_entries.
    - Set number from d.serial\_no when self.has\_serial\_no, otherwise d.batch\_no.
      - Value choice on self.has\_serial\_no — true gives d.serial\_no, false gives d.batch\_no.
    - Set link from get\_link\_to\_form(d.voucher\_type, d.voucher\_no).
    - Update msg using + ((text in the contract + translated “{0} in {1}”.format(number, link)) + “&lt;/li&gt;”).
  - Update msg using + “&lt;/li&gt;&lt;/ul&gt;”.
  - Call the validation error handler Platform.throw(msg, title = title, exc = SerialNoExistsInFutureTransactionError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get serial nos for validate](operations-055.md#op-adbcf8f466d0f4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L560)

<a id="op-adbcf8f466d0f4"></a>
### Serialand Batch Bundle.get serial nos for validate

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_serial_numbers_for_validate`

**Inputs** self, is\_cancelled = false.

**Explicit results** tuple(serial\_nos, batch\_nos).

**Local steps**

- Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
  - Draw d from self.entries, keep a combination only if (d.serial\_no).
- Set batches from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
  - Draw d from self.entries, keep a combination only if (d.batch\_no).
- Set tuple(skip\_serial\_nos, skip\_batches) from self.get\_skip\_serial\_nos\_for\_stock\_reconciliation(is\_cancelled = is\_cancelled).
- Set serial\_nos from list((set(sorted(serial\_nos)) − set(sorted(skip\_serial\_nos)))).
- Set batch\_nos from list((set(sorted(batches)) − set(sorted(skip\_batches)))).
- Return tuple(serial\_nos, batch\_nos).

**Methods declared on this owner** [get skip serial nos for stock reconciliation](operations-055.md#op-0576fac04ef227).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0806.json#L5839) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L575)

<a id="op-0576fac04ef227"></a>
### Serialand Batch Bundle.get skip serial nos for stock reconciliation

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_skip_serial_numbers_for_stock_reconciliation`

**Inputs** self, is\_cancelled = false.

**Explicit results** tuple(list(), list()) · tuple(list(serial\_nos.intersection(current\_serial\_nos)), list()) · tuple(list(serial\_nos.intersection(current\_serial\_nos)), list(data.batch\_no)) · tuple(list(current\_serial\_nos), list(current\_batches)) · tuple(list(serial\_nos.intersection(current\_serial\_nos)), list(batches.intersection(current\_batches))).

**Local steps**

- Set data from get\_stock\_reco\_details(self.voucher\_detail\_no).
- If not data.
  - Return tuple(list(), list()).
- Set current\_serial\_nos from set().
- Set serial\_nos from set().
- Set current\_batches from set().
- Set batches from set().
- If data.current\_serial\_no.
  - Set current\_serial\_nos from set(parse\_serial\_nos(data.current\_serial\_no)).
  - Set serial\_nos from set(parse\_serial\_nos(data.serial\_no)) when data.serial\_no, otherwise set(list()).
    - Value choice on data.serial\_no — true gives set(parse\_serial\_nos(data.serial\_no)), false gives set(list()).
  - Return tuple(list(serial\_nos.intersection(current\_serial\_nos)), list()).
- Otherwise.
  - If (data.batch\_no and data.current\_qty equals data.qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.batch\_no → data.current\_qty equals data.qty.
    - If (self.has\_serial\_no and data.current\_serial\_and\_batch\_bundle and data.serial\_and\_batch\_bundle).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → data.current\_serial\_and\_batch\_bundle → data.serial\_and\_batch\_bundle.
      - Set current\_serial\_nos from set(get\_serial\_nos\_from\_bundle(data.current\_serial\_and\_batch\_bundle)).
      - Set serial\_nos from set(get\_serial\_nos\_from\_bundle(data.serial\_and\_batch\_bundle)).
    - Return tuple(list(serial\_nos.intersection(current\_serial\_nos)), list(data.batch\_no)).
  - Otherwise.
    - If data.current\_serial\_and\_batch\_bundle.
      - If self.has\_serial\_no.
        - Set current\_serial\_nos from set(get\_serial\_nos\_from\_bundle(data.current\_serial\_and\_batch\_bundle)).
      - Otherwise.
        - Set current\_batches from set(get\_batches\_from\_bundle(data.current\_serial\_and\_batch\_bundle)).
      - If is\_cancelled.
        - Return tuple(list(current\_serial\_nos), list(current\_batches)).
      - If self.has\_serial\_no.
        - Set serial\_nos from set(get\_serial\_nos\_from\_bundle(data.serial\_and\_batch\_bundle)) when data.serial\_and\_batch\_bundle, otherwise set(list()).
          - Value choice on data.serial\_and\_batch\_bundle — true gives set(get\_serial\_nos\_from\_bundle(data.serial\_and\_batch\_bundle)), false gives set(list()).
      - Otherwise.
        - If (self.has\_batch\_no and data.serial\_and\_batch\_bundle).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_batch\_no → data.serial\_and\_batch\_bundle.
          - Set batches from set(get\_batches\_from\_bundle(data.serial\_and\_batch\_bundle)).
      - Return tuple(list(serial\_nos.intersection(current\_serial\_nos)), list(batches.intersection(current\_batches))).
- Return tuple(list(), list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L932) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L576)

<a id="op-d1358fe33319de"></a>
### Serialand Batch Bundle.reset qty

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_reset_quantity`

**Inputs** self, row, qty\_field = no value.

**State and service calls** call db\_set on d · call save on self.

**Local steps**

- Set qty\_field from self.get\_qty\_field(row, qty\_field = qty\_field).
- Set qty from abs(flt(self.get\_row\_qty(row, qty\_field), self.precision(“total\_qty”))).
- Set idx from no value.
- While qty &gt; 0.
  - For each d in self.entries.
    - Set row\_qty from abs(flt(d.qty, d.precision(“qty”))).
    - If row\_qty ≥ qty.
      - Evaluate d.db\_set(“qty”, qty when self.type\_of\_transaction equals “Inward”, otherwise (qty × negative 1)).
        - Value choice on self.type\_of\_transaction equals “Inward” — true gives qty, false gives (qty × negative 1).
      - Set qty from 0.
      - Set idx from d.idx.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Otherwise.
      - Set qty from flt((qty − row\_qty), d.precision(“qty”)).
      - Set idx from d.idx.
- If (idx and len(self.entries) &gt; idx).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in idx → len(self.entries) &gt; idx.
  - Set remove\_rows from list().
  - For each d in self.entries.
    - If d.idx &gt; idx.
      - Evaluate remove\_rows.append(d).
  - For each d in remove\_rows.
    - Evaluate self.entries.remove(d).
  - Set self.flags.ignore\_links from true.
  - Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty field](operations-055.md#op-262c8890c68ef3), [get row qty](operations-055.md#op-e7a72ae97f5861).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L584)

<a id="op-e7a72ae97f5861"></a>
### Serialand Batch Bundle.get row qty

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_row_qty`

**Inputs** self, row, qty\_field.

**Declared result** float.

**Explicit results** flt(row.get(“stock\_qty”)) · (flt(row.get(qty\_field)) × flt((row.get(“conversion\_factor”) or 1))) · flt(row.get(qty\_field)).

**Local steps**

- If (qty\_field equals “qty” and row.get(“stock\_qty”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_field equals “qty” → row.get(“stock\_qty”).
  - Return flt(row.get(“stock\_qty”)).
- If qty\_field equals “rejected\_qty”.
  - Return (flt(row.get(qty\_field)) × flt((row.get(“conversion\_factor”) or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“conversion\_factor”) → 1.
- Return flt(row.get(qty\_field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1086) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L583)

<a id="op-24df5cb0189a5c"></a>
### Serialand Batch Bundle.validate quantity

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_quantity`

**Inputs** self, row, qty\_field = no value.

**Local steps**

- Set qty\_field from self.get\_qty\_field(row, qty\_field = qty\_field).
- Set qty from self.get\_row\_qty(row, qty\_field).
- Set precision from row.precision(qty\_field).
- If abs((abs(flt(self.total\_qty, precision)) − abs(flt(qty, precision)))) &gt; 0.01.
  - Set total\_qty from Platform.format\_value(abs(flt(self.total\_qty)), “Float”, row).
  - Set set\_qty from Platform.format\_value(abs(flt(qty)), “Float”, row).
  - Evaluate self.throw\_error\_message(translated “Total quantity {0} in the Serial and Batch Bundle {1} does not match with the quantity {2} for the Item {3}  …”.format(total\_qty, bold(self.name), set\_qty, bold(self.it ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty field](operations-055.md#op-262c8890c68ef3), [get row qty](operations-055.md#op-e7a72ae97f5861), [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L607)

<a id="op-17e0b0a1e2ad9f"></a>
### Serialand Batch Bundle.get transfer rates

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_transfer_rates`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Serial and Batch Bundle” via get\_value · read “Stock Entry Detail” via get\_value · read “Serial and Batch Entry” via get\_all.

**Explicit results** mapping() · mapping of tuple(d.serial\_no, d.batch\_no) → (flt(d.incoming\_rate) + additional\_cost\_per\_unit) for d drawn from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → outward\_bundle), field ….

**Local steps**

- Bind dependencies is\_serial\_no\_wise\_valuation\_disabled.
- If (self.voucher\_type differs from “Stock Entry” or not self.voucher\_detail\_no or is\_serial\_no\_wise\_valuation\_disabled(self.item\_code)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.voucher\_type differs from “Stock Entry” → not self.voucher\_detail\_no → is\_serial\_no\_wise\_valuation\_disabled(self.item\_code).
  - Return mapping().
- Set outward\_bundle from Platform.db.get\_value(“Serial and Batch Bundle”, mapping(“voucher\_type” → self.voucher\_type, “voucher\_detail\_no” → self.voucher\_detail\_no, “type\_of\_transaction” → “Outward”, “is\_cancelled” → 0)).
- If not outward\_bundle.
  - Return mapping().
- Set tuple(additional\_cost, transfer\_qty) from Platform.db.get\_value(“Stock Entry Detail”, self.voucher\_detail\_no, list(“additional\_cost”, “transfer\_qty”)).
- Set additional\_cost\_per\_unit from (flt(additional\_cost) ÷ flt(transfer\_qty)).
- Return mapping of tuple(d.serial\_no, d.batch\_no) → (flt(d.incoming\_rate) + additional\_cost\_per\_unit) for d drawn from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → outward\_bundle), field ….
  - Draw d from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → outward\_bundle), fields = list(“serial\_no”, “batch\_no”, “incoming\_rate”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1088) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L585)

<a id="op-e91d2c657a7dcc"></a>
### Serialand Batch Bundle.get subcontracting return rates

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_subcontracting_return_rates`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Subcontracting Receipt Supplied Item” via get\_value · resolve a document from “Subcontracting Receipt” via get\_doc.

**Explicit results** mapping() · mapping of key → identity.rate for tuple(key, identity) drawn from consumed.items().

**Local steps**

- If (self.voucher\_type differs from “Subcontracting Receipt” or not self.voucher\_detail\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.voucher\_type differs from “Subcontracting Receipt” → not self.voucher\_detail\_no.
  - Return mapping().
- Set row from Platform.db.get\_value(“Subcontracting Receipt Supplied Item”, self.voucher\_detail\_no, list(“parent”, “reference\_name”, “rm\_item\_code”), as\_dict = true).
- If not row.
  - Return mapping().
- Set receipt from Platform.get\_doc(“Subcontracting Receipt”, row.parent).
- If (not receipt.is\_return or row.reference\_name belongs to receipt.get\_rejected\_return\_rows()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not receipt.is\_return → row.reference\_name belongs to receipt.get\_rejected\_return\_rows().
  - Return mapping().
- Set receipt\_item from receipt.get(“items”, mapping(“name” → row.reference\_name)) at 0.subcontracting\_receipt\_item.
- Set consumed from receipt.get\_consumed\_serial\_batches().get(tuple(receipt\_item, row.rm\_item\_code), mapping()).
- Return mapping of key → identity.rate for tuple(key, identity) drawn from consumed.items().
  - Draw tuple(key, identity) from consumed.items().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1087) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L584)

<a id="op-31ece2be62ab3b"></a>
### Serialand Batch Bundle.get transit rate

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_transit_rate`

**Inputs** self, row.

**Declared result** float.

**Record and data access** read self.child\_table via get\_value.

**Explicit results** 0.0 · (flt(row.get(“sales\_incoming\_rate”)) ÷ (flt(row.get(“conversion\_factor”)) or 1.0)).

**Local steps**

- If not (row and row.get(“sales\_incoming\_rate”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → row.get(“sales\_incoming\_rate”).
  - If not (self.voucher\_detail\_no and self.voucher\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_detail\_no → self.voucher\_no.
    - Return 0.0.
  - Set row from (Platform.db.get\_value(self.child\_table, self.voucher\_detail\_no, list(“sales\_incoming\_rate”, “conversion\_factor”), as\_dict = true) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(self.child\_table, self.voucher\_detail\_no, list(“sales\_incoming\_rate”, “conversion\_factor”), as\_dict = true) → mapping().
- Return (flt(row.get(“sales\_incoming\_rate”)) ÷ (flt(row.get(“conversion\_factor”)) or 1.0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.get(“conversion\_factor”)) → 1.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1089) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L586)

<a id="op-262c8890c68ef3"></a>
### Serialand Batch Bundle.get qty field

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_quantity_field`

**Inputs** self, row, qty\_field = no value.

**Declared result** str.

**Explicit results** qty\_field.

**Local steps**

- If not qty\_field.
  - Set qty\_field from “qty”.
- If row.get(“doctype”) equals “Subcontracting Receipt Supplied Item”.
  - Set qty\_field from “consumed\_qty”.
- Otherwise.
  - If row.get(“doctype”) equals “Stock Entry Detail”.
    - Set qty\_field from “transfer\_qty”.
  - Otherwise.
    - If (row.get(“doctype”) belongs to list(“Sales Invoice Item”, “Purchase Invoice Item”) and qty\_field equals “qty”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“doctype”) belongs to list(“Sales Invoice Item”, “Purchase Invoice Item”) → qty\_field equals “qty”.
      - Set qty\_field from “stock\_qty”.
- Return qty\_field.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L571)

<a id="op-a6d3f40e6b7099"></a>
### Serialand Batch Bundle.set is outward

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_is_outward`

**Inputs** self.

**Local steps**

- For each row in self.entries.
  - If (self.type\_of\_transaction equals “Outward” and row.qty &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.type\_of\_transaction equals “Outward” → row.qty &gt; 0.
    - Update row.qty using × negative 1.
  - Otherwise.
    - If (self.type\_of\_transaction equals “Inward” and row.qty &lt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.type\_of\_transaction equals “Inward” → row.qty &lt; 0.
      - Update row.qty using × negative 1.
  - Set row.is\_outward from 1 when self.type\_of\_transaction equals “Outward”, otherwise 0.
    - Value choice on self.type\_of\_transaction equals “Outward” — true gives 1, false gives 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L942) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L591)

<a id="op-36bc8706c404e8"></a>
### Serialand Batch Bundle.set warehouse

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_warehouse`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- For each row in self.entries.
  - If row.warehouse differs from self.warehouse.
    - Set row.warehouse from self.warehouse.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L1204) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L951) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L595)

<a id="op-156485bd00687a"></a>
### Serialand Batch Bundle.calculate qty and amount

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_calculate_quantity_and_amount`

**Inputs** self, save = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.total\_amount from 0.0.
- Set self.total\_qty from 0.0.
- Set self.avg\_rate from 0.0.
- For each row in self.entries.
  - Set rate from flt(row.incoming\_rate).
  - Set row.stock\_value\_difference from (flt(row.qty) × rate).
  - Update self.total\_amount using + (flt(row.qty) × rate).
  - Update self.total\_qty using + flt(row.qty).
- If self.total\_qty.
  - Set self.avg\_rate from (flt(self.total\_amount) ÷ flt(self.total\_qty)).
- If save.
  - Evaluate self.db\_set(mapping(“total\_qty” → self.total\_qty, “avg\_rate” → self.avg\_rate, “total\_amount” → self.total\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L1321) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L913) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L558)

<a id="op-e3aa12309b354c"></a>
### Serialand Batch Bundle.calculate outgoing rate

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_calculate_outgoing_rate`

**Inputs** self.

**Record and data access** read self.voucher\_type via get\_cached\_value.

**Explicit results** no value · false · Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “is\_return”) · not Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “is\_return”) · Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “purpose”) belongs to list(“Material Receipt”).

**Local steps**

- If not (self.has\_serial\_no and self.entries).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → self.entries.
  - Return no value.
- If not (self.voucher\_type and self.voucher\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type → self.voucher\_no.
  - Return false.
- If self.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”).
  - Return Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “is\_return”).
- Otherwise.
  - If self.voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”).
    - Return not Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “is\_return”).
  - Otherwise.
    - If self.voucher\_type equals “Stock Entry”.
      - Return Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “purpose”) belongs to list(“Material Receipt”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “is\_return”), Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L1759) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L912) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L557)

<a id="op-a8084770ff6f10"></a>
### Serialand Batch Bundle.validate serial and batch no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_and_batch_number`

**Inputs** self.

**Explicit failure paths** validation helper — translated msg · validation helper — translated “At row {0}: Qty is mandatory for the batch {1}”.format(bold(row.idx), bold(row.batch\_no)) · validation helper — translated “At row {0}: Serial No is mandatory for Item {1}”.format(bold(row.idx), bold(self.item\_code)) · validation helper — translated “At row {0}: Batch No is mandatory for Item {1}”.format(bold(row.idx), bold(self.item\_code)).

**Local steps**

- If (self.item\_code and not self.has\_serial\_no and not self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → not self.has\_serial\_no → not self.has\_batch\_no.
  - Set msg from formatted text The Item {self.item\_code} does not have Serial No or Batch No.
  - Call the validation error handler Platform.throw(translated msg).
- Set serial\_nos from list().
- Set batch\_nos from set().
- Set serial\_batches from mapping().
- For each row in self.entries.
  - If (not row.qty and row.batch\_no and not row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.qty → row.batch\_no → not row.serial\_no.
    - If (self.voucher\_type equals “Stock Reconciliation” and self.type\_of\_transaction equals “Inward”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Stock Reconciliation” → self.type\_of\_transaction equals “Inward”.
      - Continue with the next iteration or loop test.
    - Call the validation error handler Platform.throw(translated “At row {0}: Qty is mandatory for the batch {1}”.format(bold(row.idx), bold(row.batch\_no))).
  - If (self.has\_serial\_no and not row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → not row.serial\_no.
    - Call the validation error handler Platform.throw(translated “At row {0}: Serial No is mandatory for Item {1}”.format(bold(row.idx), bold(self.item\_code)), title = translated “Serial No is mandatory”).
  - If (self.has\_batch\_no and not row.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_batch\_no → not row.batch\_no.
    - Call the validation error handler Platform.throw(translated “At row {0}: Batch No is mandatory for Item {1}”.format(bold(row.idx), bold(self.item\_code)), title = translated “Batch No is mandatory”).
  - If row.serial\_no.
    - Evaluate serial\_nos.append(row.serial\_no).
  - If row.batch\_no.
    - Evaluate batch\_nos.add(row.batch\_no).
  - If (row.serial\_no and row.batch\_no and self.type\_of\_transaction equals “Outward”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_no → row.batch\_no → self.type\_of\_transaction equals “Outward”.
    - Evaluate serial\_batches.setdefault(row.serial\_no, row.batch\_no).
- If serial\_nos.
  - Evaluate self.validate\_incorrect\_serial\_nos(serial\_nos).
- If batch\_nos.
  - Evaluate self.validate\_incorrect\_batch\_nos(list(batch\_nos)).
- If serial\_batches.
  - Evaluate self.validate\_serial\_batch\_no(serial\_batches).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate incorrect serial nos](operations-055.md#op-6de3199ac80020), [validate incorrect batch nos](operations-055.md#op-0acb01fc43e0e1), [validate serial batch no](operations-055.md#op-7d155d86e55e30).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L968) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L612)

<a id="op-7d155d86e55e30"></a>
### Serialand Batch Bundle.validate serial batch no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_batch_number`

**Inputs** self, serial\_batches.

**Record and data access** read “Serial No” via get\_all.

**Local steps**

- Set correct\_batches from Platform.\_dict(Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, list(nested operand in the contract.keys()))), fields = list(“name”, “batch\_no”), as\_list = true)).
- For each tuple(serial\_no, batch\_no) in serial\_batches.items().
  - If (correct\_batches.get(serial\_no) and correct\_batches.get(serial\_no) differs from batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in correct\_batches.get(serial\_no) → correct\_batches.get(serial\_no) differs from batch\_no.
    - Evaluate self.throw\_error\_message(translated “Serial No {0} does not belong to Batch No {1}”.format(bold(serial\_no), bold(batch\_no))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L970) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L614)

<a id="op-6de3199ac80020"></a>
### Serialand Batch Bundle.validate incorrect serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_incorrect_serial_numbers`

**Inputs** self, serial\_nos.

**Record and data access** read “Serial No” via get\_all.

**Local steps**

- Set incorrect\_serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, serial\_nos), “item\_code” → tuple(“!=”, self.item\_code)), fields = list(“name”)).
- If incorrect\_serial\_nos.
  - Set incorrect\_serial\_nos from “, ”.join(list of d.name for d drawn from incorrect\_serial\_nos).
    - Draw d from incorrect\_serial\_nos.
  - Evaluate self.throw\_error\_message(translated “Serial Nos {0} does not belong to Item {1}”.format(bold(incorrect\_serial\_nos), bold(self.item\_code))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L961) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L605)

<a id="op-0acb01fc43e0e1"></a>
### Serialand Batch Bundle.validate incorrect batch nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_incorrect_batch_numbers`

**Inputs** self, batch\_nos.

**Record and data access** read “Batch” via get\_all.

**Local steps**

- Set incorrect\_batch\_nos from Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, batch\_nos), “item” → tuple(“!=”, self.item\_code)), fields = list(“name”)).
- If incorrect\_batch\_nos.
  - Set incorrect\_batch\_nos from “, ”.join(list of d.name for d drawn from incorrect\_batch\_nos).
    - Draw d from incorrect\_batch\_nos.
  - Evaluate self.throw\_error\_message(translated “Batch Nos {0} does not belong to Item {1}”.format(bold(incorrect\_batch\_nos), bold(self.item\_code))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L960) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L604)

<a id="op-5bdc8fa3a3a004"></a>
### Serialand Batch Bundle.validate serial and batch no for returned

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_and_batch_number_for_returned`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.returned\_against.
  - Return no value.
- If self.voucher\_type does not belong to list(“Purchase Receipt”, “Purchase Invoice”, “Sales Invoice”, “Delivery Note”).
  - Return no value.
- Set data from self.get\_orignal\_document\_data().
- If not data.
  - Return no value.
- Set tuple(serial\_nos, batches) from tuple(list(), list()).
- Set current\_serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
  - Draw d from self.entries, keep a combination only if (d.serial\_no).
- Set current\_batches from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
  - Draw d from self.entries, keep a combination only if (d.batch\_no).
- For each d in data.
  - If self.has\_serial\_no.
    - If d.serial\_and\_batch\_bundle.
      - Set serial\_nos from get\_serial\_nos\_from\_bundle(d.serial\_and\_batch\_bundle).
    - Otherwise.
      - Set serial\_nos from parse\_serial\_nos(d.serial\_no).
  - Otherwise.
    - If self.has\_batch\_no.
      - If d.serial\_and\_batch\_bundle.
        - Set batches from get\_batches\_from\_bundle(d.serial\_and\_batch\_bundle).
      - Otherwise.
        - Set batches from Platform.\_dict(mapping(d.batch\_no → d.stock\_qty)).
      - If batches.
        - Set batches from list of d for d drawn from batches where batches at d &gt; 0.
          - Draw d from batches, keep a combination only if (batches at d &gt; 0).
  - If serial\_nos.
    - If not set(current\_serial\_nos).issubset(set(serial\_nos)).
      - Evaluate self.throw\_error\_message(formatted text Serial Nos {bold(“, ”.join(serial\_nos))} are not part of the original document.).
  - If batches.
    - If not set(current\_batches).issubset(set(batches)).
      - Evaluate self.throw\_error\_message(formatted text Batch Nos {bold(“, ”.join(batches))} are not part of the original document.).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get orignal document data](operations-056.md#op-a64ba667065bd0), [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L4092) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L969) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L613)
