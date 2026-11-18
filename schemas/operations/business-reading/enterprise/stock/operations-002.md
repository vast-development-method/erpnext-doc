# Inventory and warehouses · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Batch

[Record definition](../../../../data/record-types/batch.json)

<a id="op-1a19f7f160b9b8"></a>
### Batch.validate

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_validate`

**Inputs** self.

**Local steps**

- Evaluate self.item\_has\_batch\_enabled().
- Evaluate self.set\_batchwise\_valuation().
- Evaluate self.validate\_from\_to\_dates(“manufacturing\_date”, “expiry\_date”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [item has batch enabled](operations-002.md#op-29411e2f116894), [set batchwise valuation](operations-002.md#op-760dc02cc97073).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L781)

<a id="op-29411e2f116894"></a>
### Batch.item has batch enabled

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_item_has_batch_enabled`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “The selected item cannot have Batch”.

**Local steps**

- If Platform.db.get\_value(“Item”, self.item, “has\_batch\_no”) equals 0.
  - Call the validation error handler Platform.throw(translated “The selected item cannot have Batch”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L1257) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L775)

<a id="op-1fad326dce10cc"></a>
### Batch.recalculate batch qty

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_recalculate_batch_quantity`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self · msgprint with translated “Batch Qty updated to {0}”.format(batch\_qty).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set batches from get\_batch\_qty\_for\_stock(batch\_no = self.name, item\_code = self.item, for\_stock\_levels = true, consider\_negative\_batches = true, …).
- Set batch\_qty from 0.0.
- If batches.
  - For each row in batches.
    - Update batch\_qty using + row.get(“qty”).
- If self.batch\_qty differs from batch\_qty.
  - Evaluate self.db\_set(“batch\_qty”, batch\_qty).
- Evaluate Platform.msgprint(translated “Batch Qty updated to {0}”.format(batch\_qty), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L777)

<a id="op-6f1cc4f9351d9d"></a>
### Batch.get company

`operation_enterprise_binding_enterprise_stock_doctype_batch_batch_batch_get_company`

**Inputs** self.

**Record and data access** read self.reference\_doctype via get\_value.

**Explicit results** self.flags.company · company · Enterprise.get\_default\_company().

**Local steps**

- If self.flags.company.
  - Return self.flags.company.
- If (self.reference\_doctype and self.reference\_name and Platform.get\_meta(self.reference\_doctype).has\_field(“company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name → Platform.get\_meta(self.reference\_doctype).has\_field(“company”).
  - If company bound to Platform.db.get\_value(self.reference\_doctype, self.reference\_name, “company”).
    - Return company.
- Return Enterprise.get\_default\_company().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L197)

<a id="op-760dc02cc97073"></a>
### Batch.set batchwise valuation

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_set_batchwise_valuation`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_valuation\_method.
- If self.is\_new().
  - If (get\_valuation\_method(self.item, self.get\_company()) equals “Moving Average” and Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in get\_valuation\_method(self.item, self.get\_company()) equals “Moving Average” → Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).
    - Set self.use\_batchwise\_valuation from 0.
    - Return no value.
  - Set self.use\_batchwise\_valuation from 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get company](operations-002.md#op-6f1cc4f9351d9d).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L778)

<a id="op-66889fd49856f2"></a>
### Batch.before save

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_manufacturing\_date().
- Evaluate self.set\_expiry\_date().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set manufacturing date](operations-002.md#op-1d1c51105a9166), [set expiry date](operations-002.md#op-463550f699f1ad).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L773)

<a id="op-1d1c51105a9166"></a>
### Batch.set manufacturing date

`operation_enterprise_binding_enterprise_stock_doctype_batch_batch_batch_set_manufacturing_date`

**Inputs** self.

**Record and data access** read self.reference\_doctype via get\_value.

**Explicit results** no value.

**Local steps**

- If self.manufacturing\_date.
  - Return no value.
- If (self.reference\_doctype and self.reference\_name and Platform.get\_meta(self.reference\_doctype).has\_field(“posting\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name → Platform.get\_meta(self.reference\_doctype).has\_field(“posting\_date”).
  - Set self.manufacturing\_date from Platform.db.get\_value(self.reference\_doctype, self.reference\_name, “posting\_date”).
- Set self.manufacturing\_date from (self.manufacturing\_date or today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.manufacturing\_date → today().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L198)

<a id="op-463550f699f1ad"></a>
### Batch.set expiry date

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_set_expiry_date`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper.

**Local steps**

- Set tuple(has\_expiry\_date, shelf\_life\_in\_days) from Platform.db.get\_value(“Item”, self.item, list(“has\_expiry\_date”, “shelf\_life\_in\_days”)).
- If (not self.expiry\_date and has\_expiry\_date and shelf\_life\_in\_days).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.expiry\_date → has\_expiry\_date → shelf\_life\_in\_days.
  - Set self.expiry\_date from add\_days(self.manufacturing\_date, shelf\_life\_in\_days).
- If (has\_expiry\_date and not self.expiry\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_expiry\_date → not self.expiry\_date.
  - Call the validation error handler Platform.throw(msg = translated “Please set {0} for Batched Item {1}, which is used to set {2} on Submit.”.format(Platform.bold(translated “Shelf Life in Days”), get\_link\_to\_form(“Item”, self.item), Platfo ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L779)

<a id="op-d2e6acdfe46be6"></a>
### Batch.get name from naming series

`operation_enterprise_stock_record_definitions_batch_business_behavior_batch_get_name_from_naming_series`

**Inputs** self.

**Explicit results** name.

**Local steps**

- Set naming\_series\_prefix from \_get\_batch\_prefix().
- Set key from \_make\_naming\_series\_key(naming\_series\_prefix).
- Set name from make\_autoname(key, doc = self).
- Return name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L2519) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L774)

<a id="op-7e64a77ccf8755"></a>
### Get batch qty

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_batch_quantity`

**Inputs** batch\_no = no value, warehouse = no value, item\_code = no value, creation = no value, posting\_datetime = no value, posting\_date = no value, posting\_time = no value, ignore\_voucher\_nos = no value, for\_stock\_levels = false, consider\_negative\_batches = false, do\_not\_check\_future\_batches = false, ignore\_reserved\_stock = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Warehouse” via get\_list.

**Explicit results** batches · list of row for row drawn from batches where row.warehouse belongs to warehouses.

**Local steps**

- Evaluate Platform.has\_permission(“Batch”, “select”, throw = true).
- If warehouse.
  - Evaluate Enterprise.require\_user\_permission(“Warehouse”, warehouse).
- Set batches from get\_batch\_qty\_for\_stock(batch\_no = batch\_no, warehouse = warehouse, item\_code = item\_code, creation = creation, …).
- If (warehouse or not batches).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → not batches.
  - Return batches.
- Set warehouses from set(Platform.get\_list(“Warehouse”, filters = mapping(“name” → tuple(“in”, set of row.warehouse for row drawn from batches)), pluck = “name”, limit = 0)).
  - Draw row from batches.
- Return list of row for row drawn from batches where row.warehouse belongs to warehouses.
  - Draw row from batches, keep a combination only if (row.warehouse belongs to warehouses).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Batch”, “select”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L786)

<a id="op-0142f291bafd7d"></a>
### Get batches by oldest

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_batches_by_oldest`

**Inputs** item\_code, warehouse.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Batch” via get\_all.

**Explicit results** list() · batches\_dates.

**Local steps**

- Evaluate Platform.has\_permission(“Batch”, “select”, throw = true).
- Set batches from get\_batch\_qty(item\_code = item\_code, warehouse = warehouse).
- If not batches.
  - Return list().
- Set expiry\_dates from dict(Platform.get\_all(“Batch”, filters = mapping(“name” → list(“in”, set of batch.batch\_no for batch drawn from batches)), fields = list(“name”, “expiry\_date”), as\_list = true)).
  - Draw batch from batches.
- Set batches\_dates from list of list(batch, expiry\_dates.get(batch.batch\_no)) for batch drawn from batches.
  - Draw batch from batches.
- Evaluate batches\_dates.sort(key = deferred anonymous expression).
- Return batches\_dates.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Batch”, “select”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L787)

<a id="op-972bb50f6f01cf"></a>
### Split batch

`operation_enterprise_stock_record_definitions_batch_business_behavior_split_batch`

**Inputs** batch\_no, item\_code, warehouse, qty, new\_batch\_id = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Warehouse” via get\_value · resolve a document from “Stock Entry” via get\_doc.

**State and service calls** call insert on stock\_entry · call submit on stock\_entry.

**Explicit results** batch.name.

**Local steps**

- Set company from Platform.db.get\_value(“Warehouse”, warehouse, “company”).
- Set batch from make\_split\_batch(batch\_no, item\_code, new\_batch\_id, company).
- Set qty from flt(qty).
- Set from\_bundle\_id from make\_batch\_bundle(item\_code = item\_code, warehouse = warehouse, batches = Platform.\_dict(mapping(batch\_no → qty)), company = company, …).
- Set to\_bundle\_id from make\_batch\_bundle(item\_code = item\_code, warehouse = warehouse, batches = Platform.\_dict(mapping(batch.name → qty)), company = company, …).
- Set stock\_entry from Platform.get\_doc(doctype = “Stock Entry”, purpose = “Repack”, company = company, items = list(dict(item\_code = item\_code, qty = qty, s\_warehouse = warehouse, serial\_and\_batch\_bundle = from\_bundle\_id), dict ….
- Evaluate stock\_entry.set\_stock\_entry\_type().
- Evaluate stock\_entry.insert().
- Evaluate stock\_entry.submit().
- Return batch.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L793)

<a id="op-faa7a64f4a5d05"></a>
### Make split batch

`operation_enterprise_binding_enterprise_stock_doctype_batch_batch_make_split_batch`

**Inputs** batch\_no, item\_code, new\_batch\_id = no value, company = no value.

**Record and data access** read “Batch” via get\_value · resolve a document from “Batch” via get\_doc.

**State and service calls** call insert on batch.

**Explicit results** batch.insert().

**Local steps**

- Set source\_batch from Platform.db.get\_value(“Batch”, batch\_no, list(“manufacturing\_date”, “expiry\_date”, “supplier”, “use\_batchwise\_valuation”), as\_dict = true).
- Set batch from Platform.get\_doc(doctype = “Batch”, item = item\_code, batch\_id = new\_batch\_id, parent\_batch = batch\_no, …).
- Set batch.flags.company from company.
- Return batch.insert().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L199)

<a id="op-6a53250fdbfd90"></a>
### Make batch bundle

`operation_enterprise_stock_record_definitions_batch_business_behavior_make_batch_bundle`

**Inputs** item\_code, warehouse, batches, company, type\_of\_transaction, qty.

**Explicit results** SerialBatchCreation(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_datetime” → combine\_datetime(nested operand in the contract(), nested operand in the contract()), “voucher\_type” → “St …().name.

**Local steps**

- Bind dependencies nowtime, today.
- Bind dependencies combine\_datetime.
- Bind dependencies SerialBatchCreation.
- Return SerialBatchCreation(mapping(“item\_code” → item\_code, “warehouse” → warehouse, “posting\_datetime” → combine\_datetime(nested operand in the contract(), nested operand in the contract()), “voucher\_type” → “St …().name.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L4568) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L791)

<a id="op-6f7b8d673fe5a0"></a>
### Validate serial no with batch

`operation_enterprise_stock_record_definitions_batch_business_behavior_validate_serial_number_with_batch`

**Inputs** serial\_nos, item\_code.

**Record and data access** read “Serial No” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “The serial no {0} does not belong to item {1}”.format(get\_link\_to\_form(“Serial No”, serial\_nos at 0), get\_link\_to\_form(“Item”, item\_code)) · validation helper — translated “There is no batch found against the {0}: {1}”.format(message, serial\_no\_link).

**Local steps**

- If Platform.get\_cached\_value(“Serial No”, serial\_nos at 0, “item\_code”) differs from item\_code.
  - Call the validation error handler Platform.throw(translated “The serial no {0} does not belong to item {1}”.format(get\_link\_to\_form(“Serial No”, serial\_nos at 0), get\_link\_to\_form(“Item”, item\_code))).
- Set serial\_no\_link from “,”.join(generator of get\_link\_to\_form(“Serial No”, sn) for sn drawn from serial\_nos).
  - Draw sn from serial\_nos.
- Set message from “Serial Nos” when len(serial\_nos) &gt; 1, otherwise “Serial No”.
  - Value choice on len(serial\_nos) &gt; 1 — true gives “Serial Nos”, false gives “Serial No”.
- Call the validation error handler Platform.throw(translated “There is no batch found against the {0}: {1}”.format(message, serial\_no\_link)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Serial No”, serial\_nos at 0, “item\_code”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L794)

<a id="op-aad8f1657047c2"></a>
### Make batch

`operation_enterprise_stock_record_definitions_batch_business_behavior_make_batch`

**Inputs** kwargs.

**Record and data access** read “Item” via get\_value · resolve a document from kwargs via get\_doc.

**State and service calls** call insert on Platform.get\_doc(kwargs).

**Explicit results** Platform.get\_doc(kwargs).insert(ignore\_permissions = true).name.

**Local steps**

- If Platform.db.get\_value(“Item”, kwargs.item, “has\_batch\_no”).
  - Set kwargs.doctype from “Batch”.
  - Return Platform.get\_doc(kwargs).insert(ignore\_permissions = true).name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L790)

<a id="op-ce328f6dc2de9d"></a>
### Get pos reserved batch qty

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_point_of_sale_reserved_batch_quantity`

**Inputs** filters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** flt\_reserved\_batch\_qty.

**Local steps**

- Bind dependencies json.
- Evaluate Platform.has\_permission(“Batch”, “select”, throw = true).
- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- Set p from Platform.qb.DocType(“POS Invoice”).as\_(“p”).
- Set item from Platform.qb.DocType(“POS Invoice Item”).as\_(“item”).
- Set sum\_qty from Platform.query\_builder.functions.Sum(item.stock\_qty).as\_(“qty”).
- Set reserved\_batch\_qty from nested operand in the contract(nested operand in the contract).select(sum\_qty).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contrac ….run().
- Set flt\_reserved\_batch\_qty from flt(reserved\_batch\_qty at 0 at 0).
- Return flt\_reserved\_batch\_qty.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Batch”, “select”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L789)

<a id="op-ec9295af173c71"></a>
### Get available batches

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_available_batches`

**Inputs** kwargs.

**Explicit results** batchwise\_qty.

**Local steps**

- Bind dependencies combine\_datetime, get\_auto\_batch\_nos.
- If kwargs.get(“posting\_date”).
  - Set kwargs at “posting\_datetime” from combine\_datetime(kwargs.get(“posting\_date”), kwargs.get(“posting\_time”)).
- Set batchwise\_qty from OrderedDict().
- Set batches from get\_auto\_batch\_nos(kwargs).
- For each batch in batches.
  - Set key from batch.get(“batch\_no”).
  - If kwargs.get(“based\_on\_warehouse”).
    - Set key from tuple(batch.get(“batch\_no”), batch.get(“warehouse”)).
  - If key does not belong to batchwise\_qty.
    - Set batchwise\_qty at key from batch.get(“qty”).
  - Otherwise.
    - Update batchwise\_qty at key using + batch.get(“qty”).
- Return batchwise\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L6147) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L782)

<a id="op-980187359e749d"></a>
### Get batch no

`operation_enterprise_stock_record_definitions_batch_business_behavior_get_batch_number`

**Inputs** bundle\_id.

**Explicit results** batches.

**Local steps**

- Bind dependencies get\_batch\_nos.
- Set batches from defaultdict(float).
- For each tuple(batch\_id, d) in get\_batch\_nos(bundle\_id).items().
  - Update batches at batch\_id using + abs(d.get(“qty”)).
- Return batches.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L6594) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L784)

<a id="op-406bb7e6886a65"></a>
### Get data

`operation_enterprise_stock_record_definitions_batch_batch_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “batch\_no”, “transactions” → list(mapping(“label” → translated “Buy”, “items” → list(“Purchase Invoice”, “Purchase Receipt”)), mapping(“label” → translated “Sell”, “items” → list(“Sal ….

**Local steps**

- Return mapping(“fieldname” → “batch\_no”, “transactions” → list(mapping(“label” → translated “Buy”, “items” → list(“Purchase Invoice”, “Purchase Receipt”)), mapping(“label” → translated “Sell”, “items” → list(“Sal ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0708.json#L6766) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L770)

## Report · Batch item expiry status

<a id="op-ebfd5580bc98e6"></a>
### Execute

`operation_enterprise_stock_report_batch_item_expiry_status_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Evaluate validate\_filters(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L70)

<a id="op-d67123ab12b301"></a>
### Validate filters

`operation_enterprise_stock_report_batch_item_expiry_status_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “Please select the required filters” · validation helper — translated “'From Date' is required” · validation helper — translated “'To Date' is required”.

**Local steps**

- If not filters.
  - Call the validation error handler Platform.throw(translated “Please select the required filters”).
- If not filters.get(“from\_date”).
  - Call the validation error handler Platform.throw(translated “'From Date' is required”).
- If not filters.get(“to\_date”).
  - Call the validation error handler Platform.throw(translated “'To Date' is required”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0886.json#L3133) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L74)

<a id="op-d460f1e40fe0b4"></a>
### Get columns

`operation_enterprise_stock_report_batch_item_expiry_status_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list((translated “Item” + “:Link/Item:150”), (translated “Item Name” + “::150”), (translated “Batch” + “:Link/Batch:150”), (translated “Stock UOM” + “:Link/UOM:100”), …).

**Local steps**

- Return list((translated “Item” + “:Link/Item:150”), (translated “Item Name” + “::150”), (translated “Batch” + “:Link/Batch:150”), (translated “Stock UOM” + “:Link/UOM:100”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0886.json#L3361) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L72)

<a id="op-391a4c30fdf55c"></a>
### Get data

`operation_enterprise_stock_report_batch_item_expiry_status_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each batch in get\_batch\_details(filters).
  - Evaluate data.append(list(batch.item, batch.item\_name, batch.name, batch.stock\_uom, …)).
    - Value choice on batch.expiry\_date — true gives date\_diff(batch.expiry\_date, today()), false gives no value.
- Return data.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L73)
