# Production · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Production plan

[Record definition](../../../../data/record-types/production_plan.json)

<a id="op-98463244b91b3c"></a>
### Production Plan.combine so items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_combine_sales_order_items`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If (self.combine\_items and self.po\_items and len(self.po\_items) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.combine\_items → self.po\_items → len(self.po\_items) &gt; 0.
  - Set items from list().
  - For each row in self.po\_items.
    - Evaluate items.append(Platform.\_dict(mapping(“parent” → row.sales\_order, “item\_code” → row.item\_code, “warehouse” → row.warehouse, “qty” → row.pending\_qty, …))).
  - Evaluate self.set(“po\_items”, list()).
  - Evaluate self.add\_items(items).
- Otherwise.
  - Evaluate self.get\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add items](operations-031.md#op-064349df8b3a2f), [get items](operations-031.md#op-33bc82032d18e3).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L577)

<a id="op-33bc82032d18e3"></a>
### Production Plan.get items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_items`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set(“po\_items”, list()).
- If self.get\_items\_from equals “Sales Order”.
  - Evaluate self.get\_so\_items().
- Otherwise.
  - If self.get\_items\_from equals “Material Request”.
    - Evaluate self.get\_mr\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get so items](operations-031.md#op-0407152eb6f6f9), [get mr items](operations-031.md#op-87e5fad6527dde).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L583)

<a id="op-b9779a696ae18d"></a>
### Production Plan.get so mr list

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_sales_order_material_request_list`

**Inputs** self, field, table.

**Explicit results** so\_mr\_list.

**Local steps**

- Set so\_mr\_list from list of d.get(field) for d drawn from self.get(table) where d.get(field).
  - Draw d from self.get(table), keep a combination only if (d.get(field)).
- Return so\_mr\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L960) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L589)

<a id="op-710e615eaf2d74"></a>
### Production Plan.get bom item condition

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_bill_of_materials_item_condition`

**Inputs** self.

**Record and data access** read mapping(“doctype” → “BOM”, “item” → self.item\_code, “docstatus” → 1) via exists · read “Item” via get\_value.

**Explicit results** bom\_item\_condition.

**Local steps**

- Set bom\_item\_condition from no value.
- Set has\_bom from Platform.db.exists(mapping(“doctype” → “BOM”, “item” → self.item\_code, “docstatus” → 1)).
- If not has\_bom.
  - Set bom from Platform.qb.DocType(“BOM”).
  - Set template\_item from Platform.db.get\_value(“Item”, self.item\_code, list(“variant\_of”)).
  - Set bom\_item\_condition from (bom.item equals template\_item or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bom.item equals template\_item → no value.
- Return bom\_item\_condition.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L582)

<a id="op-0407152eb6f6f9"></a>
### Production Plan.get so items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_sales_order_items`

**Inputs** self.

**Record and data access** read “Item” via exists.

**Explicit failure paths** validation helper — translated “Please fill the Sales Orders table”.

**Local steps**

- If (not self.get(“sales\_orders”) or not self.get\_so\_mr\_list(“sales\_order”, “sales\_orders”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“sales\_orders”) → not self.get\_so\_mr\_list(“sales\_order”, “sales\_orders”).
  - Call the validation error handler Platform.throw(translated “Please fill the Sales Orders table”, title = translated “Sales Orders Required”).
- Set so\_list from self.get\_so\_mr\_list(“sales\_order”, “sales\_orders”).
- Set bom from Platform.qb.DocType(“BOM”).
- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set items\_subquery from nested operand in the contract.qb.from\_(bom).select(bom.name).where(bom.is\_active equals 1).
- Set items\_query from nested operand in the contract(nested operand in the contract).select(so\_item.parent, so\_item.item\_code, so\_item.warehouse, nested operand in the contract.as\_(“qty”), …).distinct().where((((nested operand  ….
- If (self.item\_code and Platform.db.exists(“Item”, self.item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → Platform.db.exists(“Item”, self.item\_code).
  - Set items\_query from items\_query.where(so\_item.item\_code equals self.item\_code).
  - Set items\_subquery from items\_subquery.where((self.get\_bom\_item\_condition() or bom.item equals so\_item.item\_code)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_bom\_item\_condition() → bom.item equals so\_item.item\_code.
- Set items\_query from items\_query.where(ExistsCriterion(items\_subquery)).
- Set items from items\_query.run(as\_dict = true).
- For each item in items.
  - Set pending\_qty from (flt(item.qty) − max(item.work\_order\_qty, (flt(item.delivered\_qty) × item.conversion\_factor), 0)).
  - Set item.pending\_qty from min(pending\_qty, (flt(item.stock\_qty) − flt(item.production\_plan\_qty))).
- Set pi from Platform.qb.DocType(“Packed Item”).
- Set pending\_qty from nested operand in the contract.terms.Case().when(so\_item.work\_order\_qty &gt; so\_item.delivered\_qty, (((nested operand in the contract.qty − nested operand in the contract.work\_order\_qty) × pi.qty) ÷ so\_item.q ….
- Set packed\_items\_query from nested operand in the contract(nested operand in the contract).select(pi.parent, pi.item\_code, nested operand in the contract.as\_(“warehouse”), nested operand in the contract.as\_(“pending\_qty”), …).distinc ….
- If self.item\_code.
  - Set packed\_items\_query from packed\_items\_query.where(so\_item.item\_code equals self.item\_code).
- Set packed\_items from packed\_items\_query.run(as\_dict = true).
- Evaluate self.add\_items((items + packed\_items)).
- Evaluate self.calculate\_total\_planned\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get so mr list](operations-031.md#op-b9779a696ae18d), [get bom item condition](operations-031.md#op-710e615eaf2d74), [add items](operations-031.md#op-064349df8b3a2f), [calculate total planned qty](operations-030.md#op-e5caff857b0d05).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L959) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L588)

<a id="op-87e5fad6527dde"></a>
### Production Plan.get mr items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_material_request_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please fill the Material Requests table”.

**Local steps**

- If (not self.get(“material\_requests”) or not self.get\_so\_mr\_list(“material\_request”, “material\_requests”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“material\_requests”) → not self.get\_so\_mr\_list(“material\_request”, “material\_requests”).
  - Call the validation error handler Platform.throw(translated “Please fill the Material Requests table”, title = translated “Material Requests Required”).
- Set mr\_list from self.get\_so\_mr\_list(“material\_request”, “material\_requests”).
- Set bom from Platform.qb.DocType(“BOM”).
- Set mr\_item from Platform.qb.DocType(“Material Request Item”).
- Set items\_query from nested operand in the contract(nested operand in the contract).select(mr\_item.parent, mr\_item.name, mr\_item.item\_code, mr\_item.warehouse, …).distinct().where((((nested operand in the contract.parent.isin(m ….
- If self.item\_code.
  - Set items\_query from items\_query.where(mr\_item.item\_code equals self.item\_code).
- Set items from items\_query.run(as\_dict = true).
- For each item in items.
  - Set item.pending\_qty from max(min(flt(item.pending\_qty), (flt(item.stock\_qty) − flt(item.planned\_qty))), 0).
- Evaluate self.add\_items(items).
- Evaluate self.calculate\_total\_planned\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get so mr list](operations-031.md#op-b9779a696ae18d), [add items](operations-031.md#op-064349df8b3a2f), [calculate total planned qty](operations-030.md#op-e5caff857b0d05).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L584)

<a id="op-064349df8b3a2f"></a>
### Production Plan.add items

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_add_items`

**Inputs** self, items.

**Local steps**

- Set refs from mapping().
- For each data in items.
  - If not data.pending\_qty.
    - Continue with the next iteration or loop test.
  - Set item\_details from get\_item\_details(data.item\_code, throw = false).
  - If self.combine\_items.
    - Set bom\_no from item\_details.get(“bom\_no”).
    - If data.get(“bom\_no”).
      - Set bom\_no from data.get(“bom\_no”).
    - If bom\_no belongs to refs.
      - Evaluate refs at bom\_no at “so\_details”.append(mapping(“sales\_order” → data.parent, “sales\_order\_item” → data.name, “qty” → data.pending\_qty)).
      - Update refs at bom\_no at “qty” using + data.pending\_qty.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - Set refs at bom\_no from mapping(“qty” → data.pending\_qty, “po\_item\_ref” → data.name, “so\_details” → list()).
      - Evaluate refs at bom\_no at “so\_details”.append(mapping(“sales\_order” → data.parent, “sales\_order\_item” → data.name, “qty” → data.pending\_qty)).
  - Set bom\_no from (data.bom\_no or (item\_details and item\_details.get(“bom\_no”)) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.bom\_no → (item\_details and item\_details.get(“bom\_no”)) → empty text.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details → item\_details.get(“bom\_no”).
  - If not bom\_no.
    - Continue with the next iteration or loop test.
  - Set pi from self.append(“po\_items”, mapping(“warehouse” → data.warehouse, “item\_code” → data.item\_code, “description” → (data.description or item\_details.description), “stock\_uom” → ((item\_details and item\_details.sto ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.description → item\_details.description.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (item\_details and item\_details.stock\_uom) → empty text.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details → item\_details.stock\_uom.
  - Evaluate pi.\_set\_defaults().
  - If self.get\_items\_from equals “Sales Order”.
    - Set pi.sales\_order from data.parent.
    - Set pi.sales\_order\_item from data.name.
    - Set pi.description from data.description.
  - Otherwise.
    - If self.get\_items\_from equals “Material Request”.
      - Set pi.material\_request from data.parent.
      - Set pi.material\_request\_item from data.name.
      - Set pi.description from data.description.
- If refs.
  - For each po\_item in self.po\_items.
    - Set po\_item.planned\_qty from refs at po\_item.bom\_no at “qty”.
    - Set po\_item.pending\_qty from refs at po\_item.bom\_no at “qty”.
    - Set po\_item.sales\_order from empty text.
  - Evaluate self.add\_pp\_ref(refs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add pp ref](operations-031.md#op-8e0c8a9c0670c9).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L938) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L569)

<a id="op-8e0c8a9c0670c9"></a>
### Production Plan.add pp ref

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_add_production_plan_reference`

**Inputs** self, refs.

**Local steps**

- For each bom\_no in refs.
  - For each so\_detail in refs at bom\_no at “so\_details”.
    - Evaluate self.append(“prod\_plan\_references”, mapping(“item\_reference” → refs at bom\_no at “po\_item\_ref”, “sales\_order” → so\_detail at “sales\_order”, “sales\_order\_item” → so\_detail at “sales\_order\_item”, “qty” → so\_ ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L571)

<a id="op-d90f44ac9de641"></a>
### Production Plan.calculate total produced qty

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_calculate_total_produced_quantity`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.total\_produced\_qty from 0.
- For each d in self.po\_items.
  - Update self.total\_produced\_qty using + flt(d.produced\_qty).
- Evaluate self.db\_set(“total\_produced\_qty”, self.total\_produced\_qty, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0487.json#L497) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L945) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L576)

<a id="op-29bb7dde7ac105"></a>
### Production Plan.update produced pending qty

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_update_produced_pending_quantity`

**Inputs** self, produced\_qty, production\_plan\_item.

**State and service calls** call db\_update on data.

**Local steps**

- For each data in self.po\_items.
  - If data.name equals production\_plan\_item.
    - Set data.produced\_qty from produced\_qty.
    - Set data.pending\_qty from flt((data.planned\_qty − produced\_qty)).
    - Evaluate data.db\_update().
- Evaluate self.calculate\_total\_produced\_qty().
- Evaluate self.update\_status\_and\_bin\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate total produced qty](operations-031.md#op-d90f44ac9de641), [update status and bin qty](operations-031.md#op-0b0033c68caf38).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L981) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L610)

<a id="op-0b0033c68caf38"></a>
### Production Plan.update status and bin qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_update_status_and_bin_qty`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set previous\_status from self.status.
- Evaluate self.set\_status().
- Evaluate self.db\_set(“status”, self.status).
- If (previous\_status differs from self.status and “Completed” belongs to tuple(previous\_status, self.status)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_status differs from self.status → “Completed” belongs to tuple(previous\_status, self.status).
  - Evaluate self.update\_bin\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-031.md#op-1e85174448a70e), [update bin qty](operations-031.md#op-cb664731621a42).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L952)

<a id="op-fb39103e92f6c8"></a>
### Production Plan.before submit

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_sales\_order\_planned\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate sales order planned qty](operations-031.md#op-1a1098e885b4c5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L945)

<a id="op-1a1098e885b4c5"></a>
### Production Plan.validate sales order planned qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_validate_sales_order_planned_qty`

**Inputs** self.

**Record and data access** read “Sales Order Item” via get\_all · read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot plan {0} {1} of Item {2} against Sales Order {3}. Only {4} {1} is left to plan.”.format(qty, row.stock\_uom, Platform.bold(row.item\_code), sales\_order, …).

**Local steps**

- Set planned\_qty from self.get\_so\_item\_planned\_qty().
- If not planned\_qty.
  - Return no value.
- Set already\_planned from self.get\_so\_wise\_planned\_qty(list(set of key at 0 for key drawn from planned\_qty)).
  - Draw key from planned\_qty.
- Set so\_items from mapping of row.name → row for row drawn from Platform.get\_all(“Sales Order Item”, filters = mapping(“name” → tuple(“in”, list of key at 1 for key drawn from planned\_qty)), fields = list(“name”, “item\_code” ….
  - Draw row from Platform.get\_all(“Sales Order Item”, filters = mapping(“name” → tuple(“in”, list of key at 1 for key drawn from planned\_qty)), fields = list(“name”, “item\_code”, “stock\_qty”, “stock\_uom”)).
  - Draw key from planned\_qty.
- Set allowance from flt(Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_sales\_order”)).
- Set precision from Platform.get\_precision(“Production Plan Item”, “planned\_qty”).
- For each tuple(tuple(sales\_order, so\_item), qty) in planned\_qty.items().
  - Set row from so\_items at so\_item.
  - Set unplanned\_qty from flt(((flt(row.stock\_qty) × (1 + (allowance ÷ 100))) − flt(already\_planned.get(tuple(sales\_order, so\_item)))), precision).
  - If flt(qty, precision) &gt; unplanned\_qty.
    - Call the validation error handler Platform.throw(translated “Cannot plan {0} {1} of Item {2} against Sales Order {3}. Only {4} {1} is left to plan.”.format(qty, row.stock\_uom, Platform.bold(row.item\_code), sales\_order, …), title = translat ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get so item planned qty](operations-031.md#op-60d50039694461), [get so wise planned qty](operations-031.md#op-f9bfcadbe98bb7).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “overproduction\_percentage\_for\_sales\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L955)

<a id="op-60d50039694461"></a>
### Production Plan.get so item planned qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_get_so_item_planned_qty`

**Inputs** self.

**Explicit results** planned\_qty.

**Local steps**

- Set planned\_qty from mapping().
- For each row in self.po\_items.
  - If (row.sales\_order and row.sales\_order\_item and not row.product\_bundle\_item).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.sales\_order → row.sales\_order\_item → not row.product\_bundle\_item.
    - Set key from tuple(row.sales\_order, row.sales\_order\_item).
    - Set planned\_qty at key from (planned\_qty.get(key, 0) + flt(row.planned\_qty)).
- Return planned\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L948)

<a id="op-314244672e9f33"></a>
### Production Plan.on submit

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_bin\_qty().
- Evaluate self.update\_sales\_order().
- Evaluate self.add\_reference\_to\_raw\_materials().
- Evaluate self.update\_stock\_reservation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update bin qty](operations-031.md#op-cb664731621a42), [update sales order](operations-031.md#op-e6e807c846fe63), [add reference to raw materials](operations-031.md#op-67bfef4440e4ce), [update stock reservation](operations-031.md#op-33f0592fa09a2e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0487.json#L887) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L970) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L599)

<a id="op-70aefef239b523"></a>
### Production Plan.on cancel

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.delete\_draft\_work\_order().
- Evaluate self.update\_bin\_qty().
- Evaluate self.update\_sales\_order().
- Evaluate self.update\_stock\_reservation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete draft work order](operations-031.md#op-e7ca184920024e), [update bin qty](operations-031.md#op-cb664731621a42), [update sales order](operations-031.md#op-e6e807c846fe63), [update stock reservation](operations-031.md#op-33f0592fa09a2e).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L968) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L597)

<a id="op-33f0592fa09a2e"></a>
### Production Plan.update stock reservation

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_update_stock_reservation`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.reserve\_stock.
  - Return no value.
- Evaluate reserve\_stock\_for\_production\_plan(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0487.json#L1475) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L984) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L613)

<a id="op-67bfef4440e4ce"></a>
### Production Plan.add reference to raw materials

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_add_reference_to_raw_materials`

**Inputs** self.

**Record and data access** read “BOM” via get\_cached\_value.

**State and service calls** call db\_set on item.

**Explicit failure paths** validation helper — translated “Sub assembly item references are missing. Please fetch the sub assemblies and raw materials again.”.

**Local steps**

- For each item in self.mr\_items.
  - If reference bound to next(generator of sa\_item.name for sa\_item drawn from self.sub\_assembly\_items where (sa\_item.production\_item equals item.main\_item\_code and sa\_item.bom\_no equals item.from\_bom), no value).
    - Draw sa\_item from self.sub\_assembly\_items, keep a combination only if ((sa\_item.production\_item equals item.main\_item\_code and sa\_item.bom\_no equals item.from\_bom)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sa\_item.production\_item equals item.main\_item\_code → sa\_item.bom\_no equals item.from\_bom.
    - Evaluate item.db\_set(“sub\_assembly\_item\_reference”, reference).
  - Otherwise.
    - If (self.reserve\_stock and item.main\_item\_code and item.from\_bom and item.main\_item\_code differs from Platform.get\_cached\_value(“BOM”, item.from\_bom, “item”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reserve\_stock → item.main\_item\_code → item.from\_bom → item.main\_item\_code differs from Platform.get\_cached\_value(“BOM”, item.from\_bom, “item”).
      - Call the validation error handler Platform.throw(translated “Sub assembly item references are missing. Please fetch the sub assemblies and raw materials again.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“BOM”, item.from\_bom, “item”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0487.json#L1551) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L572)

<a id="op-e6e807c846fe63"></a>
### Production Plan.update sales order

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_update_sales_order`

**Inputs** self.

**State and service calls** request set\_value on “Sales Order Item”.

**Explicit results** no value.

**Local steps**

- Set so\_items from set of tuple(row.sales\_order, row.sales\_order\_item) for row drawn from (self.po\_items + self.prod\_plan\_references) where (row.sales\_order and row.sales\_order\_item).
  - Draw row from (self.po\_items + self.prod\_plan\_references), keep a combination only if ((row.sales\_order and row.sales\_order\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.sales\_order → row.sales\_order\_item.
- If not so\_items.
  - Return no value.
- Set so\_wise\_planned\_qty from self.get\_so\_wise\_planned\_qty(list(set of key at 0 for key drawn from so\_items)).
  - Draw key from so\_items.
- For each key in so\_items.
  - Evaluate Platform.db.set\_value(“Sales Order Item”, key at 1, “production\_plan\_qty”, flt(so\_wise\_planned\_qty.get(key))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get so wise planned qty](operations-031.md#op-f9bfcadbe98bb7).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L612)

<a id="op-f9bfcadbe98bb7"></a>
### Production Plan.get so wise planned qty

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_get_sales_order_wise_planned_quantity`

**Inputs** sales\_orders.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “Production Plan Item” via get\_all.

**Explicit results** so\_wise\_planned\_qty.

**Local steps**

- Set so\_wise\_planned\_qty from Platform.\_dict().
- Set data from Platform.get\_all(“Production Plan Item”, fields = list(“sales\_order”, “sales\_order\_item”, mapping(“SUM” → “planned\_qty”, “as” → “qty”)), filters = mapping(“sales\_order” → tuple(“in”, sales\_orders), “docsta ….
- Update data using + get\_planned\_qty\_of\_references(sales\_orders).
- For each row in data.
  - Set key from tuple(row.sales\_order, row.sales\_order\_item).
  - Set so\_wise\_planned\_qty at key from (flt(so\_wise\_planned\_qty.get(key)) + flt(row.qty)).
- Return so\_wise\_planned\_qty.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L961) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L590)

<a id="op-cb664731621a42"></a>
### Production Plan.update bin qty

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_update_bin_quantity`

**Inputs** self, item\_codes = no value.

**Record and data access** resolve a document from “Bin” via get\_doc.

**Local steps**

- Set rows from list of tuple(d.item\_code, d.warehouse) for d drawn from self.mr\_items.
  - Draw d from self.mr\_items.
- Update rows using + list of tuple(d.production\_item, d.fg\_warehouse) for d drawn from self.sub\_assembly\_items where d.type\_of\_manufacturing equals “In House”.
  - Draw d from self.sub\_assembly\_items, keep a combination only if (d.type\_of\_manufacturing equals “In House”).
- For each tuple(item\_code, warehouse) in rows.
  - If (warehouse and (item\_codes is identical to no value or item\_code belongs to item\_codes)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → (item\_codes is identical to no value or item\_code belongs to item\_codes).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_codes is identical to no value → item\_code belongs to item\_codes.
    - Set bin\_name from get\_or\_make\_bin(item\_code, warehouse).
    - Set bin from Platform.get\_doc(“Bin”, bin\_name, for\_update = true).
    - Evaluate bin.update\_reserved\_qty\_for\_production\_plan().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L608)

<a id="op-e7ca184920024e"></a>
### Production Plan.delete draft work order

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_delete_draft_work_order`

**Inputs** self.

**Record and data access** read “Work Order” via get\_all.

**State and service calls** request delete\_doc for “Work Order”.

**Local steps**

- For each d in Platform.get\_all(“Work Order”, fields = list(“name”), filters = mapping(“docstatus” → 0, “production\_plan” → tuple(“=”, self.name))).
  - Evaluate Platform.delete\_doc(“Work Order”, d.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0487.json#L2843) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L580)

<a id="op-e75cc93a75064f"></a>
### Production Plan.cancel untouched stock reservations

`operation_enterprise_binding_enterprise_manufacturing_doctype_production_plan_production_plan_productionplan_cancel_untouched_stock_reservations`

**Inputs** self.

**Record and data access** read “Stock Reservation Entry” via get\_all · resolve a document from “Stock Reservation Entry” via get\_doc.

**State and service calls** call cancel on sre\_doc.

**Local steps**

- Set sre\_list from Platform.get\_all(“Stock Reservation Entry”, filters = mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “docstatus” → 1, “status” → tuple(“in”, list(“Reserved”, “Partially Reserved”))), pluc ….
- For each sre\_name in sre\_list.
  - Set sre\_doc from Platform.get\_doc(“Stock Reservation Entry”, sre\_name).
  - Set sre\_doc.flags.ignore\_permissions from true.
  - Evaluate sre\_doc.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L946)

<a id="op-1e85174448a70e"></a>
### Production Plan.set status

`operation_enterprise_manufacturing_record_definitions_production_plan_business_behavior_production_plan_set_status`

**Inputs** self, close = no value, update\_bin = false.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only a submitted Production Plan can be closed or re-opened”.

**Local steps**

- If close is distinct from no value.
  - Evaluate self.reload().
  - <a id="op-1e85174448a70e-guard-4"></a>If self.docstatus differs from 1.
    - Call the validation error handler Platform.throw(translated “Only a submitted Production Plan can be closed or re-opened”).
- Evaluate self.check\_permission(“write”).
- If (close is identical to no value and self.status equals “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in close is identical to no value → self.status equals “Closed”.
  - Return no value.
- Set self.status from mapping(0 → “Draft”, 1 → “Submitted”, 2 → “Cancelled”).get(self.docstatus).
- If close.
  - Evaluate self.db\_set(“status”, “Closed”).
  - Evaluate self.cancel\_untouched\_stock\_reservations().
  - Evaluate self.update\_bin\_qty().
  - Return no value.
- <a id="op-1e85174448a70e-guard-20"></a>If self.total\_produced\_qty &gt; 0.
  - Set self.status from “In Process”.
  - If self.all\_items\_completed().
    - Set self.status from “Completed”.
- If self.status differs from “Completed”.
  - Evaluate self.update\_requested\_status().
  - Evaluate self.update\_ordered\_status().
- If close is distinct from no value.
  - Evaluate self.db\_set(“status”, self.status).
- If (update\_bin and self.docstatus equals 1 and self.status differs from “Completed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_bin → self.docstatus equals 1 → self.status differs from “Completed”.
  - Evaluate self.update\_bin\_qty().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Production Plan can be closed or re-opened”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-1e85174448a70e-guard-4)
- At the comparison self.total\_produced\_qty &gt; 0, self.total\_produced\_qty = 1 selects the branch that assigns “In Process” to self.status. With self.total\_produced\_qty = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-1e85174448a70e-guard-20)

**Methods declared on this owner** [cancel untouched stock reservations](operations-031.md#op-e75cc93a75064f), [update bin qty](operations-031.md#op-cb664731621a42), [all items completed](operations-032.md#op-17ae94613df0b1), [update requested status](operations-032.md#op-0bdffa0df7362d), [update ordered status](operations-032.md#op-8c7038bd1db380).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L976) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L605)
