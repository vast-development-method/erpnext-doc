# Purchasing · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Supplier quotation

[Record definition](../../../../data/record-types/supplier_quotation.json)

<a id="op-fec2c8a8b3eef5"></a>
### Make quotation

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_make_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Set doclist from get\_mapped\_doc(“Supplier Quotation”, source\_name, mapping(“Supplier Quotation” → mapping(“doctype” → “Quotation”, “field\_map” → mapping(“name” → “supplier\_quotation”), “postprocess” → deferred anonymous ex ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L839) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L79)

<a id="op-5fc0b8be16ad47"></a>
### Set expired status

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_set_expired_status`

**Inputs** no declared parameters.

**Local steps**

- Set supplier\_quotation from Platform.qb.DocType(“Supplier Quotation”).
- Set purchase\_order from Platform.qb.DocType(“Purchase Order”).
- Set purchase\_order\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set purchase\_order\_against\_quotation from nested operand in the contract(nested operand in the contract).from\_(purchase\_order\_item).select(purchase\_order.name).where((((purchase\_order\_item.docstatus equals 1 bitwise and purchase\_order.docstatus eq ….
- Evaluate nested operand in the contract(nested operand in the contract).set(supplier\_quotation.status, “Expired”).where((((nested operand in the contract equals nested operand in the contract bitwise and nested ope ….run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L5937) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L73)

<a id="op-aaafaba04aa04e"></a>
### Get ordered items

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_get_ordered_items`

**Inputs** supplier\_quotation.

**Declared result** Platform.\_dict.

**Record and data access** read “Supplier Quotation Item” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Supplier Quotation Item”, mapping(“docstatus” → 1, “parent” → supplier\_quotation, “ordered\_qty” → tuple(“&gt;”, 0)), list(“name”, “ordered\_qty”), as\_list = true)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(“Supplier Quotation Item”, mapping(“docstatus” → 1, “parent” → supplier\_quotation, “ordered\_qty” → tuple(“&gt;”, 0)), list(“name”, “ordered\_qty”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L833) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L73)

<a id="op-9a680a77498939"></a>
### Get data

`operation_enterprise_buying_record_definitions_supplier_quotation_supplier_quotation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “supplier\_quotation”, “non\_standard\_fieldnames” → mapping(“Auto Repeat” → “reference\_document”), “internal\_links” → mapping(“Material Request” → list(“items”, “material\_request”), “Re ….

**Local steps**

- Return mapping(“fieldname” → “supplier\_quotation”, “non\_standard\_fieldnames” → mapping(“Auto Repeat” → “reference\_document”), “internal\_links” → mapping(“Material Request” → list(“items”, “material\_request”), “Re ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L6456) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L86)

## Report · Supplier quotation comparison

<a id="op-6154c4c1e66b78"></a>
### Execute

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list()) · tuple(columns, data, message, chart\_data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Return tuple(list(), list()).
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- Set supplier\_quotation\_data from get\_data(filters).
- Set tuple(data, chart\_data) from prepare\_data(supplier\_quotation\_data, filters).
- Set message from get\_message().
- Return tuple(columns, data, message, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L260)

<a id="op-4b19cf85089bcb"></a>
### Validate filters

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_validate_filters`

**Inputs** filters.

**Local steps**

- If (not filters.get(“categorize\_by”) and filters.get(“group\_by”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.get(“categorize\_by”) → filters.get(“group\_by”).
  - Set filters at “categorize\_by” from filters at “group\_by”.
  - Set filters at “categorize\_by” from filters at “categorize\_by”.replace(“Group by”, “Categorize by”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0362.json#L4628) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L268)

<a id="op-74ae67ca7a0726"></a>
### Get data

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_get_data`

**Inputs** filters.

**Explicit results** supplier\_quotation\_data.

**Local steps**

- Set sq from Platform.qb.DocType(“Supplier Quotation”).
- Set sq\_item from Platform.qb.DocType(“Supplier Quotation Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(sq\_item.parent, sq\_item.item\_code, sq\_item.qty, sq.currency, …).where((sq.company equals nested operand in the contract.get(“company”)  ….
- If filters.get(“status”) equals “Draft”.
  - Set query from query.where(sq\_item.docstatus equals 0).
- Otherwise.
  - If filters.get(“status”) equals “Submitted”.
    - Set query from query.where(sq\_item.docstatus equals 1).
  - Otherwise.
    - Set query from query.where(sq\_item.docstatus &lt; 2).
- If filters.get(“item\_code”).
  - Set query from query.where(sq\_item.item\_code equals filters.get(“item\_code”)).
- If filters.get(“supplier\_quotation”).
  - Set query from query.where(sq\_item.parent.isin(filters.get(“supplier\_quotation”))).
- If filters.get(“request\_for\_quotation”).
  - Set query from query.where(sq\_item.request\_for\_quotation equals filters.get(“request\_for\_quotation”)).
- If filters.get(“supplier”).
  - Set query from query.where(sq.supplier.isin(filters.get(“supplier”))).
- If filters.get(“order\_status”) equals “Not Ordered”.
  - Set query from query.where(sq.status.notin(list(“Partially Ordered”, “Ordered”))).
- Otherwise.
  - If filters.get(“order\_status”).
    - Set query from query.where(sq.status equals filters.get(“order\_status”)).
- If not filters.get(“include\_expired”).
  - Set query from query.where(sq.status differs from “Expired”).
- Set supplier\_quotation\_data from query.run(as\_dict = true).
- Return supplier\_quotation\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L262)

<a id="op-b6b4878d28a5c9"></a>
### Prepare data

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_prepare_data`

**Inputs** supplier\_quotation\_data, filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(out, chart\_data).

**Local steps**

- Set tuple(out, groups, qty\_list, suppliers, …) from tuple(list(), list(), list(), list(), …).
- Set group\_wise\_map from defaultdict(list).
- Set supplier\_qty\_price\_map from mapping().
- Set rows\_by\_item from defaultdict(list).
- Set group\_by\_field from “supplier\_name” when filters.get(“categorize\_by”) equals “Categorize by Supplier”, otherwise “item\_code”.
  - Value choice on filters.get(“categorize\_by”) equals “Categorize by Supplier” — true gives “supplier\_name”, false gives “item\_code”.
- Set float\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set company\_currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
- For each data in supplier\_quotation\_data.
  - Set group from data.get(group\_by\_field).
  - Set row from mapping(“item\_code” → empty text when group\_by\_field equals “item\_code”, otherwise data.get(“item\_code”), “supplier\_name” → empty text when group\_by\_field equals “supplier\_name”, otherwise data.get(“suppli ….
    - Value choice on group\_by\_field equals “item\_code” — true gives empty text, false gives data.get(“item\_code”).
    - Value choice on group\_by\_field equals “supplier\_name” — true gives empty text, false gives data.get(“supplier\_name”).
  - Set row at “price\_per\_unit” from get\_price\_per\_stock\_unit(row at “price”, data.get(“rate”), data).
  - Set row at “base\_price\_per\_unit” from get\_price\_per\_stock\_unit(row at “base\_amount”, row at “base\_rate”, data).
  - Evaluate group\_wise\_map at group.append(row).
  - Evaluate rows\_by\_item at data.get(“item\_code”).append(row).
  - Set supplier from data.get(“supplier\_name”).
  - If filters.get(“item\_code”).
    - Set qty\_prices from supplier\_qty\_price\_map.setdefault(supplier, mapping()).
    - Set qty\_prices at row at “qty” from min(qty\_prices.get(row at “qty”, row at “base\_amount”), row at “base\_amount”).
  - Evaluate groups.append(group).
  - Evaluate suppliers.append(supplier).
  - Evaluate qty\_list.append(data.get(“qty”)).
- Set groups from list(set(groups)).
- Set suppliers from list(set(suppliers)).
- Set qty\_list from list(set(qty\_list)).
- If (group\_by\_field equals “item\_code” or filters.get(“item\_code”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in group\_by\_field equals “item\_code” → filters.get(“item\_code”).
  - Evaluate flag\_cheapest\_quotes(rows\_by\_item).
- For each group in groups.
  - Set group\_entries from group\_wise\_map at group.
  - Evaluate group\_entries at 0.update(mapping(group\_by\_field → group)).
  - Evaluate out.extend(group\_entries).
- If filters.get(“item\_code”).
  - Set chart\_data from prepare\_chart\_data(suppliers, qty\_list, supplier\_qty\_price\_map, company\_currency).
- Return tuple(out, chart\_data).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L266)

<a id="op-20db6978537915"></a>
### Flag cheapest quotes

`operation_enterprise_binding_enterprise_buying_report_supplier_quotation_comparison_supplier_quotation_comparison_flag_cheapest_quotes`

**Inputs** rows\_by\_item.

**Local steps**

- For each rows in rows\_by\_item.values().
  - Set min\_price from min(generator of row at “base\_price\_per\_unit” for row drawn from rows).
    - Draw row from rows.
  - For each row in rows.
    - If row at “base\_price\_per\_unit” equals min\_price.
      - Set row at “min” from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L233) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L895) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L135)

<a id="op-fa9187896eb8c0"></a>
### Get price per stock unit

`operation_enterprise_binding_enterprise_buying_report_supplier_quotation_comparison_supplier_quotation_comparison_get_price_per_stock_unit`

**Inputs** amount, rate, data.

**Explicit results** (flt(amount) ÷ flt(data.get(“stock\_qty”))) · (flt(rate) ÷ (flt(data.get(“conversion\_factor”)) or 1)).

**Local steps**

- If flt(data.get(“stock\_qty”)).
  - Return (flt(amount) ÷ flt(data.get(“stock\_qty”))).
- Return (flt(rate) ÷ (flt(data.get(“conversion\_factor”)) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(data.get(“conversion\_factor”)) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L234) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L896) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L136)

<a id="op-84930f3ae500e7"></a>
### Get order status

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_get_order_status`

**Inputs** status.

**Explicit results** status when status belongs to tuple(“Partially Ordered”, “Ordered”), otherwise “Not Ordered”.

**Local steps**

- Return status when status belongs to tuple(“Partially Ordered”, “Ordered”), otherwise “Not Ordered”.
  - Value choice on status belongs to tuple(“Partially Ordered”, “Ordered”) — true gives status, false gives “Not Ordered”.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0363.json#L1828) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L264)

<a id="op-59ec546fd76725"></a>
### Prepare chart data

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_prepare_chart_data`

**Inputs** suppliers, qty\_list, supplier\_qty\_price\_map, company\_currency.

**Record and data access** read “Currency” via get\_value.

**Explicit results** chart\_data.

**Local steps**

- Set data\_points\_map from mapping().
- Evaluate qty\_list.sort().
- For each supplier in suppliers.
  - Set entry from supplier\_qty\_price\_map at supplier.
  - For each qty in qty\_list.
    - If qty does not belong to data\_points\_map.
      - Set data\_points\_map at qty from list().
    - If qty belongs to entry.
      - Evaluate data\_points\_map at qty.append(entry at qty).
    - Otherwise.
      - Evaluate data\_points\_map at qty.append(no value).
- Set dataset from list().
- Set currency\_symbol from Platform.db.get\_value(“Currency”, company\_currency, “symbol”).
- For each qty in qty\_list.
  - Set datapoints from mapping(“name” → (((currency\_symbol + “ (Qty ”) + str(qty)) + “ )”), “values” → data\_points\_map at qty).
  - Evaluate dataset.append(datapoints).
- Set chart\_data from mapping(“data” → mapping(“labels” → suppliers, “datasets” → dataset), “type” → “bar”).
- Return chart\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L265)

<a id="op-94d3aec864865a"></a>
### Get columns

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_get_columns`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** columns.

**Local steps**

- Set currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
- Set group\_by\_columns from list(mapping(“fieldname” → “supplier\_name”, “label” → translated “Supplier”, “fieldtype” → “Link”, “options” → “Supplier”, …), mapping(“fieldname” → “item\_code”, “label” → translated “Item”, “fieldtype” →  ….
- Set columns from list(mapping(“fieldname” → “uom”, “label” → translated “UOM”, “fieldtype” → “Link”, “options” → “UOM”, …), mapping(“fieldname” → “qty”, “label” → translated “Quantity”, “fieldtype” → “Float”, “width” → 80) ….
- If filters.get(“categorize\_by”) equals “Categorize by Item”.
  - Evaluate group\_by\_columns.reverse().
- Set columns at slice 0 to 0 from group\_by\_columns.
- Return columns.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L261)

<a id="op-cb4cbd2dbb1173"></a>
### Get message

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_get_message`

**Inputs** no declared parameters.

**Explicit results** formatted text &lt;span class="indicator"&gt;  {translated “Valid Till”}:&amp;nbsp;&amp;nbsp;  &lt;/span&gt;  &lt;span class="indicator orange"&gt;  {translated “Expires in a week or less.

**Local steps**

- Return formatted text &lt;span class="indicator"&gt;  {translated “Valid Till”}:&amp;nbsp;&amp;nbsp;  &lt;/span&gt;  &lt;span class="indicator orange"&gt;  {translated “Expires in a week or less.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0363.json#L4268) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L263)

<a id="op-6aaad48a1956ed"></a>
### Set default supplier

`operation_enterprise_buying_report_supplier_quotation_comparison_business_behavior_set_default_supplier`

**Inputs** item\_code, supplier, company.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “Item Default”.

**Local steps**

- Evaluate Platform.has\_permission(“Item”, “write”, doc = item\_code, throw = true).
- Evaluate Platform.db.set\_value(“Item Default”, mapping(“parent” → item\_code, “company” → company), “default\_supplier”, supplier).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, “write”, doc = item\_code, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0363.json#L4388) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L267)

## Record · Supplier scorecard

[Record definition](../../../../data/record-types/supplier_scorecard.json)

<a id="op-abdd75ac6798a6"></a>
### Supplier Scorecard.validate

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_supplier_scorecard_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_standings().
- Evaluate self.validate\_criteria\_weights().
- Evaluate self.calculate\_total\_score().
- Evaluate self.update\_standing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate standings](operations-011.md#op-ea709e5477419c), [validate criteria weights](operations-011.md#op-8f7cb27b7ae8de), [calculate total score](operations-011.md#op-9244c09f9c5518), [update standing](operations-011.md#op-67a818ef34be73).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0351.json#L3508) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L117)

<a id="op-4cc519cfd9a9df"></a>
### Supplier Scorecard.on update

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_supplier_scorecard_on_update`

**Inputs** self.

**State and service calls** call save on self.

**Explicit results** no value.

**Local steps**

- If self.flags.in\_rescore.
  - Return no value.
- Set previous\_status from (self.get\_doc\_before\_save() or Platform.\_dict()).status.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_doc\_before\_save() → Platform.\_dict().
- If create\_scorecard\_periods(self) &gt; 0.
  - Set self.flags.in\_rescore from true.
  - Attempt the following.
    - Evaluate self.save().
  - On exit, including pending return or failure.
    - Set self.flags.in\_rescore from false.
- If self.status differs from previous\_status.
  - Evaluate self.notify\_standing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify standing](operations-011.md#op-dcfb0bd780bbde).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L216) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L114)

<a id="op-dcfb0bd780bbde"></a>
### Supplier Scorecard.notify standing

`operation_enterprise_binding_enterprise_buying_doctype_supplier_scorecard_supplier_scorecard_supplierscorecard_notify_standing`

**Inputs** self.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Set recipients from self.get\_standing\_recipients().
- If (not recipients or not EmailAccount.find\_outgoing(match\_by\_doctype = self.doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not recipients → not EmailAccount.find\_outgoing(match\_by\_doctype = self.doctype).
  - Return no value.
- Evaluate Platform.sendmail(recipients = recipients, subject = translated “Supplier Scorecard standing of {0}: {1}”.format(self.supplier, self.status), message = translated “The Supplier Scorecard standing of {0} is ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get standing recipients](operations-011.md#op-4cec2da4a47ee5).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = translated “Supplier Scorecard standing of {0}: {1}”.format(self.supplier, self.status), message = translated “The Supplier Scorecard standing of {0} is ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L846) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L86)

<a id="op-4cec2da4a47ee5"></a>
### Supplier Scorecard.get standing recipients

`operation_enterprise_binding_enterprise_buying_doctype_supplier_scorecard_supplier_scorecard_supplierscorecard_get_standing_recipients`

**Inputs** self.

**Record and data access** read “Supplier” via get\_value.

**Explicit results** list of recipient for recipient drawn from recipients where recipient.

**Local steps**

- Set recipients from get\_employee\_emails(list(self.employee)) when self.notify\_employee, otherwise list().
  - Value choice on self.notify\_employee — true gives get\_employee\_emails(list(self.employee)), false gives list().
- If self.notify\_supplier.
  - Evaluate recipients.append(Platform.db.get\_value(“Supplier”, self.supplier, “email\_id”)).
- Return list of recipient for recipient drawn from recipients where recipient.
  - Draw recipient from recipients, keep a combination only if (recipient).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L845) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L85)

<a id="op-6d493a0ba954d1"></a>
### Supplier Scorecard.on trash

`operation_enterprise_binding_enterprise_buying_doctype_supplier_scorecard_supplier_scorecard_supplierscorecard_on_trash`

**Inputs** self.

**State and service calls** request set\_value on “Supplier”.

**Local steps**

- Evaluate Platform.db.set\_value(“Supplier”, self.supplier, dict.fromkeys(STANDING\_FLAGS, 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L847) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L87)

<a id="op-ea709e5477419c"></a>
### Supplier Scorecard.validate standings

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_supplier_scorecard_validate_standings`

**Inputs** self.

**Local steps**

- Set score from 0.
- For each c1 in self.standings.
  - For each c2 in self.standings.
    - If c1 differs from c2.
      - If (c1.max\_grade &gt; c2.min\_grade and c1.min\_grade &lt; c2.max\_grade).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in c1.max\_grade &gt; c2.min\_grade → c1.min\_grade &lt; c2.max\_grade.
        - Evaluate throw(translated “Overlap in scoring between {0} and {1}”.format(c1.standing\_name, c2.standing\_name)).
    - If c2.min\_grade equals score.
      - Set score from c2.max\_grade.
- If score &lt; 100.
  - Evaluate throw(translated “Unable to find score starting at {0}. You need to have standing scores covering 0 to 100”.format(score)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L119)

<a id="op-8f7cb27b7ae8de"></a>
### Supplier Scorecard.validate criteria weights

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_supplier_scorecard_validate_criteria_weights`

**Inputs** self.

**Local steps**

- Set weight from 0.
- For each c in self.criteria.
  - Update weight using + c.weight.
- If flt(weight, 2) differs from 100.
  - Evaluate throw(translated “Criteria weights must add up to 100%”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L118)

<a id="op-9244c09f9c5518"></a>
### Supplier Scorecard.calculate total score

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_supplier_scorecard_calculate_total_score`

**Inputs** self.

**Record and data access** execute query text (SELECT, Supplier Scorecard Period) · resolve a document from “Supplier Scorecard Period” via get\_doc.

**Local steps**

- Set scorecards from Platform.db.sql(query text (SELECT, Supplier Scorecard Period), mapping(“sc” → self.name), as\_dict = 1).
- Set period from 0.
- Set total\_score from 0.
- Set total\_max\_score from 0.
- For each scp in scorecards.
  - Set my\_sc from Platform.get\_doc(“Supplier Scorecard Period”, scp.name).
  - Set my\_scp\_weight from self.weighting\_function.
  - Set my\_scp\_weight from my\_scp\_weight.replace(“{period\_number}”, str(period)).
  - Set my\_scp\_maxweight from my\_scp\_weight.replace(“{total\_score}”, “100”).
  - Set my\_scp\_weight from my\_scp\_weight.replace(“{total\_score}”, str(my\_sc.total\_score)).
  - Set max\_score from my\_sc.calculate\_weighted\_score(my\_scp\_maxweight).
  - Set score from my\_sc.calculate\_weighted\_score(my\_scp\_weight).
  - Update total\_score using + score.
  - Update total\_max\_score using + max\_score.
  - Update period using + 1.
- If total\_max\_score &gt; 0.
  - Set self.supplier\_score from round((100.0 × (total\_score ÷ total\_max\_score)), 1).
- Otherwise.
  - Set self.supplier\_score from 100.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L113)

<a id="op-67a818ef34be73"></a>
### Supplier Scorecard.update standing

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_supplier_scorecard_update_standing`

**Inputs** self.

**State and service calls** request set\_value on “Supplier”.

**Local steps**

- Set highest\_grade from max(generator of s.max\_grade for s drawn from self.standings where s.max\_grade, default = 0).
  - Draw s from self.standings, keep a combination only if (s.max\_grade).
- For each standing in self.standings.
  - If self.score\_within\_standing(standing, highest\_grade).
    - Set self.status from standing.standing\_name.
    - Set self.indicator\_color from standing.standing\_color.
    - Set self.notify\_supplier from standing.notify\_supplier.
    - Set self.notify\_employee from standing.notify\_employee.
    - Set self.employee from standing.employee\_link.
    - For each fieldname in STANDING\_FLAGS.
      - Evaluate self.set(fieldname, standing.get(fieldname)).
      - Evaluate Platform.db.set\_value(“Supplier”, self.supplier, fieldname, self.get(fieldname)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [score within standing](operations-012.md#op-144545fdaef742).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L116)
