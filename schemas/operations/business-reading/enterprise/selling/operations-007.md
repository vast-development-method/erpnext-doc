# Sales · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Installation note

[Record definition](../../../../data/record-types/installation_note.json)

<a id="op-b3990aa6b00df0"></a>
### Installation Note.on cancel

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.update\_prevdoc\_status().
- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L980) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1810) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1202)

## Report · Item wise sales history

<a id="op-243e97b24faeb1"></a>
### Execute

`operation_enterprise_selling_report_item_wise_sales_history_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart\_data).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Evaluate validate\_date\_range(filters).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Set chart\_data from get\_chart\_data(data).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L19)

<a id="op-f5f1350bb95300"></a>
### Get columns

`operation_enterprise_selling_report_item_wise_sales_history_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Item Code”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldtype” → “Data”, “fieldname” → “item\_n ….

**Local steps**

- Return list(mapping(“label” → translated “Item Code”, “fieldtype” → “Link”, “fieldname” → “item\_code”, “options” → “Item”, …), mapping(“label” → translated “Item Name”, “fieldtype” → “Data”, “fieldname” → “item\_n ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0664.json#L253) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L21)

<a id="op-dc3c8765d36532"></a>
### Get data

`operation_enterprise_selling_report_item_wise_sales_history_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set company from (filters.get(“company”) or get\_default\_company()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company”) → get\_default\_company().
- If not company.
  - Return data.
- Set company\_list from get\_descendants\_of(“Company”, company).
- Evaluate company\_list.append(company).
- Set customer\_details from get\_customer\_details().
- Set item\_details from get\_item\_details().
- Set sales\_order\_records from get\_sales\_order\_details(company\_list, filters).
- For each record in sales\_order\_records.
  - Set customer\_record from customer\_details.get(record.customer).
  - Set item\_record from item\_details.get(record.item\_code).
  - Set row from mapping(“item\_code” → record.get(“item\_code”), “item\_name” → item\_record.get(“item\_name”), “item\_group” → item\_record.get(“item\_group”), “description” → record.get(“description”), …).
  - Set row at “currency” from Platform.get\_cached\_value(“Company”, row at “company”, “default\_currency”).
  - Evaluate data.append(row).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, row at “company”, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L23)

<a id="op-1fefeb00fec918"></a>
### Get customer details

`operation_enterprise_selling_report_item_wise_sales_history_business_behavior_get_customer_details`

**Inputs** no declared parameters.

**Record and data access** read “Customer” via get\_all.

**Explicit results** customer\_details.

**Local steps**

- Set details from Platform.get\_all(“Customer”, fields = list(“name”, “customer\_name”, “customer\_group”)).
- Set customer\_details from mapping().
- For each d in details.
  - Evaluate customer\_details.setdefault(d.name, Platform.\_dict(mapping(“customer\_name” → d.customer\_name, “customer\_group” → d.customer\_group))).
- Return customer\_details.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0664.json#L3365) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L22)

<a id="op-a075b06d602150"></a>
### Get item details

`operation_enterprise_selling_report_item_wise_sales_history_business_behavior_get_item_details`

**Inputs** no declared parameters.

**Record and data access** read “Item” via get\_all.

**Explicit results** item\_details.

**Local steps**

- Set details from Platform.db.get\_all(“Item”, fields = list(“name”, “item\_name”, “item\_group”)).
- Set item\_details from mapping().
- For each d in details.
  - Evaluate item\_details.setdefault(d.name, Platform.\_dict(mapping(“item\_name” → d.item\_name, “item\_group” → d.item\_group))).
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0664.json#L3588) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L24)

<a id="op-1d18f8cfb8e952"></a>
### Get sales order details

`operation_enterprise_selling_report_item_wise_sales_history_business_behavior_get_sales_order_details`

**Inputs** company\_list, filters.

**Explicit results** list() · query.run(as\_dict = 1).

**Local steps**

- Set permitted\_orders from get\_permitted\_sales\_orders(company\_list, filters).
- If not permitted\_orders.
  - Return list().
- Set db\_so from Platform.qb.DocType(“Sales Order”).
- Set db\_so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(db\_so.name, db\_so.customer, db\_so.customer\_group,  ….
- If filters.get(“item\_group”).
  - Set item\_groups from list(expanded get\_descendants\_of(“Item Group”, filters.item\_group), filters.item\_group).
  - Set query from query.where(db\_so\_item.item\_group.isin(item\_groups)).
- If filters.get(“item\_code”).
  - Set query from query.where(db\_so\_item.item\_code equals filters.item\_code).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L25)

<a id="op-0a966050e23c54"></a>
### Get permitted sales orders

`operation_enterprise_binding_enterprise_selling_report_item_wise_sales_history_item_wise_sales_history_get_permitted_sales_orders`

**Inputs** company\_list, filters.

**Explicit results** Platform.qb.get\_query(table = “Sales Order”, fields = list(“name”), filters = so\_filters, ignore\_permissions = false).run(pluck = “name”).

**Local steps**

- Set so\_filters from mapping(“docstatus” → 1, “company” → list(“in”, company\_list)).
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set so\_filters at “transaction\_date” from list(“between”, list(filters.from\_date, filters.to\_date)).
- Otherwise.
  - If filters.get(“from\_date”).
    - Set so\_filters at “transaction\_date” from list(“&gt;=”, filters.from\_date).
  - Otherwise.
    - If filters.get(“to\_date”).
      - Set so\_filters at “transaction\_date” from list(“&lt;=”, filters.to\_date).
- If filters.get(“customer”).
  - Set so\_filters at “customer” from filters.customer.
- Return Platform.qb.get\_query(table = “Sales Order”, fields = list(“name”), filters = so\_filters, ignore\_permissions = false).run(pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L109)

<a id="op-87182bad87dee5"></a>
### Get chart data

`operation_enterprise_selling_report_item_wise_sales_history_business_behavior_get_chart_data`

**Inputs** data.

**Explicit results** mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → translated “Total Sales Amount”, “values” → datapoints at slice no value to 30))), “type” → “bar”, “fi ….

**Local steps**

- Set item\_wise\_sales\_map from mapping().
- Set tuple(labels, datapoints) from tuple(list(), list()).
- For each row in data.
  - Set item\_key from row.get(“item\_code”).
  - If item\_key does not belong to item\_wise\_sales\_map.
    - Set item\_wise\_sales\_map at item\_key from 0.
  - Set item\_wise\_sales\_map at item\_key from (flt(item\_wise\_sales\_map at item\_key) + flt(row.get(“amount”))).
- Set item\_wise\_sales\_map from mapping of item → value for tuple(item, value) drawn from sorted(item\_wise\_sales\_map.items(), key = deferred anonymous expression, reverse = true).
  - Draw tuple(item, value) from sorted(item\_wise\_sales\_map.items(), key = deferred anonymous expression, reverse = true).
- For each key in item\_wise\_sales\_map.
  - Evaluate labels.append(key).
  - Evaluate datapoints.append(item\_wise\_sales\_map at key).
- Return mapping(“data” → mapping(“labels” → labels at slice no value to 30, “datasets” → list(mapping(“name” → translated “Total Sales Amount”, “values” → datapoints at slice no value to 30))), “type” → “bar”, “fi ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0664.json#L4678) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L20)

## Report · Lost quotations

<a id="op-3a506e0b5cf3c1"></a>
### Execute

`operation_enterprise_selling_report_lost_quotations_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(columns, data, no value, no value, …).

**Local steps**

- Set columns from get\_columns(filters.get(“group\_by”)).
- Set tuple(from\_date, to\_date) from get\_timespan\_date\_range(filters.get(“timespan”).lower()).
- Set lost\_quotations from get\_lost\_quotations(filters.get(“company”), from\_date, to\_date).
- Set currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
- Set data from get\_data(lost\_quotations, filters.get(“group\_by”), currency).
- Set report\_summary from get\_report\_summary(lost\_quotations, currency).
- Return tuple(columns, data, no value, no value, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L37)

<a id="op-f87c75fe17438a"></a>
### Get columns

`operation_enterprise_selling_report_lost_quotations_business_behavior_get_columns`

**Inputs** group\_by.

**Explicit results** list(mapping(“fieldname” → “lost\_reason” when group\_by equals “Lost Reason”, otherwise “competitor”, “label” → translated “Lost Reason” when group\_by equals “Lost Reason”, otherwise translated “Competitor” ….

**Local steps**

- Return list(mapping(“fieldname” → “lost\_reason” when group\_by equals “Lost Reason”, otherwise “competitor”, “label” → translated “Lost Reason” when group\_by equals “Lost Reason”, otherwise translated “Competitor” ….
  - Value choice on group\_by equals “Lost Reason” — true gives “lost\_reason”, false gives “competitor”.
  - Value choice on group\_by equals “Lost Reason” — true gives translated “Lost Reason”, false gives translated “Competitor”.
  - Value choice on group\_by equals “Lost Reason” — true gives “Quotation Lost Reason”, false gives “Competitor”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L38)

<a id="op-a5294420ab1add"></a>
### Get lost quotations

`operation_enterprise_binding_enterprise_selling_report_lost_quotations_lost_quotations_get_lost_quotations`

**Inputs** company, from\_date, to\_date.

**Declared result** list at str.

**Record and data access** read “Quotation” via get\_list.

**Explicit results** Platform.get\_list(“Quotation”, filters = mapping(“status” → “Lost”, “docstatus” → DocStatus.submitted(), “company” → company, “transaction\_date” → list(“between”, list(from\_date, to\_date))), pluck = “name” ….

**Local steps**

- Return Platform.get\_list(“Quotation”, filters = mapping(“status” → “Lost”, “docstatus” → DocStatus.submitted(), “company” → company, “transaction\_date” → list(“between”, list(from\_date, to\_date))), pluck = “name” ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L110)

<a id="op-b236bb0e7b4819"></a>
### Get data

`operation_enterprise_selling_report_lost_quotations_business_behavior_get_data`

**Inputs** lost\_quotations, group\_by, currency.

**Explicit results** list() · list of tuple(expanded row, currency) for row drawn from query.run().

**Explicit failure paths** validation helper — translated “Invalid Group By”.

**Local steps**

- If group\_by equals “Lost Reason”.
  - Set fieldname from “lost\_reason”.
  - Set dimension from Platform.qb.DocType(“Quotation Lost Reason Detail”).
- Otherwise.
  - If group\_by equals “Competitor”.
    - Set fieldname from “competitor”.
    - Set dimension from Platform.qb.DocType(“Competitor Detail”).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Invalid Group By”).
- If not lost\_quotations.
  - Return list().
- Set q from Platform.qb.DocType(“Quotation”).
- Set total\_quotations from len(lost\_quotations).
- Set total\_value from nested operand in the contract.qb.from\_(q).where(q.name.isin(lost\_quotations)).select(Sum(q.base\_net\_total)).
- Set pairs from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“quotation”), nested operand in the contract.as\_(“value”), nested operand in the contract.as\_(“reaso ….
- Set reasons\_per\_quotation from nested operand in the contract(nested operand in the contract).select(pairs.quotation, nested operand in the contract.as\_(“reasons”)).groupby(pairs.quotation).as\_(“reasons\_per\_quotation”).
- Set split from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.quotation equals nested operand in the contract.quotation).select(pairs.reason, pairs.quotation, (nested ope ….
- Set query from nested operand in the contract.qb.from\_(split).select(split.reason, Count(nested operand in the contract.quotation).distinct(), Round(((nested operand in the contract() × 100.0) ÷ total\_quotations), 2), Su ….
- Return list of tuple(expanded row, currency) for row drawn from query.run().
  - Draw row from query.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L39)

<a id="op-86953675e9a8e8"></a>
### Get report summary

`operation_enterprise_binding_enterprise_selling_report_lost_quotations_lost_quotations_get_report_summary`

**Inputs** lost\_quotations, currency.

**Explicit results** list(mapping(“label” → translated “Total Lost Quotations”, “value” → len(lost\_quotations), “datatype” → “Int”, “indicator” → “Blue”), mapping(“label” → translated “Total Lost Value”, “value” → total\_value, ….

**Local steps**

- Set total\_value from 0.
- If lost\_quotations.
  - Set q from Platform.qb.DocType(“Quotation”).
  - Set total\_value from (nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).run() at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.base\_net\_total)).run() at 0 at 0 → 0.
- Return list(mapping(“label” → translated “Total Lost Quotations”, “value” → len(lost\_quotations), “datatype” → “Int”, “indicator” → “Blue”), mapping(“label” → translated “Total Lost Value”, “value” → total\_value, ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L111)

## Record · Party specific item

[Record definition](../../../../data/record-types/party_specific_item.json)

<a id="op-fc016b706568ec"></a>
### Party Specific Item.validate

`operation_enterprise_selling_record_definitions_party_specific_item_business_behavior_party_specific_item_validate`

**Inputs** self.

**Record and data access** read “Party Specific Item” via exists.

**Explicit failure paths** validation helper — translated “This item filter has already been applied for the {0}”.format(self.party\_type).

**Local steps**

- Set exists from Platform.db.exists(“Party Specific Item”, mapping(“party\_type” → self.party\_type, “party” → self.party, “restrict\_based\_on” → self.restrict\_based\_on, “based\_on\_value” → self.based\_on\_value, …)).
- If exists.
  - Call the validation error handler Platform.throw(translated “This item filter has already been applied for the {0}”.format(self.party\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1208)

<a id="op-e7eb5b0af16967"></a>
### Get allowed items condition

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_allowed_items_condition`

**Inputs** party\_type, party.

**Explicit results** get\_rules\_condition(rules) when rules, otherwise no value.

**Local steps**

- Set rules from get\_party\_rules(party\_type, party, ignore\_permissions = true).
- Return get\_rules\_condition(rules) when rules, otherwise no value.
  - Value choice on rules — true gives get\_rules\_condition(rules), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1480)

<a id="op-2a11e484d23bf0"></a>
### Get group ancestors

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_group_ancestors`

**Inputs** group\_type, group.

**Explicit results** nested operand in the contract(nested operand in the contract).select(ancestor.name).where(node.name equals group).run(pluck = true).

**Local steps**

- Set node from Platform.qb.DocType(group\_type).
- Set ancestor from Platform.qb.DocType(group\_type).as\_(“ancestor”).
- Return nested operand in the contract(nested operand in the contract).select(ancestor.name).where(node.name equals group).run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1482)

<a id="op-fed6c20ce46eab"></a>
### Get rules condition

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_rules_condition`

**Inputs** rules.

**Explicit results** Criterion.any(conditions).

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- Set values from defaultdict(list).
- For each rule in rules.
  - Evaluate values at rule.restrict\_based\_on.append(rule.based\_on\_value).
- Set conditions from list().
- If values at “Item”.
  - Evaluate conditions.append((item.name.isin(values at “Item”) bitwise or IfNull(item.variant\_of, empty text).isin(values at “Item”))).
- If values at “Item Group”.
  - Evaluate conditions.append(item.item\_group.isin(get\_item\_group\_subtree\_query(values at “Item Group”))).
- If values at “Brand”.
  - Evaluate conditions.append(IfNull(item.brand, empty text).isin(values at “Brand”)).
- Return Criterion.any(conditions).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1489)

<a id="op-9054a9cfa50136"></a>
### Get item group subtree query

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_item_group_subtree_query`

**Inputs** item\_groups.

**Explicit results** nested operand in the contract(nested operand in the contract).on((nested operand in the contract ≥ nested operand in the contract bitwise and nested operand in the contract ≤ nested operand in the contrac ….

**Local steps**

- Set group from Platform.qb.DocType(“Item Group”).
- Set parent from Platform.qb.DocType(“Item Group”).as\_(“parent\_group”).
- Return nested operand in the contract(nested operand in the contract).on((nested operand in the contract ≥ nested operand in the contract bitwise and nested operand in the contract ≤ nested operand in the contrac ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1483)

<a id="op-16fe8b7359fdb1"></a>
### Get frequently ordered items

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_frequently_ordered_items`

**Inputs** party\_type, party.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_list.

**Explicit results** list of mapping(expand row, expand items at row.item\_code) for row drawn from history where row.item\_code belongs to items.

**Local steps**

- Set order\_doctype from validate\_party(party\_type, party).
- Evaluate Platform.has\_permission(order\_doctype, throw = true).
- Set history from get\_order\_history(party\_type, party, limit = 5).
- Set items from mapping of item.name → item for item drawn from Platform.get\_list(“Item”, filters = mapping(“name” → tuple(“in”, (list of nested operand in the contract.item\_code for row drawn from history or list(empty t ….
  - Draw item from Platform.get\_list(“Item”, filters = mapping(“name” → tuple(“in”, (list of row.item\_code for row drawn from history or list(empty text)))), fields = list(“name”, “item\_name”, “disabled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of row.item\_code for row drawn from history → list(empty text).
  - Draw row from history.
- Return list of mapping(expand row, expand items at row.item\_code) for row drawn from history where row.item\_code belongs to items.
  - Draw row from history, keep a combination only if (row.item\_code belongs to items).

**Values supplied outside this operation** effective access from Platform.has\_permission(order\_doctype, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1481)

<a id="op-b826b61f0c2561"></a>
### Party item query

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_party_item_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** list of tuple(item.name, item.item\_name, get\_order\_hint(party\_type, item)) for item drawn from items.

**Local steps**

- Set tuple(party\_type, party) from tuple(filters.get(“party\_type”), filters.get(“party”)).
- Evaluate validate\_party(party\_type, party).
- Set or\_filters from list(list(“Item”, “name”, “like”, formatted text %{txt}%), list(“Item”, “item\_name”, “like”, formatted text %{txt}%)) when txt, otherwise no value.
  - Value choice on txt — true gives list(list(“Item”, “name”, “like”, formatted text %{txt}%), list(“Item”, “item\_name”, “like”, formatted text %{txt}%)), false gives no value.
- Set items from get\_items\_ranked\_by\_orders(party\_type, party, filters = list(list(“Item”, “disabled”, “=”, 0)), or\_filters = or\_filters, fields = list(“name”, “item\_name”), start = start, …).
- Return list of tuple(item.name, item.item\_name, get\_order\_hint(party\_type, item)) for item drawn from items.
  - Draw item from items.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1490)

<a id="op-d54966d78792c0"></a>
### Get party specific items

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_party_specific_items`

**Inputs** party\_type, party.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_list.

**Explicit results** rules.

**Local steps**

- Evaluate validate\_party(party\_type, party).
- Set rules from get\_party\_rules(party\_type, party).
- Set can\_read\_items from Platform.has\_permission(“Item”).
- Set item\_names from mapping().
- If can\_read\_items.
  - Set item\_names from dict(Platform.get\_list(“Item”, filters = mapping(“name” → tuple(“in”, (list of nested operand in the contract.based\_on\_value for r drawn from rules where nested operand in the contract equals nested operand in  …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of r.based\_on\_value for r drawn from rules where r.restrict\_based\_on equals “Item” → list(empty text).
    - Draw r from rules, keep a combination only if (r.restrict\_based\_on equals “Item”).
- Set counts from count\_rule\_items(rules) when can\_read\_items, otherwise mapping().
  - Value choice on can\_read\_items — true gives count\_rule\_items(rules), false gives mapping().
- For each rule in rules.
  - If rule.restrict\_based\_on equals “Item”.
    - Set rule.item\_name from item\_names.get(rule.based\_on\_value).
    - Set rule.item\_count from 1.
  - Otherwise.
    - If can\_read\_items.
      - Set rule.item\_count from counts.get(tuple(rule.restrict\_based\_on, rule.based\_on\_value), 0).
- Evaluate rules.sort(key = deferred anonymous expression).
- For each rule in rules.
  - If rule.party\_type equals party\_type.
    - Evaluate rule.pop(“party\_type”).
    - Evaluate rule.pop(“party”).
- Return rules.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1488)

<a id="op-766927e2ce7ffb"></a>
### Get party rules

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_get_party_rules`

**Inputs** party\_type, party, ignore\_permissions = false.

**Record and data access** read party\_type via get\_value · read “Party Specific Item” via get\_list.

**Explicit results** list of rule for rule drawn from rules where rule.party equals party when rule.party\_type equals party\_type, otherwise rule.party belongs to party\_groups.

**Local steps**

- Set group\_type from formatted text {party\_type} Group.
- Set party\_group from Platform.db.get\_value(party\_type, party, Platform.scrub(group\_type)).
- Set party\_groups from get\_group\_ancestors(group\_type, party\_group) when party\_group, otherwise list().
  - Value choice on party\_group — true gives get\_group\_ancestors(group\_type, party\_group), false gives list().
- Set rules from Platform.get\_list(“Party Specific Item”, filters = mapping(“party\_type” → tuple(“in”, list(party\_type, group\_type))), or\_filters = list(list(“party”, “=”, party), list(“party”, “in”, (party\_groups or list( ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_groups → list(empty text).
- Return list of rule for rule drawn from rules where rule.party equals party when rule.party\_type equals party\_type, otherwise rule.party belongs to party\_groups.
  - Draw rule from rules, keep a combination only if (rule.party equals party when rule.party\_type equals party\_type, otherwise rule.party belongs to party\_groups).
  - Value choice on rule.party\_type equals party\_type — true gives rule.party equals party, false gives rule.party belongs to party\_groups.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1487)

<a id="op-4f711f0fb10a83"></a>
### Validate party

`operation_enterprise_binding_enterprise_selling_doctype_party_specific_item_party_specific_item_validate_party`

**Inputs** party\_type, party.

**Explicit results** ORDER\_DOCTYPES at party\_type.

**Explicit failure paths** validation helper — translated “A customer or supplier is required”.

**Local steps**

- If (party\_type does not belong to ORDER\_DOCTYPES or not party).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_type does not belong to ORDER\_DOCTYPES → not party.
  - Call the validation error handler Platform.throw(translated “A customer or supplier is required”, title = translated “Missing Party”).
- Evaluate Platform.has\_permission(party\_type, doc = party, throw = true).
- Return ORDER\_DOCTYPES at party\_type.

**Values supplied outside this operation** effective access from Platform.has\_permission(party\_type, doc = party, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1491)
