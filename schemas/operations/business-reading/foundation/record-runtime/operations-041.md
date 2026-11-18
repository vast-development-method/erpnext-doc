# Record lifecycle and persistence · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-d4b9d1aec534bc"></a>
### Document.copy attachments from amended from

`operation_foundation_model_document_business_behavior_document_copy_attachments_from_amended_from`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_url” → attach\_item.file\_url, “file\_name” → attach\_item.file\_name, “attached\_to\_name” → self.name, …) via get\_doc.

**State and service calls** call save on \_file.

**Local steps**

- Bind dependencies get\_attachments.
- For each attach\_item in get\_attachments(self.doctype, self.amended\_from).
  - Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_url” → attach\_item.file\_url, “file\_name” → attach\_item.file\_name, “attached\_to\_name” → self.name, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in attach\_item.folder → “Home/Attachments”.
  - Evaluate \_file.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L1552) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L957)

<a id="op-e1b06d0b7564c6"></a>
### Document.update children

`operation_foundation_model_document_business_behavior_document_update_children`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If getattr(self.meta, “is\_virtual”, false).
  - Return no value.
- For each df in self.meta.get\_table\_fields().
  - Evaluate self.update\_child\_table(df.fieldname, df).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update child table](operations-041.md#op-1f9f023881f4c3).

**Values supplied outside this operation** selected callable from getattr(self.meta, “is\_virtual”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L1853) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1037)

<a id="op-1f9f023881f4c3"></a>
### Document.update child table

`operation_foundation_model_document_business_behavior_document_update_child_table`

**Inputs** self, fieldname, df = no value.

**State and service calls** call db\_update on d.

**Explicit results** no value.

**Local steps**

- Set df from (df or self.meta.get\_field(fieldname)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df → self.meta.get\_field(fieldname).
- If df.is\_virtual.
  - Return no value.
- Set all\_rows from self.get(df.fieldname).
- If not (df.options belongs to (self.flags.ignore\_children\_type or tuple()) or Platform.get\_meta(df.options).is\_virtual equals 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.options belongs to (self.flags.ignore\_children\_type or tuple()) → Platform.get\_meta(df.options).is\_virtual equals 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.ignore\_children\_type → tuple().
  - Set existing\_row\_names from list of row.name for row drawn from all\_rows where (row.name and not row.is\_new()).
    - Draw row from all\_rows, keep a combination only if ((row.name and not row.is\_new())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.name → not row.is\_new().
  - Set tbl from Platform.qb.DocType(df.options).
  - Set qry from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.parenttype equals nested operand in the contract.doctype).where(tbl.parentfield equals fieldname).delete().
  - If existing\_row\_names.
    - Set qry from qry.where(tbl.name.notin(existing\_row\_names)).
  - Evaluate qry.run().
- For each d in all\_rows.
  - Evaluate d.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L1993) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1036)

<a id="op-dea25b21fb6ae0"></a>
### Document.reset computed child tables

`operation_foundation_model_document_business_behavior_document_reset_computed_child_tables`

**Inputs** self.

**Local steps**

- For each df in self.meta.get\_table\_fields(include\_computed = true).
  - If df.is\_virtual.
    - Evaluate self.\_\_dict\_\_.pop(df.fieldname, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L2653) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1008)

<a id="op-1bf04cf78b2762"></a>
### Document.get doc before save

`operation_foundation_model_document_business_behavior_document_get_record_before_save`

**Inputs** self.

**Declared result** “Self”.

**Explicit results** getattr(self, “\_doc\_before\_save”, no value).

**Local steps**

- Return getattr(self, “\_doc\_before\_save”, no value).

**Values supplied outside this operation** selected callable from getattr(self, “\_doc\_before\_save”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L2772) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L362) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L973)

<a id="op-8f6b72ab965032"></a>
### Document.has value changed

`operation_foundation_model_document_business_behavior_document_has_value_changed`

**Inputs** self, fieldname.

**Explicit results** true · previous\_value differs from current\_value.

**Local steps**

- Bind dependencies date, datetime, timedelta.
- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Return true.
- Set previous\_value from previous.get(fieldname).
- Set current\_value from self.get(fieldname).
- If isinstance(previous\_value, datetime).
  - Set current\_value from get\_datetime(current\_value).
- Otherwise.
  - If isinstance(previous\_value, date).
    - Set current\_value from getdate(current\_value).
  - Otherwise.
    - If isinstance(previous\_value, timedelta).
      - Set current\_value from get\_timedelta(current\_value).
- Return previous\_value differs from current\_value.

**Methods declared on this owner** [get doc before save](operations-041.md#op-1bf04cf78b2762), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L2834) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L371) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L982)

<a id="op-7e273e8cafb768"></a>
### Document.get value before save

`operation_foundation_model_document_business_behavior_document_get_value_before_save`

**Inputs** self, fieldname.

**Explicit results** no value · previous.get(fieldname).

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Return no value.
- Return previous.get(fieldname).

**Methods declared on this owner** [get doc before save](operations-041.md#op-1bf04cf78b2762).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L3174) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L978)

<a id="op-a4b137fe489488"></a>
### Document.set new name

`operation_foundation_model_document_business_behavior_document_set_new_name`

**Inputs** self, force = false, set\_name = no value, set\_child\_names = true.

**Explicit results** no value.

**Local steps**

- If (self.flags.name\_set and not force).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags.name\_set → not force.
  - Return no value.
- Set autoname from (self.meta.autoname or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta.autoname → empty text.
- If (self.get(“\_\_newname”) and autoname.lower() equals “prompt”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“\_\_newname”) → autoname.lower() equals “prompt”.
  - Set self.name from validate\_name(self.doctype, self.get(“\_\_newname”)).
  - Set self.flags.name\_set from true.
  - Return no value.
- If set\_name.
  - Set self.name from validate\_name(self.doctype, set\_name).
- Otherwise.
  - Evaluate set\_new\_name(self).
- If set\_child\_names.
  - For each d in self.get\_all\_children().
    - Evaluate set\_new\_name(d).
- Set self.flags.name\_set from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L85) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1025)

<a id="op-ffc6e6a2f73c1d"></a>
### Document.get title

`operation_foundation_model_document_business_behavior_document_get_title`

**Inputs** self.

**Explicit results** (self.get(self.meta.get\_title\_field()) or empty text).

**Local steps**

- Return (self.get(self.meta.get\_title\_field()) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(self.meta.get\_title\_field()) → empty text.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L3726) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L977)

<a id="op-25ed331660090f"></a>
### Document.set title field

`operation_foundation_model_document_business_behavior_document_set_title_field`

**Inputs** self.

**Local steps**

- Bind local operation get\_values for subsequent calls.
- If self.meta.get(“title\_field”) equals “title”.
  - Set df from self.meta.get\_field(self.meta.title\_field).
  - If df.options.
    - Evaluate self.set(df.fieldname, df.options.format(expanded names get\_values())).
  - Otherwise.
    - If (self.is\_new() and not self.get(df.fieldname) and df.default).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not self.get(df.fieldname) → df.default.
      - Evaluate self.set(df.fieldname, df.default.format(expanded names get\_values())).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set](operations-045.md#op-b58a481a5882b4), [is new](operations-046.md#op-e2def851dd1371), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L3805) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1029)

<a id="op-c0532b61c17e56"></a>
### Document.set title field.get values

`operation_foundation_model_document_business_behavior_document_set_title_field_get_values`

**Inputs** no declared parameters.

**Explicit results** values.

**Local steps**

- Set values from self.as\_dict().
- For each tuple(key, value) in values.items().
  - If value is identical to no value.
    - Set values at key from empty text.
- Return values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L4250) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1030)

<a id="op-51e59fec4fa09e"></a>
### Document.update single

`operation_foundation_model_document_business_behavior_document_update_single`

**Inputs** self, d.

**State and service calls** request delete on “Singles” · execute query text (INSERT, Singles).

**Explicit results** no value.

**Local steps**

- If self.meta.is\_virtual.
  - Return no value.
- Evaluate Platform.db.delete(“Singles”, mapping(“doctype” → self.doctype)).
- For each tuple(field, value) in d.items().
  - If field differs from “doctype”.
    - Evaluate Platform.db.sql(query text (INSERT, Singles), tuple(self.doctype, field, value)).
- If self.doctype belongs to Platform.db.value\_cache.
  - Evaluate Platform.db.value\_cache.pop(self.doctype, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L4380) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1038)

<a id="op-e276da7d33f1d3"></a>
### Document.set user and timestamp

`operation_foundation_model_document_business_behavior_document_set_user_and_timestamp`

**Inputs** self.

**Local steps**

- Set self.\_original\_modified from self.modified.
- Set self.modified from now().
- Set self.modified\_by from Platform.session.user.
- If (self.is\_new() and not (Platform.flags.in\_install or Platform.flags.in\_patch or Platform.flags.in\_migrate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not (Platform.flags.in\_install or Platform.flags.in\_patch or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_patch → Platform.flags.in\_migrate.
  - Set self.creation from self.modified.
  - Set self.owner from self.modified\_by.
- For each d in self.get\_all\_children().
  - Set d.modified from self.modified.
  - Set d.modified\_by from self.modified\_by.
  - If not d.owner.
    - Set d.owner from self.owner.
  - If not d.creation.
    - Set d.creation from self.creation.
- Evaluate Platform.flags.currently\_saving.append(tuple(self.doctype, self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371), [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L4734) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1031)

<a id="op-7a66a9775cbc64"></a>
### Document.set docstatus

`operation_foundation_model_document_business_behavior_document_set_record_state`

**Inputs** self.

**Local steps**

- Set docstatus from self.docstatus.
- For each d in self.get\_all\_children().
  - Evaluate d.set(“docstatus”, docstatus).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L5169) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1028)

<a id="op-e142794d43e726"></a>
### Document.validate

`operation_foundation_model_document_business_behavior_document_validate`

**Inputs** self.

**Local steps**

- Evaluate self.\_validate\_mandatory().
- Evaluate self.\_validate\_data\_fields().
- Evaluate self.\_validate\_selects().
- Evaluate self.\_validate\_non\_negative().
- Evaluate self.\_fix\_rating\_value().
- Evaluate self.\_validate\_code\_fields().
- Evaluate self.\_sync\_autoname\_field().
- Evaluate self.\_extract\_images\_from\_text\_editor().
- Evaluate self.\_sanitize\_content().
- Evaluate self.\_save\_passwords().
- Evaluate self.validate\_workflow().
- Evaluate self.\_validate\_length().
- For each d in self.get\_all\_children().
  - Evaluate d.\_validate\_data\_fields().
  - Evaluate d.\_validate\_selects().
  - Evaluate d.\_validate\_non\_negative().
  - Evaluate d.\_fix\_rating\_value().
  - Evaluate d.\_validate\_code\_fields().
  - Evaluate d.\_sync\_autoname\_field().
  - Evaluate d.\_extract\_images\_from\_text\_editor().
  - Evaluate d.\_sanitize\_content().
  - Evaluate d.\_save\_passwords().
  - Evaluate d.\_validate\_length().
- If self.is\_new().
  - For each fieldname in optional\_fields.
    - Evaluate self.set(fieldname, no value).
- Otherwise.
  - Evaluate self.validate\_set\_only\_once().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate mandatory](operations-042.md#op-2870e619f29c89), [validate data fields](operations-047.md#op-8d6ef10ed6f164), [validate selects](operations-046.md#op-db82aaefb80d1a), [validate non negative](operations-041.md#op-5f8e1cf3821b79), [fix rating value](operations-041.md#op-badb62ab76fd04), [validate code fields](operations-047.md#op-49e0d321a3c074), [sync autoname field](operations-047.md#op-ecd0b3b9981a24), [extract images from text editor](operations-047.md#op-7cccadd102f7c5), [sanitize content](operations-047.md#op-c4ce48ce32d460), [save passwords](operations-047.md#op-32c96d5c4b050b), [validate workflow](operations-041.md#op-e37c68297c1973), [validate length](operations-047.md#op-bd0f80066421dc), [get all children](operations-042.md#op-c0f0e764f5c4d1), [is new](operations-046.md#op-e2def851dd1371), [set](operations-045.md#op-b58a481a5882b4), [validate set only once](operations-041.md#op-09daea9a4e95ad).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L86) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1039)

<a id="op-5f8e1cf3821b79"></a>
### Document.validate non negative

`operation_foundation_model_document_business_behavior_document_validate_non_negative`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.NonNegativeError — msg.

**Local steps**

- Bind local operation get\_msg for subsequent calls.
- For each df in self.meta.get(“fields”, mapping(“non\_negative” → tuple(“=”, 1), “fieldtype” → tuple(“in”, list(“Int”, “Float”, “Currency”, “Percent”)))).
  - If flt(self.get(df.fieldname)) &lt; 0.
    - Set msg from get\_msg(df).
    - Call the validation error handler Platform.throw(msg, Platform.NonNegativeError, title = translated “Negative Value”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L5863) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1045)

<a id="op-67c53132f20ab6"></a>
### Document.validate non negative.get msg

`operation_foundation_model_document_business_behavior_document_validate_non_negative_get_message`

**Inputs** df.

**Explicit results** “{} {} #{}: {} {}”.format(Platform.bold(translated self.doctype), translated “Row”, self.idx, translated “Value cannot be negative for”, …) · translated “Value cannot be negative for {0}: {1}”.format(translated df.parent, Platform.bold(\_(df.label, context = df.parent))).

**Local steps**

- If self.get(“parentfield”).
  - Return “{} {} #{}: {} {}”.format(Platform.bold(translated self.doctype), translated “Row”, self.idx, translated “Value cannot be negative for”, …).
- Otherwise.
  - Return translated “Value cannot be negative for {0}: {1}”.format(translated df.parent, Platform.bold(\_(df.label, context = df.parent))).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L6465) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1046)

<a id="op-badb62ab76fd04"></a>
### Document.fix rating value

`operation_foundation_model_document_business_behavior_document_fix_rating_value`

**Inputs** self.

**Local steps**

- For each field in self.meta.get(“fields”, mapping(“fieldtype” → “Rating”)).
  - Set value from self.get(field.fieldname).
  - If not isinstance(value, float).
    - Set value from flt(value).
  - Evaluate self.set(field.fieldname, max(0, min(value, 1))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L1349) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L964)

<a id="op-e37c68297c1973"></a>
### Document.validate workflow

`operation_foundation_model_document_business_behavior_document_validate_workflow`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies set\_workflow\_state\_on\_action, validate\_workflow.
- If Platform.flags.in\_install equals “Platform”.
  - Return no value.
- Set workflow from self.meta.get\_workflow().
- If workflow.
  - Evaluate validate\_workflow(self).
  - If self.\_action differs from “save”.
    - Evaluate set\_workflow\_state\_on\_action(self, workflow, self.\_action).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L92) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1051)

<a id="op-09daea9a4e95ad"></a>
### Document.validate set only once

`operation_foundation_model_document_business_behavior_document_validate_set_only_once`

**Inputs** self.

**Explicit results** false.

**Explicit failure paths** validation helper with Platform.CannotChangeConstantError — translated “Value cannot be changed for {0}”.format(Platform.bold(translated self.meta.get\_label(field.fieldname))).

**Local steps**

- Set set\_only\_once\_fields from self.meta.get\_set\_only\_once\_fields().
- If (set\_only\_once\_fields and self.\_doc\_before\_save).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in set\_only\_once\_fields → self.\_doc\_before\_save.
  - For each field in set\_only\_once\_fields.
    - Set fail from false.
    - Set value from self.get(field.fieldname).
    - Set original\_value from self.\_doc\_before\_save.get(field.fieldname).
    - If field.fieldtype belongs to table\_fields.
      - Set fail from not self.is\_child\_table\_same(field.fieldname).
    - Otherwise.
      - If (field.fieldtype equals “Datetime” and value and original\_value).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Datetime” → value → original\_value.
        - Set fail from get\_datetime(value) differs from get\_datetime(original\_value).
      - Otherwise.
        - If field.fieldtype belongs to tuple(“Date”, “Datetime”, “Time”).
          - Set fail from str(value) differs from str(original\_value).
        - Otherwise.
          - Set fail from value differs from original\_value.
    - If fail.
      - Call the validation error handler Platform.throw(translated “Value cannot be changed for {0}”.format(Platform.bold(translated nested operand in the contract.meta.get\_label(field.fieldname))), exc = Platform.CannotChangeConstantError).
- Return false.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [is child table same](operations-041.md#op-456a186f0dfc39).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L89) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1047)

<a id="op-456a186f0dfc39"></a>
### Document.is child table same

`operation_foundation_model_document_business_behavior_document_is_child_table_same`

**Inputs** self, fieldname.

**Explicit results** false · same.

**Local steps**

- If self.is\_new().
  - Return false.
- Set same from true.
- Set value from self.get(fieldname).
- Set original\_value from self.\_doc\_before\_save.get(fieldname).
- If len(original\_value) differs from len(value).
  - Set same from false.
- Otherwise.
  - For each tuple(i, d) in enumerate(original\_value).
    - Set new\_child from value at i.as\_dict(convert\_dates\_to\_str = true).
    - Set original\_child from d.as\_dict(convert\_dates\_to\_str = true).
    - For each key in tuple(“modified”, “modified\_by”, “creation”).
      - Remove new\_child at key.
      - Remove original\_child at key.
    - If original\_child differs from new\_child.
      - Set same from false.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return same.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L2268) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L379) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L990)

<a id="op-d047126fb76210"></a>
### Document.apply fieldlevel read permissions

`operation_foundation_model_document_business_behavior_document_apply_fieldlevel_read_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 5 condition or selection sites, 5 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0278.json#L2699) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L948)

<a id="op-b915a276ebbe3c"></a>
### Document.copy with fieldlevel read permissions

`operation_foundation_binding_foundation_model_document_document_copy_with_fieldlevel_read_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1561)

<a id="op-15aa4cc364bfb4"></a>
### Document.has fieldlevel read restrictions

`operation_foundation_binding_foundation_model_document_document_has_fieldlevel_read_restrictions`

**Inputs** self.

**Declared result** bool.

**Explicit results** true · bool((permlevels − set(self.get\_permlevel\_access(“read”)))).

**Local steps**

- If self.meta.get\_masked\_fields().
  - Return true.
- Set permlevels from set of df.permlevel for df drawn from self.meta.fields where df.permlevel.
  - Draw df from self.meta.fields, keep a combination only if (df.permlevel).
- For each table\_field in self.meta.get\_table\_fields(include\_computed = true).
  - Set child\_meta from Platform.get\_meta(table\_field.options).
  - Evaluate permlevels.update(generator of df.permlevel for df drawn from child\_meta.fields where df.permlevel).
    - Draw df from child\_meta.fields, keep a combination only if (df.permlevel).
  - If child\_meta.get\_masked\_fields(parenttype = self.doctype).
    - Return true.
- Return bool((permlevels − set(self.get\_permlevel\_access(“read”)))).

**Methods declared on this owner** [get permlevel access](operations-042.md#op-a3ee87a4360b5d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1616) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1592)
