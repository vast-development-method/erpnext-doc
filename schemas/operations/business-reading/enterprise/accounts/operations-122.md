# Accounting and settlement · operations 122

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-6e30d43ef49fd3"></a>
### Create err and its journals

`operation_enterprise_accounts_utils_business_behavior_create_error_and_its_journals`

**Inputs** company.

**Declared result** no value.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**State and service calls** request new\_doc for “Exchange Rate Revaluation” · call submit on err.save() · call save on err · call submit on Platform.get\_doc(“Journal Entry”, jv).

**Local steps**

- Set err from Platform.new\_doc(“Exchange Rate Revaluation”).
- Set err.company from company.name.
- Set err.posting\_date from nowdate().
- Set err.rounding\_loss\_allowance from 0.0.
- Evaluate err.fetch\_and\_calculate\_accounts\_data().
- If err.accounts.
  - Evaluate err.save().submit().
  - Set response from err.make\_jv\_entries().
  - If company.submit\_err\_jv.
    - Set jv from response.get(“revaluation\_jv”, no value).
    - Evaluate (jv and Platform.get\_doc(“Journal Entry”, jv).submit()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in jv → Platform.get\_doc(“Journal Entry”, jv).submit().
    - Set jv from response.get(“zero\_balance\_jv”, no value).
    - Evaluate (jv and Platform.get\_doc(“Journal Entry”, jv).submit()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in jv → Platform.get\_doc(“Journal Entry”, jv).submit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L3818) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L190)

<a id="op-874f4062be430a"></a>
### Auto create exchange rate revaluation for

`operation_enterprise_accounts_utils_business_behavior_auto_create_exchange_rate_revaluation_for`

**Inputs** frequency.

**Declared result** no value.

**Record and data access** read “Company” via get\_all.

**State and service calls** enqueue with “Enterprise.accounts.utils.create\_err\_and\_its\_journals”.

**Local steps**

- Set companies from Platform.db.get\_all(“Company”, filters = mapping(“auto\_exchange\_rate\_revaluation” → 1, “auto\_err\_frequency” → frequency), fields = list(“name”, “submit\_err\_jv”)).
- If companies.
  - For each company in companies.
    - Evaluate Platform.enqueue(“Enterprise.accounts.utils.create\_err\_and\_its\_journals”, company = company, queue = “long”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Enterprise.accounts.utils.create\_err\_and\_its\_journals”, company = company, queue = “long”).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L4222) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L179)

<a id="op-e10d4ad6de8a26"></a>
### Auto create exchange rate revaluation daily

`operation_enterprise_accounts_utils_business_behavior_auto_create_exchange_rate_revaluation_daily`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate \_auto\_create\_exchange\_rate\_revaluation\_for(“Daily”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L4479) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L178)

<a id="op-4255465fa7aaa0"></a>
### Auto create exchange rate revaluation weekly

`operation_enterprise_accounts_utils_business_behavior_auto_create_exchange_rate_revaluation_weekly`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate \_auto\_create\_exchange\_rate\_revaluation\_for(“Weekly”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L4523) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L181)

<a id="op-4b364492ba5ff9"></a>
### Auto create exchange rate revaluation monthly

`operation_enterprise_accounts_utils_business_behavior_auto_create_exchange_rate_revaluation_monthly`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate \_auto\_create\_exchange\_rate\_revaluation\_for(“Monthly”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L4567) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L180)

<a id="op-6499cceafee0d9"></a>
### Get payment ledger entries

`operation_enterprise_accounts_utils_business_behavior_get_payment_ledger_entries`

**Inputs** gl\_entries, cancel = 0.

**Explicit results** ple\_map.

**Local steps**

- Set ple\_map from list().
- If gl\_entries.
  - Set ple from no value.
  - Set account from qb.DocType(“Account”).
  - Set companies from list(set(list of x.company for x drawn from gl\_entries)).
    - Draw x from gl\_entries.
  - Set accounts\_with\_types from nested operand in the contract(nested operand in the contract).select(account.name, account.account\_type).where((nested operand in the contract.account\_type.isin(list(“Receivable”, “Payable”)) bitwise and  ….
  - Set receivable\_or\_payable\_accounts from list of y.name for y drawn from accounts\_with\_types.
    - Draw y from accounts\_with\_types.
  - Bind local operation get\_account\_type for subsequent calls.
  - Set dr\_or\_cr from 0.
  - Set account\_type from no value.
  - For each gle in gl\_entries.
    - If gle.account belongs to receivable\_or\_payable\_accounts.
      - Set account\_type from get\_account\_type(gle.account).
      - If account\_type equals “Receivable”.
        - Set dr\_or\_cr from (gle.debit − gle.credit).
        - Set dr\_or\_cr\_account\_currency from (gle.debit\_in\_account\_currency − gle.credit\_in\_account\_currency).
      - Otherwise.
        - If account\_type equals “Payable”.
          - Set dr\_or\_cr from (gle.credit − gle.debit).
          - Set dr\_or\_cr\_account\_currency from (gle.credit\_in\_account\_currency − gle.debit\_in\_account\_currency).
      - If cancel.
        - Update dr\_or\_cr using × negative 1.
        - Update dr\_or\_cr\_account\_currency using × negative 1.
      - Set against\_voucher\_type from gle.against\_voucher\_type when gle.against\_voucher\_type, otherwise gle.voucher\_type.
        - Value choice on gle.against\_voucher\_type — true gives gle.against\_voucher\_type, false gives gle.voucher\_type.
      - Set against\_voucher\_no from gle.against\_voucher when gle.against\_voucher, otherwise gle.voucher\_no.
        - Value choice on gle.against\_voucher — true gives gle.against\_voucher, false gives gle.voucher\_no.
      - Set ple from Platform.\_dict(doctype = “Payment Ledger Entry”, posting\_date = gle.posting\_date, company = gle.company, account\_type = account\_type, …).
      - Set dimensions\_and\_defaults from get\_dimensions().
      - If dimensions\_and\_defaults.
        - For each dimension in dimensions\_and\_defaults at 0.
          - Set ple at dimension.fieldname from gle.get(dimension.fieldname).
      - If gle.advance\_voucher\_no.
        - Set tuple(base\_amount, exchange\_rate) from tuple(dr\_or\_cr, gle.transaction\_exchange\_rate) when gle.advance\_voucher\_type equals “Employee Advance”, otherwise tuple(no value, no value).
          - Value choice on gle.advance\_voucher\_type equals “Employee Advance” — true gives tuple(dr\_or\_cr, gle.transaction\_exchange\_rate), false gives tuple(no value, no value).
        - Set adv from get\_advance\_ledger\_entry(gle, against\_voucher\_type, against\_voucher\_no, dr\_or\_cr\_account\_currency, …).
        - Evaluate ple\_map.append(adv).
      - Evaluate ple\_map.append(ple).
- Return ple\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L4611) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L226)

<a id="op-c880f20a8fe581"></a>
### Get payment ledger entries.get account type

`operation_enterprise_accounts_utils_business_behavior_get_payment_ledger_entries_get_account_type`

**Inputs** account.

**Explicit results** entry.account\_type.

**Local steps**

- For each entry in accounts\_with\_types.
  - If entry.name equals account.
    - Return entry.account\_type.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0994.json#L4701) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L227)

<a id="op-d461bfa1a3101f"></a>
### Get advance ledger entry

`operation_enterprise_accounts_utils_business_behavior_get_advance_ledger_entry`

**Inputs** gle, against\_voucher\_type, against\_voucher\_no, amount, cancel, base\_amount = no value, exchange\_rate = no value.

**Explicit results** aple.

**Local steps**

- Set event from “Submit” when (against\_voucher\_type equals gle.voucher\_type and against\_voucher\_no equals gle.voucher\_no), otherwise “Adjustment”.
  - Value choice on (against\_voucher\_type equals gle.voucher\_type and against\_voucher\_no equals gle.voucher\_no) — true gives “Submit”, false gives “Adjustment”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in against\_voucher\_type equals gle.voucher\_type → against\_voucher\_no equals gle.voucher\_no.
- Set aple from Platform.\_dict(doctype = “Advance Payment Ledger Entry”, company = gle.company, voucher\_type = gle.voucher\_type, voucher\_no = gle.voucher\_no, …).
- If base\_amount is distinct from no value.
  - Set aple.base\_amount from base\_amount.
- If exchange\_rate is distinct from no value.
  - Set aple.exchange\_rate from exchange\_rate.
- Return aple.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0304.json#L5979) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L204)

<a id="op-8392a772d59cad"></a>
### Create payment ledger entry

`operation_enterprise_accounts_utils_business_behavior_create_payment_ledger_entry`

**Inputs** gl\_entries, cancel = 0, adv\_adj = 0, update\_outstanding = “Yes”, from\_repost = 0, partial\_cancel = false.

**Record and data access** resolve a document from entry via get\_doc.

**State and service calls** call submit on ple.

**Local steps**

- If gl\_entries.
  - Set ple\_map from get\_payment\_ledger\_entries(gl\_entries, cancel = cancel).
  - For each entry in ple\_map.
    - Set ple from Platform.get\_doc(entry).
    - If cancel.
      - If not is\_immutable\_ledger\_enabled().
        - Evaluate delink\_original\_entry(ple, partial\_cancel = partial\_cancel).
      - Otherwise.
        - Set ple.delinked from 0.
        - Set ple.posting\_date from (Platform.form\_dict.get(“posting\_date”) or getdate()).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.get(“posting\_date”) → getdate().
    - Set ple.flags.ignore\_permissions from 1.
    - Set ple.flags.adv\_adj from adv\_adj.
    - Set ple.flags.from\_repost from from\_repost.
    - Set ple.flags.update\_outstanding from update\_outstanding.
    - Evaluate ple.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L193)

<a id="op-c4c7e2b7322460"></a>
### Update voucher outstanding

`operation_enterprise_accounts_utils_business_behavior_update_voucher_outstanding`

**Inputs** voucher\_type, voucher\_no, account, party\_type, party.

**State and service calls** request set\_value on voucher\_type.

**Explicit results** no value.

**Local steps**

- Bind dependencies update\_linked\_dunnings.
- If (not voucher\_type or not voucher\_no).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not voucher\_type → not voucher\_no.
  - Return no value.
- If voucher\_type belongs to get\_advance\_payment\_doctypes().
  - Set ref\_doc from Platform.get\_lazy\_doc(voucher\_type, voucher\_no).
  - Evaluate ref\_doc.set\_total\_advance\_paid().
  - Return no value.
- If not (voucher\_type belongs to OUTSTANDING\_DOCTYPES and party\_type and party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type belongs to OUTSTANDING\_DOCTYPES → party\_type → party.
  - Return no value.
- Set ple from Platform.qb.DocType(“Payment Ledger Entry”).
- Set vouchers from list(Platform.\_dict(mapping(“voucher\_type” → voucher\_type, “voucher\_no” → voucher\_no))).
- Set common\_filter from list().
- Evaluate common\_filter.append(ple.party\_type equals party\_type).
- Evaluate common\_filter.append(ple.party equals party).
- If account.
  - Evaluate common\_filter.append(ple.account equals account).
- Set ple\_query from QueryPaymentLedger().
- Set voucher\_outstanding from ple\_query.get\_voucher\_outstandings(vouchers, common\_filter = common\_filter).
- If not voucher\_outstanding.
  - Return no value.
- Set outstanding from voucher\_outstanding at 0.
- Set ref\_doc from Platform.get\_lazy\_doc(voucher\_type, voucher\_no).
- Set previous\_outstanding\_amount from ref\_doc.outstanding\_amount.
- Set outstanding\_amount from flt(outstanding at “outstanding\_in\_account\_currency”, ref\_doc.precision(“outstanding\_amount”)).
- Set ref\_doc.outstanding\_amount from outstanding\_amount.
- Evaluate Platform.db.set\_value(voucher\_type, voucher\_no, “outstanding\_amount”, outstanding\_amount).
- Evaluate update\_linked\_dunnings(ref\_doc, previous\_outstanding\_amount).
- Evaluate ref\_doc.set\_status(update = true).
- Evaluate ref\_doc.notify\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0305.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L255)

<a id="op-7c323904092874"></a>
### Delink original entry

`operation_enterprise_accounts_utils_business_behavior_delink_original_entry`

**Inputs** pl\_entry, partial\_cancel = false.

**Explicit results** no value.

**Local steps**

- If not pl\_entry.
  - Return no value.
- If pl\_entry.doctype equals “Advance Payment Ledger Entry”.
  - Set adv from qb.DocType(“Advance Payment Ledger Entry”).
  - Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.against\_voucher\_no equals nested operand in the contract.against\_voucher\_no).where(adv.event equals pl\_en …().
- Otherwise.
  - Set ple from qb.DocType(“Payment Ledger Entry”).
  - Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).set(ple.modified\_by, nested operand in the contract.session.user).set(ple.delinked, true).where(((((((nested o ….
  - If partial\_cancel.
    - Set query from query.where(ple.voucher\_detail\_no equals pl\_entry.voucher\_detail\_no).
  - Evaluate query.run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L199)

<a id="op-dbac0ec4989cea"></a>
### Query Payment Ledger.initialize

`operation_enterprise_accounts_utils_business_behavior_query_payment_ledger_initialize`

**Inputs** self.

**Local steps**

- Set self.ple from qb.DocType(“Payment Ledger Entry”).
- Set self.voucher\_outstandings from list().
- Set self.vouchers from list().
- Set self.common\_filter from list().
- Set self.voucher\_posting\_date from list().
- Set self.min\_outstanding from no value.
- Set self.max\_outstanding from no value.
- Set self.limit, self.voucher\_no from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0305.json#L1757) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L236)

<a id="op-dfd5b0921d994f"></a>
### Query Payment Ledger.reset

`operation_enterprise_accounts_utils_business_behavior_query_payment_ledger_reset`

**Inputs** self.

**Local steps**

- Evaluate self.vouchers.clear().
- Evaluate self.common\_filter.clear().
- Set self.min\_outstanding, self.max\_outstanding, self.limit from no value.
- Evaluate self.voucher\_outstandings.clear().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0305.json#L1950) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L238)

<a id="op-46bd944c500cb2"></a>
### Query Payment Ledger.query for outstanding

`operation_enterprise_accounts_utils_business_behavior_query_payment_ledger_query_for_outstanding`

**Inputs** self.

**Local steps**

- Set ple from self.ple.
- Set filter\_on\_voucher\_no from list().
- Set filter\_on\_against\_voucher\_no from list().
- If self.vouchers.
  - Set voucher\_types from set(list of x.voucher\_type for x drawn from self.vouchers).
    - Draw x from self.vouchers.
  - Set voucher\_nos from set(list of x.voucher\_no for x drawn from self.vouchers).
    - Draw x from self.vouchers.
  - Evaluate filter\_on\_voucher\_no.append(ple.voucher\_type.isin(voucher\_types)).
  - Evaluate filter\_on\_voucher\_no.append(ple.voucher\_no.isin(voucher\_nos)).
  - Evaluate filter\_on\_against\_voucher\_no.append(ple.against\_voucher\_type.isin(voucher\_types)).
  - Evaluate filter\_on\_against\_voucher\_no.append(ple.against\_voucher\_no.isin(voucher\_nos)).
- If self.voucher\_no.
  - Evaluate filter\_on\_voucher\_no.append(ple.voucher\_no.like(formatted text %{self.voucher\_no}%)).
  - Evaluate filter\_on\_against\_voucher\_no.append(ple.against\_voucher\_no.like(formatted text %{self.voucher\_no}%)).
- Set filter\_on\_outstanding\_amount from list().
- If self.min\_outstanding.
  - If self.min\_outstanding &gt; 0.
    - Evaluate filter\_on\_outstanding\_amount.append(Table(“outstanding”).amount\_in\_account\_currency ≥ self.min\_outstanding).
  - Otherwise.
    - Evaluate filter\_on\_outstanding\_amount.append(Table(“outstanding”).amount\_in\_account\_currency ≤ self.min\_outstanding).
- If self.max\_outstanding.
  - If self.max\_outstanding &gt; 0.
    - Evaluate filter\_on\_outstanding\_amount.append(Table(“outstanding”).amount\_in\_account\_currency ≤ self.max\_outstanding).
  - Otherwise.
    - Evaluate filter\_on\_outstanding\_amount.append(Table(“outstanding”).amount\_in\_account\_currency ≥ self.max\_outstanding).
- If (self.limit and self.get\_invoices).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.limit → self.get\_invoices.
  - Set outstanding\_vouchers from nested operand in the contract(nested operand in the contract, nested operand in the contract).having(nested operand in the contract(nested operand in the contract) &gt; 0).limit(self.limit).run().
  - If outstanding\_vouchers.
    - Evaluate filter\_on\_voucher\_no.append(ple.voucher\_no.isin(list of x at 0 for x drawn from outstanding\_vouchers)).
      - Draw x from outstanding\_vouchers.
    - Evaluate filter\_on\_against\_voucher\_no.append(ple.against\_voucher\_no.isin(list of x at 0 for x drawn from outstanding\_vouchers)).
      - Draw x from outstanding\_vouchers.
- Set query\_voucher\_amount from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.all(nested operand in the contract.dimensions\_filter)).where(Criterion.all(self.voucher\_posting\_date)).gr ….
- Set query\_voucher\_outstanding from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.all(filter\_on\_against\_voucher\_no)).where(Criterion.all(self.common\_filter)).groupby(ple.against\_voucher\_t ….
- Set self.cte\_query\_voucher\_amount\_and\_outstanding from nested operand in the contract(nested operand in the contract).on(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested opera ….
- If self.get\_invoices.
  - Set self.cte\_query\_voucher\_amount\_and\_outstanding from self.cte\_query\_voucher\_amount\_and\_outstanding.having(qb.Field(“outstanding\_in\_account\_currency”) &gt; 0).
- Otherwise.
  - If self.get\_payments.
    - Set self.cte\_query\_voucher\_amount\_and\_outstanding from self.cte\_query\_voucher\_amount\_and\_outstanding.having(qb.Field(“outstanding\_in\_account\_currency”) &lt; 0).
- If self.limit.
  - Set self.cte\_query\_voucher\_amount\_and\_outstanding from self.cte\_query\_voucher\_amount\_and\_outstanding.limit(self.limit).
- Set self.voucher\_outstandings from self.cte\_query\_voucher\_amount\_and\_outstanding.run(as\_dict = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L237)

<a id="op-9ef33f2397231d"></a>
### Query Payment Ledger.get voucher outstandings

`operation_enterprise_accounts_utils_business_behavior_query_payment_ledger_get_voucher_outstandings`

**Inputs** self, vouchers = no value, common\_filter = no value, posting\_date = no value, min\_outstanding = no value, max\_outstanding = no value, get\_payments = false, get\_invoices = false, accounting\_dimensions = no value, limit = no value, voucher\_no = no value.

**Explicit results** self.voucher\_outstandings.

**Local steps**

- Evaluate self.reset().
- Set self.vouchers from vouchers.
- Set self.common\_filter from (common\_filter or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in common\_filter → list().
- Set self.dimensions\_filter from (accounting\_dimensions or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in accounting\_dimensions → list().
- Set self.voucher\_posting\_date from (posting\_date or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in posting\_date → list().
- Set self.min\_outstanding from min\_outstanding.
- Set self.max\_outstanding from max\_outstanding.
- Set self.get\_payments from get\_payments.
- Set self.get\_invoices from get\_invoices.
- Set self.limit from limit.
- Set self.voucher\_no from voucher\_no.
- Evaluate self.query\_for\_outstanding().
- Return self.voucher\_outstandings.

**Methods declared on this owner** [reset](operations-122.md#op-dfd5b0921d994f), [query for outstanding](operations-122.md#op-46bd944c500cb2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L235)

<a id="op-79fa1b36c4a490"></a>
### Create gain loss journal

`operation_enterprise_accounts_utils_business_behavior_create_gain_loss_journal`

**Inputs** company, posting\_date, party\_type, party, party\_account, gain\_loss\_account, exc\_gain\_loss, dr\_or\_cr, reverse\_dr\_or\_cr, ref1\_dt, ref1\_dn, ref1\_detail\_no, ref2\_dt, ref2\_dn, ref2\_detail\_no, cost\_center, dimensions, project = no value.

**Declared result** str.

**Record and data access** read “Account” via get\_cached\_value · read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Journal Entry” · call save on journal\_entry · call submit on journal\_entry.

**Explicit results** journal\_entry.name.

**Explicit failure paths** validation helper — translated “Please set default Exchange Gain/Loss Account in Company {}”.format(company) · validation helper — translated “Currency for {0} must be {1}”.format(gain\_loss\_account, company\_currency).

**Local steps**

- Set journal\_entry from Platform.new\_doc(“Journal Entry”).
- Set journal\_entry.voucher\_type from “Exchange Gain Or Loss”.
- Set journal\_entry.company from company.
- Set journal\_entry.posting\_date from (posting\_date or nowdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in posting\_date → nowdate().
- Set journal\_entry.multi\_currency from 1.
- Set journal\_entry.is\_system\_generated from true.
- Set party\_account\_currency from Platform.get\_cached\_value(“Account”, party\_account, “account\_currency”).
- If not gain\_loss\_account.
  - Call the validation error handler Platform.throw(translated “Please set default Exchange Gain/Loss Account in Company {}”.format(company)).
- Set gain\_loss\_account\_currency from get\_account\_currency(gain\_loss\_account).
- Set company\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- If gain\_loss\_account\_currency differs from company\_currency.
  - Call the validation error handler Platform.throw(translated “Currency for {0} must be {1}”.format(gain\_loss\_account, company\_currency)).
- Set journal\_account from Platform.\_dict(mapping(“account” → party\_account, “party\_type” → party\_type, “party” → party, “account\_currency” → party\_account\_currency, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cost\_center → Enterprise.get\_default\_cost\_center(company).
- If dimensions.
  - Evaluate journal\_account.update(dimensions).
- Evaluate journal\_entry.append(“accounts”, journal\_account).
- Set journal\_account from Platform.\_dict(mapping(“account” → gain\_loss\_account, “account\_currency” → gain\_loss\_account\_currency, “exchange\_rate” → 1, “cost\_center” → (cost\_center or Enterprise.get\_default\_cost\_center(company)), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cost\_center → Enterprise.get\_default\_cost\_center(company).
- If dimensions.
  - Evaluate journal\_account.update(dimensions).
- Evaluate journal\_entry.append(“accounts”, journal\_account).
- Evaluate journal\_entry.save().
- Evaluate journal\_entry.submit().
- Return journal\_entry.name.

**Values supplied outside this operation** clock or generated value from nowdate() · configured or stored value from Platform.get\_cached\_value(“Account”, party\_account, “account\_currency”), Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L191)

<a id="op-79cc476a43bc89"></a>
### Get party types from account type

`operation_enterprise_accounts_utils_business_behavior_get_party_types_from_account_type`

**Inputs** account\_type.

**Record and data access** read “Party Type” via get\_all.

**Explicit results** Platform.db.get\_all(“Party Type”, mapping(“account\_type” → account\_type), pluck = “name”).

**Local steps**

- Return Platform.db.get\_all(“Party Type”, mapping(“account\_type” → account\_type), pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L1609) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L225)

<a id="op-1a74b7b97409cc"></a>
### Get advance payment doctypes

`operation_enterprise_accounts_utils_business_behavior_get_advance_payment_record_types`

**Inputs** payment\_type = no value.

**Explicit results** (Platform.get\_hooks(formatted text advance\_payment\_{payment\_type}\_doctypes) or list()) · ((Platform.get\_hooks(“advance\_payment\_receivable\_doctypes”) or list()) + (Platform.get\_hooks(“advance\_payment\_payable\_doctypes”) or list())).

**Local steps**

- If payment\_type.
  - Return (Platform.get\_hooks(formatted text advance\_payment\_{payment\_type}\_doctypes) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(formatted text advance\_payment\_{payment\_type}\_doctypes) → list().
- Return ((Platform.get\_hooks(“advance\_payment\_receivable\_doctypes”) or list()) + (Platform.get\_hooks(“advance\_payment\_payable\_doctypes”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“advance\_payment\_receivable\_doctypes”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“advance\_payment\_payable\_doctypes”) → list().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(formatted text advance\_payment\_{payment\_type}\_doctypes), Platform.get\_hooks(“advance\_payment\_receivable\_doctypes”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L1708) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L205)

<a id="op-7e39942ff10290"></a>
### Run ledger health checks

`operation_enterprise_accounts_utils_business_behavior_run_ledger_health_checks`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Ledger Health Monitor” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set health\_monitor\_settings from Platform.get\_doc(“Ledger Health Monitor”).
- If not health\_monitor\_settings.enable\_health\_monitor.
  - Return no value.
- Set period\_end from getdate().
- Set period\_start from add\_days(period\_end, negative abs(health\_monitor\_settings.monitor\_for\_last\_x\_days)).
- Set companies from list of x.company for x drawn from health\_monitor\_settings.companies.
  - Draw x from health\_monitor\_settings.companies.
- Set scan from Platform.\_dict(companies = companies, from\_date = period\_start, to\_date = period\_end).
- Set run\_date from get\_datetime().
- If health\_monitor\_settings.debit\_credit\_mismatch.
  - Set vouchers from get\_vouchers\_reported\_by(“Voucher-wise Balance”, companies, mapping(“from\_date” → period\_start, “to\_date” → period\_end)).
  - Evaluate update\_ledger\_health(“debit\_credit\_mismatch”, vouchers, run\_date, scan).
- If health\_monitor\_settings.general\_and\_payment\_ledger\_mismatch.
  - Set vouchers from get\_vouchers\_reported\_by(“General and Payment Ledger Comparison”, companies, mapping(“period\_start\_date” → period\_start, “period\_end\_date” → period\_end)).
  - Evaluate update\_ledger\_health(“general\_and\_payment\_ledger\_mismatch”, vouchers, run\_date, scan).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L245)

<a id="op-7238e155722c1f"></a>
### Get vouchers reported by

`operation_enterprise_binding_enterprise_accounts_utils_get_vouchers_reported_by`

**Inputs** report\_name, companies, filters.

**Record and data access** resolve a document from “Report” via get\_doc.

**Explicit results** vouchers.

**Local steps**

- Set report from Platform.get\_doc(“Report”, report\_name).
- Set vouchers from set().
- For each company in companies.
  - Set data from report.execute\_script\_report(filters = mapping(“company” → company, expand filters)) at 1.
  - Evaluate vouchers.update(generator of tuple(row.voucher\_type, row.voucher\_no) for row drawn from data).
    - Draw row from data.
- Return vouchers.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L219) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1284)

<a id="op-a04ca2de28e180"></a>
### Sync auto reconcile config

`operation_enterprise_accounts_utils_business_behavior_sync_auto_reconcile_configuration`

**Inputs** auto\_reconciliation\_job\_trigger = 15.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “DocType” via get\_value · read “Scheduler Event” via get\_value · resolve a document from mapping(“doctype” → “Scheduler Event”, expand event\_filters) via get\_doc · read “Scheduled Job Type” via get\_value · 2 additional forms in the steps below.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Scheduler Event”, expand event\_filters)) · call save on Platform.get\_doc(“Scheduled Job Type”, job\_name).update(mapping(“cron\_format” → formatted text 0/{auto\_reconciliation\_job\_trigger} \* \* \* \*, “scheduler\_event” → sch\_event, “frequency” → “Cron”, “create\_log” … · call insert on Platform.get\_doc(mapping(“doctype” → “Scheduled Job Type”, “method” → method, “scheduler\_event” → sch\_event, “cron\_format” → formatted text 0/{auto\_reconciliation\_job\_trigger} \* \* \* \*, …)).

**Local steps**

- Set auto\_reconciliation\_job\_trigger from (auto\_reconciliation\_job\_trigger or Platform.get\_single\_value(“Accounts Settings”, “auto\_reconciliation\_job\_trigger”) or 15).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in auto\_reconciliation\_job\_trigger → Platform.get\_single\_value(“Accounts Settings”, “auto\_reconciliation\_job\_trigger”) → 15.
- Set method from “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.trigger\_reconcilia …”.
- Set event\_filters from mapping(“scheduled\_against” → “Process Payment Reconciliation”, “method” → method).
- Evaluate Platform.db.get\_value(“DocType”, “Scheduler Event”, “name”, for\_update = true).
- Set sch\_event from Platform.db.get\_value(“Scheduler Event”, event\_filters, “name”).
- If not sch\_event.
  - Set sch\_event from Platform.get\_doc(mapping(“doctype” → “Scheduler Event”, expand event\_filters)).insert(ignore\_permissions = true).name.
- Set job\_name from Platform.db.get\_value(“Scheduled Job Type”, mapping(“method” → method), “name”).
- If job\_name.
  - Evaluate Platform.get\_doc(“Scheduled Job Type”, job\_name).update(mapping(“cron\_format” → formatted text 0/{auto\_reconciliation\_job\_trigger} \* \* \* \*, “scheduler\_event” → sch\_event, “frequency” → “Cron”, “create\_log” ….
- Otherwise.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Scheduled Job Type”, “method” → method, “scheduler\_event” → sch\_event, “cron\_format” → formatted text 0/{auto\_reconciliation\_job\_trigger} \* \* \* \*, …)).insert(ignore\_pe ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “auto\_reconciliation\_job\_trigger”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L247)

<a id="op-919982a44213bb"></a>
### Get link fields grouped by option

`operation_enterprise_accounts_utils_business_behavior_get_link_fields_grouped_by_option`

**Inputs** doctype.

**Explicit results** link\_fields\_map.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set link\_fields\_map from defaultdict(list).
- For each df in meta.fields.
  - If (df.fieldtype equals “Link” and df.options and not df.ignore\_user\_permissions).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Link” → df.options → not df.ignore\_user\_permissions.
    - Evaluate link\_fields\_map at df.options.append(df.fieldname).
- Return link\_fields\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L3285) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L222)

<a id="op-e9b30ce1751548"></a>
### Build qb match conditions

`operation_enterprise_accounts_utils_business_behavior_build_query_builder_match_conditions`

**Inputs** doctype, user = no value.

**Declared result** list.

**Explicit results** criterion.

**Local steps**

- Set match\_filters from build\_match\_conditions(doctype, user, false).
- Set link\_fields\_map from get\_link\_fields\_grouped\_by\_option(doctype).
- Set criterion from list().
- Set apply\_strict\_user\_permissions from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).
- If match\_filters.
  - Set \_dt from qb.DocType(doctype).
  - For each filter in match\_filters.
    - For each tuple(link\_option, allowed\_values) in filter.items().
      - Set fieldnames from link\_fields\_map.get(link\_option, list()).
      - Set cond from no value.
      - If link\_option equals doctype.
        - Set cond from \_dt at “name”.isin(allowed\_values).
      - For each fieldname in fieldnames.
        - Set field from \_dt at fieldname.
        - Set cond from field.isin(allowed\_values).
        - If not apply\_strict\_user\_permissions.
          - Set cond from (Coalesce(field, empty text) equals empty text bitwise or cond).
      - If cond.
        - Evaluate criterion.append(cond).
- Return criterion.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L3486) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L183)

<a id="op-8b6cd7bcb4942e"></a>
### Is immutable ledger enabled

`operation_enterprise_accounts_utils_business_behavior_is_immutable_ledger_enabled`

**Inputs** no declared parameters.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** Platform.get\_single\_value(“Accounts Settings”, “enable\_immutable\_ledger”).

**Local steps**

- Return Platform.get\_single\_value(“Accounts Settings”, “enable\_immutable\_ledger”).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “enable\_immutable\_ledger”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L4003) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L233)
