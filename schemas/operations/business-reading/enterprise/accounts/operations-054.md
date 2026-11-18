# Accounting and settlement · operations 54

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Invoice discounting

[Record definition](../../../../data/record-types/invoice_discounting.json)

<a id="op-bea3daaa000f7e"></a>
### Get data

`operation_enterprise_accounts_record_definitions_invoice_discounting_invoice_discounting_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “reference\_name”, “internal\_links” → mapping(“Sales Invoice” → list(“invoices”, “sales\_invoice”)), “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“Sale ….

**Local steps**

- Return mapping(“fieldname” → “reference\_name”, “internal\_links” → mapping(“Sales Invoice” → list(“invoices”, “sales\_invoice”)), “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“Sale ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0060.json#L4287) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1088)

## Record · Item tax template

[Record definition](../../../../data/record-types/item_tax_template.json)

<a id="op-ae9f08aa17772c"></a>
### Item Tax Template.validate

`operation_enterprise_accounts_record_definitions_item_tax_template_business_behavior_item_tax_template_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_zero\_rate\_for\_not\_applicable\_tax().
- Evaluate self.validate\_tax\_accounts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set zero rate for not applicable tax](operations-054.md#op-34cc4f2a364238), [validate tax accounts](operations-054.md#op-eb70f8d0106dcb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0061.json#L4074) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1102)

<a id="op-34cc4f2a364238"></a>
### Item Tax Template.set zero rate for not applicable tax

`operation_enterprise_accounts_record_definitions_item_tax_template_business_behavior_item_tax_template_set_zero_rate_for_not_applicable_tax`

**Inputs** self.

**Local steps**

- For each row in self.get(“taxes”).
  - If row.not\_applicable.
    - Set row.tax\_rate from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0061.json#L4145) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1101)

<a id="op-888d65a8b0f642"></a>
### Item Tax Template.autoname

`operation_enterprise_accounts_record_definitions_item_tax_template_business_behavior_item_tax_template_autoname`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If (self.company and self.title).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → self.title.
  - Set abbr from Platform.get\_cached\_value(“Company”, self.company, “abbr”).
  - Set self.name from formatted text {self.title} - {abbr}.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “abbr”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0061.json#L4243) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1100)

<a id="op-eb70f8d0106dcb"></a>
### Item Tax Template.validate tax accounts

`operation_enterprise_accounts_record_definitions_item_tax_template_business_behavior_item_tax_template_validate_tax_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Item Tax Row {0}: Account must belong to Company - {1}”.format(d.idx, Platform.bold(self.company)) · validation helper — translated “Item Tax Row {0}: Account {1} is a group account”.format(d.idx, Platform.bold(d.tax\_type)) · validation helper — translated “Item Tax Row {0} must have account of type Tax or Income or Expense or Chargeable”.format(d.idx) · validation helper — translated “{0} entered twice in Item Tax”.format(d.tax\_type).

**Local steps**

- Set check\_list from list().
- For each d in self.get(“taxes”).
  - If d.tax\_type.
    - Set tuple(account\_type, account\_company, is\_group) from Platform.get\_cached\_value(“Account”, d.tax\_type, list(“account\_type”, “company”, “is\_group”)).
    - If account\_company differs from self.company.
      - Call the validation error handler Platform.throw(translated “Item Tax Row {0}: Account must belong to Company - {1}”.format(d.idx, Platform.bold(self.company))).
    - If is\_group.
      - Call the validation error handler Platform.throw(translated “Item Tax Row {0}: Account {1} is a group account”.format(d.idx, Platform.bold(d.tax\_type))).
    - If account\_type does not belong to list(“Tax”, “Chargeable”, “Income Account”, “Expense Account”, …).
      - Call the validation error handler Platform.throw(translated “Item Tax Row {0} must have account of type Tax or Income or Expense or Chargeable”.format(d.idx)).
    - Otherwise.
      - If d.tax\_type belongs to check\_list.
        - Call the validation error handler Platform.throw(translated “{0} entered twice in Item Tax”.format(d.tax\_type)).
      - Otherwise.
        - Evaluate check\_list.append(d.tax\_type).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.tax\_type, list(“account\_type”, “company”, “is\_group”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1103)

<a id="op-d1f9f78c634bfd"></a>
### Get data

`operation_enterprise_accounts_record_definitions_item_tax_template_item_tax_template_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “item\_tax\_template”, “transactions” → list(mapping(“label” → translated “Pre Sales”, “items” → list(“Quotation”, “Supplier Quotation”)), mapping(“label” → translated “Sales”, “items”  ….

**Local steps**

- Return mapping(“fieldname” → “item\_tax\_template”, “transactions” → list(mapping(“label” → translated “Pre Sales”, “items” → list(“Quotation”, “Supplier Quotation”)), mapping(“label” → translated “Sales”, “items”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0061.json#L4897) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1157) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1104)

## Report · Item wise purchase register

<a id="op-f32881998682a2"></a>
### Execute

`operation_enterprise_accounts_report_item_wise_purchase_register_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** \_execute(filters).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return \_execute(filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1096)

<a id="op-31d7d9b23a8175"></a>
### Execute

`operation_enterprise_accounts_report_item_wise_purchase_register_business_behavior_execute_2`

**Inputs** filters = no value, additional\_table\_columns = no value.

**Explicit results** tuple(columns, list(), no value, no value, …) · tuple(columns, get\_grouped\_data(filters, rows, tax\_columns), no value, no value, …) · tuple(columns, list of row for tuple(\_item, row) drawn from rows, no value, no value, …).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns(additional\_table\_columns, filters).
- Set company\_currency from Enterprise.get\_company\_currency(filters.company).
- Set item\_list from get\_items(filters, additional\_table\_columns).
- If not item\_list.
  - Return tuple(columns, list(), no value, no value, …).
- Set aii\_account\_map from get\_aii\_accounts().
- Set default\_taxes from mapping().
- Set tuple(itemised\_tax, tax\_columns) from get\_tax\_accounts(item\_list, columns, company\_currency, doctype = “Purchase Invoice”, tax\_doctype = “Purchase Taxes and Charges”).
- For each tax in tax\_columns.
  - Set default\_taxes at formatted text {tax}\_rate from 0.
  - Set default\_taxes at formatted text {tax}\_amount from 0.
- Set po\_pr\_map from get\_purchase\_receipts\_against\_purchase\_order(item\_list).
- Set rows from list().
- For each d in item\_list.
  - Set purchase\_receipt from no value.
  - If d.purchase\_receipt.
    - Set purchase\_receipt from d.purchase\_receipt.
  - Otherwise.
    - If d.po\_detail.
      - Set purchase\_receipt from “, ”.join(po\_pr\_map.get(d.po\_detail, list())).
  - Set expense\_account from (d.unrealized\_profit\_loss\_account or d.expense\_account or aii\_account\_map.get(d.company)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.unrealized\_profit\_loss\_account → d.expense\_account → aii\_account\_map.get(d.company).
  - Set row from mapping(“item\_code” → d.item\_code, “item\_name” → d.pi\_item\_name when d.pi\_item\_name, otherwise d.i\_item\_name, “item\_group” → d.pi\_item\_group when d.pi\_item\_group, otherwise d.i\_item\_group, “description” →  ….
    - Value choice on d.pi\_item\_name — true gives d.pi\_item\_name, false gives d.i\_item\_name.
    - Value choice on d.pi\_item\_group — true gives d.pi\_item\_group, false gives d.i\_item\_group.
    - Value choice on d.stock\_qty — true gives (d.base\_net\_amount ÷ d.stock\_qty), false gives d.base\_net\_amount.
  - Set total\_tax from 0.
  - Set total\_other\_charges from 0.
  - Evaluate row.update(default\_taxes.copy()).
  - For each tuple(tax, details) in itemised\_tax.get(d.name, mapping()).items().
    - Evaluate row.update(mapping(formatted text {tax}\_rate → details.get(“tax\_rate”, 0), formatted text {tax}\_amount → details.get(“tax\_amount”, 0))).
    - If details.get(“is\_other\_charges”).
      - Update total\_other\_charges using + flt(details.get(“tax\_amount”)).
    - Otherwise.
      - Update total\_tax using + flt(details.get(“tax\_amount”)).
  - Evaluate row.update(mapping(“total\_tax” → total\_tax, “total\_other\_charges” → total\_other\_charges, “total” → ((d.base\_net\_amount + total\_tax) + total\_other\_charges), “currency” → company\_currency)).
  - Evaluate rows.append(tuple(d, row)).
- If filters.get(“group\_by”).
  - Return tuple(columns, get\_grouped\_data(filters, rows, tax\_columns), no value, no value, …).
- Return tuple(columns, list of row for tuple(\_item, row) drawn from rows, no value, no value, …).
  - Draw tuple(\_item, row) from rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1097)

<a id="op-697c44cc496ce9"></a>
### Get columns

`operation_enterprise_accounts_report_item_wise_purchase_register_business_behavior_get_columns`

**Inputs** additional\_table\_columns, filters.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- If filters.get(“group\_by”) differs from “Item”.
  - Evaluate columns.extend(list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “ ….
- If filters.get(“group\_by”) does not belong to tuple(“Item”, “Item Group”).
  - Evaluate columns.extend(list(mapping(“label” → translated “Item Group”, “fieldname” → “item\_group”, “fieldtype” → “Link”, “options” → “Item Group”, …))).
- Evaluate columns.extend(list(mapping(“label” → translated “Description”, “fieldname” → “description”, “fieldtype” → “Data”, “width” → 150), mapping(“label” → translated “Invoice”, “fieldname” → “invoice”, “fieldtyp ….
- If filters.get(“group\_by”) differs from “Supplier”.
  - Evaluate columns.extend(list(mapping(“label” → translated “Supplier”, “fieldname” → “supplier”, “fieldtype” → “Link”, “options” → “Supplier”, …), mapping(“label” → translated “Supplier Name”, “fieldname” → “supplie ….
- If additional\_table\_columns.
  - Update columns using + additional\_table\_columns.
- Update columns using + list(mapping(“label” → translated “Payable Account”, “fieldname” → “credit\_to”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“label” → translated “Mode Of Payment”, “fieldname” → “mode\_of\_payme ….
- If filters.get(“group\_by”).
  - Evaluate columns.append(mapping(“label” → translated “% Of Grand Total”, “fieldname” → “percent\_gt”, “fieldtype” → “Float”, “width” → 80)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0263.json#L4524) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1099)

<a id="op-05e1578a79e675"></a>
### Apply conditions

`operation_enterprise_accounts_report_item_wise_purchase_register_business_behavior_apply_conditions`

**Inputs** query, pi, pii, filters.

**Explicit results** query.

**Local steps**

- For each opts in tuple(“company”, “supplier”, “mode\_of\_payment”).
  - If filters.get(opts).
    - Set query from query.where(pi at opts equals filters at opts).
- If filters.get(“from\_date”).
  - Set query from query.where(pi.posting\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Set query from query.where(pi.posting\_date ≤ filters.get(“to\_date”)).
- If filters.get(“item\_code”).
  - Set query from query.where(pii.item\_code equals filters.get(“item\_code”)).
- If filters.get(“item\_group”).
  - Set item\_groups from list(filters.get(“item\_group”), expanded get\_descendants\_of(“Item Group”, filters.get(“item\_group”))).
  - Set query from query.where(pii.item\_group.isin(item\_groups)).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1095)

<a id="op-210c1bf9056a6e"></a>
### Get items

`operation_enterprise_accounts_report_item_wise_purchase_register_business_behavior_get_items`

**Inputs** filters, additional\_table\_columns.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from “Purchase Invoice”.
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set pii from Platform.qb.DocType(“Purchase Invoice Item”).
- Set Item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(pii.name, pii.parent, pi.posting\_date, pi.credit\_to, …).where(pi.docstatus equals 1).where(pii.parenttype equals doctype).
- If filters.get(“supplier”).
  - Set query from query.where(pi.supplier equals filters at “supplier”).
- If filters.get(“company”).
  - Set query from query.where(pi.company equals filters at “company”).
- If additional\_table\_columns.
  - For each column in additional\_table\_columns.
    - If column.get(“\_doctype”).
      - Set table from Platform.qb.DocType(column.get(“\_doctype”)).
      - Set query from query.select(table at column.get(“fieldname”)).
    - Otherwise.
      - Set query from query.select(pi at column.get(“fieldname”)).
- Set query from apply\_conditions(query, pi, pii, filters).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(doctype).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set query from apply\_order\_by\_conditions(doctype, query, filters).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0264.json#L565) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1100)

<a id="op-3468ad937014e1"></a>
### Get aii accounts

`operation_enterprise_accounts_report_item_wise_purchase_register_business_behavior_get_aii_accounts`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Company).

**Explicit results** dict(Platform.db.sql(query text (SELECT, Company))).

**Local steps**

- Return dict(Platform.db.sql(query text (SELECT, Company))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1098)

<a id="op-7c8038c44d0e99"></a>
### Get purchase receipts against purchase order

`operation_enterprise_accounts_report_item_wise_purchase_register_business_behavior_get_purchase_receipts_against_purchase_order`

**Inputs** item\_list.

**State and service calls** execute a supplied database query.

**Explicit results** po\_pr\_map.

**Local steps**

- Set po\_pr\_map from Platform.\_dict().
- Set po\_item\_rows from list(set(generator of d.po\_detail for d drawn from item\_list)).
  - Draw d from item\_list.
- If po\_item\_rows.
  - Set purchase\_receipts from Platform.db.sql((query text (SELECT, Purchase Receipt Item) modulo or format “, ”.join((list(“%s”) × len(po\_item\_rows)))), tuple(po\_item\_rows), as\_dict = 1).
  - For each pr in purchase\_receipts.
    - Evaluate po\_pr\_map.setdefault(pr.purchase\_order\_item, list()).append(pr.parent).
- Return po\_pr\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1101)

## Report · Item wise sales register

<a id="op-cb8c82bf396727"></a>
### Execute

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** \_execute(filters).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return \_execute(filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1109)

<a id="op-9005dd0ed909d9"></a>
### Execute

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_execute_2`

**Inputs** filters = no value, additional\_table\_columns = no value, additional\_conditions = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(columns, list(), no value, no value, …) · tuple(columns, get\_grouped\_data(filters, rows, tax\_columns), no value, no value, …) · tuple(columns, list of row for tuple(\_item, row) drawn from rows, no value, no value, …).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns(additional\_table\_columns, filters).
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
- Set item\_list from get\_items(filters, additional\_table\_columns, additional\_conditions).
- If not item\_list.
  - Return tuple(columns, list(), no value, no value, …).
- Set tuple(itemised\_tax, tax\_columns) from get\_tax\_accounts(item\_list, columns, company\_currency).
- Set default\_taxes from mapping().
- For each tax in tax\_columns.
  - Set default\_taxes at formatted text {tax}\_rate from 0.
  - Set default\_taxes at formatted text {tax}\_amount from 0.
- Set mode\_of\_payments from get\_mode\_of\_payments(set(generator of d.parent for d drawn from item\_list)).
  - Draw d from item\_list.
- Set so\_dn\_map from get\_delivery\_notes\_against\_sales\_order(item\_list).
- Set rows from list().
- Set customer\_details from get\_customer\_details().
- For each d in item\_list.
  - Set customer\_record from (customer\_details.get(d.customer) or Platform.\_dict(mapping(“customer\_name” → d.customer\_name, “customer\_group” → d.customer\_group))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in customer\_details.get(d.customer) → Platform.\_dict(mapping(“customer\_name” → d.customer\_name, “customer\_group” → d.customer\_group)).
  - Set tuple(delivery\_doctype, delivery\_note) from get\_delivery\_document(d, so\_dn\_map).
  - Set row from mapping(“item\_code” → d.item\_code, “item\_name” → d.si\_item\_name when d.si\_item\_name, otherwise d.i\_item\_name, “item\_group” → d.si\_item\_group when d.si\_item\_group, otherwise d.i\_item\_group, “description” →  ….
    - Value choice on d.si\_item\_name — true gives d.si\_item\_name, false gives d.i\_item\_name.
    - Value choice on d.si\_item\_group — true gives d.si\_item\_group, false gives d.i\_item\_group.
  - If (d.stock\_uom differs from d.uom and d.stock\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.stock\_uom differs from d.uom → d.stock\_qty.
    - Evaluate row.update(mapping(“rate” → ((d.base\_net\_rate × d.qty) ÷ d.stock\_qty), “amount” → d.base\_net\_amount)).
  - Otherwise.
    - Evaluate row.update(mapping(“rate” → d.base\_net\_rate, “amount” → d.base\_net\_amount)).
  - Set total\_tax from 0.
  - Set total\_other\_charges from 0.
  - Evaluate row.update(default\_taxes.copy()).
  - For each tuple(tax, details) in itemised\_tax.get(d.name, mapping()).items().
    - Evaluate row.update(mapping(formatted text {tax}\_rate → details.get(“tax\_rate”, 0), formatted text {tax}\_amount → details.get(“tax\_amount”, 0))).
    - If details.get(“is\_other\_charges”).
      - Update total\_other\_charges using + flt(details.get(“tax\_amount”)).
    - Otherwise.
      - Update total\_tax using + flt(details.get(“tax\_amount”)).
  - Evaluate row.update(mapping(“total\_tax” → total\_tax, “total\_other\_charges” → total\_other\_charges, “total” → ((d.base\_net\_amount + total\_tax) + total\_other\_charges), “currency” → company\_currency)).
  - Evaluate rows.append(tuple(d, row)).
- If filters.get(“group\_by”).
  - Return tuple(columns, get\_grouped\_data(filters, rows, tax\_columns), no value, no value, …).
- Return tuple(columns, list of row for tuple(\_item, row) drawn from rows, no value, no value, …).
  - Draw tuple(\_item, row) from rows.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1110)

<a id="op-7b5c1701de381b"></a>
### Get grouped data

`operation_enterprise_binding_enterprise_accounts_report_item_wise_sales_register_item_wise_sales_register_get_grouped_data`

**Inputs** filters, rows, tax\_columns.

**Declared result** list at dict.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set total\_row\_map from mapping().
- Set prev\_group\_by\_value from empty text.
- Set grand\_total from sum(generator of flt(row at “total”) for tuple(\_item, row) drawn from rows).
  - Draw tuple(\_item, row) from rows.
- Set tuple(group\_by\_field, subtotal\_display\_field) from get\_group\_by\_and\_display\_fields(filters).
- For each tuple(d, row) in rows.
  - Set row at “percent\_gt” from get\_percent(row at “total”, grand\_total).
  - Set tuple(data, prev\_group\_by\_value) from add\_total\_row(data, filters, prev\_group\_by\_value, d, …).
  - Evaluate add\_sub\_total\_row(row, total\_row\_map, d.get(group\_by\_field, empty text), tax\_columns).
  - Evaluate data.append(row).
- Set total\_row from total\_row\_map.get((prev\_group\_by\_value or d.get(“item\_name”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in prev\_group\_by\_value → d.get(“item\_name”).
- Set total\_row at “percent\_gt” from get\_percent(total\_row at “total”, grand\_total).
- Evaluate data.append(total\_row).
- Evaluate data.append(mapping()).
- Evaluate add\_sub\_total\_row(total\_row, total\_row\_map, “total\_row”, tax\_columns).
- Evaluate data.append(total\_row\_map.get(“total\_row”)).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1225)

<a id="op-bfd7f8a5594d57"></a>
### Get percent

`operation_enterprise_binding_enterprise_accounts_report_item_wise_sales_register_item_wise_sales_register_get_percent`

**Inputs** value, grand\_total.

**Declared result** float.

**Explicit results** ((flt(value) ÷ grand\_total) × 100) when grand\_total, otherwise 0.0.

**Local steps**

- Return ((flt(value) ÷ grand\_total) × 100) when grand\_total, otherwise 0.0.
  - Value choice on grand\_total — true gives ((flt(value) ÷ grand\_total) × 100), false gives 0.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1226)

<a id="op-92c14df10637f5"></a>
### Get income account

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_income_account`

**Inputs** row.

**Explicit results** row.deferred\_revenue\_account · row.unrealized\_profit\_loss\_account · row.income\_account.

**Local steps**

- If row.enable\_deferred\_revenue.
  - Return row.deferred\_revenue\_account.
- Otherwise.
  - If row.is\_internal\_customer equals 1.
    - Return row.unrealized\_profit\_loss\_account.
  - Otherwise.
    - Return row.income\_account.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0264.json#L5862) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1116)

<a id="op-86b84a7cfaa18b"></a>
### Get columns

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_columns`

**Inputs** additional\_table\_columns, filters.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- If filters.get(“group\_by”) differs from “Item”.
  - Evaluate columns.extend(list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “ ….
- If filters.get(“group\_by”) does not belong to tuple(“Item”, “Item Group”).
  - Evaluate columns.extend(list(mapping(“label” → translated “Item Group”, “fieldname” → “item\_group”, “fieldtype” → “Link”, “options” → “Item Group”, …))).
- Evaluate columns.extend(list(mapping(“label” → translated “Description”, “fieldname” → “description”, “fieldtype” → “Data”, “width” → 150), mapping(“label” → translated “Invoice”, “fieldname” → “invoice”, “fieldtyp ….
- If filters.get(“group\_by”) differs from “Customer”.
  - Evaluate columns.extend(list(mapping(“label” → translated “Customer Group”, “fieldname” → “customer\_group”, “fieldtype” → “Link”, “options” → “Customer Group”, …))).
- If filters.get(“group\_by”) does not belong to tuple(“Customer”, “Customer Group”).
  - Evaluate columns.extend(list(mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“label” → translated “Customer Name”, “fieldname” → “custome ….
- If additional\_table\_columns.
  - Update columns using + additional\_table\_columns.
- Update columns using + list(mapping(“label” → translated “Receivable Account”, “fieldname” → “debit\_to”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“label” → translated “Mode Of Payment”, “fieldname” → “mode\_of\_pay ….
- If filters.get(“group\_by”) differs from “Territory”.
  - Evaluate columns.extend(list(mapping(“label” → translated “Territory”, “fieldname” → “territory”, “fieldtype” → “Link”, “options” → “Territory”, …))).
- Update columns using + list(mapping(“label” → translated “Project”, “fieldname” → “project”, “fieldtype” → “Link”, “options” → “Project”, …), mapping(“label” → translated “Company”, “fieldname” → “company”, “fieldtype” → “Link”, ….
- If filters.get(“group\_by”).
  - Evaluate columns.append(mapping(“label” → translated “% Of Grand Total”, “fieldname” → “percent\_gt”, “fieldtype” → “Float”, “width” → 80)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1111)

<a id="op-ddefb03f1e2123"></a>
### Apply conditions

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_apply_conditions`

**Inputs** query, si, sii, sip, filters, additional\_conditions = no value.

**Record and data access** read “Warehouse” via get\_value · read “Warehouse” via get\_all · read “Item Group” via get\_value.

**Explicit results** query.

**Local steps**

- For each opts in tuple(“company”, “customer”).
  - If filters.get(opts).
    - Set query from query.where(si at opts equals filters at opts).
- If filters.get(“from\_date”).
  - Set query from query.where(si.posting\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Set query from query.where(si.posting\_date ≤ filters.get(“to\_date”)).
- If filters.get(“mode\_of\_payment”).
  - Set subquery from nested operand in the contract(nested operand in the contract).select(sip.parent).where(sip.mode\_of\_payment equals filters.get(“mode\_of\_payment”)).groupby(sip.parent).
  - Set query from query.where(si.name.isin(subquery)).
- If filters.get(“warehouse”).
  - If Platform.db.get\_value(“Warehouse”, filters.get(“warehouse”), “is\_group”).
    - Set tuple(lft, rgt) from Platform.db.get\_all(“Warehouse”, filters = mapping(“name” → filters.get(“warehouse”)), fields = list(“lft”, “rgt”), as\_list = true) at 0.
    - Set warehouses from Platform.db.get\_all(“Warehouse”, mapping(“lft” → tuple(“&gt;”, lft), “rgt” → tuple(“&lt;”, rgt)), pluck = “name”).
    - Set query from query.where(sii.warehouse.isin(warehouses)).
  - Otherwise.
    - Set query from query.where(sii.warehouse equals filters.get(“warehouse”)).
- If filters.get(“brand”).
  - Set query from query.where(sii.brand equals filters.get(“brand”)).
- If filters.get(“item\_code”).
  - Set query from query.where(sii.item\_code equals filters.get(“item\_code”)).
- If filters.get(“item\_group”).
  - If Platform.db.get\_value(“Item Group”, filters.get(“item\_group”), “is\_group”).
    - Set item\_groups from get\_descendants\_of(“Item Group”, filters.get(“item\_group”)).
    - Evaluate item\_groups.append(filters.get(“item\_group”)).
    - Set query from query.where(sii.item\_group.isin(item\_groups)).
  - Otherwise.
    - Set query from query.where(sii.item\_group equals filters.get(“item\_group”)).
- If filters.get(“income\_account”).
  - Set query from query.where(((sii.income\_account equals filters.get(“income\_account”) bitwise or sii.deferred\_revenue\_account equals filters.get(“income\_account”)) bitwise or si.unrealized\_profit\_loss\_account equals filte ….
- For each tuple(key, value) in (additional\_conditions or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in additional\_conditions → mapping().
  - Set query from query.where(si at key equals value).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0265.json#L2918) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1107)

<a id="op-5758dfb6970b19"></a>
### Apply order by conditions

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_apply_order_by_conditions`

**Inputs** doctype, query, filters.

**Explicit results** query.

**Local steps**

- Set invoice from Platform.qb.DocType(doctype).
- Set invoice\_item from Platform.qb.DocType(formatted text {doctype} Item).
- If not filters.get(“group\_by”).
  - Set query from query.orderby(invoice.posting\_date, order = Order.desc).
  - Set query from query.orderby(invoice\_item.item\_group, order = Order.desc).
- Otherwise.
  - If filters.get(“group\_by”) equals “Invoice”.
    - Set query from query.orderby(invoice\_item.parent, order = Order.desc).
  - Otherwise.
    - If filters.get(“group\_by”) equals “Item”.
      - Set query from query.orderby(invoice\_item.item\_code).
    - Otherwise.
      - If filters.get(“group\_by”) equals “Item Group”.
        - Set query from query.orderby(invoice\_item.item\_group).
      - Otherwise.
        - If filters.get(“group\_by”) belongs to tuple(“Customer”, “Customer Group”, “Territory”, “Supplier”).
          - Set filter\_field from Platform.scrub(filters.get(“group\_by”)).
          - Set query from query.orderby(filter\_field, order = Order.desc).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0265.json#L4734) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1108)

<a id="op-662ae625941dfe"></a>
### Get items

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_items`

**Inputs** filters, additional\_query\_columns, additional\_conditions = no value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from “Sales Invoice”.
- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set sii from Platform.qb.DocType(“Sales Invoice Item”).
- Set sip from Platform.qb.DocType(“Sales Invoice Payment”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(sii.name, sii.parent, si.posting\_date, si.debit\_to, …).where(si.docstatus equals 1).where(sii.parenttype equals doctype).
- If additional\_query\_columns.
  - For each column in additional\_query\_columns.
    - If column.get(“\_doctype”).
      - Set table from Platform.qb.DocType(column.get(“\_doctype”)).
      - Set query from query.select(table at column.get(“fieldname”)).
    - Otherwise.
      - Set query from query.select(si at column.get(“fieldname”)).
- If filters.get(“customer”).
  - Set query from query.where(si.customer equals filters at “customer”).
- If filters.get(“customer\_group”).
  - Set query from query.where(si.customer\_group equals filters at “customer\_group”).
- Set query from apply\_conditions(query, si, sii, sip, …).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(doctype).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set query from apply\_order\_by\_conditions(doctype, query, filters).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0265.json#L5390) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1117)

<a id="op-449498a7a6a464"></a>
### Get delivery document

`operation_enterprise_binding_enterprise_accounts_report_item_wise_sales_register_item_wise_sales_register_get_delivery_document`

**Inputs** item, so\_dn\_map.

**Declared result** tuple at tuple(str, (str bitwise or no value)).

**Explicit results** tuple(“Delivery Note”, item.delivery\_note) · tuple(“Sales Invoice”, item.parent) · tuple(“Delivery Note”, (“, ”.join(so\_dn\_map.get(item.so\_detail, list())) or no value)).

**Local steps**

- If item.delivery\_note.
  - Return tuple(“Delivery Note”, item.delivery\_note).
- If item.update\_stock.
  - Return tuple(“Sales Invoice”, item.parent).
- Return tuple(“Delivery Note”, (“, ”.join(so\_dn\_map.get(item.so\_detail, list())) or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “, ”.join(so\_dn\_map.get(item.so\_detail, list())) → no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1224)

<a id="op-865a531ca0cf18"></a>
### Get delivery notes against sales order

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_delivery_notes_against_sales_order`

**Inputs** item\_list.

**Explicit results** so\_dn\_map.

**Local steps**

- Set so\_dn\_map from Platform.\_dict().
- Set so\_item\_rows from list(set(list of d.so\_detail for d drawn from item\_list)).
  - Draw d from item\_list.
- If so\_item\_rows.
  - Set dn\_item from Platform.qb.DocType(“Delivery Note Item”).
  - Set delivery\_notes from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(so\_item\_rows)).groupby(dn\_item.so\_detail, dn\_item.parent).run(as\_dict = true).
  - For each dn in delivery\_notes.
    - Evaluate so\_dn\_map.setdefault(dn.so\_detail, list()).append(dn.parent).
- Return so\_dn\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0266.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1112)
