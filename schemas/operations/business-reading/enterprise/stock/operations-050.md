# Inventory and warehouses · operations 50

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Quality inspection template

[Record definition](../../../../data/record-types/quality_inspection_template.json)

<a id="op-6bbd1c013a0058"></a>
### Get template details

`operation_enterprise_stock_record_definitions_quality_inspection_template_business_behavior_get_template_details`

**Inputs** template.

**Record and data access** read “Item Quality Inspection Parameter” via get\_all.

**Explicit results** list() · Platform.get\_all(“Item Quality Inspection Parameter”, fields = list(“specification”, “value”, “acceptance\_formula”, “numeric”, …), filters = mapping(“parenttype” → “Quality Inspection Template”, “parent” → ….

**Local steps**

- If not template.
  - Return list().
- Return Platform.get\_all(“Item Quality Inspection Parameter”, fields = list(“specification”, “value”, “acceptance\_formula”, “numeric”, …), filters = mapping(“parenttype” → “Quality Inspection Template”, “parent” → ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0798.json#L6770) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L398)

## Record · Quick stock balance

[Record definition](../../../../data/record-types/quick_stock_balance.json)

<a id="op-9e5e9eebc179c2"></a>
### Get stock item details

`operation_enterprise_stock_record_definitions_quick_stock_balance_business_behavior_get_stock_item_details`

**Inputs** warehouse, date, item = no value, barcode = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Warehouse” via get\_doc · read “Warehouse” via get\_value · read “Item Barcode” via get\_value · resolve a document from “Item” via get\_doc · read “Item Barcode” via get\_values · 1 additional forms in the steps below.

**Explicit results** out.

**Explicit failure paths** validation helper — translated “Invalid Barcode. There is no Item attached to this barcode.”.

**Local steps**

- If not Platform.has\_permission(“Item”, “read”).
  - Evaluate \_refuse().
- Set warehouse from cstr(warehouse).
- If (not warehouse or not has\_user\_permission(Platform.get\_doc(“Warehouse”, warehouse))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not warehouse → not has\_user\_permission(Platform.get\_doc(“Warehouse”, warehouse)).
  - Evaluate \_refuse().
- If Platform.db.get\_value(“Warehouse”, warehouse, “is\_group”).
  - For each descendant in get\_descendants\_of(“Warehouse”, warehouse, ignore\_permissions = true).
    - Evaluate require\_user\_permission(“Warehouse”, descendant).
- Set out from mapping().
- If barcode.
  - Set out at “item” from Platform.db.get\_value(“Item Barcode”, filters = mapping(“barcode” → barcode), fieldname = list(“parent”)).
  - If not out at “item”.
    - Call the validation error handler Platform.throw(translated “Invalid Barcode. There is no Item attached to this barcode.”).
  - Evaluate require\_user\_permission(“Item”, out at “item”).
- Otherwise.
  - Set item from cstr(item).
  - Set out at “item” from item.
  - If (not item or not has\_user\_permission(Platform.get\_doc(“Item”, item))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item → not has\_user\_permission(Platform.get\_doc(“Item”, item)).
    - Evaluate \_refuse().
- Set barcodes from Platform.db.get\_values(“Item Barcode”, filters = mapping(“parent” → out at “item”), fieldname = list(“barcode”)).
- Set out at “barcodes” from list of x at 0 for x drawn from barcodes.
  - Draw x from barcodes.
- Set out at “qty” from get\_balance\_qty(out at “item”, warehouse, date).
- Set out at “value” from get\_stock\_value\_on(warehouse, date, out at “item”).
- Set out at “image” from Platform.db.get\_value(“Item”, filters = mapping(“name” → out at “item”), fieldname = list(“image”)).
- Return out.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L426)

<a id="op-7643cc11ec43fc"></a>
### Get balance qty

`operation_enterprise_binding_enterprise_stock_doctype_quick_stock_balance_quick_stock_balance_get_balance_qty`

**Inputs** item\_code, warehouse, date.

**Explicit results** flt(result at 0 at 0) when result, otherwise 0.0.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set latest\_first from nested operand in the contract().over(sle.warehouse).orderby(sle.posting\_datetime, order = Order.desc).orderby(sle.creation, order = Order.desc).
- Set ranked from nested operand in the contract(nested operand in the contract).select(sle.qty\_after\_transaction, nested operand in the contract.as\_(“row\_no”)).where((((nested operand in the contract equals nested operand  ….
- Set result from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.qty\_after\_transaction)).where(ranked.row\_no equals 1).run().
- Return flt(result at 0 at 0) when result, otherwise 0.0.
  - Value choice on result — true gives flt(result at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1057) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L554)

<a id="op-d8e5825a0ff12b"></a>
### Get leaf warehouses

`operation_enterprise_binding_enterprise_stock_doctype_quick_stock_balance_quick_stock_balance_get_leaf_warehouses`

**Inputs** warehouse.

**Record and data access** read “Warehouse” via get\_value · read “Warehouse” via get\_all.

**Explicit results** list(warehouse) · (Platform.get\_all(“Warehouse”, filters = mapping(“lft” → tuple(“&gt;”, lft), “rgt” → tuple(“&lt;”, rgt), “is\_group” → 0), pluck = “name”) or list(warehouse)).

**Local steps**

- If not Platform.db.get\_value(“Warehouse”, warehouse, “is\_group”).
  - Return list(warehouse).
- Set tuple(lft, rgt) from Platform.db.get\_value(“Warehouse”, warehouse, list(“lft”, “rgt”)).
- Return (Platform.get\_all(“Warehouse”, filters = mapping(“lft” → tuple(“&gt;”, lft), “rgt” → tuple(“&lt;”, rgt), “is\_group” → 0), pluck = “name”) or list(warehouse)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Warehouse”, filters = mapping(“lft” → tuple(“&gt;”, lft), “rgt” → tuple(“&lt;”, rgt), “is\_group” → 0), pluck = “name”) → list(warehouse).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1058) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L555)

## Service · Reorder item

<a id="op-b33d167c15dd27"></a>
### Reorder item

`operation_enterprise_stock_reorder_item_business_behavior_reorder_item`

**Inputs** no declared parameters.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** no value · \_reorder\_item().

**Local steps**

- If not (Platform.db.a\_row\_exists(“Company”) and Platform.db.a\_row\_exists(“Fiscal Year”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.a\_row\_exists(“Company”) → Platform.db.a\_row\_exists(“Fiscal Year”).
  - Return no value.
- If cint(Platform.db.get\_single\_value(“Stock Settings”, “auto\_indent”)).
  - Return \_reorder\_item().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “auto\_indent”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0884.json#L873) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L51)

<a id="op-6a189471595477"></a>
### Reorder item

`operation_enterprise_stock_reorder_item_business_behavior_reorder_item_2`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Warehouse) · execute query text (SELECT, Company).

**Explicit results** no value · create\_material\_request(material\_requests).

**Local steps**

- Set material\_requests from mapping(“Purchase” → mapping(), “Transfer” → mapping(), “Material Issue” → mapping(), “Manufacture” → mapping()).
- Set warehouse\_company from Platform.\_dict(Platform.db.sql(query text (SELECT, Warehouse))).
- Set default\_company from (Enterprise.get\_default\_company() or Platform.db.sql(query text (SELECT, Company)) at 0 at 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Enterprise.get\_default\_company() → Platform.db.sql(query text (SELECT, Company)) at 0 at 0.
- Set items\_to\_consider from get\_items\_for\_reorder().
- If not items\_to\_consider.
  - Return no value.
- Set item\_warehouse\_projected\_qty from get\_item\_warehouse\_projected\_qty(items\_to\_consider).
- Bind local operation add\_to\_material\_request for subsequent calls.
- For each tuple(item\_code, reorder\_levels) in items\_to\_consider.items().
  - For each d in reorder\_levels.
    - If d.has\_variants.
      - Continue with the next iteration or loop test.
    - Evaluate add\_to\_material\_request(item\_code = item\_code, warehouse = d.warehouse, reorder\_level = d.warehouse\_reorder\_level, reorder\_qty = d.warehouse\_reorder\_qty, …).
- If material\_requests.
  - Return create\_material\_request(material\_requests).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L52)

<a id="op-d63f2f4d94c5a7"></a>
### Reorder item.add to material request

`operation_enterprise_stock_reorder_item_business_behavior_reorder_item_add_to_material_request`

**Inputs** remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- If kwargs.warehouse does not belong to warehouse\_company.
  - Return no value.
- Set reorder\_level from flt(kwargs.reorder\_level).
- Set reorder\_qty from flt(kwargs.reorder\_qty).
- If kwargs.warehouse\_group.
  - Set projected\_qty from flt(item\_warehouse\_projected\_qty.get(kwargs.item\_code, mapping()).get(kwargs.warehouse\_group)).
- Otherwise.
  - Set projected\_qty from flt(item\_warehouse\_projected\_qty.get(kwargs.item\_code, mapping()).get(kwargs.warehouse)).
- Set original\_reorder\_qty from reorder\_qty.
- If ((reorder\_level or reorder\_qty) and projected\_qty ≤ reorder\_level).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (reorder\_level or reorder\_qty) → projected\_qty ≤ reorder\_level.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reorder\_level → reorder\_qty.
  - If (projected\_qty + reorder\_qty) ≤ reorder\_level.
    - Update reorder\_qty using + (reorder\_level − projected\_qty).
  - Set company from (warehouse\_company.get(kwargs.warehouse) or default\_company).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in warehouse\_company.get(kwargs.warehouse) → default\_company.
  - Evaluate material\_requests at kwargs.material\_request\_type.setdefault(company, list()).append(mapping(“item\_code” → kwargs.item\_code, “warehouse” → kwargs.warehouse, “reorder\_qty” → reorder\_qty, “item\_details” → kw ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L53)

<a id="op-fece9674952dc9"></a>
### Get items for reorder

`operation_enterprise_stock_reorder_item_business_behavior_get_items_for_reorder`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, list).

**Explicit results** itemwise\_reorder.

**Local steps**

- Set reorder\_table from Platform.qb.DocType(“Item Reorder”).
- Set item\_table from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(reorder\_table.warehouse, reorder\_table.warehouse\_g ….
- Set data from query.run(as\_dict = true).
- Set itemwise\_reorder from Platform.\_dict(mapping()).
- For each d in data.
  - Evaluate itemwise\_reorder.setdefault(d.name, list()).append(d).
- Set itemwise\_reorder from get\_reorder\_levels\_for\_variants(itemwise\_reorder).
- Return itemwise\_reorder.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L48)

<a id="op-459bd6aec7eb67"></a>
### Get reorder levels for variants

`operation_enterprise_stock_reorder_item_business_behavior_get_reorder_levels_for_variants`

**Inputs** itemwise\_reorder.

**Explicit results** itemwise\_reorder.

**Local steps**

- Set item\_table from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract.qb.from\_(item\_table).select(item\_table.name, item\_table.variant\_of).where((((item\_table.disabled equals 0 bitwise and item\_table.is\_stock\_item equals 1) bitwise and ((nested  ….
- Set variants\_item from query.run(as\_dict = true).
- For each row in variants\_item.
  - If (not itemwise\_reorder.get(row.name) and itemwise\_reorder.get(row.variant\_of)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not itemwise\_reorder.get(row.name) → itemwise\_reorder.get(row.variant\_of).
    - Evaluate itemwise\_reorder.setdefault(row.name, list()).extend(itemwise\_reorder.get(row.variant\_of, list())).
- Return itemwise\_reorder.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L49)

<a id="op-91195a56ab518a"></a>
### Get item warehouse projected qty

`operation_enterprise_stock_reorder_item_business_behavior_get_item_warehouse_projected_quantity`

**Inputs** items\_to\_consider.

**Record and data access** read “Warehouse” via get\_all · execute query text (SELECT, Bin).format(“, ”.join((list(“%s”) × len(items\_to\_consider)))).

**Explicit results** item\_warehouse\_projected\_qty.

**Local steps**

- Set item\_warehouse\_projected\_qty from mapping().
- Set items\_to\_consider from list(items\_to\_consider.keys()).
- Set warehouse\_parent\_map from Platform.\_dict(Platform.get\_all(“Warehouse”, fields = list(“name”, “parent\_warehouse”), as\_list = true)).
- For each tuple(item\_code, warehouse, projected\_qty) in Platform.db.sql(query text (SELECT, Bin).format(“, ”.join((list(“%s”) × len(items\_to\_consider)))), items\_to\_consider).
  - If item\_code does not belong to item\_warehouse\_projected\_qty.
    - Evaluate item\_warehouse\_projected\_qty.setdefault(item\_code, mapping()).
  - If warehouse does not belong to item\_warehouse\_projected\_qty.get(item\_code).
    - Set item\_warehouse\_projected\_qty at item\_code at warehouse from flt(projected\_qty).
  - Set parent\_warehouse from warehouse\_parent\_map.get(warehouse).
  - While parent\_warehouse.
    - If not item\_warehouse\_projected\_qty.get(item\_code, mapping()).get(parent\_warehouse).
      - Set item\_warehouse\_projected\_qty.setdefault(item\_code, mapping()) at parent\_warehouse from flt(projected\_qty).
    - Otherwise.
      - Update item\_warehouse\_projected\_qty at item\_code at parent\_warehouse using + flt(projected\_qty).
    - Set parent\_warehouse from warehouse\_parent\_map.get(parent\_warehouse).
- Return item\_warehouse\_projected\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L47)

<a id="op-4de2f47195b9c0"></a>
### Create material request

`operation_enterprise_stock_reorder_item_business_behavior_create_material_request`

**Inputs** material\_requests.

**Record and data access** read “UOM Conversion Detail” via get\_value · read “UOM” via get\_value · read “Stock Settings” via get\_single\_value.

**State and service calls** request new\_doc for “Material Request” · call insert on mr · call submit on mr.

**Explicit results** mr\_list.

**Local steps**

- Set mr\_list from list().
- Set exceptions\_list from list().
- Set company\_wise\_mr from Platform.\_dict(mapping()).
- For each request\_type in material\_requests.
  - For each company in material\_requests at request\_type.
    - Attempt the following.
      - Set items from material\_requests at request\_type at company.
      - If not items.
        - Continue with the next iteration or loop test.
      - Set mr from Platform.new\_doc(“Material Request”).
      - Evaluate mr.update(mapping(“company” → company, “auto\_created\_via\_reorder” → 1, “transaction\_date” → nowdate(), “material\_request\_type” → “Material Transfer” when request\_type equals “Transfer”, otherwise request\_type)).
        - Value choice on request\_type equals “Transfer” — true gives “Material Transfer”, false gives request\_type.
      - For each d in items.
        - Set d from Platform.\_dict(d).
        - Set item from d.get(“item\_details”).
        - Set uom from item.stock\_uom.
        - Set conversion\_factor from 1.0.
        - If request\_type equals “Purchase”.
          - Set uom from (item.purchase\_uom or item.stock\_uom).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.purchase\_uom → item.stock\_uom.
          - If uom differs from item.stock\_uom.
            - Set conversion\_factor from (Platform.db.get\_value(“UOM Conversion Detail”, mapping(“parent” → item.name, “uom” → uom), “conversion\_factor”) or 1.0).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“UOM Conversion Detail”, mapping(“parent” → item.name, “uom” → uom), “conversion\_factor”) → 1.0.
        - Set must\_be\_whole\_number from Platform.db.get\_value(“UOM”, uom, “must\_be\_whole\_number”, cache = true).
        - Set qty from (d.reorder\_qty ÷ conversion\_factor).
        - If must\_be\_whole\_number.
          - Set qty from ceil(qty).
        - Evaluate mr.append(“items”, mapping(“doctype” → “Material Request Item”, “item\_code” → d.item\_code, “schedule\_date” → add\_days(nowdate(), cint(item.lead\_time\_days)), “qty” → qty, …)).
      - Set schedule\_dates from list of d.schedule\_date for d drawn from mr.items.
        - Draw d from mr.items.
      - Set mr.schedule\_date from max((schedule\_dates or list(nowdate()))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in schedule\_dates → list(nowdate()).
      - Set mr.flags.ignore\_mandatory from true.
      - Evaluate mr.insert().
      - Evaluate mr.submit().
      - Evaluate mr\_list.append(mr).
      - Evaluate company\_wise\_mr.setdefault(company, list()).append(mr).
    - On failure (Exception) bound to exception.
      - Evaluate exceptions\_list.append(exception).
      - Evaluate mr.log\_error(“Unable to create material request”).
- If company\_wise\_mr.
  - If getattr(Platform.local, “reorder\_email\_notify”, no value) is identical to no value.
    - Set Platform.local.reorder\_email\_notify from cint(Platform.db.get\_single\_value(“Stock Settings”, “reorder\_email\_notify”)).
  - If Platform.local.reorder\_email\_notify.
    - Evaluate send\_email\_notification(company\_wise\_mr).
- If exceptions\_list.
  - Evaluate notify\_errors(exceptions\_list).
- Return mr\_list.

**Values supplied outside this operation** clock or generated value from nowdate() · selected callable from getattr(Platform.local, “reorder\_email\_notify”, no value) · configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “reorder\_email\_notify”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L44)

<a id="op-a9b999ba8e2a30"></a>
### Send email notification

`operation_enterprise_stock_reorder_item_business_behavior_send_email_notification`

**Inputs** company\_wise\_mr.

**State and service calls** sendmail.

**Local steps**

- For each tuple(company, mr\_list) in company\_wise\_mr.items().
  - Set email\_list from get\_email\_list(company).
  - If not email\_list.
    - Continue with the next iteration or loop test.
  - Set msg from Platform.render\_template(“templates/emails/reorder\_item.html”, mapping(“mr\_list” → mr\_list)).
  - Evaluate Platform.sendmail(recipients = email\_list, subject = translated “Auto Material Requests Generated”, message = msg).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = email\_list, subject = translated “Auto Material Requests Generated”, message = msg).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0884.json#L6528) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L54)

<a id="op-e5ac8d1b8d80a8"></a>
### Get email list

`operation_enterprise_stock_reorder_item_business_behavior_get_email_list`

**Inputs** company.

**Explicit results** list(set(list of email.email for email drawn from emails)).

**Local steps**

- Set users from get\_comapny\_wise\_users(company).
- Set user\_table from Platform.qb.DocType(“User”).
- Set role\_table from Platform.qb.DocType(“Has Role”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(user\_table.email).where((((nested operand in the c ….
- If users.
  - Set query from query.where(user\_table.name.isin(users)).
- Otherwise.
  - If restricted\_users bound to get\_company\_restricted\_users(company).
    - Set query from query.where(user\_table.name.notin(restricted\_users)).
- Set emails from query.run(as\_dict = true).
- Return list(set(list of email.email for email drawn from emails)).
  - Draw email from emails.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L46)

<a id="op-7de1b76341720b"></a>
### Get comapny wise users

`operation_enterprise_stock_reorder_item_business_behavior_get_comapny_wise_users`

**Inputs** company.

**Record and data access** read “Company” via count · read “User Permission” via get\_all.

**Explicit results** list() · list(set of d.user for d drawn from permissions where (d.for\_value equals company or not d.hide\_descendants)).

**Local steps**

- If Platform.db.count(“Company”) equals 1.
  - Return list().
- Set permissions from Platform.get\_all(“User Permission”, filters = mapping(“allow” → “Company”, “for\_value” → tuple(“in”, list(company, expanded get\_ancestors\_of(“Company”, company)))), or\_filters = mapping(“apply\_to\_all\_docty ….
- Return list(set of d.user for d drawn from permissions where (d.for\_value equals company or not d.hide\_descendants)).
  - Draw d from permissions, keep a combination only if ((d.for\_value equals company or not d.hide\_descendants)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.for\_value equals company → not d.hide\_descendants.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L45)

<a id="op-e83040239dab08"></a>
### Get company restricted users

`operation_enterprise_binding_enterprise_stock_reorder_item_get_company_restricted_users`

**Inputs** company.

**Record and data access** read “Company” via count · read “User Permission” via get\_all.

**Explicit results** list() · list((set of d.user for d drawn from permissions − allowed\_users)).

**Local steps**

- If Platform.db.count(“Company”) equals 1.
  - Return list().
- Set permissions from Platform.get\_all(“User Permission”, filters = mapping(“allow” → “Company”), or\_filters = mapping(“apply\_to\_all\_doctypes” → 1, “applicable\_for” → “Material Request”), fields = list(“user”, “for\_value”, “hid ….
- Set ancestors from set(get\_ancestors\_of(“Company”, company)).
- Set allowed\_users from set of d.user for d drawn from permissions where (d.for\_value equals company or (d.for\_value belongs to ancestors and not d.hide\_descendants)).
  - Draw d from permissions, keep a combination only if ((d.for\_value equals company or (d.for\_value belongs to ancestors and not d.hide\_descendants))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.for\_value equals company → (d.for\_value belongs to ancestors and not d.hide\_descendants).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.for\_value belongs to ancestors → not d.hide\_descendants.
- Return list((set of d.user for d drawn from permissions − allowed\_users)).
  - Draw d from permissions.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L941)

<a id="op-cee31c4d65afeb"></a>
### Notify errors

`operation_enterprise_stock_reorder_item_business_behavior_notify_errors`

**Inputs** exceptions\_list.

**Local steps**

- Set subject from translated “&#91;Important&#93; &#91;Enterprise&#93; Auto Reorder Errors”.
- Set content from (((translated “Dear System Manager,” + text in the contract) + translated “An error occurred for certain Items while creating Material Requests based on Re-order level. Please rectify …”) + text in the contract).
- For each exception in exceptions\_list.
  - Attempt the following.
    - Set error\_message from formatted text &lt;div class='small text-muted'&gt;{escape\_html(str(exception))}&lt;/div&gt;&lt;br&gt;.
    - Update content using + error\_message.
  - On failure (Exception).
    - Evaluate Platform.log\_error(title = “Failed to format auto reorder exception”, message = Platform.get\_traceback()).
- Update content using + ((translated “Regards,” + text in the contract) + translated “Administrator”).
- Bind dependencies sendmail\_to\_system\_managers.
- Evaluate sendmail\_to\_system\_managers(subject, content).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0885.json#L872) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L50)

## Record · Repost item valuation

[Record definition](../../../../data/record-types/repost_item_valuation.json)

<a id="op-a003a96a2082ae"></a>
### Repost Item Valuation.clear old logs

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_clear_old_logs`

**Inputs** days = no value.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Set days from (days or 90).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in days → 90.
- Evaluate clear\_logs\_with\_references(“Repost Item Valuation”, mapping(“creation” → tuple(“&lt;”, add\_days(now(), negative days)), “status” → tuple(“in”, list(“Completed”, “Skipped”)))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L707) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L792) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L450)

<a id="op-ab4402da219b99"></a>
### Repost Item Valuation.on discard

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L890) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L797) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L455)

<a id="op-bf232af2afd8ea"></a>
### Repost Item Valuation.repost now

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_repost_now`

**Inputs** self.

**Local steps**

- Evaluate repost(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L953) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L802) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L460)

<a id="op-c43890924186f8"></a>
### Repost Item Valuation.validate

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_default\_posting\_time().
- Evaluate self.reset\_repost\_only\_accounting\_ledgers().
- Evaluate self.validate\_repost\_only\_accounting\_ledgers().
- Evaluate self.set\_company().
- Evaluate self.validate\_update\_stock().
- Evaluate self.validate\_recalculate\_valuation\_rate().
- Evaluate self.validate\_period\_closing\_voucher().
- Evaluate self.validate\_later\_vouchers\_in\_closed\_period().
- Evaluate self.set\_status(write = false).
- Evaluate self.reset\_field\_values().
- Evaluate self.validate\_accounts\_freeze().
- Evaluate check\_stock\_frozen\_date(self.posting\_date).
- Evaluate self.reset\_recreate\_stock\_ledgers().
- Evaluate self.validate\_recreate\_stock\_ledgers().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default posting time](operations-050.md#op-36bcb4defab990), [reset repost only accounting ledgers](operations-050.md#op-308a36321f46d6), [validate repost only accounting ledgers](operations-050.md#op-73fb59764894e3), [set company](operations-051.md#op-421b54bcf256d0), [validate update stock](operations-050.md#op-b7b95ee50f28cc), [validate recalculate valuation rate](operations-051.md#op-55d2493a171797), [validate period closing voucher](operations-051.md#op-e9dee7e5fbe26c), [validate later vouchers in closed period](operations-051.md#op-03cff34d2b62c4), [set status](operations-051.md#op-5ad04e77ece282), [reset field values](operations-051.md#op-07aac42b27da71), [validate accounts freeze](operations-051.md#op-2aa691f72acfb2), [reset recreate stock ledgers](operations-051.md#op-0a4dee13300a89), [validate recreate stock ledgers](operations-051.md#op-c1ee0185c54918).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L469)

<a id="op-36bcb4defab990"></a>
### Repost Item Valuation.set default posting time

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_set_default_posting_time`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Posting date is required”.

**Local steps**

- If self.posting\_time is identical to no value.
  - Set self.posting\_time from nowtime().
- If not self.posting\_date.
  - Call the validation error handler Platform.throw(translated “Posting date is required”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L1247) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L466)

<a id="op-308a36321f46d6"></a>
### Repost Item Valuation.reset repost only accounting ledgers

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_reset_repost_only_accounting_ledgers`

**Inputs** self.

**Local steps**

- If (self.repost\_only\_accounting\_ledgers and self.based\_on differs from “Transaction”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.repost\_only\_accounting\_ledgers → self.based\_on differs from “Transaction”.
  - Set self.repost\_only\_accounting\_ledgers from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L1386) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L805) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L463)

<a id="op-73fb59764894e3"></a>
### Repost Item Valuation.validate repost only accounting ledgers

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_validate_repost_only_accounting_ledgers`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “GL reposting is not allowed against the voucher type {0}.”.format(Platform.bold(translated “GL Entry”)).

**Local steps**

- If not self.repost\_only\_accounting\_ledgers.
  - Return no value.
- If self.voucher\_type equals “GL Entry”.
  - Call the validation error handler Platform.throw(translated “GL reposting is not allowed against the voucher type {0}.”.format(Platform.bold(translated “GL Entry”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1074) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L571)

<a id="op-b7b95ee50f28cc"></a>
### Repost Item Valuation.validate update stock

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_validate_update_stock`

**Inputs** self.

**Record and data access** read self.voucher\_type via get\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (self.voucher\_type belongs to list(“Sales Invoice”, “Purchase Invoice”) and not self.repost\_only\_accounting\_ledgers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to list(“Sales Invoice”, “Purchase Invoice”) → not self.repost\_only\_accounting\_ledgers.
  - Set update\_stock from Platform.get\_value(self.voucher\_type, self.voucher\_no, “update\_stock”).
  - If not update\_stock.
    - Set msg from translated “Since {0} has 'Update Stock' disabled, you cannot create repost item valuation against it”.format(get\_link\_to\_form(self.voucher\_type, self.voucher\_no)).
    - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L1473) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L473)
