# Record lifecycle and persistence · operations 60

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Mask

<a id="op-40f2955fed4155"></a>
### Mask field value

`operation_foundation_model_utils_mask_business_behavior_mask_field_value`

**Inputs** field, val.

**Explicit results** val · (val at slice no value to 3 + “XXXXXX”) · (“X” × len(val)) · (“XXXXXX@” + email at 1) when len(email) &gt; 1, otherwise “XXXXXX” · “XX-XX-XXXX” · 3 additional forms in the steps below.

**Local steps**

- If not val.
  - Return val.
- If (field.fieldtype equals “Data” and field.options equals “Phone”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Data” → field.options equals “Phone”.
  - If len(val) &gt; 3.
    - Return (val at slice no value to 3 + “XXXXXX”).
  - Otherwise.
    - Return (“X” × len(val)).
- Otherwise.
  - If (field.fieldtype equals “Data” and field.options equals “Email”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Data” → field.options equals “Email”.
    - Set email from val.split(“@”).
    - Return (“XXXXXX@” + email at 1) when len(email) &gt; 1, otherwise “XXXXXX”.
      - Value choice on len(email) &gt; 1 — true gives (“XXXXXX@” + email at 1), false gives “XXXXXX”.
  - Otherwise.
    - If field.fieldtype equals “Date”.
      - Return “XX-XX-XXXX”.
    - Otherwise.
      - If field.fieldtype equals “Time”.
        - Return “XX:XX”.
      - Otherwise.
        - If field.fieldtype equals “Datetime”.
          - Return “XX-XX-XXXX XX:XX”.
        - Otherwise.
          - Return “XXXXXXXX”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L3676) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1322)

<a id="op-f5d06b5b8a6a00"></a>
### Mask pluck results

`operation_foundation_model_utils_mask_business_behavior_mask_pluck_results`

**Inputs** result, masked\_fields, fields.

**Declared result** list at Any.

**Explicit results** result · list of mask\_field\_value(masked\_field, val) for val drawn from result.

**Local steps**

- If not fields.
  - Return result.
- Set masked\_names from set of f.fieldname for f drawn from masked\_fields.
  - Draw f from masked\_fields.
- Set first from fields at 0.
- If hasattr(first, “fields\_”).
  - Set hit\_name from next(generator of f.name for f drawn from first.fields\_() where f.name belongs to masked\_names, no value).
    - Draw f from first.fields\_(), keep a combination only if (f.name belongs to masked\_names).
- Otherwise.
  - Set name from getattr(first, “name”, no value).
  - Set hit\_name from name when name belongs to masked\_names, otherwise no value.
    - Value choice on name belongs to masked\_names — true gives name, false gives no value.
- If not hit\_name.
  - Return result.
- Set masked\_field from next(generator of f for f drawn from masked\_fields where f.fieldname equals hit\_name).
  - Draw f from masked\_fields, keep a combination only if (f.fieldname equals hit\_name).
- Return list of mask\_field\_value(masked\_field, val) for val drawn from result.
  - Draw val from result.

**Values supplied outside this operation** selected callable from getattr(first, “name”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L16) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1325)

<a id="op-47861432d06a52"></a>
### Mask dict results

`operation_foundation_model_utils_mask_business_behavior_mask_mapping_results`

**Inputs** result, masked\_fields.

**Explicit results** result.

**Local steps**

- For each row in result.
  - For each field in masked\_fields.
    - If field.fieldname belongs to row.
      - Set row at field.fieldname from mask\_field\_value(field, row at field.fieldname).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L4733) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1324)

<a id="op-9300b199da11ba"></a>
### Mask list results

`operation_foundation_model_utils_mask_business_behavior_mask_list_results`

**Inputs** result, masked\_fields, field\_index\_map.

**Explicit results** masked\_result.

**Local steps**

- Set masked\_result from list().
- For each row in result.
  - Set row from list(row).
  - For each field in masked\_fields.
    - If field.fieldname belongs to field\_index\_map.
      - Set idx from field\_index\_map at field.fieldname.
      - Set row at idx from mask\_field\_value(field, row at idx).
  - Evaluate masked\_result.append(tuple(row)).
- Return masked\_result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L4887) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1323)

## Service · Meta

<a id="op-4de910ab257a1f"></a>
### Get meta

`operation_foundation_model_meta_business_behavior_get_meta`

**Inputs** doctype, cached = true.

**Declared result** “\_Meta”.

**Explicit results** meta.

**Local steps**

- If (cached and isinstance(doctype, str) and meta bound to Platform.client\_cache.get\_value(formatted text doctype\_meta::{doctype})).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cached → isinstance(doctype, str) → meta bound to Platform.client\_cache.get\_value(formatted text doctype\_meta::{doctype}).
  - Return meta.
- Set meta from Meta(doctype).
- Set key from formatted text doctype\_meta::{meta.name}.
- Evaluate Platform.client\_cache.set\_value(key, meta).
- Return meta.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L278) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L506) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1103)

<a id="op-941d453f305166"></a>
### Clear meta cache

`operation_foundation_model_meta_business_behavior_clear_meta_cache`

**Inputs** doctype = “\*”.

**Local steps**

- Set key from formatted text doctype\_meta::{doctype}.
- If doctype equals “\*”.
  - Evaluate Platform.client\_cache.delete\_keys(key).
- Otherwise.
  - Evaluate Platform.client\_cache.delete\_value(key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L536) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L502) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1099)

<a id="op-f11a4b1436e3aa"></a>
### Load meta

`operation_foundation_model_meta_business_behavior_load_meta`

**Inputs** doctype.

**Explicit results** Meta(doctype).

**Local steps**

- Return Meta(doctype).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L682) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1107)

<a id="op-4f033c1bff4105"></a>
### Get table columns

`operation_foundation_model_meta_business_behavior_get_table_columns`

**Inputs** doctype.

**Explicit results** Platform.db.get\_table\_columns(doctype).

**Local steps**

- Return Platform.db.get\_table\_columns(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L732) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1106)

<a id="op-6b087371b8fba8"></a>
### Load doctype from file

`operation_foundation_model_meta_business_behavior_load_record_type_from_file`

**Inputs** doctype.

**Explicit results** txt.

**Local steps**

- Set fname from Platform.scrub(doctype).
- Within open(Platform.get\_app\_path(“Platform”, “core”, “doctype”, fname, …)) bound as f.
  - Set txt from json.loads(f.read()).
- For each d in txt.get(“fields”, list()).
  - Set d at “doctype” from “DocField”.
- For each d in txt.get(“permissions”, list()).
  - Set d at “doctype” from “DocPerm”.
- Set txt at “fields” from list of Document(d) for d drawn from txt at “fields”.
  - Draw d from txt at “fields”.
- If “permissions” belongs to txt.
  - Set txt at “permissions” from list of Document(d) for d drawn from txt at “permissions”.
    - Draw d from txt at “permissions”.
- Return txt.

**Boundaries to resolve** callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L103) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1108)

<a id="op-a351daec4968bb"></a>
### Meta.initialize

`operation_foundation_model_meta_business_behavior_meta_initialize`

**Inputs** self, doctype.

**Local steps**

- If isinstance(doctype, Document).
  - Evaluate super().\_\_init\_\_(doctype.as\_dict()).
- Otherwise.
  - Evaluate super().\_\_init\_\_(“DocType”, doctype).
- Evaluate self.process().

If control reaches the end, it returns no value.

**Methods declared on this owner** [process](operations-060.md#op-f3523a260d3d20).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L1274) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1156)

<a id="op-71de81c1f1b9d7"></a>
### Meta.load from db

`operation_foundation_model_meta_business_behavior_meta_load_from_database`

**Inputs** self.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Evaluate super().load\_from\_db().
- On failure (Platform.DoesNotExistError).
  - If (self.doctype equals “DocType” and self.name belongs to self.special\_doctypes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “DocType” → self.name belongs to self.special\_doctypes.
    - Evaluate self.\_\_dict\_\_.update(load\_doctype\_from\_file(self.name)).
  - Otherwise.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L1456) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1160)

<a id="op-f3523a260d3d20"></a>
### Meta.process

`operation_foundation_model_meta_business_behavior_meta_process`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.name belongs to self.special\_doctypes.
  - If self.name equals “DocPerm”.
    - Evaluate self.add\_custom\_fields().
  - Evaluate self.init\_field\_caches().
  - Return no value.
- Evaluate self.add\_custom\_fields().
- Evaluate self.apply\_property\_setters().
- Evaluate self.init\_field\_caches().
- Evaluate self.sort\_fields().
- Evaluate self.get\_valid\_columns().
- Evaluate self.set\_custom\_permissions().
- Evaluate self.add\_custom\_links\_and\_actions().
- Evaluate self.check\_if\_large\_table().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add custom fields](operations-061.md#op-8a28c1b8ce38b9), [init field caches](operations-062.md#op-e086c0ff8396cb), [apply property setters](operations-061.md#op-29c71beb960932), [sort fields](operations-062.md#op-16efbf0e54d8e3), [get valid columns](operations-061.md#op-72aec23c03a32b), [set custom permissions](operations-062.md#op-caf4fb982100c9), [add custom links and actions](operations-061.md#op-1717f4d1db2f7b), [check if large table](operations-062.md#op-f518a7fe820a9b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L1659) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1163)

<a id="op-5cb234ad8d8b97"></a>
### Meta.as dict

`operation_foundation_model_meta_business_behavior_meta_as_mapping`

**Inputs** self, no\_nulls = false.

**Explicit results** \_serialize(self, no\_nulls = no\_nulls).

**Local steps**

- Return \_serialize(self, no\_nulls = no\_nulls).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L1959) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1113)

<a id="op-6b6cac9c569804"></a>
### Meta.get link fields

`operation_foundation_model_meta_business_behavior_meta_get_link_fields`

**Inputs** self.

**Explicit results** self.get(“fields”, mapping(“fieldtype” → “Link”, “options” → list(“!=”, “&#91;Select&#93;”))).

**Local steps**

- Return self.get(“fields”, mapping(“fieldtype” → “Link”, “options” → list(“!=”, “&#91;Select&#93;”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L2033) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1131)

<a id="op-d502debc42d956"></a>
### Meta.get data fields

`operation_foundation_model_meta_business_behavior_meta_get_data_fields`

**Inputs** self.

**Explicit results** self.get(“fields”, mapping(“fieldtype” → “Data”)).

**Local steps**

- Return self.get(“fields”, mapping(“fieldtype” → “Data”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L2138) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1120)

<a id="op-7d2f5eec348c68"></a>
### Meta.get phone fields

`operation_foundation_model_meta_business_behavior_meta_get_phone_fields`

**Inputs** self.

**Explicit results** self.get(“fields”, mapping(“fieldtype” → “Phone”)).

**Local steps**

- Return self.get(“fields”, mapping(“fieldtype” → “Phone”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L2218) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1141)

<a id="op-4b0a2502dbb3a9"></a>
### Meta.get dynamic link fields

`operation_foundation_model_meta_business_behavior_meta_get_dynamic_link_fields`

**Inputs** self.

**Explicit results** self.\_dynamic\_link\_fields.

**Local steps**

- Return self.\_dynamic\_link\_fields.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L2298) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1121)

<a id="op-628c538ea3fce2"></a>
### Meta.get masked fields

`operation_foundation_model_meta_business_behavior_meta_get_masked_fields`

**Inputs** self, parenttype = no value.

**Explicit results** list() · masked\_fields.

**Local steps**

- Bind dependencies copy.
- If Platform.session.user equals “Administrator”.
  - Return list().
- Set cache\_key from formatted text masked\_fields::{self.name}::{(parenttype or empty text)}::{Platform.session.user}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parenttype → empty text.
- Set masked\_fields from Platform.cache.get\_value(cache\_key).
- If masked\_fields is identical to no value.
  - Set masked\_fields from list().
  - Set permlevel\_access from set(self.get\_permlevel\_access(“mask”, parenttype)).
  - For each df in self.fields.
    - If (df.get(“mask”) and df.permlevel does not belong to permlevel\_access).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“mask”) → df.permlevel does not belong to permlevel\_access.
      - Set df\_copy from copy.deepcopy(df).
      - Set df\_copy.mask\_readonly from 1.
      - Evaluate masked\_fields.append(df\_copy).
  - Evaluate Platform.cache.set\_value(cache\_key, masked\_fields).
- Return masked\_fields.

**Methods declared on this owner** [get permlevel access](operations-062.md#op-f464954bf55dd3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L2339) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1135)

<a id="op-60f65a14f42e56"></a>
### Meta.dynamic link fields

`operation_foundation_model_meta_business_behavior_meta_dynamic_link_fields`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** self.get(“fields”, mapping(“fieldtype” → “Dynamic Link”)).

**Local steps**

- Return self.get(“fields”, mapping(“fieldtype” → “Dynamic Link”)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L2815) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1115)

<a id="op-d68ec843f91714"></a>
### Meta.get select fields

`operation_foundation_model_meta_business_behavior_meta_get_select_fields`

**Inputs** self.

**Explicit results** self.get(“fields”, mapping(“fieldtype” → “Select”, “options” → list(“not in”, list(“&#91;Select&#93;”, “Loading...”)))).

**Local steps**

- Return self.get(“fields”, mapping(“fieldtype” → “Select”, “options” → list(“not in”, list(“&#91;Select&#93;”, “Loading...”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L2905) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1144)

<a id="op-8b7c00fae4fee1"></a>
### Meta.get image fields

`operation_foundation_model_meta_business_behavior_meta_get_image_fields`

**Inputs** self.

**Explicit results** self.get(“fields”, mapping(“fieldtype” → “Attach Image”)).

**Local steps**

- Return self.get(“fields”, mapping(“fieldtype” → “Attach Image”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L3019) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1129)

<a id="op-42d09eb70aa310"></a>
### Meta.get code fields

`operation_foundation_model_meta_business_behavior_meta_get_code_fields`

**Inputs** self.

**Explicit results** self.get(“fields”, mapping(“fieldtype” → “Code”)).

**Local steps**

- Return self.get(“fields”, mapping(“fieldtype” → “Code”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L3099) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1117)

<a id="op-43aeb6cc6c9340"></a>
### Meta.get set only once fields

`operation_foundation_model_meta_business_behavior_meta_get_set_only_once_fields`

**Inputs** self.

**Explicit results** self.\_set\_only\_once\_fields.

**Local steps**

- Return self.\_set\_only\_once\_fields.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L3179) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1145)

<a id="op-b19f1a77ff7c4e"></a>
### Meta.set only once fields

`operation_foundation_model_meta_business_behavior_meta_set_only_once_fields`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** set\_only\_once\_fields.

**Local steps**

- Set set\_only\_once\_fields from self.get(“fields”, mapping(“set\_only\_once” → 1)).
- Set fieldnames from list of d.fieldname for d drawn from set\_only\_once\_fields.
  - Draw d from set\_only\_once\_fields.
- For each df in self.standard\_set\_once\_fields.
  - If df.fieldname does not belong to fieldnames.
    - Evaluate set\_only\_once\_fields.append(df).
- Return set\_only\_once\_fields.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L3220) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1165)
