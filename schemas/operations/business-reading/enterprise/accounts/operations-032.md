# Accounting and settlement · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Customer ledger summary

<a id="op-90e09db4014583"></a>
### Party Ledger Summary Report.update hierarchical filters

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_update_hierarchical_filters`

**Inputs** self.

**Local steps**

- For each doctype in TREE\_DOCTYPES.
  - Set key from scrub(doctype).
  - If self.filters.get(key).
    - Set self.filters at key from get\_children(doctype, self.filters at key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0239.json#L6880) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L483) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L832)

<a id="op-6dde74d8fa691f"></a>
### Party Ledger Summary Report.get party details

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_get_party_details`

**Inputs** self.

**Local steps**

- Set self.parties from list().
- Set self.party\_details from Platform.\_dict().
- Set party\_type from self.filters.party\_type.
- Set doctype from qb.DocType(party\_type).
- Set party\_details\_fields from list(doctype.name.as\_(“party”), formatted text {scrub(party\_type)}\_name, formatted text {scrub(party\_type)}\_group).
- If party\_type equals “Customer”.
  - Evaluate party\_details\_fields.append(doctype.territory).
- Set conditions from self.get\_party\_conditions(doctype).
- Set query from qb.from\_(doctype).select(expanded party\_details\_fields).where(Criterion.all(conditions)).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(party\_type).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set party\_details from query.run(as\_dict = true).
- For each row in party\_details.
  - Evaluate self.parties.append(row.party).
  - Set self.party\_details at row.party from row.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party conditions](operations-032.md#op-aafcdf17e6b97a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0240.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L827)

<a id="op-aafcdf17e6b97a"></a>
### Party Ledger Summary Report.get party conditions

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_get_party_conditions`

**Inputs** self, doctype.

**Explicit results** conditions.

**Local steps**

- Set conditions from list().
- Set group\_field from “customer\_group” when self.filters.party\_type equals “Customer”, otherwise “supplier\_group”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “customer\_group”, false gives “supplier\_group”.
- If self.filters.party.
  - Evaluate conditions.append(doctype.name equals self.filters.party).
- If self.filters.territory.
  - Evaluate conditions.append(doctype.territory.isin(self.filters.territory)).
- If self.filters.get(group\_field).
  - Evaluate conditions.append(doctype at group\_field.isin(self.filters.get(group\_field))).
- If self.filters.payment\_terms\_template.
  - Evaluate conditions.append(doctype.payment\_terms equals self.filters.payment\_terms\_template).
- If self.filters.sales\_partner.
  - Evaluate conditions.append(doctype.default\_sales\_partner.isin(self.filters.sales\_partner)).
- If self.filters.sales\_person.
  - Set sales\_team from qb.DocType(“Sales Team”).
  - Set sales\_invoice from qb.DocType(“Sales Invoice”).
  - Set customers from (nested operand in the contract.select(nested operand in the contract.parent).where(nested operand in the contract.sales\_person.isin(nested operand in the contract.filters.sales\_person)).where(sales\_team.p ….
  - Evaluate conditions.append(doctype.name.isin(customers)).
- Return conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0240.json#L615) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L826)

<a id="op-0916f626c4d7e9"></a>
### Party Ledger Summary Report.get columns

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_get_columns`

**Inputs** self.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated self.filters.party\_type, “fieldtype” → “Link”, “fieldname” → “party”, “options” → self.filters.party\_type, …)).
- If self.party\_naming\_by equals “Naming Series”.
  - Evaluate columns.append(mapping(“label” → translated (self.filters.party\_type + “ Name”), “fieldtype” → “Data”, “fieldname” → “party\_name”, “width” → 150)).
- Set credit\_or\_debit\_note from “Credit Note” when self.filters.party\_type equals “Customer”, otherwise “Debit Note”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “Credit Note”, false gives “Debit Note”.
- If self.filters.party\_type equals “Customer”.
  - Update columns using + list(mapping(“label” → translated “Customer Group”, “fieldname” → “customer\_group”, “fieldtype” → “Link”, “options” → “Customer Group”), mapping(“label” → translated “Territory”, “fieldname” → “territory”, ….
- Otherwise.
  - Update columns using + list(mapping(“label” → translated “Supplier Group”, “fieldname” → “supplier\_group”, “fieldtype” → “Link”, “options” → “Supplier Group”)).
- Update columns using + list(mapping(“label” → translated “Opening Balance”, “fieldname” → “opening\_balance”, “fieldtype” → “Currency”, “options” → “currency”, …), mapping(“label” → translated “Invoiced Amount”, “fieldname” → “in ….
- For each account in self.party\_adjustment\_accounts.
  - Evaluate columns.append(mapping(“label” → account, “fieldname” → (“adj\_” + scrub(account)), “fieldtype” → “Currency”, “options” → “currency”, …)).
- Update columns using + list(mapping(“label” → translated “Closing Balance”, “fieldname” → “closing\_balance”, “fieldtype” → “Currency”, “options” → “currency”, …), mapping(“label” → translated “Currency”, “fieldname” → “currency” ….
- Evaluate columns.append(mapping(“label” → translated “Dr/Cr”, “fieldname” → “dr\_or\_cr”, “fieldtype” → “Data”, “width” → 100)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0240.json#L1533) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L822)

<a id="op-f07d0cf9a1cbbb"></a>
### Party Ledger Summary Report.get data

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_get_data`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** out.

**Local steps**

- Set company\_currency from Platform.get\_cached\_value(“Company”, self.filters.get(“company”), “default\_currency”).
- Set invoice\_dr\_or\_cr from “debit” when self.filters.party\_type equals “Customer”, otherwise “credit”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “debit”, false gives “credit”.
- Set reverse\_dr\_or\_cr from “credit” when self.filters.party\_type equals “Customer”, otherwise “debit”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “credit”, false gives “debit”.
- Set self.party\_data from Platform.\_dict(mapping()).
- For each gle in self.gl\_entries.
  - Set party\_details from self.party\_details.get(gle.party).
  - Set party\_name from party\_details.get(formatted text {scrub(self.filters.party\_type)}\_name, empty text).
  - Evaluate self.party\_data.setdefault(gle.party, Platform.\_dict(mapping(expand party\_details, “party\_name” → party\_name, “opening\_balance” → 0, “invoiced\_amount” → 0, …))).
  - Set amount from (gle.get(invoice\_dr\_or\_cr) − gle.get(reverse\_dr\_or\_cr)).
  - Update self.party\_data at gle.party.closing\_balance using + amount.
  - If (gle.posting\_date &lt; self.filters.from\_date or gle.is\_opening equals “Yes”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in gle.posting\_date &lt; self.filters.from\_date → gle.is\_opening equals “Yes”.
    - Update self.party\_data at gle.party.opening\_balance using + amount.
  - Otherwise.
    - Set party\_data from self.party\_data at gle.party.
    - If gle.voucher\_no belongs to self.return\_invoices.
      - Update party\_data.return\_amount using − amount.
    - Otherwise.
      - If gle.against\_voucher belongs to self.return\_invoices.
        - If amount &gt; 0.
          - Update party\_data.paid\_amount using − amount.
        - Otherwise.
          - Update party\_data.invoiced\_amount using + amount.
      - Otherwise.
        - If amount &gt; 0.
          - Update party\_data.invoiced\_amount using + amount.
        - Otherwise.
          - Update party\_data.paid\_amount using − amount.
- Set out from list().
- For each tuple(party, row) in self.party\_data.items().
  - If (row.opening\_balance or row.invoiced\_amount or row.paid\_amount or row.return\_amount or row.closing\_balance).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.opening\_balance → row.invoiced\_amount → row.paid\_amount → row.return\_amount → row.closing\_balance.
    - Set total\_party\_adjustment from sum(generator of amount for amount drawn from nested operand in the contract.party\_adjustment\_details.get(party, mapping()).values()).
      - Draw amount from self.party\_adjustment\_details.get(party, mapping()).values().
    - Update row.paid\_amount using − total\_party\_adjustment.
    - Set adjustments from self.party\_adjustment\_details.get(party, mapping()).
    - For each account in self.party\_adjustment\_accounts.
      - Set row at (“adj\_” + scrub(account)) from adjustments.get(account, 0).
    - If self.filters.party\_type equals “Customer”.
      - Set balance from row.get(“closing\_balance”, 0).
      - Set row at “dr\_or\_cr” from “Dr” when balance &gt; 0, otherwise “Cr” when balance &lt; 0, otherwise empty text.
        - Value choice on balance &gt; 0 — true gives “Dr”, false gives “Cr” when balance &lt; 0, otherwise empty text.
        - Value choice on balance &lt; 0 — true gives “Cr”, false gives empty text.
    - Otherwise.
      - Set balance from row.get(“closing\_balance”, 0).
      - Set row at “dr\_or\_cr” from “Cr” when balance &gt; 0, otherwise “Dr” when balance &lt; 0, otherwise empty text.
        - Value choice on balance &gt; 0 — true gives “Cr”, false gives “Dr” when balance &lt; 0, otherwise empty text.
        - Value choice on balance &lt; 0 — true gives “Dr”, false gives empty text.
    - Evaluate out.append(row).
- Return out.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0240.json#L3236) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L823)

<a id="op-78636530254299"></a>
### Party Ledger Summary Report.get gl entries

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_get_general_ledger_entries`

**Inputs** self.

**Record and data access** read “Journal Entry” via get\_all.

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Set query from qb.from\_(gle).select(gle.posting\_date, gle.party, gle.voucher\_type, gle.voucher\_no, …).where((((((nested operand in the contract &lt; nested operand in the contract bitwise and nested operand in the contract  ….
- If self.filters.get(“ignore\_cr\_dr\_notes”).
  - Set system\_generated\_cr\_dr\_journals from Platform.db.get\_all(“Journal Entry”, filters = mapping(“company” → self.filters.get(“company”), “docstatus” → 1, “voucher\_type” → tuple(“in”, list(“Credit Note”, “Debit Note”)), “is\_system\_generated” → 1,  ….
  - If system\_generated\_cr\_dr\_journals.
    - Set vouchers\_to\_ignore from ((self.filters.get(“voucher\_no\_not\_in”) or list()) + list of x at 0 for x drawn from system\_generated\_cr\_dr\_journals).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“voucher\_no\_not\_in”) → list().
      - Draw x from system\_generated\_cr\_dr\_journals.
    - Evaluate self.filters.update(mapping(“voucher\_no\_not\_in” → vouchers\_to\_ignore)).
- Set voucher\_no\_not\_in from self.filters.get(“voucher\_no\_not\_in”, list()).
- If voucher\_no\_not\_in.
  - Set query from query.where(gle.voucher\_no.notin(voucher\_no\_not\_in)).
- Set query from self.prepare\_conditions(query).
- Set self.gl\_entries from query.run(as\_dict = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare conditions](operations-032.md#op-24a4ba40e99dd8).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0240.json#L4769) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L824)

<a id="op-24a4ba40e99dd8"></a>
### Party Ledger Summary Report.prepare conditions

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_prepare_conditions`

**Inputs** self, query.

**Record and data access** read “DocType” via get\_cached\_value.

**Explicit results** query.

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- If self.filters.company.
  - Set query from query.where(gle.company equals self.filters.company).
- If self.filters.finance\_book.
  - Set query from query.where(IfNull(gle.finance\_book, empty text) equals self.filters.finance\_book).
- If self.filters.cost\_center.
  - Set query from query.where(gle.cost\_center.isin(self.filters.cost\_center)).
- If self.filters.project.
  - Set query from query.where(gle.project.isin(self.filters.project)).
- Set accounting\_dimensions from get\_accounting\_dimensions(as\_list = false).
- If accounting\_dimensions.
  - For each dimension in accounting\_dimensions.
    - If self.filters.get(dimension.fieldname).
      - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
        - Set self.filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, self.filters.get(dimension.fieldname)).
        - Set query from query.where(gle at dimension.fieldname.isin(self.filters.get(dimension.fieldname))).
      - Otherwise.
        - Set query from query.where(gle at dimension.fieldname.isin(self.filters.get(dimension.fieldname))).
- Return query.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0240.json#L5701) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L830)

<a id="op-59bec48e68abee"></a>
### Party Ledger Summary Report.get return invoices

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_get_return_invoices`

**Inputs** self.

**Record and data access** read doctype via get\_all.

**Local steps**

- Set doctype from “Sales Invoice” when self.filters.party\_type equals “Customer”, otherwise “Purchase Invoice”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “Sales Invoice”, false gives “Purchase Invoice”.
- Set filters from tuple(mapping(“is\_return” → 1, “docstatus” → 1, “posting\_date” → list(“&lt;=”, self.filters.to\_date), formatted text {scrub(self.filters.party\_type)} → list(“in”, self.parties))).
- Set self.return\_invoices from set(Platform.get\_all(doctype, filters = filters, pluck = “name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L828)

<a id="op-d7d77154923cfe"></a>
### Party Ledger Summary Report.get party adjustment amounts

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_party_ledger_summary_report_get_party_adjustment_amounts`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set account\_type from “Expense Account” when self.filters.party\_type equals “Customer”, otherwise “Income Account”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “Expense Account”, false gives “Income Account”.
- Set invoice\_dr\_or\_cr from “debit” when self.filters.party\_type equals “Customer”, otherwise “credit”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “debit”, false gives “credit”.
- Set reverse\_dr\_or\_cr from “credit” when self.filters.party\_type equals “Customer”, otherwise “debit”.
  - Value choice on self.filters.party\_type equals “Customer” — true gives “credit”, false gives “debit”.
- Set round\_off\_account from Platform.get\_cached\_value(“Company”, self.filters.company, “round\_off\_account”).
- Set current\_period\_vouchers from set().
- Set adjustment\_voucher\_entries from mapping().
- Set self.party\_adjustment\_details from mapping().
- Set self.party\_adjustment\_accounts from set().
- For each gle in self.gl\_entries.
  - If (gle.is\_opening differs from “Yes” and gle.posting\_date ≥ self.filters.from\_date and gle.posting\_date ≤ self.filters.to\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in gle.is\_opening differs from “Yes” → gle.posting\_date ≥ self.filters.from\_date → gle.posting\_date ≤ self.filters.to\_date.
    - Evaluate current\_period\_vouchers.add(tuple(gle.voucher\_type, gle.voucher\_no)).
    - Evaluate adjustment\_voucher\_entries.setdefault(tuple(gle.voucher\_type, gle.voucher\_no), list()).append(gle).
- If not current\_period\_vouchers.
  - Return no value.
- Set gl from qb.DocType(“GL Entry”).
- Set query from qb.from\_(gl).select(gl.posting\_date, gl.account, gl.party, gl.voucher\_type, …).where((((((nested operand in the contract &lt; nested operand in the contract bitwise and nested operand in the contract equals n ….
- Set query from self.prepare\_conditions(query).
- Set gl\_entries from query.run(as\_dict = true).
- For each gle in gl\_entries.
  - Evaluate adjustment\_voucher\_entries at tuple(gle.voucher\_type, gle.voucher\_no).append(gle).
- For each voucher\_gl\_entries in adjustment\_voucher\_entries.values().
  - Set parties from mapping().
  - Set accounts from mapping().
  - Set has\_irrelevant\_entry from false.
  - For each gle in voucher\_gl\_entries.
    - If gle.account equals round\_off\_account.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If gle.party.
        - Evaluate parties.setdefault(gle.party, 0).
        - Update parties at gle.party using + (gle.get(reverse\_dr\_or\_cr) − gle.get(invoice\_dr\_or\_cr)).
      - Otherwise.
        - If Platform.get\_cached\_value(“Account”, gle.account, “account\_type”) equals account\_type.
          - Evaluate accounts.setdefault(gle.account, 0).
          - Update accounts at gle.account using + (gle.get(invoice\_dr\_or\_cr) − gle.get(reverse\_dr\_or\_cr)).
        - Otherwise.
          - Set has\_irrelevant\_entry from true.
  - If (parties and accounts).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parties → accounts.
    - If len(parties) equals 1.
      - Set party from next(iter(parties.keys())).
      - For each tuple(account, amount) in accounts.items().
        - Evaluate self.party\_adjustment\_accounts.add(account).
        - Evaluate self.party\_adjustment\_details.setdefault(party, mapping()).
        - Evaluate self.party\_adjustment\_details at party.setdefault(account, 0).
        - Update self.party\_adjustment\_details at party at account using + amount.
    - Otherwise.
      - If (len(accounts) equals 1 and not has\_irrelevant\_entry).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(accounts) equals 1 → not has\_irrelevant\_entry.
        - Set account from next(iter(accounts.keys())).
        - Evaluate self.party\_adjustment\_accounts.add(account).
        - For each tuple(party, amount) in parties.items().
          - Evaluate self.party\_adjustment\_details.setdefault(party, mapping()).
          - Evaluate self.party\_adjustment\_details at party.setdefault(account, 0).
          - Update self.party\_adjustment\_details at party at account using + amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [prepare conditions](operations-032.md#op-24a4ba40e99dd8).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.filters.company, “round\_off\_account”), Platform.get\_cached\_value(“Account”, gle.account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0241.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L825)

<a id="op-6a51ac7738d31a"></a>
### Get children

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_get_children`

**Inputs** doctype, value.

**Explicit results** list(set(all\_children)).

**Local steps**

- If not isinstance(value, list).
  - Set value from list of d.strip() for d drawn from value.strip().split(“,”) where d.
    - Draw d from value.strip().split(“,”), keep a combination only if (d).
- Set all\_children from list().
- For each d in value.
  - Update all\_children using + get\_descendants\_of(doctype, d).
  - Evaluate all\_children.append(d).
- Return list(set(all\_children)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L821)

<a id="op-5344d0eefcaedb"></a>
### Execute

`operation_enterprise_accounts_report_customer_ledger_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** PartyLedgerSummaryReport(filters).run(args).

**Local steps**

- Set args from mapping(“party\_type” → “Customer”, “naming\_by” → list(“Selling Settings”, “cust\_master\_name”)).
- Return PartyLedgerSummaryReport(filters).run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0241.json#L2191) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L820)

## Report · Day book

<a id="op-6eabba658b7323"></a>
### Execute

`operation_enterprise_binding_enterprise_accounts_report_day_book_day_book_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(filters), get\_data(filters)).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Evaluate validate\_filters(filters).
- Return tuple(get\_columns(filters), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1193)

<a id="op-dd62649ec4dd5f"></a>
### Validate filters

`operation_enterprise_binding_enterprise_accounts_report_day_book_day_book_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”) · validation helper — translated “From Date must be before To Date”.

**Local steps**

- If not filters.company.
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- If getdate(filters.from\_date) &gt; getdate(filters.to\_date).
  - Call the validation error handler Platform.throw(translated “From Date must be before To Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1198)

<a id="op-bf9efe0eee7d94"></a>
### Get data

`operation_enterprise_binding_enterprise_accounts_report_day_book_day_book_get_data`

**Inputs** filters.

**Explicit results** list() · data.

**Local steps**

- Set legs from get\_legs(filters).
- If not legs.
  - Return list().
- Set party\_names from get\_party\_name\_map().
- Set vouchers from mapping().
- For each leg in legs.
  - Set key from tuple(leg.voucher\_type, leg.voucher\_no).
  - Evaluate vouchers.setdefault(key, list()).append(leg).
- Set data from list().
- Set precision from Platform.get\_precision(“GL Entry”, “debit”).
- For each tuple(tuple(voucher\_type, voucher\_no), voucher\_legs) in vouchers.items().
  - For each leg in voucher\_legs.
    - Set leg.balance from flt((leg.debit − leg.credit), precision).
    - Set leg.particulars from (party\_names.get(leg.party\_type, mapping()).get(leg.party) or leg.party or leg.account).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_names.get(leg.party\_type, mapping()).get(leg.party) → leg.party → leg.account.
  - Set main from get\_main\_leg(voucher\_legs).
  - Set key from formatted text {voucher\_type}::{voucher\_no}.
  - Evaluate data.append(mapping(“voucher” → key, “indent” → 0, “posting\_date” → main.posting\_date, “particulars” → main.particulars, …)).
    - Value choice on main.balance &gt; 0 — true gives main.balance, false gives no value.
    - Value choice on main.balance &lt; 0 — true gives negative main.balance, false gives no value.
  - For each tuple(idx, leg) in enumerate(voucher\_legs when filters.detailed, otherwise list()).
    - Value choice on filters.detailed — true gives voucher\_legs, false gives list().
    - If not leg.balance.
      - Continue with the next iteration or loop test.
    - Evaluate data.append(mapping(“voucher” → formatted text {key}::{idx}, “parent\_voucher” → key, “indent” → 1, “particulars” → leg.particulars, …)).
      - Value choice on leg.balance &gt; 0 — true gives leg.balance, false gives no value.
      - Value choice on leg.balance &lt; 0 — true gives negative leg.balance, false gives no value.
- Return data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1195)

<a id="op-080ec0bf64b3fe"></a>
### Get main leg

`operation_enterprise_binding_enterprise_accounts_report_day_book_day_book_get_main_leg`

**Inputs** legs.

**Explicit results** max(candidates, key = deferred anonymous expression).

**Local steps**

- Set with\_party from list of leg for leg drawn from legs where leg.party.
  - Draw leg from legs, keep a combination only if (leg.party).
- Set candidates from (with\_party or list of leg for leg drawn from legs where leg.balance &gt; 0 or legs).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in with\_party → list of leg for leg drawn from legs where leg.balance &gt; 0 → legs.
  - Draw leg from legs, keep a combination only if (leg.balance &gt; 0).
- Return max(candidates, key = deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1197)

<a id="op-c2ff312346b07f"></a>
### Get legs

`operation_enterprise_binding_enterprise_accounts_report_day_book_day_book_get_legs`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set gle from qb.DocType(“GL Entry”).
- Set company\_fb from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
- Set query from nested operand in the contract(nested operand in the contract).groupby(gle.voucher\_type, gle.voucher\_no, gle.account, gle.party\_type, …).orderby(Min(gle.posting\_date)).orderby(Min(gle.creation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company\_fb → empty text.
- If filters.voucher\_type.
  - Set query from query.where(gle.voucher\_type equals filters.voucher\_type).
- If match\_conditions bound to build\_match\_conditions(“GL Entry”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Return query.run(as\_dict = true).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1196)

<a id="op-e26411235c102b"></a>
### Get columns

`operation_enterprise_binding_enterprise_accounts_report_day_book_day_book_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Date”, “fieldname” → “posting\_date”, “fieldtype” → “Date”, “width” → 120), mapping(“label” → translated “Particulars”, “fieldname” → “particulars”, “fieldtype” → “Data”,  ….
- If filters.show\_remarks.
  - Evaluate columns.append(mapping(“label” → translated “Remarks”, “fieldname” → “remarks”, “fieldtype” → “Data”, “width” → 300)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1194)

## Service · Deferred revenue

<a id="op-bf09c5fef858f1"></a>
### Validate service stop date

`operation_enterprise_accounts_deferred_revenue_business_behavior_validate_service_stop_date`

**Inputs** doc.

**Record and data access** read formatted text {doc.doctype} Item via get\_all.

**Explicit failure paths** validation helper — translated “Service Stop Date cannot be before Service Start Date” · validation helper — translated “Service Stop Date cannot be after Service End Date” · validation helper — translated “Cannot change Service Stop Date for item in row {0}”.format(item.idx).

**Local steps**

- Set enable\_check from “enable\_deferred\_revenue” when doc.doctype equals “Sales Invoice”, otherwise “enable\_deferred\_expense”.
  - Value choice on doc.doctype equals “Sales Invoice” — true gives “enable\_deferred\_revenue”, false gives “enable\_deferred\_expense”.
- Set old\_stop\_dates from mapping().
- Set old\_doc from Platform.db.get\_all(formatted text {doc.doctype} Item, mapping(“parent” → doc.name), list(“name”, “service\_stop\_date”)).
- For each d in old\_doc.
  - Set old\_stop\_dates at d.name from (d.service\_stop\_date or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.service\_stop\_date → empty text.
- For each item in doc.items.
  - If not item.get(enable\_check).
    - Continue with the next iteration or loop test.
  - If item.service\_stop\_date.
    - If date\_diff(item.service\_stop\_date, item.service\_start\_date) &lt; 0.
      - Call the validation error handler Platform.throw(translated “Service Stop Date cannot be before Service Start Date”).
    - If date\_diff(item.service\_stop\_date, item.service\_end\_date) &gt; 0.
      - Call the validation error handler Platform.throw(translated “Service Stop Date cannot be after Service End Date”).
  - If (old\_stop\_dates and old\_stop\_dates.get(item.name) and item.service\_stop\_date and getdate(item.service\_stop\_date) differs from getdate(old\_stop\_dates.get(item.name))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_stop\_dates → old\_stop\_dates.get(item.name) → item.service\_stop\_date → getdate(item.service\_stop\_date) differs from getdate(old\_stop\_dates.get(item.name)).
    - Call the validation error handler Platform.throw(translated “Cannot change Service Stop Date for item in row {0}”.format(item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0003.json#L2375) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L32) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L26)

<a id="op-9b303fc73c5e47"></a>
### Build conditions

`operation_enterprise_accounts_deferred_revenue_business_behavior_build_conditions`

**Inputs** process\_type, account, company.

**Explicit results** conditions.

**Local steps**

- Set conditions from empty text.
- Set deferred\_account from “item.deferred\_revenue\_account” when process\_type equals “Income”, otherwise “item.deferred\_expense\_account”.
  - Value choice on process\_type equals “Income” — true gives “item.deferred\_revenue\_account”, false gives “item.deferred\_expense\_account”.
- If account.
  - Update conditions using + formatted text AND {deferred\_account}={Platform.db.escape(account)}.
- Otherwise.
  - If company.
    - Update conditions using + formatted text AND p.company = {Platform.db.escape(company)}.
- Return conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L21) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L15)

<a id="op-d00c1c7b96ba1d"></a>
### Convert deferred expense to expense

`operation_enterprise_accounts_deferred_revenue_business_behavior_convert_deferred_expense_to_expense`

**Inputs** deferred\_process, start\_date = no value, end\_date = no value, conditions = empty text.

**Record and data access** resolve a document from “Purchase Invoice” via get\_doc.

**Local steps**

- If not start\_date.
  - Set start\_date from add\_months(today(), negative 1).
- If not end\_date.
  - Set end\_date from add\_days(today(), negative 1).
- Set invoices from Platform.db.sql\_list(formatted text   select distinct item.parent  from ′tabPurchase Invoice Item′ item, ′tabPurchase Invoice′ p  where item.service\_start\_date&lt;=%s and item.service\_en, tuple(end\_date, s ….
- For each invoice in invoices.
  - Set doc from Platform.get\_doc(“Purchase Invoice”, invoice).
  - Evaluate book\_deferred\_income\_or\_expense(doc, deferred\_process, end\_date).
- If Platform.flags.deferred\_accounting\_error.
  - Evaluate send\_mail(deferred\_process).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L24) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L18)

<a id="op-a69f308b8dadd0"></a>
### Convert deferred revenue to income

`operation_enterprise_accounts_deferred_revenue_business_behavior_convert_deferred_revenue_to_income`

**Inputs** deferred\_process, start\_date = no value, end\_date = no value, conditions = empty text.

**Record and data access** resolve a document from “Sales Invoice” via get\_doc.

**Local steps**

- If not start\_date.
  - Set start\_date from add\_months(today(), negative 1).
- If not end\_date.
  - Set end\_date from add\_days(today(), negative 1).
- Set invoices from Platform.db.sql\_list(formatted text   select distinct item.parent  from ′tabSales Invoice Item′ item, ′tabSales Invoice′ p  where item.service\_start\_date&lt;=%s and item.service\_end\_date, tuple(end\_date, s ….
- For each invoice in invoices.
  - Set doc from Platform.get\_doc(“Sales Invoice”, invoice).
  - Evaluate book\_deferred\_income\_or\_expense(doc, deferred\_process, end\_date).
- If Platform.flags.deferred\_accounting\_error.
  - Evaluate send\_mail(deferred\_process).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L25) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L19)

<a id="op-75ffff4f05ef35"></a>
### Get booking dates

`operation_enterprise_accounts_deferred_revenue_business_behavior_get_booking_dates`

**Inputs** doc, item, posting\_date = no value, prev\_posting\_date = no value.

**Record and data access** execute query text (SELECT, GL Entry) · execute query text (SELECT, Journal Entry).

**Explicit results** tuple(start\_date, end\_date, last\_gl\_entry) · tuple(no value, no value, no value).

**Local steps**

- If not posting\_date.
  - Set posting\_date from add\_days(today(), negative 1).
- Set last\_gl\_entry from false.
- Set deferred\_account from “deferred\_revenue\_account” when doc.doctype equals “Sales Invoice”, otherwise “deferred\_expense\_account”.
  - Value choice on doc.doctype equals “Sales Invoice” — true gives “deferred\_revenue\_account”, false gives “deferred\_expense\_account”.
- If not prev\_posting\_date.
  - Set prev\_gl\_entry from Platform.db.sql(query text (SELECT, GL Entry), tuple(doc.company, item.get(deferred\_account), doc.doctype, doc.name, …), as\_dict = true).
  - Set prev\_gl\_via\_je from Platform.db.sql(query text (SELECT, Journal Entry), tuple(doc.company, item.get(deferred\_account), doc.doctype, doc.name, …), as\_dict = true).
  - If prev\_gl\_via\_je.
    - If (not prev\_gl\_entry or (prev\_gl\_entry and prev\_gl\_entry at 0.posting\_date &lt; prev\_gl\_via\_je at 0.posting\_date)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not prev\_gl\_entry → (prev\_gl\_entry and prev\_gl\_entry at 0.posting\_date &lt; prev\_gl\_via\_je at 0.posting\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in prev\_gl\_entry → prev\_gl\_entry at 0.posting\_date &lt; prev\_gl\_via\_je at 0.posting\_date.
      - Set prev\_gl\_entry from prev\_gl\_via\_je.
  - If prev\_gl\_entry.
    - Set start\_date from getdate(add\_days(prev\_gl\_entry at 0.posting\_date, 1)).
  - Otherwise.
    - Set start\_date from item.service\_start\_date.
- Otherwise.
  - Set start\_date from getdate(add\_days(prev\_posting\_date, 1)).
- Set end\_date from get\_last\_day(start\_date).
- If end\_date ≥ item.service\_end\_date.
  - Set end\_date from item.service\_end\_date.
  - Set last\_gl\_entry from true.
- Otherwise.
  - If (item.service\_stop\_date and end\_date ≥ item.service\_stop\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.service\_stop\_date → end\_date ≥ item.service\_stop\_date.
    - Set end\_date from item.service\_stop\_date.
    - Set last\_gl\_entry from true.
- If end\_date &gt; getdate(posting\_date).
  - Set end\_date from posting\_date.
- If getdate(start\_date) ≤ getdate(end\_date).
  - Return tuple(start\_date, end\_date, last\_gl\_entry).
- Otherwise.
  - Return tuple(no value, no value, no value).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L27) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L21)

<a id="op-54e98c7d950de3"></a>
### Calculate monthly amount

`operation_enterprise_accounts_deferred_revenue_business_behavior_calculate_monthly_amount`

**Inputs** doc, item, last\_gl\_entry, start\_date, end\_date, total\_days, total\_booking\_days, account\_currency.

**Explicit results** tuple(amount, base\_amount).

**Local steps**

- Set tuple(amount, base\_amount) from tuple(0, 0).
- If not last\_gl\_entry.
  - Set total\_months from ((((item.service\_end\_date.year − item.service\_start\_date.year) × 12) + (item.service\_end\_date.month − item.service\_start\_date.month)) + 1).
  - Set prorate\_factor from (flt(date\_diff(item.service\_end\_date, item.service\_start\_date)) ÷ flt(date\_diff(get\_last\_day(item.service\_end\_date), get\_first\_day(item.service\_start\_date)))).
  - Set actual\_months from rounded((total\_months × prorate\_factor), 1).
  - Set tuple(already\_booked\_amount, already\_booked\_amount\_in\_account\_currency) from get\_already\_booked\_amount(doc, item).
  - Set base\_amount from flt((item.base\_net\_amount ÷ actual\_months), item.precision(“base\_net\_amount”)).
  - If (base\_amount + already\_booked\_amount) &gt; item.base\_net\_amount.
    - Set base\_amount from (item.base\_net\_amount − already\_booked\_amount).
  - If account\_currency equals doc.company\_currency.
    - Set amount from base\_amount.
  - Otherwise.
    - Set amount from flt((item.net\_amount ÷ actual\_months), item.precision(“net\_amount”)).
    - If (amount + already\_booked\_amount\_in\_account\_currency) &gt; item.net\_amount.
      - Set amount from (item.net\_amount − already\_booked\_amount\_in\_account\_currency).
  - If (get\_first\_day(start\_date) differs from start\_date or get\_last\_day(end\_date) differs from end\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_first\_day(start\_date) differs from start\_date → get\_last\_day(end\_date) differs from end\_date.
    - Set partial\_month from (flt(date\_diff(end\_date, start\_date)) ÷ flt(date\_diff(get\_last\_day(end\_date), get\_first\_day(start\_date)))).
    - Set base\_amount from (rounded(partial\_month, 1) × base\_amount).
    - Set amount from (rounded(partial\_month, 1) × amount).
- Otherwise.
  - Set tuple(already\_booked\_amount, already\_booked\_amount\_in\_account\_currency) from get\_already\_booked\_amount(doc, item).
  - Set base\_amount from flt((item.base\_net\_amount − already\_booked\_amount), item.precision(“base\_net\_amount”)).
  - If account\_currency equals doc.company\_currency.
    - Set amount from base\_amount.
  - Otherwise.
    - Set amount from flt((item.net\_amount − already\_booked\_amount\_in\_account\_currency), item.precision(“net\_amount”)).
- Return tuple(amount, base\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0003.json#L6199) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L23) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L17)

<a id="op-4f67e1624dedb5"></a>
### Calculate amount

`operation_enterprise_accounts_deferred_revenue_business_behavior_calculate_amount`

**Inputs** doc, item, last\_gl\_entry, total\_days, total\_booking\_days, account\_currency.

**Explicit results** tuple(amount, base\_amount).

**Local steps**

- Set tuple(amount, base\_amount) from tuple(0, 0).
- If not last\_gl\_entry.
  - Set base\_amount from flt(((item.base\_net\_amount × total\_booking\_days) ÷ flt(total\_days)), item.precision(“base\_net\_amount”)).
  - If account\_currency equals doc.company\_currency.
    - Set amount from base\_amount.
  - Otherwise.
    - Set amount from flt(((item.net\_amount × total\_booking\_days) ÷ flt(total\_days)), item.precision(“net\_amount”)).
- Otherwise.
  - Set tuple(already\_booked\_amount, already\_booked\_amount\_in\_account\_currency) from get\_already\_booked\_amount(doc, item).
  - Set base\_amount from flt((item.base\_net\_amount − already\_booked\_amount), item.precision(“base\_net\_amount”)).
  - If account\_currency equals doc.company\_currency.
    - Set amount from base\_amount.
  - Otherwise.
    - Set amount from flt((item.net\_amount − already\_booked\_amount\_in\_account\_currency), item.precision(“net\_amount”)).
- Return tuple(amount, base\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0004.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L22) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L16)
