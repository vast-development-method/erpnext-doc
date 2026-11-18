# Sales · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales order

[Record definition](../../../../data/record-types/sales_order.json)

<a id="op-91f9be66d3667e"></a>
### Sales Order.cancel stock reservation entries

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_cancel_stock_reservation_entries`

**Inputs** self, sre\_list = no value, notify = true.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Bind dependencies cancel\_stock\_reservation\_entries.
- Evaluate cancel\_stock\_reservation\_entries(voucher\_type = self.doctype, voucher\_no = self.name, sre\_list = sre\_list, notify = notify).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1341)

<a id="op-7850623c563cd4"></a>
### Sales Order.set missing values

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_set_missing_values`

**Inputs** self, for\_validate = false.

**Local steps**

- Evaluate super().set\_missing\_values(for\_validate).
- If self.delivery\_date.
  - For each item in self.items.
    - If not item.delivery\_date.
      - Set item.delivery\_date from self.delivery\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L3525) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1358)

<a id="op-2ccc2e33f4390e"></a>
### Sales Order.get delivery schedule

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_get_delivery_schedule`

**Inputs** self, sales\_order\_item.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Delivery Schedule Item” via get\_all.

**Explicit results** Platform.get\_all(“Delivery Schedule Item”, filters = mapping(“sales\_order\_item” → sales\_order\_item, “sales\_order” → self.name), fields = list(“delivery\_date”, “qty”, “name”), order\_by = “delivery\_date asc”).

**Local steps**

- Return Platform.get\_all(“Delivery Schedule Item”, filters = mapping(“sales\_order\_item” → sales\_order\_item, “sales\_order” → self.name), fields = list(“delivery\_date”, “qty”, “name”), order\_by = “delivery\_date asc”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1346)

<a id="op-7c25dc62b8a5e6"></a>
### Sales Order.create delivery schedule

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_create_delivery_schedule`

**Inputs** self, child\_row, schedules.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Delivery Schedule Item” via exists · resolve a document from “Delivery Schedule Item” via get\_doc.

**State and service calls** request new\_doc for “Delivery Schedule Item” · call save on doc.

**Explicit failure paths** validation helper — translated “Row {0} does not belong to this Sales Order”.format(child\_row.name) · validation helper — translated “Total delivery schedule quantity cannot be greater than the item quantity”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- If isinstance(child\_row, dict).
  - Set child\_row from Platform.\_dict(child\_row).
- If isinstance(schedules, str).
  - Set schedules from parse\_json(schedules).
- Set item\_row from next(generator of r for r drawn from self.items where r.name equals child\_row.name, no value).
  - Draw r from self.items, keep a combination only if (r.name equals child\_row.name).
- If not item\_row.
  - Call the validation error handler Platform.throw(translated “Row {0} does not belong to this Sales Order”.format(child\_row.name)).
- Set schedules from list of Platform.\_dict(row) for row drawn from schedules.
  - Draw row from schedules.
- Set conversion\_factor from (flt(item\_row.conversion\_factor) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item\_row.conversion\_factor) → 1.0.
- Set total\_qty from sum(generator of flt(row.qty) for row drawn from schedules).
  - Draw row from schedules.
- If flt(total\_qty, item\_row.precision(“qty”)) &gt; flt(item\_row.qty, item\_row.precision(“qty”)).
  - Call the validation error handler Platform.throw(translated “Total delivery schedule quantity cannot be greater than the item quantity”).
- Set names from list().
- For each row in schedules.
  - Set data from mapping(“delivery\_date” → row.delivery\_date, “qty” → row.qty, “uom” → item\_row.uom, “stock\_uom” → item\_row.stock\_uom, …).
  - If (row.name and Platform.db.exists(“Delivery Schedule Item”, mapping(“name” → row.name, “sales\_order” → self.name, “sales\_order\_item” → item\_row.name))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.name → Platform.db.exists(“Delivery Schedule Item”, mapping(“name” → row.name, “sales\_order” → self.name, “sales\_order\_item” → item\_row.name)).
    - Set doc from Platform.get\_doc(“Delivery Schedule Item”, row.name).
  - Otherwise.
    - Set doc from Platform.new\_doc(“Delivery Schedule Item”).
  - Evaluate doc.update(data).
  - Evaluate doc.save(ignore\_permissions = true).
  - Evaluate names.append(doc.name).
- If names.
  - Evaluate self.delete\_delivery\_schedule\_items(item\_row.name, names).
- Set dated\_schedules from list of row for row drawn from schedules where row.delivery\_date.
  - Draw row from schedules, keep a combination only if (row.delivery\_date).
- If dated\_schedules.
  - Set earliest from min(dated\_schedules, key = deferred anonymous expression).
  - Evaluate self.update\_delivery\_date\_based\_on\_schedule(item\_row, earliest.delivery\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete delivery schedule items](operations-017.md#op-ec31da29995d33), [update delivery date based on schedule](operations-017.md#op-c7f36ba7d9854a).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1344)

<a id="op-c7f36ba7d9854a"></a>
### Sales Order.update delivery date based on schedule

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_update_delivery_date_based_on_schedule`

**Inputs** self, child\_row, first\_delivery\_date.

**State and service calls** call save on self.

**Local steps**

- For each row in self.items.
  - If row.name equals child\_row.name.
    - If first\_delivery\_date.
      - Set row.delivery\_date from first\_delivery\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L81)

<a id="op-0c83d0c3703f85"></a>
### Sales Order.sync schedule with item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_sync_schedule_with_item`

**Inputs** self, child\_row.

**Record and data access** read “Delivery Schedule Item” via get\_all.

**State and service calls** request set\_value on “Delivery Schedule Item”.

**Explicit results** no value.

**Local steps**

- Set schedules from Platform.get\_all(“Delivery Schedule Item”, filters = mapping(“sales\_order\_item” → child\_row.name, “sales\_order” → self.name), fields = list(“name”, “qty”), order\_by = “delivery\_date asc, creation asc”).
- If not schedules.
  - Return no value.
- Set conversion\_factor from (child\_row.conversion\_factor or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_row.conversion\_factor → 1.0.
- Set remaining from flt(child\_row.qty).
- Set stale from list().
- For each schedule in schedules.
  - Set kept\_qty from min(flt(schedule.qty), remaining) when remaining &gt; 0, otherwise 0.
    - Value choice on remaining &gt; 0 — true gives min(flt(schedule.qty), remaining), false gives 0.
  - If not kept\_qty.
    - Evaluate stale.append(schedule.name).
    - Continue with the next iteration or loop test.
  - Update remaining using − kept\_qty.
  - Evaluate Platform.db.set\_value(“Delivery Schedule Item”, schedule.name, mapping(“qty” → kept\_qty, “uom” → child\_row.uom, “stock\_uom” → child\_row.stock\_uom, “conversion\_factor” → conversion\_factor, …)).
- If stale.
  - Set doctype from Platform.qb.DocType(“Delivery Schedule Item”).
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where(doctype.name.isin(stale)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L80)

<a id="op-ec31da29995d33"></a>
### Sales Order.delete delivery schedule items

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_delete_delivery_schedule_items`

**Inputs** self, sales\_order\_item = no value, ignore\_names = no value.

**Local steps**

- Set doctype from Platform.qb.DocType(“Delivery Schedule Item”).
- Set query from nested operand in the contract.qb.from\_(doctype).delete().where(doctype.sales\_order equals self.name).
- If ignore\_names.
  - Set query from query.where(doctype.name.notin(ignore\_names)).
- If sales\_order\_item.
  - Set query from query.where(doctype.sales\_order\_item equals sales\_order\_item).
- Evaluate query.run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L74)

<a id="op-c382a0f5066202"></a>
### Get unreserved qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_unreserved_qty`

**Inputs** item, reserved\_qty\_details.

**Declared result** float.

**Record and data access** read “Sales Order Item” via get\_value.

**Explicit results** ((item.stock\_qty − (flt(item.delivered\_qty) × item.get(“conversion\_factor”, 1))) − existing\_reserved\_qty) · ((item.qty − delivered\_qty) − existing\_reserved\_qty).

**Local steps**

- Set existing\_reserved\_qty from reserved\_qty\_details.get(item.name, 0).
- If item.get(“delivered\_qty”) is distinct from no value.
  - Return ((item.stock\_qty − (flt(item.delivered\_qty) × item.get(“conversion\_factor”, 1))) − existing\_reserved\_qty).
- Otherwise.
  - Set tuple(stock\_qty, delivered\_qty, conversion\_factor) from Platform.get\_value(“Sales Order Item”, item.parent\_detail\_docname, list(“stock\_qty”, “delivered\_qty”, “conversion\_factor”)).
  - Set bundle\_conversion\_factor from (item.qty ÷ stock\_qty).
  - Set delivered\_qty from ((delivered\_qty × conversion\_factor) × bundle\_conversion\_factor).
  - Return ((item.qty − delivered\_qty) − existing\_reserved\_qty).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L31)

<a id="op-894e47d2fe1c8c"></a>
### Get list context

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Orders”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L3903) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1330)

<a id="op-3505bd4947c191"></a>
### Is enable cutoff date on bulk delivery note creation

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_is_enable_cutoff_date_on_bulk_delivery_note_creation`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** Platform.get\_single\_value(“Selling Settings”, “enable\_cutoff\_date\_on\_bulk\_delivery\_note\_creation”).

**Local steps**

- Return Platform.get\_single\_value(“Selling Settings”, “enable\_cutoff\_date\_on\_bulk\_delivery\_note\_creation”).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “enable\_cutoff\_date\_on\_bulk\_delivery\_note\_creation”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L4083) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L66) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1337)

<a id="op-ab5a9dd89ff146"></a>
### Close or unclose sales orders

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_close_or_unclose_sales_orders`

**Inputs** names, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid name”.

**Local steps**

- Evaluate Platform.has\_permission(“Sales Order”, “write”, throw = true).
- Set names from json.loads(names).
- For each name in names.
  - If not isinstance(name, str).
    - Call the validation error handler Platform.throw(translated “Invalid name”, Platform.PermissionError).
  - Set so from Platform.get\_lazy\_doc(“Sales Order”, name, check\_permission = “submit”).
  - If so.docstatus equals 1.
    - If status equals “Closed”.
      - If (so.status does not belong to tuple(“Cancelled”, “Closed”) and (so.per\_delivered &lt; 100 or so.per\_billed &lt; 100)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in so.status does not belong to tuple(“Cancelled”, “Closed”) → (so.per\_delivered &lt; 100 or so.per\_billed &lt; 100).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in so.per\_delivered &lt; 100 → so.per\_billed &lt; 100.
        - Evaluate so.update\_status(status).
    - Otherwise.
      - If so.status equals “Closed”.
        - Evaluate so.update\_status(“Draft”).
    - Evaluate so.update\_blanket\_order().
- Set Platform.local.message\_log from list().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Order”, “write”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1328)

<a id="op-b427000dfc49fa"></a>
### Get requested item qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_get_requested_item_qty`

**Inputs** sales\_order.

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Explicit results** result.

**Local steps**

- Set result from mapping().
- Set so from Platform.get\_doc(“Sales Order”, sales\_order).
- For each item in so.items.
  - If is\_product\_bundle(item.item\_code).
    - For each packed\_item in so.get(“packed\_items”).
      - If (packed\_item.parent\_item equals item.item\_code and packed\_item.parent\_detail\_docname equals item.name).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in packed\_item.parent\_item equals item.item\_code → packed\_item.parent\_detail\_docname equals item.name.
        - Set result at packed\_item.name from Platform.\_dict(mapping(“qty” → packed\_item.requested\_qty)).
  - Otherwise.
    - Set result at item.name from Platform.\_dict(mapping(“qty” → item.requested\_qty)).
- Return result.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L30)

<a id="op-c25fc646a6453a"></a>
### Make material request

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_material_request`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “Material Request already created for the ordered quantity”.

**Local steps**

- Set requested\_item\_qty from get\_requested\_item\_qty(source\_name).
- Bind local operation postprocess for subsequent calls.
- Bind local operation get\_remaining\_qty for subsequent calls.
- Bind local operation get\_remaining\_packed\_item\_qty for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Set doc from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Material Request”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Packed Item” → mapping(“doctype” → “Material ….
- If (doc and doc.items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.items.
  - Return doc.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Material Request already created for the ordered quantity”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L45)

<a id="op-2e6fcf8bc84523"></a>
### Make material request.postprocess

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_material_request_postprocess`

**Inputs** source, target.

**Record and data access** read “Terms and Conditions” via get\_value.

**Local steps**

- If (source.tc\_name and Platform.db.get\_value(“Terms and Conditions”, source.tc\_name, “buying”) differs from 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source.tc\_name → Platform.db.get\_value(“Terms and Conditions”, source.tc\_name, “buying”) differs from 1.
  - Set target.tc\_name from no value.
  - Set target.terms from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L48)

<a id="op-8f92f91e72b8e0"></a>
### Make material request.get remaining qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_material_request_get_remaining_qty`

**Inputs** so\_item.

**Explicit results** flt(((flt(so\_item.qty) − (flt(nested operand in the contract.get(“qty”)) ÷ (flt(nested operand in the contract.conversion\_factor) or 1))) − max(flt(so\_item.get(“delivered\_qty”)), 0))).

**Local steps**

- Return flt(((flt(so\_item.qty) − (flt(nested operand in the contract.get(“qty”)) ÷ (flt(nested operand in the contract.conversion\_factor) or 1))) − max(flt(so\_item.get(“delivered\_qty”)), 0))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(so\_item.conversion\_factor) → 1.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L47)

<a id="op-cef417fa56a3b8"></a>
### Make material request.get remaining packed item qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_material_request_get_remaining_packed_item_qty`

**Inputs** so\_item.

**Record and data access** read “Sales Order Item” via get\_value.

**Explicit results** flt(((flt(so\_item.qty) − flt(nested operand in the contract(nested operand in the contract, nested operand in the contract).get(“qty”))) − max((flt(parent.delivered\_qty) × components\_per\_unit), 0))).

**Local steps**

- Set parent from Platform.db.get\_value(“Sales Order Item”, so\_item.parent\_detail\_docname, list(“delivered\_qty”, “qty”), as\_dict = true).
- Set components\_per\_unit from (flt(so\_item.qty) ÷ (flt(parent.qty) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(parent.qty) → 1.
- Return flt(((flt(so\_item.qty) − flt(nested operand in the contract(nested operand in the contract, nested operand in the contract).get(“qty”))) − max((flt(parent.delivered\_qty) × components\_per\_unit), 0))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L46)

<a id="op-691165644fb600"></a>
### Make material request.update item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_material_request_update_item`

**Inputs** source, target, source\_parent.

**Record and data access** read “Buying Settings” via get\_single\_value · resolve a document from “Item” via get\_cached\_doc.

**Local steps**

- Set target.project from source\_parent.project.
- Set target.qty from get\_remaining\_packed\_item\_qty(source) when source.parentfield equals “packed\_items”, otherwise get\_remaining\_qty(source).
  - Value choice on source.parentfield equals “packed\_items” — true gives get\_remaining\_packed\_item\_qty(source), false gives get\_remaining\_qty(source).
- Set target.stock\_qty from (flt(target.qty) × flt(target.conversion\_factor)).
- Set target.actual\_qty from \_get\_bin\_details(target.item\_code, target.warehouse, source\_parent.company, true).get(“actual\_qty”, 0).
- Set ctx from ItemDetailsCtx(target.as\_dict().copy()).
- Evaluate ctx.update(mapping(“company” → source\_parent.get(“company”), “price\_list” → Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”), “currency” → source\_parent.get(“currency”), “conversion\_rat ….
- Set target.rate from flt(get\_price\_list\_rate(ctx, item\_doc = Platform.get\_cached\_doc(“Item”, target.item\_code)).get(“price\_list\_rate”)).
- Set target.amount from (target.qty × target.rate).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”), Platform.get\_cached\_doc(“Item”, target.item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L49)

<a id="op-bb2e50ffe5896b"></a>
### Make project

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_project`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- Bind local operation postprocess for subsequent calls.
- Set doc from get\_mapped\_doc(“Sales Order”, source\_name, mapping(“Sales Order” → mapping(“doctype” → “Project”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_map” → mapping(“name” → “sales\_order”, “base\_gra ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L51)

<a id="op-56d41d40ea7574"></a>
### Make project.postprocess

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_project_postprocess`

**Inputs** source, doc.

**Record and data access** read “Project Type” via exists.

**Local steps**

- If Platform.db.exists(“Project Type”, “External”).
  - Set doc.project\_type from “External”.
- Set doc.project\_name from source.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L52)

<a id="op-5ed316f07a5c21"></a>
### Set reserved serial batch

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_set_reserved_serial_batch`

**Inputs** row, sre\_list, use\_serial\_batch\_fields.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_serial\_batch\_entries\_for\_voucher.
- If use\_serial\_batch\_fields.
  - Set entries from get\_serial\_batch\_entries\_for\_voucher(list of sre.name for sre drawn from sre\_list).
    - Draw sre from sre\_list.
  - Set batch\_nos from list(set of d.batch\_no for d drawn from entries where d.batch\_no).
    - Draw d from entries, keep a combination only if (d.batch\_no).
  - If len(batch\_nos) &lt; 2.
    - Set row.use\_serial\_batch\_fields from 1.
    - Set row.serial\_no from (whitespace '\\n'.join(generator of d.serial\_no for d drawn from entries where d.serial\_no) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in whitespace '\\n'.join(generator of d.serial\_no for d drawn from entries where d.serial\_no) → no value.
      - Draw d from entries, keep a combination only if (d.serial\_no).
    - Set row.batch\_no from batch\_nos at 0 when batch\_nos, otherwise no value.
      - Value choice on batch\_nos — true gives batch\_nos at 0, false gives no value.
    - Return no value.
- Set row.use\_serial\_batch\_fields from 0.
- Set row.serial\_and\_batch\_bundle from get\_ssb\_bundle\_for\_voucher(sre\_list).name.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L89)

<a id="op-3fb4dd5d8f777b"></a>
### Set serial batch for bundle reservation

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_set_serial_batch_for_bundle_reservation`

**Inputs** target, use\_serial\_batch\_fields, packed\_sre.

**Local steps**

- For each tuple(packed\_item, so\_packed\_item) in get\_order\_packed\_item\_pairs(target).
  - Set sre\_list from list of sre for sre drawn from packed\_sre where (sre.voucher\_detail\_no equals so\_packed\_item.name and sre.warehouse equals packed\_item.warehouse).
    - Draw sre from packed\_sre, keep a combination only if ((sre.voucher\_detail\_no equals so\_packed\_item.name and sre.warehouse equals packed\_item.warehouse)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sre.voucher\_detail\_no equals so\_packed\_item.name → sre.warehouse equals packed\_item.warehouse.
  - If (sre\_list and sre\_list at 0.reservation\_based\_on equals “Serial and Batch”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sre\_list → sre\_list at 0.reservation\_based\_on equals “Serial and Batch”.
    - Evaluate set\_reserved\_serial\_batch(packed\_item, sre\_list, use\_serial\_batch\_fields).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L90)

<a id="op-a6f04d45ec24fd"></a>
### Make delivery note

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note`

**Inputs** source\_name, target\_doc = no value, kwargs = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Order” via get\_value · read “Stock Settings” via get\_single\_value · resolve a document from “Sales Order” via get\_doc.

**Explicit results** no value · target\_doc.

**Local steps**

- Bind dependencies get\_sre\_reserved\_qty\_details\_for\_voucher.
- If not kwargs.
  - Set kwargs from mapping(“for\_reserved\_stock” → (Platform.flags.args and Platform.flags.args.for\_reserved\_stock), “skip\_item\_mapping” → (Platform.flags.args and Platform.flags.args.skip\_item\_mapping)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.args → Platform.flags.args.for\_reserved\_stock.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.args → Platform.flags.args.skip\_item\_mapping.
- Set kwargs from Platform.\_dict(kwargs).
- Set sre\_details from mapping().
- If kwargs.for\_reserved\_stock.
  - Set sre\_details from get\_sre\_reserved\_qty\_details\_for\_voucher(“Sales Order”, source\_name).
- Set mapped\_qty\_by\_item from get\_qty\_already\_mapped(target\_doc, “so\_detail”).
- Set mapper from mapping(“Sales Order” → mapping(“doctype” → “Delivery Note”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Sales Taxes and Charges” → mapping(“doctype” → “Sales Taxes and Charges”, “reset\_value” →  ….
- Set has\_unit\_price\_items from Platform.db.get\_value(“Sales Order”, source\_name, “has\_unit\_price\_items”).
- Set use\_serial\_batch\_fields from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).
- Bind local operation is\_unit\_price\_row for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation condition for subsequent calls.
- Bind local operation remaining\_qty for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- If not kwargs.skip\_item\_mapping.
  - Set mapper at “Sales Order Item” from mapping(“doctype” → “Delivery Note Item”, “field\_map” → mapping(“rate” → “rate”, “name” → “so\_detail”, “parent” → “against\_sales\_order”), “condition” → deferred anonymous expression, “postprocess” → update\_item).
- Set so from Platform.get\_doc(“Sales Order”, source\_name).
- Set target\_doc from get\_mapped\_doc(“Sales Order”, so.name, mapper, target\_doc).
- Set packed\_sre from list().
- If (not kwargs.skip\_item\_mapping and kwargs.for\_reserved\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.skip\_item\_mapping → kwargs.for\_reserved\_stock.
  - Set sre\_list from get\_sre\_details\_for\_voucher(“Sales Order”, source\_name).
  - If sre\_list.
    - Bind local operation update\_dn\_item for subsequent calls.
    - Set so\_items from mapping of d.name → d for d drawn from so.items where d.stock\_reserved\_qty.
      - Draw d from so.items, keep a combination only if (d.stock\_reserved\_qty).
    - For each sre in sre\_list.
      - If not so\_items.get(sre.voucher\_detail\_no).
        - Evaluate packed\_sre.append(sre).
        - Continue with the next iteration or loop test.
      - If not condition(so\_items at sre.voucher\_detail\_no).
        - Continue with the next iteration or loop test.
      - Set dn\_item from get\_mapped\_doc(“Sales Order Item”, sre.voucher\_detail\_no, mapping(“Sales Order Item” → mapping(“doctype” → “Delivery Note Item”, “field\_map” → mapping(“rate” → “rate”, “name” → “so\_detail”, “parent” → “aga ….
      - Set dn\_item.qty from (flt(sre.reserved\_qty) ÷ flt(dn\_item.get(“conversion\_factor”, 1))).
      - Set dn\_item.warehouse from sre.warehouse.
      - If (sre.reservation\_based\_on equals “Serial and Batch” and (sre.has\_serial\_no or sre.has\_batch\_no)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in sre.reservation\_based\_on equals “Serial and Batch” → (sre.has\_serial\_no or sre.has\_batch\_no).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in sre.has\_serial\_no → sre.has\_batch\_no.
        - Evaluate set\_reserved\_serial\_batch(dn\_item, list(sre), use\_serial\_batch\_fields).
      - Evaluate target\_doc.append(“items”, dn\_item).
    - After normal loop exhaustion.
      - For each tuple(idx, item) in enumerate(target\_doc.items).
        - Set item.idx from (idx + 1).
- If (not kwargs.skip\_item\_mapping and Platform.flags.bulk\_transaction and not target\_doc.items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.skip\_item\_mapping → Platform.flags.bulk\_transaction → not target\_doc.items.
  - Remove target\_doc.
  - Return no value.
- Set target\_doc.packed\_items from list().
- Evaluate set\_missing\_values(so, target\_doc).
- Evaluate set\_serial\_batch\_for\_bundle\_reservation(target\_doc, use\_serial\_batch\_fields, packed\_sre).
- Return target\_doc.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L34)

<a id="op-9562823cc84e5a"></a>
### Make delivery note.is unit price row

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note_is_unit_price_row`

**Inputs** source.

**Explicit results** (has\_unit\_price\_items and source.qty equals 0).

**Local steps**

- Return (has\_unit\_price\_items and source.qty equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_unit\_price\_items → source.qty equals 0.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L36)

<a id="op-c1572308719a8e"></a>
### Make delivery note.select item

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_make_delivery_note_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from kwargs.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L38)
