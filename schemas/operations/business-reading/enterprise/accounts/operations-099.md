# Accounting and settlement · operations 99

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-8ca638d7e387a2"></a>
### Sales Invoice.on submit

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Authorization Control” via get\_cached\_doc · read “Selling Settings” via get\_single\_value · resolve a document from “Sales Invoice” via get\_doc · resolve a document from self.doctype via get\_doc.

**Local steps**

- Evaluate self.validate\_pos\_paid\_amount().
- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(self.doctype, self.company, self.base\_grand\_total, self).
- Evaluate self.check\_prev\_docstatus().
- If (self.is\_return and not self.update\_billed\_amount\_in\_sales\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not self.update\_billed\_amount\_in\_sales\_order.
  - Set self.status\_updater from list().
- Evaluate SalesTaxWithholding(self).on\_submit().
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.update\_billing\_status\_in\_dn().
- Evaluate self.clear\_unallocated\_mode\_of\_payments().
- If self.update\_stock equals 1.
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
- Evaluate self.split\_asset\_based\_on\_sale\_qty().
- If not self.is\_return.
  - Evaluate self.process\_asset\_depreciation().
- Evaluate self.set\_asset\_disposal\_values().
- Evaluate self.make\_gl\_entries().
- If self.is\_return.
  - Evaluate self.process\_asset\_depreciation().
- If self.update\_stock equals 1.
  - Evaluate self.repost\_future\_sle\_and\_gle().
  - Evaluate self.update\_pick\_list\_status().
  - Evaluate self.update\_project\_consumed\_material\_cost().
- If not self.is\_return.
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Delivery Note”).
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Sales Order”).
  - If self.is\_opening differs from “Yes”.
    - Evaluate self.check\_credit\_limit().
    - Evaluate self.check\_overdue\_billing\_threshold().
- If (cint(self.is\_pos) differs from 1 and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_pos) differs from 1 → not self.is\_return.
  - Evaluate self.update\_against\_document\_in\_jv().
- Evaluate self.update\_time\_sheet(no value when (self.is\_return and self.return\_against), otherwise self.name).
  - Value choice on (self.is\_return and self.return\_against) — true gives no value, false gives self.name.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
- If Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”) equals “Each Transaction”.
  - Evaluate update\_company\_current\_month\_sales(self.company).
  - Evaluate self.update\_project().
- Evaluate update\_linked\_doc(self.doctype, self.name, self.inter\_company\_invoice\_reference).
- If (self.coupon\_code and self.counts\_coupon\_use()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.coupon\_code → self.counts\_coupon\_use().
  - Evaluate update\_coupon\_code\_count(self.coupon\_code, “used”).
- If (not self.is\_return and not self.is\_consolidated and self.loyalty\_program and not self.dont\_create\_loyalty\_points).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → not self.is\_consolidated → self.loyalty\_program → not self.dont\_create\_loyalty\_points.
  - Evaluate self.make\_loyalty\_point\_entry().
- Otherwise.
  - If (self.is\_return and self.return\_against and not self.is\_consolidated and self.loyalty\_program).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → not self.is\_consolidated → self.loyalty\_program.
    - Set against\_si\_doc from Platform.get\_doc(“Sales Invoice”, self.return\_against).
    - Evaluate against\_si\_doc.delete\_loyalty\_point\_entry().
    - Evaluate against\_si\_doc.make\_loyalty\_point\_entry().
- If (self.redeem\_loyalty\_points and not self.is\_consolidated and self.loyalty\_points).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.redeem\_loyalty\_points → not self.is\_consolidated → self.loyalty\_points.
  - Evaluate self.apply\_loyalty\_points().
- Evaluate self.process\_common\_party\_accounting().
- Evaluate self.update\_billed\_qty\_in\_scio().
- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Evaluate Platform.get\_doc(self.doctype, self.return\_against).set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate pos paid amount](operations-099.md#op-9117df5b763a77), [check prev docstatus](operations-101.md#op-e62cfe01aef787), [update status updater args](operations-099.md#op-7cdec44b15b5e3), [update billing status in dn](operations-102.md#op-6b15b2f5e31a98), [clear unallocated mode of payments](operations-100.md#op-0d766644b5b568), [split asset based on sale qty](operations-101.md#op-e158713d18972b), [process asset depreciation](operations-101.md#op-50d3c2f8a2f1a8), [set asset disposal values](operations-101.md#op-35743dfc88611e), [make gl entries](operations-102.md#op-cb5da2401ff5c4), [check credit limit](operations-099.md#op-f1a6dcc40618c2), [check overdue billing threshold](operations-099.md#op-2f1141280033d1), [update time sheet](operations-099.md#op-c11c28220a5ee7), [update project](operations-102.md#op-aafaca2828d274), [counts coupon use](operations-103.md#op-83586bcd294ed4), [make loyalty point entry](operations-103.md#op-e0527769d43d3b), [apply loyalty points](operations-103.md#op-a2aff537441670), [update billed qty in scio](operations-099.md#op-f1f14a8beade02).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”), Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1031) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1161)

<a id="op-7d024d645a521b"></a>
### Sales Invoice.validate pos return

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_pos_return`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Total payments amount can't be greater than {}”.format(negative invoice\_total).

**Local steps**

- If self.is\_consolidated.
  - Return no value.
- If (self.is\_pos and self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_pos → self.is\_return.
  - Set total\_amount\_in\_payments from 0.
  - For each payment in self.payments.
    - Update total\_amount\_in\_payments using + payment.amount.
  - Set invoice\_total from (self.rounded\_total or self.grand\_total).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rounded\_total → self.grand\_total.
  - If total\_amount\_in\_payments &lt; invoice\_total.
    - Call the validation error handler Platform.throw(translated “Total payments amount can't be greater than {}”.format(negative invoice\_total)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1059)

<a id="op-9117df5b763a77"></a>
### Sales Invoice.validate pos paid amount

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_pos_paid_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “At least one mode of payment is required for POS invoice.”.

**Local steps**

- If (len(self.payments) equals 0 and self.is\_pos and flt(self.grand\_total) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(self.payments) equals 0 → self.is\_pos → flt(self.grand\_total) &gt; 0.
  - Call the validation error handler Platform.throw(translated “At least one mode of payment is required for POS invoice.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1058)

<a id="op-1ec5d67c2d8429"></a>
### Sales Invoice.check if consolidated invoice

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_check_if_consolidated_invoice`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (self.doctype equals “Sales Invoice” and self.is\_consolidated).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_consolidated.
  - Set pos\_closing\_entry from self.get\_pos\_closing\_entry\_of\_consolidated\_invoice().
  - If pos\_closing\_entry.
    - Set msg from translated “To cancel a {} you need to cancel the POS Closing Entry {}.”.format(Platform.bold(translated “Consolidated Sales Invoice”), get\_link\_to\_form(“POS Closing Entry”, pos\_closing\_entry)).
    - Call the validation error handler Platform.throw(msg, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get pos closing entry of consolidated invoice](operations-099.md#op-8e8b385598ac9d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1007)

<a id="op-8e8b385598ac9d"></a>
### Sales Invoice.get pos closing entry of consolidated invoice

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_pos_closing_entry_of_consolidated_invoice`

**Inputs** self.

**Explicit results** result at 0 at 0 when result, otherwise no value.

**Local steps**

- Set merge\_log from Platform.qb.DocType(“POS Invoice Merge Log”).
- Set query from nested operand in the contract.qb.from\_(merge\_log).select(merge\_log.pos\_closing\_entry).limit(1).
- If self.is\_return.
  - Set merge\_log\_item from Platform.qb.DocType(“POS Invoice Reference”).
  - Set pos\_invoice from Platform.qb.DocType(“POS Invoice”).
  - Set query from nested operand in the contract(nested operand in the contract).join(pos\_invoice).on(pos\_invoice.name equals merge\_log\_item.pos\_invoice).where(pos\_invoice.consolidated\_invoice equals self.name).
- Otherwise.
  - Set query from query.where(merge\_log.consolidated\_invoice equals self.name).
- Set result from query.where((nested operand in the contract.pos\_closing\_entry.isnotnull() bitwise and merge\_log.pos\_closing\_entry differs from empty text)).run().
- Return result at 0 at 0 when result, otherwise no value.
  - Value choice on result — true gives result at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1022)

<a id="op-88d6eebb2a640d"></a>
### Sales Invoice.check if created using pos and pos closing entry generated

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_check_if_created_using_pos_and_pos_closing_entry_generated`

**Inputs** self.

**Record and data access** read “POS Closing Entry” via get\_value.

**Explicit failure paths** validation helper.

**Local steps**

- If (self.doctype equals “Sales Invoice” and self.is\_created\_using\_pos and self.pos\_closing\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_created\_using\_pos → self.pos\_closing\_entry.
  - Set pos\_closing\_entry\_docstatus from Platform.db.get\_value(“POS Closing Entry”, self.pos\_closing\_entry, “docstatus”).
  - If pos\_closing\_entry\_docstatus equals 1.
    - Call the validation error handler Platform.throw(msg = translated “To cancel this Sales Invoice you need to cancel the POS Closing Entry {}.”.format(get\_link\_to\_form(“POS Closing Entry”, self.pos\_closing\_entry)), title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1008)

<a id="op-0fc4cac68bd639"></a>
### Sales Invoice.before cancel

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate validate\_deferred\_revenue\_return\_cancellation(self).
- Evaluate self.check\_if\_created\_using\_pos\_and\_pos\_closing\_entry\_generated().
- Evaluate self.check\_if\_consolidated\_invoice().
- Evaluate super().before\_cancel().
- Evaluate self.update\_time\_sheet(self.return\_against when (self.is\_return and self.return\_against), otherwise no value).
  - Value choice on (self.is\_return and self.return\_against) — true gives self.return\_against, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if created using pos and pos closing entry generated](operations-099.md#op-88d6eebb2a640d), [check if consolidated invoice](operations-099.md#op-1ec5d67c2d8429), [update time sheet](operations-099.md#op-c11c28220a5ee7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1014) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1144)

<a id="op-5de7e123b40cf7"></a>
### Sales Invoice.on cancel

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_on_cancel`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value · resolve a document from “Sales Invoice” via get\_doc · resolve a document from self.doctype via get\_doc.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate check\_if\_return\_invoice\_linked\_with\_payment\_entry(self).
- Evaluate super().on\_cancel().
- Evaluate self.check\_sales\_order\_on\_hold\_or\_close(“sales\_order”).
- If (self.is\_return and not self.update\_billed\_amount\_in\_sales\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not self.update\_billed\_amount\_in\_sales\_order.
  - Set self.status\_updater from list().
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.update\_billing\_status\_in\_dn().
- If not self.is\_return.
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Delivery Note”).
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Sales Order”).
- Evaluate SalesTaxWithholding(self).on\_cancel().
- If self.update\_stock equals 1.
  - Evaluate self.update\_stock\_ledger().
- Evaluate self.process\_asset\_depreciation().
- Evaluate self.make\_gl\_entries\_on\_cancel().
- If self.update\_stock equals 1.
  - Evaluate self.update\_stock\_reservation\_entries().
  - Evaluate self.repost\_future\_sle\_and\_gle().
  - Evaluate self.update\_pick\_list\_status().
  - Evaluate self.update\_project\_consumed\_material\_cost().
- Evaluate self.db\_set(“status”, “Cancelled”).
- If (self.coupon\_code and self.counts\_coupon\_use()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.coupon\_code → self.counts\_coupon\_use().
  - Evaluate update\_coupon\_code\_count(self.coupon\_code, “cancelled”).
- If Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”) equals “Each Transaction”.
  - Evaluate update\_company\_current\_month\_sales(self.company).
  - Evaluate self.update\_project().
- If (not self.is\_return and not self.is\_consolidated and self.loyalty\_program).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → not self.is\_consolidated → self.loyalty\_program.
  - Evaluate self.delete\_loyalty\_point\_entry().
- Otherwise.
  - If (self.is\_return and self.return\_against and not self.is\_consolidated and self.loyalty\_program).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → not self.is\_consolidated → self.loyalty\_program.
    - Set against\_si\_doc from Platform.get\_doc(“Sales Invoice”, self.return\_against).
    - Evaluate against\_si\_doc.delete\_loyalty\_point\_entry().
    - Evaluate against\_si\_doc.make\_loyalty\_point\_entry().
- Evaluate unlink\_inter\_company\_doc(self.doctype, self.name, self.inter\_company\_invoice\_reference).
- Evaluate self.unlink\_sales\_invoice\_from\_timesheets().
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Repost Payment Ledger”, …).
- Evaluate self.delete\_auto\_created\_batches().
- If (self.doctype equals “Sales Invoice” and self.is\_pos and self.is\_return and self.is\_created\_using\_pos and not self.pos\_closing\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_pos → self.is\_return → self.is\_created\_using\_pos → not self.pos\_closing\_entry.
  - Evaluate self.cancel\_pos\_invoice\_credit\_note\_generated\_during\_sales\_invoice\_mode().
- Evaluate self.update\_billed\_qty\_in\_scio().
- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Evaluate Platform.get\_doc(self.doctype, self.return\_against).set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status updater args](operations-099.md#op-7cdec44b15b5e3), [update billing status in dn](operations-102.md#op-6b15b2f5e31a98), [process asset depreciation](operations-101.md#op-50d3c2f8a2f1a8), [counts coupon use](operations-103.md#op-83586bcd294ed4), [update project](operations-102.md#op-aafaca2828d274), [delete loyalty point entry](operations-103.md#op-f8de9e8b8eb532), [unlink sales invoice from timesheets](operations-099.md#op-4f541c15547caf), [cancel pos invoice credit note generated during sales invoice mode](operations-099.md#op-d41695bd901f9a), [update billed qty in scio](operations-099.md#op-f1f14a8beade02).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1029) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1159)

<a id="op-7cdec44b15b5e3"></a>
### Sales Invoice.update status updater args

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_update_status_updater_arguments`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not cint(self.update\_stock).
  - Return no value.
- Evaluate self.status\_updater.extend(list(mapping(“source\_dt” → “Sales Invoice Item”, “target\_dt” → “Sales Order Item”, “target\_parent\_dt” → “Sales Order”, “target\_parent\_field” → “per\_delivered”, …), mapping(“sourc ….
- If not cint(self.is\_return).
  - Return no value.
- Evaluate self.status\_updater.append(mapping(“source\_dt” → “Sales Invoice Item”, “target\_dt” → “Sales Order Item”, “join\_field” → “so\_detail”, “target\_field” → “returned\_qty”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1048) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1178)

<a id="op-f1a6dcc40618c2"></a>
### Sales Invoice.check credit limit

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_check_credit_limit`

**Inputs** self.

**Local steps**

- Bind dependencies check\_credit\_limit, is\_sales\_order\_credit\_check\_bypassed.
- Set validate\_against\_credit\_limit from false.
- Set bypass\_credit\_limit\_check\_at\_sales\_order from is\_sales\_order\_credit\_check\_bypassed(self.customer, self.company).
- If bypass\_credit\_limit\_check\_at\_sales\_order.
  - Set validate\_against\_credit\_limit from true.
- For each d in self.get(“items”).
  - If not (d.sales\_order or d.delivery\_note).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.sales\_order → d.delivery\_note.
    - Set validate\_against\_credit\_limit from true.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If validate\_against\_credit\_limit.
  - Evaluate check\_credit\_limit(self.customer, self.company, bypass\_credit\_limit\_check\_at\_sales\_order).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1017) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1147)

<a id="op-4f541c15547caf"></a>
### Sales Invoice.unlink sales invoice from timesheets

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_unlink_sales_invoice_from_timesheets`

**Inputs** self.

**Record and data access** resolve a document from “Timesheet” via get\_doc.

**Local steps**

- For each row in self.timesheets.
  - Set timesheet from Platform.get\_doc(“Timesheet”, row.time\_sheet).
  - Evaluate timesheet.unlink\_sales\_invoice(self.name).
  - Set timesheet.flags.ignore\_validate\_update\_after\_submit from true.
  - Evaluate timesheet.db\_update\_all().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1046)

<a id="op-d41695bd901f9a"></a>
### Sales Invoice.cancel pos invoice credit note generated during sales invoice mode

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_cancel_pos_invoice_credit_note_generated_during_sales_invoice_mode`

**Inputs** self.

**Record and data access** read “POS Invoice” via get\_all · resolve a document from “POS Invoice” via get\_doc.

**State and service calls** call cancel on pos\_invoice\_doc.

**Local steps**

- Set pos\_invoices from Platform.get\_all(“POS Invoice”, filters = mapping(“consolidated\_invoice” → self.name), pluck = “name”).
- If pos\_invoices.
  - For each pos\_invoice in pos\_invoices.
    - Set pos\_invoice\_doc from Platform.get\_doc(“POS Invoice”, pos\_invoice).
    - Evaluate pos\_invoice\_doc.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1006)

<a id="op-2f1141280033d1"></a>
### Sales Invoice.check overdue billing threshold

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_check_overdue_billing_threshold`

**Inputs** self.

**Local steps**

- Bind dependencies check\_overdue\_billing\_threshold.
- Evaluate check\_overdue\_billing\_threshold(self.customer, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0166.json#L6781) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1018) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1148)

<a id="op-ec39fb0c043d8e"></a>
### Sales Invoice.set missing values

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_set_missing_values`

**Inputs** self, for\_validate = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_value · read “Print Format” via get\_value.

**Explicit results** mapping(“print\_format” → print\_format, “allow\_edit\_rate” → pos.get(“allow\_user\_to\_edit\_rate”), “allow\_edit\_discount” → pos.get(“allow\_user\_to\_edit\_discount”), “utm\_source” → pos.get(“utm\_source”), …).

**Local steps**

- Set pos from self.set\_pos\_fields(for\_validate).
- If not self.debit\_to.
  - Set self.debit\_to from get\_party\_account(“Customer”, self.customer, self.company).
  - Set self.party\_account\_currency from Platform.db.get\_value(“Account”, self.debit\_to, “account\_currency”, cache = true).
- If (not self.due\_date and self.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.due\_date → self.customer.
  - Set self.due\_date from get\_due\_date(self.posting\_date, “Customer”, self.customer, self.company, template\_name = self.payment\_terms\_template).
- Evaluate super().set\_missing\_values(for\_validate).
- Set print\_format from pos.get(“print\_format”) when pos, otherwise no value.
  - Value choice on pos — true gives pos.get(“print\_format”), false gives no value.
- If (not print\_format and not cint(Platform.db.get\_value(“Print Format”, “POS Invoice”, “disabled”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not print\_format → not cint(Platform.db.get\_value(“Print Format”, “POS Invoice”, “disabled”)).
  - Set print\_format from “POS Invoice”.
- If pos.
  - Return mapping(“print\_format” → print\_format, “allow\_edit\_rate” → pos.get(“allow\_user\_to\_edit\_rate”), “allow\_edit\_discount” → pos.get(“allow\_user\_to\_edit\_discount”), “utm\_source” → pos.get(“utm\_source”), …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set pos fields](operations-100.md#op-bf85303a77c6c0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1040) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1170)

<a id="op-62bc99bb6d9753"></a>
### Sales Invoice.refresh subscription status

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_refresh_subscription_status`

**Inputs** self.

**Local steps**

- If self.get(“subscription”).
  - Evaluate refresh\_subscription\_status(self.subscription).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L865) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1034) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1164)

<a id="op-c030130255877e"></a>
### Sales Invoice.reset mode of payments

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_reset_mode_of_payments`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “POS Profile” via get\_cached\_doc.

**Local steps**

- If self.pos\_profile.
  - Set pos\_profile from Platform.get\_cached\_doc(“POS Profile”, self.pos\_profile).
  - Evaluate update\_multi\_mode\_option(self, pos\_profile).
  - Set self.paid\_amount from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Profile”, self.pos\_profile).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1035) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1165)

<a id="op-c11c28220a5ee7"></a>
### Sales Invoice.update time sheet

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_update_time_sheet`

**Inputs** self, sales\_invoice.

**Record and data access** resolve a document from “Timesheet” via get\_doc.

**Local steps**

- For each d in self.timesheets.
  - If d.time\_sheet.
    - Set timesheet from Platform.get\_doc(“Timesheet”, d.time\_sheet).
    - Evaluate self.update\_time\_sheet\_detail(timesheet, d, sales\_invoice).
    - Evaluate timesheet.calculate\_total\_amounts().
    - Evaluate timesheet.calculate\_percentage\_billed().
    - Set timesheet.flags.ignore\_validate\_update\_after\_submit from true.
    - Evaluate timesheet.set\_status().
    - Evaluate timesheet.db\_update\_all().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update time sheet detail](operations-099.md#op-9b7ff271c256dc).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1049)

<a id="op-f1f14a8beade02"></a>
### Sales Invoice.update billed qty in scio

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_update_billed_quantity_in_sales_commission`

**Inputs** self.

**Local steps**

- Set table from Platform.qb.DocType(“Subcontracting Inward Order Received Item”).
- Set sign from 1 when self.\_action equals “submit”, otherwise negative 1.
  - Value choice on self.\_action equals “submit” — true gives 1, false gives negative 1.
- Set data from mapping of name → (sign × qty) for tuple(name, qty) drawn from self.get\_scio\_self\_rm\_stock\_qty().items().
  - Draw tuple(name, qty) from self.get\_scio\_self\_rm\_stock\_qty().items().
- If data.
  - Set case\_expr from Case().
  - For each tuple(name, qty) in data.items().
    - Set case\_expr from case\_expr.when(table.name equals name, (table.billed\_qty + qty)).
  - Evaluate nested operand in the contract(nested operand in the contract).set(table.billed\_qty, case\_expr).where((nested operand in the contract.name.isin(list(nested operand in the contract())) bitwise and table.doc ….run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get scio self rm stock qty](operations-099.md#op-2f0d73b6126f99).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1043) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1173)

<a id="op-2f0d73b6126f99"></a>
### Sales Invoice.get scio self rm stock qty

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_scio_self_rm_stock_qty`

**Inputs** self.

**Explicit results** stock\_qty.

**Local steps**

- Set stock\_qty from defaultdict(float).
- For each item in self.items.
  - If item.scio\_detail.
    - Update stock\_qty at item.scio\_detail using + flt(item.stock\_qty).
- Return stock\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1024)

<a id="op-9b7ff271c256dc"></a>
### Sales Invoice.update time sheet detail

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_update_time_sheet_detail`

**Inputs** self, timesheet, args, sales\_invoice.

**Local steps**

- For each data in timesheet.time\_logs.
  - If ((self.project and args.timesheet\_detail equals data.name) or (not self.project and not data.sales\_invoice and args.timesheet\_detail equals data.name) or (not sales\_invoice and data.sales\_invoice equals se ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.project and args.timesheet\_detail equals data.name) → (not self.project and not data.sales\_invoice and args.timesheet\_detail equals data.name) → (not sales\_invoice and data.sales\_invoice equals self.name and args.timesheet\_detail equals data.name) → (self.is\_return and self.return\_against and data.sales\_invoice and data.sales\_invoice equals self.return\_against and not sales\_invoice and args.timesheet\_detail equals data.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project → args.timesheet\_detail equals data.name.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.project → not data.sales\_invoice → args.timesheet\_detail equals data.name.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sales\_invoice → data.sales\_invoice equals self.name → args.timesheet\_detail equals data.name.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → data.sales\_invoice → data.sales\_invoice equals self.return\_against → not sales\_invoice → args.timesheet\_detail equals data.name.
    - Set data.sales\_invoice from sales\_invoice.

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1050)

<a id="op-f65bc86dc0220c"></a>
### Sales Invoice.on update after submit

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_on_update_after_submit`

**Inputs** self.

**Local steps**

- Set fields\_to\_check from list(“additional\_discount\_account”, “cash\_bank\_account”, “account\_for\_change\_amount”, “write\_off\_account”, …).
- Set child\_tables from mapping(“items” → tuple(“income\_account”, “expense\_account”, “discount\_account”), “taxes” → tuple(“account\_head”)).
- Set needs\_repost from self.check\_if\_fields\_updated(fields\_to\_check, child\_tables).
- If needs\_repost.
  - Evaluate self.validate\_for\_repost().
  - Evaluate self.repost\_accounting\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for repost](operations-098.md#op-6c7593fa0981f3).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1032) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1162)

<a id="op-d485c9ee08267b"></a>
### Sales Invoice.set paid amount

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_set_paid_amount`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set paid\_amount from 0.0.
- Set base\_paid\_amount from 0.0.
- If (not cint(self.is\_pos) and self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.is\_pos) → self.is\_return.
  - Evaluate self.set(“payments”, list()).
  - Set self.paid\_amount from paid\_amount.
  - Set self.base\_paid\_amount from base\_paid\_amount.
  - Return no value.
- For each data in self.payments.
  - Set data.base\_amount from flt((data.amount × self.conversion\_rate), self.precision(“base\_paid\_amount”)).
  - Update paid\_amount using + data.amount.
  - Update base\_paid\_amount using + data.base\_amount.
- Set self.paid\_amount from paid\_amount.
- Set self.base\_paid\_amount from base\_paid\_amount.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1044)

<a id="op-da8799df07a11c"></a>
### Sales Invoice.set account for mode of payment

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_set_account_for_mode_of_payment`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- For each payment in self.payments.
  - Set payment.account from get\_bank\_cash\_account(payment.mode\_of\_payment, self.company).get(“account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1037) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1167)

<a id="op-45e90820af32c1"></a>
### Sales Invoice.validate time sheets are submitted

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_time_sheets_are_submitted`

**Inputs** self.

**Record and data access** read “Timesheet Detail” via get\_value · read “Timesheet” via get\_value.

**Explicit failure paths** validation helper — translated “Row {0}: The same time log of Timesheet {1} is added more than once”.format(data.idx, Platform.bold(data.time\_sheet)) · validation helper — translated “Row {0}: Sales Invoice {1} is already created for {2}”.format(data.idx, Platform.bold(sales\_invoice), Platform.bold(data.time\_sheet)) · validation helper — translated “Timesheet {0} cannot be invoiced in its current state”.format(data.time\_sheet).

**Local steps**

- Set listed from set().
- For each data in self.timesheets.
  - If data.timesheet\_detail belongs to listed.
    - Call the validation error handler Platform.throw(translated “Row {0}: The same time log of Timesheet {1} is added more than once”.format(data.idx, Platform.bold(data.time\_sheet))).
  - If (data.time\_sheet and data.timesheet\_detail).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.time\_sheet → data.timesheet\_detail.
    - Evaluate listed.add(data.timesheet\_detail).
    - If sales\_invoice bound to Platform.db.get\_value(“Timesheet Detail”, data.timesheet\_detail, “sales\_invoice”).
      - Call the validation error handler Platform.throw(translated “Row {0}: Sales Invoice {1} is already created for {2}”.format(data.idx, Platform.bold(sales\_invoice), Platform.bold(data.time\_sheet))).
  - If data.time\_sheet.
    - Set status from Platform.db.get\_value(“Timesheet”, data.time\_sheet, “status”).
    - If status does not belong to list(“Submitted”, “Payslip”, “Partially Billed”, “Billed”).
      - Call the validation error handler Platform.throw(translated “Timesheet {0} cannot be invoiced in its current state”.format(data.time\_sheet)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1060)
