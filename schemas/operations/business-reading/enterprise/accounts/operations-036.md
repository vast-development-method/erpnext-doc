# Accounting and settlement · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Dunning type

[Record definition](../../../../data/record-types/dunning_type.json)

<a id="op-2ac4370c172ec4"></a>
### Dunning Type.autoname

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_autoname`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set company\_abbr from Platform.get\_value(“Company”, self.company, “abbr”).
- Set self.name from formatted text {self.dunning\_type} - {company\_abbr}.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L5334) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L734)

<a id="op-898f9d293f3a7c"></a>
### Dunning Type.validate

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dunning\_letter\_text().
- Evaluate self.validate\_income\_account().
- Evaluate self.validate\_cost\_center().
- Evaluate self.set\_default\_dunning\_type().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dunning letter text](operations-036.md#op-3dddeda351a847), [validate income account](operations-036.md#op-c5aa7f73947eb4), [validate cost center](operations-036.md#op-b86b13c32487ea), [set default dunning type](operations-036.md#op-9a020f53964ebd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L5468) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L781) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L736)

<a id="op-3dddeda351a847"></a>
### Dunning Type.validate dunning letter text

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_validate_dunning_letter_text`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_languages().
- Evaluate self.validate\_is\_default\_language().
- Evaluate self.validate\_dunning\_letter\_text\_templates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate languages](operations-036.md#op-d10ea7ff7adf38), [validate is default language](operations-036.md#op-2de5bcf7c572a5), [validate dunning letter text templates](operations-036.md#op-ede0fd8af85270).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L5579) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L738)

<a id="op-c5aa7f73947eb4"></a>
### Dunning Type.validate income account

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_validate_income_account`

**Inputs** self.

**Record and data access** resolve a document from “Account” via get\_cached\_doc.

**State and service calls** msgprint with msg.

**Explicit results** no value.

**Local steps**

- If not self.income\_account.
  - Return no value.
- Set account from Platform.get\_cached\_doc(“Account”, self.income\_account).
- Set msg from list().
- If account.company differs from self.company.
  - Evaluate msg.append(translated “{0} doesn't belong to Company {1}. Please select an Income Account that belongs to Company {1}.”.format(Platform.bold(self.income\_account), Platform.bold(self.company))).
- If account.disabled.
  - Evaluate msg.append(translated “{0} is disabled. Please select a valid Income Account.”.format(Platform.bold(self.income\_account))).
- If account.root\_type differs from “Income”.
  - Evaluate msg.append(translated “{0} is not an Income Account. Please select a valid Income Account.”.format(Platform.bold(self.income\_account))).
- If account.is\_group.
  - Evaluate msg.append(translated “{0} is a group account. Please select a non-group Income Account.”.format(Platform.bold(self.income\_account))).
- If msg.
  - Evaluate Platform.msgprint(msg, title = translated “Income Account Validation Error”, as\_list = true, raise\_exception = Platform.ValidationError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Account”, self.income\_account).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L5670) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L740)

<a id="op-b86b13c32487ea"></a>
### Dunning Type.validate cost center

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_validate_cost_center`

**Inputs** self.

**Record and data access** resolve a document from “Cost Center” via get\_cached\_doc.

**State and service calls** msgprint with msg.

**Explicit results** no value.

**Local steps**

- If not self.cost\_center.
  - Return no value.
- Set cost\_center from Platform.get\_cached\_doc(“Cost Center”, self.cost\_center).
- Set msg from list().
- If cost\_center.company differs from self.company.
  - Evaluate msg.append(translated “{0} doesn't belong to Company {1}. Please select a Cost Center that belongs to Company {1}.”.format(Platform.bold(self.cost\_center), Platform.bold(self.company))).
- If cost\_center.disabled.
  - Evaluate msg.append(translated “{0} is disabled. Please select an enabled Cost Center.”.format(Platform.bold(self.cost\_center))).
- If cost\_center.is\_group.
  - Evaluate msg.append(translated “{0} is a group Cost Center. Please select a non-group Cost Center.”.format(Platform.bold(self.cost\_center))).
- If msg.
  - Evaluate Platform.msgprint(msg, title = translated “Cost Center Validation Error”, as\_list = true, raise\_exception = Platform.ValidationError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Cost Center”, self.cost\_center).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L6261) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L737)

<a id="op-d10ea7ff7adf38"></a>
### Dunning Type.validate languages

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_validate_languages`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Duplicate languages found on Dunning Letter Text. Keep only one of them.”.

**Local steps**

- Set languages from list of d.language for d drawn from self.dunning\_letter\_text.
  - Draw d from self.dunning\_letter\_text.
- If len(languages) equals len(set(languages)).
  - Return no value.
- Call the validation error handler Platform.throw(translated “Duplicate languages found on Dunning Letter Text. Keep only one of them.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L6755) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L742)

<a id="op-2de5bcf7c572a5"></a>
### Dunning Type.validate is default language

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_validate_is_default_language`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} languages are marked as default languages. Please select only one of them.”.format(comma\_and(is\_default\_language\_list, add\_quotes = true)).

**Local steps**

- Set is\_default\_language\_list from list of d.language for d drawn from self.dunning\_letter\_text where d.is\_default\_language equals 1.
  - Draw d from self.dunning\_letter\_text, keep a combination only if (d.is\_default\_language equals 1).
- <a id="op-2de5bcf7c572a5-guard-6"></a>If len(is\_default\_language\_list) ≤ 1.
  - Return no value.
- Call the validation error handler Platform.throw(translated “{0} languages are marked as default languages. Please select only one of them.”.format(comma\_and(is\_default\_language\_list, add\_quotes = true))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(is\_default\_language\_list) ≤ 1, length of is\_default\_language\_list = 1 selects the branch that returns no value. With length of is\_default\_language\_list = 2, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2de5bcf7c572a5-guard-6)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L6928) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L786) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L741)

<a id="op-ede0fd8af85270"></a>
### Dunning Type.validate dunning letter text templates

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_validate_dunning_letter_text_templates`

**Inputs** self.

**Local steps**

- For each d in self.dunning\_letter\_text.
  - If d.body\_text.
    - Evaluate validate\_template(d.body\_text, restrict\_globals = true).
  - If d.closing\_text.
    - Evaluate validate\_template(d.closing\_text, restrict\_globals = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0041.json#L7140) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L739)

<a id="op-9a020f53964ebd"></a>
### Dunning Type.set default dunning type

`operation_enterprise_accounts_record_definitions_dunning_type_business_behavior_dunning_type_set_default_dunning_type`

**Inputs** self.

**State and service calls** request set\_value on “Dunning Type”.

**Explicit results** no value.

**Local steps**

- If self.is\_default differs from 1.
  - Return no value.
- Evaluate Platform.db.set\_value(“Dunning Type”, mapping(“company” → self.company, “is\_default” → 1, “name” → list(“!=”, self.name)), “is\_default”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L780) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L735)

## Record · Exchange rate revaluation

[Record definition](../../../../data/record-types/exchange_rate_revaluation.json)

<a id="op-dab6e7037e19c1"></a>
### Exchange Rate Revaluation.validate

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_rounding\_loss\_allowance().
- Evaluate self.set\_total\_gain\_loss().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate rounding loss allowance](operations-036.md#op-e52c4dddbb06cd), [set total gain loss](operations-036.md#op-d3e00e5cf01281).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L4277) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L825) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L780)

<a id="op-e52c4dddbb06cd"></a>
### Exchange Rate Revaluation.validate rounding loss allowance

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_validate_rounding_loss_allowance`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Rounding Loss Allowance should be between 0 and 1”.

**Local steps**

- If (self.rounding\_loss\_allowance &lt; 0 or self.rounding\_loss\_allowance ≥ 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rounding\_loss\_allowance &lt; 0 → self.rounding\_loss\_allowance ≥ 1.
  - Call the validation error handler Platform.throw(translated “Rounding Loss Allowance should be between 0 and 1”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L4348) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L827) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L782)

<a id="op-d3e00e5cf01281"></a>
### Exchange Rate Revaluation.set total gain loss

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_set_total_gain_loss`

**Inputs** self.

**Local steps**

- Set total\_gain\_loss from 0.
- Set gain\_loss\_booked from 0.
- Set gain\_loss\_unbooked from 0.
- For each d in self.accounts.
  - If not d.zero\_balance.
    - Set d.gain\_loss from (flt(d.new\_balance\_in\_base\_currency, d.precision(“new\_balance\_in\_base\_currency”)) − flt(d.balance\_in\_base\_currency, d.precision(“balance\_in\_base\_currency”))).
  - If d.zero\_balance.
    - Update gain\_loss\_booked using + flt(d.gain\_loss, d.precision(“gain\_loss”)).
  - Otherwise.
    - Update gain\_loss\_unbooked using + flt(d.gain\_loss, d.precision(“gain\_loss”)).
  - Update total\_gain\_loss using + flt(d.gain\_loss, d.precision(“gain\_loss”)).
- Set self.gain\_loss\_booked from gain\_loss\_booked.
- Set self.gain\_loss\_unbooked from gain\_loss\_unbooked.
- Set self.total\_gain\_loss from flt(total\_gain\_loss, self.precision(“total\_gain\_loss”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L4470) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L823) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L778)

<a id="op-c712053f62ace8"></a>
### Exchange Rate Revaluation.validate mandatory

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_validate_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select Company and Posting Date to getting entries”.

**Local steps**

- If not (self.company and self.posting\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → self.posting\_date.
  - Call the validation error handler Platform.throw(translated “Please select Company and Posting Date to getting entries”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L826) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L781)

<a id="op-90e7b606ff7fec"></a>
### Exchange Rate Revaluation.before submit

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.remove\_accounts\_without\_gain\_loss().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove accounts without gain loss](operations-036.md#op-bf7ab3433bc62e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L5039) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L810) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L765)

<a id="op-bf7ab3433bc62e"></a>
### Exchange Rate Revaluation.remove accounts without gain loss

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_remove_accounts_without_gain_loss`

**Inputs** self.

**State and service calls** msgprint with translated “Removing rows without exchange gain or loss”.

**Explicit failure paths** validation helper — translated “At least one account with exchange gain or loss is required”.

**Local steps**

- Set self.accounts from list of account for account drawn from self.accounts where account.gain\_loss.
  - Draw account from self.accounts, keep a combination only if (account.gain\_loss).
- If not self.accounts.
  - Call the validation error handler Platform.throw(translated “At least one account with exchange gain or loss is required”).
- Evaluate Platform.msgprint(translated “Removing rows without exchange gain or loss”, alert = true, indicator = “yellow”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L5090) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L822) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L777)

<a id="op-a8e6b8e5057bd3"></a>
### Exchange Rate Revaluation.on cancel

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_on_cancel`

**Inputs** self.

**Local steps**

- Set self.ignore\_linked\_doctypes from list(“GL Entry”, “Payment Ledger Entry”).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L5285) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L821) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L776)

<a id="op-c059ab01cd811f"></a>
### Exchange Rate Revaluation.check journal and reversal

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_check_journal_and_reversal`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“journals\_posted” → journals\_posted, “reversals\_posted” → reversals\_posted).

**Local steps**

- Set exchange\_gain\_loss\_account from self.get\_for\_unrealized\_gain\_loss\_account().
- Set journals\_posted from false.
- Set reversals\_posted from false.
- Set je from qb.DocType(“Journal Entry”).
- Set jea from qb.DocType(“Journal Entry Account”).
- Set journals from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nes ….
- If journals.
  - Set gle from qb.DocType(“GL Entry”).
  - Set total\_amt from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“total\_amount”)).where((((nested operand in the contract equals nested operand in the contract bitwi ….run().
  - If (total\_amt and total\_amt at 0 at 0 equals self.total\_gain\_loss).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_amt → total\_amt at 0 at 0 equals self.total\_gain\_loss.
    - Set journals\_posted from true.
  - Otherwise.
    - Set journals\_posted from false.
- Set reverse\_journals from nested operand in the contract(nested operand in the contract).select(je.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equal ….
- If reverse\_journals.
  - Set reversals\_posted from true.
- Otherwise.
  - Set reversals\_posted from false.
- Return mapping(“journals\_posted” → journals\_posted, “reversals\_posted” → reversals\_posted).

**Methods declared on this owner** [get for unrealized gain loss account](operations-036.md#op-ef196a5da326b4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L5351) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L767)

<a id="op-71f99df7f3307b"></a>
### Exchange Rate Revaluation.fetch and calculate accounts data

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_fetch_and_calculate_accounts_data`

**Inputs** self.

**Local steps**

- Set accounts from self.get\_accounts\_data().
- If accounts.
  - For each acc in accounts.
    - If acc.get(“gain\_loss”).
      - Evaluate self.append(“accounts”, acc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get accounts data](operations-036.md#op-0c6b33ec23c589).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L6431) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L768)

<a id="op-0c6b33ec23c589"></a>
### Exchange Rate Revaluation.get accounts data

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_get_accounts_data`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** accounts\_with\_new\_balance.

**Local steps**

- Evaluate self.validate\_mandatory().
- Set account\_details from self.get\_account\_balance\_from\_gle(company = self.company, posting\_date = self.posting\_date, account = no value, party\_type = no value, …).
- Set accounts\_with\_new\_balance from self.calculate\_new\_account\_balance(self.company, self.posting\_date, account\_details).
- If not accounts\_with\_new\_balance.
  - Evaluate self.throw\_invalid\_response\_message(account\_details).
- Return accounts\_with\_new\_balance.

**Methods declared on this owner** [validate mandatory](operations-036.md#op-c712053f62ace8), [get account balance from gle](operations-036.md#op-a99ca4177a8c11), [calculate new account balance](operations-036.md#op-58e26091b37836), [throw invalid response message](operations-036.md#op-716ab5390df3a6).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0042.json#L6577) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L770)

<a id="op-a99ca4177a8c11"></a>
### Exchange Rate Revaluation.get account balance from gle

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_get_account_balance_from_general_ledger_entry`

**Inputs** company, posting\_date, account, party\_type, party, rounding\_loss\_allowance.

**Wrappers, in declaration order** staticmethod.

**Explicit results** account\_details.

**Local steps**

- Set account\_details from list().
- If (company and posting\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → posting\_date.
  - Set company\_currency from Enterprise.get\_company\_currency(company).
  - Set acc from qb.DocType(“Account”).
  - If account.
    - Set accounts from list(account).
  - Otherwise.
    - Set res from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract differs from nes ….
    - Set accounts from list of x at 0 for x drawn from res.
      - Draw x from res.
  - If accounts.
    - Set having\_clause from (qb.Field(“balance”) differs from qb.Field(“balance\_in\_account\_currency”) bitwise and (qb.Field(“balance\_in\_account\_currency”) differs from 0 bitwise or qb.Field(“balance”) differs from 0)).
    - Set gle from qb.DocType(“GL Entry”).
    - Set conditions from list().
    - Evaluate conditions.append(gle.account.isin(accounts)).
    - Evaluate conditions.append(gle.posting\_date.lte(posting\_date)).
    - Evaluate conditions.append(gle.is\_cancelled equals 0).
    - If party\_type.
      - Evaluate conditions.append(gle.party\_type equals party\_type).
    - If party.
      - Evaluate conditions.append(gle.party equals party).
    - Set account\_details from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).having(having\_clause).orderby(gle.account).run(as\_dict = true).
    - Set currency\_precision from get\_currency\_precision().
    - Set rounding\_loss\_allowance from float(rounding\_loss\_allowance).
    - For each acc in account\_details.
      - Set acc.balance\_in\_account\_currency from flt(acc.balance\_in\_account\_currency, currency\_precision).
      - If abs(acc.balance\_in\_account\_currency) ≤ rounding\_loss\_allowance.
        - Set acc.balance\_in\_account\_currency from 0.
      - Set acc.balance from flt(acc.balance, currency\_precision).
      - If abs(acc.balance) ≤ rounding\_loss\_allowance.
        - Set acc.balance from 0.
      - Set acc.zero\_balance from true when (acc.balance equals 0 or acc.balance\_in\_account\_currency equals 0), otherwise false.
        - Value choice on (acc.balance equals 0 or acc.balance\_in\_account\_currency equals 0) — true gives true, false gives false.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in acc.balance equals 0 → acc.balance\_in\_account\_currency equals 0.
- Return account\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L769)

<a id="op-58e26091b37836"></a>
### Exchange Rate Revaluation.calculate new account balance

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_calculate_new_account_balance`

**Inputs** company, posting\_date, account\_details.

**Wrappers, in declaration order** staticmethod.

**Explicit results** accounts.

**Local steps**

- Set accounts from list().
- Set company\_currency from Enterprise.get\_company\_currency(company).
- Set precision from get\_field\_precision(Platform.get\_meta(“Exchange Rate Revaluation Account”).get\_field(“new\_balance\_in\_base\_currency”), currency = company\_currency).
- If account\_details.
  - For each d in list of x for x drawn from account\_details where not x.zero\_balance.
    - Draw x from account\_details, keep a combination only if (not x.zero\_balance).
    - Set current\_exchange\_rate from (d.balance ÷ d.balance\_in\_account\_currency) when d.balance\_in\_account\_currency, otherwise 0.
      - Value choice on d.balance\_in\_account\_currency — true gives (d.balance ÷ d.balance\_in\_account\_currency), false gives 0.
    - Set new\_exchange\_rate from get\_exchange\_rate(d.account\_currency, company\_currency, posting\_date).
    - Set new\_balance\_in\_base\_currency from flt((d.balance\_in\_account\_currency × new\_exchange\_rate)).
    - Set gain\_loss from (flt(new\_balance\_in\_base\_currency, precision) − flt(d.balance, precision)).
    - Evaluate accounts.append(mapping(“account” → d.account, “party\_type” → d.party\_type, “party” → d.party, “account\_currency” → d.account\_currency, …)).
  - For each d in list of x for x drawn from account\_details where x.zero\_balance.
    - Draw x from account\_details, keep a combination only if (x.zero\_balance).
    - If d.balance differs from 0.
      - Set current\_exchange\_rate, new\_exchange\_rate from 0.
      - Set new\_balance\_in\_account\_currency from 0.
      - Set new\_balance\_in\_base\_currency from 0.
      - Set gain\_loss from (flt(new\_balance\_in\_base\_currency, precision) − flt(d.balance, precision)).
    - Otherwise.
      - Set new\_exchange\_rate from 0.
      - Set new\_balance\_in\_base\_currency from 0.
      - Set new\_balance\_in\_account\_currency from 0.
      - Set current\_exchange\_rate from (calculate\_exchange\_rate\_using\_last\_gle(company, d.account, d.party\_type, d.party) or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in calculate\_exchange\_rate\_using\_last\_gle(company, d.account, d.party\_type, d.party) → 0.0.
      - Set gain\_loss from (new\_balance\_in\_account\_currency − (current\_exchange\_rate × d.balance\_in\_account\_currency)).
    - Evaluate accounts.append(mapping(“account” → d.account, “party\_type” → d.party\_type, “party” → d.party, “account\_currency” → d.account\_currency, …)).
- Return accounts.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0043.json#L1644) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L766)

<a id="op-716ab5390df3a6"></a>
### Exchange Rate Revaluation.throw invalid response message

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_throw_invalid_response_message`

**Inputs** self, account\_details.

**State and service calls** msgprint with message.

**Local steps**

- If account\_details.
  - Set message from translated “No outstanding invoices require exchange rate revaluation”.
- Otherwise.
  - Set message from translated “No outstanding invoices found”.
- Evaluate Platform.msgprint(message).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0043.json#L2848) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L824) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L779)

<a id="op-ef196a5da326b4"></a>
### Exchange Rate Revaluation.get for unrealized gain loss account

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_get_for_unrealized_gain_loss_account`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** unrealized\_exchange\_gain\_loss\_account.

**Explicit failure paths** validation helper — translated “Please set Unrealized Exchange Gain/Loss Account in Company {0}”.format(self.company).

**Local steps**

- Set unrealized\_exchange\_gain\_loss\_account from Platform.get\_cached\_value(“Company”, self.company, “unrealized\_exchange\_gain\_loss\_account”).
- If not unrealized\_exchange\_gain\_loss\_account.
  - Call the validation error handler Platform.throw(translated “Please set Unrealized Exchange Gain/Loss Account in Company {0}”.format(self.company)).
- Return unrealized\_exchange\_gain\_loss\_account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “unrealized\_exchange\_gain\_loss\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0043.json#L2975) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L816) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L771)

<a id="op-f75dc19b4e99ed"></a>
### Exchange Rate Revaluation.make jv entries

`operation_enterprise_accounts_record_definitions_exchange_rate_revaluation_business_behavior_exchange_rate_revaluation_make_journal_voucher_entries`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with formatted text Zero Balance Journal: {get\_link\_to\_form(“Journal Entry”, zero\_balance\_jv.name)} · msgprint with formatted text Revaluation Journal: {get\_link\_to\_form(“Journal Entry”, revaluation\_jv.name)}.

**Explicit results** mapping(“revaluation\_jv” → revaluation\_jv.name when revaluation\_jv, otherwise no value, “zero\_balance\_jv” → zero\_balance\_jv.name when zero\_balance\_jv, otherwise no value).

**Local steps**

- Evaluate Platform.has\_permission(“Journal Entry”, “write”, throw = true).
- Set zero\_balance\_jv from self.make\_jv\_for\_zero\_balance().
- If zero\_balance\_jv.
  - Evaluate Platform.msgprint(formatted text Zero Balance Journal: {get\_link\_to\_form(“Journal Entry”, zero\_balance\_jv.name)}).
- Set revaluation\_jv from self.make\_jv\_for\_revaluation().
- If revaluation\_jv.
  - Evaluate Platform.msgprint(formatted text Revaluation Journal: {get\_link\_to\_form(“Journal Entry”, revaluation\_jv.name)}).
- Return mapping(“revaluation\_jv” → revaluation\_jv.name when revaluation\_jv, otherwise no value, “zero\_balance\_jv” → zero\_balance\_jv.name when zero\_balance\_jv, otherwise no value).
  - Value choice on revaluation\_jv — true gives revaluation\_jv.name, false gives no value.
  - Value choice on zero\_balance\_jv — true gives zero\_balance\_jv.name, false gives no value.

**Methods declared on this owner** [make jv for zero balance](operations-037.md#op-e6b8365553bb04), [make jv for revaluation](operations-037.md#op-2fe764819750c5).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Journal Entry”, “write”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L772)
