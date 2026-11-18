# Accounting and settlement · operations 65

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment entry

[Record definition](../../../../data/record-types/payment_entry.json)

<a id="op-01994b4527f906"></a>
### Payment Entry.set amounts after tax

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_amounts_after_tax`

**Inputs** self.

**Local steps**

- Set applicable\_tax from 0.
- Set base\_applicable\_tax from 0.
- For each tax in self.get(“taxes”).
  - If tax.included\_in\_paid\_amount.
    - Continue with the next iteration or loop test.
  - Set amount from (negative 1 × tax.tax\_amount) when tax.add\_deduct\_tax equals “Deduct”, otherwise tax.tax\_amount.
    - Value choice on tax.add\_deduct\_tax equals “Deduct” — true gives (negative 1 × tax.tax\_amount), false gives tax.tax\_amount.
  - Set base\_amount from (negative 1 × tax.base\_tax\_amount) when tax.add\_deduct\_tax equals “Deduct”, otherwise tax.base\_tax\_amount.
    - Value choice on tax.add\_deduct\_tax equals “Deduct” — true gives (negative 1 × tax.base\_tax\_amount), false gives tax.base\_tax\_amount.
  - Update applicable\_tax using + amount.
  - Update base\_applicable\_tax using + base\_amount.
- Set self.paid\_amount\_after\_tax from flt((flt(self.paid\_amount) + flt(applicable\_tax)), self.precision(“paid\_amount\_after\_tax”)).
- Set self.base\_paid\_amount\_after\_tax from flt((flt(self.paid\_amount\_after\_tax) × flt(self.source\_exchange\_rate)), self.precision(“base\_paid\_amount\_after\_tax”)).
- Set self.received\_amount\_after\_tax from flt((flt(self.received\_amount) + flt(applicable\_tax)), self.precision(“paid\_amount\_after\_tax”)).
- Set self.base\_received\_amount\_after\_tax from flt((flt(self.received\_amount\_after\_tax) × flt(self.target\_exchange\_rate)), self.precision(“base\_paid\_amount\_after\_tax”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L3376) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L75)

<a id="op-f6be648945b021"></a>
### Payment Entry.set amounts in company currency

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_amounts_in_company_currency`

**Inputs** self.

**Local steps**

- Set tuple(self.base\_paid\_amount, self.base\_received\_amount, self.difference\_amount) from tuple(0, 0, 0).
- If self.paid\_amount.
  - Set self.base\_paid\_amount from flt((flt(self.paid\_amount) × flt(self.source\_exchange\_rate)), self.precision(“base\_paid\_amount”)).
- If self.received\_amount.
  - Set self.base\_received\_amount from flt((flt(self.received\_amount) × flt(self.target\_exchange\_rate)), self.precision(“base\_received\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L3984) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L76)

<a id="op-b2d6460b0c755d"></a>
### Payment Entry.calculate base allocated amount for reference

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_calculate_base_allocated_amount_for_reference`

**Inputs** self, d.

**Declared result** float.

**Explicit results** base\_allocated\_amount.

**Local steps**

- Set base\_allocated\_amount from 0.
- If d.reference\_doctype belongs to get\_advance\_payment\_doctypes().
  - Set exchange\_rate from 1.
  - If self.payment\_type equals “Receive”.
    - Set exchange\_rate from self.source\_exchange\_rate.
  - Otherwise.
    - If self.payment\_type equals “Pay”.
      - Set exchange\_rate from self.target\_exchange\_rate.
  - Update base\_allocated\_amount using + flt((flt(d.allocated\_amount) × flt(exchange\_rate)), self.precision(“base\_paid\_amount”)).
- Otherwise.
  - Set exchange\_rate from 1.
  - If self.payment\_type equals “Receive”.
    - Set exchange\_rate from self.source\_exchange\_rate.
  - Otherwise.
    - If self.payment\_type equals “Pay”.
      - Set exchange\_rate from self.target\_exchange\_rate.
  - Update base\_allocated\_amount using + flt((flt(d.allocated\_amount) × flt(exchange\_rate)), self.precision(“base\_paid\_amount”)).
  - If d.exchange\_rate is identical to no value.
    - Set d.exchange\_rate from 1.
  - Set allocated\_amount\_in\_ref\_exchange\_rate from flt((flt(d.allocated\_amount) × flt(d.exchange\_rate)), self.precision(“base\_paid\_amount”)).
  - Set d.exchange\_gain\_loss from (base\_allocated\_amount − allocated\_amount\_in\_ref\_exchange\_rate).
- Return base\_allocated\_amount.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L4276) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L51)

<a id="op-43eb91a37ca582"></a>
### Payment Entry.set total allocated amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_total_allocated_amount`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-43eb91a37ca582-guard-2"></a>If self.payment\_type equals “Internal Transfer”.
  - Return no value.
- Set tuple(total\_allocated\_amount, base\_total\_allocated\_amount) from tuple(0, 0).
- For each d in self.get(“references”).
  - If d.allocated\_amount.
    - Update total\_allocated\_amount using + flt(d.allocated\_amount).
    - Update base\_total\_allocated\_amount using + self.calculate\_base\_allocated\_amount\_for\_reference(d).
- Set self.total\_allocated\_amount from flt(abs(total\_allocated\_amount), self.precision(“total\_allocated\_amount”)).
- Set self.base\_total\_allocated\_amount from flt(abs(base\_total\_allocated\_amount), self.precision(“base\_total\_allocated\_amount”)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.payment\_type equals “Internal Transfer”, self.payment\_type = “Internal Transfer” selects the branch that returns no value. With self.payment\_type = “Receive”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-43eb91a37ca582-guard-2)

**Methods declared on this owner** [calculate base allocated amount for reference](operations-065.md#op-b2d6460b0c755d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0077.json#L4890) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L93)

<a id="op-63fd930372c0c1"></a>
### Payment Entry.set unallocated amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_unallocated_amount`

**Inputs** self.

**Local steps**

- Set self.unallocated\_amount from flt((max(self.get\_base\_unallocated\_amount(), 0) ÷ self.get\_exchange\_rate()), get\_field\_precision(self.meta.get\_field(“unallocated\_amount”), self, currency = self.party\_account\_currency)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get base unallocated amount](operations-065.md#op-3a33b350302b05), [get exchange rate](operations-066.md#op-bb0cd956198c78).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L96)

<a id="op-3a33b350302b05"></a>
### Payment Entry.get base unallocated amount

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_get_base_unallocated_amount`

**Inputs** self.

**Explicit results** 0 · (amount − self.get\_included\_taxes()).

**Local steps**

- If (not self.party or self.payment\_type equals “Internal Transfer”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.party → self.payment\_type equals “Internal Transfer”.
  - Return 0.
- Set deductions from sum(generator of flt(row.amount) for row drawn from self.deductions where not row.is\_exchange\_gain\_loss).
  - Draw row from self.deductions, keep a combination only if (not row.is\_exchange\_gain\_loss).
- If self.payment\_type equals “Receive”.
  - Set amount from ((self.base\_paid\_amount + deductions) − self.base\_total\_allocated\_amount).
- Otherwise.
  - Set amount from ((self.base\_received\_amount − deductions) − self.base\_total\_allocated\_amount).
- Return (amount − self.get\_included\_taxes()).

**Methods declared on this owner** [get included taxes](operations-065.md#op-420de7069c3599).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L831)

<a id="op-f57226a1489eec"></a>
### Payment Entry.get unallocated amount rounding

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_get_unallocated_amount_rounding`

**Inputs** self.

**Explicit results** 0 · flt((rounding × negative 1 when self.payment\_type equals “Pay”, otherwise 1), self.precision(“difference\_amount”)).

**Local steps**

- Set base\_unallocated\_amount from self.get\_base\_unallocated\_amount().
- Set rounding from (base\_unallocated\_amount − (self.unallocated\_amount × self.get\_exchange\_rate())).
- If (rounding &lt; 0 and self.total\_allocated\_amount &gt; flt(((self.base\_total\_allocated\_amount + base\_unallocated\_amount) ÷ self.get\_exchange\_rate()), get\_field\_precision(nested operand in the contract.meta.get\_fi ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rounding &lt; 0 → self.total\_allocated\_amount &gt; flt(((self.base\_total\_allocated\_amount + base\_unallocated\_amount) ÷ self.get\_exchange\_rate()), get\_field\_precision(self.meta.get\_field(“unallocated\_amount”), self, currency =  ….
  - Return 0.
- Return flt((rounding × negative 1 when self.payment\_type equals “Pay”, otherwise 1), self.precision(“difference\_amount”)).
  - Value choice on self.payment\_type equals “Pay” — true gives negative 1, false gives 1.

**Methods declared on this owner** [get base unallocated amount](operations-065.md#op-3a33b350302b05), [get exchange rate](operations-066.md#op-bb0cd956198c78).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L832)

<a id="op-0172ce965c7f28"></a>
### Payment Entry.set exchange gain loss

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_exchange_gain_loss`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** msgprint with translated “Please set {0} in Company {1} to account for Exchange Gain / Loss”.format(label, get\_link\_to\_form(“Company”, self.company)).

**Explicit results** no value · Platform.msgprint(translated “Please set {0} in Company {1} to account for Exchange Gain / Loss”.format(label, get\_link\_to\_form(“Company”, self.company)), title = translated “Missing Default in Company”, i ….

**Local steps**

- Set exchange\_gain\_loss from flt((self.base\_paid\_amount − self.base\_received\_amount), self.precision(“amount”, “deductions”)).
- Set exchange\_gain\_loss\_rows from list of row for row drawn from self.get(“deductions”) where row.is\_exchange\_gain\_loss.
  - Draw row from self.get(“deductions”), keep a combination only if (row.is\_exchange\_gain\_loss).
- Set exchange\_gain\_loss\_row from exchange\_gain\_loss\_rows.pop(0) when exchange\_gain\_loss\_rows, otherwise no value.
  - Value choice on exchange\_gain\_loss\_rows — true gives exchange\_gain\_loss\_rows.pop(0), false gives no value.
- For each row in exchange\_gain\_loss\_rows.
  - Evaluate self.remove(row).
- If not exchange\_gain\_loss.
  - If exchange\_gain\_loss\_row.
    - Evaluate self.remove(exchange\_gain\_loss\_row).
  - Return no value.
- If not exchange\_gain\_loss\_row.
  - Set values from Platform.get\_cached\_value(“Company”, self.company, tuple(“exchange\_gain\_loss\_account”, “cost\_center”), as\_dict = true).
  - For each tuple(fieldname, value) in values.items().
    - If value.
      - Continue with the next iteration or loop test.
    - Set label from translated Platform.get\_meta(“Company”).get\_label(fieldname).
    - Return Platform.msgprint(translated “Please set {0} in Company {1} to account for Exchange Gain / Loss”.format(label, get\_link\_to\_form(“Company”, self.company)), title = translated “Missing Default in Company”, i ….
      - Value choice on self.docstatus.is\_submitted() — true gives “red”, false gives “yellow”.
  - Set exchange\_gain\_loss\_row from self.append(“deductions”, mapping(“account” → values.exchange\_gain\_loss\_account, “cost\_center” → values.cost\_center, “is\_exchange\_gain\_loss” → 1)).
- Set exchange\_gain\_loss\_row.amount from exchange\_gain\_loss.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, tuple(“exchange\_gain\_loss\_account”, “cost\_center”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L79)

<a id="op-7df750f9314ae0"></a>
### Payment Entry.set difference amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_difference_amount`

**Inputs** self.

**Local steps**

- Set base\_unallocated\_amount from (flt(self.unallocated\_amount) × flt(self.source\_exchange\_rate) when self.payment\_type equals “Receive”, otherwise flt(self.target\_exchange\_rate)).
  - Value choice on self.payment\_type equals “Receive” — true gives flt(self.source\_exchange\_rate), false gives flt(self.target\_exchange\_rate).
- Set base\_party\_amount from (flt(self.base\_total\_allocated\_amount) + flt(base\_unallocated\_amount)).
- Set included\_taxes from self.get\_included\_taxes().
- If self.payment\_type equals “Receive”.
  - Set self.difference\_amount from ((base\_party\_amount − self.base\_received\_amount) + included\_taxes).
- Otherwise.
  - If self.payment\_type equals “Pay”.
    - Set self.difference\_amount from ((self.base\_paid\_amount − base\_party\_amount) − included\_taxes).
  - Otherwise.
    - Set self.difference\_amount from ((self.base\_paid\_amount − flt(self.base\_received\_amount)) − included\_taxes).
- Set total\_deductions from sum(generator of flt(d.amount) for d drawn from self.get(“deductions”)).
  - Draw d from self.get(“deductions”).
- Set self.difference\_amount from flt(((self.difference\_amount − total\_deductions) + self.get\_unallocated\_amount\_rounding()), self.precision(“difference\_amount”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get included taxes](operations-065.md#op-420de7069c3599), [get unallocated amount rounding](operations-065.md#op-f57226a1489eec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L78)

<a id="op-420de7069c3599"></a>
### Payment Entry.get included taxes

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_included_taxes`

**Inputs** self.

**Explicit results** included\_taxes.

**Local steps**

- Set included\_taxes from 0.
- For each tax in self.get(“taxes”).
  - If not tax.included\_in\_paid\_amount.
    - Continue with the next iteration or loop test.
  - If tax.add\_deduct\_tax equals “Add”.
    - Update included\_taxes using + flt(tax.base\_tax\_amount).
  - Otherwise.
    - Update included\_taxes using − flt(tax.base\_tax\_amount).
- Return included\_taxes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L62)

<a id="op-0ed028c1ef1e5a"></a>
### Payment Entry.clear unallocated reference document rows

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_clear_unallocated_reference_document_rows`

**Inputs** self.

**State and service calls** execute query text (DELETE, Payment Entry Reference).

**Local steps**

- Evaluate self.set(“references”, self.get(“references”, mapping(“allocated\_amount” → list(“not in”, list(0, no value, empty text))))).
- If not self.is\_new().
  - Evaluate Platform.db.sql(query text (DELETE, Payment Entry Reference), self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L54)

<a id="op-bf56c19143e854"></a>
### Payment Entry.set title

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_title`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_import and self.title).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_import → self.title.
  - Return no value.
- If self.payment\_type belongs to tuple(“Receive”, “Pay”).
  - Set self.title from self.party.
- Otherwise.
  - Set self.title from ((self.paid\_from + “ - ”) + self.paid\_to).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L397) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L92)

<a id="op-6433bf54aa848b"></a>
### Payment Entry.validate transaction reference

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_validate_transaction_reference`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Reference No and Reference Date is mandatory for Bank transaction”.

**Local steps**

- Set bank\_account from self.paid\_to when self.payment\_type equals “Receive”, otherwise self.paid\_from.
  - Value choice on self.payment\_type equals “Receive” — true gives self.paid\_to, false gives self.paid\_from.
- Set bank\_account\_type from Platform.get\_cached\_value(“Account”, bank\_account, “account\_type”).
- If bank\_account\_type equals “Bank”.
  - If (not self.reference\_no or not self.reference\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.reference\_no → not self.reference\_date.
    - Call the validation error handler Platform.throw(translated “Reference No and Reference Date is mandatory for Bank transaction”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, bank\_account, “account\_type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L563) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L120)

<a id="op-52d904fb7430cd"></a>
### Payment Entry.set remarks

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_remarks`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.custom\_remarks.
  - Return no value.
- If self.payment\_type equals “Internal Transfer”.
  - Set remarks from list(translated “Amount {0} {1} transferred from {2} to {3}”.format(translated self.paid\_from\_account\_currency, self.paid\_amount, self.paid\_from, self.paid\_to)).
- Otherwise.
  - Set remarks from list(translated “Amount {0} {1} {2} {3}”.format(translated self.paid\_from\_account\_currency when self.payment\_type equals “Receive”, otherwise translated self.paid\_to\_account\_currency, self.paid\_amount when self …).
    - Value choice on self.payment\_type equals “Receive” — true gives translated self.paid\_from\_account\_currency, false gives translated self.paid\_to\_account\_currency.
    - Value choice on self.payment\_type equals “Receive” — true gives self.paid\_amount, false gives self.received\_amount.
    - Value choice on self.payment\_type equals “Receive” — true gives translated “received from”, false gives translated “paid to”.
- If self.reference\_no.
  - Evaluate remarks.append(translated “Transaction reference no {0} dated {1}”.format(self.reference\_no, self.reference\_date)).
- If self.payment\_type belongs to list(“Receive”, “Pay”).
  - For each d in self.get(“references”).
    - If d.allocated\_amount.
      - Evaluate remarks.append(translated “Amount {0} {1} adjusted against {2} {3}”.format(translated self.party\_account\_currency, d.allocated\_amount, d.reference\_doctype, d.reference\_name)).
- For each d in self.get(“deductions”).
  - If d.amount.
    - Evaluate remarks.append(translated “Amount {0} {1} as adjustment to {2}”.format(translated self.company\_currency, d.amount, d.account)).
- Evaluate self.set(“remarks”, whitespace '\\n'.join(remarks)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L792) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L88)

<a id="op-62679812682750"></a>
### Payment Entry.set transaction currency and rate

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_set_transaction_currency_and_rate`

**Inputs** self.

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(self.company).
- Set self.transaction\_currency from company\_currency.
- Set self.transaction\_exchange\_rate from 1.
- If self.paid\_from\_account\_currency differs from company\_currency.
  - Set self.transaction\_currency from self.paid\_from\_account\_currency.
  - Set self.transaction\_exchange\_rate from self.source\_exchange\_rate.
- Otherwise.
  - If self.paid\_to\_account\_currency differs from company\_currency.
    - Set self.transaction\_currency from self.paid\_to\_account\_currency.
    - Set self.transaction\_exchange\_rate from self.target\_exchange\_rate.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L1604) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L95)

<a id="op-2d089e6f9241bc"></a>
### Payment Entry.build gl map

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_build_general_ledger_map`

**Inputs** self.

**Explicit results** gl\_entries.

**Local steps**

- If (self.payment\_type belongs to tuple(“Receive”, “Pay”) and not self.get(“party\_account\_field”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.payment\_type belongs to tuple(“Receive”, “Pay”) → not self.get(“party\_account\_field”).
  - Evaluate self.setup\_party\_account\_field().
- Evaluate self.set\_transaction\_currency\_and\_rate().
- Set gl\_entries from list().
- Evaluate self.add\_party\_gl\_entries(gl\_entries).
- Evaluate self.add\_bank\_gl\_entries(gl\_entries).
- Evaluate self.add\_deductions\_gl\_entries(gl\_entries).
- Evaluate self.add\_tax\_gl\_entries(gl\_entries).
- Evaluate add\_regional\_gl\_entries(gl\_entries, self).
- If rounding bound to self.get\_unallocated\_amount\_rounding().
  - Evaluate make\_round\_off\_gle(gl\_entries, rounding, (rounding ÷ self.transaction\_exchange\_rate), self.precision(“difference\_amount”)).
- Evaluate self.set\_transaction\_currency\_and\_rate\_in\_gl\_map(gl\_entries).
- Return gl\_entries.

**Methods declared on this owner** [setup party account field](operations-063.md#op-fd22c476001a12), [set transaction currency and rate](operations-065.md#op-62679812682750), [add party gl entries](operations-065.md#op-7787cccb6960a6), [add bank gl entries](operations-065.md#op-e582d352458570), [add deductions gl entries](operations-066.md#op-6d60f02cfb1947), [add tax gl entries](operations-066.md#op-a2b3d9b29619ac), [get unallocated amount rounding](operations-065.md#op-f57226a1489eec), [set transaction currency and rate in gl map](operations-065.md#op-ec64043bff708c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L50)

<a id="op-ec64043bff708c"></a>
### Payment Entry.set transaction currency and rate in gl map

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_set_transaction_currency_and_rate_in_gl_map`

**Inputs** self, gl\_entries.

**Local steps**

- For each gle in gl\_entries.
  - Evaluate gle.setdefault(“transaction\_currency”, self.transaction\_currency).
  - Evaluate gle.setdefault(“transaction\_exchange\_rate”, self.transaction\_exchange\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L834)

<a id="op-7d45e904c8a49f"></a>
### Payment Entry.make gl entries

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_make_general_ledger_entries`

**Inputs** self, cancel = 0, adv\_adj = 0.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Set gl\_entries from self.build\_gl\_map().
- Set merge\_entries from Platform.get\_single\_value(“Accounts Settings”, “merge\_similar\_account\_heads”).
- Set gl\_entries from process\_gl\_map(gl\_entries, merge\_entries = merge\_entries).
- Evaluate make\_gl\_entries(gl\_entries, cancel = cancel, adv\_adj = adv\_adj, merge\_entries = merge\_entries).
- If cancel.
  - Evaluate cancel\_exchange\_gain\_loss\_journal(Platform.\_dict(doctype = self.doctype, name = self.name)).
- Otherwise.
  - Evaluate self.make\_exchange\_gain\_loss\_journal().
- Evaluate self.make\_advance\_gl\_entries(cancel = cancel).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build gl map](operations-065.md#op-2d089e6f9241bc), [make advance gl entries](operations-065.md#op-4c0416c0f0e618).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “merge\_similar\_account\_heads”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L1912) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1482) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L69)

<a id="op-7787cccb6960a6"></a>
### Payment Entry.add party gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_add_party_gl_entries`

**Inputs** self, gl\_entries.

**Record and data access** read “Party Type” via get\_value · read d.reference\_doctype via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.party\_account.
  - Return no value.
- Set advance\_payment\_doctypes from get\_advance\_payment\_doctypes().
- If self.payment\_type equals “Receive”.
  - Set against\_account from self.paid\_to.
- Otherwise.
  - Set against\_account from self.paid\_from.
- Set party\_account\_type from Platform.db.get\_value(“Party Type”, self.party\_type, “account\_type”).
- Set party\_gl\_dict from self.get\_gl\_dict(mapping(“account” → self.party\_account, “party\_type” → self.party\_type, “party” → self.party, “against” → against\_account, …), item = self).
- For each d in self.get(“references”).
  - Set dr\_or\_cr from “credit” when self.payment\_type equals “Receive”, otherwise “debit”.
    - Value choice on self.payment\_type equals “Receive” — true gives “credit”, false gives “debit”.
  - Set cost\_center from self.cost\_center.
  - If (d.reference\_doctype equals “Sales Invoice” and not cost\_center).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_doctype equals “Sales Invoice” → not cost\_center.
    - Set cost\_center from Platform.db.get\_value(d.reference\_doctype, d.reference\_name, “cost\_center”).
  - Set gle from party\_gl\_dict.copy().
  - Set allocated\_amount\_in\_company\_currency from self.calculate\_base\_allocated\_amount\_for\_reference(d).
  - If (d.reference\_doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) and d.allocated\_amount &lt; 0 and ((party\_account\_type equals “Receivable” and self.payment\_type equals “Pay”) or (party\_account\_type  ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) → d.allocated\_amount &lt; 0 → ((party\_account\_type equals “Receivable” and self.payment\_type equals “Pay”) or (party\_account\_type equals “Payable” and self.payment\_type equals “Receive”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (party\_account\_type equals “Receivable” and self.payment\_type equals “Pay”) → (party\_account\_type equals “Payable” and self.payment\_type equals “Receive”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account\_type equals “Receivable” → self.payment\_type equals “Pay”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account\_type equals “Payable” → self.payment\_type equals “Receive”.
    - Set dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
      - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
  - Evaluate gle.update(self.get\_gl\_dict(mapping(“account” → self.party\_account, “party\_type” → self.party\_type, “party” → self.party, “against” → against\_account, …), item = self)).
    - Value choice on self.transaction\_currency equals self.party\_account\_currency — true gives d.allocated\_amount, false gives (allocated\_amount\_in\_company\_currency ÷ self.transaction\_exchange\_rate).
  - If d.reference\_doctype belongs to advance\_payment\_doctypes.
    - Evaluate gle.update(mapping(“against\_voucher\_type” → self.doctype, “against\_voucher” → self.name, “advance\_voucher\_type” → d.reference\_doctype, “advance\_voucher\_no” → d.reference\_name)).
  - Otherwise.
    - If self.book\_advance\_payments\_in\_separate\_party\_account.
      - Evaluate gle.update(mapping(“against\_voucher\_type” → self.doctype, “against\_voucher” → self.name)).
    - Otherwise.
      - Evaluate gle.update(mapping(“against\_voucher\_type” → d.reference\_doctype, “against\_voucher” → d.reference\_name)).
  - Evaluate gl\_entries.append(gle).
- If self.unallocated\_amount.
  - Set dr\_or\_cr from “credit” when self.payment\_type equals “Receive”, otherwise “debit”.
    - Value choice on self.payment\_type equals “Receive” — true gives “credit”, false gives “debit”.
  - Set exchange\_rate from self.get\_exchange\_rate().
  - Set base\_unallocated\_amount from (self.unallocated\_amount × exchange\_rate).
  - Set gle from party\_gl\_dict.copy().
  - Evaluate gle.update(self.get\_gl\_dict(mapping(“account” → self.party\_account, “party\_type” → self.party\_type, “party” → self.party, “against” → against\_account, …), item = self)).
    - Value choice on self.party\_account\_currency equals self.transaction\_currency — true gives self.unallocated\_amount, false gives (base\_unallocated\_amount ÷ self.transaction\_exchange\_rate).
  - If self.book\_advance\_payments\_in\_separate\_party\_account.
    - Evaluate gle.update(mapping(“against\_voucher\_type” → “Payment Entry”, “against\_voucher” → self.name)).
  - Evaluate gl\_entries.append(gle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate base allocated amount for reference](operations-065.md#op-b2d6460b0c755d), [get exchange rate](operations-066.md#op-bb0cd956198c78).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L829)

<a id="op-4c0416c0f0e618"></a>
### Payment Entry.make advance gl entries

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_make_advance_general_ledger_entries`

**Inputs** self, entry = no value, cancel = 0, update\_outstanding = “Yes”.

**Local steps**

- Evaluate self.set\_transaction\_currency\_and\_rate().
- Set gl\_entries from list().
- Evaluate self.add\_advance\_gl\_entries(gl\_entries, entry).
- If cancel.
  - Evaluate make\_reverse\_gl\_entries(gl\_entries, partial\_cancel = true).
- Otherwise.
  - Evaluate make\_gl\_entries(gl\_entries, update\_outstanding = update\_outstanding).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set transaction currency and rate](operations-065.md#op-62679812682750), [add advance gl entries](operations-065.md#op-189457753dd994).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L2246) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L68)

<a id="op-189457753dd994"></a>
### Payment Entry.add advance gl entries

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_add_advance_general_ledger_entries`

**Inputs** self, gl\_entries, entry.

**Local steps**

- If self.book\_advance\_payments\_in\_separate\_party\_account.
  - Set references from list of x for x drawn from self.get(“references”).
    - Draw x from self.get(“references”).
  - If entry.
    - Set references from list of x for x drawn from self.get(“references”) where x.name equals entry.name.
      - Draw x from self.get(“references”), keep a combination only if (x.name equals entry.name).
  - For each ref in references.
    - If ref.reference\_doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”, “Journal Entry”, “Payment Entry”).
      - Evaluate self.add\_advance\_gl\_for\_reference(gl\_entries, ref).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add advance gl for reference](operations-065.md#op-c41a8a008d56e9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L2471) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L44)

<a id="op-b55013ff15d813"></a>
### Payment Entry.get dr and account for advances

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_get_debit_and_account_for_advances`

**Inputs** self, reference.

**Explicit results** tuple(“credit”, reference.account) · tuple(“debit”, reference.account) · tuple(“credit”, self.party\_account) · tuple(“debit”, self.party\_account).

**Local steps**

- If reference.reference\_doctype equals “Sales Invoice”.
  - Return tuple(“credit”, reference.account).
- If reference.reference\_doctype equals “Purchase Invoice”.
  - Return tuple(“debit”, reference.account).
- If reference.reference\_doctype equals “Payment Entry”.
  - If (reference.account\_type equals “Receivable” and reference.payment\_type equals “Pay”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference.account\_type equals “Receivable” → reference.payment\_type equals “Pay”.
    - Return tuple(“credit”, self.party\_account).
  - Otherwise.
    - Return tuple(“debit”, self.party\_account).
- If reference.reference\_doctype equals “Journal Entry”.
  - If (self.party\_type equals “Customer” and self.payment\_type equals “Receive”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_type equals “Customer” → self.payment\_type equals “Receive”.
    - Return tuple(“credit”, reference.account).
  - Otherwise.
    - Return tuple(“debit”, reference.account).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L2808) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L60)

<a id="op-c41a8a008d56e9"></a>
### Payment Entry.add advance gl for reference

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_payment_entry_add_advance_general_ledger_for_reference`

**Inputs** self, gl\_entries, invoice.

**State and service calls** request set\_value on “Payment Entry Reference”.

**Local steps**

- Set args\_dict from mapping(“party\_type” → self.party\_type, “party” → self.party, “account\_currency” → self.party\_account\_currency, “cost\_center” → self.cost\_center, …).
- If invoice.reconcile\_effect\_on.
  - Set posting\_date from invoice.reconcile\_effect\_on.
- Otherwise.
  - Set posting\_date from get\_reconciliation\_effect\_date(invoice.reference\_doctype, invoice.reference\_name, self.company, self.posting\_date).
  - Evaluate Platform.db.set\_value(“Payment Entry Reference”, invoice.name, “reconcile\_effect\_on”, posting\_date).
- Set tuple(dr\_or\_cr, account) from self.get\_dr\_and\_account\_for\_advances(invoice).
- Set base\_allocated\_amount from self.calculate\_base\_allocated\_amount\_for\_reference(invoice).
- Set args\_dict at “account” from account.
- Set args\_dict at dr\_or\_cr from base\_allocated\_amount.
- Set args\_dict at (dr\_or\_cr + “\_in\_account\_currency”) from invoice.allocated\_amount.
- Set args\_dict at (dr\_or\_cr + “\_in\_transaction\_currency”) from invoice.allocated\_amount when self.party\_account\_currency equals self.transaction\_currency, otherwise (base\_allocated\_amount ÷ self.transaction\_exchange\_rate).
  - Value choice on self.party\_account\_currency equals self.transaction\_currency — true gives invoice.allocated\_amount, false gives (base\_allocated\_amount ÷ self.transaction\_exchange\_rate).
- Evaluate args\_dict.update(mapping(“against\_voucher\_type” → invoice.reference\_doctype, “against\_voucher” → invoice.reference\_name, “advance\_voucher\_type” → invoice.advance\_voucher\_type, “advance\_voucher\_no” → invoic ….
- Set gle from self.get\_gl\_dict(args\_dict, item = self).
- Evaluate gl\_entries.append(gle).
- Set args\_dict at dr\_or\_cr from 0.
- Set args\_dict at (dr\_or\_cr + “\_in\_account\_currency”) from 0.
- Set dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
  - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
- Set args\_dict at “account” from self.party\_account.
- Set args\_dict at dr\_or\_cr from base\_allocated\_amount.
- Set args\_dict at (dr\_or\_cr + “\_in\_account\_currency”) from invoice.allocated\_amount.
- Set args\_dict at (dr\_or\_cr + “\_in\_transaction\_currency”) from invoice.allocated\_amount when self.party\_account\_currency equals self.transaction\_currency, otherwise (base\_allocated\_amount ÷ self.transaction\_exchange\_rate).
  - Value choice on self.party\_account\_currency equals self.transaction\_currency — true gives invoice.allocated\_amount, false gives (base\_allocated\_amount ÷ self.transaction\_exchange\_rate).
- Evaluate args\_dict.update(mapping(“against\_voucher\_type” → “Payment Entry”, “against\_voucher” → self.name, “advance\_voucher\_type” → invoice.advance\_voucher\_type, “advance\_voucher\_no” → invoice.advance\_voucher\_no)).
- Set gle from self.get\_gl\_dict(args\_dict, item = self).
- Evaluate gl\_entries.append(gle).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get dr and account for advances](operations-065.md#op-b55013ff15d813), [calculate base allocated amount for reference](operations-065.md#op-b2d6460b0c755d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0078.json#L3230) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L45)

<a id="op-e582d352458570"></a>
### Payment Entry.add bank gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_paymententry_add_bank_gl_entries`

**Inputs** self, gl\_entries.

**Local steps**

- If self.payment\_type belongs to tuple(“Pay”, “Internal Transfer”).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.paid\_from, “account\_currency” → self.paid\_from\_account\_currency, “against” → self.party when self.payment\_type equals “Pay”, otherwise self.paid\_ ….
    - Value choice on self.payment\_type equals “Pay” — true gives self.party, false gives self.paid\_to.
    - Value choice on self.paid\_from\_account\_currency equals self.transaction\_currency — true gives self.paid\_amount, false gives (self.base\_paid\_amount ÷ self.transaction\_exchange\_rate).
- If self.payment\_type belongs to tuple(“Receive”, “Internal Transfer”).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.paid\_to, “account\_currency” → self.paid\_to\_account\_currency, “against” → self.party when self.payment\_type equals “Receive”, otherwise self.paid\_ ….
    - Value choice on self.payment\_type equals “Receive” — true gives self.party, false gives self.paid\_from.
    - Value choice on self.paid\_to\_account\_currency equals self.transaction\_currency — true gives self.received\_amount, false gives (self.base\_received\_amount ÷ self.transaction\_exchange\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L827)
