# Sales · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Proforma invoice

[Record definition](../../../../data/record-types/proforma_invoice.json)

<a id="op-337e7654348687"></a>
### Proforma Totals.calculate item values

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformatotals_calculate_item_values`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Evaluate super().calculate\_item\_values().
- If self.discount\_amount\_applied.
  - Return no value.
- For each item in self.doc.items.
  - Set item.amount, item.net\_amount from flt(self.amounts at item.name, item.precision(“amount”)).
  - Evaluate self.\_set\_in\_company\_currency(item, list(“amount”, “net\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1503)

<a id="op-6e048a0c7ecde7"></a>
### Get sales order items

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_get_sales_order_items`

**Inputs** sales\_order.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Explicit results** list of mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “description” → item.description, “uom” → item.uom, …) for item drawn from sales\_order\_doc.items.

**Local steps**

- Set sales\_order\_doc from Platform.get\_doc(“Sales Order”, sales\_order, check\_permission = “read”).
- Set proformed from get\_proformed\_totals(sales\_order).
- Return list of mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “description” → item.description, “uom” → item.uom, …) for item drawn from sales\_order\_doc.items.
  - Draw item from sales\_order\_doc.items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1231)

<a id="op-ce14addde63862"></a>
### Get proformed totals

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_get_proformed_totals`

**Inputs** sales\_order.

**Declared result** dict at tuple(str, dict).

**Record and data access** read “Proforma Invoice” via get\_all.

**Explicit results** mapping() · mapping of row.so\_detail → mapping(“qty” → flt(row.qty), “amount” → flt(row.amount)) for row drawn from rows.

**Local steps**

- Set proformas from Platform.get\_all(“Proforma Invoice”, filters = mapping(“sales\_order” → sales\_order, “docstatus” → 1), pluck = “name”).
- If not proformas.
  - Return mapping().
- Set item from Platform.qb.DocType(“Proforma Invoice Item”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(proformas)).groupby(item.so\_detail). ….
- Return mapping of row.so\_detail → mapping(“qty” → flt(row.qty), “amount” → flt(row.amount)) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0630.json#L6420) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1230)

<a id="op-52d431eed21f08"></a>
### Make proforma invoice

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_make_proforma_invoice`

**Inputs** sales\_order, items, based\_on = “Quantity”, hide\_item\_qty = 0, naming\_series = no value, print\_format = no value, letter\_head = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** read “Selling Settings” via get\_single\_value.

**State and service calls** request new\_doc for “Proforma Invoice” · call insert on proforma · call submit on proforma.

**Explicit results** proforma.name.

**Explicit failure paths** validation helper — translated “Please enter a quantity or amount for at least one item.”.

**Local steps**

- Evaluate validate\_feature\_enabled().
- Set proforma from Platform.new\_doc(“Proforma Invoice”).
- Set proforma.sales\_order from sales\_order.
- Set proforma.based\_on from based\_on.
- Set proforma.hide\_item\_qty from 1 when (based\_on equals “Amount” and int((hide\_item\_qty or 0))), otherwise 0.
  - Value choice on (based\_on equals “Amount” and int((hide\_item\_qty or 0))) — true gives 1, false gives 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in based\_on equals “Amount” → int((hide\_item\_qty or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hide\_item\_qty → 0.
- If naming\_series.
  - Set proforma.naming\_series from naming\_series.
- Set proforma.print\_format from (print\_format or Platform.db.get\_single\_value(“Selling Settings”, “default\_proforma\_print\_format”) or “Proforma Invoice”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format → Platform.db.get\_single\_value(“Selling Settings”, “default\_proforma\_print\_format”) → “Proforma Invoice”.
- Set proforma.letter\_head from letter\_head.
- For each row in Platform.parse\_json(items).
  - Evaluate proforma.append(“items”, mapping(“so\_detail” → row.get(“so\_detail”), “qty” → row.get(“qty”), “amount” → row.get(“amount”), “description” → row.get(“description”))).
- If not proforma.items.
  - Call the validation error handler Platform.throw(translated “Please enter a quantity or amount for at least one item.”).
- Evaluate proforma.insert().
- Evaluate proforma.submit().
- Return proforma.name.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings”, “default\_proforma\_print\_format”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1232)

<a id="op-bbdecc48e59836"></a>
### Send proforma email

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_send_proforma_email`

**Inputs** proforma\_name, recipients.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** resolve a document from “Proforma Invoice” via get\_doc · read “File” via get\_value.

**State and service calls** sendmail · call db\_set on proforma.

**Explicit failure paths** validation helper — translated “Only an issued Proforma Invoice can be emailed.” · validation helper — translated “This Proforma Invoice has no PDF to send.” · validation helper — translated “The attached PDF file could not be found.”.

**Local steps**

- Set proforma from Platform.get\_doc(“Proforma Invoice”, proforma\_name).
- Evaluate proforma.check\_permission(“email”).
- <a id="op-bbdecc48e59836-guard-4"></a>If proforma.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only an issued Proforma Invoice can be emailed.”).
- If not proforma.proforma\_pdf.
  - Call the validation error handler Platform.throw(translated “This Proforma Invoice has no PDF to send.”).
- Set file\_name from Platform.db.get\_value(“File”, mapping(“file\_url” → proforma.proforma\_pdf, “attached\_to\_doctype” → proforma.doctype, “attached\_to\_name” → proforma.name), “name”).
- If not file\_name.
  - Call the validation error handler Platform.throw(translated “The attached PDF file could not be found.”).
- Set tuple(subject, message) from proforma.get\_email\_content().
- Evaluate Platform.sendmail(recipients = list of email.strip() for email drawn from recipients.split(“,”) where email.strip(), subject = subject, message = message, attachments = list(mapping(“fid” → file\_name))).
  - Draw email from recipients.split(“,”), keep a combination only if (email.strip()).
- Evaluate proforma.db\_set(“sent\_on”, now()).
- Evaluate proforma.db\_set(“emailed\_to”, recipients).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison proforma.docstatus differs from 1, proforma.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only an issued Proforma Invoice can be emailed.”. With proforma.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-bbdecc48e59836-guard-4)

**Values supplied outside this operation** effective access from proforma.check\_permission(“email”) · service or queued work from Platform.sendmail(recipients = list of email.strip() for email drawn from recipients.split(“,”) where email.strip(), subject = subject, message = message, attachments = list(mapping(“fid” → file\_name))) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1240)

<a id="op-7369d1306365fe"></a>
### Set proforma line

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_set_proforma_line`

**Inputs** item, line.

**Declared result** no value.

**Local steps**

- Set item.qty from line.qty.
- Set item.rate from line.rate.
- Set item.price\_list\_rate from line.rate.
- Set item.description from line.description.
- Set item.pricing\_rules from no value.
- Set item.margin\_type from no value.
- Set item.margin\_rate\_or\_amount from 0.
- Set item.discount\_amount from 0.
- Set item.discount\_percentage from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1506)

<a id="op-5a541299de3fe7"></a>
### Prorate fixed charges

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_prorate_fixed_charges`

**Inputs** sales\_order, share.

**Declared result** no value.

**Local steps**

- If not sales\_order.additional\_discount\_percentage.
  - Set sales\_order.discount\_amount from flt((flt(sales\_order.discount\_amount) × share), sales\_order.precision(“discount\_amount”)).
- For each tax in sales\_order.taxes.
  - If tax.charge\_type equals “Actual”.
    - Set tax.tax\_amount from flt((flt(tax.tax\_amount) × share), tax.precision(“tax\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1505)

<a id="op-02e2d61ef52f8e"></a>
### Validate feature enabled

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_validate_feature_enabled`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Proforma Invoice is not enabled in Selling Settings.”.

**Local steps**

- If not Platform.db.get\_single\_value(“Selling Settings”, “enable\_proforma\_invoice”).
  - Call the validation error handler Platform.throw(translated “Proforma Invoice is not enabled in Selling Settings.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings”, “enable\_proforma\_invoice”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0631.json#L2044) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1866) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1241)

## Record · Quotation

[Record definition](../../../../data/record-types/quotation.json)

<a id="op-9e48a039cb1fc7"></a>
### Quotation.set indicator

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_set_indicator`

**Inputs** self.

**Local steps**

- <a id="op-9e48a039cb1fc7-guard-2"></a>If self.docstatus equals 1.
  - Set self.indicator\_color from “blue”.
  - Set self.indicator\_title from “Submitted”.
- If (self.valid\_till and getdate(self.valid\_till) &lt; getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valid\_till → getdate(self.valid\_till) &lt; getdate(nowdate()).
  - Set self.indicator\_color from “gray”.
  - Set self.indicator\_title from “Expired”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 1, self.docstatus = 1 (submitted) selects the branch that assigns “blue” to self.indicator\_color. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9e48a039cb1fc7-guard-2)

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0632.json#L6285) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1272)

<a id="op-78f291348e9735"></a>
### Quotation.before validate

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_has\_unit\_price\_items().
- Set self.flags.allow\_zero\_qty from self.has\_unit\_price\_items.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set has unit price items](operations-011.md#op-59d4d909ae5df4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0632.json#L6486) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1881) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1256)

<a id="op-b35f5c5e213ce3"></a>
### Quotation.validate

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- Evaluate self.set\_status().
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.set\_default\_valid\_till().
- Evaluate self.validate\_valid\_till().
- Evaluate self.validate\_lead().
- If self.coupon\_code.
  - Set customer from get\_existing\_customer\_name(self.quotation\_to, self.party\_name).
  - Evaluate validate\_coupon\_code(self.coupon\_code, customer).
- Evaluate self.set\_customer\_name().
- If self.items.
  - Set self.with\_items from 1.
- Bind dependencies make\_packing\_list.
- Evaluate make\_packing\_list(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default valid till](operations-011.md#op-a28734d7e6da3f), [validate valid till](operations-011.md#op-6c81d69942a6bb), [validate lead](operations-011.md#op-38a0bbbd7f5c80), [set customer name](operations-012.md#op-e4313b801a005c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1276)

<a id="op-856b464ebe1c79"></a>
### Quotation.after insert

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.carry\_forward\_communication().

If control reaches the end, it returns no value.

**Methods declared on this owner** [carry forward communication](operations-012.md#op-f03128ccb05406).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0632.json#L6810) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1254)

<a id="op-cfa3cb3b5e7735"></a>
### Quotation.before submit

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_has\_alternative\_item().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set has alternative item](operations-011.md#op-3fb68c6d7c63db).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0632.json#L6861) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1880) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1255)

<a id="op-a28734d7e6da3f"></a>
### Quotation.set default valid till

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_quotation_set_default_valid_till`

**Inputs** self.

**Record and data access** read “CRM Settings” via get\_single\_value.

**Local steps**

- Set validity\_days from cint(Platform.get\_single\_value(“CRM Settings”, “default\_valid\_till”)).
- If (self.is\_new() and not self.valid\_till and validity\_days &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not self.valid\_till → validity\_days &gt; 0.
  - Set self.valid\_till from add\_days(self.transaction\_date, validity\_days).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“CRM Settings”, “default\_valid\_till”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L15)

<a id="op-6c81d69942a6bb"></a>
### Quotation.validate valid till

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_validate_valid_till`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Valid till date cannot be before transaction date”.

**Local steps**

- If (self.valid\_till and getdate(self.valid\_till) &lt; getdate(self.transaction\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valid\_till → getdate(self.valid\_till) &lt; getdate(self.transaction\_date).
  - Call the validation error handler Platform.throw(translated “Valid till date cannot be before transaction date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0632.json#L6912) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1277)

<a id="op-38a0bbbd7f5c80"></a>
### Quotation.validate lead

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_quotation_validate_lead`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_lead\_is\_enabled.
- If (self.quotation\_to equals “Lead” and self.party\_name and self.is\_new() and not self.amended\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.quotation\_to equals “Lead” → self.party\_name → self.is\_new() → not self.amended\_from.
  - Evaluate validate\_lead\_is\_enabled(self.party\_name, self.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L16)

<a id="op-3fb68c6d7c63db"></a>
### Quotation.set has alternative item

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_set_has_alternative_item`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not any(generator of row.is\_alternative for row drawn from self.get(“items”)).
  - Draw row from self.get(“items”).
  - Return no value.
- Set items\_with\_alternatives from self.get\_rows\_with\_alternatives().
- For each row in self.get(“items”).
  - If (not row.is\_alternative and row.name belongs to items\_with\_alternatives).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.is\_alternative → row.name belongs to items\_with\_alternatives.
    - Set row.has\_alternative\_item from 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rows with alternatives](operations-012.md#op-fa8957c1427295).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0632.json#L7053) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1896) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1270)

<a id="op-59d4d909ae5df4"></a>
### Quotation.set has unit price items

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_set_has_unit_price_items`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_quotation”).
  - Return no value.
- Set self.has\_unit\_price\_items from any(generator of not row.qty for row drawn from self.get(“items”) where (row.item\_code and not row.qty)).
  - Draw row from self.get(“items”), keep a combination only if ((row.item\_code and not row.qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → not row.qty.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_quotation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0632.json#L7284) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1897) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1271)

<a id="op-83466582d7d32f"></a>
### Quotation.get ordered status

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_get_ordered_status`

**Inputs** self.

**Explicit results** “Open” · “Partially Ordered” · “Ordered”.

**Local steps**

- Set ordered\_items from get\_ordered\_items(self.name).
- If not ordered\_items.
  - Return “Open”.
- Set self.\_items from self.get\_valid\_items() when any(generator of row.is\_alternative for row drawn from self.get(“items”)), otherwise self.get(“items”).
  - Value choice on any(generator of row.is\_alternative for row drawn from self.get(“items”)) — true gives self.get\_valid\_items(), false gives self.get(“items”).
  - Draw row from self.get(“items”).
- For each row in self.\_items.
  - If (row.name does not belong to ordered\_items or row.stock\_qty &gt; ordered\_items at row.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.name does not belong to ordered\_items → row.stock\_qty &gt; ordered\_items at row.name.
    - Return “Partially Ordered”.
- Return “Ordered”.

**Methods declared on this owner** [get valid items](operations-011.md#op-fd79144c5c8180).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1259)

<a id="op-fd79144c5c8180"></a>
### Quotation.get valid items

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_get_valid_items`

**Inputs** self.

**Explicit results** valid\_items.

**Local steps**

- Bind local operation is\_in\_sales\_order for subsequent calls.
- Set valid\_items from list().
- Set alternatives\_set from list().
- Bind local operation collapse\_set for subsequent calls.
- For each row in self.get(“items”).
  - If row.has\_alternative\_item.
    - Evaluate collapse\_set().
    - Set alternatives\_set from list(row).
  - Otherwise.
    - If row.is\_alternative.
      - Evaluate alternatives\_set.append(row).
    - Otherwise.
      - Evaluate collapse\_set().
      - Set alternatives\_set from list().
      - Evaluate valid\_items.append(row).
- Evaluate collapse\_set().
- Return valid\_items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1886) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1261)

<a id="op-daaa8360652c17"></a>
### Quotation.get valid items.is in sales order

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_get_valid_items_is_in_sales_order`

**Inputs** row.

**Record and data access** read “Sales Order Item” via exists.

**Explicit results** bool(Platform.db.exists(“Sales Order Item”, mapping(“quotation\_item” → row.name, “item\_code” → row.item\_code, “docstatus” → 1))).

**Local steps**

- Return bool(Platform.db.exists(“Sales Order Item”, mapping(“quotation\_item” → row.name, “item\_code” → row.item\_code, “docstatus” → 1))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1888) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1262)

<a id="op-b36caf58557276"></a>
### Quotation.get valid items.collapse set

`operation_enterprise_binding_enterprise_selling_doctype_quotation_quotation_quotation_get_valid_items_collapse_set`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not alternatives\_set.
  - Return no value.
- Set ordered\_rows from list of row for row drawn from alternatives\_set where is\_in\_sales\_order(row).
  - Draw row from alternatives\_set, keep a combination only if (is\_in\_sales\_order(row)).
- Evaluate valid\_items.extend((ordered\_rows or alternatives\_set at slice no value to 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ordered\_rows → alternatives\_set at slice no value to 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L14)

<a id="op-8b27b5ee925b65"></a>
### Quotation.is fully ordered

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_is_fully_ordered`

**Inputs** self.

**Explicit results** self.get\_ordered\_status() equals “Ordered”.

**Local steps**

- Return self.get\_ordered\_status() equals “Ordered”.

**Methods declared on this owner** [get ordered status](operations-011.md#op-83466582d7d32f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L846) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1889) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1263)

<a id="op-45c1cfe9052944"></a>
### Quotation.is partially ordered

`operation_enterprise_selling_record_definitions_quotation_business_behavior_quotation_is_partially_ordered`

**Inputs** self.

**Explicit results** self.get\_ordered\_status() equals “Partially Ordered”.

**Local steps**

- Return self.get\_ordered\_status() equals “Partially Ordered”.

**Methods declared on this owner** [get ordered status](operations-011.md#op-83466582d7d32f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0633.json#L909) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1890) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1264)
