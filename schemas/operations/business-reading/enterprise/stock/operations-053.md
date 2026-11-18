# Inventory and warehouses · operations 53

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Repost item valuation

[Record definition](../../../../data/record-types/repost_item_valuation.json)

<a id="op-b696b0f3adf092"></a>
### Get items with active reposting

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_get_items_with_active_reposting`

**Inputs** entries\_in\_progress.

**Declared result** set.

**Record and data access** read “Repost Item Valuation” via get\_all.

**Explicit results** set() · set of item\_code for item\_code drawn from items where item\_code.

**Local steps**

- If not entries\_in\_progress.
  - Return set().
- Set items from Platform.get\_all(“Repost Item Valuation”, filters = mapping(“name” → tuple(“in”, list(entries\_in\_progress))), pluck = “item\_code”).
- Return set of item\_code for item\_code drawn from items where item\_code.
  - Draw item\_code from items, keep a combination only if (item\_code).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L6914) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L436)

<a id="op-67c5f4cfcf767a"></a>
### Repost entries

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_entries`

**Inputs** no declared parameters.

**Record and data access** read “Stock Reposting Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”).
  - Return no value.
- If not in\_configured\_timeslot().
  - Return no value.
- Set riv\_entries from get\_repost\_item\_valuation\_entries().
- For each row in riv\_entries.
  - Evaluate execute\_reposting\_entry(row.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L7104) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L445)

<a id="op-54645159744020"></a>
### Execute reposting entry

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_execute_reposting_entry`

**Inputs** name, continue\_reposting = false.

**Local steps**

- Attempt the following.
  - Evaluate \_execute\_reposting\_entry(name).
- On exit, including pending return or failure.
  - If continue\_reposting.
    - Evaluate enqueue\_parallel\_reposting().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0801.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L431)

<a id="op-8067bc49caf7c3"></a>
### Execute reposting entry

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_execute_reposting_entry_2`

**Inputs** name.

**Record and data access** resolve a document from “Repost Item Valuation” via get\_doc · read “Repost Item Valuation” via get\_value.

**Explicit results** no value.

**Local steps**

- Set doc from Platform.get\_doc(“Repost Item Valuation”, name).
- If (doc.repost\_only\_accounting\_ledgers and doc.reposting\_reference and Platform.db.get\_value(“Repost Item Valuation”, doc.reposting\_reference, “status”) does not belong to list(“Completed”, “Skipped”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.repost\_only\_accounting\_ledgers → doc.reposting\_reference → Platform.db.get\_value(“Repost Item Valuation”, doc.reposting\_reference, “status”) does not belong to list(“Completed”, “Skipped”).
  - Return no value.
- If doc.status belongs to tuple(“Queued”, “In Progress”).
  - Evaluate repost(doc).
  - Evaluate doc.deduplicate\_similar\_repost().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0801.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L432)

<a id="op-cca43779717e4e"></a>
### Get repost item valuation entries

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_get_repost_item_valuation_entries`

**Inputs** limit = no value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set doctype from Platform.qb.DocType(“Repost Item Valuation”).
- Set query from nested operand in the contract(nested operand in the contract).orderby(CombineDatetime(nested operand in the contract.posting\_date, nested operand in the contract.posting\_time), order = nested operand in t ….
- If limit.
  - Set query from query.limit(cint(limit)).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0801.json#L350) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L438)

<a id="op-ab1fac781d2933"></a>
### In configured timeslot

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_in_configured_timeslot`

**Inputs** repost\_settings = no value, current\_time = no value.

**Record and data access** resolve a document from “Stock Reposting Settings” via get\_cached\_doc.

**Explicit results** true · end\_time ≥ now\_time ≥ start\_time · (now\_time ≥ start\_time or now\_time ≤ end\_time).

**Local steps**

- If repost\_settings is identical to no value.
  - Set repost\_settings from Platform.get\_cached\_doc(“Stock Reposting Settings”).
- If not repost\_settings.limit\_reposting\_timeslot.
  - Return true.
- If get\_weekday() equals repost\_settings.limits\_dont\_apply\_on.
  - Return true.
- Set start\_time from to\_timedelta(repost\_settings.start\_time).
- Set end\_time from to\_timedelta(repost\_settings.end\_time).
- Set now\_time from to\_timedelta((current\_time or nowtime())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in current\_time → nowtime().
- If start\_time &lt; end\_time.
  - Return end\_time ≥ now\_time ≥ start\_time.
    - Compare adjacent operands in order, stopping at the first false comparison in end\_time ≥ now\_time ≥ start\_time.
- Otherwise.
  - Return (now\_time ≥ start\_time or now\_time ≤ end\_time).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in now\_time ≥ start\_time → now\_time ≤ end\_time.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Stock Reposting Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L439)

<a id="op-65925f0732a59e"></a>
### Execute repost item valuation

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_execute_repost_item_valuation`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Stock Reposting Settings” via get\_single\_value · read “Scheduled Job Type” via get\_value · resolve a document from “Scheduled Job Type” via get\_doc.

**State and service calls** msgprint with translated “Reposting will start within the timeslot configured in {0}”.format(get\_link\_to\_form(“Stock Reposting Settings”, “Stock Reposting Settings”)).

**Explicit results** false · true.

**Local steps**

- Evaluate Platform.has\_permission(“Repost Item Valuation”, “write”, throw = true).
- If not in\_configured\_timeslot().
  - Evaluate Platform.msgprint(translated “Reposting will start within the timeslot configured in {0}”.format(get\_link\_to\_form(“Stock Reposting Settings”, “Stock Reposting Settings”))).
  - Return false.
- Set method from “Enterprise.stock.doctype.repost\_item\_valuation.repost\_item\_valuation.repost\_entries”.
- If Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”).
  - Set method from “Enterprise.stock.doctype.repost\_item\_valuation.repost\_item\_valuation.run\_parallel\_reposting”.
- If name bound to Platform.db.get\_value(“Scheduled Job Type”, mapping(“method” → method), “name”).
  - Evaluate Platform.get\_doc(“Scheduled Job Type”, name).enqueue(force = true).
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Repost Item Valuation”, “write”, throw = true) · configured or stored value from Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L430)

<a id="op-66d2330517d8d0"></a>
### Make reposting for accounting ledgers

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_make_reposting_for_accounting_ledgers`

**Inputs** transactions, company, repost\_doc.

**State and service calls** request new\_doc for “Repost Item Valuation” · call submit on new\_repost\_doc.

**Local steps**

- Set reposting\_map from get\_existing\_reposting\_only\_gl\_entries(repost\_doc.name).
- For each tuple(voucher\_type, voucher\_no) in transactions.
  - If reposting\_map.get(tuple(voucher\_type, voucher\_no)).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set new\_repost\_doc from Platform.new\_doc(“Repost Item Valuation”).
    - Set new\_repost\_doc.company from company.
    - Set new\_repost\_doc.voucher\_type from voucher\_type.
    - Set new\_repost\_doc.voucher\_no from voucher\_no.
    - Set new\_repost\_doc.repost\_only\_accounting\_ledgers from 1.
    - Set new\_repost\_doc.reposting\_reference from repost\_doc.name.
    - Set new\_repost\_doc.flags.ignore\_permissions from true.
    - Evaluate new\_repost\_doc.submit().
  - On failure (Exception).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L440)

<a id="op-b8595252243dd4"></a>
### Get existing reposting only gl entries

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_get_existing_reposting_only_general_ledger_entries`

**Inputs** reposting\_reference.

**Record and data access** read “Repost Item Valuation” via get\_all.

**Explicit results** Platform.\_dict() · reposting\_map.

**Local steps**

- Set existing\_reposting from Platform.get\_all(“Repost Item Valuation”, filters = mapping(“reposting\_reference” → reposting\_reference, “docstatus” → 1, “status” → “Queued”, “repost\_only\_accounting\_ledgers” → 1), fields = list(“repostin ….
- If not existing\_reposting.
  - Return Platform.\_dict().
- Set reposting\_map from mapping().
- For each d in existing\_reposting.
  - Set key from tuple(d.voucher\_type, d.voucher\_no).
  - Set reposting\_map at key from d.reposting\_reference.
- Return reposting\_map.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0801.json#L1887) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L435)

## Report · Reserved stock

<a id="op-14b2087d884427"></a>
### Execute

`operation_enterprise_stock_report_reserved_stock_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Evaluate validate\_filters(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0900.json#L2582) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L267)

<a id="op-d959a666233806"></a>
### Validate filters

`operation_enterprise_stock_report_reserved_stock_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “Please set filters” · validation helper — translated “Please set {0}”.format(field).

**Local steps**

- If not filters.
  - Call the validation error handler Platform.throw(translated “Please set filters”).
- For each field in list(“company”, “from\_date”, “to\_date”).
  - If not filters.get(field).
    - Call the validation error handler Platform.throw(translated “Please set {0}”.format(field)).
- Evaluate validate\_date\_range(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L270)

<a id="op-4620327035d4cf"></a>
### Get data

`operation_enterprise_stock_report_reserved_stock_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set query from Platform.qb.get\_query(“Stock Reservation Entry”, fields = list(sre.creation, sre.warehouse, sre.item\_code, sre.stock\_uom, …), ignore\_permissions = false).where(((sre.docstatus equals 1 bitwise and sre.comp ….
- For each field in list(“item\_code”, “warehouse”, “voucher\_type”, “voucher\_no”, …).
  - If value bound to filters.get(field).
    - Set query from query.where(sre at field equals value).
- If value bound to filters.get(“stock\_reservation\_entry”).
  - Set query from query.where(sre.name equals value).
- Set data from query.run(as\_list = true).
- Evaluate set\_available\_qty(data).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L269)

<a id="op-1b74aa8d31146a"></a>
### Set available qty

`operation_enterprise_binding_enterprise_stock_report_reserved_stock_reserved_stock_set_available_qty`

**Inputs** data.

**Explicit results** no value.

**Local steps**

- If not data.
  - Return no value.
- Set bin from Platform.qb.DocType(“Bin”).
- Set free\_qty from mapping of tuple(item\_code, warehouse) → (flt(actual\_qty) − flt(reserved\_stock)) for tuple(item\_code, warehouse, actual\_qty, reserved\_stock) drawn from nested operand in the contract.select(nested operand  ….
  - Draw tuple(item\_code, warehouse, actual\_qty, reserved\_stock) from nested operand in the contract(nested operand in the contract).select(bin.item\_code, bin.warehouse, bin.actual\_qty, bin.reserved\_stock).where((nested operand in the contract.item\_code.isin(set of nested op ….run().
  - Draw row from data.
  - Draw row from data.
- For each row in data.
  - Set row at AVAILABLE\_QTY\_INDEX from free\_qty.get(tuple(row at 2, row at 1), 0.0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L985)

<a id="op-da285e064ec008"></a>
### Get columns

`operation_enterprise_stock_report_reserved_stock_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype” → “Datetime”, “width” → 150), mapping(“fieldname” → “warehouse”, “label” → translated “Warehouse”, “fieldtype” → “Link”, “options ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L268)

## Service · Return charges

<a id="op-522407df58ab2c"></a>
### Return Charges Service.initialize

`operation_enterprise_binding_enterprise_stock_services_return_charges_returnchargesservice_init`

**Inputs** self, doc.

**Local steps**

- Set self.doc from doc.
- Set self.detail\_field from get\_return\_against\_item\_fields(doc.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1082)

<a id="op-dc884e3b9b5d07"></a>
### Return Charges Service.set returned valuation charges

`operation_enterprise_binding_enterprise_stock_services_return_charges_returnchargesservice_set_returned_valuation_charges`

**Inputs** self.

**Declared result** no value.

**Record and data access** resolve a document from doc.doctype via get\_doc.

**Explicit results** no value.

**Local steps**

- Set doc from self.doc.
- Set charges from get\_actual\_valuation\_charges(doc).
- If not (doc.is\_return and doc.return\_against and charges and self.is\_traced\_to\_original()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_return → doc.return\_against → charges → self.is\_traced\_to\_original().
  - Return no value.
- Set original from Platform.get\_doc(doc.doctype, doc.return\_against).
- Set original\_charges from mapping().
- For each tax in get\_actual\_valuation\_charges(original).
  - Evaluate original\_charges.setdefault(tuple(tax.account\_head, tax.description), list()).append(tax).
- Set returned\_qty from self.get\_returned\_qty\_by\_original\_row().
- For each tax in charges.
  - If same\_charges bound to original\_charges.get(tuple(tax.account\_head, tax.description)).
    - Set base\_share from self.get\_returned\_base\_share(original, same\_charges.pop(0), returned\_qty).
    - Set tax.tax\_amount from negative flt((base\_share ÷ doc.conversion\_rate), tax.precision(“tax\_amount”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is traced to original](operations-053.md#op-992b7556c04d16), [get returned qty by original row](operations-053.md#op-32ed375d2673ae), [get returned base share](operations-053.md#op-4eea4fa73a3fe4).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1084)

<a id="op-992b7556c04d16"></a>
### Return Charges Service.is traced to original

`operation_enterprise_binding_enterprise_stock_services_return_charges_returnchargesservice_is_traced_to_original`

**Inputs** self.

**Declared result** bool.

**Explicit results** all(generator of row.get(self.detail\_field) for row drawn from self.doc.get(“items”)).

**Local steps**

- Return all(generator of row.get(self.detail\_field) for row drawn from self.doc.get(“items”)).
  - Draw row from self.doc.get(“items”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1083)

<a id="op-32ed375d2673ae"></a>
### Return Charges Service.get returned qty by original row

`operation_enterprise_binding_enterprise_stock_services_return_charges_returnchargesservice_get_returned_qty_by_original_row`

**Inputs** self.

**Declared result** dict.

**Explicit results** returned\_qty.

**Local steps**

- Set returned\_qty from mapping().
- For each row in self.doc.get(“items”).
  - If row.get(“return\_qty\_from\_rejected\_warehouse”).
    - Set tuple(accepted, rejected) from tuple(0.0, negative get\_stock\_qty(row, row.qty)).
  - Otherwise.
    - Set tuple(accepted, rejected) from tuple(negative get\_stock\_qty(row, row.qty), negative get\_stock\_qty(row, row.rejected\_qty)).
  - Set qty from returned\_qty.setdefault(row.get(self.detail\_field), mapping(“accepted” → 0.0, “rejected” → 0.0)).
  - Update qty at “accepted” using + accepted.
  - Update qty at “rejected” using + rejected.
- Return returned\_qty.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1081)

<a id="op-4eea4fa73a3fe4"></a>
### Return Charges Service.get returned base share

`operation_enterprise_binding_enterprise_stock_services_return_charges_returnchargesservice_get_returned_base_share`

**Inputs** original, original\_charge, returned\_qty.

**Wrappers, in declaration order** staticmethod.

**Declared result** float.

**Explicit results** share.

**Local steps**

- Set items from list of row for row drawn from original.get(“items”) where row.item\_code.
  - Draw row from original.get(“items”), keep a combination only if (row.item\_code).
- If original\_charge.get(“allocate\_full\_amount\_to\_stock\_items”).
  - Set stock\_items from (original.get\_stock\_items() + original.get\_asset\_items()).
  - Set items from list of row for row drawn from items where row.item\_code belongs to stock\_items.
    - Draw row from items, keep a combination only if (row.item\_code belongs to stock\_items).
- Set charge\_per\_item from mapping().
- Evaluate original.\_spread\_charge\_over\_items(charge\_per\_item, flt(original\_charge.base\_tax\_amount), items).
- Set bills\_rejected from bills\_rejected\_quantity(original).
- Set share from 0.0.
- For each row in items.
  - Set qty from returned\_qty.get(row.name, mapping(“accepted” → 0.0, “rejected” → 0.0)).
  - If flt(row.qty).
    - Set carried\_qty from original.get\_valued\_stock\_qty(row).
    - Set returned from (qty at “accepted” + qty at “rejected” when bills\_rejected, otherwise 0.0).
      - Value choice on bills\_rejected — true gives qty at “rejected”, false gives 0.0.
  - Otherwise.
    - Set carried\_qty from get\_stock\_qty(row, row.rejected\_qty).
    - Set returned from qty at “rejected”.
  - If carried\_qty.
    - Update share using + ((charge\_per\_item.get(row.idx, 0.0) × returned) ÷ carried\_qty).
- Return share.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1080)

<a id="op-f5628c9ac61ffc"></a>
### Get actual valuation charges

`operation_enterprise_binding_enterprise_stock_services_return_charges_get_actual_valuation_charges`

**Inputs** doc.

**Declared result** list.

**Explicit results** list of tax for tax drawn from doc.get(“taxes”) where (tax.charge\_type equals “Actual” and tax.category belongs to tuple(“Valuation”, “Valuation and Total”)).

**Local steps**

- Return list of tax for tax drawn from doc.get(“taxes”) where (tax.charge\_type equals “Actual” and tax.category belongs to tuple(“Valuation”, “Valuation and Total”)).
  - Draw tax from doc.get(“taxes”), keep a combination only if ((tax.charge\_type equals “Actual” and tax.category belongs to tuple(“Valuation”, “Valuation and Total”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “Actual” → tax.category belongs to tuple(“Valuation”, “Valuation and Total”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1079)

## Record · Serial and batch bundle

[Record definition](../../../../data/record-types/serial_and_batch_bundle.json)

<a id="op-dbb39664aaccce"></a>
### Serialand Batch Bundle.autoname

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_autoname`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Naming Series is mandatory”.

**Local steps**

- If Platform.get\_single\_value(“Stock Settings”, “set\_serial\_and\_batch\_bundle\_naming\_based\_on\_naming\_series”).
  - If not self.naming\_series.
    - Call the validation error handler Platform.throw(translated “Naming Series is mandatory”).
  - Set naming\_series from self.naming\_series.
  - If “#” does not belong to naming\_series.
    - Update naming\_series using + “.#####”.
  - Set self.name from make\_autoname(self.naming\_series).
- Otherwise.
  - Attempt the following.
    - Set self.name from Platform.generate\_hash(length = 20).
  - On failure (Platform.DuplicateEntryError).
    - Evaluate self.autoname().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “set\_serial\_and\_batch\_bundle\_naming\_based\_on\_naming\_series”) · clock or generated value from Platform.generate\_hash(length = 20).

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0803.json#L7045) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L554)

<a id="op-597c7113ea3f71"></a>
### Serialand Batch Bundle.validate

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate self.validate\_allow\_to\_set\_serial\_batch().
- If (self.docstatus equals 1 and self.voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.voucher\_detail\_no.
  - Evaluate self.validate\_voucher\_detail\_no().
- Evaluate self.reset\_serial\_batch\_bundle().
- Evaluate self.set\_batch\_no().
- Evaluate self.validate\_serial\_and\_batch\_no().
- Evaluate self.validate\_duplicate\_serial\_and\_batch\_no().
- Evaluate self.validate\_voucher\_no().
- <a id="op-597c7113ea3f71-guard-12"></a>If self.type\_of\_transaction equals “Maintenance”.
  - Return no value.
- Evaluate self.allow\_existing\_serial\_nos().
- If self.docstatus equals 1.
  - If (not self.flags.ignore\_validate\_serial\_batch or Platform.in\_test).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.flags.ignore\_validate\_serial\_batch → Platform.in\_test.
    - Evaluate self.validate\_serial\_nos\_duplicate().
  - Evaluate self.check\_future\_entries\_exists().
- Otherwise.
  - If (self.has\_serial\_no and self.type\_of\_transaction equals “Outward” and self.voucher\_type differs from “Stock Reconciliation” and self.voucher\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_serial\_no → self.type\_of\_transaction equals “Outward” → self.voucher\_type differs from “Stock Reconciliation” → self.voucher\_no.
    - Evaluate self.validate\_serial\_no\_status().
- Evaluate self.set\_is\_outward().
- Evaluate self.calculate\_total\_qty(save = false).
- Evaluate self.set\_warehouse().
- If (self.voucher\_type differs from “Stock Entry” or not self.voucher\_no or self.docstatus equals 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.voucher\_type differs from “Stock Entry” → not self.voucher\_no → self.docstatus equals 1.
  - Evaluate self.set\_incoming\_rate().
- Evaluate self.calculate\_qty\_and\_amount().
- Evaluate self.set\_child\_details().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.type\_of\_transaction equals “Maintenance”, self.type\_of\_transaction = “Maintenance” selects the branch that returns no value. With self.type\_of\_transaction = “Inward”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-597c7113ea3f71-guard-12)

**Methods declared on this owner** [validate allow to set serial batch](operations-053.md#op-c1f1ccd78d60bd), [validate voucher detail no](operations-054.md#op-87656f4855e411), [reset serial batch bundle](operations-054.md#op-fd0ceda49fce6c), [set batch no](operations-054.md#op-076dccadcdaf5d), [validate serial and batch no](operations-055.md#op-a8084770ff6f10), [validate duplicate serial and batch no](operations-056.md#op-3a5f69366ce28e), [validate voucher no](operations-055.md#op-75e9b7aa0e3e14), [allow existing serial nos](operations-054.md#op-2261b001214a39), [validate serial nos duplicate](operations-054.md#op-2625422eb92b1b), [check future entries exists](operations-055.md#op-04fc2eda12163a), [validate serial no status](operations-053.md#op-98ba35b16a470f), [set is outward](operations-055.md#op-a6d3f40e6b7099), [calculate total qty](operations-054.md#op-6b200e57dfcd7e), [set warehouse](operations-055.md#op-36bc8706c404e8), [set incoming rate](operations-054.md#op-25f1bfa19f8d54), [calculate qty and amount](operations-055.md#op-156485bd00687a), [set child details](operations-056.md#op-04962d4e5f28d7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L599)

<a id="op-c1f1ccd78d60bd"></a>
### Serialand Batch Bundle.validate allow to set serial batch

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_allow_to_set_serial_batch`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Please check the 'Activate Serial and Batch No for Item' checkbox in the {0} to make Serial and Batch Bundle …”.format(get\_link\_to\_form(“Stock Settings”, “Stock Settings”)).

**Local steps**

- If not Platform.db.get\_single\_value(“Stock Settings”, “enable\_serial\_and\_batch\_no\_for\_item”).
  - Call the validation error handler Platform.throw(translated “Please check the 'Activate Serial and Batch No for Item' checkbox in the {0} to make Serial and Batch Bundle …”.format(get\_link\_to\_form(“Stock Settings”, “Stock Settings”)), titl ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “enable\_serial\_and\_batch\_no\_for\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0804.json#L654) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L956) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L600)

<a id="op-98ba35b16a470f"></a>
### Serialand Batch Bundle.validate serial no status

`operation_enterprise_stock_record_definitions_serial_and_batch_bundle_business_behavior_serialand_batch_bundle_validate_serial_number_status`

**Inputs** self.

**Record and data access** read “Serial No” via get\_all.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set serial\_nos from list of d.serial\_no for d drawn from self.entries where d.serial\_no.
  - Draw d from self.entries, keep a combination only if (d.serial\_no).
- Set invalid\_serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, serial\_nos), “warehouse” → tuple(“!=”, self.warehouse)), pluck = “name”).
- If invalid\_serial\_nos.
  - Set msg from translated “You cannot outward following {0} as either they are Delivered, Inactive or located in a different warehouse.”.format(translated “Serial Nos” when len(invalid\_serial\_nos) &gt; 1, otherwise translat ….
    - Value choice on len(invalid\_serial\_nos) &gt; 1 — true gives translated “Serial Nos”, false gives translated “Serial No”.
  - Update msg using + text in the contract.
  - Update msg using + “, ”.join(generator of sn for sn drawn from invalid\_serial\_nos).
    - Draw sn from invalid\_serial\_nos.
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L971) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L615)
