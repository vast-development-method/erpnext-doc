# Accounting and settlement · operations 120

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-f0c6d1040fd9e8"></a>
### Check if advance entry modified

`operation_enterprise_accounts_utils_business_behavior_check_if_advance_entry_modified`

**Inputs** args.

**Local steps**

- If not args.get(“unreconciled\_amount”).
  - Evaluate args.update(mapping(“unreconciled\_amount” → args.get(“unadjusted\_amount”))).
- Set ret from no value.
- If args.voucher\_type equals “Journal Entry”.
  - Set journal\_entry from Platform.qb.DocType(“Journal Entry”).
  - Set journal\_acc from Platform.qb.DocType(“Journal Entry Account”).
  - Set q from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(journal\_acc at args.get(“dr\_or\_cr”)).where(((((((n ….
- Otherwise.
  - Set precision from Platform.get\_precision(“Payment Entry”, “unallocated\_amount”).
  - Set payment\_entry from Platform.qb.DocType(“Payment Entry”).
  - Set payment\_ref from Platform.qb.DocType(“Payment Entry Reference”).
  - Set q from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(payment\_entry.party\_type equals args.get(“party\_type”)).where(payment\_entry.par ….
  - If args.voucher\_detail\_no.
    - Set q from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name equals nested operand in the contract(nested operand in the contract)).where(payment\_ref.reference\_d ….
  - Otherwise.
    - Set q from q.where(Round(payment\_entry.unallocated\_amount, precision) equals Round(args.get(“unreconciled\_amount”), precision)).
- Set ret from q.run(as\_dict = true).
- If not ret.
  - Evaluate throw(translated “Payment Entry has been modified after you pulled it. Please pull it again.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L187)

<a id="op-9fd015dca89b69"></a>
### Validate allocated amount

`operation_enterprise_accounts_utils_business_behavior_validate_allocated_amount`

**Inputs** args.

**Record and data access** read “System Settings” via get\_single\_value.

**Local steps**

- Set precision from (args.get(“precision”) or Platform.db.get\_single\_value(“System Settings”, “currency\_precision”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“precision”) → Platform.db.get\_single\_value(“System Settings”, “currency\_precision”).
- If args.get(“allocated\_amount”) &lt; 0.
  - Evaluate throw(translated “Allocated amount cannot be negative”).
- Otherwise.
  - If flt(args.get(“allocated\_amount”), precision) &gt; flt(args.get(“unadjusted\_amount”), precision).
    - Evaluate throw(translated “Allocated amount cannot be greater than unadjusted amount”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “currency\_precision”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L1493) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L256)

<a id="op-817831f011dd31"></a>
### Update reference in journal entry

`operation_enterprise_accounts_utils_business_behavior_update_reference_in_journal_entry`

**Inputs** d, journal\_entry, do\_not\_save = false.

**State and service calls** call save on journal\_entry.

**Explicit results** new\_row.

**Local steps**

- Set jv\_detail from journal\_entry.get(“accounts”, mapping(“name” → d at “voucher\_detail\_no”)) at 0.
- Set rev\_dr\_or\_cr from “debit\_in\_account\_currency” when d at “dr\_or\_cr” equals “credit\_in\_account\_currency”, otherwise “credit\_in\_account\_currency”.
  - Value choice on d at “dr\_or\_cr” equals “credit\_in\_account\_currency” — true gives “debit\_in\_account\_currency”, false gives “credit\_in\_account\_currency”.
- If jv\_detail.get(rev\_dr\_or\_cr).
  - Set d at “dr\_or\_cr” from rev\_dr\_or\_cr.
  - Set d at “allocated\_amount” from (d at “allocated\_amount” × negative 1).
  - Set d at “unadjusted\_amount” from (d at “unadjusted\_amount” × negative 1).
- Set insert\_position from negative 1.
- If (flt(d at “unadjusted\_amount”) − flt(d at “allocated\_amount”)) differs from 0.
  - Set amount\_in\_account\_currency from (flt(d at “unadjusted\_amount”) − flt(d at “allocated\_amount”)).
  - Set amount\_in\_company\_currency from (amount\_in\_account\_currency × flt(jv\_detail.exchange\_rate)).
  - Evaluate jv\_detail.set(d at “dr\_or\_cr”, amount\_in\_account\_currency).
  - Evaluate jv\_detail.set(“debit” when d at “dr\_or\_cr” equals “debit\_in\_account\_currency”, otherwise “credit”, amount\_in\_company\_currency).
    - Value choice on d at “dr\_or\_cr” equals “debit\_in\_account\_currency” — true gives “debit”, false gives “credit”.
- Otherwise.
  - Evaluate journal\_entry.remove(jv\_detail).
  - Update insert\_position using + jv\_detail.idx.
- Set new\_row from journal\_entry.append(“accounts”, position = insert\_position).
- Evaluate list of new\_row.set(field, jv\_detail.get(field)) for field drawn from Platform.get\_meta(“Journal Entry Account”).get\_fieldnames\_with\_value().
  - Draw field from Platform.get\_meta(“Journal Entry Account”).get\_fieldnames\_with\_value().
- Evaluate new\_row.set(d at “dr\_or\_cr”, d at “allocated\_amount”).
- Evaluate new\_row.set(“debit” when d at “dr\_or\_cr” equals “debit\_in\_account\_currency”, otherwise “credit”, (d at “allocated\_amount” × flt(jv\_detail.exchange\_rate))).
  - Value choice on d at “dr\_or\_cr” equals “debit\_in\_account\_currency” — true gives “debit”, false gives “credit”.
- Evaluate new\_row.set(“credit\_in\_account\_currency” when d at “dr\_or\_cr” equals “debit\_in\_account\_currency”, otherwise “debit\_in\_account\_currency”, 0).
  - Value choice on d at “dr\_or\_cr” equals “debit\_in\_account\_currency” — true gives “credit\_in\_account\_currency”, false gives “debit\_in\_account\_currency”.
- Evaluate new\_row.set(“credit” when d at “dr\_or\_cr” equals “debit\_in\_account\_currency”, otherwise “debit”, 0).
  - Value choice on d at “dr\_or\_cr” equals “debit\_in\_account\_currency” — true gives “credit”, false gives “debit”.
- Evaluate new\_row.set(“reference\_type”, d at “against\_voucher\_type”).
- Evaluate new\_row.set(“reference\_name”, d at “against\_voucher”).
- Set new\_row.against\_account from cstr(jv\_detail.against\_account).
- Set new\_row.is\_advance from cstr(jv\_detail.is\_advance).
- Set new\_row.docstatus from 1.
- If jv\_detail.get(“reference\_type”) belongs to get\_advance\_payment\_doctypes().
  - Set new\_row.advance\_voucher\_type from jv\_detail.get(“reference\_type”).
  - Set new\_row.advance\_voucher\_no from jv\_detail.get(“reference\_name”).
- Set journal\_entry.flags.ignore\_validate\_update\_after\_submit from true.
- Set journal\_entry.flags.ignore\_reposting\_on\_reconciliation from true.
- If not do\_not\_save.
  - Evaluate journal\_entry.save(ignore\_permissions = true).
- Return new\_row.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L1802) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L252)

<a id="op-073569c49e74c6"></a>
### Update reference in payment entry

`operation_enterprise_accounts_utils_business_behavior_update_reference_in_payment_entry`

**Inputs** d, payment\_entry, do\_not\_save = false, skip\_ref\_details\_update\_for\_pe = false, dimensions\_dict = no value.

**State and service calls** call save on payment\_entry.

**Explicit results** row.

**Local steps**

- Set reference\_details from mapping(“reference\_doctype” → d.against\_voucher\_type, “reference\_name” → d.against\_voucher, “total\_amount” → d.grand\_total, “outstanding\_amount” → d.outstanding\_amount, …).
  - Value choice on d.difference\_amount is distinct from no value — true gives d.exchange\_rate, false gives payment\_entry.get\_exchange\_rate().
- Set advance\_payment\_doctypes from get\_advance\_payment\_doctypes().
- If payment\_entry.book\_advance\_payments\_in\_separate\_party\_account.
  - Set reconcile\_on from get\_reconciliation\_effect\_date(d.against\_voucher\_type, d.against\_voucher, payment\_entry.company, payment\_entry.posting\_date).
  - Evaluate reference\_details.update(mapping(“reconcile\_effect\_on” → reconcile\_on)).
- If d.voucher\_detail\_no.
  - Set existing\_row from payment\_entry.get(“references”, mapping(“name” → d at “voucher\_detail\_no”)) at 0.
  - If d.allocated\_amount ≤ existing\_row.allocated\_amount.
    - Update existing\_row.allocated\_amount using − d.allocated\_amount.
    - Set new\_row from payment\_entry.append(“references”).
    - Set new\_row.docstatus from 1.
    - For each field in list(reference\_details).
      - Evaluate new\_row.set(field, reference\_details at field).
    - If existing\_row.reference\_doctype belongs to advance\_payment\_doctypes.
      - Set new\_row.advance\_voucher\_type from existing\_row.reference\_doctype.
      - Set new\_row.advance\_voucher\_no from existing\_row.reference\_name.
      - Set new\_row.payment\_request from existing\_row.payment\_request.
    - Set row from new\_row.
- Otherwise.
  - Set new\_row from payment\_entry.append(“references”).
  - Set new\_row.docstatus from 1.
  - Evaluate new\_row.update(reference\_details).
  - Set row from new\_row.
- Set payment\_entry.flags.ignore\_validate\_update\_after\_submit from true.
- Evaluate payment\_entry.clear\_unallocated\_reference\_document\_rows().
- Evaluate payment\_entry.setup\_party\_account\_field().
- Evaluate payment\_entry.set\_missing\_values().
- If not skip\_ref\_details\_update\_for\_pe.
  - Set reference\_exchange\_details from Platform.\_dict().
  - If (d.against\_voucher\_type equals “Journal Entry” and d.exchange\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.against\_voucher\_type equals “Journal Entry” → d.exchange\_rate.
    - Evaluate reference\_exchange\_details.update(mapping(“reference\_doctype” → d.against\_voucher\_type, “reference\_name” → d.against\_voucher, “exchange\_rate” → d.exchange\_rate)).
  - Evaluate payment\_entry.set\_missing\_ref\_details(update\_ref\_details\_only\_for = list(tuple(d.against\_voucher\_type, d.against\_voucher)), reference\_exchange\_details = reference\_exchange\_details).
- Evaluate payment\_entry.set\_amounts().
- Evaluate payment\_entry.make\_exchange\_gain\_loss\_journal(Platform.\_dict(mapping(“difference\_posting\_date” → d.difference\_posting\_date)), dimensions\_dict).
- Set payment\_entry.flags.ignore\_reposting\_on\_reconciliation from true.
- If not do\_not\_save.
  - Evaluate payment\_entry.save(ignore\_permissions = true).
- Return row.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L253)

<a id="op-b424d30637f4a0"></a>
### Get reconciliation effect date

`operation_enterprise_accounts_utils_business_behavior_get_reconciliation_effect_date`

**Inputs** against\_voucher\_type, against\_voucher, company, posting\_date.

**Record and data access** read “Company” via get\_cached\_value · read against\_voucher\_type via get\_value.

**Explicit results** reconcile\_on.

**Local steps**

- Set reconciliation\_takes\_effect\_on from Platform.get\_cached\_value(“Company”, company, “reconciliation\_takes\_effect\_on”).
- Set reconcile\_on from posting\_date.
- If reconciliation\_takes\_effect\_on equals “Advance Payment Date”.
  - Set reconcile\_on from posting\_date.
- Otherwise.
  - If reconciliation\_takes\_effect\_on equals “Oldest Of Invoice Or Advance”.
    - Set date\_field from “posting\_date”.
    - If against\_voucher\_type belongs to list(“Sales Order”, “Purchase Order”).
      - Set date\_field from “transaction\_date”.
    - Set reconcile\_on from Platform.db.get\_value(against\_voucher\_type, against\_voucher, date\_field).
    - If getdate(reconcile\_on) &lt; getdate(posting\_date).
      - Set reconcile\_on from posting\_date.
  - Otherwise.
    - If reconciliation\_takes\_effect\_on equals “Reconciliation Date”.
      - Set reconcile\_on from nowdate().
- Return reconcile\_on.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “reconciliation\_takes\_effect\_on”) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L4572) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L228)

<a id="op-074ce6fe7f1a52"></a>
### Cancel exchange gain loss journal

`operation_enterprise_accounts_utils_business_behavior_cancel_exchange_gain_loss_journal`

**Inputs** parent\_doc, referenced\_dt = no value, referenced\_dn = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call cancel on gain\_loss\_je.

**Local steps**

- If parent\_doc.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”, “Payment Entry”, “Journal Entry”).
  - Set gain\_loss\_journals from get\_linked\_exchange\_gain\_loss\_journal(referenced\_dt = parent\_doc.doctype, referenced\_dn = parent\_doc.name, je\_docstatus = 1).
  - For each doc in gain\_loss\_journals.
    - Set gain\_loss\_je from Platform.get\_doc(“Journal Entry”, doc).
    - If (referenced\_dt and referenced\_dn).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in referenced\_dt → referenced\_dn.
      - Set references from list of tuple(x.reference\_type, x.reference\_name) for x drawn from gain\_loss\_je.accounts.
        - Draw x from gain\_loss\_je.accounts.
      - If (len(references) equals 2 and tuple(referenced\_dt, referenced\_dn) belongs to references and tuple(parent\_doc.doctype, parent\_doc.name) belongs to references).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(references) equals 2 → tuple(referenced\_dt, referenced\_dn) belongs to references → tuple(parent\_doc.doctype, parent\_doc.name) belongs to references.
        - Evaluate gain\_loss\_je.cancel().
    - Otherwise.
      - Evaluate gain\_loss\_je.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L4975) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L185)

<a id="op-73278788f637c5"></a>
### Delete exchange gain loss journal

`operation_enterprise_accounts_utils_business_behavior_delete_exchange_gain_loss_journal`

**Inputs** parent\_doc, referenced\_dt = no value, referenced\_dn = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**Local steps**

- If parent\_doc.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”, “Payment Entry”, “Journal Entry”).
  - Set gain\_loss\_journals from get\_linked\_exchange\_gain\_loss\_journal(referenced\_dt = parent\_doc.doctype, referenced\_dn = parent\_doc.name, je\_docstatus = 2).
  - For each doc in gain\_loss\_journals.
    - Set gain\_loss\_je from Platform.get\_doc(“Journal Entry”, doc).
    - If (referenced\_dt and referenced\_dn).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in referenced\_dt → referenced\_dn.
      - Set references from list of tuple(x.reference\_type, x.reference\_name) for x drawn from gain\_loss\_je.accounts.
        - Draw x from gain\_loss\_je.accounts.
      - If (len(references) equals 2 and tuple(referenced\_dt, referenced\_dn) belongs to references and tuple(parent\_doc.doctype, parent\_doc.name) belongs to references).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(references) equals 2 → tuple(referenced\_dt, referenced\_dn) belongs to references → tuple(parent\_doc.doctype, parent\_doc.name) belongs to references.
        - Evaluate gain\_loss\_je.delete().
    - Otherwise.
      - Evaluate gain\_loss\_je.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L5455) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L196)

<a id="op-a41ce8f01c6f0c"></a>
### Get linked exchange gain loss journal

`operation_enterprise_accounts_utils_business_behavior_get_linked_exchange_gain_loss_journal`

**Inputs** referenced\_dt, referenced\_dn, je\_docstatus.

**Declared result** list.

**Record and data access** read “Journal Entry Account” via get\_all · read “Journal Entry” via get\_all.

**Explicit results** gain\_loss\_journals.

**Local steps**

- Set gain\_loss\_journals from list().
- If journals bound to Platform.db.get\_all(“Journal Entry Account”, mapping(“reference\_type” → referenced\_dt, “reference\_name” → referenced\_dn, “docstatus” → je\_docstatus), pluck = “parent”).
  - Set gain\_loss\_journals from Platform.db.get\_all(“Journal Entry”, mapping(“name” → list(“in”, journals), “voucher\_type” → “Exchange Gain Or Loss”, “is\_system\_generated” → 1, “docstatus” → je\_docstatus), pluck = “name”).
- Return gain\_loss\_journals.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L5935) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L223)

<a id="op-c4b8c2da891777"></a>
### Cancel common party journal

`operation_enterprise_accounts_utils_business_behavior_cancel_common_party_journal`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Journal Entry Account” via get\_value · read “Journal Entry” via get\_value · resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call cancel on common\_party\_je.

**Explicit results** no value.

**Local steps**

- If self.doctype does not belong to list(“Sales Invoice”, “Purchase Invoice”).
  - Return no value.
- If not Platform.get\_single\_value(“Accounts Settings”, “enable\_common\_party\_accounting”).
  - Return no value.
- Set party\_link from self.get\_common\_party\_link().
- If not party\_link.
  - Return no value.
- Set journal\_entry from Platform.db.get\_value(“Journal Entry Account”, filters = mapping(“reference\_type” → self.doctype, “reference\_name” → self.name, “docstatus” → 1), fieldname = “parent”).
- If not journal\_entry.
  - Return no value.
- Set common\_party\_journal from Platform.db.get\_value(“Journal Entry”, filters = mapping(“name” → journal\_entry, “is\_system\_generated” → true, “docstatus” → 1)).
- If not common\_party\_journal.
  - Return no value.
- Set common\_party\_je from Platform.get\_doc(“Journal Entry”, common\_party\_journal).
- Evaluate common\_party\_je.cancel().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “enable\_common\_party\_accounting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0301.json#L6257) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L184)

<a id="op-3bc904566623c0"></a>
### Update accounting ledgers after reference removal

`operation_enterprise_accounts_utils_business_behavior_update_accounting_ledgers_after_reference_removal`

**Inputs** ref\_type = no value, ref\_no = no value, payment\_name = no value.

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Set gle\_update\_query from nested operand in the contract(nested operand in the contract, nested operand in the contract).set(gle.modified, now()).set(gle.modified\_by, Platform.session.user).where((gle.against\_voucher\_type equals re ….
- If payment\_name.
  - Set gle\_update\_query from gle\_update\_query.where(gle.voucher\_no equals payment\_name).
- Evaluate gle\_update\_query.run().
- Set ple from qb.DocType(“Payment Ledger Entry”).
- Set ple\_update\_query from nested operand in the contract(nested operand in the contract, nested operand in the contract).set(ple.modified, now()).set(ple.modified\_by, Platform.session.user).where(((ple.against\_voucher\_type equals r ….
- If payment\_name.
  - Set ple\_update\_query from ple\_update\_query.where(ple.voucher\_no equals payment\_name).
- Evaluate ple\_update\_query.run().
- Set adv from qb.DocType(“Advance Payment Ledger Entry”).
- Set adv\_ple from nested operand in the contract(nested operand in the contract, nested operand in the contract).set(adv.modified\_by, nested operand in the contract.session.user).where(adv.delinked equals 0).where(((adv.aga ….
- If payment\_name.
  - Set adv\_ple from adv\_ple.where(adv.voucher\_no equals payment\_name).
- Evaluate adv\_ple.run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L249)

<a id="op-7d163fbf56752d"></a>
### Remove ref from advance section

`operation_enterprise_accounts_utils_business_behavior_remove_reference_from_advance_section`

**Inputs** ref\_doc = no value, payment\_name = no value.

**State and service calls** request delete on child\_table.

**Explicit results** no value.

**Local steps**

- If ref\_doc.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
  - Set row\_names from list().
  - For each adv in (ref\_doc.get(“advances”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“advances”) → list().
    - If adv.get(“reference\_name”, no value) equals payment\_name.
      - Evaluate row\_names.append(adv.name).
  - If not row\_names.
    - Return no value.
  - Set child\_table from “Sales Invoice Advance” when ref\_doc.doctype equals “Sales Invoice”, otherwise “Purchase Invoice Advance”.
    - Value choice on ref\_doc.doctype equals “Sales Invoice” — true gives “Sales Invoice Advance”, false gives “Purchase Invoice Advance”.
  - Evaluate Platform.db.delete(child\_table, mapping(“name” → tuple(“in”, row\_names))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L1088) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L241)

<a id="op-a44fb06ff5b2a3"></a>
### Unlink ref doc from payment entries

`operation_enterprise_accounts_utils_business_behavior_unlink_reference_record_from_payment_entries`

**Inputs** ref\_doc = no value, payment\_name = no value.

**Local steps**

- Evaluate remove\_ref\_doc\_link\_from\_jv(ref\_doc.doctype, ref\_doc.name, payment\_name).
- Evaluate remove\_ref\_doc\_link\_from\_pe(ref\_doc.doctype, ref\_doc.name, payment\_name).
- Evaluate update\_accounting\_ledgers\_after\_reference\_removal(ref\_doc.doctype, ref\_doc.name, payment\_name).
- Evaluate remove\_ref\_from\_advance\_section(ref\_doc, payment\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L1461) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L248)

<a id="op-57899eb40d9fb8"></a>
### Remove ref doc link from jv

`operation_enterprise_accounts_utils_business_behavior_remove_reference_record_link_from_journal_voucher`

**Inputs** ref\_type = no value, ref\_no = no value, payment\_name = no value.

**State and service calls** msgprint with translated “Journal Entries {0} are un-linked”.format(whitespace '\\n'.join(linked\_jv)).

**Local steps**

- Set jea from qb.DocType(“Journal Entry Account”).
- Set linked\_jv from nested operand in the contract(nested operand in the contract).select(jea.parent).where(((nested operand in the contract.reference\_type equals ref\_type bitwise and nested operand in the contract.reference\_ ….
- Set linked\_jv from convert\_to\_list(linked\_jv).
- Set linked\_jv from list of x for x drawn from linked\_jv where x equals payment\_name when payment\_name, otherwise linked\_jv.
  - Value choice on payment\_name — true gives list of x for x drawn from linked\_jv where x equals payment\_name, false gives linked\_jv.
  - Draw x from linked\_jv, keep a combination only if (x equals payment\_name).
- If linked\_jv.
  - Set update\_query from nested operand in the contract(nested operand in the contract, nested operand in the contract).set(jea.modified, now()).set(jea.modified\_by, Platform.session.user).where((jea.reference\_type equals ref\_type ….
  - If payment\_name.
    - Set update\_query from update\_query.where(jea.parent equals payment\_name).
  - Evaluate update\_query.run().
  - Evaluate Platform.msgprint(translated “Journal Entries {0} are un-linked”.format(whitespace '\\n'.join(linked\_jv))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L1665) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L242)

<a id="op-d8560be74f4b75"></a>
### Convert to list

`operation_enterprise_accounts_utils_business_behavior_convert_to_list`

**Inputs** result.

**Explicit results** list of x at 0 for x drawn from result.

**Local steps**

- Return list of x at 0 for x drawn from result.
  - Draw x from result.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L2427) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L189)

<a id="op-a654ccfd5ff681"></a>
### Remove ref doc link from pe

`operation_enterprise_accounts_utils_business_behavior_remove_reference_record_link_from_pe`

**Inputs** ref\_type = no value, ref\_no = no value, payment\_name = no value.

**Record and data access** read row.advance\_voucher\_type via get\_value · read “Payment Entry” via get\_value · resolve a document from mapping(“doctype” → “Payment Entry Reference”, “parent” → row.parent, “parenttype” → “Payment Entry”, “parentfield” → “references”, …) via get\_doc · resolve a document from “Payment Entry” via get\_doc.

**State and service calls** call db\_insert on advance\_reference · msgprint with translated “Payment Entries {0} are un-linked”.format(whitespace '\\n'.join(linked\_pe)).

**Explicit results** no value.

**Explicit failure paths** validation helper with PaymentEntryUnlinkError — msg.

**Local steps**

- Set per from qb.DocType(“Payment Entry Reference”).
- Set pay from qb.DocType(“Payment Entry”).
- Set query from qb.from\_(per).select(“\*”).where((((per.reference\_doctype equals ref\_type bitwise and per.reference\_name equals ref\_no) bitwise and per.docstatus.lt(2)) bitwise and per.parenttype equals “Payment Entry”)).
- If payment\_name.
  - Set query from query.where(per.parent equals payment\_name).
- Set reference\_rows from query.run(as\_dict = true).
- If not reference\_rows.
  - Return no value.
- Set transferred\_rows from set().
- For each row in reference\_rows.
  - If not (row.payment\_request and row.advance\_voucher\_type and row.advance\_voucher\_no and row.allocated\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.payment\_request → row.advance\_voucher\_type → row.advance\_voucher\_no → row.allocated\_amount.
    - Continue with the next iteration or loop test.
  - Set advance\_row from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.reference\_name equals nested operand in the contract.advance\_voucher\_no).where(per.docstatus equals 1).ru ….
  - Set advance\_row from next(generator of r for r drawn from advance\_row where r.payment\_request equals row.payment\_request, no value).
    - Draw r from advance\_row, keep a combination only if (r.payment\_request equals row.payment\_request).
  - If advance\_row.
    - Evaluate nested operand in the contract(nested operand in the contract).set(per.allocated\_amount, (nested operand in the contract.allocated\_amount + nested operand in the contract.allocated\_amount)).where(per.name  ….run().
  - Otherwise.
    - Set order\_totals from Platform.db.get\_value(row.advance\_voucher\_type, row.advance\_voucher\_no, list(“company”, “grand\_total”, “rounded\_total”, “base\_grand\_total”, …), as\_dict = true).
    - Set payment\_currencies from Platform.db.get\_value(“Payment Entry”, row.parent, list(“payment\_type”, “paid\_from\_account\_currency”, “paid\_to\_account\_currency”), as\_dict = true).
    - Set party\_account\_currency from payment\_currencies.paid\_from\_account\_currency when payment\_currencies.payment\_type equals “Receive”, otherwise payment\_currencies.paid\_to\_account\_currency.
      - Value choice on payment\_currencies.payment\_type equals “Receive” — true gives payment\_currencies.paid\_from\_account\_currency, false gives payment\_currencies.paid\_to\_account\_currency.
    - Set company\_currency from Enterprise.get\_company\_currency(order\_totals.company).
    - If party\_account\_currency equals company\_currency.
      - Set total\_amount from (order\_totals.base\_rounded\_total or order\_totals.base\_grand\_total).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in order\_totals.base\_rounded\_total → order\_totals.base\_grand\_total.
    - Otherwise.
      - Set total\_amount from (order\_totals.rounded\_total or order\_totals.grand\_total).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in order\_totals.rounded\_total → order\_totals.grand\_total.
    - Set advance\_reference from Platform.get\_doc(mapping(“doctype” → “Payment Entry Reference”, “parent” → row.parent, “parenttype” → “Payment Entry”, “parentfield” → “references”, …)).
    - Evaluate advance\_reference.db\_insert().
  - Evaluate transferred\_rows.add(row.name).
- Set linked\_pe from set().
- Set reference\_amounts from mapping().
- Set advance\_vouchers from set().
- For each row in reference\_rows.
  - Evaluate linked\_pe.add(row.parent).
  - Set reference\_amounts at row.name from row.allocated\_amount.
  - If (row.advance\_voucher\_type and row.advance\_voucher\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.advance\_voucher\_type → row.advance\_voucher\_no.
    - Evaluate advance\_vouchers.add(tuple(row.advance\_voucher\_type, row.advance\_voucher\_no)).
- Bind dependencies update\_payment\_requests\_as\_per\_pe\_references.
- Evaluate update\_payment\_requests\_as\_per\_pe\_references(list of row for row drawn from reference\_rows where row.name does not belong to transferred\_rows, cancel = true).
  - Draw row from reference\_rows, keep a combination only if (row.name does not belong to transferred\_rows).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.isin(nested operand in the contract(nested operand in the contract))).whe ….run().
- For each pe in linked\_pe.
  - Attempt the following.
    - Set pe\_doc from Platform.get\_doc(“Payment Entry”, pe).
    - Evaluate pe\_doc.set\_amounts().
    - For each reference in pe\_doc.references.
      - If reference.name belongs to reference\_amounts.
        - Set reference.allocated\_amount from reference\_amounts at reference.name.
        - Evaluate pe\_doc.make\_advance\_gl\_entries(reference, cancel = 1).
        - Set reference.allocated\_amount from 0.
    - Evaluate pe\_doc.clear\_unallocated\_reference\_document\_rows().
    - Evaluate pe\_doc.validate\_payment\_type\_with\_outstanding().
  - On failure (Exception).
    - Set msg from translated “There were issues unlinking payment entry {0}.”.format(pe\_doc.name).
    - Update msg using + text in the contract.
    - Update msg using + translated “Please cancel payment entry manually first”.
    - Call the validation error handler Platform.throw(msg, exc = PaymentEntryUnlinkError, title = translated “Payment Unlink Error”).
  - If (pe\_doc.docstatus equals 1 and not pe\_doc.book\_advance\_payments\_in\_separate\_party\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pe\_doc.docstatus equals 1 → not pe\_doc.book\_advance\_payments\_in\_separate\_party\_account.
    - Evaluate repost\_advance\_payment\_ledger(pe\_doc).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(pay.modified\_by, nested operand in the contract.session.user).where(pay.name equals pe).run().
- For each tuple(voucher\_type, voucher\_no) in advance\_vouchers.
  - Evaluate update\_voucher\_outstanding(voucher\_type, voucher\_no, no value, no value, …).
- Evaluate Platform.msgprint(translated “Payment Entries {0} are un-linked”.format(whitespace '\\n'.join(linked\_pe))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L243)

<a id="op-40e1d9368047ab"></a>
### Repost advance payment ledger

`operation_enterprise_binding_enterprise_accounts_utils_repost_advance_payment_ledger`

**Inputs** doc.

**Record and data access** resolve a document from entry via get\_doc.

**State and service calls** call submit on adv.

**Local steps**

- Evaluate \_delete\_adv\_pl\_entries(doc.doctype, doc.name).
- For each entry in get\_payment\_ledger\_entries(doc.build\_gl\_map()).
  - If entry.doctype equals “Advance Payment Ledger Entry”.
    - Set adv from Platform.get\_doc(entry).
    - Set adv.flags.ignore\_permissions from 1.
    - Evaluate adv.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L220) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1285)

<a id="op-d4f414e608e664"></a>
### Get company default

`operation_enterprise_accounts_utils_business_behavior_get_company_default`

**Inputs** company, fieldname, ignore\_validation = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** value.

**Local steps**

- Set value from Platform.get\_cached\_value(“Company”, company, fieldname).
- If (not ignore\_validation and not value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ignore\_validation → not value.
  - Evaluate throw(translated “Please set default {0} in Company {1}”.format(translated nested operand in the contract.get\_meta(“Company”).get\_label(fieldname), company)).
- Return value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L211)

<a id="op-42b61ba319cc96"></a>
### Fix total debit credit

`operation_enterprise_accounts_utils_business_behavior_fix_total_debit_credit`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, GL Entry).

**State and service calls** execute a supplied database query.

**Local steps**

- Set vouchers from Platform.db.sql(query text (SELECT, GL Entry), as\_dict = 1).
- For each d in vouchers.
  - If abs(d.diff) &gt; 0.
    - Set dr\_or\_cr from ((d.voucher\_type equals “Sales Invoice” and “credit”) or “debit”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (d.voucher\_type equals “Sales Invoice” and “credit”) → “debit”.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.voucher\_type equals “Sales Invoice” → “credit”.
    - Evaluate Platform.db.sql(“update ′tabGL Entry′ set {} = {} + {}\\n\\t\\t\\t\\twhere voucher\_type = {} and voucher\_no = {} and {} &gt; 0 limit 1”.format(dr\_or\_cr, dr\_or\_cr, “%s”, “%s”, …), tuple(d.diff, d.voucher\_type, d.voucher\_no)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L200)

<a id="op-6efd6e767666db"></a>
### Get currency precision

`operation_enterprise_accounts_utils_business_behavior_get_currency_precision`

**Inputs** no declared parameters.

**Explicit results** cint(currency\_precision) · get\_number\_format\_info(number\_format) at 2.

**Local steps**

- Set currency\_precision from Platform.db.get\_default(“currency\_precision”).
- If currency\_precision does not belong to tuple(no value, empty text).
  - Return cint(currency\_precision).
- Set number\_format from (Platform.db.get\_default(“number\_format”) or “#,###.##”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(“number\_format”) → “#,###.##”.
- Return get\_number\_format\_info(number\_format) at 2.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L4854) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L213)

<a id="op-1492c0dae0a950"></a>
### Get fraction units

`operation_enterprise_accounts_utils_business_behavior_get_fraction_units`

**Inputs** currency.

**Declared result** int.

**Record and data access** read “Currency” via get\_value.

**Explicit results** fraction\_units.

**Local steps**

- Set fraction\_units from Platform.db.get\_value(“Currency”, currency, “fraction\_units”).
- If fraction\_units is identical to no value.
  - Set fraction\_units from 100.
- Return fraction\_units.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L5042) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L218)

<a id="op-3dc8064e0ee62c"></a>
### Get zero cutoff

`operation_enterprise_accounts_utils_business_behavior_get_zero_cutoff`

**Inputs** currency.

**Wrappers, in declaration order** site\_cache().

**Declared result** float.

**Explicit results** (0.5 ÷ (fraction\_units or 1)).

**Local steps**

- Set fraction\_units from get\_fraction\_units(currency).
- Return (0.5 ÷ (fraction\_units or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fraction\_units → 1.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L5172) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L232)

<a id="op-41d6d57108982e"></a>
### Get held invoices

`operation_enterprise_accounts_utils_business_behavior_get_held_invoices`

**Inputs** party\_type, party.

**Record and data access** execute query text (SELECT, Purchase Invoice).

**Explicit results** held\_invoices.

**Local steps**

- Set held\_invoices from no value.
- If party\_type equals “Supplier”.
  - Set held\_invoices from Platform.db.sql(query text (SELECT, Purchase Invoice), as\_dict = 1).
  - Set held\_invoices from set(generator of d at “name” for d drawn from held\_invoices).
    - Draw d from held\_invoices.
- Return held\_invoices.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L220)

<a id="op-6936dc8d63b1bc"></a>
### Get outstanding invoices

`operation_enterprise_accounts_utils_business_behavior_get_outstanding_invoices`

**Inputs** party\_type, party, account, common\_filter = no value, posting\_date = no value, min\_outstanding = no value, max\_outstanding = no value, accounting\_dimensions = no value, vouchers = no value, limit = no value, voucher\_no = no value.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** outstanding\_invoices.

**Local steps**

- Set ple from qb.DocType(“Payment Ledger Entry”).
- Set outstanding\_invoices from list().
- Set precision from (Platform.get\_precision(“Sales Invoice”, “outstanding\_amount”) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_precision(“Sales Invoice”, “outstanding\_amount”) → 2.
- If account.
  - Set tuple(root\_type, account\_type) from Platform.get\_cached\_value(“Account”, account at 0, list(“root\_type”, “account\_type”)).
  - Set party\_account\_type from “Receivable” when root\_type equals “Asset”, otherwise “Payable”.
    - Value choice on root\_type equals “Asset” — true gives “Receivable”, false gives “Payable”.
  - Set party\_account\_type from (account\_type or party\_account\_type).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_type → party\_account\_type.
- Otherwise.
  - Set party\_account\_type from Enterprise.get\_party\_account\_type(party\_type).
- Set held\_invoices from get\_held\_invoices(party\_type, party).
- Set common\_filter from (common\_filter or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in common\_filter → list().
- Evaluate common\_filter.append(ple.account\_type equals party\_account\_type).
- Evaluate common\_filter.append(ple.account.isin(account)).
- Evaluate common\_filter.append(ple.party\_type equals party\_type).
- Evaluate common\_filter.append(ple.party equals party).
- Set ple\_query from QueryPaymentLedger().
- Set invoice\_list from ple\_query.get\_voucher\_outstandings(vouchers = vouchers, common\_filter = common\_filter, posting\_date = posting\_date, min\_outstanding = min\_outstanding, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in accounting\_dimensions → list().
- For each d in invoice\_list.
  - Set payment\_amount from (d.invoice\_amount\_in\_account\_currency − d.outstanding\_in\_account\_currency).
  - Set outstanding\_amount from d.outstanding\_in\_account\_currency.
  - If outstanding\_amount &gt; (0.5 ÷ (10 to the power precision)).
    - If (min\_outstanding and max\_outstanding and (outstanding\_amount &lt; min\_outstanding or outstanding\_amount &gt; max\_outstanding)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in min\_outstanding → max\_outstanding → (outstanding\_amount &lt; min\_outstanding or outstanding\_amount &gt; max\_outstanding).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in outstanding\_amount &lt; min\_outstanding → outstanding\_amount &gt; max\_outstanding.
      - Continue with the next iteration or loop test.
    - If (d.voucher\_type differs from “Purchase Invoice” or d.voucher\_no does not belong to held\_invoices).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.voucher\_type differs from “Purchase Invoice” → d.voucher\_no does not belong to held\_invoices.
      - Evaluate outstanding\_invoices.append(Platform.\_dict(mapping(“voucher\_no” → d.voucher\_no, “voucher\_type” → d.voucher\_type, “posting\_date” → d.posting\_date, “invoice\_amount” → flt(d.invoice\_amount\_in\_account\_currency), …))).
- Set outstanding\_invoices from sorted(outstanding\_invoices, key = deferred anonymous expression).
- Return outstanding\_invoices.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account at 0, list(“root\_type”, “account\_type”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L5495) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L224)

<a id="op-7b808af29c2a12"></a>
### Get account name

`operation_enterprise_accounts_utils_business_behavior_get_account_name`

**Inputs** account\_type = no value, root\_type = no value, is\_group = no value, account\_currency = no value, company = no value.

**Record and data access** read “Account” via get\_value.

**Explicit results** Platform.db.get\_value(“Account”, mapping(“account\_type” → (account\_type or empty text), “root\_type” → (root\_type or empty text), “is\_group” → (is\_group or 0), “account\_currency” → (account\_currency or nest ….

**Local steps**

- Return Platform.db.get\_value(“Account”, mapping(“account\_type” → (account\_type or empty text), “root\_type” → (root\_type or empty text), “is\_group” → (is\_group or 0), “account\_currency” → (account\_currency or nest ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_type → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in root\_type → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_group → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_currency → Platform.defaults.get\_defaults().currency.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company → Platform.defaults.get\_defaults().company.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0302.json#L6786) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L203)
