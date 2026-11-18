# Purchasing · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Supplier

[Record definition](../../../../data/record-types/supplier.json)

<a id="op-5aadeefdb9c842"></a>
### Advances

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_advances`

**Inputs** supplier, company, as\_of.

**Explicit results** no value · flt(get\_partywise\_advanced\_payment\_amount(list(“Supplier”), as\_of, company = company, party = supplier).get(supplier)).

**Local steps**

- If not \_unrestricted\_read(“Payment Ledger Entry”).
  - Return no value.
- Return flt(get\_partywise\_advanced\_payment\_amount(list(“Supplier”), as\_of, company = company, party = supplier).get(supplier)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L849) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L89)

<a id="op-176b52f274096e"></a>
### Get supplier transactions

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_get_supplier_transactions`

**Inputs** supplier, company, doc\_type = “All”, limit = 20.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** rows at slice no value to limit.

**Local steps**

- Evaluate check\_access(supplier, company).
- Set limit from min((cint(limit) or 20), 100).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(limit) → 20.
- Set accounts from accounts\_access().
- Set wanted from list(doc\_type) when doc\_type belongs to TRANSACTION\_TYPES, otherwise list(TRANSACTION\_TYPES).
  - Value choice on doc\_type belongs to TRANSACTION\_TYPES — true gives list(doc\_type), false gives list(TRANSACTION\_TYPES).
- Set rows from list().
- For each doctype in wanted.
  - If ((doctype belongs to tuple(“Purchase Invoice”, “Payment Entry”) and not accounts) or not Platform.has\_permission(doctype, “read”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (doctype belongs to tuple(“Purchase Invoice”, “Payment Entry”) and not accounts) → not Platform.has\_permission(doctype, “read”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype belongs to tuple(“Purchase Invoice”, “Payment Entry”) → not accounts.
    - Continue with the next iteration or loop test.
  - Evaluate rows.extend(transaction\_rows(doctype, supplier, company, limit)).
- Evaluate rows.sort(key = deferred anonymous expression, reverse = true).
- Return rows at slice no value to limit.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L97)

<a id="op-412a7efb495dd6"></a>
### Transaction rows

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_transaction_rows`

**Inputs** doctype, supplier, company, limit.

**Record and data access** read “Company” via get\_cached\_value · read doctype via get\_list.

**Explicit results** list of mapping(“name” → r.name, “doctype” → doctype, “type\_label” → translated doctype, “date” → str(r.date), …) for r drawn from Platform.get\_list(doctype, filters = filters, fields = fields, order\_by =  ….

**Local steps**

- Set is\_payment from doctype equals “Payment Entry”.
- Set date\_field from “transaction\_date” when doctype equals “Purchase Order”, otherwise “posting\_date”.
  - Value choice on doctype equals “Purchase Order” — true gives “transaction\_date”, false gives “posting\_date”.
- Set amount\_field from “base\_paid\_amount” when is\_payment, otherwise “base\_grand\_total”.
  - Value choice on is\_payment — true gives “base\_paid\_amount”, false gives “base\_grand\_total”.
- Set fields from list(“name”, “status”, formatted text {date\_field} as date, formatted text {amount\_field} as amount).
- If doctype equals “Purchase Invoice”.
  - Update fields using + list(“outstanding\_amount”, “party\_account\_currency”, “conversion\_rate”).
- Set filters from mapping(“docstatus” → 1, “company” → company).
- Evaluate filters.update(mapping(“party\_type” → “Supplier”, “party” → supplier) when is\_payment, otherwise mapping(“supplier” → supplier)).
  - Value choice on is\_payment — true gives mapping(“party\_type” → “Supplier”, “party” → supplier), false gives mapping(“supplier” → supplier).
- Set currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Return list of mapping(“name” → r.name, “doctype” → doctype, “type\_label” → translated doctype, “date” → str(r.date), …) for r drawn from Platform.get\_list(doctype, filters = filters, fields = fields, order\_by =  ….
  - Draw r from Platform.get\_list(doctype, filters = filters, fields = fields, order\_by = formatted text {date\_field} desc, creation desc, limit = limit).
  - Value choice on doctype equals “Purchase Invoice” — true gives invoice\_outstanding(r, currency), false gives no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L209) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L111)

<a id="op-35e92013abffd5"></a>
### Invoice outstanding

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_invoice_outstanding`

**Inputs** row, currency.

**Explicit results** (flt(row.outstanding\_amount) × rate).

**Local steps**

- Set rate from 1 when row.party\_account\_currency equals currency, otherwise flt(row.conversion\_rate).
  - Value choice on row.party\_account\_currency equals currency — true gives 1, false gives flt(row.conversion\_rate).
- Return (flt(row.outstanding\_amount) × rate).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L197) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L859) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L99)

<a id="op-f21f1a88f461d1"></a>
### Get supplier companies

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_overview_get_supplier_companies`

**Inputs** supplier.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** sorted(companies).

**Local steps**

- Evaluate check\_access(supplier).
- Set companies from set().
- For each tuple(doctype, filters) in tuple(tuple(“Purchase Invoice”, mapping(“supplier” → supplier)), tuple(“Purchase Order”, mapping(“supplier” → supplier)), tuple(“Purchase Receipt”, mapping(“supplier” → supplier)), tuple(“Supplier Quotatio ….
  - If Platform.has\_permission(doctype, “read”).
    - Evaluate companies.update(Platform.get\_list(doctype, filters = mapping(expand filters, “docstatus” → 1), distinct = true, pluck = “company”)).
- Evaluate companies.discard(no value).
- Return sorted(companies).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L854) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L94)

## Record · Supplier quotation

[Record definition](../../../../data/record-types/supplier_quotation.json)

<a id="op-58f4b5a4176513"></a>
### Supplier Quotation.before validate

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_has\_unit\_price\_items().
- Set self.flags.allow\_zero\_qty from self.has\_unit\_price\_items.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set has unit price items](operations-010.md#op-a5d679a5f38984).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L3205) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L74)

<a id="op-194f23ec113fd0"></a>
### Supplier Quotation.validate

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_validate`

**Inputs** self.

**Local steps**

- Evaluate super().validate().
- Evaluate self.set\_status().
- If not self.status.
  - Set self.status from “Draft”.
- Bind dependencies validate\_status.
- Evaluate validate\_status(self.status, list(“Draft”, “Submitted”, “Partially Ordered”, “Ordered”, …)).
- Evaluate validate\_for\_items(self).
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.validate\_valid\_till().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate with previous doc](operations-010.md#op-aa4fb533e3db68), [validate valid till](operations-010.md#op-773b88af782f24).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L209) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L83)

<a id="op-b078d8d8abf2fa"></a>
### Supplier Quotation.on submit

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(update = true).
- Evaluate self.update\_rfq\_supplier\_status(1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update rfq supplier status](operations-010.md#op-d04b7939f7169e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L3555) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L79)

<a id="op-6850db94128351"></a>
### Supplier Quotation.on cancel

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(update = true).
- Evaluate self.update\_rfq\_supplier\_status(0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update rfq supplier status](operations-010.md#op-d04b7939f7169e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L3640) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L78)

<a id="op-7639f22e1fb57c"></a>
### Supplier Quotation.on trash

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_on_trash`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L3725) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L80)

<a id="op-a5d679a5f38984"></a>
### Supplier Quotation.set has unit price items

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_set_has_unit_price_items`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_supplier\_quotation”).
  - Set self.has\_unit\_price\_items from 0.
  - Return no value.
- Set self.has\_unit\_price\_items from any(generator of not row.qty for row drawn from self.get(“items”) where (row.item\_code and not row.qty)).
  - Draw row from self.get(“items”), keep a combination only if ((row.item\_code and not row.qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_code → not row.qty.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “allow\_zero\_qty\_in\_supplier\_quotation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L207) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L81)

<a id="op-aa4fb533e3db68"></a>
### Supplier Quotation.validate with previous doc

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_validate_with_previous_record`

**Inputs** self.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Material Request” → mapping(“ref\_dn\_field” → “prevdoc\_docname”, “compare\_fields” → list(list(“company”, “=”))), “Material Request Item” → mapping(“ref\_dn\_field”  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L3958) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L85)

<a id="op-773b88af782f24"></a>
### Supplier Quotation.validate valid till

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_validate_valid_till`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Valid till Date cannot be before Transaction Date”.

**Local steps**

- If (self.valid\_till and getdate(self.valid\_till) &lt; getdate(self.transaction\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valid\_till → getdate(self.valid\_till) &lt; getdate(self.transaction\_date).
  - Call the validation error handler Platform.throw(translated “Valid till Date cannot be before Transaction Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L4180) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L84)

<a id="op-990078804a75df"></a>
### Supplier Quotation.get ordered status

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_get_ordered_status`

**Inputs** self.

**Explicit results** “Submitted” · “Partially Ordered” · “Ordered”.

**Local steps**

- Set ordered\_items from get\_ordered\_items(self.name).
- If not ordered\_items.
  - Return “Submitted”.
- For each row in self.items.
  - If (row.name does not belong to ordered\_items or row.stock\_qty &gt; ordered\_items at row.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.name does not belong to ordered\_items → row.stock\_qty &gt; ordered\_items at row.name.
    - Return “Partially Ordered”.
- Return “Ordered”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L4321) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L75)

<a id="op-0fbe567d74eb52"></a>
### Supplier Quotation.is fully ordered

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_is_fully_ordered`

**Inputs** self.

**Explicit results** self.get\_ordered\_status() equals “Ordered”.

**Local steps**

- Return self.get\_ordered\_status() equals “Ordered”.

**Methods declared on this owner** [get ordered status](operations-010.md#op-990078804a75df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L4506) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L76)

<a id="op-efd24f272cbb83"></a>
### Supplier Quotation.is partially ordered

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_is_partially_ordered`

**Inputs** self.

**Explicit results** self.get\_ordered\_status() equals “Partially Ordered”.

**Local steps**

- Return self.get\_ordered\_status() equals “Partially Ordered”.

**Methods declared on this owner** [get ordered status](operations-010.md#op-990078804a75df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L4569) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L77)

<a id="op-d81758246fd4d9"></a>
### Supplier Quotation.get request for quotations

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_supplierquotation_get_request_for_quotations`

**Inputs** self.

**Declared result** set at str.

**Explicit results** set of item.request\_for\_quotation for item drawn from self.items where item.request\_for\_quotation.

**Local steps**

- Return set of item.request\_for\_quotation for item drawn from self.items where item.request\_for\_quotation.
  - Draw item from self.items, keep a combination only if (item.request\_for\_quotation).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L840) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L80)

<a id="op-d04b7939f7169e"></a>
### Supplier Quotation.update rfq supplier status

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_supplier_quotation_update_request_for_quotation_supplier_status`

**Inputs** self, include\_me, previous\_rfqs = no value.

**Record and data access** resolve a document from “Request for Quotation” via get\_doc · read “Request for Quotation Supplier” via get\_all · execute query text (SELECT, Supplier Quotation Item).

**State and service calls** request set\_value on “Request for Quotation Supplier”.

**Explicit failure paths** validation helper — translated “Supplier {0} not found in {1}”.format(self.supplier, text in the contract.format(doc.name)).

**Local steps**

- For each rfq in (self.get\_request\_for\_quotations() bitwise or (previous\_rfqs or set())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_rfqs → set().
  - Set doc from Platform.get\_doc(“Request for Quotation”, rfq).
  - Set doc\_sup from Platform.get\_all(“Request for Quotation Supplier”, filters = mapping(“parent” → doc.name, “supplier” → self.supplier), fields = list(“name”, “quote\_status”)).
  - Set doc\_sup from doc\_sup at 0 when doc\_sup, otherwise no value.
    - Value choice on doc\_sup — true gives doc\_sup at 0, false gives no value.
  - If not doc\_sup.
    - Call the validation error handler Platform.throw(translated “Supplier {0} not found in {1}”.format(self.supplier, text in the contract.format(doc.name))).
  - Set quote\_status from translated “Received”.
  - For each item in doc.items.
    - Set sqi\_count from Platform.db.sql(query text (SELECT, Supplier Quotation Item), mapping(“supplier” → self.supplier, “rqi” → item.name, “me” → self.name), as\_dict = 1) at 0.
    - Set self\_count from sum(generator of my\_item.request\_for\_quotation\_item equals item.name for my\_item drawn from self.items) when include\_me, otherwise 0.
      - Value choice on include\_me — true gives sum(generator of my\_item.request\_for\_quotation\_item equals item.name for my\_item drawn from self.items), false gives 0.
      - Draw my\_item from self.items.
    - If (sqi\_count.count + self\_count) equals 0.
      - Set quote\_status from translated “Pending”.
    - Evaluate Platform.db.set\_value(“Request for Quotation Supplier”, doc\_sup.name, “quote\_status”, quote\_status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get request for quotations](operations-010.md#op-d81758246fd4d9).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L82)

<a id="op-52731db06f3b45"></a>
### Get list context

`operation_enterprise_buying_record_definitions_supplier_quotation_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Supplier Quotation”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0349.json#L5752) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L72)

<a id="op-55b32e0de2dab1"></a>
### Make purchase order

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_make_purchase_order`

**Inputs** source\_name, target\_doc = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Supplier Quotation” via get\_doc.

**Explicit results** doclist.

**Explicit failure paths** validation helper — translated “Supplier Quotation {0} has expired.”.format(source\_name).

**Local steps**

- Set supplier\_quotation from Platform.get\_doc(“Supplier Quotation”, source\_name).
- If supplier\_quotation.get\_status() at “status” equals “Expired”.
  - Call the validation error handler Platform.throw(translated “Supplier Quotation {0} has expired.”.format(source\_name)).
- If args is identical to no value.
  - Set args from mapping().
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set qty\_to\_order from get\_qty\_to\_order(supplier\_quotation.items, “supplier\_quotation\_item”).
- Set mapped\_items from get\_qty\_already\_mapped(target\_doc, “supplier\_quotation\_item”).
- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Bind local operation select\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Supplier Quotation”, source\_name, mapping(“Supplier Quotation” → mapping(“doctype” → “Purchase Order”, “field\_no\_map” → list(“transaction\_date”), “validation” → mapping(“docstatus” → list(“ ….
- Return doclist.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L835) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L75)

<a id="op-a0c7dd88a2fdab"></a>
### Make purchase order.set missing values

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_make_purchase_order_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“get\_schedule\_dates”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“get\_schedule\_dates”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L837) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L77)

<a id="op-81cbfcbff50a9d"></a>
### Make purchase order.update item

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_make_purchase_order_update_item`

**Inputs** obj, target, source\_parent.

**Local steps**

- Set target.qty from max(qty\_to\_order at obj.name, 0).
- Set target.stock\_qty from (target.qty × flt(obj.conversion\_factor)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L838) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L78)

<a id="op-37296a9ced9784"></a>
### Make purchase order.select item

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_make_purchase_order_select_item`

**Inputs** d.

**Explicit results** child\_filter.

**Local steps**

- Set filtered\_items from args.get(“filtered\_children”, list()).
- Set child\_filter from d.name belongs to filtered\_items when filtered\_items, otherwise true.
  - Value choice on filtered\_items — true gives d.name belongs to filtered\_items, false gives true.
- Return child\_filter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L836) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L76)

<a id="op-d167d9b19b8f2a"></a>
### Make purchase invoice

`operation_enterprise_binding_enterprise_buying_doctype_supplier_quotation_supplier_quotation_make_purchase_invoice`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist(), record a compatibility advisory for the invoked interface.

**Explicit results** doc.

**Local steps**

- Set doc from get\_mapped\_doc(“Supplier Quotation”, source\_name, mapping(“Supplier Quotation” → mapping(“doctype” → “Purchase Invoice”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Supplier Quotation Item” → map ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L834) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L74)
