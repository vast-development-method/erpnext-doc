# Accounting and settlement · operations 72

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment reconciliation

[Record definition](../../../../data/record-types/payment_reconciliation.json)

<a id="op-ad1ff0b85593e7"></a>
### Payment Reconciliation.validate entries

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_validate_entries`

**Inputs** self.

**Explicit failure paths** validation helper — translated “No records found in the Invoices table” · validation helper — translated “No records found in the Payments table”.

**Local steps**

- If not self.get(“invoices”).
  - Call the validation error handler Platform.throw(translated “No records found in the Invoices table”).
- If not self.get(“payments”).
  - Call the validation error handler Platform.throw(translated “No records found in the Payments table”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0094.json#L4159) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L22) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L273)

<a id="op-939daeda6f6d58"></a>
### Payment Reconciliation.get invoice exchange map

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_invoice_exchange_map`

**Inputs** self, invoices, payments.

**Record and data access** read “Sales Invoice” via get\_all · read “Purchase Invoice” via get\_all · read “Journal Entry Account” via get\_all.

**Explicit results** invoice\_exchange\_map.

**Local steps**

- Set sales\_invoices from list of d.get(“invoice\_number”) for d drawn from invoices where d.get(“invoice\_type”) equals “Sales Invoice”.
  - Draw d from invoices, keep a combination only if (d.get(“invoice\_type”) equals “Sales Invoice”).
- Evaluate sales\_invoices.extend(list of d.get(“reference\_name”) for d drawn from payments where d.get(“reference\_type”) equals “Sales Invoice”).
  - Draw d from payments, keep a combination only if (d.get(“reference\_type”) equals “Sales Invoice”).
- Set purchase\_invoices from list of d.get(“invoice\_number”) for d drawn from invoices where d.get(“invoice\_type”) equals “Purchase Invoice”.
  - Draw d from invoices, keep a combination only if (d.get(“invoice\_type”) equals “Purchase Invoice”).
- Evaluate purchase\_invoices.extend(list of d.get(“reference\_name”) for d drawn from payments where d.get(“reference\_type”) equals “Purchase Invoice”).
  - Draw d from payments, keep a combination only if (d.get(“reference\_type”) equals “Purchase Invoice”).
- Set invoice\_exchange\_map from Platform.\_dict().
- If sales\_invoices.
  - Set sales\_invoice\_map from Platform.\_dict(Platform.db.get\_all(“Sales Invoice”, filters = mapping(“name” → tuple(“in”, sales\_invoices)), fields = list(“name”, “conversion\_rate”), as\_list = 1)).
  - Evaluate invoice\_exchange\_map.update(sales\_invoice\_map).
- If purchase\_invoices.
  - Set purchase\_invoice\_map from Platform.\_dict(Platform.db.get\_all(“Purchase Invoice”, filters = mapping(“name” → tuple(“in”, purchase\_invoices)), fields = list(“name”, “conversion\_rate”), as\_list = 1)).
  - Evaluate invoice\_exchange\_map.update(purchase\_invoice\_map).
- Set journals from list of d.get(“invoice\_number”) for d drawn from invoices where d.get(“invoice\_type”) equals “Journal Entry”.
  - Draw d from invoices, keep a combination only if (d.get(“invoice\_type”) equals “Journal Entry”).
- Evaluate journals.extend(list of d.get(“reference\_name”) for d drawn from payments where d.get(“reference\_type”) equals “Journal Entry”).
  - Draw d from payments, keep a combination only if (d.get(“reference\_type”) equals “Journal Entry”).
- If journals.
  - Set journals from list(set(journals)).
  - Set journals\_map from Platform.\_dict(Platform.db.get\_all(“Journal Entry Account”, filters = mapping(“parent” → tuple(“in”, journals), “account” → tuple(“in”, list(self.receivable\_payable\_account)), “party\_type” → self.party\_typ ….
  - Evaluate invoice\_exchange\_map.update(journals\_map).
- Set payment\_entries from list of d.get(“invoice\_number”) for d drawn from invoices where d.get(“invoice\_type”) equals “Payment Entry”.
  - Draw d from invoices, keep a combination only if (d.get(“invoice\_type”) equals “Payment Entry”).
- Evaluate payment\_entries.extend(list of d.get(“reference\_name”) for d drawn from payments where d.get(“reference\_type”) equals “Payment Entry”).
  - Draw d from payments, keep a combination only if (d.get(“reference\_type”) equals “Payment Entry”).
- If payment\_entries.
  - Set pe from Platform.qb.DocType(“Payment Entry”).
  - Set query from nested operand in the contract.qb.from\_(pe).select(pe.name, nested operand in the contract.else\_(nested operand in the contract.target\_exchange\_rate).as\_(“exchange\_rate”)).where(pe.name.isin(payment\_entries)).
  - Set payment\_entries from query.run(as\_list = 1).
  - Evaluate invoice\_exchange\_map.update(payment\_entries).
- Return invoice\_exchange\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0094.json#L4336) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L252)

<a id="op-42cb853c17715b"></a>
### Payment Reconciliation.validate allocation

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_validate_allocation`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Allocated amount {1} must be less than or equal to remaining payment amount {2}”.format(row.idx, row.allocated\_amount, row.amount) · validation helper — translated “Row {0}: Allocated amount {1} must be less than or equal to invoice outstanding amount {2}”.format(row.idx, row.allocated\_amount, invoice\_outstanding) · validation helper — translated “No records found in Allocation table”.

**Local steps**

- Set unreconciled\_invoices from Platform.\_dict().
- For each inv in self.get(“invoices”).
  - Evaluate unreconciled\_invoices.setdefault(inv.invoice\_type, mapping()).setdefault(inv.invoice\_number, inv.outstanding\_amount).
- Set invoices\_to\_reconcile from list().
- For each row in self.get(“allocation”).
  - If (row.invoice\_type and row.invoice\_number and row.allocated\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.invoice\_type → row.invoice\_number → row.allocated\_amount.
    - Evaluate invoices\_to\_reconcile.append(row.invoice\_number).
    - If (flt(row.amount) − flt(row.allocated\_amount)) &lt; 0.
      - Call the validation error handler Platform.throw(translated “Row {0}: Allocated amount {1} must be less than or equal to remaining payment amount {2}”.format(row.idx, row.allocated\_amount, row.amount)).
    - Set invoice\_outstanding from unreconciled\_invoices.get(row.invoice\_type, mapping()).get(row.invoice\_number, 0).
    - If (flt(row.allocated\_amount) − invoice\_outstanding) &gt; 0.009.
      - Call the validation error handler Platform.throw(translated “Row {0}: Allocated amount {1} must be less than or equal to invoice outstanding amount {2}”.format(row.idx, row.allocated\_amount, invoice\_outstanding)).
    - Set unreconciled\_invoices.setdefault(row.invoice\_type, mapping()) at row.invoice\_number from (invoice\_outstanding − flt(row.allocated\_amount)).
- If not invoices\_to\_reconcile.
  - Call the validation error handler Platform.throw(translated “No records found in Allocation table”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L21) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L272)

<a id="op-7a45a020f17b67"></a>
### Payment Reconciliation.build dimensions filter conditions

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_build_dimensions_filter_conditions`

**Inputs** self.

**Local steps**

- Set ple from qb.DocType(“Payment Ledger Entry”).
- For each x in self.dimensions.
  - Set dimension from x.fieldname.
  - If Platform.db.has\_column(“Payment Ledger Entry”, dimension).
    - Set allowed from self.get\_permitted\_dimension\_values(x.document\_type, “Payment Ledger Entry”).
    - If value bound to self.get(dimension).
      - Evaluate self.validate\_permitted\_dimension\_value(x.document\_type, value, allowed).
      - Evaluate self.accounting\_dimension\_filter\_conditions.append(ple at dimension equals value).
    - Otherwise.
      - If allowed.
        - Evaluate self.accounting\_dimension\_filter\_conditions.append(self.get\_user\_permission\_dimension\_condition(ple at dimension, allowed)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get permitted dimension values](operations-071.md#op-2e897ef5d44960), [validate permitted dimension value](operations-071.md#op-0b75113f41e064), [get user permission dimension condition](operations-071.md#op-961c1f61748312).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0095.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L240)

<a id="op-20c7b8d5a28634"></a>
### Payment Reconciliation.build qb filter conditions

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_build_query_builder_filter_conditions`

**Inputs** self, get\_invoices = false, get\_return\_invoices = false.

**Local steps**

- Evaluate self.common\_filter\_conditions.clear().
- Evaluate self.accounting\_dimension\_filter\_conditions.clear().
- Evaluate self.ple\_posting\_date\_filter.clear().
- Set ple from qb.DocType(“Payment Ledger Entry”).
- Evaluate self.common\_filter\_conditions.append(ple.company equals self.company).
- If (self.get(“cost\_center”) and (get\_invoices or get\_return\_invoices)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“cost\_center”) → (get\_invoices or get\_return\_invoices).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_invoices → get\_return\_invoices.
  - Evaluate self.accounting\_dimension\_filter\_conditions.append(ple.cost\_center equals self.cost\_center).
- If get\_invoices.
  - If self.from\_invoice\_date.
    - Evaluate self.ple\_posting\_date\_filter.append(ple.posting\_date.gte(self.from\_invoice\_date)).
  - If self.to\_invoice\_date.
    - Evaluate self.ple\_posting\_date\_filter.append(ple.posting\_date.lte(self.to\_invoice\_date)).
- Otherwise.
  - If get\_return\_invoices.
    - If self.from\_payment\_date.
      - Evaluate self.ple\_posting\_date\_filter.append(ple.posting\_date.gte(self.from\_payment\_date)).
    - If self.to\_payment\_date.
      - Evaluate self.ple\_posting\_date\_filter.append(ple.posting\_date.lte(self.to\_payment\_date)).
- Evaluate self.build\_dimensions\_filter\_conditions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [build dimensions filter conditions](operations-072.md#op-7a45a020f17b67).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0095.json#L373) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L241)

<a id="op-74f414161b81c9"></a>
### Payment Reconciliation.get journal filter conditions

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_journal_filter_conditions`

**Inputs** self.

**Explicit results** conditions.

**Local steps**

- Set conditions from list().
- Set je from qb.DocType(“Journal Entry”).
- Evaluate qb.DocType(“Journal Entry Account”).
- Evaluate conditions.append(je.company equals self.company).
- If self.from\_payment\_date.
  - Evaluate conditions.append(je.posting\_date.gte(self.from\_payment\_date)).
- If self.to\_payment\_date.
  - Evaluate conditions.append(je.posting\_date.lte(self.to\_payment\_date)).
- If self.minimum\_payment\_amount.
  - Evaluate conditions.append(je.total\_debit.gte(self.minimum\_payment\_amount)).
- If self.maximum\_payment\_amount.
  - Evaluate conditions.append(je.total\_debit.lte(self.maximum\_payment\_amount)).
- Return conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0095.json#L968) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L2) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L253)

<a id="op-5b6f11a480679f"></a>
### Reconcile dr cr note

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_reconcile_debit_credit_note`

**Inputs** dr\_cr\_notes, company, active\_dimensions = no value.

**Record and data access** read inv.voucher\_type via get\_value · resolve a document from mapping(“doctype” → “Journal Entry”, “voucher\_type” → voucher\_type, “posting\_date” → (inv.get(“debit\_or\_credit\_note\_posting\_date”) or today()), “company” → company, …) via get\_doc.

**State and service calls** call submit on jv.

**Explicit failure paths** validation helper — translated “{0} has been modified after you pulled it. Please pull it again.”.format(inv.voucher\_type).

**Local steps**

- Set allocated\_amount\_precision from get\_field\_precision(Platform.get\_meta(“Payment Reconciliation Allocation”).get\_field(“allocated\_amount”)).
- For each inv in dr\_cr\_notes.
  - If flt((abs(nested operand in the contract.db.get\_value(inv.voucher\_type, inv.voucher\_no, “outstanding\_amount”)) − inv.allocated\_amount), allocated\_amount\_precision) &lt; 0.
    - Call the validation error handler Platform.throw(translated “{0} has been modified after you pulled it. Please pull it again.”.format(inv.voucher\_type)).
  - Set voucher\_type from “Credit Note” when inv.voucher\_type equals “Sales Invoice”, otherwise “Debit Note”.
    - Value choice on inv.voucher\_type equals “Sales Invoice” — true gives “Credit Note”, false gives “Debit Note”.
  - Set reconcile\_dr\_or\_cr from “debit\_in\_account\_currency” when inv.dr\_or\_cr equals “credit\_in\_account\_currency”, otherwise “credit\_in\_account\_currency”.
    - Value choice on inv.dr\_or\_cr equals “credit\_in\_account\_currency” — true gives “debit\_in\_account\_currency”, false gives “credit\_in\_account\_currency”.
  - Set company\_currency from Enterprise.get\_company\_currency(company).
  - Set jv from Platform.get\_doc(mapping(“doctype” → “Journal Entry”, “voucher\_type” → voucher\_type, “posting\_date” → (inv.get(“debit\_or\_credit\_note\_posting\_date”) or today()), “company” → company, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in inv.get(“debit\_or\_credit\_note\_posting\_date”) → today().
    - Value choice on inv.currency differs from company\_currency — true gives 1, false gives 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in inv.cost\_center → Enterprise.get\_default\_cost\_center(company).
    - Value choice on abs(inv.unadjusted\_amount) &gt; abs(inv.allocated\_amount) — true gives abs(inv.allocated\_amount), false gives abs(inv.unadjusted\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in inv.cost\_center → Enterprise.get\_default\_cost\_center(company).
  - Set dimensions\_dict from Platform.\_dict().
  - If active\_dimensions.
    - For each dim in active\_dimensions.
      - Set dimensions\_dict at dim.fieldname from inv.get(dim.fieldname).
  - Evaluate jv.accounts at 0.update(dimensions\_dict).
  - Evaluate jv.accounts at 1.update(dimensions\_dict).
  - Set jv.flags.ignore\_mandatory from true.
  - Set jv.flags.ignore\_exchange\_rate from true.
  - Set jv.remark from no value.
  - Set jv.flags.skip\_remarks\_creation from true.
  - Set jv.is\_system\_generated from true.
  - Evaluate jv.submit().
  - If inv.difference\_amount differs from 0.
    - If inv.party\_type equals “Customer”.
      - Set dr\_or\_cr from “credit” when inv.difference\_amount &lt; 0, otherwise “debit”.
        - Value choice on inv.difference\_amount &lt; 0 — true gives “credit”, false gives “debit”.
    - Otherwise.
      - Set dr\_or\_cr from “debit” when inv.difference\_amount &lt; 0, otherwise “credit”.
        - Value choice on inv.difference\_amount &lt; 0 — true gives “debit”, false gives “credit”.
    - Set reverse\_dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
      - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
    - Evaluate create\_gain\_loss\_journal(company, inv.difference\_posting\_date, inv.party\_type, inv.party, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L24) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L275)

<a id="op-11ac3e11e82f43"></a>
### Adjust allocations for taxes

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_adjust_allocations_for_taxes`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0095.json#L3239) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L235)

<a id="op-8ffb2cc37e7428"></a>
### Get queries for dimension filters

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_get_queries_for_dimension_filters`

**Inputs** company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** dimensions\_with\_filters.

**Local steps**

- Set dimensions\_with\_filters from list().
- For each d in get\_dimensions() at 0.
  - Set filters from mapping().
  - Set meta from Platform.get\_meta(d.document\_type).
  - If (meta.has\_field(“company”) and company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.has\_field(“company”) → company.
    - Evaluate filters.update(mapping(“company” → company)).
  - If meta.is\_tree.
    - Evaluate filters.update(mapping(“is\_group” → 0)).
  - Evaluate dimensions\_with\_filters.append(mapping(“fieldname” → d.fieldname, “filters” → filters)).
- Return dimensions\_with\_filters.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0095.json#L3281) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L236)

## Record · Payment reconciliation allocation

[Record definition](../../../../data/record-types/payment_reconciliation_allocation.json)

<a id="op-a70db83671287b"></a>
### Payment Reconciliation Allocation.get list

`operation_enterprise_accounts_record_definitions_payment_reconciliation_allocation_business_behavior_payment_reconciliation_allocation_get_list`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L4927) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L234)

## Record · Payment reconciliation invoice

[Record definition](../../../../data/record-types/payment_reconciliation_invoice.json)

<a id="op-3029d459f141fb"></a>
### Payment Reconciliation Invoice.get list

`operation_enterprise_accounts_record_definitions_payment_reconciliation_invoice_business_behavior_payment_reconciliation_invoice_get_list`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L4965) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L25) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L276)

## Record · Payment reconciliation payment

[Record definition](../../../../data/record-types/payment_reconciliation_payment.json)

<a id="op-11a7998bd6b6e8"></a>
### Payment Reconciliation Payment.get list

`operation_enterprise_accounts_record_definitions_payment_reconciliation_payment_business_behavior_payment_reconciliation_payment_get_list`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L5003) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L26) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L277)

## Record · Payment request

[Record definition](../../../../data/record-types/payment_request.json)

<a id="op-35088eb613c490"></a>
### Run as administrator

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_run_as_administrator`

**Inputs** no declared parameters.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set previous\_session from Platform.\_dict(Platform.session).
- Set previous\_form\_dict from Platform.local.form\_dict.
- Evaluate Platform.set\_user(“Administrator”).
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(previous\_session.user).
  - Evaluate Platform.local.session.update(previous\_session).
  - Set Platform.local.form\_dict from previous\_form\_dict.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L866)

<a id="op-8d934877b5806d"></a>
### Get payment gateway controller

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_get_payment_gateway_controller`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** get\_payment\_gateway\_controller(expanded args, expanded names kwargs).

**Local steps**

- Within payment\_app\_import\_guard().
  - Bind dependencies get\_payment\_gateway\_controller.
- Return get\_payment\_gateway\_controller(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L5041) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L343)

<a id="op-d8b2c29afc87c8"></a>
### Payment Request.on discard

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L5355) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L362)

<a id="op-c9dd6743588b9e"></a>
### Payment Request.validate

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_validate`

**Inputs** self.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**Local steps**

- Evaluate validate\_enabled\_mode\_of\_payment(self.mode\_of\_payment).
- If self.get(“\_\_islocal”).
  - Set self.status from “Draft”.
- Evaluate self.validate\_reference\_document().
- Set ref\_doc from Platform.get\_doc(self.reference\_doctype, self.reference\_name).
- If not self.flags.portal\_payment.
  - Evaluate ref\_doc.check\_permission(“read”).
- Evaluate self.validate\_reference\_company(ref\_doc).
- Evaluate self.validate\_party(ref\_doc).
- Evaluate self.validate\_bank\_account().
- Evaluate self.validate\_print\_format().
- Evaluate self.set\_payment\_references\_within\_requestable\_amount(ref\_doc).
- Evaluate self.validate\_against\_payment\_reference().
- Evaluate self.validate\_payment\_request\_amount(ref\_doc).
- Evaluate self.validate\_subscription\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reference document](operations-072.md#op-a6a19a71a1d9b3), [validate reference company](operations-072.md#op-15f2864f266c39), [validate party](operations-072.md#op-22736a1ae4b4ea), [validate bank account](operations-072.md#op-ea11af8859cd40), [validate print format](operations-072.md#op-33ef7e256f7976), [set payment references within requestable amount](operations-072.md#op-bb942b6194c51c), [validate against payment reference](operations-072.md#op-3a6a91f2226560), [validate payment request amount](operations-072.md#op-5f4fe49a71d92c), [validate subscription details](operations-073.md#op-3272cdcabf5863).

**Values supplied outside this operation** effective access from ref\_doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L373)

<a id="op-22736a1ae4b4ea"></a>
### Payment Request.validate party

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_paymentrequest_validate_party`

**Inputs** self, ref\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Party Type {0} is not valid for {1} {2}”.format(Platform.bold(translated self.party\_type), translated self.reference\_doctype, Platform.bold(self.reference\_name)) · validation helper — translated “{0} {1} is not the {0} of {2} {3}”.format(translated self.party\_type, Platform.bold(self.party), translated self.reference\_doctype, Platform.bold(self.reference\_name)).

**Local steps**

- If not self.party\_type.
  - Return no value.
- Set party\_field from Platform.scrub(self.party\_type).
- If not ref\_doc.meta.has\_field(party\_field).
  - Call the validation error handler Platform.throw(translated “Party Type {0} is not valid for {1} {2}”.format(Platform.bold(translated self.party\_type), translated self.reference\_doctype, Platform.bold(self.reference\_name)), title = transla ….
- If (self.party and self.party differs from ref\_doc.get(party\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party → self.party differs from ref\_doc.get(party\_field).
  - Call the validation error handler Platform.throw(translated “{0} {1} is not the {0} of {2} {3}”.format(translated self.party\_type, Platform.bold(self.party), translated self.reference\_doctype, Platform.bold(self.reference\_name)), title = t ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L863)

<a id="op-ea11af8859cd40"></a>
### Payment Request.validate bank account

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_paymentrequest_validate_bank_account`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Bank Account {0} is missing or disabled”.format(self.bank\_account) · validation helper — translated “Bank Account {0} does not belong to Company {1}”.format(self.bank\_account, self.company) · validation helper — translated “Bank Account {0} does not belong to {1} {2}”.format(self.bank\_account, self.party\_type, self.party).

**Local steps**

- If not self.bank\_account.
  - Return no value.
- Set bank\_account from Platform.get\_cached\_value(“Bank Account”, self.bank\_account, list(“disabled”, “is\_company\_account”, “company”, “party\_type”, …), as\_dict = true).
- If (not bank\_account or bank\_account.disabled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bank\_account → bank\_account.disabled.
  - Call the validation error handler Platform.throw(translated “Bank Account {0} is missing or disabled”.format(self.bank\_account)).
- If bank\_account.is\_company\_account.
  - If (not self.company or bank\_account.company differs from self.company).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.company → bank\_account.company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Bank Account {0} does not belong to Company {1}”.format(self.bank\_account, self.company)).
- Otherwise.
  - If (not self.party\_type or not self.party or bank\_account.party\_type differs from self.party\_type or bank\_account.party differs from self.party).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.party\_type → not self.party → bank\_account.party\_type differs from self.party\_type → bank\_account.party differs from self.party.
    - Call the validation error handler Platform.throw(translated “Bank Account {0} does not belong to {1} {2}”.format(self.bank\_account, self.party\_type, self.party)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Bank Account”, self.bank\_account, list(“disabled”, “is\_company\_account”, “company”, “party\_type”, …), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L862)

<a id="op-3a6a91f2226560"></a>
### Payment Request.validate against payment reference

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_validate_against_payment_reference`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Grand Total must match sum of Payment References” · validation helper — translated “Duplicate Payment Schedule selected”.

**Local steps**

- If not self.payment\_reference.
  - Return no value.
- Set expected from sum(generator of flt(r.amount) for r drawn from self.payment\_reference).
  - Draw r from self.payment\_reference.
- If flt(expected, self.precision(“grand\_total”)) differs from flt(self.grand\_total).
  - Call the validation error handler Platform.throw(translated “Grand Total must match sum of Payment References”).
- Set seen from set().
- For each r in self.payment\_reference.
  - If not r.payment\_schedule.
    - Continue with the next iteration or loop test.
  - If r.payment\_schedule belongs to seen.
    - Call the validation error handler Platform.throw(translated “Duplicate Payment Schedule selected”).
  - Evaluate seen.add(r.payment\_schedule).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0103.json#L5573) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L374)

<a id="op-a6a19a71a1d9b3"></a>
### Payment Request.validate reference document

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_validate_reference_document`

**Inputs** self.

**Explicit failure paths** validation helper — translated “To create a Payment Request reference document is required” · validation helper — translated “Payment Requests cannot be created against: {0}”.format(Platform.bold(self.reference\_doctype)).

**Local steps**

- If (not self.reference\_doctype or not self.reference\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.reference\_doctype → not self.reference\_name.
  - Call the validation error handler Platform.throw(translated “To create a Payment Request reference document is required”).
- If self.reference\_doctype does not belong to ALLOWED\_DOCTYPES\_FOR\_PAYMENT\_REQUEST.
  - Call the validation error handler Platform.throw(translated “Payment Requests cannot be created against: {0}”.format(Platform.bold(self.reference\_doctype))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L377)

<a id="op-33ef7e256f7976"></a>
### Payment Request.validate print format

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_paymentrequest_validate_print_format`

**Inputs** self.

**Record and data access** read “Print Format” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Print Format {0} is not valid for {1}”.format(Platform.bold(self.print\_format), translated self.reference\_doctype).

**Local steps**

- If (not self.print\_format or self.print\_format equals “Standard”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.print\_format → self.print\_format equals “Standard”.
  - Return no value.
- If Platform.db.get\_value(“Print Format”, self.print\_format, “doc\_type”) differs from self.reference\_doctype.
  - Call the validation error handler Platform.throw(translated “Print Format {0} is not valid for {1}”.format(Platform.bold(self.print\_format), translated self.reference\_doctype), title = translated “Invalid Print Format”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L864)

<a id="op-15f2864f266c39"></a>
### Payment Request.validate reference company

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_paymentrequest_validate_reference_company`

**Inputs** self, ref\_doc.

**Explicit failure paths** validation helper — translated “Company {0} does not match the company {1} of {2} {3}”.format(Platform.bold(self.company), Platform.bold(ref\_doc.company), translated self.reference\_doctype, Platform.bold(self.reference\_name)).

**Local steps**

- If self.company differs from ref\_doc.company.
  - Call the validation error handler Platform.throw(translated “Company {0} does not match the company {1} of {2} {3}”.format(Platform.bold(self.company), Platform.bold(ref\_doc.company), translated self.reference\_doctype, Platform.bold(self.r ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L865)

<a id="op-5f4fe49a71d92c"></a>
### Payment Request.validate payment request amount

`operation_enterprise_accounts_record_definitions_payment_request_business_behavior_payment_request_validate_payment_request_amount`

**Inputs** self, ref\_doc.

**Explicit failure paths** validation helper — translated “{0} cannot be zero”.format(self.get\_label\_from\_fieldname(“grand\_total”)) · validation helper — translated “Payment Entry is already created” · validation helper — translated “Total Payment Request amount cannot be greater than {0} amount”.format(self.reference\_doctype).

**Local steps**

- <a id="op-5f4fe49a71d92c-guard-2"></a>If self.grand\_total equals 0.
  - Call the validation error handler Platform.throw(translated “{0} cannot be zero”.format(self.get\_label\_from\_fieldname(“grand\_total”)), title = translated “Invalid Amount”).
- If (not hasattr(ref\_doc, “order\_type”) or ref\_doc.order\_type differs from “Shopping Cart”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(ref\_doc, “order\_type”) → ref\_doc.order\_type differs from “Shopping Cart”.
  - Set ref\_amount from get\_amount(ref\_doc, self.payment\_account).
  - If not ref\_amount.
    - Call the validation error handler Platform.throw(translated “Payment Entry is already created”).
  - Set existing\_payment\_request\_amount from flt(get\_existing\_payment\_request\_amount(ref\_doc)).
  - If flt((existing\_payment\_request\_amount + flt(self.grand\_total, self.precision(“grand\_total”))), get\_currency\_precision()) &gt; ref\_amount.
    - Call the validation error handler Platform.throw(translated “Total Payment Request amount cannot be greater than {0} amount”.format(self.reference\_doctype)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.grand\_total equals 0, self.grand\_total = 0 selects the branch that calls the validation-error handler with translated “{0} cannot be zero”.format(self.get\_label\_from\_fieldname(“grand\_total”)). With self.grand\_total = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5f4fe49a71d92c-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L376)

<a id="op-bb942b6194c51c"></a>
### Payment Request.set payment references within requestable amount

`operation_enterprise_binding_enterprise_accounts_doctype_payment_request_payment_request_paymentrequest_set_payment_references_within_requestable_amount`

**Inputs** self, ref\_doc.

**Explicit results** no value.

**Local steps**

- If (not self.payment\_reference or ref\_doc.get(“order\_type”) equals “Shopping Cart”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.payment\_reference → ref\_doc.get(“order\_type”) equals “Shopping Cart”.
  - Return no value.
- Set precision from self.precision(“grand\_total”).
- Set requestable\_amount from (get\_amount(ref\_doc, self.payment\_account) − flt(get\_existing\_payment\_request\_amount(ref\_doc))).
- Set excess from flt((sum(generator of flt(row.amount) for row drawn from self.payment\_reference) − requestable\_amount), precision).
  - Draw row from self.payment\_reference.
- If (excess ≤ 0 or excess &gt; get\_payment\_schedule\_rounding\_difference(ref\_doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in excess ≤ 0 → excess &gt; get\_payment\_schedule\_rounding\_difference(ref\_doc).
  - Return no value.
- Set last\_reference from self.payment\_reference at negative 1.
- Set last\_reference.amount from flt((last\_reference.amount − excess), precision).
- Set self.grand\_total from flt((self.grand\_total − excess), precision).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L861)
