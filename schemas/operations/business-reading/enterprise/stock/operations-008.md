# Inventory and warehouses · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Delivery note

[Record definition](../../../../data/record-types/delivery_note.json)

<a id="op-03277e31269120"></a>
### Get list context

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Shipments”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0713.json#L6625) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L891)

<a id="op-7f47c47a6af380"></a>
### Get invoiced qty map

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_invoiced_qty_map`

**Inputs** delivery\_note.

**Explicit results** invoiced\_qty\_map.

**Local steps**

- Set sii from DocType(“Sales Invoice Item”).
- Set dni from DocType(“Delivery Note Item”).
- Set invoiced\_qty\_map from Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(dni.name).run()).
- Return invoiced\_qty\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L226)

<a id="op-3d1b3bb34e9bee"></a>
### Get returned qty map

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_returned_qty_map`

**Inputs** delivery\_note.

**Explicit results** returned\_qty\_map.

**Local steps**

- Set dn from DocType(“Delivery Note”).
- Set dni from DocType(“Delivery Note Item”).
- Set returned\_against from DocType(“Delivery Note Item”).as\_(“returned\_against”).
- Set returned\_qty\_map from Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(returned\_against.name).run()).
- Return returned\_qty\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L230)

<a id="op-5e975b5639d81c"></a>
### Make sales invoice

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_sales_invoice`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Delivery Note” via get\_doc · read “Accounts Settings” via get\_single\_value · read doctype via get\_value.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “Delivery Note {0} is closed and cannot be invoiced”.format(Platform.bold(doc.name)).

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set doc from Platform.get\_doc(“Delivery Note”, source\_name).
- If doc.status equals “Closed”.
  - Call the validation error handler Platform.throw(translated “Delivery Note {0} is closed and cannot be invoiced”.format(Platform.bold(doc.name))).
- Set to\_make\_invoice\_qty\_map from mapping().
- Set returned\_qty\_map from get\_returned\_qty\_map(source\_name).
- Set invoiced\_qty\_map from get\_invoiced\_qty\_map(source\_name).
- For each tuple(ref, qty) in get\_qty\_already\_mapped(target\_doc, “dn\_detail”).items().
  - Set invoiced\_qty\_map at ref from (invoiced\_qty\_map.get(ref, 0) + qty).
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation get\_pending\_qty for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set doc from get\_mapped\_doc(“Delivery Note”, source\_name, mapping(“Delivery Note” → mapping(“doctype” → “Sales Invoice”, “field\_map” → mapping(“is\_return” → “is\_return”), “validation” → mapping(“docstatus” → list(“=”,  ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args → args.get(“merge\_taxes”).
  - Value choice on args — true gives args.get(“merge\_taxes”), false gives 0.
- Set automatically\_fetch\_payment\_terms from cint(Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”)).
- If doc.is\_return.
  - Set doc.update\_billed\_amount\_in\_sales\_order from true.
- Otherwise.
  - Set tuple(so, doctype, fieldname) from doc.get\_order\_details().
  - If (doc.linked\_order\_has\_payment\_terms(so, fieldname, doctype) and not automatically\_fetch\_payment\_terms).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.linked\_order\_has\_payment\_terms(so, fieldname, doctype) → not automatically\_fetch\_payment\_terms.
    - Set payment\_terms\_template from Platform.db.get\_value(doctype, so, “payment\_terms\_template”).
    - Set doc.payment\_terms\_template from payment\_terms\_template.
    - Set doc.due\_date from get\_due\_date(doc.posting\_date, “Customer”, doc.customer, doc.company, template\_name = doc.payment\_terms\_template).
  - Otherwise.
    - If automatically\_fetch\_payment\_terms.
      - Evaluate doc.set\_payment\_schedule().
- Return doc.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L247)

<a id="op-948d027f1f7cd8"></a>
### Make sales invoice.set missing values

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_sales_invoice_set_missing_values`

**Inputs** source, target.

**Explicit failure paths** validation helper — translated “All these items have already been Invoiced/Returned”.

**Local steps**

- Set target.update\_stock from 0.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“set\_po\_nos”).
- <a id="op-948d027f1f7cd8-guard-6"></a>If len(target.get(“items”)) equals 0.
  - Call the validation error handler Platform.throw(translated “All these items have already been Invoiced/Returned”).
- If (args and args.get(“merge\_taxes”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args → args.get(“merge\_taxes”).
  - Evaluate merge\_taxes(source, target).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).
- If source.company\_address.
  - Evaluate target.update(mapping(“company\_address” → source.company\_address)).
- Otherwise.
  - Evaluate target.update(get\_company\_address(target.company)).
- If target.company\_address.
  - Evaluate target.update(get\_fetch\_values(“Sales Invoice”, “company\_address”, target.company\_address)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(target.get(“items”)) equals 0, length of target.items = 0 selects the branch that calls the validation-error handler with translated “All these items have already been Invoiced/Returned”. With length of target.items = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-948d027f1f7cd8-guard-6)

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“set\_po\_nos”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L250)

<a id="op-debdbaec727e2a"></a>
### Make sales invoice.update item

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_sales_invoice_update_item`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Set target\_doc.qty from to\_make\_invoice\_qty\_map at source\_doc.name.
- Set target\_doc.\_old\_name from source\_doc.name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L251)

<a id="op-675b0a62a572c6"></a>
### Make sales invoice.get pending qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_sales_invoice_get_pending_qty`

**Inputs** item\_row.

**Explicit results** pending\_qty.

**Local steps**

- Set pending\_qty from (item\_row.qty − invoiced\_qty\_map.get(item\_row.name, 0)).
- Set returned\_qty from 0.
- If returned\_qty\_map.get(item\_row.name, 0) &gt; 0.
  - Set returned\_qty from flt(returned\_qty\_map.get(item\_row.name, 0)).
  - Update returned\_qty\_map at item\_row.name using − pending\_qty.
- If returned\_qty.
  - If returned\_qty ≥ pending\_qty.
    - Set pending\_qty from 0.
    - Update returned\_qty using − pending\_qty.
  - Otherwise.
    - Update pending\_qty using − returned\_qty.
    - Set returned\_qty from 0.
- Set to\_make\_invoice\_qty\_map at item\_row.name from pending\_qty.
- Return pending\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L248)

<a id="op-dddf25cb513096"></a>
### Make sales invoice.select item

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_sales_invoice_select_item`

**Inputs** d.

**Explicit results** (child\_filter and not d.si\_detail).

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return (child\_filter and not d.si\_detail).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in child\_filter → not d.si\_detail.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L249)

<a id="op-b83d8da8af0906"></a>
### Make delivery trip

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_delivery_trip`

**Inputs** source\_name, target\_doc = no value, kwargs = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Delivery Note” via get\_value.

**State and service calls** request new\_doc for “Delivery Trip”.

**Explicit results** doclist.

**Explicit failure paths** validation helper — translated “Delivery Note {0} is cancelled”.format(source\_name).

**Local steps**

- Set tuple(docstatus, company) from Platform.db.get\_value(“Delivery Note”, source\_name, list(“docstatus”, “company”)).
- <a id="op-b83d8da8af0906-guard-5"></a>If docstatus equals 2.
  - Call the validation error handler Platform.throw(translated “Delivery Note {0} is cancelled”.format(source\_name)).
- If not target\_doc.
  - Set target\_doc from Platform.new\_doc(“Delivery Trip”).
  - Set target\_doc.company from company.
- Bind local operation update\_address for subsequent calls.
- Set doclist from get\_mapped\_doc(“Delivery Note”, source\_name, mapping(“Delivery Note” → mapping(“doctype” → “Delivery Stop”, “on\_parent” → target\_doc, “field\_map” → mapping(“name” → “delivery\_note”, “contact\_person” → “con ….
- Return doclist.

**Derived branch illustrations**

- At the comparison docstatus equals 2, docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “Delivery Note {0} is cancelled”.format(source\_name). With docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b83d8da8af0906-guard-5)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L234)

<a id="op-6095b716f3666d"></a>
### Make delivery trip.update address

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_delivery_trip_update_address`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Set target\_doc.address from (source\_doc.shipping\_address\_name or source\_doc.customer\_address).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_doc.shipping\_address\_name → source\_doc.customer\_address.
- Set target\_doc.customer\_address from (source\_doc.shipping\_address or source\_doc.address\_display).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_doc.shipping\_address → source\_doc.address\_display.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L235)

<a id="op-f2bba50bd3c44a"></a>
### Make installation note

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_installation_note`

**Inputs** source\_name, target\_doc = no value, kwargs = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind dependencies get\_returned\_serial\_nos.
- Bind dependencies get\_valid\_serial\_nos.
- Set returned\_qty\_map from get\_returned\_qty\_map(source\_name).
- Bind local operation update\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Delivery Note”, source\_name, mapping(“Delivery Note” → mapping(“doctype” → “Installation Note”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Delivery Note Item” → mapping(“doctype” ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L236)

<a id="op-843c80c26b17d5"></a>
### Make installation note.update item

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_installation_note_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set target.qty from ((flt(obj.qty) − flt(returned\_qty\_map.get(obj.name, 0))) − flt(obj.installed\_qty)).
- If obj.serial\_no.
  - Set returned from set(get\_returned\_serial\_nos(obj, source\_parent)).
  - Set target.serial\_no from whitespace '\\n'.join(generator of s for s drawn from get\_valid\_serial\_nos(obj.serial\_no) where s does not belong to returned).
    - Draw s from get\_valid\_serial\_nos(obj.serial\_no), keep a combination only if (s does not belong to returned).
- Otherwise.
  - Set target.serial\_no from obj.serial\_no.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L237)

<a id="op-a207e19220f004"></a>
### Make packing slip

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_packing_slip`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Delivery Note”, source\_name, mapping(“Delivery Note” → mapping(“doctype” → “Packing Slip”, “field\_map” → mapping(“name” → “delivery\_note”, “letter\_head” → “letter\_head”), “validation” → map ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L244)

<a id="op-21dedf5196bcde"></a>
### Make packing slip.set missing values

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_packing_slip_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate target.run\_method(“set\_missing\_values”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L245)

<a id="op-fe016a073f7c50"></a>
### Make packing slip.update item

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_packing_slip_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set target.qty from (flt(obj.qty) − flt(obj.packed\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L246)

<a id="op-b1ea09b6e33ffc"></a>
### Make shipment

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_shipment`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation postprocess for subsequent calls.
- Set doclist from get\_mapped\_doc(“Delivery Note”, source\_name, mapping(“Delivery Note” → mapping(“doctype” → “Shipment”, “field\_map” → mapping(“grand\_total” → “value\_of\_goods”, “company” → “pickup\_company”, “company\_address ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L253)

<a id="op-47c0cb2355903d"></a>
### Make shipment.postprocess

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_shipment_postprocess`

**Inputs** source, target.

**Record and data access** read “User” via get\_value · read “Contact” via get\_value.

**Local steps**

- Evaluate target.append(“shipment\_delivery\_note”, mapping(“delivery\_note” → source.name, “grand\_total” → source.base\_grand\_total)).
- Set user from Platform.db.get\_value(“User”, Platform.session.user, list(“email”, “full\_name”, “phone”, “mobile\_no”), as\_dict = 1).
- Set target.pickup\_contact\_email from user.email.
- Set pickup\_contact\_display from formatted text {user.full\_name}.
- If user.
  - If user.email.
    - Update pickup\_contact\_display using + (text in the contract + user.email).
  - If user.phone.
    - Update pickup\_contact\_display using + (text in the contract + user.phone).
  - If (user.mobile\_no and not user.phone).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in user.mobile\_no → not user.phone.
    - Update pickup\_contact\_display using + (text in the contract + user.mobile\_no).
- Set target.pickup\_contact from pickup\_contact\_display.
- Set target.pickup\_contact\_person from Platform.session.user.
- Set contact\_person from (source.contact\_person or get\_default\_contact(“Customer”, source.customer)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.contact\_person → get\_default\_contact(“Customer”, source.customer).
- If contact\_person.
  - Set contact from Platform.db.get\_value(“Contact”, contact\_person, list(“email\_id”, “phone”, “mobile\_no”), as\_dict = 1).
  - Set delivery\_contact\_display from (source.contact\_display or contact\_person or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.contact\_display → contact\_person → empty text.
  - If (contact and not source.contact\_display).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in contact → not source.contact\_display.
    - If contact.email\_id.
      - Update delivery\_contact\_display using + (text in the contract + contact.email\_id).
    - If contact.phone.
      - Update delivery\_contact\_display using + (text in the contract + contact.phone).
    - If (contact.mobile\_no and not contact.phone).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in contact.mobile\_no → not contact.phone.
      - Update delivery\_contact\_display using + (text in the contract + contact.mobile\_no).
  - Set target.delivery\_contact\_name from contact\_person.
  - If (contact and contact.email\_id and not target.delivery\_contact\_email).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in contact → contact.email\_id → not target.delivery\_contact\_email.
    - Set target.delivery\_contact\_email from contact.email\_id.
  - Set target.delivery\_contact from delivery\_contact\_display.
- If source.shipping\_address\_name.
  - Set target.delivery\_address\_name from source.shipping\_address\_name.
  - Set target.delivery\_address from source.shipping\_address.
- Otherwise.
  - If source.customer\_address.
    - Set target.delivery\_address\_name from source.customer\_address.
    - Set target.delivery\_address from source.address\_display.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L254)

<a id="op-279872e5a7474c"></a>
### Make sales return

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_sales_return`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“Delivery Note”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“Delivery Note”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L252)

<a id="op-6b5e1d35dd7e1d"></a>
### Update delivery note status

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_update_delivery_note_status`

**Inputs** docname, status.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — translated “Only a submitted Delivery Note can be closed or reopened”.

**Local steps**

- Set dn from Platform.get\_lazy\_doc(“Delivery Note”, docname).
- Evaluate dn.check\_permission(“submit”).
- <a id="op-6b5e1d35dd7e1d-guard-4"></a>If dn.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Delivery Note can be closed or reopened”).
- Evaluate dn.update\_status(status).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison dn.docstatus differs from 1, dn.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Delivery Note can be closed or reopened”. With dn.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6b5e1d35dd7e1d-guard-4)

**Values supplied outside this operation** effective access from dn.check\_permission(“submit”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L892)

<a id="op-88c9982b7f9516"></a>
### Make inter company purchase receipt

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_inter_company_purchase_receipt`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_inter\_company\_transaction(“Delivery Note”, source\_name, target\_doc).

**Local steps**

- Return make\_inter\_company\_transaction(“Delivery Note”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L238)

<a id="op-3f38ca81fe27f2"></a>
### Make inter company transaction

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_inter_company_transaction`

**Inputs** doctype, source\_name, target\_doc = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** get\_mapped\_doc(doctype, source\_name, table\_maps, target\_doc, …).

**Local steps**

- Bind dependencies clear\_item\_tax\_template\_of\_other\_company, get\_inter\_company\_details, set\_purchase\_references, update\_address, update\_taxes, validate\_inter\_company\_transaction.
- If doctype equals “Delivery Note”.
  - Set source\_doc from Platform.get\_doc(doctype, source\_name).
  - Set target\_doctype from “Purchase Receipt”.
  - Set source\_document\_warehouse\_field from “target\_warehouse”.
  - Set target\_document\_warehouse\_field from “from\_warehouse”.
- Otherwise.
  - Set source\_doc from Platform.get\_doc(doctype, source\_name).
  - Set target\_doctype from “Delivery Note”.
  - Set source\_document\_warehouse\_field from “from\_warehouse”.
  - Set target\_document\_warehouse\_field from “target\_warehouse”.
- Evaluate validate\_inter\_company\_transaction(source\_doc, doctype).
- Set details from get\_inter\_company\_details(source\_doc, doctype).
- Set accepted\_returns from get\_accepted\_returned\_qty(source\_doc) when doctype equals “Purchase Receipt”, otherwise mapping().
  - Value choice on doctype equals “Purchase Receipt” — true gives get\_accepted\_returned\_qty(source\_doc), false gives mapping().
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_details for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Set bundle\_rows from mapping of d.parent\_detail\_docname → d for d drawn from (source\_doc.get(“packed\_items”) or list()).
  - Draw d from (source\_doc.get(“packed\_items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_doc.get(“packed\_items”) → list().
- Set bundle\_rows from mapping of d.name → d for d drawn from source\_doc.items where d.name belongs to bundle\_rows.
  - Draw d from source\_doc.items, keep a combination only if (d.name belongs to bundle\_rows).
- Set table\_maps from mapping(doctype → mapping(“doctype” → target\_doctype, “validation” → mapping(“docstatus” → list(“=”, 1)), “postprocess” → update\_details, “field\_no\_map” → list(expanded CROSS\_PARTY\_FIELD\_NO\_MAP, “set\_wareh ….
- If (doctype equals “Delivery Note” and bundle\_rows).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “Delivery Note” → bundle\_rows.
  - Set table\_maps at “Packed Item” from get\_component\_receipt\_map(bundle\_rows).
- Return get\_mapped\_doc(doctype, source\_name, table\_maps, target\_doc, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L239)

<a id="op-fdf221af9a7e37"></a>
### Make inter company transaction.set missing values

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_inter_company_transaction_set_missing_values`

**Inputs** source, target.

**Explicit failure paths** validation helper — translated “All items have already been delivered” · validation helper — translated “All items have already been received”.

**Local steps**

- Set target.conversion\_rate, target.plc\_conversion\_rate from 0.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate set\_purchase\_references(target).
- If target.doctype equals “Purchase Receipt”.
  - Set master\_doctype from “Purchase Taxes and Charges Template”.
- Otherwise.
  - Set master\_doctype from “Sales Taxes and Charges Template”.
- If (not target.get(“taxes”) and target.get(“taxes\_and\_charges”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not target.get(“taxes”) → target.get(“taxes\_and\_charges”).
  - For each tax in \_get\_taxes\_and\_charges(master\_doctype, target.get(“taxes\_and\_charges”)).
    - Evaluate target.append(“taxes”, tax).
- If not target.get(“items”).
  - If target.doctype equals “Delivery Note”.
    - Call the validation error handler Platform.throw(translated “All items have already been delivered”).
  - Call the validation error handler Platform.throw(translated “All items have already been received”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L240)

<a id="op-b0feeeb393ec13"></a>
### Make inter company transaction.update details

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_inter_company_transaction_update_details`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Bind local operation \_validate\_address\_link for subsequent calls.
- Set target\_doc.inter\_company\_invoice\_reference from source\_doc.name.
- Evaluate clear\_inapplicable\_terms(target\_doc).
- If target\_doc.doctype equals “Purchase Receipt”.
  - Set target\_doc.company from details.get(“company”).
  - Set target\_doc.supplier from details.get(“party”).
  - Set target\_doc.buying\_price\_list from source\_doc.selling\_price\_list.
  - Set target\_doc.is\_internal\_supplier from 1.
  - Set target\_doc.inter\_company\_reference from source\_doc.name.
  - If (source\_doc.company\_address and \_validate\_address\_link(source\_doc.company\_address, “Supplier”, details.get(“party”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.company\_address → \_validate\_address\_link(source\_doc.company\_address, “Supplier”, details.get(“party”)).
    - Evaluate update\_address(target\_doc, “supplier\_address”, “address\_display”, source\_doc.company\_address).
  - If (source\_doc.dispatch\_address\_name and \_validate\_address\_link(source\_doc.dispatch\_address\_name, “Company”, details.get(“company”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.dispatch\_address\_name → \_validate\_address\_link(source\_doc.dispatch\_address\_name, “Company”, details.get(“company”)).
    - Evaluate update\_address(target\_doc, “dispatch\_address”, “dispatch\_address\_display”, source\_doc.dispatch\_address\_name).
  - If (source\_doc.shipping\_address\_name and \_validate\_address\_link(source\_doc.shipping\_address\_name, “Company”, details.get(“company”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.shipping\_address\_name → \_validate\_address\_link(source\_doc.shipping\_address\_name, “Company”, details.get(“company”)).
    - Evaluate update\_address(target\_doc, “shipping\_address”, “shipping\_address\_display”, source\_doc.shipping\_address\_name).
  - If (source\_doc.customer\_address and \_validate\_address\_link(source\_doc.customer\_address, “Company”, details.get(“company”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.customer\_address → \_validate\_address\_link(source\_doc.customer\_address, “Company”, details.get(“company”)).
    - Evaluate update\_address(target\_doc, “billing\_address”, “billing\_address\_display”, source\_doc.customer\_address).
  - Evaluate update\_taxes(target\_doc, party = target\_doc.supplier, party\_type = “Supplier”, company = target\_doc.company, doctype = target\_doc.doctype, …).
- Otherwise.
  - Set target\_doc.company from details.get(“company”).
  - Set target\_doc.customer from details.get(“party”).
  - Set target\_doc.company\_address from source\_doc.supplier\_address.
  - Set target\_doc.selling\_price\_list from source\_doc.buying\_price\_list.
  - Set target\_doc.is\_internal\_customer from 1.
  - Set target\_doc.inter\_company\_reference from source\_doc.name.
  - If (source\_doc.supplier\_address and \_validate\_address\_link(source\_doc.supplier\_address, “Company”, details.get(“company”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.supplier\_address → \_validate\_address\_link(source\_doc.supplier\_address, “Company”, details.get(“company”)).
    - Evaluate update\_address(target\_doc, “company\_address”, “company\_address\_display”, source\_doc.supplier\_address).
  - If (source\_doc.shipping\_address and \_validate\_address\_link(source\_doc.shipping\_address, “Customer”, details.get(“party”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.shipping\_address → \_validate\_address\_link(source\_doc.shipping\_address, “Customer”, details.get(“party”)).
    - Evaluate update\_address(target\_doc, “shipping\_address\_name”, “shipping\_address”, source\_doc.shipping\_address).
  - If (source\_doc.shipping\_address and \_validate\_address\_link(source\_doc.shipping\_address, “Customer”, details.get(“party”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.shipping\_address → \_validate\_address\_link(source\_doc.shipping\_address, “Customer”, details.get(“party”)).
    - Evaluate update\_address(target\_doc, “customer\_address”, “address\_display”, source\_doc.shipping\_address).
  - Evaluate update\_taxes(target\_doc, party = target\_doc.customer, party\_type = “Customer”, company = target\_doc.company, doctype = target\_doc.doctype, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L241)

<a id="op-e96f7afaec18b2"></a>
### Make inter company transaction.update details.validate address link

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_inter_company_transaction_update_details_validate_address_link`

**Inputs** address, link\_doctype, link\_name.

**Record and data access** read “Dynamic Link” via get\_value.

**Explicit results** Platform.db.get\_value(“Dynamic Link”, mapping(“parent” → address, “parenttype” → “Address”, “link\_doctype” → link\_doctype, “link\_name” → link\_name), “parent”).

**Local steps**

- Return Platform.db.get\_value(“Dynamic Link”, mapping(“parent” → address, “parenttype” → “Address”, “link\_doctype” → link\_doctype, “link\_name” → link\_name), “parent”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L242)
