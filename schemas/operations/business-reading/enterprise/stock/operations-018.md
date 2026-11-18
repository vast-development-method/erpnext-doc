# Inventory and warehouses · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Incorrect serial and batch bundle

<a id="op-b472347ae4405e"></a>
### Execute

`operation_enterprise_stock_report_incorrect_serial_and_batch_bundle_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set unlinked\_bundles from (get\_unlinked\_serial\_batch\_bundles(filters) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_unlinked\_serial\_batch\_bundles(filters) → list().
- Set linked\_cancelled\_bundles from (get\_linked\_cancelled\_sabb(filters) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_linked\_cancelled\_sabb(filters) → list().
- Set data from (unlinked\_bundles + linked\_cancelled\_bundles).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0891.json#L3499) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L148)

<a id="op-bb1e75825ca27e"></a>
### Get columns

`operation_enterprise_stock_report_incorrect_serial_and_batch_bundle_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Serial and Batch Bundle”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Serial and Batch Bundle”, …), mapping(“label” → translated “Voucher Type”, “fieldname”  ….

**Local steps**

- Return list(mapping(“label” → translated “Serial and Batch Bundle”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Serial and Batch Bundle”, …), mapping(“label” → translated “Voucher Type”, “fieldname”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L150)

<a id="op-dc17a33bfb72c4"></a>
### Get unlinked serial batch bundles

`operation_enterprise_stock_report_incorrect_serial_and_batch_bundle_business_behavior_get_unlinked_serial_batch_bundles`

**Inputs** filters.

**Declared result** list at list.

**Explicit results** data.

**Local steps**

- Set SABB from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set SLE from Platform.qb.DocType(“Stock Ledger Entry”).
- Set POS from Platform.qb.DocType(“POS Invoice”).
- Set ignore\_voycher\_types from list(“Installation Note”, “Job Card”, “Maintenance Schedule”, “Pick List”).
- Set query from nested operand in the contract(nested operand in the contract).on((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in t ….
- For each field in filters.
  - Set query from query.where(SABB at field equals filters at field).
- Set data from query.run(as\_dict = 1).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L152)

<a id="op-68e802b8d6441f"></a>
### Get linked cancelled sabb

`operation_enterprise_stock_report_incorrect_serial_and_batch_bundle_business_behavior_get_linked_cancelled_stock_accounting_balance`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set SABB from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set SLE from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.serial\_and\_batch\_bundle).select(SABB.name, SABB.voucher\_type, SAB ….
- For each field in filters.
  - Set query from query.where(SABB at field equals filters at field).
- Set data from query.run(as\_dict = 1).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0891.json#L4737) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L151)

<a id="op-04b0dbff7661ee"></a>
### Fix sabb entries

`operation_enterprise_stock_report_incorrect_serial_and_batch_bundle_business_behavior_fix_stock_accounting_balance_entries`

**Inputs** selected\_rows.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc · read “Stock Ledger Entry” via exists.

**State and service calls** msgprint with translated “Selected Serial and Batch Bundle entries have been fixed.”.

**Local steps**

- Evaluate Platform.has\_permission(“Serial and Batch Bundle”, “write”, throw = true).
- If isinstance(selected\_rows, str).
  - Set selected\_rows from Platform.parse\_json(selected\_rows).
- For each row in selected\_rows.
  - Set doc from Platform.get\_doc(“Serial and Batch Bundle”, row.get(“name”)).
  - Evaluate doc.check\_permission(“write”).
  - Set has\_active\_entry from Platform.db.exists(“Stock Ledger Entry”, mapping(“serial\_and\_batch\_bundle” → doc.name, “is\_cancelled” → 0)).
  - If (doc.docstatus equals 1 and not doc.is\_cancelled and not has\_active\_entry).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus equals 1 → not doc.is\_cancelled → not has\_active\_entry.
    - If not is\_pending\_pos\_invoice\_bundle(doc).
      - Evaluate set\_bundle\_docstatus(doc, 2).
  - Otherwise.
    - If (doc.docstatus equals 2 and doc.is\_cancelled and has\_active\_entry).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.docstatus equals 2 → doc.is\_cancelled → has\_active\_entry.
      - Evaluate set\_bundle\_docstatus(doc, 1).
- Evaluate Platform.msgprint(translated “Selected Serial and Batch Bundle entries have been fixed.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Serial and Batch Bundle”, “write”, throw = true), doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L149)

<a id="op-9ee721a258e60a"></a>
### Is pending pos invoice bundle

`operation_enterprise_binding_enterprise_stock_report_incorrect_serial_and_batch_bundle_incorrect_serial_and_batch_bundle_is_pending_pos_invoice_bundle`

**Inputs** doc.

**Record and data access** read “POS Invoice” via get\_value.

**Explicit results** (doc.voucher\_type equals “POS Invoice” and Platform.db.get\_value(“POS Invoice”, doc.voucher\_no, “docstatus”) equals 1).

**Local steps**

- Return (doc.voucher\_type equals “POS Invoice” and Platform.db.get\_value(“POS Invoice”, doc.voucher\_no, “docstatus”) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.voucher\_type equals “POS Invoice” → Platform.db.get\_value(“POS Invoice”, doc.voucher\_no, “docstatus”) equals 1.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L958)

<a id="op-1ab9bc054589a2"></a>
### Set bundle docstatus

`operation_enterprise_binding_enterprise_stock_report_incorrect_serial_and_batch_bundle_incorrect_serial_and_batch_bundle_set_bundle_docstatus`

**Inputs** doc, docstatus.

**State and service calls** call db\_set on doc · call db\_set on entry.

**Local steps**

- Evaluate doc.db\_set(mapping(“is\_cancelled” → cint(docstatus equals 2), “docstatus” → docstatus)).
- For each entry in doc.entries.
  - Evaluate entry.db\_set(“docstatus”, docstatus).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L959)

## Report · Incorrect serial no valuation

<a id="op-ef1734b28fef55"></a>
### Execute

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L155)

<a id="op-d4509df22fcf29"></a>
### Get data

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from get\_stock\_ledger\_entries(filters).
- Set bundles from get\_bundles(data).
- Set serial\_nos\_data from prepare\_serial\_nos(data, bundles).
- Set data from get\_incorrect\_serial\_nos(serial\_nos\_data, (filters.from\_date and getdate(filters.from\_date))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.from\_date → getdate(filters.from\_date).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L158)

<a id="op-1adf3483d27520"></a>
### Get bundles

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_get_bundles`

**Inputs** data.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** bundle\_dict.

**Local steps**

- Set bundles from list of d.serial\_and\_batch\_bundle for d drawn from data where d.serial\_and\_batch\_bundle.
  - Draw d from data, keep a combination only if (d.serial\_and\_batch\_bundle).
- Set bundle\_dict from Platform.\_dict().
- Set serial\_nos\_data from Platform.get\_all(“Serial and Batch Entry”, fields = list(“parent”, “serial\_no”, “incoming\_rate”, “qty”), filters = mapping(“parent” → tuple(“in”, bundles), “serial\_no” → tuple(“is”, “set”))).
- For each entry in serial\_nos\_data.
  - Evaluate bundle\_dict.setdefault(entry.parent, list()).append(entry).
- Return bundle\_dict.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0892.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L156)

<a id="op-dd6f76bc5fec82"></a>
### Prepare serial nos

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_prepare_serial_numbers`

**Inputs** data, bundles.

**Explicit results** serial\_no\_wise\_data.

**Local steps**

- Set serial\_no\_wise\_data from mapping().
- For each row in data.
  - If (not row.serial\_nos and not row.serial\_and\_batch\_bundle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.serial\_nos → not row.serial\_and\_batch\_bundle.
    - Continue with the next iteration or loop test.
  - If row.serial\_and\_batch\_bundle.
    - For each bundle in bundles.get(row.serial\_and\_batch\_bundle, list()).
      - Set sle from copy.deepcopy(row).
      - Set sle.serial\_no from bundle.serial\_no.
      - Set sle.qty from bundle.qty.
      - Set sle.valuation\_rate from (bundle.incoming\_rate × 1 when sle.qty &gt; 0, otherwise negative 1).
        - Value choice on sle.qty &gt; 0 — true gives 1, false gives negative 1.
      - Evaluate serial\_no\_wise\_data.setdefault(bundle.serial\_no, list()).append(sle).
    - Continue with the next iteration or loop test.
  - For each serial\_no in get\_serial\_nos(row.serial\_nos).
    - Set sle from copy.deepcopy(row).
    - Set sle.serial\_no from serial\_no.
    - Set sle.qty from 1 when sle.actual\_qty &gt; 0, otherwise negative 1.
      - Value choice on sle.actual\_qty &gt; 0 — true gives 1, false gives negative 1.
    - Set sle.valuation\_rate from sle.valuation\_rate when sle.actual\_qty &gt; 0, otherwise (sle.valuation\_rate × negative 1).
      - Value choice on sle.actual\_qty &gt; 0 — true gives sle.valuation\_rate, false gives (sle.valuation\_rate × negative 1).
    - Evaluate serial\_no\_wise\_data.setdefault(serial\_no, list()).append(sle).
- Return serial\_no\_wise\_data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0892.json#L320) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L522) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L161)

<a id="op-10358a7b450743"></a>
### Get incorrect serial nos

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_get_incorrect_serial_numbers`

**Inputs** serial\_nos\_data, from\_date.

**Explicit results** result.

**Local steps**

- Set result from list().
- Set total\_value from Platform.\_dict(mapping(“qty” → 0, “valuation\_rate” → 0, “serial\_no” → Platform.bold(translated “Balance”))).
- For each tuple(\_serial\_no, data) in serial\_nos\_data.items().
  - Set total\_dict from Platform.\_dict(mapping(“qty” → 0, “valuation\_rate” → 0, “serial\_no” → Platform.bold(translated “Total”))).
  - If check\_incorrect\_serial\_data(data, total\_dict, from\_date).
    - Evaluate result.extend(generator of row for row drawn from data where (not from\_date or row.posting\_date ≥ from\_date)).
      - Draw row from data, keep a combination only if ((not from\_date or row.posting\_date ≥ from\_date)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → row.posting\_date ≥ from\_date.
    - Update total\_value.qty using + total\_dict.qty.
    - Update total\_value.valuation\_rate using + total\_dict.valuation\_rate.
    - If (total\_dict.qty equals 0 and abs(total\_dict.valuation\_rate) equals 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_dict.qty equals 0 → abs(total\_dict.valuation\_rate) equals 0.
      - Continue with the next iteration or loop test.
    - Evaluate result.append(total\_dict).
    - Evaluate result.append(mapping()).
- Evaluate result.append(total\_value).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L520) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L159)

<a id="op-2fc44a17c45259"></a>
### Check incorrect serial data

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_check_incorrect_serial_data`

**Inputs** data, total\_dict, from\_date.

**Explicit results** incorrect\_data.

**Local steps**

- Set incorrect\_data from false.
- For each row in data.
  - Update total\_dict.qty using + row.qty.
  - Update total\_dict.valuation\_rate using + row.valuation\_rate.
  - If (from\_date and row.posting\_date &lt; from\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → row.posting\_date &lt; from\_date.
    - Continue with the next iteration or loop test.
  - If ((total\_dict.qty equals 0 and abs(total\_dict.valuation\_rate) &gt; 0) or total\_dict.qty &lt; 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (total\_dict.qty equals 0 and abs(total\_dict.valuation\_rate) &gt; 0) → total\_dict.qty &lt; 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_dict.qty equals 0 → abs(total\_dict.valuation\_rate) &gt; 0.
    - Set incorrect\_data from true.
- Return incorrect\_data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L154)

<a id="op-29b6ee28711e68"></a>
### Get stock ledger entries

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_get_stock_ledger_entries`

**Inputs** report\_filters.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, fields = fields, filters = filters, or\_filters = or\_filters, order\_by = “posting\_date asc, posting\_time asc, creation asc”).

**Local steps**

- Set fields from list(“name”, “voucher\_type”, “voucher\_no”, “item\_code”, …).
- Set filters from mapping(“is\_cancelled” → 0).
- Set or\_filters from mapping(“serial\_no” → tuple(“is”, “set”), “serial\_and\_batch\_bundle” → tuple(“is”, “set”)).
- If report\_filters.get(“item\_code”).
  - Set filters at “item\_code” from report\_filters.get(“item\_code”).
- Otherwise.
  - If (report\_filters.get(“from\_date”) and report\_filters.get(“to\_date”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_filters.get(“from\_date”) → report\_filters.get(“to\_date”).
    - Set filters at “item\_code” from tuple(“in”, get\_items\_moved\_in\_period(report\_filters, filters, or\_filters)).
- If report\_filters.get(“to\_date”).
  - Set filters at “posting\_date” from tuple(“&lt;=”, report\_filters.get(“to\_date”)).
- Return Platform.get\_all(“Stock Ledger Entry”, fields = fields, filters = filters, or\_filters = or\_filters, order\_by = “posting\_date asc, posting\_time asc, creation asc”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L521) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L160)

<a id="op-33860d667cb48d"></a>
### Get items moved in period

`operation_enterprise_binding_enterprise_stock_report_incorrect_serial_no_valuation_incorrect_serial_no_valuation_get_items_moved_in_period`

**Inputs** report\_filters, filters, or\_filters.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, filters = mapping(expand filters, “posting\_date” → tuple(“between”, period)), or\_filters = or\_filters, pluck = “item\_code”, distinct = true).

**Local steps**

- Set period from list(report\_filters.get(“from\_date”), report\_filters.get(“to\_date”)).
- Return Platform.get\_all(“Stock Ledger Entry”, filters = mapping(expand filters, “posting\_date” → tuple(“between”, period)), or\_filters = or\_filters, pluck = “item\_code”, distinct = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L960)

<a id="op-7006f86a67025b"></a>
### Get columns

`operation_enterprise_stock_report_incorrect_serial_number_valuation_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Company”, “fieldtype” → “Link”, “fieldname” → “company”, “options” → “Company”, …), mapping(“label” → translated “Id”, “fieldtype” → “Link”, “fieldname” → “name”, “option ….

**Local steps**

- Return list(mapping(“label” → translated “Company”, “fieldtype” → “Link”, “fieldname” → “company”, “options” → “Company”, …), mapping(“label” → translated “Id”, “fieldtype” → “Link”, “fieldname” → “name”, “option ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0892.json#L2301) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L157)

## Report · Incorrect stock value report

<a id="op-52a3dbae0d88ae"></a>
### Execute

`operation_enterprise_stock_report_incorrect_stock_value_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “Perpetual inventory required for the company {0} to view this report.”.format(filters.company) · validation helper with Platform.MandatoryError — translated “Select the stock Account to compare with the stock value”.

**Local steps**

- If not Enterprise.is\_perpetual\_inventory\_enabled(filters.company).
  - Call the validation error handler Platform.throw(translated “Perpetual inventory required for the company {0} to view this report.”.format(filters.company)).
- If not filters.get(“account”).
  - Call the validation error handler Platform.throw(translated “Select the stock Account to compare with the stock value”, Platform.MandatoryError).
- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L163)

<a id="op-f043da1f3e0a39"></a>
### Get unsync date

`operation_enterprise_stock_report_incorrect_stock_value_report_business_behavior_get_unsync_date`

**Inputs** filters.

**Explicit results** no value · date.

**Local steps**

- Set date from filters.from\_date.
- If not date.
  - Set date from nested operand in the contract.qb.from\_(“Stock Ledger Entry”).select(Min(Field(“posting\_date”))).run().
  - Set date from date at 0 at 0.
- If not date.
  - Return no value.
- While getdate(date) ≤ getdate(today()).
  - Set tuple(account\_bal, stock\_bal, warehouse\_list) from get\_stock\_and\_account\_balance(posting\_date = date, company = filters.company, account = filters.account).
  - If abs((account\_bal − stock\_bal)) &gt; 0.1.
    - Return date.
  - Set date from add\_days(date, 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L166)

<a id="op-a0a056c50f1704"></a>
### Get data

`operation_enterprise_stock_report_incorrect_stock_value_report_business_behavior_get_data`

**Inputs** report\_filters.

**Explicit results** list() · result.

**Local steps**

- Set from\_date from (report\_filters.from\_date or get\_unsync\_date(report\_filters)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in report\_filters.from\_date → get\_unsync\_date(report\_filters).
- If not from\_date.
  - Return list().
- Set warehouses from get\_account\_warehouses(report\_filters.company, report\_filters.account).
- If warehouses equals list().
  - Return list().
- Set entries from get\_entries\_from(from\_date, report\_filters.company, warehouses).
- Set running\_values from get\_stock\_values\_before(from\_date, report\_filters.company, entries).
- Set result from list().
- For each data in entries.
  - Set key from tuple(data.item\_code, data.warehouse).
  - Set expected\_stock\_value from (flt(running\_values.get(key)) + flt(data.stock\_value\_difference)).
  - If abs((flt(data.stock\_value) − expected\_stock\_value)) &gt; 0.1.
    - Set data.difference\_value from abs((flt(data.stock\_value) − expected\_stock\_value)).
    - Set data.expected\_stock\_value from expected\_stock\_value.
    - Evaluate result.append(data).
  - Set running\_values at key from expected\_stock\_value.
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L165)

<a id="op-8d9bb66e5fc1fd"></a>
### Get account warehouses

`operation_enterprise_binding_enterprise_stock_report_incorrect_stock_value_report_incorrect_stock_value_report_get_account_warehouses`

**Inputs** company, account.

**Explicit results** no value · list of warehouse for tuple(warehouse, details) drawn from get\_warehouse\_account\_map(company).items() where (details.account equals account and not details.is\_group).

**Local steps**

- Set stock\_account from Platform.qb.DocType(“Account”).
- Set no\_of\_stock\_accounts from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … at 0.
- If cint(no\_of\_stock\_accounts) ≤ 1.
  - Return no value.
- Return list of warehouse for tuple(warehouse, details) drawn from get\_warehouse\_account\_map(company).items() where (details.account equals account and not details.is\_group).
  - Draw tuple(warehouse, details) from get\_warehouse\_account\_map(company).items(), keep a combination only if ((details.account equals account and not details.is\_group)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in details.account equals account → not details.is\_group.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L961)

<a id="op-8389d0c652b3ad"></a>
### Get entries from

`operation_enterprise_binding_enterprise_stock_report_incorrect_stock_value_report_incorrect_stock_value_report_get_entries_from`

**Inputs** from\_date, company, warehouses = no value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.name, sle.posting\_date, sle.posting\_time, sle.voucher\_type, …).where(((nested operand in the contract.posting\_date ≥ from\_date bitw ….
- If warehouses.
  - Set query from query.where(sle.warehouse.isin(warehouses)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L962)

<a id="op-4c82bf831231c9"></a>
### Get stock values before

`operation_enterprise_binding_enterprise_stock_report_incorrect_stock_value_report_incorrect_stock_value_report_get_stock_values_before`

**Inputs** from\_date, company, entries.

**Explicit results** mapping() · mapping of tuple(item\_code, warehouse) → flt(value) for tuple(item\_code, warehouse, value) drawn from rows.

**Local steps**

- If not entries.
  - Return mapping().
- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….run().
  - Draw row from entries.
  - Draw row from entries.
- Return mapping of tuple(item\_code, warehouse) → flt(value) for tuple(item\_code, warehouse, value) drawn from rows.
  - Draw tuple(item\_code, warehouse, value) from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L963)

<a id="op-ac7178092955a8"></a>
### Get columns

`operation_enterprise_stock_report_incorrect_stock_value_report_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Stock Ledger ID”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Stock Ledger Entry”, …), mapping(“label” → translated “Posting Date”, “fieldname” → “posting\_da ….

**Local steps**

- Return list(mapping(“label” → translated “Stock Ledger ID”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Stock Ledger Entry”, …), mapping(“label” → translated “Posting Date”, “fieldname” → “posting\_da ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L164)

## Record · Inventory dimension

[Record definition](../../../../data/record-types/inventory_dimension.json)

<a id="op-79cf9ed0af17c5"></a>
### Inventory Dimension.onload

`operation_enterprise_stock_record_definitions_inventory_dimension_business_behavior_inventory_dimension_onload`

**Inputs** self.

**Local steps**

- If (not self.is\_new() and Platform.db.has\_column(“Stock Ledger Entry”, self.target\_fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → Platform.db.has\_column(“Stock Ledger Entry”, self.target\_fieldname).
  - Evaluate self.set\_onload(“has\_stock\_ledger”, self.has\_stock\_ledger()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has stock ledger](operations-019.md#op-5cca1d513742b4).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0728.json#L490) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1029)
