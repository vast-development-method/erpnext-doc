# Shared transaction rules · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Sales and purchase return

<a id="op-bd7bba25cee40a"></a>
### Is rejected subcontracting return

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_is_rejected_subcontracting_return`

**Inputs** return\_row, original\_rejected\_warehouse.

**Declared result** bool.

**Explicit results** bool((return\_row.return\_qty\_from\_rejected\_warehouse and return\_row.warehouse and return\_row.warehouse equals original\_rejected\_warehouse)).

**Local steps**

- Return bool((return\_row.return\_qty\_from\_rejected\_warehouse and return\_row.warehouse and return\_row.warehouse equals original\_rejected\_warehouse)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in return\_row.return\_qty\_from\_rejected\_warehouse → return\_row.warehouse → return\_row.warehouse equals original\_rejected\_warehouse.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1094) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L334)

<a id="op-a94a80798cde9c"></a>
### Get warehouses for return

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_warehouses_for_return`

**Inputs** voucher\_type, name.

**Record and data access** read (voucher\_type + “ Item”) via get\_all.

**Explicit results** warehouses.

**Local steps**

- Set warehouses from list().
- Set warehouse\_details from Platform.get\_all((voucher\_type + “ Item”), filters = mapping(“name” → name, “docstatus” → 1), fields = list(“warehouse”, “rejected\_warehouse”)).
- For each d in warehouse\_details.
  - If d.warehouse.
    - Evaluate warehouses.append(d.warehouse).
  - If d.rejected\_warehouse.
    - Evaluate warehouses.append(d.rejected\_warehouse).
- Return warehouses.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L679) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L535)

<a id="op-9c308dc3d32b82"></a>
### Get returned serial nos

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_returned_serial_numbers`

**Inputs** child\_doc, parent\_doc, serial\_no\_field = no value, ignore\_voucher\_detail\_no = no value.

**Record and data access** read parent\_doc.doctype via get\_all.

**Explicit results** serial\_nos.

**Local steps**

- Bind dependencies get\_serial\_nos\_from\_serial\_no.
- Bind dependencies get\_serial\_nos.
- If not serial\_no\_field.
  - Set serial\_no\_field from “serial\_and\_batch\_bundle”.
- Set old\_field from “serial\_no”.
- If serial\_no\_field equals “rejected\_serial\_and\_batch\_bundle”.
  - Set old\_field from “rejected\_serial\_no”.
- Set return\_ref\_field from Platform.scrub(child\_doc.doctype).
- If child\_doc.doctype equals “Delivery Note Item”.
  - Set return\_ref\_field from “dn\_detail”.
- Set serial\_nos from list().
- Set fields from list(formatted text ′{(“tab” + child\_doc.doctype)}′.′{serial\_no\_field}′, formatted text ′{(“tab” + child\_doc.doctype)}′.′{old\_field}′).
- Set filters from list(list(parent\_doc.doctype, “return\_against”, “=”, parent\_doc.name), list(parent\_doc.doctype, “is\_return”, “=”, 1), list(child\_doc.doctype, return\_ref\_field, “=”, child\_doc.name), list(parent\_doc.doctype ….
- If serial\_no\_field equals “rejected\_serial\_and\_batch\_bundle”.
  - Evaluate filters.append(list(child\_doc.doctype, “rejected\_qty”, “&gt;”, 0)).
- If ignore\_voucher\_detail\_no.
  - Evaluate filters.append(list(child\_doc.doctype, “name”, “!=”, ignore\_voucher\_detail\_no)).
- Set ids from list().
- For each row in Platform.get\_all(parent\_doc.doctype, fields = fields, filters = filters).
  - Evaluate ids.append(row.get(“serial\_and\_batch\_bundle”)).
  - If (row.get(old\_field) and not row.get(serial\_no\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(old\_field) → not row.get(serial\_no\_field).
    - Evaluate serial\_nos.extend(get\_serial\_nos\_from\_serial\_no(row.get(old\_field))).
- If ids.
  - Evaluate serial\_nos.extend(get\_serial\_nos(ids)).
- Return serial\_nos.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L944) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L850) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L531)

<a id="op-9744b95b004837"></a>
### Get returned batches

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_returned_batches`

**Inputs** child\_doc, parent\_doc, batch\_no\_field = no value, ignore\_voucher\_detail\_no = no value.

**Record and data access** read parent\_doc.doctype via get\_all.

**Explicit results** batches.

**Local steps**

- Set batches from Platform.\_dict().
- Set old\_field from “batch\_no”.
- If not batch\_no\_field.
  - Set batch\_no\_field from “serial\_and\_batch\_bundle”.
- Set return\_ref\_field from Platform.scrub(child\_doc.doctype).
- If child\_doc.doctype equals “Delivery Note Item”.
  - Set return\_ref\_field from “dn\_detail”.
- Set fields from list(formatted text ′{(“tab” + child\_doc.doctype)}′.′{batch\_no\_field}′, formatted text ′{(“tab” + child\_doc.doctype)}′.′batch\_no′, formatted text ′{(“tab” + child\_doc.doctype)}′.′stock\_qty′).
- Set filters from list(list(parent\_doc.doctype, “return\_against”, “=”, parent\_doc.name), list(parent\_doc.doctype, “is\_return”, “=”, 1), list(child\_doc.doctype, return\_ref\_field, “=”, child\_doc.name), list(parent\_doc.doctype ….
- If batch\_no\_field equals “rejected\_serial\_and\_batch\_bundle”.
  - Evaluate filters.append(list(child\_doc.doctype, “rejected\_qty”, “&gt;”, 0)).
- If ignore\_voucher\_detail\_no.
  - Evaluate filters.append(list(child\_doc.doctype, “name”, “!=”, ignore\_voucher\_detail\_no)).
- Set ids from list().
- For each row in Platform.get\_all(parent\_doc.doctype, fields = fields, filters = filters).
  - Evaluate ids.append(row.get(“serial\_and\_batch\_bundle”)).
  - If (row.get(old\_field) and not row.get(batch\_no\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(old\_field) → not row.get(batch\_no\_field).
    - Evaluate batches.setdefault(row.get(old\_field), row.get(“stock\_qty”)).
- If ids.
  - Evaluate batches.update(get\_batches\_from\_bundle(ids)).
- Return batches.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L1874) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L847) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L528)

<a id="op-226b7f820d5a34"></a>
### Available serial batch for return

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_available_serial_batch_for_return`

**Inputs** field, doctype, reference\_ids, is\_rejected = false.

**Explicit results** available\_dict.

**Explicit failure paths** validation helper — translated “No Serial / Batches are available for return”.

**Local steps**

- Set available\_dict from get\_available\_serial\_batches(field, doctype, reference\_ids, is\_rejected = is\_rejected).
- If not available\_dict.
  - Call the validation error handler Platform.throw(translated “No Serial / Batches are available for return”).
- Return available\_dict.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L2786) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L834) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L515)

<a id="op-fa5c7413f7292d"></a>
### Get available serial batches

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_available_serial_batches`

**Inputs** field, doctype, reference\_ids, is\_rejected = false.

**Explicit results** Platform.\_dict(mapping()) · get\_serial\_batches\_based\_on\_bundle(doctype, field, \_bundle\_ids).

**Local steps**

- Set \_bundle\_ids from get\_serial\_and\_batch\_bundle(field, doctype, reference\_ids, is\_rejected = is\_rejected).
- If not \_bundle\_ids.
  - Return Platform.\_dict(mapping()).
- Return get\_serial\_batches\_based\_on\_bundle(doctype, field, \_bundle\_ids).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L2948) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L838) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L519)

<a id="op-3c42e4c088fecf"></a>
### Get serial batches based on bundle

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_serial_batches_based_on_bundle`

**Inputs** doctype, field, \_bundle\_ids.

**Record and data access** read “Serial and Batch Bundle” via get\_all · read row.voucher\_type via get\_cached\_value · read (row.voucher\_type + “ Item”) via get\_cached\_value · read “Packed Item” via get\_cached\_value · read “Delivery Note Item” via get\_cached\_value · 1 additional forms in the steps below.

**Explicit results** available\_dict.

**Local steps**

- Set available\_dict from Platform.\_dict(mapping()).
- Set batch\_serial\_nos from Platform.get\_all(“Serial and Batch Bundle”, fields = list(“′tabSerial and Batch Entry′.′serial\_no′”, “′tabSerial and Batch Entry′.′batch\_no′”, “′tabSerial and Batch Entry′.′qty′”, “′tabSerial and Batch Ent ….
- For each row in batch\_serial\_nos.
  - Set key from row.voucher\_detail\_no.
  - If Platform.get\_cached\_value(row.voucher\_type, row.voucher\_no, “is\_return”).
    - Set key from Platform.get\_cached\_value((row.voucher\_type + “ Item”), row.voucher\_detail\_no, field).
  - If doctype equals “Packed Item”.
    - If key is identical to no value.
      - Set key from Platform.get\_cached\_value(“Packed Item”, mapping(“parent\_detail\_docname” → row.voucher\_detail\_no, “item\_code” → row.item\_code), field).
      - If key is identical to no value.
        - Set key from Platform.get\_cached\_value(“Packed Item”, row.voucher\_detail\_no, field).
      - If row.voucher\_type equals “Delivery Note”.
        - Set key from Platform.get\_cached\_value(“Delivery Note Item”, key, “dn\_detail”).
      - Otherwise.
        - If row.voucher\_type equals “Sales Invoice”.
          - Set key from Platform.get\_cached\_value(“Sales Invoice Item”, key, “sales\_invoice\_item”).
    - Set key from tuple(row.item\_code, key).
  - If row.voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”).
    - Set row.qty from (negative 1 × row.qty).
  - If key does not belong to available\_dict.
    - Set available\_dict at key from Platform.\_dict(mapping(“qty” → 0.0, “serial\_nos” → defaultdict(float), “batches” → defaultdict(float), “serial\_nos\_valuation” → defaultdict(float), …)).
  - Update available\_dict at key at “qty” using + row.qty.
  - If row.serial\_no.
    - Update available\_dict at key at “serial\_nos” at row.serial\_no using + row.qty.
    - Set available\_dict at key at “serial\_nos\_valuation” at row.serial\_no from row.incoming\_rate.
  - Otherwise.
    - If row.batch\_no.
      - Update available\_dict at key at “batches” at row.batch\_no using + row.qty.
      - Set available\_dict at key at “batches\_valuation” at row.batch\_no from row.incoming\_rate.
- Return available\_dict.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(row.voucher\_type, row.voucher\_no, “is\_return”), Platform.get\_cached\_value((row.voucher\_type + “ Item”), row.voucher\_detail\_no, field) and 4 further calls.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L3117) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L853) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L534)

<a id="op-ed4c04783d85a8"></a>
### Get serial and batch bundle

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_serial_and_batch_bundle`

**Inputs** field, doctype, reference\_ids, is\_rejected = false.

**Record and data access** read doctype via get\_all.

**Explicit results** \_bundle\_ids · mapping().

**Local steps**

- Set filters from mapping(“docstatus” → 1, “name” → tuple(“in”, reference\_ids), “serial\_and\_batch\_bundle” → tuple(“is”, “set”)).
- If doctype equals “Packed Item”.
  - Set filters from get\_filters\_for\_packed\_item(field, reference\_ids).
- Set pluck\_field from “serial\_and\_batch\_bundle”.
- If is\_rejected.
  - Remove filters at “serial\_and\_batch\_bundle”.
  - Set filters at “rejected\_serial\_and\_batch\_bundle” from tuple(“is”, “set”).
  - Set pluck\_field from “rejected\_serial\_and\_batch\_bundle”.
- Set \_bundle\_ids from Platform.get\_all(doctype, filters = filters, pluck = pluck\_field).
- If (\_bundle\_ids and doctype equals “Packed Item”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_bundle\_ids → doctype equals “Packed Item”.
  - Return \_bundle\_ids.
- If not \_bundle\_ids.
  - Return mapping().
- If “name” belongs to filters.
  - Remove filters at “name”.
- Set filters at field from tuple(“in”, reference\_ids).
- If not is\_rejected.
  - Evaluate \_bundle\_ids.extend(Platform.get\_all(doctype, filters = filters, pluck = “serial\_and\_batch\_bundle”)).
- Otherwise.
  - Set fields from list(“serial\_and\_batch\_bundle”).
  - If is\_rejected.
    - Evaluate fields.append(“rejected\_serial\_and\_batch\_bundle”).
    - If doctype equals “Purchase Receipt Item”.
      - Evaluate fields.append(“return\_qty\_from\_rejected\_warehouse”).
  - Remove filters at “rejected\_serial\_and\_batch\_bundle”.
  - Set data from Platform.get\_all(doctype, fields = fields, filters = filters).
  - For each d in data.
    - If (not d.get(“serial\_and\_batch\_bundle”) and not d.get(“rejected\_serial\_and\_batch\_bundle”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.get(“serial\_and\_batch\_bundle”) → not d.get(“rejected\_serial\_and\_batch\_bundle”).
      - Continue with the next iteration or loop test.
    - If is\_rejected.
      - If d.get(“return\_qty\_from\_rejected\_warehouse”).
        - Evaluate \_bundle\_ids.append(d.get(“serial\_and\_batch\_bundle”)).
      - Otherwise.
        - Evaluate \_bundle\_ids.append(d.get(“rejected\_serial\_and\_batch\_bundle”)).
    - Otherwise.
      - Evaluate \_bundle\_ids.append(d.get(“serial\_and\_batch\_bundle”)).
- Return \_bundle\_ids.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L4368) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L852) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L533)

<a id="op-85a3832c70a8b5"></a>
### Get filters for packed item

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_filters_for_packed_item`

**Inputs** field, reference\_ids.

**Record and data access** read “Delivery Note Item” via get\_all · read “Sales Invoice Item” via get\_all.

**Explicit results** mapping(“docstatus” → 1, field → tuple(“in”, reference\_ids), “serial\_and\_batch\_bundle” → tuple(“is”, “set”)).

**Local steps**

- Set names from list().
- Set filters from mapping(“docstatus” → 1, “dn\_detail” → tuple(“in”, reference\_ids)).
- If dns bound to Platform.get\_all(“Delivery Note Item”, filters = filters, pluck = “name”).
  - Evaluate names.extend(dns).
- Set filters from mapping(“docstatus” → 1, “sales\_invoice\_item” → tuple(“in”, reference\_ids)).
- If sis bound to Platform.get\_all(“Sales Invoice Item”, filters = filters, pluck = “name”).
  - Evaluate names.extend(sis).
- If names.
  - Evaluate reference\_ids.extend(names).
- Return mapping(“docstatus” → 1, field → tuple(“in”, reference\_ids), “serial\_and\_batch\_bundle” → tuple(“is”, “set”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L5383) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L841) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L522)

<a id="op-6908caa1071327"></a>
### Filter serial batches

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_filter_serial_batches`

**Inputs** parent\_doc, data, row, warehouse\_field = no value, qty\_field = no value.

**Explicit results** filterd\_serial\_batch.

**Explicit failure paths** validation helper — translated “Batch {0} is not available in warehouse {1}”.format(unavailable\_batch, warehouse).

**Local steps**

- If not qty\_field.
  - Set qty\_field from “stock\_qty”.
- If not hasattr(row, qty\_field).
  - Set qty\_field from “qty”.
- If not warehouse\_field.
  - Set warehouse\_field from “warehouse”.
- Set warehouse from row.get(warehouse\_field).
- Set qty from abs(get\_return\_bundle\_qty(row, qty\_field)).
- Set filterd\_serial\_batch from Platform.\_dict(mapping(“serial\_nos” → list(), “batches” → defaultdict(float), “serial\_nos\_valuation” → data.get(“serial\_nos\_valuation”), “batches\_valuation” → data.get(“batches\_valuation”))).
- If data.serial\_nos.
  - Set available\_serial\_nos from list().
  - For each tuple(serial\_no, sn\_qty) in data.serial\_nos.items().
    - If sn\_qty differs from 0.
      - Evaluate available\_serial\_nos.append(serial\_no).
  - If available\_serial\_nos.
    - If parent\_doc.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
      - Set available\_serial\_nos from get\_available\_serial\_nos(available\_serial\_nos, warehouse).
    - If len(available\_serial\_nos) &gt; qty.
      - Set filterd\_serial\_batch at “serial\_nos” from sorted(available\_serial\_nos at slice 0 to cint(qty)).
    - Otherwise.
      - Set filterd\_serial\_batch at “serial\_nos” from available\_serial\_nos.
- Otherwise.
  - If data.batches.
    - Set unavailable\_batch from no value.
    - For each tuple(batch\_no, batch\_qty) in data.batches.items().
      - <a id="op-6908caa1071327-guard-41"></a>If qty ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - If parent\_doc.get(“is\_internal\_customer”).
        - Set batch\_qty from (batch\_qty × negative 1).
      - <a id="op-6908caa1071327-guard-47"></a>If batch\_qty ≤ 0.
        - Continue with the next iteration or loop test.
      - If parent\_doc.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
        - Set batch\_qty from min(batch\_qty, get\_available\_batch\_qty(parent\_doc, batch\_no, warehouse)).
        - If batch\_qty ≤ 0.
          - Set unavailable\_batch from batch\_no.
          - Continue with the next iteration or loop test.
      - If batch\_qty &gt; qty.
        - Set filterd\_serial\_batch at “batches” at batch\_no from qty.
        - Set qty from 0.
      - Otherwise.
        - Update filterd\_serial\_batch at “batches” at batch\_no using + batch\_qty.
        - Update qty using − batch\_qty.
    - If (unavailable\_batch and not filterd\_serial\_batch at “batches”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in unavailable\_batch → not filterd\_serial\_batch at “batches”.
      - Call the validation error handler Platform.throw(translated “Batch {0} is not available in warehouse {1}”.format(unavailable\_batch, warehouse), title = translated “Batch Not Available for Return”).
- Return filterd\_serial\_batch.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6908caa1071327-guard-41)
- At the comparison batch\_qty ≤ 0, batch\_qty = 0 selects the branch that continues with the next loop iteration. With batch\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6908caa1071327-guard-47)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L835) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L516)

<a id="op-e4b71cb8ffafe6"></a>
### Remove picked serial batches

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_remove_picked_serial_batches`

**Inputs** data, picked, parent\_doc.

**Local steps**

- For each serial\_no in picked.serial\_nos.
  - Evaluate data.serial\_nos.pop(serial\_no, no value).
- Set sign from negative 1 when parent\_doc.get(“is\_internal\_customer”), otherwise 1.
  - Value choice on parent\_doc.get(“is\_internal\_customer”) — true gives negative 1, false gives 1.
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- For each tuple(batch\_no, qty) in picked.batches.items().
  - Set data.batches at batch\_no from flt((data.batches at batch\_no − (sign × qty)), precision).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1096) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L336)

<a id="op-c15748ff3b6f9f"></a>
### Get available batch qty

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_available_batch_quantity`

**Inputs** parent\_doc, batch\_no, warehouse.

**Explicit results** get\_batch\_qty\_for\_stock(batch\_no, warehouse, posting\_date = parent\_doc.posting\_date, posting\_time = parent\_doc.posting\_time, for\_stock\_levels = true).

**Local steps**

- Return get\_batch\_qty\_for\_stock(batch\_no, warehouse, posting\_date = parent\_doc.posting\_date, posting\_time = parent\_doc.posting\_time, for\_stock\_levels = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L837) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L518)

<a id="op-7cfae856691f47"></a>
### Make serial batch bundle for return

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_serial_batch_bundle_for_return`

**Inputs** data, child\_doc, parent\_doc, warehouse\_field = no value, qty\_field = no value.

**Explicit results** cls\_obj.name.

**Explicit failure paths** validation helper — translated “For the {0}, the quantity is required to make the return entry”.format(Platform.bold(child\_doc.item\_code)).

**Local steps**

- Bind dependencies SerialBatchCreation.
- Set type\_of\_transaction from “Outward”.
- If parent\_doc.doctype belongs to list(“Sales Invoice”, “Delivery Note”, “POS Invoice”).
  - Set type\_of\_transaction from “Inward”.
- If not warehouse\_field.
  - Set warehouse\_field from “warehouse”.
- If not qty\_field.
  - Set qty\_field from “stock\_qty”.
- If not hasattr(child\_doc, qty\_field).
  - Set qty\_field from “qty”.
- Set warehouse from child\_doc.get(warehouse\_field).
- If parent\_doc.get(“is\_internal\_customer”).
  - Set warehouse from child\_doc.get(“target\_warehouse”).
  - Set type\_of\_transaction from “Outward”.
- If not child\_doc.get(qty\_field).
  - Call the validation error handler Platform.throw(translated “For the {0}, the quantity is required to make the return entry”.format(Platform.bold(child\_doc.item\_code))).
- Set cls\_obj from SerialBatchCreation(mapping(“type\_of\_transaction” → type\_of\_transaction, “item\_code” → child\_doc.item\_code, “warehouse” → warehouse, “serial\_nos” → data.get(“serial\_nos”), …)).make\_serial\_and\_batch\_bundle().
- Return cls\_obj.name.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L864) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L545)

<a id="op-13b7500ae030e4"></a>
### Get return bundle qty

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_get_return_bundle_qty`

**Inputs** row, qty\_field.

**Explicit results** get\_stock\_qty(row, row.rejected\_qty) · row.get(qty\_field).

**Local steps**

- Bind dependencies get\_stock\_qty.
- If qty\_field equals “rejected\_qty”.
  - Return get\_stock\_qty(row, row.rejected\_qty).
- Return row.get(qty\_field).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1090) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L330)

<a id="op-1fc3b84c18b21c"></a>
### Get available serial nos

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_available_serial_numbers`

**Inputs** serial\_nos, warehouse.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** Platform.get\_all(“Serial No”, filters = mapping(“warehouse” → warehouse, “name” → tuple(“in”, serial\_nos)), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“Serial No”, filters = mapping(“warehouse” → warehouse, “name” → tuple(“in”, serial\_nos)), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L861) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L839) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L520)

<a id="op-1f08eb4e00029c"></a>
### Get payment data

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_payment_data`

**Inputs** invoice.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Invoice Payment” via get\_value · read “Sales Invoice Payment” via get\_all.

**Explicit results** list() · payment.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid document type”.

**Local steps**

- Set parenttype from Platform.db.get\_value(“Sales Invoice Payment”, mapping(“parent” → invoice), “parenttype”).
- If not parenttype.
  - Return list().
- If parenttype does not belong to RETURNABLE\_INVOICE\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Invalid document type”, Platform.PermissionError).
- Evaluate Platform.has\_permission(parenttype, doc = invoice, throw = true).
- Set payment from Platform.db.get\_all(“Sales Invoice Payment”, mapping(“parent” → invoice), list(“mode\_of\_payment”, “amount”)).
- Return payment.

**Values supplied outside this operation** effective access from Platform.has\_permission(parenttype, doc = invoice, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L843) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L524)

<a id="op-91e868c7a4e6b3"></a>
### Validate returnable invoice

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_validate_returnable_invoice`

**Inputs** doctype, invoice.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid document type”.

**Local steps**

- If doctype does not belong to RETURNABLE\_INVOICE\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Invalid document type”, Platform.PermissionError).
- Evaluate Platform.has\_permission(doctype, doc = invoice, throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = invoice, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1098) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L338)

<a id="op-76031895d75673"></a>
### Get invoice item returned qty

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_invoice_item_returned_quantity`

**Inputs** doctype, invoice, customer, item\_row\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_value.

**Explicit results** get\_returned\_qty\_map\_for\_row(invoice, customer, item\_row\_name, doctype).

**Local steps**

- Evaluate validate\_returnable\_invoice(doctype, invoice).
- Set tuple(is\_return, docstatus) from Platform.db.get\_value(doctype, invoice, list(“is\_return”, “docstatus”)).
- If (not is\_return and docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_return → docstatus equals 1.
  - Return get\_returned\_qty\_map\_for\_row(invoice, customer, item\_row\_name, doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L842) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L523)

<a id="op-ad3c00c0e2c56d"></a>
### Is invoice returnable

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_is_invoice_returnable`

**Inputs** doctype, invoice.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_value · read formatted text {doctype} Item via get\_all.

**Explicit results** false · len(invoice\_item\_qty) differs from already\_full\_returned.

**Local steps**

- Evaluate validate\_returnable\_invoice(doctype, invoice).
- Set tuple(is\_return, docstatus, customer) from Platform.db.get\_value(doctype, invoice, list(“is\_return”, “docstatus”, “customer”)).
- If (is\_return or docstatus equals 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_return → docstatus equals 0.
  - Return false.
- Set invoice\_item\_qty from Platform.db.get\_all(formatted text {doctype} Item, mapping(“parent” → invoice), list(“name”, “qty”)).
- Set already\_full\_returned from 0.
- For each d in invoice\_item\_qty.
  - Set returned\_qty from get\_returned\_qty\_map\_for\_row(invoice, customer, d.name, doctype).
  - If returned\_qty.qty equals d.qty.
    - Update already\_full\_returned using + 1.
- Return len(invoice\_item\_qty) differs from already\_full\_returned.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L537)

<a id="op-9fbbedeb7670ef"></a>
### Get sales invoice item from consolidated invoice

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_sales_invoice_item_from_consolidated_invoice`

**Inputs** return\_against\_pos\_invoice, pos\_invoice\_item.

**Explicit results** result at 0.name when result, otherwise no value · no value.

**Local steps**

- Attempt the following.
  - Set SalesInvoice from DocType(“Sales Invoice”).
  - Set SalesInvoiceItem from DocType(“Sales Invoice Item”).
  - Set query from nested operand in the contract(nested operand in the contract).from\_(SalesInvoiceItem).select(SalesInvoiceItem.name).where((((SalesInvoice.name equals SalesInvoiceItem.parent bitwise and SalesInvoice.is\_re ….
  - Set result from query.run(as\_dict = true).
  - Return result at 0.name when result, otherwise no value.
    - Value choice on result — true gives result at 0.name, false gives no value.
- On failure (Exception).
  - Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L1807) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L532)

<a id="op-4434410253fdd8"></a>
### Is batch expired

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_is_batch_expired`

**Inputs** batch\_no, posting\_date.

**Record and data access** read “Batch” via get\_value.

**Explicit results** no value · true · false.

**Local steps**

- Set expiry\_date from Platform.db.get\_value(“Batch”, batch\_no, “expiry\_date”).
- If not expiry\_date.
  - Return no value.
- If getdate(posting\_date) &gt; getdate(expiry\_date).
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L2182) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L536)

<a id="op-b6ecddf76d094f"></a>
### Get change by payment row

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_get_change_by_payment_row`

**Inputs** invoice.

**Explicit results** change\_by\_row.

**Local steps**

- Bind dependencies get\_change\_payment\_row.
- Set change\_row from get\_change\_payment\_row(invoice.payments, invoice.account\_for\_change\_amount).
- Set rows from sorted(invoice.payments, key = deferred anonymous expression).
- Set change\_left from flt(invoice.change\_amount).
- Set change\_by\_row from mapping().
- For each row in rows.
  - Set change\_by\_row at row.idx from min(change\_left, flt(row.amount)).
  - Update change\_left using − change\_by\_row at row.idx.
- Return change\_by\_row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1087) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L327)

## Service · Selling controller

<a id="op-538eaf15da83ad"></a>
### Selling Controller.setup

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_setup`

**Inputs** self.

**Local steps**

- Set self.flags.ignore\_permlevel\_for\_fields from list(“selling\_price\_list”, “price\_list\_currency”).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L2355) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L579)

<a id="op-db9df0262c20eb"></a>
### Selling Controller.onload

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_onload`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Company” via get\_value · resolve a document from “Terms and Conditions” via get\_cached\_doc.

**Local steps**

- Evaluate super().onload().
- If (self.doctype belongs to tuple(“Sales Order”, “Delivery Note”, “Sales Invoice”, “Quotation”) and self.docstatus.is\_draft() and not hasattr(self, “\_action”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to tuple(“Sales Order”, “Delivery Note”, “Sales Invoice”, “Quotation”) → self.docstatus.is\_draft() → not hasattr(self, “\_action”).
  - For each item in (self.get(“items”) + (self.get(“packed\_items”) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“packed\_items”) → list().
    - Set company from self.company.
    - Evaluate item.update(\_get\_bin\_details(item.item\_code, item.warehouse, company = company, include\_child\_warehouses = true)).
- If (self.docstatus equals 1 and self.doctype belongs to list(“Delivery Note”, “Sales Invoice”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.doctype belongs to list(“Delivery Note”, “Sales Invoice”).
  - Evaluate self.set\_onload(“allow\_to\_make\_qc\_after\_submission”, Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”)).
- If (self.docstatus.is\_draft() and self.get(“company”) and not self.get(“terms”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus.is\_draft() → self.get(“company”) → not self.get(“terms”).
  - If not self.get(“tc\_name”).
    - Set self.tc\_name from Platform.get\_value(“Company”, self.company, “default\_selling\_terms”).
  - Set tnc from Platform.get\_cached\_doc(“Terms and Conditions”, self.tc\_name) when self.tc\_name, otherwise no value.
    - Value choice on self.tc\_name — true gives Platform.get\_cached\_doc(“Terms and Conditions”, self.tc\_name), false gives no value.
  - If (tnc and not tnc.disabled and tnc.get(“selling”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tnc → not tnc.disabled → tnc.get(“selling”).
    - Evaluate self.set\_missing\_terms\_for\_display().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”), Platform.get\_cached\_doc(“Terms and Conditions”, self.tc\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L563)
