# Forms, reports and navigation · operations 38

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · List filter

[Record definition](../../../../data/record-types/list_filter.json)

<a id="op-870a8ed1e4d24b"></a>
### List Filter.was standard

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_was_standard`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool((before and before.is\_standard)).

**Local steps**

- Set before from self.get\_doc\_before\_save().
- Return bool((before and before.is\_standard)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → before.is\_standard.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L262) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L720)

<a id="op-3262c78dcb0e95"></a>
### List Filter.before save

`operation_foundation_desk_record_definitions_list_filter_business_behavior_list_filter_before_save`

**Inputs** self.

**Local steps**

- If self.filter\_name.
  - Set self.filter\_name from \_clean\_filter\_name(self.filter\_name).
- If self.reference\_doctype.
  - Set valid\_fields from \_get\_valid\_filter\_fields(self.reference\_doctype).
  - If self.filters.
    - Set parsed\_filters from Platform.parse\_json(self.filters).
    - Set self.filters from json.dumps(\_sanitize\_filters(parsed\_filters, valid\_fields, self.reference\_doctype)).
  - If self.columns.
    - Set parsed\_columns from Platform.parse\_json(self.columns).
    - Set self.columns from json.dumps(\_sanitize\_columns(parsed\_columns, valid\_fields)).
  - Set tuple(self.sort\_field, self.sort\_order) from \_sanitize\_sorting(self.sort\_field, self.sort\_order, valid\_fields).
- Set self.route\_signature from compute\_route\_signature(self.reference\_doctype, self.filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L14) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L845)

<a id="op-86d15f486b8e59"></a>
### List Filter.on update

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_on_update`

**Inputs** self.

**Local steps**

- If (self.is\_standard and Platform.conf.developer\_mode and not Platform.flags.in\_import).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → Platform.conf.developer\_mode → not Platform.flags.in\_import.
  - Evaluate self.export\_layout().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export layout](operations-038.md#op-c3759a99c9ef1a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L260) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L718)

<a id="op-3f1a1d51bce00d"></a>
### List Filter.on trash

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_on_trash`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to delete this layout” · validation helper with Platform.PermissionError — translated “Standard list layouts can only be deleted in developer mode”.

**Local steps**

- If Platform.flags.in\_migrate.
  - Return no value.
- If not \_can\_update\_list\_filter(self).
  - Call the validation error handler Platform.throw(translated “You are not allowed to delete this layout”, Platform.PermissionError).
- If not self.is\_standard.
  - Return no value.
- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Standard list layouts can only be deleted in developer mode”, Platform.PermissionError).
- Set path from self.get\_export\_path().
- If os.path.exists(path).
  - Evaluate os.remove(path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export path](operations-038.md#op-c948d38aba7976).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L259) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L717)

<a id="op-c948d38aba7976"></a>
### List Filter.get export path

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_get_export_path`

**Inputs** self.

**Declared result** str.

**Explicit results** os.path.join(get\_module\_path(self.module), “doctype”, Platform.scrub(self.reference\_doctype), “list\_filter”, …).

**Local steps**

- Return os.path.join(get\_module\_path(self.module), “doctype”, Platform.scrub(self.reference\_doctype), “list\_filter”, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L258) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L716)

<a id="op-c3759a99c9ef1a"></a>
### List Filter.export layout

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_export_layout`

**Inputs** self.

**Local steps**

- Set path from self.get\_export\_path().
- Evaluate Platform.create\_folder(os.path.dirname(path)).
- Within open(path, “w+”) bound as f.
  - Evaluate f.write((Platform.as\_json(self.as\_dict(no\_nulls = true, no\_private\_properties = true)) + whitespace '\\n')).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export path](operations-038.md#op-c948d38aba7976).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L257) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L715)

<a id="op-fec91e56a74b3a"></a>
### Clean filter name

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_clean_filter_name`

**Inputs** filter\_name.

**Declared result** str.

**Explicit results** strip\_html(cstr(filter\_name)).strip().

**Local steps**

- Return strip\_html(cstr(filter\_name)).strip().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L254) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L712)

<a id="op-2f0f4d83e6156c"></a>
### Compute route signature

`operation_foundation_desk_record_definitions_list_filter_business_behavior_compute_route_signature`

**Inputs** reference\_doctype, filters.

**Declared result** str.

**Explicit results** empty text · “&amp;”.join(generator of formatted text {key}={value} for tuple(key, value) drawn from params).

**Local steps**

- If isinstance(filters, str).
  - Set filters from (Platform.parse\_json(filters) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(filters) → list().
- If (not isinstance(filters, list) or not reference\_doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(filters, list) → not reference\_doctype.
  - Return empty text.
- Set params from list().
- For each row in filters.
  - If (not isinstance(row, tuple(list, tuple)) or len(row) &lt; 4).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(row, tuple(list, tuple)) → len(row) &lt; 4.
    - Continue with the next iteration or loop test.
  - Set tuple(doctype, field, operator, value) from tuple(row at 0, row at 1, row at 2, row at 3).
  - Set query\_key from cstr(field) when doctype equals reference\_doctype, otherwise formatted text {doctype}.{field}.
    - Value choice on doctype equals reference\_doctype — true gives cstr(field), false gives formatted text {doctype}.{field}.
  - If operator equals “=”.
    - Set query\_value from cstr(value).
  - Otherwise.
    - Set query\_value from json.dumps(list(operator, value), separators = tuple(“,”, “:”)).
  - Evaluate params.append(tuple(query\_key, query\_value)).
- Evaluate params.sort(key = deferred anonymous expression).
- Return “&amp;”.join(generator of formatted text {key}={value} for tuple(key, value) drawn from params).
  - Draw tuple(key, value) from params.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0175.json#L5750) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L841)

<a id="op-47605bbe410ed2"></a>
### Can edit global filter

`operation_foundation_desk_record_definitions_list_filter_business_behavior_can_edit_global_filter`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** (Platform.session.user equals “Administrator” or “System Manager” belongs to Platform.get\_roles()).

**Local steps**

- Return (Platform.session.user equals “Administrator” or “System Manager” belongs to Platform.get\_roles()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.session.user equals “Administrator” → “System Manager” belongs to Platform.get\_roles().

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0175.json#L6452) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L381) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L839)

<a id="op-8d6a376ecd0745"></a>
### Can update list filter

`operation_foundation_desk_record_definitions_list_filter_business_behavior_can_update_list_filter`

**Inputs** doc.

**Declared result** bool.

**Explicit results** \_can\_edit\_global\_filter() · doc.for\_user equals Platform.session.user.

**Local steps**

- If not doc.for\_user.
  - Return \_can\_edit\_global\_filter().
- Return doc.for\_user equals Platform.session.user.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0175.json#L6539) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L840)

<a id="op-1afee6f557a1b5"></a>
### Get valid filter fields

`operation_foundation_desk_record_definitions_list_filter_business_behavior_get_valid_filter_fields`

**Inputs** reference\_doctype.

**Declared result** set at str.

**Explicit results** valid\_fields.

**Local steps**

- Set meta from Platform.get\_meta(reference\_doctype).
- Set valid\_fields from set of field at “fieldname” for field drawn from std\_fields.
  - Draw field from std\_fields.
- Evaluate valid\_fields.add(“status\_field”).
- Evaluate valid\_fields.update(generator of df.fieldname for df drawn from meta.fields).
  - Draw df from meta.fields.
- Return valid\_fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0175.json#L6642) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L844)

<a id="op-271a2b891db72e"></a>
### Sanitize filters

`operation_foundation_desk_record_definitions_list_filter_business_behavior_sanitize_filters`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** filters, valid\_fields, reference\_doctype.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L16) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L848)

<a id="op-04ebaca9daa831"></a>
### Sanitize columns

`operation_foundation_desk_record_definitions_list_filter_business_behavior_sanitize_columns`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** columns, valid\_fields.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0175.json#L7044) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L847)

<a id="op-abad0fdd7a2350"></a>
### Sanitize sorting

`operation_foundation_desk_record_definitions_list_filter_business_behavior_sanitize_sorting`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** sort\_field, sort\_order, valid\_fields.

**Explicit result forms** a structured result.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0175.json#L7304) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L849)

<a id="op-8f9470f21244b3"></a>
### Update list filter

`operation_foundation_desk_record_definitions_list_filter_business_behavior_update_list_filter`

**Inputs** name, filter\_name = no value, for\_user = no value, filters = no value, columns = no value, sort\_field = no value, sort\_order = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “List Filter” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** doc.as\_dict().

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to update global layouts” · validation helper with Platform.PermissionError — translated “You are not allowed to update this layout” · validation helper with Platform.PermissionError — translated “You are not allowed to assign layouts to other users”.

**Local steps**

- Set doc from Platform.get\_doc(“List Filter”, name).
- If not \_can\_update\_list\_filter(doc).
  - If not doc.for\_user.
    - Call the validation error handler Platform.throw(translated “You are not allowed to update global layouts”, Platform.PermissionError).
  - Call the validation error handler Platform.throw(translated “You are not allowed to update this layout”, Platform.PermissionError).
- If filter\_name is distinct from no value.
  - Set doc.filter\_name from cstr(filter\_name).strip().
- If for\_user is distinct from no value.
  - Set next\_for\_user from cstr(for\_user).
  - If (not next\_for\_user and not \_can\_edit\_global\_filter()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not next\_for\_user → not \_can\_edit\_global\_filter().
    - Call the validation error handler Platform.throw(translated “You are not allowed to update global layouts”, Platform.PermissionError).
  - If (next\_for\_user and next\_for\_user differs from Platform.session.user and not \_can\_edit\_global\_filter()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in next\_for\_user → next\_for\_user differs from Platform.session.user → not \_can\_edit\_global\_filter().
    - Call the validation error handler Platform.throw(translated “You are not allowed to assign layouts to other users”, Platform.PermissionError).
  - Set doc.for\_user from next\_for\_user.
- If filters is distinct from no value.
  - Set doc.filters from json.dumps((Platform.parse\_json(filters) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(filters) → list().
- If columns is distinct from no value.
  - Set doc.columns from json.dumps((Platform.parse\_json(columns) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(columns) → list().
- If sort\_field is distinct from no value.
  - Set doc.sort\_field from sort\_field.
- If sort\_order is distinct from no value.
  - Set doc.sort\_order from sort\_order.
- Evaluate doc.save(ignore\_permissions = true).
- Return doc.as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0176.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L850)

<a id="op-c7f62386ad774b"></a>
### Delete list filter

`operation_foundation_desk_record_definitions_list_filter_business_behavior_delete_list_filter`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “List Filter” via get\_doc.

**Explicit results** true.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to delete global layouts” · validation helper with Platform.PermissionError — translated “You are not allowed to delete this layout”.

**Local steps**

- Set doc from Platform.get\_doc(“List Filter”, name).
- If not \_can\_update\_list\_filter(doc).
  - If not doc.for\_user.
    - Call the validation error handler Platform.throw(translated “You are not allowed to delete global layouts”, Platform.PermissionError).
  - Call the validation error handler Platform.throw(translated “You are not allowed to delete this layout”, Platform.PermissionError).
- Evaluate doc.delete(ignore\_permissions = true).
- Return true.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0176.json#L985) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L842)

<a id="op-9498733b79be52"></a>
### Update list layout

`operation_foundation_desk_record_definitions_list_filter_business_behavior_update_list_layout`

**Inputs** name, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** update\_list\_filter(name, expanded names kwargs).

**Local steps**

- If (“layout\_name” belongs to kwargs and “filter\_name” does not belong to kwargs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “layout\_name” belongs to kwargs → “filter\_name” does not belong to kwargs.
  - Set kwargs at “filter\_name” from kwargs.pop(“layout\_name”).
- Return update\_list\_filter(name, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0176.json#L1251) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L851)

<a id="op-a8faff29bf6aa0"></a>
### Delete list layout

`operation_foundation_desk_record_definitions_list_filter_business_behavior_delete_list_layout`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** delete\_list\_filter(name).

**Local steps**

- Return delete\_list\_filter(name).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0176.json#L1431) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L385) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L843)

## Record · List view settings

[Record definition](../../../../data/record-types/list_view_settings.json)

<a id="op-b70d503a4fa60c"></a>
### Save listview settings

`operation_foundation_desk_record_definitions_list_view_settings_business_behavior_save_listview_settings`

**Inputs** doctype, listview\_settings, removed\_listview\_fields.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “List View Settings” via get\_all · resolve a document from “List View Settings” via get\_doc.

**State and service calls** call save on doc · request new\_doc for “List View Settings” · call insert on doc.

**Explicit results** mapping(“meta” → Platform.get\_meta(doctype, false), “listview\_settings” → doc).

**Local steps**

- Set listview\_settings from Platform.parse\_json(listview\_settings).
- Set removed\_listview\_fields from Platform.parse\_json(removed\_listview\_fields).
- If Platform.get\_all(“List View Settings”, filters = mapping(“name” → doctype)).
  - Set doc from Platform.get\_doc(“List View Settings”, doctype).
  - Evaluate doc.update(listview\_settings).
  - Evaluate doc.save().
- Otherwise.
  - Set doc from Platform.new\_doc(“List View Settings”).
  - Set doc.name from doctype.
  - Evaluate doc.update(listview\_settings).
  - Evaluate doc.insert().
- Evaluate set\_listview\_fields(doctype, listview\_settings.get(“fields”), removed\_listview\_fields).
- Return mapping(“meta” → Platform.get\_meta(doctype, false), “listview\_settings” → doc).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0176.json#L5884) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L871)

<a id="op-0b999fb43f0d34"></a>
### Set listview fields

`operation_foundation_desk_record_definitions_list_view_settings_business_behavior_set_listview_fields`

**Inputs** doctype, listview\_fields, removed\_listview\_fields.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set listview\_fields from list of f.get(“fieldname”) for f drawn from Platform.parse\_json(listview\_fields) where f.get(“fieldname”).
  - Draw f from Platform.parse\_json(listview\_fields), keep a combination only if (f.get(“fieldname”)).
- For each field in removed\_listview\_fields.
  - Evaluate set\_in\_list\_view\_property(doctype, meta.get\_field(field), “0”).
- For each field in listview\_fields.
  - Evaluate set\_in\_list\_view\_property(doctype, meta.get\_field(field), “1”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0176.json#L6398) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L873)

<a id="op-cab1448ae89cc1"></a>
### Set in list view property

`operation_foundation_desk_record_definitions_list_view_settings_business_behavior_set_in_list_view_property`

**Inputs** doctype, field, value.

**Record and data access** read “Property Setter” via get\_value · resolve a document from “Property Setter” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- If (not field or field.fieldname equals “status\_field”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not field → field.fieldname equals “status\_field”.
  - Return no value.
- Set property\_setter from Platform.db.get\_value(“Property Setter”, mapping(“doc\_type” → doctype, “field\_name” → field.fieldname, “property” → “in\_list\_view”)).
- If property\_setter.
  - Set doc from Platform.get\_doc(“Property Setter”, property\_setter).
  - Set doc.value from value.
  - Evaluate doc.save().
- Otherwise.
  - Evaluate Platform.make\_property\_setter(mapping(“doctype” → doctype, “doctype\_or\_field” → “DocField”, “fieldname” → field.fieldname, “property” → “in\_list\_view”, …), ignore\_validate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0176.json#L6684) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L872)

<a id="op-7456097315ff61"></a>
### Get default listview fields

`operation_foundation_desk_record_definitions_list_view_settings_business_behavior_get_default_listview_fields`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** fields.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set path from Platform.get\_module\_path(Platform.scrub(meta.module), “doctype”, Platform.scrub(meta.name), (Platform.scrub(meta.name) + “.json”)).
- Set doctype\_json from Platform.get\_file\_json(path).
- Set fields from list of f.get(“fieldname”) for f drawn from doctype\_json.get(“fields”) where f.get(“in\_list\_view”).
  - Draw f from doctype\_json.get(“fields”), keep a combination only if (f.get(“in\_list\_view”)).
- If meta.title\_field.
  - If meta.title\_field.strip() does not belong to fields.
    - Evaluate fields.append(meta.title\_field.strip()).
- Return fields.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L870)

## Service · Listview

<a id="op-921b2f046d9419"></a>
### Get list settings

`operation_foundation_desk_listview_business_behavior_get_list_settings`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “List View Settings” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“List View Settings”, doctype).

**Local steps**

- Attempt the following.
  - Return Platform.get\_cached\_doc(“List View Settings”, doctype).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_messages().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“List View Settings”, doctype).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L3367) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L299)

<a id="op-0ff07a98bcf9d4"></a>
### Set list settings

`operation_foundation_desk_listview_business_behavior_set_list_settings`

**Inputs** doctype, values.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “List View Settings” via get\_doc.

**State and service calls** request new\_doc for “List View Settings” · call save on doc.

**Local steps**

- Attempt the following.
  - Set doc from Platform.get\_doc(“List View Settings”, doctype).
- On failure (Platform.DoesNotExistError).
  - Set doc from Platform.new\_doc(“List View Settings”).
  - Set doc.name from doctype.
  - Evaluate Platform.clear\_messages().
- Evaluate doc.update(Platform.parse\_json(values)).
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0205.json#L3498) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L300)
