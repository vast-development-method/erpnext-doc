# Record lifecycle and persistence · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Custom

<a id="op-cc6b84af6617cd"></a>
### GROUP CONCAT.initialize

`operation_foundation_query_builder_custom_business_behavior_group_concat_initialize`

**Inputs** self, column, alias = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(“GROUP\_CONCAT”, column, alias = alias).
- Set self.\_separator from “,”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L91) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L139)

<a id="op-321730954172b9"></a>
### GROUP CONCAT.separator

`operation_foundation_query_builder_custom_business_behavior_group_concat_separator`

**Inputs** self, separator = empty text.

**Wrappers, in declaration order** builder.

**Local steps**

- Set self.\_separator from separator.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L92) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L140)

<a id="op-10ac7aa66f9092"></a>
### GROUP CONCAT.get sql

`operation_foundation_query_builder_custom_business_behavior_group_concat_get_database_query`

**Inputs** self, remaining named values kwargs.

**Explicit results** format\_alias\_sql(sql, query\_alias, expanded names kwargs) · sql.

**Local steps**

- Set query\_alias from self.alias.
- Set self.alias from no value.
- Attempt the following.
  - Set sql from super().get\_sql(expanded names kwargs).
- On exit, including pending return or failure.
  - Set self.alias from query\_alias.
- If self.\_separator.
  - Set sql from formatted text {sql at slice no value to negative 1} SEPARATOR {Platform.db.escape(self.\_separator)}).
- If kwargs.get(“with\_alias”).
  - Return format\_alias\_sql(sql, query\_alias, expanded names kwargs).
- Return sql.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L90) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L138)

<a id="op-02b9b76f40a645"></a>
### STRING AGG.initialize

`operation_foundation_query_builder_custom_business_behavior_string_aggregation_initialize`

**Inputs** self, column, separator = “,”, alias = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(“STRING\_AGG”, column, separator, alias = alias).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L3484) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L147)

<a id="op-02460a0c8540b1"></a>
### MATCH.initialize

`operation_foundation_query_builder_custom_business_behavior_match_initialize`

**Inputs** self, column, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set alias from kwargs.get(“alias”).
- Evaluate super().\_\_init\_\_(“ MATCH”, column, expanded args, alias = alias).
- Set self.\_Against from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L3706) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L143)

<a id="op-df782aaf11ec2c"></a>
### MATCH.get function sql

`operation_foundation_query_builder_custom_business_behavior_match_get_function_database_query`

**Inputs** self, remaining named values kwargs.

**Explicit results** formatted text {s} AGAINST ({Platform.db.escape(formatted text +{self.\_Against}\*)} IN BOOLEAN MODE).

**Explicit failure paths** Exception(“Chain the ′Against()′ method with match to complete the query”).

**Local steps**

- Set s from super(DistinctOptionFunction, self).get\_function\_sql(expanded names kwargs).
- If self.\_Against.
  - Return formatted text {s} AGAINST ({Platform.db.escape(formatted text +{self.\_Against}\*)} IN BOOLEAN MODE).
- Raise Exception(“Chain the ′Against()′ method with match to complete the query”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L3861) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L142)

<a id="op-099c37b5e5c379"></a>
### MATCH.Against

`operation_foundation_query_builder_custom_business_behavior_match_against`

**Inputs** self, text.

**Wrappers, in declaration order** builder.

**Local steps**

- Set self.\_Against from text.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L4066) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L141)

<a id="op-019edce4da7cee"></a>
### TO TSVECTOR.initialize

`operation_foundation_query_builder_custom_business_behavior_to_text_search_vector_initialize`

**Inputs** self, column, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set alias from kwargs.get(“alias”).
- Evaluate super().\_\_init\_\_(“TO\_TSVECTOR”, column, expanded args, alias = alias).
- Set self.\_PLAINTO\_TSQUERY from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L97) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L150)

<a id="op-cea737f912b96a"></a>
### TO TSVECTOR.get function sql

`operation_foundation_query_builder_custom_business_behavior_to_text_search_vector_get_function_database_query`

**Inputs** self, remaining named values kwargs.

**Explicit results** formatted text {s} @@ PLAINTO\_TSQUERY({Platform.db.escape(self.\_PLAINTO\_TSQUERY)}) · s.

**Local steps**

- Set s from super(DistinctOptionFunction, self).get\_function\_sql(expanded names kwargs).
- If self.\_PLAINTO\_TSQUERY.
  - Return formatted text {s} @@ PLAINTO\_TSQUERY({Platform.db.escape(self.\_PLAINTO\_TSQUERY)}).
- Return s.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L96) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L149)

<a id="op-385b0b3e73a306"></a>
### TO TSVECTOR.Against

`operation_foundation_query_builder_custom_business_behavior_to_text_search_vector_against`

**Inputs** self, text.

**Wrappers, in declaration order** builder.

**Local steps**

- Set self.\_PLAINTO\_TSQUERY from text.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L4457) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L148)

<a id="op-66594440e15a47"></a>
### Constant Column.initialize

`operation_foundation_query_builder_custom_business_behavior_constant_column_initialize`

**Inputs** self, value.

**Declared result** no value.

**Local steps**

- Set self.value from value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L4521) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L137)

<a id="op-57b3c727236f61"></a>
### Constant Column.get sql

`operation_foundation_query_builder_custom_business_behavior_constant_column_get_database_query`

**Inputs** self, quote\_char = no value, remaining named values kwargs.

**Declared result** str.

**Explicit results** format\_alias\_sql(format\_quotes(self.value, (kwargs.get(“secondary\_quote\_char”) or empty text)), (self.alias or self.value), quote\_char = quote\_char, expanded names kwargs).

**Local steps**

- Return format\_alias\_sql(format\_quotes(self.value, (kwargs.get(“secondary\_quote\_char”) or empty text)), (self.alias or self.value), quote\_char = quote\_char, expanded names kwargs).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.get(“secondary\_quote\_char”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.alias → self.value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0319.json#L4580) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L136)

<a id="op-1c6fc93a91d8b6"></a>
### Month Name.initialize

`operation_foundation_query_builder_custom_business_behavior_month_name_initialize`

**Inputs** self, field, alias = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(“MONTHNAME”, field, alias = alias).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L94) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L145)

<a id="op-49a0a074ba0261"></a>
### Quarter.initialize

`operation_foundation_query_builder_custom_business_behavior_quarter_initialize`

**Inputs** self, field, alias = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(“QUARTER”, field, alias = alias).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L95) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L146)

<a id="op-240be4de7aa0d4"></a>
### Month.initialize

`operation_foundation_query_builder_custom_business_behavior_month_initialize`

**Inputs** self, field, alias = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(“MONTH”, field, alias = alias).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L93) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L144)

<a id="op-4b51755d649b7b"></a>
### Year.initialize

`operation_foundation_query_builder_custom_business_behavior_year_initialize`

**Inputs** self, field, alias = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(“YEAR”, field, alias = alias).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L98) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L151)

## Record · Custom docperm

<a id="op-01bade788760aa"></a>
### Custom Doc Perm.on update

`operation_foundation_core_record_definitions_custom_docperm_business_behavior_custom_record_permission_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(doctype = self.parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0047.json#L3782) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1098) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1115)

<a id="op-4dc6cbcbdaa270"></a>
### Custom Doc Perm.get permission log options

`operation_foundation_core_record_definitions_custom_docperm_business_behavior_custom_record_permission_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0047.json#L3847) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1097) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1114)

<a id="op-8e3bb977ccad63"></a>
### Update custom docperm

`operation_foundation_core_record_definitions_custom_docperm_business_behavior_update_custom_docperm`

**Inputs** docperm, values.

**Record and data access** resolve a document from “Custom DocPerm” via get\_doc.

**State and service calls** call save on custom\_docperm.

**Local steps**

- Set custom\_docperm from Platform.get\_doc(“Custom DocPerm”, docperm).
- Evaluate custom\_docperm.update(values).
- Evaluate custom\_docperm.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0047.json#L3938) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1116)

## Record · Custom role

[Record definition](../../../../data/record-types/custom_role.json)

<a id="op-3d4b743fdb43b2"></a>
### Custom Role.validate

`operation_foundation_core_record_definitions_custom_role_business_behavior_custom_role_validate`

**Inputs** self.

**Record and data access** read “Report” via get\_value.

**Local steps**

- If (self.report and not self.ref\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.report → not self.ref\_doctype.
  - Set self.ref\_doctype from Platform.db.get\_value(“Report”, self.report, “ref\_doctype”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L708) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1118)

<a id="op-4e75cd3f35ad50"></a>
### Custom Role.get permission log options

`operation_foundation_core_record_definitions_custom_role_business_behavior_custom_role_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L830) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1117)

<a id="op-7a5df8a431de37"></a>
### Get custom allowed roles

`operation_foundation_core_record_definitions_custom_role_business_behavior_get_custom_allowed_roles`

**Inputs** field, name.

**Record and data access** read “Custom Role” via get\_value · resolve a document from “Custom Role” via get\_doc.

**Explicit results** allowed\_roles.

**Local steps**

- Set allowed\_roles from list().
- Set custom\_role from Platform.db.get\_value(“Custom Role”, mapping(field → name), “name”).
- If custom\_role.
  - Set custom\_role\_doc from Platform.get\_doc(“Custom Role”, custom\_role).
  - Set allowed\_roles from list of d.role for d drawn from custom\_role\_doc.roles.
    - Draw d from custom\_role\_doc.roles.
- Return allowed\_roles.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L1034) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1119)

## Record · Data export

[Record definition](../../../../data/record-types/data_export.json)

<a id="op-69f84d22a10616"></a>
### Get data keys

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_get_data_keys`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(mapping(“data\_separator” → translated “Start entering data below this line”, “main\_table” → (translated “Table” + “:”), “parent\_table” → (translated “Parent Table” + “:”), “columns” → (trans ….

**Local steps**

- Return Platform.\_dict(mapping(“data\_separator” → translated “Start entering data below this line”, “main\_table” → (translated “Table” + “:”), “parent\_table” → (translated “Parent Table” + “:”), “columns” → (trans ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L1242) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1134)

<a id="op-1422e7a312b6c8"></a>
### Export data

`operation_foundation_core_record_definitions_data_export_exporter_business_behavior_export_data`

**Inputs** doctype = no value, parent\_doctype = no value, all\_doctypes = true, with\_data = false, select\_columns = no value, file\_type = “CSV”, template = false, filters = no value, export\_without\_column\_meta = false.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set \_doctype from doctype.
- If isinstance(\_doctype, list).
  - Set \_doctype from \_doctype at 0.
- Evaluate make\_access\_log(doctype = \_doctype, file\_type = file\_type, columns = select\_columns, filters = filters, …).
- Set template\_bool from template.
- If isinstance(template, str).
  - Set template\_bool from template.lower() equals “true”.
- Set export\_without\_column\_meta\_bool from export\_without\_column\_meta.
- If isinstance(export\_without\_column\_meta, str).
  - Set export\_without\_column\_meta\_bool from export\_without\_column\_meta.lower() equals “true”.
- Set exporter from DataExporter(doctype = doctype, parent\_doctype = parent\_doctype, all\_doctypes = all\_doctypes, with\_data = with\_data, …).
- Evaluate exporter.build\_response().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0048.json#L1458) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1133)
