# Record lifecycle and persistence · operations 63

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Meta

<a id="op-f0ceba60cd7806"></a>
### Meta.is nested set

`operation_foundation_model_meta_business_behavior_meta_is_nested_set`

**Inputs** self.

**Explicit results** (self.has\_field(“lft”) and self.has\_field(“rgt”)).

**Local steps**

- Return (self.has\_field(“lft”) and self.has\_field(“rgt”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_field(“lft”) → self.has\_field(“rgt”).

**Methods declared on this owner** [has field](operations-061.md#op-8dc399a0b494c4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L1357) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1158)

<a id="op-7040e5ff1fa2d7"></a>
### Get parent dt

`operation_foundation_model_meta_business_behavior_get_parent_record_type`

**Inputs** dt.

**Record and data access** read “DocField” via get\_value.

**Explicit results** empty text · (Platform.db.get\_value(“DocField”, mapping(“fieldtype” → tuple(“in”, Platform.model.table\_fields), “options” → dt), “parent”) or empty text).

**Local steps**

- If not Platform.is\_table(dt).
  - Return empty text.
- Return (Platform.db.get\_value(“DocField”, mapping(“fieldtype” → tuple(“in”, Platform.model.table\_fields), “options” → dt), “parent”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“DocField”, mapping(“fieldtype” → tuple(“in”, Platform.model.table\_fields), “options” → dt), “parent”) → empty text.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L1703) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1104)

<a id="op-53c5afcbf2c032"></a>
### Set fieldname

`operation_foundation_model_meta_business_behavior_set_fieldname`

**Inputs** field\_id, fieldname.

**State and service calls** request set\_value on “DocField”.

**Local steps**

- Evaluate Platform.db.set\_value(“DocField”, field\_id, “fieldname”, fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L1879) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1173)

<a id="op-3e212264bcfa72"></a>
### Get field currency

`operation_foundation_model_meta_business_behavior_get_field_currency`

**Inputs** df, doc = no value.

**Record and data access** read split\_opts at 0 via get\_cached\_value · read doc.parenttype via get\_value.

**Explicit results** no value · (nested operand in the contract.local.field\_currency.get(tuple(doc.doctype, doc.name), mapping()).get(df.fieldname) or (doc.get(“parent”) and nested operand in the contract.field\_currency.get(tuple(nested  ….

**Local steps**

- Set currency from no value.
- If not df.get(“options”).
  - Return no value.
- If not doc.
  - Return no value.
- If not getattr(Platform.local, “field\_currency”, no value).
  - Set Platform.local.field\_currency from Platform.\_dict().
- If not (nested operand in the contract.field\_currency.get(tuple(nested operand in the contract.doctype, nested operand in the contract.name), mapping()).get(df.fieldname) or (doc.get(“parent”) and nested operand  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.field\_currency.get(tuple(doc.doctype, doc.name), mapping()).get(df.fieldname) → (doc.get(“parent”) and nested operand in the contract.local.field\_currency.get(tuple(doc.doctype, doc.parent), mapping()).get(df.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“parent”) → Platform.local.field\_currency.get(tuple(doc.doctype, doc.parent), mapping()).get(df.fieldname).
  - Set ref\_docname from (doc.get(“parent”) or doc.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“parent”) → doc.name.
  - If “:” belongs to cstr(df.get(“options”)).
    - Set split\_opts from df.get(“options”).split(“:”).
    - If (len(split\_opts) equals 3 and doc.get(split\_opts at 1)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(split\_opts) equals 3 → doc.get(split\_opts at 1).
      - Set currency from Platform.get\_cached\_value(split\_opts at 0, doc.get(split\_opts at 1), split\_opts at 2).
  - Otherwise.
    - Set currency from doc.get(df.get(“options”)).
    - If doc.get(“parenttype”).
      - If currency.
        - Set ref\_docname from doc.name.
      - Otherwise.
        - If Platform.get\_meta(doc.parenttype).has\_field(df.get(“options”)).
          - Set currency from Platform.db.get\_value(doc.parenttype, doc.parent, df.get(“options”)).
          - If not currency.
            - Set parent from getattr(doc, “parent\_doc”, no value).
            - If parent.
              - Set currency from parent.get(df.get(“options”)).
  - If currency.
    - Evaluate Platform.local.field\_currency.setdefault(tuple(doc.doctype, ref\_docname), Platform.\_dict()).setdefault(df.fieldname, currency).
- Return (nested operand in the contract.local.field\_currency.get(tuple(doc.doctype, doc.name), mapping()).get(df.fieldname) or (doc.get(“parent”) and nested operand in the contract.field\_currency.get(tuple(nested  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.field\_currency.get(tuple(doc.doctype, doc.name), mapping()).get(df.fieldname) → (doc.get(“parent”) and nested operand in the contract.local.field\_currency.get(tuple(doc.doctype, doc.parent), mapping()).get(df.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“parent”) → Platform.local.field\_currency.get(tuple(doc.doctype, doc.parent), mapping()).get(df.fieldname).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “field\_currency”, no value), getattr(doc, “parent\_doc”, no value) · configured or stored value from Platform.get\_cached\_value(split\_opts at 0, doc.get(split\_opts at 1), split\_opts at 2).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L1966) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1101)

<a id="op-31d3ab649b8b37"></a>
### Get field precision

`operation_foundation_model_meta_business_behavior_get_field_precision`

**Inputs** df, doc = no value, currency = no value.

**Explicit results** precision.

**Local steps**

- If df.precision.
  - Set precision from cint(df.precision).
- Otherwise.
  - If df.fieldtype equals “Currency”.
    - Set currency\_precision from get\_currency\_precision().
    - If currency\_precision is distinct from no value.
      - Set precision from currency\_precision.
    - Otherwise.
      - Set precision from get\_precision\_from\_currency\_format((currency or get\_field\_currency(df, doc))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → get\_field\_currency(df, doc).
  - Otherwise.
    - Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 3).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 3.
- Return precision.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L101) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1102)

<a id="op-aef8423412c043"></a>
### Get precision from currency format

`operation_foundation_model_meta_business_behavior_get_precision_from_currency_format`

**Inputs** currency.

**Declared result** int.

**Record and data access** read “Currency” via get\_value.

**Explicit results** number\_format.precision.

**Local steps**

- Bind dependencies get\_number\_format.
- Bind dependencies NumberFormat.
- Set use\_format\_from\_currency from Platform.get\_system\_settings(“use\_number\_format\_from\_currency”).
- Set number\_format from get\_number\_format().
- If use\_format\_from\_currency.
  - Set currency\_format from Platform.db.get\_value(“Currency”, currency, “number\_format”, cache = true).
  - Set number\_format from NumberFormat.from\_string(currency\_format) when currency\_format, otherwise number\_format.
    - Value choice on currency\_format — true gives NumberFormat.from\_string(currency\_format), false gives number\_format.
- Return number\_format.precision.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“use\_number\_format\_from\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L102) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1105)

<a id="op-1a9222e85996eb"></a>
### Get default df

`operation_foundation_model_meta_business_behavior_get_default_df`

**Inputs** fieldname.

**Explicit results** Platform.\_dict(fieldname = fieldname, fieldtype = “Datetime”) · Platform.\_dict(fieldname = fieldname, fieldtype = “Int”) · Platform.\_dict(fieldname = fieldname, fieldtype = “Link”, options = “User”) · Platform.\_dict(fieldname = fieldname, fieldtype = “Data”).

**Local steps**

- If fieldname belongs to (default\_fields + child\_table\_fields).
  - If fieldname belongs to tuple(“creation”, “modified”).
    - Return Platform.\_dict(fieldname = fieldname, fieldtype = “Datetime”).
  - Otherwise.
    - If fieldname belongs to tuple(“idx”, “docstatus”).
      - Return Platform.\_dict(fieldname = fieldname, fieldtype = “Int”).
    - Otherwise.
      - If fieldname belongs to tuple(“owner”, “modified\_by”).
        - Return Platform.\_dict(fieldname = fieldname, fieldtype = “Link”, options = “User”).
  - Return Platform.\_dict(fieldname = fieldname, fieldtype = “Data”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L3855) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1100)

<a id="op-3f30e03c7448f8"></a>
### Trim tables

`operation_foundation_model_meta_business_behavior_trim_tables`

**Inputs** doctype = no value, dry\_run = false, quiet = false.

**Record and data access** read “DocType” via get\_all.

**Explicit results** UPDATED\_TABLES.

**Local steps**

- Bind dependencies click.
- Set UPDATED\_TABLES from mapping().
- Set filters from mapping(“issingle” → 0, “is\_virtual” → 0).
- If doctype.
  - Set filters at “name” from doctype.
- For each doctype in Platform.get\_all(“DocType”, filters = filters, pluck = “name”).
  - Attempt the following.
    - Set dropped\_columns from trim\_table(doctype, dry\_run = dry\_run).
    - If dropped\_columns.
      - Set UPDATED\_TABLES at doctype from dropped\_columns.
  - On failure (Platform.db.TableMissingError).
    - If quiet.
      - Continue with the next iteration or loop test.
    - Evaluate click.secho(formatted text Ignoring missing table for DocType: {doctype}, fg = “yellow”, err = true).
    - Evaluate click.secho(formatted text Consider removing record in the DocType table for {doctype}, fg = “yellow”, err = true).
  - On failure (Exception) bound to e.
    - If quiet.
      - Continue with the next iteration or loop test.
    - Evaluate click.echo(e, err = true).
- Return UPDATED\_TABLES.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L4200) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1176)

<a id="op-f9f7db0b815fba"></a>
### Trim table

`operation_foundation_model_meta_business_behavior_trim_table`

**Inputs** doctype, dry\_run = true.

**Explicit results** DROPPED\_COLUMNS.

**Local steps**

- Set key from formatted text table\_columns::tab{doctype}.
- Evaluate Platform.cache.delete\_value(key).
- Set ignore\_fields from ((default\_fields + optional\_fields) + child\_table\_fields).
- Set columns from Platform.db.get\_table\_columns(doctype).
- Set fields from Platform.get\_meta(doctype, cached = false).get\_fieldnames\_with\_value().
- Set generated\_columns from set of column.name for column drawn from Platform.db.get\_table\_columns\_description(formatted text tab{doctype}) where column.is\_generated.
  - Draw column from Platform.db.get\_table\_columns\_description(formatted text tab{doctype}), keep a combination only if (column.is\_generated).
- Bind local operation is\_internal for subsequent calls.
- Set columns\_to\_remove from list of f for f drawn from list(((set(columns) − set(fields)) − generated\_columns)) where is\_internal(f).
  - Draw f from list(((set(columns) − set(fields)) − generated\_columns)), keep a combination only if (is\_internal(f)).
- Set DROPPED\_COLUMNS from columns\_to\_remove at slice no value to no value.
- If (columns\_to\_remove and not dry\_run).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in columns\_to\_remove → not dry\_run.
  - Set columns\_to\_remove from “, ”.join(generator of formatted text DROP ′{c}′ for c drawn from columns\_to\_remove).
    - Draw c from columns\_to\_remove.
  - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE ′tab{doctype}′ {columns\_to\_remove}).
- Return DROPPED\_COLUMNS.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L117) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1174)

<a id="op-5a240509653258"></a>
### Trim table.is internal

`operation_foundation_model_meta_business_behavior_trim_table_is_internal`

**Inputs** field.

**Explicit results** (field does not belong to ignore\_fields and not field.startswith(“\_”)).

**Local steps**

- Return (field does not belong to ignore\_fields and not field.startswith(“\_”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field does not belong to ignore\_fields → not field.startswith(“\_”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L5264) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1175)

<a id="op-dd46fdb83c1547"></a>
### Update field order based on insert after

`operation_foundation_model_meta_business_behavior_update_field_order_based_on_insert_after`

**Inputs** field\_order, insert\_after\_map.

**State and service calls** call insert on field\_order.

**Local steps**

- Set retry\_field\_insertion from true.
- While retry\_field\_insertion.
  - Set retry\_field\_insertion from false.
  - For each fieldname in list(insert\_after\_map).
    - If fieldname does not belong to field\_order.
      - Continue with the next iteration or loop test.
    - Set custom\_field\_index from field\_order.index(fieldname).
    - For each custom\_field\_name in insert\_after\_map.pop(fieldname).
      - Update custom\_field\_index using + 1.
      - Evaluate field\_order.insert(custom\_field\_index, custom\_field\_name).
    - Set retry\_field\_insertion from true.
- If insert\_after\_map.
  - For each fields in insert\_after\_map.values().
    - Evaluate field\_order.extend(fields).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0285.json#L5344) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1177)

<a id="op-cb59ea10205e33"></a>
### Serialize

`operation_foundation_model_meta_business_behavior_serialize`

**Inputs** doc, no\_nulls = false, is\_child (named only, default false).

**Explicit results** out.

**Local steps**

- Set out from Platform.\_dict().
- For each tuple(key, value) in doc.\_\_dict\_\_.items().
  - If not is\_child.
    - If key belongs to CACHE\_PROPERTIES.
      - Continue with the next iteration or loop test.
    - If isinstance(value, ListOrTuple).
      - If (value and isinstance(value at 0, Document)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → isinstance(value at 0, Document).
        - Set out at key from list of \_serialize(d, no\_nulls = no\_nulls, is\_child = true) for d drawn from value.
          - Draw d from value.
      - Continue with the next iteration or loop test.
  - If ((not no\_nulls and value is identical to no value) or isinstance(value, SerializableTypes)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not no\_nulls and value is identical to no value) → isinstance(value, SerializableTypes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not no\_nulls → value is identical to no value.
    - Set out at key from value.
- If not is\_child.
  - For each fieldname in TABLE\_DOCTYPES\_FOR\_DOCTYPE.
    - If out.get(fieldname) is identical to no value.
      - Set out at fieldname from list().
- Return out.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L116) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1172)

## Service · Model

<a id="op-5071337b0298d4"></a>
### Delete fields

`operation_foundation_model_initialize_business_behavior_delete_fields`

**Inputs** args\_dict, delete = 0.

**Record and data access** read “DocType” via get\_value.

**State and service calls** request delete on “DocField” · request delete on “Singles” · commit · execute a supplied database query.

**Local steps**

- Bind dependencies Platform.utils.
- For each dt in args\_dict.
  - Set fields from args\_dict at dt.
  - If not fields.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.db.delete(“DocField”, mapping(“parent” → dt, “fieldname” → tuple(“in”, fields))).
  - If not delete.
    - Continue with the next iteration or loop test.
  - If Platform.db.get\_value(“DocType”, dt, “issingle”).
    - Evaluate Platform.db.delete(“Singles”, mapping(“doctype” → dt, “field” → tuple(“in”, fields))).
  - Otherwise.
    - Set existing\_fields from Platform.db.describe(dt).
    - Set existing\_fields from ((existing\_fields and list of e at 0 for e drawn from existing\_fields) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (existing\_fields and list of e at 0 for e drawn from existing\_fields) → list().
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing\_fields → list of e at 0 for e drawn from existing\_fields.
      - Draw e from existing\_fields.
    - Set fields\_need\_to\_delete from (set(fields) bitwise and set(existing\_fields)).
    - If not fields\_need\_to\_delete.
      - Continue with the next iteration or loop test.
    - If Platform.db.db\_type equals “mariadb”.
      - Evaluate Platform.db.commit().
    - Set query from (query text (ALTER).format(dt) + “, ”.join(generator of “DROP COLUMN ′{}′”.format(f) for f drawn from fields\_need\_to\_delete)).
      - Draw f from fields\_need\_to\_delete.
    - Evaluate Platform.db.sql(query).
  - If Platform.db.db\_type equals “postgres”.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L2244) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1089)

<a id="op-f2cf848d284937"></a>
### Get permitted fields

`operation_foundation_model_initialize_business_behavior_get_permitted_fields`

**Inputs** doctype, parenttype = no value, user = no value, permission\_type = no value, ignore\_virtual (named only, default false).

**Declared result** list at str.

**Explicit results** valid\_columns · list(expanded meta.default\_fields, expanded permitted\_fields) · result.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set valid\_columns from meta.get\_valid\_columns().
- If (doctype belongs to CORE\_DOCTYPES and doctype differs from “User”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype belongs to CORE\_DOCTYPES → doctype differs from “User”.
  - Return valid\_columns.
- If DEFAULT\_FIELDS.issuperset(valid\_columns).
  - Return valid\_columns.
- If permission\_type is identical to no value.
  - Set permission\_type from “select” when Platform.only\_has\_select\_perm(doctype, user = user), otherwise “read”.
    - Value choice on Platform.only\_has\_select\_perm(doctype, user = user) — true gives “select”, false gives “read”.
- Set permitted\_fields from meta.get\_permitted\_fieldnames(parenttype = parenttype, user = user, permission\_type = permission\_type, with\_virtual\_fields = not ignore\_virtual).
- If permission\_type equals “select”.
  - Return list(expanded meta.default\_fields, expanded permitted\_fields).
- Set valid\_columns from set(valid\_columns).
- Set result from list(expanded meta.default\_fields, expanded generator of fieldname for fieldname drawn from optional\_fields where fieldname belongs to valid\_columns).
  - Draw fieldname from optional\_fields, keep a combination only if (fieldname belongs to valid\_columns).
- If not permitted\_fields.
  - Return result.
- If meta.istable.
  - Evaluate result.extend(child\_table\_fields).
- Evaluate result.extend(permitted\_fields).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L2932) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1090)

<a id="op-1194b479f74788"></a>
### Is default field

`operation_foundation_model_initialize_business_behavior_is_default_field`

**Inputs** fieldname.

**Declared result** bool.

**Explicit results** fieldname belongs to default\_fields.

**Local steps**

- Return fieldname belongs to default\_fields.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L3584) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1091)

## Record · Module def

[Record definition](../../../../data/record-types/module_def.json)

<a id="op-471e54a4008733"></a>
### Module Def.validate

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_placement().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate placement](operations-063.md#op-a1288ccece93e2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L3727) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1670)

<a id="op-a1288ccece93e2"></a>
### Module Def.validate placement

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_validate_placement`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.custom.
  - If (self.app\_name and not Platform.flags.in\_install).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.app\_name → not Platform.flags.in\_install.
    - If self.app\_name does not belong to Platform.get\_installed\_apps().
      - Set self.app\_name from no value.
  - Return no value.
- If not self.app\_name.
  - Bind dependencies get\_module\_app.
  - Set self.app\_name from get\_module\_app(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L3778) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1671)

<a id="op-250b97fa258f72"></a>
### Module Def.after insert

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_after_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies PRIVATE\_MODULE, make\_module\_workspace.
- If (not self.custom or self.name equals PRIVATE\_MODULE).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.custom → self.name equals PRIVATE\_MODULE.
  - Return no value.
- If (Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_patch).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate → Platform.flags.in\_patch.
  - Return no value.
- If (Platform.flags.in\_import or Platform.flags.in\_fixtures).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → Platform.flags.in\_fixtures.
  - Return no value.
- Evaluate make\_module\_workspace(self.name, icon = self.flags.page\_icon).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L81) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1664)

<a id="op-d4675896d82ac2"></a>
### Module Def.on update

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache().
- If (not self.custom and Platform.conf.get(“developer\_mode”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.custom → Platform.conf.get(“developer\_mode”).
  - Evaluate self.create\_modules\_folder().
  - Evaluate self.add\_to\_modules\_txt().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create modules folder](operations-063.md#op-6a23eaadf5d209), [add to modules txt](operations-063.md#op-5310dd03683411).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L4195) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1669)

<a id="op-6a23eaadf5d209"></a>
### Module Def.create modules folder

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_create_modules_folder`

**Inputs** self.

**Local steps**

- Set module\_path from Platform.get\_app\_path(self.app\_name, self.name).
- If not os.path.exists(module\_path).
  - Evaluate os.mkdir(module\_path).
  - Within open(os.path.join(module\_path, “\_\_init\_\_.py”), “w”) bound as f.
    - Evaluate f.write(empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L4333) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1666)

<a id="op-5310dd03683411"></a>
### Module Def.add to modules txt

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_add_to_modules_text_resource`

**Inputs** self.

**Local steps**

- Set modules from no value.
- If not Platform.local.module\_app.get(Platform.scrub(self.name)).
  - Within open(Platform.get\_app\_path(self.app\_name, “modules.txt”)) bound as f.
    - Set content from f.read().
    - If self.name does not belong to content.splitlines().
      - Set modules from list(filter(no value, content.splitlines())).
      - Evaluate modules.append(self.name).
  - If modules.
    - Within open(Platform.get\_app\_path(self.app\_name, “modules.txt”), “w”) bound as f.
      - Evaluate f.write(whitespace '\\n'.join(modules)).
    - Evaluate Platform.clear\_cache().
    - Evaluate Platform.setup\_module\_map().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L4547) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1663)

<a id="op-6cee8ac0c2b16f"></a>
### Module Def.on trash

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_on_trash`

**Inputs** self.

**Record and data access** read “Sidebar” via get\_all · read “Custom Sidebar” via get\_all.

**State and service calls** request delete\_doc for “Sidebar” · request delete\_doc for “Custom Sidebar”.

**Explicit results** no value.

**Local steps**

- For each name in Platform.get\_all(“Sidebar”, filters = mapping(“module” → self.name), pluck = “name”).
  - Evaluate Platform.delete\_doc(“Sidebar”, name, ignore\_missing = true, force = true).
- For each name in Platform.get\_all(“Custom Sidebar”, filters = mapping(“module” → self.name), pluck = “name”).
  - Evaluate Platform.delete\_doc(“Custom Sidebar”, name, ignore\_permissions = true, force = true).
- If (not Platform.conf.get(“developer\_mode”) or Platform.flags.in\_uninstall or self.custom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.conf.get(“developer\_mode”) → Platform.flags.in\_uninstall → self.custom.
  - Return no value.
- If Platform.local.module\_app.get(Platform.scrub(self.name)).
  - Evaluate Platform.db.after\_commit.add(self.delete\_module\_from\_file).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L4996) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1668)

<a id="op-6acf213d3b3aee"></a>
### Module Def.delete module from file

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_delete_module_from_file`

**Inputs** self.

**Local steps**

- Attempt the following.
  - Evaluate delete\_folder(self.module\_name, “Module Def”, self.name).
- On failure (Platform.DoesNotExistError).
  - Take no action here.
- Set modules from list().
- Set modules\_txt from Path(Platform.get\_app\_path(self.app\_name, “modules.txt”)).
- Set modules from list of m for m drawn from modules\_txt.read\_text().splitlines() where m.
  - Draw m from modules\_txt.read\_text().splitlines(), keep a combination only if (m).
- If self.name belongs to modules.
  - Evaluate modules.remove(self.name).
- If modules.
  - Evaluate modules\_txt.write\_text(whitespace '\\n'.join(modules)).
  - Evaluate Platform.clear\_cache().
  - Evaluate Platform.setup\_module\_map().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L5465) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1667)

<a id="op-d0d58876bac8e6"></a>
### Module Def.before rename

`operation_foundation_core_record_definitions_module_def_business_behavior_module_def_before_rename`

**Inputs** self, old, new, merge = false.

**Explicit failure paths** validation helper — translated “Only Custom Modules can be renamed.”.

**Local steps**

- If not self.custom.
  - Call the validation error handler Platform.throw(translated “Only Custom Modules can be renamed.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0088.json#L5834) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1665)
