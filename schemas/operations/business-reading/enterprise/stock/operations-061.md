# Inventory and warehouses · operations 61

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Serial batch bundle

<a id="op-5154e4af494f6a"></a>
### Serial Batch Bundle.set serial and batch bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_set_serial_and_batch_bundle`

**Inputs** self, sn\_doc.

**Record and data access** read “Stock Entry Detail” via get\_value · read “Stock Settings” via get\_single\_value · read “Packed Item” via get\_value.

**State and service calls** call db\_set on self.sle · request set\_value on self.child\_doctype · request set\_value on doctype.

**Local steps**

- Set self.sle.auto\_created\_serial\_and\_batch\_bundle from 1.
- Evaluate self.sle.db\_set(mapping(“serial\_and\_batch\_bundle” → sn\_doc.name, “auto\_created\_serial\_and\_batch\_bundle” → 1)).
- If sn\_doc.is\_rejected.
  - Evaluate Platform.db.set\_value(self.child\_doctype, self.sle.voucher\_detail\_no, “rejected\_serial\_and\_batch\_bundle”, sn\_doc.name).
- Otherwise.
  - Set values\_to\_update from mapping(“serial\_and\_batch\_bundle” → sn\_doc.name).
  - If (self.sle.actual\_qty &lt; 0 and self.is\_material\_transfer()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.actual\_qty &lt; 0 → self.is\_material\_transfer().
    - Set basic\_rate from flt(sn\_doc.avg\_rate).
    - Set ste\_detail from Platform.db.get\_value(“Stock Entry Detail”, self.sle.voucher\_detail\_no, list(“additional\_cost”, “landed\_cost\_voucher\_amount”, “transfer\_qty”), as\_dict = true).
    - Set additional\_cost from 0.0.
    - If ste\_detail.
      - Set additional\_cost from ((flt(ste\_detail.additional\_cost) + flt(ste\_detail.landed\_cost\_voucher\_amount)) ÷ flt(ste\_detail.transfer\_qty)).
    - Set values\_to\_update at “basic\_rate” from basic\_rate.
    - Set values\_to\_update at “valuation\_rate” from (basic\_rate + additional\_cost).
  - If not Platform.get\_single\_value(“Stock Settings”, “do\_not\_update\_serial\_batch\_on\_creation\_of\_auto\_bundle”).
    - If sn\_doc.has\_serial\_no.
      - Set values\_to\_update at “serial\_no” from “,”.join(generator of cstr(d.serial\_no) for d drawn from sn\_doc.entries).
        - Draw d from sn\_doc.entries.
    - Otherwise.
      - If (sn\_doc.has\_batch\_no and len(sn\_doc.entries) equals 1).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in sn\_doc.has\_batch\_no → len(sn\_doc.entries) equals 1.
        - Set values\_to\_update at “batch\_no” from sn\_doc.entries at 0.batch\_no.
  - Set doctype from self.child\_doctype.
  - Set name from self.sle.voucher\_detail\_no.
  - If sn\_doc.is\_packed.
    - Set doctype from “Packed Item”.
    - Set name from Platform.db.get\_value(“Packed Item”, mapping(“parent\_detail\_docname” → sn\_doc.voucher\_detail\_no, “item\_code” → self.sle.item\_code, “serial\_and\_batch\_bundle” → tuple(“is”, “not set”)), “name”).
  - Evaluate Platform.db.set\_value(doctype, name, values\_to\_update).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is material transfer](operations-060.md#op-1292a2c6991f3b).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “do\_not\_update\_serial\_batch\_on\_creation\_of\_auto\_bundle”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L2593) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1086) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L658)

<a id="op-ee6f06dbc10034"></a>
### Serial Batch Bundle.child doctype

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_child_record_type`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** child\_doctype.

**Local steps**

- Set child\_doctype from (self.sle.voucher\_type + “ Item”).
- If (self.sle.voucher\_type equals “Subcontracting Receipt” and self.sle.dependant\_sle\_voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.voucher\_type equals “Subcontracting Receipt” → self.sle.dependant\_sle\_voucher\_detail\_no.
  - Set child\_doctype from “Subcontracting Receipt Supplied Item”.
- If self.sle.voucher\_type equals “Stock Entry”.
  - Set child\_doctype from “Stock Entry Detail”.
- If self.sle.voucher\_type equals “Asset Capitalization”.
  - Set child\_doctype from “Asset Capitalization Stock Item”.
- If self.sle.voucher\_type equals “Asset Repair”.
  - Set child\_doctype from “Asset Repair Consumed Item”.
- Return child\_doctype.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L3619) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1070) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L642)

<a id="op-58e15093bfdbaf"></a>
### Serial Batch Bundle.is rejected entry

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_is_rejected_entry`

**Inputs** self.

**Explicit results** is\_rejected(self.sle.voucher\_type, self.sle.voucher\_detail\_no, self.sle.warehouse).

**Local steps**

- Return is\_rejected(self.sle.voucher\_type, self.sle.voucher\_detail\_no, self.sle.warehouse).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L3920) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1077) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L649)

<a id="op-323cf5ccc8e185"></a>
### Serial Batch Bundle.is packed entry

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_is_packed_entry`

**Inputs** self.

**Record and data access** read (self.sle.voucher\_type + “ Item”) via get\_value · read “Item” via get\_value.

**Explicit results** Platform.db.get\_value(“Item”, item\_code, “is\_stock\_item”) equals 0 · false.

**Local steps**

- If self.sle.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”).
  - Set item\_code from Platform.db.get\_value((self.sle.voucher\_type + “ Item”), self.sle.voucher\_detail\_no, “item\_code”).
  - If item\_code differs from self.sle.item\_code.
    - Return Platform.db.get\_value(“Item”, item\_code, “is\_stock\_item”) equals 0.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L4004) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1075) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L647)

<a id="op-0a86cdadca10be"></a>
### Serial Batch Bundle.process batch no

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_process_batch_number`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If (not self.sle.is\_cancelled and not self.sle.serial\_and\_batch\_bundle and self.item\_details.has\_batch\_no equals 1 and ((self.item\_details.create\_new\_batch and self.sle.actual\_qty &gt; 0) or (Platform.get\_single ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sle.is\_cancelled → not self.sle.serial\_and\_batch\_bundle → self.item\_details.has\_batch\_no equals 1 → ((self.item\_details.create\_new\_batch and self.sle.actual\_qty &gt; 0) or (Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”) and self.sle.actual\_qty &lt; 0) or (self.sl ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.item\_details.create\_new\_batch and self.sle.actual\_qty &gt; 0) → (Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”) and self.sle.actual\_qty &lt; 0) → (self.sle.actual\_qty &gt; 0 and self.get\_transit\_package()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_details.create\_new\_batch → self.sle.actual\_qty &gt; 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”) → self.sle.actual\_qty &lt; 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.actual\_qty &gt; 0 → self.get\_transit\_package().
  - Evaluate self.make\_serial\_batch\_no\_bundle().
- Otherwise.
  - If not self.sle.is\_cancelled.
    - Evaluate self.validate\_item\_and\_warehouse().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get transit package](operations-060.md#op-f0b23e84b0d405), [make serial batch no bundle](operations-060.md#op-49a89cdbc6e608), [validate item and warehouse](operations-061.md#op-4adecaec74981a).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1081) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L653)

<a id="op-4adecaec74981a"></a>
### Serial Batch Bundle.validate item and warehouse

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_validate_item_and_warehouse`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via exists.

**Explicit failure paths** validation helper — translated “The Serial and Batch Bundle {0} does not belong to Item {1} or Warehouse {2} or {3} no {4}”.format(bold(self.sle.serial\_and\_batch\_bundle), bold(self.item\_code), bold(self.warehouse), translated ….

**Local steps**

- If (self.sle.serial\_and\_batch\_bundle and not Platform.db.exists(“Serial and Batch Bundle”, mapping(“name” → self.sle.serial\_and\_batch\_bundle, “item\_code” → self.item\_code, “warehouse” → self.warehouse, “vouch ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.serial\_and\_batch\_bundle → not Platform.db.exists(“Serial and Batch Bundle”, mapping(“name” → self.sle.serial\_and\_batch\_bundle, “item\_code” → self.item\_code, “warehouse” → self.warehouse, “voucher\_no” → self.sle.voucher\_no)).
  - Call the validation error handler Platform.throw(translated “The Serial and Batch Bundle {0} does not belong to Item {1} or Warehouse {2} or {3} no {4}”.format(bold(self.sle.serial\_and\_batch\_bundle), bold(self.item\_code), bold(self.warehou ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1093) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L665)

<a id="op-43a7acd2290c7b"></a>
### Serial Batch Bundle.delink serial and batch bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_delink_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_cached\_doc.

**State and service calls** request set\_value on self.child\_doctype · request set\_value on “Packed Item” · request set\_value on “Serial and Batch Bundle” · request set\_value on “Serial and Batch Entry”.

**Explicit results** no value.

**Local steps**

- If self.is\_pos\_or\_asset\_repair\_transaction().
  - Return no value.
- Set update\_values from mapping(“serial\_and\_batch\_bundle” → empty text).
- If is\_rejected(self.sle.voucher\_type, self.sle.voucher\_detail\_no, self.sle.warehouse).
  - Set update\_values at “rejected\_serial\_and\_batch\_bundle” from empty text.
- Evaluate Platform.db.set\_value(self.child\_doctype, self.sle.voucher\_detail\_no, update\_values).
- If self.child\_doctype equals “Delivery Note”.
  - Evaluate Platform.db.set\_value(“Packed Item”, mapping(“parent\_detail\_docname” → self.sle.voucher\_detail\_no), update\_values).
- Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, mapping(“voucher\_no” → self.sle.voucher\_no, “voucher\_type” → self.sle.voucher\_type), mapping(“is\_cancelled” → 1)).
- Evaluate Platform.db.set\_value(“Serial and Batch Entry”, mapping(“voucher\_no” → self.sle.voucher\_no, “voucher\_type” → self.sle.voucher\_type), mapping(“is\_cancelled” → 1)).
- If self.sle.serial\_and\_batch\_bundle.
  - Evaluate Platform.get\_cached\_doc(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle).validate\_serial\_and\_batch\_inventory().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is pos or asset repair transaction](operations-061.md#op-d701d5db8734ca).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L4921) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1071) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L643)

<a id="op-e62993cd0eeaff"></a>
### Serial Batch Bundle.post process

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_post_process`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value · read “Serial and Batch Entry” via count.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Serial and Batch Bundle {0} is not submitted”.format(bold(self.sle.serial\_and\_batch\_bundle)).

**Local steps**

- If (not self.sle.serial\_and\_batch\_bundle and not self.sle.serial\_no and not self.sle.batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sle.serial\_and\_batch\_bundle → not self.sle.serial\_no → not self.sle.batch\_no.
  - Return no value.
- If self.sle.serial\_and\_batch\_bundle.
  - Set docstatus from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “docstatus”).
  - If docstatus equals 0.
    - Evaluate self.submit\_serial\_and\_batch\_bundle().
  - If (Platform.db.count(“Serial and Batch Entry”, mapping(“parent” → self.sle.serial\_and\_batch\_bundle, “docstatus” → 0)) &gt; 0 and not self.sle.is\_cancelled).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.count(“Serial and Batch Entry”, mapping(“parent” → self.sle.serial\_and\_batch\_bundle, “docstatus” → 0)) &gt; 0 → not self.sle.is\_cancelled.
    - Call the validation error handler Platform.throw(translated “Serial and Batch Bundle {0} is not submitted”.format(bold(self.sle.serial\_and\_batch\_bundle))).
- If self.item\_details.has\_serial\_no equals 1.
  - Evaluate self.set\_warehouse\_and\_status\_in\_serial\_nos().
- If (self.sle.actual\_qty &gt; 0 and self.item\_details.has\_serial\_no equals 1 and self.item\_details.has\_batch\_no equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.actual\_qty &gt; 0 → self.item\_details.has\_serial\_no equals 1 → self.item\_details.has\_batch\_no equals 1.
  - Evaluate self.set\_batch\_no\_in\_serial\_nos().
- If (self.sle.is\_cancelled and self.sle.serial\_and\_batch\_bundle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.is\_cancelled → self.sle.serial\_and\_batch\_bundle.
  - Evaluate self.cancel\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [submit serial and batch bundle](operations-061.md#op-59a1f44f9bc5f0), [set warehouse and status in serial nos](operations-061.md#op-646847074c0d04), [set batch no in serial nos](operations-061.md#op-c3172b10619ebc), [cancel serial and batch bundle](operations-061.md#op-05d1c2fb8596d8).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “docstatus”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L5514) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1080) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L652)

<a id="op-05d1c2fb8596d8"></a>
### Serial Batch Bundle.cancel serial and batch bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_cancel_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_cached\_doc.

**State and service calls** call cancel on doc.

**Explicit results** no value.

**Local steps**

- If self.is\_pos\_or\_asset\_repair\_transaction().
  - Return no value.
- Set doc from Platform.get\_cached\_doc(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle).
- If doc.docstatus equals 1.
  - Evaluate doc.cancel().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is pos or asset repair transaction](operations-061.md#op-d701d5db8734ca).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L6128) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1069) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L641)

<a id="op-d701d5db8734ca"></a>
### Serial Batch Bundle.is pos or asset repair transaction

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_is_point_of_sale_or_asset_repair_transaction`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value · read “Sales Invoice” via get\_cached\_value.

**Explicit results** true.

**Local steps**

- Set voucher\_type from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “voucher\_type”).
- If (self.sle.voucher\_type equals “Sales Invoice” and self.sle.serial\_and\_batch\_bundle and (voucher\_type equals “POS Invoice” or Platform.get\_cached\_value(“Sales Invoice”, self.sle.voucher\_no, “is\_consolidated”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.voucher\_type equals “Sales Invoice” → self.sle.serial\_and\_batch\_bundle → (voucher\_type equals “POS Invoice” or Platform.get\_cached\_value(“Sales Invoice”, self.sle.voucher\_no, “is\_consolidated”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in voucher\_type equals “POS Invoice” → Platform.get\_cached\_value(“Sales Invoice”, self.sle.voucher\_no, “is\_consolidated”).
  - Return true.
- If (self.sle.voucher\_type equals “Stock Entry” and self.sle.serial\_and\_batch\_bundle and voucher\_type equals “Asset Repair”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.voucher\_type equals “Stock Entry” → self.sle.serial\_and\_batch\_bundle → voucher\_type equals “Asset Repair”.
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “voucher\_type”), Platform.get\_cached\_value(“Sales Invoice”, self.sle.voucher\_no, “is\_consolidated”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1076) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L648)

<a id="op-59a1f44f9bc5f0"></a>
### Serial Batch Bundle.submit serial and batch bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_submit_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call submit on doc.

**Local steps**

- Set doc from Platform.get\_doc(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle).
- If (self.sle.voucher\_detail\_no and doc.voucher\_detail\_no differs from self.sle.voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.voucher\_detail\_no → doc.voucher\_detail\_no differs from self.sle.voucher\_detail\_no.
  - Set doc.voucher\_detail\_no from self.sle.voucher\_detail\_no.
- Evaluate self.validate\_actual\_qty(doc).
- Set doc.flags.ignore\_voucher\_validation from true.
- Evaluate doc.submit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate actual qty](operations-060.md#op-238b03afd46aad).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L6527) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1088) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L660)

<a id="op-646847074c0d04"></a>
### Serial Batch Bundle.set warehouse and status in serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_set_warehouse_and_status_in_serial_numbers`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_parsed\_serial\_nos.
- If (self.sle.auto\_created\_serial\_and\_batch\_bundle and self.sle.actual\_qty &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.auto\_created\_serial\_and\_batch\_bundle → self.sle.actual\_qty &gt; 0.
  - Return no value.
- Set serial\_nos from get\_serial\_nos(self.sle.serial\_and\_batch\_bundle).
- If (not self.sle.serial\_and\_batch\_bundle and self.sle.serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sle.serial\_and\_batch\_bundle → self.sle.serial\_no.
  - Set serial\_nos from get\_parsed\_serial\_nos(self.sle.serial\_no).
- If not serial\_nos.
  - Return no value.
- If (self.sle.voucher\_type equals “Stock Reconciliation” and self.sle.actual\_qty &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.voucher\_type equals “Stock Reconciliation” → self.sle.actual\_qty &gt; 0.
  - Evaluate self.update\_serial\_no\_status\_for\_stock\_reco(serial\_nos).
  - Return no value.
- Evaluate self.update\_serial\_no\_status\_warehouse(self.sle, serial\_nos).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update serial no status for stock reco](operations-061.md#op-81a3a40df9d76c), [update serial no status warehouse](operations-061.md#op-2b4a3df44e94b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L6746) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1087) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L659)

<a id="op-3f2708a354f500"></a>
### Serial Batch Bundle.get status for serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_get_status_for_serial_numbers`

**Inputs** self, sle.

**Explicit results** get\_status\_for\_serial\_nos(sle).

**Local steps**

- Return get\_status\_for\_serial\_nos(sle).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L7099) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1072) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L644)

<a id="op-2b4a3df44e94b4"></a>
### Serial Batch Bundle.update serial no status warehouse

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_update_serial_number_status_warehouse`

**Inputs** self, sle, serial\_nos.

**Record and data access** read sle.voucher\_type via get\_cached\_value · read “Item” via get\_cached\_value.

**Local steps**

- Set warehouse from sle.warehouse when sle.actual\_qty &gt; 0, otherwise no value.
  - Value choice on sle.actual\_qty &gt; 0 — true gives sle.warehouse, false gives no value.
- If isinstance(serial\_nos, str).
  - Set serial\_nos from list(serial\_nos).
- Set status from get\_serial\_no\_status(sle).
- Set customer from no value.
- If (sle.voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”) and sle.actual\_qty &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”) → sle.actual\_qty &lt; 0.
  - Set customer from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “customer”).
- Set sn\_table from Platform.qb.DocType(“Serial No”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).set(sn\_table.company, sle.company).set(sn\_table.customer, customer).where(sn\_table.name.isin(serial\_nos)).
- If status equals “Delivered”.
  - Set warranty\_period from Platform.get\_cached\_value(“Item”, sle.item\_code, “warranty\_period”).
  - If warranty\_period.
    - Set warranty\_expiry\_date from add\_days(getdate(sle.posting\_datetime), cint(warranty\_period)).
    - Set query from query.set(sn\_table.warranty\_expiry\_date, warranty\_expiry\_date).
    - Set query from query.set(sn\_table.warranty\_period, warranty\_period).
- Otherwise.
  - Set query from query.set(sn\_table.warranty\_expiry\_date, no value).
  - Set query from query.set(sn\_table.warranty\_period, 0).
- Evaluate query.run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(sle.voucher\_type, sle.voucher\_no, “customer”), Platform.get\_cached\_value(“Item”, sle.item\_code, “warranty\_period”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1090) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L662)

<a id="op-81a3a40df9d76c"></a>
### Serial Batch Bundle.update serial no status for stock reco

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_update_serial_number_status_for_stock_reco`

**Inputs** self, serial\_nos.

**Local steps**

- For each serial\_no in serial\_nos.
  - Set sle\_doctype from Platform.qb.DocType(“Stock Ledger Entry”).
  - Set sn\_table from Platform.qb.DocType(“Serial and Batch Entry”).
  - Set query from nested operand in the contract(nested operand in the contract).orderby(sle\_doctype.posting\_datetime, order = Order.desc).orderby(sle\_doctype.creation, order = Order.desc).limit(1).
  - Set sle from query.run(as\_dict = 1).
  - If sle.
    - Evaluate self.update\_serial\_no\_status\_warehouse(sle at 0, serial\_no).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update serial no status warehouse](operations-061.md#op-2b4a3df44e94b4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L881) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1089) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L661)

<a id="op-c3172b10619ebc"></a>
### Serial Batch Bundle.set batch no in serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_set_batch_number_in_serial_numbers`

**Inputs** self.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Local steps**

- Set entries from Platform.get\_all(“Serial and Batch Entry”, fields = list(“serial\_no”, “batch\_no”), filters = mapping(“parent” → self.sle.serial\_and\_batch\_bundle)).
- Set batch\_serial\_nos from mapping().
- For each ledger in entries.
  - Evaluate batch\_serial\_nos.setdefault(ledger.batch\_no, list()).append(ledger.serial\_no).
- For each tuple(batch\_no, serial\_nos) in batch\_serial\_nos.items().
  - Set sn\_table from Platform.qb.DocType(“Serial No”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(sn\_table.batch\_no, batch\_no).where(sn\_table.name.isin(serial\_nos)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L1418) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1084) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L656)

<a id="op-f6e6ab96b4c7fb"></a>
### Get serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_serial_numbers`

**Inputs** serial\_and\_batch\_bundle, serial\_nos = no value.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** list() · serial\_nos.

**Local steps**

- If not serial\_and\_batch\_bundle.
  - Return list().
- Set filters from mapping(“parent” → serial\_and\_batch\_bundle, “serial\_no” → tuple(“is”, “set”)).
- If isinstance(serial\_and\_batch\_bundle, list).
  - Set filters from mapping(“parent” → tuple(“in”, serial\_and\_batch\_bundle)).
- If serial\_nos.
  - Set filters at “serial\_no” from tuple(“in”, serial\_nos).
- Set serial\_nos from Platform.get\_all(“Serial and Batch Entry”, filters = filters, order\_by = “idx”, pluck = “serial\_no”).
- Return serial\_nos.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L1801) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1062) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L634)

<a id="op-e06c4e07ff65a0"></a>
### Get batches from bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_batches_from_bundle`

**Inputs** serial\_and\_batch\_bundle, batches = no value.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** list() · Platform.\_dict(mapping()) · Platform.\_dict(entries).

**Local steps**

- If not serial\_and\_batch\_bundle.
  - Return list().
- Set filters from mapping(“parent” → serial\_and\_batch\_bundle, “batch\_no” → tuple(“is”, “set”)).
- If isinstance(serial\_and\_batch\_bundle, list).
  - Set filters from mapping(“parent” → tuple(“in”, serial\_and\_batch\_bundle)).
- If batches.
  - Set filters at “batch\_no” from tuple(“in”, batches).
- Set entries from Platform.get\_all(“Serial and Batch Entry”, fields = list(“batch\_no”, “qty”), filters = filters, order\_by = “idx”, as\_list = 1).
- If not entries.
  - Return Platform.\_dict(mapping()).
- Return Platform.\_dict(entries).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L2109) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1055) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L627)

<a id="op-42e7629f099419"></a>
### Get serial nos from bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_serial_numbers_from_bundle`

**Inputs** serial\_and\_batch\_bundle, serial\_nos = no value.

**Explicit results** get\_serial\_nos(serial\_and\_batch\_bundle, serial\_nos = serial\_nos).

**Local steps**

- Return get\_serial\_nos(serial\_and\_batch\_bundle, serial\_nos = serial\_nos).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L2492) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1064) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L636)

<a id="op-c4a0d1e0390591"></a>
### Get serial or batch nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_serial_or_batch_numbers`

**Inputs** bundle.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value · read “Serial and Batch Entry” via get\_all.

**Explicit results** “, ”.join(list of d.serial\_no for d drawn from data) · html.

**Local steps**

- Set bundle\_data from Platform.get\_cached\_value(“Serial and Batch Bundle”, bundle, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = true).
- Set fields from list().
- If bundle\_data.has\_serial\_no.
  - Evaluate fields.append(“serial\_no”).
- If bundle\_data.has\_batch\_no.
  - Evaluate fields.extend(list(“batch\_no”, “qty”)).
- Set data from Platform.get\_all(“Serial and Batch Entry”, fields = fields, filters = mapping(“parent” → bundle)).
- If (bundle\_data.has\_serial\_no and not bundle\_data.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bundle\_data.has\_serial\_no → not bundle\_data.has\_batch\_no.
  - Return “, ”.join(list of d.serial\_no for d drawn from data).
    - Draw d from data.
- Otherwise.
  - If bundle\_data.has\_batch\_no.
    - Set html from text in the contract.
    - For each d in data.
      - If d.serial\_no.
        - Update html using + formatted text &lt;tr&gt;&lt;td&gt;{d.batch\_no}&lt;/td&gt;&lt;td&gt;{d.serial\_no}&lt;/td&gt;&lt;td&gt;{abs(d.qty)}&lt;/td&gt;&lt;/tr&gt;.
      - Otherwise.
        - Update html using + formatted text &lt;tr&gt;&lt;td&gt;{d.batch\_no}&lt;/td&gt;&lt;td&gt;{abs(d.qty)}&lt;/td&gt;&lt;/tr&gt;.
    - Update html using + “&lt;/table&gt;”.
    - Return html.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, bundle, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L2565) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1066) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L638)

<a id="op-f2cfd3ed8503be"></a>
### Serial No Valuation.initialize

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_initialize`

**Inputs** self, remaining named values kwargs.

**Local steps**

- For each tuple(key, value) in kwargs.items().
  - Evaluate setattr(self, key, value).
- Evaluate self.calculate\_stock\_value\_change().
- Evaluate self.calculate\_valuation\_rate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate stock value change](operations-061.md#op-8a3d5a1698df07), [calculate valuation rate](operations-062.md#op-78e7365005d604).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0927.json#L3169) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L691)

<a id="op-8a3d5a1698df07"></a>
### Serial No Valuation.calculate stock value change

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_calculate_stock_value_change`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value.

**Local steps**

- If flt(self.sle.actual\_qty) &gt; 0.
  - Set self.stock\_value\_change from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “total\_amount”).
- Otherwise.
  - Set self.serial\_no\_incoming\_rate from defaultdict(float).
  - Set self.stock\_value\_change from 0.0.
  - Set self.old\_serial\_nos from list().
  - Set serial\_nos from self.get\_serial\_nos().
  - Set result from self.get\_serial\_no\_wise\_incoming\_rate(serial\_nos).
  - For each serial\_no in serial\_nos.
    - Set incoming\_rate from result.get(serial\_no).
    - If incoming\_rate is identical to no value.
      - Evaluate self.old\_serial\_nos.append(serial\_no).
      - Continue with the next iteration or loop test.
    - Update self.stock\_value\_change using + incoming\_rate.
    - Update self.serial\_no\_incoming\_rate at serial\_no using + incoming\_rate.
  - Evaluate self.calculate\_stock\_value\_from\_deprecarated\_ledgers().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get serial nos](operations-062.md#op-12bea2b3b6259c), [get serial no wise incoming rate](operations-061.md#op-847e9574039ad7).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, self.sle.serial\_and\_batch\_bundle, “total\_amount”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L685)

<a id="op-847e9574039ad7"></a>
### Serial No Valuation.get serial no wise incoming rate

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_number_valuation_get_serial_number_wise_incoming_rate`

**Inputs** self, serial\_nos.

**Explicit results** incoming\_rates.

**Local steps**

- Set incoming\_rates from Platform.\_dict().
- For each serial\_nos\_batch in create\_batch(serial\_nos, SERIAL\_NO\_QUERY\_BATCH\_SIZE).
  - For each tuple(serial\_no, incoming\_rate) in self.get\_inward\_serial\_no\_rates(serial\_nos\_batch).
    - Evaluate incoming\_rates.setdefault(serial\_no, incoming\_rate).
- Return incoming\_rates.

**Methods declared on this owner** [get inward serial no rates](operations-061.md#op-c4cf2f085f7ba9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L689)

<a id="op-c4cf2f085f7ba9"></a>
### Serial No Valuation.get inward serial no rates

`operation_enterprise_binding_enterprise_stock_serial_batch_bundle_serialnovaluation_get_inward_serial_no_rates`

**Inputs** self, serial\_nos.

**Explicit results** query.run().

**Local steps**

- Set bundle\_child from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- If self.sle.voucher\_no.
  - Set query from query.where(bundle\_child.voucher\_no differs from self.sle.voucher\_no).
- If self.sle.posting\_datetime.
  - Set query from query.where(bundle\_child.posting\_datetime ≤ self.sle.posting\_datetime).
- Return query.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1078)
