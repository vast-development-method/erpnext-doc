# Record lifecycle and persistence · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Doctype

<a id="op-28894e08119b08"></a>
### Doc Type.setup autoincrement and sequence

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_setup_autoincrement_and_sequence`

**Inputs** self.

**Local steps**

- Set name\_type from formatted text varchar({Platform.db.VARCHAR\_LEN}).
- If self.autoname equals “autoincrement”.
  - Set name\_type from “bigint”.
  - Evaluate Platform.db.create\_sequence(self.name, check\_not\_exists = true).
- Evaluate change\_name\_column\_type(self.name, name\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L2937) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1991) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L176)

<a id="op-ad2dbc1ae0f962"></a>
### Doc Type.sync global search

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_sync_global_search`

**Inputs** self.

**State and service calls** enqueue with “Platform.utils.global\_search.rebuild\_for\_doctype”.

**Local steps**

- Set global\_search\_fields\_before\_update from list of d.fieldname for d drawn from self.before\_update.fields where d.in\_global\_search.
  - Draw d from self.before\_update.fields, keep a combination only if (d.in\_global\_search).
- If self.before\_update.show\_name\_in\_global\_search.
  - Evaluate global\_search\_fields\_before\_update.append(“name”).
- Set global\_search\_fields\_after\_update from list of d.fieldname for d drawn from self.fields where d.in\_global\_search.
  - Draw d from self.fields, keep a combination only if (d.in\_global\_search).
- If self.show\_name\_in\_global\_search.
  - Evaluate global\_search\_fields\_after\_update.append(“name”).
- If set(global\_search\_fields\_before\_update) differs from set(global\_search\_fields\_after\_update).
  - Set now from (not Platform.request or Platform.in\_test or Platform.flags.in\_install).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.request → Platform.in\_test → Platform.flags.in\_install.
  - Evaluate Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, now = now, doctype = self.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, now = now, doctype = self.name).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L3123) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1993) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L178)

<a id="op-2d7240f9534ddf"></a>
### Doc Type.set base class for controller

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_set_base_class_for_controller`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.has\_value\_changed(“has\_web\_view”).
  - Return no value.
- Set despaced\_name from self.name.replace(one space, empty text).
- Set scrubbed\_name from Platform.scrub(self.name).
- Set scrubbed\_module from Platform.scrub(self.module).
- Set controller\_path from Platform.get\_module\_path(scrubbed\_module, “doctype”, scrubbed\_name, formatted text {scrubbed\_name}.py).
- Set document\_cls\_tag from formatted text class {despaced\_name}(Document).
- Set document\_import\_tag from “from Platform.model.document import Document”.
- Set website\_generator\_cls\_tag from formatted text class {despaced\_name}(WebsiteGenerator).
- Set website\_generator\_import\_tag from “from Platform.website.website\_generator import WebsiteGenerator”.
- Within open(controller\_path) bound as f.
  - Set code from f.read().
- Set updated\_code from code.
- Set is\_website\_generator\_class from all(list(website\_generator\_cls\_tag belongs to code, website\_generator\_import\_tag belongs to code)).
- If (self.has\_web\_view and not is\_website\_generator\_class).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_web\_view → not is\_website\_generator\_class.
  - Set updated\_code from updated\_code.replace(document\_import\_tag, website\_generator\_import\_tag).replace(document\_cls\_tag, website\_generator\_cls\_tag).
- Otherwise.
  - If (not self.has\_web\_view and is\_website\_generator\_class).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_web\_view → is\_website\_generator\_class.
    - Set updated\_code from updated\_code.replace(website\_generator\_import\_tag, document\_import\_tag).replace(website\_generator\_cls\_tag, document\_cls\_tag).
- If updated\_code differs from code.
  - Within open(controller\_path, “w”) bound as f.
    - Evaluate f.write(updated\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L3527) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1987) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L172)

<a id="op-0e7d7f4493c513"></a>
### Doc Type.run module method

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_run_module_method`

**Inputs** self, method.

**Local steps**

- Bind dependencies load\_doctype\_module.
- Set module from load\_doctype\_module(self.name, self.module).
- If hasattr(module, method).
  - Evaluate getattr(module, method)().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(module, method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L4268) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1985) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L170)

<a id="op-0cdd5adafe8ee9"></a>
### Doc Type.before rename

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_before_rename`

**Inputs** self, old, new, merge = false.

**Explicit failure paths** validation helper — translated “DocType can only be renamed by Administrator” · validation helper — translated “DocType can not be merged”.

**Local steps**

- If (not self.custom and Platform.session.user differs from “Administrator”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.custom → Platform.session.user differs from “Administrator”.
  - Call the validation error handler Platform.throw(translated “DocType can only be renamed by Administrator”).
- Evaluate self.check\_developer\_mode().
- Evaluate self.validate\_name(new).
- If merge.
  - Call the validation error handler Platform.throw(translated “DocType can not be merged”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check developer mode](operations-034.md#op-cd0b255feb1d3c), [validate name](operations-036.md#op-c7b7ed98a2240f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L4411) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L150)

<a id="op-c1429513cbf964"></a>
### Doc Type.after rename

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_after_rename`

**Inputs** self, old, new, merge = false.

**State and service calls** execute query text (UPDATE, Singles) · request rename\_table on old · commit.

**Local steps**

- If self.issingle.
  - Evaluate Platform.db.sql(query text (UPDATE, Singles), tuple(new, old)).
  - Evaluate Platform.db.sql(query text (UPDATE, Singles), tuple(new, new, old)).
- Otherwise.
  - If not self.is\_virtual.
    - Evaluate Platform.db.rename\_table(old, new).
    - Evaluate Platform.db.commit().
- If not self.custom.
  - If not Platform.flags.in\_patch.
    - Evaluate self.rename\_files\_and\_folders(old, new).
  - Evaluate clear\_controller\_cache(old).

If control reaches the end, it returns no value.

**Methods declared on this owner** [rename files and folders](operations-035.md#op-2311c55937e763).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L110) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L146)

<a id="op-30f3d6f153a8e4"></a>
### Doc Type.clear cache

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Bind dependencies clear\_computed\_base\_for.
- Evaluate clear\_computed\_base\_for(self).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L5066) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L155)

<a id="op-2831ea0bd3499b"></a>
### Doc Type.after delete

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_after_delete`

**Inputs** self.

**Local steps**

- If not self.custom.
  - Evaluate clear\_controller\_cache(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L5151) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L145)

<a id="op-2311c55937e763"></a>
### Doc Type.rename files and folders

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_rename_files_and_folders`

**Inputs** self, old, new.

**State and service calls** msgprint with translated “Renamed files and replaced code in controllers, please check!”.

**Local steps**

- Set new\_path from get\_doc\_path(self.module, “doctype”, new).
- Set old\_path from get\_doc\_path(self.module, “doctype”, old).
- Evaluate shutil.move(old\_path, new\_path).
- For each fname in os.listdir(new\_path).
  - If Platform.scrub(old) belongs to fname.
    - Set old\_file\_name from os.path.join(new\_path, fname).
    - Set new\_file\_name from os.path.join(new\_path, fname.replace(Platform.scrub(old), Platform.scrub(new))).
    - Evaluate shutil.move(old\_file\_name, new\_file\_name).
- Evaluate self.rename\_inside\_controller(new, old, new\_path).
- Evaluate Platform.msgprint(translated “Renamed files and replaced code in controllers, please check!”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [rename inside controller](operations-035.md#op-dd6e90ac3cd49e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L5227) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L168)

<a id="op-dd6e90ac3cd49e"></a>
### Doc Type.rename inside controller

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_rename_inside_controller`

**Inputs** self, new, old, new\_path.

**Local steps**

- For each fname in tuple(“{}.js”, “{}.py”, “{}\_list.js”, “{}\_calendar.js”, …).
  - Set fname from os.path.join(new\_path, fname.format(Platform.scrub(new))).
  - If os.path.exists(fname).
    - Within open(fname) bound as f.
      - Set code from f.read().
    - Within open(fname, “w”) bound as f.
      - If fname.endswith(“.js”).
        - Set file\_content from code.replace(old, new).
      - Otherwise.
        - If fname.endswith(“.py”).
          - Set new\_scrub from Platform.scrub(new).
          - Set new\_no\_space\_no\_hyphen from new.replace(one space, empty text).replace(“-”, empty text).
          - Set new\_no\_space from new.replace(one space, empty text).
          - Set old\_scrub from Platform.scrub(old).
          - Set old\_no\_space\_no\_hyphen from old.replace(one space, empty text).replace(“-”, empty text).
          - Set old\_no\_space from old.replace(one space, empty text).
          - Set file\_content from re.sub(formatted text {old\_scrub}\|{old\_no\_space}\|{old\_no\_space\_no\_hyphen}, deferred anonymous expression, code).
      - Evaluate f.write(file\_content).
- Set doctype\_json\_path from os.path.join(new\_path, formatted text {Platform.scrub(new)}.json).
- Set current\_data from Platform.get\_file\_json(doctype\_json\_path).
- Set current\_data at “name” from new.
- Within open(doctype\_json\_path, “w”) bound as f.
  - Evaluate json.dump(current\_data, f, indent = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L5683) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1984) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L169)

<a id="op-6a4fe023bcc6ea"></a>
### Doc Type.before reload

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_before_reload`

**Inputs** self.

**Local steps**

- If not (self.issingle and self.istable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.issingle → self.istable.
  - Evaluate self.preserve\_naming\_series\_options\_in\_property\_setter().

If control reaches the end, it returns no value.

**Methods declared on this owner** [preserve naming series options in property setter](operations-035.md#op-4dccfeeffe54a5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0063.json#L6652) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L149)

<a id="op-4dccfeeffe54a5"></a>
### Doc Type.preserve naming series options in property setter

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_preserve_naming_series_options_in_property_setter`

**Inputs** self.

**Record and data access** read self.name via get\_all · read “Property Setter” via get\_value.

**Explicit results** no value.

**Local steps**

- Set naming\_series from self.get(“fields”, mapping(“fieldname” → “naming\_series”)).
- If not naming\_series.
  - Return no value.
- If not (Platform.db.table\_exists(self.name) and Platform.get\_all(self.name, fields = list(“name”), limit = 1, as\_list = true)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.table\_exists(self.name) → Platform.get\_all(self.name, fields = list(“name”), limit = 1, as\_list = true).
  - Return no value.
- Set existing\_property\_setter from Platform.db.get\_value(“Property Setter”, mapping(“doc\_type” → self.name, “property” → “options”, “field\_name” → “naming\_series”)).
- If not existing\_property\_setter.
  - Evaluate make\_property\_setter(self.name, “naming\_series”, “options”, naming\_series at 0.options, validate\_fields\_for\_doctype = false, …).
  - If naming\_series at 0.default.
    - Evaluate make\_property\_setter(self.name, “naming\_series”, “default”, naming\_series at 0.default, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L167)

<a id="op-06e33f73afa799"></a>
### Doc Type.before export

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_before_export`

**Inputs** self, docdict.

**Explicit results** no value.

**Local steps**

- Bind local operation remove\_null\_fields for subsequent calls.
- Evaluate remove\_null\_fields(docdict).
- Set docdict at “field\_order” from list of f.fieldname for f drawn from self.fields.
  - Draw f from self.fields.
- If self.custom.
  - Return no value.
- Set path from get\_file\_path(self.module, “DocType”, self.name).
- If os.path.exists(path).
  - Attempt the following.
    - Within open(path) bound as txtfile.
      - Set olddoc from json.loads(txtfile.read()).
    - Set old\_field\_names from list of f at “fieldname” for f drawn from olddoc.get(“fields”, list()).
      - Draw f from olddoc.get(“fields”, list()).
    - If old\_field\_names.
      - Set new\_field\_dicts from list().
      - Set remaining\_field\_names from list of f.fieldname for f drawn from self.fields.
        - Draw f from self.fields.
      - For each fieldname in old\_field\_names.
        - Set field\_dict from list of f for f drawn from docdict at “fields” where f at “fieldname” equals fieldname.
          - Draw f from docdict at “fields”, keep a combination only if (f at “fieldname” equals fieldname).
        - If field\_dict.
          - Evaluate new\_field\_dicts.append(field\_dict at 0).
          - If fieldname belongs to remaining\_field\_names.
            - Evaluate remaining\_field\_names.remove(fieldname).
      - For each fieldname in remaining\_field\_names.
        - Set field\_dict from list of f for f drawn from docdict at “fields” where f at “fieldname” equals fieldname.
          - Draw f from docdict at “fields”, keep a combination only if (f at “fieldname” equals fieldname).
        - Evaluate new\_field\_dicts.append(field\_dict at 0).
      - Set docdict at “fields” from new\_field\_dicts.
  - On failure (ValueError).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L527) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L147)

<a id="op-3645846f2d24be"></a>
### Doc Type.before export.remove null fields

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_before_export_remove_null_fields`

**Inputs** o.

**Local steps**

- Set to\_remove from list().
- For each tuple(attr, value) in o.items().
  - If isinstance(value, list).
    - For each v in value.
      - Evaluate remove\_null\_fields(v).
  - Otherwise.
    - If not value.
      - Evaluate to\_remove.append(attr).
- For each attr in to\_remove.
  - Remove o at attr.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L1464) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L148)

<a id="op-a5252fa6b8ccdd"></a>
### Doc Type.prepare for import

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_prepare_for_import`

**Inputs** docdict.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- If docdict.get(“field\_order”).
  - Set new\_field\_dicts from list().
  - Set remaining\_field\_names from list of f at “fieldname” for f drawn from docdict.get(“fields”, list()).
    - Draw f from docdict.get(“fields”, list()).
  - For each fieldname in docdict.get(“field\_order”).
    - Set field\_dict from list of f for f drawn from docdict.get(“fields”, list()) where f at “fieldname” equals fieldname.
      - Draw f from docdict.get(“fields”, list()), keep a combination only if (f at “fieldname” equals fieldname).
    - If field\_dict.
      - Evaluate new\_field\_dicts.append(field\_dict at 0).
      - If fieldname belongs to remaining\_field\_names.
        - Evaluate remaining\_field\_names.remove(fieldname).
  - For each fieldname in remaining\_field\_names.
    - Set field\_dict from list of f for f drawn from docdict.get(“fields”, list()) where f at “fieldname” equals fieldname.
      - Draw f from docdict.get(“fields”, list()), keep a combination only if (f at “fieldname” equals fieldname).
    - Evaluate new\_field\_dicts.append(field\_dict at 0).
  - Set docdict at “fields” from new\_field\_dicts.
- If “field\_order” belongs to docdict.
  - Remove docdict at “field\_order”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L1675) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1981) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L166)

<a id="op-65a0bff2e08f62"></a>
### Doc Type.warn on module change

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_warn_on_module_change`

**Inputs** self.

**State and service calls** msgprint with translated “Module changed to {0}. Files in the previous module were not moved and remain at {1}, remove or relocate the …”.format(Platform.bold(self.module), Platform.bold(str(old\_path))).

**Explicit results** no value.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If (not previous or previous.module equals self.module).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous → previous.module equals self.module.
  - Return no value.
- Attempt the following.
  - Set old\_path from get\_doc\_path(previous.module, “doctype”, self.name).
- On failure (Exception).
  - Return no value.
- Evaluate Platform.msgprint(translated “Module changed to {0}. Files in the previous module were not moved and remain at {1}, remove or relocate the …”.format(Platform.bold(self.module), Platform.bold(str(old\_path)) ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L2207) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2004) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L189)

<a id="op-6619d0144a4ce4"></a>
### Doc Type.export doc

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_export_record`

**Inputs** self.

**Local steps**

- Bind dependencies export\_to\_files.
- Evaluate export\_to\_files(record\_list = list(list(“DocType”, self.name)), create\_init = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L2510) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L157)

<a id="op-7f23a6b3fd0aeb"></a>
### Doc Type.make controller template

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_make_controller_template`

**Inputs** self.

**Local steps**

- Evaluate make\_boilerplate(“controller.\_py”, self).
- If not self.istable.
  - Evaluate make\_boilerplate(“test\_controller.\_py”, self.as\_dict()).
  - Evaluate make\_boilerplate(“controller.js”, self.as\_dict()).
- If self.is\_tree.
  - Evaluate make\_boilerplate(“controller\_tree.js”, self.as\_dict()).
- If self.has\_web\_view.
  - Set templates\_path from Platform.get\_module\_path(Platform.scrub(self.module), “doctype”, Platform.scrub(self.name), “templates”).
  - If not os.path.exists(templates\_path).
    - Evaluate os.makedirs(templates\_path).
  - Evaluate make\_boilerplate(“templates/controller.html”, self.as\_dict()).
  - Evaluate make\_boilerplate(“templates/controller\_list.html”, self.as\_dict()).
  - Evaluate make\_boilerplate(“templates/controller\_row.html”, self.as\_dict()).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L111) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1975) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L162)

<a id="op-615898841779cb"></a>
### Doc Type.export types to controller

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_export_types_to_controller`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_module\_app.
- Bind dependencies TypeExporter.
- Attempt the following.
  - Set app from get\_module\_app(self.module).
- On failure (Platform.DoesNotExistError).
  - Return no value.
- If any(Platform.get\_hooks(“export\_python\_type\_annotations”, app\_name = app)).
  - Evaluate TypeExporter(self).export\_types().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“export\_python\_type\_annotations”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L3113) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L158)

<a id="op-c7081c8a34b972"></a>
### Doc Type.make amendable

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_make_amendable`

**Inputs** self.

**Local steps**

- If self.is\_submittable.
  - Set docfield from list of f for f drawn from self.fields where f.fieldname equals “amended\_from”.
    - Draw f from self.fields, keep a combination only if (f.fieldname equals “amended\_from”).
  - If docfield.
    - Set docfield at 0.options from self.name.
  - Otherwise.
    - Evaluate self.append(“fields”, mapping(“label” → “Amended From”, “fieldtype” → “Link”, “fieldname” → “amended\_from”, “options” → self.name, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L3305) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L161)

<a id="op-bcf4108e63df64"></a>
### Doc Type.make repeatable

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_make_repeatable`

**Inputs** self.

**Record and data access** read “Custom Field” via exists · read “DocField” via exists.

**Local steps**

- If self.allow\_auto\_repeat.
  - If (not Platform.db.exists(“Custom Field”, mapping(“fieldname” → “auto\_repeat”, “dt” → self.name)) and not Platform.db.exists(“DocField”, mapping(“fieldname” → “auto\_repeat”, “parent” → self.name))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.exists(“Custom Field”, mapping(“fieldname” → “auto\_repeat”, “dt” → self.name)) → not Platform.db.exists(“DocField”, mapping(“fieldname” → “auto\_repeat”, “parent” → self.name)).
    - Set insert\_after from self.fields at (len(self.fields) − 1).fieldname.
    - Set df from dict(fieldname = “auto\_repeat”, label = “Auto Repeat”, fieldtype = “Link”, options = “Auto Repeat”, …).
    - Evaluate create\_custom\_field(self.name, df, ignore\_validate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L3624) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1976) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L163)

<a id="op-ced048c6b68b73"></a>
### Doc Type.validate nestedset

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate_nestedset`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “{0} is a mandatory field”.format(field\_label) · validation helper with InvalidFieldNameError — translated “Parent Field must be a valid fieldname”.

**Local steps**

- If not self.get(“is\_tree”).
  - Return no value.
- Evaluate self.add\_nestedset\_fields().
- If not self.nsm\_parent\_field.
  - Set field\_label from Platform.bold(translated “Parent Field (Tree)”).
  - Call the validation error handler Platform.throw(translated “{0} is a mandatory field”.format(field\_label), Platform.MandatoryError).
- Set fieldnames from list of df.fieldname for df drawn from self.fields.
  - Draw df from self.fields.
- If (self.nsm\_parent\_field and self.nsm\_parent\_field does not belong to fieldnames).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.nsm\_parent\_field → self.nsm\_parent\_field does not belong to fieldnames.
  - Call the validation error handler Platform.throw(translated “Parent Field must be a valid fieldname”, InvalidFieldNameError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add nestedset fields](operations-035.md#op-52424d59373e6c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L4045) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2001) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L186)

<a id="op-52424d59373e6c"></a>
### Doc Type.add nestedset fields

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_add_nestedset_fields`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set fieldnames from list of df.fieldname for df drawn from self.fields.
  - Draw df from self.fields.
- If “lft” belongs to fieldnames.
  - Return no value.
- Evaluate self.append(“fields”, mapping(“label” → “Left”, “fieldtype” → “Int”, “fieldname” → “lft”, “read\_only” → 1, …)).
- Evaluate self.append(“fields”, mapping(“label” → “Right”, “fieldtype” → “Int”, “fieldname” → “rgt”, “read\_only” → 1, …)).
- Evaluate self.append(“fields”, mapping(“label” → “Is Group”, “fieldtype” → “Check”, “fieldname” → “is\_group”)).
- Evaluate self.append(“fields”, mapping(“label” → “Old Parent”, “fieldtype” → “Link”, “options” → self.name, “fieldname” → “old\_parent”, …)).
- Set parent\_field\_label from formatted text Parent {self.name}.
- Set parent\_field\_name from Platform.scrub(parent\_field\_label).
- Evaluate self.append(“fields”, mapping(“label” → parent\_field\_label, “fieldtype” → “Link”, “options” → self.name, “fieldname” → parent\_field\_name, …)).
- Set self.nsm\_parent\_field from parent\_field\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L4389) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L144)

<a id="op-41937365169297"></a>
### Doc Type.validate child table

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate_child_table`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.get(“istable”) or self.is\_new() or self.get(“is\_virtual”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“istable”) → self.is\_new() → self.get(“is\_virtual”).
  - Return no value.
- Evaluate self.add\_child\_table\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add child table fields](operations-036.md#op-87be035194dc75).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L5171) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1997) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L182)
