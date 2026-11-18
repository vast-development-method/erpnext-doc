# Inventory and warehouses · operations 48

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Putaway rule

[Record definition](../../../../data/record-types/putaway_rule.json)

<a id="op-7dd0a324f313b3"></a>
### Get item putaway rules

`operation_enterprise_binding_enterprise_stock_doctype_putaway_rule_putaway_rule_get_item_putaway_rules`

**Inputs** item\_code, company.

**Record and data access** read “Putaway Rule” via get\_all.

**Explicit results** rules.

**Local steps**

- Set rules from Platform.get\_all(“Putaway Rule”, fields = list(“name”, “item\_code”, “stock\_capacity”, “priority”, …), filters = mapping(“item\_code” → item\_code, “company” → company, “disable” → 0), order\_by = “priority as ….
- For each rule in rules.
  - Set balance\_qty from \_get\_stock\_balance(rule.item\_code, rule.warehouse, nowdate()).
  - Set rule at “free\_space” from max((flt(rule.stock\_capacity) − flt(balance\_qty)), 0).
- Return rules.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1040) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L537)

<a id="op-3524aa08e4d36c"></a>
### Select vacant rules

`operation_enterprise_binding_enterprise_stock_doctype_putaway_rule_putaway_rule_select_vacant_rules`

**Inputs** rules, source\_warehouse = no value.

**Explicit results** tuple(false, no value) · tuple(true, no value) · tuple(false, sorted(vacant\_rules, key = deferred anonymous expression)).

**Local steps**

- Set rules from list of rule for rule drawn from rules where rule.warehouse differs from source\_warehouse.
  - Draw rule from rules, keep a combination only if (rule.warehouse differs from source\_warehouse).
- If not rules.
  - Return tuple(false, no value).
- Set vacant\_rules from list of rule for rule drawn from rules where rule.free\_space &gt; 0.
  - Draw rule from rules, keep a combination only if (rule.free\_space &gt; 0).
- If not vacant\_rules.
  - Return tuple(true, no value).
- Return tuple(false, sorted(vacant\_rules, key = deferred anonymous expression)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1042) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L539)

<a id="op-605d514d481272"></a>
### Add row

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_add_row`

**Inputs** item, to\_allocate, warehouse, updated\_table, rule = no value, serial\_nos = no value, keep\_rejected = false.

**Explicit results** updated\_table.

**Local steps**

- Set new\_updated\_table\_row from copy.deepcopy(item).
- Set new\_updated\_table\_row.idx from 1 when not updated\_table, otherwise (cint(updated\_table at negative 1.idx) + 1).
  - Value choice on not updated\_table — true gives 1, false gives (cint(updated\_table at negative 1.idx) + 1).
- Set new\_updated\_table\_row.name from no value.
- Set new\_updated\_table\_row.qty from to\_allocate.
- If item.doctype equals “Stock Entry Detail”.
  - Set new\_updated\_table\_row.t\_warehouse from warehouse.
  - Set new\_updated\_table\_row.transfer\_qty from (flt(to\_allocate) × flt(new\_updated\_table\_row.conversion\_factor)).
- Otherwise.
  - Set new\_updated\_table\_row.stock\_qty from (flt(to\_allocate) × flt(new\_updated\_table\_row.conversion\_factor)).
  - Set new\_updated\_table\_row.warehouse from warehouse.
  - If not keep\_rejected.
    - Set new\_updated\_table\_row.rejected\_qty from 0.
  - Set new\_updated\_table\_row.received\_qty from (flt(to\_allocate) + flt(new\_updated\_table\_row.rejected\_qty)).
- If rule.
  - Set new\_updated\_table\_row.putaway\_rule from rule.
- If serial\_nos.
  - Set new\_updated\_table\_row.serial\_no from get\_serial\_nos\_to\_allocate(serial\_nos, (flt(to\_allocate) × flt((new\_updated\_table\_row.conversion\_factor or 1)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_updated\_table\_row.conversion\_factor → 1.
- If (item.get(“use\_serial\_batch\_fields”) or item.get(“serial\_no”) or item.get(“batch\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“use\_serial\_batch\_fields”) → item.get(“serial\_no”) → item.get(“batch\_no”).
  - Set new\_updated\_table\_row.serial\_and\_batch\_bundle from empty text.
- If not keep\_rejected.
  - Set new\_updated\_table\_row.rejected\_serial\_and\_batch\_bundle from empty text.
- Evaluate updated\_table.append(new\_updated\_table\_row).
- Return updated\_table.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L341)

<a id="op-ed1400a36a1df2"></a>
### Split bundles

`operation_enterprise_binding_enterprise_stock_doctype_putaway_rule_putaway_rule_split_bundles`

**Inputs** rows, doctype, keep\_original = true.

**Record and data access** read “Serial and Batch Bundle” via get\_all · resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** request copy\_doc for bundle · call save on doc.

**Local steps**

- Set qty\_field from “transfer\_qty” when doctype equals “Stock Entry”, otherwise “stock\_qty”.
  - Value choice on doctype equals “Stock Entry” — true gives “transfer\_qty”, false gives “stock\_qty”.
- Set warehouse\_field from “t\_warehouse” when doctype equals “Stock Entry”, otherwise “warehouse”.
  - Value choice on doctype equals “Stock Entry” — true gives “t\_warehouse”, false gives “warehouse”.
- Set rows\_by\_bundle from defaultdict(list).
- For each row in rows.
  - If row.get(“serial\_and\_batch\_bundle”).
    - Evaluate rows\_by\_bundle at row.get(“serial\_and\_batch\_bundle”).append(row).
- Set precision from Platform.get\_precision(“Serial and Batch Bundle”, “total\_qty”).
- For each bundle in Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“name” → tuple(“in”, list(rows\_by\_bundle))), fields = list(“name”, “total\_qty”, “warehouse”, “type\_of\_transaction”)).
  - Set bundle\_rows from rows\_by\_bundle at bundle.name.
  - Set qtys from list of abs(flt(row.get(qty\_field))) for row drawn from bundle\_rows.
    - Draw row from bundle\_rows.
  - If (len(bundle\_rows) equals 1 and not flt((qtys at 0 − abs(flt(nested operand in the contract.total\_qty))), precision) and (bundle.type\_of\_transaction equals “Outward” or bundle.warehouse equals bundle\_rows a ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(bundle\_rows) equals 1 → not flt((qtys at 0 − abs(flt(bundle.total\_qty))), precision) → (bundle.type\_of\_transaction equals “Outward” or bundle.warehouse equals bundle\_rows at 0.get(warehouse\_field)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundle.type\_of\_transaction equals “Outward” → bundle.warehouse equals bundle\_rows at 0.get(warehouse\_field).
    - Continue with the next iteration or loop test.
  - Set bundle from Platform.get\_doc(“Serial and Batch Bundle”, bundle.name).
  - Set slices from \_slice\_entries(bundle.entries, qtys, precision).
  - For each tuple(idx, tuple(row, share)) in enumerate(zip(bundle\_rows, slices, strict = true)).
    - If not share.
      - Set row.serial\_and\_batch\_bundle from empty text.
      - Continue with the next iteration or loop test.
    - Set doc from bundle when (idx equals 0 and keep\_original), otherwise Platform.copy\_doc(bundle, ignore\_no\_copy = false).
      - Value choice on (idx equals 0 and keep\_original) — true gives bundle, false gives Platform.copy\_doc(bundle, ignore\_no\_copy = false).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in idx equals 0 → keep\_original.
    - Evaluate doc.set(“entries”, list()).
    - For each entry in share.
      - Evaluate doc.append(“entries”, entry).
    - If doc.type\_of\_transaction equals “Inward”.
      - Set doc.warehouse from row.get(warehouse\_field).
    - Evaluate doc.save().
    - Set row.serial\_and\_batch\_bundle from doc.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1044) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L541)

<a id="op-3b9ba0618cf886"></a>
### Slice entries

`operation_enterprise_binding_enterprise_stock_doctype_putaway_rule_putaway_rule_slice_entries`

**Inputs** entries, qtys, precision.

**Explicit results** slices.

**Local steps**

- Set slices from list().
- Set tuple(idx, left) from tuple(0, 0.0).
- For each qty in qtys.
  - Set tuple(share, need) from tuple(list(), flt(qty, precision)).
  - While (need &gt; 0 and idx &lt; len(entries)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in need &gt; 0 → idx &lt; len(entries).
    - Set entry from entries at idx.
    - If not left.
      - Set left from abs(flt(entry.qty)).
    - Set take from min(left, need).
    - Set row from entry.as\_dict(no\_default\_fields = true).
    - Set row at “qty” from take.
    - Evaluate share.append(row).
    - Set left from flt((left − take), precision).
    - Set need from flt((need − take), precision).
    - If not left.
      - Update idx using + 1.
  - Evaluate slices.append(share).
- Return slices.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1043) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L540)

<a id="op-b0e3194b72898d"></a>
### Show unassigned items message

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_show_unassigned_items_message`

**Inputs** items\_not\_accomodated.

**State and service calls** msgprint with msg.

**Local steps**

- Set msg from (translated “The following Items, having Putaway Rules, could not be accomodated:” + text in the contract).
- Set formatted\_item\_rows from empty text.
- For each entry in items\_not\_accomodated.
  - Set item\_link from Platform.utils.get\_link\_to\_form(“Item”, entry at 0).
  - Update formatted\_item\_rows using + formatted text   &lt;td&gt;{item\_link}&lt;/td&gt;  &lt;td&gt;{Platform.bold(entry at 1)}&lt;/td&gt;  &lt;/tr&gt;.
- Update msg using + multiline text in the contract.format(translated “Item”, translated “Unassigned Qty”, formatted\_item\_rows).
- Evaluate Platform.msgprint(msg, title = translated “Insufficient Capacity”, is\_minimizable = true, wide = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L353)

<a id="op-bc17b337dc549d"></a>
### Get serial nos to allocate

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_get_serial_numbers_to_allocate`

**Inputs** serial\_nos, to\_allocate.

**Explicit results** whitespace '\\n'.join(allocated\_serial\_nos) when allocated\_serial\_nos, otherwise empty text · empty text.

**Local steps**

- If serial\_nos.
  - Set allocated\_serial\_nos from serial\_nos at slice 0 to cint(to\_allocate).
  - Set serial\_nos at slice no value to no value from serial\_nos at slice cint(to\_allocate) to no value.
  - Return whitespace '\\n'.join(allocated\_serial\_nos) when allocated\_serial\_nos, otherwise empty text.
    - Value choice on allocated\_serial\_nos — true gives whitespace '\\n'.join(allocated\_serial\_nos), false gives empty text.
- Otherwise.
  - Return empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0794.json#L4705) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L345)

## Record · Quality inspection

[Record definition](../../../../data/record-types/quality_inspection.json)

<a id="op-f0aab739dcf14c"></a>
### Quality Inspection.on discard

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.update\_qc\_reference().
- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update qc reference](operations-049.md#op-dad77e12780ee7).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L774) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L384)

<a id="op-5c9b86833fa94b"></a>
### Quality Inspection.validate

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_validate`

**Inputs** self.

**Local steps**

- If (not self.readings and self.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.readings → self.item\_code.
  - Evaluate self.get\_item\_specification\_details().
- If (self.inspection\_type equals “In Process” and self.reference\_type equals “Job Card”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.inspection\_type equals “In Process” → self.reference\_type equals “Job Card”.
  - Evaluate self.set\_acceptance\_criteria\_from\_template().
- If self.readings.
  - Evaluate self.validate\_reading\_number\_format().
  - Evaluate self.inspect\_and\_set\_status().
- Evaluate self.validate\_inspection\_required().
- Evaluate self.validate\_status().
- Evaluate self.set\_child\_row\_reference().
- Evaluate self.set\_company().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item specification details](operations-048.md#op-34b397930a8281), [set acceptance criteria from template](operations-048.md#op-72bb61dc844dd2), [validate reading number format](operations-049.md#op-b8b540637b929f), [inspect and set status](operations-049.md#op-8f21c2670696d7), [validate inspection required](operations-048.md#op-95853a73a84b62), [validate status](operations-048.md#op-1f379fa2cebecf), [set child row reference](operations-048.md#op-7de0a5927ea369), [set company](operations-048.md#op-05dce2f5d234d9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L394)

<a id="op-72bb61dc844dd2"></a>
### Quality Inspection.set acceptance criteria from template

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_qualityinspection_set_acceptance_criteria_from_template`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Local steps**

- Set template from (self.quality\_inspection\_template or Platform.db.get\_value(“Item”, self.item\_code, “quality\_inspection\_template”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.quality\_inspection\_template → Platform.db.get\_value(“Item”, self.item\_code, “quality\_inspection\_template”).
- Set parameters from mapping of d.specification → d for d drawn from get\_template\_details(template).
  - Draw d from get\_template\_details(template).
- For each reading in self.readings.
  - If criteria bound to parameters.get(reading.specification).
    - Evaluate reading.update(criteria).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1048) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L545)

<a id="op-1f379fa2cebecf"></a>
### Quality Inspection.validate status

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_qualityinspection_validate_status`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Status Cancelled can only be set by cancelling the Quality Inspection”.

**Local steps**

- If (self.status equals “Cancelled” and self.docstatus &lt; 2).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Cancelled” → self.docstatus &lt; 2.
  - Call the validation error handler Platform.throw(translated “Status Cancelled can only be set by cancelling the Quality Inspection”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1051) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L548)

<a id="op-05dce2f5d234d9"></a>
### Quality Inspection.set company

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_set_company`

**Inputs** self.

**Record and data access** read self.reference\_type via get\_cached\_value.

**Local steps**

- If (self.reference\_type and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type → self.reference\_name.
  - Set company from Platform.get\_cached\_value(self.reference\_type, self.reference\_name, “company”).
  - If company differs from self.company.
    - Set self.company from company.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(self.reference\_type, self.reference\_name, “company”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L1299) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L390)

<a id="op-7de0a5927ea369"></a>
### Quality Inspection.set child row reference

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_set_child_row_reference`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Every row of Item {0} in {1} {2} already has a Quality Inspection”.format(Platform.bold(self.item\_code), translated self.reference\_type, Platform.bold(self.reference\_name)).

**Local steps**

- If self.child\_row\_reference.
  - Return no value.
- If not (self.reference\_type and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type → self.reference\_name.
  - Return no value.
- Set doctype from (self.reference\_type + “ Item”).
- If self.reference\_type equals “Stock Entry”.
  - Set doctype from “Stock Entry Detail”.
- Set child\_doc from Platform.qb.DocType(doctype).
- Set qi\_doc from Platform.qb.DocType(“Quality Inspection”).
- Set query from nested operand in the contract(nested operand in the contract).select(child\_doc.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contrac ….
- If (self.batch\_no and Platform.get\_meta(doctype).has\_field(“batch\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.batch\_no → Platform.get\_meta(doctype).has\_field(“batch\_no”).
  - Set query from query.where(child\_doc.batch\_no equals self.batch\_no).
- If child\_row\_references bound to query.run(pluck = true).
  - Set self.child\_row\_reference from child\_row\_references at 0.
- Otherwise.
  - If (Platform.get\_meta(doctype).has\_field(“quality\_inspection”) and self.has\_inspected\_rows(doctype)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_meta(doctype).has\_field(“quality\_inspection”) → self.has\_inspected\_rows(doctype).
    - Call the validation error handler Platform.throw(translated “Every row of Item {0} in {1} {2} already has a Quality Inspection”.format(Platform.bold(self.item\_code), translated self.reference\_type, Platform.bold(self.reference\_name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has inspected rows](operations-048.md#op-fd2807eb4c8246).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L389)

<a id="op-fd2807eb4c8246"></a>
### Quality Inspection.has inspected rows

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_qualityinspection_has_inspected_rows`

**Inputs** self, doctype.

**Record and data access** read doctype via exists.

**Explicit results** Platform.db.exists(doctype, mapping(“parent” → self.reference\_name, “item\_code” → self.item\_code, “quality\_inspection” → tuple(“not in”, list(empty text, self.name)))).

**Local steps**

- Return Platform.db.exists(doctype, mapping(“parent” → self.reference\_name, “item\_code” → self.item\_code, “quality\_inspection” → tuple(“not in”, list(empty text, self.name)))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1046) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L543)

<a id="op-95853a73a84b62"></a>
### Quality Inspection.validate inspection required

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_validate_inspection_required`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Item” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “'Inspection Required before Purchase' has disabled for the item {0}, no need to create the QI”.format(get\_link\_to\_form(“Item”, self.item\_code)) · validation helper — translated “'Inspection Required before Delivery' has disabled for the item {0}, no need to create the QI”.format(get\_link\_to\_form(“Item”, self.item\_code)).

**Local steps**

- If Platform.db.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).
  - Return no value.
- If (self.reference\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) and not Platform.get\_cached\_value(“Item”, self.item\_code, “inspection\_required\_before\_purchase”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) → not Platform.get\_cached\_value(“Item”, self.item\_code, “inspection\_required\_before\_purchase”).
  - Call the validation error handler Platform.throw(translated “'Inspection Required before Purchase' has disabled for the item {0}, no need to create the QI”.format(get\_link\_to\_form(“Item”, self.item\_code))).
- If (self.reference\_type belongs to list(“Delivery Note”, “Sales Invoice”) and not Platform.get\_cached\_value(“Item”, self.item\_code, “inspection\_required\_before\_delivery”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type belongs to list(“Delivery Note”, “Sales Invoice”) → not Platform.get\_cached\_value(“Item”, self.item\_code, “inspection\_required\_before\_delivery”).
  - Call the validation error handler Platform.throw(translated “'Inspection Required before Delivery' has disabled for the item {0}, no need to create the QI”.format(get\_link\_to\_form(“Item”, self.item\_code))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”), Platform.get\_cached\_value(“Item”, self.item\_code, “inspection\_required\_before\_purchase”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L395)

<a id="op-a47276527c7067"></a>
### Quality Inspection.before submit

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_sample\_size().
- Evaluate self.validate\_readings\_status\_mandatory().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate sample size](operations-048.md#op-1ac548336646a3), [validate readings status mandatory](operations-049.md#op-08ece159940489).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L376)

<a id="op-1ac548336646a3"></a>
### Quality Inspection.validate sample size

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_qualityinspection_validate_sample_size`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Sample Size must be greater than zero”.

**Local steps**

- If flt(self.sample\_size) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Sample Size must be greater than zero”, title = translated “Invalid Sample Size”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1050) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L547)

<a id="op-34b397930a8281"></a>
### Quality Inspection.get item specification details

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_get_item_specification_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_value · read “Quality Inspection Parameter” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.quality\_inspection\_template.
  - Set self.quality\_inspection\_template from Platform.db.get\_value(“Item”, self.item\_code, “quality\_inspection\_template”).
- If not self.quality\_inspection\_template.
  - Return no value.
- Evaluate self.set(“readings”, list()).
- Set parameters from get\_template\_details(self.quality\_inspection\_template).
- For each d in parameters.
  - Set child from self.append(“readings”, mapping()).
  - Evaluate child.update(d).
  - Set child.status from “Accepted”.
  - Set child.parameter\_group from Platform.get\_value(“Quality Inspection Parameter”, d.specification, “parameter\_group”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L2483) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L379)

<a id="op-8fcd2739476c66"></a>
### Quality Inspection.get quality inspection template

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_get_quality_inspection_template`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “BOM” via get\_value.

**Local steps**

- Set template from empty text.
- If self.bom\_no.
  - Set template from Platform.db.get\_value(“BOM”, self.bom\_no, “quality\_inspection\_template”).
- If not template.
  - Set template from Platform.db.get\_value(“BOM”, self.item\_code, “quality\_inspection\_template”).
- Set self.quality\_inspection\_template from template.
- Evaluate self.get\_item\_specification\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item specification details](operations-048.md#op-34b397930a8281).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L2847) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L380)

<a id="op-d7fcffabb99234"></a>
### Quality Inspection.on update

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_on_update`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- Set action\_if\_qi\_in\_draft from Platform.db.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_not\_submitted”).
- If (not action\_if\_qi\_in\_draft or action\_if\_qi\_in\_draft equals “Warn”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not action\_if\_qi\_in\_draft → action\_if\_qi\_in\_draft equals “Warn”.
  - Evaluate self.update\_qc\_reference().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update qc reference](operations-049.md#op-dad77e12780ee7).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_not\_submitted”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L3084) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L387)

<a id="op-a960d9cc0f563d"></a>
### Quality Inspection.on submit

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_on_submit`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If Platform.db.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_not\_submitted”) equals “Stop”.
  - Evaluate self.update\_qc\_reference().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update qc reference](operations-049.md#op-dad77e12780ee7).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_not\_submitted”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L3219) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L385)

<a id="op-055bd2c87d75cb"></a>
### Quality Inspection.before cancel

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_qualityinspection_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_not\_used\_by\_submitted\_document().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate not used by submitted document](operations-048.md#op-2578fa995c5781).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1045) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L542)

<a id="op-2578fa995c5781"></a>
### Quality Inspection.validate not used by submitted document

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_qualityinspection_validate_not_used_by_submitted_document`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read self.reference\_type via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Quality Inspection {0} is used by {1} {2}. Cancel {2} first.”.format(Platform.bold(self.name), translated self.reference\_type, get\_link\_to\_form(self.reference\_type, self.reference\_name)).

**Local steps**

- If (not (self.reference\_type and self.reference\_name) or Platform.db.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (self.reference\_type and self.reference\_name) → Platform.db.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type → self.reference\_name.
  - Return no value.
- If Platform.db.get\_value(self.reference\_type, self.reference\_name, “docstatus”) differs from 1.
  - Return no value.
- If self.is\_linked\_on\_reference().
  - Call the validation error handler Platform.throw(translated “Quality Inspection {0} is used by {1} {2}. Cancel {2} first.”.format(Platform.bold(self.name), translated self.reference\_type, get\_link\_to\_form(self.reference\_type, self.reference\_name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is linked on reference](operations-048.md#op-3606e760e3f0db).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1049) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L546)

<a id="op-3606e760e3f0db"></a>
### Quality Inspection.is linked on reference

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_qualityinspection_is_linked_on_reference`

**Inputs** self.

**Record and data access** read “Job Card” via get\_value · read doctype via exists.

**Explicit results** Platform.db.get\_value(“Job Card”, self.reference\_name, “quality\_inspection”) equals self.name · Platform.db.exists(doctype, mapping(“parent” → self.reference\_name, “quality\_inspection” → self.name)).

**Local steps**

- If self.reference\_type equals “Job Card”.
  - Return Platform.db.get\_value(“Job Card”, self.reference\_name, “quality\_inspection”) equals self.name.
- Set doctype from “Stock Entry Detail” when self.reference\_type equals “Stock Entry”, otherwise (self.reference\_type + “ Item”).
  - Value choice on self.reference\_type equals “Stock Entry” — true gives “Stock Entry Detail”, false gives (self.reference\_type + “ Item”).
- Return Platform.db.exists(doctype, mapping(“parent” → self.reference\_name, “quality\_inspection” → self.name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1047) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L544)
