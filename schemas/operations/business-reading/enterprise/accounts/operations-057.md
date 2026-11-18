# Accounting and settlement · operations 57

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Journal entry

[Record definition](../../../../data/record-types/journal_entry.json)

<a id="op-851ea152e440cc"></a>
### Journal Entry.system generated gain loss

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_system_generated_gain_loss`

**Inputs** self.

**Explicit results** (self.voucher\_type equals “Exchange Gain Or Loss” and self.multi\_currency and self.is\_system\_generated).

**Local steps**

- Return (self.voucher\_type equals “Exchange Gain Or Loss” and self.multi\_currency and self.is\_system\_generated).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Exchange Gain Or Loss” → self.multi\_currency → self.is\_system\_generated.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L777) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1136)

<a id="op-f785f1746bc81a"></a>
### Journal Entry.validate against jv

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_against_journal_voucher`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value · execute query text (SELECT, Journal Entry Account).

**Explicit failure paths** validation helper — translated “Row #{0}: For {1}, you can select reference document only if account gets credited”.format(d.idx, d.account) · validation helper — translated “Row #{0}: For {1}, you can select reference document only if account gets debited”.format(d.idx, d.account) · validation helper — translated “You can not enter current voucher in 'Against Journal Entry' column” · validation helper — translated “Journal Entry {0} does not have account {1} or already matched against other voucher”.format(d.reference\_name, d.account) · validation helper — translated “Against Journal Entry {0} does not have any unmatched {1} entry”.format(d.reference\_name, dr\_or\_cr).

**Local steps**

- For each d in self.get(“accounts”).
  - If d.reference\_type equals “Journal Entry”.
    - Set account\_root\_type from Platform.get\_cached\_value(“Account”, d.account, “root\_type”).
    - If (account\_root\_type equals “Asset” and flt(d.debit) &gt; 0 and not self.system\_generated\_gain\_loss()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_root\_type equals “Asset” → flt(d.debit) &gt; 0 → not self.system\_generated\_gain\_loss().
      - Call the validation error handler Platform.throw(translated “Row #{0}: For {1}, you can select reference document only if account gets credited”.format(d.idx, d.account)).
    - Otherwise.
      - If (account\_root\_type equals “Liability” and flt(d.credit) &gt; 0 and not self.system\_generated\_gain\_loss()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_root\_type equals “Liability” → flt(d.credit) &gt; 0 → not self.system\_generated\_gain\_loss().
        - Call the validation error handler Platform.throw(translated “Row #{0}: For {1}, you can select reference document only if account gets debited”.format(d.idx, d.account)).
    - If d.reference\_name equals self.name.
      - Call the validation error handler Platform.throw(translated “You can not enter current voucher in 'Against Journal Entry' column”).
    - Set against\_entries from Platform.db.sql(query text (SELECT, Journal Entry Account), tuple(d.account, d.reference\_name), as\_dict = true).
    - If not against\_entries.
      - <a id="op-f785f1746bc81a-guard-39"></a>If self.voucher\_type differs from “Exchange Gain Or Loss”.
        - Call the validation error handler Platform.throw(translated “Journal Entry {0} does not have account {1} or already matched against other voucher”.format(d.reference\_name, d.account)).
    - Otherwise.
      - Set dr\_or\_cr from “debit” when flt(d.credit) &gt; 0, otherwise “credit”.
        - Value choice on flt(d.credit) &gt; 0 — true gives “debit”, false gives “credit”.
      - Set valid from false.
      - For each jvd in against\_entries.
        - If flt(jvd at dr\_or\_cr) &gt; 0.
          - Set valid from true.
      - If (not valid and not self.system\_generated\_gain\_loss()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not valid → not self.system\_generated\_gain\_loss().
        - Call the validation error handler Platform.throw(translated “Against Journal Entry {0} does not have any unmatched {1} entry”.format(d.reference\_name, dr\_or\_cr)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.voucher\_type differs from “Exchange Gain Or Loss”, self.voucher\_type = “Journal Entry” selects the branch that calls the validation-error handler with translated “Journal Entry {0} does not have account {1} or already matched against other voucher”.format(d.reference\_name, d.account). With self.voucher\_type = “Exchange Gain Or Loss”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-f785f1746bc81a-guard-39)

**Methods declared on this owner** [system generated gain loss](operations-057.md#op-851ea152e440cc).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, “root\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1143)

<a id="op-9c9dfd1b26c980"></a>
### Journal Entry.validate reference doc

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_validate_reference_doc`

**Inputs** self.

**Record and data access** read d.reference\_type via get\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Debit entry can not be linked with a {1}”.format(d.idx, d.reference\_type) · validation helper — translated “Row {0}: Credit entry can not be linked with a {1}”.format(d.idx, d.reference\_type) · validation helper — translated “Row {0}: Invalid reference {1}”.format(d.idx, d.reference\_name) · validation helper — translated “Row {0}: Party / Account does not match with {1} / {2} in {3} {4}”.format(d.idx, field\_dict.get(d.reference\_type) at 0, field\_dict.get(d.reference\_type) at 1, d.reference\_type, …) · validation helper — translated “Row {0}: {1} {2} does not match with {3}”.format(d.idx, d.party\_type, d.party, d.reference\_type).

**Local steps**

- Set field\_dict from mapping(“Sales Invoice” → list(“Customer”, “Debit To”), “Purchase Invoice” → list(“Supplier”, “Credit To”), “Sales Order” → list(“Customer”), “Purchase Order” → list(“Supplier”)).
- Set self.reference\_totals from mapping().
- Set self.reference\_types from mapping().
- Set self.reference\_accounts from mapping().
- For each d in self.get(“accounts”).
  - If not d.reference\_type.
    - Set d.reference\_name from no value.
  - If not d.reference\_name.
    - Set d.reference\_type from no value.
  - If (d.reference\_type and d.reference\_name and d.reference\_type belongs to list(field\_dict)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type → d.reference\_name → d.reference\_type belongs to list(field\_dict).
    - Set dr\_or\_cr from “credit\_in\_account\_currency” when d.reference\_type belongs to tuple(“Sales Order”, “Sales Invoice”), otherwise “debit\_in\_account\_currency”.
      - Value choice on d.reference\_type belongs to tuple(“Sales Order”, “Sales Invoice”) — true gives “credit\_in\_account\_currency”, false gives “debit\_in\_account\_currency”.
    - If (d.reference\_type equals “Sales Order” and flt(d.debit) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Sales Order” → flt(d.debit) &gt; 0.
      - Call the validation error handler Platform.throw(translated “Row {0}: Debit entry can not be linked with a {1}”.format(d.idx, d.reference\_type)).
    - If (d.reference\_type equals “Purchase Order” and flt(d.credit) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Purchase Order” → flt(d.credit) &gt; 0.
      - Call the validation error handler Platform.throw(translated “Row {0}: Credit entry can not be linked with a {1}”.format(d.idx, d.reference\_type)).
    - If d.reference\_name does not belong to self.reference\_totals.
      - Set self.reference\_totals at d.reference\_name from 0.0.
    - If self.voucher\_type does not belong to tuple(“Deferred Revenue”, “Deferred Expense”).
      - Update self.reference\_totals at d.reference\_name using + flt(d.get(dr\_or\_cr)).
    - Set self.reference\_types at d.reference\_name from d.reference\_type.
    - Set self.reference\_accounts at d.reference\_name from d.account.
    - Set against\_voucher from Platform.db.get\_value(d.reference\_type, d.reference\_name, list of scrub(dt) for dt drawn from field\_dict.get(d.reference\_type)).
      - Draw dt from field\_dict.get(d.reference\_type).
    - If not against\_voucher.
      - Call the validation error handler Platform.throw(translated “Row {0}: Invalid reference {1}”.format(d.idx, d.reference\_name)).
    - If d.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
      - If (self.voucher\_type belongs to tuple(“Deferred Revenue”, “Deferred Expense”) and d.reference\_detail\_no).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type belongs to tuple(“Deferred Revenue”, “Deferred Expense”) → d.reference\_detail\_no.
        - Set debit\_or\_credit from “Debit” when d.debit, otherwise “Credit”.
          - Value choice on d.debit — true gives “Debit”, false gives “Credit”.
        - Set party\_account from get\_deferred\_booking\_accounts(d.reference\_type, d.reference\_detail\_no, debit\_or\_credit).
        - Set against\_voucher from list(empty text, against\_voucher at 1).
      - Otherwise.
        - If d.reference\_type equals “Sales Invoice”.
          - Set party\_account from (get\_party\_account\_based\_on\_invoice\_discounting(d.reference\_name) or against\_voucher at 1).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_party\_account\_based\_on\_invoice\_discounting(d.reference\_name) → against\_voucher at 1.
        - Otherwise.
          - Set party\_account from against\_voucher at 1.
      - If ((against\_voucher at 0 differs from cstr(d.party) or party\_account differs from d.account) and self.voucher\_type differs from “Exchange Gain Or Loss”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in (against\_voucher at 0 differs from cstr(d.party) or party\_account differs from d.account) → self.voucher\_type differs from “Exchange Gain Or Loss”.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in against\_voucher at 0 differs from cstr(d.party) → party\_account differs from d.account.
        - Call the validation error handler Platform.throw(translated “Row {0}: Party / Account does not match with {1} / {2} in {3} {4}”.format(d.idx, field\_dict.get(d.reference\_type) at 0, field\_dict.get(d.reference\_type) at 1, d.reference\_type, …)).
    - If d.reference\_type belongs to tuple(“Sales Order”, “Purchase Order”).
      - If against\_voucher differs from d.party.
        - Call the validation error handler Platform.throw(translated “Row {0}: {1} {2} does not match with {3}”.format(d.idx, d.party\_type, d.party, d.reference\_type)).
- Evaluate self.validate\_orders().
- Evaluate self.validate\_invoices().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate orders](operations-057.md#op-069417a7c07ced), [validate invoices](operations-057.md#op-7d7e0965ff26d1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L815)

<a id="op-069417a7c07ced"></a>
### Journal Entry.validate orders

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_validate_orders`

**Inputs** self.

**Record and data access** resolve a document from reference\_type via get\_doc.

**Explicit failure paths** validation helper — translated “{0} {1} is not submitted”.format(reference\_type, reference\_name) · validation helper — translated “{0} {1} is fully billed”.format(reference\_type, reference\_name) · validation helper — translated “{0} {1} is closed”.format(reference\_type, reference\_name) · validation helper — translated “Advance paid against {0} {1} cannot be greater than Grand Total {2}”.format(reference\_type, reference\_name, formatted\_voucher\_total).

**Local steps**

- For each tuple(reference\_name, total) in self.reference\_totals.items().
  - Set reference\_type from self.reference\_types at reference\_name.
  - Set account from self.reference\_accounts at reference\_name.
  - If reference\_type belongs to tuple(“Sales Order”, “Purchase Order”).
    - Set order from Platform.get\_doc(reference\_type, reference\_name).
    - <a id="op-069417a7c07ced-guard-10"></a>If order.docstatus differs from 1.
      - Call the validation error handler Platform.throw(translated “{0} {1} is not submitted”.format(reference\_type, reference\_name)).
    - If flt(order.per\_billed) ≥ 100.
      - Call the validation error handler Platform.throw(translated “{0} {1} is fully billed”.format(reference\_type, reference\_name)).
    - If cstr(order.status) equals “Closed”.
      - Call the validation error handler Platform.throw(translated “{0} {1} is closed”.format(reference\_type, reference\_name)).
    - Set account\_currency from get\_account\_currency(account).
    - If account\_currency equals self.company\_currency.
      - Set voucher\_total from order.base\_grand\_total.
      - Set formatted\_voucher\_total from fmt\_money(voucher\_total, order.precision(“base\_grand\_total”), currency = account\_currency).
    - Otherwise.
      - Set voucher\_total from order.grand\_total.
      - Set formatted\_voucher\_total from fmt\_money(voucher\_total, order.precision(“grand\_total”), currency = account\_currency).
    - If flt(voucher\_total) &lt; (flt(order.advance\_paid) + total).
      - Call the validation error handler Platform.throw(translated “Advance paid against {0} {1} cannot be greater than Grand Total {2}”.format(reference\_type, reference\_name, formatted\_voucher\_total)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison order.docstatus differs from 1, order.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “{0} {1} is not submitted”.format(reference\_type, reference\_name). With order.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-069417a7c07ced-guard-10)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L814)

<a id="op-7d7e0965ff26d1"></a>
### Journal Entry.validate invoices

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_validate_invoices`

**Inputs** self.

**Record and data access** resolve a document from reference\_type via get\_doc.

**Explicit failure paths** validation helper — translated “{0} {1} is not submitted”.format(reference\_type, reference\_name) · validation helper — translated “Payment against {0} {1} cannot be greater than Outstanding Amount {2}”.format(reference\_type, reference\_name, invoice.outstanding\_amount) · validation helper — msg.

**Local steps**

- For each tuple(reference\_name, total) in self.reference\_totals.items().
  - Set reference\_type from self.reference\_types at reference\_name.
  - If (reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and self.voucher\_type does not belong to list(“Debit Note”, “Credit Note”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) → self.voucher\_type does not belong to list(“Debit Note”, “Credit Note”).
    - Set invoice from Platform.get\_doc(reference\_type, reference\_name).
    - <a id="op-7d7e0965ff26d1-guard-12"></a>If invoice.docstatus differs from 1.
      - Call the validation error handler Platform.throw(translated “{0} {1} is not submitted”.format(reference\_type, reference\_name)).
    - Set precision from invoice.precision(“outstanding\_amount”).
    - If (total and flt(invoice.outstanding\_amount, precision) &lt; flt(total, precision)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in total → flt(invoice.outstanding\_amount, precision) &lt; flt(total, precision).
      - Call the validation error handler Platform.throw(translated “Payment against {0} {1} cannot be greater than Outstanding Amount {2}”.format(reference\_type, reference\_name, invoice.outstanding\_amount)).
    - If (reference\_type equals “Purchase Invoice” and invoice.invoice\_is\_blocked()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_type equals “Purchase Invoice” → invoice.invoice\_is\_blocked().
      - Set msg from translated “{0} {1} is blocked and on hold until {2}.”.format(invoice.doctype, invoice.name, invoice.release\_date) when invoice.release\_date, otherwise translated “{0} {1} is blocked.”.format(invoice.docty ….
        - Value choice on invoice.release\_date — true gives translated “{0} {1} is blocked and on hold until {2}.”.format(invoice.doctype, invoice.name, invoice.release\_date), false gives translated “{0} {1} is blocked.”.format(invoice.doctype, invoice.name).
      - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison invoice.docstatus differs from 1, invoice.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “{0} {1} is not submitted”.format(reference\_type, reference\_name). With invoice.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7d7e0965ff26d1-guard-12)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L813)

<a id="op-ff05d785ce3a81"></a>
### Journal Entry.set against account

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_set_against_account`

**Inputs** self.

**Record and data access** read d.reference\_type via get\_value.

**Local steps**

- Set tuple(accounts\_debited, accounts\_credited) from tuple(list(), list()).
- If self.voucher\_type belongs to tuple(“Deferred Revenue”, “Deferred Expense”).
  - For each d in self.get(“accounts”).
    - If d.reference\_type equals “Sales Invoice”.
      - Set field from “customer”.
    - Otherwise.
      - Set field from “supplier”.
    - Set d.against\_account from Platform.db.get\_value(d.reference\_type, d.reference\_name, field).
- Otherwise.
  - For each d in self.get(“accounts”).
    - If flt(d.debit) &gt; 0.
      - Evaluate accounts\_debited.append((d.party or d.account)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.party → d.account.
    - If flt(d.credit) &gt; 0.
      - Evaluate accounts\_credited.append((d.party or d.account)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.party → d.account.
  - For each d in self.get(“accounts”).
    - If flt(d.debit) &gt; 0.
      - Set d.against\_account from “, ”.join(list(set(accounts\_credited))).
    - If flt(d.credit) &gt; 0.
      - Set d.against\_account from “, ”.join(list(set(accounts\_debited))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L2187) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1129)

<a id="op-a02cd4d3977469"></a>
### Journal Entry.validate debit credit amount

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_debit_credit_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Both Debit and Credit values cannot be zero”.format(d.idx).

**Local steps**

- If not (self.voucher\_type equals “Exchange Gain Or Loss” and self.multi\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Exchange Gain Or Loss” → self.multi\_currency.
  - For each d in self.get(“accounts”).
    - If (not flt(d.debit) and not flt(d.credit)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(d.debit) → not flt(d.credit).
      - Call the validation error handler Platform.throw(translated “Row {0}: Both Debit and Credit values cannot be zero”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L2854) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1147)

<a id="op-6e9eb3aba72aab"></a>
### Journal Entry.validate total debit and credit

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_total_debit_and_credit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Total Debit must be equal to Total Credit. The difference is {0}”.format(self.difference).

**Local steps**

- If not (self.voucher\_type equals “Exchange Gain Or Loss” and self.multi\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Exchange Gain Or Loss” → self.multi\_currency.
  - If self.difference.
    - Call the validation error handler Platform.throw(translated “Total Debit must be equal to Total Credit. The difference is {0}”.format(self.difference)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L3086) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1155)

<a id="op-037540bec72f17"></a>
### Journal Entry.set total debit credit

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_set_total_debit_credit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You cannot credit and debit same account at the same time”.

**Local steps**

- Set tuple(self.total\_debit, self.total\_credit, self.difference) from tuple(0, 0, 0).
- For each d in self.get(“accounts”).
  - If (d.debit and d.credit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.debit → d.credit.
    - Call the validation error handler Platform.throw(translated “You cannot credit and debit same account at the same time”).
  - Set self.total\_debit from flt((self.total\_debit + flt(d.debit, d.precision(“debit”))), self.precision(“total\_debit”)).
  - Set self.total\_credit from flt((self.total\_credit + flt(d.credit, d.precision(“credit”))), self.precision(“total\_credit”)).
- Set self.difference from flt((self.total\_debit − self.total\_credit), self.precision(“difference”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L3235) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1134)

<a id="op-79b67fa98d3e46"></a>
### Journal Entry.validate multi currency

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_multi_currency`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Please check Multi Currency option to allow accounts with other currency”.

**Local steps**

- Set alternate\_currency from list().
- For each d in self.get(“accounts”).
  - Set account from Platform.get\_cached\_value(“Account”, d.account, list(“account\_currency”, “account\_type”), as\_dict = 1).
  - If account.
    - Set d.account\_currency from account.account\_currency.
    - Set d.account\_type from account.account\_type.
  - If not d.account\_currency.
    - Set d.account\_currency from self.company\_currency.
  - If (d.account\_currency differs from self.company\_currency and d.account\_currency does not belong to alternate\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.account\_currency differs from self.company\_currency → d.account\_currency does not belong to alternate\_currency.
    - Evaluate alternate\_currency.append(d.account\_currency).
- If alternate\_currency.
  - If not self.multi\_currency.
    - Call the validation error handler Platform.throw(translated “Please check Multi Currency option to allow accounts with other currency”).
- Evaluate self.set\_exchange\_rate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set exchange rate](operations-057.md#op-694fe7a9f3d83a).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, list(“account\_currency”, “account\_type”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L3698) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1152)

<a id="op-2d8efb445635b0"></a>
### Journal Entry.set amounts in company currency

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_set_amounts_in_company_currency`

**Inputs** self.

**Local steps**

- If not (self.voucher\_type equals “Exchange Gain Or Loss” and self.multi\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Exchange Gain Or Loss” → self.multi\_currency.
  - For each d in self.get(“accounts”).
    - Set d.debit\_in\_account\_currency from flt(d.debit\_in\_account\_currency, d.precision(“debit\_in\_account\_currency”)).
    - Set d.credit\_in\_account\_currency from flt(d.credit\_in\_account\_currency, d.precision(“credit\_in\_account\_currency”)).
    - Set d.debit from flt((d.debit\_in\_account\_currency × flt(d.exchange\_rate)), d.precision(“debit”)).
    - Set d.credit from flt((d.credit\_in\_account\_currency × flt(d.exchange\_rate)), d.precision(“credit”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L4115) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1130)

<a id="op-694fe7a9f3d83a"></a>
### Journal Entry.set exchange rate

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_set_exchange_rate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Exchange Rate is mandatory”.format(d.idx).

**Local steps**

- For each d in self.get(“accounts”).
  - If d.account\_currency equals self.company\_currency.
    - Set d.exchange\_rate from 1.
  - Otherwise.
    - If (not d.exchange\_rate or d.exchange\_rate equals 1 or (d.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and d.reference\_name and self.posting\_date)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.exchange\_rate → d.exchange\_rate equals 1 → (d.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and d.reference\_name and self.posting\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) → d.reference\_name → self.posting\_date.
      - Set ignore\_exchange\_rate from false.
      - If (self.get(“flags”) and self.flags.get(“ignore\_exchange\_rate”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“flags”) → self.flags.get(“ignore\_exchange\_rate”).
        - Set ignore\_exchange\_rate from true.
      - If not ignore\_exchange\_rate.
        - Set d.exchange\_rate from get\_exchange\_rate(self.posting\_date, d.account, d.account\_currency, self.company, …).
  - If not d.exchange\_rate.
    - Call the validation error handler Platform.throw(translated “Row {0}: Exchange Rate is mandatory”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1131)

<a id="op-c963c6b4bcd0ce"></a>
### Journal Entry.create remarks

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_create_remarks`

**Inputs** self.

**Record and data access** execute query text (SELECT, Purchase Invoice).

**Explicit results** no value.

**Local steps**

- Set r from list().
- If self.flags.skip\_remarks\_creation.
  - Return no value.
- If self.get(“custom\_remark”).
  - Return no value.
- If self.cheque\_no.
  - If self.cheque\_date.
    - Evaluate r.append(translated “Reference #{0} dated {1}”.format(self.cheque\_no, formatdate(self.cheque\_date))).
  - Otherwise.
    - Evaluate msgprint(translated “Please enter Reference date”, raise\_exception = Platform.MandatoryError).
- For each d in self.get(“accounts”).
  - If (d.reference\_type equals “Sales Invoice” and d.credit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Sales Invoice” → d.credit.
    - Evaluate r.append(translated “{0} against Sales Invoice {1}”.format(fmt\_money(flt(d.credit), currency = self.company\_currency), d.reference\_name)).
  - If (d.reference\_type equals “Sales Order” and d.credit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Sales Order” → d.credit.
    - Evaluate r.append(translated “{0} against Sales Order {1}”.format(fmt\_money(flt(d.credit), currency = self.company\_currency), d.reference\_name)).
  - If (d.reference\_type equals “Purchase Invoice” and d.debit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Purchase Invoice” → d.debit.
    - Set bill\_no from Platform.db.sql(query text (SELECT, Purchase Invoice), d.reference\_name).
    - If (bill\_no and bill\_no at 0 at 0 and nested operand in the contract at nested operand in the contract.lower().strip() does not belong to list(“na”, “not applicable”, “none”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in bill\_no → bill\_no at 0 at 0 → nested operand in the contract at nested operand in the contract at 0.lower().strip() does not belong to list(“na”, “not applicable”, “none”).
      - Evaluate r.append(translated “{0} against Bill {1} dated {2}”.format(fmt\_money(flt(d.debit), currency = self.company\_currency), bill\_no at 0 at 0, (bill\_no at 0 at 1 and formatdate(nested operand in the contract at ….
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in bill\_no at 0 at 1 → formatdate(bill\_no at 0 at 1.strftime(“%Y-%m-%d”)).
  - If (d.reference\_type equals “Purchase Order” and d.debit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Purchase Order” → d.debit.
    - Evaluate r.append(translated “{0} against Purchase Order {1}”.format(fmt\_money(flt(d.credit), currency = self.company\_currency), d.reference\_name)).
- If r.
  - Set self.remark from whitespace '\\n'.join(r).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1117)

<a id="op-77ef939269fb52"></a>
### Journal Entry.set print format fields

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_set_print_format_fields`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value · read party\_type via get\_value.

**Local steps**

- Set bank\_amount, party\_amount, total\_amount from 0.0.
- Set currency, bank\_account\_currency, party\_account\_currency, pay\_to\_recd\_from from no value.
- Set party\_type from no value.
- For each d in self.get(“accounts”).
  - If (d.party\_type belongs to list(“Customer”, “Supplier”) and d.party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type belongs to list(“Customer”, “Supplier”) → d.party.
    - Set party\_type from d.party\_type.
    - If not pay\_to\_recd\_from.
      - Set pay\_to\_recd\_from from d.party.
    - If (pay\_to\_recd\_from and pay\_to\_recd\_from equals d.party).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pay\_to\_recd\_from → pay\_to\_recd\_from equals d.party.
      - Update party\_amount using + (flt(d.debit\_in\_account\_currency) or flt(d.credit\_in\_account\_currency)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.debit\_in\_account\_currency) → flt(d.credit\_in\_account\_currency).
      - Set party\_account\_currency from d.account\_currency.
  - Otherwise.
    - If Platform.get\_cached\_value(“Account”, d.account, “account\_type”) belongs to list(“Bank”, “Cash”).
      - Update bank\_amount using + (flt(d.debit\_in\_account\_currency) or flt(d.credit\_in\_account\_currency)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.debit\_in\_account\_currency) → flt(d.credit\_in\_account\_currency).
      - Set bank\_account\_currency from d.account\_currency.
- If (party\_type and pay\_to\_recd\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → pay\_to\_recd\_from.
  - Set self.pay\_to\_recd\_from from Platform.db.get\_value(party\_type, pay\_to\_recd\_from, “customer\_name” when party\_type equals “Customer”, otherwise “supplier\_name”).
    - Value choice on party\_type equals “Customer” — true gives “customer\_name”, false gives “supplier\_name”.
  - If bank\_amount.
    - Set total\_amount from bank\_amount.
    - Set currency from bank\_account\_currency.
  - Otherwise.
    - Set total\_amount from party\_amount.
    - Set currency from party\_account\_currency.
- Evaluate self.set\_total\_amount(total\_amount, currency).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set total amount](operations-057.md#op-5d757b092790ae).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1132)

<a id="op-5d757b092790ae"></a>
### Journal Entry.set total amount

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_set_total_amount`

**Inputs** self, amt, currency.

**Local steps**

- Set self.total\_amount from amt.
- Set self.total\_amount\_currency from currency.
- Bind dependencies money\_in\_words.
- Set self.total\_amount\_in\_words from money\_in\_words(amt, currency).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1133)

<a id="op-db59417889b041"></a>
### Journal Entry.build gl map

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_build_general_ledger_map`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** gl\_map.

**Local steps**

- Set gl\_map from list().
- Set company\_currency from Enterprise.get\_company\_currency(self.company).
- Set self.transaction\_currency from company\_currency.
- Set self.transaction\_exchange\_rate from 1.
- If self.multi\_currency.
  - For each row in self.get(“accounts”).
    - If row.account\_currency differs from company\_currency.
      - Set self.transaction\_currency from row.account\_currency.
      - Set self.transaction\_exchange\_rate from row.exchange\_rate.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Set advance\_doctypes from get\_advance\_payment\_doctypes().
- For each d in self.get(“accounts”).
  - If (d.debit or d.credit or self.voucher\_type equals “Exchange Gain Or Loss”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.debit → d.credit → self.voucher\_type equals “Exchange Gain Or Loss”.
    - Set r from list(d.user\_remark, self.remark).
    - Set r from list of x for x drawn from r where x.
      - Draw x from r, keep a combination only if (x).
    - Set remarks from whitespace '\\n'.join(r).
    - Set row from mapping(“account” → d.account, “party\_type” → d.party\_type, “due\_date” → self.due\_date, “party” → d.party, …).
      - Value choice on self.transaction\_currency equals d.account\_currency — true gives flt(d.debit\_in\_account\_currency, d.precision(“debit\_in\_account\_currency”)), false gives (flt(d.debit, d.precision(“debit”)) ÷ self.transaction\_exchange\_rate).
      - Value choice on self.transaction\_currency equals d.account\_currency — true gives flt(d.credit\_in\_account\_currency, d.precision(“credit\_in\_account\_currency”)), false gives (flt(d.credit, d.precision(“credit”)) ÷ self.transaction\_exchange\_rate).
    - If d.reference\_type belongs to advance\_doctypes.
      - Evaluate row.update(mapping(“against\_voucher\_type” → self.doctype, “against\_voucher” → self.name, “advance\_voucher\_type” → d.reference\_type, “advance\_voucher\_no” → d.reference\_name)).
    - Set account\_type from Platform.get\_cached\_value(“Account”, d.account, “account\_type”).
    - If (account\_type belongs to list(“Receivable”, “Payable”) and self.party\_not\_required).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type belongs to list(“Receivable”, “Payable”) → self.party\_not\_required.
      - Set Platform.flags.party\_not\_required from true.
    - Evaluate gl\_map.append(self.get\_gl\_dict(row, item = d)).
- Return gl\_map.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1114)

<a id="op-cfdfd9f84a32e5"></a>
### Journal Entry.make gl entries

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_make_general_ledger_entries`

**Inputs** self, cancel = 0, adv\_adj = 0.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Bind dependencies make\_gl\_entries.
- Set merge\_entries from Platform.get\_single\_value(“Accounts Settings”, “merge\_similar\_account\_heads”).
- Set gl\_map from self.build\_gl\_map().
- If self.voucher\_type belongs to tuple(“Deferred Revenue”, “Deferred Expense”).
  - Set update\_outstanding from “No”.
- Otherwise.
  - Set update\_outstanding from “Yes”.
- If gl\_map.
  - Evaluate make\_gl\_entries(gl\_map, cancel = cancel, adv\_adj = adv\_adj, merge\_entries = merge\_entries, update\_outstanding = update\_outstanding).
  - Set Platform.flags.party\_not\_required from false.
  - If cancel.
    - Evaluate cancel\_exchange\_gain\_loss\_journal(Platform.\_dict(doctype = self.doctype, name = self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build gl map](operations-057.md#op-db59417889b041).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “merge\_similar\_account\_heads”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1125)

<a id="op-0ef586976ec823"></a>
### Journal Entry.get balance

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_get_balance`

**Inputs** self, difference\_account = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If not self.get(“accounts”).
  - Evaluate msgprint(translated “'Entries' cannot be empty”, raise\_exception = true).
- Otherwise.
  - Set tuple(self.total\_debit, self.total\_credit) from tuple(0, 0).
  - Set diff from flt(self.difference, self.precision(“difference”)).
  - If diff.
    - Set blank\_row from no value.
    - For each d in self.get(“accounts”).
      - If (not d.credit\_in\_account\_currency and not d.debit\_in\_account\_currency and diff differs from 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.credit\_in\_account\_currency → not d.debit\_in\_account\_currency → diff differs from 0.
        - Set blank\_row from d.
    - If not blank\_row.
      - Set blank\_row from self.append(“accounts”, mapping(“account” → difference\_account, “cost\_center” → Enterprise.get\_default\_cost\_center(self.company))).
    - Set blank\_row.exchange\_rate from 1.
    - If diff &gt; 0.
      - Set blank\_row.credit\_in\_account\_currency from diff.
      - Set blank\_row.credit from diff.
    - Otherwise.
      - If diff &lt; 0.
        - Set blank\_row.debit\_in\_account\_currency from abs(diff).
        - Set blank\_row.debit from abs(diff).
  - Evaluate self.set\_total\_debit\_credit().
  - Evaluate self.validate\_total\_debit\_and\_credit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set total debit credit](operations-057.md#op-037540bec72f17), [validate total debit and credit](operations-057.md#op-6e9eb3aba72aab).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1118)

<a id="op-2036ccecf716d2"></a>
### Journal Entry.get outstanding invoices

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_get_outstanding_invoices`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set(“accounts”, list()).
- Set total from 0.
- For each d in self.get\_values().
  - Update total using + flt(d.outstanding\_amount, self.precision(“credit”, “accounts”)).
  - Set jd1 from self.append(“accounts”, mapping()).
  - Set jd1.account from d.account.
  - Set jd1.party from d.party.
  - If self.write\_off\_based\_on equals “Accounts Receivable”.
    - Set jd1.party\_type from “Customer”.
    - Set jd1.credit\_in\_account\_currency from flt(d.outstanding\_amount, self.precision(“credit”, “accounts”)).
    - Set jd1.reference\_type from “Sales Invoice”.
    - Set jd1.reference\_name from cstr(d.name).
  - Otherwise.
    - If self.write\_off\_based\_on equals “Accounts Payable”.
      - Set jd1.party\_type from “Supplier”.
      - Set jd1.debit\_in\_account\_currency from flt(d.outstanding\_amount, self.precision(“debit”, “accounts”)).
      - Set jd1.reference\_type from “Purchase Invoice”.
      - Set jd1.reference\_name from cstr(d.name).
- Set jd2 from self.append(“accounts”, mapping()).
- If self.write\_off\_based\_on equals “Accounts Receivable”.
  - Set jd2.debit\_in\_account\_currency from total.
- Otherwise.
  - If self.write\_off\_based\_on equals “Accounts Payable”.
    - Set jd2.credit\_in\_account\_currency from total.
- Evaluate self.validate\_total\_debit\_and\_credit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get values](operations-057.md#op-465f46b652eb73), [validate total debit and credit](operations-057.md#op-6e9eb3aba72aab).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1120)

<a id="op-465f46b652eb73"></a>
### Journal Entry.get values

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_get_values`

**Inputs** self.

**Record and data access** execute query text (SELECT, Sales Invoice).format(“%s”, cond) · execute query text (SELECT, Purchase Invoice).format(“%s”, cond).

**Explicit results** Platform.db.sql(query text (SELECT, Sales Invoice).format(“%s”, cond), self.company, as\_dict = true) · Platform.db.sql(query text (SELECT, Purchase Invoice).format(“%s”, cond), self.company, as\_dict = true).

**Local steps**

- Set cond from formatted text  and outstanding\_amount &lt;= {flt(self.write\_off\_amount)} when flt(self.write\_off\_amount) &gt; 0, otherwise empty text.
  - Value choice on flt(self.write\_off\_amount) &gt; 0 — true gives formatted text  and outstanding\_amount &lt;= {flt(self.write\_off\_amount)}, false gives empty text.
- If self.write\_off\_based\_on equals “Accounts Receivable”.
  - Return Platform.db.sql(query text (SELECT, Sales Invoice).format(“%s”, cond), self.company, as\_dict = true).
- Otherwise.
  - If self.write\_off\_based\_on equals “Accounts Payable”.
    - Return Platform.db.sql(query text (SELECT, Purchase Invoice).format(“%s”, cond), self.company, as\_dict = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1123)

<a id="op-4e1606f7dbac32"></a>
### Journal Entry.validate credit debit note

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_credit_debit_note`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_value · read mapping(“doctype” → “Journal Entry”, “stock\_entry” → self.stock\_entry, “docstatus” → 1) via exists.

**State and service calls** msgprint with translated “Warning: Another {0} # {1} exists against stock entry {2}”.format(self.voucher\_type, self.name, self.stock\_entry).

**Explicit failure paths** validation helper — translated “Stock Entry {0} is not submitted”.format(self.stock\_entry).

**Local steps**

- If self.stock\_entry.
  - If Platform.db.get\_value(“Stock Entry”, self.stock\_entry, “docstatus”) differs from 1.
    - Call the validation error handler Platform.throw(translated “Stock Entry {0} is not submitted”.format(self.stock\_entry)).
  - If Platform.db.exists(mapping(“doctype” → “Journal Entry”, “stock\_entry” → self.stock\_entry, “docstatus” → 1)).
    - Evaluate Platform.msgprint(translated “Warning: Another {0} # {1} exists against stock entry {2}”.format(self.voucher\_type, self.name, self.stock\_entry)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0064.json#L2693) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1146)

<a id="op-7175d9d60b9163"></a>
### Journal Entry.validate empty accounts table

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_empty_accounts_table`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Accounts table cannot be blank.”.

**Local steps**

- If not self.get(“accounts”).
  - Call the validation error handler Platform.throw(translated “Accounts table cannot be blank.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0064.json#L3025) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1148)

<a id="op-caad2b45f31c3c"></a>
### Get default bank cash account

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_get_default_bank_cash_account`

**Inputs** company, account\_type = no value, mode\_of\_payment = no value, account = no value, fetch\_balance (named only, default true).

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_all · read “Account” via get\_cached\_value.

**Explicit results** Platform.\_dict(result) · Platform.\_dict().

**Local steps**

- Bind dependencies get\_bank\_cash\_account.
- Evaluate Platform.has\_permission(“Company”, ptype = “select”, doc = company, throw = true).
- If mode\_of\_payment.
  - Set account from get\_bank\_cash\_account(mode\_of\_payment, company).get(“account”).
- If not account.
  - If account\_type equals “Bank”.
    - Set account from Platform.get\_cached\_value(“Company”, company, “default\_bank\_account”).
    - If not account.
      - Set account\_list from Platform.get\_all(“Account”, filters = mapping(“company” → company, “account\_type” → “Bank”, “is\_group” → 0)).
      - If len(account\_list) equals 1.
        - Set account from account\_list at 0.name.
  - Otherwise.
    - If account\_type equals “Cash”.
      - Set account from Platform.get\_cached\_value(“Company”, company, “default\_cash\_account”).
      - If not account.
        - Set account\_list from Platform.get\_all(“Account”, filters = mapping(“company” → company, “account\_type” → “Cash”, “is\_group” → 0)).
        - If len(account\_list) equals 1.
          - Set account from account\_list at 0.name.
- If account.
  - Evaluate Platform.has\_permission(“Account”, doc = account, throw = true).
  - Set account\_details from Platform.get\_cached\_value(“Account”, account, list(“account\_currency”, “account\_type”), as\_dict = 1).
  - Set result from mapping(“account” → account, “account\_currency” → account\_details.account\_currency, “account\_type” → account\_details.account\_type).
  - If fetch\_balance.
    - Set result at “balance” from get\_balance\_on(account).
  - Return Platform.\_dict(result).
- Otherwise.
  - Return Platform.\_dict().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, ptype = “select”, doc = company, throw = true), Platform.has\_permission(“Account”, doc = account, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_bank\_account”), Platform.get\_cached\_value(“Company”, company, “default\_cash\_account”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1168) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1108)

<a id="op-e75d8c2e806d37"></a>
### Get payment entry against order

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_get_payment_entry_against_order`

**Inputs** dt, dn, amount = no value, debit\_in\_account\_currency = no value, journal\_entry = false, bank\_account = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from dt via get\_doc.

**Explicit results** get\_payment\_entry(ref\_doc, mapping(“party\_type” → party\_type, “party\_account” → party\_account, “party\_account\_currency” → party\_account\_currency, “amount\_field\_party” → amount\_field\_party, …)).

**Explicit failure paths** validation helper — translated “Can only make payment against unbilled {0}”.format(dt).

**Local steps**

- Set ref\_doc from Platform.get\_doc(dt, dn).
- Evaluate ref\_doc.check\_permission().
- If flt(ref\_doc.per\_billed, 2) &gt; 0.
  - Call the validation error handler Platform.throw(translated “Can only make payment against unbilled {0}”.format(dt)).
- If dt equals “Sales Order”.
  - Set party\_type from “Customer”.
  - Set amount\_field\_party from “credit\_in\_account\_currency”.
  - Set amount\_field\_bank from “debit\_in\_account\_currency”.
- Otherwise.
  - Set party\_type from “Supplier”.
  - Set amount\_field\_party from “debit\_in\_account\_currency”.
  - Set amount\_field\_bank from “credit\_in\_account\_currency”.
- Set party\_account from get\_party\_account(party\_type, ref\_doc.get(party\_type.lower()), ref\_doc.company).
- Set party\_account\_currency from get\_account\_currency(party\_account).
- If not amount.
  - If party\_account\_currency equals ref\_doc.company\_currency.
    - Set amount from (flt(ref\_doc.base\_grand\_total) − flt(ref\_doc.advance\_paid)).
  - Otherwise.
    - Set amount from (flt(ref\_doc.grand\_total) − flt(ref\_doc.advance\_paid)).
- Return get\_payment\_entry(ref\_doc, mapping(“party\_type” → party\_type, “party\_account” → party\_account, “party\_account\_currency” → party\_account\_currency, “amount\_field\_party” → amount\_field\_party, …)).

**Values supplied outside this operation** effective access from ref\_doc.check\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L161) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L799)
