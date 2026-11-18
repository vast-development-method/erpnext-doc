# Inventory and warehouses · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Item

[Record definition](../../../../data/record-types/item.json)

<a id="op-3244b2f9b87445"></a>
### Get timeline data

`operation_enterprise_stock_record_definitions_item_business_behavior_get_timeline_data`

**Inputs** doctype, name.

**Declared result** dict at tuple(int, int).

**Explicit results** dict(nested operand in the contract.where(nested operand in the contract &gt; nested operand in the contract).groupby(sle.posting\_date).run()).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Return dict(nested operand in the contract.where(nested operand in the contract &gt; nested operand in the contract).groupby(sle.posting\_date).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1083)

<a id="op-bb3ddf5cfdd9c8"></a>
### Validate end of life

`operation_enterprise_stock_record_definitions_item_business_behavior_validate_end_of_life`

**Inputs** item\_code, end\_of\_life = no value, disabled = no value.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Item {0} has reached its end of life on {1}”.format(item\_code, formatdate(end\_of\_life)) · validation helper — translated “Item {0} is disabled”.format(item\_code).

**Local steps**

- If (not end\_of\_life or disabled is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not end\_of\_life → disabled is identical to no value.
  - Set tuple(end\_of\_life, disabled) from Platform.db.get\_value(“Item”, item\_code, list(“end\_of\_life”, “disabled”)).
- If (end\_of\_life and end\_of\_life differs from “0000-00-00” and getdate(end\_of\_life) ≤ now\_datetime().date()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_of\_life → end\_of\_life differs from “0000-00-00” → getdate(end\_of\_life) ≤ now\_datetime().date().
  - Call the validation error handler Platform.throw(translated “Item {0} has reached its end of life on {1}”.format(item\_code, formatdate(end\_of\_life))).
- If disabled.
  - Call the validation error handler Platform.throw(translated “Item {0} is disabled”.format(item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L6543) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1146)

<a id="op-0a9d120fee9eaa"></a>
### Validate is stock item

`operation_enterprise_stock_record_definitions_item_business_behavior_validate_is_stock_item`

**Inputs** item\_code, is\_stock\_item = no value.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Item {0} is not a stock Item”.format(item\_code).

**Local steps**

- If not is\_stock\_item.
  - Set is\_stock\_item from Platform.db.get\_value(“Item”, item\_code, “is\_stock\_item”).
- <a id="op-0a9d120fee9eaa-guard-5"></a>If is\_stock\_item differs from 1.
  - Call the validation error handler Platform.throw(translated “Item {0} is not a stock Item”.format(item\_code)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison is\_stock\_item differs from 1, is\_stock\_item = 2 selects the branch that calls the validation-error handler with translated “Item {0} is not a stock Item”.format(item\_code). With is\_stock\_item = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0a9d120fee9eaa-guard-5)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0733.json#L6919) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1147)

<a id="op-a5de57bd1f97ab"></a>
### Validate cancelled item

`operation_enterprise_stock_record_definitions_item_business_behavior_validate_cancelled_item`

**Inputs** item\_code, docstatus = no value.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Item {0} is cancelled”.format(item\_code).

**Local steps**

- If docstatus is identical to no value.
  - Set docstatus from Platform.db.get\_value(“Item”, item\_code, “docstatus”).
- <a id="op-a5de57bd1f97ab-guard-5"></a>If docstatus equals 2.
  - Call the validation error handler Platform.throw(translated “Item {0} is cancelled”.format(item\_code)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison docstatus equals 2, docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “Item {0} is cancelled”.format(item\_code). With docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-a5de57bd1f97ab-guard-5)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0734.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1145)

<a id="op-4c0baf7c70af60"></a>
### Get last purchase details

`operation_enterprise_stock_record_definitions_item_business_behavior_get_last_purchase_details`

**Inputs** item\_code, doc\_name = no value, conversion\_rate = 1.0.

**Wrappers, in declaration order** Platform.request\_cache.

**Explicit results** Platform.\_dict() · out.

**Local steps**

- Set last\_purchase\_order from get\_purchase\_voucher\_details(“Purchase Order”, item\_code, doc\_name).
- Set last\_purchase\_receipt from get\_purchase\_voucher\_details(“Purchase Receipt”, item\_code, doc\_name).
- Set purchase\_order\_date from getdate(((last\_purchase\_order and last\_purchase\_order at 0.transaction\_date) or “1900-01-01”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (last\_purchase\_order and last\_purchase\_order at 0.transaction\_date) → “1900-01-01”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_purchase\_order → last\_purchase\_order at 0.transaction\_date.
- Set purchase\_receipt\_date from getdate(((last\_purchase\_receipt and last\_purchase\_receipt at 0.posting\_date) or “1900-01-01”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (last\_purchase\_receipt and last\_purchase\_receipt at 0.posting\_date) → “1900-01-01”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_purchase\_receipt → last\_purchase\_receipt at 0.posting\_date.
- If (last\_purchase\_order and (purchase\_order\_date ≥ purchase\_receipt\_date or not last\_purchase\_receipt)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_purchase\_order → (purchase\_order\_date ≥ purchase\_receipt\_date or not last\_purchase\_receipt).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in purchase\_order\_date ≥ purchase\_receipt\_date → not last\_purchase\_receipt.
  - Set last\_purchase from last\_purchase\_order at 0.
  - Set purchase\_date from purchase\_order\_date.
- Otherwise.
  - If (last\_purchase\_receipt and (purchase\_receipt\_date &gt; purchase\_order\_date or not last\_purchase\_order)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_purchase\_receipt → (purchase\_receipt\_date &gt; purchase\_order\_date or not last\_purchase\_order).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in purchase\_receipt\_date &gt; purchase\_order\_date → not last\_purchase\_order.
    - Set last\_purchase from last\_purchase\_receipt at 0.
    - Set purchase\_date from purchase\_receipt\_date.
  - Otherwise.
    - Set last\_purchase\_invoice from get\_purchase\_voucher\_details(“Purchase Invoice”, item\_code, doc\_name).
    - If last\_purchase\_invoice.
      - Set last\_purchase from last\_purchase\_invoice at 0.
      - Set purchase\_date from getdate(last\_purchase.posting\_date).
    - Otherwise.
      - Return Platform.\_dict().
- Set conversion\_factor from flt(last\_purchase.conversion\_factor).
- Set out from Platform.\_dict(mapping(“base\_price\_list\_rate” → (flt(last\_purchase.base\_price\_list\_rate) ÷ conversion\_factor), “base\_rate” → (flt(last\_purchase.base\_rate) ÷ conversion\_factor), “base\_net\_rate” → (flt(last\_ ….
- Set conversion\_rate from (flt(conversion\_rate) or 1.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(conversion\_rate) → 1.0.
- Evaluate out.update(mapping(“price\_list\_rate” → (out.base\_price\_list\_rate ÷ conversion\_rate), “rate” → (out.base\_rate ÷ conversion\_rate), “discount\_amount” → (max((out.base\_price\_list\_rate − out.base\_rate), 0) ÷ co ….
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1081)

<a id="op-199a6a8da1a1c9"></a>
### Get purchase voucher details

`operation_enterprise_stock_record_definitions_item_business_behavior_get_purchase_voucher_details`

**Inputs** doctype, item\_code, document\_name = no value.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set parent\_doc from Platform.qb.DocType(doctype).
- Set child\_doc from Platform.qb.DocType((doctype + “ Item”)).
- Set query from nested operand in the contract(nested operand in the contract).select(parent\_doc.name, parent\_doc.conversion\_rate, child\_doc.conversion\_factor, child\_doc.base\_price\_list\_rate, …).where(parent\_doc.docstatus ….
- If document\_name.
  - Set query from query.where(parent\_doc.name differs from document\_name).
- If doctype belongs to tuple(“Purchase Receipt”, “Purchase Invoice”).
  - Set query from query.where(parent\_doc.is\_return equals 0).
  - Set query from query.select(parent\_doc.posting\_date, parent\_doc.posting\_time).
  - Set query from query.orderby(parent\_doc.posting\_date, parent\_doc.posting\_time, parent\_doc.name, order = Order.desc).
- Otherwise.
  - Set query from query.select(parent\_doc.transaction\_date).
  - Set query from query.orderby(parent\_doc.transaction\_date, parent\_doc.name, order = Order.desc).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1082)

<a id="op-9978688fffd9a4"></a>
### Rebuild bin reservations

`operation_enterprise_binding_enterprise_stock_doctype_item_item_rebuild_bin_reservations`

**Inputs** item\_code, warehouse.

**Record and data access** resolve a document from “Bin” via get\_doc.

**Local steps**

- Bind dependencies get\_or\_make\_bin.
- Set bin\_doc from Platform.get\_doc(“Bin”, get\_or\_make\_bin(item\_code, warehouse)).
- Evaluate bin\_doc.update\_reserved\_qty\_for\_sub\_contracting().
- Evaluate bin\_doc.update\_reserved\_stock().
- Evaluate bin\_doc.update\_reserved\_qty\_for\_production().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L793) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L290)

<a id="op-5bfcda60f97c84"></a>
### Check stock uom with bin

`operation_enterprise_stock_record_definitions_item_business_behavior_check_stock_unit_of_measure_with_bin`

**Inputs** item, stock\_uom.

**Record and data access** read “Item” via get\_value · read “Stock Ledger Entry” via get\_value · read “Bin” via get\_all.

**State and service calls** execute query text (UPDATE, Bin).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Default Unit of Measure for Item {0} cannot be changed directly because you have already made some transacti …”.format(item).

**Local steps**

- If stock\_uom equals Platform.db.get\_value(“Item”, item, “stock\_uom”).
  - Return no value.
- Set ref\_uom from Platform.db.get\_value(“Stock Ledger Entry”, mapping(“item\_code” → item, “is\_cancelled” → 0), “stock\_uom”).
- If ref\_uom.
  - If cstr(ref\_uom) differs from cstr(stock\_uom).
    - Call the validation error handler Platform.throw(translated “Default Unit of Measure for Item {0} cannot be changed directly because you have already made some transacti …”.format(item)).
- Set bin\_list from Platform.get\_all(“Bin”, filters = mapping(“item\_code” → item, “stock\_uom” → list(“!=”, stock\_uom)), or\_filters = list(list(“reserved\_qty”, “&gt;”, 0), list(“ordered\_qty”, “&gt;”, 0), list(“indented\_qty”, “&gt;”, 0) ….
- If bin\_list.
  - Call the validation error handler Platform.throw(translated “Default Unit of Measure for Item {0} cannot be changed directly because you have already made some transacti …”.format(item)).
- Evaluate Platform.db.sql(query text (UPDATE, Bin), tuple(stock\_uom, item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1071)

<a id="op-449b2cc1a21db6"></a>
### Get item defaults

`operation_enterprise_stock_record_definitions_item_business_behavior_get_item_defaults`

**Inputs** item\_code, company.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Set item from Platform.get\_cached\_doc(“Item”, item\_code).
- Set out from item.as\_dict().
- For each d in item.item\_defaults.
  - If d.company equals company.
    - Set row from d.as\_dict(no\_private\_properties = true).
    - Evaluate row.pop(“name”).
    - Evaluate out.update(row).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item\_code).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0734.json#L2483) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1078)

<a id="op-33cfa6b3e22ced"></a>
### Set item default

`operation_enterprise_stock_record_definitions_item_business_behavior_set_item_default`

**Inputs** item\_code, company, fieldname, value.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**State and service calls** request set\_value on d.doctype · call db\_insert on d.

**Explicit results** no value.

**Local steps**

- Set item from Platform.get\_cached\_doc(“Item”, item\_code).
- For each d in item.item\_defaults.
  - If d.company equals company.
    - If not d.get(fieldname).
      - Evaluate Platform.db.set\_value(d.doctype, d.name, fieldname, value).
      - Evaluate item.clear\_cache().
    - Return no value.
- Set d from item.append(“item\_defaults”, mapping(fieldname → value, “company” → company)).
- Evaluate d.db\_insert().
- Evaluate item.clear\_cache().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1142)

<a id="op-e4d13de31ccdd3"></a>
### Get item details

`operation_enterprise_stock_record_definitions_item_business_behavior_get_item_details`

**Inputs** item\_code, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_item\_details(item\_code, company, ignore\_permissions = false).

**Local steps**

- Return \_get\_item\_details(item\_code, company, ignore\_permissions = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1079)

<a id="op-a87716934655e7"></a>
### Get item details

`operation_enterprise_binding_enterprise_stock_doctype_item_item_get_item_details`

**Inputs** item\_code, company = no value, ignore\_permissions = true.

**Record and data access** resolve a document from “Item” via get\_cached\_doc.

**Explicit results** out.

**Local steps**

- Set doc from Platform.get\_cached\_doc(“Item”, item\_code).
- If not ignore\_permissions.
  - Evaluate doc.check\_permission().
- Set out from Platform.\_dict().
- If company.
  - Set out from (get\_item\_defaults(item\_code, company) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_item\_defaults(item\_code, company) → Platform.\_dict().
- Evaluate out.update(doc.as\_dict()).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item\_code) · effective access from doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L281)

<a id="op-66379c461f83ff"></a>
### Get uom conv factor

`operation_enterprise_stock_record_definitions_item_business_behavior_get_unit_of_measure_conv_factor`

**Inputs** uom, stock\_uom.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “UOM Conversion Factor” via get\_value.

**Explicit results** 1.0 · exact\_match.value · flt((1 ÷ inverse\_match.value), Platform.get\_precision(“UOM Conversion Factor”, “value”)) · flt(shared\_source\_match at 0.value, Platform.get\_precision(“UOM Conversion Factor”, “value”)) · flt(shared\_target\_match at 0.value, Platform.get\_precision(“UOM Conversion Factor”, “value”)).

**Local steps**

- If uom equals stock\_uom.
  - Return 1.0.
- Set tuple(from\_uom, to\_uom) from tuple(uom, stock\_uom).
- Set exact\_match from Platform.db.get\_value(“UOM Conversion Factor”, mapping(“to\_uom” → to\_uom, “from\_uom” → from\_uom, “value” → list(“&gt;”, 0)), list(“value”), as\_dict = 1).
- If exact\_match.
  - Return exact\_match.value.
- Set inverse\_match from Platform.db.get\_value(“UOM Conversion Factor”, mapping(“to\_uom” → from\_uom, “from\_uom” → to\_uom, “value” → list(“&gt;”, 0)), list(“value”), as\_dict = 1).
- If (inverse\_match and inverse\_match.value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in inverse\_match → inverse\_match.value.
  - Return flt((1 ÷ inverse\_match.value), Platform.get\_precision(“UOM Conversion Factor”, “value”)).
- Set first from Platform.qb.DocType(“UOM Conversion Factor”).as\_(“first”).
- Set second from Platform.qb.DocType(“UOM Conversion Factor”).as\_(“second”).
- Set shared\_source\_match from nested operand in the contract(nested operand in the contract).orderby(first.name, second.name).limit(1).run(as\_dict = 1).
- If shared\_source\_match.
  - Return flt(shared\_source\_match at 0.value, Platform.get\_precision(“UOM Conversion Factor”, “value”)).
- Set shared\_target\_match from nested operand in the contract(nested operand in the contract).orderby(first.name, second.name).limit(1).run(as\_dict = 1).
- If shared\_target\_match.
  - Return flt(shared\_target\_match at 0.value, Platform.get\_precision(“UOM Conversion Factor”, “value”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1084)

<a id="op-2b3a3b90137187"></a>
### Get item attribute

`operation_enterprise_stock_record_definitions_item_business_behavior_get_item_attribute`

**Inputs** parent, attribute\_value = empty text.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item Attribute Value” via get\_all.

**Explicit results** Platform.get\_all(“Item Attribute Value”, fields = list(“attribute\_value”), filters = mapping(“parent” → parent, “attribute\_value” → tuple(“like”, formatted text %{attribute\_value}%))).

**Explicit failure paths** validation helper — translated “No Permission”.

**Local steps**

- If not Platform.has\_permission(“Item”).
  - Call the validation error handler Platform.throw(translated “No Permission”).
- Return Platform.get\_all(“Item Attribute Value”, fields = list(“attribute\_value”), filters = mapping(“parent” → parent, “attribute\_value” → tuple(“like”, formatted text %{attribute\_value}%))).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1077)

<a id="op-6c5e43f3918f01"></a>
### Update variants

`operation_enterprise_stock_record_definitions_item_business_behavior_update_variants`

**Inputs** variants, template, publish\_progress = true.

**Record and data access** resolve a document from “Item” via get\_doc.

**State and service calls** call save on variant.

**Local steps**

- Set total from len(variants).
- For each tuple(count, d) in enumerate(variants, start = 1).
  - Set variant from Platform.get\_doc(“Item”, d).
  - Evaluate copy\_attributes\_to\_variant(template, variant).
  - Evaluate variant.save().
  - If publish\_progress.
    - Evaluate Platform.publish\_progress(((count ÷ total) × 100), title = translated “Updating Variants...”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0734.json#L4821) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1144)

<a id="op-25b825460f8de2"></a>
### Validate item defaults

`operation_enterprise_binding_enterprise_stock_doctype_item_item_validate_item_defaults`

**Inputs** item\_defaults.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Cannot set multiple Item Defaults for a company.”.

**Local steps**

- Set companies from set of row.company for row drawn from item\_defaults.
  - Draw row from item\_defaults.
- If len(companies) differs from len(item\_defaults).
  - Call the validation error handler Platform.throw(translated “Cannot set multiple Item Defaults for a company.”).
- Evaluate validate\_item\_default\_company\_links(item\_defaults).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L820) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L317)

<a id="op-09d123d5e74566"></a>
### Validate item default company links

`operation_enterprise_stock_record_definitions_item_business_behavior_validate_item_default_company_links`

**Inputs** item\_defaults.

**Declared result** no value.

**Record and data access** read doctype via get\_value.

**Explicit failure paths** validation helper — translated “Row #{}: {} {} doesn't belong to Company {}. Please select valid {}.”.format(item\_default.idx, doctype, Platform.bold(item\_default.get(field)), Platform.bold(item\_default.company), …).

**Local steps**

- Set company\_links from list of tuple(df.options, df.fieldname) for df drawn from Platform.get\_meta(“Item Default”).get\_link\_fields() where df.options belongs to tuple(“Warehouse”, “Cost Center”, “Account”).
  - Draw df from Platform.get\_meta(“Item Default”).get\_link\_fields(), keep a combination only if (df.options belongs to tuple(“Warehouse”, “Cost Center”, “Account”)).
- For each item\_default in item\_defaults.
  - For each tuple(doctype, field) in company\_links.
    - If item\_default.get(field).
      - Set company from Platform.db.get\_value(doctype, item\_default.get(field), “company”, cache = true).
      - If (company and company differs from item\_default.company).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → company differs from item\_default.company.
        - Call the validation error handler Platform.throw(translated “Row #{}: {} {} doesn't belong to Company {}. Please select valid {}.”.format(item\_default.idx, doctype, Platform.bold(item\_default.get(field)), Platform.bold(item\_default.company ….
  - Evaluate validate\_default\_inventory\_account(item\_default).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1148)

<a id="op-59eb8a03eabc3a"></a>
### Validate default inventory account

`operation_enterprise_binding_enterprise_stock_doctype_item_item_validate_default_inventory_account`

**Inputs** item\_default.

**Declared result** no value.

**Record and data access** read “Account” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Default Inventory Account {1} must be a Stock account that is not a group.”.format(item\_default.idx, Platform.bold(item\_default.default\_inventory\_account)).

**Local steps**

- If not item\_default.default\_inventory\_account.
  - Return no value.
- Set tuple(account\_type, is\_group) from Platform.db.get\_value(“Account”, item\_default.default\_inventory\_account, list(“account\_type”, “is\_group”), cache = true).
- If (account\_type differs from “Stock” or is\_group).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_type differs from “Stock” → is\_group.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Default Inventory Account {1} must be a Stock account that is not a group.”.format(item\_default.idx, Platform.bold(item\_default.default\_inventory\_account)), title = tra ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L819) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L316)

<a id="op-9c16a58c759ce7"></a>
### Get asset naming series

`operation_enterprise_stock_record_definitions_item_business_behavior_get_asset_naming_series`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_asset\_naming\_series().

**Local steps**

- Bind dependencies get\_asset\_naming\_series.
- Return get\_asset\_naming\_series().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0734.json#L5621) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1074)

<a id="op-800d0f20bfcc7c"></a>
### Get child warehouses

`operation_enterprise_stock_record_definitions_item_business_behavior_get_child_warehouses`

**Inputs** warehouse.

**Wrappers, in declaration order** Platform.request\_cache.

**Explicit results** get\_child\_warehouses(warehouse).

**Local steps**

- Bind dependencies get\_child\_warehouses.
- Return get\_child\_warehouses(warehouse).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0734.json#L5687) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1075)

<a id="op-942234adc86855"></a>
### Get item prices

`operation_enterprise_stock_record_definitions_item_business_behavior_get_item_prices`

**Inputs** item\_code.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item Price” via get\_list.

**Explicit results** mapping(“prices” → prices at slice no value to ITEM\_PRICES\_LIMIT, “has\_more” → len(prices) &gt; ITEM\_PRICES\_LIMIT).

**Local steps**

- Evaluate Platform.has\_permission(“Item Price”, “read”, throw = true).
- Set today from getdate().
- Set prices from Platform.get\_list(“Item Price”, filters = mapping(“item\_code” → item\_code, “docstatus” → list(“!=”, 2)), or\_filters = list(list(“valid\_upto”, “is”, “not set”), list(“valid\_upto”, “&gt;=”, today)), fields = li ….
- Return mapping(“prices” → prices at slice no value to ITEM\_PRICES\_LIMIT, “has\_more” → len(prices) &gt; ITEM\_PRICES\_LIMIT).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item Price”, “read”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1080)

<a id="op-12f11404362fdf"></a>
### Make opening stock entry

`operation_enterprise_stock_record_definitions_item_business_behavior_make_opening_stock_entry`

**Inputs** item\_code, company, qty, valuation\_rate, warehouse = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Item” via get\_doc · read “Warehouse” via get\_value · read “Account” via get\_value.

**State and service calls** msgprint with translated “Opening Stock reconciliation created: {0}”.format(get\_link\_to\_form(“Stock Reconciliation”, stock\_reco.name)).

**Explicit results** stock\_reco.name.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted” · validation helper — translated “Opening Stock can only be set for stock items.” · validation helper — translated “Opening Stock for serialised or batch items must be set via the Stock Reconciliation form.” · validation helper — translated “Opening Stock cannot be created as stock transactions already exist for item {0}.”.format(Platform.bold(item\_code)) · validation helper — translated “Quantity must be greater than zero.” · 3 additional forms in the steps below.

**Local steps**

- If not Platform.has\_permission(“Item”, “write”, item\_code).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set item from Platform.get\_doc(“Item”, item\_code).
- If not item.is\_stock\_item.
  - Call the validation error handler Platform.throw(translated “Opening Stock can only be set for stock items.”).
- If (item.has\_serial\_no or item.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.has\_serial\_no → item.has\_batch\_no.
  - Call the validation error handler Platform.throw(translated “Opening Stock for serialised or batch items must be set via the Stock Reconciliation form.”).
- If item.stock\_ledger\_created().
  - Call the validation error handler Platform.throw(translated “Opening Stock cannot be created as stock transactions already exist for item {0}.”.format(Platform.bold(item\_code))).
- If flt(qty) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Quantity must be greater than zero.”).
- If flt(valuation\_rate) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Valuation Rate cannot be negative.”).
- If warehouse.
  - Set warehouse\_company from Platform.db.get\_value(“Warehouse”, warehouse, “company”).
  - If warehouse\_company differs from company.
    - Call the validation error handler Platform.throw(translated “Warehouse {0} does not belong to Company {1}.”.format(warehouse, company)).
- Set target\_warehouse from get\_default\_warehouse\_for\_opening\_stock(item, company, warehouse).
- Set opening\_account from Platform.db.get\_value(“Account”, mapping(“company” → company, “account\_type” → “Temporary”, “is\_group” → 0), “name”).
- If not opening\_account.
  - Call the validation error handler Platform.throw(translated “Please set a Temporary Opening account for company {0} to create an Opening Stock reconciliation.”.format(Platform.bold(company))).
- Set stock\_reco from create\_opening\_stock\_reconciliation(item\_code = item\_code, company = company, qty = qty, valuation\_rate = valuation\_rate, …).
- Evaluate stock\_reco.add\_comment(“Comment”, translated “Opening Stock”).
- Evaluate Platform.msgprint(translated “Opening Stock reconciliation created: {0}”.format(get\_link\_to\_form(“Stock Reconciliation”, stock\_reco.name)), indicator = “green”, alert = true).
- Return stock\_reco.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “write”, item\_code).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0735.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1141)

<a id="op-298e1c1b98aec2"></a>
### Create opening stock reconciliation

`operation_enterprise_stock_record_definitions_item_business_behavior_create_opening_stock_reconciliation`

**Inputs** item\_code, company, qty, valuation\_rate, warehouse, expense\_account.

**Record and data access** resolve a document from mapping(“doctype” → “Stock Reconciliation”, “purpose” → “Opening Stock”, “company” → company, “expense\_account” → expense\_account, …) via get\_doc.

**State and service calls** call insert on stock\_reco · call submit on stock\_reco.

**Explicit results** stock\_reco.

**Local steps**

- Set stock\_reco from Platform.get\_doc(mapping(“doctype” → “Stock Reconciliation”, “purpose” → “Opening Stock”, “company” → company, “expense\_account” → expense\_account, …)).
  - Value choice on flt(valuation\_rate) equals 0 — true gives 1, false gives 0.
- Evaluate stock\_reco.insert().
- Evaluate set\_opening\_stock\_serial\_batch\_bundle(stock\_reco).
- Evaluate stock\_reco.submit().
- Return stock\_reco.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0735.json#L1208) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1073)

<a id="op-c2d359722ad048"></a>
### Set opening stock serial batch bundle

`operation_enterprise_stock_record_definitions_item_business_behavior_set_opening_stock_serial_batch_bundle`

**Inputs** stock\_reco.

**Record and data access** read “Item” via get\_cached\_value.

**State and service calls** call db\_set on row.

**Explicit results** no value.

**Local steps**

- Set row from stock\_reco.items at 0.
- Set item\_details from Platform.get\_cached\_value(“Item”, row.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).
- If not (item\_details.has\_serial\_no or item\_details.has\_batch\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details.has\_serial\_no → item\_details.has\_batch\_no.
  - Return no value.
- Set bundle from SerialBatchCreation(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “voucher\_type” → stock\_reco.doctype, “voucher\_no” → stock\_reco.name, …)).make\_serial\_and\_batch\_bundle().
- If not bundle.
  - Return no value.
- Evaluate row.db\_set(“serial\_and\_batch\_bundle”, bundle.name, update\_modified = false).
- Set row.serial\_and\_batch\_bundle from bundle.name.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, list(“has\_serial\_no”, “has\_batch\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0735.json#L1643) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1143)
