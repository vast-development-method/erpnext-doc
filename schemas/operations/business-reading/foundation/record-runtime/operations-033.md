# Record lifecycle and persistence · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Delete doc

<a id="op-247cc451f09c69"></a>
### Delete dynamic links

`operation_foundation_model_delete_record_business_behavior_delete_dynamic_links`

**Inputs** doctype, name.

**Local steps**

- Evaluate delete\_references(“Submission Queue”, doctype, name, “ref\_doctype”, …).
- Evaluate delete\_references(“ToDo”, doctype, name, “reference\_type”).
- Evaluate delete\_references(“Email Unsubscribe”, doctype, name).
- Evaluate delete\_references(“DocShare”, doctype, name, “share\_doctype”, …).
- Evaluate delete\_references(“Version”, doctype, name, “ref\_doctype”, …).
- Evaluate delete\_references(“Comment”, doctype, name).
- Evaluate delete\_references(“View Log”, doctype, name).
- Evaluate delete\_references(“Document Follow”, doctype, name, “ref\_doctype”, …).
- Evaluate delete\_references(“Notification Log”, doctype, name, “document\_type”, …).
- Evaluate clear\_timeline\_references(doctype, name).
- Evaluate clear\_references(“Communication”, doctype, name).
- Evaluate clear\_references(“Activity Log”, doctype, name).
- Evaluate clear\_references(“Activity Log”, doctype, name, “timeline\_doctype”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L70) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L927)

<a id="op-3227a363d05362"></a>
### Delete references

`operation_foundation_model_delete_record_business_behavior_delete_references`

**Inputs** doctype, reference\_doctype, reference\_name, reference\_doctype\_field = “reference\_doctype”, reference\_name\_field = “reference\_name”.

**State and service calls** request delete on doctype.

**Local steps**

- Evaluate Platform.db.delete(doctype, mapping(reference\_doctype\_field → reference\_doctype, reference\_name\_field → reference\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L2701) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L317) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L930)

<a id="op-d7663859c430b2"></a>
### Clear references

`operation_foundation_model_delete_record_business_behavior_clear_references`

**Inputs** doctype, reference\_doctype, reference\_name, reference\_doctype\_field = “reference\_doctype”, reference\_name\_field = “reference\_name”.

**State and service calls** execute a supplied database query.

**Local steps**

- Evaluate Platform.db.sql(formatted text update  ′tab{doctype}′  set  {reference\_doctype\_field}=NULL, {reference\_name\_field}=NULL  where  {reference\_doctype\_field}=%s and {reference\_n, tuple(reference\_doctyp ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L2832) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L924)

<a id="op-a1afa651e6c422"></a>
### Clear timeline references

`operation_foundation_model_delete_record_business_behavior_clear_timeline_references`

**Inputs** link\_doctype, link\_name.

**State and service calls** request delete on “Communication Link”.

**Local steps**

- Evaluate Platform.db.delete(“Communication Link”, mapping(“link\_doctype” → link\_doctype, “link\_name” → link\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3029) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L925)

<a id="op-f284b0b7a94693"></a>
### Insert feed

`operation_foundation_model_delete_record_business_behavior_insert_feed`

**Inputs** doc.

**Record and data access** resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Deleted”, “reference\_doctype” → doc.doctype, “subject” → formatted text {translated doc.doctype} {doc.name}, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Deleted”, “reference\_doctype” → doc.doctype, “subject” → formatted text {translated doc.doctype} {doc.name}, …)).

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_install or Platform.flags.in\_uninstall or Platform.flags.in\_import or getattr(doc, “no\_feed\_on\_delete”, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_uninstall → Platform.flags.in\_import → getattr(doc, “no\_feed\_on\_delete”, false).
  - Return no value.
- Bind dependencies get\_fullname.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Deleted”, “reference\_doctype” → doc.doctype, “subject” → formatted text {translated nested operand in the contract.doctype} {doc.name}, …)) ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, “no\_feed\_on\_delete”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3136) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L933)

<a id="op-192d42811230ca"></a>
### Delete controllers

`operation_foundation_model_delete_record_business_behavior_delete_controllers`

**Inputs** doctype, module.

**Local steps**

- Set module\_path from get\_module\_path(module).
- Set dir\_path from os.path.join(module\_path, “doctype”, Platform.scrub(doctype)).
- Evaluate shutil.rmtree(dir\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3457) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L926)

## Record · Deleted document

[Record definition](../../../../data/record-types/deleted_document.json)

<a id="op-48dfe00ff2f895"></a>
### Deleted Document.clear old logs

`operation_foundation_core_record_definitions_deleted_document_business_behavior_deleted_document_clear_old_logs`

**Inputs** days = 180.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Deleted Document”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L6905) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1351)

<a id="op-ac69fca0bd32d3"></a>
### Restore

`operation_foundation_core_record_definitions_deleted_document_business_behavior_restore`

**Inputs** name, alert = true.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Deleted Document” via get\_doc · resolve a document from json.loads(deleted.data) via get\_doc · read “Workflow” via get\_value.

**State and service calls** call insert on doc · msgprint with translated “Cancelled Document restored as Draft” · request set\_value on doc.doctype · call db\_update on deleted · msgprint with translated “Document Restored”.

**Explicit failure paths** validation helper with Platform.DocumentAlreadyRestored — translated “Document {0} Already Restored”.format(name) · validation helper with Platform.PermissionError — translated “You do not have permission to create or restore documents of type {0}.”.format(doc.doctype) · validation helper with Platform.PermissionError — translated “You do not have permission to restore this document.”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set deleted from Platform.get\_doc(“Deleted Document”, name).
- If deleted.restored.
  - Call the validation error handler Platform.throw(translated “Document {0} Already Restored”.format(name), exc = Platform.DocumentAlreadyRestored).
- Set doc from Platform.get\_doc(json.loads(deleted.data)).
- If not Platform.has\_permission(doc.doctype, “create”).
  - Call the validation error handler Platform.throw(translated “You do not have permission to create or restore documents of type {0}.”.format(doc.doctype), Platform.PermissionError).
- If not Platform.has\_permission(doc.doctype, “read”, doc = doc).
  - Call the validation error handler Platform.throw(translated “You do not have permission to restore this document.”, Platform.PermissionError).
- Set original\_owner from doc.get(“owner”).
- Set original\_creation from doc.get(“creation”).
- Set original\_modified from doc.get(“modified”).
- Set original\_modified\_by from doc.get(“modified\_by”).
- Set doc.flags.from\_restore from true.
- Attempt the following.
  - Evaluate doc.insert().
- On failure (Platform.DocstatusTransitionError).
  - Evaluate Platform.msgprint(translated “Cancelled Document restored as Draft”).
  - Set doc.docstatus from 0.
  - Set active\_workflow from get\_workflow\_name(doc.doctype).
  - If active\_workflow.
    - Set workflow\_state\_fieldname from Platform.get\_value(“Workflow”, active\_workflow, “workflow\_state\_field”).
    - If doc.get(workflow\_state\_fieldname).
      - Evaluate doc.set(workflow\_state\_fieldname, no value).
  - Evaluate doc.insert().
- Evaluate Platform.db.set\_value(doc.doctype, doc.name, mapping(“owner” → original\_owner, “creation” → original\_creation, “modified” → original\_modified, “modified\_by” → original\_modified\_by), update\_modified = false).
- Evaluate doc.add\_comment(“Edit”, translated “restored {0} as {1}”.format(deleted.deleted\_name, doc.name)).
- Set deleted.new\_name from doc.name.
- Set deleted.restored from 1.
- Evaluate deleted.db\_update().
- If alert.
  - Evaluate Platform.msgprint(translated “Document Restored”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”), Platform.has\_permission(doc.doctype, “create”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1352)

<a id="op-218365b252575c"></a>
### Bulk restore

`operation_foundation_core_record_definitions_deleted_document_business_behavior_bulk_restore`

**Inputs** docnames.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** commit · rollback.

**Explicit results** mapping(“restored” → restored, “invalid” → invalid, “failed” → failed).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set docnames from Platform.parse\_json(docnames).
- Set message from translated “Restoring Deleted Document”.
- Set tuple(restored, invalid, failed) from tuple(list(), list(), list()).
- For each tuple(i, d) in enumerate(docnames).
  - Attempt the following.
    - Evaluate show\_progress(docnames, message, (i + 1), d).
    - Evaluate restore(d, alert = false).
    - Evaluate Platform.db.commit().
    - Evaluate restored.append(d).
  - On failure (Platform.DocumentAlreadyRestored).
    - Evaluate Platform.clear\_last\_message().
    - Evaluate invalid.append(d).
  - On failure (Exception).
    - Evaluate Platform.clear\_last\_message().
    - Evaluate failed.append(d).
    - Evaluate Platform.db.rollback().
- Return mapping(“restored” → restored, “invalid” → invalid, “failed” → failed).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L1194) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1360) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1350)

## Record · Docfield

<a id="op-69b91f3aa7aed6"></a>
### Doc Field.get link doctype

`operation_foundation_core_record_definitions_record_field_business_behavior_record_field_get_link_record_type`

**Inputs** self.

**Record and data access** read “DocField” via get\_value.

**Explicit results** self.options · Platform.db.get\_value(“DocField”, mapping(“fieldtype” → “Link”, “parenttype” → “DocType”, “parent” → table\_doctype, “in\_list\_view” → 1), “options”).

**Local steps**

- If self.fieldtype equals “Link”.
  - Return self.options.
- If self.fieldtype equals “Table MultiSelect”.
  - Set table\_doctype from self.options.
  - Return Platform.db.get\_value(“DocField”, mapping(“fieldtype” → “Link”, “parenttype” → “DocType”, “parent” → table\_doctype, “in\_list\_view” → 1), “options”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L2437) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L84) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L287)

<a id="op-1399087d81915c"></a>
### Doc Field.get select options

`operation_foundation_core_record_definitions_record_field_business_behavior_record_field_get_select_options`

**Inputs** self.

**Explicit results** list of d for d drawn from options.split(whitespace '\\n') where d.

**Local steps**

- If self.fieldtype equals “Select”.
  - Set options from (self.options or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.options → empty text.
  - Return list of d for d drawn from options.split(whitespace '\\n') where d.
    - Draw d from options.split(whitespace '\\n'), keep a combination only if (d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L2663) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L85) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L288)

<a id="op-8e5732163c9160"></a>
### Doc Field.repr

`operation_foundation_core_record_definitions_record_field_business_behavior_record_field_representation`

**Inputs** self.

**Explicit results** formatted text &lt;{self.fieldtype}{doctype}: {self.fieldname}{docstatus}{parent}{unsaved}&gt;.

**Local steps**

- Set unsaved from “unsaved” when not self.name, otherwise empty text.
  - Value choice on not self.name — true gives “unsaved”, false gives empty text.
- Set doctype from self.\_\_class\_\_.\_\_name\_\_.
- Set docstatus from formatted text  docstatus={self.docstatus} when self.docstatus, otherwise empty text.
  - Value choice on self.docstatus — true gives formatted text  docstatus={self.docstatus}, false gives empty text.
- Set parent from formatted text  parent={self.parent} when getattr(self, “parent”, no value), otherwise empty text.
  - Value choice on getattr(self, “parent”, no value) — true gives formatted text  parent={self.parent}, false gives empty text.
- Return formatted text &lt;{self.fieldtype}{doctype}: {self.fieldname}{docstatus}{parent}{unsaved}&gt;.

**Values supplied outside this operation** selected callable from getattr(self, “parent”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L2793) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L86) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L289)

## Service · Docfield

<a id="op-23515df11a4306"></a>
### Supports translation

`operation_foundation_model_record_field_business_behavior_supports_translation`

**Inputs** fieldtype.

**Explicit results** fieldtype belongs to list(“Data”, “Select”, “Text”, “Small Text”, …).

**Local steps**

- Return fieldtype belongs to list(“Data”, “Select”, “Text”, “Small Text”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3605) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1266)

## Record · Docshare

<a id="op-4896a730f0733e"></a>
### Doc Share.validate

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_user().
- Evaluate self.check\_share\_permission().
- Evaluate self.check\_is\_submittable().
- Evaluate self.cascade\_permissions\_downwards().
- Evaluate self.get\_doc().run\_method(“validate\_share”, self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate user](operations-033.md#op-2b643d78b3c871), [check share permission](operations-033.md#op-e437e7d33fc177), [check is submittable](operations-033.md#op-60610814205e54), [cascade permissions downwards](operations-033.md#op-6cc2a4e3cb6bde), [get doc](operations-033.md#op-557fd99fad26a6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L3091) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1361)

<a id="op-6cc2a4e3cb6bde"></a>
### Doc Share.cascade permissions downwards

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_cascade_permissions_downwards`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L3243) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1356)

<a id="op-557fd99fad26a6"></a>
### Doc Share.get doc

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_get_record`

**Inputs** self.

**Explicit results** self.\_doc.

**Local steps**

- If not getattr(self, “\_doc”, no value).
  - Set self.\_doc from Platform.get\_lazy\_doc(self.share\_doctype, self.share\_name).
- Return self.\_doc.

**Values supplied outside this operation** selected callable from getattr(self, “\_doc”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L3357) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1359)

<a id="op-2b643d78b3c871"></a>
### Doc Share.validate user

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_validate_user`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “User is mandatory for Share”.

**Local steps**

- If self.everyone.
  - Set self.user from no value.
- Otherwise.
  - If not self.user.
    - Call the validation error handler Platform.throw(translated “User is mandatory for Share”, Platform.MandatoryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L3477) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1372) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1362)

<a id="op-e437e7d33fc177"></a>
### Doc Share.check share permission

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_check_share_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L3604) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1358)

<a id="op-60610814205e54"></a>
### Doc Share.check is submittable

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_check_is_submittable`

**Inputs** self.

**Record and data access** read “DocType” via get\_value.

**Explicit failure paths** validation helper — translated “Cannot share {0} with submit permission as the doctype {1} is not submittable”.format(Platform.bold(self.share\_name), Platform.bold(self.share\_doctype)).

**Local steps**

- If (self.submit and not cint(Platform.db.get\_value(“DocType”, self.share\_doctype, “is\_submittable”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.submit → not cint(Platform.db.get\_value(“DocType”, self.share\_doctype, “is\_submittable”)).
  - Call the validation error handler Platform.throw(translated “Cannot share {0} with submit permission as the doctype {1} is not submittable”.format(Platform.bold(self.share\_name), Platform.bold(self.share\_doctype))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L3766) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1357)

<a id="op-ba4c006f334336"></a>
### Doc Share.after insert

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_after_insert`

**Inputs** self.

**Local steps**

- Set doc from self.get\_doc().
- Set owner from get\_fullname(self.owner).
- If self.everyone.
  - Evaluate doc.add\_comment(“Shared”, translated “{0} shared this document with everyone”.format(owner)).
- Otherwise.
  - Evaluate doc.add\_comment(“Shared”, translated “{0} shared this document with {1}”.format(owner, get\_fullname(self.user))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get doc](operations-033.md#op-557fd99fad26a6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L3984) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1365) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1355)

<a id="op-4766a6ffa93edc"></a>
### Doc Share.on trash

`operation_foundation_core_record_definitions_docshare_business_behavior_record_share_on_trash`

**Inputs** self.

**Local steps**

- If not self.flags.ignore\_share\_permission.
  - Evaluate self.check\_share\_permission().
- Evaluate self.get\_doc().add\_comment(“Unshared”, translated “{0} un-shared this document with {1}”.format(get\_fullname(self.owner), get\_fullname(self.user))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check share permission](operations-033.md#op-e437e7d33fc177), [get doc](operations-033.md#op-557fd99fad26a6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L4220) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1360)

<a id="op-6f822c6ea04583"></a>
### On doctype update

`operation_foundation_core_record_definitions_docshare_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “DocShare”.

**Local steps**

- Evaluate Platform.db.add\_index(“DocShare”, list(“user”, “share\_doctype”)).
- Evaluate Platform.db.add\_index(“DocShare”, list(“share\_doctype”, “share\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0061.json#L4403) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1354)

## Service · Docstatus

<a id="op-795af625aa2c03"></a>
### Doc Status.is draft

`operation_foundation_model_record_state_business_behavior_record_status_is_draft`

**Inputs** self.

**Explicit results** self equals DocStatus.DRAFT.

**Local steps**

- Return self equals DocStatus.DRAFT.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3675) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1270)

<a id="op-9dc60d4baa4186"></a>
### Doc Status.is submitted

`operation_foundation_model_record_state_business_behavior_record_status_is_submitted`

**Inputs** self.

**Explicit results** self equals DocStatus.SUBMITTED.

**Local steps**

- Return self equals DocStatus.SUBMITTED.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3728) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1271)
