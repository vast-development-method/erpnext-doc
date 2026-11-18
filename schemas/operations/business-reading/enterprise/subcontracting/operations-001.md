# Subcontracting · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Subcontracted items to be delivered

<a id="op-0e64a6a0989951"></a>
### Execute

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_items_to_be_delivered_subcontracted_items_to_be_delivered_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data(filters)).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return tuple(get\_columns(), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1234)

<a id="op-7efef01a250f9d"></a>
### Get data

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_items_to_be_delivered_subcontracted_items_to_be_delivered_get_data`

**Inputs** filters.

**Explicit results** list of row for row drawn from rows where row.pending\_qty &gt; 0.

**Local steps**

- Set rows from get\_open\_inward\_order\_rows(filters, “items”, list(“item\_code”, “item\_name”, “stock\_uom”, “qty”, …), list()).
- Set precision from Platform.get\_precision(“Subcontracting Inward Order Item”, “qty”).
- For each row in rows.
  - Set row.pending\_qty from flt((row.qty − row.delivered\_qty), precision).
- Return list of row for row drawn from rows where row.pending\_qty &gt; 0.
  - Draw row from rows, keep a combination only if (row.pending\_qty &gt; 0).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1236)

<a id="op-6b7fdff1c126b1"></a>
### Get columns

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_items_to_be_delivered_subcontracted_items_to_be_delivered_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(expanded get\_inward\_order\_columns(), mapping(“label” → translated “Finished Good”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “f ….

**Local steps**

- Return list(expanded get\_inward\_order\_columns(), mapping(“label” → translated “Finished Good”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “f ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1235)

## Report · Subcontracted raw materials to be received

<a id="op-07d066dd741325"></a>
### Execute

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_raw_materials_to_be_received_subcontracted_raw_materials_to_be_received_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data(filters)).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return tuple(get\_columns(), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1237)

<a id="op-71517e4d552319"></a>
### Get data

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_raw_materials_to_be_received_subcontracted_raw_materials_to_be_received_get_data`

**Inputs** filters.

**Explicit results** list of row for row drawn from rows where row.pending\_qty &gt; 0.

**Local steps**

- Set rows from get\_open\_inward\_order\_rows(filters, “received\_items”, list(“reference\_name”, “main\_item\_code”, “rm\_item\_code”, “stock\_uom”, …), list(list(“per\_produced”, “&lt;”, 100), list(“Subcontracting Inward Order Receiv ….
- Evaluate set\_pending\_qty(rows).
- Return list of row for row drawn from rows where row.pending\_qty &gt; 0.
  - Draw row from rows, keep a combination only if (row.pending\_qty &gt; 0).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1239)

<a id="op-3527a673f3ce83"></a>
### Set pending qty

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_raw_materials_to_be_received_subcontracted_raw_materials_to_be_received_set_pending_qty`

**Inputs** rows.

**Local steps**

- Set finished\_goods from get\_finished\_goods(set of row.reference\_name for row drawn from rows).
  - Draw row from rows.
- Set precision from Platform.get\_precision(“Subcontracting Inward Order Received Item”, “required\_qty”).
- For each row in rows.
  - Set finished\_good from finished\_goods at row.reference\_name.
  - Set row.process\_loss\_qty from flt(((row.required\_qty ÷ finished\_good.qty) × finished\_good.process\_loss\_qty), precision).
  - Set row.pending\_qty from flt((((row.required\_qty − row.received\_qty) + row.returned\_qty) + row.process\_loss\_qty), precision).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1241)

<a id="op-df64074b66bfe0"></a>
### Get finished goods

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_raw_materials_to_be_received_subcontracted_raw_materials_to_be_received_get_finished_goods`

**Inputs** order\_items.

**Record and data access** read “Subcontracting Inward Order Item” via get\_all.

**Explicit results** mapping() · mapping of row.name → row for row drawn from Platform.get\_all(“Subcontracting Inward Order Item”, filters = mapping(“name” → list(“in”, list(order\_items))), fields = list(“name”, “qty”, “process\_loss\_qty”)).

**Local steps**

- If not order\_items.
  - Return mapping().
- Return mapping of row.name → row for row drawn from Platform.get\_all(“Subcontracting Inward Order Item”, filters = mapping(“name” → list(“in”, list(order\_items))), fields = list(“name”, “qty”, “process\_loss\_qty”)).
  - Draw row from Platform.get\_all(“Subcontracting Inward Order Item”, filters = mapping(“name” → list(“in”, list(order\_items))), fields = list(“name”, “qty”, “process\_loss\_qty”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1240)

<a id="op-8f6618ede98936"></a>
### Get columns

`operation_enterprise_binding_enterprise_subcontracting_report_subcontracted_raw_materials_to_be_received_subcontracted_raw_materials_to_be_received_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(expanded get\_inward\_order\_columns(), mapping(“label” → translated “Finished Good”, “fieldname” → “main\_item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Raw Mater ….

**Local steps**

- Return list(expanded get\_inward\_order\_columns(), mapping(“label” → translated “Finished Good”, “fieldname” → “main\_item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Raw Mater ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1238)

## Record · Subcontracting bom

<a id="op-317b9aa65563d0"></a>
### Subcontracting BOM.validate

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_subcontracting_bill_of_materials_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_finished\_good().
- Evaluate self.validate\_finished\_good\_bom().
- Evaluate self.validate\_service\_item().
- Evaluate self.validate\_quantities().
- Evaluate self.validate\_is\_active().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate finished good](operations-001.md#op-4f24f699b3b750), [validate finished good bom](operations-001.md#op-0615b8dc7516d0), [validate service item](operations-001.md#op-f7dc932812c0a1), [validate quantities](operations-001.md#op-14a6bb52a6a1d1), [validate is active](operations-001.md#op-ba8496bd92fd5b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L923)

<a id="op-fb6e81fd735c57"></a>
### Subcontracting BOM.before save

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_subcontracting_bill_of_materials_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_conversion\_factor().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set conversion factor](operations-001.md#op-6947db69dc369b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L1342) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L921)

<a id="op-4f24f699b3b750"></a>
### Subcontracting BOM.validate finished good

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_subcontracting_bill_of_materials_validate_finished_good`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Finished Good {0} is disabled.”.format(Platform.bold(self.finished\_good)) · validation helper — translated “Finished Good {0} must be a stock item.”.format(Platform.bold(self.finished\_good)) · validation helper — translated “Finished Good {0} does not have a default BOM.”.format(Platform.bold(self.finished\_good)) · validation helper — translated “Finished Good {0} must be a sub-contracted item.”.format(Platform.bold(self.finished\_good)).

**Local steps**

- Set tuple(disabled, is\_stock\_item, default\_bom, is\_sub\_contracted\_item) from Platform.db.get\_value(“Item”, self.finished\_good, list(“disabled”, “is\_stock\_item”, “default\_bom”, “is\_sub\_contracted\_item”)).
- If disabled.
  - Call the validation error handler Platform.throw(translated “Finished Good {0} is disabled.”.format(Platform.bold(self.finished\_good))).
- If not is\_stock\_item.
  - Call the validation error handler Platform.throw(translated “Finished Good {0} must be a stock item.”.format(Platform.bold(self.finished\_good))).
- If (not default\_bom and not get\_default\_bom(self.finished\_good)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not default\_bom → not get\_default\_bom(self.finished\_good).
  - Call the validation error handler Platform.throw(translated “Finished Good {0} does not have a default BOM.”.format(Platform.bold(self.finished\_good))).
- If not is\_sub\_contracted\_item.
  - Call the validation error handler Platform.throw(translated “Finished Good {0} must be a sub-contracted item.”.format(Platform.bold(self.finished\_good))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L924)

<a id="op-0615b8dc7516d0"></a>
### Subcontracting BOM.validate finished good bom

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_bom_subcontracting_bom_subcontractingbom_validate_finished_good_bom`

**Inputs** self.

**Record and data access** read “BOM” via get\_value.

**Explicit failure paths** validation helper — translated “BOM {0} does not belong to Item {1}”.format(Platform.bold(self.finished\_good\_bom), Platform.bold(self.finished\_good)) · validation helper — translated “BOM {0} must be active and submitted.”.format(Platform.bold(self.finished\_good\_bom)).

**Local steps**

- Set tuple(bom\_item, is\_active, docstatus) from Platform.db.get\_value(“BOM”, self.finished\_good\_bom, list(“item”, “is\_active”, “docstatus”)).
- If bom\_item does not belong to get\_applicable\_bom\_items(self.finished\_good).
  - Call the validation error handler Platform.throw(translated “BOM {0} does not belong to Item {1}”.format(Platform.bold(self.finished\_good\_bom), Platform.bold(self.finished\_good))).
- If (self.is\_active and (not is\_active or docstatus differs from 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_active → (not is\_active or docstatus differs from 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_active → docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “BOM {0} must be active and submitted.”.format(Platform.bold(self.finished\_good\_bom))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1182)

<a id="op-f7dc932812c0a1"></a>
### Subcontracting BOM.validate service item

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_subcontracting_bill_of_materials_validate_service_item`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Service Item {0} is disabled.”.format(Platform.bold(self.service\_item)) · validation helper — translated “Service Item {0} must be a non-stock item.”.format(Platform.bold(self.service\_item)).

**Local steps**

- Set tuple(disabled, is\_stock\_item) from Platform.db.get\_value(“Item”, self.service\_item, list(“disabled”, “is\_stock\_item”)).
- If disabled.
  - Call the validation error handler Platform.throw(translated “Service Item {0} is disabled.”.format(Platform.bold(self.service\_item))).
- If is\_stock\_item.
  - Call the validation error handler Platform.throw(translated “Service Item {0} must be a non-stock item.”.format(Platform.bold(self.service\_item))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L1877) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L926)

<a id="op-14a6bb52a6a1d1"></a>
### Subcontracting BOM.validate quantities

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_bom_subcontracting_bom_subcontractingbom_validate_quantities`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} must be greater than zero.”.format(translated self.meta.get\_label(fieldname)).

**Local steps**

- For each fieldname in tuple(“finished\_good\_qty”, “service\_item\_qty”).
  - If flt(self.get(fieldname)) ≤ 0.
    - Call the validation error handler Platform.throw(translated “{0} must be greater than zero.”.format(translated self.meta.get\_label(fieldname))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1183)

<a id="op-ba8496bd92fd5b"></a>
### Subcontracting BOM.validate is active

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_subcontracting_bill_of_materials_validate_is_active`

**Inputs** self.

**Record and data access** read “Subcontracting BOM” via exists.

**Explicit failure paths** validation helper — translated “There is already an active Subcontracting BOM {0} for the Finished Good {1}.”.format(Platform.bold(sb), Platform.bold(self.finished\_good)).

**Local steps**

- If self.is\_active.
  - If sb bound to Platform.db.exists(“Subcontracting BOM”, mapping(“finished\_good” → self.finished\_good, “is\_active” → 1, “name” → list(“!=”, self.name))).
    - Call the validation error handler Platform.throw(translated “There is already an active Subcontracting BOM {0} for the Finished Good {1}.”.format(Platform.bold(sb), Platform.bold(self.finished\_good))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L2157) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L925)

<a id="op-6947db69dc369b"></a>
### Subcontracting BOM.set conversion factor

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_subcontracting_bill_of_materials_set_conversion_factor`

**Inputs** self.

**Local steps**

- Set self.conversion\_factor from (flt(self.service\_item\_qty) ÷ flt(self.finished\_good\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L2415) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L922)

<a id="op-e3254822c6507f"></a>
### Get finished good bom

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_bom_subcontracting_bom_get_finished_good_bom`

**Inputs** item.

**Declared result** (str bitwise or no value).

**Record and data access** read “Subcontracting BOM” via get\_value.

**Explicit results** (Platform.db.get\_value(“Subcontracting BOM”, mapping(“finished\_good” → item.name, “is\_active” → 1), “finished\_good\_bom”) or item.default\_bom or get\_default\_bom(item.variant\_of)).

**Local steps**

- Return (Platform.db.get\_value(“Subcontracting BOM”, mapping(“finished\_good” → item.name, “is\_active” → 1), “finished\_good\_bom”) or item.default\_bom or get\_default\_bom(item.variant\_of)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Subcontracting BOM”, mapping(“finished\_good” → item.name, “is\_active” → 1), “finished\_good\_bom”) → item.default\_bom → get\_default\_bom(item.variant\_of).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1181)

<a id="op-7ee6d448123db2"></a>
### Get applicable bom items

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_bom_subcontracting_bom_get_applicable_bom_items`

**Inputs** item\_code.

**Declared result** list at str.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** list(item\_code, template) when template, otherwise list(item\_code).

**Local steps**

- Set template from Platform.get\_cached\_value(“Item”, item\_code, “variant\_of”).
- Return list(item\_code, template) when template, otherwise list(item\_code).
  - Value choice on template — true gives list(item\_code, template), false gives list(item\_code).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “variant\_of”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1180)

<a id="op-585208785f43e7"></a>
### Finished good bom query

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_bom_subcontracting_bom_finished_good_bom_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** list() · bom(doctype, txt, searchfield, start, …).

**Local steps**

- Set filters from (filters or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set finished\_good from filters.pop(“finished\_good”, no value).
- If (not finished\_good or not isinstance(finished\_good, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not finished\_good → not isinstance(finished\_good, str).
  - Return list().
- Set filters at “item” from list(“in”, get\_applicable\_bom\_items(finished\_good)).
- Return bom(doctype, txt, searchfield, start, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1179)

<a id="op-a18bc198b12799"></a>
### Check order read permission

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_bom_subcontracting_bom_check_order_read_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1178)

<a id="op-df5fad55004453"></a>
### Get subcontracting boms for finished goods

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_get_subcontracting_bills_of_materials_for_finished_goods`

**Inputs** fg\_items.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Subcontracting BOM” via get\_all.

**Explicit results** mapping of d.finished\_good → d for d drawn from subcontracting\_boms · subcontracting\_boms at 0 · Platform.\_dict(mapping()).

**Local steps**

- Evaluate check\_order\_read\_permission().
- If fg\_items.
  - Set filters from mapping(“is\_active” → 1).
  - If isinstance(fg\_items, list).
    - Set filters at “finished\_good” from list(“in”, fg\_items).
  - Otherwise.
    - Set filters at “finished\_good” from fg\_items.
  - If subcontracting\_boms bound to Platform.get\_all(“Subcontracting BOM”, filters = filters, fields = LOOKUP\_FIELDS).
    - If isinstance(fg\_items, list).
      - Return mapping of d.finished\_good → d for d drawn from subcontracting\_boms.
        - Draw d from subcontracting\_boms.
    - Otherwise.
      - Return subcontracting\_boms at 0.
- Return Platform.\_dict(mapping()).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L919)

<a id="op-2799be7ed8bdc3"></a>
### Get subcontracting boms for service item

`operation_enterprise_subcontracting_record_definitions_subcontracting_bill_of_materials_business_behavior_get_subcontracting_bills_of_materials_for_service_item`

**Inputs** service\_item.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Subcontracting BOM” via get\_all.

**Explicit results** mapping of d.finished\_good → d for d drawn from Subcontracting\_boms · mapping().

**Local steps**

- Evaluate check\_order\_read\_permission().
- If service\_item.
  - Set filters from mapping(“is\_active” → 1, “service\_item” → service\_item).
  - Set Subcontracting\_boms from Platform.db.get\_all(“Subcontracting BOM”, filters = filters, fields = LOOKUP\_FIELDS).
  - If Subcontracting\_boms.
    - Return mapping of d.finished\_good → d for d drawn from Subcontracting\_boms.
      - Draw d from Subcontracting\_boms.
- Return mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L920)

## Record · Subcontracting inward order

[Record definition](../../../../data/record-types/subcontracting_inward_order.json)

<a id="op-b4ad8ea518564f"></a>
### Subcontracting Inward Order.validate

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- Evaluate check\_on\_hold\_or\_closed\_status(“Sales Order”, self.sales\_order).
- Evaluate self.set\_is\_customer\_provided\_item().
- Evaluate self.validate\_customer\_provided\_items().
- Evaluate self.validate\_customer\_warehouse().
- Evaluate self.validate\_service\_items().
- Evaluate self.set\_missing\_values().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set is customer provided item](operations-002.md#op-b2c6c1f744356c), [validate customer provided items](operations-002.md#op-3076c4bd05e6ab), [validate customer warehouse](operations-002.md#op-15bbf2facdbdc9), [validate service items](operations-002.md#op-1d6163c91d4b4d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L948)

<a id="op-8913db698fa2ab"></a>
### Subcontracting Inward Order.on submit

`operation_enterprise_subcontracting_record_definitions_subcontracting_inward_order_business_behavior_subcontracting_inward_order_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- Evaluate self.update\_subcontracted\_quantity\_in\_so().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-002.md#op-05b7f44912f36b), [update subcontracted quantity in so](operations-002.md#op-025fa8a844a662).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0949.json#L3548) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L942)
