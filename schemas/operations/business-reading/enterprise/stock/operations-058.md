# Inventory and warehouses · operations 58

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Serial and batch bundle

[Record definition](../../../../data/record-types/serial_and_batch_bundle.json)

<a id="op-7e277dc79c3ffc"></a>
### Get batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_batch`

**Inputs** item\_code.

**Explicit results** make\_batch(Platform.\_dict(mapping(“item” → item\_code))).

**Local steps**

- Bind dependencies make\_batch.
- Return make\_batch(Platform.\_dict(mapping(“item” → item\_code))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0809.json#L7307) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L510)

<a id="op-067e1bf1df547c"></a>
### Get type of transaction

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_type_of_transaction`

**Inputs** parent\_doc, child\_row.

**Explicit results** type\_of\_transaction.

**Local steps**

- Set type\_of\_transaction from child\_row.get(“type\_of\_transaction”).
- If parent\_doc.get(“doctype”) equals “Stock Entry”.
  - Set type\_of\_transaction from “Outward” when child\_row.s\_warehouse, otherwise “Inward”.
    - Value choice on child\_row.s\_warehouse — true gives “Outward”, false gives “Inward”.
- If not type\_of\_transaction.
  - Set type\_of\_transaction from “Outward”.
  - If parent\_doc.get(“doctype”) belongs to list(“Purchase Receipt”, “Purchase Invoice”).
    - Set type\_of\_transaction from “Inward”.
- If parent\_doc.get(“doctype”) equals “Subcontracting Receipt”.
  - Set type\_of\_transaction from “Outward”.
  - If child\_row.get(“doctype”) equals “Subcontracting Receipt Item”.
    - Set type\_of\_transaction from “Inward”.
- Otherwise.
  - If parent\_doc.get(“doctype”) equals “Stock Reconciliation”.
    - Set type\_of\_transaction from “Inward”.
- If (parent\_doc.get(“is\_return”) and parent\_doc.get(“doctype”) differs from “Stock Entry”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_doc.get(“is\_return”) → parent\_doc.get(“doctype”) differs from “Stock Entry”.
  - Set type\_of\_transaction from “Inward”.
  - If (parent\_doc.get(“doctype”) belongs to list(“Purchase Receipt”, “Purchase Invoice”) or child\_row.get(“doctype”) equals “Subcontracting Receipt Item”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_doc.get(“doctype”) belongs to list(“Purchase Receipt”, “Purchase Invoice”) → child\_row.get(“doctype”) equals “Subcontracting Receipt Item”.
    - Set type\_of\_transaction from “Outward”.
- Return type\_of\_transaction.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L894) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L540)

<a id="op-8b2ad63d2f98bb"></a>
### Update serial batch no ledgers

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_update_serial_batch_number_ledgers`

**Inputs** bundle, entries, child\_row, parent\_doc, warehouse = no value.

**Declared result** object.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call save on doc · msgprint with translated “Serial and Batch Bundle updated”.

**Explicit results** doc.

**Local steps**

- Evaluate Platform.has\_permission(“Serial and Batch Bundle”, “write”, throw = true).
- Set doc from Platform.get\_doc(“Serial and Batch Bundle”, bundle).
- If doc.docstatus equals 1.
  - Evaluate doc.throw\_error\_message(translated “Serial and Batch Bundle {0} is submitted and its entries cannot be modified.”.format(Platform.bold(bundle))).
- Set doc.voucher\_detail\_no from child\_row.name.
- Set doc.posting\_datetime from combine\_datetime((parent\_doc.get(“posting\_date”) or today()), (parent\_doc.get(“posting\_time”) or nowtime())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_doc.get(“posting\_date”) → today().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_doc.get(“posting\_time”) → nowtime().
- Set doc.warehouse from (warehouse or doc.warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → doc.warehouse.
- Evaluate doc.set(“entries”, list()).
- For each d in entries.
  - Evaluate doc.append(“entries”, mapping(“qty” → ((flt(nested operand in the contract.get(“qty”)) or 1.0) × 1 when doc.type\_of\_transaction equals “Inward”, otherwise negative 1), “warehouse” → (warehouse or d.get(“wa ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.get(“qty”)) → 1.0.
    - Value choice on doc.type\_of\_transaction equals “Inward” — true gives 1, false gives negative 1.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → d.get(“warehouse”).
- Evaluate doc.save(ignore\_permissions = true).
- Evaluate Platform.msgprint(translated “Serial and Batch Bundle updated”, alert = true).
- Return doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Serial and Batch Bundle”, “write”, throw = true) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L654) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L622)

<a id="op-5b3a420d0d7f80"></a>
### Get serial and batch ledger

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_and_batch_ledger`

**Inputs** remaining named values kwargs.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set kwargs from Platform.\_dict(kwargs).
- Set sle\_table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set serial\_batch\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.serial\_and\_batch\_bundle equals nested operand in the contract.parent).select(serial\_batch\_table.serial\_no, s ….
- If kwargs.serial\_nos.
  - Set query from query.where(serial\_batch\_table.serial\_no.isin(kwargs.serial\_nos)).
- If kwargs.batch\_nos.
  - Set query from query.where(serial\_batch\_table.batch\_no.isin(kwargs.batch\_nos)).
- If kwargs.fetch\_incoming\_rate.
  - Set query from query.where(sle\_table.actual\_qty &gt; 0).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L1444) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L529)

<a id="op-941e8ffaed6389"></a>
### Get auto data

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_auto_data`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_serial\_nos\_from\_sre(kwargs) when kwargs.scio\_detail, otherwise get\_available\_serial\_nos(kwargs) · get\_batch\_nos\_from\_sre(kwargs) when kwargs.scio\_detail, otherwise get\_auto\_batch\_nos(kwargs).

**Local steps**

- Set kwargs from Platform.\_dict(kwargs).
- If cint(kwargs.has\_serial\_no).
  - Return get\_serial\_nos\_from\_sre(kwargs) when kwargs.scio\_detail, otherwise get\_available\_serial\_nos(kwargs).
    - Value choice on kwargs.scio\_detail — true gives get\_serial\_nos\_from\_sre(kwargs), false gives get\_available\_serial\_nos(kwargs).
- Otherwise.
  - If cint(kwargs.has\_batch\_no).
    - Return get\_batch\_nos\_from\_sre(kwargs) when kwargs.scio\_detail, otherwise get\_auto\_batch\_nos(kwargs).
      - Value choice on kwargs.scio\_detail — true gives get\_batch\_nos\_from\_sre(kwargs), false gives get\_auto\_batch\_nos(kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L2037) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L506)

<a id="op-971adf6126de04"></a>
### Get available batches qty

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_available_batches_quantity`

**Inputs** available\_batches.

**Explicit results** available\_batches\_qty.

**Local steps**

- Set available\_batches\_qty from defaultdict(float).
- For each batch in available\_batches.
  - Update available\_batches\_qty at batch.batch\_no using + batch.qty.
- Return available\_batches\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L2272) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L508)

<a id="op-db1667ddece944"></a>
### Get available serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_available_serial_numbers`

**Inputs** kwargs.

**Explicit results** list() · get\_serial\_nos\_based\_on\_filters(filters, fields, order\_by, kwargs).

**Local steps**

- Set fields from list(“name as serial\_no”, “warehouse”).
- If kwargs.has\_batch\_no.
  - Evaluate fields.append(“batch\_no”).
- Set order\_by from “creation”.
- If kwargs.based\_on equals “LIFO”.
  - Set order\_by from “creation”.
- Otherwise.
  - If kwargs.based\_on equals “Expiry”.
    - Set order\_by from “amc\_expiry\_date”.
- If (not kwargs.get(“posting\_datetime”) and kwargs.get(“posting\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kwargs.get(“posting\_datetime”) → kwargs.get(“posting\_date”).
  - Set kwargs at “posting\_datetime” from combine\_datetime(kwargs.get(“posting\_date”), kwargs.get(“posting\_time”)).
- Set filters from mapping(“item\_code” → kwargs.item\_code).
- If not kwargs.get(“ignore\_warehouse”).
  - Set filters at “warehouse” from tuple(“is”, “set”).
  - If kwargs.warehouse.
    - Set filters at “warehouse” from kwargs.warehouse.
- Set reserved\_entries from list() when kwargs.get(“ignore\_reserved\_stock”), otherwise get\_reserved\_serial\_nos\_for\_sre(kwargs).
  - Value choice on kwargs.get(“ignore\_reserved\_stock”) — true gives list(), false gives get\_reserved\_serial\_nos\_for\_sre(kwargs).
- Set ignore\_serial\_nos from list().
- If reserved\_entries.
  - If (kwargs.get(“sabb\_voucher\_type”) belongs to tuple(“Delivery Note”, “Sales Invoice”) and kwargs.get(“against\_sales\_order”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.get(“sabb\_voucher\_type”) belongs to tuple(“Delivery Note”, “Sales Invoice”) → kwargs.get(“against\_sales\_order”).
    - Set reserved\_voucher\_details from list(kwargs.get(“against\_sales\_order”)).
  - Otherwise.
    - Set reserved\_voucher\_details from get\_reserved\_voucher\_details(kwargs).
  - If reserved\_serial\_nos bound to get\_reserved\_serial\_nos\_for\_voucher(kwargs, reserved\_entries, reserved\_voucher\_details).
    - Set ignore from set((kwargs.get(“ignore\_serial\_nos”) or list())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“ignore\_serial\_nos”) → list().
    - Set reserved\_serial\_nos from list of sn for sn drawn from reserved\_serial\_nos where sn does not belong to ignore.
      - Draw sn from reserved\_serial\_nos, keep a combination only if (sn does not belong to ignore).
    - If (not reserved\_serial\_nos or not set\_batch\_filter(filters, kwargs)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not reserved\_serial\_nos → not set\_batch\_filter(filters, kwargs).
      - Return list().
    - Set filters at “name” from tuple(“in”, reserved\_serial\_nos).
    - Return get\_serial\_nos\_based\_on\_filters(filters, fields, order\_by, kwargs).
  - Otherwise.
    - If ignore\_reserved\_serial\_nos bound to get\_other\_doc\_reserved\_serials(kwargs, reserved\_entries, reserved\_voucher\_details).
      - Evaluate ignore\_serial\_nos.extend(ignore\_reserved\_serial\_nos).
- If reserved\_for\_pos bound to get\_reserved\_serial\_nos\_for\_pos(kwargs).
  - Evaluate ignore\_serial\_nos.extend(reserved\_for\_pos).
- If kwargs.get(“ignore\_serial\_nos”).
  - Evaluate ignore\_serial\_nos.extend(kwargs.get(“ignore\_serial\_nos”)).
- Set ignore\_serial\_nos from list(set(ignore\_serial\_nos)).
- If kwargs.get(“posting\_datetime”).
  - Set time\_based\_serial\_nos from get\_serial\_nos\_based\_on\_posting\_date(kwargs, ignore\_serial\_nos).
  - If not time\_based\_serial\_nos.
    - Return list().
  - For each sn in ignore\_serial\_nos.
    - If sn belongs to time\_based\_serial\_nos.
      - Evaluate time\_based\_serial\_nos.remove(sn).
  - Set filters at “name” from tuple(“in”, time\_based\_serial\_nos).
- Otherwise.
  - If (kwargs.get(“check\_serial\_nos”) and kwargs.get(“serial\_nos”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.get(“check\_serial\_nos”) → kwargs.get(“serial\_nos”).
    - Set ignore from set(ignore\_serial\_nos).
    - Set serial\_nos from list of sn for sn drawn from kwargs.get(“serial\_nos”) where sn does not belong to ignore.
      - Draw sn from kwargs.get(“serial\_nos”), keep a combination only if (sn does not belong to ignore).
    - If not serial\_nos.
      - Return list().
    - Set filters at “name” from tuple(“in”, serial\_nos).
  - Otherwise.
    - If ignore\_serial\_nos.
      - Set filters at “name” from tuple(“not in”, ignore\_serial\_nos).
    - Otherwise.
      - If kwargs.get(“serial\_nos”).
        - Set filters at “name” from tuple(“in”, kwargs.get(“serial\_nos”)).
- If not set\_batch\_filter(filters, kwargs).
  - Return list().
- Return get\_serial\_nos\_based\_on\_filters(filters, fields, order\_by, kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L509)

<a id="op-55dc7f5bd2e3dc"></a>
### Set batch filter

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_set_batch_filter`

**Inputs** filters, kwargs.

**Explicit results** true · false.

**Local steps**

- If not kwargs.get(“batches”).
  - Return true.
- Set batches from get\_non\_expired\_batches(kwargs.get(“batches”)).
- If not batches.
  - Return false.
- Set filters at “batch\_no” from tuple(“in”, batches).
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1096) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L593)

<a id="op-8f1409a46d8593"></a>
### Get batch expiry date column

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_get_batch_expiry_date_column`

**Inputs** serial\_no.

**Explicit results** nested operand in the contract.qb.from\_(batch).select(batch.expiry\_date).where(batch.name equals serial\_no.batch\_no).

**Local steps**

- Set batch from Platform.qb.DocType(“Batch”).
- Return nested operand in the contract.qb.from\_(batch).select(batch.expiry\_date).where(batch.name equals serial\_no.batch\_no).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1076) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L573)

<a id="op-75ed5a01b71e94"></a>
### Get serial nos based on filters

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_numbers_based_on_filters`

**Inputs** filters, fields, order\_by, kwargs.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(“Serial No”).
- Set order\_by\_column from getattr(doctype, order\_by).
- Set query from nested operand in the contract.qb.from\_(doctype).limit((cint(kwargs.qty) or 10000000)).for\_update().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(kwargs.qty) → 10000000.
- If kwargs.based\_on equals “LIFO”.
  - Set query from query.orderby(order\_by\_column, order = Platform.query\_builder.Order.desc).
- Otherwise.
  - If kwargs.based\_on equals “Expiry”.
    - Set expiry\_date from Coalesce(get\_batch\_expiry\_date\_column(doctype), doctype.amc\_expiry\_date, “9999-12-31”).
    - Set query from query.orderby(expiry\_date).orderby(doctype.creation).
  - Otherwise.
    - Set query from query.orderby(order\_by\_column).
- For each tuple(key, value) in filters.items().
  - Set column from getattr(doctype, key).
  - If isinstance(value, tuple).
    - Set operator from value at 0.
    - If operator equals “between”.
      - Set query from query.where(column.between(value at 1, value at 2)).
    - Otherwise.
      - If operator equals “in”.
        - Set query from query.where(column.isin(value at 1)).
      - Otherwise.
        - If operator equals “not in”.
          - Set query from query.where(column.notin(value at 1)).
        - Otherwise.
          - If operator equals “is”.
            - If value at 1 equals “set”.
              - Set query from query.where(column.isnotnull()).
            - Otherwise.
              - If value at 1 equals “not set”.
                - Set query from query.where(column.isnull()).
  - Otherwise.
    - Set query from query.where(column equals value).
- For each field in fields.
  - If “ as ” belongs to field.lower().
    - Set tuple(field\_name, alias) from field.split(“ as ”, 1).
    - Set query from query.select(getattr(doctype, field\_name).as\_(alias)).
  - Otherwise.
    - Set query from query.select(getattr(doctype, field)).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** selected callable from getattr(doctype, order\_by), getattr(doctype, key) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L888) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L534)

<a id="op-48b5d0cc0e542f"></a>
### Get serial nos from sre

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_numbers_from_stock_reservation_entry`

**Inputs** kwargs.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set table from Platform.qb.DocType(“Stock Reservation Entry”).
- Set child\_table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(child\_table.serial\_no, child\_table.batch\_no, child\_table.warehouse).where(((nested operand in the contract.docstatus equals 1 bitwise a ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(kwargs.qty) → 10000000.
- If kwargs.based\_on equals “LIFO”.
  - Set query from query.orderby(child\_table.creation, order = Platform.query\_builder.Order.desc).
- Otherwise.
  - Set query from query.orderby(child\_table.creation).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L5011) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L890) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L536)

<a id="op-10be6dfdb306c2"></a>
### Get non expired batches

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_non_expired_batches`

**Inputs** batches.

**Record and data access** read “Batch” via get\_all.

**Explicit results** list of d.name for d drawn from data when data, otherwise list().

**Local steps**

- Set filters from mapping().
- If isinstance(batches, list).
  - Set filters at “name” from tuple(“in”, batches).
- Otherwise.
  - Set filters at “name” from batches.
- Set data from Platform.get\_all(“Batch”, filters = filters, or\_filters = list(list(“expiry\_date”, “&gt;=”, today()), list(“expiry\_date”, “is”, “not set”)), fields = list(“name”)).
- Return list of d.name for d drawn from data when data, otherwise list().
  - Value choice on data — true gives list of d.name for d drawn from data, false gives list().
  - Draw d from data.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L5535) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L517)

<a id="op-9ee9be83df18e3"></a>
### Get serial nos based on posting date

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_numbers_based_on_posting_date`

**Inputs** kwargs, ignore\_serial\_nos.

**Explicit results** list of serial\_no for tuple(serial\_no, qty) drawn from serial\_nos.items() where (qty &gt; 0 and serial\_no does not belong to ignore\_serial\_nos).

**Local steps**

- Set serial\_nos from Counter().
- Set data from get\_stock\_ledgers\_for\_serial\_nos(kwargs).
- Set bundle\_wise\_serial\_nos from get\_bundle\_wise\_serial\_nos(data, kwargs).
- For each d in data.
  - If d.serial\_and\_batch\_bundle.
    - Set sns from bundle\_wise\_serial\_nos.get(d.serial\_and\_batch\_bundle, list()).
  - Otherwise.
    - If d.serial\_no.
      - Set sns from parse\_serial\_nos(d.serial\_no).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - If d.actual\_qty &gt; 0.
    - Evaluate serial\_nos.update(sns).
  - Otherwise.
    - Evaluate serial\_nos.subtract(sns).
- Set ignore\_serial\_nos from set(ignore\_serial\_nos).
- Return list of serial\_no for tuple(serial\_no, qty) drawn from serial\_nos.items() where (qty &gt; 0 and serial\_no does not belong to ignore\_serial\_nos).
  - Draw tuple(serial\_no, qty) from serial\_nos.items(), keep a combination only if ((qty &gt; 0 and serial\_no does not belong to ignore\_serial\_nos)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty &gt; 0 → serial\_no does not belong to ignore\_serial\_nos.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L889) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L535)

<a id="op-aad1e0f0d98f19"></a>
### Get bundle wise serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_bundle_wise_serial_numbers`

**Inputs** data, kwargs.

**Explicit results** bundle\_wise\_serial\_nos.

**Local steps**

- Set bundle\_wise\_serial\_nos from defaultdict(list).
- Set bundles from list(set of d.serial\_and\_batch\_bundle for d drawn from data where d.serial\_and\_batch\_bundle).
  - Draw d from data, keep a combination only if (d.serial\_and\_batch\_bundle).
- If not bundles.
  - Return bundle\_wise\_serial\_nos.
- Set sabe from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(sabe.serial\_no.isnotnull()).where(sabe.serial\_no differs from empty text).
- If (kwargs.get(“check\_serial\_nos”) and kwargs.get(“serial\_nos”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.get(“check\_serial\_nos”) → kwargs.get(“serial\_nos”).
  - Set query from query.where(sabe.serial\_no.isin(kwargs.get(“serial\_nos”))).
- For each d in query.run(as\_dict = true).
  - If d.parent.
    - Evaluate bundle\_wise\_serial\_nos at d.parent.append(d.serial\_no).
- Return bundle\_wise\_serial\_nos.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0810.json#L6299) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L866) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L514)

<a id="op-41e3124a5d7658"></a>
### Get reserved voucher details

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_reserved_voucher_details`

**Inputs** kwargs.

**Record and data access** read row at 0 via get\_all.

**Explicit results** reserved\_voucher\_details.

**Local steps**

- Set reserved\_voucher\_details from list().
- Set field\_mapper from mapping(“Delivery Note” → list(list(“Delivery Note Item”, “against\_sales\_order”)), “Sales Invoice” → list(list(“Sales Invoice Item”, “sales\_order”)), “Stock Entry” → list(list(“Stock Entry”, “work\_order”), ….
- If (not field\_mapper or not kwargs.get(“sabb\_voucher\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not field\_mapper → not kwargs.get(“sabb\_voucher\_no”).
  - Return reserved\_voucher\_details.
- Set voucher\_item\_filters from mapping(“name” → kwargs.get(“sabb\_voucher\_detail\_no”), “parent” → kwargs.get(“sabb\_voucher\_no”), “docstatus” → tuple(“&lt;”, 2)).
- Set voucher\_based\_filters from mapping(“Delivery Note” → voucher\_item\_filters, “Sales Invoice” → voucher\_item\_filters, “Stock Entry” → mapping(“name” → kwargs.get(“sabb\_voucher\_no”), “docstatus” → tuple(“&lt;”, 2)), “Work Order” → mapping( ….
- Set reserved\_voucher\_details from list().
- For each row in field\_mapper.
  - Evaluate reserved\_voucher\_details.extend(Platform.get\_all(row at 0, pluck = row at 1, filters = voucher\_based\_filters)).
- Return reserved\_voucher\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L528)

<a id="op-b0020d4d103500"></a>
### Get reserved serial nos for pos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_reserved_serial_numbers_for_point_of_sale`

**Inputs** kwargs.

**Explicit results** list() · list((reserved\_serial\_nos − returned\_serial\_nos)).

**Local steps**

- Set pos\_invoices from get\_unconsolidated\_pos\_invoice\_items(kwargs).
- Set serial\_nos\_by\_row from get\_pos\_serial\_nos\_by\_row(kwargs.item\_code, pos\_invoices).
- If not serial\_nos\_by\_row.
  - Return list().
- If (kwargs.get(“check\_serial\_nos”) and kwargs.get(“serial\_nos”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.get(“check\_serial\_nos”) → kwargs.get(“serial\_nos”).
  - Set serial\_nos\_by\_row from filter\_rows\_by\_serial\_nos(serial\_nos\_by\_row, kwargs.get(“serial\_nos”)).
  - Set pos\_invoices from list of row for row drawn from pos\_invoices where row.child\_docname belongs to serial\_nos\_by\_row.
    - Draw row from pos\_invoices, keep a combination only if (row.child\_docname belongs to serial\_nos\_by\_row).
- Set reserved\_serial\_nos from Counter(generator of sn for row\_serial\_nos drawn from serial\_nos\_by\_row.values(), then sn drawn from row\_serial\_nos).
  - Draw row\_serial\_nos from serial\_nos\_by\_row.values().
  - Draw sn from row\_serial\_nos.
- Set returned\_serial\_nos from Counter(get\_pos\_returned\_serial\_nos(pos\_invoices, kwargs)).
- Return list((reserved\_serial\_nos − returned\_serial\_nos)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L525)

<a id="op-5a2eef3cd3e3c4"></a>
### Get unconsolidated pos invoice items

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_get_unconsolidated_pos_invoice_items`

**Inputs** kwargs.

**Record and data access** read “POS Invoice” via get\_all.

**Explicit results** Platform.get\_all(“POS Invoice”, fields = list(“′tabPOS Invoice Item′.serial\_no”, “′tabPOS Invoice′.is\_return”, “′tabPOS Invoice Item′.name as child\_docname”, “′tabPOS Invoice′.name as parent\_docname”, …),  ….

**Local steps**

- Return Platform.get\_all(“POS Invoice”, fields = list(“′tabPOS Invoice Item′.serial\_no”, “′tabPOS Invoice′.is\_return”, “′tabPOS Invoice Item′.name as child\_docname”, “′tabPOS Invoice′.name as parent\_docname”, …),  ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1081) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L578)

<a id="op-f42e3afb1e9a60"></a>
### Get pos serial nos by row

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_get_pos_serial_nos_by_row`

**Inputs** item\_code, pos\_invoices.

**Explicit results** serial\_nos\_by\_row.

**Local steps**

- Set serial\_nos\_by\_row from defaultdict(list).
- Set rows\_by\_bundle from defaultdict(list).
- For each row in pos\_invoices.
  - If row.serial\_and\_batch\_bundle.
    - Evaluate rows\_by\_bundle at row.serial\_and\_batch\_bundle.append(row.child\_docname).
- If not rows\_by\_bundle.
  - Return serial\_nos\_by\_row.
- For each d in \_get\_serial\_batch\_ledgers(item\_code, docstatus = 1, name = list(rows\_by\_bundle)).
  - For each child\_docname in rows\_by\_bundle at d.name.
    - Evaluate serial\_nos\_by\_row at child\_docname.append(d.serial\_no).
- For each row in pos\_invoices.
  - If row.serial\_no.
    - Evaluate serial\_nos\_by\_row at row.child\_docname.extend(parse\_serial\_nos(row.serial\_no)).
- Return serial\_nos\_by\_row.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1079) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L576)

<a id="op-2b7060cfcaea25"></a>
### Filter rows by serial nos

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_filter_rows_by_serial_nos`

**Inputs** serial\_nos\_by\_row, serial\_nos.

**Explicit results** filtered\_rows.

**Local steps**

- Set serial\_nos from set(serial\_nos).
- Set filtered\_rows from mapping().
- For each tuple(child\_docname, row\_serial\_nos) in serial\_nos\_by\_row.items().
  - If matched bound to list of sn for sn drawn from row\_serial\_nos where sn belongs to serial\_nos.
    - Draw sn from row\_serial\_nos, keep a combination only if (sn belongs to serial\_nos).
    - Set filtered\_rows at child\_docname from matched.
- Return filtered\_rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1075) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L572)

<a id="op-495227e2793646"></a>
### Get pos returned serial nos

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_get_pos_returned_serial_nos`

**Inputs** pos\_invoices, kwargs.

**Explicit results** returned\_serial\_nos.

**Local steps**

- Bind dependencies get\_returned\_serial\_nos.
- Set returned\_serial\_nos from list().
- For each row in pos\_invoices.
  - Evaluate returned\_serial\_nos.extend(get\_returned\_serial\_nos(\_dict(mapping(“doctype” → “POS Invoice Item”, “name” → row.child\_docname)), \_dict(mapping(“doctype” → “POS Invoice”, “name” → row.parent\_docname)), ignore ….
- Return returned\_serial\_nos.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1078) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L575)

<a id="op-f855a1ec48146e"></a>
### Get reserved serial nos for voucher

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_reserved_serial_numbers_for_voucher`

**Inputs** kwargs, reserved\_entries, reserved\_voucher\_details.

**Explicit results** serial\_nos.

**Explicit failure paths** validation helper — translated “The Serial No {0} is reserved against the {1} {2} and cannot be used for any other transaction.”.format(bold(entry.serial\_no), entry.voucher\_type, bold(entry.voucher\_no)).

**Local steps**

- Set serial\_nos from list().
- If not kwargs.get(“pick\_reserved\_items”).
  - Return serial\_nos.
- For each entry in reserved\_entries.
  - If entry.voucher\_no belongs to reserved\_voucher\_details.
    - Evaluate serial\_nos.append(entry.serial\_no).
    - Continue with the next iteration or loop test.
  - If (kwargs.get(“serial\_nos”) and entry.serial\_no belongs to kwargs.get(“serial\_nos”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.get(“serial\_nos”) → entry.serial\_no belongs to kwargs.get(“serial\_nos”).
    - Call the validation error handler Platform.throw(translated “The Serial No {0} is reserved against the {1} {2} and cannot be used for any other transaction.”.format(bold(entry.serial\_no), entry.voucher\_type, bold(entry.voucher\_no)), title  ….
- Return serial\_nos.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0811.json#L1526) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L881) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L527)

<a id="op-946deacf3bab13"></a>
### Get other doc reserved serials

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_other_record_reserved_serials`

**Inputs** kwargs, reserved\_entries, reserved\_voucher\_details.

**Explicit results** serial\_nos.

**Local steps**

- Set serial\_nos from list().
- For each entry in reserved\_entries.
  - If entry.voucher\_no belongs to reserved\_voucher\_details.
    - Continue with the next iteration or loop test.
  - Evaluate serial\_nos.append(entry.serial\_no).
- Return serial\_nos.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0811.json#L1889) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L518)

<a id="op-18684312c4b0e1"></a>
### Get reserved serial nos for sre

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_reserved_serial_numbers_for_stock_reservation_entry`

**Inputs** kwargs.

**Declared result** list.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sb\_entry.serial\_no, sre.voucher\_no, sre.voucher\_type).where(((((nested operand in the contract bitwise and nested operand in the contra ….
- If kwargs.warehouse.
  - Set query from query.where(sre.warehouse equals kwargs.warehouse).
- If kwargs.ignore\_voucher\_nos.
  - Set query from query.where(sre.name.notin(kwargs.ignore\_voucher\_nos)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L880) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L526)

<a id="op-5e0b032f380e18"></a>
### Get serial no reservation

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_number_reservation`

**Inputs** item\_code, serial\_no, warehouse.

**Declared result** (\_dict bitwise or no value).

**Explicit results** result at 0 when result, otherwise no value.

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set result from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
- Return result at 0 when result, otherwise no value.
  - Value choice on result — true gives result at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0811.json#L2585) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L887) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L533)
