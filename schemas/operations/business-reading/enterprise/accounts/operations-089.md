# Accounting and settlement · operations 89

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Process period closing voucher

[Record definition](../../../../data/record-types/process_period_closing_voucher.json)

<a id="op-172053df6aafc3"></a>
### Pause pcv processing

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_pause_period_closing_voucher_processing`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Process Period Closing Voucher Detail” via get\_all.

**Explicit results** no value.

**Local steps**

- Evaluate Platform.has\_permission(“Process Period Closing Voucher”, ptype = “write”, doc = docname, throw = true).
- If not Platform.get\_lazy\_doc(“Process Period Closing Voucher”, docname).validate\_processing(list(“Running”)).
  - Return no value.
- Set ppcv from qb.DocType(“Process Period Closing Voucher”).
- Evaluate nested operand in the contract(nested operand in the contract).set(ppcv.status, “Paused”).where(ppcv.name.eq(docname)).run().
- If queued\_dates bound to Platform.db.get\_all(“Process Period Closing Voucher Detail”, filters = mapping(“parent” → docname, “status” → list(“in”, list(“Queued”, “Running”))), pluck = “name”).
  - Set ppcvd from qb.DocType(“Process Period Closing Voucher Detail”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(ppcvd.status, “Paused”).where(ppcvd.name.isin(queued\_dates)).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Period Closing Voucher”, ptype = “write”, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L836)

<a id="op-409f8237cd415e"></a>
### Cancel pcv processing

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_cancel_period_closing_voucher_processing`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Process Period Closing Voucher” via get\_value · read “Process Period Closing Voucher Detail” via get\_all.

**Explicit failure paths** validation helper — translated “Cancel the Process Period Closing Voucher document to stop processing”.

**Local steps**

- Evaluate Platform.has\_permission(“Process Period Closing Voucher”, ptype = “cancel”, doc = docname, throw = true).
- If Platform.db.get\_value(“Process Period Closing Voucher”, docname, “docstatus”) differs from 2.
  - Call the validation error handler Platform.throw(translated “Cancel the Process Period Closing Voucher document to stop processing”).
- Set ppcv from qb.DocType(“Process Period Closing Voucher”).
- Evaluate nested operand in the contract(nested operand in the contract).set(ppcv.status, “Cancelled”).where(ppcv.name.eq(docname)).run().
- If queued\_dates bound to Platform.db.get\_all(“Process Period Closing Voucher Detail”, filters = mapping(“parent” → docname, “status” → list(“in”, list(“Queued”, “Running”, “Paused”))), pluck = “name”).
  - Set ppcvd from qb.DocType(“Process Period Closing Voucher Detail”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(ppcvd.status, “Cancelled”).where(ppcvd.name.isin(queued\_dates)).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Period Closing Voucher”, ptype = “cancel”, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L823)

<a id="op-28ad6df9e2f360"></a>
### Resume pcv processing

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_resume_period_closing_voucher_processing`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Process Period Closing Voucher Detail” via get\_all.

**Explicit results** no value.

**Local steps**

- Evaluate Platform.has\_permission(“Process Period Closing Voucher”, ptype = “write”, doc = docname, throw = true).
- If not Platform.get\_lazy\_doc(“Process Period Closing Voucher”, docname).validate\_processing(list(“Paused”, “Running”)).
  - Return no value.
- Set ppcv from qb.DocType(“Process Period Closing Voucher”).
- Evaluate nested operand in the contract(nested operand in the contract).set(ppcv.status, “Running”).where(ppcv.name.eq(docname)).run().
- If paused\_dates bound to Platform.db.get\_all(“Process Period Closing Voucher Detail”, filters = mapping(“parent” → docname, “status” → “Paused”), pluck = “name”).
  - Set ppcvd from qb.DocType(“Process Period Closing Voucher Detail”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(ppcvd.status, “Queued”).where(ppcvd.name.isin(paused\_dates)).run().
  - Evaluate start\_pcv\_processing(docname).
- Otherwise.
  - Evaluate schedule\_next\_date(docname).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Period Closing Voucher”, ptype = “write”, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L846)

<a id="op-e7d8b02b1bb08f"></a>
### Update default dimensions

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_update_default_dimensions`

**Inputs** dimension\_fields, gl\_entry, dimension\_values.

**Local steps**

- For each tuple(i, dimension) in enumerate(dimension\_fields).
  - Set gl\_entry at dimension from dimension\_values at i.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L2503) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L850)

<a id="op-3012a60b3dd452"></a>
### Get gle for pl account

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_general_ledger_entry_for_profit_and_loss_account`

**Inputs** pcv, acc, balances, dimensions.

**Explicit results** gl\_entry.

**Local steps**

- Set balance\_in\_account\_currency from (flt(balances.debit\_in\_account\_currency) − flt(balances.credit\_in\_account\_currency)).
- Set balance\_in\_company\_currency from (flt(balances.debit) − flt(balances.credit)).
- Set gl\_entry from Platform.\_dict(mapping(“company” → pcv.company, “posting\_date” → pcv.period\_end\_date, “account” → acc, “account\_currency” → balances.account\_currency, …)).
  - Value choice on balance\_in\_account\_currency &lt; 0 — true gives abs(balance\_in\_account\_currency), false gives 0.
  - Value choice on balance\_in\_company\_currency &lt; 0 — true gives abs(balance\_in\_company\_currency), false gives 0.
  - Value choice on balance\_in\_account\_currency &gt; 0 — true gives abs(balance\_in\_account\_currency), false gives 0.
  - Value choice on balance\_in\_company\_currency &gt; 0 — true gives abs(balance\_in\_company\_currency), false gives 0.
- Evaluate update\_default\_dimensions(get\_dimensions(), gl\_entry, dimensions).
- Return gl\_entry.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L2611) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L832)

<a id="op-8255ccdabe65cd"></a>
### Get gle for closing account

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_general_ledger_entry_for_closing_account`

**Inputs** pcv, dimension\_balance, dimensions.

**Record and data access** read “Account” via get\_value.

**Explicit results** gl\_entry.

**Local steps**

- Set balance\_in\_company\_currency from flt(dimension\_balance.balance\_in\_company\_currency).
- Set debit from balance\_in\_company\_currency when balance\_in\_company\_currency &gt; 0, otherwise 0.
  - Value choice on balance\_in\_company\_currency &gt; 0 — true gives balance\_in\_company\_currency, false gives 0.
- Set credit from abs(balance\_in\_company\_currency) when balance\_in\_company\_currency &lt; 0, otherwise 0.
  - Value choice on balance\_in\_company\_currency &lt; 0 — true gives abs(balance\_in\_company\_currency), false gives 0.
- Set gl\_entry from Platform.\_dict(mapping(“company” → pcv.company, “posting\_date” → pcv.period\_end\_date, “account” → pcv.closing\_account\_head, “account\_currency” → Platform.db.get\_value(“Account”, pcv.closing\_account\_head, “ ….
- Evaluate update\_default\_dimensions(get\_dimensions(), gl\_entry, dimensions).
- Return gl\_entry.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L3234) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L831)

<a id="op-69e2e3755b9602"></a>
### Schedule next date

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_schedule_next_date`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Accounts Settings” via get\_single\_value.

**State and service calls** request set\_value on “Process Period Closing Voucher Detail” · commit · enqueue.

**Explicit results** no value.

**Local steps**

- Evaluate Platform.has\_permission(“Process Period Closing Voucher”, ptype = “write”, doc = docname, throw = true).
- If not Platform.get\_lazy\_doc(“Process Period Closing Voucher”, docname).validate\_processing(list(“Running”)).
  - Return no value.
- Set timeout from (Platform.db.get\_single\_value(“Accounts Settings”, “pcv\_job\_timeout”) or 3600).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Accounts Settings”, “pcv\_job\_timeout”) → 3600.
- Set ppcvd from qb.DocType(“Process Period Closing Voucher Detail”).
- If to\_process bound to nested operand in the contract.limit(1).for\_update(skip\_locked = true).run(as\_dict = true).
  - If not is\_scheduler\_inactive().
    - Evaluate Platform.db.set\_value(“Process Period Closing Voucher Detail”, to\_process at 0.name, “status”, “Running”).
    - If not Platform.in\_test.
      - Evaluate Platform.db.commit().
    - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_period\_closing\_voucher.process\_period\_closing\_voucher.process\_individual\_date”, queue = “long”, timeout = timeout, is\_async = true, …).
- Otherwise.
  - Set ppcvd from qb.DocType(“Process Period Closing Voucher Detail”).
  - Set total\_no\_of\_dates from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.eq(docname)).run() at 0 at 0.
  - Set completed from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract(nested operand in the contrac … at 0.
  - If total\_no\_of\_dates equals completed.
    - Bind dependencies is\_job\_running.
    - Set job\_name from formatted text summarize\_{docname}.
    - If not is\_job\_running(job\_name).
      - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_period\_closing\_voucher.process\_period\_closing\_voucher.summarize\_and\_post …”, queue = “long”, timeout = timeout, is\_async = true, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Period Closing Voucher”, ptype = “write”, doc = docname, throw = true) · configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “pcv\_job\_timeout”) · service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.process\_period\_closing\_voucher.process\_period\_closing\_voucher.process\_individual\_date”, queue = “long”, timeout = timeout, is\_async = true, …), Platform.enqueue(method = “Enterprise.accounts.doctype.process\_period\_closing\_voucher.process\_period\_closing\_voucher.summarize\_and\_post …”, queue = “long”, timeout = timeout, is\_async = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L847)

<a id="op-0e7abe26679f57"></a>
### Make dict json compliant

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_make_mapping_structured_data_compliant`

**Inputs** dimension\_wise\_balance.

**Declared result** dict.

**Explicit results** converted\_dict.

**Local steps**

- Set converted\_dict from mapping().
- For each tuple(k, v) in dimension\_wise\_balance.items().
  - Set str\_key from list of str(x) for x drawn from k.
    - Draw x from k.
  - Set str\_key from “,”.join(str\_key).
  - Set converted\_dict at str\_key from v.
- Return converted\_dict.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L5026) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L835)

<a id="op-e3ccb24ed51ed3"></a>
### Get consolidated gles

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_consolidated_general_ledger_entries`

**Inputs** balances, report\_type.

**Declared result** list.

**Explicit results** gl\_entries.

**Local steps**

- Set gl\_entries from list().
- For each x in balances.
  - If x.report\_type equals report\_type.
    - Set closing\_balances from list of Platform.\_dict(gle) for gle drawn from Platform.json.loads(x.closing\_balance).
      - Draw gle from Platform.json.loads(x.closing\_balance).
    - Evaluate gl\_entries.extend(closing\_balances).
- Return gl\_entries.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L5206) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L827)

<a id="op-202806ad82f9ec"></a>
### Get gl entries

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_general_ledger_entries`

**Inputs** docname.

**Record and data access** resolve a document from “Process Period Closing Voucher” via get\_doc · resolve a document from “Period Closing Voucher” via get\_doc.

**State and service calls** request set\_value on “Process Period Closing Voucher”.

**Explicit results** tuple(pl\_accounts\_reverse\_gle, closing\_account\_gle).

**Local steps**

- Set ppcv from Platform.get\_doc(“Process Period Closing Voucher”, docname).
- Set gl\_entries from get\_consolidated\_gles(ppcv.normal\_balances, “Profit and Loss”).
- Set pl\_dimension\_wise\_acc\_balance from build\_dimension\_wise\_balance\_dict(gl\_entries).
- Set json\_dict from make\_dict\_json\_compliant(pl\_dimension\_wise\_acc\_balance).
- Evaluate Platform.db.set\_value(“Process Period Closing Voucher”, docname, “p\_l\_closing\_balance”, Platform.json.dumps(json\_dict)).
- Set pcv from Platform.get\_doc(“Period Closing Voucher”, ppcv.parent\_pcv).
- Set pl\_accounts\_reverse\_gle from list().
- Set closing\_account\_gle from list().
- For each tuple(dimensions, account\_balances) in pl\_dimension\_wise\_acc\_balance.items().
  - For each tuple(acc, balances) in account\_balances.items().
    - Set balance\_in\_company\_currency from (flt(balances.debit) − flt(balances.credit)).
    - If balance\_in\_company\_currency.
      - Evaluate pl\_accounts\_reverse\_gle.append(get\_gle\_for\_pl\_account(pcv, acc, balances, dimensions)).
  - Evaluate closing\_account\_gle.append(get\_gle\_for\_closing\_account(pcv, account\_balances at “balances”, dimensions)).
- Return tuple(pl\_accounts\_reverse\_gle, closing\_account\_gle).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L5401) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L830)

<a id="op-524396ece22ff7"></a>
### Calculate balance sheet balance

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_calculate_balance_sheet_balance`

**Inputs** docname.

**Record and data access** resolve a document from “Process Period Closing Voucher” via get\_doc.

**State and service calls** request set\_value on “Process Period Closing Voucher”.

**Explicit results** bs\_dimension\_wise\_acc\_balance.

**Local steps**

- Set ppcv from Platform.get\_doc(“Process Period Closing Voucher”, docname).
- Set gl\_entries from get\_consolidated\_gles((ppcv.normal\_balances + ppcv.z\_opening\_balances), “Balance Sheet”).
- Set bs\_dimension\_wise\_acc\_balance from build\_dimension\_wise\_balance\_dict(gl\_entries).
- Set json\_dict from make\_dict\_json\_compliant(bs\_dimension\_wise\_acc\_balance).
- Evaluate Platform.db.set\_value(“Process Period Closing Voucher”, docname, “bs\_closing\_balance”, Platform.json.dumps(json\_dict)).
- Return bs\_dimension\_wise\_acc\_balance.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L5952) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L822)

<a id="op-67ec9ca6477c81"></a>
### Get p l closing entries

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_p_l_closing_entries`

**Inputs** pl\_gles, pcv.

**Explicit results** pl\_closing\_entries.

**Local steps**

- Set pl\_closing\_entries from copy.deepcopy(pl\_gles).
- For each d in pl\_gles.
  - Set gle\_copy from copy.deepcopy(d).
  - Set gle\_copy.debit from d.credit.
  - Set gle\_copy.credit from d.debit.
  - Set gle\_copy.debit\_in\_account\_currency from d.credit\_in\_account\_currency.
  - Set gle\_copy.credit\_in\_account\_currency from d.debit\_in\_account\_currency.
  - Set gle\_copy.is\_period\_closing\_voucher\_entry from 0.
  - Set gle\_copy.period\_closing\_voucher from pcv.name.
  - Evaluate pl\_closing\_entries.append(gle\_copy).
- Return pl\_closing\_entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L6199) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L833)

<a id="op-12c3c558e9e995"></a>
### Get bs closing entries

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_balance_sheet_closing_entries`

**Inputs** dimension\_wise\_balance, pcv.

**Explicit results** closing\_entries.

**Local steps**

- Set closing\_entries from list().
- For each tuple(dimensions, account\_balances) in dimension\_wise\_balance.items().
  - For each tuple(acc, balances) in account\_balances.items().
    - Set balance\_in\_company\_currency from (flt(balances.debit) − flt(balances.credit)).
    - If (acc differs from “balances” and balance\_in\_company\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in acc differs from “balances” → balance\_in\_company\_currency.
      - Evaluate closing\_entries.append(get\_closing\_entry(pcv, acc, balances, dimensions)).
- Return closing\_entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L6463) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L824)

<a id="op-22400c8ff804e6"></a>
### Get closing account closing entry

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_closing_account_closing_entry`

**Inputs** closing\_account\_gle, pcv.

**Explicit results** closing\_entries\_for\_closing\_account.

**Local steps**

- Set closing\_entries\_for\_closing\_account from copy.deepcopy(closing\_account\_gle).
- For each d in closing\_entries\_for\_closing\_account.
  - Set d.period\_closing\_voucher from pcv.name.
- Return closing\_entries\_for\_closing\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0140.json#L6730) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L825)

<a id="op-f021ed4dded7d6"></a>
### Summarize and post ledger entries

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_summarize_and_post_ledger_entries`

**Inputs** docname.

**Record and data access** resolve a document from “Process Period Closing Voucher” via get\_doc · resolve a document from “Period Closing Voucher” via get\_doc.

**State and service calls** request set\_value on “Period Closing Voucher” · request set\_value on “Process Period Closing Voucher”.

**Explicit results** no value.

**Local steps**

- Set ppcv from Platform.get\_doc(“Process Period Closing Voucher”, docname, for\_update = true).
- If not ppcv.validate\_processing(list(“Running”)).
  - Return no value.
- Set pcv from Platform.get\_doc(“Period Closing Voucher”, ppcv.parent\_pcv).
- Set tuple(pl\_accounts\_reverse\_gle, closing\_account\_gle) from get\_gl\_entries(docname).
- Set gl\_entries from (pl\_accounts\_reverse\_gle + closing\_account\_gle).
- Bind dependencies make\_gl\_entries.
- If gl\_entries.
  - Evaluate make\_gl\_entries(gl\_entries, merge\_entries = false).
- Set bs\_dimension\_wise\_acc\_balance from calculate\_balance\_sheet\_balance(docname).
- Set pl\_closing\_entries from get\_p\_l\_closing\_entries(pl\_accounts\_reverse\_gle, pcv).
- Set bs\_closing\_entries from get\_bs\_closing\_entries(bs\_dimension\_wise\_acc\_balance, pcv).
- Set closing\_entries\_for\_closing\_account from get\_closing\_account\_closing\_entry(closing\_account\_gle, pcv).
- Set closing\_entries from ((pl\_closing\_entries + bs\_closing\_entries) + closing\_entries\_for\_closing\_account).
- Evaluate make\_closing\_entries(closing\_entries, pcv.name, pcv.company, pcv.period\_end\_date).
- Evaluate Platform.db.set\_value(“Period Closing Voucher”, pcv.name, “gle\_processing\_status”, “Completed”).
- Evaluate Platform.db.set\_value(“Process Period Closing Voucher”, docname, “status”, “Completed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L849)

<a id="op-84e708e1183569"></a>
### Get closing entry

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_closing_entry`

**Inputs** pcv, account, balances, dimensions.

**Explicit results** closing\_entry.

**Local steps**

- Set closing\_entry from Platform.\_dict(mapping(“company” → pcv.company, “closing\_date” → pcv.period\_end\_date, “period\_closing\_voucher” → pcv.name, “account” → account, …)).
- Evaluate update\_default\_dimensions(get\_dimensions(), closing\_entry, dimensions).
- Return closing\_entry.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0141.json#L572) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L826)

<a id="op-e09d496639f2e7"></a>
### Get dimensions

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_dimensions`

**Inputs** no declared parameters.

**Explicit results** dimensions.

**Local steps**

- Bind dependencies get\_accounting\_dimensions.
- Set default\_dimensions from list(“cost\_center”, “finance\_book”, “project”).
- Set dimensions from (default\_dimensions + get\_accounting\_dimensions()).
- Return dimensions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0141.json#L939) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L829)

<a id="op-c4e8d413de5b21"></a>
### Get dimension key

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_get_dimension_key`

**Inputs** res.

**Explicit results** tuple(list of res.get(dimension) for dimension drawn from get\_dimensions()).

**Local steps**

- Return tuple(list of res.get(dimension) for dimension drawn from get\_dimensions()).
  - Draw dimension from get\_dimensions().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0141.json#L1048) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L828)

<a id="op-c13007c03f43e8"></a>
### Build dimension wise balance dict

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_build_dimension_wise_balance_mapping`

**Inputs** gl\_entries.

**Explicit results** dimension\_balances.

**Local steps**

- Set dimension\_balances from Platform.\_dict().
- For each x in gl\_entries.
  - Set dimension\_key from get\_dimension\_key(x).
  - Evaluate dimension\_balances.setdefault(dimension\_key, Platform.\_dict()).setdefault(x.account, Platform.\_dict(mapping(“debit\_in\_account\_currency” → 0, “credit\_in\_account\_currency” → 0, “debit” → 0, “credit” → 0, …))).
  - Update dimension\_balances at dimension\_key at x.account.debit\_in\_account\_currency using + flt(x.debit\_in\_account\_currency).
  - Update dimension\_balances at dimension\_key at x.account.credit\_in\_account\_currency using + flt(x.credit\_in\_account\_currency).
  - Update dimension\_balances at dimension\_key at x.account.debit using + flt(x.debit).
  - Update dimension\_balances at dimension\_key at x.account.credit using + flt(x.credit).
  - Evaluate dimension\_balances at dimension\_key.setdefault(“balances”, Platform.\_dict(mapping(“balance\_in\_account\_currency” → 0, “balance\_in\_company\_currency” → 0))).
  - Set balance\_in\_account\_currency from (flt(x.debit\_in\_account\_currency) − flt(x.credit\_in\_account\_currency)).
  - Set balance\_in\_company\_currency from (flt(x.debit) − flt(x.credit)).
  - Update dimension\_balances at dimension\_key at “balances”.balance\_in\_account\_currency using + balance\_in\_account\_currency.
  - Update dimension\_balances at dimension\_key at “balances”.balance\_in\_company\_currency using + balance\_in\_company\_currency.
- Return dimension\_balances.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0141.json#L1142) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L821)

<a id="op-6746e153ee2ca9"></a>
### Process individual date

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_individual_date`

**Inputs** docname, row\_name, date, report\_type, parentfield.

**Record and data access** read “Process Period Closing Voucher Detail” via get\_value · read “Process Period Closing Voucher” via get\_value · read “Period Closing Voucher” via get\_value · read “Account” via get\_all.

**State and service calls** request set\_value on “Process Period Closing Voucher Detail” · commit.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_lazy\_doc(“Process Period Closing Voucher”, docname).validate\_processing(list(“Running”)).
  - Return no value.
- Set current\_date\_status from Platform.db.get\_value(“Process Period Closing Voucher Detail”, row\_name, “status”).
- If current\_date\_status differs from “Running”.
  - Return no value.
- Set pcv\_name from Platform.db.get\_value(“Process Period Closing Voucher”, docname, “parent\_pcv”).
- Set company from Platform.db.get\_value(“Period Closing Voucher”, pcv\_name, “company”).
- Set dimensions from get\_dimensions().
- Set accounts from Platform.db.get\_all(“Account”, filters = mapping(“company” → company, “report\_type” → report\_type), pluck = “name”).
- Set gle from qb.DocType(“GL Entry”).
- Set query from qb.from\_(gle).select(gle.account).
- For each dim in dimensions.
  - Set query from query.select(gle at dim).
- Set query from query.select(Sum(nested operand in the contract.debit).as\_(“debit”), Sum(nested operand in the contract.credit).as\_(“credit”), Sum(nested operand in the contract.debit\_in\_account\_currency).as\_(“debit\_in\_ac ….
- If parentfield equals “z\_opening\_balances”.
  - Set query from query.where(gle.is\_opening.eq(“Yes”)).
- Otherwise.
  - Set query from query.where(gle.is\_opening.eq(“No”)).
- Set query from query.groupby(gle.account).
- For each dim in dimensions.
  - Set query from query.groupby(gle at dim).
- Set res from query.run(as\_dict = true).
- Evaluate Platform.db.set\_value(“Process Period Closing Voucher Detail”, row\_name, “closing\_balance”, Platform.json.dumps(res)).
- Evaluate Platform.db.set\_value(“Process Period Closing Voucher Detail”, row\_name, “status”, “Completed”).
- If not Platform.in\_test.
  - Evaluate Platform.db.commit().
- Evaluate schedule\_next\_date(docname).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L837)

## Record · Process period closing voucher detail

[Record definition](../../../../data/record-types/process_period_closing_voucher_detail.json)

<a id="op-4115c32f67f359"></a>
### On doctype update

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_detail_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Process Period Closing Voucher Detail”.

**Local steps**

- Evaluate Platform.db.add\_index(“Process Period Closing Voucher Detail”, list(“parent”, “status”, “parentfield”, “idx”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0141.json#L6324) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L851)

## Record · Process statement of accounts

[Record definition](../../../../data/record-types/process_statement_of_accounts.json)

<a id="op-d3d51fe3d011a4"></a>
### Process Statement Of Accounts.validate

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_process_statement_of_accounts_validate`

**Inputs** self.

**Record and data access** read “Print Format” via get\_value.

**Explicit failure paths** validation helper — translated “Customers not selected.” · validation helper.

**Local steps**

- Evaluate self.validate\_account().
- Evaluate self.validate\_company\_for\_table(“Cost Center”).
- Evaluate self.validate\_company\_for\_table(“Project”).
- If not self.subject.
  - Set self.subject from “Statement Of Accounts for {{ customer.customer\_name }}”.
- If not self.body.
  - If self.report equals “General Ledger”.
    - Set body\_str from “ from {{ doc.from\_date }} to {{ doc.to\_date }}.”.
  - Otherwise.
    - Set body\_str from “ until {{ doc.posting\_date }}.”.
  - Set self.body from (“Hello {{ customer.customer\_name }},&lt;br&gt;PFA your Statement Of Accounts” + body\_str).
- If not self.pdf\_name.
  - Set self.pdf\_name from “{{ customer.customer\_name }}”.
- Evaluate validate\_template(self.subject, restrict\_globals = true).
- Evaluate validate\_template(self.body, restrict\_globals = true).
- Evaluate validate\_template(self.pdf\_name, restrict\_globals = true).
- If not self.customers.
  - Call the validation error handler Platform.throw(translated “Customers not selected.”).
- If (self.enable\_auto\_email and self.start\_date and (self.has\_value\_changed(“start\_date”) or self.has\_value\_changed(“enable\_auto\_email”) or self.has\_value\_changed(“report”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_auto\_email → self.start\_date → (self.has\_value\_changed(“start\_date”) or self.has\_value\_changed(“enable\_auto\_email”) or self.has\_value\_changed(“report”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“start\_date”) → self.has\_value\_changed(“enable\_auto\_email”) → self.has\_value\_changed(“report”).
  - Set scheduled\_date from self.start\_date.
  - If (not self.has\_value\_changed(“start\_date”) and not self.has\_value\_changed(“enable\_auto\_email”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_value\_changed(“start\_date”) → not self.has\_value\_changed(“enable\_auto\_email”).
    - Set scheduled\_date from self.get\_value\_before\_save(“posting\_date” when self.report equals “General Ledger”, otherwise “to\_date”).
      - Value choice on self.report equals “General Ledger” — true gives “posting\_date”, false gives “to\_date”.
  - If self.report equals “General Ledger”.
    - Set self.to\_date from scheduled\_date.
  - Otherwise.
    - Set self.posting\_date from scheduled\_date.
- If (self.enable\_auto\_email and self.report equals “General Ledger” and self.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_auto\_email → self.report equals “General Ledger” → self.to\_date.
  - Set self.from\_date from add\_months(self.to\_date, (negative 1 × self.filter\_duration)).
- If self.print\_format.
  - Set pf from Platform.db.get\_value(“Print Format”, self.print\_format, list(“print\_format\_type”, “print\_format\_for”, “report”, “disabled”), as\_dict = true).
  - If not pf.
    - Call the validation error handler Platform.throw(title = translated “Invalid Print Format”, msg = translated “Selected Print Format does not exist.”).
  - If pf.print\_format\_type differs from “Jinja”.
    - Call the validation error handler Platform.throw(title = translated “Invalid Print Format”, msg = translated “Print Format Type should be Jinja.”).
  - If (pf.print\_format\_for differs from “Report” or pf.report differs from self.report or pf.disabled).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pf.print\_format\_for differs from “Report” → pf.report differs from self.report → pf.disabled.
    - Call the validation error handler Platform.throw(title = translated “Invalid Print Format”, msg = translated “Print Format must be an enabled Report Print Format matching the selected Report.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account](operations-089.md#op-18f59945060c60), [validate company for table](operations-089.md#op-aa689d06a25347).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L872)

<a id="op-18f59945060c60"></a>
### Process Statement Of Accounts.validate account

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_process_statement_of_accounts_validate_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Account {0} doesn't belong to Company {1}”.format(Platform.bold(self.account), Platform.bold(self.company)).

**Local steps**

- If not self.account.
  - Return no value.
- If self.company differs from Platform.get\_cached\_value(“Account”, self.account, “company”).
  - Call the validation error handler Platform.throw(translated “Account {0} doesn't belong to Company {1}”.format(Platform.bold(self.account), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0142.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L873)

<a id="op-aa689d06a25347"></a>
### Process Statement Of Accounts.validate company for table

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_process_statement_of_accounts_validate_company_for_table`

**Inputs** self, doctype.

**Record and data access** read doctype via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- Set field from Platform.scrub(doctype).
- If not self.get(field).
  - Return no value.
- Set fieldname from (field + “\_name”).
- Set values from set(generator of d.get(fieldname) for d drawn from self.get(field)).
  - Draw d from self.get(field).
- Set invalid\_values from Platform.db.get\_all(doctype, filters = mapping(“name” → list(“in”, values), “company” → list(“!=”, self.company)), pluck = “name”).
- If invalid\_values.
  - Set msg from translated text in the contract.format(doctype, Platform.bold(self.company)).
  - Update msg using + ((text in the contract + empty text.join(generator of nested operand in the contract(nested operand in the contract).format(nested operand in the contract.bold(row)) for row drawn from invalid\_values)) + “&lt;/ul&gt;”).
    - Draw row from invalid\_values.
  - Call the validation error handler Platform.throw(translated msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L874)
