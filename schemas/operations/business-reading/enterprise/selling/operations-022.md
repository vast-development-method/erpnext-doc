# Sales · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Sales partner target variance based on item group

<a id="op-f958c84076861a"></a>
### Get sales user map

`operation_enterprise_binding_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_get_sales_user_map`

**Inputs** partner\_doctype, sales\_users.

**Record and data access** read partner\_doctype via get\_all.

**Explicit results** mapping of name → set(name) for name drawn from sales\_users · mapping of name → set of node.name for node drawn from nodes where by\_name at name.lft ≤ node.lft ≤ by\_name at name.rgt for name drawn from sales\_users where name belongs to by\_name.

**Local steps**

- If partner\_doctype does not belong to tuple(“Territory”, “Sales Person”).
  - Return mapping of name → set(name) for name drawn from sales\_users.
    - Draw name from sales\_users.
- Set nodes from Platform.get\_all(partner\_doctype, fields = list(“name”, “lft”, “rgt”)).
- Set by\_name from mapping of node.name → node for node drawn from nodes.
  - Draw node from nodes.
- Return mapping of name → set of node.name for node drawn from nodes where by\_name at name.lft ≤ node.lft ≤ by\_name at name.rgt for name drawn from sales\_users where name belongs to by\_name.
  - Draw name from sales\_users, keep a combination only if (name belongs to by\_name).
  - Draw node from nodes, keep a combination only if (by\_name at name.lft ≤ node.lft ≤ by\_name at name.rgt).
  - Compare adjacent operands in order, stopping at the first false comparison in by\_name at name.lft ≤ node.lft ≤ by\_name at name.rgt.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L136)

<a id="op-eb685b415acc2f"></a>
### Get columns

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_business_behavior_get_columns`

**Inputs** filters, period\_list, partner\_doctype.

**Explicit results** columns.

**Local steps**

- Set tuple(fieldtype, options) from tuple(“Currency”, “currency”).
- If filters.get(“target\_on”) equals “Quantity”.
  - Set tuple(fieldtype, options) from tuple(“Float”, empty text).
- Set columns from list(mapping(“fieldname” → Platform.scrub(partner\_doctype), “label” → translated partner\_doctype, “fieldtype” → “Link”, “options” → partner\_doctype, …), mapping(“fieldname” → “item\_group”, “label” → transl ….
- For each period in period\_list.
  - Set target\_key from formatted text target\_{period.key}.
  - Set variance\_key from formatted text variance\_{period.key}.
  - Evaluate columns.extend(list(mapping(“fieldname” → target\_key, “label” → translated “Target ({})”.format(period.label), “fieldtype” → fieldtype, “options” → options, …), mapping(“fieldname” → period.key, “label” →  ….
- Evaluate columns.extend(list(mapping(“fieldname” → “total\_target”, “label” → translated “Total Target”, “fieldtype” → fieldtype, “options” → options, …), mapping(“fieldname” → “total\_achieved”, “label” → translated ….
- Return columns.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0676.json#L2064) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L176)

<a id="op-191d5cc9ee4b00"></a>
### Prepare data

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_business_behavior_prepare_data`

**Inputs** filters, sales\_users\_data, sales\_user\_wise\_item\_groups, actual\_data, date\_field, period\_list, sales\_field, sales\_user\_map = no value.

**Explicit results** rows.

**Local steps**

- Set rows from mapping().
- Set target\_qty\_amt\_field from “target\_qty” when filters.get(“target\_on”) equals “Quantity”, otherwise “target\_amount”.
  - Value choice on filters.get(“target\_on”) equals “Quantity” — true gives “target\_qty”, false gives “target\_amount”.
- Set qty\_or\_amount\_field from “stock\_qty” when filters.get(“target\_on”) equals “Quantity”, otherwise “base\_net\_amount”.
  - Value choice on filters.get(“target\_on”) equals “Quantity” — true gives “stock\_qty”, false gives “base\_net\_amount”.
- Set item\_group\_parent\_child\_map from get\_item\_group\_parent\_child\_map().
- For each d in sales\_users\_data.
  - Set key from tuple(d.parent, (d.item\_group or no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.item\_group → no value.
  - Set dist\_data from get\_periodwise\_distribution\_data(d.distribution\_id, period\_list, filters.get(“period”)).
  - Set details from rows.setdefault(key, mapping(“total\_target” → 0, “total\_achieved” → 0)).
  - For each period in period\_list.
    - Set target\_key from formatted text target\_{period.key}.
    - Set target from ((d.get(target\_qty\_amt\_field) × dist\_data.get(period.key)) ÷ 100).
    - Set details at target\_key from (details.get(target\_key, 0) + target).
    - Update details at “total\_target” using + target.
- For each tuple(tuple(parent, item\_group), details) in rows.items().
  - For each period in period\_list.
    - Set p\_key from period.key.
    - Set details at p\_key from sum(generator of r.get(qty\_or\_amount\_field, 0) for r drawn from actual\_data where (r.get(sales\_field) belongs to (nested operand in the contract or nested operand in the contract).get(parent, set(parent)) and  …).
      - Draw r from actual\_data, keep a combination only if ((r.get(sales\_field) belongs to (sales\_user\_map or mapping()).get(parent, set(parent)) and period.from\_date ≤ r.get(date\_field) ≤ period.to\_date and (not item\_group or r.item\_group equals item\_group or r.it …).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in r.get(sales\_field) belongs to (sales\_user\_map or mapping()).get(parent, set(parent)) → period.from\_date ≤ r.get(date\_field) ≤ period.to\_date → (not item\_group or r.item\_group equals item\_group or r.item\_group belongs to item\_group\_parent\_child\_map.get(item\_group, list())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in sales\_user\_map → mapping().
      - Compare adjacent operands in order, stopping at the first false comparison in period.from\_date ≤ r.get(date\_field) ≤ period.to\_date.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item\_group → r.item\_group equals item\_group → r.item\_group belongs to item\_group\_parent\_child\_map.get(item\_group, list()).
    - Set details at formatted text variance\_{p\_key} from (details at p\_key − details at formatted text target\_{p\_key}).
    - Update details at “total\_achieved” using + details at p\_key.
  - Set details at “total\_variance” from (details at “total\_achieved” − details at “total\_target”).
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L181)

<a id="op-4310f4d2d0f848"></a>
### Get item group parent child map

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_business_behavior_get_item_group_parent_child_map`

**Inputs** no declared parameters.

**Record and data access** read “Item Group” via get\_all.

**Explicit results** item\_group\_parent\_child\_map.

**Local steps**

- Set item\_groups from Platform.get\_all(“Item Group”, fields = list(“name”, “parent\_item\_group”), order\_by = “lft desc, rgt desc”).
- Set item\_group\_parent\_child\_map from mapping().
- For each item\_group in item\_groups.
  - Set children from item\_group\_parent\_child\_map.get(item\_group.name, list()).
  - If not children.
    - Set children from list(item\_group.name).
  - Evaluate item\_group\_parent\_child\_map.setdefault(item\_group.parent\_item\_group, list()).extend(children).
- Return item\_group\_parent\_child\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0676.json#L4430) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L179)

<a id="op-3dbf4d93413cf1"></a>
### Get actual data

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_business_behavior_get_actual_data`

**Inputs** filters, sales\_users\_or\_territory\_data, date\_field, sales\_field.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set fiscal\_year from get\_fiscal\_year(fiscal\_year = filters.get(“fiscal\_year”), as\_dict = 1).
- Set doctype from filters.get(“doctype”).
- Set doc\_filters from mapping(“docstatus” → 1, date\_field → list(“between”, list(fiscal\_year.year\_start\_date, fiscal\_year.year\_end\_date))).
- If filters.get(“company”).
  - Set doc\_filters at “company” from filters.company.
- Set permitted\_docs from Platform.qb.get\_query(table = doctype, fields = list(“name”), filters = doc\_filters, ignore\_permissions = false).
- Set parent\_doc from Platform.qb.DocType(doctype).
- Set child\_doc from Platform.qb.DocType((doctype + “ Item”)).
- Set query from nested operand in the contract.qb.from\_(parent\_doc).inner\_join(child\_doc).on(child\_doc.parent equals parent\_doc.name).
- If sales\_field equals “sales\_person”.
  - Set sales\_team from Platform.qb.DocType(“Sales Team”).
  - Set stock\_qty from ((child\_doc.stock\_qty × sales\_team.allocated\_percentage) ÷ 100).
  - Set net\_amount from ((child\_doc.base\_net\_amount × sales\_team.allocated\_percentage) ÷ 100).
  - Set sales\_field\_col from sales\_team at sales\_field.
  - Set query from query.inner\_join(sales\_team).on((sales\_team.parent equals parent\_doc.name bitwise and sales\_team.parenttype equals doctype)).
- Otherwise.
  - Set stock\_qty from child\_doc.stock\_qty.
  - Set net\_amount from child\_doc.base\_net\_amount.
  - Set sales\_field\_col from parent\_doc at sales\_field.
- Set query from query.select(child\_doc.item\_group, parent\_doc at date\_field, stock\_qty.as\_(“stock\_qty”), net\_amount.as\_(“base\_net\_amount”), …).where((parent\_doc.name.isin(permitted\_docs) bitwise and sales\_field\_col.isin(s ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L175)

<a id="op-ab852a6b801510"></a>
### Get parents data

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_item_group_wise_sales_target_variance_business_behavior_get_parents_data`

**Inputs** filters, partner\_doctype.

**Record and data access** read “Target Detail” via get\_all.

**Explicit results** Platform.get\_all(“Target Detail”, filters = filters\_dict, fields = list(“parent”, “item\_group”, target\_qty\_amt\_field, “fiscal\_year”, …)).

**Local steps**

- Set filters\_dict from mapping(“parenttype” → partner\_doctype).
- Set target\_qty\_amt\_field from “target\_qty” when filters.get(“target\_on”) equals “Quantity”, otherwise “target\_amount”.
  - Value choice on filters.get(“target\_on”) equals “Quantity” — true gives “target\_qty”, false gives “target\_amount”.
- If filters.get(“fiscal\_year”).
  - Set filters\_dict at “fiscal\_year” from filters.get(“fiscal\_year”).
- Return Platform.get\_all(“Target Detail”, filters = filters\_dict, fields = list(“parent”, “item\_group”, target\_qty\_amt\_field, “fiscal\_year”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0676.json#L5512) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L180)

<a id="op-3aa83e6bd1cc97"></a>
### Execute

`operation_enterprise_selling_report_sales_partner_target_variance_based_on_item_group_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** get\_data\_column(filters, “Sales Partner”).

**Local steps**

- Return get\_data\_column(filters, “Sales Partner”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0676.json#L5808) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L174)

## Report · Sales partner transaction summary

<a id="op-20a447ad468733"></a>
### Execute

`operation_enterprise_selling_report_sales_partner_transaction_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** SalesPartnerTransactionSummaryReport(filters = filters).run().

**Local steps**

- If not filters.
  - Set filters from mapping().
- Return SalesPartnerTransactionSummaryReport(filters = filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0676.json#L6441) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L184)

<a id="op-26758302efdce3"></a>
### Sales Partner Transaction Summary Report.prepare columns

`operation_enterprise_selling_report_sales_partner_transaction_summary_business_behavior_sales_partner_transaction_summary_report_prepare_columns`

**Inputs** self.

**Local steps**

- Evaluate self.make\_column(translated self.filters.get(“doctype”), “name”, “Link”, options = self.filters.get(“doctype”)).
- Evaluate self.make\_column(translated “Customer”, “customer”, “Link”, options = “Customer”).
- Evaluate self.make\_column(translated “Currency”, “currency”, “Data”, 80, hidden = 1).
- Evaluate self.make\_column(translated “Territory”, “territory”, “Link”, 100, …).
- Evaluate self.make\_column(self.date\_label, “posting\_date”, “Date”).
- Evaluate self.make\_column(translated “Item Code”, “item\_code”, “Link”, 100, …).
- Evaluate self.make\_column(translated “Item Group”, “item\_group”, “Link”, 100, …).
- Evaluate self.make\_column(translated “Brand”, “brand”, “Link”, 100, …).
- Evaluate self.make\_column(translated “Quantity”, “qty”, “Float”, 120).
- Evaluate self.make\_column(translated “Rate”, “rate”, “Currency”, 120, …).
- Evaluate self.make\_column(translated “Amount”, “amount”, “Currency”, 120, …).
- Evaluate self.make\_column(translated “Sales Partner”, “sales\_partner”, “Link”, options = “Sales Partner”).
- Evaluate self.make\_column(translated “Commission Rate %”, “commission\_rate”, “Data”, 100).
- Evaluate self.make\_column(translated “Commission”, “commission”, “Currency”, 120, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0677.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L187)

<a id="op-08d22a09f76af7"></a>
### Sales Partner Transaction Summary Report.extend report query

`operation_enterprise_selling_report_sales_partner_transaction_summary_business_behavior_sales_partner_transaction_summary_report_extend_report_query`

**Inputs** self.

**Local steps**

- Set self.dt\_item from Platform.qb.DocType(formatted text {self.filters at “doctype”} Item).
- Set self.query from nested operand in the contract.query.join(self.dt\_item).on(self.dt.name equals self.dt\_item.parent).select(self.dt\_item.base\_net\_rate.as\_(“rate”), self.dt\_item.qty, self.dt\_item.base\_net\_amount.as\_(“amount ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0677.json#L945) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L186)

<a id="op-13e96b49c90a7f"></a>
### Sales Partner Transaction Summary Report.apply filters

`operation_enterprise_selling_report_sales_partner_transaction_summary_business_behavior_sales_partner_transaction_summary_report_apply_filters`

**Inputs** self.

**Record and data access** read “Item Group” via get\_cached\_value · read “Item Group” via get\_all.

**Local steps**

- If not self.filters.get(“account\_for\_return\_entries”, self.filters.get(“show\_return\_entries”)).
  - Set self.query from self.query.where(self.dt\_item.qty &gt; 0.0).
- If self.filters.get(“brand”).
  - Set self.query from self.query.where(self.dt\_item.brand equals self.filters.get(“brand”)).
- If self.filters.get(“item\_group”).
  - Set tuple(lft, rgt) from Platform.get\_cached\_value(“Item Group”, self.filters.get(“item\_group”), list(“lft”, “rgt”)).
  - If item\_groups bound to Platform.get\_all(“Item Group”, filters = list(list(“lft”, “&gt;=”, lft), list(“rgt”, “&lt;=”, rgt)), pluck = “name”).
    - Set self.query from self.query.where(self.dt\_item.item\_group.isin(item\_groups)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item Group”, self.filters.get(“item\_group”), list(“lft”, “rgt”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L185)

## Report · Sales person commission summary

<a id="op-a063d1fbfa36ca"></a>
### Execute

`operation_enterprise_selling_report_sales_person_commission_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Set filters from mapping().
- Set columns from get\_columns(filters).
- Set entries from get\_entries(filters).
- Set data from list().
- Set seen\_documents from set().
- For each d in entries.
  - Set amount from no value when d.name belongs to seen\_documents, otherwise d.base\_net\_amount.
    - Value choice on d.name belongs to seen\_documents — true gives no value, false gives d.base\_net\_amount.
  - Evaluate seen\_documents.add(d.name).
  - Evaluate data.append(list(d.name, d.customer, d.territory, d.posting\_date, …)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L192)

<a id="op-681d1d09f0d1d2"></a>
### Get columns

`operation_enterprise_selling_report_sales_person_commission_summary_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- If not filters.get(“doc\_type”).
  - Evaluate msgprint(translated “Please select the document type first”, raise\_exception = 1).
- Set columns from list(mapping(“label” → translated filters at “doc\_type”, “options” → filters at “doc\_type”, “fieldname” → filters at “doc\_type”, “fieldtype” → “Link”, …), mapping(“label” → translated “Customer”, “options” ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0677.json#L4997) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L193)

<a id="op-747963b8f47459"></a>
### Get entries

`operation_enterprise_selling_report_sales_person_commission_summary_business_behavior_get_entries`

**Inputs** filters.

**Explicit results** entries.

**Local steps**

- Set dt from qb.DocType(filters at “doc\_type”).
- Set st from qb.DocType(“Sales Team”).
- Set date\_field from dt at “transaction\_date” when filters at “doc\_type” equals “Sales Order”, otherwise dt at “posting\_date”.
  - Value choice on filters at “doc\_type” equals “Sales Order” — true gives dt at “transaction\_date”, false gives dt at “posting\_date”.
- Set conditions from get\_conditions(dt, st, filters, date\_field).
- Set entries from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.all(co ….
- Return entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0677.json#L6131) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L195)

<a id="op-a18f68b176e8d4"></a>
### Get conditions

`operation_enterprise_selling_report_sales_person_commission_summary_business_behavior_get_conditions`

**Inputs** dt, st, filters, date\_field.

**Record and data access** read “Sales Person” via get\_value.

**Explicit results** conditions.

**Local steps**

- Set conditions from list().
- Evaluate conditions.append(dt.docstatus.eq(1)).
- Set from\_dt from filters.get(“from\_date”).
- Set to\_dt from filters.get(“to\_date”).
- If (from\_dt and to\_dt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_dt → to\_dt.
  - Evaluate conditions.append(date\_field.between(from\_dt, to\_dt)).
- Otherwise.
  - If (from\_dt and not to\_dt).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_dt → not to\_dt.
    - Evaluate conditions.append(date\_field.gte(from\_dt)).
  - Otherwise.
    - If (not from\_dt and to\_dt).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_dt → to\_dt.
      - Evaluate conditions.append(date\_field.lte(to\_dt)).
- For each field in list(“company”, “customer”, “territory”).
  - If filters.get(field).
    - Evaluate conditions.append(dt at field.eq(filters.get(field))).
- If filters.get(“sales\_person”).
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Sales Person”, filters.get(“sales\_person”), list(“lft”, “rgt”)).
  - Set sp from qb.DocType(“Sales Person”).
  - Evaluate conditions.append(st.sales\_person.isin(nested operand in the contract(nested operand in the contract).select(sp.name).where((sp.lft ≥ lft bitwise and sp.rgt ≤ rgt)))).
- Return conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L194)

## Report · Sales person target variance based on item group

<a id="op-878c08ca5e6e35"></a>
### Execute

`operation_enterprise_selling_report_sales_person_target_variance_based_on_item_group_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** get\_data\_column(filters, “Sales Person”).

**Local steps**

- Return get\_data\_column(filters, “Sales Person”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0678.json#L2178) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L202)

## Report · Sales person wise transaction summary

<a id="op-945adae905a3c3"></a>
### Execute

`operation_enterprise_selling_report_sales_person_wise_transaction_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Set filters from mapping().
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- Set entries from get\_entries(filters).
- Set item\_details from get\_item\_details().
- Set data from list().
- Set company\_currency from get\_company\_currency(filters.get(“company”)).
- Set seen\_item\_rows from set().
- For each d in entries.
  - If (d.stock\_qty &gt; 0 or filters.get(“show\_return\_entries”, 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.stock\_qty &gt; 0 → filters.get(“show\_return\_entries”, 0).
    - Set first\_row from d.item\_row does not belong to seen\_item\_rows.
    - Evaluate seen\_item\_rows.add(d.item\_row).
    - Evaluate data.append(list(d.name, d.customer, d.territory, d.warehouse, …)).
      - Value choice on first\_row — true gives d.stock\_qty, false gives no value.
      - Value choice on first\_row — true gives d.base\_net\_amount, false gives no value.
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L207)

<a id="op-8091fdb0219f3b"></a>
### Validate filters

`operation_enterprise_selling_report_sales_person_wise_transaction_summary_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “{0}, {1} or {2} are the only allowed options.”.format(expanded ALLOWED\_DOCTYPES).

**Local steps**

- Set ALLOWED\_DOCTYPES from list(“Sales Order”, “Sales Invoice”, “Delivery Note”).
- If not filters.get(“doc\_type”).
  - Evaluate msgprint(translated “Please select the document type first”, raise\_exception = 1).
- If filters.get(“doc\_type”) does not belong to ALLOWED\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “{0}, {1} or {2} are the only allowed options.”.format(expanded ALLOWED\_DOCTYPES)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0678.json#L4035) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L212)

<a id="op-cdfa330cc1a82f"></a>
### Get columns

`operation_enterprise_selling_report_sales_person_wise_transaction_summary_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated filters at “doc\_type”, “options” → filters at “doc\_type”, “fieldname” → Platform.scrub(filters at “doc\_type”), “fieldtype” → “Link”, …), mapping(“label” → translated “Cust ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0678.json#L4288) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L208)

<a id="op-10ad5edbb35393"></a>
### Get entries

`operation_enterprise_selling_report_sales_person_wise_transaction_summary_business_behavior_get_entries`

**Inputs** filters.

**Record and data access** read “Sales Person” via get\_value.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- Set doc\_type from filters at “doc\_type”.
- Set date\_field from “transaction\_date” when doc\_type equals “Sales Order”, otherwise “posting\_date”.
  - Value choice on doc\_type equals “Sales Order” — true gives “transaction\_date”, false gives “posting\_date”.
- Set qty\_field from “delivered\_qty” when doc\_type equals “Sales Order”, otherwise “qty”.
  - Value choice on doc\_type equals “Sales Order” — true gives “delivered\_qty”, false gives “qty”.
- Set dt from Platform.qb.DocType(doc\_type).
- Set dt\_item from Platform.qb.DocType(formatted text {doc\_type} Item).
- Set st from Platform.qb.DocType(“Sales Team”).
- Set calc\_qty from (dt\_item at qty\_field × dt\_item.conversion\_factor).
- Set calc\_net\_amount from (dt\_item.base\_net\_rate × dt\_item at qty\_field).
- Set stock\_qty\_case from nested operand in the contract().when(nested operand in the contract.status equals “Closed”, calc\_qty).else\_(dt\_item.stock\_qty).as\_(“stock\_qty”).
- Set base\_net\_amount\_case from nested operand in the contract().when(nested operand in the contract.status equals “Closed”, calc\_net\_amount).else\_(dt\_item.base\_net\_amount).as\_(“base\_net\_amount”).
- Set contribution\_amt\_case from nested operand in the contract().when(nested operand in the contract.status equals “Closed”, ((nested operand in the contract × nested operand in the contract) ÷ 100)).else\_(((dt\_item.base\_net\_amount × st. ….
- Set doc\_filters from mapping(“docstatus” → 1).
- For each field in list(“company”, “customer”, “territory”).
  - If filters.get(field).
    - Set doc\_filters at field from filters.get(field).
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set doc\_filters at date\_field from list(“between”, list(filters.get(“from\_date”), filters.get(“to\_date”))).
- Otherwise.
  - If filters.get(“from\_date”).
    - Set doc\_filters at date\_field from list(“&gt;=”, filters.get(“from\_date”)).
  - Otherwise.
    - If filters.get(“to\_date”).
      - Set doc\_filters at date\_field from list(“&lt;=”, filters.get(“to\_date”)).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(dt.name, dt.customer, dt.territory, dt at date\_fie ….
- If filters.get(“sales\_person”).
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Sales Person”, filters.get(“sales\_person”), list(“lft”, “rgt”)).
  - Set sp from Platform.qb.DocType(“Sales Person”).
  - Set query from query.where(st.sales\_person.isin(nested operand in the contract(nested operand in the contract).select(sp.name).where((sp.lft ≥ lft bitwise and sp.rgt ≤ rgt)))).
- If (filters.get(“item\_group”) or filters.get(“brand”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“item\_group”) → filters.get(“brand”).
  - Set items from get\_items(filters).
  - If not items.
    - Return list().
  - Set query from query.where(dt\_item.item\_code.isin(list of d at 0 for d drawn from items)).
    - Draw d from items.
- Set query from query.orderby(st.sales\_person).orderby(dt.name, order = Platform.qb.desc).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L209)

<a id="op-017ee46feb4b8b"></a>
### Get items

`operation_enterprise_selling_report_sales_person_wise_transaction_summary_business_behavior_get_items`

**Inputs** filters.

**Record and data access** read “Item Group” via get\_all.

**Explicit results** items.

**Local steps**

- Set item from qb.DocType(“Item”).
- Set item\_query\_conditions from list().
- If filters.get(“item\_group”).
  - Set item\_group from qb.DocType(“Item Group”).
  - Set tuple(lft, rgt) from Platform.db.get\_all(“Item Group”, filters = mapping(“name” → filters.get(“item\_group”)), fields = list(“lft”, “rgt”), as\_list = true) at 0.
  - Set item\_group\_query from qb.from\_(item\_group).select(item\_group.name).where((item\_group.lft ≥ lft bitwise and item\_group.rgt ≤ rgt)).
  - Evaluate item\_query\_conditions.append(item.item\_group.isin(item\_group\_query)).
- If filters.get(“brand”).
  - Evaluate item\_query\_conditions.append(item.brand equals filters.get(“brand”)).
- Set items from nested operand in the contract(nested operand in the contract).select(item.name).where(Criterion.all(item\_query\_conditions)).run().
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0679.json#L1989) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L211)

<a id="op-3b73ee278c81bd"></a>
### Get item details

`operation_enterprise_selling_report_sales_person_wise_transaction_summary_business_behavior_get_item_details`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Item).

**Explicit results** item\_details.

**Local steps**

- Set item\_details from mapping().
- For each d in Platform.db.sql(query text (SELECT, Item), as\_dict = 1).
  - Evaluate item\_details.setdefault(d.name, d).
- Return item\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L210)

## Record · Selling settings

[Record definition](../../../../data/record-types/selling_settings.json)

<a id="op-082e02354f53c8"></a>
### Selling Settings.on update

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_selling_settings_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.toggle\_hide\_tax\_id().
- Evaluate self.toggle\_editable\_rate\_for\_bundle\_items().
- Evaluate self.toggle\_discount\_accounting\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [toggle hide tax id](operations-023.md#op-0eaa8603d4056e), [toggle editable rate for bundle items](operations-023.md#op-e66a8d671e79ac), [toggle discount accounting fields](operations-023.md#op-e5abc8b26b8613).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0656.json#L3641) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1494)

<a id="op-e72cc2112b6a10"></a>
### Selling Settings.validate

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_selling_settings_validate`

**Inputs** self.

**Local steps**

- Set old\_doc from self.get\_doc\_before\_save().
- For each key in list(“cust\_master\_name”, “customer\_group”, “territory”, “maintain\_same\_sales\_rate”, …).
  - Set value from self.get(key).
  - Evaluate Platform.db.set\_default(key, empty text when value is identical to no value, otherwise value).
    - Value choice on value is identical to no value — true gives empty text, false gives value.
- Bind dependencies set\_by\_naming\_series.
- Evaluate set\_by\_naming\_series(“Customer”, “customer\_name”, self.get(“cust\_master\_name”) equals “Naming Series”, hide\_name\_field = false).
- Evaluate self.validate\_fallback\_to\_default\_price\_list().
- If (old\_doc and old\_doc.enable\_tracking\_sales\_commissions differs from self.enable\_tracking\_sales\_commissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_doc → old\_doc.enable\_tracking\_sales\_commissions differs from self.enable\_tracking\_sales\_commissions.
  - Evaluate toggle\_tracking\_sales\_commissions\_section(not self.enable\_tracking\_sales\_commissions).
- If (old\_doc and old\_doc.enable\_utm differs from self.enable\_utm).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_doc → old\_doc.enable\_utm differs from self.enable\_utm.
  - Evaluate toggle\_utm\_analytics\_section(not self.enable\_utm).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate fallback to default price list](operations-023.md#op-423ec68bd94baa).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1498)
