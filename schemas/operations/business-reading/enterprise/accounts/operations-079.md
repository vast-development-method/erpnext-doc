# Accounting and settlement · operations 79

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pos invoice

<a id="op-902b29bdc653f7"></a>
### POSInvoice.on submit

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “POS Invoice” via get\_doc.

**Local steps**

- If (not self.is\_return and self.loyalty\_program).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → self.loyalty\_program.
  - Evaluate self.make\_loyalty\_point\_entry().
- Otherwise.
  - If (self.is\_return and self.return\_against and self.loyalty\_program).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → self.loyalty\_program.
    - Set against\_psi\_doc from Platform.get\_doc(“POS Invoice”, self.return\_against).
    - Evaluate against\_psi\_doc.delete\_loyalty\_point\_entry().
    - Evaluate against\_psi\_doc.make\_loyalty\_point\_entry().
- If (self.redeem\_loyalty\_points and self.loyalty\_points).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.redeem\_loyalty\_points → self.loyalty\_points.
  - Evaluate self.apply\_loyalty\_points().
- Evaluate self.check\_phone\_payments().
- Evaluate self.set\_status(update = true).
- Evaluate self.update\_status\_of\_return\_against().
- Evaluate self.make\_bundle\_for\_sales\_purchase\_return().
- For each table\_name in list(“items”, “packed\_items”).
  - Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields(table\_name).
- Evaluate self.make\_packed\_item\_bundles().
- For each table\_name in list(“items”, “packed\_items”).
  - Evaluate self.submit\_serial\_batch\_bundle(table\_name).
- If (self.coupon\_code and self.counts\_coupon\_use()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.coupon\_code → self.counts\_coupon\_use().
  - Bind dependencies update\_coupon\_code\_count.
  - Evaluate update\_coupon\_code\_count(self.coupon\_code, “used”).
- Evaluate self.clear\_unallocated\_mode\_of\_payments().
- If (self.is\_return and self.invoice\_type\_in\_pos equals “Sales Invoice”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.invoice\_type\_in\_pos equals “Sales Invoice”.
  - Evaluate self.create\_and\_add\_consolidated\_sales\_invoice().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check phone payments](operations-079.md#op-e069b3176231dd), [set status](operations-080.md#op-c4fa1c7ebc3e03), [update status of return against](operations-079.md#op-700e399f14951e), [submit serial batch bundle](operations-079.md#op-cf8641386a99c0), [clear unallocated mode of payments](operations-079.md#op-061a2697eb22c1), [create and add consolidated sales invoice](operations-079.md#op-0f35252f198d23).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L533)

<a id="op-cf041af7d38923"></a>
### POSInvoice.before cancel

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_before_cancel`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_value · read “POS Invoice Reference” via get\_all.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (self.consolidated\_invoice and Platform.db.get\_value(“Sales Invoice”, self.consolidated\_invoice, “docstatus”) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.consolidated\_invoice → Platform.db.get\_value(“Sales Invoice”, self.consolidated\_invoice, “docstatus”) equals 1.
  - Set pos\_closing\_entry from Platform.get\_all(“POS Invoice Reference”, ignore\_permissions = true, filters = mapping(“pos\_invoice” → self.name), pluck = “parent”, limit = 1).
  - If pos\_closing\_entry.
    - Set msg from translated “You need to cancel POS Closing Entry {} to be able to cancel this document.”.format(get\_link\_to\_form(“POS Closing Entry”, pos\_closing\_entry at 0)).
  - Otherwise.
    - Set msg from translated “You need to cancel Sales Invoice {0} to be able to cancel this document.”.format(get\_link\_to\_form(“Sales Invoice”, self.consolidated\_invoice)).
  - Call the validation error handler Platform.throw(msg, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L521)

<a id="op-8c48fb4a835239"></a>
### POSInvoice.on cancel

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “POS Invoice” via get\_doc.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.ignore\_linked\_doctypes from list(“Payment Ledger Entry”, “Serial and Batch Bundle”).
- Evaluate super(SalesInvoice, self).on\_cancel().
- If (not self.is\_return and self.loyalty\_program).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → self.loyalty\_program.
  - Evaluate self.delete\_loyalty\_point\_entry().
- Otherwise.
  - If (self.is\_return and self.return\_against and self.loyalty\_program).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → self.loyalty\_program.
    - Set against\_psi\_doc from Platform.get\_doc(“POS Invoice”, self.return\_against).
    - Evaluate against\_psi\_doc.delete\_loyalty\_point\_entry().
    - Evaluate against\_psi\_doc.make\_loyalty\_point\_entry().
- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.update\_status\_of\_return\_against().
- If (self.coupon\_code and self.counts\_coupon\_use()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.coupon\_code → self.counts\_coupon\_use().
  - Bind dependencies update\_coupon\_code\_count.
  - Evaluate update\_coupon\_code\_count(self.coupon\_code, “cancelled”).
- Evaluate self.delink\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status of return against](operations-079.md#op-700e399f14951e), [delink serial and batch bundle](operations-079.md#op-bc55083fe94cbd).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L532)

<a id="op-700e399f14951e"></a>
### POSInvoice.update status of return against

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_posinvoice_update_status_of_return_against`

**Inputs** self.

**Record and data access** resolve a document from “POS Invoice” via get\_doc.

**Local steps**

- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Evaluate Platform.get\_doc(“POS Invoice”, self.return\_against).set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L900)

<a id="op-061a2697eb22c1"></a>
### POSInvoice.clear unallocated mode of payments

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_clear_unallocated_mode_of_payments`

**Inputs** self.

**Local steps**

- Evaluate self.set(“payments”, self.get(“payments”, mapping(“amount” → list(“not in”, list(0, no value, empty text))))).
- Set sip from Platform.qb.DocType(“Sales Invoice Payment”).
- Evaluate nested operand in the contract().where(nested operand in the contract.parent equals nested operand in the contract.name).where(sip.amount equals 0).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0119.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L524)

<a id="op-0f35252f198d23"></a>
### POSInvoice.create and add consolidated sales invoice

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_create_and_add_consolidated_sales_invoice`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set sales\_inv from self.create\_return\_sales\_invoice().
- Evaluate self.db\_set(“consolidated\_invoice”, sales\_inv.name).
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create return sales invoice](operations-079.md#op-a32c4522b50761), [set status](operations-080.md#op-c4fa1c7ebc3e03).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0119.json#L290) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L525)

<a id="op-a32c4522b50761"></a>
### POSInvoice.create return sales invoice

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_create_return_sales_invoice`

**Inputs** self.

**Record and data access** read “POS Invoice” via get\_value.

**State and service calls** request new\_doc for “Sales Invoice” · call save on return\_sales\_invoice · call submit on return\_sales\_invoice.

**Explicit results** return\_sales\_invoice.

**Local steps**

- Set return\_sales\_invoice from Platform.new\_doc(“Sales Invoice”).
- Set return\_sales\_invoice.is\_pos from 1.
- Set return\_sales\_invoice.is\_return from 1.
- Evaluate map\_doc(self, return\_sales\_invoice, table\_map = mapping(“doctype” → return\_sales\_invoice.doctype)).
- Set return\_sales\_invoice.is\_created\_using\_pos from 1.
- Set return\_sales\_invoice.is\_consolidated from 1.
- Set return\_sales\_invoice.flags.is\_consolidated from true.
- Set return\_sales\_invoice.return\_against from Platform.db.get\_value(“POS Invoice”, self.return\_against, “consolidated\_invoice”).
- Set tuple(items, taxes, payments) from tuple(list(), list(), list()).
- For each d in self.items.
  - Set si\_item from map\_child\_doc(d, return\_sales\_invoice, mapping(“doctype” → “Sales Invoice Item”)).
  - Set si\_item.pos\_invoice from self.name.
  - Set si\_item.pos\_invoice\_item from d.name.
  - Set si\_item.sales\_invoice\_item from get\_sales\_invoice\_item\_from\_consolidated\_invoice(self.return\_against, d.pos\_invoice\_item).
  - Evaluate items.append(si\_item).
- For each d in self.get(“taxes”).
  - Set tax from map\_child\_doc(d, return\_sales\_invoice, mapping(“doctype” → “Sales Taxes and Charges”)).
  - Evaluate taxes.append(tax).
- For each d in self.get(“payments”).
  - Set payment from map\_child\_doc(d, return\_sales\_invoice, mapping(“doctype” → “Sales Invoice Payment”)).
  - Evaluate payments.append(payment).
- Evaluate return\_sales\_invoice.set(“items”, items).
- Evaluate return\_sales\_invoice.set(“taxes”, taxes).
- Evaluate return\_sales\_invoice.set(“payments”, payments).
- Evaluate return\_sales\_invoice.save().
- Evaluate return\_sales\_invoice.submit().
- Return return\_sales\_invoice.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L527)

<a id="op-bc55083fe94cbd"></a>
### POSInvoice.delink serial and batch bundle

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_delink_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** request set\_value on “Serial and Batch Bundle” · call cancel on Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle) · call db\_set on row.

**Local steps**

- For each row in self.items.
  - If row.serial\_and\_batch\_bundle.
    - If not self.consolidated\_invoice.
      - Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, mapping(“is\_cancelled” → 1, “voucher\_no” → empty text)).
    - Evaluate Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle).cancel().
    - Evaluate row.db\_set(“serial\_and\_batch\_bundle”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0119.json#L1260) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L528)

<a id="op-cf8641386a99c0"></a>
### POSInvoice.submit serial batch bundle

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_submit_serial_batch_bundle`

**Inputs** self, table\_name.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call submit on doc.

**Local steps**

- For each item in self.get(table\_name).
  - If item.serial\_and\_batch\_bundle.
    - Set doc from Platform.get\_doc(“Serial and Batch Bundle”, item.serial\_and\_batch\_bundle).
    - If doc.docstatus equals 0.
      - Set doc.flags.ignore\_voucher\_validation from true.
      - Evaluate doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0119.json#L1497) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L539)

<a id="op-e069b3176231dd"></a>
### POSInvoice.check phone payments

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_check_phone_payments`

**Inputs** self.

**Record and data access** read “Payment Request” via get\_value.

**Explicit results** Platform.throw(translated “Payment related to {0} is not completed”.format(pay.mode\_of\_payment)).

**Explicit failure paths** validation helper — translated “Payment related to {0} is not completed”.format(pay.mode\_of\_payment).

**Local steps**

- For each pay in self.payments.
  - If (pay.type equals “Phone” and pay.amount ≥ 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pay.type equals “Phone” → pay.amount ≥ 0.
    - Set paid\_amt from Platform.db.get\_value(“Payment Request”, filters = dict(reference\_doctype = “POS Invoice”, reference\_name = self.name, mode\_of\_payment = pay.mode\_of\_payment, status = “Paid”), fieldname = “grand\_total”).
    - If (paid\_amt and pay.amount differs from paid\_amt).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in paid\_amt → pay.amount differs from paid\_amt.
      - Return Platform.throw(translated “Payment related to {0} is not completed”.format(pay.mode\_of\_payment)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0119.json#L1687) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L523)

<a id="op-9df628d748a94f"></a>
### POSInvoice.validate stock availablility

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_stock_availablility`

**Inputs** self.

**Record and data access** resolve a document from “Stock Settings” via get\_cached\_doc · read “POS Profile” via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.is\_return or Platform.get\_cached\_doc(“Stock Settings”).allow\_negative\_stock).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → Platform.get\_cached\_doc(“Stock Settings”).allow\_negative\_stock.
  - Return no value.
- If (self.docstatus.is\_draft() and not Platform.db.get\_value(“POS Profile”, self.pos\_profile, “validate\_stock\_on\_save”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus.is\_draft() → not Platform.db.get\_value(“POS Profile”, self.pos\_profile, “validate\_stock\_on\_save”).
  - Return no value.
- Set rows from list of d for d drawn from self.get(“items”) where (d.item\_code and not d.serial\_and\_batch\_bundle).
  - Draw d from self.get(“items”), keep a combination only if ((d.item\_code and not d.serial\_and\_batch\_bundle)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code → not d.serial\_and\_batch\_bundle.
- If not rows.
  - Return no value.
- Set bundle\_items from get\_active\_bundle\_items(set of d.item\_code for d drawn from rows).
  - Draw d from rows.
- Set required\_qty from get\_required\_stock\_qty(rows, bundle\_items).
- Set tuple(available\_qty, reserved\_stock\_keys) from get\_available\_stock\_qty(required\_qty).
- Set items from get\_stock\_item\_details(set of item\_code for tuple(item\_code, warehouse) drawn from required\_qty).
  - Draw tuple(item\_code, warehouse) from required\_qty.
- Set keys\_to\_check from set of key for key drawn from required\_qty where is\_stock\_check\_needed(items.get(key at 0), key belongs to reserved\_stock\_keys).
  - Draw key from required\_qty, keep a combination only if (is\_stock\_check\_needed(items.get(key at 0), key belongs to reserved\_stock\_keys)).
- For each d in rows.
  - If d.item\_code belongs to bundle\_items.
    - Evaluate self.validate\_bundle\_stock(d, bundle\_items at d.item\_code, required\_qty, available\_qty, …).
  - Otherwise.
    - If tuple(d.item\_code, d.warehouse) belongs to keys\_to\_check.
      - Evaluate self.validate\_item\_stock(d, required\_qty, available\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate bundle stock](operations-079.md#op-28e37f21938dce), [validate item stock](operations-079.md#op-ed9dbdb39e8701).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Stock Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L551)

<a id="op-ed9dbdb39e8701"></a>
### POSInvoice.validate item stock

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_posinvoice_validate_item_stock`

**Inputs** self, row, required\_qty, available\_qty.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} has no stock in warehouse {2}.”.format(row.idx, item\_code, warehouse) · validation helper — translated “Row #{0}: Item {1} in warehouse {2}: Available {3}, Needed {4}.”.format(row.idx, item\_code, warehouse, Platform.bold(flt(available\_qty at key, 2)), …).

**Local steps**

- Set key from tuple(row.item\_code, row.warehouse).
- Set tuple(item\_code, warehouse) from tuple(Platform.bold(row.item\_code), Platform.bold(row.warehouse)).
- If available\_qty at key ≤ 0.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} has no stock in warehouse {2}.”.format(row.idx, item\_code, warehouse), title = translated “Item Out of Stock”).
- Otherwise.
  - If available\_qty at key &lt; required\_qty at key.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} in warehouse {2}: Available {3}, Needed {4}.”.format(row.idx, item\_code, warehouse, Platform.bold(flt(available\_qty at key, 2)), …), title = translated “Insuff ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L902)

<a id="op-28e37f21938dce"></a>
### POSInvoice.validate bundle stock

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_posinvoice_validate_bundle_stock`

**Inputs** self, row, components, required\_qty, available\_qty, keys\_to\_check.

**Explicit failure paths** validation helper with ProductBundleStockValidationError — translated text in the contract.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.warehouse), text in the contract.join(error\_msgs)).

**Local steps**

- Set error\_msgs from list().
- For each component in components.
  - Set key from tuple(component.item\_code, row.warehouse).
  - If (key belongs to keys\_to\_check and available\_qty at key &lt; required\_qty at key).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in key belongs to keys\_to\_check → available\_qty at key &lt; required\_qty at key.
    - Evaluate error\_msgs.append(translated text in the contract.format(Platform.bold(component.item\_code), Platform.bold(flt(required\_qty at key, 2)), Platform.bold(flt(available\_qty at key, 2)))).
- If error\_msgs.
  - Call the validation error handler Platform.throw(translated text in the contract.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.warehouse), text in the contract.join(error\_msgs)), title = translated “Insufficient Stock for ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L901)

<a id="op-fede8a1ee4745e"></a>
### POSInvoice.validate is pos using sales invoice

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_is_point_of_sale_using_sales_invoice`

**Inputs** self.

**Record and data access** read “POS Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Sales Invoice mode is activated in POS. Please create Sales Invoice instead.”.

**Local steps**

- Set self.invoice\_type\_in\_pos from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).
- If (self.invoice\_type\_in\_pos equals “Sales Invoice” and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.invoice\_type\_in\_pos equals “Sales Invoice” → not self.is\_return.
  - Call the validation error handler Platform.throw(translated “Sales Invoice mode is activated in POS. Please create Sales Invoice instead.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0119.json#L3240) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L545)

<a id="op-7e936d87fc81b5"></a>
### POSInvoice.validate serialised or batched item

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_serialised_or_batched_item`

**Inputs** self.

**Explicit failure paths** validation helper — error\_msg.

**Local steps**

- Set auto\_picks\_serial\_nos from self.auto\_picks\_outward\_serial\_batch().
- Set error\_msg from list().
- For each d in self.get(“items”).
  - Set error\_msg from empty text.
  - Set serial\_no\_missing from (not d.serial\_no and not (auto\_picks\_serial\_nos and d.get(“has\_batch\_no”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.serial\_no → not (auto\_picks\_serial\_nos and d.get(“has\_batch\_no”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in auto\_picks\_serial\_nos → d.get(“has\_batch\_no”).
  - If (d.get(“has\_serial\_no”) and ((not d.use\_serial\_batch\_fields and not d.serial\_and\_batch\_bundle) or (d.use\_serial\_batch\_fields and serial\_no\_missing))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“has\_serial\_no”) → ((not d.use\_serial\_batch\_fields and not d.serial\_and\_batch\_bundle) or (d.use\_serial\_batch\_fields and serial\_no\_missing)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not d.use\_serial\_batch\_fields and not d.serial\_and\_batch\_bundle) → (d.use\_serial\_batch\_fields and serial\_no\_missing).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.use\_serial\_batch\_fields → not d.serial\_and\_batch\_bundle.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.use\_serial\_batch\_fields → serial\_no\_missing.
    - Set error\_msg from formatted text Row #{d.idx}: Please select Serial No. for item {bold(d.item\_code)}.
  - Otherwise.
    - If (d.get(“has\_batch\_no”) and ((not d.use\_serial\_batch\_fields and not d.serial\_and\_batch\_bundle) or (d.use\_serial\_batch\_fields and not d.batch\_no))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“has\_batch\_no”) → ((not d.use\_serial\_batch\_fields and not d.serial\_and\_batch\_bundle) or (d.use\_serial\_batch\_fields and not d.batch\_no)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not d.use\_serial\_batch\_fields and not d.serial\_and\_batch\_bundle) → (d.use\_serial\_batch\_fields and not d.batch\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.use\_serial\_batch\_fields → not d.serial\_and\_batch\_bundle.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.use\_serial\_batch\_fields → not d.batch\_no.
      - Set error\_msg from formatted text Row #{d.idx}: Please select Batch No. for item {bold(d.item\_code)}.
- If error\_msg.
  - Call the validation error handler Platform.throw(error\_msg, title = translated “Serial / Batch Bundle Missing”, as\_list = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L550)

<a id="op-6267292a7cb408"></a>
### POSInvoice.validate return items qty

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_return_items_quantity`

**Inputs** self.

**Record and data access** execute query text (SELECT, POS Invoice Item).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{}: You cannot add positive quantities in a return invoice. Please remove item {} to complete the return.”.format(d.idx, Platform.bold(d.item\_code)) · validation helper — translated “Row #{}: Serial No {} cannot be returned since it was not transacted in original invoice {}”.format(d.idx, bold\_serial\_no, bold\_return\_against).

**Local steps**

- If not self.get(“is\_return”).
  - Return no value.
- For each d in self.get(“items”).
  - <a id="op-6267292a7cb408-guard-6"></a>If d.get(“qty”) &gt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{}: You cannot add positive quantities in a return invoice. Please remove item {} to complete the return.”.format(d.idx, Platform.bold(d.item\_code)), title = translated “Inv ….
  - If d.get(“serial\_no”).
    - Set serial\_nos from get\_serial\_nos(d.serial\_no).
    - For each sr in serial\_nos.
      - Set serial\_no\_exists from Platform.db.sql(query text (SELECT, POS Invoice Item), tuple(self.return\_against, sr, (sr + “\\n%”), (“%\\n” + sr), …)).
      - If not serial\_no\_exists.
        - Set bold\_return\_against from Platform.bold(self.return\_against).
        - Set bold\_serial\_no from Platform.bold(sr).
        - Call the validation error handler Platform.throw(translated “Row #{}: Serial No {} cannot be returned since it was not transacted in original invoice {}”.format(d.idx, bold\_serial\_no, bold\_return\_against)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison d.get(“qty”) &gt; 0, d.qty = 1 selects the branch that calls the validation-error handler with translated “Row #{}: You cannot add positive quantities in a return invoice. Please remove item {} to complete the return.”.format(d. …. With d.qty = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6267292a7cb408-guard-6)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L549)

<a id="op-8c794bd3718a64"></a>
### POSInvoice.validate mode of payment

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_mode_of_payment`

**Inputs** self.

**Explicit failure paths** validation helper — translated “At least one mode of payment is required for POS invoice.”.

**Local steps**

- <a id="op-8c794bd3718a64-guard-2"></a>If len(self.payments) equals 0.
  - Call the validation error handler Platform.throw(translated “At least one mode of payment is required for POS invoice.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(self.payments) equals 0, length of self.payments = 0 selects the branch that calls the validation-error handler with translated “At least one mode of payment is required for POS invoice.”. With length of self.payments = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8c794bd3718a64-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0119.json#L4782) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L547)

<a id="op-52d55db02a4bbc"></a>
### POSInvoice.validate change account

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_change_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “The selected change account {} doesn't belongs to Company {}.”.format(self.account\_for\_change\_amount, self.company).

**Local steps**

- If (self.change\_amount and self.account\_for\_change\_amount and Platform.get\_cached\_value(“Account”, self.account\_for\_change\_amount, “company”) differs from self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.change\_amount → self.account\_for\_change\_amount → Platform.get\_cached\_value(“Account”, self.account\_for\_change\_amount, “company”) differs from self.company.
  - Call the validation error handler Platform.throw(translated “The selected change account {} doesn't belongs to Company {}.”.format(self.account\_for\_change\_amount, self.company)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account\_for\_change\_amount, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L542)

<a id="op-1e3bfe125ecd5e"></a>
### POSInvoice.set pos paid amount

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_posinvoice_set_pos_paid_amount`

**Inputs** self.

**Local steps**

- Evaluate self.set\_paid\_amount().
- If (self.redeem\_loyalty\_points and self.loyalty\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.redeem\_loyalty\_points → self.loyalty\_amount.
  - Update self.base\_paid\_amount using + flt(self.loyalty\_amount).
  - Update self.paid\_amount using + (flt(self.loyalty\_amount) ÷ flt(self.conversion\_rate)).
- Set self.paid\_amount from flt(self.paid\_amount, self.precision(“paid\_amount”)).
- Set self.base\_paid\_amount from flt(self.base\_paid\_amount, self.precision(“base\_paid\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L899)

<a id="op-fdc9b0225cb55d"></a>
### POSInvoice.validate change amount

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_change_amount`

**Inputs** self.

**State and service calls** msgprint with translated “Please enter Account for Change Amount”.

**Local steps**

- Set grand\_total from (flt(self.rounded\_total) or flt(self.grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.rounded\_total) → flt(self.grand\_total).
- Set self.change\_amount, self.base\_change\_amount from 0.
- If grand\_total &lt; flt((flt(self.paid\_amount) + flt(self.write\_off\_amount)), self.precision(“grand\_total”)).
  - Set self.change\_amount from flt(((self.paid\_amount − grand\_total) + flt(self.write\_off\_amount)), self.precision(“change\_amount”)).
  - Set self.base\_change\_amount from flt((self.change\_amount × flt(self.conversion\_rate)), self.precision(“base\_change\_amount”)).
- If (flt(self.change\_amount) and not self.account\_for\_change\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.change\_amount) → not self.account\_for\_change\_amount.
  - Evaluate Platform.msgprint(translated “Please enter Account for Change Amount”, raise\_exception = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L543)

<a id="op-15f07558f65b99"></a>
### POSInvoice.validate payment amount

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_payment_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0} (Payment Table): Amount must be positive”.format(entry.idx) · validation helper — translated “Row #{0} (Payment Table): Amount must be negative”.format(entry.idx) · validation helper — translated “Total payments amount can't be greater than {}”.format(negative invoice\_total).

**Local steps**

- Set total\_amount\_in\_payments from 0.
- For each entry in self.payments.
  - Update total\_amount\_in\_payments using + entry.amount.
  - If (not self.is\_return and entry.amount &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → entry.amount &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0} (Payment Table): Amount must be positive”.format(entry.idx)).
  - If (self.is\_return and entry.amount &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → entry.amount &gt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0} (Payment Table): Amount must be negative”.format(entry.idx)).
- If (self.is\_return and self.docstatus differs from 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.docstatus differs from 0.
  - Set invoice\_total from (self.rounded\_total or self.grand\_total).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rounded\_total → self.grand\_total.
  - Set total\_amount\_in\_payments from flt(total\_amount\_in\_payments, self.precision(“grand\_total”)).
  - If (total\_amount\_in\_payments and total\_amount\_in\_payments &lt; invoice\_total).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_amount\_in\_payments → total\_amount\_in\_payments &lt; invoice\_total.
    - Call the validation error handler Platform.throw(translated “Total payments amount can't be greater than {}”.format(negative invoice\_total)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L548)

<a id="op-1749f21f793e59"></a>
### POSInvoice.validate company with pos company

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_company_with_point_of_sale_company`

**Inputs** self.

**Record and data access** read “POS Profile” via get\_value.

**Explicit failure paths** validation helper — translated “Company {} does not match with POS Profile Company {}”.format(self.company, Platform.db.get\_value(“POS Profile”, self.pos\_profile, “company”)).

**Local steps**

- If self.company differs from Platform.db.get\_value(“POS Profile”, self.pos\_profile, “company”).
  - Call the validation error handler Platform.throw(translated “Company {} does not match with POS Profile Company {}”.format(self.company, Platform.db.get\_value(“POS Profile”, self.pos\_profile, “company”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L544)

<a id="op-5863bde92b1c9b"></a>
### POSInvoice.set outstanding amount

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_set_outstanding_amount`

**Inputs** self.

**Local steps**

- Set precision from self.precision(“outstanding\_amount”).
- Set total from flt(((flt(self.rounded\_total) or flt(self.grand\_total)) − flt(self.write\_off\_amount)), precision).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.rounded\_total) → flt(self.grand\_total).
- Set paid\_amount from flt(self.paid\_amount, precision).
- Set self.outstanding\_amount from flt((total − paid\_amount), precision) when total &gt; paid\_amount, otherwise 0.
  - Value choice on total &gt; paid\_amount — true gives flt((total − paid\_amount), precision), false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L536)

<a id="op-15346b78f0c4b5"></a>
### POSInvoice.validate loyalty transaction

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate_loyalty_transaction`

**Inputs** self.

**Record and data access** read “Loyalty Program” via get\_value.

**Local steps**

- If (self.redeem\_loyalty\_points and (not self.loyalty\_redemption\_account or not self.loyalty\_redemption\_cost\_center)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.redeem\_loyalty\_points → (not self.loyalty\_redemption\_account or not self.loyalty\_redemption\_cost\_center).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.loyalty\_redemption\_account → not self.loyalty\_redemption\_cost\_center.
  - Set tuple(expense\_account, cost\_center) from Platform.db.get\_value(“Loyalty Program”, self.loyalty\_program, list(“expense\_account”, “cost\_center”)).
  - If not self.loyalty\_redemption\_account.
    - Set self.loyalty\_redemption\_account from expense\_account.
  - If not self.loyalty\_redemption\_cost\_center.
    - Set self.loyalty\_redemption\_cost\_center from cost\_center.
- If (self.redeem\_loyalty\_points and self.loyalty\_program and self.loyalty\_points).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.redeem\_loyalty\_points → self.loyalty\_program → self.loyalty\_points.
  - Evaluate validate\_loyalty\_points(self, self.loyalty\_points).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0120.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L546)
