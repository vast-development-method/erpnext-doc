# Accounting and settlement · operations 82

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pos invoice merge log

<a id="op-ee5c0c17aa2801"></a>
### Get reversed rows

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_merge_log_pos_invoice_merge_log_get_reversed_rows`

**Inputs** return\_against.

**Explicit results** mapping() · mapping of row.pos\_invoice\_item → row for row drawn from rows.

**Local steps**

- If not return\_against.
  - Return mapping().
- Set sales\_invoice from DocType(“Sales Invoice”).
- Set sales\_invoice\_item from DocType(“Sales Invoice Item”).
- Set rows from nested operand in the contract(nested operand in the contract).select(sales\_invoice\_item.name, sales\_invoice\_item.rate, sales\_invoice\_item.pos\_invoice\_item).where(((nested operand in the contract.name equa ….
- Return mapping of row.pos\_invoice\_item → row for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L886)

<a id="op-8133f28253b96b"></a>
### Get all unconsolidated invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_get_all_unconsolidated_invoices`

**Inputs** no declared parameters.

**Record and data access** read “POS Invoice” via get\_all.

**Explicit results** pos\_invoices.

**Local steps**

- Set filters from mapping(“consolidated\_invoice” → list(“in”, list(empty text, no value)), “status” → list(“not in”, list(“Consolidated”)), “docstatus” → 1).
- Set pos\_invoices from Platform.db.get\_all(“POS Invoice”, filters = filters, fields = list(“name as pos\_invoice”, “posting\_date”, “grand\_total”, “customer”, …)).
- Return pos\_invoices.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L4506) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L559)

<a id="op-487e107cee97f0"></a>
### Get invoice customer map

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_get_invoice_customer_map`

**Inputs** pos\_invoices.

**Explicit results** pos\_invoice\_customer\_map.

**Local steps**

- Set pos\_invoice\_customer\_map from mapping().
- For each invoice in pos\_invoices.
  - Set customer from invoice.get(“customer”).
  - Evaluate pos\_invoice\_customer\_map.setdefault(customer, list()).
  - Evaluate pos\_invoice\_customer\_map at customer.append(invoice).
- For each tuple(customer, invoices) in pos\_invoice\_customer\_map.items().
  - Set pos\_invoice\_customer\_map at customer from split\_invoices\_by\_accounting\_dimension(invoices).
- Return pos\_invoice\_customer\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L4736) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L561)

<a id="op-987bb10a208d2a"></a>
### Split invoices by accounting dimension

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_split_invoices_by_accounting_dimension`

**Inputs** pos\_invoices.

**Record and data access** read “POS Invoice” via get\_value.

**Explicit results** pos\_invoice\_accounting\_dimensions\_map.

**Local steps**

- Set pos\_invoice\_accounting\_dimensions\_map from mapping().
- For each invoice in pos\_invoices.
  - Set dimension\_fields from list of d.fieldname for d drawn from get\_checks\_for\_pl\_and\_bs\_accounts().
    - Draw d from get\_checks\_for\_pl\_and\_bs\_accounts().
  - Set accounting\_dimensions from Platform.db.get\_value(“POS Invoice”, invoice.pos\_invoice, list(expanded dimension\_fields, “cost\_center”, “project”), as\_dict = 1).
  - Set accounting\_dimensions\_dic\_hash from hashlib.sha256(nested operand in the contract.dumps(accounting\_dimensions).encode()).hexdigest().
  - Evaluate pos\_invoice\_accounting\_dimensions\_map.setdefault(accounting\_dimensions\_dic\_hash, list()).
  - Evaluate pos\_invoice\_accounting\_dimensions\_map at accounting\_dimensions\_dic\_hash.append(invoice).
- Return pos\_invoice\_accounting\_dimensions\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L4963) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L579)

<a id="op-989d8676d05311"></a>
### Consolidate pos invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_consolidate_point_of_sale_invoices`

**Inputs** pos\_invoices = no value, closing\_entry = no value.

**Local steps**

- Set invoices from (pos\_invoices or (closing\_entry and closing\_entry.get(“pos\_invoices”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pos\_invoices → (closing\_entry and closing\_entry.get(“pos\_invoices”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in closing\_entry → closing\_entry.get(“pos\_invoices”).
- If (Platform.in\_test and not invoices).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.in\_test → not invoices.
  - Set invoices from get\_all\_unconsolidated\_invoices().
- Set invoice\_by\_customer from get\_invoice\_customer\_map(invoices).
- If (len(invoices) ≥ 10 and closing\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(invoices) ≥ 10 → closing\_entry.
  - Evaluate closing\_entry.set\_status(update = true, status = “Queued”).
  - Evaluate enqueue\_job(create\_merge\_logs, invoice\_by\_customer = invoice\_by\_customer, closing\_entry = closing\_entry).
- Otherwise.
  - Evaluate create\_merge\_logs(invoice\_by\_customer, closing\_entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L5284) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L555)

<a id="op-e49ced1ca379fc"></a>
### Unconsolidate pos invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_unconsolidate_point_of_sale_invoices`

**Inputs** closing\_entry.

**Record and data access** read “POS Invoice Merge Log” via get\_all.

**Local steps**

- Set merge\_logs from Platform.get\_all(“POS Invoice Merge Log”, filters = mapping(“pos\_closing\_entry” → closing\_entry.name), pluck = “name”).
- If len(closing\_entry.pos\_invoices) ≥ 10.
  - Set closing\_entry.ignore\_linked\_doctypes from tuple(“POS Invoice Merge Log”, “Sales Invoice”).
  - Evaluate closing\_entry.set\_status(update = true, status = “Queued”).
  - Evaluate enqueue\_job(cancel\_merge\_logs, merge\_logs = merge\_logs, closing\_entry = closing\_entry).
- Otherwise.
  - Evaluate cancel\_merge\_logs(merge\_logs, closing\_entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L580)

<a id="op-f9fe457aa59b17"></a>
### Split invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_split_invoices`

**Inputs** invoices.

**Record and data access** resolve a document from “POS Invoice” via get\_cached\_doc · read “POS Invoice” via get\_value.

**Explicit results** \_invoices.

**Local steps**

- Set \_invoices from list().
- Set special\_invoices from list().
- Set pos\_return\_docs from list of Platform.get\_cached\_doc(“POS Invoice”, d.pos\_invoice) for d drawn from invoices where (d.is\_return and d.return\_against).
  - Draw d from invoices, keep a combination only if ((d.is\_return and d.return\_against)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_return → d.return\_against.
- For each pos\_invoice in pos\_return\_docs.
  - For each item in pos\_invoice.items.
    - If (not item.serial\_no and not item.serial\_and\_batch\_bundle).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.serial\_no → not item.serial\_and\_batch\_bundle.
      - Continue with the next iteration or loop test.
    - Set return\_against\_is\_added from any(generator of d for d drawn from \_invoices where (d and d at 0.pos\_invoice equals pos\_invoice.return\_against)).
      - Draw d from \_invoices, keep a combination only if ((d and d at 0.pos\_invoice equals pos\_invoice.return\_against)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d → d at 0.pos\_invoice equals pos\_invoice.return\_against.
    - If return\_against\_is\_added.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Set return\_against\_is\_consolidated from Platform.db.get\_value(“POS Invoice”, pos\_invoice.return\_against, “status”, cache = true) equals “Consolidated”.
    - If return\_against\_is\_consolidated.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Set pos\_invoice\_row from list of d for d drawn from invoices where d.pos\_invoice equals pos\_invoice.return\_against.
      - Draw d from invoices, keep a combination only if (d.pos\_invoice equals pos\_invoice.return\_against).
    - Evaluate \_invoices.append(pos\_invoice\_row).
    - Evaluate special\_invoices.append(pos\_invoice.return\_against).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate \_invoices.append(list of d for d drawn from invoices where d.pos\_invoice does not belong to special\_invoices).
  - Draw d from invoices, keep a combination only if (d.pos\_invoice does not belong to special\_invoices).
- Return \_invoices.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Invoice”, d.pos\_invoice).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L5863) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L578)

<a id="op-76c2d4f4b62679"></a>
### Create merge logs

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_create_merge_logs`

**Inputs** invoice\_by\_customer, closing\_entry = no value.

**State and service calls** rollback · commit · publish realtime with “closing\_process\_complete”.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind local operation merge\_and\_close for subsequent calls.
- If Platform.in\_test.
  - Evaluate merge\_and\_close().
- Otherwise.
  - Attempt the following.
    - Evaluate merge\_and\_close().
  - On failure (Exception) bound to e.
    - Evaluate Platform.db.rollback().
    - Set message\_log from Platform.message\_log.pop() when Platform.message\_log, otherwise str(e).
      - Value choice on Platform.message\_log — true gives Platform.message\_log.pop(), false gives str(e).
    - Set error\_message from get\_error\_message(message\_log).
    - If closing\_entry.
      - Evaluate set\_closing\_entry\_status\_after\_failure(closing\_entry, “Failed”, error\_message).
    - Propagate the active failure.
  - On exit, including pending return or failure.
    - Evaluate Platform.db.commit().
    - Evaluate Platform.publish\_realtime(“closing\_process\_complete”, user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“closing\_process\_complete”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L556)

<a id="op-70fa9a02effb86"></a>
### Create merge logs.merge and close

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_create_merge_logs_merge_and_close`

**Inputs** no declared parameters.

**State and service calls** request new\_doc for “POS Invoice Merge Log” · call save on merge\_log · call submit on merge\_log · call db\_set on closing\_entry.

**Local steps**

- For each tuple(customer, invoices\_acc\_dim) in invoice\_by\_customer.items().
  - For each invoices in invoices\_acc\_dim.values().
    - For each \_invoices in split\_invoices(invoices).
      - Set merge\_log from Platform.new\_doc(“POS Invoice Merge Log”).
      - Set merge\_log.posting\_date from getdate(closing\_entry.get(“posting\_date”)) when closing\_entry, otherwise nowdate().
        - Value choice on closing\_entry — true gives getdate(closing\_entry.get(“posting\_date”)), false gives nowdate().
      - Set merge\_log.posting\_time from get\_time(closing\_entry.get(“posting\_time”)) when closing\_entry, otherwise nowtime().
        - Value choice on closing\_entry — true gives get\_time(closing\_entry.get(“posting\_time”)), false gives nowtime().
      - Set merge\_log.company from closing\_entry.get(“company”) when closing\_entry, otherwise no value.
        - Value choice on closing\_entry — true gives closing\_entry.get(“company”), false gives no value.
      - Set merge\_log.customer from customer.
      - Set merge\_log.pos\_closing\_entry from closing\_entry.get(“name”) when closing\_entry, otherwise no value.
        - Value choice on closing\_entry — true gives closing\_entry.get(“name”), false gives no value.
      - Evaluate merge\_log.set(“pos\_invoices”, \_invoices).
      - Evaluate merge\_log.save(ignore\_permissions = true).
      - Evaluate merge\_log.submit().
- If closing\_entry.
  - Evaluate closing\_entry.set\_status(update = true, status = “Submitted”).
  - Evaluate closing\_entry.db\_set(“error\_message”, empty text).
  - Evaluate closing\_entry.update\_opening\_entry().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0126.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L557)

<a id="op-b83bb11e46432f"></a>
### Cancel merge logs

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_cancel_merge_logs`

**Inputs** merge\_logs, closing\_entry = no value.

**State and service calls** rollback · commit · publish realtime with “closing\_process\_complete”.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind local operation merge\_cancel\_and\_close for subsequent calls.
- If Platform.flags.in\_test.
  - Evaluate merge\_cancel\_and\_close().
- Otherwise.
  - Attempt the following.
    - Evaluate merge\_cancel\_and\_close().
  - On failure (Exception) bound to e.
    - Evaluate Platform.db.rollback().
    - Set message\_log from Platform.message\_log.pop() when Platform.message\_log, otherwise str(e).
      - Value choice on Platform.message\_log — true gives Platform.message\_log.pop(), false gives str(e).
    - Set error\_message from get\_error\_message(message\_log).
    - If closing\_entry.
      - Evaluate set\_closing\_entry\_status\_after\_failure(closing\_entry, “Submitted”, error\_message).
    - Propagate the active failure.
  - On exit, including pending return or failure.
    - Evaluate Platform.db.commit().
    - Evaluate Platform.publish\_realtime(“closing\_process\_complete”, user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“closing\_process\_complete”, user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L552)

<a id="op-502f3624637dbe"></a>
### Cancel merge logs.merge cancel and close

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_cancel_merge_logs_merge_cancel_and_close`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “POS Invoice Merge Log” via get\_doc.

**State and service calls** call cancel on merge\_log · call db\_set on closing\_entry.

**Local steps**

- For each log in merge\_logs.
  - Set merge\_log from Platform.get\_doc(“POS Invoice Merge Log”, log).
  - <a id="op-502f3624637dbe-guard-4"></a>If merge\_log.docstatus equals 2.
    - Continue with the next iteration or loop test.
  - Set merge\_log.flags.ignore\_permissions from true.
  - Evaluate merge\_log.cancel().
- If closing\_entry.
  - Evaluate closing\_entry.set\_status(update = true, status = “Cancelled”).
  - Evaluate closing\_entry.db\_set(“error\_message”, empty text).
  - Evaluate closing\_entry.update\_opening\_entry(for\_cancel = true).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison merge\_log.docstatus equals 2, merge\_log.docstatus = 2 (cancelled) selects the branch that continues with the next loop iteration. With merge\_log.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-502f3624637dbe-guard-4)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0126.json#L1188) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L553)

<a id="op-98bd0008d56cd2"></a>
### Set closing entry status after failure

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_merge_log_pos_invoice_merge_log_set_closing_entry_status_after_failure`

**Inputs** closing\_entry, status, error\_message.

**Record and data access** read “POS Closing Entry” via get\_value.

**State and service calls** call db\_set on closing\_entry.

**Explicit results** no value.

**Local steps**

- Set docstatus from Platform.db.get\_value(“POS Closing Entry”, closing\_entry.name, “docstatus”).
- If not docstatus.
  - Return no value.
- If isinstance(error\_message, list).
  - Set error\_message from json.dumps(error\_message).
- Evaluate closing\_entry.db\_set(mapping(“status” → “Failed” when docstatus equals 2, otherwise status, “error\_message” → error\_message)).
  - Value choice on docstatus equals 2 — true gives “Failed”, false gives status.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L889)

<a id="op-7a09c80a793905"></a>
### Enqueue job

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_enqueue_job`

**Inputs** job, remaining named values kwargs.

**State and service calls** msgprint with msg.

**Local steps**

- Evaluate check\_scheduler\_status().
- Set closing\_entry from (kwargs.get(“closing\_entry”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“closing\_entry”) → mapping().
- Set job\_id from (“pos\_invoice\_merge::” + str(closing\_entry.get(“name”))).
- If not is\_job\_enqueued(job\_id).
  - Evaluate enqueue(job, expanded names kwargs, queue = “long”, timeout = 10000, event = “processing\_merge\_logs”, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.in\_test.
  - If job equals create\_merge\_logs.
    - Set msg from translated “POS Invoices will be consolidated in a background process”.
  - Otherwise.
    - Set msg from translated “POS Invoices will be unconsolidated in a background process”.
  - Evaluate Platform.msgprint(msg, alert = 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from enqueue(job, expanded names kwargs, queue = “long”, timeout = 10000, event = “processing\_merge\_logs”, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L558)

<a id="op-f825cafdc678ac"></a>
### Check scheduler status

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_check_scheduler_status`

**Inputs** no declared parameters.

**Explicit failure paths** validation helper — translated “Scheduler is inactive. Cannot enqueue job.”.

**Local steps**

- If (is\_scheduler\_inactive() and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_scheduler\_inactive() → not Platform.in\_test.
  - Call the validation error handler Platform.throw(translated “Scheduler is inactive. Cannot enqueue job.”, title = translated “Scheduler Inactive”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0126.json#L1827) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L554)

<a id="op-7a96c2b61bf1c7"></a>
### Get error message

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_get_error_message`

**Inputs** message.

**Declared result** str.

**Explicit results** message at “message” · str(message).

**Local steps**

- Attempt the following.
  - Return message at “message”.
- On failure (Exception).
  - Return str(message).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0126.json#L1950) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L560)

## Record · Pos opening entry

<a id="op-34ad5a64dd38b9"></a>
### POSOpening Entry.validate

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_pos\_profile\_and\_cashier().
- Evaluate self.check\_open\_pos\_exists().
- Evaluate self.check\_user\_already\_assigned().
- Evaluate self.validate\_balance\_details().
- Evaluate self.validate\_payment\_method\_account().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate pos profile and cashier](operations-082.md#op-8f144c7499bfbf), [check open pos exists](operations-082.md#op-8b2e8503c10af6), [check user already assigned](operations-082.md#op-d0ad63f1e54739), [validate balance details](operations-082.md#op-10b2c9f572fcdc), [validate payment method account](operations-082.md#op-a9624e9b8b0974).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L636)

<a id="op-8f144c7499bfbf"></a>
### POSOpening Entry.validate pos profile and cashier

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_validate_point_of_sale_profile_and_cashier`

**Inputs** self.

**Record and data access** read “POS Profile” via exists · read “POS Profile” via get\_value · read “User” via get\_value.

**Explicit failure paths** validation helper — translated “POS Profile {} does not exist.”.format(self.pos\_profile) · validation helper — translated “POS Profile {} is disabled.”.format(Platform.bold(self.pos\_profile)) · validation helper — translated “POS Profile {} does not belong to company {}”.format(self.pos\_profile, self.company) · validation helper — translated “User {} is disabled. Please select valid user/cashier”.format(self.user).

**Local steps**

- If not Platform.db.exists(“POS Profile”, self.pos\_profile).
  - Call the validation error handler Platform.throw(translated “POS Profile {} does not exist.”.format(self.pos\_profile)).
- Set tuple(pos\_profile\_company, pos\_profile\_disabled) from Platform.db.get\_value(“POS Profile”, self.pos\_profile, list(“company”, “disabled”)).
- If pos\_profile\_disabled.
  - Call the validation error handler Platform.throw(translated “POS Profile {} is disabled.”.format(Platform.bold(self.pos\_profile))).
- If self.company differs from pos\_profile\_company.
  - Call the validation error handler Platform.throw(translated “POS Profile {} does not belong to company {}”.format(self.pos\_profile, self.company)).
- If not cint(Platform.db.get\_value(“User”, self.user, “enabled”)).
  - Call the validation error handler Platform.throw(translated “User {} is disabled. Please select valid user/cashier”.format(self.user)).
- Evaluate self.validate\_cashier\_of\_pos\_profile().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate cashier of pos profile](operations-082.md#op-09e68f36a695ec).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L638)

<a id="op-09e68f36a695ec"></a>
### POSOpening Entry.validate cashier of pos profile

`operation_enterprise_binding_enterprise_accounts_doctype_pos_opening_entry_pos_opening_entry_posopeningentry_validate_cashier_of_pos_profile`

**Inputs** self.

**Record and data access** read “POS Profile User” via get\_all.

**Explicit failure paths** validation helper — translated “User {0} is not in Applicable for Users of POS Profile {1}”.format(Platform.bold(self.user), Platform.bold(self.pos\_profile)).

**Local steps**

- Set cashiers from Platform.get\_all(“POS Profile User”, filters = mapping(“parent” → self.pos\_profile, “parenttype” → “POS Profile”), pluck = “user”).
- If (cashiers and all(cashiers) and self.user does not belong to cashiers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cashiers → all(cashiers) → self.user does not belong to cashiers.
  - Call the validation error handler Platform.throw(translated “User {0} is not in Applicable for Users of POS Profile {1}”.format(Platform.bold(self.user), Platform.bold(self.pos\_profile)), title = translated “Invalid Cashier”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L905)

<a id="op-8b2e8503c10af6"></a>
### POSOpening Entry.check open pos exists

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_check_open_point_of_sale_exists`

**Inputs** self.

**Record and data access** read “POS Opening Entry” via exists.

**Explicit failure paths** validation helper.

**Local steps**

- If Platform.db.exists(“POS Opening Entry”, mapping(“pos\_profile” → self.pos\_profile, “status” → “Open”)).
  - Call the validation error handler Platform.throw(title = translated “POS Opening Entry Exists”, msg = translated “{0} is open. Close the POS or cancel the existing POS Opening Entry to create a new POS Opening Entry.”.format(Platform.bold( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0127.json#L4101) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L631)

<a id="op-d0ad63f1e54739"></a>
### POSOpening Entry.check user already assigned

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_check_user_already_assigned`

**Inputs** self.

**Record and data access** read “POS Opening Entry” via exists.

**Explicit failure paths** validation helper.

**Local steps**

- If Platform.db.exists(“POS Opening Entry”, mapping(“user” → self.user, “status” → “Open”)).
  - Call the validation error handler Platform.throw(title = translated “Cannot Assign Cashier”, msg = translated “Cashier is currently assigned to another POS.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0127.json#L4315) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L633)

<a id="op-10b2c9f572fcdc"></a>
### POSOpening Entry.validate balance details

`operation_enterprise_binding_enterprise_accounts_doctype_pos_opening_entry_pos_opening_entry_posopeningentry_validate_balance_details`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Opening Amount for {1} cannot be negative”.format(d.idx, Platform.bold(d.mode\_of\_payment)) · validation helper — translated “Row #{0}: Mode of Payment {1} is added more than once”.format(d.idx, Platform.bold(d.mode\_of\_payment)).

**Local steps**

- Set modes\_of\_payment from set().
- For each d in self.balance\_details.
  - If flt(d.opening\_amount) &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Opening Amount for {1} cannot be negative”.format(d.idx, Platform.bold(d.mode\_of\_payment))).
  - If d.mode\_of\_payment belongs to modes\_of\_payment.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Mode of Payment {1} is added more than once”.format(d.idx, Platform.bold(d.mode\_of\_payment))).
  - Evaluate modes\_of\_payment.add(d.mode\_of\_payment).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L904)

<a id="op-a9624e9b8b0974"></a>
### POSOpening Entry.validate payment method account

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_validate_payment_method_account`

**Inputs** self.

**Record and data access** read “Mode of Payment Account” via get\_value.

**Explicit failure paths** validation helper — msg.format(“, ”.join(invalid\_modes)).

**Local steps**

- Set invalid\_modes from list().
- For each d in self.balance\_details.
  - If d.mode\_of\_payment.
    - Set account from Platform.db.get\_value(“Mode of Payment Account”, mapping(“parent” → d.mode\_of\_payment, “company” → self.company), “default\_account”).
    - If not account.
      - Evaluate invalid\_modes.append(get\_link\_to\_form(“Mode of Payment”, d.mode\_of\_payment)).
- If invalid\_modes.
  - If invalid\_modes equals 1.
    - Set msg from translated “Please set default Cash or Bank account in Mode of Payment {}”.
  - Otherwise.
    - Set msg from translated “Please set default Cash or Bank account in Mode of Payments {}”.
  - Call the validation error handler Platform.throw(msg.format(“, ”.join(invalid\_modes)), title = translated “Missing Account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L637)

<a id="op-143e572240ac02"></a>
### POSOpening Entry.on submit

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0127.json#L4892) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L635)

<a id="op-7fd3a0af190622"></a>
### POSOpening Entry.before cancel

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.check\_poe\_is\_cancellable().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check poe is cancellable](operations-083.md#op-eb97c9c9cb53f7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0127.json#L4951) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L630)
