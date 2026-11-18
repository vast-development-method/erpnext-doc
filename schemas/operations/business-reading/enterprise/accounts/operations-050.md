# Accounting and settlement · operations 50

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Gl entry

<a id="op-1de5a76106ddbc"></a>
### GLEntry.pl must have cost center

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_profit_and_loss_must_have_cost_center`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (self.cost\_center or self.voucher\_type equals “Period Closing Voucher”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → self.voucher\_type equals “Period Closing Voucher”.
  - Return no value.
- If Platform.get\_cached\_value(“Account”, self.account, “report\_type”) equals “Profit and Loss”.
  - Set msg from translated “{0} {1}: Cost Center is required for 'Profit and Loss' account {2}.”.format(self.voucher\_type, self.voucher\_no, self.account).
  - Update msg using + one space.
  - Update msg using + translated “Please set the cost center field in {0} or setup a default Cost Center for the Company.”.format(self.voucher\_type).
  - Call the validation error handler Platform.throw(msg, title = translated “Missing Cost Center”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L2284) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1054)

<a id="op-4cbc046bfa6e70"></a>
### GLEntry.validate dimensions for pl and bs

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_validate_dimensions_for_profit_and_loss_and_balance_sheet`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Profit and Loss' account {1}.”.format(dimension.label, self.account) · validation helper — translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Balance Sheet' account {1}.”.format(dimension.label, self.account).

**Local steps**

- Set account\_type from Platform.get\_cached\_value(“Account”, self.account, “report\_type”).
- For each dimension in get\_checks\_for\_pl\_and\_bs\_accounts().
  - If (account\_type equals “Profit and Loss” and self.company equals dimension.company and dimension.mandatory\_for\_pl and not self.is\_cancelled).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type equals “Profit and Loss” → self.company equals dimension.company → dimension.mandatory\_for\_pl → not self.is\_cancelled.
    - If not self.get(dimension.fieldname).
      - Call the validation error handler Platform.throw(translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Profit and Loss' account {1}.”.format(dimension.label, self.account)).
  - If (account\_type equals “Balance Sheet” and self.company equals dimension.company and dimension.mandatory\_for\_bs and not self.is\_cancelled).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type equals “Balance Sheet” → self.company equals dimension.company → dimension.mandatory\_for\_bs → not self.is\_cancelled.
    - If not self.get(dimension.fieldname).
      - Call the validation error handler Platform.throw(translated “Accounting Dimension &lt;b&gt;{0}&lt;/b&gt; is required for 'Balance Sheet' account {1}.”.format(dimension.label, self.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L2595) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1061)

<a id="op-c7d82fc65b8250"></a>
### GLEntry.check pl account

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_check_profit_and_loss_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} {1}: 'Profit and Loss' type account {2} not allowed in Opening Entry”.format(self.voucher\_type, self.voucher\_no, self.account).

**Local steps**

- If (self.is\_opening equals “Yes” and Platform.get\_cached\_value(“Account”, self.account, “report\_type”) equals “Profit and Loss” and not self.is\_cancelled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_opening equals “Yes” → Platform.get\_cached\_value(“Account”, self.account, “report\_type”) equals “Profit and Loss” → not self.is\_cancelled.
  - Call the validation error handler Platform.throw(translated “{0} {1}: 'Profit and Loss' type account {2} not allowed in Opening Entry”.format(self.voucher\_type, self.voucher\_no, self.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L3048) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1051)

<a id="op-4473b407719b1b"></a>
### GLEntry.validate account details

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_validate_account_details`

**Inputs** self, adv\_adj.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} {1}: Account {2} is a Group Account and group accounts cannot be used in transactions”.format(self.voucher\_type, self.voucher\_no, self.account) · validation helper — translated “{0} {1}: Account {2} is inactive”.format(self.voucher\_type, self.voucher\_no, self.account) · validation helper — translated “{0} {1}: Account {2} does not belong to Company {3}”.format(self.voucher\_type, self.voucher\_no, self.account, self.company).

**Local steps**

- Set account from Platform.get\_cached\_value(“Account”, self.account, fieldname = list(“is\_group”, “docstatus”, “company”), as\_dict = true).
- If account.is\_group equals 1.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Account {2} is a Group Account and group accounts cannot be used in transactions”.format(self.voucher\_type, self.voucher\_no, self.account)).
- <a id="op-4473b407719b1b-guard-15"></a>If account.docstatus equals 2.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Account {2} is inactive”.format(self.voucher\_type, self.voucher\_no, self.account)).
- If account.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Account {2} does not belong to Company {3}”.format(self.voucher\_type, self.voucher\_no, self.account, self.company)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison account.docstatus equals 2, account.docstatus = 2 (cancelled) selects the branch that calls the validation-error handler with translated “{0} {1}: Account {2} is inactive”.format(self.voucher\_type, self.voucher\_no, self.account). With account.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4473b407719b1b-guard-15)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, fieldname = list(“is\_group”, “docstatus”, “company”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L3253) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1057)

<a id="op-2a6e28012caba9"></a>
### GLEntry.validate cost center

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_validate_cost_center`

**Inputs** self.

**Record and data access** read “Cost Center” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} {1}: Cost Center {2} does not belong to Company {3}”.format(self.voucher\_type, self.voucher\_no, self.cost\_center, self.company) · validation helper — translated “{0} {1}: Cost Center {2} is a group cost center and group cost centers cannot be used in transactions”.format(self.voucher\_type, self.voucher\_no, Platform.bold(self.cost\_center)).

**Local steps**

- If (not self.cost\_center or self.is\_cancelled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.cost\_center → self.is\_cancelled.
  - Return no value.
- Set tuple(is\_group, company) from Platform.get\_cached\_value(“Cost Center”, self.cost\_center, list(“is\_group”, “company”)).
- If company differs from self.company.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Cost Center {2} does not belong to Company {3}”.format(self.voucher\_type, self.voucher\_no, self.cost\_center, self.company)).
- If (self.voucher\_type differs from “Period Closing Voucher” and is\_group).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type differs from “Period Closing Voucher” → is\_group.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Cost Center {2} is a group cost center and group cost centers cannot be used in transactions”.format(self.voucher\_type, self.voucher\_no, Platform.bold(self.cost\_center))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Cost Center”, self.cost\_center, list(“is\_group”, “company”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L3690) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1059)

<a id="op-b4d6a8af2fec3e"></a>
### GLEntry.validate party

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_validate_party`

**Inputs** self.

**Local steps**

- Evaluate validate\_party\_frozen\_disabled(self.company, self.party\_type, self.party).
- Evaluate validate\_account\_party\_type(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L4074) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1062)

<a id="op-bde378a357ed12"></a>
### GLEntry.validate currency

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_validate_currency`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidAccountCurrency — translated “{0} {1}: Accounting Entry for {2} can only be made in currency: {3}”.format(self.voucher\_type, self.voucher\_no, self.account, (account\_currency or company\_currency)).

**Local steps**

- If self.is\_cancelled.
  - Return no value.
- Set company\_currency from Enterprise.get\_company\_currency(self.company).
- Set account\_currency from get\_account\_currency(self.account).
- If not self.account\_currency.
  - Set self.account\_currency from (account\_currency or company\_currency).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_currency → company\_currency.
- If account\_currency differs from self.account\_currency.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Accounting Entry for {2} can only be made in currency: {3}”.format(self.voucher\_type, self.voucher\_no, self.account, (account\_currency or company\_currency)), InvalidAcco ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_currency → company\_currency.
- If (self.party\_type and self.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_type → self.party.
  - Evaluate validate\_party\_gle\_currency(self.party\_type, self.party, self.company, self.account\_currency).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L4167) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1060)

<a id="op-44d4954c5560f6"></a>
### GLEntry.set amount in reporting currency

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_set_amount_in_reporting_currency`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with ReportingCurrencyExchangeNotFoundError.

**Local steps**

- Set tuple(default\_currency, reporting\_currency) from Platform.get\_cached\_value(“Company”, self.company, list(“default\_currency”, “reporting\_currency”)).
- If not reporting\_currency.
  - Return no value.
- Set transaction\_date from (self.transaction\_date or self.posting\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.transaction\_date → self.posting\_date.
- Set self.reporting\_currency\_exchange\_rate from get\_exchange\_rate(default\_currency, reporting\_currency, transaction\_date).
- If not self.reporting\_currency\_exchange\_rate.
  - Call the validation error handler Platform.throw(title = translated “Reporting Currency Exchange Not Found”, msg = translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually. ….
- Set self.debit\_in\_reporting\_currency from flt((self.debit × self.reporting\_currency\_exchange\_rate)).
- Set self.credit\_in\_reporting\_currency from flt((self.credit × self.reporting\_currency\_exchange\_rate)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, list(“default\_currency”, “reporting\_currency”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1055)

<a id="op-ac22c714598223"></a>
### GLEntry.validate and set fiscal year

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_validate_and_set_fiscal_year`

**Inputs** self.

**Local steps**

- If not self.fiscal\_year.
  - Set self.fiscal\_year from get\_fiscal\_year(self.posting\_date, company = self.company) at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L4911) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1058)

<a id="op-8ebef86a3733aa"></a>
### GLEntry.on cancel

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_on_cancel`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set msg from translated “Individual GL Entry cannot be cancelled.”.
- Update msg using + (text in the contract + translated “Please cancel related transaction.”).
- Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L5017) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1052)

<a id="op-02cd339a4c0021"></a>
### Validate balance type

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_validate_balance_type`

**Inputs** account, adv\_adj = false.

**Record and data access** read “Account” via get\_cached\_value · execute query text (SELECT, GL Entry).

**Explicit failure paths** validation helper — translated “Balance for Account {0} must always be {1}”.format(account, translated balance\_must\_be).

**Local steps**

- If (not adv\_adj and account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not adv\_adj → account.
  - Set balance\_must\_be from Platform.get\_cached\_value(“Account”, account, “balance\_must\_be”).
  - If balance\_must\_be.
    - Set balance from Platform.db.sql(query text (SELECT, GL Entry), account) at 0 at 0.
    - If ((balance\_must\_be equals “Debit” and flt(balance) &lt; 0) or (balance\_must\_be equals “Credit” and flt(balance) &gt; 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (balance\_must\_be equals “Debit” and flt(balance) &lt; 0) → (balance\_must\_be equals “Credit” and flt(balance) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in balance\_must\_be equals “Debit” → flt(balance) &lt; 0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in balance\_must\_be equals “Credit” → flt(balance) &gt; 0.
      - Call the validation error handler Platform.throw(translated “Balance for Account {0} must always be {1}”.format(account, translated balance\_must\_be)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “balance\_must\_be”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1068)

<a id="op-abea5c167edeb6"></a>
### Update outstanding amt

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_update_outstanding_amount`

**Inputs** account, party\_type, party, against\_voucher\_type, against\_voucher, on\_cancel = false.

**Record and data access** read against\_voucher\_type via get\_cached\_value · resolve a document from against\_voucher\_type via get\_doc.

**State and service calls** execute a supplied database query · request set\_value on against\_voucher\_type.

**Explicit failure paths** validation helper — translated “Against Journal Entry {0} is already adjusted against some other voucher”.format(against\_voucher) · validation helper — translated “Outstanding for {0} cannot be less than zero ({1})”.format(against\_voucher, fmt\_money(bal)).

**Local steps**

- If (party\_type and party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
  - Set party\_condition from “ and party\_type={} and party={}”.format(Platform.db.escape(party\_type), Platform.db.escape(party)).
- Otherwise.
  - Set party\_condition from empty text.
- If against\_voucher\_type equals “Sales Invoice”.
  - Set party\_account from Platform.get\_cached\_value(against\_voucher\_type, against\_voucher, “debit\_to”).
  - Set account\_condition from formatted text and account in ({Platform.db.escape(account)}, {Platform.db.escape(party\_account)}).
- Otherwise.
  - Set account\_condition from formatted text  and account = {Platform.db.escape(account)}.
- Set bal from flt((nested operand in the contract.db.sql(formatted text   select sum(debit\_in\_account\_currency) - sum(credit\_in\_account\_currency)  from ′tabGL Entry′  where against\_voucher\_type=%s and against\_voucher=%s, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.sql(formatted text   select sum(debit\_in\_account\_currency) - sum(credit\_in\_account\_currency)  from ′tabGL Entry′  where against\_voucher\_type=%s and against\_voucher=%s, tuple(against\_voucher\_ … → 0.0.
- If against\_voucher\_type equals “Purchase Invoice”.
  - Set bal from negative bal.
- Otherwise.
  - If against\_voucher\_type equals “Journal Entry”.
    - Set against\_voucher\_amount from flt(Platform.db.sql(formatted text   select sum(debit\_in\_account\_currency) - sum(credit\_in\_account\_currency)  from ′tabGL Entry′ where voucher\_type = 'Journal Entry' and voucher\_no , tuple(against\_vouc ….
    - If not against\_voucher\_amount.
      - Call the validation error handler Platform.throw(translated “Against Journal Entry {0} is already adjusted against some other voucher”.format(against\_voucher)).
    - Set bal from (against\_voucher\_amount + bal).
    - If against\_voucher\_amount &lt; 0.
      - Set bal from negative bal.
    - If (bal &lt; 0 and not on\_cancel).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in bal &lt; 0 → not on\_cancel.
      - Call the validation error handler Platform.throw(translated “Outstanding for {0} cannot be less than zero ({1})”.format(against\_voucher, fmt\_money(bal))).
- If against\_voucher\_type belongs to OUTSTANDING\_DOCTYPES.
  - Set ref\_doc from Platform.get\_doc(against\_voucher\_type, against\_voucher).
  - Set ref\_doc.outstanding\_amount from bal.
  - Evaluate Platform.db.set\_value(against\_voucher\_type, against\_voucher, “outstanding\_amount”, bal).
  - Evaluate ref\_doc.set\_status(update = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(against\_voucher\_type, against\_voucher, “debit\_to”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1067)

<a id="op-1d356a29ef72ed"></a>
### Validate frozen account

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_validate_frozen_account`

**Inputs** company, account, adv\_adj = no value.

**Record and data access** read “Account” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Account {0} is frozen”.format(account) · validation helper — translated “Not authorized to edit frozen Account {0}”.format(account).

**Local steps**

- Set frozen\_account from Platform.get\_cached\_value(“Account”, account, “freeze\_account”).
- If (frozen\_account equals “Yes” and not adv\_adj).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in frozen\_account equals “Yes” → not adv\_adj.
  - Set role\_allowed\_for\_frozen\_entries from Platform.get\_cached\_value(“Company”, company, “role\_allowed\_for\_frozen\_entries”).
  - If not role\_allowed\_for\_frozen\_entries.
    - Call the validation error handler Platform.throw(translated “Account {0} is frozen”.format(account)).
  - Otherwise.
    - If role\_allowed\_for\_frozen\_entries does not belong to Platform.get\_roles().
      - Call the validation error handler Platform.throw(translated “Not authorized to edit frozen Account {0}”.format(account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “freeze\_account”), Platform.get\_cached\_value(“Company”, company, “role\_allowed\_for\_frozen\_entries”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1069)

<a id="op-f527fb3c05db4a"></a>
### Update against account

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_update_against_account`

**Inputs** voucher\_type, voucher\_no.

**Record and data access** read “GL Entry” via get\_all.

**State and service calls** request set\_value on “GL Entry”.

**Explicit results** no value.

**Local steps**

- Set entries from Platform.db.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no), fields = list(“name”, “party”, “against”, “debit”, …)).
- If not entries.
  - Return no value.
- Set company\_currency from Enterprise.get\_company\_currency(entries at 0.company).
- Set precision from get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit”), currency = company\_currency).
- Set tuple(accounts\_debited, accounts\_credited) from tuple(list(), list()).
- For each d in entries.
  - If flt(d.debit, precision) &gt; 0.
    - Evaluate accounts\_debited.append((d.party or d.account)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.party → d.account.
  - If flt(d.credit, precision) &gt; 0.
    - Evaluate accounts\_credited.append((d.party or d.account)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.party → d.account.
- For each d in entries.
  - If flt(d.debit, precision) &gt; 0.
    - Set new\_against from “, ”.join(list(set(accounts\_credited))).
  - If flt(d.credit, precision) &gt; 0.
    - Set new\_against from “, ”.join(list(set(accounts\_debited))).
  - If d.against differs from new\_against.
    - Evaluate Platform.db.set\_value(“GL Entry”, d.name, “against”, new\_against).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L341) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1066)

<a id="op-0c39d675125e8f"></a>
### On doctype update

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “GL Entry”.

**Local steps**

- Evaluate Platform.db.add\_index(“GL Entry”, list(“voucher\_type”, “voucher\_no”)).
- Evaluate Platform.db.add\_index(“GL Entry”, list(“posting\_date”, “company”)).
- Evaluate Platform.db.add\_index(“GL Entry”, list(“party\_type”, “party”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1063)

<a id="op-f4b40eb204a91d"></a>
### Rename gle sle docs

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_rename_general_ledger_entry_stock_ledger_entry_records`

**Inputs** no declared parameters.

**Local steps**

- For each doctype in list(“GL Entry”, “Stock Ledger Entry”).
  - Evaluate rename\_temporarily\_named\_docs(doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L1576) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1064)

<a id="op-f2e9fd5c80d5d9"></a>
### Rename temporarily named docs

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_rename_temporarily_named_records`

**Inputs** doctype.

**Record and data access** read doctype via get\_all.

**State and service calls** execute a supplied database query · commit.

**Local steps**

- Set docs\_to\_rename from Platform.get\_all(doctype, mapping(“to\_rename” → “1”), order\_by = “creation”, limit = 50000).
- Set autoname from Platform.get\_meta(doctype).autoname.
- For each batch in create\_batch(docs\_to\_rename, 100).
  - For each doc in batch.
    - Set oldname from doc.name.
    - Evaluate set\_name\_from\_naming\_options(autoname, doc).
    - Set newname from doc.name.
    - Evaluate Platform.db.sql(formatted text UPDATE ′tab{doctype}′ SET name = %s, to\_rename = 0, modified = %s where name = %s, tuple(newname, now(), oldname)).
    - For each hook\_type in tuple(“on\_gle\_rename”, “on\_sle\_rename”).
      - For each hook in Platform.get\_hooks(hook\_type).
        - Evaluate Platform.call(hook, newname = newname, oldname = oldname).
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now() · selected callable from Platform.get\_hooks(hook\_type).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1065)

## Report · Gross and net profit report

<a id="op-73b6730dea2407"></a>
### Execute

`operation_enterprise_accounts_report_gross_and_net_profit_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set period\_list from get\_period\_list(filters.from\_fiscal\_year, filters.to\_fiscal\_year, filters.period\_start\_date, filters.period\_end\_date, …).
- Set tuple(columns, data) from tuple(list(), list()).
- Set income from get\_data(filters.company, “Income”, “Credit”, period\_list, filters = filters, accumulated\_values = filters.accumulated\_values, ignore\_closing\_entries = true, ignore\_accumulated\_values\_for\_fy = bool(filters ….
- Set expense from get\_data(filters.company, “Expense”, “Debit”, period\_list, filters = filters, accumulated\_values = filters.accumulated\_values, ignore\_closing\_entries = true, ignore\_accumulated\_values\_for\_fy = bool(filters ….
- Set columns from get\_columns(filters.periodicity, period\_list, filters.accumulated\_values, filters.company).
- Set gross\_income from get\_revenue(income, period\_list).
- Set gross\_expense from get\_revenue(expense, period\_list).
- If (gross\_income or gross\_expense).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gross\_income → gross\_expense.
  - Evaluate data.extend(get\_gross\_rows(gross\_income, gross\_expense, period\_list, filters)).
- Otherwise.
  - Evaluate data.append(mapping(“account\_name” → ((“'” + translated “Nothing is included in gross”) + “'”), “account” → ((“'” + translated “Nothing is included in gross”) + “'”))).
- Set non\_gross\_income from get\_revenue(income, period\_list, 0).
- Evaluate data.append(mapping()).
- Evaluate data.extend((non\_gross\_income or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in non\_gross\_income → list().
- Set non\_gross\_expense from get\_revenue(expense, period\_list, 0).
- Evaluate data.append(mapping()).
- Evaluate data.extend((non\_gross\_expense or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in non\_gross\_expense → list().
- Set net\_profit from get\_net\_profit(non\_gross\_income, gross\_income, gross\_expense, non\_gross\_expense, …).
- If net\_profit.
  - Evaluate data.append(mapping()).
  - Evaluate data.append(net\_profit).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L990)

<a id="op-fe50dab062ab53"></a>
### Get gross rows

`operation_enterprise_binding_enterprise_accounts_report_gross_and_net_profit_report_gross_and_net_profit_report_get_gross_rows`

**Inputs** gross\_income, gross\_expense, period\_list, filters.

**Explicit results** data.

**Local steps**

- Set data from list(mapping(“account\_name” → ((“'” + translated “Included in Gross Profit”) + “'”), “account” → ((“'” + translated “Included in Gross Profit”) + “'”))).
- Set gross\_income from (gross\_income or list(mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gross\_income → list(mapping()).
- Set gross\_expense from (gross\_expense or list(mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gross\_expense → list(mapping()).
- Evaluate data.append(mapping()).
- Evaluate data.extend(gross\_income).
- Evaluate data.append(mapping()).
- Evaluate data.extend(gross\_expense).
- Evaluate data.append(mapping()).
- Set gross\_profit from get\_profit(gross\_income, gross\_expense, period\_list, filters.company, …).
- Evaluate data.append(gross\_profit).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1214)

<a id="op-cd37247a438304"></a>
### Get revenue

`operation_enterprise_accounts_report_gross_and_net_profit_report_business_behavior_get_revenue`

**Inputs** data, period\_list, include\_in\_gross = 1.

**Explicit results** copy.deepcopy(revenue).

**Local steps**

- Set revenue from list of item for item drawn from data where (item at “include\_in\_gross” equals include\_in\_gross or item at “is\_group” equals 1).
  - Draw item from data, keep a combination only if ((item at “include\_in\_gross” equals include\_in\_gross or item at “is\_group” equals 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item at “include\_in\_gross” equals include\_in\_gross → item at “is\_group” equals 1.
- Set data\_to\_be\_removed from true.
- While data\_to\_be\_removed.
  - Set tuple(revenue, data\_to\_be\_removed) from remove\_parent\_with\_no\_child(revenue).
- Evaluate adjust\_account\_totals(revenue, period\_list).
- Return copy.deepcopy(revenue).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0254.json#L4258) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L993)

<a id="op-c7e6755414a583"></a>
### Remove parent with no child

`operation_enterprise_accounts_report_gross_and_net_profit_report_business_behavior_remove_parent_with_number_child`

**Inputs** data.

**Explicit results** tuple(data, data\_to\_be\_removed).

**Local steps**

- Set data\_to\_be\_removed from false.
- For each parent in list(data).
  - If (“is\_group” belongs to parent and parent.get(“is\_group”) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in “is\_group” belongs to parent → parent.get(“is\_group”) equals 1.
    - Set have\_child from false.
    - For each child in data.
      - If (“parent\_account” belongs to child and child.get(“parent\_account”) equals parent.get(“account”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in “parent\_account” belongs to child → child.get(“parent\_account”) equals parent.get(“account”).
        - Set have\_child from true.
        - Leave the innermost loop without its normal-exhaustion alternative.
    - If not have\_child.
      - Set data\_to\_be\_removed from true.
      - Evaluate data.remove(parent).
- Return tuple(data, data\_to\_be\_removed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0254.json#L4509) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L994)

<a id="op-43f719307b103f"></a>
### Adjust account totals

`operation_enterprise_accounts_report_gross_and_net_profit_report_business_behavior_adjust_account_totals`

**Inputs** data, period\_list.

**Local steps**

- Set totals from mapping().
- For each d in reversed(data).
  - If d.get(“is\_group”).
    - For each period in period\_list.
      - Set d at period.key from sum(generator of item at period.key for item drawn from data where item.get(“parent\_account”) equals d.get(“account”)).
        - Draw item from data, keep a combination only if (item.get(“parent\_account”) equals d.get(“account”)).
  - Otherwise.
    - Evaluate set\_total(d, d at “total”, data, totals).
  - Set d at “total” from totals at d at “account”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0254.json#L4850) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L989)

<a id="op-67435e36faa5b4"></a>
### Set total

`operation_enterprise_accounts_report_gross_and_net_profit_report_business_behavior_set_total`

**Inputs** node, value, complete\_list, totals.

**Explicit results** set\_total(next(generator of item for item drawn from complete\_list where item at “account” equals parent), value, complete\_list, totals).

**Local steps**

- If not totals.get(node at “account”).
  - Set totals at node at “account” from 0.
- Update totals at node at “account” using + value.
- Set parent from node at “parent\_account”.
- If parent differs from empty text.
  - Return set\_total(next(generator of item for item drawn from complete\_list where item at “account” equals parent), value, complete\_list, totals).
    - Draw item from complete\_list, keep a combination only if (item at “account” equals parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0254.json#L5188) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L995)

<a id="op-2d4520abaa96d8"></a>
### Get profit

`operation_enterprise_accounts_report_gross_and_net_profit_report_business_behavior_get_profit`

**Inputs** gross\_income, gross\_expense, period\_list, company, profit\_type, currency = no value, consolidated = false.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** profit\_loss.

**Local steps**

- Set profit\_loss from mapping(“account\_name” → ((“'” + translated profit\_type) + “'”), “account” → ((“'” + translated profit\_type) + “'”), “warn\_if\_negative” → true, “currency” → (currency or Platform.get\_cached\_value(“Company” ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Set has\_value from false.
- For each period in period\_list.
  - Set key from period when consolidated, otherwise period.key.
    - Value choice on consolidated — true gives period, false gives period.key.
  - Set gross\_income\_for\_period from flt(gross\_income at 0.get(key, 0)) when gross\_income, otherwise 0.
    - Value choice on gross\_income — true gives flt(gross\_income at 0.get(key, 0)), false gives 0.
  - Set gross\_expense\_for\_period from flt(gross\_expense at 0.get(key, 0)) when gross\_expense, otherwise 0.
    - Value choice on gross\_expense — true gives flt(gross\_expense at 0.get(key, 0)), false gives 0.
  - Set profit\_loss at key from (gross\_income\_for\_period − gross\_expense\_for\_period).
  - If profit\_loss at key.
    - Set has\_value from true.
    - If not profit\_loss.get(“total”).
      - Set profit\_loss at “total” from 0.
    - Update profit\_loss at “total” using + profit\_loss at key.
- If has\_value.
  - Return profit\_loss.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0254.json#L5485) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L992)
