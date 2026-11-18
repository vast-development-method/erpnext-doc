# Shared transaction rules · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Subcontracting controller

<a id="op-58a1884544a316"></a>
### Make return stock entry for subcontract.post process

`operation_enterprise_controllers_subcontracting_controller_business_behavior_make_return_stock_entry_for_subcontract_post_process`

**Inputs** source\_doc, target\_doc.

**Local steps**

- Set target\_doc.purpose from “Material Transfer”.
- If source\_doc.doctype equals “Purchase Order”.
  - Set target\_doc.purchase\_order from source\_doc.name.
- Otherwise.
  - Set target\_doc.subcontracting\_order from source\_doc.name.
- Set target\_doc.company from source\_doc.company.
- Set target\_doc.is\_return from 1.
- For each tuple(\_key, value) in available\_materials.items().
  - If not value.qty.
    - Continue with the next iteration or loop test.
  - If item\_details bound to value.get(“item\_details”).
    - Set item\_details at “serial\_and\_batch\_bundle” from no value.
  - If value.batch\_no.
    - For each tuple(batch\_no, qty) in value.batch\_no.items().
      - If qty &gt; 0.
        - Evaluate add\_items\_in\_ste(target\_doc, value, qty, rm\_details, …).
  - Otherwise.
    - Evaluate add\_items\_in\_ste(target\_doc, value, value.qty, rm\_details, …).
- Evaluate target\_doc.set\_stock\_entry\_type().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L1231) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L997) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L674)

<a id="op-938312082b41eb"></a>
### Get materials from supplier

`operation_enterprise_controllers_subcontracting_controller_business_behavior_get_materials_from_supplier`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from order\_doctype via get\_cached\_doc.

**Explicit results** make\_return\_stock\_entry\_for\_subcontract(doc.available\_materials, doc, rm\_details, order\_doctype).

**Explicit failure paths** validation helper — translated “Materials are already received against the {0} {1}”.format(order\_doctype, subcontract\_order).

**Local steps**

- Set args from (Platform.flags.args or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.args → mapping().
- Set subcontract\_order from (args.get(“subcontract\_order”) or source\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“subcontract\_order”) → source\_name.
- Set rm\_details from args.get(“rm\_details”).
- Set order\_doctype from (args.get(“order\_doctype”) or “Subcontracting Order”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“order\_doctype”) → “Subcontracting Order”.
- If isinstance(rm\_details, str).
  - Set rm\_details from json.loads(rm\_details).
- Set doc from Platform.get\_cached\_doc(order\_doctype, subcontract\_order).
- Evaluate doc.initialized\_fields().
- Set doc.subcontract\_orders from list(doc.name).
- Evaluate doc.get\_available\_materials().
- If not doc.available\_materials.
  - Call the validation error handler Platform.throw(translated “Materials are already received against the {0} {1}”.format(order\_doctype, subcontract\_order)).
- Return make\_return\_stock\_entry\_for\_subcontract(doc.available\_materials, doc, rm\_details, order\_doctype).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(order\_doctype, subcontract\_order).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L992) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L669)

## Service · Subcontracting inward controller

<a id="op-9499051a95f9ba"></a>
### Subcontracting Inward Controller.validate subcontracting inward

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_subcontracting_inward`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_inward\_order().
- Evaluate self.set\_allow\_zero\_valuation\_rate().
- Evaluate self.validate\_warehouse\_().
- Evaluate self.validate\_serial\_batch\_for\_return\_or\_delivery().
- Evaluate self.validate\_delivery().
- Evaluate self.update\_customer\_provided\_item\_cost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate inward order](operations-032.md#op-4690ba1c09ae7c), [set allow zero valuation rate](operations-032.md#op-118653b2ad7c7a), [validate warehouse](operations-032.md#op-4382199ef8c3c4), [validate serial batch for return or delivery](operations-032.md#op-6cb1414587b22b), [validate delivery](operations-032.md#op-32988026999a25), [update customer provided item cost](operations-032.md#op-50f404ec61db3a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L2213) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1093) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L762)

<a id="op-9d10872119ef38"></a>
### Subcontracting Inward Controller.on submit subcontracting inward

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_on_submit_subcontracting_inward`

**Inputs** self.

**Local steps**

- Evaluate self.update\_inward\_order\_item().
- Evaluate self.update\_inward\_order\_received\_items().
- Evaluate self.update\_inward\_order\_secondary\_items().
- Evaluate self.create\_stock\_reservation\_entries\_for\_inward().
- Evaluate self.update\_inward\_order\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update inward order item](operations-032.md#op-c52d120258c4a0), [update inward order received items](operations-032.md#op-56ea7c553b95f4), [update inward order secondary items](operations-033.md#op-ed6e81bc4cbbf4), [create stock reservation entries for inward](operations-033.md#op-7ec9633ff145a8), [update inward order status](operations-033.md#op-45a9e97d5d9e45).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L2364) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1064) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L741)

<a id="op-d66dff893906cc"></a>
### Subcontracting Inward Controller.on cancel subcontracting inward

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_on_cancel_subcontracting_inward`

**Inputs** self.

**Local steps**

- Evaluate self.update\_inward\_order\_item().
- Evaluate self.validate\_manufacture\_entry\_cancel().
- Evaluate self.validate\_delivery().
- Evaluate self.validate\_receive\_from\_customer\_cancel().
- Evaluate self.update\_inward\_order\_received\_items().
- Evaluate self.update\_inward\_order\_secondary\_items().
- Evaluate self.remove\_reference\_for\_additional\_items().
- Evaluate self.update\_inward\_order\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update inward order item](operations-032.md#op-c52d120258c4a0), [validate manufacture entry cancel](operations-032.md#op-2869fcf3a08dd4), [validate delivery](operations-032.md#op-32988026999a25), [validate receive from customer cancel](operations-032.md#op-a6941ae58800bf), [update inward order received items](operations-032.md#op-56ea7c553b95f4), [update inward order secondary items](operations-033.md#op-ed6e81bc4cbbf4), [remove reference for additional items](operations-033.md#op-6c78329a62936b), [update inward order status](operations-033.md#op-45a9e97d5d9e45).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L2495) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1063) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L740)

<a id="op-de4eec8cf137e8"></a>
### Subcontracting Inward Controller.validate purpose

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_purpose`

**Inputs** self.

**Local steps**

- If (self.subcontracting\_inward\_order and self.purpose does not belong to list(“Receive from Customer”, “Return Raw Material to Customer”, “Manufacture”, “Subcontracting Delivery”, …)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_inward\_order → self.purpose does not belong to list(“Receive from Customer”, “Return Raw Material to Customer”, “Manufacture”, “Subcontracting Delivery”, …).
  - Set self.subcontracting\_inward\_order from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L2686) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1089) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L758)

<a id="op-4690ba1c09ae7c"></a>
### Subcontracting Inward Controller.validate inward order

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_inward_order`

**Inputs** self.

**Local steps**

- If self.subcontracting\_inward\_order.
  - Select the first matching pattern against self.purpose.
    - Pattern “Receive from Customer”.
      - Evaluate self.validate\_material\_receipt().
    - Pattern purpose with guard purpose belongs to list(“Return Raw Material to Customer”, “Subcontracting Return”).
      - Evaluate self.validate\_returns().
    - Pattern “Material Transfer for Manufacture”.
      - Evaluate self.validate\_material\_transfer().
    - Pattern “Manufacture”.
      - Evaluate self.validate\_manufacture().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate material receipt](operations-032.md#op-24c136121d49c1), [validate returns](operations-032.md#op-f4bbf4da0ba2e0), [validate material transfer](operations-032.md#op-42094b4a34c183), [validate manufacture](operations-032.md#op-e9e3c8a0c8d0a0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L2797) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1077) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L753)

<a id="op-24c136121d49c1"></a>
### Subcontracting Inward Controller.validate material receipt

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_material_receipt`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value · read “Subcontracting Inward Order Received Item” via get\_cached\_value · read “Subcontracting Inward Order Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not a Customer Provided Item.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times in the Subcontracting Inward process.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Item {1} mismatch. Changing of item code is not permitted, add another row instead.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Customer Provided Item {1} against Subcontracting Inward Order Item {2} ({3}) cannot be added mult …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), bold(item.against\_fg), … · validation helper — translated “Row #{0}: Please select the Finished Good Item against which this Customer Provided Item will be used.”.format(item.idx).

**Local steps**

- Evaluate self.set\_scio\_detail\_for\_received\_items().
- Set rm\_item\_fg\_combo from list().
- Set scio\_details from list().
- For each item in self.items.
  - If not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not a Customer Provided Item.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - If item.scio\_detail belongs to scio\_details.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times in the Subcontracting Inward process.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - Otherwise.
    - If item.scio\_detail.
      - Evaluate scio\_details.append(item.scio\_detail).
  - If (item.scio\_detail and Platform.get\_cached\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, “rm\_item\_code”) differs from item.item\_code).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.scio\_detail → Platform.get\_cached\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, “rm\_item\_code”) differs from item.item\_code.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} mismatch. Changing of item code is not permitted, add another row instead.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - If not item.scio\_detail.
    - If item.against\_fg.
      - If tuple(item.item\_code, item.against\_fg) does not belong to rm\_item\_fg\_combo.
        - Evaluate rm\_item\_fg\_combo.append(tuple(item.item\_code, item.against\_fg)).
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} against Subcontracting Inward Order Item {2} ({3}) cannot be added mult …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), bold(it ….
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Please select the Finished Good Item against which this Customer Provided Item will be used.”.format(item.idx)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set scio detail for received items](operations-032.md#op-f79f6aab665203).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”), Platform.get\_cached\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, “rm\_item\_code”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1087) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L756)

<a id="op-f79f6aab665203"></a>
### Subcontracting Inward Controller.set scio detail for received items

`operation_enterprise_binding_enterprise_controllers_subcontracting_inward_controller_subcontractinginwardcontroller_set_scio_detail_for_received_items`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Received Item” via get\_all.

**Explicit results** no value.

**Local steps**

- Set items from list of item for item drawn from self.items where not item.scio\_detail.
  - Draw item from self.items, keep a combination only if (not item.scio\_detail).
- If not items.
  - Return no value.
- Set received\_items from Platform.get\_all(“Subcontracting Inward Order Received Item”, filters = mapping(“parent” → self.subcontracting\_inward\_order, “docstatus” → 1, “reference\_name” → list(“in”, list of item.against\_fg for item  ….
  - Draw item from items.
- Set row\_names from mapping of tuple(row.rm\_item\_code, row.reference\_name) → row.name for row drawn from received\_items.
  - Draw row from received\_items.
- For each item in items.
  - Set item.scio\_detail from row\_names.get(tuple(item.item\_code, item.against\_fg)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L449)

<a id="op-f4bbf4da0ba2e0"></a>
### Subcontracting Inward Controller.validate returns

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_returns`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Received Item” via get\_cached\_value · read “Subcontracting Inward Order Item” via get\_cached\_value · read “Subcontracting Inward Order Received Item” via get\_value · read “Subcontracting Inward Order Item” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not a part of Subcontracting Inward Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Subcontracting Inward Order”, self.subcontracti … · validation helper — translated “Row #{0}: Item {1} mismatch. Changing of item code is not permitted.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Returned quantity cannot be greater than available quantity for Item {1}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Returned quantity cannot be greater than available quantity to return for Item {1}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)).

**Local steps**

- For each item in self.items.
  - If not item.scio\_detail.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not a part of Subcontracting Inward Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Subcontracting Inward Order”, se ….
  - Otherwise.
    - If item.item\_code differs from (Platform.get\_cached\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, “rm\_item\_code”) or Platform.get\_cached\_value(“Subcontracting Inward Order Item”, item.s ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, “rm\_item\_code”) → Platform.get\_cached\_value(“Subcontracting Inward Order Item”, item.scio\_detail, “item\_code”).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} mismatch. Changing of item code is not permitted.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - Set precision from item.precision(“transfer\_qty”).
  - If self.purpose equals “Return Raw Material to Customer”.
    - Set data from Platform.get\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, list(“received\_qty”, “returned\_qty”, “work\_order\_qty”), as\_dict = true).
    - If flt((data.returned\_qty + item.transfer\_qty), precision) &gt; flt((data.received\_qty − data.work\_order\_qty), precision).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Returned quantity cannot be greater than available quantity for Item {1}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
  - Otherwise.
    - Set data from Platform.get\_value(“Subcontracting Inward Order Item”, item.scio\_detail, list(“returned\_qty”, “delivered\_qty”), as\_dict = true).
    - If flt(item.transfer\_qty, precision) &gt; flt((data.delivered\_qty − data.returned\_qty), precision).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Returned quantity cannot be greater than available quantity to return for Item {1}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, “rm\_item\_code”), Platform.get\_cached\_value(“Subcontracting Inward Order Item”, item.scio\_detail, “item\_code”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1091) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L760)

<a id="op-42094b4a34c183"></a>
### Subcontracting Inward Controller.validate material transfer

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_material_transfer`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order” via get\_cached\_value · read “Item” via get\_cached\_value · read “Work Order Item” via get\_all.

**Explicit failure paths** validation helper — translated “Row #{0}: For Customer Provided Item {1}, Source Warehouse must be {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Warehouse”, customer\_warehouse)) · validation helper — translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times in the Subcontracting Inward process.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Overconsumption of Customer Provided Item {1} against Work Order {2} is not allowed in the Subcont …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Work … · validation helper — translated “Row #{0}: Customer Provided Item {1} is not a part of Work Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Work Order”, self.work\_order)).

**Local steps**

- Set customer\_warehouse from Platform.get\_cached\_value(“Subcontracting Inward Order”, self.subcontracting\_inward\_order, “customer\_warehouse”).
- Set item\_codes from list().
- For each item in self.items.
  - If not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).
    - Continue with the next iteration or loop test.
  - Otherwise.
    - If item.s\_warehouse differs from customer\_warehouse.
      - Call the validation error handler Platform.throw(translated “Row #{0}: For Customer Provided Item {1}, Source Warehouse must be {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Warehouse”, customer\_warehouse))).
    - Otherwise.
      - If item.item\_code belongs to item\_codes.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times in the Subcontracting Inward process.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
      - Otherwise.
        - Set work\_order\_items from Platform.get\_all(“Work Order Item”, mapping(“parent” → self.work\_order, “docstatus” → 1, “is\_customer\_provided\_item” → 1), list(“item\_code”, “transferred\_qty”, “required\_qty”, “stock\_reserved\_qty”)).
        - Set wo\_item\_dict from Platform.\_dict(mapping of wo\_item.item\_code → Platform.\_dict(mapping(“transferred\_qty” → wo\_item.transferred\_qty, “required\_qty” → wo\_item.required\_qty, “stock\_reserved\_qty” → wo\_item.stock\_reserved\_qty))  ….
          - Draw wo\_item from work\_order\_items.
        - If wo\_item bound to wo\_item\_dict.get(item.item\_code).
          - If (wo\_item.transferred\_qty + item.transfer\_qty) &gt; max(wo\_item.required\_qty, wo\_item.stock\_reserved\_qty).
            - Call the validation error handler Platform.throw(translated “Row #{0}: Overconsumption of Customer Provided Item {1} against Work Order {2} is not allowed in the Subcont …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_lin ….
          - Otherwise.
            - Evaluate item\_codes.append(item.item\_code).
        - Otherwise.
          - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} is not a part of Work Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Work Order”, self.work\_order))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Subcontracting Inward Order”, self.subcontracting\_inward\_order, “customer\_warehouse”), Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1088) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L757)

<a id="op-e9e3c8a0c8d0a0"></a>
### Subcontracting Inward Controller.validate manufacture

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_manufacture`

**Inputs** self.

**Record and data access** read “Work Order” via get\_cached\_value · read “Item” via get\_cached\_value · read “Subcontracting Inward Order” via get\_cached\_value · read “Work Order Item” via get\_all.

**Explicit failure paths** validation helper — translated “Target Warehouse for Finished Good must be same as Finished Good Warehouse {1} in Work Order {2} linked to t …”.format(get\_link\_to\_form(“Warehouse”, fg\_warehouse), get\_link\_to\_form(“Work Order” … · validation helper — translated “Row #{0}: Customer Provided Item {1} exceeds quantity available through Subcontracting Inward Order”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), item.transfer\_qty) · validation helper — translated “Row #{0}: For Customer Provided Item {1}, Source Warehouse must be {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Warehouse”, customer\_warehouse)) · validation helper — translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times in the Subcontracting Inward process.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Customer Provided Item {1} is not a part of Subcontracting Inward Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Subcontracting Inward Order”, … · 2 additional forms in the steps below.

**Local steps**

- If next(generator of item for item drawn from self.items where item.is\_finished\_item).t\_warehouse differs from fg\_warehouse bound to Platform.get\_cached\_value(“Work Order”, self.work\_order, “fg\_warehouse”).
  - Draw item from self.items, keep a combination only if (item.is\_finished\_item).
  - Call the validation error handler Platform.throw(translated “Target Warehouse for Finished Good must be same as Finished Good Warehouse {1} in Work Order {2} linked to t …”.format(get\_link\_to\_form(“Warehouse”, fg\_warehouse), get\_link\_to\_fo ….
- Set items from list of item for item drawn from self.get(“items”) where (not item.is\_finished\_item and not item.secondary\_item\_type and not item.valuation\_type and Platform.get\_cached\_value(“Item”, item.item\_code, “is\_cu ….
  - Draw item from self.get(“items”), keep a combination only if ((not item.is\_finished\_item and not item.secondary\_item\_type and not item.valuation\_type and Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.is\_finished\_item → not item.secondary\_item\_type → not item.valuation\_type → Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).
- Set customer\_warehouse from Platform.get\_cached\_value(“Subcontracting Inward Order”, self.subcontracting\_inward\_order, “customer\_warehouse”).
- If Platform.get\_cached\_value(“Work Order”, self.work\_order, “skip\_transfer”).
  - Set table from Platform.qb.DocType(“Subcontracting Inward Order Received Item”).
  - Set query from nested operand in the contract.qb.from\_(table).select(table.rm\_item\_code, (nested operand in the contract.received\_qty − nested operand in the contract.returned\_qty).as\_(“total\_qty”), table.consumed\_qty, t ….
    - Draw item from items.
  - Set rm\_item\_dict from Platform.\_dict(mapping of d.rm\_item\_code → Platform.\_dict(mapping(“name” → d.name, “total\_qty” → d.total\_qty, “qty” → d.consumed\_qty)) for d drawn from query.run(as\_dict = true)).
    - Draw d from query.run(as\_dict = true).
  - Set item\_codes from list().
  - For each item in items.
    - If rm bound to rm\_item\_dict.get(item.item\_code).
      - If (rm.qty + item.transfer\_qty) &gt; rm.total\_qty.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} exceeds quantity available through Subcontracting Inward Order”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), item.transfer\_qty)).
      - Otherwise.
        - If item.s\_warehouse differs from customer\_warehouse.
          - Call the validation error handler Platform.throw(translated “Row #{0}: For Customer Provided Item {1}, Source Warehouse must be {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Warehouse”, customer\_warehouse))).
        - Otherwise.
          - If item.item\_code belongs to item\_codes.
            - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times in the Subcontracting Inward process.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
          - Otherwise.
            - Evaluate item\_codes.append(item.item\_code).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} is not a part of Subcontracting Inward Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Subcontracting ….
- Otherwise.
  - Set work\_order\_items from Platform.get\_all(“Work Order Item”, mapping(“parent” → self.work\_order, “docstatus” → 1, “is\_customer\_provided\_item” → 1), list(“item\_code”, “transferred\_qty”, “consumed\_qty”)).
  - Set wo\_item\_dict from Platform.\_dict(mapping of wo\_item.item\_code → Platform.\_dict(mapping(“transferred\_qty” → wo\_item.transferred\_qty, “consumed\_qty” → wo\_item.consumed\_qty)) for wo\_item drawn from work\_order\_items).
    - Draw wo\_item from work\_order\_items.
  - Set item\_codes from list().
  - For each item in items.
    - If wo\_item bound to wo\_item\_dict.get(item.item\_code).
      - If (wo\_item.consumed\_qty + item.transfer\_qty) &gt; wo\_item.transferred\_qty.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Overconsumption of Customer Provided Item {1} against Work Order {2} is not allowed in the Subcont …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_lin ….
      - Otherwise.
        - If item.item\_code belongs to item\_codes.
          - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} cannot be added multiple times in the Subcontracting Inward process.”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
        - Otherwise.
          - Evaluate item\_codes.append(item.item\_code).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Customer Provided Item {1} is not a part of Work Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Work Order”, self.work\_order))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “fg\_warehouse”), Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”) and 3 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1078) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L754)

<a id="op-118653b2ad7c7a"></a>
### Subcontracting Inward Controller.set allow zero valuation rate

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_set_allow_zero_valuation_rate`

**Inputs** self.

**Local steps**

- If self.subcontracting\_inward\_order.
  - If self.purpose belongs to list(“Subcontracting Delivery”, “Subcontracting Return”, “Manufacture”).
    - For each item in self.items.
      - If ((item.is\_finished\_item or item.secondary\_item\_type or item.valuation\_type) and item.valuation\_rate equals 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in (item.is\_finished\_item or item.secondary\_item\_type or item.valuation\_type) → item.valuation\_rate equals 0.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.is\_finished\_item → item.secondary\_item\_type → item.valuation\_type.
        - Set item.allow\_zero\_valuation\_rate from 1.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0398.json#L2670) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1066) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L743)

<a id="op-4382199ef8c3c4"></a>
### Subcontracting Inward Controller.validate warehouse

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_warehouse`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order” via get\_cached\_value · read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Target Warehouse must be same as Customer Warehouse {1} from the linked Subcontracting Inward Order”.format(item.idx, get\_link\_to\_form(“Warehouse”, customer\_warehouse)) · validation helper — translated “Row #{0}: Source Warehouse must be same as Customer Warehouse {1} from the linked Subcontracting Inward Order”.format(item.idx, get\_link\_to\_form(“Warehouse”, customer\_warehouse)).

**Local steps**

- If (self.subcontracting\_inward\_order and self.purpose belongs to list(“Receive from Customer”, “Return Raw Material to Customer”, “Material Transfer for Manufacture”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_inward\_order → self.purpose belongs to list(“Receive from Customer”, “Return Raw Material to Customer”, “Material Transfer for Manufacture”).
  - Set customer\_warehouse from Platform.get\_cached\_value(“Subcontracting Inward Order”, self.subcontracting\_inward\_order, “customer\_warehouse”).
  - For each item in self.items.
    - If (self.purpose equals “Material Transfer for Manufacture” and not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Material Transfer for Manufacture” → not Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).
      - Continue with the next iteration or loop test.
    - If (item.s\_warehouse or item.t\_warehouse) differs from customer\_warehouse.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.s\_warehouse → item.t\_warehouse.
      - If item.t\_warehouse.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Target Warehouse must be same as Customer Warehouse {1} from the linked Subcontracting Inward Order”.format(item.idx, get\_link\_to\_form(“Warehouse”, customer\_warehouse))).
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Source Warehouse must be same as Customer Warehouse {1} from the linked Subcontracting Inward Order”.format(item.idx, get\_link\_to\_form(“Warehouse”, customer\_warehouse))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Subcontracting Inward Order”, self.subcontracting\_inward\_order, “customer\_warehouse”), Platform.get\_cached\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0398.json#L2851) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1094) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L763)

<a id="op-6cb1414587b22b"></a>
### Subcontracting Inward Controller.validate serial batch for return or delivery

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_serial_batch_for_return_or_delivery`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Serial No(s) {1} are not a part of the linked Subcontracting Inward Order. Please select valid Ser …”.format(item.idx, “, ”.join(list of get\_link\_to\_form(“Serial No”, sn) for sn drawn … · validation helper — translated “Row #{0}: Batch No(s) {1} is not a part of the linked Subcontracting Inward Order. Please select valid Batch No(s).”.format(item.idx, “, ”.join(list of get\_link\_to\_form(“Batch No”, bn) for bn d ….

**Local steps**

- If (self.subcontracting\_inward\_order and self.purpose belongs to list(“Return Raw Material to Customer”, “Subcontracting Delivery”, “Subcontracting Return”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_inward\_order → self.purpose belongs to list(“Return Raw Material to Customer”, “Subcontracting Delivery”, “Subcontracting Return”).
  - For each item in self.items.
    - Set tuple(serial\_nos, batch\_nos) from self.get\_serial\_nos\_and\_batches\_from\_sres(item.scio\_detail, only\_pending = self.purpose differs from “Subcontracting Return”).
    - Set tuple(serial\_list, batch\_list) from get\_serial\_batch\_list\_from\_item(item).
    - If (serial\_list and incorrect\_serial\_nos bound to list of sn for sn drawn from serial\_list where sn does not belong to serial\_nos).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial\_list → incorrect\_serial\_nos bound to list of sn for sn drawn from serial\_list where sn does not belong to serial\_nos.
      - Draw sn from serial\_list, keep a combination only if (sn does not belong to serial\_nos).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Serial No(s) {1} are not a part of the linked Subcontracting Inward Order. Please select valid Ser …”.format(item.idx, “, ”.join(list of get\_link\_to\_form(“Serial No”, s ….
        - Draw sn from incorrect\_serial\_nos.
    - If (batch\_list and incorrect\_batch\_nos bound to list of bn for bn drawn from batch\_list where bn does not belong to list(nested operand in the contract.keys())).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_list → incorrect\_batch\_nos bound to list of bn for bn drawn from batch\_list where bn does not belong to list(batch\_nos.keys()).
      - Draw bn from batch\_list, keep a combination only if (bn does not belong to list(batch\_nos.keys())).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Batch No(s) {1} is not a part of the linked Subcontracting Inward Order. Please select valid Batch No(s).”.format(item.idx, “, ”.join(list of get\_link\_to\_form(“Batch No ….
        - Draw bn from incorrect\_batch\_nos.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get serial nos and batches from sres](operations-032.md#op-2c4a76301a34eb).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1092) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L761)

<a id="op-2c4a76301a34eb"></a>
### Subcontracting Inward Controller.get serial nos and batches from sres

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_get_serial_numbers_and_batches_from_sres`

**Inputs** self, scio\_detail, only\_pending = true.

**Explicit results** tuple(serial\_nos, batch\_nos).

**Local steps**

- Set tuple(serial\_nos, batch\_nos) from tuple(list(), Platform.\_dict()).
- Set table from Platform.qb.DocType(“Stock Reservation Entry”).
- Set child\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(child\_table.serial\_no, child\_table.batch\_no, child ….
- If only\_pending.
  - Set query from query.where(child\_table.qty differs from child\_table.delivered\_qty).
- Otherwise.
  - Set query from query.where(child\_table.delivered\_qty &gt; 0).
- For each d in query.run(as\_dict = true).
  - If (d.serial\_no and d.serial\_no does not belong to serial\_nos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.serial\_no → d.serial\_no does not belong to serial\_nos.
    - Evaluate serial\_nos.append(d.serial\_no).
  - If d.batch\_no.
    - Set qty from (d.qty − d.delivered\_qty) when only\_pending, otherwise d.qty.
      - Value choice on only\_pending — true gives (d.qty − d.delivered\_qty), false gives d.qty.
    - Set batch\_nos at d.batch\_no from (batch\_nos.get(d.batch\_no, 0) + qty).
- Return tuple(serial\_nos, batch\_nos).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1062) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L739)

<a id="op-32988026999a25"></a>
### Subcontracting Inward Controller.validate delivery

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_delivery`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Item” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot cancel this Stock Entry as returned quantity cannot be greater than delivered quantity for  …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)).

**Local steps**

- If self.purpose equals “Subcontracting Delivery”.
  - If self.\_action belongs to list(“save”, “submit”).
    - Evaluate self.validate\_delivery\_on\_save().
  - Otherwise.
    - For each item in self.items.
      - If (not item.secondary\_item\_type and not item.valuation\_type).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.secondary\_item\_type → not item.valuation\_type.
        - Set tuple(delivered\_qty, returned\_qty) from Platform.get\_value(“Subcontracting Inward Order Item”, item.scio\_detail, list(“delivered\_qty”, “returned\_qty”)).
        - If returned\_qty &gt; delivered\_qty.
          - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot cancel this Stock Entry as returned quantity cannot be greater than delivered quantity for  …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate delivery on save](operations-032.md#op-dbf3e4c38087ff).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0398.json#L4563) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1075) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L751)

<a id="op-dbf3e4c38087ff"></a>
### Subcontracting Inward Controller.validate delivery on save

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_delivery_on_save`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Subcontracting Inward Order Item” when (not item.secondary\_item\_type and not item.valuation\_type), otherwise “Subcontracting Inward Order Secondary Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Item {1} is not a part of Subcontracting Inward Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Subcontracting Inward Order”, self.subcontracti … · validation helper — translated “Row #{0}: Quantity of Item {1} cannot be more than {2} {3} against Subcontracting Inward Order {4}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), bold(max\_allowed\_qty), bold(Platfo ….

**Local steps**

- Set allow\_delivery\_of\_overproduced\_qty from Platform.get\_single\_value(“Selling Settings”, “allow\_delivery\_of\_overproduced\_qty”).
- For each item in self.items.
  - If not item.scio\_detail.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} is not a part of Subcontracting Inward Order {2}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), get\_link\_to\_form(“Subcontracting Inward Order”, se ….
  - Bind dependencies ValueWrapper.
  - Set table from Platform.qb.DocType(“Subcontracting Inward Order Item”).
  - Set query from nested operand in the contract.qb.from\_(table).select((nested operand in the contract(nested operand in the contract) − nested operand in the contract.delivered\_qty).as\_(“max\_allowed\_qty”)).where((table.na ….
  - Set max\_allowed\_qty from query.run(pluck = “max\_allowed\_qty”).
  - If max\_allowed\_qty.
    - Set max\_allowed\_qty from max\_allowed\_qty at 0.
  - Otherwise.
    - Set table from Platform.qb.DocType(“Subcontracting Inward Order Secondary Item”).
    - Set query from nested operand in the contract.qb.from\_(table).select((nested operand in the contract.produced\_qty − nested operand in the contract.delivered\_qty).as\_(“max\_allowed\_qty”)).where((table.name equals item.scio ….
    - Set max\_allowed\_qty from query.run(pluck = “max\_allowed\_qty”) at 0.
  - If item.transfer\_qty &gt; max\_allowed\_qty.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Quantity of Item {1} cannot be more than {2} {3} against Subcontracting Inward Order {4}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code), bold(max\_allowed\_qt ….
      - Value choice on (not item.secondary\_item\_type and not item.valuation\_type) — true gives “Subcontracting Inward Order Item”, false gives “Subcontracting Inward Order Secondary Item”.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.secondary\_item\_type → not item.valuation\_type.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_delivery\_of\_overproduced\_qty”), Platform.get\_cached\_value(“Subcontracting Inward Order Item” when (not item.secondary\_item\_type and not item.valuation\_type), otherwise “Subcontracting Inward Order Secondary Item”, item.scio\_detail, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1076) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L752)

<a id="op-50f404ec61db3a"></a>
### Subcontracting Inward Controller.update customer provided item cost

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_update_customer_provided_item_cost`

**Inputs** self.

**Local steps**

- If self.purpose equals “Receive from Customer”.
  - For each item in self.items.
    - Set item.valuation\_rate from 0.
    - Set item.customer\_provided\_item\_cost from flt((item.basic\_rate + (item.additional\_cost ÷ item.transfer\_qty)), item.precision(“basic\_rate”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0398.json#L6015) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1067) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L744)

<a id="op-a6941ae58800bf"></a>
### Subcontracting Inward Controller.validate receive from customer cancel

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_receive_from_customer_cancel`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Received Item” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Work Order exists against full or partial quantity of Item {1}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)).

**Local steps**

- If self.purpose equals “Receive from Customer”.
  - For each item in self.items.
    - Set scio\_rm\_item from Platform.get\_value(“Subcontracting Inward Order Received Item”, item.scio\_detail, list(“received\_qty”, “returned\_qty”, “work\_order\_qty”), as\_dict = true).
    - If ((scio\_rm\_item.received\_qty − scio\_rm\_item.returned\_qty) − item.transfer\_qty) &lt; scio\_rm\_item.work\_order\_qty.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Work Order exists against full or partial quantity of Item {1}”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0399.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1090) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L759)

<a id="op-2869fcf3a08dd4"></a>
### Subcontracting Inward Controller.validate manufacture entry cancel

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_validate_manufacture_entry_cancel`

**Inputs** self.

**Record and data access** read “Work Order” via get\_cached\_value · read “Subcontracting Inward Order Item” via get\_value · read “Subcontracting Inward Order Secondary Item” via get\_value · read “Subcontracting Inward Order Received Item” via get\_value.

**Explicit failure paths** validation helper — translated “Cannot cancel this Manufacturing Stock Entry as quantity of Finished Good produced cannot be less than quant …” · validation helper — translated “Row #{0}: Cannot cancel this Manufacturing Stock Entry as quantity of Secondary Item {1} produced cannot be  …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)) · validation helper — translated “Row #{0}: Cannot cancel this Manufacturing Stock Entry as billed quantity of Item {1} cannot be greater than …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code)).

**Local steps**

- If (self.subcontracting\_inward\_order and self.purpose equals “Manufacture”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.subcontracting\_inward\_order → self.purpose equals “Manufacture”.
  - Set fg\_item\_name from Platform.get\_cached\_value(“Work Order”, self.work\_order, “subcontracting\_inward\_order\_item”).
  - Set tuple(produced\_qty, delivered\_qty) from Platform.get\_value(“Subcontracting Inward Order Item”, fg\_item\_name, list(“produced\_qty”, “delivered\_qty”)).
  - If produced\_qty &lt; delivered\_qty.
    - Call the validation error handler Platform.throw(translated “Cannot cancel this Manufacturing Stock Entry as quantity of Finished Good produced cannot be less than quant …”).
  - For each item in list of item for item drawn from self.items where not item.is\_finished\_item.
    - Draw item from self.items, keep a combination only if (not item.is\_finished\_item).
    - If (item.secondary\_item\_type or item.valuation\_type).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → item.valuation\_type.
      - Set scio\_secondary\_item from Platform.get\_value(“Subcontracting Inward Order Secondary Item”, mapping(“docstatus” → 1, “item\_code” → item.item\_code, “warehouse” → item.t\_warehouse, “reference\_name” → fg\_item\_name), list(“produced\_qty” ….
      - If (scio\_secondary\_item and scio\_secondary\_item.delivered\_qty &gt; (scio\_secondary\_item.produced\_qty − item.transfer\_qty)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in scio\_secondary\_item → scio\_secondary\_item.delivered\_qty &gt; (scio\_secondary\_item.produced\_qty − item.transfer\_qty).
        - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot cancel this Manufacturing Stock Entry as quantity of Secondary Item {1} produced cannot be  …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).
    - Otherwise.
      - Set scio\_rm\_item from Platform.get\_value(“Subcontracting Inward Order Received Item”, mapping(“docstatus” → 1, “rm\_item\_code” → item.item\_code, “warehouse” → item.s\_warehouse, “is\_customer\_provided\_item” → 0, …), list(“consumed ….
      - If (scio\_rm\_item and (scio\_rm\_item.billed\_qty − scio\_rm\_item.returned\_qty) &gt; (scio\_rm\_item.consumed\_qty − item.transfer\_qty)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in scio\_rm\_item → (scio\_rm\_item.billed\_qty − scio\_rm\_item.returned\_qty) &gt; (scio\_rm\_item.consumed\_qty − item.transfer\_qty).
        - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot cancel this Manufacturing Stock Entry as billed quantity of Item {1} cannot be greater than …”.format(item.idx, get\_link\_to\_form(“Item”, item.item\_code))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “subcontracting\_inward\_order\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0399.json#L317) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1086) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L755)

<a id="op-c52d120258c4a0"></a>
### Subcontracting Inward Controller.update inward order item

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_update_inward_order_item`

**Inputs** self.

**Record and data access** read “Work Order” via get\_cached\_value · resolve a document from “Subcontracting Inward Order Item” via get\_doc.

**State and service calls** request bulk\_update on doctype.

**Local steps**

- If (self.purpose equals “Manufacture” and scio\_item\_name bound to Platform.get\_cached\_value(“Work Order”, self.work\_order, “subcontracting\_inward\_order\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purpose equals “Manufacture” → scio\_item\_name bound to Platform.get\_cached\_value(“Work Order”, self.work\_order, “subcontracting\_inward\_order\_item”).
  - If scio\_item\_name.
    - Evaluate Platform.get\_doc(“Subcontracting Inward Order Item”, scio\_item\_name).update\_manufacturing\_qty\_fields().
- Otherwise.
  - If self.purpose belongs to list(“Subcontracting Delivery”, “Subcontracting Return”).
    - Set fieldname from “delivered\_qty” when self.purpose equals “Subcontracting Delivery”, otherwise “returned\_qty”.
      - Value choice on self.purpose equals “Subcontracting Delivery” — true gives “delivered\_qty”, false gives “returned\_qty”.
    - Set qty\_map from defaultdict(deferred anonymous expression).
    - For each item in self.items.
      - Set doctype from “Subcontracting Inward Order Item” when (not item.secondary\_item\_type and not item.valuation\_type), otherwise “Subcontracting Inward Order Secondary Item”.
        - Value choice on (not item.secondary\_item\_type and not item.valuation\_type) — true gives “Subcontracting Inward Order Item”, false gives “Subcontracting Inward Order Secondary Item”.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.secondary\_item\_type → not item.valuation\_type.
      - Update qty\_map at doctype at item.scio\_detail using + item.transfer\_qty when self.\_action equals “submit”, otherwise negative item.transfer\_qty.
        - Value choice on self.\_action equals “submit” — true gives item.transfer\_qty, false gives negative item.transfer\_qty.
    - For each tuple(doctype, item\_qty\_map) in qty\_map.items().
      - Set table from Platform.qb.DocType(doctype).
      - Set field from table at fieldname.
      - Set doc\_updates from mapping of scio\_detail → mapping(fieldname → (field + qty)) for tuple(scio\_detail, qty) drawn from item\_qty\_map.items().
        - Draw tuple(scio\_detail, qty) from item\_qty\_map.items().
      - Evaluate Platform.db.bulk\_update(doctype, doc\_updates, chunk\_size = len(doc\_updates)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Work Order”, self.work\_order, “subcontracting\_inward\_order\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1068) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L745)

<a id="op-56ea7c553b95f4"></a>
### Subcontracting Inward Controller.update inward order received items

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_update_inward_order_received_items`

**Inputs** self.

**State and service calls** request bulk\_update on “Subcontracting Inward Order Received Item”.

**Local steps**

- If self.subcontracting\_inward\_order.
  - Select the first matching pattern against self.purpose.
    - Pattern “Receive from Customer”.
      - Evaluate self.update\_inward\_order\_received\_items\_for\_raw\_materials\_receipt().
    - Pattern “Manufacture”.
      - Evaluate self.update\_inward\_order\_received\_items\_for\_manufacture().
    - Pattern “Return Raw Material to Customer”.
      - Set scio\_rm\_names from mapping of item.scio\_detail → item.transfer\_qty when self.\_action equals “submit”, otherwise negative item.transfer\_qty for item drawn from self.items.
        - Draw item from self.items.
        - Value choice on self.\_action equals “submit” — true gives item.transfer\_qty, false gives negative item.transfer\_qty.
      - Set table from Platform.qb.DocType(“Subcontracting Inward Order Received Item”).
      - Set doc\_updates from mapping of scio\_rm\_name → mapping(“returned\_qty” → (table.returned\_qty + qty)) for tuple(scio\_rm\_name, qty) drawn from scio\_rm\_names.items().
        - Draw tuple(scio\_rm\_name, qty) from scio\_rm\_names.items().
      - If doc\_updates.
        - Evaluate Platform.db.bulk\_update(“Subcontracting Inward Order Received Item”, doc\_updates, chunk\_size = len(doc\_updates), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update inward order received items for raw materials receipt](operations-032.md#op-7477cd0590b92b), [update inward order received items for manufacture](operations-033.md#op-e42fee6a905ecc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0399.json#L1913) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1069) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L746)

<a id="op-7477cd0590b92b"></a>
### Subcontracting Inward Controller.update inward order received items for raw materials receipt

`operation_enterprise_controllers_subcontracting_inward_controller_business_behavior_subcontracting_inward_controller_update_inward_order_received_items_for_raw_materials_receipt`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Received Item” via count · read “Subcontracting Inward Order Item” via get\_cached\_value · read “Subcontracting Inward Order Received Item” via get\_all.

**State and service calls** request new\_doc for “Subcontracting Inward Order Received Item” · call insert on scio\_rm · call submit on scio\_rm · call db\_set on item · request delete\_doc for “Subcontracting Inward Order Received Item” · 1 additional forms in the steps below.

**Local steps**

- Set data from Platform.\_dict().
- For each item in self.items.
  - If item.scio\_detail.
    - Set data at item.scio\_detail from Platform.\_dict(mapping(“transfer\_qty” → item.transfer\_qty, “rate” → item.customer\_provided\_item\_cost)).
  - Otherwise.
    - Set scio\_rm from Platform.new\_doc(“Subcontracting Inward Order Received Item”, parent = self.subcontracting\_inward\_order, parenttype = “Subcontracting Inward Order”, parentfield = “received\_items”, idx = (Platform.db.count ….
    - Evaluate scio\_rm.insert(ignore\_permissions = true).
    - Evaluate scio\_rm.submit().
    - Evaluate item.db\_set(“scio\_detail”, scio\_rm.name).
- If data.
  - Set precision from self.precision(“customer\_provided\_item\_cost”, “items”).
  - Set result from Platform.get\_all(“Subcontracting Inward Order Received Item”, filters = mapping(“parent” → self.subcontracting\_inward\_order, “name” → list(“in”, list(data.keys())), “docstatus” → 1), fields = list(“rate”,  ….
  - Set doc\_updates from mapping().
  - For each d in result.
    - Set current\_qty from (flt(data at d.name.transfer\_qty) × 1 when self.\_action equals “submit”, otherwise negative 1).
      - Value choice on self.\_action equals “submit” — true gives 1, false gives negative 1.
    - Set current\_rate from flt(data at d.name.rate).
    - Set balance\_qty from ((d.received\_qty − d.returned\_qty) − d.consumed\_qty).
    - Set old\_total from (d.rate × balance\_qty).
    - Set current\_total from (current\_rate × current\_qty).
    - Set new\_balance\_qty from (balance\_qty + current\_qty).
    - Set d.received\_qty from (d.received\_qty + current\_qty).
    - Set d.rate from flt(((old\_total + current\_total) ÷ new\_balance\_qty), precision) when new\_balance\_qty &gt; 0, otherwise 0.0.
      - Value choice on new\_balance\_qty &gt; 0 — true gives flt(((old\_total + current\_total) ÷ new\_balance\_qty), precision), false gives 0.0.
    - If (not d.required\_qty and not d.received\_qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.required\_qty → not d.received\_qty.
      - Evaluate Platform.delete\_doc(“Subcontracting Inward Order Received Item”, d.name, ignore\_permissions = true).
    - Otherwise.
      - Set doc\_updates at d.name from mapping(“received\_qty” → d.received\_qty, “rate” → d.rate).
  - If doc\_updates.
    - Evaluate Platform.db.bulk\_update(“Subcontracting Inward Order Received Item”, doc\_updates, chunk\_size = len(doc\_updates), update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Subcontracting Inward Order Item”, item.against\_fg, “item\_code”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1071) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L748)
