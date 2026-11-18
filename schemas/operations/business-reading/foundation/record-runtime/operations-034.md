# Record lifecycle and persistence · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Docstatus

<a id="op-43d74c546a361f"></a>
### Doc Status.is cancelled

`operation_foundation_model_record_state_business_behavior_record_status_is_cancelled`

**Inputs** self.

**Explicit results** self equals DocStatus.CANCELLED.

**Local steps**

- Return self equals DocStatus.CANCELLED.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3781) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1269)

<a id="op-43e87ce8817cb7"></a>
### Doc Status.draft

`operation_foundation_model_record_state_business_behavior_record_status_draft`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** DocStatus.DRAFT.

**Local steps**

- Return DocStatus.DRAFT.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3834) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1268)

<a id="op-3fc056ed3c117e"></a>
### Doc Status.submitted

`operation_foundation_model_record_state_business_behavior_record_status_submitted`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** DocStatus.SUBMITTED.

**Local steps**

- Return DocStatus.SUBMITTED.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3872) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1272)

<a id="op-1fc9b1f008ca6e"></a>
### Doc Status.cancelled

`operation_foundation_model_record_state_business_behavior_record_status_cancelled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** DocStatus.CANCELLED.

**Local steps**

- Return DocStatus.CANCELLED.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3910) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L682) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1267)

## Record · Doctype

<a id="op-ee946a35ee6aab"></a>
### Doc Type.before insert

`operation_foundation_binding_foundation_core_doctype_doctype_doctype_doctype_before_insert`

**Inputs** self.

**Local steps**

- If (not self.istable and not self.permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.istable → not self.permissions.
  - Evaluate self.append(“permissions”, mapping(“role” → “System Manager”, “read” → 1, “write” → 1, “create” → 1, …)).
    - Value choice on self.is\_submittable — true gives 1, false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L625)

<a id="op-5afd306a54a959"></a>
### Doc Type.validate

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate`

**Inputs** self.

**Record and data access** resolve a document from “DocType” via get\_doc.

**Explicit failure paths** validation helper — translated “Standard DocType cannot have default print format, use Customize Form”.

**Local steps**

- Evaluate self.check\_developer\_mode().
- Evaluate self.validate\_name().
- Evaluate self.set\_defaults\_for\_single\_and\_table().
- Evaluate self.scrub\_field\_names().
- Evaluate self.set\_default\_in\_list\_view().
- Evaluate self.set\_default\_translatable().
- Evaluate validate\_series(self).
- Evaluate self.set(“can\_change\_name\_type”, validate\_autoincrement\_autoname(self)).
- Evaluate self.validate\_document\_type().
- Evaluate validate\_fields(self).
- Evaluate self.check\_indexing\_for\_dashboard\_links().
- If not self.istable.
  - Evaluate validate\_permissions(self).
- Evaluate self.make\_amendable().
- Evaluate self.make\_repeatable().
- Evaluate self.validate\_nestedset().
- Evaluate self.validate\_child\_table().
- Evaluate self.validate\_website().
- Evaluate self.validate\_virtual\_doctype\_methods().
- Evaluate self.ensure\_minimum\_max\_attachment\_limit().
- Evaluate self.patch\_old\_naming\_expressions().
- Evaluate validate\_links\_table\_fieldnames(self).
- If not self.is\_new().
  - Set self.before\_update from Platform.get\_doc(“DocType”, self.name).
  - Evaluate self.setup\_fields\_to\_fetch().
  - Evaluate self.validate\_field\_name\_conflicts().
- Evaluate check\_email\_append\_to(self).
- If (self.default\_print\_format and not self.custom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default\_print\_format → not self.custom.
  - Call the validation error handler Platform.throw(translated “Standard DocType cannot have default print format, use Customize Form”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check developer mode](operations-034.md#op-cd0b255feb1d3c), [validate name](operations-036.md#op-c7b7ed98a2240f), [set defaults for single and table](operations-034.md#op-b93adca367c4e7), [scrub field names](operations-034.md#op-b690188a3be8d5), [set default in list view](operations-034.md#op-486b166f44cd1f), [set default translatable](operations-034.md#op-af1356e083796c), [validate document type](operations-034.md#op-dd928ef4450290), [check indexing for dashboard links](operations-034.md#op-1f33fb42a2f2fb), [make amendable](operations-035.md#op-c7081c8a34b972), [make repeatable](operations-035.md#op-bcf4108e63df64), [validate nestedset](operations-035.md#op-ced048c6b68b73), [validate child table](operations-035.md#op-41937365169297), [validate website](operations-034.md#op-96e90ef9704a14), [validate virtual doctype methods](operations-034.md#op-d4a8a980b54d0a), [ensure minimum max attachment limit](operations-034.md#op-d2748a720d833d), [patch old naming expressions](operations-034.md#op-4ee874604ccb65), [setup fields to fetch](operations-034.md#op-5a4a0cc807fee4), [validate field name conflicts](operations-034.md#op-ad176a8c97e019).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L114) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1996) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L181)

<a id="op-ad176a8c97e019"></a>
### Doc Type.validate field name conflicts

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate_field_name_conflicts`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Fieldname '{0}' conflicting with a {1} of the name {2} in {3}”.format(field\_label, conflict\_type, field, self.name).

**Local steps**

- Set core\_doctypes from list(“Custom DocPerm”, “DocPerm”, “Custom Field”, “Customize Form Field”, …).
- If self.name belongs to core\_doctypes.
  - Return no value.
- Attempt the following.
  - Set controller from get\_controller(self.name).
- On failure (ImportError).
  - Set controller from Document.
- Set available\_objects from set of x for x drawn from dir(controller) where isinstance(x, str).
  - Draw x from dir(controller), keep a combination only if (isinstance(x, str)).
- Set property\_set from set of x for x drawn from available\_objects where is\_a\_property(getattr(controller, x, no value)).
  - Draw x from available\_objects, keep a combination only if (is\_a\_property(getattr(controller, x, no value))).
- Set method\_set from set of x for x drawn from available\_objects where (x does not belong to property\_set and callable(getattr(controller, x, no value))).
  - Draw x from available\_objects, keep a combination only if ((x does not belong to property\_set and callable(getattr(controller, x, no value)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in x does not belong to property\_set → callable(getattr(controller, x, no value)).
- For each docfield in (self.get(“fields”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“fields”) → list().
  - If docfield.fieldtype belongs to no\_value\_fields.
    - Continue with the next iteration or loop test.
  - Set conflict\_type from no value.
  - Set field from docfield.fieldname.
  - Set field\_label from (docfield.label or docfield.fieldname).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in docfield.label → docfield.fieldname.
  - If docfield.fieldname belongs to method\_set.
    - Set conflict\_type from “controller method”.
  - If (docfield.fieldname belongs to property\_set and not docfield.is\_virtual).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.fieldname belongs to property\_set → not docfield.is\_virtual.
    - Set conflict\_type from “class property”.
  - If conflict\_type.
    - Call the validation error handler Platform.throw(translated “Fieldname '{0}' conflicting with a {1} of the name {2} in {3}”.format(field\_label, conflict\_type, field, self.name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from get\_controller(self.name), getattr(controller, x, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L3751) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1999) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L184)

<a id="op-b93adca367c4e7"></a>
### Doc Type.set defaults for single and table

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_set_defaults_for_single_and_table`

**Inputs** self.

**Local steps**

- If self.issingle.
  - Set self.allow\_import from 0.
  - Set self.allow\_rename from 0.
  - Set self.is\_submittable from 0.
  - Set self.istable from 0.
- Otherwise.
  - If self.istable.
    - Set self.allow\_import from 0.
    - Set self.permissions from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L113) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1990) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L175)

<a id="op-486b166f44cd1f"></a>
### Doc Type.set default in list view

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_set_default_in_list_view`

**Inputs** self.

**Local steps**

- Set not\_allowed\_in\_list\_view from get\_fields\_not\_allowed\_in\_list\_view(self.meta).
- If not list of d.fieldname for d drawn from self.fields where d.in\_list\_view.
  - Draw d from self.fields, keep a combination only if (d.in\_list\_view).
  - Set cnt from 0.
  - For each d in self.fields.
    - If (d.reqd and not d.hidden and d.fieldtype does not belong to not\_allowed\_in\_list\_view).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reqd → not d.hidden → d.fieldtype does not belong to not\_allowed\_in\_list\_view.
      - Set d.in\_list\_view from 1.
      - Update cnt using + 1.
      - If cnt equals 4.
        - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L4630) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1988) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L173)

<a id="op-af1356e083796c"></a>
### Doc Type.set default translatable

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_set_default_translatable`

**Inputs** self.

**Local steps**

- For each d in self.fields.
  - If (d.translatable and not supports\_translation(d.fieldtype)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.translatable → not supports\_translation(d.fieldtype).
    - Set d.translatable from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L4881) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1989) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L174)

<a id="op-1f33fb42a2f2fb"></a>
### Doc Type.check indexing for dashboard links

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_check_indexing_for_dashboard_links`

**Inputs** self.

**Record and data access** read “DocType Link” via exists.

**State and service calls** msgprint with translated “{0} should be indexed because it's referred in dashboard connections”.format(\_(d.label, context = d.parent)).

**Local steps**

- For each d in self.fields.
  - If (d.fieldtype equals “Link” and not d.unique and not d.search\_index).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype equals “Link” → not d.unique → not d.search\_index.
    - Set referred\_as\_link from Platform.db.exists(“DocType Link”, mapping(“parent” → d.options, “link\_doctype” → self.name, “link\_fieldname” → d.fieldname)).
    - If not referred\_as\_link.
      - Continue with the next iteration or loop test.
    - Evaluate Platform.msgprint(translated “{0} should be indexed because it's referred in dashboard connections”.format(\_(d.label, context = d.parent)), alert = true, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L4994) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L153)

<a id="op-cd0b255feb1d3c"></a>
### Doc Type.check developer mode

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_check_developer_mode`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with CannotCreateStandardDoctypeError — translated “Not in Developer Mode! Set in site\_config.json or make 'Custom' DocType.” · validation helper with CannotCreateStandardDoctypeError — translated “Not allowed to create custom Virtual DocType.”.

**Local steps**

- If (Platform.flags.in\_patch or Platform.in\_test).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_patch → Platform.in\_test.
  - Return no value.
- If (not Platform.conf.get(“developer\_mode”) and not self.custom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.get(“developer\_mode”) → not self.custom.
  - Call the validation error handler Platform.throw(translated “Not in Developer Mode! Set in site\_config.json or make 'Custom' DocType.”, CannotCreateStandardDoctypeError).
- If (self.is\_virtual and self.custom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_virtual → self.custom.
  - Call the validation error handler Platform.throw(translated “Not allowed to create custom Virtual DocType.”, CannotCreateStandardDoctypeError).
- If (Platform.conf.developer\_mode and not self.owner).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → not self.owner.
  - Set self.owner from “Administrator”.
  - Set self.modified\_by from “Administrator”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L5333) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L152)

<a id="op-5a4a0cc807fee4"></a>
### Doc Type.setup fields to fetch

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_setup_fields_to_fetch`

**Inputs** self.

**Record and data access** resolve a document from “DocType” via get\_doc.

**Local steps**

- Attempt the following.
  - Set old\_meta from Platform.get\_meta(Platform.get\_doc(“DocType”, self.name), cached = false).
  - Set old\_fields\_to\_fetch from list of df.fieldname for df drawn from old\_meta.get\_fields\_to\_fetch().
    - Draw df from old\_meta.get\_fields\_to\_fetch().
- On failure (Platform.DoesNotExistError).
  - Set old\_fields\_to\_fetch from list().
- Set new\_meta from Platform.get\_meta(self, cached = false).
- Set self.flags.update\_fields\_to\_fetch\_queries from list().
- Set new\_fields\_to\_fetch from new\_meta.get\_fields\_to\_fetch().
- If set(old\_fields\_to\_fetch) differs from set of df.fieldname for df drawn from new\_fields\_to\_fetch.
  - Draw df from new\_fields\_to\_fetch.
  - For each df in new\_fields\_to\_fetch.
    - If df.fieldname does not belong to old\_fields\_to\_fetch.
      - Set tuple(link\_fieldname, source\_fieldname) from df.fetch\_from.split(“.”, 1).
      - If not source\_fieldname.
        - Continue with the next iteration or loop test.
      - Set link\_df from new\_meta.get\_field(link\_fieldname).
      - If Platform.db.db\_type equals “mariadb”.
        - Set update\_query from multiline text in the contract.
        - If df.not\_nullable.
          - Update update\_query using + “WHERE ′target′.′{fieldname}′=''”.
        - Otherwise.
          - Update update\_query using + “WHERE ifnull(′target′.′{fieldname}′, '')=''”.
      - Otherwise.
        - Set update\_query from query text (UPDATE).
        - If df.not\_nullable.
          - Update update\_query using + “AND ′{fieldname}′=''”.
        - Otherwise.
          - Update update\_query using + “AND ifnull(′{fieldname}′, '')=''”.
      - Evaluate self.flags.update\_fields\_to\_fetch\_queries.append(update\_query.format(link\_doctype = link\_df.options, source\_fieldname = source\_fieldname, doctype = self.name, fieldname = df.fieldname, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L5637) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1992) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L177)

<a id="op-6d7f7cf63b054b"></a>
### Doc Type.update fields to fetch

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_update_fields_to_fetch`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Local steps**

- If (self.flags.update\_fields\_to\_fetch\_queries and not self.issingle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags.update\_fields\_to\_fetch\_queries → not self.issingle.
  - For each query in self.flags.update\_fields\_to\_fetch\_queries.
    - Evaluate Platform.db.sql(query).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L6475) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1995) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L180)

<a id="op-dd928ef4450290"></a>
### Doc Type.validate document type

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate_document_type`

**Inputs** self.

**Local steps**

- If self.document\_type equals “Transaction”.
  - Set self.document\_type from “Document”.
- If self.document\_type equals “Master”.
  - Set self.document\_type from “Setup”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L6592) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1998) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L183)

<a id="op-96e90ef9704a14"></a>
### Doc Type.validate website

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate_website`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Field "route" is mandatory for Web Views”.

**Local steps**

- If self.route.
  - Set self.route from self.route.strip(“/”).
- If self.has\_web\_view.
  - If “route” does not belong to list of d.fieldname for d drawn from self.fields.
    - Draw d from self.fields.
    - Call the validation error handler Platform.throw(translated “Field "route" is mandatory for Web Views”, title = “Missing Field”).
  - Evaluate clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L6708) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2003) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L188)

<a id="op-d4a8a980b54d0a"></a>
### Doc Type.validate virtual doctype methods

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate_virtual_record_type_methods`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.get(“is\_virtual”) or self.is\_new()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“is\_virtual”) → self.is\_new().
  - Return no value.
- Bind dependencies validate\_controller.
- Evaluate validate\_controller(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L6924) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2002) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L187)

<a id="op-d2748a720d833d"></a>
### Doc Type.ensure minimum max attachment limit

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_ensure_minimum_maximum_attachment_limit`

**Inputs** self.

**State and service calls** msgprint with translated “Number of attachment fields are more than {}, limit updated to {}.”.format(field\_label, total\_attach\_fields).

**Explicit results** no value.

**Local steps**

- Bind dependencies attachment\_fieldtypes.
- If not self.max\_attachments.
  - Return no value.
- Set total\_attach\_fields from len(list of d for d drawn from self.fields where d.fieldtype belongs to attachment\_fieldtypes).
  - Draw d from self.fields, keep a combination only if (d.fieldtype belongs to attachment\_fieldtypes).
- If total\_attach\_fields &gt; self.max\_attachments.
  - Set self.max\_attachments from total\_attach\_fields.
  - Set field\_label from Platform.bold(self.meta.get\_field(“max\_attachments”).label).
  - Evaluate Platform.msgprint(translated “Number of attachment fields are more than {}, limit updated to {}.”.format(field\_label, total\_attach\_fields), title = translated “Insufficient attachment limit”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0062.json#L7052) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L156)

<a id="op-4ee874604ccb65"></a>
### Doc Type.patch old naming expressions

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_patch_old_naming_expressions`

**Inputs** self.

**State and service calls** toast with translated “Warning: Usage of 'format:' is discouraged.”.

**Explicit results** no value.

**Local steps**

- If not self.autoname.
  - Return no value.
- If (self.autoname and self.autoname.startswith(“format:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.autoname → self.autoname.startswith(“format:”).
  - Set self.naming\_rule from “Expression (old style)”.
  - Evaluate Platform.toast(translated “Warning: Usage of 'format:' is discouraged.”, indicator = “yellow”).
- If (self.naming\_rule equals “Expression (old style)” and not self.autoname.startswith(“format:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.naming\_rule equals “Expression (old style)” → not self.autoname.startswith(“format:”).
  - Set self.naming\_rule from “Expression”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L165)

<a id="op-954d55f1540d1f"></a>
### Doc Type.change modified of parent

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_change_modified_of_parent`

**Inputs** self.

**Record and data access** read “DocField” via get\_all.

**State and service calls** request set\_value on “DocType”.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_import.
  - Return no value.
- Set parent\_list from Platform.get\_all(“DocField”, “parent”, dict(fieldtype = list(“in”, Platform.model.table\_fields), options = self.name)).
- For each p in parent\_list.
  - Evaluate Platform.db.set\_value(“DocType”, p.parent, mapping()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L249) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L151)

<a id="op-b690188a3be8d5"></a>
### Doc Type.scrub field names

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_scrub_field_names`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{}: Fieldname is required”.format(d.idx) · validation helper with InvalidFieldNameError — translated “Fieldname {0} is restricted”.format(d.fieldname).

**Local steps**

- Set restricted from tuple(“name”, “parent”, “creation”, “owner”, …).
- For each d in self.get(“fields”).
  - If d.fieldtype.
    - If not getattr(d, “fieldname”, no value).
      - If d.label.
        - Set d.fieldname from nested operand in the contract().lower().replace(one space, “\_”).strip(“?”).
        - If d.fieldname belongs to restricted.
          - Set d.fieldname from (d.fieldname + “1”).
        - If d.fieldtype equals “Section Break”.
          - Set d.fieldname from (d.fieldname + “\_section”).
        - Otherwise.
          - If d.fieldtype equals “Column Break”.
            - Set d.fieldname from (d.fieldname + “\_column”).
          - Otherwise.
            - If d.fieldtype equals “Tab Break”.
              - Set d.fieldname from (d.fieldname + “\_tab”).
      - Otherwise.
        - If d.fieldtype belongs to tuple(“Section Break”, “Column Break”, “Tab Break”).
          - Set d.fieldname from ((nested operand in the contract.fieldtype.lower().replace(one space, “\_”) + “\_”) + str(random\_string(4))).
        - Otherwise.
          - Call the validation error handler Platform.throw(translated “Row #{}: Fieldname is required”.format(d.idx), title = “Missing Fieldname”).
    - Otherwise.
      - If d.fieldname belongs to restricted.
        - Call the validation error handler Platform.throw(translated “Fieldname {0} is restricted”.format(d.fieldname), InvalidFieldNameError).
    - Set d.fieldname from ILLEGAL\_FIELDNAME\_PATTERN.sub(empty text, d.fieldname).
    - Set d.fieldname from d.fieldname.lower().
  - If d.unique.
    - Set d.search\_index from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(d, “fieldname”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L464) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1986) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L171)

<a id="op-0fe1dfd79117e6"></a>
### Doc Type.get permission log options

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L1399) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L160)

<a id="op-1ef7631010f353"></a>
### Doc Type.on update

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_on_update`

**Inputs** self.

**Explicit failure paths** e.

**Local steps**

- If self.get(“can\_change\_name\_type”).
  - Evaluate self.setup\_autoincrement\_and\_sequence().
- Attempt the following.
  - Evaluate Platform.db.updatedb(self.name, Meta(self)).
- On failure (Exception) bound to e.
  - Evaluate print(formatted text   There was an issue while migrating the DocType: {self.name} ).
  - Raise e.
- Evaluate self.change\_modified\_of\_parent().
- Evaluate make\_module\_and\_roles(self).
- Evaluate self.update\_fields\_to\_fetch().
- Set allow\_doctype\_export from (not self.custom and not Platform.flags.in\_import and (Platform.conf.developer\_mode or Platform.flags.allow\_doctype\_export)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.custom → not Platform.flags.in\_import → (Platform.conf.developer\_mode or Platform.flags.allow\_doctype\_export).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.flags.allow\_doctype\_export.
- If allow\_doctype\_export.
  - Evaluate self.warn\_on\_module\_change().
  - Evaluate self.export\_doc().
  - Evaluate self.make\_controller\_template().
  - Evaluate self.set\_base\_class\_for\_controller().
  - Evaluate self.export\_types\_to\_controller().
- If not self.custom.
  - Evaluate self.run\_module\_method(“on\_doctype\_update”).
  - If self.flags.in\_insert.
    - Evaluate self.run\_module\_method(“after\_doctype\_insert”).
- Evaluate self.sync\_doctype\_layouts().
- Evaluate delete\_notification\_count\_for(doctype = self.name).
- Evaluate Platform.clear\_cache(doctype = self.name).
- Evaluate clear\_user\_cache(Platform.session.user).
- If (not Platform.flags.in\_install and hasattr(self, “before\_update”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.in\_install → hasattr(self, “before\_update”).
  - Evaluate self.sync\_global\_search().
- Evaluate clear\_linked\_doctype\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup autoincrement and sequence](operations-035.md#op-28894e08119b08), [change modified of parent](operations-034.md#op-954d55f1540d1f), [update fields to fetch](operations-034.md#op-6d7f7cf63b054b), [warn on module change](operations-035.md#op-65a0bff2e08f62), [export doc](operations-035.md#op-6619d0144a4ce4), [make controller template](operations-035.md#op-7f23a6b3fd0aeb), [set base class for controller](operations-035.md#op-2d7240f9534ddf), [export types to controller](operations-035.md#op-615898841779cb), [run module method](operations-035.md#op-0e7d7f4493c513), [sync doctype layouts](operations-034.md#op-b52997551b0a00), [sync global search](operations-035.md#op-ad2dbc1ae0f962).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L112) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1977) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L164)

<a id="op-b52997551b0a00"></a>
### Doc Type.sync doctype layouts

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_sync_record_type_layouts`

**Inputs** self.

**Wrappers, in declaration order** savepoint(catch = Exception).

**Record and data access** read “DocType Layout” via get\_all · resolve a document from “DocType Layout” via get\_doc.

**State and service calls** call save on layout\_doc.

**Local steps**

- Set doctype\_layouts from Platform.get\_all(“DocType Layout”, filters = mapping(“document\_type” → self.name), pluck = “name”, ignore\_ddl = true).
- For each layout in doctype\_layouts.
  - Set layout\_doc from Platform.get\_doc(“DocType Layout”, layout).
  - Evaluate layout\_doc.sync\_fields().
  - Evaluate layout\_doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L2699) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1994) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L179)
