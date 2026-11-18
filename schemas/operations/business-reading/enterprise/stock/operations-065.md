# Inventory and warehouses · operations 65

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Serial no and batch traceability

<a id="op-8adc63474dbf9e"></a>
### Report Data.get data

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_data`

**Inputs** self.

**Explicit results** result\_data.

**Local steps**

- Set result\_data from list().
- If self.filters.get(“traceability\_direction”) belongs to list(“Backward”, “Both”).
  - Set data from self.split\_by\_production\_entries(self.get\_serial\_no\_batches()).
  - Set source\_data from self.prepare\_source\_data(data).
  - For each key in source\_data.
    - Set sabb\_data from source\_data at key.
    - If sabb\_data.reference\_doctype differs from “Stock Entry”.
      - Continue with the next iteration or loop test.
    - Evaluate self.set\_backward\_data(sabb\_data).
  - Evaluate self.parse\_batch\_details(source\_data, result\_data, “Backward”).
- If self.filters.get(“traceability\_direction”) belongs to list(“Forward”, “Both”).
  - Set data from self.get\_serial\_no\_batches().
  - Set batch\_details from Platform.\_dict(mapping()).
  - For each row in data.
    - Set value from (row.serial\_no or row.batch\_no).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
    - Evaluate self.set\_forward\_data(value, batch\_details).
  - Evaluate self.parse\_batch\_details(batch\_details, result\_data, “Forward”).
- Return result\_data.

**Methods declared on this owner** [split by production entries](operations-065.md#op-ba92c23dfaab7b), [get serial no batches](operations-065.md#op-6246fc6acb9a1e), [prepare source data](operations-065.md#op-bcbfbd2f13056e), [set backward data](operations-065.md#op-2e37a6496a3762), [parse batch details](operations-065.md#op-a210a6fb2ee7ae), [set forward data](operations-065.md#op-fcda904b1f2364).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L285)

<a id="op-a210a6fb2ee7ae"></a>
### Report Data.parse batch details

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_parse_batch_details`

**Inputs** self, sabb\_data\_details, data, direction, indent = 0.

**Record and data access** read “Purchase Receipt” via get\_value · read “Stock Entry” via get\_value · read “Delivery Note” via get\_value.

**Explicit results** data.

**Local steps**

- For each key in sabb\_data\_details.
  - Set sabb from sabb\_data\_details at key.
  - Set row from mapping(“item\_code” → sabb.item\_code, “batch\_no” → sabb.batch\_no, “serial\_no” → sabb.serial\_no, “warehouse” → sabb.warehouse, …).
  - If (data and indent equals 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → indent equals 0.
    - Evaluate data.append(mapping()).
  - If sabb.reference\_doctype equals “Purchase Receipt”.
    - Set row at “supplier” from Platform.db.get\_value(“Purchase Receipt”, sabb.reference\_name, “supplier”).
  - Otherwise.
    - If sabb.reference\_doctype equals “Stock Entry”.
      - Set row at “work\_order” from Platform.db.get\_value(“Stock Entry”, sabb.reference\_name, “work\_order”).
    - Otherwise.
      - If sabb.reference\_doctype equals “Delivery Note”.
        - Set row at “customer” from Platform.db.get\_value(“Delivery Note”, sabb.reference\_name, “customer”).
  - Evaluate data.append(row).
  - Set raw\_materials from sabb.get(“raw\_materials”).
  - If raw\_materials.
    - Evaluate self.parse\_batch\_details(raw\_materials, data, direction, (indent + 1)).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L294)

<a id="op-ba92c23dfaab7b"></a>
### Report Data.split by production entries

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_reportdata_split_by_production_entries`

**Inputs** self, rows.

**Explicit results** result.

**Local steps**

- Set production\_entries from self.get\_production\_entries(list of (row.serial\_no or row.batch\_no) for row drawn from rows).
  - Draw row from rows.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
- Set result from list().
- For each row in rows.
  - Set entries from production\_entries.get((row.serial\_no or row.batch\_no)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
  - If not entries.
    - Evaluate result.append(row).
    - Continue with the next iteration or loop test.
  - For each stock\_entry in entries.
    - Evaluate result.append(Platform.\_dict(row, reference\_doctype = “Stock Entry”, reference\_name = stock\_entry)).
- Return result.

**Methods declared on this owner** [get production entries](operations-065.md#op-c726eeeca39e60).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L994)

<a id="op-c726eeeca39e60"></a>
### Report Data.get production entries

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_reportdata_get_production_entries`

**Inputs** self, values.

**Explicit results** mapping() · production\_entries.

**Local steps**

- If not values.
  - Return mapping().
- Set sabb from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set sabe from Platform.qb.DocType(“Serial and Batch Entry”).
- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set value\_field from sabe.serial\_no when self.doctype\_name equals “Serial No”, otherwise sabe.batch\_no.
  - Value choice on self.doctype\_name equals “Serial No” — true gives sabe.serial\_no, false gives sabe.batch\_no.
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“value”), sabb.voucher\_no).where(((((nested operand in the contract bitwise and nested operand in th ….
- Set production\_entries from defaultdict(list).
- For each row in query.run(as\_dict = true).
  - If row.voucher\_no does not belong to production\_entries at row.value.
    - Evaluate production\_entries at row.value.append(row.voucher\_no).
- Return production\_entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L992)

<a id="op-bcbfbd2f13056e"></a>
### Report Data.prepare source data

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_prepare_source_data`

**Inputs** self, data.

**Explicit results** source\_data.

**Local steps**

- Set source\_data from Platform.\_dict(mapping()).
- For each row in data.
  - Set key from tuple(row.item\_code, row.reference\_name).
  - Set value from (row.serial\_no or row.batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
  - If value.
    - Set key from tuple(row.item\_code, row.reference\_name, value).
  - Set sabb\_details from self.get\_data\_from\_sabb(row).
  - Evaluate row.update(sabb\_details).
  - If key does not belong to source\_data.
    - Set row at “raw\_materials” from Platform.\_dict(mapping()).
    - Set source\_data at key from row.
- Return source\_data.

**Methods declared on this owner** [get data from sabb](operations-065.md#op-39f82b278dbb48).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0901.json#L6823) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L295)

<a id="op-39f82b278dbb48"></a>
### Report Data.get data from sabb

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_data_from_stock_accounting_balance`

**Inputs** self, row.

**Explicit results** mapping() · Platform.\_dict(results at 0, qty = sum(generator of flt(result.qty) for result drawn from results)).

**Local steps**

- Set sabb from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set sabb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(sabb\_entry.qty, sabb\_entry.warehouse, sabb\_entry.p ….
- If row.batch\_no.
  - Set query from query.where(sabb\_entry.batch\_no equals row.batch\_no).
- Otherwise.
  - Set query from query.where(sabb\_entry.serial\_no equals row.serial\_no).
- Set results from query.run(as\_dict = true).
- If not results.
  - Return mapping().
- Return Platform.\_dict(results at 0, qty = sum(generator of flt(result.qty) for result drawn from results)).
  - Draw result from results.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L286)

<a id="op-2e37a6496a3762"></a>
### Report Data.set backward data

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_set_backward_data`

**Inputs** self, sabb\_data, qty = no value.

**Explicit results** sabb\_data.

**Local steps**

- If qty.
  - Set sabb\_data.qty from qty.
- If “raw\_materials” does not belong to sabb\_data.
  - Set sabb\_data.raw\_materials from Platform.\_dict(mapping()).
- Evaluate self.backward\_trace\_path.add(sabb\_data.reference\_name).
- Attempt the following.
  - For each material in self.get\_materials(sabb\_data).
    - Evaluate self.add\_backward\_material(sabb\_data, material).
- On exit, including pending return or failure.
  - Evaluate self.backward\_trace\_path.discard(sabb\_data.reference\_name).
- Return sabb\_data.

**Methods declared on this owner** [get materials](operations-065.md#op-215a3b84653469), [add backward material](operations-065.md#op-5f8aa11877db7e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L297)

<a id="op-5f8aa11877db7e"></a>
### Report Data.add backward material

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_reportdata_add_backward_material`

**Inputs** self, sabb\_data, material.

**Explicit results** no value.

**Local steps**

- If (material.fg\_serial\_no and material.fg\_serial\_no differs from sabb\_data.serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in material.fg\_serial\_no → material.fg\_serial\_no differs from sabb\_data.serial\_no.
  - Return no value.
- If (material.fg\_batch\_no and material.fg\_batch\_no differs from sabb\_data.batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in material.fg\_batch\_no → material.fg\_batch\_no differs from sabb\_data.batch\_no.
  - Return no value.
- If (material.serial\_no or material.batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in material.serial\_no → material.batch\_no.
  - Evaluate self.set\_backward\_data\_for\_component(sabb\_data, material).
  - Return no value.
- Set sub\_key from tuple(material.item\_code, material.name).
- If sub\_key does not belong to sabb\_data.raw\_materials.
  - Set sabb\_data.raw\_materials at sub\_key from Platform.\_dict(mapping(“item\_code” → material.item\_code, “item\_name” → material.item\_name, “qty” → (material.qty or material.quantity), “warehouse” → material.warehouse)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in material.qty → material.quantity.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set backward data for component](operations-065.md#op-2dfe180aad9a4e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L988)

<a id="op-2dfe180aad9a4e"></a>
### Report Data.set backward data for component

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_reportdata_set_backward_data_for_component`

**Inputs** self, sabb\_data, material.

**Local steps**

- Set value from (material.serial\_no or material.batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in material.serial\_no → material.batch\_no.
- Set key from tuple(material.item\_code, material.reference\_name, material.name, value).
- If key does not belong to sabb\_data.raw\_materials.
  - For each tuple(idx, details) in enumerate(self.get\_component\_sources(value)).
    - Set sabb\_data.raw\_materials at key when idx equals 0, otherwise tuple(expanded key, details.reference\_name) from details.
      - Value choice on idx equals 0 — true gives key, false gives tuple(expanded key, details.reference\_name).
- Set sources from list of details for tuple(node\_key, details) drawn from sabb\_data.raw\_materials.items() where node\_key at slice no value to 4 equals key.
  - Draw tuple(node\_key, details) from sabb\_data.raw\_materials.items(), keep a combination only if (node\_key at slice no value to 4 equals key).
- Set produced\_qty from sum(generator of abs(flt(details.qty)) for details drawn from sources).
  - Draw details from sources.
- For each details in sources.
  - Set share from (abs(flt(details.qty)) ÷ produced\_qty) when produced\_qty, otherwise (1 ÷ len(sources)).
    - Value choice on produced\_qty — true gives (abs(flt(details.qty)) ÷ produced\_qty), false gives (1 ÷ len(sources)).
  - Evaluate self.set\_backward\_data(details, (flt(material.qty) × share)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get component sources](operations-065.md#op-3e057e14cbef1d), [set backward data](operations-065.md#op-2e37a6496a3762).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L993)

<a id="op-3e057e14cbef1d"></a>
### Report Data.get component sources

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_reportdata_get_component_sources`

**Inputs** self, value.

**Explicit results** list() · sources.

**Local steps**

- Set details from self.get\_serial\_no\_batches(value).
- If not details.
  - Set inward\_data from self.get\_sabb\_entries(value, “Inward”).
  - Set details from inward\_data at negative 1 when inward\_data, otherwise no value.
    - Value choice on inward\_data — true gives inward\_data at negative 1, false gives no value.
- If not details.
  - Return list().
- Set sources from list of source for source drawn from self.split\_by\_production\_entries(list(details)) where source.reference\_name does not belong to self.backward\_trace\_path.
  - Draw source from self.split\_by\_production\_entries(list(details)), keep a combination only if (source.reference\_name does not belong to self.backward\_trace\_path).
- If (not sources and details.reference\_name does not belong to self.backward\_trace\_path).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sources → details.reference\_name does not belong to self.backward\_trace\_path.
  - Set sources from list(details).
- For each source in sources.
  - Evaluate source.update(self.get\_data\_from\_sabb(source)).
- Return sources.

**Methods declared on this owner** [get serial no batches](operations-065.md#op-6246fc6acb9a1e), [get sabb entries](operations-065.md#op-dcfe34c25dfe70), [split by production entries](operations-065.md#op-ba92c23dfaab7b), [get data from sabb](operations-065.md#op-39f82b278dbb48).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L214) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L989)

<a id="op-6246fc6acb9a1e"></a>
### Report Data.get serial no batches

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_serial_number_batches`

**Inputs** self, name = no value.

**Explicit results** data at 0 when data, otherwise mapping() · query.run(as\_dict = true).

**Local steps**

- Set batches from self.filters.get(“batches”, list()).
- Set serial\_nos from self.filters.get(“serial\_nos”, list()).
- Set doctype from Platform.qb.DocType(self.doctype\_name).
- Set query from Platform.qb.from\_(doctype).select(doctype.reference\_doctype, doctype.reference\_name, doctype.item\_name).
- If self.doctype\_name equals “Batch”.
  - Set query from query.select(doctype.item.as\_(“item\_code”), doctype.name.as\_(“batch\_no”), doctype.expiry\_date.as\_(“batch\_expiry\_date”)).
- Otherwise.
  - Set query from query.select(doctype.item\_code, doctype.name.as\_(“serial\_no”), doctype.warranty\_expiry\_date, doctype.amc\_expiry\_date).
- If name.
  - Set query from query.where(doctype.name equals name).
  - Set data from query.run(as\_dict = true).
  - Return data at 0 when data, otherwise mapping().
    - Value choice on data — true gives data at 0, false gives mapping().
- If (batches and self.doctype\_name equals “Serial No”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batches → self.doctype\_name equals “Serial No”.
  - Set query from query.where(doctype.batch\_no.isin(batches)).
- Otherwise.
  - If batches.
    - Set query from query.where(doctype.name.isin(batches)).
  - Otherwise.
    - If serial\_nos.
      - Set query from query.where(doctype.name.isin(serial\_nos)).
- If self.filters.get(“item\_code”).
  - If self.doctype\_name equals “Serial No”.
    - Set query from query.where(doctype.item\_code equals self.filters.item\_code).
  - Otherwise.
    - Set query from query.where(doctype.item equals self.filters.item\_code).
- Set item\_field from doctype.item\_code when self.doctype\_name equals “Serial No”, otherwise doctype.item.
  - Value choice on self.doctype\_name equals “Serial No” — true gives doctype.item\_code, false gives doctype.item.
- If condition bound to get\_allowed\_masters\_condition(item\_field, “Item”).
  - Set query from query.where(condition).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L291)

<a id="op-c63a53a68c3a67"></a>
### Report Data.get doctype

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_record_type`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** “Serial No” · “Batch”.

**Local steps**

- If self.filters.item\_code.
  - Set item\_details from Platform.get\_cached\_value(“Item”, self.filters.item\_code, list(“has\_batch\_no”, “has\_serial\_no”), as\_dict = true).
  - If item\_details.has\_serial\_no.
    - Return “Serial No”.
  - Otherwise.
    - If item\_details.has\_batch\_no.
      - Return “Batch”.
- Otherwise.
  - If self.filters.get(“serial\_nos”).
    - Return “Serial No”.
- Return “Batch”.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.filters.item\_code, list(“has\_batch\_no”, “has\_serial\_no”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0902.json#L2190) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L289)

<a id="op-215a3b84653469"></a>
### Report Data.get materials

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_materials`

**Inputs** self, sabb\_data.

**Explicit results** materials.

**Local steps**

- Set stock\_entry from Platform.qb.DocType(“Stock Entry”).
- Set stock\_entry\_detail from Platform.qb.DocType(“Stock Entry Detail”).
- Set sabb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).on((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in t ….
- Set materials from query.run(as\_dict = true).
- For each material in materials.
  - Set material.qty from get\_material\_qty(material, sabb\_data.qty, self.get\_mapped\_fg\_batch\_qty(material)).
- Return materials.

**Methods declared on this owner** [get mapped fg batch qty](operations-065.md#op-3c9350ec86bef3).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L288)

<a id="op-3c9350ec86bef3"></a>
### Report Data.get mapped fg batch qty

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_reportdata_get_mapped_fg_batch_qty`

**Inputs** self, material.

**Explicit results** 0 · sum(generator of abs(flt(entry.qty)) for entry drawn from self.get\_mapped\_fg\_entries(material.reference\_name, material.item\_code) where (entry.batch\_no equals material.fg\_batch\_no and not entry.serial\_no)).

**Local steps**

- If (not material.fg\_batch\_no or material.fg\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not material.fg\_batch\_no → material.fg\_serial\_no.
  - Return 0.
- Return sum(generator of abs(flt(entry.qty)) for entry drawn from self.get\_mapped\_fg\_entries(material.reference\_name, material.item\_code) where (entry.batch\_no equals material.fg\_batch\_no and not entry.serial\_no)).
  - Draw entry from self.get\_mapped\_fg\_entries(material.reference\_name, material.item\_code), keep a combination only if ((entry.batch\_no equals material.fg\_batch\_no and not entry.serial\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.batch\_no equals material.fg\_batch\_no → not entry.serial\_no.

**Methods declared on this owner** [get mapped fg entries](operations-065.md#op-8aa8564fd76559).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L990)

<a id="op-fcda904b1f2364"></a>
### Report Data.set forward data

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_set_forward_data`

**Inputs** self, value, sabb\_data.

**Explicit results** no value.

**Local steps**

- If value belongs to self.forward\_trace\_path.
  - Return no value.
- Evaluate self.forward\_trace\_path.add(value).
- Attempt the following.
  - For each row in self.get\_sabb\_entries(value).
    - If row.reference\_doctype equals “Stock Entry”.
      - Evaluate self.process\_manufacture\_or\_repack\_entry(row, sabb\_data).
    - Otherwise.
      - Evaluate self.add\_direct\_outward\_entry(row, sabb\_data).
- On exit, including pending return or failure.
  - Evaluate self.forward\_trace\_path.discard(value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sabb entries](operations-065.md#op-dcfe34c25dfe70), [process manufacture or repack entry](operations-065.md#op-a91c24411c215b), [add direct outward entry](operations-065.md#op-67f3298ab43e1b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L298)

<a id="op-67f3298ab43e1b"></a>
### Report Data.add direct outward entry

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_add_direct_outward_entry`

**Inputs** self, row, batch\_details.

**Local steps**

- Set key from tuple(row.item\_code, row.reference\_name, row.serial\_no, row.batch\_no).
- If key does not belong to batch\_details.
  - Set row at “indent” from 0.
  - Set batch\_details at key from row.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0902.json#L3391) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L283)

<a id="op-dcfe34c25dfe70"></a>
### Report Data.get sabb entries

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_stock_accounting_balance_entries`

**Inputs** self, value, type\_of\_transaction = no value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- If not type\_of\_transaction.
  - Set type\_of\_transaction from “Outward”.
- Set SABB from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set SABE from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“reference\_doctype”), nested operand in the contract.as\_(“reference\_name”), SABE.batch\_no, SABE.seri ….
- Set query from query.where((SABE.serial\_no equals value bitwise or SABE.batch\_no equals value)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L292)

<a id="op-a91c24411c215b"></a>
### Report Data.process manufacture or repack entry

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_process_manufacture_or_repack_entry`

**Inputs** self, row, batch\_details.

**Record and data access** read “Stock Entry” via get\_value.

**Explicit results** no value.

**Local steps**

- Set ste from Platform.db.get\_value(“Stock Entry”, row.reference\_name, list(“purpose”, “work\_order”), as\_dict = true).
- If (ste and ste.purpose belongs to list(“Manufacture”, “Repack”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ste → ste.purpose belongs to list(“Manufacture”, “Repack”).
  - Set fg\_item from self.get\_finished\_item\_from\_stock\_entry(row.reference\_name).
  - If not fg\_item.
    - Return no value.
  - Set mapped\_fg\_entries from self.get\_mapped\_fg\_entries(row.reference\_name, row.item\_code).
  - Set fg\_value from (row.fg\_serial\_no or row.fg\_batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.fg\_serial\_no → row.fg\_batch\_no.
  - If fg\_value.
    - Set fg\_entries from list of entry for entry drawn from mapped\_fg\_entries where ((row.fg\_serial\_no and entry.serial\_no equals row.fg\_serial\_no) or (row.fg\_batch\_no and entry.batch\_no equals row.fg\_batch\_no)).
      - Draw entry from mapped\_fg\_entries, keep a combination only if (((row.fg\_serial\_no and entry.serial\_no equals row.fg\_serial\_no) or (row.fg\_batch\_no and entry.batch\_no equals row.fg\_batch\_no))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (row.fg\_serial\_no and entry.serial\_no equals row.fg\_serial\_no) → (row.fg\_batch\_no and entry.batch\_no equals row.fg\_batch\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.fg\_serial\_no → entry.serial\_no equals row.fg\_serial\_no.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.fg\_batch\_no → entry.batch\_no equals row.fg\_batch\_no.
    - If fg\_entries.
      - Set fg\_item from self.get\_finished\_item\_from\_stock\_entry(row.reference\_name, fg\_entries at 0.detail\_name).
  - Set key from tuple(fg\_item.item\_code, row.reference\_name, fg\_value).
  - If key does not belong to batch\_details.
    - Set tuple(serial\_no, batch\_no) from self.get\_serial\_batch\_no(fg\_item.serial\_and\_batch\_bundle).
    - If fg\_value.
      - Set tuple(serial\_no, batch\_no) from tuple(row.fg\_serial\_no, row.fg\_batch\_no).
      - Set fg\_item.qty from (sum(generator of abs(entry.qty) for entry drawn from fg\_entries) or fg\_item.qty).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in sum(generator of abs(entry.qty) for entry drawn from fg\_entries) → fg\_item.qty.
        - Draw entry from fg\_entries.
    - Otherwise.
      - If mapped\_fg\_entries.
        - Set tuple(serial\_no, batch\_no) from tuple(no value, no value).
        - Update fg\_item.qty using − sum(generator of abs(entry.qty) for entry drawn from mapped\_fg\_entries where entry.detail\_name equals fg\_item.name).
          - Draw entry from mapped\_fg\_entries, keep a combination only if (entry.detail\_name equals fg\_item.name).
    - Evaluate fg\_item.update(mapping(“work\_order” → ste.work\_order, “posting\_datetime” → row.posting\_datetime, “serial\_no” → serial\_no, “batch\_no” → batch\_no, …)).
    - Set batch\_details at key from fg\_item.
    - If (serial\_no or batch\_no).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_no → batch\_no.
      - Evaluate self.set\_forward\_data((serial\_no or batch\_no), fg\_item.raw\_materials).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_no → batch\_no.
  - Otherwise.
    - Set batch\_details at key.raw\_materials at tuple(row.item\_code, row.reference\_name, row.serial\_no, row.batch\_no) from row.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get finished item from stock entry](operations-065.md#op-252fa986463170), [get mapped fg entries](operations-065.md#op-8aa8564fd76559), [get serial batch no](operations-065.md#op-7cf0f9c30f3f18), [set forward data](operations-065.md#op-fcda904b1f2364).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L296)

<a id="op-252fa986463170"></a>
### Report Data.get finished item from stock entry

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_finished_item_from_stock_entry`

**Inputs** self, reference\_name, detail\_name = no value.

**Record and data access** read “Stock Entry Detail” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Entry Detail”, filters, list(“name”, “item\_code”, “item\_name”, “serial\_and\_batch\_bundle”, …), as\_dict = true).

**Local steps**

- Set filters from mapping(“parent” → reference\_name, “is\_finished\_item” → 1).
- If detail\_name.
  - Set filters at “name” from detail\_name.
- Return Platform.db.get\_value(“Stock Entry Detail”, filters, list(“name”, “item\_code”, “item\_name”, “serial\_and\_batch\_bundle”, …), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L287)

<a id="op-8aa8564fd76559"></a>
### Report Data.get mapped fg entries

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_reportdata_get_mapped_fg_entries`

**Inputs** self, stock\_entry, item\_code.

**Explicit results** self.mapped\_fg\_entries at tuple(stock\_entry, item\_code) · mapped\_entries.

**Local steps**

- If tuple(stock\_entry, item\_code) belongs to self.mapped\_fg\_entries.
  - Return self.mapped\_fg\_entries at tuple(stock\_entry, item\_code).
- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set sabe from Platform.qb.DocType(“Serial and Batch Entry”).
- Set mapped\_values from nested operand in the contract(nested operand in the contract, nested operand in the contract).distinct().where((((nested operand in the contract equals nested operand in the contract bitwise and nested op ….
- Set mapped\_entries from list().
- If mapped\_values.
  - Set serial\_nos from set of row.fg\_serial\_no for row drawn from mapped\_values where row.fg\_serial\_no.
    - Draw row from mapped\_values, keep a combination only if (row.fg\_serial\_no).
  - Set batch\_nos from set of row.fg\_batch\_no for row drawn from mapped\_values where row.fg\_batch\_no.
    - Draw row from mapped\_values, keep a combination only if (row.fg\_batch\_no).
  - Set fg\_entries from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“detail\_name”), sabe.serial\_no, sabe.batch\_no, sabe.qty).where((sed.parent equals stock\_entry bitwis ….
  - Set mapped\_entries from list of entry for entry drawn from fg\_entries where ((entry.serial\_no and entry.serial\_no belongs to serial\_nos) or (not entry.serial\_no and entry.batch\_no belongs to batch\_nos)).
    - Draw entry from fg\_entries, keep a combination only if (((entry.serial\_no and entry.serial\_no belongs to serial\_nos) or (not entry.serial\_no and entry.batch\_no belongs to batch\_nos))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (entry.serial\_no and entry.serial\_no belongs to serial\_nos) → (not entry.serial\_no and entry.batch\_no belongs to batch\_nos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.serial\_no → entry.serial\_no belongs to serial\_nos.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not entry.serial\_no → entry.batch\_no belongs to batch\_nos.
- Set self.mapped\_fg\_entries at tuple(stock\_entry, item\_code) from mapped\_entries.
- Return mapped\_entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L216) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L991)

<a id="op-7cf0f9c30f3f18"></a>
### Report Data.get serial batch no

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_serial_batch_number`

**Inputs** self, serial\_and\_batch\_bundle.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** tuple(serial\_nos.pop() when len(serial\_nos) equals 1, otherwise no value, batch\_nos.pop() when len(batch\_nos) equals 1, otherwise no value).

**Local steps**

- Set sabb\_details from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → serial\_and\_batch\_bundle), fields = list(“batch\_no”, “serial\_no”)).
- Set serial\_nos from set of row.serial\_no for row drawn from sabb\_details.
  - Draw row from sabb\_details.
- Set batch\_nos from set of row.batch\_no for row drawn from sabb\_details.
  - Draw row from sabb\_details.
- Return tuple(serial\_nos.pop() when len(serial\_nos) equals 1, otherwise no value, batch\_nos.pop() when len(batch\_nos) equals 1, otherwise no value).
  - Value choice on len(serial\_nos) equals 1 — true gives serial\_nos.pop(), false gives no value.
  - Value choice on len(batch\_nos) equals 1 — true gives batch\_nos.pop(), false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L290)

<a id="op-6781e289c43abd"></a>
### Report Data.get columns

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_get_columns`

**Inputs** self, has\_serial\_no = no value, has\_batch\_no = no value.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “item\_code”, “label” → translated “Item Code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“fieldname” → “item\_name”, “label” → translated “Item Name”, “fieldtype” → “D ….
- If has\_serial\_no.
  - Evaluate columns.append(mapping(“fieldname” → “serial\_no”, “label” → translated “Serial No”, “fieldtype” → “Link”, “options” → “Serial No”, …)).
- If has\_batch\_no.
  - Evaluate columns.extend(list(mapping(“fieldname” → “batch\_no”, “label” → translated “Batch No”, “fieldtype” → “Link”, “options” → “Batch”, …), mapping(“fieldname” → “batch\_expiry\_date”, “label” → translated “Batch  ….
- Evaluate columns.extend(list(mapping(“fieldname” → “qty”, “label” → translated “Quantity”, “fieldtype” → “Float”, “width” → 90), mapping(“fieldname” → “reference\_doctype”, “label” → translated “Voucher Type”, “fiel ….
- If self.filters.get(“traceability\_direction”) equals “Backward”.
  - Evaluate columns.append(mapping(“fieldname” → “supplier”, “label” → translated “Supplier”, “fieldtype” → “Link”, “options” → “Supplier”, …)).
- Otherwise.
  - Evaluate columns.append(mapping(“fieldname” → “customer”, “label” → translated “Customer”, “fieldtype” → “Link”, “options” → “Customer”, …)).
- If has\_serial\_no.
  - Evaluate columns.extend(list(mapping(“fieldname” → “warranty\_expiry\_date”, “label” → translated “Warranty Expiry (Serial)”, “fieldtype” → “Date”, “width” → 200), mapping(“fieldname” → “amc\_expiry\_date”, “label” → t ….
- Return columns.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L284)

<a id="op-7ae035d79e054e"></a>
### Get material qty

`operation_enterprise_binding_enterprise_stock_report_serial_no_and_batch_traceability_serial_no_and_batch_traceability_get_material_qty`

**Inputs** material, fg\_qty, mapped\_fg\_qty = 0.

**Explicit results** abs(flt(material.quantity)) · (abs(flt(material.quantity)) × (flt(fg\_qty) ÷ mapped\_fg\_qty) when (fg\_qty and mapped\_fg\_qty), otherwise 1.0) · (abs(flt(material.quantity)) × ratio) · (flt(material.row\_qty) × ratio).

**Local steps**

- If (material.serial\_no or material.fg\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in material.serial\_no → material.fg\_serial\_no.
  - Return abs(flt(material.quantity)).
- If material.fg\_batch\_no.
  - Return (abs(flt(material.quantity)) × (flt(fg\_qty) ÷ mapped\_fg\_qty) when (fg\_qty and mapped\_fg\_qty), otherwise 1.0).
    - Value choice on (fg\_qty and mapped\_fg\_qty) — true gives (flt(fg\_qty) ÷ mapped\_fg\_qty), false gives 1.0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fg\_qty → mapped\_fg\_qty.
- Set ratio from (flt(fg\_qty) ÷ (flt(material.fg\_completed\_qty) or flt(fg\_qty))) when fg\_qty, otherwise 1.0.
  - Value choice on fg\_qty — true gives (flt(fg\_qty) ÷ (flt(material.fg\_completed\_qty) or flt(fg\_qty))), false gives 1.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(material.fg\_completed\_qty) → flt(fg\_qty).
- If material.batch\_no.
  - Return (abs(flt(material.quantity)) × ratio).
- Return (flt(material.row\_qty) × ratio).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L212) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L987)

## Report · Serial no ledger

<a id="op-6cf2e836d5b9b1"></a>
### Execute

`operation_enterprise_stock_report_serial_number_ledger_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L1448) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L304)
