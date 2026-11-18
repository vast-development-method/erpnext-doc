# Record lifecycle and persistence · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Doctype settings map

<a id="op-883f798454d362"></a>
### Doc Type Settings Map.export doc

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_export_record`

**Inputs** self.

**Explicit results** no value · path.

**Local steps**

- If (Platform.flags.in\_import or not self.is\_standard or not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → not self.is\_standard → not Platform.conf.developer\_mode.
  - Return no value.
- Bind dependencies strip\_default\_fields.
- Set doc\_export from self.as\_dict(no\_nulls = true, ignore\_computed\_child\_tables = true).
- Evaluate self.run\_method(“before\_export”, doc\_export).
- Set doc\_export from strip\_default\_fields(self, doc\_export).
- Set path from self.get\_export\_path().
- Evaluate Platform.create\_folder(os.path.dirname(path)).
- Within open(path, “w+”) bound as f.
  - Evaluate f.write((Platform.as\_json(doc\_export) + whitespace '\\n')).
- Return path.

**Methods declared on this owner** [get export path](operations-039.md#op-e12635c0b77c21).

**Values supplied outside this operation** selected callable from self.run\_method(“before\_export”, doc\_export).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L2133) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L294)

<a id="op-e12635c0b77c21"></a>
### Doc Type Settings Map.get export path

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_get_export_path`

**Inputs** self.

**Declared result** str.

**Explicit results** os.path.join(get\_module\_path(self.module), “doctype\_settings\_map”, formatted text {Platform.scrub(self.applies\_to\_doctype)}.json).

**Local steps**

- Bind dependencies get\_module\_path.
- Return os.path.join(get\_module\_path(self.module), “doctype\_settings\_map”, formatted text {Platform.scrub(self.applies\_to\_doctype)}.json).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L2491) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L109) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L295)

<a id="op-4fcaaad7515cf6"></a>
### Doc Type Settings Map.on trash

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.\_guard\_standard().
- If self.is\_active.
  - Evaluate self.\_set\_sibling\_active().
- If (self.is\_standard and Platform.conf.developer\_mode and not Platform.flags.in\_test and not (Platform.flags.in\_migrate or Platform.flags.in\_install or Platform.flags.in\_patch)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → Platform.conf.developer\_mode → not Platform.flags.in\_test → not (Platform.flags.in\_migrate or Platform.flags.in\_install or Platform.flags.in\_patch).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_install → Platform.flags.in\_patch.
  - Evaluate Platform.db.after\_commit(self.delete\_export\_file).

If control reaches the end, it returns no value.

**Methods declared on this owner** [guard standard](operations-039.md#op-de86846acdf21f), [set sibling active](operations-039.md#op-0ff2196a2ee552).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L2624) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L297)

<a id="op-7ffb533b19a5b8"></a>
### Doc Type Settings Map.delete export file

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_delete_export_file`

**Inputs** self.

**Local steps**

- Set path from self.get\_export\_path().
- If os.path.exists(path).
  - Evaluate os.remove(path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export path](operations-039.md#op-e12635c0b77c21).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L2835) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L292)

<a id="op-de86846acdf21f"></a>
### Doc Type Settings Map.guard standard

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_guard_standard`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Standard DocType Settings Map can only be changed in Developer Mode.”.

**Local steps**

- If not self.is\_standard.
  - Return no value.
- If (Platform.conf.developer\_mode or Platform.flags.in\_migrate or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.flags.in\_migrate → Platform.flags.in\_install.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Standard DocType Settings Map can only be changed in Developer Mode.”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L2946) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L110) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L296)

<a id="op-07ad2c57c76446"></a>
### Doc Type Settings Map.validate unique per doctype

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_validate_unique_per_record_type`

**Inputs** self.

**Record and data access** read “DocType Settings Map” via exists.

**Explicit failure paths** validation helper — translated “A standard settings map already exists for {0} in {1}.”.format(self.applies\_to\_doctype, self.module) · validation helper — translated “A custom settings map already exists for {0}.”.format(self.applies\_to\_doctype).

**Local steps**

- Set filters from mapping(“applies\_to\_doctype” → self.applies\_to\_doctype, “is\_standard” → self.is\_standard, “name” → tuple(“!=”, self.name)).
- If self.is\_standard.
  - Set filters at “module” from self.module.
- If Platform.db.exists(“DocType Settings Map”, filters).
  - If self.is\_standard.
    - Call the validation error handler Platform.throw(translated “A standard settings map already exists for {0} in {1}.”.format(self.applies\_to\_doctype, self.module)).
  - Call the validation error handler Platform.throw(translated “A custom settings map already exists for {0}.”.format(self.applies\_to\_doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L3102) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L116) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L302)

<a id="op-efe753e3a8a84d"></a>
### Doc Type Settings Map.enforce single active

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_enforce_single_active`

**Inputs** self.

**Record and data access** read “DocType Settings Map” via get\_all.

**State and service calls** request set\_value on “DocType Settings Map”.

**Explicit results** no value.

**Local steps**

- If self.is\_active.
  - Evaluate Platform.db.set\_value(“DocType Settings Map”, mapping(“applies\_to\_doctype” → self.applies\_to\_doctype, “name” → tuple(“!=”, self.name)), “is\_active”, 0).
  - Return no value.
- Set siblings from Platform.get\_all(“DocType Settings Map”, filters = mapping(“applies\_to\_doctype” → self.applies\_to\_doctype, “name” → tuple(“!=”, self.name)), fields = list(“name”, “is\_standard”, “is\_active”)).
- If (siblings and not any(generator of s.is\_active for s drawn from siblings)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in siblings → not any(generator of s.is\_active for s drawn from siblings).
  - Draw s from siblings.
  - Set fallback from next(generator of s for s drawn from siblings where s.is\_standard, siblings at 0).
    - Draw s from siblings, keep a combination only if (s.is\_standard).
  - Evaluate Platform.db.set\_value(“DocType Settings Map”, fallback.name, “is\_active”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L3438) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L293)

<a id="op-0ff2196a2ee552"></a>
### Doc Type Settings Map.set sibling active

`operation_foundation_core_record_definitions_record_type_settings_map_business_behavior_record_type_settings_map_set_sibling_active`

**Inputs** self.

**Record and data access** read “DocType Settings Map” via get\_all.

**State and service calls** request set\_value on “DocType Settings Map”.

**Local steps**

- Set siblings from Platform.get\_all(“DocType Settings Map”, filters = mapping(“applies\_to\_doctype” → self.applies\_to\_doctype, “name” → tuple(“!=”, self.name)), fields = list(“name”), order\_by = “is\_standard desc”, limit = 1).
- If siblings.
  - Evaluate Platform.db.set\_value(“DocType Settings Map”, siblings at 0.name, “is\_active”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L3901) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L114) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L300)

## Service · Document

<a id="op-b3fb4f29a94cf2"></a>
### Reduce extended instance

`operation_foundation_binding_foundation_model_document_reduce_extended_instance`

**Inputs** doc.

**Explicit results** tuple(\_reconstruct\_extended\_instance, tuple(type(doc).\_\_bases\_\_), doc.\_\_getstate\_\_()).

**Local steps**

- Return tuple(\_reconstruct\_extended\_instance, tuple(type(doc).\_\_bases\_\_), doc.\_\_getstate\_\_()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L205) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1637)

<a id="op-37c0b2fa63c95d"></a>
### Reconstruct extended instance

`operation_foundation_binding_foundation_model_document_reconstruct_extended_instance`

**Inputs** bases.

**Explicit results** extended\_class.\_\_new\_\_(extended\_class).

**Local steps**

- Set extended\_class from \_create\_extended\_class(bases).
- Return extended\_class.\_\_new\_\_(extended\_class).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L204) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1636)

<a id="op-f1d17e541806d9"></a>
### Get controller

`operation_foundation_binding_foundation_model_document_get_controller`

**Inputs** doctype.

**Explicit results** site\_controllers at doctype.

**Local steps**

- Set site\_controllers from Platform.controllers.setdefault(Platform.local.site, mapping()).
- If doctype does not belong to site\_controllers.
  - Set site\_controllers at doctype from import\_controller(doctype).
- Return site\_controllers at doctype.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L200) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1632)

<a id="op-c6affb479a31b6"></a>
### Import controller

`operation_foundation_binding_foundation_model_document_import_controller`

**Inputs** doctype.

**Record and data access** read “DocType” via get\_value.

**Explicit results** NestedSet when doctype\_info.is\_tree, otherwise Document · \_update\_computed\_ct\_props(class\_, doctype).

**Explicit failure paths** validation helper — formatted text {doctype}: {Platform.bold(import\_path)} must be a subclass of {original\_class\_path} · ImportError(doctype when module\_path is identical to no value, otherwise formatted text {doctype}: {classname} does not exist in module {module\_path}) · ImportError(formatted text {doctype}: {classname} is not a subclass of Document).

**Local steps**

- Bind dependencies NestedSet.
- Set module\_name from “Core”.
- If doctype does not belong to DOCTYPES\_FOR\_DOCTYPE.
  - Set doctype\_info from Platform.db.get\_value(“DocType”, doctype, tuple(“module”, “custom”, “is\_tree”), as\_dict = true).
  - If doctype\_info.
    - If doctype\_info.custom.
      - Return NestedSet when doctype\_info.is\_tree, otherwise Document.
        - Value choice on doctype\_info.is\_tree — true gives NestedSet, false gives Document.
    - Set module\_name from doctype\_info.module.
- Set module\_path from no value.
- Set class\_overrides from Platform.get\_hooks(“override\_doctype\_class”).
- Set module from load\_doctype\_module(doctype, module\_name).
- Set classname from doctype.replace(one space, empty text).replace(“-”, empty text).
- Set class\_ from getattr(module, classname, no value).
- If (class\_overrides and class\_overrides.get(doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in class\_overrides → class\_overrides.get(doctype).
  - Set import\_path from class\_overrides at doctype at negative 1.
  - Set tuple(module\_path, custom\_classname) from import\_path.rsplit(“.”, 1).
  - Set custom\_module from Platform.get\_module(module\_path).
  - Set custom\_class\_ from getattr(custom\_module, custom\_classname, no value).
  - If not issubclass(custom\_class\_, class\_).
    - Set original\_class\_path from Platform.bold(formatted text {class\_.\_\_module\_\_}.{class\_.\_\_name\_\_}).
    - Call the validation error handler Platform.throw(formatted text {doctype}: {Platform.bold(import\_path)} must be a subclass of {original\_class\_path}, title = translated “Invalid Override”).
  - Set class\_ from custom\_class\_.
- If class\_ is identical to no value.
  - Raise ImportError(doctype when module\_path is identical to no value, otherwise formatted text {doctype}: {classname} does not exist in module {module\_path}).
    - Value choice on module\_path is identical to no value — true gives doctype, false gives formatted text {doctype}: {classname} does not exist in module {module\_path}.
- If not issubclass(class\_, Document).
  - Raise ImportError(formatted text {doctype}: {classname} is not a subclass of Document).
- Set class\_ from \_get\_extended\_class(class\_, doctype).
- Return \_update\_computed\_ct\_props(class\_, doctype).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“override\_doctype\_class”), getattr(module, classname, no value) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L203) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1635)

<a id="op-f72de1d3ee8d7c"></a>
### Update computed ct props

`operation_foundation_binding_foundation_model_document_update_computed_ct_props`

**Inputs** class\_, doctype.

**Explicit results** class\_.

**Local steps**

- If (doctype belongs to DOCTYPES\_FOR\_DOCTYPE or getattr(class\_, “\_computed\_ct\_props\_updated”, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype belongs to DOCTYPES\_FOR\_DOCTYPE → getattr(class\_, “\_computed\_ct\_props\_updated”, false).
  - Return class\_.
- Set meta from Platform.get\_meta(doctype).
- For each df in meta.get\_table\_fields(include\_computed = true).
  - If df.is\_virtual.
    - Evaluate \_update\_computed\_ct\_prop(class\_, df).
- Set class\_.\_computed\_ct\_props\_updated from true.
- Return class\_.

**Values supplied outside this operation** selected callable from getattr(class\_, “\_computed\_ct\_props\_updated”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1640)

<a id="op-3d5b40f166f44c"></a>
### Update computed ct prop

`operation_foundation_binding_foundation_model_document_update_computed_ct_prop`

**Inputs** class\_, df.

**Local steps**

- Set fieldname from df.fieldname.
- Set original\_prop from getattr(class\_, fieldname, no value).
- Bind local operation computed\_ct\_prop for subsequent calls.
- Evaluate setattr(class\_, fieldname, property(computed\_ct\_prop)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(class\_, fieldname, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L206) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1662) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1638)

<a id="op-287a3093988e35"></a>
### Update computed ct prop.computed ct prop

`operation_foundation_binding_foundation_model_document_update_computed_ct_prop_computed_ct_prop`

**Inputs** self.

**Explicit results** self.\_\_dict\_\_ at fieldname.

**Local steps**

- If (original\_prop and is\_a\_property(original\_prop)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in original\_prop → is\_a\_property(original\_prop).
  - Set value from original\_prop.\_\_get\_\_(self, type(self)).
- Otherwise.
  - If options bound to getattr(df, “options”, no value).
    - Set value from self.\_evaluate\_virtual\_field\_options(options).
  - Otherwise.
    - Set value from list().
- Evaluate self.set(fieldname, value).
- Return self.\_\_dict\_\_ at fieldname.

**Values supplied outside this operation** selected callable from getattr(df, “options”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L207) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1639)

<a id="op-a1f0032f4b20d7"></a>
### Get extended class

`operation_foundation_binding_foundation_model_document_get_extended_class`

**Inputs** base\_class, doctype.

**Explicit results** base\_class · \_create\_extended\_class(tuple(expanded extension\_classes, base\_class)).

**Explicit failure paths** ImportError(“Error retrieving extension class from path:\\n{0}”.format(extension\_path)).

**Local steps**

- Set extensions from Platform.get\_hooks(“extend\_doctype\_class”, mapping()).get(doctype).
- If not extensions.
  - Return base\_class.
- Set extension\_classes from list().
- For each extension\_path in reversed(extensions).
  - Attempt the following.
    - Set extension\_class from Platform.get\_attr(extension\_path).
  - On failure (Exception) bound to e.
    - Raise ImportError(“Error retrieving extension class from path:\\n{0}”.format(extension\_path)) with cause e.
  - Evaluate extension\_classes.append(extension\_class).
- Return \_create\_extended\_class(tuple(expanded extension\_classes, base\_class)).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“extend\_doctype\_class”, mapping()), Platform.get\_attr(extension\_path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L201) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1633)

<a id="op-d332d6bd29f29b"></a>
### Create extended class

`operation_foundation_binding_foundation_model_document_create_extended_class`

**Inputs** bases.

**Wrappers, in declaration order** functools.cache.

**Explicit results** type(formatted text Extended{base\_class.\_\_name\_\_}, bases, mapping(“\_\_reduce\_\_” → \_reduce\_extended\_instance, “\_\_module\_\_” → base\_class.\_\_module\_\_)).

**Local steps**

- Set base\_class from bases at negative 1.
- Return type(formatted text Extended{base\_class.\_\_name\_\_}, bases, mapping(“\_\_reduce\_\_” → \_reduce\_extended\_instance, “\_\_module\_\_” → base\_class.\_\_module\_\_)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L124) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1556)

<a id="op-6b05b1e8bf142f"></a>
### Accepts method argument

`operation_foundation_model_document_business_behavior_accepts_method_argument`

**Inputs** f.

**Wrappers, in declaration order** functools.cache.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set signature from inspect.signature(f).
- Set kinds from list of p.kind for p drawn from signature.parameters.values().
  - Draw p from signature.parameters.values().
- If any(generator of kind equals inspect.Parameter.VAR\_POSITIONAL for kind drawn from kinds).
  - Draw kind from kinds.
  - Return true.
- If sum(generator of 1 for kind drawn from kinds where kind belongs to \_POSITIONAL\_PARAM\_KINDS) &gt; 1.
  - Draw kind from kinds, keep a combination only if (kind belongs to \_POSITIONAL\_PARAM\_KINDS).
  - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L3948) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L937)

<a id="op-7a8b241f164faf"></a>
### Get doc

`operation_foundation_model_document_business_behavior_get_record`

**Inputs** document (positional only).

**Wrappers, in declaration order** overload.

**Declared result** “Document”.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4224) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1060)

<a id="op-ffe9a715629d94"></a>
### Get doc

`operation_foundation_model_document_business_behavior_get_record_2`

**Inputs** doctype (positional only).

**Wrappers, in declaration order** overload.

**Declared result** \_SingleDocument.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4275) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1061)

<a id="op-96d8fdddd94a1d"></a>
### Get doc

`operation_foundation_model_document_business_behavior_get_record_3`

**Inputs** doctype (positional only), name (positional only), for\_update (named only, default no value), check\_permission (named only, default no value).

**Wrappers, in declaration order** overload.

**Declared result** “Document”.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4320) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1062)

<a id="op-2b0af693d770cd"></a>
### Get doc

`operation_foundation_model_document_business_behavior_get_record_4`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** overload.

**Declared result** “\_NewDocument”.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4400) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1063)

<a id="op-bda1d8c3d26fe2"></a>
### Get doc

`operation_foundation_model_document_business_behavior_get_record_5`

**Inputs** documentdict.

**Wrappers, in declaration order** overload.

**Declared result** “\_NewDocument”.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4441) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1064)

<a id="op-2f4e8178daf818"></a>
### Get doc

`operation_foundation_model_document_business_behavior_get_record_6`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** simple\_singledispatch.

**Declared result** “Document”.

**Explicit results** get\_doc\_from\_dict(kwargs).

**Explicit failure paths** ValueError(“First non keyword argument must be a string or dict”).

**Local steps**

- If (not args and kwargs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args → kwargs.
  - Return get\_doc\_from\_dict(kwargs).
- Otherwise.
  - Raise ValueError(“First non keyword argument must be a string or dict”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4489) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1065)
