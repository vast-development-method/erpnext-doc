# Shared transaction rules · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock controller

<a id="op-9edffb657c724c"></a>
### Stock Controller.get voucher details

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_voucher_details`

**Inputs** self, default\_expense\_account, default\_cost\_center, sle\_map.

**Record and data access** read self.doctype via get\_value.

**Explicit results** details.

**Local steps**

- If self.doctype equals “Stock Reconciliation”.
  - Set reconciliation\_purpose from Platform.db.get\_value(self.doctype, self.name, “purpose”).
  - Set is\_opening from “Yes” when reconciliation\_purpose equals “Opening Stock”, otherwise “No”.
    - Value choice on reconciliation\_purpose equals “Opening Stock” — true gives “Yes”, false gives “No”.
  - Set details from list().
  - For each voucher\_detail\_no in sle\_map.
    - Evaluate details.append(Platform.\_dict(mapping(“name” → voucher\_detail\_no, “expense\_account” → default\_expense\_account, “cost\_center” → default\_cost\_center, “is\_opening” → is\_opening))).
  - Return details.
- Otherwise.
  - Set details from self.get(“items”).
  - If (default\_expense\_account or default\_cost\_center).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in default\_expense\_account → default\_cost\_center.
    - For each d in details.
      - If (default\_expense\_account and not d.get(“expense\_account”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_expense\_account → not d.get(“expense\_account”).
        - Set d.expense\_account from default\_expense\_account.
      - If (default\_cost\_center and not d.get(“cost\_center”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_cost\_center → not d.get(“cost\_center”).
        - Set d.cost\_center from default\_cost\_center.
  - Return details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L391)

<a id="op-d8ad7738461a38"></a>
### Stock Controller.get items and warehouses

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_items_and_warehouses`

**Inputs** self.

**Declared result** tuple at tuple(list at str, list at str).

**Explicit results** tuple(list(), list()) · tuple(list(items), list(warehouses)).

**Local steps**

- If not (hasattr(self, “items”) or hasattr(self, “packed\_items”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hasattr(self, “items”) → hasattr(self, “packed\_items”).
  - Return tuple(list(), list()).
- Set item\_rows from ((self.get(“items”) or list()) + (self.get(“packed\_items”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“items”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“packed\_items”) → list().
- Set items from set of d.item\_code for d drawn from item\_rows where d.item\_code.
  - Draw d from item\_rows, keep a combination only if (d.item\_code).
- Set warehouses from set().
- For each d in item\_rows.
  - If d.get(“warehouse”).
    - Evaluate warehouses.add(d.warehouse).
  - If self.doctype equals “Stock Entry”.
    - If d.get(“s\_warehouse”).
      - Evaluate warehouses.add(d.s\_warehouse).
    - If d.get(“t\_warehouse”).
      - Evaluate warehouses.add(d.t\_warehouse).
- Return tuple(list(items), list(warehouses)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L640)

<a id="op-e84139200ec5e1"></a>
### Stock Controller.get stock ledger details

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_stock_ledger_details`

**Inputs** self.

**Explicit results** stock\_ledger.

**Local steps**

- Set stock\_ledger from mapping().
- Set table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set stock\_ledger\_entries from nested operand in the contract(nested operand in the contract).select(table.name, table.warehouse, table.stock\_value\_difference, table.valuation\_rate, …).where(((nested operand in the contract.voucher\_type ….
- For each sle in stock\_ledger\_entries.
  - Evaluate stock\_ledger.setdefault(sle.voucher\_detail\_no, list()).append(sle).
- Return stock\_ledger.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L964) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L641)

<a id="op-b88e34fa13f933"></a>
### Stock Controller.check expense account

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_check_expense_account`

**Inputs** self, item.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Expense Account not set for the Item {1}. {2}”.format(item.idx, Platform.bold(item.item\_code), msg) · validation helper — translated “Expense / Difference account ({0}) must be a 'Profit or Loss' account”.format(item.get(“expense\_account”)) · validation helper — translated “{0} {1}: Cost Center is mandatory for Item {2}”.format(translated self.doctype, self.name, item.get(“item\_code”)).

**Local steps**

- If not item.get(“expense\_account”).
  - Set msg from translated “Please set an Expense Account in the Items table”.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Expense Account not set for the Item {1}. {2}”.format(item.idx, Platform.bold(item.item\_code), msg), title = translated “Expense Account Missing”).
- Otherwise.
  - Set is\_expense\_account from Platform.get\_cached\_value(“Account”, item.get(“expense\_account”), “report\_type”) equals “Profit and Loss”.
  - If (self.doctype does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”, “Stock Reconciliation”, “Stock Entry”, …) and not is\_expense\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”, “Stock Reconciliation”, “Stock Entry”, …) → not is\_expense\_account.
    - Call the validation error handler Platform.throw(translated “Expense / Difference account ({0}) must be a 'Profit or Loss' account”.format(item.get(“expense\_account”))).
  - If (is\_expense\_account and not item.get(“cost\_center”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_expense\_account → not item.get(“cost\_center”).
    - Call the validation error handler Platform.throw(translated “{0} {1}: Cost Center is mandatory for Item {2}”.format(translated self.doctype, self.name, item.get(“item\_code”))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, item.get(“expense\_account”), “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L373)

<a id="op-90def406e2addb"></a>
### Stock Controller.delete auto created batches

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_delete_auto_created_batches`

**Inputs** self.

**State and service calls** request set\_value on “Serial and Batch Bundle” · request set\_value on “Serial and Batch Entry” · call db\_set on row.

**Local steps**

- For each table\_name in list(“items”, “packed\_items”, “supplied\_items”).
  - If not self.get(table\_name).
    - Continue with the next iteration or loop test.
  - For each row in self.get(table\_name).
    - Set update\_values from mapping().
    - If row.get(“batch\_no”).
      - Set update\_values at “batch\_no” from no value.
    - If row.get(“serial\_and\_batch\_bundle”).
      - Set update\_values at “serial\_and\_batch\_bundle” from no value.
      - Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle, mapping(“is\_cancelled” → 1)).
      - Evaluate Platform.db.set\_value(“Serial and Batch Entry”, mapping(“parent” → row.serial\_and\_batch\_bundle), mapping(“is\_cancelled” → 1)).
    - If update\_values.
      - Evaluate row.db\_set(update\_values).
    - If (table\_name equals “items” and row.get(“rejected\_serial\_and\_batch\_bundle”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_name equals “items” → row.get(“rejected\_serial\_and\_batch\_bundle”).
      - Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, row.rejected\_serial\_and\_batch\_bundle, mapping(“is\_cancelled” → 1)).
      - Evaluate Platform.db.set\_value(“Serial and Batch Entry”, mapping(“parent” → row.rejected\_serial\_and\_batch\_bundle), mapping(“is\_cancelled” → 1)).
      - Evaluate row.db\_set(“rejected\_serial\_and\_batch\_bundle”, no value).
    - If row.get(“current\_serial\_and\_batch\_bundle”).
      - Evaluate row.db\_set(“current\_serial\_and\_batch\_bundle”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L634)

<a id="op-4da1c281f4bf9c"></a>
### Stock Controller.set serial and batch bundle

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_set_serial_and_batch_bundle`

**Inputs** self, table\_name = no value, ignore\_validate = false.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**Local steps**

- If not table\_name.
  - Set table\_name from “items”.
- Set QTY\_FIELD from mapping(“serial\_and\_batch\_bundle” → “qty”, “current\_serial\_and\_batch\_bundle” → “current\_qty”, “rejected\_serial\_and\_batch\_bundle” → “rejected\_qty”).
- For each row in self.get(table\_name).
  - For each field in QTY\_FIELD.keys().
    - If row.get(field).
      - Evaluate Platform.get\_doc(“Serial and Batch Bundle”, row.get(field)).set\_serial\_and\_batch\_values(self, row, qty\_field = QTY\_FIELD at field).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L976) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L653)

<a id="op-8fdf7d816cdfa6"></a>
### Stock Controller.make package for transfer

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_make_package_for_transfer`

**Inputs** self, serial\_and\_batch\_bundle, warehouse, type\_of\_transaction = no value, do\_not\_submit = no value, qty = 0, include\_bundle = no value, exclude\_serial\_nos = no value, total\_qty = 0.

**Explicit results** make\_bundle\_for\_material\_transfer(is\_new = self.is\_new(), docstatus = self.docstatus, voucher\_type = self.doctype, voucher\_no = self.name, …).

**Local steps**

- Return make\_bundle\_for\_material\_transfer(is\_new = self.is\_new(), docstatus = self.docstatus, voucher\_type = self.doctype, voucher\_no = self.name, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L970) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L647)

<a id="op-8be5cc79cee615"></a>
### Stock Controller.get sl entries

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_stock_ledger_entries`

**Inputs** self, d, args.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** sl\_dict.

**Local steps**

- Set sl\_dict from Platform.\_dict(mapping(“item\_code” → d.get(“item\_code”, no value), “warehouse” → d.get(“warehouse”, no value), “serial\_and\_batch\_bundle” → d.get(“serial\_and\_batch\_bundle”), “posting\_date” → self.posting\_date, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.docstatus equals 1 and 1) → negative 1.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“item\_code”) → d.get(“item\_code”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“project”) → self.get(“project”).
  - Value choice on self.docstatus equals 2 — true gives 1, false gives 0.
- Evaluate sl\_dict.update(args).
- Evaluate self.update\_inventory\_dimensions(d, sl\_dict).
- If self.docstatus equals 2.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
  - For each field in list(“serial\_no”, “batch\_no”).
    - If d.get(field).
      - Set sl\_dict at field from d.get(field).
- Return sl\_dict.

**Methods declared on this owner** [update inventory dimensions](operations-025.md#op-4b6e8cd6cec1e5).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, (args.get(“item\_code”) or d.get(“item\_code”)), “stock\_uom”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L965) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L642)

<a id="op-5207ec5cb4e136"></a>
### Stock Controller.set landed cost voucher amount

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_set_landed_cost_voucher_amount`

**Inputs** self.

**State and service calls** call db\_set on d.

**Local steps**

- For each d in self.get(“items”).
  - Set lcv\_item from Platform.qb.DocType(“Landed Cost Item”).
  - Set query from nested operand in the contract.qb.from\_(lcv\_item).select(Sum(lcv\_item.applicable\_charges), lcv\_item.cost\_center).where((lcv\_item.docstatus equals 1 bitwise and lcv\_item.receipt\_document equals self.name)).
  - If self.doctype equals “Stock Entry”.
    - Set query from query.where(lcv\_item.stock\_entry\_item equals d.name).
  - Otherwise.
    - Set query from query.where(lcv\_item.purchase\_receipt\_item equals d.name).
  - Set lc\_voucher\_data from query.run(as\_list = true).
  - Set d.landed\_cost\_voucher\_amount from lc\_voucher\_data at 0 at 0 when lc\_voucher\_data, otherwise 0.0.
    - Value choice on lc\_voucher\_data — true gives lc\_voucher\_data at 0 at 0, false gives 0.0.
  - If (not d.cost\_center and lc\_voucher\_data and lc\_voucher\_data at 0 at 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.cost\_center → lc\_voucher\_data → lc\_voucher\_data at 0 at 1.
    - Evaluate d.db\_set(“cost\_center”, lc\_voucher\_data at 0 at 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1162) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L402)

<a id="op-f13ef23ea28ec8"></a>
### Stock Controller.has landed cost amount

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_has_landed_cost_amount`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- For each row in self.items.
  - If row.get(“landed\_cost\_voucher\_amount”).
    - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L392)

<a id="op-48870ebe76031f"></a>
### Stock Controller.get item account wise lcv entries

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_item_account_wise_landed_cost_voucher_entries`

**Inputs** self.

**Record and data access** read “Landed Cost Purchase Receipt” via get\_all · resolve a document from “Landed Cost Voucher” via get\_doc.

**Explicit results** no value · mapping of key → list(charges.values()) for tuple(key, charges) drawn from item\_account\_wise\_cost.items().

**Local steps**

- If not self.has\_landed\_cost\_amount().
  - Return no value.
- Set landed\_cost\_vouchers from Platform.get\_all(“Landed Cost Purchase Receipt”, fields = list(“parent”), filters = mapping(“receipt\_document” → self.name, “docstatus” → 1)).
- If not landed\_cost\_vouchers.
  - Return no value.
- Bind dependencies get\_lcv\_dimension\_fields, get\_row\_dimensions.
- Set item\_account\_wise\_cost from mapping().
- Set dimension\_fields from get\_lcv\_dimension\_fields().
- Set row\_fieldname from “purchase\_receipt\_item”.
- If self.doctype equals “Stock Entry”.
  - Set row\_fieldname from “stock\_entry\_item”.
- For each lcv in landed\_cost\_vouchers.
  - Set landed\_cost\_voucher\_doc from Platform.get\_doc(“Landed Cost Voucher”, lcv.parent).
  - Set based\_on\_field from “applicable\_charges”.
  - If landed\_cost\_voucher\_doc.distribute\_charges\_based\_on differs from “Distribute Manually”.
    - Set based\_on\_field from Platform.scrub(landed\_cost\_voucher\_doc.distribute\_charges\_based\_on).
  - Set total\_item\_cost from 0.
  - If based\_on\_field.
    - For each item in landed\_cost\_voucher\_doc.items.
      - Update total\_item\_cost using + item.get(based\_on\_field).
  - For each item in landed\_cost\_voucher\_doc.items.
    - If item.receipt\_document equals self.name.
      - Set charges from item\_account\_wise\_cost.setdefault(tuple(item.item\_code, item.get(row\_fieldname)), mapping()).
      - For each account in landed\_cost\_voucher\_doc.taxes.
        - Set exchange\_rate from (account.exchange\_rate or 1).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.exchange\_rate → 1.
        - Set dimensions from get\_row\_dimensions(account, item, dimension\_fields).
        - Set group\_key from tuple(account.expense\_account, tuple(generator of dimensions.get(field) for field drawn from dimension\_fields)).
          - Draw field from dimension\_fields.
        - Set item\_row from charges.get(group\_key).
        - If item\_row is identical to no value.
          - Set item\_row, charges at group\_key from Platform.\_dict(expense\_account = account.expense\_account, amount = 0.0, base\_amount = 0.0, dimensions = dimensions).
        - If total\_item\_cost &gt; 0.
          - Update item\_row.amount using + ((account.amount × item.get(based\_on\_field)) ÷ total\_item\_cost).
          - Update item\_row.base\_amount using + ((account.base\_amount × item.get(based\_on\_field)) ÷ total\_item\_cost).
        - Otherwise.
          - Update item\_row.amount using + (item.applicable\_charges ÷ exchange\_rate).
          - Update item\_row.base\_amount using + item.applicable\_charges.
- Return mapping of key → list(charges.values()) for tuple(key, charges) drawn from item\_account\_wise\_cost.items().
  - Draw tuple(key, charges) from item\_account\_wise\_cost.items().

**Methods declared on this owner** [has landed cost amount](operations-025.md#op-f13ef23ea28ec8).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L961) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L638)

<a id="op-94ce2f196969bb"></a>
### Stock Controller.validate inventory dimension mandatory

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_inventory_dimension_mandatory`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-94ce2f196969bb-guard-4"></a>If self.docstatus ≥ 2.
  - Return no value.
- For each table\_field in list(“items”, “packed\_items”, “supplied\_items”).
  - Set rows from self.get(table\_field).
  - If rows.
    - Evaluate self.validate\_mandatory\_dimensions\_in\_table(rows).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus ≥ 2, self.docstatus = 2 (cancelled) selects the branch that returns no value. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-94ce2f196969bb-guard-4)

**Methods declared on this owner** [validate mandatory dimensions in table](operations-025.md#op-316feef894e8f7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1172) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L412)

<a id="op-316feef894e8f7"></a>
### Stock Controller.validate mandatory dimensions in table

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_mandatory_dimensions_in_table`

**Inputs** self, rows.

**Explicit results** no value.

**Local steps**

- Set child\_doctype from rows at 0.doctype.
- Set dimensions from get\_mandatory\_inventory\_dimensions(child\_doctype).
- If not dimensions.
  - Return no value.
- Set child\_meta from Platform.get\_meta(child\_doctype).
- For each dimension in dimensions.
  - Set mandatory\_fields from get\_mandatory\_dimension\_fields(child\_doctype, dimension).
  - For each row in rows.
    - If (mandatory\_fields and not self.is\_service\_item\_row(row)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in mandatory\_fields → not self.is\_service\_item\_row(row).
      - Evaluate self.validate\_mandatory\_dimension\_row(row, dimension, mandatory\_fields, child\_meta).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is service item row](operations-025.md#op-190a9b160267a1), [validate mandatory dimension row](operations-025.md#op-8b08b68a0ecd5d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L414)

<a id="op-190a9b160267a1"></a>
### Stock Controller.is service item row

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_is_service_item_row`

**Inputs** self, row.

**Declared result** bool.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** (bool(item\_code) and not Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”)).

**Local steps**

- Set item\_code from row.get(“item\_code”).
- Return (bool(item\_code) and not Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(item\_code) → not Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L396)

<a id="op-8b08b68a0ecd5d"></a>
### Stock Controller.validate mandatory dimension row

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_mandatory_dimension_row`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, row, dimension, mandatory\_fields, child\_meta.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L413)

<a id="op-4b6e8cd6cec1e5"></a>
### Stock Controller.update inventory dimensions

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_update_inventory_dimensions`

**Inputs** self, row, sl\_dict.

**Declared result** no value.

**State and service calls** call db\_set on row.

**Local steps**

- If row.get(“item\_row”).
  - Set row from row.get(“item\_row”).
- Set dimensions from get\_evaluated\_inventory\_dimension(row, sl\_dict, parent\_doc = self).
- For each dimension in dimensions.
  - If not dimension.
    - Continue with the next iteration or loop test.
  - If (self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”) and row.get(“rejected\_warehouse”) and sl\_dict.get(“warehouse”) equals row.get(“rejected\_warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”) → row.get(“rejected\_warehouse”) → sl\_dict.get(“warehouse”) equals row.get(“rejected\_warehouse”).
    - Set fieldname from formatted text rejected\_{dimension.source\_fieldname}.
    - Set sl\_dict at dimension.target\_fieldname from row.get(fieldname).
    - Continue with the next iteration or loop test.
  - If self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Sales Invoice”, “Delivery Note”, …).
    - If ((((sl\_dict.actual\_qty &gt; 0 and not nested operand in the contract.get(“is\_return”)) or (sl\_dict.actual\_qty &lt; 0 and self.get(“is\_return”))) and self.doctype belongs to list(“Purchase Invoice”, “Purchase Rec ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (((sl\_dict.actual\_qty &gt; 0 and not self.get(“is\_return”)) or (sl\_dict.actual\_qty &lt; 0 and self.get(“is\_return”))) and self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Stock Entry”)) → (((sl\_dict.actual\_qty &lt; 0 and not self.get(“is\_return”)) or (sl\_dict.actual\_qty &gt; 0 and self.get(“is\_return”))) and self.doctype belongs to list(“Sales Invoice”, “Delivery Note”, “Stock Entry”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ((sl\_dict.actual\_qty &gt; 0 and not self.get(“is\_return”)) or (sl\_dict.actual\_qty &lt; 0 and self.get(“is\_return”))) → self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Stock Entry”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (sl\_dict.actual\_qty &gt; 0 and not self.get(“is\_return”)) → (sl\_dict.actual\_qty &lt; 0 and self.get(“is\_return”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sl\_dict.actual\_qty &gt; 0 → not self.get(“is\_return”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sl\_dict.actual\_qty &lt; 0 → self.get(“is\_return”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ((sl\_dict.actual\_qty &lt; 0 and not self.get(“is\_return”)) or (sl\_dict.actual\_qty &gt; 0 and self.get(“is\_return”))) → self.doctype belongs to list(“Sales Invoice”, “Delivery Note”, “Stock Entry”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (sl\_dict.actual\_qty &lt; 0 and not self.get(“is\_return”)) → (sl\_dict.actual\_qty &gt; 0 and self.get(“is\_return”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sl\_dict.actual\_qty &lt; 0 → not self.get(“is\_return”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sl\_dict.actual\_qty &gt; 0 → self.get(“is\_return”).
      - If self.doctype equals “Stock Entry”.
        - If (row.get(“t\_warehouse”) equals sl\_dict.warehouse and sl\_dict.get(“actual\_qty”) &gt; 0).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“t\_warehouse”) equals sl\_dict.warehouse → sl\_dict.get(“actual\_qty”) &gt; 0.
          - Set fieldname from formatted text to\_{dimension.source\_fieldname}.
          - If dimension.source\_fieldname.startswith(“to\_”).
            - Set fieldname from formatted text {dimension.source\_fieldname}.
          - Set sl\_dict at dimension.target\_fieldname from row.get(fieldname).
          - Continue with the next iteration or loop test.
      - Set sl\_dict at dimension.target\_fieldname from row.get(dimension.source\_fieldname).
    - Otherwise.
      - Set fieldname\_start\_with from “to”.
      - If self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”).
        - Set fieldname\_start\_with from “from”.
      - Set fieldname from formatted text {fieldname\_start\_with}\_{dimension.source\_fieldname}.
      - Set sl\_dict at dimension.target\_fieldname from row.get(fieldname).
      - If not sl\_dict.get(dimension.target\_fieldname).
        - Set sl\_dict at dimension.target\_fieldname from row.get(dimension.source\_fieldname).
  - Otherwise.
    - If row.get(dimension.source\_fieldname).
      - Set sl\_dict at dimension.target\_fieldname from row.get(dimension.source\_fieldname).
  - If (not sl\_dict.get(dimension.target\_fieldname) and dimension.fetch\_from\_parent).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sl\_dict.get(dimension.target\_fieldname) → dimension.fetch\_from\_parent.
    - Set sl\_dict at dimension.target\_fieldname from self.get(dimension.fetch\_from\_parent).
    - If not sl\_dict.get(dimension.target\_fieldname).
      - Set fieldname from next(generator of field.fieldname for field drawn from Platform.get\_meta(self.doctype).fields where field.options equals dimension.fetch\_from\_parent, no value).
        - Draw field from Platform.get\_meta(self.doctype).fields, keep a combination only if (field.options equals dimension.fetch\_from\_parent).
      - If (fieldname and self.get(fieldname)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname → self.get(fieldname).
        - Set sl\_dict at dimension.target\_fieldname from self.get(fieldname).
    - If (sl\_dict at dimension.target\_fieldname and self.docstatus equals 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sl\_dict at dimension.target\_fieldname → self.docstatus equals 1.
      - Evaluate row.db\_set(dimension.source\_fieldname, sl\_dict at dimension.target\_fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1164) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L404)

<a id="op-8678d524cbb513"></a>
### Stock Controller.make sl entries

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_make_stock_ledger_entries`

**Inputs** self, sl\_entries, allow\_negative\_stock = false, via\_landed\_cost\_voucher = false.

**Local steps**

- Bind dependencies update\_batch\_qty.
- Bind dependencies make\_sl\_entries.
- Evaluate make\_sl\_entries(sl\_entries, allow\_negative\_stock, via\_landed\_cost\_voucher).
- Evaluate update\_batch\_qty(self.doctype, self.name, self.docstatus, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).
- Evaluate self.validate\_reserved\_batches().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reserved batches](operations-025.md#op-0c4fa5aef4f5ba).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L971) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L648)

<a id="op-0c4fa5aef4f5ba"></a>
### Stock Controller.validate reserved batches

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_reserved_batches`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Serial and Batch Entry” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The batch {0} is reserved for {1} in the warehouse {2} and the remaining quantity is not enough to cover the …”.format(Platform.bold(batch\_no), vouchers, Platform.bold(warehouse), Platform.bold ….

**Local steps**

- If not Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Return no value.
- If self.doctype does not belong to list(“Delivery Note”, “Sales Invoice”, “Stock Entry”, “Stock Reconciliation”).
  - Return no value.
- Set batches from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “docstatus” → 1, “batch\_no” → tuple(“is”, “set”), …), pluck = “batch\_no”).
- If not batches.
  - Return no value.
- Set reference\_fields from mapping(“Sales Invoice” → list(“sales\_order”), “Delivery Note” → list(“against\_sales\_order”), “Stock Entry” → list(“work\_order”, “subcontracting\_inward\_order”)).get(self.doctype, list()).
- Set items from self.items.
- If self.doctype equals “Stock Entry”.
  - Set items from list(self).
- Set own\_vouchers from set of item.get(field) for item drawn from items, then field drawn from reference\_fields where item.get(field).
  - Draw item from items.
  - Draw field from reference\_fields, keep a combination only if (item.get(field)).
- Set outstanding\_qty from defaultdict(float).
- Set reservations from defaultdict(list).
- For each row in self.get\_reserved\_batches(batches).
  - If row.voucher\_no belongs to own\_vouchers.
    - Continue with the next iteration or loop test.
  - Set key from tuple(row.batch\_no, row.warehouse).
  - Set outstanding from (flt(row.qty) − flt(row.delivered\_qty)).
  - Update outstanding\_qty at key using + outstanding.
  - If outstanding &gt; 0.
    - Evaluate reservations at key.append(row).
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- For each tuple(tuple(batch\_no, warehouse), reserved\_qty) in outstanding\_qty.items().
  - If flt(reserved\_qty, precision) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set batch\_qty from get\_batch\_qty\_for\_stock(batch\_no, warehouse, posting\_date = self.posting\_date, posting\_time = self.posting\_time, consider\_negative\_batches = true).
  - If flt(batch\_qty, precision) ≥ flt(reserved\_qty, precision).
    - Continue with the next iteration or loop test.
  - Set vouchers from “, ”.join(generator of formatted text {Platform.bold(voucher\_type)} {Platform.bold(voucher\_no)} for tuple(voucher\_type, voucher\_no) drawn from dict.fromkeys(generator of tuple(row.voucher\_type, row.voucher ….
    - Draw tuple(voucher\_type, voucher\_no) from dict.fromkeys(generator of tuple(row.voucher\_type, row.voucher\_no) for row drawn from reservations at tuple(batch\_no, warehouse)).
    - Draw row from reservations at tuple(batch\_no, warehouse).
  - Call the validation error handler Platform.throw(translated “The batch {0} is reserved for {1} in the warehouse {2} and the remaining quantity is not enough to cover the …”.format(Platform.bold(batch\_no), vouchers, Platform.bold(warehouse) ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reserved batches](operations-025.md#op-004158ec676c7b).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L422)

<a id="op-004158ec676c7b"></a>
### Stock Controller.get reserved batches

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_reserved_batches`

**Inputs** self, batches.

**Explicit results** nested operand in the contract(nested operand in the contract).select(child\_doc.batch\_no, child\_doc.qty, child\_doc.delivered\_qty, doctype.voucher\_type, …).where((doctype.docstatus equals 1 bitwise and nest ….

**Local steps**

- Set doctype from Platform.qb.DocType(“Stock Reservation Entry”).
- Set child\_doc from Platform.qb.DocType(“Serial and Batch Entry”).
- Return nested operand in the contract(nested operand in the contract).select(child\_doc.batch\_no, child\_doc.qty, child\_doc.delivered\_qty, doctype.voucher\_type, …).where((doctype.docstatus equals 1 bitwise and nest ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L386)

<a id="op-1461e467432281"></a>
### Stock Controller.make gl entries on cancel

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_make_general_ledger_entries_on_cancel`

**Inputs** self, from\_repost = false.

**Record and data access** execute query text (SELECT, GL Entry).

**Local steps**

- If not from\_repost.
  - Evaluate cancel\_exchange\_gain\_loss\_journal(Platform.\_dict(doctype = self.doctype, name = self.name)).
- If Platform.db.sql(query text (SELECT, GL Entry), tuple(self.doctype, self.name)).
  - Evaluate self.make\_gl\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [make gl entries](operations-023.md#op-1962b7ab32e527).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L969) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L646)

<a id="op-2f9b29f543494e"></a>
### Stock Controller.get serialized items

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_serialized_items`

**Inputs** self.

**Explicit results** serialized\_items.

**Local steps**

- Set serialized\_items from list().
- Set item\_codes from list(set(generator of d.item\_code for d drawn from self.get(“items”))).
  - Draw d from self.get(“items”).
- If item\_codes.
  - Set serialized\_items from Platform.db.sql\_list(query text (SELECT, Item).format(“, ”.join((list(“%s”) × len(item\_codes)))), tuple(item\_codes)).
- Return serialized\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L388)

<a id="op-bd20d0f6be0920"></a>
### Stock Controller.validate warehouse

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_validate_warehouse`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_disabled\_warehouse, validate\_warehouse\_company.
- Set warehouses from list(set(generator of d.warehouse for d drawn from self.get(“items”) where getattr(d, “warehouse”, no value))).
  - Draw d from self.get(“items”), keep a combination only if (getattr(d, “warehouse”, no value)).
- Set target\_warehouses from list(set(list of d.target\_warehouse for d drawn from self.get(“items”) where getattr(d, “target\_warehouse”, no value))).
  - Draw d from self.get(“items”), keep a combination only if (getattr(d, “target\_warehouse”, no value)).
- Evaluate warehouses.extend(target\_warehouses).
- Set from\_warehouse from list(set(list of d.from\_warehouse for d drawn from self.get(“items”) where getattr(d, “from\_warehouse”, no value))).
  - Draw d from self.get(“items”), keep a combination only if (getattr(d, “from\_warehouse”, no value)).
- Evaluate warehouses.extend(from\_warehouse).
- For each w in warehouses.
  - Evaluate validate\_disabled\_warehouse(w).
  - Evaluate validate\_warehouse\_company(w, self.company).

If control reaches the end, it returns no value.

**Derived worked case from the contract** If a transfer’s source belongs to the voucher company but its target belongs to another company, target validation fails.

**Values supplied outside this operation** selected callable from getattr(d, “warehouse”, no value), getattr(d, “target\_warehouse”, no value) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0442.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L988) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L665) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-6cdb56174869dc"></a>
### Stock Controller.update billing percentage

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_update_billing_percentage`

**Inputs** self, update\_modified = true.

**Local steps**

- Set target\_ref\_field from “amount”.
- If self.doctype equals “Delivery Note”.
  - Set total\_amount, total\_returned from 0.
  - For each item in self.items.
    - Update total\_amount using + flt(item.amount).
    - Update total\_returned using + flt((item.returned\_qty × item.rate)).
  - If total\_returned &lt; total\_amount.
    - Set target\_ref\_field from mapping(“SUB” → list(“amount”, mapping(“MUL” → list(“returned\_qty”, “rate”))), “as” → “ref\_amount”).
- Evaluate self.\_update\_percent\_field(mapping(“target\_dt” → (self.doctype + “ Item”), “target\_parent\_dt” → self.doctype, “target\_parent\_field” → “per\_billed”, “target\_ref\_field” → target\_ref\_field, …), update\_modified).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L655)

<a id="op-bdd2cd46e592d3"></a>
### Stock Controller.validate inspection

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_validate_inspection`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set inspection\_fieldname\_map from mapping(“Purchase Receipt” → “inspection\_required\_before\_purchase”, “Purchase Invoice” → “inspection\_required\_before\_purchase”, “Subcontracting Receipt” → “inspection\_required\_before\_purchase”, “Sales Invo ….
- Set inspection\_required\_fieldname from inspection\_fieldname\_map.get(self.doctype).
- If ((not inspection\_required\_fieldname and self.doctype differs from “Stock Entry”) or (self.doctype equals “Stock Entry” and not self.inspection\_required) or (self.doctype belongs to list(“Sales Invoice”, “P ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not inspection\_required\_fieldname and self.doctype differs from “Stock Entry”) → (self.doctype equals “Stock Entry” and not self.inspection\_required) → (self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) and not self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not inspection\_required\_fieldname → self.doctype differs from “Stock Entry”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Stock Entry” → not self.inspection\_required.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) → not self.update\_stock.
  - Return no value.
- Bind dependencies validate\_qi\_reference.
- For each row in self.get(“items”).
  - Evaluate validate\_qi\_reference(self, row).
  - Set qi\_required from false.
  - If (inspection\_required\_fieldname and Platform.get\_cached\_value(“Item”, row.item\_code, inspection\_required\_fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in inspection\_required\_fieldname → Platform.get\_cached\_value(“Item”, row.item\_code, inspection\_required\_fieldname).
    - Set qi\_required from true.
  - Otherwise.
    - If self.doctype equals “Stock Entry”.
      - Set qi\_required from stock\_entry\_row\_requires\_inspection(self.purpose, row).
  - If is\_inspection\_exempt\_secondary\_row(self, row).
    - Continue with the next iteration or loop test.
  - If qi\_required.
    - If (self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Sales Invoice”, “Delivery Note”, …) and Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_o ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Sales Invoice”, “Delivery Note”, …) → Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).
      - Return no value.
    - Evaluate self.validate\_qi\_presence(row).
    - If self.docstatus equals 1.
      - Evaluate self.validate\_qi\_submission(row).
      - Evaluate self.validate\_qi\_rejection(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate qi presence](operations-026.md#op-843de2b14cddae), [validate qi submission](operations-026.md#op-7894a202e13ffd), [validate qi rejection](operations-026.md#op-e0ea7b8e0768a9).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, inspection\_required\_fieldname), Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L986) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L663)
