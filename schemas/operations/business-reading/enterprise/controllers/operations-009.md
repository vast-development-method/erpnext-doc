# Shared transaction rules · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-67b780c17c78c8"></a>
### Validate child on delete

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_child_on_delete`

**Inputs** row, parent, ordered\_item = no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot delete item {1} which has already been delivered”.format(row.idx, row.item\_code) · validation helper — translated “Row #{0}: Cannot delete item {1} which has work order assigned to it.”.format(row.idx, row.item\_code) · validation helper — translated “Row #{0}: Cannot delete item {1} which is already ordered against this Sales Order.”.format(row.idx, row.item\_code) · validation helper — translated “Row #{0}: Cannot delete item {1} which has already been received”.format(row.idx, row.item\_code) · validation helper — translated “Row #{0}: Cannot delete item {1} which has already been billed.”.format(row.idx, row.item\_code) · 1 additional forms in the steps below.

**Local steps**

- If parent.doctype equals “Sales Order”.
  - If (flt(row.delivered\_qty) or flt(row.returned\_qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.delivered\_qty) → flt(row.returned\_qty).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which has already been delivered”.format(row.idx, row.item\_code)).
  - If flt(row.work\_order\_qty).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which has work order assigned to it.”.format(row.idx, row.item\_code)).
  - If flt(row.ordered\_qty).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which is already ordered against this Sales Order.”.format(row.idx, row.item\_code)).
- If (parent.doctype equals “Purchase Order” and (flt(row.received\_qty) or flt(row.returned\_qty))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.doctype equals “Purchase Order” → (flt(row.received\_qty) or flt(row.returned\_qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.received\_qty) → flt(row.returned\_qty).
  - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which has already been received”.format(row.idx, row.item\_code)).
- If parent.doctype belongs to list(“Purchase Order”, “Sales Order”).
  - If flt(row.billed\_amt).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which has already been billed.”.format(row.idx, row.item\_code)).
- If parent.doctype equals “Quotation”.
  - If ordered\_item.get(row.name).
    - Call the validation error handler Platform.throw(translated “Cannot delete an item which has been ordered”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1024) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L264)

<a id="op-d432059d269b0d"></a>
### Update bin on delete

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_bin_on_delete`

**Inputs** row, doctype.

**Local steps**

- Bind dependencies get\_indented\_qty, get\_ordered\_qty, get\_reserved\_qty, update\_bin\_qty.
- Set qty\_dict from mapping().
- If doctype equals “Sales Order”.
  - Set qty\_dict at “reserved\_qty” from get\_reserved\_qty(row.item\_code, row.warehouse).
- Otherwise.
  - If row.material\_request\_item.
    - Set qty\_dict at “indented\_qty” from get\_indented\_qty(row.item\_code, row.warehouse).
  - Set qty\_dict at “ordered\_qty” from get\_ordered\_qty(row.item\_code, row.warehouse).
- If row.warehouse.
  - Evaluate update\_bin\_qty(row.item\_code, row.warehouse, qty\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1006) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L246)

<a id="op-7fbe42cb9da0a6"></a>
### Validate blanket order changes

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_blanket_order_changes`

**Inputs** parent, data.

**Declared result** no value.

**Record and data access** resolve a document from “Blanket Order” via get\_doc.

**Explicit results** no value.

**Local steps**

- If parent.doctype does not belong to tuple(“Sales Order”, “Purchase Order”).
  - Return no value.
- Set new\_rows from mapping of d.get(“docname”) → d for d drawn from data where d.get(“docname”).
  - Draw d from data, keep a combination only if (d.get(“docname”)).
- Set precision from Platform.get\_precision((parent.doctype + “ Item”), “stock\_qty”).
- Set changes from defaultdict(float).
- For each row in parent.items.
  - If not (row.blanket\_order and row.against\_blanket\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.blanket\_order → row.against\_blanket\_order.
    - Continue with the next iteration or loop test.
  - Set new\_row from new\_rows.get(row.name).
  - If (new\_row and not new\_row.get(“item\_code”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_row → not new\_row.get(“item\_code”).
    - Continue with the next iteration or loop test.
  - Set new\_stock\_qty from 0.0.
  - If new\_row.
    - Set conversion\_factor from (flt(new\_row.get(“conversion\_factor”)) or flt(row.conversion\_factor) or 1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(new\_row.get(“conversion\_factor”)) → flt(row.conversion\_factor) → 1.
    - Set new\_stock\_qty from flt((flt(new\_row.get(“qty”)) × conversion\_factor), precision).
  - Update changes at tuple(row.blanket\_order, row.item\_code) using + (new\_stock\_qty − flt(row.stock\_qty)).
- For each tuple(tuple(blanket\_order, item\_code), change) in sorted(changes.items()).
  - If change &gt; 0.
    - Evaluate Platform.get\_doc(“Blanket Order”, blanket\_order, for\_update = true).validate\_qty\_can\_be\_ordered(mapping(item\_code → change), parent.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1023) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L263)

<a id="op-d162324d0d4b66"></a>
### Validate no issued proforma

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_no_issued_proforma`

**Inputs** rows.

**Declared result** no value.

**Record and data access** read “Proforma Invoice Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot delete item {1} which has an issued Proforma Invoice.”.format(row.idx, row.item\_code).

**Local steps**

- If not rows.
  - Return no value.
- Set proformed from set(Platform.get\_all(“Proforma Invoice Item”, filters = mapping(“so\_detail” → list(“in”, list of row.name for row drawn from rows), “docstatus” → 1), pluck = “so\_detail”)).
  - Draw row from rows.
- For each row in rows.
  - If row.name belongs to proformed.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which has an issued Proforma Invoice.”.format(row.idx, row.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1030) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L270)

<a id="op-6e76426a746b53"></a>
### Validate no linked order

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_no_linked_order`

**Inputs** rows, parent, linked\_doctype.

**Declared result** no value.

**Record and data access** read formatted text {linked\_doctype} Item via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot delete item {1} which is already ordered on {2} {3}.”.format(row.idx, row.item\_code, translated linked\_doctype, get\_link\_to\_form(linked\_doctype, linked\_order)).

**Local steps**

- If not rows.
  - Return no value.
- Set link\_field from Platform.scrub(parent.doctype).
- Set linked\_orders from dict(Platform.get\_all(formatted text {linked\_doctype} Item, filters = mapping(link\_field → parent.name, formatted text {link\_field}\_item → list(“in”, list of row.name for row drawn from rows), “docstatus” → lis …).
  - Draw row from rows.
- For each row in rows.
  - If linked\_order bound to linked\_orders.get(row.name).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which is already ordered on {2} {3}.”.format(row.idx, row.item\_code, translated linked\_doctype, get\_link\_to\_form(linked\_doctype, linked\_order))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1031) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L271)

<a id="op-a99d0213597c5b"></a>
### Validate no ordered packed item

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_no_ordered_packed_item`

**Inputs** rows, parent.

**Declared result** no value.

**Record and data access** read “Purchase Order Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot delete item {1} which is already ordered on {2} {3}.”.format(row.idx, row.item\_code, translated “Purchase Order”, get\_link\_to\_form(“Purchase Order”, purchase\_order)).

**Local steps**

- Set deleted\_rows from set of row.name for row drawn from rows.
  - Draw row from rows.
- Set row\_by\_packed\_item from mapping of packed.name → packed.parent\_detail\_docname for packed drawn from parent.get(“packed\_items”) where packed.parent\_detail\_docname belongs to deleted\_rows.
  - Draw packed from parent.get(“packed\_items”), keep a combination only if (packed.parent\_detail\_docname belongs to deleted\_rows).
- If not row\_by\_packed\_item.
  - Return no value.
- Set purchase\_orders from dict(Platform.get\_all(“Purchase Order Item”, filters = mapping(“sales\_order” → parent.name, “sales\_order\_packed\_item” → list(“in”, list(row\_by\_packed\_item)), “docstatus” → list(“&lt;”, 2)), fields = list(“sales\_or …).
- Set ordered\_rows from mapping of row\_by\_packed\_item at packed → order for tuple(packed, order) drawn from purchase\_orders.items().
  - Draw tuple(packed, order) from purchase\_orders.items().
- For each row in rows.
  - If purchase\_order bound to ordered\_rows.get(row.name).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot delete item {1} which is already ordered on {2} {3}.”.format(row.idx, row.item\_code, translated “Purchase Order”, get\_link\_to\_form(“Purchase Order”, purchase\_order))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1032) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L272)

<a id="op-681a6c16798ace"></a>
### Validate and delete children

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_and_delete_children`

**Inputs** parent, data, ordered\_item = no value, rows\_with\_kept\_reservation = no value.

**Declared result** bool.

**State and service calls** call cancel on d.

**Explicit results** bool(deleted\_children).

**Explicit failure paths** validation helper — translated “Row #{0}: Unreserve stock before deleting item {1}.”.format(row.idx, Platform.bold(row.item\_code)).

**Local steps**

- Set deleted\_children from list().
- Set updated\_item\_names from list of d.get(“docname”) for d drawn from data.
  - Draw d from data.
- For each item in parent.items.
  - If item.name does not belong to updated\_item\_names.
    - Evaluate deleted\_children.append(item).
- If deleted\_children.
  - If rows\_with\_kept\_reservation is identical to no value.
    - Set rows\_with\_kept\_reservation from get\_rows\_with\_kept\_reservation(parent).
  - For each row in deleted\_children.
    - If row.name belongs to rows\_with\_kept\_reservation.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Unreserve stock before deleting item {1}.”.format(row.idx, Platform.bold(row.item\_code)), title = translated “Stock Reserved”).
- If parent.doctype equals “Sales Order”.
  - Evaluate validate\_no\_issued\_proforma(deleted\_children).
  - Evaluate validate\_no\_linked\_order(deleted\_children, parent, “Purchase Order”).
  - Evaluate validate\_no\_ordered\_packed\_item(deleted\_children, parent).
- Otherwise.
  - If parent.doctype equals “Purchase Order”.
    - Evaluate validate\_no\_linked\_order(deleted\_children, parent, “Sales Order”).
- For each d in deleted\_children.
  - Evaluate validate\_child\_on\_delete(d, parent, ordered\_item).
  - Set d.flags.ignore\_permissions from true.
  - Evaluate d.cancel().
  - Evaluate d.delete().
- If (parent.doctype equals “Sales Order” and deleted\_children).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.doctype equals “Sales Order” → deleted\_children.
  - For each d in deleted\_children.
    - Evaluate parent.delete\_delivery\_schedule\_items(d.name).
- If parent.doctype equals “Purchase Order”.
  - Evaluate parent.update\_ordered\_qty\_in\_so\_for\_removed\_items(deleted\_children).
- Otherwise.
  - If parent.doctype equals “Sales Order”.
    - Evaluate parent.update\_ordered\_qty\_in\_quotation\_for\_removed\_items(deleted\_children).
- If parent.doctype does not belong to list(“Quotation”, “Supplier Quotation”).
  - Evaluate parent.update\_prevdoc\_status().
  - For each d in deleted\_children.
    - Evaluate update\_bin\_on\_delete(d, parent.doctype).
- Return bool(deleted\_children).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1022) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L262)

<a id="op-06cb077d2b9cc8"></a>
### Update child item uom and weight

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_item_uom_and_weight`

**Inputs** child\_item, new\_data.

**Declared result** no value.

**Local steps**

- If new\_data.get(“conversion\_factor”).
  - If child\_item.stock\_uom equals child\_item.uom.
    - Set child\_item.conversion\_factor from 1.
  - Otherwise.
    - Set child\_item.conversion\_factor from flt(new\_data.get(“conversion\_factor”)).
- If new\_data.get(“uom”).
  - Set child\_item.uom from new\_data.get(“uom”).
  - Set conversion\_factor from flt(get\_conversion\_factor(child\_item.item\_code, child\_item.uom).get(“conversion\_factor”)).
  - Set child\_item.conversion\_factor from (flt(new\_data.get(“conversion\_factor”)) or conversion\_factor).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(new\_data.get(“conversion\_factor”)) → conversion\_factor.
- If child\_item.get(“weight\_per\_unit”).
  - Set child\_item.total\_weight from flt(((child\_item.weight\_per\_unit × child\_item.qty) × child\_item.conversion\_factor), child\_item.precision(“total\_weight”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1007) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L247)

<a id="op-9a88c05467d53b"></a>
### Update child qty rate

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate`

**Inputs** parent\_doctype, trans\_items, parent\_doctype\_name, child\_docname = “items”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from parent\_doctype via get\_doc · resolve a document from (parent\_doctype + “ Item”) via get\_doc · resolve a document from “Authorization Control” via get\_cached\_doc.

**State and service calls** call insert on child\_item · call save on child\_item · call save on parent.

**Explicit failure paths** validation helper — translated “Rate of '{}' items cannot be changed”.format(Platform.bold(translated “Unit Price”)) · validation helper — translated “Row #{0}: Cannot set Rate if the billed amount is greater than the amount for Item {1}.”.format(child\_item.idx, child\_item.item\_code) · validation helper — translated “Items cannot be updated as Subcontracting Order is created against the Purchase Order {0}.”.format(Platform.bold(parent.name)) · validation helper — translated “Items cannot be updated as Subcontracting Inward Order(s) exist against this Subcontracted Sales Order.”.

**Local steps**

- Bind dependencies get\_ordered\_supplier\_quotation\_items.
- Bind dependencies get\_ordered\_items.
- Bind local operation check\_doc\_permissions for subsequent calls.
- Bind local operation validate\_parent\_status for subsequent calls.
- Bind local operation validate\_workflow\_conditions for subsequent calls.
- Bind local operation get\_new\_child\_item for subsequent calls.
- Bind local operation is\_allowed\_zero\_qty for subsequent calls.
- Bind local operation validate\_quantity\_and\_rate for subsequent calls.
- Bind local operation get\_new\_conversion\_factor for subsequent calls.
- Bind local operation validate\_uom\_unchanged\_after\_fulfilment for subsequent calls.
- Bind local operation should\_update\_supplied\_items for subsequent calls.
- Bind local operation validate\_fg\_item\_for\_subcontracting for subsequent calls.
- Set data from json.loads(trans\_items).
- Set any\_qty\_changed from false.
- Set items\_added\_or\_removed from false.
- Set any\_conversion\_factor\_changed from false.
- Set transacted\_stock\_qty from no value.
- Set parent from Platform.get\_doc(parent\_doctype, parent\_doctype\_name).
- Set had\_mapped\_discount from parent.has\_mapped\_discount.
- Set rfqs\_before\_update from set().
- Set blanket\_orders\_before\_update from set of d.blanket\_order for d drawn from parent.items where d.get(“blanket\_order”).
  - Draw d from parent.items, keep a combination only if (d.get(“blanket\_order”)).
- Evaluate check\_doc\_permissions(parent, “write”).
- Set rows\_with\_kept\_reservation from get\_rows\_with\_kept\_reservation(parent).
- Evaluate validate\_parent\_status(parent).
- Evaluate validate\_blanket\_order\_changes(parent, data).
- Set packed\_items\_before\_update from mapping().
- If parent\_doctype equals “Sales Order”.
  - Set packed\_items\_before\_update from get\_packed\_items\_of\_order\_rows(set of row.name for row drawn from parent.items).
    - Draw row from parent.items.
- If parent\_doctype equals “Quotation”.
  - Set transacted\_stock\_qty from get\_ordered\_items(parent.name).
  - Set \_removed\_items from validate\_and\_delete\_children(parent, data, transacted\_stock\_qty).
- Otherwise.
  - If parent\_doctype equals “Supplier Quotation”.
    - Set rfqs\_before\_update from parent.get\_request\_for\_quotations().
    - Set transacted\_stock\_qty from get\_ordered\_supplier\_quotation\_items(parent.name).
    - Set \_removed\_items from validate\_and\_delete\_children(parent, data, transacted\_stock\_qty).
  - Otherwise.
    - Set \_removed\_items from validate\_and\_delete\_children(parent, data, rows\_with\_kept\_reservation = rows\_with\_kept\_reservation).
- Update items\_added\_or\_removed using bitwise or \_removed\_items.
- For each d in data.
  - Set new\_child\_flag from false.
  - If not d.get(“item\_code”).
    - Continue with the next iteration or loop test.
  - If not d.get(“docname”).
    - Set new\_child\_flag from true.
    - Set items\_added\_or\_removed from true.
    - Evaluate check\_doc\_permissions(parent, “create”).
    - Set child\_item from get\_new\_child\_item(d).
  - Otherwise.
    - Evaluate check\_doc\_permissions(parent, “write”).
    - Set child\_item from Platform.get\_doc((parent\_doctype + “ Item”), d.get(“docname”)).
    - Set d at “conversion\_factor” from get\_new\_conversion\_factor(child\_item, d).
    - Set tuple(prev\_rate, new\_rate) from tuple(flt(child\_item.get(“rate”)), flt(d.get(“rate”))).
    - Set tuple(prev\_qty, new\_qty) from tuple(flt(child\_item.get(“qty”)), flt(d.get(“qty”))).
    - Set tuple(prev\_fg\_qty, new\_fg\_qty) from tuple(flt(child\_item.get(“fg\_item\_qty”)), flt(d.get(“fg\_item\_qty”))).
    - Set tuple(prev\_con\_fac, new\_con\_fac) from tuple(flt(child\_item.get(“conversion\_factor”)), flt(d.get(“conversion\_factor”))).
    - Set tuple(prev\_uom, new\_uom) from tuple(child\_item.get(“uom”), d.get(“uom”)).
    - If parent\_doctype equals “Sales Order”.
      - Set tuple(prev\_date, new\_date) from tuple(child\_item.get(“delivery\_date”), d.get(“delivery\_date”)).
    - Otherwise.
      - If parent\_doctype equals “Purchase Order”.
        - Set tuple(prev\_date, new\_date) from tuple(child\_item.get(“schedule\_date”), d.get(“schedule\_date”)).
    - Set tuple(prev\_description, new\_description) from tuple(child\_item.get(“description”), d.get(“description”)).
    - Set description\_unchanged from prev\_description equals new\_description.
    - Set rate\_unchanged from prev\_rate equals new\_rate.
    - Set qty\_unchanged from prev\_qty equals new\_qty.
    - Set fg\_qty\_unchanged from prev\_fg\_qty equals new\_fg\_qty.
    - Set uom\_unchanged from prev\_uom equals new\_uom.
    - Set conversion\_factor\_unchanged from prev\_con\_fac equals new\_con\_fac.
    - Update any\_conversion\_factor\_changed using bitwise or not conversion\_factor\_unchanged.
    - Set date\_unchanged from prev\_date equals getdate(new\_date) when (prev\_date and new\_date), otherwise false when parent\_doctype does not belong to list(“Quotation”, “Supplier Quotation”), otherwise no value.
      - Value choice on parent\_doctype does not belong to list(“Quotation”, “Supplier Quotation”) — true gives prev\_date equals getdate(new\_date) when (prev\_date and new\_date), otherwise false, false gives no value.
      - Value choice on (prev\_date and new\_date) — true gives prev\_date equals getdate(new\_date), false gives false.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in prev\_date → new\_date.
    - If (rate\_unchanged and qty\_unchanged and fg\_qty\_unchanged and conversion\_factor\_unchanged and uom\_unchanged and date\_unchanged and description\_unchanged).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in rate\_unchanged → qty\_unchanged → fg\_qty\_unchanged → conversion\_factor\_unchanged → uom\_unchanged → date\_unchanged → description\_unchanged.
      - Continue with the next iteration or loop test.
  - Evaluate validate\_quantity\_and\_rate(child\_item, d).
  - If not new\_child\_flag.
    - Evaluate validate\_uom\_unchanged\_after\_fulfilment(child\_item, d).
  - If flt(child\_item.get(“qty”)) differs from flt(d.get(“qty”)).
    - Set any\_qty\_changed from true.
  - If (parent.doctype belongs to list(“Sales Order”, “Purchase Order”) and parent.is\_subcontracted and not parent.get(“is\_old\_subcontracting\_flow”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.doctype belongs to list(“Sales Order”, “Purchase Order”) → parent.is\_subcontracted → not parent.get(“is\_old\_subcontracting\_flow”).
    - Evaluate validate\_fg\_item\_for\_subcontracting(d, new\_child\_flag).
    - Set child\_item.fg\_item\_qty from flt(d at “fg\_item\_qty”).
    - If new\_child\_flag.
      - Set child\_item.fg\_item from d at “fg\_item”.
  - Set child\_item.qty from flt(d.get(“qty”)).
  - Set child\_item.description from d.get(“description”).
  - Set rate\_precision from (child\_item.precision(“rate”) or 2).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_item.precision(“rate”) → 2.
  - Set qty\_precision from (child\_item.precision(“qty”) or 2).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_item.precision(“qty”) → 2.
  - Set tuple(prev\_rate, new\_rate) from tuple(flt(child\_item.get(“rate”)), flt(d.get(“rate”))).
  - Set rate\_unchanged from prev\_rate equals new\_rate.
  - If (not rate\_unchanged and not child\_item.get(“qty”) and is\_allowed\_zero\_qty()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not rate\_unchanged → not child\_item.get(“qty”) → is\_allowed\_zero\_qty().
    - Call the validation error handler Platform.throw(translated “Rate of '{}' items cannot be changed”.format(Platform.bold(translated “Unit Price”))).
  - Set row\_rate from flt(d.get(“rate”), rate\_precision).
  - If parent\_doctype belongs to list(“Purchase Order”, “Sales Order”).
    - Set amount\_below\_billed\_amt from flt(child\_item.billed\_amt, rate\_precision) &gt; flt((row\_rate × flt(d.get(“qty”), qty\_precision)), rate\_precision).
    - If (amount\_below\_billed\_amt and row\_rate &gt; 0.0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in amount\_below\_billed\_amt → row\_rate &gt; 0.0.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot set Rate if the billed amount is greater than the amount for Item {1}.”.format(child\_item.idx, child\_item.item\_code)).
    - Otherwise.
      - Set child\_item.rate from row\_rate.
  - Otherwise.
    - Set child\_item.rate from row\_rate.
  - Evaluate update\_child\_item\_uom\_and\_weight(child\_item, d).
  - If (d.get(“delivery\_date”) and parent\_doctype equals “Sales Order”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“delivery\_date”) → parent\_doctype equals “Sales Order”.
    - Set child\_item.delivery\_date from d.get(“delivery\_date”).
  - If (d.get(“schedule\_date”) and parent\_doctype equals “Purchase Order”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“schedule\_date”) → parent\_doctype equals “Purchase Order”.
    - Set child\_item.schedule\_date from d.get(“schedule\_date”).
  - If (d.get(“bom\_no”) and parent\_doctype equals “Sales Order”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“bom\_no”) → parent\_doctype equals “Sales Order”.
    - Set child\_item.bom\_no from d.get(“bom\_no”).
  - If flt(child\_item.price\_list\_rate).
    - If flt(child\_item.rate) &gt; flt(child\_item.price\_list\_rate).
      - Set child\_item.discount\_percentage from 0.
      - Set child\_item.discount\_amount from 0.
      - Set child\_item.margin\_type from “Amount”.
      - Set child\_item.margin\_rate\_or\_amount from flt((child\_item.rate − child\_item.price\_list\_rate), child\_item.precision(“margin\_rate\_or\_amount”)).
      - Set child\_item.rate\_with\_margin from child\_item.rate.
    - Otherwise.
      - Set child\_item.margin\_type from empty text.
      - Set child\_item.margin\_rate\_or\_amount from 0.
      - Set child\_item.rate\_with\_margin from child\_item.price\_list\_rate.
      - Set child\_item.discount\_percentage from 0.
      - Set child\_item.discount\_amount from (flt(child\_item.rate\_with\_margin) − flt(child\_item.rate)).
  - Set child\_item.flags.ignore\_validate\_update\_after\_submit from true.
  - If new\_child\_flag.
    - Evaluate parent.load\_from\_db().
    - Set child\_item.idx from (len(parent.items) + 1).
    - Evaluate child\_item.insert().
  - Otherwise.
    - Evaluate child\_item.save(ignore\_permissions = true).
    - If (parent\_doctype equals “Sales Order” and not (qty\_unchanged and uom\_unchanged and conversion\_factor\_unchanged)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_doctype equals “Sales Order” → not (qty\_unchanged and uom\_unchanged and conversion\_factor\_unchanged).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_unchanged → uom\_unchanged → conversion\_factor\_unchanged.
      - Evaluate parent.sync\_schedule\_with\_item(child\_item).
- Evaluate parent.reload().
- If had\_mapped\_discount.
  - Evaluate parent.clear\_stale\_mapped\_discount\_total().
- Set parent.flags.ignore\_validate\_update\_after\_submit from true.
- Evaluate parent.set\_qty\_as\_per\_stock\_uom().
- Evaluate parent.calculate\_taxes\_and\_totals().
- Evaluate parent.set\_total\_in\_words().
- Evaluate parent.validate\_party\_specific\_items().
- If (parent\_doctype equals “Sales Order” and not parent.is\_subcontracted).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_doctype equals “Sales Order” → not parent.is\_subcontracted.
  - Evaluate make\_packing\_list(parent, packed\_items\_before\_update).
  - Evaluate parent.set\_gross\_profit().
- Otherwise.
  - If parent\_doctype equals “Quotation”.
    - Evaluate make\_packing\_list(parent).
- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(parent.doctype, parent.company, parent.base\_grand\_total, parent).
- If parent\_doctype differs from “Supplier Quotation”.
  - Evaluate parent.set\_payment\_schedule().
- If parent\_doctype equals “Purchase Order”.
  - Evaluate parent.set\_last\_purchase\_rate().
  - Evaluate parent.validate\_minimum\_order\_qty().
  - Evaluate parent.validate\_budget().
  - If parent.is\_against\_so().
    - Evaluate parent.update\_status\_updater().
- Otherwise.
  - If parent\_doctype equals “Sales Order”.
    - Evaluate parent.check\_credit\_limit().
- For each tuple(idx, row) in enumerate(parent.get(child\_docname), start = 1).
  - Set row.idx from idx.
- Evaluate parent.save().
- If parent\_doctype equals “Purchase Order”.
  - Evaluate update\_last\_purchase\_rate(parent, is\_submit = 1).
  - If (any\_qty\_changed or items\_added\_or\_removed or any\_conversion\_factor\_changed).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in any\_qty\_changed → items\_added\_or\_removed → any\_conversion\_factor\_changed.
    - Evaluate parent.update\_prevdoc\_status().
  - Evaluate parent.update\_requested\_qty().
  - Evaluate parent.update\_ordered\_qty().
  - Evaluate parent.update\_ordered\_and\_reserved\_qty().
  - Evaluate parent.update\_receiving\_percentage().
  - If parent.is\_subcontracted.
    - If parent.is\_old\_subcontracting\_flow.
      - If should\_update\_supplied\_items(parent).
        - Evaluate parent.update\_reserved\_qty\_for\_subcontract().
        - Evaluate parent.create\_raw\_materials\_supplied\_or\_received().
      - Evaluate parent.save().
    - Otherwise.
      - If not parent.can\_update\_items().
        - Call the validation error handler Platform.throw(translated “Items cannot be updated as Subcontracting Order is created against the Purchase Order {0}.”.format(Platform.bold(parent.name))).
- Otherwise.
  - If parent\_doctype equals “Sales Order”.
    - If (parent.is\_subcontracted and not parent.can\_update\_items()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.is\_subcontracted → not parent.can\_update\_items().
      - Call the validation error handler Platform.throw(translated “Items cannot be updated as Subcontracting Inward Order(s) exist against this Subcontracted Sales Order.”).
    - Evaluate parent.validate\_selling\_price().
    - Evaluate parent.validate\_for\_duplicate\_items().
    - Evaluate parent.validate\_warehouse().
    - Evaluate parent.update\_reserved\_qty().
    - Evaluate parent.update\_project().
    - Evaluate parent.update\_prevdoc\_status(“submit”, update\_quotation\_qty = true).
    - Evaluate parent.update\_delivery\_status().
  - Otherwise.
    - If parent\_doctype equals “Supplier Quotation”.
      - Evaluate parent.update\_rfq\_supplier\_status(parent.docstatus.is\_submitted(), rfqs\_before\_update).
      - Evaluate parent.set\_status(update = true).
    - Otherwise.
      - If parent\_doctype equals “Quotation”.
        - Evaluate parent.set\_status(update = true).
- Evaluate parent.reload().
- Evaluate validate\_workflow\_conditions(parent).
- If parent\_doctype belongs to list(“Purchase Order”, “Sales Order”).
  - Evaluate parent.update\_blanket\_order(blanket\_orders\_before\_update).
  - Evaluate parent.update\_billing\_percentage().
  - Evaluate parent.set\_status().
- Evaluate parent.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate parent.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- If (parent\_doctype equals “Sales Order” and not parent.is\_subcontracted).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_doctype equals “Sales Order” → not parent.is\_subcontracted.
  - Bind dependencies cancel\_stock\_reservation\_entries, has\_reserved\_stock.
  - If (parent.per\_picked equals 0 and (any\_qty\_changed or any\_conversion\_factor\_changed or items\_added\_or\_removed) and has\_reserved\_stock(parent.doctype, parent.name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.per\_picked equals 0 → (any\_qty\_changed or any\_conversion\_factor\_changed or items\_added\_or\_removed) → has\_reserved\_stock(parent.doctype, parent.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in any\_qty\_changed → any\_conversion\_factor\_changed → items\_added\_or\_removed.
    - Evaluate cancel\_stock\_reservation\_entries(parent.doctype, parent.name).
    - Evaluate parent.\_create\_stock\_reservation\_entries().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1008) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L248)

<a id="op-bb2e568230acb1"></a>
### Update child qty rate.check doc permissions

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_check_doc_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, perm\_type.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L249)

<a id="op-7534e4d4b59808"></a>
### Update child qty rate.validate parent status

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_validate_parent_status`

**Inputs** doc.

**Explicit failure paths** validation helper — translated “Cannot update items of Purchase Order {0} because it is {1}.”.format(doc.name, translated doc.status) · validation helper — translated “Cannot update items of Supplier Quotation {0} because it is {1}.”.format(doc.name, translated doc.status) · validation helper — translated “Cannot update items of Quotation {0} because it is {1}.”.format(doc.name, translated doc.status) · validation helper — translated “Cannot update items of Quotation {0} because it has expired.”.format(doc.name).

**Local steps**

- If (doc.doctype equals “Purchase Order” and doc.status belongs to tuple(“Closed”, “On Hold”, “Delivered”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Purchase Order” → doc.status belongs to tuple(“Closed”, “On Hold”, “Delivered”).
  - Call the validation error handler Platform.throw(translated “Cannot update items of Purchase Order {0} because it is {1}.”.format(doc.name, translated doc.status)).
- If (doc.doctype equals “Supplier Quotation” and doc.status belongs to tuple(“Ordered”, “Stopped”, “Expired”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Supplier Quotation” → doc.status belongs to tuple(“Ordered”, “Stopped”, “Expired”).
  - Call the validation error handler Platform.throw(translated “Cannot update items of Supplier Quotation {0} because it is {1}.”.format(doc.name, translated doc.status)).
- If doc.doctype equals “Quotation”.
  - If doc.status belongs to tuple(“Lost”, “Ordered”).
    - Call the validation error handler Platform.throw(translated “Cannot update items of Quotation {0} because it is {1}.”.format(doc.name, translated doc.status)).
  - If (doc.valid\_till and getdate(doc.valid\_till) &lt; getdate()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.valid\_till → getdate(doc.valid\_till) &lt; getdate().
    - Call the validation error handler Platform.throw(translated “Cannot update items of Quotation {0} because it has expired.”.format(doc.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1015) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L255)

<a id="op-2fa2d3fcea976b"></a>
### Update child qty rate.validate workflow conditions

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_validate_workflow_conditions`

**Inputs** doc.

**Record and data access** resolve a document from “Workflow” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “You are not allowed to update as per the conditions set in {} Workflow.”.format(get\_link\_to\_form(“Workflow”, workflow)).

**Local steps**

- Set workflow from get\_workflow\_name(doc.doctype).
- If not workflow.
  - Return no value.
- Set workflow\_doc from Platform.get\_doc(“Workflow”, workflow).
- Set current\_state from doc.get(workflow\_doc.workflow\_state\_field).
- Set roles from Platform.get\_roles().
- Set allowed from any(generator of (state.state equals current\_state and (not state.allow\_edit or state.allow\_edit belongs to roles)) for state drawn from workflow\_doc.states).
  - Draw state from workflow\_doc.states.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in state.state equals current\_state → (not state.allow\_edit or state.allow\_edit belongs to roles).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not state.allow\_edit → state.allow\_edit belongs to roles.
- If not allowed.
  - Call the validation error handler Platform.throw(translated “You are not allowed to update as per the conditions set in {} Workflow.”.format(get\_link\_to\_form(“Workflow”, workflow)), title = translated “Insufficient Permissions”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1018) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L258)

<a id="op-2688601fd0dfd3"></a>
### Update child qty rate.get new child item

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_get_new_child_item`

**Inputs** item\_row.

**Explicit results** set\_order\_defaults(parent\_doctype, parent\_doctype\_name, child\_doctype, child\_docname, …).

**Local steps**

- Set child\_doctype from (parent\_doctype + “ Item”).
- Return set\_order\_defaults(parent\_doctype, parent\_doctype\_name, child\_doctype, child\_docname, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L250)

<a id="op-d2844c1d98cce0"></a>
### Update child qty rate.is allowed zero qty

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_is_allowed_zero_qty`

**Inputs** no declared parameters.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Buying Settings” via get\_single\_value.

**Explicit results** (Platform.db.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_sales\_order”) or false) · (Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_purchase\_order”) or false) · false.

**Local steps**

- If parent\_doctype equals “Sales Order”.
  - Return (Platform.db.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_sales\_order”) or false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_sales\_order”) → false.
- Otherwise.
  - If parent\_doctype equals “Purchase Order”.
    - Return (Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_purchase\_order”) or false).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_purchase\_order”) → false.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_sales\_order”), Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_purchase\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1012) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L252)

<a id="op-53e26ac45f7281"></a>
### Update child qty rate.validate quantity and rate

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_validate_quantity_and_rate`

**Inputs** child\_item, new\_data.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}:Quantity for Item {1} cannot be zero.”.format(new\_data.get(“idx”), Platform.bold(new\_data.get(“item\_code”))) · validation helper — (translated “Row #{0}:”.format(new\_data.get(“idx”)) + error\_message.format(Platform.bold(new\_data.get(“item\_code”)))) · validation helper — translated “Row #{0}: Cannot set quantity less than delivered and reserved quantity. Unreserve stock before reducing the …”.format((new\_data.get(“idx”) or child\_item.idx)) · validation helper — translated “Cannot update rate as item {0} is already ordered or purchased against this quotation”.format(Platform.bold(new\_data.get(“item\_code”))) · validation helper — translated “Cannot reduce quantity than ordered or purchased quantity”.

**Local steps**

- If (not flt(new\_data.get(“qty”)) and not is\_allowed\_zero\_qty()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(new\_data.get(“qty”)) → not is\_allowed\_zero\_qty().
  - Call the validation error handler Platform.throw(translated “Row #{0}:Quantity for Item {1} cannot be zero.”.format(new\_data.get(“idx”), Platform.bold(new\_data.get(“item\_code”))), title = translated “Invalid Qty”).
- Set qty\_limits from mapping(“Sales Order” → tuple(“delivered\_qty”, translated “Cannot set quantity less than delivered quantity.”), “Purchase Order” → tuple(“received\_qty”, translated “Cannot set quantity less than received q ….
- Set old\_conversion\_factor from (flt(child\_item.get(“conversion\_factor”)) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(child\_item.get(“conversion\_factor”)) → 1.
- Set new\_conversion\_factor from (flt(new\_data.get(“conversion\_factor”)) or old\_conversion\_factor).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(new\_data.get(“conversion\_factor”)) → old\_conversion\_factor.
- Set new\_stock\_qty from (flt(new\_data.get(“qty”)) × new\_conversion\_factor).
- If parent\_doctype belongs to qty\_limits.
  - Set tuple(qty\_field, error\_message) from qty\_limits at parent\_doctype.
  - Set old\_stock\_qty from (flt(child\_item.get(qty\_field)) × old\_conversion\_factor).
  - If new\_stock\_qty &lt; old\_stock\_qty.
    - Call the validation error handler Platform.throw((translated “Row #{0}:”.format(new\_data.get(“idx”)) + error\_message.format(Platform.bold(new\_data.get(“item\_code”)))), title = translated “Invalid Qty”).
- If child\_item.name belongs to rows\_with\_kept\_reservation.
  - Set min\_stock\_qty from ((flt(child\_item.delivered\_qty) × flt(child\_item.conversion\_factor)) + flt(child\_item.stock\_reserved\_qty)).
  - If not flt(child\_item.stock\_reserved\_qty).
    - Set min\_stock\_qty from flt(child\_item.stock\_qty).
  - If flt((new\_stock\_qty − min\_stock\_qty), child\_item.precision(“stock\_qty”)) &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot set quantity less than delivered and reserved quantity. Unreserve stock before reducing the …”.format((new\_data.get(“idx”) or child\_item.idx)), title = translate ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_data.get(“idx”) → child\_item.idx.
- If not transacted\_stock\_qty.
  - Return no value.
- Set old\_stock\_qty from transacted\_stock\_qty.get(child\_item.name).
- If not old\_stock\_qty.
  - Return no value.
- If not rate\_unchanged.
  - Call the validation error handler Platform.throw(translated “Cannot update rate as item {0} is already ordered or purchased against this quotation”.format(Platform.bold(new\_data.get(“item\_code”)))).
- If new\_stock\_qty &lt; old\_stock\_qty.
  - Call the validation error handler Platform.throw(translated “Cannot reduce quantity than ordered or purchased quantity”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1016) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L256)

<a id="op-b18993e5d8c7f4"></a>
### Update child qty rate.get new conversion factor

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_get_new_conversion_factor`

**Inputs** child\_item, new\_data.

**Explicit results** 1 · requested\_factor · current\_factor · (flt(get\_conversion\_factor(child\_item.item\_code, uom).get(“conversion\_factor”)) or 1).

**Local steps**

- Set current\_factor from (flt(child\_item.get(“conversion\_factor”)) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(child\_item.get(“conversion\_factor”)) → 1.
- Set uom from (new\_data.get(“uom”) or child\_item.get(“uom”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_data.get(“uom”) → child\_item.get(“uom”).
- If uom equals child\_item.get(“stock\_uom”).
  - Return 1.
- Set requested\_factor from flt(new\_data.get(“conversion\_factor”)).
- If requested\_factor.
  - Return requested\_factor.
- If uom equals child\_item.get(“uom”).
  - Return current\_factor.
- Return (flt(get\_conversion\_factor(child\_item.item\_code, uom).get(“conversion\_factor”)) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(get\_conversion\_factor(child\_item.item\_code, uom).get(“conversion\_factor”)) → 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L251)

<a id="op-d64809291fef8a"></a>
### Update child qty rate.validate uom unchanged after fulfilment

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_validate_uom_unchanged_after_fulfilment`

**Inputs** child\_item, new\_data.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Unreserve stock before changing the UOM or conversion factor of Item {1}.”.format((new\_data.get(“idx”) or child\_item.idx), Platform.bold(child\_item.item\_code)) · validation helper — translated “Row #{0}: Cannot change the UOM or conversion factor of Item {1} after part of it was received or delivered.”.format((new\_data.get(“idx”) or child\_item.idx), Platform.bold(child\_item.item\_code)).

**Local steps**

- Set uom\_changed from new\_data.get(“uom”) does not belong to tuple(no value, child\_item.uom).
- Set factor\_changed from flt(new\_data.get(“conversion\_factor”)) does not belong to tuple(0, flt(child\_item.conversion\_factor)).
- If (not uom\_changed and not factor\_changed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not uom\_changed → not factor\_changed.
  - Return no value.
- If child\_item.name belongs to rows\_with\_kept\_reservation.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Unreserve stock before changing the UOM or conversion factor of Item {1}.”.format((new\_data.get(“idx”) or child\_item.idx), Platform.bold(child\_item.item\_code)), title = ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_data.get(“idx”) → child\_item.idx.
- Set fulfilled\_qty\_field from mapping(“Sales Order” → “delivered\_qty”, “Purchase Order” → “received\_qty”).get(parent\_doctype).
- If (not fulfilled\_qty\_field or not flt(child\_item.get(fulfilled\_qty\_field))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fulfilled\_qty\_field → not flt(child\_item.get(fulfilled\_qty\_field)).
  - Return no value.
- Call the validation error handler Platform.throw(translated “Row #{0}: Cannot change the UOM or conversion factor of Item {1} after part of it was received or delivered.”.format((new\_data.get(“idx”) or child\_item.idx), Platform.bold(child\_ ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_data.get(“idx”) → child\_item.idx.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1017) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L257)

<a id="op-8528b5602be4b1"></a>
### Update child qty rate.should update supplied items

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_should_update_supplied_items`

**Inputs** doc.

**Declared result** bool.

**Explicit results** update\_supplied\_items.

**Explicit failure paths** validation helper — translated “Item qty can not be updated as raw materials are already processed.”.

**Local steps**

- Set supplied\_items\_processed from any(generator of (item.supplied\_qty or item.consumed\_qty or item.returned\_qty) for item drawn from doc.supplied\_items).
  - Draw item from doc.supplied\_items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.supplied\_qty → item.consumed\_qty → item.returned\_qty.
- Set update\_supplied\_items from (any\_qty\_changed or items\_added\_or\_removed or any\_conversion\_factor\_changed).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in any\_qty\_changed → items\_added\_or\_removed → any\_conversion\_factor\_changed.
- If (update\_supplied\_items and supplied\_items\_processed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_supplied\_items → supplied\_items\_processed.
  - Call the validation error handler Platform.throw(translated “Item qty can not be updated as raw materials are already processed.”).
- Return update\_supplied\_items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1013) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L253)

<a id="op-6aeb47e29a93e4"></a>
### Update child qty rate.validate fg item for subcontracting

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_child_qty_rate_validate_fg_item_for_subcontracting`

**Inputs** new\_data, is\_new.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Finished Good Item is not specified for service item {0}”.format(new\_data at “item\_code”) · validation helper — translated “Finished Good Item {0} must be a sub-contracted item”.format(new\_data at “fg\_item”) · validation helper — translated “Default BOM not found for FG Item {0}”.format(new\_data at “fg\_item”) · validation helper — translated “Finished Good Item {0} Qty can not be zero”.format(new\_data at “fg\_item”).

**Local steps**

- If is\_new.
  - If not new\_data.get(“fg\_item”).
    - Call the validation error handler Platform.throw(translated “Finished Good Item is not specified for service item {0}”.format(new\_data at “item\_code”)).
  - Otherwise.
    - If not Platform.db.get\_value(“Item”, new\_data at “fg\_item”, “is\_sub\_contracted\_item”).
      - Call the validation error handler Platform.throw(translated “Finished Good Item {0} must be a sub-contracted item”.format(new\_data at “fg\_item”)).
    - Otherwise.
      - If not get\_default\_bom(new\_data at “fg\_item”).
        - Call the validation error handler Platform.throw(translated “Default BOM not found for FG Item {0}”.format(new\_data at “fg\_item”)).
- If not new\_data.get(“fg\_item\_qty”).
  - Call the validation error handler Platform.throw(translated “Finished Good Item {0} Qty can not be zero”.format(new\_data at “fg\_item”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1014) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L254)

<a id="op-6c9097952f3b72"></a>
### Check if child table updated

`operation_enterprise_binding_enterprise_controllers_accounts_controller_check_if_child_table_updated`

**Inputs** child\_table\_before\_update, child\_table\_after\_update, fields\_to\_check.

**Explicit results** true · false.

**Local steps**

- Set fields\_to\_check from ((list(fields\_to\_check) + get\_accounting\_dimensions()) + list(“cost\_center”, “project”)).
- For each tuple(index, item) in enumerate(child\_table\_before\_update).
  - For each field in fields\_to\_check.
    - If child\_table\_after\_update at index.get(field) differs from item.get(field).
      - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L980) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L220)

<a id="op-851fb0d9f7774f"></a>
### Merge taxes

`operation_enterprise_binding_enterprise_controllers_accounts_controller_merge_taxes`

**Inputs** source\_doc, target\_doc.

**Local steps**

- Set tax\_map from mapping().
- For each tax in (source\_doc.get(“taxes”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_doc.get(“taxes”) → list().
  - Set found from false.
  - For each t in (target\_doc.get(“taxes”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in target\_doc.get(“taxes”) → list().
    - If (t.account\_head equals tax.account\_head and t.cost\_center equals tax.cost\_center).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in t.account\_head equals tax.account\_head → t.cost\_center equals tax.cost\_center.
      - Set t.tax\_amount from (flt(t.tax\_amount) + flt(tax.tax\_amount\_after\_discount\_amount)).
      - Set t.base\_tax\_amount from (flt(t.base\_tax\_amount) + flt(tax.base\_tax\_amount\_after\_discount\_amount)).
      - Set tax\_map at tax.name from t.
      - Set found from true.
  - If not found.
    - Set tax.charge\_type from “Actual”.
    - Set tax.included\_in\_print\_rate from 0.
    - Set tax.dont\_recompute\_tax from 1.
    - Set tax.row\_id from no value.
    - Set tax.idx from no value.
    - Set tax.tax\_amount from tax.tax\_amount\_after\_discount\_amount.
    - Set tax.base\_tax\_amount from tax.base\_tax\_amount\_after\_discount\_amount.
    - Set tax\_map at tax.name from target\_doc.append(“taxes”, tax).
- Set item\_map from mapping of d.\_old\_name → d for d drawn from target\_doc.get(“items”) where d.get(“\_old\_name”).
  - Draw d from target\_doc.get(“items”), keep a combination only if (d.get(“\_old\_name”)).
- Set item\_tax\_details from (target\_doc.get(“\_item\_wise\_tax\_details”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target\_doc.get(“\_item\_wise\_tax\_details”) → list().
- For each row in source\_doc.get(“item\_wise\_tax\_details”).
  - Set item from item\_map.get(row.item\_row).
  - Set tax from tax\_map.get(row.tax\_row).
  - If not (item and tax).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → tax.
    - Continue with the next iteration or loop test.
  - Evaluate item\_tax\_details.append(Platform.\_dict(item = item, tax = tax, amount = row.amount, rate = row.rate, …)).
- Set target\_doc.\_item\_wise\_tax\_details from item\_tax\_details.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1000) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L240)

<a id="op-0f1ad53a7f3ee4"></a>
### Validate regional

`operation_enterprise_controllers_accounts_controller_business_behavior_validate_regional`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0369.json#L4056) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L382)

<a id="op-17ce2cfab73aa1"></a>
### Validate einvoice fields

`operation_enterprise_controllers_accounts_controller_business_behavior_validate_einvoice_fields`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0369.json#L4098) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L381)

<a id="op-a20421f2a8a3c0"></a>
### Update gl dict with regional fields

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_gl_dict_with_regional_fields`

**Inputs** doc, gl\_dict.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1020) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L260)
