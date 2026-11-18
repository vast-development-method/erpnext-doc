# Inventory and warehouses · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pick list

[Record definition](../../../../data/record-types/pick_list.json)

<a id="op-ca3966462e0f19"></a>
### Set target missing values

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_set_target_missing_values`

**Inputs** target.

**Local steps**

- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“set\_po\_nos”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“set\_po\_nos”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L956) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L453)

<a id="op-b03748aab7e4d9"></a>
### Stock entry exists

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_stock_entry_exists`

**Inputs** pick\_list\_name.

**Record and data access** read “Stock Entry” via exists.

**Explicit results** Platform.db.exists(“Stock Entry”, mapping(“pick\_list” → pick\_list\_name)).

**Local steps**

- Return Platform.db.exists(“Stock Entry”, mapping(“pick\_list” → pick\_list\_name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L209) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L454)

<a id="op-36dda22b0310a8"></a>
### Update stock entry based on job card

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_update_stock_entry_based_on_job_card`

**Inputs** pick\_list, stock\_entry, job\_card.

**Record and data access** read “Job Card” via get\_value.

**Explicit results** stock\_entry.

**Local steps**

- Set job\_card from Platform.db.get\_value(“Job Card”, job\_card, list(“name”, “work\_order”, “bom\_no”, “semi\_fg\_bom”, …), as\_dict = true).
- Set stock\_entry.purpose from “Material Transfer for Manufacture”.
- Set stock\_entry.job\_card from job\_card.name.
- Set stock\_entry.work\_order from job\_card.work\_order.
- Set stock\_entry.from\_bom from 1.
- Set stock\_entry.bom\_no from (job\_card.semi\_fg\_bom or job\_card.bom\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in job\_card.semi\_fg\_bom → job\_card.bom\_no.
- Set stock\_entry.fg\_completed\_qty from max((flt(job\_card.for\_quantity) − flt(job\_card.transferred\_qty)), 0).
- Set stock\_entry.to\_warehouse from job\_card.wip\_warehouse.
- Set stock\_entry.project from job\_card.project.
- Set job\_card\_items from get\_job\_card\_items\_by\_material\_request\_item(pick\_list).
- Set moved\_serial\_nos from get\_moved\_serial\_nos(pick\_list.locations, “transferred\_qty”).
- For each location in pick\_list.locations.
  - If get\_pending\_transfer\_stock\_qty(location) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set item from Platform.\_dict().
  - Evaluate update\_common\_item\_properties(item, location, moved\_serial\_nos).
  - Set item.t\_warehouse from job\_card.wip\_warehouse.
  - Set item.job\_card\_item from job\_card\_items.get(location.material\_request\_item).
  - Evaluate stock\_entry.append(“items”, item).
- Return stock\_entry.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L961) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L458)

<a id="op-034eb712f75038"></a>
### Get job card items by material request item

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_job_card_items_by_material_request_item`

**Inputs** pick\_list.

**Record and data access** read “Material Request Item” via get\_all.

**Explicit results** mapping() · dict(Platform.get\_all(“Material Request Item”, filters = mapping(“name” → list(“in”, material\_request\_items)), fields = list(“name”, “job\_card\_item”), as\_list = true)).

**Local steps**

- Set material\_request\_items from list of location.material\_request\_item for location drawn from pick\_list.locations where location.material\_request\_item.
  - Draw location from pick\_list.locations, keep a combination only if (location.material\_request\_item).
- If not material\_request\_items.
  - Return mapping().
- Return dict(Platform.get\_all(“Material Request Item”, filters = mapping(“name” → list(“in”, material\_request\_items)), fields = list(“name”, “job\_card\_item”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L932) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L429)

<a id="op-2566100777c939"></a>
### Update stock entry based on work order

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_update_stock_entry_based_on_work_order`

**Inputs** pick\_list, stock\_entry.

**Record and data access** resolve a document from “Work Order” via get\_doc · read “BOM” via get\_value · read “Warehouse” via get\_value.

**Explicit results** stock\_entry.

**Local steps**

- Set work\_order from Platform.get\_doc(“Work Order”, pick\_list.get(“work\_order”)).
- Set stock\_entry.purpose from “Material Transfer for Manufacture”.
- Set stock\_entry.work\_order from work\_order.name.
- Set stock\_entry.company from work\_order.company.
- Set stock\_entry.from\_bom from 1.
- Set stock\_entry.bom\_no from work\_order.bom\_no.
- Set stock\_entry.use\_multi\_level\_bom from work\_order.use\_multi\_level\_bom.
- Set stock\_entry.fg\_completed\_qty from 0.
- If work\_order.bom\_no.
  - Set stock\_entry.inspection\_required from Platform.db.get\_value(“BOM”, work\_order.bom\_no, “inspection\_required”).
- Set is\_wip\_warehouse\_group from Platform.db.get\_value(“Warehouse”, work\_order.wip\_warehouse, “is\_group”).
- If not (is\_wip\_warehouse\_group and work\_order.skip\_transfer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_wip\_warehouse\_group → work\_order.skip\_transfer.
  - Set wip\_warehouse from work\_order.wip\_warehouse.
- Otherwise.
  - Set wip\_warehouse from no value.
- Set stock\_entry.to\_warehouse from wip\_warehouse.
- Set stock\_entry.project from work\_order.project.
- Set moved\_serial\_nos from get\_moved\_serial\_nos(pick\_list.locations, “transferred\_qty”).
- For each location in pick\_list.locations.
  - If get\_pending\_transfer\_stock\_qty(location) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set item from Platform.\_dict().
  - Evaluate update\_common\_item\_properties(item, location, moved\_serial\_nos).
  - Set item.t\_warehouse from wip\_warehouse.
  - Evaluate stock\_entry.append(“items”, item).
- Return stock\_entry.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L460)

<a id="op-b069fc8a6937f2"></a>
### Update stock entry based on material request

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_update_stock_entry_based_on_material_request`

**Inputs** pick\_list, stock\_entry.

**Record and data access** read “Material Request Item” via get\_value.

**Explicit results** stock\_entry.

**Local steps**

- Set moved\_serial\_nos from get\_moved\_serial\_nos(pick\_list.locations, “transferred\_qty”).
- For each location in pick\_list.locations.
  - If get\_pending\_transfer\_stock\_qty(location) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set target\_warehouse from no value.
  - If location.material\_request\_item.
    - Set target\_warehouse from Platform.get\_value(“Material Request Item”, location.material\_request\_item, “warehouse”).
  - Set item from Platform.\_dict().
  - Evaluate update\_common\_item\_properties(item, location, moved\_serial\_nos).
  - Set item.t\_warehouse from target\_warehouse.
  - Evaluate stock\_entry.append(“items”, item).
- Return stock\_entry.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L214) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L962) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L459)

<a id="op-48d9a511e92fd2"></a>
### Update stock entry items with no reference

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_update_stock_entry_items_with_no_reference`

**Inputs** pick\_list, stock\_entry.

**Explicit results** stock\_entry.

**Local steps**

- Set moved\_serial\_nos from get\_moved\_serial\_nos(pick\_list.locations, “transferred\_qty”).
- For each location in pick\_list.locations.
  - If get\_pending\_transfer\_stock\_qty(location) ≤ 0.
    - Continue with the next iteration or loop test.
  - Set item from Platform.\_dict().
  - Evaluate update\_common\_item\_properties(item, location, moved\_serial\_nos).
  - Evaluate stock\_entry.append(“items”, item).
- Return stock\_entry.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L216) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L964) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L461)

<a id="op-3fd72159551cef"></a>
### Get pending transfer stock qty

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_pending_transfer_stock_qty`

**Inputs** location.

**Explicit results** (flt(location.picked\_qty) − flt(location.transferred\_qty)).

**Local steps**

- Return (flt(location.picked\_qty) − flt(location.transferred\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L937) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L434)

<a id="op-a1fa99d619c0e5"></a>
### Update common item properties

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_update_common_item_properties`

**Inputs** item, location, moved\_serial\_nos.

**Local steps**

- Set pending\_stock\_qty from get\_pending\_transfer\_stock\_qty(location).
- Set item.item\_code from location.item\_code.
- Set item.item\_name from location.item\_name.
- Set item.s\_warehouse from location.warehouse.
- Set item.transfer\_qty from pending\_stock\_qty.
- Set item.qty from flt((pending\_stock\_qty ÷ (location.conversion\_factor or 1)), location.precision(“qty”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in location.conversion\_factor → 1.
- Set item.uom from location.uom.
- Set item.conversion\_factor from location.conversion\_factor.
- Set item.stock\_uom from location.stock\_uom.
- Set item.material\_request from location.material\_request.
- Set item.serial\_no from get\_pending\_serial\_nos(location, moved\_serial\_nos, “transferred\_qty”).
- Set item.batch\_no from location.batch\_no.
- Set item.use\_serial\_batch\_fields from location.use\_serial\_batch\_fields.
- Set item.material\_request\_item from location.material\_request\_item.
- Set item.pick\_list\_item from location.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L211) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L959) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L456)

<a id="op-df3f2e0e213151"></a>
### Get rejected warehouses

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_rejected_warehouses`

**Inputs** no declared parameters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** Platform.local.rejected\_warehouses.

**Local steps**

- If not hasattr(Platform.local, “rejected\_warehouses”).
  - Set Platform.local.rejected\_warehouses from list().
- If not Platform.local.rejected\_warehouses.
  - Set Platform.local.rejected\_warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“is\_rejected\_warehouse” → 1), pluck = “name”).
- Return Platform.local.rejected\_warehouses.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0766.json#L1177) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L69)

<a id="op-9c15354d944bea"></a>
### Check pick list company

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_check_pick_list_company`

**Inputs** company.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Company must be text” · validation helper with Platform.PermissionError — translated “Not permitted for {0}”.format(company).

**Local steps**

- If (company is distinct from no value and not isinstance(company, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company is distinct from no value → not isinstance(company, str).
  - Call the validation error handler Platform.throw(translated “Company must be text”, Platform.ValidationError).
- If not company.
  - Return no value.
- Bind dependencies get\_allowed\_companies.
- Set allowed\_companies from get\_allowed\_companies(Platform.session.user, “Pick List”).
- If (allowed\_companies and company does not belong to allowed\_companies).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_companies → company does not belong to allowed\_companies.
  - Call the validation error handler Platform.throw(translated “Not permitted for {0}”.format(company), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L412)

<a id="op-76d333d60800f5"></a>
### Get pick list query

`operation_enterprise_stock_record_definitions_pick_list_business_behavior_get_pick_list_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** query.run(as\_dict = true).

**Explicit failure paths** validation helper — translated “Please select a Company”.

**Local steps**

- Evaluate Platform.has\_permission(“Pick List”, throw = true).
- If not filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “Please select a Company”).
- Evaluate check\_pick\_list\_company(filters.get(“company”)).
- Set PICK\_LIST from Platform.qb.DocType(“Pick List”).
- Set PICK\_LIST\_ITEM from Platform.qb.DocType(“Pick List Item”).
- Set SALES\_ORDER from Platform.qb.DocType(“Sales Order”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.company equals nested operand in the contract(nested operand in the contract)).where(SALES\_ORDER.customer ….
- If filters.get(“sales\_order”).
  - Set query from query.where(PICK\_LIST\_ITEM.sales\_order equals filters.get(“sales\_order”)).
- If txt.
  - Set meta from Platform.get\_meta(“Pick List”).
  - Set search\_fields from meta.get\_search\_fields().
  - Set txt from formatted text %{txt}%.
  - Set txt\_condition from PICK\_LIST at search\_fields at negative 1.like(txt).
  - For each field in search\_fields at slice no value to negative 1.
    - Update txt\_condition using bitwise or PICK\_LIST at field.like(txt).
  - Set query from query.where(txt\_condition).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Pick List”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L67)

<a id="op-77533b3b4bdc23"></a>
### Get delivered bundle component qty

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_delivered_bundle_component_qty`

**Inputs** pick\_list, sales\_order\_items.

**Explicit results** tuple(delivered\_qty, delivered\_serial\_nos).

**Local steps**

- Set tuple(delivered\_qty, delivered\_serial\_nos) from tuple(defaultdict(float), defaultdict(set)).
- For each parenttype in tuple(“Delivery Note”, “Sales Invoice”).
  - For each row in get\_delivered\_packed\_items(pick\_list, parenttype, sales\_order\_items).
    - Set key from tuple(row.so\_detail, row.item\_code, row.warehouse, (row.batch\_no or empty text)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.batch\_no → empty text.
    - Update delivered\_qty at key using + flt(row.delivered\_qty).
    - Evaluate delivered\_serial\_nos at key.update(generator of number.lower() for number drawn from get\_serial\_nos(row.serial\_no)).
      - Draw number from get\_serial\_nos(row.serial\_no).
- Return tuple(delivered\_qty, delivered\_serial\_nos).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L424)

<a id="op-202e0ea72d2640"></a>
### Get delivered packed items

`operation_enterprise_binding_enterprise_stock_doctype_pick_list_pick_list_get_delivered_packed_items`

**Inputs** pick\_list, parenttype, sales\_order\_items.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(conditions).groupby(transaction\_item. ….

**Local steps**

- Set packed\_item from Platform.qb.DocType(“Packed Item”).
- Set transaction\_item from Platform.qb.DocType(formatted text {parenttype} Item).
- Set query from nested operand in the contract.qb.from\_(transaction\_item).inner\_join(packed\_item).on(((packed\_item.parent equals transaction\_item.parent bitwise and packed\_item.parent\_detail\_docname equals transaction\_ite ….
- Set conditions from ((transaction\_item.docstatus equals 1 bitwise and transaction\_item.against\_pick\_list equals pick\_list) bitwise and transaction\_item.so\_detail.isin(sales\_order\_items)).
- If parenttype equals “Sales Invoice”.
  - Set transaction from Platform.qb.DocType(parenttype).
  - Set query from query.inner\_join(transaction).on(transaction.name equals transaction\_item.parent).
  - Update conditions using bitwise and transaction.update\_stock equals 1.
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(conditions).groupby(transaction\_item. ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L425)

<a id="op-cd709a7aca9590"></a>
### Get data

`operation_enterprise_stock_record_definitions_pick_list_pick_list_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “pick\_list”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “from\_voucher\_no”, “Delivery Note” → “against\_pick\_list”, “Sales Invoice” → “against\_pick\_list”), “interna ….

**Local steps**

- Return mapping(“fieldname” → “pick\_list”, “non\_standard\_fieldnames” → mapping(“Stock Reservation Entry” → “from\_voucher\_no”, “Delivery Note” → “against\_pick\_list”, “Sales Invoice” → “against\_pick\_list”), “interna ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0766.json#L2539) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L126)

## Record · Price list

[Record definition](../../../../data/record-types/price_list.json)

<a id="op-7915e0477fe35a"></a>
### Price List.validate

`operation_enterprise_stock_record_definitions_price_list_business_behavior_price_list_validate`

**Inputs** self.

**Local steps**

- If (not cint(self.buying) and not cint(self.selling)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.buying) → not cint(self.selling).
  - Evaluate throw(translated “Price List must be applicable for Buying or Selling”).
- Evaluate self.validate\_currency\_change().
- Evaluate self.validate\_side\_not\_used\_as\_default(“selling”).
- Evaluate self.validate\_side\_not\_used\_as\_default(“buying”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate currency change](operations-042.md#op-f0df6919921779), [validate side not used as default](operations-042.md#op-7f7eca37a87321).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L185)

<a id="op-7f7eca37a87321"></a>
### Price List.validate side not used as default

`operation_enterprise_binding_enterprise_stock_doctype_price_list_price_list_pricelist_validate_side_not_used_as_default`

**Inputs** self, side.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or cint(self.get(side)) or not cint(nested operand in the contract.get\_doc\_before\_save().get(side))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → cint(self.get(side)) → not cint(self.get\_doc\_before\_save().get(side)).
  - Return no value.
- If used\_in bound to self.get\_doctype\_using\_as\_default(side).
  - Evaluate throw(translated “Price List {0} is the default in {1}, so it must stay applicable for {2}”.format(Platform.bold(self.name), translated used\_in, get\_price\_list\_side\_label(side))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get doctype using as default](operations-042.md#op-c58e852fc042a7).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L970) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L467)

<a id="op-c58e852fc042a7"></a>
### Price List.get doctype using as default

`operation_enterprise_binding_enterprise_stock_doctype_price_list_price_list_pricelist_get_doctype_using_as_default`

**Inputs** self, side.

**Record and data access** read settings via get\_single\_value · read doctype via exists.

**Explicit results** settings · doctype.

**Local steps**

- Set tuple(settings, fieldname) from DEFAULT\_PRICE\_LIST\_SETTINGS at side.
- If Platform.db.get\_single\_value(settings, fieldname) equals self.name.
  - Return settings.
- For each tuple(doctype, holder\_field) in DEFAULT\_PRICE\_LIST\_HOLDERS at side.
  - If Platform.db.exists(doctype, mapping(holder\_field → self.name)).
    - Return doctype.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(settings, fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L968) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L465)

<a id="op-f0df6919921779"></a>
### Price List.validate currency change

`operation_enterprise_binding_enterprise_stock_doctype_price_list_price_list_pricelist_validate_currency_change`

**Inputs** self.

**Record and data access** read “Item Price” via count.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or not self.has\_value\_changed(“currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_value\_changed(“currency”).
  - Return no value.
- If item\_prices bound to Platform.db.count(“Item Price”, mapping(“price\_list” → self.name)).
  - Evaluate throw(translated “Currency of Price List {0} cannot be changed because it has {1} Item Prices in {2}. Create a new Price List  …”.format(Platform.bold(self.name), item\_prices, Platform.bold(self.get\_doc\_before\_s …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L969) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L466)

<a id="op-69d5360b92dc6a"></a>
### Price List.on update

`operation_enterprise_stock_record_definitions_price_list_business_behavior_price_list_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.set\_default\_if\_missing().
- Evaluate self.update\_item\_price().
- Evaluate self.delete\_price\_list\_details\_key().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default if missing](operations-042.md#op-47a04f3bd92a0e), [update item price](operations-042.md#op-44deb7d22df922), [delete price list details key](operations-043.md#op-a9c78b923b53f4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0773.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L182)

<a id="op-47a04f3bd92a0e"></a>
### Price List.set default if missing

`operation_enterprise_stock_record_definitions_price_list_business_behavior_price_list_set_default_if_missing`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Buying Settings” via get\_single\_value.

**Local steps**

- If cint(self.selling).
  - If not Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”).
    - Evaluate Platform.set\_value(“Selling Settings”, “Selling Settings”, “selling\_price\_list”, self.name).
- Otherwise.
  - If cint(self.buying).
    - If not Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”).
      - Evaluate Platform.set\_value(“Buying Settings”, “Buying Settings”, “buying\_price\_list”, self.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”), Platform.db.get\_single\_value(“Buying Settings”, “buying\_price\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0773.json#L226) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L183)

<a id="op-44deb7d22df922"></a>
### Price List.update item price

`operation_enterprise_stock_record_definitions_price_list_business_behavior_price_list_update_item_price`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Local steps**

- Evaluate Platform.db.sql(“update ′tabItem Price′ set currency=%s,\\n\\t\\t\\tbuying=%s, selling=%s, modified=NOW() where price\_list=%s”, tuple(self.currency, cint(self.buying), cint(self.selling), self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L184)

<a id="op-5e9fac8abc340b"></a>
### Price List.on trash

`operation_enterprise_stock_record_definitions_price_list_business_behavior_price_list_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.delete\_price\_list\_details\_key().
- Bind local operation \_update\_default\_price\_list for subsequent calls.
- For each module in list(“Selling”, “Buying”).
  - Evaluate \_update\_default\_price\_list(module).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete price list details key](operations-043.md#op-a9c78b923b53f4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0773.json#L810) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L180)

<a id="op-a8c2f122ff5c87"></a>
### Price List.on trash.update default price list

`operation_enterprise_stock_record_definitions_price_list_business_behavior_price_list_on_trash_update_default_price_list`

**Inputs** module.

**Record and data access** resolve a document from (module + “ Settings”) via get\_doc.

**State and service calls** call save on b.

**Local steps**

- Set b from Platform.get\_doc((module + “ Settings”)).
- Set price\_list\_fieldname from (module.lower() + “\_price\_list”).
- If self.name equals b.get(price\_list\_fieldname).
  - Evaluate b.set(price\_list\_fieldname, no value).
  - Set b.flags.ignore\_permissions from true.
  - Evaluate b.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0773.json#L1102) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L181)
