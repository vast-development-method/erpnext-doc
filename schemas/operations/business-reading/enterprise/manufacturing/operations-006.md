# Production · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom

<a id="op-5789b21fcae98f"></a>
### BOM.get tree representation

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_get_tree_representation`

**Inputs** self.

**Declared result** BOMTree.

**Explicit results** BOMTree(self.name).

**Local steps**

- Return BOMTree(self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0457.json#L2024) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L173)

<a id="op-84602c279c691c"></a>
### BOM.set process loss qty

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_set_process_loss_quantity`

**Inputs** self.

**Local steps**

- If self.process\_loss\_percentage.
  - Set self.process\_loss\_qty from ((flt(self.quantity) × flt(self.process\_loss\_percentage)) ÷ 100).
- For each item in self.secondary\_items.
  - Set item.process\_loss\_qty from flt((item.stock\_qty × (item.process\_loss\_per ÷ 100)), self.precision(“quantity”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0457.json#L2082) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L190)

<a id="op-3d35030e004353"></a>
### BOM.validate uoms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_units_of_measure`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_uom(self.item, self.uom, self.process\_loss\_percentage, self.process\_loss\_qty).
- For each item in self.secondary\_items.
  - Evaluate self.validate\_uom(item.item\_code, item.stock\_uom, item.process\_loss\_per, item.process\_loss\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate uom](operations-006.md#op-e9e793272669eb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0457.json#L2287) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L220)

<a id="op-e9e793272669eb"></a>
### BOM.validate uom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_validate_unit_of_measure`

**Inputs** self, item\_code, uom, process\_loss\_per, process\_loss\_qty.

**Record and data access** read “UOM” via get\_value.

**Explicit failure paths** validation helper — translated “Process Loss Percentage cannot be greater than 100” · validation helper — msg.

**Local steps**

- Set must\_be\_whole\_number from Platform.get\_value(“UOM”, uom, “must\_be\_whole\_number”).
- If (process\_loss\_per and process\_loss\_per &gt; 100).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in process\_loss\_per → process\_loss\_per &gt; 100.
  - Call the validation error handler Platform.throw(translated “Process Loss Percentage cannot be greater than 100”).
- If (process\_loss\_qty and must\_be\_whole\_number and (process\_loss\_qty modulo or format 1) differs from 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in process\_loss\_qty → must\_be\_whole\_number → (process\_loss\_qty modulo or format 1) differs from 0.
  - Set msg from formatted text Item: {Platform.bold(item\_code)} with Stock UOM: {Platform.bold(uom)} can't have fractional process loss qty as UOM {Platform.bold(uom)} is a whole Nu.
  - Call the validation error handler Platform.throw(msg, title = translated “Invalid Process Loss Configuration”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L218)

<a id="op-0b08127d4d04dc"></a>
### BOM.has scrap items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_bill_of_materials_has_scrap_items`

**Inputs** self.

**Explicit results** any(generator of (d.get(“secondary\_item\_type”) equals “Scrap” or d.get(“valuation\_type”) equals “Valuation Rate”) for d drawn from self.get(“secondary\_items”)).

**Local steps**

- Return any(generator of (d.get(“secondary\_item\_type”) equals “Scrap” or d.get(“valuation\_type”) equals “Valuation Rate”) for d drawn from self.get(“secondary\_items”)).
  - Draw d from self.get(“secondary\_items”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“secondary\_item\_type”) equals “Scrap” → d.get(“valuation\_type”) equals “Valuation Rate”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0457.json#L2816) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L174)

<a id="op-b9bb8d5887b880"></a>
### Get bom item rate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_get_bill_of_materials_item_rate`

**Inputs** args, bom\_doc.

**Record and data access** read “Item” via get\_value · resolve a document from “Item” via get\_cached\_doc.

**Explicit results** flt(rate).

**Explicit failure paths** validation helper — translated “Please select Price List”.

**Local steps**

- If bom\_doc.rm\_cost\_as\_per equals “Valuation Rate”.
  - Set rate from (get\_valuation\_rate(args) × (args.get(“conversion\_factor”) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“conversion\_factor”) → 1.
- Otherwise.
  - If bom\_doc.rm\_cost\_as\_per equals “Last Purchase Rate”.
    - Set rate from ((flt(args.get(“last\_purchase\_rate”)) or flt(Platform.db.get\_value(“Item”, args at “item\_code”, “last\_purchase\_rate”))) × (args.get(“conversion\_factor”) or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(args.get(“last\_purchase\_rate”)) → flt(Platform.db.get\_value(“Item”, args at “item\_code”, “last\_purchase\_rate”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“conversion\_factor”) → 1.
  - Otherwise.
    - If bom\_doc.rm\_cost\_as\_per equals “Price List”.
      - If not bom\_doc.buying\_price\_list.
        - Call the validation error handler Platform.throw(translated “Please select Price List”).
      - Set ctx from ItemDetailsCtx(mapping(“doctype” → “BOM”, “price\_list” → bom\_doc.buying\_price\_list, “qty” → (args.get(“qty”) or 1), “uom” → (args.get(“uom”) or args.get(“stock\_uom”)), …)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“qty”) → 1.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“uom”) → args.get(“stock\_uom”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“conversion\_factor”) → 1.
      - Set item\_doc from Platform.get\_cached\_doc(“Item”, args.get(“item\_code”)).
      - Set price\_list\_data from get\_price\_list\_rate(ctx, item\_doc).
      - Set rate from price\_list\_data.price\_list\_rate.
- Return flt(rate).

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_doc(“Item”, args.get(“item\_code”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L222)

<a id="op-56b760fd621eba"></a>
### Get valuation rate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_get_valuation_rate`

**Inputs** data.

**Record and data access** read “Item” via get\_value.

**Explicit results** flt(valuation\_rate).

**Local steps**

- Bind dependencies Case.
- Set tuple(item\_code, company) from tuple(data.get(“item\_code”), data.get(“company”)).
- Set valuation\_rate from 0.0.
- Set bin\_table from Platform.qb.DocType(“Bin”).
- Set wh\_table from Platform.qb.DocType(“Warehouse”).
- Set item\_valuation from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.warehouse equals nested operand in the contract.name).select(nested operand in the contract.else\_(no value). ….
- Set warehouse from data.get(“source\_warehouse”).
- If (data.get(“set\_rate\_based\_on\_warehouse”) and data.get(“warehouse”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.get(“set\_rate\_based\_on\_warehouse”) → data.get(“warehouse”).
  - Set warehouse from data.get(“warehouse”).
- If warehouse.
  - Set item\_valuation from item\_valuation.where(bin\_table.warehouse equals warehouse).
- Set item\_valuation from item\_valuation.run(as\_dict = true) at 0.
- Set valuation\_rate from item\_valuation.get(“valuation\_rate”).
- If flt(valuation\_rate) ≤ 0.
  - Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
  - Set last\_val\_rate from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(sle.creation, order = nested operand in the contract.qb.desc).limit(1).run(as\_dict = true).
  - Set valuation\_rate from flt(last\_val\_rate at 0.get(“valuation\_rate”)) when last\_val\_rate, otherwise 0.
    - Value choice on last\_val\_rate — true gives flt(last\_val\_rate at 0.get(“valuation\_rate”)), false gives 0.
- If not valuation\_rate.
  - Set valuation\_rate from Platform.db.get\_value(“Item”, item\_code, “valuation\_rate”).
- Return flt(valuation\_rate).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L226)

<a id="op-2fe5dd551ab332"></a>
### Get list context

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_get_list_context`

**Inputs** context.

**Local steps**

- Set context.title from translated “Bill of Materials”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0458.json#L380) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L225)

<a id="op-c06e5ce77469b2"></a>
### Get step material names

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_step_material_names`

**Inputs** bom, operation\_row\_id.

**Explicit results** set of row.name for row drawn from bom.items where cint(row.operation\_row\_id) equals cint(operation\_row\_id).

**Local steps**

- Return set of row.name for row drawn from bom.items where cint(row.operation\_row\_id) equals cint(operation\_row\_id).
  - Draw row from bom.items, keep a combination only if (cint(row.operation\_row\_id) equals cint(operation\_row\_id)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L654)

<a id="op-32c2d07fd68063"></a>
### Get bom items as dict

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_get_bill_of_materials_items_as_mapping`

**Inputs** bom, company, qty = 1, fetch\_exploded = 1, fetch\_secondary\_items = 0, include\_non\_stock\_items = false, fetch\_qty\_in\_stock\_uom = true, ignore\_permissions = true.

**Record and data access** read “BOM” via get\_cached\_value · read d at 0 via get\_all · read “Company” via get\_cached\_value.

**State and service calls** execute a supplied database query.

**Explicit results** item\_dict.

**Local steps**

- If not ignore\_permissions.
  - Evaluate Platform.has\_permission(“BOM”, “read”, doc = bom, throw = true).
- Set item\_dict from mapping().
- Set group\_by\_cond from “group by item\_code, stock\_uom, operation”.
- If Platform.get\_cached\_value(“BOM”, bom, “track\_semi\_finished\_goods”).
  - Set fetch\_exploded from 0.
  - Set group\_by\_cond from “group by item\_code, operation\_row\_id, stock\_uom”.
- If fetch\_secondary\_items.
  - Set fetch\_exploded from 0.
  - Set group\_by\_cond from “group by item\_code, secondary\_item\_type”.
- Set query from query text (SELECT, BOM, Item, Item Default).
- Set is\_stock\_item from cint(not include\_non\_stock\_items).
- If cint(fetch\_exploded).
  - Set query from query.format(table = “BOM Explosion Item”, where\_conditions = “)”, is\_stock\_item = is\_stock\_item, qty\_field = “stock\_qty”, …).
  - Set items from Platform.db.sql(query, mapping(“parent” → bom, “qty” → qty, “bom” → bom, “company” → company), as\_dict = true).
- Otherwise.
  - If fetch\_secondary\_items.
    - Set query from query.format(table = “BOM Secondary Item”, where\_conditions = “)”, select\_columns = “, item.description, bom\_item.cost\_allocation\_per, bom\_item.process\_loss\_per, bom\_item.secondary\_item\_type, b …”, is\_stoc ….
    - Set items from Platform.db.sql(query, mapping(“qty” → qty, “bom” → bom, “company” → company), as\_dict = true).
  - Otherwise.
    - Set rate\_col from “bom\_item.base\_rate”.
    - If fetch\_qty\_in\_stock\_uom.
      - Update rate\_col using + “ / ifnull(nullif(bom\_item.conversion\_factor, 0), 1)”.
    - Set query from query.format(table = “BOM Item”, where\_conditions = “or bom\_item.is\_phantom\_item)”, is\_stock\_item = is\_stock\_item, qty\_field = “stock\_qty” when fetch\_qty\_in\_stock\_uom, otherwise “qty”, …).
      - Value choice on fetch\_qty\_in\_stock\_uom — true gives “stock\_qty”, false gives “qty”.
    - Set items from Platform.db.sql(query, mapping(“qty” → qty, “bom” → bom, “company” → company), as\_dict = true).
- For each item in items.
  - Set key from item.item\_code.
  - If fetch\_secondary\_items.
    - Set key from tuple(item.item\_code, (item.secondary\_item\_type or empty text)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.secondary\_item\_type → empty text.
  - If item.operation\_row\_id.
    - Set key from tuple(item.item\_code, item.operation\_row\_id).
  - If item.operation.
    - Set key from tuple(item.item\_code, item.operation).
  - Set stock\_qty from item.pop(“stock\_qty”).
  - If item.get(“is\_phantom\_item”).
    - Set data from get\_bom\_items\_as\_dict(item.get(“bom\_no”), company, qty = stock\_qty, fetch\_exploded = fetch\_exploded, fetch\_secondary\_items = fetch\_secondary\_items, include\_non\_stock\_items = include\_non\_stock\_items, …).
    - For each tuple(k, v) in data.items().
      - If item\_dict.get(k).
        - Update item\_dict at k at “qty” using + flt(v.qty).
      - Otherwise.
        - Set item\_dict at k from v.
  - Otherwise.
    - If key belongs to item\_dict.
      - Update item\_dict at key at “qty” using + flt(item.qty).
    - Otherwise.
      - Set item\_dict at key from item.
- Set fields from list(list(“Account”, “expense\_account”, “stock\_adjustment\_account”), list(“Cost Center”, “cost\_center”, “cost\_center”), list(“Warehouse”, “default\_warehouse”, empty text)).
- Set company\_of from mapping().
- For each d in fields.
  - Set names from set of item\_details.get(d at 1) for item\_details drawn from item\_dict.values() where item\_details.get(d at 1).
    - Draw item\_details from item\_dict.values(), keep a combination only if (item\_details.get(d at 1)).
  - Set company\_of at d at 0 from mapping of r.name → r.company for r drawn from Platform.get\_all(d at 0, filters = mapping(“name” → tuple(“in”, list(names))), fields = list(“name”, “company”)) when names, otherwise mapping().
    - Value choice on names — true gives mapping of r.name → r.company for r drawn from Platform.get\_all(d at 0, filters = mapping(“name” → tuple(“in”, list(names))), fields = list(“name”, “company”)), false gives mapping().
    - Draw r from Platform.get\_all(d at 0, filters = mapping(“name” → tuple(“in”, list(names))), fields = list(“name”, “company”)).
- For each tuple(item, item\_details) in item\_dict.items().
  - For each d in fields.
    - Set company\_in\_record from company\_of at d at 0.get(item\_details.get(d at 1)).
    - If (not item\_details.get(d at 1) or (company\_in\_record and company differs from company\_in\_record)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_details.get(d at 1) → (company\_in\_record and company differs from company\_in\_record).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_in\_record → company differs from company\_in\_record.
      - Set item\_dict at item at d at 1 from Platform.get\_cached\_value(“Company”, company, d at 2) when d at 2, otherwise no value.
        - Value choice on d at 2 — true gives Platform.get\_cached\_value(“Company”, company, d at 2), false gives no value.
- Return item\_dict.

**Values supplied outside this operation** effective access from Platform.has\_permission(“BOM”, “read”, doc = bom, throw = true) · configured or stored value from Platform.get\_cached\_value(“BOM”, bom, “track\_semi\_finished\_goods”), Platform.get\_cached\_value(“Company”, company, d at 2).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L224)

<a id="op-c5d47ce5f7cd0e"></a>
### Get bom items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_get_bill_of_materials_items`

**Inputs** bom, company, qty = 1, fetch\_exploded = 1.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** items.

**Local steps**

- Evaluate Platform.has\_permission(“BOM”, “read”, doc = bom, throw = true).
- Set items from get\_bom\_items\_as\_dict(bom, company, qty, fetch\_exploded, include\_non\_stock\_items = true, ignore\_permissions = false).values().
- Set items from list(items).
- Evaluate items.sort(key = functools.cmp\_to\_key(deferred anonymous expression)).
- Return items.

**Values supplied outside this operation** effective access from Platform.has\_permission(“BOM”, “read”, doc = bom, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L223)

<a id="op-f1b3b0d631fc55"></a>
### Validate bom no

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_business_behavior_validate_bill_of_materials_number`

**Inputs** item, bom\_no.

**Explicit failure paths** validation helper — translated “BOM {0} does not belong to Item {1}”.format(bom\_no, item).

**Local steps**

- Set bom from get\_usable\_bom(bom\_no).
- If item.
  - Set rm\_item\_exists from false.
  - For each d in bom.items.
    - If d.item\_code.lower() equals item.lower().
      - Set rm\_item\_exists from true.
  - For each d in bom.secondary\_items.
    - If d.item\_code.lower() equals item.lower().
      - Set rm\_item\_exists from true.
  - If \_bom\_produces\_item(bom, item).
    - Set rm\_item\_exists from true.
  - If not rm\_item\_exists.
    - Call the validation error handler Platform.throw(translated “BOM {0} does not belong to Item {1}”.format(bom\_no, item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L227)

<a id="op-a8a2184ac18ed1"></a>
### Validate production bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_validate_production_bom`

**Inputs** item, bom\_no.

**Explicit failure paths** validation helper — translated “BOM {0} does not belong to Item {1}”.format(bom\_no, item).

**Local steps**

- Set bom from get\_usable\_bom(bom\_no).
- If not \_bom\_produces\_item(bom, item).
  - Call the validation error handler Platform.throw(translated “BOM {0} does not belong to Item {1}”.format(bom\_no, item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L661)

<a id="op-77dbfb18a5e5f5"></a>
### Get usable bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_usable_bom`

**Inputs** bom\_no.

**Record and data access** resolve a document from “BOM” via get\_doc.

**Explicit results** bom.

**Explicit failure paths** validation helper — translated “BOM {0} must be active”.format(bom\_no) · validation helper — translated “BOM {0} must be submitted”.format(bom\_no).

**Local steps**

- Set bom from Platform.get\_doc(“BOM”, bom\_no).
- If not bom.is\_active.
  - Call the validation error handler Platform.throw(translated “BOM {0} must be active”.format(bom\_no)).
- If bom.docstatus differs from 1.
  - If not Platform.in\_test.
    - Call the validation error handler Platform.throw(translated “BOM {0} must be submitted”.format(bom\_no)).
- Return bom.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L656)

<a id="op-57c403984337f3"></a>
### Bom produces item

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_bom_produces_item`

**Inputs** bom, item.

**Record and data access** read “Item” via get\_value.

**Explicit results** (bom.item.lower() equals item.lower() or bom.item.lower() equals cstr(nested operand in the contract.get\_value(“Item”, item, “variant\_of”)).lower()).

**Local steps**

- Return (bom.item.lower() equals item.lower() or bom.item.lower() equals cstr(nested operand in the contract.get\_value(“Item”, item, “variant\_of”)).lower()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bom.item.lower() equals item.lower() → bom.item.lower() equals cstr(nested operand in the contract.db.get\_value(“Item”, item, “variant\_of”)).lower().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L633)

<a id="op-7e51b37c2207ef"></a>
### Get children

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_children`

**Inputs** doctype = no value, parent = no value, is\_root = false, remaining named values filters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “BOM” via get\_cached\_doc · read “BOM Item” via get\_all · read “Item” via get\_list.

**State and service calls** msgprint with translated “Please select a BOM”.

**Explicit results** no value · bom\_items.

**Local steps**

- If (not parent or parent equals “BOM”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → parent equals “BOM”.
  - Evaluate Platform.msgprint(translated “Please select a BOM”).
  - Return no value.
- If parent.
  - Set Platform.form\_dict.parent from parent.
- If Platform.form\_dict.parent.
  - Set bom\_doc from Platform.get\_cached\_doc(“BOM”, Platform.form\_dict.parent).
  - Evaluate Platform.has\_permission(“BOM”, doc = bom\_doc, throw = true).
  - Set bom\_items from Platform.get\_all(“BOM Item”, fields = list(“item\_code”, “bom\_no as value”, “stock\_qty”, “qty”, …), filters = list(list(“parent”, “=”, Platform.form\_dict.parent)), order\_by = “idx”).
  - Set item\_names from tuple(generator of d.get(“item\_code”) for d drawn from bom\_items).
    - Draw d from bom\_items.
  - Set items from Platform.get\_list(“Item”, fields = list(“image”, “description”, “name”, “stock\_uom”, …), filters = list(list(“name”, “in”, item\_names))).
  - For each bom\_item in bom\_items.
    - Evaluate bom\_item.update(next(generator of item for item drawn from items where item.get(“name”) equals bom\_item.get(“item\_code”))).
      - Draw item from items, keep a combination only if (item.get(“name”) equals bom\_item.get(“item\_code”)).
    - Set bom\_item.parent\_bom\_qty from bom\_doc.quantity.
    - Set bom\_item.expandable from 0 when bom\_item.value belongs to tuple(empty text, no value), otherwise 1.
      - Value choice on bom\_item.value belongs to tuple(empty text, no value) — true gives 0, false gives 1.
  - Return bom\_items.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“BOM”, Platform.form\_dict.parent) · effective access from Platform.has\_permission(“BOM”, doc = bom\_doc, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L647)

<a id="op-aa76902b905646"></a>
### Add additional cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_additional_cost`

**Inputs** stock\_entry, work\_order, job\_card = no value.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set stock\_entry.additional\_costs from list().
- Set expense\_account from Platform.get\_value(“Company”, work\_order.company, “default\_operating\_cost\_account”).
- Evaluate add\_non\_stock\_items\_cost(stock\_entry, work\_order, expense\_account, job\_card = job\_card).
- Evaluate add\_operations\_cost(stock\_entry, work\_order, expense\_account, job\_card = job\_card).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L617)

<a id="op-b193a415f4bb89"></a>
### Add non stock items cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_non_stock_items_cost`

**Inputs** stock\_entry, work\_order, expense\_account, job\_card = no value.

**Record and data access** resolve a document from “BOM” via get\_doc · read “Item” via get\_all.

**Local steps**

- Set bom from Platform.get\_doc(“BOM”, work\_order.bom\_no).
- Set table from “items”.
- If (work\_order and not job\_card).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in work\_order → not job\_card.
  - Set table from “exploded\_items” when work\_order.get(“use\_multi\_level\_bom”), otherwise “items”.
    - Value choice on work\_order.get(“use\_multi\_level\_bom”) — true gives “exploded\_items”, false gives “items”.
- Set items from Platform.\_dict().
- For each d in bom.get(table).
  - If d.get(“is\_phantom\_item”).
    - Continue with the next iteration or loop test.
  - Evaluate items.setdefault(d.item\_code, 0).
  - Update items at d.item\_code using + flt(d.base\_amount when table equals “items”, otherwise d.amount).
    - Value choice on table equals “items” — true gives d.base\_amount, false gives d.amount.
- Set non\_stock\_items from Platform.get\_all(“Item”, fields = “name”, filters = list(list(“name”, “in”, list(items.keys())), list(IfNull(Field(“is\_stock\_item”), 0), “=”, 0)), as\_list = 1).
- Set non\_stock\_items\_cost from 0.0.
- For each name in non\_stock\_items.
  - Update non\_stock\_items\_cost using + ((flt(items.get(name at 0)) × flt(stock\_entry.fg\_completed\_qty)) ÷ flt(bom.quantity)).
- If non\_stock\_items\_cost.
  - Evaluate stock\_entry.append(“additional\_costs”, mapping(“expense\_account” → expense\_account, “description” → translated “Non stock items”, “amount” → non\_stock\_items\_cost)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L620)

<a id="op-8ced01ccbf1fcd"></a>
### Get component operating cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_component_operating_cost`

**Inputs** wc, row, consumed\_op\_cost, total\_component\_rate.

**Explicit results** flt((cost − flt(consumed\_op\_cost.get(“consumed\_cost”))), row.precision(“actual\_operating\_cost”)).

**Local steps**

- If (flt(row.actual\_operating\_cost) and total\_component\_rate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(row.actual\_operating\_cost) → total\_component\_rate.
  - Set cost from ((flt(row.actual\_operating\_cost) × flt(wc.operating\_cost)) ÷ total\_component\_rate).
- Otherwise.
  - Set cost from (flt(wc.operating\_cost) × flt((flt(row.actual\_operation\_time) ÷ 60.0))).
- Return flt((cost − flt(consumed\_op\_cost.get(“consumed\_cost”))), row.precision(“actual\_operating\_cost”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L649)

<a id="op-5ec238c33e9c19"></a>
### Add operating cost component wise

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_operating_cost_component_wise`

**Inputs** stock\_entry, work\_order = no value, op\_expense\_account = no value, job\_card = no value.

**Record and data access** read “Workstation Cost” via get\_all.

**Explicit results** false · cost\_added.

**Local steps**

- If not work\_order.
  - Return false.
- Bind dependencies get\_consumed\_operating\_cost.
- Set cost\_added from false.
- For each row in work\_order.operations.
  - If (job\_card and job\_card.operation\_id differs from row.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in job\_card → job\_card.operation\_id differs from row.name.
    - Continue with the next iteration or loop test.
  - If not row.actual\_operation\_time.
    - Continue with the next iteration or loop test.
  - Set workstation\_cost from Platform.get\_all(“Workstation Cost”, fields = list(“operating\_component”, “operating\_cost”), filters = mapping(“parent” → row.workstation, “parenttype” → “Workstation”)).
  - Set consumed\_operating\_cost from (get\_consumed\_operating\_cost(work\_order.name, stock\_entry.bom\_no, row.name) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_consumed\_operating\_cost(work\_order.name, stock\_entry.bom\_no, row.name) → list().
  - Set total\_component\_rate from sum(generator of flt(wc.operating\_cost) for wc drawn from workstation\_cost).
    - Draw wc from workstation\_cost.
  - For each wc in workstation\_cost.
    - Set expense\_account from (get\_component\_account(wc.operating\_component, stock\_entry.company) or op\_expense\_account).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_component\_account(wc.operating\_component, stock\_entry.company) → op\_expense\_account.
    - Set consumed\_op\_cost from next(generator of cost for cost drawn from consumed\_operating\_cost where cost.get(“operating\_component”) equals wc.operating\_component, mapping()).
      - Draw cost from consumed\_operating\_cost, keep a combination only if (cost.get(“operating\_component”) equals wc.operating\_component).
    - Set actual\_cp\_operating\_cost from get\_component\_operating\_cost(wc, row, consumed\_op\_cost, total\_component\_rate).
    - Set remaining\_qty from (row.completed\_qty − consumed\_op\_cost.get(“consumed\_qty”, 0)).
    - Set per\_unit\_cost from (actual\_cp\_operating\_cost ÷ (remaining\_qty or 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in remaining\_qty → 1.
    - Set operating\_cost from (per\_unit\_cost × stock\_entry.fg\_completed\_qty).
    - If actual\_cp\_operating\_cost.
      - Evaluate stock\_entry.append(“additional\_costs”, mapping(“expense\_account” → expense\_account, “description” → translated “{0} Operating Cost for operation {1}”.format(wc.operating\_component, row.operation), “amount” ….
      - Set cost\_added from true.
- Return cost\_added.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L621)

<a id="op-b41da08ebf49ee"></a>
### Add operation cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_operation_cost`

**Inputs** stock\_entry, work\_order, operation, expense\_account.

**Local steps**

- Set tuple(amount, qty) from \_get\_operation\_cost\_and\_qty(stock\_entry, work\_order, operation).
- If amount &gt; 0.
  - Evaluate \_append\_operating\_cost(stock\_entry, expense\_account, amount, operation\_id = operation.name, qty = qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L622)

<a id="op-0e20c51393178f"></a>
### Get operation cost and qty

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_get_operation_cost_and_qty`

**Inputs** stock\_entry, work\_order, operation.

**Explicit results** tuple((cost\_per\_unit × qty), qty) · tuple(0, 0) · tuple(((remaining\_cost ÷ remaining\_qty) × qty), qty).

**Local steps**

- Bind dependencies get\_consumed\_operating\_cost.
- Set qty from flt(stock\_entry.fg\_completed\_qty).
- If not flt(operation.completed\_qty).
  - Set cost\_per\_unit from (flt(operation.planned\_operating\_cost) ÷ flt(work\_order.qty)) when work\_order.qty, otherwise 0.
    - Value choice on work\_order.qty — true gives (flt(operation.planned\_operating\_cost) ÷ flt(work\_order.qty)), false gives 0.
  - Return tuple((cost\_per\_unit × qty), qty).
- Set consumed from get\_consumed\_operating\_cost(work\_order.name, stock\_entry.bom\_no, operation.name).
- Set remaining\_cost from (flt(operation.actual\_operating\_cost) − sum(generator of flt(row.consumed\_cost) for row drawn from consumed)).
  - Draw row from consumed.
- Set remaining\_qty from (flt(operation.completed\_qty) − max(generator of flt(row.consumed\_qty) for row drawn from consumed, default = 0)).
  - Draw row from consumed.
- <a id="op-0e20c51393178f-guard-12"></a>If remaining\_qty ≤ 0.
  - Return tuple(0, 0).
- Set qty from min(remaining\_qty, qty).
- Return tuple(((remaining\_cost ÷ remaining\_qty) × qty), qty).

**Derived branch illustrations**

- At the comparison remaining\_qty ≤ 0, remaining\_qty = 0 selects the branch that returns tuple(0, 0). With remaining\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0e20c51393178f-guard-12)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L652)

<a id="op-992bbe9390befb"></a>
### Append operating cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_append_operating_cost`

**Inputs** stock\_entry, expense\_account, amount, remaining named values operation\_fields.

**Local steps**

- Evaluate stock\_entry.append(“additional\_costs”, mapping(“expense\_account” → expense\_account, “description” → translated “Operating Cost as per Work Order / BOM”, “amount” → flt(amount, Platform.get\_precision(“Lande ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L626)

<a id="op-f749c7cc69b7c2"></a>
### Add fg based operating cost

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_bom_add_fg_based_operating_cost`

**Inputs** stock\_entry, work\_order, expense\_account, job\_card = no value.

**Explicit results** no value.

**Local steps**

- If (job\_card or not work\_order.use\_multi\_level\_bom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in job\_card → not work\_order.use\_multi\_level\_bom.
  - Return no value.
- Set unit\_cost from get\_op\_cost\_from\_sub\_assemblies(work\_order.bom\_no, skip\_boms\_with\_operations = true).
- If unit\_cost.
  - Evaluate \_append\_operating\_cost(stock\_entry, expense\_account, (unit\_cost × flt(stock\_entry.fg\_completed\_qty))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L619)
