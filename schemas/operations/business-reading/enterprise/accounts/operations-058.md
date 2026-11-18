# Accounting and settlement · operations 58

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Journal entry

[Record definition](../../../../data/record-types/journal_entry.json)

<a id="op-9cc76cd663c713"></a>
### Get payment entry against invoice

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_get_payment_entry_against_invoice`

**Inputs** dt, dn, amount = no value, debit\_in\_account\_currency = no value, journal\_entry = false, bank\_account = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from dt via get\_doc.

**Explicit results** get\_payment\_entry(ref\_doc, mapping(“party\_type” → party\_type, “party\_account” → party\_account, “party\_account\_currency” → ref\_doc.party\_account\_currency, “amount\_field\_party” → amount\_field\_party, …)).

**Local steps**

- Set ref\_doc from Platform.get\_doc(dt, dn).
- Evaluate ref\_doc.check\_permission().
- If dt equals “Sales Invoice”.
  - Set party\_type from “Customer”.
  - Set party\_account from (get\_party\_account\_based\_on\_invoice\_discounting(dn) or ref\_doc.debit\_to).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_party\_account\_based\_on\_invoice\_discounting(dn) → ref\_doc.debit\_to.
- Otherwise.
  - Set party\_type from “Supplier”.
  - Set party\_account from ref\_doc.credit\_to.
- If ((dt equals “Sales Invoice” and ref\_doc.outstanding\_amount &gt; 0) or (dt equals “Purchase Invoice” and ref\_doc.outstanding\_amount &lt; 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (dt equals “Sales Invoice” and ref\_doc.outstanding\_amount &gt; 0) → (dt equals “Purchase Invoice” and ref\_doc.outstanding\_amount &lt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “Sales Invoice” → ref\_doc.outstanding\_amount &gt; 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “Purchase Invoice” → ref\_doc.outstanding\_amount &lt; 0.
  - Set amount\_field\_party from “credit\_in\_account\_currency”.
  - Set amount\_field\_bank from “debit\_in\_account\_currency”.
- Otherwise.
  - Set amount\_field\_party from “debit\_in\_account\_currency”.
  - Set amount\_field\_bank from “credit\_in\_account\_currency”.
- Return get\_payment\_entry(ref\_doc, mapping(“party\_type” → party\_type, “party\_account” → party\_account, “party\_account\_currency” → ref\_doc.party\_account\_currency, “amount\_field\_party” → amount\_field\_party, …)).
  - Value choice on amount — true gives amount, false gives abs(ref\_doc.outstanding\_amount).

**Values supplied outside this operation** effective access from ref\_doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L160) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L798)

<a id="op-a27cc9d6c3e995"></a>
### Get payment entry

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_get_payment_entry`

**Inputs** ref\_doc, args.

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_cached\_value.

**State and service calls** request new\_doc for “Journal Entry”.

**Explicit results** je when args.get(“journal\_entry”), otherwise je.as\_dict().

**Local steps**

- Evaluate Platform.has\_permission(“Journal Entry”, ptype = “create”, throw = true).
- Set cost\_center from (ref\_doc.get(“cost\_center”) or Platform.get\_cached\_value(“Company”, ref\_doc.company, “cost\_center”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“cost\_center”) → Platform.get\_cached\_value(“Company”, ref\_doc.company, “cost\_center”).
- Set exchange\_rate from 1.
- If args.get(“party\_account”).
  - Set exchange\_rate from get\_exchange\_rate((ref\_doc.get(“posting\_date”) or ref\_doc.get(“transaction\_date”)), args.get(“party\_account”), args.get(“party\_account\_currency”), ref\_doc.company, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“posting\_date”) → ref\_doc.get(“transaction\_date”).
- Set je from Platform.new\_doc(“Journal Entry”).
- Evaluate je.update(mapping(“voucher\_type” → “Bank Entry”, “company” → ref\_doc.company, “remark” → args.get(“remarks”))).
- Set party\_row from je.append(“accounts”, mapping(“account” → args.get(“party\_account”), “party\_type” → args.get(“party\_type”), “party” → ref\_doc.get(nested operand in the contract.get(“party\_type”).lower()), “cost\_center” →  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“party\_account\_currency”) → get\_account\_currency(args.get(“party\_account”)).
- Set bank\_row from je.append(“accounts”).
- Set bank\_account from get\_default\_bank\_cash\_account(ref\_doc.company, “Bank”, account = args.get(“bank\_account”)).
- If bank\_account.
  - Evaluate bank\_row.update(bank\_account).
  - Set bank\_row.exchange\_rate from get\_exchange\_rate((ref\_doc.get(“posting\_date”) or ref\_doc.get(“transaction\_date”)), bank\_account at “account”, bank\_account at “account\_currency”, ref\_doc.company).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“posting\_date”) → ref\_doc.get(“transaction\_date”).
- Set bank\_row.cost\_center from cost\_center.
- Set amount from (args.get(“debit\_in\_account\_currency”) or args.get(“amount”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“debit\_in\_account\_currency”) → args.get(“amount”).
- If bank\_row.account\_currency equals args.get(“party\_account\_currency”).
  - Evaluate bank\_row.set(args.get(“amount\_field\_bank”), amount).
- Otherwise.
  - Evaluate bank\_row.set(args.get(“amount\_field\_bank”), (amount × exchange\_rate)).
- If (party\_row.account\_currency differs from ref\_doc.company\_currency or (bank\_row.account\_currency and bank\_row.account\_currency differs from ref\_doc.company\_currency)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_row.account\_currency differs from ref\_doc.company\_currency → (bank\_row.account\_currency and bank\_row.account\_currency differs from ref\_doc.company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bank\_row.account\_currency → bank\_row.account\_currency differs from ref\_doc.company\_currency.
  - Set je.multi\_currency from 1.
- Evaluate je.set\_amounts\_in\_company\_currency().
- Evaluate je.set\_total\_debit\_credit().
- Return je when args.get(“journal\_entry”), otherwise je.as\_dict().
  - Value choice on args.get(“journal\_entry”) — true gives je, false gives je.as\_dict().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Journal Entry”, ptype = “create”, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, ref\_doc.company, “cost\_center”), Platform.get\_cached\_value(“Account”, args.get(“party\_account”), “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L159) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L797)

<a id="op-3c5ee6fbdf3864"></a>
### Get against jv

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_get_against_journal_voucher`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Journal Entry” via get\_list.

**Explicit results** list() · Platform.get\_list(“Journal Entry”, filters = je\_filters, fields = list(“name”, “posting\_date”, “remark”), order\_by = “name desc”, limit\_start = start, …).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid filter”.

**Local steps**

- If not Platform.db.has\_column(“Journal Entry”, searchfield).
  - Return list().
- Set account from filters.get(“account”).
- Set party from filters.get(“party”).
- For each value in tuple(account, party).
  - If (value and not isinstance(value, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → not isinstance(value, str).
    - Call the validation error handler Platform.throw(translated “Invalid filter”, Platform.PermissionError).
- Set je\_filters from list(list(“docstatus”, “=”, 1), list(searchfield, “like”, formatted text %{txt}%), list(“Journal Entry Account”, “account”, “=”, account), list(“Journal Entry Account”, “reference\_type”, “is”, “not set”)).
- Evaluate je\_filters.append(list(“Journal Entry Account”, “party”, “=”, party) when party, otherwise list(“Journal Entry Account”, “party”, “is”, “not set”)).
  - Value choice on party — true gives list(“Journal Entry Account”, “party”, “=”, party), false gives list(“Journal Entry Account”, “party”, “is”, “not set”).
- Return Platform.get\_list(“Journal Entry”, filters = je\_filters, fields = list(“name”, “posting\_date”, “remark”), order\_by = “name desc”, limit\_start = start, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1107)

<a id="op-88f9ebeef9dfb4"></a>
### Get outstanding

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_get_outstanding`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read args at “doctype” via get\_value.

**State and service calls** msgprint with translated “No Permission” · execute a supplied database query.

**Explicit results** mapping(amount\_field → abs(against\_jv\_amount)) · mapping(amount\_field → abs(flt(invoice.outstanding\_amount)), “exchange\_rate” → exchange\_rate, “party\_type” → party\_type, “party” → invoice.get(scrub(party\_type)), …).

**Local steps**

- If not Platform.has\_permission(“Account”).
  - Evaluate Platform.msgprint(translated “No Permission”, raise\_exception = 1).
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set company\_currency from Enterprise.get\_company\_currency(args.get(“company”)).
- Set due\_date from no value.
- If args.get(“doctype”) equals “Journal Entry”.
  - Set condition from “ and party=%(party)s” when args.get(“party”), otherwise empty text.
    - Value choice on args.get(“party”) — true gives “ and party=%(party)s”, false gives empty text.
  - Set against\_jv\_amount from Platform.db.sql(formatted text   select sum(debit\_in\_account\_currency) - sum(credit\_in\_account\_currency)  from ′tabJournal Entry Account′ where parent=%(docname)s and account=%(, args).
  - Set against\_jv\_amount from flt(against\_jv\_amount at 0 at 0) when against\_jv\_amount, otherwise 0.
    - Value choice on against\_jv\_amount — true gives flt(against\_jv\_amount at 0 at 0), false gives 0.
  - Set amount\_field from “credit\_in\_account\_currency” when against\_jv\_amount &gt; 0, otherwise “debit\_in\_account\_currency”.
    - Value choice on against\_jv\_amount &gt; 0 — true gives “credit\_in\_account\_currency”, false gives “debit\_in\_account\_currency”.
  - Return mapping(amount\_field → abs(against\_jv\_amount)).
- Otherwise.
  - If args.get(“doctype”) belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
    - Set party\_type from “Customer” when args.get(“doctype”) equals “Sales Invoice”, otherwise “Supplier”.
      - Value choice on args.get(“doctype”) equals “Sales Invoice” — true gives “Customer”, false gives “Supplier”.
    - Set invoice from Platform.db.get\_value(args at “doctype”, args at “docname”, list(“outstanding\_amount”, “conversion\_rate”, scrub(party\_type), “due\_date”), as\_dict = 1).
    - Set due\_date from invoice.get(“due\_date”).
    - Set exchange\_rate from invoice.conversion\_rate when args.get(“account\_currency”) differs from company\_currency, otherwise 1.
      - Value choice on args.get(“account\_currency”) differs from company\_currency — true gives invoice.conversion\_rate, false gives 1.
    - If args at “doctype” equals “Sales Invoice”.
      - Set amount\_field from “credit\_in\_account\_currency” when flt(invoice.outstanding\_amount) &gt; 0, otherwise “debit\_in\_account\_currency”.
        - Value choice on flt(invoice.outstanding\_amount) &gt; 0 — true gives “credit\_in\_account\_currency”, false gives “debit\_in\_account\_currency”.
    - Otherwise.
      - Set amount\_field from “debit\_in\_account\_currency” when flt(invoice.outstanding\_amount) &gt; 0, otherwise “credit\_in\_account\_currency”.
        - Value choice on flt(invoice.outstanding\_amount) &gt; 0 — true gives “debit\_in\_account\_currency”, false gives “credit\_in\_account\_currency”.
    - Return mapping(amount\_field → abs(flt(invoice.outstanding\_amount)), “exchange\_rate” → exchange\_rate, “party\_type” → party\_type, “party” → invoice.get(scrub(party\_type)), …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1172) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1110)

<a id="op-811b51d5dae357"></a>
### Get party account and currency

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_get_party_account_and_currency`

**Inputs** company, party\_type, party.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_cached\_value.

**State and service calls** msgprint with translated “No Permission”.

**Explicit results** mapping(“account” → account, “account\_currency” → Platform.get\_cached\_value(“Account”, account, “account\_currency”)).

**Local steps**

- If not Platform.has\_permission(“Account”).
  - Evaluate Platform.msgprint(translated “No Permission”, raise\_exception = 1).
- Set account from get\_party\_account(party\_type, party, company).
- Return mapping(“account” → account, “account\_currency” → Platform.get\_cached\_value(“Account”, account, “account\_currency”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”) · configured or stored value from Platform.get\_cached\_value(“Account”, account, “account\_currency”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1111)

<a id="op-509be4f231258c"></a>
### Get account details and party type

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_get_account_details_and_party_type`

**Inputs** account, date, company, debit = no value, credit = no value, exchange\_rate = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_cached\_value · read “Bank Account” via get\_value.

**State and service calls** msgprint with translated “No Permission”.

**Explicit results** no value · grid\_values.

**Local steps**

- If not Platform.has\_permission(“Account”).
  - Evaluate Platform.msgprint(translated “No Permission”, raise\_exception = 1).
- Set company\_currency from Enterprise.get\_company\_currency(company).
- Set account\_details from Platform.get\_cached\_value(“Account”, account, list(“account\_type”, “account\_currency”), as\_dict = 1).
- If not account\_details.
  - Return no value.
- If account\_details.account\_type equals “Receivable”.
  - Set party\_type from “Customer”.
- Otherwise.
  - If account\_details.account\_type equals “Payable”.
    - Set party\_type from “Supplier”.
  - Otherwise.
    - Set party\_type from empty text.
- Set grid\_values from mapping(“party\_type” → party\_type, “account\_type” → account\_details.account\_type, “account\_currency” → (account\_details.account\_currency or company\_currency), “bank\_account” → (Platform.db.get\_value(“Bank  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_details.account\_currency → company\_currency.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Bank Account”, mapping(“account” → account, “company” → company)) → no value.
- If not party\_type.
  - Set grid\_values at “party” from empty text.
- Return grid\_values.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”) · configured or stored value from Platform.get\_cached\_value(“Account”, account, list(“account\_type”, “account\_currency”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1166) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1106)

<a id="op-c564a619800c50"></a>
### Get exchange rate

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_get_exchange_rate`

**Inputs** posting\_date, account = no value, account\_currency = no value, company = no value, reference\_type = no value, reference\_name = no value, debit = no value, credit = no value, exchange\_rate = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_cached\_value · read reference\_type via get\_value.

**Explicit results** (exchange\_rate or 1).

**Explicit failure paths** validation helper — translated “Please select correct account”.

**Local steps**

- If isinstance(exchange\_rate, str).
  - Set exchange\_rate from (flt(exchange\_rate) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(exchange\_rate) → 1.
- Set account\_details from Platform.get\_cached\_value(“Account”, account, list(“account\_type”, “root\_type”, “account\_currency”, “company”), as\_dict = 1).
- If not account\_details.
  - Call the validation error handler Platform.throw(translated “Please select correct account”).
- If not company.
  - Set company from account\_details.company.
- If not account\_currency.
  - Set account\_currency from account\_details.account\_currency.
- Set company\_currency from Enterprise.get\_company\_currency(company).
- If account\_currency differs from company\_currency.
  - If (reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and reference\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”) → reference\_name.
    - Set exchange\_rate from Platform.db.get\_value(reference\_type, reference\_name, “conversion\_rate”).
  - Otherwise.
    - If ((not flt(exchange\_rate) or flt(exchange\_rate) equals 1) and account\_currency and posting\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not flt(exchange\_rate) or flt(exchange\_rate) equals 1) → account\_currency → posting\_date.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not flt(exchange\_rate) → flt(exchange\_rate) equals 1.
      - Set exchange\_rate from \_get\_exchange\_rate(account\_currency, company\_currency, posting\_date).
- Otherwise.
  - Set exchange\_rate from 1.
- Return (exchange\_rate or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in exchange\_rate → 1.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, list(“account\_type”, “root\_type”, “account\_currency”, “company”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1109)

<a id="op-2ae15345aab194"></a>
### Get average exchange rate

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_get_average_exchange_rate`

**Inputs** account.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** exchange\_rate.

**Local steps**

- Set exchange\_rate from 0.
- Set bank\_balance\_in\_account\_currency from get\_balance\_on(account).
- If bank\_balance\_in\_account\_currency.
  - Set bank\_balance\_in\_company\_currency from get\_balance\_on(account, in\_account\_currency = false).
  - Set exchange\_rate from (bank\_balance\_in\_company\_currency ÷ bank\_balance\_in\_account\_currency).
- Return exchange\_rate.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L796)

<a id="op-c36659d51e21cf"></a>
### Make inter company journal entry

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_make_inter_company_journal_entry`

**Inputs** name, voucher\_type, company.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Journal Entry”.

**Explicit results** journal\_entry.as\_dict().

**Local steps**

- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Set journal\_entry.voucher\_type from voucher\_type.
- Set journal\_entry.company from company.
- Set journal\_entry.posting\_date from nowdate().
- Set journal\_entry.inter\_company\_journal\_entry\_reference from name.
- Return journal\_entry.as\_dict().

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L816)

<a id="op-e9967df2cdeaf3"></a>
### Make reverse journal entry

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_make_reverse_journal_entry`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** map\_reverse\_journal\_entry(source\_name, target\_doc).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“Journal Entry”, doc = source\_name).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Return map\_reverse\_journal\_entry(source\_name, target\_doc).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Journal Entry”, doc = source\_name).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L817)

<a id="op-342bf9e8456124"></a>
### Map reverse journal entry

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_map_reverse_journal_entry`

**Inputs** source\_name, target\_doc = no value, ignore\_permissions = false.

**Record and data access** read “Journal Entry” via get\_value · read “Journal Entry” via exists.

**Explicit results** doclist.

**Explicit failure paths** validation helper — translated “{0} is already a Reverse Journal Entry of {1}. Cancel it instead of reversing it.”.format(get\_link\_to\_form(“Journal Entry”, source\_name), get\_link\_to\_form(“Journal Entry”, reversal\_of)) · validation helper — translated “A Reverse Journal Entry {0} already exists for this Journal Entry.”.format(get\_link\_to\_form(“Journal Entry”, existing\_reverse)).

**Local steps**

- Set reversal\_of from Platform.db.get\_value(“Journal Entry”, source\_name, “reversal\_of”).
- If reversal\_of.
  - Call the validation error handler Platform.throw(translated “{0} is already a Reverse Journal Entry of {1}. Cancel it instead of reversing it.”.format(get\_link\_to\_form(“Journal Entry”, source\_name), get\_link\_to\_form(“Journal Entry”, reversal\_of))).
- Set existing\_reverse from Platform.db.exists(“Journal Entry”, mapping(“reversal\_of” → source\_name, “docstatus” → 1)).
- If existing\_reverse.
  - Call the validation error handler Platform.throw(translated “A Reverse Journal Entry {0} already exists for this Journal Entry.”.format(get\_link\_to\_form(“Journal Entry”, existing\_reverse))).
- Bind dependencies get\_mapped\_doc.
- Bind local operation post\_process for subsequent calls.
- Set doclist from get\_mapped\_doc(“Journal Entry”, source\_name, mapping(“Journal Entry” → mapping(“doctype” → “Journal Entry”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Journal Entry Account” → mapping(“doctype”  ….
- Return doclist.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L818)

<a id="op-4133aabab75f5e"></a>
### Map reverse journal entry.post process

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_map_reverse_journal_entry_post_process`

**Inputs** source, target.

**Local steps**

- Set target.reversal\_of from source.name.
- Set target.naming\_series from source.naming\_series.
- If source.voucher\_type equals “Bank Entry”.
  - Set target.cheque\_no from source.cheque\_no.
  - Set target.cheque\_date from source.cheque\_date.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L819)

## Record · Journal entry template

[Record definition](../../../../data/record-types/journal_entry_template.json)

<a id="op-3d6fab4ec400e3"></a>
### Journal Entry Template.validate

`operation_enterprise_accounts_record_definitions_journal_entry_template_business_behavior_journal_entry_template_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_party().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate party](operations-058.md#op-8e00b5e4698492).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1157)

<a id="op-8e00b5e4698492"></a>
### Journal Entry Template.validate party

`operation_enterprise_accounts_record_definitions_journal_entry_template_business_behavior_journal_entry_template_validate_party`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Check row {0} for account {1}: Party Type is only allowed for Receivable or Payable accounts”.format(account.idx, account.account) · validation helper — translated “Check row {0} for account {1}: Party is only allowed if Party Type is set”.format(account.idx, account.account).

**Local steps**

- For each account in self.accounts.
  - If account.party\_type.
    - Set account\_type from Platform.get\_cached\_value(“Account”, account.account, “account\_type”).
    - If account\_type does not belong to list(“Receivable”, “Payable”).
      - Call the validation error handler Platform.throw(translated “Check row {0} for account {1}: Party Type is only allowed for Receivable or Payable accounts”.format(account.idx, account.account)).
  - If (account.party and not account.party\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account.party → not account.party\_type.
    - Call the validation error handler Platform.throw(translated “Check row {0} for account {1}: Party is only allowed if Party Type is set”.format(account.idx, account.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account.account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0069.json#L4718) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1158)

<a id="op-52b9af079929b7"></a>
### Get naming series

`operation_enterprise_accounts_record_definitions_journal_entry_template_business_behavior_get_naming_series`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.get\_meta(“Journal Entry”).get\_field(“naming\_series”).options.

**Local steps**

- Return Platform.get\_meta(“Journal Entry”).get\_field(“naming\_series”).options.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0069.json#L5032) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1156)

## Record · Ledger health

[Record definition](../../../../data/record-types/ledger_health.json)

<a id="op-f4f11314f40df3"></a>
### Update ledger health

`operation_enterprise_binding_enterprise_accounts_doctype_ledger_health_ledger_health_update_ledger_health`

**Inputs** check, vouchers, run\_date, scan.

**State and service calls** request delete on “Ledger Health” · request new\_doc for “Ledger Health” · call save on doc.

**Local steps**

- Set tuple(still\_reported, stale) from get\_kept\_and\_stale\_ledger\_health(check, vouchers, scan).
- If stale.
  - Evaluate Platform.db.delete(“Ledger Health”, mapping(“name” → tuple(“in”, stale))).
- If still\_reported.
  - Set ledger\_health from Platform.qb.DocType(“Ledger Health”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(ledger\_health.checked\_on, run\_date).where(ledger\_health.name.isin(list(nested operand in the contract.values()))).run().
- For each tuple(voucher\_type, voucher\_no) in (vouchers − still\_reported.keys()).
  - Set doc from Platform.new\_doc(“Ledger Health”).
  - Evaluate doc.update(mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no, check → 1, “checked\_on” → run\_date)).
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L822)

<a id="op-bcc8322b568c23"></a>
### Get kept and stale ledger health

`operation_enterprise_binding_enterprise_accounts_doctype_ledger_health_ledger_health_get_kept_and_stale_ledger_health`

**Inputs** check, vouchers, scan.

**Record and data access** read “Ledger Health” via get\_all.

**Explicit results** tuple(still\_reported, stale).

**Local steps**

- Set tuple(still\_reported, extra\_records) from tuple(mapping(), mapping()).
- For each row in Platform.get\_all(“Ledger Health”, filters = mapping(check → 1), fields = list(“name”, “voucher\_type”, “voucher\_no”), order\_by = “name”).
  - Set voucher from tuple(row.voucher\_type, row.voucher\_no).
  - If (voucher belongs to vouchers and voucher does not belong to still\_reported).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher belongs to vouchers → voucher does not belong to still\_reported.
    - Set still\_reported at voucher from row.name.
  - Otherwise.
    - Evaluate extra\_records.setdefault(voucher, list()).append(row.name).
- Set rechecked from (vouchers bitwise or get\_vouchers\_in\_scan((extra\_records.keys() − vouchers), scan)).
- Set stale from list of name for voucher drawn from (extra\_records.keys() bitwise and rechecked), then name drawn from extra\_records at voucher.
  - Draw voucher from (extra\_records.keys() bitwise and rechecked).
  - Draw name from extra\_records at voucher.
- Return tuple(still\_reported, stale).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L820)

<a id="op-3236cec00b7276"></a>
### Get vouchers in scan

`operation_enterprise_binding_enterprise_accounts_doctype_ledger_health_ledger_health_get_vouchers_in_scan`

**Inputs** vouchers, scan.

**Explicit results** set() · (set of tuple(row) for row drawn from scanned bitwise and vouchers).

**Local steps**

- If (not vouchers or not scan.companies).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not vouchers → not scan.companies.
  - Return set().
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set scanned from nested operand in the contract(nested operand in the contract, nested operand in the contract).distinct().where(((nested operand in the contract.isin(nested operand in the contract.companies) bitwise and n ….run().
  - Draw tuple(\_voucher\_type, voucher\_no) from vouchers.
- Return (set of tuple(row) for row drawn from scanned bitwise and vouchers).
  - Draw row from scanned.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L821)

## Record · Ledger merge

[Record definition](../../../../data/record-types/ledger_merge.json)

<a id="op-60d234d7d6451b"></a>
### Ledger Merge.start merge

`operation_enterprise_accounts_record_definitions_ledger_merge_business_behavior_ledger_merge_start_merge`

**Inputs** self.

**Explicit results** true · false.

**Explicit failure paths** validation helper — translated “Scheduler is inactive. Cannot merge accounts.”.

**Local steps**

- Bind dependencies enqueue.
- Bind dependencies is\_scheduler\_inactive.
- If (is\_scheduler\_inactive() and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_scheduler\_inactive() → not Platform.in\_test.
  - Call the validation error handler Platform.throw(translated “Scheduler is inactive. Cannot merge accounts.”, title = translated “Scheduler Inactive”).
- Set job\_id from formatted text ledger\_merge::{self.name}.
- If not is\_job\_enqueued(job\_id).
  - Evaluate enqueue(start\_merge, queue = “default”, timeout = 6000, event = “ledger\_merge”, job\_id = job\_id, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.in\_test.
  - Return true.
- Return false.

**Values supplied outside this operation** service or queued work from enqueue(start\_merge, queue = “default”, timeout = 6000, event = “ledger\_merge”, job\_id = job\_id, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0070.json#L463) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1202)

<a id="op-d74dd1f74d51c3"></a>
### Form start merge

`operation_enterprise_accounts_record_definitions_ledger_merge_business_behavior_form_start_merge`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Ledger Merge” via get\_doc.

**Explicit results** lm\_doc.start\_merge().

**Local steps**

- Set lm\_doc from Platform.get\_doc(“Ledger Merge”, docname).
- Evaluate lm\_doc.check\_permission(“write”).
- Return lm\_doc.start\_merge().

**Values supplied outside this operation** effective access from lm\_doc.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1201)

<a id="op-7754c560369231"></a>
### Start merge

`operation_enterprise_accounts_record_definitions_ledger_merge_business_behavior_start_merge`

**Inputs** docname.

**Record and data access** resolve a document from “Ledger Merge” via get\_doc.

**State and service calls** call db\_set on row · commit · publish realtime with “ledger\_merge\_progress” · rollback · call db\_set on ledger\_merge · 1 additional forms in the steps below.

**Local steps**

- Set ledger\_merge from Platform.get\_doc(“Ledger Merge”, docname).
- Set successful\_merges from 0.
- Set total from len(ledger\_merge.merge\_accounts).
- For each row in ledger\_merge.merge\_accounts.
  - If not row.merged.
    - Attempt the following.
      - Evaluate merge\_account(row.account, ledger\_merge.account).
      - Evaluate row.db\_set(“merged”, 1).
      - If not Platform.in\_test.
        - Evaluate Platform.db.commit().
      - Update successful\_merges using + 1.
      - Evaluate Platform.publish\_realtime(“ledger\_merge\_progress”, mapping(“ledger\_merge” → ledger\_merge.name, “current” → successful\_merges, “total” → total)).
    - On failure (Exception).
      - If not Platform.in\_test.
        - Evaluate Platform.db.rollback().
      - Evaluate ledger\_merge.log\_error(“Ledger merge failed”).
    - On exit, including pending return or failure.
      - If successful\_merges equals total.
        - Evaluate ledger\_merge.db\_set(“status”, “Success”).
      - Otherwise.
        - If successful\_merges &gt; 0.
          - Evaluate ledger\_merge.db\_set(“status”, “Partial Success”).
        - Otherwise.
          - Evaluate ledger\_merge.db\_set(“status”, “Error”).
- Evaluate Platform.publish\_realtime(“ledger\_merge\_refresh”, mapping(“ledger\_merge” → ledger\_merge.name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“ledger\_merge\_progress”, mapping(“ledger\_merge” → ledger\_merge.name, “current” → successful\_merges, “total” → total)), Platform.publish\_realtime(“ledger\_merge\_refresh”, mapping(“ledger\_merge” → ledger\_merge.name)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1203)

## Record · Loyalty point entry

[Record definition](../../../../data/record-types/loyalty_point_entry.json)

<a id="op-9bded453f43f9a"></a>
### Get loyalty point entries

`operation_enterprise_accounts_record_definitions_loyalty_point_entry_business_behavior_get_loyalty_point_entries`

**Inputs** customer, loyalty\_program, company, expiry\_date = no value.

**Record and data access** execute query text (SELECT, Loyalty Point Entry).

**Explicit results** Platform.db.sql(query text (SELECT, Loyalty Point Entry), tuple(customer, loyalty\_program, expiry\_date, company), as\_dict = 1).

**Local steps**

- If not expiry\_date.
  - Set expiry\_date from today().
- Return Platform.db.sql(query text (SELECT, Loyalty Point Entry), tuple(customer, loyalty\_program, expiry\_date, company), as\_dict = 1).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1206)

<a id="op-efc1bc308908a1"></a>
### Get redemption details

`operation_enterprise_accounts_record_definitions_loyalty_point_entry_business_behavior_get_redemption_details`

**Inputs** customer, loyalty\_program, company.

**Record and data access** execute query text (SELECT, Loyalty Point Entry).

**Explicit results** Platform.\_dict(Platform.db.sql(query text (SELECT, Loyalty Point Entry), tuple(customer, loyalty\_program, company))).

**Local steps**

- Return Platform.\_dict(Platform.db.sql(query text (SELECT, Loyalty Point Entry), tuple(customer, loyalty\_program, company))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1207)

## Record · Loyalty program

[Record definition](../../../../data/record-types/loyalty_program.json)

<a id="op-bfdb0e9c615e44"></a>
### Loyalty Program.validate

`operation_enterprise_accounts_record_definitions_loyalty_program_business_behavior_loyalty_program_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_lowest\_tier().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate lowest tier](operations-059.md#op-492a573700ad5b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0070.json#L5416) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1217)
