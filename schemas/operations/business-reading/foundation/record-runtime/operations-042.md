# Record lifecycle and persistence · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-7eac18ffc32aae"></a>
### Document.restore masked fields from db

`operation_foundation_model_document_business_behavior_document_restore_masked_fields_from_database`

**Inputs** self.

**Record and data access** resolve a document from self.doctype via get\_doc.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_install or Platform.session.user equals “Administrator” or self.is\_new()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.session.user equals “Administrator” → self.is\_new().
  - Return no value.
- Set mask\_fields from self.meta.get\_masked\_fields().
- Set child\_mask\_fields from mapping of table\_field.fieldname → masked for table\_field drawn from self.meta.get\_table\_fields() where masked bound to Platform.get\_meta(table\_field.options).get\_masked\_fields(parenttype = self.doctype).
  - Draw table\_field from self.meta.get\_table\_fields(), keep a combination only if (masked bound to Platform.get\_meta(table\_field.options).get\_masked\_fields(parenttype = self.doctype)).
- If (not mask\_fields and not child\_mask\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not mask\_fields → not child\_mask\_fields.
  - Return no value.
- Set db\_doc from Platform.get\_doc(self.doctype, self.name).
- For each df in mask\_fields.
  - Evaluate self.set(df.fieldname, db\_doc.get(df.fieldname)).
- For each tuple(fieldname, masked) in child\_mask\_fields.items().
  - Set db\_rows from mapping of row.name → row for row drawn from db\_doc.get(fieldname).
    - Draw row from db\_doc.get(fieldname).
  - For each row in (self.get(fieldname) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(fieldname) → list().
    - Set db\_row from db\_rows.get(row.name).
    - If not db\_row.
      - Continue with the next iteration or loop test.
    - For each df in masked.
      - Evaluate row.set(df.fieldname, db\_row.get(df.fieldname)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371), [set](operations-045.md#op-b58a481a5882b4), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L3396) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1010)

<a id="op-d8cda0d8ca39a4"></a>
### Document.validate higher perm levels

`operation_foundation_model_document_business_behavior_document_validate_higher_permission_levels`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.flags.ignore\_permissions or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.ignore\_permissions → Platform.flags.in\_install.
  - Return no value.
- If Platform.session.user equals “Administrator”.
  - Return no value.
- Set has\_access\_to from self.get\_permlevel\_access().
- Set high\_permlevel\_fields from self.meta.get\_high\_permlevel\_fields().
- If high\_permlevel\_fields.
  - Evaluate self.reset\_values\_if\_no\_permlevel\_access(has\_access\_to, high\_permlevel\_fields).
- If self.is\_new().
  - Return no value.
- For each df in self.meta.get\_table\_fields().
  - Set high\_permlevel\_fields from Platform.get\_meta(df.options).get\_high\_permlevel\_fields().
  - If high\_permlevel\_fields.
    - For each d in self.get(df.fieldname).
      - Evaluate d.reset\_values\_if\_no\_permlevel\_access(has\_access\_to, high\_permlevel\_fields).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get permlevel access](operations-042.md#op-a3ee87a4360b5d), [reset values if no permlevel access](operations-047.md#op-9efa21377582a6), [is new](operations-046.md#op-e2def851dd1371), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L4028) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1042)

<a id="op-a3ee87a4360b5d"></a>
### Document.get permlevel access

`operation_foundation_model_document_business_behavior_document_get_permission_level_access`

**Inputs** self, permission\_type = “write”.

**Explicit results** allowed\_permlevels.

**Local steps**

- Set allowed\_permlevels from list().
- Set roles from Platform.get\_roles().
- For each perm in self.get\_permissions().
  - If (perm.role belongs to roles and perm.get(permission\_type) and perm.permlevel does not belong to allowed\_permlevels).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in perm.role belongs to roles → perm.get(permission\_type) → perm.permlevel does not belong to allowed\_permlevels.
    - Evaluate allowed\_permlevels.append(perm.permlevel).
- Return allowed\_permlevels.

**Methods declared on this owner** [get permissions](operations-042.md#op-aa6a8545e6b1cf).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L4402) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L971)

<a id="op-8336ec83dd8b19"></a>
### Document.has permlevel access to

`operation_foundation_model_document_business_behavior_document_has_permission_level_access_to`

**Inputs** self, fieldname, df = no value, permission\_type = “read”.

**Explicit results** df.permlevel belongs to self.get\_permlevel\_access(permission\_type).

**Local steps**

- If not df.
  - Set df from self.meta.get\_field(fieldname).
- Return df.permlevel belongs to self.get\_permlevel\_access(permission\_type).

**Methods declared on this owner** [get permlevel access](operations-042.md#op-a3ee87a4360b5d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L4627) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L981)

<a id="op-aa6a8545e6b1cf"></a>
### Document.get permissions

`operation_foundation_model_document_business_behavior_document_get_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L4782) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L972)

<a id="op-260bfc0ce25898"></a>
### Document.set defaults

`operation_foundation_model_document_business_behavior_document_set_defaults`

**Inputs** self.

**State and service calls** request new\_doc for self.doctype · request new\_doc for df.options.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_import.
  - Return no value.
- If self.is\_new().
  - Set new\_doc from Platform.new\_doc(self.doctype, as\_dict = true).
  - Evaluate self.update\_if\_missing(new\_doc).
- For each df in self.meta.get\_table\_fields().
  - Set new\_doc from Platform.new\_doc(df.options, parent\_doc = self, parentfield = df.fieldname, as\_dict = true).
  - Set value from self.get(df.fieldname).
  - If isinstance(value, list).
    - For each d in value.
      - If d.is\_new().
        - Evaluate d.update\_if\_missing(new\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371), [update if missing](operations-045.md#op-1cf98cd7adffc8), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L4899) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1023)

<a id="op-0148e812fab947"></a>
### Document.check if latest

`operation_foundation_model_document_business_behavior_document_check_if_latest`

**Inputs** self.

**State and service calls** msgprint with ((translated formatted text Error: {self.name} ({self.doctype}) has been modified after you have opened it + formatted text  ({previous.modified}, {self.modified}). ) + translated “Please refresh to get th ….

**Explicit results** no value.

**Local steps**

- Evaluate self.load\_doc\_before\_save(raise\_exception = true).
- If not hasattr(self, “\_action”).
  - Set self.\_action from “save”.
- Set previous from self.\_doc\_before\_save.
- If (not previous and self.\_action differs from “discard”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not previous → self.\_action differs from “discard”.
  - Evaluate self.check\_docstatus\_transition(0).
  - Return no value.
- Set previous\_modified from get\_datetime(previous.modified) when previous.modified, otherwise no value.
  - Value choice on previous.modified — true gives get\_datetime(previous.modified), false gives no value.
- Set original\_modified from get\_datetime(self.\_original\_modified) when self.\_original\_modified, otherwise no value.
  - Value choice on self.\_original\_modified — true gives get\_datetime(self.\_original\_modified), false gives no value.
- If previous\_modified differs from original\_modified.
  - Evaluate Platform.msgprint(((translated formatted text Error: {self.name} ({self.doctype}) has been modified after you have opened it + formatted text  ({previous.modified}, {self.modified}). ) + translated “Please ….
- If (not self.meta.issingle and self.\_action differs from “discard”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.issingle → self.\_action differs from “discard”.
  - Evaluate self.check\_docstatus\_transition(previous.docstatus).

If control reaches the end, it returns no value.

**Methods declared on this owner** [load doc before save](operations-043.md#op-6916982d5f9ee2), [check docstatus transition](operations-042.md#op-36280f271479f7).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L73) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L951)

<a id="op-36280f271479f7"></a>
### Document.check docstatus transition

`operation_foundation_model_document_business_behavior_document_check_record_state_transition`

**Inputs** self, to\_docstatus.

**Explicit failure paths** Platform.DocstatusTransitionError(translated “Cannot change docstatus from 0 (Draft) to 2 (Cancelled)”) · Platform.ValidationError(translated “Invalid docstatus”, self.docstatus) · Platform.DocstatusTransitionError(translated “Cannot change docstatus from 1 (Submitted) to 0 (Draft)”) · Platform.ValidationError(translated “Cannot edit cancelled document”).

**Local steps**

- If to\_docstatus equals DocStatus.DRAFT.
  - If self.docstatus.is\_draft().
    - Set self.\_action from “save”.
  - Otherwise.
    - If self.docstatus.is\_submitted().
      - Set self.\_action from “submit”.
      - Evaluate self.check\_permission(“submit”).
    - Otherwise.
      - If self.docstatus.is\_cancelled().
        - Raise Platform.DocstatusTransitionError(translated “Cannot change docstatus from 0 (Draft) to 2 (Cancelled)”).
      - Otherwise.
        - Raise Platform.ValidationError(translated “Invalid docstatus”, self.docstatus).
- Otherwise.
  - If to\_docstatus equals DocStatus.SUBMITTED.
    - If self.docstatus.is\_submitted().
      - Set self.\_action from “update\_after\_submit”.
      - Evaluate self.check\_permission(“submit”).
    - Otherwise.
      - If self.docstatus.is\_cancelled().
        - Set self.\_action from “cancel”.
        - Evaluate self.check\_permission(“cancel”).
      - Otherwise.
        - If self.docstatus.is\_draft().
          - Raise Platform.DocstatusTransitionError(translated “Cannot change docstatus from 1 (Submitted) to 0 (Draft)”).
        - Otherwise.
          - Raise Platform.ValidationError(translated “Invalid docstatus”, self.docstatus).
  - Otherwise.
    - If to\_docstatus equals DocStatus.CANCELLED.
      - Raise Platform.ValidationError(translated “Cannot edit cancelled document”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check permission](operations-040.md#op-5394672be646ab).

**Values supplied outside this operation** effective access from self.check\_permission(“submit”), self.check\_permission(“cancel”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L74) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L955)

<a id="op-2839bf040beb76"></a>
### Document.set parent in children

`operation_foundation_model_document_business_behavior_document_set_parent_in_children`

**Inputs** self.

**Local steps**

- For each d in self.get\_all\_children().
  - Set d.parent from self.name.
  - Set d.parenttype from self.doctype.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L6585) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1027)

<a id="op-d257082ba8108f"></a>
### Document.set name in children

`operation_foundation_model_document_business_behavior_document_set_name_in_children`

**Inputs** self.

**Local steps**

- For each d in self.get\_all\_children().
  - If not d.name.
    - Evaluate set\_new\_name(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L6692) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1024)

<a id="op-e23f7bbd8476c3"></a>
### Document.validate update after submit

`operation_foundation_model_document_business_behavior_document_validate_update_after_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.ignore\_validate\_update\_after\_submit.
  - Return no value.
- Evaluate self.\_validate\_update\_after\_submit().
- For each d in self.get\_all\_children().
  - If (d.is\_new() and self.meta.get\_field(d.parentfield).allow\_on\_submit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_new() → self.meta.get\_field(d.parentfield).allow\_on\_submit.
    - Continue with the next iteration or loop test.
  - Evaluate d.\_validate\_update\_after\_submit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate update after submit](operations-047.md#op-59d4171df5447f), [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L6792) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1049)

<a id="op-2870e619f29c89"></a>
### Document.validate mandatory

`operation_foundation_model_document_business_behavior_document_validate_mandatory`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** Platform.MandatoryError(“&#91;{doctype}, {name}&#93;: {fields}”.format(fields = “, ”.join(generator of each at 0 for each drawn from missing), doctype = self.doctype, name = self.name)).

**Local steps**

- If self.flags.ignore\_mandatory.
  - Return no value.
- Set missing from self.\_get\_missing\_mandatory\_fields().
- For each d in self.get\_all\_children().
  - Evaluate missing.extend(d.\_get\_missing\_mandatory\_fields()).
- If not missing.
  - Return no value.
- For each tuple(idx, msg) in missing.
  - Evaluate msgprint(msg).
- If Platform.flags.print\_messages.
  - Evaluate print(self.as\_json().encode(“utf-8”)).
- Raise Platform.MandatoryError(“&#91;{doctype}, {name}&#93;: {fields}”.format(fields = “, ”.join(generator of each at 0 for each drawn from missing), doctype = self.doctype, name = self.name)).
  - Draw each from missing.

**Methods declared on this owner** [get missing mandatory fields](operations-046.md#op-770315ca6e1d12), [get all children](operations-042.md#op-c0f0e764f5c4d1), [as json](operations-046.md#op-96bad16b38093f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1044)

<a id="op-d0e8ca580d3b7a"></a>
### Document.validate links

`operation_foundation_model_document_business_behavior_document_validate_links`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.LinkValidationError — translated “Could not find {0}”.format(msg) · validation helper with Platform.CancelledLinkError — translated “Cannot link cancelled document: {0}”.format(msg).

**Local steps**

- If (self.flags.ignore\_links or self.\_action equals “cancel”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.ignore\_links → self.\_action equals “cancel”.
  - Return no value.
- Set tuple(invalid\_links, cancelled\_links) from self.get\_invalid\_links().
- For each d in self.get\_all\_children().
  - Set result from d.get\_invalid\_links(is\_submittable = self.meta.is\_submittable).
  - Evaluate invalid\_links.extend(result at 0).
  - Evaluate cancelled\_links.extend(result at 1).
- If invalid\_links.
  - Set msg from “, ”.join(generator of each at 2 for each drawn from invalid\_links).
    - Draw each from invalid\_links.
  - Call the validation error handler Platform.throw(translated “Could not find {0}”.format(msg), Platform.LinkValidationError).
- If cancelled\_links.
  - Set msg from “, ”.join(generator of each at 2 for each drawn from cancelled\_links).
    - Draw each from cancelled\_links.
  - Call the validation error handler Platform.throw(translated “Cannot link cancelled document: {0}”.format(msg), Platform.CancelledLinkError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get invalid links](operations-046.md#op-0273ce8eb431f0), [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L88) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1043)

<a id="op-c0f0e764f5c4d1"></a>
### Document.get all children

`operation_foundation_model_document_business_behavior_document_get_all_children`

**Inputs** self, parenttype = no value, include\_computed (named only, default false).

**Declared result** list at “Document”.

**Explicit results** children.

**Local steps**

- Set children from list().
- Set table\_fieldnames from self.\_table\_fieldnames when include\_computed, otherwise self.\_non\_computed\_table\_fieldnames.
  - Value choice on include\_computed — true gives self.\_table\_fieldnames, false gives self.\_non\_computed\_table\_fieldnames.
- For each tuple(fieldname, child\_doctype) in table\_fieldnames.items().
  - If (parenttype and child\_doctype differs from parenttype).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parenttype → child\_doctype differs from parenttype.
    - Continue with the next iteration or loop test.
  - If value bound to self.get(fieldname).
    - Evaluate children.extend(value).
- Return children.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L3286) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L965)

<a id="op-b5adf9fc5af1a0"></a>
### Document.run method

`operation_foundation_model_document_business_behavior_document_run_method`

**Inputs** self, method, remaining positional values args, remaining named values kwargs.

**Explicit results** out.

**Explicit failure paths** Exception(“Run method is for hooks, avoid usage on internal methods”).

**Local steps**

- If method.startswith(“\_”).
  - Raise Exception(“Run method is for hooks, avoid usage on internal methods”).
- Bind local operation fn for subsequent calls.
- Set fn.\_\_name\_\_ from str(method).
- Set out from Document.hook(fn)(self, expanded args, expanded names kwargs).
- Evaluate self.run\_notifications(method).
- Evaluate run\_webhooks(self, method).
- Evaluate run\_server\_script\_for\_doc\_event(self, method).
- Evaluate run\_automations(self, method).
- Return out.

**Methods declared on this owner** [run notifications](operations-042.md#op-0de1aa4ed98b3a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L81) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1013)

<a id="op-2e9c0936348adb"></a>
### Document.run method.fn

`operation_foundation_model_document_business_behavior_document_run_method_function`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** method\_object(expanded args, expanded names kwargs).

**Local steps**

- Set method\_object from getattr(self, method, no value).
- If (method belongs to self.\_\_dict\_\_ or callable(method\_object)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in method belongs to self.\_\_dict\_\_ → callable(method\_object).
  - Return method\_object(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, method, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L3943) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1014)

<a id="op-f40c56b8c34cc5"></a>
### Document.run trigger

`operation_foundation_model_document_business_behavior_document_run_trigger`

**Inputs** self, method, remaining positional values args, remaining named values kwargs.

**Explicit results** self.run\_method(method, expanded args, expanded names kwargs).

**Local steps**

- Return self.run\_method(method, expanded args, expanded names kwargs).

**Methods declared on this owner** [run method](operations-042.md#op-b5adf9fc5af1a0).

**Values supplied outside this operation** selected callable from self.run\_method(method, expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L4095) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1019)

<a id="op-0de1aa4ed98b3a"></a>
### Document.run notifications

`operation_foundation_model_document_business_behavior_document_run_notifications`

**Inputs** self, method.

**Explicit results** no value.

**Local steps**

- If (method equals “onload” or (Platform.flags.in\_import and Platform.flags.mute\_emails) or Platform.flags.in\_patch or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in method equals “onload” → (Platform.flags.in\_import and Platform.flags.mute\_emails) → Platform.flags.in\_patch → Platform.flags.in\_install.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_import → Platform.flags.mute\_emails.
  - Return no value.
- If self.flags.notifications\_executed is identical to no value.
  - Set self.flags.notifications\_executed from list().
- Bind dependencies evaluate\_alert.
- Bind local operation \_get\_notifications for subsequent calls.
- Set notifications from Platform.client\_cache.get\_value(formatted text notifications::{self.doctype}, generator = \_get\_notifications).
- If not notifications.
  - Return no value.
- Bind local operation \_evaluate\_alert for subsequent calls.
- Set event\_map from mapping(“on\_update” → “Save”, “after\_insert” → “New”, “on\_submit” → “Submit”, “on\_cancel” → “Cancel”).
- If (not self.flags.in\_insert and not self.flags.in\_delete).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.in\_insert → not self.flags.in\_delete.
  - Set event\_map at “on\_change” from “Value Change”.
- For each alert in notifications.
  - Set event from event\_map.get(method, no value).
  - If (event and alert.event equals event).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in event → alert.event equals event.
    - Evaluate \_evaluate\_alert(alert).
  - Otherwise.
    - If (alert.event equals “Method” and method equals alert.method).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in alert.event equals “Method” → method equals alert.method.
      - Evaluate \_evaluate\_alert(alert).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L82) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1015)

<a id="op-4ea52433f241e6"></a>
### Document.run notifications.get notifications

`operation_foundation_model_document_business_behavior_document_run_notifications_get_notifications`

**Inputs** no declared parameters.

**Record and data access** read “Notification” via get\_all.

**Explicit results** Platform.get\_all(“Notification”, fields = list(“name”, “event”, “method”), filters = mapping(“enabled” → 1, “document\_type” → self.doctype)).

**Local steps**

- Return Platform.get\_all(“Notification”, fields = list(“name”, “event”, “method”), filters = mapping(“enabled” → 1, “document\_type” → self.doctype)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L83) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1017)

<a id="op-0148e7a85aa21e"></a>
### Document.run notifications.evaluate alert

`operation_foundation_model_document_business_behavior_document_run_notifications_evaluate_alert`

**Inputs** alert.

**Explicit results** no value.

**Local steps**

- If alert.name belongs to self.flags.notifications\_executed.
  - Return no value.
- Evaluate evaluate\_alert(self, alert.name, alert.event).
- Evaluate self.flags.notifications\_executed.append(alert.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L5333) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1016)

<a id="op-14bf091194ccb9"></a>
### Document.submit

`operation_foundation_model_document_business_behavior_document_submit`

**Inputs** self.

**State and service calls** call save on self.

**Explicit results** self.save().

**Local steps**

- Set self.docstatus from DocStatus.SUBMITTED.
- Return self.save().

**Methods declared on this owner** [save](operations-040.md#op-5d89aac355c0bc).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L5480) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1032)

<a id="op-d95fff80a62db7"></a>
### Document.cancel

`operation_foundation_model_document_business_behavior_document_cancel`

**Inputs** self.

**State and service calls** call save on self.

**Explicit results** self.save().

**Local steps**

- Set self.docstatus from DocStatus.CANCELLED.
- Return self.save().

**Methods declared on this owner** [save](operations-040.md#op-5d89aac355c0bc).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L5552) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L949)

<a id="op-f1274dd7869b49"></a>
### Document.rename

`operation_foundation_model_document_business_behavior_document_rename`

**Inputs** self, name, merge = false, force = false, validate\_rename = true.

**Local steps**

- Bind dependencies rename\_doc.
- Set self.name from rename\_doc(doc = self, new = name, merge = merge, force = force, …).
- Evaluate self.reload().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reload](operations-040.md#op-4c3e48e6329b61).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L5624) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1005)

<a id="op-fe612900b2359a"></a>
### Document.submit

`operation_foundation_model_document_business_behavior_document_submit_2`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** self.\_submit().

**Local steps**

- Return self.\_submit().

**Methods declared on this owner** [submit](operations-042.md#op-14bf091194ccb9).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L5828) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1033)
