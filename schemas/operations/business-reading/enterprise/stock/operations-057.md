# Inventory and warehouses · operations 57

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Serial and batch bundle

[Record definition](../../../../data/record-types/serial_and_batch_bundle.json)

<a id="op-94cf5b2dc143fa"></a>
### Serialand Batch Bundle.get batchwise available qty

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_batchwise_available_quantity`

**Inputs** self.

**Explicit results** available\_qty.

**Local steps**

- Set batchwise\_entries from self.get\_available\_qty\_from\_sabb().
- Evaluate batchwise\_entries.extend(self.get\_available\_qty\_from\_stock\_ledger()).
- Set available\_qty from Platform.\_dict(mapping()).
- Set batchwise\_entries from sorted(batchwise\_entries, key = deferred anonymous expression).
- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- Set posting\_datetime from get\_datetime(self.posting\_datetime) when self.posting\_datetime, otherwise no value.
  - Value choice on self.posting\_datetime — true gives get\_datetime(self.posting\_datetime), false gives no value.
- For each row in batchwise\_entries.
  - If row.batch\_no belongs to available\_qty.
    - Update available\_qty at row.batch\_no using + flt(row.qty).
  - Otherwise.
    - Set available\_qty at row.batch\_no from flt(row.qty).
  - If (flt(available\_qty at row.batch\_no, precision) &lt; 0 and (not posting\_datetime or get\_datetime(row.posting\_datetime) ≥ posting\_datetime)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(available\_qty at row.batch\_no, precision) &lt; 0 → (not posting\_datetime or get\_datetime(row.posting\_datetime) ≥ posting\_datetime).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not posting\_datetime → get\_datetime(row.posting\_datetime) ≥ posting\_datetime.
    - Evaluate self.throw\_negative\_batch(row.batch\_no, available\_qty at row.batch\_no, precision, row.posting\_datetime).
- Return available\_qty.

**Methods declared on this owner** [get available qty from sabb](operations-057.md#op-a82a2d3cd1e257), [get available qty from stock ledger](operations-057.md#op-f95436b67d2293), [throw negative batch](operations-056.md#op-c40637ec7057f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L3763) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L567)

<a id="op-f95436b67d2293"></a>
### Serialand Batch Bundle.get available qty from stock ledger

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_available_quantity_from_stock_ledger`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set batches from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
  - Draw d from self.entries, keep a combination only if (d.batch\_no).
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.batch\_no, nested operand in the contract.as\_(“qty”), sle.posting\_datetime, sle.creation).where(((((nested operand in the contract b …().
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L4393) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L566)

<a id="op-a82a2d3cd1e257"></a>
### Serialand Batch Bundle.get available qty from sabb

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_available_quantity_from_stock_accounting_balance`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set batches from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
  - Draw d from self.entries, keep a combination only if (d.batch\_no).
- Set child from Platform.qb.DocType(“Serial and Batch Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(child.batch\_no, child.qty, child.posting\_datetime, child.creation).where(((((nested operand in the contract bitwise and nested operand  …().
- Set query from query.where(child.voucher\_type differs from “Pick List”).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L565)

<a id="op-79f0110121721c"></a>
### Serialand Batch Bundle.validate voucher no docstatus

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_voucher_number_record_state`

**Inputs** self.

**Record and data access** read “Delivery Note Item” via exists · read “Sales Invoice Item” via exists · read “Subcontracting Receipt Item” via exists · read self.voucher\_type via get\_value · read child\_doctype via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- If self.is\_cancelled.
  - Return no value.
- If self.voucher\_type equals “POS Invoice”.
  - Return no value.
- Set child\_doctype from (self.voucher\_type + “ Item”).
- Set mapper from mapping(“Asset Capitalization” → “Asset Capitalization Stock Item”, “Asset Repair” → “Asset Repair Consumed Item”, “Stock Entry” → “Stock Entry Detail”).get(self.voucher\_type).
- If mapper.
  - Set child\_doctype from mapper.
- If (self.voucher\_type equals “Delivery Note” and not Platform.db.exists(“Delivery Note Item”, self.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Delivery Note” → not Platform.db.exists(“Delivery Note Item”, self.voucher\_detail\_no).
  - Set child\_doctype from “Packed Item”.
- Otherwise.
  - If (self.voucher\_type equals “Sales Invoice” and not Platform.db.exists(“Sales Invoice Item”, self.voucher\_detail\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Sales Invoice” → not Platform.db.exists(“Sales Invoice Item”, self.voucher\_detail\_no).
    - Set child\_doctype from “Packed Item”.
  - Otherwise.
    - If (self.voucher\_type equals “Subcontracting Receipt” and not Platform.db.exists(“Subcontracting Receipt Item”, self.voucher\_detail\_no)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Subcontracting Receipt” → not Platform.db.exists(“Subcontracting Receipt Item”, self.voucher\_detail\_no).
      - Set child\_doctype from “Subcontracting Receipt Supplied Item”.
- If (Platform.db.get\_value(self.voucher\_type, self.voucher\_no, “docstatus”) equals 1 and self.voucher\_detail\_no and Platform.db.exists(child\_doctype, self.voucher\_detail\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_value(self.voucher\_type, self.voucher\_no, “docstatus”) equals 1 → self.voucher\_detail\_no → Platform.db.exists(child\_doctype, self.voucher\_detail\_no).
  - Set msg from formatted text The {self.voucher\_type} {bold(self.voucher\_no)}  is in submitted state, please cancel it first.
  - Call the validation error handler Platform.throw(translated msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L976) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L620)

<a id="op-354fcb9e28715e"></a>
### Serialand Batch Bundle.on trash

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_voucher\_no\_docstatus().
- Evaluate self.delink\_refernce\_from\_voucher().
- Evaluate self.delink\_reference\_from\_batch().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate voucher no docstatus](operations-057.md#op-79f0110121721c), [delink refernce from voucher](operations-056.md#op-ffc87310b2ed66), [delink reference from batch](operations-056.md#op-1a4a932c7ff860).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L938) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L582)

<a id="op-429ee1199bc442"></a>
### Serialand Batch Bundle.add serial batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_add_serial_batch`

**Inputs** self, data.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- Set tuple(serial\_nos, batch\_nos) from tuple(list(), list()).
- If isinstance(data, str).
  - Set data from parse\_json(data).
- If data.get(“csv\_file”).
  - Set tuple(serial\_nos, batch\_nos) from get\_serial\_batch\_from\_csv(self.item\_code, data.get(“csv\_file”)).
- Otherwise.
  - Set tuple(serial\_nos, batch\_nos) from get\_serial\_batch\_from\_data(self.item\_code, data).
- If (not serial\_nos and not batch\_nos).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not serial\_nos → not batch\_nos.
  - Return no value.
- If serial\_nos.
  - Evaluate self.set(“entries”, serial\_nos).
- Otherwise.
  - If batch\_nos.
    - Evaluate self.set(“entries”, batch\_nos).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L552)

<a id="op-f096f64736ae48"></a>
### Serialand Batch Bundle.delete serial batch entries

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_delete_serial_batch_entries`

**Inputs** self.

**Local steps**

- Set SBBE from Platform.qb.DocType(“Serial and Batch Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(SBBE.parent equals self.name).run().
- Evaluate self.set(“entries”, list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0808.json#L6620) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L562)

<a id="op-2f7510b72e39f6"></a>
### Download blank csv template

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_download_blank_comma_separated_values_template`

**Inputs** content.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set csv\_data from list().
- If isinstance(content, str).
  - Set content from parse\_json(content).
- Evaluate csv\_data.append(content).
- Evaluate csv\_data.append(list()).
- Evaluate csv\_data.append(list()).
- Set filename from “serial\_and\_batch\_bundle”.
- Evaluate build\_csv\_response(csv\_data, filename).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L503)

<a id="op-f5eda389d8afab"></a>
### Upload csv file

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_upload_comma_separated_values_file`

**Inputs** item\_code, file\_path.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“serial\_nos” → serial\_nos, “batch\_nos” → batch\_nos).

**Local steps**

- Evaluate Platform.has\_permission(“Item”, ptype = “select”, throw = true).
- Set tuple(serial\_nos, batch\_nos) from tuple(list(), list()).
- Set tuple(serial\_nos, batch\_nos) from get\_serial\_batch\_from\_csv(item\_code, file\_path).
- Return mapping(“serial\_nos” → serial\_nos, “batch\_nos” → batch\_nos).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “select”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L623)

<a id="op-3e2cca49ec7dfd"></a>
### Get serial batch from csv

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_batch_from_comma_separated_values`

**Inputs** item\_code, file\_path.

**State and service calls** msgprint with translated “File '{0}' not found”.format(Platform.bold(file\_path)) · msgprint with translated “{0} is not a CSV file.”.format(Platform.bold(file.file\_name)).

**Explicit results** tuple(serial\_nos, batch\_nos).

**Local steps**

- Bind dependencies read\_csv\_content.
- Set serial\_nos from list().
- Set batch\_nos from list().
- If not file\_path.
  - Return tuple(serial\_nos, batch\_nos).
- Bind dependencies find\_file\_by\_url.
- Set file from find\_file\_by\_url(file\_path).
- If not file.
  - Evaluate Platform.msgprint(translated “File '{0}' not found”.format(Platform.bold(file\_path)), alert = true, indicator = “red”, raise\_exception = FileNotFoundError).
- If file.file\_type differs from “CSV”.
  - Evaluate Platform.msgprint(translated “{0} is not a CSV file.”.format(Platform.bold(file.file\_name)), alert = true, indicator = “red”, raise\_exception = Platform.ValidationError).
- Set csv\_data from read\_csv\_content(file.get\_content()).
- Set tuple(serial\_nos, batch\_nos) from parse\_csv\_file\_to\_get\_serial\_batch(csv\_data).
- If serial\_nos.
  - Evaluate make\_serial\_nos(item\_code, serial\_nos).
- If batch\_nos.
  - Evaluate make\_batch\_nos(item\_code, batch\_nos).
- Return tuple(serial\_nos, batch\_nos).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L530)

<a id="op-e7af96298d29d0"></a>
### Parse csv file to get serial batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_parse_comma_separated_values_file_to_get_serial_batch`

**Inputs** reader.

**Explicit results** tuple(serial\_nos, batch\_nos).

**Local steps**

- Set tuple(has\_serial\_no, has\_batch\_no) from tuple(false, false).
- Set serial\_nos from list().
- Set batch\_nos from list().
- For each tuple(index, row) in enumerate(reader).
  - If index equals 0.
    - Set has\_serial\_no from row at 0 equals “Serial No”.
    - Set has\_batch\_no from row at 0 equals “Batch No”.
    - If (not has\_batch\_no and len(row) &gt; 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not has\_batch\_no → len(row) &gt; 1.
      - Set has\_batch\_no from row at 1 equals “Batch No”.
    - Continue with the next iteration or loop test.
  - If not row at 0.
    - Continue with the next iteration or loop test.
  - If (has\_serial\_no or (has\_serial\_no and has\_batch\_no)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_serial\_no → (has\_serial\_no and has\_batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_serial\_no → has\_batch\_no.
    - Set \_dict from mapping(“serial\_no” → row at 0.strip(), “qty” → 1).
    - If has\_batch\_no.
      - Evaluate \_dict.update(mapping(“batch\_no” → row at 1.strip(), “qty” → row at 2)).
      - Evaluate batch\_nos.append(mapping(“batch\_no” → row at 1.strip(), “qty” → row at 2)).
    - Evaluate serial\_nos.append(\_dict).
  - Otherwise.
    - If has\_batch\_no.
      - Evaluate batch\_nos.append(mapping(“batch\_no” → row at 0.strip(), “qty” → row at 1)).
- Return tuple(serial\_nos, batch\_nos).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0809.json#L977) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L550)

<a id="op-621962d515b781"></a>
### Get serial batch from data

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_batch_from_data`

**Inputs** item\_code, kwargs.

**Explicit results** serial\_nos · tuple(serial\_nos, batch\_nos).

**Local steps**

- Set serial\_nos from list().
- Set batch\_nos from list().
- If kwargs.get(“serial\_nos”).
  - Set data from parse\_serial\_nos(kwargs.get(“serial\_nos”)).
  - For each serial\_no in data.
    - If not serial\_no.
      - Continue with the next iteration or loop test.
    - Evaluate serial\_nos.append(mapping(“serial\_no” → serial\_no, “qty” → 1)).
  - Evaluate make\_serial\_nos(item\_code, serial\_nos).
- If kwargs.get(“\_has\_serial\_nos”).
  - Return serial\_nos.
- Return tuple(serial\_nos, batch\_nos).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0809.json#L1692) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L885) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L531)

<a id="op-92d7dbc52f8fdd"></a>
### Create serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_create_serial_numbers`

**Inputs** item\_code, serial\_nos.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** serial\_nos.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, ptype = “select”, throw = true).
- Set serial\_nos from get\_serial\_batch\_from\_data(item\_code, mapping(“serial\_nos” → serial\_nos, “\_has\_serial\_nos” → true)).
- Return serial\_nos.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, ptype = “select”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L502)

<a id="op-018b83e02955d8"></a>
### Make serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_make_serial_numbers`

**Inputs** item\_code, serial\_nos.

**Record and data access** read “Item” via get\_cached\_value · read “Serial No” via get\_all.

**State and service calls** request bulk\_insert on “Serial No” · msgprint with translated “Serial Nos are created successfully”.

**Explicit results** no value.

**Local steps**

- Set item from Platform.get\_cached\_value(“Item”, item\_code, list(“description”, “item\_code”, “item\_name”, “warranty\_period”), as\_dict = 1).
- Set serial\_nos from list of d.get(“serial\_no”).strip() for d drawn from serial\_nos where d.get(“serial\_no”).
  - Draw d from serial\_nos, keep a combination only if (d.get(“serial\_no”)).
- Set existing\_serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, serial\_nos))).
- Set existing\_serial\_nos from list of d.get(“name”) for d drawn from existing\_serial\_nos where d.get(“name”).
  - Draw d from existing\_serial\_nos, keep a combination only if (d.get(“name”)).
- Set serial\_nos from list((set(serial\_nos) − set(existing\_serial\_nos))).
- If not serial\_nos.
  - Return no value.
- Evaluate Platform.has\_permission(“Serial and Batch Bundle”, “create”, throw = true).
- Set serial\_nos\_details from list().
- Set user from Platform.session.user.
- For each serial\_no in serial\_nos.
  - Evaluate serial\_nos\_details.append(tuple(serial\_no, serial\_no, now(), now(), …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.warranty\_period → 0.
- Set fields from list(“name”, “serial\_no”, “creation”, “modified”, …).
- Evaluate Platform.db.bulk\_insert(“Serial No”, fields = fields, values = set(serial\_nos\_details)).
- Evaluate Platform.msgprint(translated “Serial Nos are created successfully”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“description”, “item\_code”, “item\_name”, “warranty\_period”), as\_dict = 1) · effective access from Platform.has\_permission(“Serial and Batch Bundle”, “create”, throw = true) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L548)

<a id="op-cbed6f5388c87b"></a>
### Make batch nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_make_batch_numbers`

**Inputs** item\_code, batch\_nos.

**Record and data access** read “Item” via get\_cached\_value · read “Batch” via get\_all · read “Batch” via exists.

**State and service calls** request bulk\_insert on “Batch” · msgprint with translated “Batch Nos are created successfully”.

**Explicit results** no value.

**Local steps**

- Set item from Platform.get\_cached\_value(“Item”, item\_code, list(“description”, “item\_code”), as\_dict = 1).
- Set batch\_nos from list of d.get(“batch\_no”) for d drawn from batch\_nos where d.get(“batch\_no”).
  - Draw d from batch\_nos, keep a combination only if (d.get(“batch\_no”)).
- Set existing\_batches from Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, batch\_nos))).
- Set existing\_batches from list of d.get(“name”) for d drawn from existing\_batches where d.get(“name”).
  - Draw d from existing\_batches, keep a combination only if (d.get(“name”)).
- Set batch\_nos from list((set(batch\_nos) − set(existing\_batches))).
- If not batch\_nos.
  - Return no value.
- Evaluate Platform.has\_permission(“Serial and Batch Bundle”, “create”, throw = true).
- Set batch\_nos\_details from list().
- Set user from Platform.session.user.
- For each batch\_no in batch\_nos.
  - If Platform.db.exists(“Batch”, batch\_no).
    - Continue with the next iteration or loop test.
  - Evaluate batch\_nos\_details.append(tuple(batch\_no, batch\_no, now(), now(), …)).
- Set fields from list(“name”, “batch\_id”, “creation”, “modified”, …).
- Evaluate Platform.db.bulk\_insert(“Batch”, fields = fields, values = set(batch\_nos\_details)).
- Evaluate Platform.msgprint(translated “Batch Nos are created successfully”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“description”, “item\_code”), as\_dict = 1) · effective access from Platform.has\_permission(“Serial and Batch Bundle”, “create”, throw = true) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L546)

<a id="op-7263d0cbcec347"></a>
### Item query

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_item_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters, as\_dict = false.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Item” via get\_list.

**Explicit results** Platform.get\_list(“Item”, filters = item\_filters, or\_filters = mapping(“has\_serial\_no” → 1, “has\_batch\_no” → 1), fields = list(“name”, “item\_name”), as\_list = 1).

**Local steps**

- Set item\_filters from mapping(“disabled” → 0).
- If txt.
  - Set item\_filters at “name” from tuple(“like”, formatted text %{txt}%).
- Return Platform.get\_list(“Item”, filters = item\_filters, or\_filters = mapping(“has\_serial\_no” → 1, “has\_batch\_no” → 1), fields = list(“name”, “item\_name”), as\_list = 1).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L898) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L544)

<a id="op-b592e86d684d9b"></a>
### Get serial batch ledgers

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_serial_batch_ledgers`

**Inputs** item\_code = no value, docstatus = no value, voucher\_no = no value, name = no value, child\_row = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Serial and Batch Bundle” via get\_list.

**Explicit results** list() · ledgers · visible.

**Local steps**

- If isinstance(child\_row, dict).
  - Set child\_row from \_dict(child\_row).
- If not Platform.has\_permission(“Serial and Batch Bundle”, “select”).
  - Evaluate \_refuse().
- Set filters from get\_filters\_for\_bundle(item\_code = item\_code, docstatus = docstatus, voucher\_no = voucher\_no, name = name, …).
- Set parent\_filters from list().
- For each condition in filters.
  - If (condition at 0 equals “Serial and Batch Entry” and condition at 1 equals “parent”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in condition at 0 equals “Serial and Batch Entry” → condition at 1 equals “parent”.
    - Set condition from list(“Serial and Batch Bundle”, “name”, condition at 2, condition at 3).
  - Evaluate parent\_filters.append(condition).
- Set permitted from Platform.get\_list(“Serial and Batch Bundle”, filters = parent\_filters, pluck = “name”).
- If not permitted.
  - Return list().
- Set ledgers from \_get\_serial\_batch\_ledgers(name = permitted, child\_row = child\_row).
- If not get\_user\_permissions(Platform.session.user).
  - Return ledgers.
- Set visible from list().
- For each ledger in ledgers.
  - If (ledger.batch\_no and not \_is\_within\_user\_permissions(“Batch”, ledger.batch\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ledger.batch\_no → not \_is\_within\_user\_permissions(“Batch”, ledger.batch\_no).
    - Continue with the next iteration or loop test.
  - If (ledger.serial\_no and not \_is\_within\_user\_permissions(“Serial No”, ledger.serial\_no)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ledger.serial\_no → not \_is\_within\_user\_permissions(“Serial No”, ledger.serial\_no).
    - Continue with the next iteration or loop test.
  - Evaluate visible.append(ledger).
- Return visible.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Serial and Batch Bundle”, “select”), get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L886) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L532)

<a id="op-481ba2bf81857a"></a>
### Get serial batch ledgers

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_get_serial_batch_ledgers`

**Inputs** item\_code = no value, docstatus = no value, voucher\_no = no value, name = no value, child\_row = no value.

**Record and data access** read “Serial and Batch Bundle” via get\_all.

**Explicit results** Platform.get\_all(“Serial and Batch Bundle”, fields = fields, filters = filters, order\_by = “′tabSerial and Batch Entry′.′idx′”).

**Local steps**

- Set filters from get\_filters\_for\_bundle(item\_code = item\_code, docstatus = docstatus, voucher\_no = voucher\_no, name = name, …).
- Set fields from list(“′tabSerial and Batch Bundle′.′item\_code′”, “′tabSerial and Batch Entry′.′qty′”, “′tabSerial and Batch Entry′.′warehouse′”, “′tabSerial and Batch Entry′.′batch\_no′”, …).
- If not child\_row.
  - Evaluate fields.append(“′tabSerial and Batch Bundle′.′name′”).
- Return Platform.get\_all(“Serial and Batch Bundle”, fields = fields, filters = filters, order\_by = “′tabSerial and Batch Entry′.′idx′”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1080) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L577)

<a id="op-c8560cfc4ad317"></a>
### Get filters for bundle

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_filters_for_bundle`

**Inputs** item\_code = no value, docstatus = no value, voucher\_no = no value, name = no value, child\_row = no value.

**Explicit results** filters.

**Local steps**

- Set filters from list(list(“Serial and Batch Bundle”, “is\_cancelled”, “=”, 0)).
- If (child\_row and isinstance(child\_row, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in child\_row → isinstance(child\_row, str).
  - Set child\_row from parse\_json(child\_row).
- If (not name and child\_row).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not name → child\_row.
  - Set bundle from get\_reference\_serial\_and\_batch\_bundle(child\_row).
  - If bundle.
    - Set voucher\_no from no value.
    - Evaluate filters.append(list(“Serial and Batch Bundle”, “name”, “=”, bundle)).
- If item\_code.
  - Evaluate filters.append(list(“Serial and Batch Bundle”, “item\_code”, “=”, item\_code)).
- If not docstatus.
  - Set docstatus from list(0, 1).
- If isinstance(docstatus, list).
  - Evaluate filters.append(list(“Serial and Batch Bundle”, “docstatus”, “in”, docstatus)).
- Otherwise.
  - Evaluate filters.append(list(“Serial and Batch Bundle”, “docstatus”, “=”, docstatus)).
- If voucher\_no.
  - Evaluate filters.append(list(“Serial and Batch Bundle”, “voucher\_no”, “=”, voucher\_no)).
- If name.
  - If isinstance(name, list).
    - Evaluate filters.append(list(“Serial and Batch Entry”, “parent”, “in”, name)).
  - Otherwise.
    - Evaluate filters.append(list(“Serial and Batch Entry”, “parent”, “=”, name)).
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L869) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L515)

<a id="op-7af81cec15568d"></a>
### Get reference serial and batch bundle

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_get_reference_serial_and_batch_bundle`

**Inputs** child\_row.

**Record and data access** read doctype via get\_cached\_value.

**Explicit results** no value · Platform.get\_cached\_value(doctype, child\_row.get(field), bundle\_field).

**Local steps**

- If flt(child\_row.get(“rejected\_qty” when child\_row.get(“is\_rejected”), otherwise “qty”)) ≥ 0.
  - Value choice on child\_row.get(“is\_rejected”) — true gives “rejected\_qty”, false gives “qty”.
  - Return no value.
- Set doctype from child\_row.get(“doctype”).
- Set field from mapping(“Sales Invoice Item” → “sales\_invoice\_item”, “Delivery Note Item” → “dn\_detail”, “Purchase Receipt Item” → “purchase\_receipt\_item”, “Purchase Invoice Item” → “purchase\_invoice\_item”, …).get(doctype).
- If field.
  - Set from\_rejected from (child\_row.get(“is\_rejected”) or child\_row.get(“return\_qty\_from\_rejected\_warehouse”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_row.get(“is\_rejected”) → child\_row.get(“return\_qty\_from\_rejected\_warehouse”).
  - Set bundle\_field from “rejected\_serial\_and\_batch\_bundle” when from\_rejected, otherwise “serial\_and\_batch\_bundle”.
    - Value choice on from\_rejected — true gives “rejected\_serial\_and\_batch\_bundle”, false gives “serial\_and\_batch\_bundle”.
  - Return Platform.get\_cached\_value(doctype, child\_row.get(field), bundle\_field).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(doctype, child\_row.get(field), bundle\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L876) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L522)

<a id="op-5db9d02a2ad772"></a>
### Add serial batch ledgers

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_add_serial_batch_ledgers`

**Inputs** entries, child\_row, doc, warehouse = no value, do\_not\_save = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read child\_row.doctype via get\_value · read “Serial and Batch Bundle” via exists.

**Explicit results** sb\_doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “{0} does not hold a Serial and Batch Bundle”.format(child\_row.doctype).

**Local steps**

- Set child\_row from parse\_json(child\_row).
- If isinstance(entries, str).
  - Set entries from parse\_json(entries).
- Set parent\_doc from doc.
- If (parent\_doc and isinstance(parent\_doc, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_doc → isinstance(parent\_doc, str).
  - Set parent\_doc from parse\_json(parent\_doc).
- If do\_not\_save.
  - Set child\_row.doctype from cstr(child\_row.doctype).
  - Set child\_row.name from cstr(child\_row.name).
  - Set meta from Platform.get\_meta(child\_row.doctype).
  - If (not meta.istable or not meta.has\_field(“serial\_and\_batch\_bundle”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta.istable → not meta.has\_field(“serial\_and\_batch\_bundle”).
    - Call the validation error handler Platform.throw(translated “{0} does not hold a Serial and Batch Bundle”.format(child\_row.doctype), Platform.PermissionError).
  - Set fields from list(“parenttype”, “parent”, “serial\_and\_batch\_bundle”).
  - If meta.has\_field(“rejected\_serial\_and\_batch\_bundle”).
    - Evaluate fields.append(“rejected\_serial\_and\_batch\_bundle”).
  - Set row from Platform.\_dict().
  - If child\_row.name.
    - Set row from Platform.db.get\_value(child\_row.doctype, child\_row.name, fields, as\_dict = true).
  - Set row from (row or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row → Platform.\_dict().
  - Evaluate require\_permission(row.parenttype, row.parent, “write”).
  - Set bundle\_source from row.
- Otherwise.
  - Set bundle\_source from child\_row.
- Set bundle\_field from “serial\_and\_batch\_bundle”.
- If child\_row.get(“is\_rejected”).
  - Set bundle\_field from “rejected\_serial\_and\_batch\_bundle”.
- Set bundle from cstr(bundle\_source.get(bundle\_field)).
- If Platform.db.exists(“Serial and Batch Bundle”, bundle).
  - If do\_not\_save.
    - Evaluate require\_permission(“Serial and Batch Bundle”, bundle, “write”).
  - Otherwise.
    - If not Platform.has\_permission(“Serial and Batch Bundle”, “write”, doc = bundle).
      - Evaluate \_refuse().
  - Set sb\_doc from update\_serial\_batch\_no\_ledgers(bundle, entries, child\_row, parent\_doc, …).
- Otherwise.
  - Set sb\_doc from create\_serial\_batch\_no\_ledgers(entries, child\_row, parent\_doc, warehouse, do\_not\_save = do\_not\_save).
- Return sb\_doc.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Serial and Batch Bundle”, “write”, doc = bundle).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L850) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L498)

<a id="op-0d5a040235774d"></a>
### Create serial batch no ledgers

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_create_serial_batch_number_ledgers`

**Inputs** entries, child\_row, parent\_doc, warehouse = no value, do\_not\_save = false.

**Declared result** object.

**Record and data access** resolve a document from mapping(“doctype” → “Serial and Batch Bundle”, “voucher\_type” → child\_row.parenttype, “item\_code” → child\_row.item\_code, “warehouse” → warehouse, …) via get\_doc · read “Item” via get\_cached\_value.

**State and service calls** call save on doc · request set\_value on child\_row.doctype · msgprint with translated “Serial and Batch Bundle created”.

**Explicit results** doc.

**Local steps**

- Set warehouse from (warehouse or child\_row.rejected\_warehouse when child\_row.is\_rejected, otherwise child\_row.warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → child\_row.rejected\_warehouse when child\_row.is\_rejected, otherwise child\_row.warehouse.
  - Value choice on child\_row.is\_rejected — true gives child\_row.rejected\_warehouse, false gives child\_row.warehouse.
- Set type\_of\_transaction from get\_type\_of\_transaction(parent\_doc, child\_row).
- If parent\_doc.get(“doctype”) equals “Stock Entry”.
  - Set warehouse from (warehouse or child\_row.s\_warehouse or child\_row.t\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse → child\_row.s\_warehouse → child\_row.t\_warehouse.
- Set posting\_datetime from combine\_datetime((parent\_doc.get(“posting\_date”) or today()), (parent\_doc.get(“posting\_time”) or nowtime())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_doc.get(“posting\_date”) → today().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_doc.get(“posting\_time”) → nowtime().
- Set doc from Platform.get\_doc(mapping(“doctype” → “Serial and Batch Bundle”, “voucher\_type” → child\_row.parenttype, “item\_code” → child\_row.item\_code, “warehouse” → warehouse, …)).
- Set batch\_no from no value.
- If (not entries at 0.get(“batch\_no”) and entries at 0.get(“serial\_no”) and Platform.get\_cached\_value(“Item”, child\_row.item\_code, “has\_batch\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not entries at 0.get(“batch\_no”) → entries at 0.get(“serial\_no”) → Platform.get\_cached\_value(“Item”, child\_row.item\_code, “has\_batch\_no”).
  - Set batch\_no from get\_batch(child\_row.item\_code).
- For each row in entries.
  - Set row from Platform.\_dict(row).
  - Evaluate doc.append(“entries”, mapping(“qty” → ((flt(row.qty) or 1.0) × 1 when type\_of\_transaction equals “Inward”, otherwise negative 1), “warehouse” → warehouse, “batch\_no” → (row.batch\_no or batch\_no), “serial\_n ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.qty) → 1.0.
    - Value choice on type\_of\_transaction equals “Inward” — true gives 1, false gives negative 1.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.batch\_no → batch\_no.
- Evaluate doc.save().
- If do\_not\_save.
  - Evaluate Platform.db.set\_value(child\_row.doctype, child\_row.name, “serial\_and\_batch\_bundle”, doc.name).
- Evaluate Platform.msgprint(translated “Serial and Batch Bundle created”, alert = true).
- Return doc.

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Item”, child\_row.item\_code, “has\_batch\_no”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0809.json#L6017) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L853) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L501)

<a id="op-da9b76977b847b"></a>
### Combine datetime

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_combine_datetime`

**Inputs** date, time = no value.

**Explicit results** get\_combine\_datetime(date, time).

**Local steps**

- Bind dependencies get\_combine\_datetime.
- Return get\_combine\_datetime(date, time).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0809.json#L7084) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L852) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L500)

<a id="op-61cc2bfee83fd8"></a>
### Allow negative stock for batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_allow_negative_stock_for_batch`

**Inputs** batch\_no.

**Record and data access** read “Batch” via get\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** true · bool(Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock\_for\_batch”)).

**Local steps**

- If (batch\_no and Platform.db.get\_value(“Batch”, batch\_no, “allow\_negative\_stock\_for\_batch”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no → Platform.db.get\_value(“Batch”, batch\_no, “allow\_negative\_stock\_for\_batch”).
  - Return true.
- Return bool(Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock\_for\_batch”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “allow\_negative\_stock\_for\_batch”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0809.json#L7158) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L851) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L499)
