# Web content and issued documents · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Print format

[Record definition](../../../../data/record-types/print_format.json)

<a id="op-09a5bdfb3e305b"></a>
### Apply draft

`operation_foundation_printing_record_definitions_print_format_business_behavior_apply_draft`

**Inputs** name, modified, data = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on doc.

**Explicit results** doc.as\_dict().

**Local steps**

- Set doc from \_writable\_format(name, modified).
- For each tuple(field, value) in \_draft\_payload(data when data is distinct from no value, otherwise doc.draft\_data).items().
  - Value choice on data is distinct from no value — true gives data, false gives doc.draft\_data.
  - Evaluate doc.set(field, value).
- Set doc.draft\_data from no value.
- Evaluate doc.save().
- Evaluate \_record\_version(doc, “Save &amp; Apply”, mapping of field → doc.get(field) for field drawn from BUILDER\_DRAFT\_FIELDS).
  - Draw field from BUILDER\_DRAFT\_FIELDS.
- Return doc.as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L48) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1736)

<a id="op-f46ab33d7f61f6"></a>
### Record version

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_record_version`

**Inputs** doc, snapshot\_type, fields, label = no value.

**Record and data access** resolve a document from mapping(“doctype” → “Version”, “ref\_doctype” → doc.doctype, “docname” → doc.name, “data” → Platform.as\_json(mapping(“comment” → comment, VERSION\_KEY → mapping(“type” → snapshot\_type, “label” → label, “fiel … via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Version”, “ref\_doctype” → doc.doctype, “docname” → doc.name, “data” → Platform.as\_json(mapping(“comment” → comment, VERSION\_KEY → mapping(“type” → snapshot\_type, “labe ….

**Local steps**

- Set comment from translated “saved version {0}”.format(Platform.bold(label)) when label, otherwise translated “applied the editor draft”.
  - Value choice on label — true gives translated “saved version {0}”.format(Platform.bold(label)), false gives translated “applied the editor draft”.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Version”, “ref\_doctype” → doc.doctype, “docname” → doc.name, “data” → Platform.as\_json(mapping(“comment” → comment, VERSION\_KEY → mapping(nested operand in the contrac ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1673)

<a id="op-6088bb495c0937"></a>
### Save version

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_save_version`

**Inputs** name, label, data, modified.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper — translated “Give the version a name”.

**Local steps**

- Evaluate \_require\_str(name = name, label = label).
- Set doc from \_writable\_format(name, modified).
- Set label from label.strip().
- If not label.
  - Call the validation error handler Platform.throw(translated “Give the version a name”).
- Evaluate \_record\_version(doc, “Manual”, \_draft\_payload(data), label).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1677)

<a id="op-22d58c15df1f90"></a>
### Require str

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_require_str`

**Inputs** remaining named values values.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “{0} must be text”.format(key).

**Local steps**

- For each tuple(key, value) in values.items().
  - If not isinstance(value, str).
    - Call the validation error handler Platform.throw(translated “{0} must be text”.format(key), Platform.ValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1674)

<a id="op-185bc36252adb9"></a>
### Delete version

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_delete_version`

**Inputs** name, version.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request delete\_doc for “Version”.

**Local steps**

- Evaluate \_require\_str(name = name, version = version).
- Evaluate Platform.has\_permission(“Print Format”, “write”, doc = name, throw = true).
- Evaluate \_version\_snapshot(name, version).
- Evaluate Platform.delete\_doc(“Version”, version, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Print Format”, “write”, doc = name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L230) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1662)

<a id="op-a0a5c85fe11264"></a>
### Get versions

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_get_versions`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Version” via get\_all.

**Explicit results** out.

**Local steps**

- Evaluate \_require\_str(name = name).
- Evaluate Platform.has\_permission(“Print Format”, “read”, doc = name, throw = true).
- Set out from list().
- For each row in Platform.get\_all(“Version”, filters = mapping(“ref\_doctype” → “Print Format”, “docname” → name, “data” → tuple(“like”, formatted text %"{VERSION\_KEY}"%)), fields = list(“name”, “owner”, “creation”, “data”) ….
  - Set snapshot from (Platform.parse\_json(row.data) or mapping()).get(VERSION\_KEY).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(row.data) → mapping().
  - If snapshot.
    - Evaluate out.append(mapping(“name” → row.name, “owner” → row.owner, “creation” → row.creation, “type” → snapshot.get(“type”), …)).
- Return out.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Print Format”, “read”, doc = name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1665)

<a id="op-998e6ab99fa532"></a>
### Get version fields

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_get_version_fields`

**Inputs** name, version.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_version\_snapshot(name, version).get(“fields”).

**Local steps**

- Evaluate \_require\_str(name = name, version = version).
- Evaluate Platform.has\_permission(“Print Format”, “read”, doc = name, throw = true).
- Return \_version\_snapshot(name, version).get(“fields”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Print Format”, “read”, doc = name, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L232) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1664)

<a id="op-742cfc8a3e197f"></a>
### Version snapshot

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_version_snapshot`

**Inputs** name, version.

**Declared result** dict.

**Record and data access** read “Version” via get\_value.

**Explicit results** snapshot.

**Explicit failure paths** validation helper — translated “This version does not belong to {0}”.format(Platform.bold(name)).

**Local steps**

- Set row from Platform.db.get\_value(“Version”, version, list(“docname”, “data”), as\_dict = true).
- Set snapshot from (row and row.docname equals name and (Platform.parse\_json(row.data) or mapping()).get(VERSION\_KEY)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row → row.docname equals name → (Platform.parse\_json(row.data) or mapping()).get(VERSION\_KEY).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(row.data) → mapping().
- If not snapshot.
  - Call the validation error handler Platform.throw(translated “This version does not belong to {0}”.format(Platform.bold(name))).
- Return snapshot.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1702) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1678)

<a id="op-e41db4104648f2"></a>
### Restore version

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_restore_version`

**Inputs** name, version, modified.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on doc.

**Explicit results** doc.modified.

**Local steps**

- Evaluate \_require\_str(name = name, version = version).
- Set doc from \_writable\_format(name, modified).
- Set snapshot from \_version\_snapshot(name, version).
- Evaluate doc.db\_set(“draft\_data”, Platform.as\_json(\_draft\_payload(snapshot.get(“fields”)))).
- Return doc.modified.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1676)

<a id="op-bf37c04f936f2e"></a>
### Discard draft

`operation_foundation_printing_record_definitions_print_format_business_behavior_discard_draft`

**Inputs** name, modified.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on doc.

**Explicit results** doc.modified.

**Local steps**

- Set doc from \_writable\_format(name, modified).
- Evaluate doc.db\_set(“draft\_data”, no value).
- Return doc.modified.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L2777) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1739)

<a id="op-eb501f57163d51"></a>
### Make default

`operation_foundation_printing_record_definitions_print_format_business_behavior_make_default`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Print Format” via get\_doc · resolve a document from “DocType” via get\_doc.

**State and service calls** call save on doctype · msgprint with Platform.\_(“{0} is now default print format for {1} doctype”).format(Platform.bold(name), Platform.bold(print\_format.doc\_type)).

**Local steps**

- Set print\_format from Platform.get\_doc(“Print Format”, name).
- Evaluate print\_format.check\_permission(“write”).
- Set doctype from Platform.get\_doc(“DocType”, print\_format.doc\_type).
- If doctype.custom.
  - Set doctype.default\_print\_format from name.
  - Evaluate doctype.save().
- Otherwise.
  - Evaluate Platform.make\_property\_setter(mapping(“doctype\_or\_field” → “DocType”, “doctype” → print\_format.doc\_type, “property” → “default\_print\_format”, “value” → name)).
- Evaluate Platform.msgprint(Platform.\_(“{0} is now default print format for {1} doctype”).format(Platform.bold(name), Platform.bold(print\_format.doc\_type))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from print\_format.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L2927) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1742)

<a id="op-c97684efa182b5"></a>
### Printable sample

`operation_foundation_printing_record_definitions_print_format_business_behavior_printable_sample`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Record and data access** read doctype via get\_list.

**Explicit results** sample at 0 when sample, otherwise no value.

**Local steps**

- Set filters from mapping(“docstatus” → 1) when Platform.get\_meta(doctype).is\_submittable, otherwise mapping().
  - Value choice on Platform.get\_meta(doctype).is\_submittable — true gives mapping(“docstatus” → 1), false gives mapping().
- Set sample from Platform.get\_list(doctype, filters = filters, limit = 1, order\_by = “modified desc”, pluck = “name”).
- Return sample at 0 when sample, otherwise no value.
  - Value choice on sample — true gives sample at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0315.json#L3332) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1757)

<a id="op-cd4eee6746fad5"></a>
### Generate preview

`operation_foundation_binding_foundation_printing_doctype_print_format_print_format_generate_preview`

**Inputs** name.

**Declared result** (str bitwise or no value).

**Record and data access** resolve a document from “Print Format” via get\_doc · read “File” via get\_value.

**State and service calls** request delete\_doc for “File” · call db\_set on doc.

**Explicit results** no value · file.file\_url.

**Local steps**

- Set doc from Platform.get\_doc(“Print Format”, name).
- Set sample\_name from printable\_sample(doc.doc\_type).
- If not sample\_name.
  - Return no value.
- Bind dependencies save\_file.
- Bind dependencies get\_preview\_from\_html.
- Attempt the following.
  - Set html from Platform.get\_print(doc.doc\_type, sample\_name, name).
  - Set image from get\_preview\_from\_html(html, format = “webp”, width = 850).
- On failure (Exception).
  - Set Platform.local.message\_log from list().
  - Evaluate Platform.log\_error(formatted text Print format preview generation failed: {name}).
  - Return no value.
- If doc.preview\_image.
  - Set old from Platform.db.get\_value(“File”, mapping(“file\_url” → doc.preview\_image, “attached\_to\_doctype” → “Print Format”, “attached\_to\_name” → name), “name”).
  - If old.
    - Evaluate Platform.delete\_doc(“File”, old, ignore\_permissions = true, delete\_permanently = true).
- Set fname from formatted text pf-preview-{Platform.generate\_hash(length = 10)}.webp.
- Set file from save\_file(fname, image, “Print Format”, name, is\_private = 1).
- Evaluate doc.db\_set(“preview\_image”, file.file\_url, update\_modified = false).
- Return file.file\_url.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 10).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L231) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1663)

## Workspace · Print format builder beta

<a id="op-5bb23321fd923a"></a>
### Get google fonts

`operation_foundation_binding_foundation_printing_page_print_format_builder_beta_print_format_builder_beta_get_google_fonts`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_google\_fonts().

**Local steps**

- Return \_get\_google\_fonts().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1687)

<a id="op-5446f9967dbf76"></a>
### Get google fonts

`operation_foundation_binding_foundation_printing_page_print_format_builder_beta_print_format_builder_beta_get_google_fonts_0e1270d0f1e3`

**Inputs** no declared parameters.

**Wrappers, in declaration order** functools.lru\_cache.

**Explicit results** Platform.parse\_json(Platform.read\_file(file\_path)).

**Local steps**

- Set file\_path from Platform.get\_app\_path(“Platform”, “data”, “google\_fonts.json”).
- Return Platform.parse\_json(Platform.read\_file(file\_path)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L25) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1688)

## Record · Print format field template

[Record definition](../../../../data/record-types/print_format_field_template.json)

<a id="op-3860b57c65bbab"></a>
### Print Format Field Template.validate

`operation_foundation_printing_record_definitions_print_format_field_template_business_behavior_print_format_field_template_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enable developer mode to create a standard Print Template” · validation helper — translated “Module is required for a standard Print Template”.

**Local steps**

- If self.standard.
  - If (not Platform.conf.developer\_mode and not Platform.flags.in\_patch).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.flags.in\_patch.
    - Call the validation error handler Platform.throw(translated “Enable developer mode to create a standard Print Template”).
  - If not self.module.
    - Call the validation error handler Platform.throw(translated “Module is required for a standard Print Template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L407) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1778)

<a id="op-6d531413e5614f"></a>
### Print Format Field Template.before insert

`operation_foundation_printing_record_definitions_print_format_field_template_business_behavior_print_format_field_template_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate](operations-010.md#op-3e361d8630fdcc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L590) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1775)

<a id="op-92a67801523a73"></a>
### Print Format Field Template.on update

`operation_foundation_printing_record_definitions_print_format_field_template_business_behavior_print_format_field_template_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate().
- Evaluate self.export\_doc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate](operations-010.md#op-3e361d8630fdcc), [export doc](operations-010.md#op-2f43961a904b3c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L641) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1777)

<a id="op-3e361d8630fdcc"></a>
### Print Format Field Template.validate duplicate

`operation_foundation_printing_record_definitions_print_format_field_template_business_behavior_print_format_field_template_validate_duplicate`

**Inputs** self.

**Record and data access** read “Print Format Field Template” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “A template already exists for field {0} of {1}”.format(Platform.bold(self.field), Platform.bold(self.document\_type)).

**Local steps**

- If not self.standard.
  - Return no value.
- If (not self.field or not self.document\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.field → not self.document\_type.
  - Return no value.
- Set filters from mapping(“document\_type” → self.document\_type, “field” → self.field).
- If not self.is\_new().
  - Evaluate filters.update(mapping(“name” → tuple(“!=”, self.name))).
- Set result from Platform.get\_all(“Print Format Field Template”, filters = filters, limit = 1).
- If result.
  - Call the validation error handler Platform.throw(translated “A template already exists for field {0} of {1}”.format(Platform.bold(self.field), Platform.bold(self.document\_type)), Platform.DuplicateEntryError, title = translated “Duplicate Entry”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L712) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1779)

<a id="op-2f43961a904b3c"></a>
### Print Format Field Template.export doc

`operation_foundation_printing_record_definitions_print_format_field_template_business_behavior_print_format_field_template_export_record`

**Inputs** self.

**Local steps**

- Bind dependencies export\_module\_json.
- Evaluate export\_module\_json(self, self.standard, self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L1143) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1776)

## Record · Print format snippet

[Record definition](../../../../data/record-types/print_format_snippet.json)

<a id="op-04291be848965f"></a>
### Print Format Snippet.validate

`operation_foundation_printing_record_definitions_print_format_snippet_business_behavior_print_format_snippet_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Enable developer mode to create a standard Print Format Snippet” · validation helper — translated “Module is required for a standard Print Format Snippet”.

**Local steps**

- Evaluate self.validate\_content().
- If self.standard.
  - If (not Platform.conf.developer\_mode and not Platform.flags.in\_patch).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.flags.in\_patch.
    - Call the validation error handler Platform.throw(translated “Enable developer mode to create a standard Print Format Snippet”).
  - If not self.module.
    - Call the validation error handler Platform.throw(translated “Module is required for a standard Print Format Snippet”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate content](operations-010.md#op-52b3f34d56bd12).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L1219) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1783)

<a id="op-52b3f34d56bd12"></a>
### Print Format Snippet.validate content

`operation_foundation_printing_record_definitions_print_format_snippet_business_behavior_print_format_snippet_validate_content`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Content must be valid JSON” · validation helper — translated “Content must be a JSON object”.

**Local steps**

- If not self.content.
  - Return no value.
- Attempt the following.
  - Set content from json.loads(self.content).
- On failure (tuple(TypeError, ValueError)).
  - Call the validation error handler Platform.throw(translated “Content must be valid JSON”, title = translated “Invalid Snippet”).
- If not isinstance(content, dict).
  - Call the validation error handler Platform.throw(translated “Content must be a JSON object”, title = translated “Invalid Snippet”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L1422) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1784)

<a id="op-d233e30333bb80"></a>
### Print Format Snippet.on update

`operation_foundation_printing_record_definitions_print_format_snippet_business_behavior_print_format_snippet_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.export\_doc().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export doc](operations-010.md#op-a70b0e38cf6937).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L1694) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1782)

<a id="op-a70b0e38cf6937"></a>
### Print Format Snippet.export doc

`operation_foundation_printing_record_definitions_print_format_snippet_business_behavior_print_format_snippet_export_record`

**Inputs** self.

**Local steps**

- Bind dependencies export\_module\_json.
- Evaluate export\_module\_json(self, self.standard, self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0318.json#L1745) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1781)
