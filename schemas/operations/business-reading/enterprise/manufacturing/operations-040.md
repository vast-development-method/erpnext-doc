# Production · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Work order

[Record definition](../../../../data/record-types/work_order.json)

<a id="op-6c6e6700985d19"></a>
### Work Order.before submit

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_before_submit`

**Inputs** self.

**Local steps**

- If self.production\_plan.
  - Evaluate ProductionPlanWorkOrderQuantities(self.production\_plan).validate\_work\_order(self).
- Evaluate self.create\_serial\_no\_batch\_no().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create serial no batch no](operations-040.md#op-ba0aad9c279d96).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L3222) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L789)

<a id="op-0775330092d141"></a>
### Work Order.on submit

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_warehouse().
- Evaluate self.update\_work\_order\_qty\_in\_sales\_orders().
- Evaluate self.update\_ordered\_qty().
- Evaluate self.update\_reserved\_qty\_for\_production().
- Evaluate self.update\_completed\_qty\_in\_material\_request().
- Evaluate self.update\_planned\_qty().
- Evaluate self.create\_job\_card().
- Evaluate self.update\_subcontracting\_inward\_order\_received\_items().
- If self.reserve\_stock.
  - Evaluate self.update\_stock\_reservation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate warehouse](operations-039.md#op-853e07d5695a23), [update work order qty in sales orders](operations-040.md#op-4dd2788d870eea), [update ordered qty](operations-040.md#op-a2189321370169), [update reserved qty for production](operations-041.md#op-d40b48267db3bf), [update completed qty in material request](operations-041.md#op-26e29b30c59274), [update planned qty](operations-040.md#op-3d1e585dffd3ff), [create job card](operations-040.md#op-726dbc64c043d5), [update subcontracting inward order received items](operations-040.md#op-62168b44418fa5), [update stock reservation](operations-040.md#op-4d75fcf6a13105).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L804)

<a id="op-9222e6db84cc4e"></a>
### Work Order.on cancel

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.validate\_cancel().
- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.on\_close\_or\_cancel().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate cancel](operations-040.md#op-e7fce116f4b24d), [on close or cancel](operations-040.md#op-d71b13e6eef616).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0533.json#L3658) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L801)

<a id="op-d71b13e6eef616"></a>
### Work Order.on close or cancel

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_on_close_or_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_work\_order\_qty\_in\_sales\_orders().
- Evaluate self.update\_completed\_qty\_in\_material\_request().
- Evaluate self.update\_planned\_qty().
- Evaluate self.update\_ordered\_qty().
- Evaluate self.update\_reserved\_qty\_for\_production().
- If self.reserve\_stock.
  - Evaluate self.update\_stock\_reservation().
- Evaluate self.update\_subcontracting\_inward\_order\_received\_items().
- Evaluate self.discard\_draft\_job\_cards().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update work order qty in sales orders](operations-040.md#op-4dd2788d870eea), [update completed qty in material request](operations-041.md#op-26e29b30c59274), [update planned qty](operations-040.md#op-3d1e585dffd3ff), [update ordered qty](operations-040.md#op-a2189321370169), [update reserved qty for production](operations-041.md#op-d40b48267db3bf), [update stock reservation](operations-040.md#op-4d75fcf6a13105), [update subcontracting inward order received items](operations-040.md#op-62168b44418fa5), [discard draft job cards](operations-040.md#op-a0da9e9b8b5359).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L802)

<a id="op-a0da9e9b8b5359"></a>
### Work Order.discard draft job cards

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_discard_draft_job_cards`

**Inputs** self.

**Record and data access** read “Job Card” via get\_all · resolve a document from “Job Card” via get\_doc.

**Local steps**

- For each name in Platform.get\_all(“Job Card”, filters = mapping(“work\_order” → self.name, “docstatus” → 0), pluck = “name”).
  - Set job\_card from Platform.get\_doc(“Job Card”, name).
  - Set job\_card.flags.ignore\_permissions from true.
  - Evaluate job\_card.discard().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L39) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1049)

<a id="op-4d75fcf6a13105"></a>
### Work Order.update stock reservation

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_update_stock_reservation`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate reserve\_stock\_for\_work\_order(self).
- Evaluate self.db\_set(“status”, self.get\_status()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get status](operations-039.md#op-7a6d94ec35a98e).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1105)

<a id="op-bda3c20d4a7ba0"></a>
### Work Order.set qty change

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_quantity_change`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Received Item” via get\_all.

**Local steps**

- If scio\_item\_name bound to self.get(“subcontracting\_inward\_order\_item”).
  - Set self.qty\_change from Platform.\_dict().
  - Set data from Platform.get\_all(“Subcontracting Inward Order Received Item”, mapping(“reference\_name” → scio\_item\_name, “docstatus” → 1, “is\_customer\_provided\_item” → 1), list(“rm\_item\_code”, “required\_qty as bom\_qty”, “ ….
  - For each d in data.
    - Set wo\_item from next(generator of wo\_item for wo\_item drawn from self.get(“required\_items”) where wo\_item.item\_code equals d.rm\_item\_code, no value).
      - Draw wo\_item from self.get(“required\_items”), keep a combination only if (wo\_item.item\_code equals d.rm\_item\_code).
    - If (wo\_item and d.work\_order\_qty equals d.bom\_qty and d.received\_qty &gt; d.bom\_qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in wo\_item → d.work\_order\_qty equals d.bom\_qty → d.received\_qty &gt; d.bom\_qty.
      - Set self.qty\_change at wo\_item.name from (d.received\_qty − d.bom\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L816)

<a id="op-62168b44418fa5"></a>
### Work Order.update subcontracting inward order received items

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_subcontracting_inward_order_received_items`

**Inputs** self.

**Record and data access** read “Subcontracting Inward Order Received Item” via get\_all.

**Explicit results** no value.

**Local steps**

- If not scio\_item\_name bound to self.get(“subcontracting\_inward\_order\_item”).
  - Return no value.
- Set scio\_rm\_data from Platform.get\_all(“Subcontracting Inward Order Received Item”, filters = mapping(“reference\_name” → scio\_item\_name, “docstatus” → 1, “rm\_item\_code” → list(“in”, list of d.item\_code for d drawn from self.get ….
  - Draw d from self.get(“required\_items”).
- If not scio\_rm\_data.
  - Return no value.
- Set allocated\_qty from get\_work\_order\_allocated\_qty(scio\_item\_name, list of d.rm\_item\_code for d drawn from scio\_rm\_data).
  - Draw d from scio\_rm\_data.
- Set table from Platform.qb.DocType(“Subcontracting Inward Order Received Item”).
- Set case\_expr from Case().
- For each item in scio\_rm\_data.
  - Set case\_expr from case\_expr.when(table.rm\_item\_code equals item.rm\_item\_code, flt(allocated\_qty.get(item.rm\_item\_code))).
- Evaluate nested operand in the contract(nested operand in the contract).set(table.work\_order\_qty, case\_expr).where((nested operand in the contract.name.isin(list of nested operand in the contract.name for d drawn f ….run().
  - Draw d from scio\_rm\_data.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L833)

<a id="op-ba0aad9c279d96"></a>
### Work Order.create serial no batch no

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_create_serial_number_batch_number`

**Inputs** self.

**Record and data access** read “Manufacturing Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If self.track\_semi\_finished\_goods.
  - Return no value.
- If not (self.has\_serial\_no or self.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_serial\_no → self.has\_batch\_no.
  - Return no value.
- If not cint(Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”)).
  - Return no value.
- If self.has\_batch\_no.
  - Set remaining\_qty from (flt(self.qty) − self.reuse\_batches\_of\_amended\_order()).
  - If remaining\_qty &gt; 0.
    - Evaluate self.create\_batch\_for\_finished\_good(remaining\_qty).
- Set args from mapping(“item\_code” → self.production\_item, “work\_order” → self.name).
- If self.has\_serial\_no.
  - Set remaining\_qty from (flt(self.qty) − self.reuse\_serial\_nos\_of\_amended\_order()).
  - If remaining\_qty &gt; 0.
    - Evaluate self.make\_serial\_nos(args, remaining\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [reuse batches of amended order](operations-040.md#op-4443a047c5a86f), [create batch for finished good](operations-040.md#op-1c1fbd751142e3), [reuse serial nos of amended order](operations-040.md#op-45971544513897), [make serial nos](operations-040.md#op-101b62588e08c3).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Manufacturing Settings”, “make\_serial\_no\_batch\_from\_work\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L793)

<a id="op-4443a047c5a86f"></a>
### Work Order.reuse batches of amended order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_reuse_batches_of_amended_order`

**Inputs** self.

**Record and data access** read “Batch” via get\_all.

**Explicit results** 0 · sum(generator of flt(d.qty\_to\_produce) for d drawn from batches).

**Local steps**

- If not self.amended\_from.
  - Return 0.
- Set batches from Platform.get\_all(“Batch”, filters = mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.amended\_from, “item” → self.production\_item), fields = list(“name”, “qty\_to\_produce”)).
- If not batches.
  - Return 0.
- Set batch from Platform.qb.DocType(“Batch”).
- Evaluate nested operand in the contract(nested operand in the contract).set(batch.reference\_name, self.name).where(batch.name.isin(list of d.name for d drawn from batches)).run().
  - Draw d from batches.
- Return sum(generator of flt(d.qty\_to\_produce) for d drawn from batches).
  - Draw d from batches.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1085)

<a id="op-45971544513897"></a>
### Work Order.reuse serial nos of amended order

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_reuse_serial_nos_of_amended_order`

**Inputs** self.

**Record and data access** read “Serial No” via get\_all.

**Explicit results** 0 · len(serial\_nos).

**Local steps**

- If not self.amended\_from.
  - Return 0.
- Set serial\_nos from Platform.get\_all(“Serial No”, filters = mapping(“work\_order” → self.amended\_from, “item\_code” → self.production\_item, “status” → “Inactive”), order\_by = “creation”, limit = cint(self.qty), pluck = “name”).
- If serial\_nos.
  - Set serial\_no from Platform.qb.DocType(“Serial No”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(serial\_no.work\_order, self.name).where(serial\_no.name.isin(serial\_nos)).run().
- Return len(serial\_nos).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1086)

<a id="op-96162935ce18c0"></a>
### Work Order.get batch capacity

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_get_batch_capacity`

**Inputs** self.

**Record and data access** read “Batch” via get\_all.

**Explicit results** list of list(d.name, (cint(d.qty\_to\_produce) − cint(used.get(d.name)))) for d drawn from batches.

**Local steps**

- Set batches from Platform.get\_all(“Batch”, filters = mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name), fields = list(“name”, “qty\_to\_produce”), order\_by = “creation”).
- Set serial\_no from Platform.qb.DocType(“Serial No”).
- Set used from dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(serial\_no.batch\_no).run()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of d.name for d drawn from batches → list(empty text).
  - Draw d from batches.
- Return list of list(d.name, (cint(d.qty\_to\_produce) − cint(used.get(d.name)))) for d drawn from batches.
  - Draw d from batches.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L42) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1052)

<a id="op-1c1fbd751142e3"></a>
### Work Order.create batch for finished good

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_create_batch_for_finished_good`

**Inputs** self, total\_qty = no value.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set total\_qty from (total\_qty or self.qty).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in total\_qty → self.qty.
- If not self.batch\_size.
  - Set self.batch\_size from self.qty.
- If not Platform.get\_cached\_value(“Item”, self.production\_item, “create\_new\_batch”).
  - Evaluate self.throw\_missing\_item\_setting(“create\_new\_batch”).
- While total\_qty &gt; 0.
  - Set qty from self.batch\_size.
  - If self.batch\_size ≥ total\_qty.
    - Set qty from total\_qty.
  - If total\_qty &gt; self.batch\_size.
    - Update total\_qty using − self.batch\_size.
  - Otherwise.
    - Set qty from total\_qty.
    - Set total\_qty from 0.
  - Evaluate make\_batch(Platform.\_dict(mapping(“item” → self.production\_item, “qty\_to\_produce” → qty, “reference\_doctype” → self.doctype, “reference\_name” → self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw missing item setting](operations-040.md#op-f7a3a4bda58699).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.production\_item, “create\_new\_batch”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L792)

<a id="op-101b62588e08c3"></a>
### Work Order.make serial nos

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_make_serial_numbers`

**Inputs** self, args, qty = no value.

**Record and data access** read “Item” via get\_cached\_value.

**State and service calls** request bulk\_insert on “Serial No”.

**Explicit results** no value.

**Local steps**

- Set item\_details from Platform.get\_cached\_value(“Item”, self.production\_item, list(“serial\_no\_series”, “item\_name”, “description”), as\_dict = 1).
- Set batch\_capacity from self.get\_batch\_capacity() when self.has\_batch\_no, otherwise list().
  - Value choice on self.has\_batch\_no — true gives self.get\_batch\_capacity(), false gives list().
- If not item\_details.serial\_no\_series.
  - Evaluate self.throw\_missing\_item\_setting(“serial\_no\_series”).
- Set serial\_no\_values from Platform.\_dict(company = self.company, item\_code = self.production\_item, item\_name = item\_details.item\_name, description = item\_details.description, …).
- Set serial\_nos from get\_available\_serial\_nos(item\_details.serial\_no\_series, (qty or self.qty), serial\_no\_values).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty → self.qty.
- If not serial\_nos.
  - Return no value.
- Set fields from list(“name”, “serial\_no”, “creation”, “modified”, …).
- Set serial\_nos\_details from list().
- For each serial\_no in serial\_nos.
  - Set batch\_no from no value.
  - For each capacity in batch\_capacity.
    - If capacity at 1 &gt; 0.
      - Set batch\_no from capacity at 0.
      - Update capacity at 1 using − 1.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate serial\_nos\_details.append(tuple(serial\_no, serial\_no, now(), now(), …)).
- Evaluate Platform.db.bulk\_insert(“Serial No”, fields = fields, values = set(serial\_nos\_details)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get batch capacity](operations-040.md#op-96162935ce18c0), [throw missing item setting](operations-040.md#op-f7a3a4bda58699).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.production\_item, list(“serial\_no\_series”, “item\_name”, “description”), as\_dict = 1) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L799)

<a id="op-726dbc64c043d5"></a>
### Work Order.create job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_create_job_card`

**Inputs** self.

**Record and data access** resolve a document from “Manufacturing Settings” via get\_doc.

**State and service calls** call db\_set on self.

**Local steps**

- Set manufacturing\_settings\_doc from Platform.get\_doc(“Manufacturing Settings”).
- Set enable\_capacity\_planning from not cint(manufacturing\_settings\_doc.disable\_capacity\_planning).
- Set plan\_days from get\_capacity\_planning\_days().
- For each tuple(idx, row) in enumerate(self.operations).
  - Set qty from get\_operation\_qty(self, row).
  - While qty &gt; 0.
    - Set qty from split\_qty\_based\_on\_batch\_size(self, row, qty).
    - If row.job\_card\_qty &gt; 0.
      - Evaluate self.prepare\_data\_for\_job\_card(row, idx, plan\_days, enable\_capacity\_planning).
- Set planned\_end\_date from (self.operations and self.operations at negative 1.planned\_end\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.operations → self.operations at negative 1.planned\_end\_time.
- If planned\_end\_date.
  - Evaluate self.db\_set(“planned\_end\_date”, planned\_end\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare data for job card](operations-040.md#op-f60d8db1a35387).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L38) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1048)

<a id="op-f60d8db1a35387"></a>
### Work Order.prepare data for job card

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_prepare_data_for_job_card`

**Inputs** self, row, idx, plan\_days, enable\_capacity\_planning.

**State and service calls** call db\_update on row.

**Explicit failure paths** validation helper with CapacityError — translated “Unable to find the time slot in the next {0} days for the operation {1}. Please increase the 'Capacity Plann …”.format(plan\_days, row.operation, get\_link\_to\_form(“Manufacturing Settings”, “Manu ….

**Local steps**

- Evaluate self.set\_operation\_start\_end\_time(row, idx).
- Set job\_card\_doc from create\_job\_card(self, row, auto\_create = true, enable\_capacity\_planning = enable\_capacity\_planning).
- If (enable\_capacity\_planning and job\_card\_doc).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in enable\_capacity\_planning → job\_card\_doc.
  - Set row.planned\_start\_time from job\_card\_doc.scheduled\_time\_logs at 0.from\_time.
  - Set row.planned\_end\_time from job\_card\_doc.scheduled\_time\_logs at negative 1.to\_time.
  - If date\_diff(row.planned\_end\_time, self.planned\_start\_date) &gt; plan\_days.
    - Evaluate Platform.message\_log.pop().
    - Call the validation error handler Platform.throw(translated “Unable to find the time slot in the next {0} days for the operation {1}. Please increase the 'Capacity Plann …”.format(plan\_days, row.operation, get\_link\_to\_form(“Manufacturing S ….
  - Evaluate row.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set operation start end time](operations-040.md#op-b79c79553fb358).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1080)

<a id="op-b79c79553fb358"></a>
### Work Order.set operation start end time

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_set_operation_start_end_time`

**Inputs** self, row, idx.

**Explicit failure paths** validation helper — translated “Capacity Planning Error, planned start time can not be same as end time”.

**Local steps**

- If idx equals 0.
  - Set row.planned\_start\_time from self.planned\_start\_date.
- Otherwise.
  - If self.operations at (idx − 1).sequence\_id.
    - If self.operations at (idx − 1).sequence\_id equals row.sequence\_id.
      - Set row.planned\_start\_time from self.operations at (idx − 1).planned\_start\_time.
    - Otherwise.
      - Set last\_ops\_with\_same\_sequence\_ids from sorted(list of op for op drawn from self.operations where op.sequence\_id equals self.operations at (idx − 1).sequence\_id, key = deferred anonymous expression).
        - Draw op from self.operations, keep a combination only if (op.sequence\_id equals self.operations at (idx − 1).sequence\_id).
      - Set row.planned\_start\_time from (get\_datetime(last\_ops\_with\_same\_sequence\_ids at negative 1.planned\_end\_time) + get\_mins\_between\_operations()).
  - Otherwise.
    - Set row.planned\_start\_time from (get\_datetime(self.operations at (idx − 1).planned\_end\_time) + get\_mins\_between\_operations()).
- Set row.planned\_end\_time from (get\_datetime(row.planned\_start\_time) + relativedelta(minutes = row.time\_in\_mins)).
- If row.planned\_start\_time equals row.planned\_end\_time.
  - Call the validation error handler Platform.throw(translated “Capacity Planning Error, planned start time can not be same as end time”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L81) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1091)

<a id="op-f7a3a4bda58699"></a>
### Work Order.throw missing item setting

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_throw_missing_item_setting`

**Inputs** self, fieldname.

**Explicit failure paths** validation helper — translated “Set {0} in Item {1} or disable {2} in {3}”.format(Platform.bold(translated nested operand in the contract.get\_meta(“Item”).get\_label(fieldname)), get\_link\_to\_form(“Item”, self.production\_item), ….

**Local steps**

- Call the validation error handler Platform.throw(translated “Set {0} in Item {1} or disable {2} in {3}”.format(Platform.bold(translated nested operand in the contract(nested operand in the contract).get\_label(fieldname)), get\_link\_to\_form( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1100)

<a id="op-e7fce116f4b24d"></a>
### Work Order.validate cancel

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_validate_cancel`

**Inputs** self.

**Record and data access** execute query text (SELECT, Stock Entry).

**Explicit failure paths** validation helper — translated “Stopped Work Order cannot be cancelled, Unstop it first to cancel” · validation helper — translated “Cannot cancel because submitted Stock Entry {0} exists”.format(Platform.utils.get\_link\_to\_form(“Stock Entry”, stock\_entry at 0 at 0)).

**Local steps**

- <a id="op-e7fce116f4b24d-guard-2"></a>If self.status equals “Stopped”.
  - Call the validation error handler Platform.throw(translated “Stopped Work Order cannot be cancelled, Unstop it first to cancel”).
- Set stock\_entry from Platform.db.sql(query text (SELECT, Stock Entry), self.name).
- If stock\_entry.
  - Call the validation error handler Platform.throw(translated “Cannot cancel because submitted Stock Entry {0} exists”.format(Platform.utils.get\_link\_to\_form(“Stock Entry”, stock\_entry at 0 at 0))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Stopped”, self.status = “Stopped” selects the branch that calls the validation-error handler with translated “Stopped Work Order cannot be cancelled, Unstop it first to cancel”. With self.status = “Draft”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e7fce116f4b24d-guard-2)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L840)

<a id="op-3d1e585dffd3ff"></a>
### Work Order.update planned qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_planned_quantity`

**Inputs** self.

**Record and data access** resolve a document from “Material Request” via get\_doc.

**Explicit results** no value.

**Local steps**

- If self.track\_semi\_finished\_goods.
  - Return no value.
- Evaluate update\_bin\_qty(self.production\_item, self.fg\_warehouse, mapping(“planned\_qty” → get\_planned\_qty(self.production\_item, self.fg\_warehouse))).
- If self.material\_request.
  - Set mr\_obj from Platform.get\_doc(“Material Request”, self.material\_request).
  - Evaluate mr\_obj.update\_requested\_qty(list(self.material\_request\_item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L827)

<a id="op-16e7a9419fcadf"></a>
### Work Order.set produced qty for sub assembly item

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_set_produced_quantity_for_subordinate_assembly_item`

**Inputs** self.

**State and service calls** request set\_value on “Production Plan Sub Assembly Item”.

**Local steps**

- Set table from Platform.qb.DocType(“Work Order”).
- Set query from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.produced\_qty)).where(((nested operand in the contract.production\_plan equals nested operand in the c ….run().
- Set produced\_qty from flt(query at 0 at 0) when query, otherwise 0.
  - Value choice on query — true gives flt(query at 0 at 0), false gives 0.
- Evaluate Platform.db.set\_value(“Production Plan Sub Assembly Item”, self.production\_plan\_sub\_assembly\_item, “wo\_produced\_qty”, produced\_qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L815)

<a id="op-a2189321370169"></a>
### Work Order.update ordered qty

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_ordered_quantity`

**Inputs** self.

**Record and data access** resolve a document from “Production Plan” via get\_doc.

**State and service calls** request set\_value on “Production Plan Item” · request set\_value on “Production Plan Sub Assembly Item”.

**Local steps**

- If (self.production\_plan and (self.production\_plan\_item or self.production\_plan\_sub\_assembly\_item)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.production\_plan → (self.production\_plan\_item or self.production\_plan\_sub\_assembly\_item).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.production\_plan\_item → self.production\_plan\_sub\_assembly\_item.
  - Set table from Platform.qb.DocType(“Work Order”).
  - Set query from nested operand in the contract.qb.from\_(table).select(Sum(table.qty)).where((table.production\_plan equals self.production\_plan bitwise and table.docstatus equals 1)).
  - If self.production\_plan\_item.
    - Set query from query.where(table.production\_plan\_item equals self.production\_plan\_item).
  - Otherwise.
    - If self.production\_plan\_sub\_assembly\_item.
      - Set query from query.where(table.production\_plan\_sub\_assembly\_item equals self.production\_plan\_sub\_assembly\_item).
  - Set query from query.run().
  - Set qty from flt(query at 0 at 0) when query, otherwise 0.
    - Value choice on query — true gives flt(query at 0 at 0), false gives 0.
  - If self.production\_plan\_item.
    - Evaluate Platform.db.set\_value(“Production Plan Item”, self.production\_plan\_item, “ordered\_qty”, qty).
  - Otherwise.
    - If self.production\_plan\_sub\_assembly\_item.
      - Evaluate Platform.db.set\_value(“Production Plan Sub Assembly Item”, self.production\_plan\_sub\_assembly\_item, “ordered\_qty”, qty).
  - Set doc from Platform.get\_doc(“Production Plan”, self.production\_plan).
  - Set doc.flags.ignore\_permissions from true.
  - Evaluate doc.update\_status\_and\_bin\_qty().
  - Evaluate doc.update\_bin\_qty(set of d.item\_code for d drawn from self.required\_items).
    - Draw d from self.required\_items.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L826)

<a id="op-4dd2788d870eea"></a>
### Work Order.update work order qty in sales orders

`operation_enterprise_binding_enterprise_manufacturing_doctype_work_order_work_order_workorder_update_work_order_qty_in_sales_orders`

**Inputs** self.

**Record and data access** read “Production Plan Item Reference” via exists.

**Local steps**

- If (self.production\_plan and Platform.db.exists(“Production Plan Item Reference”, mapping(“parent” → self.production\_plan))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.production\_plan → Platform.db.exists(“Production Plan Item Reference”, mapping(“parent” → self.production\_plan)).
  - Evaluate self.update\_work\_order\_qty\_in\_combined\_so().
- Otherwise.
  - Evaluate self.update\_work\_order\_qty\_in\_so().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update work order qty in combined so](operations-041.md#op-454162196d3239), [update work order qty in so](operations-040.md#op-4926d36e3337c6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1106)

<a id="op-4926d36e3337c6"></a>
### Work Order.update work order qty in so

`operation_enterprise_manufacturing_record_definitions_work_order_business_behavior_work_order_update_work_order_quantity_in_sales_order`

**Inputs** self.

**Record and data access** execute query text (SELECT, Product Bundle Item).

**State and service calls** request set\_value on “Sales Order Item”.

**Explicit results** no value.

**Local steps**

- If ((not self.sales\_order and not self.sales\_order\_item) or self.production\_plan\_sub\_assembly\_item).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not self.sales\_order and not self.sales\_order\_item) → self.production\_plan\_sub\_assembly\_item.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sales\_order → not self.sales\_order\_item.
  - Return no value.
- Set total\_bundle\_qty from 1.
- If self.product\_bundle\_item.
  - Set total\_bundle\_qty from Platform.db.sql(query text (SELECT, Product Bundle Item), Platform.db.escape(self.product\_bundle\_item)) at 0 at 0.
  - If not total\_bundle\_qty.
    - Set total\_bundle\_qty from 1.
- Set qty from self.get\_work\_order\_qty\_against\_sales\_order().
- Set work\_order\_qty from qty at 0 at 0 when (qty and qty at 0 at 0), otherwise 0.
  - Value choice on (qty and qty at 0 at 0) — true gives qty at 0 at 0, false gives 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty → qty at 0 at 0.
- Evaluate Platform.db.set\_value(“Sales Order Item”, self.sales\_order\_item, “work\_order\_qty”, flt((work\_order\_qty ÷ total\_bundle\_qty), 2)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get work order qty against sales order](operations-041.md#op-c8bdb41034bf45).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L837)
