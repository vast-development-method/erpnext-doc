# Inventory and warehouses · operations 54

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Serial and batch bundle

[Record definition](../../../../data/record-types/serial_and_batch_bundle.json)

<a id="op-87656f4855e411"></a>
### Serialand Batch Bundle.validate voucher detail no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_voucher_detail_number`

**Inputs** self.

**Record and data access** read “POS Invoice Item” via exists · read “Stock Ledger Entry” via exists · read “Packed Item” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The serial and batch bundle {0} not linked to {1} {2}”.format(bold(self.name), self.voucher\_type, bold(self.voucher\_no)).

**Local steps**

- If (self.type\_of\_transaction does not belong to list(“Inward”, “Outward”) or self.voucher\_type belongs to list(“Installation Note”, “Job Card”, “Maintenance Schedule”, “Pick List”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.type\_of\_transaction does not belong to list(“Inward”, “Outward”) → self.voucher\_type belongs to list(“Installation Note”, “Job Card”, “Maintenance Schedule”, “Pick List”).
  - Return no value.
- If self.voucher\_type equals “POS Invoice”.
  - If not Platform.db.exists(“POS Invoice Item”, self.voucher\_detail\_no).
    - Call the validation error handler Platform.throw(translated “The serial and batch bundle {0} not linked to {1} {2}”.format(bold(self.name), self.voucher\_type, bold(self.voucher\_no))).
- Otherwise.
  - If not Platform.db.exists(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → self.voucher\_detail\_no)).
    - If (self.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”) and Platform.db.exists(“Packed Item”, self.voucher\_detail\_no)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”) → Platform.db.exists(“Packed Item”, self.voucher\_detail\_no).
      - Return no value.
    - Call the validation error handler Platform.throw(translated “The serial and batch bundle {0} not linked to {1} {2}”.format(bold(self.name), self.voucher\_type, bold(self.voucher\_no))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L974) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L618)

<a id="op-2261b001214a39"></a>
### Serialand Batch Bundle.allow existing serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_allow_existing_serial_numbers`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Stock Entry” via get\_cached\_value · read “Serial and Batch Entry” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “You can't process the serial number {0} as it has already been used in the SABB {1}. {2} if you want to inwa …”.format(row.serial\_no, get\_link\_to\_form(“Serial and Batch Bundle”, row.parent), no ….

**Local steps**

- If (self.type\_of\_transaction equals “Outward” or not self.has\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.type\_of\_transaction equals “Outward” → not self.has\_serial\_no.
  - Return no value.
- If Platform.get\_single\_value(“Stock Settings”, “allow\_existing\_serial\_no”).
  - Return no value.
- If self.voucher\_type does not belong to list(“Purchase Receipt”, “Purchase Invoice”, “Stock Entry”).
  - Return no value.
- If (self.voucher\_type equals “Stock Entry” and Platform.get\_cached\_value(“Stock Entry”, self.voucher\_no, “purpose”) belongs to list(“Material Transfer”, “Send to Subcontractor”, “Material Transfer for Manufacture”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Stock Entry” → Platform.get\_cached\_value(“Stock Entry”, self.voucher\_no, “purpose”) belongs to list(“Material Transfer”, “Send to Subcontractor”, “Material Transfer for Manufacture”).
  - Return no value.
- Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
  - Draw d from self.entries, keep a combination only if (d.serial\_no).
- Set data from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“serial\_no” → tuple(“in”, serial\_nos), “docstatus” → 1, “qty” → tuple(“&lt;”, 0)), fields = list(“serial\_no”, “parent”)).
- Set note from text in the contract.
- For each row in data.
  - Call the validation error handler Platform.throw(translated “You can't process the serial number {0} as it has already been used in the SABB {1}. {2} if you want to inwa …”.format(row.serial\_no, get\_link\_to\_form(“Serial and Batch Bundle”,  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_existing\_serial\_no”), Platform.get\_cached\_value(“Stock Entry”, self.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L553)

<a id="op-fd0ceda49fce6c"></a>
### Serialand Batch Bundle.reset serial batch bundle

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_reset_serial_batch_bundle`

**Inputs** self.

**Local steps**

- If (self.is\_new() and self.amended\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.amended\_from.
  - For each field in list(“is\_cancelled”, “is\_rejected”).
    - If self.get(field).
      - Evaluate self.set(field, 0).
  - If self.voucher\_detail\_no.
    - Set self.voucher\_detail\_no from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0804.json#L2440) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L585)

<a id="op-076dccadcdaf5d"></a>
### Serialand Batch Bundle.set batch no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_batch_number`

**Inputs** self.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** no value.

**Local steps**

- If (self.has\_serial\_no and self.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → self.has\_batch\_no.
  - Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
    - Draw d from self.entries, keep a combination only if (d.serial\_no).
  - Set has\_no\_batch from any(generator of not d.batch\_no for d drawn from self.entries).
    - Draw d from self.entries.
  - If not has\_no\_batch.
    - Return no value.
  - Set serial\_no\_batch from Platform.\_dict(Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, serial\_nos)), fields = list(“name”, “batch\_no”), as\_list = true)).
  - For each row in self.entries.
    - If not row.batch\_no.
      - Set row.batch\_no from serial\_no\_batch.get(row.serial\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0804.json#L2623) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L586)

<a id="op-7cf520b07f7d56"></a>
### Serialand Batch Bundle.validate serial nos inventory

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_numbers_inventory`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.has\_serial\_no and self.type\_of\_transaction equals “Outward”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → self.type\_of\_transaction equals “Outward”.
  - Return no value.
- If self.voucher\_type equals “Stock Reconciliation”.
  - Set tuple(serial\_nos, batches) from self.get\_serial\_nos\_for\_validate().
- Otherwise.
  - Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
    - Draw d from self.entries, keep a combination only if (d.serial\_no).
- If not serial\_nos.
  - Return no value.
- Set kwargs from mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse, “check\_serial\_nos” → true, “serial\_nos” → serial\_nos, …).
- If self.voucher\_type equals “POS Invoice”.
  - Set kwargs at “ignore\_voucher\_nos” from list(self.voucher\_no).
- If self.voucher\_type equals “Stock Reconciliation”.
  - Evaluate kwargs.update(mapping(“voucher\_no” → self.voucher\_no, “posting\_datetime” → self.posting\_datetime)).
- Set available\_serial\_nos from get\_available\_serial\_nos(Platform.\_dict(kwargs)).
- Set serial\_no\_warehouse from mapping().
- For each data in available\_serial\_nos.
  - If data.serial\_no does not belong to serial\_nos.
    - Continue with the next iteration or loop test.
  - Set serial\_no\_warehouse at data.serial\_no from data.warehouse.
- For each serial\_no in serial\_nos.
  - If (not serial\_no\_warehouse.get(serial\_no) or serial\_no\_warehouse.get(serial\_no) differs from self.warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not serial\_no\_warehouse.get(serial\_no) → serial\_no\_warehouse.get(serial\_no) differs from self.warehouse.
    - Set reservation from get\_serial\_no\_reservation(self.item\_code, serial\_no, self.warehouse).
    - If reservation.
      - Evaluate self.throw\_error\_message(translated “Serial No {0} is in warehouse {1} but is reserved for {2} {3} via {4}. Please use an unreserved serial numbe …”.format(bold(serial\_no), bold(self.warehouse), reservatio ….
    - Otherwise.
      - Evaluate self.throw\_error\_message(translated “Serial No {0} is not present in the warehouse {1}.”.format(bold(serial\_no), bold(self.warehouse)), SerialNoWarehouseError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get serial nos for validate](operations-055.md#op-adbcf8f466d0f4), [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L973) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L617)

<a id="op-2625422eb92b1b"></a>
### Serialand Batch Bundle.validate serial nos duplicate

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_numbers_duplicate`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_cached\_value · read “Serial No” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Serial No {0} is already Delivered. You cannot use them again in Manufacture / Repack entry.”.format(bold(serial\_nos at 0)) · validation helper — translated “Serial Nos {0} are already Delivered. You cannot use them again in Manufacture / Repack entry.”.format(bold(“, ”.join(serial\_nos))).

**Local steps**

- If self.voucher\_type belongs to list(“POS Invoice”, “Pick List”).
  - Return no value.
- If not self.warehouse.
  - Return no value.
- If (self.voucher\_type belongs to list(“Stock Reconciliation”, “Stock Entry”) and self.docstatus differs from 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to list(“Stock Reconciliation”, “Stock Entry”) → self.docstatus differs from 1.
  - Return no value.
- If not (self.has\_serial\_no and self.type\_of\_transaction equals “Inward”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → self.type\_of\_transaction equals “Inward”.
  - Return no value.
- Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
  - Draw d from self.entries, keep a combination only if (d.serial\_no).
- Set kwargs from Platform.\_dict(mapping(“item\_code” → self.item\_code, “posting\_datetime” → self.posting\_datetime, “serial\_nos” → serial\_nos, “check\_serial\_nos” → true)).
- If self.docstatus equals 1.
  - Set kwargs at “ignore\_voucher\_detail\_no” from self.voucher\_detail\_no.
  - Set kwargs at “voucher\_no” from self.voucher\_no.
- Set available\_serial\_nos from get\_available\_serial\_nos(kwargs).
- For each data in available\_serial\_nos.
  - If data.serial\_no belongs to serial\_nos.
    - Evaluate self.throw\_error\_message(translated “Serial No {0} is already present in the warehouse {1}.”.format(bold(data.serial\_no), bold(data.warehouse)), SerialNoDuplicateError).
- If (self.voucher\_type equals “Stock Entry” and self.type\_of\_transaction equals “Inward” and Platform.get\_cached\_value(“Stock Entry”, self.voucher\_no, “purpose”) belongs to list(“Manufacture”, “Repack”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Stock Entry” → self.type\_of\_transaction equals “Inward” → Platform.get\_cached\_value(“Stock Entry”, self.voucher\_no, “purpose”) belongs to list(“Manufacture”, “Repack”).
  - Set serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, serial\_nos), “status” → “Delivered”), pluck = “name”).
  - If serial\_nos.
    - <a id="op-2625422eb92b1b-guard-50"></a>If len(serial\_nos) equals 1.
      - Call the validation error handler Platform.throw(translated “Serial No {0} is already Delivered. You cannot use them again in Manufacture / Repack entry.”.format(bold(serial\_nos at 0))).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Serial Nos {0} are already Delivered. You cannot use them again in Manufacture / Repack entry.”.format(bold(“, ”.join(serial\_nos)))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(serial\_nos) equals 1, length of serial\_nos = 1 selects the branch that calls the validation-error handler with translated “Serial No {0} is already Delivered. You cannot use them again in Manufacture / Repack entry.”.format(bold(serial\_nos at 0)). With length of serial\_nos = 2, the alternative calls the validation-error handler with translated “Serial Nos {0} are already Delivered. You cannot use them again in Manufacture / Repack entry.”.format(bold(“, ”.join(ser …. [Local guard](#op-2625422eb92b1b-guard-50)

**Methods declared on this owner** [throw error message](operations-054.md#op-2c6f3f95226244).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry”, self.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L616)

<a id="op-2c6f3f95226244"></a>
### Serialand Batch Bundle.throw error message

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_throw_error_message`

**Inputs** self, message, exception = Platform.ValidationError.

**Explicit failure paths** validation helper with exception — message.

**Local steps**

- Call the validation error handler Platform.throw(message, exception, title = translated “Error”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L596)

<a id="op-25f1bfa19f8d54"></a>
### Serialand Batch Bundle.set incoming rate

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_incoming_rate`

**Inputs** self, parent = no value, row = no value, save = false, allow\_negative\_stock = false, prev\_sle = no value.

**Explicit results** no value.

**Local steps**

- If (self.type\_of\_transaction does not belong to list(“Inward”, “Outward”) or self.voucher\_type belongs to list(“Installation Note”, “Job Card”, “Maintenance Schedule”, “Pick List”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.type\_of\_transaction does not belong to list(“Inward”, “Outward”) → self.voucher\_type belongs to list(“Installation Note”, “Job Card”, “Maintenance Schedule”, “Pick List”).
  - Return no value.
- If return\_against bound to self.get\_return\_against(parent = parent).
  - Evaluate self.set\_valuation\_rate\_for\_return\_entry(return\_against, row, save, prev\_sle = prev\_sle).
- Otherwise.
  - If self.type\_of\_transaction equals “Outward”.
    - Evaluate self.set\_incoming\_rate\_for\_outward\_transaction(row, save, allow\_negative\_stock = allow\_negative\_stock).
  - Otherwise.
    - Evaluate self.set\_incoming\_rate\_for\_inward\_transaction(row, save, prev\_sle = prev\_sle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get return against](operations-055.md#op-bcbf7e69a1d3e5), [set valuation rate for return entry](operations-054.md#op-4129a31a2cb488), [set incoming rate for outward transaction](operations-054.md#op-d4892294352b78), [set incoming rate for inward transaction](operations-055.md#op-fa1d7426b159cc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0804.json#L5272) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L944) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L588)

<a id="op-4129a31a2cb488"></a>
### Serialand Batch Bundle.set valuation rate for return entry

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_valuation_rate_for_return_entry`

**Inputs** self, return\_against, row, save = false, prev\_sle = no value.

**Record and data access** read “Batch” via get\_all.

**State and service calls** call db\_set on row.

**Local steps**

- If valuation\_details bound to self.get\_valuation\_rate\_for\_return\_entry(return\_against).
  - Bind dependencies get\_valuation\_method, is\_serial\_no\_wise\_valuation\_disabled.
  - Set skip\_rate\_update from is\_serial\_no\_wise\_valuation\_disabled(self.item\_code).
  - Set valuation\_method from get\_valuation\_method(self.item\_code, self.company).
  - Set batchwise\_avg\_rates from self.get\_batchwise\_return\_avg\_rates().
  - Set stock\_queue from list().
  - Set non\_batchwise\_batches from list().
  - If (not self.has\_serial\_no and valuation\_method belongs to tuple(“FIFO”, “LIFO”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_serial\_no → valuation\_method belongs to tuple(“FIFO”, “LIFO”).
    - Set non\_batchwise\_batches from Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, list of d.batch\_no for d drawn from self.entries where d.batch\_no), “use\_batchwise\_valuation” → 0), pluck = “name”).
      - Draw d from self.entries, keep a combination only if (d.batch\_no).
    - If (non\_batchwise\_batches and prev\_sle and prev\_sle.stock\_queue).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in non\_batchwise\_batches → prev\_sle → prev\_sle.stock\_queue.
      - Set stock\_queue from parse\_json(prev\_sle.stock\_queue).
  - For each row in self.entries.
    - If valuation\_details.
      - Evaluate self.validate\_returned\_serial\_batch\_no(return\_against, row, valuation\_details).
    - If skip\_rate\_update.
      - Continue with the next iteration or loop test.
    - If row.serial\_no.
      - Set valuation\_rate from valuation\_details at “serial\_nos”.get(row.serial\_no).
    - Otherwise.
      - Set valuation\_rate from valuation\_details at “batches”.get(row.batch\_no).
    - If (Platform.flags.through\_repost\_item\_valuation and not valuation\_rate).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.through\_repost\_item\_valuation → not valuation\_rate.
      - If row.serial\_no.
        - Set serial\_nos from sorted(list(valuation\_details at “serial\_nos”.keys())).
        - Set valuation\_rate from valuation\_details at “serial\_nos”.get(serial\_nos at (cint(row.idx) − 1)).
      - Otherwise.
        - Set batches from sorted(list(valuation\_details at “batches”.keys())).
        - Set valuation\_rate from valuation\_details at “batches”.get(batches at (cint(row.idx) − 1)).
    - If (not row.serial\_no and row.batch\_no belongs to batchwise\_avg\_rates).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.serial\_no → row.batch\_no belongs to batchwise\_avg\_rates.
      - Set valuation\_rate from batchwise\_avg\_rates at row.batch\_no.
    - Set row.incoming\_rate from flt(valuation\_rate).
    - Set row.stock\_value\_difference from (flt(row.qty) × flt(row.incoming\_rate)).
    - If (non\_batchwise\_batches and row.batch\_no belongs to non\_batchwise\_batches and row.incoming\_rate is distinct from no value).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in non\_batchwise\_batches → row.batch\_no belongs to non\_batchwise\_batches → row.incoming\_rate is distinct from no value.
      - If flt(row.qty) &gt; 0.
        - Evaluate stock\_queue.append(list(row.qty, row.incoming\_rate)).
      - Otherwise.
        - If flt(row.qty) &lt; 0.
          - Set queue\_class from LIFOValuation when valuation\_method equals “LIFO”, otherwise FIFOValuation.
            - Value choice on valuation\_method equals “LIFO” — true gives LIFOValuation, false gives FIFOValuation.
          - Set stock\_queue from queue\_class(stock\_queue).
          - Evaluate stock\_queue.remove\_stock(qty = abs(row.qty), outgoing\_rate = row.incoming\_rate, is\_return\_purchase\_entry = true).
          - Set stock\_queue from stock\_queue.state.
      - Set row.stock\_queue from json.dumps(stock\_queue).
    - If save.
      - Evaluate row.db\_set(mapping(“incoming\_rate” → row.incoming\_rate, “stock\_value\_difference” → row.stock\_value\_difference, “stock\_queue” → row.get(“stock\_queue”))).
- Otherwise.
  - If self.type\_of\_transaction equals “Inward”.
    - Evaluate self.set\_incoming\_rate\_for\_inward\_transaction(row, save, prev\_sle = prev\_sle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get valuation rate for return entry](operations-054.md#op-dae71d3b9c717f), [get batchwise return avg rates](operations-054.md#op-9fb0ee86bd0376), [validate returned serial batch no](operations-054.md#op-6d25fe3fb67440), [set incoming rate for inward transaction](operations-055.md#op-fa1d7426b159cc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L950) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L594)

<a id="op-9fb0ee86bd0376"></a>
### Serialand Batch Bundle.get batchwise return avg rates

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_batchwise_return_average_rates`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · read “Batch” via get\_all.

**Explicit results** mapping() · mapping of batch\_no → abs(flt(sn\_obj.batch\_avg\_rate.get(batch\_no))) for batch\_no drawn from batchwise\_batches where flt(sn\_obj.available\_qty.get(batch\_no)).

**Local steps**

- Bind dependencies get\_valuation\_method.
- If (self.type\_of\_transaction differs from “Outward” or self.has\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.type\_of\_transaction differs from “Outward” → self.has\_serial\_no.
  - Return mapping().
- Set batch\_nos from list of d.batch\_no for d drawn from self.entries where d.batch\_no.
  - Draw d from self.entries, keep a combination only if (d.batch\_no).
- If not batch\_nos.
  - Return mapping().
- If (get\_valuation\_method(self.item\_code, self.company) equals “Moving Average” and Platform.db.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in get\_valuation\_method(self.item\_code, self.company) equals “Moving Average” → Platform.db.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).
  - Return mapping().
- Set batchwise\_batches from Platform.get\_all(“Batch”, filters = mapping(“name” → tuple(“in”, batch\_nos), “use\_batchwise\_valuation” → 1), pluck = “name”).
- If not batchwise\_batches.
  - Return mapping().
- Set sle from self.get\_sle\_for\_outward\_transaction().
- Set sle.batch\_nos from mapping of batch\_no → sle.batch\_nos at batch\_no for batch\_no drawn from batchwise\_batches.
  - Draw batch\_no from batchwise\_batches.
- Set sle.batchwise\_valuation\_batches from batchwise\_batches.
- Set sn\_obj from BatchNoValuation(sle = sle, item\_code = self.item\_code, warehouse = self.warehouse).
- Return mapping of batch\_no → abs(flt(sn\_obj.batch\_avg\_rate.get(batch\_no))) for batch\_no drawn from batchwise\_batches where flt(sn\_obj.available\_qty.get(batch\_no)).
  - Draw batch\_no from batchwise\_batches, keep a combination only if (flt(sn\_obj.available\_qty.get(batch\_no))).

**Methods declared on this owner** [get sle for outward transaction](operations-054.md#op-89e245ee04c598).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “do\_not\_use\_batchwise\_valuation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0805.json#L1539) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L568)

<a id="op-6d25fe3fb67440"></a>
### Serialand Batch Bundle.validate returned serial batch no

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_returned_serial_batch_number`

**Inputs** self, return\_against, row, original\_inv\_details.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.through\_repost\_item\_valuation and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.through\_repost\_item\_valuation → not Platform.in\_test.
  - Return no value.
- If (row.serial\_no and row.serial\_no does not belong to original\_inv\_details at “serial\_nos”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.serial\_no → row.serial\_no does not belong to original\_inv\_details at “serial\_nos”.
  - Evaluate self.throw\_error\_message(translated “Serial No {0} is not present in the {1} {2}, hence you can't return it against the {1} {2}”.format(bold(row.serial\_no), self.voucher\_type, bold(return\_against))).
- If (row.batch\_no and row.batch\_no does not belong to original\_inv\_details at “batches”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → row.batch\_no does not belong to original\_inv\_details at “batches”.
  - Evaluate self.throw\_error\_message(translated “Batch No {0} is not present in the original {1} {2}, hence you can't return it against the {1} {2}”.format(bold(row.batch\_no), self.voucher\_type, bold(return\_against))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw error message](operations-054.md#op-2c6f3f95226244).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0805.json#L2173) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L965) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L609)

<a id="op-dae71d3b9c717f"></a>
### Serialand Batch Bundle.get valuation rate for return entry

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_valuation_rate_for_return_entry`

**Inputs** self, return\_against.

**Record and data access** read self.child\_table via get\_value · read “Serial and Batch Bundle” via get\_all.

**Explicit results** mapping() · self.get\_valuation\_rate\_for\_returned\_supplied\_item(return\_against) · self.get\_valuation\_details(bundle\_data).

**Local steps**

- Bind dependencies get\_warehouses\_for\_return.
- If not self.voucher\_detail\_no.
  - Return mapping().
- Set field from mapping(“Sales Invoice” → “sales\_invoice\_item”, “Purchase Invoice” → “purchase\_invoice\_item”, “Delivery Note” → “dn\_detail”, “Purchase Receipt” → “purchase\_receipt\_item”, …).get(self.voucher\_type).
- Set return\_against\_voucher\_detail\_no from Platform.db.get\_value(self.child\_table, self.voucher\_detail\_no, field).
- If (not return\_against\_voucher\_detail\_no and self.voucher\_type belongs to tuple(“Delivery Note”, “Sales Invoice”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not return\_against\_voucher\_detail\_no → self.voucher\_type belongs to tuple(“Delivery Note”, “Sales Invoice”).
  - Set return\_against\_voucher\_detail\_no from self.get\_return\_against\_packed\_item(field).
- If (not return\_against\_voucher\_detail\_no and self.voucher\_type equals “Subcontracting Receipt”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not return\_against\_voucher\_detail\_no → self.voucher\_type equals “Subcontracting Receipt”.
  - Return self.get\_valuation\_rate\_for\_returned\_supplied\_item(return\_against).
- Set filters from list(list(“Serial and Batch Bundle”, “voucher\_no”, “=”, return\_against), list(“Serial and Batch Entry”, “docstatus”, “=”, 1), list(“Serial and Batch Bundle”, “is\_cancelled”, “=”, 0), list(“Serial and Batch ….
- Set return\_warehouse from no value.
- If self.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”).
  - Set warehouses from get\_warehouses\_for\_return(self.voucher\_type, return\_against\_voucher\_detail\_no).
  - If self.warehouse belongs to warehouses.
    - Set return\_warehouse from self.warehouse.
    - Evaluate filters.append(list(“Serial and Batch Entry”, “warehouse”, “=”, return\_warehouse)).
- Set bundle\_data from Platform.get\_all(“Serial and Batch Bundle”, fields = list(“name”, “′tabSerial and Batch Entry′.′serial\_no′”, “′tabSerial and Batch Entry′.′batch\_no′”, “′tabSerial and Batch Entry′.′incoming\_rate′”), filter ….
- If delivered\_bundle bound to self.get\_delivered\_packed\_item\_bundle().
  - Evaluate bundle\_data.sort(key = deferred anonymous expression).
- If not bundle\_data.
  - Set bundle\_data from self.get\_legacy\_valuation\_rate\_for\_return\_entry(return\_against, return\_against\_voucher\_detail\_no, return\_warehouse).
- Return self.get\_valuation\_details(bundle\_data).

**Methods declared on this owner** [get return against packed item](operations-054.md#op-f1e390e127ce7a), [get valuation rate for returned supplied item](operations-054.md#op-4c4d0a4215e544), [get delivered packed item bundle](operations-054.md#op-2de141b73fcf7f), [get legacy valuation rate for return entry](operations-054.md#op-db399d9a575c99), [get valuation details](operations-054.md#op-0761bfe332f188).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L578)

<a id="op-4c4d0a4215e544"></a>
### Serialand Batch Bundle.get valuation rate for returned supplied item

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_valuation_rate_for_returned_supplied_item`

**Inputs** self, return\_against.

**Explicit results** self.get\_valuation\_details(bundle\_data).

**Local steps**

- Set returned from Platform.qb.DocType(“Subcontracting Receipt Supplied Item”).
- Set consumed from Platform.qb.DocType(“Subcontracting Receipt Supplied Item”).as\_(“consumed”).
- Set item from Platform.qb.DocType(“Subcontracting Receipt Item”).
- Set original from Platform.qb.DocType(“Subcontracting Receipt Item”).as\_(“original”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set bundle\_data from nested operand in the contract(nested operand in the contract).orderby(consumed.idx).orderby(entry.idx).run(as\_dict = true).
- Return self.get\_valuation\_details(bundle\_data).

**Methods declared on this owner** [get valuation details](operations-054.md#op-0761bfe332f188).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1091) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L588)

<a id="op-0761bfe332f188"></a>
### Serialand Batch Bundle.get valuation details

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_valuation_details`

**Inputs** bundle\_data.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping() · valuation\_details.

**Local steps**

- If not bundle\_data.
  - Return mapping().
- Set valuation\_details from Platform.\_dict(mapping(“serial\_nos” → defaultdict(float), “batches” → defaultdict(float))).
- For each row in bundle\_data.
  - If row.serial\_no.
    - Set valuation\_details at “serial\_nos” at row.serial\_no from row.incoming\_rate.
  - If row.batch\_no.
    - Set valuation\_details at “batches” at row.batch\_no from row.incoming\_rate.
- Return valuation\_details.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1090) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L587)

<a id="op-2de141b73fcf7f"></a>
### Serialand Batch Bundle.get delivered packed item bundle

`operation_enterprise_binding_enterprise_stock_doctype_serial_and_batch_bundle_serial_and_batch_bundle_serialandbatchbundle_get_delivered_packed_item_bundle`

**Inputs** self.

**Explicit results** no value · bundles at 0 at 0 when bundles, otherwise no value.

**Local steps**

- If self.voucher\_type does not belong to tuple(“Delivery Note”, “Sales Invoice”).
  - Return no value.
- Set returned from Platform.qb.DocType(“Packed Item”).
- Set delivered from Platform.qb.DocType(“Packed Item”).as\_(“delivered”).
- Set bundles from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise or (nested operand in the contract bitwise and nested oper ….run().
- Return bundles at 0 at 0 when bundles, otherwise no value.
  - Value choice on bundles — true gives bundles at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1084) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L581)

<a id="op-f1e390e127ce7a"></a>
### Serialand Batch Bundle.get return against packed item

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_return_against_packed_item`

**Inputs** self, field.

**Record and data access** read “Packed Item” via get\_value · read self.child\_table via get\_value.

**Explicit results** no value · Platform.db.get\_value(self.child\_table, parent\_detail\_docname, field).

**Local steps**

- Set parent\_detail\_docname from Platform.db.get\_value(“Packed Item”, self.voucher\_detail\_no, “parent\_detail\_docname”).
- If not parent\_detail\_docname.
  - Return no value.
- Return Platform.db.get\_value(self.child\_table, parent\_detail\_docname, field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0805.json#L3585) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L573)

<a id="op-db399d9a575c99"></a>
### Serialand Batch Bundle.get legacy valuation rate for return entry

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_legacy_valuation_rate_for_return_entry`

**Inputs** self, return\_against, return\_against\_voucher\_detail\_no, return\_warehouse = no value.

**Explicit results** list() · data.

**Local steps**

- Bind dependencies get\_serial\_nos.
- If not (self.has\_serial\_no or self.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_serial\_no → self.has\_batch\_no.
  - Return list().
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract.qb.from\_(sle).select(sle.serial\_no, sle.batch\_no, sle.incoming\_rate, sle.actual\_qty, …).where(((((nested operand in the contract.voucher\_no equals return\_against bitwise and  ….
- If return\_warehouse.
  - Set query from query.where(sle.warehouse equals return\_warehouse).
- Set data from list().
- For each d in query.run(as\_dict = true).
  - Set incoming\_rate from d.incoming\_rate.
  - If d.actual\_qty &lt; 0.
    - Set incoming\_rate from abs((d.stock\_value\_difference ÷ d.actual\_qty)).
  - If d.serial\_no.
    - For each serial\_no in get\_serial\_nos(d.serial\_no).
      - Evaluate data.append(Platform.\_dict(mapping(“serial\_no” → serial\_no, “batch\_no” → d.batch\_no, “incoming\_rate” → incoming\_rate))).
  - Otherwise.
    - If d.batch\_no.
      - Evaluate data.append(Platform.\_dict(mapping(“serial\_no” → no value, “batch\_no” → d.batch\_no, “incoming\_rate” → incoming\_rate))).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L569)

<a id="op-6b200e57dfcd7e"></a>
### Serialand Batch Bundle.calculate total qty

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_calculate_total_quantity`

**Inputs** self, save = true.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.total\_qty from 0.0.
- For each d in self.entries.
  - Set d.qty from 1 when (self.has\_serial\_no and abs(d.qty) &gt; 1), otherwise abs(d.qty) when d.qty, otherwise 0.
    - Value choice on (self.has\_serial\_no and abs(d.qty) &gt; 1) — true gives 1, false gives abs(d.qty) when d.qty, otherwise 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → abs(d.qty) &gt; 1.
    - Value choice on d.qty — true gives abs(d.qty), false gives 0.
  - Set d.stock\_value\_difference from abs(d.stock\_value\_difference) when d.stock\_value\_difference, otherwise 0.
    - Value choice on d.stock\_value\_difference — true gives abs(d.stock\_value\_difference), false gives 0.
  - If self.type\_of\_transaction equals “Outward”.
    - Update d.qty using × negative 1.
    - Update d.stock\_value\_difference using × negative 1.
  - Update self.total\_qty using + flt(d.qty).
- If save.
  - Evaluate self.db\_set(“total\_qty”, self.total\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0805.json#L4438) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L914) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L559)

<a id="op-137a920a05a565"></a>
### Serialand Batch Bundle.get serial nos

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_serial_numbers`

**Inputs** self.

**Explicit results** list of d.serial\_no for d drawn from self.entries where d.serial\_no.

**Local steps**

- Return list of d.serial\_no for d drawn from self.entries where d.serial\_no.
  - Draw d from self.entries, keep a combination only if (d.serial\_no).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0805.json#L4843) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L574)

<a id="op-88f322e3eb919e"></a>
### Serialand Batch Bundle.update valuation rate

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_update_valuation_rate`

**Inputs** self, valuation\_rate = no value, save = false.

**State and service calls** call db\_set on row.

**Local steps**

- For each row in self.entries.
  - Set row.incoming\_rate from valuation\_rate.
  - Set row.stock\_value\_difference from (flt(row.qty) × flt(valuation\_rate)).
  - If save.
    - Evaluate row.db\_set(mapping(“incoming\_rate” → row.incoming\_rate, “stock\_value\_difference” → row.stock\_value\_difference)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0805.json#L4915) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L598)

<a id="op-d4892294352b78"></a>
### Serialand Batch Bundle.set incoming rate for outward transaction

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_set_incoming_rate_for_outward_transaction`

**Inputs** self, row = no value, save = false, allow\_negative\_stock = false.

**State and service calls** call db\_set on d.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_valuation\_method, is\_serial\_no\_wise\_valuation\_disabled.
- If is\_serial\_no\_wise\_valuation\_disabled(self.item\_code).
  - Return no value.
- Set sle from self.get\_sle\_for\_outward\_transaction().
- If self.has\_serial\_no.
  - Set sn\_obj from SerialNoValuation(sle = sle, item\_code = self.item\_code, warehouse = self.warehouse).
- Otherwise.
  - Set sn\_obj from BatchNoValuation(sle = sle, item\_code = self.item\_code, warehouse = self.warehouse).
- Set stock\_queue from list().
- If (hasattr(sn\_obj, “stock\_queue”) and sn\_obj.stock\_queue).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(sn\_obj, “stock\_queue”) → sn\_obj.stock\_queue.
  - Set stock\_queue from parse\_json(sn\_obj.stock\_queue).
- Set val\_method from get\_valuation\_method(self.item\_code, self.company).
- For each d in self.entries.
  - Set available\_qty from 0.
  - If self.has\_serial\_no.
    - Set d.incoming\_rate from abs(sn\_obj.serial\_no\_incoming\_rate.get(d.serial\_no, 0.0)).
  - Otherwise.
    - Set actual\_qty from d.qty.
    - If (stock\_queue and val\_method belongs to tuple(“FIFO”, “LIFO”) and d.batch\_no belongs to sn\_obj.non\_batchwise\_valuation\_batches).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_queue → val\_method belongs to tuple(“FIFO”, “LIFO”) → d.batch\_no belongs to sn\_obj.non\_batchwise\_valuation\_batches.
      - If actual\_qty &lt; 0.
        - Set queue\_class from LIFOValuation when val\_method equals “LIFO”, otherwise FIFOValuation.
          - Value choice on val\_method equals “LIFO” — true gives LIFOValuation, false gives FIFOValuation.
        - Set stock\_queue from queue\_class(stock\_queue).
        - Set tuple(\_prev\_qty, prev\_stock\_value) from stock\_queue.get\_total\_stock\_and\_value().
        - Evaluate stock\_queue.remove\_stock(qty = abs(actual\_qty)).
        - Set tuple(\_qty, stock\_value) from stock\_queue.get\_total\_stock\_and\_value().
        - Set stock\_value\_difference from (stock\_value − prev\_stock\_value).
        - Set d.incoming\_rate from abs((flt(stock\_value\_difference) ÷ abs(flt(actual\_qty)))).
        - Set stock\_queue from stock\_queue.state.
      - Otherwise.
        - Set d.incoming\_rate from abs(flt(sn\_obj.batch\_avg\_rate.get(d.batch\_no))).
        - Evaluate stock\_queue.append(list(d.qty, d.incoming\_rate)).
      - Set d.stock\_queue from json.dumps(stock\_queue).
    - Otherwise.
      - Set d.incoming\_rate from abs(flt(sn\_obj.batch\_avg\_rate.get(d.batch\_no))).
    - Set precision from d.precision(“qty”).
    - Set available\_qty from flt(sn\_obj.available\_qty.get(d.batch\_no), precision).
    - If self.docstatus equals 1.
      - Update available\_qty using + flt(d.qty, precision).
    - If not allow\_negative\_stock.
      - Evaluate self.validate\_negative\_batch(d.batch\_no, available\_qty).
  - Set d.stock\_value\_difference from (flt(d.qty) × flt(d.incoming\_rate)).
  - If save.
    - Evaluate d.db\_set(mapping(“incoming\_rate” → d.incoming\_rate, “stock\_value\_difference” → d.stock\_value\_difference, “stock\_queue” → d.get(“stock\_queue”))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sle for outward transaction](operations-054.md#op-89e245ee04c598), [validate negative batch](operations-054.md#op-6d7ab4db8b61c3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L590)

<a id="op-6d7ab4db8b61c3"></a>
### Serialand Batch Bundle.validate negative batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_negative_batch`

**Inputs** self, batch\_no, available\_qty.

**Explicit failure paths** validation helper with BatchNegativeStockError — translated msg.

**Local steps**

- If (available\_qty &lt; 0 and not self.is\_stock\_reco\_for\_valuation\_adjustment(available\_qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in available\_qty &lt; 0 → not self.is\_stock\_reco\_for\_valuation\_adjustment(available\_qty).
  - Set msg from formatted text Batch No {bold(batch\_no)} of an Item {bold(self.item\_code)}  has negative stock  of quantity {bold(available\_qty)} in the  warehouse {self.wa.
  - Call the validation error handler Platform.throw(translated msg, BatchNegativeStockError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is stock reco for valuation adjustment](operations-054.md#op-ceeabff1af13af).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L962) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L606)

<a id="op-ceeabff1af13af"></a>
### Serialand Batch Bundle.is stock reco for valuation adjustment

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_is_stock_reco_for_valuation_adjustment`

**Inputs** self, available\_qty.

**Record and data access** read “Stock Reconciliation Item” via get\_value.

**Explicit results** true · false.

**Local steps**

- If (self.voucher\_type equals “Stock Reconciliation” and self.type\_of\_transaction equals “Outward” and self.voucher\_detail\_no and abs(Platform.db.get\_value(“Stock Reconciliation Item”, self.voucher\_detail\_no,  ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Stock Reconciliation” → self.type\_of\_transaction equals “Outward” → self.voucher\_detail\_no → abs(Platform.db.get\_value(“Stock Reconciliation Item”, self.voucher\_detail\_no, “qty”)) equals abs(available\_qty).
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0805.json#L6721) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L579)

<a id="op-89e245ee04c598"></a>
### Serialand Batch Bundle.get sle for outward transaction

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_get_stock_ledger_entry_for_outward_transaction`

**Inputs** self.

**Explicit results** sle.

**Local steps**

- Set sle from Platform.\_dict(mapping(“posting\_datetime” → self.posting\_datetime, “item\_code” → self.item\_code, “warehouse” → self.warehouse, “serial\_and\_batch\_bundle” → self.name, …)).
  - Draw row from self.entries, keep a combination only if (row.serial\_no).
  - Draw row from self.entries, keep a combination only if (row.batch\_no).
- If self.docstatus equals 1.
  - Set sle at “voucher\_no” from self.voucher\_no.
- If not sle.actual\_qty.
  - Evaluate self.calculate\_total\_qty().
  - Set sle.actual\_qty from self.total\_qty.
- Return sle.

**Methods declared on this owner** [calculate total qty](operations-054.md#op-6b200e57dfcd7e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0806.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L577)
