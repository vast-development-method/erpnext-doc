# Shared transaction rules · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock controller

<a id="op-de27d6f6cbe084"></a>
### Stock Controller.get serial nos used in rows

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_serial_nos_used_in_rows`

**Inputs** self.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** picked\_serial\_nos.

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set picked\_serial\_nos from defaultdict(list).
- Set bundle\_items from mapping().
- For each row in (self.get(“items”) + self.get\_current\_packed\_rows()).
  - Set item\_code from (row.get(“rm\_item\_code”) or row.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“rm\_item\_code”) → row.item\_code.
  - If row.get(“serial\_no”).
    - Evaluate picked\_serial\_nos at item\_code.extend(get\_serial\_nos(row.serial\_no)).
  - Otherwise.
    - If row.get(“serial\_and\_batch\_bundle”).
      - Set bundle\_items at row.serial\_and\_batch\_bundle from item\_code.
- If bundle\_items.
  - For each entry in Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, list(bundle\_items)), “serial\_no” → tuple(“is”, “set”)), fields = list(“parent”, “serial\_no”)).
    - Evaluate picked\_serial\_nos at bundle\_items at entry.parent.append(entry.serial\_no).
- Return picked\_serial\_nos.

**Methods declared on this owner** [get current packed rows](operations-024.md#op-896913ccac8bcf).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L387)

<a id="op-4a933e693a0bd2"></a>
### Stock Controller.get batches used in rows

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_batches_used_in_rows`

**Inputs** self.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** picked\_batches.

**Local steps**

- Set tuple(entries, bundles) from tuple(list(), list()).
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- For each row in (self.get(“items”) + self.get\_current\_packed\_rows()).
  - If row.get(“serial\_and\_batch\_bundle”).
    - Evaluate bundles.append(row.serial\_and\_batch\_bundle).
  - Otherwise.
    - If row.get(“batch\_no”).
      - Set qty from row.qty when row.doctype equals “Packed Item”, otherwise row.stock\_qty.
        - Value choice on row.doctype equals “Packed Item” — true gives row.qty, false gives row.stock\_qty.
      - Evaluate entries.append(Platform.\_dict(batch\_no = row.batch\_no, warehouse = row.warehouse, qty = negative flt(qty, precision))).
- If bundles.
  - Update entries using + Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, bundles), “batch\_no” → tuple(“is”, “set”)), fields = list(“batch\_no”, “warehouse”, “qty”)).
- Set picked\_batches from Platform.\_dict().
- Evaluate add\_picked\_batches(picked\_batches, entries).
- Return picked\_batches.

**Methods declared on this owner** [get current packed rows](operations-024.md#op-896913ccac8bcf).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L377)

<a id="op-896913ccac8bcf"></a>
### Stock Controller.get current packed rows

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_current_packed_rows`

**Inputs** self.

**Explicit results** list of row for row drawn from (self.get(“packed\_items”) or list()) where tuple(row.parent\_detail\_docname, row.parent\_item) belongs to item\_rows.

**Local steps**

- Set item\_rows from set of tuple(row.name, row.item\_code) for row drawn from self.get(“items”).
  - Draw row from self.get(“items”).
- Return list of row for row drawn from (self.get(“packed\_items”) or list()) where tuple(row.parent\_detail\_docname, row.parent\_item) belongs to item\_rows.
  - Draw row from (self.get(“packed\_items”) or list()), keep a combination only if (tuple(row.parent\_detail\_docname, row.parent\_item) belongs to item\_rows).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“packed\_items”) → list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L378)

<a id="op-e957efecf3b3c4"></a>
### Stock Controller.create auto picked bundle

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_create_auto_picked_bundle`

**Inputs** self, bundle\_details, row, picked\_serial\_nos, picked\_batches.

**Explicit results** no value.

**Local steps**

- If (picked\_serial\_nos is identical to no value or row.serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in picked\_serial\_nos is identical to no value → row.serial\_no.
  - Evaluate self.create\_serial\_batch\_bundle(bundle\_details, row).
  - Return no value.
- Set item\_code from bundle\_details at “item\_code”.
- Set bundle\_details at “ignore\_serial\_nos” from list(picked\_serial\_nos at item\_code).
- Set bundle\_details at “already\_picked\_batches” from picked\_batches.
- Set sn\_doc from self.create\_serial\_batch\_bundle(bundle\_details, row).
- Set entries from (sn\_doc.get(“entries”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sn\_doc.get(“entries”) → list().
- Evaluate picked\_serial\_nos at item\_code.extend(generator of d.serial\_no for d drawn from entries where d.serial\_no).
  - Draw d from entries, keep a combination only if (d.serial\_no).
- If not row.batch\_no.
  - Evaluate add\_picked\_batches(picked\_batches, entries).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create serial batch bundle](operations-024.md#op-19c69b2a367f92).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L375)

<a id="op-2e58de777b7e65"></a>
### Stock Controller.auto picks outward serial batch

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_auto_picks_outward_serial_batch`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** false · bool(Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”)).

**Local steps**

- If (self.doctype does not belong to tuple(“Delivery Note”, “Sales Invoice”, “POS Invoice”) or self.get(“is\_return”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype does not belong to tuple(“Delivery Note”, “Sales Invoice”, “POS Invoice”) → self.get(“is\_return”).
  - Return false.
- Return bool(Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L371)

<a id="op-fe206441fa2192"></a>
### Stock Controller.get parent details for packed items

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_parent_details_for_packed_items`

**Inputs** self.

**Explicit results** parent\_details.

**Local steps**

- Set parent\_details from Platform.\_dict().
- For each row in self.get(“items”).
  - Set parent\_details at row.name from row.
- Return parent\_details.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L383)

<a id="op-d1d08974415315"></a>
### Stock Controller.make bundle for sales purchase return

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_make_bundle_for_sales_purchase_return`

**Inputs** self, table\_name = no value.

**Explicit results** no value.

**Local steps**

- If not self.get(“is\_return”).
  - Return no value.
- If not table\_name.
  - Set table\_name from “items”.
- Evaluate self.make\_bundle\_for\_non\_rejected\_qty(table\_name).
- If self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
  - Evaluate self.make\_bundle\_for\_rejected\_qty(table\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make bundle for non rejected qty](operations-024.md#op-6de646286e5ec5), [make bundle for rejected qty](operations-024.md#op-fd38ddcda92fb2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L966) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L643)

<a id="op-fd38ddcda92fb2"></a>
### Stock Controller.make bundle for rejected qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_make_bundle_for_rejected_qty`

**Inputs** self, table\_name = no value.

**State and service calls** call db\_set on row.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “For the {0}, no stock is available for the return in the warehouse {1}.”.format(Platform.bold(row.item\_code), row.get(warehouse\_field)).

**Local steps**

- Set tuple(field, reference\_ids) from self.get\_reference\_ids(table\_name, “rejected\_qty”, “rejected\_serial\_and\_batch\_bundle”).
- If not reference\_ids.
  - Return no value.
- Set child\_doctype from (self.doctype + “ Item”).
- Set available\_dict from available\_serial\_batch\_for\_return(field, child\_doctype, reference\_ids, is\_rejected = true).
- For each row in self.get(table\_name).
  - If not self.needs\_rejected\_bundle(row).
    - Continue with the next iteration or loop test.
  - If data bound to available\_dict.get(row.get(field)).
    - Set qty\_field from “rejected\_qty”.
    - Set warehouse\_field from “rejected\_warehouse”.
    - If row.get(“return\_qty\_from\_rejected\_warehouse”).
      - Set qty\_field from “stock\_qty”.
      - Set warehouse\_field from “warehouse”.
    - If not data.get(“qty”).
      - Call the validation error handler Platform.throw(translated “For the {0}, no stock is available for the return in the warehouse {1}.”.format(Platform.bold(row.item\_code), row.get(warehouse\_field))).
    - Set picked from filter\_serial\_batches(self, data, row, warehouse\_field = warehouse\_field, qty\_field = qty\_field).
    - Set bundle from make\_serial\_batch\_bundle\_for\_return(picked, row, self, warehouse\_field, …).
    - Evaluate remove\_picked\_serial\_batches(data, picked, self).
    - If row.get(“return\_qty\_from\_rejected\_warehouse”).
      - Evaluate row.db\_set(mapping(“serial\_and\_batch\_bundle” → bundle, “batch\_no” → empty text, “serial\_no” → empty text)).
    - Otherwise.
      - Evaluate row.db\_set(mapping(“rejected\_serial\_and\_batch\_bundle” → bundle, “batch\_no” → empty text, “rejected\_serial\_no” → empty text)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reference ids](operations-024.md#op-b4587e0fb29f4e), [needs rejected bundle](operations-024.md#op-3ef895b6fcb26e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L398)

<a id="op-6de646286e5ec5"></a>
### Stock Controller.make bundle for non rejected qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_make_bundle_for_non_rejected_qty`

**Inputs** self, table\_name.

**Record and data access** read “Serial and Batch Bundle” via get\_value.

**State and service calls** call db\_set on row.

**Explicit results** no value.

**Local steps**

- Set tuple(field, reference\_ids) from self.get\_reference\_ids(table\_name).
- If not reference\_ids.
  - Return no value.
- Set reference\_field from field.
- Set child\_doctype from (self.doctype + “ Item”).
- If table\_name equals “packed\_items”.
  - Set field from “parent\_detail\_docname”.
  - Set child\_doctype from “Packed Item”.
- Set available\_dict from available\_serial\_batch\_for\_return(field, child\_doctype, reference\_ids).
- For each row in self.get(table\_name).
  - If (row.get(“return\_qty\_from\_rejected\_warehouse”) or not row.get(“qty”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“return\_qty\_from\_rejected\_warehouse”) → not row.get(“qty”).
    - Continue with the next iteration or loop test.
  - Set value from row.get(field).
  - If (table\_name equals “packed\_items” and row.get(“parent\_detail\_docname”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_name equals “packed\_items” → row.get(“parent\_detail\_docname”).
    - Set value from self.get\_value\_for\_packed\_item(row, reference\_field).
    - If not value.
      - Continue with the next iteration or loop test.
  - If data bound to available\_dict.get(value).
    - Set picked from filter\_serial\_batches(self, data, row).
    - Set bundle from make\_serial\_batch\_bundle\_for\_return(picked, row, self).
    - Evaluate remove\_picked\_serial\_batches(data, picked, self).
    - Evaluate row.db\_set(mapping(“serial\_and\_batch\_bundle” → bundle, “batch\_no” → empty text, “serial\_no” → empty text)).
    - If self.doctype belongs to list(“Sales Invoice”, “Delivery Note”).
      - Evaluate row.db\_set(“incoming\_rate”, Platform.db.get\_value(“Serial and Batch Bundle”, bundle, “avg\_rate”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reference ids](operations-024.md#op-b4587e0fb29f4e), [get value for packed item](operations-024.md#op-6ae19714686acf).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1157) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L397)

<a id="op-3ef895b6fcb26e"></a>
### Stock Controller.needs rejected bundle

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_needs_rejected_bundle`

**Inputs** self, row.

**Declared result** bool.

**Explicit results** not row.get(“serial\_and\_batch\_bundle”) · bool((row.get(“rejected\_warehouse”) and self.get\_rejected\_stock\_qty(row) and not row.get(“rejected\_serial\_and\_batch\_bundle”))).

**Local steps**

- If row.get(“return\_qty\_from\_rejected\_warehouse”).
  - Return not row.get(“serial\_and\_batch\_bundle”).
- Return bool((row.get(“rejected\_warehouse”) and self.get\_rejected\_stock\_qty(row) and not row.get(“rejected\_serial\_and\_batch\_bundle”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“rejected\_warehouse”) → self.get\_rejected\_stock\_qty(row) → not row.get(“rejected\_serial\_and\_batch\_bundle”).

**Methods declared on this owner** [get rejected stock qty](operations-024.md#op-17db5cd27dc4ff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1159) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L399)

<a id="op-17db5cd27dc4ff"></a>
### Stock Controller.get rejected stock qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_rejected_stock_qty`

**Inputs** self, row.

**Declared result** float.

**Explicit results** flt((flt(row.get(“rejected\_qty”)) × flt(row.get(“conversion\_factor”, 1.0))), Platform.get\_precision(“Serial and Batch Entry”, “qty”)).

**Local steps**

- Return flt((flt(row.get(“rejected\_qty”)) × flt(row.get(“conversion\_factor”, 1.0))), Platform.get\_precision(“Serial and Batch Entry”, “qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L385)

<a id="op-6ae19714686acf"></a>
### Stock Controller.get value for packed item

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_value_for_packed_item`

**Inputs** self, row, reference\_field.

**Explicit results** tuple(row.item\_code, parent\_items at 0.get(reference\_field)) · no value.

**Local steps**

- Set parent\_items from self.get(“items”, mapping(“name” → row.parent\_detail\_docname)).
- If parent\_items.
  - Return tuple(row.item\_code, parent\_items at 0.get(reference\_field)).
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L390)

<a id="op-b4587e0fb29f4e"></a>
### Stock Controller.get reference ids

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_reference_ids`

**Inputs** self, table\_name, qty\_field = no value, bundle\_field = no value.

**Declared result** tuple at tuple(str, list at str).

**Explicit results** tuple(field, reference\_ids).

**Local steps**

- Set field from mapping(“Sales Invoice” → “sales\_invoice\_item”, “Delivery Note” → “dn\_detail”, “Purchase Receipt” → “purchase\_receipt\_item”, “Purchase Invoice” → “purchase\_invoice\_item”, …).get(self.doctype).
- If not bundle\_field.
  - Set bundle\_field from “serial\_and\_batch\_bundle”.
- If not qty\_field.
  - Set qty\_field from “qty”.
- Set reference\_ids from list().
- For each row in self.get(table\_name).
  - If not self.is\_serial\_batch\_item(row.item\_code).
    - Continue with the next iteration or loop test.
  - Set needs\_bundle from self.needs\_rejected\_bundle(row) when qty\_field equals “rejected\_qty”, otherwise (row.get(“qty”) and not row.get(“return\_qty\_from\_rejected\_warehouse”) and not row.get(bundle\_field)).
    - Value choice on qty\_field equals “rejected\_qty” — true gives self.needs\_rejected\_bundle(row), false gives (row.get(“qty”) and not row.get(“return\_qty\_from\_rejected\_warehouse”) and not row.get(bundle\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“qty”) → not row.get(“return\_qty\_from\_rejected\_warehouse”) → not row.get(bundle\_field).
  - If (row.get(field) and needs\_bundle and not row.get(“use\_serial\_batch\_fields”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(field) → needs\_bundle → not row.get(“use\_serial\_batch\_fields”).
    - Evaluate reference\_ids.append(row.get(field)).
  - If (table\_name equals “packed\_items” and row.get(“parent\_detail\_docname”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_name equals “packed\_items” → row.get(“parent\_detail\_docname”).
    - Set parent\_rows from (self.get(“items”, mapping(“name” → row.parent\_detail\_docname)) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“items”, mapping(“name” → row.parent\_detail\_docname)) → list().
    - For each d in parent\_rows.
      - If (d.get(field) and not d.get(bundle\_field) and not self.is\_legacy\_packed\_item(row, d.get(field))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(field) → not d.get(bundle\_field) → not self.is\_legacy\_packed\_item(row, d.get(field)).
        - Evaluate reference\_ids.append(d.get(field)).
- Return tuple(field, reference\_ids).

**Methods declared on this owner** [is serial batch item](operations-024.md#op-5219fa77dc344f), [needs rejected bundle](operations-024.md#op-3ef895b6fcb26e), [is legacy packed item](operations-024.md#op-9449c9ab488ac0).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L384)

<a id="op-9449c9ab488ac0"></a>
### Stock Controller.is legacy packed item

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_is_legacy_packed_item`

**Inputs** self, row, source\_parent\_detail\_docname.

**Record and data access** read “Packed Item” via exists.

**Explicit results** false · not Platform.db.exists(“Packed Item”, mapping(“parent\_detail\_docname” → source\_parent\_detail\_docname, “item\_code” → row.item\_code, “serial\_and\_batch\_bundle” → tuple(“is”, “set”))).

**Local steps**

- If not (row.serial\_no or row.batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
  - Return false.
- Return not Platform.db.exists(“Packed Item”, mapping(“parent\_detail\_docname” → source\_parent\_detail\_docname, “item\_code” → row.item\_code, “serial\_and\_batch\_bundle” → tuple(“is”, “set”))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L394)

<a id="op-5219fa77dc344f"></a>
### Stock Controller.is serial batch item

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_is_serial_batch_item`

**Inputs** self, item\_code.

**Wrappers, in declaration order** Platform.request\_cache.

**Declared result** bool.

**Record and data access** read “Item” via exists · read “Item” via get\_value.

**Explicit results** true · false.

**Explicit failure paths** validation helper — translated “Item {0} does not exist.”.format(bold(item\_code)).

**Local steps**

- If not Platform.db.exists(“Item”, item\_code).
  - Call the validation error handler Platform.throw(translated “Item {0} does not exist.”.format(bold(item\_code))).
- Set item\_details from Platform.db.get\_value(“Item”, item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
- If (item\_details.has\_serial\_no or item\_details.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details.has\_serial\_no → item\_details.has\_batch\_no.
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L395)

<a id="op-9a4bfbf8cb752b"></a>
### Stock Controller.update bundle details

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_update_bundle_details`

**Inputs** self, bundle\_details, table\_name, row, is\_rejected = false, parent\_details = no value.

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set qty from row.get(“qty”).
- Set warehouse from row.get(“warehouse”).
- If table\_name equals “packed\_items”.
  - Set type\_of\_transaction from “Inward”.
  - If not self.is\_return.
    - Set type\_of\_transaction from “Outward”.
- Otherwise.
  - If table\_name equals “supplied\_items”.
    - Set qty from row.consumed\_qty.
    - Set warehouse from self.supplier\_warehouse.
    - Set type\_of\_transaction from “Outward”.
    - If self.is\_return.
      - Set type\_of\_transaction from “Inward”.
  - Otherwise.
    - Set type\_of\_transaction from get\_type\_of\_transaction(self, row).
- If hasattr(row, “stock\_qty”).
  - Set qty from row.stock\_qty.
- If self.doctype equals “Stock Entry”.
  - Set qty from row.transfer\_qty.
  - Set warehouse from (row.s\_warehouse or row.t\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.s\_warehouse → row.t\_warehouse.
- Set serial\_nos from row.serial\_no.
- If is\_rejected.
  - Set serial\_nos from row.get(“rejected\_serial\_no”).
  - Set type\_of\_transaction from “Inward” when not self.is\_return, otherwise “Outward”.
    - Value choice on not self.is\_return — true gives “Inward”, false gives “Outward”.
  - Set qty from self.get\_rejected\_stock\_qty(row).
  - Set warehouse from row.get(“rejected\_warehouse”).
- If (self.is\_internal\_transfer() and self.doctype belongs to list(“Sales Invoice”, “Delivery Note”) and self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → self.doctype belongs to list(“Sales Invoice”, “Delivery Note”) → self.is\_return.
  - Set warehouse from (row.get(“target\_warehouse”) or row.get(“warehouse”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“target\_warehouse”) → row.get(“warehouse”).
  - Set type\_of\_transaction from “Outward”.
- If table\_name equals “packed\_items”.
  - If not warehouse.
    - Set warehouse from parent\_details at row.parent\_detail\_docname.warehouse.
  - Set bundle\_details at “voucher\_detail\_no” from parent\_details at row.parent\_detail\_docname.name.
- Evaluate bundle\_details.update(mapping(“qty” → qty, “is\_rejected” → is\_rejected, “type\_of\_transaction” → type\_of\_transaction, “warehouse” → warehouse, …)).
  - Value choice on row.batch\_no — true gives Platform.\_dict(mapping(row.batch\_no → qty)), false gives no value.
  - Value choice on serial\_nos — true gives get\_serial\_nos(serial\_nos), false gives no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get rejected stock qty](operations-024.md#op-17db5cd27dc4ff).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1163) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L403)

<a id="op-19c69b2a367f92"></a>
### Stock Controller.create serial batch bundle

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_create_serial_batch_bundle`

**Inputs** self, bundle\_details, row.

**State and service calls** call db\_set on row.

**Explicit results** sn\_doc.

**Local steps**

- Bind dependencies SerialBatchCreation.
- Set sn\_doc from SerialBatchCreation(bundle\_details).make\_serial\_and\_batch\_bundle().
- Set field from “serial\_and\_batch\_bundle”.
- If bundle\_details.get(“is\_rejected”).
  - Set field from “rejected\_serial\_and\_batch\_bundle”.
- Evaluate row.set(field, sn\_doc.name).
- Evaluate row.db\_set(mapping(field → sn\_doc.name)).
- Return sn\_doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L376)

<a id="op-87162f775da4dd"></a>
### Stock Controller.validate serial nos and batches with bundle

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_serial_nos_and_batches_with_bundle`

**Inputs** self, row.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit failure paths** validation helper — translated “At row {0}: Serial and Batch Bundle {1} has already created. Please remove the values from the serial no or  …”.format(row.idx, row.serial\_and\_batch\_bundle).

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set throw\_error from false.
- If row.serial\_no.
  - Set serial\_nos from Platform.get\_all(“Serial and Batch Entry”, fields = list(“serial\_no”), filters = mapping(“parent” → row.serial\_and\_batch\_bundle)).
  - Set serial\_nos from sorted(list of cstr(d.serial\_no) for d drawn from serial\_nos).
    - Draw d from serial\_nos.
  - Set parsed\_serial\_nos from get\_serial\_nos(row.serial\_no).
  - If len(serial\_nos) differs from len(parsed\_serial\_nos).
    - Set throw\_error from true.
  - Otherwise.
    - If serial\_nos differs from parsed\_serial\_nos.
      - For each serial\_no in serial\_nos.
        - If serial\_no does not belong to parsed\_serial\_nos.
          - Set throw\_error from true.
          - Leave the innermost loop without its normal-exhaustion alternative.
- Otherwise.
  - If row.batch\_no.
    - Set batches from sorted(Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → row.serial\_and\_batch\_bundle), pluck = “batch\_no”, distinct = true)).
    - If batches differs from list(row.batch\_no).
      - Set throw\_error from true.
- If throw\_error.
  - Call the validation error handler Platform.throw(translated “At row {0}: Serial and Batch Bundle {1} has already created. Please remove the values from the serial no or  …”.format(row.idx, row.serial\_and\_batch\_bundle)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L423)

<a id="op-02c29f31beabd5"></a>
### Stock Controller.set use serial batch fields

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_set_use_serial_batch_fields`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).
  - For each row in self.items.
    - Set row.use\_serial\_batch\_fields from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “use\_serial\_batch\_fields”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L654)

<a id="op-cd83339415d33f"></a>
### Stock Controller.get gl entries

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map = no value, default\_expense\_account = no value, default\_cost\_center = no value.

**Record and data access** read “Company” via get\_cached\_value · read “Warehouse” via get\_cached\_value.

**Explicit results** process\_gl\_map(gl\_list, precision = precision, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Explicit failure paths** validation helper — translated “Please set default cost of goods sold account in company {0} for booking rounding gain and loss during stock …”.format(Platform.bold(self.company)) · validation helper — translated “Warehouse {0} is not linked to any account, please mention the account in the warehouse record or set defaul …”.format(wh, self.company).

**Local steps**

- If not inventory\_account\_map.
  - Set inventory\_account\_map from self.get\_inventory\_account\_map().
- Set sle\_map from self.get\_stock\_ledger\_details().
- Set voucher\_details from self.get\_voucher\_details(default\_expense\_account, default\_cost\_center, sle\_map).
- Set gl\_list from list().
- Set warehouse\_with\_no\_account from list().
- Set precision from self.get\_debit\_field\_precision().
- For each item\_row in voucher\_details.
  - Set sle\_list from sle\_map.get(item\_row.name).
  - Set sle\_rounding\_diff from 0.0.
  - If sle\_list.
    - For each sle in sle\_list.
      - Set \_inv\_dict from self.get\_inventory\_account\_dict(sle, inventory\_account\_map).
      - If \_inv\_dict.get(“account”).
        - Update sle\_rounding\_diff using + flt(sle.stock\_value\_difference).
        - Evaluate self.check\_expense\_account(item\_row).
        - If item\_row.get(“target\_warehouse”).
          - Set \_target\_wh\_inv\_dict from self.get\_inventory\_account\_dict(item\_row, inventory\_account\_map, warehouse\_field = “target\_warehouse”).
          - Set expense\_account from \_target\_wh\_inv\_dict at “account”.
        - Otherwise.
          - Set expense\_account from item\_row.expense\_account.
        - Evaluate gl\_list.append(self.get\_gl\_dict(mapping(“account” → \_inv\_dict at “account”, “against” → expense\_account, “cost\_center” → item\_row.cost\_center, “project” → (sle.get(“project”) or item\_row.project or self.ge ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.get(“project”) → item\_row.project → self.get(“project”).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“is\_opening”) → self.get(“is\_opening”) → “No”.
        - Evaluate gl\_list.append(self.get\_gl\_dict(mapping(“account” → expense\_account, “against” → \_inv\_dict at “account”, “cost\_center” → item\_row.cost\_center, “remarks” → (self.get(“remarks”) or translated “Accounting Ent ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.get(“project”) → item\_row.get(“project”) → self.get(“project”).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“is\_opening”) → self.get(“is\_opening”) → “No”.
      - Otherwise.
        - If sle.warehouse does not belong to warehouse\_with\_no\_account.
          - Evaluate warehouse\_with\_no\_account.append(sle.warehouse).
  - If (abs(sle\_rounding\_diff) &gt; (1.0 ÷ (10 to the power precision)) and self.is\_internal\_transfer()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in abs(sle\_rounding\_diff) &gt; (1.0 ÷ (10 to the power precision)) → self.is\_internal\_transfer().
    - Set warehouse\_asset\_account from empty text.
    - If self.get(“is\_internal\_customer”).
      - Set \_inv\_dict from self.get\_inventory\_account\_dict(item\_row, inventory\_account\_map, warehouse\_field = “target\_warehouse”).
      - Set warehouse\_asset\_account from \_inv\_dict.get(“account”) when \_inv\_dict, otherwise no value.
        - Value choice on \_inv\_dict — true gives \_inv\_dict.get(“account”), false gives no value.
    - Otherwise.
      - If self.get(“is\_internal\_supplier”).
        - Set \_inv\_dict from self.get\_inventory\_account\_dict(item\_row, inventory\_account\_map).
        - Set warehouse\_asset\_account from \_inv\_dict.get(“account”) when \_inv\_dict, otherwise no value.
          - Value choice on \_inv\_dict — true gives \_inv\_dict.get(“account”), false gives no value.
    - Set expense\_account from Platform.get\_cached\_value(“Company”, self.company, “default\_expense\_account”).
    - If not expense\_account.
      - Call the validation error handler Platform.throw(translated “Please set default cost of goods sold account in company {0} for booking rounding gain and loss during stock …”.format(Platform.bold(self.company))).
    - Evaluate gl\_list.append(self.get\_gl\_dict(mapping(“account” → expense\_account, “against” → warehouse\_asset\_account, “cost\_center” → item\_row.cost\_center, “project” → (item\_row.project or self.get(“project”)), …), \_i ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.project → self.get(“project”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“is\_opening”) → self.get(“is\_opening”) → “No”.
    - Evaluate gl\_list.append(self.get\_gl\_dict(mapping(“account” → warehouse\_asset\_account, “against” → expense\_account, “cost\_center” → item\_row.cost\_center, “remarks” → translated “Rounding gain/loss Entry for Stock Tr ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“project”) → self.get(“project”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“is\_opening”) → self.get(“is\_opening”) → “No”.
- If warehouse\_with\_no\_account.
  - For each wh in warehouse\_with\_no\_account.
    - If Platform.get\_cached\_value(“Warehouse”, wh, “company”).
      - Call the validation error handler Platform.throw(translated “Warehouse {0} is not linked to any account, please mention the account in the warehouse record or set defaul …”.format(wh, self.company)).
- If self.book\_expenses\_added\_to\_stock.
  - Evaluate self.append\_expenses\_added\_to\_stock\_entries(gl\_list, voucher\_details, sle\_map).
- Return process\_gl\_map(gl\_list, precision = precision, from\_repost = Platform.flags.through\_repost\_item\_valuation).

**Methods declared on this owner** [get inventory account map](operations-023.md#op-bbc9dc6a238ee8), [get stock ledger details](operations-025.md#op-e84139200ec5e1), [get voucher details](operations-025.md#op-9edffb657c724c), [get debit field precision](operations-024.md#op-6f205f04045db1), [get inventory account dict](operations-023.md#op-28a7e9087c9063), [check expense account](operations-025.md#op-b88e34fa13f933), [append expenses added to stock entries](operations-024.md#op-196182204f8c0e).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_expense\_account”), Platform.get\_cached\_value(“Warehouse”, wh, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L635)

<a id="op-147b22db18b30b"></a>
### Stock Controller.book stock expense enabled

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_book_stock_expense_enabled`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** self.\_book\_stock\_expense\_enabled.

**Local steps**

- If not hasattr(self, “\_book\_stock\_expense\_enabled”).
  - Set self.\_book\_stock\_expense\_enabled from cint(Platform.db.get\_single\_value(“Accounts Settings”, “book\_stock\_expense\_gl\_entries”)).
- Return self.\_book\_stock\_expense\_enabled.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “book\_stock\_expense\_gl\_entries”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L372)

<a id="op-196182204f8c0e"></a>
### Stock Controller.append expenses added to stock entries

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_append_expenses_added_to_stock_entries`

**Inputs** self, gl\_list, voucher\_details, sle\_map.

**Explicit results** no value.

**Local steps**

- If not self.book\_stock\_expense\_enabled().
  - Return no value.
- Set precision from self.get\_debit\_field\_precision().
- For each item\_row in voucher\_details.
  - Set sle\_list from sle\_map.get(item\_row.name).
  - If not sle\_list.
    - Continue with the next iteration or loop test.
  - Set amount from flt(sum(generator of flt(sle.stock\_value\_difference) for sle drawn from sle\_list), precision).
    - Draw sle from sle\_list.
  - If not amount.
    - Continue with the next iteration or loop test.
  - Set item\_code from (item\_row.get(“item\_code”) or sle\_list at 0.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“item\_code”) → sle\_list at 0.item\_code.
  - Evaluate self.append\_expenses\_added\_to\_stock\_pair(gl\_list, item\_code, amount, item\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [book stock expense enabled](operations-024.md#op-147b22db18b30b), [get debit field precision](operations-024.md#op-6f205f04045db1), [append expenses added to stock pair](operations-024.md#op-7b5c624ea146da).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L369)

<a id="op-7b5c624ea146da"></a>
### Stock Controller.append expenses added to stock pair

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_append_expenses_added_to_stock_pair`

**Inputs** self, gl\_list, item\_code, amount, item\_row.

**Record and data access** read “Item” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please set {0} in Company {1} or in the Item Defaults of Item {2}”.format(Platform.bold(translated Platform.unscrub(field)), self.company, item\_code).

**Local steps**

- If (not amount or not Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not amount → not Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”).
  - Return no value.
- Set fields from tuple(“expenses\_added\_to\_stock\_account”, “expenses\_added\_to\_stock\_contra\_account”).
- Set details from get\_expenses\_added\_to\_stock\_accounts(item\_code, self.company).
- For each field in fields.
  - If not details.get(field).
    - Call the validation error handler Platform.throw(translated “Please set {0} in Company {1} or in the Item Defaults of Item {2}”.format(Platform.bold(translated Platform.unscrub(field)), self.company, item\_code)).
- Set cost\_center from (item\_row.get(“cost\_center”) or Platform.get\_cached\_value(“Company”, self.company, “cost\_center”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“cost\_center”) → Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).
- Set remarks from translated “Expenses Added To Stock for Item {0}”.format(item\_code).
- Set common\_args from mapping(“cost\_center” → cost\_center, “project” → (item\_row.get(“project”) or self.get(“project”)), “remarks” → remarks).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row.get(“project”) → self.get(“project”).
- Evaluate gl\_list.append(self.get\_gl\_dict(mapping(“account” → details.expenses\_added\_to\_stock\_account, “against” → details.expenses\_added\_to\_stock\_contra\_account, “debit” → amount, expand common\_args), item = item\_row)).
- Evaluate gl\_list.append(self.get\_gl\_dict(mapping(“account” → details.expenses\_added\_to\_stock\_contra\_account, “against” → details.expenses\_added\_to\_stock\_account, “debit” → (negative 1 × amount), expand common\_args) ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “is\_stock\_item”), Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L370)

<a id="op-6f205f04045db1"></a>
### Stock Controller.get debit field precision

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_get_debit_field_precision`

**Inputs** self.

**Explicit results** Platform.flags.debit\_field\_precision.

**Local steps**

- If not Platform.flags.debit\_field\_precision.
  - Set Platform.flags.debit\_field\_precision from Platform.get\_precision(“GL Entry”, “debit\_in\_account\_currency”).
- Return Platform.flags.debit\_field\_precision.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L379)
