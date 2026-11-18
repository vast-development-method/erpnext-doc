# Inventory and warehouses · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bin

[Record definition](../../../../data/record-types/bin.json)

<a id="op-12a3c7bf10858b"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_bin_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_unique on “Bin”.

**Local steps**

- Evaluate Platform.db.add\_unique(“Bin”, list(“item\_code”, “warehouse”), constraint\_name = “unique\_item\_warehouse”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0710.json#L7414) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L831)

<a id="op-cf06d7ea8e2a43"></a>
### Get bin details

`operation_enterprise_stock_record_definitions_bin_business_behavior_get_bin_details`

**Inputs** bin\_name.

**Record and data access** read “Bin” via get\_value.

**Explicit results** Platform.db.get\_value(“Bin”, bin\_name, list(“actual\_qty”, “ordered\_qty”, “reserved\_qty”, “indented\_qty”, …), as\_dict = 1).

**Local steps**

- Return Platform.db.get\_value(“Bin”, bin\_name, list(“actual\_qty”, “ordered\_qty”, “reserved\_qty”, “indented\_qty”, …), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0710.json#L7502) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L829)

<a id="op-84481aa19ca644"></a>
### Update bin columns

`operation_enterprise_binding_enterprise_stock_doctype_bin_bin_update_bin_columns`

**Inputs** bin\_name, values.

**Local steps**

- Set table from Platform.qb.DocType(“Bin”).
- Set query from nested operand in the contract.qb.update(table).set(table.modified, now()).where(table.name equals bin\_name).
- For each tuple(fieldname, value) in values.items().
  - Set query from query.set(table at fieldname, value).
- Evaluate query.set(table.projected\_qty, get\_projected\_qty\_term(table, values)).run().
- Evaluate Platform.clear\_document\_cache(“Bin”, bin\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L204)

<a id="op-738ca576833dad"></a>
### Get projected qty term

`operation_enterprise_binding_enterprise_stock_doctype_bin_bin_get_projected_qty_term`

**Inputs** table, values.

**Explicit results** projected\_qty.

**Local steps**

- Bind local operation qty for subsequent calls.
- Set projected\_qty from ValueWrapper(0).
- For each fieldname in PROJECTED\_QTY\_ADDITIONS.
  - Set projected\_qty from (projected\_qty + qty(fieldname)).
- For each fieldname in PROJECTED\_QTY\_DEDUCTIONS.
  - Set projected\_qty from (projected\_qty − qty(fieldname)).
- Return projected\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L202)

<a id="op-a4c8d35a69eb86"></a>
### Get projected qty term.qty

`operation_enterprise_binding_enterprise_stock_doctype_bin_bin_get_projected_qty_term_qty`

**Inputs** fieldname.

**Explicit results** flt(values at fieldname) when fieldname belongs to values, otherwise Coalesce(table at fieldname, 0).

**Local steps**

- Return flt(values at fieldname) when fieldname belongs to values, otherwise Coalesce(table at fieldname, 0).
  - Value choice on fieldname belongs to values — true gives flt(values at fieldname), false gives Coalesce(table at fieldname, 0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L203)

<a id="op-2a1d0d95322bef"></a>
### Update qty

`operation_enterprise_binding_enterprise_stock_doctype_bin_bin_update_qty`

**Inputs** bin\_name, args.

**State and service calls** request set\_value on “Bin”.

**Local steps**

- Bind dependencies future\_sle\_exists.
- Set bin\_details from get\_bin\_details(bin\_name).
- Set actual\_qty from (bin\_details.actual\_qty or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bin\_details.actual\_qty → 0.0.
- If (future\_sle\_exists(args) or args.get(“is\_cancelled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in future\_sle\_exists(args) → args.get(“is\_cancelled”).
  - Set actual\_qty from get\_actual\_qty(args.get(“item\_code”), args.get(“warehouse”)).
- Set ordered\_qty from (flt(bin\_details.ordered\_qty) + flt(args.get(“ordered\_qty”))).
- Set reserved\_qty from (flt(bin\_details.reserved\_qty) + flt(args.get(“reserved\_qty”))).
- Set indented\_qty from (flt(bin\_details.indented\_qty) + flt(args.get(“indented\_qty”))).
- Set planned\_qty from (flt(bin\_details.planned\_qty) + flt(args.get(“planned\_qty”))).
- Set projected\_qty from (((((((nested operand in the contract + nested operand in the contract) + nested operand in the contract(nested operand in the contract)) + flt(planned\_qty)) − flt(reserved\_qty)) − flt(bin\_details.reserved ….
- Evaluate Platform.db.set\_value(“Bin”, bin\_name, mapping(“actual\_qty” → actual\_qty, “ordered\_qty” → ordered\_qty, “reserved\_qty” → reserved\_qty, “indented\_qty” → indented\_qty, …), update\_modified = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L205)

<a id="op-9a64c47f48405b"></a>
### Get actual qty

`operation_enterprise_stock_record_definitions_bin_business_behavior_get_actual_quantity`

**Inputs** item\_code, warehouse.

**Explicit results** get\_last\_sle\_values(item\_code, warehouse).qty\_after\_transaction.

**Local steps**

- Return get\_last\_sle\_values(item\_code, warehouse).qty\_after\_transaction.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L1018) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L828)

<a id="op-4f7d24d663a7ed"></a>
### Get last sle values

`operation_enterprise_stock_record_definitions_bin_business_behavior_get_last_stock_ledger_entry_values`

**Inputs** item\_code, warehouse.

**Explicit results** last\_sle at 0 · Platform.\_dict(qty\_after\_transaction = 0.0, valuation\_rate = 0.0, stock\_value = 0.0).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set last\_sle from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(sle.creation, order = Order.desc).limit(1).run(as\_dict = true).
- If last\_sle.
  - Return last\_sle at 0.
- Return Platform.\_dict(qty\_after\_transaction = 0.0, valuation\_rate = 0.0, stock\_value = 0.0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L1085) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L830)

## Report · Bom search

<a id="op-7017b9fa7e8944"></a>
### Execute

`operation_enterprise_stock_report_bill_of_materials_search_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read doctype via get\_all.

**Explicit results** tuple(list(mapping(“fieldname” → “parent”, “label” → translated “BOM”, “width” → 200, “fieldtype” → “Dynamic Link”, …), mapping(“fieldname” → “doctype”, “label” → translated “Type”, “width” → 200, “fieldty ….

**Local steps**

- Set data from list().
- Set parents from mapping(“Product Bundle Item” → “Product Bundle”, “BOM Explosion Item” → “BOM”, “BOM Item” → “BOM”).
- Set doctypes from list(“Product Bundle Item”, “BOM Item”).
- If filters.search\_sub\_assemblies.
  - Evaluate doctypes.append(“BOM Explosion Item”).
- Set all\_boms from mapping().
- For each doctype in doctypes.
  - For each d in Platform.get\_all(doctype, fields = list(“parent”, “item\_code”), filters = get\_parent\_filters(doctype)).
    - Evaluate all\_boms.setdefault(tuple(d.parent, parents at doctype), set()).add(d.item\_code).
- For each tuple(parent, items) in all\_boms.items().
  - Set valid from true.
  - For each tuple(key, item) in filters.items().
    - If key differs from “search\_sub\_assemblies”.
      - If (item and item does not belong to items).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item does not belong to items.
        - Set valid from false.
  - If valid.
    - Evaluate data.append(parent).
- Return tuple(list(mapping(“fieldname” → “parent”, “label” → translated “BOM”, “width” → 200, “fieldtype” → “Dynamic Link”, …), mapping(“fieldname” → “doctype”, “label” → translated “Type”, “width” → 200, “fieldty ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L87)

<a id="op-f0c831ce7564ee"></a>
### Get parent filters

`operation_enterprise_binding_enterprise_stock_report_bom_search_bom_search_get_parent_filters`

**Inputs** doctype.

**Explicit results** list() · list(nested operand in the contract.qb.DocType(doctype).parent.isin(allowed\_bundles)) · list(nested operand in the contract.qb.DocType(doctype).parent.isin(submitted\_boms)).

**Local steps**

- If doctype equals “Product Bundle Item”.
  - Set bundle from Platform.qb.DocType(“Product Bundle”).
  - Set condition from get\_allowed\_masters\_condition(bundle.new\_item\_code, “Item”).
  - If not condition.
    - Return list().
  - Set allowed\_bundles from nested operand in the contract.qb.from\_(bundle).select(bundle.name).where(condition).
  - Return list(nested operand in the contract.qb.DocType(doctype).parent.isin(allowed\_bundles)).
- Set bom from Platform.qb.DocType(“BOM”).
- Set submitted\_boms from nested operand in the contract.qb.from\_(bom).select(bom.name).where(bom.docstatus equals 1).
- Return list(nested operand in the contract.qb.DocType(doctype).parent.isin(submitted\_boms)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L950)

## Report · Cogs by item group

<a id="op-d8e5acd5fe9092"></a>
### Execute

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_execute`

**Inputs** filters.

**Declared result** tuple at tuple(Columns, Data).

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate update\_filters\_with\_account(filters).
- Evaluate validate\_filters(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L1648) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L94)

<a id="op-226c6bbe3d7980"></a>
### Update filters with account

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_update_filters_with_account`

**Inputs** filters.

**Declared result** no value.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set account from Platform.get\_value(“Company”, filters.get(“company”), “default\_expense\_account”).
- Evaluate filters.update(dict(account = account)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L1808) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L103)

<a id="op-b32d435474cf5e"></a>
### Validate filters

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_validate_filters`

**Inputs** filters.

**Declared result** no value.

**Local steps**

- Evaluate validate\_mandatory\_date\_range(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L1955) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L105)

<a id="op-bcdf3b8d3b0c1a"></a>
### Get columns

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** Columns.

**Explicit results** list(mapping(“label” → translated “Item Group”, “fieldname” → “item\_group”, “fieldtype” → “Data”, “width” → “200”), mapping(“label” → translated “COGS Debit”, “fieldname” → “cogs\_debit”, “fieldtype” → “Cur ….

**Local steps**

- Return list(mapping(“label” → translated “Item Group”, “fieldname” → “item\_group”, “fieldtype” → “Data”, “width” → “200”), mapping(“label” → translated “COGS Debit”, “fieldname” → “cogs\_debit”, “fieldtype” → “Cur ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L2012) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L95)

<a id="op-4eb2a275091778"></a>
### Get data

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_data`

**Inputs** filters.

**Declared result** Data.

**Explicit results** data.

**Local steps**

- Set account from filters.account.
- Set filtered\_entries from get\_filtered\_entries(filters).
- Set svd\_list from get\_stock\_value\_difference\_list(filtered\_entries, account).
- Set leveled\_dict from get\_leveled\_dict().
- Evaluate assign\_self\_values(leveled\_dict, svd\_list).
- Evaluate assign\_agg\_values(leveled\_dict).
- Set data from list().
- For each item in leveled\_dict.items().
  - Set i from item at 1.
  - If i at “agg\_value” equals 0.
    - Continue with the next iteration or loop test.
  - Evaluate data.append(get\_row(i at “name”, i at “agg\_value”, i at “is\_group”, i at “level”)).
  - If (i at “self\_value” &lt; i at “agg\_value” and i at “self\_value” &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in i at “self\_value” &lt; i at “agg\_value” → i at “self\_value” &gt; 0.
    - Evaluate data.append(get\_row(i at “name”, i at “self\_value”, 0, (i at “level” + 1))).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L96)

<a id="op-54d6dc5e9595c5"></a>
### Get filtered entries

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_filtered_entries`

**Inputs** filters.

**Declared result** FilteredEntries.

**Explicit results** filtered\_entries.

**Local steps**

- Set gl\_entries from get\_gl\_entries(filters, list()).
- Set filtered\_entries from list().
- For each entry in gl\_entries.
  - Set posting\_date from entry.get(“posting\_date”).
  - Set from\_date from filters.get(“from\_date”).
  - If date\_diff(from\_date, posting\_date) &gt; 0.
    - Continue with the next iteration or loop test.
  - Evaluate filtered\_entries.append(entry).
- Return filtered\_entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L2727) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L97)

<a id="op-74f9d90eb0be14"></a>
### Get stock value difference list

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_stock_value_difference_list`

**Inputs** filtered\_entries, account.

**Declared result** SVDList.

**Record and data access** read “Stock Ledger Entry” via get\_list.

**Explicit results** svd\_list.

**Local steps**

- Set voucher\_nos from list of fe.get(“voucher\_no”) for fe drawn from filtered\_entries.
  - Draw fe from filtered\_entries.
- Set svd\_list from Platform.get\_list(“Stock Ledger Entry”, fields = list(“item\_code”, “stock\_value\_difference”, “voucher\_type”, “voucher\_no”, …), filters = list(tuple(“voucher\_no”, “in”, voucher\_nos), tuple(“is\_cancelled”, “=”, 0))).
- Set booked\_rows from get\_rows\_booked\_to\_account(svd\_list, account).
- Set booked\_reconciliations from get\_reconciliations\_booked\_to\_account(svd\_list, account).
- Set svd\_list from list of row for row drawn from svd\_list where is\_booked\_to\_account(row, booked\_rows, booked\_reconciliations).
  - Draw row from svd\_list, keep a combination only if (is\_booked\_to\_account(row, booked\_rows, booked\_reconciliations)).
- Evaluate assign\_item\_groups\_to\_svd\_list(svd\_list).
- Return svd\_list.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L102)

<a id="op-3df29e6db47e19"></a>
### Is booked to account

`operation_enterprise_binding_enterprise_stock_report_cogs_by_item_group_cogs_by_item_group_is_booked_to_account`

**Inputs** row, booked\_rows, booked\_reconciliations.

**Declared result** bool.

**Explicit results** row.voucher\_no belongs to booked\_reconciliations · row.voucher\_detail\_no belongs to booked\_rows · true.

**Local steps**

- If row.voucher\_type equals “Stock Reconciliation”.
  - Return row.voucher\_no belongs to booked\_reconciliations.
- If row.voucher\_type belongs to ITEM\_ROW\_DOCTYPES.
  - Return row.voucher\_detail\_no belongs to booked\_rows.
- Return true.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L953)

<a id="op-ff985a5983a93b"></a>
### Get rows booked to account

`operation_enterprise_binding_enterprise_stock_report_cogs_by_item_group_cogs_by_item_group_get_rows_booked_to_account`

**Inputs** svd\_list, account.

**Declared result** set at str.

**Explicit results** booked\_rows.

**Local steps**

- Set rows\_by\_doctype from defaultdict(set).
- For each row in svd\_list.
  - For each row\_doctype in ITEM\_ROW\_DOCTYPES.get(row.voucher\_type, tuple()).
    - Evaluate rows\_by\_doctype at row\_doctype.add(row.voucher\_detail\_no).
- Set booked\_rows from set().
- For each tuple(row\_doctype, names) in rows\_by\_doctype.items().
  - Set table from Platform.qb.DocType(row\_doctype).
  - Evaluate booked\_rows.update(nested operand in the contract.select(nested operand in the contract.name).where((nested operand in the contract.isin(names) bitwise and nested operand in the contract.expense\_account eq ….
- Return booked\_rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L952)

<a id="op-7c75e1ec4030a6"></a>
### Get reconciliations booked to account

`operation_enterprise_binding_enterprise_stock_report_cogs_by_item_group_cogs_by_item_group_get_reconciliations_booked_to_account`

**Inputs** svd\_list, account.

**Declared result** set at str.

**Record and data access** read “Stock Reconciliation” via get\_all.

**Explicit results** set() · set(Platform.get\_all(“Stock Reconciliation”, filters = mapping(“name” → tuple(“in”, list(names)), “expense\_account” → account), pluck = “name”)).

**Local steps**

- Set names from set of row.voucher\_no for row drawn from svd\_list where row.voucher\_type equals “Stock Reconciliation”.
  - Draw row from svd\_list, keep a combination only if (row.voucher\_type equals “Stock Reconciliation”).
- If not names.
  - Return set().
- Return set(Platform.get\_all(“Stock Reconciliation”, filters = mapping(“name” → tuple(“in”, list(names)), “expense\_account” → account), pluck = “name”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L951)

<a id="op-8ebd4e6b0068e7"></a>
### Get leveled dict

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_leveled_mapping`

**Inputs** no declared parameters.

**Declared result** OrderedDict.

**Explicit results** leveled\_dict.

**Local steps**

- Set item\_groups\_dict from get\_item\_groups\_dict().
- Set lr\_list from sorted(item\_groups\_dict, key = deferred anonymous expression).
- Set leveled\_dict from OrderedDict().
- Set current\_level from 0.
- Set nesting\_r from list().
- For each tuple(l, r) in lr\_list.
  - While (current\_level &gt; 0 and nesting\_r at negative 1 &lt; l).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_level &gt; 0 → nesting\_r at negative 1 &lt; l.
    - Evaluate nesting\_r.pop().
    - Update current\_level using − 1.
  - Set leveled\_dict at tuple(l, r) from mapping(“level” → current\_level, “name” → item\_groups\_dict at tuple(l, r) at “name”, “is\_group” → item\_groups\_dict at tuple(l, r) at “is\_group”).
  - If (int(r) − int(l)) &gt; 1.
    - Update current\_level using + 1.
    - Evaluate nesting\_r.append(r).
- Evaluate update\_leveled\_dict(leveled\_dict).
- Return leveled\_dict.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L3204) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L100)

<a id="op-6f85182a66c484"></a>
### Assign self values

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_assign_self_values`

**Inputs** leveled\_dict, svd\_list.

**Declared result** no value.

**Local steps**

- Set key\_dict from mapping of v at “name” → k for tuple(k, v) drawn from leveled\_dict.items().
  - Draw tuple(k, v) from leveled\_dict.items().
- For each item in svd\_list.
  - Set key from key\_dict at item.get(“item\_group”).
  - Update leveled\_dict at key at “self\_value” using + negative item.get(“stock\_value\_difference”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L3722) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L93)

<a id="op-682e065212be53"></a>
### Assign agg values

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_assign_aggregation_values`

**Inputs** leveled\_dict.

**Declared result** no value.

**Local steps**

- Set keys from list(leveled\_dict.keys()) at slice no value to no value with step negative 1.
- Set prev\_level from leveled\_dict at keys at negative 1 at “level”.
- Set accu from list(0).
- For each k in keys at slice no value to negative 1.
  - Set curr\_level from leveled\_dict at k at “level”.
  - If curr\_level equals prev\_level.
    - Update accu at negative 1 using + leveled\_dict at k at “self\_value”.
    - Set leveled\_dict at k at “agg\_value” from leveled\_dict at k at “self\_value”.
  - Otherwise.
    - If curr\_level &gt; prev\_level.
      - Evaluate accu.append(leveled\_dict at k at “self\_value”).
      - Set leveled\_dict at k at “agg\_value” from accu at negative 1.
    - Otherwise.
      - If curr\_level &lt; prev\_level.
        - Update accu at negative 1 using + leveled\_dict at k at “self\_value”.
        - Set leveled\_dict at k at “agg\_value” from accu at negative 1.
  - Set prev\_level from curr\_level.
- Set rk from keys at negative 1.
- Set leveled\_dict at rk at “agg\_value” from (sum(accu) + leveled\_dict at rk at “self\_value”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L3943) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L91)

<a id="op-ed26de9ed02203"></a>
### Get row

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_row`

**Inputs** name, value, is\_bold, indent.

**Declared result** Row.

**Explicit results** Platform.\_dict(item\_group = item\_group, cogs\_debit = value, indent = indent).

**Local steps**

- Set item\_group from name.
- If is\_bold.
  - Set item\_group from Platform.bold(item\_group).
- Return Platform.\_dict(item\_group = item\_group, cogs\_debit = value, indent = indent).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L4557) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L101)
