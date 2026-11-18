# Accounting and settlement · operations 74

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment request

[Record definition](../../../../data/record-types/payment_request.json)

<a id="op-30ebc881993af7"></a>
### Make payment request

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_make_payment_request`

**Inputs** remaining named values args.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from args.dt via get\_doc · read “Payment Request” via get\_value · resolve a document from “Payment Request” via get\_doc · read “Accounts Settings” via get\_single\_value.

**State and service calls** call save on pr · request new\_doc for “Payment Request” · call insert on pr · call submit on pr · commit.

**Explicit results** pr · pr.as\_dict().

**Explicit failure paths** validation helper — translated “Payment Requests cannot be created against: {0}”.format(Platform.bold(args.dt)) · validation helper — translated “Invalid parameter. 'dn' should be of type str” · validation helper — translated “Payment Schedule based Payment Requests cannot be created because a Payment Entry already exists for this document.” · validation helper — translated “The following payment schedule(s) already exist:\\n{0}”.format(whitespace '\\n'.join(duplicate\_schedules)) · validation helper — translated “Payment Entry is already created”.

**Local steps**

- Set args from Platform.\_dict(args).
- Set is\_portal\_payment from (args.order\_type equals “Shopping Cart” and “Customer” belongs to Platform.get\_roles() and not Platform.has\_permission(“Payment Request”, “create”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.order\_type equals “Shopping Cart” → “Customer” belongs to Platform.get\_roles() → not Platform.has\_permission(“Payment Request”, “create”).
- If is\_portal\_payment.
  - Set args from get\_portal\_payment\_args(args.dt, args.dn, args.submit\_doc).
- If args.dt does not belong to ALLOWED\_DOCTYPES\_FOR\_PAYMENT\_REQUEST.
  - Call the validation error handler Platform.throw(translated “Payment Requests cannot be created against: {0}”.format(Platform.bold(args.dt))).
- If (args.dn and not isinstance(args.dn, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.dn → not isinstance(args.dn, str).
  - Call the validation error handler Platform.throw(translated “Invalid parameter. 'dn' should be of type str”).
- If not is\_portal\_payment.
  - Evaluate Platform.has\_permission(“Payment Request”, “create”, throw = true).
  - Evaluate Platform.has\_permission(args.dt, “read”, args.dn, throw = true).
- Set ref\_doc from (args.ref\_doc or Platform.get\_doc(args.dt, args.dn)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.ref\_doc → Platform.get\_doc(args.dt, args.dn).
- If not args.get(“company”).
  - Set args.company from ref\_doc.company.
- Set gateway\_account from (get\_gateway\_details(args) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_gateway\_details(args) → Platform.\_dict().
- Set selected\_payment\_schedules from json.loads(args.get(“schedules”)) when args.get(“schedules”), otherwise list().
  - Value choice on args.get(“schedules”) — true gives json.loads(args.get(“schedules”)), false gives list().
- If (selected\_payment\_schedules and get\_existing\_payment\_entry(ref\_doc.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in selected\_payment\_schedules → get\_existing\_payment\_entry(ref\_doc.name).
  - Call the validation error handler Platform.throw(translated “Payment Schedule based Payment Requests cannot be created because a Payment Entry already exists for this document.”).
- Set has\_payment\_entry from bool(get\_existing\_payment\_entry(ref\_doc.name)).
- Set payment\_reference from list().
- If selected\_payment\_schedules.
  - Set existing\_payment\_references from get\_existing\_payment\_references(ref\_doc.name).
  - If existing\_payment\_references.
    - Set existing\_ids from set of r at “payment\_schedule” for r drawn from existing\_payment\_references.
      - Draw r from existing\_payment\_references.
    - Set selected\_ids from set of r at “name” for r drawn from selected\_payment\_schedules.
      - Draw r from selected\_payment\_schedules.
    - Set duplicate\_ids from (existing\_ids bitwise and selected\_ids).
    - If duplicate\_ids.
      - Set duplicate\_schedules from list().
      - For each row in selected\_payment\_schedules.
        - If row at “name” belongs to duplicate\_ids.
          - Set existing\_ref from next(generator of r for r drawn from existing\_payment\_references where r at “payment\_schedule” equals row at “name”, mapping()).
            - Draw r from existing\_payment\_references, keep a combination only if (r at “payment\_schedule” equals row at “name”).
          - Set existing\_pr from existing\_ref.get(“parent”).
          - Evaluate duplicate\_schedules.append(formatted text Payment Term: {row.get(“payment\_term”)}, Due Date: {row.get(“due\_date”)}, Amount: {row.get(“payment\_amount”)} (already requested in PR {existing\_pr})).
      - Call the validation error handler Platform.throw(translated “The following payment schedule(s) already exist:\\n{0}”.format(whitespace '\\n'.join(duplicate\_schedules))).
  - Set payment\_reference from set\_payment\_references(args.get(“schedules”)).
- If (selected\_payment\_schedules and not has\_payment\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in selected\_payment\_schedules → not has\_payment\_entry.
  - Set grand\_total from sum(generator of row.get(“payment\_amount”) for row drawn from selected\_payment\_schedules).
    - Draw row from selected\_payment\_schedules.
- Otherwise.
  - Set grand\_total from get\_amount(ref\_doc, gateway\_account.get(“payment\_account”)).
- If not grand\_total.
  - Call the validation error handler Platform.throw(translated “Payment Entry is already created”).
- If (args.loyalty\_points and ref\_doc.doctype equals “Sales Order”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.loyalty\_points → ref\_doc.doctype equals “Sales Order”.
  - Update grand\_total using − apply\_loyalty\_points(ref\_doc, cint(args.loyalty\_points)).
- Set existing\_payment\_request\_amount from get\_existing\_payment\_request\_amount(ref\_doc).
- Bind local operation validate\_and\_calculate\_grand\_total for subsequent calls.
- If existing\_payment\_request\_amount.
  - If args.order\_type equals “Shopping Cart”.
    - If get\_existing\_payment\_request\_amount(ref\_doc, list(“Initiated”, “Partially Paid”, “Payment Ordered”, “Paid”)).
      - Set grand\_total from validate\_and\_calculate\_grand\_total(grand\_total, existing\_payment\_request\_amount).
    - Otherwise.
      - Evaluate cancel\_old\_payment\_requests(ref\_doc.doctype, ref\_doc.name, ignore\_permissions = is\_portal\_payment).
  - Otherwise.
    - If not selected\_payment\_schedules.
      - Set grand\_total from validate\_and\_calculate\_grand\_total(grand\_total, existing\_payment\_request\_amount).
- Set draft\_payment\_request from (not is\_portal\_payment and Platform.db.get\_value(“Payment Request”, mapping(“reference\_doctype” → ref\_doc.doctype, “reference\_name” → ref\_doc.name, “docstatus” → 0))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_portal\_payment → Platform.db.get\_value(“Payment Request”, mapping(“reference\_doctype” → ref\_doc.doctype, “reference\_name” → ref\_doc.name, “docstatus” → 0)).
- If draft\_payment\_request.
  - Set pr from Platform.get\_doc(“Payment Request”, draft\_payment\_request).
  - If selected\_payment\_schedules.
    - Evaluate apply\_payment\_references(pr, payment\_reference).
    - Evaluate pr.save().
- Otherwise.
  - Set party\_type from (args.get(“party\_type”) or “Supplier” when ref\_doc.doctype belongs to list(“Purchase Order”, “Purchase Invoice”), otherwise “Customer”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“party\_type”) → “Supplier” when ref\_doc.doctype belongs to list(“Purchase Order”, “Purchase Invoice”), otherwise “Customer”.
    - Value choice on ref\_doc.doctype belongs to list(“Purchase Order”, “Purchase Invoice”) — true gives “Supplier”, false gives “Customer”.
  - Set party\_field from Platform.scrub(party\_type).
  - Set party from ref\_doc.get(party\_field).
  - Set bank\_account from get\_party\_bank\_account(party\_type, party) when args.get(“party\_type”), otherwise empty text.
    - Value choice on args.get(“party\_type”) — true gives get\_party\_bank\_account(party\_type, party), false gives empty text.
  - Set pr from Platform.new\_doc(“Payment Request”).
  - If not args.get(“payment\_request\_type”).
    - Set args at “payment\_request\_type” from “Outward” when args.get(“dt”) belongs to list(“Purchase Order”, “Purchase Invoice”), otherwise “Inward”.
      - Value choice on args.get(“dt”) belongs to list(“Purchase Order”, “Purchase Invoice”) — true gives “Outward”, false gives “Inward”.
  - Set party\_account\_currency from ref\_doc.get(“party\_account\_currency”).
  - If not party\_account\_currency.
    - Set find\_account from find\_party\_account when is\_portal\_payment, otherwise get\_party\_account.
      - Value choice on is\_portal\_payment — true gives find\_party\_account, false gives get\_party\_account.
    - Set party\_account from find\_account(party\_type, party, ref\_doc.company).
    - Set party\_account\_currency from get\_account\_currency(party\_account).
  - Set subscription\_plans from get\_subscription\_plans(ref\_doc.doctype, ref\_doc.name).
  - Evaluate pr.update(mapping(“payment\_gateway\_account” → gateway\_account.get(“name”), “payment\_gateway” → gateway\_account.get(“payment\_gateway”), “payment\_account” → gateway\_account.get(“payment\_account”), “payment\_c ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.recipient\_id → ref\_doc.owner.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in gateway\_account.get(“message”) → get\_dummy\_message(ref\_doc).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_doc.doctype equals “Sales Order” → (args.make\_sales\_invoice or (args.order\_type equals “Shopping Cart” and flt(ref\_doc.get(“per\_billed”)) &lt; 100)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.make\_sales\_invoice → (args.order\_type equals “Shopping Cart” and flt(ref\_doc.get(“per\_billed”)) &lt; 100).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.order\_type equals “Shopping Cart” → flt(ref\_doc.get(“per\_billed”)) &lt; 100.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.mute\_email → args.order\_type equals “Shopping Cart” → gateway\_account.get(“payment\_channel”, “Email”) differs from “Email”.
    - Value choice on args.get(“phone\_number”) — true gives args.get(“phone\_number”), false gives no value.
    - Value choice on subscription\_plans — true gives 1, false gives 0.
  - If selected\_payment\_schedules.
    - Evaluate apply\_payment\_references(pr, payment\_reference).
  - If subscription\_plans.
    - Evaluate pr.set(“subscription\_plans”, list of mapping(“plan” → row.plan, “qty” → row.qty) for row drawn from subscription\_plans).
      - Draw row from subscription\_plans.
  - Evaluate pr.update(mapping(“cost\_center” → ref\_doc.get(“cost\_center”), “project” → ref\_doc.get(“project”))).
  - For each dimension in get\_accounting\_dimensions().
    - Evaluate pr.update(mapping(dimension → ref\_doc.get(dimension))).
  - Set pr.flags.portal\_payment from is\_portal\_payment.
  - If Platform.db.get\_single\_value(“Accounts Settings”, “create\_pr\_in\_draft\_status”, cache = true).
    - Evaluate pr.insert(ignore\_permissions = true).
  - If args.submit\_doc.
    - If pr.get(“\_\_unsaved”).
      - Evaluate pr.insert(ignore\_permissions = true).
    - Set pr.flags.ignore\_permissions from is\_portal\_payment.
    - Evaluate pr.submit().
- If args.order\_type equals “Shopping Cart”.
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().
  - Set Platform.local.response at “type” from “redirect”.
  - Set Platform.local.response at “location” from pr.get\_payment\_url().
- If args.return\_doc.
  - Return pr.
- Return pr.as\_dict().

**Values supplied outside this operation** effective access from Platform.get\_roles(), Platform.has\_permission(“Payment Request”, “create”) and 2 further calls · configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “create\_pr\_in\_draft\_status”, cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L349)

<a id="op-a74ffcb0e7c9a9"></a>
### Make payment request.validate and calculate grand total

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_make_payment_request_validate_and_calculate_grand_total`

**Inputs** grand\_total, existing\_payment\_request\_amount.

**Explicit results** grand\_total.

**Explicit failure paths** validation helper — translated “Payment Request is already created”.

**Local steps**

- Update grand\_total using − existing\_payment\_request\_amount.
- If not grand\_total.
  - Call the validation error handler Platform.throw(translated “Payment Request is already created”).
- Return grand\_total.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0105.json#L4257) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L350)

<a id="op-957a6e7e20448e"></a>
### Get portal payment args

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_get_portal_payment_args`

**Inputs** doctype, docname, submit\_doc.

**Record and data access** read doctype via exists · resolve a document from doctype via get\_doc.

**Explicit results** Platform.\_dict(dt = doctype, dn = docname, order\_type = “Shopping Cart”, submit\_doc = submit\_doc, …).

**Local steps**

- If (doctype does not belong to PORTAL\_PAYABLE\_DOCTYPES or not isinstance(docname, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype does not belong to PORTAL\_PAYABLE\_DOCTYPES → not isinstance(docname, str).
  - Evaluate Platform.throw\_permission\_error().
- If not Platform.db.exists(doctype, docname).
  - Evaluate Platform.throw\_permission\_error().
- Set ref\_doc from Platform.get\_doc(doctype, docname).
- If (ref\_doc.docstatus differs from 1 or not has\_website\_permission(ref\_doc, “read”, Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.docstatus differs from 1 → not has\_website\_permission(ref\_doc, “read”, Platform.session.user).
  - Evaluate Platform.throw\_permission\_error().
- Return Platform.\_dict(dt = doctype, dn = docname, order\_type = “Shopping Cart”, submit\_doc = submit\_doc, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L857)

<a id="op-4dd85980456480"></a>
### Apply loyalty points

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_apply_loyalty_points`

**Inputs** sales\_order, loyalty\_points.

**Declared result** float.

**State and service calls** call db\_update on sales\_order.

**Explicit results** loyalty\_amount.

**Explicit failure paths** validation helper — translated “Loyalty Points can be redeemed in a Payment Request only for Shopping Cart orders” · validation helper — translated “Customer {0} is not enrolled in a Loyalty Program”.format(sales\_order.customer).

**Local steps**

- Bind dependencies validate\_loyalty\_points.
- If sales\_order.order\_type differs from “Shopping Cart”.
  - Call the validation error handler Platform.throw(translated “Loyalty Points can be redeemed in a Payment Request only for Shopping Cart orders”).
- Evaluate sales\_order.check\_permission(“write”).
- Set loyalty\_amount from validate\_loyalty\_points(sales\_order, loyalty\_points).
- If loyalty\_amount is identical to no value.
  - Call the validation error handler Platform.throw(translated “Customer {0} is not enrolled in a Loyalty Program”.format(sales\_order.customer)).
- Evaluate validate\_loyalty\_points\_used\_in\_other\_orders(sales\_order, loyalty\_points).
- Evaluate sales\_order.db\_update().
- Return loyalty\_amount.

**Values supplied outside this operation** effective access from sales\_order.check\_permission(“write”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L852)

<a id="op-fb798e2fefdf6c"></a>
### Validate loyalty points used in other orders

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_validate_loyalty_points_used_in_other_orders`

**Inputs** sales\_order, loyalty\_points.

**Record and data access** read “Customer” via get\_value.

**Explicit failure paths** validation helper — translated “Only {0} Loyalty Points of Customer {1} are free. The other points are used in open Shopping Cart orders.”.format(free\_points, sales\_order.customer).

**Local steps**

- Bind dependencies get\_loyalty\_details.
- Set loyalty\_program from Platform.db.get\_value(“Customer”, sales\_order.customer, “loyalty\_program”).
- Set available\_points from cint(get\_loyalty\_details(sales\_order.customer, loyalty\_program, company = sales\_order.company).get(“loyalty\_points”)).
- Set so from Platform.qb.DocType(“Sales Order”).
- Set points\_in\_other\_orders from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract differs from nes … at 0.
- Set free\_points from max((available\_points − cint(points\_in\_other\_orders)), 0).
- If loyalty\_points &gt; free\_points.
  - Call the validation error handler Platform.throw(translated “Only {0} Loyalty Points of Customer {1} are free. The other points are used in open Shopping Cart orders.”.format(free\_points, sales\_order.customer)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L867)

<a id="op-0946f397ff7141"></a>
### Apply payment references

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_apply_payment_references`

**Inputs** pr, payment\_reference.

**Local steps**

- Set existing\_refs from (pr.get(“payment\_reference”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pr.get(“payment\_reference”) → list().
- Set existing\_ids from set of r.get(“payment\_schedule”) for r drawn from existing\_refs where r.get(“payment\_schedule”).
  - Draw r from existing\_refs, keep a combination only if (r.get(“payment\_schedule”)).
- Set new\_refs from list of r for r drawn from (payment\_reference or list()) where r.get(“payment\_schedule”) does not belong to existing\_ids.
  - Draw r from (payment\_reference or list()), keep a combination only if (r.get(“payment\_schedule”) does not belong to existing\_ids).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in payment\_reference → list().
- Evaluate pr.set(“payment\_reference”, (existing\_refs + new\_refs)).
- Evaluate pr.set(“grand\_total”, sum(generator of flt(r.get(“amount”)) for r drawn from pr.get(“payment\_reference”))).
  - Draw r from pr.get(“payment\_reference”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0105.json#L4367) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L86) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L330)

<a id="op-ea3bc8e0de4da1"></a>
### Set payment references

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_set_payment_references`

**Inputs** payment\_schedules.

**Explicit results** payment\_reference.

**Local steps**

- Set payment\_schedules from json.loads(payment\_schedules) when payment\_schedules, otherwise list().
  - Value choice on payment\_schedules — true gives json.loads(payment\_schedules), false gives list().
- Set payment\_reference from list().
- For each row in payment\_schedules.
  - Evaluate payment\_reference.append(mapping(“payment\_term” → row.get(“payment\_term”), “payment\_schedule” → row.get(“name”), “description” → row.get(“description”), “due\_date” → row.get(“due\_date”), …)).
- Return payment\_reference.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L379)

<a id="op-9cade57a4c2dc9"></a>
### Get payment schedule rounding difference

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_get_payment_schedule_rounding_difference`

**Inputs** ref\_doc.

**Explicit results** 0 · flt(min((schedule\_total − ref\_doc.get\_payment\_schedule\_grand\_totals() at 0), rounding\_limit), precision).

**Local steps**

- If not ref\_doc.get(“payment\_schedule”).
  - Return 0.
- Set precision from ref\_doc.precision(“grand\_total”).
- Set schedule\_total from sum(generator of flt(row.payment\_amount, precision) for row drawn from ref\_doc.payment\_schedule).
  - Draw row from ref\_doc.payment\_schedule.
- Set rounding\_limit from ((len(ref\_doc.payment\_schedule) × 0.5) ÷ (10 to the power precision)).
- Return flt(min((schedule\_total − ref\_doc.get\_payment\_schedule\_grand\_totals() at 0), rounding\_limit), precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L856)

<a id="op-7d6c71cc63871c"></a>
### Get existing payment entry

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_existing_payment_entry`

**Inputs** ref\_docname.

**Explicit results** existing\_pe.

**Local steps**

- Set pe from Platform.qb.DocType(“Payment Entry”).
- Set per from Platform.qb.DocType(“Payment Entry Reference”).
- Set existing\_pe from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.reference\_name equals ref\_docname).limit(1).run().
- Return existing\_pe.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0105.json#L5104) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L335)

<a id="op-97e0aa7b7208b6"></a>
### Get amount

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_amount`

**Inputs** ref\_doc, payment\_account = no value.

**Explicit results** flt(grand\_total, get\_currency\_precision()) when grand\_total &gt; 0, otherwise 0.

**Local steps**

- Set grand\_total from 0.
- Set dt from ref\_doc.doctype.
- If dt belongs to list(“Sales Order”, “Purchase Order”).
  - Set advance\_amount from flt(ref\_doc.advance\_paid).
  - If ref\_doc.party\_account\_currency differs from ref\_doc.currency.
    - Set advance\_amount from flt((flt(ref\_doc.advance\_paid) ÷ ref\_doc.conversion\_rate)).
  - Set grand\_total from ((flt(ref\_doc.rounded\_total) or flt(ref\_doc.grand\_total)) − advance\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(ref\_doc.rounded\_total) → flt(ref\_doc.grand\_total).
- Otherwise.
  - If dt belongs to list(“Sales Invoice”, “Purchase Invoice”).
    - If (dt equals “Sales Invoice” and ref\_doc.is\_pos and ref\_doc.payments and any(list of (payment.type equals “Phone” and payment.account equals payment\_account) for payment drawn from ref\_doc.payments)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “Sales Invoice” → ref\_doc.is\_pos → ref\_doc.payments → any(list of (payment.type equals “Phone” and payment.account equals payment\_account) for payment drawn from ref\_doc.payments).
      - Draw payment from ref\_doc.payments.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in payment.type equals “Phone” → payment.account equals payment\_account.
      - Set grand\_total from sum(list of payment.amount for payment drawn from ref\_doc.payments where (payment.type equals “Phone” and payment.account equals payment\_account)).
        - Draw payment from ref\_doc.payments, keep a combination only if ((payment.type equals “Phone” and payment.account equals payment\_account)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in payment.type equals “Phone” → payment.account equals payment\_account.
    - Otherwise.
      - If ref\_doc.party\_account\_currency equals ref\_doc.currency.
        - Set grand\_total from flt(ref\_doc.outstanding\_amount).
      - Otherwise.
        - Set grand\_total from flt((flt(ref\_doc.outstanding\_amount) ÷ ref\_doc.conversion\_rate)).
  - Otherwise.
    - If dt equals “POS Invoice”.
      - For each pay in ref\_doc.payments.
        - If (pay.type equals “Phone” and pay.account equals payment\_account).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in pay.type equals “Phone” → pay.account equals payment\_account.
          - Set grand\_total from pay.amount.
          - Leave the innermost loop without its normal-exhaustion alternative.
    - Otherwise.
      - If dt equals “Fees”.
        - Set grand\_total from ref\_doc.outstanding\_amount.
- Return flt(grand\_total, get\_currency\_precision()) when grand\_total &gt; 0, otherwise 0.
  - Value choice on grand\_total &gt; 0 — true gives flt(grand\_total, get\_currency\_precision()), false gives 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0105.json#L5418) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L332)

<a id="op-7b88e8f7e1a80d"></a>
### Get irequest status

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_irequest_status`

**Inputs** payment\_requests = no value.

**Declared result** list.

**Explicit results** res.

**Local steps**

- Set IR from Platform.qb.DocType(“Integration Request”).
- Set res from list().
- If payment\_requests.
  - Set res from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(payment\_requests)).where(IR.status.isin(list(“Authorized”, “Completed”))).run(as\_dict = true).
- Return res.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0105.json#L6295) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L339)

<a id="op-b543f9a3206ee0"></a>
### Cancel old payment requests

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_cancel_old_payment_remote_requests`

**Inputs** ref\_dt, ref\_dn, ignore\_permissions = false.

**Record and data access** resolve a document from “Payment Request” via get\_doc.

**State and service calls** call cancel on doc · request set\_value on “Integration Request”.

**Explicit failure paths** validation helper — translated “Another Payment Request is already processed”.

**Local steps**

- Set PR from Platform.qb.DocType(“Payment Request”).
- If res bound to nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).where(nested operand in the contract.status.isin(list(“Draft”, “Requested”))).run(as\_dict = true).
  - If get\_irequest\_status(list of x.name for x drawn from res).
    - Draw x from res.
    - Call the validation error handler Platform.throw(translated “Another Payment Request is already processed”).
  - Otherwise.
    - For each x in res.
      - Set doc from Platform.get\_doc(“Payment Request”, x.name).
      - Set doc.flags.ignore\_permissions from ignore\_permissions.
      - Evaluate doc.cancel().
      - If ireqs bound to get\_irequests\_of\_payment\_request(doc.name).
        - For each ireq in ireqs.
          - Evaluate Platform.db.set\_value(“Integration Request”, ireq.name, “status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L87) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L331)

<a id="op-a95bf049819ae4"></a>
### Get existing payment request amount

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_existing_payment_request_amount`

**Inputs** ref\_doc, statuses = no value.

**Declared result** list.

**Explicit results** os\_amount\_in\_transaction\_currency.

**Local steps**

- Set PR from Platform.qb.DocType(“Payment Request”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.reference\_doctype equals nested operand in the contract.doctype).where(PR.reference\_name equals ref\_doc.n ….
- If statuses.
  - Set query from query.where(PR.status.isin(statuses)).
- Set response from query.run().
- Set os\_amount\_in\_transaction\_currency from flt(response at 0 at 0 when response at 0, otherwise 0).
  - Value choice on response at 0 — true gives response at 0 at 0, false gives 0.
- If ref\_doc.currency differs from ref\_doc.party\_account\_currency.
  - Set os\_amount\_in\_transaction\_currency from flt((os\_amount\_in\_transaction\_currency ÷ ref\_doc.conversion\_rate)).
- Return os\_amount\_in\_transaction\_currency.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L594) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L337)

<a id="op-b29ee8c02b0380"></a>
### Get gateway details

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_gateway_details`

**Inputs** args.

**Explicit results** get\_payment\_gateway\_account(gateway\_account).

**Local steps**

- Set gateway\_account from args.get(“payment\_gateway\_account”, mapping(“is\_default” → 1, “company” → args.company)).
- Return get\_payment\_gateway\_account(gateway\_account).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L1070) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L338)

<a id="op-809f3bfb056c2f"></a>
### Get payment gateway account

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_payment_gateway_account`

**Inputs** filter.

**Record and data access** read “Payment Gateway Account” via get\_value.

**Explicit results** Platform.db.get\_value(“Payment Gateway Account”, filter, list(“name”, “payment\_gateway”, “payment\_account”, “payment\_channel”, …), as\_dict = 1).

**Local steps**

- Return Platform.db.get\_value(“Payment Gateway Account”, filter, list(“name”, “payment\_gateway”, “payment\_account”, “payment\_channel”, …), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L1198) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L342)

<a id="op-9243a2c15bb8c2"></a>
### Get print format list

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_print_format_list`

**Inputs** ref\_doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Print Format” via get\_all.

**Explicit results** mapping(“print\_format” → print\_format\_list).

**Local steps**

- Set print\_format\_list from list(“Standard”).
- Evaluate print\_format\_list.extend(list of p.name for p drawn from Platform.get\_all(“Print Format”, filters = mapping(“doc\_type” → ref\_doctype))).
  - Draw p from Platform.get\_all(“Print Format”, filters = mapping(“doc\_type” → ref\_doctype)).
- Return mapping(“print\_format” → print\_format\_list).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L344)

<a id="op-f04cf8fca3fee2"></a>
### Make payment entry

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_make_payment_entry`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Payment Request” via get\_doc.

**Explicit results** doc.create\_payment\_entry(submit = false).as\_dict().

**Local steps**

- Set doc from Platform.get\_doc(“Payment Request”, docname).
- Evaluate doc.check\_permission(“read”).
- Return doc.create\_payment\_entry(submit = false).as\_dict().

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L346)

<a id="op-b1bd576474143a"></a>
### Get requested amount in party account currency

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_get_requested_amount_in_party_account_currency`

**Inputs** doc.

**Declared result** float.

**Record and data access** read doc.get(“reference\_doctype”) via get\_value.

**Explicit results** flt(((flt(doc.get(“grand\_total”)) ÷ grand\_total) × base\_grand\_total), precision) · flt(doc.get(“grand\_total”)).

**Local steps**

- Set company from doc.get(“company”).
- If (doc.get(“currency”) differs from doc.get(“party\_account\_currency”) and doc.get(“party\_account\_currency”) equals get\_company\_currency(company) and doc.get(“reference\_doctype”) and doc.get(“reference\_name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“currency”) differs from doc.get(“party\_account\_currency”) → doc.get(“party\_account\_currency”) equals get\_company\_currency(company) → doc.get(“reference\_doctype”) → doc.get(“reference\_name”).
  - Set invoice from Platform.get\_value(doc.get(“reference\_doctype”), doc.get(“reference\_name”), list(“rounded\_total”, “grand\_total”, “base\_rounded\_total”, “base\_grand\_total”), as\_dict = 1).
  - If invoice.
    - Set grand\_total from (invoice.get(“rounded\_total”) or invoice.get(“grand\_total”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in invoice.get(“rounded\_total”) → invoice.get(“grand\_total”).
    - Set base\_grand\_total from (invoice.get(“base\_rounded\_total”) or invoice.get(“base\_grand\_total”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in invoice.get(“base\_rounded\_total”) → invoice.get(“base\_grand\_total”).
    - If grand\_total.
      - Set precision from doc.precision(“outstanding\_amount”) when callable(getattr(doc, “precision”, no value)), otherwise Platform.get\_precision(“Payment Request”, “outstanding\_amount”, currency = doc.get(“party\_account\_currency”)).
        - Value choice on callable(getattr(doc, “precision”, no value)) — true gives doc.precision(“outstanding\_amount”), false gives Platform.get\_precision(“Payment Request”, “outstanding\_amount”, currency = doc.get(“party\_account\_currency”)).
      - Return flt(((flt(doc.get(“grand\_total”)) ÷ grand\_total) × base\_grand\_total), precision).
- Return flt(doc.get(“grand\_total”)).

**Values supplied outside this operation** selected callable from getattr(doc, “precision”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L858)

<a id="op-b5176aea3f0901"></a>
### Update payment requests as per pe references

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_update_payment_remote_requests_as_per_pe_references`

**Inputs** references = no value, cancel = false.

**State and service calls** request bulk\_update on “Payment Request”.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- If not references.
  - Return no value.
- Set precision from Platform.get\_precision(“Payment Entry Reference”, “allocated\_amount”).
- Set referenced\_payment\_requests from mapping of pr.name → pr for pr drawn from get\_payment\_requests\_with\_total\_requested(list(set of row.payment\_request for row drawn from references where row.payment\_request)).
  - Draw pr from get\_payment\_requests\_with\_total\_requested(list(set of row.payment\_request for row drawn from references where row.payment\_request)).
  - Draw row from references, keep a combination only if (row.payment\_request).
- Set doc\_updates from mapping().
- For each ref in references.
  - If not ref.payment\_request.
    - Continue with the next iteration or loop test.
  - Set payment\_request from referenced\_payment\_requests at ref.payment\_request.
  - Set pr\_outstanding from payment\_request at “outstanding\_amount”.
  - Set new\_outstanding\_amount from flt((pr\_outstanding + ref.allocated\_amount) when cancel, otherwise (pr\_outstanding − ref.allocated\_amount), precision).
    - Value choice on cancel — true gives (pr\_outstanding + ref.allocated\_amount), false gives (pr\_outstanding − ref.allocated\_amount).
  - Set payment\_request at “outstanding\_amount” from new\_outstanding\_amount.
  - If (not cancel and new\_outstanding\_amount &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cancel → new\_outstanding\_amount &lt; 0.
    - Call the validation error handler Platform.throw(msg = translated “The allocated amount is greater than the outstanding amount of Payment Request {0}”.format(ref.payment\_request), title = translated “Invalid Allocated Amount”).
  - Set doc\_updates at ref.payment\_request from mapping(“outstanding\_amount” → new\_outstanding\_amount, “status” → get\_payment\_request\_status(payment\_request, new\_outstanding\_amount, payment\_request.total\_requested, precision)).
- If doc\_updates.
  - Evaluate Platform.db.bulk\_update(“Payment Request”, doc\_updates).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L380)

<a id="op-53d81fcb54277c"></a>
### Get payment requests with total requested

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_get_payment_requests_with_total_requested`

**Inputs** names.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Payment Request” via get\_all.

**Explicit results** payment\_requests.

**Local steps**

- Set payment\_requests from Platform.get\_all(“Payment Request”, filters = mapping(“name” → list(“in”, names)), fields = list(“name”, “grand\_total”, “outstanding\_amount”, “payment\_request\_type”, …)).
- For each payment\_request in payment\_requests.
  - Set payment\_request.total\_requested from get\_requested\_amount\_in\_party\_account\_currency(payment\_request).
- Return payment\_requests.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L855)

<a id="op-b9e71851c9535e"></a>
### Get payment request status

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_get_payment_request_status`

**Inputs** payment\_request, outstanding\_amount, total\_requested, precision.

**Explicit results** “Initiated” when payment\_request.payment\_request\_type equals “Outward”, otherwise “Requested” · “Paid” when outstanding\_amount ≤ 0, otherwise “Partially Paid”.

**Local steps**

- If (total\_requested &gt; 0 and flt(outstanding\_amount, precision) ≥ flt(total\_requested, precision)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_requested &gt; 0 → flt(outstanding\_amount, precision) ≥ flt(total\_requested, precision).
  - Return “Initiated” when payment\_request.payment\_request\_type equals “Outward”, otherwise “Requested”.
    - Value choice on payment\_request.payment\_request\_type equals “Outward” — true gives “Initiated”, false gives “Requested”.
- Return “Paid” when outstanding\_amount ≤ 0, otherwise “Partially Paid”.
  - Value choice on outstanding\_amount ≤ 0 — true gives “Paid”, false gives “Partially Paid”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L854)

<a id="op-0d5c7c0cb77d86"></a>
### Get dummy message

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_dummy_message`

**Inputs** doc.

**Explicit results** multiline text in the contract.

**Local steps**

- Return multiline text in the contract.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0106.json#L2548) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L334)

<a id="op-ffe86f7ddb149b"></a>
### Get subscription details

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_subscription_details`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** get\_subscription\_plans(reference\_doctype, reference\_name).

**Local steps**

- Evaluate Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).
- Return get\_subscription\_plans(reference\_doctype, reference\_name).

**Values supplied outside this operation** effective access from Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L345)

<a id="op-0fc71661bba0c4"></a>
### Get subscription plans

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_get_subscription_plans`

**Inputs** reference\_doctype, reference\_name.

**Record and data access** read reference\_doctype via get\_value · read “Subscription Plan Detail” via get\_all.

**Explicit results** list() · Platform.get\_all(“Subscription Plan Detail”, filters = mapping(“parent” → subscription, “parenttype” → “Subscription”, “parentfield” → “plans”), fields = list(“plan”, “qty”)).

**Local steps**

- If not Platform.get\_meta(reference\_doctype).has\_field(“subscription”).
  - Return list().
- Set subscription from Platform.db.get\_value(reference\_doctype, reference\_name, “subscription”).
- If not subscription.
  - Return list().
- Return Platform.get\_all(“Subscription Plan Detail”, filters = mapping(“parent” → subscription, “parenttype” → “Subscription”, “parentfield” → “plans”), fields = list(“plan”, “qty”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L859)
