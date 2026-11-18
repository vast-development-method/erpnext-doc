# Accounting and settlement · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Accounts receivable

<a id="op-0fcb4ec2c7e83a"></a>
### Receivable Payable Report.update sub total row

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_update_subordinate_total_row`

**Inputs** self, row, party.

**Local steps**

- Set total\_row from self.total\_row\_map.get(party).
- If total\_row.
  - For each field in self.get\_currency\_fields().
    - Update total\_row at field using + row.get(field, 0.0).
  - Set total\_row at “currency” from row.get(“currency”, empty text).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get currency fields](operations-006.md#op-ada6129f60dc83).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L4509) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L597)

<a id="op-8c14512af46738"></a>
### Receivable Payable Report.append subtotal row

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_append_subtotal_row`

**Inputs** self, party.

**Local steps**

- Set sub\_total\_row from self.total\_row\_map.get(party).
- If sub\_total\_row.
  - Evaluate self.data.append(sub\_total\_row).
  - Evaluate self.data.append(mapping()).
  - Evaluate self.update\_sub\_total\_row(sub\_total\_row, “Total”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update sub total row](operations-007.md#op-0fcb4ec2c7e83a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L4714) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L558)

<a id="op-13a01173089ebd"></a>
### Receivable Payable Report.build data

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_build_data`

**Inputs** self.

**Local steps**

- For each tuple(\_key, row) in self.voucher\_balance.items().
  - Set row.outstanding from flt(((row.invoiced − row.paid) − row.credit\_note), self.currency\_precision).
  - Set row.outstanding\_in\_account\_currency from flt(((row.invoiced\_in\_account\_currency − row.paid\_in\_account\_currency) − row.credit\_note\_in\_account\_currency), self.currency\_precision).
  - Set row.invoice\_grand\_total from row.invoiced.
  - Set must\_consider from false.
  - If self.filters.get(“for\_revaluation\_journals”).
    - If (abs(row.outstanding) ≥ (1.0 ÷ (10 to the power self.currency\_precision)) or abs(row.outstanding\_in\_account\_currency) ≥ (1.0 ÷ (10 to the power self.currency\_precision))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in abs(row.outstanding) ≥ (1.0 ÷ (10 to the power self.currency\_precision)) → abs(row.outstanding\_in\_account\_currency) ≥ (1.0 ÷ (10 to the power self.currency\_precision)).
      - Set must\_consider from true.
  - Otherwise.
    - If (abs(row.outstanding) ≥ (1.0 ÷ (10 to the power self.currency\_precision)) and (abs(row.outstanding\_in\_account\_currency) ≥ (1.0 ÷ (10 to the power self.currency\_precision)) or row.voucher\_no belongs to self ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in abs(row.outstanding) ≥ (1.0 ÷ (10 to the power self.currency\_precision)) → (abs(row.outstanding\_in\_account\_currency) ≥ (1.0 ÷ (10 to the power self.currency\_precision)) or row.voucher\_no belongs to self.err\_journals).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in abs(row.outstanding\_in\_account\_currency) ≥ (1.0 ÷ (10 to the power self.currency\_precision)) → row.voucher\_no belongs to self.err\_journals.
      - Set must\_consider from true.
  - If must\_consider.
    - If (self.is\_invoice(row) and self.filters.based\_on\_payment\_terms).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_invoice(row) → self.filters.based\_on\_payment\_terms.
      - Evaluate self.allocate\_outstanding\_based\_on\_payment\_terms(row).
      - If row.payment\_terms.
        - For each d in row.payment\_terms.
          - If d.outstanding &gt; 0.
            - Evaluate self.append\_row(d).
        - Evaluate self.allocate\_extra\_payments\_or\_credits(row).
      - Otherwise.
        - Evaluate self.append\_row(row).
    - Otherwise.
      - Evaluate self.append\_row(row).
- If self.filters.get(“group\_by\_party”).
  - Evaluate self.append\_subtotal\_row(self.previous\_party).
  - If self.data.
    - Evaluate self.data.append(self.total\_row\_map.get(“Total”, mapping())).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is invoice](operations-008.md#op-9338432b038ecb), [allocate outstanding based on payment terms](operations-007.md#op-ce7eb1f984f970), [append row](operations-007.md#op-8bdab019660b76), [allocate extra payments or credits](operations-007.md#op-1a42d594f6ccd9), [append subtotal row](operations-007.md#op-8c14512af46738).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L4878) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L559)

<a id="op-8bdab019660b76"></a>
### Receivable Payable Report.append row

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_append_row`

**Inputs** self, row.

**Local steps**

- Evaluate self.allocate\_future\_payments(row).
- Evaluate self.set\_invoice\_details(row).
- Evaluate self.set\_party\_details(row).
- Evaluate self.set\_ageing(row).
- If self.filters.get(“group\_by\_party”).
  - Evaluate self.update\_sub\_total\_row(row, row.party).
  - If (self.previous\_party and self.previous\_party differs from row.party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.previous\_party → self.previous\_party differs from row.party.
    - Evaluate self.append\_subtotal\_row(self.previous\_party).
  - Set self.previous\_party from row.party.
- Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [allocate future payments](operations-007.md#op-f15f6881b74ec0), [set invoice details](operations-007.md#op-0d974f97b990b1), [set party details](operations-007.md#op-e9d0e568a5f357), [set ageing](operations-007.md#op-75fd78ce1affd6), [update sub total row](operations-007.md#op-0fcb4ec2c7e83a), [append subtotal row](operations-007.md#op-8c14512af46738).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L5791) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L557)

<a id="op-0d974f97b990b1"></a>
### Receivable Payable Report.set invoice details

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_set_invoice_details`

**Inputs** self, row.

**Local steps**

- Set invoice\_details from self.invoice\_details.get(row.voucher\_no, mapping()).
- If row.due\_date.
  - Evaluate invoice\_details.pop(“due\_date”, no value).
- Evaluate row.update(invoice\_details).
- If row.voucher\_type equals “Sales Invoice”.
  - If self.filters.show\_delivery\_notes.
    - Evaluate self.set\_delivery\_notes(row).
  - If (self.filters.show\_sales\_person and row.sales\_team).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.show\_sales\_person → row.sales\_team.
    - Set row.sales\_person from “, ”.join(row.sales\_team).
    - Remove row at “sales\_team”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set delivery notes](operations-007.md#op-90edd8107cdb4a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L6114) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L594)

<a id="op-90edd8107cdb4a"></a>
### Receivable Payable Report.set delivery notes

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_set_delivery_notes`

**Inputs** self, row.

**Local steps**

- Set delivery\_notes from self.delivery\_notes.get(row.voucher\_no, list()).
- If delivery\_notes.
  - Set row.delivery\_notes from “, ”.join(delivery\_notes).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L6426) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L593)

<a id="op-35cfd51083f59e"></a>
### Receivable Payable Report.build delivery note map

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_build_delivery_note_map`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Local steps**

- If (self.invoices and self.filters.show\_delivery\_notes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.invoices → self.filters.show\_delivery\_notes.
  - Set self.delivery\_notes from Platform.\_dict().
  - Set si\_against\_dn from Platform.db.sql((query text (SELECT, Sales Invoice Item) modulo or format “,”.join((list(“%s”) × len(self.invoices)))), tuple(self.invoices), as\_dict = 1).
  - For each d in si\_against\_dn.
    - If d.delivery\_note.
      - Evaluate self.delivery\_notes.setdefault(d.parent, set()).add(d.delivery\_note).
  - Set dn\_against\_si from Platform.db.sql((query text (SELECT, Delivery Note Item) modulo or format “,”.join((list(“%s”) × len(self.invoices)))), tuple(self.invoices), as\_dict = 1).
  - For each d in dn\_against\_si.
    - Evaluate self.delivery\_notes.setdefault(d.against\_sales\_invoice, set()).add(d.parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L560)

<a id="op-9d420f0976a28a"></a>
### Receivable Payable Report.get invoice details

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_invoice_details`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_list · execute query text (SELECT, Sales Team) · read “Purchase Invoice” via get\_list · read “Journal Entry” via get\_list.

**Local steps**

- Set self.invoice\_details from Platform.\_dict().
- If self.account\_type equals “Receivable”.
  - Set si\_list from Platform.get\_list(“Sales Invoice”, filters = mapping(“posting\_date” → tuple(“&lt;=”, self.filters.report\_date), “company” → self.filters.company, “docstatus” → 1), fields = list(“name”, “due\_date”, “po\_no”, “ ….
  - For each d in si\_list.
    - Evaluate self.invoice\_details.setdefault(d.name, d).
  - If self.filters.show\_sales\_person.
    - Set sales\_team from Platform.db.sql(query text (SELECT, Sales Team), as\_dict = 1).
    - For each d in sales\_team.
      - Evaluate nested operand in the contract.invoice\_details.setdefault(d.parent, mapping()).setdefault(“sales\_team”, list()).append(d.sales\_person).
- If self.account\_type equals “Payable”.
  - Set invoices from Platform.get\_list(“Purchase Invoice”, filters = mapping(“posting\_date” → tuple(“&lt;=”, self.filters.report\_date), “company” → self.filters.company, “docstatus” → 1), fields = list(“name”, “due\_date”, “bill\_n ….
  - For each pi in invoices.
    - Evaluate self.invoice\_details.setdefault(pi.name, pi).
- Set journal\_entries from Platform.get\_list(“Journal Entry”, filters = mapping(“posting\_date” → tuple(“&lt;=”, self.filters.report\_date), “company” → self.filters.company, “docstatus” → 1), fields = list(“name”, “due\_date”, “bill\_no”, ….
- For each je in journal\_entries.
  - If je.bill\_no.
    - Evaluate self.invoice\_details.setdefault(je.name, je).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L575)

<a id="op-e9d0e568a5f357"></a>
### Receivable Payable Report.set party details

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_set_party_details`

**Inputs** self, row.

**Local steps**

- If row.party.
  - Evaluate row.update((self.get\_party\_details(row.party) or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_party\_details(row.party) → mapping().
- If (self.filters.get(“in\_party\_currency”) or self.filters.get(“party\_account”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“in\_party\_currency”) → self.filters.get(“party\_account”).
  - Set row.currency from row.account\_currency.
- Otherwise.
  - Set row.currency from self.company\_currency.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party details](operations-008.md#op-5ddbb4d1bd4eb1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L595)

<a id="op-ce7eb1f984f970"></a>
### Receivable Payable Report.allocate outstanding based on payment terms

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_allocate_outstanding_based_on_payment_terms`

**Inputs** self, row.

**Local steps**

- Evaluate self.get\_payment\_terms(row).
- For each term in row.payment\_terms.
  - If not term.paid.
    - Evaluate self.allocate\_closing\_to\_term(row, term, “paid”).
  - If term.outstanding.
    - Evaluate self.allocate\_closing\_to\_term(row, term, “credit\_note”).
- Set row.payment\_terms from sorted(row.payment\_terms, key = deferred anonymous expression).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get payment terms](operations-007.md#op-3fea427e053e2f), [allocate closing to term](operations-007.md#op-90680611062543).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0217.json#L1225) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L555)

<a id="op-3fea427e053e2f"></a>
### Receivable Payable Report.get payment terms

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_payment_terms`

**Inputs** self, row.

**Record and data access** read “Company” via get\_value.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- Set order\_by from “due\_date” when self.is\_historical\_report(), otherwise “ps.paid\_amount desc, due\_date”.
  - Value choice on self.is\_historical\_report() — true gives “due\_date”, false gives “ps.paid\_amount desc, due\_date”.
- Set payment\_terms\_details from Platform.db.sql(formatted text   select  si.name, si.party\_account\_currency, si.currency, si.conversion\_rate,  si.total\_advance, ps.due\_date, ps.payment\_term, ps.payment\_amo, row.voucher\_no, as\_dict = 1).
- Set original\_row from Platform.\_dict(row).
- Set row.payment\_terms from list().
- If not payment\_terms\_details.
  - Return no value.
- Set company\_currency from Platform.get\_value(“Company”, self.filters.get(“company”), “default\_currency”).
- Update row.paid using − self.get\_advance\_in\_report\_currency(payment\_terms\_details at 0, company\_currency).
- If (len(payment\_terms\_details) equals 1 and payment\_terms\_details at 0.payment\_term).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(payment\_terms\_details) equals 1 → payment\_terms\_details at 0.payment\_term.
  - Evaluate self.append\_payment\_term(row, payment\_terms\_details at 0, original\_row, company\_currency).
  - Return no value.
- For each d in payment\_terms\_details.
  - Set term from Platform.\_dict(original\_row).
  - Evaluate self.append\_payment\_term(row, d, term, company\_currency).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is historical report](operations-007.md#op-e5c1e2acba8f9a), [get advance in report currency](operations-007.md#op-e6a2f3222b904c), [append payment term](operations-007.md#op-2a8169f1047fc7).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L579)

<a id="op-e6a2f3222b904c"></a>
### Receivable Payable Report.get advance in report currency

`operation_enterprise_binding_enterprise_accounts_report_accounts_receivable_accounts_receivable_receivablepayablereport_get_advance_in_report_currency`

**Inputs** self, invoice, company\_currency.

**Explicit results** advance · (advance × flt(invoice.conversion\_rate)).

**Local steps**

- Set advance from flt(invoice.total\_advance).
- If (self.filters.get(“in\_party\_currency”) or self.filters.get(“party\_account”) or invoice.party\_account\_currency equals company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“in\_party\_currency”) → self.filters.get(“party\_account”) → invoice.party\_account\_currency equals company\_currency.
  - Return advance.
- Return (advance × flt(invoice.conversion\_rate)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1110)

<a id="op-2a8169f1047fc7"></a>
### Receivable Payable Report.append payment term

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_append_payment_term`

**Inputs** self, row, d, term, company\_currency.

**Local steps**

- Set invoiced from d.base\_payment\_amount.
- Set paid\_amount from d.base\_paid\_amount.
- Set in\_party\_currency from self.filters.get(“in\_party\_currency”).
- If (company\_currency equals d.currency and company\_currency equals d.party\_account\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_currency equals d.currency → company\_currency equals d.party\_account\_currency.
  - Set in\_party\_currency from false.
- If (in\_party\_currency and d.currency differs from d.party\_account\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_party\_currency → d.currency differs from d.party\_account\_currency.
  - Set in\_party\_currency from false.
- If in\_party\_currency.
  - Set invoiced from d.payment\_amount.
  - Set paid\_amount from d.paid\_amount.
- Set discounted\_amount from d.discounted\_amount.
- If self.is\_historical\_report().
  - Set paid\_amount, discounted\_amount from 0.0.
- Evaluate row.payment\_terms.append(term.update(mapping(“due\_date” → d.due\_date, “invoiced” → invoiced, “invoice\_grand\_total” → row.invoiced, “payment\_term” → (d.description or d.payment\_term), …))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.description → d.payment\_term.
- If paid\_amount.
  - Update row at “paid” using − (paid\_amount + discounted\_amount).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is historical report](operations-007.md#op-e5c1e2acba8f9a).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L556)

<a id="op-e5c1e2acba8f9a"></a>
### Receivable Payable Report.is historical report

`operation_enterprise_binding_enterprise_accounts_report_accounts_receivable_accounts_receivable_receivablepayablereport_is_historical_report`

**Inputs** self.

**Declared result** bool.

**Explicit results** self.filters.report\_date &lt; getdate(nowdate()).

**Local steps**

- Return self.filters.report\_date &lt; getdate(nowdate()).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1111)

<a id="op-90680611062543"></a>
### Receivable Payable Report.allocate closing to term

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_allocate_closing_to_term`

**Inputs** self, row, term, key.

**Local steps**

- If row at key.
  - If row at key &gt; term.outstanding.
    - Set term at key from term.outstanding.
    - Update row at key using − term.outstanding.
  - Otherwise.
    - Set term at key from row at key.
    - Set row at key from 0.
- Update term.outstanding using − term at key.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0217.json#L2858) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L552)

<a id="op-1a42d594f6ccd9"></a>
### Receivable Payable Report.allocate extra payments or credits

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_allocate_extra_payments_or_credits`

**Inputs** self, row.

**Local steps**

- Set additional\_row from no value.
- For each key in tuple(“paid”, “credit\_note”).
  - If row at key &gt; 0.
    - If not additional\_row.
      - Set additional\_row from Platform.\_dict(row).
    - Set additional\_row.invoiced from 0.0.
    - Set additional\_row at key from row at key.
- If additional\_row.
  - Set additional\_row.outstanding from ((additional\_row.invoiced − additional\_row.paid) − additional\_row.credit\_note).
  - Evaluate self.append\_row(additional\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append row](operations-007.md#op-8bdab019660b76).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0217.json#L3077) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L553)

<a id="op-9a60d202ab6990"></a>
### Receivable Payable Report.get future payments

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_future_payments`

**Inputs** self.

**Local steps**

- If self.filters.show\_future\_payments.
  - Set self.future\_payments from Platform.\_dict().
  - Set future\_payments from list(self.get\_future\_payments\_from\_payment\_entry()).
  - Update future\_payments using + list(self.get\_future\_payments\_from\_journal\_entry()).
  - If future\_payments.
    - For each d in future\_payments.
      - If (d.future\_amount and d.invoice\_no).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.future\_amount → d.invoice\_no.
        - Evaluate self.future\_payments.setdefault(tuple(d.invoice\_no, d.party), list()).append(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get future payments from payment entry](operations-007.md#op-2e2ffa55cc595a), [get future payments from journal entry](operations-007.md#op-5693eac23ac12b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0217.json#L3353) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L572)

<a id="op-2e2ffa55cc595a"></a>
### Receivable Payable Report.get future payments from payment entry

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_future_payments_from_payment_entry`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“invoice\_no”), pe.party, pe.party\_type, nested operand in the contract.as\_(“future\_date”), …).where( ….

**Local steps**

- Set pe from Platform.qb.DocType(“Payment Entry”).
- Set pe\_ref from Platform.qb.DocType(“Payment Entry Reference”).
- Set ifelse from query\_builder.CustomFunction(“IF”, list(“condition”, “then”, “else”)).
- Return nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“invoice\_no”), pe.party, pe.party\_type, nested operand in the contract.as\_(“future\_date”), …).where( ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L574)

<a id="op-5693eac23ac12b"></a>
### Receivable Payable Report.get future payments from journal entry

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_future_payments_from_journal_entry`

**Inputs** self.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set je from Platform.qb.DocType(“Journal Entry”).
- Set jea from Platform.qb.DocType(“Journal Entry Account”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(jea.reference\_name.as\_(“invoice\_no”), jea.party, j ….
- If self.filters.get(“party”).
  - If self.account\_type equals “Payable”.
    - Set query from query.select(Sum((jea.debit\_in\_account\_currency − jea.credit\_in\_account\_currency)).as\_(“future\_amount”)).
    - Set query from query.select(Sum((jea.debit − jea.credit)).as\_(“future\_amount\_in\_base\_currency”)).
  - Otherwise.
    - Set query from query.select(Sum((jea.credit\_in\_account\_currency − jea.debit\_in\_account\_currency)).as\_(“future\_amount”)).
    - Set query from query.select(Sum((jea.credit − jea.debit)).as\_(“future\_amount\_in\_base\_currency”)).
- Otherwise.
  - Set query from query.select(Sum(jea.debit when nested operand in the contract.account\_type equals “Payable”, otherwise jea.credit).as\_(“future\_amount\_in\_base\_currency”)).
    - Value choice on self.account\_type equals “Payable” — true gives jea.debit, false gives jea.credit.
  - Set query from query.select(Sum(jea.debit\_in\_account\_currency when nested operand in the contract.account\_type equals “Payable”, otherwise jea.credit\_in\_account\_currency).as\_(“future\_amount”)).
    - Value choice on self.account\_type equals “Payable” — true gives jea.debit\_in\_account\_currency, false gives jea.credit\_in\_account\_currency.
- Set query from query.having(qb.Field(“future\_amount”) &gt; 0).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L573)

<a id="op-f15f6881b74ec0"></a>
### Receivable Payable Report.allocate future payments

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_allocate_future_payments`

**Inputs** self, row.

**Explicit results** no value.

**Local steps**

- If not self.filters.show\_future\_payments.
  - Return no value.
- Set row.remaining\_balance from row.outstanding.
- Set row.future\_amount from 0.0.
- For each future in self.future\_payments.get(tuple(row.voucher\_no, row.party), list()).
  - If self.filters.in\_party\_currency.
    - Set future\_amount\_field from “future\_amount”.
  - Otherwise.
    - Set future\_amount\_field from “future\_amount\_in\_base\_currency”.
  - If (row.remaining\_balance differs from 0 and future.get(future\_amount\_field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.remaining\_balance differs from 0 → future.get(future\_amount\_field).
    - Set amount from min(future.get(future\_amount\_field), row.remaining\_balance).
    - Update row.future\_amount using + amount.
    - Update future at future\_amount\_field using − amount.
    - Set row.remaining\_balance from (row.outstanding − row.future\_amount).
    - Evaluate row.setdefault(“future\_ref”, list()).append(((cstr(future.future\_ref) + “/”) + cstr(future.future\_date))).
- If row.future\_ref.
  - Set row.future\_ref from “, ”.join(row.future\_ref).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L554)

<a id="op-5d4119ed94abd1"></a>
### Receivable Payable Report.get return entries

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_return_entries`

**Inputs** self.

**Record and data access** read doctype via get\_all.

**Local steps**

- Set doctype from “Sales Invoice” when self.account\_type equals “Receivable”, otherwise “Purchase Invoice”.
  - Value choice on self.account\_type equals “Receivable” — true gives “Sales Invoice”, false gives “Purchase Invoice”.
- Set filters from mapping(“posting\_date” → tuple(“&lt;=”, self.filters.report\_date), “is\_return” → 1, “docstatus” → 1, “company” → self.filters.company, …).
- Set or\_filters from mapping().
- If party\_type bound to self.filters.party\_type.
  - Set party\_field from scrub(party\_type).
  - If parties bound to self.filters.get(“party”).
    - Evaluate or\_filters.update(mapping(party\_field → list(“in”, parties))).
- Set self.return\_entries from Platform.\_dict(Platform.get\_all(doctype, filters = filters, or\_filters = or\_filters, fields = list(“name”, “return\_against”), as\_list = 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0217.json#L5770) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L581)

<a id="op-75fd78ce1affd6"></a>
### Receivable Payable Report.set ageing

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_set_ageing`

**Inputs** self, row.

**Explicit results** no value.

**Local steps**

- If self.filters.ageing\_based\_on equals “Due Date”.
  - Set entry\_date from (row.due\_date or row.posting\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.due\_date → row.posting\_date.
- Otherwise.
  - If self.filters.ageing\_based\_on equals “Supplier Invoice Date”.
    - Set entry\_date from (row.bill\_date or row.posting\_date).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.bill\_date → row.posting\_date.
  - Otherwise.
    - Set entry\_date from row.posting\_date.
- Set row.range0 from 0.0.
- Evaluate self.get\_ageing\_data(entry\_date, row).
- If getdate(entry\_date) &gt; getdate(self.age\_as\_on).
  - Set row.range0 from row.outstanding.
  - Evaluate list of setattr(row, formatted text range{i}, 0.0) for i drawn from self.range\_numbers.
    - Draw i from self.range\_numbers.
  - Set row.total\_due from 0.
  - Return no value.
- Set row.total\_due from sum(generator of row at formatted text range{i} for i drawn from self.range\_numbers).
  - Draw i from self.range\_numbers.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get ageing data](operations-007.md#op-ee8be494ad6b31).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L591)

<a id="op-ee8be494ad6b31"></a>
### Receivable Payable Report.get ageing data

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_ageing_data`

**Inputs** self, entry\_date, row.

**Explicit results** no value.

**Local steps**

- Evaluate list of setattr(row, formatted text range{i}, 0.0) for i drawn from self.range\_numbers.
  - Draw i from self.range\_numbers.
- If not (self.age\_as\_on and entry\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.age\_as\_on → entry\_date.
  - Return no value.
- Set row.age from ((getdate(self.age\_as\_on) − getdate(entry\_date)).days or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (getdate(self.age\_as\_on) − getdate(entry\_date)).days → 0.
- Set index from next(generator of i for tuple(i, days) drawn from enumerate(self.ranges) where cint(row.age) ≤ cint(days), len(self.ranges)).
  - Draw tuple(i, days) from enumerate(self.ranges), keep a combination only if (cint(row.age) ≤ cint(days)).
- Set row at (“range” + str((index + 1))) from row.outstanding.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0217.json#L6687) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L565)

<a id="op-98b475fffa21fe"></a>
### Receivable Payable Report.prepare ple query

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_prepare_ple_query`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Evaluate self.prepare\_conditions().
- Evaluate self.qb\_selection\_filter.append(self.ple.posting\_date.lte(self.filters.report\_date)).
- Set ple from qb.DocType(“Payment Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.delink ….
- If self.filters.get(“show\_remarks”).
  - If remarks\_length bound to Platform.get\_single\_value(“Accounts Settings”, “receivable\_payable\_remarks\_length”).
    - Set query from query.select(Substring(ple.remarks, 1, remarks\_length).as\_(“remarks”)).
  - Otherwise.
    - Set query from query.select(ple.remarks).
- If match\_conditions bound to build\_qb\_match\_conditions(“Payment Ledger Entry”).
  - Set query from query.where(Criterion.all(match\_conditions)).
- If self.filters.get(“group\_by\_party”).
  - Set query from query.orderby(self.ple.party, self.ple.posting\_date).
- Otherwise.
  - Set query from query.orderby(self.ple.posting\_date, self.ple.party).
- Set self.ple\_query from query.

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare conditions](operations-008.md#op-a19fa26835c104).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “receivable\_payable\_remarks\_length”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L589)
