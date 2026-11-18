# Inventory and warehouses · operations 56

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Serial and batch bundle

[Record definition](../../../../data/record-types/serial_and_batch_bundle.json)

<a id="op-8b55d011f0ff48"></a>
### Serialand Batch Bundle.validate returned batch qty

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_validate_returned_batch_qty`

**Inputs** self.

**Record and data access** read child\_doctype via get\_value.

**Explicit results** no value.

**Local steps**

- Set reference\_field from mapping(“Delivery Note” → “dn\_detail”, “Sales Invoice” → “sales\_invoice\_item”).get(self.voucher\_type).
- If (self.type\_of\_transaction differs from “Inward” or not reference\_field or not self.has\_batch\_no or self.has\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.type\_of\_transaction differs from “Inward” → not reference\_field → not self.has\_batch\_no → self.has\_serial\_no.
  - Return no value.
- Set child\_doctype from (self.voucher\_type + “ Item”).
- Set original\_row from Platform.db.get\_value(child\_doctype, self.voucher\_detail\_no, reference\_field).
- Set available from (original\_row and self.get\_batch\_qty\_left\_to\_return(child\_doctype, reference\_field, original\_row)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in original\_row → self.get\_batch\_qty\_left\_to\_return(child\_doctype, reference\_field, original\_row).
- If not available.
  - Return no value.
- Set precision from self.precision(“total\_qty”).
- For each row in self.entries.
  - Set remaining from flt(available.get(row.batch\_no), precision).
  - If (row.batch\_no and flt(abs(row.qty), precision) &gt; remaining).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → flt(abs(row.qty), precision) &gt; remaining.
    - Evaluate self.throw\_error\_message(translated “Row #{0}: Cannot return {1} of Batch {2}, only {3} was delivered and not returned yet.”.format(row.idx, abs(row.qty), bold(row.batch\_no), max(remaining, 0))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get batch qty left to return](operations-056.md#op-970814260c2420), [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1094) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L591)

<a id="op-970814260c2420"></a>
### Serialand Batch Bundle.get batch qty left to return

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_batch_qty_left_to_return`

**Inputs** self, child\_doctype, reference\_field, original\_row.

**Record and data access** read child\_doctype via get\_value.

**Explicit results** mapping() · available.

**Local steps**

- Set original from Platform.db.get\_value(child\_doctype, original\_row, list(“serial\_and\_batch\_bundle”, “batch\_no”, “stock\_qty”), as\_dict = true).
- If not original.
  - Return mapping().
- Set delivered from (get\_batches\_from\_bundle(original.serial\_and\_batch\_bundle) or mapping(original.batch\_no → original.stock\_qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_batches\_from\_bundle(original.serial\_and\_batch\_bundle) → mapping(original.batch\_no → original.stock\_qty).
- Set available from mapping of batch\_no → abs(flt(qty)) for tuple(batch\_no, qty) drawn from delivered.items() where batch\_no.
  - Draw tuple(batch\_no, qty) from delivered.items(), keep a combination only if (batch\_no).
- If not available.
  - Return available.
- For each tuple(batch\_no, qty) in self.get\_returned\_batch\_qty(child\_doctype, reference\_field, original\_row).
  - Set available at batch\_no from (flt(available.get(batch\_no)) − flt(qty)).
- Return available.

**Methods declared on this owner** [get returned batch qty](operations-056.md#op-c28c79d1358345).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1083) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L580)

<a id="op-c28c79d1358345"></a>
### Serialand Batch Bundle.get returned batch qty

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_returned_batch_qty`

**Inputs** self, child\_doctype, reference\_field, original\_row.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….run().

**Local steps**

- Set child from Platform.qb.DocType(child\_doctype).
- Set parent from Platform.qb.DocType(self.voucher\_type).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1085) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L582)

<a id="op-a64ba667065bd0"></a>
### Serialand Batch Bundle.get orignal document data

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_orignal_document_data`

**Inputs** self.

**Record and data access** read child\_doc via get\_all.

**Explicit results** Platform.get\_all(child\_doc, fields = fields, filters = mapping(“name” → self.returned\_against)).

**Local steps**

- Set fields from list(“serial\_and\_batch\_bundle”, “stock\_qty”).
- If self.has\_serial\_no.
  - Evaluate fields.append(“serial\_no”).
- Otherwise.
  - If self.has\_batch\_no.
    - Evaluate fields.append(“batch\_no”).
- Set child\_doc from (self.voucher\_type + “ Item”).
- Return Platform.get\_all(child\_doc, fields = fields, filters = mapping(“name” → self.returned\_against)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L4942) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L570)

<a id="op-3a5f69366ce28e"></a>
### Serialand Batch Bundle.validate duplicate serial and batch no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_duplicate_serial_and_batch_number`

**Inputs** self.

**Local steps**

- Set serial\_nos from list().
- Set batch\_nos from list().
- For each row in self.entries.
  - If row.serial\_no.
    - Evaluate serial\_nos.append(row.serial\_no).
  - If (row.batch\_no and not row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → not row.serial\_no.
    - Evaluate batch\_nos.append(row.batch\_no).
- If serial\_nos.
  - For each tuple(key, value) in collections.Counter(serial\_nos).items().
    - If value &gt; 1.
      - Evaluate self.throw\_error\_message(formatted text Duplicate Serial No {key} found).
- If batch\_nos.
  - For each tuple(key, value) in collections.Counter(batch\_nos).items().
    - If value &gt; 1.
      - Evaluate self.throw\_error\_message(formatted text Duplicate Batch No {key} found).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L5177) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L959) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L603)

<a id="op-bf5938cb91fb82"></a>
### Serialand Batch Bundle.before cancel

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.delink\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delink serial and batch bundle](operations-056.md#op-134a541fa0376b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L5607) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L910) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L555)

<a id="op-134a541fa0376b"></a>
### Serialand Batch Bundle.delink serial and batch bundle

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_delink_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**State and service calls** request set\_value on “Stock Ledger Entry”.

**Local steps**

- Set sles from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“serial\_and\_batch\_bundle” → self.name)).
- For each sle in sles.
  - Evaluate Platform.db.set\_value(“Stock Ledger Entry”, sle.name, “serial\_and\_batch\_bundle”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L5658) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L564)

<a id="op-b453533967fda8"></a>
### Serialand Batch Bundle.child table

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_child_table`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** no value · parent\_child\_map at self.voucher\_type when self.voucher\_type belongs to parent\_child\_map, otherwise formatted text {self.voucher\_type} Item.

**Local steps**

- If self.voucher\_type equals “Job Card”.
  - Return no value.
- Set parent\_child\_map from mapping(“Asset Capitalization” → “Asset Capitalization Stock Item”, “Asset Repair” → “Asset Repair Consumed Item”, “Quotation” → “Packed Item”, “Stock Entry” → “Stock Entry Detail”).
- Return parent\_child\_map at self.voucher\_type when self.voucher\_type belongs to parent\_child\_map, otherwise formatted text {self.voucher\_type} Item.
  - Value choice on self.voucher\_type belongs to parent\_child\_map — true gives parent\_child\_map at self.voucher\_type, false gives formatted text {self.voucher\_type} Item.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0807.json#L5825) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L561)

<a id="op-ffc87310b2ed66"></a>
### Serialand Batch Bundle.delink refernce from voucher

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_delink_refernce_from_voucher`

**Inputs** self.

**Record and data access** read “Subcontracting Receipt Item” via exists · read self.child\_table via get\_all · read “Packed Item” via exists · read “Packed Item” via get\_all.

**State and service calls** request set\_value on “Packed Item” · request set\_value on self.child\_table.

**Explicit results** no value.

**Local steps**

- Set or\_filters from mapping(“serial\_and\_batch\_bundle” → self.name).
- Set fields from list(“name”, “serial\_and\_batch\_bundle”).
- If self.voucher\_type equals “Stock Reconciliation”.
  - Set fields from list(“name”, “current\_serial\_and\_batch\_bundle”, “serial\_and\_batch\_bundle”).
  - Set or\_filters at “current\_serial\_and\_batch\_bundle” from self.name.
- Otherwise.
  - If self.voucher\_type equals “Purchase Receipt”.
    - Set fields from list(“name”, “rejected\_serial\_and\_batch\_bundle”, “serial\_and\_batch\_bundle”).
    - Set or\_filters at “rejected\_serial\_and\_batch\_bundle” from self.name.
- If (self.voucher\_type equals “Subcontracting Receipt” and self.voucher\_detail\_no and not Platform.db.exists(“Subcontracting Receipt Item”, self.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Subcontracting Receipt” → self.voucher\_detail\_no → not Platform.db.exists(“Subcontracting Receipt Item”, self.voucher\_detail\_no).
  - Set self.voucher\_type from “Subcontracting Receipt Supplied”.
- Set vouchers from Platform.get\_all(self.child\_table, fields = fields, filters = mapping(“docstatus” → 0), or\_filters = or\_filters).
- If (not vouchers and self.voucher\_type equals “Delivery Note”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not vouchers → self.voucher\_type equals “Delivery Note”.
  - If Platform.db.exists(“Packed Item”, self.voucher\_detail\_no).
    - Evaluate Platform.db.set\_value(“Packed Item”, self.voucher\_detail\_no, “serial\_and\_batch\_bundle”, no value).
  - Otherwise.
    - Set packed\_items from Platform.get\_all(“Packed Item”, filters = mapping(“parent\_detail\_docname” → self.voucher\_detail\_no, “serial\_and\_batch\_bundle” → self.name), pluck = “name”).
    - For each packed\_item in packed\_items.
      - Evaluate Platform.db.set\_value(“Packed Item”, packed\_item, “serial\_and\_batch\_bundle”, no value).
  - Return no value.
- For each voucher in vouchers.
  - If voucher.get(“current\_serial\_and\_batch\_bundle”).
    - Evaluate Platform.db.set\_value(self.child\_table, voucher.name, “current\_serial\_and\_batch\_bundle”, no value).
  - Otherwise.
    - If voucher.get(“rejected\_serial\_and\_batch\_bundle”).
      - Evaluate Platform.db.set\_value(self.child\_table, voucher.name, “rejected\_serial\_and\_batch\_bundle”, no value).
  - Evaluate Platform.db.set\_value(self.child\_table, voucher.name, “serial\_and\_batch\_bundle”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1082) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L579)

<a id="op-1a4a932c7ff860"></a>
### Serialand Batch Bundle.delink reference from batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_delink_reference_from_batch`

**Inputs** self.

**Record and data access** read “Batch” via get\_all.

**State and service calls** request set\_value on “Batch”.

**Local steps**

- Set batches from Platform.get\_all(“Batch”, fields = list(“name”), filters = mapping(“reference\_name” → self.name, “reference\_doctype” → “Serial and Batch Bundle”)).
- For each batch in batches.
  - Evaluate Platform.db.set\_value(“Batch”, batch.name, mapping(“reference\_name” → no value, “reference\_doctype” → no value)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L563)

<a id="op-9b83a3b6b2c779"></a>
### Serialand Batch Bundle.validate serial and batch data

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_and_batch_data`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Voucher No is mandatory”.

**Local steps**

- If not self.voucher\_no.
  - Call the validation error handler Platform.throw(translated “Voucher No is mandatory”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L236) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L966) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L610)

<a id="op-a20df61df03fa6"></a>
### Serialand Batch Bundle.before submit

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_submitted\_with\_its\_voucher().
- Evaluate self.validate\_serial\_and\_batch\_data().
- Evaluate self.validate\_serial\_and\_batch\_no\_for\_returned().
- Evaluate self.validate\_returned\_batch\_qty().
- Evaluate self.set\_child\_details().
- Evaluate self.set\_source\_document\_no().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate submitted with its voucher](operations-056.md#op-8519c8be848aed), [validate serial and batch data](operations-056.md#op-9b83a3b6b2c779), [validate serial and batch no for returned](operations-055.md#op-5bdc8fa3a3a004), [validate returned batch qty](operations-056.md#op-8b55d011f0ff48), [set child details](operations-056.md#op-04962d4e5f28d7), [set source document no](operations-056.md#op-4b89c23b77b575).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L911) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L556)

<a id="op-8519c8be848aed"></a>
### Serialand Batch Bundle.validate submitted with its voucher

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_validate_submitted_with_its_voucher`

**Inputs** self.

**Record and data access** read self.voucher\_type via get\_value · read “Stock Ledger Entry” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Serial and Batch Bundle {0} is not posted by {1} {2}. A bundle is submitted with the transaction it belongs to.”.format(bold(self.name), self.voucher\_type, bold(self.voucher\_no)).

**Local steps**

- If (self.flags.ignore\_voucher\_validation or self.type\_of\_transaction does not belong to tuple(“Inward”, “Outward”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.ignore\_voucher\_validation → self.type\_of\_transaction does not belong to tuple(“Inward”, “Outward”).
  - Return no value.
- If (not self.voucher\_no or self.voucher\_type belongs to tuple(“Installation Note”, “Job Card”, “Maintenance Schedule”, “Pick List”, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.voucher\_no → self.voucher\_type belongs to tuple(“Installation Note”, “Job Card”, “Maintenance Schedule”, “Pick List”, …).
  - Return no value.
- If Platform.db.get\_value(self.voucher\_type, self.voucher\_no, “docstatus”) differs from 1.
  - Return no value.
- If not Platform.db.exists(“Stock Ledger Entry”, mapping(“serial\_and\_batch\_bundle” → self.name, “voucher\_no” → self.voucher\_no, “is\_cancelled” → 0)).
  - Call the validation error handler Platform.throw(translated “Serial and Batch Bundle {0} is not posted by {1} {2}. A bundle is submitted with the transaction it belongs to.”.format(bold(self.name), self.voucher\_type, bold(self.voucher\_no))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1095) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L592)

<a id="op-d38d944ee66286"></a>
### Serialand Batch Bundle.on submit

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_docstatus().
- Evaluate self.validate\_serial\_nos\_inventory().
- Evaluate self.validate\_batch\_quantity().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate docstatus](operations-056.md#op-cc77e148c05bf6), [validate serial nos inventory](operations-054.md#op-7cf520b07f7d56), [validate batch quantity](operations-056.md#op-d2f962d690d346).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L434) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L937) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L581)

<a id="op-cc77e148c05bf6"></a>
### Serialand Batch Bundle.validate docstatus

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_record_state`

**Inputs** self.

**Explicit failure paths** validation helper — translated “At Row {0}: In Serial and Batch Bundle {1} must have docstatus as 1 and not 0”.format(bold(row.idx), bold(self.name)).

**Local steps**

- For each row in self.entries.
  - <a id="op-cc77e148c05bf6-guard-3"></a>If row.docstatus differs from 1.
    - Call the validation error handler Platform.throw(translated “At Row {0}: In Serial and Batch Bundle {1} must have docstatus as 1 and not 0”.format(bold(row.idx), bold(self.name))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison row.docstatus differs from 1, row.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “At Row {0}: In Serial and Batch Bundle {1} must have docstatus as 1 and not 0”.format(bold(row.idx), bold(self.name)). With row.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cc77e148c05bf6-guard-3)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L525) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L964) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L608)

<a id="op-04962d4e5f28d7"></a>
### Serialand Batch Bundle.set child details

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_child_details`

**Inputs** self.

**Local steps**

- For each row in self.entries.
  - For each field in list(“warehouse”, “posting\_datetime”, “voucher\_type”, “voucher\_no”, …).
    - If (not row.get(field) or row.get(field) differs from self.get(field)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.get(field) → row.get(field) differs from self.get(field).
      - Evaluate row.set(field, self.get(field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L698) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L943) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L587)

<a id="op-4b89c23b77b575"></a>
### Serialand Batch Bundle.set source document no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_source_document_number`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.ignore\_validate\_serial\_batch.
  - Return no value.
- If (not self.has\_serial\_no and not self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_serial\_no → not self.has\_batch\_no.
  - Return no value.
- <a id="op-4b89c23b77b575-guard-8"></a>If self.total\_qty ≤ 0.
  - Return no value.
- If self.has\_serial\_no.
  - Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
    - Draw d from self.entries, keep a combination only if (d.serial\_no).
  - Set sn\_table from Platform.qb.DocType(“Serial No”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(sn\_table.posting\_date, getdate(nested operand in the contract.posting\_datetime)).where((nested operand in  ….run().
- If self.has\_batch\_no.
  - Set batch\_nos from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
    - Draw d from self.entries, keep a combination only if (d.batch\_no).
  - Set batch\_table from Platform.qb.DocType(“Batch”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(batch\_table.reference\_name, self.voucher\_no).where((nested operand in the contract.name.isin(batch\_nos) bi ….run().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.total\_qty ≤ 0, self.total\_qty = 0 selects the branch that returns no value. With self.total\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4b89c23b77b575-guard-8)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L952) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L593)

<a id="op-c8a5314d99a2cd"></a>
### Serialand Batch Bundle.validate serial and batch inventory

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_and_batch_inventory`

**Inputs** self.

**Local steps**

- Evaluate self.check\_future\_entries\_exists(is\_cancelled = true).
- Evaluate self.validate\_batch\_inventory().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check future entries exists](operations-055.md#op-04fc2eda12163a), [validate batch inventory](operations-056.md#op-5d0944f63c9420).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L1626) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L967) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L611)

<a id="op-5d0944f63c9420"></a>
### Serialand Batch Bundle.validate batch inventory

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_batch_inventory`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.has\_batch\_no.
  - Return no value.
- Set batches from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
  - Draw d from self.entries, keep a combination only if (d.batch\_no).
- If not batches.
  - Return no value.
- Set available\_batches from get\_auto\_batch\_nos(Platform.\_dict(mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse, “batch\_no” → batches, “consider\_negative\_batches” → true))).
- If not available\_batches.
  - Return no value.
- Set available\_batches from get\_available\_batches\_qty(available\_batches).
- For each batch\_no in batches.
  - If (batch\_no belongs to available\_batches and available\_batches at batch\_no &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no belongs to available\_batches → available\_batches at batch\_no &lt; 0.
    - If flt(available\_batches.get(batch\_no)) &lt; 0.
      - Evaluate self.validate\_negative\_batch(batch\_no, available\_batches at batch\_no).
    - Evaluate self.throw\_error\_message(translated “Batch {0} is not available in the selected warehouse {1}”.format(bold(batch\_no), self.warehouse)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate negative batch](operations-054.md#op-6d7ab4db8b61c3), [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L601)

<a id="op-483c9ad9a58f11"></a>
### Serialand Batch Bundle.on cancel

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_voucher\_no\_docstatus().
- Evaluate self.validate\_batch\_quantity().
- Evaluate self.remove\_source\_document\_no().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate voucher no docstatus](operations-057.md#op-79f0110121721c), [validate batch quantity](operations-056.md#op-d2f962d690d346), [remove source document no](operations-056.md#op-cf32bbf7ef08fa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L2216) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L936) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L580)

<a id="op-d2f962d690d346"></a>
### Serialand Batch Bundle.validate batch quantity

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_batch_quantity`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.type\_of\_transaction differs from “Outward” or self.voucher\_type equals “Stock Reconciliation”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.type\_of\_transaction differs from “Outward” → self.voucher\_type equals “Stock Reconciliation”.
  - Return no value.
- Evaluate self.validate\_future\_batch\_quantity().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate future batch quantity](operations-056.md#op-823b340a5cdc02).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L602)

<a id="op-823b340a5cdc02"></a>
### Serialand Batch Bundle.validate future batch quantity

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_validate_future_batch_quantity`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.has\_batch\_no.
  - Return no value.
- Set batch\_wise\_available\_qty from self.get\_batchwise\_available\_qty().
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- For each d in self.entries.
  - Set available\_qty from batch\_wise\_available\_qty.get(d.batch\_no, 0).
  - If flt(available\_qty, precision) &lt; 0.
    - Evaluate self.throw\_negative\_batch(d.batch\_no, available\_qty, precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get batchwise available qty](operations-057.md#op-94cf5b2dc143fa), [throw negative batch](operations-056.md#op-c40637ec7057f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1092) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L589)

<a id="op-cf32bbf7ef08fa"></a>
### Serialand Batch Bundle.remove source document no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_remove_source_document_number`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.has\_serial\_no and not self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_serial\_no → not self.has\_batch\_no.
  - Return no value.
- <a id="op-cf32bbf7ef08fa-guard-5"></a>If self.total\_qty ≤ 0.
  - Return no value.
- If self.has\_serial\_no.
  - Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
    - Draw d from self.entries, keep a combination only if (d.serial\_no).
  - Set sn\_table from Platform.qb.DocType(“Serial No”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(sn\_table.posting\_date, no value).where((((nested operand in the contract(nested operand in the contract) b ….run().
- If self.has\_batch\_no.
  - Set batch\_nos from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
    - Draw d from self.entries, keep a combination only if (d.batch\_no).
  - Set batch\_table from Platform.qb.DocType(“Batch”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(batch\_table.reference\_name, no value).where(((nested operand in the contract.isin(batch\_nos) bitwise and n ….run().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.total\_qty ≤ 0, self.total\_qty = 0 selects the branch that returns no value. With self.total\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cf32bbf7ef08fa-guard-5)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L2652) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L939) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L583)

<a id="op-c40637ec7057f2"></a>
### Serialand Batch Bundle.throw negative batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_throw_negative_batch`

**Inputs** self, batch\_no, available\_qty, precision, posting\_datetime = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with NegativeStockError — msg.

**Local steps**

- Bind dependencies NegativeStockError.
- If allow\_negative\_stock\_for\_batch(batch\_no).
  - Return no value.
- Set date\_msg from empty text.
- If posting\_datetime.
  - Set date\_msg from (one space + translated “as of {0}”.format(format\_datetime(posting\_datetime))).
- Set msg from translated multiline text in the contract.format(bold(batch\_no), bold(self.item\_code), bold(self.warehouse), date\_msg, …).
- Call the validation error handler Platform.throw(msg, title = translated “Negative Stock Error”, exc = NegativeStockError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L597)
