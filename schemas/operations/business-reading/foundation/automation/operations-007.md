# Workflow, automation and dispatch · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Auto repeat

[Record definition](../../../../data/record-types/auto_repeat.json)

<a id="op-c60d805cee8090"></a>
### Auto Repeat.update status

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_update_status`

**Inputs** self.

**Local steps**

- If self.disabled.
  - Set self.status from “Disabled”.
- Otherwise.
  - If self.is\_completed().
    - Set self.status from “Completed”.
  - Otherwise.
    - Set self.status from “Active”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is completed](operations-007.md#op-2e3d61d63a3963).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L3292) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L208)

<a id="op-2e3d61d63a3963"></a>
### Auto Repeat.is completed

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_is_completed`

**Inputs** self.

**Explicit results** (self.end\_date and getdate(self.end\_date) &lt; getdate(today())).

**Local steps**

- Return (self.end\_date and getdate(self.end\_date) &lt; getdate(today())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(self.end\_date) &lt; getdate(today()).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L3413) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L196)

<a id="op-7ecab75bf9d8a1"></a>
### Auto Repeat.get auto repeat schedule

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_get_auto_repeat_schedule`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** schedule\_details.

**Local steps**

- Set schedule\_details from list().
- Set start\_date from getdate(self.start\_date).
- Set end\_date from getdate(self.end\_date).
- If not self.end\_date.
  - Set next\_date from self.get\_next\_schedule\_date(schedule\_date = start\_date).
  - Set row from mapping(“reference\_document” → self.reference\_document, “frequency” → self.frequency, “next\_scheduled\_date” → next\_date).
  - Evaluate schedule\_details.append(row).
- If self.end\_date.
  - Set next\_date from self.get\_next\_schedule\_date(schedule\_date = start\_date, for\_full\_schedule = true).
  - While getdate(next\_date) ≤ getdate(end\_date).
    - Set row from mapping(“reference\_document” → self.reference\_document, “frequency” → self.frequency, “next\_scheduled\_date” → next\_date).
    - Evaluate schedule\_details.append(row).
    - Set next\_date from self.get\_next\_schedule\_date(schedule\_date = next\_date, for\_full\_schedule = true).
- Return schedule\_details.

**Methods declared on this owner** [get next schedule date](operations-007.md#op-f78d102469ea91).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L3517) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L192)

<a id="op-4b26e230609a2c"></a>
### Auto Repeat.create documents

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_create_documents`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - If not Platform.has\_permission(self.reference\_doctype, “read”, self.reference\_document, user = self.owner).
    - Evaluate self.log\_error(translated “Auto repeat skipped. The owner cannot access the reference document.”).
    - Return no value.
  - If (self.generate\_separate\_documents\_for\_each\_assignee and self.assignee).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.generate\_separate\_documents\_for\_each\_assignee → self.assignee.
    - Set new\_docs from self.make\_new\_documents().
  - Otherwise.
    - Set new\_docs from self.make\_new\_document(list of assignee.user for assignee drawn from self.assignee).
      - Draw assignee from self.assignee.
  - If (self.notify\_by\_email and self.recipients).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.notify\_by\_email → self.recipients.
    - If isinstance(new\_docs, list).
      - For each new\_doc in new\_docs.
        - Evaluate self.send\_notification(new\_doc).
    - Otherwise.
      - Evaluate self.send\_notification(new\_docs).
- On failure (Exception).
  - Set error\_log from self.log\_error(translated “Auto repeat failed. Please enable auto repeat after fixing the issues.”).
  - Evaluate self.disable\_auto\_repeat().
  - If (self.reference\_document and not Platform.in\_test).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_document → not Platform.in\_test.
    - Evaluate self.notify\_error\_to\_user(error\_log).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make new documents](operations-007.md#op-dc08a42dcab86d), [make new document](operations-007.md#op-cb9a3f04ee8171), [send notification](operations-007.md#op-0d5041e12d3906), [disable auto repeat](operations-007.md#op-ab9c867578864d), [notify error to user](operations-007.md#op-aef2868eb15d29).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.reference\_doctype, “read”, self.reference\_document, user = self.owner).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L4032) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L188)

<a id="op-dc08a42dcab86d"></a>
### Auto Repeat.make new documents

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_make_new_documents`

**Inputs** self.

**Explicit results** docs.

**Local steps**

- Set docs from list().
- For each assignee in self.assignee.
  - Set new\_doc from self.make\_new\_document(assignee = list(assignee.user)).
  - Evaluate docs.append(new\_doc).
- Return docs.

**Methods declared on this owner** [make new document](operations-007.md#op-cb9a3f04ee8171).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L4544) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L198)

<a id="op-cb9a3f04ee8171"></a>
### Auto Repeat.make new document

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_make_new_document`

**Inputs** self, assignee = no value.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**State and service calls** request copy\_doc for reference\_doc · call insert on new\_doc · call submit on new\_doc.

**Explicit results** new\_doc.

**Local steps**

- Set reference\_doc from Platform.get\_doc(self.reference\_doctype, self.reference\_document).
- Evaluate Platform.has\_permission(self.reference\_doctype, “read”, reference\_doc, user = self.owner, throw = true).
- Set new\_doc from Platform.copy\_doc(reference\_doc, ignore\_no\_copy = false).
- Evaluate self.update\_doc(new\_doc, reference\_doc).
- Set new\_doc.flags.updater\_reference from mapping(“doctype” → self.doctype, “docname” → self.name, “label” → translated “via Auto Repeat”).
- Evaluate new\_doc.insert(ignore\_permissions = true).
- If assignee.
  - Set args from mapping(“assign\_to” → assignee, “doctype” → self.reference\_doctype, “name” → new\_doc.name, “description” → new\_doc.get\_title()).
  - Evaluate assign\_to(args = args).
- If self.submit\_on\_creation.
  - Evaluate new\_doc.submit().
- Return new\_doc.

**Methods declared on this owner** [update doc](operations-007.md#op-f5570cc59fa0e3).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.reference\_doctype, “read”, reference\_doc, user = self.owner, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L4684) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L197)

<a id="op-f5570cc59fa0e3"></a>
### Auto Repeat.update doc

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_update_record`

**Inputs** self, new\_doc, reference\_doc.

**Record and data access** resolve a document from “Auto Repeat” via get\_doc.

**Local steps**

- Set new\_doc.docstatus from 0.
- If new\_doc.meta.get\_field(“set\_posting\_time”).
  - Evaluate new\_doc.set(“set\_posting\_time”, 1).
- If new\_doc.meta.get\_field(“auto\_repeat”).
  - Evaluate new\_doc.set(“auto\_repeat”, self.name).
- For each fieldname in list(“naming\_series”, “ignore\_pricing\_rule”, “posting\_time”, “select\_print\_heading”, …).
  - If new\_doc.meta.get\_field(fieldname).
    - Evaluate new\_doc.set(fieldname, reference\_doc.get(fieldname)).
- For each data in new\_doc.meta.fields.
  - If (data.fieldtype equals “Date” and data.reqd).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.fieldtype equals “Date” → data.reqd.
    - Evaluate new\_doc.set(data.fieldname, self.next\_schedule\_date).
- Evaluate self.set\_auto\_repeat\_period(new\_doc, reference\_doc).
- Set auto\_repeat\_doc from Platform.get\_doc(“Auto Repeat”, self.name).
- Evaluate new\_doc.run\_method(“on\_recurring”, reference\_doc = reference\_doc, auto\_repeat\_doc = auto\_repeat\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set auto repeat period](operations-007.md#op-2f5fdbf745f2f5).

**Values supplied outside this operation** selected callable from new\_doc.run\_method(“on\_recurring”, reference\_doc = reference\_doc, auto\_repeat\_doc = auto\_repeat\_doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L43) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L231) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L207)

<a id="op-2f5fdbf745f2f5"></a>
### Auto Repeat.set auto repeat period

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_set_auto_repeat_period`

**Inputs** self, new\_doc, reference\_doc = no value.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**Explicit results** no value.

**Local steps**

- Set reference\_doc from (reference\_doc or Platform.get\_doc(self.reference\_doctype, self.reference\_document)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doc → Platform.get\_doc(self.reference\_doctype, self.reference\_document).
- Set anchor from reference\_doc.get(“from\_date”).
- If not (anchor and new\_doc.meta.get\_field(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in anchor → new\_doc.meta.get\_field(“to\_date”).
  - Return no value.
- Set schedule\_date from getdate(self.next\_schedule\_date).
- If mcount bound to month\_map.get(self.frequency).
  - Set n from ((month\_diff(schedule\_date, self.start\_date) − 1) floor divide mcount).
- Otherwise.
  - Set n from (date\_diff(schedule\_date, self.start\_date) floor divide day\_map at self.frequency).
- Set tuple(from\_date, to\_date) from get\_auto\_repeat\_period(anchor, self.frequency, n).
- Evaluate new\_doc.set(“from\_date”, from\_date).
- Evaluate new\_doc.set(“to\_date”, to\_date).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L42) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L227) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L203)

<a id="op-f78d102469ea91"></a>
### Auto Repeat.get next schedule date

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_get_next_schedule_date`

**Inputs** self, schedule\_date, for\_full\_schedule = false.

**Explicit results** next\_date.

**Local steps**

- If month\_map.get(self.frequency).
  - Set month\_count from ((month\_map.get(self.frequency) + month\_diff(schedule\_date, self.start\_date)) − 1).
- Otherwise.
  - Set month\_count from 0.
- Set day\_count from 0.
- If month\_count.
  - Set day\_count from 31 when self.repeat\_on\_last\_day, otherwise (self.repeat\_on\_day or no value).
    - Value choice on self.repeat\_on\_last\_day — true gives 31, false gives (self.repeat\_on\_day or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.repeat\_on\_day → no value.
  - Set next\_date from get\_next\_date(self.start\_date, month\_count, day\_count).
- Otherwise.
  - Set days from self.get\_days(schedule\_date).
  - Set next\_date from add\_days(schedule\_date, days).
- If not for\_full\_schedule.
  - While getdate(next\_date) &lt; getdate(today()).
    - If month\_count.
      - Update month\_count using + month\_map.get(self.frequency, 0).
      - Set next\_date from get\_next\_date(self.start\_date, month\_count, day\_count).
    - Otherwise.
      - Set days from self.get\_days(next\_date).
      - Set next\_date from add\_days(next\_date, days).
  - If (self.end\_date and getdate(next\_date) &gt; getdate(self.end\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(next\_date) &gt; getdate(self.end\_date).
    - Set next\_date from schedule\_date.
- Return next\_date.

**Methods declared on this owner** [get days](operations-007.md#op-865fc0cadd52b6).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L218) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L194)

<a id="op-865fc0cadd52b6"></a>
### Auto Repeat.get days

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_get_days`

**Inputs** self, schedule\_date.

**Explicit results** days.

**Local steps**

- If self.frequency equals “Weekly”.
  - Set days from self.get\_offset\_for\_weekly\_frequency(schedule\_date).
- Otherwise.
  - If self.frequency equals “Fortnightly”.
    - Set days from 14.
  - Otherwise.
    - Set days from 1.
- Return days.

**Methods declared on this owner** [get offset for weekly frequency](operations-007.md#op-8310ddde970309).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L638) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L193)

<a id="op-8310ddde970309"></a>
### Auto Repeat.get offset for weekly frequency

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_get_offset_for_weekly_frequency`

**Inputs** self, schedule\_date.

**Explicit results** 7 · timedelta((((7 + next\_weekday\_number) − current\_schedule\_day) modulo or format 7)).days.

**Local steps**

- If not self.repeat\_on\_days.
  - Return 7.
- Set repeat\_on\_days from self.get\_auto\_repeat\_days().
- Set current\_schedule\_day from getdate(schedule\_date).weekday().
- Set weekdays from list(week\_map.keys()).
- If (len(repeat\_on\_days) &gt; 1 or weekdays at current\_schedule\_day does not belong to repeat\_on\_days).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(repeat\_on\_days) &gt; 1 → weekdays at current\_schedule\_day does not belong to repeat\_on\_days.
  - Set weekday from get\_next\_weekday(current\_schedule\_day, repeat\_on\_days).
  - Set next\_weekday\_number from week\_map.get(weekday, 0).
  - Return timedelta((((7 + next\_weekday\_number) − current\_schedule\_day) modulo or format 7)).days.
- Return 7.

**Methods declared on this owner** [get auto repeat days](operations-007.md#op-30e46ef82d0a3d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L794) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L195)

<a id="op-30e46ef82d0a3d"></a>
### Auto Repeat.get auto repeat days

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_get_auto_repeat_days`

**Inputs** self.

**Explicit results** list of d.day for d drawn from self.get(“repeat\_on\_days”, list()).

**Local steps**

- Return list of d.day for d drawn from self.get(“repeat\_on\_days”, list()).
  - Draw d from self.get(“repeat\_on\_days”, list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L1139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L191)

<a id="op-0d5041e12d3906"></a>
### Auto Repeat.send notification

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_send_notification`

**Inputs** self, new\_doc.

**Record and data access** read “Print Format” via get\_cached\_value.

**Local steps**

- Set subject from (self.subject or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.subject → empty text.
- Set message from (self.message or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.message → empty text.
- If not self.subject.
  - Set subject from translated “New {0}: {1}”.format(new\_doc.doctype, new\_doc.name).
- Otherwise.
  - If “{” belongs to self.subject.
    - Set subject from Platform.render\_template(self.subject, mapping(“doc” → new\_doc), restrict\_globals = true).
- Set print\_format from (self.print\_format or Platform.get\_meta(new\_doc.doctype).default\_print\_format).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.print\_format → Platform.get\_meta(new\_doc.doctype).default\_print\_format.
- Set error\_string from no value.
- Set session\_user from Platform.session.user.
- Evaluate Platform.set\_user(self.owner).
- Attempt the following.
  - Set attachments from list(Platform.attach\_print(new\_doc.doctype, new\_doc.name, file\_name = new\_doc.name, print\_format = print\_format, lang = (new\_doc.get(“language”) or Platform.get\_cached\_value(“Print Format”, print\_format, “defau …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_doc.get(“language”) → Platform.get\_cached\_value(“Print Format”, print\_format, “default\_print\_language”) when print\_format, otherwise no value.
    - Value choice on print\_format — true gives Platform.get\_cached\_value(“Print Format”, print\_format, “default\_print\_language”), false gives no value.
- On failure (Platform.PermissionError).
  - Set error\_string from translated “A recurring {0} {1} has been created for you via Auto Repeat {2}.”.format(new\_doc.doctype, new\_doc.name, self.name).
  - Update error\_string using + text in the contract.
  - Update error\_string using + translated “{0}: Failed to attach new recurring document. To enable attaching document in the auto repeat notification e …”.format(Platform.bold(translated “Note”), Platform.bold(translated “Allow Print for Draft”)).
  - Set attachments from no value.
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(session\_user).
- If error\_string.
  - Set message from error\_string.
- Otherwise.
  - If not self.message.
    - Set message from translated “Please find attached {0}: {1}”.format(new\_doc.doctype, new\_doc.name).
  - Otherwise.
    - If “{” belongs to self.message.
      - Set message from Platform.render\_template(self.message, mapping(“doc” → new\_doc), restrict\_globals = true).
- Evaluate make(doctype = new\_doc.doctype, name = new\_doc.name, recipients = self.recipients, subject = subject, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Print Format”, print\_format, “default\_print\_language”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L202)

<a id="op-a59f2d151bddc1"></a>
### Auto Repeat.fetch linked contacts

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_fetch_linked_contacts`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “No contacts linked to document”.

**Local steps**

- If (self.reference\_doctype and self.reference\_document).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_document.
  - Set res from get\_contacts\_linking\_to(self.reference\_doctype, self.reference\_document, fields = list(“email\_id”)).
  - Update res using + get\_contacts\_linked\_from(self.reference\_doctype, self.reference\_document, fields = list(“email\_id”)).
  - Set email\_ids from set of d.email\_id for d drawn from res.
    - Draw d from res.
  - If not email\_ids.
    - Evaluate Platform.msgprint(translated “No contacts linked to document”, alert = true).
  - Otherwise.
    - Set self.recipients from “, ”.join(email\_ids).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L2102) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L190)

<a id="op-ab9c867578864d"></a>
### Auto Repeat.disable auto repeat

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_disable_auto_repeat`

**Inputs** self.

**State and service calls** request set\_value on “Auto Repeat”.

**Local steps**

- Evaluate Platform.db.set\_value(“Auto Repeat”, self.name, “disabled”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L2432) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L189)

<a id="op-aef2868eb15d29"></a>
### Auto Repeat.notify error to user

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_notify_error_to_user`

**Inputs** self, error\_log.

**State and service calls** sendmail.

**Local steps**

- Set recipients from list(get\_system\_managers(only\_name = true)).
- Evaluate recipients.append(self.owner).
- Set subject from translated “Auto Repeat Document Creation Failed”.
- Set form\_link from Platform.utils.get\_link\_to\_form(self.reference\_doctype, self.reference\_document).
- Set auto\_repeat\_failed\_for from translated “Auto Repeat failed for {0}”.format(form\_link).
- Set error\_log\_link from Platform.utils.get\_link\_to\_form(“Error Log”, error\_log.name).
- Set error\_log\_message from translated “Check the Error Log for more information: {0}”.format(error\_log\_link).
- Evaluate Platform.sendmail(recipients = recipients, subject = subject, template = “auto\_repeat\_fail”, args = mapping(“auto\_repeat\_failed\_for” → auto\_repeat\_failed\_for, “error\_log\_message” → error\_log\_message), …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = subject, template = “auto\_repeat\_fail”, args = mapping(“auto\_repeat\_failed\_for” → auto\_repeat\_failed\_for, “error\_log\_message” → error\_log\_message), …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L2518) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L199)

<a id="op-ef8c7f1fc9cd17"></a>
### Get next date

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_get_next_date`

**Inputs** dt, mcount, day = no value.

**Explicit results** dt.

**Local steps**

- Set dt from getdate(dt).
- Update dt using + relativedelta(months = mcount, day = day).
- Return dt.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L2931) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L220)

<a id="op-83f231c09694b1"></a>
### Get auto repeat period

`operation_foundation_binding_foundation_automation_doctype_auto_repeat_auto_repeat_get_auto_repeat_period`

**Inputs** anchor, frequency, n.

**Explicit results** tuple(get\_next\_date(anchor, (n × mcount)), add\_days(get\_next\_date(anchor, ((n + 1) × mcount)), negative 1)) · tuple(from\_date, add\_days(from\_date, (days − 1))).

**Local steps**

- If mcount bound to month\_map.get(frequency).
  - Return tuple(get\_next\_date(anchor, (n × mcount)), add\_days(get\_next\_date(anchor, ((n + 1) × mcount)), negative 1)).
- Set days from day\_map at frequency.
- Set from\_date from add\_days(getdate(anchor), (n × days)).
- Return tuple(from\_date, add\_days(from\_date, (days − 1))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L45) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L261)

<a id="op-e17efbde5d6964"></a>
### Get next weekday

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_get_next_weekday`

**Inputs** current\_schedule\_day, weekdays.

**Explicit results** entry.

**Local steps**

- Set days from list(week\_map.keys()).
- If current\_schedule\_day &gt; 0.
  - Set days from (days at slice (current\_schedule\_day + 1) to no value + days at slice no value to current\_schedule\_day).
- Otherwise.
  - Set days from days at slice (current\_schedule\_day + 1) to no value.
- For each entry in days.
  - If entry belongs to weekdays.
    - Return entry.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L3052) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L245) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L221)

<a id="op-71f540f8966add"></a>
### Make auto repeat entry

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_make_auto_repeat_entry`

**Inputs** no declared parameters.

**State and service calls** enqueue with enqueued\_method.

**Local steps**

- Set enqueued\_method from “Platform.automation.doctype.auto\_repeat.auto\_repeat.create\_repeated\_entries”.
- Set jobs from get\_jobs().
- If (not jobs or enqueued\_method does not belong to jobs at Platform.local.site).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not jobs → enqueued\_method does not belong to jobs at Platform.local.site.
  - Set date from getdate(today()).
  - Set data from get\_auto\_repeat\_entries(date).
  - Evaluate Platform.enqueue(enqueued\_method, data = data, queue = “long”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today() · service or queued work from Platform.enqueue(enqueued\_method, data = data, queue = “long”).

**Boundaries to resolve** external or queued work, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L3291) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L223)

<a id="op-1ca8369ca77bed"></a>
### Create repeated entries

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_create_repeated_entries`

**Inputs** data.

**Record and data access** resolve a document from “Auto Repeat” via get\_doc.

**State and service calls** request set\_value on “Auto Repeat” · call save on doc.

**Local steps**

- For each d in data.
  - Set doc from Platform.get\_doc(“Auto Repeat”, d.name).
  - Set current\_date from getdate(today()).
  - Set schedule\_date from getdate(doc.next\_schedule\_date).
  - If (schedule\_date equals current\_date and not doc.disabled).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule\_date equals current\_date → not doc.disabled.
    - Evaluate doc.create\_documents().
    - Set schedule\_date from doc.get\_next\_schedule\_date(schedule\_date = schedule\_date).
    - If (schedule\_date and not doc.disabled).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule\_date → not doc.disabled.
      - Evaluate Platform.db.set\_value(“Auto Repeat”, doc.name, “next\_schedule\_date”, schedule\_date).
  - If doc.is\_completed().
    - Set doc.status from “Completed”.
    - Evaluate doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L3567) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L216)

<a id="op-f014c533c5ee8d"></a>
### Get auto repeat entries

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_get_auto_repeat_entries`

**Inputs** date = no value.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- If not date.
  - Set date from getdate(today()).
- Set auto\_repeat from Platform.qb.DocType(“Auto Repeat”).
- Set query from Platform.qb.from\_(auto\_repeat).
- Set query from query.select(“name”).
- Set query from query.where(((auto\_repeat.next\_schedule\_date ≤ date bitwise and auto\_repeat.status equals “Active”) bitwise and (auto\_repeat.end\_date ≥ auto\_repeat.next\_schedule\_date bitwise or auto\_repeat.end\_date.isnull()))).
- Return query.run(as\_dict = 1).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L3955) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L218)

<a id="op-d91fdaed69a296"></a>
### Make auto repeat

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_make_auto_repeat`

**Inputs** doctype, docname, frequency = “Daily”, start\_date = no value, end\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Auto Repeat” · call save on doc.

**Explicit results** doc.

**Local steps**

- If not start\_date.
  - Set start\_date from getdate(today()).
- Set doc from Platform.new\_doc(“Auto Repeat”).
- Set doc.reference\_doctype from doctype.
- Set doc.reference\_document from docname.
- Set doc.frequency from frequency.
- Set doc.start\_date from start\_date.
- If end\_date.
  - Set doc.end\_date from end\_date.
- Evaluate doc.save().
- Return doc.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L4293) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L246) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L222)

<a id="op-694e8248902e49"></a>
### Get auto repeat doctypes

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_get_auto_repeat_record_types`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Property Setter” via get\_all · read “DocType” via get\_all.

**Explicit results** list of list(d) for d drawn from docs where txt belongs to d.

**Local steps**

- Set res from Platform.get\_all(“Property Setter”, mapping(“property” → “allow\_auto\_repeat”, “value” → “1”), list(“doc\_type”)).
- Set docs from list of r.doc\_type for r drawn from res.
  - Draw r from res.
- Set res from Platform.get\_all(“DocType”, mapping(“allow\_auto\_repeat” → 1), list(“name”)).
- Update docs using + list of r.name for r drawn from res.
  - Draw r from res.
- Set docs from set(list(docs)).
- Return list of list(d) for d drawn from docs where txt belongs to d.
  - Draw d from docs, keep a combination only if (txt belongs to d).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0014.json#L4656) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L219)
