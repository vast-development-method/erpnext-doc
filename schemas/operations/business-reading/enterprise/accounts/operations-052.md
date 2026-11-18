# Accounting and settlement · operations 52

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Gross profit

<a id="op-0a50cd04568e9c"></a>
### Gross Profit Generator.load drop ship buying rates

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_load_drop_ship_buying_rates`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.drop\_ship\_buying\_rates from mapping().
- Set sales\_order\_items from set of row.so\_detail for row drawn from self.si\_list where (row.delivered\_by\_supplier and row.so\_detail).
  - Draw row from self.si\_list, keep a combination only if ((row.delivered\_by\_supplier and row.so\_detail)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.delivered\_by\_supplier → row.so\_detail.
- If not sales\_order\_items.
  - Return no value.
- Bind dependencies Sum.
- Set purchase\_order\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set purchase\_invoice\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set buying\_amounts from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise  ….
- For each row in buying\_amounts.
  - If flt(row.stock\_qty).
    - Set self.drop\_ship\_buying\_rates at row.sales\_order\_item from (flt(row.buying\_amount) ÷ flt(row.stock\_qty)).
- Evaluate self.load\_drop\_ship\_order\_rates((sales\_order\_items − set(self.drop\_ship\_buying\_rates))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [load drop ship order rates](operations-052.md#op-7460aa0008d742).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1029)

<a id="op-7460aa0008d742"></a>
### Gross Profit Generator.load drop ship order rates

`operation_enterprise_binding_enterprise_accounts_report_gross_profit_gross_profit_grossprofitgenerator_load_drop_ship_order_rates`

**Inputs** self, sales\_order\_items.

**Explicit results** no value.

**Local steps**

- If not sales\_order\_items.
  - Return no value.
- Bind dependencies Sum.
- Set purchase\_order\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set order\_amounts from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise  ….
- For each row in order\_amounts.
  - Set self.drop\_ship\_buying\_rates at row.sales\_order\_item from (flt(row.buying\_amount) ÷ flt(row.stock\_qty)) when flt(row.stock\_qty), otherwise 0.
    - Value choice on flt(row.stock\_qty) — true gives (flt(row.buying\_amount) ÷ flt(row.stock\_qty)), false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1218)

<a id="op-411d8554a99e64"></a>
### Gross Profit Generator.get drop ship buying amount

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_drop_ship_buying_amount`

**Inputs** self, row.

**Explicit results** no value · (flt(row.qty) × self.drop\_ship\_buying\_rates at row.so\_detail).

**Local steps**

- If row.so\_detail does not belong to self.drop\_ship\_buying\_rates.
  - Return no value.
- Return (flt(row.qty) × self.drop\_ship\_buying\_rates at row.so\_detail).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L6827) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1020)

<a id="op-79d6b5de94103f"></a>
### Gross Profit Generator.get buying amount from so dn

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_buying_amount_from_sales_order_record_name`

**Inputs** self, sales\_order, so\_detail, item\_code.

**Explicit results** flt(incoming\_amount at 0 at 0) when incoming\_amount, otherwise 0.

**Local steps**

- Bind dependencies Sum.
- Set delivery\_note\_item from Platform.qb.DocType(“Delivery Note Item”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.against\_sales\_order equals sales\_order).where(delivery\_note\_item.so\_detail equals so\_detail).groupby(deli ….
- Set incoming\_amount from query.run().
- Return flt(incoming\_amount at 0 at 0) when incoming\_amount, otherwise 0.
  - Value choice on incoming\_amount — true gives flt(incoming\_amount at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1018)

<a id="op-c33a86156cf4e3"></a>
### Gross Profit Generator.get average buying rate

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_average_buying_rate`

**Inputs** self, row, item\_code.

**Explicit results** self.average\_buying\_rate at key.

**Local steps**

- Set args from row.
- Set key from tuple(item\_code, row.warehouse, row.posting\_date, row.posting\_time, …).
- If key does not belong to self.average\_buying\_rate.
  - Evaluate args.update(mapping(“voucher\_type” → row.parenttype, “voucher\_no” → row.parent, “allow\_zero\_valuation” → true, “company” → self.filters.company, …)).
  - If row.serial\_and\_batch\_bundle.
    - Evaluate args.update(mapping(“serial\_and\_batch\_bundle” → row.serial\_and\_batch\_bundle)).
  - Set average\_buying\_rate from \_get\_incoming\_rate(args).
  - Set self.average\_buying\_rate at key from flt(average\_buying\_rate).
- Return self.average\_buying\_rate at key.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1013)

<a id="op-5b7d7a9260b173"></a>
### Gross Profit Generator.get last purchase rate

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_last_purchase_rate`

**Inputs** self, item\_code, row.

**Explicit results** flt(last\_purchase\_rate at 0 at 0) when last\_purchase\_rate, otherwise 0.

**Local steps**

- Set purchase\_invoice from Platform.qb.DocType(“Purchase Invoice”).
- Set purchase\_invoice\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.item\_code equals item\_code).where(purchase\_invoice.is\_return equals 0).where(purchase\_invoice\_item.parent ….
- If row.project.
  - Set query from query.where(purchase\_invoice\_item.project equals row.project).
- If row.cost\_center.
  - Set query from query.where(purchase\_invoice\_item.cost\_center equals row.cost\_center).
- Set query from query.orderby(purchase\_invoice.posting\_date, order = Platform.qb.desc).limit(1).
- Set last\_purchase\_rate from query.run().
- Return flt(last\_purchase\_rate at 0 at 0) when last\_purchase\_rate, otherwise 0.
  - Value choice on last\_purchase\_rate — true gives flt(last\_purchase\_rate at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1022)

<a id="op-75c4a6cfacf489"></a>
### Gross Profit Generator.load invoice items

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_load_invoice_items`

**Inputs** self.

**Local steps**

- Set self.si\_list from list().
- Set SalesInvoice from Platform.qb.DocType(“Sales Invoice”).
- Set base\_query from self.prepare\_invoice\_query().
- If self.filters.include\_returned\_invoices.
  - Set invoice\_query from base\_query.where((SalesInvoice.is\_return equals 0 bitwise or (SalesInvoice.is\_return equals 1 bitwise and SalesInvoice.return\_against.isnull()))).
- Otherwise.
  - Set invoice\_query from base\_query.where(SalesInvoice.is\_return equals 0).
- Update self.si\_list using + invoice\_query.run(as\_dict = true).
- Evaluate self.prepare\_vouchers\_to\_ignore().
- Set ret\_invoice\_query from base\_query.where((SalesInvoice.is\_return equals 1 bitwise and SalesInvoice.return\_against.isnotnull())).
- If self.vouchers\_to\_ignore.
  - Set ret\_invoice\_query from ret\_invoice\_query.where(SalesInvoice.return\_against.notin(self.vouchers\_to\_ignore)).
- Update self.si\_list using + ret\_invoice\_query.run(as\_dict = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare invoice query](operations-052.md#op-361aa205580679), [prepare vouchers to ignore](operations-052.md#op-77b6a777bfe4e9).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0258.json#L1464) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1030)

<a id="op-361aa205580679"></a>
### Gross Profit Generator.prepare invoice query

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_prepare_invoice_query`

**Inputs** self.

**Explicit results** query.

**Local steps**

- Set SalesInvoice from Platform.qb.DocType(“Sales Invoice”).
- Set SalesInvoiceItem from Platform.qb.DocType(“Sales Invoice Item”).
- Set Item from Platform.qb.DocType(“Item”).
- Set SalesTeam from Platform.qb.DocType(“Sales Team”).
- Set PaymentSchedule from Platform.qb.DocType(“Payment Schedule”).
- Set DeliveryNoteItem from Platform.qb.DocType(“Delivery Note Item”).
- Set query from nested operand in the contract(nested operand in the contract).left\_join(DeliveryNoteItem).on(DeliveryNoteItem.name equals SalesInvoiceItem.dn\_detail).where((SalesInvoice.docstatus equals 1 bitwise and Sal ….
- Set query from self.apply\_common\_filters(query, SalesInvoice, SalesInvoiceItem, SalesTeam, …).
- If match\_conditions bound to build\_match\_conditions(“Sales Invoice”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set query from query.select(SalesInvoiceItem.parenttype, SalesInvoiceItem.parent, SalesInvoice.posting\_date, SalesInvoice.posting\_time, …).
- If self.filters.group\_by equals “Sales Person”.
  - Set query from query.select(SalesTeam.sales\_person, ((SalesTeam.allocated\_percentage × SalesInvoiceItem.base\_net\_amount) ÷ 100).as\_(“allocated\_amount”), SalesTeam.incentives).
  - Set query from query.left\_join(SalesTeam).on(SalesTeam.parent equals SalesInvoice.name).
- If self.filters.group\_by equals “Payment Term”.
  - Set query from query.select(nested operand in the contract.when(nested operand in the contract equals nested operand in the contract, nested operand in the contract(nested operand in the contract)).else\_(Coalesce(Payment ….
  - Set query from query.left\_join(PaymentSchedule).on((PaymentSchedule.parent equals SalesInvoice.name bitwise and SalesInvoice.is\_return equals 0)).
- Set query from query.orderby(SalesInvoice.posting\_date, order = Order.desc).orderby(SalesInvoice.posting\_time, order = Order.desc).
- Return query.

**Methods declared on this owner** [apply common filters](operations-052.md#op-1964ba6ee9b05e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1033)

<a id="op-1964ba6ee9b05e"></a>
### Gross Profit Generator.apply common filters

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_apply_common_filters`

**Inputs** self, query, SalesInvoice, SalesInvoiceItem, SalesTeam, Item.

**Record and data access** read “DocType” via get\_cached\_value · read “Warehouse” via get\_value.

**Explicit results** query.

**Local steps**

- If self.filters.company.
  - Set query from query.where(SalesInvoice.company equals self.filters.company).
- If self.filters.from\_date.
  - Set query from query.where(SalesInvoice.posting\_date ≥ self.filters.from\_date).
- If self.filters.to\_date.
  - Set query from query.where(SalesInvoice.posting\_date ≤ self.filters.to\_date).
- If self.filters.item\_group.
  - Set query from query.where(get\_item\_group\_condition(self.filters.item\_group, Item)).
- If self.filters.sales\_person.
  - Set query from query.where(ExistsCriterion(nested operand in the contract(nested operand in the contract).select(1).where((SalesTeam.parent equals SalesInvoice.name bitwise and SalesTeam.sales\_person equals nested operan ….
- If self.filters.sales\_invoice.
  - Set query from query.where(SalesInvoice.name equals self.filters.sales\_invoice).
- If self.filters.item\_code.
  - Set query from query.where(SalesInvoiceItem.item\_code equals self.filters.item\_code).
- If self.filters.cost\_center.
  - Set self.filters.cost\_center from Platform.parse\_json(self.filters.get(“cost\_center”)).
  - Set self.filters.cost\_center from get\_cost\_centers\_with\_children(self.filters.cost\_center).
  - Set query from query.where(SalesInvoiceItem.cost\_center.isin(self.filters.cost\_center)).
- If self.filters.project.
  - Set self.filters.project from Platform.parse\_json(self.filters.get(“project”)).
  - Set query from query.where(SalesInvoiceItem.project.isin(self.filters.project)).
- For each dim in (get\_accounting\_dimensions(as\_list = false) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_accounting\_dimensions(as\_list = false) → list().
  - If self.filters.get(dim.fieldname).
    - If Platform.get\_cached\_value(“DocType”, dim.document\_type, “is\_tree”).
      - Set self.filters at dim.fieldname from get\_dimension\_with\_children(dim.document\_type, self.filters.get(dim.fieldname)).
    - Set query from query.where(SalesInvoiceItem at dim.fieldname.isin(self.filters at dim.fieldname)).
- If self.filters.warehouse.
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Warehouse”, self.filters.warehouse, list(“lft”, “rgt”)).
  - Set WH from Platform.qb.DocType(“Warehouse”).
  - Set query from query.where(SalesInvoiceItem.warehouse.isin(nested operand in the contract(nested operand in the contract).select(WH.name).where((WH.lft ≥ lft bitwise and WH.rgt ≤ rgt)))).
- Return query.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“DocType”, dim.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0258.json#L3327) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1011)

<a id="op-77b6a777bfe4e9"></a>
### Gross Profit Generator.prepare vouchers to ignore

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_prepare_vouchers_to_ignore`

**Inputs** self.

**Local steps**

- Set self.vouchers\_to\_ignore from tuple(generator of row at “parent” for row drawn from self.si\_list).
  - Draw row from self.si\_list.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0258.json#L4859) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1034)

<a id="op-c2af1304132507"></a>
### Gross Profit Generator.get delivery notes

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_delivery_notes`

**Inputs** self.

**Local steps**

- Set self.delivery\_notes from Platform.\_dict(mapping()).
- If self.si\_list.
  - Bind dependencies Sum.
  - Set invoices from list of x.parent for x drawn from self.si\_list.
    - Draw x from self.si\_list.
  - Set dni from qb.DocType(“Delivery Note Item”).
  - Set delivery\_notes from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
  - For each entry in delivery\_notes.
    - Set self.delivery\_notes at entry.si\_detail from entry.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0258.json#L4953) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1019)

<a id="op-4b415c684af2ab"></a>
### Gross Profit Generator.group items by invoice

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_group_items_by_invoice`

**Inputs** self.

**Local steps**

- Set grouped from OrderedDict().
- Set product\_bundles from self.product\_bundles.get(“Sales Invoice”, mapping()).
- For each row in self.si\_list.
  - Evaluate grouped.setdefault(row.parent, list(self.get\_invoice\_row(row))).append(row.update(mapping(“indent” → 1.0, “parent\_invoice” → row.parent, “invoice\_or\_item” → row.item\_code))).
  - If bundled\_items bound to product\_bundles.get(row.parent, mapping()).get(row.item\_code).
    - For each x in bundled\_items.
      - Set bundle\_item from self.get\_bundle\_item\_row(row, x).
      - Evaluate grouped.get(row.parent).append(bundle\_item).
- Evaluate self.si\_list.clear().
- For each items in grouped.values().
  - Evaluate self.si\_list.extend(items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get invoice row](operations-052.md#op-f3696fa0907c9b), [get bundle item row](operations-052.md#op-74e5fccd030de5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0258.json#L5448) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1026)

<a id="op-f3696fa0907c9b"></a>
### Gross Profit Generator.get invoice row

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_invoice_row`

**Inputs** self, row.

**Explicit results** Platform.\_dict(mapping(“parent\_invoice” → empty text, “indent” → 0.0, “invoice\_or\_item” → row.parent, “parent” → no value, …)).

**Local steps**

- Return Platform.\_dict(mapping(“parent\_invoice” → empty text, “indent” → 0.0, “invoice\_or\_item” → row.parent, “parent” → no value, …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1021)

<a id="op-74e5fccd030de5"></a>
### Gross Profit Generator.get bundle item row

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_bundle_item_row`

**Inputs** self, row, item.

**Explicit results** Platform.\_dict(mapping(“parent\_invoice” → row.item\_code, “parenttype” → row.parenttype, “indent” → (row.indent + 1), “parent” → no value, …)).

**Local steps**

- Return Platform.\_dict(mapping(“parent\_invoice” → row.item\_code, “parenttype” → row.parenttype, “indent” → (row.indent + 1), “parent” → no value, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.warehouse → row.warehouse.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0258.json#L6421) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1015)

<a id="op-2f2ee4eee17c34"></a>
### Gross Profit Generator.get stock ledger entries

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_stock_ledger_entries`

**Inputs** self, item\_code, warehouse.

**Explicit results** self.sle at tuple(item\_code, warehouse) · list().

**Local steps**

- If (item\_code and warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_code → warehouse.
  - If tuple(item\_code, warehouse) does not belong to self.sle.
    - Set sle from qb.DocType(“Stock Ledger Entry”).
    - Set res from nested operand in the contract(nested operand in the contract).orderby(sle.item\_code).orderby(sle.warehouse, sle.posting\_datetime, sle.creation, order = Order.desc).run(as\_dict = true).
    - Set self.sle at tuple(item\_code, warehouse) from res.
  - Return self.sle at tuple(item\_code, warehouse).
- Return list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0259.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1025)

<a id="op-c91a3e47163ed3"></a>
### Gross Profit Generator.load product bundle

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_load_product_bundle`

**Inputs** self.

**Local steps**

- Set self.product\_bundles from mapping().
- Set pki from qb.DocType(“Packed Item”).
- Set pki\_query from nested operand in the contract.qb.from\_(pki).select(pki.parenttype, pki.parent, pki.parent\_item, pki.item\_code, …).where(pki.docstatus equals 1).
- For each d in pki\_query.run(as\_dict = true).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).setdefault(d.parent, nested operand in the contract.\_dict()).setdefault(d.parent\_item, list()).append(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0259.json#L529) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1032)

<a id="op-06f8cc7506f608"></a>
### Gross Profit Generator.load bundle deliveries

`operation_enterprise_binding_enterprise_accounts_report_gross_profit_gross_profit_grossprofitgenerator_load_bundle_deliveries`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.bundle\_deliveries from mapping().
- Set invoices from set of row.parent for row drawn from self.si\_list.
  - Draw row from self.si\_list.
- If not invoices.
  - Return no value.
- Set dni from qb.DocType(“Delivery Note Item”).
- Set delivered\_rows from nested operand in the contract(nested operand in the contract).select(dni.name, dni.parent, dni.item\_code, dni.stock\_qty, …).where(((nested operand in the contract.docstatus equals 1 bitwise and nested ope ….
- Set delivery\_note\_bundles from self.product\_bundles.get(“Delivery Note”, mapping()).
- For each delivered\_row in delivered\_rows.
  - If packed\_items bound to delivery\_note\_bundles.get(delivered\_row.parent, mapping()).get(delivered\_row.item\_code).
    - Evaluate self.bundle\_deliveries.setdefault(delivered\_row.si\_detail, list()).append(tuple(delivered\_row, packed\_items)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1217)

<a id="op-2c157d1a2d5d2b"></a>
### Gross Profit Generator.load non stock items

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_load_non_stock_items`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Local steps**

- Set self.non\_stock\_items from Platform.get\_all(“Item”, filters = mapping(“is\_stock\_item” → 0), pluck = “name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0259.json#L1008) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1031)

## Report · Inactive sales items

<a id="op-82967992f061a4"></a>
### Execute

`operation_enterprise_accounts_report_inactive_sales_items_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0262.json#L870) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1071)

<a id="op-14da257b8bff6e"></a>
### Get columns

`operation_enterprise_accounts_report_inactive_sales_items_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “territory”, “fieldtype” → “Link”, “label” → translated “Territory”, “options” → “Territory”, …), mapping(“fieldname” → “item\_group”, “fieldtype” → “Link”, “label” → translated “ ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0262.json#L969) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1072)

<a id="op-7f393f6019ce60"></a>
### Get data

`operation_enterprise_accounts_report_inactive_sales_items_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set items from get\_items(filters).
- Set territories from get\_territories(filters).
- Set last\_sales from get\_sales\_details(filters).
- For each territory in territories.
  - Set subtree from set(territory.name, expanded get\_descendants\_of(“Territory”, territory.name, ignore\_permissions = true)).
  - For each item in items.
    - Set row from mapping(“territory” → territory.name, “item\_group” → item.item\_group, “item” → item.item\_code, “item\_name” → item.item\_name).
    - Set last\_sale from get\_last\_sale(last\_sales, item.item\_code, subtree).
    - If last\_sale.
      - If last\_sale.days\_since\_last\_order ≤ cint(filters at “days”).
        - Continue with the next iteration or loop test.
      - Evaluate row.update(mapping(“customer” → last\_sale.customer, “last\_order\_date” → last\_sale.last\_order\_date, “qty” → last\_sale.qty, “days\_since\_last\_order” → last\_sale.days\_since\_last\_order)).
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1073)

<a id="op-c54c7b3e514c9c"></a>
### Get last sale

`operation_enterprise_binding_enterprise_accounts_report_inactive_sales_items_inactive_sales_items_get_last_sale`

**Inputs** last\_sales, item\_code, territories.

**Declared result** (dict bitwise or no value).

**Explicit results** min(sales, key = deferred anonymous expression, default = no value).

**Local steps**

- Set sales from generator of last\_sales at tuple(item\_code, t) for t drawn from territories where tuple(item\_code, t) belongs to last\_sales.
  - Draw t from territories, keep a combination only if (tuple(item\_code, t) belongs to last\_sales).
- Return min(sales, key = deferred anonymous expression, default = no value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1219)

<a id="op-8c8040d0d4e58a"></a>
### Get sales details

`operation_enterprise_accounts_report_inactive_sales_items_business_behavior_get_sales_details`

**Inputs** filters.

**Explicit results** item\_details\_map.

**Explicit failure paths** validation helper — translated “Invalid value {0} for 'Based On'”.format(filters at “based\_on”).

**Local steps**

- Set item\_details\_map from mapping().
- If filters at “based\_on” does not belong to tuple(“Sales Order”, “Sales Invoice”).
  - Call the validation error handler Platform.throw(translated “Invalid value {0} for 'Based On'”.format(filters at “based\_on”)).
- Set parent from Platform.qb.DocType(filters at “based\_on”).
- Set child\_doctype from “Sales Order Item” when filters at “based\_on” equals “Sales Order”, otherwise “Sales Invoice Item”.
  - Value choice on filters at “based\_on” equals “Sales Order” — true gives “Sales Order Item”, false gives “Sales Invoice Item”.
- Set child from Platform.qb.DocType(child\_doctype).
- Set date\_diff from CustomFunction(“DATEDIFF”, list(“d1”, “d2”)).
- Set current\_date from CustomFunction(“CURRENT\_DATE”, list()).
- Set date\_col from parent.transaction\_date when filters at “based\_on” equals “Sales Order”, otherwise parent.posting\_date.
  - Value choice on filters at “based\_on” equals “Sales Order” — true gives parent.transaction\_date, false gives parent.posting\_date.
- Set days\_since\_last\_order from date\_diff(current\_date(), date\_col).
- Set query from nested operand in the contract(nested operand in the contract).select(parent.territory, parent.customer, child.item\_group, child.item\_code, …).where(parent.docstatus equals 1).orderby(days\_since\_last\_order).
- If filters at “based\_on” equals “Sales Invoice”.
  - Set query from query.where(parent.is\_return equals 0).
- Set sales\_data from query.run(as\_dict = true).
- For each d in sales\_data.
  - Evaluate item\_details\_map.setdefault(tuple(d.item\_code, d.territory), d).
- Return item\_details\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1075)

<a id="op-c3316f74031260"></a>
### Get territories

`operation_enterprise_accounts_report_inactive_sales_items_business_behavior_get_territories`

**Inputs** filters.

**Record and data access** read “Territory” via get\_all.

**Explicit results** territories.

**Local steps**

- Set filter\_dict from mapping().
- If filters.get(“territory”).
  - Evaluate filter\_dict.update(mapping(“name” → filters at “territory”)).
- Set territories from Platform.get\_all(“Territory”, fields = list(“name”), filters = filter\_dict).
- Return territories.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0262.json#L3070) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1076)
