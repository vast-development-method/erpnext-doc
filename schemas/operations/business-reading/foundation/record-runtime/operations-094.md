# Record lifecycle and persistence · operations 94

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Setup db

<a id="op-019a145a41ffe0"></a>
### Get root connection

`operation_foundation_database_sqlite_setup_persistent_records_business_behavior_get_root_connection`

**Inputs** no declared parameters.

**Explicit results** Platform.local.flags.root\_connection.

**Local steps**

- Set Platform.local.flags.root\_connection from Platform.database.get\_db(cur\_db\_name = Platform.conf.db\_name).
- Return Platform.local.flags.root\_connection.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0148.json#L4430) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1521)

## Record · Sms settings

<a id="op-721fe61a651015"></a>
### Validate receiver nos

`operation_foundation_core_record_definitions_sms_settings_business_behavior_validate_receiver_numbers`

**Inputs** receiver\_list.

**Explicit results** validated\_receiver\_list.

**Local steps**

- Set validated\_receiver\_list from list().
- For each d in receiver\_list.
  - If not d.
    - Continue with the next iteration or loop test.
  - For each x in list(one space, “-”, “(”, “)”).
    - Set d from d.replace(x, empty text).
  - Evaluate validated\_receiver\_list.append(d).
- If not validated\_receiver\_list.
  - Evaluate throw(translated “Please enter valid mobile nos”).
- Return validated\_receiver\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L4394) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L588)

<a id="op-c9b8f80590dbf9"></a>
### Get contact number

`operation_foundation_core_record_definitions_sms_settings_business_behavior_get_contact_number`

**Inputs** contact\_name, ref\_doctype, ref\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Dynamic Link” via exists · read “Contact” via get\_value.

**Explicit results** empty text · ((contact and (contact.mobile\_no or contact.phone)) or empty text).

**Local steps**

- Evaluate Platform.has\_permission(“Contact”, doc = contact\_name, throw = true).
- Evaluate Platform.has\_permission(ref\_doctype, doc = ref\_name, throw = true).
- Set is\_linked from Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → “Contact”, “parent” → contact\_name, “link\_doctype” → ref\_doctype, “link\_name” → ref\_name)).
- If not is\_linked.
  - Return empty text.
- Set contact from Platform.db.get\_value(“Contact”, contact\_name, list(“mobile\_no”, “phone”), as\_dict = true).
- Return ((contact and (contact.mobile\_no or contact.phone)) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (contact and (contact.mobile\_no or contact.phone)) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in contact → (contact.mobile\_no or contact.phone).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in contact.mobile\_no → contact.phone.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Contact”, doc = contact\_name, throw = true), Platform.has\_permission(ref\_doctype, doc = ref\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L4615) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L582)

<a id="op-b937fcabc7a450"></a>
### Check sms permission

`operation_foundation_core_record_definitions_sms_settings_business_behavior_check_short_message_service_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L5043) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L580)

<a id="op-644259e1c0ca5e"></a>
### Send sms

`operation_foundation_core_record_definitions_sms_settings_business_behavior_send_short_message_service`

**Inputs** receiver\_list, msg, sender\_name = empty text, success\_msg = true.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_send\_sms(receiver\_list, msg, sender\_name, success\_msg).

**Local steps**

- Evaluate check\_sms\_permission().
- Return \_send\_sms(receiver\_list, msg, sender\_name, success\_msg).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L5288) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L585)

<a id="op-cab6b83d1bb013"></a>
### Send sms

`operation_foundation_core_record_definitions_sms_settings_business_behavior_send_short_message_service_2`

**Inputs** receiver\_list, msg, sender\_name = empty text, success\_msg = true.

**Record and data access** read “SMS Settings” via get\_single\_value.

**Explicit results** Platform.get\_attr(send\_sms\_hook\_methods at negative 1)(receiver\_list, msg, sender\_name, success\_msg).

**Local steps**

- Set send\_sms\_hook\_methods from Platform.get\_hooks(“send\_sms”).
- If send\_sms\_hook\_methods.
  - Return Platform.get\_attr(send\_sms\_hook\_methods at negative 1)(receiver\_list, msg, sender\_name, success\_msg).
- Bind dependencies json.
- If isinstance(receiver\_list, str).
  - Set receiver\_list from json.loads(receiver\_list).
  - If not isinstance(receiver\_list, list).
    - Set receiver\_list from list(receiver\_list).
- Set receiver\_list from validate\_receiver\_nos(receiver\_list).
- Set arg from mapping(“receiver\_list” → receiver\_list, “message” → Platform.safe\_decode(msg).encode(“utf-8”), “success\_msg” → success\_msg).
- If Platform.db.get\_single\_value(“SMS Settings”, “sms\_gateway\_url”).
  - Evaluate send\_via\_gateway(arg).
- Otherwise.
  - Evaluate msgprint(translated query text (UPDATE)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“send\_sms”), Platform.get\_attr(send\_sms\_hook\_methods at negative 1) · configured or stored value from Platform.db.get\_single\_value(“SMS Settings”, “sms\_gateway\_url”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L5455) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L586)

<a id="op-225bac192f4a5a"></a>
### Send via gateway

`operation_foundation_core_record_definitions_sms_settings_business_behavior_send_via_gateway`

**Inputs** arg.

**Record and data access** resolve a document from “SMS Settings” via get\_doc.

**State and service calls** msgprint with translated “SMS sent successfully”.

**Local steps**

- Set ss from Platform.get\_doc(“SMS Settings”, “SMS Settings”).
- Set headers from get\_headers(ss).
- Set use\_json from headers.get(“Content-Type”) equals “application/json”.
- Set message from Platform.safe\_decode(arg.get(“message”)).
- Set args from mapping(ss.message\_parameter → message).
- For each d in ss.get(“parameters”).
  - If not d.header.
    - Set args at d.parameter from d.value.
- Set success\_list from list().
- For each d in arg.get(“receiver\_list”).
  - Set args at ss.receiver\_parameter from d.
  - Set status from send\_request(ss.sms\_gateway\_url, args, headers, ss.use\_post, …).
  - If 200 ≤ status &lt; 300.
    - Compare adjacent operands in order, stopping at the first false comparison in 200 ≤ status &lt; 300.
    - Evaluate success\_list.append(d).
- If len(success\_list) &gt; 0.
  - Evaluate args.update(arg).
  - Evaluate create\_sms\_log(args, success\_list).
  - If arg.get(“success\_msg”).
    - Evaluate Platform.msgprint(translated “SMS sent successfully”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L5991) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L587)

<a id="op-7ca073c472544e"></a>
### Get headers

`operation_foundation_core_record_definitions_sms_settings_business_behavior_get_headers`

**Inputs** sms\_settings = no value.

**Record and data access** resolve a document from “SMS Settings” via get\_doc.

**Explicit results** headers.

**Local steps**

- If not sms\_settings.
  - Set sms\_settings from Platform.get\_doc(“SMS Settings”, “SMS Settings”).
- Set headers from mapping(“Accept” → “text/plain, text/html, \*/\*”).
- For each d in sms\_settings.get(“parameters”).
  - If d.header equals 1.
    - Evaluate headers.update(mapping(d.parameter → d.value)).
- Return headers.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L6620) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L583)

<a id="op-ed000576b29067"></a>
### Send request

`operation_foundation_core_record_definitions_sms_settings_business_behavior_send_request`

**Inputs** gateway\_url, params, headers = no value, use\_post = false, use\_json = false.

**Explicit results** response.status\_code.

**Explicit failure paths** Platform.ValidationError(translated “SMS gateway request failed”).

**Local steps**

- Bind dependencies requests.
- If not headers.
  - Set headers from get\_headers().
- Set kwargs from mapping(“headers” → headers).
- If use\_json.
  - Set kwargs at “json” from params.
- Otherwise.
  - If use\_post.
    - Set kwargs at “data” from params.
  - Otherwise.
    - Set kwargs at “params” from params.
- Attempt the following.
  - If use\_post.
    - Set response from requests.post(gateway\_url, expanded names kwargs).
  - Otherwise.
    - Set response from requests.get(gateway\_url, expanded names kwargs).
  - Evaluate response.raise\_for\_status().
- On failure (requests.RequestException) bound to e.
  - Set status from getattr(e.response, “status\_code”, no value).
  - Evaluate Platform.log\_error(title = “SMS gateway request failed”, message = formatted text {type(e).\_\_name\_\_} (status {status})).
  - Raise Platform.ValidationError(translated “SMS gateway request failed”) with cause no value.
- Return response.status\_code.

**Values supplied outside this operation** service or queued work from requests.post(gateway\_url, expanded names kwargs), requests.get(gateway\_url, expanded names kwargs) · selected callable from getattr(e.response, “status\_code”, no value).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L36) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L584)

<a id="op-0804e582b9b007"></a>
### Create sms log

`operation_foundation_core_record_definitions_sms_settings_business_behavior_create_short_message_service_log`

**Inputs** args, sent\_to.

**Record and data access** read “DocType” via exists.

**State and service calls** request new\_doc for “SMS Log” · call save on sl.

**Explicit results** no value.

**Local steps**

- If not Platform.db.exists(“DocType”, “SMS Log”).
  - Return no value.
- Set sl from Platform.new\_doc(“SMS Log”).
- Set sl.sent\_on from nowdate().
- Set sl.message from args at “message”.decode(“utf-8”).
- Set sl.no\_of\_requested\_sms from len(args at “receiver\_list”).
- Set sl.requested\_numbers from whitespace '\\n'.join(args at “receiver\_list”).
- Set sl.no\_of\_sent\_sms from len(sent\_to).
- Set sl.sent\_to from whitespace '\\n'.join(sent\_to).
- Set sl.flags.ignore\_permissions from true.
- Evaluate sl.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0106.json#L7203) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L581)

## Record · Submission queue

[Record definition](../../../../data/record-types/submission_queue.json)

<a id="op-56c47723064cf5"></a>
### Submission Queue.created at

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_created_at`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.creation.

**Local steps**

- Return self.creation.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L737) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L600)

<a id="op-faebd3e8d600d4"></a>
### Submission Queue.enqueued by

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_enqueued_by`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.owner.

**Local steps**

- Return self.owner.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L785) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L602)

<a id="op-a8a334d293a6ec"></a>
### Submission Queue.queued doc

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_queued_record`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** resolve a document from self.ref\_doctype via get\_doc.

**Explicit results** getattr(self, “to\_be\_queued\_doc”, Platform.get\_doc(self.ref\_doctype, self.ref\_docname)).

**Local steps**

- Return getattr(self, “to\_be\_queued\_doc”, Platform.get\_doc(self.ref\_doctype, self.ref\_docname)).

**Values supplied outside this operation** selected callable from getattr(self, “to\_be\_queued\_doc”, Platform.get\_doc(self.ref\_doctype, self.ref\_docname)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L831) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L605)

<a id="op-2956c6aa09b9cb"></a>
### Submission Queue.clear old logs

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Submission Queue”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L922) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L599)

<a id="op-dd4ac991094b6f"></a>
### Submission Queue.insert

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_insert`

**Inputs** self, to\_be\_queued\_doc, action.

**State and service calls** call insert on super().

**Local steps**

- Set self.status from “Queued”.
- Set self.to\_be\_queued\_doc from to\_be\_queued\_doc.
- Set self.action\_for\_queuing from action.
- Evaluate super().insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L1107) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L603)

<a id="op-1fbec7dd88dce2"></a>
### Submission Queue.lock

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_dependency_lock`

**Inputs** self.

**Local steps**

- Evaluate self.queued\_doc.lock().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L1248) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L601)

<a id="op-29ab3146cf755f"></a>
### Submission Queue.unlock

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_unlock`

**Inputs** self.

**Local steps**

- Evaluate self.queued\_doc.unlock().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L1301) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L606)

<a id="op-a2b4d321a13f37"></a>
### Submission Queue.update job id

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_update_job_identifier`

**Inputs** self, job\_id.

**State and service calls** request set\_value on self.doctype · commit.

**Local steps**

- Evaluate Platform.db.set\_value(self.doctype, self.name, mapping(“job\_id” → job\_id), update\_modified = false).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L1354) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L608)

<a id="op-cfbeac47413f7a"></a>
### Submission Queue.after insert

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.queue\_action(“background\_submission”, to\_be\_queued\_doc = self.queued\_doc, action\_for\_queuing = self.action\_for\_queuing, timeout = (Platform.get\_system\_settings(“submission\_queue\_timeout”) or 600), enq ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“submission\_queue\_timeout”) → 600.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“submission\_queue\_timeout”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L38) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L597)

<a id="op-c8c2afdf8b2717"></a>
### Submission Queue.background submission

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_background_submission`

**Inputs** self, to\_be\_queued\_doc, action\_for\_queuing.

**State and service calls** rollback · request set\_value on self.doctype.

**Local steps**

- Evaluate self.update\_job\_id(get\_current\_job().id).
- Set \_action from action\_for\_queuing.lower().
- If \_action equals “update”.
  - Set \_action from “submit”.
- Attempt the following.
  - Evaluate getattr(to\_be\_queued\_doc, \_action)().
  - Evaluate add\_data\_to\_monitor(doctype = to\_be\_queued\_doc.doctype, docname = to\_be\_queued\_doc.name, action = \_action, execution\_time = time\_diff\_in\_seconds(now(), self.created\_at), …).
  - Set values from mapping(“status” → “Finished”).
- On failure (Exception).
  - Set values from mapping(“status” → “Failed”, “exception” → Platform.get\_traceback(with\_context = true)).
  - Evaluate Platform.db.rollback().
- Set values at “ended\_at” from now().
- Evaluate Platform.db.set\_value(self.doctype, self.name, values, update\_modified = false).
- Evaluate self.notify(values at “status”, action\_for\_queuing).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update job id](operations-094.md#op-a2b4d321a13f37), [notify](operations-094.md#op-ab0f486757372a).

**Values supplied outside this operation** selected callable from getattr(to\_be\_queued\_doc, \_action) · clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L1585) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L598)

<a id="op-ab0f486757372a"></a>
### Submission Queue.notify

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_notify`

**Inputs** self, submission\_status, action.

**Record and data access** read “User” via get\_value.

**State and service calls** publish realtime with “msgprint”.

**Local steps**

- If submission\_status equals “Failed”.
  - Set doctype from self.doctype.
  - Set docname from self.name.
  - Set message from translated “Action {0} failed on {1} {2}. View it {3}”.
- Otherwise.
  - Set doctype from self.ref\_doctype.
  - Set docname from self.ref\_docname.
  - Set message from translated “Action {0} completed successfully on {1} {2}. View it {3}”.
- Set message\_replacements from tuple(Platform.bold(action), Platform.bold(str(self.ref\_doctype)), Platform.bold(str(self.ref\_docname))).
- Set time\_diff from time\_diff\_in\_seconds(now(), self.created\_at).
- If cint(time\_diff) ≤ 60.
  - Evaluate Platform.publish\_realtime(“msgprint”, mapping(“message” → message.format(expanded message\_replacements, formatted text &lt;a href='/desk/{quote(nested operand in the contract.replace(one space, “-”))}/{quote( ….
    - Value choice on submission\_status equals “Failed” — true gives “red”, false gives “green”.
- Otherwise.
  - Set notification\_doc from mapping(“type” → “Alert”, “document\_type” → doctype, “document\_name” → docname, “subject” → message.format(expanded message\_replacements, “here”)).
  - Set notify\_to from Platform.db.get\_value(“User”, self.enqueued\_by, fieldname = “email”).
  - Evaluate enqueue\_create\_notification(list(notify\_to), notification\_doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now() · service or queued work from Platform.publish\_realtime(“msgprint”, mapping(“message” → message.format(expanded message\_replacements, formatted text &lt;a href='/desk/{quote(nested operand in the contract.replace(one space, “-”))}/{quote( ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L2151) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L604)

<a id="op-c589d7c046be1c"></a>
### Submission Queue.unlock doc

`operation_foundation_core_record_definitions_submission_queue_business_behavior_submission_queue_unlock_record`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Document Unlocked”.

**Explicit results** no value.

**Local steps**

- If self.status differs from “Queued”.
  - Return no value.
- Evaluate self.queued\_doc.unlock().
- Evaluate Platform.msgprint(translated “Document Unlocked”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L2954) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L607)

<a id="op-d380fadea51c92"></a>
### Queue submission

`operation_foundation_core_record_definitions_submission_queue_business_behavior_queue_submission`

**Inputs** doc, action, alert = true.

**Record and data access** read “Submission Queue” via get\_value.

**State and service calls** msgprint with translated “This document has already been queued for {0}. You can track the progress over {1}.”.format(action, formatted text &lt;a href='/desk/submission-queue/{existing\_queue}'&gt;&lt;b&gt;here&lt;/b&gt;&lt;/a&gt;) · request new\_doc for “Submission Queue” · call insert on queue · msgprint with translated “Queued for {0}. You can track the progress over {1}.”.format(action, formatted text &lt;a href='/desk/submission-queue/{queue.name}'&gt;&lt;b&gt;here&lt;/b&gt;&lt;/a&gt;).

**Explicit results** no value.

**Local steps**

- If existing\_queue bound to Platform.db.get\_value(“Submission Queue”, mapping(“ref\_doctype” → doc.doctype, “ref\_docname” → doc.name, “status” → “Queued”)).
  - Evaluate Platform.msgprint(translated “This document has already been queued for {0}. You can track the progress over {1}.”.format(action, formatted text &lt;a href='/desk/submission-queue/{existing\_queue}'&gt;&lt;b&gt;here&lt;/b ….
  - Return no value.
- Set queue from Platform.new\_doc(“Submission Queue”).
- Set queue.ref\_doctype from doc.doctype.
- Set queue.ref\_docname from doc.name.
- Evaluate queue.insert(doc, action).
- If alert.
  - Evaluate Platform.msgprint(translated “Queued for {0}. You can track the progress over {1}.”.format(action, formatted text &lt;a href='/desk/submission-queue/{queue.name}'&gt;&lt;b&gt;here&lt;/b&gt;&lt;/a&gt;), indicator = “green”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L3097) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L596)

<a id="op-a3e3274de884bc"></a>
### Get latest submissions

`operation_foundation_core_record_definitions_submission_queue_business_behavior_get_latest_submissions`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Submission Queue” via get\_value.

**Explicit results** out.

**Local steps**

- Evaluate Platform.has\_permission(doctype, “read”, doc = docname, throw = true).
- Set latest\_submission from Platform.db.get\_value(“Submission Queue”, filters = mapping(“ref\_doctype” → doctype, “ref\_docname” → docname), fieldname = list(“name”, “exception”, “status”)).
- Set out from no value.
- If latest\_submission.
  - Set out from mapping(“latest\_submission” → latest\_submission at 0, “exc” → format\_tb(latest\_submission at 1), “status” → latest\_submission at 2).
- Return out.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, doc = docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L37) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L595)
