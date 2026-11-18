# Inventory and warehouses · operations 66

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Serial no ledger

<a id="op-031ff58fd25f15"></a>
### Get columns

`operation_enterprise_stock_report_serial_number_ledger_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Posting Date”, “fieldtype” → “Date”, “fieldname” → “posting\_date”, “width” → 120), mapping(“label” → translated “Posting Time”, “fieldtype” → “Time”, “fieldname” → “posti ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L305)

<a id="op-57de4767107812"></a>
### Get data

`operation_enterprise_stock_report_serial_number_ledger_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Stock Entry” via get\_cached\_value · read row.voucher\_type via get\_value.

**Explicit results** list() · data.

**Local steps**

- Set filters from Platform.\_dict(filters).
- Set filters.posting\_date from (filters.get(“posting\_date”) or today()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“posting\_date”) → today().
- If (isinstance(filters.get(“warehouse”), str) and filters.warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(filters.get(“warehouse”), str) → filters.warehouse.
  - Set filters.warehouse from list(filters.warehouse, expanded get\_descendants\_of(“Warehouse”, filters.warehouse)).
- Set stock\_ledgers from get\_stock\_ledger\_entries(filters, “&lt;=”, order = “asc”, check\_serial\_no = false).
- If not stock\_ledgers.
  - Return list().
- Set data from list().
- Set serial\_bundle\_ids from list of d.serial\_and\_batch\_bundle for d drawn from stock\_ledgers where d.serial\_and\_batch\_bundle.
  - Draw d from stock\_ledgers, keep a combination only if (d.serial\_and\_batch\_bundle).
- Set bundle\_wise\_serial\_nos from get\_serial\_nos(filters, serial\_bundle\_ids).
- For each row in stock\_ledgers.
  - Set args from Platform.\_dict(mapping(“posting\_date” → row.posting\_date, “posting\_time” → row.posting\_time, “voucher\_type” → row.voucher\_type, “voucher\_no” → row.voucher\_no, …)).
    - Value choice on row.actual\_qty &gt; 0 — true gives 1, false gives negative 1.
  - If (row.voucher\_type equals “Stock Entry” and row.actual\_qty &lt; 0 and Platform.get\_cached\_value(“Stock Entry”, row.voucher\_no, “purpose”) belongs to tuple(“Material Transfer”, “Material Transfer for Manufacture”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.voucher\_type equals “Stock Entry” → row.actual\_qty &lt; 0 → Platform.get\_cached\_value(“Stock Entry”, row.voucher\_no, “purpose”) belongs to tuple(“Material Transfer”, “Material Transfer for Manufacture”).
    - Set args.status from “Active”.
  - Set party\_field from “supplier” when row.voucher\_type belongs to BUYING\_VOUCHER\_TYPES, otherwise “customer” when row.voucher\_type belongs to SELLING\_VOUCHER\_TYPES, otherwise no value.
    - Value choice on row.voucher\_type belongs to BUYING\_VOUCHER\_TYPES — true gives “supplier”, false gives “customer” when row.voucher\_type belongs to SELLING\_VOUCHER\_TYPES, otherwise no value.
    - Value choice on row.voucher\_type belongs to SELLING\_VOUCHER\_TYPES — true gives “customer”, false gives no value.
  - Set args.party\_type from party\_field.title() when party\_field, otherwise no value.
    - Value choice on party\_field — true gives party\_field.title(), false gives no value.
  - Set args.party from Platform.db.get\_value(row.voucher\_type, row.voucher\_no, party\_field) when party\_field, otherwise no value.
    - Value choice on party\_field — true gives Platform.db.get\_value(row.voucher\_type, row.voucher\_no, party\_field), false gives no value.
  - Set serial\_nos from list().
  - If row.serial\_no.
    - Set parsed\_serial\_nos from get\_serial\_nos\_from\_sle(row.serial\_no).
    - For each serial\_no in parsed\_serial\_nos.
      - If (filters.get(“serial\_no”) and filters.get(“serial\_no”) differs from serial\_no).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“serial\_no”) → filters.get(“serial\_no”) differs from serial\_no.
        - Continue with the next iteration or loop test.
      - Evaluate serial\_nos.append(mapping(“serial\_no” → serial\_no, “valuation\_rate” → abs((row.stock\_value\_difference ÷ row.actual\_qty)))).
  - If row.serial\_and\_batch\_bundle.
    - Evaluate serial\_nos.extend(bundle\_wise\_serial\_nos.get(row.serial\_and\_batch\_bundle, list())).
  - For each bundle\_data in serial\_nos.
    - Set new\_args from args.copy().
    - Set new\_args.serial\_no from bundle\_data.get(“serial\_no”).
    - Set new\_args.valuation\_rate from bundle\_data.get(“valuation\_rate”).
    - Evaluate data.append(new\_args).
- Return data.

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_value(“Stock Entry”, row.voucher\_no, “purpose”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0041.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L306)

<a id="op-899c99a1e08d2c"></a>
### Get serial nos

`operation_enterprise_stock_report_serial_number_ledger_business_behavior_get_serial_numbers`

**Inputs** filters, serial\_bundle\_ids.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** bundle\_wise\_serial\_nos.

**Local steps**

- Set bundle\_wise\_serial\_nos from mapping().
- Set bundle\_filters from mapping(“parent” → list(“in”, serial\_bundle\_ids)).
- If filters.get(“serial\_no”).
  - Set bundle\_filters at “serial\_no” from filters.get(“serial\_no”).
- For each d in Platform.get\_all(“Serial and Batch Entry”, fields = list(“serial\_no”, “parent”, “stock\_value\_difference as valuation\_rate”), filters = bundle\_filters, order\_by = “idx asc”).
  - Evaluate bundle\_wise\_serial\_nos.setdefault(d.parent, list()).append(mapping(“serial\_no” → d.serial\_no, “valuation\_rate” → abs(d.valuation\_rate))).
- Return bundle\_wise\_serial\_nos.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0903.json#L4004) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L307)

## Record · Shipment

[Record definition](../../../../data/record-types/shipment.json)

<a id="op-c76d8ab6ebf4a2"></a>
### Shipment.on discard

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0820.json#L7482) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1093) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L703)

<a id="op-0bc5bd5c773cf1"></a>
### Shipment.validate

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_weight().
- Evaluate self.validate\_pickup\_time().
- Evaluate self.validate\_parties().
- Evaluate self.validate\_delivery\_notes().
- Evaluate self.set\_value\_of\_goods().
- Evaluate self.set\_total\_weight().
- <a id="op-0bc5bd5c773cf1-guard-8"></a>If self.docstatus equals 0.
  - Set self.status from “Draft”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that assigns “Draft” to self.status. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0bc5bd5c773cf1-guard-8)

**Methods declared on this owner** [validate weight](operations-066.md#op-6ddd09d8d0f90d), [validate pickup time](operations-066.md#op-e57495910ed69f), [validate parties](operations-066.md#op-902ecf21865531), [validate delivery notes](operations-066.md#op-d5c0453e4f9527), [set value of goods](operations-066.md#op-bc37cefe6e19dd), [set total weight](operations-066.md#op-3b024c9a325eb9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1097) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L707)

<a id="op-3a3bb865f1a8a7"></a>
### Shipment.before update after submit

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_shipment_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_pickup\_time().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate pickup time](operations-066.md#op-e57495910ed69f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L597)

<a id="op-aa570ce4986ac8"></a>
### Shipment.on submit

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Please enter Shipment Parcel information” · validation helper — translated “Value of goods must be greater than 0”.

**Local steps**

- If not self.shipment\_parcel.
  - Call the validation error handler Platform.throw(translated “Please enter Shipment Parcel information”).
- If flt(self.value\_of\_goods) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Value of goods must be greater than 0”).
- Evaluate self.db\_set(“status”, “Submitted”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1094) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L704)

<a id="op-009cae05d2f6de"></a>
### Shipment.on cancel

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L344) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1092) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L702)

<a id="op-6ddd09d8d0f90d"></a>
### Shipment.validate weight

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_validate_weight`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Parcel weight cannot be 0” · validation helper — translated “Row #{0}: Parcel count must be at least 1”.format(parcel.idx) · validation helper — translated “Row #{0}: Parcel {1} cannot be negative”.format(parcel.idx, translated parcel.meta.get\_label(fieldname)).

**Local steps**

- For each parcel in self.shipment\_parcel.
  - If flt(parcel.weight) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Parcel weight cannot be 0”).
  - If cint(parcel.count) &lt; 1.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Parcel count must be at least 1”.format(parcel.idx)).
  - For each fieldname in tuple(“length”, “width”, “height”).
    - If flt(parcel.get(fieldname)) &lt; 0.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Parcel {1} cannot be negative”.format(parcel.idx, translated parcel.meta.get\_label(fieldname))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1099) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L709)

<a id="op-3b024c9a325eb9"></a>
### Shipment.set total weight

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_set_total_weight`

**Inputs** self.

**Local steps**

- Set self.total\_weight from self.get\_total\_weight().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get total weight](operations-066.md#op-1bedb54ade8dc2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L535) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1095) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L705)

<a id="op-1bedb54ade8dc2"></a>
### Shipment.get total weight

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_get_total_weight`

**Inputs** self.

**Explicit results** sum(generator of (flt(parcel.weight) × parcel.count) for parcel drawn from self.shipment\_parcel where parcel.count &gt; 0).

**Local steps**

- Return sum(generator of (flt(parcel.weight) × parcel.count) for parcel drawn from self.shipment\_parcel where parcel.count &gt; 0).
  - Draw parcel from self.shipment\_parcel, keep a combination only if (parcel.count &gt; 0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L596) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1091) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L701)

<a id="op-e57495910ed69f"></a>
### Shipment.validate pickup time

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_validate_pickup_time`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Pickup To time should be greater than Pickup From time” · validation helper — translated “Pickup Date cannot be before today”.

**Local steps**

- If (self.pickup\_from and self.pickup\_to and get\_time(self.pickup\_to) ≤ get\_time(self.pickup\_from)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.pickup\_from → self.pickup\_to → get\_time(self.pickup\_to) ≤ get\_time(self.pickup\_from).
  - Call the validation error handler Platform.throw(translated “Pickup To time should be greater than Pickup From time”).
- If ((self.is\_new() or self.has\_value\_changed(“pickup\_date”)) and getdate(self.pickup\_date) &lt; getdate()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.is\_new() or self.has\_value\_changed(“pickup\_date”)) → getdate(self.pickup\_date) &lt; getdate().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_value\_changed(“pickup\_date”).
  - Call the validation error handler Platform.throw(translated “Pickup Date cannot be before today”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1098) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L708)

<a id="op-902ecf21865531"></a>
### Shipment.validate parties

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_shipment_validate_parties`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is required for the {1} party”.format(translated party\_type, translated side.title()).

**Local steps**

- For each tuple(side, party\_type) in tuple(tuple(“pickup”, self.pickup\_from\_type), tuple(“delivery”, self.delivery\_to\_type)).
  - Set party from self.get(formatted text {side}\_{Platform.scrub(party\_type)}).
  - If not party.
    - Call the validation error handler Platform.throw(translated “{0} is required for the {1} party”.format(translated party\_type, translated side.title())).
  - For each other\_type in tuple(“Company”, “Customer”, “Supplier”).
    - If other\_type differs from party\_type.
      - Evaluate self.set(formatted text {side}\_{Platform.scrub(other\_type)}, no value).
  - Evaluate self.set(“pickup” when side equals “pickup”, otherwise “delivery\_to”, party).
    - Value choice on side equals “pickup” — true gives “pickup”, false gives “delivery\_to”.
  - If (self.is\_new() or self.has\_party\_details\_changed(side)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_party\_details\_changed(side).
    - Evaluate self.validate\_party\_links(side, party\_type, party).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has party details changed](operations-066.md#op-9756978eaeb207), [validate party links](operations-066.md#op-a75bea98599e73).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L601)

<a id="op-9756978eaeb207"></a>
### Shipment.has party details changed

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_shipment_has_party_details_changed`

**Inputs** self, side.

**Explicit results** any(generator of self.has\_value\_changed(formatted text {side}\_{fieldname}) for fieldname drawn from tuple(“company”, “customer”, “supplier”, “address\_name”, …)).

**Local steps**

- Return any(generator of self.has\_value\_changed(formatted text {side}\_{fieldname}) for fieldname drawn from tuple(“company”, “customer”, “supplier”, “address\_name”, …)).
  - Draw fieldname from tuple(“company”, “customer”, “supplier”, “address\_name”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L598)

<a id="op-a75bea98599e73"></a>
### Shipment.validate party links

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_shipment_validate_party_links`

**Inputs** self, side, party\_type, party.

**Explicit failure paths** validation helper — translated “{0} {1} is not linked to {2} {3}”.format(translated doctype, bold(name), translated party\_type, bold(party)).

**Local steps**

- For each tuple(doctype, fieldname) in tuple(tuple(“Address”, formatted text {side}\_address\_name), tuple(“Contact”, formatted text {side}\_contact\_name)).
  - Set name from self.get(fieldname).
  - If (name and not is\_linked\_to\_party(doctype, name, party\_type, party)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in name → not is\_linked\_to\_party(doctype, name, party\_type, party).
    - Call the validation error handler Platform.throw(translated “{0} {1} is not linked to {2} {3}”.format(translated doctype, bold(name), translated party\_type, bold(party))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L602)

<a id="op-d5c0453e4f9527"></a>
### Shipment.validate delivery notes

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_shipment_validate_delivery_notes`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Delivery Note {1} is added more than once”.format(row.idx, bold(row.delivery\_note)).

**Local steps**

- Set delivery\_notes from set().
- For each row in self.get(“shipment\_delivery\_note”).
  - If row.delivery\_note belongs to delivery\_notes.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery Note {1} is added more than once”.format(row.idx, bold(row.delivery\_note))).
  - Evaluate delivery\_notes.add(row.delivery\_note).
  - Evaluate self.validate\_delivery\_note\_row(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate delivery note row](operations-066.md#op-ec137fc688eb62).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L600)

<a id="op-ec137fc688eb62"></a>
### Shipment.validate delivery note row

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_shipment_validate_delivery_note_row`

**Inputs** self, row.

**Record and data access** read “Delivery Note” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Delivery Note {1} must be submitted”.format(row.idx, bold(row.delivery\_note)) · validation helper — translated “Row #{0}: Delivery Note {1} belongs to Customer {2}”.format(row.idx, bold(row.delivery\_note), bold(delivery\_note.customer)) · validation helper — translated “Row #{0}: Delivery Note {1} is already in Shipment {2}”.format(row.idx, bold(row.delivery\_note), get\_link\_to\_form(“Shipment”, shipment)).

**Local steps**

- Set lock from self.docstatus equals 1.
- Set delivery\_note from Platform.db.get\_value(“Delivery Note”, row.delivery\_note, list(“docstatus”, “customer”, “base\_grand\_total”), as\_dict = true, for\_update = lock).
- <a id="op-ec137fc688eb62-guard-10"></a>If delivery\_note.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery Note {1} must be submitted”.format(row.idx, bold(row.delivery\_note))).
- If (self.delivery\_to\_type equals “Customer” and delivery\_note.customer differs from self.delivery\_customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.delivery\_to\_type equals “Customer” → delivery\_note.customer differs from self.delivery\_customer.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery Note {1} belongs to Customer {2}”.format(row.idx, bold(row.delivery\_note), bold(delivery\_note.customer))).
- If shipment bound to get\_other\_shipment(row.delivery\_note, self.name, for\_update = lock).
  - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery Note {1} is already in Shipment {2}”.format(row.idx, bold(row.delivery\_note), get\_link\_to\_form(“Shipment”, shipment))).
- Set row.grand\_total from delivery\_note.base\_grand\_total.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison delivery\_note.docstatus differs from 1, delivery\_note.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Row #{0}: Delivery Note {1} must be submitted”.format(row.idx, bold(row.delivery\_note)). With delivery\_note.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ec137fc688eb62-guard-10)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L599)

<a id="op-bc37cefe6e19dd"></a>
### Shipment.set value of goods

`operation_enterprise_stock_record_definitions_shipment_business_behavior_shipment_set_value_of_goods`

**Inputs** self.

**Local steps**

- Set value\_of\_goods from 0.
- For each entry in self.get(“shipment\_delivery\_note”).
  - Update value\_of\_goods using + flt(entry.get(“grand\_total”)).
- Set self.value\_of\_goods from value\_of\_goods when value\_of\_goods, otherwise self.value\_of\_goods.
  - Value choice on value\_of\_goods — true gives value\_of\_goods, false gives self.value\_of\_goods.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0821.json#L866) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1096) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L706)

<a id="op-e9e90041da364f"></a>
### Is linked to party

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_is_linked_to_party`

**Inputs** doctype, name, party\_type, party.

**Record and data access** read “Dynamic Link” via exists.

**Explicit results** bool(Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → doctype, “parent” → name, “link\_doctype” → party\_type, “link\_name” → party))).

**Local steps**

- Return bool(Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → doctype, “parent” → name, “link\_doctype” → party\_type, “link\_name” → party))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1099) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L596)

<a id="op-24308322d4d731"></a>
### Get other shipment

`operation_enterprise_binding_enterprise_stock_doctype_shipment_shipment_get_other_shipment`

**Inputs** delivery\_note, shipment\_name, for\_update = false.

**Explicit results** result at 0 at 0 when result, otherwise no value.

**Local steps**

- Set shipment from Platform.qb.DocType(“Shipment”).
- Set row from Platform.qb.DocType(“Shipment Delivery Note”).
- Set query from nested operand in the contract(nested operand in the contract).select(shipment.name).where(((nested operand in the contract.delivery\_note equals delivery\_note bitwise and nested operand in the contract.doc ….
- If for\_update.
  - Set query from query.for\_update().
- Set result from query.run().
- Return result at 0 at 0 when result, otherwise no value.
  - Value choice on result — true gives result at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1098) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L595)

<a id="op-f61d1b43e5dac5"></a>
### Get address name

`operation_enterprise_stock_record_definitions_shipment_business_behavior_get_address_name`

**Inputs** ref\_doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_party\_shipping\_address(ref\_doctype, docname).

**Local steps**

- Evaluate Platform.has\_permission(ref\_doctype, “select”, doc = docname, throw = true).
- Return get\_party\_shipping\_address(ref\_doctype, docname).

**Values supplied outside this operation** effective access from Platform.has\_permission(ref\_doctype, “select”, doc = docname, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1088) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L698)

<a id="op-a63f7f982dfe48"></a>
### Get contact name

`operation_enterprise_stock_record_definitions_shipment_business_behavior_get_contact_name`

**Inputs** ref\_doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_default\_contact(ref\_doctype, docname).

**Local steps**

- Evaluate Platform.has\_permission(ref\_doctype, “select”, doc = docname, throw = true).
- Return get\_default\_contact(ref\_doctype, docname).

**Values supplied outside this operation** effective access from Platform.has\_permission(ref\_doctype, “select”, doc = docname, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1090) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L700)

<a id="op-9cef6bf5799824"></a>
### Get company contact

`operation_enterprise_stock_record_definitions_shipment_business_behavior_get_company_contact`

**Inputs** user.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_value.

**Explicit results** contact.

**Local steps**

- Evaluate Platform.has\_permission(“Shipment”, “write”, throw = true).
- Set contact from Platform.db.get\_value(“User”, user, list(“first\_name”, “last\_name”, “email”, “phone”, …), as\_dict = 1).
- If not contact.phone.
  - Set contact.phone from contact.mobile\_no.
- Return contact.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Shipment”, “write”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1089) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L699)

## Record · Shipment parcel template

[Record definition](../../../../data/record-types/shipment_parcel_template.json)

<a id="op-5181e6ccebbe78"></a>
### Shipment Parcel Template.validate

`operation_enterprise_binding_enterprise_stock_doctype_shipment_parcel_template_shipment_parcel_template_shipmentparceltemplate_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} must be greater than 0”.format(Platform.bold(self.meta.get\_label(fieldname))).

**Local steps**

- For each fieldname in tuple(“length”, “width”, “height”, “weight”).
  - If flt(self.get(fieldname)) ≤ 0.
    - Call the validation error handler Platform.throw(translated “{0} must be greater than 0”.format(Platform.bold(self.meta.get\_label(fieldname)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1097) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L594)
