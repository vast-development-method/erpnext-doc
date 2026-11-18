# Record lifecycle and persistence · operations 83

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Recorder suggested index

[Record definition](../../../../data/record-types/recorder_suggested_index.json)

<a id="op-fe10439a674698"></a>
### Recorder Suggested Index.db update

`operation_foundation_core_record_definitions_recorder_suggested_index_business_behavior_recorder_suggested_index_database_update`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6259) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L355)

<a id="op-5a6fcebe4213bc"></a>
### Recorder Suggested Index.delete

`operation_foundation_core_record_definitions_recorder_suggested_index_business_behavior_recorder_suggested_index_delete`

**Inputs** self.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6301) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L356)

<a id="op-2b79b4a8fc5dd4"></a>
### Recorder Suggested Index.get list

`operation_foundation_core_record_definitions_recorder_suggested_index_business_behavior_recorder_suggested_index_get_list`

**Inputs** filters = no value, page\_length = 20, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6343) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L358)

<a id="op-43625581ab6cb4"></a>
### Recorder Suggested Index.get count

`operation_foundation_core_record_definitions_recorder_suggested_index_business_behavior_recorder_suggested_index_get_count`

**Inputs** filters = no value, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6400) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L357)

<a id="op-34640017247e22"></a>
### Recorder Suggested Index.get stats

`operation_foundation_core_record_definitions_recorder_suggested_index_business_behavior_recorder_suggested_index_get_stats`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0096.json#L6446) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L359)

## Service · Rename doc

<a id="op-d81d37afb6d0aa"></a>
### Update document title

`operation_foundation_model_rename_record_business_behavior_update_document_title`

**Inputs** doctype (named only), docname (named only), title (named only, default no value), name (named only, default no value), merge (named only, default false), enqueue (named only, default false), remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** enqueue with “Platform.client.set\_value” · call save on doc · msgprint with translated “Saved”.

**Explicit results** doc.name.

**Explicit failure paths** validation helper — formatted text obj={obj} must be of type str or None · validation helper with Platform.DuplicateEntryError — translated “{0} {1} already exists”.format(doctype, Platform.bold(docname)) · propagate active failure.

**Local steps**

- Set updated\_title from (kwargs.get(“new\_title”) or title).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“new\_title”) → title.
- Set updated\_name from (kwargs.get(“new\_name”) or name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“new\_name”) → name.
- For each obj in list(docname, updated\_title, updated\_name).
  - If not isinstance(obj, (str bitwise or NoneType)).
    - Call the validation error handler Platform.throw(formatted text obj={obj} must be of type str or None).
- Set merge from sbool(merge).
- Set enqueue from sbool(enqueue).
- Set action\_enqueued from (enqueue and not is\_scheduler\_inactive()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in enqueue → not is\_scheduler\_inactive().
- Set doc from Platform.get\_doc(doctype, docname).
- Evaluate doc.check\_permission(permtype = “write”).
- Set title\_field from doc.meta.get\_title\_field().
- Set title\_updated from (updated\_title and title\_field differs from “name” and updated\_title differs from doc.get(title\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in updated\_title → title\_field differs from “name” → updated\_title differs from doc.get(title\_field).
- Set name\_updated from (updated\_name and updated\_name differs from doc.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in updated\_name → updated\_name differs from doc.name.
- Set queue from (kwargs.get(“queue”) or “long”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“queue”) → “long”.
- If name\_updated.
  - If action\_enqueued.
    - Set current\_name from doc.name.
    - Set transformed\_name from doc.run\_method(“before\_rename”, current\_name, updated\_name, merge).
    - If isinstance(transformed\_name, dict).
      - Set transformed\_name from transformed\_name.get(“new”).
    - Set transformed\_name from (transformed\_name or updated\_name).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in transformed\_name → updated\_name.
    - Evaluate doc.queue\_action(“rename”, name = transformed\_name, merge = merge, queue = queue, timeout = 36000).
  - Otherwise.
    - Evaluate doc.\_rename(updated\_name, merge = merge).
- If title\_updated.
  - If (action\_enqueued and name\_updated).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in action\_enqueued → name\_updated.
    - Evaluate Platform.enqueue(“Platform.client.set\_value”, doctype = doc.doctype, name = updated\_name, fieldname = title\_field, value = updated\_title).
  - Otherwise.
    - Attempt the following.
      - Evaluate setattr(doc, title\_field, updated\_title).
      - Evaluate doc.save().
      - Evaluate Platform.msgprint(translated “Saved”, alert = true, indicator = “green”).
    - On failure (Exception) bound to e.
      - If Platform.db.is\_duplicate\_entry(e).
        - Call the validation error handler Platform.throw(translated “{0} {1} already exists”.format(doctype, Platform.bold(docname)), title = translated “Duplicate Name”, exc = Platform.DuplicateEntryError).
      - Propagate the active failure.
- Return doc.name.

**Values supplied outside this operation** effective access from doc.check\_permission(permtype = “write”) · selected callable from doc.run\_method(“before\_rename”, current\_name, updated\_name, merge) · service or queued work from Platform.enqueue(“Platform.client.set\_value”, doctype = doc.doctype, name = updated\_name, fieldname = title\_field, value = updated\_title).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L11) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1286)

<a id="op-6aef1ca541f42c"></a>
### Rename doc

`operation_foundation_model_rename_record_business_behavior_rename_record`

**Inputs** doctype = no value, old = no value, new = no value, force = false, merge = false, ignore\_permissions = false, ignore\_if\_exists = false, show\_alert = true, rebuild\_search = true, doc = no value, validate = true.

**Declared result** str.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** request delete\_doc for doctype · enqueue with “Platform.utils.global\_search.rebuild\_for\_doctype” · msgprint with translated “Document renamed from {0} to {1}”.format(bold(old), bold(new)) · publish realtime with doctype.

**Explicit results** new.

**Explicit failure paths** TypeError(“{doctype, old, new} or {doc, new} are required arguments for Platform.model.rename\_doc”).

**Local steps**

- Set old\_usage\_style from (doctype and old and new).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → old → new.
- Set new\_usage\_style from (doc and new).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → new.
- If not (new\_usage\_style or old\_usage\_style).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_usage\_style → old\_usage\_style.
  - Raise TypeError(“{doctype, old, new} or {doc, new} are required arguments for Platform.model.rename\_doc”).
- Set old from (old or doc.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in old → doc.name.
- Set doctype from (doctype or doc.doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → doc.doctype.
- Set force from sbool(force).
- Set merge from sbool(merge).
- Set meta from Platform.get\_meta(doctype).
- If meta.naming\_rule equals “Autoincrement”.
  - Set old from cint(old).
  - Set new from cint(new).
- If validate.
  - Set old\_doc from (doc or Platform.get\_doc(doctype, old)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc → Platform.get\_doc(doctype, old).
  - Set out from (old\_doc.run\_method(“before\_rename”, old, new, merge) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in old\_doc.run\_method(“before\_rename”, old, new, merge) → mapping().
  - Set new from (out.get(“new”) or new) when isinstance(out, dict), otherwise (out or new).
    - Value choice on isinstance(out, dict) — true gives (out.get(“new”) or new), false gives (out or new).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in out.get(“new”) → new.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in out → new.
  - Set new from validate\_rename(doctype = doctype, old = old, new = new, meta = meta, …).
- If not merge.
  - Evaluate rename\_parent\_and\_child(doctype, old, new, meta).
- Otherwise.
  - Evaluate update\_assignments(old, new, doctype).
- Set link\_fields from get\_link\_fields(doctype).
- Evaluate update\_link\_field\_values(link\_fields, old, new, doctype).
- Evaluate rename\_dynamic\_links(doctype, old, new).
- Evaluate update\_user\_settings(old, new, link\_fields).
- If doctype equals “DocType”.
  - Evaluate rename\_doctype(doctype, old, new).
  - Evaluate update\_customizations(old, new).
- Evaluate update\_attachments(doctype, old, new).
- Evaluate rename\_versions(doctype, old, new).
- Set new\_doc from Platform.get\_doc(doctype, new).
- If validate.
  - Set new\_doc.\_local from getattr(old\_doc, “\_local”, no value).
- Evaluate new\_doc.run\_method(“after\_rename”, old, new, merge).
- If not merge.
  - Evaluate rename\_password(doctype, old, new).
- If merge.
  - Evaluate new\_doc.add\_comment(“Edit”, translated “merged {0} into {1}”.format(Platform.bold(old), Platform.bold(new))).
- Otherwise.
  - Evaluate new\_doc.add\_comment(“Edit”, translated “renamed from {0} to {1}”.format(Platform.bold(old), Platform.bold(new))).
- If merge.
  - Evaluate Platform.delete\_doc(doctype, old, ignore\_permissions = ignore\_permissions).
- Evaluate new\_doc.clear\_cache().
- Evaluate Platform.clear\_cache().
- If rebuild\_search.
  - Evaluate Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = doctype).
- If show\_alert.
  - Evaluate Platform.msgprint(translated “Document renamed from {0} to {1}”.format(bold(old), bold(new)), alert = true, indicator = “green”).
- Evaluate Platform.publish\_realtime(event = “doc\_rename”, message = mapping(“doctype” → doctype, “old” → old, “new” → new), doctype = doctype, docname = old, …).
- Return new.

**Values supplied outside this operation** selected callable from old\_doc.run\_method(“before\_rename”, old, new, merge), getattr(old\_doc, “\_local”, no value) and 1 further calls · service or queued work from Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = doctype), Platform.publish\_realtime(event = “doc\_rename”, message = mapping(“doctype” → doctype, “old” → old, “new” → new), doctype = doctype, docname = old, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L9) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1278)

<a id="op-a831ea70b9238f"></a>
### Update assignments

`operation_foundation_model_rename_record_business_behavior_update_assignments`

**Inputs** old, new, doctype.

**Declared result** no value.

**Record and data access** read doctype via get\_value · read “ToDo” via get\_all.

**State and service calls** request delete\_doc for “ToDo” · request set\_value on doctype.

**Local steps**

- Set old\_assignments from (Platform.parse\_json(Platform.db.get\_value(doctype, old, “\_assign”)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(Platform.db.get\_value(doctype, old, “\_assign”)) → list().
- Set new\_assignments from (Platform.parse\_json(Platform.db.get\_value(doctype, new, “\_assign”)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(Platform.db.get\_value(doctype, new, “\_assign”)) → list().
- Set common\_assignments from list(set(old\_assignments).intersection(new\_assignments)).
- For each user in common\_assignments.
  - Set todos from Platform.get\_all(“ToDo”, mapping(“owner” → user, “reference\_type” → doctype, “reference\_name” → old), list(“name”, “description”)).
  - For each todo in todos.
    - Evaluate Platform.delete\_doc(“ToDo”, todo.name, force = true).
- Set unique\_assignments from list(set((old\_assignments + new\_assignments))).
- Evaluate Platform.db.set\_value(doctype, new, “\_assign”, Platform.as\_json(unique\_assignments, indent = 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L1975) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1281)

<a id="op-59323840ea60d0"></a>
### Update user settings

`operation_foundation_model_rename_record_business_behavior_update_user_settings`

**Inputs** old, new, link\_fields.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Evaluate sync\_user\_settings().
- If not link\_fields.
  - Return no value.
- Set linked\_doctypes from set of d.parent for d drawn from link\_fields where not d.issingle.
  - Draw d from link\_fields, keep a combination only if (not d.issingle).
- Set UserSettings from Platform.qb.Table(“\_\_UserSettings”).
- Set user\_settings\_details from nested operand in the contract(nested operand in the contract).select(“user”, “doctype”, “data”).where((nested operand in the contract.data.like(cstr(old)) bitwise and nested operand in the contract.doctyp ….
- Bind dependencies defaultdict.
- Set user\_settings\_dict from defaultdict(list).
- For each user\_setting in user\_settings\_details.
  - Evaluate user\_settings\_dict at user\_setting.doctype.append(user\_setting).
- For each fields in link\_fields.
  - Set user\_settings from user\_settings\_dict.get(fields.parent).
  - If user\_settings.
    - For each user\_setting in user\_settings.
      - Evaluate update\_user\_settings\_data(user\_setting, “value”, old, new, …).
  - Otherwise.
    - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L2516) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1291)

<a id="op-65f529abfba499"></a>
### Update customizations

`operation_foundation_model_rename_record_business_behavior_update_customizations`

**Inputs** old, new.

**Declared result** no value.

**State and service calls** request set\_value on “Custom DocPerm”.

**Local steps**

- Evaluate Platform.db.set\_value(“Custom DocPerm”, mapping(“parent” → old), “parent”, new, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L3090) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1285)

<a id="op-8fe5fbbf6bf683"></a>
### Update attachments

`operation_foundation_model_rename_record_business_behavior_update_attachments`

**Inputs** doctype, old, new.

**Declared result** no value.

**Local steps**

- If doctype differs from “DocType”.
  - Set File from Platform.qb.DocType(“File”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(File.attached\_to\_name, new).where((File.attached\_to\_name equals old bitwise and File.attached\_to\_doctype equals doctype)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L3214) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1282)

<a id="op-cc93dcae869e6f"></a>
### Rename versions

`operation_foundation_model_rename_record_business_behavior_rename_versions`

**Inputs** doctype, old, new.

**Declared result** no value.

**Local steps**

- Set Version from Platform.qb.DocType(“Version”).
- Evaluate nested operand in the contract(nested operand in the contract).set(Version.docname, new).where((Version.docname equals old bitwise and Version.ref\_doctype equals doctype)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L3457) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1280)

<a id="op-72d098901e6937"></a>
### Rename parent and child

`operation_foundation_model_rename_record_business_behavior_rename_parent_and_child`

**Inputs** doctype, old, new, meta.

**Declared result** no value.

**Local steps**

- Evaluate nested operand in the contract(nested operand in the contract).set(“name”, new).where(Field(“name”) equals old).run().
- Evaluate update\_autoname\_field(doctype, new, meta).
- Evaluate update\_child\_docs(old, new, meta).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L3673) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1277)

<a id="op-7ca9621a55338f"></a>
### Update autoname field

`operation_foundation_model_rename_record_business_behavior_update_autoname_field`

**Inputs** doctype, new, meta.

**Declared result** no value.

**Local steps**

- If meta.get(“autoname”).
  - Set field from meta.get(“autoname”).split(“:”).
  - If (field and field at 0 equals “field”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field → field at 0 equals “field”.
    - Evaluate nested operand in the contract(nested operand in the contract).set(field at 1, new).where(Field(“name”) equals new).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L3915) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1283)

<a id="op-c6bab970831590"></a>
### Validate rename

`operation_foundation_model_rename_record_business_behavior_validate_rename`

**Inputs** doctype, old, new, meta, merge, force = false, ignore\_permissions = false, ignore\_if\_exists = false, save\_point = false, old\_doc = no value.

**Declared result** str.

**Record and data access** read doctype via exists · resolve a document from doctype via get\_doc.

**State and service calls** savepoint \_SAVE\_POINT · rollback.

**Explicit results** new.

**Explicit failure paths** validation helper — translated “Single DocTypes cannot be renamed” · validation helper — translated “Can't rename {0} to {1} because {0} doesn't exist.”.format(old, new) · validation helper — translated “No changes made because old and new name are the same.”.format(old, new) · validation helper — translated “{0} {1} does not exist, select a new target to merge”.format(doctype, new) · validation helper — translated “Another {0} with name {1} exists, select another name”.format(doctype, new) · 3 additional forms in the steps below.

**Local steps**

- If meta.issingle.
  - Call the validation error handler Platform.throw(translated “Single DocTypes cannot be renamed”).
- If save\_point.
  - Set \_SAVE\_POINT from formatted text validate\_rename\_{Platform.generate\_hash(length = 8)}.
  - Evaluate Platform.db.savepoint(\_SAVE\_POINT).
- Set exists from nested operand in the contract(nested operand in the contract).for\_update().select(“name”).run(pluck = true).
- Set exists from exists at 0 when exists, otherwise no value.
  - Value choice on exists — true gives exists at 0, false gives no value.
- If not Platform.db.exists(doctype, old).
  - Call the validation error handler Platform.throw(translated “Can't rename {0} to {1} because {0} doesn't exist.”.format(old, new)).
- If old equals new.
  - Call the validation error handler Platform.throw(translated “No changes made because old and new name are the same.”.format(old, new)).
- If (exists and exists differs from new).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in exists → exists differs from new.
  - Set exists from no value.
- If (merge and not exists).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in merge → not exists.
  - Call the validation error handler Platform.throw(translated “{0} {1} does not exist, select a new target to merge”.format(doctype, new)).
- If (not merge and exists and not ignore\_if\_exists).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not merge → exists → not ignore\_if\_exists.
  - Call the validation error handler Platform.throw(translated “Another {0} with name {1} exists, select another name”.format(doctype, new)).
- Set kwargs from mapping(“doctype” → doctype, “ptype” → “write”, “print\_logs” → false).
- If old\_doc.
  - Set kwargs at “doc” from old\_doc.
- If not (ignore\_permissions or Platform.permissions.has\_permission(expanded names kwargs)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_permissions → Platform.permissions.has\_permission(expanded names kwargs).
  - Call the validation error handler Platform.throw(translated “You need write permission on {0} {1} to rename”.format(doctype, old)).
- If merge.
  - Set kwargs at “doc” from Platform.get\_doc(doctype, new).
  - If not (ignore\_permissions or Platform.permissions.has\_permission(expanded names kwargs)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_permissions → Platform.permissions.has\_permission(expanded names kwargs).
    - Call the validation error handler Platform.throw(translated “You need write permission on {0} {1} to merge”.format(doctype, new)).
- If (not force and not ignore\_permissions and not meta.allow\_rename).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not force → not ignore\_permissions → not meta.allow\_rename.
  - Call the validation error handler Platform.throw(translated “{0} not allowed to be renamed”.format(translated doctype)).
- Set new from validate\_name(doctype, new).
- If save\_point.
  - Evaluate Platform.db.rollback(save\_point = \_SAVE\_POINT).
- Return new.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 8) · effective access from Platform.permissions.has\_permission(expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L12) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1292)

<a id="op-04e0de500d179a"></a>
### Rename doctype

`operation_foundation_model_rename_record_business_behavior_rename_record_type`

**Inputs** doctype, old, new.

**Declared result** no value.

**Local steps**

- Set fields\_with\_options from tuple(“Link”, expanded Platform.model.table\_fields).
- For each fieldtype in fields\_with\_options.
  - Evaluate update\_options\_for\_fieldtype(fieldtype, old, new).
- Evaluate update\_parenttype\_values(old, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L10) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1279)

<a id="op-85d0c5918aed06"></a>
### Update child docs

`operation_foundation_model_rename_record_business_behavior_update_child_records`

**Inputs** old, new, meta.

**Declared result** no value.

**Local steps**

- For each df in meta.get\_table\_fields().
  - Evaluate nested operand in the contract(nested operand in the contract).set(“parent”, new).where((Field(“parent”) equals old bitwise and Field(“parenttype”) equals meta.name)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L5799) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1284)

<a id="op-1aaff2110defd1"></a>
### Update link field values

`operation_foundation_model_rename_record_business_behavior_update_link_field_values`

**Inputs** link\_fields, old, new, doctype.

**Declared result** no value.

**Record and data access** resolve a document from field at “parent” via get\_doc.

**State and service calls** call save on single\_doc · request set\_value on parent.

**Local steps**

- For each field in link\_fields.
  - If field at “issingle”.
    - Attempt the following.
      - Set single\_doc from Platform.get\_doc(field at “parent”).
      - If single\_doc.get(field at “fieldname”) equals old.
        - Evaluate single\_doc.set(field at “fieldname”, new).
        - Set single\_doc.flags.ignore\_mandatory from true.
        - Set single\_doc.flags.ignore\_links from true.
        - Evaluate single\_doc.save(ignore\_permissions = true).
    - On failure (ImportError).
      - Take no action here.
  - Otherwise.
    - Set parent from field at “parent”.
    - Set docfield from field at “fieldname”.
    - If (parent equals new and doctype equals “DocType”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent equals new → doctype equals “DocType”.
      - Set parent from old.
    - Evaluate Platform.db.set\_value(parent, mapping(docfield → cstr(old)), docfield, cstr(new), update\_modified = false).
  - If (doctype equals “DocType” and field at “parent” equals old).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “DocType” → field at “parent” equals old.
    - Set field at “parent” from new.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0288.json#L6042) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L702) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1287)

<a id="op-cefa9ff53aa5a2"></a>
### Get link fields

`operation_foundation_model_rename_record_business_behavior_get_link_fields`

**Inputs** doctype.

**Declared result** list at dict.

**Record and data access** read “DocType” via get\_all.

**Explicit results** Platform.flags.link\_fields at doctype.

**Local steps**

- If not Platform.flags.link\_fields.
  - Set Platform.flags.link\_fields from mapping().
- If doctype does not belong to Platform.flags.link\_fields.
  - Set dt from Platform.qb.DocType(“DocType”).
  - Set df from Platform.qb.DocType(“DocField”).
  - Set cf from Platform.qb.DocType(“Custom Field”).
  - Set ps from Platform.qb.DocType(“Property Setter”).
  - Set standard\_fields\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(df.parent, df.fieldname, dt.issingle.as\_(“issingle ….
  - Set virtual\_doctypes from Platform.get\_all(“DocType”, mapping(“is\_virtual” → 1), pluck = “name”).
  - Set standard\_fields from standard\_fields\_query.run(as\_dict = true).
  - Set cf\_issingle from nested operand in the contract(nested operand in the contract).select(dt.issingle).where(dt.name equals cf.dt).as\_(“issingle”).
  - Set custom\_fields from nested operand in the contract.qb.from\_(cf).select(cf.dt.as\_(“parent”), cf.fieldname, cf\_issingle).where(((cf.options equals doctype bitwise and cf.fieldtype equals “Link”) bitwise and cf.is\_virtual equals 0)).
  - If virtual\_doctypes.
    - Set custom\_fields from custom\_fields.where(cf.dt.notin(virtual\_doctypes)).
  - Set custom\_fields from custom\_fields.run(as\_dict = true).
  - Set ps\_issingle from nested operand in the contract(nested operand in the contract).select(dt.issingle).where(dt.name equals ps.doc\_type).as\_(“issingle”).
  - Set property\_setter\_fields from nested operand in the contract.qb.from\_(ps).select(ps.doc\_type.as\_(“parent”), ps.field\_name.as\_(“fieldname”), ps\_issingle).where(((ps.property equals “options” bitwise and ps.value equals doctype) bitwise  ….
  - If virtual\_doctypes.
    - Set property\_setter\_fields from property\_setter\_fields.where(ps.doc\_type.notin(virtual\_doctypes)).
  - Set property\_setter\_fields from property\_setter\_fields.run(as\_dict = true).
  - Set Platform.flags.link\_fields at doctype from ((standard\_fields + custom\_fields) + property\_setter\_fields).
- Return Platform.flags.link\_fields at doctype.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0289.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1274)

<a id="op-29078bb231f99a"></a>
### Update options for fieldtype

`operation_foundation_model_rename_record_business_behavior_update_options_for_fieldtype`

**Inputs** fieldtype, old, new.

**Declared result** no value.

**Record and data access** read “DocField” via get\_all · resolve a document from “DocType” via get\_doc.

**State and service calls** call save on doctype.

**Local steps**

- Set CustomField from Platform.qb.DocType(“Custom Field”).
- Set PropertySetter from Platform.qb.DocType(“Property Setter”).
- If Platform.conf.developer\_mode.
  - For each name in Platform.get\_all(“DocField”, filters = mapping(“options” → old), pluck = “parent”).
    - If name belongs to tuple(old, new).
      - Continue with the next iteration or loop test.
    - Set doctype from Platform.get\_doc(“DocType”, name).
    - Set save from false.
    - For each f in doctype.fields.
      - If f.options equals old.
        - Set f.options from new.
        - Set save from true.
    - If save.
      - Evaluate doctype.save().
- Set DocField from Platform.qb.DocType(“DocField”).
- Evaluate nested operand in the contract(nested operand in the contract).set(DocField.options, new).where((DocField.fieldtype equals fieldtype bitwise and DocField.options equals old)).run().
- Evaluate nested operand in the contract(nested operand in the contract).set(CustomField.options, new).where((CustomField.fieldtype equals fieldtype bitwise and CustomField.options equals old)).run().
- Evaluate nested operand in the contract(nested operand in the contract).set(PropertySetter.value, new).where((PropertySetter.property equals “options” bitwise and PropertySetter.value equals old)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0289.json#L1452) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1288)

<a id="op-7e356150b9c6a3"></a>
### Get select fields

`operation_foundation_model_rename_record_business_behavior_get_select_fields`

**Inputs** old, new.

**Declared result** list at dict.

**Explicit results** ((standard\_fields + custom\_select\_fields) + property\_setter\_select\_fields).

**Local steps**

- Set df from Platform.qb.DocType(“DocField”).
- Set dt from Platform.qb.DocType(“DocType”).
- Set cf from Platform.qb.DocType(“Custom Field”).
- Set ps from Platform.qb.DocType(“Property Setter”).
- Set st\_issingle from nested operand in the contract(nested operand in the contract).select(dt.issingle).where(dt.name equals df.parent).as\_(“issingle”).
- Set standard\_fields from nested operand in the contract(nested operand in the contract).select(df.parent, df.fieldname, st\_issingle).where((((nested operand in the contract differs from nested operand in the contract bitwise and n ….
- Set cf\_issingle from nested operand in the contract(nested operand in the contract).select(dt.issingle).where(dt.name equals cf.dt).as\_(“issingle”).
- Set custom\_select\_fields from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“parent”), cf.fieldname, cf\_issingle).where(((nested operand in the contract.dt differs from new bit ….
- Set ps\_issingle from nested operand in the contract(nested operand in the contract).select(dt.issingle).where(dt.name equals ps.doc\_type).as\_(“issingle”).
- Set property\_setter\_select\_fields from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“parent”), nested operand in the contract.as\_(“fieldname”), ps\_issingle).where((((nested operand in  ….
- Return ((standard\_fields + custom\_select\_fields) + property\_setter\_select\_fields).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0289.json#L2258) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1275)

<a id="op-c34962d7b5b807"></a>
### Update select field values

`operation_foundation_model_rename_record_business_behavior_update_select_field_values`

**Inputs** old, new.

**Local steps**

- Bind dependencies Replace.
- Set DocField from Platform.qb.DocType(“DocField”).
- Set CustomField from Platform.qb.DocType(“Custom Field”).
- Set PropertySetter from Platform.qb.DocType(“Property Setter”).
- Evaluate nested operand in the contract(nested operand in the contract).set(DocField.options, Replace(nested operand in the contract.options, old, new)).where(((nested operand in the contract.fieldtype equals “Sele ….run().
- Evaluate nested operand in the contract(nested operand in the contract).set(CustomField.options, Replace(nested operand in the contract.options, old, new)).where(((nested operand in the contract.fieldtype equals “S ….run().
- Evaluate nested operand in the contract(nested operand in the contract).set(PropertySetter.value, Replace(nested operand in the contract.value, old, new)).where((((nested operand in the contract equals nested opera ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0289.json#L3503) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1290)

<a id="op-43a74bd05548ed"></a>
### Update parenttype values

`operation_foundation_model_rename_record_business_behavior_update_parenttype_values`

**Inputs** old, new.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all · read “Property Setter” via get\_all.

**Local steps**

- Set child\_doctypes from Platform.get\_all(“DocField”, fields = list(“options”, “fieldname”), filters = mapping(“parent” → new, “fieldtype” → list(“in”, Platform.model.table\_fields))).
- Set custom\_child\_doctypes from Platform.get\_all(“Custom Field”, fields = list(“options”, “fieldname”), filters = mapping(“dt” → new, “fieldtype” → list(“in”, Platform.model.table\_fields))).
- Update child\_doctypes using + custom\_child\_doctypes.
- Set fields from list of d at “fieldname” for d drawn from child\_doctypes.
  - Draw d from child\_doctypes.
- Set property\_setter\_child\_doctypes from Platform.get\_all(“Property Setter”, filters = mapping(“doc\_type” → new, “property” → “options”, “field\_name” → tuple(“in”, fields)), pluck = “value”).
- Set child\_doctypes from set((list(generator of d at “options” for d drawn from child\_doctypes) + property\_setter\_child\_doctypes)).
  - Draw d from child\_doctypes.
- For each doctype in child\_doctypes.
  - If Platform.get\_meta(doctype).is\_virtual.
    - Continue with the next iteration or loop test.
  - Set table from Platform.qb.DocType(doctype).
  - Evaluate nested operand in the contract(nested operand in the contract).set(table.parenttype, new).where(table.parenttype equals old).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0289.json#L4404) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1289)

<a id="op-1978c465acd18c"></a>
### Rename dynamic links

`operation_foundation_model_rename_record_business_behavior_rename_dynamic_links`

**Inputs** doctype, old, new.

**Local steps**

- Set Singles from Platform.qb.DocType(“Singles”).
- For each df in get\_dynamic\_link\_map().get(doctype, list()).
  - Set meta from Platform.get\_meta(df.parent).
  - If meta.is\_virtual.
    - Continue with the next iteration or loop test.
  - If meta.issingle.
    - Set refdoc from Platform.db.get\_singles\_dict(df.parent).
    - If (refdoc.get(df.options) equals doctype and refdoc.get(df.fieldname) equals old).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in refdoc.get(df.options) equals doctype → refdoc.get(df.fieldname) equals old.
      - Evaluate nested operand in the contract(nested operand in the contract).set(Singles.value, new).where(((nested operand in the contract.field equals nested operand in the contract.fieldname bitwise and nested operan ….run().
  - Otherwise.
    - Set parent from df.parent when df.parent differs from new, otherwise old.
      - Value choice on df.parent differs from new — true gives df.parent, false gives old.
    - Evaluate nested operand in the contract(nested operand in the contract).set(df.fieldname, new).where((Field(nested operand in the contract.options) equals doctype bitwise and Field(nested operand in the contract.fi ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0289.json#L5411) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1276)
