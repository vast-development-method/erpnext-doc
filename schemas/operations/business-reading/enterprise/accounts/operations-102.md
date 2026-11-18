# Accounting and settlement · operations 102

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-bca9e6987d3bea"></a>
### Sales Invoice.restore asset

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_restore_asset`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_cached\_doc.

**Local steps**

- For each d in self.get(“items”).
  - If d.asset.
    - Set asset from Platform.get\_cached\_doc(“Asset”, d.asset).
    - If asset.calculate\_depreciation.
      - Evaluate reverse\_depreciation\_entry\_made\_on\_disposal(asset).
      - Set note from self.get\_note\_for\_asset\_return(asset).
      - Evaluate reset\_depreciation\_schedule(asset, note).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get note for asset return](operations-102.md#op-ca5645b80930ae).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Asset”, d.asset).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1039)

<a id="op-ca5645b80930ae"></a>
### Sales Invoice.get note for asset return

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_note_for_asset_return`

**Inputs** self, asset.

**Explicit results** translated “This schedule was created when Asset {0} was returned through Sales Invoice {1}.”.format(asset\_link, invoice\_link) · translated “This schedule was created when Asset {0} was restored due to Sales Invoice {1} cancellation.”.format(asset\_link, invoice\_link).

**Local steps**

- Set asset\_link from get\_link\_to\_form(asset.doctype, asset.name).
- Set invoice\_link from get\_link\_to\_form(self.doctype, self.get(“name”)).
- If self.is\_return.
  - Return translated “This schedule was created when Asset {0} was returned through Sales Invoice {1}.”.format(asset\_link, invoice\_link).
- Otherwise.
  - Return translated “This schedule was created when Asset {0} was restored due to Sales Invoice {1} cancellation.”.format(asset\_link, invoice\_link).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1020)

<a id="op-5a3a12b9930c39"></a>
### Sales Invoice.update asset

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_update_asset`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_cached\_doc.

**Local steps**

- Bind local operation \_update\_asset for subsequent calls.
- Set disposal\_date from self.get\_disposal\_date().
- For each d in self.get(“items”).
  - If d.asset.
    - Set asset from Platform.get\_cached\_doc(“Asset”, d.asset).
    - If ((self.is\_return and self.docstatus equals 1) or (not self.is\_return and self.docstatus equals 2)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.is\_return and self.docstatus equals 1) → (not self.is\_return and self.docstatus equals 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.docstatus equals 1.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → self.docstatus equals 2.
      - Set note from translated “Asset returned” when self.is\_return, otherwise translated “Asset sold”.
        - Value choice on self.is\_return — true gives translated “Asset returned”, false gives translated “Asset sold”.
      - Set tuple(asset\_status, disposal\_date) from tuple(no value, no value).
    - Otherwise.
      - Set note from translated “Asset sold” when not self.is\_return, otherwise translated “Return invoice of asset cancelled”.
        - Value choice on not self.is\_return — true gives translated “Asset sold”, false gives translated “Return invoice of asset cancelled”.
      - Set asset\_status from “Sold”.
    - Evaluate \_update\_asset(asset, disposal\_date, note, asset\_status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get disposal date](operations-102.md#op-7b77f56c5f6393).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Asset”, d.asset).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1047)

<a id="op-5454cbd8ecf23c"></a>
### Sales Invoice.update asset.update asset

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_update_asset_update_asset`

**Inputs** asset, disposal\_date, note, asset\_status = no value.

**State and service calls** call db\_set on asset.

**Local steps**

- Evaluate asset.db\_set(“disposal\_date”, disposal\_date).
- Evaluate add\_asset\_activity(asset.name, note).
- Evaluate asset.set\_status(asset\_status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1048)

<a id="op-7b77f56c5f6393"></a>
### Sales Invoice.get disposal date

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_disposal_date`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_value.

**Explicit results** disposal\_date.

**Local steps**

- If self.is\_return.
  - Set disposal\_date from Platform.db.get\_value(“Sales Invoice”, self.return\_against, “posting\_date”).
- Otherwise.
  - Set disposal\_date from self.posting\_date.
- Return disposal\_date.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1016)

<a id="op-cb5da2401ff5c4"></a>
### Sales Invoice.make gl entries

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_make_general_ledger_entries`

**Inputs** self, gl\_entries = no value, from\_repost = false.

**Local steps**

- Bind dependencies make\_gl\_entries, make\_reverse\_gl\_entries.
- Set auto\_accounting\_for\_stock from Enterprise.is\_perpetual\_inventory\_enabled(self.company).
- If not gl\_entries.
  - Set gl\_entries from self.get\_gl\_entries().
- If gl\_entries.
  - Set update\_outstanding from “No” when (cint(self.is\_pos) or self.write\_off\_account or cint(self.redeem\_loyalty\_points)), otherwise “Yes”.
    - Value choice on (cint(self.is\_pos) or self.write\_off\_account or cint(self.redeem\_loyalty\_points)) — true gives “No”, false gives “Yes”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(self.is\_pos) → self.write\_off\_account → cint(self.redeem\_loyalty\_points).
  - If self.docstatus equals 1.
    - Evaluate make\_gl\_entries(gl\_entries, update\_outstanding = update\_outstanding, merge\_entries = false, from\_repost = from\_repost).
    - Evaluate self.make\_exchange\_gain\_loss\_journal().
  - Otherwise.
    - If self.docstatus equals 2.
      - Evaluate make\_reverse\_gl\_entries(voucher\_type = self.doctype, voucher\_no = self.name).
  - If update\_outstanding equals “No”.
    - Evaluate update\_voucher\_outstanding(voucher\_type = self.doctype, voucher\_no = self.return\_against when (cint(self.is\_return) and self.return\_against), otherwise self.name, account = self.debit\_to, party\_type = “Customer”, …).
      - Value choice on (cint(self.is\_return) and self.return\_against) — true gives self.return\_against, false gives self.name.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.return\_against.
- Otherwise.
  - If (self.docstatus equals 2 and cint(self.update\_stock) and cint(auto\_accounting\_for\_stock)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 2 → cint(self.update\_stock) → cint(auto\_accounting\_for\_stock).
    - Evaluate make\_reverse\_gl\_entries(voucher\_type = self.doctype, voucher\_no = self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl entries](operations-102.md#op-d8e8ed58702719).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L359) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1028) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1158)

<a id="op-d8e8ed58702719"></a>
### Sales Invoice.get gl entries

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map = no value.

**Explicit results** gl\_entries.

**Local steps**

- Bind dependencies merge\_similar\_entries.
- Set gl\_entries from list().
- Set deferred\_return\_items from self.get\_deferred\_return\_items().
- Evaluate self.make\_customer\_gl\_entry(gl\_entries).
- Evaluate self.make\_tax\_gl\_entries(gl\_entries).
- Evaluate self.make\_internal\_transfer\_gl\_entries(gl\_entries).
- Evaluate self.make\_item\_gl\_entries(gl\_entries, deferred\_return\_items).
- Evaluate self.make\_precision\_loss\_gl\_entry(gl\_entries).
- Evaluate self.make\_discount\_gl\_entries(gl\_entries, deferred\_return\_items).
- Set gl\_entries from make\_regional\_gl\_entries(gl\_entries, self).
- Set gl\_entries from merge\_similar\_entries(gl\_entries).
- Evaluate self.make\_loyalty\_point\_redemption\_gle(gl\_entries).
- Evaluate self.make\_pos\_gl\_entries(gl\_entries).
- Evaluate self.make\_write\_off\_gl\_entry(gl\_entries).
- Evaluate self.make\_gle\_for\_rounding\_adjustment(gl\_entries).
- Evaluate self.set\_transaction\_currency\_and\_rate\_in\_gl\_map(gl\_entries).
- Return gl\_entries.

**Methods declared on this owner** [get deferred return items](operations-102.md#op-e34902256f09a9), [make customer gl entry](operations-102.md#op-664674b442dedb), [make tax gl entries](operations-102.md#op-969c46fe91966c), [make internal transfer gl entries](operations-102.md#op-1d93d8b6a7f697), [make item gl entries](operations-102.md#op-a71e8f6c432189), [make loyalty point redemption gle](operations-102.md#op-882bacbaa5b4d0), [make pos gl entries](operations-102.md#op-99ee5afc9c16f7), [make write off gl entry](operations-102.md#op-174c41ed90822f), [make gle for rounding adjustment](operations-102.md#op-f1847263b3ca21).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1024) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1154)

<a id="op-664674b442dedb"></a>
### Sales Invoice.make customer gl entry

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_customer_gl_entry`

**Inputs** self, gl\_entries.

**Local steps**

- Set grand\_total from self.rounded\_total when (self.rounding\_adjustment and self.rounded\_total), otherwise self.grand\_total.
  - Value choice on (self.rounding\_adjustment and self.rounded\_total) — true gives self.rounded\_total, false gives self.grand\_total.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.rounding\_adjustment → self.rounded\_total.
- Set base\_grand\_total from flt(self.base\_rounded\_total when (self.base\_rounding\_adjustment and self.base\_rounded\_total), otherwise self.base\_grand\_total, self.precision(“base\_grand\_total”)).
  - Value choice on (self.base\_rounding\_adjustment and self.base\_rounded\_total) — true gives self.base\_rounded\_total, false gives self.base\_grand\_total.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.base\_rounding\_adjustment → self.base\_rounded\_total.
- If (grand\_total and not self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in grand\_total → not self.is\_internal\_transfer().
  - Set against\_voucher from self.name.
  - If (self.is\_return and self.return\_against and not self.update\_outstanding\_for\_self).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → not self.update\_outstanding\_for\_self.
    - Set against\_voucher from self.return\_against.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.debit\_to, “party\_type” → “Customer”, “party” → self.customer, “due\_date” → self.due\_date, …), self.party\_account\_currency, item = self)).
    - Value choice on self.party\_account\_currency equals self.company\_currency — true gives base\_grand\_total, false gives grand\_total.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1028)

<a id="op-969c46fe91966c"></a>
### Sales Invoice.make tax gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_tax_gl_entries`

**Inputs** self, gl\_entries.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Local steps**

- Set enable\_discount\_accounting from cint(Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”)).
- For each tax in self.get(“taxes”).
  - Set tuple(amount, base\_amount) from self.get\_tax\_amounts(tax, enable\_discount\_accounting).
  - If flt(tax.base\_tax\_amount\_after\_discount\_amount).
    - Set account\_currency from get\_account\_currency(tax.account\_head).
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → tax.account\_head, “against” → self.customer, “credit” → flt(base\_amount, tax.precision(“tax\_amount\_after\_discount\_amount”)), “credit\_in\_account\_curren ….
      - Value choice on account\_currency equals self.company\_currency — true gives flt(base\_amount, tax.precision(“base\_tax\_amount\_after\_discount\_amount”)), false gives flt(amount, tax.precision(“tax\_amount\_after\_discount\_amount”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1035)

<a id="op-1d93d8b6a7f697"></a>
### Sales Invoice.make internal transfer gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_internal_transfer_gl_entries`

**Inputs** self, gl\_entries.

**Local steps**

- If (self.is\_internal\_transfer() and flt(self.base\_total\_taxes\_and\_charges)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → flt(self.base\_total\_taxes\_and\_charges).
  - Set account\_currency from get\_account\_currency(self.unrealized\_profit\_loss\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.unrealized\_profit\_loss\_account, “against” → self.customer, “debit” → flt(self.total\_taxes\_and\_charges), “debit\_in\_account\_currency” → flt(self.ba ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1030)

<a id="op-a71e8f6c432189"></a>
### Sales Invoice.make item gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_item_gl_entries`

**Inputs** self, gl\_entries, deferred\_return\_items = no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Local steps**

- Set enable\_discount\_accounting from cint(Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”)).
- For each item in self.get(“items”).
  - If (flt(item.base\_net\_amount, item.precision(“base\_net\_amount”)) or item.is\_fixed\_asset or enable\_discount\_accounting).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.base\_net\_amount, item.precision(“base\_net\_amount”)) → item.is\_fixed\_asset → enable\_discount\_accounting.
    - If self.is\_internal\_transfer().
      - Continue with the next iteration or loop test.
    - If (item.is\_fixed\_asset and item.asset).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_fixed\_asset → item.asset.
      - Evaluate self.get\_gl\_entries\_for\_fixed\_asset(item, gl\_entries).
    - Otherwise.
      - Set income\_account from self.get\_item\_income\_account(item, deferred\_return\_items).
      - Set tuple(amount, base\_amount) from self.get\_amount\_and\_base\_amount(item, enable\_discount\_accounting).
      - Set account\_currency from get\_account\_currency(income\_account).
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → income\_account, “voucher\_detail\_no” → item.name when (self.is\_return and item.enable\_deferred\_revenue), otherwise no value, “against” → self.customer, ….
        - Value choice on (self.is\_return and item.enable\_deferred\_revenue) — true gives item.name, false gives no value.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → item.enable\_deferred\_revenue.
        - Value choice on account\_currency equals self.company\_currency — true gives flt(base\_amount, item.precision(“base\_net\_amount”)), false gives flt(amount, item.precision(“net\_amount”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
- If (cint(self.update\_stock) and Enterprise.is\_perpetual\_inventory\_enabled(self.company)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.update\_stock) → Enterprise.is\_perpetual\_inventory\_enabled(self.company).
  - Update gl\_entries using + super().get\_gl\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl entries for fixed asset](operations-102.md#op-2b0c9da0601291), [get item income account](operations-102.md#op-f7432a6f7ebfac).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1031)

<a id="op-f7432a6f7ebfac"></a>
### Sales Invoice.get item income account

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_item_income_account`

**Inputs** self, item, deferred\_return\_items = no value.

**Explicit results** item.income\_account · item.deferred\_revenue\_account.

**Local steps**

- If not item.enable\_deferred\_revenue.
  - Return item.income\_account.
- If not self.is\_return.
  - Return item.deferred\_revenue\_account.
- If (not self.return\_against or not item.sales\_invoice\_item).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.return\_against → not item.sales\_invoice\_item.
  - Return item.income\_account.
- If deferred\_return\_items is identical to no value.
  - Set deferred\_return\_items from self.get\_deferred\_return\_items().
- If item.name belongs to deferred\_return\_items.
  - Return item.deferred\_revenue\_account.
- Return item.income\_account.

**Methods declared on this owner** [get deferred return items](operations-102.md#op-e34902256f09a9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1019)

<a id="op-e34902256f09a9"></a>
### Sales Invoice.get deferred return items

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_deferred_return_items`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_value · read “GL Entry” via get\_all · resolve a document from “Sales Invoice” via get\_cached\_doc.

**Explicit results** set() · deferred\_items.

**Local steps**

- If (not self.is\_return or not self.return\_against).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_return → not self.return\_against.
  - Return set().
- Set items from list of item for item drawn from self.items where (item.enable\_deferred\_revenue and item.sales\_invoice\_item).
  - Draw item from self.items, keep a combination only if ((item.enable\_deferred\_revenue and item.sales\_invoice\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.enable\_deferred\_revenue → item.sales\_invoice\_item.
- If not items.
  - Return set().
- Evaluate Platform.db.get\_value(“Sales Invoice”, self.return\_against, “name”, for\_update = true).
- Set entries from set of tuple(entry.voucher\_detail\_no, entry.account) for entry drawn from Platform.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → “Sales Invoice”, “voucher\_no” → self.name, “is\_cancelled” → 0), fie ….
  - Draw entry from Platform.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → “Sales Invoice”, “voucher\_no” → self.name, “is\_cancelled” → 0), fields = list(“voucher\_detail\_no”, “account”)).
- Set deferred\_items from set of item.name for item drawn from items where tuple(item.name, item.deferred\_revenue\_account) belongs to entries.
  - Draw item from items, keep a combination only if (tuple(item.name, item.deferred\_revenue\_account) belongs to entries).
- Set items from list of item for item drawn from items where item.name does not belong to deferred\_items.
  - Draw item from items, keep a combination only if (item.name does not belong to deferred\_items).
- If not items.
  - Return deferred\_items.
- Set invoice from Platform.get\_cached\_doc(“Sales Invoice”, self.return\_against).
- Set original\_names from set of item.sales\_invoice\_item for item drawn from items.
  - Draw item from items.
- Set original\_items from mapping of item.name → item for item drawn from invoice.items where (item.name belongs to original\_names and item.enable\_deferred\_revenue).
  - Draw item from invoice.items, keep a combination only if ((item.name belongs to original\_names and item.enable\_deferred\_revenue)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.name belongs to original\_names → item.enable\_deferred\_revenue.
- Set booked\_amounts from get\_already\_booked\_amounts(invoice, list(original\_items.values())).
- For each item in items.
  - Set original\_item from original\_items.get(item.sales\_invoice\_item).
  - If (original\_item and original\_item.deferred\_revenue\_account equals item.deferred\_revenue\_account and not any(booked\_amounts at original\_item.name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in original\_item → original\_item.deferred\_revenue\_account equals item.deferred\_revenue\_account → not any(booked\_amounts at original\_item.name).
    - Evaluate deferred\_items.add(item.name).
- Return deferred\_items.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Sales Invoice”, self.return\_against).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1015)

<a id="op-2b0c9da0601291"></a>
### Sales Invoice.get gl entries for fixed asset

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_gl_entries_for_fixed_asset`

**Inputs** self, item, gl\_entries.

**Record and data access** resolve a document from “Asset” via get\_cached\_doc.

**Local steps**

- Set asset from Platform.get\_cached\_doc(“Asset”, item.asset).
- Set disposal\_values from get\_stored\_asset\_disposal\_values(item).
- If self.is\_return.
  - Set fixed\_asset\_gl\_entries from get\_gl\_entries\_on\_asset\_regain(asset, item.base\_net\_amount, item.finance\_book, self.get(“doctype”), …).
- Otherwise.
  - Set fixed\_asset\_gl\_entries from get\_gl\_entries\_on\_asset\_disposal(asset, item.base\_net\_amount, item.finance\_book, self.get(“doctype”), …).
- For each gle in fixed\_asset\_gl\_entries.
  - Set gle at “against” from self.customer.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(gle, item = item)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Asset”, item.asset).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1017)

<a id="op-67283ab5a6a5de"></a>
### Sales Invoice.enable discount accounting

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_enable_discount_accounting`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** self.\_enable\_discount\_accounting.

**Local steps**

- If not hasattr(self, “\_enable\_discount\_accounting”).
  - Set self.\_enable\_discount\_accounting from cint(Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”)).
- Return self.\_enable\_discount\_accounting.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L1106) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1021) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1151)

<a id="op-882bacbaa5b4d0"></a>
### Sales Invoice.make loyalty point redemption gle

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_loyalty_point_redemption_gle`

**Inputs** self, gl\_entries.

**Local steps**

- If cint((self.redeem\_loyalty\_points and self.loyalty\_points)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.redeem\_loyalty\_points → self.loyalty\_points.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.debit\_to, “party\_type” → “Customer”, “party” → self.customer, “against” → ((“Expense account - ” + cstr(nested operand in the contract.loyalty\_re ….
    - Value choice on cint(self.is\_return) — true gives self.return\_against, false gives self.name.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.loyalty\_redemption\_account, “cost\_center” → (self.cost\_center or self.loyalty\_redemption\_cost\_center), “against” → self.customer, “debit” → self. ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → self.loyalty\_redemption\_cost\_center.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1033)

<a id="op-99ee5afc9c16f7"></a>
### Sales Invoice.make pos gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_pos_gl_entries`

**Inputs** self, gl\_entries.

**Record and data access** read “POS Settings” via get\_single\_value.

**Local steps**

- If cint(self.is\_pos).
  - Set skip\_change\_gl\_entries from not cint(Platform.get\_single\_value(“POS Settings”, “post\_change\_gl\_entries”)).
  - For each payment\_mode in self.payments.
    - If (skip\_change\_gl\_entries and payment\_mode.account equals self.account\_for\_change\_amount).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in skip\_change\_gl\_entries → payment\_mode.account equals self.account\_for\_change\_amount.
      - Update payment\_mode.base\_amount using − flt(self.base\_change\_amount).
    - Set against\_voucher from self.name.
    - If (self.is\_return and self.return\_against and not self.update\_outstanding\_for\_self).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → not self.update\_outstanding\_for\_self.
      - Set against\_voucher from self.return\_against.
    - If payment\_mode.base\_amount.
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.debit\_to, “party\_type” → “Customer”, “party” → self.customer, “against” → payment\_mode.account, …), self.party\_account\_currency, item = self)).
        - Value choice on self.party\_account\_currency equals self.company\_currency — true gives payment\_mode.base\_amount, false gives payment\_mode.amount.
      - Set payment\_mode\_account\_currency from get\_account\_currency(payment\_mode.account).
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → payment\_mode.account, “against” → self.customer, “debit” → payment\_mode.base\_amount, “debit\_in\_account\_currency” → payment\_mode.base\_amount when payme ….
        - Value choice on payment\_mode\_account\_currency equals self.company\_currency — true gives payment\_mode.base\_amount, false gives payment\_mode.amount.
  - If not skip\_change\_gl\_entries.
    - Evaluate gl\_entries.extend(self.get\_gle\_for\_change\_amount()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gle for change amount](operations-102.md#op-15fce6f0b006b9).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“POS Settings”, “post\_change\_gl\_entries”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1034)

<a id="op-15fce6f0b006b9"></a>
### Sales Invoice.get gle for change amount

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_gle_for_change_amount`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** list() · list(self.get\_gl\_dict(mapping(“account” → self.debit\_to, “party\_type” → “Customer”, “party” → self.customer, “against” → self.account\_for\_change\_amount, …), self.party\_account\_currency, item = self), self. ….

**Explicit failure paths** validation helper — translated “Please set Account for Change Amount”.

**Local steps**

- If not self.change\_amount.
  - Return list().
- If not self.account\_for\_change\_amount.
  - Call the validation error handler Platform.throw(translated “Please set Account for Change Amount”, title = translated “Mandatory Field”).
- Return list(self.get\_gl\_dict(mapping(“account” → self.debit\_to, “party\_type” → “Customer”, “party” → self.customer, “against” → self.account\_for\_change\_amount, …), self.party\_account\_currency, item = self), self. ….
  - Value choice on self.party\_account\_currency equals self.company\_currency — true gives flt(self.base\_change\_amount), false gives flt(self.change\_amount).
  - Value choice on (cint(self.is\_return) and self.return\_against) — true gives self.return\_against, false gives self.name.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.return\_against.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1018)

<a id="op-174c41ed90822f"></a>
### Sales Invoice.make write off gl entry

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_write_off_gl_entry`

**Inputs** self, gl\_entries.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If (self.is\_pos and self.write\_off\_account and flt(self.write\_off\_amount, self.precision(“write\_off\_amount”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_pos → self.write\_off\_account → flt(self.write\_off\_amount, self.precision(“write\_off\_amount”)).
  - Set write\_off\_account\_currency from get\_account\_currency(self.write\_off\_account).
  - Set default\_cost\_center from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.debit\_to, “party\_type” → “Customer”, “party” → self.customer, “against” → self.write\_off\_account, …), self.party\_account\_currency, item = self)).
    - Value choice on self.party\_account\_currency equals self.company\_currency — true gives flt(self.base\_write\_off\_amount, self.precision(“base\_write\_off\_amount”)), false gives flt(self.write\_off\_amount, self.precision(“write\_off\_amount”)).
    - Value choice on cint(self.is\_return) — true gives self.return\_against, false gives self.name.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.write\_off\_account, “against” → self.customer, “debit” → flt(self.base\_write\_off\_amount, self.precision(“base\_write\_off\_amount”)), “debit\_in\_accou ….
    - Value choice on write\_off\_account\_currency equals self.company\_currency — true gives flt(self.base\_write\_off\_amount, self.precision(“base\_write\_off\_amount”)), false gives flt(self.write\_off\_amount, self.precision(“write\_off\_amount”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → self.write\_off\_cost\_center → default\_cost\_center.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1036)

<a id="op-f1847263b3ca21"></a>
### Sales Invoice.make gle for rounding adjustment

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_gle_for_rounding_adjustment`

**Inputs** self, gl\_entries.

**Explicit failure paths** validation helper — translated “Opening Invoice has rounding adjustment of {0}.&lt;br&gt;&lt;br&gt; '{1}' account is required to post these values. Plea …”.format(Platform.bold(self.rounding\_adjustment), Platform.bold(“Round Off for Open ….

**Local steps**

- If (flt(self.rounding\_adjustment, self.precision(“rounding\_adjustment”)) and self.base\_rounding\_adjustment and not self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.rounding\_adjustment, self.precision(“rounding\_adjustment”)) → self.base\_rounding\_adjustment → not self.is\_internal\_transfer().
  - Set tuple(round\_off\_account, round\_off\_cost\_center, round\_off\_for\_opening) from get\_round\_off\_account\_and\_cost\_center(self.company, “Sales Invoice”, self.name, self.use\_company\_roundoff\_cost\_center).
  - If (self.is\_opening equals “Yes” and self.rounding\_adjustment).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_opening equals “Yes” → self.rounding\_adjustment.
    - If not round\_off\_for\_opening.
      - Call the validation error handler Platform.throw(translated “Opening Invoice has rounding adjustment of {0}.&lt;br&gt;&lt;br&gt; '{1}' account is required to post these values. Plea …”.format(Platform.bold(self.rounding\_adjustment), Platform.bold(“Rou ….
    - Otherwise.
      - Set round\_off\_account from round\_off\_for\_opening.
  - Set rounding\_adjustment from flt(self.rounding\_adjustment, self.precision(“rounding\_adjustment”)).
  - Set base\_rounding\_adjustment from flt(self.base\_rounding\_adjustment, self.precision(“base\_rounding\_adjustment”)).
  - Set round\_off\_account\_currency from get\_account\_currency(round\_off\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → round\_off\_account, “against” → self.customer, “credit\_in\_account\_currency” → base\_rounding\_adjustment when round\_off\_account\_currency equals self.comp ….
    - Value choice on round\_off\_account\_currency equals self.company\_currency — true gives base\_rounding\_adjustment, false gives rounding\_adjustment.
    - Value choice on self.use\_company\_roundoff\_cost\_center — true gives round\_off\_cost\_center, false gives (self.cost\_center or round\_off\_cost\_center).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → round\_off\_cost\_center.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1029)

<a id="op-6b15b2f5e31a98"></a>
### Sales Invoice.update billing status in dn

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_update_billing_status_in_record_name`

**Inputs** self, update\_modified = true.

**Record and data access** resolve a document from “Delivery Note” via get\_doc.

**State and service calls** request set\_value on “Delivery Note Item”.

**Explicit results** no value.

**Local steps**

- If (self.is\_return and not self.update\_billed\_amount\_in\_delivery\_note).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not self.update\_billed\_amount\_in\_delivery\_note.
  - Return no value.
- Set updated\_delivery\_notes from list().
- Set SalesInvoiceItem from Platform.qb.DocType(“Sales Invoice Item”).
- Bind dependencies Coalesce, Sum.
- For each d in self.get(“items”).
  - If d.dn\_detail.
    - Set query from nested operand in the contract(nested operand in the contract).select(Coalesce(nested operand in the contract(nested operand in the contract), 0)).where(SalesInvoiceItem.dn\_detail equals d.dn\_detail).where ….
    - Set res from query.run().
    - Set billed\_amt from res at 0 at 0 when res, otherwise 0.
      - Value choice on res — true gives res at 0 at 0, false gives 0.
    - Evaluate Platform.db.set\_value(“Delivery Note Item”, d.dn\_detail, “billed\_amt”, billed\_amt, update\_modified = update\_modified).
    - Evaluate updated\_delivery\_notes.append(d.delivery\_note).
  - Otherwise.
    - If d.so\_detail.
      - Update updated\_delivery\_notes using + update\_billed\_amount\_based\_on\_so(d.so\_detail, update\_modified).
- For each dn in set(updated\_delivery\_notes).
  - Evaluate Platform.get\_doc(“Delivery Note”, dn).update\_billing\_percentage(update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L1245) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1044) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1174)

<a id="op-ee8b178f1ed41d"></a>
### Sales Invoice.on recurring

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_on_recurring`

**Inputs** self, reference\_doc, auto\_repeat\_doc.

**Local steps**

- Evaluate super().on\_recurring(reference\_doc, auto\_repeat\_doc).
- Evaluate self.set(“write\_off\_amount”, reference\_doc.get(“write\_off\_amount”)).
- Set self.po\_no from reference\_doc.po\_no.
- Set self.payment\_terms\_template from reference\_doc.payment\_terms\_template.
- Set self.due\_date from no value.
- Evaluate self.shift\_service\_dates(reference\_doc, auto\_repeat\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1030) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1160)

<a id="op-aafaca2828d274"></a>
### Sales Invoice.update project

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_update_project`

**Inputs** self.

**Record and data access** resolve a document from “Project” via get\_doc.

**State and service calls** call db\_update on project.

**Local steps**

- Set unique\_projects from list(set(list of d.project for d drawn from self.get(“items”) where d.project)).
  - Draw d from self.get(“items”), keep a combination only if (d.project).
- If (self.project and self.project does not belong to unique\_projects).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project → self.project does not belong to unique\_projects.
  - Evaluate unique\_projects.append(self.project).
- For each p in unique\_projects.
  - Set project from Platform.get\_doc(“Project”, p).
  - Evaluate project.update\_billed\_amount().
  - Evaluate project.calculate\_gross\_margin().
  - Evaluate project.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L1984) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1047) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1177)

<a id="op-8a65cdee3fa796"></a>
### Sales Invoice.verify payment amount is positive

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_verify_payment_amount_is_positive`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0} (Payment Table): Amount must be positive”.format(entry.idx).

**Local steps**

- For each entry in self.payments.
  - <a id="op-8a65cdee3fa796-guard-3"></a>If entry.amount &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0} (Payment Table): Amount must be positive”.format(entry.idx)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison entry.amount &lt; 0, entry.amount = -1 selects the branch that calls the validation-error handler with translated “Row #{0} (Payment Table): Amount must be positive”.format(entry.idx). With entry.amount = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8a65cdee3fa796-guard-3)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1062)
