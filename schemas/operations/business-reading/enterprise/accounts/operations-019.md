# Accounting and settlement · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank transaction

[Record definition](../../../../data/record-types/bank_transaction.json)

<a id="op-277dc4e135c94f"></a>
### Bank Transaction.on discard

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L5017) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L463)

<a id="op-2b6cb9cc033454"></a>
### Bank Transaction.validate

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status().
- Evaluate self.validate\_included\_fee().
- Evaluate self.validate\_duplicate\_references().
- Evaluate self.validate\_currency().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-019.md#op-d9ab4eaca1772f), [validate included fee](operations-019.md#op-47347c05377b20), [validate duplicate references](operations-019.md#op-99022e0618faff), [validate currency](operations-019.md#op-47a0618bd2e9a8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L469)

<a id="op-47a0618bd2e9a8"></a>
### Bank Transaction.validate currency

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_validate_currency`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_cached\_value · read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Transaction currency: {0} cannot be different from Bank Account({1}) currency: {2}”.format(Platform.bold(self.currency), Platform.bold(self.bank\_account), Platform.bold(account\_currency)).

**Local steps**

- If (self.currency and self.bank\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency → self.bank\_account.
  - If account bound to Platform.get\_cached\_value(“Bank Account”, self.bank\_account, “account”).
    - Set account\_currency from Platform.get\_cached\_value(“Account”, account, “account\_currency”).
    - If self.currency differs from account\_currency.
      - Call the validation error handler Platform.throw(translated “Transaction currency: {0} cannot be different from Bank Account({1}) currency: {2}”.format(Platform.bold(self.currency), Platform.bold(self.bank\_account), Platform.bold(account\_currency))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Bank Account”, self.bank\_account, “account”), Platform.get\_cached\_value(“Account”, account, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L5171) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L470)

<a id="op-d9ab4eaca1772f"></a>
### Bank Transaction.set status

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_set_status`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If self.docstatus.is\_draft().
  - Set self.status from “Pending”.
- Otherwise.
  - If self.docstatus.is\_cancelled().
    - Evaluate self.db\_set(“status”, “Cancelled”).
  - Otherwise.
    - If self.unallocated\_amount &gt; 0.
      - Evaluate self.db\_set(“status”, “Unreconciled”).
    - Otherwise.
      - Evaluate self.db\_set(“status”, “Reconciled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L466)

<a id="op-99022e0618faff"></a>
### Bank Transaction.validate duplicate references

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_validate_duplicate_references`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} {1} is allocated twice in this Bank Transaction”.format(row.payment\_document, row.payment\_entry).

**Local steps**

- If not self.payment\_entries.
  - Return no value.
- Set references from set().
- For each row in self.payment\_entries.
  - Set reference from tuple(row.payment\_document, row.payment\_entry).
  - If reference belongs to references.
    - Call the validation error handler Platform.throw(translated “{0} {1} is allocated twice in this Bank Transaction”.format(row.payment\_document, row.payment\_entry)).
  - Evaluate references.add(reference).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L5712) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L471)

<a id="op-a717d4756822c0"></a>
### Bank Transaction.update allocated amount

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_update_allocated_amount`

**Inputs** self.

**Local steps**

- Set allocated\_amount from sum(generator of p.allocated\_amount for p drawn from self.payment\_entries) when self.payment\_entries, otherwise 0.0.
  - Value choice on self.payment\_entries — true gives sum(generator of p.allocated\_amount for p drawn from self.payment\_entries), false gives 0.0.
  - Draw p from self.payment\_entries.
- Set unallocated\_amount from (abs((flt(self.withdrawal) − flt(self.deposit))) − allocated\_amount).
- Set self.allocated\_amount from flt(allocated\_amount, self.precision(“allocated\_amount”)).
- Set self.unallocated\_amount from flt(unallocated\_amount, self.precision(“unallocated\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L5949) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L467)

<a id="op-9cdd1b3031d95d"></a>
### Bank Transaction.delink old payment entries

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_delink_old_payment_entries`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.updating\_linked\_bank\_transaction.
  - Return no value.
- Set old\_doc from self.get\_doc\_before\_save().
- Set payment\_entry\_names from set(generator of pe.name for pe drawn from self.payment\_entries).
  - Draw pe from self.payment\_entries.
- For each old\_pe in old\_doc.payment\_entries.
  - If old\_pe.name belongs to payment\_entry\_names.
    - Continue with the next iteration or loop test.
  - Evaluate self.delink\_payment\_entry(old\_pe).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delink payment entry](operations-019.md#op-9e46891b816879).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L6223) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L459)

<a id="op-0b7c60447fe5b7"></a>
### Bank Transaction.before submit

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_before_submit`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Evaluate self.allocate\_payment\_entries().
- Evaluate self.set\_status().
- If Platform.get\_single\_value(“Accounts Settings”, “enable\_party\_matching”).
  - Evaluate self.auto\_set\_party().

If control reaches the end, it returns no value.

**Methods declared on this owner** [allocate payment entries](operations-019.md#op-9f0ce660610f4c), [set status](operations-019.md#op-d9ab4eaca1772f), [auto set party](operations-019.md#op-f65c51975be97c).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “enable\_party\_matching”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L6431) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L455)

<a id="op-b76e2ee35de677"></a>
### Bank Transaction.before update after submit

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_references().
- Evaluate self.update\_allocated\_amount().
- Evaluate self.delink\_old\_payment\_entries().
- Evaluate self.allocate\_payment\_entries().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate references](operations-019.md#op-99022e0618faff), [update allocated amount](operations-019.md#op-a717d4756822c0), [delink old payment entries](operations-019.md#op-9cdd1b3031d95d), [allocate payment entries](operations-019.md#op-9f0ce660610f4c), [set status](operations-019.md#op-d9ab4eaca1772f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L6563) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L456)

<a id="op-99be78bb569e59"></a>
### Bank Transaction.on cancel

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from list(“GL Entry”).
- For each payment\_entry in self.payment\_entries.
  - Evaluate self.delink\_payment\_entry(payment\_entry).
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delink payment entry](operations-019.md#op-9e46891b816879), [set status](operations-019.md#op-d9ab4eaca1772f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L6694) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L462)

<a id="op-145f724cc8aebc"></a>
### Bank Transaction.add payment entries

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_add_payment_entries`

**Inputs** self, vouchers, is\_new\_voucher = false.

**Explicit failure paths** validation helper — translated “Bank Transaction {0} is already fully reconciled”.format(self.name).

**Local steps**

- If 0.0 ≥ self.unallocated\_amount.
  - Call the validation error handler Platform.throw(translated “Bank Transaction {0} is already fully reconciled”.format(self.name)).
- For each voucher in vouchers.
  - Evaluate self.append(“payment\_entries”, mapping(“payment\_document” → voucher at “payment\_doctype”, “payment\_entry” → voucher at “payment\_name”, “allocated\_amount” → 0.0, “reconciliation\_type” → “Voucher Created” wh ….
    - Value choice on is\_new\_voucher — true gives “Voucher Created”, false gives “Matched”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L6816) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L452)

<a id="op-9f0ce660610f4c"></a>
### Bank Transaction.allocate payment entries

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_allocate_payment_entries`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Voucher {0} is over-allocated by {1}”.format(allocable\_amount).

**Local steps**

- If (self.flags.updating\_linked\_bank\_transaction or not self.payment\_entries).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.updating\_linked\_bank\_transaction → not self.payment\_entries.
  - Return no value.
- Set remaining\_amount from self.unallocated\_amount.
- Set payment\_entry\_docs from list of tuple(pe.payment\_document, pe.payment\_entry) for pe drawn from self.payment\_entries.
  - Draw pe from self.payment\_entries.
- Set pe\_bt\_allocations from get\_total\_allocated\_amount(payment\_entry\_docs).
- Set gl\_entries from get\_related\_bank\_gl\_entries(payment\_entry\_docs).
- Set gl\_bank\_account from Platform.db.get\_value(“Bank Account”, self.bank\_account, “account”).
- For each payment\_entry in list(self.payment\_entries).
  - <a id="op-9f0ce660610f4c-guard-25"></a>If payment\_entry.allocated\_amount differs from 0.
    - Continue with the next iteration or loop test.
  - Set tuple(allocable\_amount, should\_clear, clearance\_date) from get\_clearance\_details(self, payment\_entry, (pe\_bt\_allocations.get(tuple(payment\_entry.payment\_document, payment\_entry.payment\_entry)) or mapping()), (gl\_entries.get(tuple(payment\_entry.payment\_document, pa ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pe\_bt\_allocations.get(tuple(payment\_entry.payment\_document, payment\_entry.payment\_entry)) → mapping().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in gl\_entries.get(tuple(payment\_entry.payment\_document, payment\_entry.payment\_entry)) → mapping().
  - <a id="op-9f0ce660610f4c-guard-36"></a>If allocable\_amount &lt; 0.
    - Call the validation error handler Platform.throw(translated “Voucher {0} is over-allocated by {1}”.format(allocable\_amount)).
  - If remaining\_amount ≤ 0.
    - Evaluate self.remove(payment\_entry).
    - Continue with the next iteration or loop test.
  - If allocable\_amount equals 0.
    - If should\_clear.
      - Evaluate self.clear\_linked\_payment\_entry(payment\_entry, clearance\_date = clearance\_date).
    - Evaluate self.remove(payment\_entry).
    - Continue with the next iteration or loop test.
  - Set should\_clear from (should\_clear and allocable\_amount ≤ remaining\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in should\_clear → allocable\_amount ≤ remaining\_amount.
  - Set payment\_entry.allocated\_amount from min(allocable\_amount, remaining\_amount).
  - Set remaining\_amount from flt((remaining\_amount − payment\_entry.allocated\_amount), self.precision(“unallocated\_amount”)).
  - If payment\_entry.payment\_document equals “Bank Transaction”.
    - Evaluate self.update\_linked\_bank\_transaction(payment\_entry.payment\_entry, payment\_entry.allocated\_amount).
  - Otherwise.
    - If should\_clear.
      - Evaluate self.clear\_linked\_payment\_entry(payment\_entry, clearance\_date = clearance\_date).
- Evaluate self.update\_allocated\_amount().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison payment\_entry.allocated\_amount differs from 0, payment\_entry.allocated\_amount = 1 selects the branch that continues with the next loop iteration. With payment\_entry.allocated\_amount = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9f0ce660610f4c-guard-25)
- At the comparison allocable\_amount &lt; 0, allocable\_amount = -1 selects the branch that calls the validation-error handler with translated “Voucher {0} is over-allocated by {1}”.format(allocable\_amount). With allocable\_amount = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9f0ce660610f4c-guard-36)

**Methods declared on this owner** [clear linked payment entry](operations-019.md#op-66a749fe075875), [update linked bank transaction](operations-019.md#op-d1310147c70bf4), [update allocated amount](operations-019.md#op-a717d4756822c0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L453)

<a id="op-6e632fb650e80c"></a>
### Bank Transaction.remove payment entries

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_remove_payment_entries`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Local steps**

- For each payment\_entry in self.payment\_entries.
  - Evaluate self.remove\_payment\_entry(payment\_entry).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove payment entry](operations-019.md#op-57f4ea619afbdf).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L942) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L484) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L464)

<a id="op-57f4ea619afbdf"></a>
### Bank Transaction.remove payment entry

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_remove_payment_entry`

**Inputs** self, payment\_entry.

**Local steps**

- Evaluate self.delink\_payment\_entry(payment\_entry).
- Evaluate self.remove(payment\_entry).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delink payment entry](operations-019.md#op-9e46891b816879).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L1054) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L485) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L465)

<a id="op-9e46891b816879"></a>
### Bank Transaction.delink payment entry

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_delink_payment_entry`

**Inputs** self, payment\_entry.

**Local steps**

- If payment\_entry.payment\_document equals “Bank Transaction”.
  - Evaluate self.update\_linked\_bank\_transaction(payment\_entry.payment\_entry, allocated\_amount = no value).
- Otherwise.
  - Evaluate self.clear\_linked\_payment\_entry(payment\_entry, clearance\_date = no value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update linked bank transaction](operations-019.md#op-d1310147c70bf4), [clear linked payment entry](operations-019.md#op-66a749fe075875).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L1141) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L460)

<a id="op-66a749fe075875"></a>
### Bank Transaction.clear linked payment entry

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_clear_linked_payment_entry`

**Inputs** self, payment\_entry, clearance\_date = no value.

**State and service calls** request set\_value on “Sales Invoice Payment” · request set\_value on doctype.

**Explicit results** no value.

**Local steps**

- Set doctype from payment\_entry.payment\_document.
- Set docname from payment\_entry.payment\_entry.
- If doctype does not belong to get\_doctypes\_for\_bank\_reconciliation().
  - Return no value.
- If doctype equals “Sales Invoice”.
  - Evaluate Platform.db.set\_value(“Sales Invoice Payment”, dict(parenttype = doctype, parent = docname), “clearance\_date”, clearance\_date).
  - Return no value.
- Evaluate Platform.db.set\_value(doctype, docname, “clearance\_date”, clearance\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L1285) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L458)

<a id="op-d1310147c70bf4"></a>
### Bank Transaction.update linked bank transaction

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_update_linked_bank_transaction`

**Inputs** self, bank\_transaction\_name, allocated\_amount = no value.

**Record and data access** resolve a document from self.doctype via get\_doc.

**State and service calls** call save on bt.

**Explicit results** no value.

**Local steps**

- Set bt from Platform.get\_doc(self.doctype, bank\_transaction\_name).
- If allocated\_amount.
  - Evaluate bt.append(“payment\_entries”, mapping(“payment\_document” → self.doctype, “payment\_entry” → self.name, “allocated\_amount” → allocated\_amount)).
- Otherwise.
  - Set pe from next(generator of pe for pe drawn from bt.payment\_entries where (pe.payment\_document equals self.doctype and pe.payment\_entry equals self.name), no value).
    - Draw pe from bt.payment\_entries, keep a combination only if ((pe.payment\_document equals self.doctype and pe.payment\_entry equals self.name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pe.payment\_document equals self.doctype → pe.payment\_entry equals self.name.
  - If not pe.
    - Return no value.
  - Set bt.flags.updating\_linked\_bank\_transaction from true.
  - Evaluate bt.remove(pe).
- Evaluate bt.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L1556) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L468)

<a id="op-f65c51975be97c"></a>
### Bank Transaction.auto set party

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_auto_set_party`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies AutoMatchParty.
- If (self.party\_type and self.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_type → self.party.
  - Return no value.
- Set result from no value.
- Attempt the following.
  - Set result from AutoMatchParty(bank\_party\_account\_number = self.bank\_party\_account\_number, bank\_party\_iban = self.bank\_party\_iban, bank\_party\_name = self.bank\_party\_name, description = self.description, …).match().
- On failure (Exception).
  - Evaluate Platform.log\_error(title = translated “Error in party matching for Bank Transaction {0}”.format(self.name)).
- If not result.
  - Return no value.
- Set tuple(self.party\_type, self.party) from result.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L1932) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L454)

<a id="op-47347c05377b20"></a>
### Bank Transaction.validate included fee

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_validate_included_fee`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Included fee is bigger than the withdrawal itself.”.

**Local steps**

- If (self.included\_fee and self.withdrawal).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.included\_fee → self.withdrawal.
  - If self.included\_fee &gt; self.withdrawal.
    - Call the validation error handler Platform.throw(translated “Included fee is bigger than the withdrawal itself.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L2253) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L472)

<a id="op-52de0923a27478"></a>
### Bank Transaction.handle excluded fee

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_handle_excluded_fee`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The Excluded Fee is bigger than the Deposit it is deducted from.” · validation helper — translated “Only one of Deposit or Withdrawal should be non-zero when applying an Excluded Fee.”.

**Local steps**

- Set excluded\_fee from flt(self.excluded\_fee).
- If excluded\_fee ≤ 0.
  - Return no value.
- If (flt(self.deposit) &gt; 0 and (flt(self.deposit) − excluded\_fee) &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.deposit) &gt; 0 → (flt(self.deposit) − excluded\_fee) &lt; 0.
  - Call the validation error handler Platform.throw(translated “The Excluded Fee is bigger than the Deposit it is deducted from.”).
- If (flt(self.deposit) &gt; 0 and flt(self.withdrawal) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.deposit) &gt; 0 → flt(self.withdrawal) &gt; 0.
  - Call the validation error handler Platform.throw(translated “Only one of Deposit or Withdrawal should be non-zero when applying an Excluded Fee.”).
- If flt(self.deposit) &gt; 0.
  - Set self.deposit from (flt(self.deposit) − excluded\_fee).
- Otherwise.
  - If flt(self.withdrawal) ≥ 0.
    - Set self.withdrawal from (flt(self.withdrawal) + excluded\_fee).
- Set self.included\_fee from (flt(self.included\_fee) + excluded\_fee).
- Set self.excluded\_fee from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L2381) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L461)

<a id="op-2c4e821a984ba2"></a>
### Get doctypes for bank reconciliation

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_get_record_types_for_bank_reconciliation`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.get\_hooks(“bank\_reconciliation\_doctypes”).

**Local steps**

- Return Platform.get\_hooks(“bank\_reconciliation\_doctypes”).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“bank\_reconciliation\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L2914) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L475)

<a id="op-af2003bfb81f1f"></a>
### Unreconcile transaction

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_unreconcile_transaction`

**Inputs** transaction\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Bank Transaction” via get\_doc · resolve a document from voucher at “doctype” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(voucher at “doctype”, voucher at “name”).

**Local steps**

- Set transaction from Platform.get\_doc(“Bank Transaction”, transaction\_name).
- Set vouchers\_to\_cancel from list().
- For each entry in transaction.payment\_entries.
  - If entry.reconciliation\_type equals “Voucher Created”.
    - Evaluate vouchers\_to\_cancel.append(mapping(“doctype” → entry.payment\_document, “name” → entry.payment\_entry)).
- Evaluate transaction.remove\_payment\_entries().
- For each voucher in vouchers\_to\_cancel.
  - Evaluate Platform.get\_doc(voucher at “doctype”, voucher at “name”).cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L479)

<a id="op-94d2d54f14ce7f"></a>
### Unreconcile transaction entry

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_unreconcile_transaction_entry`

**Inputs** bank\_transaction\_id, voucher\_type, voucher\_id.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Transaction” via get\_doc · resolve a document from voucher\_type via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(voucher\_type, voucher\_id) · call save on bank\_transaction.

**Explicit results** mapping(“success” → true).

**Local steps**

- Set bank\_transaction from Platform.get\_doc(“Bank Transaction”, bank\_transaction\_id).
- For each entry in bank\_transaction.payment\_entries.
  - If (entry.payment\_document equals voucher\_type and entry.payment\_entry equals voucher\_id).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.payment\_document equals voucher\_type → entry.payment\_entry equals voucher\_id.
    - If entry.reconciliation\_type equals “Voucher Created”.
      - Evaluate Platform.get\_doc(voucher\_type, voucher\_id).cancel().
    - Otherwise.
      - Evaluate bank\_transaction.remove\_payment\_entry(entry).
      - Evaluate bank\_transaction.save().
- Return mapping(“success” → true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L480)

<a id="op-2fded187ab1991"></a>
### Get clearance details

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_get_clearance_details`

**Inputs** transaction, payment\_entry, bt\_allocations, gl\_entries, gl\_bank\_account.

**Record and data access** read “Bank Transaction” via get\_value · read “Bank Account” via get\_value.

**Explicit results** tuple(abs(bt.unallocated\_amount), true, transaction\_date) · tuple(allocable\_amount, should\_clear, clearance\_date).

**Explicit failure paths** validation helper — translated “Bank Account {} in Bank Transaction {} is not matching with Bank Account {}”.format(bt\_bank\_account, payment\_entry.payment\_entry, gl\_bank\_account) · validation helper — translated “{} {} is not affecting bank account {}”.format(payment\_entry.payment\_document, payment\_entry.payment\_entry, gl\_bank\_account) · validation helper — translated “Invalid amount in accounting entries of {} {} for Account {}: {}”.format(payment\_entry.payment\_document, payment\_entry.payment\_entry, gl\_bank\_account, allocable\_amount).

**Local steps**

- Set transaction\_date from getdate(transaction.date).
- If payment\_entry.payment\_document equals “Bank Transaction”.
  - Set bt from Platform.db.get\_value(“Bank Transaction”, payment\_entry.payment\_entry, tuple(“unallocated\_amount”, “bank\_account”), as\_dict = true).
  - Set bt\_bank\_account from Platform.db.get\_value(“Bank Account”, bt.bank\_account, “account”).
  - If bt\_bank\_account differs from gl\_bank\_account.
    - Call the validation error handler Platform.throw(translated “Bank Account {} in Bank Transaction {} is not matching with Bank Account {}”.format(bt\_bank\_account, payment\_entry.payment\_entry, gl\_bank\_account)).
  - Return tuple(abs(bt.unallocated\_amount), true, transaction\_date).
- If gl\_bank\_account does not belong to gl\_entries.
  - Call the validation error handler Platform.throw(translated “{} {} is not affecting bank account {}”.format(payment\_entry.payment\_document, payment\_entry.payment\_entry, gl\_bank\_account)).
- Set allocable\_amount from (gl\_entries.pop(gl\_bank\_account) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gl\_entries.pop(gl\_bank\_account) → 0.
- <a id="op-2fded187ab1991-guard-38"></a>If allocable\_amount ≤ 0.0.
  - Call the validation error handler Platform.throw(translated “Invalid amount in accounting entries of {} {} for Account {}: {}”.format(payment\_entry.payment\_document, payment\_entry.payment\_entry, gl\_bank\_account, allocable\_amount)).
- Set matching\_bt\_allocaion from bt\_allocations.pop(gl\_bank\_account, mapping()).
- Set allocable\_amount from flt((allocable\_amount − matching\_bt\_allocaion.get(“total”, 0)), transaction.precision(“unallocated\_amount”)).
- Set should\_clear from all(generator of gl\_entries at gle\_account equals nested operand in the contract.get(gle\_account, mapping()).get(“total”, 0) for gle\_account drawn from gl\_entries).
  - Draw gle\_account from gl\_entries.
- Set bt\_allocation\_date from matching\_bt\_allocaion.get(“latest\_date”, no value).
- Set clearance\_date from transaction\_date when not bt\_allocation\_date, otherwise max(transaction\_date, bt\_allocation\_date).
  - Value choice on not bt\_allocation\_date — true gives transaction\_date, false gives max(transaction\_date, bt\_allocation\_date).
- Return tuple(allocable\_amount, should\_clear, clearance\_date).

**Derived branch illustrations**

- At the comparison allocable\_amount ≤ 0.0, allocable\_amount = 0 selects the branch that calls the validation-error handler with translated “Invalid amount in accounting entries of {} {} for Account {}: {}”.format(payment\_entry.payment\_document, payment\_entry.pa …. With allocable\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2fded187ab1991-guard-38)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L473)
