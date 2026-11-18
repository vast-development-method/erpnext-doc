# Inventory and warehouses · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Landed cost voucher

[Record definition](../../../../data/record-types/landed_cost_voucher.json)

<a id="op-b79f850821f030"></a>
### Landed Cost Voucher.update project purchase cost

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_landedcostvoucher_update_project_purchase_cost`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If Platform.db.get\_single\_value(“Buying Settings”, “project\_update\_frequency”) differs from “Each Transaction”.
  - Return no value.
- Set receipts from mapping().
- Set projects from set of self.get\_receipt\_dimension(receipts, item, “project”) for item drawn from self.get(“items”).
  - Draw item from self.get(“items”).
- Evaluate update\_purchase\_cost((projects − set(no value, empty text))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get receipt dimension](operations-030.md#op-143efda2ea30c4).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “project\_update\_frequency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L837) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L334)

<a id="op-7235b448bd413a"></a>
### Landed Cost Voucher.update claimed landed cost

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_update_claimed_landed_cost`

**Inputs** self.

**State and service calls** request set\_value on “Purchase Invoice”.

**Local steps**

- For each vendor\_invoice in set of row.vendor\_invoice for row drawn from self.vendor\_invoices.
  - Draw row from self.vendor\_invoices.
  - Evaluate Platform.db.set\_value(“Purchase Invoice”, vendor\_invoice, “claimed\_landed\_cost\_amount”, get\_claimed\_landed\_cost(vendor\_invoice)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1251)

<a id="op-b264bc3b102220"></a>
### Landed Cost Voucher.validate vendor invoice claims

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_landedcostvoucher_validate_vendor_invoice_claims`

**Inputs** self.

**Record and data access** read “Purchase Invoice” via get\_value.

**Explicit failure paths** validation helper — translated “Claimed amount {0} for Vendor Invoice {1} exceeds its unclaimed amount {2}”.format(Platform.bold(amount), Platform.bold(vendor\_invoice), Platform.bold(unclaimed\_amount)).

**Local steps**

- Set claimed\_by\_invoice from mapping().
- For each row in self.vendor\_invoices.
  - Set claimed\_by\_invoice at row.vendor\_invoice from (claimed\_by\_invoice.get(row.vendor\_invoice, 0) + flt(row.amount)).
- For each tuple(vendor\_invoice, amount) in claimed\_by\_invoice.items().
  - Set invoice\_total from Platform.db.get\_value(“Purchase Invoice”, vendor\_invoice, “base\_total”, for\_update = true).
  - Set unclaimed\_amount from (flt(invoice\_total) − flt(get\_claimed\_landed\_cost(vendor\_invoice, exclude\_voucher = self.name, for\_update = true))).
  - If flt(amount, 2) &gt; flt(unclaimed\_amount, 2).
    - Call the validation error handler Platform.throw(translated “Claimed amount {0} for Vendor Invoice {1} exceeds its unclaimed amount {2}”.format(Platform.bold(amount), Platform.bold(vendor\_invoice), Platform.bold(unclaimed\_amount))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L840) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L337)

<a id="op-cab7870fd2aa3a"></a>
### Landed Cost Voucher.update landed cost

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_update_landed_cost`

**Inputs** self.

**Record and data access** resolve a document from d.receipt\_document\_type via get\_doc.

**State and service calls** call db\_update on item.

**Local steps**

- For each d in self.get(“purchase\_receipts”).
  - Set doc from Platform.get\_doc(d.receipt\_document\_type, d.receipt\_document).
  - If self.docstatus differs from 2.
    - Evaluate self.validate\_asset\_qty\_and\_status(d.receipt\_document\_type, doc).
  - Evaluate doc.set\_landed\_cost\_voucher\_amount().
  - If d.receipt\_document\_type equals “Subcontracting Receipt”.
    - Evaluate doc.calculate\_items\_qty\_and\_amount().
  - Otherwise.
    - Evaluate doc.update\_valuation\_rate(reset\_outgoing\_rate = false).
  - For each item in doc.get(“items”).
    - Evaluate item.db\_update().
  - If d.receipt\_document\_type belongs to list(“Stock Entry”, “Subcontracting Receipt”).
    - Continue with the next iteration or loop test.
  - Evaluate self.update\_rate\_in\_serial\_no\_for\_non\_asset\_items(doc).
- For each d in self.get(“purchase\_receipts”).
  - Set doc from Platform.get\_doc(d.receipt\_document\_type, d.receipt\_document).
  - Set doc.docstatus from 2.
  - Evaluate doc.update\_stock\_ledger(allow\_negative\_stock = true, via\_landed\_cost\_voucher = true).
  - Evaluate doc.make\_gl\_entries\_on\_cancel(from\_repost = true).
  - Set doc.docstatus from 1.
  - Evaluate doc.make\_bundle\_using\_old\_serial\_batch\_fields(via\_landed\_cost\_voucher = true).
  - Evaluate doc.update\_stock\_ledger(allow\_negative\_stock = true, via\_landed\_cost\_voucher = true).
  - If d.receipt\_document\_type equals “Purchase Receipt”.
    - Evaluate doc.make\_gl\_entries(via\_landed\_cost\_voucher = true).
  - Otherwise.
    - Evaluate doc.make\_gl\_entries().
  - Evaluate doc.repost\_future\_sle\_and\_gle(via\_landed\_cost\_voucher = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset qty and status](operations-031.md#op-83cdbabb428803), [update rate in serial no for non asset items](operations-031.md#op-458257ff5a787a).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1252)

<a id="op-83cdbabb428803"></a>
### Landed Cost Voucher.validate asset qty and status

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_validate_asset_quantity_and_status`

**Inputs** self, receipt\_document\_type, receipt\_document.

**Record and data access** read “Asset” via get\_all.

**Explicit failure paths** validation helper — translated “For item &lt;b&gt;{0}&lt;/b&gt;, only &lt;b&gt;{1}&lt;/b&gt; asset have been created or linked to &lt;b&gt;{2}&lt;/b&gt;. Please create or link  …”.format(item.item\_code, total\_asset\_qty, item.receipt\_document, (item.qty − total\_ … · validation helper — translated “{0} &lt;b&gt;{1}&lt;/b&gt; has submitted Assets. Remove Item &lt;b&gt;{2}&lt;/b&gt; from table to continue.”.format(item.receipt\_document\_type, item.receipt\_document, item.item\_code).

**Local steps**

- For each item in self.get(“items”).
  - If item.is\_fixed\_asset.
    - Set receipt\_document\_type from “purchase\_invoice” when item.receipt\_document\_type equals “Purchase Invoice”, otherwise “purchase\_receipt”.
      - Value choice on item.receipt\_document\_type equals “Purchase Invoice” — true gives “purchase\_invoice”, false gives “purchase\_receipt”.
    - Set docs from Platform.db.get\_all(“Asset”, filters = mapping(receipt\_document\_type → item.receipt\_document, “item\_code” → item.item\_code, “docstatus” → list(“!=”, 2)), fields = list(“name”, “docstatus”, “asset\_quantity”)).
    - Set total\_asset\_qty from sum(generator of cint(d.asset\_quantity) for d drawn from docs).
      - Draw d from docs.
    - If (not docs or total\_asset\_qty &lt; item.qty).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not docs → total\_asset\_qty &lt; item.qty.
      - Call the validation error handler Platform.throw(translated “For item &lt;b&gt;{0}&lt;/b&gt;, only &lt;b&gt;{1}&lt;/b&gt; asset have been created or linked to &lt;b&gt;{2}&lt;/b&gt;. Please create or link  …”.format(item.item\_code, total\_asset\_qty, item.receipt\_document, (it ….
    - If docs.
      - For each d in docs.
        - <a id="op-83cdbabb428803-guard-32"></a>If d.docstatus equals 1.
          - Call the validation error handler Platform.throw(translated “{0} &lt;b&gt;{1}&lt;/b&gt; has submitted Assets. Remove Item &lt;b&gt;{2}&lt;/b&gt; from table to continue.”.format(item.receipt\_document\_type, item.receipt\_document, item.item\_code)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison d.docstatus equals 1, d.docstatus = 1 (submitted) selects the branch that calls the validation-error handler with translated “{0} &lt;b&gt;{1}&lt;/b&gt; has submitted Assets. Remove Item &lt;b&gt;{2}&lt;/b&gt; from table to continue.”.format(item.receipt\_document\_type, i …. With d.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-83cdbabb428803-guard-32)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1256)

<a id="op-458257ff5a787a"></a>
### Landed Cost Voucher.update rate in serial no for non asset items

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_update_rate_in_serial_number_for_non_asset_items`

**Inputs** self, receipt\_document.

**State and service calls** execute a supplied database query.

**Local steps**

- For each item in receipt\_document.get(“items”).
  - If (not item.is\_fixed\_asset and item.serial\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.is\_fixed\_asset → item.serial\_no.
    - Set serial\_nos from get\_serial\_nos(item.serial\_no).
    - If serial\_nos.
      - Evaluate Platform.db.sql(“update ′tabSerial No′ set purchase\_rate=%s where name in ({})”.format(“, ”.join((list(“%s”) × len(serial\_nos)))), tuple(list(item.valuation\_rate, expanded serial\_nos))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1253)

<a id="op-f4100bc8da27d7"></a>
### Landed Cost Voucher.get vendor invoice amount

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_landed_cost_voucher_get_vendor_invoice_amount`

**Inputs** self, vendor\_invoice.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“amount” → amount).

**Local steps**

- Evaluate Platform.has\_permission(“Purchase Invoice”, “read”, vendor\_invoice, throw = true).
- Set filters from Platform.\_dict(mapping(“name” → vendor\_invoice, “company” → self.company)).
- Set query from get\_vendor\_invoice\_query(filters).
- Set result from query.run(as\_dict = true).
- Set amount from result at 0.unclaimed\_amount when result, otherwise 0.0.
  - Value choice on result — true gives result at 0.unclaimed\_amount, false gives 0.0.
- Return mapping(“amount” → amount).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Invoice”, “read”, vendor\_invoice, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1245)

<a id="op-2b3a642447f2e3"></a>
### Check receipt document access

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_check_receipt_document_access`

**Inputs** receipt\_document\_type, receipt\_document.

**Explicit failure paths** validation helper — translated “Receipt Document Type {0} is not supported”.format(receipt\_document\_type).

**Local steps**

- If receipt\_document\_type does not belong to RECEIPT\_DOCUMENT\_TYPES.
  - Call the validation error handler Platform.throw(translated “Receipt Document Type {0} is not supported”.format(receipt\_document\_type)).
- Evaluate Platform.has\_permission(receipt\_document\_type, “select”, receipt\_document, throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(receipt\_document\_type, “select”, receipt\_document, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L832) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L329)

<a id="op-a4154a713b8a69"></a>
### Get pr items

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_get_purchase_receipt_items`

**Inputs** purchase\_receipt.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set item from Platform.qb.DocType(“Item”).
- If purchase\_receipt.receipt\_document\_type equals “Stock Entry”.
  - Set pr\_item from Platform.qb.DocType(“Stock Entry Detail”).
- Otherwise.
  - Set pr\_item from Platform.qb.DocType((purchase\_receipt.receipt\_document\_type + “ Item”)).
- Set query from nested operand in the contract(nested operand in the contract).select(pr\_item.item\_code, pr\_item.description, pr\_item.qty, pr\_item.name, …).where((pr\_item.parent equals purchase\_receipt.receipt\_document bi ….
- If purchase\_receipt.receipt\_document\_type equals “Subcontracting Receipt”.
  - Set query from query.select(pr\_item.rate.as\_(“base\_rate”), pr\_item.amount.as\_(“base\_amount”)).
- Otherwise.
  - If purchase\_receipt.receipt\_document\_type equals “Stock Entry”.
    - Set query from query.select(pr\_item.basic\_rate.as\_(“base\_rate”), pr\_item.basic\_amount.as\_(“base\_amount”)).
    - Set query from query.where(pr\_item.is\_finished\_item equals 1).
  - Otherwise.
    - Set query from query.select(pr\_item.base\_net\_rate.as\_(“base\_rate”), pr\_item.base\_net\_amount.as\_(“base\_amount”), pr\_item.is\_fixed\_asset).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L53) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1237)

<a id="op-36d7cfc38c4644"></a>
### Get vendor invoices

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_get_vendor_invoices`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** list() · query.run(as\_list = true).

**Explicit failure paths** validation helper — translated “Invalid search query”.

**Local steps**

- If not Platform.has\_permission(“Purchase Invoice”, “read”).
  - Return list().
- If (txt and txt.lower().startswith(tuple(“select”, “delete”, “update”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in txt → txt.lower().startswith(tuple(“select”, “delete”, “update”)).
  - Call the validation error handler Platform.throw(translated “Invalid search query”, title = translated “Invalid Query”).
- Set query from get\_vendor\_invoice\_query(filters).where(nested operand in the contract.qb.DocType(“Purchase Invoice”).name.isin(Platform.qb.get\_query(“Purchase Invoice”, fields = list(“name”), ignore\_permissions = false))).
- If txt.
  - Set query from query.where(nested operand in the contract.qb.DocType(doctype).name.like(formatted text %{txt}%)).
- If start.
  - Set query from query.limit(page\_len).offset(start).
- Return query.run(as\_list = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Invoice”, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L56) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1240)

<a id="op-676aa58d72611f"></a>
### Absorb rounding difference

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_absorb_rounding_difference`

**Inputs** items, diff, precision, total.

**Local steps**

- Set sign from negative 1 when flt(total) &lt; 0, otherwise 1.
  - Value choice on flt(total) &lt; 0 — true gives negative 1, false gives 1.
- For each item in reversed(items).
  - If not diff.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set share from (flt(item.applicable\_charges) × sign).
  - Set adjustment from diff when (diff × sign) &gt; 0, otherwise (sign × max((diff × sign), negative share)).
    - Value choice on (diff × sign) &gt; 0 — true gives diff, false gives (sign × max((diff × sign), negative share)).
  - Set item.applicable\_charges from flt((flt(item.applicable\_charges) + adjustment), precision).
  - Set diff from flt((diff − adjustment), precision).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L831) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L328)

<a id="op-2d7dffc69f81c2"></a>
### Get claimed landed cost

`operation_enterprise_binding_enterprise_stock_doctype_landed_cost_voucher_landed_cost_voucher_get_claimed_landed_cost`

**Inputs** vendor\_invoice, exclude\_voucher = no value, for\_update = false.

**Explicit results** sum(generator of flt(amount) for amount drawn from query.run(pluck = true)).

**Local steps**

- Set vendor\_invoice\_row from Platform.qb.DocType(“Landed Cost Vendor Invoice”).
- Set query from nested operand in the contract.qb.from\_(vendor\_invoice\_row).select(vendor\_invoice\_row.amount).where((vendor\_invoice\_row.vendor\_invoice equals vendor\_invoice bitwise and vendor\_invoice\_row.docstatus equals 1)).
- If exclude\_voucher.
  - Set query from query.where(vendor\_invoice\_row.parent differs from exclude\_voucher).
- If for\_update.
  - Set query from query.for\_update().
- Return sum(generator of flt(amount) for amount drawn from query.run(pluck = true)).
  - Draw amount from query.run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L833) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L330)

<a id="op-bad7586b084a63"></a>
### Get vendor invoice query

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_get_vendor_invoice_query`

**Inputs** filters.

**Explicit results** query.

**Local steps**

- Set doctype from Platform.qb.DocType(“Purchase Invoice”).
- Set child\_doctype from Platform.qb.DocType(“Purchase Invoice Item”).
- Set item from Platform.qb.DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.name, nested operand in the contract.as\_(“unclaimed\_amount”)).where(((((nested operand in the contract bitwise and nested opera ….
- If filters.get(“name”).
  - Set query from query.where(doctype.name equals filters.get(“name”)).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L55) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1239)

<a id="op-61c3eb778ffc94"></a>
### Get lcv dimension fields

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_get_landed_cost_voucher_dimension_fields`

**Inputs** no declared parameters.

**Explicit results** list(“cost\_center”, “project”, expanded get\_accounting\_dimensions()).

**Local steps**

- Bind dependencies get\_accounting\_dimensions.
- Return list(“cost\_center”, “project”, expanded get\_accounting\_dimensions()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0746.json#L4609) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1236)

<a id="op-f986f82ae03239"></a>
### Get row dimensions

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_get_row_dimensions`

**Inputs** tax\_row, lcv\_item, dimension\_fields.

**Explicit results** Platform.\_dict(mapping of field → (tax\_row.get(field) or lcv\_item.get(field) or no value) for field drawn from dimension\_fields).

**Local steps**

- Return Platform.\_dict(mapping of field → (tax\_row.get(field) or lcv\_item.get(field) or no value) for field drawn from dimension\_fields).
  - Draw field from dimension\_fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_row.get(field) → lcv\_item.get(field) → no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0746.json#L4682) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L54) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1238)

<a id="op-e5b08a33e5e279"></a>
### Get custom dimension overrides

`operation_enterprise_stock_record_definitions_landed_cost_voucher_business_behavior_get_custom_dimension_overrides`

**Inputs** entry.

**Explicit results** mapping of dimension → value for tuple(dimension, value) drawn from (entry.dimensions or mapping()).items() where (value and dimension does not belong to tuple(“cost\_center”, “project”)).

**Local steps**

- Return mapping of dimension → value for tuple(dimension, value) drawn from (entry.dimensions or mapping()).items() where (value and dimension does not belong to tuple(“cost\_center”, “project”)).
  - Draw tuple(dimension, value) from (entry.dimensions or mapping()).items(), keep a combination only if ((value and dimension does not belong to tuple(“cost\_center”, “project”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions → mapping().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → dimension does not belong to tuple(“cost\_center”, “project”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0746.json#L4817) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1235)

## Record · Manufacturer

[Record definition](../../../../data/record-types/manufacturer.json)

<a id="op-a7bca18f0d5064"></a>
### Manufacturer.onload

`operation_enterprise_stock_record_definitions_manufacturer_business_behavior_manufacturer_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0750.json#L4965) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1300)

## Record · Material request

[Record definition](../../../../data/record-types/material_request.json)

<a id="op-42efab875d935b"></a>
### Material Request.initialize

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Material Request Item”, “target\_dt” → “Sales Order Item”, “target\_field” → “requested\_qty”, “target\_parent\_dt” → “Sales Order”, …), mapping(“source\_dt” → “Material Request Item” ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L1820) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1311)

<a id="op-2d1b3b8c19ec86"></a>
### Material Request.check if already pulled

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_check_if_already_pulled`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L2166) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1308)

<a id="op-908798d1b06d23"></a>
### Material Request.validate with previous doc

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_validate_with_previous_record`

**Inputs** self.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Sales Order” → mapping(“ref\_dn\_field” → “sales\_order”, “compare\_fields” → list(list(“company”, “=”))), “Sales Order Item” → mapping(“ref\_dn\_field” → “sales\_order ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L2199) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1329)

<a id="op-c26b7ec4c2a002"></a>
### Material Request.validate qty against so

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_validate_quantity_against_sales_order`

**Inputs** self.

**Record and data access** execute query text (SELECT, Material Request Item) · execute query text (SELECT, Sales).

**Explicit failure paths** validation helper — translated “Material Request of maximum {0} can be made for Item {1} against Sales Order {2}”.format((actual\_so\_qty − already\_indented), item, so\_no).

**Local steps**

- Set so\_items from mapping().
- For each d in self.get(“items”).
  - If d.sales\_order.
    - If d.sales\_order does not belong to so\_items.
      - Set so\_items at d.sales\_order from mapping(d.item\_code → flt(d.qty)).
    - Otherwise.
      - If d.item\_code does not belong to so\_items at d.sales\_order.
        - Set so\_items at d.sales\_order at d.item\_code from flt(d.qty).
      - Otherwise.
        - Update so\_items at d.sales\_order at d.item\_code using + flt(d.qty).
- For each so\_no in so\_items.keys().
  - For each item in so\_items at so\_no.keys().
    - Set already\_indented from Platform.db.sql(query text (SELECT, Material Request Item), tuple(item, so\_no, self.name)).
    - Set already\_indented from ((already\_indented and flt(already\_indented at 0 at 0)) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (already\_indented and flt(already\_indented at 0 at 0)) → 0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in already\_indented → flt(already\_indented at 0 at 0).
    - Set actual\_so\_qty from Platform.db.sql(query text (SELECT, Sales), tuple(so\_no, item)).
    - Set actual\_so\_qty from ((actual\_so\_qty and flt(actual\_so\_qty at 0 at 0)) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (actual\_so\_qty and flt(actual\_so\_qty at 0 at 0)) → 0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in actual\_so\_qty → flt(actual\_so\_qty at 0 at 0).
    - If (actual\_so\_qty and (flt(so\_items at so\_no at item) + already\_indented) &gt; actual\_so\_qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in actual\_so\_qty → (flt(so\_items at so\_no at item) + already\_indented) &gt; actual\_so\_qty.
      - Call the validation error handler Platform.throw(translated “Material Request of maximum {0} can be made for Item {1} against Sales Order {2}”.format((actual\_so\_qty − already\_indented), item, so\_no)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1328)

<a id="op-894874e7b50edd"></a>
### Material Request.validate

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_validate`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_source\_warehouse().
- Evaluate self.validate\_material\_request\_type().
- Evaluate super().validate().
- Evaluate self.validate\_schedule\_date().
- Evaluate self.check\_for\_on\_hold\_or\_closed\_status(“Sales Order”, “sales\_order”).
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- If not self.status.
  - Set self.status from “Draft”.
- Bind dependencies validate\_status.
- Evaluate validate\_status(self.status, list(“Draft”, “Submitted”, “Stopped”, “Cancelled”, …)).
- Evaluate validate\_for\_items(self).
- Evaluate self.set\_title().
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).
- Evaluate self.reset\_default\_field\_value(“set\_from\_warehouse”, “items”, “from\_warehouse”).
- Evaluate self.validate\_pp\_qty().
- Evaluate self.set\_buying\_price\_list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear source warehouse](operations-032.md#op-bdbcbf86bbc5f7), [validate material request type](operations-032.md#op-85f6567f8f721c), [validate with previous doc](operations-031.md#op-908798d1b06d23), [set title](operations-032.md#op-aea116e0bfb713), [validate pp qty](operations-032.md#op-3c6d5c953a63b1), [set buying price list](operations-031.md#op-8a136cfa88f707).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0037.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1324)

<a id="op-8a136cfa88f707"></a>
### Material Request.set buying price list

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_set_buying_price_list`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not is\_valid\_buying\_price\_list(self.buying\_price\_list).
  - Set self.buying\_price\_list from no value.
- If self.buying\_price\_list.
  - Return no value.
- Set default\_price\_list from Platform.defaults.get\_defaults().buying\_price\_list.
- If (is\_valid\_buying\_price\_list(default\_price\_list) and Platform.has\_permission(“Price List”, “read”, default\_price\_list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_valid\_buying\_price\_list(default\_price\_list) → Platform.has\_permission(“Price List”, “read”, default\_price\_list).
  - Set self.buying\_price\_list from default\_price\_list.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Price List”, “read”, default\_price\_list).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L3858) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1315)

<a id="op-bd229d05710f14"></a>
### Material Request.on update

`operation_enterprise_stock_record_definitions_material_request_business_behavior_material_request_on_update`

**Inputs** self.

**Local steps**

- If (not self.is\_new() and self.buying\_price\_list and self.has\_value\_changed(“buying\_price\_list”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.buying\_price\_list → self.has\_value\_changed(“buying\_price\_list”).
  - Evaluate self.update\_item\_rates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update item rates](operations-032.md#op-db46186a9c7a90).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0752.json#L4074) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L1314)
