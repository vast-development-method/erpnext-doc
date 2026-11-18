# Record lifecycle and persistence · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Audit trail

[Record definition](../../../../data/record-types/audit_trail.json)

<a id="op-728eb87837b68b"></a>
### Audit Trail.validate

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_fields().
- Evaluate self.validate\_document().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate fields](operations-002.md#op-95ae582f410ad2), [validate document](operations-002.md#op-ccba3a69ee2366).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L3552) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L952)

<a id="op-95ae582f410ad2"></a>
### Audit Trail.validate fields

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_validate_fields`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{} field cannot be empty.”.format(Platform.bold(field)).

**Local steps**

- Set fields\_dict from mapping(“DocType” → self.doctype\_name, “Document” → self.document).
- For each field in fields\_dict.
  - If not fields\_dict at field.
    - Call the validation error handler Platform.throw(translated “{} field cannot be empty.”.format(Platform.bold(field))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L3623) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L954)

<a id="op-ccba3a69ee2366"></a>
### Audit Trail.validate document

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_validate_document`

**Inputs** self.

**Record and data access** read self.doctype\_name via exists.

**Explicit failure paths** validation helper — translated “The selected document {0} is not a {1}.”.format(Platform.bold(self.document), Platform.bold(self.doctype\_name)).

**Local steps**

- If not Platform.db.exists(self.doctype\_name, self.document).
  - Call the validation error handler Platform.throw(translated “The selected document {0} is not a {1}.”.format(Platform.bold(self.document), Platform.bold(self.doctype\_name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L3813) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L953)

<a id="op-1eecc2303f5c1d"></a>
### Audit Trail.compare document

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_compare_document`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from self.doctype\_name via get\_doc.

**Explicit results** tuple(amended\_document\_names, mapping(“changed” → self.changed, “row\_changed” → self.row\_changed, “added” → self.added, “removed” → self.removed)).

**Local steps**

- Evaluate self.validate().
- Set amended\_document\_names from self.get\_amended\_documents().
- Set self.amended\_docs from list of Platform.get\_doc(self.doctype\_name, name) for name drawn from amended\_document\_names.
  - Draw name from amended\_document\_names.
- Set self.docs\_to\_compare from len(self.amended\_docs).
- Set tuple(self.changed, self.row\_changed, self.added, self.removed) from tuple(mapping(), mapping(), mapping(), mapping()).
- For each i in range(1, self.docs\_to\_compare).
  - Set diff from get\_diff(self.amended\_docs at (i − 1), self.amended\_docs at i, compare\_cancelled = true).
  - Evaluate self.get\_diff\_grid(i, diff).
  - Evaluate self.get\_rows\_added\_removed\_grid(i, diff, “added”, self.added).
  - Evaluate self.get\_rows\_added\_removed\_grid(i, diff, “removed”, self.removed).
  - Evaluate self.get\_rows\_updated\_grid(i, diff).
- Return tuple(amended\_document\_names, mapping(“changed” → self.changed, “row\_changed” → self.row\_changed, “added” → self.added, “removed” → self.removed)).

**Methods declared on this owner** [validate](operations-002.md#op-728eb87837b68b), [get amended documents](operations-002.md#op-e39c16ef967145), [get diff grid](operations-002.md#op-72b961cfe1a5af), [get rows added removed grid](operations-002.md#op-31d20eee31f21b), [get rows updated grid](operations-002.md#op-f28ad2091515d4).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L3993) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L947)

<a id="op-e39c16ef967145"></a>
### Audit Trail.get amended documents

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_get_amended_documents`

**Inputs** self.

**Record and data access** read self.doctype\_name via get\_value.

**Explicit results** amended\_document\_names.

**Local steps**

- Set start\_date from self.get(“start\_date”).
- Set amended\_document\_names from list().
- Set curr\_doc from self.document.
- Set creation from Platform.db.get\_value(self.doctype\_name, self.document, “creation”).
- While (curr\_doc and len(amended\_document\_names) &lt; 5 and (start\_date is identical to no value or compare(creation, “&gt;=”, start\_date, “Date”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in curr\_doc → len(amended\_document\_names) &lt; 5 → (start\_date is identical to no value or compare(creation, “&gt;=”, start\_date, “Date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in start\_date is identical to no value → compare(creation, “&gt;=”, start\_date, “Date”).
  - Evaluate amended\_document\_names.append(curr\_doc).
  - Set curr\_doc from Platform.db.get\_value(self.doctype\_name, curr\_doc, “amended\_from”).
  - Set creation from Platform.db.get\_value(self.doctype\_name, curr\_doc, “creation”).
- Set amended\_document\_names from amended\_document\_names at slice no value to no value with step negative 1.
- Return amended\_document\_names.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L4577) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L948)

<a id="op-72b961cfe1a5af"></a>
### Audit Trail.get diff grid

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_get_diff_grid`

**Inputs** self, i, diff.

**Local steps**

- For each change in diff.changed.
  - Set fieldname from get\_field\_label(change at 0, doctype = self.doctype\_name).
  - Set value from change at negative 1.
  - Set value\_list from (list(empty text) × self.docs\_to\_compare).
  - Evaluate self.changed.setdefault(fieldname, value\_list).
  - Set self.changed at fieldname at i from (value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.
  - If i equals 1.
    - Set value from change at 1.
    - Set self.changed at fieldname at (i − 1) from (value or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L4983) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L949)

<a id="op-31d20eee31f21b"></a>
### Audit Trail.get rows added removed grid

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_get_rows_added_removed_grid`

**Inputs** self, i, diff, key, changed\_dict.

**Local steps**

- Set doc\_name from self.amended\_docs at i.name.
- Set changed\_dict at doc\_name from mapping().
- For each change in diff at key.
  - Set tablename from get\_field\_label(change at 0, doctype = self.doctype\_name).
  - Set value\_dict from filter\_fields\_for\_gridview(change at negative 1).
  - Evaluate changed\_dict at doc\_name.setdefault(tablename, list()).append(value\_dict).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L5314) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L950)

<a id="op-f28ad2091515d4"></a>
### Audit Trail.get rows updated grid

`operation_foundation_core_record_definitions_audit_trail_business_behavior_audit_trail_get_rows_updated_grid`

**Inputs** self, i, diff.

**Local steps**

- For each change in diff.row\_changed.
  - Set table\_name from get\_field\_label(change at 0, doctype = self.doctype\_name).
  - Set index from change at 1.
  - Evaluate self.row\_changed.setdefault(table\_name, mapping()).setdefault(index, mapping()).
  - For each field in change at negative 1.
    - Set fieldname from get\_field\_label(field at 0, doctype = self.doctype\_name, child\_field = change at 0).
    - Set value from field at negative 1.
    - Set value\_list from (list(empty text) × self.docs\_to\_compare).
    - Evaluate self.row\_changed at table\_name at index.setdefault(fieldname, value\_list).
    - Set self.row\_changed at table\_name at index at fieldname at i from (value or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.
    - If i equals 1.
      - Set value from field at 1.
      - Set self.row\_changed at table\_name at index at fieldname at (i − 1) from (value or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L5583) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L951)

<a id="op-3860b06836a39c"></a>
### Get field label

`operation_foundation_core_record_definitions_audit_trail_business_behavior_get_field_label`

**Inputs** fieldname, doctype, child\_field = no value.

**Explicit results** label · fieldname.

**Local steps**

- If child\_field.
  - Set meta from Platform.get\_meta(doctype).
  - For each field in meta.fields.
    - If field.fieldname equals child\_field.
      - Set doctype from field.options.
- Set meta from Platform.get\_meta(doctype).
- Set label from meta.get\_label(fieldname).
- If label does not belong to list(“No Label”, no value, empty text).
  - Return label.
- Return fieldname.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L6117) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L956)

<a id="op-ad6631b598049c"></a>
### Filter fields for gridview

`operation_foundation_core_record_definitions_audit_trail_business_behavior_filter_fields_for_gridview`

**Inputs** row.

**Explicit results** grid\_row.

**Local steps**

- Set grid\_row from mapping().
- Set meta from Platform.get\_meta(row.doctype).
- For each field in meta.fields.
  - If field.in\_list\_view equals 1.
    - Set fieldlabel from get\_field\_label(field.fieldname, row.doctype).
    - Set grid\_row at fieldlabel from (row at field.fieldname or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at field.fieldname → empty text.
- Return grid\_row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0038.json#L6371) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L955)

## Service · Builder

<a id="op-3869dee0dfd265"></a>
### Flatten

`operation_foundation_query_builder_builder_business_behavior_flatten`

**Inputs** module.

**Explicit results** new\_mod.

**Local steps**

- Bind dependencies inspect.
- Bind dependencies \_dict.
- Set new\_mod from \_dict().
- For each tuple(name, obj) in inspect.getmembers(module, deferred anonymous expression).
  - If not name.startswith(“\_”).
    - Set new\_mod at name from obj.
- Return new\_mod.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L745) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L128)

<a id="op-7e83d5c5482c16"></a>
### Base.functions

`operation_foundation_query_builder_builder_business_behavior_base_functions`

**Inputs** name, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Declared result** Function.

**Explicit results** Function(name, expanded args, expanded names kwargs).

**Local steps**

- Return Function(name, expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L949) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L123)

<a id="op-d5b0a5e84f63a2"></a>
### Base.Doc Type

`operation_foundation_query_builder_builder_business_behavior_base_record_type`

**Inputs** table\_name, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Declared result** Table.

**Explicit results** Table(table\_name, expanded args, expanded names kwargs).

**Local steps**

- Evaluate Base.validate\_doctype(table\_name).
- Set table\_name from get\_table\_name(table\_name).
- Return Table(table\_name, expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L1037) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L125)

<a id="op-42824904ca639a"></a>
### Base.into

`operation_foundation_query_builder_builder_business_behavior_base_into`

**Inputs** cls, table, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Declared result** QueryBuilder.

**Explicit results** super().into(table, expanded args, expanded names kwargs).

**Local steps**

- If isinstance(table, str).
  - Set table from cls.DocType(table).
- Return super().into(table, expanded args, expanded names kwargs).

**Methods declared on this owner** [Doc Type](operations-002.md#op-d5b0a5e84f63a2).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L1178) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L124)

<a id="op-445655bfa9bfbf"></a>
### Base.update

`operation_foundation_query_builder_builder_business_behavior_base_update`

**Inputs** cls, table, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Declared result** QueryBuilder.

**Explicit results** super().update(table, expanded args, expanded names kwargs).

**Local steps**

- If isinstance(table, str).
  - Set table from cls.DocType(table).
- Return super().update(table, expanded args, expanded names kwargs).

**Methods declared on this owner** [Doc Type](operations-002.md#op-d5b0a5e84f63a2).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L1337) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L126)

<a id="op-cb0f7b598c382c"></a>
### Base.validate doctype

`operation_foundation_query_builder_builder_business_behavior_base_validate_record_type`

**Inputs** doctype.

**Wrappers, in declaration order** staticmethod.

**Declared result** no value.

**Local steps**

- Bind dependencies \_, throw.
- If not TABLE\_NAME\_PATTERN.match(doctype).
  - Evaluate throw(translated “Invalid DocType: {0}”.format(doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L1496) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1425) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L127)

<a id="op-f245b1b0b3c959"></a>
### Maria DB.builder

`operation_foundation_query_builder_builder_business_behavior_maria_database_builder`

**Inputs** cls, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Declared result** “MySQLQueryBuilder”.

**Explicit results** super().\_builder(expanded args, wrapper\_cls = ParameterizedValueWrapper, expanded names kwargs).

**Local steps**

- Return super().\_builder(expanded args, wrapper\_cls = ParameterizedValueWrapper, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L87) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L129)

<a id="op-e31abf7f275339"></a>
### Maria DB.from

`operation_foundation_query_builder_builder_business_behavior_maria_database_from`

**Inputs** cls, table, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Explicit results** super().from\_(table, expanded args, expanded names kwargs).

**Local steps**

- If isinstance(table, str).
  - Set table from cls.DocType(table).
- Return super().from\_(table, expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L2028) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L130)

<a id="op-38a86108ba72f3"></a>
### Postgres.builder

`operation_foundation_query_builder_builder_business_behavior_relational_database_builder`

**Inputs** cls, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Declared result** “PostgreSQLQueryBuilder”.

**Explicit results** super().\_builder(expanded args, wrapper\_cls = ParameterizedValueWrapper, expanded names kwargs).

**Local steps**

- Return super().\_builder(expanded args, wrapper\_cls = ParameterizedValueWrapper, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L88) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L131)

<a id="op-363f67e3bc8029"></a>
### Postgres.Field

`operation_foundation_query_builder_builder_business_behavior_relational_database_field`

**Inputs** cls, field\_name, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Explicit results** terms.Field(field\_name, expanded args, expanded names kwargs).

**Local steps**

- If field\_name belongs to cls.field\_translation.
  - Set field\_name from cls.field\_translation at field\_name.
- Return terms.Field(field\_name, expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L2273) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L132)

<a id="op-b7a7a60d0bdf29"></a>
### Postgres.from

`operation_foundation_query_builder_builder_business_behavior_relational_database_from`

**Inputs** cls, table, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Explicit results** super().from\_(table, expanded args, expanded names kwargs).

**Local steps**

- If isinstance(table, Table).
  - If table.\_schema.
    - If table.\_schema.\_name equals “information\_schema”.
      - Set table from (cls.schema\_translation.get(table.\_table\_name) or table).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in cls.schema\_translation.get(table.\_table\_name) → table.
- Otherwise.
  - If isinstance(table, str).
    - Set table from cls.DocType(table).
- Return super().from\_(table, expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L2415) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L133)

<a id="op-ccf7a738c37cc7"></a>
### SQLite.builder

`operation_foundation_query_builder_builder_business_behavior_supplier_quotation_lite_builder`

**Inputs** cls, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Declared result** “SQLLiteQueryBuilder”.

**Explicit results** super().\_builder(expanded args, wrapper\_cls = SQLiteParameterizedValueWrapper, expanded names kwargs).

**Local steps**

- Return super().\_builder(expanded args, wrapper\_cls = SQLiteParameterizedValueWrapper, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L89) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L134)

<a id="op-df5e5009e99ed6"></a>
### SQLite.from

`operation_foundation_query_builder_builder_business_behavior_supplier_quotation_lite_from`

**Inputs** cls, table, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** classmethod.

**Explicit results** super().from\_(table, expanded args, expanded names kwargs).

**Local steps**

- If isinstance(table, str).
  - Set table from cls.DocType(table).
- Return super().from\_(table, expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L2777) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L135)

## Service · Client

<a id="op-5405f228fa2b70"></a>
### Get list

`operation_foundation_client_business_behavior_get_list`

**Inputs** doctype, fields = no value, filters = no value, group\_by = no value, order\_by = no value, limit\_start = no value, limit\_page\_length = 20, parent = no value, debug = false, as\_dict = true, or\_filters = no value, expand = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read call context via get\_list.

**Explicit results** \_list.

**Local steps**

- Set args from Platform.\_dict(doctype = doctype, parent\_doctype = parent, fields = fields, filters = filters, …).
- Evaluate validate\_args(args).
- Set \_list from Platform.get\_list(expanded names args).
- If not expand.
  - Return \_list.
- If (fields and not fields at 0 equals “\*”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → not fields at 0 equals “\*”.
  - Set expand from list of f for f drawn from expand where f belongs to fields.
    - Draw f from expand, keep a combination only if (f belongs to fields).
- Evaluate attach\_expanded\_links(doctype, \_list, expand).
- Return \_list.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L1490) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L556)
