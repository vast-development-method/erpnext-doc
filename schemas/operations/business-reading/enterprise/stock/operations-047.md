# Inventory and warehouses · operations 47

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase receipt

[Record definition](../../../../data/record-types/purchase_receipt.json)

<a id="op-44d0ff22b94e00"></a>
### Get provisional receipt rows

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_provisional_receipt_rows`

**Inputs** company, po\_details.

**Declared result** dict.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** group\_rows\_with\_provisional\_entries(rows).

**Local steps**

- Set pr from Platform.qb.DocType(“Purchase Receipt”).
- Set pr\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set rows from nested operand in the contract(nested operand in the contract).orderby(pr.posting\_time).orderby(pr.creation).run(as\_dict = true).
- Set default\_account from Platform.get\_cached\_value(“Company”, company, “default\_provisional\_account”).
- For each row in rows.
  - Set row.provisional\_expense\_account from (row.provisional\_expense\_account or default\_account).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.provisional\_expense\_account → default\_account.
- Return group\_rows\_with\_provisional\_entries(rows).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_provisional\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L988) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L485)

<a id="op-901d4abd0f8788"></a>
### Group rows with provisional entries

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_group_rows_with_provisional_entries`

**Inputs** rows.

**Declared result** dict.

**Explicit results** mapping() · grouped.

**Local steps**

- If not rows.
  - Return mapping().
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set rows\_with\_entries from set(nested operand in the contract.distinct().where((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract(nested operand in the contract)) bit …).
  - Draw d from rows.
  - Draw d from rows.
- Set grouped from mapping().
- For each row in rows.
  - If row.name belongs to rows\_with\_entries.
    - Evaluate grouped.setdefault(row.purchase\_order\_item, list()).append(row).
- Return grouped.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L999) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L496)

<a id="op-92b31885c06222"></a>
### Get unreversed receipt qty

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_unreversed_receipt_qty`

**Inputs** receipt\_rows, invoice.

**Declared result** dict.

**Explicit results** unreversed\_qty.

**Local steps**

- Set rows from list of row for po\_rows drawn from receipt\_rows.values(), then row drawn from po\_rows.
  - Draw po\_rows from receipt\_rows.values().
  - Draw row from po\_rows.
- Set names from list of d.name for d drawn from rows.
  - Draw d from rows.
- Set billed\_qty from get\_invoiced\_qty(“pr\_detail”, names).
- Set returned\_qty from get\_returned\_receipt\_qty(names).
- For each d in rows.
  - Set d.kept\_qty from ((flt(d.qty) + flt(returned\_qty.get(d.name))) − flt(billed\_qty.get(d.name))).
- Set unreversed\_qty from mapping of d.name → d.kept\_qty for d drawn from rows.
  - Draw d from rows.
- Set order\_billed\_qty from get\_invoiced\_qty(“po\_detail”, list(receipt\_rows), invoice).
- For each tuple(po\_detail, po\_rows) in receipt\_rows.items().
  - Evaluate allocate\_receipt\_rows(po\_rows, unreversed\_qty, flt(order\_billed\_qty.get(po\_detail))).
- Return unreversed\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L998) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L495)

<a id="op-a16d7aeade2c7c"></a>
### Get returned receipt qty

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_returned_receipt_qty`

**Inputs** names.

**Declared result** dict.

**Explicit results** Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(pr\_item.purchase\_receipt\_item).run()).

**Local steps**

- Set pr from Platform.qb.DocType(“Purchase Receipt”).
- Set pr\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Return Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(pr\_item.purchase\_receipt\_item).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L492)

<a id="op-a003b6c415b4d2"></a>
### Get invoiced qty

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_get_invoiced_qty`

**Inputs** fieldname, names, invoice = no value.

**Declared result** dict.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(pi\_item at fieldname, Sum(nested operand in the contract.qty)).where((nested operand in the contract at nested operand in the contract. ….
- If invoice.
  - Set query from query.where((IfNull(pi\_item.pr\_detail, empty text) equals empty text bitwise and pi.name differs from invoice.name)).
- Return Platform.\_dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L476)

<a id="op-6fb8c2fa6d1887"></a>
### Allocate receipt rows

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_allocate_receipt_rows`

**Inputs** rows, unreversed\_qty, qty.

**Declared result** list.

**Explicit results** allocations.

**Local steps**

- Set allocations from list().
- For each row in rows.
  - <a id="op-6fb8c2fa6d1887-guard-4"></a>If qty ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set allocated\_qty from min(qty, unreversed\_qty at row.name).
  - If allocated\_qty &gt; 0.
    - Evaluate allocations.append(tuple(row, allocated\_qty)).
    - Update unreversed\_qty at row.name using − allocated\_qty.
    - Update qty using − allocated\_qty.
- Return allocations.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6fb8c2fa6d1887-guard-4)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L974) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L471)

<a id="op-18bd8c56cc35ed"></a>
### Release receipt rows

`operation_enterprise_binding_enterprise_stock_doctype_purchase_receipt_purchase_receipt_release_receipt_rows`

**Inputs** rows, unreversed\_qty, qty.

**Declared result** list.

**Explicit results** allocations.

**Local steps**

- Set allocations from list().
- For each row in reversed(rows).
  - <a id="op-18bd8c56cc35ed-guard-4"></a>If qty ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set released\_qty from min(qty, (flt(row.kept\_qty) − unreversed\_qty at row.name)).
  - If released\_qty &gt; 0.
    - Evaluate allocations.append(tuple(row, negative released\_qty)).
    - Update unreversed\_qty at row.name using + released\_qty.
    - Update qty using − released\_qty.
- Return allocations.

**Derived branch illustrations**

- At the comparison qty ≤ 0, qty = 0 selects the branch that exits the enclosing loop. With qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-18bd8c56cc35ed-guard-4)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1034) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L531)

<a id="op-491cc4dc435c52"></a>
### Get data

`operation_enterprise_stock_record_definitions_purchase_receipt_purchase_receipt_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “purchase\_receipt\_no”, “non\_standard\_fieldnames” → mapping(“Purchase Invoice” → “purchase\_receipt”, “Asset” → “purchase\_receipt”, “Landed Cost Voucher” → “receipt\_document”, “Auto Rep ….

**Local steps**

- Return mapping(“fieldname” → “purchase\_receipt\_no”, “non\_standard\_fieldnames” → mapping(“Purchase Invoice” → “purchase\_receipt”, “Asset” → “purchase\_receipt”, “Landed Cost Voucher” → “receipt\_document”, “Auto Rep ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0775.json#L3133) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L215)

## Report · Purchase receipt trends

<a id="op-1eaafb5e5819ba"></a>
### Execute

`operation_enterprise_stock_report_purchase_receipt_trends_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(conditions at “columns”, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set data from list().
- Set conditions from get\_columns(filters, “Purchase Receipt”).
- Set data from get\_data(filters, conditions).
- Set chart\_data from get\_chart\_data(data, conditions, filters).
- Return tuple(conditions at “columns”, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0899.json#L5739) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L252)

<a id="op-3ad82b03f929e7"></a>
### Get chart data

`operation_enterprise_stock_report_purchase_receipt_trends_business_behavior_get_chart_data`

**Inputs** data, conditions, filters.

**Explicit results** list() · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Total Received Amount”, “values” → datapoints))), “type” → “bar”, “colors” → list(“#5e64ff”), “fieldtype” → “Currency”, …).

**Local steps**

- Bind local operation wrap\_in\_quotes for subsequent calls.
- If not data.
  - Return list().
- Set tuple(labels, datapoints) from tuple(list(), list()).
- If filters.get(“group\_by”).
  - Set data from list of row for row drawn from data where row at 0.
    - Draw row from data, keep a combination only if (row at 0).
- Set data from sorted(data, key = deferred anonymous expression, reverse = true).
- If len(data) &gt; 10.
  - Set data from data at slice no value to 10.
- For each row in data.
  - If row at 0 equals wrap\_in\_quotes(translated “Total”).
    - Continue with the next iteration or loop test.
  - Evaluate labels.append(row at 0).
  - Evaluate datapoints.append(row at negative 1).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Total Received Amount”, “values” → datapoints))), “type” → “bar”, “colors” → list(“#5e64ff”), “fieldtype” → “Currency”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0899.json#L5950) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L253)

<a id="op-3f782f06e9b095"></a>
### Get chart data.wrap in quotes

`operation_enterprise_stock_report_purchase_receipt_trends_business_behavior_get_chart_data_wrap_in_quotes`

**Inputs** label.

**Explicit results** formatted text '{label}'.

**Local steps**

- Return formatted text '{label}'.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0899.json#L6629) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L254)

## Record · Putaway rule

[Record definition](../../../../data/record-types/putaway_rule.json)

<a id="op-ff91c929da0fed"></a>
### Putaway Rule.validate

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_putaway_rule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_rule().
- Evaluate self.validate\_warehouse\_and\_company().
- Evaluate self.set\_stock\_capacity().
- Evaluate self.validate\_capacity().
- Evaluate self.validate\_priority().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate rule](operations-047.md#op-503abd16d5271e), [validate warehouse and company](operations-047.md#op-a38c91c0f8b6c6), [set stock capacity](operations-047.md#op-f3898f27a15a33), [validate capacity](operations-047.md#op-d8ba647240a011), [validate priority](operations-047.md#op-ad4dbf1fcf4a3f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L348)

<a id="op-503abd16d5271e"></a>
### Putaway Rule.validate duplicate rule

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_putaway_rule_validate_duplicate_rule`

**Inputs** self.

**Record and data access** read “Putaway Rule” via exists.

**Explicit failure paths** validation helper — translated “Putaway Rule already exists for Item {0} in Warehouse {1}.”.format(Platform.bold(self.item\_code), Platform.bold(self.warehouse)).

**Local steps**

- Set existing\_rule from Platform.db.exists(“Putaway Rule”, mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse)).
- If (existing\_rule and existing\_rule differs from self.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing\_rule → existing\_rule differs from self.name.
  - Call the validation error handler Platform.throw(translated “Putaway Rule already exists for Item {0} in Warehouse {1}.”.format(Platform.bold(self.item\_code), Platform.bold(self.warehouse)), title = translated “Duplicate”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0793.json#L6611) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L350)

<a id="op-ad4dbf1fcf4a3f"></a>
### Putaway Rule.validate priority

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_putaway_rule_validate_priority`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Priority cannot be lesser than 1.”.

**Local steps**

- <a id="op-ad4dbf1fcf4a3f-guard-2"></a>If self.priority &lt; 1.
  - Call the validation error handler Platform.throw(translated “Priority cannot be lesser than 1.”, title = translated “Invalid Priority”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.priority &lt; 1, self.priority = 0 selects the branch that calls the validation-error handler with translated “Priority cannot be lesser than 1.”. With self.priority = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ad4dbf1fcf4a3f-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L351)

<a id="op-a38c91c0f8b6c6"></a>
### Putaway Rule.validate warehouse and company

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_putaway_rule_validate_warehouse_and_company`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value · read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Warehouse {0} must be an enabled warehouse that is not a group.”.format(Platform.bold(self.warehouse)) · validation helper — translated “Item {0} is not a stock item.”.format(Platform.bold(self.item\_code)) · validation helper — translated “Warehouse {0} does not belong to Company {1}.”.format(Platform.bold(self.warehouse), Platform.bold(self.company)).

**Local steps**

- Set tuple(company, is\_group, disabled) from Platform.db.get\_value(“Warehouse”, self.warehouse, list(“company”, “is\_group”, “disabled”)).
- If ((is\_group or disabled) and not self.disable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (is\_group or disabled) → not self.disable.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_group → disabled.
  - Call the validation error handler Platform.throw(translated “Warehouse {0} must be an enabled warehouse that is not a group.”.format(Platform.bold(self.warehouse)), title = translated “Invalid Warehouse”).
- If (not self.disable and not Platform.get\_cached\_value(“Item”, self.item\_code, “is\_stock\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.disable → not Platform.get\_cached\_value(“Item”, self.item\_code, “is\_stock\_item”).
  - Call the validation error handler Platform.throw(translated “Item {0} is not a stock item.”.format(Platform.bold(self.item\_code))).
- If company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Warehouse {0} does not belong to Company {1}.”.format(Platform.bold(self.warehouse), Platform.bold(self.company)), title = translated “Invalid Warehouse”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L352)

<a id="op-d8ba647240a011"></a>
### Putaway Rule.validate capacity

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_putaway_rule_validate_capacity`

**Inputs** self.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Warehouse Capacity for Item '{0}' must be greater than the existing stock level of {1} {2}.”.format(self.item\_code, Platform.bold(balance\_qty), stock\_uom) · validation helper — translated “Capacity must be greater than 0”.

**Local steps**

- Set stock\_uom from Platform.db.get\_value(“Item”, self.item\_code, “stock\_uom”).
- Set balance\_qty from \_get\_stock\_balance(self.item\_code, self.warehouse, nowdate()).
- If flt(self.stock\_capacity) &lt; flt(balance\_qty).
  - Call the validation error handler Platform.throw(translated “Warehouse Capacity for Item '{0}' must be greater than the existing stock level of {1} {2}.”.format(self.item\_code, Platform.bold(balance\_qty), stock\_uom), title = translated “In ….
- If not self.capacity.
  - Call the validation error handler Platform.throw(translated “Capacity must be greater than 0”, title = translated “Invalid”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L349)

<a id="op-f3898f27a15a33"></a>
### Putaway Rule.set stock capacity

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_putaway_rule_set_stock_capacity`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- Set self.stock\_uom from Platform.get\_cached\_value(“Item”, self.item\_code, “stock\_uom”).
- Set self.uom from (self.uom or self.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.uom → self.stock\_uom.
- Set self.conversion\_factor from (get\_conversion\_factor(self.item\_code, self.uom).get(“conversion\_factor”) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_conversion\_factor(self.item\_code, self.uom).get(“conversion\_factor”) → 1.
- Set self.stock\_capacity from (flt(self.conversion\_factor) × flt(self.capacity)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L347)

<a id="op-0444a13131b25a"></a>
### Get available putaway capacity

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_get_available_putaway_capacity`

**Inputs** rule.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_available\_putaway\_capacity(rule).

**Local steps**

- Evaluate Platform.has\_permission(“Putaway Rule”, “read”, doc = rule, throw = true).
- Return \_get\_available\_putaway\_capacity(rule).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Putaway Rule”, “read”, doc = rule, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L343)

<a id="op-d3e54ed0476347"></a>
### Get available putaway capacity

`operation_enterprise_binding_enterprise_stock_doctype_putaway_rule_putaway_rule_get_available_putaway_capacity`

**Inputs** rule.

**Record and data access** read “Putaway Rule” via get\_value.

**Explicit results** free\_space when free\_space &gt; 0, otherwise 0.

**Local steps**

- Set tuple(stock\_capacity, item\_code, warehouse) from Platform.db.get\_value(“Putaway Rule”, rule, list(“stock\_capacity”, “item\_code”, “warehouse”)).
- Set balance\_qty from \_get\_stock\_balance(item\_code, warehouse, nowdate()).
- Set free\_space from (flt(stock\_capacity) − flt(balance\_qty)).
- Return free\_space when free\_space &gt; 0, otherwise 0.
  - Value choice on free\_space &gt; 0 — true gives free\_space, false gives 0.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1039) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L536)

<a id="op-136aefa848602c"></a>
### Apply putaway rule

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_apply_putaway_rule`

**Inputs** doctype, items, company, sync = no value, purpose = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Serial and Batch Bundle” via get\_list.

**Explicit results** no value · \_apply\_putaway\_rule(doctype, items, company, sync, …).

**Local steps**

- If doctype does not belong to tuple(“Purchase Receipt”, “Stock Entry”).
  - Evaluate \_refuse().
- Evaluate Platform.has\_permission(doctype, “write”, throw = true).
- Set allowed\_companies from get\_allowed\_docs\_for\_doctype(get\_user\_permissions(Platform.session.user).get(“Company”, list()), doctype).
- If (allowed\_companies and company does not belong to allowed\_companies).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_companies → company does not belong to allowed\_companies.
  - Evaluate \_refuse().
- If not Platform.has\_permission(“Item”, “read”).
  - Return no value.
- Set items from Platform.parse\_json(items).
- Set bundles from set of item.get(“serial\_and\_batch\_bundle”) for item drawn from items where item.get(“serial\_and\_batch\_bundle”).
  - Draw item from items, keep a combination only if (item.get(“serial\_and\_batch\_bundle”)).
- If bundles.
  - Set readable from Platform.get\_list(“Serial and Batch Bundle”, filters = mapping(“name” → tuple(“in”, list(bundles))), pluck = “name”, limit\_page\_length = 0).
  - If len(readable) &lt; len(bundles).
    - Evaluate \_refuse().
- Return \_apply\_putaway\_rule(doctype, items, company, sync, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “write”, throw = true), get\_user\_permissions(Platform.session.user) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L342)

<a id="op-4adde0a41d4d6f"></a>
### Get row conversion factor

`operation_enterprise_binding_enterprise_stock_doctype_putaway_rule_putaway_rule_get_row_conversion_factor`

**Inputs** item.

**Explicit results** (flt(get\_conversion\_factor(item.item\_code, item.uom).get(“conversion\_factor”)) or 1.0) · 1.0.

**Local steps**

- If (item.uom and item.item\_code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.uom → item.item\_code.
  - Return (flt(get\_conversion\_factor(item.item\_code, item.uom).get(“conversion\_factor”)) or 1.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(get\_conversion\_factor(item.item\_code, item.uom).get(“conversion\_factor”)) → 1.0.
- Return 1.0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1041) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L538)

<a id="op-d5e50fd475a686"></a>
### Apply putaway rule

`operation_enterprise_binding_enterprise_stock_doctype_putaway_rule_putaway_rule_apply_putaway_rule`

**Inputs** doctype, items, company, sync = no value, purpose = no value.

**Record and data access** read “UOM” via get\_cached\_value.

**State and service calls** msgprint with translated “Applied putaway rules.”.

**Explicit results** items.

**Local steps**

- If isinstance(items, str).
  - Set items from json.loads(items).
- Set sync from bool((sync and Platform.parse\_json(sync))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sync → Platform.parse\_json(sync).
- Set tuple(items\_not\_accomodated, updated\_table) from tuple(list(), list()).
- Set item\_wise\_rules from mapping().
- For each item in items.
  - If isinstance(item, dict).
    - Set item from Platform.\_dict(item).
  - Set source\_warehouse from item.get(“s\_warehouse”).
  - Set serial\_nos from list().
  - If item.get(“serial\_no”).
    - Set serial\_nos from get\_serial\_nos(item.get(“serial\_no”)).
  - Set item.conversion\_factor from (flt(item.conversion\_factor) or get\_row\_conversion\_factor(item)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.conversion\_factor) → get\_row\_conversion\_factor(item).
  - Set tuple(pending\_qty, item\_code) from tuple(flt(item.qty), item.item\_code).
  - Set pending\_stock\_qty from (pending\_qty × item.conversion\_factor).
  - Set uom\_must\_be\_whole\_number from Platform.get\_cached\_value(“UOM”, item.uom, “must\_be\_whole\_number”).
  - If (not pending\_qty or not item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not pending\_qty → not item\_code.
    - Set updated\_table from add\_row(item, pending\_qty, (source\_warehouse or item.warehouse), updated\_table, serial\_nos = serial\_nos, keep\_rejected = true).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_warehouse → item.warehouse.
    - Continue with the next iteration or loop test.
  - If item\_code does not belong to item\_wise\_rules.
    - Set item\_wise\_rules at item\_code from get\_item\_putaway\_rules(item\_code, company).
  - Set tuple(at\_capacity, rules) from select\_vacant\_rules(item\_wise\_rules at item\_code, source\_warehouse).
  - If not rules.
    - Set warehouse from (source\_warehouse or item.get(“warehouse”)) when not item.get(“t\_warehouse”), otherwise item.get(“t\_warehouse”).
      - Value choice on not item.get(“t\_warehouse”) — true gives (source\_warehouse or item.get(“warehouse”)), false gives item.get(“t\_warehouse”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_warehouse → item.get(“warehouse”).
    - If at\_capacity.
      - Evaluate items\_not\_accomodated.append(list(item\_code, pending\_qty)).
    - Otherwise.
      - Set updated\_table from add\_row(item, pending\_qty, warehouse, updated\_table, serial\_nos = serial\_nos, keep\_rejected = true).
    - Continue with the next iteration or loop test.
  - Set keep\_rejected from true.
  - For each rule in rules.
    - If (pending\_stock\_qty &gt; 0 and rule.free\_space).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pending\_stock\_qty &gt; 0 → rule.free\_space.
      - Set stock\_qty\_to\_allocate from flt(rule.free\_space) when pending\_stock\_qty ≥ flt(rule.free\_space), otherwise pending\_stock\_qty.
        - Value choice on pending\_stock\_qty ≥ flt(rule.free\_space) — true gives flt(rule.free\_space), false gives pending\_stock\_qty.
      - Set qty\_to\_allocate from (stock\_qty\_to\_allocate ÷ item.conversion\_factor).
      - If uom\_must\_be\_whole\_number.
        - Set qty\_to\_allocate from floor(qty\_to\_allocate).
        - Set stock\_qty\_to\_allocate from (qty\_to\_allocate × item.conversion\_factor).
      - If not qty\_to\_allocate.
        - Continue with the next iteration or loop test.
      - Set updated\_table from add\_row(item, qty\_to\_allocate, rule.warehouse, updated\_table, serial\_nos = serial\_nos, keep\_rejected = keep\_rejected, …).
      - Set keep\_rejected from false.
      - Update pending\_stock\_qty using − stock\_qty\_to\_allocate.
      - Update pending\_qty using − qty\_to\_allocate.
      - Update rule at “free\_space” using − stock\_qty\_to\_allocate.
      - <a id="op-d5e50fd475a686-guard-99"></a>If pending\_stock\_qty ≤ 0.
        - Leave the innermost loop without its normal-exhaustion alternative.
  - If pending\_stock\_qty &gt; 0.
    - Evaluate items\_not\_accomodated.append(list(item.item\_code, pending\_qty)).
- If items\_not\_accomodated.
  - Evaluate show\_unassigned\_items\_message(items\_not\_accomodated).
- If (updated\_table and \_items\_changed(items, updated\_table, doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in updated\_table → \_items\_changed(items, updated\_table, doctype).
  - Evaluate \_split\_bundles(updated\_table, doctype, keep\_original = not sync).
  - Set items at slice no value to no value from updated\_table.
  - Evaluate Platform.msgprint(translated “Applied putaway rules.”, alert = true).
- If sync.
  - Return items.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison pending\_stock\_qty ≤ 0, pending\_stock\_qty = 0 selects the branch that exits the enclosing loop. With pending\_stock\_qty = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d5e50fd475a686-guard-99)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“UOM”, item.uom, “must\_be\_whole\_number”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1038) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L535)

<a id="op-b9ec1cae15e13a"></a>
### Items changed

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_items_changed`

**Inputs** old, new, doctype.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- If len(old) differs from len(new).
  - Return true.
- Set old from list of Platform.\_dict(item) when isinstance(item, dict), otherwise item for item drawn from old.
  - Draw item from old.
  - Value choice on isinstance(item, dict) — true gives Platform.\_dict(item), false gives item.
- If doctype equals “Stock Entry”.
  - Set compare\_keys from tuple(“item\_code”, “t\_warehouse”, “transfer\_qty”, “serial\_no”).
  - Set sort\_key from deferred anonymous expression.
- Otherwise.
  - Set compare\_keys from tuple(“item\_code”, “warehouse”, “stock\_qty”, “received\_qty”, …).
  - Set sort\_key from deferred anonymous expression.
- Set old\_sorted from sorted(old, key = sort\_key).
- Set new\_sorted from sorted(new, key = sort\_key).
- For each tuple(old\_item, new\_item) in zip(old\_sorted, new\_sorted, strict = false).
  - For each key in compare\_keys.
    - If old\_item.get(key) differs from new\_item.get(key).
      - Return true.
- Return false.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0794.json#L2458) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L346)

<a id="op-bb38b451d47250"></a>
### Get ordered putaway rules

`operation_enterprise_stock_record_definitions_putaway_rule_business_behavior_get_ordered_putaway_rules`

**Inputs** item\_code, company, source\_warehouse = no value.

**Explicit results** select\_vacant\_rules(get\_item\_putaway\_rules(item\_code, company), source\_warehouse).

**Local steps**

- Return select\_vacant\_rules(get\_item\_putaway\_rules(item\_code, company), source\_warehouse).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L344)
