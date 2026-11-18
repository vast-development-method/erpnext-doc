# Record lifecycle and persistence · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-db8630eefd40e1"></a>
### Document.add comment

`operation_foundation_model_document_business_behavior_document_add_comment`

**Inputs** self, comment\_type = “Comment”, text = no value, comment\_email = no value, comment\_by = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → comment\_type, “comment\_email” → (comment\_email or Platform.session.user), “comment\_by” → comment\_by, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → comment\_type, “comment\_email” → (comment\_email or Platform.session.user), “comment\_by” → comment\_by, …)).

**Explicit results** Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → comment\_type, “comment\_email” → (comment\_email or nested operand in the contract.session.user), “comment\_by” → comment\_by, …)).insert(ignore ….

**Local steps**

- Return Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → comment\_type, “comment\_email” → (comment\_email or nested operand in the contract.session.user), “comment\_by” → comment\_by, …)).insert(ignore ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in comment\_email → Platform.session.user.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in text → comment\_type.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L6337) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L944)

<a id="op-3019c6ca6d7e9c"></a>
### Document.add seen

`operation_foundation_model_document_business_behavior_document_add_seen`

**Inputs** self, user = no value.

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- If (self.meta.track\_seen and not Platform.flags.read\_only and not self.meta.issingle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.track\_seen → not Platform.flags.read\_only → not self.meta.issingle.
  - Set \_seen from (self.get(“\_seen”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_seen”) → list().
  - Set \_seen from Platform.parse\_json(\_seen).
  - If user does not belong to \_seen.
    - Evaluate \_seen.append(user).
    - Evaluate commit\_after\_response(deferred anonymous expression).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L6677) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L945)

<a id="op-8892864f3f990d"></a>
### Document.add viewed

`operation_foundation_model_document_business_behavior_document_add_viewed`

**Inputs** self, user = no value, force = false, unique\_views = false.

**Record and data access** read “View Log” via exists · resolve a document from mapping(“doctype” → “View Log”, “viewed\_by” → user, “reference\_doctype” → self.doctype, “reference\_name” → self.name) via get\_doc.

**Explicit results** no value · view\_log.

**Local steps**

- If not (getattr(self.meta, “track\_views”, false) or force).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self.meta, “track\_views”, false) → force.
  - Return no value.
- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- If (unique\_views and Platform.db.exists(“View Log”, mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name, “viewed\_by” → user))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in unique\_views → Platform.db.exists(“View Log”, mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name, “viewed\_by” → user)).
  - Return no value.
- Set view\_log from Platform.get\_doc(mapping(“doctype” → “View Log”, “viewed\_by” → user, “reference\_doctype” → self.doctype, “reference\_name” → self.name)).
- If Platform.flags.read\_only.
  - Evaluate view\_log.deferred\_insert().
- Otherwise.
  - Evaluate commit\_after\_response(deferred anonymous expression).
- Return view\_log.

**Values supplied outside this operation** selected callable from getattr(self.meta, “track\_views”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L7016) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L947)

<a id="op-fe2eb57df6193e"></a>
### Document.log error

`operation_foundation_model_document_business_behavior_document_log_error`

**Inputs** self, title = no value, message = no value, defer\_insert (named only, default false).

**Explicit results** Platform.log\_error(message = message, title = title, reference\_doctype = self.doctype, reference\_name = self.name, …).

**Local steps**

- Return Platform.log\_error(message = message, title = title, reference\_doctype = self.doctype, reference\_name = self.name, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L997)

<a id="op-8c487683e98ecb"></a>
### Document.get signature

`operation_foundation_model_document_business_behavior_document_get_signature`

**Inputs** self.

**Explicit results** hashlib.sha224(formatted text {nested operand in the contract.doctype}:{nested operand in the contract.name}.encode(), usedforsecurity = false).hexdigest().

**Local steps**

- Return hashlib.sha224(formatted text {nested operand in the contract.doctype}:{nested operand in the contract.name}.encode(), usedforsecurity = false).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L142) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L975)

<a id="op-ad85f825ccd24e"></a>
### Document.get document share key

`operation_foundation_model_document_business_behavior_document_get_document_share_key`

**Inputs** self, expires\_on = no value, no\_expiry = false.

**Record and data access** read “Document Share Key” via exists · resolve a document from “Document Share Key” via get\_doc.

**State and service calls** request new\_doc for “Document Share Key” · call insert on doc.

**Explicit results** doc.key.

**Local steps**

- If no\_expiry.
  - Set expires\_on from no value.
- Set existing\_key from Platform.db.exists(“Document Share Key”, mapping(“reference\_doctype” → self.doctype, “reference\_docname” → self.name, “expires\_on” → expires\_on)).
- If existing\_key.
  - Set doc from Platform.get\_doc(“Document Share Key”, existing\_key).
- Otherwise.
  - Set doc from Platform.new\_doc(“Document Share Key”).
  - Set doc.reference\_doctype from self.doctype.
  - Set doc.reference\_docname from self.name.
  - Set doc.expires\_on from expires\_on.
  - Set doc.flags.no\_expiry from no\_expiry.
  - Evaluate doc.insert(ignore\_permissions = true).
- Return doc.key.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L265) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L967)

<a id="op-b917aa064609be"></a>
### Document.get liked by

`operation_foundation_model_document_business_behavior_document_get_liked_by`

**Inputs** self.

**Explicit results** json.loads(liked\_by) · list().

**Local steps**

- Set liked\_by from getattr(self, “\_liked\_by”, no value).
- If liked\_by.
  - Return json.loads(liked\_by).
- Otherwise.
  - Return list().

**Values supplied outside this operation** selected callable from getattr(self, “\_liked\_by”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L644) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L969)

<a id="op-e9cdbf2660b671"></a>
### Document.onload

`operation_foundation_model_document_business_behavior_document_onload`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** onload.

**Local steps**

- Set onload from self.get(“\_\_onload”).
- If onload is identical to no value.
  - Set onload from Platform.\_dict().
  - Evaluate self.set(“\_\_onload”, onload).
- Return onload.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L748) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1000)

<a id="op-22c0c3ca769797"></a>
### Document.set onload

`operation_foundation_model_document_business_behavior_document_set_onload`

**Inputs** self, key, value.

**Local steps**

- Set self.\_\_onload at key from value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L892) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L417) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1026)

<a id="op-075a7a1778814c"></a>
### Document.get onload

`operation_foundation_model_document_business_behavior_document_get_onload`

**Inputs** self, key = no value.

**Explicit results** self.\_\_onload at key when key, otherwise self.\_\_onload.

**Local steps**

- Return self.\_\_onload at key when key, otherwise self.\_\_onload.
  - Value choice on key — true gives self.\_\_onload at key, false gives self.\_\_onload.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L960) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L970)

<a id="op-98f8a41d3c3333"></a>
### Document.queue action

`operation_foundation_model_document_business_behavior_document_queue_action`

**Inputs** self, action, remaining named values kwargs.

**Explicit results** enqueue(“Platform.model.document.execute\_action”, \_\_doctype = self.doctype, \_\_name = self.name, \_\_action = action, enqueue\_after\_commit = enqueue\_after\_commit, …).

**Local steps**

- Bind dependencies enqueue.
- If hasattr(self, formatted text \_{action}).
  - Set action from formatted text \_{action}.
- Evaluate self.check\_if\_locked().
- Evaluate self.lock().
- Set enqueue\_after\_commit from kwargs.pop(“enqueue\_after\_commit”, no value).
- If enqueue\_after\_commit is identical to no value.
  - Set enqueue\_after\_commit from true.
- Return enqueue(“Platform.model.document.execute\_action”, \_\_doctype = self.doctype, \_\_name = self.name, \_\_action = action, enqueue\_after\_commit = enqueue\_after\_commit, …).

**Methods declared on this owner** [check if locked](operations-040.md#op-39a20656da1053), [lock](operations-044.md#op-6cab8a8d65f273).

**Values supplied outside this operation** service or queued work from enqueue(“Platform.model.document.execute\_action”, \_\_doctype = self.doctype, \_\_name = self.name, \_\_action = action, enqueue\_after\_commit = enqueue\_after\_commit, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L1033) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1001)

<a id="op-6cab8a8d65f273"></a>
### Document.lock

`operation_foundation_model_document_business_behavior_document_dependency_lock`

**Inputs** self, timeout = no value.

**Explicit failure paths** Platform.DocumentLockedError.

**Local steps**

- Set signature from self.get\_signature().
- If file\_lock.lock\_exists(signature).
  - Set lock\_exists from true.
  - If file\_lock.lock\_age(signature) &gt; DOCUMENT\_LOCK\_EXPIRY.
    - Evaluate file\_lock.delete\_lock(signature).
    - Set lock\_exists from false.
  - If timeout.
    - For each \_ in range(timeout).
      - Evaluate time.sleep(1).
      - If not file\_lock.lock\_exists(signature).
        - Set lock\_exists from false.
        - Leave the innermost loop without its normal-exhaustion alternative.
  - If lock\_exists.
    - Raise Platform.DocumentLockedError.
- Evaluate file\_lock.create\_lock(signature).
- Evaluate Platform.local.locked\_documents.append(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get signature](operations-044.md#op-8c487683e98ecb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L1383) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L962)

<a id="op-a692e8adb83841"></a>
### Document.unlock

`operation_foundation_model_document_business_behavior_document_unlock`

**Inputs** self.

**Local steps**

- Evaluate file\_lock.delete\_lock(self.get\_signature()).
- If self belongs to Platform.local.locked\_documents.
  - Evaluate Platform.local.locked\_documents.remove(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get signature](operations-044.md#op-8c487683e98ecb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L1759) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1035)

<a id="op-68eee8277b5107"></a>
### Document.validate from to dates

`operation_foundation_model_document_business_behavior_document_validate_from_to_dates`

**Inputs** self, from\_date\_field, to\_date\_field.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.exceptions.InvalidDates — (table\_row + translated “{0} must be after {1}”.format(Platform.bold(translated nested operand in the contract.meta.get\_label(to\_date\_field)), Platform.bold(translated nested operand in the contract.meta.g ….

**Local steps**

- Set from\_date from self.get(from\_date\_field).
- Set to\_date from self.get(to\_date\_field).
- If not (from\_date and to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_date → to\_date.
  - Return no value.
- If date\_diff(to\_date, from\_date) &lt; 0.
  - Set table\_row from empty text.
  - If self.meta.istable.
    - Set table\_row from (translated “{0} row #{1}:”.format(translated Platform.unscrub(self.parentfield), self.idx) + one space).
  - Call the validation error handler Platform.throw((table\_row + translated “{0} must be after {1}”.format(Platform.bold(translated nested operand in the contract.get\_label(to\_date\_field)), Platform.bold(translated nested operand in the contr ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L87) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1041)

<a id="op-4d98b7f015c075"></a>
### Document.get assigned users

`operation_foundation_model_document_business_behavior_document_get_assigned_users`

**Inputs** self.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** set(assigned\_users).

**Local steps**

- Set assigned\_users from Platform.get\_all(“ToDo”, fields = list(“allocated\_to”), filters = mapping(“reference\_type” → self.doctype, “reference\_name” → self.name, “status” → tuple(“!=”, “Cancelled”)), pluck = “allocated\_to”).
- Return set(assigned\_users).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L2353) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L966)

<a id="op-2c91ca0e0080a6"></a>
### Document.add tag

`operation_foundation_model_document_business_behavior_document_add_tag`

**Inputs** self, tag.

**Local steps**

- Bind dependencies DocTags.
- Evaluate DocTags(self.doctype).add(self.name, tag).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L2551) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L946)

<a id="op-0dfaae7d5be750"></a>
### Document.remove tag

`operation_foundation_model_document_business_behavior_document_remove_tag`

**Inputs** self, tag.

**Local steps**

- Bind dependencies DocTags.
- Evaluate DocTags(self.doctype).remove(self.name, tag).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L2648) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1004)

<a id="op-a359d110fea80b"></a>
### Document.get tags

`operation_foundation_model_document_business_behavior_document_get_tags`

**Inputs** self.

**Explicit results** DocTags(nested operand in the contract.doctype).get\_tags(self.name).split(“,”) at slice 1 to no value.

**Local steps**

- Bind dependencies DocTags.
- Return DocTags(nested operand in the contract.doctype).get\_tags(self.name).split(“,”) at slice 1 to no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L75) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L976)

<a id="op-b5888fee6f4d4b"></a>
### Document.deferred insert

`operation_foundation_model_document_business_behavior_document_deferred_insert`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind dependencies deferred\_insert.
- Evaluate self.set\_user\_and\_timestamp().
- Set doc from self.get\_valid\_dict(convert\_dates\_to\_str = true, ignore\_virtual = true).
- Evaluate deferred\_insert(doctype = self.doctype, records = doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set user and timestamp](operations-041.md#op-e276da7d33f1d3), [get valid dict](operations-045.md#op-c47e5bad7a2c34).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L2883) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L960)

<a id="op-6ba742e3bde72f"></a>
### Document.str

`operation_foundation_model_document_business_behavior_document_text`

**Inputs** self.

**Explicit results** formatted text {self.doctype} ({(self.name or “unsaved”)}).

**Local steps**

- Return formatted text {self.doctype} ({(self.name or “unsaved”)}).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → “unsaved”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L3025) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L425) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1034)

<a id="op-96f11dcbafcdd0"></a>
### Document.repr

`operation_foundation_model_document_business_behavior_document_representation`

**Inputs** self.

**Explicit results** formatted text &lt;{self.\_\_class\_\_.\_\_name\_\_}: {doctype} {name}{docstatus}{parent}&gt;.

**Local steps**

- Set doctype from formatted text doctype={self.doctype}.
- Set name from (self.name or “unsaved”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → “unsaved”.
- Set docstatus from formatted text  docstatus={self.docstatus} when self.docstatus, otherwise empty text.
  - Value choice on self.docstatus — true gives formatted text  docstatus={self.docstatus}, false gives empty text.
- Set parent from formatted text  parent={self.parent} when getattr(self, “parent”, no value), otherwise empty text.
  - Value choice on getattr(self, “parent”, no value) — true gives formatted text  parent={self.parent}, false gives empty text.
- Return formatted text &lt;{self.\_\_class\_\_.\_\_name\_\_}: {doctype} {name}{docstatus}{parent}&gt;.

**Values supplied outside this operation** selected callable from getattr(self, “parent”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L3113) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1007)

<a id="op-4eb72c4f0d0721"></a>
### Document.json

`operation_foundation_binding_foundation_model_document_document_json`

**Inputs** self.

**Explicit results** self.as\_dict(no\_nulls = true).

**Local steps**

- Return self.as\_dict(no\_nulls = true).

**Methods declared on this owner** [as dict](operations-046.md#op-8dc085dc083de4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1625) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1601)

<a id="op-e7280a1f6affd4"></a>
### Document.meta

`operation_foundation_binding_foundation_model_document_document_meta`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** Platform.get\_meta(self.doctype).

**Local steps**

- Return Platform.get\_meta(self.doctype).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1626) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1602)

<a id="op-041c185071decc"></a>
### Document.permitted fieldnames

`operation_foundation_binding_foundation_model_document_document_permitted_fieldnames`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** set at str.

**Explicit results** set(get\_permitted\_fields(doctype = self.doctype, parenttype = getattr(self, “parenttype”, no value))).

**Local steps**

- Return set(get\_permitted\_fields(doctype = self.doctype, parenttype = getattr(self, “parenttype”, no value))).

**Values supplied outside this operation** selected callable from getattr(self, “parenttype”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1607)
