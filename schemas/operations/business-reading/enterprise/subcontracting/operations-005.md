# Subcontracting · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subcontracting receipt

[Record definition](../../../../data/record-types/subcontracting_receipt.json)

<a id="op-ae33c3647dad00"></a>
### Subcontracting Receipt.validate

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Posting Date cannot be future date”.

**Local steps**

- Evaluate self.reset\_supplied\_items().
- Evaluate self.validate\_posting\_time().
- If not self.get(“is\_return”).
  - Evaluate self.validate\_inspection().
  - Evaluate self.validate\_purchase\_orders\_share\_terms().
- If getdate(self.posting\_date) &gt; getdate(nowdate()).
  - Call the validation error handler Platform.throw(translated “Posting Date cannot be future date”).
- Evaluate super().validate().
- Evaluate self.validate\_item\_stock\_uom\_is\_integer(“item\_code”, list(“qty”, “received\_qty”, “rejected\_qty”), “Subcontracting Receipt Item”, row\_filter = deferred anonymous expression).
- Evaluate self.set\_missing\_values().
- If (self.is\_new() and self.get(“\_action”) equals “save” and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.get(“\_action”) equals “save” → not Platform.in\_test.
  - Evaluate self.get\_secondary\_items(recalculate\_rate = true).
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate validate\_return(self).
- Evaluate self.validate\_return\_supplier\_warehouse().
- If self.get(“\_action”) equals “submit”.
  - Evaluate self.validate\_returned\_raw\_materials().
  - Evaluate self.validate\_secondary\_items().
  - Evaluate self.validate\_accepted\_warehouse().
  - Evaluate self.validate\_rejected\_warehouse().
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).
- Evaluate self.reset\_default\_field\_value(“rejected\_warehouse”, “items”, “rejected\_warehouse”).
- Evaluate self.get\_current\_stock().
- Evaluate self.set\_supplied\_items\_expense\_account().
- Evaluate self.set\_supplied\_items\_cost\_center().
- Evaluate self.set\_supplied\_items\_inventory\_dimensions().
- Evaluate self.validate\_inventory\_dimension\_mandatory().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset supplied items](operations-005.md#op-fae65fba73b219), [validate purchase orders share terms](operations-005.md#op-12ee592f58c7b1), [set missing values](operations-006.md#op-faf0205223b1fd), [get secondary items](operations-005.md#op-1d946bda796dc2), [validate with previous doc](operations-005.md#op-1edc57fe519e16), [validate return supplier warehouse](operations-005.md#op-7249c5df3ca7e6), [validate secondary items](operations-006.md#op-3734715e59eb98), [validate accepted warehouse](operations-006.md#op-fbb0fd0afaa45e), [set supplied items expense account](operations-005.md#op-8fef5bec027e6d), [set supplied items cost center](operations-005.md#op-5ccf1a4758c1cd), [set supplied items inventory dimensions](operations-005.md#op-01ecdf8fcf8cc0).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1568) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1058)

<a id="op-12ee592f58c7b1"></a>
### Subcontracting Receipt.validate purchase orders share terms

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_validate_purchase_orders_share_terms`

**Inputs** self.

**Explicit failure paths** validation helper — get\_uncombinable\_orders\_message(purchase\_orders).

**Local steps**

- If not can\_combine\_purchase\_orders(purchase\_orders bound to get\_purchase\_orders(self)).
  - Call the validation error handler Platform.throw(get\_uncombinable\_orders\_message(purchase\_orders), title = translated “Cannot Combine Orders”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1229)

<a id="op-7249c5df3ca7e6"></a>
### Subcontracting Receipt.validate return supplier warehouse

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_validate_return_supplier_warehouse`

**Inputs** self.

**Record and data access** read “Subcontracting Receipt” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} must be {1}, the same as in {2}”.format(translated self.meta.get\_label(“supplier\_warehouse”), Platform.bold(original), Platform.bold(self.return\_against)).

**Local steps**

- If not (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Return no value.
- Set original from Platform.db.get\_value(“Subcontracting Receipt”, self.return\_against, “supplier\_warehouse”).
- If self.supplier\_warehouse differs from original.
  - Call the validation error handler Platform.throw(translated “{0} must be {1}, the same as in {2}”.format(translated self.meta.get\_label(“supplier\_warehouse”), Platform.bold(original), Platform.bold(self.return\_against)), title = translated ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1230)

<a id="op-1edc57fe519e16"></a>
### Subcontracting Receipt.validate with previous doc

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_validate_with_previous_doc`

**Inputs** self.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Subcontracting Order Item” → mapping(“ref\_dn\_field” → “subcontracting\_order\_item”, “compare\_fields” → list(list(“project”, “=”)), “is\_child\_table” → true, “allow ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1231)

<a id="op-5ec4fb841c4f7f"></a>
### Subcontracting Receipt.on submit

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_closed\_subcontracting\_order().
- Evaluate self.validate\_bom\_required\_qty().
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.set\_subcontracting\_order\_status(update\_bin = false).
- Evaluate self.set\_consumed\_qty\_in\_subcontract\_order().
- Evaluate self.make\_bundle\_for\_sales\_purchase\_return().
- For each table\_name in list(“items”, “supplied\_items”).
  - Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields(table\_name).
- Evaluate self.validate\_returned\_serial\_batches().
- Evaluate self.update\_stock\_reservation\_entries().
- Evaluate self.update\_stock\_ledger().
- Evaluate self.validate\_consumed\_batches().
- Evaluate self.make\_gl\_entries().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.update\_status().
- Evaluate self.auto\_create\_purchase\_receipt().
- Evaluate self.update\_job\_card().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate closed subcontracting order](operations-005.md#op-6a914474124076), [validate bom required qty](operations-006.md#op-a0df6aa25c0286), [update status updater args](operations-007.md#op-09996a35284aef), [validate consumed batches](operations-005.md#op-853936a779f959), [update status](operations-007.md#op-3dafd9dce08074), [auto create purchase receipt](operations-007.md#op-4c25a788a31724), [update job card](operations-005.md#op-f891e5014b6d47).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1039)

<a id="op-853936a779f959"></a>
### Subcontracting Receipt.validate consumed batches

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_validate_consumed_batches`

**Inputs** self.

**Record and data access** read “Subcontracting Receipt Supplied Item” via get\_all.

**Local steps**

- Set bundles from Platform.\_dict(Platform.get\_all(“Subcontracting Receipt Supplied Item”, filters = mapping(“parent” → self.name), fields = list(“name”, “serial\_and\_batch\_bundle”), as\_list = true)).
- For each row in self.supplied\_items.
  - Set row.serial\_and\_batch\_bundle from (bundles.get(row.name) or row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundles.get(row.name) → row.serial\_and\_batch\_bundle.
- Evaluate self.validate\_outward\_bundle\_batches(check\_expiry = false, rows = self.supplied\_items, qty\_field = “consumed\_qty”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1228)

<a id="op-29ab605528bdc9"></a>
### Subcontracting Receipt.on update

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_on_update`

**Inputs** self.

**Local steps**

- For each table\_field in list(“items”, “supplied\_items”).
  - If self.get(table\_field).
    - Evaluate self.set\_serial\_and\_batch\_bundle(table\_field).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L351) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1040)

<a id="op-644cf39b3ecab5"></a>
### Subcontracting Receipt.on cancel

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Serial and Batch Bundle”, …).
- Evaluate self.validate\_closed\_subcontracting\_order().
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.set\_consumed\_qty\_in\_subcontract\_order().
- Evaluate self.set\_subcontracting\_order\_status(update\_bin = false).
- Evaluate self.update\_stock\_ledger().
- Evaluate self.update\_stock\_reservation\_entries().
- Evaluate self.make\_gl\_entries\_on\_cancel().
- Evaluate self.repost\_future\_sle\_and\_gle().
- Evaluate self.update\_status().
- Evaluate self.delete\_auto\_created\_batches().
- Evaluate self.update\_job\_card().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate closed subcontracting order](operations-005.md#op-6a914474124076), [update status updater args](operations-007.md#op-09996a35284aef), [update status](operations-007.md#op-3dafd9dce08074), [update job card](operations-005.md#op-f891e5014b6d47).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1038)

<a id="op-04ce9e2b44b8ac"></a>
### Subcontracting Receipt.reset raw materials

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_reset_raw_materials`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set self.supplied\_items from list().
- Set self.flags.reset\_raw\_materials from true.
- Evaluate self.create\_raw\_materials\_supplied\_or\_received().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L785) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1043)

<a id="op-6a914474124076"></a>
### Subcontracting Receipt.validate closed subcontracting order

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_validate_closed_subcontracting_order`

**Inputs** self.

**Local steps**

- Evaluate self.check\_for\_on\_hold\_or\_closed\_status(“Subcontracting Order”, “subcontracting\_order”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L891) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1571) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1061)

<a id="op-f891e5014b6d47"></a>
### Subcontracting Receipt.update job card

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_update_job_card`

**Inputs** self.

**Record and data access** resolve a document from “Job Card” via get\_doc.

**Local steps**

- For each row in self.get(“items”).
  - If row.job\_card.
    - Set doc from Platform.get\_doc(“Job Card”, row.job\_card).
    - Evaluate doc.set\_manufactured\_qty().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L959) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1565) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1055)

<a id="op-f2773eba9e404d"></a>
### Subcontracting Receipt.set service expense account

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_service_expense_account`

**Inputs** self, default\_expense\_account.

**Record and data access** read “Purchase Order Item” via get\_value.

**Local steps**

- For each row in self.get(“items”).
  - If (not row.service\_expense\_account and row.purchase\_order\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.service\_expense\_account → row.purchase\_order\_item.
    - Set service\_item from Platform.db.get\_value(“Purchase Order Item”, row.purchase\_order\_item, “item\_code”).
    - If service\_item.
      - If default bound to (get\_item\_defaults(service\_item, self.company) or get\_item\_group\_defaults(service\_item, self.company) or get\_brand\_defaults(service\_item, self.company)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_defaults(service\_item, self.company) → get\_item\_group\_defaults(service\_item, self.company) → get\_brand\_defaults(service\_item, self.company).
        - If service\_expense\_account bound to default.get(“expense\_account”).
          - Set row.service\_expense\_account from service\_expense\_account.
  - If not row.service\_expense\_account.
    - Set row.service\_expense\_account from default\_expense\_account.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L1100) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1051)

<a id="op-a9438da97065b0"></a>
### Subcontracting Receipt.set expense account for subcontracted items

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_expense_account_for_subcontracted_items`

**Inputs** self, default\_expense\_account.

**Local steps**

- For each row in self.get(“items”).
  - If not row.expense\_account.
    - If default bound to (get\_item\_defaults(row.item\_code, self.company) or get\_item\_group\_defaults(row.item\_code, self.company) or get\_brand\_defaults(row.item\_code, self.company)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_defaults(row.item\_code, self.company) → get\_item\_group\_defaults(row.item\_code, self.company) → get\_brand\_defaults(row.item\_code, self.company).
      - If expense\_account bound to default.get(“expense\_account”).
        - Set row.expense\_account from expense\_account.
  - If not row.expense\_account.
    - Set row.expense\_account from default\_expense\_account.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L1459) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1047)

<a id="op-7e41cac851741f"></a>
### Subcontracting Receipt.get manufactured qty

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_get_manufactured_quantity`

**Inputs** self, job\_card.

**Explicit results** flt(qty).

**Local steps**

- Set table from Platform.qb.DocType(“Subcontracting Receipt Item”).
- Set query from nested operand in the contract.qb.from\_(table).select(Sum(table.qty)).where((table.job\_card equals job\_card bitwise and table.docstatus equals 1)).
- Set qty from (query.run() at 0 at 0 or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.0.
- Return flt(qty).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L1751) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1030)

<a id="op-f392a37410b6a1"></a>
### Subcontracting Receipt.validate items qty

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_validate_items_quantity`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Accepted Qty and Rejected Qty can't be zero at the same time.”.format(item.idx).

**Local steps**

- For each item in self.items.
  - If (item.secondary\_item\_type or item.valuation\_type).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → item.valuation\_type.
    - Continue with the next iteration or loop test.
  - If not (item.qty or item.rejected\_qty).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.qty → item.rejected\_qty.
    - Call the validation error handler Platform.throw(translated “Row {0}: Accepted Qty and Rejected Qty can't be zero at the same time.”.format(item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1572) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1062)

<a id="op-dacae14289847f"></a>
### Subcontracting Receipt.set items bom

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_items_bill_of_materials`

**Inputs** self.

**Record and data access** read “Subcontracting Receipt Item” via get\_value · read “Subcontracting Order Item” via get\_value.

**Local steps**

- If self.is\_return.
  - For each item in self.items.
    - If not item.bom.
      - Set item.bom from Platform.db.get\_value(“Subcontracting Receipt Item”, mapping(“name” → item.subcontracting\_receipt\_item, “parent” → self.return\_against), “bom”).
- Otherwise.
  - For each item in self.items.
    - If not item.bom.
      - Set item.bom from Platform.db.get\_value(“Subcontracting Order Item”, mapping(“name” → item.subcontracting\_order\_item, “parent” → item.subcontracting\_order), “bom”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L2171) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1048)

<a id="op-0ca441c49b9e1d"></a>
### Subcontracting Receipt.set items received qty

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_set_items_received_qty`

**Inputs** self.

**Local steps**

- For each item in self.items.
  - If item.bom.
    - Set item.received\_qty from self.get\_qty\_for\_costing(item).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1226)

<a id="op-5c8321c36d2162"></a>
### Subcontracting Receipt.set items cost center

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_items_cost_center`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If self.company.
  - Set cost\_center from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).
  - For each item in self.items.
    - If not item.cost\_center.
      - Set item.cost\_center from cost\_center.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L2482) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1049)

<a id="op-5ccf1a4758c1cd"></a>
### Subcontracting Receipt.set supplied items cost center

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_supplied_items_cost_center`

**Inputs** self.

**Local steps**

- For each item in self.supplied\_items.
  - If not item.cost\_center.
    - Set item.cost\_center from get\_default\_cost\_center(mapping(“project” → self.project), get\_item\_defaults(item.rm\_item\_code, self.company), get\_item\_group\_defaults(item.rm\_item\_code, self.company), get\_brand\_defaults(item.rm\_item\_code ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L2632) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1052)

<a id="op-01ecdf8fcf8cc0"></a>
### Subcontracting Receipt.set supplied items inventory dimensions

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_supplied_items_inventory_dimensions`

**Inputs** self.

**Local steps**

- If (hasattr(self, “inventory\_dimensions”) and inventory\_dimensions bound to get\_inventory\_dimensions()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “inventory\_dimensions”) → inventory\_dimensions bound to get\_inventory\_dimensions().
  - For each item in self.supplied\_items.
    - Set key from tuple(item.reference\_name, item.rm\_item\_code, item.main\_item\_code, item.batch\_no, …).
    - For each dimension in inventory\_dimensions.
      - Set dimension\_values from self.inventory\_dimensions.get(dimension.source\_fieldname, mapping()).
      - If key belongs to dimension\_values.
        - Evaluate item.set(dimension.source\_fieldname, dimension\_values at key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L2856) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1054)

<a id="op-8fef5bec027e6d"></a>
### Subcontracting Receipt.set supplied items expense account

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_supplied_items_expense_account`

**Inputs** self.

**Local steps**

- For each item in self.supplied\_items.
  - If not item.expense\_account.
    - Set item.expense\_account from get\_default\_expense\_account(Platform.\_dict(mapping(“expense\_account” → self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true))), get\_item\_defaults(item.rm\_item\_code, self.company), g ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L3131) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1053)

<a id="op-95e4982fb2000f"></a>
### Subcontracting Receipt.save inventory dimensions

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_save_inventory_dimensions`

**Inputs** self.

**Local steps**

- If inventory\_dimensions bound to get\_inventory\_dimensions().
  - If not getattr(self, “inventory\_dimensions”, no value).
    - Set self.inventory\_dimensions from mapping().
  - For each dimension in inventory\_dimensions.
    - Set self.inventory\_dimensions at dimension.source\_fieldname from mapping of tuple(d.reference\_name, d.rm\_item\_code, d.main\_item\_code, d.batch\_no, …) → d.get(dimension.source\_fieldname) for d drawn from self.supplied\_items.
      - Draw d from self.supplied\_items.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “inventory\_dimensions”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L3391) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1045)

<a id="op-fae65fba73b219"></a>
### Subcontracting Receipt.reset supplied items

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_reset_supplied_items`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- If (Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”) equals “BOM” and self.supplied\_items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”) equals “BOM” → self.supplied\_items.
  - If not any(generator of (item.serial\_and\_batch\_bundle or item.batch\_no or item.serial\_no) for item drawn from self.supplied\_items).
    - Draw item from self.supplied\_items.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.serial\_and\_batch\_bundle → item.batch\_no → item.serial\_no.
    - Set self.supplied\_items from list().
  - Otherwise.
    - Evaluate self.update\_rate\_for\_supplied\_items().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L3631) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1044)

<a id="op-1d946bda796dc2"></a>
### Subcontracting Receipt.get secondary items

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_get_secondary_items`

**Inputs** self, recalculate\_rate = false.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.remove\_secondary\_items().
- Set original\_rows from self.get\_returned\_receipt\_rows().
- Set rejected\_return\_rows from self.get\_rejected\_return\_rows().
- For each item in list(self.items).
  - If (item.bom and item.name does not belong to rejected\_return\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.bom → item.name does not belong to rejected\_return\_rows.
    - Set returned\_qty from original\_rows.get(item.subcontracting\_receipt\_item, mapping()).get(“returned\_qty”).
    - Evaluate self.add\_secondary\_items\_of\_fg\_row(item, negative flt(returned\_qty)).
- Evaluate self.link\_returned\_secondary\_items(original\_rows).
- Evaluate self.set\_remaining\_secondary\_qty(original\_rows).
- If recalculate\_rate.
  - Evaluate self.set\_additional\_costs().
  - Evaluate self.calculate\_items\_qty\_and\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove secondary items](operations-006.md#op-92dee3b2ff5c62), [get returned receipt rows](operations-006.md#op-de0bd256ce04ce), [add secondary items of fg row](operations-006.md#op-d14ba1833ac8ef), [link returned secondary items](operations-006.md#op-c5b3c1d00e4f91), [set remaining secondary qty](operations-006.md#op-5ad957f50a50d5), [set additional costs](operations-006.md#op-c754a992ae004a), [calculate items qty and amount](operations-006.md#op-7b426cf1521780).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1035)
