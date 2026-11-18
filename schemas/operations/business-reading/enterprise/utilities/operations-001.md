# Supporting services · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Activation

<a id="op-3354b069a5d210"></a>
### Get level

`operation_enterprise_utilities_activation_business_behavior_get_level`

**Inputs** site\_info.

**Record and data access** read doctype via count · read “Communication” via count · execute query text (SELECT, User).

**Explicit results** level.

**Local steps**

- Set activation\_level from site\_info.get(“activation”, mapping()).get(“activation\_level”, 0).
- Set sales\_data from site\_info.get(“activation”, mapping()).get(“sales\_data”, list()).
- Set min\_count from 0.
- Set doctypes from mapping(“Asset” → 5, “BOM” → 3, “Customer” → 5, “Delivery Note” → 5, …).
- For each tuple(doctype, min\_count) in doctypes.items().
  - Set count from Platform.db.count(doctype).
  - If count &gt; min\_count.
    - Update activation\_level using + 1.
  - Evaluate sales\_data.append(mapping(doctype → count)).
- If “Enterprise” belongs to get\_setup\_wizard\_completed\_apps().
  - Update activation\_level using + 1.
- Set communication\_number from Platform.db.count(“Communication”, dict(communication\_medium = “Email”)).
- If communication\_number &gt; 10.
  - Update activation\_level using + 1.
- Evaluate sales\_data.append(mapping(“Communication” → communication\_number)).
- If Platform.db.sql(query text (SELECT, User)).
  - Update activation\_level using + 1.
- Set level from mapping(“activation\_level” → activation\_level, “sales\_data” → sales\_data).
- Return level.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L60)

<a id="op-301ccaf1d64184"></a>
### Get help messages

`operation_enterprise_utilities_activation_business_behavior_get_help_messages`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_cached\_value · read m.doctype via count.

**Explicit results** list() · messages.

**Local steps**

- If get\_level() &gt; 6.
  - Return list().
- Set domain from Platform.get\_cached\_value(“Company”, Enterprise.get\_default\_company(), “domain”).
- Set messages from list().
- Set message\_settings from list(Platform.\_dict(doctype = “Lead”, title = translated “Create Leads”, description = translated “Leads help you get business, add all your contacts and more as your leads”, action = translated “Create Le ….
- For each m in message\_settings.
  - If (not m.domain or domain belongs to m.domain).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not m.domain → domain belongs to m.domain.
    - Set m.count from Platform.db.count(m.doctype).
    - If m.count &lt; m.target.
      - Evaluate messages.append(m).
- Return messages.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, Enterprise.get\_default\_company(), “domain”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0988.json#L2592) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L59)

## Service · Addresses

<a id="op-3da4c3ae1fed75"></a>
### Get context

`operation_enterprise_utilities_web_form_addresses_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Set context.show\_sidebar from true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L2245) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L123)

## Service · Banking

<a id="op-2efce9bbcbb049"></a>
### Get context

`operation_enterprise_public_pages_banking_business_behavior_get_context`

**Inputs** context.

**Explicit results** context.

**Local steps**

- Evaluate validate\_desk\_user().
- Set csrf\_token from Platform.sessions.get\_csrf\_token().
- Set context from Platform.\_dict().
- Set context.boot from get\_boot().
- Set context.csrf\_token from csrf\_token.
- Set context.build\_version from Platform.utils.get\_build\_version().
- Set context.app\_name from (Platform.get\_website\_settings(“app\_name”) or Platform.get\_system\_settings(“app\_name”) or “Enterprise”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_website\_settings(“app\_name”) → Platform.get\_system\_settings(“app\_name”) → “Enterprise”.
- Set context.layout\_direction from “rtl” when is\_rtl(), otherwise “ltr”.
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.
- Set context.lang from Platform.local.lang.
- Return context.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“app\_name”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L883)

<a id="op-b078552bd53c97"></a>
### Validate desk user

`operation_enterprise_binding_enterprise_www_banking_validate_desk_user`

**Inputs** no declared parameters.

**State and service calls** msgprint with translated “Log in to access this page.”.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not permitted to access this page.”.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Set Platform.response at “status\_code” from 403.
  - Evaluate Platform.msgprint(translated “Log in to access this page.”).
  - Evaluate Platform.redirect(formatted text /login?{urlencode(mapping(“redirect-to” → Platform.request.path))}).
- Otherwise.
  - If is\_website\_user().
    - Call the validation error handler Platform.throw(translated “You are not permitted to access this page.”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1346)

<a id="op-68ad85a14ea1c9"></a>
### Get context for dev

`operation_enterprise_public_pages_banking_business_behavior_get_context_for_development`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”), allow\_guest = true).

**Explicit results** mapping(“boot” → json.loads(get\_boot()), “layout\_direction” → “rtl” when is\_rtl(), otherwise “ltr”).

**Explicit failure paths** validation helper — translated “This method is only meant for developer mode”.

**Local steps**

- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “This method is only meant for developer mode”).
- Evaluate validate\_desk\_user().
- Return mapping(“boot” → json.loads(get\_boot()), “layout\_direction” → “rtl” when is\_rtl(), otherwise “ltr”).
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L884)

<a id="op-0cd1c3ebf30d01"></a>
### Get boot

`operation_enterprise_public_pages_banking_business_behavior_get_boot`

**Inputs** no declared parameters.

**Explicit results** boot\_json.

**Explicit failure paths** Platform.SessionBootFailed.

**Local steps**

- Attempt the following.
  - Set boot from Platform.sessions.get().
- On failure (Exception) bound to e.
  - Raise Platform.SessionBootFailed with cause e.
- Set boot\_json from Platform.as\_json(boot, indent = no value, separators = tuple(“,”, “:”)).
- Set boot\_json from SCRIPT\_TAG\_PATTERN.sub(empty text, boot\_json).
- Set boot\_json from CLOSING\_SCRIPT\_TAG\_PATTERN.sub(empty text, boot\_json).
- Set boot\_json from json.dumps(boot\_json).
- Return boot\_json.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L2793) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L882)

## Service · Boot

<a id="op-ff3091d83dffb8"></a>
### Boot session

`operation_enterprise_startup_boot_business_behavior_boot_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** bootinfo.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L681)

<a id="op-50f8fb84fb25cf"></a>
### Remove disabled price list defaults

`operation_enterprise_startup_boot_business_behavior_remove_disabled_price_list_defaults`

**Inputs** bootinfo.

**Local steps**

- Set user\_defaults from ((bootinfo.user or mapping()).get(“defaults”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (bootinfo.user or mapping()).get(“defaults”) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bootinfo.user → mapping().
- For each key in tuple(“selling\_price\_list”, “buying\_price\_list”).
  - Set price\_list from (bootinfo.sysdefaults.get(key) or user\_defaults.get(key)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bootinfo.sysdefaults.get(key) → user\_defaults.get(key).
  - If (not isinstance(price\_list, str) or is\_price\_list\_enabled(price\_list)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(price\_list, str) → is\_price\_list\_enabled(price\_list).
    - Continue with the next iteration or loop test.
  - Evaluate bootinfo.sysdefaults.pop(key, no value).
  - Evaluate user\_defaults.pop(key, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L2244) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L683)

<a id="op-09a67bb6257171"></a>
### Update page info

`operation_enterprise_startup_boot_business_behavior_update_page_info`

**Inputs** bootinfo.

**Local steps**

- Evaluate bootinfo.page\_info.update(mapping(“Chart of Accounts” → mapping(“title” → “Chart of Accounts”, “route” → “Tree/Account”), “Chart of Cost Centers” → mapping(“title” → “Chart of Cost Centers”, “route” → “Tre ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L2540) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L684)

<a id="op-a35a6fbf251fec"></a>
### Bootinfo

`operation_enterprise_startup_boot_business_behavior_bootinfo`

**Inputs** bootinfo.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- If (bootinfo.get(“user”) and bootinfo at “user”.get(“name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bootinfo.get(“user”) → bootinfo at “user”.get(“name”).
  - Set bootinfo at “user” at “employee” from empty text.
  - Set Platform.session.data.employee from empty text.
  - Set employee from Platform.db.get\_value(“Employee”, mapping(“user\_id” → bootinfo at “user” at “name”), “name”).
  - If employee.
    - Set bootinfo at “user” at “employee” from employee.
    - Set Platform.session.data.employee from employee.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L2863) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L682)

## Service · Bulk transaction

<a id="op-6cc16c54622f74"></a>
### Transaction processing

`operation_enterprise_utilities_bulk_transaction_business_behavior_transaction_processing`

**Inputs** data, from\_doctype, to\_doctype, args = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** msgprint with skipped\_msg · msgprint with translated “Started a background job to create {1} {0}. {2}”.format(to\_doctype, length\_of\_data, skipped\_msg) · enqueue with job.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid name”.

**Local steps**

- Evaluate Platform.has\_permission(from\_doctype, “read”, throw = true).
- Evaluate Platform.has\_permission(to\_doctype, “create”, throw = true).
- If isinstance(data, str).
  - Set deserialized\_data from json.loads(data).
- Otherwise.
  - Set deserialized\_data from data.
- If isinstance(args, str).
  - Set args from Platform.\_dict(json.loads(args)).
- For each row in deserialized\_data.
  - Set source\_name from row.get(“name”).
  - If (not source\_name or not isinstance(source\_name, str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not source\_name → not isinstance(source\_name, str).
    - Call the validation error handler Platform.throw(translated “Invalid name”, Platform.PermissionError).
  - Evaluate Platform.has\_permission(from\_doctype, “read”, source\_name, throw = true).
- Set statuses from get\_statuses(from\_doctype, deserialized\_data).
- Set skipped\_records from list of d for d drawn from deserialized\_data where statuses.get(d.get(“name”)) belongs to tuple(“On Hold”, “Closed”).
  - Draw d from deserialized\_data, keep a combination only if (statuses.get(d.get(“name”)) belongs to tuple(“On Hold”, “Closed”)).
- Set deserialized\_data from list of d for d drawn from deserialized\_data where d does not belong to skipped\_records.
  - Draw d from deserialized\_data, keep a combination only if (d does not belong to skipped\_records).
- Set length\_of\_data from len(deserialized\_data).
- Set skipped\_msg from empty text.
- If skipped\_records.
  - Set skipped\_msg from translated “{0} creation for the following records will be skipped.”.format(to\_doctype).
  - Update skipped\_msg using + ((text in the contract + empty text.join(generator of nested operand in the contract(nested operand in the contract).format(nested operand in the contract.bold(nested operand in the contract(nested operand ….
    - Draw row from skipped\_records.
- If not length\_of\_data.
  - Evaluate Platform.msgprint(skipped\_msg).
  - Return no value.
- Evaluate Platform.msgprint(translated “Started a background job to create {1} {0}. {2}”.format(to\_doctype, length\_of\_data, skipped\_msg)).
- Evaluate Platform.enqueue(job, deserialized\_data = deserialized\_data, from\_doctype = from\_doctype, to\_doctype = to\_doctype, args = args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(from\_doctype, “read”, throw = true), Platform.has\_permission(to\_doctype, “create”, throw = true) and 1 further calls · service or queued work from Platform.enqueue(job, deserialized\_data = deserialized\_data, from\_doctype = from\_doctype, to\_doctype = to\_doctype, args = args).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L67)

<a id="op-524922dc521e9b"></a>
### Get statuses

`operation_enterprise_binding_enterprise_utilities_bulk_transaction_get_statuses`

**Inputs** doctype, rows.

**Declared result** dict.

**Record and data access** read doctype via get\_all.

**Explicit results** mapping() · dict(Platform.get\_all(doctype, filters = mapping(“name” → list(“in”, names)), fields = list(“name”, “status”), as\_list = true)).

**Local steps**

- If not Platform.get\_meta(doctype).has\_field(“status”).
  - Return mapping().
- Set names from list of row.get(“name”) for row drawn from rows where isinstance(row.get(“name”), str).
  - Draw row from rows, keep a combination only if (isinstance(row.get(“name”), str)).
- Return dict(Platform.get\_all(doctype, filters = mapping(“name” → list(“in”, names)), fields = list(“name”, “status”), as\_list = true)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L26) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1307)

<a id="op-bd85542c1cdecc"></a>
### Retry

`operation_enterprise_utilities_bulk_transaction_business_behavior_retry`

**Inputs** date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bulk Transaction Log Detail” via get\_all.

**State and service calls** msgprint with translated “There are no Failed transactions” · enqueue with retry\_failed\_transactions · msgprint with translated “Job: {0} has been triggered for processing failed transactions”.format(get\_link\_to\_form(“RQ Job”, job.id)).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If not date.
  - Set date from today().
- If date.
  - Set failed\_docs from Platform.db.get\_all(“Bulk Transaction Log Detail”, filters = mapping(“date” → date, “transaction\_status” → “Failed”, “retried” → 0), fields = list(“name”, “transaction\_name”, “from\_doctype”, “to\_doctype”, …)).
  - If not failed\_docs.
    - Evaluate Platform.msgprint(translated “There are no Failed transactions”).
  - Otherwise.
    - Set job from Platform.enqueue(retry\_failed\_transactions, failed\_docs = failed\_docs).
    - Evaluate Platform.msgprint(translated “Job: {0} has been triggered for processing failed transactions”.format(get\_link\_to\_form(“RQ Job”, job.id))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · clock or generated value from today() · service or queued work from Platform.enqueue(retry\_failed\_transactions, failed\_docs = failed\_docs).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L63)

<a id="op-2250ec73a78e81"></a>
### Retry failed transactions

`operation_enterprise_utilities_bulk_transaction_business_behavior_retry_failed_transactions`

**Inputs** failed\_docs.

**State and service calls** savepoint “before\_creation\_state” · rollback.

**Local steps**

- If failed\_docs.
  - For each log in failed\_docs.
    - If succeeded\_since(log).
      - Evaluate update\_log(log.name, “Failed”, 1).
      - Continue with the next iteration or loop test.
    - Attempt the following.
      - Evaluate Platform.db.savepoint(“before\_creation\_state”).
      - Evaluate task(log.transaction\_name, log.from\_doctype, log.to\_doctype).
    - On failure (Exception).
      - Evaluate Platform.db.rollback(save\_point = “before\_creation\_state”).
      - Evaluate update\_log(log.name, “Failed”, 1, str(Platform.get\_traceback(with\_context = true))).
    - When the protected block completes normally.
      - Evaluate update\_log(log.name, “Success”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L270) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L64)

<a id="op-b67f8a91def7e4"></a>
### Succeeded since

`operation_enterprise_binding_enterprise_utilities_bulk_transaction_succeeded_since`

**Inputs** log.

**Declared result** bool.

**Record and data access** read “Bulk Transaction Log Detail” via exists.

**Explicit results** bool(Platform.db.exists(“Bulk Transaction Log Detail”, mapping(“transaction\_name” → log.transaction\_name, “from\_doctype” → log.from\_doctype, “to\_doctype” → log.to\_doctype, “transaction\_status” → “Success”, …))).

**Local steps**

- Return bool(Platform.db.exists(“Bulk Transaction Log Detail”, mapping(“transaction\_name” → log.transaction\_name, “from\_doctype” → log.from\_doctype, “to\_doctype” → log.to\_doctype, “transaction\_status” → “Success”, …))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L27) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1308)

<a id="op-c0ddee042b14f9"></a>
### Update log

`operation_enterprise_utilities_bulk_transaction_business_behavior_update_log`

**Inputs** log\_name, status, retried, err = no value.

**State and service calls** request set\_value on “Bulk Transaction Log Detail”.

**Local steps**

- Evaluate Platform.db.set\_value(“Bulk Transaction Log Detail”, log\_name, “transaction\_status”, status).
- Evaluate Platform.db.set\_value(“Bulk Transaction Log Detail”, log\_name, “retried”, retried).
- If err.
  - Evaluate Platform.db.set\_value(“Bulk Transaction Log Detail”, log\_name, “error\_description”, err).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0988.json#L5422) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L68)

<a id="op-2fe0e508a287b4"></a>
### Job

`operation_enterprise_utilities_bulk_transaction_business_behavior_job`

**Inputs** deserialized\_data, from\_doctype, to\_doctype, args.

**State and service calls** savepoint “before\_creation\_state” · rollback.

**Local steps**

- Set failed from list().
- If args.
  - Set Platform.flags.args from args.
- For each d in deserialized\_data.
  - Attempt the following.
    - Set doc\_name from d.get(“name”).
    - Evaluate Platform.db.savepoint(“before\_creation\_state”).
    - Evaluate task(doc\_name, from\_doctype, to\_doctype).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = “before\_creation\_state”).
    - Evaluate failed.append(doc\_name).
    - Evaluate create\_log(doc\_name, str(Platform.get\_traceback(with\_context = true)), from\_doctype, to\_doctype, status = “Failed”, log\_date = str(date.today())).
  - When the protected block completes normally.
    - Evaluate create\_log(doc\_name, no value, from\_doctype, to\_doctype, status = “Success”, log\_date = str(date.today())).
- Evaluate show\_job\_status(failed, len(deserialized\_data), to\_doctype).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from date.today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L62)

<a id="op-edc34f2ab2201d"></a>
### Task

`operation_enterprise_utilities_bulk_transaction_business_behavior_task`

**Inputs** doc\_name, from\_doctype, to\_doctype.

**State and service calls** call insert on obj.

**Local steps**

- Bind dependencies payment\_entry.
- Bind dependencies purchase\_invoice.
- Bind dependencies sales\_invoice.
- Bind dependencies purchase\_order.
- Bind dependencies supplier\_quotation.
- Bind dependencies quotation.
- Bind dependencies sales\_order.
- Bind dependencies delivery\_note.
- Bind dependencies purchase\_receipt.
- Set mapper from mapping(“Sales Order” → mapping(“Sales Invoice” → sales\_order.make\_sales\_invoice, “Delivery Note” → sales\_order.make\_delivery\_note, “Payment Entry” → payment\_entry.get\_payment\_entry), “Sales Invoice” → map ….
- Set hooks from Platform.get\_hooks(“bulk\_transaction\_task\_mapper”).
- For each hook in hooks.
  - Evaluate mapper.update(Platform.get\_attr(hook)()).
- Set Platform.flags.bulk\_transaction from true.
- If to\_doctype belongs to list(“Payment Entry”).
  - Set obj from mapper at from\_doctype at to\_doctype(from\_doctype, doc\_name).
- Otherwise.
  - Set obj from mapper at from\_doctype at to\_doctype(doc\_name).
- If obj.
  - Set obj.flags.ignore\_validate from true.
  - Evaluate obj.set\_title\_field().
  - Evaluate obj.insert(ignore\_mandatory = true).
- Remove obj.
- Remove Platform.flags.bulk\_transaction.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“bulk\_transaction\_task\_mapper”), Platform.get\_attr(hook).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L66)

<a id="op-d1f9b35e647b80"></a>
### Create log

`operation_enterprise_utilities_bulk_transaction_business_behavior_create_log`

**Inputs** doc\_name, e, from\_doctype, to\_doctype, status, log\_date = no value, restarted = 0.

**State and service calls** request new\_doc for “Bulk Transaction Log Detail” · call save on transaction\_log.

**Local steps**

- Set transaction\_log from Platform.new\_doc(“Bulk Transaction Log Detail”).
- Set transaction\_log.transaction\_name from doc\_name.
- Set transaction\_log.date from today().
- Set now from datetime.now().
- Set transaction\_log.time from now.strftime(“%H:%M:%S”).
- Set transaction\_log.transaction\_status from status.
- Set transaction\_log.error\_description from str(e).
- Set transaction\_log.from\_doctype from from\_doctype.
- Set transaction\_log.to\_doctype from to\_doctype.
- Set transaction\_log.retried from restarted.
- Evaluate transaction\_log.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today(), datetime.now().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0988.json#L7077) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L61)

<a id="op-16ed2483a2b53c"></a>
### Show job status

`operation_enterprise_utilities_bulk_transaction_business_behavior_show_job_status`

**Inputs** failed, deserialized\_data\_count, to\_doctype.

**Declared result** no value.

**State and service calls** msgprint with translated “Creation of &lt;b&gt;&lt;a href='/app/{0}'&gt;{1}(s)&lt;/a&gt;&lt;/b&gt; successful”.format(to\_doctype.lower().replace(one space, “-”), to\_doctype) · msgprint with (translated “Creation of {0} partially successful.\\n\\t\\t\\t\\tCheck &lt;b&gt;&lt;a href="/app/bulk-transaction-log"&gt;Bulk Transaction …”.format(to\_doctype) + get\_failed\_list(failed)) · msgprint with (translated “Creation of {0} failed.\\n\\t\\t\\t\\tCheck &lt;b&gt;&lt;a href="/app/bulk-transaction-log"&gt;Bulk Transaction Log&lt;/a&gt;&lt;/b&gt;”.format(to\_doctype) + get\_failed\_list(failed)).

**Local steps**

- If not failed.
  - Evaluate Platform.msgprint(translated “Creation of &lt;b&gt;&lt;a href='/app/{0}'&gt;{1}(s)&lt;/a&gt;&lt;/b&gt; successful”.format(to\_doctype.lower().replace(one space, “-”), to\_doctype), title = “Successful”, indicator = “green”, realtime = true).
- Otherwise.
  - If len(failed) &lt; deserialized\_data\_count.
    - Evaluate Platform.msgprint((translated “Creation of {0} partially successful.\\n\\t\\t\\t\\tCheck &lt;b&gt;&lt;a href="/app/bulk-transaction-log"&gt;Bulk Transaction …”.format(to\_doctype) + get\_failed\_list(failed)), title = “Partia ….
  - Otherwise.
    - Evaluate Platform.msgprint((translated “Creation of {0} failed.\\n\\t\\t\\t\\tCheck &lt;b&gt;&lt;a href="/app/bulk-transaction-log"&gt;Bulk Transaction Log&lt;/a&gt;&lt;/b&gt;”.format(to\_doctype) + get\_failed\_list(failed)), title = “Failed”, i ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L65)

<a id="op-73499c906cbc19"></a>
### Get failed list

`operation_enterprise_binding_enterprise_utilities_bulk_transaction_get_failed_list`

**Inputs** failed.

**Declared result** str.

**Explicit results** ((text in the contract + translated “Could not be created from:”) + formatted text &lt;ul&gt;{items}&lt;/ul&gt;).

**Local steps**

- Set items from empty text.join(generator of formatted text &lt;li&gt;{Platform.bold(escape\_html(name))}&lt;/li&gt; for name drawn from failed).
  - Draw name from failed.
- Return ((text in the contract + translated “Could not be created from:”) + formatted text &lt;ul&gt;{items}&lt;/ul&gt;).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L25) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1306)

## Record · Bulk transaction log

[Record definition](../../../../data/record-types/bulk_transaction_log.json)

<a id="op-92abfb65ccffe2"></a>
### Bulk Transaction Log.db insert

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_bulk_transaction_log_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0335.json#L5794) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1349)

<a id="op-0a652d567f676a"></a>
### Bulk Transaction Log.load from db

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_bulk_transaction_log_load_from_database`

**Inputs** self.

**Record and data access** read “Bulk Transaction Log Detail” via exists.

**Explicit failure paths** Platform.DoesNotExistError.

**Local steps**

- Set log\_detail from qb.DocType(“Bulk Transaction Log Detail”).
- Set has\_records from Platform.db.exists(“Bulk Transaction Log Detail”, mapping(“date” → self.name)).
- If not has\_records.
  - Raise Platform.DoesNotExistError.
- Set succeeded\_logs from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i … at 0 → 0.
- Set failed\_logs from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i … at 0 → 0.
- Set total\_logs from (succeeded\_logs + failed\_logs).
- Set transaction\_log from Platform.\_dict(mapping(“date” → self.name, “count” → total\_logs, “succeeded” → succeeded\_logs, “failed” → failed\_logs)).
- Evaluate super(Document, self).\_\_init\_\_(serialize\_transaction\_log(transaction\_log)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0335.json#L5837) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1355)
