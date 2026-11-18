# Inventory and warehouses · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Landed cost report

<a id="op-bd168890409b1f"></a>
### Get data

`operation_enterprise_stock_report_landed_cost_report_business_behavior_get_data`

**Inputs** filters.

**Declared result** list at list.

**Explicit results** data.

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(filters.get(“company”)).
- Set landed\_cost\_vouchers from (get\_landed\_cost\_vouchers(filters) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_landed\_cost\_vouchers(filters) → mapping().
- Set landed\_vouchers from list(landed\_cost\_vouchers.keys()).
- Set vendor\_invoices from mapping().
- If landed\_vouchers.
  - Set vendor\_invoices from get\_vendor\_invoices(landed\_vouchers).
- Set data from list().
- For each tuple(name, vouchers) in landed\_cost\_vouchers.items().
  - Set res from mapping(“name” → name).
  - For each tuple(i, d) in enumerate(vouchers).
    - If i.
      - Set res from mapping().
    - Evaluate res.update(mapping(“landed\_cost” → d.landed\_cost, “voucher\_type” → d.voucher\_type, “voucher\_no” → d.voucher\_no, “currency” → company\_currency)).
    - Evaluate data.append(res).
  - For each vendor\_invoice in vendor\_invoices.get(name, list()).
    - Evaluate data.append(mapping(“vendor\_invoice” → vendor\_invoice)).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L234)

<a id="op-11fa083403a341"></a>
### Get landed cost vouchers

`operation_enterprise_stock_report_landed_cost_report_business_behavior_get_landed_cost_vouchers`

**Inputs** filters.

**Explicit results** result.

**Local steps**

- Set lcv from Platform.qb.DocType(“Landed Cost Voucher”).
- Set lcv\_voucher from Platform.qb.DocType(“Landed Cost Purchase Receipt”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….
- If (filters.from\_date and filters.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.from\_date → filters.to\_date.
  - Set query from query.where(lcv.posting\_date.between(filters.from\_date, filters.to\_date)).
- If filters.raw\_material\_voucher\_type.
  - Set query from query.where(lcv\_voucher.receipt\_document\_type equals filters.raw\_material\_voucher\_type).
- If filters.raw\_material\_voucher\_no.
  - Set query from query.where(lcv\_voucher.receipt\_document equals filters.raw\_material\_voucher\_no).
- Set data from (query.run(as\_dict = true) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = true) → list().
- Set allocations from get\_receipt\_allocations(set of row.name for row drawn from data).
  - Draw row from data.
- Set result from mapping().
- For each row in data.
  - Set row.landed\_cost from allocations.get(tuple(row.name, row.voucher\_type, row.voucher\_no), 0.0).
  - Evaluate result.setdefault(row.name, list()).append(row).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L235)

<a id="op-54f8a2ed43d759"></a>
### Get receipt allocations

`operation_enterprise_binding_enterprise_stock_report_landed_cost_report_landed_cost_report_get_receipt_allocations`

**Inputs** landed\_vouchers.

**Explicit results** mapping() · mapping of tuple(parent, doctype, name) → flt(amount) for tuple(parent, doctype, name, amount) drawn from rows.

**Local steps**

- If not landed\_vouchers.
  - Return mapping().
- Set item from Platform.qb.DocType(“Landed Cost Item”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(land ….run().
- Return mapping of tuple(parent, doctype, name) → flt(amount) for tuple(parent, doctype, name, amount) drawn from rows.
  - Draw tuple(parent, doctype, name, amount) from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L209) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L984)

<a id="op-24ba66aeab66d2"></a>
### Get vendor invoices

`operation_enterprise_stock_report_landed_cost_report_business_behavior_get_vendor_invoices`

**Inputs** landed\_vouchers.

**Explicit results** result.

**Local steps**

- Set doctype from Platform.qb.DocType(“Landed Cost Vendor Invoice”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.parent, doctype.vendor\_invoice).where((doctype.docstatus equals 1 bitwise and nested operand in the contract.parent.isin(landed ….
- Set data from (query.run(as\_dict = true) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run(as\_dict = true) → list().
- Set result from mapping().
- For each row in data.
  - Evaluate result.setdefault(row.parent, list()).append(row.vendor\_invoice).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0898.json#L706) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L236)

## Record · Landed cost voucher

[Record definition](../../../../data/record-types/landed_cost_voucher.json)

<a id="op-9e3364b33c6fa2"></a>
### Landed Cost Voucher.get items from purchase receipts

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_get_items_from_purchase_receipts`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set(“items”, list()).
- For each pr in self.get(“purchase\_receipts”).
  - If (pr.receipt\_document\_type and pr.receipt\_document).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pr.receipt\_document\_type → pr.receipt\_document.
    - Evaluate check\_receipt\_document\_access(pr.receipt\_document\_type, pr.receipt\_document).
    - Set pr\_items from get\_pr\_items(pr).
    - For each d in pr\_items.
      - Set item from self.append(“items”).
      - Set item.item\_code from d.item\_code.
      - Set item.description from d.description.
      - Set item.qty from d.qty.
      - Set item.rate from d.base\_rate.
      - Set item.cost\_center from (d.cost\_center or Enterprise.get\_default\_cost\_center(self.company)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.cost\_center → Enterprise.get\_default\_cost\_center(self.company).
      - Set item.amount from d.base\_amount.
      - Set item.receipt\_document\_type from pr.receipt\_document\_type.
      - Set item.receipt\_document from pr.receipt\_document.
      - Set item.is\_fixed\_asset from d.is\_fixed\_asset.
      - If pr.receipt\_document\_type equals “Stock Entry”.
        - Set item.stock\_entry\_item from d.name.
      - Otherwise.
        - Set item.purchase\_receipt\_item from d.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1242)

<a id="op-14c3dbb3364d13"></a>
### Landed Cost Voucher.validate

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_validate`

**Inputs** self.

**Local steps**

- Evaluate self.check\_mandatory().
- Evaluate self.validate\_receipt\_documents().
- Evaluate self.validate\_line\_items().
- Evaluate self.validate\_expense\_accounts().
- Evaluate init\_landed\_taxes\_and\_totals(self).
- Evaluate self.set\_total\_taxes\_and\_charges().
- If not self.get(“items”).
  - Evaluate self.get\_items\_from\_purchase\_receipts().
- Evaluate self.set\_applicable\_charges\_on\_item().
- Evaluate self.set\_total\_vendor\_invoices\_cost().
- Evaluate self.validate\_vendor\_invoice\_claims().
- Evaluate self.validate\_mandatory\_dimensions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check mandatory](operations-030.md#op-5c07ebc92d9e88), [validate receipt documents](operations-030.md#op-7a98268a49bb82), [validate line items](operations-030.md#op-f90c25bcce3cde), [validate expense accounts](operations-030.md#op-ad897653c85419), [set total taxes and charges](operations-030.md#op-56cf23aca3de4d), [get items from purchase receipts](operations-030.md#op-9e3364b33c6fa2), [set applicable charges on item](operations-030.md#op-d2692650944942), [set total vendor invoices cost](operations-030.md#op-01564bc7c16a1f), [validate vendor invoice claims](operations-031.md#op-b264bc3b102220), [validate mandatory dimensions](operations-030.md#op-a746b63c5443cf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1254)

<a id="op-01564bc7c16a1f"></a>
### Landed Cost Voucher.set total vendor invoices cost

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_set_total_vendor_invoices_cost`

**Inputs** self.

**Local steps**

- Set self.total\_vendor\_invoices\_cost from 0.0.
- For each row in self.vendor\_invoices.
  - Update self.total\_vendor\_invoices\_cost using + flt(row.amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0745.json#L852) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1250)

<a id="op-f90c25bcce3cde"></a>
### Landed Cost Voucher.validate line items

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_validate_line_items`

**Inputs** self.

**Record and data access** read (d.receipt\_document\_type + “ Item”) via exists.

**Explicit failure paths** validation helper — translated “Row {0}: {2} Item {1} does not exist in {2} {3}”.format(d.idx, Platform.bold(d.purchase\_receipt\_item), d.receipt\_document\_type, Platform.bold(d.receipt\_document)).

**Local steps**

- For each d in self.get(“items”).
  - If (d.docstatus equals 0 and d.purchase\_receipt\_item and not Platform.db.exists((d.receipt\_document\_type + “ Item”), mapping(“name” → d.purchase\_receipt\_item, “parent” → d.receipt\_document))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.docstatus equals 0 → d.purchase\_receipt\_item → not Platform.db.exists((d.receipt\_document\_type + “ Item”), mapping(“name” → d.purchase\_receipt\_item, “parent” → d.receipt\_document)).
    - Call the validation error handler Platform.throw(translated “Row {0}: {2} Item {1} does not exist in {2} {3}”.format(d.idx, Platform.bold(d.purchase\_receipt\_item), d.receipt\_document\_type, Platform.bold(d.receipt\_document)), title = transl ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0745.json#L951) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1258)

<a id="op-5c07ebc92d9e88"></a>
### Landed Cost Voucher.check mandatory

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_check_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please enter Receipt Document”.

**Local steps**

- If not self.get(“purchase\_receipts”).
  - Call the validation error handler Platform.throw(translated “Please enter Receipt Document”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0745.json#L1288) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1241)

<a id="op-7a98268a49bb82"></a>
### Landed Cost Voucher.validate receipt documents

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_validate_receipt_documents`

**Inputs** self.

**Record and data access** read d.receipt\_document\_type via get\_cached\_value · read d.receipt\_document\_type via get\_value.

**Explicit failure paths** validation helper — translated msg · validation helper with IncorrectCompanyValidationError — translated “Row {0}: {1} {2} is linked to company {3}. Please select a document belonging to company {4}.”.format(d.idx, d.receipt\_document\_type, Platform.bold(d.receipt\_document), Platform.bold(company), …) · validation helper — msg · validation helper — translated “Row {0}: Landed Cost Voucher can only be made against a Manufacture or Repack Stock Entry. Stock Entry {1} i …”.format(d.idx, Platform.bold(d.receipt\_document), translated purpose) · validation helper — translated “Item must be added using 'Get Items from Purchase Receipts' button” · 2 additional forms in the steps below.

**Local steps**

- Set receipt\_documents from list().
- For each d in self.get(“purchase\_receipts”).
  - Set tuple(docstatus, company) from Platform.get\_cached\_value(d.receipt\_document\_type, d.receipt\_document, list(“docstatus”, “company”)).
  - If docstatus differs from 1.
    - Set msg from formatted text Row {d.idx}: {d.receipt\_document\_type} {Platform.bold(d.receipt\_document)} must be submitted.
    - Call the validation error handler Platform.throw(translated msg, title = translated “Invalid Document”).
  - If company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Row {0}: {1} {2} is linked to company {3}. Please select a document belonging to company {4}.”.format(d.idx, d.receipt\_document\_type, Platform.bold(d.receipt\_document), Platform. ….
  - If d.receipt\_document\_type equals “Purchase Invoice”.
    - Set update\_stock from Platform.db.get\_value(d.receipt\_document\_type, d.receipt\_document, “update\_stock”).
    - If not update\_stock.
      - Set msg from translated “Row {0}: Purchase Invoice {1} has no stock impact.”.format(d.idx, Platform.bold(d.receipt\_document)).
      - Update msg using + (text in the contract + translated “Please create Landed Cost Vouchers against Invoices that have 'Update Stock' enabled.”).
      - Call the validation error handler Platform.throw(msg, title = translated “Incorrect Invoice”).
  - If d.receipt\_document\_type equals “Stock Entry”.
    - Set purpose from Platform.get\_cached\_value(d.receipt\_document\_type, d.receipt\_document, “purpose”).
    - If purpose does not belong to tuple(“Manufacture”, “Repack”).
      - Call the validation error handler Platform.throw(translated “Row {0}: Landed Cost Voucher can only be made against a Manufacture or Repack Stock Entry. Stock Entry {1} i …”.format(d.idx, Platform.bold(d.receipt\_document), translated purpos ….
  - Evaluate receipt\_documents.append(d.receipt\_document).
- For each item in self.get(“items”).
  - If not item.receipt\_document.
    - Call the validation error handler Platform.throw(translated “Item must be added using 'Get Items from Purchase Receipts' button”).
  - Otherwise.
    - If item.receipt\_document does not belong to receipt\_documents.
      - Call the validation error handler Platform.throw(translated “Item Row {0}: {1} {2} does not exist in above '{1}' table”.format(item.idx, item.receipt\_document\_type, item.receipt\_document)).
  - If not item.cost\_center.
    - Call the validation error handler Platform.throw(translated “Row {0}: Cost center is required for an item {1}”.format(item.idx, item.item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(d.receipt\_document\_type, d.receipt\_document, list(“docstatus”, “company”)), Platform.get\_cached\_value(d.receipt\_document\_type, d.receipt\_document, “purpose”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1260)

<a id="op-ad897653c85419"></a>
### Landed Cost Voucher.validate expense accounts

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_validate_expense_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with IncorrectCompanyValidationError — translated “Row {0}: Expense Account {1} is linked to company {2}. Please select an account belonging to company {3}.”.format(t.idx, Platform.bold(t.expense\_account), Platform.bold(company), Platform.bold( ….

**Local steps**

- Evaluate self.validate\_charge\_account\_types().
- If not is\_perpetual\_inventory\_enabled(self.company).
  - Return no value.
- For each t in self.taxes.
  - Set company from Platform.get\_cached\_value(“Account”, t.expense\_account, “company”).
  - If company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Row {0}: Expense Account {1} is linked to company {2}. Please select an account belonging to company {3}.”.format(t.idx, Platform.bold(t.expense\_account), Platform.bold(company), ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate charge account types](operations-030.md#op-345e0a9d1434cd).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, t.expense\_account, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1257)

<a id="op-345e0a9d1434cd"></a>
### Landed Cost Voucher.validate charge account types

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_landedcostvoucher_validate_charge_account_types`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Account {1} cannot be used for landed cost charges”.format(row.idx, Platform.bold(row.expense\_account)).

**Local steps**

- For each row in self.taxes.
  - If not row.expense\_account.
    - Continue with the next iteration or loop test.
  - Set tuple(account\_type, is\_group) from Platform.get\_cached\_value(“Account”, row.expense\_account, list(“account\_type”, “is\_group”)).
  - If (account\_type equals “Stock” or is\_group).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_type equals “Stock” → is\_group.
    - Call the validation error handler Platform.throw(translated “Row {0}: Account {1} cannot be used for landed cost charges”.format(row.idx, Platform.bold(row.expense\_account)), title = translated “Incorrect Account”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, row.expense\_account, list(“account\_type”, “is\_group”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L838) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L335)

<a id="op-a746b63c5443cf"></a>
### Landed Cost Voucher.validate mandatory dimensions

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_validate_mandatory_dimensions`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Accounting Dimension {1} is mandatory for account {2}. Set it on this Taxes and Charges row, or on  …”.format(tax.idx, Platform.bold(label), Platform.bold(tax.expense\_account), item.idx, …).

**Local steps**

- Bind dependencies get\_accounting\_dimensions, get\_checks\_for\_pl\_and\_bs\_accounts.
- Bind dependencies get\_dimension\_filter\_map.
- If not is\_perpetual\_inventory\_enabled(self.company).
  - Return no value.
- Set company\_checks from list of check for check drawn from get\_checks\_for\_pl\_and\_bs\_accounts() where (check.company equals self.company and (check.mandatory\_for\_pl or check.mandatory\_for\_bs)).
  - Draw check from get\_checks\_for\_pl\_and\_bs\_accounts(), keep a combination only if ((check.company equals self.company and (check.mandatory\_for\_pl or check.mandatory\_for\_bs))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in check.company equals self.company → (check.mandatory\_for\_pl or check.mandatory\_for\_bs).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in check.mandatory\_for\_pl → check.mandatory\_for\_bs.
- Set dimension\_filter\_map from get\_dimension\_filter\_map().
- If (not company\_checks and not dimension\_filter\_map).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not company\_checks → not dimension\_filter\_map.
  - Return no value.
- Set labels from mapping of d.fieldname → d.label for d drawn from get\_accounting\_dimensions(as\_list = false).
  - Draw d from get\_accounting\_dimensions(as\_list = false).
- Set receipts from mapping().
- For each tax in self.get(“taxes”).
  - If not tax.expense\_account.
    - Continue with the next iteration or loop test.
  - Set report\_type from Platform.get\_cached\_value(“Account”, tax.expense\_account, “report\_type”).
  - Set mandatory from mapping().
  - For each check in company\_checks.
    - Set is\_mandatory from check.mandatory\_for\_pl when report\_type equals “Profit and Loss”, otherwise check.mandatory\_for\_bs.
      - Value choice on report\_type equals “Profit and Loss” — true gives check.mandatory\_for\_pl, false gives check.mandatory\_for\_bs.
    - If is\_mandatory.
      - Set mandatory at check.fieldname from check.label.
  - For each tuple(tuple(fieldname, account), dimension\_filter) in dimension\_filter\_map.items().
    - If (account equals tax.expense\_account and dimension\_filter.get(“is\_mandatory”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in account equals tax.expense\_account → dimension\_filter.get(“is\_mandatory”).
      - Evaluate mandatory.setdefault(fieldname, (labels.get(fieldname) or Platform.unscrub(fieldname))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in labels.get(fieldname) → Platform.unscrub(fieldname).
  - For each tuple(fieldname, label) in mandatory.items().
    - If tax.get(fieldname).
      - Continue with the next iteration or loop test.
    - For each item in self.get(“items”).
      - If self.get\_receipt\_dimension(receipts, item, fieldname).
        - Continue with the next iteration or loop test.
      - Call the validation error handler Platform.throw(translated “Row {0}: Accounting Dimension {1} is mandatory for account {2}. Set it on this Taxes and Charges row, or on  …”.format(tax.idx, Platform.bold(label), Platform.bold(tax.expense\_ac ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get receipt dimension](operations-030.md#op-143efda2ea30c4).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, tax.expense\_account, “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0745.json#L2786) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1259)

<a id="op-143efda2ea30c4"></a>
### Landed Cost Voucher.get receipt dimension

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_get_receipt_dimension`

**Inputs** self, receipts, item, fieldname.

**Record and data access** resolve a document from expanded key via get\_doc.

**Explicit results** item.get(fieldname) · no value · row.get(fieldname) · receipt.get(fieldname).

**Local steps**

- If item.get(fieldname).
  - Return item.get(fieldname).
- Set key from tuple(item.receipt\_document\_type, item.receipt\_document).
- If key does not belong to receipts.
  - Set receipts at key from Platform.get\_doc(expanded key) when item.receipt\_document, otherwise no value.
    - Value choice on item.receipt\_document — true gives Platform.get\_doc(expanded key), false gives no value.
- Set receipt from receipts at key.
- If not receipt.
  - Return no value.
- Set row\_fieldname from “stock\_entry\_item” when receipt.doctype equals “Stock Entry”, otherwise “purchase\_receipt\_item”.
  - Value choice on receipt.doctype equals “Stock Entry” — true gives “stock\_entry\_item”, false gives “purchase\_receipt\_item”.
- Set receipt\_row\_name from item.get(row\_fieldname).
- For each row in (receipt.get(“items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in receipt.get(“items”) → list().
  - If (row.name equals receipt\_row\_name and row.get(fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.name equals receipt\_row\_name → row.get(fieldname).
    - Return row.get(fieldname).
- Return receipt.get(fieldname).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0745.json#L3801) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1243)

<a id="op-56cf23aca3de4d"></a>
### Landed Cost Voucher.set total taxes and charges

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_set_total_taxes_and_charges`

**Inputs** self.

**Local steps**

- Set self.total\_taxes\_and\_charges from sum(generator of flt(d.base\_amount) for d drawn from self.get(“taxes”)).
  - Draw d from self.get(“taxes”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0745.json#L4273) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L66) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1249)

<a id="op-d2692650944942"></a>
### Landed Cost Voucher.set applicable charges on item

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_set_applicable_charges_on_item`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Total {0} of all items is zero. Set 'Distribute Charges Based On' to {1}.”.format(self.distribute\_charges\_based\_on, translated “Qty” when based\_on\_field equals “amount”, otherwise translated “Amount”).

**Local steps**

- If (self.get(“taxes”) and self.distribute\_charges\_based\_on differs from “Distribute Manually”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“taxes”) → self.distribute\_charges\_based\_on differs from “Distribute Manually”.
  - Set items from self.get(“items”).
  - Set based\_on\_field from Platform.scrub(self.distribute\_charges\_based\_on).
  - Set total\_item\_cost from sum(generator of flt(item.get(based\_on\_field)) for item drawn from items).
    - Draw item from items.
  - If items.
    - Set total\_item\_cost from flt(total\_item\_cost, items at 0.precision(based\_on\_field)).
  - If not total\_item\_cost.
    - Call the validation error handler Platform.throw(translated “Total {0} of all items is zero. Set 'Distribute Charges Based On' to {1}.”.format(self.distribute\_charges\_based\_on, translated “Qty” when based\_on\_field equals “amount”, otherwis ….
      - Value choice on based\_on\_field equals “amount” — true gives translated “Qty”, false gives translated “Amount”.
  - Evaluate self.distribute\_charges(items, based\_on\_field, total\_item\_cost).

If control reaches the end, it returns no value.

**Methods declared on this owner** [distribute charges](operations-030.md#op-e36f3fac3fe647).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1248)

<a id="op-e36f3fac3fe647"></a>
### Landed Cost Voucher.distribute charges

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_landedcostvoucher_distribute_charges`

**Inputs** self, items, based\_on\_field, total\_item\_cost.

**Local steps**

- Set precision from items at 0.precision(“applicable\_charges”).
- Set charges\_per\_unit from (flt(self.total\_taxes\_and\_charges) ÷ flt(total\_item\_cost)).
- For each item in items.
  - Set item.applicable\_charges from flt((flt(item.get(based\_on\_field)) × charges\_per\_unit), precision).
- Set diff from (flt(self.total\_taxes\_and\_charges) − sum(generator of flt(item.applicable\_charges) for item drawn from items)).
  - Draw item from items.
- Evaluate absorb\_rounding\_difference(self.get\_rows\_following\_the\_basis\_total(), flt(diff, precision), precision, self.total\_taxes\_and\_charges).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rows following the basis total](operations-030.md#op-11ef74824190f2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L834) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L331)

<a id="op-a623bad1a612a0"></a>
### Landed Cost Voucher.validate applicable charges for item

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_validate_applicable_charges_for_item`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Total {0} for all items is zero, may be you should change 'Distribute Charges Based On'”.format(based\_on) · validation helper — translated “Total Applicable Charges in Purchase Receipt Items table must be same as Total Taxes and Charges”.

**Local steps**

- Set based\_on from self.distribute\_charges\_based\_on.lower().
- If based\_on differs from “distribute manually”.
  - Set total from sum(generator of flt(d.get(based\_on)) for d drawn from self.get(“items”)).
    - Draw d from self.get(“items”).
- Otherwise.
  - Set total from sum(generator of flt(d.get(“applicable\_charges”)) for d drawn from self.get(“items”)).
    - Draw d from self.get(“items”).
- If not total.
  - Call the validation error handler Platform.throw(translated “Total {0} for all items is zero, may be you should change 'Distribute Charges Based On'”.format(based\_on)).
- Set total\_applicable\_charges from sum(generator of flt(d.applicable\_charges) for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
- Set precision from get\_field\_precision(Platform.get\_meta(“Landed Cost Item”).get\_field(“applicable\_charges”), currency = Platform.get\_cached\_value(“Company”, self.company, “default\_currency”)).
- Set diff from (flt(self.total\_taxes\_and\_charges) − flt(total\_applicable\_charges)).
- Set diff from flt(diff, precision).
- If abs(diff) ≥ (2.0 ÷ (10 to the power precision)).
  - Call the validation error handler Platform.throw(translated “Total Applicable Charges in Purchase Receipt Items table must be same as Total Taxes and Charges”).
- Evaluate absorb\_rounding\_difference(self.get\_rows\_following\_the\_basis\_total(), diff, precision, self.total\_taxes\_and\_charges).
- Evaluate self.validate\_charges\_follow\_total\_sign().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rows following the basis total](operations-030.md#op-11ef74824190f2), [validate charges follow total sign](operations-030.md#op-aaaf2608b8e4f5).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1255)

<a id="op-2650901d5dbec9"></a>
### Landed Cost Voucher.get charge sign basis

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_landedcostvoucher_get_charge_sign_basis`

**Inputs** self.

**Explicit results** tuple(based\_on, basis\_sign).

**Local steps**

- Set based\_on from Platform.scrub(self.distribute\_charges\_based\_on).
- If based\_on equals “distribute\_manually”.
  - Set based\_on from “amount”.
- Set basis\_sign from negative 1 when sum(generator of flt(nested operand in the contract.get(based\_on)) for row drawn from self.get(“items”)) &lt; 0, otherwise 1.
  - Value choice on sum(generator of flt(row.get(based\_on)) for row drawn from self.get(“items”)) &lt; 0 — true gives negative 1, false gives 1.
  - Draw row from self.get(“items”).
- Return tuple(based\_on, basis\_sign).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L835) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L332)

<a id="op-11ef74824190f2"></a>
### Landed Cost Voucher.get rows following the basis total

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_landedcostvoucher_get_rows_following_the_basis_total`

**Inputs** self.

**Explicit results** list of row for row drawn from self.get(“items”) where (flt(row.get(based\_on)) × basis\_sign) ≥ 0.

**Local steps**

- Set tuple(based\_on, basis\_sign) from self.get\_charge\_sign\_basis().
- Return list of row for row drawn from self.get(“items”) where (flt(row.get(based\_on)) × basis\_sign) ≥ 0.
  - Draw row from self.get(“items”), keep a combination only if ((flt(row.get(based\_on)) × basis\_sign) ≥ 0).

**Methods declared on this owner** [get charge sign basis](operations-030.md#op-2650901d5dbec9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L836) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L333)

<a id="op-aaaf2608b8e4f5"></a>
### Landed Cost Voucher.validate charges follow total sign

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_landedcostvoucher_validate_charges_follow_total_sign`

**Inputs** self.

**Explicit failure paths** validation helper — message.format(row.idx, Platform.bold(row.item\_code)).

**Local steps**

- Set total\_sign from negative 1 when flt(self.total\_taxes\_and\_charges) &lt; 0, otherwise 1.
  - Value choice on flt(self.total\_taxes\_and\_charges) &lt; 0 — true gives negative 1, false gives 1.
- Set tuple(based\_on, basis\_sign) from self.get\_charge\_sign\_basis().
- For each row in self.get(“items”).
  - Set expected\_sign from (total\_sign × negative 1 when (flt(nested operand in the contract.get(based\_on)) × basis\_sign) &lt; 0, otherwise 1).
    - Value choice on (flt(row.get(based\_on)) × basis\_sign) &lt; 0 — true gives negative 1, false gives 1.
  - If (flt(row.applicable\_charges) × expected\_sign) ≥ 0.
    - Continue with the next iteration or loop test.
  - Set message from translated “Row {0}: Applicable Charges for Item {1} cannot be negative” when expected\_sign &gt; 0, otherwise translated “Row {0}: Applicable Charges for Item {1} cannot be positive”.
    - Value choice on expected\_sign &gt; 0 — true gives translated “Row {0}: Applicable Charges for Item {1} cannot be negative”, false gives translated “Row {0}: Applicable Charges for Item {1} cannot be positive”.
  - Call the validation error handler Platform.throw(message.format(row.idx, Platform.bold(row.item\_code))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get charge sign basis](operations-030.md#op-2650901d5dbec9).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L839) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L336)

<a id="op-3be584722f7748"></a>
### Landed Cost Voucher.get receipt document details

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_get_receipt_document_details`

**Inputs** self, receipt\_document\_type, receipt\_document.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read receipt\_document\_type via get\_value.

**Explicit results** Platform.db.get\_value(receipt\_document\_type, receipt\_document, fields, as\_dict = true).

**Local steps**

- Evaluate check\_receipt\_document\_access(receipt\_document\_type, receipt\_document).
- If receipt\_document\_type belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
  - Set fields from list(“supplier”, “posting\_date”).
  - If receipt\_document\_type equals “Subcontracting Receipt”.
    - Evaluate fields.append(“total as grand\_total”).
  - Otherwise.
    - Evaluate fields.append(“base\_grand\_total as grand\_total”).
- Otherwise.
  - If receipt\_document\_type equals “Stock Entry”.
    - Set fields from list(“total\_incoming\_value as grand\_total”).
- Return Platform.db.get\_value(receipt\_document\_type, receipt\_document, fields, as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1244)

<a id="op-36a78d8e678cdb"></a>
### Landed Cost Voucher.on submit

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_applicable\_charges\_for\_item().
- Evaluate self.update\_landed\_cost().
- Evaluate self.update\_claimed\_landed\_cost().
- Evaluate self.update\_project\_purchase\_cost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate applicable charges for item](operations-030.md#op-a623bad1a612a0), [update landed cost](operations-031.md#op-cab7870fd2aa3a), [update claimed landed cost](operations-031.md#op-7235b448bd413a), [update project purchase cost](operations-031.md#op-b79f850821f030).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1247)

<a id="op-2a1386ba704743"></a>
### Landed Cost Voucher.on cancel

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_landed\_cost().
- Evaluate self.update\_claimed\_landed\_cost().
- Evaluate self.update\_project\_purchase\_cost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update landed cost](operations-031.md#op-cab7870fd2aa3a), [update claimed landed cost](operations-031.md#op-7235b448bd413a), [update project purchase cost](operations-031.md#op-b79f850821f030).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1246)
