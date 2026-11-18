# Subcontracting · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subcontracting receipt

[Record definition](../../../../data/record-types/subcontracting_receipt.json)

<a id="op-da4e110d800b33"></a>
### Get tax terms

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_get_tax_terms`

**Inputs** taxes, key\_fields.

**Declared result** tuple.

**Explicit results** tuple(generator of tuple(row.charge\_type, row.row\_id, flt(row.rate), row.included\_in\_print\_rate, …) for row drawn from taxes where (has\_row\_based\_tax or row.charge\_type differs from “Actual”)).

**Local steps**

- Set has\_row\_based\_tax from any(generator of row.charge\_type belongs to ROW\_BASED\_CHARGE\_TYPES for row drawn from taxes).
  - Draw row from taxes.
- Return tuple(generator of tuple(row.charge\_type, row.row\_id, flt(row.rate), row.included\_in\_print\_rate, …) for row drawn from taxes where (has\_row\_based\_tax or row.charge\_type differs from “Actual”)).
  - Draw row from taxes, keep a combination only if ((has\_row\_based\_tax or row.charge\_type differs from “Actual”)).
  - Draw field from key\_fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_row\_based\_tax → row.charge\_type differs from “Actual”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1203)

<a id="op-4440c8f5e80a8c"></a>
### Get charge key fields

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_get_charge_key_fields`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list(“account\_head”, “category”, “add\_deduct\_tax”, “cost\_center”, …).

**Local steps**

- Return list(“account\_head”, “category”, “add\_deduct\_tax”, “cost\_center”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1198)

<a id="op-0ceb3eb1d05153"></a>
### Get uncombinable orders message

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_get_uncombinable_orders_message`

**Inputs** purchase\_orders.

**Declared result** str.

**Explicit results** translated “Purchase Orders {0} have different currencies, taxes or discounts, so they cannot share one Purchase Receipt …”.format(comma\_and(list of get\_link\_to\_form(“Purchase Order”, name) for name drawn  ….

**Local steps**

- Return translated “Purchase Orders {0} have different currencies, taxes or discounts, so they cannot share one Purchase Receipt …”.format(comma\_and(list of get\_link\_to\_form(“Purchase Order”, name) for name drawn  ….
  - Draw name from purchase\_orders.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1204)

<a id="op-15ca17bb5f0b16"></a>
### Add po items to pr

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_add_po_items_to_pr`

**Inputs** scr\_doc, target\_doc.

**Record and data access** resolve a document from “Purchase Order” via get\_doc.

**Local steps**

- Set fg\_items from mapping of tuple(item.item\_code, item.purchase\_order) → item.qty for item drawn from scr\_doc.items.
  - Draw item from scr\_doc.items.
- For each tuple(tuple(item\_code, po\_name), fg\_qty) in fg\_items.items().
  - Set po\_doc from Platform.get\_doc(“Purchase Order”, po\_name).
  - For each item in po\_doc.items.
    - If item.fg\_item differs from item\_code.
      - Continue with the next iteration or loop test.
    - Set qty from (((item.stock\_qty − item.received\_qty) × fg\_qty) ÷ item.fg\_item\_qty).
    - If qty.
      - Evaluate target\_doc.append(“items”, mapping(“item\_code” → item.item\_code, “item\_name” → item.item\_name, “description” → item.description, “qty” → qty, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1196)

<a id="op-e335f39eecd268"></a>
### Get data

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_subcontracting_receipt_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “subcontracting\_receipt”, “non\_standard\_fieldnames” → mapping(“Subcontracting Receipt” → “return\_against”), “internal\_links” → mapping(“Subcontracting Order” → list(“items”, “subcontr ….

**Local steps**

- Return mapping(“fieldname” → “subcontracting\_receipt”, “non\_standard\_fieldnames” → mapping(“Subcontracting Receipt” → “return\_against”), “internal\_links” → mapping(“Subcontracting Order” → list(“items”, “subcontr ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L4932) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1064)

## Service · Utils

<a id="op-8745cf19007fdd"></a>
### Get inward order filters

`operation_enterprise_binding_enterprise_subcontracting_report_utils_get_inward_order_filters`

**Inputs** filters.

**Explicit results** order\_filters.

**Local steps**

- Set order\_filters from list(list(“docstatus”, “=”, 1), list(“company”, “=”, filters.company), list(“transaction\_date”, “between”, list(filters.from\_date, filters.to\_date))).
- If filters.get(“customer”).
  - Evaluate order\_filters.append(list(“customer”, “=”, filters.customer)).
- Return order\_filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1249)

<a id="op-9f543e5509362b"></a>
### Get open inward order rows

`operation_enterprise_binding_enterprise_subcontracting_report_utils_get_open_inward_order_rows`

**Inputs** filters, table\_fieldname, fields, extra\_filters.

**Record and data access** read “Subcontracting Inward Order” via get\_list.

**Explicit results** Platform.get\_list(“Subcontracting Inward Order”, fields = list(“name as subcontracting\_inward\_order”, “transaction\_date”, “customer”, expanded list of formatted text {table\_fieldname}.{field} for field dra ….

**Local steps**

- Return Platform.get\_list(“Subcontracting Inward Order”, fields = list(“name as subcontracting\_inward\_order”, “transaction\_date”, “customer”, expanded list of formatted text {table\_fieldname}.{field} for field dra ….
  - Draw field from fields.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1250)

<a id="op-563567e3512d1d"></a>
### Get inward order columns

`operation_enterprise_binding_enterprise_subcontracting_report_utils_get_inward_order_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Subcontracting Inward Order”, “fieldname” → “subcontracting\_inward\_order”, “fieldtype” → “Link”, “options” → “Subcontracting Inward Order”, …), mapping(“label” → translat ….

**Local steps**

- Return list(mapping(“label” → translated “Subcontracting Inward Order”, “fieldname” → “subcontracting\_inward\_order”, “fieldtype” → “Link”, “options” → “Subcontracting Inward Order”, …), mapping(“label” → translat ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1248)
