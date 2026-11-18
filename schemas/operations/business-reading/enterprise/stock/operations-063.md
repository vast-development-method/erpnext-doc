# Inventory and warehouses · operations 63

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Serial batch bundle

<a id="op-c31a07270ab07e"></a>
### Serial Batch Creation.set

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_set`

**Inputs** self, args.

**Local steps**

- Set self.\_\_dict\_\_ from mapping().
- For each tuple(key, value) in args.items().
  - Evaluate setattr(self, key, value).
  - Set self.\_\_dict\_\_ at key from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L5702) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L677)

<a id="op-f8dcfddc85d782"></a>
### Serial Batch Creation.get

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_get`

**Inputs** self, key.

**Explicit results** self.\_\_dict\_\_.get(key).

**Local steps**

- Return self.\_\_dict\_\_.get(key).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L5843) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1097) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L669)

<a id="op-068dccff5aa91d"></a>
### Serial Batch Creation.set item details

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_set_item_details`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set fields from list(“has\_batch\_no”, “has\_serial\_no”, “item\_name”, “item\_group”, …).
- Set item\_details from Platform.get\_cached\_value(“Item”, self.item\_code, fields, as\_dict = 1).
- For each tuple(key, value) in item\_details.items().
  - Evaluate setattr(self, key, value).
- Evaluate self.\_\_dict\_\_.update(item\_details).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, fields, as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L5908) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L680)

<a id="op-52eaa15a42aab1"></a>
### Serial Batch Creation.set other details

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_set_other_details`

**Inputs** self.

**Local steps**

- Bind dependencies get\_combine\_datetime.
- If not self.get(“posting\_datetime”).
  - If (self.get(“posting\_date”) and self.get(“posting\_time”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“posting\_date”) → self.get(“posting\_time”).
    - Set self.posting\_datetime from get\_combine\_datetime(self.posting\_date, self.posting\_time).
- If not self.get(“posting\_datetime”).
  - Set self.posting\_datetime from now().
  - Set self.\_\_dict\_\_ at “posting\_datetime” from self.posting\_datetime.
- If not self.get(“actual\_qty”).
  - Set qty from (self.get(“qty”) or self.get(“total\_qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“qty”) → self.get(“total\_qty”).
  - Set self.actual\_qty from qty.
  - Set self.\_\_dict\_\_ at “actual\_qty” from self.actual\_qty.
- If not hasattr(self, “use\_serial\_batch\_fields”).
  - Set self.use\_serial\_batch\_fields from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L6170) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L681)

<a id="op-feb99ed1b3c968"></a>
### Serial Batch Creation.duplicate package

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_duplicate_package`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** request copy\_doc for package · call save on new\_package.

**Explicit results** no value · new\_package.

**Local steps**

- If not self.serial\_and\_batch\_bundle.
  - Return no value.
- Set id from self.serial\_and\_batch\_bundle.
- Set package from Platform.get\_doc(“Serial and Batch Bundle”, id).
- Set new\_package from Platform.copy\_doc(package, ignore\_no\_copy = false).
- If self.get(“returned\_serial\_nos”).
  - Evaluate self.remove\_returned\_serial\_nos(new\_package).
- Set new\_package.docstatus from 0.
- Set new\_package.warehouse from self.warehouse.
- Set new\_package.voucher\_no from empty text.
- Set new\_package.posting\_datetime from self.posting\_datetime when hasattr(self, “posting\_datetime”), otherwise now().
  - Value choice on hasattr(self, “posting\_datetime”) — true gives self.posting\_datetime, false gives now().
- Set new\_package.type\_of\_transaction from self.type\_of\_transaction.
- Set new\_package.returned\_against from self.get(“returned\_against”).
- If self.get(“do\_not\_save”).
  - Return new\_package.
- Evaluate new\_package.save().
- Set self.serial\_and\_batch\_bundle from new\_package.name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782), [remove returned serial nos](operations-063.md#op-79125d84f507ff).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L6654) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1096) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L668)

<a id="op-79125d84f507ff"></a>
### Serial Batch Creation.remove returned serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_remove_returned_serial_numbers`

**Inputs** self, package.

**Local steps**

- Set remove\_list from list().
- For each d in package.entries.
  - If d.serial\_no belongs to self.returned\_serial\_nos.
    - Evaluate remove\_list.append(d).
- For each d in remove\_list.
  - Evaluate package.remove(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0928.json#L7109) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L676)

<a id="op-e98289407e70cc"></a>
### Serial Batch Creation.make serial and batch bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_make_serial_and_batch_bundle`

**Inputs** self, serial\_nos = no value, batch\_nos = no value.

**Record and data access** read doc.voucher\_type via get\_cached\_value.

**State and service calls** request new\_doc for “Serial and Batch Bundle” · call save on doc · call db\_set on self.sle · call submit on doc.

**Explicit results** Platform.\_dict(mapping()) · doc.

**Local steps**

- Set serial\_nos from (serial\_nos or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_nos → list().
- Set batch\_nos from (batch\_nos or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in batch\_nos → list().
- Set doc from Platform.new\_doc(“Serial and Batch Bundle”).
- Set valid\_columns from doc.meta.get\_valid\_columns().
- For each tuple(key, value) in self.\_\_dict\_\_.items().
  - If key belongs to valid\_columns.
    - Evaluate doc.set(key, value).
- If serial\_nos.
  - Set self.serial\_nos from serial\_nos.
- If batch\_nos.
  - Set self.batches from batch\_nos.
- If self.type\_of\_transaction equals “Outward”.
  - Evaluate self.set\_auto\_serial\_batch\_entries\_for\_outward().
- Otherwise.
  - If self.type\_of\_transaction equals “Inward”.
    - Evaluate self.set\_auto\_serial\_batch\_entries\_for\_inward().
    - Evaluate self.add\_serial\_nos\_for\_batch\_item().
- If (hasattr(self, “via\_landed\_cost\_voucher”) and self.via\_landed\_cost\_voucher).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “via\_landed\_cost\_voucher”) → self.via\_landed\_cost\_voucher.
  - Set doc.flags.via\_landed\_cost\_voucher from self.via\_landed\_cost\_voucher.
- Evaluate self.set\_serial\_batch\_entries(doc).
- If not doc.get(“entries”).
  - Return Platform.\_dict(mapping()).
- If (doc.voucher\_no and Platform.get\_cached\_value(doc.voucher\_type, doc.voucher\_no, “docstatus”) equals 2).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.voucher\_no → Platform.get\_cached\_value(doc.voucher\_type, doc.voucher\_no, “docstatus”) equals 2.
  - Set doc.voucher\_no from empty text.
- Set doc.flags.ignore\_validate\_serial\_batch from false.
- If (self.get(“make\_bundle\_from\_sle”) and self.type\_of\_transaction equals “Inward”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“make\_bundle\_from\_sle”) → self.type\_of\_transaction equals “Inward”.
  - Set doc.flags.ignore\_validate\_serial\_batch from true.
- If (not hasattr(self, “do\_not\_submit”) or not self.do\_not\_submit).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(self, “do\_not\_submit”) → not self.do\_not\_submit.
  - Set doc.flags.ignore\_voucher\_validation from true.
  - If self.get(“sle”).
    - Set doc.flags.ignore\_validate from true.
    - Evaluate doc.save().
    - Evaluate self.sle.db\_set(“serial\_and\_batch\_bundle”, doc.name, update\_modified = false).
  - If doc.flags.ignore\_validate.
    - Set doc.flags.ignore\_validate from false.
  - Evaluate doc.submit().
- Otherwise.
  - If self.get(“ignore\_sabb\_validation”).
    - Set doc.flags.ignore\_validate from true.
  - Evaluate doc.save().
- Evaluate self.validate\_qty(doc).
- Return doc.

**Methods declared on this owner** [set auto serial batch entries for outward](operations-063.md#op-eb814543033593), [set auto serial batch entries for inward](operations-063.md#op-9775e21acd58ed), [add serial nos for batch item](operations-063.md#op-df62e62a2a9e49), [set serial batch entries](operations-063.md#op-bd47007508f49c), [get](operations-063.md#op-f8dcfddc85d782), [validate qty](operations-063.md#op-0cae23eae32899).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(doc.voucher\_type, doc.voucher\_no, “docstatus”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L673)

<a id="op-df62e62a2a9e49"></a>
### Serial Batch Creation.add serial nos for batch item

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_add_serial_numbers_for_batch_item`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.has\_serial\_no and self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → self.has\_batch\_no.
  - Return no value.
- If (not self.get(“serial\_nos”) and self.get(“batches”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“serial\_nos”) → self.get(“batches”).
  - Set batches from list(self.get(“batches”).keys()).
  - If len(batches) equals 1.
    - Set self.batch\_no from batches at 0.
    - Set self.serial\_nos from self.get\_auto\_created\_serial\_nos().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782), [get auto created serial nos](operations-063.md#op-e7aeffb5a8a69d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L1101) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1094) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L666)

<a id="op-626db5823f2595"></a>
### Serial Batch Creation.update serial and batch entries

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_update_serial_and_batch_entries`

**Inputs** self, serial\_nos = no value, batch\_nos = no value.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** Platform.\_dict(mapping()) · doc.

**Local steps**

- Set serial\_nos from (serial\_nos or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_nos → list().
- Set batch\_nos from (batch\_nos or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in batch\_nos → list().
- Set doc from Platform.get\_doc(“Serial and Batch Bundle”, self.serial\_and\_batch\_bundle).
- Set doc.type\_of\_transaction from self.type\_of\_transaction.
- Evaluate doc.set(“entries”, list()).
- If serial\_nos.
  - Set self.serial\_nos from serial\_nos.
- If batch\_nos.
  - Set self.batch\_nos from batch\_nos.
- Evaluate self.set\_auto\_serial\_batch\_entries\_for\_outward().
- Evaluate self.set\_serial\_batch\_entries(doc).
- If not doc.get(“entries”).
  - Return Platform.\_dict(mapping()).
- Evaluate doc.save().
- Return doc.

**Methods declared on this owner** [set auto serial batch entries for outward](operations-063.md#op-eb814543033593), [set serial batch entries](operations-063.md#op-bd47007508f49c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L1371) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L683)

<a id="op-0cae23eae32899"></a>
### Serial Batch Creation.validate qty

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_validate_quantity`

**Inputs** self, doc.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (doc.type\_of\_transaction equals “Outward” and self.actual\_qty and doc.total\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.type\_of\_transaction equals “Outward” → self.actual\_qty → doc.total\_qty.
  - Set precision from doc.precision(“total\_qty”).
  - Set total\_qty from flt(abs(doc.total\_qty), precision).
  - Set required\_qty from flt(abs(self.actual\_qty), precision).
  - If (required\_qty − total\_qty) &gt; 0.
    - Set msg from formatted text For the item {bold(doc.item\_code)}, the Available qty {bold(total\_qty)} is less than the Required Qty {bold(required\_qty)} in the warehouse {bold(doc..
    - Call the validation error handler Platform.throw(msg, title = translated “Insufficient Stock”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L684)

<a id="op-eb814543033593"></a>
### Serial Batch Creation.set auto serial batch entries for outward

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_set_auto_serial_batch_entries_for_outward`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- Bind dependencies get\_available\_batches.
- Bind dependencies get\_serial\_nos\_for\_outward.
- Set kwargs from Platform.\_dict(mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse, “company” → self.get(“company”), “qty” → abs(self.actual\_qty) when self.actual\_qty, otherwise 0, …)).
  - Value choice on self.actual\_qty — true gives abs(self.actual\_qty), false gives 0.
- If self.get(“ignore\_serial\_nos”).
  - Set kwargs at “ignore\_serial\_nos” from self.ignore\_serial\_nos.
- If self.get(“already\_picked\_batches”).
  - Set kwargs at “already\_picked\_batches” from self.already\_picked\_batches.
  - If self.get(“voucher\_type”) equals “POS Invoice”.
    - Set kwargs at “ignore\_voucher\_nos” from list(self.voucher\_no).
- Evaluate kwargs.update(self.get\_reservation\_kwargs()).
- If (self.has\_serial\_no and self.has\_batch\_no and not self.get(“serial\_nos”) and self.get(“batches”) and len(self.get(“batches”)) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → self.has\_batch\_no → not self.get(“serial\_nos”) → self.get(“batches”) → len(self.get(“batches”)) equals 1.
  - Set kwargs at “batches” from next(iter(self.get(“batches”).keys())).
  - Set self.serial\_nos from get\_serial\_nos\_for\_outward(kwargs).
- Otherwise.
  - If (self.has\_serial\_no and not self.get(“serial\_nos”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → not self.get(“serial\_nos”).
    - Set self.serial\_nos from get\_serial\_nos\_for\_outward(kwargs).
  - Otherwise.
    - If (not self.has\_serial\_no and self.has\_batch\_no and not self.get(“batches”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_serial\_no → self.has\_batch\_no → not self.get(“batches”).
      - If self.get(“posting\_datetime”).
        - Set kwargs at “posting\_datetime” from self.get(“posting\_datetime”).
      - Set self.batches from get\_available\_batches(kwargs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782), [get reservation kwargs](operations-063.md#op-7e1450dd7df9d2).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L679)

<a id="op-7e1450dd7df9d2"></a>
### Serial Batch Creation.get reservation kwargs

`operation_enterprise_binding_enterprise_stock_serial_batch_bundle_serialbatchcreation_get_reservation_kwargs`

**Inputs** self.

**Explicit results** mapping() · mapping(“pick\_reserved\_items” → true, “sabb\_voucher\_type” → self.voucher\_type, “sabb\_voucher\_no” → self.get(“voucher\_no”), “sabb\_voucher\_detail\_no” → self.get(“voucher\_detail\_no”)).

**Local steps**

- If self.get(“voucher\_type”) does not belong to tuple(“Delivery Note”, “Sales Invoice”, “POS Invoice”).
  - Return mapping().
- Return mapping(“pick\_reserved\_items” → true, “sabb\_voucher\_type” → self.voucher\_type, “sabb\_voucher\_no” → self.get(“voucher\_no”), “sabb\_voucher\_detail\_no” → self.get(“voucher\_detail\_no”)).

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1077)

<a id="op-9775e21acd58ed"></a>
### Serial Batch Creation.set auto serial batch entries for inward

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_set_auto_serial_batch_entries_for_inward`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If ((self.get(“batches”) and self.has\_batch\_no) or (self.get(“serial\_nos”) and self.has\_serial\_no)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.get(“batches”) and self.has\_batch\_no) → (self.get(“serial\_nos”) and self.has\_serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“batches”) → self.has\_batch\_no.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“serial\_nos”) → self.has\_serial\_no.
  - If (self.use\_serial\_batch\_fields and self.get(“serial\_nos”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.use\_serial\_batch\_fields → self.get(“serial\_nos”).
    - Evaluate self.make\_serial\_no\_if\_not\_exists().
  - Return no value.
- Set self.batch\_no from no value.
- If self.has\_batch\_no.
  - Set self.batch\_no from self.create\_batch().
- If self.has\_serial\_no.
  - Set self.serial\_nos from self.get\_auto\_created\_serial\_nos().
- Otherwise.
  - Set self.batches from Platform.\_dict(mapping(self.batch\_no → abs(self.actual\_qty))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782), [make serial no if not exists](operations-063.md#op-536080540cf822), [create batch](operations-063.md#op-906f0628ef7171), [get auto created serial nos](operations-063.md#op-e7aeffb5a8a69d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L2877) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L678)

<a id="op-536080540cf822"></a>
### Serial Batch Creation.make serial no if not exists

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_make_serial_number_if_not_exists`

**Inputs** self.

**Record and data access** read “Serial No” via exists.

**Local steps**

- Set non\_exists\_serial\_nos from list().
- For each row in self.serial\_nos.
  - If not Platform.db.exists(“Serial No”, row).
    - Evaluate non\_exists\_serial\_nos.append(row).
- If non\_exists\_serial\_nos.
  - Evaluate self.make\_serial\_nos(non\_exists\_serial\_nos).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make serial nos](operations-063.md#op-88f5ed968b3647).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L3229) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L674)

<a id="op-88f5ed968b3647"></a>
### Serial Batch Creation.make serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_make_serial_numbers`

**Inputs** self, serial\_nos.

**State and service calls** request bulk\_insert on “Serial No”.

**Local steps**

- Set serial\_nos\_details from list().
- Set batch\_no from no value.
- If self.batches.
  - Set batch\_no from next(iter(self.batches.keys())).
- For each serial\_no in serial\_nos.
  - Evaluate serial\_nos\_details.append(tuple(serial\_no, serial\_no, now(), now(), …)).
- If serial\_nos\_details.
  - Set fields from list(“name”, “serial\_no”, “creation”, “modified”, …).
  - Evaluate Platform.db.bulk\_insert(“Serial No”, fields = fields, values = set(serial\_nos\_details)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L3394) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L675)

<a id="op-bd47007508f49c"></a>
### Serial Batch Creation.set serial batch entries

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_set_serial_batch_entries`

**Inputs** self, doc.

**Local steps**

- Set incoming\_rate from self.get(“incoming\_rate”).
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- If self.get(“serial\_nos”).
  - Set serial\_no\_wise\_batch from Platform.\_dict(mapping()).
  - If self.has\_batch\_no.
    - Set serial\_no\_wise\_batch from get\_serial\_nos\_batch(self.serial\_nos).
  - Set qty from negative 1 when self.type\_of\_transaction equals “Outward”, otherwise 1.
    - Value choice on self.type\_of\_transaction equals “Outward” — true gives negative 1, false gives 1.
  - For each serial\_no in self.serial\_nos.
    - If self.get(“serial\_nos\_valuation”).
      - Set incoming\_rate from self.get(“serial\_nos\_valuation”).get(serial\_no).
    - Evaluate doc.append(“entries”, mapping(“serial\_no” → serial\_no, “qty” → qty, “batch\_no” → (serial\_no\_wise\_batch.get(serial\_no) or self.get(“batch\_no”)), “incoming\_rate” → incoming\_rate)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_no\_wise\_batch.get(serial\_no) → self.get(“batch\_no”).
- Otherwise.
  - If self.get(“batches”).
    - For each tuple(batch\_no, batch\_qty) in self.batches.items().
      - If self.get(“batches\_valuation”).
        - Set incoming\_rate from self.get(“batches\_valuation”).get(batch\_no).
      - Evaluate doc.append(“entries”, mapping(“batch\_no” → batch\_no, “qty” → (flt(batch\_qty, precision) × negative 1 when self.type\_of\_transaction equals “Outward”, otherwise 1), “incoming\_rate” → incoming\_rate)).
        - Value choice on self.type\_of\_transaction equals “Outward” — true gives negative 1, false gives 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L682)

<a id="op-906f0628ef7171"></a>
### Serial Batch Creation.create batch

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_create_batch`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_value · read “Serial and Batch Entry” via get\_value.

**Explicit results** batch\_no · make\_batch(Platform.\_dict(mapping(“item” → self.get(“item\_code”), “reference\_doctype” → self.get(“voucher\_type”), “reference\_name” → self.get(“voucher\_no”), “manufacturing\_date” → self.get\_posting\_date\_for ….

**Local steps**

- Bind dependencies make\_batch.
- If (hasattr(self, “is\_rejected”) and self.is\_rejected).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “is\_rejected”) → self.is\_rejected.
  - Set bundle from Platform.db.get\_value(“Serial and Batch Bundle”, mapping(“voucher\_no” → self.voucher\_no, “voucher\_type” → self.voucher\_type, “voucher\_detail\_no” → self.voucher\_detail\_no, “is\_rejected” → 0, …), “name”).
  - If bundle.
    - If batch\_no bound to Platform.db.get\_value(“Serial and Batch Entry”, mapping(“parent” → bundle), “batch\_no”).
      - Return batch\_no.
- Return make\_batch(Platform.\_dict(mapping(“item” → self.get(“item\_code”), “reference\_doctype” → self.get(“voucher\_type”), “reference\_name” → self.get(“voucher\_no”), “manufacturing\_date” → self.get\_posting\_date\_for ….

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782), [get posting date for new batch](operations-063.md#op-348a1513a6c2d4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1095) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L667)

<a id="op-348a1513a6c2d4"></a>
### Serial Batch Creation.get posting date for new batch

`operation_enterprise_binding_enterprise_stock_serial_batch_bundle_serialbatchcreation_get_posting_date_for_new_batch`

**Inputs** self.

**Explicit results** getdate(self.posting\_date) · getdate(self.posting\_datetime).

**Local steps**

- If self.get(“posting\_date”).
  - Return getdate(self.posting\_date).
- If self.get(“posting\_datetime”).
  - Return getdate(self.posting\_datetime).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1076)

<a id="op-e7aeffb5a8a69d"></a>
### Serial Batch Creation.get auto created serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_get_auto_created_serial_numbers`

**Inputs** self.

**Record and data access** read voucher\_type via get\_value.

**State and service calls** request bulk\_insert on “Serial No”.

**Explicit results** sr\_nos.

**Explicit failure paths** validation helper — translated “Please set Serial No Series in the item {0} or create Serial and Batch Bundle manually.”.format(self.item\_code) · validation helper — translated “A naming series conflict occurred while creating serial numbers. Please change the naming series for the item {0}.”.format(bold(self.item\_code)) · e.

**Local steps**

- Set sr\_nos from list().
- Set serial\_nos\_details from list().
- If not self.serial\_no\_series.
  - Call the validation error handler Platform.throw(translated “Please set Serial No Series in the item {0} or create Serial and Batch Bundle manually.”.format(self.item\_code)).
- Set voucher\_no from empty text.
- If self.get(“voucher\_no”).
  - Set voucher\_no from self.get(“voucher\_no”).
- Set voucher\_type from empty text.
- If self.get(“voucher\_type”).
  - Set voucher\_type from self.get(“voucher\_type”).
- Set serial\_no\_values from Platform.\_dict(warehouse = self.warehouse, company = self.company, item\_code = self.item\_code, item\_name = self.item\_name, …).
- Set obj from NamingSeries(self.serial\_no\_series).
- Set current\_value from obj.get\_current\_value(serial\_no\_values).
- Bind local operation get\_series for subsequent calls.
- For each \_i in range(abs(cint(self.actual\_qty))).
  - Update current\_value using + 1.
  - Set serial\_no from parse\_naming\_series(self.serial\_no\_series, doc = serial\_no\_values, number\_generator = get\_series).
  - Evaluate sr\_nos.append(serial\_no).
  - Evaluate serial\_nos\_details.append(tuple(serial\_no, serial\_no, now(), now(), …)).
- If serial\_nos\_details.
  - Set fields from list(“name”, “serial\_no”, “creation”, “modified”, …).
  - Attempt the following.
    - Evaluate Platform.db.bulk\_insert(“Serial No”, fields = fields, values = set(serial\_nos\_details)).
  - On failure (Exception) bound to e.
    - If (e and len(e.args) &gt; 1 and “Duplicate” belongs to e.args at 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in e → len(e.args) &gt; 1 → “Duplicate” belongs to e.args at 1.
      - Call the validation error handler Platform.throw(translated “A naming series conflict occurred while creating serial numbers. Please change the naming series for the item {0}.”.format(bold(self.item\_code)), title = translated “Duplicate Se ….
    - Otherwise.
      - Raise e.
- Evaluate obj.update\_counter(current\_value, serial\_no\_values).
- Return sr\_nos.

**Methods declared on this owner** [get](operations-063.md#op-f8dcfddc85d782).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1098) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L670)

<a id="op-57ca4fa258bc5b"></a>
### Serial Batch Creation.get auto created serial nos.get series

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_creation_get_auto_created_serial_numbers_get_series`

**Inputs** partial\_series, digits.

**Explicit results** formatted text {current\_value}.

**Local steps**

- Return formatted text {current\_value}.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L6835) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1099) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L671)

<a id="op-556e233f419c02"></a>
### Get serial or batch items

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_serial_or_batch_items`

**Inputs** items.

**Record and data access** read “Item” via get\_all.

**Explicit results** no value · serial\_or\_batch\_items.

**Local steps**

- Set serial\_or\_batch\_items from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, list of d.item\_code for d drawn from items)), or\_filters = mapping(“has\_serial\_no” → 1, “has\_batch\_no” → 1)).
  - Draw d from items.
- If not serial\_or\_batch\_items.
  - Return no value.
- Otherwise.
  - Set serial\_or\_batch\_items from list of d.name for d drawn from serial\_or\_batch\_items.
    - Draw d from serial\_or\_batch\_items.
- Return serial\_or\_batch\_items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L6912) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1065) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L637)

<a id="op-ff2757d1d6f23e"></a>
### Get serial nos batch

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_serial_numbers_batch`

**Inputs** serial\_nos.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Serial No”, fields = list(“name”, “batch\_no”), filters = mapping(“name” → tuple(“in”, serial\_nos)), as\_list = 1)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(“Serial No”, fields = list(“name”, “batch\_no”), filters = mapping(“name” → tuple(“in”, serial\_nos)), as\_list = 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0929.json#L7144) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1063) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L635)

<a id="op-70f00ab4cdf47a"></a>
### Update batch qty

`operation_enterprise_stock_serial_batch_bundle_business_behavior_update_batch_quantity`

**Inputs** voucher\_type, voucher\_no, docstatus, via\_landed\_cost\_voucher = false.

**State and service calls** request set\_value on “Batch”.

**Explicit results** no value.

**Local steps**

- Set batches from get\_batchwise\_qty(voucher\_type, voucher\_no).
- If not batches.
  - Return no value.
- Set precision from Platform.get\_precision(“Batch”, “batch\_qty”).
- For each tuple(batch, qty) in batches.items().
  - Set current\_qty from get\_batch\_current\_qty(batch).
  - Update current\_qty using + (flt(qty, precision) × negative 1 when docstatus equals 2, otherwise 1).
    - Value choice on docstatus equals 2 — true gives negative 1, false gives 1.
  - If (not via\_landed\_cost\_voucher and current\_qty &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not via\_landed\_cost\_voucher → current\_qty &lt; 0.
    - Evaluate throw\_negative\_batch\_validation(batch, current\_qty).
  - Evaluate Platform.db.set\_value(“Batch”, batch, “batch\_qty”, current\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L695)

<a id="op-0f51ff188e1cd3"></a>
### Get batch current qty

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_batch_current_quantity`

**Inputs** batch.

**Explicit results** flt(batch\_qty at 0 at 0) when batch\_qty, otherwise 0.0.

**Local steps**

- Set doctype from Platform.qb.DocType(“Batch”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.batch\_qty).where(doctype.name equals batch).for\_update().
- Set batch\_qty from query.run().
- Return flt(batch\_qty at 0 at 0) when batch\_qty, otherwise 0.0.
  - Value choice on batch\_qty — true gives flt(batch\_qty at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0930.json#L406) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1053) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L625)
