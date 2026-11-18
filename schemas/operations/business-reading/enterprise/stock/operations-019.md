# Inventory and warehouses · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Inventory dimension

[Record definition](../../../../data/record-types/inventory_dimension.json)

<a id="op-5cca1d513742b4"></a>
### Inventory Dimension.has stock ledger

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_has_stock_ledger`

**Inputs** self.

**Declared result** str.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** no value · Platform.get\_all(“Stock Ledger Entry”, filters = mapping(self.target\_fieldname → tuple(“is”, “set”), “is\_cancelled” → 0), limit = 1).

**Local steps**

- If not self.target\_fieldname.
  - Return no value.
- Return Platform.get\_all(“Stock Ledger Entry”, filters = mapping(self.target\_fieldname → tuple(“is”, “set”), “is\_cancelled” → 0), limit = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L630) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1026)

<a id="op-766e0f8b8b65a0"></a>
### Inventory Dimension.validate

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_reference\_document().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reference document](operations-019.md#op-4fc5bd6fcc1452).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L777) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1033)

<a id="op-2513277935ff6e"></a>
### Inventory Dimension.before save

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.do\_not\_update\_document().
- Evaluate self.reset\_value().
- Evaluate self.set\_source\_and\_target\_fieldname().
- Evaluate self.set\_type\_of\_transaction().

If control reaches the end, it returns no value.

**Methods declared on this owner** [do not update document](operations-019.md#op-03714de1e83d91), [reset value](operations-019.md#op-d59e085e4d5017), [set source and target fieldname](operations-019.md#op-97b2819e601b91), [set type of transaction](operations-019.md#op-21080e1bba24d5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L828) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1021)

<a id="op-21080e1bba24d5"></a>
### Inventory Dimension.set type of transaction

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_set_type_of_transaction`

**Inputs** self.

**Local steps**

- If self.apply\_to\_all\_doctypes.
  - Set self.type\_of\_transaction from “Both”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L939) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1032)

<a id="op-03714de1e83d91"></a>
### Inventory Dimension.do not update document

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_do_not_update_document`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with DoNotChangeError — translated “The user can not change value of the field {0} because stock transactions exists against the dimension {1}.”.format(bold(translated field.label), bold(self.name)).

**Local steps**

- If (self.is\_new() or not self.has\_stock\_ledger()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_stock\_ledger().
  - Return no value.
- Set old\_doc from self.\_doc\_before\_save.
- Set allow\_to\_edit\_fields from list(“fetch\_from\_parent”, “type\_of\_transaction”, “condition”, “validate\_negative\_stock”).
- For each field in Platform.get\_meta(“Inventory Dimension”).fields.
  - If (field.fieldname does not belong to allow\_to\_edit\_fields and old\_doc.get(field.fieldname) differs from self.get(field.fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldname does not belong to allow\_to\_edit\_fields → old\_doc.get(field.fieldname) differs from self.get(field.fieldname).
    - Call the validation error handler Platform.throw(translated “The user can not change value of the field {0} because stock transactions exists against the dimension {1}.”.format(bold(translated field.label), bold(self.name)), DoNotChangeError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has stock ledger](operations-019.md#op-5cca1d513742b4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1023)

<a id="op-f029c875058128"></a>
### Inventory Dimension.on trash

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper with DoNotChangeError — translated “Inventory Dimension {0} cannot be deleted as stock transactions exist against it”.format(bold(self.name)).

**Local steps**

- If self.has\_stock\_ledger().
  - Call the validation error handler Platform.throw(translated “Inventory Dimension {0} cannot be deleted as stock transactions exist against it”.format(bold(self.name)), DoNotChangeError).
- Evaluate self.delete\_custom\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [has stock ledger](operations-019.md#op-5cca1d513742b4), [delete custom fields](operations-019.md#op-da226bf4e13410).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1027)

<a id="op-da226bf4e13410"></a>
### Inventory Dimension.delete custom fields

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_delete_custom_fields`

**Inputs** self.

**Record and data access** read “Custom Field” via get\_all.

**State and service calls** msgprint with translated “Deleted custom fields related to the dimension {0}”.format(self.name).

**Local steps**

- Set document\_fieldnames from list(self.source\_fieldname, formatted text to\_{self.source\_fieldname}, formatted text from\_{self.source\_fieldname}, formatted text rejected\_{self.source\_fieldname}).
- For each doctype in self.get\_dimension\_doctypes().
  - For each field in Platform.get\_all(“Custom Field”, filters = mapping(“dt” → doctype, “fieldname” → tuple(“in”, document\_fieldnames))).
    - Evaluate delete\_dimension\_custom\_field(field.name).
- For each doctype in tuple(“Stock Ledger Entry”, “Stock Closing Balance”).
  - For each field in Platform.get\_all(“Custom Field”, filters = mapping(“dt” → doctype, “fieldname” → self.target\_fieldname)).
    - Evaluate delete\_dimension\_custom\_field(field.name).
- Evaluate Platform.msgprint(translated “Deleted custom fields related to the dimension {0}”.format(self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get dimension doctypes](operations-019.md#op-59932b8d905fd7).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1022)

<a id="op-59932b8d905fd7"></a>
### Inventory Dimension.get dimension doctypes

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_inventorydimension_get_dimension_doctypes`

**Inputs** self.

**Explicit results** list(self.document\_type) · list of row at 0 for row drawn from get\_inventory\_documents().

**Local steps**

- If not self.apply\_to\_all\_doctypes.
  - Return list(self.document\_type).
- Return list of row at 0 for row drawn from get\_inventory\_documents().
  - Draw row from get\_inventory\_documents().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L274)

<a id="op-d59e085e4d5017"></a>
### Inventory Dimension.reset value

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_reset_value`

**Inputs** self.

**Local steps**

- If self.apply\_to\_all\_doctypes.
  - Set self.type\_of\_transaction from empty text.
  - Set self.istable from 0.
  - For each field in list(“document\_type”, “condition”).
    - Evaluate self.set(field, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1030)

<a id="op-4fc5bd6fcc1452"></a>
### Inventory Dimension.validate reference document

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_validate_reference_document`

**Inputs** self.

**Record and data access** read “DocType” via get\_cached\_value.

**Explicit failure paths** validation helper with CanNotBeChildDoc — translated “The reference document {0} can not be child table.”.format(self.reference\_document) · validation helper with CanNotBeDefaultDimension — translated “The reference document {0} can not be an Inventory Dimension.”.format(self.reference\_document).

**Local steps**

- If Platform.get\_cached\_value(“DocType”, self.reference\_document, “istable”) equals 1.
  - Call the validation error handler Platform.throw(translated “The reference document {0} can not be child table.”.format(self.reference\_document), CanNotBeChildDoc).
- If self.reference\_document belongs to list(“Batch”, “Serial No”, “Warehouse”, “Item”).
  - Call the validation error handler Platform.throw(translated “The reference document {0} can not be an Inventory Dimension.”.format(self.reference\_document), CanNotBeDefaultDimension).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“DocType”, self.reference\_document, “istable”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1034)

<a id="op-97b2819e601b91"></a>
### Inventory Dimension.set source and target fieldname

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_set_source_and_target_fieldname`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If not self.source\_fieldname.
  - Set self.source\_fieldname from scrub(self.dimension\_name).
- If not self.target\_fieldname.
  - Set self.target\_fieldname from scrub(self.dimension\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L2285) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1031)

<a id="op-84139f46cf0086"></a>
### Inventory Dimension.on update

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.add\_custom\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add custom fields](operations-019.md#op-63df0800610541).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L2421) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1028)

<a id="op-c18361bc60bf17"></a>
### Inventory Dimension.get insert after fieldname

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_get_insert_after_fieldname`

**Inputs** doctype.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “DocField” via get\_all.

**Explicit results** Platform.get\_all(“DocField”, fields = list(“fieldname”), filters = mapping(“parent” → doctype), order\_by = “idx desc”, limit = 1) at 0.fieldname.

**Local steps**

- Return Platform.get\_all(“DocField”, fields = list(“fieldname”), filters = mapping(“parent” → doctype), order\_by = “idx desc”, limit = 1) at 0.fieldname.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L2472) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1025)

<a id="op-017bef784bf458"></a>
### Inventory Dimension.get dimension fields

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_get_dimension_fields`

**Inputs** self, doctype = no value.

**Explicit results** dimension\_fields.

**Local steps**

- If not doctype.
  - Set doctype from self.document\_type.
- Set label\_start\_with from empty text.
- If doctype belongs to list(“Purchase Invoice Item”, “Purchase Receipt Item”).
  - Set label\_start\_with from “Target”.
- Otherwise.
  - If doctype belongs to list(“Sales Invoice Item”, “Delivery Note Item”, “Stock Entry Detail”).
    - Set label\_start\_with from “Source”.
- Set label from self.dimension\_name.
- If label\_start\_with.
  - Set label from formatted text {label\_start\_with} {self.dimension\_name}.
- Set dimension\_fields from list(dict(fieldname = “inventory\_dimension”, fieldtype = “Section Break”, insert\_after = self.get\_insert\_after\_fieldname(doctype), label = translated “Inventory Dimension”, …), dict(fieldname = self.source ….
  - Value choice on doctype equals “Stock Entry Detail” — true gives “eval:doc.s\_warehouse”, false gives empty text.
- If doctype belongs to list(“Purchase Invoice Item”, “Purchase Receipt Item”).
  - Evaluate dimension\_fields.append(dict(fieldname = (“rejected\_” + self.source\_fieldname), fieldtype = “Link”, insert\_after = self.source\_fieldname, options = self.reference\_document, …)).
- Return dimension\_fields.

**Methods declared on this owner** [get insert after fieldname](operations-019.md#op-c18361bc60bf17).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1024)

<a id="op-63df0800610541"></a>
### Inventory Dimension.add custom fields

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_add_custom_fields`

**Inputs** self.

**Record and data access** read “Custom Field” via get\_value.

**Local steps**

- Set custom\_fields from mapping().
- Set dimension\_fields from list().
- If self.apply\_to\_all\_doctypes.
  - For each doctype in get\_inventory\_documents().
    - Set dimension\_fields from self.get\_dimension\_fields(doctype at 0).
    - Evaluate self.add\_transfer\_field(doctype at 0, dimension\_fields).
    - Evaluate custom\_fields.setdefault(doctype at 0, dimension\_fields).
- Otherwise.
  - Set dimension\_fields from self.get\_dimension\_fields().
  - Evaluate self.add\_transfer\_field(self.document\_type, dimension\_fields).
  - Evaluate custom\_fields.setdefault(self.document\_type, dimension\_fields).
- For each dt in list(“Stock Ledger Entry”, “Stock Closing Balance”).
  - If (dimension\_fields and not Platform.db.get\_value(“Custom Field”, mapping(“dt” → dt, “fieldname” → self.target\_fieldname)) and not field\_exists(dt, self.target\_fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimension\_fields → not Platform.db.get\_value(“Custom Field”, mapping(“dt” → dt, “fieldname” → self.target\_fieldname)) → not field\_exists(dt, self.target\_fieldname).
    - Set dimension\_field from dimension\_fields at 1.copy().
    - Set dimension\_field at “fieldname” from self.target\_fieldname.
    - Set custom\_fields at dt from dimension\_field.
- Set filter\_custom\_fields from mapping().
- Set ignore\_doctypes from list(“Serial and Batch Bundle”, “Serial and Batch Entry”, “Pick List Item”, “Maintenance Visit Purpose”).
- If custom\_fields.
  - For each tuple(doctype, fields) in custom\_fields.items().
    - If doctype belongs to ignore\_doctypes.
      - Continue with the next iteration or loop test.
    - If isinstance(fields, dict).
      - Set fields from list(fields).
    - For each field in fields.
      - If not field\_exists(doctype, field at “fieldname”).
        - Evaluate filter\_custom\_fields.setdefault(doctype, list()).append(field).
- Evaluate create\_dimension\_custom\_fields(filter\_custom\_fields).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get dimension fields](operations-019.md#op-017bef784bf458), [add transfer field](operations-019.md#op-4e5471d25ce286).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1019)

<a id="op-4e5471d25ce286"></a>
### Inventory Dimension.add transfer field

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_add_transfer_field`

**Inputs** self, doctype, dimension\_fields.

**Explicit results** no value.

**Local steps**

- If doctype does not belong to list(“Stock Entry Detail”, “Sales Invoice Item”, “Delivery Note Item”, “Purchase Invoice Item”, …).
  - Return no value.
- Set fieldname\_start\_with from “to”.
- Set label\_start\_with from “Target”.
- Set display\_depends\_on from empty text.
- If doctype belongs to list(“Purchase Invoice Item”, “Purchase Receipt Item”).
  - Set fieldname\_start\_with from “from”.
  - Set label\_start\_with from “Source”.
  - Set display\_depends\_on from “eval:parent.is\_internal\_supplier == 1”.
- Otherwise.
  - If doctype differs from “Stock Entry Detail”.
    - Set display\_depends\_on from “eval:parent.is\_internal\_customer == 1”.
  - Otherwise.
    - If doctype equals “Stock Entry Detail”.
      - Set display\_depends\_on from “eval:doc.t\_warehouse”.
- Set fieldname from formatted text {fieldname\_start\_with}\_{self.source\_fieldname}.
- Set label from formatted text {label\_start\_with} {self.dimension\_name}.
- If field\_exists(doctype, fieldname).
  - Return no value.
- Evaluate dimension\_fields.extend(list(dict(fieldname = “inventory\_dimension\_col\_break”, fieldtype = “Column Break”, insert\_after = self.source\_fieldname), dict(fieldname = fieldname, fieldtype = “Link”, insert\_afte ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1020)

<a id="op-7dc427a0bb1fd8"></a>
### Field exists

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_field_exists`

**Inputs** doctype, fieldname.

**Declared result** (str bitwise or no value).

**Record and data access** read “DocField” via get\_value.

**Explicit results** Platform.db.get\_value(“DocField”, mapping(“parent” → doctype, “fieldname” → fieldname), “name”).

**Local steps**

- Return Platform.db.get\_value(“DocField”, mapping(“parent” → doctype, “fieldname” → fieldname), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L5040) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1013)

<a id="op-0a8939a1687e5a"></a>
### Get inventory documents

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_get_inventory_documents`

**Inputs** doctype = no value, txt = no value, searchfield = no value, start = no value, page\_len = no value, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocField” via get\_all.

**Explicit results** Platform.get\_all(“DocField”, fields = list(“parent”), filters = and\_filters, or\_filters = or\_filters, start = start, …).

**Local steps**

- Set and\_filters from list(list(“DocField”, “parent”, “not in”, list(“Batch”, “Serial No”, “Item Price”))).
- Set or\_filters from list(list(“DocField”, “options”, “in”, list(“Batch”, “Serial No”)), list(“DocField”, “parent”, “in”, list(“Putaway Rule”))).
- If txt.
  - Evaluate and\_filters.append(list(“DocField”, “parent”, “like”, formatted text %{txt}%)).
- Return Platform.get\_all(“DocField”, fields = list(“parent”), filters = and\_filters, or\_filters = or\_filters, start = start, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1017)

<a id="op-c497dde8153dd6"></a>
### Get evaluated inventory dimension

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_get_evaluated_inventory_dimension`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doc, sl\_dict, parent\_doc.

**Explicit result forms** a value selected from the current context.

**Local structure** 6 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1015)

<a id="op-494ef950d281c3"></a>
### Get condition values

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_get_condition_values`

**Inputs** doc, parent\_doc = no value.

**Explicit results** values.

**Local steps**

- Set values from mapping(“doc” → get\_field\_values(doc)).
- If parent\_doc.
  - Set values at “parent” from get\_field\_values(parent\_doc).
- Return values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L773) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L270)

<a id="op-f564ff876c7c7d"></a>
### Get field values

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_get_field_values`

**Inputs** doc.

**Explicit results** Platform.\_dict(doc.get\_valid\_dict(sanitize = false, ignore\_virtual = true), doctype = doc.doctype) · Platform.\_dict(doc).

**Local steps**

- If isinstance(doc, BaseDocument).
  - Return Platform.\_dict(doc.get\_valid\_dict(sanitize = false, ignore\_virtual = true), doctype = doc.doctype).
- Return Platform.\_dict(doc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L271)

<a id="op-17caaf9c416bcb"></a>
### Get document wise inventory dimensions

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_get_document_wise_inventory_dimensions`

**Inputs** doctype.

**Wrappers, in declaration order** request\_cache.

**Declared result** dict.

**Record and data access** read “Inventory Dimension” via get\_all.

**Explicit results** Platform.get\_all(“Inventory Dimension”, fields = list(“name”, “source\_fieldname”, “condition”, “target\_fieldname”, …), or\_filters = mapping(“document\_type” → doctype, “apply\_to\_all\_doctypes” → 1)).

**Local steps**

- Return Platform.get\_all(“Inventory Dimension”, fields = list(“name”, “source\_fieldname”, “condition”, “target\_fieldname”, …), or\_filters = mapping(“document\_type” → doctype, “apply\_to\_all\_doctypes” → 1)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L6215) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1014)

<a id="op-64f2e9f0c89539"></a>
### Get mandatory inventory dimensions

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_get_mandatory_inventory_dimensions`

**Inputs** doctype.

**Wrappers, in declaration order** request\_cache.

**Declared result** list.

**Record and data access** read “Inventory Dimension” via get\_all.

**Explicit results** list of d for d drawn from dimensions where (d.reqd or d.mandatory\_depends\_on\_backend).

**Local steps**

- Set dimensions from Platform.get\_all(“Inventory Dimension”, fields = list(“name”, “dimension\_name”, “source\_fieldname”, “reqd”, …), or\_filters = mapping(“document\_type” → doctype, “apply\_to\_all\_doctypes” → 1)).
- Return list of d for d drawn from dimensions where (d.reqd or d.mandatory\_depends\_on\_backend).
  - Draw d from dimensions, keep a combination only if ((d.reqd or d.mandatory\_depends\_on\_backend)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.reqd → d.mandatory\_depends\_on\_backend.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L776) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L273)

<a id="op-36c3b2557f5b7e"></a>
### Get mandatory dimension fields

`operation_enterprise_binding_enterprise_stock_doctype_inventory_dimension_inventory_dimension_get_mandatory_dimension_fields`

**Inputs** doctype, dimension.

**Declared result** list.

**Explicit results** fields.

**Local steps**

- Set fields from list().
- Set source\_fieldname from dimension.source\_fieldname.
- Set backend\_condition from ((dimension.mandatory\_depends\_on\_backend or empty text).strip() or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (dimension.mandatory\_depends\_on\_backend or empty text).strip() → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dimension.mandatory\_depends\_on\_backend → empty text.
- If (dimension.reqd and doctype equals “Stock Entry Detail”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimension.reqd → doctype equals “Stock Entry Detail”.
  - Evaluate fields.append(tuple(source\_fieldname, “doc.s\_warehouse”)).
- Otherwise.
  - If (dimension.reqd and doctype equals “Subcontracting Receipt Supplied Item”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimension.reqd → doctype equals “Subcontracting Receipt Supplied Item”.
    - Evaluate fields.append(tuple(source\_fieldname, “doc.reference\_name”)).
  - Otherwise.
    - If (dimension.reqd and doctype equals “Packed Item”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimension.reqd → doctype equals “Packed Item”.
      - Evaluate fields.append(tuple(source\_fieldname, “doc.parent\_detail\_docname and parent.doctype in &#91;'Delivery Note', 'Sales Invoice', 'POS Invoice'&#93;”)).
    - Otherwise.
      - If dimension.reqd.
        - Evaluate fields.append(tuple(source\_fieldname, no value)).
      - Otherwise.
        - If backend\_condition.
          - Evaluate fields.append(tuple(source\_fieldname, backend\_condition)).
- If doctype belongs to list(“Purchase Invoice Item”, “Purchase Receipt Item”).
  - If dimension.reqd.
    - Evaluate fields.append(tuple(formatted text rejected\_{source\_fieldname}, “doc.rejected\_qty &gt; 0”)).
  - Otherwise.
    - If backend\_condition.
      - Evaluate fields.append(tuple(formatted text rejected\_{source\_fieldname}, formatted text ({backend\_condition}) and doc.rejected\_qty &gt; 0)).
- If ((dimension.reqd or backend\_condition) and doctype belongs to list(“Stock Entry Detail”, “Sales Invoice Item”, “Delivery Note Item”, “Purchase Invoice Item”, …)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (dimension.reqd or backend\_condition) → doctype belongs to list(“Stock Entry Detail”, “Sales Invoice Item”, “Delivery Note Item”, “Purchase Invoice Item”, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dimension.reqd → backend\_condition.
  - If doctype belongs to list(“Purchase Invoice Item”, “Purchase Receipt Item”).
    - Set tuple(transfer\_fieldname, display\_condition) from tuple(formatted text from\_{source\_fieldname}, “parent.is\_internal\_supplier == 1”).
  - Otherwise.
    - If doctype equals “Stock Entry Detail”.
      - Set tuple(transfer\_fieldname, display\_condition) from tuple(formatted text to\_{source\_fieldname}, “doc.t\_warehouse”).
    - Otherwise.
      - Set tuple(transfer\_fieldname, display\_condition) from tuple(formatted text to\_{source\_fieldname}, “parent.is\_internal\_customer == 1”).
  - If dimension.reqd.
    - Set transfer\_condition from display\_condition.
  - Otherwise.
    - Set transfer\_condition from formatted text ({display\_condition}) and ({backend\_condition}).
  - Evaluate fields.append(tuple(transfer\_fieldname, transfer\_condition)).
- Return fields.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L272)
