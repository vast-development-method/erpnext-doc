# Record lifecycle and persistence · operations 43

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-e2321ee3f434d5"></a>
### Document.cancel

`operation_foundation_model_document_business_behavior_document_cancel_2`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** self.\_cancel().

**Local steps**

- Return self.\_cancel().

**Methods declared on this owner** [cancel](operations-042.md#op-d95fff80a62db7).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L5897) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L950)

<a id="op-f4e795ce4e2402"></a>
### Document.discard

`operation_foundation_model_document_business_behavior_document_discard`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self.

**Explicit failure paths** Platform.ValidationError(translated “Only draft documents can be discarded”, self.docstatus).

**Local steps**

- Set self.\_action from “discard”.
- Evaluate self.check\_if\_locked().
- Evaluate self.set\_user\_and\_timestamp().
- Evaluate self.check\_if\_latest().
- If not self.docstatus.is\_draft().
  - Raise Platform.ValidationError(translated “Only draft documents can be discarded”, self.docstatus).
- Evaluate self.check\_permission(“write”).
- Evaluate self.run\_method(“before\_discard”).
- Evaluate self.db\_set(“docstatus”, DocStatus.CANCELLED).
- Evaluate delattr(self, “\_action”).
- Evaluate self.run\_method(“on\_discard”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if locked](operations-040.md#op-39a20656da1053), [set user and timestamp](operations-041.md#op-e276da7d33f1d3), [check if latest](operations-042.md#op-0148e812fab947), [check permission](operations-040.md#op-5394672be646ab), [run method](operations-042.md#op-b5adf9fc5af1a0), [db set](operations-043.md#op-ec0ea799d0b42c).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · selected callable from self.run\_method(“before\_discard”), self.run\_method(“on\_discard”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L5966) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L963)

<a id="op-43a6baf4f18d25"></a>
### Document.rename

`operation_foundation_model_document_business_behavior_document_rename_2`

**Inputs** self, name, merge = false, force = false, validate\_rename = true.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** self.\_rename(name = name, merge = merge, force = force).

**Local steps**

- Return self.\_rename(name = name, merge = merge, force = force).

**Methods declared on this owner** [rename](operations-042.md#op-f1274dd7869b49).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L80) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1006)

<a id="op-9dce773fd5275a"></a>
### Document.delete

`operation_foundation_model_document_business_behavior_document_delete`

**Inputs** self, ignore\_permissions = false, force = false, delete\_permanently (named only, default false).

**State and service calls** request delete\_doc for self.doctype.

**Explicit results** Platform.delete\_doc(self.doctype, self.name, ignore\_permissions = ignore\_permissions, flags = self.flags, force = force, delete\_permanently = delete\_permanently).

**Local steps**

- Return Platform.delete\_doc(self.doctype, self.name, ignore\_permissions = ignore\_permissions, flags = self.flags, force = force, delete\_permanently = delete\_permanently).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L6492) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L961)

<a id="op-6237ba21102192"></a>
### Document.run before save methods

`operation_foundation_model_document_business_behavior_document_run_before_save_methods`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate self.reset\_seen().
- If self.\_action belongs to tuple(“save”, “submit”).
  - Evaluate self.run\_method(“before\_validate”).
- If self.flags.ignore\_validate.
  - Return no value.
- If self.\_action equals “save”.
  - Evaluate self.run\_method(“validate”).
  - Evaluate self.run\_method(“before\_save”).
- Otherwise.
  - If self.\_action equals “submit”.
    - Evaluate self.run\_method(“validate”).
    - Evaluate self.run\_method(“before\_submit”).
  - Otherwise.
    - If self.\_action equals “cancel”.
      - Evaluate self.run\_method(“before\_cancel”).
    - Otherwise.
      - If self.\_action equals “update\_after\_submit”.
        - Evaluate self.run\_method(“before\_update\_after\_submit”).
- Evaluate self.set\_title\_field().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset seen](operations-043.md#op-62ae7ec0f43e78), [run method](operations-042.md#op-b5adf9fc5af1a0), [set title field](operations-041.md#op-25ed331660090f).

**Values supplied outside this operation** selected callable from self.run\_method(“before\_validate”), self.run\_method(“validate”) and 4 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0279.json#L6640) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1012)

<a id="op-6916982d5f9ee2"></a>
### Document.load doc before save

`operation_foundation_model_document_business_behavior_document_load_record_before_save`

**Inputs** self, raise\_exception (named only, default false).

**Record and data access** resolve a document from self.doctype via get\_doc.

**Explicit results** no value · Platform.clear\_last\_message().

**Explicit failure paths** propagate active failure.

**Local steps**

- Set self.\_doc\_before\_save from no value.
- If self.is\_new().
  - Return no value.
- Attempt the following.
  - Set self.\_doc\_before\_save from Platform.get\_doc(self.doctype, self.name, for\_update = true).
- On failure (Platform.DoesNotExistError).
  - If raise\_exception.
    - Propagate the active failure.
  - Return Platform.clear\_last\_message().
- For each fieldname in self.\_non\_computed\_table\_fieldnames.
  - For each row in (self.get(fieldname) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(fieldname) → list().
    - Set row.\_doc\_before\_save from next(generator of d for d drawn from (self.\_doc\_before\_save.get(fieldname) or list()) where d.name equals row.name, no value).
      - Draw d from (self.\_doc\_before\_save.get(fieldname) or list()), keep a combination only if (d.name equals row.name).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_doc\_before\_save.get(fieldname) → list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L78) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L996)

<a id="op-0c820dbc721118"></a>
### Document.run post save methods

`operation_foundation_model_document_business_behavior_document_run_post_save_methods`

**Inputs** self.

**Local steps**

- If self.\_action equals “save”.
  - Evaluate self.run\_method(“on\_update”).
- Otherwise.
  - If self.\_action equals “submit”.
    - Evaluate self.run\_method(“on\_update”).
    - Evaluate self.run\_method(“on\_submit”).
  - Otherwise.
    - If self.\_action equals “cancel”.
      - Evaluate self.run\_method(“on\_cancel”).
      - Evaluate self.check\_no\_back\_links\_exist().
    - Otherwise.
      - If self.\_action equals “update\_after\_submit”.
        - Evaluate self.run\_method(“on\_update\_after\_submit”).
- If not (Platform.flags.in\_import and self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_import → self.is\_new().
  - Evaluate self.clear\_cache().
- If self.flags.get(“notify\_update”, true).
  - Evaluate self.notify\_update().
- Bind dependencies update\_global\_search.
- Evaluate update\_global\_search(self).
- Evaluate self.save\_version().
- Evaluate self.run\_method(“on\_change”).
- If tuple(self.doctype, self.name) belongs to Platform.flags.currently\_saving.
  - Evaluate Platform.flags.currently\_saving.remove(tuple(self.doctype, self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [run method](operations-042.md#op-b5adf9fc5af1a0), [check no back links exist](operations-043.md#op-1e852bee989ffc), [is new](operations-046.md#op-e2def851dd1371), [clear cache](operations-043.md#op-5180f597fc280c), [notify update](operations-043.md#op-065004d4ec04c4), [save version](operations-043.md#op-fbb5266f20646e).

**Values supplied outside this operation** selected callable from self.run\_method(“on\_update”), self.run\_method(“on\_submit”) and 3 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L84) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1018)

<a id="op-5180f597fc280c"></a>
### Document.clear cache

`operation_foundation_model_document_business_behavior_document_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_document\_cache(self.doctype, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L577) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L956)

<a id="op-62ae7ec0f43e78"></a>
### Document.reset seen

`operation_foundation_model_document_business_behavior_document_reset_seen`

**Inputs** self.

**State and service calls** request set\_value on self.doctype.

**Local steps**

- If (getattr(self.meta, “track\_seen”, false) and not getattr(self.meta, “issingle”, false) and not self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(self.meta, “track\_seen”, false) → not getattr(self.meta, “issingle”, false) → not self.is\_new().
  - Evaluate Platform.db.set\_value(self.doctype, self.name, “\_seen”, json.dumps(list(Platform.session.user)), update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371).

**Values supplied outside this operation** selected callable from getattr(self.meta, “track\_seen”, false), getattr(self.meta, “issingle”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L645) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1009)

<a id="op-065004d4ec04c4"></a>
### Document.notify update

`operation_foundation_model_document_business_behavior_document_notify_update`

**Inputs** self.

**State and service calls** publish realtime with “doc\_update” · publish realtime with “list\_update”.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_import or Platform.flags.in\_patch or Platform.flags.in\_migrate or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → Platform.flags.in\_patch → Platform.flags.in\_migrate → Platform.flags.in\_install.
  - Return no value.
- Evaluate Platform.publish\_realtime(“doc\_update”, mapping(“modified” → self.modified, “doctype” → self.doctype, “name” → self.name), doctype = self.doctype, docname = self.name, after\_commit = true).
- If (not self.meta.get(“read\_only”) and not self.meta.get(“issingle”) and not self.meta.get(“istable”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.meta.get(“read\_only”) → not self.meta.get(“issingle”) → not self.meta.get(“istable”).
  - Set data from mapping(“doctype” → self.doctype, “name” → self.name, “user” → Platform.session.user).
  - Evaluate Platform.publish\_realtime(“list\_update”, data, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“doc\_update”, mapping(“modified” → self.modified, “doctype” → self.doctype, “name” → self.name), doctype = self.doctype, docname = self.name, after\_commit = true), Platform.publish\_realtime(“list\_update”, data, after\_commit = true).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L864) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L999)

<a id="op-ec0ea799d0b42c"></a>
### Document.db set

`operation_foundation_model_document_business_behavior_document_database_set`

**Inputs** self, fieldname, value = no value, update\_modified = true, notify = false, commit = false.

**State and service calls** request set\_single\_value on self.doctype · request set\_value on self.doctype · commit.

**Explicit results** no value.

**Local steps**

- If isinstance(fieldname, dict).
  - Evaluate self.update(fieldname).
- Otherwise.
  - Evaluate self.set(fieldname, value).
- If (update\_modified and tuple(self.doctype, self.name) does not belong to Platform.flags.currently\_saving).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update\_modified → tuple(self.doctype, self.name) does not belong to Platform.flags.currently\_saving.
  - Evaluate self.set(“modified”, now()).
  - Evaluate self.set(“modified\_by”, Platform.session.user).
- If (not self.get\_doc\_before\_save() and not self.meta.istable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get\_doc\_before\_save() → not self.meta.istable.
  - Evaluate self.load\_doc\_before\_save().
- Evaluate self.run\_method(“before\_change”).
- If self.name is identical to no value.
  - Return no value.
- If self.meta.issingle.
  - Evaluate Platform.db.set\_single\_value(self.doctype, fieldname, value, modified = self.modified, modified\_by = self.modified\_by, update\_modified = update\_modified).
- Otherwise.
  - Evaluate Platform.db.set\_value(self.doctype, self.name, fieldname, value, update\_modified = update\_modified, …).
- Evaluate self.run\_method(“on\_change”).
- If notify.
  - Evaluate self.notify\_update().
- If commit.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update](operations-045.md#op-b90034268a7194), [set](operations-045.md#op-b58a481a5882b4), [get doc before save](operations-041.md#op-1bf04cf78b2762), [load doc before save](operations-043.md#op-6916982d5f9ee2), [run method](operations-042.md#op-b5adf9fc5af1a0), [notify update](operations-043.md#op-065004d4ec04c4).

**Values supplied outside this operation** clock or generated value from now() · selected callable from self.run\_method(“before\_change”), self.run\_method(“on\_change”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L1316) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L959)

<a id="op-0b3ca64be2049e"></a>
### Document.db get

`operation_foundation_model_document_business_behavior_document_database_get`

**Inputs** self, fieldname.

**Record and data access** read self.doctype via get\_value.

**Explicit results** Platform.db.get\_value(self.doctype, self.name, fieldname).

**Local steps**

- Return Platform.db.get\_value(self.doctype, self.name, fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L1999) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L958)

<a id="op-1e852bee989ffc"></a>
### Document.check no back links exist

`operation_foundation_model_document_business_behavior_document_check_number_back_links_exist`

**Inputs** self.

**Local steps**

- Bind dependencies check\_if\_doc\_is\_dynamically\_linked, check\_if\_doc\_is\_linked.
- If not self.flags.ignore\_links.
  - Evaluate check\_if\_doc\_is\_linked(self, method = “Cancel”).
  - Evaluate check\_if\_doc\_is\_dynamically\_linked(self, method = “Cancel”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L2082) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L953)

<a id="op-fbb5266f20646e"></a>
### Document.save version

`operation_foundation_model_document_business_behavior_document_save_version`

**Inputs** self.

**Record and data access** resolve a document from self.doctype via get\_doc.

**State and service calls** request new\_doc for “Version” · call insert on version.

**Explicit results** no value.

**Local steps**

- If (not getattr(self.meta, “track\_changes”, false) or self.doctype equals “Version” or self.flags.ignore\_version or Platform.flags.in\_install or (not self.\_doc\_before\_save and Platform.flags.in\_patch)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not getattr(self.meta, “track\_changes”, false) → self.doctype equals “Version” → self.flags.ignore\_version → Platform.flags.in\_install → (not self.\_doc\_before\_save and Platform.flags.in\_patch).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.\_doc\_before\_save → Platform.flags.in\_patch.
  - Return no value.
- Set doc\_to\_compare from self.\_doc\_before\_save.
- If (not doc\_to\_compare and amended\_from bound to self.get(“amended\_from”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc\_to\_compare → amended\_from bound to self.get(“amended\_from”).
  - Set doc\_to\_compare from Platform.get\_doc(self.doctype, amended\_from).
- Set version from Platform.new\_doc(“Version”).
- If (not doc\_to\_compare and not self.flags.updater\_reference).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc\_to\_compare → not self.flags.updater\_reference.
  - Return no value.
- If version.update\_version\_info(doc\_to\_compare, self).
  - Evaluate version.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Values supplied outside this operation** selected callable from getattr(self.meta, “track\_changes”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L2207) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1022)

<a id="op-ab16eb56809943"></a>
### Document.hook

`operation_foundation_model_document_business_behavior_document_hook`

**Inputs** f.

**Wrappers, in declaration order** staticmethod.

**Explicit results** composer.

**Local steps**

- Bind local operation add\_to\_return\_value for subsequent calls.
- Bind local operation compose for subsequent calls.
- Bind local operation composer for subsequent calls.
- Return composer.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L2612) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L983)

<a id="op-d8d4c04531b440"></a>
### Document.hook.add to return value

`operation_foundation_model_document_business_behavior_document_hook_add_to_return_value`

**Inputs** self, new\_return\_value.

**Explicit results** no value.

**Local steps**

- If new\_return\_value is identical to no value.
  - Set self.\_return\_value from self.get(“\_return\_value”).
  - Return no value.
- If isinstance(new\_return\_value, dict).
  - If not self.get(“\_return\_value”).
    - Set self.\_return\_value from mapping().
  - Evaluate self.\_return\_value.update(new\_return\_value).
- Otherwise.
  - Set self.\_return\_value from new\_return\_value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L3511) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L373) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L984)

<a id="op-3e6a369cb4d491"></a>
### Document.hook.compose

`operation_foundation_model_document_business_behavior_document_hook_compose`

**Inputs** fn, remaining positional values hooks.

**Explicit results** runner.

**Local steps**

- Bind local operation runner for subsequent calls.
- Return runner.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L3726) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L374) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L985)

<a id="op-1551f7dd1fa3d6"></a>
### Document.hook.compose.runner

`operation_foundation_model_document_business_behavior_document_hook_compose_runner`

**Inputs** self, method, remaining positional values args, remaining named values kwargs.

**Explicit results** self.\_\_dict\_\_.pop(“\_return\_value”, no value).

**Local steps**

- Evaluate add\_to\_return\_value(self, fn(self, expanded args, expanded names kwargs)).
- For each f in hooks.
  - Attempt the following.
    - Update Platform.db.\_disable\_transaction\_control using + 1.
    - If (not args and not \_accepts\_method\_argument(f)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args → not \_accepts\_method\_argument(f).
      - Evaluate add\_to\_return\_value(self, f(self, expanded names kwargs)).
    - Otherwise.
      - Evaluate add\_to\_return\_value(self, f(self, method, expanded args, expanded names kwargs)).
  - On exit, including pending return or failure.
    - Update Platform.db.\_disable\_transaction\_control using − 1.
- Return self.\_\_dict\_\_.pop(“\_return\_value”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L4095) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L375) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L986)

<a id="op-adb711b1e680f5"></a>
### Document.hook.composer

`operation_foundation_model_document_business_behavior_document_hook_composer`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** composed(self, method, expanded args, expanded names kwargs).

**Local steps**

- Set hooks from list().
- Set method from f.\_\_name\_\_.
- Set doc\_events from Platform.get\_doc\_hooks().
- For each handler in (doc\_events.get(self.doctype, mapping()).get(method, list()) + doc\_events.get(“\*”, mapping()).get(method, list())).
  - Evaluate hooks.append(Platform.get\_attr(handler)).
- Set composed from compose(f, expanded hooks).
- Return composed(self, method, expanded args, expanded names kwargs).

**Values supplied outside this operation** selected callable from Platform.get\_attr(handler).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L4435) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L376) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L987)

<a id="op-931f8772c19f7e"></a>
### Document.is whitelisted

`operation_foundation_model_document_business_behavior_document_is_whitelisted`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, method\_name.

**Locally raised failures** NotFound.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L4750) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L992)

<a id="op-fb642895b0e859"></a>
### Document.validate value

`operation_foundation_model_document_business_behavior_document_validate_value`

**Inputs** self, fieldname, condition, val2, doc = no value, raise\_exception = no value.

**Local steps**

- If not doc.
  - Set doc from self.
- Set val1 from doc.get\_value(fieldname).
- Set df from doc.meta.get\_field(fieldname).
- Set val2 from doc.cast(val2, df).
- If not compare(val1, condition, val2).
  - Set label from doc.meta.get\_label(fieldname).
  - If doc.get(“parentfield”).
    - Set msg from translated “Incorrect value in row {0}:”.format(doc.idx).
  - Otherwise.
    - Set msg from translated “Incorrect value:”.
  - If condition equals “in”.
    - Update msg using + translated “{0} must be one of {1}”.format(label, val2).
  - Otherwise.
    - If condition equals “not in”.
      - Update msg using + translated “{0} must be none of {1}”.format(label, val2).
    - Otherwise.
      - If condition equals “^”.
        - Update msg using + translated “{0} must be beginning with '{1}'”.format(label, val2).
      - Otherwise.
        - If condition equals “=”.
          - Update msg using + translated “{0} must be equal to '{1}'”.format(label, val2).
        - Otherwise.
          - Update msg using + translated “{0} must be {1} {2}”.format(label, condition, val2).
  - Evaluate msgprint(msg, raise\_exception = (raise\_exception or true)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in raise\_exception → true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L91) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1050)

<a id="op-497c3bd7944d0a"></a>
### Document.validate table has rows

`operation_foundation_model_document_business_behavior_document_validate_table_has_rows`

**Inputs** self, parentfield, raise\_exception = no value.

**Explicit failure paths** validation helper with (raise\_exception or Platform.EmptyTableError) — translated “Table {0} cannot be empty”.format(label).

**Local steps**

- If not (isinstance(self.get(parentfield), list) and len(self.get(parentfield)) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(self.get(parentfield), list) → len(self.get(parentfield)) &gt; 0.
  - Set label from translated self.meta.get\_label(parentfield).
  - Call the validation error handler Platform.throw(translated “Table {0} cannot be empty”.format(label), (raise\_exception or Platform.EmptyTableError)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in raise\_exception → Platform.EmptyTableError.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L90) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1048)

<a id="op-232e17136514c1"></a>
### Document.round floats in

`operation_foundation_model_document_business_behavior_document_round_floats_in`

**Inputs** self, doc, fieldnames = no value, do\_not\_round\_fields = no value.

**Local steps**

- If not fieldnames.
  - Set fieldnames from generator of df.fieldname for df drawn from doc.meta.get(“fields”, mapping(“fieldtype” → list(“in”, list(“Currency”, “Float”, “Percent”)))).
    - Draw df from doc.meta.get(“fields”, mapping(“fieldtype” → list(“in”, list(“Currency”, “Float”, “Percent”)))).
- Set rounding\_method from Platform.get\_system\_settings(“rounding\_method”).
- For each fieldname in fieldnames.
  - If (do\_not\_round\_fields and fieldname belongs to do\_not\_round\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in do\_not\_round\_fields → fieldname belongs to do\_not\_round\_fields.
    - Continue with the next iteration or loop test.
  - Evaluate doc.set(fieldname, flt(doc.get(fieldname), self.precision(fieldname, doc.get(“parentfield”)), rounding\_method = rounding\_method)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [precision](operations-047.md#op-0b10c9f2ef5edd).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“rounding\_method”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L5898) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1011)

<a id="op-b3d3e2bcfb72f7"></a>
### Document.get url

`operation_foundation_model_document_business_behavior_document_get_resource_address`

**Inputs** self.

**Explicit results** get\_absolute\_url(self.doctype, self.name).

**Local steps**

- Return get\_absolute\_url(self.doctype, self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0280.json#L6271) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L363) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L974)
