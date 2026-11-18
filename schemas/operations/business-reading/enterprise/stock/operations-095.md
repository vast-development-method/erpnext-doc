# Inventory and warehouses · operations 95

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock ledger entry

[Record definition](../../../../data/record-types/stock_ledger_entry.json)

<a id="op-c870dab4c2f604"></a>
### Stock Ledger Entry.validate inventory dimension negative stock

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate_inventory_dimension_negative_stock`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_cancelled or self.actual\_qty ≥ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_cancelled → self.actual\_qty ≥ 0.
  - Return no value.
- Set dimensions from self.\_get\_inventory\_dimensions().
- If not dimensions.
  - Return no value.
- Set flt\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set available\_qty from self.get\_available\_qty\_after\_prev\_transaction(dimensions).
- Set diff from flt((available\_qty + flt(self.actual\_qty)), flt\_precision).
- If (diff &lt; 0 and abs(diff) &gt; 0.0001).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in diff &lt; 0 → abs(diff) &gt; 0.0001.
  - Evaluate self.throw\_validation\_error(diff, dimensions).
- If not self.flags.defer\_future\_dimension\_check.
  - Evaluate self.validate\_future\_inventory\_dimension\_balance(diff, dimensions, flt\_precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get inventory dimensions](operations-095.md#op-698e31df21c724), [get available qty after prev transaction](operations-095.md#op-eed5d9c5f024e7), [throw validation error](operations-095.md#op-7776471848eeea), [validate future inventory dimension balance](operations-095.md#op-bfed52a97bfb94).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L54) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L983)

<a id="op-ed960ea18998d4"></a>
### Stock Ledger Entry.validate future dimension balance after voucher

`operation_enterprise_binding_enterprise_stock_doctype_stock_ledger_entry_stock_ledger_entry_stockledgerentry_validate_future_dimension_balance_after_voucher`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_cancelled or self.actual\_qty ≥ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_cancelled → self.actual\_qty ≥ 0.
  - Return no value.
- Set dimensions from self.\_get\_inventory\_dimensions().
- If not dimensions.
  - Return no value.
- Set flt\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set balance from flt(self.get\_available\_qty\_after\_prev\_transaction(dimensions), flt\_precision).
- Evaluate self.validate\_future\_inventory\_dimension\_balance(balance, dimensions, flt\_precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get inventory dimensions](operations-095.md#op-698e31df21c724), [get available qty after prev transaction](operations-095.md#op-eed5d9c5f024e7), [validate future inventory dimension balance](operations-095.md#op-bfed52a97bfb94).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L790)

<a id="op-bfed52a97bfb94"></a>
### Stock Ledger Entry.validate future inventory dimension balance

`operation_enterprise_binding_enterprise_stock_doctype_stock_ledger_entry_stock_ledger_entry_stockledgerentry_validate_future_inventory_dimension_balance`

**Inputs** self, balance, dimensions, precision.

**Local steps**

- For each actual\_qty in self.get\_future\_dimension\_qty(dimensions).
  - Set balance from flt((balance + flt(actual\_qty)), precision).
  - If (balance &lt; 0 and abs(balance) &gt; 0.0001).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in balance &lt; 0 → abs(balance) &gt; 0.0001.
    - Evaluate self.throw\_validation\_error(balance, dimensions).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get future dimension qty](operations-095.md#op-09c7914852422a), [throw validation error](operations-095.md#op-7776471848eeea).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L791)

<a id="op-eed5d9c5f024e7"></a>
### Stock Ledger Entry.get available qty after prev transaction

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_get_available_quantity_after_previous_transaction`

**Inputs** self, dimensions.

**Explicit results** (available\_qty at 0 at 0 or 0).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set available\_qty from nested operand in the contract(nested operand in the contract, nested operand in the contract).select(Sum(nested operand in the contract.actual\_qty)).where(sle.posting\_datetime ≤ self.posting\_datetime).run().
- Return (available\_qty at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in available\_qty at 0 at 0 → 0.

**Methods declared on this owner** [get dimension sle query](operations-095.md#op-d95ecbed565e43).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L41) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L972)

<a id="op-09c7914852422a"></a>
### Stock Ledger Entry.get future dimension qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_ledger_entry_stock_ledger_entry_stockledgerentry_get_future_dimension_qty`

**Inputs** self, dimensions.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).orderby(sle.posting\_datetime).orderby(Min(sle.creation)).run(pluck = true).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).orderby(sle.posting\_datetime).orderby(Min(sle.creation)).run(pluck = true).

**Methods declared on this owner** [get dimension sle query](operations-095.md#op-d95ecbed565e43).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L789)

<a id="op-d95ecbed565e43"></a>
### Stock Ledger Entry.get dimension sle query

`operation_enterprise_binding_enterprise_stock_doctype_stock_ledger_entry_stock_ledger_entry_stockledgerentry_get_dimension_sle_query`

**Inputs** self, sle, dimensions.

**Explicit results** query.

**Local steps**

- Set query from Platform.qb.from\_(sle).where((((sle.item\_code equals self.item\_code bitwise and sle.warehouse equals self.warehouse) bitwise and sle.company equals self.company) bitwise and sle.is\_cancelled equals 0)).
- For each tuple(dimension, values) in dimensions.items().
  - Set query from query.where(sle at dimension equals values.get(“value”)).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L788)

<a id="op-7776471848eeea"></a>
### Stock Ledger Entry.throw validation error

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_throw_validation_error`

**Inputs** self, diff, dimensions.

**Explicit failure paths** validation helper with InventoryDimensionNegativeStockError — msg.

**Local steps**

- Set msg from translated “{0} units of {1} are required in {2} with the inventory dimension: {3} on {4} {5} for {6} to complete the tr …”.format(abs(diff), Platform.get\_desk\_link(“Item”, self.item\_code), Platform.get\_de ….
  - Draw tuple(dimension, values) from dimensions.items().
- Call the validation error handler Platform.throw(msg, title = translated “Inventory Dimension Negative Stock”, exc = InventoryDimensionNegativeStockError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L6611) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L979)

<a id="op-698e31df21c724"></a>
### Stock Ledger Entry.get inventory dimensions

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_get_inventory_dimensions`

**Inputs** self.

**Explicit results** inv\_dimension\_dict.

**Local steps**

- Set inv\_dimensions from get\_inventory\_dimensions().
- Set inv\_dimension\_dict from mapping().
- For each dimension in inv\_dimensions.
  - If (not dimension.get(“validate\_negative\_stock”) or not self.get(dimension.fieldname)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not dimension.get(“validate\_negative\_stock”) → not self.get(dimension.fieldname).
    - Continue with the next iteration or loop test.
  - Set dimension at “value” from self.get(dimension.fieldname).
  - Evaluate inv\_dimension\_dict.setdefault(dimension.fieldname, dimension).
- Return inv\_dimension\_dict.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L7013) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L42) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L973)

<a id="op-26760f178d505e"></a>
### Stock Ledger Entry.validate serial no inventory dimension

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate_serial_number_inventory_dimension`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with SerialNoInventoryDimensionError — translated “Serial No {0} is not available in the selected inventory dimensions: {1}”.format(Platform.bold(serial\_no), Platform.bold(“, ”.join(mismatches))).

**Local steps**

- If (self.is\_cancelled or self.actual\_qty ≥ 0 or not self.has\_serial\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_cancelled → self.actual\_qty ≥ 0 → not self.has\_serial\_no.
  - Return no value.
- Set dimensions from get\_inventory\_dimensions().
- If not dimensions.
  - Return no value.
- Set serial\_nos from get\_serial\_nos(self.serial\_and\_batch\_bundle).
- If (not serial\_nos and self.serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not serial\_nos → self.serial\_no.
  - Set serial\_nos from get\_parsed\_serial\_nos(self.serial\_no).
- If not serial\_nos.
  - Return no value.
- For each tuple(serial\_no, values) in self.get\_last\_inward\_dimensions(serial\_nos, dimensions).items().
  - Set mismatches from list().
  - For each dimension in dimensions.
    - Set fieldname from dimension.fieldname.
    - Set expected\_value from (values.get(fieldname) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in values.get(fieldname) → no value.
    - Set actual\_value from (self.get(fieldname) or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(fieldname) → no value.
    - If expected\_value differs from actual\_value.
      - Evaluate mismatches.append(translated “{0}: expected "{1}", got "{2}"”.format(dimension.dimension\_name, (expected\_value or translated “Not Set”), (actual\_value or translated “Not Set”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in expected\_value → translated “Not Set”.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in actual\_value → translated “Not Set”.
  - If mismatches.
    - Call the validation error handler Platform.throw(translated “Serial No {0} is not available in the selected inventory dimensions: {1}”.format(Platform.bold(serial\_no), Platform.bold(“, ”.join(mismatches))), title = translated “Incorrect In ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get last inward dimensions](operations-095.md#op-6dcfde76ab0d6d).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L986)

<a id="op-6dcfde76ab0d6d"></a>
### Stock Ledger Entry.get last inward dimensions

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_get_last_inward_dimensions`

**Inputs** self, serial\_nos, dimensions.

**Explicit results** last\_inward\_dimensions.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set serial\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set dimension\_fields from list of sle at dimension.fieldname.as\_(dimension.fieldname) for dimension drawn from dimensions.
  - Draw dimension from dimensions.
- Set escaped\_serial\_nos from list of re.escape(serial\_no) for serial\_no drawn from serial\_nos.
  - Draw serial\_no from serial\_nos.
- Set legacy\_serial\_pattern from ((“&#91;\\n,&#93;&#91;&#91;:space:&#93;&#93;\*(” + “\|”.join(escaped\_serial\_nos)) + “)&#91;&#91;:space:&#93;&#93;\*&#91;\\n,&#93;”).
- Set legacy\_serial\_condition from ((sle.serial\_and\_batch\_bundle.isnull() bitwise or sle.serial\_and\_batch\_bundle equals empty text) bitwise and Concat\_ws(empty text, whitespace '\\n', sle.serial\_no, whitespace '\\n').regexp(legacy\_serial\_pattern)).
- Set rows from nested operand in the contract(nested operand in the contract).orderby(sle.posting\_datetime, order = nested operand in the contract.qb.desc).orderby(sle.creation, order = Platform.qb.desc).run(as\_dict = true).
- Set serial\_nos from set(serial\_nos).
- Set last\_inward\_dimensions from mapping().
- For each row in rows.
  - Set row\_serial\_nos from list(row.bundle\_serial\_no) when row.bundle\_serial\_no, otherwise get\_parsed\_serial\_nos(row.legacy\_serial\_nos).
    - Value choice on row.bundle\_serial\_no — true gives list(row.bundle\_serial\_no), false gives get\_parsed\_serial\_nos(row.legacy\_serial\_nos).
  - For each serial\_no in serial\_nos.intersection(row\_serial\_nos).
    - Evaluate last\_inward\_dimensions.setdefault(serial\_no, row).
- Return last\_inward\_dimensions.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0853.json#L672) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L43) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L974)

<a id="op-4950766f05f8a4"></a>
### Stock Ledger Entry.on submit

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_on_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate self.check\_stock\_frozen\_date().
- If (Platform.in\_test and Platform.flags.ignore\_serial\_batch\_bundle\_validation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.in\_test → Platform.flags.ignore\_serial\_batch\_bundle\_validation.
  - Return no value.
- If (self.is\_adjustment\_entry and not self.serial\_and\_batch\_bundle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_adjustment\_entry → not self.serial\_and\_batch\_bundle.
  - Return no value.
- If not self.get(“via\_landed\_cost\_voucher”).
  - Evaluate SerialBatchBundle(sle = self, item\_code = self.item\_code, warehouse = self.warehouse, company = self.company).
- Evaluate self.validate\_serial\_batch\_no\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check stock frozen date](operations-095.md#op-ea64504d334701), [validate serial batch no bundle](operations-095.md#op-c588d02593324f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L46) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L976)

<a id="op-c0383c5c119096"></a>
### Stock Ledger Entry.validate mandatory

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is required”.format(translated self.meta.get\_label(k)) · validation helper — translated “Actual Qty is mandatory”.

**Local steps**

- Set mandatory from list(“warehouse”, “posting\_date”, “voucher\_type”, “voucher\_no”, …).
- For each k in mandatory.
  - If not self.get(k).
    - Call the validation error handler Platform.throw(translated “{0} is required”.format(translated self.meta.get\_label(k))).
- If (self.voucher\_type differs from “Stock Reconciliation” and not self.actual\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type differs from “Stock Reconciliation” → not self.actual\_qty.
  - Call the validation error handler Platform.throw(translated “Actual Qty is mandatory”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L55) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L984)

<a id="op-c588d02593324f"></a>
### Stock Ledger Entry.validate serial batch no bundle

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate_serial_batch_number_bundle`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item {0} not found”.format(self.item\_code) · validation helper with ItemTemplateCannotHaveStock — translated “Stock cannot exist for Item {0} since it has variants”.format(self.item\_code) · validation helper — translated “Item {0} must be a stock Item”.format(self.item\_code) · validation helper — translated “Serial No / Batch No are mandatory for Item {0}”.format(self.item\_code) · validation helper — translated “Serial No and Batch No are not allowed for Item {0}”.format(self.item\_code).

**Local steps**

- If self.is\_cancelled equals 1.
  - Return no value.
- Set item\_detail from Platform.get\_cached\_value(“Item”, self.item\_code, list(“has\_serial\_no”, “has\_batch\_no”, “is\_stock\_item”, “has\_variants”, …), as\_dict = 1).
- Set values\_to\_be\_change from mapping().
- If self.has\_batch\_no differs from item\_detail.has\_batch\_no.
  - Set values\_to\_be\_change at “has\_batch\_no” from item\_detail.has\_batch\_no.
- If self.has\_serial\_no differs from item\_detail.has\_serial\_no.
  - Set values\_to\_be\_change at “has\_serial\_no” from item\_detail.has\_serial\_no.
- If values\_to\_be\_change.
  - Evaluate self.db\_set(values\_to\_be\_change).
- If not item\_detail.
  - Call the validation error handler Platform.throw(translated “Item {0} not found”.format(self.item\_code)).
- If item\_detail.has\_variants.
  - Call the validation error handler Platform.throw(translated “Stock cannot exist for Item {0} since it has variants”.format(self.item\_code), ItemTemplateCannotHaveStock).
- <a id="op-c588d02593324f-guard-31"></a>If item\_detail.is\_stock\_item differs from 1.
  - Call the validation error handler Platform.throw(translated “Item {0} must be a stock Item”.format(self.item\_code)).
- If (item\_detail.has\_serial\_no or item\_detail.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_detail.has\_serial\_no → item\_detail.has\_batch\_no.
  - If not self.serial\_and\_batch\_bundle.
    - Call the validation error handler Platform.throw(translated “Serial No / Batch No are mandatory for Item {0}”.format(self.item\_code)).
- If (self.serial\_and\_batch\_bundle and not item\_detail.has\_serial\_no and not item\_detail.has\_batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.serial\_and\_batch\_bundle → not item\_detail.has\_serial\_no → not item\_detail.has\_batch\_no.
  - Call the validation error handler Platform.throw(translated “Serial No and Batch No are not allowed for Item {0}”.format(self.item\_code)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison item\_detail.is\_stock\_item differs from 1, item\_detail.is\_stock\_item = 2 selects the branch that calls the validation-error handler with translated “Item {0} must be a stock Item”.format(self.item\_code). With item\_detail.is\_stock\_item = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c588d02593324f-guard-31)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, list(“has\_serial\_no”, “has\_batch\_no”, “is\_stock\_item”, “has\_variants”, …), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L56) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L985)

<a id="op-ea64504d334701"></a>
### Stock Ledger Entry.check stock frozen date

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_check_stock_frozen_date`

**Inputs** self.

**Local steps**

- Evaluate check\_stock\_frozen\_date(self.posting\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L40) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L971)

<a id="op-8ceb672cb99b57"></a>
### Stock Ledger Entry.scrub posting time

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_scrub_posting_time`

**Inputs** self.

**Local steps**

- If (not self.posting\_time or self.posting\_time equals “00:0”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.posting\_time → self.posting\_time equals “00:0”.
  - Set self.posting\_time from “00:00”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0853.json#L3557) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L977)

<a id="op-70064f3bfb016f"></a>
### Stock Ledger Entry.validate batch

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate_batch`

**Inputs** self.

**Record and data access** read “Batch” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Batch {0} of Item {1} has expired.”.format(self.batch\_no, self.item\_code).

**Local steps**

- If (self.batch\_no and self.voucher\_type differs from “Stock Entry”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.batch\_no → self.voucher\_type differs from “Stock Entry”.
  - If ((self.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) and self.actual\_qty &lt; 0) or (self.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”) and self.actual\_qty &gt; 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) and self.actual\_qty &lt; 0) → (self.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”) and self.actual\_qty &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) → self.actual\_qty &lt; 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to list(“Delivery Note”, “Sales Invoice”) → self.actual\_qty &gt; 0.
    - Return no value.
  - Set expiry\_date from Platform.db.get\_value(“Batch”, self.batch\_no, “expiry\_date”).
  - If expiry\_date.
    - If getdate(self.posting\_date) &gt; getdate(expiry\_date).
      - Call the validation error handler Platform.throw(translated “Batch {0} of Item {1} has expired.”.format(self.batch\_no, self.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0853.json#L3648) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L53) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L982)

<a id="op-ad88385d81758a"></a>
### Stock Ledger Entry.validate and set fiscal year

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate_and_set_fiscal_year`

**Inputs** self.

**Local steps**

- If not self.fiscal\_year.
  - Set self.fiscal\_year from get\_fiscal\_year(self.posting\_date, company = self.company) at 0.
- Otherwise.
  - Bind dependencies validate\_fiscal\_year.
  - Evaluate validate\_fiscal\_year(self.posting\_date, self.fiscal\_year, self.company, self.meta.get\_label(“posting\_date”), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0853.json#L4058) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L981)

<a id="op-0aae79fc132768"></a>
### Stock Ledger Entry.block transactions against group warehouse

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_block_transactions_against_group_warehouse`

**Inputs** self.

**Local steps**

- Bind dependencies is\_group\_warehouse.
- Evaluate is\_group\_warehouse(self.warehouse).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0853.json#L4248) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L39) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L970)

<a id="op-e446968cc5f3d9"></a>
### Stock Ledger Entry.validate with last transaction posting time

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate_with_last_transaction_posting_time`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value · execute query text (SELECT, Stock Ledger Entry).

**Explicit failure paths** validation helper with BackDatedStockTransaction — msg.

**Local steps**

- Set authorized\_role from Platform.get\_single\_value(“Stock Settings”, “role\_allowed\_to\_create\_edit\_back\_dated\_transactions”).
- If authorized\_role.
  - Set authorized\_users from get\_users(authorized\_role).
  - If (authorized\_users and Platform.session.user does not belong to authorized\_users).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in authorized\_users → Platform.session.user does not belong to authorized\_users.
    - Set last\_transaction\_time from Platform.db.sql(query text (SELECT, Stock Ledger Entry), tuple(self.item\_code, self.warehouse)) at 0 at 0.
    - Set cur\_doc\_posting\_datetime from “{} {}”.format(self.posting\_date, (self.get(“posting\_time”) or “00:00:00”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“posting\_time”) → “00:00:00”.
    - If (last\_transaction\_time and get\_datetime(cur\_doc\_posting\_datetime) &lt; get\_datetime(last\_transaction\_time)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_transaction\_time → get\_datetime(cur\_doc\_posting\_datetime) &lt; get\_datetime(last\_transaction\_time).
      - Set msg from translated “Last Stock Transaction for item {0} under warehouse {1} was on {2}.”.format(Platform.bold(self.item\_code), Platform.bold(self.warehouse), Platform.bold(last\_transaction\_time)).
      - Update msg using + (text in the contract + translated “You are not authorized to make/edit Stock Transactions for Item {0} under warehouse {1} before this time.”.format(Platform.bold(self.item\_code), Platform.bold(self.warehouse))).
      - Update msg using + (text in the contract + translated “Please contact any of the following users for this transaction.”).
      - Update msg using + (text in the contract + text in the contract.join(authorized\_users)).
      - Call the validation error handler Platform.throw(msg, BackDatedStockTransaction, title = translated “Backdated Stock Entry”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “role\_allowed\_to\_create\_edit\_back\_dated\_transactions”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L987)

<a id="op-ad126d37b52a53"></a>
### Stock Ledger Entry.on cancel

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_on_cancel`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set msg from translated “Individual Stock Ledger Entry cannot be cancelled.”.
- Update msg using + (text in the contract + translated “Please cancel related transaction.”).
- Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0853.json#L5157) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L45) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L975)

<a id="op-3f2215196f5420"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Stock Ledger Entry”.

**Local steps**

- Evaluate Platform.db.add\_index(“Stock Ledger Entry”, list(“voucher\_no”, “voucher\_type”)).
- Evaluate Platform.db.add\_index(“Stock Ledger Entry”, list(“item\_code”, “warehouse”, “posting\_datetime”, “creation”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L37) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L968)

<a id="op-e56156f7b56695"></a>
### Check stock frozen date

`operation_enterprise_binding_enterprise_stock_doctype_stock_ledger_entry_stock_ledger_entry_check_stock_frozen_date`

**Inputs** posting\_date.

**Record and data access** resolve a document from “Stock Settings” via get\_cached\_doc.

**Explicit failure paths** validation helper with StockFreezeError — translated “Stock transactions before {0} are frozen”.format(formatdate(stock\_settings.stock\_frozen\_upto)) · validation helper with StockFreezeError — translated “Not allowed to update stock transactions older than {0}”.format(stock\_frozen\_upto\_days).

**Local steps**

- Set stock\_settings from Platform.get\_cached\_doc(“Stock Settings”).
- If stock\_settings.stock\_frozen\_upto.
  - If (getdate(posting\_date) ≤ getdate(stock\_settings.stock\_frozen\_upto) and stock\_settings.stock\_auth\_role does not belong to Platform.get\_roles()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(posting\_date) ≤ getdate(stock\_settings.stock\_frozen\_upto) → stock\_settings.stock\_auth\_role does not belong to Platform.get\_roles().
    - Call the validation error handler Platform.throw(translated “Stock transactions before {0} are frozen”.format(formatdate(stock\_settings.stock\_frozen\_upto)), StockFreezeError).
- Set stock\_frozen\_upto\_days from cint(stock\_settings.stock\_frozen\_upto\_days).
- If stock\_frozen\_upto\_days.
  - Set older\_than\_x\_days\_ago from add\_days(getdate(posting\_date), stock\_frozen\_upto\_days) ≤ date.today().
  - If (older\_than\_x\_days\_ago and stock\_settings.stock\_auth\_role does not belong to Platform.get\_roles()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in older\_than\_x\_days\_ago → stock\_settings.stock\_auth\_role does not belong to Platform.get\_roles().
    - Call the validation error handler Platform.throw(translated “Not allowed to update stock transactions older than {0}”.format(stock\_frozen\_upto\_days), StockFreezeError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Stock Settings”) · effective access from Platform.get\_roles() · clock or generated value from date.today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L787)

## Report · Stock ledger invariant check

<a id="op-472f1cf6ddcdca"></a>
### Execute

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0920.json#L1526) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L526)

<a id="op-0822cb0a02b30f"></a>
### Get data

`operation_enterprise_stock_report_stock_ledger_invariant_check_business_behavior_get_data`

**Inputs** filters.

**Explicit results** add\_invariant\_check\_fields(sles, filters).

**Local steps**

- Set sles from get\_stock\_ledger\_entries(filters).
- Return add\_invariant\_check\_fields(sles, filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0920.json#L1625) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L528)
