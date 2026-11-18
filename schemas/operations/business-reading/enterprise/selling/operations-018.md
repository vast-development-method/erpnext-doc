# Sales · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales order

[Record definition](../../../../data/record-types/sales_order.json)

<a id="op-862b4565e7dbdd"></a>
### Make delivery note.set missing values

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note_set_missing_values`

**Inputs** source, target.

**Local steps**

- If kwargs.get(“ignore\_pricing\_rule”).
  - Set target.ignore\_pricing\_rule from 1.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“set\_po\_nos”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).
- Evaluate target.run\_method(“set\_use\_serial\_batch\_fields”).
- If source.company\_address.
  - Evaluate target.update(mapping(“company\_address” → source.company\_address)).
- Otherwise.
  - Evaluate target.update(get\_company\_address(target.company)).
- If target.company\_address.
  - Evaluate target.update(get\_fetch\_values(“Delivery Note”, “company\_address”, target.company\_address)).
- If Platform.flags.bulk\_transaction.
  - Evaluate target.set\_new\_name().
- Evaluate make\_packing\_list(target).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“set\_po\_nos”) and 2 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L39)

<a id="op-b2683d7c5acd4b"></a>
### Make delivery note.condition

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note_condition`

**Inputs** doc.

**Explicit results** false · (((abs(doc.delivered\_qty) + abs(nested operand in the contract.get(nested operand in the contract.name, 0))) &lt; abs(doc.qty) or (is\_unit\_price\_row(doc) and doc.name does not belong to mapped\_qty\_by\_item)) a ….

**Local steps**

- If doc.name belongs to sre\_details.
  - Remove sre\_details at doc.name.
  - Return false.
- If (Platform.flags.args and Platform.flags.args.delivery\_dates).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.args → Platform.flags.args.delivery\_dates.
  - If cstr(doc.delivery\_date) does not belong to Platform.flags.args.delivery\_dates.
    - Return false.
- If (Platform.flags.args and Platform.flags.args.until\_delivery\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.args → Platform.flags.args.until\_delivery\_date.
  - If cstr(doc.delivery\_date) &gt; Platform.flags.args.until\_delivery\_date.
    - Return false.
- Return (((abs(doc.delivered\_qty) + abs(nested operand in the contract.get(nested operand in the contract.name, 0))) &lt; abs(doc.qty) or (is\_unit\_price\_row(doc) and doc.name does not belong to mapped\_qty\_by\_item)) a ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ((abs(doc.delivered\_qty) + abs(mapped\_qty\_by\_item.get(doc.name, 0))) &lt; abs(doc.qty) or (is\_unit\_price\_row(doc) and doc.name does not belong to mapped\_qty\_by\_item)) → doc.delivered\_by\_supplier differs from 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (abs(doc.delivered\_qty) + abs(mapped\_qty\_by\_item.get(doc.name, 0))) &lt; abs(doc.qty) → (is\_unit\_price\_row(doc) and doc.name does not belong to mapped\_qty\_by\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_unit\_price\_row(doc) → doc.name does not belong to mapped\_qty\_by\_item.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L35)

<a id="op-12cf5a205bb58c"></a>
### Make delivery note.remaining qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note_remaining_qty`

**Inputs** source.

**Explicit results** ((flt(source.qty) − flt(source.delivered\_qty)) − flt(mapped\_qty\_by\_item.get(source.name, 0))).

**Local steps**

- Return ((flt(source.qty) − flt(source.delivered\_qty)) − flt(mapped\_qty\_by\_item.get(source.name, 0))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L37)

<a id="op-d41510ee1d229d"></a>
### Make delivery note.update item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note_update_item`

**Inputs** source, target, source\_parent.

**Record and data access** read “Project” via get\_value.

**Local steps**

- Set target.base\_amount from (remaining\_qty(source) × flt(source.base\_rate)).
- Set target.amount from (remaining\_qty(source) × flt(source.rate)).
- Set target.qty from flt(source.qty) when is\_unit\_price\_row(source), otherwise remaining\_qty(source).
  - Value choice on is\_unit\_price\_row(source) — true gives flt(source.qty), false gives remaining\_qty(source).
- Set item from get\_item\_defaults(target.item\_code, source\_parent.company).
- Set item\_group from get\_item\_group\_defaults(target.item\_code, source\_parent.company).
- If item.
  - Set target.cost\_center from (Platform.db.get\_value(“Project”, source\_parent.project, “cost\_center”) or item.get(“buying\_cost\_center”) or item\_group.get(“buying\_cost\_center”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Project”, source\_parent.project, “cost\_center”) → item.get(“buying\_cost\_center”) → item\_group.get(“buying\_cost\_center”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L41)

<a id="op-518c790eaf58d6"></a>
### Make delivery note.update dn item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note_update_dn_item`

**Inputs** source, target, source\_parent.

**Local steps**

- Evaluate update\_item(source, target, so).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L40)

<a id="op-c054db18817196"></a>
### Get qty net of returns

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_qty_net_of_returns`

**Inputs** so\_item, credit\_note\_returned\_qty = 0.

**Declared result** float.

**Explicit results** min(qty, max((qty − returned\_qty), flt(so\_item.delivered\_qty))).

**Local steps**

- Set qty from flt(so\_item.qty).
- Set returned\_qty from (flt(so\_item.returned\_qty) − flt(credit\_note\_returned\_qty)).
- Return min(qty, max((qty − returned\_qty), flt(so\_item.delivered\_qty))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L29)

<a id="op-7be792b98dd4b2"></a>
### Make sales invoice

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice`

**Inputs** source\_name, target\_doc = no value, args = no value, ignore\_permissions = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Order” via get\_value · read “Sales Order” via get\_cached\_value · read “Accounts Settings” via get\_single\_value.

**Explicit results** doclist.

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set has\_unit\_price\_items from Platform.db.get\_value(“Sales Order”, source\_name, “has\_unit\_price\_items”).
- Set invoiced\_qty\_by\_item from no value.
- Set pending\_qty\_by\_item from mapping().
- Set amount\_allowance\_by\_item from mapping().
- Set mapped\_qty\_by\_item from get\_qty\_already\_mapped(target\_doc, “so\_detail”).
- Bind local operation is\_unit\_price\_row for subsequent calls.
- Bind local operation is\_amount\_billable for subsequent calls.
- Bind local operation get\_invoiced\_qty\_by\_item for subsequent calls.
- Bind local operation get\_pending\_qty for subsequent calls.
- Bind local operation is\_qty\_billed\_below\_amount for subsequent calls.
- Bind local operation postprocess for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Bind local operation add\_self\_rm for subsequent calls.
- Set doclist from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Sales Invoice”, “field\_map” → mapping(“party\_account\_currency” → “party\_account\_currency”), “field\_no\_map” → list(“pa ….
- If Platform.get\_cached\_value(“Sales Order”, source\_name, “is\_subcontracted”).
  - Evaluate add\_self\_rm(doclist).
- Set automatically\_fetch\_payment\_terms from cint(Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”)).
- If automatically\_fetch\_payment\_terms.
  - Evaluate doclist.set\_payment\_schedule().
- Return doclist.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Sales Order”, source\_name, “is\_subcontracted”), Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L59)

<a id="op-bb098c158d88dc"></a>
### Make sales invoice.is unit price row

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_is_unit_price_row`

**Inputs** source.

**Explicit results** (has\_unit\_price\_items and source.qty equals 0).

**Local steps**

- Return (has\_unit\_price\_items and source.qty equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_unit\_price\_items → source.qty equals 0.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L65)

<a id="op-1d46f6f700e7c8"></a>
### Make sales invoice.is amount billable

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_is_amount_billable`

**Inputs** source.

**Explicit results** abs(flt(source.billed\_amt)) &lt; (abs(flt(source.amount)) × (1 + (allowance ÷ 100))).

**Local steps**

- Bind dependencies get\_allowance\_for.
- If source.item\_code does not belong to amount\_allowance\_by\_item.
  - Set amount\_allowance\_by\_item at source.item\_code from flt(get\_allowance\_for(source.item\_code, qty\_or\_amount = “amount”) at 0).
- Set allowance from amount\_allowance\_by\_item at source.item\_code.
- Return abs(flt(source.billed\_amt)) &lt; (abs(flt(source.amount)) × (1 + (allowance ÷ 100))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L566) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L63)

<a id="op-1df9c6cc3c2bbf"></a>
### Make sales invoice.get invoiced qty by item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_get_invoiced_qty_by_item`

**Inputs** no declared parameters.

**Explicit results** invoiced\_qty\_by\_item.

**Local steps**

- Use enclosing bindings invoiced\_qty\_by\_item.
- If invoiced\_qty\_by\_item is identical to no value.
  - Set invoice from Platform.qb.DocType(“Sales Invoice”).
  - Set invoice\_item from Platform.qb.DocType(“Sales Invoice Item”).
  - Set sales\_order\_item from Platform.qb.DocType(“Sales Order Item”).
  - Set qty\_in\_stock\_uom from (invoice\_item.qty × invoice\_item.conversion\_factor).
  - Set credit\_note\_qty from Case().when(get\_credit\_note\_return\_criterion(invoice), negative qty\_in\_stock\_uom).else\_(0).
  - Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….
  - Set invoiced\_qty\_by\_item from mapping of row.so\_detail → row for row drawn from rows.
    - Draw row from rows.
- Return invoiced\_qty\_by\_item.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L61)

<a id="op-b49266ecbdcb3f"></a>
### Make sales invoice.get pending qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_get_pending_qty`

**Inputs** source.

**Explicit results** pending\_qty\_by\_item at source.name.

**Local steps**

- If source.name does not belong to pending\_qty\_by\_item.
  - Set invoiced from get\_invoiced\_qty\_by\_item().get(source.name, Platform.\_dict()).
  - Set billable\_qty from get\_qty\_net\_of\_returns(source, invoiced.credit\_note\_returned\_qty).
  - Update billable\_qty using − flt(invoiced.billed\_qty).
  - Update billable\_qty using − mapped\_qty\_by\_item.get(source.name, 0).
  - Set pending\_qty\_by\_item at source.name from max(flt(billable\_qty, source.precision(“qty”)), 0).
- Return pending\_qty\_by\_item at source.name.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L62)

<a id="op-66af9dccecd416"></a>
### Make sales invoice.is qty billed below amount

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_is_qty_billed_below_amount`

**Inputs** source.

**Explicit results** (source.name does not belong to mapped\_qty\_by\_item and flt((flt(source.qty) − flt(invoiced.billed\_qty)), source.precision(“qty”)) ≤ 0 and abs(flt(source.billed\_amt)) &lt; abs(flt(source.amount))).

**Local steps**

- Set invoiced from get\_invoiced\_qty\_by\_item().get(source.name, Platform.\_dict()).
- Return (source.name does not belong to mapped\_qty\_by\_item and flt((flt(source.qty) − flt(invoiced.billed\_qty)), source.precision(“qty”)) ≤ 0 and abs(flt(source.billed\_amt)) &lt; abs(flt(source.amount))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source.name does not belong to mapped\_qty\_by\_item → flt((flt(source.qty) − flt(invoiced.billed\_qty)), source.precision(“qty”)) ≤ 0 → abs(flt(source.billed\_amt)) &lt; abs(flt(source.amount)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L567) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L64)

<a id="op-eb362200a5d159"></a>
### Make sales invoice.postprocess

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_postprocess`

**Inputs** source, target.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- Evaluate set\_missing\_values(source, target).
- If target.get(“allocate\_advances\_automatically”).
  - Evaluate target.set\_advances().
- Evaluate make\_packing\_list(target).
- Evaluate set\_serial\_batch\_for\_bundle\_reservation(target, Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”), get\_sre\_details\_for\_voucher(“Sales Order”, source\_name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L66)

<a id="op-09f4918400c680"></a>
### Make sales invoice.set missing values

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.flags.ignore\_permissions from ignore\_permissions.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“set\_po\_nos”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).
- Evaluate target.run\_method(“set\_use\_serial\_batch\_fields”).
- If source.company\_address.
  - Evaluate target.update(mapping(“company\_address” → source.company\_address)).
- Otherwise.
  - Evaluate target.update(get\_company\_address(target.company)).
- If target.company\_address.
  - Evaluate target.update(get\_fetch\_values(“Sales Invoice”, “company\_address”, target.company\_address)).
- If (source.loyalty\_points and source.order\_type equals “Shopping Cart”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source.loyalty\_points → source.order\_type equals “Shopping Cart”.
  - Set target.redeem\_loyalty\_points from 1.
  - Set target.loyalty\_points from source.loyalty\_points.
- Set target.debit\_to from get\_party\_account(“Customer”, source.customer, source.company).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“set\_po\_nos”) and 2 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L68)

<a id="op-f4b97566688fd0"></a>
### Make sales invoice.update item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_update_item`

**Inputs** source, target, source\_parent.

**Record and data access** read “Project” via get\_value · read “Item” via get\_cached\_value.

**Local steps**

- If source\_parent.has\_unit\_price\_items.
  - Set pending\_amount from (flt(source.amount) − flt(source.billed\_amt)).
  - Set target.amount from pending\_amount when flt(source.amount), otherwise 0.
    - Value choice on flt(source.amount) — true gives pending\_amount, false gives 0.
- Otherwise.
  - Set target.amount from (flt(source.amount) − flt(source.billed\_amt)).
- Set target.base\_amount from (target.amount × flt(source\_parent.conversion\_rate)).
- Set target.qty from source.qty when is\_unit\_price\_row(source), otherwise get\_pending\_qty(source).
  - Value choice on is\_unit\_price\_row(source) — true gives source.qty, false gives get\_pending\_qty(source).
- If source\_parent.project.
  - Set target.cost\_center from Platform.db.get\_value(“Project”, source\_parent.project, “cost\_center”).
- If target.item\_code.
  - Set target.enable\_deferred\_revenue from Platform.get\_cached\_value(“Item”, target.item\_code, “enable\_deferred\_revenue”).
  - Set item from get\_item\_defaults(target.item\_code, source\_parent.company).
  - Set item\_group from get\_item\_group\_defaults(target.item\_code, source\_parent.company).
  - Set cost\_center from (item.get(“selling\_cost\_center”) or item\_group.get(“selling\_cost\_center”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“selling\_cost\_center”) → item\_group.get(“selling\_cost\_center”).
  - If cost\_center.
    - Set target.cost\_center from cost\_center.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, target.item\_code, “enable\_deferred\_revenue”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L69)

<a id="op-96ffb614d88595"></a>
### Make sales invoice.select item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L67)

<a id="op-f926285f2aed90"></a>
### Make sales invoice.add self rm

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_sales_invoice_add_self_rm`

**Inputs** doclist.

**Local steps**

- Set parent from Platform.qb.DocType(“Subcontracting Inward Order”).
- Set child from Platform.qb.DocType(“Subcontracting Inward Order Received Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(child.required\_qty, child.consumed\_qty, child.bill ….
- Set result from query.run(as\_dict = true).
- If result.
  - Set idx from (len(doclist.items) + 1).
  - For each item in result.
    - If qty bound to (max(item.required\_qty, item.consumed\_qty) − item.billed\_qty) &gt; 0.
      - Evaluate doclist.append(“items”, mapping(“item\_code” → item.rm\_item\_code, “qty” → qty, “uom” → item.stock\_uom, “scio\_detail” → item.name)).
      - Evaluate doclist.process\_item\_selection(idx).
      - Update idx using + 1.
- Set doclist.has\_subcontracted from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L60)

<a id="op-4a493808eb9526"></a>
### Make maintenance schedule

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_maintenance_schedule`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Maintenance Schedule).

**Explicit results** doclist.

**Local steps**

- Set maint\_schedule from Platform.db.sql(query text (SELECT, Maintenance Schedule), source\_name).
- If not maint\_schedule.
  - Set doclist from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Maintenance Schedule”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Sales Order Item” → mapping(“doctype” →  ….
  - Return doclist.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L43)

<a id="op-8e1a94e6864504"></a>
### Make maintenance visit

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_maintenance_visit`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Maintenance Visit).

**Explicit results** doclist.

**Local steps**

- Set visit from Platform.db.sql(query text (SELECT, Maintenance Visit), source\_name).
- If not visit.
  - Set doclist from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Maintenance Visit”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Sales Order Item” → mapping(“doctype” → “Ma ….
  - Return doclist.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L44)

<a id="op-abb3a04cc38c79"></a>
### Get events

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_get_events`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** execute a supplied database query.

**Explicit results** data.

**Local steps**

- Bind dependencies get\_event\_conditions.
- Set conditions from get\_event\_conditions(“Sales Order”, filters).
- Set data from Platform.db.sql(formatted text   select  distinct ′tabSales Order′.name, ′tabSales Order′.customer\_name, ′tabSales Order′.status,  ′tabSales Order′.delivery\_status, ′tabSales O, mapping(“start” → star ….
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1329)

<a id="op-8da888a99bf553"></a>
### Make purchase order

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_purchase_order`

**Inputs** source\_name, selected\_items = no value, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** no value · purchase\_orders.

**Explicit failure paths** validation helper — translated “Select a valid Sales Order row for Item {0}.”.format(Platform.bold((item.get(“item\_code”) or item.get(“name”)))).

**Local steps**

- Bind dependencies get\_exchange\_rate.
- If not selected\_items.
  - Return no value.
- If isinstance(selected\_items, str).
  - Set selected\_items from json.loads(selected\_items).
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation update\_item\_for\_packed\_item for subsequent calls.
- Bind local operation filter\_items for subsequent calls.
- Set sales\_order from Platform.get\_doc(“Sales Order”, source\_name).
- Evaluate sales\_order.check\_permission(“read”).
- Set qty\_to\_order from get\_qty\_to\_order(sales\_order.items, “sales\_order\_item”).
- Set items\_to\_map from mapping().
- For each item in selected\_items.
  - Set filters from mapping(“name” → item.get(“name”)) when item.get(“name”), otherwise mapping(“item\_code” → item.get(“item\_code”)).
    - Value choice on item.get(“name”) — true gives mapping(“name” → item.get(“name”)), false gives mapping(“item\_code” → item.get(“item\_code”)).
  - Set rows from sales\_order.get(“items”, filters).
  - <a id="op-8da888a99bf553-guard-88"></a>If len(rows) differs from 1.
    - Call the validation error handler Platform.throw(translated “Select a valid Sales Order row for Item {0}.”.format(Platform.bold((item.get(“item\_code”) or item.get(“name”)))), title = translated “Invalid Item Selection”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“item\_code”) → item.get(“name”).
  - Set items\_to\_map at rows at 0.name from item.get(“supplier”).
- Set suppliers from list(set(items\_to\_map.values())).
- If not suppliers.
  - Set suppliers from list(no value).
- Set purchase\_orders from list().
- For each supplier in suppliers.
  - Set doc from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Purchase Order”, “field\_no\_map” → list(expanded CROSS\_PARTY\_FIELD\_NO\_MAP), “validation” → mapping(“docstatus” → list( ….
  - Evaluate set\_delivery\_date(doc.items, source\_name).
  - If doc.supplier.
    - Evaluate doc.insert().
  - Evaluate purchase\_orders.append(doc).
- Return purchase\_orders.

**Derived branch illustrations**

- At the comparison len(rows) differs from 1, length of rows = 2 selects the branch that calls the validation-error handler with translated “Select a valid Sales Order row for Item {0}.”.format(Platform.bold((item.get(“item\_code”) or item.get(“name”)))). With length of rows = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8da888a99bf553-guard-88)

**Values supplied outside this operation** effective access from sales\_order.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L53)

<a id="op-1cb3cf4fed3965"></a>
### Make purchase order.set missing values

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_purchase_order_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Supplier” via get\_value · read “Company” via get\_value.

**Local steps**

- Set target.supplier from supplier.
- Set target.currency from Platform.db.get\_value(“Supplier”, filters = mapping(“name” → supplier), fieldname = list(“default\_currency”)).
- Set company\_currency from Platform.db.get\_value(“Company”, filters = mapping(“name” → target.company), fieldname = list(“default\_currency”)).
- Set target.conversion\_rate from get\_exchange\_rate(target.currency, company\_currency, args = “for\_buying”).
- Set target.apply\_discount\_on from empty text.
- Set target.additional\_discount\_percentage from 0.0.
- Set target.discount\_amount from 0.0.
- Set target.shipping\_rule from empty text.
- Set target.tc\_name from empty text.
- Set target.terms from empty text.
- Set target.incoterm from empty text.
- Set target.named\_place from empty text.
- Set target.payment\_schedule from list().
- Set default\_price\_list from Platform.get\_value(“Supplier”, supplier, “default\_price\_list”).
- If default\_price\_list.
  - Set target.buying\_price\_list from default\_price\_list.
- Set default\_payment\_terms from Platform.get\_value(“Supplier”, supplier, “payment\_terms”).
- If default\_payment\_terms.
  - Set target.payment\_terms\_template from default\_payment\_terms.
- If any(generator of item.delivered\_by\_supplier for item drawn from target.items).
  - Draw item from target.items.
  - If source.shipping\_address\_name.
    - Set target.shipping\_address from source.shipping\_address\_name.
    - Set target.shipping\_address\_display from source.shipping\_address.
  - Otherwise.
    - Set target.shipping\_address from source.customer\_address.
    - Set target.shipping\_address\_display from source.address\_display.
  - Set target.customer\_contact\_person from source.contact\_person.
  - Set target.customer\_contact\_display from source.contact\_display.
  - Set target.customer\_contact\_mobile from source.contact\_mobile.
  - Set target.customer\_contact\_email from source.contact\_email.
- Otherwise.
  - Set target.customer from empty text.
  - Set target.customer\_name from empty text.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“calculate\_taxes\_and\_totals”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L55)

<a id="op-aaabb6814efe91"></a>
### Make purchase order.update item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_purchase_order_update_item`

**Inputs** source, target, source\_parent.

**Local steps**

- Set target.schedule\_date from source.delivery\_date.
- Set target.qty from qty\_to\_order at source.name.
- Set target.stock\_qty from (target.qty × flt(source.conversion\_factor)).
- Set target.project from source\_parent.project.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L56)

<a id="op-a9a402ae96c69a"></a>
### Make purchase order.update item for packed item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_purchase_order_update_item_for_packed_item`

**Inputs** source, target, \_.

**Local steps**

- Set target.qty from (flt(source.qty) − flt(source.ordered\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L57)
