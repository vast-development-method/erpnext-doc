# Sales · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Product bundle

[Record definition](../../../../data/record-types/product_bundle.json)

<a id="op-13302259e67b84"></a>
### Product Bundle.on trash

`operation_enterprise_selling_record_definitions_product_bundle_business_behavior_product_bundle_on_trash`

**Inputs** self.

**Record and data access** read item\_doctype via get\_all.

**Explicit failure paths** validation helper — “This Product Bundle is linked with {}. You will have to cancel these documents in order to delete this Produ …”.format(“, ”.join(invoice\_links)).

**Local steps**

- Set linked\_doctypes from list(“Delivery Note”, “Sales Invoice”, “POS Invoice”, “Purchase Receipt”, …).
- Set invoice\_links from list().
- For each doctype in linked\_doctypes.
  - Set item\_doctype from (doctype + “ Item”).
  - If doctype equals “Stock Entry”.
    - Set item\_doctype from (doctype + “ Detail”).
  - Set invoices from Platform.db.get\_all(item\_doctype, mapping(“item\_code” → self.new\_item\_code, “docstatus” → 1), list(“parent”)).
  - For each invoice in invoices.
    - Evaluate invoice\_links.append(get\_link\_to\_form(doctype, invoice at “parent”)).
- If len(invoice\_links).
  - Call the validation error handler Platform.throw(“This Product Bundle is linked with {}. You will have to cancel these documents in order to delete this Produ …”.format(“, ”.join(invoice\_links)), title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1835) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1219)

<a id="op-20eac366bcb5df"></a>
### Product Bundle.validate main item

`operation_enterprise_selling_record_definitions_product_bundle_business_behavior_product_bundle_validate_main_item`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Parent Item {0} must not be a Stock Item”.format(self.new\_item\_code) · validation helper — translated “Parent Item {0} must not be a Fixed Asset”.format(self.new\_item\_code).

**Local steps**

- If Platform.db.get\_value(“Item”, self.new\_item\_code, “is\_stock\_item”).
  - Call the validation error handler Platform.throw(translated “Parent Item {0} must not be a Stock Item”.format(self.new\_item\_code)).
- If Platform.db.get\_value(“Item”, self.new\_item\_code, “is\_fixed\_asset”).
  - Call the validation error handler Platform.throw(translated “Parent Item {0} must not be a Fixed Asset”.format(self.new\_item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L4996) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1840) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1223)

<a id="op-02727b24f14aff"></a>
### Product Bundle.validate child items

`operation_enterprise_selling_record_definitions_product_bundle_business_behavior_product_bundle_validate_child_items`

**Inputs** self.

**Record and data access** read “Product Bundle” via exists.

**Explicit failure paths** validation helper — translated “Row #{0}: A Product Bundle cannot contain its own parent Item {1}.”.format(item.idx, Platform.bold(item.item\_code)) · validation helper — translated “Row #{0}: Child Item should not be a Product Bundle. Please remove Item {1} and Save”.format(item.idx, Platform.bold(item.item\_code)).

**Local steps**

- For each item in self.items.
  - If item.item\_code equals self.new\_item\_code.
    - Call the validation error handler Platform.throw(translated “Row #{0}: A Product Bundle cannot contain its own parent Item {1}.”.format(item.idx, Platform.bold(item.item\_code))).
  - If Platform.db.exists(“Product Bundle”, mapping(“name” → item.item\_code, “disabled” → 0)).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Child Item should not be a Product Bundle. Please remove Item {1} and Save”.format(item.idx, Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1838) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1221)

<a id="op-f69ea0b3943307"></a>
### Product Bundle.validate not nested

`operation_enterprise_binding_enterprise_selling_doctype_product_bundle_product_bundle_productbundle_validate_not_nested`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Item {0} is already a component of Product Bundle {1}; nested bundles are not supported.”.format(Platform.bold(self.new\_item\_code), Platform.bold(outer at 0)).

**Local steps**

- Set pb from Platform.qb.DocType(“Product Bundle”).
- Set pbi from Platform.qb.DocType(“Product Bundle Item”).
- Set outer from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….
- If outer.
  - Call the validation error handler Platform.throw(translated “Item {0} is already a component of Product Bundle {1}; nested bundles are not supported.”.format(Platform.bold(self.new\_item\_code), Platform.bold(outer at 0)), title = translated ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1493)

<a id="op-1f6a1eda6018c2"></a>
### Product Bundle.validate child items uom

`operation_enterprise_binding_enterprise_selling_doctype_product_bundle_product_bundle_productbundle_validate_child_items_uom`

**Inputs** self.

**Record and data access** read “Item” via get\_value · read “UOM Conversion Detail” via exists.

**Explicit failure paths** validation helper — translated “Row #{0}: UOM {1} is not configured for Item {2}. Add a UOM conversion on the Item or use its stock UOM.”.format(item.idx, Platform.bold(item.uom), Platform.bold(item.item\_code)).

**Local steps**

- Bind dependencies get\_uom\_conv\_factor.
- For each item in self.items.
  - If not item.uom.
    - Continue with the next iteration or loop test.
  - Set item\_info from Platform.db.get\_value(“Item”, item.item\_code, list(“stock\_uom”, “variant\_of”), as\_dict = true).
  - If (not item\_info or item.uom equals item\_info.stock\_uom).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_info → item.uom equals item\_info.stock\_uom.
    - Continue with the next iteration or loop test.
  - Set tuple(stock\_uom, variant\_of) from tuple(item\_info.stock\_uom, item\_info.variant\_of).
  - Set parents from list(item.item\_code, variant\_of) when variant\_of, otherwise list(item.item\_code).
    - Value choice on variant\_of — true gives list(item.item\_code, variant\_of), false gives list(item.item\_code).
  - If Platform.db.exists(“UOM Conversion Detail”, mapping(“parent” → list(“in”, parents), “uom” → item.uom)).
    - Continue with the next iteration or loop test.
  - If get\_uom\_conv\_factor(item.uom, stock\_uom).
    - Continue with the next iteration or loop test.
  - Call the validation error handler Platform.throw(translated “Row #{0}: UOM {1} is not configured for Item {2}. Add a UOM conversion on the Item or use its stock UOM.”.format(item.idx, Platform.bold(item.uom), Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1492)

<a id="op-9d5ba15c0a5d7a"></a>
### Product Bundle.validate child items qty non zero

`operation_enterprise_selling_record_definitions_product_bundle_business_behavior_product_bundle_validate_child_items_quantity_non_zero`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Quantity cannot be a non-positive number. Please increase the quantity or remove the Item {1}”.format(item.idx, Platform.bold(item.item\_code)).

**Local steps**

- For each item in self.items.
  - <a id="op-9d5ba15c0a5d7a-guard-3"></a>If item.qty ≤ 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Quantity cannot be a non-positive number. Please increase the quantity or remove the Item {1}”.format(item.idx, Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison item.qty ≤ 0, item.qty = 0 selects the branch that calls the validation-error handler with translated “Row #{0}: Quantity cannot be a non-positive number. Please increase the quantity or remove the Item {1}”.format(item.idx, …. With item.qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9d5ba15c0a5d7a-guard-3)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L5412) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1839) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1222)

<a id="op-6511ce2bca1b25"></a>
### Get new item code

`operation_enterprise_selling_record_definitions_product_bundle_business_behavior_get_new_item_code`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Product Bundle” via get\_list · read “Item” via get\_list.

**Explicit results** Platform.get\_list(“Item”, filters = item\_filters, or\_filters = list of list(fieldname, “like”, formatted text %{txt}%) for fieldname drawn from searchfield when searchfield, otherwise no value, fields = li ….

**Local steps**

- Set product\_bundles from Platform.db.get\_list(“Product Bundle”, mapping(“disabled” → 0), pluck = “name”).
- If (not searchfield or searchfield equals “name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not searchfield → searchfield equals “name”.
  - Set searchfield from Platform.get\_meta(“Item”).get(“search\_fields”).
- Set searchfield from searchfield.split(“,”).
- Evaluate searchfield.append(“name”).
- Set item\_filters from list(list(“is\_stock\_item”, “=”, 0), list(“is\_fixed\_asset”, “=”, 0)).
- If product\_bundles.
  - Evaluate item\_filters.append(list(“name”, “not in”, product\_bundles)).
- Return Platform.get\_list(“Item”, filters = item\_filters, or\_filters = list of list(fieldname, “like”, formatted text %{txt}%) for fieldname drawn from searchfield when searchfield, otherwise no value, fields = li ….
  - Value choice on searchfield — true gives list of list(fieldname, “like”, formatted text %{txt}%) for fieldname drawn from searchfield, false gives no value.
  - Draw fieldname from searchfield.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1827) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1217)

## Record · Proforma invoice

[Record definition](../../../../data/record-types/proforma_invoice.json)

<a id="op-fc7348e8917dd9"></a>
### Proforma Invoice.validate

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_proforma_invoice_validate`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate validate\_feature\_enabled().
- Evaluate self.validate\_amended\_doc().
- Evaluate self.validate\_sales\_order().
- Evaluate self.validate\_duplicate\_lines().
- Evaluate self.set\_item\_values().
- Evaluate self.set\_total\_qty().
- Evaluate self.clear\_generated\_values().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate amended doc](operations-010.md#op-669530ecdca7ca), [validate sales order](operations-010.md#op-f7bc6d5602aa64), [validate duplicate lines](operations-010.md#op-8cf6f97217bbef), [set item values](operations-010.md#op-73c2925c8b042b), [set total qty](operations-010.md#op-05f018980bbec6), [clear generated values](operations-010.md#op-d8c602c804dc79).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1239)

<a id="op-f7bc6d5602aa64"></a>
### Proforma Invoice.validate sales order

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_validate_sales_order`

**Inputs** self.

**Declared result** no value.

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Explicit failure paths** validation helper — translated “A Proforma Invoice can only be created against a submitted Sales Order.”.

**Local steps**

- Set sales\_order from Platform.get\_doc(“Sales Order”, self.sales\_order, check\_permission = “read”).
- <a id="op-f7bc6d5602aa64-guard-4"></a>If sales\_order.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “A Proforma Invoice can only be created against a submitted Sales Order.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison sales\_order.docstatus differs from 1, sales\_order.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “A Proforma Invoice can only be created against a submitted Sales Order.”. With sales\_order.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f7bc6d5602aa64-guard-4)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1502)

<a id="op-8cf6f97217bbef"></a>
### Proforma Invoice.validate duplicate lines

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_validate_duplicate_lines`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: The same Sales Order line is already in row #{1}”.format(item.idx, first\_row at item.so\_detail).

**Local steps**

- Set first\_row from mapping().
- For each item in self.items.
  - If item.so\_detail belongs to first\_row.
    - Call the validation error handler Platform.throw(translated “Row #{0}: The same Sales Order line is already in row #{1}”.format(item.idx, first\_row at item.so\_detail)).
  - Set first\_row at item.so\_detail from item.idx.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1501)

<a id="op-73c2925c8b042b"></a>
### Proforma Invoice.set item values

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_set_item_values`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Sales Order Item” via get\_all.

**Explicit failure paths** validation helper — translated “Row #{0}: The line does not belong to Sales Order {1}”.format(item.idx, Platform.bold(self.sales\_order)).

**Local steps**

- Set so\_items from mapping of row.name → row for row drawn from Platform.get\_all(“Sales Order Item”, filters = mapping(“parent” → self.sales\_order, “parenttype” → “Sales Order”), fields = list(“name”, “item\_code”, “item\_name ….
  - Draw row from Platform.get\_all(“Sales Order Item”, filters = mapping(“parent” → self.sales\_order, “parenttype” → “Sales Order”), fields = list(“name”, “item\_code”, “item\_name”, “description”, …)).
- For each item in self.items.
  - Set so\_item from so\_items.get(item.so\_detail).
  - If not so\_item.
    - Call the validation error handler Platform.throw(translated “Row #{0}: The line does not belong to Sales Order {1}”.format(item.idx, Platform.bold(self.sales\_order))).
  - Set item.item\_code from so\_item.item\_code.
  - Set item.item\_name from so\_item.item\_name.
  - Set item.uom from so\_item.uom.
  - Set item.description from (item.description or so\_item.description).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.description → so\_item.description.
  - Evaluate self.set\_rate\_and\_amount(item, so\_item.rate).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set rate and amount](operations-010.md#op-f5f21d023daf36).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1498)

<a id="op-f5f21d023daf36"></a>
### Proforma Invoice.set rate and amount

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_set_rate_and_amount`

**Inputs** self, item, sales\_order\_rate.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Qty must be a positive number”.format(item.idx) · validation helper — translated “Row #{0}: Amount must be a positive number”.format(item.idx).

**Local steps**

- If flt(item.qty) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Qty must be a positive number”.format(item.idx)).
- If self.based\_on equals “Amount”.
  - If flt(item.amount) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Amount must be a positive number”.format(item.idx)).
  - Set item.rate from (flt(item.amount) ÷ flt(item.qty)).
- Otherwise.
  - Set item.rate from sales\_order\_rate.
  - Set item.amount from (flt(item.qty) × flt(sales\_order\_rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1499)

<a id="op-669530ecdca7ca"></a>
### Proforma Invoice.validate amended doc

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_validate_amended_doc`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Cannot amend {0} {1}, please create a new one instead.”.format(self.doctype, Platform.bold(self.amended\_from)).

**Local steps**

- If self.amended\_from.
  - Call the validation error handler Platform.throw(translated “Cannot amend {0} {1}, please create a new one instead.”.format(self.doctype, Platform.bold(self.amended\_from))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1500)

<a id="op-9399adcc9f9fc1"></a>
### Proforma Invoice.before submit

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_proforma_invoice_before_submit`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.status from “Issued”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0630.json#L4961) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1233)

<a id="op-3d76d9fc95981c"></a>
### Proforma Invoice.on submit

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_proforma_invoice_on_submit`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.generate\_and\_attach\_pdf().

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate and attach pdf](operations-010.md#op-bcf2fbee98c6ba).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0630.json#L5008) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1236)

<a id="op-88f8f2199118b3"></a>
### Proforma Invoice.on cancel

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_proforma_invoice_on_cancel`

**Inputs** self.

**Declared result** no value.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0630.json#L5059) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1859) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1235)

<a id="op-05f018980bbec6"></a>
### Proforma Invoice.set total qty

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_proforma_invoice_set_total_quantity`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.total\_qty from sum(generator of flt(item.qty) for item drawn from self.items).
  - Draw item from self.items.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0630.json#L5122) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1238)

<a id="op-d8c602c804dc79"></a>
### Proforma Invoice.clear generated values

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_clear_generated_values`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.proforma\_pdf from no value.
- Set self.grand\_total from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1494)

<a id="op-bcf2fbee98c6ba"></a>
### Proforma Invoice.generate and attach pdf

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_proforma_invoice_generate_and_attach_portable_document`

**Inputs** self.

**Declared result** no value.

**State and service calls** call db\_set on self.

**Local steps**

- Set printed from self.render\_pdf().
- Set file from save\_file(printed at “fname”, printed at “fcontent”, self.doctype, self.name, is\_private = 1).
- Evaluate self.db\_set(“proforma\_pdf”, file.file\_url).

If control reaches the end, it returns no value.

**Methods declared on this owner** [render pdf](operations-010.md#op-74d012906ec073).

**Boundaries to resolve** stored data, callee failures, file state.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1234)

<a id="op-74d012906ec073"></a>
### Proforma Invoice.render pdf

`operation_enterprise_selling_record_definitions_proforma_invoice_business_behavior_proforma_invoice_render_portable_document`

**Inputs** self.

**Declared result** dict.

**State and service calls** call db\_set on self.

**Explicit results** Platform.attach\_print(“Sales Order”, sales\_order.name, doc = sales\_order, file\_name = self.name, print\_format = self.print\_format, letterhead = self.letter\_head).

**Local steps**

- Set sales\_order from self.get\_sales\_order\_copy().
- Evaluate self.db\_set(“grand\_total”, sales\_order.grand\_total).
- Return Platform.attach\_print(“Sales Order”, sales\_order.name, doc = sales\_order, file\_name = self.name, print\_format = self.print\_format, letterhead = self.letter\_head).

**Methods declared on this owner** [get sales order copy](operations-010.md#op-3fc413de755933).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1237)

<a id="op-3fc413de755933"></a>
### Proforma Invoice.get sales order copy

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_get_sales_order_copy`

**Inputs** self.

**Declared result** Document.

**Record and data access** resolve a document from “Sales Order” via get\_doc.

**Explicit results** sales\_order.

**Explicit failure paths** validation helper — translated “The grand total of a Proforma Invoice cannot be negative.”.

**Local steps**

- Set sales\_order from Platform.get\_doc(“Sales Order”, self.sales\_order).
- Set lines from mapping of item.so\_detail → item for item drawn from self.items.
  - Draw item from self.items.
- Evaluate prorate\_fixed\_charges(sales\_order, self.get\_order\_share(sales\_order)).
- Set sales\_order.items from list of item for item drawn from sales\_order.items where item.name belongs to lines.
  - Draw item from sales\_order.items, keep a combination only if (item.name belongs to lines).
- For each item in sales\_order.items.
  - Evaluate set\_proforma\_line(item, lines at item.name).
- Evaluate ProformaTotals(sales\_order, mapping of item.so\_detail → item.amount for item drawn from self.items).
  - Draw item from self.items.
- If flt(sales\_order.grand\_total) &lt; 0.
  - Call the validation error handler Platform.throw(translated “The grand total of a Proforma Invoice cannot be negative.”).
- Set sales\_order.proforma\_no from self.name.
- Set sales\_order.proforma\_date from self.proforma\_date.
- Set sales\_order.hide\_item\_qty from self.hide\_item\_qty.
- Return sales\_order.

**Methods declared on this owner** [get order share](operations-010.md#op-88508fb5ddf794).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1497)

<a id="op-88508fb5ddf794"></a>
### Proforma Invoice.get order share

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_get_order_share`

**Inputs** self, sales\_order.

**Declared result** float.

**Explicit results** 1 · (sum(generator of flt(item.amount) for item drawn from self.items) ÷ flt(sales\_order.total)).

**Local steps**

- If not flt(sales\_order.total).
  - Return 1.
- Return (sum(generator of flt(item.amount) for item drawn from self.items) ÷ flt(sales\_order.total)).
  - Draw item from self.items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1496)

<a id="op-21454df610c5d0"></a>
### Proforma Invoice.get email content

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformainvoice_get_email_content`

**Inputs** self.

**Declared result** tuple at tuple(str, str).

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** get\_email\_subject\_and\_message(Platform.db.get\_single\_value(“Selling Settings”, “proforma\_email\_template”), mapping(“doc” → self), default\_subject = translated “Proforma Invoice {0}”.format(self.name), defa ….

**Local steps**

- Return get\_email\_subject\_and\_message(Platform.db.get\_single\_value(“Selling Settings”, “proforma\_email\_template”), mapping(“doc” → self), default\_subject = translated “Proforma Invoice {0}”.format(self.name), defa ….

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings”, “proforma\_email\_template”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1495)

<a id="op-050d95b30c4e02"></a>
### Proforma Totals.initialize

`operation_enterprise_binding_enterprise_selling_doctype_proforma_invoice_proforma_invoice_proformatotals_init`

**Inputs** self, doc, amounts.

**Declared result** no value.

**Local steps**

- Set self.amounts from amounts.
- Evaluate super().\_\_init\_\_(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1504)
