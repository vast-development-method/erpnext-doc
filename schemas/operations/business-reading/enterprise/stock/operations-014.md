# Inventory and warehouses · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Fifo queue vs qty after transaction comparison

<a id="op-0276e207779df4"></a>
### Keeps fifo queue

`operation_enterprise_binding_enterprise_stock_report_fifo_queue_vs_qty_after_transaction_comparison_fifo_queue_vs_qty_after_transaction_comparison_keeps_fifo_queue`

**Inputs** sle, valuation\_method.

**Explicit results** true · maintains\_fifo\_queue(sle, valuation\_method).

**Local steps**

- If (valuation\_method differs from “Moving Average” and is\_serial\_no\_wise\_valuation\_disabled(sle.item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in valuation\_method differs from “Moving Average” → is\_serial\_no\_wise\_valuation\_disabled(sle.item\_code).
  - Return true.
- Return maintains\_fifo\_queue(sle, valuation\_method).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L955)

<a id="op-fe6de1bc7ac618"></a>
### Set queue totals

`operation_enterprise_binding_enterprise_stock_report_fifo_queue_vs_qty_after_transaction_comparison_fifo_queue_vs_qty_after_transaction_comparison_set_queue_totals`

**Inputs** sle.

**Local steps**

- Set sle.fifo\_queue\_qty from 0.0.
- Set sle.fifo\_stock\_value from 0.0.
- For each tuple(qty, rate) in json.loads((sle.stock\_queue or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sle.stock\_queue → “&#91;&#93;”.
  - Update sle.fifo\_queue\_qty using + flt(qty).
  - Update sle.fifo\_stock\_value using + (flt(qty) × flt(rate)).
- Set sle.fifo\_qty\_diff from (sle.qty\_after\_transaction − sle.fifo\_queue\_qty).
- Set sle.fifo\_value\_diff from (sle.stock\_value − sle.fifo\_stock\_value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L956)

<a id="op-b482f6ac5b7f3d"></a>
### Get columns

`operation_enterprise_stock_report_fifo_queue_vs_quantity_after_transaction_comparison_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → translated “Stock Ledger Entry”, “options” → “Stock Ledger Entry”), mapping(“fieldname” → “item\_code”, “fieldtype” → “Link”, “label” → tra ….

**Local steps**

- Return list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → translated “Stock Ledger Entry”, “options” → “Stock Ledger Entry”), mapping(“fieldname” → “item\_code”, “fieldtype” → “Link”, “label” → tra ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0890.json#L4906) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L137)

## Service · Get item details

<a id="op-12593369f18ce3"></a>
### Preprocess ctx

`operation_enterprise_stock_get_item_details_business_behavior_preprocess_context`

**Inputs** ctx.

**Local steps**

- If not ctx.price\_list.
  - Set ctx.price\_list from (ctx.selling\_price\_list or ctx.buying\_price\_list).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.selling\_price\_list → ctx.buying\_price\_list.
- If (not ctx.item\_code and ctx.barcode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ctx.item\_code → ctx.barcode.
  - Set ctx.item\_code from get\_item\_code(barcode = ctx.barcode).
- Otherwise.
  - If (not ctx.item\_code and ctx.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ctx.item\_code → ctx.serial\_no.
    - Set ctx.item\_code from get\_item\_code(serial\_no = ctx.serial\_no).
- Evaluate set\_transaction\_type(ctx).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0879.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L758)

<a id="op-bff43fa634cd86"></a>
### Get item details

`operation_enterprise_stock_get_item_details_business_behavior_get_item_details`

**Inputs** ctx, doc = no value, for\_validate = false, overwrite\_warehouse = true.

**Wrappers, in declaration order** Platform.whitelist(), Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Declared result** ItemDetails.

**Explicit results** out.

**Local steps**

- Evaluate validate\_pricing\_context(ctx).
- Set out from \_get\_item\_details(ctx, doc, for\_validate, overwrite\_warehouse).
- For each warehouse in tuple(out.warehouse, ctx.warehouse, ctx.from\_warehouse).
  - If warehouse.
    - Evaluate Enterprise.require\_user\_permission(“Warehouse”, warehouse).
- Return out.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L733)

<a id="op-360e9e1bb2814b"></a>
### Get item details

`operation_enterprise_binding_enterprise_stock_get_item_details_get_item_details`

**Inputs** ctx, doc = no value, for\_validate = false, overwrite\_warehouse = true.

**Wrappers, in declaration order** Enterprise.normalize\_ctx\_input(ItemDetailsCtx).

**Declared result** ItemDetails.

**Record and data access** resolve a document from “Item” via get\_cached\_doc · read “Selling Settings” via get\_single\_value · read “Stock Settings” via get\_single\_value.

**Explicit results** out.

**Local steps**

- Evaluate \_preprocess\_ctx(ctx).
- Set for\_validate from parse\_json(for\_validate).
- Set overwrite\_warehouse from parse\_json(overwrite\_warehouse).
- Set item from Platform.get\_cached\_doc(“Item”, ctx.item\_code).
- Set is\_portal\_quotation from (isinstance(doc, Document) and doc.doctype equals “Supplier Quotation” and doc.flags.ignore\_permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(doc, Document) → doc.doctype equals “Supplier Quotation” → doc.flags.ignore\_permissions.
- If not is\_portal\_quotation.
  - Evaluate item.check\_permission().
- Evaluate validate\_item\_details(ctx, item).
- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- If doc.
  - Set ctx.transaction\_date from (doc.get(“transaction\_date”) or doc.get(“posting\_date”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“transaction\_date”) → doc.get(“posting\_date”).
  - If doc.get(“doctype”) equals “Purchase Invoice”.
    - Set ctx.bill\_date from doc.get(“bill\_date”).
- Set out from get\_basic\_details(ctx, item, overwrite\_warehouse).
- Evaluate get\_item\_tax\_template(ctx, item, out).
- Set out.item\_tax\_rate from \_get\_item\_tax\_map(doc = (doc or ctx), tax\_template = (out.item\_tax\_template or ctx.item\_tax\_template), as\_json = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → ctx.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in out.item\_tax\_template → ctx.item\_tax\_template.
- Evaluate get\_party\_item\_code(ctx, item, out).
- If ctx.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Evaluate get\_tax\_withholding\_category(ctx, item, out).
- If ctx.doctype belongs to list(“Sales Order”, “Quotation”).
  - Evaluate set\_valuation\_rate(out, ctx).
- Evaluate update\_party\_blanket\_order(ctx, out).
- Set current\_customer from ctx.customer.
- If ctx.doctype belongs to list(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”).
  - Set ctx.customer from no value.
- Set source\_row from get\_rate\_locked\_source\_row(ctx, doc).
- If source\_row.
  - Evaluate lock\_source\_rate(out, source\_row).
- Otherwise.
  - Evaluate out.update(get\_price\_list\_rate(ctx, item)).
  - If (not out.price\_list\_rate and ctx.transaction\_type equals “selling” and Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not out.price\_list\_rate → ctx.transaction\_type equals “selling” → Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”).
    - Set fallback\_args from ctx.copy().
    - Set fallback\_args.price\_list from Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”).
    - Set fallback\_args.price\_list\_uom\_dependant from no value.
    - Evaluate out.update(get\_price\_list\_rate(fallback\_args, item)).
- Set ctx.customer from current\_customer.
- If (ctx.customer and cint(ctx.is\_pos)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.customer → cint(ctx.is\_pos).
  - Evaluate out.update(get\_pos\_profile\_item\_details\_(ctx, ctx.company, update\_data = true)).
- If item.is\_stock\_item.
  - Evaluate update\_bin\_details(ctx, out, doc).
- For each tuple(key, value) in out.items().
  - If ctx.get(key) is identical to no value.
    - Set ctx at key from value.
- If not ctx.price\_list\_rate.
  - Set ctx.price\_list\_rate from out.price\_list\_rate.
- If not source\_row.
  - Evaluate out.update(get\_pricing\_rule\_for\_item(ctx, doc = doc, for\_validate = for\_validate)).
- If (Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”) and not ctx.get(“serial\_and\_batch\_bundle”) and (ctx.get(“use\_serial\_batch\_fields”) or ctx.get(“doctype”) equa ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_single\_value(“Stock Settings”, “auto\_create\_serial\_and\_batch\_bundle\_for\_outward”) → not ctx.get(“serial\_and\_batch\_bundle”) → (ctx.get(“use\_serial\_batch\_fields”) or ctx.get(“doctype”) equals “POS Invoice”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.get(“use\_serial\_batch\_fields”) → ctx.get(“doctype”) equals “POS Invoice”.
  - Evaluate update\_stock(ctx, out, doc).
- If (ctx.transaction\_date and item.lead\_time\_days).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.transaction\_date → item.lead\_time\_days.
  - Set out.schedule\_date, out.lead\_time\_date from add\_days(ctx.transaction\_date, item.lead\_time\_days).
- If ctx.is\_subcontracted.
  - Set out.bom from (ctx.bom or get\_default\_bom(ctx.item\_code)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.bom → get\_default\_bom(ctx.item\_code).
- Evaluate get\_gross\_profit(out).
- If ctx.doctype equals “Material Request”.
  - Set out.rate from (ctx.rate or out.price\_list\_rate).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.rate → out.price\_list\_rate.
  - Set out.amount from (flt(ctx.qty) × flt(out.rate)).
- Set out from remove\_standard\_fields(out).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, ctx.item\_code), Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”) and 2 further calls · effective access from item.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L923)

<a id="op-fa905296394ec9"></a>
### Remove standard fields

`operation_enterprise_stock_get_item_details_business_behavior_remove_standard_fields`

**Inputs** out.

**Explicit results** out.

**Local steps**

- For each key in (child\_table\_fields + default\_fields).
  - Evaluate out.pop(key, no value).
- Return out.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L759)

<a id="op-876da5f54b00a2"></a>
### Has source doc permission

`operation_enterprise_binding_enterprise_stock_get_item_details_has_source_doc_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, docname, user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L936)

<a id="op-84a1074da4872f"></a>
### Get rate locked source row

`operation_enterprise_stock_get_item_details_business_behavior_get_rate_locked_source_row`

**Inputs** ctx, doc.

**Declared result** (Platform.\_dict bitwise or no value).

**Record and data access** read source\_doctype via get\_value.

**Explicit results** no value · source.

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- Set source\_fields from maintain\_same\_rate\_source\_fields.get((ctx.parenttype or ctx.doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.parenttype → ctx.doctype.
- If (not source\_fields or not doc or ctx.get(“is\_return”) or not maintain\_same\_rate\_enabled(ctx)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not source\_fields → not doc → ctx.get(“is\_return”) → not maintain\_same\_rate\_enabled(ctx).
  - Return no value.
- Set row from next(generator of d for d drawn from (doc.get(“items”) or list()) where d.get(“name”) equals ctx.child\_docname, no value) when ctx.child\_docname, otherwise ctx.
  - Value choice on ctx.child\_docname — true gives next(generator of d for d drawn from (doc.get(“items”) or list()) where d.get(“name”) equals ctx.child\_docname, no value), false gives ctx.
  - Draw d from (doc.get(“items”) or list()), keep a combination only if (d.get(“name”) equals ctx.child\_docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“items”) → list().
- If not row.
  - Return no value.
- For each tuple(link\_field, source\_doctype) in source\_fields.items().
  - If source\_name bound to row.get(link\_field).
    - Set source from Platform.db.get\_value(source\_doctype, source\_name, list(expanded LOCKED\_RATE\_FIELDS, “parent”, “parenttype”), as\_dict = true).
    - If (source and has\_source\_doc\_permission(source.parenttype, source.parent, Platform.session.user)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in source → has\_source\_doc\_permission(source.parenttype, source.parent, Platform.session.user).
      - Return source.
    - Return no value.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L749)

<a id="op-cbfa6e82d29982"></a>
### Maintain same rate enabled

`operation_enterprise_stock_get_item_details_business_behavior_maintain_same_rate_enabled`

**Inputs** ctx.

**Declared result** bool.

**Record and data access** read “Buying Settings” via get\_cached\_value · read “Selling Settings” via get\_cached\_value.

**Explicit results** false · bool(cint(Platform.get\_cached\_value(“Buying Settings”, “Buying Settings”, “maintain\_same\_rate”))) · bool(cint(Platform.get\_cached\_value(“Selling Settings”, “Selling Settings”, “maintain\_same\_sales\_rate”))).

**Local steps**

- If (ctx.parenttype or ctx.doctype) belongs to purchase\_doctypes.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.parenttype → ctx.doctype.
  - If ctx.get(“is\_internal\_supplier”).
    - Return false.
  - Return bool(cint(Platform.get\_cached\_value(“Buying Settings”, “Buying Settings”, “maintain\_same\_rate”))).
- If ctx.get(“is\_internal\_customer”).
  - Return false.
- Return bool(cint(Platform.get\_cached\_value(“Selling Settings”, “Selling Settings”, “maintain\_same\_sales\_rate”))).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Buying Settings”, “Buying Settings”, “maintain\_same\_rate”), Platform.get\_cached\_value(“Selling Settings”, “Selling Settings”, “maintain\_same\_sales\_rate”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L757)

<a id="op-49c04e4c998d08"></a>
### Lock source rate

`operation_enterprise_stock_get_item_details_business_behavior_dependency_lock_source_rate`

**Inputs** out, source\_row.

**Declared result** no value.

**Local steps**

- Set out.price\_list\_rate from (flt(source\_row.get(“price\_list\_rate”)) or flt(source\_row.get(“rate”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(source\_row.get(“price\_list\_rate”)) → flt(source\_row.get(“rate”)).
- Set out.rate from flt(source\_row.get(“rate”)).
- Set out.discount\_percentage from flt(source\_row.get(“discount\_percentage”)).
- Set out.discount\_amount from flt(source\_row.get(“discount\_amount”)).
- Set out.margin\_type from source\_row.get(“margin\_type”).
- Set out.margin\_rate\_or\_amount from flt(source\_row.get(“margin\_rate\_or\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0879.json#L3465) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1170) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L710)

<a id="op-76fa163dae5657"></a>
### Set valuation rate

`operation_enterprise_stock_get_item_details_business_behavior_set_valuation_rate`

**Inputs** out, ctx.

**Record and data access** read “Product Bundle” via exists · resolve a document from “Product Bundle” via get\_doc.

**Local steps**

- If Platform.db.exists(“Product Bundle”, mapping(“name” → ctx.item\_code, “disabled” → 0), cache = true).
  - Set valuation\_rate from 0.0.
  - Set bundled\_items from Platform.get\_doc(“Product Bundle”, ctx.item\_code).
  - For each bundle\_item in bundled\_items.items.
    - Update valuation\_rate using + flt((\_get\_valuation\_rate(bundle\_item.item\_code, ctx.company, nested operand in the contract.get(“warehouse”)).get(“valuation\_rate”) × bundle\_item.qty)).
  - Evaluate out.update(mapping(“valuation\_rate” → valuation\_rate)).
- Otherwise.
  - Evaluate out.update(\_get\_valuation\_rate(ctx.item\_code, ctx.company, out.get(“warehouse”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L760)

<a id="op-42aa20d48cbd73"></a>
### Update stock

`operation_enterprise_stock_get_item_details_business_behavior_update_stock`

**Inputs** ctx, out, doc = no value.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If ((ctx.get(“doctype”) belongs to list(“Delivery Note”, “POS Invoice”) or (ctx.get(“doctype”) equals “Sales Invoice” and ctx.get(“update\_stock”))) and out.warehouse and out.stock\_qty &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (ctx.get(“doctype”) belongs to list(“Delivery Note”, “POS Invoice”) or (ctx.get(“doctype”) equals “Sales Invoice” and ctx.get(“update\_stock”))) → out.warehouse → out.stock\_qty &gt; 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.get(“doctype”) belongs to list(“Delivery Note”, “POS Invoice”) → (ctx.get(“doctype”) equals “Sales Invoice” and ctx.get(“update\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“doctype”) equals “Sales Invoice” → ctx.get(“update\_stock”).
  - If (doc and isinstance(doc, dict)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → isinstance(doc, dict).
    - Set doc from Platform.\_dict(doc).
  - Set out.stock\_qty from flt(out.stock\_qty, Platform.get\_precision(formatted text {ctx.doctype} Item, “stock\_qty”)).
  - Set kwargs from Platform.\_dict(mapping(“item\_code” → ctx.item\_code, “warehouse” → ctx.warehouse, “based\_on” → Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”), “sabb\_voucher\_no” → doc.get(“nam ….
    - Value choice on doc — true gives doc.get(“name”), false gives no value.
  - If ctx.get(“doctype”) equals “Delivery Note”.
    - Set kwargs at “against\_sales\_order” from ctx.get(“against\_sales\_order”).
  - Otherwise.
    - If ctx.get(“doctype”) equals “Sales Invoice”.
      - Set kwargs at “against\_sales\_order” from ctx.get(“sales\_order”).
  - If ctx.get(“ignore\_serial\_nos”).
    - Set kwargs at “ignore\_serial\_nos” from ctx.get(“ignore\_serial\_nos”).
  - If (out.has\_batch\_no and not ctx.get(“batch\_no”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in out.has\_batch\_no → not ctx.get(“batch\_no”).
    - Set batch\_no from get\_batch\_no\_covering\_qty(kwargs, doc, out.stock\_qty).
    - If batch\_no.
      - Evaluate out.update(mapping(“batch\_no” → batch\_no, “actual\_batch\_qty” → out.stock\_qty)).
      - Set rate from \_get\_batch\_based\_item\_price(mapping(“price\_list” → doc.get(“selling\_price\_list”), “uom” → out.uom, “batch\_no” → batch\_no), out.item\_code).
      - If rate.
        - Evaluate out.update(mapping(“rate” → rate, “price\_list\_rate” → rate)).
  - If (out.has\_serial\_no and needs\_serial\_nos(ctx, out)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in out.has\_serial\_no → needs\_serial\_nos(ctx, out).
    - Evaluate set\_serial\_nos\_for\_outward(ctx, out, kwargs, doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “pick\_serial\_and\_batch\_based\_on”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L764)

<a id="op-b04e4b1b65d077"></a>
### Needs serial nos

`operation_enterprise_binding_enterprise_stock_get_item_details_needs_serial_nos`

**Inputs** ctx, out.

**Explicit results** not ctx.get(“serial\_no”) · false · has\_incorrect\_serial\_nos(ctx, out).

**Local steps**

- If not out.has\_batch\_no.
  - Return not ctx.get(“serial\_no”).
- If ctx.get(“use\_serial\_batch\_fields”).
  - Return false.
- Return has\_incorrect\_serial\_nos(ctx, out).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L937)

<a id="op-68a86690de1b8a"></a>
### Set serial nos for outward

`operation_enterprise_binding_enterprise_stock_get_item_details_set_serial_nos_for_outward`

**Inputs** ctx, out, kwargs, doc.

**Local steps**

- Bind dependencies get\_serial\_nos\_for\_outward.
- Set batch\_no from (ctx.get(“batch\_no”) or out.get(“batch\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.get(“batch\_no”) → out.get(“batch\_no”).
- If (out.has\_batch\_no and batch\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in out.has\_batch\_no → batch\_no.
  - Set kwargs at “batches” from list(batch\_no).
- Set kwargs at “ignore\_serial\_nos” from list(expanded (kwargs.get(“ignore\_serial\_nos”) or list()), expanded get\_used\_serial\_nos(doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“ignore\_serial\_nos”) → list().
- Set serial\_nos from get\_serial\_nos\_for\_outward(kwargs).
- Set out at “serial\_no” from whitespace '\\n'.join(serial\_nos at slice no value to cint(out.stock\_qty)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L939)

<a id="op-11d64584c2b02a"></a>
### Has incorrect serial nos

`operation_enterprise_stock_get_item_details_business_behavior_has_incorrect_serial_numbers`

**Inputs** ctx, out.

**Explicit results** true · false.

**Local steps**

- Bind dependencies get\_serial\_nos.
- If not ctx.get(“serial\_no”).
  - Return true.
- Set serial\_nos from get\_serial\_nos(ctx.get(“serial\_no”)).
- If len(serial\_nos) differs from out.get(“stock\_qty”).
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0879.json#L5675) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L754)

<a id="op-1ebb21459d7aea"></a>
### Get batch no covering qty

`operation_enterprise_stock_get_item_details_business_behavior_get_batch_number_covering_quantity`

**Inputs** kwargs, doc, qty.

**Explicit results** batch\_no · no value.

**Local steps**

- Bind dependencies get\_available\_batches.
- Set batches from get\_available\_batches(Platform.\_dict(kwargs, qty = 0)).
- If doc.
  - Evaluate filter\_batches(batches, doc, kwargs.item\_code, kwargs.warehouse).
- Set batch\_no from next(iter(batches), no value).
- If (batch\_no and flt(batches at batch\_no) ≥ flt(qty, Platform.get\_precision(“Serial and Batch Entry”, “qty”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no → flt(batches at batch\_no) ≥ flt(qty, Platform.get\_precision(“Serial and Batch Entry”, “qty”)).
  - Return batch\_no.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L715)

<a id="op-87b8ee1f36ee67"></a>
### Filter batches

`operation_enterprise_stock_get_item_details_business_behavior_filter_batches`

**Inputs** batches, doc, item\_code, warehouse.

**Local steps**

- Set precision from Platform.get\_precision(“Serial and Batch Entry”, “qty”).
- For each tuple(batch\_no, stock\_qty) in get\_batch\_qty\_taken\_by\_rows(doc, item\_code, warehouse).
  - If batch\_no belongs to batches.
    - Set batches at batch\_no from flt((batches at batch\_no − flt(stock\_qty, precision)), precision).
    - If batches at batch\_no ≤ 0.
      - Remove batches at batch\_no.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1171) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L711)

<a id="op-71c8901f659766"></a>
### Get batch qty taken by rows

`operation_enterprise_binding_enterprise_stock_get_item_details_get_batch_qty_taken_by_rows`

**Inputs** doc, item\_code, warehouse.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** taken.

**Local steps**

- Set rows from list of row for row drawn from list(expanded doc.get(“items”), expanded (doc.get(“packed\_items”) or list())) where row.get(“warehouse”) belongs to tuple(no value, empty text, warehouse).
  - Draw row from list(expanded doc.get(“items”), expanded (doc.get(“packed\_items”) or list())), keep a combination only if (row.get(“warehouse”) belongs to tuple(no value, empty text, warehouse)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“packed\_items”) → list().
- Set taken from list of tuple(row.get(“batch\_no”), get\_row\_stock\_qty(row, item\_code)) for row drawn from rows where row.get(“batch\_no”).
  - Draw row from rows, keep a combination only if (row.get(“batch\_no”)).
- Set bundles from list of row.get(“serial\_and\_batch\_bundle”) for row drawn from rows where (not row.get(“batch\_no”) and row.get(“serial\_and\_batch\_bundle”)).
  - Draw row from rows, keep a combination only if ((not row.get(“batch\_no”) and row.get(“serial\_and\_batch\_bundle”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.get(“batch\_no”) → row.get(“serial\_and\_batch\_bundle”).
- If bundles.
  - Set entries from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → list(“in”, bundles), “batch\_no” → list(“is”, “set”)), fields = list(“batch\_no”, “qty”)).
  - Evaluate taken.extend(generator of tuple(entry.batch\_no, abs(entry.qty)) for entry drawn from entries).
    - Draw entry from entries.
- Return taken.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1422) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L919)

<a id="op-d955f3d8ccbcdb"></a>
### Get row stock qty

`operation_enterprise_binding_enterprise_stock_get_item_details_get_row_stock_qty`

**Inputs** row, item\_code.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** flt(row.get(“qty”)) · (flt(row.get(“qty”)) × flt(conversion\_factor)).

**Local steps**

- Set item from Platform.get\_cached\_value(“Item”, item\_code, list(“stock\_uom”, “sales\_uom”), as\_dict = true).
- Set uom from (row.get(“uom”) or item.sales\_uom or item.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“uom”) → item.sales\_uom → item.stock\_uom.
- If uom equals item.stock\_uom.
  - Return flt(row.get(“qty”)).
- Set conversion\_factor from (row.get(“conversion\_factor”) or get\_uom\_conversion\_factor(item\_code, uom)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“conversion\_factor”) → get\_uom\_conversion\_factor(item\_code, uom).
- Return (flt(row.get(“qty”)) × flt(conversion\_factor)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item\_code, list(“stock\_uom”, “sales\_uom”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L932)

<a id="op-07e4cea999c648"></a>
### Get uom conversion factor

`operation_enterprise_binding_enterprise_stock_get_item_details_get_uom_conversion_factor`

**Inputs** item\_code, uom.

**Wrappers, in declaration order** Platform.request\_cache.

**Explicit results** get\_conversion\_factor(item\_code, uom) at “conversion\_factor”.

**Local steps**

- Return get\_conversion\_factor(item\_code, uom) at “conversion\_factor”.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L933)

<a id="op-9e94e1a935d952"></a>
### Get filtered serial nos

`operation_enterprise_stock_get_item_details_business_behavior_get_filtered_serial_numbers`

**Inputs** serial\_nos, doc, table = no value.

**Explicit results** list of serial\_no for serial\_no drawn from serial\_nos where serial\_no does not belong to used.

**Local steps**

- Set used from get\_used\_serial\_nos(doc, table).
- Return list of serial\_no for serial\_no drawn from serial\_nos where serial\_no does not belong to used.
  - Draw serial\_no from serial\_nos, keep a combination only if (serial\_no does not belong to used).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L730)

<a id="op-590b3af8824441"></a>
### Get used serial nos

`operation_enterprise_binding_enterprise_stock_get_item_details_get_used_serial_nos`

**Inputs** doc, table = no value.

**Explicit results** used.

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set rows from doc.get(table) when table, otherwise list(expanded doc.get(“items”), expanded (doc.get(“packed\_items”) or list())).
  - Value choice on table — true gives doc.get(table), false gives list(expanded doc.get(“items”), expanded (doc.get(“packed\_items”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“packed\_items”) → list().
- Set used from set().
- For each row in rows.
  - If row.get(“serial\_no”).
    - Evaluate used.update(get\_serial\_nos(row.get(“serial\_no”))).
- Return used.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L934)

<a id="op-e0738ae8397ae1"></a>
### Update bin details

`operation_enterprise_stock_get_item_details_business_behavior_update_bin_details`

**Inputs** ctx, out, doc.

**Local steps**

- If (ctx.doctype equals “Material Request” and ctx.material\_request\_type equals “Material Transfer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.doctype equals “Material Request” → ctx.material\_request\_type equals “Material Transfer”.
  - Evaluate out.update(\_get\_bin\_details(ctx.item\_code, ctx.from\_warehouse)).
- Otherwise.
  - If out.get(“warehouse”).
    - Set bin\_details from \_get\_bin\_details(ctx.item\_code, out.warehouse, ctx.company, include\_child\_warehouses = true).
    - Evaluate out.update(bin\_details).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L762)
