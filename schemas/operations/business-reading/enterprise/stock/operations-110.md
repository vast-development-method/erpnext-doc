# Inventory and warehouses · operations 110

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Warehouse

[Record definition](../../../../data/record-types/warehouse.json)

<a id="op-4294d1bc083c9b"></a>
### Warehouse.on update

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_on_update`

**Inputs** self.

**Local steps**

- Evaluate super().on\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L18)

<a id="op-3d1e3c9419b5be"></a>
### Warehouse.update nsm model

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_update_nested_set_model_model`

**Inputs** self.

**Local steps**

- Evaluate Platform.utils.nestedset.update\_nsm(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L2804) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L21)

<a id="op-6a6877bb0fde06"></a>
### Warehouse.on trash

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_on_trash`

**Inputs** self.

**State and service calls** request delete on “Bin”.

**Local steps**

- If bin\_with\_qty bound to self.get\_bin\_with\_quantity().
  - Evaluate throw(translated “Warehouse {0} can not be deleted as quantity exists for Item {1}”.format(self.name, bin\_with\_qty.item\_code)).
- If self.check\_if\_sle\_exists().
  - Evaluate throw(translated “Warehouse can not be deleted as stock ledger entry exists for this warehouse.”).
- If self.check\_if\_child\_exists().
  - Evaluate throw(translated “Child warehouse exists for this warehouse. You can not delete this warehouse.”).
- Evaluate Platform.db.delete(“Bin”, filters = mapping(“warehouse” → self.name)).
- Evaluate self.update\_nsm\_model().
- Evaluate self.unlink\_from\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get bin with quantity](operations-110.md#op-b549dff773aaad), [check if sle exists](operations-110.md#op-9b3e0b6b71a80c), [check if child exists](operations-110.md#op-ff68794464e502), [update nsm model](operations-110.md#op-3d1e3c9419b5be), [unlink from items](operations-110.md#op-4d90690b6212f6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L17)

<a id="op-b549dff773aaad"></a>
### Warehouse.get bin with quantity

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_warehouse_warehouse_get_bin_with_quantity`

**Inputs** self.

**Record and data access** read “Bin” via get\_all.

**Explicit results** d.

**Local steps**

- Set qty\_fields from tuple(“actual\_qty”, “reserved\_qty”, “ordered\_qty”, “indented\_qty”, …).
- For each d in Platform.get\_all(“Bin”, fields = list(“item\_code”, expanded qty\_fields), filters = mapping(“warehouse” → self.name)).
  - If any(generator of d.get(field) for field drawn from qty\_fields).
    - Draw field from qty\_fields.
    - Return d.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L844)

<a id="op-8438ede5d7a30c"></a>
### Warehouse.warn about multiple warehouse account

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_warn_about_multiple_warehouse_account`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via count.

**State and service calls** msgprint.

**Explicit results** no value.

**Local steps**

- If not Platform.db.count(“Stock Ledger Entry”, mapping(“warehouse” → self.name)).
  - Return no value.
- Set doc\_before\_save from self.get\_doc\_before\_save().
- Set old\_wh\_account from doc\_before\_save.account when doc\_before\_save, otherwise no value.
  - Value choice on doc\_before\_save — true gives doc\_before\_save.account, false gives no value.
- If (self.is\_new() or (self.account and old\_wh\_account equals self.account)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → (self.account and old\_wh\_account equals self.account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.account → old\_wh\_account equals self.account.
  - Return no value.
- Evaluate Platform.msgprint(title = translated “Warning: Account changed for warehouse”, indicator = “orange”, msg = translated “Stock entries exist with the old account. Changing the account may lead to a mismatch  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L3391) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L24)

<a id="op-9b3e0b6b71a80c"></a>
### Warehouse.check if sle exists

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_check_if_stock_ledger_entry_exists`

**Inputs** self, non\_cancelled\_only = false.

**Record and data access** read “Stock Ledger Entry” via exists.

**Explicit results** Platform.db.exists(“Stock Ledger Entry”, filters).

**Local steps**

- Set filters from mapping(“warehouse” → self.name).
- If non\_cancelled\_only.
  - Set filters at “is\_cancelled” from 0.
- Return Platform.db.exists(“Stock Ledger Entry”, filters).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L3701) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L13)

<a id="op-ff68794464e502"></a>
### Warehouse.check if child exists

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_check_if_child_exists`

**Inputs** self.

**Record and data access** read “Warehouse” via exists.

**Explicit results** Platform.db.exists(“Warehouse”, mapping(“parent\_warehouse” → self.name)).

**Local steps**

- Return Platform.db.exists(“Warehouse”, mapping(“parent\_warehouse” → self.name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L3850) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L12)

<a id="op-4b6112f31acb1b"></a>
### Warehouse.convert to group or ledger

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_convert_to_group_or_ledger`

**Inputs** self.

**Local steps**

- If self.is\_group.
  - Evaluate self.convert\_to\_ledger().
- Otherwise.
  - Evaluate self.convert\_to\_group().

If control reaches the end, it returns no value.

**Methods declared on this owner** [convert to ledger](operations-110.md#op-1ad3a984a57d53), [convert to group](operations-110.md#op-05ac6db5ad616f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L3940) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L15)

<a id="op-1ad3a984a57d53"></a>
### Warehouse.convert to ledger

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_convert_to_ledger`

**Inputs** self.

**State and service calls** call save on self.

**Explicit results** 1.

**Explicit failure paths** validation helper — translated “Warehouses with child nodes cannot be converted to ledger”.

**Local steps**

- If self.check\_if\_child\_exists().
  - Call the validation error handler Platform.throw(translated “Warehouses with child nodes cannot be converted to ledger”).
- Otherwise.
  - If self.check\_if\_sle\_exists().
    - Evaluate throw(translated “Warehouses with existing transaction can not be converted to ledger.”).
  - Otherwise.
    - Set self.is\_group from 0.
    - Evaluate self.save().
    - Return 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if child exists](operations-110.md#op-ff68794464e502), [check if sle exists](operations-110.md#op-9b3e0b6b71a80c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L4026) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L16)

<a id="op-05ac6db5ad616f"></a>
### Warehouse.convert to group

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_convert_to_group`

**Inputs** self.

**State and service calls** call save on self.

**Explicit results** 1.

**Local steps**

- If self.check\_if\_sle\_exists().
  - Evaluate throw(translated “Warehouses with existing transaction can not be converted to group.”).
- Otherwise.
  - Set self.is\_group from 1.
  - Evaluate self.save().
  - Return 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if sle exists](operations-110.md#op-9b3e0b6b71a80c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L4220) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L14)

<a id="op-4d90690b6212f6"></a>
### Warehouse.unlink from items

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_warehouse_unlink_from_items`

**Inputs** self.

**State and service calls** request set\_value on “Item Default”.

**Local steps**

- Evaluate Platform.db.set\_value(“Item Default”, mapping(“default\_warehouse” → self.name), “default\_warehouse”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L4353) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L20)

<a id="op-a7cb98a2bfa371"></a>
### Get children

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_get_children`

**Inputs** doctype, parent = no value, company = no value, is\_root = false, include\_disabled = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.get\_list(doctype, fields = fields, filters = filters, order\_by = “name”).

**Local steps**

- If is\_root.
  - Set parent from empty text.
- If isinstance(include\_disabled, str).
  - Set include\_disabled from json.loads(include\_disabled).
- Set fields from list(“name as value”, “is\_group as expandable”).
- Set filters from list(list(IfNull(Field(“parent\_warehouse”), empty text), “=”, parent), list(“company”, “in”, tuple(company, no value, empty text))).
- If (Platform.db.has\_column(doctype, “disabled”) and not include\_disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.has\_column(doctype, “disabled”) → not include\_disabled.
  - Evaluate filters.append(list(“disabled”, “=”, false)).
- Return Platform.get\_list(doctype, fields = fields, filters = filters, order\_by = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L8)

<a id="op-69918e7f7c7614"></a>
### Add node

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_add_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(args).

**Local steps**

- Bind dependencies make\_tree\_args.
- Set args from make\_tree\_args(expanded names Platform.form\_dict).
- If cint(args.is\_root).
  - Set args.parent\_warehouse from no value.
- Evaluate Platform.get\_doc(args).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L4922) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L4)

<a id="op-2a98f58c390ac0"></a>
### Convert to group or ledger

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_convert_to_group_or_ledger`

**Inputs** docname = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Warehouse” via get\_doc.

**Explicit results** warehouse.convert\_to\_group\_or\_ledger().

**Local steps**

- If not docname.
  - Set docname from Platform.form\_dict.docname.
- Set warehouse from Platform.get\_doc(“Warehouse”, docname).
- Evaluate warehouse.check\_permission(“write”).
- Return warehouse.convert\_to\_group\_or\_ledger().

**Values supplied outside this operation** effective access from warehouse.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L6)

<a id="op-82e183f26f59fe"></a>
### Get child warehouses

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_get_child_warehouses`

**Inputs** warehouse.

**Wrappers, in declaration order** request\_cache.

**Explicit results** list(expanded children, warehouse).

**Local steps**

- Bind dependencies get\_descendants\_of.
- Set children from get\_descendants\_of(“Warehouse”, warehouse, ignore\_permissions = true, order\_by = “lft”).
- Return list(expanded children, warehouse).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L5245) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L7)

<a id="op-75329bf3b476ec"></a>
### Get warehouses based on account

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_get_warehouses_based_on_account`

**Inputs** account, company = no value.

**Explicit results** warehouses.

**Explicit failure paths** validation helper — translated “Warehouse not found against the account {0}”.format(account).

**Local steps**

- Set warehouse\_account\_map from get\_warehouse\_account\_map(company).
- Set warehouses from list of warehouse for tuple(warehouse, details) drawn from warehouse\_account\_map.items() where (not details.is\_group and details.account equals account).
  - Draw tuple(warehouse, details) from warehouse\_account\_map.items(), keep a combination only if ((not details.is\_group and details.account equals account)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not details.is\_group → details.account equals account.
- If not warehouses.
  - Call the validation error handler Platform.throw(translated “Warehouse not found against the account {0}”.format(account)).
- Return warehouses.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L9)

<a id="op-4107f911eb48fc"></a>
### Apply warehouse filter

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_apply_warehouse_filter`

**Inputs** query, sle, filters.

**Record and data access** read “Warehouse” via get\_all.

**Explicit results** query.

**Local steps**

- If not warehouses bound to filters.get(“warehouse”).
  - Return query.
- Set warehouse\_table from Platform.qb.DocType(“Warehouse”).
- If isinstance(warehouses, str).
  - Set warehouses from list(warehouses).
- Set warehouse\_range from Platform.get\_all(“Warehouse”, filters = mapping(“name” → tuple(“in”, warehouses)), fields = list(“lft”, “rgt”), as\_list = true).
- Set child\_query from Platform.qb.from\_(warehouse\_table).select(warehouse\_table.name).
- Set range\_conditions from list of (warehouse\_table.lft ≥ lft bitwise and warehouse\_table.rgt ≤ rgt) for tuple(lft, rgt) drawn from warehouse\_range.
  - Draw tuple(lft, rgt) from warehouse\_range.
- Set combined\_condition from range\_conditions at 0.
- For each condition in range\_conditions at slice 1 to no value.
  - Set combined\_condition from (combined\_condition bitwise or condition).
- Set child\_query from child\_query.where(combined\_condition).where(warehouse\_table.name equals sle.warehouse).
- Set query from query.where(ExistsCriterion(child\_query)).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0878.json#L5997) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L5)

<a id="op-4cfe964c85e482"></a>
### Get warehouses for reorder

`operation_enterprise_stock_record_definitions_warehouse_business_behavior_get_warehouses_for_reorder`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Warehouse” via exists · read “Warehouse” via get\_list.

**Explicit results** warehouses.

**Explicit failure paths** validation helper — translated “Warehouse {0} does not exist”.format(filters.warehouse).

**Local steps**

- Evaluate Platform.has\_permission(“Warehouse”, throw = true).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If (filters.warehouse and not Platform.db.exists(“Warehouse”, filters.warehouse)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.warehouse → not Platform.db.exists(“Warehouse”, filters.warehouse).
  - Call the validation error handler Platform.throw(translated “Warehouse {0} does not exist”.format(filters.warehouse)).
- Set warehouses from Platform.get\_list(“Warehouse”, filters = mapping(“disabled” → 0), or\_filters = list(list(“is\_group”, “=”, 1), list(“name”, “=”, filters.warehouse)), fields = list(“name”), order\_by = “name”, …).
- Return warehouses.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Warehouse”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L10)

## Service · Warehouse capacity dashboard

<a id="op-899595ca383874"></a>
### Get data

`operation_enterprise_stock_dashboard_warehouse_capacity_dashboard_business_behavior_get_data`

**Inputs** item\_code = no value, warehouse = no value, parent\_warehouse = no value, company = no value, start = 0, sort\_by = “stock\_capacity”, sort\_order = “desc”.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list() · capacity\_data.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, “read”, throw = true).
- Set filters from get\_filters(item\_code, warehouse, parent\_warehouse, company).
- Set tuple(no\_permission, filters) from get\_warehouse\_filter\_based\_on\_permissions(filters).
- If no\_permission.
  - Return list().
- Set capacity\_data from get\_warehouse\_capacity\_data(filters, start).
- Set asc\_desc from negative 1 when sort\_order equals “desc”, otherwise 1.
  - Value choice on sort\_order equals “desc” — true gives negative 1, false gives 1.
- Set capacity\_data from sorted(capacity\_data, key = deferred anonymous expression).
- Return capacity\_data.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L692)

<a id="op-ea682944c2d5f7"></a>
### Get filters

`operation_enterprise_stock_dashboard_warehouse_capacity_dashboard_business_behavior_get_filters`

**Inputs** item\_code = no value, warehouse = no value, parent\_warehouse = no value, company = no value.

**Record and data access** read “Warehouse” via get\_value.

**Explicit results** filters.

**Local steps**

- Set filters from list(list(“disable”, “=”, 0)).
- If item\_code.
  - Evaluate filters.append(list(“item\_code”, “=”, item\_code)).
- If warehouse.
  - Evaluate filters.append(list(“warehouse”, “=”, warehouse)).
- If company.
  - Evaluate filters.append(list(“company”, “=”, company)).
- If parent\_warehouse.
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Warehouse”, parent\_warehouse, list(“lft”, “rgt”)).
  - Set warehouses from Platform.db.sql\_list(query text (SELECT, Warehouse), tuple(lft, rgt)).
  - Evaluate filters.append(list(“warehouse”, “in”, warehouses)).
- Return filters.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L693)

<a id="op-bf4af9c2f78767"></a>
### Get warehouse filter based on permissions

`operation_enterprise_stock_dashboard_warehouse_capacity_dashboard_business_behavior_get_warehouse_filter_based_on_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** filters.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0706.json#L3878) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L695)

<a id="op-a0bada63d8e6b3"></a>
### Get warehouse capacity data

`operation_enterprise_stock_dashboard_warehouse_capacity_dashboard_business_behavior_get_warehouse_capacity_data`

**Inputs** filters, start.

**Record and data access** read “Putaway Rule” via get\_all.

**Explicit results** capacity\_data.

**Local steps**

- Set capacity\_data from Platform.db.get\_all(“Putaway Rule”, fields = list(“item\_code”, “warehouse”, “stock\_capacity”, “company”), filters = filters, limit\_start = start, limit\_page\_length = “11”).
- For each entry in capacity\_data.
  - Set balance\_qty from (\_get\_stock\_balance(entry.item\_code, entry.warehouse, nowdate()) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_get\_stock\_balance(entry.item\_code, entry.warehouse, nowdate()) → 0.
  - Evaluate entry.update(mapping(“warehouse” → escape\_html(entry.warehouse), “item\_code” → escape\_html(entry.item\_code), “company” → escape\_html(entry.company), “actual\_qty” → balance\_qty, …)).
- Return capacity\_data.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L694)

## Record · Warehouse type

[Record definition](../../../../data/record-types/warehouse_type.json)

<a id="op-be758810c29cf3"></a>
### Warehouse Type.on trash

`operation_enterprise_binding_enterprise_stock_doctype_warehouse_type_warehouse_type_warehousetype_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Warehouse Type {0} is required by the system and cannot be deleted”.format(self.name).

**Local steps**

- If self.name equals “Transit”.
  - Call the validation error handler Platform.throw(translated “Warehouse Type {0} is required by the system and cannot be deleted”.format(self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L843)

## Report · Warehouse wise item balance age and value

<a id="op-8deaa25c081ea8"></a>
### Execute

`operation_enterprise_stock_report_warehouse_wise_item_balance_age_and_value_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, list()) · tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Evaluate is\_reposting\_item\_valuation\_in\_progress().
- If not filters.
  - Set filters from mapping().
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- If not apply\_permitted\_warehouses(filters).
  - Return tuple(columns, list()).
- Set items from get\_items(filters).
- Set sle from get\_stock\_ledger\_entries(filters, items).
- Set item\_map from get\_item\_details(items, sle).
- Set iwb\_map from get\_item\_warehouse\_map(filters, sle).
- Set warehouse\_list from get\_warehouse\_list(filters).
- Set item\_ageing from FIFOSlots(filters).generate().
- Set data from list().
- Set item\_balance from mapping().
- Set item\_value from mapping().
- For each tuple(company, item, warehouse) in sorted(iwb\_map).
  - If not item\_map.get(item).
    - Continue with the next iteration or loop test.
  - Set row from list().
  - Set qty\_dict from iwb\_map at tuple(company, item, warehouse).
  - Evaluate item\_balance.setdefault(tuple(item, item\_map at item at “item\_group”), list()).
  - Set total\_stock\_value from 0.0.
  - For each wh in warehouse\_list.
    - Update row using + list(qty\_dict.bal\_qty) when wh.name equals warehouse, otherwise list(0.0).
      - Value choice on wh.name equals warehouse — true gives list(qty\_dict.bal\_qty), false gives list(0.0).
    - Update total\_stock\_value using + qty\_dict.bal\_val when wh.name equals warehouse, otherwise 0.0.
      - Value choice on wh.name equals warehouse — true gives qty\_dict.bal\_val, false gives 0.0.
  - Evaluate item\_balance at tuple(item, item\_map at item at “item\_group”).append(row).
  - Evaluate item\_value.setdefault(tuple(item, item\_map at item at “item\_group”), list()).
  - Evaluate item\_value at tuple(item, item\_map at item at “item\_group”).append(total\_stock\_value).
- Set itemwise\_brand from Platform.\_dict(get\_itemwise\_brand(items)).
- For each tuple(tuple(item, item\_group), wh\_balance) in item\_balance.items().
  - If not item\_ageing.get(item).
    - Continue with the next iteration or loop test.
  - Set total\_stock\_value from sum(item\_value at tuple(item, item\_group)).
  - Set row from list(item, item\_map at item at “item\_name”, item\_group, itemwise\_brand.get(item), …).
  - Set fifo\_queue from item\_ageing at item at “fifo\_queue”.
  - Set average\_age from 0.0.
  - If fifo\_queue.
    - Set average\_age from get\_average\_age(fifo\_queue, filters at “to\_date”).
  - Update row using + list(average\_age).
  - Set bal\_qty from list of sum(bal\_qty) for bal\_qty drawn from zip(expanded wh\_balance, strict = false).
    - Draw bal\_qty from zip(expanded wh\_balance, strict = false).
  - Set total\_qty from sum(bal\_qty).
  - If len(warehouse\_list) &gt; 1.
    - Update row using + list(total\_qty).
  - Update row using + bal\_qty.
  - If total\_qty differs from 0.
    - Evaluate data.append(row).
  - Otherwise.
    - If not filters.get(“filter\_total\_zero\_qty”).
      - Evaluate data.append(row).
- Evaluate add\_warehouse\_column(columns, warehouse\_list).
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1016) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L591)
