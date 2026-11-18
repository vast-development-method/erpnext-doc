# Inventory and warehouses · operations 94

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock ledger

<a id="op-1009e1338f19c5"></a>
### Get stock value difference

`operation_enterprise_stock_stock_ledger_business_behavior_get_stock_value_difference`

**Inputs** item\_code, warehouse, posting\_date, posting\_time, voucher\_no = no value, voucher\_detail\_no = no value, creation = no value.

**Explicit results** flt(difference\_amount at 0 at 0) when difference\_amount, otherwise 0.

**Local steps**

- Set table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set posting\_datetime from get\_combine\_datetime(posting\_date, posting\_time).
- Set query from nested operand in the contract.qb.from\_(table).select(Sum(nested operand in the contract.stock\_value\_difference).as\_(“value”)).where(((table.is\_cancelled equals 0 bitwise and table.item\_code equals item\_co ….
- If voucher\_detail\_no.
  - Set query from query.where((table.voucher\_detail\_no differs from voucher\_detail\_no bitwise or table.voucher\_detail\_no.isnull())).
- Otherwise.
  - If voucher\_no.
    - Set query from query.where(table.voucher\_no differs from voucher\_no).
- Set query from query.where(get\_prior\_ledger\_condition(table, posting\_datetime, creation)).
- Set difference\_amount from query.run().
- Return flt(difference\_amount at 0 at 0) when difference\_amount, otherwise 0.
  - Value choice on difference\_amount — true gives flt(difference\_amount at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L731)

<a id="op-920d3a35ddfeb5"></a>
### Get serial from sabb

`operation_enterprise_stock_stock_ledger_business_behavior_get_serial_from_stock_accounting_balance`

**Inputs** serial\_and\_batch\_bundle.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → serial\_and\_batch\_bundle), fields = list(“serial\_no”, “batch\_no”, “name”, “qty”, …), order\_by = “idx”).

**Local steps**

- Return Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → serial\_and\_batch\_bundle), fields = list(“serial\_no”, “batch\_no”, “name”, “qty”, …), order\_by = “idx”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L3522) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L726)

<a id="op-dfa628120201b1"></a>
### Get incoming rate for serial and batch

`operation_enterprise_stock_stock_ledger_business_behavior_get_incoming_rate_for_serial_and_batch`

**Inputs** item\_code, row, sn\_obj, company.

**Explicit results** abs(sn\_obj.serial\_no\_incoming\_rate.get(row.serial\_no, 0.0)) · incoming\_rate.

**Local steps**

- If row.serial\_no.
  - Return abs(sn\_obj.serial\_no\_incoming\_rate.get(row.serial\_no, 0.0)).
- Otherwise.
  - Set stock\_queue from list().
  - If (hasattr(sn\_obj, “stock\_queue”) and sn\_obj.stock\_queue).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(sn\_obj, “stock\_queue”) → sn\_obj.stock\_queue.
    - Set stock\_queue from parse\_json(sn\_obj.stock\_queue).
  - Set val\_method from get\_valuation\_method(item\_code, company).
  - Set actual\_qty from row.qty.
  - If (stock\_queue and val\_method belongs to tuple(“FIFO”, “LIFO”) and row.batch\_no belongs to sn\_obj.non\_batchwise\_valuation\_batches).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_queue → val\_method belongs to tuple(“FIFO”, “LIFO”) → row.batch\_no belongs to sn\_obj.non\_batchwise\_valuation\_batches.
    - If actual\_qty &lt; 0.
      - Set queue\_class from LIFOValuation when val\_method equals “LIFO”, otherwise FIFOValuation.
        - Value choice on val\_method equals “LIFO” — true gives LIFOValuation, false gives FIFOValuation.
      - Set stock\_queue from queue\_class(stock\_queue).
      - Set tuple(\_prev\_qty, prev\_stock\_value) from stock\_queue.get\_total\_stock\_and\_value().
      - Evaluate stock\_queue.remove\_stock(qty = abs(actual\_qty)).
      - Set tuple(\_qty, stock\_value) from stock\_queue.get\_total\_stock\_and\_value().
      - Set stock\_value\_difference from (stock\_value − prev\_stock\_value).
      - Set incoming\_rate from abs((flt(stock\_value\_difference) ÷ abs(flt(actual\_qty)))).
      - Set stock\_queue from stock\_queue.state.
    - Otherwise.
      - Set incoming\_rate from abs(flt(sn\_obj.batch\_avg\_rate.get(row.batch\_no))).
      - Evaluate stock\_queue.append(list(row.qty, incoming\_rate)).
    - Set row.stock\_queue from json.dumps(stock\_queue).
  - Otherwise.
    - Set incoming\_rate from abs(flt(sn\_obj.batch\_avg\_rate.get(row.batch\_no))).
- Return incoming\_rate.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L717)

<a id="op-a2335dc22226a2"></a>
### Is repack entry

`operation_enterprise_stock_stock_ledger_business_behavior_is_repack_entry`

**Inputs** stock\_entry\_id.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Stock Entry” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Stock Entry”, stock\_entry\_id, “purpose”) equals “Repack”.

**Local steps**

- Return Platform.get\_cached\_value(“Stock Entry”, stock\_entry\_id, “purpose”) equals “Repack”.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry”, stock\_entry\_id, “purpose”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L4458) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L737)

<a id="op-1d22d482ca6cc3"></a>
### Is manufactured finished good

`operation_enterprise_binding_enterprise_stock_stock_ledger_is_manufactured_finished_good`

**Inputs** sle.

**Record and data access** read “Stock Entry” via get\_cached\_value · read “Stock Entry Detail” via get\_value.

**Explicit results** bool((sle.voucher\_type equals “Stock Entry” and flt(sle.actual\_qty) &gt; 0 and Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”) equals “Manufacture” and Platform.db.get\_value(“Stock Entry Detail …).

**Local steps**

- Return bool((sle.voucher\_type equals “Stock Entry” and flt(sle.actual\_qty) &gt; 0 and Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”) equals “Manufacture” and Platform.db.get\_value(“Stock Entry Detail …).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals “Stock Entry” → flt(sle.actual\_qty) &gt; 0 → Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”) equals “Manufacture” → Platform.db.get\_value(“Stock Entry Detail”, sle.voucher\_detail\_no, “is\_finished\_item”, cache = true).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry”, sle.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1096)

<a id="op-5ff60b331de400"></a>
### Is manufacture or repack entry

`operation_enterprise_binding_enterprise_stock_stock_ledger_is_manufacture_or_repack_entry`

**Inputs** stock\_entry\_id.

**Record and data access** read “Stock Entry” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Stock Entry”, stock\_entry\_id, “purpose”) belongs to tuple(“Manufacture”, “Repack”).

**Local steps**

- Return Platform.get\_cached\_value(“Stock Entry”, stock\_entry\_id, “purpose”) belongs to tuple(“Manufacture”, “Repack”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Stock Entry”, stock\_entry\_id, “purpose”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1095)

<a id="op-09f659eaaf60a7"></a>
### Has correct data

`operation_enterprise_stock_stock_ledger_business_behavior_has_correct_data`

**Inputs** sle.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** true · false.

**Local steps**

- Set previous\_sle from get\_previous\_sle(mapping(“item\_code” → sle.item\_code, “warehouse” → sle.warehouse, “posting\_date” → sle.posting\_date, “posting\_time” → sle.posting\_time, …)).
- If not previous\_sle.
  - Return true.
- Set previous\_qty from (previous\_sle.get(“qty\_after\_transaction”) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_sle.get(“qty\_after\_transaction”) → 0.
- If (previous\_qty and not Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → sle.voucher\_detail\_no, “is\_cancelled” → 0, “actual\_qty” → tuple(“&lt;”, 0)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_qty → not Platform.db.get\_value(“Stock Ledger Entry”, mapping(“voucher\_detail\_no” → sle.voucher\_detail\_no, “is\_cancelled” → 0, “actual\_qty” → tuple(“&lt;”, 0))).
  - Return false.
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0942.json#L4551) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L733)

## Report · Stock ledger entries of cancelled vouchers

<a id="op-2499126399d21d"></a>
### Execute

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data(filters)).

**Explicit failure paths** validation helper — translated “Please select a Company”.

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If not filters.company.
  - Call the validation error handler Platform.throw(translated “Please select a Company”).
- Evaluate validate\_company\_permission(filters.company).
- Return tuple(get\_columns(), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1038)

<a id="op-371cdf98846cd5"></a>
### Validate company permission

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_validate_company_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** company.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1048)

<a id="op-d20ee02c8311a5"></a>
### Get allowed values

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_get_allowed_values`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping() · allowed\_values.

**Local steps**

- Bind dependencies get\_user\_permissions.
- Set user\_permissions from get\_user\_permissions().
- If not user\_permissions.
  - Return mapping().
- Set allowed\_values from mapping().
- For each df in Platform.get\_meta(“Stock Ledger Entry”).get\_link\_fields().
  - If df.ignore\_user\_permissions.
    - Continue with the next iteration or loop test.
  - Set values from list of d.doc for d drawn from user\_permissions.get(df.options, list()) where (not d.applicable\_for or d.applicable\_for equals “Stock Ledger Entry”).
    - Draw d from user\_permissions.get(df.options, list()), keep a combination only if ((not d.applicable\_for or d.applicable\_for equals “Stock Ledger Entry”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.applicable\_for → d.applicable\_for equals “Stock Ledger Entry”.
  - If values.
    - Set allowed\_values at df.fieldname from values.
- Return allowed\_values.

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1041)

<a id="op-4153103273c888"></a>
### Get columns

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Stock Ledger Entry”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Stock Ledger Entry”, …), mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher ….

**Local steps**

- Return list(mapping(“label” → translated “Stock Ledger Entry”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Stock Ledger Entry”, …), mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1043)

<a id="op-16d7d6adc82a2a"></a>
### Get data

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_get_data`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** sorted(data, key = deferred anonymous expression).

**Local steps**

- Set data from list().
- For each voucher\_type in get\_voucher\_types(filters).
  - Evaluate data.extend(get\_uncancelled\_entries(voucher\_type, filters)).
- Return sorted(data, key = deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1044)

<a id="op-c3dc59efde66af"></a>
### Get voucher types

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_get_voucher_types`

**Inputs** filters.

**Declared result** list at str.

**Explicit results** list of d for d drawn from voucher\_types where Platform.db.table\_exists(d).

**Local steps**

- If filters.voucher\_type.
  - Set voucher\_types from list(filters.voucher\_type).
- Otherwise.
  - Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
  - Set query from nested operand in the contract.qb.from\_(sle).select(sle.voucher\_type).distinct().
  - Set voucher\_types from list of d at 0 for d drawn from apply\_filters(query, sle, filters).run().
    - Draw d from apply\_filters(query, sle, filters).run().
- Return list of d for d drawn from voucher\_types where Platform.db.table\_exists(d).
  - Draw d from voucher\_types, keep a combination only if (Platform.db.table\_exists(d)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1046)

<a id="op-3243d625338bc2"></a>
### Get uncancelled entries

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_get_uncancelled_entries`

**Inputs** voucher\_type, filters.

**Declared result** list at dict.

**Explicit results** apply\_filters(query, sle, filters).run(as\_dict = true).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set voucher from Platform.qb.DocType(voucher\_type).
- Set sabb from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set query from nested operand in the contract(nested operand in the contract).on(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested opera ….
- Return apply\_filters(query, sle, filters).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1045)

<a id="op-4f80e802e063e5"></a>
### Apply filters

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_apply_filters`

**Inputs** query, sle, filters.

**Explicit results** query.

**Local steps**

- Set query from query.where(sle.is\_cancelled equals 0).
- For each field in tuple(“company”, “item\_code”, “warehouse”).
  - If filters.get(field).
    - Set query from query.where(sle at field equals filters.get(field)).
- If filters.from\_date.
  - Set query from query.where(sle.posting\_date ≥ filters.from\_date).
- If filters.to\_date.
  - Set query from query.where(sle.posting\_date ≤ filters.to\_date).
- Set strict from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).
- For each tuple(field, values) in get\_allowed\_values().items().
  - Set condition from sle at field.isin(values).
  - If not strict.
    - Update condition using bitwise or (sle at field.isnull() bitwise or sle at field equals empty text).
  - Set query from query.where(condition).
- Return query.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1036)

<a id="op-f90efb50802809"></a>
### Fix uncancelled entries

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_fix_uncancelled_entries`

**Inputs** selected\_rows.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read voucher\_type via get\_value.

**State and service calls** msgprint with translated “Stock Ledger Entries of the selected vouchers have been cancelled and reposting has been queued.”.

**Local steps**

- Evaluate Platform.only\_for(list(“Stock Manager”, “System Manager”)).
- If isinstance(selected\_rows, str).
  - Set selected\_rows from Platform.parse\_json(selected\_rows).
- Set vouchers from set of tuple(row.get(“voucher\_type”), row.get(“voucher\_no”)) for row drawn from selected\_rows.
  - Draw row from selected\_rows.
- For each tuple(voucher\_type, voucher\_no) in vouchers.
  - If Platform.db.get\_value(voucher\_type, voucher\_no, “docstatus”) differs from 2.
    - Continue with the next iteration or loop test.
  - Evaluate validate\_voucher\_permission(voucher\_type, voucher\_no).
  - Evaluate fix\_voucher(voucher\_type, voucher\_no).
- Evaluate Platform.msgprint(translated “Stock Ledger Entries of the selected vouchers have been cancelled and reposting has been queued.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(list(“Stock Manager”, “System Manager”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1039)

<a id="op-755b2a82b6d55c"></a>
### Validate voucher permission

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_validate_voucher_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** voucher\_type, voucher\_no.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 3 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1049)

<a id="op-4c0ef0bc575287"></a>
### Fix voucher

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_fix_voucher`

**Inputs** voucher\_type, voucher\_no.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** no value.

**Local steps**

- Set entries from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no, “is\_cancelled” → 0), fields = list(“item\_code”, “warehouse”, “posting\_date”, “posting\_time ….
- If not entries.
  - Return no value.
- Evaluate set\_as\_cancel(voucher\_type, voucher\_no).
- Evaluate cancel\_serial\_and\_batch\_bundles(voucher\_type, voucher\_no).
- Evaluate repost\_future\_entries(entries).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1040)

<a id="op-43553a5c904abc"></a>
### Get bundles to cancel

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_get_bundles_to_cancel`

**Inputs** voucher\_type, voucher\_no.

**Record and data access** read “Serial and Batch Bundle” via get\_all.

**Explicit results** Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no, “docstatus” → list(“!=”, 0)), or\_filters = mapping(“is\_cancelled” → 0, “docstatus” →  ….

**Local steps**

- Return Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no, “docstatus” → list(“!=”, 0)), or\_filters = mapping(“is\_cancelled” → 0, “docstatus” →  ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1042)

<a id="op-8baf7911e564c0"></a>
### Cancel serial and batch bundles

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_cancel_serial_and_batch_bundles`

**Inputs** voucher\_type, voucher\_no.

**Explicit results** no value.

**Local steps**

- Set bundles from get\_bundles\_to\_cancel(voucher\_type, voucher\_no).
- If not bundles.
  - Return no value.
- Set sabb from Platform.qb.DocType(“Serial and Batch Bundle”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(sabb.docstatus, 2).where(sabb.name.isin(bundles)).run().
- Set sabb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(sabb\_entry.docstatus, 2).where(sabb\_entry.parent.isin(bundles)).run().
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).set(sle.serial\_and\_batch\_bundle, no value).where(sle.serial\_and\_batch\_bundle.isin(bundles)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1037)

<a id="op-f000015b90b9d7"></a>
### Repost future entries

`operation_enterprise_binding_enterprise_stock_report_stock_ledger_entries_of_cancelled_vouchers_stock_ledger_entries_of_cancelled_vouchers_repost_future_entries`

**Inputs** entries.

**Local steps**

- Bind dependencies create\_repost\_item\_valuation\_entry.
- Set reposted from set().
- For each sle in entries.
  - Set key from tuple(sle.item\_code, sle.warehouse).
  - If key belongs to reposted.
    - Continue with the next iteration or loop test.
  - Evaluate reposted.add(key).
  - Evaluate create\_repost\_item\_valuation\_entry(mapping(“based\_on” → “Item and Warehouse”, “item\_code” → sle.item\_code, “warehouse” → sle.warehouse, “posting\_date” → sle.posting\_date, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1047)

## Record · Stock ledger entry

[Record definition](../../../../data/record-types/stock_ledger_entry.json)

<a id="op-29be4f20076eef"></a>
### Stock Ledger Entry.autoname

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_autoname`

**Inputs** self.

**Local steps**

- Set self.name from Platform.generate\_hash(txt = empty text, length = 10).
- If self.meta.autoname equals “hash”.
  - Set self.to\_rename from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(txt = empty text, length = 10).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L5286) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L38) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L969)

<a id="op-9e033c9ecbf6b5"></a>
### Stock Ledger Entry.validate

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_validate`

**Inputs** self.

**Local steps**

- Set self.flags.ignore\_submit\_comment from true.
- Bind dependencies validate\_disabled\_warehouse, validate\_warehouse\_company.
- Evaluate self.set\_posting\_datetime().
- Evaluate self.validate\_mandatory().
- Evaluate self.validate\_batch().
- Evaluate validate\_disabled\_warehouse(self.warehouse).
- Evaluate validate\_warehouse\_company(self.warehouse, self.company).
- Evaluate self.scrub\_posting\_time().
- Evaluate self.validate\_and\_set\_fiscal\_year().
- Evaluate self.block\_transactions\_against\_group\_warehouse().
- Evaluate self.validate\_with\_last\_transaction\_posting\_time().
- Evaluate validate\_no\_later\_adjustment\_entry(self).
- Evaluate self.validate\_inventory\_dimension\_negative\_stock().
- Evaluate self.validate\_serial\_no\_inventory\_dimension().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set posting datetime](operations-094.md#op-e265976df59bd2), [validate mandatory](operations-095.md#op-c0383c5c119096), [validate batch](operations-095.md#op-70064f3bfb016f), [scrub posting time](operations-095.md#op-8ceb672cb99b57), [validate and set fiscal year](operations-095.md#op-ad88385d81758a), [block transactions against group warehouse](operations-095.md#op-0aae79fc132768), [validate with last transaction posting time](operations-095.md#op-e446968cc5f3d9), [validate inventory dimension negative stock](operations-095.md#op-c870dab4c2f604), [validate serial no inventory dimension](operations-095.md#op-26760f178d505e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L51) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L980)

<a id="op-e265976df59bd2"></a>
### Stock Ledger Entry.set posting datetime

`operation_enterprise_stock_record_definitions_stock_ledger_entry_business_behavior_stock_ledger_entry_set_posting_datetime`

**Inputs** self.

**Local steps**

- Bind dependencies get\_combine\_datetime.
- Set self.posting\_datetime from get\_combine\_datetime(self.posting\_date, self.posting\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0852.json#L5718) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L978)
