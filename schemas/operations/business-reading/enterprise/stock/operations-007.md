# Inventory and warehouses · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Delivery note

[Record definition](../../../../data/record-types/delivery_note.json)

<a id="op-713b883e6305aa"></a>
### Delivery Note.validate dependent item fields

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_dependent_item_fields`

**Inputs** self, field\_a, field\_b, error\_title.

**Explicit failure paths** validation helper — text in the contract.join(errors).

**Local steps**

- Set errors from list().
- For each item in self.items.
  - Set missing\_label from no value.
  - If (item.get(field\_a) and not item.get(field\_b)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(field\_a) → not item.get(field\_b).
    - Set missing\_label from item.meta.get\_label(field\_b).
  - Otherwise.
    - If (item.get(field\_b) and not item.get(field\_a)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(field\_b) → not item.get(field\_a).
      - Set missing\_label from item.meta.get\_label(field\_a).
  - If (missing\_label and missing\_label differs from “No Label”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in missing\_label → missing\_label differs from “No Label”.
    - Evaluate errors.append(translated “The field {0} in row {1} is not set”.format(Platform.bold(translated missing\_label), Platform.bold(item.idx))).
- If errors.
  - Call the validation error handler Platform.throw(text in the contract.join(errors), title = error\_title).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L883)

<a id="op-f6ab5d9dab6e71"></a>
### Delivery Note.validate proj cust

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_project_customer`

**Inputs** self.

**Record and data access** execute query text (SELECT, Project).

**Explicit failure paths** validation helper — translated “Customer {0} does not belong to project {1}”.format(self.customer, self.project).

**Local steps**

- If (self.project and self.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project → self.customer.
  - Set res from Platform.db.sql(query text (SELECT, Project), tuple(self.project, self.customer)).
  - If not res.
    - Call the validation error handler Platform.throw(translated “Customer {0} does not belong to project {1}”.format(self.customer, self.project)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L885)

<a id="op-69f1db00cd2844"></a>
### Delivery Note.validate warehouse

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_warehouse`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Warehouse required for stock Item {0}”.format(d at “item\_code”).

**Local steps**

- Evaluate super().validate\_warehouse().
- For each d in self.get\_item\_list().
  - If (not d at “warehouse” and Platform.get\_cached\_value(“Item”, d at “item\_code”, “is\_stock\_item”) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d at “warehouse” → Platform.get\_cached\_value(“Item”, d at “item\_code”, “is\_stock\_item”) equals 1.
    - Call the validation error handler Platform.throw(translated “Warehouse required for stock Item {0}”.format(d at “item\_code”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d at “item\_code”, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0713.json#L2587) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L889)

<a id="op-3602af0f06aae4"></a>
### Delivery Note.update current stock

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_update_current_stock`

**Inputs** self.

**Record and data access** read “Bin” via get\_all.

**Explicit results** no value.

**Local steps**

- If not (self.get(“\_action”) and self.\_action differs from “update\_after\_submit”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“\_action”) → self.\_action differs from “update\_after\_submit”.
  - Return no value.
- Set warehouse\_item\_codes from mapping().
- For each d in (self.get(“items”) + self.get(“packed\_items”)).
  - Evaluate warehouse\_item\_codes.setdefault(d.warehouse, set()).add(d.item\_code).
- If not warehouse\_item\_codes.
  - Return no value.
- Set bin\_map from mapping().
- For each tuple(warehouse, item\_codes) in warehouse\_item\_codes.items().
  - For each b in Platform.get\_all(“Bin”, filters = mapping(“item\_code” → list(“in”, item\_codes), “warehouse” → warehouse), fields = list(“item\_code”, “actual\_qty”, “projected\_qty”)).
    - Set bin\_map at tuple(b.item\_code, warehouse) from b.
- For each d in self.get(“items”).
  - Set bin\_data from bin\_map.get(tuple(d.item\_code, d.warehouse)).
  - Set d.actual\_qty from bin\_data.actual\_qty when bin\_data, otherwise no value.
    - Value choice on bin\_data — true gives bin\_data.actual\_qty, false gives no value.
- For each d in self.get(“packed\_items”).
  - Set bin\_data from bin\_map.get(tuple(d.item\_code, d.warehouse)).
  - If bin\_data.
    - Set d.actual\_qty from flt(bin\_data.actual\_qty).
    - Set d.projected\_qty from flt(bin\_data.projected\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L880)

<a id="op-1a7cd28186e661"></a>
### Delivery Note.on submit

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Authorization Control” via get\_cached\_doc.

**Local steps**

- Evaluate self.validate\_packed\_qty().
- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(self.doctype, self.company, self.base\_grand\_total, self).
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.update\_pick\_list\_status().
- Evaluate self.update\_billing\_status().
- If not self.is\_return.
  - Evaluate self.check\_credit\_limit().
- Otherwise.
  - If self.issue\_credit\_note.
    - Evaluate self.make\_return\_invoice().
- For each table\_name in list(“items”, “packed\_items”).
  - If not self.get(table\_name).
    - Continue with the next iteration or loop test.
  - Evaluate self.make\_bundle\_for\_sales\_purchase\_return(table\_name).
  - Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields(table\_name).
- Evaluate self.validate\_standalone\_serial\_nos\_customer().
- Evaluate self.make\_packed\_item\_bundles().
- Evaluate self.update\_stock\_reservation\_entries().
- Evaluate self.update\_stock\_ledger().
- Evaluate self.validate\_produced\_serial\_nos\_against\_reservation().
- Evaluate self.make\_gl\_entries().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.update\_project\_consumed\_material\_cost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate packed qty](operations-007.md#op-9e2a72d55c2353), [update status updater args](operations-006.md#op-3276bd923be9d1), [update billing status](operations-007.md#op-15923547dcacd7), [check credit limit](operations-007.md#op-a0362ed4afe72f), [make return invoice](operations-007.md#op-b68068ab2a0da9).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L876)

<a id="op-c459fdae87f18d"></a>
### Delivery Note.on cancel

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().on\_cancel().
- Evaluate self.check\_sales\_order\_on\_hold\_or\_close(“against\_sales\_order”).
- Evaluate self.check\_next\_docstatus().
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.update\_billing\_status().
- Evaluate self.update\_stock\_reservation\_entries().
- Evaluate self.update\_stock\_ledger().
- Evaluate self.cancel\_packing\_slips().
- Evaluate self.update\_pick\_list\_status().
- Evaluate self.make\_gl\_entries\_on\_cancel().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.update\_project\_consumed\_material\_cost().
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Serial and Batch Bundle”, …).
- Evaluate self.delete\_auto\_created\_batches().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check next docstatus](operations-007.md#op-e7089b4ea8551e), [update status updater args](operations-006.md#op-3276bd923be9d1), [update billing status](operations-007.md#op-15923547dcacd7), [cancel packing slips](operations-007.md#op-64d80e5d0f506a).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L875)

<a id="op-a0362ed4afe72f"></a>
### Delivery Note.check credit limit

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_check_credit_limit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies check\_credit\_limit, is\_sales\_order\_credit\_check\_bypassed.
- <a id="op-a0362ed4afe72f-guard-7"></a>If self.per\_billed equals 100.
  - Return no value.
- Set extra\_amount from 0.
- Set validate\_against\_credit\_limit from false.
- Set bypass\_credit\_limit\_check\_at\_sales\_order from is\_sales\_order\_credit\_check\_bypassed(self.customer, self.company).
- If bypass\_credit\_limit\_check\_at\_sales\_order.
  - For each d in self.get(“items”).
    - If not d.against\_sales\_invoice.
      - Set validate\_against\_credit\_limit from true.
      - If (self.docstatus equals 0 and self.base\_net\_total).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 0 → self.base\_net\_total.
        - Update extra\_amount using + ((d.base\_net\_amount ÷ self.base\_net\_total) × self.base\_grand\_total).
  - If (validate\_against\_credit\_limit and not self.base\_net\_total).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in validate\_against\_credit\_limit → not self.base\_net\_total.
    - Set extra\_amount from self.base\_grand\_total.
- Otherwise.
  - For each d in self.get(“items”).
    - If not (d.against\_sales\_order or d.against\_sales\_invoice).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.against\_sales\_order → d.against\_sales\_invoice.
      - Set validate\_against\_credit\_limit from true.
      - Leave the innermost loop without its normal-exhaustion alternative.
- If validate\_against\_credit\_limit.
  - Evaluate check\_credit\_limit(self.customer, self.company, bypass\_credit\_limit\_check\_at\_sales\_order, extra\_amount).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.per\_billed equals 100, self.per\_billed = 100 selects the branch that returns no value. With self.per\_billed = 101, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-a0362ed4afe72f-guard-7)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L871)

<a id="op-9e2a72d55c2353"></a>
### Delivery Note.validate packed qty

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_packed_quantity`

**Inputs** self.

**Record and data access** read “Packing Slip” via exists.

**Explicit failure paths** validation helper — translated “Row {0}: Packed Qty must be equal to {1} Qty.”.format(item.idx, Platform.bold(item.doctype)).

**Local steps**

- If Platform.db.exists(“Packing Slip”, mapping(“docstatus” → 1, “delivery\_note” → self.name)).
  - Set product\_bundle\_list from self.get\_product\_bundle\_list().
  - For each item in (self.items + self.packed\_items).
    - If (item.item\_code does not belong to product\_bundle\_list and flt(item.packed\_qty) and flt(item.packed\_qty) differs from flt(item.qty)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code does not belong to product\_bundle\_list → flt(item.packed\_qty) → flt(item.packed\_qty) differs from flt(item.qty).
      - Call the validation error handler Platform.throw(translated “Row {0}: Packed Qty must be equal to {1} Qty.”.format(item.idx, Platform.bold(item.doctype))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get product bundle list](operations-007.md#op-543b81d309a620).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L884)

<a id="op-e7089b4ea8551e"></a>
### Delivery Note.check next docstatus

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_check_next_record_state`

**Inputs** self.

**Record and data access** execute query text (SELECT, Sales Invoice) · execute query text (SELECT, Installation Note).

**Explicit failure paths** validation helper — translated “Sales Invoice {0} has already been submitted”.format(submit\_rv at 0 at 0) · validation helper — translated “Installation Note {0} has already been submitted”.format(submit\_in at 0 at 0).

**Local steps**

- Set submit\_rv from Platform.db.sql(query text (SELECT, Sales Invoice), self.name).
- If submit\_rv.
  - Call the validation error handler Platform.throw(translated “Sales Invoice {0} has already been submitted”.format(submit\_rv at 0 at 0)).
- Set submit\_in from Platform.db.sql(query text (SELECT, Installation Note), self.name).
- If submit\_in.
  - Call the validation error handler Platform.throw(translated “Installation Note {0} has already been submitted”.format(submit\_in at 0 at 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L872)

<a id="op-64d80e5d0f506a"></a>
### Delivery Note.cancel packing slips

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_deliverynote_cancel_packing_slips`

**Inputs** self.

**Record and data access** execute query text (SELECT, Packing Slip) · resolve a document from “Packing Slip” via get\_doc.

**State and service calls** call cancel on ps · msgprint with translated “Packing Slip(s) cancelled”.

**Local steps**

- Set res from Platform.db.sql(query text (SELECT, Packing Slip), self.name).
- If res.
  - For each r in res.
    - Set ps from Platform.get\_doc(“Packing Slip”, r at 0).
    - Set ps.flags.cancelled\_by\_delivery\_note from true.
    - Evaluate ps.cancel().
  - Evaluate Platform.msgprint(translated “Packing Slip(s) cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L214)

<a id="op-602ef5cb0028a0"></a>
### Delivery Note.update status

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_update_status`

**Inputs** self, status.

**Local steps**

- Evaluate self.set\_status(update = true, status = status).
- Evaluate self.notify\_update().
- Evaluate clear\_doctype\_notifications(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L881)

<a id="op-15923547dcacd7"></a>
### Delivery Note.update billing status

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_update_billing_status`

**Inputs** self, update\_modified = true.

**State and service calls** call db\_set on d.

**Local steps**

- Set updated\_delivery\_notes from list(self.name).
- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Evaluate updated\_delivery\_notes.append(self.return\_against).
- For each d in self.get(“items”).
  - If (d.si\_detail and not d.so\_detail).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.si\_detail → not d.so\_detail.
    - Evaluate d.db\_set(“billed\_amt”, d.amount, update\_modified = update\_modified).
  - Otherwise.
    - If d.so\_detail.
      - Update updated\_delivery\_notes using + update\_billed\_amount\_based\_on\_so(d.so\_detail, update\_modified).
- For each dn in set(updated\_delivery\_notes).
  - Set dn\_doc from self when dn equals self.name, otherwise Platform.get\_lazy\_doc(“Delivery Note”, dn).
    - Value choice on dn equals self.name — true gives self, false gives Platform.get\_lazy\_doc(“Delivery Note”, dn).
  - Set update\_dn\_modified from (update\_modified and dn differs from self.return\_against).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_modified → dn differs from self.return\_against.
  - Evaluate dn\_doc.update\_billing\_percentage(update\_modified = update\_dn\_modified).
- Evaluate self.load\_from\_db().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L879)

<a id="op-b68068ab2a0da9"></a>
### Delivery Note.make return invoice

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_deliverynote_make_return_invoice`

**Inputs** self.

**State and service calls** msgprint with translated “No Credit Note was created because the returned items were not invoiced” · call save on return\_invoice · call submit on return\_invoice · msgprint with translated “Credit Note {0} has been created automatically”.format(credit\_note\_link).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Could not create Credit Note automatically, please uncheck 'Issue Credit Note' and submit again”.

**Local steps**

- Set creditable\_qty from get\_creditable\_qty(self).
- If not any(creditable\_qty.values()).
  - Evaluate Platform.msgprint(translated “No Credit Note was created because the returned items were not invoiced”).
  - Return no value.
- Attempt the following.
  - Set return\_invoice from make\_sales\_invoice(self.name).
  - Set return\_invoice.is\_return from true.
  - Evaluate limit\_to\_creditable\_qty(return\_invoice, creditable\_qty).
  - Evaluate return\_invoice.save().
  - Evaluate return\_invoice.submit().
  - Set credit\_note\_link from Platform.utils.get\_link\_to\_form(“Sales Invoice”, return\_invoice.name).
  - Evaluate Platform.msgprint(translated “Credit Note {0} has been created automatically”.format(credit\_note\_link)).
- On failure (Exception).
  - Call the validation error handler Platform.throw(translated “Could not create Credit Note automatically, please uncheck 'Issue Credit Note' and submit again”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L216)

<a id="op-262334b948d07e"></a>
### Delivery Note.has unpacked items

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_has_unpacked_items`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- Set product\_bundle\_list from self.get\_product\_bundle\_list().
- For each item in (self.items + self.packed\_items).
  - If (item.item\_code does not belong to product\_bundle\_list and flt(item.packed\_qty) &lt; flt(item.qty)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code does not belong to product\_bundle\_list → flt(item.packed\_qty) &lt; flt(item.qty).
    - Return true.
- Return false.

**Methods declared on this owner** [get product bundle list](operations-007.md#op-543b81d309a620).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L873)

<a id="op-543b81d309a620"></a>
### Delivery Note.get product bundle list

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_deliverynote_get_product_bundle_list`

**Inputs** self.

**Record and data access** read “Product Bundle” via get\_all.

**Explicit results** Platform.db.get\_all(“Product Bundle”, filters = mapping(“new\_item\_code” → list(“in”, items\_list), “disabled” → 0), pluck = “name”).

**Local steps**

- Set items\_list from list of item.item\_code for item drawn from self.items.
  - Draw item from self.items.
- Return Platform.db.get\_all(“Product Bundle”, filters = mapping(“new\_item\_code” → list(“in”, items\_list), “disabled” → 0), pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L215)

<a id="op-56731611836b97"></a>
### Get creditable qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_creditable_qty`

**Inputs** return\_doc.

**Declared result** dict.

**Explicit results** mapping() · creditable\_qty.

**Local steps**

- Set original\_rows from get\_original\_rows(return\_doc).
- If not original\_rows.
  - Return mapping().
- Set available from get\_billed\_stock\_qty(set of row.name for row drawn from original\_rows).
  - Draw row from original\_rows.
- Evaluate apply\_earlier\_credits(available, original\_rows, return\_doc).
- Set creditable\_qty from mapping().
- Set rows from (list of d for d drawn from return\_doc.items where d.dn\_detail + list of d for d drawn from return\_doc.items where not d.dn\_detail).
  - Draw d from return\_doc.items, keep a combination only if (d.dn\_detail).
  - Draw d from return\_doc.items, keep a combination only if (not d.dn\_detail).
- For each row in rows.
  - Set sources from list(row.dn\_detail) when row.dn\_detail, otherwise list of d.name for d drawn from original\_rows where d.item\_code equals row.item\_code.
    - Value choice on row.dn\_detail — true gives list(row.dn\_detail), false gives list of d.name for d drawn from original\_rows where d.item\_code equals row.item\_code.
    - Draw d from original\_rows, keep a combination only if (d.item\_code equals row.item\_code).
  - Set factor from (flt(row.conversion\_factor) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.conversion\_factor) → 1.
  - Set needed from abs((flt(row.stock\_qty) or (flt(row.qty) × factor))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.stock\_qty) → (flt(row.qty) × factor).
  - Set creditable\_qty at row.name from flt((take\_credit(available, sources, needed) ÷ factor), 6).
- Return creditable\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L224)

<a id="op-9a808bf3ce5c9f"></a>
### Get original rows

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_original_rows`

**Inputs** return\_doc.

**Declared result** list.

**Record and data access** read “Delivery Note Item” via get\_all.

**Explicit results** sorted(rows.values(), key = deferred anonymous expression).

**Local steps**

- Set linked from set of d.dn\_detail for d drawn from return\_doc.items where d.dn\_detail.
  - Draw d from return\_doc.items, keep a combination only if (d.dn\_detail).
- Set item\_codes from set of d.item\_code for d drawn from return\_doc.items.
  - Draw d from return\_doc.items.
- Set rows from mapping().
- Set fields from list(“name”, “item\_code”, “idx”).
- If linked.
  - For each row in Platform.get\_all(“Delivery Note Item”, filters = mapping(“name” → tuple(“in”, list(linked))), fields = fields).
    - Set rows at row.name from row.
- If return\_doc.return\_against.
  - For each row in Platform.get\_all(“Delivery Note Item”, filters = mapping(“parent” → return\_doc.return\_against, “item\_code” → tuple(“in”, list(item\_codes))), fields = fields).
    - Set rows at row.name from row.
- Return sorted(rows.values(), key = deferred anonymous expression).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L227)

<a id="op-a15cd9dfec3a3b"></a>
### Take credit

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_take_credit`

**Inputs** available, sources, needed.

**Declared result** float.

**Explicit results** taken.

**Local steps**

- Set taken from 0.0.
- For each source in sources.
  - Set take from min((needed − taken), max(flt(available.get(source)), 0)).
  - Set available at source from (flt(available.get(source)) − take).
  - Update taken using + take.
- Return taken.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L255)

<a id="op-7cd386e914fcc1"></a>
### Apply earlier credits

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_apply_earlier_credits`

**Inputs** available, original\_rows, return\_doc.

**Declared result** no value.

**Local steps**

- Set earlier\_credits from get\_earlier\_credits(original\_rows, return\_doc).
- For each earlier in earlier\_credits.
  - If earlier.dn\_detail belongs to available.
    - Evaluate take\_credit(available, list(earlier.dn\_detail), earlier.stock\_qty).
- For each earlier in earlier\_credits.
  - If not earlier.dn\_detail.
    - Set sources from list of d.name for d drawn from original\_rows where d.item\_code equals earlier.item\_code.
      - Draw d from original\_rows, keep a combination only if (d.item\_code equals earlier.item\_code).
    - Evaluate take\_credit(available, sources, earlier.stock\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L212)

<a id="op-5b14398f626f75"></a>
### Get billed stock qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_billed_stock_qty`

**Inputs** original\_rows.

**Declared result** dict.

**Record and data access** read “Delivery Note Item” via get\_all.

**Explicit results** billed\_qty.

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set sii from Platform.qb.DocType(“Sales Invoice Item”).
- Set invoiced from mapping of row.dn\_detail → row for row drawn from nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(sii.dn\_detail).run(as\_dict = true).
  - Draw row from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- Set billed\_qty from mapping().
- For each row in Platform.get\_all(“Delivery Note Item”, filters = mapping(“name” → tuple(“in”, list(original\_rows))), fields = list(“name”, “billed\_amt”, “rate”, “qty”, …)).
  - Set factor from (flt(row.conversion\_factor) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.conversion\_factor) → 1.
  - Set billed\_qty at row.name from (get\_row\_billed\_qty(row, invoiced.get(row.name)) × factor).
- Return billed\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L221)

<a id="op-09ad90fa9fa8bb"></a>
### Get row billed qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_row_billed_qty`

**Inputs** row, invoiced.

**Declared result** float.

**Explicit results** direct\_qty when invoiced, otherwise flt(row.qty) · (direct\_qty + flt((order\_billed\_amount ÷ flt(row.rate)), 6)).

**Local steps**

- Set direct\_qty from (flt(invoiced.stock\_qty) ÷ (flt(row.conversion\_factor) or 1)) when invoiced, otherwise 0.0.
  - Value choice on invoiced — true gives (flt(invoiced.stock\_qty) ÷ (flt(row.conversion\_factor) or 1)), false gives 0.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.conversion\_factor) → 1.
- If not flt(row.rate).
  - Return direct\_qty when invoiced, otherwise flt(row.qty).
    - Value choice on invoiced — true gives direct\_qty, false gives flt(row.qty).
- Set direct\_amount from flt(invoiced.amount) when invoiced, otherwise 0.0.
  - Value choice on invoiced — true gives flt(invoiced.amount), false gives 0.0.
- Set order\_billed\_amount from max((flt(row.billed\_amt) − direct\_amount), 0.0).
- Return (direct\_qty + flt((order\_billed\_amount ÷ flt(row.rate)), 6)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L231)

<a id="op-48f7571b16d056"></a>
### Get earlier credits

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_earlier_credits`

**Inputs** original\_rows, return\_doc.

**Declared result** list.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….

**Local steps**

- Set dn from Platform.qb.DocType(“Delivery Note”).
- Set dni from Platform.qb.DocType(“Delivery Note Item”).
- Set sii from Platform.qb.DocType(“Sales Invoice Item”).
- Set condition from dni.dn\_detail.isin(list of row.name for row drawn from original\_rows).
  - Draw row from original\_rows.
- If return\_doc.return\_against.
  - Update condition using bitwise or dn.return\_against equals return\_doc.return\_against.
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L225)

<a id="op-acde97248e4cc8"></a>
### Limit to creditable qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_limit_to_creditable_qty`

**Inputs** return\_invoice, creditable\_qty.

**Declared result** no value.

**Local steps**

- Set rows from list().
- For each row in return\_invoice.items.
  - Set qty from flt(creditable\_qty.get(row.dn\_detail)).
  - If qty.
    - Set row.qty from negative min(abs(flt(row.qty)), qty).
    - Evaluate rows.append(row).
- Evaluate return\_invoice.set(“items”, rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L233)

<a id="op-a839c9ed21acd2"></a>
### Update billed amount based on so

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_update_billed_amount_based_on_so`

**Inputs** so\_detail, update\_modified = true.

**Record and data access** execute query text (SELECT, Sales Invoice Item).

**State and service calls** request set\_value on “Delivery Note Item”.

**Explicit results** updated\_dn.

**Local steps**

- Bind dependencies Sum.
- Set si from Platform.qb.DocType(“Sales Invoice”).as\_(“si”).
- Set si\_item from Platform.qb.DocType(“Sales Invoice Item”).as\_(“si\_item”).
- Set sum\_amount from Sum(si\_item.amount).as\_(“amount”).
- Set billed\_against\_so from nested operand in the contract(nested operand in the contract).select(sum\_amount).where((((nested operand in the contract equals nested operand in the contract bitwise and (nested operand in the contract b ….run().
- Set billed\_against\_so from ((billed\_against\_so and billed\_against\_so at 0 at 0) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (billed\_against\_so and billed\_against\_so at 0 at 0) → 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in billed\_against\_so → billed\_against\_so at 0 at 0.
- Set dn from Platform.qb.DocType(“Delivery Note”).as\_(“dn”).
- Set dn\_item from Platform.qb.DocType(“Delivery Note Item”).as\_(“dn\_item”).
- Set dn\_details from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise ….
- Set updated\_dn from list().
- For each dnd in dn\_details.
  - Set billed\_amt\_against\_dn from 0.
  - If dnd.si\_detail.
    - Set billed\_amt\_against\_dn from flt(dnd.amount).
    - Update billed\_against\_so using − billed\_amt\_against\_dn.
  - Otherwise.
    - Set billed\_amt\_against\_dn from Platform.db.sql(query text (SELECT, Sales Invoice Item), dnd.name).
    - Set billed\_amt\_against\_dn from ((billed\_amt\_against\_dn and billed\_amt\_against\_dn at 0 at 0) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (billed\_amt\_against\_dn and billed\_amt\_against\_dn at 0 at 0) → 0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in billed\_amt\_against\_dn → billed\_amt\_against\_dn at 0 at 0.
  - If (billed\_against\_so and billed\_amt\_against\_dn &lt; dnd.amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in billed\_against\_so → billed\_amt\_against\_dn &lt; dnd.amount.
    - Set pending\_to\_bill from (flt(dnd.amount) − billed\_amt\_against\_dn).
    - If pending\_to\_bill ≤ billed\_against\_so.
      - Update billed\_amt\_against\_dn using + pending\_to\_bill.
      - Update billed\_against\_so using − pending\_to\_bill.
    - Otherwise.
      - Update billed\_amt\_against\_dn using + billed\_against\_so.
      - Set billed\_against\_so from 0.
  - Evaluate Platform.db.set\_value(“Delivery Note Item”, dnd.name, “billed\_amt”, billed\_amt\_against\_dn, update\_modified = update\_modified).
  - Evaluate updated\_dn.append(dnd.parent).
- Return updated\_dn.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L256)
