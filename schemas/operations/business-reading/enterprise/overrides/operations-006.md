# Regional rules and controller overrides · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Vat audit report

<a id="op-db95bfe50c9518"></a>
### VATAudit Report.get invoice filters

`operation_enterprise_binding_enterprise_regional_report_vat_audit_report_vat_audit_report_vatauditreport_get_invoice_filters`

**Inputs** self.

**Explicit results** filters.

**Local steps**

- Set filters from list(list(“docstatus”, “=”, 1), list(“is\_opening”, “=”, “No”)).
- If self.filters.get(“company”).
  - Evaluate filters.append(list(“company”, “=”, self.filters.company)).
- If self.filters.get(“from\_date”).
  - Evaluate filters.append(list(“posting\_date”, “&gt;=”, self.filters.from\_date)).
- If self.filters.get(“to\_date”).
  - Evaluate filters.append(list(“posting\_date”, “&lt;=”, self.filters.to\_date)).
- Return filters.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1426)

<a id="op-d77b4691558629"></a>
### VATAudit Report.get invoice items

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_get_invoice_items`

**Inputs** self, doctype.

**Local steps**

- Set item\_doctype from Platform.qb.DocType((doctype + “ Item”)).
- Set items from nested operand in the contract(nested operand in the contract).select(item\_doctype.name, item\_doctype.is\_zero\_rated, item\_doctype.base\_net\_amount).where(item\_doctype.parent.isin(list(nested operand in the  ….
- Set self.invoice\_items from Platform.\_dict(mapping of item.name → item for item drawn from items).
  - Draw item from items.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1042)

<a id="op-7d8c1dfd51c060"></a>
### VATAudit Report.get items based on tax rate

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_get_items_based_on_tax_rate`

**Inputs** self, doctype.

**Explicit results** no value.

**Local steps**

- Set self.items\_based\_on\_tax\_rate from Platform.\_dict().
- Set self.tax\_doctype from “Purchase Taxes and Charges” when doctype equals “Purchase Invoice”, otherwise “Sales Taxes and Charges”.
  - Value choice on doctype equals “Purchase Invoice” — true gives “Purchase Taxes and Charges”, false gives “Sales Taxes and Charges”.
- Set taxes\_and\_charges from Platform.qb.DocType(self.tax\_doctype).
- Set item\_wise\_tax from Platform.qb.DocType(“Item Wise Tax Detail”).
- Set invoice\_names from list(self.invoices.keys()).
- If not invoice\_names.
  - Return no value.
- Set tax\_details from nested operand in the contract(nested operand in the contract, nested operand in the contract).select(item\_wise\_tax.tax\_row).where(item\_wise\_tax.parent.isin(invoice\_names)).where(taxes\_and\_charges.account\_ ….
- If doctype equals “Purchase Invoice”.
  - Set tax\_details from tax\_details.select(taxes\_and\_charges.add\_deduct\_tax).
- Set tax\_details from tax\_details.run(as\_dict = true).
- Set actual\_tax\_rates from get\_actual\_tax\_rates(tax\_details).
- For each row in tax\_details.
  - Set is\_zero\_rated from self.invoice\_items.get(row.item\_row, mapping()).get(“is\_zero\_rated”).
  - If row.charge\_type equals “Actual”.
    - Set row.rate from actual\_tax\_rates.get(row.tax\_row, 0).
  - If (row.rate equals 0 and not is\_zero\_rated).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.rate equals 0 → not is\_zero\_rated.
    - Continue with the next iteration or loop test.
  - Evaluate self.add\_item\_tax(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add item tax](operations-006.md#op-74ff7dda64ce4a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1043)

<a id="op-74ff7dda64ce4a"></a>
### VATAudit Report.add item tax

`operation_enterprise_binding_enterprise_regional_report_vat_audit_report_vat_audit_report_vatauditreport_add_item_tax`

**Inputs** self, row.

**Declared result** no value.

**Local steps**

- Set is\_deduct from row.add\_deduct\_tax equals “Deduct”.
- Set totals from self.items\_based\_on\_tax\_rate.setdefault(row.parent, mapping()).setdefault(tuple(row.rate, is\_deduct), mapping(“gross\_amount” → 0.0, “tax\_amount” → 0.0, “net\_amount” → 0.0, “items” → set())).
- Set net\_amount from 0.0.
- If row.item\_row does not belong to totals at “items”.
  - Evaluate totals at “items”.add(row.item\_row).
  - Set net\_amount from self.get\_deducted\_net\_amount(row) when is\_deduct, otherwise row.taxable\_amount.
    - Value choice on is\_deduct — true gives self.get\_deducted\_net\_amount(row), false gives row.taxable\_amount.
- Update totals at “tax\_amount” using + row.amount.
- Update totals at “net\_amount” using + net\_amount.
- Update totals at “gross\_amount” using + (row.amount + net\_amount).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get deducted net amount](operations-006.md#op-f48d5947a97c12).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1424)

<a id="op-f48d5947a97c12"></a>
### VATAudit Report.get deducted net amount

`operation_enterprise_binding_enterprise_regional_report_vat_audit_report_vat_audit_report_vatauditreport_get_deducted_net_amount`

**Inputs** self, row.

**Declared result** float.

**Explicit results** (abs(flt(row.taxable\_amount)) × sign).

**Local steps**

- Set item\_net\_amount from flt(self.invoice\_items.get(row.item\_row, mapping()).get(“base\_net\_amount”)).
- Set sign from negative 1 when item\_net\_amount &lt; 0, otherwise 1.
  - Value choice on item\_net\_amount &lt; 0 — true gives negative 1, false gives 1.
- Return (abs(flt(row.taxable\_amount)) × sign).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1425)

<a id="op-36b3e0e3b9e68c"></a>
### VATAudit Report.get data

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_get_data`

**Inputs** self, doctype.

**Local steps**

- Set consolidated\_data from self.get\_consolidated\_data(doctype).
- Set section\_name from translated “Purchases” when doctype equals “Purchase Invoice”, otherwise translated “Sales”.
  - Value choice on doctype equals “Purchase Invoice” — true gives translated “Purchases”, false gives translated “Sales”.
- For each tuple(rate, section) in consolidated\_data.items().
  - Set rate from int(rate).
  - Set label from Platform.bold((((((section\_name + “- ”) + “Rate”) + one space) + str(rate)) + “%”)).
  - Set section\_head from mapping(“posting\_date” → label).
  - Set total\_gross, total\_tax, total\_net from 0.
  - Evaluate self.data.append(section\_head).
  - For each row in section.get(“data”).
    - Evaluate self.data.append(row).
    - Update total\_gross using + row at “gross\_amount”.
    - Update total\_tax using + row at “tax\_amount”.
    - Update total\_net using + row at “net\_amount”.
  - Set total from mapping(“posting\_date” → Platform.bold(translated “Total”), “gross\_amount” → total\_gross, “tax\_amount” → total\_tax, “net\_amount” → total\_net, …).
  - Evaluate self.data.append(total).
  - Evaluate self.data.append(mapping()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get consolidated data](operations-006.md#op-fef22122fbce7e).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0622.json#L2292) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1040)

<a id="op-fef22122fbce7e"></a>
### VATAudit Report.get consolidated data

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_get_consolidated_data`

**Inputs** self, doctype.

**Explicit results** consolidated\_data\_map.

**Local steps**

- Set consolidated\_data\_map from mapping().
- For each tuple(inv, inv\_data) in self.invoices.items().
  - Set rate\_details from self.items\_based\_on\_tax\_rate.get(inv, mapping()).
  - If not rate\_details.
    - Continue with the next iteration or loop test.
  - For each tuple(tuple(rate, \_is\_deduct), item\_details) in rate\_details.items().
    - Set row from mapping(“tax\_amount” → 0.0, “gross\_amount” → 0.0, “net\_amount” → 0.0).
    - Set row at “account” from inv\_data.get(“account”).
    - Set row at “posting\_date” from formatdate(inv\_data.get(“posting\_date”), “dd-mm-yyyy”).
    - Set row at “voucher\_type” from doctype.
    - Set row at “voucher\_no” from inv.
    - Set row at “party\_type” from “Customer” when doctype equals “Sales Invoice”, otherwise “Supplier”.
      - Value choice on doctype equals “Sales Invoice” — true gives “Customer”, false gives “Supplier”.
    - Set row at “party” from inv\_data.get(“party”).
    - Set row at “remarks” from inv\_data.get(“remarks”).
    - Update row at “gross\_amount” using + item\_details.get(“gross\_amount”).
    - Update row at “tax\_amount” using + item\_details.get(“tax\_amount”).
    - Update row at “net\_amount” using + item\_details.get(“net\_amount”).
    - Evaluate consolidated\_data\_map.setdefault(rate, mapping(“data” → list())).
    - Evaluate consolidated\_data\_map at rate at “data”.append(row).
- Return consolidated\_data\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1039)

<a id="op-c0fb55a04986b1"></a>
### VATAudit Report.get columns

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list(mapping(“fieldname” → “posting\_date”, “label” → “Posting Date”, “fieldtype” → “Data”, “width” → 200), mapping(“fieldname” → “account”, “label” → “Account”, “fieldtype” → “Link”, “options” → “Account”, ….

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0622.json#L3713) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1038)

<a id="op-e53c0abcb0a3f7"></a>
### Get actual tax rates

`operation_enterprise_binding_enterprise_regional_report_vat_audit_report_vat_audit_report_get_actual_tax_rates`

**Inputs** tax\_details.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of tax\_row → flt(((amount ÷ taxable\_amount) × 100), 2) for tuple(tax\_row, tuple(amount, taxable\_amount)) drawn from totals.items() where taxable\_amount.

**Local steps**

- Set totals from mapping().
- For each row in tax\_details.
  - If row.charge\_type equals “Actual”.
    - Set tuple(amount, taxable\_amount) from totals.get(row.tax\_row, tuple(0.0, 0.0)).
    - Set totals at row.tax\_row from tuple((amount + flt(row.amount)), (taxable\_amount + flt(row.taxable\_amount))).
- Return mapping of tax\_row → flt(((amount ÷ taxable\_amount) × 100), 2) for tuple(tax\_row, tuple(amount, taxable\_amount)) drawn from totals.items() where taxable\_amount.
  - Draw tuple(tax\_row, tuple(amount, taxable\_amount)) from totals.items(), keep a combination only if (taxable\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1423)
