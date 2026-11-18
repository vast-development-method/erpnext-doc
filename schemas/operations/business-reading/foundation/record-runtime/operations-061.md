# Record lifecycle and persistence · operations 61

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Meta

<a id="op-993022051b04f8"></a>
### Meta.get table fields

`operation_foundation_model_meta_business_behavior_meta_get_table_fields`

**Inputs** self, include\_computed = false.

**Explicit results** self.\_table\_fields when include\_computed, otherwise self.\_non\_computed\_table\_fields.

**Local steps**

- Return self.\_table\_fields when include\_computed, otherwise self.\_non\_computed\_table\_fields.
  - Value choice on include\_computed — true gives self.\_table\_fields, false gives self.\_non\_computed\_table\_fields.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L3421) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1146)

<a id="op-da6e6de23bbc05"></a>
### Meta.get global search fields

`operation_foundation_model_meta_business_behavior_meta_get_global_search_fields`

**Inputs** self.

**Explicit results** fields.

**Local steps**

- Set fields from self.get(“fields”, mapping(“in\_global\_search” → 1, “fieldtype” → list(“not in”, NO\_VALUE\_FIELDS))).
- If getattr(self, “show\_name\_in\_global\_search”, no value).
  - Evaluate fields.append(Platform.\_dict(fieldtype = “Data”, fieldname = “name”, label = “Name”)).
- Return fields.

**Values supplied outside this operation** selected callable from getattr(self, “show\_name\_in\_global\_search”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L3488) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1127)

<a id="op-72aec23c03a32b"></a>
### Meta.get valid columns

`operation_foundation_model_meta_business_behavior_meta_get_valid_columns`

**Inputs** self.

**Declared result** list at str.

**Explicit results** self.\_valid\_columns.

**Local steps**

- Return self.\_valid\_columns.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L3707) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1150)

<a id="op-20abf9391b5ed6"></a>
### Meta.valid columns

`operation_foundation_model_meta_business_behavior_meta_valid_columns`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** valid\_columns.

**Local steps**

- Set table\_exists from Platform.db.table\_exists(self.name).
- If (self.name belongs to self.special\_doctypes and table\_exists).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.name belongs to self.special\_doctypes → table\_exists.
  - Set valid\_columns from list of c for c drawn from get\_table\_columns(self.name) where c differs from “\_comments”.
    - Draw c from get\_table\_columns(self.name), keep a combination only if (c differs from “\_comments”).
- Otherwise.
  - Set valid\_columns from (self.default\_fields + list of df.fieldname for df drawn from self.get(“fields”) where (not getattr(df, “is\_virtual”, false) and df.fieldtype belongs to data\_fieldtypes)).
    - Draw df from self.get(“fields”), keep a combination only if ((not getattr(df, “is\_virtual”, false) and df.fieldtype belongs to data\_fieldtypes)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not getattr(df, “is\_virtual”, false) → df.fieldtype belongs to data\_fieldtypes.
  - If self.istable.
    - Update valid\_columns using + list(child\_table\_fields).
- Return valid\_columns.

**Values supplied outside this operation** selected callable from getattr(df, “is\_virtual”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L115) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1170)

<a id="op-3d6383e9f3310b"></a>
### Meta.get valid fields

`operation_foundation_model_meta_business_behavior_meta_get_valid_fields`

**Inputs** self.

**Declared result** list at str.

**Explicit results** self.\_valid\_fields.

**Local steps**

- Return self.\_valid\_fields.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L4085) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1151)

<a id="op-7391927e44abb5"></a>
### Meta.valid fields

`operation_foundation_model_meta_business_behavior_meta_valid_fields`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** valid\_fields.

**Local steps**

- If ((Platform.flags.in\_install or Platform.flags.in\_migrate) and self.name belongs to self.special\_doctypes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (Platform.flags.in\_install or Platform.flags.in\_migrate) → self.name belongs to self.special\_doctypes.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate.
  - Set valid\_fields from get\_table\_columns(self.name).
- Otherwise.
  - Set valid\_fields from (self.default\_fields + list of df.fieldname for df drawn from self.get(“fields”) where df.fieldtype belongs to data\_fieldtypes).
    - Draw df from self.get(“fields”), keep a combination only if (df.fieldtype belongs to data\_fieldtypes).
  - If self.istable.
    - Update valid\_fields using + list(child\_table\_fields).
- Return valid\_fields.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L4138) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1171)

<a id="op-d0eff0d3504376"></a>
### Meta.get field

`operation_foundation_model_meta_business_behavior_meta_get_field`

**Inputs** self, fieldname.

**Explicit results** self.\_fields.get(fieldname).

**Local steps**

- Return self.\_fields.get(fieldname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L4411) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1122)

<a id="op-8dc399a0b494c4"></a>
### Meta.has field

`operation_foundation_model_meta_business_behavior_meta_has_field`

**Inputs** self, fieldname.

**Explicit results** fieldname belongs to self.\_fields.

**Local steps**

- Return fieldname belongs to self.\_fields.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L4476) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1154)

<a id="op-4b0bb8dff14d73"></a>
### Meta.get label

`operation_foundation_model_meta_business_behavior_meta_get_label`

**Inputs** self, fieldname.

**Explicit results** df.get(“label”) · str(DEFAULT\_FIELD\_LABELS at fieldname) · “No Label”.

**Local steps**

- If df bound to self.get\_field(fieldname).
  - Return df.get(“label”).
- If fieldname belongs to DEFAULT\_FIELD\_LABELS.
  - Return str(DEFAULT\_FIELD\_LABELS at fieldname).
- Return “No Label”.

**Methods declared on this owner** [get field](operations-061.md#op-d0eff0d3504376).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L107) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1130)

<a id="op-08890b43702cfa"></a>
### Meta.get translated label

`operation_foundation_model_meta_business_behavior_meta_get_translated_label`

**Inputs** self, fieldname.

**Explicit results** str(DEFAULT\_FIELD\_LABELS at fieldname) · \_(self.get\_label(fieldname), context = self.name).

**Local steps**

- If fieldname belongs to DEFAULT\_FIELD\_LABELS.
  - Return str(DEFAULT\_FIELD\_LABELS at fieldname).
- Return \_(self.get\_label(fieldname), context = self.name).

**Methods declared on this owner** [get label](operations-061.md#op-4b0bb8dff14d73).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L112) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1149)

<a id="op-079cbfbd99f6f5"></a>
### Meta.get options

`operation_foundation_model_meta_business_behavior_meta_get_options`

**Inputs** self, fieldname.

**Explicit results** self.get\_field(fieldname).options.

**Local steps**

- Return self.get\_field(fieldname).options.

**Methods declared on this owner** [get field](operations-061.md#op-d0eff0d3504376).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L4775) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1137)

<a id="op-e31d48db551942"></a>
### Meta.get link doctype

`operation_foundation_model_meta_business_behavior_meta_get_link_record_type`

**Inputs** self, fieldname.

**Explicit results** df.options · self.get\_options(df.options).

**Local steps**

- Set df from self.get\_field(fieldname).
- If df.fieldtype equals “Link”.
  - Return df.options.
- If df.fieldtype equals “Dynamic Link”.
  - Return self.get\_options(df.options).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get field](operations-061.md#op-d0eff0d3504376), [get options](operations-061.md#op-079cbfbd99f6f5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L4842) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1132)

<a id="op-8796f7f09f3b61"></a>
### Meta.get search fields

`operation_foundation_model_meta_business_behavior_meta_get_search_fields`

**Inputs** self.

**Explicit results** search\_fields.

**Local steps**

- Set search\_fields from (self.search\_fields or “name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.search\_fields → “name”.
- Set search\_fields from list of d.strip() for d drawn from search\_fields.split(“,”).
  - Draw d from search\_fields.split(“,”).
- If “name” does not belong to search\_fields.
  - Evaluate search\_fields.append(“name”).
- Return search\_fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L110) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1143)

<a id="op-6c010372732f47"></a>
### Meta.get fields to fetch

`operation_foundation_model_meta_business_behavior_meta_get_fields_to_fetch`

**Inputs** self, link\_fieldname = no value.

**Explicit results** out.

**Local steps**

- Set out from list().
- If not link\_fieldname.
  - Set link\_fields from list of df.fieldname for df drawn from self.get\_link\_fields().
    - Draw df from self.get\_link\_fields().
- For each df in self.fields.
  - If (df.fieldtype does not belong to NO\_VALUE\_FIELDS and getattr(df, “fetch\_from”, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to NO\_VALUE\_FIELDS → getattr(df, “fetch\_from”, no value).
    - If link\_fieldname.
      - If df.fetch\_from.startswith((link\_fieldname + “.”)).
        - Evaluate out.append(df).
    - Otherwise.
      - If “.” belongs to df.fetch\_from.
        - Set fieldname from df.fetch\_from.split(“.”, 1) at 0.
        - If fieldname belongs to link\_fields.
          - Evaluate out.append(df).
- Return out.

**Methods declared on this owner** [get link fields](operations-060.md#op-6b6cac9c569804).

**Values supplied outside this operation** selected callable from getattr(df, “fetch\_from”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L5220) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1126)

<a id="op-1fddb72fdc3f03"></a>
### Meta.get list fields

`operation_foundation_model_meta_business_behavior_meta_get_list_fields`

**Inputs** self.

**Explicit results** list\_fields.

**Local steps**

- Set list\_fields from (list(“name”) + list of d.fieldname for d drawn from self.fields where (d.in\_list\_view and d.fieldtype belongs to data\_fieldtypes)).
  - Draw d from self.fields, keep a combination only if ((d.in\_list\_view and d.fieldtype belongs to data\_fieldtypes)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.in\_list\_view → d.fieldtype belongs to data\_fieldtypes.
- If (self.title\_field and self.title\_field does not belong to list\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.title\_field → self.title\_field does not belong to list\_fields.
  - Evaluate list\_fields.append(self.title\_field).
- Return list\_fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L5609) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1133)

<a id="op-b494fd9ec31cd8"></a>
### Meta.get custom fields

`operation_foundation_model_meta_business_behavior_meta_get_custom_fields`

**Inputs** self.

**Explicit results** list of d for d drawn from self.fields where getattr(d, “is\_custom\_field”, false).

**Local steps**

- Return list of d for d drawn from self.fields where getattr(d, “is\_custom\_field”, false).
  - Draw d from self.fields, keep a combination only if (getattr(d, “is\_custom\_field”, false)).

**Values supplied outside this operation** selected callable from getattr(d, “is\_custom\_field”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L5806) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1118)

<a id="op-6dc8549c68ccc9"></a>
### Meta.get title field

`operation_foundation_model_meta_business_behavior_meta_get_title_field`

**Inputs** self.

**Explicit results** title\_field.

**Local steps**

- Set title\_field from getattr(self, “title\_field”, no value).
- If (not title\_field and self.has\_field(“title”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not title\_field → self.has\_field(“title”).
  - Set title\_field from “title”.
- If not title\_field.
  - Set title\_field from “name”.
- Return title\_field.

**Methods declared on this owner** [has field](operations-061.md#op-8dc399a0b494c4).

**Values supplied outside this operation** selected callable from getattr(self, “title\_field”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L111) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1147)

<a id="op-8de668bb57c399"></a>
### Meta.get translatable fields

`operation_foundation_model_meta_business_behavior_meta_get_translatable_fields`

**Inputs** self.

**Explicit results** list of d.fieldname for d drawn from self.fields where d.translatable.

**Local steps**

- Return list of d.fieldname for d drawn from self.fields where d.translatable.
  - Draw d from self.fields, keep a combination only if (d.translatable).

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L6081) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1148)

<a id="op-766e46dc05018a"></a>
### Meta.is translatable

`operation_foundation_model_meta_business_behavior_meta_is_translatable`

**Inputs** self, fieldname.

**Explicit results** field.translatable.

**Local steps**

- If field bound to self.get\_field(fieldname).
  - Return field.translatable.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get field](operations-061.md#op-d0eff0d3504376).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L6153) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1159)

<a id="op-c30be1b0918f89"></a>
### Meta.get workflow

`operation_foundation_model_meta_business_behavior_meta_get_workflow`

**Inputs** self.

**Explicit results** get\_workflow\_name(self.name).

**Local steps**

- Return get\_workflow\_name(self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L6237) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1153)

<a id="op-5284b7ca92f16d"></a>
### Meta.get naming series options

`operation_foundation_model_meta_business_behavior_meta_get_naming_series_options`

**Inputs** self.

**Declared result** list at str.

**Explicit results** options.split(whitespace '\\n') · list().

**Local steps**

- If field bound to self.get\_field(“naming\_series”).
  - Set options from (field.options or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.options → empty text.
  - Return options.split(whitespace '\\n').
- Return list().

**Methods declared on this owner** [get field](operations-061.md#op-d0eff0d3504376).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0283.json#L6295) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1136)

<a id="op-8a28c1b8ce38b9"></a>
### Meta.add custom fields

`operation_foundation_model_meta_business_behavior_meta_add_custom_fields`

**Inputs** self.

**Record and data access** read “Custom Field” via get\_values.

**Explicit results** no value.

**Local steps**

- If not Platform.db.table\_exists(“Custom Field”).
  - Return no value.
- Set custom\_fields from Platform.db.get\_values(“Custom Field”, filters = mapping(“dt” → self.name), fieldname = “\*”, as\_dict = true, order\_by = “idx”, …).
- If not custom\_fields.
  - Return no value.
- Evaluate self.extend(“fields”, custom\_fields).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L104) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1109)

<a id="op-29c71beb960932"></a>
### Meta.apply property setters

`operation_foundation_model_meta_business_behavior_meta_apply_property_setters`

**Inputs** self.

**Record and data access** read “Property Setter” via get\_values.

**Explicit results** no value.

**Local steps**

- If not Platform.db.table\_exists(“Property Setter”).
  - Return no value.
- Set property\_setters from Platform.db.get\_values(“Property Setter”, filters = mapping(“doc\_type” → self.name), fieldname = “\*”, as\_dict = true).
- If not property\_setters.
  - Return no value.
- For each ps in property\_setters.
  - If ps.doctype\_or\_field equals “DocType”.
    - Evaluate self.set(ps.property, cast(ps.property\_type, ps.value)).
  - Otherwise.
    - If ps.doctype\_or\_field equals “DocField”.
      - For each d in self.fields.
        - If d.fieldname equals ps.field\_name.
          - Evaluate d.set(ps.property, cast(ps.property\_type, ps.value)).
          - Leave the innermost loop without its normal-exhaustion alternative.
    - Otherwise.
      - If ps.doctype\_or\_field equals “DocType Link”.
        - For each d in self.links.
          - If d.name equals ps.row\_name.
            - Evaluate d.set(ps.property, cast(ps.property\_type, ps.value)).
            - Leave the innermost loop without its normal-exhaustion alternative.
      - Otherwise.
        - If ps.doctype\_or\_field equals “DocType Action”.
          - For each d in self.actions.
            - If d.name equals ps.row\_name.
              - Evaluate d.set(ps.property, cast(ps.property\_type, ps.value)).
              - Leave the innermost loop without its normal-exhaustion alternative.
        - Otherwise.
          - If ps.doctype\_or\_field equals “DocType State”.
            - For each d in self.states.
              - If d.name equals ps.row\_name.
                - Evaluate d.set(ps.property, cast(ps.property\_type, ps.value)).
                - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L105) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1112)

<a id="op-1717f4d1db2f7b"></a>
### Meta.add custom links and actions

`operation_foundation_model_meta_business_behavior_meta_add_custom_links_and_actions`

**Inputs** self.

**Record and data access** read doctype via get\_all.

**Local steps**

- For each tuple(doctype, fieldname) in tuple(tuple(“DocType Link”, “links”), tuple(“DocType Action”, “actions”), tuple(“DocType State”, “states”)).
  - For each d in Platform.get\_all(doctype, fields = “\*”, filters = dict(parent = self.name, custom = 1), ignore\_ddl = true).
    - Evaluate self.append(fieldname, d).
  - Set order from json.loads((self.get(formatted text {fieldname}\_order) or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(formatted text {fieldname}\_order) → “&#91;&#93;”.
  - If order.
    - Set name\_map from mapping of d.name → d for d drawn from self.get(fieldname).
      - Draw d from self.get(fieldname).
    - Set new\_list from list of name\_map at name for name drawn from order where name belongs to name\_map.
      - Draw name from order, keep a combination only if (name belongs to name\_map).
    - For each d in self.get(fieldname).
      - If d does not belong to new\_list.
        - Evaluate new\_list.append(d).
    - Evaluate self.set(fieldname, new\_list).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0284.json#L979) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1110)
