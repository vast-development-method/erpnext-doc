# Employment and attendance · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Interview

[Record definition](../../../../data/record-types/interview.json)

<a id="op-e95dd9777eb034"></a>
### Interview.validate designation

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_validate_designation`

**Inputs** self.

**Record and data access** read “Job Applicant” via get\_value.

**Explicit failure paths** validation helper with DuplicateInterviewRoundError — translated “Interview Type {0} is only for Designation {1}. Job Applicant has applied for the role {2}”.format(self.interview\_type, Platform.bold(self.designation), applicant\_designation).

**Local steps**

- Set applicant\_designation from Platform.db.get\_value(“Job Applicant”, self.job\_applicant, “designation”).
- If self.designation.
  - If self.designation differs from applicant\_designation.
    - Call the validation error handler Platform.throw(translated “Interview Type {0} is only for Designation {1}. Job Applicant has applied for the role {2}”.format(self.interview\_type, Platform.bold(self.designation), applicant\_designation), e ….
- Otherwise.
  - Set self.designation from applicant\_designation.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L3705) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L873) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L853)

<a id="op-020395449faed8"></a>
### Interview.show job applicant update dialog

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_show_job_applicant_update_dialog`

**Inputs** self.

**Record and data access** read “Job Applicant” via get\_value.

**State and service calls** msgprint with translated “Do you want to update the Job Applicant {0} as {1} based on this interview result?”.format(Platform.bold(job\_application\_name), Platform.bold(job\_applicant\_status)).

**Explicit results** no value.

**Local steps**

- Set job\_applicant\_status from self.get\_job\_applicant\_status().
- If not job\_applicant\_status.
  - Return no value.
- Set job\_application\_name from Platform.db.get\_value(“Job Applicant”, self.job\_applicant, “applicant\_name”).
- Evaluate Platform.msgprint(translated “Do you want to update the Job Applicant {0} as {1} based on this interview result?”.format(Platform.bold(job\_application\_name), Platform.bold(job\_applicant\_status)), title = t ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get job applicant status](operations-020.md#op-00e1ac0ea0bec8).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L3950) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L871) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L851)

<a id="op-00e1ac0ea0bec8"></a>
### Interview.get job applicant status

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_get_job_applicant_status`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** status\_map.get(self.status, no value).

**Local steps**

- Set status\_map from mapping(“Cleared” → “Accepted”, “Rejected” → “Rejected”).
- Return status\_map.get(self.status, no value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L4376) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L867) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L847)

<a id="op-395da5766368aa"></a>
### Interview.reschedule interview

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_reschedule_interview`

**Inputs** self, scheduled\_on, from\_time, to\_time.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**State and service calls** msgprint with translated “No changes found in timings.” · call db\_set on self · sendmail · msgprint with translated “Failed to send the Interview Reschedule notification. Please configure your email account.” · msgprint with translated “Interview Rescheduled successfully”.

**Explicit results** no value.

**Local steps**

- If (getdate(scheduled\_on) equals getdate(self.scheduled\_on) and get\_time(from\_time) equals get\_time(self.from\_time) and get\_time(to\_time) equals get\_time(self.to\_time)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(scheduled\_on) equals getdate(self.scheduled\_on) → get\_time(from\_time) equals get\_time(self.from\_time) → get\_time(to\_time) equals get\_time(self.to\_time).
  - Evaluate Platform.msgprint(translated “No changes found in timings.”, indicator = “orange”, title = translated “Interview Not Rescheduled”).
  - Return no value.
- Set original\_date from self.scheduled\_on.
- Set original\_from\_time from self.from\_time.
- Set original\_to\_time from self.to\_time.
- Evaluate self.db\_set(mapping(“scheduled\_on” → scheduled\_on, “from\_time” → from\_time, “to\_time” → to\_time)).
- Evaluate self.notify\_update().
- Set recipients from get\_recipients(self.name).
- Attempt the following.
  - Evaluate Platform.sendmail(recipients = recipients, subject = translated “Interview: {0} Rescheduled”.format(self.name), message = translated “Your Interview session is rescheduled from {0} {1} - {2} to {3} {4} - { ….
- On failure (Exception).
  - Evaluate Platform.msgprint(translated “Failed to send the Interview Reschedule notification. Please configure your email account.”).
- Evaluate Platform.msgprint(translated “Interview Rescheduled successfully”, indicator = “green”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = translated “Interview: {0} Rescheduled”.format(self.name), message = translated “Your Interview session is rescheduled from {0} {1} - {2} to {3} {4} - { ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L35) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L870) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L850)

<a id="op-5deb3117cd9ca5"></a>
### Interview.on discard

`operation_workforce_human_resources_record_definitions_interview_business_behavior_interview_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L5184) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L868) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L848)

<a id="op-cdccb1891d1806"></a>
### Get interviewers

`operation_workforce_human_resources_record_definitions_interview_business_behavior_get_interviewers`

**Inputs** interview\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Interviewer” via get\_all.

**Explicit results** Platform.get\_all(“Interviewer”, filters = mapping(“parent” → interview\_type), fields = list(“user as interviewer”)).

**Local steps**

- Evaluate Platform.has\_permission(“Interview Type”, “read”, interview\_type, throw = true).
- Return Platform.get\_all(“Interviewer”, filters = mapping(“parent” → interview\_type), fields = list(“user as interviewer”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview Type”, “read”, interview\_type, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L5247) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L864) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L844)

<a id="op-a0f296912f5b51"></a>
### Get recipients

`operation_workforce_human_resources_record_definitions_interview_business_behavior_get_recipients`

**Inputs** name, for\_feedback = 0.

**Record and data access** resolve a document from “Interview” via get\_doc · read “Interview Feedback” via get\_all · read “Job Applicant” via get\_value.

**Explicit results** recipients.

**Local steps**

- Set interview from Platform.get\_doc(“Interview”, name).
- Set interviewers from list of d.interviewer for d drawn from interview.interview\_details.
  - Draw d from interview.interview\_details.
- If for\_feedback.
  - Set feedback\_given\_interviewers from Platform.get\_all(“Interview Feedback”, filters = mapping(“interview” → name, “docstatus” → 1), pluck = “interviewer”).
  - Set recipients from list of d for d drawn from interviewers where d does not belong to feedback\_given\_interviewers.
    - Draw d from interviewers, keep a combination only if (d does not belong to feedback\_given\_interviewers).
- Otherwise.
  - Set recipients from interviewers.
  - Evaluate recipients.append(Platform.db.get\_value(“Job Applicant”, interview.job\_applicant, “email\_id”)).
- Return recipients.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L5438) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L865) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L845)

<a id="op-784c815ce6595a"></a>
### Get feedback

`operation_workforce_human_resources_record_definitions_interview_business_behavior_get_feedback`

**Inputs** interview.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i ….

**Local steps**

- Evaluate Platform.has\_permission(“Interview”, “read”, interview, throw = true).
- Evaluate Platform.has\_permission(“Interview Feedback”, “read”, throw = true).
- Set interview\_feedback from Platform.qb.DocType(“Interview Feedback”).
- Set employee from Platform.qb.DocType(“Employee”).
- Return nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview”, “read”, interview, throw = true), Platform.has\_permission(“Interview Feedback”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L34) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L862) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L842)

<a id="op-9257bd54c28e55"></a>
### Get skill wise average rating

`operation_workforce_human_resources_record_definitions_interview_business_behavior_get_skill_wise_average_rating`

**Inputs** interview.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract).groupby(skill\_assessment.skill).orderby(skill\_assessment.idx).run(as\_dict = true).

**Local steps**

- Evaluate Platform.has\_permission(“Interview”, “read”, interview, throw = true).
- Set skill\_assessment from Platform.qb.DocType(“Skill Assessment”).
- Set interview\_feedback from Platform.qb.DocType(“Interview Feedback”).
- Return nested operand in the contract(nested operand in the contract).groupby(skill\_assessment.skill).orderby(skill\_assessment.idx).run(as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview”, “read”, interview, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0035.json#L6350) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L866) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L846)

<a id="op-ad72b1e52d2976"></a>
### Update job applicant status

`operation_workforce_human_resources_record_definitions_interview_business_behavior_update_job_applicant_status`

**Inputs** status, job\_applicant.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Job Applicant” via get\_doc.

**State and service calls** call save on doc · msgprint with translated “Updated the Job Applicant status to {0}”.format(doc.status) · msgprint with translated “Failed to update the Job Applicant status”.

**Explicit failure paths** validation helper — translated “Please specify the job applicant to be updated.”.

**Local steps**

- Attempt the following.
  - If not job\_applicant.
    - Call the validation error handler Platform.throw(translated “Please specify the job applicant to be updated.”).
  - Set doc from Platform.get\_doc(“Job Applicant”, job\_applicant).
  - Set doc.status from status.
  - Evaluate doc.save().
  - Evaluate Platform.msgprint(translated “Updated the Job Applicant status to {0}”.format(doc.status), alert = true, indicator = “green”).
- On failure (Exception).
  - Evaluate Platform.log\_error(“Failed to update Job Applicant status”).
  - Evaluate Platform.msgprint(translated “Failed to update the Job Applicant status”, alert = true, indicator = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0036.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L877) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L857)

<a id="op-c6e8e034deb262"></a>
### Send interview reminder

`operation_workforce_human_resources_record_definitions_interview_business_behavior_send_interview_reminder`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_value · read “HR Settings” via get\_single\_value · read “Interview” via get\_all · resolve a document from “Email Template” via get\_doc · resolve a document from “Interview” via get\_doc.

**State and service calls** sendmail · call db\_set on doc.

**Explicit results** no value.

**Local steps**

- Set reminder\_settings from Platform.db.get\_value(“HR Settings”, “HR Settings”, list(“send\_interview\_reminder”, “interview\_reminder\_template”, “hiring\_sender\_email”), as\_dict = true).
- If not cint(reminder\_settings.send\_interview\_reminder).
  - Return no value.
- Set remind\_before from (cstr(Platform.db.get\_single\_value(“HR Settings”, “remind\_before”)) or “01:00:00”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(Platform.db.get\_single\_value(“HR Settings”, “remind\_before”)) → “01:00:00”.
- Set remind\_before from datetime.datetime.strptime(remind\_before, “%H:%M:%S”).
- Set reminder\_date\_time from (datetime.datetime.now() + datetime.timedelta(hours = remind\_before.hour, minutes = remind\_before.minute, seconds = remind\_before.second)).
- Set interviews from Platform.get\_all(“Interview”, filters = list(list(“scheduled\_on”, “between”, list(nested operand in the contract.datetime.now(), reminder\_date\_time)), list(“status”, “=”, “Pending”), list(“reminded”, “=”,  ….
- Set interview\_template from Platform.get\_doc(“Email Template”, reminder\_settings.interview\_reminder\_template).
- For each d in interviews.
  - Set doc from Platform.get\_doc(“Interview”, d.name).
  - Set context from doc.as\_dict().
  - Set message from Platform.render\_template(interview\_template.response, context).
  - Set recipients from get\_recipients(doc.name).
  - Evaluate Platform.sendmail(sender = reminder\_settings.hiring\_sender\_email, recipients = recipients, subject = interview\_template.subject, message = message, …).
  - Evaluate doc.db\_set(“reminded”, 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “remind\_before”) · clock or generated value from datetime.datetime.now() · service or queued work from Platform.sendmail(sender = reminder\_settings.hiring\_sender\_email, recipients = recipients, subject = interview\_template.subject, message = message, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0036.json#L395) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L876) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L856)

<a id="op-40d60534355a84"></a>
### Send daily feedback reminder

`operation_workforce_human_resources_record_definitions_interview_business_behavior_send_daily_feedback_reminder`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_value · resolve a document from “Email Template” via get\_doc · read “Interview” via get\_all · resolve a document from “Interview” via get\_doc.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Set reminder\_settings from Platform.db.get\_value(“HR Settings”, “HR Settings”, list(“send\_interview\_feedback\_reminder”, “feedback\_reminder\_notification\_template”, “hiring\_sender\_email”), as\_dict = true).
- If not cint(reminder\_settings.send\_interview\_feedback\_reminder).
  - Return no value.
- Set interview\_feedback\_template from Platform.get\_doc(“Email Template”, reminder\_settings.feedback\_reminder\_notification\_template).
- Set interviews from Platform.get\_all(“Interview”, filters = mapping(“status” → “Under Review”, “docstatus” → list(“!=”, 2), “scheduled\_on” → list(“&lt;=”, getdate()), “to\_time” → list(“&lt;=”, nowtime())), pluck = “name”).
- For each interview in interviews.
  - Set recipients from get\_recipients(interview, for\_feedback = 1).
  - Set doc from Platform.get\_doc(“Interview”, interview).
  - Set context from doc.as\_dict().
  - Set message from Platform.render\_template(interview\_feedback\_template.response, context).
  - If len(recipients).
    - Evaluate Platform.sendmail(sender = reminder\_settings.hiring\_sender\_email, recipients = recipients, subject = interview\_feedback\_template.subject, message = message, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(sender = reminder\_settings.hiring\_sender\_email, recipients = recipients, subject = interview\_feedback\_template.subject, message = message, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0036.json#L1218) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L875) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L855)

<a id="op-86e4bd96577339"></a>
### Get expected skill set

`operation_workforce_human_resources_record_definitions_interview_business_behavior_get_expected_skill_set`

**Inputs** interview\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Expected Skill Set” via get\_all.

**Explicit results** Platform.get\_all(“Expected Skill Set”, filters = mapping(“parent” → interview\_type), fields = list(“skill”), order\_by = “idx”).

**Local steps**

- Evaluate Platform.has\_permission(“Interview Type”, “read”, interview\_type, throw = true).
- Return Platform.get\_all(“Expected Skill Set”, filters = mapping(“parent” → interview\_type), fields = list(“skill”), order\_by = “idx”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Interview Type”, “read”, interview\_type, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L33) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L861) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L841)

<a id="op-2c7a1ba0b623e1"></a>
### Create interview feedback

`operation_workforce_human_resources_record_definitions_interview_business_behavior_create_interview_feedback`

**Inputs** data, interview\_name, interviewer, job\_applicant.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** request new\_doc for “Interview Feedback” · call save on interview\_feedback · call submit on interview\_feedback · msgprint with translated “Interview Feedback {0} submitted successfully”.format(get\_link\_to\_form(“Interview Feedback”, interview\_feedback.name)).

**Explicit failure paths** validation helper — translated “Only Interviewer Are allowed to submit Interview Feedback”.

**Local steps**

- Bind dependencies json.
- If isinstance(data, str).
  - Set data from Platform.\_dict(json.loads(data)).
- If Platform.session.user differs from interviewer.
  - Call the validation error handler Platform.throw(translated “Only Interviewer Are allowed to submit Interview Feedback”).
- Set interview\_feedback from Platform.new\_doc(“Interview Feedback”).
- Set interview\_feedback.interview from interview\_name.
- Set interview\_feedback.interviewer from interviewer.
- Set interview\_feedback.job\_applicant from job\_applicant.
- For each d in data.skill\_set.
  - Set d from Platform.\_dict(d).
  - Evaluate interview\_feedback.append(“skill\_assessment”, d).
- Set interview\_feedback.feedback from data.feedback.
- Set interview\_feedback.result from data.result.
- Evaluate interview\_feedback.save().
- Evaluate interview\_feedback.submit().
- Evaluate Platform.msgprint(translated “Interview Feedback {0} submitted successfully”.format(get\_link\_to\_form(“Interview Feedback”, interview\_feedback.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0036.json#L2040) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L859) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L839)

<a id="op-676ac7e6f8da9f"></a>
### Get interviewer list

`operation_workforce_human_resources_record_definitions_interview_business_behavior_get_interviewer_list`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list.

**Record and data access** read “Has Role” via get\_all.

**Explicit results** Platform.get\_all(“Has Role”, limit\_start = start, limit\_page\_length = page\_len, filters = filters, fields = list(“parent”), …).

**Local steps**

- Set filters from list(list(“Has Role”, “parent”, “like”, formatted text %{txt}%), list(“Has Role”, “role”, “=”, “interviewer”), list(“Has Role”, “parenttype”, “=”, “User”)).
- If (filters and isinstance(filters, list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → isinstance(filters, list).
  - Evaluate filters.extend(filters).
- Return Platform.get\_all(“Has Role”, limit\_start = start, limit\_page\_length = page\_len, filters = filters, fields = list(“parent”), …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0036.json#L2632) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L863) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L843)

<a id="op-37a3676f988f48"></a>
### Get events

`operation_workforce_human_resources_record_definitions_interview_business_behavior_get_events`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** execute a supplied database query.

**Explicit results** events.

**Local steps**

- Bind dependencies get\_event\_conditions.
- Set events from list().
- Set event\_color from mapping(“Pending” → “#fff4f0”, “Under Review” → “#d3e8fc”, “Cleared” → “#eaf5ed”, “Rejected” → “#fce7e7”).
- Set conditions from get\_event\_conditions(“Interview”, filters).
- Set interviews from Platform.db.sql(formatted text   SELECT DISTINCT  ′tabInterview′.name, ′tabInterview′.job\_applicant, ′tabInterview′.interview\_type,  ′tabInterview′.scheduled\_on, ′tabIntervi, mapping(“start” → star ….
- For each d in interviews.
  - Set subject\_data from list().
  - For each field in list(“name”, “job\_applicant”, “interview\_type”).
    - If not d.get(field).
      - Continue with the next iteration or loop test.
    - Evaluate subject\_data.append(d.get(field)).
  - Set color from event\_color.get(d.status).
  - Set interview\_data from mapping(“from” → get\_datetime(“{scheduled\_on} {from\_time}”.format(scheduled\_on = d.scheduled\_on, from\_time = (d.from\_time or “00:00:00”))), “to” → get\_datetime(“{scheduled\_on} {to\_time}”.format(scheduled\_o ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.from\_time → “00:00:00”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.to\_time → “00:00:00”.
    - Value choice on color — true gives color, false gives “#89bcde”.
  - Evaluate events.append(interview\_data).
- Return events.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0036.json#L3039) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L860) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L840)

## Record · Interview feedback

[Record definition](../../../../data/record-types/interview_feedback.json)

<a id="op-96fb2b4e19fd65"></a>
### Interview Feedback.validate

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_interviewer().
- Evaluate self.validate\_interview\_date().
- Evaluate self.validate\_duplicate().
- Evaluate self.calculate\_average\_rating().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate interviewer](operations-020.md#op-a1c8843229fa7c), [validate interview date](operations-020.md#op-4fd8585d503097), [validate duplicate](operations-020.md#op-68247eea22b6fa), [calculate average rating](operations-020.md#op-f9b079f553d064).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L2221) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L883) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L863)

<a id="op-cb7268f07d028e"></a>
### Interview Feedback.on submit

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_interview\_average\_rating().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update interview average rating](operations-020.md#op-a91d467aba6cbf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L2332) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L881) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L861)

<a id="op-2a94b3db933d40"></a>
### Interview Feedback.on cancel

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_interview\_average\_rating().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update interview average rating](operations-020.md#op-a91d467aba6cbf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L2383) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L880) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L860)

<a id="op-a1c8843229fa7c"></a>
### Interview Feedback.validate interviewer

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_validate_interviewer`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is not allowed to submit Interview Feedback for the Interview: {1}”.format(Platform.bold(self.interviewer), Platform.bold(self.interview)).

**Local steps**

- Set applicable\_interviewers from get\_applicable\_interviewers(self.interview).
- If self.interviewer does not belong to applicable\_interviewers.
  - Call the validation error handler Platform.throw(translated “{0} is not allowed to submit Interview Feedback for the Interview: {1}”.format(Platform.bold(self.interviewer), Platform.bold(self.interview))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L2434) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L886) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L866)

<a id="op-4fd8585d503097"></a>
### Interview Feedback.validate interview date

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_validate_interview_date`

**Inputs** self.

**Record and data access** read “Interview” via get\_value.

**Explicit failure paths** validation helper — translated “Submission of {0} before {1} is not allowed”.format(Platform.bold(translated “Interview Feedback”), Platform.bold(translated “Interview Scheduled Date”)).

**Local steps**

- Set scheduled\_date from Platform.db.get\_value(“Interview”, self.interview, “scheduled\_on”).
- If (getdate() &lt; getdate(scheduled\_date) and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate() &lt; getdate(scheduled\_date) → self.docstatus equals 1.
  - Call the validation error handler Platform.throw(translated “Submission of {0} before {1} is not allowed”.format(Platform.bold(translated “Interview Feedback”), Platform.bold(translated “Interview Scheduled Date”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L2625) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L885) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L865)

<a id="op-68247eea22b6fa"></a>
### Interview Feedback.validate duplicate

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_validate_duplicate`

**Inputs** self.

**Record and data access** read “Interview Feedback” via exists.

**Explicit failure paths** validation helper — translated “Feedback already submitted for the Interview {0}. Please cancel the previous Interview Feedback {1} to continue.”.format(self.interview, get\_link\_to\_form(“Interview Feedback”, duplicate\_feedback)).

**Local steps**

- Set duplicate\_feedback from Platform.db.exists(“Interview Feedback”, mapping(“interviewer” → self.interviewer, “interview” → self.interview, “docstatus” → 1)).
- If duplicate\_feedback.
  - Call the validation error handler Platform.throw(translated “Feedback already submitted for the Interview {0}. Please cancel the previous Interview Feedback {1} to continue.”.format(self.interview, get\_link\_to\_form(“Interview Feedback”, du ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L2907) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L884) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L864)

<a id="op-f9b079f553d064"></a>
### Interview Feedback.calculate average rating

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_calculate_average_rating`

**Inputs** self.

**Local steps**

- Set total\_rating from 0.
- For each d in self.skill\_assessment.
  - If d.rating.
    - Update total\_rating using + flt(d.rating).
- Set self.average\_rating from flt((total\_rating ÷ len(self.skill\_assessment)) when len(self.skill\_assessment), otherwise 0).
  - Value choice on len(self.skill\_assessment) — true gives (total\_rating ÷ len(self.skill\_assessment)), false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L3134) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L879) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L859)

<a id="op-a91d467aba6cbf"></a>
### Interview Feedback.update interview average rating

`operation_workforce_human_resources_record_definitions_interview_feedback_business_behavior_interview_feedback_update_interview_average_rating`

**Inputs** self.

**Record and data access** resolve a document from “Interview” via get\_doc.

**State and service calls** call db\_set on interview.

**Local steps**

- Set interview\_feedback from Platform.qb.DocType(“Interview Feedback”).
- Set query from nested operand in the contract.qb.from\_(interview\_feedback).where((interview\_feedback.interview equals self.interview bitwise and interview\_feedback.docstatus equals 1)).select(Avg(interview\_feedback.avera ….
- Set data from query.run(as\_dict = true).
- Set average\_rating from data at 0.average.
- Set interview from Platform.get\_doc(“Interview”, self.interview).
- Evaluate interview.db\_set(“average\_rating”, average\_rating).
- Evaluate interview.notify\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0037.json#L3317) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L882) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L862)
