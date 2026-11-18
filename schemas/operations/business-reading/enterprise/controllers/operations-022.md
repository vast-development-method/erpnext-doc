# Shared transaction rules · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Selling controller

<a id="op-cafae1f958a517"></a>
### Selling Controller.update pick list status

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_update_pick_list_status`

**Inputs** self.

**Local steps**

- Bind dependencies update\_pick\_list\_status.
- Set pick\_lists from set of row.against\_pick\_list for row drawn from self.items where row.against\_pick\_list.
  - Draw row from self.items, keep a combination only if (row.against\_pick\_list).
- For each pick\_list in pick\_lists.
  - Evaluate update\_pick\_list\_status(pick\_list).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0389.json#L6083) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L580)

<a id="op-8f7775f8399e53"></a>
### Remove delivered entries

`operation_enterprise_binding_enterprise_controllers_selling_controller_remove_delivered_entries`

**Inputs** package, pick\_list\_item.

**Local steps**

- Bind dependencies get\_moved\_entries.
- Set delivered from get\_moved\_entries(list(pick\_list\_item)).get(pick\_list\_item, list()).
- Set delivered\_serial\_nos from set of row.serial\_no for row drawn from delivered where row.serial\_no.
  - Draw row from delivered, keep a combination only if (row.serial\_no).
- Set delivered\_batch\_qty from defaultdict(float).
- For each row in delivered.
  - If (row.batch\_no and not row.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → not row.serial\_no.
    - Update delivered\_batch\_qty at row.batch\_no using + abs(row.qty).
- For each row in list(package.entries).
  - If row.serial\_no.
    - If row.serial\_no belongs to delivered\_serial\_nos.
      - Evaluate package.remove(row).
    - Continue with the next iteration or loop test.
  - Set taken from min(delivered\_batch\_qty at row.batch\_no, abs(row.qty)).
  - Update delivered\_batch\_qty at row.batch\_no using − taken.
  - Set row.qty from flt((abs(row.qty) − taken), row.precision(“qty”)).
  - If not row.qty.
    - Evaluate package.remove(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L342)

<a id="op-7229e9da1740b7"></a>
### Set default income account for item

`operation_enterprise_controllers_selling_controller_business_behavior_set_default_income_account_for_item`

**Inputs** obj.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Set company\_default from Platform.get\_cached\_value(“Company”, obj.company, “default\_income\_account”).
- For each d in sorted(obj.get(“items”, default = list()), key = deferred anonymous expression).
  - Set income\_account from getattr(d, “income\_account”, no value).
  - If (d.item\_code and income\_account and income\_account differs from company\_default).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code → income\_account → income\_account differs from company\_default.
    - Evaluate set\_item\_default(d.item\_code, obj.company, “income\_account”, income\_account).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, obj.company, “default\_income\_account”) · selected callable from getattr(d, “income\_account”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L913) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L594)

<a id="op-773b3097dec937"></a>
### Get serial and batch bundle

`operation_enterprise_controllers_selling_controller_business_behavior_get_serial_and_batch_bundle`

**Inputs** child, parent, delivery\_note\_child = no value, picked\_serial\_nos = no value, picked\_batches = no value.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Item” via get\_value.

**State and service calls** call db\_set on child.

**Explicit results** no value · doc.name.

**Local steps**

- Bind dependencies SerialBatchCreation.
- If (parent.get(“is\_return”) and parent.get(“packed\_items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent.get(“is\_return”) → parent.get(“packed\_items”).
  - Return no value.
- If (child.get(“use\_serial\_batch\_fields”) or child.get(“serial\_no”) or child.get(“batch\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in child.get(“use\_serial\_batch\_fields”) → child.get(“serial\_no”) → child.get(“batch\_no”).
  - Return no value.
- If not Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).
  - Return no value.
- Set item\_details from Platform.db.get\_value(“Item”, child.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
- If (not item\_details.has\_serial\_no and not item\_details.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_details.has\_serial\_no → not item\_details.has\_batch\_no.
  - Return no value.
- Set sn\_doc from SerialBatchCreation(mapping(“item\_code” → child.item\_code, “warehouse” → child.warehouse, “voucher\_type” → parent.doctype, “voucher\_no” → parent.name when parent.docstatus &lt; 2, otherwise no value, …)).
  - Value choice on parent.docstatus &lt; 2 — true gives parent.name, false gives no value.
  - Value choice on delivery\_note\_child — true gives delivery\_note\_child.name, false gives child.name.
  - Value choice on (child.qty &gt; 0 and parent.docstatus &lt; 2) — true gives “Outward”, false gives “Inward”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in child.qty &gt; 0 → parent.docstatus &lt; 2.
  - Value choice on picked\_serial\_nos — true gives picked\_serial\_nos at child.item\_code, false gives no value.
- Set doc from sn\_doc.make\_serial\_and\_batch\_bundle().
- Evaluate child.db\_set(“serial\_and\_batch\_bundle”, doc.name).
- If picked\_serial\_nos is distinct from no value.
  - Evaluate picked\_serial\_nos at child.item\_code.extend(generator of d.serial\_no for d drawn from (doc.get(“entries”) or list()) where d.serial\_no).
    - Draw d from (doc.get(“entries”) or list()), keep a combination only if (d.serial\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“entries”) → list().
- If picked\_batches is distinct from no value.
  - Evaluate add\_picked\_batches(picked\_batches, (doc.get(“entries”) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“entries”) → list().
- Return doc.name.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L551)

<a id="op-a824b18f1a3f09"></a>
### Get delivered serial batch for reservation

`operation_enterprise_controllers_selling_controller_business_behavior_get_delivered_serial_batch_for_reservation`

**Inputs** item.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**Explicit results** tuple(serial\_nos, batch\_qty).

**Local steps**

- Set tuple(serial\_nos, batch\_qty) from tuple(list(), mapping()).
- If item.get(“serial\_and\_batch\_bundle”).
  - Set bundle from Platform.get\_doc(“Serial and Batch Bundle”, item.serial\_and\_batch\_bundle).
  - For each row in bundle.entries.
    - If row.serial\_no.
      - Evaluate serial\_nos.append(row.serial\_no).
    - If row.batch\_no.
      - Set batch\_qty at row.batch\_no from (batch\_qty.get(row.batch\_no, 0) + abs(flt(row.qty))).
- Otherwise.
  - Bind dependencies get\_serial\_nos.
  - If item.get(“serial\_no”).
    - Set serial\_nos from get\_serial\_nos(item.serial\_no).
  - If item.get(“batch\_no”).
    - Set batch\_qty at item.batch\_no from abs(flt((item.get(“stock\_qty”) or item.get(“qty”)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“stock\_qty”) → item.get(“qty”).
- Return tuple(serial\_nos, batch\_qty).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0390.json#L762) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L869) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L550)

<a id="op-951eb3038b1dfa"></a>
### Get reserved warehouses by order row

`operation_enterprise_binding_enterprise_controllers_selling_controller_get_reserved_warehouses_by_order_row`

**Inputs** so\_details.

**Declared result** dict.

**Explicit results** mapping() · reserved\_warehouses.

**Local steps**

- If not so\_details.
  - Return mapping().
- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set rows from nested operand in the contract(nested operand in the contract).groupby(sre.voucher\_detail\_no, sre.warehouse).orderby(Min(sre.creation)).run(as\_dict = true).
- Set reserved\_warehouses from mapping().
- For each row in rows.
  - Evaluate reserved\_warehouses.setdefault(row.voucher\_detail\_no, list()).append(row.warehouse).
- Return reserved\_warehouses.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L341)

<a id="op-85a96e8cf3e81d"></a>
### Get ledger qty

`operation_enterprise_binding_enterprise_controllers_selling_controller_get_ledger_qty`

**Inputs** qty.

**Declared result** float.

**Explicit results** flt(qty, Platform.get\_precision(“Stock Ledger Entry”, “actual\_qty”)).

**Local steps**

- Return flt(qty, Platform.get\_precision(“Stock Ledger Entry”, “actual\_qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L340)

## Service · Status updater

<a id="op-21c14d411cd273"></a>
### Validate status

`operation_enterprise_controllers_status_updater_business_behavior_validate_status`

**Inputs** status, options.

**Explicit failure paths** validation helper — translated “Status must be one of {0}”.format(comma\_or(options)).

**Local steps**

- If status does not belong to options.
  - Call the validation error handler Platform.throw(translated “Status must be one of {0}”.format(comma\_or(options))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0390.json#L1273) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L614)

<a id="op-5678e3e281a9a7"></a>
### Status Updater.on discard

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If self.meta.has\_field(“status”).
  - Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0390.json#L1403) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L602)

<a id="op-54dd7c83576bdf"></a>
### Status Updater.update prevdoc status

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_prevdoc_status`

**Inputs** self.

**Local steps**

- Evaluate self.update\_qty().
- Evaluate self.validate\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update qty](operations-022.md#op-26cf55ad3fada8), [validate qty](operations-022.md#op-32efb62523bbe7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L610)

<a id="op-9c7e634f71f252"></a>
### Status Updater.set status

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_set_status`

**Inputs** self, update = false, status = no value, update\_modified = true.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If self.is\_new().
  - If self.get(“amended\_from”).
    - Set self.status from “Draft”.
  - Return no value.
- If self.doctype does not belong to status\_map.
  - Return no value.
- Set \_status from self.status.
- Set self.status from status when status, otherwise self.status.
  - Value choice on status — true gives status, false gives self.status.
- Set new\_status from self.get\_status() at “status”.
- If new\_status differs from \_status.
  - If new\_status does not belong to tuple(“Cancelled”, “Partially Ordered”, “Ordered”, “Issued”, …).
    - Evaluate self.add\_comment(“Label”, translated new\_status).
  - Set self.status from new\_status.
  - If update.
    - Evaluate self.db\_set(“status”, new\_status, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get status](operations-022.md#op-6e692c831e8311).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0390.json#L2398) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L603)

<a id="op-6e692c831e8311"></a>
### Status Updater.get status

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_get_status`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0390.json#L2831) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L600)

<a id="op-32efb62523bbe7"></a>
### Status Updater.validate qty

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_validate_quantity`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Buying Settings” via get\_single\_value · read “Production Plan Sub Assembly Item” via get\_all.

**Explicit failure paths** validation helper — translated “For an item {0}, quantity must be positive number”.format(d.item\_code) · validation helper — translated “For an item {0}, quantity must be negative number”.format(d.item\_code) · validation helper — translated “For item {0}, rate must be a positive number. To Allow negative rates, enable {1} in {2}”.format(Platform.bold(d.item\_code), Platform.bold(translated “′Allow Negative rates for Items′”), get\_li ….

**Local steps**

- Set selling\_doctypes from tuple(“Sales Order”, “Sales Invoice”, “Delivery Note”).
- Set buying\_doctypes from tuple(“Purchase Order”, “Purchase Invoice”, “Purchase Receipt”).
- For each args in self.status\_updater.
  - If (“target\_ref\_field” does not belong to args or args.get(“validate\_qty”) is identical to false).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “target\_ref\_field” does not belong to args → args.get(“validate\_qty”) is identical to false.
    - Continue with the next iteration or loop test.
  - Set self.item\_allowance from mapping().
  - Set self.global\_qty\_allowance from no value.
  - Set self.global\_amount\_allowance from no value.
  - Set items\_to\_validate from list().
  - Set selling\_negative\_rate\_allowed from Platform.get\_single\_value(“Selling Settings”, “allow\_negative\_rates\_for\_items”).
  - Set buying\_negative\_rate\_allowed from Platform.get\_single\_value(“Buying Settings”, “allow\_negative\_rates\_for\_items”).
  - For each d in self.get\_all\_children().
    - If (hasattr(d, “qty”) and flt(d.qty) &lt; 0 and not self.get(“is\_return”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(d, “qty”) → flt(d.qty) &lt; 0 → not self.get(“is\_return”).
      - Call the validation error handler Platform.throw(translated “For an item {0}, quantity must be positive number”.format(d.item\_code)).
    - If (hasattr(d, “qty”) and flt(d.qty) &gt; 0 and self.get(“is\_return”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(d, “qty”) → flt(d.qty) &gt; 0 → self.get(“is\_return”).
      - Call the validation error handler Platform.throw(translated “For an item {0}, quantity must be negative number”.format(d.item\_code)).
    - If ((not selling\_negative\_rate\_allowed and self.doctype belongs to selling\_doctypes) or (not buying\_negative\_rate\_allowed and self.doctype belongs to buying\_doctypes)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not selling\_negative\_rate\_allowed and self.doctype belongs to selling\_doctypes) → (not buying\_negative\_rate\_allowed and self.doctype belongs to buying\_doctypes).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not selling\_negative\_rate\_allowed → self.doctype belongs to selling\_doctypes.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not buying\_negative\_rate\_allowed → self.doctype belongs to buying\_doctypes.
      - If (hasattr(d, “item\_code”) and hasattr(d, “rate”) and flt(d.rate) &lt; 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(d, “item\_code”) → hasattr(d, “rate”) → flt(d.rate) &lt; 0.
        - Call the validation error handler Platform.throw(translated “For item {0}, rate must be a positive number. To Allow negative rates, enable {1} in {2}”.format(Platform.bold(d.item\_code), Platform.bold(translated “′Allow Negative rates for I ….
          - Value choice on self.doctype belongs to selling\_doctypes — true gives “Selling Settings”, false gives “Buying Settings”.
    - If (d.doctype equals args at “source\_dt” and d.get(args at “join\_field”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.doctype equals args at “source\_dt” → d.get(args at “join\_field”).
      - Evaluate items\_to\_validate.append(Platform.\_dict(mapping(“name” → d.get(args at “join\_field”), “production\_plan\_sub\_assembly\_item” → d.get(“production\_plan\_sub\_assembly\_item”), “idx” → d.idx, “child\_doc” → d))).
  - Set skip\_on\_cancel from (self.docstatus equals 2 and args.get(“overflow\_type”) equals “installation”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 2 → args.get(“overflow\_type”) equals “installation”.
  - If (self.get(“is\_return”) and args.get(“overflow\_type”) equals “billing”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → args.get(“overflow\_type”) equals “billing”.
    - If (args.get(“billing\_flag”) and not self.get(args at “billing\_flag”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“billing\_flag”) → not self.get(args at “billing\_flag”).
      - Set items\_to\_validate from list().
    - Otherwise.
      - If self.docstatus differs from 2.
        - Set items\_to\_validate from list of d for d drawn from items\_to\_validate where (flt(nested operand in the contract.child\_doc.get(“qty”)) × flt(nested operand in the contract.child\_doc.get(“rate”))) &gt; 0.
          - Draw d from items\_to\_validate, keep a combination only if ((flt(d.child\_doc.get(“qty”)) × flt(d.child\_doc.get(“rate”))) &gt; 0).
  - If (items\_to\_validate and not skip\_on\_cancel).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in items\_to\_validate → not skip\_on\_cancel.
    - Set pp\_sub\_assembly\_items from list of item.production\_plan\_sub\_assembly\_item for item drawn from items\_to\_validate where item.production\_plan\_sub\_assembly\_item.
      - Draw item from items\_to\_validate, keep a combination only if (item.production\_plan\_sub\_assembly\_item).
    - Set pp\_subcontract\_items from list().
    - If pp\_sub\_assembly\_items.
      - Set pp\_subcontract\_items from Platform.db.get\_all(“Production Plan Sub Assembly Item”, filters = mapping(“name” → tuple(“in”, pp\_sub\_assembly\_items), “type\_of\_manufacturing” → “Subcontract”), pluck = “name”).
    - Set regular\_items from list().
    - Set pp\_items from list().
    - For each item in items\_to\_validate.
      - If item.production\_plan\_sub\_assembly\_item belongs to pp\_subcontract\_items.
        - Evaluate pp\_items.append(item.name).
      - Otherwise.
        - Evaluate regular\_items.append(item.name).
    - Set item\_details from list().
    - If regular\_items.
      - Evaluate item\_details.extend(self.fetch\_items\_with\_pending\_qty(args, “item\_code”, regular\_items)).
    - If (pp\_items and args.get(“target\_dt”) belongs to list(“Production Plan Sub Assembly Item”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pp\_items → args.get(“target\_dt”) belongs to list(“Production Plan Sub Assembly Item”).
      - Evaluate item\_details.extend(self.fetch\_items\_with\_pending\_qty(args, “production\_item”, pp\_items)).
    - Set item\_lookup from mapping of item.name → item for item drawn from item\_details.
      - Draw item from item\_details.
    - For each child\_item in items\_to\_validate.
      - Set item from item\_lookup.get(child\_item.name).
      - If item.
        - Set item at “idx” from child\_item.idx.
        - Set item at “target\_ref\_field” from args at “target\_ref\_field”.replace(“\_”, one space).
        - If args.get(“no\_allowance”).
          - Set item at “reduce\_by” from (item at args at “target\_field” − item at args at “target\_ref\_field”).
          - If item at “reduce\_by” &gt; 0.01.
            - Evaluate self.limits\_crossed\_error(args, item, “qty”).
        - Otherwise.
          - If item at args at “target\_ref\_field”.
            - Evaluate self.check\_overflow\_with\_allowance(item, args).
          - Otherwise.
            - If (args.get(“overflow\_type”) equals “installation” and flt(item at args at “target\_field”) &gt; 0).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“overflow\_type”) equals “installation” → flt(item at args at “target\_field”) &gt; 0.
              - Set item at “reduce\_by” from flt(item at args at “target\_field”).
              - Evaluate self.limits\_crossed\_error(args, item, “qty”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch items with pending qty](operations-022.md#op-bb2d1011df1496), [limits crossed error](operations-022.md#op-4b62c30ca24b8c), [check overflow with allowance](operations-022.md#op-d29dc4db946b37).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_negative\_rates\_for\_items”), Platform.get\_single\_value(“Buying Settings”, “allow\_negative\_rates\_for\_items”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L612)

<a id="op-bb2d1011df1496"></a>
### Status Updater.fetch items with pending qty

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_fetch_items_with_pending_quantity`

**Inputs** self, args, item\_field, items.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(args at “target\_dt”).
- Set item\_field\_col from doctype at item\_field.
- Set target\_field from doctype at args at “target\_field”.
- Set is\_qty\_check from “qty” belongs to args at “target\_ref\_field”.
- Set is\_installation from args.get(“overflow\_type”) equals “installation”.
- If is\_installation.
  - Set target\_ref\_value from (doctype at args at “target\_ref\_field” − (doctype.returned\_qty ÷ doctype.conversion\_factor)).
- Otherwise.
  - Set target\_ref\_value from doctype at args at “target\_ref\_field”.
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(target\_ref\_value &lt; target\_field).wher ….
- If (is\_qty\_check and not is\_installation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_qty\_check → not is\_installation.
  - Set item\_table from Platform.qb.DocType(“Item”).
  - Set bundle from Platform.qb.DocType(“Product Bundle”).
  - Set active\_bundle\_items from nested operand in the contract.qb.from\_(bundle).select(bundle.new\_item\_code).where(bundle.disabled equals 0).
  - Set query from query.join(item\_table).on(item\_table.name equals item\_field\_col).where((item\_table.is\_stock\_item equals 1 bitwise or item\_field\_col.isin(active\_bundle\_items))).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L599)

<a id="op-d29dc4db946b37"></a>
### Status Updater.check overflow with allowance

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_check_overflow_with_allowance`

**Inputs** self, item, args.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Accounts Settings” via get\_single\_value.

**Local steps**

- Set qty\_or\_amount from “qty” when “qty” belongs to args at “target\_ref\_field”, otherwise “amount”.
  - Value choice on “qty” belongs to args at “target\_ref\_field” — true gives “qty”, false gives “amount”.
- Set global\_qty\_allowance\_field from args.get(“global\_allowance\_field”, “over\_delivery\_receipt\_allowance”).
- Set global\_qty\_allowance\_doctype from args.get(“global\_allowance\_doctype”, “Stock Settings”).
- Set item\_qty\_allowance\_field from args.get(“item\_allowance\_field”, “over\_delivery\_receipt\_allowance”).
- Set tuple(allowance, self.item\_allowance, self.global\_qty\_allowance, self.global\_amount\_allowance) from get\_allowance\_for(item at “item\_code”, self.item\_allowance, self.global\_qty\_allowance, self.global\_amount\_allowance, …) when args at “source\_dt” differs from “Pick List Item”, otherwise tuple(0, mapping(), ….
  - Value choice on args at “source\_dt” differs from “Pick List Item” — true gives get\_allowance\_for(item at “item\_code”, self.item\_allowance, self.global\_qty\_allowance, self.global\_amount\_allowance, …), false gives tuple(0, mapping(), no value, no value).
- Set role from no value.
- If qty\_or\_amount equals “qty”.
  - If args.get(“overflow\_type”) belongs to tuple(“delivery”, “receipt”).
    - Set role from Platform.get\_single\_value(“Stock Settings”, “role\_allowed\_to\_over\_deliver\_receive”).
- Otherwise.
  - Set role from Platform.get\_single\_value(“Accounts Settings”, “role\_allowed\_to\_over\_bill”).
- Set overflow\_percent from (((item at args at “target\_field” − item at args at “target\_ref\_field”) ÷ item at args at “target\_ref\_field”) × 100).
- If (overflow\_percent − allowance) &gt; 0.01.
  - Set item at “max\_allowed” from flt(((item at args at “target\_ref\_field” × (100 + allowance)) ÷ 100)).
  - Set item at “reduce\_by” from (item at args at “target\_field” − item at “max\_allowed”).
  - If role does not belong to Platform.get\_roles().
    - Evaluate self.limits\_crossed\_error(args, item, qty\_or\_amount).
  - Otherwise.
    - Evaluate self.warn\_about\_bypassing\_with\_role(item, qty\_or\_amount, role).

If control reaches the end, it returns no value.

**Methods declared on this owner** [limits crossed error](operations-022.md#op-4b62c30ca24b8c), [warn about bypassing with role](operations-022.md#op-27bd97ce080125).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “role\_allowed\_to\_over\_deliver\_receive”), Platform.get\_single\_value(“Accounts Settings”, “role\_allowed\_to\_over\_bill”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0390.json#L6030) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L597)

<a id="op-4b62c30ca24b8c"></a>
### Status Updater.limits crossed error

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_limits_crossed_error`

**Inputs** self, args, item, qty\_or\_amount.

**Explicit results** no value.

**Explicit failure paths** validation helper with OverAllowanceError — (translated “This document is over limit by {0} {1} for item {4}. Are you making another {3} against the same {2}?”.format(Platform.bold(translated nested operand in the contract at nested operand in the c ….

**Local steps**

- If (self.doctype belongs to list(“Sales Invoice”, “Delivery Note”) and qty\_or\_amount equals “amount” and self.is\_internal\_customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Sales Invoice”, “Delivery Note”) → qty\_or\_amount equals “amount” → self.is\_internal\_customer.
  - Return no value.
- Otherwise.
  - If (self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”) and qty\_or\_amount equals “amount” and self.is\_internal\_supplier).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”) → qty\_or\_amount equals “amount” → self.is\_internal\_supplier.
    - Return no value.
- If (args at “source\_dt” differs from “Pick List Item” and args at “target\_dt” does not belong to list(“Quotation Item”, “Supplier Quotation Item”, “Packed Item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args at “source\_dt” differs from “Pick List Item” → args at “target\_dt” does not belong to list(“Quotation Item”, “Supplier Quotation Item”, “Packed Item”).
  - If args.get(“target\_dt”) equals “Material Request Item”.
    - Set action\_msg from translated “To allow over ordering, update "Over Order Allowance" in Buying Settings.”.
  - Otherwise.
    - If qty\_or\_amount equals “qty”.
      - Set action\_msg from translated “To allow over receipt / delivery, update "Over Receipt/Delivery Allowance" in Stock Settings or the Item.”.
    - Otherwise.
      - Set action\_msg from translated “To allow over billing, update "Over Billing Allowance" in Accounts Settings or the Item.”.
- Otherwise.
  - Set action\_msg from no value.
- Call the validation error handler Platform.throw((translated “This document is over limit by {0} {1} for item {4}. Are you making another {3} against the same {2}?”.format(Platform.bold(translated nested operand in the contract.title()), P ….
  - Value choice on action\_msg — true gives (text in the contract + action\_msg), false gives empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0391.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L601)

<a id="op-27bd97ce080125"></a>
### Status Updater.warn about bypassing with role

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_warn_about_bypassing_with_role`

**Inputs** self, item, qty\_or\_amount, role.

**State and service calls** msgprint with msg.format(translated item at “target\_ref\_field”.title(), Platform.bold(item at “reduce\_by”), Platform.bold(item.get(“item\_code”)), role).

**Local steps**

- If qty\_or\_amount equals “qty”.
  - Set msg from translated “Over Receipt/Delivery of {0} {1} ignored for item {2} because you have {3} role.”.
- Otherwise.
  - Set msg from translated “Overbilling of {0} {1} ignored for item {2} because you have {3} role.”.
- Evaluate Platform.msgprint(msg.format(translated item at “target\_ref\_field”.title(), Platform.bold(item at “reduce\_by”), Platform.bold(item.get(“item\_code”)), role), indicator = “orange”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0391.json#L802) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L613)

<a id="op-26cf55ad3fada8"></a>
### Status Updater.update qty

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_quantity`

**Inputs** self, update\_modified = true.

**Local steps**

- For each args in self.status\_updater.
  - If self.docstatus equals 1.
    - Set args at “cond” from (“ or parent=%s” modulo or format Platform.db.escape(self.name)).
  - Otherwise.
    - Set args at “cond” from (“ and parent!=%s” modulo or format Platform.db.escape(self.name)).
  - Evaluate self.\_update\_children(args, update\_modified).
  - If (“percent\_join\_field” belongs to args or “percent\_join\_field\_parent” belongs to args).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “percent\_join\_field” belongs to args → “percent\_join\_field\_parent” belongs to args.
    - Evaluate self.\_update\_percent\_field\_in\_targets(args, update\_modified).
- Bind dependencies refresh\_blanket\_orders\_of\_fulfilled\_rows.
- Evaluate refresh\_blanket\_orders\_of\_fulfilled\_rows(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update children](operations-022.md#op-07d922467e3515), [update percent field in targets](operations-022.md#op-4c70b75ae07b02).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L611)

<a id="op-07d922467e3515"></a>
### Status Updater.update children

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_children`

**Inputs** self, args, update\_modified.

**Record and data access** execute query text (SELECT).format(expanded names args).

**State and service calls** execute query text (UPDATE).format(target\_value = target\_value, expanded names args).

**Local steps**

- For each d in self.get\_all\_children().
  - If d.doctype differs from args at “source\_dt”.
    - Continue with the next iteration or loop test.
  - Evaluate self.\_update\_modified(args, update\_modified).
  - Set args at “detail\_id” from d.get(args at “join\_field”).
  - Set args at “second\_source\_condition” from empty text.
  - If (args.get(“second\_source\_dt”) and args.get(“second\_source\_field”) and args.get(“second\_join\_field”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“second\_source\_dt”) → args.get(“second\_source\_field”) → args.get(“second\_join\_field”).
    - If not args.get(“second\_source\_extra\_cond”).
      - Set args at “second\_source\_extra\_cond” from empty text.
    - Set args at “second\_source\_condition” from Platform.db.sql(query text (SELECT).format(expanded names args), mapping(“detail\_id” → args at “detail\_id”)) at 0 at 0.
  - If args at “detail\_id”.
    - If not args.get(“extra\_cond”).
      - Set args at “extra\_cond” from empty text.
    - Set args at “source\_dt\_value” from (Platform.db.sql(query text (SELECT).format(expanded names args), mapping(“detail\_id” → args at “detail\_id”)) at 0 at 0 or 0.0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.sql(query text (SELECT).format(expanded names args), mapping(“detail\_id” → args at “detail\_id”)) at 0 at 0 → 0.0.
    - If args at “second\_source\_condition”.
      - Update args at “source\_dt\_value” using + flt(args at “second\_source\_condition”).
    - Set round\_total from args.get(“round\_to\_target\_precision”).
    - If callable(round\_total).
      - Set round\_total from round\_total(d).
    - If round\_total.
      - Set args at “source\_dt\_value” from flt(args at “source\_dt\_value”, Platform.get\_precision(args at “target\_dt”, args at “target\_field”)).
    - Set target\_value from args at “source\_dt\_value”.
    - If args.get(“target\_conversion\_factor”).
      - Set target\_value from formatted text {target\_value} / {args at “target\_conversion\_factor”}.
    - Evaluate Platform.db.sql(query text (UPDATE).format(target\_value = target\_value, expanded names args), mapping(“detail\_id” → args at “detail\_id”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update modified](operations-023.md#op-3291f6e79ff4e2).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L606)

<a id="op-600af54caf6ec0"></a>
### Status Updater.calculate target parent percentage

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_calculate_target_parent_percentage`

**Inputs** name, target\_parent\_dt, target\_dt, target\_ref\_field, target\_field.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read target\_dt via get\_all.

**Explicit results** percentage.

**Local steps**

- Set child\_records from Platform.get\_all(target\_dt, filters = mapping(“parent” → name, “parenttype” → target\_parent\_dt), fields = list(target\_ref\_field, target\_field)).
- Set ref\_key from target\_ref\_field.get(“as”) when isinstance(target\_ref\_field, dict), otherwise target\_ref\_field.
  - Value choice on isinstance(target\_ref\_field, dict) — true gives target\_ref\_field.get(“as”), false gives target\_ref\_field.
- Set sum\_ref from sum(generator of abs(record at ref\_key) for record drawn from child\_records).
  - Draw record from child\_records.
- If sum\_ref &gt; 0.
  - Set percentage from round(((sum(generator of min(nested operand in the contract(nested operand in the contract), nested operand in the contract(nested operand in the contract)) for record drawn from child\_records) ÷ sum\_ref) × 100), 6).
    - Draw record from child\_records.
- Otherwise.
  - Set percentage from 0.
- Return percentage.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L596)

<a id="op-6220aca43095ad"></a>
### Status Updater.snap full percentage

`operation_enterprise_binding_enterprise_controllers_status_updater_statusupdater_snap_full_percentage`

**Inputs** percentage.

**Wrappers, in declaration order** staticmethod.

**Explicit results** 100 when flt(percentage) ≥ COMPLETE\_PERCENTAGE, otherwise percentage.

**Local steps**

- Return 100 when flt(percentage) ≥ COMPLETE\_PERCENTAGE, otherwise percentage.
  - Value choice on flt(percentage) ≥ COMPLETE\_PERCENTAGE — true gives 100, false gives percentage.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L352)

<a id="op-47ba0f8a8ae35b"></a>
### Status Updater.determine status

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_determine_status`

**Inputs** percentage, keyword.

**Wrappers, in declaration order** staticmethod.

**Explicit results** formatted text Not {keyword} · formatted text Fully {keyword} · formatted text Partly {keyword}.

**Local steps**

- If percentage &lt; 0.001.
  - Return formatted text Not {keyword}.
- Otherwise.
  - If percentage ≥ COMPLETE\_PERCENTAGE.
    - Return formatted text Fully {keyword}.
  - Otherwise.
    - Return formatted text Partly {keyword}.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L598)

<a id="op-4c70b75ae07b02"></a>
### Status Updater.update percent field in targets

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_percent_field_in_targets`

**Inputs** self, args, update\_modified = true.

**Local steps**

- If args.get(“percent\_join\_field\_parent”).
  - If name bound to self.get(args at “percent\_join\_field\_parent”).
    - Set args at “name” from name.
    - Evaluate self.\_update\_percent\_field(args, update\_modified).
- Otherwise.
  - Set distinct\_transactions from set(generator of d.get(args at “percent\_join\_field”) for d drawn from self.get\_all\_children(args at “source\_dt”)).
    - Draw d from self.get\_all\_children(args at “source\_dt”).
  - For each name in distinct\_transactions.
    - If name.
      - Set args at “name” from name.
      - Evaluate self.\_update\_percent\_field(args, update\_modified).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update percent field](operations-022.md#op-badaba547af69f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L609)

<a id="op-badaba547af69f"></a>
### Status Updater.update percent field

`operation_enterprise_controllers_status_updater_business_behavior_status_updater_update_percent_field`

**Inputs** self, args, update\_modified = true.

**State and service calls** call db\_set on target.

**Local steps**

- Set update\_data from mapping().
- If args.get(“target\_parent\_field”).
  - Set update\_data at args.get(“target\_parent\_field”) from self.\_calculate\_target\_parent\_percentage(args at “name”, args at “target\_parent\_dt”, args at “target\_dt”, args at “target\_ref\_field”, …).
  - Set update\_data at args.get(“target\_parent\_field”) from self.snap\_full\_percentage(update\_data at args.get(“target\_parent\_field”)).
  - If args.get(“status\_field”).
    - Set update\_data at args.get(“status\_field”) from self.\_determine\_status(update\_data at args.get(“target\_parent\_field”), args at “keyword”).
- If update\_data.
  - Set target from Platform.get\_lazy\_doc(args at “target\_parent\_dt”, args at “name”).
  - Evaluate target.update(update\_data).
  - Set status from target.get\_status().
  - If status.get(“status”).
    - Evaluate update\_data.update(status).
  - Evaluate target.db\_set(update\_data, update\_modified = update\_modified, notify = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate target parent percentage](operations-022.md#op-600af54caf6ec0), [snap full percentage](operations-022.md#op-6220aca43095ad), [determine status](operations-022.md#op-47ba0f8a8ae35b).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L608)
