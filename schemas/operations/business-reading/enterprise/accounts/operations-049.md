# Accounting and settlement · operations 49

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · General ledger

<a id="op-6c76eb5fc376ac"></a>
### Get merge key

`operation_enterprise_accounts_general_ledger_business_behavior_get_merge_key`

**Inputs** entry, merge\_properties.

**Explicit results** tuple(merge\_key).

**Local steps**

- Set merge\_key from list().
- For each fieldname in merge\_properties.
  - Evaluate merge\_key.append(entry.get(fieldname, empty text)).
- Return tuple(merge\_key).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L4339) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L39) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L33)

<a id="op-e9f3fe8bf4356c"></a>
### Check if in list

`operation_enterprise_accounts_general_ledger_business_behavior_check_if_in_list`

**Inputs** gle, gl\_map.

**Explicit results** e.

**Local steps**

- For each e in gl\_map.
  - If e.merge\_key equals gle.merge\_key.
    - Return e.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L4467) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L33) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L27)

<a id="op-a583c6c2c1a95d"></a>
### Toggle debit credit if negative

`operation_enterprise_accounts_general_ledger_business_behavior_toggle_debit_credit_if_negative`

**Inputs** gl\_map.

**Explicit results** gl\_map.

**Local steps**

- Set debit\_credit\_field\_map from mapping(“debit” → “credit”, “debit\_in\_account\_currency” → “credit\_in\_account\_currency”, “debit\_in\_transaction\_currency” → “credit\_in\_transaction\_currency”).
- For each entry in gl\_map.
  - For each tuple(debit\_field, credit\_field) in debit\_credit\_field\_map.items().
    - Set debit from flt(entry.get(debit\_field)).
    - Set credit from flt(entry.get(credit\_field)).
    - If (debit &lt; 0 and credit &lt; 0 and debit equals credit).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in debit &lt; 0 → credit &lt; 0 → debit equals credit.
      - Update debit using × negative 1.
      - Update credit using × negative 1.
    - If debit &lt; 0.
      - Set credit from (credit − debit).
      - Set debit from 0.0.
    - If credit &lt; 0.
      - Set debit from (debit − credit).
      - Set credit from 0.0.
    - If (entry.post\_net\_value and debit and credit).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.post\_net\_value → debit → credit.
      - If debit &gt; credit.
        - Set debit from (debit − credit).
        - Set credit from 0.0.
      - Otherwise.
        - Set credit from (credit − debit).
        - Set debit from 0.0.
    - Set entry at debit\_field from debit.
    - Set entry at credit\_field from credit.
- Return gl\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L4556) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L54) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L48)

<a id="op-bc8524bd1f1de6"></a>
### Save entries

`operation_enterprise_accounts_general_ledger_business_behavior_save_entries`

**Inputs** gl\_map, adv\_adj, update\_outstanding, from\_repost = false.

**Local steps**

- If not from\_repost.
  - Evaluate validate\_cwip\_accounts(gl\_map).
- Evaluate process\_debit\_credit\_difference(gl\_map).
- Set dimension\_filter\_map from get\_dimension\_filter\_map().
- If gl\_map.
  - Evaluate check\_freezing\_date(gl\_map at 0 at “posting\_date”, gl\_map at 0 at “company”, adv\_adj).
  - Set is\_opening from any(generator of d.get(“is\_opening”) equals “Yes” for d drawn from gl\_map).
    - Draw d from gl\_map.
  - If gl\_map at 0 at “voucher\_type” differs from “Period Closing Voucher”.
    - Evaluate validate\_against\_pcv(is\_opening, gl\_map at 0 at “posting\_date”, gl\_map at 0 at “company”).
- For each entry in gl\_map.
  - Evaluate validate\_allowed\_dimensions(entry, dimension\_filter\_map).
  - Evaluate make\_entry(entry, adv\_adj, update\_outstanding, from\_repost).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L5164) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L46)

<a id="op-e80e0d8af2f0f8"></a>
### Make entry

`operation_enterprise_accounts_general_ledger_business_behavior_make_entry`

**Inputs** args, adv\_adj, update\_outstanding, from\_repost = false, from\_reversal (named only, default false).

**State and service calls** request new\_doc for “GL Entry” · call submit on gle.

**Local steps**

- Set gle from Platform.new\_doc(“GL Entry”).
- Evaluate gle.update(args).
- Set gle.flags.ignore\_permissions from 1.
- Set gle.flags.from\_repost from from\_repost.
- Set gle.flags.from\_reversal from from\_reversal.
- Set gle.flags.adv\_adj from adv\_adj.
- Set gle.flags.update\_outstanding from (update\_outstanding or “Yes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in update\_outstanding → “Yes”.
- Set gle.flags.notify\_update from false.
- If (gle.is\_cancelled or is\_immutable\_ledger\_enabled()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gle.is\_cancelled → is\_immutable\_ledger\_enabled().
  - Set gle.flags.ignore\_links from true.
- Evaluate gle.submit().
- If (not from\_repost and gle.voucher\_type differs from “Period Closing Voucher” and (gle.is\_cancelled equals 0 or gle.voucher\_type equals “Journal Entry”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not from\_repost → gle.voucher\_type differs from “Period Closing Voucher” → (gle.is\_cancelled equals 0 or gle.voucher\_type equals “Journal Entry”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gle.is\_cancelled equals 0 → gle.voucher\_type equals “Journal Entry”.
  - Evaluate validate\_expense\_against\_budget(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L44) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L38)

<a id="op-7a4a5b3821b796"></a>
### Validate cwip accounts

`operation_enterprise_binding_enterprise_accounts_general_ledger_validate_cwip_accounts`

**Inputs** gl\_map.

**Record and data access** read “Asset Category” via get\_all · execute query text (SELECT, Account).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Account: &lt;b&gt;{0}&lt;/b&gt; is capital Work in progress and can not be updated by Journal Entry”.format(entry.account).

**Local steps**

- If (gl\_map and gl\_map at 0.voucher\_type differs from “Journal Entry”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_map → gl\_map at 0.voucher\_type differs from “Journal Entry”.
  - Return no value.
- Set cwip\_enabled from any(generator of cint(ac.enable\_cwip\_accounting) for ac drawn from Platform.db.get\_all(“Asset Category”, “enable\_cwip\_accounting”)).
  - Draw ac from Platform.db.get\_all(“Asset Category”, “enable\_cwip\_accounting”).
- If cwip\_enabled.
  - Set cwip\_accounts from list of d at 0 for d drawn from Platform.db.sql(query text (SELECT, Account)).
    - Draw d from Platform.db.sql(query text (SELECT, Account)).
  - For each entry in gl\_map.
    - If entry.account belongs to cwip\_accounts.
      - Call the validation error handler Platform.throw(translated “Account: &lt;b&gt;{0}&lt;/b&gt; is capital Work in progress and can not be updated by Journal Entry”.format(entry.account)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1100)

<a id="op-fa02e04f777681"></a>
### Process debit credit difference

`operation_enterprise_accounts_general_ledger_business_behavior_process_debit_credit_difference`

**Inputs** gl\_map.

**Record and data access** read “Company” via get\_cached\_value · read “Journal Entry” via get\_cached\_value.

**Local steps**

- Set precision from get\_field\_precision(Platform.get\_meta(“GL Entry”).get\_field(“debit”), currency = Platform.get\_cached\_value(“Company”, gl\_map at 0.company, “default\_currency”)).
- Set voucher\_type from gl\_map at 0.voucher\_type.
- Set voucher\_no from gl\_map at 0.voucher\_no.
- Set allowance from get\_debit\_credit\_allowance(voucher\_type, precision).
- Set tuple(debit\_credit\_diff, trx\_cur\_debit\_credit\_diff) from get\_debit\_credit\_difference(gl\_map, precision).
- If abs(debit\_credit\_diff) &gt; allowance.
  - If not (voucher\_type equals “Journal Entry” and Platform.get\_cached\_value(“Journal Entry”, voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type equals “Journal Entry” → Platform.get\_cached\_value(“Journal Entry”, voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”.
    - Evaluate raise\_debit\_credit\_not\_equal\_error(debit\_credit\_diff, voucher\_type, voucher\_no).
- Otherwise.
  - If abs(debit\_credit\_diff) ≥ (1.0 ÷ (10 to the power precision)).
    - Evaluate make\_round\_off\_gle(gl\_map, debit\_credit\_diff, trx\_cur\_debit\_credit\_diff, precision).
- Set tuple(debit\_credit\_diff, trx\_cur\_debit\_credit\_diff) from get\_debit\_credit\_difference(gl\_map, precision).
- If abs(debit\_credit\_diff) &gt; allowance.
  - If not (voucher\_type equals “Journal Entry” and Platform.get\_cached\_value(“Journal Entry”, voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type equals “Journal Entry” → Platform.get\_cached\_value(“Journal Entry”, voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”.
    - Evaluate raise\_debit\_credit\_not\_equal\_error(debit\_credit\_diff, voucher\_type, voucher\_no).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, gl\_map at 0.company, “default\_currency”), Platform.get\_cached\_value(“Journal Entry”, voucher\_no, “voucher\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L6056) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L43)

<a id="op-89dc645c9a5d8b"></a>
### Get debit credit difference

`operation_enterprise_accounts_general_ledger_business_behavior_get_debit_credit_difference`

**Inputs** gl\_map, precision.

**Explicit results** tuple(debit\_credit\_diff, trx\_cur\_debit\_credit\_diff).

**Local steps**

- Set debit\_credit\_diff from 0.0.
- Set trx\_cur\_debit\_credit\_diff from 0.
- Set transaction\_precision from 0.
- For each entry in gl\_map.
  - Set entry.debit from flt(entry.debit, precision).
  - Set entry.credit from flt(entry.credit, precision).
  - Update debit\_credit\_diff using + (entry.debit − entry.credit).
  - Set entry\_precision from get\_transaction\_currency\_precision(entry, precision).
  - Set transaction\_precision from max(transaction\_precision, entry\_precision).
  - Set entry.debit\_in\_transaction\_currency from flt(entry.debit\_in\_transaction\_currency, entry\_precision).
  - Set entry.credit\_in\_transaction\_currency from flt(entry.credit\_in\_transaction\_currency, entry\_precision).
  - Update trx\_cur\_debit\_credit\_diff using + (entry.debit\_in\_transaction\_currency − entry.credit\_in\_transaction\_currency).
- Set debit\_credit\_diff from flt(debit\_credit\_diff, precision).
- Set trx\_cur\_debit\_credit\_diff from flt(trx\_cur\_debit\_credit\_diff, transaction\_precision).
- Return tuple(debit\_credit\_diff, trx\_cur\_debit\_credit\_diff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L38) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L32)

<a id="op-2fd9ec208dd66a"></a>
### Get debit credit allowance

`operation_enterprise_accounts_general_ledger_business_behavior_get_debit_credit_allowance`

**Inputs** voucher\_type, precision.

**Explicit results** allowance.

**Local steps**

- If voucher\_type belongs to tuple(“Journal Entry”, “Payment Entry”).
  - Set allowance from (5.0 ÷ (10 to the power precision)).
- Otherwise.
  - Set allowance from 0.5.
- Return allowance.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L7102) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L37) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L31)

<a id="op-1a44a8dddb77c5"></a>
### Raise debit credit not equal error

`operation_enterprise_accounts_general_ledger_business_behavior_raise_debit_credit_not_equal_error`

**Inputs** debit\_credit\_diff, voucher\_type, voucher\_no.

**Explicit failure paths** validation helper — translated “Debit and Credit not equal for {0} #{1}. Difference is {2}.”.format(voucher\_type, voucher\_no, debit\_credit\_diff).

**Local steps**

- Call the validation error handler Platform.throw(translated “Debit and Credit not equal for {0} #{1}. Difference is {2}.”.format(voucher\_type, voucher\_no, debit\_credit\_diff)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L7230) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L51) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L45)

<a id="op-993d60b3bae24c"></a>
### Has opening entries

`operation_enterprise_accounts_general_ledger_business_behavior_has_opening_entries`

**Inputs** gl\_map.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- For each x in gl\_map.
  - If x.is\_opening equals “Yes”.
    - Return true.
- Return false.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0210.json#L7339) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L42) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L36)

<a id="op-52a6a4c2ed9abd"></a>
### Make round off gle

`operation_enterprise_accounts_general_ledger_business_behavior_make_round_off_general_ledger_entry`

**Inputs** gl\_map, debit\_credit\_diff, trx\_cur\_debit\_credit\_diff, precision.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please set '{0}' in Company: {1}”.format(Platform.bold(“Round Off for Opening”), get\_link\_to\_form(“Company”, gl\_map at 0.company)).

**Local steps**

- Set tuple(round\_off\_account, round\_off\_cost\_center, round\_off\_for\_opening) from get\_round\_off\_account\_and\_cost\_center(gl\_map at 0.company, gl\_map at 0.voucher\_type, gl\_map at 0.voucher\_no).
- Set round\_off\_gle from Platform.\_dict().
- Set round\_off\_account\_exists from false.
- Set has\_opening\_entry from has\_opening\_entries(gl\_map).
- If has\_opening\_entry.
  - If not round\_off\_for\_opening.
    - Call the validation error handler Platform.throw(translated “Please set '{0}' in Company: {1}”.format(Platform.bold(“Round Off for Opening”), get\_link\_to\_form(“Company”, gl\_map at 0.company))).
  - Set account from round\_off\_for\_opening.
- Otherwise.
  - Set account from round\_off\_account.
- If gl\_map at 0.voucher\_type differs from “Period Closing Voucher”.
  - For each d in gl\_map.
    - If d.account equals account.
      - Set round\_off\_gle from d.
      - If d.debit.
        - Update debit\_credit\_diff using − (flt(d.debit) − flt(d.credit)).
      - Otherwise.
        - Update debit\_credit\_diff using + flt(d.credit).
      - Update trx\_cur\_debit\_credit\_diff using − (flt(d.debit\_in\_transaction\_currency) − flt(d.credit\_in\_transaction\_currency)).
      - Set round\_off\_account\_exists from true.
  - Set debit\_credit\_diff from flt(debit\_credit\_diff, precision).
  - If (round\_off\_account\_exists and abs(debit\_credit\_diff) &lt; (1.0 ÷ (10 to the power precision))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in round\_off\_account\_exists → abs(debit\_credit\_diff) &lt; (1.0 ÷ (10 to the power precision)).
    - Evaluate gl\_map.remove(round\_off\_gle).
    - Return no value.
- If not round\_off\_gle.
  - For each k in list(“voucher\_type”, “voucher\_no”, “company”, “posting\_date”, …).
    - Set round\_off\_gle at k from gl\_map at 0 at k.
- Evaluate round\_off\_gle.update(mapping(“account” → account, “debit\_in\_account\_currency” → abs(debit\_credit\_diff) when debit\_credit\_diff &lt; 0, otherwise 0, “credit\_in\_account\_currency” → debit\_credit\_diff when debit\_c ….
  - Value choice on debit\_credit\_diff &lt; 0 — true gives abs(debit\_credit\_diff), false gives 0.
  - Value choice on debit\_credit\_diff &gt; 0 — true gives debit\_credit\_diff, false gives 0.
  - Value choice on debit\_credit\_diff &lt; 0 — true gives abs(debit\_credit\_diff), false gives 0.
  - Value choice on debit\_credit\_diff &gt; 0 — true gives debit\_credit\_diff, false gives 0.
  - Value choice on trx\_cur\_debit\_credit\_diff &lt; 0 — true gives abs(trx\_cur\_debit\_credit\_diff), false gives 0.
  - Value choice on trx\_cur\_debit\_credit\_diff &gt; 0 — true gives trx\_cur\_debit\_credit\_diff, false gives 0.
- If has\_opening\_entry.
  - Evaluate round\_off\_gle.update(mapping(“is\_opening” → “Yes”)).
- Evaluate update\_accounting\_dimensions(round\_off\_gle).
- If not round\_off\_account\_exists.
  - Evaluate gl\_map.append(round\_off\_gle).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L41)

<a id="op-7fc07555fc351f"></a>
### Update accounting dimensions

`operation_enterprise_accounts_general_ledger_business_behavior_update_accounting_dimensions`

**Inputs** round\_off\_gle.

**Record and data access** read round\_off\_gle at “voucher\_type” via get\_value · read “Account” via get\_cached\_value.

**Local steps**

- Set dimensions from get\_accounting\_dimensions().
- Set meta from Platform.get\_meta(round\_off\_gle at “voucher\_type”).
- Set has\_all\_dimensions from true.
- For each dimension in dimensions.
  - If not meta.has\_field(dimension).
    - Set has\_all\_dimensions from false.
- If (dimensions and has\_all\_dimensions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dimensions → has\_all\_dimensions.
  - Set dimension\_values from Platform.db.get\_value(round\_off\_gle at “voucher\_type”, round\_off\_gle at “voucher\_no”, dimensions, as\_dict = 1).
  - For each dimension in dimensions.
    - Set round\_off\_gle at dimension from dimension\_values.get(dimension).
- Otherwise.
  - Set report\_type from Platform.get\_cached\_value(“Account”, round\_off\_gle.account, “report\_type”).
  - For each dimension in get\_checks\_for\_pl\_and\_bs\_accounts().
    - If (round\_off\_gle.company equals dimension.company and ((report\_type equals “Profit and Loss” and dimension.mandatory\_for\_pl) or (report\_type equals “Balance Sheet” and dimension.mandatory\_for\_bs)) and dimens ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in round\_off\_gle.company equals dimension.company → ((report\_type equals “Profit and Loss” and dimension.mandatory\_for\_pl) or (report\_type equals “Balance Sheet” and dimension.mandatory\_for\_bs)) → dimension.default\_dimension.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (report\_type equals “Profit and Loss” and dimension.mandatory\_for\_pl) → (report\_type equals “Balance Sheet” and dimension.mandatory\_for\_bs).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_type equals “Profit and Loss” → dimension.mandatory\_for\_pl.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in report\_type equals “Balance Sheet” → dimension.mandatory\_for\_bs.
      - Set round\_off\_gle at dimension.fieldname from dimension.default\_dimension.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, round\_off\_gle.account, “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0211.json#L1268) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L55) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L49)

<a id="op-2c440d0f12488c"></a>
### Get round off account and cost center

`operation_enterprise_accounts_general_ledger_business_behavior_get_round_off_account_and_cost_center`

**Inputs** company, voucher\_type, voucher\_no, use\_company\_default = false.

**Record and data access** read “Company” via get\_cached\_value · read voucher\_type via get\_value.

**Explicit results** tuple(round\_off\_account, round\_off\_cost\_center, round\_off\_for\_opening).

**Explicit failure paths** validation helper — translated “Please mention '{0}' in Company: {1}”.format(Platform.bold(“Round Off Account”), get\_link\_to\_form(“Company”, company)) · validation helper — translated “Please mention '{0}' in Company: {1}”.format(Platform.bold(“Round Off Cost Center”), get\_link\_to\_form(“Company”, company)).

**Local steps**

- Set tuple(round\_off\_account, round\_off\_cost\_center, round\_off\_for\_opening) from (Platform.get\_cached\_value(“Company”, company, list(“round\_off\_account”, “round\_off\_cost\_center”, “round\_off\_for\_opening”)) or list(no value, no value, no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Company”, company, list(“round\_off\_account”, “round\_off\_cost\_center”, “round\_off\_for\_opening”)) → list(no value, no value, no value).
- If not round\_off\_account.
  - Set round\_off\_account from Platform.get\_cached\_value(“Company”, company, “default\_expense\_account”).
- Set meta from Platform.get\_meta(voucher\_type).
- If (not use\_company\_default and meta.has\_field(“cost\_center”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not use\_company\_default → meta.has\_field(“cost\_center”).
  - Set parent\_cost\_center from Platform.db.get\_value(voucher\_type, voucher\_no, “cost\_center”).
  - If parent\_cost\_center.
    - Set round\_off\_cost\_center from parent\_cost\_center.
- If not round\_off\_account.
  - Call the validation error handler Platform.throw(translated “Please mention '{0}' in Company: {1}”.format(Platform.bold(“Round Off Account”), get\_link\_to\_form(“Company”, company))).
- If not round\_off\_cost\_center.
  - Call the validation error handler Platform.throw(translated “Please mention '{0}' in Company: {1}”.format(Platform.bold(“Round Off Cost Center”), get\_link\_to\_form(“Company”, company))).
- Return tuple(round\_off\_account, round\_off\_cost\_center, round\_off\_for\_opening).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“round\_off\_account”, “round\_off\_cost\_center”, “round\_off\_for\_opening”)), Platform.get\_cached\_value(“Company”, company, “default\_expense\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0211.json#L1798) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L41) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L35)

<a id="op-4352eebd573652"></a>
### Make reverse gl entries

`operation_enterprise_accounts_general_ledger_business_behavior_make_reverse_general_ledger_entries`

**Inputs** gl\_entries = no value, voucher\_type = no value, voucher\_no = no value, adv\_adj = false, update\_outstanding = “Yes”, partial\_cancel = false, posting\_date = no value.

**State and service calls** execute a supplied database query.

**Local steps**

- Set immutable\_ledger\_enabled from is\_immutable\_ledger\_enabled().
- If not gl\_entries.
  - Set gl\_entry from Platform.qb.DocType(“GL Entry”).
  - Set gl\_entries from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_cancelled equals 0).for\_update().run(as\_dict = 1).
- If gl\_entries.
  - Evaluate create\_payment\_ledger\_entry(gl\_entries, cancel = 1, adv\_adj = adv\_adj, update\_outstanding = update\_outstanding, partial\_cancel = partial\_cancel).
  - Evaluate validate\_accounting\_period(gl\_entries).
  - Set is\_opening from any(generator of d.get(“is\_opening”) equals “Yes” for d drawn from gl\_entries).
    - Draw d from gl\_entries.
  - If immutable\_ledger\_enabled.
    - Set validation\_date from (posting\_date or Platform.form\_dict.get(“posting\_date”) or getdate()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in posting\_date → Platform.form\_dict.get(“posting\_date”) → getdate().
  - Otherwise.
    - Set validation\_date from posting\_date when posting\_date, otherwise gl\_entries at 0 at “posting\_date”.
      - Value choice on posting\_date — true gives posting\_date, false gives gl\_entries at 0 at “posting\_date”.
  - Evaluate check\_freezing\_date(validation\_date, gl\_entries at 0 at “company”, adv\_adj).
  - Evaluate validate\_against\_pcv(is\_opening, validation\_date, gl\_entries at 0 at “company”).
  - If partial\_cancel.
    - Set gle from Platform.qb.DocType(“GL Entry”).
    - For each x in gl\_entries.
      - Set query from nested operand in the contract(nested operand in the contract).set(gle.modified, now()).set(gle.modified\_by, Platform.session.user).where(((((((nested operand in the contract bitwise and nested operand in  ….
      - If not immutable\_ledger\_enabled.
        - Set query from query.set(gle.is\_cancelled, true).
      - Evaluate query.run().
  - Otherwise.
    - If not immutable\_ledger\_enabled.
      - Set gle\_names from list of x.get(“name”) for x drawn from gl\_entries.
        - Draw x from gl\_entries.
      - If not all(gle\_names).
        - Evaluate set\_as\_cancel(gl\_entries at 0 at “voucher\_type”, gl\_entries at 0 at “voucher\_no”).
      - Otherwise.
        - Evaluate Platform.db.sql(“UPDATE ′tabGL Entry′ SET is\_cancelled = 1,\\n\\t\\t\\t\\t\\t\\tmodified=%s, modified\_by=%s\\n\\t\\t\\t\\t\\t\\twhere name  …”, tuple(now(), Platform.session.user, tuple(gle\_names))).
  - For each entry in gl\_entries.
    - Set new\_gle from copy.deepcopy(entry).
    - Set new\_gle at “name” from no value.
    - Set debit from new\_gle.get(“debit”, 0).
    - Set credit from new\_gle.get(“credit”, 0).
    - Set debit\_in\_account\_currency from new\_gle.get(“debit\_in\_account\_currency”, 0).
    - Set credit\_in\_account\_currency from new\_gle.get(“credit\_in\_account\_currency”, 0).
    - Set debit\_in\_transaction\_currency from new\_gle.get(“debit\_in\_transaction\_currency”, 0).
    - Set credit\_in\_transaction\_currency from new\_gle.get(“credit\_in\_transaction\_currency”, 0).
    - Set new\_gle at “debit” from credit.
    - Set new\_gle at “credit” from debit.
    - Set new\_gle at “debit\_in\_account\_currency” from credit\_in\_account\_currency.
    - Set new\_gle at “credit\_in\_account\_currency” from debit\_in\_account\_currency.
    - Set new\_gle at “debit\_in\_transaction\_currency” from credit\_in\_transaction\_currency.
    - Set new\_gle at “credit\_in\_transaction\_currency” from debit\_in\_transaction\_currency.
    - Set new\_gle at “remarks” from (“On cancellation of ” + new\_gle at “voucher\_no”).
    - Set new\_gle at “is\_cancelled” from 1.
    - If immutable\_ledger\_enabled.
      - Set new\_gle at “is\_cancelled” from 0.
      - Set new\_gle at “posting\_date” from (posting\_date or Platform.form\_dict.get(“posting\_date”) or getdate()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in posting\_date → Platform.form\_dict.get(“posting\_date”) → getdate().
    - Otherwise.
      - If posting\_date.
        - Set new\_gle at “posting\_date” from posting\_date.
    - If any(list(debit, credit, debit\_in\_account\_currency, credit\_in\_account\_currency)).
      - Evaluate make\_entry(new\_gle, adv\_adj, “Yes”, from\_reversal = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L46) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L40)

<a id="op-067f18a4f8004f"></a>
### Check freezing date

`operation_enterprise_binding_enterprise_accounts_general_ledger_check_freezing_date`

**Inputs** posting\_date, company, adv\_adj = false.

**Record and data access** read “Company” via get\_value.

**Explicit failure paths** validation helper — translated “You are not authorized to add or update entries before {0}”.format(formatdate(acc\_frozen\_till\_date)).

**Local steps**

- If not adv\_adj.
  - Set acc\_frozen\_till\_date from Platform.db.get\_value(“Company”, company, “accounts\_frozen\_till\_date”).
  - If acc\_frozen\_till\_date.
    - Set frozen\_accounts\_modifier from Platform.db.get\_value(“Company”, company, “role\_allowed\_for\_frozen\_entries”).
    - If (getdate(posting\_date) ≤ getdate(acc\_frozen\_till\_date) and (frozen\_accounts\_modifier does not belong to Platform.get\_roles() or Platform.session.user equals “Administrator”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(posting\_date) ≤ getdate(acc\_frozen\_till\_date) → (frozen\_accounts\_modifier does not belong to Platform.get\_roles() or Platform.session.user equals “Administrator”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in frozen\_accounts\_modifier does not belong to Platform.get\_roles() → Platform.session.user equals “Administrator”.
      - Call the validation error handler Platform.throw(translated “You are not authorized to add or update entries before {0}”.format(formatdate(acc\_frozen\_till\_date))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1094)

<a id="op-d5a1af1eb7d946"></a>
### Validate opening entry against pcv

`operation_enterprise_binding_enterprise_accounts_general_ledger_validate_opening_entry_against_pcv`

**Inputs** company.

**Record and data access** read “Period Closing Voucher” via exists.

**Explicit failure paths** validation helper — translated “A Period Closing Voucher is already submitted and an Opening Entry can no longer be created. {0} to learn more.”.format(((text in the contract + translated “Read the docs”) + “&lt;/a&gt;”)).

**Local steps**

- If Platform.db.exists(“Period Closing Voucher”, mapping(“docstatus” → 1, “company” → company)).
  - Call the validation error handler Platform.throw(translated “A Period Closing Voucher is already submitted and an Opening Entry can no longer be created. {0} to learn more.”.format(((text in the contract + translated “Read the docs”) + “&lt;/ ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1102)

<a id="op-25557287d764f4"></a>
### Validate against pcv

`operation_enterprise_binding_enterprise_accounts_general_ledger_validate_against_pcv`

**Inputs** is\_opening, posting\_date, company.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If is\_opening.
  - Evaluate validate\_opening\_entry\_against\_pcv(company).
- Set last\_pcv\_date from Platform.db.get\_value(“Period Closing Voucher”, mapping(“docstatus” → 1, “company” → company), list(mapping(“MAX” → “period\_end\_date”))).
- If (last\_pcv\_date and getdate(posting\_date) ≤ getdate(last\_pcv\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_pcv\_date → getdate(posting\_date) ≤ getdate(last\_pcv\_date).
  - Set message from translated “Books have been closed till the period ending on {0}”.format(formatdate(last\_pcv\_date)).
  - Update message using + “&lt;/br &gt;”.
  - Update message using + translated “You cannot create/amend any accounting entries till this date.”.
  - Call the validation error handler Platform.throw(message, title = translated “Period Closed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1098)

<a id="op-4a3c2a5678fbb5"></a>
### Set as cancel

`operation_enterprise_accounts_general_ledger_business_behavior_set_as_cancel`

**Inputs** voucher\_type, voucher\_no.

**State and service calls** execute a supplied database query.

**Local steps**

- Evaluate Platform.db.sql(“UPDATE ′tabGL Entry′ SET is\_cancelled = 1,\\n\\t\\tmodified=%s, modified\_by=%s\\n\\t\\twhere voucher\_type=%s and v …”, tuple(now(), Platform.session.user, voucher\_type, voucher\_no)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L53) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L47)

<a id="op-0bf8431de8334b"></a>
### Validate allowed dimensions

`operation_enterprise_binding_enterprise_accounts_general_ledger_validate_allowed_dimensions`

**Inputs** gl\_entry, dimension\_filter\_map.

**Explicit failure paths** validation helper with MandatoryAccountDimensionError — translated “{0} is mandatory for account {1}”.format(Platform.bold(dimension\_label), Platform.bold(gl\_entry.account)) · validation helper with InvalidAccountDimensionError — translated “Invalid value {0} for {1} against account {2}”.format(Platform.bold(gl\_entry.get(dimension)), Platform.bold(dimension\_label), Platform.bold(gl\_entry.account)).

**Local steps**

- Set meta from Platform.get\_meta(“GL Entry”).
- For each tuple(key, value) in dimension\_filter\_map.items().
  - Set dimension from key at 0.
  - Set account from key at 1.
  - If gl\_entry.account equals account.
    - Set dimension\_label from get\_dimension\_label(meta, dimension).
    - If (value at “is\_mandatory” and not gl\_entry.get(dimension)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in value at “is\_mandatory” → not gl\_entry.get(dimension).
      - Call the validation error handler Platform.throw(translated “{0} is mandatory for account {1}”.format(Platform.bold(dimension\_label), Platform.bold(gl\_entry.account)), MandatoryAccountDimensionError).
    - If value at “allow\_or\_restrict” equals “Allow”.
      - If (gl\_entry.get(dimension) and gl\_entry.get(dimension) does not belong to value at “allowed\_dimensions”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_entry.get(dimension) → gl\_entry.get(dimension) does not belong to value at “allowed\_dimensions”.
        - Call the validation error handler Platform.throw(translated “Invalid value {0} for {1} against account {2}”.format(Platform.bold(gl\_entry.get(dimension)), Platform.bold(dimension\_label), Platform.bold(gl\_entry.account)), InvalidAccountDime ….
    - Otherwise.
      - If (gl\_entry.get(dimension) and gl\_entry.get(dimension) belongs to value at “allowed\_dimensions”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_entry.get(dimension) → gl\_entry.get(dimension) belongs to value at “allowed\_dimensions”.
        - Call the validation error handler Platform.throw(translated “Invalid value {0} for {1} against account {2}”.format(Platform.bold(gl\_entry.get(dimension)), Platform.bold(dimension\_label), Platform.bold(gl\_entry.account)), InvalidAccountDime ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1099)

## Record · Gl entry

<a id="op-fa5a684d65ca2d"></a>
### GLEntry.autoname

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_autoname`

**Inputs** self.

**Local steps**

- Set self.name from Platform.generate\_hash(txt = empty text, length = 10).
- If self.meta.autoname equals “hash”.
  - Set self.to\_rename from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(txt = empty text, length = 10).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L563) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1049)

<a id="op-80d23df86db52b"></a>
### GLEntry.validate

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_validate`

**Inputs** self.

**Local steps**

- Set self.flags.ignore\_submit\_comment from true.
- Evaluate self.validate\_and\_set\_fiscal\_year().
- Evaluate self.pl\_must\_have\_cost\_center().
- If (not self.flags.from\_repost and self.voucher\_type differs from “Period Closing Voucher”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.from\_repost → self.voucher\_type differs from “Period Closing Voucher”.
  - Evaluate self.check\_mandatory().
  - Evaluate self.validate\_cost\_center().
  - Evaluate self.check\_pl\_account().
  - Evaluate self.validate\_party().
  - Evaluate self.validate\_currency().
- Evaluate self.set\_amount\_in\_reporting\_currency().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate and set fiscal year](operations-050.md#op-ac22c714598223), [pl must have cost center](operations-050.md#op-1de5a76106ddbc), [check mandatory](operations-049.md#op-bb42dc69690b3d), [validate cost center](operations-050.md#op-2a6e28012caba9), [check pl account](operations-050.md#op-c7d82fc65b8250), [validate party](operations-050.md#op-b4d6a8af2fec3e), [validate currency](operations-050.md#op-bde378a357ed12), [set amount in reporting currency](operations-050.md#op-44d4954c5560f6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L694) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1056)

<a id="op-1a51837ab76d6d"></a>
### GLEntry.on update

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_on_update`

**Inputs** self.

**Record and data access** read “Journal Entry” via get\_cached\_value · read “Account” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set adv\_adj from self.flags.adv\_adj.
- If (not self.flags.from\_repost and self.voucher\_type differs from “Period Closing Voucher”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.from\_repost → self.voucher\_type differs from “Period Closing Voucher”.
  - Evaluate self.validate\_account\_details(adv\_adj).
  - Evaluate self.validate\_dimensions\_for\_pl\_and\_bs().
  - Evaluate validate\_balance\_type(self.account, adv\_adj).
  - Evaluate validate\_frozen\_account(self.company, self.account, adv\_adj).
  - If (self.voucher\_type equals “Journal Entry” and Platform.get\_cached\_value(“Journal Entry”, self.voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Journal Entry” → Platform.get\_cached\_value(“Journal Entry”, self.voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”.
    - Return no value.
  - If Platform.get\_cached\_value(“Account”, self.account, “account\_type”) does not belong to list(“Receivable”, “Payable”).
    - If (self.against\_voucher\_type belongs to list(“Journal Entry”, “Sales Invoice”, “Purchase Invoice”, “Fees”) and self.against\_voucher and self.flags.update\_outstanding equals “Yes” and not Platform.flags.is\_re ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.against\_voucher\_type belongs to list(“Journal Entry”, “Sales Invoice”, “Purchase Invoice”, “Fees”) → self.against\_voucher → self.flags.update\_outstanding equals “Yes” → not Platform.flags.is\_reverse\_depr\_entry.
      - Evaluate update\_outstanding\_amt(self.account, self.party\_type, self.party, self.against\_voucher\_type, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account details](operations-050.md#op-4473b407719b1b), [validate dimensions for pl and bs](operations-050.md#op-4cbc046bfa6e70).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Journal Entry”, self.voucher\_no, “voucher\_type”), Platform.get\_cached\_value(“Account”, self.account, “account\_type”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0058.json#L959) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1053)

<a id="op-bb42dc69690b3d"></a>
### GLEntry.check mandatory

`operation_enterprise_accounts_record_definitions_general_ledger_entry_business_behavior_general_ledger_entry_check_mandatory`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value · read “Journal Entry” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} is required”.format(translated self.meta.get\_label(k)) · validation helper — translated “{0} {1}: Customer is required against Receivable account {2}”.format(self.voucher\_type, self.voucher\_no, self.account) · validation helper — translated “{0} {1}: Supplier is required against Payable account {2}”.format(self.voucher\_type, self.voucher\_no, self.account) · validation helper — translated “{0} {1}: Either debit or credit amount is required for {2}”.format(self.voucher\_type, self.voucher\_no, self.account).

**Local steps**

- Set mandatory from list(“account”, “voucher\_type”, “voucher\_no”, “company”).
- For each k in mandatory.
  - If not self.get(k).
    - Call the validation error handler Platform.throw(translated “{0} is required”.format(translated self.meta.get\_label(k))).
- If (not self.is\_cancelled and not (self.party\_type and self.party)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_cancelled → not (self.party\_type and self.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_type → self.party.
  - Set account\_type from Platform.get\_cached\_value(“Account”, self.account, “account\_type”).
  - If not Platform.flags.party\_not\_required.
    - If account\_type equals “Receivable”.
      - Call the validation error handler Platform.throw(translated “{0} {1}: Customer is required against Receivable account {2}”.format(self.voucher\_type, self.voucher\_no, self.account)).
    - Otherwise.
      - If account\_type equals “Payable”.
        - Call the validation error handler Platform.throw(translated “{0} {1}: Supplier is required against Payable account {2}”.format(self.voucher\_type, self.voucher\_no, self.account)).
- If not (flt(self.debit, self.precision(“debit”)) or flt(self.credit, self.precision(“credit”)) or (self.voucher\_type equals “Journal Entry” and Platform.get\_cached\_value(“Journal Entry”, self.voucher\_no, “voucher ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.debit, self.precision(“debit”)) → flt(self.credit, self.precision(“credit”)) → (self.voucher\_type equals “Journal Entry” and Platform.get\_cached\_value(“Journal Entry”, self.voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Journal Entry” → Platform.get\_cached\_value(“Journal Entry”, self.voucher\_no, “voucher\_type”) equals “Exchange Gain Or Loss”.
  - Call the validation error handler Platform.throw(translated “{0} {1}: Either debit or credit amount is required for {2}”.format(self.voucher\_type, self.voucher\_no, self.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “account\_type”), Platform.get\_cached\_value(“Journal Entry”, self.voucher\_no, “voucher\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1050)
