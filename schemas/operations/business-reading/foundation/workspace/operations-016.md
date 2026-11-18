# Forms, reports and navigation · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Custom workspace

[Record definition](../../../../data/record-types/custom_workspace.json)

<a id="op-59bd41a5ef2413"></a>
### Upsert settings customization

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_upsert_settings_customization`

**Inputs** workspace, icon (named only, default no value), indicator\_color (named only, default no value), roles (named only, default no value).

**Declared result** no value.

**Record and data access** resolve a document from “Workspace” via get\_cached\_doc.

**State and service calls** call save on customization.

**Local steps**

- Set customization from \_get\_or\_new(workspace).
- If icon is distinct from no value.
  - Set customization.icon from icon.
- If indicator\_color is distinct from no value.
  - Set customization.indicator\_color from indicator\_color.
- If roles is distinct from no value.
  - Set base from set of r.role for r drawn from Platform.get\_cached\_doc(“Workspace”, workspace).roles.
    - Draw r from Platform.get\_cached\_doc(“Workspace”, workspace).roles.
  - Set desired from set(roles).
  - Evaluate customization.set(“added\_roles”, list of mapping(“role” → r) for r drawn from sorted((desired − base))).
    - Draw r from sorted((desired − base)).
  - Evaluate customization.set(“removed\_roles”, list of mapping(“role” → r) for r drawn from sorted((base − desired))).
    - Draw r from sorted((base − desired)).
- Evaluate customization.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Workspace”, workspace).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L4514) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L50) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L573)

<a id="op-49d3f83b3604d3"></a>
### Get or new

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_get_or_new`

**Inputs** workspace.

**Declared result** “CustomWorkspace”.

**Record and data access** read “Custom Workspace” via exists · resolve a document from “Custom Workspace” via get\_doc · resolve a document from mapping(“doctype” → “Custom Workspace”, “workspace” → workspace) via get\_doc.

**Explicit results** Platform.get\_doc(“Custom Workspace”, workspace) · Platform.get\_doc(mapping(“doctype” → “Custom Workspace”, “workspace” → workspace)).

**Local steps**

- If Platform.db.exists(“Custom Workspace”, workspace).
  - Return Platform.get\_doc(“Custom Workspace”, workspace).
- Return Platform.get\_doc(mapping(“doctype” → “Custom Workspace”, “workspace” → workspace)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L4994) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L45) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L568)

<a id="op-1be1ebbf3860fc"></a>
### Reset workspace customization

`operation_foundation_desk_record_definitions_custom_workspace_business_behavior_reset_workspace_customization`

**Inputs** workspace.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need to be Workspace Manager to reset a workspace.”.

**Local steps**

- Bind dependencies is\_workspace\_manager.
- If not is\_workspace\_manager().
  - Call the validation error handler Platform.throw(translated “You need to be Workspace Manager to reset a workspace.”, Platform.PermissionError).
- Evaluate Platform.delete\_doc\_if\_exists(“Custom Workspace”, workspace).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0161.json#L5166) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L47) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L570)

## Record · Customize form

[Record definition](../../../../data/record-types/customize_form.json)

<a id="op-9013e53fd76d18"></a>
### Customize Form.on update

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_on_update`

**Inputs** self.

**State and service calls** request delete on “Singles” · request delete on “Customize Form Field”.

**Local steps**

- Evaluate Platform.db.delete(“Singles”, mapping(“doctype” → “Customize Form”)).
- Evaluate Platform.db.delete(“Customize Form Field”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0123.json#L6491) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L967)

<a id="op-3f872e4720ee3f"></a>
### Customize Form.fetch to customize

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_fetch_to_customize`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- Evaluate self.clear\_existing\_doc().
- If not self.doc\_type.
  - Return no value.
- Set meta from Platform.get\_meta(self.doc\_type, cached = false).
- Evaluate self.validate\_doctype(meta).
- Evaluate self.load\_properties(meta).
- Set translation from self.get\_name\_translation().
- Set self.label from translation.translated\_text when translation, otherwise empty text.
  - Value choice on translation — true gives translation.translated\_text, false gives empty text.
- Evaluate self.create\_auto\_repeat\_custom\_field\_if\_required(meta).

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear existing doc](operations-016.md#op-53866b63cf4112), [validate doctype](operations-016.md#op-952725a794db11), [load properties](operations-016.md#op-f7de63c0d6753a), [get name translation](operations-016.md#op-8f707728cdf151), [create auto repeat custom field if required](operations-016.md#op-d39da7329b20cf).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0123.json#L6606) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L962)

<a id="op-952725a794db11"></a>
### Customize Form.validate doctype

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_validate_record_type`

**Inputs** self, meta.

**Explicit failure paths** validation helper — translated “Core DocTypes cannot be customized.” · validation helper — translated “Single DocTypes cannot be customized.” · validation helper — translated “Only standard DocTypes are allowed to be customized from Customize Form.”.

**Local steps**

- If self.doc\_type belongs to core\_doctypes\_list.
  - Call the validation error handler Platform.throw(translated “Core DocTypes cannot be customized.”).
- If meta.issingle.
  - Call the validation error handler Platform.throw(translated “Single DocTypes cannot be customized.”).
- If meta.custom.
  - Call the validation error handler Platform.throw(translated “Only standard DocTypes are allowed to be customized from Customize Form.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0123.json#L6874) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L983)

<a id="op-f7de63c0d6753a"></a>
### Customize Form.load properties

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_load_properties`

**Inputs** self, meta.

**Local steps**

- For each prop in doctype\_properties.
  - Evaluate self.set(prop, meta.get(prop)).
- For each d in meta.get(“fields”).
  - Set new\_d from mapping(“fieldname” → d.fieldname, “is\_custom\_field” → d.get(“is\_custom\_field”), “is\_system\_generated” → d.get(“is\_system\_generated”), “name” → d.name).
  - For each prop in docfield\_properties.
    - Set new\_d at prop from d.get(prop).
  - Evaluate self.append(“fields”, new\_d).
- For each fieldname in tuple(“links”, “actions”, “states”).
  - For each d in meta.get(fieldname).
    - Evaluate self.append(fieldname, d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L965)

<a id="op-d39da7329b20cf"></a>
### Customize Form.create auto repeat custom field if required

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_create_auto_repeat_custom_field_if_required`

**Inputs** self, meta.

**Explicit results** no value.

**Local steps**

- If self.allow\_auto\_repeat.
  - Set all\_fields from list of df.fieldname for df drawn from meta.fields.
    - Draw df from meta.fields.
  - If “auto\_repeat” belongs to all\_fields.
    - Return no value.
  - Set insert\_after from self.fields at (len(self.fields) − 1).fieldname.
  - Evaluate create\_custom\_field(self.doc\_type, dict(fieldname = “auto\_repeat”, label = “Auto Repeat”, fieldtype = “Link”, options = “Auto Repeat”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L447) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L960)

<a id="op-8f707728cdf151"></a>
### Customize Form.get name translation

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_get_name_translation`

**Inputs** self.

**Record and data access** read “Translation” via get\_value.

**Explicit results** Platform.get\_value(“Translation”, mapping(“source\_text” → self.doc\_type, “language” → (Platform.local.lang or “en”)), list(“name”, “translated\_text”), as\_dict = true).

**Local steps**

- Return Platform.get\_value(“Translation”, mapping(“source\_text” → self.doc\_type, “language” → (Platform.local.lang or “en”)), list(“name”, “translated\_text”), as\_dict = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → “en”.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L748) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L964)

<a id="op-392598429566a5"></a>
### Customize Form.set name translation

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_set_name_translation`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Translation”, “source\_text” → self.doc\_type, “translated\_text” → self.label, “language\_code” → (Platform.local.lang or “en”)) via get\_doc.

**State and service calls** request delete\_doc for “Translation” · call insert on Platform.get\_doc(mapping(“doctype” → “Translation”, “source\_text” → self.doc\_type, “translated\_text” → self.label, “language\_code” → (Platform.local.lang or “en”))) · request set\_value on “Translation”.

**Explicit results** no value.

**Local steps**

- Set current from self.get\_name\_translation().
- If not self.label.
  - If current.
    - Evaluate Platform.delete\_doc(“Translation”, current.name).
  - Return no value.
- If not current.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Translation”, “source\_text” → self.doc\_type, “translated\_text” → self.label, “language\_code” → (nested operand in the contract.local.lang or “en”))).insert().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → “en”.
  - Return no value.
- If self.label differs from current.translated\_text.
  - Evaluate Platform.db.set\_value(“Translation”, current.name, “translated\_text”, self.label).
  - Evaluate Platform.translate.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get name translation](operations-016.md#op-8f707728cdf151).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L899) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L971)

<a id="op-53866b63cf4112"></a>
### Customize Form.clear existing doc

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_clear_existing_record`

**Inputs** self.

**Local steps**

- Set doc\_type from self.doc\_type.
- For each fieldname in self.meta.get\_valid\_columns().
  - Evaluate self.set(fieldname, no value).
- For each df in self.meta.get\_table\_fields().
  - Evaluate self.set(df.fieldname, list()).
- Set self.doc\_type from doc\_type.
- Set self.name from “Customize Form”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L1290) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L958)

<a id="op-5a20d81c966e0f"></a>
### Customize Form.save customization

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_save_customization`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “{0} updated”.format(translated self.doc\_type) · enqueue with “Platform.utils.global\_search.rebuild\_for\_doctype”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “You have hit the row size limit on database table: {0}”.format(text in the contract) · propagate active failure.

**Local steps**

- If not self.doc\_type.
  - Return no value.
- Evaluate validate\_series(self, self.autoname, self.doc\_type).
- Evaluate validate\_autoincrement\_autoname(self).
- Set self.flags.update\_db from false.
- Set self.flags.rebuild\_doctype\_for\_global\_search from false.
- Evaluate self.update\_custom\_fields().
- Evaluate self.set\_property\_setters().
- Evaluate self.set\_name\_translation().
- Evaluate validate\_fields\_for\_doctype(self.doc\_type).
- Evaluate check\_email\_append\_to(self).
- If self.flags.update\_db.
  - Attempt the following.
    - Evaluate Platform.db.updatedb(self.doc\_type).
  - On failure (Exception) bound to e.
    - If Platform.db.is\_db\_table\_size\_limit(e).
      - Call the validation error handler Platform.throw(translated “You have hit the row size limit on database table: {0}”.format(text in the contract), title = translated “Database Table Row Size Limit”).
    - Propagate the active failure.
- If (not hasattr(self, “hide\_success”) or not self.hide\_success).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(self, “hide\_success”) → not self.hide\_success.
  - Evaluate Platform.msgprint(translated “{0} updated”.format(translated self.doc\_type), alert = true).
- Evaluate Platform.clear\_cache(doctype = self.doc\_type).
- Evaluate self.fetch\_to\_customize().
- If self.flags.rebuild\_doctype\_for\_global\_search.
  - Evaluate Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = self.doc\_type, enqueue\_after\_commit = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update custom fields](operations-016.md#op-682d0e7cac71e0), [set property setters](operations-016.md#op-90f58eedb6cefd), [set name translation](operations-016.md#op-392598429566a5), [fetch to customize](operations-016.md#op-3f872e4720ee3f).

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = self.doc\_type, enqueue\_after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L71) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L970)

<a id="op-90f58eedb6cefd"></a>
### Customize Form.set property setters

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_set_property_setters`

**Inputs** self.

**Local steps**

- Set meta from Platform.get\_meta(self.doc\_type).
- Evaluate self.set\_property\_setters\_for\_doctype(meta).
- For each df in self.get(“fields”).
  - Set meta\_df from meta.get(“fields”, mapping(“fieldname” → df.fieldname)).
  - If (not meta\_df or not is\_standard\_or\_system\_generated\_field(meta\_df at 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta\_df → not is\_standard\_or\_system\_generated\_field(meta\_df at 0).
    - Continue with the next iteration or loop test.
  - Evaluate self.set\_property\_setters\_for\_docfield(meta, df, meta\_df).
- Evaluate self.set\_property\_setters\_for\_actions\_and\_links(meta).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set property setters for doctype](operations-016.md#op-3cdcf32588a4b1), [set property setters for docfield](operations-016.md#op-fe9a3927a6a65b), [set property setters for actions and links](operations-016.md#op-4a8df135c488cb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L2309) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L973)

<a id="op-8bd91a033df8b6"></a>
### Customize Form.set property setter for field order

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_set_property_setter_for_field_order`

**Inputs** self, meta.

**Explicit results** no value.

**Local steps**

- Set new\_order from list of df.fieldname for df drawn from self.fields.
  - Draw df from self.fields.
- Set existing\_order from getattr(meta, “field\_order”, no value).
- Set default\_order from list of fieldname for tuple(fieldname, df) drawn from meta.\_fields.items() where not getattr(df, “is\_custom\_field”, false).
  - Draw tuple(fieldname, df) from meta.\_fields.items(), keep a combination only if (not getattr(df, “is\_custom\_field”, false)).
- If new\_order equals default\_order.
  - If existing\_order.
    - Evaluate delete\_property\_setter(self.doc\_type, “field\_order”).
  - Return no value.
- If (existing\_order and new\_order equals json.loads(existing\_order)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing\_order → new\_order equals json.loads(existing\_order).
  - Return no value.
- Evaluate Platform.make\_property\_setter(mapping(“doctype” → self.doc\_type, “doctype\_or\_field” → “DocType”, “property” → “field\_order”, “value” → json.dumps(new\_order)), is\_system\_generated = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(meta, “field\_order”, no value), getattr(df, “is\_custom\_field”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L2604) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L972)

<a id="op-3cdcf32588a4b1"></a>
### Customize Form.set property setters for doctype

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_set_property_setters_for_record_type`

**Inputs** self, meta.

**Local steps**

- If self.get(“show\_name\_in\_global\_search”) differs from meta.get(“show\_name\_in\_global\_search”).
  - Set self.flags.rebuild\_doctype\_for\_global\_search from true.
- For each tuple(prop, prop\_type) in doctype\_properties.items().
  - If self.get(prop) differs from meta.get(prop).
    - Evaluate self.make\_property\_setter(prop, self.get(prop), prop\_type).
- Evaluate self.set\_property\_setter\_for\_field\_order(meta).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make property setter](operations-017.md#op-55a98050d46882), [set property setter for field order](operations-016.md#op-8bd91a033df8b6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L3046) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L976)

<a id="op-fe9a3927a6a65b"></a>
### Customize Form.set property setters for docfield

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_set_property_setters_for_record_field`

**Inputs** self, meta, df, meta\_df.

**Local steps**

- For each tuple(prop, prop\_type) in docfield\_properties.items().
  - If (prop differs from “idx” and (df.get(prop) or empty text) differs from (meta\_df at 0.get(prop) or empty text)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop differs from “idx” → (df.get(prop) or empty text) differs from (meta\_df at 0.get(prop) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(prop) → empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta\_df at 0.get(prop) → empty text.
    - If not self.allow\_property\_change(prop, meta\_df, df, meta).
      - Continue with the next iteration or loop test.
    - Evaluate self.make\_property\_setter(prop, df.get(prop), prop\_type, fieldname = df.fieldname).

If control reaches the end, it returns no value.

**Methods declared on this owner** [allow property change](operations-016.md#op-dacf0aba065832), [make property setter](operations-017.md#op-55a98050d46882).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L3330) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L975)

<a id="op-dacf0aba065832"></a>
### Customize Form.allow property change

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_allow_property_change`

**Inputs** self, prop, meta\_df, df, meta.

**Record and data access** read “DocField” via get\_value.

**State and service calls** msgprint with translated “Row {0}: Not allowed to enable Allow on Submit for standard fields”.format(df.idx) · msgprint with translated “Row {0}: Not allowed to disable Mandatory for standard fields”.format(df.idx) · msgprint with translated “'In List View' not allowed for type {0} in row {1}”.format(df.fieldtype, df.idx) · msgprint with translated “You cannot unset 'Read Only' for field {0}”.format(df.label) · msgprint with translated “You can't set 'Options' for field {0}”.format(df.label) · 2 additional forms in the steps below.

**Explicit results** false · true.

**Local steps**

- If prop equals “fieldtype”.
  - Evaluate self.validate\_fieldtype\_change(df, meta\_df at 0.get(prop), df.get(prop)).
- Otherwise.
  - If prop equals “length”.
    - Set old\_value\_length from cint(meta\_df at 0.get(prop)).
    - Set new\_value\_length from cint(df.get(prop)).
    - If (new\_value\_length and old\_value\_length &gt; new\_value\_length).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_value\_length → old\_value\_length &gt; new\_value\_length.
      - Evaluate self.check\_length\_for\_fieldtypes.append(mapping(“df” → df, “old\_value” → meta\_df at 0.get(prop))).
      - Evaluate self.validate\_fieldtype\_length().
    - Otherwise.
      - Set self.flags.update\_db from true.
  - Otherwise.
    - If (prop equals “allow\_on\_submit” and df.get(prop)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “allow\_on\_submit” → df.get(prop).
      - If not Platform.db.get\_value(“DocField”, mapping(“parent” → self.doc\_type, “fieldname” → df.fieldname), “allow\_on\_submit”).
        - Evaluate Platform.msgprint(translated “Row {0}: Not allowed to enable Allow on Submit for standard fields”.format(df.idx)).
        - Return false.
    - Otherwise.
      - If (prop equals “reqd” and (Platform.db.get\_value(“DocField”, mapping(“parent” → self.doc\_type, “fieldname” → df.fieldname), “reqd”) equals 1 and df.get(prop) equals 0)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “reqd” → (Platform.db.get\_value(“DocField”, mapping(“parent” → self.doc\_type, “fieldname” → df.fieldname), “reqd”) equals 1 and df.get(prop) equals 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_value(“DocField”, mapping(“parent” → self.doc\_type, “fieldname” → df.fieldname), “reqd”) equals 1 → df.get(prop) equals 0.
        - Evaluate Platform.msgprint(translated “Row {0}: Not allowed to disable Mandatory for standard fields”.format(df.idx)).
        - Return false.
      - Otherwise.
        - If (prop equals “in\_list\_view” and df.get(prop) and df.fieldtype belongs to get\_fields\_not\_allowed\_in\_list\_view(meta)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “in\_list\_view” → df.get(prop) → df.fieldtype belongs to get\_fields\_not\_allowed\_in\_list\_view(meta).
          - Evaluate Platform.msgprint(translated “'In List View' not allowed for type {0} in row {1}”.format(df.fieldtype, df.idx)).
          - Return false.
        - Otherwise.
          - If (prop equals “precision” and cint(df.get(“precision”)) &gt; 6 and cint(df.get(“precision”)) &gt; cint(meta\_df at 0.get(“precision”))).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “precision” → cint(df.get(“precision”)) &gt; 6 → cint(df.get(“precision”)) &gt; cint(meta\_df at 0.get(“precision”)).
            - Set self.flags.update\_db from true.
          - Otherwise.
            - If prop equals “unique”.
              - Set self.flags.update\_db from true.
            - Otherwise.
              - If (prop equals “read\_only” and cint(df.get(“read\_only”)) equals 0 and Platform.db.get\_value(“DocField”, mapping(“parent” → self.doc\_type, “fieldname” → df.fieldname), “read\_only”) equals 1).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “read\_only” → cint(df.get(“read\_only”)) equals 0 → Platform.db.get\_value(“DocField”, mapping(“parent” → self.doc\_type, “fieldname” → df.fieldname), “read\_only”) equals 1.
                - Evaluate Platform.msgprint(translated “You cannot unset 'Read Only' for field {0}”.format(df.label)).
                - Return false.
              - Otherwise.
                - If (prop equals “options” and df.get(“fieldtype”) does not belong to ALLOWED\_OPTIONS\_CHANGE).
                  - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “options” → df.get(“fieldtype”) does not belong to ALLOWED\_OPTIONS\_CHANGE.
                  - Evaluate Platform.msgprint(translated “You can't set 'Options' for field {0}”.format(df.label)).
                  - Return false.
                - Otherwise.
                  - If (prop equals “translatable” and not supports\_translation(df.get(“fieldtype”))).
                    - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “translatable” → not supports\_translation(df.get(“fieldtype”)).
                    - Evaluate Platform.msgprint(translated “You can't set 'Translatable' for field {0}”.format(df.label)).
                    - Return false.
                  - Otherwise.
                    - If (prop equals “in\_global\_search” and df.in\_global\_search differs from meta\_df at 0.get(“in\_global\_search”)).
                      - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “in\_global\_search” → df.in\_global\_search differs from meta\_df at 0.get(“in\_global\_search”).
                      - Set self.flags.rebuild\_doctype\_for\_global\_search from true.
                    - Otherwise.
                      - If (prop equals “is\_virtual” and meta\_df at 0.get(“is\_virtual”) equals 0 and df.get(“is\_virtual”) equals 1).
                        - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop equals “is\_virtual” → meta\_df at 0.get(“is\_virtual”) equals 0 → df.get(“is\_virtual”) equals 1.
                        - Evaluate Platform.msgprint(translated “You can't set standard field {0} as virtual”.format(Platform.bold(df.label))).
                        - Return false.
- Return true.

**Methods declared on this owner** [validate fieldtype change](operations-017.md#op-3232a44d6881e5), [validate fieldtype length](operations-017.md#op-df97c0a32c22f5).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0124.json#L3636) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L957)

<a id="op-4a8df135c488cb"></a>
### Customize Form.set property setters for actions and links

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_set_property_setters_for_actions_and_links`

**Inputs** self, meta.

**Record and data access** read doctype via exists · resolve a document from doctype via get\_doc.

**State and service calls** call save on d.

**Local steps**

- For each tuple(doctype, fieldname, field\_map) in tuple(tuple(“DocType Link”, “links”, doctype\_link\_properties), tuple(“DocType Action”, “actions”, doctype\_action\_properties), tuple(“DocType State”, “states”, doctype\_state\_properties)).
  - Set has\_custom from false.
  - Set items from list().
  - For each tuple(i, d) in enumerate((self.get(fieldname) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(fieldname) → list().
    - Set d.idx from i.
    - If (Platform.db.exists(doctype, d.name) and not d.custom).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.exists(doctype, d.name) → not d.custom.
      - Set original from Platform.get\_doc(doctype, d.name).
      - For each tuple(prop, prop\_type) in field\_map.items().
        - If d.get(prop) differs from original.get(prop).
          - Evaluate self.make\_property\_setter(prop, d.get(prop), prop\_type, apply\_on = doctype, row\_name = d.name).
      - Evaluate items.append(d.name).
    - Otherwise.
      - Set d.parent from self.doc\_type.
      - Set d.custom from 1.
      - Evaluate d.save(ignore\_permissions = true).
      - Set has\_custom from true.
      - Evaluate items.append(d.name).
  - Evaluate self.update\_order\_property\_setter(has\_custom, fieldname).
  - Evaluate self.clear\_removed\_items(doctype, items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make property setter](operations-017.md#op-55a98050d46882), [update order property setter](operations-016.md#op-8a36918a8b3850), [clear removed items](operations-016.md#op-214a63c48c2d73).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L974)

<a id="op-8a36918a8b3850"></a>
### Customize Form.update order property setter

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_update_order_property_setter`

**Inputs** self, has\_custom, fieldname.

**Local steps**

- Set property\_name from formatted text {fieldname}\_order.
- If has\_custom.
  - Evaluate self.make\_property\_setter(property\_name, json.dumps(list of d.name for d drawn from self.get(fieldname)), “Small Text”).
    - Draw d from self.get(fieldname).
- Otherwise.
  - Evaluate delete\_property\_setter(self.doc\_type, property = property\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make property setter](operations-017.md#op-55a98050d46882).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L720) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L980)

<a id="op-214a63c48c2d73"></a>
### Customize Form.clear removed items

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_clear_removed_items`

**Inputs** self, doctype, items.

**State and service calls** request delete on doctype.

**Local steps**

- If items.
  - Evaluate Platform.db.delete(doctype, dict(parent = self.doc\_type, custom = 1, name = tuple(“not in”, items))).
- Otherwise.
  - Evaluate Platform.db.delete(doctype, dict(parent = self.doc\_type, custom = 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L931) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L959)

<a id="op-682d0e7cac71e0"></a>
### Customize Form.update custom fields

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_update_custom_fields`

**Inputs** self.

**Record and data access** read “Custom Field” via exists.

**Local steps**

- For each tuple(i, df) in enumerate(self.get(“fields”)).
  - If is\_standard\_or\_system\_generated\_field(df).
    - Continue with the next iteration or loop test.
  - If not Platform.db.exists(“Custom Field”, mapping(“dt” → self.doc\_type, “fieldname” → df.fieldname)).
    - Evaluate self.add\_custom\_field(df, i).
    - Set self.flags.update\_db from true.
  - Otherwise.
    - Evaluate self.update\_in\_custom\_field(df, i).
- Evaluate self.delete\_custom\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add custom field](operations-016.md#op-66faed7d954a09), [update in custom field](operations-016.md#op-c3635054f6a7c5), [delete custom fields](operations-016.md#op-718115b6ac51e1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L1125) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L978)

<a id="op-66faed7d954a09"></a>
### Customize Form.add custom field

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_add_custom_field`

**Inputs** self, df, i.

**State and service calls** request new\_doc for “Custom Field” · call insert on d.

**Local steps**

- Set d from Platform.new\_doc(“Custom Field”).
- Set d.dt from self.doc\_type.
- For each prop in docfield\_properties.
  - Evaluate d.set(prop, df.get(prop)).
- If i differs from 0.
  - Set d.insert\_after from self.fields at (i − 1).fieldname.
- Set d.idx from i.
- Evaluate d.insert().
- Set df.fieldname from d.fieldname.
- If df.get(“in\_global\_search”).
  - Set self.flags.rebuild\_doctype\_for\_global\_search from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L1425) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L954)

<a id="op-c3635054f6a7c5"></a>
### Customize Form.update in custom field

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_update_in_custom_field`

**Inputs** self, df, i.

**Record and data access** resolve a document from “Custom Field” via get\_doc.

**State and service calls** call db\_update on custom\_field.

**Explicit results** no value.

**Local steps**

- Set meta from Platform.get\_meta(self.doc\_type).
- Set meta\_df from meta.get(“fields”, mapping(“fieldname” → df.fieldname)).
- If (not meta\_df or is\_standard\_or\_system\_generated\_field(meta\_df at 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta\_df → is\_standard\_or\_system\_generated\_field(meta\_df at 0).
  - Return no value.
- Set custom\_field from Platform.get\_doc(“Custom Field”, meta\_df at 0.name).
- Set changed from false.
- For each prop in docfield\_properties.
  - If df.get(prop) differs from custom\_field.get(prop).
    - If prop equals “fieldtype”.
      - Evaluate self.validate\_fieldtype\_change(df, meta\_df at 0.get(prop), df.get(prop)).
    - If prop equals “in\_global\_search”.
      - Set self.flags.rebuild\_doctype\_for\_global\_search from true.
    - Evaluate custom\_field.set(prop, df.get(prop)).
    - Set changed from true.
- If i differs from 0.
  - Set insert\_after from self.fields at (i − 1).fieldname.
  - If custom\_field.insert\_after differs from insert\_after.
    - Set custom\_field.insert\_after from insert\_after.
    - Set custom\_field.idx from i.
    - Set changed from true.
- If changed.
  - Evaluate custom\_field.db\_update().
  - Set self.flags.update\_db from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate fieldtype change](operations-017.md#op-3232a44d6881e5).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L1754) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L979)

<a id="op-718115b6ac51e1"></a>
### Customize Form.delete custom fields

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_delete_custom_fields`

**Inputs** self.

**State and service calls** request delete\_doc for “Custom Field”.

**Local steps**

- Set meta from Platform.get\_meta(self.doc\_type).
- Set fields\_to\_remove from (set of df.fieldname for df drawn from meta.get(“fields”) − set of df.fieldname for df drawn from self.get(“fields”)).
  - Draw df from meta.get(“fields”).
  - Draw df from self.get(“fields”).
- For each fieldname in fields\_to\_remove.
  - Set df from meta.get(“fields”, mapping(“fieldname” → fieldname)) at 0.
  - If not is\_standard\_or\_system\_generated\_field(df).
    - Evaluate Platform.delete\_doc(“Custom Field”, df.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L2459) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L961)
