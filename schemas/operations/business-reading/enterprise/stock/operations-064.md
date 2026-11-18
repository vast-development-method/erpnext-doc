# Inventory and warehouses · operations 64

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Serial batch bundle

<a id="op-7307db9e7ddd68"></a>
### Throw negative batch validation

`operation_enterprise_stock_serial_batch_bundle_business_behavior_throw_negative_batch_validation`

**Inputs** batch\_no, qty.

**Explicit failure paths** validation helper — translated “The Batch {0} has negative batch quantity {1}. To fix this, go to the batch and click on Recalculate Batch Q …”.format(bold(get\_link\_to\_form(“Batch”, batch\_no)), bold(qty)).

**Local steps**

- Call the validation error handler Platform.throw(translated “The Batch {0} has negative batch quantity {1}. To fix this, go to the batch and click on Recalculate Batch Q …”.format(bold(get\_link\_to\_form(“Batch”, batch\_no)), bold(qty)), titl ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0930.json#L641) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L694)

<a id="op-2209c7248d507d"></a>
### Get batchwise qty

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_batchwise_quantity`

**Inputs** voucher\_type, voucher\_no.

**Record and data access** read “Serial and Batch Bundle” via get\_all · read “Serial and Batch Entry” via get\_all.

**Explicit results** no value · Platform.\_dict(mapping()) · Platform.\_dict(batches).

**Local steps**

- Set bundles from Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“voucher\_no” → voucher\_no, “voucher\_type” → voucher\_type, “docstatus” → tuple(“&gt;”, 0)), pluck = “name”).
- If not bundles.
  - Return no value.
- Set batches from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, bundles), “batch\_no” → tuple(“is”, “set”)), fields = list(“batch\_no”, mapping(“SUM” → “qty”, “as” → “qty”)), group\_by = “ ….
- If not batches.
  - Return Platform.\_dict(mapping()).
- Return Platform.\_dict(batches).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0930.json#L813) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1058) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L630)

<a id="op-dc22e0b9847886"></a>
### Get serial batch list from item

`operation_enterprise_stock_serial_batch_bundle_business_behavior_get_serial_batch_list_from_item`

**Inputs** item.

**Explicit results** tuple(serial\_list, batch\_list).

**Local steps**

- Set tuple(serial\_list, batch\_list) from tuple(list(), list()).
- If item.serial\_and\_batch\_bundle.
  - Set table from Platform.qb.DocType(“Serial and Batch Entry”).
  - Set query from nested operand in the contract.qb.from\_(table).select(table.serial\_no, table.batch\_no).where(table.parent equals item.serial\_and\_batch\_bundle).
  - Set result from query.run(as\_dict = true).
  - For each row in result.
    - If (row.serial\_no and row.serial\_no does not belong to serial\_list).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_no → row.serial\_no does not belong to serial\_list.
      - Evaluate serial\_list.append(row.serial\_no).
    - If (row.batch\_no and row.batch\_no does not belong to batch\_list).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → row.batch\_no does not belong to batch\_list.
      - Evaluate batch\_list.append(row.batch\_no).
- Otherwise.
  - Bind dependencies get\_serial\_nos.
  - Set serial\_list from get\_serial\_nos(item.serial\_no) when item.serial\_no, otherwise list().
    - Value choice on item.serial\_no — true gives get\_serial\_nos(item.serial\_no), false gives list().
  - Set batch\_list from list(item.batch\_no) when item.batch\_no, otherwise list().
    - Value choice on item.batch\_no — true gives list(item.batch\_no), false gives list().
- Return tuple(serial\_list, batch\_list).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0930.json#L1224) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1060) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L632)

## Record · Serial no

[Record definition](../../../../data/record-types/serial_no.json)

<a id="op-a2d46eb15d8fb1"></a>
### Serial No.initialize

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_serial_number_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.via\_stock\_ledger from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L3157) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1071) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L684)

<a id="op-edc4cd0388faec"></a>
### Serial No.validate

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_serial_number_validate`

**Inputs** self.

**Explicit failure paths** validation helper with SerialNoCannotCreateDirectError — translated “New Serial No cannot have Warehouse. Warehouse must be set by Stock Entry or Purchase Receipt”.

**Local steps**

- If (self.get(“\_\_islocal”) and self.warehouse and not self.via\_stock\_ledger).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“\_\_islocal”) → self.warehouse → not self.via\_stock\_ledger.
  - Call the validation error handler Platform.throw(translated “New Serial No cannot have Warehouse. Warehouse must be set by Stock Entry or Purchase Receipt”, SerialNoCannotCreateDirectError).
- Evaluate self.set\_maintenance\_status().
- Evaluate self.validate\_warehouse().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set maintenance status](operations-064.md#op-6835bf90390278), [validate warehouse](operations-064.md#op-6e1529f1ccb18a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L3257) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1074) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L687)

<a id="op-6e1529f1ccb18a"></a>
### Serial No.validate warehouse

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_serial_number_validate_warehouse`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with SerialNoCannotCannotChangeError — translated “{0} cannot be changed for Serial No.”.format(translated self.meta.get\_label(fieldname)).

**Local steps**

- If (self.get(“\_\_islocal”) or self.via\_stock\_ledger).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_\_islocal”) → self.via\_stock\_ledger.
  - Return no value.
- For each fieldname in STOCK\_MANAGED\_FIELDS.
  - If self.has\_value\_changed(fieldname).
    - Call the validation error handler Platform.throw(translated “{0} cannot be changed for Serial No.”.format(translated self.meta.get\_label(fieldname)), SerialNoCannotCannotChangeError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1075) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L688)

<a id="op-6835bf90390278"></a>
### Serial No.set maintenance status

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_serial_number_set_maintenance_status`

**Inputs** self.

**Local steps**

- If (not self.warranty\_expiry\_date and not self.amc\_expiry\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.warranty\_expiry\_date → not self.amc\_expiry\_date.
  - Set self.maintenance\_status from no value.
- If (self.warranty\_expiry\_date and getdate(self.warranty\_expiry\_date) &lt; getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.warranty\_expiry\_date → getdate(self.warranty\_expiry\_date) &lt; getdate(nowdate()).
  - Set self.maintenance\_status from “Out of Warranty”.
- If (self.amc\_expiry\_date and getdate(self.amc\_expiry\_date) &lt; getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.amc\_expiry\_date → getdate(self.amc\_expiry\_date) &lt; getdate(nowdate()).
  - Set self.maintenance\_status from “Out of AMC”.
- If (self.amc\_expiry\_date and getdate(self.amc\_expiry\_date) ≥ getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.amc\_expiry\_date → getdate(self.amc\_expiry\_date) ≥ getdate(nowdate()).
  - Set self.maintenance\_status from “Under AMC”.
- If (self.warranty\_expiry\_date and getdate(self.warranty\_expiry\_date) ≥ getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.warranty\_expiry\_date → getdate(self.warranty\_expiry\_date) ≥ getdate(nowdate()).
  - Set self.maintenance\_status from “Under Warranty”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L3738) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1073) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L686)

<a id="op-26d4616217077d"></a>
### Serial No.on trash

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_serial_number_on_trash`

**Inputs** self.

**Record and data access** execute query text (SELECT, Stock Ledger Entry).

**Explicit failure paths** validation helper — translated “Cannot delete Serial No {0}, as it is used in stock transactions”.format(self.name).

**Local steps**

- Set sl\_entries from Platform.db.sql(query text (SELECT, Stock Ledger Entry), tuple((“%%%s%%” modulo or format self.name), self.item\_code), as\_dict = true).
- Set sle\_exists from false.
- For each d in sl\_entries.
  - If self.name.upper() belongs to get\_serial\_nos(d.serial\_no).
    - Set sle\_exists from true.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If sle\_exists.
  - Call the validation error handler Platform.throw(translated “Cannot delete Serial No {0}, as it is used in stock transactions”.format(self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1072) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L685)

<a id="op-b00600c01eea96"></a>
### Get available serial nos

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_get_available_serial_numbers`

**Inputs** serial\_no\_series, qty, doc = no value.

**Declared result** list at str.

**Explicit results** serial\_nos.

**Local steps**

- Set serial\_nos from list().
- For each \_i in range(cint(qty)).
  - Evaluate serial\_nos.append(get\_new\_serial\_number(serial\_no\_series, doc)).
- Return serial\_nos.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1063) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L676)

<a id="op-19c53e0faefa9c"></a>
### Get new serial number

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_get_new_serial_number`

**Inputs** series, doc = no value.

**Record and data access** read “Serial No” via exists.

**Explicit results** sr\_no.

**Local steps**

- Set sr\_no from make\_autoname(series, “Serial No”, doc).
- If Platform.db.exists(“Serial No”, sr\_no).
  - Set sr\_no from get\_new\_serial\_number(series, doc).
- Return sr\_no.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1065) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L678)

<a id="op-86a17f2fb775fd"></a>
### Get items html

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_get_items_document_markup`

**Inputs** serial\_nos, item\_code.

**Explicit results** formatted text &lt;details&gt;&lt;summary&gt;  &lt;b&gt;{item\_code}:&lt;/b&gt; {len(serial\_nos)} Serial Numbers &lt;span class="caret"&gt;&lt;/span&gt;  &lt;/summary&gt;  &lt;div class="small"&gt;{body}&lt;/div&gt;&lt;/de.

**Local steps**

- Set body from “, ”.join(serial\_nos).
- Return formatted text &lt;details&gt;&lt;summary&gt;  &lt;b&gt;{item\_code}:&lt;/b&gt; {len(serial\_nos)} Serial Numbers &lt;span class="caret"&gt;&lt;/span&gt;  &lt;/summary&gt;  &lt;div class="small"&gt;{body}&lt;/div&gt;&lt;/de.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L4844) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1064) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L677)

<a id="op-7ad7a225f1d3e1"></a>
### Get serial nos

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_get_serial_numbers`

**Inputs** serial\_no.

**Explicit results** serial\_no · list of s.strip() for s drawn from nested operand in the contract.strip().replace(“,”, whitespace '\\n').split(whitespace '\\n') where s.strip().

**Local steps**

- If isinstance(serial\_no, list).
  - Return serial\_no.
- Return list of s.strip() for s drawn from nested operand in the contract.strip().replace(“,”, whitespace '\\n').split(whitespace '\\n') where s.strip().
  - Draw s from nested operand in the contract(nested operand in the contract).strip().replace(“,”, whitespace '\\n').split(whitespace '\\n'), keep a combination only if (s.strip()).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L4980) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1067) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L680)

<a id="op-2163e6af9b2b87"></a>
### Get serial nos from sle list

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_get_serial_numbers_from_stock_ledger_entry_list`

**Inputs** bundles.

**Explicit results** result.

**Local steps**

- Set table from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract.qb.from\_(table).select(table.parent, table.serial\_no).where(table.parent.isin(bundles)).
- Set data from query.run(as\_dict = true).
- Set result from mapping().
- For each d in data.
  - Evaluate result.setdefault(d.parent, list()).append(d.serial\_no).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L5157) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1069) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L682)

<a id="op-79e5d863d7c611"></a>
### Clean serial no string

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_clean_serial_number_string`

**Inputs** serial\_no.

**Declared result** str.

**Explicit results** empty text · whitespace '\\n'.join(serial\_no\_list).

**Local steps**

- If not serial\_no.
  - Return empty text.
- Set serial\_no\_list from get\_serial\_nos(serial\_no).
- Return whitespace '\\n'.join(serial\_no\_list).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0819.json#L5449) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1061) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L674)

<a id="op-480674d3d83e92"></a>
### Update maintenance status

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_update_maintenance_status`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Serial No) · resolve a document from “Serial No” via get\_doc.

**State and service calls** request set\_value on “Serial No”.

**Local steps**

- Set serial\_nos from Platform.db.sql(query text (SELECT, Serial No), tuple(nowdate(), nowdate())).
- For each serial\_no in serial\_nos.
  - Set doc from Platform.get\_doc(“Serial No”, serial\_no at 0).
  - Evaluate doc.set\_maintenance\_status().
  - Evaluate Platform.db.set\_value(“Serial No”, doc.name, “maintenance\_status”, doc.maintenance\_status).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1076) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L689)

<a id="op-6740414a94673e"></a>
### Auto fetch serial number

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_auto_fetch_serial_number`

**Inputs** qty, item\_code, warehouse, posting\_date = no value, batch\_nos = no value, for\_doctype = no value, exclude\_sr\_nos = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** sorted(list of d.get(“name”) for d drawn from serial\_numbers).

**Local steps**

- Evaluate require\_permission(“Warehouse”, warehouse, “select”).
- Set filters from Platform.\_dict(mapping(“item\_code” → item\_code, “warehouse” → warehouse)).
- If exclude\_sr\_nos is identical to no value.
  - Set exclude\_sr\_nos from list().
- Otherwise.
  - Set exclude\_sr\_nos from safe\_json\_loads(exclude\_sr\_nos).
  - Set exclude\_sr\_nos from get\_serial\_nos(clean\_serial\_no\_string(whitespace '\\n'.join(exclude\_sr\_nos))).
- If batch\_nos.
  - Set batch\_nos\_list from safe\_json\_loads(batch\_nos).
  - If isinstance(batch\_nos\_list, list).
    - Set filters.batch\_no from batch\_nos\_list.
  - Otherwise.
    - Set filters.batch\_no from list(batch\_nos).
- If posting\_date.
  - Set filters.expiry\_date from posting\_date.
- Set serial\_numbers from list().
- If for\_doctype equals “POS Invoice”.
  - Evaluate exclude\_sr\_nos.extend(get\_pos\_reserved\_serial\_nos(filters)).
- Set serial\_numbers from fetch\_serial\_numbers(filters, qty, do\_not\_include = exclude\_sr\_nos).
- Return sorted(list of d.get(“name”) for d drawn from serial\_numbers).
  - Draw d from serial\_numbers.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1060) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L673)

<a id="op-5d794ec77b3baa"></a>
### Get pos reserved serial nos

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_get_point_of_sale_reserved_serial_numbers`

**Inputs** filters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** reserved\_sr\_nos.

**Local steps**

- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- Evaluate Platform.has\_permission(“POS Invoice”, “read”, throw = true).
- Evaluate require\_permission(“Warehouse”, filters.get(“warehouse”), “select”).
- Set POSInvoice from Platform.qb.DocType(“POS Invoice”).
- Set POSInvoiceItem from Platform.qb.DocType(“POS Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).from\_(POSInvoiceItem).select(POSInvoice.is\_return, POSInvoiceItem.serial\_no).where(((((((nested operand in the contract bitwise and nested ope ….
- Set pos\_transacted\_sr\_nos from query.run(as\_dict = true).
- Set reserved\_sr\_nos from list().
- Set returned\_sr\_nos from list().
- For each d in pos\_transacted\_sr\_nos.
  - If d.is\_return equals 0.
    - Evaluate list of reserved\_sr\_nos.append(x) for x drawn from get\_serial\_nos(d.serial\_no).
      - Draw x from get\_serial\_nos(d.serial\_no).
  - Otherwise.
    - If d.is\_return equals 1.
      - Evaluate list of returned\_sr\_nos.append(x) for x drawn from get\_serial\_nos(d.serial\_no).
        - Draw x from get\_serial\_nos(d.serial\_no).
- For each x in returned\_sr\_nos.
  - If x belongs to reserved\_sr\_nos.
    - Evaluate reserved\_sr\_nos.remove(x).
- Return reserved\_sr\_nos.

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Invoice”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1066) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L679)

<a id="op-3ec890f72858ba"></a>
### Fetch serial numbers

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_fetch_serial_numbers`

**Inputs** filters, qty, do\_not\_include = no value.

**Explicit results** serial\_numbers.

**Local steps**

- If do\_not\_include is identical to no value.
  - Set do\_not\_include from list().
- Set batch\_nos from filters.get(“batch\_no”).
- Set expiry\_date from filters.get(“expiry\_date”).
- Set serial\_no from Platform.qb.DocType(“Serial No”).
- Set query from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty → 1.
- If do\_not\_include.
  - Set query from query.where(serial\_no.name.notin(do\_not\_include)).
- If batch\_nos.
  - Set query from query.where(serial\_no.batch\_no.isin(batch\_nos)).
- If expiry\_date.
  - Set batch from Platform.qb.DocType(“Batch”).
  - Set query from query.left\_join(batch).on(serial\_no.batch\_no equals batch.name).where(Coalesce(batch.expiry\_date, “4000-12-31”) ≥ expiry\_date).
- Set serial\_numbers from query.run(as\_dict = true).
- Return serial\_numbers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0820.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1062) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L675)

<a id="op-e572c0d051bcd1"></a>
### Get serial nos for outward

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_get_serial_numbers_for_outward`

**Inputs** kwargs.

**Explicit results** list() · list of d.serial\_no for d drawn from serial\_nos.

**Local steps**

- Bind dependencies get\_available\_serial\_nos.
- Set serial\_nos from get\_available\_serial\_nos(kwargs).
- If not serial\_nos.
  - Return list().
- Return list of d.serial\_no for d drawn from serial\_nos.
  - Draw d from serial\_nos.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0820.json#L697) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1068) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L681)

<a id="op-e36906869ce7ba"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_serial_number_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Serial No”.

**Local steps**

- Evaluate Platform.db.add\_index(“Serial No”, list(“item\_code”, “warehouse”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0820.json#L813) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1070) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L683)

## Report · Serial no and batch traceability

<a id="op-d98eef53abd372"></a>
### Execute

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set report from ReportData(filters).
- Evaluate report.validate\_filters().
- Set data from report.get\_data().
- Set tuple(has\_serial\_no, has\_batch\_no) from check\_has\_serial\_no\_in\_data(data).
- Set columns from report.get\_columns(has\_serial\_no, has\_batch\_no).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0901.json#L4726) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L282)

<a id="op-62255e915bbdd6"></a>
### Check has serial no in data

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_check_has_serial_number_in_data`

**Inputs** data.

**Explicit results** tuple(has\_serial\_no, has\_batch\_no).

**Local steps**

- Set has\_serial\_no from false.
- Set has\_batch\_no from false.
- For each row in data.
  - If row.get(“serial\_no”).
    - Set has\_serial\_no from true.
  - If row.get(“batch\_no”).
    - Set has\_batch\_no from true.
  - If (has\_serial\_no and has\_batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_serial\_no → has\_batch\_no.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return tuple(has\_serial\_no, has\_batch\_no).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0901.json#L4926) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L281)

<a id="op-8e3a481724e2d7"></a>
### Report Data.initialize

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_initialize`

**Inputs** self, filters.

**Local steps**

- Set self.filters from filters.
- Set self.doctype\_name from self.get\_doctype().
- Set self.mapped\_fg\_entries from mapping().
- Set self.forward\_trace\_path from set().
- Set self.backward\_trace\_path from set().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get doctype](operations-065.md#op-c63a53a68c3a67).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L293)

<a id="op-23b4a8942fb0f2"></a>
### Report Data.validate filters

`operation_enterprise_stock_report_serial_number_and_batch_traceability_business_behavior_report_data_validate_filters`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select at least one filter: Item Code, Batch, or Serial No.”.

**Local steps**

- If (not self.filters.item\_code and not self.filters.batches and not self.filters.serial\_nos).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.filters.item\_code → not self.filters.batches → not self.filters.serial\_nos.
  - Call the validation error handler Platform.throw(translated “Please select at least one filter: Item Code, Batch, or Serial No.”, title = translated “Missing Filters”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0901.json#L5209) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L299)
