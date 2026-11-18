# Accounting and settlement · operations 118

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Trial balance for party

<a id="op-108c82fd2e469d"></a>
### Toggle debit credit

`operation_enterprise_accounts_report_trial_balance_for_party_business_behavior_toggle_debit_credit`

**Inputs** debit, credit.

**Explicit results** tuple(debit, credit).

**Local steps**

- If flt(debit) &gt; flt(credit).
  - Set debit from (flt(debit) − flt(credit)).
  - Set credit from 0.0.
- Otherwise.
  - Set credit from (flt(credit) − flt(debit)).
  - Set debit from 0.0.
- Return tuple(debit, credit).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0286.json#L7083) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1033) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L119)

<a id="op-cc82dc432c109e"></a>
### Get columns

`operation_enterprise_accounts_report_trial_balance_for_party_business_behavior_get_columns`

**Inputs** filters, show\_party\_name.

**State and service calls** call insert on columns.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “party”, “label” → translated filters.party\_type, “fieldtype” → “Link”, “options” → filters.party\_type, …), mapping(“fieldname” → “opening\_debit”, “label” → translated “Opening ( ….
- If show\_party\_name.
  - Evaluate columns.insert(1, mapping(“fieldname” → “party\_name”, “label” → (translated filters.party\_type + “ Name”), “fieldtype” → “Data”, “width” → 200)).
- Return columns.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1029) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L115)

<a id="op-ae48bcac6de8fc"></a>
### Is party name visible

`operation_enterprise_accounts_report_trial_balance_for_party_business_behavior_is_party_name_visible`

**Inputs** filters.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Buying Settings” via get\_single\_value.

**Explicit results** show\_party\_name.

**Local steps**

- Set show\_party\_name from false.
- If filters.get(“party\_type”) belongs to list(“Customer”, “Supplier”).
  - If filters.get(“party\_type”) equals “Customer”.
    - Set party\_naming\_by from Platform.get\_single\_value(“Selling Settings”, “cust\_master\_name”).
  - Otherwise.
    - Set party\_naming\_by from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”).
  - If party\_naming\_by equals “Naming Series”.
    - Set show\_party\_name from true.
- Otherwise.
  - Set show\_party\_name from true.
- Return show\_party\_name.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “cust\_master\_name”), Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L1081) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1032) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L118)

## Record · Unreconcile payment

[Record definition](../../../../data/record-types/unreconcile_payment.json)

<a id="op-0965c89cb53258"></a>
### Unreconcile Payment.validate

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_unreconcile_payment_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only {0} are supported”.format(comma\_and(self.supported\_types)).

**Local steps**

- Set self.supported\_types from SUPPORTED\_VOUCHER\_TYPES.
- If self.voucher\_type does not belong to self.supported\_types.
  - Call the validation error handler Platform.throw(translated “Only {0} are supported”.format(comma\_and(self.supported\_types))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L508)

<a id="op-6752916e850285"></a>
### Unreconcile Payment.get allocations from payment

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_unreconcile_payment_get_allocations_from_payment`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_linked\_payments\_for\_doc(company = self.company, doctype = self.voucher\_type, docname = self.voucher\_no).

**Local steps**

- Return get\_linked\_payments\_for\_doc(company = self.company, doctype = self.voucher\_type, docname = self.voucher\_no).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0209.json#L3467) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L506)

<a id="op-b8df7b131efaa0"></a>
### Unreconcile Payment.add references

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_unreconcile_payment_add_references`

**Inputs** self.

**Local steps**

- Set allocations from self.get\_allocations\_from\_payment().
- For each alloc in allocations.
  - Evaluate self.append(“allocations”, alloc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get allocations from payment](operations-118.md#op-6752916e850285).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0209.json#L3575) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L505)

<a id="op-53b65972dfbc0e"></a>
### Unreconcile Payment.on submit

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_unreconcile_payment_on_submit`

**Inputs** self.

**Record and data access** resolve a document from alloc.reference\_doctype via get\_doc.

**State and service calls** request set\_value on “Unreconcile Payment Entries”.

**Local steps**

- Evaluate self.cancel\_legacy\_return\_exchange\_journal().
- For each alloc in self.allocations.
  - Set doc from Platform.get\_doc(alloc.reference\_doctype, alloc.reference\_name).
  - Evaluate unlink\_ref\_doc\_from\_payment\_entries(doc, self.voucher\_no).
  - Evaluate cancel\_exchange\_gain\_loss\_journal(doc, self.voucher\_type, self.voucher\_no).
  - Evaluate update\_voucher\_outstanding(alloc.reference\_doctype, alloc.reference\_name, alloc.account, alloc.party\_type, …).
  - Evaluate Platform.db.set\_value(“Unreconcile Payment Entries”, alloc.name, “unlinked”, true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel legacy return exchange journal](operations-118.md#op-2470be8dd29662).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L507)

<a id="op-2470be8dd29662"></a>
### Unreconcile Payment.cancel legacy return exchange journal

`operation_enterprise_binding_enterprise_accounts_doctype_unreconcile_payment_unreconcile_payment_unreconcilepayment_cancel_legacy_return_exchange_journal`

**Inputs** self.

**Record and data access** resolve a document from “Journal Entry” via get\_doc · read row.reference\_type via get\_cached\_value · read return\_row.reference\_type via get\_cached\_value.

**State and service calls** call cancel on gain\_loss.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Exchange journal {0} could not be matched to reconciliation journal {1}.”.format(Platform.bold(gain\_loss.name), Platform.bold(journal.name)).

**Local steps**

- If self.voucher\_type differs from “Journal Entry”.
  - Return no value.
- Set journal from Platform.get\_doc(“Journal Entry”, self.voucher\_no).
- If not (journal.docstatus equals 1 and journal.is\_system\_generated and journal.voucher\_type belongs to tuple(“Credit Note”, “Debit Note”) and len(journal.accounts) equals 2).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in journal.docstatus equals 1 → journal.is\_system\_generated → journal.voucher\_type belongs to tuple(“Credit Note”, “Debit Note”) → len(journal.accounts) equals 2.
  - Return no value.
- Evaluate journal.check\_permission(“write”).
- Set return\_rows from list of row for row drawn from journal.accounts where (row.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and row.reference\_name and Platform.get\_cached\_value(row.reference\_type, row. ….
  - Draw row from journal.accounts, keep a combination only if ((row.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and row.reference\_name and Platform.get\_cached\_value(row.reference\_type, row.reference\_name, “is\_return”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) → row.reference\_name → Platform.get\_cached\_value(row.reference\_type, row.reference\_name, “is\_return”).
- <a id="op-2470be8dd29662-guard-22"></a>If len(return\_rows) differs from 1.
  - Return no value.
- Set return\_row from return\_rows at 0.
- Set invoice\_row from next(generator of row for row drawn from journal.accounts where row.name differs from return\_row.name).
  - Draw row from journal.accounts, keep a combination only if (row.name differs from return\_row.name).
- If not any(generator of (row.reference\_doctype equals return\_row.reference\_type and row.reference\_name equals return\_row.reference\_name) for row drawn from self.allocations).
  - Draw row from self.allocations.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_doctype equals return\_row.reference\_type → row.reference\_name equals return\_row.reference\_name.
  - Return no value.
- Set legacy\_journals from self.get\_legacy\_return\_exchange\_journals(journal, invoice\_row, return\_row).
- If not legacy\_journals.
  - Return no value.
- Evaluate self.validate\_legacy\_return\_exchange\_journal(journal, invoice\_row, return\_row, legacy\_journals).
- Set gain\_loss from legacy\_journals at 0.
- Set precision from gain\_loss.precision(“total\_debit”).
- Set amount from (return\_row.debit\_in\_account\_currency − return\_row.credit\_in\_account\_currency).
- Set return\_rate from Platform.get\_cached\_value(return\_row.reference\_type, return\_row.reference\_name, “conversion\_rate”).
- Set difference from (flt((amount × return\_rate), precision) − flt((amount × return\_row.exchange\_rate), precision)).
- If (gain\_loss.creation &lt; journal.creation or flt((sum(generator of (nested operand in the contract.debit − nested operand in the contract.credit) for row drawn from gain\_loss.accounts where nested operand in  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gain\_loss.creation &lt; journal.creation → flt((sum(generator of (row.debit − row.credit) for row drawn from gain\_loss.accounts where row.account equals return\_row.account) − difference), precision).
  - Draw row from gain\_loss.accounts, keep a combination only if (row.account equals return\_row.account).
  - Call the validation error handler Platform.throw(translated “Exchange journal {0} could not be matched to reconciliation journal {1}.”.format(Platform.bold(gain\_loss.name), Platform.bold(journal.name)), title = translated “Exchange Journal ….
- Evaluate gain\_loss.cancel().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(return\_rows) differs from 1, length of return\_rows = 2 selects the branch that returns no value. With length of return\_rows = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2470be8dd29662-guard-22)

**Methods declared on this owner** [get legacy return exchange journals](operations-118.md#op-6390726cd52a7a), [validate legacy return exchange journal](operations-118.md#op-2eda04ba105451).

**Values supplied outside this operation** effective access from journal.check\_permission(“write”) · configured or stored value from Platform.get\_cached\_value(row.reference\_type, row.reference\_name, “is\_return”), Platform.get\_cached\_value(return\_row.reference\_type, return\_row.reference\_name, “conversion\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1091)

<a id="op-6390726cd52a7a"></a>
### Unreconcile Payment.get legacy return exchange journals

`operation_enterprise_binding_enterprise_accounts_doctype_unreconcile_payment_unreconcile_payment_unreconcilepayment_get_legacy_return_exchange_journals`

**Inputs** self, journal, invoice\_row, return\_row.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**Explicit results** list() · legacy\_journals.

**Local steps**

- Set legacy\_journals from list().
- For each name in get\_linked\_exchange\_gain\_loss\_journal(return\_row.reference\_type, return\_row.reference\_name, 1).
  - Set gain\_loss from Platform.get\_doc(“Journal Entry”, name).
  - If any(generator of (row.reference\_type equals “Journal Entry” and row.reference\_name equals journal.name) for row drawn from gain\_loss.accounts).
    - Draw row from gain\_loss.accounts.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_type equals “Journal Entry” → row.reference\_name equals journal.name.
    - Return list().
  - If (len(gain\_loss.accounts) differs from 2 or gain\_loss.company differs from journal.company).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(gain\_loss.accounts) differs from 2 → gain\_loss.company differs from journal.company.
    - Continue with the next iteration or loop test.
  - Set party\_rows from gain\_loss.get(“accounts”, mapping(“account” → return\_row.account)).
  - <a id="op-6390726cd52a7a-guard-17"></a>If len(party\_rows) differs from 1.
    - Continue with the next iteration or loop test.
  - Set party\_row from party\_rows at 0.
  - Set reference\_row from next(generator of row for row drawn from gain\_loss.accounts where row.name differs from party\_row.name).
    - Draw row from gain\_loss.accounts, keep a combination only if (row.name differs from party\_row.name).
  - If (party\_row.reference\_type equals return\_row.reference\_type and party\_row.reference\_name equals return\_row.reference\_name and party\_row.party\_type equals return\_row.party\_type and party\_row.party equals ret ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_row.reference\_type equals return\_row.reference\_type → party\_row.reference\_name equals return\_row.reference\_name → party\_row.party\_type equals return\_row.party\_type → party\_row.party equals return\_row.party → reference\_row.reference\_type equals return\_row.reference\_type → (not invoice\_row.reference\_name or reference\_row.reference\_name equals invoice\_row.reference\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not invoice\_row.reference\_name → reference\_row.reference\_name equals invoice\_row.reference\_name.
    - Evaluate legacy\_journals.append(gain\_loss).
- Return legacy\_journals.

**Derived branch illustrations**

- At the comparison len(party\_rows) differs from 1, length of party\_rows = 2 selects the branch that continues with the next loop iteration. With length of party\_rows = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6390726cd52a7a-guard-17)

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1092)

<a id="op-2eda04ba105451"></a>
### Unreconcile Payment.validate legacy return exchange journal

`operation_enterprise_binding_enterprise_accounts_doctype_unreconcile_payment_unreconcile_payment_unreconcilepayment_validate_legacy_return_exchange_journal`

**Inputs** self, journal, invoice\_row, return\_row, legacy\_journals.

**Record and data access** read “Journal Entry Account” via get\_all · read “Journal Entry” via get\_all.

**Explicit failure paths** validation helper — translated “Cannot uniquely match exchange journals {0} to {1}. Review and cancel the matching exchange journal and reco …”.format(comma\_and(list of Platform.bold(row.name) for row drawn from legacy\_journa ….

**Local steps**

- Set linked\_journals from Platform.get\_all(“Journal Entry Account”, filters = mapping(“reference\_type” → return\_row.reference\_type, “reference\_name” → return\_row.reference\_name, “docstatus” → 1), pluck = “parent”).
- If invoice\_row.reference\_name.
  - Set linked\_journals from Platform.get\_all(“Journal Entry Account”, filters = mapping(“parent” → tuple(“in”, linked\_journals), “reference\_type” → invoice\_row.reference\_type, “reference\_name” → invoice\_row.reference\_name, “docstatus ….
- Set linked\_journals from Platform.get\_all(“Journal Entry”, filters = mapping(“name” → tuple(“in”, linked\_journals), “company” → journal.company, “voucher\_type” → journal.voucher\_type, “is\_system\_generated” → 1, …), pluck = “name”).
- If (len(legacy\_journals) differs from 1 or linked\_journals differs from list(journal.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(legacy\_journals) differs from 1 → linked\_journals differs from list(journal.name).
  - Call the validation error handler Platform.throw(translated “Cannot uniquely match exchange journals {0} to {1}. Review and cancel the matching exchange journal and reco …”.format(comma\_and(list of Platform.bold(row.name) for row drawn fro ….
    - Draw row from legacy\_journals.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1093)

<a id="op-2607226e84852c"></a>
### Doc has references

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_record_has_references`

**Inputs** doctype = no value, docname = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Payment Ledger Entry” via count · read “Advance Payment Ledger Entry” via count.

**Explicit results** count.

**Explicit failure paths** validation helper — translated “{0} and {1} are required”.format(Platform.bold(“doctype”), Platform.bold(“docname”)).

**Local steps**

- If (not doctype or not docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not docname.
  - Call the validation error handler Platform.throw(translated “{0} and {1} are required”.format(Platform.bold(“doctype”), Platform.bold(“docname”))).
- Evaluate Platform.has\_permission(doctype, “read”, doc = docname, throw = true).
- Set count from 0.
- If doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Set count from Platform.db.count(“Payment Ledger Entry”, filters = mapping(“delinked” → 0, “against\_voucher\_no” → docname, “amount” → list(“&lt;”, 0))).
- Otherwise.
  - Set count from Platform.db.count(“Payment Ledger Entry”, filters = mapping(“delinked” → 0, “voucher\_no” → docname, “against\_voucher\_no” → list(“!=”, docname))).
  - Update count using + Platform.db.count(“Advance Payment Ledger Entry”, filters = mapping(“delinked” → 0, “voucher\_no” → docname, “voucher\_type” → doctype, “event” → list(“=”, “Submit”))).
- Return count.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L504)

<a id="op-e3a682cc4a9727"></a>
### Get linked payments for doc

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_get_linked_payments_for_record`

**Inputs** company = no value, doctype = no value, docname = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Explicit results** res · list().

**Local steps**

- If (company and doctype and docname).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → doctype → docname.
  - Evaluate Platform.has\_permission(doctype, doc = docname, throw = true).
  - Set \_dt from doctype.
  - Set \_dn from docname.
  - Set ple from qb.DocType(“Payment Ledger Entry”).
  - If \_dt belongs to list(“Sales Invoice”, “Purchase Invoice”).
    - Set criteria from list(ple.company equals company, ple.delinked equals 0, ple.against\_voucher\_no equals \_dn, ple.amount &lt; 0).
    - Set res from nested operand in the contract(nested operand in the contract).groupby(ple.voucher\_no, ple.against\_voucher\_no).having(qb.Field(“allocated\_amount”) &gt; 0).run(as\_dict = true).
    - Return res.
  - Otherwise.
    - Set criteria from list(ple.company equals company, ple.delinked equals 0, ple.voucher\_no equals \_dn, ple.against\_voucher\_no differs from \_dn).
    - Set query from nested operand in the contract(nested operand in the contract).select(ple.company, ple.account, ple.party\_type, ple.party, …).where(Criterion.all(criteria)).groupby(ple.against\_voucher\_no).
    - Set res from query.run(as\_dict = true).
    - Update res using + get\_linked\_advances(company, \_dn).
    - Return res.
- Return list().

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L503)

<a id="op-c08e29b16f7000"></a>
### Get linked advances

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_get_linked_advances`

**Inputs** company, docname.

**Explicit results** nested operand in the contract(nested operand in the contract).having(nested operand in the contract(nested operand in the contract) &gt; 0).groupby(adv.against\_voucher\_no).run(as\_dict = true).

**Local steps**

- Set adv from qb.DocType(“Advance Payment Ledger Entry”).
- Set criteria from list(adv.company equals company, adv.delinked equals 0, adv.voucher\_no equals docname, adv.event equals “Submit”).
- Return nested operand in the contract(nested operand in the contract).having(nested operand in the contract(nested operand in the contract) &gt; 0).groupby(adv.against\_voucher\_no).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L502)

<a id="op-21eaf67ac5acdd"></a>
### Create unreconcile doc for selection

`operation_enterprise_accounts_record_definitions_unreconcile_payment_business_behavior_create_unreconcile_record_for_selection`

**Inputs** selections = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Unreconcile Payment” · call submit on unrecon.save() · call save on unrecon.

**Explicit failure paths** validation helper — translated “Only {0} are supported”.format(comma\_and(SUPPORTED\_VOUCHER\_TYPES)).

**Local steps**

- If selections.
  - If isinstance(selections, str).
    - Set selections from json.loads(selections).
  - For each row in selections.
    - If row.get(“voucher\_type”) does not belong to SUPPORTED\_VOUCHER\_TYPES.
      - Call the validation error handler Platform.throw(translated “Only {0} are supported”.format(comma\_and(SUPPORTED\_VOUCHER\_TYPES))).
    - Set row at “voucher\_no” from cstr(row.get(“voucher\_no”)).
    - If (not row at “voucher\_no” or not Platform.has\_permission(row.get(“voucher\_type”), “write”, doc = row at “voucher\_no”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row at “voucher\_no” → not Platform.has\_permission(row.get(“voucher\_type”), “write”, doc = row at “voucher\_no”).
      - Evaluate \_refuse().
  - For each row in selections.
    - Set unrecon from Platform.new\_doc(“Unreconcile Payment”).
    - Set unrecon.company from row.get(“company”).
    - Set unrecon.voucher\_type from row.get(“voucher\_type”).
    - Set unrecon.voucher\_no from row.get(“voucher\_no”).
    - Evaluate unrecon.add\_references().
    - Set unrecon.allocations from list of x for x drawn from unrecon.allocations where (x.reference\_doctype equals row.get(“against\_voucher\_type”) and x.reference\_name equals row.get(“against\_voucher\_no”)).
      - Draw x from unrecon.allocations, keep a combination only if ((x.reference\_doctype equals row.get(“against\_voucher\_type”) and x.reference\_name equals row.get(“against\_voucher\_no”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in x.reference\_doctype equals row.get(“against\_voucher\_type”) → x.reference\_name equals row.get(“against\_voucher\_no”).
    - Evaluate unrecon.save().submit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(row.get(“voucher\_type”), “write”, doc = row at “voucher\_no”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L501)

## Service · Utils

<a id="op-53347427fd9326"></a>
### Validate mandatory date range

`operation_enterprise_accounts_report_utils_business_behavior_validate_mandatory_date_range`

**Inputs** filters, from\_field = “from\_date”, to\_field = “to\_date”.

**Explicit failure paths** validation helper — translated “{0} and {1} are mandatory”.format(Platform.bold(translated “From Date”), Platform.bold(translated “To Date”)).

**Local steps**

- Set from\_date from filters.get(from\_field).
- Set to\_date from filters.get(to\_field).
- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Call the validation error handler Platform.throw(translated “{0} and {1} are mandatory”.format(Platform.bold(translated “From Date”), Platform.bold(translated “To Date”))).
- Evaluate validate\_date\_range(filters, from\_field, to\_field).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1075) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L146)

<a id="op-132a0bb5da5526"></a>
### Validate date range

`operation_enterprise_binding_enterprise_accounts_report_utils_validate_date_range`

**Inputs** filters, from\_field = “from\_date”, to\_field = “to\_date”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “From Date must be before To Date”.

**Local steps**

- If not filters.
  - Return no value.
- Set from\_date from filters.get(from\_field).
- Set to\_date from filters.get(to\_field).
- If (from\_date and to\_date and get\_datetime(from\_date) &gt; get\_datetime(to\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date → get\_datetime(from\_date) &gt; get\_datetime(to\_date).
  - Call the validation error handler Platform.throw(translated “From Date must be before To Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1282)

<a id="op-65f4c7ba99bfe8"></a>
### Get currency

`operation_enterprise_accounts_report_utils_business_behavior_get_currency`

**Inputs** filters.

**Explicit results** currency\_map.

**Local steps**

- Set company from get\_appropriate\_company(filters).
- Set company\_currency from get\_company\_currency(company).
- Set presentation\_currency from filters at “presentation\_currency” when filters.get(“presentation\_currency”), otherwise company\_currency.
  - Value choice on filters.get(“presentation\_currency”) — true gives filters at “presentation\_currency”, false gives company\_currency.
- Set report\_date from (filters.get(“to\_date”) or filters.get(“period\_end\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“to\_date”) → filters.get(“period\_end\_date”).
- If not report\_date.
  - Set fiscal\_year\_to\_date from get\_from\_and\_to\_date(filters.get(“to\_fiscal\_year”)) at “to\_date”.
  - Set report\_date from formatdate(get\_datetime\_str(fiscal\_year\_to\_date), “dd-MM-yyyy”).
- Set currency\_map from dict(company = company, company\_currency = company\_currency, presentation\_currency = presentation\_currency, report\_date = report\_date).
- Return currency\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L1709) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1065) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L136)

<a id="op-99f2971110d4d7"></a>
### Convert

`operation_enterprise_accounts_report_utils_business_behavior_convert`

**Inputs** value, from\_, to, date.

**Explicit results** converted\_value.

**Local steps**

- Set rate from get\_rate\_as\_at(date, from\_, to).
- Set converted\_value from (flt(value) ÷ rate).
- Return converted\_value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1060) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L131)

<a id="op-e3bfce61befb03"></a>
### Get rate as at

`operation_enterprise_accounts_report_utils_business_behavior_get_rate_as_at`

**Inputs** date, from\_currency, to\_currency.

**Explicit results** 1 · rate.

**Local steps**

- If from\_currency equals to\_currency.
  - Return 1.
- Set rate from \_\_exchange\_rates.get(formatted text {from\_currency}-{to\_currency}@{date}).
- If not rate.
  - Set rate from get\_exchange\_rate(from\_currency, to\_currency, date).
  - If not rate.
    - Evaluate throw\_missing\_exchange\_rate(date, from\_currency, to\_currency).
  - Set \_\_exchange\_rates at formatted text {from\_currency}-{to\_currency}@{date} from rate.
- Return rate.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1072) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L143)

<a id="op-9380bfb48a753a"></a>
### Throw missing exchange rate

`operation_enterprise_binding_enterprise_accounts_report_utils_throw_missing_exchange_rate`

**Inputs** date, from\_currency, to\_currency.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Exchange rate from {0} to {1} on {2} not found. Create a {3} record and run the report again.”.format(Platform.bold(from\_currency), Platform.bold(to\_currency), Platform.bold(formatdate(date)),  ….

**Local steps**

- Call the validation error handler Platform.throw(translated “Exchange rate from {0} to {1} on {2} not found. Create a {3} record and run the report again.”.format(Platform.bold(from\_currency), Platform.bold(to\_currency), Platform.bold(form ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L216) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1281)

<a id="op-a8ec0f62504bef"></a>
### Convert to presentation currency

`operation_enterprise_accounts_report_utils_business_behavior_convert_to_presentation_currency`

**Inputs** gl\_entries, currency\_info, filters = no value, use\_account\_currency = false.

**Record and data access** read “Company” via get\_value.

**Explicit results** converted\_gl\_list.

**Local steps**

- Set converted\_gl\_list from list().
- Set presentation\_currency from currency\_info at “presentation\_currency”.
- Set company\_currency from currency\_info at “company\_currency”.
- Set account\_currencies from list(set(generator of entry at “account\_currency” for entry drawn from gl\_entries)).
  - Draw entry from gl\_entries.
- Set exchange\_gain\_or\_loss from false.
- If (filters and isinstance(filters.get(“account”), list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → isinstance(filters.get(“account”), list).
  - Set account\_filter from filters.get(“account”).
  - Set gain\_loss\_account from Platform.db.get\_value(“Company”, filters.company, “exchange\_gain\_loss\_account”).
  - Set exchange\_gain\_or\_loss from (len(account\_filter) equals 1 and account\_filter at 0 equals gain\_loss\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(account\_filter) equals 1 → account\_filter at 0 equals gain\_loss\_account.
- For each entry in gl\_entries.
  - Set debit from flt(entry at “debit”).
  - Set credit from flt(entry at “credit”).
  - Set debit\_in\_account\_currency from flt(entry at “debit\_in\_account\_currency”).
  - Set credit\_in\_account\_currency from flt(entry at “credit\_in\_account\_currency”).
  - Set account\_currency from entry at “account\_currency”.
  - If (use\_account\_currency and len(account\_currencies) equals 1 and account\_currency equals presentation\_currency and not exchange\_gain\_or\_loss and not (filters and filters.get(“show\_amount\_in\_company\_currency”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in use\_account\_currency → len(account\_currencies) equals 1 → account\_currency equals presentation\_currency → not exchange\_gain\_or\_loss → not (filters and filters.get(“show\_amount\_in\_company\_currency”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“show\_amount\_in\_company\_currency”).
    - Set entry at “debit” from debit\_in\_account\_currency.
    - Set entry at “credit” from credit\_in\_account\_currency.
  - Otherwise.
    - Set date from currency\_info at “report\_date”.
    - Set converted\_debit\_value from convert(debit, presentation\_currency, company\_currency, date).
    - Set converted\_credit\_value from convert(credit, presentation\_currency, company\_currency, date).
    - If entry.get(“debit”).
      - Set entry at “debit” from converted\_debit\_value.
    - If entry.get(“credit”).
      - Set entry at “credit” from converted\_credit\_value.
  - Evaluate converted\_gl\_list.append(entry).
- Return converted\_gl\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1061) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L132)

<a id="op-8b7dc56403b6ff"></a>
### Get appropriate company

`operation_enterprise_accounts_report_utils_business_behavior_get_appropriate_company`

**Inputs** filters.

**Explicit results** company.

**Local steps**

- If filters.get(“company”).
  - Set company from filters at “company”.
- Otherwise.
  - Set company from get\_default\_company().
- Return company.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L3442) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1064) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L135)

<a id="op-77c9c886258207"></a>
### Get invoiced item gross margin

`operation_enterprise_accounts_report_utils_business_behavior_get_invoiced_item_gross_margin`

**Inputs** sales\_invoice = no value, item\_code = no value, company = no value, with\_item\_data = false.

**Record and data access** read “Sales Invoice” via get\_cached\_value.

**Explicit results** result.

**Local steps**

- Bind dependencies GrossProfitGenerator.
- Set sales\_invoice from (sales\_invoice or Platform.form\_dict.get(“sales\_invoice”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sales\_invoice → Platform.form\_dict.get(“sales\_invoice”).
- Set item\_code from (item\_code or Platform.form\_dict.get(“item\_code”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_code → Platform.form\_dict.get(“item\_code”).
- Set company from (company or Platform.get\_cached\_value(“Sales Invoice”, sales\_invoice, “company”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company → Platform.get\_cached\_value(“Sales Invoice”, sales\_invoice, “company”).
- Set filters from mapping(“sales\_invoice” → sales\_invoice, “item\_code” → item\_code, “company” → company, “group\_by” → “Invoice”).
- Set gross\_profit\_data from GrossProfitGenerator(filters).
- Set result from gross\_profit\_data.grouped\_data.
- If not with\_item\_data.
  - Set result from sum(generator of d.gross\_profit for d drawn from result).
    - Draw d from result.
- Return result.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Sales Invoice”, sales\_invoice, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1066) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L137)

<a id="op-fcb3c6a610f55f"></a>
### Get query columns

`operation_enterprise_accounts_report_utils_business_behavior_get_query_columns`

**Inputs** report\_columns.

**Explicit results** empty text · columns.

**Local steps**

- If not report\_columns.
  - Return empty text.
- Set columns from list().
- For each column in report\_columns.
  - Set fieldname from column at “fieldname”.
  - If doctype bound to column.get(“\_doctype”).
    - Evaluate columns.append(formatted text ′{get\_table\_name(doctype)}′.′{fieldname}′).
  - Otherwise.
    - Evaluate columns.append(fieldname).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L4014) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1071) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L142)
