# Subcontracting · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subcontracting receipt

[Record definition](../../../../data/record-types/subcontracting_receipt.json)

<a id="op-de0bd256ce04ce"></a>
### Subcontracting Receipt.get returned receipt rows

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_get_returned_receipt_rows`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Subcontracting Receipt Item” via get\_all.

**Explicit results** mapping() · mapping of row.name → row for row drawn from Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against), fields = list(“name”, “item\_code”, “qty”, “received\_qty”, …)).

**Local steps**

- If not (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Return mapping().
- Return mapping of row.name → row for row drawn from Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against), fields = list(“name”, “item\_code”, “qty”, “received\_qty”, …)).
  - Draw row from Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against), fields = list(“name”, “item\_code”, “qty”, “received\_qty”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1214)

<a id="op-c5b3c1d00e4f91"></a>
### Subcontracting Receipt.link returned secondary items

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_link_returned_secondary_items`

**Inputs** self, original\_rows.

**Explicit results** no value.

**Local steps**

- If not original\_rows.
  - Return no value.
- Set secondary\_rows from mapping().
- Set legacy\_rows from defaultdict(list).
- For each row in original\_rows.values().
  - If row.bom\_secondary\_item.
    - Set secondary\_rows at tuple(row.reference\_name, row.bom\_secondary\_item) from row.name.
  - Otherwise.
    - If (row.secondary\_item\_type or row.valuation\_type).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.secondary\_item\_type → row.valuation\_type.
      - Evaluate legacy\_rows at row.reference\_name.append(row).
- For each fg\_row in self.items.
  - If (fg\_row.bom and fg\_row.subcontracting\_receipt\_item belongs to legacy\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fg\_row.bom → fg\_row.subcontracting\_receipt\_item belongs to legacy\_rows.
    - Evaluate secondary\_rows.update(self.pair\_legacy\_secondary\_rows(fg\_row, legacy\_rows at fg\_row.subcontracting\_receipt\_item)).
- Set returned\_fg\_rows from mapping of row.name → row.subcontracting\_receipt\_item for row drawn from self.items where row.bom.
  - Draw row from self.items, keep a combination only if (row.bom).
- For each row in self.items.
  - If row.bom\_secondary\_item.
    - Set row.subcontracting\_receipt\_item from secondary\_rows.get(tuple(returned\_fg\_rows.get(row.reference\_name), row.bom\_secondary\_item)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [pair legacy secondary rows](operations-006.md#op-648b93241dfeb1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1217)

<a id="op-648b93241dfeb1"></a>
### Subcontracting Receipt.pair legacy secondary rows

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_pair_legacy_secondary_rows`

**Inputs** fg\_row, receipt\_rows.

**Wrappers, in declaration order** staticmethod.

**Record and data access** resolve a document from “BOM” via get\_cached\_doc.

**Explicit results** pairs.

**Local steps**

- Set bom\_rows from Platform.get\_cached\_doc(“BOM”, fg\_row.bom).secondary\_items.
- Set pairs from mapping().
- For each item\_code in set of row.item\_code for row drawn from receipt\_rows.
  - Draw row from receipt\_rows.
  - Set by\_qty from sorted(generator of row for row drawn from receipt\_rows where row.item\_code equals item\_code, key = deferred anonymous expression).
    - Draw row from receipt\_rows, keep a combination only if (row.item\_code equals item\_code).
  - Set bom\_by\_qty from sorted(generator of row for row drawn from bom\_rows where row.item\_code equals item\_code, key = deferred anonymous expression).
    - Draw row from bom\_rows, keep a combination only if (row.item\_code equals item\_code).
  - For each tuple(receipt\_row, bom\_row) in zip(by\_qty, bom\_by\_qty, strict = false).
    - Set pairs at tuple(fg\_row.subcontracting\_receipt\_item, bom\_row.name) from receipt\_row.name.
- Return pairs.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“BOM”, fg\_row.bom).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1221)

<a id="op-5ad957f50a50d5"></a>
### Subcontracting Receipt.set remaining secondary qty

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_set_remaining_secondary_qty`

**Inputs** self, original\_rows.

**Explicit results** no value.

**Local steps**

- Set last\_fg\_rows from list of row.name for row drawn from self.items where self.returns\_last\_finished\_goods(row, original\_rows).
  - Draw row from self.items, keep a combination only if (self.returns\_last\_finished\_goods(row, original\_rows)).
- If not last\_fg\_rows.
  - Return no value.
- Set already\_returned from get\_already\_returned\_items(self).
- For each row in self.items.
  - If not (row.subcontracting\_receipt\_item and row.reference\_name belongs to last\_fg\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.subcontracting\_receipt\_item → row.reference\_name belongs to last\_fg\_rows.
    - Continue with the next iteration or loop test.
  - Set original\_row from original\_rows at row.subcontracting\_receipt\_item.
  - Set returned from already\_returned.get(tuple(row.item\_code, row.subcontracting\_receipt\_item), mapping()).
  - Set row.received\_qty from flt((flt(returned.get(“received\_qty”)) − original\_row.received\_qty), row.precision(“received\_qty”)).
  - Set row.qty from flt((flt(returned.get(“qty”)) − original\_row.qty), row.precision(“qty”)).
  - Set row.process\_loss\_qty from flt((row.received\_qty − row.qty), row.precision(“process\_loss\_qty”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [returns last finished goods](operations-006.md#op-702853e2bbc52a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1227)

<a id="op-702853e2bbc52a"></a>
### Subcontracting Receipt.returns last finished goods

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_returns_last_finished_goods`

**Inputs** row, original\_rows.

**Wrappers, in declaration order** staticmethod.

**Explicit results** false · flt((original\_row.returned\_qty − flt(row.received\_qty)), precision) ≥ flt(original\_row.received\_qty, precision).

**Local steps**

- Set original\_row from original\_rows.get(row.subcontracting\_receipt\_item).
- If not (row.bom and original\_row).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.bom → original\_row.
  - Return false.
- Set precision from row.precision(“received\_qty”).
- Return flt((original\_row.returned\_qty − flt(row.received\_qty)), precision) ≥ flt(original\_row.received\_qty, precision).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1222)

<a id="op-486e92128f82ad"></a>
### Subcontracting Receipt.calculate percentage secondary rows

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_calculate_percentage_secondary_rows`

**Inputs** self, percentage\_rows, secondary\_items\_cost\_map.

**Record and data access** read “BOM Secondary Item” via get\_all.

**Local steps**

- Set allocation\_map from mapping().
- Set names from list of row.bom\_secondary\_item for row drawn from percentage\_rows where row.bom\_secondary\_item.
  - Draw row from percentage\_rows, keep a combination only if (row.bom\_secondary\_item).
- If names.
  - Set allocation\_map from dict(Platform.get\_all(“BOM Secondary Item”, filters = mapping(“name” → tuple(“in”, names)), fields = list(“name”, “cost\_allocation\_per”), as\_list = true)).
- Set fg\_rows from mapping of row.name → row for row drawn from self.get(“items”) where row.bom.
  - Draw row from self.get(“items”), keep a combination only if (row.bom).
- For each item in percentage\_rows.
  - Set qty from (flt(item.received\_qty) − flt(item.process\_loss\_qty)).
  - Set fg\_row from fg\_rows.get(item.reference\_name).
  - If (qty and fg\_row and item.bom\_secondary\_item belongs to allocation\_map).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty → fg\_row → item.bom\_secondary\_item belongs to allocation\_map.
    - Set item.rate from self.get\_percentage\_secondary\_rate(fg\_row, flt(allocation\_map at item.bom\_secondary\_item), qty, secondary\_items\_cost\_map.get(item.reference\_name, 0)).
  - Set item.amount from (qty × flt(item.rate)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get percentage secondary rate](operations-006.md#op-e0f548e9c726f2).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L4059) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1028)

<a id="op-e60608559a3948"></a>
### Subcontracting Receipt.get secondary item valuation rate

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_get_secondary_item_valuation_rate`

**Inputs** self, item.

**Explicit results** (get\_valuation\_rate(item.item\_code, (item.warehouse or self.set\_warehouse), self.doctype, self.name, currency = Enterprise.get\_company\_currency(self.company), company = self.company) or item.rate).

**Local steps**

- Return (get\_valuation\_rate(item.item\_code, (item.warehouse or self.set\_warehouse), self.doctype, self.name, currency = Enterprise.get\_company\_currency(self.company), company = self.company) or item.rate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_valuation\_rate(item.item\_code, (item.warehouse or self.set\_warehouse), self.doctype, self.name, currency = Enterprise.get\_company\_currency(self.company), company = self.company) → item.rate.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.warehouse → self.set\_warehouse.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L4637) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1034)

<a id="op-d14ba1833ac8ef"></a>
### Subcontracting Receipt.add secondary items of fg row

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_add_secondary_items_of_finished_goods_row`

**Inputs** self, item, fg\_qty\_before = 0.0.

**Record and data access** resolve a document from “BOM” via get\_doc.

**Local steps**

- Set bom from Platform.get\_doc(“BOM”, item.bom).
- Set warehouse from (self.set\_warehouse or item.warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.set\_warehouse → item.warehouse.
- Set own\_cost from 0.0.
- Set percentage\_rows from list().
- For each secondary\_item in bom.secondary\_items.
  - If secondary\_item.valuation\_type belongs to tuple(“Valuation Rate”, “Manual”).
    - If row bound to self.append\_secondary\_item(item, bom, secondary\_item, warehouse, …).
      - Update own\_cost using + (flt(row.qty) × flt(row.rate)).
  - Otherwise.
    - Evaluate percentage\_rows.append(secondary\_item).
- For each secondary\_item in percentage\_rows.
  - Evaluate self.append\_secondary\_item(item, bom, secondary\_item, warehouse, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append secondary item](operations-006.md#op-6592c55751e61f).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1023)

<a id="op-6592c55751e61f"></a>
### Subcontracting Receipt.append secondary item

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_append_secondary_item`

**Inputs** self, item, bom, secondary\_item, warehouse, own\_cost = 0.0, fg\_qty\_before = 0.0.

**Explicit results** no value · self.append(“items”, mapping(“secondary\_item\_type” → secondary\_item.secondary\_item\_type, “valuation\_type” → secondary\_item.valuation\_type, “bom\_secondary\_item” → secondary\_item.name, “reference\_name” → ite ….

**Local steps**

- Set per\_unit from (secondary\_item.stock\_qty ÷ bom.quantity).
- Set received\_qty from self.get\_secondary\_qty(item, per\_unit, fg\_qty\_before, “received\_qty”).
- Set qty from self.get\_secondary\_qty(item, (per\_unit − (secondary\_item.process\_loss\_qty ÷ bom.quantity)), fg\_qty\_before, “qty”).
- If (self.is\_return and not qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not qty.
  - Return no value.
- Set rate from self.get\_secondary\_item\_rate(item, secondary\_item, warehouse, qty, …).
- Return self.append(“items”, mapping(“secondary\_item\_type” → secondary\_item.secondary\_item\_type, “valuation\_type” → secondary\_item.valuation\_type, “bom\_secondary\_item” → secondary\_item.name, “reference\_name” → ite ….
  - Value choice on secondary\_item.valuation\_type does not belong to tuple(“Valuation Rate”, “Manual”) — true gives received\_qty, false gives (flt(item.qty) × (flt(secondary\_item.stock\_qty) ÷ flt(bom.quantity))).

**Methods declared on this owner** [get secondary qty](operations-006.md#op-1fcf8da88c3038), [get secondary item rate](operations-006.md#op-7fb71bb421b475).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1024)

<a id="op-1fcf8da88c3038"></a>
### Subcontracting Receipt.get secondary qty

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_get_secondary_qty`

**Inputs** item, per\_unit, fg\_qty\_before, fieldname.

**Wrappers, in declaration order** staticmethod.

**Explicit results** flt((flt((fg\_qty\_after × per\_unit), precision) − flt((fg\_qty\_before × per\_unit), precision)), precision).

**Local steps**

- Set precision from item.precision(fieldname).
- Set fg\_qty\_after from (fg\_qty\_before + flt(item.received\_qty)).
- Return flt((flt((fg\_qty\_after × per\_unit), precision) − flt((fg\_qty\_before × per\_unit), precision)), precision).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1216)

<a id="op-7fb71bb421b475"></a>
### Subcontracting Receipt.get secondary item rate

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_get_secondary_item_rate`

**Inputs** self, item, secondary\_item, warehouse, qty, own\_cost.

**Explicit results** 0 · (flt(secondary\_item.base\_cost) ÷ flt(secondary\_item.stock\_qty)) · rate · self.get\_percentage\_secondary\_rate(item, secondary\_item.cost\_allocation\_per, qty, own\_cost).

**Local steps**

- If secondary\_item.valuation\_type equals “Manual”.
  - If not flt(secondary\_item.stock\_qty).
    - Return 0.
  - Return (flt(secondary\_item.base\_cost) ÷ flt(secondary\_item.stock\_qty)).
- If secondary\_item.valuation\_type equals “Valuation Rate”.
  - Set rate from get\_valuation\_rate(secondary\_item.item\_code, warehouse, self.doctype, self.name, currency = Enterprise.get\_company\_currency(self.company), company = self.company).
  - If (not rate and secondary\_item.stock\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not rate → secondary\_item.stock\_qty.
    - Set rate from (flt(secondary\_item.base\_cost) ÷ flt(secondary\_item.stock\_qty)).
  - Return rate.
- Return self.get\_percentage\_secondary\_rate(item, secondary\_item.cost\_allocation\_per, qty, own\_cost).

**Methods declared on this owner** [get percentage secondary rate](operations-006.md#op-e0f548e9c726f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1033)

<a id="op-e0f548e9c726f2"></a>
### Subcontracting Receipt.get percentage secondary rate

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_get_percentage_secondary_rate`

**Inputs** self, fg\_row, cost\_allocation\_per, qty, own\_cost.

**Explicit results** ((fg\_item\_cost × (cost\_allocation\_per ÷ 100)) ÷ qty).

**Local steps**

- Set received\_qty from (flt(fg\_row.received\_qty) or flt(fg\_row.qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(fg\_row.received\_qty) → flt(fg\_row.qty).
- Set lcv\_cost\_per\_qty from (flt(fg\_row.landed\_cost\_voucher\_amount) ÷ received\_qty) when received\_qty, otherwise 0.0.
  - Value choice on received\_qty — true gives (flt(fg\_row.landed\_cost\_voucher\_amount) ÷ received\_qty), false gives 0.0.
- Set fg\_item\_cost from (((((flt(nested operand in the contract.rm\_cost\_per\_qty) + flt(nested operand in the contract.additional\_cost\_per\_qty)) + flt(lcv\_cost\_per\_qty)) + flt(fg\_row.service\_cost\_per\_qty)) × flt(fg\_row.received\_qt ….
- Return ((fg\_item\_cost × (cost\_allocation\_per ÷ 100)) ÷ qty).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1031)

<a id="op-92dee3b2ff5c62"></a>
### Subcontracting Receipt.remove secondary items

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_remove_secondary_items`

**Inputs** self.

**Local steps**

- For each item in list(self.items).
  - If (item.secondary\_item\_type or item.valuation\_type).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → item.valuation\_type.
    - Evaluate self.remove(item).
  - Otherwise.
    - Set item.secondary\_items\_cost\_per\_qty from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0958.json#L6686) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1042)

<a id="op-faf0205223b1fd"></a>
### Subcontracting Receipt.set missing values

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_missing_values`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set\_available\_qty\_for\_consumption().
- Evaluate self.set\_additional\_costs().
- Evaluate self.calculate\_items\_qty\_and\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set available qty for consumption](operations-006.md#op-28b131e7efc08e), [set additional costs](operations-006.md#op-c754a992ae004a), [calculate items qty and amount](operations-006.md#op-7b426cf1521780).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1050)

<a id="op-c754a992ae004a"></a>
### Subcontracting Receipt.set additional costs

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_set_additional_costs`

**Inputs** self.

**Local steps**

- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Evaluate self.set\_additional\_costs\_for\_return().
- Otherwise.
  - Evaluate self.set\_additional\_costs\_base\_amount().
  - Evaluate self.calculate\_additional\_costs().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set additional costs for return](operations-006.md#op-9e418eaa2f5b3b), [set additional costs base amount](operations-006.md#op-9ff0a7658cfb85).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1223)

<a id="op-9e418eaa2f5b3b"></a>
### Subcontracting Receipt.set additional costs for return

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_set_additional_costs_for_return`

**Inputs** self.

**Record and data access** resolve a document from “Subcontracting Receipt” via get\_doc.

**Local steps**

- Set original from Platform.get\_doc(“Subcontracting Receipt”, self.return\_against, check\_permission = “read”).
- Set original\_rows from mapping of row.name → row for row drawn from original.items where row.bom.
  - Draw row from original.items, keep a combination only if (row.bom).
- Set basis from “amount” when original.distribute\_additional\_costs\_based\_on equals “Amount”, otherwise “qty”.
  - Value choice on original.distribute\_additional\_costs\_based\_on equals “Amount” — true gives “amount”, false gives “qty”.
- Set total\_basis from sum(generator of flt(row.get(basis)) for row drawn from original\_rows.values()).
  - Draw row from original\_rows.values().
- Set total\_cost from sum(generator of (self.get\_qty\_for\_costing(row) × flt(row.additional\_cost\_per\_qty)) for row drawn from original\_rows.values()).
  - Draw row from original\_rows.values().
- Set returned\_basis, returned\_cost from 0.0.
- For each row in self.items.
  - Set original\_row from original\_rows.get(row.subcontracting\_receipt\_item).
  - If not original\_row.
    - Continue with the next iteration or loop test.
  - Set row.additional\_cost\_per\_qty from 0.0.
  - If (flt(original\_row.qty) and row.warehouse and row.warehouse differs from original\_row.rejected\_warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(original\_row.qty) → row.warehouse → row.warehouse differs from original\_row.rejected\_warehouse.
    - Set row\_returned\_cost from (((flt(row.qty) × flt(original\_row.additional\_cost\_per\_qty)) × self.get\_qty\_for\_costing(original\_row)) ÷ flt(original\_row.qty)).
    - Set costing\_qty from self.get\_qty\_for\_costing(row).
    - Set row.additional\_cost\_per\_qty from (row\_returned\_cost ÷ costing\_qty) when costing\_qty, otherwise 0.0.
      - Value choice on costing\_qty — true gives (row\_returned\_cost ÷ costing\_qty), false gives 0.0.
    - Update returned\_cost using + row\_returned\_cost.
    - Update returned\_basis using + ((flt(row.qty) × flt(original\_row.get(basis))) ÷ flt(original\_row.qty)).
- If total\_cost.
  - Set ratio from (returned\_cost ÷ total\_cost).
- Otherwise.
  - Set ratio from (returned\_basis ÷ total\_basis) when total\_basis, otherwise 0.0.
    - Value choice on total\_basis — true gives (returned\_basis ÷ total\_basis), false gives 0.0.
- Evaluate self.set(“additional\_costs”, list()).
- For each row in original.additional\_costs.
  - Evaluate self.append(“additional\_costs”, mapping(“expense\_account” → row.expense\_account, “account\_currency” → row.account\_currency, “exchange\_rate” → row.exchange\_rate, “description” → row.description, …)).
- Set self.total\_additional\_costs from sum(generator of flt(row.amount) for row drawn from self.additional\_costs).
  - Draw row from self.additional\_costs.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1225)

<a id="op-9ff0a7658cfb85"></a>
### Subcontracting Receipt.set additional costs base amount

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_set_additional_costs_base_amount`

**Inputs** self.

**Local steps**

- For each row in self.get(“additional\_costs”).
  - Set row.base\_amount from flt((flt(row.amount) × (flt(row.exchange\_rate) or 1)), row.precision(“base\_amount”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.exchange\_rate) → 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1224)

<a id="op-28b131e7efc08e"></a>
### Subcontracting Receipt.set available qty for consumption

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_set_available_quantity_for_consumption`

**Inputs** self.

**Local steps**

- Set supplied\_items\_details from mapping().
- Set sco\_supplied\_item from Platform.qb.DocType(“Subcontracting Order Supplied Item”).
- For each item in self.get(“items”).
  - Set supplied\_items from nested operand in the contract(nested operand in the contract).select(sco\_supplied\_item.rm\_item\_code, sco\_supplied\_item.reference\_name, nested operand in the contract.as\_(“available\_qty”)).where(((nested o ….
  - If supplied\_items.
    - Set supplied\_items\_details at item.name from mapping().
    - For each supplied\_item in supplied\_items.
      - If supplied\_item.rm\_item\_code does not belong to supplied\_items\_details at item.name.
        - Set supplied\_items\_details at item.name at supplied\_item.rm\_item\_code from 0.0.
      - Update supplied\_items\_details at item.name at supplied\_item.rm\_item\_code using + supplied\_item.available\_qty.
- After normal loop exhaustion.
  - For each item in self.get(“supplied\_items”).
    - Set item.available\_qty\_for\_consumption from supplied\_items\_details.get(item.reference\_name, mapping()).get(item.rm\_item\_code, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1046)

<a id="op-7b426cf1521780"></a>
### Subcontracting Receipt.calculate items qty and amount

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_calculate_items_quantity_and_amount`

**Inputs** self.

**Record and data access** read “BOM” via get\_value.

**Local steps**

- Set rm\_cost\_map from mapping().
- For each item in (self.get(“supplied\_items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“supplied\_items”) → list().
  - Set item.amount from (flt(item.consumed\_qty) × flt(item.rate)).
  - If item.reference\_name belongs to rm\_cost\_map.
    - Update rm\_cost\_map at item.reference\_name using + item.amount.
  - Otherwise.
    - Set rm\_cost\_map at item.reference\_name from item.amount.
- Set secondary\_items\_cost\_map from mapping().
- Set percentage\_rows from list().
- Set is\_return from (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
- For each item in (self.get(“items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“items”) → list().
  - If not (item.secondary\_item\_type or item.valuation\_type).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → item.valuation\_type.
    - Continue with the next iteration or loop test.
  - If is\_return.
    - Set item.rate from get\_rate\_for\_return(self.doctype, self.name, item.item\_code, self.return\_against, item\_row = item).
  - Otherwise.
    - If item.valuation\_type equals “Valuation Rate”.
      - Set item.rate from self.get\_secondary\_item\_valuation\_rate(item).
  - If item.valuation\_type belongs to tuple(“Valuation Rate”, “Manual”).
    - Set item.amount from (flt(item.qty) × flt(item.rate)).
    - Set secondary\_items\_cost\_map at item.reference\_name from (secondary\_items\_cost\_map.get(item.reference\_name, 0) + item.amount).
  - Otherwise.
    - If not is\_return.
      - Evaluate percentage\_rows.append(item).
- Evaluate self.calculate\_percentage\_secondary\_rows(percentage\_rows, secondary\_items\_cost\_map).
- Set rejected\_return\_rows from self.get\_rejected\_return\_rows().
- Set received\_qty\_ratios from self.get\_received\_qty\_ratios\_for\_return(rejected\_return\_rows).
- Set returned\_costs from self.get\_returned\_costs().
- Set total\_qty, total\_amount from 0.
- For each item in (self.get(“items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“items”) → list().
  - If (not item.secondary\_item\_type and not item.valuation\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.secondary\_item\_type → not item.valuation\_type.
    - Set returned from returned\_costs.get(item.name).
    - If returned.
      - Set item.service\_cost\_per\_qty from 0.0 when item.name belongs to rejected\_return\_rows, otherwise returned.service\_cost\_per\_qty.
        - Value choice on item.name belongs to rejected\_return\_rows — true gives 0.0, false gives returned.service\_cost\_per\_qty.
    - If item.qty.
      - If item.name belongs to rm\_cost\_map.
        - Set item.rm\_supp\_cost from rm\_cost\_map at item.name.
        - Set item.rm\_cost\_per\_qty from (item.rm\_supp\_cost ÷ (item.received\_qty or item.qty)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.received\_qty → item.qty.
        - Evaluate rm\_cost\_map.pop(item.name).
      - If (returned and item.name does not belong to rejected\_return\_rows).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in returned → item.name does not belong to rejected\_return\_rows.
        - Set item.secondary\_items\_cost\_per\_qty from returned.secondary\_items\_cost\_per\_qty.
      - Otherwise.
        - If item.name belongs to secondary\_items\_cost\_map.
          - Set item.secondary\_items\_cost\_per\_qty from (secondary\_items\_cost\_map at item.name ÷ (item.received\_qty or item.qty)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.received\_qty → item.qty.
          - Evaluate secondary\_items\_cost\_map.pop(item.name).
        - Otherwise.
          - Set item.secondary\_items\_cost\_per\_qty from 0.
    - Set lcv\_cost\_per\_qty from 0.0.
    - If item.landed\_cost\_voucher\_amount.
      - Set lcv\_cost\_per\_qty from (item.landed\_cost\_voucher\_amount ÷ (item.received\_qty or item.qty)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.received\_qty → item.qty.
    - Set item.rate from ((((flt(item.rm\_cost\_per\_qty) + flt(item.service\_cost\_per\_qty)) + flt(item.additional\_cost\_per\_qty)) + flt(lcv\_cost\_per\_qty)) − flt(item.secondary\_items\_cost\_per\_qty)).
  - If item.bom.
    - Set item.received\_qty from self.get\_qty\_for\_costing(item).
    - If item.name belongs to received\_qty\_ratios.
      - Set additional\_cost from (flt(item.received\_qty) × flt(item.additional\_cost\_per\_qty)).
      - Set amount from (((flt(item.qty) × received\_qty\_ratios at item.name) × (flt(item.rate) − flt(item.additional\_cost\_per\_qty))) + additional\_cost).
    - Otherwise.
      - Set amount from (flt(item.received\_qty) × flt(item.rate)).
    - Set item.amount from (amount × (Platform.get\_value(“BOM”, item.bom, “cost\_allocation\_per”) ÷ 100)).
    - Set item.rate from (item.amount ÷ (item.qty or item.rejected\_qty)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.qty → item.rejected\_qty.
  - Otherwise.
    - Set item.qty from (flt(item.received\_qty) − flt(item.process\_loss\_qty)).
    - Set item.amount from (flt(item.qty) × flt(item.rate)).
  - Update total\_qty using + (flt(item.qty) + flt(item.rejected\_qty)).
  - Update total\_amount using + item.amount.
- After normal loop exhaustion.
  - Set self.total\_qty from total\_qty.
  - Set self.total from total\_amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get secondary item valuation rate](operations-006.md#op-e60608559a3948), [calculate percentage secondary rows](operations-006.md#op-486e92128f82ad), [get received qty ratios for return](operations-006.md#op-0e06101abbb8d5), [get returned costs](operations-006.md#op-43f2576976f476).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1027)

<a id="op-43f2576976f476"></a>
### Subcontracting Receipt.get returned costs

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_get_returned_costs`

**Inputs** self.

**Declared result** dict at tuple(str, Platform.\_dict).

**Record and data access** read “Subcontracting Receipt Item” via get\_all.

**Explicit results** mapping() · mapping of item.name → received\_rows at item.subcontracting\_receipt\_item for item drawn from self.items where item.subcontracting\_receipt\_item belongs to received\_rows.

**Local steps**

- If not (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Return mapping().
- Set received\_rows from mapping of row.name → row for row drawn from Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against, “parenttype” → “Subcontracting Receipt”), fields = list(“name” ….
  - Draw row from Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against, “parenttype” → “Subcontracting Receipt”), fields = list(“name”, “service\_cost\_per\_qty”, “secondary\_items\_co ….
- Return mapping of item.name → received\_rows at item.subcontracting\_receipt\_item for item drawn from self.items where item.subcontracting\_receipt\_item belongs to received\_rows.
  - Draw item from self.items, keep a combination only if (item.subcontracting\_receipt\_item belongs to received\_rows).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1213)

<a id="op-0e06101abbb8d5"></a>
### Subcontracting Receipt.get received qty ratios for return

`operation_enterprise_binding_enterprise_subcontracting_doctype_subcontracting_receipt_subcontracting_receipt_subcontractingreceipt_get_received_qty_ratios_for_return`

**Inputs** self, rejected\_return\_rows.

**Declared result** dict at tuple(str, float).

**Record and data access** read “Subcontracting Receipt Item” via get\_all.

**Explicit results** mapping() · ratios.

**Local steps**

- If not (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Return mapping().
- Set original\_rows from mapping of row.name → row for row drawn from Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against, “parenttype” → “Subcontracting Receipt”), fields = list(“name” ….
  - Draw row from Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against, “parenttype” → “Subcontracting Receipt”), fields = list(“name”, “qty”, “received\_qty”)).
- Set ratios from mapping().
- For each item in self.items.
  - Set original\_row from original\_rows.get(item.subcontracting\_receipt\_item).
  - If (original\_row and flt(original\_row.qty) and item.name does not belong to rejected\_return\_rows).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in original\_row → flt(original\_row.qty) → item.name does not belong to rejected\_return\_rows.
    - Set ratios at item.name from (flt(original\_row.received\_qty) ÷ flt(original\_row.qty)).
- Return ratios.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1212)

<a id="op-3734715e59eb98"></a>
### Subcontracting Receipt.validate secondary items

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_validate_secondary_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Secondary Item Qty cannot be zero”.format(item.idx) · validation helper — translated “Row #{0}: Rejected Qty cannot be set for Secondary Item {1}.”.format(item.idx, Platform.bold(item.item\_code)) · validation helper — translated “Row #{0}: Finished Good reference is mandatory for Secondary Item {1}.”.format(item.idx, Platform.bold(item.item\_code)).

**Local steps**

- For each item in self.items.
  - If (item.secondary\_item\_type or item.valuation\_type).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → item.valuation\_type.
    - If not item.qty.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Secondary Item Qty cannot be zero”.format(item.idx)).
    - If item.rejected\_qty.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Rejected Qty cannot be set for Secondary Item {1}.”.format(item.idx, Platform.bold(item.item\_code))).
    - If not item.reference\_name.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good reference is mandatory for Secondary Item {1}.”.format(item.idx, Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L2285) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1573) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1063)

<a id="op-fbb0fd0afaa45e"></a>
### Subcontracting Receipt.validate accepted warehouse

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_validate_accepted_warehouse`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Accepted Warehouse is mandatory for the accepted Item {1}”.format(item.idx, item.item\_code) · validation helper — translated “Row #{0}: Accepted Warehouse and Rejected Warehouse cannot be same”.format(item.idx).

**Local steps**

- For each item in self.get(“items”).
  - If (flt(item.qty) and not item.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(item.qty) → not item.warehouse.
    - If self.set\_warehouse.
      - Set item.warehouse from self.set\_warehouse.
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Accepted Warehouse is mandatory for the accepted Item {1}”.format(item.idx, item.item\_code)).
  - If (item.get(“warehouse”) and item.get(“warehouse”) equals item.get(“rejected\_warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“warehouse”) → item.get(“warehouse”) equals item.get(“rejected\_warehouse”).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Accepted Warehouse and Rejected Warehouse cannot be same”.format(item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0959.json#L2648) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1569) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1059)

<a id="op-a0df6aa25c0286"></a>
### Subcontracting Receipt.validate bom required qty

`operation_enterprise_subcontracting_record_definitions_subcontracting_receipt_business_behavior_subcontracting_receipt_validate_bill_of_materials_required_quantity`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with BOMQuantityError — msg.

**Local steps**

- If (self.is\_return or (Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”) equals “Material Transferred for Subcontract” and not Platform.db.get\_single\_value(“Bu ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → (Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”) equals “Material Transferred for Subcontract” and not Platform.db.get\_single\_value(“Buying Settings”, “va ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”) equals “Material Transferred for Subcontract” → not Platform.db.get\_single\_value(“Buying Settings”, “validate\_consumed\_qty”).
  - Return no value.
- Set precision from Platform.get\_precision(“Subcontracting Receipt Item”, “qty”).
- Set rm\_consumed\_dict from self.get\_rm\_wise\_consumed\_qty().
- For each tuple(rm\_item\_code, required) in self.get\_rm\_wise\_required\_qty(precision).items().
  - Set diff from flt((rm\_consumed\_dict.get(rm\_item\_code, 0) − required.qty), precision).
  - If diff &lt; 0.
    - Set msg from translated “Additional {0} {1} of item {2} required as per BOM to complete this transaction”.format(Platform.bold(abs(diff)), Platform.bold(required.stock\_uom), Platform.bold(rm\_item\_code)).
    - Call the validation error handler Platform.throw(msg, exc = BOMQuantityError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rm wise consumed qty](operations-007.md#op-74fe63ebf38677), [get rm wise required qty](operations-007.md#op-43dd9061671415).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”), Platform.db.get\_single\_value(“Buying Settings”, “validate\_consumed\_qty”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1570) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1060)
