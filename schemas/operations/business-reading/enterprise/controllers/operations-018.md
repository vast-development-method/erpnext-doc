# Shared transaction rules · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Sales and purchase return

<a id="op-b64aef50479dac"></a>
### Validate returned items

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_validate_returned_items`

**Inputs** doc.

**Record and data access** execute query text (SELECT, Packed Item) · read “Item” via get\_value.

**State and service calls** execute a supplied database query · msgprint with translated “Row # {0}: Returned Item {1} does not exist in {2} {3}”.format(d.idx, d.item\_code, doc.doctype, doc.return\_against).

**Explicit failure paths** validation helper — translated “Row # {0}: Rate cannot be greater than the rate used in {1} {2}”.format(d.idx, doc.doctype, doc.return\_against) · validation helper — translated “Warehouse is mandatory” · validation helper — translated “At least one item should be entered with negative quantity in return document”.

**Local steps**

- Set valid\_items from Platform.\_dict().
- Set select\_fields from “item\_code, qty, rate, parenttype, conversion\_factor, name”.
- If doc.doctype differs from “Subcontracting Receipt”.
  - Update select\_fields using + “, stock\_qty”.
- If doc.doctype differs from “Purchase Invoice”.
  - Update select\_fields using + “,serial\_no, batch\_no”.
- If doc.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
  - Update select\_fields using + “,rejected\_qty, received\_qty”.
- For each d in Platform.db.sql(formatted text select {select\_fields} from ′tab{doc.doctype} Item′ where parent = %s, doc.return\_against, as\_dict = 1).
  - If doc.doctype equals “Subcontracting Receipt”.
    - Set d.stock\_qty from (flt(d.qty) × flt((d.conversion\_factor or 1))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.conversion\_factor → 1.
  - Set valid\_items from get\_ref\_item\_dict(valid\_items, d).
  - If doc.doctype equals “Delivery Note”.
    - Set valid\_items from get\_ref\_item\_dict(valid\_items, Platform.\_dict(d, name = no value)).
- If doc.doctype belongs to tuple(“Delivery Note”, “Sales Invoice”).
  - For each d in Platform.db.sql(query text (SELECT, Packed Item), doc.return\_against, as\_dict = 1).
    - Set valid\_items from get\_ref\_item\_dict(valid\_items, Platform.\_dict(d, stock\_qty = d.qty)).
- Set already\_returned\_items from get\_already\_returned\_items(doc).
- Set warehouse\_mandatory from not ((doc.doctype equals “Purchase Invoice” or doc.doctype equals “Sales Invoice”) and not doc.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (doc.doctype equals “Purchase Invoice” or doc.doctype equals “Sales Invoice”) → not doc.update\_stock.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype equals “Purchase Invoice” → doc.doctype equals “Sales Invoice”.
- Set items\_returned from false.
- For each d in doc.get(“items”).
  - Set key from d.item\_code.
  - Set raise\_exception from false.
  - If doc.doctype belongs to ROW\_REFERENCE\_DOCTYPES.
    - Set field from (Platform.scrub(doc.doctype) + “\_item”).
    - If d.get(field).
      - Set key from tuple(d.item\_code, d.get(field)).
      - Set raise\_exception from true.
  - Otherwise.
    - If doc.doctype equals “Delivery Note”.
      - Set key from tuple(d.item\_code, d.dn\_detail) when d.get(“dn\_detail”), otherwise d.item\_code.
        - Value choice on d.get(“dn\_detail”) — true gives tuple(d.item\_code, d.dn\_detail), false gives d.item\_code.
      - Set raise\_exception from true.
  - If (d.item\_code and (flt(d.qty) ≤ 0 or flt(d.get(“received\_qty”)) ≤ 0)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code → (flt(d.qty) ≤ 0 or flt(d.get(“received\_qty”)) ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.qty) ≤ 0 → flt(d.get(“received\_qty”)) ≤ 0.
    - If key does not belong to valid\_items.
      - Evaluate Platform.msgprint(translated “Row # {0}: Returned Item {1} does not exist in {2} {3}”.format(d.idx, d.item\_code, doc.doctype, doc.return\_against), raise\_exception = raise\_exception).
    - Otherwise.
      - Set ref from valid\_items.get(key, Platform.\_dict()).
      - Evaluate validate\_quantity(doc, key, d, ref, …).
      - If doc.doctype equals “Delivery Note”.
        - Evaluate validate\_delivery\_note\_item\_qty(doc, key, d, valid\_items, …).
      - If (ref.rate and flt(d.rate) &gt; ref.rate and doc.doctype belongs to tuple(“Delivery Note”, “Sales Invoice”) and get\_valuation\_method(d.item\_code, doc.company) differs from “Moving Average”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref.rate → flt(d.rate) &gt; ref.rate → doc.doctype belongs to tuple(“Delivery Note”, “Sales Invoice”) → get\_valuation\_method(d.item\_code, doc.company) differs from “Moving Average”.
        - Call the validation error handler Platform.throw(translated “Row # {0}: Rate cannot be greater than the rate used in {1} {2}”.format(d.idx, doc.doctype, doc.return\_against)).
      - If (warehouse\_mandatory and not d.get(“warehouse”) and Platform.db.get\_value(“Item”, d.item\_code, “is\_stock\_item”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse\_mandatory → not d.get(“warehouse”) → Platform.db.get\_value(“Item”, d.item\_code, “is\_stock\_item”).
        - Call the validation error handler Platform.throw(translated “Warehouse is mandatory”).
    - If doc.doctype belongs to tuple(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”, “Sales Invoice”, …).
      - If (flt(d.qty) &lt; 0 or flt(d.get(“received\_qty”)) &lt; 0 or flt(d.get(“rejected\_qty”)) &lt; 0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.qty) &lt; 0 → flt(d.get(“received\_qty”)) &lt; 0 → flt(d.get(“rejected\_qty”)) &lt; 0.
        - Set items\_returned from true.
    - Otherwise.
      - Set items\_returned from true.
  - Otherwise.
    - If d.item\_name.
      - If doc.doctype belongs to tuple(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
        - If flt(d.qty) &lt; 0.
          - Set items\_returned from true.
      - Otherwise.
        - Set items\_returned from true.
- If not items\_returned.
  - Call the validation error handler Platform.throw(translated “At least one item should be entered with negative quantity in return document”).
- If doc.doctype equals “Delivery Note”.
  - Evaluate validate\_returned\_bundle\_components(doc, valid\_items, already\_returned\_items).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L868) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L549)

<a id="op-c7e36d7e7686ad"></a>
### Validate returned bundle components

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_validate_returned_bundle_components`

**Inputs** doc, valid\_items, already\_returned\_items.

**Record and data access** read “Product Bundle” via get\_all · read “Stock Settings” via get\_single\_value · read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper with StockOverReturnError — translated “Row # {0}: Cannot return {1}, only {2} {3} of its component {4} is left to return”.format(row.idx, Platform.bold(row.item\_code), flt(remaining, row.precision(“stock\_qty”)), Platform.get\_cached\_ ….

**Local steps**

- Bind dependencies get\_component\_order\_rows, get\_component\_stock\_qty\_per\_unit, get\_order\_packed\_items, get\_order\_row, get\_product\_bundle\_items.
- Set returned\_rows from list of row for row drawn from doc.get(“items”) where (row.item\_code and flt(row.qty) &lt; 0).
  - Draw row from doc.get(“items”), keep a combination only if ((row.item\_code and flt(row.qty) &lt; 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → flt(row.qty) &lt; 0.
- Set bundle\_items from set(Platform.get\_all(“Product Bundle”, filters = mapping(“new\_item\_code” → list(“in”, list of row.item\_code for row drawn from returned\_rows), “disabled” → 0), pluck = “new\_item\_code”)).
  - Draw row from returned\_rows.
- Set order\_packed\_items from get\_order\_packed\_items(doc).
- Set components from mapping().
- For each row in returned\_rows.
  - If row.item\_code does not belong to bundle\_items.
    - Continue with the next iteration or loop test.
  - If row.item\_code does not belong to components.
    - Set components at row.item\_code from get\_product\_bundle\_items(row.item\_code).
  - Set bundle\_stock\_qty from abs((flt(row.qty) × flt((row.conversion\_factor or 1)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.conversion\_factor → 1.
  - If Platform.db.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_sales”).
    - Set bundle\_stock\_qty from flt(bundle\_stock\_qty, row.precision(“stock\_qty”)).
  - Set so\_packed\_items from list(order\_packed\_items.get(get\_order\_row(doc, row), list())).
  - For each tuple(component, so\_packed\_item) in get\_component\_order\_rows(doc, row.item\_code, components at row.item\_code, so\_packed\_items).
    - Set ref from valid\_items.get(component.item\_code).
    - If not ref.
      - Continue with the next iteration or loop test.
    - Set returned from already\_returned\_items.setdefault(component.item\_code, Platform.\_dict(qty = 0, stock\_qty = 0)).
    - Set remaining from (flt(ref.stock\_qty) − flt(returned.stock\_qty)).
    - Set component\_stock\_qty from get\_component\_stock\_qty\_per\_unit(component, no value, so\_packed\_item).
    - Set returned.stock\_qty from (flt(returned.stock\_qty) + (bundle\_stock\_qty × component\_stock\_qty)).
    - If flt(returned.stock\_qty, row.precision(“stock\_qty”)) &gt; flt(ref.stock\_qty, row.precision(“stock\_qty”)).
      - Call the validation error handler Platform.throw(translated “Row # {0}: Cannot return {1}, only {2} {3} of its component {4} is left to return”.format(row.idx, Platform.bold(row.item\_code), flt(remaining, row.precision(“stock\_qty”)), Platf ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_sales”), Platform.get\_cached\_value(“Item”, component.item\_code, “stock\_uom”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1099) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L339)

<a id="op-8316fe9e49df38"></a>
### Validate quantity

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_validate_quantity`

**Inputs** doc, key, args, ref, valid\_items, already\_returned\_items.

**Explicit failure paths** validation helper — translated “{0} must be negative in return document”.format(label) · validation helper with StockOverReturnError — translated “Item {0} has already been returned”.format(args.item\_code) · validation helper with StockOverReturnError — translated “Row # {0}: Cannot return more than {1} for Item {2}”.format(args.idx, max\_returnable\_qty, args.item\_code).

**Local steps**

- Set fields from list(“stock\_qty”).
- If ((doc.doctype equals “Purchase Invoice” or doc.doctype equals “Sales Invoice”) and not doc.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (doc.doctype equals “Purchase Invoice” or doc.doctype equals “Sales Invoice”) → not doc.update\_stock.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype equals “Purchase Invoice” → doc.doctype equals “Sales Invoice”.
  - Set fields from list(“qty”).
- Set tracks\_accepted\_rejected\_split from (doc.doctype belongs to tuple(“Purchase Receipt”, “Subcontracting Receipt”) or (doc.doctype equals “Purchase Invoice” and doc.update\_stock)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype belongs to tuple(“Purchase Receipt”, “Subcontracting Receipt”) → (doc.doctype equals “Purchase Invoice” and doc.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Purchase Invoice” → doc.update\_stock.
- If tracks\_accepted\_rejected\_split.
  - If not args.get(“return\_qty\_from\_rejected\_warehouse”).
    - Evaluate fields.extend(list(“received\_qty”, “rejected\_qty”)).
  - Otherwise.
    - Evaluate fields.extend(list(“received\_qty”)).
- Set already\_returned\_data from (already\_returned\_items.get(key) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in already\_returned\_items.get(key) → mapping().
- Set returns\_nothing from not (flt(args.get(“qty”)) or flt(args.get(“rejected\_qty”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(args.get(“qty”)) → flt(args.get(“rejected\_qty”)).
- Set company\_currency from Enterprise.get\_company\_currency(doc.company).
- Set field\_precision from get\_field\_precision(Platform.get\_meta((doc.doctype + “ Item”)).get\_field(“stock\_qty” when doc.get(“update\_stock”, empty text), otherwise “qty”), currency = company\_currency).
  - Value choice on doc.get(“update\_stock”, empty text) — true gives “stock\_qty”, false gives “qty”.
- For each column in fields.
  - Set returned\_column from column.
  - If (args.get(“return\_qty\_from\_rejected\_warehouse”) and doc.doctype belongs to REJECTED\_WAREHOUSE\_RETURN\_DOCTYPES).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“return\_qty\_from\_rejected\_warehouse”) → doc.doctype belongs to REJECTED\_WAREHOUSE\_RETURN\_DOCTYPES.
    - Set returned\_column from “rejected\_qty”.
  - Set returned\_qty from flt(already\_returned\_data.get(returned\_column, 0), field\_precision) when len(already\_returned\_data) &gt; 0, otherwise 0.
    - Value choice on len(already\_returned\_data) &gt; 0 — true gives flt(already\_returned\_data.get(returned\_column, 0), field\_precision), false gives 0.
  - If (column belongs to tuple(“stock\_qty”, “qty”) and not args.get(“return\_qty\_from\_rejected\_warehouse”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in column belongs to tuple(“stock\_qty”, “qty”) → not args.get(“return\_qty\_from\_rejected\_warehouse”).
    - Set reference\_qty from ref.get(column).
    - Set current\_stock\_qty from args.get(column).
    - If column equals “stock\_qty”.
      - Set current\_stock\_qty from (flt(args.get(“qty”)) × flt((args.get(“conversion\_factor”) or 1))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“conversion\_factor”) → 1.
  - Otherwise.
    - If args.get(“return\_qty\_from\_rejected\_warehouse”).
      - Set reference\_qty from (ref.get(“rejected\_qty”) × ref.get(“conversion\_factor”, 1.0)).
      - Set current\_stock\_qty from (args.get(column) × args.get(“conversion\_factor”, 1.0)) when column differs from “stock\_qty”, otherwise (flt(args.get(“qty”)) × flt((args.get(“conversion\_factor”) or 1))).
        - Value choice on column differs from “stock\_qty” — true gives (args.get(column) × args.get(“conversion\_factor”, 1.0)), false gives (flt(args.get(“qty”)) × flt((args.get(“conversion\_factor”) or 1))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“conversion\_factor”) → 1.
    - Otherwise.
      - Set reference\_qty from (ref.get(column) × ref.get(“conversion\_factor”, 1.0)).
      - Set current\_stock\_qty from (flt(args.get(column)) × args.get(“conversion\_factor”, 1.0)).
  - Set max\_returnable\_qty from flt((flt(reference\_qty, field\_precision) − returned\_qty), field\_precision).
  - Set label from column.replace(“\_”, one space).title().
  - If (reference\_qty or flt(current\_stock\_qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_qty → flt(current\_stock\_qty).
    - If flt(current\_stock\_qty) &gt; 0.
      - Call the validation error handler Platform.throw(translated “{0} must be negative in return document”.format(label)).
    - Otherwise.
      - If (returned\_qty ≥ reference\_qty and returns\_nothing).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in returned\_qty ≥ reference\_qty → returns\_nothing.
        - Call the validation error handler Platform.throw(translated “Item {0} has already been returned”.format(args.item\_code), StockOverReturnError).
      - Otherwise.
        - If abs(flt(current\_stock\_qty, field\_precision)) &gt; max\_returnable\_qty.
          - Call the validation error handler Platform.throw(translated “Row # {0}: Cannot return more than {1} for Item {2}”.format(args.idx, max\_returnable\_qty, args.item\_code), StockOverReturnError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L546)

<a id="op-34648326c148e9"></a>
### Validate delivery note item qty

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_validate_delivery_note_item_qty`

**Inputs** doc, key, row, valid\_items, already\_returned\_items.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Local steps**

- If key differs from row.item\_code.
  - Set ref from valid\_items at row.item\_code.
  - Evaluate validate\_quantity(doc, row.item\_code, row, ref, …).
- Set stock\_qty from abs((flt(row.qty) × flt((row.conversion\_factor or 1)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.conversion\_factor → 1.
- If Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_sales”).
  - Set stock\_qty from flt(stock\_qty, row.precision(“stock\_qty”)).
- For each returned\_key in set(key, row.item\_code).
  - Set returned from already\_returned\_items.setdefault(returned\_key, Platform.\_dict(qty = 0, stock\_qty = 0)).
  - Set returned.qty from (flt(returned.qty) + abs(flt(row.qty))).
  - Set returned.stock\_qty from (flt(returned.stock\_qty) + stock\_qty).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_sales”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1097) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L337)

<a id="op-7acc540fdd152a"></a>
### Get ref item dict

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_reference_item_mapping`

**Inputs** valid\_items, ref\_item\_row.

**Explicit results** valid\_items.

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set key from ref\_item\_row.item\_code.
- If ref\_item\_row.get(“name”).
  - Set key from tuple(ref\_item\_row.item\_code, ref\_item\_row.name).
- Evaluate valid\_items.setdefault(key, Platform.\_dict(mapping(“qty” → 0, “rate” → 0, “stock\_qty” → 0, “rejected\_qty” → 0, …))).
- Set item\_dict from valid\_items at key.
- Update item\_dict at “qty” using + ref\_item\_row.qty.
- Update item\_dict at “stock\_qty” using + ref\_item\_row.get(“stock\_qty”, 0).
- If ref\_item\_row.get(“rate”, 0) &gt; item\_dict at “rate”.
  - Set item\_dict at “rate” from ref\_item\_row.get(“rate”, 0).
- If ref\_item\_row.parenttype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
  - Update item\_dict at “received\_qty” using + ref\_item\_row.received\_qty.
  - Update item\_dict at “rejected\_qty” using + ref\_item\_row.rejected\_qty.
- If ref\_item\_row.get(“serial\_no”).
  - Update item\_dict at “serial\_no” using + get\_serial\_nos(ref\_item\_row.serial\_no).
- If ref\_item\_row.get(“batch\_no”).
  - Evaluate item\_dict at “batch\_no”.append(ref\_item\_row.batch\_no).
- Return valid\_items.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0381.json#L6034) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L845) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L526)

<a id="op-7171768dcf5c6d"></a>
### Get already returned items

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_already_returned_items`

**Inputs** doc.

**Explicit results** items.

**Local steps**

- Set child from DocType(formatted text {doc.doctype} Item).
- Set par from DocType(doc.doctype).
- Set field from (Platform.scrub(doc.doctype) + “\_item”) when doc.doctype belongs to ROW\_REFERENCE\_DOCTYPES, otherwise “dn\_detail”.
  - Value choice on doc.doctype belongs to ROW\_REFERENCE\_DOCTYPES — true gives (Platform.scrub(doc.doctype) + “\_item”), false gives “dn\_detail”.
- Set stock\_qty from Abs(child.stock\_qty).
- If doc.doctype equals “Subcontracting Receipt”.
  - Set stock\_qty from (Abs(child.qty) × child.conversion\_factor).
- Set rejected\_qty from (Abs(child.rejected\_qty) × child.conversion\_factor).
- If doc.doctype belongs to REJECTED\_WAREHOUSE\_RETURN\_DOCTYPES.
  - Set from\_rejected\_warehouse from child.return\_qty\_from\_rejected\_warehouse equals 1.
  - Update rejected\_qty using + Case().when(from\_rejected\_warehouse, stock\_qty).else\_(0).
  - Set stock\_qty from Case().when(from\_rejected\_warehouse, 0).else\_(stock\_qty).
- Set query from nested operand in the contract(nested operand in the contract).select(child.item\_code, nested operand in the contract.as\_(“qty”), nested operand in the contract.as\_(“stock\_qty”), child at field).where(((ne ….
- If doc.doctype belongs to list(“Purchase Invoice”, “Purchase Receipt”, “Subcontracting Receipt”).
  - Set query from query.select(Sum(rejected\_qty).as\_(“rejected\_qty”), Sum((Abs(nested operand in the contract.received\_qty) × child.conversion\_factor)).as\_(“received\_qty”)).
- Set data from query.run(as\_dict = 1).
- Set items from mapping().
- If doc.doctype equals “Delivery Note”.
  - For each d in (data + get\_returned\_packed\_items(doc.return\_against)).
    - Set item\_total from items.setdefault(d.item\_code, Platform.\_dict(qty = 0, stock\_qty = 0)).
    - Update item\_total.qty using + flt(d.qty).
    - Update item\_total.stock\_qty using + flt(d.stock\_qty).
- For each d in data.
  - Evaluate items.setdefault(tuple(d.item\_code, d.get(field)), Platform.\_dict(mapping(“qty” → d.get(“qty”), “stock\_qty” → d.get(“stock\_qty”), “received\_qty” → d.get(“received\_qty”), “rejected\_qty” → d.get(“rejected\_qty”)))).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L836) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L517)

<a id="op-16dd2811b27ae7"></a>
### Get returned packed items

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_get_returned_packed_items`

**Inputs** delivery\_note.

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….

**Local steps**

- Set packed\_item from DocType(“Packed Item”).
- Set parent from DocType(“Delivery Note”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1091) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L331)

<a id="op-05efccbf95b043"></a>
### Get returned qty map for purchase flow

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_returned_quantity_map_for_purchase_flow`

**Inputs** return\_against, supplier, row\_name, doctype.

**Explicit results** \_return\_map.

**Local steps**

- Set parent\_doc from Platform.qb.DocType(doctype).
- Set child\_doc from Platform.qb.DocType((doctype + “ Item”)).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(child\_doc.qty, child\_doc.rejected\_qty, child\_doc.w ….
- If doctype differs from “Subcontracting Receipt”.
  - Set query from query.select(child\_doc.stock\_qty).
- Set doctype\_field\_map from mapping(“Purchase Receipt” → child\_doc.purchase\_receipt\_item, “Subcontracting Receipt” → child\_doc.subcontracting\_receipt\_item).
- Set field from doctype\_field\_map.get(doctype).
- If field.
  - Set query from query.where(field equals row\_name).
- Set data from query.run(as\_dict = true).
- Set \_return\_map from Platform.\_dict(mapping()).
- For each row in data.
  - If (row.warehouse and row.warehouse does not belong to \_return\_map).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.warehouse → row.warehouse does not belong to \_return\_map.
    - Set \_return\_map at row.warehouse from Platform.\_dict(mapping(“qty” → 0, “stock\_qty” → 0)).
  - If (row.rejected\_warehouse and row.rejected\_warehouse does not belong to \_return\_map).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.rejected\_warehouse → row.rejected\_warehouse does not belong to \_return\_map.
    - Set \_return\_map at row.rejected\_warehouse from Platform.\_dict(mapping(“qty” → 0, “stock\_qty” → 0)).
  - If row.warehouse.
    - Set qty\_map from \_return\_map.get(row.warehouse).
    - Update qty\_map.qty using + abs(flt(row.qty)).
    - Update qty\_map.stock\_qty using + abs(flt(row.stock\_qty)).
  - If row.rejected\_warehouse.
    - Set rejected\_qty\_map from \_return\_map.get(row.rejected\_warehouse).
    - Update rejected\_qty\_map.qty using + abs(flt(row.rejected\_qty)).
    - Update rejected\_qty\_map.stock\_qty using + abs((flt(row.rejected\_qty) × flt(row.conversion\_factor))).
- Return \_return\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0382.json#L1060) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L848) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L529)

<a id="op-b09cee8e2671f8"></a>
### Get returned qty map for row

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_returned_quantity_map_for_row`

**Inputs** return\_against, party, row\_name, doctype.

**Record and data access** read doctype via get\_all.

**Explicit results** data at 0.

**Local steps**

- Set child\_doctype from (doctype + “ Item”).
- Set reference\_field from “dn\_detail” when doctype equals “Delivery Note”, otherwise Platform.scrub(child\_doctype).
  - Value choice on doctype equals “Delivery Note” — true gives “dn\_detail”, false gives Platform.scrub(child\_doctype).
- If doctype belongs to tuple(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”).
  - Set party\_type from “supplier”.
- Otherwise.
  - Set party\_type from “customer”.
- Set fields from list(mapping(“SUM” → list(mapping(“ABS” → formatted text ′tab{child\_doctype}′.qty)), “as” → “qty”)).
- If doctype differs from “Subcontracting Receipt”.
  - Update fields using + list(mapping(“SUM” → list(mapping(“ABS” → formatted text ′tab{child\_doctype}′.stock\_qty)), “as” → “stock\_qty”)).
- If doctype belongs to tuple(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”).
  - Update fields using + list(mapping(“SUM” → list(mapping(“ABS” → formatted text ′tab{child\_doctype}′.rejected\_qty)), “as” → “rejected\_qty”), mapping(“SUM” → list(mapping(“ABS” → formatted text ′tab{child\_doctype}′.received\_qty)) ….
  - If doctype equals “Purchase Receipt”.
    - Update fields using + list(mapping(“SUM” → list(mapping(“ABS” → formatted text ′tab{child\_doctype}′.received\_stock\_qty)), “as” → “received\_stock\_qty”)).
- Set data from Platform.get\_all(doctype, fields = fields, filters = list(list(doctype, “return\_against”, “=”, return\_against), list(doctype, party\_type, “=”, party), list(doctype, “docstatus”, “=”, 1), list(doctype, “is\_ ….
- Return data at 0.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0382.json#L2243) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L849) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L530)

<a id="op-86b4e09a5b434f"></a>
### Make return doc

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_return_record`

**Inputs** doctype, source\_name, target\_doc = no value, return\_against\_rejected\_qty = false.

**Record and data access** read doctype via get\_value · read “Company” via get\_cached\_value · read “Sales Invoice” via get\_value.

**Explicit results** doclist.

**Explicit failure paths** validation helper — translated “Cannot create return for consolidated invoice {0}.”.format(source\_name).

**Local steps**

- Bind dependencies get\_mapped\_doc.
- Set company from Platform.db.get\_value(doctype, source\_name, “company”).
- Set default\_warehouse\_for\_sales\_return from Platform.get\_cached\_value(“Company”, company, “default\_warehouse\_for\_sales\_return”).
- If doctype equals “Sales Invoice”.
  - Set tuple(inv\_is\_consolidated, inv\_is\_pos) from Platform.db.get\_value(“Sales Invoice”, source\_name, list(“is\_consolidated”, “is\_pos”)).
  - If (inv\_is\_consolidated and inv\_is\_pos).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in inv\_is\_consolidated → inv\_is\_pos.
    - Call the validation error handler Platform.throw(translated “Cannot create return for consolidated invoice {0}.”.format(source\_name), title = translated “Cannot Create Return”).
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_packed\_items for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation update\_non\_bundled\_serial\_nos for subsequent calls.
- Bind local operation get\_returned\_non\_bundled\_serial\_nos for subsequent calls.
- Bind local operation update\_terms for subsequent calls.
- Bind local operation item\_condition for subsequent calls.
- Set doclist from get\_mapped\_doc(doctype, source\_name, mapping(doctype → mapping(“doctype” → doctype, “validation” → mapping(“docstatus” → list(“=”, 1))), (doctype + “ Item”) → mapping(“doctype” → (doctype + “ Item”), “fiel ….
- Return doclist.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_warehouse\_for\_sales\_return”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L538)

<a id="op-d54fbd26d2a93f"></a>
### Make return doc.set missing values

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_return_record_set_missing_values`

**Inputs** source, target.

**Record and data access** resolve a document from target via get\_doc · read “Print Heading” via get\_cached\_value.

**Local steps**

- Set doc from Platform.get\_doc(target).
- Set doc.is\_return from 1.
- Set doc.ignore\_pricing\_rule from 1.
- Set doc.pricing\_rules from list().
- Set doc.return\_against from source.name.
- Set doc.set\_warehouse from empty text.
- If doctype equals “Sales Invoice”.
  - Set doc.is\_debit\_note from 0.
- If (doctype equals “Sales Invoice” or doctype equals “POS Invoice”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype equals “Sales Invoice” → doctype equals “POS Invoice”.
  - Set doc.is\_pos from source.is\_pos.
  - If not doc.select\_print\_heading.
    - Set doc.select\_print\_heading from Platform.get\_cached\_value(“Print Heading”, “Credit Note”).
- Otherwise.
  - If doctype equals “Purchase Invoice”.
    - Set doc.select\_print\_heading from Platform.get\_cached\_value(“Print Heading”, “Debit Note”).
  - Otherwise.
    - If doctype equals “Delivery Note”.
      - Set doc.set\_warehouse from default\_warehouse\_for\_sales\_return.
- If doc.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Set doc.tax\_withholding\_group from source.tax\_withholding\_group.
  - Set doc.ignore\_tax\_withholding\_threshold from source.ignore\_tax\_withholding\_threshold.
- If doc.doctype belongs to list(“Sales Invoice”, “POS Invoice”, “Purchase Invoice”).
  - Evaluate doc.set(“advances”, list()).
  - Set doc.allocate\_advances\_automatically from 0.
- For each tax in (doc.get(“taxes”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“taxes”) → list().
  - If tax.charge\_type equals “Actual”.
    - Set tax.tax\_amount from (negative 1 × tax.tax\_amount).
- If doc.get(“is\_return”).
  - If (doc.doctype equals “Sales Invoice” or doc.doctype equals “POS Invoice”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype equals “Sales Invoice” → doc.doctype equals “POS Invoice”.
    - Set doc.consolidated\_invoice from empty text.
    - If doc.doctype equals “Sales Invoice”.
      - Set doc.pos\_closing\_entry from empty text.
    - Set doc.party\_account\_currency from source.party\_account\_currency.
    - Evaluate doc.set(“payments”, list()).
    - Set doc.update\_billed\_amount\_in\_delivery\_note from true.
    - Set change\_by\_row from get\_change\_by\_payment\_row(source).
    - For each data in source.payments.
      - Set paid\_amount from flt((data.amount − change\_by\_row at data.idx), data.precision(“amount”)).
      - Set base\_paid\_amount from flt((paid\_amount × source.conversion\_rate), source.precision(“base\_paid\_amount”)).
      - Evaluate doc.append(“payments”, mapping(“mode\_of\_payment” → data.mode\_of\_payment, “type” → data.type, “amount” → (negative 1 × paid\_amount), “base\_amount” → (negative 1 × base\_paid\_amount), …)).
    - If doc.is\_pos.
      - Set doc.paid\_amount from flt((flt(source.change\_amount) − source.paid\_amount), doc.precision(“paid\_amount”)).
  - Otherwise.
    - If doc.doctype equals “Purchase Invoice”.
      - Set doc.paid\_amount from (negative 1 × source.paid\_amount).
      - Set doc.base\_paid\_amount from (negative 1 × source.base\_paid\_amount).
      - Set doc.payment\_terms\_template from empty text.
      - Set doc.payment\_schedule from list().
- If (doc.get(“is\_return”) and hasattr(doc, “packed\_items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“is\_return”) → hasattr(doc, “packed\_items”).
  - Evaluate update\_packed\_items(doc).
- If doc.get(“discount\_amount”).
  - Set doc.discount\_amount from (negative 1 × source.discount\_amount).
- If doctype equals “Subcontracting Receipt”.
  - Set doc.set\_warehouse from source.set\_warehouse.
  - Set doc.supplier\_warehouse from source.supplier\_warehouse.
- Otherwise.
  - Evaluate doc.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Print Heading”, “Credit Note”), Platform.get\_cached\_value(“Print Heading”, “Debit Note”) · selected callable from doc.run\_method(“calculate\_taxes\_and\_totals”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L541)

<a id="op-0fe803dd60dc52"></a>
### Make return doc.update packed items

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_make_return_doc_update_packed_items`

**Inputs** doc.

**Local steps**

- Set ref\_field from “dn\_detail” when doctype equals “Delivery Note”, otherwise (Platform.scrub(doctype) + “\_item”).
  - Value choice on doctype equals “Delivery Note” — true gives “dn\_detail”, false gives (Platform.scrub(doctype) + “\_item”).
- Set item\_idx from mapping of item.get(ref\_field) → item.idx for item drawn from doc.get(“items”).
  - Draw item from doc.get(“items”).
- For each d in doc.get(“packed\_items”).
  - Set d.qty from (d.qty × negative 1).
  - Set d.parent\_detail\_docname from item\_idx.get(d.parent\_detail\_docname).
  - If default\_warehouse\_for\_sales\_return.
    - Set d.warehouse from default\_warehouse\_for\_sales\_return.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1095) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L335)

<a id="op-c5dfa1cc915557"></a>
### Make return doc.update item

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_return_record_update_item`

**Inputs** source\_doc, target\_doc, source\_parent.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set target\_doc.qty from (negative 1 × source\_doc.qty).
- Set target\_doc.pricing\_rules from no value.
- If doctype belongs to list(“Purchase Receipt”, “Subcontracting Receipt”).
  - Set returned\_qty\_map from get\_returned\_qty\_map\_for\_purchase\_flow(source\_parent.name, source\_parent.supplier, source\_doc.name, doctype).
  - Set wh\_map from (returned\_qty\_map.get(source\_doc.warehouse) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(source\_doc.warehouse) → Platform.\_dict().
  - Set rejected\_wh\_map from (returned\_qty\_map.get(source\_doc.rejected\_warehouse) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(source\_doc.rejected\_warehouse) → Platform.\_dict().
  - If doctype equals “Subcontracting Receipt”.
    - Set target\_doc.received\_qty from (negative 1 × flt(source\_doc.qty)).
  - Otherwise.
    - Set target\_doc.rejected\_qty from (negative 1 × flt((source\_doc.rejected\_qty − (rejected\_wh\_map.qty or 0)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in rejected\_wh\_map.qty → 0.
  - Set target\_doc.qty from (negative 1 × flt((source\_doc.qty − (wh\_map.qty or 0)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in wh\_map.qty → 0.
  - If (hasattr(target\_doc, “stock\_qty”) and not return\_against\_rejected\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(target\_doc, “stock\_qty”) → not return\_against\_rejected\_qty.
    - Set target\_doc.stock\_qty from (negative 1 × flt((source\_doc.stock\_qty − (flt(wh\_map.stock\_qty) or 0)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(wh\_map.stock\_qty) → 0.
  - If doctype equals “Subcontracting Receipt”.
    - Set target\_doc.process\_loss\_qty from 0.
    - Set target\_doc.subcontracting\_order from source\_doc.subcontracting\_order.
    - Set target\_doc.subcontracting\_order\_item from source\_doc.subcontracting\_order\_item.
    - Set target\_doc.rejected\_warehouse from source\_doc.rejected\_warehouse.
    - Set target\_doc.subcontracting\_receipt\_item from source\_doc.name.
    - If return\_against\_rejected\_qty.
      - Set target\_doc.qty from (negative 1 × flt((source\_doc.rejected\_qty − (rejected\_wh\_map.qty or 0)))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in rejected\_wh\_map.qty → 0.
      - Set target\_doc.rejected\_qty from 0.0.
      - Set target\_doc.rejected\_warehouse from empty text.
      - Set target\_doc.warehouse from source\_doc.rejected\_warehouse.
      - Set target\_doc.received\_qty from target\_doc.qty.
      - Set target\_doc.return\_qty\_from\_rejected\_warehouse from 1.
  - Otherwise.
    - Set target\_doc.purchase\_order from source\_doc.purchase\_order.
    - Set target\_doc.purchase\_order\_item from source\_doc.purchase\_order\_item.
    - Set target\_doc.rejected\_warehouse from source\_doc.rejected\_warehouse.
    - Set target\_doc.purchase\_receipt\_item from source\_doc.name.
    - Set target\_doc.delivery\_note\_packed\_item from source\_doc.delivery\_note\_packed\_item.
  - If (doctype equals “Purchase Receipt” and return\_against\_rejected\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “Purchase Receipt” → return\_against\_rejected\_qty.
    - Set target\_doc.qty from (negative 1 × flt((source\_doc.rejected\_qty − (rejected\_wh\_map.qty or 0)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in rejected\_wh\_map.qty → 0.
    - Set target\_doc.rejected\_qty from 0.0.
    - Set target\_doc.rejected\_warehouse from empty text.
    - Set target\_doc.warehouse from source\_doc.rejected\_warehouse.
    - Set target\_doc.received\_qty from target\_doc.qty.
    - Set target\_doc.return\_qty\_from\_rejected\_warehouse from 1.
- Otherwise.
  - If doctype equals “Purchase Invoice”.
    - Set returned\_qty\_map from get\_returned\_qty\_map\_for\_row(source\_parent.name, source\_parent.supplier, source\_doc.name, doctype).
    - Set target\_doc.received\_qty from (negative 1 × flt((source\_doc.received\_qty − (returned\_qty\_map.get(“received\_qty”) or 0)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“received\_qty”) → 0.
    - Set target\_doc.rejected\_qty from (negative 1 × flt((source\_doc.rejected\_qty − (returned\_qty\_map.get(“rejected\_qty”) or 0)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“rejected\_qty”) → 0.
    - Set target\_doc.qty from (negative 1 × flt((source\_doc.qty − (returned\_qty\_map.get(“qty”) or 0)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“qty”) → 0.
    - Set target\_doc.stock\_qty from (negative 1 × flt((source\_doc.stock\_qty − (returned\_qty\_map.get(“stock\_qty”) or 0)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“stock\_qty”) → 0.
    - Set target\_doc.purchase\_order from source\_doc.purchase\_order.
    - Set target\_doc.purchase\_receipt from source\_doc.purchase\_receipt.
    - Set target\_doc.rejected\_warehouse from source\_doc.rejected\_warehouse.
    - Set target\_doc.po\_detail from source\_doc.po\_detail.
    - Set target\_doc.pr\_detail from source\_doc.pr\_detail.
    - Set target\_doc.purchase\_invoice\_item from source\_doc.name.
    - Set target\_doc.tax\_withholding\_category from source\_doc.tax\_withholding\_category.
    - Set target\_doc.apply\_tds from source\_doc.apply\_tds.
  - Otherwise.
    - If doctype equals “Delivery Note”.
      - Set returned\_qty\_map from get\_returned\_qty\_map\_for\_row(source\_parent.name, source\_parent.customer, source\_doc.name, doctype).
      - Set target\_doc.qty from (negative 1 × flt((source\_doc.qty − (returned\_qty\_map.get(“qty”) or 0)))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“qty”) → 0.
      - Set target\_doc.stock\_qty from (negative 1 × flt((source\_doc.stock\_qty − (returned\_qty\_map.get(“stock\_qty”) or 0)))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“stock\_qty”) → 0.
      - Set target\_doc.against\_sales\_order from source\_doc.against\_sales\_order.
      - Set target\_doc.against\_sales\_invoice from source\_doc.against\_sales\_invoice.
      - Set target\_doc.so\_detail from source\_doc.so\_detail.
      - Set target\_doc.expense\_account from source\_doc.expense\_account.
      - Set target\_doc.dn\_detail from source\_doc.name.
      - Set target\_doc.cost\_center from source\_doc.cost\_center.
      - Set target\_doc.target\_warehouse from source\_doc.target\_warehouse.
      - If default\_warehouse\_for\_sales\_return.
        - Set target\_doc.warehouse from default\_warehouse\_for\_sales\_return.
    - Otherwise.
      - If (doctype equals “Sales Invoice” or doctype equals “POS Invoice”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype equals “Sales Invoice” → doctype equals “POS Invoice”.
        - Set returned\_qty\_map from get\_returned\_qty\_map\_for\_row(source\_parent.name, source\_parent.customer, source\_doc.name, doctype).
        - Set target\_doc.qty from (negative 1 × flt((source\_doc.qty − (returned\_qty\_map.get(“qty”) or 0)))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“qty”) → 0.
        - Set target\_doc.stock\_qty from (negative 1 × flt((source\_doc.stock\_qty − (returned\_qty\_map.get(“stock\_qty”) or 0)))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in returned\_qty\_map.get(“stock\_qty”) → 0.
        - Set target\_doc.sales\_order from source\_doc.sales\_order.
        - Set target\_doc.delivery\_note from source\_doc.delivery\_note.
        - Set target\_doc.so\_detail from source\_doc.so\_detail.
        - Set target\_doc.dn\_detail from source\_doc.dn\_detail.
        - Set target\_doc.expense\_account from source\_doc.expense\_account.
        - If doctype equals “Sales Invoice”.
          - Set target\_doc.sales\_invoice\_item from source\_doc.name.
          - Set target\_doc.tax\_withholding\_category from source\_doc.tax\_withholding\_category.
          - Set target\_doc.apply\_tds from source\_doc.apply\_tds.
        - Otherwise.
          - Set target\_doc.pos\_invoice\_item from source\_doc.name.
        - If default\_warehouse\_for\_sales\_return.
          - Set target\_doc.warehouse from default\_warehouse\_for\_sales\_return.
- If (not source\_doc.use\_serial\_batch\_fields and source\_doc.serial\_and\_batch\_bundle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not source\_doc.use\_serial\_batch\_fields → source\_doc.serial\_and\_batch\_bundle.
  - Set target\_doc.serial\_no from no value.
  - Set target\_doc.batch\_no from no value.
- If ((source\_doc.serial\_no or source\_doc.batch\_no) and not source\_doc.serial\_and\_batch\_bundle and not source\_doc.use\_serial\_batch\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (source\_doc.serial\_no or source\_doc.batch\_no) → not source\_doc.serial\_and\_batch\_bundle → not source\_doc.use\_serial\_batch\_fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_doc.serial\_no → source\_doc.batch\_no.
  - Evaluate target\_doc.set(“use\_serial\_batch\_fields”, 1).
- If (not source\_doc.serial\_no and not source\_doc.batch\_no and source\_doc.serial\_and\_batch\_bundle and source\_doc.use\_serial\_batch\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not source\_doc.serial\_no → not source\_doc.batch\_no → source\_doc.serial\_and\_batch\_bundle → source\_doc.use\_serial\_batch\_fields.
  - Evaluate target\_doc.set(“use\_serial\_batch\_fields”, 0).
- If (source\_doc.item\_code and target\_doc.get(“use\_serial\_batch\_fields”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_doc.item\_code → target\_doc.get(“use\_serial\_batch\_fields”).
  - Set item\_details from Platform.get\_cached\_value(“Item”, source\_doc.item\_code, list(“has\_batch\_no”, “has\_serial\_no”), as\_dict = 1).
  - If (not item\_details.has\_batch\_no and not item\_details.has\_serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_details.has\_batch\_no → not item\_details.has\_serial\_no.
    - Return no value.
  - Evaluate update\_non\_bundled\_serial\_nos(source\_doc, target\_doc, source\_parent).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, source\_doc.item\_code, list(“has\_batch\_no”, “has\_serial\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L861) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L542)

<a id="op-6d2ba4716540e7"></a>
### Make return doc.update non bundled serial nos

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_return_record_update_non_bundled_serial_numbers`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Bind dependencies get\_serial\_nos.
- If source\_doc.serial\_no.
  - Set returned\_serial\_nos from get\_returned\_non\_bundled\_serial\_nos(source\_doc, source\_parent).
  - Set serial\_nos from list((set(get\_serial\_nos(source\_doc.serial\_no)) − set(returned\_serial\_nos))).
  - If serial\_nos.
    - Set target\_doc.serial\_no from whitespace '\\n'.join(serial\_nos).
- If source\_doc.get(“rejected\_serial\_no”).
  - Set returned\_serial\_nos from get\_returned\_non\_bundled\_serial\_nos(source\_doc, source\_parent, serial\_no\_field = “rejected\_serial\_no”).
  - Set rejected\_serial\_nos from list((set(get\_serial\_nos(source\_doc.rejected\_serial\_no)) − set(returned\_serial\_nos))).
  - If rejected\_serial\_nos.
    - Set target\_doc.rejected\_serial\_no from whitespace '\\n'.join(rejected\_serial\_nos).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0384.json#L4902) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L862) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L543)

<a id="op-86887de44094ed"></a>
### Make return doc.get returned non bundled serial nos

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_return_record_get_returned_non_bundled_serial_numbers`

**Inputs** child\_doc, parent\_doc, serial\_no\_field = “serial\_no”.

**Record and data access** read parent\_doc.doctype via get\_all.

**Explicit results** serial\_nos.

**Local steps**

- Bind dependencies get\_serial\_nos.
- Set return\_ref\_field from Platform.scrub(child\_doc.doctype).
- If child\_doc.doctype equals “Delivery Note Item”.
  - Set return\_ref\_field from “dn\_detail”.
- Set serial\_nos from list().
- Set fields from list(formatted text ′{(“tab” + child\_doc.doctype)}′.′{serial\_no\_field}′).
- Set filters from list(list(parent\_doc.doctype, “return\_against”, “=”, parent\_doc.name), list(parent\_doc.doctype, “is\_return”, “=”, 1), list(child\_doc.doctype, return\_ref\_field, “=”, child\_doc.name), list(parent\_doc.doctype ….
- For each row in Platform.get\_all(parent\_doc.doctype, fields = fields, filters = filters).
  - Evaluate serial\_nos.extend(get\_serial\_nos(row.get(serial\_no\_field))).
- Return serial\_nos.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0384.json#L5306) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L539)

<a id="op-abd4e42017935b"></a>
### Make return doc.update terms

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_return_record_update_terms`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Set target\_doc.payment\_amount from negative source\_doc.payment\_amount.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0384.json#L5788) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L544)

<a id="op-6acf6d7d32a29c"></a>
### Make return doc.item condition

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_make_return_record_item_condition`

**Inputs** doc.

**Explicit results** doc.rejected\_qty · (doc.qty or doc.get(“rejected\_qty”)).

**Local steps**

- If return\_against\_rejected\_qty.
  - Return doc.rejected\_qty.
- Return (doc.qty or doc.get(“rejected\_qty”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.qty → doc.get(“rejected\_qty”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L859) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L540)

<a id="op-f2a38b876685a4"></a>
### Get rate for return

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_rate_for_return`

**Inputs** voucher\_type, voucher\_no, item\_code, return\_against = no value, item\_row = no value, voucher\_detail\_no = no value, sle = no value.

**Record and data access** read voucher\_type via get\_cached\_value · read “Item” via get\_cached\_value · read “Selling Settings” via get\_single\_value · read formatted text {voucher\_type} Item via get\_value · read “Stock Ledger Entry” via get\_value · 1 additional forms in the steps below.

**State and service calls** request set\_value on (voucher\_type + “ Item”).

**Explicit results** 0 · rate.

**Local steps**

- If not return\_against.
  - Set return\_against from Platform.get\_cached\_value(voucher\_type, voucher\_no, “return\_against”).
- Set return\_against\_item\_field from get\_return\_against\_item\_fields(voucher\_type).
- Set filters from get\_filters(voucher\_type, voucher\_no, voucher\_detail\_no, return\_against, warehouse = sle.get(“warehouse”) when sle, otherwise no value, …).
  - Value choice on sle — true gives sle.get(“warehouse”), false gives no value.
- If voucher\_type belongs to tuple(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”).
  - Set select\_field from “incoming\_rate”.
- Otherwise.
  - Set StockLedgerEntry from Platform.qb.DocType(“Stock Ledger Entry”).
  - Set select\_field from Abs((StockLedgerEntry.stock\_value\_difference ÷ StockLedgerEntry.actual\_qty)).
- Set item\_details from Platform.get\_cached\_value(“Item”, item\_code, list(“has\_batch\_no”, “has\_expiry\_date”), as\_dict = 1).
- Set set\_zero\_rate\_for\_expired\_batch from Platform.db.get\_single\_value(“Selling Settings”, “set\_zero\_rate\_for\_expired\_batch”).
- If (set\_zero\_rate\_for\_expired\_batch and item\_details.has\_batch\_no and item\_details.has\_expiry\_date and not return\_against and voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in set\_zero\_rate\_for\_expired\_batch → item\_details.has\_batch\_no → item\_details.has\_expiry\_date → not return\_against → voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”).
  - Set batch\_no from Platform.db.get\_value(formatted text {voucher\_type} Item, voucher\_detail\_no, “batch\_no”).
  - If (batch\_no and is\_batch\_expired(batch\_no, sle.get(“posting\_date”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in batch\_no → is\_batch\_expired(batch\_no, sle.get(“posting\_date”)).
    - Evaluate Platform.db.set\_value((voucher\_type + “ Item”), voucher\_detail\_no, “incoming\_rate”, 0).
    - Return 0.
- Set rate from get\_rate\_for\_returned\_packed\_item(voucher\_type, return\_against, item\_row, sle).
- If rate is identical to no value.
  - Set rate from flt(Platform.db.get\_value(“Stock Ledger Entry”, filters, select\_field)).
- If (not (rate and return\_against) and voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (rate and return\_against) → voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rate → return\_against.
  - Set rate from Platform.db.get\_value(formatted text {voucher\_type} Item, voucher\_detail\_no, “incoming\_rate”).
  - If (rate is identical to no value and sle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in rate is identical to no value → sle.
    - Set rate from \_get\_incoming\_rate(mapping(“item\_code” → sle.item\_code, “warehouse” → sle.warehouse, “posting\_date” → sle.get(“posting\_date”), “posting\_time” → sle.get(“posting\_time”), …), raise\_error\_if\_no\_rate = false).
- If (not rate and voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not rate → voucher\_type belongs to list(“Sales Invoice”, “Delivery Note”).
  - Set details from Platform.db.get\_value((voucher\_type + “ Item”), voucher\_detail\_no, list(“rate”, “allow\_zero\_valuation\_rate”), as\_dict = 1).
  - If (details and not details.allow\_zero\_valuation\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in details → not details.allow\_zero\_valuation\_rate.
    - Set rate from flt(details.rate).
- Return rate.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(voucher\_type, voucher\_no, “return\_against”), Platform.get\_cached\_value(“Item”, item\_code, list(“has\_batch\_no”, “has\_expiry\_date”), as\_dict = 1) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L844) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L525)

<a id="op-68f8c54a16703c"></a>
### Get rate for returned packed item

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_get_rate_for_returned_packed_item`

**Inputs** voucher\_type, return\_against, item\_row = no value, sle = no value.

**Explicit results** no value · (sum(generator of (flt(nested operand in the contract.get(name)) × qty) for tuple(name, qty) drawn from returned\_qty.items()) ÷ sum(returned\_qty.values())).

**Local steps**

- If (not return\_against or voucher\_type does not belong to tuple(“Delivery Note”, “Sales Invoice”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not return\_against → voucher\_type does not belong to tuple(“Delivery Note”, “Sales Invoice”).
  - Return no value.
- Set returned\_qty from get\_returned\_qty\_by\_delivered\_packed\_item(item\_row, sle).
- If not returned\_qty.
  - Return no value.
- Set rates from get\_delivered\_packed\_item\_rates(voucher\_type, return\_against, list(returned\_qty)).
- If not rates.
  - Return no value.
- Return (sum(generator of (flt(nested operand in the contract.get(name)) × qty) for tuple(name, qty) drawn from returned\_qty.items()) ÷ sum(returned\_qty.values())).
  - Draw tuple(name, qty) from returned\_qty.items().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1089) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L329)

<a id="op-6a84cea7b587a1"></a>
### Get returned qty by delivered packed item

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_get_returned_qty_by_delivered_packed_item`

**Inputs** item\_row = no value, sle = no value.

**Declared result** dict.

**Record and data access** read “Packed Item” via get\_all.

**Explicit results** mapping of row.return\_against\_packed\_item → (abs(flt(row.qty)) or 1) for row drawn from returned\_rows where row.get(“return\_against\_packed\_item”).

**Local steps**

- Bind dependencies get\_location\_filters.
- If item\_row.
  - Set returned\_rows from list(item\_row) when item\_row.get(“doctype”) equals “Packed Item”, otherwise list().
    - Value choice on item\_row.get(“doctype”) equals “Packed Item” — true gives list(item\_row), false gives list().
- Otherwise.
  - Set filters from mapping(“parent\_detail\_docname” → sle.voucher\_detail\_no, “item\_code” → sle.item\_code, “qty” → tuple(“!=”, 0)).
  - Set returned\_rows from Platform.get\_all(“Packed Item”, filters = (filters bitwise or get\_location\_filters(sle)), fields = list(“qty”, “return\_against\_packed\_item”)).
- Return mapping of row.return\_against\_packed\_item → (abs(flt(row.qty)) or 1) for row drawn from returned\_rows where row.get(“return\_against\_packed\_item”).
  - Draw row from returned\_rows, keep a combination only if (row.get(“return\_against\_packed\_item”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in abs(flt(row.qty)) → 1.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1092) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L332)

<a id="op-f50abf0d978258"></a>
### Get delivered packed item rates

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_get_delivered_packed_item_rates`

**Inputs** voucher\_type, voucher\_no, packed\_items.

**Declared result** dict.

**Explicit results** dict(rates).

**Local steps**

- Set packed\_item from DocType(“Packed Item”).
- Set sle from DocType(“Stock Ledger Entry”).
- Set same\_location from (sle.serial\_and\_batch\_bundle equals packed\_item.serial\_and\_batch\_bundle bitwise or (IfNull(packed\_item.serial\_and\_batch\_bundle, empty text) equals empty text bitwise and sle.warehouse equals packed\_item.warehouse)).
- Set rates from nested operand in the contract(nested operand in the contract).select(packed\_item.name, Abs((nested operand in the contract ÷ nested operand in the contract))).where((((nested operand in the contract(neste ….run().
- Return dict(rates).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1088) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L328)

<a id="op-d1b2590c1c4d75"></a>
### Get return against item fields

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_return_against_item_fields`

**Inputs** voucher\_type.

**Explicit results** return\_against\_item\_fields at voucher\_type.

**Local steps**

- Set return\_against\_item\_fields from mapping(“Purchase Receipt” → “purchase\_receipt\_item”, “Purchase Invoice” → “purchase\_invoice\_item”, “Delivery Note” → “dn\_detail”, “Sales Invoice” → “sales\_invoice\_item”, …).
- Return return\_against\_item\_fields at voucher\_type.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0385.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L846) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L527)

<a id="op-0f139835ffefce"></a>
### Get filters

`operation_enterprise_controllers_sales_and_purchase_return_business_behavior_get_filters`

**Inputs** voucher\_type, voucher\_no, voucher\_detail\_no, return\_against, item\_code, return\_against\_item\_field, item\_row, warehouse = no value.

**Record and data access** read (voucher\_type + “ Item”) via get\_value · read “Subcontracting Receipt Item” via get\_value.

**Explicit results** filters.

**Local steps**

- Set filters from mapping(“voucher\_type” → voucher\_type, “voucher\_no” → return\_against, “item\_code” → item\_code).
- If item\_row.
  - Set reference\_voucher\_detail\_no from item\_row.get(return\_against\_item\_field).
- Otherwise.
  - Set reference\_voucher\_detail\_no from Platform.db.get\_value((voucher\_type + “ Item”), voucher\_detail\_no, return\_against\_item\_field).
- If reference\_voucher\_detail\_no.
  - Set filters at “voucher\_detail\_no” from reference\_voucher\_detail\_no.
- Set warehouses from list().
- If (voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”) and (item\_row or warehouse)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”, “Subcontracting Receipt”) → (item\_row or warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row → warehouse.
  - If reference\_voucher\_detail\_no.
    - Set warehouses from get\_warehouses\_for\_return(voucher\_type, reference\_voucher\_detail\_no).
  - If item\_row.
    - Set warehouse\_field from “warehouse”.
    - If (not flt(item\_row.get(“qty”)) and flt(item\_row.get(“rejected\_qty”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(item\_row.get(“qty”)) → flt(item\_row.get(“rejected\_qty”)).
      - Set warehouse\_field from “rejected\_warehouse”.
    - Set warehouse from item\_row.get(warehouse\_field).
  - If (warehouse and warehouse belongs to warehouses).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in warehouse → warehouse belongs to warehouses.
    - Set filters at “warehouse” from warehouse.
- If (voucher\_type equals “Subcontracting Receipt” and reference\_voucher\_detail\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type equals “Subcontracting Receipt” → reference\_voucher\_detail\_no.
  - Set return\_row from (item\_row or Platform.db.get\_value(“Subcontracting Receipt Item”, voucher\_detail\_no, list(“warehouse”, “return\_qty\_from\_rejected\_warehouse”), as\_dict = true)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_row → Platform.db.get\_value(“Subcontracting Receipt Item”, voucher\_detail\_no, list(“warehouse”, “return\_qty\_from\_rejected\_warehouse”), as\_dict = true).
  - If (return\_row and warehouse equals return\_row.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in return\_row → warehouse equals return\_row.warehouse.
    - Set filters at “warehouse” from get\_subcontracting\_return\_warehouse(reference\_voucher\_detail\_no, return\_row).
- Return filters.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L840) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L521)

<a id="op-f614b8dd52135f"></a>
### Get subcontracting return warehouse

`operation_enterprise_binding_enterprise_controllers_sales_and_purchase_return_get_subcontracting_return_warehouse`

**Inputs** original\_row\_name, return\_row.

**Record and data access** read “Subcontracting Receipt Item” via get\_value.

**Explicit results** original.rejected\_warehouse · original.warehouse.

**Local steps**

- Set original from Platform.db.get\_value(“Subcontracting Receipt Item”, original\_row\_name, list(“warehouse”, “rejected\_warehouse”), as\_dict = true).
- If is\_rejected\_subcontracting\_return(return\_row, original.rejected\_warehouse).
  - Return original.rejected\_warehouse.
- Return original.warehouse.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1093) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L333)
