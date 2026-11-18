# Accounting and settlement · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Dunning

[Record definition](../../../../data/record-types/dunning.json)

<a id="op-460cb59076c542"></a>
### Dunning.validate currency

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_dunning_validate_currency`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Conversion Rate from {0} to {1} must be greater than zero.”.format(self.currency, self.company\_currency).

**Local steps**

- Set self.currency from (self.currency or self.company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.currency → self.company\_currency.
- If self.currency equals self.company\_currency.
  - Set self.conversion\_rate from 1.
- Otherwise.
  - If (not self.conversion\_rate or (self.get\_doc\_before\_save() and not self.has\_value\_changed(“conversion\_rate”) and any(generator of self.has\_value\_changed(field) for field drawn from tuple(“currency”, “company ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.conversion\_rate → (self.get\_doc\_before\_save() and not self.has\_value\_changed(“conversion\_rate”) and any(generator of self.has\_value\_changed(field) for field drawn from tuple(“currency”, “company”, “posting\_date”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get\_doc\_before\_save() → not self.has\_value\_changed(“conversion\_rate”) → any(generator of self.has\_value\_changed(field) for field drawn from tuple(“currency”, “company”, “posting\_date”)).
    - Draw field from tuple(“currency”, “company”, “posting\_date”).
    - Set self.conversion\_rate from get\_exchange\_rate(self.currency, self.company\_currency, self.posting\_date, “for\_selling”).
- If flt(self.conversion\_rate) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Conversion Rate from {0} to {1} must be greater than zero.”.format(self.currency, self.company\_currency)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L789)

<a id="op-ddd9db6b63c87d"></a>
### Dunning.before submit

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_dunning_before_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Income Account is required to collect dunning fees or interest.”.

**Local steps**

- If (self.dunning\_amount and not self.income\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.dunning\_amount → not self.income\_account.
  - Call the validation error handler Platform.throw(translated “Income Account is required to collect dunning fees or interest.”).
- Set self.status from “Unresolved”.
- Set self.superseded\_by from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L786)

<a id="op-90f179a081118c"></a>
### Dunning.set dunning fee

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_dunning_set_dunning_fee`

**Inputs** self.

**Record and data access** read “Dunning Type” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Conversion Rate must be greater than zero.”.

**Local steps**

- If not self.dunning\_type.
  - Set self.dunning\_fee from flt(self.dunning\_fee).
  - Return no value.
- Set default\_fee from flt(Platform.get\_cached\_value(“Dunning Type”, self.dunning\_type, “dunning\_fee”)).
- Set previous from self.get\_doc\_before\_save().
- If (self.dunning\_fee is identical to no value or (previous and previous.dunning\_type equals self.dunning\_type and previous.dunning\_fee equals self.dunning\_fee and flt(previous.conversion\_rate) &gt; 0 and previou ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.dunning\_fee is identical to no value → (previous and previous.dunning\_type equals self.dunning\_type and previous.dunning\_fee equals self.dunning\_fee and flt(previous.conversion\_rate) &gt; 0 and previous.conversion\_rate differs from self.conversion ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.dunning\_type equals self.dunning\_type → previous.dunning\_fee equals self.dunning\_fee → flt(previous.conversion\_rate) &gt; 0 → previous.conversion\_rate differs from self.conversion\_rate → previous.dunning\_fee equals flt((default\_fee ÷ previous.conversion\_rate), self.precision(“dunning\_fee”)).
  - If flt(self.conversion\_rate) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Conversion Rate must be greater than zero.”).
  - Set self.dunning\_fee from flt((default\_fee ÷ self.conversion\_rate), self.precision(“dunning\_fee”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Dunning Type”, self.dunning\_type, “dunning\_fee”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L788)

<a id="op-cad8b56f60213a"></a>
### Dunning.validate overdue payment references

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_dunning_validate_overdue_payment_references`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_list · read “Payment Schedule” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Select an accessible, submitted Sales Invoice.”.format(row.idx) · validation helper — translated “Row #{0}: Sales Invoice {1} must have the same {2} as this Dunning.”.format(row.idx, row.sales\_invoice, translated self.meta.get\_label(field)) · validation helper — translated “Row #{0}: Payment Schedule must belong to the selected Sales Invoice.”.format(row.idx) · validation helper — translated “Row #{0}: {1} is already included in this Dunning.”.format(row.idx, reference\_type) · validation helper — translated “Row #{0}: {1} must match the Payment Schedule.”.format(row.idx, translated row.meta.get\_label(field)) · 3 additional forms in the steps below.

**Local steps**

- If not self.overdue\_payments.
  - Return no value.
- Set invoices from mapping of invoice.name → invoice for invoice drawn from Platform.get\_list(“Sales Invoice”, filters = mapping(“name” → tuple(“in”, set of row.sales\_invoice for row drawn from self.overdue\_payments)), field ….
  - Draw invoice from Platform.get\_list(“Sales Invoice”, filters = mapping(“name” → tuple(“in”, set of row.sales\_invoice for row drawn from self.overdue\_payments)), fields = list(“name”, “customer”, “company”, “currency”, …), l ….
  - Draw row from self.overdue\_payments.
- Set schedules from mapping of schedule.name → schedule for schedule drawn from Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → tuple(“in”, list(invoices)), “parenttype” → “Sales Invoice”, “parentfield” → “p ….
  - Value choice on invoices — true gives mapping of schedule.name → schedule for schedule drawn from Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → tuple(“in”, list(invoices)), “parenttype” → “Sales Invoice”, “parentfield” → “p …, false gives mapping().
  - Draw schedule from Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → tuple(“in”, list(invoices)), “parenttype” → “Sales Invoice”, “parentfield” → “payment\_schedule”), fields = list(“name”, “idx”, “parent”, “d ….
- Set invoice\_schedules from mapping of name → list() for name drawn from invoices.
  - Draw name from invoices.
- For each schedule in schedules.values().
  - Evaluate invoice\_schedules at schedule.parent.append(schedule).
- Set schedule\_outstanding from mapping().
- For each tuple(name, invoice) in invoices.items().
  - Evaluate schedule\_outstanding.update(get\_payment\_schedule\_outstanding(invoice, invoice\_schedules at name)).
- Set seen\_references from set().
- Set invoice\_outstanding from mapping().
- For each row in self.overdue\_payments.
  - Set invoice from invoices.get(row.sales\_invoice).
  - If (not invoice or invoice.docstatus differs from 1 or invoice.is\_return).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not invoice → invoice.docstatus differs from 1 → invoice.is\_return.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Select an accessible, submitted Sales Invoice.”.format(row.idx)).
  - For each field in tuple(“customer”, “company”, “currency”).
    - If invoice.get(field) differs from self.get(field).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Sales Invoice {1} must have the same {2} as this Dunning.”.format(row.idx, row.sales\_invoice, translated self.meta.get\_label(field))).
  - Set schedule from schedules.get(row.payment\_schedule).
  - If (row.payment\_schedule or invoice.is\_opening differs from “Yes” or invoice\_schedules at invoice.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.payment\_schedule → invoice.is\_opening differs from “Yes” → invoice\_schedules at invoice.name.
    - If (not schedule or schedule.parent differs from row.sales\_invoice).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not schedule → schedule.parent differs from row.sales\_invoice.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Payment Schedule must belong to the selected Sales Invoice.”.format(row.idx)).
  - Set reference from (schedule or invoice).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in schedule → invoice.
  - Set reference\_type from translated “Payment Schedule” when schedule, otherwise translated “Sales Invoice”.
    - Value choice on schedule — true gives translated “Payment Schedule”, false gives translated “Sales Invoice”.
  - Set reference\_key from tuple(row.sales\_invoice, (row.payment\_schedule or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.payment\_schedule → empty text.
  - If reference\_key belongs to seen\_references.
    - Call the validation error handler Platform.throw(translated “Row #{0}: {1} is already included in this Dunning.”.format(row.idx, reference\_type)).
  - Evaluate seen\_references.add(reference\_key).
  - If schedule.
    - For each field in tuple(“payment\_term”, “mode\_of\_payment”, “payment\_amount”, “invoice\_portion”).
      - If field belongs to tuple(“payment\_amount”, “invoice\_portion”).
        - Set matches from flt(row.get(field), row.precision(field)) equals flt(schedule.get(field), row.precision(field)).
      - Otherwise.
        - Set matches from (row.get(field) or empty text) equals (schedule.get(field) or empty text).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(field) → empty text.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in schedule.get(field) → empty text.
      - If not matches.
        - Call the validation error handler Platform.throw(translated “Row #{0}: {1} must match the Payment Schedule.”.format(row.idx, translated row.meta.get\_label(field))).
  - Otherwise.
    - Set row.payment\_term from no value.
    - Set row.mode\_of\_payment from no value.
    - Set row.payment\_amount from (invoice.rounded\_total or invoice.grand\_total).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in invoice.rounded\_total → invoice.grand\_total.
    - Set row.invoice\_portion from 100.
  - If (not row.due\_date or not reference.due\_date or getdate(row.due\_date) differs from getdate(reference.due\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.due\_date → not reference.due\_date → getdate(row.due\_date) differs from getdate(reference.due\_date).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Due Date must match the {1}.”.format(row.idx, reference\_type)).
  - If getdate(reference.due\_date) ≥ getdate(self.posting\_date).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Payment must be overdue on the Dunning Posting Date.”.format(row.idx)).
  - Set outstanding from schedule\_outstanding at schedule.name when schedule, otherwise get\_invoice\_outstanding(invoice).
    - Value choice on schedule — true gives schedule\_outstanding at schedule.name, false gives get\_invoice\_outstanding(invoice).
  - Set invoice\_outstanding at row.sales\_invoice from (invoice\_outstanding.get(row.sales\_invoice, 0) + flt(row.outstanding)).
  - If (flt(row.outstanding, row.precision(“outstanding”)) ≤ 0 or flt(invoice.outstanding\_amount) ≤ 0 or flt(row.outstanding, row.precision(“outstanding”)) &gt; flt(outstanding, row.precision(“outstanding”)) or (inv ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.outstanding, row.precision(“outstanding”)) ≤ 0 → flt(invoice.outstanding\_amount) ≤ 0 → flt(row.outstanding, row.precision(“outstanding”)) &gt; flt(outstanding, row.precision(“outstanding”)) → (invoice.party\_account\_currency equals invoice.currency and flt(invoice\_outstanding at row.sales\_invoice, row.precision(“outstanding”)) &gt; flt(invoice.outstanding\_amount, row.precision(“outstanding”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoice.party\_account\_currency equals invoice.currency → flt(invoice\_outstanding at row.sales\_invoice, row.precision(“outstanding”)) &gt; flt(invoice.outstanding\_amount, row.precision(“outstanding”)).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Outstanding must be positive and cannot exceed the unpaid invoice or installment amount.”.format(row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L790)

<a id="op-68e1ea5202fb89"></a>
### Dunning.validate overdue payments

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_validate_overdue_payments`

**Inputs** self.

**Local steps**

- Set daily\_interest from ((self.rate\_of\_interest ÷ 100) ÷ 365).
- For each row in self.overdue\_payments.
  - Set row.overdue\_days from ((getdate(self.posting\_date) − getdate(row.due\_date)).days or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (getdate(self.posting\_date) − getdate(row.due\_date)).days → 0.
  - Set row.interest from ((row.outstanding × daily\_interest) × row.overdue\_days).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0040.json#L234) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L712)

<a id="op-9d9424a8f72fa3"></a>
### Dunning.validate totals

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_validate_totals`

**Inputs** self.

**Local steps**

- Set self.total\_outstanding from sum(generator of row.outstanding for row drawn from self.overdue\_payments).
  - Draw row from self.overdue\_payments.
- Set self.total\_interest from sum(generator of row.interest for row drawn from self.overdue\_payments).
  - Draw row from self.overdue\_payments.
- Set self.dunning\_amount from (self.total\_interest + self.dunning\_fee).
- Set self.base\_dunning\_amount from (self.dunning\_amount × self.conversion\_rate).
- Set self.grand\_total from (self.total\_outstanding + self.dunning\_amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0040.json#L432) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L713)

<a id="op-51903ffdf468ae"></a>
### Dunning.set party details

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_set_party_details`

**Inputs** self.

**Local steps**

- Bind dependencies \_get\_party\_details.
- Set party\_details from \_get\_party\_details(self.customer, ignore\_permissions = self.flags.ignore\_permissions, doctype = self.doctype, company = self.company, posting\_date = self.get(“posting\_date”), …).
- For each field in list(“customer\_address”, “address\_display”, “company\_address”, “contact\_person”, …).
  - Evaluate self.set(field, party\_details.get(field)).
- Evaluate self.set(“company\_address\_display”, get\_address\_display(self.company\_address)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0040.json#L671) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L710)

<a id="op-e1b4d3b6b637cb"></a>
### Dunning.set dunning level

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_set_dunning_level`

**Inputs** self.

**Record and data access** read “Overdue Payment” via get\_all.

**Local steps**

- For each row in self.overdue\_payments.
  - Set past\_dunnings from Platform.get\_all(“Overdue Payment”, filters = mapping(“sales\_invoice” → row.sales\_invoice, “payment\_schedule” → (row.payment\_schedule or tuple(“is”, “not set”)), “parent” → tuple(“!=”, row.parent), “docstatus” → 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.payment\_schedule → tuple(“is”, “not set”).
  - Set row.dunning\_level from (len(past\_dunnings) + 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L709)

<a id="op-99e317b3a90e35"></a>
### Dunning.get unpaid base dunning amount

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_get_unpaid_base_dunning_amount`

**Inputs** self, ignore\_successors = false.

**Explicit results** 0.0 · unpaid\_amount.

**Local steps**

- If not self.base\_dunning\_amount.
  - Return 0.0.
- Set unpaid\_amount from flt((flt(self.base\_dunning\_amount) − get\_paid\_dunning\_amount(self.name)), self.precision(“base\_dunning\_amount”)).
- If (unpaid\_amount &gt; 0 and not ignore\_successors and self.get\_settled\_successor()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in unpaid\_amount &gt; 0 → not ignore\_successors → self.get\_settled\_successor().
  - Return 0.0.
- Return unpaid\_amount.

**Methods declared on this owner** [get settled successor](operations-035.md#op-a72d9c393d7e61).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L705)

<a id="op-a72d9c393d7e61"></a>
### Dunning.get settled successor

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_dunning_get_settled_successor`

**Inputs** self.

**Record and data access** read “Dunning” via get\_all · resolve a document from “Dunning” via get\_doc.

**Explicit results** no value · successor.name.

**Local steps**

- Set payment\_schedules from set of row.payment\_schedule for row drawn from self.overdue\_payments.
  - Draw row from self.overdue\_payments.
- If (self.docstatus differs from 1 or not payment\_schedules or not all(payment\_schedules)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus differs from 1 → not payment\_schedules → not all(payment\_schedules).
  - Return no value.
- For each row in Platform.get\_all(“Dunning”, filters = list(list(“Dunning”, “docstatus”, “=”, 1), list(“Dunning”, “customer”, “=”, self.customer), list(“Dunning”, “company”, “=”, self.company), list(“Dunning”, “currency”,  ….
  - Set successor from Platform.get\_doc(“Dunning”, row.name).
  - If not payment\_schedules.issubset(set of payment.payment\_schedule for payment drawn from successor.overdue\_payments).
    - Draw payment from successor.overdue\_payments.
    - Continue with the next iteration or loop test.
  - If successor.get\_unpaid\_overdue\_payments().
    - Continue with the next iteration or loop test.
  - If successor.get\_unpaid\_base\_dunning\_amount(ignore\_successors = true) ≤ 0.
    - Return successor.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L787)

<a id="op-4f0d1b827155e1"></a>
### Dunning.get unpaid dunning amount

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_get_unpaid_dunning_amount`

**Inputs** self.

**Explicit results** flt((self.get\_unpaid\_base\_dunning\_amount() ÷ (flt(self.conversion\_rate) or 1)), self.precision(“dunning\_amount”)).

**Local steps**

- Return flt((self.get\_unpaid\_base\_dunning\_amount() ÷ (flt(self.conversion\_rate) or 1)), self.precision(“dunning\_amount”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.conversion\_rate) → 1.

**Methods declared on this owner** [get unpaid base dunning amount](operations-035.md#op-99e317b3a90e35).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0040.json#L1375) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L706)

<a id="op-2ff86f7e45caea"></a>
### Dunning.get unpaid overdue payments

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_get_unpaid_overdue_payments`

**Inputs** self, in\_account\_currency = false.

**Explicit results** list of tuple(row, outstanding) for row drawn from self.overdue\_payments where outstanding bound to get\_current\_outstanding(row, in\_account\_currency = in\_account\_currency) &gt; 0.

**Local steps**

- Return list of tuple(row, outstanding) for row drawn from self.overdue\_payments where outstanding bound to get\_current\_outstanding(row, in\_account\_currency = in\_account\_currency) &gt; 0.
  - Draw row from self.overdue\_payments, keep a combination only if (outstanding bound to get\_current\_outstanding(row, in\_account\_currency = in\_account\_currency) &gt; 0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L707)

<a id="op-e8b5a97e2a6d7f"></a>
### Dunning.before cancel

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_dunning_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().before\_cancel().
- Set self.status from “Cancelled”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L785)

<a id="op-3a33b04a0ec0bc"></a>
### Dunning.on cancel

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().on\_cancel().
- Set self.ignore\_linked\_doctypes from list(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Repost Payment Ledger”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L708)

<a id="op-ced4e2cceac674"></a>
### Dunning.get dunning letter text

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_dunning_get_dunning_letter_text`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read DOCTYPE via get\_value.

**State and service calls** msgprint with msg.

**Explicit results** no value.

**Local steps**

- Set DOCTYPE from “Dunning Letter Text”.
- Set FIELDS from list(“body\_text”, “closing\_text”, “language”).
- If not self.dunning\_type.
  - Return no value.
- Set filters from mapping(“parent” → self.dunning\_type, “is\_default\_language” → 1).
- If self.language.
  - Evaluate filters.pop(“is\_default\_language”).
  - Set filters at “language” from self.language.
- Set letter\_text from Platform.db.get\_value(DOCTYPE, filters, FIELDS, as\_dict = true).
- If not letter\_text.
  - Set msg from translated “Dunning Letter for Dunning Type {0} in language '{1}' not found.”.format(Platform.bold(self.dunning\_type), Platform.bold(self.language)) when self.language, otherwise translated “Dunning Letter ….
    - Value choice on self.language — true gives translated “Dunning Letter for Dunning Type {0} in language '{1}' not found.”.format(Platform.bold(self.dunning\_type), Platform.bold(self.language)), false gives translated “Dunning Letter for Dunning Type {0} not found.”.format(Platform.bold(self.dunning\_type)).
  - Evaluate Platform.msgprint(msg, alert = true, indicator = “yellow”).
- Set self.body\_text from Platform.render\_template(letter\_text.body\_text, self.as\_dict(), restrict\_globals = true) when letter\_text, otherwise no value.
  - Value choice on letter\_text — true gives Platform.render\_template(letter\_text.body\_text, self.as\_dict(), restrict\_globals = true), false gives no value.
- Set self.closing\_text from Platform.render\_template(letter\_text.closing\_text, self.as\_dict(), restrict\_globals = true) when letter\_text, otherwise no value.
  - Value choice on letter\_text — true gives Platform.render\_template(letter\_text.closing\_text, self.as\_dict(), restrict\_globals = true), false gives no value.
- Set self.language from letter\_text.language when letter\_text, otherwise self.language.
  - Value choice on letter\_text — true gives letter\_text.language, false gives self.language.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0040.json#L1786) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L704)

<a id="op-25ae98349b37b8"></a>
### Get invoice outstanding

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_get_invoice_outstanding`

**Inputs** invoice.

**Explicit results** (flt(invoice.outstanding\_amount) ÷ flt(invoice.conversion\_rate)) · flt(invoice.outstanding\_amount).

**Local steps**

- If invoice.party\_account\_currency differs from invoice.currency.
  - Return (flt(invoice.outstanding\_amount) ÷ flt(invoice.conversion\_rate)).
- Return flt(invoice.outstanding\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L791)

<a id="op-b7b6c1a9919bae"></a>
### Get payment schedule outstanding

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_get_payment_schedule_outstanding`

**Inputs** invoice, payment\_schedule, in\_account\_currency = false.

**Explicit results** outstanding.

**Local steps**

- Set outstanding from mapping of row.name → flt(row.outstanding) for row drawn from payment\_schedule.
  - Draw row from payment\_schedule.
- Set invoice\_outstanding from flt(invoice.outstanding\_amount).
- If invoice.party\_account\_currency differs from invoice.currency.
  - If in\_account\_currency.
    - Set outstanding from mapping of name → (amount × flt(invoice.conversion\_rate)) for tuple(name, amount) drawn from outstanding.items().
      - Draw tuple(name, amount) from outstanding.items().
  - Otherwise.
    - Set invoice\_outstanding from get\_invoice\_outstanding(invoice).
- Set unallocated\_payment from max((sum(outstanding.values()) − invoice\_outstanding), 0).
- For each row in sorted(payment\_schedule, key = deferred anonymous expression).
  - Set paid\_amount from min(outstanding at row.name, unallocated\_payment).
  - Update unallocated\_payment using − paid\_amount.
  - Update outstanding at row.name using − paid\_amount.
- Return outstanding.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L792)

<a id="op-8b4b5a0dd6d9de"></a>
### Update linked dunnings

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_update_linked_dunnings`

**Inputs** doc, previous\_outstanding\_amount.

**Record and data access** read “Overdue Payment” via get\_all · read “Dunning” via get\_all · resolve a document from “Dunning” via get\_doc · read “Sales Invoice” via get\_all · read “Payment Schedule” via get\_all.

**Explicit results** no value.

**Local steps**

- If (doc.doctype differs from “Sales Invoice” or doc.is\_return or previous\_outstanding\_amount equals doc.outstanding\_amount).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype differs from “Sales Invoice” → doc.is\_return → previous\_outstanding\_amount equals doc.outstanding\_amount.
  - Return no value.
- Set dunnings from Platform.get\_all(“Overdue Payment”, filters = mapping(“sales\_invoice” → doc.name, “docstatus” → 1), pluck = “parent”).
- If not dunnings.
  - Return no value.
- Set dunnings from Platform.get\_all(“Dunning”, filters = mapping(“name” → tuple(“in”, get\_related\_dunnings(dunnings)), “docstatus” → 1, “status” → “Unresolved” when doc.outstanding\_amount &lt; previous\_outstanding\_amount, other ….
  - Value choice on doc.outstanding\_amount &lt; previous\_outstanding\_amount — true gives “Unresolved”, false gives “Resolved”.
- If not dunnings.
  - Return no value.
- Set dunnings from list of Platform.get\_doc(“Dunning”, name) for name drawn from dunnings.
  - Draw name from dunnings.
- Set invoices from set().
- Set payment\_schedule\_ids from set().
- For each dunning in dunnings.
  - For each overdue\_payment in dunning.overdue\_payments.
    - Evaluate invoices.add(overdue\_payment.sales\_invoice).
    - If overdue\_payment.payment\_schedule.
      - Evaluate payment\_schedule\_ids.add(overdue\_payment.payment\_schedule).
- Set invoice\_outstanding\_amounts from dict(Platform.get\_all(“Sales Invoice”, filters = mapping(“name” → list(“in”, list(invoices))), fields = list(“name”, “outstanding\_amount”), as\_list = true)).
- Set ps\_outstanding\_amounts from dict(Platform.get\_all(“Payment Schedule”, filters = mapping(“name” → list(“in”, list(payment\_schedule\_ids))), fields = list(“name”, “outstanding”), as\_list = true)) when payment\_schedule\_ids, otherwise mapping().
  - Value choice on payment\_schedule\_ids — true gives dict(Platform.get\_all(“Payment Schedule”, filters = mapping(“name” → list(“in”, list(payment\_schedule\_ids))), fields = list(“name”, “outstanding”), as\_list = true)), false gives mapping().
- For each dunning in dunnings.
  - Set has\_outstanding from false.
  - For each overdue\_payment in dunning.overdue\_payments.
    - Set invoice\_outstanding from invoice\_outstanding\_amounts at overdue\_payment.sales\_invoice.
    - Set ps\_outstanding from ps\_outstanding\_amounts.get(overdue\_payment.payment\_schedule, 0) when overdue\_payment.payment\_schedule, otherwise invoice\_outstanding.
      - Value choice on overdue\_payment.payment\_schedule — true gives ps\_outstanding\_amounts.get(overdue\_payment.payment\_schedule, 0), false gives invoice\_outstanding.
    - Set has\_outstanding from (invoice\_outstanding &gt; 0 and ps\_outstanding &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoice\_outstanding &gt; 0 → ps\_outstanding &gt; 0.
    - If has\_outstanding.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate set\_dunning\_status(dunning, has\_outstanding, respect\_manual\_resolution = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L718)

<a id="op-597571fc3230df"></a>
### Update dunnings linked to payment

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_update_dunnings_linked_to_payment`

**Inputs** payment\_entry.

**Record and data access** resolve a document from “Dunning” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set referenced\_dunnings from set of row.dunning for row drawn from payment\_entry.get(“deductions”) where row.dunning.
  - Draw row from payment\_entry.get(“deductions”), keep a combination only if (row.dunning).
- If not referenced\_dunnings.
  - Return no value.
- For each name in get\_related\_dunnings(referenced\_dunnings).
  - Set dunning from Platform.get\_doc(“Dunning”, name).
  - <a id="op-597571fc3230df-guard-9"></a>If dunning.docstatus differs from 1.
    - Continue with the next iteration or loop test.
  - Evaluate set\_dunning\_status(dunning, bool(dunning.get\_unpaid\_overdue\_payments()), respect\_manual\_resolution = name does not belong to referenced\_dunnings).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison dunning.docstatus differs from 1, dunning.docstatus = 0 (draft) selects the branch that continues with the next loop iteration. With dunning.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-597571fc3230df-guard-9)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L717)

<a id="op-0b371132ff8fed"></a>
### Update superseded dunnings

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_update_superseded_dunnings`

**Inputs** no declared parameters.

**Record and data access** read “Dunning” via get\_all · resolve a document from “Dunning” via get\_doc.

**Local steps**

- For each name in Platform.get\_all(“Dunning”, filters = mapping(“docstatus” → 1, “status” → “Unresolved”), pluck = “name”).
  - Set dunning from Platform.get\_doc(“Dunning”, name).
  - If not dunning.get\_unpaid\_overdue\_payments().
    - Evaluate set\_dunning\_status(dunning, false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L794)

<a id="op-688ee345b53be0"></a>
### Set dunning status

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_set_dunning_status`

**Inputs** dunning, has\_outstanding\_payments, respect\_manual\_resolution = false.

**State and service calls** call db\_set on dunning.

**Explicit results** no value.

**Local steps**

- If (respect\_manual\_resolution and dunning.status equals “Resolved” and not dunning.superseded\_by and not has\_outstanding\_payments).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in respect\_manual\_resolution → dunning.status equals “Resolved” → not dunning.superseded\_by → not has\_outstanding\_payments.
  - Return no value.
- Set has\_unpaid\_dunning\_amount from dunning.get\_unpaid\_base\_dunning\_amount(ignore\_successors = true) &gt; 0.
- Set superseded\_by from dunning.get\_settled\_successor() when (has\_unpaid\_dunning\_amount and not has\_outstanding\_payments), otherwise no value.
  - Value choice on (has\_unpaid\_dunning\_amount and not has\_outstanding\_payments) — true gives dunning.get\_settled\_successor(), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_unpaid\_dunning\_amount → not has\_outstanding\_payments.
- Set new\_status from “Unresolved” when (has\_outstanding\_payments or (has\_unpaid\_dunning\_amount and not superseded\_by)), otherwise “Resolved”.
  - Value choice on (has\_outstanding\_payments or (has\_unpaid\_dunning\_amount and not superseded\_by)) — true gives “Unresolved”, false gives “Resolved”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_outstanding\_payments → (has\_unpaid\_dunning\_amount and not superseded\_by).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_unpaid\_dunning\_amount → not superseded\_by.
- If (dunning.status differs from new\_status or dunning.superseded\_by differs from superseded\_by).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dunning.status differs from new\_status → dunning.superseded\_by differs from superseded\_by.
  - Evaluate dunning.db\_set(mapping(“status” → new\_status, “superseded\_by” → superseded\_by), notify = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L716)

<a id="op-284fe6c37eff1e"></a>
### Get paid dunning amount

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_get_paid_dunning_amount`

**Inputs** dunning.

**Declared result** float.

**Explicit results** negative flt(paid at 0 at 0) when paid, otherwise 0.0.

**Local steps**

- Set deduction from Platform.qb.DocType(“Payment Entry Deduction”).
- Set payment\_entry from Platform.qb.DocType(“Payment Entry”).
- Set dunning\_doc from Platform.qb.DocType(“Dunning”).
- Set paid from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.amount)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwis ….run().
- Return negative flt(paid at 0 at 0) when paid, otherwise 0.0.
  - Value choice on paid — true gives negative flt(paid at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L715)

<a id="op-59e78166e35e3e"></a>
### Get current outstanding

`operation_enterprise_accounts_record_definitions_dunning_business_behavior_get_current_outstanding`

**Inputs** overdue\_payment, in\_account\_currency = false.

**Declared result** float.

**Record and data access** read “Sales Invoice” via get\_value · read “Payment Schedule” via get\_all.

**Explicit results** 0.0 · outstanding.

**Local steps**

- Set invoice from Platform.db.get\_value(“Sales Invoice”, overdue\_payment.sales\_invoice, list(“outstanding\_amount”, “currency”, “party\_account\_currency”, “conversion\_rate”), as\_dict = true).
- Set outstanding from flt(overdue\_payment.outstanding).
- If (in\_account\_currency and invoice.currency differs from invoice.party\_account\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_account\_currency → invoice.currency differs from invoice.party\_account\_currency.
  - Set outstanding from flt((outstanding × flt(invoice.conversion\_rate)), overdue\_payment.precision(“outstanding”)).
- If overdue\_payment.payment\_schedule.
  - Set payment\_schedule from Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → overdue\_payment.sales\_invoice, “parenttype” → “Sales Invoice”), fields = list(“name”, “idx”, “due\_date”, “outstanding”)).
  - Set schedule\_outstanding from get\_payment\_schedule\_outstanding(invoice, payment\_schedule, in\_account\_currency = in\_account\_currency).
  - Set outstanding from min(outstanding, schedule\_outstanding.get(overdue\_payment.payment\_schedule, 0)).
- Otherwise.
  - If not in\_account\_currency.
    - Set outstanding from min(outstanding, get\_invoice\_outstanding(invoice)).
- If (flt(invoice.outstanding\_amount) ≤ 0 or outstanding ≤ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(invoice.outstanding\_amount) ≤ 0 → outstanding ≤ 0.
  - Return 0.0.
- If (in\_account\_currency or invoice.currency equals invoice.party\_account\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in in\_account\_currency → invoice.currency equals invoice.party\_account\_currency.
  - Set outstanding from min(outstanding, flt(invoice.outstanding\_amount)).
- Return outstanding.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L714)

<a id="op-998b1123d82552"></a>
### Get related dunnings

`operation_enterprise_binding_enterprise_accounts_doctype_dunning_dunning_get_related_dunnings`

**Inputs** dunnings.

**Record and data access** read “Overdue Payment” via get\_all.

**Explicit results** (set(dunnings) bitwise or set(Platform.get\_all(“Overdue Payment”, filters = mapping(“payment\_schedule” → tuple(“in”, payment\_schedules), “docstatus” → 1), pluck = “parent”))).

**Local steps**

- Set payment\_schedules from Platform.get\_all(“Overdue Payment”, filters = mapping(“parent” → tuple(“in”, dunnings), “docstatus” → 1), pluck = “payment\_schedule”).
- Return (set(dunnings) bitwise or set(Platform.get\_all(“Overdue Payment”, filters = mapping(“payment\_schedule” → tuple(“in”, payment\_schedules), “docstatus” → 1), pluck = “parent”))).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L793)
