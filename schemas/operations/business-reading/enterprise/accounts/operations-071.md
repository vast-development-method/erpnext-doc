# Accounting and settlement · operations 71

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment reconciliation

[Record definition](../../../../data/record-types/payment_reconciliation.json)

<a id="op-fc13645521d88b"></a>
### Payment Reconciliation.delete

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_delete`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6806) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L246)

<a id="op-a1af3244ae9c11"></a>
### Payment Reconciliation.get unreconciled entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_unreconciled_entries`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.validate\_payment\_limit().
- Evaluate self.get\_nonreconciled\_payment\_entries().
- Evaluate self.get\_invoice\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate payment limit](operations-071.md#op-c38f802235b433), [get nonreconciled payment entries](operations-071.md#op-20066b8282b4ab), [get invoice entries](operations-071.md#op-062ace3e35dd01).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L11) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L262)

<a id="op-c38f802235b433"></a>
### Payment Reconciliation.validate payment limit

`operation_enterprise_binding_enterprise_accounts_doctype_payment_reconciliation_payment_reconciliation_paymentreconciliation_validate_payment_limit`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with TypeError — translated “Payment Limit must be a non-negative integer”.

**Local steps**

- If not self.payment\_limit.
  - Return no value.
- Attempt the following.
  - Set self.payment\_limit from int(self.payment\_limit).
- On failure (tuple(TypeError, ValueError)).
  - Call the validation error handler Platform.throw(translated “Payment Limit must be a non-negative integer”, TypeError).
- <a id="op-c38f802235b433-guard-10"></a>If self.payment\_limit &lt; 0.
  - Call the validation error handler Platform.throw(translated “Payment Limit must be a non-negative integer”, TypeError).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.payment\_limit &lt; 0, self.payment\_limit = -1 selects the branch that calls the validation-error handler with translated “Payment Limit must be a non-negative integer”. With self.payment\_limit = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c38f802235b433-guard-10)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L851)

<a id="op-20066b8282b4ab"></a>
### Payment Reconciliation.get nonreconciled payment entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_nonreconciled_payment_entries`

**Inputs** self.

**Local steps**

- Evaluate self.check\_mandatory\_to\_fetch().
- Set payment\_entries from self.get\_payment\_entries().
- Set journal\_entries from self.get\_jv\_entries().
- If self.party\_type belongs to list(“Customer”, “Supplier”).
  - Set dr\_or\_cr\_notes from self.get\_dr\_or\_cr\_notes().
- Otherwise.
  - Set dr\_or\_cr\_notes from list().
- Set non\_reconciled\_payments from ((payment\_entries + journal\_entries) + dr\_or\_cr\_notes).
- If self.payment\_limit.
  - Set non\_reconciled\_payments from non\_reconciled\_payments at slice no value to self.payment\_limit.
- Set non\_reconciled\_payments from sorted(non\_reconciled\_payments, key = deferred anonymous expression).
- Evaluate self.add\_payment\_entries(non\_reconciled\_payments).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check mandatory to fetch](operations-071.md#op-a0b049cd3ed784), [get payment entries](operations-071.md#op-74195f48cfa784), [get jv entries](operations-071.md#op-d969f8588456d0), [get dr or cr notes](operations-071.md#op-02ab8965e14dfb), [add payment entries](operations-071.md#op-d1d44313844f54).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L5) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L256)

<a id="op-2e897ef5d44960"></a>
### Payment Reconciliation.get permitted dimension values

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_permitted_dimension_values`

**Inputs** self, document\_type, reference\_doctype.

**Explicit results** get\_allowed\_docs\_for\_doctype(self.user\_permissions.get(document\_type, list()), reference\_doctype).

**Local steps**

- Return get\_allowed\_docs\_for\_doctype(self.user\_permissions.get(document\_type, list()), reference\_doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L388) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L8) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L259)

<a id="op-0b75113f41e064"></a>
### Payment Reconciliation.validate permitted dimension value

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_validate_permitted_dimension_value`

**Inputs** self, document\_type, value, allowed.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have enough permission to access {0}: {1}”.format(translated document\_type, value).

**Local steps**

- If (value and allowed and value does not belong to allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → allowed → value does not belong to allowed.
  - Call the validation error handler Platform.throw(translated “You do not have enough permission to access {0}: {1}”.format(translated document\_type, value), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L483) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L23) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L274)

<a id="op-961c1f61748312"></a>
### Payment Reconciliation.get user permission dimension condition

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_user_permission_dimension_condition`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, field, allowed.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L652) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L12) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L263)

<a id="op-74195f48cfa784"></a>
### Payment Reconciliation.get payment entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_payment_entries`

**Inputs** self.

**Explicit results** payment\_entries.

**Local steps**

- Set party\_account from list(self.receivable\_payable\_account).
- Set order\_doctype from “Sales Order” when self.party\_type equals “Customer”, otherwise “Purchase Order”.
  - Value choice on self.party\_type equals “Customer” — true gives “Sales Order”, false gives “Purchase Order”.
- Set condition from Platform.\_dict(mapping(“company” → self.get(“company”), “get\_payments” → true, “cost\_center” → self.get(“cost\_center”), “from\_payment\_date” → self.get(“from\_payment\_date”), …)).
- If self.payment\_name.
  - Evaluate condition.update(mapping(“name” → self.payment\_name)).
- Set dimensions from mapping().
- For each x in self.dimensions.
  - Set dimension from x.fieldname.
  - Set allowed from self.get\_permitted\_dimension\_values(x.document\_type, “Payment Entry”).
  - If value bound to self.get(dimension).
    - Evaluate self.validate\_permitted\_dimension\_value(x.document\_type, value, allowed).
    - Set dimensions at dimension from value.
  - Otherwise.
    - If allowed.
      - Set dimensions at dimension from allowed.
- Evaluate condition.update(mapping(“accounting\_dimensions” → dimensions)).
- Set payment\_entries from get\_advance\_payment\_entries\_for\_regional(self.party\_type, self.party, party\_account, order\_doctype, default\_advance\_account = self.default\_advance\_account, against\_all\_orders = true, limit = self.payment\_l ….
- Return payment\_entries.

**Methods declared on this owner** [get permitted dimension values](operations-071.md#op-2e897ef5d44960), [validate permitted dimension value](operations-071.md#op-0b75113f41e064).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L807) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L7) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L258)

<a id="op-d969f8588456d0"></a>
### Payment Reconciliation.get jv entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_journal_voucher_entries`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** list(journal\_entries).

**Local steps**

- Set je from qb.DocType(“Journal Entry”).
- Set jea from qb.DocType(“Journal Entry Account”).
- Set conditions from self.get\_journal\_filter\_conditions().
- For each x in self.dimensions.
  - Set dimension from x.fieldname.
  - Set allowed from self.get\_permitted\_dimension\_values(x.document\_type, “Journal Entry Account”).
  - If value bound to self.get(dimension).
    - Evaluate self.validate\_permitted\_dimension\_value(x.document\_type, value, allowed).
    - Evaluate conditions.append(jea at dimension equals value).
  - Otherwise.
    - If allowed.
      - Evaluate conditions.append(self.get\_user\_permission\_dimension\_condition(jea at dimension, allowed)).
- If self.payment\_name.
  - Evaluate conditions.append(je.name.like(formatted text %%{self.payment\_name}%%)).
- If self.get(“cost\_center”).
  - Evaluate conditions.append(jea.cost\_center equals self.cost\_center).
- Set account\_type from Platform.get\_cached\_value(“Account”, self.receivable\_payable\_account, “account\_type”).
- If account\_type equals “Receivable”.
  - Set dr\_or\_cr from (jea.credit\_in\_account\_currency − jea.debit\_in\_account\_currency).
- Otherwise.
  - If account\_type equals “Payable”.
    - Set dr\_or\_cr from (jea.debit\_in\_account\_currency − jea.credit\_in\_account\_currency).
- Evaluate conditions.append(dr\_or\_cr.gt(0)).
- If self.bank\_cash\_account.
  - Evaluate conditions.append(jea.against\_account.like(formatted text %%{self.bank\_cash\_account}%%)).
- Set journal\_query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If self.payment\_limit.
  - Set journal\_query from journal\_query.limit(self.payment\_limit).
- Set journal\_entries from journal\_query.run(as\_dict = true).
- Return list(journal\_entries).

**Methods declared on this owner** [get journal filter conditions](operations-072.md#op-74f414161b81c9), [get permitted dimension values](operations-071.md#op-2e897ef5d44960), [validate permitted dimension value](operations-071.md#op-0b75113f41e064), [get user permission dimension condition](operations-071.md#op-961c1f61748312).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.receivable\_payable\_account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L3) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L254)

<a id="op-0225f8121cfc67"></a>
### Payment Reconciliation.get return invoices

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_return_invoices`

**Inputs** self.

**Local steps**

- Set voucher\_type from “Sales Invoice” when self.party\_type equals “Customer”, otherwise “Purchase Invoice”.
  - Value choice on self.party\_type equals “Customer” — true gives “Sales Invoice”, false gives “Purchase Invoice”.
- Set doc from qb.DocType(voucher\_type).
- Set conditions from list().
- Evaluate conditions.append(doc.docstatus equals 1).
- Evaluate conditions.append(doc at Platform.scrub(self.party\_type) equals self.party).
- Evaluate conditions.append(doc.is\_return equals 1).
- Evaluate conditions.append(doc.outstanding\_amount differs from 0).
- If self.payment\_name.
  - Evaluate conditions.append(doc.name.like(formatted text %{self.payment\_name}%)).
- Set self.return\_invoices\_query from qb.from\_(doc).select(ConstantColumn(voucher\_type).as\_(“voucher\_type”), doc.name.as\_(“voucher\_no”), doc.return\_against).where(Criterion.all(conditions)).
- If self.payment\_limit.
  - Set self.return\_invoices\_query from self.return\_invoices\_query.limit(self.payment\_limit).
- Set self.return\_invoices from self.return\_invoices\_query.run(as\_dict = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L3065) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L9) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L260)

<a id="op-02ab8965e14dfb"></a>
### Payment Reconciliation.get dr or cr notes

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_debit_or_credit_notes`

**Inputs** self.

**Explicit results** outstanding\_dr\_or\_cr.

**Local steps**

- Evaluate self.build\_qb\_filter\_conditions(get\_return\_invoices = true).
- Set ple from qb.DocType(“Payment Ledger Entry”).
- If Enterprise.get\_party\_account\_type(self.party\_type) equals “Receivable”.
  - Evaluate self.common\_filter\_conditions.append(ple.account\_type equals “Receivable”).
- Otherwise.
  - Evaluate self.common\_filter\_conditions.append(ple.account\_type equals “Payable”).
- Evaluate self.common\_filter\_conditions.append(ple.account equals self.receivable\_payable\_account).
- Evaluate self.get\_return\_invoices().
- Set outstanding\_dr\_or\_cr from list().
- If self.return\_invoices.
  - Set ple\_query from QueryPaymentLedger().
  - Set return\_outstanding from ple\_query.get\_voucher\_outstandings(vouchers = self.return\_invoices, common\_filter = self.common\_filter\_conditions, posting\_date = self.ple\_posting\_date\_filter, min\_outstanding = negative self.minimum\_payme ….
    - Value choice on self.minimum\_payment\_amount — true gives negative self.minimum\_payment\_amount, false gives no value.
    - Value choice on self.maximum\_payment\_amount — true gives negative self.maximum\_payment\_amount, false gives no value.
  - For each inv in return\_outstanding.
    - If inv.outstanding differs from 0.
      - Evaluate outstanding\_dr\_or\_cr.append(Platform.\_dict(mapping(“reference\_type” → inv.voucher\_type, “reference\_name” → inv.voucher\_no, “amount” → negative inv.outstanding\_in\_account\_currency, “posting\_date” → inv.post ….
- Return outstanding\_dr\_or\_cr.

**Methods declared on this owner** [build qb filter conditions](operations-072.md#op-20c7b8d5a28634), [get return invoices](operations-071.md#op-0225f8121cfc67).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L3708) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L249)

<a id="op-d1d44313844f54"></a>
### Payment Reconciliation.add payment entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_add_payment_entries`

**Inputs** self, non\_reconciled\_payments.

**Local steps**

- Evaluate self.set(“payments”, list()).
- For each payment in non\_reconciled\_payments.
  - Set row from self.append(“payments”, mapping()).
  - Evaluate row.update(payment).
  - Set row.is\_advance from payment.book\_advance\_payments\_in\_separate\_party\_account.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L4428) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L238)

<a id="op-062ace3e35dd01"></a>
### Payment Reconciliation.get invoice entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_invoice_entries`

**Inputs** self, vouchers = no value.

**Local steps**

- Evaluate self.build\_qb\_filter\_conditions(get\_invoices = true).
- Set accounts from list(self.receivable\_payable\_account).
- If self.default\_advance\_account.
  - Evaluate accounts.append(self.default\_advance\_account).
- Set non\_reconciled\_invoices from get\_outstanding\_invoices(self.party\_type, self.party, accounts, common\_filter = self.common\_filter\_conditions, posting\_date = self.ple\_posting\_date\_filter, min\_outstanding = self.minimum\_invoice\_amount whe ….
  - Value choice on self.minimum\_invoice\_amount — true gives self.minimum\_invoice\_amount, false gives no value.
  - Value choice on self.maximum\_invoice\_amount — true gives self.maximum\_invoice\_amount, false gives no value.
  - Value choice on not vouchers — true gives self.invoice\_limit, false gives no value.
- Set cr\_dr\_notes from list of x.voucher\_no for x drawn from self.return\_invoices when self.party\_type belongs to list(“Customer”, “Supplier”), otherwise list().
  - Value choice on self.party\_type belongs to list(“Customer”, “Supplier”) — true gives list of x.voucher\_no for x drawn from self.return\_invoices, false gives list().
  - Draw x from self.return\_invoices.
- Set non\_reconciled\_invoices from list of x for x drawn from non\_reconciled\_invoices where x.voucher\_no does not belong to cr\_dr\_notes.
  - Draw x from non\_reconciled\_invoices, keep a combination only if (x.voucher\_no does not belong to cr\_dr\_notes).
- If (self.invoice\_limit and not vouchers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.invoice\_limit → not vouchers.
  - Set non\_reconciled\_invoices from non\_reconciled\_invoices at slice no value to self.invoice\_limit.
- Set non\_reconciled\_invoices from sorted(non\_reconciled\_invoices, key = deferred anonymous expression).
- Evaluate self.add\_invoice\_entries(non\_reconciled\_invoices).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build qb filter conditions](operations-072.md#op-20c7b8d5a28634), [add invoice entries](operations-071.md#op-de396954f4235e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L251)

<a id="op-de396954f4235e"></a>
### Payment Reconciliation.add invoice entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_add_invoice_entries`

**Inputs** self, non\_reconciled\_invoices.

**Local steps**

- Evaluate self.set(“invoices”, list()).
- For each entry in non\_reconciled\_invoices.
  - Set inv from self.append(“invoices”, mapping()).
  - Set inv.invoice\_type from entry.get(“voucher\_type”).
  - Set inv.invoice\_number from entry.get(“voucher\_no”).
  - Set inv.invoice\_date from entry.get(“posting\_date”).
  - Set inv.amount from flt(entry.get(“invoice\_amount”)).
  - Set inv.currency from entry.get(“currency”).
  - Set inv.outstanding\_amount from flt(entry.get(“outstanding\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L5192) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L237)

<a id="op-77d974489c406b"></a>
### Payment Reconciliation.get difference amount

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_difference_amount`

**Inputs** self, payment\_entry, invoice, allocated\_amount.

**Record and data access** read “Account” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** difference\_amount.

**Local steps**

- Set party\_account\_defaults from Platform.get\_cached\_value(“Account”, self.receivable\_payable\_account, list(“account\_type”, “account\_currency”), as\_dict = true).
- Set allocated\_amount\_precision from get\_field\_precision(Platform.get\_meta(“Payment Reconciliation Allocation”).get\_field(“allocated\_amount”)).
- Set difference\_amount\_precision from get\_field\_precision(Platform.get\_meta(“Payment Reconciliation Allocation”).get\_field(“difference\_amount”)).
- Set difference\_amount from 0.
- If party\_account\_defaults.get(“account\_currency”) differs from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
  - If (invoice.get(“exchange\_rate”) and payment\_entry.get(“exchange\_rate”, 1) differs from invoice.get(“exchange\_rate”, 1)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoice.get(“exchange\_rate”) → payment\_entry.get(“exchange\_rate”, 1) differs from invoice.get(“exchange\_rate”, 1).
    - Set allocated\_amount\_in\_ref\_rate from flt((payment\_entry.get(“exchange\_rate”, 1) × flt(allocated\_amount, allocated\_amount\_precision)), difference\_amount\_precision).
    - Set allocated\_amount\_in\_inv\_rate from flt((invoice.get(“exchange\_rate”, 1) × flt(allocated\_amount, allocated\_amount\_precision)), difference\_amount\_precision).
    - If (party\_account\_defaults.get(“account\_type”) belongs to “Payable” and invoice.get(“invoice\_type”) belongs to list(“Payment Entry”, “Journal Entry”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account\_defaults.get(“account\_type”) belongs to “Payable” → invoice.get(“invoice\_type”) belongs to list(“Payment Entry”, “Journal Entry”).
      - Set difference\_amount from (allocated\_amount\_in\_inv\_rate − allocated\_amount\_in\_ref\_rate).
    - Otherwise.
      - Set difference\_amount from (allocated\_amount\_in\_ref\_rate − allocated\_amount\_in\_inv\_rate).
- Return difference\_amount.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.receivable\_payable\_account, list(“account\_type”, “account\_currency”), as\_dict = true), Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L5556) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L250)

<a id="op-2cdb0f9f6e76e1"></a>
### Payment Reconciliation.is auto process enabled

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_is_auto_process_enabled`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”).

**Local steps**

- Return Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0093.json#L6318) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L14) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L265)

<a id="op-b0f04fa523ba9b"></a>
### Payment Reconciliation.calculate difference on allocation change

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_calculate_difference_on_allocation_change`

**Inputs** self, payment\_entry, invoice, allocated\_amount.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** new\_difference\_amount.

**Local steps**

- Set invoice\_exchange\_map from self.get\_invoice\_exchange\_map(invoice, payment\_entry).
- Set invoice at 0 at “exchange\_rate” from invoice\_exchange\_map.get(invoice at 0.get(“invoice\_number”)).
- If payment\_entry at 0.get(“reference\_type”) belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Set payment\_entry at 0 at “exchange\_rate” from invoice\_exchange\_map.get(payment\_entry at 0.get(“reference\_name”)).
- Set new\_difference\_amount from self.get\_difference\_amount(payment\_entry at 0, invoice at 0, allocated\_amount).
- Return new\_difference\_amount.

**Methods declared on this owner** [get invoice exchange map](operations-072.md#op-939daeda6f6d58), [get difference amount](operations-071.md#op-77d974489c406b).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L242)

<a id="op-23b84610e10b99"></a>
### Payment Reconciliation.allocate entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_allocate_entries`

**Inputs** self, args.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Company” via get\_cached\_value.

**Local steps**

- Evaluate self.validate\_entries().
- Set exc\_gain\_loss\_posting\_date from Platform.db.get\_single\_value(“Accounts Settings”, “exchange\_gain\_loss\_posting\_date”, cache = true).
- Set invoice\_exchange\_map from self.get\_invoice\_exchange\_map(args.get(“invoices”), args.get(“payments”)).
- Set default\_exchange\_gain\_loss\_account from Platform.get\_cached\_value(“Company”, self.company, “exchange\_gain\_loss\_account”).
- Set entries from list().
- For each pay in args.get(“payments”).
  - Evaluate pay.update(mapping(“unreconciled\_amount” → pay.get(“amount”))).
  - For each inv in args.get(“invoices”).
    - If pay.get(“amount”) ≥ inv.get(“outstanding\_amount”).
      - Set res from self.get\_allocated\_entry(pay, inv, inv at “outstanding\_amount”).
      - Set pay at “amount” from (flt(pay.get(“amount”)) − flt(inv.get(“outstanding\_amount”))).
      - Set inv at “outstanding\_amount” from 0.
    - Otherwise.
      - Set res from self.get\_allocated\_entry(pay, inv, pay at “amount”).
      - Set inv at “outstanding\_amount” from (flt(inv.get(“outstanding\_amount”)) − flt(pay.get(“amount”))).
      - Set pay at “amount” from 0.
    - Set inv at “exchange\_rate” from invoice\_exchange\_map.get(inv.get(“invoice\_number”)).
    - If pay.get(“reference\_type”) belongs to list(“Sales Invoice”, “Purchase Invoice”).
      - Set pay at “exchange\_rate” from invoice\_exchange\_map.get(pay.get(“reference\_name”)).
    - Set res.difference\_amount from self.get\_difference\_amount(pay, inv, res at “allocated\_amount”).
    - Set res.difference\_account from default\_exchange\_gain\_loss\_account.
    - Set res.exchange\_rate from inv.get(“exchange\_rate”).
    - Evaluate res.update(mapping(“gain\_loss\_posting\_date” → pay.get(“posting\_date”))).
    - If not pay.get(“is\_advance”).
      - If exc\_gain\_loss\_posting\_date equals “Invoice”.
        - Evaluate res.update(mapping(“gain\_loss\_posting\_date” → inv.get(“invoice\_date”))).
      - Otherwise.
        - If exc\_gain\_loss\_posting\_date equals “Reconciliation Date”.
          - Evaluate res.update(mapping(“gain\_loss\_posting\_date” → nowdate())).
    - If pay.get(“amount”) equals 0.
      - Evaluate entries.append(res).
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Otherwise.
      - If inv.get(“outstanding\_amount”) equals 0.
        - Evaluate entries.append(res).
        - Continue with the next iteration or loop test.
  - After normal loop exhaustion.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate self.set(“allocation”, list()).
- For each entry in entries.
  - If entry at “allocated\_amount” differs from 0.
    - Set row from self.append(“allocation”, mapping()).
    - Evaluate row.update(entry).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate entries](operations-072.md#op-ad1ff0b85593e7), [get invoice exchange map](operations-072.md#op-939daeda6f6d58), [get allocated entry](operations-071.md#op-6912df698b6e57), [get difference amount](operations-071.md#op-77d974489c406b).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “exchange\_gain\_loss\_posting\_date”, cache = true), Platform.get\_cached\_value(“Company”, self.company, “exchange\_gain\_loss\_account”) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L239)

<a id="op-c52151e1940281"></a>
### Payment Reconciliation.update dimension values in allocated entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_update_dimension_values_in_allocated_entries`

**Inputs** self, res.

**Explicit results** res.

**Local steps**

- For each x in self.dimensions.
  - Set dimension from x.fieldname.
  - If self.get(dimension).
    - Set res at dimension from self.get(dimension).
- Return res.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0094.json#L1689) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L19) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L270)

<a id="op-6912df698b6e57"></a>
### Payment Reconciliation.get allocated entry

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_allocated_entry`

**Inputs** self, pay, inv, allocated\_amount.

**Explicit results** res.

**Local steps**

- Set res from Platform.\_dict(mapping(“reference\_type” → pay.get(“reference\_type”), “reference\_name” → pay.get(“reference\_name”), “reference\_row” → pay.get(“reference\_row”), “invoice\_type” → inv.get(“invoice\_type”), …)).
- Set res from self.update\_dimension\_values\_in\_allocated\_entries(res).
- Return res.

**Methods declared on this owner** [update dimension values in allocated entries](operations-071.md#op-c52151e1940281).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0094.json#L1831) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L247)

<a id="op-ff091a963dfca4"></a>
### Payment Reconciliation.reconcile allocations

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_reconcile_allocations`

**Inputs** self, skip\_ref\_details\_update\_for\_pe = false.

**Record and data access** read “Account” via get\_cached\_value.

**Local steps**

- Evaluate adjust\_allocations\_for\_taxes(self).
- Set account\_type from Platform.get\_cached\_value(“Account”, self.receivable\_payable\_account, “account\_type”).
- Set dr\_or\_cr from “credit\_in\_account\_currency” when account\_type equals “Receivable”, otherwise “debit\_in\_account\_currency”.
  - Value choice on account\_type equals “Receivable” — true gives “credit\_in\_account\_currency”, false gives “debit\_in\_account\_currency”.
- Set entry\_list from list().
- Set dr\_or\_cr\_notes from list().
- For each row in self.get(“allocation”).
  - Set reconciled\_entry from list().
  - If (row.invoice\_number and row.allocated\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.invoice\_number → row.allocated\_amount.
    - If row.reference\_type belongs to list(“Sales Invoice”, “Purchase Invoice”).
      - Set reconciled\_entry from dr\_or\_cr\_notes.
    - Otherwise.
      - Set reconciled\_entry from entry\_list.
    - Set payment\_details from self.get\_payment\_details(row, dr\_or\_cr).
    - Evaluate reconciled\_entry.append(payment\_details).
- If entry\_list.
  - Evaluate reconcile\_against\_document(entry\_list, skip\_ref\_details\_update\_for\_pe, self.dimensions).
- If dr\_or\_cr\_notes.
  - Evaluate reconcile\_dr\_cr\_note(dr\_or\_cr\_notes, self.company, self.dimensions).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get payment details](operations-071.md#op-ddb3bc8669158b).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.receivable\_payable\_account, “account\_type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L17) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L268)

<a id="op-0c0713a85aafcb"></a>
### Payment Reconciliation.reconcile

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_reconcile`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A Reconciliation Job {0} is running for the same filters. Cannot reconcile now”.format(get\_link\_to\_form(“Auto Reconcile”, running\_doc)).

**Local steps**

- If Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”).
  - Set running\_doc from is\_any\_doc\_running(dict(company = self.company, party\_type = self.party\_type, party = self.party, receivable\_payable\_account = self.receivable\_payable\_account)).
  - If running\_doc.
    - Call the validation error handler Platform.throw(translated “A Reconciliation Job {0} is running for the same filters. Cannot reconcile now”.format(get\_link\_to\_form(“Auto Reconcile”, running\_doc))).
    - Return no value.
- Evaluate self.validate\_allocation().
- Evaluate self.reconcile\_allocations().
- Evaluate msgprint(translated “Successfully Reconciled”).
- Evaluate self.get\_unreconciled\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate allocation](operations-072.md#op-42cb853c17715b), [reconcile allocations](operations-071.md#op-ff091a963dfca4), [get unreconciled entries](operations-071.md#op-a1af3244ae9c11).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0094.json#L2785) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L16) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L267)

<a id="op-ddb3bc8669158b"></a>
### Payment Reconciliation.get payment details

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_payment_details`

**Inputs** self, row, dr\_or\_cr.

**Explicit results** payment\_details.

**Local steps**

- Set payment\_details from Platform.\_dict(mapping(“voucher\_type” → row.get(“reference\_type”), “voucher\_no” → row.get(“reference\_name”), “voucher\_detail\_no” → row.get(“reference\_row”), “against\_voucher\_type” → row.get(“invoice\_type”), …)).
- For each x in self.dimensions.
  - If row.get(x.fieldname).
    - Set payment\_details at x.fieldname from row.get(x.fieldname).
- Return payment\_details.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0094.json#L3145) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L6) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L257)

<a id="op-a0b049cd3ed784"></a>
### Payment Reconciliation.check mandatory to fetch

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_check_mandatory_to_fetch`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select {0} first”.format(translated self.meta.get\_label(fieldname)).

**Local steps**

- For each fieldname in list(“company”, “party\_type”, “party”, “receivable\_payable\_account”).
  - If not self.get(fieldname).
    - Call the validation error handler Platform.throw(translated “Please select {0} first”.format(translated self.meta.get\_label(fieldname))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L243)
