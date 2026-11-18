# Shared transaction rules · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Subcontracting controller

<a id="op-7245405c2bddda"></a>
### Subcontracting Controller.validate batch no

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_validate_batch_number`

**Inputs** self, row, key, bundle\_entries.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- Set transferred\_batches from self.\_\_transferred\_items.get(key).get(“batch\_no”).
- Set batch\_nos from set(row.get(“batch\_no”)) when row.get(“batch\_no”), otherwise set().
  - Value choice on row.get(“batch\_no”) — true gives set(row.get(“batch\_no”)), false gives set().
- If transferred\_batches.
  - Evaluate batch\_nos.update(generator of entry.batch\_no for entry drawn from bundle\_entries where entry.batch\_no).
    - Draw entry from bundle\_entries, keep a combination only if (entry.batch\_no).
- Set incorrect\_batches from batch\_nos.difference(transferred\_batches).
- If incorrect\_batches.
  - Set link from get\_link\_to\_form(self.subcontract\_data.order\_doctype, row.get(self.subcontract\_data.order\_field)).
  - Set msg from formatted text The Batch No {Platform.bold(“, ”.join(incorrect\_batches))} has not supplied against the {self.subcontract\_data.order\_doctype} {link}.
  - Call the validation error handler Platform.throw(translated msg, title = translated “Incorrect Batch Consumed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1053) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L730)

<a id="op-074c91013b046c"></a>
### Subcontracting Controller.validate serial no

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_validate_serial_number`

**Inputs** self, row, key, bundle\_entries.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- If self.\_\_transferred\_items.get(key).get(“serial\_no”).
  - Set serial\_nos from set of entry.serial\_no for entry drawn from bundle\_entries where entry.serial\_no.
    - Draw entry from bundle\_entries, keep a combination only if (entry.serial\_no).
  - Set incorrect\_sn from serial\_nos.difference(self.\_\_transferred\_items.get(key).get(“serial\_no”)).
  - If incorrect\_sn.
    - Set incorrect\_sn from whitespace '\\n'.join(incorrect\_sn).
    - Set link from get\_link\_to\_form(self.subcontract\_data.order\_doctype, row.get(self.subcontract\_data.order\_field)).
    - Set msg from formatted text The Serial Nos {incorrect\_sn} has not supplied against the {self.subcontract\_data.order\_doctype} {link}.
    - Call the validation error handler Platform.throw(translated msg, title = translated “Incorrect Serial Number Consumed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1056) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L733)

<a id="op-4de47098c35648"></a>
### Subcontracting Controller.validate supplied or received items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_validate_supplied_or_received_items`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If self.doctype does not belong to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
  - Return no value.
- If Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”) equals “BOM”.
  - Return no value.
- Set bundle\_entries from self.get\_bundle\_entries(self.get(self.raw\_material\_table)).
- For each row in self.get(self.raw\_material\_table).
  - Set key from tuple(row.rm\_item\_code, row.main\_item\_code, row.get(self.subcontract\_data.order\_field)).
  - If not self.\_\_transferred\_items.get(key).
    - Continue with the next iteration or loop test.
  - Set entries from bundle\_entries.get(row.get(“serial\_and\_batch\_bundle”), list()).
  - Evaluate self.\_\_validate\_batch\_no(row, key, entries).
  - Evaluate self.\_\_validate\_serial\_no(row, key, entries).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bundle entries](operations-031.md#op-35127706a964f2), [validate batch no](operations-031.md#op-7245405c2bddda), [validate serial no](operations-031.md#op-074c91013b046c).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1057) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L734)

<a id="op-35127706a964f2"></a>
### Subcontracting Controller.get bundle entries

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_bundle_entries`

**Inputs** self, rows.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** mapping() · bundle\_entries.

**Local steps**

- Set bundles from list of row.get(“serial\_and\_batch\_bundle”) for row drawn from rows where row.get(“serial\_and\_batch\_bundle”).
  - Draw row from rows, keep a combination only if (row.get(“serial\_and\_batch\_bundle”)).
- If not bundles.
  - Return mapping().
- Set bundle\_entries from defaultdict(list).
- For each entry in Platform.get\_all(“Serial and Batch Entry”, fields = list(“parent”, “serial\_no”, “batch\_no”, “qty”), filters = mapping(“parent” → tuple(“in”, bundles))).
  - Evaluate bundle\_entries at entry.parent.append(entry).
- Return bundle\_entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L429)

<a id="op-9154a55f4f9abe"></a>
### Subcontracting Controller.set materials for subcontracted items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_materials_for_subcontracted_items`

**Inputs** self, raw\_material\_table.

**Explicit results** no value.

**Local steps**

- If (self.doctype equals “Purchase Invoice” and not self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → not self.update\_stock.
  - Return no value.
- Set self.raw\_material\_table from raw\_material\_table.
- Evaluate self.\_\_identify\_change\_in\_item\_table().
- Evaluate self.\_\_prepare\_supplied\_or\_received\_items().
- Evaluate self.\_\_validate\_supplied\_or\_received\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [identify change in item table](operations-029.md#op-58c96fb1ff5b2b), [prepare supplied or received items](operations-030.md#op-80cb4a7991f343), [validate supplied or received items](operations-031.md#op-4de47098c35648).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0395.json#L4478) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1036) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L713)

<a id="op-b358c7a6655104"></a>
### Subcontracting Controller.create raw materials supplied or received

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_create_raw_materials_supplied_or_received`

**Inputs** self, raw\_material\_table = “supplied\_items”.

**Local steps**

- If self.get(“supplier\_warehouse”).
  - Evaluate validate\_warehouse\_company(self.supplier\_warehouse, self.company).
- Evaluate self.set\_materials\_for\_subcontracted\_items(raw\_material\_table).
- If self.doctype belongs to list(“Subcontracting Receipt”, “Purchase Receipt”, “Purchase Invoice”).
  - For each item in self.get(“items”).
    - Set item.rm\_supp\_cost from 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set materials for subcontracted items](operations-031.md#op-9154a55f4f9abe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1002) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L679)

<a id="op-764f4df116c1ce"></a>
### Subcontracting Controller.update consumed qty in subcontract order

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_update_consumed_quantity_in_subcontract_order`

**Inputs** self, itemwise\_consumed\_qty.

**Record and data access** read self.subcontract\_data.order\_supplied\_items\_field via get\_all.

**State and service calls** request set\_value on self.subcontract\_data.order\_supplied\_items\_field.

**Local steps**

- Set fields from list(“main\_item\_code”, “rm\_item\_code”, “parent”, “supplied\_qty”, …).
- Set filters from mapping(“docstatus” → 1, “parent” → tuple(“in”, self.subcontract\_orders)).
- For each row in Platform.get\_all(self.subcontract\_data.order\_supplied\_items\_field, fields = fields, filters = filters, order\_by = “idx”).
  - Set key from tuple(row.rm\_item\_code, row.main\_item\_code, row.parent).
  - Set consumed\_qty from itemwise\_consumed\_qty.get(key, 0).
  - If row.supplied\_qty &lt; consumed\_qty.
    - Set consumed\_qty from row.supplied\_qty.
  - Update itemwise\_consumed\_qty at key using − consumed\_qty.
  - Evaluate Platform.db.set\_value(self.subcontract\_data.order\_supplied\_items\_field, row.name, “consumed\_qty”, consumed\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0395.json#L4830) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1046) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L723)

<a id="op-e8dd000e5decda"></a>
### Subcontracting Controller.set consumed qty in subcontract order

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_consumed_quantity_in_subcontract_order`

**Inputs** self.

**Local steps**

- If (self.doctype belongs to list(“Subcontracting Order”, “Subcontracting Receipt”) or self.get(“is\_old\_subcontracting\_flow”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype belongs to list(“Subcontracting Order”, “Subcontracting Receipt”) → self.get(“is\_old\_subcontracting\_flow”).
  - Evaluate self.\_\_get\_subcontract\_orders().
  - Set itemwise\_consumed\_qty from defaultdict(float).
  - If self.get(“is\_old\_subcontracting\_flow”).
    - Set doctypes from list(“Purchase Receipt”, “Purchase Invoice”).
  - Otherwise.
    - Set doctypes from list(“Subcontracting Receipt”).
  - For each doctype in doctypes.
    - Set tuple(consumed\_items, receipt\_items) from self.\_\_update\_consumed\_materials(doctype, return\_consumed\_items = true).
    - For each row in consumed\_items.
      - Set key from tuple(row.rm\_item\_code, row.main\_item\_code, receipt\_items.get(row.reference\_name)).
      - Update itemwise\_consumed\_qty at key using + row.consumed\_qty.
  - Evaluate self.\_\_update\_consumed\_qty\_in\_subcontract\_order(itemwise\_consumed\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get subcontract orders](operations-029.md#op-e3716ec4f97c2d), [update consumed materials](operations-029.md#op-54bf6518aa48ac), [update consumed qty in subcontract order](operations-031.md#op-764f4df116c1ce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1034) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L711)

<a id="op-c4e2f401b17ba4"></a>
### Subcontracting Controller.update ordered and reserved qty

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_update_ordered_and_reserved_quantity`

**Inputs** self.

**Record and data access** resolve a document from “Subcontracting Order” via get\_doc.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “{0} {1} is cancelled or closed”.format(translated “Subcontracting Order”, sco).

**Local steps**

- Set sco\_map from mapping().
- For each item in self.get(“items”).
  - If (self.doctype equals “Subcontracting Receipt” and item.subcontracting\_order).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Subcontracting Receipt” → item.subcontracting\_order.
    - Evaluate sco\_map.setdefault(item.subcontracting\_order, list()).append(item.subcontracting\_order\_item).
- For each tuple(sco, sco\_item\_rows) in sco\_map.items().
  - If (sco and sco\_item\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sco → sco\_item\_rows.
    - Set sco\_doc from Platform.get\_doc(“Subcontracting Order”, sco).
    - If sco\_doc.status belongs to list(“Closed”, “Cancelled”).
      - Call the validation error handler Platform.throw(translated “{0} {1} is cancelled or closed”.format(translated “Subcontracting Order”, sco), Platform.InvalidStatusError).
    - Evaluate sco\_doc.update\_ordered\_qty\_for\_subcontracting(sco\_item\_rows).
    - Evaluate sco\_doc.update\_reserved\_qty\_for\_subcontracting(sco\_item\_rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0395.json#L5553) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1047) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L724)

<a id="op-f9de798b784eba"></a>
### Subcontracting Controller.make sl entries for supplier warehouse

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_make_stock_ledger_entries_for_supplier_warehouse`

**Inputs** self, sl\_entries.

**Local steps**

- If hasattr(self, “supplied\_items”).
  - Set projects from mapping of row.name → row.get(“project”) for row drawn from self.get(“items”).
    - Draw row from self.get(“items”).
  - For each item in self.get(“supplied\_items”).
    - Evaluate sl\_entries.append(self.get\_sl\_entries(item, mapping(“item\_code” → item.rm\_item\_code, “incoming\_rate” → item.rate when self.is\_return, otherwise 0, “recalculate\_rate” → cint(self.is\_return), “warehouse” → s ….
      - Value choice on self.is\_return — true gives item.rate, false gives 0.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in projects.get(item.reference\_name) → self.get(“project”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1022) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L699)

<a id="op-b4f0039ee64d8c"></a>
### Subcontracting Controller.update stock ledger

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_update_stock_ledger`

**Inputs** self, allow\_negative\_stock = false, via\_landed\_cost\_voucher = false.

**Local steps**

- Evaluate self.update\_ordered\_and\_reserved\_qty().
- Set sl\_entries from list().
- Set stock\_items from self.get\_stock\_items().
- Evaluate self.make\_sl\_entries\_for\_supplier\_warehouse(sl\_entries).
- For each item in self.get(“items”).
  - If (item.item\_code belongs to stock\_items and item.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code belongs to stock\_items → item.warehouse.
    - Set scr\_qty from (flt(item.qty) × flt(item.conversion\_factor)).
    - If scr\_qty.
      - Set sle from self.get\_sl\_entries(item, mapping(“actual\_qty” → flt(scr\_qty), “recalculate\_rate” → 1)).
      - If not self.is\_return.
        - Set rate\_db\_precision from 6 when cint(self.precision(“rate”, item)) ≤ 6, otherwise 9.
          - Value choice on cint(self.precision(“rate”, item)) ≤ 6 — true gives 6, false gives 9.
        - Set sle.incoming\_rate from flt(item.rate, rate\_db\_precision).
      - Otherwise.
        - If not is\_serial\_no\_wise\_valuation\_disabled(item.item\_code).
          - Set sle.outgoing\_rate from get\_rate\_for\_return(self.doctype, self.name, item.item\_code, self.return\_against, item\_row = item).
      - Evaluate sl\_entries.append(sle).
    - If flt(item.rejected\_qty) differs from 0.
      - Evaluate sl\_entries.append(self.get\_sl\_entries(item, mapping(“warehouse” → item.rejected\_warehouse, “serial\_and\_batch\_bundle” → item.get(“rejected\_serial\_and\_batch\_bundle”), “actual\_qty” → (flt(item.rejected\_qty) × ….
- Evaluate self.make\_sl\_entries(sl\_entries, allow\_negative\_stock = allow\_negative\_stock, via\_landed\_cost\_voucher = via\_landed\_cost\_voucher).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update ordered and reserved qty](operations-031.md#op-c4e2f401b17ba4), [make sl entries for supplier warehouse](operations-031.md#op-f9de798b784eba).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1051) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L728)

<a id="op-cd8d2fbac9dde4"></a>
### Subcontracting Controller.get supplied items cost

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_supplied_items_cost`

**Inputs** self, item\_row\_id, reset\_outgoing\_rate = true.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** supplied\_items\_cost.

**Local steps**

- Set supplied\_items\_cost from 0.0.
- For each item in self.get(“supplied\_items”).
  - If item.reference\_name equals item\_row\_id.
    - If (self.get(“is\_old\_subcontracting\_flow”) and reset\_outgoing\_rate and Platform.get\_cached\_value(“Item”, item.rm\_item\_code, “is\_stock\_item”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_old\_subcontracting\_flow”) → reset\_outgoing\_rate → Platform.get\_cached\_value(“Item”, item.rm\_item\_code, “is\_stock\_item”).
      - Set rate from \_get\_incoming\_rate(mapping(“item\_code” → item.rm\_item\_code, “warehouse” → self.supplier\_warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).
      - If rate &gt; 0.
        - Set item.rate from rate.
    - Set item.amount from flt((flt(item.consumed\_qty) × flt(item.rate)), item.precision(“amount”)).
    - Update supplied\_items\_cost using + item.amount.
- Return supplied\_items\_cost.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.rm\_item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1017) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L694)

<a id="op-d6e355597733e6"></a>
### Subcontracting Controller.set subcontracting order status

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_subcontracting_order_status`

**Inputs** self, update\_bin = true.

**Record and data access** resolve a document from “Subcontracting Order” via get\_doc.

**Local steps**

- If self.doctype equals “Subcontracting Order”.
  - Evaluate self.update\_status().
- Otherwise.
  - If self.doctype equals “Subcontracting Receipt”.
    - Evaluate self.\_\_get\_subcontract\_orders.
    - If self.subcontract\_orders.
      - For each sco in set(self.subcontract\_orders).
        - Set sco\_doc from Platform.get\_doc(“Subcontracting Order”, sco).
        - Evaluate sco\_doc.update\_status(update\_bin = update\_bin).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0396.json#L1009) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1041) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L718)

<a id="op-43d40c755d2e09"></a>
### Subcontracting Controller.calculate additional costs

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_calculate_additional_costs`

**Inputs** self.

**Local steps**

- Set self.total\_additional\_costs from sum(generator of flt(item.amount) for item drawn from self.get(“additional\_costs”)).
  - Draw item from self.get(“additional\_costs”).
- If self.total\_additional\_costs.
  - If self.distribute\_additional\_costs\_based\_on equals “Amount”.
    - Set total\_amt from sum(generator of flt(item.amount) for item drawn from self.get(“items”) where (not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”))).
      - Draw item from self.get(“items”), keep a combination only if ((not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“secondary\_item\_type”) → not item.get(“valuation\_type”).
    - For each item in self.items.
      - If (not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“secondary\_item\_type”) → not item.get(“valuation\_type”).
        - Set item.additional\_cost\_per\_qty from (((item.amount × self.total\_additional\_costs) ÷ total\_amt) ÷ self.get\_qty\_for\_costing(item)).
  - Otherwise.
    - Set total\_qty from sum(generator of self.get\_qty\_for\_costing(item) for item drawn from self.get(“items”) where (not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”))).
      - Draw item from self.get(“items”), keep a combination only if ((not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“secondary\_item\_type”) → not item.get(“valuation\_type”).
    - Set additional\_cost\_per\_qty from (self.total\_additional\_costs ÷ total\_qty).
    - For each item in self.items.
      - If (not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“secondary\_item\_type”) → not item.get(“valuation\_type”).
        - Set item.additional\_cost\_per\_qty from additional\_cost\_per\_qty.
- Otherwise.
  - For each item in self.items.
    - If (not item.get(“secondary\_item\_type”) and not item.get(“valuation\_type”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“secondary\_item\_type”) → not item.get(“valuation\_type”).
      - Set item.additional\_cost\_per\_qty from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get qty for costing](operations-031.md#op-17e3a48aaee02f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1001) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L678)

<a id="op-17e3a48aaee02f"></a>
### Subcontracting Controller.get qty for costing

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_qty_for_costing`

**Inputs** self, item.

**Explicit results** ((flt(item.qty) + flt(item.get(“rejected\_qty”))) + flt(item.get(“process\_loss\_qty”))).

**Local steps**

- Return ((flt(item.qty) + flt(item.get(“rejected\_qty”))) + flt(item.get(“process\_loss\_qty”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L433)

<a id="op-d49d65b463c0f2"></a>
### Subcontracting Controller.get current stock

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_get_current_stock`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Bin” via get\_value.

**Local steps**

- If self.doctype belongs to list(“Purchase Receipt”, “Subcontracting Receipt”).
  - If (self.supplier\_warehouse and self.get(“supplied\_items”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.supplier\_warehouse → self.get(“supplied\_items”).
    - Evaluate validate\_warehouse\_company(self.supplier\_warehouse, self.company).
  - For each item in self.get(“supplied\_items”).
    - If self.supplier\_warehouse.
      - Set actual\_qty from Platform.db.get\_value(“Bin”, mapping(“item\_code” → item.rm\_item\_code, “warehouse” → self.supplier\_warehouse), “actual\_qty”).
      - Set item.current\_stock from flt(actual\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1008) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L685)

<a id="op-d9a46f00d806c8"></a>
### Subcontracting Controller.sub contracted items

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_subordinate_contracted_items`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Item” via get\_all.

**Explicit results** self.\_sub\_contracted\_items.

**Local steps**

- If not hasattr(self, “\_sub\_contracted\_items”).
  - Set self.\_sub\_contracted\_items from list().
  - Set item\_codes from list(set(generator of item.item\_code for item drawn from self.get(“items”))).
    - Draw item from self.get(“items”).
  - If item\_codes.
    - Set items from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, item\_codes), “is\_sub\_contracted\_item” → 1)).
    - Set self.\_sub\_contracted\_items from list of item.name for item drawn from items.
      - Draw item from items.
- Return self.\_sub\_contracted\_items.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0396.json#L2345) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1044) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L721)

<a id="op-6675b16faf3ed6"></a>
### Subcontracting Controller.update requested qty

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_update_requested_quantity`

**Inputs** self.

**Record and data access** resolve a document from “Material Request” via get\_doc.

**Explicit failure paths** validation helper with Platform.InvalidStatusError — translated “Material Request {0} is cancelled or stopped”.format(mr).

**Local steps**

- Set material\_request\_map from mapping().
- For each d in self.get(“items”).
  - If d.material\_request\_item.
    - Evaluate material\_request\_map.setdefault(d.material\_request, list()).append(d.material\_request\_item).
- For each tuple(mr, mr\_item\_rows) in material\_request\_map.items().
  - If (mr and mr\_item\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in mr → mr\_item\_rows.
    - Set mr\_obj from Platform.get\_doc(“Material Request”, mr).
    - If (mr\_obj.status belongs to list(“Stopped”, “Cancelled”) and self.get(“\_action”) equals “submit”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in mr\_obj.status belongs to list(“Stopped”, “Cancelled”) → self.get(“\_action”) equals “submit”.
      - Call the validation error handler Platform.throw(translated “Material Request {0} is cancelled or stopped”.format(mr), Platform.InvalidStatusError).
    - Evaluate mr\_obj.update\_requested\_qty(mr\_item\_rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1049) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L726)

<a id="op-6747124770f66b"></a>
### Get item details

`operation_enterprise_controllers_subcontracting_controller_business_behavior_get_item_details`

**Inputs** items.

**Explicit results** item\_details.

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set item\_list from nested operand in the contract(nested operand in the contract).select(item.item\_code, item.item\_name, item.description, item.allow\_alternative\_item).where(item.name.isin(items)).run(as\_dict = true).
- Set item\_details from mapping().
- For each item in item\_list.
  - Set item\_details at item.item\_code from item.
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0396.json#L3019) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L991) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L668)

<a id="op-97958c6fa9c67e"></a>
### Get pending subcontracted quantity

`operation_enterprise_controllers_subcontracting_controller_business_behavior_get_pending_subcontracted_quantity`

**Inputs** doctype, name.

**Explicit results** mapping of item.name → (item at qty\_field − item.subcontracted\_qty) for item drawn from query.run(as\_dict = true).

**Local steps**

- Set qty\_field from “qty” when doctype equals “Purchase Order Item”, otherwise “stock\_qty”.
  - Value choice on doctype equals “Purchase Order Item” — true gives “qty”, false gives “stock\_qty”.
- Set table from Platform.qb.DocType(doctype).
- Set query from nested operand in the contract.qb.from\_(table).select(table.name, table at qty\_field, table.subcontracted\_qty).where(table.parent equals name).
- Return mapping of item.name → (item at qty\_field − item.subcontracted\_qty) for item drawn from query.run(as\_dict = true).
  - Draw item from query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L993) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L670)

<a id="op-e2319ba259ab58"></a>
### Make rm stock entry

`operation_enterprise_controllers_subcontracting_controller_business_behavior_make_raw_material_stock_entry`

**Inputs** subcontract\_order, rm\_items = no value, order\_doctype = “Subcontracting Order”, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from order\_doctype via get\_doc.

**Explicit results** stock\_entry · stock\_entry.as\_dict().

**Explicit failure paths** validation helper — translated “No item available for transfer.” · validation helper — translated “No Items selected for transfer.”.

**Local steps**

- If subcontract\_order.
  - Set subcontract\_order from Platform.get\_doc(order\_doctype, subcontract\_order).
  - If not rm\_items.
    - If not subcontract\_order.supplied\_items.
      - Call the validation error handler Platform.throw(translated “No item available for transfer.”).
    - Set rm\_items from subcontract\_order.supplied\_items.
  - Set fg\_item\_code\_list from list(set(generator of (item.get(“main\_item\_code”) or item.get(“item\_code”)) for item drawn from rm\_items)).
    - Draw item from rm\_items.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“main\_item\_code”) → item.get(“item\_code”).
  - If fg\_item\_code\_list.
    - Set rm\_item\_code\_list from tuple(set(generator of item.get(“rm\_item\_code”) for item drawn from rm\_items)).
      - Draw item from rm\_items.
    - Set item\_wh from get\_item\_details(rm\_item\_code\_list).
    - Set tuple(field\_no\_map, rm\_detail\_field) from tuple(“purchase\_order”, “sco\_rm\_detail”).
    - If order\_doctype equals “Purchase Order”.
      - Set tuple(field\_no\_map, rm\_detail\_field) from tuple(“subcontracting\_order”, “po\_detail”).
    - If (target\_doc and target\_doc.get(“items”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → target\_doc.get(“items”).
      - Set target\_doc.items from list().
    - Bind local operation post\_process for subsequent calls.
    - Set stock\_entry from get\_mapped\_doc(order\_doctype, subcontract\_order.name, mapping(order\_doctype → mapping(“doctype” → “Stock Entry”, “field\_map” → mapping(“supplier” → “supplier”, “supplier\_name” → “supplier\_name”, “supplier\_ ….
    - If target\_doc.
      - Return stock\_entry.
    - Otherwise.
      - Return stock\_entry.as\_dict().
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “No Items selected for transfer.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L671)

<a id="op-639d6806039872"></a>
### Make rm stock entry.post process

`operation_enterprise_controllers_subcontracting_controller_business_behavior_make_raw_material_stock_entry_post_process`

**Inputs** source\_doc, target\_doc.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- Set target\_doc.purpose from “Send to Subcontractor”.
- If order\_doctype equals “Purchase Order”.
  - Set target\_doc.purchase\_order from source\_doc.name.
- Otherwise.
  - Set target\_doc.subcontracting\_order from source\_doc.name.
- Evaluate target\_doc.set\_stock\_entry\_type().
- Set over\_transfer\_allowance from Platform.get\_single\_value(“Buying Settings”, “over\_transfer\_allowance”).
- For each fg\_item\_code in fg\_item\_code\_list.
  - For each rm\_item in rm\_items.
    - If (rm\_item.get(“main\_item\_code”) equals fg\_item\_code or rm\_item.get(“item\_code”) equals fg\_item\_code).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in rm\_item.get(“main\_item\_code”) equals fg\_item\_code → rm\_item.get(“item\_code”) equals fg\_item\_code.
      - Set rm\_item\_code from rm\_item.get(“rm\_item\_code”).
      - Set qty from (rm\_item.get(“qty”) or max((rm\_item.get(“required\_qty”) − rm\_item.get(“total\_supplied\_qty”)), 0)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in rm\_item.get(“qty”) → max((rm\_item.get(“required\_qty”) − rm\_item.get(“total\_supplied\_qty”)), 0).
      - If (qty ≤ 0 and rm\_item.get(“total\_supplied\_qty”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty ≤ 0 → rm\_item.get(“total\_supplied\_qty”).
        - Set per\_transferred from (flt((rm\_item.get(“total\_supplied\_qty”) ÷ rm\_item.get(“required\_qty”)), Platform.db.get\_default(“float\_precision”)) × 100).
        - If per\_transferred ≥ (100 + over\_transfer\_allowance).
          - Continue with the next iteration or loop test.
      - Set items\_dict from mapping(rm\_item\_code → mapping(rm\_detail\_field → rm\_item.get(“name”), “item\_name” → (rm\_item.get(“item\_name”) or nested operand in the contract.get(rm\_item\_code, mapping()).get(“item\_name”, empty text)), “ ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in rm\_item.get(“item\_name”) → item\_wh.get(rm\_item\_code, mapping()).get(“item\_name”, empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in rm\_item.get(“warehouse”) → rm\_item.get(“reserve\_warehouse”).
        - Value choice on rm\_item.get(“use\_serial\_batch\_fields”) — true gives rm\_item.get(“serial\_no”), false gives no value.
        - Value choice on rm\_item.get(“use\_serial\_batch\_fields”) — true gives rm\_item.get(“batch\_no”), false gives no value.
      - Evaluate target\_doc.add\_to\_stock\_entry\_detail(items\_dict).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Buying Settings”, “over\_transfer\_allowance”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L672)

<a id="op-a00929931bdda7"></a>
### Add items in ste

`operation_enterprise_controllers_subcontracting_controller_business_behavior_add_items_in_stock_entry`

**Inputs** ste\_doc, row, qty, rm\_details, rm\_detail\_field = “sco\_rm\_detail”, batch\_no = no value.

**Local steps**

- Set item from ste\_doc.append(“items”, row.item\_details).
- Set rm\_detail from list(set(row.get(formatted text {rm\_detail\_field}s)).intersection(rm\_details)).
- Evaluate item.update(mapping(“qty” → qty, “batch\_no” → batch\_no, “basic\_rate” → row.item\_details at “rate”, rm\_detail\_field → rm\_detail at 0 when rm\_detail, otherwise empty text, …)).
  - Value choice on rm\_detail — true gives rm\_detail at 0, false gives empty text.
  - Value choice on row.serial\_no — true gives whitespace '\\n'.join(row.serial\_no), false gives empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L990) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L667)

<a id="op-a0e5301af6b42d"></a>
### Make return stock entry for subcontract

`operation_enterprise_controllers_subcontracting_controller_business_behavior_make_return_stock_entry_for_subcontract`

**Inputs** available\_materials, order\_doc, rm\_details, order\_doctype = “Subcontracting Order”.

**Explicit results** ste\_doc.

**Local steps**

- Set rm\_detail\_field from “po\_detail” when order\_doctype equals “Purchase Order”, otherwise “sco\_rm\_detail”.
  - Value choice on order\_doctype equals “Purchase Order” — true gives “po\_detail”, false gives “sco\_rm\_detail”.
- Bind local operation post\_process for subsequent calls.
- Set ste\_doc from get\_mapped\_doc(order\_doctype, order\_doc.name, mapping(order\_doctype → mapping(“doctype” → “Stock Entry”, “field\_no\_map” → list(“purchase\_order”, “subcontracting\_order”))), ignore\_child\_tables = true, postp ….
- Return ste\_doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0397.json#L523) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L673)
