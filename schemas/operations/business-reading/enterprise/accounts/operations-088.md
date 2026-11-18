# Accounting and settlement · operations 88

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Process payment reconciliation

[Record definition](../../../../data/record-types/process_payment_reconciliation.json)

<a id="op-eb8ef938286d2d"></a>
### Pause job for doc

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_pause_job_for_record`

**Inputs** docname = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Process Payment Reconciliation Log” via get\_value.

**State and service calls** request set\_value on “Process Payment Reconciliation” · request set\_value on “Process Payment Reconciliation Log”.

**Local steps**

- If docname.
  - Evaluate Platform.has\_permission(“Process Payment Reconciliation”, “write”, doc = docname, throw = true).
  - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, docname, “status”, “Paused”).
  - Set log from Platform.db.get\_value(“Process Payment Reconciliation Log”, filters = mapping(“process\_pr” → docname)).
  - If log.
    - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “status”, “Paused”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Payment Reconciliation”, “write”, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L1647) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L799)

<a id="op-e50d05d5184b5a"></a>
### Trigger job for doc

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_trigger_job_for_record`

**Inputs** docname = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Process Payment Reconciliation” via get\_value · read “Process Payment Reconciliation Log” via get\_value.

**State and service calls** request set\_value on “Process Payment Reconciliation” · enqueue · request set\_value on “Process Payment Reconciliation Log” · msgprint with translated “Scheduler is Inactive. Can't trigger job now.”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Auto Reconciliation of Payments has been disabled. Enable it through {0}”.format(get\_link\_to\_form(“Accounts Settings”, “Accounts Settings”)).

**Local steps**

- If not docname.
  - Return no value.
- Evaluate Platform.has\_permission(“Process Payment Reconciliation”, “write”, doc = docname, throw = true).
- If not Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”).
  - Call the validation error handler Platform.throw(translated “Auto Reconciliation of Payments has been disabled. Enable it through {0}”.format(get\_link\_to\_form(“Accounts Settings”, “Accounts Settings”))).
  - Return no value.
- If not is\_scheduler\_inactive().
  - If Platform.db.get\_value(“Process Payment Reconciliation”, docname, “status”) equals “Queued”.
    - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, docname, “status”, “Running”).
    - Set job\_name from formatted text start\_processing\_{docname}.
    - If not is\_job\_running(job\_name).
      - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile\_based\_on …”, queue = “long”, is\_async = true, job\_name = job\_name, …).
  - Otherwise.
    - If Platform.db.get\_value(“Process Payment Reconciliation”, docname, “status”) equals “Paused”.
      - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, docname, “status”, “Running”).
      - Set log from Platform.db.get\_value(“Process Payment Reconciliation Log”, filters = mapping(“process\_pr” → docname)).
      - If log.
        - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “status”, “Running”).
      - Set job\_name from formatted text start\_processing\_{docname}.
      - If not is\_job\_running(job\_name).
        - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile\_based\_on …”, queue = “long”, is\_async = true, job\_name = job\_name, …).
- Otherwise.
  - Evaluate Platform.msgprint(translated “Scheduler is Inactive. Can't trigger job now.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Payment Reconciliation”, “write”, doc = docname, throw = true) · configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”) · service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile\_based\_on …”, queue = “long”, is\_async = true, job\_name = job\_name, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L809)

<a id="op-5965ec6ee69f2f"></a>
### Trigger reconciliation for queued docs

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_trigger_reconciliation_for_queued_records`

**Inputs** no declared parameters.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Process Payment Reconciliation” via get\_all · resolve a document from “Process Payment Reconciliation” via get\_doc.

**State and service calls** msgprint with translated “Auto Reconciliation of Payments has been disabled. Enable it through {0}”.format(get\_link\_to\_form(“Accounts Settings”, “Accounts Settings”)) · msgprint with translated “Scheduler is Inactive. Can't trigger jobs now.”.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”).
  - Evaluate Platform.msgprint(translated “Auto Reconciliation of Payments has been disabled. Enable it through {0}”.format(get\_link\_to\_form(“Accounts Settings”, “Accounts Settings”))).
  - Return no value.
- If not is\_scheduler\_inactive().
  - Set all\_queued from Platform.db.get\_all(“Process Payment Reconciliation”, filters = mapping(“docstatus” → 1, “status” → “Queued”), order\_by = “creation desc”, as\_list = 1).
  - Set docs\_to\_trigger from list().
  - Set unique\_filters from set().
  - Set queue\_size from (Platform.get\_single\_value(“Accounts Settings”, “reconciliation\_queue\_size”) or 5).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“Accounts Settings”, “reconciliation\_queue\_size”) → 5.
  - Set fields from list(“company”, “party\_type”, “party”, “receivable\_payable\_account”, …).
  - Bind local operation get\_filters\_as\_tuple for subsequent calls.
  - For each x in all\_queued.
    - Set doc from Platform.get\_doc(“Process Payment Reconciliation”, x).
    - Set filters from get\_filters\_as\_tuple(fields, doc).
    - If filters does not belong to unique\_filters.
      - Evaluate unique\_filters.add(filters).
      - Evaluate docs\_to\_trigger.append(doc.name).
    - If len(docs\_to\_trigger) equals queue\_size.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - For each doc in docs\_to\_trigger.
    - Evaluate trigger\_job\_for\_doc(doc).
- Otherwise.
  - Evaluate Platform.msgprint(translated “Scheduler is Inactive. Can't trigger jobs now.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “auto\_reconcile\_payments”), Platform.get\_single\_value(“Accounts Settings”, “reconciliation\_queue\_size”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L3006) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L810)

<a id="op-577484740b6504"></a>
### Trigger reconciliation for queued docs.get filters as tuple

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_trigger_reconciliation_for_queued_records_get_filters_as_tuple`

**Inputs** fields, doc.

**Explicit results** tuple(generator of (doc.get(x) or empty text) for x drawn from fields).

**Local steps**

- Return tuple(generator of (doc.get(x) or empty text) for x drawn from fields).
  - Draw x from fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(x) → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0994.json#L4600) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L811)

<a id="op-1b46676554d97e"></a>
### Reconcile based on filters

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_reconcile_based_on_filters`

**Inputs** doc = no value.

**Declared result** no value.

**Record and data access** read “Process Payment Reconciliation Log” via get\_value · read “Process Payment Reconciliation Log” via get\_all.

**State and service calls** request new\_doc for “Process Payment Reconciliation Log” · call save on log · enqueue · request set\_value on “Process Payment Reconciliation”.

**Local steps**

- If doc.
  - Set log from Platform.db.get\_value(“Process Payment Reconciliation Log”, filters = mapping(“process\_pr” → doc)).
  - If not log.
    - Set log from Platform.new\_doc(“Process Payment Reconciliation Log”).
    - Set log.process\_pr from doc.
    - Set log.status from “Running”.
    - Set log from log.save(ignore\_permissions = true).
    - Set job\_name from formatted text process\_{doc}\_fetch\_and\_allocate.
    - If not is\_job\_running(job\_name).
      - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.fetch\_and\_allocate”, queue = “long”, timeout = “3600”, is\_async = true, …).
  - Otherwise.
    - Set res from Platform.get\_all(“Process Payment Reconciliation Log”, filters = mapping(“name” → log), fields = list(“allocated”, “reconciled”), as\_list = 1).
    - Set tuple(allocated, reconciled) from res at 0.
    - If not allocated.
      - Set job\_name from formatted text process\_\_{doc}\_fetch\_and\_allocate.
      - If not is\_job\_running(job\_name).
        - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.fetch\_and\_allocate”, queue = “long”, timeout = “3600”, is\_async = true, …).
    - Otherwise.
      - If not reconciled.
        - Set allocation from get\_next\_allocation(log).
        - If allocation.
          - Set reconcile\_job\_name from formatted text process\_{doc}\_reconcile\_allocation\_{allocation at 0.idx}\_{allocation at negative 1.idx}.
        - Otherwise.
          - Set reconcile\_job\_name from formatted text process\_{doc}\_reconcile.
        - If not is\_job\_running(reconcile\_job\_name).
          - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile”, queue = “long”, timeout = “3600”, is\_async = true, …).
      - Otherwise.
        - If reconciled.
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, doc, “status”, “Completed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.fetch\_and\_allocate”, queue = “long”, timeout = “3600”, is\_async = true, …), Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile”, queue = “long”, timeout = “3600”, is\_async = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L808)

<a id="op-760597012897d6"></a>
### Get next allocation

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_get_next_allocation`

**Inputs** log.

**Declared result** list.

**Record and data access** read “Process Payment Reconciliation Log Allocations” via get\_all.

**Explicit results** allocations · list().

**Local steps**

- If log.
  - Set allocations from list().
  - Set next from Platform.db.get\_all(“Process Payment Reconciliation Log Allocations”, filters = mapping(“parent” → log, “reconciled” → 0), fields = list(“reference\_type”, “reference\_name”), order\_by = “idx”, limit = 1).
  - If next.
    - Set allocations from Platform.db.get\_all(“Process Payment Reconciliation Log Allocations”, filters = mapping(“parent” → log, “reconciled” → 0, “reference\_type” → next at 0.reference\_type, “reference\_name” → next at 0.reference ….
  - Return allocations.
- Return list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L4968) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L794)

<a id="op-a4271a32681e86"></a>
### Fetch and allocate

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_fetch_and_allocate`

**Inputs** doc.

**Declared result** no value.

**Record and data access** read “Process Payment Reconciliation Log” via get\_value · resolve a document from “Process Payment Reconciliation Log” via get\_doc.

**State and service calls** call save on reconcile\_log · enqueue.

**Local steps**

- If doc.
  - Set log from Platform.db.get\_value(“Process Payment Reconciliation Log”, filters = mapping(“process\_pr” → doc)).
  - If log.
    - If not Platform.db.get\_value(“Process Payment Reconciliation Log”, log, “allocated”).
      - Set reconcile\_log from Platform.get\_doc(“Process Payment Reconciliation Log”, log).
      - Set pr from get\_pr\_instance(doc).
      - Evaluate pr.get\_unreconciled\_entries().
      - If (len(pr.invoices) &gt; 0 and len(pr.payments) &gt; 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(pr.invoices) &gt; 0 → len(pr.payments) &gt; 0.
        - Set invoices from list of x.as\_dict() for x drawn from pr.invoices.
          - Draw x from pr.invoices.
        - Set payments from list of x.as\_dict() for x drawn from pr.payments.
          - Draw x from pr.payments.
        - Evaluate pr.allocate\_entries(Platform.\_dict(mapping(“invoices” → invoices, “payments” → payments))).
        - For each x in pr.get(“allocation”).
          - Evaluate reconcile\_log.append(“allocations”, x.as\_dict().update(mapping(“parenttype” → “Process Payment Reconciliation Log”, “parent” → reconcile\_log.name, “name” → no value, “reconciled” → false))).
      - Set reconcile\_log.allocated from true.
      - Set reconcile\_log.total\_allocations from len(reconcile\_log.get(“allocations”)).
      - Set reconcile\_log.reconciled\_entries from 0.
      - Evaluate reconcile\_log.save(ignore\_permissions = true).
      - Set allocation from get\_next\_allocation(log).
      - If allocation.
        - Set reconcile\_job\_name from formatted text process\_{doc}\_reconcile\_allocation\_{allocation at 0.idx}\_{allocation at negative 1.idx}.
      - Otherwise.
        - Set reconcile\_job\_name from formatted text process\_{doc}\_reconcile.
      - If not is\_job\_running(reconcile\_job\_name).
        - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile”, queue = “long”, timeout = “3600”, is\_async = true, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile”, queue = “long”, timeout = “3600”, is\_async = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L793)

<a id="op-e5d1d39ebf7002"></a>
### Reconcile

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_reconcile`

**Inputs** doc = no value.

**Declared result** no value.

**Record and data access** read “Process Payment Reconciliation Log” via get\_value · read “Process Payment Reconciliation Log” via get\_all · resolve a document from allocations at 0.reference\_type via get\_doc · read “Process Payment Reconciliation Log Allocations” via count · read “Process Payment Reconciliation” via get\_value.

**State and service calls** call save on pe · request set\_value on “Process Payment Reconciliation Log” · rollback · request set\_value on “Process Payment Reconciliation” · enqueue.

**Local steps**

- If doc.
  - Set log from Platform.db.get\_value(“Process Payment Reconciliation Log”, filters = mapping(“process\_pr” → doc)).
  - If log.
    - Set res from Platform.get\_all(“Process Payment Reconciliation Log”, filters = mapping(“name” → log), fields = list(“reconciled\_entries”, “total\_allocations”), as\_list = 1, limit = 1).
    - Set tuple(reconciled\_entries, total\_allocations) from res at 0.
    - If reconciled\_entries differs from total\_allocations.
      - Attempt the following.
        - Set allocations from get\_next\_allocation(log).
        - Set pr from get\_pr\_instance(doc).
        - For each x in allocations.
          - Evaluate pr.append(“allocation”, x).
        - Evaluate pr.get\_nonreconciled\_payment\_entries().
        - Evaluate pr.get\_invoice\_entries(vouchers = list of Platform.\_dict(voucher\_type = x.invoice\_type, voucher\_no = x.invoice\_number) for x drawn from allocations).
          - Draw x from allocations.
        - Evaluate pr.validate\_allocation().
        - Set skip\_ref\_details\_update\_for\_pe from check\_multi\_currency(pr).
        - Evaluate pr.reconcile\_allocations(skip\_ref\_details\_update\_for\_pe = skip\_ref\_details\_update\_for\_pe).
        - If allocations at 0.reference\_type equals “Payment Entry”.
          - Set references from list of tuple(x.invoice\_type, x.invoice\_number) for x drawn from allocations.
            - Draw x from allocations.
          - Set pe from Platform.get\_doc(allocations at 0.reference\_type, allocations at 0.reference\_name).
          - Set pe.flags.ignore\_validate\_update\_after\_submit from true.
          - Evaluate pe.set\_missing\_ref\_details(update\_ref\_details\_only\_for = references).
          - Evaluate pe.save().
        - Set allocation\_names from list of x.name for x drawn from allocations.
          - Draw x from allocations.
        - Set ppa from qb.DocType(“Process Payment Reconciliation Log Allocations”).
        - Evaluate nested operand in the contract(nested operand in the contract).set(ppa.reconciled, true).where(ppa.name.isin(allocation\_names)).run().
        - Set reconciled\_count from Platform.db.count(“Process Payment Reconciliation Log Allocations”, filters = mapping(“parent” → log, “reconciled” → true)).
        - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “reconciled\_entries”, reconciled\_count).
      - On failure (Exception).
        - Evaluate Platform.db.rollback().
        - Set traceback from Platform.get\_traceback(with\_context = true).
        - If traceback.
          - Set message from (“Traceback: &lt;br&gt;” + traceback).
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “error\_log”, message).
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, doc, “error\_log”, message).
        - If (reconciled\_entries and total\_allocations and reconciled\_entries &lt; total\_allocations).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in reconciled\_entries → total\_allocations → reconciled\_entries &lt; total\_allocations.
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “status”, “Partially Reconciled”).
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, doc, “status”, “Partially Reconciled”).
        - Otherwise.
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “status”, “Failed”).
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, doc, “status”, “Failed”).
      - On exit, including pending return or failure.
        - If reconciled\_entries equals total\_allocations.
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “status”, “Reconciled”).
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “reconciled”, true).
          - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, doc, “status”, “Completed”).
        - Otherwise.
          - If Platform.db.get\_value(“Process Payment Reconciliation”, doc, “status”) differs from “Paused”.
            - Set allocation from get\_next\_allocation(log).
            - If allocation.
              - Set reconcile\_job\_name from formatted text process\_{doc}\_reconcile\_allocation\_{allocation at 0.idx}\_{allocation at negative 1.idx}.
            - Otherwise.
              - Set reconcile\_job\_name from formatted text process\_{doc}\_reconcile.
            - If not is\_job\_running(reconcile\_job\_name).
              - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile”, queue = “long”, timeout = “3600”, is\_async = true, …).
    - Otherwise.
      - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “status”, “Reconciled”).
      - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “reconciled”, true).
      - Evaluate Platform.db.set\_value(“Process Payment Reconciliation”, doc, “status”, “Completed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.process\_payment\_reconciliation.process\_payment\_reconciliation.reconcile”, queue = “long”, timeout = “3600”, is\_async = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L807)

<a id="op-c863650bb2c1f8"></a>
### Check multi currency

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_check_multi_currency`

**Inputs** pr\_doc.

**Explicit results** true · false.

**Local steps**

- Set GL from Platform.qb.DocType(“GL Entry”).
- Set Account from Platform.qb.DocType(“Account”).
- Bind local operation get\_account\_currency for subsequent calls.
- For each allocation in pr\_doc.allocation.
  - Set reference\_currency from get\_account\_currency(allocation.reference\_type, allocation.reference\_name).
  - Set invoice\_currency from get\_account\_currency(allocation.invoice\_type, allocation.invoice\_number).
  - If reference\_currency differs from invoice\_currency.
    - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L2094) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L791)

<a id="op-f551ef22706233"></a>
### Check multi currency.get account currency

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_check_multi_currency_get_account_currency`

**Inputs** voucher\_type, voucher\_no.

**Explicit results** currency at 0.account\_currency when currency, otherwise no value.

**Local steps**

- Set currency from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract(nested operand i ….
- Return currency at 0.account\_currency when currency, otherwise no value.
  - Value choice on currency — true gives currency at 0.account\_currency, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L2622) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L792)

<a id="op-8ee9be42f9cd67"></a>
### Is any doc running

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_is_any_record_running`

**Inputs** for\_filter = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Record and data access** read “Process Payment Reconciliation” via get\_value.

**Explicit results** running\_doc.

**Local steps**

- Set running\_doc from no value.
- If for\_filter.
  - If isinstance(for\_filter, str).
    - Set for\_filter from json.loads(for\_filter).
  - Set running\_doc from Platform.db.get\_value(“Process Payment Reconciliation”, filters = mapping(“docstatus” → 1, “status” → list(“in”, list(“Running”, “Paused”)), “company” → for\_filter.get(“company”), “party\_type” → for\_filter ….
- Otherwise.
  - Set running\_doc from Platform.db.get\_value(“Process Payment Reconciliation”, filters = mapping(“docstatus” → 1, “status” → “Running”)).
- Return running\_doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L797)

<a id="op-818a8323718828"></a>
### Get data

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_process_payment_reconciliation_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “process\_pr”, “transactions” → list(mapping(“label” → translated “Reconciliation Logs”, “items” → list(“Process Payment Reconciliation Log”)))).

**Local steps**

- Return mapping(“fieldname” → “process\_pr”, “transactions” → list(mapping(“label” → translated “Reconciliation Logs”, “items” → list(“Process Payment Reconciliation Log”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L3408) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L812)

## Record · Process period closing voucher

[Record definition](../../../../data/record-types/process_period_closing_voucher.json)

<a id="op-c945bf4f25fba2"></a>
### Process Period Closing Voucher.on discard

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L4966) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L842)

<a id="op-a03c925994b427"></a>
### Process Period Closing Voucher.validate

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_validate`

**Inputs** self.

**Record and data access** read self.doctype via get\_value.

**Explicit failure paths** validation helper — translated “A Process Period Closing Voucher already exists for {0}”.format(self.parent\_pcv).

**Local steps**

- Evaluate self.validate\_parent\_pcv().
- If Platform.db.get\_value(self.doctype, mapping(“parent\_pcv” → self.parent\_pcv, “docstatus” → list(“!=”, 2), “name” → list(“!=”, self.name)), for\_update = true).
  - Call the validation error handler Platform.throw(translated “A Process Period Closing Voucher already exists for {0}”.format(self.parent\_pcv)).
- Set self.status from “Queued”.
- Evaluate self.populate\_processing\_tables().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate parent pcv](operations-088.md#op-b7ccacbfefd39b), [populate processing tables](operations-088.md#op-9ea7875493c280).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L845)

<a id="op-b33995da12de1a"></a>
### Process Period Closing Voucher.validate processing

`operation_enterprise_binding_enterprise_accounts_doctype_process_period_closing_voucher_process_period_closing_voucher_processperiodclosingvoucher_validate_processing`

**Inputs** self, statuses.

**Explicit results** false · true.

**Explicit failure paths** validation helper — translated “Process Period Closing Voucher must be submitted before processing”.

**Local steps**

- <a id="op-b33995da12de1a-guard-2"></a>If self.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Process Period Closing Voucher must be submitted before processing”).
- If self.status does not belong to statuses.
  - Return false.
- Evaluate self.validate\_parent\_pcv().
- Return true.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Process Period Closing Voucher must be submitted before processing”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b33995da12de1a-guard-2)

**Methods declared on this owner** [validate parent pcv](operations-088.md#op-b7ccacbfefd39b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L930)

<a id="op-b7ccacbfefd39b"></a>
### Process Period Closing Voucher.validate parent pcv

`operation_enterprise_binding_enterprise_accounts_doctype_process_period_closing_voucher_process_period_closing_voucher_processperiodclosingvoucher_validate_parent_pcv`

**Inputs** self.

**Record and data access** resolve a document from “Period Closing Voucher” via get\_doc · read “GL Entry” via exists · read “Account Closing Balance” via exists.

**Explicit failure paths** validation helper — translated “Period Closing Voucher {0} must be submitted before processing”.format(pcv.name) · validation helper — translated “Period Closing Voucher {0} has already been processed”.format(pcv.name).

**Local steps**

- Set pcv from Platform.get\_doc(“Period Closing Voucher”, self.parent\_pcv).
- <a id="op-b7ccacbfefd39b-guard-3"></a>If pcv.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Period Closing Voucher {0} must be submitted before processing”.format(pcv.name)).
- If (pcv.gle\_processing\_status equals “Completed” or Platform.db.exists(“GL Entry”, mapping(“voucher\_type” → pcv.doctype, “voucher\_no” → pcv.name, “is\_cancelled” → 0)) or Platform.db.exists(“Account Closing Ba ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pcv.gle\_processing\_status equals “Completed” → Platform.db.exists(“GL Entry”, mapping(“voucher\_type” → pcv.doctype, “voucher\_no” → pcv.name, “is\_cancelled” → 0)) → Platform.db.exists(“Account Closing Balance”, mapping(“period\_closing\_voucher” → pcv.name)).
  - Call the validation error handler Platform.throw(translated “Period Closing Voucher {0} has already been processed”.format(pcv.name)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison pcv.docstatus differs from 1, pcv.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Period Closing Voucher {0} must be submitted before processing”.format(pcv.name). With pcv.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b7ccacbfefd39b-guard-3)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L929)

<a id="op-9ea7875493c280"></a>
### Process Period Closing Voucher.populate processing tables

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_populate_processing_tables`

**Inputs** self.

**Local steps**

- Evaluate self.generate\_pcv\_dates().
- Evaluate self.generate\_opening\_balances\_dates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate pcv dates](operations-088.md#op-a2f361b08b3674), [generate opening balances dates](operations-088.md#op-e4ec435711427c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L5097) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L844)

<a id="op-a502e54db967e1"></a>
### Process Period Closing Voucher.get dates

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_get_dates`

**Inputs** self, start, end.

**Explicit results** list of (start + timedelta(days = x)) for x drawn from range(((end − start).days + 1)).

**Local steps**

- Return list of (start + timedelta(days = x)) for x drawn from range(((end − start).days + 1)).
  - Draw x from range(((end − start).days + 1)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L5168) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L840)

<a id="op-a2f361b08b3674"></a>
### Process Period Closing Voucher.generate pcv dates

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_generate_period_closing_voucher_dates`

**Inputs** self.

**Record and data access** resolve a document from “Period Closing Voucher” via get\_doc.

**Local steps**

- Set self.normal\_balances from list().
- Set pcv from Platform.get\_doc(“Period Closing Voucher”, self.parent\_pcv).
- Set dates from self.get\_dates(get\_datetime(pcv.period\_start\_date), get\_datetime(pcv.period\_end\_date)).
- For each x in dates.
  - Evaluate self.append(“normal\_balances”, mapping(“processing\_date” → x, “status” → “Queued”, “report\_type” → “Profit and Loss”)).
  - Evaluate self.append(“normal\_balances”, mapping(“processing\_date” → x, “status” → “Queued”, “report\_type” → “Balance Sheet”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get dates](operations-088.md#op-a502e54db967e1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L5295) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L839)

<a id="op-e4ec435711427c"></a>
### Process Period Closing Voucher.generate opening balances dates

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_generate_opening_balances_dates`

**Inputs** self.

**Record and data access** resolve a document from “Period Closing Voucher” via get\_doc.

**Local steps**

- Set self.z\_opening\_balances from list().
- Set pcv from Platform.get\_doc(“Period Closing Voucher”, self.parent\_pcv).
- If pcv.is\_first\_period\_closing\_voucher().
  - Set gl from qb.DocType(“GL Entry”).
  - Set min from nested operand in the contract(nested operand in the contract).select(Min(nested operand in the contract.posting\_date)).run() at 0 at 0.
  - Set max from nested operand in the contract(nested operand in the contract).select(Max(nested operand in the contract.posting\_date)).run() at 0 at 0.
  - Set dates from self.get\_dates(get\_datetime(min), get\_datetime(max)).
  - For each x in dates.
    - Evaluate self.append(“z\_opening\_balances”, mapping(“processing\_date” → x, “status” → “Queued”, “report\_type” → “Balance Sheet”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get dates](operations-088.md#op-a502e54db967e1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L5634) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L838)

<a id="op-9cd955473bcc82"></a>
### Process Period Closing Voucher.on submit

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_on_submit`

**Inputs** self.

**Local steps**

- Evaluate start\_pcv\_processing(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L6109) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L843)

<a id="op-1238ca1779091e"></a>
### Process Period Closing Voucher.on cancel

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_process_period_closing_voucher_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate cancel\_pcv\_processing(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0139.json#L6167) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L841)

<a id="op-d7cf04c08aa6b4"></a>
### Initialize parallel threads

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_initialize_parallel_threads`

**Inputs** docname.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**State and service calls** request set\_value on “Process Period Closing Voucher” · request set\_value on “Process Period Closing Voucher Detail” · enqueue · commit.

**Local steps**

- Set threads from 4.
- Set timeout from (Platform.db.get\_single\_value(“Accounts Settings”, “pcv\_job\_timeout”) or 3600).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Accounts Settings”, “pcv\_job\_timeout”) → 3600.
- Set ppcvd from qb.DocType(“Process Period Closing Voucher Detail”).
- Evaluate Platform.db.set\_value(“Process Period Closing Voucher”, docname, “status”, “Running”).
- If normal\_balances bound to nested operand in the contract.limit(threads).for\_update(skip\_locked = true).run(as\_dict = true).
  - If not is\_scheduler\_inactive().
    - For each x in normal\_balances.
      - Evaluate Platform.db.set\_value(“Process Period Closing Voucher Detail”, x.name, “status”, “Running”).
      - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.process\_period\_closing\_voucher.process\_period\_closing\_voucher.process\_individual\_date”, queue = “long”, timeout = timeout, is\_async = true, …).
    - If not Platform.in\_test.
      - Evaluate Platform.db.commit().
- Otherwise.
  - Evaluate schedule\_next\_date(docname).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “pcv\_job\_timeout”) · service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.process\_period\_closing\_voucher.process\_period\_closing\_voucher.process\_individual\_date”, queue = “long”, timeout = timeout, is\_async = true, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L834)

<a id="op-13438082ce7b9c"></a>
### Start pcv processing

`operation_enterprise_accounts_record_definitions_process_period_closing_voucher_business_behavior_start_period_closing_voucher_processing`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Local steps**

- Evaluate Platform.has\_permission(“Process Period Closing Voucher”, “write”, doc = docname, throw = true).
- If Platform.get\_lazy\_doc(“Process Period Closing Voucher”, docname).validate\_processing(list(“Queued”, “Running”)).
  - Evaluate initialize\_parallel\_threads(docname).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Period Closing Voucher”, “write”, doc = docname, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L848)
