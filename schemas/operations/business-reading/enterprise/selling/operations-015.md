# Sales · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales order

[Record definition](../../../../data/record-types/sales_order.json)

<a id="op-d0e58007df3678"></a>
### Sales Order.initialize

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Sales Order Item”, “target\_dt” → “Quotation Item”, “join\_field” → “quotation\_item”, “target\_field” → “ordered\_qty”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0641.json#L6197) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1348)

<a id="op-d7f9c09c8c53c5"></a>
### Sales Order.onload

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_onload`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Evaluate super().onload().
- Evaluate self.set\_proforma\_onload().
- If self.get(“is\_subcontracted”).
  - Evaluate self.set\_onload(“can\_update\_items”, self.can\_update\_items()).
  - Return no value.
- If Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - If (self.has\_unreserved\_stock() or self.has\_unreserved\_stock(“packed\_items”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_unreserved\_stock() → self.has\_unreserved\_stock(“packed\_items”).
    - Evaluate self.set\_onload(“has\_unreserved\_stock”, true).
- If has\_reserved\_stock(self.doctype, self.name).
  - Evaluate self.set\_onload(“has\_reserved\_stock”, true).
- If (self.docstatus equals 1 and self.status does not belong to set(“Closed”, “On Hold”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.status does not belong to set(“Closed”, “On Hold”).
  - Evaluate self.set\_onload(“has\_potentially\_billable\_items”, has\_potentially\_billable\_items(self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set proforma onload](operations-015.md#op-93fa6ee0bfc663), [can update items](operations-015.md#op-2213eaf999ecc5), [has unreserved stock](operations-016.md#op-ce485f3326c4fd).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L86) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1354)

<a id="op-93fa6ee0bfc663"></a>
### Sales Order.set proforma onload

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_set_proforma_onload`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- <a id="op-93fa6ee0bfc663-guard-3"></a>If self.docstatus equals 0.
  - Return no value.
- If not Platform.db.get\_single\_value(“Selling Settings”, “enable\_proforma\_invoice”).
  - Return no value.
- Evaluate self.set\_onload(“enable\_proforma\_invoice”, true).
- Evaluate self.set\_onload(“default\_proforma\_print\_format”, Platform.db.get\_single\_value(“Selling Settings”, “default\_proforma\_print\_format”)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that returns no value. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-93fa6ee0bfc663-guard-3)

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings”, “enable\_proforma\_invoice”), Platform.db.get\_single\_value(“Selling Settings”, “default\_proforma\_print\_format”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L79)

<a id="op-2213eaf999ecc5"></a>
### Sales Order.can update items

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_can_update_items`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Subcontracting Inward Order” via exists.

**Explicit results** result.

**Local steps**

- Set result from true.
- If self.is\_subcontracted.
  - If Platform.db.exists(“Subcontracting Inward Order”, mapping(“sales\_order” → self.name, “docstatus” → 1)).
    - Set result from false.
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1340)

<a id="op-a78a34032ffc8a"></a>
### Sales Order.before validate

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_has\_unit\_price\_items().
- Set self.flags.allow\_zero\_qty from self.has\_unit\_price\_items.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set has unit price items](operations-015.md#op-3bb4b06e748d05).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0641.json#L6888) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1339)

<a id="op-03ddedcd825283"></a>
### Sales Order.validate

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- Evaluate self.validate\_delivery\_date().
- Evaluate self.validate\_proj\_cust().
- Evaluate self.validate\_po().
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_for\_items().
- Evaluate self.validate\_warehouse().
- Evaluate self.validate\_drop\_ship().
- Evaluate self.validate\_reserved\_stock().
- Evaluate self.validate\_serial\_no\_based\_delivery().
- Evaluate validate\_against\_blanket\_order(self).
- Evaluate validate\_inter\_company\_party(self.doctype, self.customer, self.company, self.inter\_company\_order\_reference).
- If self.coupon\_code.
  - Evaluate validate\_coupon\_code(self.coupon\_code, self.customer).
- If not self.get(“is\_subcontracted”).
  - Evaluate self.enable\_auto\_reserve\_stock().
- Evaluate make\_packing\_list(self).
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.validate\_fg\_item\_for\_subcontracting().
- Evaluate self.set\_status().
- If not self.billing\_status.
  - Set self.billing\_status from “Not Billed”.
- If not self.delivery\_status.
  - Set self.delivery\_status from “Not Delivered”.
- If not self.advance\_payment\_status.
  - Set self.advance\_payment\_status from “Not Requested”.
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate delivery date](operations-015.md#op-89d2f5a35547bc), [validate proj cust](operations-015.md#op-98651243d300c9), [validate po](operations-015.md#op-cacd7f6caf9ea5), [validate for items](operations-015.md#op-7c2fd05a5b5292), [validate warehouse](operations-015.md#op-06e0a93faf7167), [validate drop ship](operations-015.md#op-fb048507fa996f), [validate reserved stock](operations-016.md#op-61d1c840289423), [validate serial no based delivery](operations-016.md#op-862564c4d92f67), [enable auto reserve stock](operations-015.md#op-392eed918a05a0), [validate with previous doc](operations-015.md#op-b23c3f59d9f416), [validate fg item for subcontracting](operations-015.md#op-1494031037c5ac).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1366)

<a id="op-1494031037c5ac"></a>
### Sales Order.validate fg item for subcontracting

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_validate_fg_item_for_subcontracting`

**Inputs** self.

**Record and data access** read “Item” via get\_value · read “Subcontracting BOM” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Finished Good Item is not specified for service item {1}”.format(item.idx, item.item\_code) · validation helper — translated “Row #{0}: Finished Good Item {1} must be a sub-contracted item”.format(item.idx, item.fg\_item) · validation helper — translated “Row #{0}: BOM not found for FG Item {1}”.format(item.idx, item.fg\_item) · validation helper — translated “Row #{0}: Finished Good Item Qty can not be zero”.format(item.idx).

**Local steps**

- If self.is\_subcontracted.
  - For each item in self.items.
    - If not item.fg\_item.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good Item is not specified for service item {1}”.format(item.idx, item.item\_code)).
    - Otherwise.
      - If not Platform.get\_value(“Item”, item.fg\_item, “is\_sub\_contracted\_item”).
        - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good Item {1} must be a sub-contracted item”.format(item.idx, item.fg\_item)).
      - If (not Platform.db.get\_value(“Subcontracting BOM”, mapping(“finished\_good” → item.fg\_item, “is\_active” → 1), “finished\_good\_bom”) and not get\_default\_bom(item.fg\_item)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.get\_value(“Subcontracting BOM”, mapping(“finished\_good” → item.fg\_item, “is\_active” → 1), “finished\_good\_bom”) → not get\_default\_bom(item.fg\_item).
        - Call the validation error handler Platform.throw(translated “Row #{0}: BOM not found for FG Item {1}”.format(item.idx, item.fg\_item)).
    - If not item.fg\_item\_qty.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good Item Qty can not be zero”.format(item.idx)).
- Otherwise.
  - For each item in self.items.
    - Evaluate item.set(“fg\_item”, no value).
    - Evaluate item.set(“fg\_item\_qty”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L85)

<a id="op-392eed918a05a0"></a>
### Sales Order.enable auto reserve stock

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_enable_auto_reserve_stock`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If (self.is\_new() and Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”).
  - Set self.reserve\_stock from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L76)

<a id="op-3bb4b06e748d05"></a>
### Sales Order.set has unit price items

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_set_has_unit_price_items`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_sales\_order”).
  - Return no value.
- Set self.has\_unit\_price\_items from any(generator of not row.qty for row drawn from self.get(“items”) where (row.item\_code and not row.qty)).
  - Draw row from self.get(“items”), keep a combination only if ((row.item\_code and not row.qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → not row.qty.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_zero\_qty\_in\_sales\_order”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0642.json#L672) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1356)

<a id="op-cacd7f6caf9ea5"></a>
### Sales Order.validate po

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_purchase_order`

**Inputs** self.

**Record and data access** execute query text (SELECT, Sales) · read “Selling Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Warning: Sales Order {0} already exists against Customer's Purchase Order {1}”.format(Platform.bold(so at 0 at 0), Platform.bold(self.po\_no)).

**Explicit failure paths** validation helper — translated “Row #{0}: Expected Delivery Date cannot be before Purchase Order Date”.format(d.idx) · validation helper — translated “Sales Order {0} already exists against Customer's Purchase Order {1}. To allow multiple Sales Orders, Enable …”.format(Platform.bold(so at 0 at 0), Platform.bold(self.po\_no), Platform.bold(tran ….

**Local steps**

- If (self.po\_date and not self.skip\_delivery\_note).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.po\_date → not self.skip\_delivery\_note.
  - For each d in self.get(“items”).
    - If (d.delivery\_date and getdate(self.po\_date) &gt; getdate(d.delivery\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.delivery\_date → getdate(self.po\_date) &gt; getdate(d.delivery\_date).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Expected Delivery Date cannot be before Purchase Order Date”.format(d.idx)).
- If (self.po\_no and self.customer and not self.skip\_delivery\_note).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.po\_no → self.customer → not self.skip\_delivery\_note.
  - Set so from Platform.db.sql(query text (SELECT, Sales), tuple(self.po\_no, self.name, self.customer)).
  - If (so and so at 0 at 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in so → so at 0 at 0.
    - If cint(Platform.get\_single\_value(“Selling Settings”, “allow\_against\_multiple\_purchase\_orders”)).
      - Evaluate Platform.msgprint(translated “Warning: Sales Order {0} already exists against Customer's Purchase Order {1}”.format(Platform.bold(so at 0 at 0), Platform.bold(self.po\_no)), alert = true).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Sales Order {0} already exists against Customer's Purchase Order {1}. To allow multiple Sales Orders, Enable …”.format(Platform.bold(so at 0 at 0), Platform.bold(self.po\_no), Pla ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_against\_multiple\_purchase\_orders”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1371)

<a id="op-7c2fd05a5b5292"></a>
### Sales Order.validate for items

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_for_items`

**Inputs** self.

**Record and data access** execute query text (SELECT, Bin).

**Local steps**

- For each d in self.get(“items”).
  - Set d.transaction\_date from self.transaction\_date.
  - Set tot\_avail\_qty from Platform.db.sql(query text (SELECT, Bin), tuple(d.item\_code, d.warehouse)).
  - Set d.projected\_qty from ((tot\_avail\_qty and flt(tot\_avail\_qty at 0 at 0)) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (tot\_avail\_qty and flt(tot\_avail\_qty at 0 at 0)) → 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tot\_avail\_qty → flt(tot\_avail\_qty at 0 at 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1369)

<a id="op-4f88a5c8fe6d4b"></a>
### Sales Order.product bundle has stock item

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_product_bundle_has_stock_item`

**Inputs** self, product\_bundle.

**Record and data access** execute query text (SELECT).

**Explicit results** ret.

**Local steps**

- Set ret from len(Platform.db.sql(query text (SELECT), product\_bundle)).
- Return ret.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L87) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1355)

<a id="op-abcf3b2ca18f5b"></a>
### Sales Order.validate sales mntc quotation

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_sales_mntc_quotation`

**Inputs** self.

**Record and data access** execute query text (SELECT, Quotation).

**State and service calls** msgprint with translated “Quotation {0} not of type {1}”.format(d.prevdoc\_docname, self.order\_type).

**Local steps**

- For each d in self.get(“items”).
  - If d.prevdoc\_docname.
    - Set res from Platform.db.sql(query text (SELECT, Quotation), tuple(d.prevdoc\_docname, self.order\_type)).
    - If not res.
      - Evaluate Platform.msgprint(translated “Quotation {0} not of type {1}”.format(d.prevdoc\_docname, self.order\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1372)

<a id="op-89d2f5a35547bc"></a>
### Sales Order.validate delivery date

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_delivery_date`

**Inputs** self.

**State and service calls** msgprint with translated “Expected Delivery Date should be after Sales Order Date”.

**Explicit failure paths** validation helper — translated “Please enter Delivery Date”.

**Local steps**

- If (self.order\_type equals “Sales” and not self.skip\_delivery\_note).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.order\_type equals “Sales” → not self.skip\_delivery\_note.
  - Set delivery\_date\_list from list of d.delivery\_date for d drawn from self.get(“items”) where d.delivery\_date.
    - Draw d from self.get(“items”), keep a combination only if (d.delivery\_date).
  - Set max\_delivery\_date from max(delivery\_date\_list) when delivery\_date\_list, otherwise no value.
    - Value choice on delivery\_date\_list — true gives max(delivery\_date\_list), false gives no value.
  - If ((max\_delivery\_date and not self.delivery\_date) or (max\_delivery\_date and getdate(self.delivery\_date) differs from getdate(max\_delivery\_date))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (max\_delivery\_date and not self.delivery\_date) → (max\_delivery\_date and getdate(self.delivery\_date) differs from getdate(max\_delivery\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_delivery\_date → not self.delivery\_date.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_delivery\_date → getdate(self.delivery\_date) differs from getdate(max\_delivery\_date).
    - Set self.delivery\_date from max\_delivery\_date.
  - If self.delivery\_date.
    - For each d in self.get(“items”).
      - If not d.delivery\_date.
        - Set d.delivery\_date from self.delivery\_date.
      - If getdate(self.transaction\_date) &gt; getdate(d.delivery\_date).
        - Evaluate Platform.msgprint(translated “Expected Delivery Date should be after Sales Order Date”, indicator = “orange”, title = translated “Invalid Delivery Date”, raise\_exception = true).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Please enter Delivery Date”).
- Evaluate self.validate\_sales\_mntc\_quotation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate sales mntc quotation](operations-015.md#op-abcf3b2ca18f5b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1367)

<a id="op-98651243d300c9"></a>
### Sales Order.validate proj cust

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_project_customer`

**Inputs** self.

**Record and data access** execute query text (SELECT, Project).

**Explicit failure paths** validation helper — translated “Customer {0} does not belong to project {1}”.format(self.customer, self.project).

**Local steps**

- If (self.project and self.customer\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project → self.customer\_name.
  - Set res from Platform.db.sql(query text (SELECT, Project), tuple(self.project, self.customer)).
  - If not res.
    - Call the validation error handler Platform.throw(translated “Customer {0} does not belong to project {1}”.format(self.customer, self.project)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1370)

<a id="op-06e0a93faf7167"></a>
### Sales Order.validate warehouse

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_warehouse`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper with WarehouseRequired — translated “Source warehouse required for stock item {0}”.format(d.item\_code).

**Local steps**

- Evaluate super().validate\_warehouse().
- For each d in self.get(“items”).
  - If ((Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”) equals 1 or (self.has\_product\_bundle(d.item\_code) and self.product\_bundle\_has\_stock\_item(d.item\_code))) and not d.warehouse and not cint(d. ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”) equals 1 or (self.has\_product\_bundle(d.item\_code) and self.product\_bundle\_has\_stock\_item(d.item\_code))) → not d.warehouse → not cint(d.delivered\_by\_supplier).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”) equals 1 → (self.has\_product\_bundle(d.item\_code) and self.product\_bundle\_has\_stock\_item(d.item\_code)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_product\_bundle(d.item\_code) → self.product\_bundle\_has\_stock\_item(d.item\_code).
    - Call the validation error handler Platform.throw(translated “Source warehouse required for stock item {0}”.format(d.item\_code), WarehouseRequired).

If control reaches the end, it returns no value.

**Methods declared on this owner** [product bundle has stock item](operations-015.md#op-4f88a5c8fe6d4b).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0642.json#L4685) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1375)

<a id="op-b23c3f59d9f416"></a>
### Sales Order.validate with previous doc

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_with_previous_record`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Quotation” → mapping(“ref\_dn\_field” → “prevdoc\_docname”, “compare\_fields” → list(list(“company”, “=”))), “Quotation Item” → mapping(“ref\_dn\_field” → “quotation\_i ….
- If cint(Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”)).
  - Evaluate self.validate\_rate\_with\_reference\_doc(list(list(“Quotation”, “prevdoc\_docname”, “quotation\_item”))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0642.json#L5005) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1376)

<a id="op-35effa722f1137"></a>
### Sales Order.update enquiry status

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_update_enquiry_status`

**Inputs** self, prevdoc, flag.

**Record and data access** execute query text (SELECT, Quotation).

**State and service calls** execute query text (UPDATE, Opportunity).

**Local steps**

- Set enq from Platform.db.sql(query text (SELECT, Quotation), prevdoc).
- If enq.
  - Evaluate Platform.db.sql(query text (UPDATE, Opportunity), tuple(flag, enq at 0 at 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1360)

<a id="op-0327d9cce8131c"></a>
### Sales Order.update prevdoc status

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_update_prevdoc_status`

**Inputs** self, flag = no value, update\_quotation\_qty = false.

**Record and data access** resolve a document from “Quotation” via get\_doc.

**Explicit failure paths** validation helper — translated “Quotation {0} is cancelled”.format(quotation).

**Local steps**

- If update\_quotation\_qty.
  - Evaluate super().update\_prevdoc\_status().
- For each quotation in set(generator of d.prevdoc\_docname for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
  - If quotation.
    - Set doc from Platform.get\_doc(“Quotation”, quotation).
    - If doc.docstatus.is\_cancelled().
      - Call the validation error handler Platform.throw(translated “Quotation {0} is cancelled”.format(quotation)).
    - Evaluate doc.set\_status(update = true).
    - Evaluate doc.update\_opportunity(“Converted” when flag equals “submit”, otherwise “Quotation”).
      - Value choice on flag equals “submit” — true gives “Converted”, false gives “Quotation”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1362)

<a id="op-8cf1a0040fa024"></a>
### Sales Order.update ordered qty in quotation for removed items

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_update_ordered_qty_in_quotation_for_removed_items`

**Inputs** self, removed\_items.

**Record and data access** read “Quotation Item” via get\_value · resolve a document from “Quotation” via get\_doc.

**State and service calls** request set\_value on “Quotation Item”.

**Local steps**

- Set soi from Platform.qb.DocType(“Sales Order Item”).
- Set quotations from set().
- For each item in removed\_items.
  - Set quotation\_item from item.get(“quotation\_item”).
  - If not quotation\_item.
    - Continue with the next iteration or loop test.
  - Set ordered\_qty from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i … at 0.
  - Evaluate Platform.db.set\_value(“Quotation Item”, quotation\_item, “ordered\_qty”, flt(ordered\_qty)).
  - Set quotation from Platform.db.get\_value(“Quotation Item”, quotation\_item, “parent”).
  - If quotation.
    - Evaluate quotations.add(quotation).
- For each quotation in quotations.
  - Evaluate Platform.get\_doc(“Quotation”, quotation).set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L82)

<a id="op-fb048507fa996f"></a>
### Sales Order.validate drop ship

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_drop_ship`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Set Supplier for item {1}”.format(d.idx, d.item\_code).

**Local steps**

- For each d in self.get(“items”).
  - If (d.delivered\_by\_supplier and not d.supplier).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.delivered\_by\_supplier → not d.supplier.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Set Supplier for item {1}”.format(d.idx, d.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0642.json#L5861) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1368)

<a id="op-49f52e401deeb8"></a>
### Sales Order.on submit

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Authorization Control” via get\_cached\_doc.

**Local steps**

- Evaluate super().update\_prevdoc\_status().
- Evaluate self.check\_credit\_limit().
- Evaluate self.update\_reserved\_qty().
- Evaluate self.delete\_removed\_delivery\_schedule\_items().
- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(self.doctype, self.company, self.base\_grand\_total, self).
- Evaluate self.update\_project().
- Evaluate self.update\_prevdoc\_status(“submit”).
- Evaluate self.update\_blanket\_order().
- Evaluate update\_linked\_doc(self.doctype, self.name, self.inter\_company\_order\_reference).
- If self.coupon\_code.
  - Bind dependencies update\_coupon\_code\_count.
  - Evaluate update\_coupon\_code\_count(self.coupon\_code, “used”).
- If (self.get(“reserve\_stock”) and not self.get(“is\_subcontracted”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“reserve\_stock”) → not self.get(“is\_subcontracted”).
  - Evaluate self.\_create\_stock\_reservation\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check credit limit](operations-016.md#op-07d1e9d51b6f8e), [update reserved qty](operations-016.md#op-37dcf68b41e0b9), [delete removed delivery schedule items](operations-015.md#op-381909972633f8), [update project](operations-016.md#op-4f41adc5244b95), [update prevdoc status](operations-015.md#op-0327d9cce8131c), [create stock reservation entries](operations-016.md#op-f39d24086207e0).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L84) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1352)

<a id="op-381909972633f8"></a>
### Sales Order.delete removed delivery schedule items

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_delete_removed_delivery_schedule_items`

**Inputs** self.

**Local steps**

- Set items from list of d.name for d drawn from self.get(“items”).
  - Draw d from self.get(“items”).
- Set doctype from Platform.qb.DocType(“Delivery Schedule Item”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((doctype.sales\_order equals self.name bitwise and nested operand in the contract.sales\_order\_item.notin(items))).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L75)

<a id="op-e8939d122c84d0"></a>
### Sales Order.on cancel

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Closed order cannot be cancelled. Unclose to cancel.”.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Payment Ledger Entry”, “Advance Payment Ledger Entry”, …).
- Evaluate super().on\_cancel().
- Evaluate super().update\_prevdoc\_status().
- <a id="op-e8939d122c84d0-guard-13"></a>If self.status equals “Closed”.
  - Call the validation error handler Platform.throw(translated “Closed order cannot be cancelled. Unclose to cancel.”).
- Evaluate self.delete\_delivery\_schedule\_items().
- Evaluate self.check\_nextdoc\_docstatus().
- Evaluate self.update\_reserved\_qty().
- Evaluate self.update\_project().
- Evaluate self.update\_prevdoc\_status(“cancel”).
- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.update\_blanket\_order().
- Evaluate self.cancel\_stock\_reservation\_entries().
- Evaluate unlink\_inter\_company\_doc(self.doctype, self.name, self.inter\_company\_order\_reference).
- If self.coupon\_code.
  - Bind dependencies update\_coupon\_code\_count.
  - Evaluate update\_coupon\_code\_count(self.coupon\_code, “cancelled”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Closed”, self.status = “Closed” selects the branch that calls the validation-error handler with translated “Closed order cannot be cancelled. Unclose to cancel.”. With self.status = “Draft”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e8939d122c84d0-guard-13)

**Methods declared on this owner** [delete delivery schedule items](operations-017.md#op-ec31da29995d33), [check nextdoc docstatus](operations-016.md#op-8e03460de90855), [update reserved qty](operations-016.md#op-37dcf68b41e0b9), [update project](operations-016.md#op-4f41adc5244b95), [update prevdoc status](operations-015.md#op-0327d9cce8131c), [cancel stock reservation entries](operations-017.md#op-91f9be66d3667e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1349)
