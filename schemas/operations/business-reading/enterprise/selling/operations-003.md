# Sales · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Customer

[Record definition](../../../../data/record-types/customer.json)

<a id="op-073a64792ba819"></a>
### Make quotation

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_make_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Record and data access** read “Customer” via get\_value.

**Explicit results** target\_doc.

**Local steps**

- Set target\_doc from get\_mapped\_doc(“Customer”, source\_name, mapping(“Customer” → mapping(“doctype” → “Quotation”, “field\_map” → mapping(“name” → “party\_name”))), target\_doc).
- Set target\_doc.quotation\_to from “Customer”.
- Set tuple(price\_list, currency) from Platform.db.get\_value(“Customer”, mapping(“name” → source\_name), list(“default\_price\_list”, “default\_currency”)).
- If price\_list.
  - Set target\_doc.selling\_price\_list from price\_list.
- If currency.
  - Set target\_doc.currency from currency.
- Evaluate target\_doc.run\_method(“set\_missing\_values”).
- Evaluate target\_doc.run\_method(“set\_other\_charges”).
- Evaluate target\_doc.run\_method(“calculate\_taxes\_and\_totals”).
- Return target\_doc.

**Values supplied outside this operation** selected callable from target\_doc.run\_method(“set\_missing\_values”), target\_doc.run\_method(“set\_other\_charges”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1446)

<a id="op-b84f7f5c0b669c"></a>
### Make opportunity

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_make_opportunity`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** target\_doc.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set target\_doc from get\_mapped\_doc(“Customer”, source\_name, mapping(“Customer” → mapping(“doctype” → “Opportunity”, “field\_map” → mapping(“name” → “party\_name”, “doctype” → “opportunity\_from”))), target\_doc, …).
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1442)

<a id="op-1fc5bf1561732a"></a>
### Make opportunity.set missing values

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_make_opportunity_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate \_set\_missing\_values(source, target).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1443)

<a id="op-5c863bf5dff96f"></a>
### Make payment entry

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_make_payment_entry`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** target\_doc.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set target\_doc from get\_mapped\_doc(“Customer”, source\_name, mapping(“Customer” → mapping(“doctype” → “Payment Entry”, “field\_map” → mapping(“name” → “party”))), target\_doc, …).
- Set target\_doc.party\_type from “Customer”.
- Set target\_doc.party\_name from target\_doc.party.
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1444)

<a id="op-96f8114d3aadac"></a>
### Make payment entry.set missing values

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_make_payment_entry_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate \_set\_missing\_values(source, target).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1445)

<a id="op-05cfa97b89e541"></a>
### Set missing values

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Address” via get\_value · read “Contact” via get\_value.

**Local steps**

- Bind dependencies get\_default\_address.
- Bind dependencies get\_default\_contact.
- Set address from source.customer\_primary\_address.
- If (not address or Platform.db.get\_value(“Address”, address, “disabled”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not address → Platform.db.get\_value(“Address”, address, “disabled”).
  - Set address from get\_default\_address(source.doctype, source.name).
- Set contact from (source.customer\_primary\_contact or get\_default\_contact(source.doctype, source.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.customer\_primary\_contact → get\_default\_contact(source.doctype, source.name).
- If address.
  - Set target.customer\_address from address.
- If contact.
  - Set target.contact\_person from contact.
  - Set tuple(target.contact\_display, target.contact\_email, target.contact\_mobile) from Platform.get\_value(“Contact”, contact, list(“full\_name”, “email\_id”, “mobile\_no”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1476)

<a id="op-053733892c0492"></a>
### Get loyalty programs

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_loyalty_programs`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Loyalty Program” via get\_all.

**Explicit results** lp\_details.

**Local steps**

- Set lp\_details from list().
- Set loyalty\_programs from Platform.get\_all(“Loyalty Program”, fields = list(“name”, “customer\_group”, “customer\_territory”), filters = list(list(“auto\_opt\_in”, “=”, 1), list(“from\_date”, “&lt;=”, today()), list(functions.IfNull(Field( ….
- For each loyalty\_program in loyalty\_programs.
  - If ((not loyalty\_program.customer\_group or doc.customer\_group belongs to get\_nested\_links(“Customer Group”, loyalty\_program.customer\_group)) and (not loyalty\_program.customer\_territory or doc.territory belong ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not loyalty\_program.customer\_group or doc.customer\_group belongs to get\_nested\_links(“Customer Group”, loyalty\_program.customer\_group)) → (not loyalty\_program.customer\_territory or doc.territory belongs to get\_nested\_links(“Territory”, loyalty\_program.customer\_territory)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not loyalty\_program.customer\_group → doc.customer\_group belongs to get\_nested\_links(“Customer Group”, loyalty\_program.customer\_group).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not loyalty\_program.customer\_territory → doc.territory belongs to get\_nested\_links(“Territory”, loyalty\_program.customer\_territory).
    - Evaluate lp\_details.append(loyalty\_program.name).
- Return lp\_details.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1158)

<a id="op-149e548c4d5c92"></a>
### Get nested links

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_nested_links`

**Inputs** link\_doctype, link\_name, ignore\_permissions = false.

**Explicit results** list(link\_name, expanded Platform.db.get\_descendants(link\_doctype, link\_name)).

**Local steps**

- Return list(link\_name, expanded Platform.db.get\_descendants(link\_doctype, link\_name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1159)

<a id="op-98d2196fbe9b11"></a>
### Is customer blocked

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_is_customer_blocked`

**Inputs** customer.

**Declared result** bool.

**Record and data access** read “Customer” via get\_value.

**Explicit results** false · (not release\_date or getdate(today()) &lt; getdate(release\_date)).

**Local steps**

- Set tuple(on\_hold, release\_date) from Platform.db.get\_value(“Customer”, customer, list(“on\_hold”, “release\_date”)).
- If not on\_hold.
  - Return false.
- Return (not release\_date or getdate(today()) &lt; getdate(release\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not release\_date → getdate(today()) &lt; getdate(release\_date).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1438)

<a id="op-2703f1844ec739"></a>
### Check credit limit

`operation_enterprise_selling_record_definitions_customer_business_behavior_check_credit_limit`

**Inputs** customer, company, ignore\_outstanding\_sales\_order = false, extra\_amount = 0.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**State and service calls** msgprint with message.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please contact your administrator to extend the credit limits for {0}.”.format(customer).

**Local steps**

- Set credit\_limit from get\_credit\_limit(customer, company).
- If not credit\_limit.
  - Return no value.
- Set customer\_outstanding from get\_customer\_outstanding(customer, company, ignore\_outstanding\_sales\_order).
- If extra\_amount &gt; 0.
  - Update customer\_outstanding using + flt(extra\_amount).
- Set customer\_outstanding from flt(customer\_outstanding, Platform.get\_precision(“Customer Credit Limit”, “credit\_limit”, get\_company\_currency(company))).
- If (credit\_limit &gt; 0 and customer\_outstanding &gt; credit\_limit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in credit\_limit &gt; 0 → customer\_outstanding &gt; credit\_limit.
  - Set message from translated “Credit limit has been crossed for customer {0} ({1}/{2})”.format(customer, customer\_outstanding, credit\_limit).
  - Update message using + text in the contract.
  - Set credit\_controller\_role from Platform.get\_single\_value(“Accounts Settings”, “credit\_controller”).
  - If (not credit\_controller\_role or credit\_controller\_role does not belong to Platform.get\_roles()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not credit\_controller\_role → credit\_controller\_role does not belong to Platform.get\_roles().
    - Set credit\_controller\_users from get\_credit\_controller\_users().
    - Set credit\_controller\_users\_formatted from list of get\_formatted\_email(user).replace(“&lt;”, “(”).replace(“&gt;”, “)”) for user drawn from credit\_controller\_users.
      - Draw user from credit\_controller\_users.
    - If not credit\_controller\_users\_formatted.
      - Call the validation error handler Platform.throw(translated “Please contact your administrator to extend the credit limits for {0}.”.format(customer)).
    - Set user\_list from text in the contract.format(text in the contract.join(credit\_controller\_users\_formatted)).
    - Update message using + translated “Please contact any of the following users to extend the credit limits for {0}: {1}”.format(customer, user\_list).
    - Set primary\_action from mapping(“label” → “Send Email”, “server\_action” → “Enterprise.selling.doctype.customer.customer.send\_emails”, “hide\_on\_success” → true, “args” → mapping(“customer” → customer, “company” → company)) when Pl ….
      - Value choice on Platform.has\_permission(“Customer”, ptype = “email”, doc = customer) — true gives mapping(“label” → “Send Email”, “server\_action” → “Enterprise.selling.doctype.customer.customer.send\_emails”, “hide\_on\_success” → true, “args” → mapping(“customer” → customer, “company” → company)), false gives no value.
    - Evaluate Platform.msgprint(message, title = translated “Credit Limit Crossed”, raise\_exception = 1, primary\_action = primary\_action).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “credit\_controller”) · effective access from Platform.get\_roles(), Platform.has\_permission(“Customer”, ptype = “email”, doc = customer).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1127)

<a id="op-dd5cf59b54dee9"></a>
### Send emails

`operation_enterprise_selling_record_definitions_customer_business_behavior_send_emails`

**Inputs** customer, company.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** sendmail.

**Local steps**

- Evaluate Platform.has\_permission(“Customer”, ptype = “email”, doc = customer, throw = true).
- Set currency from get\_company\_currency(company).
- Set outstanding from get\_customer\_outstanding(customer, company, is\_sales\_order\_credit\_check\_bypassed(customer, company)).
- Set subject from translated “Credit limit reached for customer {0}”.format(customer).
- Set message from translated “A transaction for customer {0} is blocked by its credit limit. Current outstanding: {1}, credit limit: {2}”.format(customer, fmt\_money(outstanding, currency = currency), fmt\_money(get\_credit\_li ….
- Evaluate Platform.sendmail(recipients = get\_credit\_controller\_users(), subject = subject, message = message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, ptype = “email”, doc = customer, throw = true) · service or queued work from Platform.sendmail(recipients = get\_credit\_controller\_users(), subject = subject, message = message).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1164)

<a id="op-02de4927e69f2f"></a>
### Get credit controller users

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_get_credit_controller_users`

**Inputs** no declared parameters.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** get\_users\_with\_role((credit\_controller\_role or “Sales Master Manager”)).

**Local steps**

- Set credit\_controller\_role from Platform.get\_single\_value(“Accounts Settings”, “credit\_controller”).
- Return get\_users\_with\_role((credit\_controller\_role or “Sales Master Manager”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in credit\_controller\_role → “Sales Master Manager”.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “credit\_controller”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L425) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1435)

<a id="op-41bcd6491a6e24"></a>
### Check overdue billing threshold

`operation_enterprise_selling_record_definitions_customer_business_behavior_check_overdue_billing_threshold`

**Inputs** customer, company.

**Declared result** no value.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Overdue Limit crossed for customer {0}. Overdue amount {1} exceeds the allowed limit {2}.”.format(customer, fmt\_money(overdue\_amount, currency = company\_currency), fmt\_money(threshold, currency ….

**Local steps**

- If not Platform.get\_single\_value(“Accounts Settings”, “enable\_overdue\_billing\_threshold”).
  - Return no value.
- Set threshold from get\_overdue\_billing\_threshold(customer, company).
- If not threshold.
  - Return no value.
- Set overdue\_amount from get\_customer\_overdue\_amount(customer, company).
- If overdue\_amount ≤ threshold.
  - Return no value.
- Set bypass\_role from Platform.get\_single\_value(“Accounts Settings”, “role\_allowed\_to\_bypass\_overdue\_billing”).
- If (bypass\_role and bypass\_role belongs to Platform.get\_roles()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bypass\_role → bypass\_role belongs to Platform.get\_roles().
  - Return no value.
- Set company\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Call the validation error handler Platform.throw(translated “Overdue Limit crossed for customer {0}. Overdue amount {1} exceeds the allowed limit {2}.”.format(customer, fmt\_money(overdue\_amount, currency = company\_currency), fmt\_money(thre ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “enable\_overdue\_billing\_threshold”), Platform.get\_single\_value(“Accounts Settings”, “role\_allowed\_to\_bypass\_overdue\_billing”) and 1 further calls · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0625.json#L3363) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1128)

<a id="op-8da8214470b9a9"></a>
### Get overdue billing threshold

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_overdue_billing_threshold`

**Inputs** customer, company.

**Declared result** float.

**Record and data access** read “Customer Credit Limit” via get\_value · read “Customer” via get\_cached\_value.

**Explicit results** flt(threshold).

**Local steps**

- Set threshold from Platform.db.get\_value(“Customer Credit Limit”, mapping(“parent” → customer, “parenttype” → “Customer”, “company” → company), “overdue\_billing\_threshold”).
- If not threshold.
  - Set customer\_group from Platform.get\_cached\_value(“Customer”, customer, “customer\_group”).
  - Set threshold from Platform.db.get\_value(“Customer Credit Limit”, mapping(“parent” → customer\_group, “parenttype” → “Customer Group”, “company” → company), “overdue\_billing\_threshold”).
- Return flt(threshold).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer”, customer, “customer\_group”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0625.json#L3843) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1161)

<a id="op-18b1710f2d8ec9"></a>
### Get customer overdue amount

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_customer_overdue_amount`

**Inputs** customer, company.

**Declared result** float.

**Explicit results** 0.0 · flt(sum(generator of get\_overdue\_portion(d, payable\_amounts.get(d.name)) for d drawn from invoices)).

**Local steps**

- Set invoices from get\_outstanding\_invoices\_for\_customer(customer, company).
- If not invoices.
  - Return 0.0.
- Set payable\_amounts from get\_past\_due\_payable\_amounts(list of d.name for d drawn from invoices).
  - Draw d from invoices.
- Return flt(sum(generator of get\_overdue\_portion(d, payable\_amounts.get(d.name)) for d drawn from invoices)).
  - Draw d from invoices.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0625.json#L4182) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1156)

<a id="op-09b88f577d292a"></a>
### Get outstanding invoices for customer

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_outstanding_invoices_for_customer`

**Inputs** customer, company.

**Declared result** list at Platform.\_dict.

**Explicit results** nested operand in the contract(nested operand in the contract).groupby(sales\_invoice.name, sales\_invoice.due\_date, sales\_invoice.base\_grand\_total).having(outstanding &gt; 0).run(as\_dict = true).

**Local steps**

- Bind dependencies Sum.
- Set ple from Platform.qb.DocType(“Payment Ledger Entry”).
- Set sales\_invoice from Platform.qb.DocType(“Sales Invoice”).
- Set outstanding from Sum(ple.amount).
- Return nested operand in the contract(nested operand in the contract).groupby(sales\_invoice.name, sales\_invoice.due\_date, sales\_invoice.base\_grand\_total).having(outstanding &gt; 0).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0625.json#L4425) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1160)

<a id="op-177dd1454e862f"></a>
### Get past due payable amounts

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_past_due_payable_amounts`

**Inputs** invoices.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of d.parent → flt(d.payable) for d drawn from rows.

**Local steps**

- Bind dependencies Sum.
- Set payment\_schedule from Platform.qb.DocType(“Payment Schedule”).
- Set rows from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.due\_date &lt; nested operand in the contract()).groupby(payment\_schedule.parent).run(as\_dict = true).
- Return mapping of d.parent → flt(d.payable) for d drawn from rows.
  - Draw d from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0625.json#L4996) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1163)

<a id="op-bf86d508b84c4b"></a>
### Get overdue portion

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_overdue_portion`

**Inputs** invoice, payable\_amount.

**Declared result** float.

**Explicit results** outstanding when (invoice.due\_date and getdate(invoice.due\_date) &lt; getdate()), otherwise 0.0 · min(max((payable\_amount − paid), 0.0), outstanding).

**Local steps**

- Set outstanding from flt(invoice.outstanding).
- If payable\_amount is identical to no value.
  - Return outstanding when (invoice.due\_date and getdate(invoice.due\_date) &lt; getdate()), otherwise 0.0.
    - Value choice on (invoice.due\_date and getdate(invoice.due\_date) &lt; getdate()) — true gives outstanding, false gives 0.0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoice.due\_date → getdate(invoice.due\_date) &lt; getdate().
- Set paid from (flt(invoice.base\_grand\_total) − outstanding).
- Return min(max((payable\_amount − paid), 0.0), outstanding).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0625.json#L5409) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1162)

<a id="op-1d137560154002"></a>
### Get customer outstanding

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_customer_outstanding`

**Inputs** customer, company, ignore\_outstanding\_sales\_order = false, cost\_center = no value.

**Record and data access** read “Cost Center” via get\_cached\_value.

**State and service calls** execute a supplied database query.

**Explicit results** ((outstanding\_based\_on\_gle + outstanding\_based\_on\_so) + outstanding\_based\_on\_dn).

**Local steps**

- Set cond from empty text.
- If cost\_center.
  - Set tuple(lft, rgt) from Platform.get\_cached\_value(“Cost Center”, cost\_center, list(“lft”, “rgt”)).
  - Set cond from formatted text  and cost\_center in (select name from ′tabCost Center′ where  lft &gt;= {lft} and rgt &lt;= {rgt}).
- Set outstanding\_based\_on\_gle from Platform.db.sql(formatted text   select sum(debit) - sum(credit)  from ′tabGL Entry′ where party\_type = 'Customer'  and is\_cancelled = 0 and party = %s  and company=%s {cond}, tuple(customer, company)).
- Set outstanding\_based\_on\_gle from flt(outstanding\_based\_on\_gle at 0 at 0) when outstanding\_based\_on\_gle, otherwise 0.
  - Value choice on outstanding\_based\_on\_gle — true gives flt(outstanding\_based\_on\_gle at 0 at 0), false gives 0.
- Set outstanding\_based\_on\_so from get\_sales\_order\_outstanding(customer, company, delivered\_only = ignore\_outstanding\_sales\_order).
- Set DeliveryNote from Platform.qb.DocType(“Delivery Note”).
- Set DeliveryNoteItem from Platform.qb.DocType(“Delivery Note Item”).
- Set SalesInvoice from Platform.qb.DocType(“Sales Invoice”).
- Set SalesInvoiceItem from Platform.qb.DocType(“Sales Invoice Item”).
- Set returned\_items from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(DeliveryNote.is\_return equals 1).as\_(“returned\_items”).
- Set billed\_dn\_detail from Coalesce(returned\_items.dn\_detail, SalesInvoiceItem.dn\_detail).
- Set si\_subquery from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.company equals company).where((SalesInvoice.is\_return equals 0 bitwise or SalesInvoice.update\_billed\_amou ….
- Set returned\_qty from IfNull(DeliveryNoteItem.returned\_qty, 0.0).
- Set dn\_query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.stock\_qty &gt; (nested operand in the contract + nested operand in the contract)).where(Criterion.any(list(n ….
- Set dn\_res from dn\_query.run().
- Set outstanding\_based\_on\_dn from flt(dn\_res at 0 at 0) when (dn\_res and dn\_res at 0 at 0 is distinct from no value), otherwise 0.0.
  - Value choice on (dn\_res and dn\_res at 0 at 0 is distinct from no value) — true gives flt(dn\_res at 0 at 0), false gives 0.0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dn\_res → dn\_res at 0 at 0 is distinct from no value.
- Return ((outstanding\_based\_on\_gle + outstanding\_based\_on\_so) + outstanding\_based\_on\_dn).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Cost Center”, cost\_center, list(“lft”, “rgt”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1155)

<a id="op-4bf3ec21020942"></a>
### Get sales order outstanding

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_get_sales_order_outstanding`

**Inputs** customer, company, delivered\_only = false.

**Explicit results** flt(res at 0 at 0) when (res and res at 0 at 0 is distinct from no value), otherwise 0.0.

**Local steps**

- Set SalesOrder from Platform.qb.DocType(“Sales Order”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(SalesOrder.per\_billed &lt; 100).where(SalesOrder.status differs from “Closed”).
- If delivered\_only.
  - Set SalesOrderItem from Platform.qb.DocType(“Sales Order Item”).
  - Set Greatest from CustomFunction(“GREATEST”, list(“a”, “b”)).
  - Set unbilled\_delivered\_share from Greatest(((SalesOrderItem.delivered\_qty ÷ SalesOrderItem.qty) − (SalesOrderItem.billed\_amt ÷ SalesOrderItem.amount)), 0).
  - Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.base\_net\_total &gt; 0).where(SalesOrderItem.amount &gt; 0).where(SalesOrderItem.delivered\_qty &gt; 0).
- Otherwise.
  - Set query from query.select(Sum(((SalesOrder.base\_grand\_total × (100 − SalesOrder.per\_billed)) ÷ 100))).
- Set res from query.run().
- Return flt(res at 0 at 0) when (res and res at 0 at 0 is distinct from no value), otherwise 0.0.
  - Value choice on (res and res at 0 at 0 is distinct from no value) — true gives flt(res at 0 at 0), false gives 0.0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in res → res at 0 at 0 is distinct from no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1437)

<a id="op-58ee27eeeb20bc"></a>
### Get credit limit

`operation_enterprise_selling_record_definitions_customer_business_behavior_get_credit_limit`

**Inputs** customer, company.

**Explicit results** get\_credit\_limit\_settings(customer, company) at 0.

**Local steps**

- Return get\_credit\_limit\_settings(customer, company) at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1154)

<a id="op-a552323627f12f"></a>
### Is sales order credit check bypassed

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_is_sales_order_credit_check_bypassed`

**Inputs** customer, company.

**Explicit results** get\_credit\_limit\_settings(customer, company) at 1.

**Local steps**

- Return get\_credit\_limit\_settings(customer, company) at 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1439)

<a id="op-79bc3771ef127e"></a>
### Get credit limit settings

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_get_credit_limit_settings`

**Inputs** customer, company.

**Record and data access** read “Customer Credit Limit” via get\_value · read “Customer” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** tuple(credit\_limit, bypass).

**Local steps**

- Set tuple(credit\_limit, bypass) from tuple(0.0, false).
- If customer.
  - Set customer\_limit from Platform.db.get\_value(“Customer Credit Limit”, mapping(“parent” → customer, “parenttype” → “Customer”, “company” → company), list(“credit\_limit”, “bypass\_credit\_limit\_check”), as\_dict = true).
  - If customer\_limit.
    - Set credit\_limit from flt(customer\_limit.credit\_limit).
    - Set bypass from bool(customer\_limit.bypass\_credit\_limit\_check).
  - If not credit\_limit.
    - Set customer\_group from Platform.get\_cached\_value(“Customer”, customer, “customer\_group”).
    - Set group\_limit from Platform.db.get\_value(“Customer Credit Limit”, mapping(“parent” → customer\_group, “parenttype” → “Customer Group”, “company” → company), list(“credit\_limit”, “bypass\_credit\_limit\_check”), as\_dict = true).
    - If group\_limit.
      - Set credit\_limit from flt(group\_limit.credit\_limit).
      - Set bypass from (bypass or bool(group\_limit.bypass\_credit\_limit\_check)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in bypass → bool(group\_limit.bypass\_credit\_limit\_check).
- If not credit\_limit.
  - Set credit\_limit from flt(Platform.get\_cached\_value(“Company”, company, “credit\_limit”)).
- Return tuple(credit\_limit, bypass).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer”, customer, “customer\_group”), Platform.get\_cached\_value(“Company”, company, “credit\_limit”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1436)

<a id="op-d4f3766ee9041d"></a>
### Make contact

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_make_contact`

**Inputs** args, is\_primary\_contact = 1.

**Record and data access** resolve a document from values via get\_doc.

**State and service calls** call insert on contact.

**Explicit results** contact.

**Local steps**

- Set values from mapping(“doctype” → “Contact”, “is\_primary\_contact” → is\_primary\_contact, “links” → list(mapping(“link\_doctype” → args.get(“doctype”), “link\_name” → args.get(“name”)))).
- Set party\_type from args.customer\_type when args.doctype equals “Customer”, otherwise args.supplier\_type.
  - Value choice on args.doctype equals “Customer” — true gives args.customer\_type, false gives args.supplier\_type.
- Set party\_name\_key from “customer\_name” when args.doctype equals “Customer”, otherwise “supplier\_name”.
  - Value choice on args.doctype equals “Customer” — true gives “customer\_name”, false gives “supplier\_name”.
- If party\_type equals “Individual”.
  - Set tuple(first, middle, last) from parse\_full\_name(args.get(party\_name\_key)).
  - Evaluate values.update(mapping(“first\_name” → first, “middle\_name” → middle, “last\_name” → last)).
- Otherwise.
  - Evaluate values.update(mapping(“company\_name” → args.get(party\_name\_key))).
- Set contact from Platform.get\_doc(values).
- If args.get(“email\_id”).
  - Evaluate contact.add\_email(args.get(“email\_id”), is\_primary = true).
- If args.get(“mobile\_no”).
  - Evaluate contact.add\_phone(args.get(“mobile\_no”), is\_primary\_mobile\_no = true).
- If args.get(“first\_name”).
  - Set contact.first\_name from args.get(“first\_name”).
- If args.get(“last\_name”).
  - Set contact.last\_name from args.get(“last\_name”).
- If flags bound to args.get(“flags”).
  - Evaluate contact.insert(ignore\_permissions = flags.get(“ignore\_permissions”)).
- Otherwise.
  - Evaluate contact.insert().
- Return contact.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1441)
