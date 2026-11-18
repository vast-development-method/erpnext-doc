# Accounting and settlement · operations 73

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment request

[Record definition](../../../../data/record-types/payment_request.json)

<a id="op-cfc8c63af83f1e"></a>
### Payment Request.validate currency

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_validate_currency`

**Inputs** self.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc · read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Transaction currency must be same as Payment Gateway currency”.

**Local steps**

- Set ref\_doc from Platform.get\_doc(self.reference\_doctype, self.reference\_name).
- If (self.payment\_account and ref\_doc.currency differs from Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_currency”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_account → ref\_doc.currency differs from Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_currency”).
  - Call the validation error handler Platform.throw(translated “Transaction currency must be same as Payment Gateway currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L6615) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L375)

<a id="op-3272cdcabf5863"></a>
### Payment Request.validate subscription details

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_validate_subscription_details`

**Inputs** self.

**Record and data access** read “Subscription Plan” via get\_value.

**State and service calls** msgprint with translated “The amount of {0} set in this payment request is different from the calculated amount of all payment plans:  …”.format(self.grand\_total, amount).

**Explicit failure paths** validation helper — translated “The payment gateway account in plan {0} is different from the payment gateway account in this payment request”.format(subscription\_plan.name).

**Local steps**

- If self.is\_a\_subscription.
  - Set amount from 0.
  - For each subscription\_plan in self.subscription\_plans.
    - Set payment\_gateway from Platform.db.get\_value(“Subscription Plan”, subscription\_plan.plan, “payment\_gateway”).
    - If payment\_gateway differs from self.payment\_gateway\_account.
      - Call the validation error handler Platform.throw(translated “The payment gateway account in plan {0} is different from the payment gateway account in this payment request”.format(subscription\_plan.name)).
    - Set rate from get\_plan\_rate(subscription\_plan.plan, quantity = subscription\_plan.qty).
    - Update amount using + rate.
  - If amount differs from self.grand\_total.
    - Evaluate Platform.msgprint(translated “The amount of {0} set in this payment request is different from the calculated amount of all payment plans:  …”.format(self.grand\_total, amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L6805) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L378)

<a id="op-e8ae1905721c5c"></a>
### Payment Request.before submit

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_before_submit`

**Inputs** self.

**Local steps**

- Set self.outstanding\_amount from get\_requested\_amount\_in\_party\_account\_currency(self).
- If self.payment\_request\_type equals “Outward”.
  - Set self.status from “Initiated”.
- Otherwise.
  - <a id="op-e8ae1905721c5c-guard-6"></a>If self.payment\_request\_type equals “Inward”.
    - Set self.status from “Requested”.
- If self.payment\_request\_type equals “Inward”.
  - If self.payment\_channel equals “Phone”.
    - Evaluate self.request\_phone\_payment().
  - Otherwise.
    - Evaluate self.set\_payment\_request\_url().
    - If not (self.mute\_email or self.flags.mute\_email).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mute\_email → self.flags.mute\_email.
      - Evaluate self.send\_email().
      - Evaluate self.make\_communication\_entry().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.payment\_request\_type equals “Inward”, self.payment\_request\_type = “Inward” selects the branch that assigns “Requested” to self.status. With self.payment\_request\_type = “Outward”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e8ae1905721c5c-guard-6)

**Methods declared on this owner** [request phone payment](operations-073.md#op-0c7d5668a6e196), [set payment request url](operations-073.md#op-e466f4ecef470e), [send email](operations-073.md#op-d61d62adae96ac), [make communication entry](operations-073.md#op-c59324e133ba04).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L352)

<a id="op-49b2669ea46193"></a>
### Payment Request.on submit

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_reference\_advance\_payment\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reference advance payment status](operations-073.md#op-81aa4b6f8c0ffa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L363)

<a id="op-0c7d5668a6e196"></a>
### Payment Request.request phone payment

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_request_phone_payment`

**Inputs** self.

**Local steps**

- Set controller from \_get\_payment\_gateway\_controller(self.payment\_gateway).
- Set request\_amount from self.get\_request\_amount().
- Set payment\_record from dict(reference\_doctype = “Payment Request”, reference\_docname = self.name, payment\_reference = self.reference\_name, request\_amount = request\_amount, …).
- Evaluate controller.validate\_transaction\_currency(self.currency).
- Evaluate controller.request\_for\_payment(expanded names payment\_record).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get request amount](operations-073.md#op-26841f7907c1d4).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L1986) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L365)

<a id="op-26841f7907c1d4"></a>
### Payment Request.get request amount

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_get_request_amount`

**Inputs** self.

**Record and data access** read “Integration Request” via get\_all.

**Explicit results** self.grand\_total · request\_amounts.

**Local steps**

- Set data\_of\_completed\_requests from Platform.get\_all(“Integration Request”, filters = mapping(“reference\_doctype” → self.doctype, “reference\_docname” → self.name, “status” → “Completed”), pluck = “data”).
- If not data\_of\_completed\_requests.
  - Return self.grand\_total.
- Set request\_amounts from sum(generator of json.loads(d).get(“request\_amount”) for d drawn from data\_of\_completed\_requests).
  - Draw d from data\_of\_completed\_requests.
- Return request\_amounts.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L2253) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L358)

<a id="op-2c4247bf87e73b"></a>
### Payment Request.on cancel

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.check\_if\_payment\_entry\_exists().
- Evaluate self.set\_as\_cancelled().
- Evaluate self.update\_reference\_advance\_payment\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if payment entry exists](operations-073.md#op-4159a56a599359), [set as cancelled](operations-073.md#op-12eb834ef97926), [update reference advance payment status](operations-073.md#op-81aa4b6f8c0ffa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L2511) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L361)

<a id="op-7dd4473574a9a7"></a>
### Payment Request.make invoice

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_make_invoice`

**Inputs** self.

**State and service calls** call insert on si · call submit on si.

**Local steps**

- Bind dependencies make\_sales\_invoice.
- Set si from make\_sales\_invoice(self.reference\_name, ignore\_permissions = true).
- Set si.allocate\_advances\_automatically from true.
- Set si from si.insert(ignore\_permissions = true).
- Evaluate si.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L360)

<a id="op-0a86f1d8b21124"></a>
### Payment Request.payment gateway validation

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_payment_gateway_validation`

**Inputs** self.

**Explicit results** controller.on\_payment\_request\_submission(self) · true · false.

**Local steps**

- Attempt the following.
  - Set controller from \_get\_payment\_gateway\_controller(self.payment\_gateway).
  - If hasattr(controller, “on\_payment\_request\_submission”).
    - Return controller.on\_payment\_request\_submission(self).
  - Otherwise.
    - Return true.
- On failure (Exception).
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L364)

<a id="op-e466f4ecef470e"></a>
### Payment Request.set payment request url

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_set_payment_request_resource_address`

**Inputs** self.

**Local steps**

- If (self.payment\_account and self.payment\_gateway and self.payment\_gateway\_validation()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_account → self.payment\_gateway → self.payment\_gateway\_validation().
  - Set self.payment\_url from self.get\_payment\_url().

If control reaches the end, it returns no value.

**Methods declared on this owner** [payment gateway validation](operations-073.md#op-0a86f1d8b21124), [get payment url](operations-073.md#op-d6f09d6b39791b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L2974) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L371)

<a id="op-d6f09d6b39791b"></a>
### Payment Request.get payment url

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_get_payment_resource_address`

**Inputs** self.

**Record and data access** read self.reference\_doctype via get\_value.

**Explicit results** controller.get\_payment\_url(expanded names mapping(“amount” → flt(self.grand\_total, self.precision(“grand\_total”)), “title” → data.company, “description” → self.subject, “reference\_doctype” → “Payment Request”, …)).

**Local steps**

- If self.reference\_doctype differs from “Fees”.
  - Set data from Platform.db.get\_value(self.reference\_doctype, self.reference\_name, list(“company”, “customer\_name”), as\_dict = 1).
- Otherwise.
  - Set data from Platform.db.get\_value(self.reference\_doctype, self.reference\_name, list(“student\_name”), as\_dict = 1).
  - Evaluate data.update(mapping(“company” → Platform.defaults.get\_defaults().company)).
- Set controller from \_get\_payment\_gateway\_controller(self.payment\_gateway).
- Evaluate controller.validate\_transaction\_currency(self.currency).
- If hasattr(controller, “validate\_minimum\_transaction\_amount”).
  - Evaluate controller.validate\_minimum\_transaction\_amount(self.currency, self.grand\_total).
- Return controller.get\_payment\_url(expanded names mapping(“amount” → flt(self.grand\_total, self.precision(“grand\_total”)), “title” → data.company, “description” → self.subject, “reference\_doctype” → “Payment Request”, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.email\_to → Platform.session.user.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L3080) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L357)

<a id="op-cd7cd7ac3f0bc5"></a>
### Payment Request.on payment authorized

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_paymentrequest_on_payment_authorized`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, status.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L860)

<a id="op-e3d91062bc2e14"></a>
### Payment Request.set as paid

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_set_as_paid`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** payment\_entry.

**Local steps**

- If self.payment\_channel equals “Phone”.
  - Evaluate self.db\_set(mapping(“status” → “Paid”, “outstanding\_amount” → 0)).
- Otherwise.
  - Within run\_as\_administrator().
    - Set payment\_entry from self.create\_payment\_entry().
    - If self.make\_sales\_invoice.
      - Evaluate self.make\_invoice().
  - Return payment\_entry.

If control reaches the end, it returns no value.

**Methods declared on this owner** [create payment entry](operations-073.md#op-cdd6ac26d90fd8), [make invoice](operations-073.md#op-7dd4473574a9a7).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L369)

<a id="op-cdd6ac26d90fd8"></a>
### Payment Request.create payment entry

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_create_payment_entry`

**Inputs** self, submit = true.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**State and service calls** call insert on payment\_entry · call submit on payment\_entry.

**Explicit results** payment\_entry.

**Local steps**

- Set Platform.flags.ignore\_account\_permission from true.
- Set ref\_doc from Platform.get\_doc(self.reference\_doctype, self.reference\_name).
- If self.reference\_doctype belongs to list(“Sales Invoice”, “POS Invoice”).
  - Set party\_account from ref\_doc.debit\_to.
- Otherwise.
  - If self.reference\_doctype equals “Purchase Invoice”.
    - Set party\_account from ref\_doc.credit\_to.
  - Otherwise.
    - Set party\_account from get\_party\_account(“Customer”, ref\_doc.get(“customer”), ref\_doc.company).
- Set party\_account\_currency from (self.get(“party\_account\_currency”) or ref\_doc.get(“party\_account\_currency”) or get\_account\_currency(party\_account)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“party\_account\_currency”) → ref\_doc.get(“party\_account\_currency”) → get\_account\_currency(party\_account).
- Set bank\_amount from no value.
- If (party\_account\_currency equals ref\_doc.company\_currency and party\_account\_currency differs from self.currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account\_currency equals ref\_doc.company\_currency → party\_account\_currency differs from self.currency.
  - Set exchange\_rate from ref\_doc.get(“conversion\_rate”).
  - Set bank\_amount from flt((self.outstanding\_amount ÷ exchange\_rate), self.precision(“grand\_total”)).
- Set payment\_entry from get\_payment\_entry(self.reference\_doctype, self.reference\_name, party\_amount = self.outstanding\_amount, bank\_account = self.payment\_account, bank\_amount = bank\_amount, created\_from\_payment\_request = true).
- Evaluate payment\_entry.set\_missing\_ref\_details(force = true).
- Evaluate payment\_entry.update(mapping(“mode\_of\_payment” → self.mode\_of\_payment, “reference\_no” → self.name, “reference\_date” → nowdate(), “remarks” → “Payment Entry against {} {} via Payment Request {}”.format(self ….
- Evaluate self.\_allocate\_payment\_request\_to\_pe\_references(references = payment\_entry.references).
- Evaluate payment\_entry.update(mapping(“cost\_center” → self.get(“cost\_center”), “project” → self.get(“project”))).
- If self.currency differs from ref\_doc.company\_currency.
  - If (self.payment\_request\_type equals “Outward” and payment\_entry.paid\_from\_account\_currency equals ref\_doc.company\_currency and payment\_entry.paid\_from\_account\_currency differs from payment\_entry.paid\_to\_acco ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_request\_type equals “Outward” → payment\_entry.paid\_from\_account\_currency equals ref\_doc.company\_currency → payment\_entry.paid\_from\_account\_currency differs from payment\_entry.paid\_to\_account\_currency.
    - Set payment\_entry.paid\_amount, payment\_entry.base\_paid\_amount from (payment\_entry.target\_exchange\_rate × payment\_entry.received\_amount).
- For each dimension in get\_accounting\_dimensions().
  - Evaluate payment\_entry.update(mapping(dimension → self.get(dimension))).
- If submit.
  - Evaluate payment\_entry.insert(ignore\_permissions = true).
  - Evaluate payment\_entry.submit().
- Return payment\_entry.

**Methods declared on this owner** [allocate payment request to pe references](operations-073.md#op-940ecfdd2caa8d).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L354)

<a id="op-4a98c103c30781"></a>
### Payment Request.resend payment email

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_resend_payment_email`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper — translated “Payment Link couldn't be sent.”.

**Local steps**

- Evaluate self.reload().
- Evaluate self.check\_permission(“email”).
- Evaluate Platform.has\_permission(self.reference\_doctype, “read”, self.reference\_name, throw = true).
- If not (self.docstatus equals 1 and self.payment\_request\_type equals “Inward” and self.payment\_channel differs from “Phone” and self.status does not belong to list(“Initiated”, “Paid”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.payment\_request\_type equals “Inward” → self.payment\_channel differs from “Phone” → self.status does not belong to list(“Initiated”, “Paid”).
  - Call the validation error handler Platform.throw(translated “Payment Link couldn't be sent.”).
- Evaluate self.send\_email().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send email](operations-073.md#op-d61d62adae96ac).

**Values supplied outside this operation** effective access from self.check\_permission(“email”), Platform.has\_permission(self.reference\_doctype, “read”, self.reference\_name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L366)

<a id="op-d61d62adae96ac"></a>
### Payment Request.send email

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_send_email`

**Inputs** self.

**Local steps**

- Set email\_args from mapping(“recipients” → self.email\_to, “sender” → no value, “subject” → self.subject, “message” → self.get\_message(), …).
- Set job\_id from formatted text send\_payment\_email::{self.name}.
- Evaluate enqueue(method = Platform.sendmail, queue = “short”, timeout = 300, is\_async = true, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get message](operations-073.md#op-16b8b78fb2912d).

**Values supplied outside this operation** service or queued work from enqueue(method = Platform.sendmail, queue = “short”, timeout = 300, is\_async = true, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L5372) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L367)

<a id="op-16b8b78fb2912d"></a>
### Payment Request.get message

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_get_message`

**Inputs** self.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**Explicit results** Platform.render\_template(self.message, context, restrict\_globals = true).

**Local steps**

- Set context from mapping(“doc” → Platform.get\_doc(self.reference\_doctype, self.reference\_name), “payment\_url” → self.payment\_url, “payment\_request” → self).
- If self.message.
  - Return Platform.render\_template(self.message, context, restrict\_globals = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L5723) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L356)

<a id="op-f89c127d954dcd"></a>
### Payment Request.set failed

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_set_failed`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L5902) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L370)

<a id="op-12eb834ef97926"></a>
### Payment Request.set as cancelled

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_set_as_cancelled`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L5935) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L368)

<a id="op-4159a56a599359"></a>
### Payment Request.check if payment entry exists

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_check_if_payment_entry_exists`

**Inputs** self.

**Record and data access** read “Payment Entry Reference” via get\_all.

**Explicit failure paths** validation helper — translated “Payment Entry already exists”.

**Local steps**

- If self.status equals “Paid”.
  - If Platform.get\_all(“Payment Entry Reference”, filters = mapping(“reference\_name” → self.reference\_name, “docstatus” → list(“&lt;”, 2)), fields = list(“parent”), limit = 1).
    - Call the validation error handler Platform.throw(translated “Payment Entry already exists”, title = translated “Error”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L353)

<a id="op-c59324e133ba04"></a>
### Payment Request.make communication entry

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_make_communication_entry`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Communication”, “subject” → self.subject, “content” → self.get\_message(), “sent\_or\_received” → “Sent”, …) via get\_doc.

**State and service calls** call insert on comm.

**Local steps**

- Set comm from Platform.get\_doc(mapping(“doctype” → “Communication”, “subject” → self.subject, “content” → self.get\_message(), “sent\_or\_received” → “Sent”, …)).
- Evaluate comm.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get message](operations-073.md#op-16b8b78fb2912d).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L6204) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L359)

<a id="op-28901410f2b32a"></a>
### Payment Request.create subscription

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_create_subscription`

**Inputs** self, payment\_provider, gateway\_controller, data.

**Explicit results** create\_stripe\_subscription(gateway\_controller, data).

**Local steps**

- If payment\_provider equals “stripe”.
  - Within payment\_app\_import\_guard().
    - Bind dependencies create\_stripe\_subscription.
  - Return create\_stripe\_subscription(gateway\_controller, data).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L6420) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L355)

<a id="op-81aa4b6f8c0ffa"></a>
### Payment Request.update reference advance payment status

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_update_reference_advance_payment_status`

**Inputs** self.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**Local steps**

- If self.reference\_doctype belongs to get\_advance\_payment\_doctypes().
  - Set ref\_doc from Platform.get\_doc(self.reference\_doctype, self.reference\_name).
  - Evaluate ref\_doc.set\_advance\_payment\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L6554) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L372)

<a id="op-940ecfdd2caa8d"></a>
### Payment Request.allocate payment request to pe references

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_allocate_payment_request_to_pe_references`

**Inputs** self, references.

**State and service calls** request copy\_doc for row · call insert on references.

**Explicit results** no value.

**Local steps**

- If len(references) equals 1.
  - Set references at 0.payment\_request from self.name.
  - Return no value.
- Set precision from references at 0.precision(“allocated\_amount”).
- Set outstanding\_amount from self.outstanding\_amount.
- Set row\_number from 1.
- Set MOVE\_TO\_NEXT\_ROW from 1.
- Set TO\_SKIP\_NEW\_ROW from 2.
- Set NEW\_ROW\_ADDED from false.
- While row\_number ≤ len(references).
  - Set row from references at (row\_number − 1).
  - Set row.idx from row\_number.
  - If outstanding\_amount equals 0.
    - If not NEW\_ROW\_ADDED.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Update row\_number using + MOVE\_TO\_NEXT\_ROW.
    - Continue with the next iteration or loop test.
  - Set row.payment\_request from self.name.
  - If row.allocated\_amount ≤ outstanding\_amount.
    - Set outstanding\_amount from flt((outstanding\_amount − row.allocated\_amount), precision).
    - Update row\_number using + MOVE\_TO\_NEXT\_ROW.
  - Otherwise.
    - Set remaining\_allocated\_amount from flt((row.allocated\_amount − outstanding\_amount), precision).
    - Set row.allocated\_amount from outstanding\_amount.
    - Set outstanding\_amount from 0.
    - Set new\_row from Platform.copy\_doc(row).
    - Evaluate references.insert(row\_number, new\_row).
    - Set new\_row.idx from (row\_number + 1).
    - Set new\_row.payment\_request from no value.
    - Set new\_row.allocated\_amount from remaining\_allocated\_amount.
    - Set NEW\_ROW\_ADDED from true.
    - Update row\_number using + TO\_SKIP\_NEW\_ROW.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0104.json#L6680) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L351)
