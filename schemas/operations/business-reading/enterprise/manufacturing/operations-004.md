# Production · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom

<a id="op-c4372c2b24970d"></a>
### BOM.update cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_update_cost`

**Inputs** self, update\_parent = true, from\_child\_bom = false, update\_hour\_rate = true, save = true.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If (cint(save) and not self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(save) → not self.is\_new().
  - Evaluate self.load\_from\_db().
  - Evaluate self.check\_permission(“write”).
- Evaluate self.\_update\_cost(update\_parent = (cint(update\_parent) and cint(save)), from\_child\_bom = from\_child\_bom, update\_hour\_rate = update\_hour\_rate, save = cint(save)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(update\_parent) → cint(save).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update cost](operations-004.md#op-e42139ecb39eb0).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L201)

<a id="op-e42139ecb39eb0"></a>
### BOM.update cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_update_cost`

**Inputs** self, update\_parent = true, from\_child\_bom = false, update\_hour\_rate = true, save = true.

**State and service calls** call db\_update on self · msgprint with translated msg.

**Explicit results** no value.

**Local steps**

- <a id="op-e42139ecb39eb0-guard-2"></a>If self.docstatus equals 2.
  - Return no value.
- Set self.flags.cost\_updated from false.
- Set existing\_bom\_cost from self.total\_cost.
- <a id="op-e42139ecb39eb0-guard-8"></a>If self.docstatus equals 1.
  - Set self.flags.ignore\_validate\_update\_after\_submit from true.
- Evaluate self.set\_plc\_conversion\_rate().
- Evaluate self.calculate\_cost(save\_updates = save, update\_hour\_rate = update\_hour\_rate).
- If save.
  - Evaluate self.db\_update().
- If (self.total\_cost differs from existing\_bom\_cost and update\_parent).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.total\_cost differs from existing\_bom\_cost → update\_parent.
  - Evaluate self.update\_parent\_boms().
- If not from\_child\_bom.
  - Set msg from “Cost Updated”.
  - If not self.flags.cost\_updated.
    - Set msg from “No changes in cost found”.
  - Evaluate Platform.msgprint(translated msg, alert = true).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 2, self.docstatus = 2 (cancelled) selects the branch that returns no value. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e42139ecb39eb0-guard-2)
- At the comparison self.docstatus equals 1, self.docstatus = 1 (submitted) selects the branch that assigns true to self.flags.ignore\_validate\_update\_after\_submit. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e42139ecb39eb0-guard-8)

**Methods declared on this owner** [set plc conversion rate](operations-004.md#op-afcec7fccd031c), [calculate cost](operations-005.md#op-0154f61889ef02), [update parent boms](operations-004.md#op-7ecaeacf8f5029).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L640)

<a id="op-7ecaeacf8f5029"></a>
### BOM.update parent boms

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_update_parent_boms`

**Inputs** self.

**Record and data access** resolve a document from “BOM” via get\_doc.

**Local steps**

- Set bom\_item from Platform.qb.DocType(“BOM Item”).
- Set parent\_boms from nested operand in the contract(nested operand in the contract).distinct().where(((nested operand in the contract.bom\_no equals nested operand in the contract.name bitwise and nested operand in the contract ….
- For each bom in parent\_boms.
  - Evaluate Platform.get\_doc(“BOM”, bom).\_update\_cost(from\_child\_bom = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L641)

<a id="op-e7e3d166e2a1cc"></a>
### BOM.update parent cost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_update_parent_cost`

**Inputs** self.

**Local steps**

- If self.total\_cost.
  - Set cost from (self.total\_cost ÷ get\_good\_qty(self)).
  - Set bom\_item from Platform.qb.DocType(“BOM Item”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(bom\_item.amount, (nested operand in the contract.stock\_qty × cost)).where(((nested operand in the contract ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L203)

<a id="op-324e71b1370efc"></a>
### BOM.get bom unitcost

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_bill_of_materials_unitcost`

**Inputs** self, bom\_no.

**Explicit results** (flt(bom at 0.base\_total\_cost) ÷ get\_good\_qty(bom at 0)) when bom, otherwise 0.

**Local steps**

- Set bom\_table from Platform.qb.DocType(“BOM”).
- Set bom from nested operand in the contract(nested operand in the contract).select(bom\_table.base\_total\_cost, bom\_table.quantity, bom\_table.process\_loss\_qty).where((bom\_table.is\_active equals 1 bitwise and bom\_table.na ….
- Return (flt(bom at 0.base\_total\_cost) ÷ get\_good\_qty(bom at 0)) when bom, otherwise 0.
  - Value choice on bom — true gives (flt(bom at 0.base\_total\_cost) ÷ get\_good\_qty(bom at 0)), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L162)

<a id="op-5718f55d3fd761"></a>
### BOM.manage default bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_manage_default_bill_of_materials`

**Inputs** self.

**Record and data access** resolve a document from “Item” via get\_doc · read dict(doctype = “BOM”, docstatus = 1, item = self.item, is\_default = 1) via exists.

**State and service calls** request set\_value on “Item” · call db\_set on self.

**Local steps**

- If (self.is\_default and self.is\_active).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_default → self.is\_active.
  - Bind dependencies set\_default.
  - Evaluate set\_default(self, “item”).
  - Set item from Platform.get\_doc(“Item”, self.item).
  - If item.default\_bom differs from self.name.
    - Evaluate Platform.db.set\_value(“Item”, self.item, “default\_bom”, self.name).
- Otherwise.
  - If (not Platform.db.exists(dict(doctype = “BOM”, docstatus = 1, item = self.item, is\_default = 1)) and self.is\_active).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.exists(dict(doctype = “BOM”, docstatus = 1, item = self.item, is\_default = 1)) → self.is\_active.
    - Evaluate self.db\_set(“is\_default”, 1).
    - Evaluate Platform.db.set\_value(“Item”, self.item, “default\_bom”, self.name).
  - Otherwise.
    - Evaluate self.\_unset\_default\_bom().

If control reaches the end, it returns no value.

**Methods declared on this owner** [unset default bom](operations-004.md#op-1a2ad89989b9bb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L176)

<a id="op-1a2ad89989b9bb"></a>
### BOM.unset default bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_unset_default_bill_of_materials`

**Inputs** self.

**Record and data access** read “Item” via get\_value · read “BOM” via get\_value.

**State and service calls** call db\_set on self · request set\_value on “BOM” · request set\_value on “Item”.

**Explicit results** no value.

**Local steps**

- Evaluate self.db\_set(“is\_default”, 0).
- If Platform.db.get\_value(“Item”, self.item, “default\_bom”) differs from self.name.
  - Return no value.
- Set next\_default from Platform.db.get\_value(“BOM”, mapping(“item” → self.item, “docstatus” → 1, “is\_active” → 1, “name” → tuple(“!=”, self.name)), “name”, order\_by = “creation desc”).
- If next\_default.
  - Evaluate Platform.db.set\_value(“BOM”, next\_default, “is\_default”, 1).
- Evaluate Platform.db.set\_value(“Item”, self.item, “default\_bom”, next\_default).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L199)

<a id="op-138e1223070aba"></a>
### BOM.clear operations

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_clear_operations`

**Inputs** self.

**Local steps**

- If not self.with\_operations.
  - Evaluate self.set(“operations”, list()).
- If (not self.with\_operations and self.track\_semi\_finished\_goods).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.with\_operations → self.track\_semi\_finished\_goods.
  - Set self.track\_semi\_finished\_goods from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L397) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L159)

<a id="op-c1abbe469b9d82"></a>
### BOM.clear inspection

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_clear_inspection`

**Inputs** self.

**Local steps**

- If not self.inspection\_required.
  - Set self.quality\_inspection\_template from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L527) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L158)

<a id="op-6d1e90684e9adc"></a>
### BOM.validate main item

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_main_item`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Item {0} does not exist in the system or has expired”.format(self.item) · validation helper — translated “Quantity should be greater than 0”.

**Local steps**

- Set item from self.get\_item\_det(self.item).
- If not item.
  - Call the validation error handler Platform.throw(translated “Item {0} does not exist in the system or has expired”.format(self.item)).
- Otherwise.
  - Set ret from Platform.db.get\_value(“Item”, self.item, list(“description”, “stock\_uom”, “item\_name”)).
  - Set self.description from ret at 0.
  - Set self.uom from ret at 1.
  - Set self.item\_name from ret at 2.
- If not self.quantity.
  - Call the validation error handler Platform.throw(translated “Quantity should be greater than 0”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item det](operations-003.md#op-66c87353b2ffd8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L591) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L210)

<a id="op-ff60beef71204c"></a>
### BOM.validate currency

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_currency`

**Inputs** self.

**Record and data access** read “Price List” via get\_value.

**Explicit failure paths** validation helper — translated “Currency of the price list {0} must be {1} or {2}”.format(self.buying\_price\_list, self.currency, self.company\_currency()).

**Local steps**

- If self.rm\_cost\_as\_per equals “Price List”.
  - Set price\_list\_currency from Platform.db.get\_value(“Price List”, self.buying\_price\_list, “currency”).
  - If price\_list\_currency does not belong to tuple(self.currency, self.company\_currency()).
    - Call the validation error handler Platform.throw(translated “Currency of the price list {0} must be {1} or {2}”.format(self.buying\_price\_list, self.currency, self.company\_currency())).

If control reaches the end, it returns no value.

**Methods declared on this owner** [company currency](operations-005.md#op-748c84316a0566).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L2472) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L209)

<a id="op-ff59a363479ac1"></a>
### BOM.update stock qty

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_update_stock_quantity`

**Inputs** self.

**Local steps**

- For each m in (self.get(“items”) + self.get(“secondary\_items”)).
  - If not m.conversion\_factor.
    - Set m.conversion\_factor from flt(get\_conversion\_factor(m.item\_code, m.uom) at “conversion\_factor”).
  - If (m.uom and m.qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in m.uom → m.qty.
    - Set m.stock\_qty from (flt(m.conversion\_factor) × flt(m.qty)).
  - If (not m.uom and m.stock\_uom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not m.uom → m.stock\_uom.
    - Set m.uom from m.stock\_uom.
    - Set m.qty from m.stock\_qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L2723) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L205)

<a id="op-cdb478fec9f2da"></a>
### BOM.validate uom is interger

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_unit_of_measure_is_interger`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_uom\_is\_integer.
- Evaluate validate\_uom\_is\_integer(self, “uom”, “qty”, “BOM Item”).
- Evaluate validate\_uom\_is\_integer(self, “stock\_uom”, “stock\_qty”, “BOM Item”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L3079) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L219)

<a id="op-2ea08a92d23a47"></a>
### BOM.set conversion rate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_conversion_rate`

**Inputs** self.

**Local steps**

- If self.currency equals self.company\_currency().
  - Set self.conversion\_rate from 1.
- Otherwise.
  - If (self.conversion\_rate equals 1 or flt(self.conversion\_rate) ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.conversion\_rate equals 1 → flt(self.conversion\_rate) ≤ 0.
    - Set self.conversion\_rate from get\_exchange\_rate(self.currency, self.company\_currency(), args = “for\_buying”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [company currency](operations-005.md#op-748c84316a0566).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L3211) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L183)

<a id="op-afcec7fccd031c"></a>
### BOM.set plc conversion rate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_plc_conversion_rate`

**Inputs** self.

**Record and data access** read “Price List” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- <a id="op-afcec7fccd031c-guard-2"></a>If self.rm\_cost\_as\_per belongs to list(“Valuation Rate”, “Last Purchase Rate”).
  - Set self.plc\_conversion\_rate from 1.
  - Return no value.
- If self.buying\_price\_list.
  - Set self.price\_list\_currency from Platform.get\_cached\_value(“Price List”, self.buying\_price\_list, “currency”).
- If not self.price\_list\_currency.
  - Return no value.
- If self.price\_list\_currency equals self.company\_currency().
  - Set self.plc\_conversion\_rate from 1.
- Otherwise.
  - If (flt(self.plc\_conversion\_rate) belongs to tuple(0, 1) or self.has\_value\_changed(“buying\_price\_list”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.plc\_conversion\_rate) belongs to tuple(0, 1) → self.has\_value\_changed(“buying\_price\_list”).
    - Set self.plc\_conversion\_rate from get\_exchange\_rate(self.price\_list\_currency, self.company\_currency(), args = “for\_buying”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.rm\_cost\_as\_per belongs to list(“Valuation Rate”, “Last Purchase Rate”), self.rm\_cost\_as\_per = “Valuation Rate” selects the branch that assigns 1 to self.plc\_conversion\_rate. With self.rm\_cost\_as\_per = “Price List”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-afcec7fccd031c-guard-2)

**Methods declared on this owner** [company currency](operations-005.md#op-748c84316a0566).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, self.buying\_price\_list, “currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L189)

<a id="op-09224d1a506b48"></a>
### BOM.validate materials

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_materials`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Explicit failure paths** validation helper — translated “Raw Materials cannot be blank.” · validation helper — translated “Quantity required for Item {0} in row {1}”.format(m.item\_code, m.idx) · validation helper — translated “Fixed Asset item {0} cannot be used in BOMs.”.format(“, ”.join(generator of get\_link\_to\_form(“Item”, item) for item drawn from fixed\_asset\_items)) · validation helper — translated “Disabled Item {0} cannot be used in BOMs.”.format(“, ”.join(generator of get\_link\_to\_form(“Item”, item) for item drawn from disabled\_items)).

**Local steps**

- If not self.get(“items”).
  - Call the validation error handler Platform.throw(translated “Raw Materials cannot be blank.”).
- Set check\_list from list().
- Set items from list().
- For each m in self.get(“items”).
  - If m.bom\_no.
    - Evaluate validate\_production\_bom(m.item\_code, m.bom\_no).
  - If flt(m.qty) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Quantity required for Item {0} in row {1}”.format(m.item\_code, m.idx)).
  - Evaluate check\_list.append(m).
  - Evaluate items.append(m.item\_code).
- If fixed\_asset\_items bound to Platform.db.get\_all(“Item”, filters = mapping(“item\_code” → tuple(“in”, items), “is\_fixed\_asset” → 1), pluck = “name”).
  - Call the validation error handler Platform.throw(translated “Fixed Asset item {0} cannot be used in BOMs.”.format(“, ”.join(generator of get\_link\_to\_form(“Item”, item) for item drawn from fixed\_asset\_items))).
    - Draw item from fixed\_asset\_items.
- Set bom\_items from set(self.item, expanded items).
- Evaluate bom\_items.update(generator of d.item\_code for d drawn from self.get(“secondary\_items”)).
  - Draw d from self.get(“secondary\_items”).
- Evaluate bom\_items.update(generator of d.finished\_good for d drawn from self.get(“operations”) where d.finished\_good).
  - Draw d from self.get(“operations”), keep a combination only if (d.finished\_good).
- If disabled\_items bound to Platform.db.get\_all(“Item”, filters = mapping(“item\_code” → tuple(“in”, list(bom\_items)), “disabled” → 1), pluck = “name”).
  - Call the validation error handler Platform.throw(translated “Disabled Item {0} cannot be used in BOMs.”.format(“, ”.join(generator of get\_link\_to\_form(“Item”, item) for item drawn from disabled\_items))).
    - Draw item from disabled\_items.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L211)

<a id="op-fe77e8cf67c8fa"></a>
### BOM.check recursion

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_check_recursion`

**Inputs** self, bom\_list = no value.

**Record and data access** read “BOM Item” via get\_all.

**Local steps**

- Bind local operation \_throw\_error for subsequent calls.
- Set bom\_list from self.traverse\_tree().
- Set child\_items from Platform.get\_all(“BOM Item”, fields = list(“bom\_no”, “item\_code”), filters = mapping(“parent” → tuple(“in”, bom\_list), “parenttype” → “BOM”)).
- For each item in child\_items.
  - If self.name equals item.bom\_no.
    - Evaluate \_throw\_error(self.name).
  - If (self.item equals item.item\_code and item.bom\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item equals item.item\_code → item.bom\_no.
    - Evaluate \_throw\_error(item.bom\_no, self.item).
- If self.name belongs to set of d.bom\_no for d drawn from self.items.
  - Draw d from self.items.
  - Evaluate \_throw\_error(self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [traverse tree](operations-005.md#op-df25f2b27230a6).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L157)

<a id="op-82af84c779cfe5"></a>
### BOM.check recursion.throw error

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_check_recursion_throw_error`

**Inputs** bom\_name, production\_item = no value.

**Explicit failure paths** validation helper with BOMRecursionError — msg.

**Local steps**

- Set msg from translated “BOM recursion: {1} cannot be parent or child of {0}”.format(self.name, bom\_name).
- If (production\_item and bom\_name differs from self.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in production\_item → bom\_name differs from self.name.
  - Update msg using + text in the contract.
  - Update msg using + translated “Note: If you want to use the finished good {0} as a raw material, then enable the 'Do Not Explode' checkbox  …”.format(bold(production\_item)).
- Call the validation error handler Platform.throw(msg, exc = BOMRecursionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L627)

<a id="op-6bdcb38e2bc9e4"></a>
### BOM.set materials based on operation bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_materials_based_on_operation_bill_of_materials`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.track\_semi\_finished\_goods.
  - Return no value.
- For each row in self.get(“operations”).
  - If (row.bom\_no and row.finished\_good).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.bom\_no → row.finished\_good.
    - Evaluate self.add\_materials\_from\_bom(row.finished\_good, row.bom\_no, row.idx, qty = row.finished\_good\_qty, replace = self.operation\_bom\_changed(row)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add materials from bom](operations-005.md#op-3e99612fb18c1b), [operation bom changed](operations-004.md#op-04f2a9d157a811).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L186)

<a id="op-04f2a9d157a811"></a>
### BOM.operation bom changed

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_operation_bom_changed`

**Inputs** self, row.

**Explicit results** false · get\_step\_material\_names(doc\_before\_save, old\_row.idx) equals get\_step\_material\_names(self, row.idx).

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return false.
- Set old\_row from next(generator of d for d drawn from doc\_before\_save.operations where d.name equals row.name, no value).
  - Draw d from doc\_before\_save.operations, keep a combination only if (d.name equals row.name).
- If (not old\_row or old\_row.bom\_no equals row.bom\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not old\_row → old\_row.bom\_no equals row.bom\_no.
  - Return false.
- Return get\_step\_material\_names(doc\_before\_save, old\_row.idx) equals get\_step\_material\_names(self, row.idx).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L632)

<a id="op-0db60429d9e112"></a>
### BOM.remove operation materials

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_remove_operation_materials`

**Inputs** self, operation\_row\_id.

**Local steps**

- Evaluate self.set(“items”, list of row for row drawn from self.items where cint(row.operation\_row\_id) differs from cint(operation\_row\_id)).
  - Draw row from self.items, keep a combination only if (cint(row.operation\_row\_id) differs from cint(operation\_row\_id)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L634)

<a id="op-8aeaf788bab9d2"></a>
### BOM.add raw materials

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_add_raw_materials`

**Inputs** self, operation\_row\_id, items.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**State and service calls** call save on self.

**Local steps**

- If isinstance(items, str).
  - Set items from parse\_json(items).
- For each row in items.
  - Set row from parse\_json(row).
  - Evaluate row.update(\_get\_item\_details(row.get(“item\_code”))).
  - Set row.operation\_row\_id from operation\_row\_id.
  - Set item\_row from self.get\_item\_data(row.item\_code, operation\_row\_id).
  - If item\_row.
    - Set item\_row.qty from row.get(“qty”).
  - Otherwise.
    - Set row.idx from no value.
    - Set row.name from no value.
    - Set row.do\_not\_explode from 1.
    - Set row.is\_sub\_assembly\_item from self.is\_sub\_assembly\_item(row.item\_code).
    - Evaluate self.append(“items”, row).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item data](operations-004.md#op-bd38a4a6409e13), [is sub assembly item](operations-004.md#op-a172e82f9b8289).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L148)

<a id="op-a172e82f9b8289"></a>
### BOM.is sub assembly item

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_is_subordinate_assembly_item`

**Inputs** self, item\_code.

**Explicit results** false · true.

**Local steps**

- If not self.operations.
  - Return false.
- For each row in self.operations.
  - If row.finished\_good equals item\_code.
    - Return true.
- Return false.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L5685) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L175)

<a id="op-bd38a4a6409e13"></a>
### BOM.get item data

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_item_data`

**Inputs** self, item\_code, operation\_row\_id.

**Explicit results** row.

**Local steps**

- For each row in self.items.
  - If (row.item\_code equals item\_code and cint(row.operation\_row\_id) equals cint(operation\_row\_id)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code equals item\_code → cint(row.operation\_row\_id) equals cint(operation\_row\_id).
    - Return row.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0456.json#L5806) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L167)
