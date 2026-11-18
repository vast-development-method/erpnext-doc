# Inventory and warehouses · operations 60

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Serial and batch entry

[Record definition](../../../../data/record-types/serial_and_batch_entry.json)

<a id="op-89b12767080426"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_serial_and_batch_entry_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Serial and Batch Entry”.

**Local steps**

- Evaluate Platform.db.add\_index(“Serial and Batch Entry”, list(“warehouse”, “batch\_no”, “posting\_datetime”)).
- Evaluate Platform.db.add\_index(“Serial and Batch Entry”, list(“warehouse”, “serial\_no”, “posting\_datetime”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L3007) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1059) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L672)

## Report · Serial and batch summary

<a id="op-f4b958ac1c776a"></a>
### Execute

`operation_enterprise_stock_report_serial_and_batch_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set data from get\_data(filters).
- Set columns from get\_columns(filters, data).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L273)

<a id="op-f452da5b94418d"></a>
### Get data

`operation_enterprise_stock_report_serial_and_batch_summary_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Serial and Batch Bundle” via get\_all.

**Explicit results** Platform.get\_all(“Serial and Batch Bundle”, fields = list(“′tabSerial and Batch Bundle′.′voucher\_type′”, “′tabSerial and Batch Bundle′.′posting\_datetime′ as posting\_date”, “′tabSerial and Batch Bundle′.′na ….

**Local steps**

- Set filter\_conditions from get\_filter\_conditions(filters).
- Return Platform.get\_all(“Serial and Batch Bundle”, fields = list(“′tabSerial and Batch Bundle′.′voucher\_type′”, “′tabSerial and Batch Bundle′.′posting\_datetime′ as posting\_date”, “′tabSerial and Batch Bundle′.′na ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0900.json#L6205) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L276)

<a id="op-42e60c6e0a3c95"></a>
### Get filter conditions

`operation_enterprise_stock_report_serial_and_batch_summary_business_behavior_get_filter_conditions`

**Inputs** filters.

**Explicit results** filter\_conditions.

**Local steps**

- Set filter\_conditions from list(list(“Serial and Batch Entry”, “docstatus”, “=”, 1), list(“Serial and Batch Entry”, “is\_cancelled”, “=”, 0)).
- If not filters.get(“voucher\_type”).
  - Evaluate filter\_conditions.append(list(“Serial and Batch Bundle”, “voucher\_type”, “not in”, RESERVING\_VOUCHER\_TYPES)).
- For each field in list(“voucher\_type”, “voucher\_no”, “item\_code”, “warehouse”, …).
  - If filters.get(field).
    - If field equals “warehouse”.
      - Evaluate filter\_conditions.append(list(“Serial and Batch Entry”, field, “descendants of (inclusive)”, filters.get(field))).
    - Otherwise.
      - If field equals “voucher\_no”.
        - Evaluate filter\_conditions.append(list(“Serial and Batch Bundle”, field, “in”, filters.get(field))).
      - Otherwise.
        - Set doctype from “Serial and Batch Entry” when field equals “item\_code”, otherwise “Serial and Batch Bundle”.
          - Value choice on field equals “item\_code” — true gives “Serial and Batch Entry”, false gives “Serial and Batch Bundle”.
        - Evaluate filter\_conditions.append(list(doctype, field, “=”, filters.get(field))).
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Evaluate filter\_conditions.append(list(“Serial and Batch Entry”, “posting\_datetime”, “between”, list(filters.get(“from\_date”), filters.get(“to\_date”)))).
- For each field in list(“serial\_no”, “batch\_no”).
  - If filters.get(field).
    - Evaluate filter\_conditions.append(list(“Serial and Batch Entry”, field, “=”, filters.get(field))).
- Return filter\_conditions.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L277)

<a id="op-803dd067f2cbad"></a>
### Get columns

`operation_enterprise_stock_report_serial_and_batch_summary_business_behavior_get_columns`

**Inputs** filters, data.

**Record and data access** read “Item” via get\_cached\_value · read “Warehouse” via get\_cached\_value.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Company”, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”, …), mapping(“label” → translated “Serial and Batch Bundle”, “fieldname” → “name”, “fieldty ….
- Set item\_details from mapping().
- Set item\_codes from list().
- If filters.get(“voucher\_type”).
  - Set item\_codes from list of d.item\_code for d drawn from data.
    - Draw d from data.
- If (filters.get(“item\_code”) or (item\_codes and len(list(set(item\_codes))) equals 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“item\_code”) → (item\_codes and len(list(set(item\_codes))) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_codes → len(list(set(item\_codes))) equals 1.
  - Set item\_details from Platform.get\_cached\_value(“Item”, (filters.get(“item\_code”) or item\_codes at 0), list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = true).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“item\_code”) → item\_codes at 0.
- If not filters.get(“voucher\_no”).
  - Evaluate columns.extend(list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Voucher No”, “fieldname” → “vou ….
- If not filters.get(“item\_code”).
  - Evaluate columns.extend(list(mapping(“label” → translated “Item Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldname” → “item\_name”, “ ….
- If (not filters.get(“warehouse”) or Platform.get\_cached\_value(“Warehouse”, filters.warehouse, “is\_group”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.get(“warehouse”) → Platform.get\_cached\_value(“Warehouse”, filters.warehouse, “is\_group”).
  - Evaluate columns.append(mapping(“label” → translated “Warehouse”, “fieldname” → “warehouse”, “fieldtype” → “Link”, “options” → “Warehouse”, …)).
- If (not item\_details or item\_details.get(“has\_serial\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_details → item\_details.get(“has\_serial\_no”).
  - Evaluate columns.append(mapping(“label” → translated “Serial No”, “fieldname” → “serial\_no”, “fieldtype” → “Link”, “width” → 120, …)).
- If (not item\_details or item\_details.get(“has\_batch\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_details → item\_details.get(“has\_batch\_no”).
  - Evaluate columns.append(mapping(“label” → translated “Batch No”, “fieldname” → “batch\_no”, “fieldtype” → “Data”, “width” → 120)).
- Evaluate columns.extend(list(mapping(“label” → translated “Qty”, “fieldname” → “qty”, “fieldtype” → “Float”, “width” → 120), mapping(“label” → translated “Incoming Rate”, “fieldname” → “incoming\_rate”, “fieldtype”  ….
- Return columns.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, (filters.get(“item\_code”) or item\_codes at 0), list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = true), Platform.get\_cached\_value(“Warehouse”, filters.warehouse, “is\_group”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L275)

<a id="op-9e8dfb7772974c"></a>
### Get voucher type

`operation_enterprise_stock_report_serial_and_batch_summary_business_behavior_get_voucher_type`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “DocField” via get\_all.

**Explicit results** Platform.get\_all(“DocField”, filters = query\_filters, fields = list(“parent”), as\_list = true, distinct = true).

**Local steps**

- Set child\_doctypes from Platform.get\_all(“DocField”, filters = mapping(“fieldname” → “serial\_and\_batch\_bundle”), fields = list(“parent”), distinct = true).
- Set query\_filters from mapping(“options” → list(“in”, list of d.parent for d drawn from child\_doctypes)).
  - Draw d from child\_doctypes.
- If txt.
  - Set query\_filters at “parent” from list(“like”, formatted text %{txt}%).
- Return Platform.get\_all(“DocField”, filters = query\_filters, fields = list(“parent”), as\_list = true, distinct = true).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L279)

<a id="op-c22839b53b9fd8"></a>
### Get serial nos

`operation_enterprise_stock_report_serial_and_batch_summary_business_behavior_get_serial_numbers`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value · read “Serial and Batch Entry” via get\_all · read “Serial No” via get\_list.

**Explicit results** list() · Platform.get\_all(“Serial and Batch Entry”, filters = query\_filters, fields = list(“serial\_no”), as\_list = true) · Platform.get\_list(“Serial No”, filters = query\_filters, as\_list = true).

**Local steps**

- If not has\_filter\_scope(filters).
  - Return list().
- If not Platform.has\_permission(“Serial No”, “select”).
  - Return list().
- Set query\_filters from mapping().
- If txt.
  - Set query\_filters at “serial\_no” from list(“like”, formatted text %{txt}%).
- If filters.get(“voucher\_no”).
  - Set serial\_batch\_bundle from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_type” → filters at “voucher\_type”, “voucher\_no” → tuple(“in”, filters.get(“voucher\_no”)), “docstatus” → 1, “is\_cancelled” → 0), “name”).
  - Set query\_filters at “parent” from serial\_batch\_bundle.
  - If not txt.
    - Set query\_filters at “serial\_no” from tuple(“is”, “set”).
  - Return Platform.get\_all(“Serial and Batch Entry”, filters = query\_filters, fields = list(“serial\_no”), as\_list = true).
- Otherwise.
  - Set query\_filters at “item\_code” from filters.get(“item\_code”).
  - Return Platform.get\_list(“Serial No”, filters = query\_filters, as\_list = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Serial No”, “select”) · configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_type” → filters at “voucher\_type”, “voucher\_no” → tuple(“in”, filters.get(“voucher\_no”)), “docstatus” → 1, “is\_cancelled” → 0), “name”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L278)

<a id="op-386d952c22e206"></a>
### Get batch nos

`operation_enterprise_stock_report_serial_and_batch_summary_business_behavior_get_batch_numbers`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Serial and Batch Bundle” via get\_cached\_value · read “Serial and Batch Entry” via get\_all · read “Batch” via get\_list.

**Explicit results** list() · Platform.get\_all(“Serial and Batch Entry”, filters = query\_filters, fields = list(“batch\_no”), as\_list = true) · Platform.get\_list(“Batch”, filters = query\_filters, as\_list = true).

**Local steps**

- If not has\_filter\_scope(filters).
  - Return list().
- If not Platform.has\_permission(“Batch”, “select”).
  - Return list().
- Set query\_filters from mapping().
- If (filters.get(“voucher\_no”) and txt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“voucher\_no”) → txt.
  - Set query\_filters at “batch\_no” from list(“like”, formatted text %{txt}%).
- If filters.get(“voucher\_no”).
  - Set serial\_batch\_bundle from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_type” → filters at “voucher\_type”, “voucher\_no” → tuple(“in”, filters.get(“voucher\_no”)), “docstatus” → 1, “is\_cancelled” → 0), “name”).
  - Set query\_filters at “parent” from serial\_batch\_bundle.
  - If not txt.
    - Set query\_filters at “batch\_no” from tuple(“is”, “set”).
  - Return Platform.get\_all(“Serial and Batch Entry”, filters = query\_filters, fields = list(“batch\_no”), as\_list = true).
- Otherwise.
  - If txt.
    - Set query\_filters at “name” from list(“like”, formatted text %{txt}%).
  - Set query\_filters at “item” from filters.get(“item\_code”).
  - Return Platform.get\_list(“Batch”, filters = query\_filters, as\_list = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Batch”, “select”) · configured or stored value from Platform.get\_cached\_value(“Serial and Batch Bundle”, mapping(“voucher\_type” → filters at “voucher\_type”, “voucher\_no” → tuple(“in”, filters.get(“voucher\_no”)), “docstatus” → 1, “is\_cancelled” → 0), “name”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L274)

<a id="op-b8560fbd4aca94"></a>
### Has filter scope

`operation_enterprise_binding_enterprise_stock_report_serial_and_batch_summary_serial_and_batch_summary_has_filter_scope`

**Inputs** filters.

**Explicit results** false · true.

**Local steps**

- If (not filters.get(“item\_code”) and not filters.get(“voucher\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.get(“item\_code”) → not filters.get(“voucher\_no”).
  - Return false.
- If (filters.get(“voucher\_no”) and not filters.get(“voucher\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“voucher\_no”) → not filters.get(“voucher\_type”).
  - Return false.
- Set voucher\_nos from (filters.get(“voucher\_no”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“voucher\_no”) → list().
- If isinstance(voucher\_nos, str).
  - Set voucher\_nos from list(voucher\_nos).
- For each voucher\_no in voucher\_nos.
  - Evaluate Platform.has\_permission(filters at “voucher\_type”, “read”, voucher\_no, throw = true).
- If filters.get(“item\_code”).
  - Evaluate Platform.has\_permission(“Item”, “read”, filters at “item\_code”, throw = true).
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(filters at “voucher\_type”, “read”, voucher\_no, throw = true), Platform.has\_permission(“Item”, “read”, filters at “item\_code”, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L211) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L986)

## Service · Serial batch bundle

<a id="op-fc2fdcc8ebb4aa"></a>
### Get serial no status

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_serial_number_status`

**Inputs** sle.

**Record and data access** read “Stock Entry” via get\_cached\_value.

**Explicit results** “Active” · status.

**Local steps**

- Set warehouse from sle.warehouse when sle.actual\_qty &gt; 0, otherwise no value.
  - Value choice on sle.actual\_qty &gt; 0 — true gives sle.warehouse, false gives no value.
- If warehouse.
  - Return “Active”.
- Set status from get\_status\_for\_serial\_nos(sle).
- If (sle.voucher\_type equals “Stock Entry” and sle.actual\_qty &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Entry” → sle.actual\_qty &lt; 0.
  - Set purpose from Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”).
  - If purpose belongs to INACTIVE\_SERIAL\_NO\_STOCK\_ENTRY\_PURPOSES.
    - Set status from “Inactive”.
- Return status.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L6384) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1061) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L633)

<a id="op-31f84708bb12d1"></a>
### Get status for serial nos

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_status_for_serial_numbers`

**Inputs** sle.

**Record and data access** read “Stock Entry” via get\_cached\_value.

**Explicit results** status.

**Local steps**

- Set status from “Inactive”.
- If (sle.actual\_qty &lt; 0 and sle.voucher\_type does not belong to list(“Purchase Invoice”, “Purchase Receipt”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.actual\_qty &lt; 0 → sle.voucher\_type does not belong to list(“Purchase Invoice”, “Purchase Receipt”).
  - Set status from “Delivered”.
  - If sle.voucher\_type equals “Stock Entry”.
    - Set purpose from Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”).
    - If purpose belongs to CONSUMED\_SERIAL\_NO\_STOCK\_ENTRY\_PURPOSES.
      - Set status from “Consumed”.
  - If (sle.is\_cancelled equals 1 and (sle.voucher\_type belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Stock Reconciliation”) or status equals “Consumed”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.is\_cancelled equals 1 → (sle.voucher\_type belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Stock Reconciliation”) or status equals “Consumed”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.voucher\_type belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Stock Reconciliation”) → status equals “Consumed”.
    - Set status from “Inactive”.
- Return status.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1067) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L639)

<a id="op-ffa173a0694b97"></a>
### Get serial no status term

`operation_enterprise_binding_enterprise_stock_serial_batch_bundle_get_serial_no_status_term`

**Inputs** sn\_table, sle, warehouse, status.

**Explicit results** “Active” · status · Case().when(sn\_table.reference\_name equals sle.voucher\_no, “Inactive”).else\_(status).

**Local steps**

- If warehouse.
  - Return “Active”.
- If not sle.is\_cancelled.
  - Return status.
- Return Case().when(sn\_table.reference\_name equals sle.voucher\_no, “Inactive”).else\_(status).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1072)

<a id="op-95a4bf573c62e6"></a>
### Serial Batch Bundle.initialize

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_initialize`

**Inputs** self, remaining named values kwargs.

**Local steps**

- For each tuple(key, value) in kwargs.items().
  - Evaluate setattr(self, key, value).
- Evaluate self.set\_item\_details().
- Evaluate self.process\_serial\_and\_batch\_bundle().
- If self.sle.is\_cancelled.
  - Evaluate self.delink\_serial\_and\_batch\_bundle().
- Evaluate self.post\_process().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set item details](operations-060.md#op-43ade651b293e9), [process serial and batch bundle](operations-060.md#op-edc7873117190b), [delink serial and batch bundle](operations-061.md#op-43a7acd2290c7b), [post process](operations-061.md#op-e62993cd0eeaff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L6966) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1073) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L645)

<a id="op-edc7873117190b"></a>
### Serial Batch Bundle.process serial and batch bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_process_serial_and_batch_bundle`

**Inputs** self.

**Local steps**

- If self.item\_details.has\_serial\_no.
  - Evaluate self.process\_serial\_no().
- Otherwise.
  - If self.item\_details.has\_batch\_no.
    - Evaluate self.process\_batch\_no().

If control reaches the end, it returns no value.

**Methods declared on this owner** [process serial no](operations-060.md#op-fbfdcd08be9a04), [process batch no](operations-061.md#op-0a86cdadca10be).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L7163) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1082) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L654)

<a id="op-43ade651b293e9"></a>
### Serial Batch Bundle.set item details

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_set_item_details`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set fields from list(“has\_batch\_no”, “has\_serial\_no”, “item\_name”, “item\_group”, …).
- Set self.item\_details from Platform.get\_cached\_value(“Item”, self.sle.item\_code, fields, as\_dict = 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.sle.item\_code, fields, as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0925.json#L7271) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1085) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L657)

<a id="op-fbfdcd08be9a04"></a>
### Serial Batch Bundle.process serial no

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_process_serial_number`

**Inputs** self.

**Local steps**

- If (not self.sle.is\_cancelled and not self.sle.serial\_and\_batch\_bundle and self.item\_details.has\_serial\_no equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sle.is\_cancelled → not self.sle.serial\_and\_batch\_bundle → self.item\_details.has\_serial\_no equals 1.
  - Evaluate self.make\_serial\_batch\_no\_bundle().
- Otherwise.
  - If not self.sle.is\_cancelled.
    - Evaluate self.validate\_item\_and\_warehouse().

If control reaches the end, it returns no value.

**Methods declared on this owner** [make serial batch no bundle](operations-060.md#op-49a89cdbc6e608), [validate item and warehouse](operations-061.md#op-4adecaec74981a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1083) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L655)

<a id="op-1292a2c6991f3b"></a>
### Serial Batch Bundle.is material transfer

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_is_material_transfer`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_cached\_value.

**Explicit results** true.

**Local steps**

- Set allowed\_types from list(“Material Transfer”, “Send to Subcontractor”, “Material Transfer for Manufacture”).
- If (self.sle.voucher\_type equals “Stock Entry” and not self.sle.is\_cancelled and Platform.get\_cached\_value(“Stock Entry”, self.sle.voucher\_no, “purpose”) belongs to allowed\_types).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.voucher\_type equals “Stock Entry” → not self.sle.is\_cancelled → Platform.get\_cached\_value(“Stock Entry”, self.sle.voucher\_no, “purpose”) belongs to allowed\_types.
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry”, self.sle.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0926.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1074) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L646)

<a id="op-f0b23e84b0d405"></a>
### Serial Batch Bundle.get transit package

`operation_enterprise_binding_enterprise_stock_serial_batch_bundle_serialbatchbundle_get_transit_package`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** no value · Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_no” → self.sle.voucher\_no, “voucher\_detail\_no” → self.sle.voucher\_detail\_no, “item\_code” → self.sle.item\_code, “actual\_qty” → tuple(“&lt;”, 0), …), ….

**Local steps**

- If (self.sle.is\_cancelled or self.sle.voucher\_type does not belong to list(“Delivery Note”, “Sales Invoice”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.sle.is\_cancelled → self.sle.voucher\_type does not belong to list(“Delivery Note”, “Sales Invoice”).
  - Return no value.
- Return Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_no” → self.sle.voucher\_no, “voucher\_detail\_no” → self.sle.voucher\_detail\_no, “item\_code” → self.sle.item\_code, “actual\_qty” → tuple(“&lt;”, 0), …), ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1075)

<a id="op-a452082c65dba4"></a>
### Serial Batch Bundle.make serial batch no bundle for material transfer

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_make_serial_batch_number_bundle_for_material_transfer`

**Inputs** self, bundle.

**State and service calls** call db\_set on self.sle.

**Explicit results** no value.

**Local steps**

- Bind dependencies make\_bundle\_for\_material\_transfer.
- If not bundle.
  - Return no value.
- Set new\_bundle\_id from make\_bundle\_for\_material\_transfer(is\_new = false, docstatus = 1, voucher\_type = self.sle.voucher\_type, voucher\_no = self.sle.voucher\_no, …).
  - Value choice on self.sle.actual\_qty &gt; 0 — true gives “Inward”, false gives “Outward”.
- Evaluate self.sle.db\_set(mapping(“serial\_and\_batch\_bundle” → new\_bundle\_id)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1079) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L651)

<a id="op-49a89cdbc6e608"></a>
### Serial Batch Bundle.make serial batch no bundle

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_make_serial_batch_number_bundle`

**Inputs** self.

**Record and data access** read “Stock Entry Detail” via get\_value.

**State and service calls** request set\_value on self.child\_doctype.

**Explicit results** no value.

**Local steps**

- If (self.sle.actual\_qty &gt; 0 and transit\_package bound to self.get\_transit\_package()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.actual\_qty &gt; 0 → transit\_package bound to self.get\_transit\_package().
  - Evaluate self.make\_serial\_batch\_no\_bundle\_for\_material\_transfer(transit\_package).
  - If not self.is\_packed\_entry().
    - Evaluate Platform.db.set\_value(self.child\_doctype, self.sle.voucher\_detail\_no, “serial\_and\_batch\_bundle”, self.sle.serial\_and\_batch\_bundle).
  - Return no value.
- Evaluate self.validate\_item().
- If (self.sle.actual\_qty &gt; 0 and self.is\_material\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.actual\_qty &gt; 0 → self.is\_material\_transfer().
  - Evaluate self.make\_serial\_batch\_no\_bundle\_for\_material\_transfer(Platform.db.get\_value(“Stock Entry Detail”, self.sle.voucher\_detail\_no, “serial\_and\_batch\_bundle”)).
  - Return no value.
- Set sn\_doc from SerialBatchCreation(mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse, “posting\_datetime” → self.sle.posting\_datetime, “voucher\_type” → self.sle.voucher\_type, …)).make\_serial\_and\_batch\_bundle().
  - Value choice on self.sle.actual\_qty &gt; 0 — true gives “Inward”, false gives “Outward”.
- Evaluate self.set\_serial\_and\_batch\_bundle(sn\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get transit package](operations-060.md#op-f0b23e84b0d405), [make serial batch no bundle for material transfer](operations-060.md#op-a452082c65dba4), [is packed entry](operations-061.md#op-323cf5ccc8e185), [validate item](operations-060.md#op-eb171a78d66792), [is material transfer](operations-060.md#op-1292a2c6991f3b), [is rejected entry](operations-061.md#op-58e15093bfdbaf), [get entries held by voucher](operations-060.md#op-c8f080010a68e6), [set serial and batch bundle](operations-061.md#op-5154e4af494f6a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1078) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L650)

<a id="op-c8f080010a68e6"></a>
### Serial Batch Bundle.get entries held by voucher

`operation_enterprise_binding_enterprise_stock_serial_batch_bundle_serialbatchbundle_get_entries_held_by_voucher`

**Inputs** self.

**Explicit results** mapping() · mapping(“ignore\_serial\_nos” → list of row.serial\_no for row drawn from entries where row.serial\_no, “already\_picked\_batches” → held\_batches).

**Local steps**

- If self.sle.actual\_qty &gt; 0.
  - Return mapping().
- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set entries from nested operand in the contract(nested operand in the contract).select(entry.serial\_no, entry.batch\_no, entry.qty, bundle.warehouse).where(((((nested operand in the contract bitwise or nested operand in the ….
- Set held\_batches from Platform.\_dict().
- For each row in entries.
  - If row.batch\_no.
    - Set held from held\_batches.setdefault(tuple(row.batch\_no, row.warehouse), Platform.\_dict(batch\_no = row.batch\_no, warehouse = row.warehouse, qty = 0)).
    - Update held.qty using + row.qty.
- Return mapping(“ignore\_serial\_nos” → list of row.serial\_no for row drawn from entries where row.serial\_no, “already\_picked\_batches” → held\_batches).
  - Draw row from entries, keep a combination only if (row.serial\_no).

**Methods declared on this owner** [get bundles on voucher rows](operations-060.md#op-ee0ee286cbf1b8).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1074)

<a id="op-ee0ee286cbf1b8"></a>
### Serial Batch Bundle.get bundles on voucher rows

`operation_enterprise_binding_enterprise_stock_serial_batch_bundle_serialbatchbundle_get_bundles_on_voucher_rows`

**Inputs** self, doctype.

**Explicit results** nested operand in the contract.qb.from\_(row).select(row.serial\_and\_batch\_bundle).where((row.parenttype equals self.sle.voucher\_type bitwise and row.parent equals self.sle.voucher\_no)).

**Local steps**

- Set row from Platform.qb.DocType(doctype).
- Return nested operand in the contract.qb.from\_(row).select(row.serial\_and\_batch\_bundle).where((row.parenttype equals self.sle.voucher\_type bitwise and row.parent equals self.sle.voucher\_no)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1073)

<a id="op-238b03afd46aad"></a>
### Serial Batch Bundle.validate actual qty

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_validate_actual_quantity`

**Inputs** self, sn\_doc.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set link from get\_link\_to\_form(“Serial and Batch Bundle”, sn\_doc.name).
- Set condition from mapping(“Inward” → self.sle.actual\_qty &gt; 0, “Outward” → self.sle.actual\_qty &lt; 0).get(sn\_doc.type\_of\_transaction).
- If (not condition and self.sle.actual\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not condition → self.sle.actual\_qty.
  - Set correct\_type from “Inward”.
  - If sn\_doc.type\_of\_transaction equals “Inward”.
    - Set correct\_type from “Outward”.
  - Set msg from translated “The type of transaction of Serial and Batch Bundle {0} is {1} but as per the Actual Qty {2} for the item {3} …”.format(link, bold(translated sn\_doc.type\_of\_transaction), self.sle.actual\_qty, bo ….
  - Call the validation error handler Platform.throw(msg, title = translated “Incorrect Type of Transaction”).
- Set precision from sn\_doc.precision(“total\_qty”).
- If (self.sle.actual\_qty and flt(sn\_doc.total\_qty, precision) differs from flt(self.sle.actual\_qty, precision)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.sle.actual\_qty → flt(sn\_doc.total\_qty, precision) differs from flt(self.sle.actual\_qty, precision).
  - Set msg from translated “Total qty {0} of Serial and Batch Bundle {1} is not equal to Actual Qty {2} in the {3} {4}”.format(flt(sn\_doc.total\_qty, precision), link, flt(self.sle.actual\_qty, precision), translated self.s ….
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1091) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L663)

<a id="op-eb171a78d66792"></a>
### Serial Batch Bundle.validate item

`operation_enterprise_stock_serial_batch_bundle_business_behavior_serial_batch_bundle_validate_item`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit failure paths** validation helper — “. ”.join(list(msg, expanded hints)).

**Local steps**

- Set hints from list().
- If self.sle.actual\_qty &gt; 0.
  - If (not self.item\_details.has\_batch\_no and not self.item\_details.has\_serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.item\_details.has\_batch\_no → not self.item\_details.has\_serial\_no.
    - Evaluate hints.append(translated “Item {0} is not a batch or serial no item”.format(self.item\_code)).
  - If (self.item\_details.has\_serial\_no and not self.item\_details.serial\_no\_series).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_details.has\_serial\_no → not self.item\_details.serial\_no\_series.
    - Evaluate hints.append(translated “If you want auto pick serial bundle, then kindly set Serial No Series in Item {0}”.format(self.item\_code)).
  - If (self.item\_details.has\_batch\_no and not self.item\_details.batch\_number\_series and not Platform.get\_single\_value(“Stock Settings”, “naming\_series\_prefix”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_details.has\_batch\_no → not self.item\_details.batch\_number\_series → not Platform.get\_single\_value(“Stock Settings”, “naming\_series\_prefix”).
    - Evaluate hints.append(translated “If you want auto pick batch bundle, then kindly set Batch Number Series in Item {0}”.format(self.item\_code)).
- Otherwise.
  - If self.sle.actual\_qty &lt; 0.
    - If not Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).
      - Evaluate hints.append(translated “If you want auto pick serial/batch bundle, then kindly enable 'Auto Create Serial and Batch Bundle' in Stock …”).
- If hints.
  - Set msg from translated “Serial and Batch Bundle not set for item {0} in warehouse {1}”.format(self.item\_code, self.warehouse).
  - Call the validation error handler Platform.throw(“. ”.join(list(msg, expanded hints))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “naming\_series\_prefix”), Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1092) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L664)
