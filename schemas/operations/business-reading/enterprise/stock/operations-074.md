# Inventory and warehouses · operations 74

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock balance

<a id="op-7ef1dfef577068"></a>
### Get indented qty

`operation_enterprise_stock_stock_balance_business_behavior_get_indented_quantity`

**Inputs** item\_code, warehouse.

**Explicit results** (flt(quantities at 0 at 0) − flt(quantities at 0 at 1)) when quantities, otherwise 0.

**Local steps**

- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Set mr from Platform.qb.DocType(“Material Request”).
- Set base\_conditions from ((((mr\_item.item\_code equals item\_code bitwise and mr\_item.warehouse equals warehouse) bitwise and mr\_item.stock\_qty &gt; mr\_item.ordered\_qty) bitwise and mr.status differs from “Stopped”) bitwise and mr.docs ….
- Set pending\_qty from (mr\_item.stock\_qty − mr\_item.ordered\_qty).
- Set inward\_types from list(“Purchase”, “Manufacture”, “Customer Provided”, “Material Transfer”, …).
- Set quantities from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract(nested operand in the contract)), Sum(nested operand in the contract(nested operand in the contract) ….run().
- Return (flt(quantities at 0 at 0) − flt(quantities at 0 at 1)) when quantities, otherwise 0.
  - Value choice on quantities — true gives (flt(quantities at 0 at 0) − flt(quantities at 0 at 1)), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L697)

<a id="op-592108a7df8037"></a>
### Get ordered qty

`operation_enterprise_stock_stock_balance_business_behavior_get_ordered_quantity`

**Inputs** item\_code, warehouse.

**Explicit results** (flt(purchase\_order\_qty) + flt(subcontracting\_order\_qty)).

**Local steps**

- Set precision from get\_whole\_number\_qty\_precision(item\_code).
- Set purchase\_order\_qty from get\_purchase\_order\_qty(item\_code, warehouse, precision).
- Set subcontracting\_order\_qty from get\_subcontracting\_order\_qty(item\_code, warehouse, precision).
- Return (flt(purchase\_order\_qty) + flt(subcontracting\_order\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L698)

<a id="op-e933960d33d572"></a>
### Get whole number qty precision

`operation_enterprise_binding_enterprise_stock_stock_balance_get_whole_number_qty_precision`

**Inputs** item\_code.

**Record and data access** read “Item” via get\_cached\_value · read “UOM” via get\_cached\_value.

**Explicit results** Platform.get\_precision(“Bin”, “ordered\_qty”).

**Local steps**

- Set stock\_uom from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”).
- If (stock\_uom and Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stock\_uom → Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”).
  - Return Platform.get\_precision(“Bin”, “ordered\_qty”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, “stock\_uom”), Platform.get\_cached\_value(“UOM”, stock\_uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1085)

<a id="op-8e56d999470f04"></a>
### Get purchase order qty

`operation_enterprise_stock_stock_balance_business_behavior_get_purchase_order_quantity`

**Inputs** item\_code, warehouse, precision = no value.

**Explicit results** purchase\_order\_qty at 0 at 0 when purchase\_order\_qty, otherwise 0.

**Local steps**

- Set PurchaseOrder from Platform.qb.DocType(“Purchase Order”).
- Set PurchaseOrderItem from Platform.qb.DocType(“Purchase Order Item”).
- Set pending\_qty from ((PurchaseOrderItem.qty − PurchaseOrderItem.received\_qty) × PurchaseOrderItem.conversion\_factor).
- If precision is distinct from no value.
  - Set pending\_qty from Round(pending\_qty, precision).
- Set purchase\_order\_qty from nested operand in the contract(nested operand in the contract).select(Sum(pending\_qty)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in th ….run().
- Return purchase\_order\_qty at 0 at 0 when purchase\_order\_qty, otherwise 0.
  - Value choice on purchase\_order\_qty — true gives purchase\_order\_qty at 0 at 0, false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L700)

<a id="op-2970ee9aa6d7ac"></a>
### Get subcontracting order qty

`operation_enterprise_stock_stock_balance_business_behavior_get_subcontracting_order_quantity`

**Inputs** item\_code, warehouse, precision = no value.

**Explicit results** subcontracting\_order\_qty at 0 at 0 when subcontracting\_order\_qty, otherwise 0.

**Local steps**

- Set SubcontractingOrder from Platform.qb.DocType(“Subcontracting Order”).
- Set SubcontractingOrderItem from Platform.qb.DocType(“Subcontracting Order Item”).
- Set pending\_qty from ((SubcontractingOrderItem.qty − SubcontractingOrderItem.received\_qty) × SubcontractingOrderItem.conversion\_factor).
- If precision is distinct from no value.
  - Set pending\_qty from Round(pending\_qty, precision).
- Set subcontracting\_order\_qty from nested operand in the contract(nested operand in the contract).select(Sum(pending\_qty)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in th ….run().
- Return subcontracting\_order\_qty at 0 at 0 when subcontracting\_order\_qty, otherwise 0.
  - Value choice on subcontracting\_order\_qty — true gives subcontracting\_order\_qty at 0 at 0, false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L702)

<a id="op-7ef5b9fb24b2fe"></a>
### Get planned qty

`operation_enterprise_stock_stock_balance_business_behavior_get_planned_quantity`

**Inputs** item\_code, warehouse.

**Explicit results** flt(planned\_qty at 0 at 0) when planned\_qty, otherwise 0.

**Local steps**

- Set wo from Platform.qb.DocType(“Work Order”).
- Set planned\_qty from nested operand in the contract(nested operand in the contract).select(Sum((nested operand in the contract − nested operand in the contract))).where(((((nested operand in the contract bitwise and nested ope ….run().
- Return flt(planned\_qty at 0 at 0) when planned\_qty, otherwise 0.
  - Value choice on planned\_qty — true gives flt(planned\_qty at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L699)

<a id="op-eee14993898428"></a>
### Update bin qty

`operation_enterprise_stock_stock_balance_business_behavior_update_bin_quantity`

**Inputs** item\_code, warehouse, qty\_dict = no value.

**Local steps**

- Bind dependencies update\_bin\_columns.
- Bind dependencies get\_bin.
- Set bin from get\_bin(item\_code, warehouse).
- Set changed\_values from mapping of field → flt(value) for tuple(field, value) drawn from qty\_dict.items() where flt(bin.get(field)) differs from flt(value).
  - Draw tuple(field, value) from qty\_dict.items(), keep a combination only if (flt(bin.get(field)) differs from flt(value)).
- If changed\_values.
  - Evaluate update\_bin\_columns(bin.name, changed\_values).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L707)

<a id="op-c03fd860af68dc"></a>
### Set stock balance as per serial no

`operation_enterprise_stock_stock_balance_business_behavior_set_stock_balance_as_per_serial_number`

**Inputs** item\_code = no value, posting\_date = no value, posting\_time = no value, fiscal\_year = no value.

**Record and data access** execute query text (SELECT, Serial No) · execute query text (SELECT, Stock Ledger Entry) · resolve a document from sle\_dict via get\_doc.

**State and service calls** execute a supplied database query · call insert on sle\_doc.

**Local steps**

- If not posting\_date.
  - Set posting\_date from nowdate().
- If not posting\_time.
  - Set posting\_time from nowtime().
- Set condition from (“ and item.name=%s” modulo or format Platform.db.escape(item\_code, percent = false)) when item\_code, otherwise empty text.
  - Value choice on item\_code — true gives (“ and item.name=%s” modulo or format Platform.db.escape(item\_code, percent = false)), false gives empty text.
- Set bin from Platform.db.sql((query text (SELECT, Bin) modulo or format condition)).
- For each d in bin.
  - Set serial\_nos from Platform.db.sql(query text (SELECT, Serial No), tuple(d at 0, d at 1)).
  - Set sle from Platform.db.sql(query text (SELECT, Stock Ledger Entry), tuple(d at 0, d at 1)).
  - Set sle\_dict from mapping(“doctype” → “Stock Ledger Entry”, “item\_code” → d at 0, “warehouse” → d at 1, “transaction\_date” → nowdate(), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (sle and flt(serial\_nos at 0 at 0) &gt; flt(d at 2) and flt(sle at 0 at 0)) → 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle → flt(serial\_nos at 0 at 0) &gt; flt(d at 2) → flt(sle at 0 at 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (sle and cstr(sle at 0 at 1)) → 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle → cstr(sle at 0 at 1).
  - Set sle\_doc from Platform.get\_doc(sle\_dict).
  - Set sle\_doc.flags.ignore\_validate from true.
  - Set sle\_doc.flags.ignore\_links from true.
  - Evaluate sle\_doc.insert().
  - Set args from sle\_dict.copy().
  - Evaluate args.update(mapping(“sle\_id” → sle\_doc.name)).
  - Evaluate create\_repost\_item\_valuation\_entry(mapping(“item\_code” → d at 0, “warehouse” → d at 1, “posting\_date” → posting\_date, “posting\_time” → posting\_time)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L706)

## Record · Stock closing entry

[Record definition](../../../../data/record-types/stock_closing_entry.json)

<a id="op-39fec321d231bd"></a>
### Apply unscoped filters

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_apply_unscoped_filters`

**Inputs** filters.

**Explicit results** filters.

**Local steps**

- Set meta from Platform.get\_meta(“Stock Closing Entry”).
- For each fieldname in SCOPE\_FIELDS.
  - If meta.has\_field(fieldname).
    - Set filters at fieldname from tuple(“is”, “not set”).
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L5747) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L725)

<a id="op-de19330cb4c842"></a>
### Get closing entry for closed period

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_get_closing_entry_for_closed_period`

**Inputs** company.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit results** no value · \_get\_completed\_closing\_entry(company, str(closed\_upto)).

**Local steps**

- Set closed\_upto from Platform.db.get\_value(“Period Closing Voucher”, mapping(“docstatus” → 1, “company” → company), list(mapping(“MAX” → “period\_end\_date”))).
- If not closed\_upto.
  - Return no value.
- Return \_get\_completed\_closing\_entry(company, str(closed\_upto)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L5889) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L726)

<a id="op-88ba6ca0b64421"></a>
### Mark closing entries outdated

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_mark_closing_entries_outdated`

**Inputs** company, posting\_date.

**Record and data access** read “Stock Closing Entry” via get\_values.

**State and service calls** request set\_value on “Stock Closing Entry”.

**Local steps**

- Set names from Platform.db.get\_values(“Stock Closing Entry”, mapping(“company” → company, “docstatus” → 1, “status” → “Completed”, “to\_date” → tuple(“&gt;=”, posting\_date)), “name”, for\_update = true, skip\_locked = true, pl ….
- For each name in names.
  - Evaluate Platform.db.set\_value(“Stock Closing Entry”, name, “status”, “Outdated”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L606)

<a id="op-9bc56487e07889"></a>
### Has closing entry to coordinate

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_has_closing_entry_to_coordinate`

**Inputs** company, posting\_date.

**Record and data access** read “Stock Closing Entry” via exists.

**Explicit results** Platform.db.exists(“Stock Closing Entry”, mapping(“company” → company, “docstatus” → 1, “status” → tuple(“in”, list(“Queued”, “In Progress”, “Completed”)), “to\_date” → tuple(“&gt;=”, posting\_date))).

**Local steps**

- Return Platform.db.exists(“Stock Closing Entry”, mapping(“company” → company, “docstatus” → 1, “status” → tuple(“in”, list(“Queued”, “In Progress”, “Completed”)), “to\_date” → tuple(“&gt;=”, posting\_date))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L603)

<a id="op-13dcde10f01b45"></a>
### Lock company for closing

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_lock_company_for_closing`

**Inputs** company.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Evaluate Platform.db.get\_value(“Company”, company, “name”, for\_update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L605)

<a id="op-a4f9851b199418"></a>
### Get completed closing entry

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_get_completed_closing_entry`

**Inputs** company, closed\_upto.

**Wrappers, in declaration order** request\_cache.

**Record and data access** read “Stock Closing Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Closing Entry”, filters, list(“name”, “to\_date”), order\_by = “to\_date desc”, as\_dict = true).

**Local steps**

- Set filters from apply\_unscoped\_filters(mapping(“company” → company, “docstatus” → 1, “status” → “Completed”, “to\_date” → tuple(“&lt;=”, closed\_upto))).
- Return Platform.db.get\_value(“Stock Closing Entry”, filters, list(“name”, “to\_date”), order\_by = “to\_date desc”, as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L6079) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L727)

<a id="op-7eadfc2bacd4e8"></a>
### Stock Closing Entry.on discard

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L6302) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L734)

<a id="op-7a317d2d8da88d"></a>
### Stock Closing Entry.before save

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-074.md#op-fc833c3b850b9a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L6365) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L729)

<a id="op-fc833c3b850b9a"></a>
### Stock Closing Entry.set status

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_set_status`

**Inputs** self, save = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.status from “Queued”.
- <a id="op-fc833c3b850b9a-guard-3"></a>If self.docstatus equals 2.
  - Set self.status from “Cancelled”.
- <a id="op-fc833c3b850b9a-guard-6"></a>If self.docstatus equals 0.
  - Set self.status from “Draft”.
- If save.
  - Evaluate self.db\_set(“status”, self.status).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 2, self.docstatus = 2 (cancelled) selects the branch that assigns “Cancelled” to self.status. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fc833c3b850b9a-guard-3)
- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that assigns “Draft” to self.status. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fc833c3b850b9a-guard-6)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L6416) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L738)

<a id="op-b2bd59522b1467"></a>
### Stock Closing Entry.validate

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_to\_date().
- Evaluate self.set\_from\_date().
- Evaluate self.validate\_duplicate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate to date](operations-074.md#op-159de1c75ba455), [set from date](operations-074.md#op-58a737ba5f5adf), [validate duplicate](operations-074.md#op-9cedd93ff71e76).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L739)

<a id="op-159de1c75ba455"></a>
### Stock Closing Entry.validate to date

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_validate_to_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “To Date cannot be a future date”.

**Local steps**

- If (self.to\_date and getdate(self.to\_date) &gt; getdate(nowdate())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.to\_date → getdate(self.to\_date) &gt; getdate(nowdate()).
  - Call the validation error handler Platform.throw(translated “To Date cannot be a future date”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L621)

<a id="op-58a737ba5f5adf"></a>
### Stock Closing Entry.set from date

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_set_from_date`

**Inputs** self.

**Record and data access** read “Stock Closing Entry” via get\_value · read “Stock Ledger Entry” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “To Date is mandatory” · validation helper — translated “To Date must be after {0}, the To Date of the last Stock Closing Entry {1}”.format(Platform.bold(Platform.format(previous.to\_date, “Date”)), get\_link\_to\_form(“Stock Closing Entry”, previous.name)).

**Local steps**

- If not self.to\_date.
  - Call the validation error handler Platform.throw(translated “To Date is mandatory”).
- Set previous from Platform.db.get\_value(“Stock Closing Entry”, mapping(“company” → self.company, “docstatus” → 1, “name” → tuple(“!=”, self.name)), list(“name”, “to\_date”), order\_by = “to\_date desc”, as\_dict = true).
- If previous.
  - If getdate(previous.to\_date) ≥ getdate(self.to\_date).
    - Call the validation error handler Platform.throw(translated “To Date must be after {0}, the To Date of the last Stock Closing Entry {1}”.format(Platform.bold(Platform.format(previous.to\_date, “Date”)), get\_link\_to\_form(“Stock Closing Entry ….
  - Set self.from\_date from add\_days(previous.to\_date, 1).
  - Return no value.
- Set first\_posting\_date from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“company” → self.company, “is\_cancelled” → 0, “docstatus” → 1), list(mapping(“MIN” → “posting\_date”))).
- Set self.from\_date from (first\_posting\_date or self.to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in first\_posting\_date → self.to\_date.
- If getdate(self.from\_date) &gt; getdate(self.to\_date).
  - Set self.from\_date from self.to\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L616)

<a id="op-9cedd93ff71e76"></a>
### Stock Closing Entry.validate duplicate

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_validate_duplicate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Stock Closing Entry {0} already exists for the selected date range”.format(name).

**Local steps**

- Set table from Platform.qb.DocType(“Stock Closing Entry”).
- Set query from nested operand in the contract.qb.from\_(table).select(table.name).where(((table.docstatus equals 1 bitwise and table.company equals self.company) bitwise and ((nested operand in the contract.from\_date.betw ….
- For each fieldname in SCOPE\_FIELDS.
  - If self.get(fieldname).
    - Set query from query.where(table at fieldname equals self.get(fieldname)).
- Set query from query.run(as\_dict = true).
- If (query and query at 0.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in query → query at 0.name.
  - Set name from get\_link\_to\_form(“Stock Closing Entry”, query at 0.name).
  - Call the validation error handler Platform.throw(translated “Stock Closing Entry {0} already exists for the selected date range”.format(name), title = translated “Duplicate Stock Closing Entry”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L741)

<a id="op-ccbafb961a416b"></a>
### Stock Closing Entry.on submit

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(save = true).
- Evaluate self.enqueue\_job().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-074.md#op-fc833c3b850b9a), [enqueue job](operations-075.md#op-fba9c1d9fb1469).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L7198) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L735)

<a id="op-5cf3045d7555b3"></a>
### Stock Closing Entry.before cancel

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_later\_closing\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate later closing entry](operations-075.md#op-1b4d0d97fed46f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L610)

<a id="op-425553e0ba9a5d"></a>
### Stock Closing Entry.on cancel

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_closed\_period\_lock().
- Evaluate self.set\_status(save = true).
- Evaluate self.remove\_stock\_closing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate closed period lock](operations-075.md#op-a739ffc49ae5e2), [set status](operations-074.md#op-fc833c3b850b9a), [remove stock closing](operations-075.md#op-eb12d28d6dffbf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L7280) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L733)
