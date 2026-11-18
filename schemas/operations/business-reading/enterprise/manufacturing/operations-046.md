# Production · operations 46

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-6c33464855e0f8"></a>
### Get row wise serial batch

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_row_wise_serial_batch`

**Inputs** work\_order, purpose = no value.

**Record and data access** read “Stock Entry” via get\_all · read “Serial and Batch Bundle” via get\_all.

**Explicit results** row\_wise\_serial\_batch.

**Local steps**

- If not purpose.
  - Set purpose from “Material Transfer for Manufacture”.
- Set purposes from list(purpose) when isinstance(purpose, str), otherwise purpose.
  - Value choice on isinstance(purpose, str) — true gives list(purpose), false gives purpose.
- Set stock\_entries from Platform.get\_all(“Stock Entry”, filters = mapping(“work\_order” → work\_order, “purpose” → tuple(“in”, purposes), “docstatus” → 1), pluck = “name”).
- Set serial\_batch\_entries from Platform.get\_all(“Serial and Batch Bundle”, fields = list(“′tabSerial and Batch Entry′.′serial\_no′”, “′tabSerial and Batch Entry′.′batch\_no′”, “′tabSerial and Batch Entry′.′qty′”, “′tabSerial and Batch Bun ….
- Set row\_wise\_serial\_batch from mapping().
- For each entry in serial\_batch\_entries.
  - Set key from tuple(entry.item\_code, entry.warehouse).
  - If key does not belong to row\_wise\_serial\_batch.
    - Set row\_wise\_serial\_batch at key from Platform.\_dict(mapping(“serial\_nos” → set(), “batch\_nos” → defaultdict(float))).
  - Set details from row\_wise\_serial\_batch at key.
  - If entry.serial\_no.
    - Evaluate details.serial\_nos.add(entry.serial\_no).
  - If entry.batch\_no.
    - Update details.batch\_nos at entry.batch\_no using + abs(entry.qty).
- Return row\_wise\_serial\_batch.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1011)

<a id="op-33da65c52cd739"></a>
### Get hour rate

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_get_hour_rate`

**Inputs** workstation.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Workstation” via get\_cached\_value.

**Explicit results** (Platform.get\_cached\_value(“Workstation”, workstation, “hour\_rate”) or 0.0).

**Local steps**

- Return (Platform.get\_cached\_value(“Workstation”, workstation, “hour\_rate”) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Workstation”, workstation, “hour\_rate”) → 0.0.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Workstation”, workstation, “hour\_rate”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1763) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1003)

<a id="op-826e24cd97243a"></a>
### Get data

`operation_enterprise_manufacturing_record_definitions_work_order_work_order_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “work\_order”, “non\_standard\_fieldnames” → mapping(“Batch” → “reference\_name”, “Stock Reservation Entry” → “voucher\_no”), “transactions” → list(mapping(“label” → translated “Transactio ….

**Local steps**

- Return mapping(“fieldname” → “work\_order”, “non\_standard\_fieldnames” → mapping(“Batch” → “reference\_name”, “Stock Reservation Entry” → “voucher\_no”), “transactions” → list(mapping(“label” → translated “Transactio ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L565) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L977)

## Record · Work order additional item

[Record definition](../../../../data/record-types/work_order_additional_item.json)

<a id="op-22b75c6d8353a6"></a>
### Work Order Additional Item.get list

`operation_enterprise_manufacturing_record_definitions_work_order_additional_item_business_behavior_work_order_additional_item_get_list`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L900) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L777)

<a id="op-38204b16600d2d"></a>
### Work Order Additional Item.get count

`operation_enterprise_manufacturing_record_definitions_work_order_additional_item_business_behavior_work_order_additional_item_get_count`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L948) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L776)

<a id="op-92ca21e772a085"></a>
### Work Order Additional Item.get stats

`operation_enterprise_manufacturing_record_definitions_work_order_additional_item_business_behavior_work_order_additional_item_get_stats`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L996) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L778)

<a id="op-84f6f607ca201c"></a>
### Work Order Additional Item.db insert

`operation_enterprise_manufacturing_record_definitions_work_order_additional_item_business_behavior_work_order_additional_item_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L1044) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L773)

<a id="op-7e279ce8d91bd0"></a>
### Work Order Additional Item.load from db

`operation_enterprise_manufacturing_record_definitions_work_order_additional_item_business_behavior_work_order_additional_item_load_from_database`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L1087) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L779)

<a id="op-047211558d8bcc"></a>
### Work Order Additional Item.db update

`operation_enterprise_manufacturing_record_definitions_work_order_additional_item_business_behavior_work_order_additional_item_database_update`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L1130) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L774)

<a id="op-7cf4604c0cd86d"></a>
### Work Order Additional Item.delete

`operation_enterprise_manufacturing_record_definitions_work_order_additional_item_business_behavior_work_order_additional_item_delete`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L1173) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L775)

## Report · Work order consumed materials

<a id="op-b496bcd27c0b82"></a>
### Execute

`operation_enterprise_manufacturing_report_work_order_consumed_materials_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1223)

<a id="op-36f57e3028b918"></a>
### Get data

`operation_enterprise_manufacturing_report_work_order_consumed_materials_business_behavior_get_data`

**Inputs** report\_filters.

**Record and data access** read “Work Order” via get\_all.

**Explicit results** data.

**Local steps**

- Set fields from get\_fields().
- Set filters from list(get\_filter\_condition(report\_filters)).
- If allowed\_companies bound to get\_allowed\_companies(Platform.session.user, “Work Order”).
  - Evaluate filters.append(nested operand in the contract.qb.DocType(“Work Order”).company.isin(allowed\_companies)).
- Set wo\_items from mapping().
- Set work\_orders from Platform.get\_all(“Work Order”, filters = filters, fields = fields).
- For each d in work\_orders.
  - Set d.consumed\_qty from (flt(d.consumed\_qty) − flt(d.returned\_qty)).
  - Set d.extra\_consumed\_qty from 0.0.
  - If (d.consumed\_qty and d.consumed\_qty &gt; d.required\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.consumed\_qty → d.consumed\_qty &gt; d.required\_qty.
    - Set d.extra\_consumed\_qty from (d.consumed\_qty − d.required\_qty).
  - If d.is\_additional\_item.
    - Set d.extra\_consumed\_qty from d.consumed\_qty.
  - If (d.extra\_consumed\_qty or not report\_filters.show\_extra\_consumed\_materials).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.extra\_consumed\_qty → not report\_filters.show\_extra\_consumed\_materials.
    - Evaluate wo\_items.setdefault(tuple(d.name, d.production\_item), list()).append(d).
- Set data from list().
- For each tuple(\_key, wo\_data) in wo\_items.items().
  - For each tuple(index, row) in enumerate(wo\_data).
    - If index differs from 0.
      - For each field in list(“name”, “status”, “production\_item”, “qty”, …).
        - Set row at field from empty text.
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1225)

<a id="op-684ebc11cf0e5d"></a>
### Get fields

`operation_enterprise_manufacturing_report_work_order_consumed_materials_business_behavior_get_fields`

**Inputs** no declared parameters.

**Explicit results** list(“′tabWork Order Item′.′parent′”, “′tabWork Order Item′.′item\_code′ as raw\_material\_item\_code”, “′tabWork Order Item′.′item\_name′ as raw\_material\_name”, “′tabWork Order Item′.′required\_qty′”, …).

**Local steps**

- Return list(“′tabWork Order Item′.′parent′”, “′tabWork Order Item′.′item\_code′ as raw\_material\_item\_code”, “′tabWork Order Item′.′item\_name′ as raw\_material\_name”, “′tabWork Order Item′.′required\_qty′”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1226)

<a id="op-44397a32610a8a"></a>
### Get filter condition

`operation_enterprise_manufacturing_report_work_order_consumed_materials_business_behavior_get_filter_condition`

**Inputs** report\_filters.

**Explicit results** filters.

**Local steps**

- Set filters from mapping(“docstatus” → 1, “status” → tuple(“in”, list(“In Process”, “Completed”, “Stopped”, “Closed”)), “creation” → tuple(“between”, list(report\_filters.from\_date, report\_filters.to\_date))).
- For each field in list(“name”, “production\_item”, “company”, “status”).
  - Set value from report\_filters.get(field).
  - If value.
    - Set key from formatted text {field}.
    - Evaluate filters.update(mapping(key → value)).
- Return filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1227)

<a id="op-5aa30891b5d8b3"></a>
### Get columns

`operation_enterprise_manufacturing_report_work_order_consumed_materials_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Id”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Work Order”, …), mapping(“label” → translated “Status”, “fieldname” → “status”, “fieldtype” → “Data”, “width ….

**Local steps**

- Return list(mapping(“label” → translated “Id”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Work Order”, …), mapping(“label” → translated “Status”, “fieldname” → “status”, “fieldtype” → “Data”, “width ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0556.json#L4060) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1224)

## Record · Work order item

[Record definition](../../../../data/record-types/work_order_item.json)

<a id="op-80e0bf58b7d1c7"></a>
### On doctype update

`operation_enterprise_manufacturing_record_definitions_work_order_item_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Work Order Item”.

**Local steps**

- Evaluate Platform.db.add\_index(“Work Order Item”, list(“item\_code”, “source\_warehouse”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0535.json#L1216) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L853)

## Report · Work order stock report

<a id="op-34f980f4015e57"></a>
### Execute

`operation_enterprise_manufacturing_report_work_order_stock_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set wo\_list from get\_work\_orders().
- Set data from get\_item\_list(wo\_list, filters).
- Set columns from get\_columns().
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0556.json#L6075) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1231)

<a id="op-7ec3bb1389badd"></a>
### Get item list

`operation_enterprise_manufacturing_report_work_order_stock_report_business_behavior_get_item_list`

**Inputs** wo\_list, filters.

**Explicit results** list() · sorted(out, key = deferred anonymous expression).

**Local steps**

- If not wo\_list.
  - Return list().
- Set descriptions from get\_bom\_descriptions(wo\_list).
- Set items\_by\_order from get\_work\_order\_items(wo\_list).
- Set stock from get\_stock(items\_by\_order, filters).
- Evaluate set\_aside\_transferred\_stock(wo\_list, stock).
- Set warehouses from set(get\_child\_warehouses(filters.warehouse)) when filters.get(“warehouse”), otherwise no value.
  - Value choice on filters.get(“warehouse”) — true gives set(get\_child\_warehouses(filters.warehouse)), false gives no value.
- Set out from list().
- For each wo\_details in wo\_list.
  - For each item in items\_by\_order.get(wo\_details.name, list()).
    - If (warehouses and item.source\_warehouse and item.source\_warehouse does not belong to warehouses).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouses → item.source\_warehouse → item.source\_warehouse does not belong to warehouses.
      - Continue with the next iteration or loop test.
    - Evaluate out.append(get\_row(wo\_details, item, descriptions, stock, …)).
- Return sorted(out, key = deferred anonymous expression).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1233)

<a id="op-7d421880937250"></a>
### Get row

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_get_row`

**Inputs** wo\_details, item, descriptions, stock, filters.

**Explicit results** Platform.\_dict(mapping(“work\_order” → wo\_details.name, “status” → wo\_details.status, “req\_items” → 1, “instock” → in\_stock, …)).

**Local steps**

- Set warehouse from (item.source\_warehouse or filters.get(“warehouse”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.source\_warehouse → filters.get(“warehouse”).
- Set pending\_qty from (flt(wo\_details.qty) − flt(wo\_details.produced\_qty)).
- Set qty\_per\_unit from (flt(item.required\_qty) ÷ flt(wo\_details.qty)) when flt(wo\_details.qty), otherwise 0.0.
  - Value choice on flt(wo\_details.qty) — true gives (flt(item.required\_qty) ÷ flt(wo\_details.qty)), false gives 0.0.
- Set in\_wip\_qty from get\_in\_wip\_qty(item).
- Set needed\_qty from max(((qty\_per\_unit × pending\_qty) − in\_wip\_qty), 0.0).
- Set available\_qty from (allocate\_stock(stock, tuple(item.item\_code, warehouse), needed\_qty) + in\_wip\_qty).
- Set build\_qty from (available\_qty ÷ qty\_per\_unit) when qty\_per\_unit, otherwise flt(wo\_details.qty).
  - Value choice on qty\_per\_unit — true gives (available\_qty ÷ qty\_per\_unit), false gives flt(wo\_details.qty).
- Set in\_stock from 1 when build\_qty ≥ pending\_qty, otherwise 0.
  - Value choice on build\_qty ≥ pending\_qty — true gives 1, false gives 0.
- Return Platform.\_dict(mapping(“work\_order” → wo\_details.name, “status” → wo\_details.status, “req\_items” → 1, “instock” → in\_stock, …)).
  - Value choice on in\_stock — true gives wo\_details.qty, false gives build\_qty.
  - Value choice on in\_stock — true gives “Y”, false gives “N”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1158)

<a id="op-f54c7307e816bc"></a>
### Get in wip qty

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_get_in_wip_qty`

**Inputs** item.

**Explicit results** max((flt(item.transferred\_qty) − flt(item.consumed\_qty)), 0.0).

**Local steps**

- Return max((flt(item.transferred\_qty) − flt(item.consumed\_qty)), 0.0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1157)

<a id="op-318fd6ef7a39d9"></a>
### Set aside transferred stock

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_set_aside_transferred_stock`

**Inputs** wo\_list, stock.

**Local steps**

- For each tuple(tuple(item\_code, warehouse), qty) in get\_stock\_held\_in\_wip(wo\_list).items().
  - If tuple(item\_code, warehouse) belongs to stock.
    - Set stock at tuple(item\_code, warehouse) from max((stock at tuple(item\_code, warehouse) − qty), 0.0).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1163)

<a id="op-10ae11dd336e68"></a>
### Get stock held in wip

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_get_stock_held_in_wip`

**Inputs** wo\_list.

**Explicit results** held.

**Local steps**

- Set held\_by\_order from mapping().
- For each tuple(purpose, is\_return, warehouse\_field, sign) in WIP\_STOCK\_MOVES.
  - For each row in get\_work\_order\_stock\_moves(wo\_list, purpose, is\_return, warehouse\_field).
    - Set key from tuple(row.work\_order, row.item\_code, row.warehouse).
    - Set held\_by\_order at key from (held\_by\_order.get(key, 0.0) + (sign × flt(row.qty))).
- Set held from mapping().
- For each tuple(tuple(\_work\_order, item\_code, warehouse), qty) in held\_by\_order.items().
  - If qty &gt; 0.
    - Set held at tuple(item\_code, warehouse) from (held.get(tuple(item\_code, warehouse), 0.0) + qty).
- Return held.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1160)

<a id="op-bf7052a627bf6d"></a>
### Get work order stock moves

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_get_work_order_stock_moves`

**Inputs** wo\_list, purpose, is\_return, warehouse\_field.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set se from Platform.qb.DocType(“Stock Entry”).
- Set sed from Platform.qb.DocType(“Stock Entry Detail”).
- Set warehouse from sed at warehouse\_field.
- Set query from nested operand in the contract(nested operand in the contract).select(se.work\_order, sed.item\_code, nested operand in the contract.as\_(“warehouse”), nested operand in the contract.as\_(“qty”)).where((((nest ….
  - Draw d from wo\_list.
- If is\_return is distinct from no value.
  - Set query from query.where(IfNull(se.is\_return, 0) equals is\_return).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1162)

<a id="op-360f5bcb22a8d1"></a>
### Allocate stock

`operation_enterprise_binding_enterprise_manufacturing_report_work_order_stock_report_work_order_stock_report_allocate_stock`

**Inputs** stock, key, needed\_qty.

**Explicit results** available\_qty.

**Local steps**

- Set available\_qty from flt(stock.get(key)).
- Set stock at key from (available\_qty − min(available\_qty, needed\_qty)).
- Return available\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1155)
