# Accounting and settlement · operations 66

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment entry

[Record definition](../../../../data/record-types/payment_entry.json)

<a id="op-a2b3d9b29619ac"></a>
### Payment Entry.add tax gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_add_tax_gl_entries`

**Inputs** self, gl\_entries.

**Explicit failure paths** validation helper — translated “Currency for {0} must be {1}”.format(d.account\_head, self.company\_currency).

**Local steps**

- For each d in self.get(“taxes”).
  - Set account\_currency from get\_account\_currency(d.account\_head).
  - If account\_currency differs from self.company\_currency.
    - Call the validation error handler Platform.throw(translated “Currency for {0} must be {1}”.format(d.account\_head, self.company\_currency)).
  - If self.payment\_type belongs to tuple(“Pay”, “Internal Transfer”).
    - Set dr\_or\_cr from “debit” when d.add\_deduct\_tax equals “Add”, otherwise “credit”.
      - Value choice on d.add\_deduct\_tax equals “Add” — true gives “debit”, false gives “credit”.
    - Set rev\_dr\_or\_cr from “credit” when dr\_or\_cr equals “debit”, otherwise “debit”.
      - Value choice on dr\_or\_cr equals “debit” — true gives “credit”, false gives “debit”.
    - Set against from (self.party or self.paid\_from).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.party → self.paid\_from.
  - Otherwise.
    - If self.payment\_type equals “Receive”.
      - Set dr\_or\_cr from “credit” when d.add\_deduct\_tax equals “Add”, otherwise “debit”.
        - Value choice on d.add\_deduct\_tax equals “Add” — true gives “credit”, false gives “debit”.
      - Set rev\_dr\_or\_cr from “credit” when dr\_or\_cr equals “debit”, otherwise “debit”.
        - Value choice on dr\_or\_cr equals “debit” — true gives “credit”, false gives “debit”.
      - Set against from (self.party or self.paid\_to).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.party → self.paid\_to.
  - Set payment\_account from self.get\_party\_account\_for\_taxes().
  - Set tax\_amount from d.tax\_amount.
  - Set base\_tax\_amount from d.base\_tax\_amount.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → d.account\_head, “against” → against, dr\_or\_cr → tax\_amount, (dr\_or\_cr + “\_in\_account\_currency”) → base\_tax\_amount when account\_currency equals self.co ….
    - Value choice on account\_currency equals self.company\_currency — true gives base\_tax\_amount, false gives d.tax\_amount.
  - If not d.included\_in\_paid\_amount.
    - If get\_account\_currency(payment\_account) differs from self.company\_currency.
      - If self.payment\_type equals “Receive”.
        - Set exchange\_rate from self.target\_exchange\_rate.
      - Otherwise.
        - If self.payment\_type belongs to list(“Pay”, “Internal Transfer”).
          - Set exchange\_rate from self.source\_exchange\_rate.
      - Set base\_tax\_amount from flt((tax\_amount ÷ exchange\_rate), self.precision(“paid\_amount”)).
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → payment\_account, “against” → against, rev\_dr\_or\_cr → tax\_amount, (rev\_dr\_or\_cr + “\_in\_account\_currency”) → base\_tax\_amount when account\_currency equal ….
      - Value choice on account\_currency equals self.company\_currency — true gives base\_tax\_amount, false gives d.tax\_amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party account for taxes](operations-066.md#op-ad1a41ab5d38d1).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L830)

<a id="op-6d60f02cfb1947"></a>
### Payment Entry.add deductions gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_add_deductions_gl_entries`

**Inputs** self, gl\_entries.

**Explicit failure paths** validation helper — translated “Currency for {0} must be {1}”.format(d.account, self.company\_currency).

**Local steps**

- For each d in self.get(“deductions”).
  - If not d.amount.
    - Continue with the next iteration or loop test.
  - Set account\_currency from get\_account\_currency(d.account).
  - If account\_currency differs from self.company\_currency.
    - Call the validation error handler Platform.throw(translated “Currency for {0} must be {1}”.format(d.account, self.company\_currency)).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → d.account, “account\_currency” → account\_currency, “against” → (self.party or self.paid\_from), “debit\_in\_account\_currency” → d.amount, …), item = d)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.party → self.paid\_from.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L828)

<a id="op-ad1a41ab5d38d1"></a>
### Payment Entry.get party account for taxes

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_party_account_for_taxes`

**Inputs** self.

**Explicit results** self.paid\_to · self.paid\_from.

**Local steps**

- If self.payment\_type equals “Receive”.
  - Return self.paid\_to.
- Otherwise.
  - <a id="op-ad1a41ab5d38d1-guard-4"></a>If self.payment\_type belongs to tuple(“Pay”, “Internal Transfer”).
    - Return self.paid\_from.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.payment\_type belongs to tuple(“Pay”, “Internal Transfer”), self.payment\_type = “Pay” selects the branch that returns self.paid\_from. With self.payment\_type = “Receive”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ad1a41ab5d38d1-guard-4)

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L4403) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L63)

<a id="op-b8fa5a8c843815"></a>
### Payment Entry.get value in transaction currency

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_value_in_transaction_currency`

**Inputs** self, account\_currency, gl\_dict, field.

**Explicit results** flt((gl\_dict.get(field, 0) ÷ (conversion\_rate or 1))).

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(self.company).
- Set conversion\_rate from self.target\_exchange\_rate.
- If self.paid\_from\_account\_currency differs from company\_currency.
  - Set conversion\_rate from self.source\_exchange\_rate.
- Return flt((gl\_dict.get(field, 0) ÷ (conversion\_rate or 1))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conversion\_rate → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L4517) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L65)

<a id="op-8d4980bdcaf11a"></a>
### Payment Entry.on recurring

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_on_recurring`

**Inputs** self, reference\_doc, auto\_repeat\_doc.

**Local steps**

- Set self.reference\_no from reference\_doc.name.
- Set self.reference\_date from nowdate().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L4722) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L71)

<a id="op-b76ea248c4ef17"></a>
### Payment Entry.calculate deductions

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_calculate_deductions`

**Inputs** self, tax\_details.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** mapping(“account” → tax\_details at “tax” at “account\_head”, “cost\_center” → Platform.get\_cached\_value(“Company”, self.company, “cost\_center”), “amount” → (self.total\_allocated\_amount × (tax\_details at “tax ….

**Local steps**

- Return mapping(“account” → tax\_details at “tax” at “account\_head”, “cost\_center” → Platform.get\_cached\_value(“Company”, self.company, “cost\_center”), “amount” → (self.total\_allocated\_amount × (tax\_details at “tax ….

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L4816) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L52)

<a id="op-cd35802de0ba5b"></a>
### Payment Entry.set gain or loss

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_gain_or_loss`

**Inputs** self, account\_details = no value.

**Explicit results** no value.

**Local steps**

- If not self.difference\_amount.
  - Evaluate self.set\_difference\_amount().
- Set row from mapping(“amount” → self.difference\_amount).
- If account\_details.
  - Evaluate row.update(account\_details).
- If not row.get(“amount”).
  - Return no value.
- Evaluate self.append(“deductions”, row).
- Evaluate self.set\_unallocated\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set difference amount](operations-065.md#op-7df750f9314ae0), [set unallocated amount](operations-065.md#op-63fd930372c0c1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L5006) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L81)

<a id="op-bb0cd956198c78"></a>
### Payment Entry.get exchange rate

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_exchange_rate`

**Inputs** self.

**Explicit results** self.source\_exchange\_rate when self.payment\_type equals “Receive”, otherwise self.target\_exchange\_rate.

**Local steps**

- Return self.source\_exchange\_rate when self.payment\_type equals “Receive”, otherwise self.target\_exchange\_rate.
  - Value choice on self.payment\_type equals “Receive” — true gives self.source\_exchange\_rate, false gives self.target\_exchange\_rate.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L5246) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L61)

<a id="op-072a4523789f03"></a>
### Payment Entry.initialize taxes

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_initialize_taxes`

**Inputs** self.

**Local steps**

- For each tax in self.get(“taxes”).
  - Evaluate validate\_taxes\_and\_charges(tax).
  - Evaluate validate\_inclusive\_tax(tax, self).
  - Set tax\_fields from list(“total”, “tax\_fraction\_for\_current\_item”, “grand\_total\_fraction\_for\_current\_item”).
  - If tax.charge\_type differs from “Actual”.
    - Evaluate tax\_fields.append(“tax\_amount”).
  - For each fieldname in tax\_fields.
    - Evaluate tax.set(fieldname, 0.0).
- Set self.paid\_amount\_after\_tax from self.base\_paid\_amount.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L5318) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L67)

<a id="op-7c532e0c95abfe"></a>
### Payment Entry.determine exclusive rate

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_determine_exclusive_rate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not any(generator of cint(tax.included\_in\_paid\_amount) for tax drawn from self.get(“taxes”)).
  - Draw tax from self.get(“taxes”).
  - Return no value.
- Set cumulated\_tax\_fraction from 0.
- For each tuple(i, tax) in enumerate(self.get(“taxes”)).
  - Set tax.tax\_fraction\_for\_current\_item from self.get\_current\_tax\_fraction(tax).
  - If i equals 0.
    - Set tax.grand\_total\_fraction\_for\_current\_item from (1 + tax.tax\_fraction\_for\_current\_item).
  - Otherwise.
    - Set tax.grand\_total\_fraction\_for\_current\_item from (self.get(“taxes”) at (i − 1).grand\_total\_fraction\_for\_current\_item + tax.tax\_fraction\_for\_current\_item).
  - Update cumulated\_tax\_fraction using + tax.tax\_fraction\_for\_current\_item.
- Set self.paid\_amount\_after\_tax from flt((self.base\_paid\_amount ÷ (1 + cumulated\_tax\_fraction))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current tax fraction](operations-066.md#op-07ea8f85927487).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L5580) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L56)

<a id="op-11f0f198901561"></a>
### Payment Entry.calculate taxes

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_calculate_taxes`

**Inputs** self.

**Local steps**

- Set self.total\_taxes\_and\_charges from 0.0.
- Set self.base\_total\_taxes\_and\_charges from 0.0.
- Set actual\_tax\_dict from dict(list of list(tax.idx, flt(tax.tax\_amount, tax.precision(“tax\_amount”))) for tax drawn from self.get(“taxes”) where tax.charge\_type equals “Actual”).
  - Draw tax from self.get(“taxes”), keep a combination only if (tax.charge\_type equals “Actual”).
- For each tuple(i, tax) in enumerate(self.get(“taxes”)).
  - Set current\_tax\_amount from self.get\_current\_tax\_amount(tax).
  - If tax.charge\_type equals “Actual”.
    - Update actual\_tax\_dict at tax.idx using − current\_tax\_amount.
    - If i equals (len(self.get(“taxes”)) − 1).
      - Update current\_tax\_amount using + actual\_tax\_dict at tax.idx.
  - Set tax.tax\_amount from current\_tax\_amount.
  - Set tax.base\_tax\_amount from current\_tax\_amount.
  - If tax.add\_deduct\_tax equals “Deduct”.
    - Update current\_tax\_amount using × negative 1.0.
  - Otherwise.
    - Update current\_tax\_amount using × 1.0.
  - If i equals 0.
    - Set tax.total from flt((self.paid\_amount\_after\_tax + current\_tax\_amount), self.precision(“total”, tax)).
  - Otherwise.
    - Set tax.total from flt((self.get(“taxes”) at (i − 1).total + current\_tax\_amount), self.precision(“total”, tax)).
  - Set tax.base\_total from tax.total.
  - If self.payment\_type equals “Pay”.
    - If tax.currency differs from self.paid\_to\_account\_currency.
      - Update self.total\_taxes\_and\_charges using + flt((current\_tax\_amount ÷ self.target\_exchange\_rate)).
    - Otherwise.
      - Update self.total\_taxes\_and\_charges using + current\_tax\_amount.
  - Otherwise.
    - If self.payment\_type equals “Receive”.
      - If tax.currency differs from self.paid\_from\_account\_currency.
        - Update self.total\_taxes\_and\_charges using + flt((current\_tax\_amount ÷ self.source\_exchange\_rate)).
      - Otherwise.
        - Update self.total\_taxes\_and\_charges using + current\_tax\_amount.
  - Update self.base\_total\_taxes\_and\_charges using + current\_tax\_amount.
- If self.get(“taxes”).
  - Set self.paid\_amount\_after\_tax from self.get(“taxes”) at negative 1.base\_total.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current tax amount](operations-066.md#op-d8f2205ab378cf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L5990) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L53)

<a id="op-d8f2205ab378cf"></a>
### Payment Entry.get current tax amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_current_tax_amount`

**Inputs** self, tax.

**Explicit results** current\_tax\_amount.

**Explicit failure paths** validation helper — translated “Cannot select charge type as 'On Previous Row Amount' or 'On Previous Row Total' for first row”.

**Local steps**

- Set tax\_rate from tax.rate.
- If tax.charge\_type belongs to list(“On Previous Row Amount”, “On Previous Row Total”).
  - If tax.idx equals 1.
    - Call the validation error handler Platform.throw(translated “Cannot select charge type as 'On Previous Row Amount' or 'On Previous Row Total' for first row”).
  - If not tax.row\_id.
    - Set tax.row\_id from (tax.idx − 1).
- If tax.charge\_type equals “Actual”.
  - Set current\_tax\_amount from flt(tax.tax\_amount, self.precision(“tax\_amount”, tax)).
- Otherwise.
  - If tax.charge\_type equals “On Paid Amount”.
    - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × self.paid\_amount\_after\_tax).
  - Otherwise.
    - If tax.charge\_type equals “On Previous Row Amount”.
      - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × self.get(“taxes”) at (cint(tax.row\_id) − 1).tax\_amount).
    - Otherwise.
      - If tax.charge\_type equals “On Previous Row Total”.
        - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × self.get(“taxes”) at (cint(tax.row\_id) − 1).total).
- Return current\_tax\_amount.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L7050) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L58)

<a id="op-07ea8f85927487"></a>
### Payment Entry.get current tax fraction

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_current_tax_fraction`

**Inputs** self, tax.

**Explicit results** current\_tax\_fraction.

**Local steps**

- Set current\_tax\_fraction from 0.
- If cint(tax.included\_in\_paid\_amount).
  - Set tax\_rate from tax.rate.
  - If tax.charge\_type equals “On Paid Amount”.
    - Set current\_tax\_fraction from (tax\_rate ÷ 100.0).
  - Otherwise.
    - If tax.charge\_type equals “On Previous Row Amount”.
      - Set current\_tax\_fraction from ((tax\_rate ÷ 100.0) × self.get(“taxes”) at (cint(tax.row\_id) − 1).tax\_fraction\_for\_current\_item).
    - Otherwise.
      - If tax.charge\_type equals “On Previous Row Total”.
        - Set current\_tax\_fraction from ((tax\_rate ÷ 100.0) × self.get(“taxes”) at (cint(tax.row\_id) − 1).grand\_total\_fraction\_for\_current\_item).
- If (getattr(tax, “add\_deduct\_tax”, no value) and tax.add\_deduct\_tax equals “Deduct”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(tax, “add\_deduct\_tax”, no value) → tax.add\_deduct\_tax equals “Deduct”.
  - Update current\_tax\_fraction using × negative 1.0.
- Return current\_tax\_fraction.

**Values supplied outside this operation** selected callable from getattr(tax, “add\_deduct\_tax”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L59)

<a id="op-5149f268b78cf5"></a>
### Payment Entry.set matched unset payment requests to response

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_matched_unset_payment_remote_requests_to_response`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.references.
  - Return no value.
- Set matched\_payment\_requests from get\_matched\_payment\_request\_of\_references(list of row for row drawn from self.references where not row.payment\_request).
  - Draw row from self.references, keep a combination only if (not row.payment\_request).
- If not matched\_payment\_requests.
  - Return no value.
- Set Platform.response at “matched\_payment\_requests” from matched\_payment\_requests.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L458) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L84)

<a id="op-0c10a98b46d887"></a>
### Payment Entry.allocate amount to references

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_allocate_amount_to_references`

**Inputs** self, paid\_amount, paid\_amount\_change, allocate\_payment\_amount.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Cannot {0} from {1} without any negative outstanding invoice”.format(self.payment\_type, self.party\_type) · msgprint with translated “Paid Amount cannot be greater than total negative outstanding amount {0}”.format(total\_negative\_outstanding).

**Explicit results** no value.

**Local steps**

- If not self.references.
  - Return no value.
- If not allocate\_payment\_amount.
  - For each ref in self.references.
    - Set ref.allocated\_amount from 0.
  - Return no value.
- Set precision from self.precision(“paid\_amount”).
- Set total\_positive\_outstanding\_including\_order from 0.
- Set total\_negative\_outstanding from 0.
- Update paid\_amount using − sum(generator of flt(d.amount, precision) for d drawn from self.deductions).
  - Draw d from self.deductions.
- For each ref in self.references.
  - Set reference\_outstanding\_amount from flt(ref.outstanding\_amount).
  - Set abs\_outstanding\_amount from abs(reference\_outstanding\_amount).
  - If reference\_outstanding\_amount &gt; 0.
    - Update total\_positive\_outstanding\_including\_order using + abs\_outstanding\_amount.
  - Otherwise.
    - Update total\_negative\_outstanding using + abs\_outstanding\_amount.
- Set allocated\_negative\_outstanding from 0.
- Set allocated\_positive\_outstanding from 0.
- If ((self.payment\_type equals “Receive” and self.party\_type equals “Customer”) or (self.payment\_type equals “Pay” and self.party\_type belongs to tuple(“Supplier”, “Employee”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.payment\_type equals “Receive” and self.party\_type equals “Customer”) → (self.payment\_type equals “Pay” and self.party\_type belongs to tuple(“Supplier”, “Employee”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_type equals “Receive” → self.party\_type equals “Customer”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_type equals “Pay” → self.party\_type belongs to tuple(“Supplier”, “Employee”).
  - If total\_positive\_outstanding\_including\_order &gt; paid\_amount.
    - Set remaining\_outstanding from flt((total\_positive\_outstanding\_including\_order − paid\_amount), precision).
    - Set allocated\_negative\_outstanding from min(remaining\_outstanding, total\_negative\_outstanding).
  - Set allocated\_positive\_outstanding from (paid\_amount + allocated\_negative\_outstanding).
- Otherwise.
  - If self.party\_type belongs to tuple(“Supplier”, “Customer”).
    - If paid\_amount &gt; total\_negative\_outstanding.
      - <a id="op-0c10a98b46d887-guard-49"></a>If total\_negative\_outstanding equals 0.
        - Evaluate Platform.msgprint(translated “Cannot {0} from {1} without any negative outstanding invoice”.format(self.payment\_type, self.party\_type)).
      - Otherwise.
        - Evaluate Platform.msgprint(translated “Paid Amount cannot be greater than total negative outstanding amount {0}”.format(total\_negative\_outstanding)).
      - Return no value.
    - Otherwise.
      - Set allocated\_positive\_outstanding from flt((total\_negative\_outstanding − paid\_amount), precision).
      - Set allocated\_negative\_outstanding from (paid\_amount + min(total\_positive\_outstanding\_including\_order, allocated\_positive\_outstanding)).
- Bind local operation \_allocation\_to\_unset\_pr\_row for subsequent calls.
- If not paid\_amount\_change.
  - For each ref in self.references.
    - Set tuple(allocated\_positive\_outstanding, allocated\_negative\_outstanding) from \_allocation\_to\_unset\_pr\_row(ref, ref.outstanding\_amount, allocated\_positive\_outstanding, allocated\_negative\_outstanding).
  - Evaluate allocate\_open\_payment\_requests\_to\_references(self.references, self.precision(“paid\_amount”)).
- Otherwise.
  - Set payment\_request\_outstanding\_amounts from (get\_payment\_request\_outstanding\_set\_in\_references(self.references) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_payment\_request\_outstanding\_set\_in\_references(self.references) → mapping().
  - Set references\_outstanding\_amounts from (get\_references\_outstanding\_amount(self.references) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_references\_outstanding\_amount(self.references) → mapping().
  - Set remaining\_references\_allocated\_amounts from references\_outstanding\_amounts.copy().
  - For each ref in self.references.
    - If not (ref.reference\_doctype and ref.reference\_name and ref.payment\_request).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref.reference\_doctype → ref.reference\_name → ref.payment\_request.
      - Continue with the next iteration or loop test.
    - Set key from tuple(ref.reference\_doctype, ref.reference\_name, ref.get(“payment\_term”)).
    - Set reference\_outstanding\_amount from references\_outstanding\_amounts at key.
    - Set pr\_outstanding\_amount from payment\_request\_outstanding\_amounts at ref.payment\_request.
    - If (reference\_outstanding\_amount &gt; 0 and allocated\_positive\_outstanding ≥ 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_outstanding\_amount &gt; 0 → allocated\_positive\_outstanding ≥ 0.
      - Set outstanding\_amounts from tuple(allocated\_positive\_outstanding, reference\_outstanding\_amount, pr\_outstanding\_amount).
      - Set ref.allocated\_amount from min(outstanding\_amounts).
      - Set allocated\_amount from ref.allocated\_amount.
      - Set allocated\_positive\_outstanding from flt((allocated\_positive\_outstanding − allocated\_amount), precision).
      - Set remaining\_references\_allocated\_amounts at key from flt((remaining\_references\_allocated\_amounts at key − allocated\_amount), precision).
      - Set payment\_request\_outstanding\_amounts at ref.payment\_request from flt((payment\_request\_outstanding\_amounts at ref.payment\_request − allocated\_amount), precision).
    - Otherwise.
      - If (reference\_outstanding\_amount &lt; 0 and allocated\_negative\_outstanding).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_outstanding\_amount &lt; 0 → allocated\_negative\_outstanding.
        - Set outstanding\_amounts from tuple(allocated\_negative\_outstanding, abs(reference\_outstanding\_amount), pr\_outstanding\_amount).
        - Set ref.allocated\_amount from (min(outstanding\_amounts) × negative 1).
        - Set allocated\_amount from abs(ref.allocated\_amount).
        - Set allocated\_negative\_outstanding from flt((allocated\_negative\_outstanding − allocated\_amount), precision).
        - Update remaining\_references\_allocated\_amounts at key using + allocated\_amount.
        - Set payment\_request\_outstanding\_amounts at ref.payment\_request from flt((payment\_request\_outstanding\_amounts at ref.payment\_request − allocated\_amount), precision).
  - For each ref in self.references.
    - If (ref.payment\_request or not (ref.reference\_doctype and ref.reference\_name)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref.payment\_request → not (ref.reference\_doctype and ref.reference\_name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref.reference\_doctype → ref.reference\_name.
      - Continue with the next iteration or loop test.
    - Set key from tuple(ref.reference\_doctype, ref.reference\_name, ref.get(“payment\_term”)).
    - Set reference\_outstanding\_amount from remaining\_references\_allocated\_amounts at key.
    - Set tuple(allocated\_positive\_outstanding, allocated\_negative\_outstanding) from \_allocation\_to\_unset\_pr\_row(ref, reference\_outstanding\_amount, allocated\_positive\_outstanding, allocated\_negative\_outstanding).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison total\_negative\_outstanding equals 0, total\_negative\_outstanding = 0 selects the branch that requests a message with translated “Cannot {0} from {1} without any negative outstanding invoice”.format(self.payment\_type, self.party\_type). With total\_negative\_outstanding = 1, the alternative requests a message with translated “Paid Amount cannot be greater than total negative outstanding amount {0}”.format(total\_negative\_outstanding). [Local guard](#op-0c10a98b46d887-guard-49)

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L46)

<a id="op-63a517c3ee03cc"></a>
### Payment Entry.allocate amount to references.allocation to unset pr row

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_allocate_amount_to_references_allocation_to_unset_purchase_receipt_row`

**Inputs** row, outstanding\_amount, allocated\_positive\_outstanding, allocated\_negative\_outstanding.

**Explicit results** tuple(allocated\_positive\_outstanding, allocated\_negative\_outstanding).

**Local steps**

- If (outstanding\_amount &gt; 0 and allocated\_positive\_outstanding ≥ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in outstanding\_amount &gt; 0 → allocated\_positive\_outstanding ≥ 0.
  - Set row.allocated\_amount from min(allocated\_positive\_outstanding, outstanding\_amount).
  - Set allocated\_positive\_outstanding from flt((allocated\_positive\_outstanding − row.allocated\_amount), precision).
- Otherwise.
  - If (outstanding\_amount &lt; 0 and allocated\_negative\_outstanding).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in outstanding\_amount &lt; 0 → allocated\_negative\_outstanding.
    - Set row.allocated\_amount from (min(allocated\_negative\_outstanding, abs(outstanding\_amount)) × negative 1).
    - Set allocated\_negative\_outstanding from flt((allocated\_negative\_outstanding − abs(row.allocated\_amount)), precision).
- Return tuple(allocated\_positive\_outstanding, allocated\_negative\_outstanding).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L2991) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L47)

<a id="op-a215d1ce796113"></a>
### Payment Entry.set matched payment requests

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_matched_payment_remote_requests`

**Inputs** self, matched\_payment\_requests.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- If (not self.references or not matched\_payment\_requests).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.references → not matched\_payment\_requests.
  - Return no value.
- If isinstance(matched\_payment\_requests, str).
  - Set matched\_payment\_requests from json.loads(matched\_payment\_requests).
- Set payment\_requests from mapping().
- For each row in matched\_payment\_requests.
  - Set key from tuple(row at slice no value to 3).
  - Set payment\_requests at key from row at 3.
- For each ref in self.references.
  - If ref.payment\_request.
    - Continue with the next iteration or loop test.
  - Set key from tuple(ref.reference\_doctype, ref.reference\_name, ref.allocated\_amount).
  - If key belongs to payment\_requests.
    - Set ref.payment\_request from payment\_requests at key.
    - Remove payment\_requests at key.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L83)

<a id="op-c8bf6c5858bbd2"></a>
### Get matched payment request of references

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_matched_payment_request_of_references`

**Inputs** references = no value.

**Explicit results** no value · matched\_prs when matched\_prs, otherwise no value.

**Local steps**

- If not references.
  - Return no value.
- Set refs from set of tuple(row.reference\_doctype, row.reference\_name, row.allocated\_amount) for row drawn from references where (row.reference\_doctype and row.reference\_name and row.allocated\_amount).
  - Draw row from references, keep a combination only if ((row.reference\_doctype and row.reference\_name and row.allocated\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_doctype → row.reference\_name → row.allocated\_amount.
- If not refs.
  - Return no value.
- Set PR from Platform.qb.DocType(“Payment Request”).
- Set subquery from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.status differs from “Paid”).where(PR.docstatus equals 1).groupby(PR.reference\_doctype, PR.reference\_name, ….
- Set matched\_prs from nested operand in the contract(nested operand in the contract).select(subquery.reference\_doctype, subquery.reference\_name, subquery.allocated\_amount, subquery.payment\_request).where(subquery.count equals 1).run().
- Return matched\_prs when matched\_prs, otherwise no value.
  - Value choice on matched\_prs — true gives matched\_prs, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L25)

<a id="op-6688ececd2f72b"></a>
### Get references outstanding amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_references_outstanding_amount`

**Inputs** references = no value.

**Explicit results** no value · mapping(expand refs\_with\_payment\_term, expand refs\_without\_payment\_term).

**Local steps**

- If not references.
  - Return no value.
- Set refs\_with\_payment\_term from (get\_outstanding\_of\_references\_with\_payment\_term(references) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_outstanding\_of\_references\_with\_payment\_term(references) → mapping().
- Set refs\_without\_payment\_term from (get\_outstanding\_of\_references\_with\_no\_payment\_term(references) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_outstanding\_of\_references\_with\_no\_payment\_term(references) → mapping().
- Return mapping(expand refs\_with\_payment\_term, expand refs\_without\_payment\_term).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L4360) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L39)

<a id="op-0bbde2cd4ec870"></a>
### Get outstanding of references with payment term

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_outstanding_of_references_with_payment_term`

**Inputs** references = no value.

**Explicit results** no value · mapping of tuple(row.parenttype, row.parent, row.payment\_term) → row.outstanding for row drawn from response.

**Local steps**

- If not references.
  - Return no value.
- Set refs from set of tuple(row.reference\_doctype, row.reference\_name, row.payment\_term) for row drawn from references where (row.reference\_doctype and row.reference\_name and row.payment\_term).
  - Draw row from references, keep a combination only if ((row.reference\_doctype and row.reference\_name and row.payment\_term)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_doctype → row.reference\_name → row.payment\_term.
- If not refs.
  - Return no value.
- Set PS from Platform.qb.DocType(“Payment Schedule”).
- Set response from nested operand in the contract(nested operand in the contract).select(PS.parenttype, PS.parent, PS.payment\_term, PS.outstanding).where(Tuple(nested operand in the contract.parenttype, nested operand in the ….
- If not response.
  - Return no value.
- Return mapping of tuple(row.parenttype, row.parent, row.payment\_term) → row.outstanding for row drawn from response.
  - Draw row from response.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L4516) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L30)

<a id="op-c6699e6cde3144"></a>
### Get outstanding of references with no payment term

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_outstanding_of_references_with_number_payment_term`

**Inputs** references.

**Explicit results** no value · outstanding\_amounts.

**Local steps**

- If not references.
  - Return no value.
- Set outstanding\_amounts from mapping().
- For each ref in references.
  - If ref.payment\_term.
    - Continue with the next iteration or loop test.
  - Set key from tuple(ref.reference\_doctype, ref.reference\_name, no value).
  - If key does not belong to outstanding\_amounts.
    - Set outstanding\_amounts at key from ref.outstanding\_amount.
- Return outstanding\_amounts.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L4967) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L29)

<a id="op-25228c7f14c0cf"></a>
### Get payment request outstanding set in references

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_payment_request_outstanding_set_in_references`

**Inputs** references = no value.

**Explicit results** no value · dict(response) when response, otherwise no value.

**Local steps**

- If not references.
  - Return no value.
- Set referenced\_payment\_requests from set of row.payment\_request for row drawn from references where row.payment\_request.
  - Draw row from references, keep a combination only if (row.payment\_request).
- If not referenced\_payment\_requests.
  - Return no value.
- Set PR from Platform.qb.DocType(“Payment Request”).
- Set response from nested operand in the contract(nested operand in the contract).select(PR.name, PR.outstanding\_amount).where(PR.name.isin(referenced\_payment\_requests)).run().
- Return dict(response) when response, otherwise no value.
  - Value choice on response — true gives dict(response), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L5148) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L36)

<a id="op-78de15f30c8610"></a>
### Validate inclusive tax

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_validate_inclusive_tax`

**Inputs** tax, doc.

**Explicit failure paths** validation helper — translated “Valuation type charges can not be marked as Inclusive”.

**Local steps**

- Bind local operation \_on\_previous\_row\_error for subsequent calls.
- If cint(getattr(tax, “included\_in\_paid\_amount”, no value)).
  - If tax.charge\_type equals “Actual”.
    - Evaluate throw(translated “Charge of type 'Actual' in row {0} cannot be included in Item Rate or Paid Amount”.format(tax.idx)).
  - Otherwise.
    - If (tax.charge\_type equals “On Previous Row Amount” and not cint(nested operand in the contract.get(“taxes”) at (nested operand in the contract(nested operand in the contract) − 1).included\_in\_paid\_amount)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “On Previous Row Amount” → not cint(doc.get(“taxes”) at (cint(nested operand in the contract.row\_id) − 1).included\_in\_paid\_amount).
      - Evaluate \_on\_previous\_row\_error(tax.row\_id).
    - Otherwise.
      - If (tax.charge\_type equals “On Previous Row Total” and not all(list(cint(generator of nested operand in the contract.included\_in\_paid\_amount for t drawn from nested operand in the contract at nested operand i ….
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “On Previous Row Total” → not all(list(cint(generator of t.included\_in\_paid\_amount for t drawn from nested operand in the contract(nested operand in the contract) at slice no value to nested operand in the contract))).
        - Draw t from doc.get(“taxes”) at slice no value to (cint(tax.row\_id) − 1).
        - Evaluate \_on\_previous\_row\_error((“1 - %d” modulo or format tuple(cint(tax.row\_id)))).
      - Otherwise.
        - If tax.get(“category”) equals “Valuation”.
          - Call the validation error handler Platform.throw(translated “Valuation type charges can not be marked as Inclusive”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(tax, “included\_in\_paid\_amount”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L5445) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L131)

<a id="op-0079de7b4c8821"></a>
### Validate inclusive tax.on previous row error

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_validate_inclusive_tax_on_previous_row_error`

**Inputs** row\_range.

**Local steps**

- Evaluate throw(translated “To include tax in row {0} in Item rate, taxes in rows {1} must also be included”.format(tax.idx, row\_range)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0079.json#L6111) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L132)
