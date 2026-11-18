# Purchasing · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase order

[Record definition](../../../../data/record-types/purchase_order.json)

<a id="op-a2abf8f628a39e"></a>
### Make purchase invoice from portal

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_make_purchase_invoice_from_portal`

**Inputs** purchase\_order\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Portal User” via get\_all.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set doc from get\_mapped\_purchase\_invoice(purchase\_order\_name, ignore\_permissions = true).
- If Platform.session.user does not belong to Platform.get\_all(“Portal User”, mapping(“parenttype” → “Supplier”, “parent” → doc.supplier), pluck = “user”).
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- For each item in list of item for item drawn from doc.items where not item.qty.
  - Draw item from doc.items, keep a combination only if (not item.qty).
  - Evaluate doc.remove(item).
- Evaluate doc.save().
- Set Platform.response at “type” from “redirect”.
- Set Platform.response.location from (“/purchase-invoices/” + doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L806) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L46)

<a id="op-297fcb7b0777db"></a>
### Get mapped purchase invoice

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_purchase_invoice`

**Inputs** source\_name, target\_doc = no value, ignore\_permissions = false, args = no value.

**Record and data access** read “Purchase Order” via get\_value · read “Purchase Order Item” via get\_all.

**Explicit results** doc.

**Local steps**

- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Bind local operation postprocess for subsequent calls.
- Bind dependencies get\_billed\_qty\_data.
- Set has\_unit\_price\_items from Platform.db.get\_value(“Purchase Order”, source\_name, “has\_unit\_price\_items”).
- Set mapped\_qty\_by\_item from get\_qty\_already\_mapped(target\_doc, “po\_detail”).
- Set po\_items from Platform.get\_all(“Purchase Order Item”, filters = mapping(“parent” → source\_name), fields = list(“name”)).
- Set billed\_qty\_by\_item from get\_billed\_qty\_data(po\_items) when po\_items, otherwise mapping().
  - Value choice on po\_items — true gives get\_billed\_qty\_data(po\_items), false gives mapping().
- Bind local operation get\_billed\_and\_mapped\_qty for subsequent calls.
- Bind local operation is\_qty\_billed\_below\_amount for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set fields from mapping(“Purchase Order” → mapping(“doctype” → “Purchase Invoice”, “field\_map” → mapping(“party\_account\_currency” → “party\_account\_currency”, “supplier\_warehouse” → “supplier\_warehouse”), “field\_no\_map” →  ….
- Set doc from get\_mapped\_doc(“Purchase Order”, source\_name, fields, target\_doc, ignore\_permissions = ignore\_permissions, …).
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L794) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L34)

<a id="op-3a680806fe41b6"></a>
### Get mapped purchase invoice.postprocess

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_purchase_invoice_postprocess`

**Inputs** source, target.

**Local steps**

- Set target.flags.ignore\_permissions from ignore\_permissions.
- Evaluate set\_missing\_values(source, target).
- If target.get(“allocate\_advances\_automatically”).
  - Evaluate target.set\_advances().
- Evaluate target.set\_payment\_schedule().
- Set target.credit\_to from get\_party\_account(“Supplier”, source.supplier, source.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L797) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L37)

<a id="op-a970910829bc30"></a>
### Get mapped purchase invoice.get billed and mapped qty

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_purchase_invoice_get_billed_and_mapped_qty`

**Inputs** po\_item.

**Explicit results** (billed\_qty + flt(mapped\_qty\_by\_item.get(po\_item.name, 0))).

**Local steps**

- Set billed\_qty from flt(billed\_qty\_by\_item.get(po\_item.name), po\_item.precision(“qty”)).
- Return (billed\_qty + flt(mapped\_qty\_by\_item.get(po\_item.name, 0))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L795) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L35)

<a id="op-bb9e7072bf4f76"></a>
### Get mapped purchase invoice.is qty billed below amount

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_purchase_invoice_is_qty_billed_below_amount`

**Inputs** po\_item.

**Explicit results** (po\_item.name does not belong to mapped\_qty\_by\_item and po\_item.qty ≤ get\_billed\_and\_mapped\_qty(po\_item) and abs(flt(po\_item.billed\_amt)) &lt; abs(flt(po\_item.amount))).

**Local steps**

- Return (po\_item.name does not belong to mapped\_qty\_by\_item and po\_item.qty ≤ get\_billed\_and\_mapped\_qty(po\_item) and abs(flt(po\_item.billed\_amt)) &lt; abs(flt(po\_item.amount))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in po\_item.name does not belong to mapped\_qty\_by\_item → po\_item.qty ≤ get\_billed\_and\_mapped\_qty(po\_item) → abs(flt(po\_item.billed\_amt)) &lt; abs(flt(po\_item.amount)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L796) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L36)

<a id="op-af54581ae2b6f1"></a>
### Get mapped purchase invoice.update item

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_purchase_invoice_update_item`

**Inputs** obj, target, source\_parent.

**Record and data access** read “Project” via get\_value.

**Local steps**

- Set target.qty from 0 when is\_unit\_price\_row(obj, has\_unit\_price\_items), otherwise max((flt(obj.qty) − get\_billed\_and\_mapped\_qty(obj)), 0).
  - Value choice on is\_unit\_price\_row(obj, has\_unit\_price\_items) — true gives 0, false gives max((flt(obj.qty) − get\_billed\_and\_mapped\_qty(obj)), 0).
- Set item from get\_item\_defaults(target.item\_code, source\_parent.company).
- Set item\_group from get\_item\_group\_defaults(target.item\_code, source\_parent.company).
- Set target.cost\_center from (obj.cost\_center or Platform.db.get\_value(“Project”, obj.project, “cost\_center”) or item.get(“buying\_cost\_center”) or item\_group.get(“buying\_cost\_center”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in obj.cost\_center → Platform.db.get\_value(“Project”, obj.project, “cost\_center”) → item.get(“buying\_cost\_center”) → item\_group.get(“buying\_cost\_center”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L799) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L39)

<a id="op-794d5cbd34fbb8"></a>
### Get mapped purchase invoice.select item

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_purchase_invoice_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L798) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L38)

<a id="op-5be8d8e8e02c67"></a>
### Get list context

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Purchase Orders”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0339.json#L508) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L89) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1367)

<a id="op-02b3df97440c18"></a>
### Update status

`operation_enterprise_buying_record_definitions_purchase_order_business_behavior_update_status`

**Inputs** status, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper — translated “Cannot set the status of a Purchase Order to {0}.”.format(status) · validation helper — translated “Only a submitted Purchase Order can be held, closed or re-opened.”.

**Local steps**

- If status does not belong to tuple(“Draft”, “Submitted”, “On Hold”, “Closed”).
  - Call the validation error handler Platform.throw(translated “Cannot set the status of a Purchase Order to {0}.”.format(status)).
- Set po from Platform.get\_lazy\_doc(“Purchase Order”, name, check\_permission = “submit”).
- <a id="op-02b3df97440c18-guard-6"></a>If po.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Only a submitted Purchase Order can be held, closed or re-opened.”).
- Evaluate po.update\_status(status).
- Evaluate po.update\_delivered\_qty\_in\_sales\_order().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison po.docstatus differs from 1, po.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Only a submitted Purchase Order can be held, closed or re-opened.”. With po.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-02b3df97440c18-guard-6)

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1394)

<a id="op-49e2404edff7f5"></a>
### Make inter company sales order

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_make_inter_company_sales_order`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_inter\_company\_transaction(“Purchase Order”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_inter\_company\_transaction.
- Return make\_inter\_company\_transaction(“Purchase Order”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L804) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L44)

<a id="op-bf00c08246d136"></a>
### Make subcontracting order

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_make_subcontracting_order`

**Inputs** source\_name, target\_doc = no value, save = false, submit = false, notify = false.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on target\_doc · call submit on target\_doc · msgprint with translated “Subcontracting Order {0} created.”.format(get\_link\_to\_form(target\_doc.doctype, target\_doc.name)).

**Explicit results** target\_doc.

**Explicit failure paths** validation helper — translated “This Purchase Order has been fully subcontracted.”.

**Local steps**

- If not is\_po\_fully\_subcontracted(source\_name).
  - Set target\_doc from get\_mapped\_subcontracting\_order(source\_name, target\_doc).
  - If ((save or submit) and Platform.has\_permission(target\_doc.doctype, “create”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (save or submit) → Platform.has\_permission(target\_doc.doctype, “create”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in save → submit.
    - Evaluate target\_doc.save().
    - If (submit and Platform.has\_permission(target\_doc.doctype, “submit”, target\_doc)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in submit → Platform.has\_permission(target\_doc.doctype, “submit”, target\_doc).
      - Attempt the following.
        - Evaluate target\_doc.submit().
      - On failure (Exception) bound to e.
        - Evaluate target\_doc.add\_comment(“Comment”, ((translated “Submit Action Failed” + text in the contract) + str(e))).
    - If notify.
      - Evaluate Platform.msgprint(translated “Subcontracting Order {0} created.”.format(get\_link\_to\_form(target\_doc.doctype, target\_doc.name)), indicator = “green”, alert = true).
  - Return target\_doc.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “This Purchase Order has been fully subcontracted.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(target\_doc.doctype, “create”), Platform.has\_permission(target\_doc.doctype, “submit”, target\_doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L810) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L50)

<a id="op-cd177d0fda97f1"></a>
### Is po fully subcontracted

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_is_po_fully_subcontracted`

**Inputs** po\_name.

**Explicit results** not query.run(as\_dict = true).

**Local steps**

- Set table from Platform.qb.DocType(“Purchase Order Item”).
- Set query from nested operand in the contract.qb.from\_(table).select(table.name).where((table.parent equals po\_name bitwise and table.qty &gt; table.subcontracted\_qty)).
- Return not query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L802) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L42)

<a id="op-3c8404be2d9719"></a>
### Get mapped subcontracting order

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_subcontracting_order`

**Inputs** source\_name, target\_doc = no value.

**Explicit results** target\_doc.

**Local steps**

- Bind local operation post\_process for subsequent calls.
- If (target\_doc and isinstance(target\_doc, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → isinstance(target\_doc, str).
  - Set target\_doc from json.loads(target\_doc).
  - For each key in list(“service\_items”, “items”, “supplied\_items”).
    - If key belongs to target\_doc.
      - Remove target\_doc at key.
  - Set target\_doc from json.dumps(target\_doc).
- Set target\_doc from get\_mapped\_doc(“Purchase Order”, source\_name, mapping(“Purchase Order” → mapping(“doctype” → “Subcontracting Order”, “field\_map” → mapping(), “field\_no\_map” → list(“total\_qty”, “total”, “net\_total”), “vali ….
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L800) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L40)

<a id="op-b85851fa967177"></a>
### Get mapped subcontracting order.post process

`operation_enterprise_binding_enterprise_buying_doctype_purchase_order_purchase_order_get_mapped_subcontracting_order_post_process`

**Inputs** source\_doc, target\_doc.

**Record and data access** read “Job Card” via get\_cached\_value · read “Stock Settings” via get\_single\_value · read “Production Plan” via get\_value.

**Local steps**

- Evaluate target\_doc.populate\_items\_table().
- Set source\_rows from mapping of row.name → row for row drawn from source\_doc.items.
  - Draw row from source\_doc.items.
- If target\_doc.set\_warehouse.
  - For each item in target\_doc.items.
    - Set item.warehouse from target\_doc.set\_warehouse.
- Otherwise.
  - If source\_doc.set\_warehouse.
    - For each item in target\_doc.items.
      - Set item.warehouse from source\_doc.set\_warehouse.
  - Otherwise.
    - For each item in target\_doc.items.
      - Set item.warehouse from source\_rows at item.purchase\_order\_item.warehouse.
- For each item in target\_doc.items.
  - Set item.job\_card from source\_rows at item.purchase\_order\_item.job\_card.
  - If not target\_doc.supplier\_warehouse.
    - Set target\_doc.supplier\_warehouse from Platform.get\_cached\_value(“Job Card”, item.job\_card, “wip\_warehouse”).
- Set production\_plan from set(list of item.production\_plan for item drawn from source\_doc.items where item.production\_plan).
  - Draw item from source\_doc.items, keep a combination only if (item.production\_plan).
- If production\_plan.
  - Set target\_doc.production\_plan from production\_plan.pop().
- Set target\_doc.reserve\_stock from (Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”) or Platform.get\_value(“Production Plan”, target\_doc.production\_plan, “reserve\_stock”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”) → Platform.get\_value(“Production Plan”, target\_doc.production\_plan, “reserve\_stock”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Job Card”, item.job\_card, “wip\_warehouse”), Platform.get\_single\_value(“Stock Settings”, “auto\_reserve\_stock”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L801) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L41)

<a id="op-203ec461204482"></a>
### Get data

`operation_enterprise_buying_record_definitions_purchase_order_purchase_order_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “purchase\_order”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Request” → “reference\_name”, “Auto Repeat” → “re ….

**Local steps**

- Return mapping(“fieldname” → “purchase\_order”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Request” → “reference\_name”, “Auto Repeat” → “re ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0339.json#L861) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1396)

## Report · Purchase order analysis

<a id="op-55847e05911c28"></a>
### Execute

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(list(), list()) · tuple(list(), list(), no value, list()) · tuple(columns, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Return tuple(list(), list()).
- Set filters from Platform.\_dict(filters).
- Set filters.company from (filters.get(“company”) or Enterprise.get\_default\_company()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company”) → Enterprise.get\_default\_company().
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- If not data.
  - Return tuple(list(), list(), no value, list()).
- Evaluate update\_received\_amount(data).
- Evaluate update\_billed\_qty(data).
- Set tuple(data, chart\_data) from prepare\_data(data, filters).
- Return tuple(columns, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L215)

<a id="op-0704c984be7d7d"></a>
### Validate filters

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”) · validation helper — translated “From and To Dates are required.” · validation helper — translated “To Date cannot be before From Date.” · validation helper — translated “Group the report by Purchase Order or by Item, not both.”.

**Local steps**

- If not filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- Set tuple(from\_date, to\_date) from tuple(filters.get(“from\_date”), filters.get(“to\_date”)).
- Evaluate validate\_date\_range(mapping(“from\_date” → getdate(from\_date), “to\_date” → getdate(to\_date))).
- If (not from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_date → to\_date.
  - Call the validation error handler Platform.throw(translated “From and To Dates are required.”).
- Otherwise.
  - If date\_diff(to\_date, from\_date) &lt; 0.
    - Call the validation error handler Platform.throw(translated “To Date cannot be before From Date.”).
- If (filters.get(“group\_by\_po”) and filters.get(“group\_by\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“group\_by\_po”) → filters.get(“group\_by\_item”).
  - Call the validation error handler Platform.throw(translated “Group the report by Purchase Order or by Item, not both.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L222)

<a id="op-627cd8b1d6426d"></a>
### Get data

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set po from Platform.qb.DocType(“Purchase Order”).
- Set po\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If filters.get(“name”).
  - Set query from query.where(po.name.isin(filters.get(“name”))).
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set query from query.where(po.transaction\_date.between(filters.get(“from\_date”), filters.get(“to\_date”))).
- If filters.get(“status”).
  - Set query from query.where(po.status.isin(filters.get(“status”))).
- If filters.get(“project”).
  - Set query from query.where(po\_item.project equals filters.get(“project”)).
- If match\_conditions bound to build\_match\_conditions(“Purchase Order”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set data from query.run(as\_dict = true).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L217)

<a id="op-f2e6c90e4d7030"></a>
### Update received amount

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_update_received_amount`

**Inputs** data.

**Local steps**

- Set pr\_data from get\_received\_amount\_data(data).
- For each row in data.
  - Set row.received\_qty\_amount from flt(pr\_data.get(row.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0358.json#L6059) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L221)

<a id="op-a786f902cda5d2"></a>
### Update billed qty

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_update_billed_qty`

**Inputs** data.

**Local steps**

- Set billed\_qty from get\_billed\_qty\_data(data).
- For each row in data.
  - Set row.billed\_qty from flt(billed\_qty.get(row.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L232) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L894) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L134)

<a id="op-bc09682de5481a"></a>
### Get billed qty data

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_get_billed_qty_data`

**Inputs** data.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set pi\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set po\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(po\_item.name, (nested operand in the contract(nested operand in the contract) ÷ nested operand in the contract.conversion\_factor)).wher ….
  - Draw row from data.
- Return Platform.\_dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L222) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L124)

<a id="op-b0fcd94b8430d1"></a>
### Get received amount data

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_get_received_amount_data`

**Inputs** data.

**Explicit results** Platform.\_dict() · Platform.\_dict(data).

**Local steps**

- Set pr from Platform.qb.DocType(“Purchase Receipt”).
- Set pr\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set po\_items from list of row.name for row drawn from data.
  - Draw row from data.
- If not po\_items.
  - Return Platform.\_dict().
- Set query from nested operand in the contract(nested operand in the contract).select(pr\_item.purchase\_order\_item, nested operand in the contract.as\_(“received\_qty\_amount”)).where((pr.docstatus equals 1 bitwise and nested ….
- Set data from query.run().
- If not data.
  - Return Platform.\_dict().
- Return Platform.\_dict(data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0358.json#L6184) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L218)

<a id="op-c6bb5f44799c46"></a>
### Prepare data

`operation_enterprise_buying_report_purchase_order_analysis_business_behavior_prepare_data`

**Inputs** data, filters.

**Explicit results** tuple(data, chart\_data).

**Local steps**

- Set tuple(completed, pending) from tuple(0, 0).
- For each row in data.
  - Set row at “qty\_to\_bill” from (flt(row at “qty”) − flt(row at “billed\_qty”)).
  - If row at “status” equals “Closed”.
    - Evaluate row.update(pending\_qty = 0, qty\_to\_bill = 0, pending\_amount = 0).
  - Update completed using + row at “billed\_amount”.
  - Update pending using + row at “pending\_amount”.
- Set chart\_data from prepare\_chart\_data(pending, completed).
- If filters.get(“group\_by\_po”).
  - Set data from group\_by\_purchase\_order(data).
- Otherwise.
  - If filters.get(“group\_by\_item”).
    - Set data from group\_by\_item(data).
- Return tuple(data, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L220)

<a id="op-2b514e8a763dee"></a>
### Group by purchase order

`operation_enterprise_binding_enterprise_buying_report_purchase_order_analysis_purchase_order_analysis_group_by_purchase_order`

**Inputs** data.

**Explicit results** list(purchase\_order\_map.values()).

**Local steps**

- Set purchase\_order\_map from mapping().
- For each row in data.
  - Set group from purchase\_order\_map.get(row at “purchase\_order”).
  - If not group.
    - Set purchase\_order\_map at row at “purchase\_order” from copy.deepcopy(row).
    - Continue with the next iteration or loop test.
  - Set group at “required\_date” from min(getdate(group at “required\_date”), getdate(row at “required\_date”)).
  - Evaluate add\_aggregated\_fields(group, row).
- Return list(purchase\_order\_map.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L231) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L893) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L133)
