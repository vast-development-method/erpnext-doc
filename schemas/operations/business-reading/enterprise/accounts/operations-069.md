# Accounting and settlement · operations 69

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Payment ledger

<a id="op-8a7e1fb62f49f8"></a>
### Execute

`operation_enterprise_accounts_report_payment_ledger_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** PaymentLedger(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters, “period\_start\_date”, “period\_end\_date”).
- Return PaymentLedger(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1126)

## Record · Payment ledger entry

[Record definition](../../../../data/record-types/payment_ledger_entry.json)

<a id="op-01d0ac34c0deaf"></a>
### Payment Ledger Entry.validate account

`operation_enterprise_accounts_record_definitions_payment_ledger_entry_business_behavior_payment_ledger_entry_validate_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} account is not of company {1}”.format(self.account, self.company) · validation helper — translated “{0} account is not of type {1}”.format(self.account, self.account\_type).

**Local steps**

- Set account from Platform.get\_cached\_value(“Account”, self.account, fieldname = list(“account\_type”, “company”), as\_dict = true).
- If account.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “{0} account is not of company {1}”.format(self.account, self.company)).
- If account.account\_type differs from self.account\_type.
  - Call the validation error handler Platform.throw(translated “{0} account is not of type {1}”.format(self.account, self.account\_type)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, fieldname = list(“account\_type”, “company”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L4953) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L206)

<a id="op-7cc022e50826ef"></a>
### Payment Ledger Entry.validate account details

`operation_enterprise_accounts_record_definitions_payment_ledger_entry_business_behavior_payment_ledger_entry_validate_account_details`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} {1}: Account {2} is a Group Account and group accounts cannot be used in transactions”.format(self.voucher\_type, self.voucher\_no, self.account) · validation helper — translated “{0} {1}: Account {2} is inactive”.format(self.voucher\_type, self.voucher\_no, self.account) · validation helper — translated “{0} {1}: Account {2} does not belong to Company {3}”.format(self.voucher\_type, self.voucher\_no, self.account, self.company).

**Local steps**

- Set account from Platform.get\_cached\_value(“Account”, self.account, fieldname = list(“is\_group”, “docstatus”, “company”), as\_dict = true).
- If account.is\_group equals 1.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Account {2} is a Group Account and group accounts cannot be used in transactions”.format(self.voucher\_type, self.voucher\_no, self.account)).
- <a id="op-7cc022e50826ef-guard-15"></a>If account.docstatus equals 2.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Account {2} is inactive”.format(self.voucher\_type, self.voucher\_no, self.account)).
- If account.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Account {2} does not belong to Company {3}”.format(self.voucher\_type, self.voucher\_no, self.account, self.company)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison account.docstatus equals 2, account.docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “{0} {1}: Account {2} is inactive”.format(self.voucher\_type, self.voucher\_no, self.account). With account.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7cc022e50826ef-guard-15)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, fieldname = list(“is\_group”, “docstatus”, “company”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L5256) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L207)

<a id="op-c96bef006bfc9e"></a>
### Payment Ledger Entry.validate allowed dimensions

`operation_enterprise_accounts_record_definitions_payment_ledger_entry_business_behavior_payment_ledger_entry_validate_allowed_dimensions`

**Inputs** self.

**Explicit failure paths** validation helper with MandatoryAccountDimensionError — translated “{0} is mandatory for account {1}”.format(Platform.bold(dimension\_label), Platform.bold(self.account)) · validation helper with InvalidAccountDimensionError — translated “Invalid value {0} for {1} against account {2}”.format(Platform.bold(self.get(dimension)), Platform.bold(dimension\_label), Platform.bold(self.account)).

**Local steps**

- Set dimension\_filter\_map from get\_dimension\_filter\_map().
- For each tuple(key, value) in dimension\_filter\_map.items().
  - Set dimension from key at 0.
  - Set account from key at 1.
  - If self.account equals account.
    - Set dimension\_label from get\_dimension\_label(self.meta, dimension).
    - If (value at “is\_mandatory” and not self.get(dimension)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in value at “is\_mandatory” → not self.get(dimension).
      - Call the validation error handler Platform.throw(translated “{0} is mandatory for account {1}”.format(Platform.bold(dimension\_label), Platform.bold(self.account)), MandatoryAccountDimensionError).
    - If value at “allow\_or\_restrict” equals “Allow”.
      - If (self.get(dimension) and self.get(dimension) does not belong to value at “allowed\_dimensions”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(dimension) → self.get(dimension) does not belong to value at “allowed\_dimensions”.
        - Call the validation error handler Platform.throw(translated “Invalid value {0} for {1} against account {2}”.format(Platform.bold(self.get(dimension)), Platform.bold(dimension\_label), Platform.bold(self.account)), InvalidAccountDimensionError).
    - Otherwise.
      - If (self.get(dimension) and self.get(dimension) belongs to value at “allowed\_dimensions”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(dimension) → self.get(dimension) belongs to value at “allowed\_dimensions”.
        - Call the validation error handler Platform.throw(translated “Invalid value {0} for {1} against account {2}”.format(Platform.bold(self.get(dimension)), Platform.bold(dimension\_label), Platform.bold(self.account)), InvalidAccountDimensionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L208)

<a id="op-98aa76fd4d875f"></a>
### Payment Ledger Entry.validate dimensions for pl and bs

`operation_enterprise_accounts_record_definitions_payment_ledger_entry_business_behavior_payment_ledger_entry_validate_dimensions_for_profit_and_loss_and_balance_sheet`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Profit and Loss' account {1}.”.format(dimension.label, self.account) · validation helper — translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Balance Sheet' account {1}.”.format(dimension.label, self.account).

**Local steps**

- Set account\_type from Platform.get\_cached\_value(“Account”, self.account, “report\_type”).
- For each dimension in get\_checks\_for\_pl\_and\_bs\_accounts().
  - If (account\_type equals “Profit and Loss” and self.company equals dimension.company and dimension.mandatory\_for\_pl).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type equals “Profit and Loss” → self.company equals dimension.company → dimension.mandatory\_for\_pl.
    - If not self.get(dimension.fieldname).
      - Call the validation error handler Platform.throw(translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Profit and Loss' account {1}.”.format(dimension.label, self.account)).
  - If (account\_type equals “Balance Sheet” and self.company equals dimension.company and dimension.mandatory\_for\_bs).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type equals “Balance Sheet” → self.company equals dimension.company → dimension.mandatory\_for\_bs.
    - If not self.get(dimension.fieldname).
      - Call the validation error handler Platform.throw(translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Balance Sheet' account {1}.”.format(dimension.label, self.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L6488) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L209)

<a id="op-c8ebba597cd7eb"></a>
### Payment Ledger Entry.validate

`operation_enterprise_accounts_record_definitions_payment_ledger_entry_business_behavior_payment_ledger_entry_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account](operations-069.md#op-01d0ac34c0deaf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0091.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L205)

<a id="op-633b5b8f47c336"></a>
### Payment Ledger Entry.on update

`operation_enterprise_accounts_record_definitions_payment_ledger_entry_business_behavior_payment_ledger_entry_on_update`

**Inputs** self.

**Local steps**

- Set adv\_adj from self.flags.adv\_adj.
- If not self.flags.from\_repost.
  - Evaluate validate\_frozen\_account(self.company, self.account, adv\_adj).
  - If not self.delinked.
    - Evaluate self.validate\_account\_details().
    - Evaluate self.validate\_dimensions\_for\_pl\_and\_bs().
    - Evaluate self.validate\_allowed\_dimensions().
    - Evaluate validate\_balance\_type(self.account, adv\_adj).
- If (self.against\_voucher\_type belongs to OUTSTANDING\_DOCTYPES and self.flags.update\_outstanding equals “Yes” and not Platform.flags.is\_reverse\_depr\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.against\_voucher\_type belongs to OUTSTANDING\_DOCTYPES → self.flags.update\_outstanding equals “Yes” → not Platform.flags.is\_reverse\_depr\_entry.
  - Evaluate update\_voucher\_outstanding(self.against\_voucher\_type, self.against\_voucher\_no, self.account, self.party\_type, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account details](operations-069.md#op-7cc022e50826ef), [validate dimensions for pl and bs](operations-069.md#op-98aa76fd4d875f), [validate allowed dimensions](operations-069.md#op-c96bef006bfc9e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0091.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L204)

<a id="op-43ce87367759e5"></a>
### On doctype update

`operation_enterprise_accounts_record_definitions_payment_ledger_entry_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Payment Ledger Entry”.

**Local steps**

- Evaluate Platform.db.add\_index(“Payment Ledger Entry”, list(“against\_voucher\_no”, “against\_voucher\_type”)).
- Evaluate Platform.db.add\_index(“Payment Ledger Entry”, list(“voucher\_no”, “voucher\_type”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0091.json#L404) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L203)

## Record · Payment order

[Record definition](../../../../data/record-types/payment_order.json)

<a id="op-2a98167e3ca030"></a>
### Payment Order.validate

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_company\_bank\_account().
- Evaluate self.validate\_references().
- Evaluate self.validate\_references\_not\_in\_other\_orders().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate company bank account](operations-069.md#op-cf49be196d0dca), [validate references](operations-069.md#op-fde5fcd513695b), [validate references not in other orders](operations-069.md#op-7f588fe1ed6e32).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L842)

<a id="op-16f5d6a9193e38"></a>
### Payment Order.reference field

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_reference_field`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** “payment\_request” when self.payment\_order\_type equals “Payment Request”, otherwise “reference\_name”.

**Local steps**

- Return “payment\_request” when self.payment\_order\_type equals “Payment Request”, otherwise “reference\_name”.
  - Value choice on self.payment\_order\_type equals “Payment Request” — true gives “payment\_request”, false gives “reference\_name”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L840)

<a id="op-16feaf83d8d886"></a>
### Payment Order.get reference names

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_get_reference_names`

**Inputs** self.

**Explicit results** list(set of d.get(self.reference\_field) for d drawn from self.references where d.get(self.reference\_field)).

**Local steps**

- Return list(set of d.get(self.reference\_field) for d drawn from self.references where d.get(self.reference\_field)).
  - Draw d from self.references, keep a combination only if (d.get(self.reference\_field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L839)

<a id="op-fde5fcd513695b"></a>
### Payment Order.validate references

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_validate_references`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set references from self.get\_reference\_names().
- If (not self.payment\_order\_type or not references).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.payment\_order\_type → not references.
  - Return no value.
- Set order\_status\_field from “status” when self.payment\_order\_type equals “Payment Request”, otherwise “payment\_order\_status”.
  - Value choice on self.payment\_order\_type equals “Payment Request” — true gives “status”, false gives “payment\_order\_status”.
- Set reference\_details from mapping of reference.name → reference for reference drawn from Platform.qb.get\_query(self.payment\_order\_type, fields = list(“name”, “company”, “docstatus”, “status”, …), filters = mapping(“name” → list(“in ….
  - Draw reference from Platform.qb.get\_query(self.payment\_order\_type, fields = list(“name”, “company”, “docstatus”, “status”, …), filters = mapping(“name” → list(“in”, references)), for\_update = self.docstatus equals 1).run(as\_d ….
- For each d in self.references.
  - Evaluate self.validate\_reference(d, reference\_details.get(d.get(self.reference\_field))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reference names](operations-069.md#op-16feaf83d8d886), [validate reference](operations-069.md#op-1b0322c5389bb6).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L845)

<a id="op-1b0322c5389bb6"></a>
### Payment Order.validate reference

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_validate_reference`

**Inputs** self, row, reference.

**Explicit failure paths** validation helper — translated “Row #{0}: {1} {2} must be submitted”.format(row.idx, translated self.payment\_order\_type, reference\_name) · validation helper — translated “Row #{0}: {1} {2} belongs to Company {3}, not {4}”.format(row.idx, translated self.payment\_order\_type, reference\_name, reference.company, …) · validation helper — translated “Row #{0}: {1} {2} is already paid”.format(row.idx, translated self.payment\_order\_type, reference\_name) · validation helper — translated “Row #{0}: {1} {2} is already in another Payment Order”.format(row.idx, translated self.payment\_order\_type, reference\_name).

**Local steps**

- Set reference\_name from row.get(self.reference\_field).
- If (not reference or reference.docstatus differs from 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not reference → reference.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Row #{0}: {1} {2} must be submitted”.format(row.idx, translated self.payment\_order\_type, reference\_name)).
- If (reference.company and reference.company differs from self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference.company → reference.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Row #{0}: {1} {2} belongs to Company {3}, not {4}”.format(row.idx, translated self.payment\_order\_type, reference\_name, reference.company, …)).
- If reference.status equals “Paid”.
  - Call the validation error handler Platform.throw(translated “Row #{0}: {1} {2} is already paid”.format(row.idx, translated self.payment\_order\_type, reference\_name)).
- If (self.docstatus equals 1 and reference.order\_status equals “Payment Ordered”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → reference.order\_status equals “Payment Ordered”.
  - Call the validation error handler Platform.throw(translated “Row #{0}: {1} {2} is already in another Payment Order”.format(row.idx, translated self.payment\_order\_type, reference\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L844)

<a id="op-7f588fe1ed6e32"></a>
### Payment Order.validate references not in other orders

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_validate_references_not_in_other_orders`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} {1} is already in Payment Order {2}”.format(translated self.payment\_order\_type, other\_order at 0 at 0, other\_order at 0 at 1).

**Local steps**

- Set references from self.get\_reference\_names().
- If (not self.payment\_order\_type or not references).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.payment\_order\_type → not references.
  - Return no value.
- Set order from Platform.qb.DocType(“Payment Order”).
- Set order\_reference from Platform.qb.DocType(“Payment Order Reference”).
- Set reference\_column from order\_reference at self.reference\_field.
- Set other\_order from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(references)).limit(1).run().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
- If other\_order.
  - Call the validation error handler Platform.throw(translated “{0} {1} is already in Payment Order {2}”.format(translated self.payment\_order\_type, other\_order at 0 at 0, other\_order at 0 at 1)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reference names](operations-069.md#op-16feaf83d8d886).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L846)

<a id="op-cf49be196d0dca"></a>
### Payment Order.validate company bank account

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_validate_company_bank_account`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Bank Account {0} is missing or disabled”.format(self.company\_bank\_account) · validation helper — translated “Bank Account {0} must be a company account belonging to {1}”.format(self.company\_bank\_account, self.company).

**Local steps**

- If not self.company\_bank\_account.
  - Return no value.
- Set bank\_account from Platform.get\_cached\_value(“Bank Account”, self.company\_bank\_account, list(“is\_company\_account”, “company”, “disabled”, “bank”, …), as\_dict = true).
- If (not bank\_account or bank\_account.disabled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_account → bank\_account.disabled.
  - Call the validation error handler Platform.throw(translated “Bank Account {0} is missing or disabled”.format(self.company\_bank\_account)).
- If (not bank\_account.is\_company\_account or bank\_account.company differs from self.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_account.is\_company\_account → bank\_account.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Bank Account {0} must be a company account belonging to {1}”.format(self.company\_bank\_account, self.company)).
- Set self.company\_bank from bank\_account.bank.
- Set self.account from bank\_account.account.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Bank Account”, self.company\_bank\_account, list(“is\_company\_account”, “company”, “disabled”, “bank”, …), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L843)

<a id="op-8c3e165133f2f8"></a>
### Payment Order.on submit

`operation_enterprise_accounts_record_definitions_payment_order_business_behavior_payment_order_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_payment\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update payment status](operations-069.md#op-06ea201482330a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L3058) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L228)

<a id="op-dd47045c7eb411"></a>
### Payment Order.on cancel

`operation_enterprise_accounts_record_definitions_payment_order_business_behavior_payment_order_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_payment\_status(cancel = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update payment status](operations-069.md#op-06ea201482330a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L3109) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L227)

<a id="op-06ea201482330a"></a>
### Payment Order.update payment status

`operation_enterprise_accounts_record_definitions_payment_order_business_behavior_payment_order_update_payment_status`

**Inputs** self, cancel = false.

**State and service calls** request set\_value on self.payment\_order\_type.

**Explicit results** no value.

**Local steps**

- If self.payment\_order\_type equals “Payment Request”.
  - If cancel.
    - Evaluate self.reset\_payment\_request\_status().
  - Otherwise.
    - Evaluate set\_payment\_requests\_as\_ordered(self.get\_reference\_names()).
  - Return no value.
- Set status from “Initiated” when cancel, otherwise “Payment Ordered”.
  - Value choice on cancel — true gives “Initiated”, false gives “Payment Ordered”.
- For each d in self.references.
  - Evaluate Platform.db.set\_value(self.payment\_order\_type, d.reference\_name, “payment\_order\_status”, status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset payment request status](operations-069.md#op-a42fe0fdeb3347), [get reference names](operations-069.md#op-16feaf83d8d886).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L229)

<a id="op-a42fe0fdeb3347"></a>
### Payment Order.reset payment request status

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_paymentorder_reset_payment_request_status`

**Inputs** self.

**State and service calls** request bulk\_update on “Payment Request”.

**Local steps**

- Set precision from Platform.get\_precision(“Payment Request”, “outstanding\_amount”).
- Set payment\_requests from get\_payment\_requests\_with\_total\_requested(self.get\_reference\_names()).
- Set status\_updates from mapping of payment\_request.name → mapping(“status” → get\_payment\_request\_status(payment\_request, payment\_request.outstanding\_amount, payment\_request.total\_requested, precision)) for payment\_request drawn f ….
  - Draw payment\_request from payment\_requests.
- Evaluate Platform.db.bulk\_update(“Payment Request”, status\_updates).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reference names](operations-069.md#op-16feaf83d8d886).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L841)

<a id="op-76af331c4f1a8c"></a>
### Set payment requests as ordered

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_set_payment_requests_as_ordered`

**Inputs** payment\_requests.

**State and service calls** request set\_value on “Payment Request”.

**Local steps**

- If payment\_requests.
  - Evaluate Platform.db.set\_value(“Payment Request”, mapping(“name” → list(“in”, payment\_requests)), “status”, “Payment Ordered”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L849)

<a id="op-b801c10d374cb9"></a>
### Readable payment order

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_readable_payment_order`

**Inputs** filters.

**Record and data access** read “Payment Order” via exists.

**Explicit results** no value · parent.

**Local steps**

- Set parent from filters.get(“parent”).
- If (not parent or not Platform.db.exists(“Payment Order”, parent)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → not Platform.db.exists(“Payment Order”, parent).
  - Return no value.
- Set ptype from “select” when Platform.only\_has\_select\_perm(“Payment Order”), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(“Payment Order”) — true gives “select”, false gives “read”.
- Evaluate Platform.has\_permission(“Payment Order”, ptype, doc = parent, throw = true).
- Return parent.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Payment Order”, ptype, doc = parent, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L847)

<a id="op-3f2dc163cde4ff"></a>
### Get mop query

`operation_enterprise_accounts_record_definitions_payment_order_business_behavior_get_mop_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Payment Order Reference” via get\_all.

**Explicit results** list() · Platform.get\_all(“Payment Order Reference”, filters = mapping(“parent” → filters.get(“parent”), “mode\_of\_payment” → list(“like”, formatted text %{txt}%)), fields = list(“mode\_of\_payment”), limit\_start = st ….

**Local steps**

- If not \_readable\_payment\_order(filters).
  - Return list().
- Return Platform.get\_all(“Payment Order Reference”, filters = mapping(“parent” → filters.get(“parent”), “mode\_of\_payment” → list(“like”, formatted text %{txt}%)), fields = list(“mode\_of\_payment”), limit\_start = st ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L223)

<a id="op-f9da9375759787"></a>
### Get supplier query

`operation_enterprise_accounts_record_definitions_payment_order_business_behavior_get_supplier_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Payment Order Reference” via get\_all.

**Explicit results** list() · Platform.get\_all(“Payment Order Reference”, filters = mapping(“parent” → filters.get(“parent”), “supplier” → list(“like”, formatted text %{txt}%), “payment\_reference” → list(“is”, “not set”)), fields = lis ….

**Local steps**

- If not \_readable\_payment\_order(filters).
  - Return list().
- Return Platform.get\_all(“Payment Order Reference”, filters = mapping(“parent” → filters.get(“parent”), “supplier” → list(“like”, formatted text %{txt}%), “payment\_reference” → list(“is”, “not set”)), fields = lis ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L224)

<a id="op-bf62920986f2e8"></a>
### Make payment records

`operation_enterprise_accounts_record_definitions_payment_order_business_behavior_make_payment_records`

**Inputs** name, supplier, mode\_of\_payment = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Payment Order” via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(“Payment Order”, name).
- Evaluate doc.check\_permission().
- Evaluate make\_journal\_entry(doc, supplier, mode\_of\_payment).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L226)
