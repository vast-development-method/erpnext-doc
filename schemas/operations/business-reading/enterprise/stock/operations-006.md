# Inventory and warehouses · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Delayed item report

<a id="op-9c8966c488553c"></a>
### Delayed Item Report.initialize

`operation_enterprise_stock_report_delayed_item_report_business_behavior_delayed_item_report_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L6389) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L111)

<a id="op-26a41bb05db123"></a>
### Delayed Item Report.run

`operation_enterprise_stock_report_delayed_item_report_business_behavior_delayed_item_report_run`

**Inputs** self.

**Explicit results** tuple(self.get\_columns(), (self.get\_data() or list())).

**Local steps**

- Return tuple(self.get\_columns(), (self.get\_data() or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_data() → list().

**Methods declared on this owner** [get columns](operations-006.md#op-ad7032f73104af), [get data](operations-006.md#op-3b639a7481cfd6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L6473) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L112)

<a id="op-3b639a7481cfd6"></a>
### Delayed Item Report.get data

`operation_enterprise_stock_report_delayed_item_report_business_behavior_delayed_item_report_get_data`

**Inputs** self, consolidated = false.

**Explicit results** self.transactions.

**Local steps**

- Set doctype from self.filters.get(“based\_on”).
- Set sales\_order\_field from “sales\_order” when doctype equals “Sales Invoice”, otherwise “against\_sales\_order”.
  - Value choice on doctype equals “Sales Invoice” — true gives “sales\_order”, false gives “against\_sales\_order”.
- Set parent from Platform.qb.DocType(doctype).
- Set child from Platform.qb.DocType(formatted text {doctype} Item).
- Set query from nested operand in the contract(nested operand in the contract).from\_(parent).select(child.item\_code, child.item\_name, child.item\_group, child.qty, …).where((((((nested operand in the contract equals nested ….
- If doctype equals “Sales Invoice”.
  - Set query from query.where((parent.update\_stock equals 1 bitwise and parent.is\_pos equals 0)).
- If item\_group bound to self.filters.get(“item\_group”).
  - Set query from query.where(child.item\_group.isin(get\_group\_and\_descendants(“Item Group”, item\_group))).
- If customer\_group bound to self.filters.get(“customer\_group”).
  - Set query from query.where(parent.customer\_group.isin(get\_group\_and\_descendants(“Customer Group”, customer\_group))).
- If self.filters.get(“sales\_order”).
  - Set query from query.where(child at sales\_order\_field equals self.filters.get(“sales\_order”)).
- For each field in tuple(“customer”, “company”).
  - If self.filters.get(field).
    - Set query from query.where(parent at field equals self.filters.get(field)).
- Set self.transactions from query.run(as\_dict = true).
- If self.transactions.
  - Evaluate self.filter\_transactions\_data(consolidated).
  - Set self.transactions from list of row for row drawn from self.transactions where row.delayed\_days &gt; 0.
    - Draw row from self.transactions, keep a combination only if (row.delayed\_days &gt; 0).
  - Return self.transactions.

If control reaches the end, it returns no value.

**Methods declared on this owner** [filter transactions data](operations-006.md#op-2e483dea9392c3).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L110)

<a id="op-2e483dea9392c3"></a>
### Delayed Item Report.filter transactions data

`operation_enterprise_stock_report_delayed_item_report_business_behavior_delayed_item_report_filter_transactions_data`

**Inputs** self, consolidated = false.

**Record and data access** read doctype via get\_all.

**Explicit results** self.transactions.

**Local steps**

- Set sales\_orders from list of d.sales\_order for d drawn from self.transactions.
  - Draw d from self.transactions.
- Set doctype from “Sales Order”.
- Set filters from mapping(“name” → tuple(“in”, sales\_orders)).
- If not consolidated.
  - Set sales\_order\_items from list of d.so\_detail for d drawn from self.transactions.
    - Draw d from self.transactions.
  - Set doctype from “Sales Order Item”.
  - Set filters from mapping(“parent” → tuple(“in”, sales\_orders), “name” → tuple(“in”, sales\_order\_items)).
- Set so\_data from mapping().
- Set fields from list(“delivery\_date”, “name”).
- If Platform.db.has\_column(doctype, “parent”).
  - Evaluate fields.append(“parent”).
- For each d in Platform.get\_all(doctype, filters = filters, fields = fields).
  - Set key from d.name when consolidated, otherwise tuple(d.parent, d.name).
    - Value choice on consolidated — true gives d.name, false gives tuple(d.parent, d.name).
  - If key does not belong to so\_data.
    - Evaluate so\_data.setdefault(key, d.delivery\_date).
- For each row in self.transactions.
  - Set key from row.sales\_order when consolidated, otherwise tuple(row.sales\_order, row.so\_detail).
    - Value choice on consolidated — true gives row.sales\_order, false gives tuple(row.sales\_order, row.so\_detail).
  - Evaluate row.update(mapping(“delivery\_date” → so\_data.get(key), “delayed\_days” → date\_diff(row.posting\_date, so\_data.get(key)))).
- Return self.transactions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0889.json#L1150) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L108)

<a id="op-ad7032f73104af"></a>
### Delayed Item Report.get columns

`operation_enterprise_stock_report_delayed_item_report_business_behavior_delayed_item_report_get_columns`

**Inputs** self.

**Explicit results** list(mapping(“label” → translated based\_on, “fieldname” → “name”, “fieldtype” → “Link”, “options” → based\_on, …), mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “o ….

**Local steps**

- Set based\_on from self.filters.get(“based\_on”).
- Return list(mapping(“label” → translated based\_on, “fieldname” → “name”, “fieldtype” → “Link”, “options” → based\_on, …), mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “o ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0889.json#L1871) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L109)

<a id="op-8d5892e83b76ba"></a>
### Get group and descendants

`operation_enterprise_binding_enterprise_stock_report_delayed_item_report_delayed_item_report_get_group_and_descendants`

**Inputs** doctype, group.

**Explicit results** list(group, expanded get\_descendants\_of(doctype, group)).

**Local steps**

- Return list(group, expanded get\_descendants\_of(doctype, group)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L954)

## Report · Delayed order report

<a id="op-bf5075d3e1b672"></a>
### Execute

`operation_enterprise_stock_report_delayed_order_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set tuple(columns, data) from DelayedOrderReport(filters).run().
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L118)

<a id="op-31427ca6c1952c"></a>
### Delayed Order Report.run

`operation_enterprise_stock_report_delayed_order_report_business_behavior_delayed_order_report_run`

**Inputs** self.

**Explicit results** tuple(self.get\_columns(), (self.get\_data(consolidated = true) or list())).

**Local steps**

- Return tuple(self.get\_columns(), (self.get\_data(consolidated = true) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_data(consolidated = true) → list().

**Methods declared on this owner** [get columns](operations-006.md#op-cdf9ffc9b27ab0), [get data](operations-006.md#op-036f9f9f732ea7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0889.json#L4336) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L117)

<a id="op-036f9f9f732ea7"></a>
### Delayed Order Report.get data

`operation_enterprise_stock_report_delayed_order_report_business_behavior_delayed_order_report_get_data`

**Inputs** self, consolidated = false.

**Record and data access** read “Sales Order” via get\_all.

**Explicit results** list(last\_deliveries.values()).

**Local steps**

- Set data from (super().get\_data(consolidated) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in super().get\_data(consolidated) → list().
- Set last\_deliveries from mapping().
- For each d in data.
  - If flt(d.qty) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set last from last\_deliveries.get(d.sales\_order).
  - If (not last or getdate(d.posting\_date) &gt; getdate(last.posting\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not last → getdate(d.posting\_date) &gt; getdate(last.posting\_date).
    - Set last\_deliveries at d.sales\_order from d.
- Set order\_totals from dict(Platform.get\_all(“Sales Order”, filters = mapping(“name” → tuple(“in”, list(last\_deliveries))), fields = list(“name”, “grand\_total”), as\_list = true)).
- For each tuple(sales\_order, row) in last\_deliveries.items().
  - Set row.grand\_total from order\_totals.get(sales\_order).
- Return list(last\_deliveries.values()).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L116)

<a id="op-cdf9ffc9b27ab0"></a>
### Delayed Order Report.get columns

`operation_enterprise_stock_report_delayed_order_report_business_behavior_delayed_order_report_get_columns`

**Inputs** self.

**Explicit results** list(mapping(“label” → translated based\_on, “fieldname” → “name”, “fieldtype” → “Link”, “options” → based\_on, …), mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “o ….

**Local steps**

- Set based\_on from self.filters.get(“based\_on”).
- Return list(mapping(“label” → translated based\_on, “fieldname” → “name”, “fieldtype” → “Link”, “options” → based\_on, …), mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “o ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0889.json#L4642) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L115)

## Record · Delivery note

[Record definition](../../../../data/record-types/delivery_note.json)

<a id="op-a4fba00c928ead"></a>
### Delivery Note.initialize

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Delivery Note Item”, “target\_dt” → “Sales Order Item”, “join\_field” → “so\_detail”, “target\_field” → “delivered\_qty”, …), mapping(“source\_dt” → “Delivery Note Item”, “target\_dt”  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L874)

<a id="op-3276bd923be9d1"></a>
### Delivery Note.update status updater args

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_deliverynote_update_status_updater_args`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not cint(self.is\_return) or self.flags.get(“return\_updaters\_added”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cint(self.is\_return) → self.flags.get(“return\_updaters\_added”).
  - Return no value.
- Set self.flags.return\_updaters\_added from true.
- Evaluate self.status\_updater.extend(list(mapping(“source\_dt” → “Delivery Note Item”, “target\_dt” → “Sales Order Item”, “join\_field” → “so\_detail”, “target\_field” → “returned\_qty”, …), mapping(“source\_dt” → “Deliver ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L219)

<a id="op-b255ef2ee7941f"></a>
### Delivery Note.onload

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_onload`

**Inputs** self.

**Local steps**

- Evaluate super().onload().
- If self.docstatus equals 0.
  - Evaluate self.set\_onload(“has\_unpacked\_items”, self.has\_unpacked\_items()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has unpacked items](operations-007.md#op-262334b948d07e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0712.json#L6447) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L877)

<a id="op-75ffd36821dbc1"></a>
### Delivery Note.before print

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_before_print`

**Inputs** self, settings = no value.

**Local steps**

- Bind local operation toggle\_print\_hide for subsequent calls.
- Set item\_meta from Platform.get\_meta(“Delivery Note Item”).
- Set print\_hide\_fields from mapping(“parent” → list(“grand\_total”, “rounded\_total”, “in\_words”, “currency”, …), “items” → list(“rate”, “amount”, “discount\_amount”, “price\_list\_rate”, …)).
- For each tuple(key, fieldname) in print\_hide\_fields.items().
  - For each f in fieldname.
    - Evaluate toggle\_print\_hide(self.meta when key equals “parent”, otherwise item\_meta, f).
      - Value choice on key equals “parent” — true gives self.meta, false gives item\_meta.
- Evaluate super().before\_print(settings).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0712.json#L6570) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L869)

<a id="op-582bdf6fb2a73d"></a>
### Delivery Note.before print.toggle print hide

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_before_print_toggle_print_hide`

**Inputs** meta, fieldname.

**Local steps**

- Set df from meta.get\_field(fieldname).
- If self.get(“print\_without\_amount”).
  - Evaluate df.set(“\_\_print\_hide”, 1).
- Otherwise.
  - Evaluate df.delete\_key(“\_\_print\_hide”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0713.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L870)

<a id="op-d78acf13ac2f0b"></a>
### Delivery Note.set actual qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_deliverynote_set_actual_qty`

**Inputs** self.

**Record and data access** execute query text (SELECT, Bin).

**Local steps**

- For each d in self.get(“items”).
  - If (d.item\_code and d.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code → d.warehouse.
    - Set actual\_qty from Platform.db.sql(query text (SELECT, Bin), tuple(d.item\_code, d.warehouse)).
    - Set d.actual\_qty from ((actual\_qty and flt(actual\_qty at 0 at 0)) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (actual\_qty and flt(actual\_qty at 0 at 0)) → 0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in actual\_qty → flt(actual\_qty at 0 at 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L217)

<a id="op-88e2597ef67478"></a>
### Delivery Note.so required

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_sales_order_required`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Sales Order required for Item {0}”.format(d.item\_code).

**Local steps**

- If self.is\_return.
  - Return no value.
- If Platform.get\_single\_value(“Selling Settings”, “so\_required”) equals “Yes”.
  - For each d in self.get(“items”).
    - If not d.against\_sales\_order.
      - Call the validation error handler Platform.throw(translated “Sales Order required for Item {0}”.format(d.item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “so\_required”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L878)

<a id="op-5468c863296f80"></a>
### Delivery Note.before insert

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_deliverynote_before_insert`

**Inputs** self.

**Local steps**

- If self.amended\_from.
  - Set self.delivery\_trip from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L213)

<a id="op-41b7ca74153aac"></a>
### Delivery Note.validate

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_posting\_time().
- Evaluate self.set\_internal\_return\_target\_warehouse().
- Evaluate super().validate().
- Evaluate self.validate\_references().
- Evaluate self.set\_status().
- Evaluate self.so\_required().
- Evaluate self.validate\_proj\_cust().
- Evaluate self.check\_sales\_order\_on\_hold\_or\_close(“against\_sales\_order”).
- Evaluate self.validate\_warehouse().
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.set\_serial\_and\_batch\_bundle\_from\_pick\_list().
- Evaluate make\_packing\_list(self).
- Evaluate self.update\_current\_stock().
- If not self.installation\_status.
  - Set self.installation\_status from “Not Installed”.
- Evaluate self.validate\_against\_stock\_reservation\_entries().
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set internal return target warehouse](operations-006.md#op-2fb1cb91726b48), [validate references](operations-006.md#op-32e2318beea3f5), [so required](operations-006.md#op-88e2597ef67478), [validate proj cust](operations-007.md#op-f6ab5d9dab6e71), [validate warehouse](operations-007.md#op-69f1db00cd2844), [validate with previous doc](operations-006.md#op-352e8ff2713140), [update current stock](operations-007.md#op-3602af0f06aae4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L882)

<a id="op-2fb1cb91726b48"></a>
### Delivery Note.set internal return target warehouse

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_deliverynote_set_internal_return_target_warehouse`

**Inputs** self.

**Record and data access** read “Delivery Note Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Target Warehouse must be {1}, as on Delivery Note {2}”.format(row.idx, Platform.bold(expected), Platform.bold(self.return\_against)).

**Local steps**

- Set original\_rows from list of d.dn\_detail for d drawn from self.items where d.dn\_detail.
  - Draw d from self.items, keep a combination only if (d.dn\_detail).
- If not (self.is\_return and self.return\_against and self.is\_internal\_customer and original\_rows).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → self.is\_internal\_customer → original\_rows.
  - Return no value.
- Set target\_warehouses from Platform.\_dict(Platform.get\_all(“Delivery Note Item”, filters = mapping(“name” → tuple(“in”, original\_rows)), fields = list(“name”, “target\_warehouse”), as\_list = true)).
- For each row in self.items.
  - Set expected from target\_warehouses.get(row.dn\_detail).
  - If not expected.
    - Continue with the next iteration or loop test.
  - If not row.target\_warehouse.
    - Set row.target\_warehouse from expected.
  - Otherwise.
    - If row.target\_warehouse differs from expected.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Target Warehouse must be {1}, as on Delivery Note {2}”.format(row.idx, Platform.bold(expected), Platform.bold(self.return\_against))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L218)

<a id="op-352e8ff2713140"></a>
### Delivery Note.validate with previous doc

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_with_previous_record`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Sales Order” → mapping(“ref\_dn\_field” → “against\_sales\_order”, “compare\_fields” → list(list(“customer”, “=”), list(“company”, “=”), list(“project”, “=”), list(“c ….
- If (cint(Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”)) and not self.is\_return and not self.is\_internal\_customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”)) → not self.is\_return → not self.is\_internal\_customer.
  - Evaluate self.validate\_rate\_with\_reference\_doc(list(list(“Sales Order”, “against\_sales\_order”, “so\_detail”), list(“Sales Invoice”, “against\_sales\_invoice”, “si\_detail”))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0713.json#L826) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L890)

<a id="op-32e2318beea3f5"></a>
### Delivery Note.validate references

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_references`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_sales\_order\_references().
- Evaluate self.validate\_sales\_invoice\_references().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate sales order references](operations-006.md#op-b464e099258bca), [validate sales invoice references](operations-006.md#op-37b530a7751a65).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0713.json#L1547) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L886)

<a id="op-b464e099258bca"></a>
### Delivery Note.validate sales order references

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_sales_order_references`

**Inputs** self.

**Local steps**

- Evaluate self.\_validate\_dependent\_item\_fields(“against\_sales\_order”, “so\_detail”, translated “References to Sales Orders are Incomplete”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dependent item fields](operations-007.md#op-713b883e6305aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0713.json#L1618) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L888)

<a id="op-37b530a7751a65"></a>
### Delivery Note.validate sales invoice references

`operation_enterprise_stock_record_definitions_delivery_note_business_behavior_delivery_note_validate_sales_invoice_references`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.is\_return.
  - Return no value.
- Evaluate self.\_validate\_dependent\_item\_fields(“against\_sales\_invoice”, “si\_detail”, translated “References to Sales Invoices are Incomplete”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dependent item fields](operations-007.md#op-713b883e6305aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0713.json#L1706) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L887)
