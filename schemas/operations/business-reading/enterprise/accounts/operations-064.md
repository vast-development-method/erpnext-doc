# Accounting and settlement · operations 64

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment entry

[Record definition](../../../../data/record-types/payment_entry.json)

<a id="op-e697758c42d7e7"></a>
### Payment Entry.trigger invoice update for subscriptions

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_trigger_invoice_update_for_subscriptions`

**Inputs** self.

**Record and data access** read doctype via get\_all · resolve a document from doctype via get\_doc.

**Local steps**

- For each doctype in tuple(“Sales Invoice”, “Purchase Invoice”).
  - Set names from set of ref.reference\_name for ref drawn from self.references where ref.reference\_doctype equals doctype.
    - Draw ref from self.references, keep a combination only if (ref.reference\_doctype equals doctype).
  - If not names.
    - Continue with the next iteration or loop test.
  - Set filters from mapping(“name” → list(“in”, list(names)), “subscription” → list(“is”, “set”)).
  - For each name in Platform.get\_all(doctype, filters = filters, pluck = “name”).
    - Attempt the following.
      - Set doc from Platform.get\_doc(doctype, name).
      - Evaluate doc.refresh\_subscription\_status().
    - On failure (Exception).
      - Evaluate Platform.log\_error(translated “Failed to update subscription status for {0} {1}”.format(doctype, name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1512) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L99)

<a id="op-47a3a71aa3cc61"></a>
### Payment Entry.set missing values

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_missing_values`

**Inputs** self.

**Record and data access** read self.party\_type via get\_value.

**Explicit failure paths** validation helper — translated “Party Type is mandatory” · validation helper — translated “Party is mandatory”.

**Local steps**

- If self.payment\_type equals “Internal Transfer”.
  - For each field in tuple(“party”, “total\_allocated\_amount”, “base\_total\_allocated\_amount”, “unallocated\_amount”).
    - Evaluate self.set(field, no value).
  - Set self.references from list().
- Otherwise.
  - If not self.party\_type.
    - Call the validation error handler Platform.throw(translated “Party Type is mandatory”).
  - If not self.party.
    - Call the validation error handler Platform.throw(translated “Party is mandatory”).
  - Set \_party\_name from “title” when self.party\_type equals “Shareholder”, otherwise (self.party\_type.lower() + “\_name”).
    - Value choice on self.party\_type equals “Shareholder” — true gives “title”, false gives (self.party\_type.lower() + “\_name”).
  - If Platform.db.has\_column(self.party\_type, \_party\_name).
    - Set self.party\_name from Platform.db.get\_value(self.party\_type, self.party, \_party\_name).
  - Otherwise.
    - Set self.party\_name from Platform.db.get\_value(self.party\_type, self.party, “name”).
- If self.party.
  - If self.party\_type equals “Employee”.
    - Set self.contact\_person from no value.
  - Otherwise.
    - If not self.contact\_person.
      - Set self.contact\_person from get\_default\_contact(self.party\_type, self.party).
  - Evaluate complete\_contact\_details(self).
  - If not self.party\_account.
    - Set party\_account from get\_party\_account(self.party\_type, self.party, self.company).
    - Evaluate self.set(self.party\_account\_field, party\_account).
    - Set self.party\_account from party\_account.
- If (self.paid\_from and (not self.paid\_from\_account\_currency or not self.paid\_from\_account\_type)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.paid\_from → (not self.paid\_from\_account\_currency or not self.paid\_from\_account\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.paid\_from\_account\_currency → not self.paid\_from\_account\_type.
  - Set acc from get\_account\_details(self.paid\_from, self.posting\_date, self.cost\_center).
  - Set self.paid\_from\_account\_currency from acc.account\_currency.
  - Set self.paid\_from\_account\_type from acc.account\_type.
- If (self.paid\_to and (not self.paid\_to\_account\_currency or not self.paid\_to\_account\_type)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.paid\_to → (not self.paid\_to\_account\_currency or not self.paid\_to\_account\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.paid\_to\_account\_currency → not self.paid\_to\_account\_type.
  - Set acc from get\_account\_details(self.paid\_to, self.posting\_date, self.cost\_center).
  - Set self.paid\_to\_account\_currency from acc.account\_currency.
  - Set self.paid\_to\_account\_type from acc.account\_type.
- Set self.party\_account\_currency from self.paid\_from\_account\_currency when self.payment\_type equals “Receive”, otherwise self.paid\_to\_account\_currency.
  - Value choice on self.payment\_type equals “Receive” — true gives self.paid\_from\_account\_currency, false gives self.paid\_to\_account\_currency.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0075.json#L5735) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1499) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L86)

<a id="op-b2c3ee93cef56a"></a>
### Payment Entry.set missing ref details

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_missing_reference_details`

**Inputs** self, force = false, update\_ref\_details\_only\_for = no value, reference\_exchange\_details = no value.

**Declared result** no value.

**State and service calls** call db\_set on d.

**Local steps**

- For each d in self.get(“references”).
  - If not d.allocated\_amount.
    - Continue with the next iteration or loop test.
  - If (update\_ref\_details\_only\_for and tuple(d.reference\_doctype, d.reference\_name) does not belong to update\_ref\_details\_only\_for).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_ref\_details\_only\_for → tuple(d.reference\_doctype, d.reference\_name) does not belong to update\_ref\_details\_only\_for.
    - Continue with the next iteration or loop test.
  - Set ref\_details from get\_reference\_details(d.reference\_doctype, d.reference\_name, self.party\_account\_currency, self.party\_type, party\_account = self.party\_account, …).
  - If (reference\_exchange\_details and d.reference\_doctype equals reference\_exchange\_details.reference\_doctype and d.reference\_name equals reference\_exchange\_details.reference\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_exchange\_details → d.reference\_doctype equals reference\_exchange\_details.reference\_doctype → d.reference\_name equals reference\_exchange\_details.reference\_name.
    - Evaluate ref\_details.update(mapping(“exchange\_rate” → reference\_exchange\_details.exchange\_rate)).
  - Set values from mapping().
  - For each tuple(field, value) in ref\_details.items().
    - If (d.exchange\_gain\_loss and self.docstatus differs from 0 and self.get(“\_action”) differs from “submit”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.exchange\_gain\_loss → self.docstatus differs from 0 → self.get(“\_action”) differs from “submit”.
      - Continue with the next iteration or loop test.
    - If (field equals “exchange\_rate” or not d.get(field) or force).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field equals “exchange\_rate” → not d.get(field) → force.
      - Set values at field from value.
  - If (values and self.get(“\_action”) belongs to tuple(“submit”, “cancel”) and not self.is\_new()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in values → self.get(“\_action”) belongs to tuple(“submit”, “cancel”) → not self.is\_new().
    - Evaluate d.db\_set(values).
  - Otherwise.
    - Evaluate d.update(values).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L85)

<a id="op-7eab4851d4fc71"></a>
### Payment Entry.validate payment type

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_payment_type`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Payment Type must be one of Receive, Pay and Internal Transfer”.

**Local steps**

- If self.payment\_type does not belong to tuple(“Receive”, “Pay”, “Internal Transfer”).
  - Call the validation error handler Platform.throw(translated “Payment Type must be one of Receive, Pay and Internal Transfer”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L116)

<a id="op-ff9438efeffb69"></a>
### Payment Entry.validate internal transfer accounts

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_internal_transfer_accounts`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Paid From and Paid To accounts must be different for an Internal Transfer.”.

**Local steps**

- If (self.payment\_type equals “Internal Transfer” and self.paid\_from and self.paid\_from equals self.paid\_to).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_type equals “Internal Transfer” → self.paid\_from → self.paid\_from equals self.paid\_to.
  - Call the validation error handler Platform.throw(translated “Paid From and Paid To accounts must be different for an Internal Transfer.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0076.json#L713) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L111)

<a id="op-e9468b8cacbd25"></a>
### Payment Entry.validate party details

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_party_details`

**Inputs** self.

**Record and data access** read “Party Type” via exists · read “Account” via get\_cached\_value · read “Party Type” via get\_cached\_value · read self.party\_type via exists.

**Explicit failure paths** validation helper — translated “{0} is not a valid Party Type”.format(self.party\_type) · validation helper — translated “Account {0} and Party Type {1} have different account types”.format(self.party\_account, self.party\_type) · validation helper — translated “{0} {1} does not exist”.format(translated self.party\_type, self.party).

**Local steps**

- If self.party\_type.
  - If not Platform.db.exists(“Party Type”, self.party\_type).
    - Call the validation error handler Platform.throw(translated “{0} is not a valid Party Type”.format(self.party\_type)).
  - If (self.get(“party\_account”) and self.party\_type differs from “Employee”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“party\_account”) → self.party\_type differs from “Employee”.
    - Set account\_type from Platform.get\_cached\_value(“Account”, self.party\_account, “account\_type”).
    - Set party\_account\_type from Platform.get\_cached\_value(“Party Type”, self.party\_type, “account\_type”).
    - If (account\_type differs from party\_account\_type and not (self.party\_type equals “Shareholder” and account\_type equals “Equity”) and not self.book\_advance\_payments\_in\_separate\_party\_account).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type differs from party\_account\_type → not (self.party\_type equals “Shareholder” and account\_type equals “Equity”) → not self.book\_advance\_payments\_in\_separate\_party\_account.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_type equals “Shareholder” → account\_type equals “Equity”.
      - Call the validation error handler Platform.throw(translated “Account {0} and Party Type {1} have different account types”.format(self.party\_account, self.party\_type)).
- If (self.party and not Platform.db.exists(self.party\_type, self.party)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party → not Platform.db.exists(self.party\_type, self.party).
  - Call the validation error handler Platform.throw(translated “{0} {1} does not exist”.format(translated self.party\_type, self.party)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.party\_account, “account\_type”), Platform.get\_cached\_value(“Party Type”, self.party\_type, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L115)

<a id="op-da36d8f3f32005"></a>
### Payment Entry.set exchange rate

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_exchange_rate`

**Inputs** self, ref\_doc = no value.

**Local steps**

- Evaluate self.set\_source\_exchange\_rate(ref\_doc).
- Evaluate self.set\_target\_exchange\_rate(ref\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set source exchange rate](operations-064.md#op-4e5320a0b786ca), [set target exchange rate](operations-064.md#op-1a5212f9f28953).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0076.json#L1019) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L80)

<a id="op-4e5320a0b786ca"></a>
### Payment Entry.set source exchange rate

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_source_exchange_rate`

**Inputs** self, ref\_doc = no value.

**Local steps**

- If self.paid\_from.
  - If self.paid\_from\_account\_currency equals self.company\_currency.
    - Set self.source\_exchange\_rate from 1.
  - Otherwise.
    - If (ref\_doc and self.paid\_from\_account\_currency equals ref\_doc.currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_doc → self.paid\_from\_account\_currency equals ref\_doc.currency.
      - Set self.source\_exchange\_rate from (ref\_doc.get(“exchange\_rate”) or ref\_doc.get(“conversion\_rate”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“exchange\_rate”) → ref\_doc.get(“conversion\_rate”).
  - If not self.source\_exchange\_rate.
    - Set self.source\_exchange\_rate from get\_exchange\_rate(self.paid\_from\_account\_currency, self.company\_currency, self.posting\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0076.json#L1110) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L89)

<a id="op-1a5212f9f28953"></a>
### Payment Entry.set target exchange rate

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_target_exchange_rate`

**Inputs** self, ref\_doc = no value.

**Local steps**

- If self.paid\_from\_account\_currency equals self.paid\_to\_account\_currency.
  - Set self.target\_exchange\_rate from self.source\_exchange\_rate.
- Otherwise.
  - If (self.paid\_to and not self.target\_exchange\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.paid\_to → not self.target\_exchange\_rate.
    - If (ref\_doc and self.paid\_to\_account\_currency equals ref\_doc.currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_doc → self.paid\_to\_account\_currency equals ref\_doc.currency.
      - Set self.target\_exchange\_rate from (ref\_doc.get(“exchange\_rate”) or ref\_doc.get(“conversion\_rate”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“exchange\_rate”) → ref\_doc.get(“conversion\_rate”).
    - If not self.target\_exchange\_rate.
      - Set self.target\_exchange\_rate from get\_exchange\_rate(self.paid\_to\_account\_currency, self.company\_currency, self.posting\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0076.json#L1391) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L91)

<a id="op-8f0328e2d0df04"></a>
### Payment Entry.validate mandatory

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated self.meta.get\_label(field)) · validation helper — translated “{0} must be greater than zero”.format(translated self.meta.get\_label(field)).

**Local steps**

- For each field in tuple(“paid\_amount”, “received\_amount”, “source\_exchange\_rate”, “target\_exchange\_rate”).
  - Evaluate self.set(field, flt(self.get(field))).
  - If not self.get(field).
    - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated self.meta.get\_label(field))).
  - If self.get(field) &lt; 0.
    - Call the validation error handler Platform.throw(translated “{0} must be greater than zero”.format(translated self.meta.get\_label(field))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L113)

<a id="op-ea832d4a8b140e"></a>
### Payment Entry.validate reference documents

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_reference_documents`

**Inputs** self.

**Record and data access** read d.reference\_doctype via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Reference Doctype must be one of {0}”.format(comma\_or(list of translated d for d drawn from valid\_reference\_doctypes)) · validation helper — translated “{0} {1} does not exist”.format(d.reference\_doctype, d.reference\_name) · validation helper — translated “{0} {1} is not associated with {2} {3}”.format(translated d.reference\_doctype, d.reference\_name, translated self.party\_type, self.party) · validation helper — translated “{0} {1} is associated with {2}, but Party Account is {3}”.format(translated d.reference\_doctype, d.reference\_name, ref\_party\_account, self.party\_account) · validation helper — translated “{0} {1} is on hold”.format(translated d.reference\_doctype, d.reference\_name) · 1 additional forms in the steps below.

**Local steps**

- Set valid\_reference\_doctypes from self.get\_valid\_reference\_doctypes().
- If not valid\_reference\_doctypes.
  - Return no value.
- For each d in self.get(“references”).
  - If not d.allocated\_amount.
    - Continue with the next iteration or loop test.
  - If d.reference\_doctype does not belong to valid\_reference\_doctypes.
    - Call the validation error handler Platform.throw(translated “Reference Doctype must be one of {0}”.format(comma\_or(list of translated d for d drawn from valid\_reference\_doctypes))).
      - Draw d from valid\_reference\_doctypes.
  - Otherwise.
    - If d.reference\_name.
      - If not Platform.db.exists(d.reference\_doctype, d.reference\_name).
        - Call the validation error handler Platform.throw(translated “{0} {1} does not exist”.format(d.reference\_doctype, d.reference\_name)).
      - Set ref\_doc from Platform.get\_lazy\_doc(d.reference\_doctype, d.reference\_name).
      - If d.reference\_doctype differs from “Journal Entry”.
        - If self.party differs from ref\_doc.get(scrub(self.party\_type)).
          - Call the validation error handler Platform.throw(translated “{0} {1} is not associated with {2} {3}”.format(translated d.reference\_doctype, d.reference\_name, translated self.party\_type, self.party)).
      - Otherwise.
        - Evaluate self.validate\_journal\_entry().
      - If d.reference\_doctype belongs to Platform.get\_hooks(“invoice\_doctypes”).
        - If self.party\_type equals “Customer”.
          - Set ref\_party\_account from (get\_party\_account\_based\_on\_invoice\_discounting(d.reference\_name) or ref\_doc.debit\_to).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_party\_account\_based\_on\_invoice\_discounting(d.reference\_name) → ref\_doc.debit\_to.
        - Otherwise.
          - If self.party\_type equals “Supplier”.
            - Set ref\_party\_account from ref\_doc.credit\_to.
          - Otherwise.
            - If self.party\_type equals “Employee”.
              - Set ref\_party\_account from ref\_doc.payable\_account.
        - If (ref\_party\_account differs from self.party\_account and not self.book\_advance\_payments\_in\_separate\_party\_account).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_party\_account differs from self.party\_account → not self.book\_advance\_payments\_in\_separate\_party\_account.
          - Call the validation error handler Platform.throw(translated “{0} {1} is associated with {2}, but Party Account is {3}”.format(translated d.reference\_doctype, d.reference\_name, ref\_party\_account, self.party\_account)).
        - If (ref\_doc.doctype equals “Purchase Invoice” and ref\_doc.get(“on\_hold”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_doc.doctype equals “Purchase Invoice” → ref\_doc.get(“on\_hold”).
          - Call the validation error handler Platform.throw(translated “{0} {1} is on hold”.format(translated d.reference\_doctype, d.reference\_name), title = translated “Invalid Purchase Invoice”).
      - <a id="op-ea832d4a8b140e-guard-63"></a>If ref\_doc.docstatus differs from 1.
        - Call the validation error handler Platform.throw(translated “{0} {1} must be submitted”.format(translated d.reference\_doctype, d.reference\_name)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison ref\_doc.docstatus differs from 1, ref\_doc.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “{0} {1} must be submitted”.format(translated d.reference\_doctype, d.reference\_name). With ref\_doc.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ea832d4a8b140e-guard-63)

**Methods declared on this owner** [get valid reference doctypes](operations-064.md#op-05046676d168cc), [validate journal entry](operations-064.md#op-6966b1acc5b840).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“invoice\_doctypes”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L119)

<a id="op-05046676d168cc"></a>
### Payment Entry.get valid reference doctypes

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_valid_reference_record_types`

**Inputs** self.

**Explicit results** tuple(“Sales Order”, “Sales Invoice”, “Journal Entry”, “Dunning”, …) · tuple(“Journal Entry”) · tuple(“Purchase Order”, “Purchase Invoice”, “Journal Entry”, “Payment Entry”).

**Local steps**

- If self.party\_type equals “Customer”.
  - Return tuple(“Sales Order”, “Sales Invoice”, “Journal Entry”, “Dunning”, …).
- Otherwise.
  - If self.party\_type belongs to list(“Shareholder”, “Employee”).
    - Return tuple(“Journal Entry”).
  - Otherwise.
    - If self.party\_type equals “Supplier”.
      - Return tuple(“Purchase Order”, “Purchase Invoice”, “Journal Entry”, “Payment Entry”).

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0076.json#L3157) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L64)

<a id="op-f1a8d99621f9e7"></a>
### Payment Entry.validate paid invoices

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_paid_invoices`

**Inputs** self.

**Record and data access** read doctype via get\_all.

**State and service calls** msgprint with ((translated “References {0} of type {1} had no outstanding amount left before submitting the Payment Entry. Now they have …”.format(Platform.bold(comma\_and(paid\_invoices)), translated doctype) + text in t ….

**Local steps**

- For each doctype in tuple(“Sales Invoice”, “Purchase Invoice”).
  - Set names from set of d.reference\_name for d drawn from self.references where (d.allocated\_amount and d.reference\_doctype equals doctype).
    - Draw d from self.references, keep a combination only if ((d.allocated\_amount and d.reference\_doctype equals doctype)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.allocated\_amount → d.reference\_doctype equals doctype.
  - If not names.
    - Continue with the next iteration or loop test.
  - Set paid\_invoices from Platform.get\_all(doctype, filters = mapping(“name” → list(“in”, list(names)), “outstanding\_amount” → list(“&lt;=”, 0), “is\_return” → 0), pluck = “name”).
  - If not paid\_invoices.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.msgprint(((translated “References {0} of type {1} had no outstanding amount left before submitting the Payment Entry. Now they have …”.format(Platform.bold(comma\_and(paid\_invoices)), translated do ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L114)

<a id="op-6966b1acc5b840"></a>
### Payment Entry.validate journal entry

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_journal_entry`

**Inputs** self.

**Record and data access** execute query text (SELECT, Journal Entry Account).

**Explicit failure paths** validation helper — translated “Row #{0}: Journal Entry {1} does not have account {2} or already matched against another voucher”.format(d.idx, d.reference\_name, self.party\_account) · validation helper — translated “Against Journal Entry {0} does not have any unmatched {1} entry”.format(d.reference\_name, translated dr\_or\_cr).

**Local steps**

- For each d in self.get(“references”).
  - If (d.allocated\_amount and d.reference\_doctype equals “Journal Entry”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.allocated\_amount → d.reference\_doctype equals “Journal Entry”.
    - Set je\_accounts from Platform.db.sql(query text (SELECT, Journal Entry Account), tuple(self.party\_account, self.party, d.reference\_name), as\_dict = true).
    - If not je\_accounts.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Journal Entry {1} does not have account {2} or already matched against another voucher”.format(d.idx, d.reference\_name, self.party\_account)).
    - Otherwise.
      - Set dr\_or\_cr from “debit” when self.payment\_type equals “Receive”, otherwise “credit”.
        - Value choice on self.payment\_type equals “Receive” — true gives “debit”, false gives “credit”.
      - Set valid from false.
      - For each jvd in je\_accounts.
        - If flt(jvd at dr\_or\_cr) &gt; 0.
          - Set valid from true.
      - If not valid.
        - Call the validation error handler Platform.throw(translated “Against Journal Entry {0} does not have any unmatched {1} entry”.format(d.reference\_name, translated dr\_or\_cr)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L112)

<a id="op-9cb0ed819994d8"></a>
### Payment Entry.update payment schedule

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_update_payment_schedule`

**Inputs** self, cancel = 0.

**Record and data access** read “Payment Schedule” via get\_all · read key at 2 via get\_value.

**State and service calls** execute a supplied database query.

**Explicit failure paths** validation helper — translated “Payment term {0} not used in {1}”.format(key at 0, key at 1) · validation helper — translated “Row #{0}: Cannot allocate more than {1} against payment term {2}”.format(idx, fmt\_money(outstanding), key at 0).

**Local steps**

- If not cancel.
  - Evaluate self.set\_payment\_term\_discounts().
- Set invoice\_payment\_amount\_map from mapping().
- Set invoice\_paid\_amount\_map from mapping().
- For each ref in self.get(“references”).
  - If (not ref.payment\_term or not ref.reference\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ref.payment\_term → not ref.reference\_name.
    - Continue with the next iteration or loop test.
  - Set key from tuple(ref.payment\_term, ref.reference\_name, ref.reference\_doctype).
  - Evaluate invoice\_payment\_amount\_map.setdefault(key, 0.0).
  - Update invoice\_payment\_amount\_map at key using + ref.allocated\_amount.
  - If not invoice\_paid\_amount\_map.get(key).
    - Set payment\_schedule from Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → ref.reference\_name), fields = list(“paid\_amount”, “payment\_amount”, “payment\_term”, “discount”, …)).
    - For each term in payment\_schedule.
      - Set invoice\_key from tuple(term.payment\_term, ref.reference\_name, ref.reference\_doctype).
      - Evaluate invoice\_paid\_amount\_map.setdefault(invoice\_key, mapping()).
      - Set invoice\_paid\_amount\_map at invoice\_key at “outstanding” from term.outstanding.
      - If (self.payment\_term\_discounts\_calculated or not (term.discount\_type and term.discount)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.payment\_term\_discounts\_calculated → not (term.discount\_type and term.discount).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in term.discount\_type → term.discount.
        - Continue with the next iteration or loop test.
      - If term.discount\_type equals “Percentage”.
        - Set invoice\_paid\_amount\_map at invoice\_key at “discounted\_amt” from (ref.total\_amount × (term.discount ÷ 100)).
      - Otherwise.
        - Set invoice\_paid\_amount\_map at invoice\_key at “discounted\_amt” from term.discount.
  - If (self.payment\_term\_discounts\_calculated and key belongs to invoice\_paid\_amount\_map).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_term\_discounts\_calculated → key belongs to invoice\_paid\_amount\_map.
    - Set invoice\_paid\_amount\_map at key at “discounted\_amt” from (invoice\_paid\_amount\_map at key.get(“discounted\_amt”, 0) + flt(ref.payment\_term\_discount)).
- For each tuple(idx, tuple(key, allocated\_amount)) in enumerate(invoice\_payment\_amount\_map.items(), 1).
  - If not invoice\_paid\_amount\_map.get(key).
    - Call the validation error handler Platform.throw(translated “Payment term {0} not used in {1}”.format(key at 0, key at 1)).
  - Set allocated\_amount from self.get\_allocated\_amount\_in\_transaction\_currency(allocated\_amount, key at 2, key at 1).
  - Set outstanding from flt(invoice\_paid\_amount\_map.get(key, mapping()).get(“outstanding”)).
  - Set discounted\_amt from flt(invoice\_paid\_amount\_map.get(key, mapping()).get(“discounted\_amt”)).
  - Set conversion\_rate from Platform.db.get\_value(key at 2, mapping(“name” → key at 1), “conversion\_rate”).
  - Set base\_paid\_amount\_precision from get\_field\_precision(Platform.get\_meta(“Payment Schedule”).get\_field(“base\_paid\_amount”)).
  - Set base\_outstanding\_precision from get\_field\_precision(Platform.get\_meta(“Payment Schedule”).get\_field(“base\_outstanding”)).
  - Set base\_paid\_amount from flt(((allocated\_amount − discounted\_amt) × conversion\_rate), base\_paid\_amount\_precision).
  - Set base\_outstanding from flt((allocated\_amount × conversion\_rate), base\_outstanding\_precision).
  - If cancel.
    - Evaluate Platform.db.sql(multiline text in the contract, tuple((allocated\_amount − discounted\_amt), base\_paid\_amount, discounted\_amt, allocated\_amount, …)).
  - Otherwise.
    - If allocated\_amount &gt; outstanding.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot allocate more than {1} against payment term {2}”.format(idx, fmt\_money(outstanding), key at 0)).
    - If (allocated\_amount and outstanding).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in allocated\_amount → outstanding.
      - Evaluate Platform.db.sql(multiline text in the contract, tuple((allocated\_amount − discounted\_amt), base\_paid\_amount, discounted\_amt, allocated\_amount, …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set payment term discounts](operations-064.md#op-fb98fe1d4cf2cb), [get allocated amount in transaction currency](operations-064.md#op-ebc79ada986398).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L103)

<a id="op-fb98fe1d4cf2cb"></a>
### Payment Entry.set payment term discounts

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_set_payment_term_discounts`

**Inputs** self.

**Record and data access** resolve a document from “Company” via get\_cached\_doc · resolve a document from expanded key via get\_doc.

**State and service calls** call db\_set on ref · call db\_set on self.

**Local steps**

- Set documents from mapping().
- Set remaining\_discounts from mapping().
- Set remaining\_deductions from mapping of row.name → max(0, (row.amount × negative 1 when self.payment\_type equals “Pay”, otherwise 1)) for row drawn from self.deductions where (not row.is\_exchange\_gain\_loss and not row.dunning).
  - Draw row from self.deductions, keep a combination only if ((not row.is\_exchange\_gain\_loss and not row.dunning)).
  - Value choice on self.payment\_type equals “Pay” — true gives negative 1, false gives 1.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.is\_exchange\_gain\_loss → not row.dunning.
- Set company from Platform.get\_cached\_doc(“Company”, self.company).
- For each ref in self.references.
  - Set ref.payment\_term\_discount from 0.
  - If (not ref.payment\_term or not ref.allocated\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not ref.payment\_term → not ref.allocated\_amount.
    - Continue with the next iteration or loop test.
  - Set key from tuple(ref.reference\_doctype, ref.reference\_name).
  - If key does not belong to documents.
    - Set documents at key from Platform.get\_doc(expanded key).
  - Set doc from documents at key.
  - Set term from next(generator of row for row drawn from doc.get(“payment\_schedule”, list()) where row.payment\_term equals ref.payment\_term, no value).
    - Draw row from doc.get(“payment\_schedule”, list()), keep a combination only if (row.payment\_term equals ref.payment\_term).
  - Set term\_key from tuple(expanded key, ref.payment\_term).
  - If term\_key does not belong to remaining\_discounts.
    - Set remaining\_discounts at term\_key from 0.
    - If (term and term.discount and not term.discounted\_amount and term.discount\_date and getdate((self.reference\_date or self.posting\_date)) ≤ getdate(term.discount\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in term → term.discount → not term.discounted\_amount → term.discount\_date → getdate((self.reference\_date or self.posting\_date)) ≤ getdate(term.discount\_date).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.reference\_date → self.posting\_date.
      - Set remaining\_discounts at term\_key from ((doc.grand\_total × term.discount) ÷ 100) when term.discount\_type equals “Percentage”, otherwise term.discount.
        - Value choice on term.discount\_type equals “Percentage” — true gives ((doc.grand\_total × term.discount) ÷ 100), false gives term.discount.
  - If not remaining\_discounts at term\_key.
    - Evaluate ref.db\_set(“payment\_term\_discount”, 0).
    - Continue with the next iteration or loop test.
  - Set discount from min(remaining\_discounts at term\_key, self.get\_allocated\_amount\_in\_transaction\_currency(ref.allocated\_amount, expanded key)).
  - Set discount\_accounts from set(company.default\_discount\_account, company.round\_off\_account).
  - Evaluate discount\_accounts.update(generator of row.account\_head for row drawn from doc.taxes).
    - Draw row from doc.taxes.
  - For each deduction in self.deductions.
    - If (deduction.account does not belong to discount\_accounts or deduction.name does not belong to remaining\_deductions).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in deduction.account does not belong to discount\_accounts → deduction.name does not belong to remaining\_deductions.
      - Continue with the next iteration or loop test.
    - Set amount from min(remaining\_deductions at deduction.name, (max(0, (discount − ref.payment\_term\_discount)) × doc.conversion\_rate)).
    - Update ref.payment\_term\_discount using + (amount ÷ doc.conversion\_rate).
    - Update remaining\_deductions at deduction.name using − amount.
  - Set ref.payment\_term\_discount from flt(ref.payment\_term\_discount, term.precision(“discounted\_amount”)).
  - Update remaining\_discounts at term\_key using − ref.payment\_term\_discount.
  - Evaluate ref.db\_set(“payment\_term\_discount”, ref.payment\_term\_discount).
- Evaluate self.db\_set(“payment\_term\_discounts\_calculated”, 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get allocated amount in transaction currency](operations-064.md#op-ebc79ada986398).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Company”, self.company).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L833)

<a id="op-ebc79ada986398"></a>
### Payment Entry.get allocated amount in transaction currency

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_allocated_amount_in_transaction_currency`

**Inputs** self, allocated\_amount, reference\_doctype, reference\_docname.

**Record and data access** read reference\_doctype via get\_value.

**Explicit results** allocated\_amount.

**Local steps**

- Set tuple(ref\_currency, ref\_exchange\_rate) from Platform.db.get\_value(reference\_doctype, reference\_docname, list(“currency”, “conversion\_rate”)).
- If self.party\_account\_currency equals ref\_currency.
  - Return allocated\_amount.
- Set allocated\_amount from flt((allocated\_amount ÷ ref\_exchange\_rate), self.precision(“total\_allocated\_amount”)).
- Return allocated\_amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L57)

<a id="op-cec3f4bf4f6aa7"></a>
### Payment Entry.set status

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_status`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If self.docstatus equals 2.
  - Set self.status from “Cancelled”.
- Otherwise.
  - <a id="op-cec3f4bf4f6aa7-guard-4"></a>If self.docstatus equals 1.
    - Set self.status from “Submitted”.
  - Otherwise.
    - Set self.status from “Draft”.
- If not self.is\_new().
  - Evaluate self.db\_set(“status”, self.status, update\_modified = true).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 1, self.docstatus = 1 (submitted) selects the branch that assigns “Submitted” to self.status. With self.docstatus = 0 (draft), the alternative assigns “Draft” to self.status. [Local guard](#op-cec3f4bf4f6aa7-guard-4)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L90)

<a id="op-8b25753da4b991"></a>
### Payment Entry.set total in words

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_total_in_words`

**Inputs** self.

**Local steps**

- Bind dependencies money\_in\_words.
- If self.payment\_type belongs to tuple(“Pay”, “Internal Transfer”).
  - Set base\_amount from abs(self.base\_paid\_amount).
  - Set amount from abs(self.paid\_amount).
  - Set currency from self.paid\_from\_account\_currency.
- Otherwise.
  - If self.payment\_type equals “Receive”.
    - Set base\_amount from abs(self.base\_received\_amount).
    - Set amount from abs(self.received\_amount).
    - Set currency from self.paid\_to\_account\_currency.
- Set self.base\_in\_words from money\_in\_words(base\_amount, self.company\_currency).
- Set self.in\_words from money\_in\_words(amount, currency).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L2506) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L94)

<a id="op-19f1aed3b88d25"></a>
### Payment Entry.apply taxes

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_apply_taxes`

**Inputs** self.

**Local steps**

- Evaluate self.initialize\_taxes().
- Evaluate self.determine\_exclusive\_rate().
- Evaluate self.calculate\_taxes().

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialize taxes](operations-066.md#op-072a4523789f03), [determine exclusive rate](operations-066.md#op-7c532e0c95abfe), [calculate taxes](operations-066.md#op-11f0f198901561).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L2825) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L48)

<a id="op-5375912c31b22f"></a>
### Payment Entry.set amounts

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_amounts`

**Inputs** self.

**Local steps**

- Evaluate self.set\_received\_amount().
- Evaluate self.set\_amounts\_in\_company\_currency().
- Evaluate self.set\_total\_allocated\_amount().
- Evaluate self.set\_unallocated\_amount().
- Evaluate self.set\_exchange\_gain\_loss().
- Evaluate self.set\_difference\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set received amount](operations-064.md#op-065220f14d0ebd), [set amounts in company currency](operations-065.md#op-f6be648945b021), [set total allocated amount](operations-065.md#op-43eb91a37ca582), [set unallocated amount](operations-065.md#op-63fd930372c0c1), [set exchange gain loss](operations-065.md#op-0172ce965c7f28), [set difference amount](operations-065.md#op-7df750f9314ae0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L2916) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1487) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L74)

<a id="op-44c320825e98ec"></a>
### Payment Entry.validate amounts

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_amounts`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_received\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate received amount](operations-064.md#op-b91372436e64a0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L3067) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1521) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L108)

<a id="op-b91372436e64a0"></a>
### Payment Entry.validate received amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_received_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Received Amount cannot be greater than Paid Amount”.

**Local steps**

- If self.paid\_from\_account\_currency equals self.paid\_to\_account\_currency.
  - If self.paid\_amount &lt; self.received\_amount.
    - Call the validation error handler Platform.throw(translated “Received Amount cannot be greater than Paid Amount”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L3118) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L118)

<a id="op-065220f14d0ebd"></a>
### Payment Entry.set received amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_received_amount`

**Inputs** self.

**Local steps**

- Set self.base\_received\_amount from self.base\_paid\_amount.
- If (self.paid\_from\_account\_currency equals self.paid\_to\_account\_currency and self.payment\_type differs from “Internal Transfer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.paid\_from\_account\_currency equals self.paid\_to\_account\_currency → self.payment\_type differs from “Internal Transfer”.
  - Set self.received\_amount from self.paid\_amount.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L3248) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L87)
