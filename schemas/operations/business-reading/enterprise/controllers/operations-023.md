# Shared transaction rules · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Status updater

<a id="op-3291f6e79ff4e2"></a>
### Status Updater.update modified

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_modified`

**Inputs** self, args, update\_modified.

**Explicit results** no value.

**Local steps**

- If not update\_modified.
  - Set args at “update\_modified” from empty text.
  - Return no value.
- Set args at “update\_modified” from “, modified = {}, modified\_by = {}”.format(Platform.db.escape(now()), Platform.db.escape(Platform.session.user)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0391.json#L4168) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L607)

<a id="op-10dac6f18c550a"></a>
### Status Updater.update billing status for zero amount refdoc

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_billing_status_for_zero_amount_refdoc`

**Inputs** self, ref\_dt.

**Explicit results** no value.

**Local steps**

- Set ref\_fieldname from Platform.scrub(ref\_dt).
- Set ref\_docs from list of item.get(ref\_fieldname) for item drawn from (self.get(“items”) or list()) where item.get(ref\_fieldname).
  - Draw item from (self.get(“items”) or list()), keep a combination only if (item.get(ref\_fieldname)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“items”) → list().
- If not ref\_docs.
  - Return no value.
- Set zero\_amount\_refdocs from Platform.db.sql\_list(formatted text   SELECT  name  from  ′tab{ref\_dt}′  where  docstatus = 1  and base\_net\_total = 0  and name in %(ref\_docs)s  , mapping(“ref\_docs” → ref\_docs)).
- If zero\_amount\_refdocs.
  - Evaluate self.update\_billing\_status(zero\_amount\_refdocs, ref\_dt, ref\_fieldname).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update billing status](operations-023.md#op-198ecad682ca28).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L605)

<a id="op-198ecad682ca28"></a>
### Status Updater.update billing status

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_billing_status`

**Inputs** self, zero\_amount\_refdoc, ref\_dt, ref\_fieldname.

**Record and data access** execute query text (SELECT).format(ref\_dt, “%s”) · execute query text (SELECT).format(self.doctype, ref\_fieldname, “%s”).

**State and service calls** call db\_set on ref\_doc.

**Local steps**

- For each ref\_dn in zero\_amount\_refdoc.
  - Set ref\_doc\_qty from flt(Platform.db.sql(query text (SELECT).format(ref\_dt, “%s”), ref\_dn) at 0 at 0).
  - Set billed\_qty from flt(Platform.db.sql(query text (SELECT).format(self.doctype, ref\_fieldname, “%s”), ref\_dn) at 0 at 0).
  - Set per\_billed from self.snap\_full\_percentage((safe\_div(min(ref\_doc\_qty, billed\_qty), ref\_doc\_qty) × 100)).
  - Set ref\_doc from Platform.get\_lazy\_doc(ref\_dt, ref\_dn).
  - Evaluate ref\_doc.db\_set(“per\_billed”, per\_billed).
  - If hasattr(ref\_doc, “billing\_status”).
    - If ref\_doc.per\_billed &lt; 0.001.
      - Evaluate ref\_doc.db\_set(“billing\_status”, “Not Billed”).
    - Otherwise.
      - If ref\_doc.per\_billed ≥ COMPLETE\_PERCENTAGE.
        - Evaluate ref\_doc.db\_set(“billing\_status”, “Fully Billed”).
      - Otherwise.
        - Evaluate ref\_doc.db\_set(“billing\_status”, “Partly Billed”).
  - Evaluate ref\_doc.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [snap full percentage](operations-022.md#op-6220aca43095ad).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L604)

<a id="op-98b425b5b2c990"></a>
### Get allowance for

`operation_enterprise_controllers_status_updater_business_behavior_get_allowance_for`

**Inputs** item\_code, item\_allowance = no value, global\_qty\_allowance = no value, global\_amount\_allowance = no value, qty\_or\_amount = “qty”, global\_qty\_allowance\_field = “over\_delivery\_receipt\_allowance”, global\_qty\_allowance\_doctype = “Stock Settings”, item\_qty\_allowance\_field = “over\_delivery\_receipt\_allowance”.

**Record and data access** read “Item” via get\_cached\_value · read global\_qty\_allowance\_doctype via get\_single\_value · read “Accounts Settings” via get\_cached\_value.

**Explicit results** tuple(item\_allowance at item\_code.qty, item\_allowance, global\_qty\_allowance, global\_amount\_allowance) · tuple(item\_allowance at item\_code.amount, item\_allowance, global\_qty\_allowance, global\_amount\_allowance) · tuple(allowance, item\_allowance, global\_qty\_allowance, global\_amount\_allowance).

**Local steps**

- If item\_allowance is identical to no value.
  - Set item\_allowance from mapping().
- If qty\_or\_amount equals “qty”.
  - If item\_allowance.get(item\_code, Platform.\_dict()).get(“qty”).
    - Return tuple(item\_allowance at item\_code.qty, item\_allowance, global\_qty\_allowance, global\_amount\_allowance).
- Otherwise.
  - If item\_allowance.get(item\_code, Platform.\_dict()).get(“amount”).
    - Return tuple(item\_allowance at item\_code.amount, item\_allowance, global\_qty\_allowance, global\_amount\_allowance).
- Set tuple(qty\_allowance, over\_billing\_allowance) from Platform.get\_cached\_value(“Item”, item\_code, list(item\_qty\_allowance\_field, “over\_billing\_allowance”)).
- If (qty\_or\_amount equals “qty” and not qty\_allowance).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_or\_amount equals “qty” → not qty\_allowance.
  - If global\_qty\_allowance is identical to no value.
    - Set global\_qty\_allowance from flt(Platform.get\_single\_value(global\_qty\_allowance\_doctype, global\_qty\_allowance\_field)).
  - Set qty\_allowance from global\_qty\_allowance.
- Otherwise.
  - If (qty\_or\_amount equals “amount” and not over\_billing\_allowance).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_or\_amount equals “amount” → not over\_billing\_allowance.
    - If global\_amount\_allowance is identical to no value.
      - Set global\_amount\_allowance from flt(Platform.get\_cached\_value(“Accounts Settings”, no value, “over\_billing\_allowance”)).
    - Set over\_billing\_allowance from global\_amount\_allowance.
- If qty\_or\_amount equals “qty”.
  - Set allowance from qty\_allowance.
  - Evaluate item\_allowance.setdefault(item\_code, Platform.\_dict()).setdefault(“qty”, qty\_allowance).
- Otherwise.
  - Set allowance from over\_billing\_allowance.
  - Evaluate item\_allowance.setdefault(item\_code, Platform.\_dict()).setdefault(“amount”, over\_billing\_allowance).
- Return tuple(allowance, item\_allowance, global\_qty\_allowance, global\_amount\_allowance).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(item\_qty\_allowance\_field, “over\_billing\_allowance”)), Platform.get\_single\_value(global\_qty\_allowance\_doctype, global\_qty\_allowance\_field) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0391.json#L5496) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L914) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L595)

## Service · Stock controller

<a id="op-55f37c54de84b6"></a>
### Is inspection exempt secondary row

`operation_enterprise_binding_enterprise_controllers_stock_controller_is_inspection_exempt_secondary_row`

**Inputs** doc, row.

**Declared result** bool.

**Explicit results** false · doc.purpose belongs to SECONDARY\_ITEM\_PURPOSES · true.

**Local steps**

- If not (row.get(“secondary\_item\_type”) or row.get(“valuation\_type”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“secondary\_item\_type”) → row.get(“valuation\_type”).
  - Return false.
- If doc.doctype equals “Stock Entry”.
  - Return doc.purpose belongs to SECONDARY\_ITEM\_PURPOSES.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L363)

<a id="op-bbc5463b1902d5"></a>
### Stock entry row requires inspection

`operation_enterprise_binding_enterprise_controllers_stock_controller_stock_entry_row_requires_inspection`

**Inputs** purpose, row.

**Explicit results** false · bool(row.is\_finished\_item) · bool(row.t\_warehouse) · bool((row.s\_warehouse and row.s\_warehouse differs from row.t\_warehouse)).

**Local steps**

- If (purpose belongs to SECONDARY\_ITEM\_PURPOSES and (row.get(“secondary\_item\_type”) or row.get(“valuation\_type”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in purpose belongs to SECONDARY\_ITEM\_PURPOSES → (row.get(“secondary\_item\_type”) or row.get(“valuation\_type”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“secondary\_item\_type”) → row.get(“valuation\_type”).
  - Return false.
- If purpose equals “Manufacture”.
  - Return bool(row.is\_finished\_item).
- If purpose belongs to QI\_INCOMING\_PURPOSES.
  - Return bool(row.t\_warehouse).
- If purpose belongs to QI\_OUTGOING\_PURPOSES.
  - Return bool((row.s\_warehouse and row.s\_warehouse differs from row.t\_warehouse)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.s\_warehouse → row.s\_warehouse differs from row.t\_warehouse.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L367)

<a id="op-a9ee57e761705f"></a>
### Stock Controller.validate

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- If self.docstatus equals 0.
  - For each table\_name in list(“items”, “packed\_items”, “supplied\_items”).
    - Evaluate self.validate\_duplicate\_serial\_and\_batch\_bundle(table\_name).
- If not self.get(“is\_return”).
  - Evaluate self.validate\_inspection().
- Evaluate self.validate\_warehouse\_of\_sabb().
- Evaluate self.validate\_serialized\_batch().
- Evaluate self.clean\_serial\_nos().
- Evaluate self.validate\_customer\_provided\_item().
- Evaluate self.reset\_conversion\_factor().
- Evaluate self.set\_rate\_of\_stock\_uom().
- Evaluate self.validate\_internal\_transfer().
- Evaluate self.validate\_putaway\_capacity().
- Evaluate self.validate\_inventory\_dimension\_mandatory().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate serial and batch bundle](operations-023.md#op-5c2edd0de9ad26), [validate inspection](operations-025.md#op-bdd2cd46e592d3), [validate warehouse of sabb](operations-023.md#op-15935fad9a56f4), [validate serialized batch](operations-023.md#op-9643f74ec85910), [clean serial nos](operations-023.md#op-232168d6781351), [validate customer provided item](operations-026.md#op-cda5158b267171), [reset conversion factor](operations-023.md#op-9d64ab416ef2cd), [set rate of stock uom](operations-026.md#op-56e788a0c17f36), [validate internal transfer](operations-026.md#op-e060badbb7138e), [validate putaway capacity](operations-026.md#op-a3e3163b2adde2), [validate inventory dimension mandatory](operations-025.md#op-94ce2f196969bb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L984) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L661)

<a id="op-9e6d58613753d7"></a>
### Stock Controller.on update

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_on_update`

**Inputs** self.

**Local steps**

- Evaluate super().on\_update().
- Evaluate self.check\_zero\_rate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check zero rate](operations-023.md#op-4d543996696382).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0391.json#L6809) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L649)

<a id="op-15935fad9a56f4"></a>
### Stock Controller.validate warehouse of sabb

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_warehouse_of_sabb`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_value · resolve a document from “Serial and Batch Bundle” via get\_doc.

**Explicit failure paths** validation helper — translated “Row #{0}: Company {1} does not match with the company {2} in Serial and Batch Bundle {3}.”.format(row.idx, self.company, sabb\_details.company, bundle) · validation helper — translated “Row #{0}: Warehouse {1} does not match with the warehouse {2} in Serial and Batch Bundle {3}.”.format(row.idx, warehouse, sabb\_details.warehouse, row.serial\_and\_batch\_bundle).

**Local steps**

- Set is\_internal\_transfer from self.is\_internal\_transfer().
- Set doc\_before\_save from self.get\_doc\_before\_save().
- Set bundle\_details from mapping().
- For each row in self.items.
  - For each fieldname in tuple(“serial\_and\_batch\_bundle”, “rejected\_serial\_and\_batch\_bundle”).
    - Set bundle from row.get(fieldname).
    - If not bundle.
      - Continue with the next iteration or loop test.
    - If bundle does not belong to bundle\_details.
      - Set bundle\_details at bundle from Platform.db.get\_value(“Serial and Batch Bundle”, bundle, list(“company”, “type\_of\_transaction”, “warehouse”, “has\_serial\_no”), as\_dict = true).
    - Set sabb\_details from bundle\_details at bundle.
    - If (sabb\_details and sabb\_details.company differs from self.company).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in sabb\_details → sabb\_details.company differs from self.company.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Company {1} does not match with the company {2} in Serial and Batch Bundle {3}.”.format(row.idx, self.company, sabb\_details.company, bundle)).
  - Set sabb\_details from bundle\_details.get(row.get(“serial\_and\_batch\_bundle”)).
  - If not sabb\_details.
    - Continue with the next iteration or loop test.
  - If (is\_internal\_transfer or sabb\_details.type\_of\_transaction differs from “Outward”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_internal\_transfer → sabb\_details.type\_of\_transaction differs from “Outward”.
    - Continue with the next iteration or loop test.
  - Set warehouse from (row.get(“warehouse”) or row.get(“s\_warehouse”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“warehouse”) → row.get(“s\_warehouse”).
  - If sabb\_details.warehouse differs from warehouse.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Warehouse {1} does not match with the warehouse {2} in Serial and Batch Bundle {3}.”.format(row.idx, warehouse, sabb\_details.warehouse, row.serial\_and\_batch\_bundle)).
  - If self.doctype equals “Stock Reconciliation”.
    - Continue with the next iteration or loop test.
  - If (sabb\_details.has\_serial\_no and doc\_before\_save and doc\_before\_save.get(“items”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sabb\_details.has\_serial\_no → doc\_before\_save → doc\_before\_save.get(“items”).
    - Set prev\_row from doc\_before\_save.get(“items”, mapping(“idx” → row.idx)).
    - If (prev\_row and prev\_row at 0.serial\_and\_batch\_bundle differs from row.serial\_and\_batch\_bundle).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in prev\_row → prev\_row at 0.serial\_and\_batch\_bundle differs from row.serial\_and\_batch\_bundle.
      - Set sabb\_doc from Platform.get\_doc(“Serial and Batch Bundle”, row.serial\_and\_batch\_bundle).
      - Evaluate sabb\_doc.validate\_serial\_no\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L425)

<a id="op-9d64ab416ef2cd"></a>
### Stock Controller.reset conversion factor

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_reset_conversion_factor`

**Inputs** self.

**State and service calls** msgprint with translated “Conversion factor for item {0} has been reset to 1.0 as the uom {1} is same as stock uom {2}.”.format(bold(row.item\_code), bold(row.uom), bold(row.stock\_uom)).

**Local steps**

- For each row in self.get(“items”).
  - If row.uom differs from row.stock\_uom.
    - Continue with the next iteration or loop test.
  - If row.conversion\_factor differs from 1.0.
    - Set row.conversion\_factor from 1.0.
    - Evaluate Platform.msgprint(translated “Conversion factor for item {0} has been reset to 1.0 as the uom {1} is same as stock uom {2}.”.format(bold(row.item\_code), bold(row.uom), bold(row.stock\_uom)), alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0391.json#L6886) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L974) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L651)

<a id="op-4d543996696382"></a>
### Stock Controller.check zero rate

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_check_zero_rate`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**State and service calls** toast with translated “Row #{0}: Item {1} has zero rate but '{2}' is not enabled.”.format(item.idx, Platform.bold(item.item\_code), item.meta.get\_label(“allow\_zero\_valuation\_rate”)).

**Local steps**

- If self.doctype belongs to list(“POS Invoice”, “Purchase Invoice”, “Sales Invoice”, “Delivery Note”, …).
  - For each item in self.get(“items”).
    - If ((item.get(“valuation\_rate”) equals 0 or (item.get(“incoming\_rate”) equals 0 and self.get(“update\_stock”, 1))) and item.get(“allow\_zero\_valuation\_rate”) equals 0 and Platform.get\_cached\_value(“Item”, item. ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (item.get(“valuation\_rate”) equals 0 or (item.get(“incoming\_rate”) equals 0 and self.get(“update\_stock”, 1))) → item.get(“allow\_zero\_valuation\_rate”) equals 0 → Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“valuation\_rate”) equals 0 → (item.get(“incoming\_rate”) equals 0 and self.get(“update\_stock”, 1)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“incoming\_rate”) equals 0 → self.get(“update\_stock”, 1).
      - Evaluate Platform.toast(translated “Row #{0}: Item {1} has zero rate but '{2}' is not enabled.”.format(item.idx, Platform.bold(item.item\_code), item.meta.get\_label(“allow\_zero\_valuation\_rate”)), indicator = “orange”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L633)

<a id="op-2752a1ef52fe37"></a>
### Stock Controller.validate items exist

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_validate_items_exist`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Items {0} do not exist in the Item master.”.format(“, ”.join(non\_exists\_items)).

**Local steps**

- If not self.get(“items”).
  - Return no value.
- Set items from list of d.item\_code for d drawn from self.get(“items”).
  - Draw d from self.get(“items”).
- Set exists\_items from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, items)), pluck = “name”).
- Set non\_exists\_items from (set(items) − set(exists\_items)).
- If non\_exists\_items.
  - Call the validation error handler Platform.throw(translated “Items {0} do not exist in the Item master.”.format(“, ”.join(non\_exists\_items))).

If control reaches the end, it returns no value.

**Derived worked case from the contract** Rows A, B, B against master A fail with one missing code, B.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0441.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L987) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L664) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-5c2edd0de9ad26"></a>
### Stock Controller.validate duplicate serial and batch bundle

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_duplicate_serial_and_batch_bundle`

**Inputs** self, table\_name.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Serial and Batch Bundle {0} is already used in {1} {2}.”.format(Platform.bold(data.serial\_and\_batch\_bundle), data.voucher\_type, data.voucher\_no).

**Local steps**

- If not self.get(table\_name).
  - Return no value.
- Set sbb\_list from list().
- For each item in self.get(table\_name).
  - If item.get(“serial\_and\_batch\_bundle”).
    - Evaluate sbb\_list.append(item.get(“serial\_and\_batch\_bundle”)).
  - If item.get(“rejected\_serial\_and\_batch\_bundle”).
    - Evaluate sbb\_list.append(item.get(“rejected\_serial\_and\_batch\_bundle”)).
- If sbb\_list.
  - Set SLE from Platform.qb.DocType(“Stock Ledger Entry”).
  - Set data from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
  - If data.
    - Set data from data at 0.
    - Call the validation error handler Platform.throw(translated “Serial and Batch Bundle {0} is already used in {1} {2}.”.format(Platform.bold(data.serial\_and\_batch\_bundle), data.voucher\_type, data.voucher\_no)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L407)

<a id="op-9bc36743aa1616"></a>
### Stock Controller.get item wise inventory account map

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_item_wise_inventory_account_map`

**Inputs** self.

**Explicit results** inventory\_account\_map.

**Local steps**

- Set inventory\_account\_map from Platform.\_dict().
- For each table in list(“items”, “packed\_items”, “supplied\_items”, “stock\_items”).
  - If not self.get(table).
    - Continue with the next iteration or loop test.
  - Set \_map from get\_item\_wise\_inventory\_account\_map(self.get(table), self.company).
  - Evaluate inventory\_account\_map.update(\_map).
- Return inventory\_account\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L962) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L639)

<a id="op-7feb3ef5e4cb33"></a>
### Stock Controller.use item inventory account

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_use_item_inventory_account`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Company”, self.company, “enable\_item\_wise\_inventory\_account”).

**Local steps**

- Return Platform.get\_cached\_value(“Company”, self.company, “enable\_item\_wise\_inventory\_account”).

**Derived worked case from the contract** An enabled flag for company A selects the per-item route whenever the caller queries A. Company B supplies its own flag.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “enable\_item\_wise\_inventory\_account”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0441.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L660) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-28a7e9087c9063"></a>
### Stock Controller.get inventory account dict

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_inventory_account_mapping`

**Inputs** self, row, inventory\_account\_map, warehouse\_field = no value, raise\_error (named only, default true).

**Record and data access** resolve a document from “Warehouse” via get\_cached\_doc · read “Account” via get\_cached\_value.

**Explicit results** account\_dict.

**Explicit failure paths** validation helper — translated “Please set default inventory account for item {0}, or their item group or brand.”.format(bold(item\_code)).

**Local steps**

- Set account\_dict from Platform.\_dict().
- If isinstance(row, dict).
  - Set row from Platform.\_dict(row).
- If self.use\_item\_inventory\_account.
  - Set item\_code from row.rm\_item\_code when (hasattr(row, “rm\_item\_code”) and row.rm\_item\_code), otherwise row.item\_code.
    - Value choice on (hasattr(row, “rm\_item\_code”) and row.rm\_item\_code) — true gives row.rm\_item\_code, false gives row.item\_code.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(row, “rm\_item\_code”) → row.rm\_item\_code.
  - Set account\_dict from inventory\_account\_map.get(item\_code).
  - If not account\_dict.
    - Call the validation error handler Platform.throw(translated “Please set default inventory account for item {0}, or their item group or brand.”.format(bold(item\_code))).
  - Return account\_dict.
- If not warehouse\_field.
  - Set warehouse\_field from “warehouse”.
- Set warehouse from row.get(warehouse\_field).
- If not warehouse.
  - Set warehouse from self.get(warehouse\_field).
- If warehouse.
  - Set account\_dict from inventory\_account\_map.get(warehouse).
  - If (not account\_dict and raise\_error).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account\_dict → raise\_error.
    - Set account from get\_warehouse\_account(Platform.get\_cached\_doc(“Warehouse”, warehouse)).
    - Set account\_dict from Platform.\_dict(account = account, account\_currency = Platform.get\_cached\_value(“Account”, account, “account\_currency”)).
    - Set inventory\_account\_map at warehouse from account\_dict.
- Return account\_dict.

**Derived worked case from the contract** With a warehouse account map initially empty, a warehouse resolving to Stock EUR yields that account and its stored currency and fills the cache for subsequent rows.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Warehouse”, warehouse), Platform.get\_cached\_value(“Account”, account, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0441.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L959) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L637) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-bbc9dc6a238ee8"></a>
### Stock Controller.get inventory account map

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_get_inventory_account_map`

**Inputs** self.

**Explicit results** self.get\_item\_wise\_inventory\_account\_map() · get\_warehouse\_account\_map(self.company).

**Local steps**

- If self.use\_item\_inventory\_account.
  - Return self.get\_item\_wise\_inventory\_account\_map().
- Return get\_warehouse\_account\_map(self.company).

**Derived worked case from the contract** With warehouse accounting enabled through the item-account switch being off, two items at the same warehouse look up the same warehouse key.

**Methods declared on this owner** [get item wise inventory account map](operations-023.md#op-9bc36743aa1616).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0441.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L636) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-1962b7ab32e527"></a>
### Stock Controller.make gl entries

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_make_general_ledger_entries`

**Inputs** self, gl\_entries = no value, from\_repost = false, via\_landed\_cost\_voucher = false.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If self.docstatus equals 2.
  - Evaluate make\_reverse\_gl\_entries(voucher\_type = self.doctype, voucher\_no = self.name).
- Set provisional\_accounting\_for\_non\_stock\_items from cint(Platform.get\_cached\_value(“Company”, self.company, “enable\_provisional\_accounting\_for\_non\_stock\_items”)).
- Set is\_asset\_pr from any(generator of d.get(“is\_fixed\_asset”) for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
- Set need\_inventory\_map from ((self.get\_stock\_items() or self.get(“packed\_items”)) and cint(Enterprise.is\_perpetual\_inventory\_enabled(self.company))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.get\_stock\_items() or self.get(“packed\_items”)) → cint(Enterprise.is\_perpetual\_inventory\_enabled(self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_stock\_items() → self.get(“packed\_items”).
- Set inventory\_account\_map from Platform.\_dict().
- If need\_inventory\_map.
  - Set inventory\_account\_map from self.get\_inventory\_account\_map().
- If (need\_inventory\_map or provisional\_accounting\_for\_non\_stock\_items or is\_asset\_pr).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in need\_inventory\_map → provisional\_accounting\_for\_non\_stock\_items → is\_asset\_pr.
  - If self.docstatus equals 1.
    - If not gl\_entries.
      - Set gl\_entries from self.get\_gl\_entries(inventory\_account\_map, via\_landed\_cost\_voucher) when self.doctype equals “Purchase Receipt”, otherwise self.get\_gl\_entries(inventory\_account\_map).
        - Value choice on self.doctype equals “Purchase Receipt” — true gives self.get\_gl\_entries(inventory\_account\_map, via\_landed\_cost\_voucher), false gives self.get\_gl\_entries(inventory\_account\_map).
    - Evaluate make\_gl\_entries(gl\_entries, from\_repost = from\_repost).

If control reaches the end, it returns no value.

**Derived worked case from the contract** A submitted purchase receipt containing only a fixed asset can enter the journal path with an empty inventory map. A cancelled receipt requests reversal and creates no forward journal through this branch.

**Methods declared on this owner** [get inventory account map](operations-023.md#op-bbc9dc6a238ee8), [get gl entries](operations-024.md#op-cd83339415d33f).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “enable\_provisional\_accounting\_for\_non\_stock\_items”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0441.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L968) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L645) · [Worked case record](../../../../../docs/rebuild/checkpoint-corrections/stock-controller.json)

<a id="op-9643f74ec85910"></a>
### Stock Controller.validate serialized batch

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_serialized_batch`

**Inputs** self.

**Record and data access** read “Serial No” via get\_all · read “Batch” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Serial No {1} does not belong to Batch {2}”.format(d.idx, row.name, d.batch\_no).

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set is\_material\_issue from false.
- If (self.doctype equals “Stock Entry” and self.purpose belongs to list(“Material Issue”, “Material Transfer”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Stock Entry” → self.purpose belongs to list(“Material Issue”, “Material Transfer”).
  - Set is\_material\_issue from true.
- Set check\_batches from self.is\_batch\_check\_needed().
- For each d in self.get(“items”).
  - If (hasattr(d, “serial\_no”) and hasattr(d, “batch\_no”) and d.serial\_no and d.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(d, “serial\_no”) → hasattr(d, “batch\_no”) → d.serial\_no → d.batch\_no.
    - Set serial\_nos from Platform.get\_all(“Serial No”, fields = list(“batch\_no”, “name”, “warehouse”), filters = mapping(“name” → tuple(“in”, get\_serial\_nos(d.serial\_no)))).
    - For each row in serial\_nos.
      - If (row.warehouse and row.batch\_no differs from d.batch\_no).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.warehouse → row.batch\_no differs from d.batch\_no.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Serial No {1} does not belong to Batch {2}”.format(d.idx, row.name, d.batch\_no)).
  - If (check\_batches and flt(d.qty) &gt; 0.0 and d.get(“batch\_no”) and self.get(“posting\_date”) and self.docstatus &lt; 2).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in check\_batches → flt(d.qty) &gt; 0.0 → d.get(“batch\_no”) → self.get(“posting\_date”) → self.docstatus &lt; 2.
    - Set tuple(expiry\_date, disabled) from Platform.get\_cached\_value(“Batch”, d.get(“batch\_no”), list(“expiry\_date”, “disabled”)).
    - Evaluate self.validate\_batch\_is\_usable(d.idx, d.batch\_no, no value when is\_material\_issue, otherwise expiry\_date, disabled).
      - Value choice on is\_material\_issue — true gives no value, false gives expiry\_date.
- If check\_batches.
  - Evaluate self.validate\_outward\_bundle\_batches(check\_expiry = not is\_material\_issue).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is batch check needed](operations-023.md#op-efef9d2489d4d9), [validate batch is usable](operations-023.md#op-7513959721aec6), [validate outward bundle batches](operations-023.md#op-0bc121e2b0f242).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Batch”, d.get(“batch\_no”), list(“expiry\_date”, “disabled”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L424)

<a id="op-efef9d2489d4d9"></a>
### Stock Controller.is batch check needed

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_is_batch_check_needed`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · (not is\_invoice or bool(self.get(“update\_stock”))).

**Local steps**

- If self.flags.is\_consolidated.
  - Return false.
- Set is\_invoice from self.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
- Return (not is\_invoice or bool(self.get(“update\_stock”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_invoice → bool(self.get(“update\_stock”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L393)

<a id="op-7513959721aec6"></a>
### Stock Controller.validate batch is usable

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_batch_is_usable`

**Inputs** self, idx, batch\_no, expiry\_date, disabled.

**Explicit failure paths** validation helper — translated “Row #{0}: The batch {1} is disabled.”.format(idx, get\_link\_to\_form(“Batch”, batch\_no)) · validation helper with BatchExpiredError — translated “Row #{0}: The batch {1} has already expired.”.format(idx, get\_link\_to\_form(“Batch”, batch\_no)).

**Local steps**

- If disabled.
  - Call the validation error handler Platform.throw(translated “Row #{0}: The batch {1} is disabled.”.format(idx, get\_link\_to\_form(“Batch”, batch\_no))).
- If (expiry\_date and getdate(expiry\_date) &lt; getdate(self.posting\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in expiry\_date → getdate(expiry\_date) &lt; getdate(self.posting\_date).
  - Call the validation error handler Platform.throw(translated “Row #{0}: The batch {1} has already expired.”.format(idx, get\_link\_to\_form(“Batch”, batch\_no)), BatchExpiredError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1166) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L406)

<a id="op-0bc121e2b0f242"></a>
### Stock Controller.validate outward bundle batches

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_validate_outward_bundle_batches`

**Inputs** self, check\_expiry = true, rows = no value, qty\_field = “qty”.

**Explicit results** no value.

**Local steps**

- If (self.get(“is\_return”) or not self.get(“posting\_date”) or self.docstatus equals 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_return”) → not self.get(“posting\_date”) → self.docstatus equals 2.
  - Return no value.
- If rows is identical to no value.
  - Set rows from ((self.get(“items”) or list()) + (self.get(“packed\_items”) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“items”) → list().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“packed\_items”) → list().
- Set row\_idx\_by\_bundle from mapping of d.serial\_and\_batch\_bundle → d.idx for d drawn from rows where (d.get(“serial\_and\_batch\_bundle”) and flt(d.get(qty\_field)) &gt; 0).
  - Draw d from rows, keep a combination only if ((d.get(“serial\_and\_batch\_bundle”) and flt(d.get(qty\_field)) &gt; 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“serial\_and\_batch\_bundle”) → flt(d.get(qty\_field)) &gt; 0.
- If not row\_idx\_by\_bundle.
  - Return no value.
- Set posting\_date from self.posting\_date when check\_expiry, otherwise no value.
  - Value choice on check\_expiry — true gives self.posting\_date, false gives no value.
- For each row in get\_unusable\_outward\_bundle\_batches(list(row\_idx\_by\_bundle), posting\_date).
  - Evaluate self.validate\_batch\_is\_usable(row\_idx\_by\_bundle at row.bundle, row.batch\_no, row.expiry\_date when check\_expiry, otherwise no value, row.disabled).
    - Value choice on check\_expiry — true gives row.expiry\_date, false gives no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate batch is usable](operations-023.md#op-7513959721aec6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L416)

<a id="op-232168d6781351"></a>
### Stock Controller.clean serial nos

`operation_enterprise_binding_enterprise_controllers_stock_controller_stockcontroller_clean_serial_nos`

**Inputs** self.

**Local steps**

- Bind dependencies clean\_serial\_no\_string.
- For each row in self.get(“items”).
  - If (hasattr(row, “serial\_no”) and row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(row, “serial\_no”) → row.serial\_no.
    - Set row.serial\_no from clean\_serial\_no\_string(row.serial\_no).
- For each row in (self.get(“packed\_items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“packed\_items”) → list().
  - If (hasattr(row, “serial\_no”) and row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(row, “serial\_no”) → row.serial\_no.
    - Set row.serial\_no from clean\_serial\_no\_string(row.serial\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L374)

<a id="op-8d5d9808378f14"></a>
### Stock Controller.make bundle using old serial batch fields

`operation_enterprise_controllers_stock_controller_business_behavior_stock_controller_make_bundle_using_old_serial_batch_fields`

**Inputs** self, table\_name = no value, via\_landed\_cost\_voucher = false.

**Explicit results** no value.

**Local steps**

- If self.get(“\_action”) equals “update\_after\_submit”.
  - Return no value.
- If (Platform.in\_test and Platform.flags.use\_serial\_and\_batch\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.in\_test → Platform.flags.use\_serial\_and\_batch\_fields.
  - Return no value.
- If not table\_name.
  - Set table\_name from “items”.
- If self.doctype equals “Asset Capitalization”.
  - Set table\_name from “stock\_items”.
- Set parent\_details from Platform.\_dict().
- If table\_name equals “packed\_items”.
  - Set parent\_details from self.get\_parent\_details\_for\_packed\_items().
- Set auto\_pick\_outward from self.auto\_picks\_outward\_serial\_batch().
- Set picked\_serial\_nos, picked\_batches from no value.
- If auto\_pick\_outward.
  - Set picked\_serial\_nos from self.get\_serial\_nos\_used\_in\_rows().
  - Set picked\_batches from self.get\_batches\_used\_in\_rows().
- For each row in self.get(table\_name).
  - Set item\_code from (row.get(“rm\_item\_code”) or row.get(“item\_code”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“rm\_item\_code”) → row.get(“item\_code”).
  - If (not item\_code or not self.is\_serial\_batch\_item(item\_code)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_code → not self.is\_serial\_batch\_item(item\_code).
    - Continue with the next iteration or loop test.
  - If (not via\_landed\_cost\_voucher and row.serial\_and\_batch\_bundle and (row.serial\_no or row.batch\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not via\_landed\_cost\_voucher → row.serial\_and\_batch\_bundle → (row.serial\_no or row.batch\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no.
    - Evaluate self.validate\_serial\_nos\_and\_batches\_with\_bundle(row).
  - If (not row.serial\_no and not row.batch\_no and not row.get(“rejected\_serial\_no”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.serial\_no → not row.batch\_no → not row.get(“rejected\_serial\_no”).
    - If not (auto\_pick\_outward and row.get(“use\_serial\_batch\_fields”) and flt(row.get(“qty”)) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in auto\_pick\_outward → row.get(“use\_serial\_batch\_fields”) → flt(row.get(“qty”)) &gt; 0.
      - Continue with the next iteration or loop test.
  - If (not row.use\_serial\_batch\_fields and (row.serial\_no or row.batch\_no or row.get(“rejected\_serial\_no”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.use\_serial\_batch\_fields → (row.serial\_no or row.batch\_no or row.get(“rejected\_serial\_no”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.serial\_no → row.batch\_no → row.get(“rejected\_serial\_no”).
    - Set row.use\_serial\_batch\_fields from 1.
  - If (row.use\_serial\_batch\_fields and (not row.serial\_and\_batch\_bundle and not row.get(“rejected\_serial\_and\_batch\_bundle”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.use\_serial\_batch\_fields → (not row.serial\_and\_batch\_bundle and not row.get(“rejected\_serial\_and\_batch\_bundle”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.serial\_and\_batch\_bundle → not row.get(“rejected\_serial\_and\_batch\_bundle”).
    - Set bundle\_details from mapping(“item\_code” → (row.get(“rm\_item\_code”) or row.item\_code), “posting\_datetime” → combine\_datetime(self.posting\_date, self.posting\_time), “voucher\_type” → self.doctype, “voucher\_no” → self.name, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“rm\_item\_code”) → row.item\_code.
      - Value choice on row.get(“rejected\_warehouse”) — true gives 1, false gives 0.
      - Value choice on not via\_landed\_cost\_voucher — true gives true, false gives false.
    - If (self.is\_internal\_transfer() and row.get(“from\_warehouse”) and not self.is\_return).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → row.get(“from\_warehouse”) → not self.is\_return.
      - Evaluate self.update\_bundle\_details(bundle\_details, table\_name, row).
      - Set bundle\_details at “type\_of\_transaction” from “Outward”.
      - Set bundle\_details at “warehouse” from row.get(“from\_warehouse”).
      - Set bundle\_details at “qty” from (row.get(“stock\_qty”) or row.get(“qty”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“stock\_qty”) → row.get(“qty”).
      - Evaluate self.create\_serial\_batch\_bundle(bundle\_details, row).
      - Continue with the next iteration or loop test.
    - If (row.get(“qty”) or row.get(“consumed\_qty”) or row.get(“stock\_qty”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“qty”) → row.get(“consumed\_qty”) → row.get(“stock\_qty”).
      - Evaluate self.update\_bundle\_details(bundle\_details, table\_name, row, parent\_details = parent\_details).
      - Evaluate self.create\_auto\_picked\_bundle(bundle\_details, row, picked\_serial\_nos, picked\_batches).
    - If self.get\_rejected\_stock\_qty(row).
      - Evaluate self.update\_bundle\_details(bundle\_details, table\_name, row, is\_rejected = true).
      - Evaluate self.create\_serial\_batch\_bundle(bundle\_details, row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get parent details for packed items](operations-024.md#op-fe206441fa2192), [auto picks outward serial batch](operations-024.md#op-2e58de777b7e65), [get serial nos used in rows](operations-024.md#op-de27d6f6cbe084), [get batches used in rows](operations-024.md#op-4a933e693a0bd2), [is serial batch item](operations-024.md#op-5219fa77dc344f), [validate serial nos and batches with bundle](operations-024.md#op-87162f775da4dd), [update bundle details](operations-024.md#op-9a4bfbf8cb752b), [create serial batch bundle](operations-024.md#op-19c69b2a367f92), [create auto picked bundle](operations-024.md#op-e957efecf3b3c4), [get rejected stock qty](operations-024.md#op-17db5cd27dc4ff).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L967) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L644)
