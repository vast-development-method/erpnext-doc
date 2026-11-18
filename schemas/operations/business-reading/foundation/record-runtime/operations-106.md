# Record lifecycle and persistence · operations 106

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-0248a3a0df9ca0"></a>
### Drop index if exists

`operation_foundation_database_utils_business_behavior_drop_index_if_exists`

**Inputs** table, index.

**Explicit results** no value.

**Local steps**

- Bind dependencies click.
- If not Platform.db.has\_index(table, index).
  - Evaluate click.echo(formatted text - Skipped {index} index for {table} because it doesn't exist).
  - Return no value.
- Attempt the following.
  - If Platform.db.db\_type equals “postgres”.
    - Set safe\_index from index.replace(“"”, “""”).
    - Evaluate Platform.db.sql\_ddl(formatted text DROP INDEX IF EXISTS "{safe\_index}").
  - Otherwise.
    - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′{table}′ DROP INDEX ′{index}′).
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(“Failed to drop index”).
  - Evaluate click.secho(formatted text x Failed to drop index {index} from {table}  {e}, fg = “red”).
  - Return no value.
- Evaluate click.echo(formatted text ✓ dropped {index} index from {table}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L265) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1531)

<a id="op-5afceea89f8c5a"></a>
### Set default

`operation_foundation_model_utils_initialize_business_behavior_set_default`

**Inputs** doc, key.

**State and service calls** execute query text (UPDATE).format(doc.doctype, key, “%s”, “%s”).

**Local steps**

- If not doc.is\_default.
  - Evaluate Platform.db.set(doc, “is\_default”, 1).
- Evaluate Platform.db.sql(query text (UPDATE).format(doc.doctype, key, “%s”, “%s”), tuple(doc.get(key), doc.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L7036) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1312)

<a id="op-685816234bc6c6"></a>
### Set field property

`operation_foundation_model_utils_initialize_business_behavior_set_field_property`

**Inputs** filters, key, value.

**Record and data access** resolve a document from “DocType” via get\_doc · read “DocField” via get\_all.

**State and service calls** call save on d · commit.

**Local steps**

- Set docs from list of Platform.get\_doc(“DocType”, d.parent) for d drawn from Platform.get\_all(“DocField”, fields = list(“parent”), filters = filters).
  - Draw d from Platform.get\_all(“DocField”, fields = list(“parent”), filters = filters).
- For each d in docs.
  - Evaluate d.get(“fields”, filters) at 0.set(key, value).
  - Evaluate d.save().
  - Evaluate print(formatted text Updated {d.name}).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1313)

<a id="op-7136d3a2357186"></a>
### Render include

`operation_foundation_model_utils_initialize_business_behavior_render_include`

**Inputs** content.

**Explicit results** content.

**Explicit failure paths** InvalidIncludePath · validation helper — Platform.\_(“Security Error: The Path provided is not safe.”).

**Local steps**

- Bind dependencies os.
- Set content from cstr(content).
- For each \_ in range(5).
  - If “{% include” belongs to content.
    - Set paths from INCLUDE\_DIRECTIVE\_PATTERN.findall(content).
    - If not paths.
      - Raise InvalidIncludePath.
    - For each path in paths.
      - Set tuple(app, app\_path) from path.split(“/”, 1).
      - Set resolved\_path from os.path.realpath(Platform.get\_app\_path(app, app\_path)).
      - Set app\_root from os.path.realpath(Platform.get\_app\_path(app)).
      - If not resolved\_path.startswith((app\_root + os.sep)).
        - Call the validation error handler Platform.throw(Platform.\_(“Security Error: The Path provided is not safe.”)).
      - Within open(resolved\_path, encoding = “utf-8”) bound as f.
        - Set include from f.read().
        - If path.endswith(“.html”).
          - Bind dependencies html\_to\_js\_template.
          - Set include from html\_to\_js\_template(path, include).
        - Set content from re.sub(formatted text {% include\\s&#91;'"&#93;{path}&#91;'"&#93;\\s%}, include.replace(“\\”, “\\\\”), content).
  - Otherwise.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return content.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L321) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1311)

<a id="op-ebeeb027e38f15"></a>
### Get fetch values

`operation_foundation_model_utils_initialize_business_behavior_get_fetch_values`

**Inputs** doctype, fieldname, value.

**Record and data access** read meta.get\_options(fieldname) via get\_value.

**Explicit results** result.

**Local steps**

- Set result from Platform.\_dict().
- Set meta from Platform.get\_meta(doctype).
- Set fields\_to\_fetch from mapping of df.fieldname → df.fetch\_from.split(“.”, 1) at 1 for df drawn from meta.get\_fields\_to\_fetch(fieldname).
  - Draw df from meta.get\_fields\_to\_fetch(fieldname).
- If not fields\_to\_fetch.
  - Return result.
- For each target\_fieldname in fields\_to\_fetch.
  - Set result at target\_fieldname from no value.
- If not value.
  - Return result.
- Set db\_values from Platform.db.get\_value(meta.get\_options(fieldname), value, tuple(set(fields\_to\_fetch.values())), as\_dict = true).
- If not db\_values.
  - Return result.
- For each tuple(target\_fieldname, source\_fieldname) in fields\_to\_fetch.items().
  - Set result at target\_fieldname from db\_values.get(source\_fieldname).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L953) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1308)

<a id="op-61e95e7a792c0b"></a>
### Is virtual doctype

`operation_foundation_model_utils_initialize_business_behavior_is_virtual_record_type`

**Inputs** doctype.

**Wrappers, in declaration order** site\_cache().

**Record and data access** read “DocType” via get\_value.

**Explicit results** Platform.db.get\_value(“DocType”, doctype, “is\_virtual”) when Platform.db.has\_column(“DocType”, “is\_virtual”), otherwise false · getattr(Platform.get\_meta(doctype), “is\_virtual”, false).

**Local steps**

- If (Platform.flags.in\_install or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate.
  - Return Platform.db.get\_value(“DocType”, doctype, “is\_virtual”) when Platform.db.has\_column(“DocType”, “is\_virtual”), otherwise false.
    - Value choice on Platform.db.has\_column(“DocType”, “is\_virtual”) — true gives Platform.db.get\_value(“DocType”, doctype, “is\_virtual”), false gives false.
- Return getattr(Platform.get\_meta(doctype), “is\_virtual”, false).

**Values supplied outside this operation** selected callable from getattr(Platform.get\_meta(doctype), “is\_virtual”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L1414) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1310)

<a id="op-8def64151fa480"></a>
### Is single doctype

`operation_foundation_model_utils_initialize_business_behavior_is_single_record_type`

**Inputs** doctype.

**Wrappers, in declaration order** site\_cache().

**Declared result** bool.

**Record and data access** read “DocType” via get\_value.

**Explicit results** false · Platform.db.get\_value(“DocType”, doctype, “issingle”) · getattr(Platform.get\_meta(doctype), “issingle”, false).

**Local steps**

- Bind dependencies DOCTYPES\_FOR\_DOCTYPE.
- If doctype belongs to DOCTYPES\_FOR\_DOCTYPE.
  - Return false.
- If (Platform.flags.in\_install or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate.
  - Return Platform.db.get\_value(“DocType”, doctype, “issingle”).
- Otherwise.
  - Return getattr(Platform.get\_meta(doctype), “issingle”, false).

**Values supplied outside this operation** selected callable from getattr(Platform.get\_meta(doctype), “issingle”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L15) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1309)

<a id="op-0ace20d0ceccc7"></a>
### Simple singledispatch

`operation_foundation_model_utils_initialize_business_behavior_simple_singledispatch`

**Inputs** func.

**Explicit results** wrapper.

**Local steps**

- Set registry from mapping().
- Bind local operation dispatch for subsequent calls.
- Bind local operation register for subsequent calls.
- Bind local operation wrapper for subsequent calls.
- Set wrapper.register from register.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L1861) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1314)

<a id="op-4204e8050a7fb1"></a>
### Simple singledispatch.dispatch

`operation_foundation_model_utils_initialize_business_behavior_simple_singledispatch_dispatch`

**Inputs** arg.

**Explicit results** registry at cls · func.

**Local steps**

- For each cls in arg.\_\_class\_\_.\_\_mro\_\_.
  - If cls belongs to registry.
    - Return registry at cls.
- Return func.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L2215) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1315)

<a id="op-f50a2bfa199ecc"></a>
### Simple singledispatch.register

`operation_foundation_model_utils_initialize_business_behavior_simple_singledispatch_register`

**Inputs** type\_.

**Explicit results** decorator.

**Local steps**

- Bind local operation decorator for subsequent calls.
- Return decorator.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L2311) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1316)

<a id="op-8b3af0e05f42b2"></a>
### Simple singledispatch.register.decorator

`operation_foundation_model_utils_initialize_business_behavior_simple_singledispatch_register_decorator`

**Inputs** f.

**Explicit results** f.

**Local steps**

- Set registry at type\_ from f.
- Return f.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L2392) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1317)

<a id="op-38009e2dcfd8cb"></a>
### Simple singledispatch.wrapper

`operation_foundation_model_utils_initialize_business_behavior_simple_singledispatch_wrapper`

**Inputs** remaining positional values args, remaining named values kw.

**Wrappers, in declaration order** wraps(func).

**Explicit results** func(expanded args, expanded names kw) · dispatch(args at 0)(expanded args, expanded names kw).

**Local steps**

- If not args.
  - Return func(expanded args, expanded names kw).
- Return dispatch(args at 0)(expanded args, expanded names kw).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L2449) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1318)

<a id="op-473007ea7af844"></a>
### Pseudo Column Mapper.initialize

`operation_foundation_query_builder_utils_business_behavior_pseudo_column_mapper_initialize`

**Inputs** self, name.

**Declared result** no value.

**Local steps**

- Evaluate super().\_\_init\_\_(name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L2773) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L195)

<a id="op-f1ea6d08eb88f7"></a>
### Pseudo Column Mapper.get sql

`operation_foundation_query_builder_utils_business_behavior_pseudo_column_mapper_get_database_query`

**Inputs** self, remaining named values kwargs.

**Explicit results** convert\_backtick\_identifiers(self.name) · self.name.

**Local steps**

- If Platform.db.db\_type equals “postgres”.
  - Bind dependencies convert\_backtick\_identifiers.
  - Return convert\_backtick\_identifiers(self.name).
- Return self.name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L2846) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L194)

<a id="op-bf74b5e2bdcd64"></a>
### Import Mapper.initialize

`operation_foundation_query_builder_utils_business_behavior_import_mapper_initialize`

**Inputs** self, func\_map.

**Declared result** no value.

**Local steps**

- Set self.func\_map from func\_map.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L2960) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L186)

<a id="op-3a66f531e20b19"></a>
### Import Mapper.invoke

`operation_foundation_query_builder_utils_business_behavior_import_mapper_call`

**Inputs** self, remaining positional values args, remaining named values kwds.

**Declared result** Callable.

**Explicit results** self.func\_map at db(expanded args, expanded names kwds).

**Local steps**

- Set db from db\_type\_is(Platform.conf.db\_type).
- Return self.func\_map at db(expanded args, expanded names kwds).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L3034) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L185)

<a id="op-8e7dee2ffa211c"></a>
### Builder Identification Failed.initialize

`operation_foundation_query_builder_utils_business_behavior_builder_identification_failed_initialize`

**Inputs** self.

**Local steps**

- Evaluate super().\_\_init\_\_(“Couldn't guess builder”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L3152) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L179)

<a id="op-b246856d3b6018"></a>
### Get query builder

`operation_foundation_query_builder_utils_business_behavior_get_query_builder`

**Inputs** type\_of\_db.

**Declared result** ((Postgres bitwise or MariaDB) bitwise or SQLite).

**Explicit results** DB\_TYPE\_MAP at db\_type\_is(type\_of\_db).

**Local steps**

- Return DB\_TYPE\_MAP at db\_type\_is(type\_of\_db).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L3213) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L184)

<a id="op-b183953e9323a3"></a>
### Get query

`operation_foundation_query_builder_utils_business_behavior_get_query`

**Inputs** remaining positional values args, remaining named values kwargs.

**Declared result** QueryBuilder.

**Explicit results** Engine().get\_query(expanded args, expanded names kwargs).

**Local steps**

- Bind dependencies Engine.
- Return Engine().get\_query(expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L3297) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L183)

<a id="op-9a2d6b9392caeb"></a>
### Get attr

`operation_foundation_query_builder_utils_business_behavior_get_attr`

**Inputs** method\_string.

**Explicit results** getattr(import\_module(modulename), methodname).

**Local steps**

- Set modulename from “.”.join(method\_string.split(“.”) at slice no value to negative 1).
- Set methodname from method\_string.split(“.”) at negative 1.
- Return getattr(import\_module(modulename), methodname).

**Values supplied outside this operation** selected callable from getattr(import\_module(modulename), methodname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L3385) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L182)

<a id="op-bacaf950174d09"></a>
### Doc Type

`operation_foundation_query_builder_utils_business_behavior_record_type`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** Platform.qb.DocType(expanded args, expanded names kwargs).

**Local steps**

- Return Platform.qb.DocType(expanded args, expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L3555) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L196)

<a id="op-c2007e69466ce6"></a>
### Table

`operation_foundation_query_builder_utils_business_behavior_table`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** Platform.qb.Table(expanded args, expanded names kwargs).

**Local steps**

- Return Platform.qb.Table(expanded args, expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L3628) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L197)

<a id="op-9187c35f68d558"></a>
### Mask fields

`operation_foundation_query_builder_utils_business_behavior_mask_fields`

**Inputs** doctype, fields, result, as\_dict = true, pluck = false, parent\_doctype = no value.

**Declared result** (list at dict bitwise or list at tuple).

**Explicit results** result · mask\_pluck\_results(result, masked\_fields, fields) · mask\_list\_results(result, masked\_fields, field\_index\_map) · mask\_dict\_results(result, masked\_fields).

**Local steps**

- Bind dependencies CORE\_DOCTYPES.
- Bind dependencies mask\_dict\_results, mask\_list\_results, mask\_pluck\_results.
- If doctype belongs to CORE\_DOCTYPES.
  - Return result.
- Set masked\_fields from Platform.get\_meta(doctype).get\_masked\_fields(parenttype = parent\_doctype).
- If not masked\_fields.
  - Return result.
- If pluck.
  - Return mask\_pluck\_results(result, masked\_fields, fields).
- If not as\_dict.
  - Set field\_index\_map from mapping().
  - For each tuple(idx, field) in enumerate(fields).
    - If alias bound to getattr(field, “alias”, no value).
      - Set field\_index\_map at alias from idx.
    - Otherwise.
      - If name bound to getattr(field, “name”, no value).
        - Set field\_index\_map at name from idx.
  - Return mask\_list\_results(result, masked\_fields, field\_index\_map).
- Return mask\_dict\_results(result, masked\_fields).

**Values supplied outside this operation** selected callable from getattr(field, “alias”, no value), getattr(field, “name”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L102) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L188)

<a id="op-a627943a068c5d"></a>
### Execute query

`operation_foundation_query_builder_utils_business_behavior_execute_query`

**Inputs** query, remaining positional values args, remaining named values kwargs.

**Explicit results** result.

**Local steps**

- Set dt from query.\_\_dict\_\_.get(“\_doctype”).
- Set parent\_dt from query.\_\_dict\_\_.get(“\_parent\_doctype”).
- Set fields from query.\_\_dict\_\_.get(“\_fields\_list”, list()).
- Set child\_queries from query.\_child\_queries.
- Set name\_field\_injected from query.\_\_dict\_\_.get(“\_name\_field\_injected”, false).
- Set tuple(query, params) from prepare\_query(query).
- Set result from Platform.local.db.sql(query, params, expanded args, expanded names kwargs).
- If (child\_queries and isinstance(child\_queries, list) and result).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in child\_queries → isinstance(child\_queries, list) → result.
  - Evaluate execute\_child\_queries(child\_queries, result).
  - If dt.
    - Evaluate mask\_child\_query\_fields(child\_queries, result).
- If (result and dt and fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in result → dt → fields.
  - Set as\_dict from kwargs.get(“as\_dict”, not kwargs.get(“as\_list”, false)).
  - Set result from mask\_fields(dt, fields, result, as\_dict = as\_dict, pluck = kwargs.get(“pluck”, false), parent\_doctype = parent\_dt).
- If (name\_field\_injected and result and not kwargs.get(“pluck”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name\_field\_injected → result → not kwargs.get(“pluck”).
  - If isinstance(result at 0, dict).
    - For each row in result.
      - Evaluate row.pop(“name”, no value).
  - Otherwise.
    - If isinstance(result, tuple).
      - Set result from tuple(generator of row at slice no value to negative 1 for row drawn from result).
        - Draw row from result.
    - Otherwise.
      - Set result from list of row at slice no value to negative 1 for row drawn from result.
        - Draw row from result.
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L101) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L181)
