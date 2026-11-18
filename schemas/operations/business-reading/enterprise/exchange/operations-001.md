# Integrations and service calls · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Call log

[Record definition](../../../../data/record-types/call_log.json)

<a id="op-c897616f2bffba"></a>
### Call Log.validate

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_validate`

**Inputs** self.

**Local steps**

- Evaluate deduplicate\_dynamic\_links(self).
- If (not self.is\_new() and self.is\_incoming\_call() and self.has\_value\_changed(“to”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.is\_incoming\_call() → self.has\_value\_changed(“to”).
  - Evaluate self.update\_received\_by().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is incoming call](operations-001.md#op-a2faab25354e93), [update received by](operations-001.md#op-1ab814bc91c862).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1325)

<a id="op-1332b361cd089d"></a>
### Call Log.before insert

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_before_insert`

**Inputs** self.

**Local steps**

- Set number from self.get(“from”) when self.is\_incoming\_call(), otherwise self.get(“to”).
  - Value choice on self.is\_incoming\_call() — true gives self.get(“from”), false gives self.get(“to”).
- For each contact in get\_contacts\_with\_phone\_number(number).
  - Evaluate self.add\_link(link\_type = “Contact”, link\_name = contact).
  - Evaluate self.link\_customer\_of\_contact(contact).
- For each lead in get\_leads\_with\_phone\_number(number).
  - Evaluate self.add\_link(link\_type = “Lead”, link\_name = lead).
- If self.is\_incoming\_call().
  - Evaluate self.update\_received\_by().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is incoming call](operations-001.md#op-a2faab25354e93), [add link](operations-001.md#op-747ed2428fbdfd), [link customer of contact](operations-001.md#op-88018e20bd2119), [update received by](operations-001.md#op-1ab814bc91c862).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1318)

<a id="op-92635d967db79b"></a>
### Call Log.after insert

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.trigger\_call\_popup().

If control reaches the end, it returns no value.

**Methods declared on this owner** [trigger call popup](operations-001.md#op-c7bc320a10fc7f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L6677) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L89) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1317)

<a id="op-8339b8d14ede95"></a>
### Call Log.on update

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind local operation \_is\_call\_missed for subsequent calls.
- Bind local operation \_is\_call\_ended for subsequent calls.
- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- If \_is\_call\_missed(doc\_before\_save, self).
  - Evaluate self.notify\_call\_agents(doc\_before\_save, “missed”).
  - Evaluate self.trigger\_call\_popup().
- If \_is\_call\_ended(doc\_before\_save, self).
  - Evaluate self.notify\_call\_agents(doc\_before\_save, “ended”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify call agents](operations-001.md#op-c6148121bda8f8), [trigger call popup](operations-001.md#op-c7bc320a10fc7f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1320)

<a id="op-7faa0636da6a1f"></a>
### Call Log.on update.is call missed

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_on_update_is_call_missed`

**Inputs** doc\_before\_save, doc\_after\_save.

**Explicit results** (doc\_before\_save.to differs from doc\_after\_save.to and doc\_after\_save.status does not belong to END\_CALL\_STATUSES).

**Local steps**

- Return (doc\_before\_save.to differs from doc\_after\_save.to and doc\_after\_save.status does not belong to END\_CALL\_STATUSES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save.to differs from doc\_after\_save.to → doc\_after\_save.status does not belong to END\_CALL\_STATUSES.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L7205) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1322)

<a id="op-455908ab25bbee"></a>
### Call Log.on update.is call ended

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_on_update_is_call_ended`

**Inputs** doc\_before\_save, doc\_after\_save.

**Explicit results** (doc\_before\_save.status does not belong to END\_CALL\_STATUSES and self.status belongs to END\_CALL\_STATUSES).

**Local steps**

- Return (doc\_before\_save.status does not belong to END\_CALL\_STATUSES and self.status belongs to END\_CALL\_STATUSES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save.status does not belong to END\_CALL\_STATUSES → self.status belongs to END\_CALL\_STATUSES.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L7295) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1321)

<a id="op-c6148121bda8f8"></a>
### Call Log.notify call agents

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_calllog_notify_call_agents`

**Inputs** self, doc\_before\_save, event.

**State and service calls** publish realtime with formatted text call\_{self.id}\_{event}.

**Local steps**

- For each email in doc\_before\_save.get\_agent\_emails().
  - Evaluate Platform.publish\_realtime(formatted text call\_{self.id}\_{event}, self, user = email).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(formatted text call\_{self.id}\_{event}, self, user = email).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L11) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1292)

<a id="op-a2faab25354e93"></a>
### Call Log.is incoming call

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_is_incoming_call`

**Inputs** self.

**Explicit results** self.type equals “Incoming”.

**Local steps**

- Return self.type equals “Incoming”.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0976.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1319)

<a id="op-747ed2428fbdfd"></a>
### Call Log.add link

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_add_link`

**Inputs** self, link\_type, link\_name.

**Local steps**

- Evaluate self.append(“links”, mapping(“link\_doctype” → link\_type, “link\_name” → link\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0976.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1316)

<a id="op-88018e20bd2119"></a>
### Call Log.link customer of contact

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_calllog_link_customer_of_contact`

**Inputs** self, contact.

**Record and data access** read “Dynamic Link” via get\_value.

**Local steps**

- Set customer from Platform.db.get\_value(“Dynamic Link”, mapping(“parenttype” → “Contact”, “parent” → contact, “link\_doctype” → “Customer”), “link\_name”).
- If customer.
  - Set self.customer from (self.customer or customer).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.customer → customer.
  - Evaluate self.add\_link(link\_type = “Customer”, link\_name = customer).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add link](operations-001.md#op-747ed2428fbdfd).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L10) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1291)

<a id="op-c7bc320a10fc7f"></a>
### Call Log.trigger call popup

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_trigger_call_popup`

**Inputs** self.

**State and service calls** publish realtime with “show\_call\_popup”.

**Explicit results** no value.

**Local steps**

- If not self.is\_incoming\_call().
  - Return no value.
- Set scheduled\_employees from get\_scheduled\_employees\_for\_popup(self.medium).
- Set employees from get\_employees\_with\_number(self.to).
- Set employee\_emails from list of employee.get(“user\_id”) for employee drawn from employees.
  - Draw employee from employees.
- Set emails from set(scheduled\_employees).intersection(employee\_emails).
- If Platform.conf.developer\_mode.
  - Evaluate self.add\_comment(text = formatted text   Scheduled Employees: {scheduled\_employees}  Matching Employee: {employee\_emails}  Show Popup To: {emails}  ).
- If (employee\_emails and not emails).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee\_emails → not emails.
  - Evaluate self.add\_comment(text = translated “No employee was scheduled for call popup”).
- For each email in emails.
  - Evaluate Platform.publish\_realtime(“show\_call\_popup”, self, user = email).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is incoming call](operations-001.md#op-a2faab25354e93).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“show\_call\_popup”, self, user = email).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0976.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1323)

<a id="op-312a55da7492c7"></a>
### Call Log.get agent emails

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_calllog_get_agent_emails`

**Inputs** self.

**Declared result** set at str.

**Explicit results** set() · set of employee.get(“user\_id”) for employee drawn from get\_employees\_with\_number(self.to).

**Local steps**

- If not self.is\_incoming\_call().
  - Return set().
- Return set of employee.get(“user\_id”) for employee drawn from get\_employees\_with\_number(self.to).
  - Draw employee from get\_employees\_with\_number(self.to).

**Methods declared on this owner** [is incoming call](operations-001.md#op-a2faab25354e93).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L9) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1290)

<a id="op-1ab814bc91c862"></a>
### Call Log.update received by

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_call_log_update_received_by`

**Inputs** self.

**Local steps**

- If employees bound to get\_employees\_with\_number(self.get(“to”)).
  - Set self.call\_received\_by from employees at 0.get(“name”).
  - Set self.employee\_user\_id from employees at 0.get(“user\_id”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0976.json#L602) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1324)

<a id="op-2b6ef08ddb034c"></a>
### Add call summary and call type

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_add_call_summary_and_call_type`

**Inputs** call\_log, summary, call\_type = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Call Log” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Evaluate validate\_call\_type(call\_type).
- Set doc from Platform.get\_doc(“Call Log”, call\_log).
- Evaluate doc.check\_permission(“read”).
- If doc.employee\_user\_id differs from Platform.session.user.
  - Evaluate doc.check\_permission(“write”).
- If call\_type.
  - Set doc.type\_of\_call from call\_type.
- Set doc.summary from summary.
- Evaluate doc.save(ignore\_permissions = true).
- Evaluate doc.add\_comment(“Comment”, ((Platform.bold(translated “Call Summary”) + text in the contract) + summary)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”), doc.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L87) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1315)

<a id="op-5d408e2c677a08"></a>
### Has permission

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L16) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1297)

<a id="op-cddb126540b09b"></a>
### Get permission query conditions

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L13) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1294)

<a id="op-33f9cc4816e782"></a>
### Has unrestricted access

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_has_unrestricted_access`

**Inputs** user.

**Declared result** bool.

**Explicit results** any(generator of (perm.get(“read”) and not perm.get(“permlevel”) and perm.get(“role”) differs from RESTRICTED\_ROLE) for perm drawn from get\_valid\_perms(“Call Log”, user)).

**Local steps**

- Return any(generator of (perm.get(“read”) and not perm.get(“permlevel”) and perm.get(“role”) differs from RESTRICTED\_ROLE) for perm drawn from get\_valid\_perms(“Call Log”, user)).
  - Draw perm from get\_valid\_perms(“Call Log”, user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in perm.get(“read”) → not perm.get(“permlevel”) → perm.get(“role”) differs from RESTRICTED\_ROLE.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L17) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1298)

<a id="op-abc1cbafbdf266"></a>
### Validate call type

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_validate_call_type`

**Inputs** call\_type.

**Record and data access** read “Telephony Call Type” via get\_value.

**Explicit failure paths** validation helper — translated “Call Type {0} is not submitted.”.format(Platform.bold(call\_type)).

**Local steps**

- If (call\_type and Platform.db.get\_value(“Telephony Call Type”, call\_type, “docstatus”) differs from 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in call\_type → Platform.db.get\_value(“Telephony Call Type”, call\_type, “docstatus”) differs from 1.
  - Call the validation error handler Platform.throw(translated “Call Type {0} is not submitted.”.format(Platform.bold(call\_type))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L18) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1299)

<a id="op-ebcde3e5c1e7d6"></a>
### Get employees with number

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_get_employees_with_number`

**Inputs** number.

**Record and data access** read “Employee” via get\_all.

**Explicit results** list() · employee\_doc\_name\_and\_emails.

**Local steps**

- Set key from get\_phone\_number\_key(number).
- If not key.
  - Return list().
- Set employee\_doc\_name\_and\_emails from Platform.cache().hget(“employees\_with\_number”, key).
- If employee\_doc\_name\_and\_emails.
  - Return employee\_doc\_name\_and\_emails.
- Set employees from Platform.get\_all(“Employee”, filters = mapping(“cell\_number” → list(“like”, get\_phone\_number\_like\_pattern(key)), “user\_id” → list(“!=”, empty text)), fields = list(“name”, “user\_id”, “cell\_number”)).
- Set employee\_doc\_name\_and\_emails from list of Platform.\_dict(name = employee.name, user\_id = employee.user\_id) for employee drawn from employees where get\_phone\_number\_key(employee.cell\_number) equals key.
  - Draw employee from employees, keep a combination only if (get\_phone\_number\_key(employee.cell\_number) equals key).
- Evaluate Platform.cache().hset(“employees\_with\_number”, key, employee\_doc\_name\_and\_emails).
- Return employee\_doc\_name\_and\_emails.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1326)

<a id="op-934fdea059d56f"></a>
### Link existing conversations

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_link_existing_conversations`

**Inputs** doc, state.

**Record and data access** resolve a document from “Call Log” via get\_doc.

**State and service calls** savepoint “link\_call\_logs” · call save on call\_log · rollback.

**Explicit results** no value.

**Local steps**

- If doc.flags.ignore\_auto\_link\_call\_log.
  - Return no value.
- Set numbers from get\_new\_phone\_numbers(doc).
- If not numbers.
  - Return no value.
- Evaluate Platform.db.savepoint(“link\_call\_logs”).
- Attempt the following.
  - For each number in numbers.
    - For each log in get\_unlinked\_call\_logs\_with\_number(doc, number).
      - Set call\_log from Platform.get\_doc(“Call Log”, log).
      - Evaluate call\_log.add\_link(link\_type = doc.doctype, link\_name = doc.name).
      - If (doc.doctype equals “Contact” and not call\_log.customer).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Contact” → not call\_log.customer.
        - Evaluate call\_log.link\_customer\_of\_contact(doc.name).
      - Evaluate call\_log.save(ignore\_permissions = true).
- On failure (Exception).
  - Evaluate Platform.db.rollback(save\_point = “link\_call\_logs”).
  - Evaluate Platform.log\_error(title = translated “Error during caller information update”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1328)

<a id="op-c2fc42f67b2552"></a>
### Get unlinked call logs with number

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_get_unlinked_call_logs_with_number`

**Inputs** doc, number.

**Declared result** list at str.

**Explicit results** list() · list of log.name for log drawn from logs where key belongs to tuple(get\_phone\_number\_key(log at “from”), get\_phone\_number\_key(log.to)).

**Local steps**

- If not key bound to get\_phone\_number\_key(number).
  - Return list().
- Set pattern from get\_phone\_number\_like\_pattern(key).
- Set call\_log from Platform.qb.DocType(“Call Log”).
- Set dynamic\_link from Platform.qb.DocType(“Dynamic Link”).
- Set logs from nested operand in the contract(nested operand in the contract).groupby(call\_log.name, call\_log at “from”, call\_log at “to”).having(Sum(nested operand in the contract.else\_(0)) equals 0).run(as\_dict = true).
- Return list of log.name for log drawn from logs where key belongs to tuple(get\_phone\_number\_key(log at “from”), get\_phone\_number\_key(log.to)).
  - Draw log from logs, keep a combination only if (key belongs to tuple(get\_phone\_number\_key(log at “from”), get\_phone\_number\_key(log.to))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L15) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1296)

<a id="op-cd03e1abb869f0"></a>
### Get new phone numbers

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_get_new_phone_numbers`

**Inputs** doc.

**Declared result** set at str.

**Explicit results** numbers.

**Local steps**

- Set numbers from set(get\_phone\_numbers(doc)).
- If doc\_before\_save bound to doc.get\_doc\_before\_save().
  - Update numbers using − set(get\_phone\_numbers(doc\_before\_save)).
- Return numbers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L12) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1293)

<a id="op-f3bf5517889ff8"></a>
### Get phone numbers

`operation_enterprise_binding_enterprise_telephony_doctype_call_log_call_log_get_phone_numbers`

**Inputs** doc.

**Declared result** list at str.

**Explicit results** list of number for number drawn from numbers where number.

**Local steps**

- If doc.doctype equals “Contact”.
  - Set numbers from list of d.phone for d drawn from doc.phone\_nos.
    - Draw d from doc.phone\_nos.
- Otherwise.
  - Set numbers from list(doc.get(“phone”), doc.get(“mobile\_no”)).
- Return list of number for number drawn from numbers where number.
  - Draw number from numbers, keep a combination only if (number).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L14) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1295)

<a id="op-be766644df5f5f"></a>
### Get linked call logs

`operation_enterprise_telephony_record_definitions_call_log_business_behavior_get_linked_call_logs`

**Inputs** doctype, docname.

**Record and data access** read “Dynamic Link” via get\_all · read “Call Log” via get\_list.

**Explicit results** list() · timeline\_contents.

**Local steps**

- If not Platform.has\_permission(“Call Log”, “read”).
  - Return list().
- Set logs from Platform.get\_all(“Dynamic Link”, fields = list(“parent”), filters = mapping(“parenttype” → “Call Log”, “link\_doctype” → doctype, “link\_name” → docname)).
- If not logs.
  - Return list().
- Set logs from set of log.parent for log drawn from logs.
  - Draw log from logs.
- Set logs from Platform.get\_list(“Call Log”, fields = list(“name”, “type”, “from”, “to”, …), filters = mapping(“name” → list(“in”, logs))).
- Set timeline\_contents from list().
- For each log in logs.
  - Set log.show\_call\_button from 0.
  - Evaluate timeline\_contents.append(mapping(“icon” → “phone”, “is\_card” → true, “creation” → log.creation, “template” → “call\_link”, …)).
- Return timeline\_contents.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Call Log”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1327)
