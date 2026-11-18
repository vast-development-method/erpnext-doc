# Sales · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales order

[Record definition](../../../../data/record-types/sales_order.json)

<a id="op-33ef7fe32ed932"></a>
### Sales Order.on trash

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.delete\_delivery\_schedule\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete delivery schedule items](operations-017.md#op-ec31da29995d33).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L78)

<a id="op-4f41adc5244b95"></a>
### Sales Order.update project

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_update_project`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**State and service calls** call db\_update on project.

**Explicit results** no value.

**Local steps**

- If Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”) differs from “Each Transaction”.
  - Return no value.
- If self.project.
  - Set project from Platform.get\_lazy\_doc(“Project”, self.project).
  - Evaluate project.update\_sales\_amount().
  - Evaluate project.db\_update().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1363)

<a id="op-07d1e9d51b6f8e"></a>
### Sales Order.check credit limit

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_check_credit_limit`

**Inputs** self.

**Local steps**

- If not is\_sales\_order\_credit\_check\_bypassed(self.customer, self.company).
  - Evaluate check\_credit\_limit(self.customer, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1342)

<a id="op-8e03460de90855"></a>
### Sales Order.check nextdoc docstatus

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_check_nextdoc_record_state`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Sales Invoice {0} must be deleted before cancelling this Sales Order”.format(“, ”.join(linked\_invoices)).

**Local steps**

- Set linked\_invoices from Platform.db.sql\_list(query text (SELECT, Sales Invoice), self.name).
- If linked\_invoices.
  - Set linked\_invoices from list of get\_link\_to\_form(“Sales Invoice”, si) for si drawn from linked\_invoices.
    - Draw si from linked\_invoices.
  - Call the validation error handler Platform.throw(translated “Sales Invoice {0} must be deleted before cancelling this Sales Order”.format(“, ”.join(linked\_invoices))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1343)

<a id="op-c58c6a6524f63d"></a>
### Sales Order.check modified date

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_check_modified_date`

**Inputs** self.

**Record and data access** read “Sales Order” via get\_value.

**State and service calls** execute a supplied database query.

**Explicit failure paths** validation helper — translated “{0} {1} has been modified. Please refresh.”.format(self.doctype, self.name).

**Local steps**

- Set mod\_db from Platform.db.get\_value(“Sales Order”, self.name, “modified”).
- Set date\_diff from Platform.db.sql(formatted text select TIMEDIFF('{mod\_db}', '{cstr(self.modified)}')).
- If (date\_diff and date\_diff at 0 at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in date\_diff → date\_diff at 0 at 0.
  - Call the validation error handler Platform.throw(translated “{0} {1} has been modified. Please refresh.”.format(self.doctype, self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L72)

<a id="op-91848f7de91a40"></a>
### Sales Order.update status

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_update_status`

**Inputs** self, status.

**Local steps**

- Bind dependencies validate\_reopen\_against\_blanket\_order.
- Evaluate self.check\_modified\_date().
- If status equals “Closed”.
  - Evaluate self.validate\_no\_reserved\_stock().
- If (status differs from “Closed” and self.status equals “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status differs from “Closed” → self.status equals “Closed”.
  - Evaluate validate\_reopen\_against\_blanket\_order(self).
- Evaluate self.set\_status(update = true, status = status).
- If (status equals “Draft” and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status equals “Draft” → self.docstatus equals 1.
  - Evaluate self.check\_credit\_limit().
- Evaluate self.update\_reserved\_qty().
- Evaluate self.update\_subcontracting\_order\_status().
- Evaluate self.notify\_update().
- Evaluate clear\_doctype\_notifications(self).
- Evaluate self.update\_blanket\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check modified date](operations-016.md#op-c58c6a6524f63d), [validate no reserved stock](operations-016.md#op-67e978f1a52d00), [check credit limit](operations-016.md#op-07d1e9d51b6f8e), [update reserved qty](operations-016.md#op-37dcf68b41e0b9), [update subcontracting order status](operations-016.md#op-ca103df6185a48).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1365)

<a id="op-67e978f1a52d00"></a>
### Sales Order.validate no reserved stock

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_validate_no_reserved_stock`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Sales Order {0} has reserved stock. Unreserve it before closing.”.format(Platform.bold(self.name)).

**Local steps**

- If has\_reserved\_stock(self.doctype, self.name).
  - Call the validation error handler Platform.throw(translated “Sales Order {0} has reserved stock. Unreserve it before closing.”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L86)

<a id="op-ca103df6185a48"></a>
### Sales Order.update subcontracting order status

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_update_subcontracting_order_status`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order” via get\_all.

**Local steps**

- Bind dependencies update\_scio\_status.
- If self.is\_subcontracted.
  - For each scio in Platform.get\_all(“Subcontracting Inward Order”, mapping(“sales\_order” → self.name, “docstatus” → 1), pluck = “name”).
    - Evaluate update\_scio\_status(scio, “Closed” when self.status equals “Closed”, otherwise no value).
      - Value choice on self.status equals “Closed” — true gives “Closed”, false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L84)

<a id="op-37dcf68b41e0b9"></a>
### Sales Order.update reserved qty

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_update_reserved_quantity`

**Inputs** self, so\_item\_rows = no value.

**Local steps**

- Set item\_wh\_list from list().
- Bind local operation \_valid\_for\_reserve for subsequent calls.
- For each d in self.get(“items”).
  - If ((not so\_item\_rows or d.name belongs to so\_item\_rows) and not d.delivered\_by\_supplier).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not so\_item\_rows or d.name belongs to so\_item\_rows) → not d.delivered\_by\_supplier.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not so\_item\_rows → d.name belongs to so\_item\_rows.
    - If self.has\_product\_bundle(d.item\_code).
      - For each p in self.get(“packed\_items”).
        - If (p.parent\_detail\_docname equals d.name and p.parent\_item equals d.item\_code).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in p.parent\_detail\_docname equals d.name → p.parent\_item equals d.item\_code.
          - Evaluate \_valid\_for\_reserve(p.item\_code, p.warehouse).
    - Otherwise.
      - Evaluate \_valid\_for\_reserve(d.item\_code, d.warehouse).
- For each tuple(item\_code, warehouse) in item\_wh\_list.
  - Evaluate update\_bin\_qty(item\_code, warehouse, mapping(“reserved\_qty” → get\_reserved\_qty(item\_code, warehouse))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1364)

<a id="op-0c5dfb4cbf4a0f"></a>
### Sales Order.update reserved qty.valid for reserve

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_update_reserved_qty_valid_for_reserve`

**Inputs** item\_code, warehouse.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- If (item\_code and warehouse and list(item\_code, warehouse) does not belong to item\_wh\_list and Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_code → warehouse → list(item\_code, warehouse) does not belong to item\_wh\_list → Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”).
  - Evaluate item\_wh\_list.append(list(item\_code, warehouse)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L83)

<a id="op-f43dbd0ca1caf8"></a>
### Sales Order.on update after submit

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.check\_credit\_limit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check credit limit](operations-016.md#op-07d1e9d51b6f8e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L85) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1353)

<a id="op-4ed5c922e83eb6"></a>
### Sales Order.before update after submit

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate super().before\_update\_after\_submit().
- Evaluate self.validate\_po().
- Evaluate self.validate\_drop\_ship().
- Evaluate self.validate\_supplier\_after\_submit().
- Evaluate self.validate\_delivery\_date().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate po](operations-015.md#op-cacd7f6caf9ea5), [validate drop ship](operations-015.md#op-fb048507fa996f), [validate supplier after submit](operations-016.md#op-4d0608f61d318e), [validate delivery date](operations-015.md#op-89d2f5a35547bc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1338)

<a id="op-4d0608f61d318e"></a>
### Sales Order.validate supplier after submit

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_supplier_after_submit`

**Inputs** self.

**Record and data access** read “Sales Order Item” via get\_value.

**Explicit failure paths** validation helper — whitespace '\\n'.join(exc\_list).

**Local steps**

- Set exc\_list from list().
- For each item in self.items.
  - If item.supplier.
    - Set supplier from Platform.db.get\_value(“Sales Order Item”, item.name, “supplier”).
    - If (item.ordered\_qty &gt; 0.0 and item.supplier differs from supplier).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.ordered\_qty &gt; 0.0 → item.supplier differs from supplier.
      - Evaluate exc\_list.append(translated “Row #{0}: Not allowed to change Supplier as Purchase Order already exists”.format(item.idx)).
- If exc\_list.
  - Call the validation error handler Platform.throw(whitespace '\\n'.join(exc\_list)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L1372) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1374)

<a id="op-fbdfd9c8e74874"></a>
### Sales Order.update delivery status

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_update_delivery_status`

**Inputs** self.

**State and service calls** call db\_set on item · call db\_set on self.

**Local steps**

- Set tuple(tot\_qty, delivered\_qty) from tuple(0.0, 0.0).
- For each item in self.items.
  - If item.delivered\_by\_supplier.
    - Evaluate item.db\_set(“delivered\_qty”, self.get\_drop\_ship\_delivered\_qty(item), update\_modified = false).
  - Update delivered\_qty using + min(item.delivered\_qty, item.qty).
  - Update tot\_qty using + item.qty.
- If tot\_qty differs from 0.
  - Evaluate self.db\_set(“per\_delivered”, (flt((delivered\_qty ÷ tot\_qty)) × 100), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get drop ship delivered qty](operations-016.md#op-373b2bef361674).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1359)

<a id="op-373b2bef361674"></a>
### Sales Order.get drop ship delivered qty

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_get_drop_ship_delivered_qty`

**Inputs** self, item.

**Declared result** float.

**Explicit results** flt((flt(received\_stock\_qty) ÷ flt((item.conversion\_factor or 1))), item.precision(“delivered\_qty”)).

**Local steps**

- Set po\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set received\_stock\_qty from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i … at 0.
- Return flt((flt(received\_stock\_qty) ÷ flt((item.conversion\_factor or 1))), item.precision(“delivered\_qty”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L77)

<a id="op-9aa3041f15df7c"></a>
### Sales Order.update picking status

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_update_picking_status`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value · read “Stock Settings” via get\_single\_value.

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Total Picked Quantity {0} is more than ordered qty {1}. You can set the Over Picking Allowance in Stock Settings.”.format(total\_picked\_qty, total\_qty).

**Local steps**

- Set total\_picked\_qty from 0.0.
- Set total\_qty from 0.0.
- Set per\_picked from 0.0.
- For each so\_item in self.items.
  - If (cint(Platform.get\_cached\_value(“Item”, so\_item.item\_code, “is\_stock\_item”)) or self.has\_product\_bundle(so\_item.item\_code)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.get\_cached\_value(“Item”, so\_item.item\_code, “is\_stock\_item”)) → self.has\_product\_bundle(so\_item.item\_code).
    - Update total\_picked\_qty using + flt(so\_item.picked\_qty).
    - Update total\_qty using + flt(so\_item.stock\_qty).
- If (total\_picked\_qty and total\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_picked\_qty → total\_qty.
  - Set per\_picked from ((total\_picked\_qty ÷ total\_qty) × 100).
  - Set pick\_percentage from Platform.get\_single\_value(“Stock Settings”, “over\_picking\_allowance”).
  - If pick\_percentage.
    - Update total\_qty using + (flt(total\_qty) × (pick\_percentage ÷ 100)).
  - If total\_picked\_qty &gt; total\_qty.
    - Call the validation error handler Platform.throw(translated “Total Picked Quantity {0} is more than ordered qty {1}. You can set the Over Picking Allowance in Stock Settings.”.format(total\_picked\_qty, total\_qty)).
- Evaluate self.db\_set(“per\_picked”, flt(per\_picked), update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, so\_item.item\_code, “is\_stock\_item”), Platform.get\_single\_value(“Stock Settings”, “over\_picking\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1361)

<a id="op-6387943a138686"></a>
### Sales Order.set indicator

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_set_indicator`

**Inputs** self.

**Local steps**

- Set self.indicator\_color from mapping(“Draft” → “red”, “On Hold” → “orange”, “To Deliver and Bill” → “orange”, “To Bill” → “orange”, …).get(self.status, “blue”).
- Set self.indicator\_title from translated self.status.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1357)

<a id="op-6b04352ece4d23"></a>
### Sales Order.on recurring

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_on_recurring`

**Inputs** self, reference\_doc, auto\_repeat\_doc.

**Record and data access** read “Sales Order Item” via get\_value.

**Local steps**

- Evaluate super().on\_recurring(reference\_doc, auto\_repeat\_doc).
- Bind local operation \_get\_delivery\_date for subsequent calls.
- Evaluate self.set(“delivery\_date”, \_get\_delivery\_date(reference\_doc.delivery\_date, reference\_doc.transaction\_date, self.transaction\_date)).
- For each d in self.get(“items”).
  - Set reference\_delivery\_date from Platform.db.get\_value(“Sales Order Item”, mapping(“parent” → reference\_doc.name, “item\_code” → d.item\_code, “idx” → d.idx), “delivery\_date”).
  - Evaluate d.set(“delivery\_date”, \_get\_delivery\_date(reference\_delivery\_date, reference\_doc.transaction\_date, self.transaction\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1350)

<a id="op-d673576279aaa7"></a>
### Sales Order.on recurring.get delivery date

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_on_recurring_get_delivery_date`

**Inputs** ref\_doc\_delivery\_date, red\_doc\_transaction\_date, transaction\_date.

**Explicit results** delivery\_date.

**Local steps**

- Set delivery\_date from auto\_repeat\_doc.get\_next\_schedule\_date(schedule\_date = ref\_doc\_delivery\_date).
- If delivery\_date ≤ transaction\_date.
  - Set delivery\_date\_diff from Platform.utils.date\_diff(ref\_doc\_delivery\_date, red\_doc\_transaction\_date).
  - Set delivery\_date from Platform.utils.add\_days(transaction\_date, delivery\_date\_diff).
- Return delivery\_date.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L2343) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1351)

<a id="op-862564c4d92f67"></a>
### Sales Order.validate serial no based delivery

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_validate_serial_number_based_delivery`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value · read “BOM” via exists.

**Explicit failure paths** validation helper — translated “Cannot ensure delivery by Serial No as Item {0} is added with and without Ensure Delivery by Serial No.”.format(item.item\_code) · validation helper — translated “Item {0} has no Serial No. Only serialized items can have delivery based on Serial No”.format(item.item\_code) · validation helper — translated “No active BOM found for item {0}. Delivery by Serial No cannot be ensured”.format(item.item\_code).

**Local steps**

- Set reserved\_items from list().
- Set normal\_items from list().
- For each item in self.items.
  - If item.ensure\_delivery\_based\_on\_produced\_serial\_no.
    - If item.item\_code belongs to normal\_items.
      - Call the validation error handler Platform.throw(translated “Cannot ensure delivery by Serial No as Item {0} is added with and without Ensure Delivery by Serial No.”.format(item.item\_code)).
    - If item.item\_code does not belong to reserved\_items.
      - If not Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”).
        - Call the validation error handler Platform.throw(translated “Item {0} has no Serial No. Only serialized items can have delivery based on Serial No”.format(item.item\_code)).
      - If not Platform.db.exists(“BOM”, mapping(“item” → item.item\_code, “is\_active” → 1)).
        - Call the validation error handler Platform.throw(translated “No active BOM found for item {0}. Delivery by Serial No cannot be ensured”.format(item.item\_code)).
    - Evaluate reserved\_items.append(item.item\_code).
  - Otherwise.
    - Evaluate normal\_items.append(item.item\_code).
  - If (not item.ensure\_delivery\_based\_on\_produced\_serial\_no and item.item\_code belongs to reserved\_items).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.ensure\_delivery\_based\_on\_produced\_serial\_no → item.item\_code belongs to reserved\_items.
    - Call the validation error handler Platform.throw(translated “Cannot ensure delivery by Serial No as Item {0} is added with and without Ensure Delivery by Serial No.”.format(item.item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “has\_serial\_no”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0643.json#L2525) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1373)

<a id="op-61d1c840289423"></a>
### Sales Order.validate reserved stock

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_validate_reserved_stock`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Row #{0}: Stock cannot be reserved for the Item {1} as its delivery is ensured based on the produced Serial  …”.format(item.idx, Platform.bold(item.item\_code)).

**Local steps**

- Evaluate clear\_reserve\_stock\_if\_disabled(self).
- Set enable\_stock\_reservation from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
- For each item in self.items.
  - If (item.reserve\_stock and (not enable\_stock\_reservation or not cint(item.is\_stock\_item))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.reserve\_stock → (not enable\_stock\_reservation or not cint(item.is\_stock\_item)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not enable\_stock\_reservation → not cint(item.is\_stock\_item).
    - Set item.reserve\_stock from 0.
  - If item.ensure\_delivery\_based\_on\_produced\_serial\_no.
    - If not enable\_stock\_reservation.
      - Set item.ensure\_delivery\_based\_on\_produced\_serial\_no from 0.
    - Otherwise.
      - If item.reserve\_stock.
        - Set item.reserve\_stock from 0.
        - Evaluate Platform.msgprint(translated “Row #{0}: Stock cannot be reserved for the Item {1} as its delivery is ensured based on the produced Serial  …”.format(item.idx, Platform.bold(item.item\_code)), title = transl ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L87)

<a id="op-ce485f3326c4fd"></a>
### Sales Order.has unreserved stock

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_has_unreserved_stock`

**Inputs** self, table\_name = “items”.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**Explicit results** data.

**Local steps**

- Set reserved\_qty\_details from get\_sre\_reserved\_qty\_details\_for\_voucher(“Sales Order”, self.name).
- Set data from mapping().
- For each item in self.get(table\_name).
  - If not item.get(“reserve\_stock”).
    - Continue with the next iteration or loop test.
  - Set unreserved\_qty from get\_unreserved\_qty(item, reserved\_qty\_details).
  - If unreserved\_qty &gt; 0.
    - Set data at item.name from unreserved\_qty.
- Return data.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1347)

<a id="op-2522b35c3ee92c"></a>
### Sales Order.create stock reservation entries

`operation_enterprise_selling_record_definitions_sales_order_business_behavior_sales_order_create_stock_reservation_entries`

**Inputs** self, items\_details = no value, from\_voucher\_type = no value, notify = true.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate self.\_create\_stock\_reservation\_entries(items\_details, from\_voucher\_type, notify).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create stock reservation entries](operations-016.md#op-f39d24086207e0).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1345)

<a id="op-f39d24086207e0"></a>
### Sales Order.create stock reservation entries

`operation_enterprise_binding_enterprise_selling_doctype_sales_order_sales_order_salesorder_create_stock_reservation_entries`

**Inputs** self, items\_details = no value, from\_voucher\_type = no value, notify = true.

**Declared result** no value.

**Record and data access** read “Sales Order Item” via exists.

**State and service calls** msgprint with translated “Stock Reservation Entries Created”.

**Local steps**

- Bind dependencies create\_stock\_reservation\_entries.
- Set packed\_items from list().
- If items\_details.
  - For each item in items\_details.
    - If not Platform.db.exists(“Sales Order Item”, item.get(“sales\_order\_item”)).
      - Evaluate packed\_items.append(item).
  - Set packed\_item\_warehouses from mapping of d.name → d.warehouse for d drawn from self.packed\_items.
    - Draw d from self.packed\_items.
  - For each item in packed\_items.
    - Evaluate items\_details.remove(item).
    - Set item at “qty” from item.pop(“qty\_to\_reserve”).
    - Set item at “from\_voucher\_type” from from\_voucher\_type.
    - If not from\_voucher\_type.
      - Set item at “warehouse” from packed\_item\_warehouses.get(item.get(“sales\_order\_item”), item.get(“warehouse”)).
    - Set picked\_bundle from item.pop(“serial\_and\_batch\_bundle”, no value).
    - If picked\_bundle.
      - Set item at “serial\_and\_batch\_bundles” from list(picked\_bundle).
- Set sre\_count from 0.
- If items\_details differs from list().
  - Set sre\_count from create\_stock\_reservation\_entries(sales\_order = self, items\_details = items\_details, from\_voucher\_type = from\_voucher\_type, notify = notify).
- Set items from list().
- If packed\_items.
  - Set items from packed\_items.
- Otherwise.
  - If not items\_details.
    - Set items from list of item for item drawn from self.packed\_items where item.reserve\_stock.
      - Draw item from self.packed\_items, keep a combination only if (item.reserve\_stock).
- If items.
  - Bind dependencies StockReservation.
  - Set stock\_reservation from StockReservation(doc = self, items = items).
  - Set stock\_reservation.table\_name from “packed\_items”.
  - Set stock\_reservation.qty\_field from “qty”.
  - Set is\_sre\_created from stock\_reservation.make\_stock\_reservation\_entries().
  - If (notify and is\_sre\_created and not sre\_count).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in notify → is\_sre\_created → not sre\_count.
    - Evaluate Platform.msgprint(translated “Stock Reservation Entries Created”, alert = true, indicator = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L73)
