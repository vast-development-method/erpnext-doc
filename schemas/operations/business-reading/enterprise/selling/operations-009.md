# Sales · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Workspace · Point of sale

<a id="op-01d81620a8ce0b"></a>
### Search by term

`operation_enterprise_selling_page_point_of_sale_business_behavior_search_by_term`

**Inputs** search\_term, warehouse, price\_list.

**Record and data access** resolve a document from “Item” via get\_doc · read “Item Price” via get\_list.

**Explicit results** no value · mapping(“items” → list(item)).

**Local steps**

- Set result from (search\_for\_serial\_or\_batch\_or\_barcode\_number(search\_term) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in search\_for\_serial\_or\_batch\_or\_barcode\_number(search\_term) → mapping().
- Set item\_code from result.get(“item\_code”, search\_term).
- Set serial\_no from result.get(“serial\_no”, empty text).
- Set batch\_no from result.get(“batch\_no”, empty text).
- Set barcode from result.get(“barcode”, empty text).
- If not result.
  - Return no value.
- Set item\_doc from Platform.get\_doc(“Item”, item\_code).
- If not item\_doc.
  - Return no value.
- Set item from mapping(“barcode” → barcode, “batch\_no” → batch\_no, “description” → item\_doc.description, “is\_stock\_item” → item\_doc.is\_stock\_item, …).
- If barcode.
  - Set barcode\_info from next(filter(deferred anonymous expression, item\_doc.get(“barcodes”, list())), no value).
  - If (barcode\_info and barcode\_info.uom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in barcode\_info → barcode\_info.uom.
    - Set uom from next(filter(deferred anonymous expression, item\_doc.uoms), mapping()).
    - Evaluate item.update(mapping(“uom” → barcode\_info.uom, “conversion\_factor” → uom.get(“conversion\_factor”, 1))).
- Set tuple(item\_stock\_qty, is\_stock\_item, is\_negative\_stock\_allowed) from get\_stock\_availability(item\_code, warehouse).
- Set item\_stock\_qty from (item\_stock\_qty floor divide item.get(“conversion\_factor”, 1)).
- Evaluate item.update(mapping(“actual\_qty” → item\_stock\_qty)).
- Set price\_filters from mapping(“price\_list” → price\_list, “item\_code” → item\_code).
- If batch\_no.
  - Set price\_filters at “batch\_no” from list(“in”, list(batch\_no, empty text)).
- If serial\_no.
  - Set price\_filters at “uom” from item\_doc.stock\_uom.
- Set price from Platform.get\_list(doctype = “Item Price”, filters = price\_filters, fields = list(“uom”, “currency”, “price\_list\_rate”, “batch\_no”)).
- Bind local operation \_\_sort for subsequent calls.
- Set price from sorted(price, key = \_\_sort).
- If len(price) &gt; 0.
  - Set p from price.pop(0).
  - Evaluate item.update(mapping(“currency” → p.get(“currency”), “price\_list\_rate” → p.get(“price\_list\_rate”))).
- Return mapping(“items” → list(item)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0657.json#L2296) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1100)

<a id="op-07e0e325e5f3ba"></a>
### Search by term.sort

`operation_enterprise_selling_page_point_of_sale_business_behavior_search_by_term_sort`

**Inputs** p.

**Explicit results** 0 · 1 · 2 · 3 · 4 · 1 additional forms in the steps below.

**Local steps**

- Set p\_uom from p.get(“uom”).
- Set p\_batch from p.get(“batch\_no”).
- Set batch\_no from item.get(“batch\_no”).
- If (batch\_no and p\_batch and p\_batch equals batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no → p\_batch → p\_batch equals batch\_no.
  - If p\_uom equals item.get(“uom”).
    - Return 0.
  - Otherwise.
    - If p\_uom equals item.get(“stock\_uom”).
      - Return 1.
    - Otherwise.
      - Return 2.
- If p\_uom equals item.get(“uom”).
  - Return 3.
- Otherwise.
  - If p\_uom equals item.get(“stock\_uom”).
    - Return 4.
  - Otherwise.
    - Return 5.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0657.json#L4073) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1101)

<a id="op-f222c752fc6883"></a>
### Filter result items

`operation_enterprise_selling_page_point_of_sale_business_behavior_filter_result_items`

**Inputs** result, pos\_profile.

**Record and data access** resolve a document from “POS Profile” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- If (result and result.get(“items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in result → result.get(“items”).
  - Set pos\_profile\_doc from Platform.get\_cached\_doc(“POS Profile”, pos\_profile).
  - Set pos\_item\_groups from get\_item\_group(pos\_profile\_doc).
  - If not pos\_item\_groups.
    - Return no value.
  - Set result at “items” from list of item for item drawn from result.get(“items”) where item.get(“item\_group”) belongs to pos\_item\_groups.
    - Draw item from result.get(“items”), keep a combination only if (item.get(“item\_group”) belongs to pos\_item\_groups).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Profile”, pos\_profile).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0657.json#L4455) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1089)

<a id="op-2dd198eacd1558"></a>
### Check pos profile access

`operation_enterprise_binding_enterprise_selling_page_point_of_sale_point_of_sale_check_pos_profile_access`

**Inputs** pos\_profile.

**Local steps**

- Set ptype from “select” when Platform.only\_has\_select\_perm(“POS Profile”), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(“POS Profile”) — true gives “select”, false gives “read”.
- If (isinstance(pos\_profile, str) and pos\_profile).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(pos\_profile, str) → pos\_profile.
  - Evaluate Platform.has\_permission(“POS Profile”, ptype, doc = pos\_profile, throw = true).
- Otherwise.
  - Evaluate Platform.has\_permission(“POS Profile”, ptype, throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Profile”, ptype, doc = pos\_profile, throw = true), Platform.has\_permission(“POS Profile”, ptype, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L91)

<a id="op-155f90aaf860d8"></a>
### Get parent item group

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_parent_item_group`

**Inputs** pos\_profile.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item Group” via get\_all.

**Explicit results** get\_common\_ancestor\_item\_group(item\_groups) · Platform.get\_all(“Item Group”, mapping(“lft” → 1, “is\_group” → 1), pluck = “name”) at 0.

**Local steps**

- Evaluate check\_pos\_profile\_access(pos\_profile).
- Set item\_groups from get\_item\_groups(pos\_profile).
- If item\_groups.
  - Return get\_common\_ancestor\_item\_group(item\_groups).
- Return Platform.get\_all(“Item Group”, mapping(“lft” → 1, “is\_group” → 1), pluck = “name”) at 0.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1095)

<a id="op-98f9f5a27c4985"></a>
### Get common ancestor item group

`operation_enterprise_binding_enterprise_selling_page_point_of_sale_point_of_sale_get_common_ancestor_item_group`

**Inputs** item\_groups.

**Declared result** str.

**Record and data access** read “Item Group” via get\_all.

**Explicit results** Platform.get\_all(“Item Group”, filters = mapping(“lft” → tuple(“&lt;=”, min(generator of nested operand in the contract.lft for r drawn from bounds)), “rgt” → tuple(“&gt;=”, max(generator of nested operand in th … at 0.

**Local steps**

- Set bounds from Platform.get\_all(“Item Group”, filters = mapping(“name” → tuple(“in”, item\_groups)), fields = list(“lft”, “rgt”)).
- Return Platform.get\_all(“Item Group”, filters = mapping(“lft” → tuple(“&lt;=”, min(generator of nested operand in the contract.lft for r drawn from bounds)), “rgt” → tuple(“&gt;=”, max(generator of nested operand in th … at 0.
  - Draw r from bounds.
  - Draw r from bounds.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L92)

<a id="op-0daf9aa6ff90f7"></a>
### Get items

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_items`

**Inputs** start, page\_length, price\_list, item\_group, pos\_profile, search\_term = empty text.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “POS Profile” via get\_value · read “Item Group” via exists · read “Item Group” via get\_value.

**Explicit results** result · mapping(“items” → result).

**Local steps**

- Evaluate check\_pos\_profile\_access(pos\_profile).
- Set tuple(warehouse, hide\_unavailable\_items) from Platform.db.get\_value(“POS Profile”, pos\_profile, list(“warehouse”, “hide\_unavailable\_items”)).
- Set result from list().
- If search\_term.
  - Set result from (search\_by\_term(search\_term, warehouse, price\_list) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in search\_by\_term(search\_term, warehouse, price\_list) → list().
  - Evaluate filter\_result\_items(result, pos\_profile).
  - If result.
    - Return result.
- If not Platform.db.exists(“Item Group”, item\_group).
  - Set item\_group from get\_root\_of(“Item Group”).
- Set tuple(lft, rgt) from Platform.db.get\_value(“Item Group”, item\_group, list(“lft”, “rgt”)).
- Set item from Platform.qb.DocType(“Item”).
- Set item\_group\_dt from Platform.qb.DocType(“Item Group”).
- Set item\_group\_subquery from nested operand in the contract.qb.from\_(item\_group\_dt).select(item\_group\_dt.name).where((item\_group\_dt.lft ≥ lft bitwise and item\_group\_dt.rgt ≤ rgt)).
- Set query from nested operand in the contract.qb.from\_(item).select(item.name.as\_(“item\_code”), item.item\_name, item.description, item.stock\_uom, …).where((((((nested operand in the contract equals nested operand in the  ….
- Set item\_group\_condition from get\_item\_group\_condition(pos\_profile, item).
- If item\_group\_condition is distinct from no value.
  - Set query from query.where(item\_group\_condition).
- If hide\_unavailable\_items.
  - Set bin\_dt from Platform.qb.DocType(“Bin”).
  - Set query from query.left\_join(bin\_dt).on(bin\_dt.item\_code equals item.name).where((item.is\_stock\_item equals 0 bitwise or ((item.is\_stock\_item equals 1 bitwise and bin\_dt.warehouse equals warehouse) bitwise and bin\_dt.a ….
- Set items\_data from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).limit(cint(page\_length)).offset(cint(start)).run(as\_dict = 1).
- If not items\_data.
  - Return result.
- Set current\_date from Platform.utils.today().
- For each item in items\_data.
  - Set tuple(item.actual\_qty, \_, is\_negative\_stock\_allowed) from get\_stock\_availability(item.item\_code, warehouse).
  - Set ItemPrice from DocType(“Item Price”).
  - Set item\_prices from nested operand in the contract(nested operand in the contract).where((nested operand in the contract ≥ nested operand in the contract bitwise or nested operand in the contract())).orderby(ItemPrice.valid\_f ….
  - Set stock\_uom\_price from next(generator of d for d drawn from item\_prices where d.get(“uom”) equals item.stock\_uom, mapping()).
    - Draw d from item\_prices, keep a combination only if (d.get(“uom”) equals item.stock\_uom).
  - Set item\_uom from item.stock\_uom.
  - Set item\_uom\_price from stock\_uom\_price.
  - If (item.sales\_uom and item.sales\_uom differs from item.stock\_uom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.sales\_uom → item.sales\_uom differs from item.stock\_uom.
    - Set item\_uom from item.sales\_uom.
    - Set sales\_uom\_price from next(generator of d for d drawn from item\_prices where d.get(“uom”) equals item.sales\_uom, mapping()).
      - Draw d from item\_prices, keep a combination only if (d.get(“uom”) equals item.sales\_uom).
    - If sales\_uom\_price.
      - Set item\_uom\_price from sales\_uom\_price.
  - If (item\_prices and not item\_uom\_price).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_prices → not item\_uom\_price.
    - Set item\_uom from item\_prices at 0.get(“uom”).
    - Set item\_uom\_price from item\_prices at 0.
  - Set item\_conversion\_factor from get\_conversion\_factor(item.item\_code, item\_uom).get(“conversion\_factor”).
  - If item.stock\_uom differs from item\_uom.
    - Set item.actual\_qty from (item.actual\_qty floor divide item\_conversion\_factor).
  - If (item\_uom\_price and item\_uom differs from item\_uom\_price.get(“uom”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_uom\_price → item\_uom differs from item\_uom\_price.get(“uom”).
    - Set item\_uom\_price.price\_list\_rate from (item\_uom\_price.price\_list\_rate × item\_conversion\_factor).
  - Evaluate result.append(mapping(expand item, “price\_list\_rate” → item\_uom\_price.get(“price\_list\_rate”), “currency” → item\_uom\_price.get(“currency”), “uom” → item\_uom, …)).
- Return mapping(“items” → result).

**Values supplied outside this operation** clock or generated value from Platform.utils.today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1094)

<a id="op-4a02cf30513b42"></a>
### Search for serial or batch or barcode number

`operation_enterprise_selling_page_point_of_sale_business_behavior_search_for_serial_or_batch_or_barcode_number`

**Inputs** search\_value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, (str bitwise or no value)).

**Explicit results** scan\_barcode(search\_value).

**Local steps**

- Set ptype from “select” when Platform.only\_has\_select\_perm(“POS Profile”), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(“POS Profile”) — true gives “select”, false gives “read”.
- Evaluate Platform.has\_permission(“POS Profile”, ptype, throw = true).
- Return scan\_barcode(search\_value).

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Profile”, ptype, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1102)

<a id="op-e5104940b5af5d"></a>
### Get conditions

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_conditions`

**Inputs** search\_term, item = no value.

**Explicit results** Criterion.any(conditions).

**Local steps**

- If item is identical to no value.
  - Set item from Platform.qb.DocType(“Item”).
- Set pattern from formatted text %{search\_term}%.
- Set conditions from list(item.name.like(pattern), item.item\_name.like(pattern)).
- Update conditions using + add\_search\_fields\_condition(search\_term, item).
- Return Criterion.any(conditions).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0658.json#L2789) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1090)

<a id="op-e65a5edf8fefd8"></a>
### Add search fields condition

`operation_enterprise_selling_page_point_of_sale_business_behavior_add_search_fields_condition`

**Inputs** search\_term, item = no value.

**Record and data access** read “POS Search Fields” via get\_all.

**Explicit results** conditions.

**Local steps**

- If item is identical to no value.
  - Set item from Platform.qb.DocType(“Item”).
- Set pattern from formatted text %{search\_term}%.
- Set conditions from list().
- Set search\_fields from Platform.get\_all(“POS Search Fields”, fields = list(“fieldname”)).
- For each field in search\_fields.
  - If not field.get(“fieldname”).
    - Continue with the next iteration or loop test.
  - Evaluate conditions.append(item at field at “fieldname”.like(pattern)).
- Return conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0658.json#L3040) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1086)

<a id="op-f49c569f2e7831"></a>
### Get item group condition

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_item_group_condition`

**Inputs** pos\_profile, item = no value.

**Explicit results** item.item\_group.isin(item\_groups) · no value.

**Local steps**

- If item is identical to no value.
  - Set item from Platform.qb.DocType(“Item”).
- Set item\_groups from get\_item\_groups(pos\_profile).
- If item\_groups.
  - Return item.item\_group.isin(item\_groups).
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0658.json#L3361) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1093)

<a id="op-50d9c77d336d55"></a>
### Item group query

`operation_enterprise_selling_page_point_of_sale_business_behavior_item_group_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Item Group” via get\_list.

**Explicit results** Platform.get\_list(“Item Group”, filters = item\_filters, fields = list(“name”), distinct = true, order\_by = empty text, …).

**Local steps**

- Set pos\_profile from filters.get(“pos\_profile”).
- Evaluate check\_pos\_profile\_access(pos\_profile).
- Set item\_filters from list(list(“name”, “like”, formatted text %{txt}%)).
- If pos\_profile.
  - Set item\_groups from get\_item\_groups(pos\_profile).
  - If item\_groups.
    - Evaluate item\_filters.append(list(“name”, “in”, item\_groups)).
- Return Platform.get\_list(“Item Group”, filters = item\_filters, fields = list(“name”), distinct = true, order\_by = empty text, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1098)

<a id="op-2f69c4bf7c0c46"></a>
### Check opening entry

`operation_enterprise_selling_page_point_of_sale_business_behavior_check_opening_entry`

**Inputs** user.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “POS Opening Entry” via get\_all.

**Explicit results** open\_vouchers.

**Local steps**

- If user differs from Platform.session.user.
  - Evaluate Platform.has\_permission(“POS Opening Entry”, throw = true).
- Set open\_vouchers from Platform.db.get\_all(“POS Opening Entry”, filters = mapping(“user” → user, “pos\_closing\_entry” → list(“in”, list(empty text, no value)), “docstatus” → 1), fields = list(“name”, “company”, “pos\_profile”, “pe ….
- Return open\_vouchers.

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Opening Entry”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1087)

<a id="op-606cc9d2126fe0"></a>
### Create opening voucher

`operation_enterprise_selling_page_point_of_sale_business_behavior_create_opening_voucher`

**Inputs** pos\_profile, company, balance\_details.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “POS Opening Entry”, “period\_start\_date” → Platform.utils.get\_datetime(), “posting\_date” → Platform.utils.getdate(), “user” → Platform.session.user, …) via get\_doc.

**State and service calls** call submit on new\_pos\_opening.

**Explicit results** new\_pos\_opening.as\_dict().

**Local steps**

- Evaluate check\_pos\_profile\_access(pos\_profile).
- Set balance\_details from Platform.parse\_json(balance\_details).
- Set new\_pos\_opening from Platform.get\_doc(mapping(“doctype” → “POS Opening Entry”, “period\_start\_date” → Platform.utils.get\_datetime(), “posting\_date” → Platform.utils.getdate(), “user” → Platform.session.user, …)).
- Evaluate new\_pos\_opening.set(“balance\_details”, balance\_details).
- Evaluate new\_pos\_opening.submit().
- Return new\_pos\_opening.as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1088)

<a id="op-bcb15875468d2e"></a>
### Get past order list

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_past_order_list`

**Inputs** search\_term, status, limit = 20.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “POS Invoice” via get\_list · read “Sales Invoice” via get\_list.

**Explicit results** invoice\_list.

**Local steps**

- Set fields from list(“name”, “grand\_total”, “currency”, “customer”, …).
- Set invoice\_list from list().
- If (search\_term and status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in search\_term → status.
  - Set pos\_invoices\_by\_customer from Platform.db.get\_list(“POS Invoice”, filters = get\_invoice\_filters(“POS Invoice”, status), or\_filters = mapping(“customer\_name” → list(“like”, formatted text %{search\_term}%), “customer” → list(“like”, form ….
  - Set pos\_invoices\_by\_name from Platform.db.get\_list(“POS Invoice”, filters = get\_invoice\_filters(“POS Invoice”, status, name = search\_term), fields = fields, page\_length = limit).
  - Set pos\_invoice\_list from add\_doctype\_to\_results(“POS Invoice”, (pos\_invoices\_by\_customer + pos\_invoices\_by\_name)).
  - Set sales\_invoices\_by\_customer from Platform.db.get\_list(“Sales Invoice”, filters = get\_invoice\_filters(“Sales Invoice”, status), or\_filters = mapping(“customer\_name” → list(“like”, formatted text %{search\_term}%), “customer” → list(“like”,  ….
  - Set sales\_invoices\_by\_name from Platform.db.get\_list(“Sales Invoice”, filters = get\_invoice\_filters(“Sales Invoice”, status, name = search\_term), fields = fields, page\_length = limit).
  - Set sales\_invoice\_list from add\_doctype\_to\_results(“Sales Invoice”, (sales\_invoices\_by\_customer + sales\_invoices\_by\_name)).
- Otherwise.
  - If status.
    - Set pos\_invoice\_list from Platform.db.get\_list(“POS Invoice”, filters = get\_invoice\_filters(“POS Invoice”, status), fields = fields, page\_length = limit).
    - Set pos\_invoice\_list from add\_doctype\_to\_results(“POS Invoice”, pos\_invoice\_list).
    - Set sales\_invoice\_list from Platform.db.get\_list(“Sales Invoice”, filters = get\_invoice\_filters(“Sales Invoice”, status), fields = fields, page\_length = limit).
    - Set sales\_invoice\_list from add\_doctype\_to\_results(“Sales Invoice”, sales\_invoice\_list).
- Set invoice\_list from order\_results\_by\_posting\_date(list(expanded pos\_invoice\_list, expanded sales\_invoice\_list)).
- Return invoice\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1096)

<a id="op-9b1457ebd99293"></a>
### Set customer info

`operation_enterprise_selling_page_point_of_sale_business_behavior_set_customer_info`

**Inputs** fieldname, customer, value = empty text.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Customer” via get\_doc · resolve a document from “Contact” via get\_doc.

**State and service calls** request new\_doc for “Contact” · call save on new\_contact · call save on contact\_doc · call save on customer\_doc.

**Local steps**

- Set customer\_doc from Platform.get\_doc(“Customer”, customer).
- Evaluate customer\_doc.check\_permission(“write”).
- If fieldname equals “loyalty\_program”.
  - Set customer\_doc.loyalty\_program from value.
- Otherwise.
  - Set contact from customer\_doc.get(“customer\_primary\_contact”).
  - If not contact.
    - Set Contact from DocType(“Contact”).
    - Set DynamicLink from DocType(“Dynamic Link”).
    - Set query from nested operand in the contract(nested operand in the contract).select(DynamicLink.parent).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the con ….
    - Set contacts from query.run(pluck = DynamicLink.parent).
    - Set contact from contacts at 0 when contacts, otherwise no value.
      - Value choice on contacts — true gives contacts at 0, false gives no value.
  - If not contact.
    - Set new\_contact from Platform.new\_doc(“Contact”).
    - Set new\_contact.is\_primary\_contact from 1.
    - Set new\_contact.first\_name from customer.
    - Evaluate new\_contact.set(“links”, list(mapping(“link\_doctype” → “Customer”, “link\_name” → customer))).
    - Evaluate new\_contact.save().
    - Set contact from new\_contact.name.
  - Bind local operation set\_primary\_phone\_no\_email for subsequent calls.
  - Set contact\_doc from Platform.get\_doc(“Contact”, contact).
  - Evaluate contact\_doc.set(“is\_primary\_contact”, 1).
  - If fieldname equals “email\_id”.
    - Evaluate set\_primary\_phone\_no\_email(“email\_ids”, value).
  - Otherwise.
    - If fieldname equals “mobile\_no”.
      - Evaluate set\_primary\_phone\_no\_email(“phone\_nos”, value).
  - Evaluate contact\_doc.save().
  - Set customer\_doc.customer\_primary\_contact from contact.
- Evaluate customer\_doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from customer\_doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1103)

<a id="op-e421491ca96845"></a>
### Set customer info.set primary phone no email

`operation_enterprise_selling_page_point_of_sale_business_behavior_set_customer_info_set_primary_phone_number_email`

**Inputs** field, value.

**Local steps**

- Set field\_mapper from mapping(“email\_ids” → mapping(“field” → “email\_id”, “primary” → “is\_primary”), “phone\_nos” → mapping(“field” → “phone”, “primary” → “is\_primary\_mobile\_no”)).
- Set value\_already\_exists from false.
- For each d in contact\_doc.get(field).
  - If (d.get(field\_mapper at field.get(“field”)) equals value and not value\_already\_exists).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(field\_mapper at field.get(“field”)) equals value → not value\_already\_exists.
    - Evaluate d.set(field\_mapper at field at “primary”, 1).
    - Set value\_already\_exists from true.
    - Continue with the next iteration or loop test.
  - Evaluate d.set(field\_mapper at field at “primary”, 0).
- If not value\_already\_exists.
  - Evaluate contact\_doc.append(field, mapping(field\_mapper at field at “field” → value, field\_mapper at field at “primary” → 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0995.json#L626) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1104)

<a id="op-7b90ed3754f738"></a>
### Get pos profile data

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_point_of_sale_profile_data`

**Inputs** pos\_profile.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “POS Profile” via get\_doc.

**Explicit results** pos\_profile.

**Local steps**

- Evaluate check\_pos\_profile\_access(pos\_profile).
- Set pos\_profile from Platform.get\_doc(“POS Profile”, pos\_profile).
- Set pos\_profile from pos\_profile.as\_dict().
- Set \_customer\_groups\_with\_children from list().
- For each row in pos\_profile.customer\_groups.
  - Set children from get\_child\_nodes(“Customer Group”, row.customer\_group).
  - Evaluate \_customer\_groups\_with\_children.extend(children).
- Set pos\_profile.customer\_groups from \_customer\_groups\_with\_children.
- Return pos\_profile.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1097)

<a id="op-9f85f7a6dfd700"></a>
### Add doctype to results

`operation_enterprise_selling_page_point_of_sale_business_behavior_add_record_type_to_results`

**Inputs** doctype, results.

**Explicit results** results.

**Local steps**

- For each result in results.
  - Set result at “doctype” from doctype.
- Return results.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0659.json#L1830) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1085)

<a id="op-0dc04ad7b5a60e"></a>
### Order results by posting date

`operation_enterprise_selling_page_point_of_sale_business_behavior_order_results_by_posting_date`

**Inputs** results.

**Explicit results** sorted(results, key = deferred anonymous expression, reverse = true).

**Local steps**

- Return sorted(results, key = deferred anonymous expression, reverse = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0659.json#L1914) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1099)

<a id="op-97a32a1e935acd"></a>
### Get invoice filters

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_invoice_filters`

**Inputs** doctype, status, name = no value.

**Explicit results** filters.

**Local steps**

- Set filters from mapping().
- If name.
  - Set filters at “name” from list(“like”, formatted text %{name}%).
- If doctype equals “POS Invoice”.
  - Set filters at “status” from status.
  - If status equals “Partly Paid”.
    - Set filters at “status” from list(“in”, list(“Partly Paid”, “Overdue”, “Unpaid”)).
  - Return filters.
- If doctype equals “Sales Invoice”.
  - Set filters at “is\_created\_using\_pos” from 1.
  - Set filters at “is\_consolidated” from 0.
  - If status equals “Consolidated”.
    - Set filters at “pos\_closing\_entry” from list(“is”, “set”).
  - Otherwise.
    - Set filters at “pos\_closing\_entry” from list(“is”, “not set”).
    - If status equals “Draft”.
      - Set filters at “docstatus” from 0.
    - Otherwise.
      - If status equals “Partly Paid”.
        - Set filters at “status” from list(“in”, list(“Partly Paid”, “Overdue”, “Unpaid”)).
      - Otherwise.
        - Set filters at “docstatus” from 1.
        - If status equals “Paid”.
          - Set filters at “is\_return” from 0.
        - If status equals “Return”.
          - Set filters at “is\_return” from 1.
- Return filters.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0659.json#L2078) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1092)

<a id="op-8012fb9ddad572"></a>
### Get customer recent transactions

`operation_enterprise_selling_page_point_of_sale_business_behavior_get_customer_recent_transactions`

**Inputs** customer.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Invoice” via get\_list · read “POS Invoice” via get\_list.

**Explicit results** invoices.

**Local steps**

- Set sales\_invoices from Platform.db.get\_list(“Sales Invoice”, filters = mapping(“customer” → customer, “docstatus” → 1, “is\_pos” → 1, “is\_consolidated” → 0, …), fields = list(“name”, “grand\_total”, “status”, “posting\_date”, …), p ….
- Set pos\_invoices from Platform.db.get\_list(“POS Invoice”, filters = mapping(“customer” → customer, “docstatus” → 1), fields = list(“name”, “grand\_total”, “status”, “posting\_date”, …), page\_length = 20).
- Set invoices from order\_results\_by\_posting\_date((sales\_invoices + pos\_invoices)).
- Return invoices.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1091)

## Record · Product bundle

[Record definition](../../../../data/record-types/product_bundle.json)

<a id="op-b7108c2106fb15"></a>
### Product Bundle.autoname

`operation_enterprise_selling_record_definitions_product_bundle_business_behavior_product_bundle_autoname`

**Inputs** self.

**Local steps**

- Set self.name from self.new\_item\_code.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1831) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1218)

<a id="op-14fa92b5e25fc7"></a>
### Product Bundle.validate

`operation_enterprise_selling_record_definitions_product_bundle_business_behavior_product_bundle_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_main\_item().
- Evaluate self.validate\_child\_items().
- Evaluate self.validate\_not\_nested().
- Evaluate self.validate\_child\_items\_uom().
- Evaluate self.validate\_child\_items\_qty\_non\_zero().
- Bind dependencies validate\_uom\_is\_integer.
- Evaluate validate\_uom\_is\_integer(self, “uom”, “qty”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate main item](operations-010.md#op-20eac366bcb5df), [validate child items](operations-010.md#op-02727b24f14aff), [validate not nested](operations-010.md#op-f69ea0b3943307), [validate child items uom](operations-010.md#op-1f6a1eda6018c2), [validate child items qty non zero](operations-010.md#op-9d5ba15c0a5d7a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1837) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1220)
