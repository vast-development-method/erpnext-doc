# Production · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Production plan summary

<a id="op-35722c05db1777"></a>
### Get data

`operation_enterprise_manufacturing_report_production_plan_summary_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set order\_details from mapping().
- Evaluate get\_work\_order\_details(filters, order\_details).
- Evaluate get\_purchase\_order\_details(filters, order\_details).
- Evaluate get\_production\_plan\_item\_details(filters, data, order\_details).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1189)

<a id="op-5c8e80efba8f84"></a>
### Get production plan item details

`operation_enterprise_binding_enterprise_manufacturing_report_production_plan_summary_production_plan_summary_get_production_plan_item_details`

**Inputs** filters, data, order\_details.

**Record and data access** resolve a document from “Production Plan” via get\_cached\_doc · read “Work Order” via get\_all · read “Item” via get\_cached\_value.

**Local steps**

- Set production\_plan\_doc from Platform.get\_cached\_doc(“Production Plan”, filters.get(“production\_plan”)).
- For each row in production\_plan\_doc.po\_items.
  - Set work\_orders from Platform.get\_all(“Work Order”, filters = mapping(“production\_plan\_item” → row.name, “bom\_no” → row.bom\_no, “production\_item” → row.item\_code, “docstatus” → 1), order\_by = “creation”, pluck = “name”).
  - Set order\_qty from flt(row.planned\_qty).
  - Set total\_produced\_qty from 0.0.
  - Set pending\_qty from order\_qty.
  - For each work\_order in work\_orders.
    - Set details from order\_details.get(tuple(work\_order, row.item\_code), mapping()).
    - Set produced\_qty from flt(details.get(“produced\_qty”, 0)).
    - Set pending\_qty from get\_pending\_qty(order\_qty, produced\_qty, details.get(“process\_loss\_qty”)).
    - Update total\_produced\_qty using + produced\_qty.
    - Evaluate data.append(mapping(“indent” → 0, “item\_code” → row.item\_code, “sales\_order” → row.get(“sales\_order”), “item\_name” → Platform.get\_cached\_value(“Item”, row.item\_code, “item\_name”), …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in work\_order → empty text.
    - Set order\_qty from get\_pending\_qty(order\_qty, produced\_qty, 0).
  - Evaluate data.append(mapping(“item\_code” → row.item\_code, “indent” → 0, “qty” → row.planned\_qty, “produced\_qty” → total\_produced\_qty, …)).
    - Value choice on work\_orders — true gives get\_summary\_pending\_qty(row, work\_orders, order\_details), false gives pending\_qty.
  - Evaluate get\_production\_plan\_sub\_assembly\_item\_details(filters, row, production\_plan\_doc, data, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Production Plan”, filters.get(“production\_plan”)), Platform.get\_cached\_value(“Item”, row.item\_code, “item\_name”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1149)

<a id="op-4d85efbce7f3aa"></a>
### Get production plan sub assembly item details

`operation_enterprise_binding_enterprise_manufacturing_report_production_plan_summary_production_plan_summary_get_production_plan_sub_assembly_item_details`

**Inputs** filters, row, production\_plan\_doc, data, order\_details.

**Record and data access** read “Purchase Order Item” via get\_all · read “Work Order” via get\_all.

**Local steps**

- For each item in production\_plan\_doc.sub\_assembly\_items.
  - If row.name equals item.production\_plan\_item.
    - Set subcontracted\_item from item.type\_of\_manufacturing equals “Subcontract”.
    - If subcontracted\_item.
      - Set docnames from Platform.get\_all(“Purchase Order Item”, filters = mapping(“production\_plan\_sub\_assembly\_item” → item.name, “docstatus” → 1), fields = list(“parent”), order\_by = “creation”, pluck = “parent”).
    - Otherwise.
      - Set docnames from Platform.get\_all(“Work Order”, filters = mapping(“production\_plan\_sub\_assembly\_item” → item.name, “docstatus” → 1), fields = list(“name”), order\_by = “creation”, pluck = “name”).
    - Set remaining\_qty from flt(item.qty).
    - For each docname in docnames.
      - Set details from order\_details.get(tuple(docname, item.production\_item), mapping()).
      - Set produced\_qty from flt(details.get(“produced\_qty”, 0)).
      - Evaluate data.append(mapping(“indent” → (1 + item.indent), “item\_code” → item.production\_item, “item\_name” → item.item\_name, “qty” → item.qty, …)).
        - Value choice on not subcontracted\_item — true gives “Work Order”, false gives “Purchase Order”.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in docname → empty text.
      - Set remaining\_qty from get\_pending\_qty(remaining\_qty, produced\_qty, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1150)

<a id="op-c15b700d7bda89"></a>
### Get summary pending qty

`operation_enterprise_binding_enterprise_manufacturing_report_production_plan_summary_production_plan_summary_get_summary_pending_qty`

**Inputs** row, work\_orders, order\_details.

**Explicit results** get\_pending\_qty(row.planned\_qty, produced\_qty, unreplaced\_loss\_qty).

**Local steps**

- Set details from list of order\_details.get(tuple(work\_order, row.item\_code), mapping()) for work\_order drawn from work\_orders.
  - Draw work\_order from work\_orders.
- Set produced\_qty from sum(generator of flt(d.get(“produced\_qty”)) for d drawn from details).
  - Draw d from details.
- Set ordered\_beyond\_plan from max((sum(generator of flt(nested operand in the contract.get(“qty”)) for d drawn from details) − flt(row.planned\_qty)), 0).
  - Draw d from details.
- Set process\_loss\_qty from sum(generator of flt(d.get(“process\_loss\_qty”)) for d drawn from details).
  - Draw d from details.
- Set unreplaced\_loss\_qty from max((process\_loss\_qty − ordered\_beyond\_plan), 0).
- Return get\_pending\_qty(row.planned\_qty, produced\_qty, unreplaced\_loss\_qty).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1152)

<a id="op-0f0d81dc852b1a"></a>
### Get pending qty

`operation_enterprise_binding_enterprise_manufacturing_report_production_plan_summary_production_plan_summary_get_pending_qty`

**Inputs** qty, produced\_qty, process\_loss\_qty.

**Explicit results** flt(((flt(qty) − flt(produced\_qty)) − flt(process\_loss\_qty)), Platform.get\_precision(“Work Order”, “qty”)).

**Local steps**

- Return flt(((flt(qty) − flt(produced\_qty)) − flt(process\_loss\_qty)), Platform.get\_precision(“Work Order”, “qty”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1148)

<a id="op-8f39b054c3e247"></a>
### Get work order details

`operation_enterprise_binding_enterprise_manufacturing_report_production_plan_summary_production_plan_summary_get_work_order_details`

**Inputs** filters, order\_details.

**Record and data access** read “Work Order” via get\_all.

**Local steps**

- For each row in Platform.get\_all(“Work Order”, filters = mapping(“production\_plan” → filters.get(“production\_plan”), “docstatus” → 1), fields = list(“name”, “qty”, “produced\_qty”, “process\_loss\_qty”, …)).
  - Evaluate order\_details.setdefault(tuple(row.name, row.production\_item), row).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1153)

<a id="op-3ef3d503a0fe37"></a>
### Get purchase order details

`operation_enterprise_binding_enterprise_manufacturing_report_production_plan_summary_production_plan_summary_get_purchase_order_details`

**Inputs** filters, order\_details.

**Record and data access** read “Purchase Order Item” via get\_all.

**Local steps**

- For each row in Platform.get\_all(“Purchase Order Item”, filters = mapping(“production\_plan” → filters.get(“production\_plan”), “docstatus” → 1), fields = list(“parent”, “qty”, “received\_qty as produced\_qty”, “item\_code”, …)).
  - If row.fg\_item.
    - Update row.produced\_qty using ÷ ((row.qty ÷ row.fg\_item\_qty) or 1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (row.qty ÷ row.fg\_item\_qty) → 1.
  - Evaluate order\_details.setdefault(tuple(row.parent, (row.fg\_item or row.item\_code)), row).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.fg\_item → row.item\_code.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1151)

<a id="op-ce9c2b8138ad72"></a>
### Get column

`operation_enterprise_manufacturing_report_production_plan_summary_business_behavior_get_column`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Finished Good”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “width” → 240, …), mapping(“label” → translated “Item Name”, “fieldtype” → “data”, “fieldname” → “item\_na ….

**Local steps**

- Return list(mapping(“label” → translated “Finished Good”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “width” → 240, …), mapping(“label” → translated “Item Name”, “fieldtype” → “data”, “fieldname” → “item\_na ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1188)

## Report · Production planning report

<a id="op-494b7631b887f7"></a>
### Execute

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** ProductionPlanReport(filters).execute\_report().

**Local steps**

- Return ProductionPlanReport(filters).execute\_report().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0554.json#L977) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1200)

<a id="op-3a19bcdab7e7ce"></a>
### Production Plan Report.initialize

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.raw\_materials\_dict from mapping().
- Set self.data from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0554.json#L1041) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1209)

<a id="op-6814e4d162e979"></a>
### Production Plan Report.execute report

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_execute_report`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Evaluate self.get\_open\_orders().
- Evaluate self.get\_raw\_materials().
- Evaluate self.get\_item\_details().
- Evaluate self.get\_bin\_details().
- Evaluate self.get\_purchase\_details().
- Evaluate self.prepare\_data().
- Evaluate self.get\_columns().
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [get open orders](operations-036.md#op-8ee1ddc27c2f63), [get raw materials](operations-036.md#op-26a4638a8a97f1), [get item details](operations-036.md#op-278783507366ab), [get bin details](operations-036.md#op-321702b4264c34), [get purchase details](operations-036.md#op-f07a60740481fc), [prepare data](operations-036.md#op-f2fbc61adaee72), [get columns](operations-036.md#op-5c98633552c93d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0554.json#L1159) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1201)

<a id="op-8ee1ddc27c2f63"></a>
### Production Plan Report.get open orders

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_get_open_orders`

**Inputs** self.

**Local steps**

- Set tuple(doctype, order\_by) from tuple(self.filters.based\_on, self.filters.order\_by).
- Set parent from Platform.qb.DocType(doctype).
- Set query from no value.
- If doctype equals “Work Order”.
  - Set query from nested operand in the contract.qb.from\_(parent).select(parent.production\_item, parent.item\_name.as\_(“production\_item\_name”), parent.planned\_start\_date, parent.stock\_uom, …).where(parent.status.notin(list(“ ….
  - If order\_by equals “Planned Start Date”.
    - Set query from query.orderby(parent.planned\_start\_date, order = Order.asc).
  - Set query from query.orderby(parent.name).
  - If self.filters.docnames.
    - Set query from query.where(parent.name.isin(self.filters.docnames)).
- Otherwise.
  - Set child from Platform.qb.DocType(formatted text {doctype} Item).
  - Set query from nested operand in the contract(nested operand in the contract).from\_(child).select(child.bom\_no, child.stock\_uom, child.warehouse, child.parent.as\_(“name”), …).where(parent.name equals child.parent).
  - If self.filters.docnames.
    - Set query from query.where(child.parent.isin(self.filters.docnames)).
  - If doctype equals “Sales Order”.
    - Set query from query.select(child.delivery\_date, parent.base\_grand\_total, child.delivered\_qty, child.conversion\_factor, …).where(((child.stock\_qty &gt; child.produced\_qty bitwise and parent.per\_delivered &lt; 100.0) bitwise an ….
    - If order\_by equals “Delivery Date”.
      - Set query from query.orderby(child.delivery\_date, order = Order.asc).
    - Otherwise.
      - If order\_by equals “Total Amount”.
        - Set query from query.orderby(parent.base\_grand\_total, order = Order.desc).
  - Otherwise.
    - If doctype equals “Material Request”.
      - Set query from query.select(child.schedule\_date, child.ordered\_qty).where(((parent.per\_ordered &lt; 100 bitwise and parent.material\_request\_type equals “Manufacture”) bitwise and parent.status differs from “Stopped”)).
      - If order\_by equals “Required Date”.
        - Set query from query.orderby(child.schedule\_date, order = Order.asc).
  - Set query from query.orderby(child.parent).orderby(child.idx).
- Set query from query.where(parent.docstatus equals 1).
- If self.filters.company.
  - Set query from query.where(parent.company equals self.filters.company).
- Set self.orders from query.run(as\_dict = true).
- Evaluate self.set\_pending\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set pending qty](operations-036.md#op-8c6af77df4b1d5).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1206)

<a id="op-8c6af77df4b1d5"></a>
### Production Plan Report.set pending qty

`operation_enterprise_binding_enterprise_manufacturing_report_production_planning_report_production_planning_report_productionplanreport_set_pending_qty`

**Inputs** self.

**Local steps**

- For each d in self.orders.
  - Set done\_qty from max(flt(d.produced\_qty), (flt(d.delivered\_qty) × flt(d.conversion\_factor)), flt(d.ordered\_qty)).
  - Set d.qty\_to\_manufacture from (flt(d.qty\_to\_manufacture) − done\_qty).
- Set self.orders from list of d for d drawn from self.orders where d.qty\_to\_manufacture &gt; 0.
  - Draw d from self.orders, keep a combination only if (d.qty\_to\_manufacture &gt; 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1154)

<a id="op-26a4638a8a97f1"></a>
### Production Plan Report.get raw materials

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_get_raw_materials`

**Inputs** self.

**Record and data access** read “Work Order Item” via get\_all · read “Item” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not self.orders.
  - Return no value.
- Set self.warehouses from list of d.warehouse for d drawn from self.orders.
  - Draw d from self.orders.
- Set self.item\_codes from list of d.production\_item for d drawn from self.orders.
  - Draw d from self.orders.
- If self.filters.based\_on equals “Work Order”.
  - Set work\_orders from list of d.name for d drawn from self.orders.
    - Draw d from self.orders.
  - Set raw\_materials from (Platform.get\_all(“Work Order Item”, fields = list(“parent”, “item\_code”, “item\_name as raw\_material\_name”, “source\_warehouse as warehouse”, …), filters = mapping(“docstatus” → 1, “parent” → tuple(“in”, wo ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Work Order Item”, fields = list(“parent”, “item\_code”, “item\_name as raw\_material\_name”, “source\_warehouse as warehouse”, …), filters = mapping(“docstatus” → 1, “parent” → tuple(“in”, wor … → list().
  - For each d in raw\_materials.
    - Set issued\_qty from (max(flt(d.transferred\_qty), flt(d.consumed\_qty)) − flt(d.returned\_qty)).
    - Set d.required\_qty from max((flt(d.required\_qty) − issued\_qty), 0).
  - Evaluate self.warehouses.extend(list of d.warehouse for d drawn from raw\_materials).
    - Draw d from raw\_materials.
- Otherwise.
  - Set bom\_nos from list().
  - For each d in self.orders.
    - Set bom\_no from (d.bom\_no or Platform.get\_cached\_value(“Item”, d.production\_item, “default\_bom”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.bom\_no → Platform.get\_cached\_value(“Item”, d.production\_item, “default\_bom”).
    - If not d.bom\_no.
      - Set d.bom\_no from bom\_no.
    - Evaluate bom\_nos.append(bom\_no).
  - Set bom\_item\_doctype from “BOM Explosion Item” when self.filters.include\_subassembly\_raw\_materials, otherwise “BOM Item”.
    - Value choice on self.filters.include\_subassembly\_raw\_materials — true gives “BOM Explosion Item”, false gives “BOM Item”.
  - Set bom from Platform.qb.DocType(“BOM”).
  - Set bom\_item from Platform.qb.DocType(bom\_item\_doctype).
  - If self.filters.include\_subassembly\_raw\_materials.
    - Set qty\_field from bom\_item.qty\_consumed\_per\_unit.
  - Otherwise.
    - Set qty\_field from (bom\_item.stock\_qty ÷ bom.quantity).
  - Set raw\_materials from nested operand in the contract(nested operand in the contract).orderby(bom\_item.parent).orderby(bom\_item.idx).run(as\_dict = true).
- If not raw\_materials.
  - Return no value.
- Evaluate self.item\_codes.extend(list of d.item\_code for d drawn from raw\_materials).
  - Draw d from raw\_materials.
- For each d in raw\_materials.
  - If d.parent does not belong to self.raw\_materials\_dict.
    - Evaluate self.raw\_materials\_dict.setdefault(d.parent, list()).
  - Set rows from self.raw\_materials\_dict at d.parent.
  - Evaluate rows.append(d).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.production\_item, “default\_bom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1208)

<a id="op-278783507366ab"></a>
### Production Plan Report.get item details

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_get_item_details`

**Inputs** self.

**Record and data access** read “Item Default” via get\_all.

**Explicit results** no value.

**Local steps**

- If not (self.orders and self.item\_codes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.orders → self.item\_codes.
  - Return no value.
- Set self.item\_details from mapping().
- For each d in Platform.get\_all(“Item Default”, fields = list(“parent”, “default\_warehouse”), filters = mapping(“company” → self.filters.company, “parent” → tuple(“in”, self.item\_codes))).
  - Set self.item\_details at d.parent from d.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0554.json#L4107) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1205)

<a id="op-321702b4264c34"></a>
### Production Plan Report.get bin details

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_get_bin_details`

**Inputs** self.

**Record and data access** read “Bin” via get\_all.

**Explicit results** no value.

**Local steps**

- If not (self.orders and self.raw\_materials\_dict).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.orders → self.raw\_materials\_dict.
  - Return no value.
- Set self.bin\_details from mapping().
- Set self.mrp\_warehouses from list().
- If self.filters.raw\_material\_warehouse.
  - Evaluate self.mrp\_warehouses.extend(get\_child\_warehouses(self.filters.raw\_material\_warehouse)).
  - Evaluate self.warehouses.extend(self.mrp\_warehouses).
- For each d in Platform.get\_all(“Bin”, fields = list(“warehouse”, “item\_code”, “actual\_qty”, “ordered\_qty”, …), filters = mapping(“item\_code” → tuple(“in”, self.item\_codes), “warehouse” → tuple(“in”, self.warehouses))).
  - Set key from tuple(d.item\_code, d.warehouse).
  - If key does not belong to self.bin\_details.
    - Evaluate self.bin\_details.setdefault(key, d).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0554.json#L4353) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1203)

<a id="op-f07a60740481fc"></a>
### Production Plan Report.get purchase details

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_get_purchase_details`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.orders and self.raw\_materials\_dict).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.orders → self.raw\_materials\_dict.
  - Return no value.
- Set self.purchase\_details from mapping().
- Set po from Platform.qb.DocType(“Purchase Order”).
- Set poi from Platform.qb.DocType(“Purchase Order Item”).
- Set purchased\_items from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise ….
- For each d in purchased\_items.
  - Set key from tuple(d.item\_code, d.warehouse).
  - If key does not belong to self.purchase\_details.
    - Evaluate self.purchase\_details.setdefault(key, d).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1207)

<a id="op-f2fbc61adaee72"></a>
### Production Plan Report.prepare data

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_prepare_data`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.orders.
  - Return no value.
- For each d in self.orders.
  - Set key from d.name when self.filters.based\_on equals “Work Order”, otherwise d.bom\_no.
    - Value choice on self.filters.based\_on equals “Work Order” — true gives d.name, false gives d.bom\_no.
  - If not self.raw\_materials\_dict.get(key).
    - Continue with the next iteration or loop test.
  - Set bin\_data from (self.bin\_details.get(tuple(d.production\_item, d.warehouse)) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.bin\_details.get(tuple(d.production\_item, d.warehouse)) → mapping().
  - Evaluate d.update(mapping(“for\_warehouse” → d.warehouse, “available\_qty” → 0)).
  - If (bin\_data and bin\_data.get(“actual\_qty”) &gt; 0 and d.qty\_to\_manufacture).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bin\_data → bin\_data.get(“actual\_qty”) &gt; 0 → d.qty\_to\_manufacture.
    - Set d.available\_qty from bin\_data.get(“actual\_qty”) when d.qty\_to\_manufacture &gt; bin\_data.get(“actual\_qty”), otherwise d.qty\_to\_manufacture.
      - Value choice on d.qty\_to\_manufacture &gt; bin\_data.get(“actual\_qty”) — true gives bin\_data.get(“actual\_qty”), false gives d.qty\_to\_manufacture.
    - Update bin\_data at “actual\_qty” using − d.available\_qty.
  - Evaluate self.update\_raw\_materials(d, key).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update raw materials](operations-036.md#op-59ca85c09fca44).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0554.json#L5498) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1211)

<a id="op-59ca85c09fca44"></a>
### Production Plan Report.update raw materials

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_update_raw_materials`

**Inputs** self, data, key.

**Local steps**

- Set self.index from 0.
- Evaluate self.raw\_materials\_dict.get(key).
- For each d in self.raw\_materials\_dict.get(key).
  - If self.filters.based\_on differs from “Work Order”.
    - Set d.required\_qty from (d.required\_qty\_per\_unit × data.qty\_to\_manufacture).
  - Set warehouses from (self.mrp\_warehouses or list(data.warehouse)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mrp\_warehouses → list(data.warehouse).
  - If (self.filters.based\_on equals “Work Order” and d.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.based\_on equals “Work Order” → d.warehouse.
    - Set warehouses from list(d.warehouse).
  - Otherwise.
    - Set item\_details from self.item\_details.get(d.item\_code).
    - If (item\_details and item\_details.get(“default\_warehouse”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details → item\_details.get(“default\_warehouse”).
      - Set warehouses from list(item\_details at “default\_warehouse”).
  - If self.filters.raw\_material\_warehouse.
    - Set warehouses from get\_child\_warehouses(self.filters.raw\_material\_warehouse).
  - Set d.remaining\_qty from d.required\_qty.
  - Evaluate self.pick\_materials\_from\_warehouses(d, data, warehouses).
  - If (d.remaining\_qty and self.filters.raw\_material\_warehouse and d.remaining\_qty differs from d.required\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.remaining\_qty → self.filters.raw\_material\_warehouse → d.remaining\_qty differs from d.required\_qty.
    - Set row from self.get\_args().
    - Set d.warehouse from self.filters.raw\_material\_warehouse.
    - Set d.required\_qty from d.remaining\_qty.
    - Set d.allotted\_qty from 0.
    - Evaluate row.update(d).
    - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [pick materials from warehouses](operations-036.md#op-2ee11031eb279e), [get args](operations-036.md#op-682a94f6367fbb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1212)

<a id="op-2ee11031eb279e"></a>
### Production Plan Report.pick materials from warehouses

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_pick_materials_from_warehouses`

**Inputs** self, args, order\_data, warehouses.

**Explicit results** no value.

**Local steps**

- For each tuple(index, warehouse) in enumerate(warehouses).
  - If not args.remaining\_qty.
    - Return no value.
  - Set row from self.get\_args().
  - Set key from tuple(args.item\_code, warehouse).
  - Set bin\_data from self.bin\_details.get(key).
  - If bin\_data.
    - Evaluate row.update(bin\_data).
  - Set args.allotted\_qty from 0.
  - If (bin\_data and bin\_data.get(“actual\_qty”) &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bin\_data → bin\_data.get(“actual\_qty”) &gt; 0.
    - Set args.allotted\_qty from bin\_data.get(“actual\_qty”) when args.required\_qty &gt; bin\_data.get(“actual\_qty”), otherwise args.required\_qty.
      - Value choice on args.required\_qty &gt; bin\_data.get(“actual\_qty”) — true gives bin\_data.get(“actual\_qty”), false gives args.required\_qty.
    - Update args.remaining\_qty using − args.allotted\_qty.
    - Update bin\_data at “actual\_qty” using − args.allotted\_qty.
  - If ((self.mrp\_warehouses and (args.allotted\_qty or index equals (len(warehouses) − 1))) or not self.mrp\_warehouses).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.mrp\_warehouses and (args.allotted\_qty or index equals (len(warehouses) − 1))) → not self.mrp\_warehouses.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.mrp\_warehouses → (args.allotted\_qty or index equals (len(warehouses) − 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.allotted\_qty → index equals (len(warehouses) − 1).
    - If not self.index.
      - Evaluate row.update(order\_data).
      - Update self.index using + 1.
    - Set args.warehouse from warehouse.
    - Evaluate row.update(args).
    - If self.purchase\_details.get(key).
      - Evaluate row.update(self.purchase\_details.get(key)).
    - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get args](operations-036.md#op-682a94f6367fbb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0554.json#L6701) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1210)

<a id="op-682a94f6367fbb"></a>
### Production Plan Report.get args

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_get_arguments`

**Inputs** self.

**Explicit results** Platform.\_dict(mapping(“work\_order” → empty text, “sales\_order” → empty text, “production\_item” → empty text, “production\_item\_name” → empty text, …)).

**Local steps**

- Return Platform.\_dict(mapping(“work\_order” → empty text, “sales\_order” → empty text, “production\_item” → empty text, “production\_item\_name” → empty text, …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0555.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1202)

<a id="op-5c98633552c93d"></a>
### Production Plan Report.get columns

`operation_enterprise_manufacturing_report_production_planning_report_business_behavior_production_plan_report_get_columns`

**Inputs** self.

**Local steps**

- Set based\_on from self.filters.based\_on.
- Set self.columns from list(mapping(“label” → translated “ID”, “options” → based\_on, “fieldname” → “name”, “fieldtype” → “Link”, …), mapping(“label” → translated “Item Code”, “fieldname” → “production\_item”, “fieldtype” → “Link” ….
- Set tuple(fieldname, fieldtype) from tuple(“delivery\_date”, “Date”).
- If (self.filters.based\_on equals “Sales Order” and self.filters.order\_by equals “Total Amount”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.based\_on equals “Sales Order” → self.filters.order\_by equals “Total Amount”.
  - Set tuple(fieldname, fieldtype) from tuple(“base\_grand\_total”, “Currency”).
- Otherwise.
  - If self.filters.based\_on equals “Material Request”.
    - Set fieldname from “schedule\_date”.
  - Otherwise.
    - If self.filters.based\_on equals “Work Order”.
      - Set fieldname from “planned\_start\_date”.
- Evaluate self.columns.append(mapping(“label” → translated self.filters.order\_by, “fieldname” → fieldname, “fieldtype” → fieldtype, “width” → 100)).
- Evaluate self.columns.extend(list(mapping(“label” → translated “Raw Material Code”, “fieldname” → “item\_code”, “fieldtype” → “Link”, “options” → “Item”, …), mapping(“label” → translated “Raw Material Name”, “fieldn ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0555.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1204)

## Report · Quality inspection summary

<a id="op-163a5d07a47a8e"></a>
### Execute

`operation_enterprise_manufacturing_report_quality_inspection_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart\_data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set data from get\_data(filters).
- Set columns from get\_columns(filters).
- Set chart\_data from get\_chart\_data(data, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1213)

<a id="op-a1127ddd7d0413"></a>
### Get data

`operation_enterprise_manufacturing_report_quality_inspection_summary_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Quality Inspection” via get\_list.

**Explicit results** Platform.get\_list(“Quality Inspection”, fields = fields, filters = query\_filters, order\_by = “report\_date asc”).

**Local steps**

- Set query\_filters from mapping(“docstatus” → 1).
- Set fields from list(“name”, “status”, “report\_date”, “item\_code”, …).
- For each field in list(“status”, “item\_code”, “status”, “inspected\_by”).
  - If filters.get(field).
    - Set query\_filters at field from tuple(“in”, filters.get(field)).
- Set query\_filters at “report\_date” from list(“between”, list(filters.get(“from\_date”), filters.get(“to\_date”))).
- Return Platform.get\_list(“Quality Inspection”, fields = fields, filters = query\_filters, order\_by = “report\_date asc”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1216)
