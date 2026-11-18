# Record lifecycle and persistence · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Access log

[Record definition](../../../../data/record-types/access_log.json)

<a id="op-9b55aa7fd5940f"></a>
### Access Log.clear old logs

`operation_foundation_core_record_definitions_access_log_business_behavior_access_log_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Access Log”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L5593) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L925)

<a id="op-999093c806e801"></a>
### Make access log

`operation_foundation_core_record_definitions_access_log_business_behavior_make_access_log`

**Inputs** doctype = no value, document = no value, method = no value, file\_type = no value, report\_name = no value, filters = no value, page = no value, columns = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.write\_only(), retry(stop = stop\_after\_attempt(3), retry = retry\_if\_exception\_type(Platform.DuplicateEntryError), reraise = true).

**Record and data access** resolve a document from mapping(“doctype” → “Access Log”, “user” → Platform.session.user, “export\_from” → doctype, “reference\_document” → document, …) via get\_doc.

**State and service calls** call db\_insert on access\_log.

**Local steps**

- Set access\_log from Platform.get\_doc(mapping(“doctype” → “Access Log”, “user” → Platform.session.user, “export\_from” → doctype, “reference\_document” → document, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(filters) → no value.
- If not Platform.in\_test.
  - Evaluate access\_log.deferred\_insert().
- Otherwise.
  - Evaluate access\_log.db\_insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L5778) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L926)

## Record · Activity log

[Record definition](../../../../data/record-types/activity_log.json)

<a id="op-e2b1b3316bdbf0"></a>
### Activity Log.before insert

`operation_foundation_core_record_definitions_activity_log_business_behavior_activity_log_before_insert`

**Inputs** self.

**Local steps**

- Set self.full\_name from strip\_html(get\_fullname(self.user)).
- Set self.date from now().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L481) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L932)

<a id="op-9cc0ad2760bf87"></a>
### Activity Log.validate

`operation_foundation_core_record_definitions_activity_log_business_behavior_activity_log_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status().
- Evaluate set\_timeline\_doc(self).
- Evaluate self.set\_ip\_address().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-001.md#op-586d2c0362d7b1), [set ip address](operations-001.md#op-bdb2ade5d8d33f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L587) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L936)

<a id="op-586d2c0362d7b1"></a>
### Activity Log.set status

`operation_foundation_core_record_definitions_activity_log_business_behavior_activity_log_set_status`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.is\_new().
  - Return no value.
- If (self.reference\_doctype and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name.
  - Set self.status from “Linked”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L679) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L935)

<a id="op-bdb2ade5d8d33f"></a>
### Activity Log.set ip address

`operation_foundation_core_record_definitions_activity_log_business_behavior_activity_log_set_internet_protocol_address`

**Inputs** self.

**Local steps**

- If self.operation belongs to tuple(“Login”, “Logout”).
  - Set self.ip\_address from Platform.local.request\_ip.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L786) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L934)

<a id="op-e9e9a8c327b23d"></a>
### Activity Log.clear old logs

`operation_foundation_core_record_definitions_activity_log_business_behavior_activity_log_clear_old_logs`

**Inputs** days = no value.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on doctype.

**Local steps**

- If not days.
  - Set days from 90.
- Set doctype from DocType(“Activity Log”).
- Evaluate Platform.db.delete(doctype, filters = doctype.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L876) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L933)

<a id="op-e7bb940850595e"></a>
### On doctype update

`operation_foundation_core_record_definitions_activity_log_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Activity Log”.

**Local steps**

- Evaluate Platform.db.add\_index(“Activity Log”, list(“reference\_doctype”, “reference\_name”)).
- Evaluate Platform.db.add\_index(“Activity Log”, list(“timeline\_doctype”, “timeline\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L1062) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L938)

<a id="op-193796e3823690"></a>
### Add authentication log

`operation_foundation_core_record_definitions_activity_log_business_behavior_add_authentication_log`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** subject, user, operation, status.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L1194) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L937)

<a id="op-e43e944c6e55ab"></a>
### Login feed

`operation_foundation_core_record_definitions_activity_log_feed_business_behavior_login_feed`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** login\_manager.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L1393) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L939)

<a id="op-55971641a68ee9"></a>
### Logout feed

`operation_foundation_core_record_definitions_activity_log_feed_business_behavior_logout_feed`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, reason.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L1541) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L940)

## Record · Api request log

<a id="op-2a53aef37be843"></a>
### APIRequest Log.clear old logs

`operation_foundation_core_record_definitions_application_interface_request_log_business_behavior_application_programming_interface_request_log_clear_old_logs`

**Inputs** days = 90.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“API Request Log”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L3362) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L946)

## Record · Attachment queue

<a id="op-8198d0b12f5b74"></a>
### Attachment Queue.validate

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_attachmentqueue_validate`

**Inputs** self.

**Local steps**

- If self.document\_type.
  - Evaluate self.validate\_document\_type().
- If self.source\_file.
  - Evaluate self.validate\_source\_file\_type().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate document type](operations-001.md#op-f03b01ec83cf66), [validate source file type](operations-001.md#op-129c9444bd7de1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L608) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L584)

<a id="op-663eff828958c5"></a>
### Attachment Queue.notify update

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_attachmentqueue_notify_update`

**Inputs** self.

**Local steps**

- Evaluate super().notify\_update().
- Evaluate publish\_queue\_update(self.document\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L607) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L583)

<a id="op-f03b01ec83cf66"></a>
### Attachment Queue.validate document type

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_attachmentqueue_validate_document_type`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} does not allow document creation from an uploaded file.”.format(Platform.bold(translated self.document\_type)).

**Local steps**

- If not Platform.get\_meta(self.document\_type).get(“enable\_upload\_first\_workflow”).
  - Call the validation error handler Platform.throw(translated “{0} does not allow document creation from an uploaded file.”.format(Platform.bold(translated self.document\_type)), title = translated “Not Enabled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L609) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L585)

<a id="op-129c9444bd7de1"></a>
### Attachment Queue.validate source file type

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_attachmentqueue_validate_source_file_type`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Attach a PDF or an image. Other file types cannot be previewed.”.

**Local steps**

- If get\_file\_extension(self.source\_file) does not belong to SUPPORTED\_EXTENSIONS.
  - Call the validation error handler Platform.throw(translated “Attach a PDF or an image. Other file types cannot be previewed.”, title = translated “Unsupported File”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L586)

<a id="op-4af8c7809ec565"></a>
### Attachment Queue.link to document

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_attachmentqueue_link_to_document`

**Inputs** self, document\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** read self.doctype via get\_value · read self.document\_type via exists.

**State and service calls** call db\_set on self.

**Explicit results** claimed · document\_name.

**Explicit failure paths** validation helper — translated “{0} has already produced {1} {2}.”.format(Platform.bold(self.name), Platform.bold(translated self.document\_type), Platform.bold(claimed)) · validation helper — translated “{0} {1} does not exist.”.format(Platform.bold(translated self.document\_type), Platform.bold(document\_name)).

**Local steps**

- Set document\_name from cstr(document\_name).
- Set claimed from Platform.db.get\_value(self.doctype, self.name, “created\_document”, for\_update = true).
- Set source\_file from self.source\_file.
- If claimed.
  - If claimed equals document\_name.
    - Return claimed.
  - Call the validation error handler Platform.throw(translated “{0} has already produced {1} {2}.”.format(Platform.bold(self.name), Platform.bold(translated self.document\_type), Platform.bold(claimed))).
- If not Platform.db.exists(self.document\_type, document\_name).
  - Call the validation error handler Platform.throw(translated “{0} {1} does not exist.”.format(Platform.bold(translated self.document\_type), Platform.bold(document\_name))).
- Evaluate Platform.has\_permission(self.document\_type, “write”, doc = document\_name, throw = true).
- Evaluate self.attach\_source\_file\_to(self.document\_type, document\_name, source\_file).
- Evaluate self.db\_set(“created\_document”, document\_name).
- Evaluate publish\_queue\_update(self.document\_type).
- Return document\_name.

**Methods declared on this owner** [attach source file to](operations-001.md#op-0e980291834c5d).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.document\_type, “write”, doc = document\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L582)

<a id="op-0e980291834c5d"></a>
### Attachment Queue.attach source file to

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_attachmentqueue_attach_source_file_to`

**Inputs** self, document\_type, document\_name, source\_file.

**Declared result** no value.

**Record and data access** read “File” via get\_value · resolve a document from “File” via get\_doc.

**Explicit failure paths** validation helper — translated “The file for {0} is no longer available.”.format(Platform.bold(self.name)).

**Local steps**

- Set file\_name from Platform.db.get\_value(“File”, mapping(“file\_url” → source\_file, “attached\_to\_doctype” → self.doctype, “attached\_to\_name” → self.name)).
- If not file\_name.
  - Call the validation error handler Platform.throw(translated “The file for {0} is no longer available.”.format(Platform.bold(self.name))).
- Evaluate Platform.get\_doc(“File”, file\_name).create\_attachment\_copy(attached\_to\_doctype = document\_type, attached\_to\_name = document\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L122) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L604) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L580)

<a id="op-a1b95145447a00"></a>
### Attachment Queue.clear old logs

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_attachmentqueue_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**Declared result** no value.

**Record and data access** read “Attachment Queue” via get\_all.

**State and service calls** request delete\_doc for “Attachment Queue”.

**Local steps**

- Set cutoff from add\_to\_date(now(), days = negative cint(days), as\_datetime = true).
- Set rows from Platform.get\_all(“Attachment Queue”, filters = mapping(“modified” → tuple(“&lt;”, cutoff), “created\_document” → tuple(“is”, “set”)), pluck = “name”).
- For each name in rows.
  - Evaluate Platform.delete\_doc(“Attachment Queue”, name, delete\_permanently = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L605) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L581)

<a id="op-535672b7cade61"></a>
### Unlink deleted document

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_unlink_deleted_document`

**Inputs** doc, method = no value.

**Record and data access** read “Attachment Queue” via get\_all.

**State and service calls** request set\_value on “Attachment Queue”.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_meta(doc.doctype).get(“enable\_upload\_first\_workflow”).
  - Return no value.
- Set entries from Platform.get\_all(“Attachment Queue”, filters = mapping(“document\_type” → doc.doctype, “created\_document” → cstr(doc.name)), pluck = “name”).
- For each name in entries.
  - Evaluate Platform.db.set\_value(“Attachment Queue”, name, “created\_document”, no value).
- If entries.
  - Evaluate publish\_queue\_update(doc.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L615) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L591)

<a id="op-0b200bb60ad4fe"></a>
### Publish queue update

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_publish_queue_update`

**Inputs** document\_type.

**Declared result** no value.

**State and service calls** publish realtime with “attachment\_queue\_update”.

**Local steps**

- Evaluate Platform.publish\_realtime(“attachment\_queue\_update”, mapping(“document\_type” → document\_type), room = get\_doctype\_room(document\_type), after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“attachment\_queue\_update”, mapping(“document\_type” → document\_type), room = get\_doctype\_room(document\_type), after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L614) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L590)

<a id="op-44d2ab82a0ae05"></a>
### Get file extension

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_get_file_extension`

**Inputs** file\_url.

**Declared result** str.

**Explicit results** Path(nested operand in the contract.split(“?”, 1) at 0).suffix.lower().

**Local steps**

- Return Path(nested operand in the contract.split(“?”, 1) at 0).suffix.lower().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L587)

<a id="op-d8a4eed39d3b2c"></a>
### Has permission

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L589)

<a id="op-97618896b2bdd2"></a>
### Get permission query conditions

`operation_foundation_binding_foundation_core_doctype_attachment_queue_attachment_queue_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, no value, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L588)
