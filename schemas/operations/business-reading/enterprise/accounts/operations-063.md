# Accounting and settlement · operations 63

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Party

<a id="op-b18c7c4017ae47"></a>
### Validate party currency before merging

`operation_enterprise_accounts_party_business_behavior_validate_party_currency_before_merging`

**Inputs** party\_type, old\_party, new\_party.

**Record and data access** read “Company” via get\_all.

**Explicit failure paths** validation helper — translated “Cannot merge {0} '{1}' into '{2}' as both have existing accounting entries in different currencies for compa …”.format(party\_type, old\_party, new\_party, company.name).

**Local steps**

- For each company in Platform.get\_all(“Company”).
  - Set old\_party\_currency from get\_party\_gle\_currency(party\_type, old\_party, company.name).
  - Set new\_party\_currency from get\_party\_gle\_currency(party\_type, new\_party, company.name).
  - If (old\_party\_currency and new\_party\_currency and old\_party\_currency differs from new\_party\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_party\_currency → new\_party\_currency → old\_party\_currency differs from new\_party\_currency.
    - Call the validation error handler Platform.throw(translated “Cannot merge {0} '{1}' into '{2}' as both have existing accounting entries in different currencies for compa …”.format(party\_type, old\_party, new\_party, company.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L4424) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L85)

## Record · Party link

[Record definition](../../../../data/record-types/party_link.json)

<a id="op-63257dde49887f"></a>
### Party Link.validate

`operation_enterprise_accounts_record_definitions_party_link_business_behavior_party_link_validate`

**Inputs** self.

**Record and data access** read “Party Link” via get\_all.

**Explicit failure paths** validation helper — translated “Allowed primary roles are 'Customer' and 'Supplier'. Please select one of these roles only.” · validation helper — translated “{} {} is already linked with {} {}”.format(self.primary\_role, bold(self.primary\_party), self.secondary\_role, bold(self.secondary\_party)) · validation helper — translated “{} {} is already linked with another {}”.format(self.secondary\_role, self.secondary\_party, existing\_party\_link at 0) · validation helper — translated “{} {} is already linked with another {}”.format(self.primary\_role, self.primary\_party, existing\_party\_link at 0).

**Local steps**

- If self.primary\_role does not belong to list(“Customer”, “Supplier”).
  - Call the validation error handler Platform.throw(translated “Allowed primary roles are 'Customer' and 'Supplier'. Please select one of these roles only.”, title = translated “Invalid Primary Role”).
- Set existing\_party\_link from Platform.get\_all(“Party Link”, mapping(“primary\_party” → self.primary\_party, “secondary\_party” → self.secondary\_party), pluck = “primary\_role”).
- If existing\_party\_link.
  - Call the validation error handler Platform.throw(translated “{} {} is already linked with {} {}”.format(self.primary\_role, bold(self.primary\_party), self.secondary\_role, bold(self.secondary\_party))).
- Set existing\_party\_link from Platform.get\_all(“Party Link”, mapping(“primary\_party” → self.secondary\_party), pluck = “primary\_role”).
- If existing\_party\_link.
  - Call the validation error handler Platform.throw(translated “{} {} is already linked with another {}”.format(self.secondary\_role, self.secondary\_party, existing\_party\_link at 0)).
- Set existing\_party\_link from Platform.get\_all(“Party Link”, mapping(“secondary\_party” → self.primary\_party), pluck = “primary\_role”).
- If existing\_party\_link.
  - Call the validation error handler Platform.throw(translated “{} {} is already linked with another {}”.format(self.primary\_role, self.primary\_party, existing\_party\_link at 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L16)

<a id="op-330e6787696e20"></a>
### Create party link

`operation_enterprise_accounts_record_definitions_party_link_business_behavior_create_party_link`

**Inputs** primary\_role, primary\_party, secondary\_party.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Party Link” · call save on party\_link.

**Explicit results** party\_link.

**Local steps**

- Set party\_link from Platform.new\_doc(“Party Link”).
- Set party\_link.primary\_role from primary\_role.
- Set party\_link.primary\_party from primary\_party.
- Set party\_link.secondary\_role from “Customer” when primary\_role equals “Supplier”, otherwise “Supplier”.
  - Value choice on primary\_role equals “Supplier” — true gives “Customer”, false gives “Supplier”.
- Set party\_link.secondary\_party from secondary\_party.
- Evaluate party\_link.save().
- Return party\_link.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L15)

## Record · Payment entry

[Record definition](../../../../data/record-types/payment_entry.json)

<a id="op-fefcaa66d96d98"></a>
### Payment Entry.initialize

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- If not self.is\_new().
  - Evaluate self.setup\_party\_account\_field().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup party account field](operations-063.md#op-fd22c476001a12).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0074.json#L5100) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L66)

<a id="op-fd22c476001a12"></a>
### Payment Entry.setup party account field

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_setup_party_account_field`

**Inputs** self.

**Local steps**

- Set self.party\_account\_field from no value.
- Set self.party\_account from no value.
- Set self.party\_account\_currency from no value.
- If self.payment\_type equals “Receive”.
  - Set self.party\_account\_field from “paid\_from”.
  - Set self.party\_account from self.paid\_from.
  - Set self.party\_account\_currency from self.paid\_from\_account\_currency.
- Otherwise.
  - <a id="op-fd22c476001a12-guard-11"></a>If self.payment\_type equals “Pay”.
    - Set self.party\_account\_field from “paid\_to”.
    - Set self.party\_account from self.paid\_to.
    - Set self.party\_account\_currency from self.paid\_to\_account\_currency.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.payment\_type equals “Pay”, self.payment\_type = “Pay” selects the branch that assigns “paid\_to” to self.party\_account\_field. With self.payment\_type = “Receive”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-fd22c476001a12-guard-11)

[Applicable decision contract](../../../enterprise-decision-contracts/part-0074.json#L5229) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L97)

<a id="op-c3af14da662459"></a>
### Payment Entry.validate

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_enabled\_mode\_of\_payment(self.mode\_of\_payment).
- Evaluate self.setup\_party\_account\_field().
- Evaluate self.set\_missing\_values().
- Evaluate self.set\_liability\_account().
- Evaluate self.set\_missing\_ref\_details(force = true).
- Evaluate self.validate\_payment\_type().
- Evaluate self.validate\_internal\_transfer\_accounts().
- Evaluate self.validate\_party\_details().
- Evaluate self.set\_exchange\_rate().
- Evaluate self.validate\_mandatory().
- Evaluate self.validate\_reference\_documents().
- Evaluate self.validate\_dunning\_deductions().
- Evaluate self.set\_amounts().
- Evaluate self.validate\_amounts().
- Evaluate self.apply\_taxes().
- Evaluate self.set\_amounts\_after\_tax().
- Evaluate self.clear\_unallocated\_reference\_document\_rows().
- Evaluate self.validate\_transaction\_reference().
- Evaluate self.set\_title().
- Evaluate self.set\_remarks().
- Evaluate self.validate\_duplicate\_entry().
- Evaluate self.validate\_payment\_type\_with\_outstanding().
- Evaluate self.validate\_allocated\_amount().
- Evaluate self.validate\_paid\_invoices().
- Evaluate self.ensure\_supplier\_is\_not\_blocked().
- Evaluate PaymentTaxWithholding(self).on\_validate().
- Evaluate self.set\_status().
- Evaluate self.set\_total\_in\_words().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup party account field](operations-063.md#op-fd22c476001a12), [set missing values](operations-064.md#op-47a3a71aa3cc61), [set liability account](operations-063.md#op-9c547a17706b4a), [set missing ref details](operations-064.md#op-b2c3ee93cef56a), [validate payment type](operations-064.md#op-7eab4851d4fc71), [validate internal transfer accounts](operations-064.md#op-ff9438efeffb69), [validate party details](operations-064.md#op-e9468b8cacbd25), [set exchange rate](operations-064.md#op-da36d8f3f32005), [validate mandatory](operations-064.md#op-8f0328e2d0df04), [validate reference documents](operations-064.md#op-ea832d4a8b140e), [validate dunning deductions](operations-063.md#op-7f539db353203a), [set amounts](operations-064.md#op-5375912c31b22f), [validate amounts](operations-064.md#op-44c320825e98ec), [apply taxes](operations-064.md#op-19f1aed3b88d25), [set amounts after tax](operations-065.md#op-01994b4527f906), [clear unallocated reference document rows](operations-065.md#op-0ed028c1ef1e5a), [validate transaction reference](operations-065.md#op-6433bf54aa848b), [set title](operations-065.md#op-bf56c19143e854), [set remarks](operations-065.md#op-52d904fb7430cd), [validate duplicate entry](operations-063.md#op-fc500b4c7e02cf), [validate payment type with outstanding](operations-063.md#op-56339c38e21f2a), [validate allocated amount](operations-063.md#op-c366b1c9048281), [validate paid invoices](operations-064.md#op-f1a8d99621f9e7), [set status](operations-064.md#op-cec3f4bf4f6aa7), [set total in words](operations-064.md#op-8b25753da4b991).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L104)

<a id="op-7f539db353203a"></a>
### Payment Entry.validate dunning deductions

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_validate_dunning_deductions`

**Inputs** self.

**Record and data access** read “Dunning” via get\_all · resolve a document from “Dunning” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Dunning {1} must be submitted.”.format(row.idx, row.dunning) · validation helper — translated “Row #{0}: Dunning charges require a Receive payment from a Customer.”.format(row.idx) · validation helper — translated “Row #{0}: Dunning {1} belongs to a different customer.”.format(row.idx, row.dunning) · validation helper — translated “Row #{0}: Dunning {1} belongs to a different company.”.format(row.idx, row.dunning) · validation helper — translated “Row #{0}: Dunning charges must use the income account {1} configured on Dunning {2}.”.format(row.idx, dunning.income\_account, row.dunning) · 2 additional forms in the steps below.

**Local steps**

- Set dunning\_names from set of row.dunning for row drawn from self.deductions where row.dunning.
  - Draw row from self.deductions, keep a combination only if (row.dunning).
- If not dunning\_names.
  - Return no value.
- Set dunnings from mapping of row.name → row for row drawn from Platform.get\_all(“Dunning”, filters = mapping(“name” → tuple(“in”, list(dunning\_names))), fields = list(“name”, “docstatus”, “customer”, “company”, …)).
  - Draw row from Platform.get\_all(“Dunning”, filters = mapping(“name” → tuple(“in”, list(dunning\_names))), fields = list(“name”, “docstatus”, “customer”, “company”, …)).
- For each row in self.deductions.
  - If not row.dunning.
    - Continue with the next iteration or loop test.
  - Set dunning from dunnings.get(row.dunning).
  - If (not dunning or dunning.docstatus differs from 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not dunning → dunning.docstatus differs from 1.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Dunning {1} must be submitted.”.format(row.idx, row.dunning)).
  - If (self.payment\_type differs from “Receive” or self.party\_type differs from “Customer”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.payment\_type differs from “Receive” → self.party\_type differs from “Customer”.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Dunning charges require a Receive payment from a Customer.”.format(row.idx)).
  - If self.party differs from dunning.customer.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Dunning {1} belongs to a different customer.”.format(row.idx, row.dunning)).
  - If self.company differs from dunning.company.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Dunning {1} belongs to a different company.”.format(row.idx, row.dunning)).
  - If row.account differs from dunning.income\_account.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Dunning charges must use the income account {1} configured on Dunning {2}.”.format(row.idx, dunning.income\_account, row.dunning)).
  - If flt(row.amount) ≥ 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Dunning charges must have a negative deduction amount.”.format(row.idx)).
  - If (not self.get\_doc\_before\_save() or self.get\_doc\_before\_save().docstatus equals 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get\_doc\_before\_save() → self.get\_doc\_before\_save().docstatus equals 0.
    - If successor bound to Platform.get\_doc(“Dunning”, row.dunning).get\_settled\_successor().
      - Call the validation error handler Platform.throw(translated “Dunning {0} has already been settled through Dunning {1}.”.format(row.dunning, successor)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L835)

<a id="op-1e1553f40ed723"></a>
### Payment Entry.before save

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_matched\_unset\_payment\_requests\_to\_response().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set matched unset payment requests to response](operations-066.md#op-5149f268b78cf5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0074.json#L6059) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L49)

<a id="op-a443309aae4f0a"></a>
### Payment Entry.on submit

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Difference Amount must be zero”.

**Local steps**

- If self.difference\_amount.
  - Call the validation error handler Platform.throw(translated “Difference Amount must be zero”).
- Evaluate PaymentTaxWithholding(self).on\_submit().
- Evaluate self.update\_payment\_requests().
- Evaluate self.update\_payment\_schedule().
- Evaluate self.make\_gl\_entries().
- Evaluate self.update\_outstanding\_amounts().
- Evaluate self.update\_linked\_dunnings().
- Evaluate self.set\_status().
- Evaluate self.trigger\_invoice\_update\_for\_subscriptions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update payment requests](operations-063.md#op-1581f4d6d6ee99), [update payment schedule](operations-064.md#op-9cb0ed819994d8), [make gl entries](operations-065.md#op-7d45e904c8a49f), [update outstanding amounts](operations-063.md#op-effbf2881c6d2f), [update linked dunnings](operations-063.md#op-07443a433445e0), [set status](operations-064.md#op-cec3f4bf4f6aa7), [trigger invoice update for subscriptions](operations-064.md#op-e697758c42d7e7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0074.json#L6110) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L72)

<a id="op-07443a433445e0"></a>
### Payment Entry.update linked dunnings

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_update_linked_dunnings`

**Inputs** self.

**Local steps**

- Bind dependencies update\_dunnings\_linked\_to\_payment.
- Evaluate update\_dunnings\_linked\_to\_payment(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0074.json#L6365) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1513) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L100)

<a id="op-576c7dd7ecbd6c"></a>
### Payment Entry.validate for repost

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_for_repost`

**Inputs** self.

**Local steps**

- Evaluate validate\_docs\_for\_voucher\_types(list(“Payment Entry”)).
- Evaluate validate\_docs\_for\_deferred\_accounting(list(self.name), list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0074.json#L6425) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1523) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L110)

<a id="op-0caa77795b8226"></a>
### Payment Entry.on update after submit

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_on_update_after_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.get(“ignore\_reposting\_on\_reconciliation”).
  - Return no value.
- Set needs\_repost from self.check\_if\_fields\_updated(fields\_to\_check = list(), child\_tables = mapping(“references” → list(), “taxes” → list(), “deductions” → list())).
- If needs\_repost.
  - Evaluate self.validate\_for\_repost().
  - Evaluate self.repost\_accounting\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for repost](operations-063.md#op-576c7dd7ecbd6c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L73)

<a id="op-9c547a17706b4a"></a>
### Payment Entry.set liability account

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_liability_account`

**Inputs** self.

**Record and data access** read “Company” via get\_value · read “Account” via get\_value.

**State and service calls** msgprint with translated “Book Advance Payments as Liability option is chosen. Paid From account changed from {0} to {1}.”.format(Platform.bold(self.party\_account), Platform.bold(liability\_account)).

**Explicit results** no value.

**Local steps**

- If (self.docstatus &gt; 0 or self.payment\_type equals “Internal Transfer”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus &gt; 0 → self.payment\_type equals “Internal Transfer”.
  - Return no value.
- Set self.book\_advance\_payments\_in\_separate\_party\_account from false.
- If self.party\_type does not belong to tuple(“Customer”, “Supplier”).
  - Set self.is\_opening from “No”.
  - Return no value.
- If not Platform.db.get\_value(“Company”, self.company, “book\_advance\_payments\_in\_separate\_party\_account”).
  - Set self.is\_opening from “No”.
  - Return no value.
- Set self.book\_advance\_payments\_in\_separate\_party\_account from true.
- Set account\_type from Platform.get\_value(“Account”, mapping(“name” → self.party\_account, “company” → self.company), “account\_type”).
- If ((account\_type equals “Payable” and self.party\_type equals “Customer”) or (account\_type equals “Receivable” and self.party\_type equals “Supplier”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (account\_type equals “Payable” and self.party\_type equals “Customer”) → (account\_type equals “Receivable” and self.party\_type equals “Supplier”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type equals “Payable” → self.party\_type equals “Customer”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type equals “Receivable” → self.party\_type equals “Supplier”.
  - Set self.is\_opening from “No”.
  - Return no value.
- If self.references.
  - Set allowed\_types from frozenset(list(“Sales Order”, “Purchase Order”)).
  - Set reference\_types from set(list of x.reference\_doctype for x drawn from self.references).
    - Draw x from self.references.
  - If (reference\_types − allowed\_types).
    - Set self.book\_advance\_payments\_in\_separate\_party\_account from false.
    - Set self.is\_opening from “No”.
    - Return no value.
- Set accounts from get\_party\_account(self.party\_type, self.party, self.company, include\_advance = true).
- Set liability\_account from accounts at 1 when len(accounts) &gt; 1, otherwise no value.
  - Value choice on len(accounts) &gt; 1 — true gives accounts at 1, false gives no value.
- Set fieldname from “default\_advance\_received\_account” when self.party\_type equals “Customer”, otherwise “default\_advance\_paid\_account”.
  - Value choice on self.party\_type equals “Customer” — true gives “default\_advance\_received\_account”, false gives “default\_advance\_paid\_account”.
- If not liability\_account.
  - Evaluate throw(translated “Please set default {0} in Company {1}”.format(Platform.bold(nested operand in the contract.get\_meta(“Company”).get\_label(fieldname)), Platform.bold(self.company))).
- Evaluate self.set(self.party\_account\_field, liability\_account).
- Evaluate Platform.msgprint(translated “Book Advance Payments as Liability option is chosen. Paid From account changed from {0} to {1}.”.format(Platform.bold(self.party\_account), Platform.bold(liability\_account)), a ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L82)

<a id="op-873d96b6aeb30c"></a>
### Payment Entry.on cancel

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Payment Ledger Entry”, “Repost Payment Ledger”, …).
- Evaluate super().on\_cancel().
- Evaluate PaymentTaxWithholding(self).on\_cancel().
- Evaluate self.update\_payment\_requests(cancel = true).
- Evaluate self.update\_payment\_schedule(cancel = 1).
- Evaluate self.make\_gl\_entries(cancel = 1).
- Evaluate self.update\_outstanding\_amounts().
- Evaluate self.update\_linked\_dunnings().
- Evaluate self.delink\_advance\_entry\_references().
- Evaluate self.set\_status().
- Evaluate self.trigger\_invoice\_update\_for\_subscriptions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update payment requests](operations-063.md#op-1581f4d6d6ee99), [update payment schedule](operations-064.md#op-9cb0ed819994d8), [make gl entries](operations-065.md#op-7d45e904c8a49f), [update outstanding amounts](operations-063.md#op-effbf2881c6d2f), [update linked dunnings](operations-063.md#op-07443a433445e0), [delink advance entry references](operations-063.md#op-2fe6d099720e6d), [set status](operations-064.md#op-cec3f4bf4f6aa7), [trigger invoice update for subscriptions](operations-064.md#op-e697758c42d7e7).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L1112) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L70)

<a id="op-1581f4d6d6ee99"></a>
### Payment Entry.update payment requests

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_update_payment_remote_requests`

**Inputs** self, cancel = false.

**Local steps**

- Bind dependencies update\_payment\_requests\_as\_per\_pe\_references.
- Evaluate update\_payment\_requests\_as\_per\_pe\_references(self.references, cancel = cancel).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L1508) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1515) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L102)

<a id="op-effbf2881c6d2f"></a>
### Payment Entry.update outstanding amounts

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_update_outstanding_amounts`

**Inputs** self.

**Local steps**

- Evaluate self.set\_missing\_ref\_details(force = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set missing ref details](operations-064.md#op-b2c3ee93cef56a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L1593) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1514) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L101)

<a id="op-fc500b4c7e02cf"></a>
### Payment Entry.validate duplicate entry

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_duplicate_entry`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Duplicate entry in References {1} {2}”.format(d.idx, d.reference\_doctype, d.reference\_name).

**Local steps**

- Set reference\_names from set().
- For each d in self.get(“references”).
  - Set key from tuple(d.reference\_doctype, d.reference\_name, d.payment\_term, d.payment\_request).
  - If key belongs to reference\_names.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Duplicate entry in References {1} {2}”.format(d.idx, d.reference\_doctype, d.reference\_name)).
  - Evaluate reference\_names.add(key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L1655) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1522) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L109)

<a id="op-c67f61de3f4be3"></a>
### Payment Entry.set bank account data

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_bank_account_data`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.bank\_account.
  - Return no value.
- Set bank\_data from get\_bank\_account\_details(self.bank\_account).
- Set field from “paid\_from” when self.payment\_type equals “Pay”, otherwise “paid\_to”.
  - Value choice on self.payment\_type equals “Pay” — true gives “paid\_from”, false gives “paid\_to”.
- Set self.bank from bank\_data.bank.
- Set self.bank\_account\_no from bank\_data.bank\_account\_no.
- If not self.get(field).
  - Evaluate self.set(field, bank\_data.account).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L1911) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L77)

<a id="op-56339c38e21f2a"></a>
### Payment Entry.validate payment type with outstanding

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_payment_type_with_outstanding`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot receive from customer against negative outstanding”.

**Local steps**

- Set total\_outstanding from sum(generator of d.allocated\_amount for d drawn from self.get(“references”)).
  - Draw d from self.get(“references”).
- If (total\_outstanding &lt; 0 and self.party\_type equals “Customer” and self.payment\_type equals “Receive”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_outstanding &lt; 0 → self.party\_type equals “Customer” → self.payment\_type equals “Receive”.
  - Call the validation error handler Platform.throw(translated “Cannot receive from customer against negative outstanding”, title = translated “Incorrect Payment Type”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L2151) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L117)

<a id="op-c366b1c9048281"></a>
### Payment Entry.validate allocated amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_allocated_amount`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — fail\_message.format(d.idx).

**Local steps**

- <a id="op-c366b1c9048281-guard-2"></a>If self.payment\_type equals “Internal Transfer”.
  - Return no value.
- Evaluate self.validate\_allocated\_amount\_as\_per\_payment\_request().
- If self.party\_type belongs to tuple(“Customer”, “Supplier”).
  - Evaluate self.validate\_allocated\_amount\_with\_latest\_data().
  - Return no value.
- Set fail\_message from translated “Row #{0}: Allocated Amount cannot be greater than outstanding amount.”.
- For each d in self.get(“references”).
  - Set precision from d.precision(“allocated\_amount”).
  - Set allocated\_amount from flt(d.allocated\_amount, precision).
  - Set outstanding\_amount from flt(d.outstanding\_amount, precision).
  - If (allocated\_amount &gt; 0 and allocated\_amount &gt; outstanding\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocated\_amount &gt; 0 → allocated\_amount &gt; outstanding\_amount.
    - Call the validation error handler Platform.throw(fail\_message.format(d.idx)).
  - If (allocated\_amount &lt; 0 and allocated\_amount &lt; outstanding\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocated\_amount &lt; 0 → allocated\_amount &lt; outstanding\_amount.
    - Call the validation error handler Platform.throw(fail\_message.format(d.idx)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.payment\_type equals “Internal Transfer”, self.payment\_type = “Internal Transfer” selects the branch that returns no value. With self.payment\_type = “Receive”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c366b1c9048281-guard-2)

**Methods declared on this owner** [validate allocated amount as per payment request](operations-063.md#op-19f85743b450be), [validate allocated amount with latest data](operations-063.md#op-e7c8232ebd7b03).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L105)

<a id="op-19f85743b450be"></a>
### Payment Entry.validate allocated amount as per payment request

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_allocated_amount_as_per_payment_request`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- If not self.references.
  - Return no value.
- Set pr\_outstanding\_amounts from get\_payment\_request\_outstanding\_set\_in\_references(self.references).
- If not pr\_outstanding\_amounts.
  - Return no value.
- For each ref in self.references.
  - If (ref.payment\_request and ref.allocated\_amount &gt; pr\_outstanding\_amounts at ref.payment\_request).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref.payment\_request → ref.allocated\_amount &gt; pr\_outstanding\_amounts at ref.payment\_request.
    - Call the validation error handler Platform.throw(msg = translated “Row #{0}: Allocated Amount cannot be greater than Outstanding Amount of Payment Request {1}”.format(ref.idx, get\_link\_to\_form(“Payment Request”, ref.payment\_request)), titl ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L2876) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L106)

<a id="op-0af29dfe34262c"></a>
### Payment Entry.term based allocation enabled for reference

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_term_based_allocation_enabled_for_reference`

**Inputs** self, reference\_doctype, reference\_name.

**Declared result** bool.

**Record and data access** read reference\_doctype via get\_value · read “Payment Terms Template” via get\_value.

**Explicit results** Platform.db.get\_value(“Payment Terms Template”, template, “allocate\_payment\_based\_on\_payment\_terms”) · false.

**Local steps**

- If (reference\_doctype and reference\_doctype belongs to list(“Sales Invoice”, “Sales Order”, “Purchase Order”, “Purchase Invoice”) and reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doctype → reference\_doctype belongs to list(“Sales Invoice”, “Sales Order”, “Purchase Order”, “Purchase Invoice”) → reference\_name.
  - If template bound to Platform.db.get\_value(reference\_doctype, reference\_name, “payment\_terms\_template”).
    - Return Platform.db.get\_value(“Payment Terms Template”, template, “allocate\_payment\_based\_on\_payment\_terms”).
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L3174) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1511) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L98)

<a id="op-e7c8232ebd7b03"></a>
### Payment Entry.validate allocated amount with latest data

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_allocated_amount_with_latest_data`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} has Payment Term based allocation enabled. Select a Payment Term for Row #{1} in Payment References section”.format(Platform.bold(d.reference\_name), Platform.bold(idx)) · validation helper — translated “{0} {1} has already been fully paid.”.format(translated d.reference\_doctype, d.reference\_name) · validation helper — translated “{0} {1} has already been partly paid. Please use the 'Get Outstanding Invoice' or the 'Get Outstanding Order …”.format(translated d.reference\_doctype, d.reference\_name) · validation helper — translated “Row #{0}: Allocated amount:{1} is greater than outstanding amount:{2} for Payment Term {3}”.format(d.idx, allocated\_term\_amount, latest.payment\_term\_outstanding, d.payment\_term) · validation helper — fail\_message.format(d.idx).

**Local steps**

- If not self.references.
  - Return no value.
- Set uniq\_vouchers from set of tuple(x.reference\_doctype, x.reference\_name) for x drawn from self.references.
  - Draw x from self.references.
- Set vouchers from list of Platform.\_dict(mapping(“voucher\_type” → x at 0, “voucher\_no” → x at 1)) for x drawn from uniq\_vouchers.
  - Draw x from uniq\_vouchers.
- Set latest\_references from get\_outstanding\_reference\_documents(mapping(“posting\_date” → self.posting\_date, “company” → self.company, “party\_type” → self.party\_type, “payment\_type” → self.payment\_type, …), validate = true).
  - Value choice on self.payment\_type equals “Receive” — true gives self.paid\_from, false gives self.paid\_to.
- Set latest\_lookup from mapping().
- For each d in latest\_references.
  - Set d from Platform.\_dict(d).
  - Set latest\_lookup.setdefault(tuple(d.voucher\_type, d.voucher\_no), Platform.\_dict()) at d.payment\_term from d.
- Set allocated\_amounts from mapping().
- Set allocated\_term\_amounts from mapping().
- For each tuple(idx, d) in enumerate(self.get(“references”), start = 1).
  - Set latest from (latest\_lookup.get(tuple(d.reference\_doctype, d.reference\_name)) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in latest\_lookup.get(tuple(d.reference\_doctype, d.reference\_name)) → Platform.\_dict().
  - If ((d.payment\_term is identical to no value or d.payment\_term equals empty text) and self.term\_based\_allocation\_enabled\_for\_reference(d.reference\_doctype, d.reference\_name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (d.payment\_term is identical to no value or d.payment\_term equals empty text) → self.term\_based\_allocation\_enabled\_for\_reference(d.reference\_doctype, d.reference\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.payment\_term is identical to no value → d.payment\_term equals empty text.
    - Call the validation error handler Platform.throw(translated “{0} has Payment Term based allocation enabled. Select a Payment Term for Row #{1} in Payment References section”.format(Platform.bold(d.reference\_name), Platform.bold(idx))).
  - Set latest from (latest.get(d.payment\_term) or latest.get(no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in latest.get(d.payment\_term) → latest.get(no value).
  - If not latest.
    - Call the validation error handler Platform.throw(translated “{0} {1} has already been fully paid.”.format(translated d.reference\_doctype, d.reference\_name)).
  - Otherwise.
    - If (latest.outstanding\_amount &lt; latest.invoice\_amount and flt(d.outstanding\_amount, d.precision(“outstanding\_amount”)) differs from flt(latest.outstanding\_amount, d.precision(“outstanding\_amount”)) and d.paym ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in latest.outstanding\_amount &lt; latest.invoice\_amount → flt(d.outstanding\_amount, d.precision(“outstanding\_amount”)) differs from flt(latest.outstanding\_amount, d.precision(“outstanding\_amount”)) → d.payment\_term equals empty text.
      - Call the validation error handler Platform.throw(translated “{0} {1} has already been partly paid. Please use the 'Get Outstanding Invoice' or the 'Get Outstanding Order …”.format(translated d.reference\_doctype, d.reference\_name)).
  - Set fail\_message from translated “Row #{0}: Allocated Amount cannot be greater than outstanding amount.”.
  - Set precision from d.precision(“allocated\_amount”).
  - Set allocated\_amount from flt(d.allocated\_amount, precision).
  - Set key from tuple(d.reference\_doctype, d.reference\_name).
  - Set allocated\_amounts at key from (allocated\_amounts.get(key, 0) + allocated\_amount).
  - Set total\_allocated\_amount from flt(allocated\_amounts at key, precision).
  - Set outstanding\_amount from flt(latest.get(“invoice\_outstanding\_amount”, latest.outstanding\_amount), precision).
  - Set term\_key from tuple(expanded key, latest.payment\_term).
  - Set allocated\_term\_amounts at term\_key from (allocated\_term\_amounts.get(term\_key, 0) + allocated\_amount).
  - Set allocated\_term\_amount from flt(allocated\_term\_amounts at term\_key, precision).
  - If (d.payment\_term and (allocated\_term\_amount &gt; 0 and latest.payment\_term\_outstanding and allocated\_term\_amount &gt; flt(latest.payment\_term\_outstanding, precision)) and self.term\_based\_allocation\_enabled\_for\_re ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.payment\_term → (allocated\_term\_amount &gt; 0 and latest.payment\_term\_outstanding and allocated\_term\_amount &gt; flt(latest.payment\_term\_outstanding, precision)) → self.term\_based\_allocation\_enabled\_for\_reference(d.reference\_doctype, d.reference\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocated\_term\_amount &gt; 0 → latest.payment\_term\_outstanding → allocated\_term\_amount &gt; flt(latest.payment\_term\_outstanding, precision).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Allocated amount:{1} is greater than outstanding amount:{2} for Payment Term {3}”.format(d.idx, allocated\_term\_amount, latest.payment\_term\_outstanding, d.payment\_term)).
  - If (allocated\_amount &gt; 0 and total\_allocated\_amount &gt; outstanding\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocated\_amount &gt; 0 → total\_allocated\_amount &gt; outstanding\_amount.
    - Call the validation error handler Platform.throw(fail\_message.format(d.idx)).
  - If (allocated\_amount &lt; 0 and total\_allocated\_amount &lt; outstanding\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocated\_amount &lt; 0 → total\_allocated\_amount &lt; outstanding\_amount.
    - Call the validation error handler Platform.throw(fail\_message.format(d.idx)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [term based allocation enabled for reference](operations-063.md#op-0af29dfe34262c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1520) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L107)

<a id="op-2fe6d099720e6d"></a>
### Payment Entry.delink advance entry references

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_delink_advance_entry_references`

**Inputs** self.

**Local steps**

- For each reference in self.references.
  - If reference.reference\_doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
    - Set doc from Platform.get\_lazy\_doc(reference.reference\_doctype, reference.reference\_name).
    - Evaluate doc.delink\_advance\_entries(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L5203) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L55)
