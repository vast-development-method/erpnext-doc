# Purchasing · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Buying settings

[Record definition](../../../../data/record-types/buying_settings.json)

<a id="op-a45ee85cbf21a0"></a>
### Buying Settings.validate

`operation_enterprise_buying_record_definitions_buying_settings_business_behavior_buying_settings_validate`

**Inputs** self.

**Local steps**

- For each key in list(“supplier\_group”, “supp\_master\_name”, “maintain\_same\_rate”, “buying\_price\_list”).
  - Set value from self.get(key).
  - Evaluate Platform.db.set\_default(key, empty text when value is identical to no value, otherwise value).
    - Value choice on value is identical to no value — true gives empty text, false gives value.
- Bind dependencies set\_by\_naming\_series.
- Evaluate set\_by\_naming\_series(“Supplier”, “supplier\_name”, self.get(“supp\_master\_name”) equals “Naming Series”, hide\_name\_field = false).
- If not self.bill\_for\_rejected\_quantity\_in\_purchase\_invoice.
  - Set self.set\_valuation\_rate\_for\_rejected\_materials from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L85) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1365)

<a id="op-b76b8ff1b03bf7"></a>
### Buying Settings.before save

`operation_enterprise_buying_record_definitions_buying_settings_business_behavior_buying_settings_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.check\_maintain\_same\_rate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check maintain same rate](operations-001.md#op-5d800ff03199c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0336.json#L2577) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1363)

<a id="op-5d800ff03199c0"></a>
### Buying Settings.check maintain same rate

`operation_enterprise_buying_record_definitions_buying_settings_business_behavior_buying_settings_check_maintain_same_rate`

**Inputs** self.

**Local steps**

- If self.maintain\_same\_rate.
  - Set self.set\_landed\_cost\_based\_on\_purchase\_invoice\_rate from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0336.json#L2628) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1364)

<a id="op-468aee5aaa5ec9"></a>
### Is rejected material valued

`operation_enterprise_binding_enterprise_buying_doctype_buying_settings_buying_settings_is_rejected_material_valued`

**Inputs** voucher\_type, voucher\_detail\_no = no value.

**Declared result** bool.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** true · false · (voucher\_type differs from “Purchase Invoice” or bool(Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”))).

**Local steps**

- If is\_material\_from\_in\_transit\_warehouse(voucher\_type, voucher\_detail\_no).
  - Return true.
- If not Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”).
  - Return false.
- Return (voucher\_type differs from “Purchase Invoice” or bool(Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in voucher\_type differs from “Purchase Invoice” → bool(Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_valuation\_rate\_for\_rejected\_materials”), Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L793) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L33)

<a id="op-b897d7807ecad6"></a>
### Is material from in transit warehouse

`operation_enterprise_binding_enterprise_buying_doctype_buying_settings_buying_settings_is_material_from_in_transit_warehouse`

**Inputs** voucher\_type, voucher\_detail\_no.

**Declared result** bool.

**Record and data access** read (voucher\_type + “ Item”) via get\_cached\_value.

**Explicit results** false · bool(Platform.get\_cached\_value((voucher\_type + “ Item”), voucher\_detail\_no, “from\_warehouse”)).

**Local steps**

- If (voucher\_type does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”) or not voucher\_detail\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in voucher\_type does not belong to tuple(“Purchase Receipt”, “Purchase Invoice”) → not voucher\_detail\_no.
  - Return false.
- Return bool(Platform.get\_cached\_value((voucher\_type + “ Item”), voucher\_detail\_no, “from\_warehouse”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value((voucher\_type + “ Item”), voucher\_detail\_no, “from\_warehouse”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L792) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L32)

<a id="op-2665ef69f4d6f7"></a>
### Bills rejected quantity

`operation_enterprise_binding_enterprise_buying_doctype_buying_settings_buying_settings_bills_rejected_quantity`

**Inputs** doc.

**Declared result** bool.

**Explicit results** false · is\_rejected\_material\_valued(doc.doctype).

**Local steps**

- If (doc.doctype differs from “Purchase Invoice” or not doc.get(“update\_stock”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype differs from “Purchase Invoice” → not doc.get(“update\_stock”).
  - Return false.
- If (doc.get(“is\_internal\_supplier”) and doc.get(“represents\_company”) equals doc.get(“company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“is\_internal\_supplier”) → doc.get(“represents\_company”) equals doc.get(“company”).
  - Return false.
- Return is\_rejected\_material\_valued(doc.doctype).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L791) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L31)

## Report · Item wise purchase history

<a id="op-09f38ba63046b7"></a>
### Execute

`operation_enterprise_buying_report_item_wise_purchase_history_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart\_data).

**Explicit failure paths** validation helper — translated “From Date cannot be greater than To Date”.

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If (filters.from\_date and filters.to\_date and filters.from\_date &gt; filters.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.from\_date → filters.to\_date → filters.from\_date &gt; filters.to\_date.
  - Call the validation error handler Platform.throw(translated “From Date cannot be greater than To Date”).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Set chart\_data from get\_chart\_data(data).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L188)

<a id="op-65136ef52d34c2"></a>
### Get columns

`operation_enterprise_buying_report_item_wise_purchase_history_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Item Code”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldtype” → “Data”, “fieldname” → “item\_n ….

**Local steps**

- Return list(mapping(“label” → translated “Item Code”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldtype” → “Data”, “fieldname” → “item\_n ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0356.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L190)

<a id="op-a55ee4ed02db7c"></a>
### Get data

`operation_enterprise_buying_report_item_wise_purchase_history_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set company\_list from get\_descendants\_of(“Company”, filters.get(“company”)).
- Evaluate company\_list.append(filters.get(“company”)).
- Set supplier\_details from get\_supplier\_details().
- Set item\_details from get\_item\_details().
- Set purchase\_order\_records from get\_purchase\_order\_details(company\_list, filters).
- For each record in purchase\_order\_records.
  - Set supplier\_record from supplier\_details.get(record.supplier).
  - Set item\_record from item\_details.get(record.item\_code).
  - Set row from mapping(“item\_code” → record.get(“item\_code”), “item\_name” → item\_record.get(“item\_name”), “item\_group” → item\_record.get(“item\_group”), “description” → record.get(“description”), …).
  - Set row at “currency” from Platform.get\_cached\_value(“Company”, row at “company”, “default\_currency”).
  - Evaluate data.append(row).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, row at “company”, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0356.json#L1951) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L191)

<a id="op-d24b73d5c840e4"></a>
### Get supplier details

`operation_enterprise_buying_report_item_wise_purchase_history_business_behavior_get_supplier_details`

**Inputs** no declared parameters.

**Record and data access** read “Supplier” via get\_all.

**Explicit results** supplier\_details.

**Local steps**

- Set details from Platform.get\_all(“Supplier”, fields = list(“name”, “supplier\_name”, “supplier\_group”)).
- Set supplier\_details from mapping().
- For each d in details.
  - Evaluate supplier\_details.setdefault(d.name, Platform.\_dict(mapping(“supplier\_name” → d.supplier\_name, “supplier\_group” → d.supplier\_group))).
- Return supplier\_details.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0356.json#L3005) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L194)

<a id="op-3b3c30c5f0d07a"></a>
### Get item details

`operation_enterprise_buying_report_item_wise_purchase_history_business_behavior_get_item_details`

**Inputs** no declared parameters.

**Record and data access** read “Item” via get\_all.

**Explicit results** item\_details.

**Local steps**

- Set details from Platform.db.get\_all(“Item”, fields = list(“name”, “item\_name”, “item\_group”)).
- Set item\_details from mapping().
- For each d in details.
  - Evaluate item\_details.setdefault(d.name, Platform.\_dict(mapping(“item\_name” → d.item\_name, “item\_group” → d.item\_group))).
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0356.json#L3228) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L192)

<a id="op-1552d84661c026"></a>
### Get purchase order details

`operation_enterprise_buying_report_item_wise_purchase_history_business_behavior_get_purchase_order_details`

**Inputs** company\_list, filters.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set db\_po from Platform.qb.DocType(“Purchase Order”).
- Set db\_po\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(db\_po.name, db\_po.supplier, db\_po.transaction\_date, db\_po.project, …).where(db\_po.docstatus equals 1).where(db\_po.company.isin(tuple(co ….
- If filters.get(“item\_code”).
  - Set query from query.where(db\_po\_item.item\_code equals filters.item\_code).
- If filters.get(“item\_group”).
  - Set item\_groups from list(filters.item\_group, expanded get\_descendants\_of(“Item Group”, filters.item\_group)).
  - Set query from query.where(db\_po\_item.item\_group.isin(item\_groups)).
- If filters.get(“from\_date”).
  - Set query from query.where(db\_po.transaction\_date ≥ filters.from\_date).
- If filters.get(“to\_date”).
  - Set query from query.where(db\_po.transaction\_date ≤ filters.to\_date).
- If filters.get(“supplier”).
  - Set query from query.where(db\_po.supplier equals filters.supplier).
- If match\_conditions bound to build\_match\_conditions(“Purchase Order”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L193)

<a id="op-09916abe96652a"></a>
### Get chart data

`operation_enterprise_buying_report_item_wise_purchase_history_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → translated “Total Purchase Amount”, “values” → datapoints at slice no value to 30))), “type” → “bar”,  ….

**Local steps**

- Set item\_wise\_purchase\_map from mapping().
- Set tuple(labels, datapoints) from tuple(list(), list()).
- For each row in data.
  - Set item\_key from row.get(“item\_code”).
  - If item\_key does not belong to item\_wise\_purchase\_map.
    - Set item\_wise\_purchase\_map at item\_key from 0.
  - Set item\_wise\_purchase\_map at item\_key from (flt(item\_wise\_purchase\_map at item\_key) + flt(row.get(“amount”))).
- Set item\_wise\_purchase\_map from mapping of item → value for tuple(item, value) drawn from sorted(item\_wise\_purchase\_map.items(), key = deferred anonymous expression, reverse = true).
  - Draw tuple(item, value) from sorted(item\_wise\_purchase\_map.items(), key = deferred anonymous expression, reverse = true).
- For each key in item\_wise\_purchase\_map.
  - Evaluate labels.append(key).
  - Evaluate datapoints.append(item\_wise\_purchase\_map at key).
- Return mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → translated “Total Purchase Amount”, “values” → datapoints at slice no value to 30))), “type” → “bar”,  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0356.json#L4267) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L189)

## Report · Procurement tracker

<a id="op-ea880d36e17ee4"></a>
### Execute

`operation_enterprise_buying_report_procurement_tracker_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L197)

<a id="op-04d7286f1a0c8b"></a>
### Get columns

`operation_enterprise_buying_report_procurement_tracker_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Material Request Date”, “fieldname” → “material\_request\_date”, “fieldtype” → “Date”, “width” → 140), mapping(“label” → translated “Material Request No”, “options” → “Mate ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0357.json#L926) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L198)

<a id="op-17d636f372a2e1"></a>
### Apply filters on query

`operation_enterprise_buying_report_procurement_tracker_business_behavior_apply_filters_on_query`

**Inputs** filters, parent, child, query.

**Explicit results** query.

**Local steps**

- If filters.get(“company”).
  - Set query from query.where(parent.company equals filters.get(“company”)).
- If filters.get(“cost\_center”).
  - Set query from query.where(child.cost\_center equals filters.get(“cost\_center”)).
- If filters.get(“project”).
  - Set query from query.where(child.project equals filters.get(“project”)).
- If filters.get(“from\_date”).
  - Set query from query.where(parent.transaction\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Set query from query.where(parent.transaction\_date ≤ filters.get(“to\_date”)).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L196)

<a id="op-bd0522bcde1559"></a>
### Get data

`operation_enterprise_buying_report_procurement_tracker_business_behavior_get_data`

**Inputs** filters.

**Explicit results** procurement\_record.

**Local steps**

- Set purchase\_order\_entry from get\_po\_entries(filters).
- Set request\_items from set of po.material\_request\_item for po drawn from purchase\_order\_entry where po.material\_request\_item.
  - Draw po from purchase\_order\_entry, keep a combination only if (po.material\_request\_item).
- Set tuple(mr\_records, procurement\_record\_against\_mr) from get\_mapped\_mr\_details(filters, request\_items).
- Set pr\_records from get\_mapped\_pr\_records().
- Set pi\_records from get\_mapped\_pi\_records(filters).
- Set ordered\_qty\_by\_request\_item from get\_ordered\_qty\_by\_request\_item(request\_items).
- Set procurement\_record from list().
- If procurement\_record\_against\_mr.
  - Update procurement\_record using + procurement\_record\_against\_mr.
- For each po in purchase\_order\_entry.
  - Set material\_requests from mr\_records.get(po.material\_request\_item, list(mapping())).
  - For each mr\_record in material\_requests.
    - Set procurement\_detail from mapping(“material\_request\_date” → mr\_record.get(“transaction\_date”), “cost\_center” → po.cost\_center, “project” → po.project, “requesting\_site” → po.warehouse, …).
    - Evaluate procurement\_record.append(procurement\_detail).
- Return procurement\_record.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L199)

<a id="op-68f4e98a540f5c"></a>
### Get ordered qty by request item

`operation_enterprise_binding_enterprise_buying_report_procurement_tracker_procurement_tracker_get_ordered_qty_by_request_item`

**Inputs** request\_items.

**Explicit results** mapping() · dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(child.material\_request\_item).run()).

**Local steps**

- If not request\_items.
  - Return mapping().
- Set parent from Platform.qb.DocType(“Purchase Order”).
- Set child from Platform.qb.DocType(“Purchase Order Item”).
- Return dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(child.material\_request\_item).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L218) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L880) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L120)

<a id="op-885f9401d97454"></a>
### Get request qty column

`operation_enterprise_binding_enterprise_buying_report_procurement_tracker_procurement_tracker_get_request_qty_column`

**Inputs** parent, child.

**Explicit results** Case().when((parent.is\_subcontracted equals 1 bitwise and parent.is\_old\_subcontracting\_flow equals 0), child.fg\_item\_qty).else\_(child.stock\_qty).

**Local steps**

- Return Case().when((parent.is\_subcontracted equals 1 bitwise and parent.is\_old\_subcontracting\_flow equals 0), child.fg\_item\_qty).else\_(child.stock\_qty).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L219) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L881) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L121)

<a id="op-42e4543a8f4190"></a>
### Get actual cost

`operation_enterprise_binding_enterprise_buying_report_procurement_tracker_procurement_tracker_get_actual_cost`

**Inputs** po, pi\_records.

**Explicit results** flt(pi\_records at po.name) · 0.0 when po.status equals “Closed”, otherwise flt(po.base\_amount).

**Local steps**

- If po.name belongs to pi\_records.
  - Return flt(pi\_records at po.name).
- Return 0.0 when po.status equals “Closed”, otherwise flt(po.base\_amount).
  - Value choice on po.status equals “Closed” — true gives 0.0, false gives flt(po.base\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L877) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L117)

<a id="op-ea704b4d1fddd9"></a>
### Get estimated cost

`operation_enterprise_binding_enterprise_buying_report_procurement_tracker_procurement_tracker_get_estimated_cost`

**Inputs** po, mr\_record, ordered\_qty\_by\_request\_item.

**Explicit results** flt(mr\_record.get(“amount”)) · (flt(mr\_record.get(“amount”)) × (flt(po.request\_qty) ÷ ordered\_qty)).

**Local steps**

- Set ordered\_qty from flt(ordered\_qty\_by\_request\_item.get(po.material\_request\_item)).
- If not ordered\_qty.
  - Return flt(mr\_record.get(“amount”)).
- Return (flt(mr\_record.get(“amount”)) × (flt(po.request\_qty) ÷ ordered\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L216) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L878) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L118)

<a id="op-55b8ee7bde5c4e"></a>
### Get mapped mr details

`operation_enterprise_buying_report_procurement_tracker_business_behavior_get_mapped_material_request_details`

**Inputs** filters, request\_items.

**Explicit results** tuple(mr\_records, procurement\_record\_against\_mr).

**Local steps**

- Set parent from Platform.qb.DocType(“Material Request”).
- Set child from Platform.qb.DocType(“Material Request Item”).
- Set query from nested operand in the contract(nested operand in the contract).from\_(child).select(parent.transaction\_date, parent.owner, child.name, child.parent, …).where((((parent.per\_ordered ≥ 0 bitwise and parent.nam ….
- Set mr\_records from mapping().
- If request\_items.
  - For each record in query.where(child.name.isin(list(request\_items))).run(as\_dict = true).
    - Evaluate mr\_records.setdefault(record.name, list()).append(record).
- Set unordered\_query from apply\_filters\_on\_query(filters, parent, child, query).where(child.ordered\_qty equals 0).
- Set procurement\_record\_against\_mr from list().
- For each record in unordered\_query.run(as\_dict = true).
  - Set procurement\_record\_details from dict(material\_request\_date = record.transaction\_date, material\_request\_no = record.parent, requestor = record.owner, item\_code = record.item\_code, …).
  - Evaluate procurement\_record\_against\_mr.append(procurement\_record\_details).
- Return tuple(mr\_records, procurement\_record\_against\_mr).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L200)

<a id="op-2d4dfc7660038a"></a>
### Get hidden order statuses

`operation_enterprise_binding_enterprise_buying_report_procurement_tracker_procurement_tracker_get_hidden_order_statuses`

**Inputs** filters.

**Explicit results** tuple(“Cancelled”) · tuple(“Closed”, “Completed”, “Cancelled”).

**Local steps**

- If filters.get(“show\_completed\_orders”).
  - Return tuple(“Cancelled”).
- Return tuple(“Closed”, “Completed”, “Cancelled”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L119)

<a id="op-b088a4109fd3f2"></a>
### Get mapped pi records

`operation_enterprise_buying_report_procurement_tracker_business_behavior_get_mapped_purchase_invoice_records`

**Inputs** filters.

**Explicit results** Platform.\_dict(pi\_records).

**Local steps**

- Set po from Platform.qb.DocType(“Purchase Order”).
- Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set pi\_records from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….run().
- Return Platform.\_dict(pi\_records).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L201)
