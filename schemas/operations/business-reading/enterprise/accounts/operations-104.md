# Accounting and settlement · operations 104

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-62cfecbfa2687d"></a>
### Get internal party

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_internal_party`

**Inputs** parties, link\_doctype, doc.

**Record and data access** read “Dynamic Link” via get\_value.

**Explicit results** party.

**Local steps**

- If len(parties) equals 1.
  - Set party from parties at 0.name.
- Otherwise.
  - If (doc.get(“company\_address”) or doc.get(“shipping\_address”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“company\_address”) → doc.get(“shipping\_address”).
    - Set party from Platform.db.get\_value(“Dynamic Link”, mapping(“parent” → (doc.get(“company\_address”) or doc.get(“shipping\_address”)), “parenttype” → “Address”, “link\_doctype” → link\_doctype), “link\_name”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“company\_address”) → doc.get(“shipping\_address”).
    - If not party.
      - Set party from parties at 0.name.
  - Otherwise.
    - Set party from parties at 0.name.
- Return party.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L981)

<a id="op-294362249c9709"></a>
### Validate inter company transaction

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_validate_inter_company_transaction`

**Inputs** doc, doctype.

**Record and data access** read “Price List” via get\_value.

**Explicit failure paths** validation helper — translated “Selected Price List should have buying and selling fields checked.” · validation helper — translated “No {0} found for Inter Company Transactions.”.format(partytype).

**Local steps**

- Set details from get\_inter\_company\_details(doc, doctype).
- Set price\_list from doc.selling\_price\_list when doctype belongs to list(“Sales Invoice”, “Sales Order”, “Delivery Note”), otherwise doc.buying\_price\_list.
  - Value choice on doctype belongs to list(“Sales Invoice”, “Sales Order”, “Delivery Note”) — true gives doc.selling\_price\_list, false gives doc.buying\_price\_list.
- Set valid\_price\_list from Platform.db.get\_value(“Price List”, mapping(“name” → price\_list, “buying” → 1, “selling” → 1)).
- If (not valid\_price\_list and not doc.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not valid\_price\_list → not doc.is\_internal\_transfer().
  - Call the validation error handler Platform.throw(translated “Selected Price List should have buying and selling fields checked.”).
- Set party from details.get(“party”).
- If not party.
  - Set partytype from “Supplier” when doctype belongs to list(“Sales Invoice”, “Sales Order”), otherwise “Customer”.
    - Value choice on doctype belongs to list(“Sales Invoice”, “Sales Order”) — true gives “Supplier”, false gives “Customer”.
  - Call the validation error handler Platform.throw(translated “No {0} found for Inter Company Transactions.”.format(partytype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1073)

<a id="op-00011959d49bd9"></a>
### Validate no counterpart sales invoice

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_validate_no_counterpart_sales_invoice`

**Inputs** purchase\_invoice.

**Explicit failure paths** validation helper — translated “Cannot create Intercompany Sales Invoice. Purchase Invoice {0} already has Sales Invoice {1}.”.format(purchase\_invoice.name, get\_link\_to\_form(“Sales Invoice”, sales\_invoice)).

**Local steps**

- If sales\_invoice bound to purchase\_invoice.inter\_company\_invoice\_reference.
  - Call the validation error handler Platform.throw(translated “Cannot create Intercompany Sales Invoice. Purchase Invoice {0} already has Sales Invoice {1}.”.format(purchase\_invoice.name, get\_link\_to\_form(“Sales Invoice”, sales\_invoice))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1074)

<a id="op-227ba0d5e85277"></a>
### Make inter company purchase invoice

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_inter_company_purchase_invoice`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_inter\_company\_transaction(“Sales Invoice”, source\_name, target\_doc).

**Local steps**

- Return make\_inter\_company\_transaction(“Sales Invoice”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L993)

<a id="op-c7f1b520202627"></a>
### Make regional gl entries

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_make_regional_general_ledger_entries`

**Inputs** gl\_entries, doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** gl\_entries.

**Local steps**

- Return gl\_entries.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L3599) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1141)

<a id="op-4cb4e267866b24"></a>
### Make inter company transaction

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_inter_company_transaction`

**Inputs** doctype, source\_name, target\_doc = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** doclist.

**Explicit failure paths** validation helper — message.format(target\_doctype, doctype, target\_doctype).

**Local steps**

- If doctype belongs to list(“Sales Invoice”, “Sales Order”).
  - Set source\_doc from Platform.get\_doc(doctype, source\_name).
  - Set target\_doctype from “Purchase Invoice” when doctype equals “Sales Invoice”, otherwise “Purchase Order”.
    - Value choice on doctype equals “Sales Invoice” — true gives “Purchase Invoice”, false gives “Purchase Order”.
  - Set target\_detail\_field from “sales\_invoice\_item” when doctype equals “Sales Invoice”, otherwise “sales\_order\_item”.
    - Value choice on doctype equals “Sales Invoice” — true gives “sales\_invoice\_item”, false gives “sales\_order\_item”.
  - Set source\_document\_warehouse\_field from “target\_warehouse”.
  - Set target\_document\_warehouse\_field from “from\_warehouse”.
  - Set received\_items from get\_received\_items(source\_name, target\_doctype, target\_detail\_field).
- Otherwise.
  - Set source\_doc from Platform.get\_doc(doctype, source\_name).
  - Set target\_doctype from “Sales Invoice” when doctype equals “Purchase Invoice”, otherwise “Sales Order”.
    - Value choice on doctype equals “Purchase Invoice” — true gives “Sales Invoice”, false gives “Sales Order”.
  - Set source\_document\_warehouse\_field from “from\_warehouse”.
  - Set target\_document\_warehouse\_field from “target\_warehouse”.
  - Set received\_items from get\_received\_items(source\_name, “Sales Order”, “purchase\_order\_item”) when doctype equals “Purchase Order”, otherwise mapping().
    - Value choice on doctype equals “Purchase Order” — true gives get\_received\_items(source\_name, “Sales Order”, “purchase\_order\_item”), false gives mapping().
- If doctype differs from “Purchase Invoice”.
  - Evaluate validate\_not\_made\_from\_counterpart(source\_doc, target\_doctype, received\_items).
- Evaluate validate\_inter\_company\_transaction(source\_doc, doctype).
- Set details from get\_inter\_company\_details(source\_doc, doctype).
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_details for subsequent calls.
- Bind local operation get\_pending\_qty for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Set item\_field\_map from mapping(“doctype” → (target\_doctype + “ Item”), “field\_no\_map” → list(“income\_account”, “expense\_account”, “cost\_center”, “warehouse”), “field\_map” → mapping(“rate” → “rate”), “postprocess” → update\_item, …).
- If doctype belongs to list(“Sales Invoice”, “Sales Order”).
  - Evaluate item\_field\_map at “field\_map”.update(mapping(“name” → target\_detail\_field)).
- If source\_doc.get(“update\_stock”).
  - Evaluate item\_field\_map at “field\_map”.update(mapping(source\_document\_warehouse\_field → target\_document\_warehouse\_field, “batch\_no” → “batch\_no”, “serial\_no” → “serial\_no”)).
- Otherwise.
  - If target\_doctype equals “Sales Order”.
    - Evaluate item\_field\_map at “field\_map”.update(mapping(source\_document\_warehouse\_field → “warehouse”)).
- Set doclist from get\_mapped\_doc(doctype, source\_name, mapping(doctype → mapping(“doctype” → target\_doctype, “validation” → mapping(“docstatus” → list(“=”, 1)), “postprocess” → update\_details, “set\_target\_warehouse” → “set\_ ….
- If doctype equals “Purchase Invoice”.
  - Evaluate validate\_no\_counterpart\_sales\_invoice(source\_doc).
- If not doclist.get(“items”).
  - If target\_doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
    - Set message from translated “Cannot create Intercompany {0}. All items in the source {1} have already been fully invoiced. Please check t …”.
  - Otherwise.
    - Set message from translated “Cannot create Intercompany {0}. All items in the source {1} have already been fully ordered. Please check th …”.
  - Call the validation error handler Platform.throw(message.format(target\_doctype, doctype, target\_doctype)).
- Return doclist.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L994)

<a id="op-3185b73f9c0060"></a>
### Make inter company transaction.set missing values

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_inter_company_transaction_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.conversion\_rate, target.plc\_conversion\_rate from 0.
- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate set\_purchase\_references(target).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L996)

<a id="op-7ced51d361ac1e"></a>
### Make inter company transaction.update details

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_inter_company_transaction_update_details`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Bind local operation \_validate\_address\_link for subsequent calls.
- Set tuple(\_, reference\_field) from get\_inter\_company\_counterpart(target\_doc.doctype).
- Evaluate target\_doc.set(reference\_field, source\_doc.name).
- Evaluate clear\_inapplicable\_terms(target\_doc).
- If target\_doc.doctype belongs to list(“Purchase Invoice”, “Purchase Order”).
  - Set target\_doc.company from details.get(“company”).
  - Set target\_doc.supplier from details.get(“party”).
  - Set target\_doc.is\_internal\_supplier from 1.
  - Set target\_doc.ignore\_pricing\_rule from 1.
  - Set target\_doc.buying\_price\_list from source\_doc.selling\_price\_list.
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
  - Set target\_doc.selling\_price\_list from source\_doc.buying\_price\_list.
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

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L997)

<a id="op-8a4cbb9ac7813e"></a>
### Make inter company transaction.update details.validate address link

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_inter_company_transaction_update_details_validate_address_link`

**Inputs** address, link\_doctype, link\_name.

**Record and data access** read “Dynamic Link” via get\_value.

**Explicit results** Platform.db.get\_value(“Dynamic Link”, mapping(“parent” → address, “parenttype” → “Address”, “link\_doctype” → link\_doctype, “link\_name” → link\_name), “parent”).

**Local steps**

- Return Platform.db.get\_value(“Dynamic Link”, mapping(“parent” → address, “parenttype” → “Address”, “link\_doctype” → link\_doctype, “link\_name” → link\_name), “parent”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L998)

<a id="op-60114631991558"></a>
### Make inter company transaction.get pending qty

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_inter_company_transaction_get_pending_qty`

**Inputs** row.

**Explicit results** flt(row.qty) · flt((max(pending\_stock\_qty, 0) ÷ (flt(row.conversion\_factor) or 1)), row.precision(“qty”)).

**Local steps**

- Set received\_stock\_qty from received\_items.get(row.name, 0.0).
- If not received\_stock\_qty.
  - Return flt(row.qty).
- Set pending\_stock\_qty from flt((flt(row.stock\_qty) − received\_stock\_qty), row.precision(“stock\_qty”)).
- Return flt((max(pending\_stock\_qty, 0) ÷ (flt(row.conversion\_factor) or 1)), row.precision(“qty”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.conversion\_factor) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L995)

<a id="op-d53d9325ca22f4"></a>
### Make inter company transaction.update item

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_inter_company_transaction_update_item`

**Inputs** source, target, source\_parent.

**Local steps**

- Set target.qty from get\_pending\_qty(source).
- If (source.doctype equals “Purchase Order Item” and target.doctype equals “Sales Order Item”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source.doctype equals “Purchase Order Item” → target.doctype equals “Sales Order Item”.
  - Set target.purchase\_order from source.parent.
  - Set target.purchase\_order\_item from source.name.
  - Set target.material\_request from source.material\_request.
  - Set target.material\_request\_item from source.material\_request\_item.
- If (source.get(“purchase\_order”) and source.get(“purchase\_order\_item”) and target.doctype equals “Purchase Invoice Item”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source.get(“purchase\_order”) → source.get(“purchase\_order\_item”) → target.doctype equals “Purchase Invoice Item”.
  - Set target.purchase\_order from source.purchase\_order.
  - Set target.po\_detail from source.purchase\_order\_item.
- If ((source.get(“serial\_no”) or source.get(“batch\_no”)) and not source.get(“serial\_and\_batch\_bundle”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (source.get(“serial\_no”) or source.get(“batch\_no”)) → not source.get(“serial\_and\_batch\_bundle”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.get(“serial\_no”) → source.get(“batch\_no”).
  - Set target.use\_serial\_batch\_fields from 1.
- Evaluate clear\_item\_tax\_template\_of\_other\_company(target, details.get(“company”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L999)

<a id="op-079e2019ea276e"></a>
### Validate not made from counterpart

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_validate_not_made_from_counterpart`

**Inputs** source\_doc, target\_doctype, received\_items.

**Explicit failure paths** validation helper — translated “Cannot create Intercompany {0}. {1} {2} was created from {0} {3}.”.format(target\_doctype, source\_doc.doctype, source\_doc.name, get\_link\_to\_form(target\_doctype, reference)).

**Local steps**

- Set reference\_field from get\_inter\_company\_counterpart(source\_doc.doctype) at 1.
- Set reference from source\_doc.get(reference\_field).
- If (reference and not any(generator of row.name belongs to received\_items for row drawn from source\_doc.items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference → not any(generator of row.name belongs to received\_items for row drawn from source\_doc.items).
  - Draw row from source\_doc.items.
  - Call the validation error handler Platform.throw(translated “Cannot create Intercompany {0}. {1} {2} was created from {0} {3}.”.format(target\_doctype, source\_doc.doctype, source\_doc.name, get\_link\_to\_form(target\_doctype, reference))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1075)

<a id="op-dea719417be843"></a>
### Clear item tax template of other company

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_clear_item_tax_template_of_other_company`

**Inputs** item, company.

**Record and data access** read “Item Tax Template” via get\_cached\_value.

**Local steps**

- If (item.get(“item\_tax\_template”) and Platform.get\_cached\_value(“Item Tax Template”, item.item\_tax\_template, “company”) differs from company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“item\_tax\_template”) → Platform.get\_cached\_value(“Item Tax Template”, item.item\_tax\_template, “company”) differs from company.
  - Set item.item\_tax\_template from no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item Tax Template”, item.item\_tax\_template, “company”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L971)

<a id="op-ade675ba2ff7de"></a>
### Get received items

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_received_items`

**Inputs** reference\_name, doctype, reference\_fieldname.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** received\_items\_map.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid doctype {0}”.format(doctype) · validation helper with Platform.ValidationError — translated “{0} is not a valid reference field for {1}”.format(reference\_fieldname, doctype).

**Local steps**

- Set reference\_fields from mapping(“Purchase Invoice” → tuple(“inter\_company\_invoice\_reference”, “Sales Invoice”, “sales\_invoice\_item”), “Purchase Order” → tuple(“inter\_company\_order\_reference”, “Sales Order”, “sales\_order\_item”), “ ….
- If doctype does not belong to reference\_fields.
  - Call the validation error handler Platform.throw(translated “Invalid doctype {0}”.format(doctype), Platform.PermissionError).
- Set tuple(reference\_field, source\_doctype, expected\_fieldname) from reference\_fields at doctype.
- Evaluate Platform.has\_permission(source\_doctype, doc = reference\_name, throw = true).
- If reference\_fieldname differs from expected\_fieldname.
  - Call the validation error handler Platform.throw(translated “{0} is not a valid reference field for {1}”.format(reference\_fieldname, doctype), Platform.ValidationError).
- Set received\_items\_map from mapping().
- For each item in get\_inter\_company\_items(doctype, mapping(reference\_field → reference\_name), reference\_fieldname, list(“stock\_qty”)).
  - Set key from item.get(reference\_fieldname).
  - If key.
    - Set received\_items\_map at key from (received\_items\_map.get(key, 0.0) + flt(item.stock\_qty)).
- Return received\_items\_map.

**Values supplied outside this operation** effective access from Platform.has\_permission(source\_doctype, doc = reference\_name, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L985)

<a id="op-d6a7b4202dcc8c"></a>
### Get inter company items

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_inter_company_items`

**Inputs** doctype, filters, reference\_fieldname, fields.

**Record and data access** read doctype via get\_all · read (doctype + “ Item”) via get\_all.

**Explicit results** list() · items.

**Local steps**

- Set parents from Platform.get\_all(doctype, filters = mapping(expand filters, “docstatus” → 1), pluck = “name”).
- If not parents.
  - Return list().
- Set fields from list(“name”, reference\_fieldname, expanded fields).
- If doctype equals “Purchase Invoice”.
  - Update parents using + Platform.get\_all(doctype, filters = mapping(“return\_against” → tuple(“in”, parents), “docstatus” → 1), pluck = “name”).
  - Evaluate fields.append(“purchase\_invoice\_item”).
- Set items from Platform.get\_all((doctype + “ Item”), filters = mapping(“parent” → tuple(“in”, parents)), fields = fields).
- Set reference\_by\_row from mapping of item.name → item.get(reference\_fieldname) for item drawn from items.
  - Draw item from items.
- For each item in items.
  - Set item at reference\_fieldname from (reference\_by\_row at item.name or reference\_by\_row.get(item.get(“purchase\_invoice\_item”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_by\_row at item.name → reference\_by\_row.get(item.get(“purchase\_invoice\_item”)).
- Return items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L980)

<a id="op-790340c3acffff"></a>
### Set purchase references

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_set_purchase_references`

**Inputs** doc.

**Local steps**

- If doc.is\_internal\_transfer().
  - If doc.doctype equals “Purchase Receipt”.
    - Set so\_item\_map from get\_delivery\_note\_details(doc.inter\_company\_invoice\_reference).
    - If so\_item\_map.
      - Set tuple(pd\_item\_map, parent\_child\_map, warehouse\_map) from get\_pd\_details(“Purchase Order Item”, so\_item\_map, “sales\_order\_item”).
      - Evaluate update\_pr\_items(doc, so\_item\_map, pd\_item\_map, parent\_child\_map, …).
  - Otherwise.
    - If doc.doctype equals “Purchase Invoice”.
      - Set tuple(dn\_item\_map, so\_item\_map) from get\_sales\_invoice\_details(doc.inter\_company\_invoice\_reference).
      - If list(dn\_item\_map.values()).
        - Set tuple(pd\_item\_map, parent\_child\_map, warehouse\_map) from get\_pd\_details(“Purchase Receipt Item”, dn\_item\_map, “delivery\_note\_item”).
        - Evaluate update\_pi\_items(doc, “pr\_detail”, “purchase\_receipt”, dn\_item\_map, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1063)

<a id="op-3f3ef4cc1ecb39"></a>
### Update pi items

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_update_pi_items`

**Inputs** doc, detail\_field, parent\_field, sales\_item\_map, purchase\_item\_map, parent\_child\_map, warehouse\_map.

**Record and data access** read “Purchase Order Item” via get\_value.

**Local steps**

- For each item in doc.get(“items”).
  - Evaluate item.set(detail\_field, purchase\_item\_map.get(sales\_item\_map.get(item.sales\_invoice\_item))).
  - Evaluate item.set(parent\_field, parent\_child\_map.get(sales\_item\_map.get(item.sales\_invoice\_item))).
  - If doc.update\_stock.
    - Set item.warehouse from warehouse\_map.get(sales\_item\_map.get(item.sales\_invoice\_item)).
    - If (not item.warehouse and item.get(“purchase\_order”) and item.get(“purchase\_order\_item”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.warehouse → item.get(“purchase\_order”) → item.get(“purchase\_order\_item”).
      - Set item.warehouse from Platform.db.get\_value(“Purchase Order Item”, item.purchase\_order\_item, “warehouse”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1069)

<a id="op-520f5729fbf1ba"></a>
### Update pr items

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_update_pr_items`

**Inputs** doc, sales\_item\_map, purchase\_item\_map, parent\_child\_map, warehouse\_map.

**Record and data access** read “Purchase Order Item” via get\_value.

**Local steps**

- For each item in doc.get(“items”).
  - Set item.warehouse from warehouse\_map.get(sales\_item\_map.get(item.delivery\_note\_item)).
  - If (not item.warehouse and item.get(“purchase\_order”) and item.get(“purchase\_order\_item”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.warehouse → item.get(“purchase\_order”) → item.get(“purchase\_order\_item”).
    - Set item.warehouse from Platform.db.get\_value(“Purchase Order Item”, item.purchase\_order\_item, “warehouse”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1070)

<a id="op-858c7950fc6561"></a>
### Get delivery note details

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_delivery_note_details`

**Inputs** internal\_reference.

**Record and data access** read “Delivery Note Item” via get\_all.

**Explicit results** mapping of d.name → d.so\_detail for d drawn from si\_item\_details where d.so\_detail.

**Local steps**

- Set si\_item\_details from Platform.get\_all(“Delivery Note Item”, fields = list(“name”, “so\_detail”), filters = mapping(“parent” → internal\_reference)).
- Return mapping of d.name → d.so\_detail for d drawn from si\_item\_details where d.so\_detail.
  - Draw d from si\_item\_details, keep a combination only if (d.so\_detail).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L976)

<a id="op-8627e21606fece"></a>
### Get sales invoice details

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_sales_invoice_details`

**Inputs** internal\_reference.

**Record and data access** read “Sales Invoice Item” via get\_all.

**Explicit results** tuple(dn\_item\_map, so\_item\_map).

**Local steps**

- Set dn\_item\_map from mapping().
- Set so\_item\_map from mapping().
- Set si\_item\_details from Platform.get\_all(“Sales Invoice Item”, fields = list(“name”, “so\_detail”, “dn\_detail”), filters = mapping(“parent” → internal\_reference)).
- For each d in si\_item\_details.
  - If d.dn\_detail.
    - Evaluate dn\_item\_map.setdefault(d.name, d.dn\_detail).
  - If d.so\_detail.
    - Evaluate so\_item\_map.setdefault(d.name, d.so\_detail).
- Return tuple(dn\_item\_map, so\_item\_map).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L986)

<a id="op-6388e2aa85ed0d"></a>
### Get pd details

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_pd_details`

**Inputs** doctype, sd\_detail\_map, sd\_detail\_field.

**Record and data access** read doctype via get\_all.

**Explicit results** tuple(pd\_item\_map, parent\_child\_map, accepted\_warehouse\_map).

**Local steps**

- Set pd\_item\_map from mapping().
- Set accepted\_warehouse\_map from mapping().
- Set parent\_child\_map from mapping().
- Set pd\_item\_details from Platform.get\_all(doctype, fields = list(sd\_detail\_field, “name”, “warehouse”, “parent”), filters = mapping(sd\_detail\_field → tuple(“in”, list(sd\_detail\_map.values())))).
- For each d in pd\_item\_details.
  - Evaluate pd\_item\_map.setdefault(d.get(sd\_detail\_field), d.name).
  - Evaluate parent\_child\_map.setdefault(d.get(sd\_detail\_field), d.parent).
  - Evaluate accepted\_warehouse\_map.setdefault(d.get(sd\_detail\_field), d.warehouse).
- Return tuple(pd\_item\_map, parent\_child\_map, accepted\_warehouse\_map).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L984)

<a id="op-8d5363886a3594"></a>
### Update taxes

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_update_taxes`

**Inputs** doc, party = no value, party\_type = no value, company = no value, doctype = no value, party\_address = no value, company\_address = no value, shipping\_address\_name = no value, master\_doctype = no value.

**Local steps**

- Set party\_details from get\_party\_details(party = party, party\_type = party\_type, company = company, doctype = doctype, …).
- Set doc.taxes\_and\_charges from party\_details.get(“taxes\_and\_charges”).
- Evaluate doc.set(“taxes”, party\_details.get(“taxes”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1071)

<a id="op-94e8816f3fb964"></a>
### Update address

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_update_address`

**Inputs** doc, address\_field, address\_display\_field, address\_name.

**Local steps**

- Evaluate doc.set(address\_field, address\_name).
- Set fetch\_values from get\_fetch\_values(doc.doctype, address\_field, address\_name).
- For each tuple(key, value) in fetch\_values.items().
  - Evaluate doc.set(key, value).
- Evaluate doc.set(address\_display\_field, get\_address\_display(doc.get(address\_field))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1065)

<a id="op-a844824038af3d"></a>
### Get loyalty programs

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_get_loyalty_programs`

**Inputs** customer.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Customer” via get\_doc.

**State and service calls** call db\_set on customer.

**Explicit results** list(customer.loyalty\_program) · lp\_details.

**Local steps**

- Bind dependencies get\_loyalty\_programs.
- Evaluate Platform.has\_permission(“Customer”, “read”, customer, throw = true).
- Set customer from Platform.get\_doc(“Customer”, customer).
- If customer.loyalty\_program.
  - Return list(customer.loyalty\_program).
- Set lp\_details from get\_loyalty\_programs(customer).
- If (len(lp\_details) equals 1 and customer.has\_permission(“write”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(lp\_details) equals 1 → customer.has\_permission(“write”).
  - Evaluate customer.db\_set(“loyalty\_program”, lp\_details at 0).
  - Return lp\_details.
- Otherwise.
  - Return lp\_details.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, “read”, customer, throw = true), customer.has\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1140)
