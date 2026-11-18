# Purchasing · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Procurement tracker

<a id="op-2acbda05d19456"></a>
### Get mapped pr records

`operation_enterprise_buying_report_procurement_tracker_business_behavior_get_mapped_purchase_receipt_records`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(pr\_records).

**Local steps**

- Set pr from Platform.qb.DocType(“Purchase Receipt”).
- Set pr\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set pr\_records from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….run().
- Return Platform.\_dict(pr\_records).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L202)

<a id="op-df3c475d1829e9"></a>
### Get po entries

`operation_enterprise_buying_report_procurement_tracker_business_behavior_get_purchase_order_entries`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set parent from Platform.qb.DocType(“Purchase Order”).
- Set child from Platform.qb.DocType(“Purchase Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).from\_(child).select(child.name, child.parent, child.cost\_center, child.project, …).where(((parent.docstatus equals 1 bitwise and parent.name e ….
- Set query from apply\_filters\_on\_query(filters, parent, child, query).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L203)

## Report · Purchase analytics

<a id="op-4b80862c2b0019"></a>
### Execute

`operation_enterprise_buying_report_purchase_analytics_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** Analytics(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return Analytics(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L204)

## Record · Purchase order

[Record definition](../../../../data/record-types/purchase_order.json)

<a id="op-6785a29ac4cb84"></a>
### Purchase Order.initialize

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Purchase Order Item”, “target\_dt” → “Material Request Item”, “join\_field” → “material\_request\_item”, “target\_field” → “ordered\_qty”, …), mapping(“source\_dt” → “Purchase Order It ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1373)

<a id="op-0370a46349503f"></a>
### Purchase Order.onload

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_onload`

**Inputs** self.

**Local steps**

- Evaluate self.set\_onload(“can\_update\_items”, self.can\_update\_items()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can update items](operations-003.md#op-1c1dc92ffe9793).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1378)

<a id="op-f8f74f3e738480"></a>
### Purchase Order.before validate

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_has\_unit\_price\_items().
- Set self.flags.allow\_zero\_qty from self.has\_unit\_price\_items.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set has unit price items](operations-002.md#op-ed195d7480d7b2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1369)

<a id="op-3d281fd336a3f9"></a>
### Purchase Order.validate

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- Evaluate self.set\_status().
- Evaluate self.validate\_supplier().
- Evaluate self.validate\_schedule\_date().
- Evaluate validate\_for\_items(self).
- Evaluate self.set\_last\_purchase\_rate().
- Evaluate self.check\_for\_on\_hold\_or\_closed\_status(“Material Request”, “material\_request”).
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.validate\_for\_subcontracting().
- Evaluate self.validate\_minimum\_order\_qty().
- Evaluate validate\_against\_blanket\_order(self).
- If self.is\_old\_subcontracting\_flow.
  - Evaluate self.validate\_bom\_for\_subcontracting\_items().
  - Evaluate self.create\_raw\_materials\_supplied\_or\_received().
- Evaluate self.validate\_fg\_item\_for\_subcontracting().
- If not self.advance\_payment\_status.
  - Set self.advance\_payment\_status from “Not Initiated”.
- Evaluate validate\_inter\_company\_party(self.doctype, self.supplier, self.company, self.inter\_company\_order\_reference).
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).
- Evaluate self.set\_missing\_terms().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate supplier](operations-002.md#op-91d863affba748), [set last purchase rate](operations-002.md#op-40020cf2faed97), [validate with previous doc](operations-002.md#op-9bc18426627486), [validate minimum order qty](operations-002.md#op-e00637bd71d722), [validate bom for subcontracting items](operations-002.md#op-d54b8f0b9c4bd6), [validate fg item for subcontracting](operations-002.md#op-5db8312ff7c0f2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1389)

<a id="op-40020cf2faed97"></a>
### Purchase Order.set last purchase rate

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_set_last_purchase_rate`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”).
  - Return no value.
- For each d in self.get(“items”).
  - If d.item\_code.
    - Set d.last\_purchase\_rate from flt(item\_last\_purchase\_rate(self.name, self.conversion\_rate, d.item\_code, d.conversion\_factor), d.precision(“last\_purchase\_rate”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “disable\_last\_purchase\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L55)

<a id="op-ed195d7480d7b2"></a>
### Purchase Order.set has unit price items

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_set_has_unit_price_items`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_purchase\_order”).
  - Return no value.
- Set self.has\_unit\_price\_items from any(generator of not row.qty for row drawn from self.get(“items”) where (row.item\_code and not row.qty)).
  - Draw row from self.get(“items”), keep a combination only if ((row.item\_code and not row.qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → not row.qty.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_purchase\_order”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0337.json#L6824) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1379)

<a id="op-9bc18426627486"></a>
### Purchase Order.validate with previous doc

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_validate_with_previous_record`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- Set mri\_compare\_fields from list(list(“project”, “=”), list(“item\_code”, “=”)).
- If self.is\_subcontracted.
  - Set mri\_compare\_fields from list(list(“project”, “=”)).
- Evaluate super().validate\_with\_previous\_doc(mapping(“Supplier Quotation” → mapping(“ref\_dn\_field” → “supplier\_quotation”, “compare\_fields” → list(list(“supplier”, “=”), list(“company”, “=”), list(“currency”, “=”))) ….
- If cint(Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”)).
  - Evaluate self.validate\_rate\_with\_reference\_doc(list(list(“Supplier Quotation”, “supplier\_quotation”, “supplier\_quotation\_item”))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0338.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1392)

<a id="op-91d863affba748"></a>
### Purchase Order.validate supplier

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_validate_supplier`

**Inputs** self.

**Record and data access** read “Supplier” via get\_value · read “Supplier Scorecard” via get\_value.

**State and service calls** msgprint with translated “{0} currently has a {1} Supplier Scorecard standing, and Purchase Orders to this supplier should be issued w …”.format(self.supplier, standing).

**Explicit failure paths** validation helper — translated “Purchase Orders are not allowed for {0} due to a scorecard standing of {1}.”.format(self.supplier, standing).

**Local steps**

- Set prevent\_po from Platform.db.get\_value(“Supplier”, self.supplier, “prevent\_pos”).
- If prevent\_po.
  - Set standing from Platform.db.get\_value(“Supplier Scorecard”, mapping(“supplier” → self.supplier), “status”).
  - If standing.
    - Call the validation error handler Platform.throw(translated “Purchase Orders are not allowed for {0} due to a scorecard standing of {1}.”.format(self.supplier, standing)).
- Set warn\_po from Platform.db.get\_value(“Supplier”, self.supplier, “warn\_pos”).
- If warn\_po.
  - Set standing from Platform.db.get\_value(“Supplier Scorecard”, mapping(“supplier” → self.supplier), “status”).
  - Evaluate Platform.msgprint(translated “{0} currently has a {1} Supplier Scorecard standing, and Purchase Orders to this supplier should be issued w …”.format(self.supplier, standing), title = translated “Caution”,  ….
- Set self.party\_account\_currency from get\_party\_account\_currency(“Supplier”, self.supplier, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1391)

<a id="op-e00637bd71d722"></a>
### Purchase Order.validate minimum order qty

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_validate_minimum_order_quantity`

**Inputs** self.

**Record and data access** execute query text (SELECT, Item).format(“, ”.join((list(“%s”) × len(items)))).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item {0}: Ordered qty {1} cannot be less than minimum order qty {2} (defined in Item).”.format(item\_code, flt(qty, precision), itemwise\_min\_order\_qty.get(item\_code)).

**Local steps**

- If not self.get(“items”).
  - Return no value.
- Set items from list(set(generator of d.item\_code for d drawn from self.get(“items”))).
  - Draw d from self.get(“items”).
- Set itemwise\_min\_order\_qty from Platform.\_dict(Platform.db.sql(query text (SELECT, Item).format(“, ”.join((list(“%s”) × len(items)))), items)).
- Set itemwise\_qty from Platform.\_dict().
- For each d in self.get(“items”).
  - Evaluate itemwise\_qty.setdefault(d.item\_code, 0).
  - Update itemwise\_qty at d.item\_code using + flt(d.stock\_qty).
- Set precision from self.items at 0.precision(“stock\_qty”).
- For each tuple(item\_code, qty) in itemwise\_qty.items().
  - If flt(qty, precision) &lt; flt(itemwise\_min\_order\_qty.get(item\_code), precision).
    - Call the validation error handler Platform.throw(translated “Item {0}: Ordered qty {1} cannot be less than minimum order qty {2} (defined in Item).”.format(item\_code, flt(qty, precision), itemwise\_min\_order\_qty.get(item\_code))).
- Evaluate self.warn\_marginal\_min\_order\_qty(itemwise\_qty, itemwise\_min\_order\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [warn marginal min order qty](operations-002.md#op-c0244946f66f08).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1390)

<a id="op-c0244946f66f08"></a>
### Purchase Order.warn marginal min order qty

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_warn_marginal_minimum_order_quantity`

**Inputs** self, itemwise\_qty, itemwise\_min\_order\_qty.

**State and service calls** toast with translated “Item {0}: Ordered qty {1} {2} exceeds the minimum order qty {3} {2} by {4} {2} due to purchase UOM rounding.”.format(item\_code, flt(qty, precision), itemwise\_stock\_uom at item\_code, min\_order\_qty, …).

**Explicit results** no value.

**Local steps**

- If not self.is\_new().
  - Return no value.
- Set precision from self.items at 0.precision(“stock\_qty”).
- Set itemwise\_steps from mapping().
- Set itemwise\_stock\_uom from Platform.\_dict().
- For each d in self.get(“items”).
  - Set step from ((10 to the power negative d.precision(“qty”)) × flt(d.conversion\_factor)).
  - Evaluate itemwise\_steps.setdefault(d.item\_code, set()).add(step).
  - Set itemwise\_stock\_uom at d.item\_code from d.stock\_uom.
- For each tuple(item\_code, qty) in itemwise\_qty.items().
  - Set steps from itemwise\_steps at item\_code.
  - <a id="op-c0244946f66f08-guard-16"></a>If len(steps) differs from 1.
    - Continue with the next iteration or loop test.
  - Set step from next(iter(steps)).
  - Set min\_order\_qty from flt(itemwise\_min\_order\_qty.get(item\_code)).
  - Set overage from (flt(qty) − min\_order\_qty).
  - If (min\_order\_qty and flt(overage, precision) &gt; 0 and overage &lt; step).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in min\_order\_qty → flt(overage, precision) &gt; 0 → overage &lt; step.
    - Evaluate Platform.toast(translated “Item {0}: Ordered qty {1} {2} exceeds the minimum order qty {3} {2} by {4} {2} due to purchase UOM rounding.”.format(item\_code, flt(qty, precision), itemwise\_stock\_uom at item\_co ….

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(steps) differs from 1, length of steps = 2 selects the branch that continues with the next loop iteration. With length of steps = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c0244946f66f08-guard-16)

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1393)

<a id="op-d54b8f0b9c4bd6"></a>
### Purchase Order.validate bom for subcontracting items

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_validate_bom_for_subcontracting_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: BOM is not specified for subcontracting item {1}”.format(item.idx, item.item\_code).

**Local steps**

- For each item in self.items.
  - If not item.bom.
    - Call the validation error handler Platform.throw(translated “Row #{0}: BOM is not specified for subcontracting item {1}”.format(item.idx, item.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L820) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L60)

<a id="op-5db8312ff7c0f2"></a>
### Purchase Order.validate fg item for subcontracting

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_validate_fg_item_for_subcontracting`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Finished Good Item is not specified for service item {1}”.format(item.idx, item.item\_code) · validation helper — translated “Row #{0}: Finished Good Item {1} must be a sub-contracted item”.format(item.idx, item.fg\_item) · validation helper — translated “Row #{0}: Default BOM not found for FG Item {1}”.format(item.idx, item.fg\_item) · validation helper — translated “Row #{0}: Finished Good Item Qty can not be zero”.format(item.idx).

**Local steps**

- If self.is\_subcontracted.
  - If not self.is\_old\_subcontracting\_flow.
    - For each item in self.items.
      - If not item.fg\_item.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good Item is not specified for service item {1}”.format(item.idx, item.item\_code)).
      - Otherwise.
        - If not Platform.get\_value(“Item”, item.fg\_item, “is\_sub\_contracted\_item”).
          - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good Item {1} must be a sub-contracted item”.format(item.idx, item.fg\_item)).
        - Otherwise.
          - If (not item.bom and not get\_default\_bom(item.fg\_item)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.bom → not get\_default\_bom(item.fg\_item).
            - Call the validation error handler Platform.throw(translated “Row #{0}: Default BOM not found for FG Item {1}”.format(item.idx, item.fg\_item)).
      - If not item.fg\_item\_qty.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Finished Good Item Qty can not be zero”.format(item.idx)).
    - Evaluate self.validate\_finished\_good\_qty().
- Otherwise.
  - For each item in self.items.
    - Evaluate item.set(“fg\_item”, no value).
    - Evaluate item.set(“fg\_item\_qty”, 0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate finished good qty](operations-002.md#op-2206a5bdbed405).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L821) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L61)

<a id="op-2206a5bdbed405"></a>
### Purchase Order.validate finished good qty

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_validate_finished_good_qty`

**Inputs** self.

**Record and data access** read “Item” via get\_all.

**Local steps**

- Set finished\_good\_uoms from mapping of item.name → item.stock\_uom for item drawn from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, list(set of nested operand in the contract.fg\_item for item drawn from nested operan ….
  - Draw item from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, list(set of item.fg\_item for item drawn from self.items))), fields = list(“name”, “stock\_uom”)).
  - Draw item from self.items.
- Set integer\_uoms from get\_whole\_number\_uoms(finished\_good\_uoms.values()).
- For each item in self.items.
  - If stock\_uom bound to finished\_good\_uoms.get(item.fg\_item).
    - If stock\_uom belongs to integer\_uoms.
      - Evaluate validate\_qty\_is\_integer(item.fg\_item\_qty, stock\_uom, item.precision(“fg\_item\_qty”), item.idx).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L822) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L62)

<a id="op-ca4a5b1da2d553"></a>
### Purchase Order.get schedule dates

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_get_schedule_dates`

**Inputs** self.

**Record and data access** read “Material Request Item” via get\_value.

**Local steps**

- For each d in self.get(“items”).
  - If (d.material\_request\_item and not d.schedule\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.material\_request\_item → not d.schedule\_date.
    - Set d.schedule\_date from Platform.db.get\_value(“Material Request Item”, d.material\_request\_item, “schedule\_date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0338.json#L2483) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1372)

<a id="op-c2cbaa2b122613"></a>
### Purchase Order.get last purchase rate

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_get_last_purchase_rate`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set conversion\_rate from (flt(self.get(“conversion\_rate”)) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.get(“conversion\_rate”)) → 1.0.
- For each d in self.get(“items”).
  - If d.item\_code.
    - Set last\_purchase\_details from get\_last\_purchase\_details(d.item\_code, self.name).
    - If last\_purchase\_details.
      - Set d.base\_price\_list\_rate from (last\_purchase\_details at “base\_price\_list\_rate” × (flt(d.conversion\_factor) or 1.0)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.conversion\_factor) → 1.0.
      - Set d.discount\_percentage from last\_purchase\_details at “discount\_percentage”.
      - Set d.discount\_amount from ((last\_purchase\_details at “discount\_amount” × (flt(d.conversion\_factor) or 1.0)) ÷ conversion\_rate).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.conversion\_factor) → 1.0.
      - Set d.base\_rate from (last\_purchase\_details at “base\_rate” × (flt(d.conversion\_factor) or 1.0)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.conversion\_factor) → 1.0.
      - Set d.price\_list\_rate from (d.base\_price\_list\_rate ÷ conversion\_rate).
      - Set d.rate from (d.base\_rate ÷ conversion\_rate).
      - Set d.last\_purchase\_rate from d.rate.
      - Evaluate remove\_margin(d).
    - Otherwise.
      - Set item\_last\_purchase\_rate from Platform.get\_cached\_value(“Item”, d.item\_code, “last\_purchase\_rate”).
      - If item\_last\_purchase\_rate.
        - Set d.base\_price\_list\_rate, d.base\_rate from (item\_last\_purchase\_rate × (flt(d.conversion\_factor) or 1.0)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.conversion\_factor) → 1.0.
        - Set d.price\_list\_rate, d.rate, d.last\_purchase\_rate from (d.base\_rate ÷ conversion\_rate).
        - Evaluate remove\_margin(d).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “last\_purchase\_rate”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1371)

<a id="op-62bff2a72fe485"></a>
### Purchase Order.update ordered qty

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_ordered_quantity`

**Inputs** self, po\_item\_rows = no value.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set item\_wh\_list from list().
- For each d in self.get(“items”).
  - If ((not po\_item\_rows or d.name belongs to po\_item\_rows) and list(d.item\_code, d.warehouse) does not belong to item\_wh\_list and Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”) and d.warehouse  ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not po\_item\_rows or d.name belongs to po\_item\_rows) → list(d.item\_code, d.warehouse) does not belong to item\_wh\_list → Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”) → d.warehouse → not d.delivered\_by\_supplier.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not po\_item\_rows → d.name belongs to po\_item\_rows.
    - Evaluate item\_wh\_list.append(list(d.item\_code, d.warehouse)).
- For each tuple(item\_code, warehouse) in item\_wh\_list.
  - Evaluate update\_bin\_qty(item\_code, warehouse, mapping(“ordered\_qty” → get\_ordered\_qty(item\_code, warehouse))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0338.json#L3190) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1382)

<a id="op-94dc3dfb573f56"></a>
### Purchase Order.check modified date

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_purchaseorder_check_modified_date`

**Inputs** self.

**Record and data access** execute query text (SELECT, Purchase).

**State and service calls** execute a supplied database query.

**Local steps**

- Set mod\_db from Platform.db.sql(query text (SELECT, Purchase), self.name).
- Set date\_diff from Platform.db.sql(formatted text select '{mod\_db at 0 at 0}' - '{cstr(self.modified)}' ).
- If (date\_diff and date\_diff at 0 at 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in date\_diff → date\_diff at 0 at 0.
  - Evaluate msgprint(translated “{0} {1} has been modified. Please refresh.”.format(self.doctype, self.name), raise\_exception = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L52)

<a id="op-ef288b09df8d7a"></a>
### Purchase Order.update prevdoc status

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_prevdoc_status`

**Inputs** self.

**Record and data access** resolve a document from “Supplier Quotation” via get\_doc.

**Explicit failure paths** validation helper — translated “Supplier Quotation {0} is cancelled”.format(supplier\_quotation).

**Local steps**

- If self.is\_subcontracted.
  - Set self.status\_updater at 0 at “source\_field” from “fg\_item\_qty”.
- Evaluate super().update\_prevdoc\_status().
- For each supplier\_quotation in set of item.supplier\_quotation for item drawn from self.items.
  - Draw item from self.items.
  - If not supplier\_quotation.
    - Continue with the next iteration or loop test.
  - Set doc from Platform.get\_doc(“Supplier Quotation”, supplier\_quotation).
  - If doc.docstatus.is\_cancelled().
    - Call the validation error handler Platform.throw(translated “Supplier Quotation {0} is cancelled”.format(supplier\_quotation)).
  - Evaluate doc.set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1384)

<a id="op-8bfe8f8ce4d688"></a>
### Purchase Order.update status

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_update_status`

**Inputs** self, status.

**Local steps**

- Bind dependencies validate\_reopen\_against\_blanket\_order.
- Evaluate self.check\_modified\_date().
- Set was\_closed from self.status equals “Closed”.
- If (status differs from “Closed” and was\_closed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status differs from “Closed” → was\_closed.
  - Evaluate validate\_reopen\_against\_blanket\_order(self).
- Evaluate self.set\_status(update = true, status = status).
- Evaluate self.update\_requested\_qty().
- Evaluate self.update\_ordered\_qty().
- Evaluate self.update\_reserved\_qty\_for\_subcontract().
- If (status equals “Closed” or was\_closed).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status equals “Closed” → was\_closed.
  - Evaluate self.update\_subcontracting\_order\_status().
- Evaluate self.update\_blanket\_order().
- Evaluate self.notify\_update().
- Evaluate clear\_doctype\_notifications(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check modified date](operations-002.md#op-94dc3dfb573f56), [update ordered qty](operations-002.md#op-62bff2a72fe485), [update reserved qty for subcontract](operations-003.md#op-10887b4d05fea4), [update subcontracting order status](operations-003.md#op-f8ec8678e8f764).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1386)

<a id="op-2d31e638b82351"></a>
### Purchase Order.on submit

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Authorization Control” via get\_cached\_doc.

**Local steps**

- Evaluate super().on\_submit().
- If self.is\_against\_so().
  - Evaluate self.update\_status\_updater().
- If self.is\_against\_pp().
  - Evaluate self.update\_status\_updater\_if\_from\_pp().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.update\_requested\_qty().
- Evaluate self.update\_ordered\_qty().
- Evaluate self.validate\_budget().
- Evaluate self.update\_reserved\_qty\_for\_subcontract().
- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(self.doctype, self.company, self.base\_grand\_total).
- Evaluate self.update\_blanket\_order().
- Evaluate update\_linked\_doc(self.doctype, self.name, self.inter\_company\_order\_reference).
- Evaluate self.auto\_create\_subcontracting\_order().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is against so](operations-003.md#op-c70a01a06197c3), [update status updater](operations-003.md#op-8810017227a24f), [is against pp](operations-003.md#op-97f7defb881378), [update status updater if from pp](operations-003.md#op-238282a0c86233), [update prevdoc status](operations-002.md#op-ef288b09df8d7a), [update ordered qty](operations-002.md#op-62bff2a72fe485), [update reserved qty for subcontract](operations-003.md#op-10887b4d05fea4), [auto create subcontracting order](operations-003.md#op-aee7bdc8f4bd23).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1377)

<a id="op-b6b18869ca4fca"></a>
### Purchase Order.on cancel

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_purchase_order_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Payment Ledger Entry”, “Advance Payment Ledger Entry”, “Unreconcile Payment”, …).
- Evaluate super().on\_cancel().
- If self.is\_against\_so().
  - Evaluate self.update\_status\_updater().
- If self.is\_against\_pp().
  - Evaluate self.update\_status\_updater\_if\_from\_pp().
- If self.has\_drop\_ship\_item().
  - Evaluate self.set\_received\_qty\_to\_zero\_for\_drop\_ship\_items().
  - Evaluate self.update\_receiving\_percentage().
  - Evaluate self.update\_delivered\_qty\_in\_sales\_order().
- Evaluate self.update\_reserved\_qty\_for\_subcontract().
- Evaluate self.check\_for\_on\_hold\_or\_closed\_status(“Material Request”, “material\_request”).
- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.update\_requested\_qty().
- Evaluate self.update\_ordered\_qty().
- Evaluate self.update\_blanket\_order().
- Evaluate unlink\_inter\_company\_doc(self.doctype, self.name, self.inter\_company\_order\_reference).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is against so](operations-003.md#op-c70a01a06197c3), [update status updater](operations-003.md#op-8810017227a24f), [is against pp](operations-003.md#op-97f7defb881378), [update status updater if from pp](operations-003.md#op-238282a0c86233), [has drop ship item](operations-003.md#op-1bdeec63022cc2), [set received qty to zero for drop ship items](operations-003.md#op-078842097cb386), [update receiving percentage](operations-003.md#op-045bbf8188f24a), [update delivered qty in sales order](operations-003.md#op-29340c99cd1a51), [update reserved qty for subcontract](operations-003.md#op-10887b4d05fea4), [update prevdoc status](operations-002.md#op-ef288b09df8d7a), [update ordered qty](operations-002.md#op-62bff2a72fe485).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1376)
