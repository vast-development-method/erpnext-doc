# Forms, reports and navigation · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Module onboarding

[Record definition](../../../../data/record-types/module_onboarding.json)

<a id="op-2bec7232071692"></a>
### Capture step update

`operation_foundation_binding_foundation_desk_doctype_module_onboarding_module_onboarding_capture_step_update`

**Inputs** step, field, value.

**Record and data access** read “Onboarding Step” via get\_value · read “Onboarding Step Map” via get\_all.

**Local steps**

- Evaluate capture(STEP\_EVENTS at field when value, otherwise “step\_reopened”, app = “Platform\_onboarding”, properties = mapping(“step” → step, “action” → Platform.db.get\_value(“Onboarding Step”, step, “action”), “on ….
  - Value choice on value — true gives STEP\_EVENTS at field, false gives “step\_reopened”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L265) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L723)

<a id="op-bbf6f723c3db03"></a>
### Capture onboarding completed

`operation_foundation_binding_foundation_desk_doctype_module_onboarding_module_onboarding_capture_onboarding_completed`

**Inputs** onboarding.

**Local steps**

- Evaluate capture(“onboarding\_completed”, app = “Platform\_onboarding”, properties = mapping(“onboarding” → onboarding.name, “module” → onboarding.module)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L264) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L722)

<a id="op-322145a929ee84"></a>
### Can update step

`operation_foundation_binding_foundation_desk_doctype_module_onboarding_module_onboarding_can_update_step`

**Inputs** step.

**Declared result** bool.

**Record and data access** read “Onboarding Step Map” via get\_all · read “Onboarding Permission” via get\_all.

**Explicit results** false · true · bool((roles bitwise and set(allowed))).

**Local steps**

- Set onboardings from Platform.get\_all(“Onboarding Step Map”, filters = mapping(“parenttype” → “Module Onboarding”, “step” → step), pluck = “parent”).
- If not onboardings.
  - Return false.
- Set roles from set(Platform.get\_roles()).
- If IMPLICIT\_ROLE belongs to roles.
  - Return true.
- Set allowed from Platform.get\_all(“Onboarding Permission”, filters = mapping(“parenttype” → “Module Onboarding”, “parent” → list(“in”, onboardings)), pluck = “role”).
- Return bool((roles bitwise and set(allowed))).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L263) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L721)

<a id="op-47f3a2d4490a11"></a>
### Get permitted onboardings

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_get_permitted_onboardings`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Module Onboarding” via get\_all · read “Onboarding Permission” via get\_all.

**Explicit results** mapping() · permitted.

**Local steps**

- Set onboardings from Platform.get\_all(“Module Onboarding”, fields = list(“name”, “module”), order\_by = “creation asc”).
- If not onboardings.
  - Return mapping().
- Set roles from set(Platform.get\_roles()).
- Set allowed\_by\_name from defaultdict(set).
- For each row in Platform.get\_all(“Onboarding Permission”, filters = mapping(“parenttype” → “Module Onboarding”, “parent” → list(“in”, list of o.name for o drawn from onboardings)), fields = list(“parent”, “role”)).
  - Draw o from onboardings.
  - Evaluate allowed\_by\_name at row.parent.add(row.role).
- Set permitted from mapping().
- For each onboarding in onboardings.
  - If (not onboarding.module or onboarding.module belongs to permitted).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not onboarding.module → onboarding.module belongs to permitted.
    - Continue with the next iteration or loop test.
  - If (roles bitwise and (allowed\_by\_name at onboarding.name bitwise or set(IMPLICIT\_ROLE))).
    - Set permitted at onboarding.module from onboarding.name.
- Return permitted.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L1610) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L874)

## Record · Note

[Record definition](../../../../data/record-types/note.json)

<a id="op-8480fba78f9c28"></a>
### Note.validate

`operation_foundation_desk_record_definitions_note_business_behavior_note_validate`

**Inputs** self.

**Local steps**

- If (self.notify\_on\_login and not self.expire\_notification\_on).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.notify\_on\_login → not self.expire\_notification\_on.
  - Set self.expire\_notification\_on from Platform.utils.add\_days(self.creation, 7).
- If (not self.public and self.notify\_on\_login).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.public → self.notify\_on\_login.
  - Set self.notify\_on\_login from 0.
- If not self.content.
  - Set self.content from text in the contract.
- Set self.content from Platform.utils.sanitize\_html(self.content, always\_sanitize = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L2151) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L891)

<a id="op-16ca193641eb20"></a>
### Note.before print

`operation_foundation_desk_record_definitions_note_business_behavior_note_before_print`

**Inputs** self, settings = no value.

**Local steps**

- Set self.print\_heading from self.name.
- Set self.sub\_heading from empty text.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L2401) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L888)

<a id="op-8baf8abba4e90e"></a>
### Note.clear cache

`operation_foundation_desk_record_definitions_note_business_behavior_note_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate Platform.cache.delete\_keys(UNSEEN\_NOTES\_KEY).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L2481) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L889)

<a id="op-df830078464ef7"></a>
### Note.mark seen by

`operation_foundation_desk_record_definitions_note_business_behavior_note_mark_seen_by`

**Inputs** self, user.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If user belongs to list of d.user for d drawn from self.seen\_by.
  - Draw d from self.seen\_by.
  - Return false.
- Evaluate self.append(“seen\_by”, mapping(“user” → user)).
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L2564) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L890)

<a id="op-f543adfb2b6184"></a>
### Mark as seen

`operation_foundation_desk_record_definitions_note_business_behavior_mark_as_seen`

**Inputs** note.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Note” via get\_doc.

**State and service calls** call save on note.

**Local steps**

- Set note from Platform.get\_doc(“Note”, note).
- Evaluate note.check\_permission(“read”).
- Set current\_user from Platform.session.user.
- Attempt the following.
  - Evaluate Platform.set\_user(“Administrator”).
  - Set added from note.mark\_seen\_by(current\_user).
  - If added.
    - Evaluate note.save(ignore\_version = true).
- On exit, including pending return or failure.
  - Evaluate Platform.set\_user(current\_user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from note.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L2720) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L887)

<a id="op-026323dc27b8f1"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_note_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L3004) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L883)

<a id="op-99725a9e624f22"></a>
### Has permission

`operation_foundation_desk_record_definitions_note_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L3117) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L886)

<a id="op-eec4cca55a142f"></a>
### Get unseen notes

`operation_foundation_desk_record_definitions_note_business_behavior_get_unseen_notes`

**Inputs** no declared parameters.

**Explicit results** (Platform.cache.get\_value(formatted text {UNSEEN\_NOTES\_KEY}{Platform.session.user}) or list()).

**Local steps**

- Return (Platform.cache.get\_value(formatted text {UNSEEN\_NOTES\_KEY}{Platform.session.user}) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.get\_value(formatted text {UNSEEN\_NOTES\_KEY}{Platform.session.user}) → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L3204) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L884)

<a id="op-d22daf2abf120a"></a>
### Reset notes

`operation_foundation_desk_record_definitions_note_business_behavior_reset_notes`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.cache.get\_value(formatted text {UNSEEN\_NOTES\_KEY}{Platform.session.user}).

**Local steps**

- Evaluate Platform.cache.set\_value(formatted text {UNSEEN\_NOTES\_KEY}{Platform.session.user}, list()).
- Return Platform.cache.get\_value(formatted text {UNSEEN\_NOTES\_KEY}{Platform.session.user}).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L3295) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L892)

<a id="op-472caf760bca89"></a>
### Get unseen notes

`operation_foundation_desk_record_definitions_note_business_behavior_get_unseen_notes_2`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies ParameterizedValueWrapper, SubQuery.
- Set note from Platform.qb.DocType(“Note”).
- Set nsb from Platform.qb.DocType(“Note Seen By”).as\_(“nsb”).
- Set results from nested operand in the contract(nested operand in the contract).select(note.name, note.title, note.content, note.notify\_on\_every\_login).where(((nested operand in the contract.notify\_on\_login equals 1 bitwis ….
- Evaluate Platform.cache.set\_value(formatted text {UNSEEN\_NOTES\_KEY}{Platform.session.user}, results).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L3457) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L885)

## Record · Notification log

[Record definition](../../../../data/record-types/notification_log.json)

<a id="op-bc3d2920a16ade"></a>
### Notification Log.before insert

`operation_foundation_desk_record_definitions_notification_log_business_behavior_notification_log_before_insert`

**Inputs** self.

**Local steps**

- If (not self.title and self.subject).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.title → self.subject.
  - Set self.title from self.subject.
- If (not self.subject and self.title).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.subject → self.title.
  - Set self.subject from self.title.
- If (not self.description and self.email\_content).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.description → self.email\_content.
  - Set self.description from self.email\_content.
- If (not self.email\_content and self.description).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.email\_content → self.description.
  - Set self.email\_content from self.description.
- If (not self.app and self.document\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.app → self.document\_type.
  - Set self.app from \_resolve\_app\_for\_doctype(self.document\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L5638) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L912)

<a id="op-1c7082c52033a8"></a>
### Notification Log.after insert

`operation_foundation_desk_record_definitions_notification_log_business_behavior_notification_log_after_insert`

**Inputs** self.

**State and service calls** publish realtime with “notification”.

**Local steps**

- Evaluate Platform.publish\_realtime(“notification”, after\_commit = true, user = self.for\_user).
- Evaluate set\_notifications\_as\_unseen(self.for\_user).
- If is\_email\_notifications\_enabled\_for\_type(self.for\_user, self.type).
  - Attempt the following.
    - Evaluate send\_notification\_email(self).
  - On failure (Platform.OutgoingEmailError).
    - Evaluate self.log\_error(translated “Failed to send notification email”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“notification”, after\_commit = true, user = self.for\_user).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L5952) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L911)

<a id="op-d966e2f2c75db0"></a>
### Notification Log.clear old logs

`operation_foundation_desk_record_definitions_notification_log_business_behavior_notification_log_clear_old_logs`

**Inputs** days = 180.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Notification Log”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6178) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L913)

<a id="op-ae2f6ac3eefaf5"></a>
### Resolve app for doctype

`operation_foundation_desk_record_definitions_notification_log_business_behavior_resolve_application_for_record_type`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Explicit results** get\_module\_app(get\_doctype\_module(doctype)) · no value.

**Local steps**

- Bind dependencies get\_doctype\_module, get\_module\_app.
- Attempt the following.
  - Return get\_module\_app(get\_doctype\_module(doctype)).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6363) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L914)

<a id="op-6e1a5e97c4f513"></a>
### Get skip email types

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_skip_email_types`

**Inputs** no declared parameters.

**Declared result** set at str.

**Explicit results** set((Platform.get\_hooks(“notification\_skip\_email\_types”) or list())).

**Local steps**

- Return set((Platform.get\_hooks(“notification\_skip\_email\_types”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“notification\_skip\_email\_types”) → list().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“notification\_skip\_email\_types”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6505) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L902)

<a id="op-49b46417ac62e9"></a>
### Get self notify types

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_self_notify_types`

**Inputs** no declared parameters.

**Declared result** set at str.

**Explicit results** set((Platform.get\_hooks(“notification\_self\_notify\_types”) or list())).

**Local steps**

- Return set((Platform.get\_hooks(“notification\_self\_notify\_types”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“notification\_self\_notify\_types”) → list().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“notification\_self\_notify\_types”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6588) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L901)

<a id="op-84ce3dfe8a749f"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** for\_user.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6671) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L900)

<a id="op-b08265621bfad7"></a>
### Has permission

`operation_foundation_desk_record_definitions_notification_log_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6812) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L906)

<a id="op-24c1293873581b"></a>
### Get title

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_title`

**Inputs** doctype, docname, title\_field = no value.

**Record and data access** read doctype via get\_value.

**Explicit results** docname · (Platform.db.get\_value(doctype, docname, title\_field) or docname).

**Local steps**

- If not title\_field.
  - Set title\_field from Platform.get\_meta(doctype).get\_title\_field().
- If title\_field equals “name”.
  - Return docname.
- Return (Platform.db.get\_value(doctype, docname, title\_field) or docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(doctype, docname, title\_field) → docname.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6944) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L903)

<a id="op-216ee91b71b8e9"></a>
### Get title html

`operation_foundation_desk_record_definitions_notification_log_business_behavior_get_title_document_markup`

**Inputs** title.

**Explicit results** formatted text &lt;b class="subject-title"&gt;{title}&lt;/b&gt;.

**Local steps**

- Return formatted text &lt;b class="subject-title"&gt;{title}&lt;/b&gt;.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L7125) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L904)
