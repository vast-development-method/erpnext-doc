# Inventory and warehouses · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pick list

[Record definition](../../../../data/record-types/pick_list.json)

<a id="op-35c2ba3ae2a68f"></a>
### Pick List.validate sales order

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_sales_order`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-35c2ba3ae2a68f-guard-4"></a>If self.purpose differs from “Delivery”.
  - Return no value.
- For each so in set of location.sales\_order for location drawn from self.locations where location.sales\_order.
  - Draw location from self.locations, keep a combination only if (location.sales\_order).
  - Evaluate validate\_no\_reserved\_stock(so).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.purpose differs from “Delivery”, self.purpose = “Material Transfer for Manufacture” selects the branch that returns no value. With self.purpose = “Delivery”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-35c2ba3ae2a68f-guard-4)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L118)

<a id="op-bd63f64c96ecac"></a>
### Pick List.validate picked items

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_picked_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0} picked quantity is less than the required quantity, additional {1} {2} required.”.format(item.idx, (item.stock\_qty − item.picked\_qty), item.stock\_uom).

**Local steps**

- For each item in self.locations.
  - If (self.scan\_mode and item.picked\_qty &lt; item.stock\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.scan\_mode → item.picked\_qty &lt; item.stock\_qty.
    - Call the validation error handler Platform.throw(translated “Row {0} picked quantity is less than the required quantity, additional {1} {2} required.”.format(item.idx, (item.stock\_qty − item.picked\_qty), item.stock\_uom), title = translated ….
  - If (not self.scan\_mode and not item.picked\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.scan\_mode → not item.picked\_qty.
    - Set item.picked\_qty from item.stock\_qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L116)

<a id="op-c2b12b6d4a6ece"></a>
### Pick List.validate picked serial and batch

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_validate_picked_serial_and_batch`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: the selected serial / batch qty is {1} but the picked qty is {2}. Select only what was picked.”.format(row.idx, selected\_qty, row.picked\_qty).

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set bundle\_qty from self.get\_bundle\_qty().
- For each row in self.locations.
  - Set selected\_qty from (bundle\_qty.get(row.serial\_and\_batch\_bundle) or len(get\_serial\_nos(row.serial\_no))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundle\_qty.get(row.serial\_and\_batch\_bundle) → len(get\_serial\_nos(row.serial\_no)).
  - Set precision from row.precision(“picked\_qty”).
  - If (selected\_qty and flt(selected\_qty, precision) differs from flt(row.picked\_qty, precision)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in selected\_qty → flt(selected\_qty, precision) differs from flt(row.picked\_qty, precision).
    - Call the validation error handler Platform.throw(translated “Row #{0}: the selected serial / batch qty is {1} but the picked qty is {2}. Select only what was picked.”.format(row.idx, selected\_qty, row.picked\_qty), title = translated “Selec ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bundle qty](operations-038.md#op-3691c92ca55406).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L204) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L449)

<a id="op-3691c92ca55406"></a>
### Pick List.get bundle qty

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_get_bundle_qty`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_all.

**Explicit results** mapping() · mapping of bundle.name → abs(bundle.total\_qty) for bundle drawn from Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“name” → tuple(“in”, bundles)), fields = list(“name”, “total\_qty”)).

**Local steps**

- Set bundles from list of row.serial\_and\_batch\_bundle for row drawn from self.locations where row.serial\_and\_batch\_bundle.
  - Draw row from self.locations, keep a combination only if (row.serial\_and\_batch\_bundle).
- If not bundles.
  - Return mapping().
- Return mapping of bundle.name → abs(bundle.total\_qty) for bundle drawn from Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“name” → tuple(“in”, bundles)), fields = list(“name”, “total\_qty”)).
  - Draw bundle from Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“name” → tuple(“in”, bundles)), fields = list(“name”, “total\_qty”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L443)

<a id="op-af4923b1658f94"></a>
### Pick List.on submit

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_serial\_and\_batch\_bundle().
- Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields().
- Evaluate self.update\_status().
- Evaluate self.update\_reference\_qty().
- Evaluate self.update\_bundle\_picked\_qty().
- Evaluate self.update\_sales\_order\_picking\_status().
- Evaluate self.update\_picked\_qty\_in\_work\_order().
- Evaluate self.update\_prevdoc\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate serial and batch bundle](operations-038.md#op-e3d9e46f5afbe5), [make bundle using old serial batch fields](operations-038.md#op-6884ff9626b831), [update status](operations-038.md#op-644d0ad34fadce), [update reference qty](operations-038.md#op-f5b888b2879347), [update bundle picked qty](operations-039.md#op-15d2b99efab325), [update sales order picking status](operations-039.md#op-3c055ff2b15a01), [update picked qty in work order](operations-039.md#op-4e1ec741cb6386).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L94)

<a id="op-af104d224e13ed"></a>
### Pick List.validate expired batches

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_expired_batches`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The following batches are expired, please restock them: &lt;br&gt; {0}”.format(msg).

**Local steps**

- Set batches from list().
- For each row in self.get(“locations”).
  - If (row.get(“batch\_no”) and (row.get(“picked\_qty”) or self.pick\_manually)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“batch\_no”) → (row.get(“picked\_qty”) or self.pick\_manually).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“picked\_qty”) → self.pick\_manually.
    - Evaluate batches.append(row.batch\_no).
- If batches.
  - Set batch from Platform.qb.DocType(“Batch”).
  - Set query from nested operand in the contract.qb.from\_(batch).select(batch.name).where(((batch.name.isin(batches) bitwise and batch.expiry\_date &lt; nested operand in the contract.utils.nowdate()) bitwise and batch.expiry\_d ….
  - Set expired\_batches from query.run(as\_dict = true).
  - If expired\_batches.
    - Set msg from ((text in the contract + empty text.join(generator of formatted text &lt;li&gt;{batch.name}&lt;/li&gt; for batch drawn from expired\_batches)) + “&lt;/ul&gt;”).
      - Draw batch from expired\_batches.
    - Call the validation error handler Platform.throw(translated “The following batches are expired, please restock them: &lt;br&gt; {0}”.format(msg), title = translated “Expired Batches”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L113)

<a id="op-6884ff9626b831"></a>
### Pick List.make bundle using old serial batch fields

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_make_bundle_using_old_serial_batch_fields`

**Inputs** self.

**State and service calls** call db\_set on row.

**Explicit failure paths** validation helper — translated “Please enable Use Old Serial / Batch Fields to make\_bundle”.

**Local steps**

- Bind dependencies get\_serial\_nos.
- For each row in self.locations.
  - If (not row.serial\_no and not row.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.serial\_no → not row.batch\_no.
    - Continue with the next iteration or loop test.
  - If (not row.use\_serial\_batch\_fields and (row.serial\_no or row.batch\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.use\_serial\_batch\_fields → (row.serial\_no or row.batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
    - Call the validation error handler Platform.throw(translated “Please enable Use Old Serial / Batch Fields to make\_bundle”).
  - If (row.use\_serial\_batch\_fields and not row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.use\_serial\_batch\_fields → not row.serial\_and\_batch\_bundle.
    - Set sn\_doc from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “voucher\_type” → self.doctype, “voucher\_no” → self.name, …)).make\_serial\_and\_batch\_bundle().
      - Value choice on row.serial\_no — true gives get\_serial\_nos(row.serial\_no), false gives no value.
      - Value choice on row.batch\_no — true gives Platform.\_dict(mapping(row.batch\_no → row.picked\_qty)), false gives no value.
    - Set row.serial\_and\_batch\_bundle from sn\_doc.name.
    - Evaluate row.db\_set(“serial\_and\_batch\_bundle”, sn\_doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L92)

<a id="op-b5d664479da519"></a>
### Pick List.on update after submit

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_on_update_after_submit`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If self.has\_reserved\_stock().
  - Set msg from translated “The Pick List having Stock Reservation Entries cannot be updated. If you need to make changes, we recommend  …”.
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has reserved stock](operations-039.md#op-3729827498d09e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0762.json#L6380) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L97)

<a id="op-6308e230d6c0bf"></a>
### Pick List.on cancel

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from list(“Serial and Batch Bundle”, “Stock Reservation Entry”, “Delivery Note”).
- Evaluate self.cancel\_open\_stock\_reservation\_entries().
- Evaluate self.update\_status().
- Evaluate self.update\_reference\_qty().
- Evaluate self.update\_bundle\_picked\_qty().
- Evaluate self.update\_sales\_order\_picking\_status().
- Evaluate self.update\_picked\_qty\_in\_work\_order().
- Evaluate self.delink\_serial\_and\_batch\_bundle().
- Evaluate self.update\_prevdoc\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel open stock reservation entries](operations-038.md#op-1a15a83619484a), [update status](operations-038.md#op-644d0ad34fadce), [update reference qty](operations-038.md#op-f5b888b2879347), [update bundle picked qty](operations-039.md#op-15d2b99efab325), [update sales order picking status](operations-039.md#op-3c055ff2b15a01), [update picked qty in work order](operations-039.md#op-4e1ec741cb6386), [delink serial and batch bundle](operations-038.md#op-59dbf5c02059fc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L93)

<a id="op-1a15a83619484a"></a>
### Pick List.cancel open stock reservation entries

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_picklist_cancel_open_stock_reservation_entries`

**Inputs** self.

**Local steps**

- Bind dependencies cancel\_stock\_reservation\_entries.
- Evaluate cancel\_stock\_reservation\_entries(from\_voucher\_type = “Pick List”, from\_voucher\_no = self.name, notify = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L944) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L441)

<a id="op-59dbf5c02059fc"></a>
### Pick List.delink serial and batch bundle

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_delink_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_value · resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** request set\_value on “Serial and Batch Bundle” · call cancel on Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle) · call db\_set on row.

**Local steps**

- For each row in self.locations.
  - If (row.serial\_and\_batch\_bundle and Platform.db.get\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “docstatus”) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_and\_batch\_bundle → Platform.db.get\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, “docstatus”) equals 1.
    - Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, mapping(“is\_cancelled” → 1, “voucher\_no” → empty text)).
    - Evaluate Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle).cancel().
    - Evaluate row.db\_set(“serial\_and\_batch\_bundle”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L79)

<a id="op-0d8af2c2161c43"></a>
### Pick List.on update

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_on_update`

**Inputs** self.

**Local steps**

- If self.get(“locations”).
  - Evaluate self.linked\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [linked serial and batch bundle](operations-038.md#op-2dfb8cbbc68664).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L289) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L96)

<a id="op-2dfb8cbbc68664"></a>
### Pick List.linked serial and batch bundle

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_linked_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**Local steps**

- For each row in self.get(“locations”).
  - If row.serial\_and\_batch\_bundle.
    - Evaluate Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle).set\_serial\_and\_batch\_values(self, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L372) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L91)

<a id="op-9d680740fa36ef"></a>
### Pick List.on trash

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.remove\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove serial and batch bundle](operations-038.md#op-e73b8ff5186b22).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L509) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L95)

<a id="op-e73b8ff5186b22"></a>
### Pick List.remove serial and batch bundle

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_remove_serial_and_batch_bundle`

**Inputs** self.

**State and service calls** request delete\_doc for “Serial and Batch Bundle”.

**Local steps**

- For each row in self.locations.
  - If row.serial\_and\_batch\_bundle.
    - Evaluate Platform.delete\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L560) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L99)

<a id="op-e3d9e46f5afbe5"></a>
### Pick List.validate serial and batch bundle

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_validate_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call submit on doc.

**Local steps**

- For each row in self.locations.
  - If row.serial\_and\_batch\_bundle.
    - Set doc from Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle).
    - If doc.docstatus equals 0.
      - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L662) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L120)

<a id="op-644d0ad34fadce"></a>
### Pick List.update status

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_status`

**Inputs** self, status = no value, update\_modified = true.

**State and service calls** call db\_set on self.

**Local steps**

- If not status.
  - Set status from self.get\_status().get(“status”).
- If status.
  - Evaluate self.db\_set(“status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L812) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L111)

<a id="op-4a2dadd31c7859"></a>
### Pick List.stock entry exists

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_stock_entry_exists`

**Inputs** self.

**Explicit results** false · stock\_entry\_exists(self.name).

**Local steps**

- <a id="op-4a2dadd31c7859-guard-2"></a>If self.docstatus differs from 1.
  - Return false.
- <a id="op-4a2dadd31c7859-guard-5"></a>If self.purpose equals “Delivery”.
  - Return false.
- Return stock\_entry\_exists(self.name).

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that returns false. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4a2dadd31c7859-guard-2)
- At the comparison self.purpose equals “Delivery”, self.purpose = “Delivery” selects the branch that returns false. With self.purpose = “Material Transfer for Manufacture”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4a2dadd31c7859-guard-5)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L965) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L102)

<a id="op-37d584310a0a93"></a>
### Pick List.get transfer status

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_get_transfer_status`

**Inputs** self.

**Explicit results** no value · “Completed” · “Partially Transferred”.

**Local steps**

- <a id="op-37d584310a0a93-guard-7"></a>If self.purpose equals “Delivery”.
  - Return no value.
- Set total\_picked from sum(generator of flt(row.picked\_qty) for row drawn from self.locations).
  - Draw row from self.locations.
- If not total\_picked.
  - Return no value.
- Set total\_transferred from sum(generator of flt(row.transferred\_qty) for row drawn from self.locations).
  - Draw row from self.locations.
- <a id="op-37d584310a0a93-guard-15"></a>If total\_transferred ≤ 0.
  - Return no value.
- If total\_transferred ≥ total\_picked.
  - Return “Completed”.
- Return “Partially Transferred”.

**Derived branch illustrations**

- At the comparison self.purpose equals “Delivery”, self.purpose = “Delivery” selects the branch that returns no value. With self.purpose = “Material Transfer for Manufacture”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-37d584310a0a93-guard-7)
- At the comparison total\_transferred ≤ 0, total\_transferred = 0 selects the branch that returns no value. With total\_transferred = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-37d584310a0a93-guard-15)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L1089) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L84)

<a id="op-60e89fd0651c85"></a>
### Pick List.is fully transferred

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_is_fully_transferred`

**Inputs** self.

**Explicit results** self.get\_transfer\_status() equals “Completed”.

**Local steps**

- Return self.get\_transfer\_status() equals “Completed”.

**Methods declared on this owner** [get transfer status](operations-038.md#op-37d584310a0a93).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L1360) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L89)

<a id="op-ad578df0b4c11c"></a>
### Pick List.is partially transferred

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_is_partially_transferred`

**Inputs** self.

**Explicit results** self.get\_transfer\_status() equals “Partially Transferred”.

**Local steps**

- Return self.get\_transfer\_status() equals “Partially Transferred”.

**Methods declared on this owner** [get transfer status](operations-038.md#op-37d584310a0a93).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L1423) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L90)

<a id="op-f5b888b2879347"></a>
### Pick List.update reference qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_reference_quantity`

**Inputs** self.

**Local steps**

- Set packed\_items from list().
- Set so\_items from list().
- For each item in self.locations.
  - If item.product\_bundle\_item.
    - Evaluate packed\_items.append(item.product\_bundle\_item).
  - Otherwise.
    - If item.sales\_order\_item.
      - Evaluate so\_items.append(item.sales\_order\_item).
- If packed\_items.
  - Evaluate self.update\_packed\_items\_qty(packed\_items).
- If so\_items.
  - Evaluate self.update\_sales\_order\_item\_qty(so\_items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update packed items qty](operations-038.md#op-16f1e2e94c2c27), [update sales order item qty](operations-038.md#op-b736bceea5e419).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L1486) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L108)

<a id="op-16f1e2e94c2c27"></a>
### Pick List.update packed items qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_packed_items_quantity`

**Inputs** self, packed\_items.

**State and service calls** request bulk\_update on “Packed Item”.

**Local steps**

- Set picked\_items from get\_picked\_items\_qty(packed\_items, contains\_packed\_items = true).
- Evaluate self.validate\_picked\_qty(picked\_items, “Packed Item”).
- Set doc\_updates from mapping of item → mapping(“picked\_qty” → 0) for item drawn from set(packed\_items).
  - Draw item from set(packed\_items).
- For each d in picked\_items.
  - Set doc\_updates at d.product\_bundle\_item from mapping(“picked\_qty” → flt(d.picked\_qty)).
- If doc\_updates.
  - Evaluate Platform.db.bulk\_update(“Packed Item”, doc\_updates, update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate picked qty](operations-039.md#op-bb470df4ddcf3d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L105)

<a id="op-b736bceea5e419"></a>
### Pick List.update sales order item qty

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_pick_list_update_sales_order_item_quantity`

**Inputs** self, so\_items.

**State and service calls** request bulk\_update on “Sales Order Item”.

**Local steps**

- Set picked\_items from get\_picked\_items\_qty(so\_items).
- Evaluate self.validate\_picked\_qty(picked\_items).
- Set doc\_updates from mapping of item → mapping(“picked\_qty” → 0) for item drawn from set(so\_items).
  - Draw item from set(so\_items).
- For each d in picked\_items.
  - Set doc\_updates at d.sales\_order\_item from mapping(“picked\_qty” → flt(d.picked\_qty)).
- If doc\_updates.
  - Evaluate Platform.db.bulk\_update(“Sales Order Item”, doc\_updates, update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate picked qty](operations-039.md#op-bb470df4ddcf3d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0763.json#L2010) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L109)
