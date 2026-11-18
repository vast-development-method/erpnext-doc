# Sales · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Customers without any sales transactions

<a id="op-46670e22136f28"></a>
### Get columns

`operation_enterprise_binding_enterprise_selling_report_customers_without_any_sales_transactions_customers_without_any_sales_transactions_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“label” → translated “Customer Name”, “fieldname” → “customer\_name”, “field ….

**Local steps**

- Return list(mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“label” → translated “Customer Name”, “fieldname” → “customer\_name”, “field ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L101)

<a id="op-d8524a44b525a0"></a>
### Get data

`operation_enterprise_binding_enterprise_selling_report_customers_without_any_sales_transactions_customers_without_any_sales_transactions_get_data`

**Inputs** filters = no value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set company from (filters or mapping()).get(“company”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If company.
  - Evaluate Platform.has\_permission(“Company”, doc = company, throw = true).
- Set customer from Platform.qb.DocType(“Customer”).
- Set query from Platform.qb.from\_(customer).select(customer.name.as\_(“customer”), customer.customer\_name, customer.territory, customer.customer\_group).
- For each doctype in SALES\_DOCTYPES.
  - Set query from query.where(ExistsCriterion(get\_submitted\_sales(customer, doctype, company)).negate()).
- If condition bound to get\_allowed\_masters\_condition(customer.name, “Customer”).
  - Set query from query.where(condition).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, doc = company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L102)

<a id="op-1dba66bd5efcac"></a>
### Get submitted sales

`operation_enterprise_binding_enterprise_selling_report_customers_without_any_sales_transactions_customers_without_any_sales_transactions_get_submitted_sales`

**Inputs** customer, doctype, company = no value.

**Explicit results** query.

**Local steps**

- Set sales from Platform.qb.DocType(doctype).
- Set query from nested operand in the contract.qb.from\_(sales).select(sales.name).where((sales.customer equals customer.name bitwise and sales.docstatus equals 1)).
- If company.
  - Set query from query.where(sales.company equals company).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L103)

## Report · Inactive customers

<a id="op-a615fdbbdb2134"></a>
### Execute

`operation_enterprise_selling_report_inactive_customers_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(doctype), get\_data(doctype, days\_since\_last\_order)).

**Explicit failure paths** validation helper — translated “Invalid value {0} for 'Doctype'”.format(doctype) · validation helper — translated “'Days Since Last Order' must be greater than zero”.

**Local steps**

- Set filters from (filters or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set doctype from filters.get(“doctype”).
- If doctype does not belong to tuple(“Sales Order”, “Sales Invoice”).
  - Call the validation error handler Platform.throw(translated “Invalid value {0} for 'Doctype'”.format(doctype)).
- Evaluate check\_doctype\_access(doctype).
- Set days\_since\_last\_order from cint(filters.get(“days\_since\_last\_order”)).
- <a id="op-a615fdbbdb2134-guard-11"></a>If days\_since\_last\_order ≤ 0.
  - Call the validation error handler Platform.throw(translated “'Days Since Last Order' must be greater than zero”).
- Return tuple(get\_columns(doctype), get\_data(doctype, days\_since\_last\_order)).

**Derived branch illustrations**

- At the comparison days\_since\_last\_order ≤ 0, days\_since\_last\_order = 0 selects the branch that calls the validation-error handler with translated “'Days Since Last Order' must be greater than zero”. With days\_since\_last\_order = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-a615fdbbdb2134-guard-11)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L12)

<a id="op-923b8f5f3f31b4"></a>
### Get data

`operation_enterprise_binding_enterprise_selling_report_inactive_customers_inactive_customers_get_data`

**Inputs** doctype, days\_since\_last\_order.

**Explicit results** rows.

**Local steps**

- Set rows from list of row for row drawn from get\_sales\_details(doctype) where cint(row.days\_since\_last\_order) ≥ days\_since\_last\_order.
  - Draw row from get\_sales\_details(doctype), keep a combination only if (cint(row.days\_since\_last\_order) ≥ days\_since\_last\_order).
- Set last\_amounts from get\_last\_order\_amounts(doctype, list of row.customer for row drawn from rows) when rows, otherwise mapping().
  - Value choice on rows — true gives get\_last\_order\_amounts(doctype, list of row.customer for row drawn from rows), false gives mapping().
  - Draw row from rows.
- For each row in rows.
  - Set row.last\_order\_amount from last\_amounts.get(row.customer, 0).
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L105)

<a id="op-515c3de76fddc2"></a>
### Get sales details

`operation_enterprise_selling_report_inactive_customers_business_behavior_get_sales_details`

**Inputs** doctype.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- Set customer from Platform.qb.DocType(“Customer”).
- Set sales from Platform.qb.DocType(doctype).
- Set date\_diff from CustomFunction(“DATEDIFF”, list(“d1”, “d2”)).
- Set current\_date from CustomFunction(“CURRENT\_DATE”, list()).
- If doctype equals “Sales Order”.
  - Set date\_col from sales.transaction\_date.
  - Set considered from Sum(Case().when(sales.status equals “Closed”, ((nested operand in the contract.base\_net\_total × nested operand in the contract.per\_delivered) ÷ 100)).else\_(sales.base\_net\_total)).
  - Set num\_of\_order from Count(sales.name).distinct().
  - Set last\_order\_date from Max(date\_col).
- Otherwise.
  - Set date\_col from sales.posting\_date.
  - Set considered from Sum(sales.base\_net\_total).
  - Set not\_return from sales.is\_return equals 0.
  - Set num\_of\_order from Count(Case().when(not\_return, sales.name)).distinct().
  - Set last\_order\_date from Max(Case().when(not\_return, date\_col)).
- Set days\_since\_last\_order from date\_diff(current\_date(), last\_order\_date).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.docsta ….
- Set permitted from get\_permitted\_customers().
- Set sales\_permitted from get\_sales\_permitted\_customers(doctype).
- If (permitted equals list() or sales\_permitted equals list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in permitted equals list() → sales\_permitted equals list().
  - Return list().
- If permitted is distinct from no value.
  - Set query from query.where(customer.name.isin(permitted)).
- If sales\_permitted is distinct from no value.
  - Set query from query.where(customer.name.isin(sales\_permitted)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L14)

<a id="op-5a5d035b900d54"></a>
### Get last order amounts

`operation_enterprise_binding_enterprise_selling_report_inactive_customers_inactive_customers_get_last_order_amounts`

**Inputs** doctype, customers.

**Explicit results** mapping of customer → amount for tuple(customer, amount) drawn from result.

**Local steps**

- Set sales from Platform.qb.DocType(doctype).
- Set date\_col from sales.transaction\_date when doctype equals “Sales Order”, otherwise sales.posting\_date.
  - Value choice on doctype equals “Sales Order” — true gives sales.transaction\_date, false gives sales.posting\_date.
- Set ranked from nested operand in the contract.qb.from\_(sales).select(sales.customer, sales.base\_net\_total, nested operand in the contract.orderby(date\_col, nested operand in the contract.name, order = nested operand in t ….
- If doctype equals “Sales Invoice”.
  - Set ranked from ranked.where(sales.is\_return equals 0).
- Set ranked from ranked.as\_(“ranked”).
- Set result from nested operand in the contract(nested operand in the contract).select(ranked.customer, ranked.base\_net\_total).where(ranked.rn equals 1).run().
- Return mapping of customer → amount for tuple(customer, amount) drawn from result.
  - Draw tuple(customer, amount) from result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L106)

<a id="op-0b94e20e2fd76a"></a>
### Check doctype access

`operation_enterprise_binding_enterprise_selling_report_inactive_customers_inactive_customers_check_doctype_access`

**Inputs** doctype.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “User {0} has no read or select permission on {1}”.format(Platform.session.user, translated doctype).

**Local steps**

- If not (Platform.has\_permission(doctype, “select”) or Platform.has\_permission(doctype, “read”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.has\_permission(doctype, “select”) → Platform.has\_permission(doctype, “read”).
  - Call the validation error handler Platform.throw(translated “User {0} has no read or select permission on {1}”.format(Platform.session.user, translated doctype), Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “select”), Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L104)

<a id="op-e122ea1991b658"></a>
### Get permitted customers

`operation_enterprise_binding_enterprise_selling_report_inactive_customers_inactive_customers_get_permitted_customers`

**Inputs** no declared parameters.

**Record and data access** read “Customer” via get\_list.

**Explicit results** no value · Platform.get\_list(“Customer”, pluck = “name”, limit\_page\_length = 0).

**Local steps**

- Set user\_permissions from get\_user\_permissions(Platform.session.user).
- If not user\_permissions.
  - Return no value.
- Set gating from set of df.options for df drawn from Platform.get\_meta(“Customer”).get\_link\_fields().
  - Draw df from Platform.get\_meta(“Customer”).get\_link\_fields().
- Evaluate gating.add(“Customer”).
- If not gating.intersection(user\_permissions).
  - Return no value.
- Return Platform.get\_list(“Customer”, pluck = “name”, limit\_page\_length = 0).

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L107)

<a id="op-b9f7f024b9abd3"></a>
### Get sales permitted customers

`operation_enterprise_binding_enterprise_selling_report_inactive_customers_inactive_customers_get_sales_permitted_customers`

**Inputs** doctype.

**Record and data access** read doctype via get\_list.

**Explicit results** no value · Platform.get\_list(doctype, pluck = “customer”, distinct = true, limit\_page\_length = 0).

**Local steps**

- If not get\_user\_permissions(Platform.session.user).
  - Return no value.
- Return Platform.get\_list(doctype, pluck = “customer”, distinct = true, limit\_page\_length = 0).

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L108)

<a id="op-2b6dbcbe3dca0c"></a>
### Get columns

`operation_enterprise_selling_report_inactive_customers_business_behavior_get_columns`

**Inputs** doctype.

**Explicit results** list(mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“label” → translated “Customer Name”, “fieldname” → “customer\_name”, “field ….

**Local steps**

- Set noun from “Order” when doctype equals “Sales Order”, otherwise “Invoice”.
  - Value choice on doctype equals “Sales Order” — true gives “Order”, false gives “Invoice”.
- Return list(mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“label” → translated “Customer Name”, “fieldname” → “customer\_name”, “field ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L13)

## Record · Installation note

[Record definition](../../../../data/record-types/installation_note.json)

<a id="op-0a263f090a9148"></a>
### Installation Note.initialize

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Installation Note Item”, “target\_dt” → “Delivery Note Item”, “target\_field” → “installed\_qty”, “target\_ref\_field” → “qty”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0628.json#L6700) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1806) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1198)

<a id="op-712de002e041f2"></a>
### Installation Note.validate

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_installation\_date().
- Evaluate self.check\_item\_table().
- Evaluate self.validate\_with\_previous\_doc().
- Bind dependencies set\_default\_income\_account\_for\_item.
- Evaluate set\_default\_income\_account\_for\_item(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate installation date](operations-006.md#op-59e918daad56c7), [check item table](operations-006.md#op-a768065575a73d), [validate with previous doc](operations-006.md#op-ddcecdff1c548b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1205)

<a id="op-ddcecdff1c548b"></a>
### Installation Note.validate with previous doc

`operation_enterprise_binding_enterprise_selling_doctype_installation_note_installation_note_installationnote_validate_with_previous_doc`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_prevdoc\_references().
- Evaluate super().validate\_with\_previous\_doc(mapping(“Delivery Note” → mapping(“ref\_dn\_field” → “prevdoc\_docname”, “compare\_fields” → list(list(“customer”, “=”), list(“company”, “=”))), “Delivery Note Item” → mappin ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate prevdoc references](operations-006.md#op-c859c986db21fe).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1478)

<a id="op-c859c986db21fe"></a>
### Installation Note.validate prevdoc references

`operation_enterprise_binding_enterprise_selling_doctype_installation_note_installation_note_installationnote_validate_prevdoc_references`

**Inputs** self.

**Record and data access** read “Delivery Note Item” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Installation can only be recorded against a submitted Delivery Note”.format(d.idx) · validation helper — translated “Row #{0}: Delivery Note Item does not belong to Delivery Note {1}”.format(d.idx, escape\_html(cstr(d.prevdoc\_docname))).

**Local steps**

- For each d in self.get(“items”).
  - If not d.prevdoc\_detail\_docname.
    - Continue with the next iteration or loop test.
  - Set dn\_item from Platform.db.get\_value(“Delivery Note Item”, d.prevdoc\_detail\_docname, list(“parent”, “docstatus”), as\_dict = true).
  - If (not dn\_item or dn\_item.docstatus differs from 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not dn\_item → dn\_item.docstatus differs from 1.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Installation can only be recorded against a submitted Delivery Note”.format(d.idx)).
  - If dn\_item.parent differs from d.prevdoc\_docname.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery Note Item does not belong to Delivery Note {1}”.format(d.idx, escape\_html(cstr(d.prevdoc\_docname)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1477)

<a id="op-cb84a2788f9391"></a>
### Installation Note.is serial no added

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_is_serial_number_added`

**Inputs** self, item\_code, serial\_no.

**Record and data access** read “Item” via get\_value.

**Explicit failure paths** validation helper — translated “Serial No is mandatory for Item {0}”.format(item\_code) · validation helper — translated “Item {0} is not a serialized Item”.format(item\_code).

**Local steps**

- Set has\_serial\_no from Platform.db.get\_value(“Item”, item\_code, “has\_serial\_no”).
- If (has\_serial\_no equals 1 and not serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_serial\_no equals 1 → not serial\_no.
  - Call the validation error handler Platform.throw(translated “Serial No is mandatory for Item {0}”.format(item\_code)).
- Otherwise.
  - If (has\_serial\_no differs from 1 and cstr(serial\_no).strip()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_serial\_no differs from 1 → cstr(serial\_no).strip().
    - Call the validation error handler Platform.throw(translated “Item {0} is not a serialized Item”.format(item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0628.json#L7094) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1807) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1199)

<a id="op-b1160fbd166faf"></a>
### Installation Note.is serial no exist

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_is_serial_number_exist`

**Inputs** self, item\_code, serial\_no.

**Record and data access** read “Serial No” via exists.

**Explicit failure paths** validation helper — translated “Serial No {0} does not exist”.format(x).

**Local steps**

- For each x in serial\_no.
  - If not Platform.db.exists(“Serial No”, x).
    - Call the validation error handler Platform.throw(translated “Serial No {0} does not exist”.format(x)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0628.json#L7392) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1200)

<a id="op-ae2a1bbac1e73a"></a>
### Installation Note.get prevdoc serial no

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_get_prevdoc_serial_number`

**Inputs** self, prevdoc\_detail\_docname.

**Record and data access** read “Delivery Note Item” via get\_value.

**Explicit results** get\_valid\_serial\_nos(serial\_nos).

**Local steps**

- Set serial\_nos from Platform.db.get\_value(“Delivery Note Item”, prevdoc\_detail\_docname, “serial\_no”).
- Return get\_valid\_serial\_nos(serial\_nos).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0628.json#L7551) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1805) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1197)

<a id="op-9dddb14a6da56a"></a>
### Installation Note.is serial no match

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_is_serial_number_match`

**Inputs** self, cur\_s\_no, prevdoc\_s\_no, prevdoc\_docname.

**Explicit failure paths** validation helper — translated “Serial No {0} does not belong to Delivery Note {1}”.format(sr, prevdoc\_docname).

**Local steps**

- For each sr in cur\_s\_no.
  - If sr does not belong to prevdoc\_s\_no.
    - Call the validation error handler Platform.throw(translated “Serial No {0} does not belong to Delivery Note {1}”.format(sr, prevdoc\_docname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1201)

<a id="op-b601995ef8f802"></a>
### Installation Note.validate serial no

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_validate_serial_number`

**Inputs** self.

**Local steps**

- Set tuple(prevdoc\_s\_no, sr\_list) from tuple(list(), list()).
- For each d in self.get(“items”).
  - Evaluate self.is\_serial\_no\_added(d.item\_code, d.serial\_no).
  - If d.serial\_no.
    - Set sr\_list from get\_valid\_serial\_nos(d.serial\_no, d.qty, d.item\_code).
    - Evaluate self.is\_serial\_no\_exist(d.item\_code, sr\_list).
    - Set prevdoc\_s\_no from self.get\_prevdoc\_serial\_no(d.prevdoc\_detail\_docname).
    - If prevdoc\_s\_no.
      - Evaluate self.is\_serial\_no\_match(sr\_list, prevdoc\_s\_no, d.prevdoc\_docname).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is serial no added](operations-006.md#op-cb84a2788f9391), [is serial no exist](operations-006.md#op-b1160fbd166faf), [get prevdoc serial no](operations-006.md#op-ae2a1bbac1e73a), [is serial no match](operations-006.md#op-9dddb14a6da56a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1207)

<a id="op-59e918daad56c7"></a>
### Installation Note.validate installation date

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_validate_installation_date`

**Inputs** self.

**Record and data access** read “Delivery Note” via get\_value.

**Explicit failure paths** validation helper — translated “Installation date cannot be before delivery date for Item {0}”.format(d.item\_code).

**Local steps**

- For each d in self.get(“items”).
  - If d.prevdoc\_docname.
    - Set d\_date from Platform.db.get\_value(“Delivery Note”, d.prevdoc\_docname, “posting\_date”).
    - If d\_date &gt; getdate(self.inst\_date).
      - Call the validation error handler Platform.throw(translated “Installation date cannot be before delivery date for Item {0}”.format(d.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L473) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1206)

<a id="op-a768065575a73d"></a>
### Installation Note.check item table

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_check_item_table`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please pull items from Delivery Note”.

**Local steps**

- If not self.get(“items”).
  - Call the validation error handler Platform.throw(translated “Please pull items from Delivery Note”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L709) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1804) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1196)

<a id="op-feda972e930fac"></a>
### Installation Note.on update

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_on_update`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Draft”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L815) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1204)

<a id="op-36b260d446dcb6"></a>
### Installation Note.on submit

`operation_enterprise_selling_record_definitions_installation_note_business_behavior_installation_note_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.validate\_serial\_no().
- Evaluate self.update\_prevdoc\_status().
- Evaluate self.db\_set(“status”, “Submitted”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate serial no](operations-006.md#op-b601995ef8f802).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0629.json#L878) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1203)
