# Accounting and settlement · operations 70

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment order

[Record definition](../../../../data/record-types/payment_order.json)

<a id="op-8777ccad985f45"></a>
### Make journal entry

`operation_enterprise_accounts_record_definitions_payment_order_business_behavior_make_journal_entry`

**Inputs** doc, supplier, mode\_of\_payment = no value.

**Record and data access** read “Mode of Payment” via get\_all.

**State and service calls** request new\_doc for “Journal Entry” · call save on je · msgprint with translated “{0} {1} created”.format(je.doctype, je.name).

**Local steps**

- Set rows from get\_unpaid\_rows(doc, supplier, mode\_of\_payment).
- Set je from Platform.new\_doc(“Journal Entry”).
- Set je.company from doc.company.
- Set je.payment\_order from doc.name.
- Set je.posting\_date from nowdate().
- Set mode\_of\_payment\_type from Platform.\_dict(Platform.get\_all(“Mode of Payment”, fields = list(“name”, “type”), as\_list = 1)).
- Set je.voucher\_type from “Bank Entry”.
- If (mode\_of\_payment and mode\_of\_payment\_type.get(mode\_of\_payment) equals “Cash”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in mode\_of\_payment → mode\_of\_payment\_type.get(mode\_of\_payment) equals “Cash”.
  - Set je.voucher\_type from “Cash Entry”.
- Set party\_account from get\_party\_account(“Supplier”, supplier, doc.company).
- For each d in rows.
  - Evaluate je.append(“accounts”, mapping(“account” → party\_account, “debit\_in\_account\_currency” → d.amount, “party\_type” → “Supplier”, “party” → supplier, …)).
- Evaluate je.append(“accounts”, mapping(“account” → doc.account, “credit\_in\_account\_currency” → sum(generator of d.amount for d drawn from rows))).
  - Draw d from rows.
- Set je.flags.ignore\_mandatory from true.
- Evaluate je.save().
- Evaluate set\_payment\_reference(list of d.name for d drawn from rows, je.name).
  - Draw d from rows.
- Evaluate Platform.msgprint(translated “{0} {1} created”.format(je.doctype, je.name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L225)

<a id="op-27fb8700912368"></a>
### Get unpaid rows

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_get_unpaid_rows`

**Inputs** doc, supplier, mode\_of\_payment = no value.

**Explicit results** rows.

**Explicit failure paths** validation helper — translated “Journal Entries are already created for Supplier {0}”.format(supplier).

**Local steps**

- Set rows from list of d for d drawn from doc.references where (d.supplier equals supplier and not d.payment\_reference and (not mode\_of\_payment or mode\_of\_payment equals d.mode\_of\_payment)).
  - Draw d from doc.references, keep a combination only if ((d.supplier equals supplier and not d.payment\_reference and (not mode\_of\_payment or mode\_of\_payment equals d.mode\_of\_payment))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.supplier equals supplier → not d.payment\_reference → (not mode\_of\_payment or mode\_of\_payment equals d.mode\_of\_payment).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not mode\_of\_payment → mode\_of\_payment equals d.mode\_of\_payment.
- If rows.
  - Set payment\_references from dict(Platform.qb.get\_query(“Payment Order Reference”, fields = list(“name”, “payment\_reference”), filters = mapping(“name” → list(“in”, list of nested operand in the contract for nested operand in the cont ….
    - Draw d from rows.
  - Set rows from list of d for d drawn from rows where not payment\_references.get(d.name).
    - Draw d from rows, keep a combination only if (not payment\_references.get(d.name)).
- If not rows.
  - Call the validation error handler Platform.throw(translated “Journal Entries are already created for Supplier {0}”.format(supplier)).
- Return rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L838)

<a id="op-1aeea7c58d20e6"></a>
### Set payment reference

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_set_payment_reference`

**Inputs** rows, journal\_entry.

**Local steps**

- Set order\_reference from Platform.qb.DocType(“Payment Order Reference”).
- Evaluate nested operand in the contract(nested operand in the contract).set(order\_reference.payment\_reference, journal\_entry).where(order\_reference.name.isin(rows)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L848)

<a id="op-bd4f19ad904d12"></a>
### Clear payment reference

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_clear_payment_reference`

**Inputs** journal\_entry.

**Explicit results** no value.

**Local steps**

- If not journal\_entry.payment\_order.
  - Return no value.
- Set order\_reference from Platform.qb.DocType(“Payment Order Reference”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.parent equals nested operand in the contract.payment\_order).where(order\_r ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L836)

<a id="op-4d261b26b87d5b"></a>
### Update payment requests from journal entry

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_update_payment_requests_from_journal_entry`

**Inputs** journal\_entry, cancel = false.

**Explicit results** no value.

**Local steps**

- If not journal\_entry.payment\_order.
  - Return no value.
- Set references from get\_payment\_request\_allocations(journal\_entry).
- Evaluate update\_payment\_requests\_as\_per\_pe\_references(references, cancel = cancel).
- If cancel.
  - Evaluate set\_payment\_requests\_as\_ordered(list of row.payment\_request for row drawn from references).
    - Draw row from references.
  - Evaluate clear\_payment\_reference(journal\_entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L850)

<a id="op-120bd889bc1fcf"></a>
### Get payment request allocations

`operation_enterprise_binding_enterprise_accounts_doctype_payment_order_payment_order_get_payment_request_allocations`

**Inputs** journal\_entry.

**Record and data access** read “Payment Order Reference” via get\_all.

**Explicit results** allocations.

**Local steps**

- Set paid\_amounts from defaultdict(float).
- For each row in journal\_entry.accounts.
  - If (row.reference\_type and row.reference\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_type → row.reference\_name.
    - Update paid\_amounts at tuple(row.reference\_type, row.reference\_name) using + flt(row.debit\_in\_account\_currency).
- Set allocations from list().
- For each row in Platform.get\_all(“Payment Order Reference”, filters = mapping(“parent” → journal\_entry.payment\_order, “parenttype” → “Payment Order”, “payment\_reference” → journal\_entry.name, “payment\_request” → list(“is” ….
  - Set key from tuple(row.reference\_doctype, row.reference\_name).
  - Set allocated\_amount from min(flt(row.amount), paid\_amounts at key).
  - Update paid\_amounts at key using − allocated\_amount.
  - If allocated\_amount &gt; 0.
    - Evaluate allocations.append(Platform.\_dict(payment\_request = row.payment\_request, allocated\_amount = allocated\_amount)).
- Return allocations.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L837)

<a id="op-3b1d27a1e9c32e"></a>
### Get data

`operation_enterprise_accounts_record_definitions_payment_order_payment_order_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payment\_order”, “transactions” → list(mapping(“items” → list(“Payment Entry”, “Journal Entry”)))).

**Local steps**

- Return mapping(“fieldname” → “payment\_order”, “transactions” → list(mapping(“items” → list(“Payment Entry”, “Journal Entry”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L5035) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L230)

## Report · Payment period based on invoice date

<a id="op-8ddbac327faa39"></a>
### Execute

`operation_enterprise_accounts_report_payment_period_based_on_invoice_date_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Set filters from mapping().
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- Set entries from get\_entries(filters).
- Set invoice\_details from get\_invoice\_posting\_date\_map(filters).
- Set report\_filters from Platform.\_dict(filters).
- Set report\_filters.range from “30, 60, 90”.
- Set report from ReceivablePayableReport(report\_filters).
- Set data from list().
- For each d in entries.
  - Set invoice from (invoice\_details.get(d.against\_voucher\_no) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in invoice\_details.get(d.against\_voucher\_no) → Platform.\_dict().
  - Set payment\_amount from d.amount.
  - Evaluate d.update(mapping(“range1” → 0, “range2” → 0, “range3” → 0, “range4” → 0, …)).
  - If d.against\_voucher\_no.
    - Set report.age\_as\_on from getdate(d.posting\_date).
    - Evaluate report.get\_ageing\_data(invoice.posting\_date, d).
  - Set row from list(d.voucher\_type, d.voucher\_no, d.party\_type, d.party, …).
  - If invoice.due\_date.
    - Evaluate row.append(((getdate(d.posting\_date) − getdate(invoice.due\_date)).days or 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (getdate(d.posting\_date) − getdate(invoice.due\_date)).days → 0.
  - Evaluate data.append(row).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L794) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1136)

<a id="op-50a2df209009d2"></a>
### Validate filters

`operation_enterprise_accounts_report_payment_period_based_on_invoice_date_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “{0} payment entries can not be filtered by {1}”.format(filters.payment\_type, filters.party\_type).

**Local steps**

- If ((filters.get(“payment\_type”) equals translated “Incoming” and filters.get(“party\_type”) equals “Supplier”) or (filters.get(“payment\_type”) equals translated “Outgoing” and filters.get(“party\_type”) equals ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (filters.get(“payment\_type”) equals translated “Incoming” and filters.get(“party\_type”) equals “Supplier”) → (filters.get(“payment\_type”) equals translated “Outgoing” and filters.get(“party\_type”) equals “Customer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“payment\_type”) equals translated “Incoming” → filters.get(“party\_type”) equals “Supplier”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“payment\_type”) equals translated “Outgoing” → filters.get(“party\_type”) equals “Customer”.
  - Call the validation error handler Platform.throw(translated “{0} payment entries can not be filtered by {1}”.format(filters.payment\_type, filters.party\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0267.json#L6393) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L799) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1141)

<a id="op-ef57dbf2ee1362"></a>
### Get columns

`operation_enterprise_accounts_report_payment_period_based_on_invoice_date_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“fieldname” → “payment\_document”, “label” → translated “Payment Document Type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“fieldname” → “payment\_entry”, “label” → translated “Pa ….

**Local steps**

- Return list(mapping(“fieldname” → “payment\_document”, “label” → translated “Payment Document Type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“fieldname” → “payment\_entry”, “label” → translated “Pa ….
  - Value choice on filters.get(“payment\_type”) equals translated “Outgoing” — true gives “Purchase Invoice”, false gives “Sales Invoice”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L795) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1137)

<a id="op-6274ca2147d9a9"></a>
### Get conditions

`operation_enterprise_accounts_report_payment_period_based_on_invoice_date_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set ple from qb.DocType(“Payment Ledger Entry”).
- Set conditions from list().
- Evaluate conditions.append(ple.delinked.eq(0)).
- Evaluate conditions.append(ple.voucher\_type.isin(list(“Payment Entry”, “Journal Entry”))).
- If filters.payment\_type equals translated “Outgoing”.
  - Set party\_type from “Supplier”.
  - Evaluate conditions.append(ple.against\_voucher\_type.eq(“Purchase Invoice”)).
- Otherwise.
  - Set party\_type from “Customer”.
  - Evaluate conditions.append(ple.against\_voucher\_type.eq(“Sales Invoice”)).
- Evaluate conditions.append(ple.party\_type.eq(party\_type)).
- If filters.party.
  - Evaluate conditions.append(ple.party.eq(filters.party)).
- If filters.get(“from\_date”).
  - Evaluate conditions.append(ple.posting\_date.gte(filters.get(“from\_date”))).
- If filters.get(“to\_date”).
  - Evaluate conditions.append(ple.posting\_date.lte(filters.get(“to\_date”))).
- If filters.get(“company”).
  - Evaluate conditions.append(ple.company.eq(filters.get(“company”))).
- Evaluate conditions.extend(build\_qb\_match\_conditions(“Payment Ledger Entry”)).
- If allowed\_parties bound to get\_allowed\_parties(party\_type).
  - Evaluate conditions.append(ple.party.isin(allowed\_parties)).
- Return conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L796) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1138)

<a id="op-5c54affaad8267"></a>
### Get allowed parties

`operation_enterprise_binding_enterprise_accounts_report_payment_period_based_on_invoice_date_payment_period_based_on_invoice_date_get_allowed_parties`

**Inputs** party\_type.

**Declared result** (list at str bitwise or no value).

**Explicit results** (get\_allowed\_docs\_for\_doctype(party\_permissions, “Payment Ledger Entry”) or no value).

**Local steps**

- Set party\_permissions from get\_user\_permissions().get(party\_type, list()).
- Return (get\_allowed\_docs\_for\_doctype(party\_permissions, “Payment Ledger Entry”) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_allowed\_docs\_for\_doctype(party\_permissions, “Payment Ledger Entry”) → no value.

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1247)

<a id="op-ed2571f94a4600"></a>
### Get entries

`operation_enterprise_accounts_report_payment_period_based_on_invoice_date_business_behavior_get_entries`

**Inputs** filters.

**Explicit results** (query.run(as\_dict = true) + get\_paid\_invoice\_entries(filters)).

**Local steps**

- Set ple from qb.DocType(“Payment Ledger Entry”).
- Set conditions from get\_conditions(filters).
- Set query from qb.from\_(ple).select(ple.voucher\_type, ple.voucher\_no, ple.party\_type, ple.party, …).where(Criterion.all(conditions)).
- Return (query.run(as\_dict = true) + get\_paid\_invoice\_entries(filters)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L797) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1139)

<a id="op-29d8b7c8cc5841"></a>
### Get paid invoice entries

`operation_enterprise_binding_enterprise_accounts_report_payment_period_based_on_invoice_date_payment_period_based_on_invoice_date_get_paid_invoice_entries`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** entries.

**Local steps**

- If filters.payment\_type equals translated “Outgoing”.
  - Set tuple(doctype, party\_type) from tuple(“Purchase Invoice”, “Supplier”).
  - Set invoice from qb.DocType(doctype).
  - Set tuple(party, paid\_amount) from tuple(invoice.supplier, invoice.base\_paid\_amount).
  - Set conditions from list(invoice.is\_paid.eq(1)).
- Otherwise.
  - Set tuple(doctype, party\_type) from tuple(“Sales Invoice”, “Customer”).
  - Set invoice from qb.DocType(doctype).
  - Set tuple(party, paid\_amount) from tuple(invoice.customer, (invoice.base\_paid\_amount − invoice.base\_change\_amount)).
  - Set conditions from list(invoice.is\_pos.eq(1)).
- Update conditions using + list(invoice.docstatus.eq(1), invoice.company.eq(filters.get(“company”)), paid\_amount.ne(0)).
- If filters.party.
  - Evaluate conditions.append(party.eq(filters.party)).
- If filters.get(“from\_date”).
  - Evaluate conditions.append(invoice.posting\_date.gte(filters.get(“from\_date”))).
- If filters.get(“to\_date”).
  - Evaluate conditions.append(invoice.posting\_date.lte(filters.get(“to\_date”))).
- Evaluate conditions.extend(build\_qb\_match\_conditions(doctype)).
- Set entries from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“voucher\_type”), nested operand in the contract.as\_(“voucher\_no”), nested operand in the contract.as ….
- For each entry in entries.
  - If (entry.is\_return and entry.return\_against and not entry.update\_outstanding\_for\_self).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.is\_return → entry.return\_against → not entry.update\_outstanding\_for\_self.
    - Set entry.against\_voucher\_no from entry.return\_against.
- Return entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1248)

<a id="op-ac7a32e33cc84c"></a>
### Get invoice posting date map

`operation_enterprise_accounts_report_payment_period_based_on_invoice_date_business_behavior_get_invoice_posting_date_map`

**Inputs** filters.

**Explicit results** invoice\_details.

**Local steps**

- Set invoice\_details from mapping().
- Set dt from qb.DocType(“Sales Invoice”) when filters.get(“payment\_type”) equals translated “Incoming”, otherwise qb.DocType(“Purchase Invoice”).
  - Value choice on filters.get(“payment\_type”) equals translated “Incoming” — true gives qb.DocType(“Sales Invoice”), false gives qb.DocType(“Purchase Invoice”).
- Set res from nested operand in the contract(nested operand in the contract).select(dt.name, dt.posting\_date, dt.due\_date).where((nested operand in the contract.docstatus.eq(1) bitwise and nested operand in the contract ….
- For each t in res.
  - Set invoice\_details at t.name from t.
- Return invoice\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0268.json#L2566) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L798) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1140)

## Record · Payment reconciliation

[Record definition](../../../../data/record-types/payment_reconciliation.json)

<a id="op-119a6b229843fc"></a>
### Payment Reconciliation.initialize

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.common\_filter\_conditions from list().
- Set self.accounting\_dimension\_filter\_conditions from list().
- Set self.ple\_posting\_date\_filter from list().
- Set self.dimensions from get\_dimensions(with\_cost\_center\_and\_project = true) at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L5924) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L13) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L264)

<a id="op-ea6e674aae0c38"></a>
### Payment Reconciliation.user permissions

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6103) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L20) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L271)

<a id="op-f3d59dad3183c3"></a>
### Payment Reconciliation.load from db

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_load_from_database`

**Inputs** self.

**Local steps**

- Set doc\_dict from Platform.\_dict(mapping(“modified” → no value, “company” → no value, “party” → no value, “party\_type” → no value, …)).
- Evaluate super(Document, self).\_\_init\_\_(doc\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6168) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L15) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L266)

<a id="op-1b84efb0a31d4a"></a>
### Payment Reconciliation.save

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_save`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6570) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L18) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L269)

<a id="op-77efa443e1331d"></a>
### Payment Reconciliation.get list

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_list`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6606) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L4) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L255)

<a id="op-09dacfabc7808a"></a>
### Payment Reconciliation.get count

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_count`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6644) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L248)

<a id="op-867038de240c50"></a>
### Payment Reconciliation.get stats

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_get_stats`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6682) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L10) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L261)

<a id="op-8d794731472529"></a>
### Payment Reconciliation.db insert

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6720) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L244)

<a id="op-21a46d278d0c6a"></a>
### Payment Reconciliation.db update

`operation_enterprise_accounts_record_definitions_payment_reconciliation_business_behavior_payment_reconciliation_database_update`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0092.json#L6763) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L245)
