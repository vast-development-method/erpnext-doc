# Accounting and settlement · operations 97

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Repost accounting ledger

[Record definition](../../../../data/record-types/repost_accounting_ledger.json)

<a id="op-d293cb7f2f7552"></a>
### Repost Accounting Ledger.validate vouchers are submitted

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_validate_vouchers_are_submitted`

**Inputs** self.

**Record and data access** read key via get\_all.

**Explicit failure paths** validation helper — translated “The following vouchers are not submitted: {0}”.format(comma\_and(non\_submitted\_vouchers, add\_quotes = true)).

**Local steps**

- Set voucher\_type\_wise\_map from mapping().
- For each d in self.vouchers.
  - Evaluate voucher\_type\_wise\_map.setdefault(d.voucher\_type, list()).
  - Evaluate voucher\_type\_wise\_map at d.voucher\_type.append(d.voucher\_no).
- Set non\_submitted\_vouchers from list().
- For each key in voucher\_type\_wise\_map.keys().
  - Evaluate non\_submitted\_vouchers.extend(Platform.get\_all(key, filters = mapping(“name” → list(“in”, voucher\_type\_wise\_map at key), “docstatus” → list(“!=”, 1)), pluck = “name”)).
- If non\_submitted\_vouchers.
  - Call the validation error handler Platform.throw(translated “The following vouchers are not submitted: {0}”.format(comma\_and(non\_submitted\_vouchers, add\_quotes = true))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L6135) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1089)

<a id="op-5bcfe63c1708da"></a>
### Repost Accounting Ledger.on discard

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L6520) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L945) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1079)

<a id="op-6819d5476eb119"></a>
### Repost Accounting Ledger.get existing ledger entries

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_get_existing_ledger_entries`

**Inputs** self.

**Local steps**

- Set vouchers from list of x.voucher\_no for x drawn from self.vouchers.
  - Draw x from self.vouchers.
- Set gl from qb.DocType(“GL Entry”).
- Set existing\_gles from nested operand in the contract(nested operand in the contract).select(gl.star).where((nested operand in the contract.voucher\_no.isin(vouchers) bitwise and gl.is\_cancelled equals 0)).run(as\_dict = true).
- Set self.gles from Platform.\_dict(mapping()).
- For each gle in existing\_gles.
  - Evaluate nested operand in the contract.gles.setdefault(tuple(nested operand in the contract.voucher\_type, nested operand in the contract.voucher\_no), nested operand in the contract.\_dict(mapping())).setdefault(“ex ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L6583) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1076)

<a id="op-89824c8c64805d"></a>
### Repost Accounting Ledger.generate preview data

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_generate_preview_data`

**Inputs** self.

**Record and data access** resolve a document from x.voucher\_type via get\_doc.

**Local steps**

- Set Platform.flags.through\_repost\_accounting\_ledger from true.
- Set self.gl\_entries from list().
- Evaluate self.get\_existing\_ledger\_entries().
- For each x in self.vouchers.
  - Set doc from Platform.get\_doc(x.voucher\_type, x.voucher\_no).
  - If doc.doctype belongs to list(“Payment Entry”, “Journal Entry”).
    - Set gle\_map from doc.build\_gl\_map().
  - Otherwise.
    - If doc.doctype equals “Purchase Receipt”.
      - Set inventory\_account\_map from doc.get\_inventory\_account\_map().
      - Set gle\_map from doc.get\_gl\_entries(inventory\_account\_map).
    - Otherwise.
      - Set gle\_map from doc.get\_gl\_entries().
  - Set old\_entries from self.gles.get(tuple(x.voucher\_type, x.voucher\_no)).
  - If old\_entries.
    - Evaluate self.gl\_entries.extend(old\_entries.existing).
  - Evaluate self.gl\_entries.extend(gle\_map).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing ledger entries](operations-097.md#op-6819d5476eb119).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1075)

<a id="op-d92f586e480128"></a>
### Repost Accounting Ledger.generate preview

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_generate_preview`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Add vouchers to generate preview.”.

**Explicit results** no value · rendered\_page.

**Local steps**

- Bind dependencies get\_gl\_columns.
- If not self.vouchers.
  - Evaluate Platform.msgprint(translated “Add vouchers to generate preview.”).
  - Return no value.
- Set gl\_columns from list().
- Set gl\_data from list().
- Evaluate self.generate\_preview\_data().
- If self.gl\_entries.
  - Set filters from mapping(“company” → self.company, “include\_dimensions” → 1).
  - For each x in get\_gl\_columns(filters).
    - If x at “fieldname” equals “gl\_entry”.
      - Set x at “fieldname” from “name”.
    - Evaluate gl\_columns.append(x).
  - Set gl\_data from self.gl\_entries.
- Set rendered\_page from Platform.render\_template(“Enterprise/accounts/doctype/repost\_accounting\_ledger/repost\_accounting\_ledger.html”, mapping(“gl\_columns” → gl\_columns, “gl\_data” → gl\_data)).
- Return rendered\_page.

**Methods declared on this owner** [generate preview data](operations-097.md#op-89824c8c64805d).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L451) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1074)

<a id="op-e2a74ca2acbf79"></a>
### Repost Accounting Ledger.on submit

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.start\_repost().

If control reaches the end, it returns no value.

**Methods declared on this owner** [start repost](operations-097.md#op-bfcac01cbc5ac0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L875) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1080)

<a id="op-515ea022fe8142"></a>
### Repost Accounting Ledger.before cancel

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.\_raise\_error\_if\_reposting\_in\_progress().

If control reaches the end, it returns no value.

**Methods declared on this owner** [raise error if reposting in progress](operations-097.md#op-b2b26fc2816740).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L926) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L939) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1073)

<a id="op-7701b5dc485942"></a>
### Repost Accounting Ledger.on cancel

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L977) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L944) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1078)

<a id="op-b2b26fc2816740"></a>
### Repost Accounting Ledger.raise error if reposting in progress

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_raise_error_if_reposting_in_progress`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Reposting is still in progress in background.”.

**Local steps**

- If (self.scheduled\_job and is\_job\_enqueued(\_repost\_job\_id(self.name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.scheduled\_job → is\_job\_enqueued(\_repost\_job\_id(self.name)).
  - Call the validation error handler Platform.throw(translated “Reposting is still in progress in background.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L1040) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1081)

<a id="op-bfcac01cbc5ac0"></a>
### Repost Accounting Ledger.start repost

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_start_repost`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read self.doctype via get\_value.

**State and service calls** msgprint with translated “Scheduler is inactive. Reposting will only run once background jobs are processed.” · call db\_set on self · msgprint with translated “Repost has started in the background”.

**Explicit failure paths** validation helper — translated “Reposting can be started only for submitted document.” · validation helper — translated “Reposting cannot be started when status is {0}.”.format(status).

**Local steps**

- <a id="op-bfcac01cbc5ac0-guard-2"></a>If self.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Reposting can be started only for submitted document.”).
- Set status from Platform.db.get\_value(self.doctype, self.name, “status”, for\_update = true).
- If status belongs to tuple(“Completed”, “Cancelled”).
  - Call the validation error handler Platform.throw(translated “Reposting cannot be started when status is {0}.”.format(status)).
- Evaluate self.\_raise\_error\_if\_reposting\_in\_progress().
- Evaluate self.check\_permission(“write”).
- If is\_scheduler\_inactive().
  - Evaluate Platform.msgprint(translated “Scheduler is inactive. Reposting will only run once background jobs are processed.”, alert = true, indicator = “orange”).
- Evaluate self.db\_set(mapping(“status” → “Queued”, “scheduled\_job” → create\_job\_id(\_repost\_job\_id(self.name)))).
- Evaluate \_enqueue\_repost(self.name).
- Evaluate Platform.msgprint(translated “Repost has started in the background”, alert = true, indicator = “blue”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Reposting can be started only for submitted document.”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-bfcac01cbc5ac0-guard-2)

**Methods declared on this owner** [raise error if reposting in progress](operations-097.md#op-b2b26fc2816740).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L948) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1082)

<a id="op-8adcbaf2a0e29d"></a>
### Repost job id

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_job_identifier`

**Inputs** repost\_doc\_name.

**Declared result** str.

**Explicit results** formatted text repost\_accounting\_ledger::{repost\_doc\_name}.

**Local steps**

- Return formatted text repost\_accounting\_ledger::{repost\_doc\_name}.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L1734) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1092)

<a id="op-deb0fa22c745ce"></a>
### Enqueue repost

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_enqueue_repost`

**Inputs** repost\_doc\_name.

**Declared result** no value.

**State and service calls** enqueue.

**Local steps**

- Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.repost\_accounting\_ledger.repost\_accounting\_ledger.repost”, repost\_doc\_name = repost\_doc\_name, commit = not Platform.in\_test, queue = “long”, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.repost\_accounting\_ledger.repost\_accounting\_ledger.repost”, repost\_doc\_name = repost\_doc\_name, commit = not Platform.in\_test, queue = “long”, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L1794) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1067)

<a id="op-b9645cd8cd1b94"></a>
### Lock vouchers

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_dependency_lock_vouchers`

**Inputs** vouchers.

**Declared result** dict.

**Record and data access** resolve a document from x.voucher\_type via get\_doc.

**Explicit results** locked\_docs.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set locked\_docs from mapping().
- Attempt the following.
  - For each x in vouchers.
    - Set doc from Platform.get\_doc(x.voucher\_type, x.voucher\_no).
    - Evaluate doc.lock().
    - Set locked\_docs at tuple(x.voucher\_type, x.voucher\_no) from doc.
- On failure (Exception).
  - For each doc in locked\_docs.values().
    - Evaluate doc.unlock().
  - Propagate the active failure.
- Return locked\_docs.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L2018) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1065)

<a id="op-5adef84c868c5b"></a>
### Repost

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost`

**Inputs** repost\_doc\_name, commit = true.

**Record and data access** resolve a document from “Repost Accounting Ledger” via get\_doc.

**State and service calls** call db\_set on repost\_doc · savepoint · call db\_set on x · rollback · commit.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies \_delete\_accounting\_ledger\_entries, \_delete\_adv\_pl\_entries.
- Set Platform.flags.through\_repost\_accounting\_ledger from true.
- Set repost\_doc from Platform.get\_doc(“Repost Accounting Ledger”, repost\_doc\_name).
- Set locked\_docs from mapping().
- Attempt the following.
  - Evaluate repost\_doc.validate\_repost\_preconditions().
  - Set pending from list of x for x drawn from repost\_doc.vouchers where x.status does not belong to HANDLED\_VOUCHER\_STATUSES.
    - Draw x from repost\_doc.vouchers, keep a combination only if (x.status does not belong to HANDLED\_VOUCHER\_STATUSES).
  - Set locked\_docs from \_lock\_vouchers(pending).
  - Evaluate repost\_doc.db\_set(“status”, “In Progress”, commit = commit).
  - For each tuple(position, x) in enumerate(pending, start = 1).
    - Evaluate Platform.publish\_progress(((position × 100) ÷ len(pending)), doctype = repost\_doc.doctype, docname = repost\_doc.name, description = translated “Reposting {0} {1}”.format(x.voucher\_type, x.voucher\_no)).
    - Set save\_point from “reposting”.
    - Evaluate Platform.db.savepoint(save\_point = save\_point).
    - Attempt the following.
      - Set doc from locked\_docs at tuple(x.voucher\_type, x.voucher\_no).
      - If doc.docstatus equals 2.
        - Evaluate x.db\_set(mapping(“status” → “Skipped”, “traceback” → empty text)).
        - Continue with the next iteration or loop test.
      - If repost\_doc.delete\_cancelled\_entries.
        - Evaluate \_delete\_accounting\_ledger\_entries(doc.doctype, doc.name).
        - Evaluate \_delete\_adv\_pl\_entries(doc.doctype, doc.name).
      - Evaluate \_repost\_vouchers(doc, repost\_doc.delete\_cancelled\_entries).
    - On failure (Exception).
      - Evaluate Platform.db.rollback(save\_point = save\_point).
      - Evaluate x.db\_set(mapping(“status” → “Failed”, “traceback” → Platform.get\_traceback())).
    - When the protected block completes normally.
      - Evaluate x.db\_set(mapping(“status” → “Reposted”, “traceback” → empty text)).
    - On exit, including pending return or failure.
      - If commit.
        - Evaluate Platform.db.commit().
- On failure (Exception).
  - If commit.
    - Evaluate Platform.db.rollback().
  - Evaluate \_record\_repost\_failure(repost\_doc, commit = commit).
  - Propagate the active failure.
- When the protected block completes normally.
  - Evaluate repost\_doc.db\_set(mapping(“status” → \_derive\_status(repost\_doc), “error\_log” → empty text), notify = true).
- On exit, including pending return or failure.
  - For each doc in locked\_docs.values().
    - Evaluate doc.unlock().
  - If commit.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L2257) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L938) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1072)

<a id="op-d4729ce197f9e1"></a>
### Derive status

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_derive_status`

**Inputs** repost\_doc.

**Declared result** str.

**Explicit results** “Completed” · “Failed” · “Partially Reposted”.

**Local steps**

- Set handled from sum(generator of 1 for voucher drawn from repost\_doc.vouchers where voucher.status belongs to HANDLED\_VOUCHER\_STATUSES).
  - Draw voucher from repost\_doc.vouchers, keep a combination only if (voucher.status belongs to HANDLED\_VOUCHER\_STATUSES).
- If handled equals len(repost\_doc.vouchers).
  - Return “Completed”.
- Otherwise.
  - If handled equals 0.
    - Return “Failed”.
- Return “Partially Reposted”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L3449) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L932) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1066)

<a id="op-ff297cefa67dd6"></a>
### Record repost failure

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_record_repost_failure`

**Inputs** repost\_doc, commit = false.

**Declared result** no value.

**State and service calls** request set\_value on repost\_doc.doctype · commit.

**Local steps**

- Set traceback from Platform.get\_traceback().
- Evaluate Platform.log\_error(title = translated “Unable to Repost Accounting Ledger”, reference\_doctype = repost\_doc.doctype, reference\_name = repost\_doc.name).
- Evaluate Platform.db.set\_value(repost\_doc.doctype, repost\_doc.name, mapping(“error\_log” → traceback, “status” → \_derive\_status(repost\_doc))).
- If commit.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L3632) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L937) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1071)

<a id="op-ec6e0dc284f6c1"></a>
### Repost vouchers

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_vouchers`

**Inputs** doc, delete\_cancelled\_entries.

**Local steps**

- If doc.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Evaluate \_repost\_invoices(doc, delete\_cancelled\_entries).
- Otherwise.
  - If doc.doctype equals “Purchase Receipt”.
    - Evaluate \_repost\_purchase\_receipt(doc, delete\_cancelled\_entries).
  - Otherwise.
    - If doc.doctype belongs to list(“Payment Entry”, “Journal Entry”).
      - Evaluate \_repost\_pe\_je(doc, delete\_cancelled\_entries).
    - Otherwise.
      - If doc.doctype belongs to Platform.get\_hooks(“repost\_allowed\_doctypes”).
        - Evaluate \_repost\_allowed\_hook\_doctypes(doc, delete\_cancelled\_entries).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“repost\_allowed\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L3893) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L961) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1095)

<a id="op-4eef0ef643da59"></a>
### Repost invoices

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_invoices`

**Inputs** invoice\_doc, delete\_cancelled\_entries.

**Local steps**

- If not delete\_cancelled\_entries.
  - Set invoice\_doc.docstatus from 2.
  - Evaluate invoice\_doc.make\_gl\_entries\_on\_cancel(from\_repost = true).
- Set invoice\_doc.docstatus from 1.
- If invoice\_doc.doctype equals “Sales Invoice”.
  - Evaluate invoice\_doc.force\_set\_against\_income\_account().
- Otherwise.
  - Evaluate invoice\_doc.force\_set\_against\_expense\_account().
- Evaluate invoice\_doc.make\_gl\_entries().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L4222) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1091)

<a id="op-d8257038dba8f6"></a>
### Repost purchase receipt

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_purchase_receipt`

**Inputs** receipt\_doc, delete\_cancelled\_entries.

**Local steps**

- If not delete\_cancelled\_entries.
  - Set receipt\_doc.docstatus from 2.
  - Evaluate receipt\_doc.make\_gl\_entries\_on\_cancel(from\_repost = true).
- Set receipt\_doc.docstatus from 1.
- Evaluate receipt\_doc.make\_gl\_entries(from\_repost = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L4422) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L960) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1094)

<a id="op-7c0d73ee558cf2"></a>
### Repost pe je

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_pe_je`

**Inputs** entry\_doc, delete\_cancelled\_entries.

**Local steps**

- If not delete\_cancelled\_entries.
  - Evaluate entry\_doc.make\_gl\_entries(cancel = 1).
- Evaluate entry\_doc.make\_gl\_entries().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L4564) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L959) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1093)

<a id="op-65a73473d20271"></a>
### Repost allowed hook doctypes

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_allowed_hook_record_types`

**Inputs** repost\_doc, delete\_cancelled\_entries.

**Local steps**

- Bind dependencies make\_reverse\_gl\_entries.
- If (hasattr(repost\_doc, “make\_gl\_entries”) and callable(repost\_doc.make\_gl\_entries)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(repost\_doc, “make\_gl\_entries”) → callable(repost\_doc.make\_gl\_entries).
  - If not delete\_cancelled\_entries.
    - If “cancel” belongs to inspect.getfullargspec(repost\_doc.make\_gl\_entries).args.
      - Evaluate repost\_doc.make\_gl\_entries(cancel = 1).
    - Otherwise.
      - Evaluate make\_reverse\_gl\_entries(voucher\_type = repost\_doc.doctype, voucher\_no = repost\_doc.name).
  - Evaluate repost\_doc.make\_gl\_entries().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L4661) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L956) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1090)

<a id="op-0bb37bf9a8bcdf"></a>
### Get allowed types from settings

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_get_allowed_types_from_settings`

**Inputs** child\_doc = false.

**Record and data access** read “Repost Allowed Types” via get\_all.

**Explicit results** result.

**Local steps**

- Set repost\_docs from list of x.document\_type for x drawn from Platform.db.get\_all(“Repost Allowed Types”, fields = list(“document\_type”), distinct = true).
  - Draw x from Platform.db.get\_all(“Repost Allowed Types”, fields = list(“document\_type”), distinct = true).
- Set result from repost\_docs.
- If (repost\_docs and child\_doc).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in repost\_docs → child\_doc.
  - Evaluate result.extend(get\_child\_docs(repost\_docs)).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L4938) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1068)

<a id="op-fa497b4589ee9c"></a>
### Get child docs

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_get_child_records`

**Inputs** doc.

**Declared result** list.

**Explicit results** child\_doc.

**Local steps**

- Set child\_doc from list().
- Set doc from get\_child\_tables\_of\_doctypes(doc).
- For each child\_list in doc.values().
  - For each child in child\_list.
    - If child.get(“child\_table”).
      - Evaluate child\_doc.append(child at “child\_table”).
- Return child\_doc.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L5145) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1069)

<a id="op-538457dfff7d9c"></a>
### Validate docs for deferred accounting

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_validate_records_for_deferred_accounting`

**Inputs** sales\_docs, purchase\_docs.

**Record and data access** read “Sales Invoice Item” via get\_all · read “Purchase Invoice Item” via get\_all.

**Explicit failure paths** validation helper — translated “Documents: {0} have deferred revenue/expense enabled for them. Cannot repost.”.format(Platform.bold(comma\_and(list of x at 0 for x drawn from (docs\_with\_deferred\_expense + docs\_with\_deferred\_revenue)))).

**Local steps**

- Set docs\_with\_deferred\_revenue from tuple().
- Set docs\_with\_deferred\_expense from tuple().
- If sales\_docs.
  - Set docs\_with\_deferred\_revenue from Platform.db.get\_all(“Sales Invoice Item”, filters = mapping(“parent” → list(“in”, sales\_docs), “docstatus” → 1, “enable\_deferred\_revenue” → true), fields = list(“parent”), as\_list = 1).
- If purchase\_docs.
  - Set docs\_with\_deferred\_expense from Platform.db.get\_all(“Purchase Invoice Item”, filters = mapping(“parent” → list(“in”, purchase\_docs), “docstatus” → 1, “enable\_deferred\_expense” → 1), fields = list(“parent”), as\_list = 1).
- If (docs\_with\_deferred\_revenue or docs\_with\_deferred\_expense).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in docs\_with\_deferred\_revenue → docs\_with\_deferred\_expense.
  - Call the validation error handler Platform.throw(translated “Documents: {0} have deferred revenue/expense enabled for them. Cannot repost.”.format(Platform.bold(comma\_and(list of x at 0 for x drawn from (docs\_with\_deferred\_expense + docs\_w ….
    - Draw x from (docs\_with\_deferred\_expense + docs\_with\_deferred\_revenue).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L962) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1096)
