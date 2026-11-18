# Shared transaction rules · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock controller

<a id="op-843de2b14cddae"></a>
### Stock Controller.validate qi presence

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_qi_presence`

**Inputs** self, row.

**State and service calls** msgprint with msg.

**Explicit failure paths** validation helper with QualityInspectionRequiredError — msg.

**Local steps**

- If not row.quality\_inspection.
  - Set msg from translated “Row #{0}: Quality Inspection is required for Item {1}”.format(row.idx, Platform.bold(row.item\_code)).
  - <a id="op-843de2b14cddae-guard-7"></a>If self.docstatus equals 1.
    - Call the validation error handler Platform.throw(msg, title = translated “Inspection Required”, exc = QualityInspectionRequiredError).
  - Otherwise.
    - Evaluate Platform.msgprint(msg, title = translated “Inspection Required”, indicator = “blue”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 1, self.docstatus = 1 (submitted) selects the branch that calls the validation-error handler with msg. With self.docstatus = 0 (draft), the alternative requests a message with msg. [Local guard](#op-843de2b14cddae-guard-7)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L419)

<a id="op-7894a202e13ffd"></a>
### Stock Controller.validate qi submission

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_qi_submission`

**Inputs** self, row.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Quality Inspection” via get\_value.

**State and service calls** msgprint with msg.

**Explicit failure paths** validation helper with QualityInspectionNotSubmittedError — msg.

**Local steps**

- Set action from Platform.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_not\_submitted”).
- Set qa\_docstatus from Platform.db.get\_value(“Quality Inspection”, row.quality\_inspection, “docstatus”).
- If qa\_docstatus differs from 1.
  - Set link from Platform.utils.get\_link\_to\_form(“Quality Inspection”, row.quality\_inspection).
  - Set msg from translated “Row #{0}: Quality Inspection {1} is not submitted for the item: {2}”.format(row.idx, link, row.item\_code).
  - If action equals “Stop”.
    - Call the validation error handler Platform.throw(msg, title = translated “Inspection Submission”, exc = QualityInspectionNotSubmittedError).
  - Otherwise.
    - Evaluate Platform.msgprint(msg, alert = true, indicator = “orange”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_not\_submitted”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L421)

<a id="op-e0ea7b8e0768a9"></a>
### Stock Controller.validate qi rejection

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_qi_rejection`

**Inputs** self, row.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Quality Inspection” via get\_value.

**State and service calls** msgprint with msg.

**Explicit failure paths** validation helper with QualityInspectionRejectedError — msg.

**Local steps**

- Set action from Platform.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_rejected”).
- Set qa\_status from Platform.db.get\_value(“Quality Inspection”, row.quality\_inspection, “status”).
- If qa\_status differs from “Accepted”.
  - Set link from Platform.utils.get\_link\_to\_form(“Quality Inspection”, row.quality\_inspection).
  - Set msg from translated “Row #{0}: Quality Inspection {1} was rejected for item {2}”.format(row.idx, link, row.item\_code).
  - If action equals “Stop”.
    - Call the validation error handler Platform.throw(msg, title = translated “Inspection Rejected”, exc = QualityInspectionRejectedError).
  - Otherwise.
    - Evaluate Platform.msgprint(msg, alert = true, indicator = “orange”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “action\_if\_quality\_inspection\_is\_rejected”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L420)

<a id="op-09600cf51a0364"></a>
### Stock Controller.update blanket order

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_update_blanket_order`

**Inputs** self, extra\_blanket\_orders = tuple().

**Record and data access** resolve a document from “Blanket Order” via get\_doc.

**Local steps**

- Set blanket\_orders from set of d.blanket\_order for d drawn from self.items where d.blanket\_order.
  - Draw d from self.items, keep a combination only if (d.blanket\_order).
- For each blanket\_order in sorted(blanket\_orders.union(extra\_blanket\_orders)).
  - Evaluate Platform.get\_doc(“Blanket Order”, blanket\_order, for\_update = true).update\_ordered\_qty().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L656)

<a id="op-cda5158b267171"></a>
### Stock Controller.validate customer provided item

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_validate_customer_provided_item`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- For each d in self.get(“items”).
  - If Platform.get\_cached\_value(“Item”, d.item\_code, “is\_customer\_provided\_item”).
    - Set d.allow\_zero\_valuation\_rate from 1.

If control reaches the end, it returns no value.

**Derived worked case from the contract** With customer-provided part C and ordinary part D, both initially disallowing zero valuation, only C becomes eligible.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “is\_customer\_provided\_item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0442.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L662) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-56e788a0c17f36"></a>
### Stock Controller.set rate of stock uom

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_set_rate_of_stock_unit_of_measure`

**Inputs** self.

**Local steps**

- If self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Purchase Order”, “Sales Invoice”, …).
  - For each d in self.get(“items”).
    - Set d.stock\_uom\_rate from (d.rate ÷ (d.conversion\_factor or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.conversion\_factor → 1.

If control reaches the end, it returns no value.

**Derived worked case from the contract** A case at 120 with 12 stock units per case gives 10 per stock unit. With conversion factor zero, the row keeps 120 as the stock-unit rate.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0442.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L652) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-e060badbb7138e"></a>
### Stock Controller.validate internal transfer

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_internal_transfer`

**Inputs** self.

**Local steps**

- If self.doctype belongs to tuple(“Sales Invoice”, “Delivery Note”, “Purchase Invoice”, “Purchase Receipt”).
  - If self.is\_internal\_transfer().
    - Evaluate self.validate\_in\_transit\_warehouses().
    - Evaluate self.validate\_multi\_currency().
    - Evaluate self.validate\_packed\_items().
    - If (self.get(“is\_internal\_supplier”) and self.docstatus equals 1 and not self.get(“is\_return”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_internal\_supplier”) → self.docstatus equals 1 → not self.get(“is\_return”).
      - Evaluate self.validate\_internal\_transfer\_qty().
  - Otherwise.
    - Evaluate self.validate\_internal\_transfer\_warehouse().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate in transit warehouses](operations-026.md#op-bafeac00c93cff), [validate multi currency](operations-026.md#op-7a2942571e0360), [validate packed items](operations-026.md#op-3fdaaa99a6666b), [validate internal transfer qty](operations-026.md#op-fc8706ea88a419), [validate internal transfer warehouse](operations-026.md#op-a8dcdbead1e2f5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L409)

<a id="op-a8dcdbead1e2f5"></a>
### Stock Controller.validate internal transfer warehouse

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_internal_transfer_warehouse`

**Inputs** self.

**Local steps**

- For each row in self.items.
  - If row.get(“target\_warehouse”).
    - Set row.target\_warehouse from no value.
  - If row.get(“from\_warehouse”).
    - Set row.from\_warehouse from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1171) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L411)

<a id="op-bafeac00c93cff"></a>
### Stock Controller.validate in transit warehouses

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_in_transit_warehouses`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Target Warehouse is mandatory for internal transfers”.format(item.idx) · validation helper — translated “Row {0}: From Warehouse is mandatory for internal transfers”.format(item.idx).

**Local steps**

- If (self.docstatus equals 0 and self.flags.ignore\_mandatory).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 0 → self.flags.ignore\_mandatory.
  - Return no value.
- If ((self.doctype equals “Sales Invoice” and self.get(“update\_stock”)) or self.doctype equals “Delivery Note”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.doctype equals “Sales Invoice” and self.get(“update\_stock”)) → self.doctype equals “Delivery Note”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.get(“update\_stock”).
  - For each item in self.get(“items”).
    - If not item.target\_warehouse.
      - Call the validation error handler Platform.throw(translated “Row {0}: Target Warehouse is mandatory for internal transfers”.format(item.idx)).
- If ((self.doctype equals “Purchase Invoice” and self.get(“update\_stock”)) or self.doctype equals “Purchase Receipt”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.doctype equals “Purchase Invoice” and self.get(“update\_stock”)) → self.doctype equals “Purchase Receipt”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → self.get(“update\_stock”).
  - For each item in self.get(“items”).
    - If not item.from\_warehouse.
      - Call the validation error handler Platform.throw(translated “Row {0}: From Warehouse is mandatory for internal transfers”.format(item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1168) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L408)

<a id="op-7a2942571e0360"></a>
### Stock Controller.validate multi currency

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_multi_currency`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Internal transfers can only be done in company's default currency”.

**Local steps**

- If self.currency differs from self.company\_currency.
  - Call the validation error handler Platform.throw(translated “Internal transfers can only be done in company's default currency”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L415)

<a id="op-3fdaaa99a6666b"></a>
### Stock Controller.validate packed items

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_packed_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Packed Items cannot be transferred internally”.

**Local steps**

- If (self.doctype equals “Sales Invoice” and self.get(“packed\_items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.get(“packed\_items”).
  - Call the validation error handler Platform.throw(translated “Packed Items cannot be transferred internally”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L417)

<a id="op-fc8706ea88a419"></a>
### Stock Controller.validate internal transfer qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_internal_transfer_qty`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with OverAllowanceError — translated “For Item {0} cannot be received more than {1} qty against the {2} {3}”.format(bold(key at 1), bold(flt(transferred\_qty, precision)), bold(parent\_doctype), get\_link\_to\_form(parent\_doctype, self. ….

**Local steps**

- If self.doctype does not belong to list(“Purchase Invoice”, “Purchase Receipt”).
  - Return no value.
- Set self.\_\_inter\_company\_reference from self.get\_inter\_company\_reference().
- Set item\_wise\_transfer\_qty from self.get\_item\_wise\_inter\_transfer\_qty().
- If not item\_wise\_transfer\_qty.
  - Return no value.
- Set item\_wise\_received\_qty from self.get\_item\_wise\_inter\_received\_qty().
- Set precision from Platform.get\_precision((self.doctype + “ Item”), “qty”).
- Set over\_receipt\_allowance from Platform.get\_single\_value(“Stock Settings”, “over\_delivery\_receipt\_allowance”).
- Set parent\_doctype from mapping(“Purchase Receipt” → “Delivery Note”, “Purchase Invoice” → “Sales Invoice”).get(self.doctype).
- For each tuple(key, transferred\_qty) in item\_wise\_transfer\_qty.items().
  - Set recevied\_qty from flt(item\_wise\_received\_qty.get(key), precision).
  - If over\_receipt\_allowance.
    - Set transferred\_qty from (transferred\_qty + flt(((transferred\_qty × over\_receipt\_allowance) ÷ 100), precision)).
  - If recevied\_qty &gt; flt(transferred\_qty, precision).
    - Bind dependencies OverAllowanceError.
    - Call the validation error handler Platform.throw(translated “For Item {0} cannot be received more than {1} qty against the {2} {3}”.format(bold(key at 1), bold(flt(transferred\_qty, precision)), bold(parent\_doctype), get\_link\_to\_form(parent ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get inter company reference](operations-026.md#op-b6947054586f87), [get item wise inter transfer qty](operations-026.md#op-1de5c13a3a6c39), [get item wise inter received qty](operations-026.md#op-5f921818b419bb).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “over\_delivery\_receipt\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1170) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L410)

<a id="op-b6947054586f87"></a>
### Stock Controller.get inter company reference

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_inter_company_reference`

**Inputs** self.

**Record and data access** read “Purchase Invoice” via get\_value.

**Explicit results** self.get(“inter\_company\_reference”) · Platform.db.get\_value(“Purchase Invoice”, self.return\_against, “inter\_company\_invoice\_reference”) · self.get(“inter\_company\_invoice\_reference”).

**Local steps**

- If self.doctype equals “Purchase Receipt”.
  - Return self.get(“inter\_company\_reference”).
- If self.get(“is\_return”).
  - Return Platform.db.get\_value(“Purchase Invoice”, self.return\_against, “inter\_company\_invoice\_reference”).
- Return self.get(“inter\_company\_invoice\_reference”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L380)

<a id="op-1de5c13a3a6c39"></a>
### Stock Controller.get item wise inter transfer qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_item_wise_inter_transfer_qty`

**Inputs** self.

**Explicit results** item\_wise\_transfer\_qty.

**Local steps**

- Set parent\_doctype from mapping(“Purchase Receipt” → “Delivery Note”, “Purchase Invoice” → “Sales Invoice”).get(self.doctype).
- Set child\_doctype from (parent\_doctype + “ Item”).
- Set parent\_tab from Platform.qb.DocType(parent\_doctype).
- Set child\_tab from Platform.qb.DocType(child\_doctype).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(child\_tab.name, child\_tab.item\_code, child\_tab.qty ….
- If parent\_doctype equals “Delivery Note”.
  - Set query from query.select(child\_tab.returned\_qty, child\_tab.stock\_qty, child\_tab.conversion\_factor).
- Set data from query.run(as\_dict = true).
- Set item\_wise\_transfer\_qty from defaultdict(float).
- For each row in data.
  - Set returned\_qty from (flt(row.get(“returned\_qty”)) ÷ (flt(row.get(“conversion\_factor”)) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.get(“conversion\_factor”)) → 1.
  - Update item\_wise\_transfer\_qty at tuple(row.name, row.item\_code) using + (flt(row.qty) − returned\_qty).
- If parent\_doctype equals “Delivery Note”.
  - Evaluate self.add\_component\_transfer\_qty(item\_wise\_transfer\_qty, self.\_\_inter\_company\_reference, data).
- Return item\_wise\_transfer\_qty.

**Methods declared on this owner** [add component transfer qty](operations-026.md#op-ff29eb943e1bbb).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L382)

<a id="op-ff29eb943e1bbb"></a>
### Stock Controller.add component transfer qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_add_component_transfer_qty`

**Inputs** self, item\_wise\_transfer\_qty, delivery\_note, bundle\_rows.

**Record and data access** read “Packed Item” via get\_all.

**Local steps**

- Bind dependencies get\_pending\_component\_qty.
- Set bundle\_rows from mapping of row.name → row for row drawn from bundle\_rows.
  - Draw row from bundle\_rows.
- For each packed in Platform.get\_all(“Packed Item”, filters = mapping(“parent” → delivery\_note, “parenttype” → “Delivery Note”), fields = list(“name”, “item\_code”, “qty”, “parent\_detail\_docname”)).
  - If bundle\_row bound to bundle\_rows.get(packed.parent\_detail\_docname).
    - Evaluate item\_wise\_transfer\_qty.pop(tuple(bundle\_row.name, bundle\_row.item\_code), no value).
    - Update item\_wise\_transfer\_qty at tuple(packed.name, packed.item\_code) using + get\_pending\_component\_qty(packed, bundle\_row).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L368)

<a id="op-5f921818b419bb"></a>
### Stock Controller.get item wise inter received qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_item_wise_inter_received_qty`

**Inputs** self.

**Explicit results** item\_wise\_received\_qty.

**Local steps**

- Bind dependencies get\_inter\_company\_items.
- If self.doctype equals “Purchase Invoice”.
  - Set tuple(reference\_field, item\_reference\_field) from tuple(“inter\_company\_invoice\_reference”, “sales\_invoice\_item”).
  - Set fields from list(“item\_code”, “qty”).
- Otherwise.
  - Set tuple(reference\_field, item\_reference\_field) from tuple(“inter\_company\_reference”, “delivery\_note\_item”).
  - Set fields from list(“item\_code”, “qty”, “delivery\_note\_packed\_item”).
- Set other\_items from get\_inter\_company\_items(self.doctype, mapping(reference\_field → self.\_\_inter\_company\_reference, “name” → tuple(“!=”, self.name)), item\_reference\_field, fields).
- Set own\_items from self.items when self.docstatus equals 1, otherwise list().
  - Value choice on self.docstatus equals 1 — true gives self.items, false gives list().
- Set item\_wise\_received\_qty from defaultdict(float).
- For each row in list(expanded other\_items, expanded own\_items).
  - Set reference from (row.get(“delivery\_note\_packed\_item”) or row.get(item\_reference\_field)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“delivery\_note\_packed\_item”) → row.get(item\_reference\_field).
  - Update item\_wise\_received\_qty at tuple(reference, row.item\_code) using + flt(row.qty).
- Return item\_wise\_received\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L381)

<a id="op-a3e3163b2adde2"></a>
### Stock Controller.validate putaway capacity

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_putaway_capacity`

**Inputs** self.

**Record and data access** read “Putaway Rule” via get\_all · read “Putaway Rule” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- Bind dependencies \_get\_available\_putaway\_capacity.
- Set valid\_doctype from self.doctype belongs to tuple(“Purchase Receipt”, “Stock Entry”, “Purchase Invoice”, “Stock Reconciliation”).
- If not Platform.get\_all(“Putaway Rule”, limit = 1).
  - Return no value.
- If (self.doctype equals “Purchase Invoice” and self.get(“update\_stock”) equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → self.get(“update\_stock”) equals 0.
  - Set valid\_doctype from false.
- If valid\_doctype.
  - Set rule\_map from defaultdict(dict).
  - For each item in self.get(“items”).
    - Set warehouse\_field from “t\_warehouse” when self.doctype equals “Stock Entry”, otherwise “warehouse”.
      - Value choice on self.doctype equals “Stock Entry” — true gives “t\_warehouse”, false gives “warehouse”.
    - Set rule from Platform.db.get\_value(“Putaway Rule”, mapping(“item\_code” → item.get(“item\_code”), “warehouse” → item.get(warehouse\_field)), list(“stock\_capacity”, “name”, “disable”), as\_dict = true).
    - If rule.
      - If rule.get(“disabled”).
        - Continue with the next iteration or loop test.
      - If self.doctype equals “Stock Reconciliation”.
        - Set stock\_qty from flt(item.qty).
      - Otherwise.
        - Set stock\_qty from flt(item.transfer\_qty) when self.doctype equals “Stock Entry”, otherwise flt(item.stock\_qty).
          - Value choice on self.doctype equals “Stock Entry” — true gives flt(item.transfer\_qty), false gives flt(item.stock\_qty).
      - Set rule\_name from rule.get(“name”).
      - If not rule\_map at rule\_name.
        - Set rule\_map at rule\_name at “warehouse” from item.get(warehouse\_field).
        - Set rule\_map at rule\_name at “item” from item.get(“item\_code”).
        - Set rule\_map at rule\_name at “qty\_put” from 0.
        - Set rule\_map at rule\_name at “capacity” from rule.stock\_capacity when self.doctype equals “Stock Reconciliation”, otherwise \_get\_available\_putaway\_capacity(rule\_name).
          - Value choice on self.doctype equals “Stock Reconciliation” — true gives rule.stock\_capacity, false gives \_get\_available\_putaway\_capacity(rule\_name).
      - Update rule\_map at rule\_name at “qty\_put” using + flt(stock\_qty).
  - For each tuple(rule, values) in rule\_map.items().
    - If flt(values at “qty\_put”) &gt; flt(values at “capacity”).
      - Set message from self.prepare\_over\_receipt\_message(rule, values).
      - Call the validation error handler Platform.throw(msg = message, title = translated “Over Receipt”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare over receipt message](operations-026.md#op-ef285f55c9779b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L418)

<a id="op-ef285f55c9779b"></a>
### Stock Controller.prepare over receipt message

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_prepare_over_receipt_message`

**Inputs** self, rule, values.

**Explicit results** message.

**Local steps**

- Set message from translated “{0} qty of Item {1} is being received into Warehouse {2} with capacity {3}.”.format(Platform.bold(values at “qty\_put”), Platform.bold(values at “item”), Platform.bold(values at “warehouse”), Pl ….
- Update message using + text in the contract.
- Set rule\_link from Platform.utils.get\_link\_to\_form(“Putaway Rule”, rule).
- Update message using + translated “Please adjust the qty or edit {0} to proceed.”.format(rule\_link).
- Return message.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1160) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L400)

<a id="op-0b8e02ead05fd1"></a>
### Stock Controller.repost future sle and gle

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_repost_future_stock_ledger_entry_and_general_ledger_entry`

**Inputs** self, force = false, via\_landed\_cost\_voucher = false.

**Record and data access** read “Stock Ledger Entry” via exists · read “Stock Reposting Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set args from Platform.\_dict(mapping(“posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, “voucher\_type” → self.doctype, “voucher\_no” → self.name, …)).
- If self.docstatus equals 2.
  - If not Platform.db.exists(“Stock Ledger Entry”, mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name)).
    - Return no value.
  - Set force from true.
- If (force or future\_sle\_exists(args, for\_update = true) or repost\_required\_for\_queue(self)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in force → future\_sle\_exists(args, for\_update = true) → repost\_required\_for\_queue(self).
  - Set item\_based\_reposting from Platform.get\_single\_value(“Stock Reposting Settings”, “item\_based\_reposting”).
  - If item\_based\_reposting.
    - Evaluate create\_item\_wise\_repost\_entries(voucher\_type = self.doctype, voucher\_no = self.name, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).
  - Otherwise.
    - Evaluate create\_repost\_item\_valuation\_entry(args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Reposting Settings”, “item\_based\_reposting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L973) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L650)

<a id="op-c1bdbfc0f25be8"></a>
### Stock Controller.update project consumed material cost

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_update_project_consumed_material_cost`

**Inputs** self.

**Local steps**

- Set projects from set(self.get(“project”), expanded generator of d.get(“project”) for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
- Evaluate update\_consumed\_material\_cost((projects − set(no value, empty text))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1165) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L405)

<a id="op-aa4501be16580a"></a>
### Stock Controller.add gl entry

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_add_general_ledger_entry`

**Inputs** self, gl\_entries, account, cost\_center, debit, credit, remarks, against\_account, debit\_in\_account\_currency = no value, credit\_in\_account\_currency = no value, account\_currency = no value, project = no value, voucher\_detail\_no = no value, item = no value, posting\_date = no value, dimensions = no value.

**Local steps**

- Set gl\_entry from mapping(“account” → account, “cost\_center” → cost\_center, “debit” → debit, “credit” → credit, …).
- If project.
  - Evaluate gl\_entry.update(mapping(“project” → project)).
- If voucher\_detail\_no.
  - Evaluate gl\_entry.update(mapping(“voucher\_detail\_no” → voucher\_detail\_no)).
- If debit\_in\_account\_currency.
  - Evaluate gl\_entry.update(mapping(“debit\_in\_account\_currency” → debit\_in\_account\_currency)).
- If credit\_in\_account\_currency.
  - Evaluate gl\_entry.update(mapping(“credit\_in\_account\_currency” → credit\_in\_account\_currency)).
- If posting\_date.
  - Evaluate gl\_entry.update(mapping(“posting\_date” → posting\_date)).
- If dimensions.
  - Evaluate gl\_entry.update(dimensions).
- Evaluate gl\_entries.append(self.get\_gl\_dict(gl\_entry, item = item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L951) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L630)

<a id="op-db6b66958e2a15"></a>
### Stock Controller.update stock reservation entries

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_update_stock_reservation_entries`

**Inputs** self.

**Record and data access** read “Subcontracting Order” via get\_value · resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call db\_update on entry · call db\_update on sre\_doc.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_delivered\_serial\_batch\_for\_reservation.
- Bind local operation get\_sre\_list for subsequent calls.
- Bind local operation get\_data\_map for subsequent calls.
- Set purpose from self.get(“purpose”).
- If (purpose equals “Subcontracting Delivery” or (purpose equals “Send to Subcontractor” and Platform.get\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”)) or (self.doctype equals “Sub ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in purpose equals “Subcontracting Delivery” → (purpose equals “Send to Subcontractor” and Platform.get\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”)) → (self.doctype equals “Subcontracting Receipt” and self.has\_reserved\_stock() and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in purpose equals “Send to Subcontractor” → Platform.get\_value(“Subcontracting Order”, self.subcontracting\_order, “reserve\_stock”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Subcontracting Receipt” → self.has\_reserved\_stock() → not self.is\_return.
  - Set data\_map from get\_data\_map().
  - If (purpose equals “Send to Subcontractor” and self.\_action equals “cancel”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in purpose equals “Send to Subcontractor” → self.\_action equals “cancel”.
    - Set rows from mapping of item.sco\_rm\_detail → item for item drawn from self.items where item.sco\_rm\_detail.
      - Draw item from self.items, keep a combination only if (item.sco\_rm\_detail).
    - Evaluate self.rebuild\_subcontracting\_transfers(mapping of row → get\_sre\_list(item) for tuple(row, item) drawn from rows.items()).
      - Draw tuple(row, item) from rows.items().
    - Return no value.
  - Set field from data\_map at (purpose or self.doctype) at “field”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in purpose → self.doctype.
  - For each item in self.get(data\_map at (purpose or self.doctype) at “table\_name”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in purpose → self.doctype.
    - Set sre\_list from get\_sre\_list(item).
    - If not sre\_list.
      - Continue with the next iteration or loop test.
    - Set qty from item.get(“transfer\_qty”, item.get(“consumed\_qty”)).
    - Set tuple(serial\_nos, batch\_qty) from get\_delivered\_serial\_batch\_for\_reservation(item).
    - For each sre in sre\_list.
      - <a id="op-db6b66958e2a15-guard-84"></a>If qty ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
      - Set sre\_doc from Platform.get\_doc(“Stock Reservation Entry”, sre).
      - Set working\_qty from 0.
      - If sre\_doc.reservation\_based\_on equals “Serial and Batch”.
        - If sre\_doc.has\_serial\_no.
          - For each entry in sre\_doc.sb\_entries.
            - Set is\_open from entry.qty &gt; entry.delivered\_qty when self.\_action equals “submit”, otherwise entry.delivered\_qty.
              - Value choice on self.\_action equals “submit” — true gives entry.qty &gt; entry.delivered\_qty, false gives entry.delivered\_qty.
            - If (entry.serial\_no belongs to serial\_nos and is\_open).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.serial\_no belongs to serial\_nos → is\_open.
              - Set entry.delivered\_qty from 1 when self.\_action equals “submit”, otherwise 0.
                - Value choice on self.\_action equals “submit” — true gives 1, false gives 0.
              - Evaluate entry.db\_update().
              - Update working\_qty using + 1.
              - Evaluate serial\_nos.remove(entry.serial\_no).
        - Otherwise.
          - For each entry in sre\_doc.sb\_entries.
            - If entry.batch\_no belongs to batch\_qty.
              - Set delivered\_qty from min((entry.qty − entry.delivered\_qty) when self.\_action equals “submit”, otherwise entry.delivered\_qty, batch\_qty at entry.batch\_no).
                - Value choice on self.\_action equals “submit” — true gives (entry.qty − entry.delivered\_qty), false gives entry.delivered\_qty.
              - Set entry.delivered\_qty from flt((entry.delivered\_qty + delivered\_qty when self.\_action equals “submit”, otherwise (negative 1 × delivered\_qty)), entry.precision(“delivered\_qty”)).
                - Value choice on self.\_action equals “submit” — true gives delivered\_qty, false gives (negative 1 × delivered\_qty).
              - Evaluate entry.db\_update().
              - Update working\_qty using + delivered\_qty.
              - Update batch\_qty at entry.batch\_no using − delivered\_qty.
      - Otherwise.
        - Set working\_qty from min((sre\_doc.reserved\_qty − sre\_doc.get(field)) when self.\_action equals “submit”, otherwise sre\_doc.get(field), qty).
          - Value choice on self.\_action equals “submit” — true gives (sre\_doc.reserved\_qty − sre\_doc.get(field)), false gives sre\_doc.get(field).
      - Evaluate sre\_doc.set(field, flt((sre\_doc.get(field) + working\_qty when self.\_action equals “submit”, otherwise (negative 1 × working\_qty)), sre\_doc.precision(field))).
        - Value choice on self.\_action equals “submit” — true gives working\_qty, false gives (negative 1 × working\_qty).
      - Evaluate sre\_doc.db\_update().
      - Evaluate sre\_doc.update\_reserved\_qty\_in\_voucher().
      - Evaluate sre\_doc.update\_status().
      - Evaluate sre\_doc.update\_reserved\_stock\_in\_bin().
      - Update qty using − working\_qty.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-db6b66958e2a15-guard-84)

**Methods declared on this owner** [rebuild subcontracting transfers](operations-027.md#op-a502a5681ce9b7).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L980) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L657)

<a id="op-aef16eec85ec6c"></a>
### Stock Controller.update stock reservation entries.get sre list

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_update_stock_reservation_entries_get_stock_reservation_entry_list`

**Inputs** item.

**Explicit results** query.run(pluck = “name”).

**Local steps**

- Set table from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(table.name).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the contract.voucher\_type equals ne ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in purpose → self.doctype.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in purpose → self.doctype.
- If reference\_field bound to data\_map at (purpose or self.doctype).get(“voucher\_detail\_no\_field”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in purpose → self.doctype.
  - Set query from query.where(table.voucher\_detail\_no equals item.get(reference\_field)).
  - If warehouse\_field bound to data\_map at (purpose or self.doctype).get(“exclude\_warehouse\_field”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in purpose → self.doctype.
    - Set query from query.where(table.warehouse differs from item.get(warehouse\_field)).
- Otherwise.
  - Set query from query.where((table.item\_code equals item.rm\_item\_code bitwise and table.warehouse equals self.supplier\_warehouse)).
- Return query.run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L659)

<a id="op-9fd0192c3c923b"></a>
### Stock Controller.update stock reservation entries.get data map

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_update_stock_reservation_entries_get_data_map`

**Inputs** no declared parameters.

**Explicit results** mapping(“Subcontracting Delivery” → mapping(“table\_name” → “items”, “voucher\_type” → “Subcontracting Inward Order”, “voucher\_no” → self.get(“subcontracting\_inward\_order”), “voucher\_detail\_no\_field” → “scio ….

**Local steps**

- Return mapping(“Subcontracting Delivery” → mapping(“table\_name” → “items”, “voucher\_type” → “Subcontracting Inward Order”, “voucher\_no” → self.get(“subcontracting\_inward\_order”), “voucher\_detail\_no\_field” → “scio ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L981) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L658)
