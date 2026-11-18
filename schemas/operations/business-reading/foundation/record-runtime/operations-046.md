# Record lifecycle and persistence · operations 46

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-a9935a702ba2d8"></a>
### Document.get valid columns

`operation_foundation_binding_foundation_model_document_document_get_valid_columns`

**Inputs** self.

**Declared result** list at str.

**Explicit results** valid\_columns\_cache at self.doctype.

**Local steps**

- Set valid\_columns\_cache from Platform.local.valid\_columns.
- If self.doctype does not belong to valid\_columns\_cache.
  - If self.doctype belongs to DOCTYPES\_FOR\_DOCTYPE.
    - Bind dependencies get\_table\_columns.
    - Set valid from get\_table\_columns(self.doctype).
  - Otherwise.
    - Set valid from self.meta.get\_valid\_columns().
  - Set valid\_columns\_cache at self.doctype from valid.
- Return valid\_columns\_cache at self.doctype.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1610) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1586)

<a id="op-e2def851dd1371"></a>
### Document.is new

`operation_foundation_binding_foundation_model_document_document_is_new`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool(self.get(“\_\_islocal”)).

**Local steps**

- Return bool(self.get(“\_\_islocal”)).

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1623) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1599)

<a id="op-6b857cbb1c8e1d"></a>
### Document.docstatus

`operation_foundation_binding_foundation_model_document_document_docstatus`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** DocStatus.

**Explicit results** value.

**Local steps**

- Set value from self.\_\_dict\_\_.get(“docstatus”).
- If not isinstance(value, DocStatus).
  - Set value from DocStatus((value or 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → 0.
  - Set self.\_\_dict\_\_ at “docstatus” from value.
- Return value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L134) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1566)

<a id="op-59c8c02ec2099b"></a>
### Document.docstatus

`operation_foundation_binding_foundation_model_document_document_docstatus_occurrence_2`

**Inputs** self, value.

**Wrappers, in declaration order** docstatus.setter.

**Declared result** no value.

**Local steps**

- If not isinstance(value, DocStatus).
  - Set value from DocStatus((value or 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → 0.
- Set self.\_\_dict\_\_ at “docstatus” from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L135) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1567)

<a id="op-8dc085dc083de4"></a>
### Document.as dict

`operation_foundation_binding_foundation_model_document_document_as_dict`

**Inputs** self, no\_nulls = false, no\_default\_fields = false, convert\_dates\_to\_str = false, no\_child\_table\_fields = false, no\_private\_properties = false, ignore\_computed\_child\_tables (named only, default false).

**Declared result** dict.

**Explicit results** doc.

**Local steps**

- Set doc from self.get\_valid\_dict(convert\_dates\_to\_str = convert\_dates\_to\_str, ignore\_nulls = no\_nulls).
- Set doc at “doctype” from self.doctype.
- Set table\_fieldnames from self.\_non\_computed\_table\_fieldnames when ignore\_computed\_child\_tables, otherwise self.\_table\_fieldnames.
  - Value choice on ignore\_computed\_child\_tables — true gives self.\_non\_computed\_table\_fieldnames, false gives self.\_table\_fieldnames.
- For each fieldname in table\_fieldnames.
  - Set children from (getattr(self, fieldname, no value) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self, fieldname, no value) → list().
  - Set doc at fieldname from list of d.as\_dict(convert\_dates\_to\_str = convert\_dates\_to\_str, no\_nulls = no\_nulls, no\_default\_fields = no\_default\_fields, no\_child\_table\_fields = no\_child\_table\_fields, …) for d drawn from children.
    - Draw d from children.
- If no\_default\_fields.
  - For each key in default\_fields.
    - If key belongs to doc.
      - Remove doc at key.
- If no\_child\_table\_fields.
  - For each key in child\_table\_fields.
    - If key belongs to doc.
      - Remove doc at key.
- If not no\_private\_properties.
  - For each key in tuple(“\_user\_tags”, “\_\_islocal”, “\_\_onload”, “\_liked\_by”, …).
    - If value bound to getattr(self, key, no value).
      - Set doc at key from value.
- Return doc.

**Methods declared on this owner** [get valid dict](operations-045.md#op-c47e5bad7a2c34).

**Values supplied outside this operation** selected callable from getattr(self, fieldname, no value), getattr(self, key, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L126) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1558)

<a id="op-96bad16b38093f"></a>
### Document.as json

`operation_foundation_binding_foundation_model_document_document_as_json`

**Inputs** self.

**Explicit results** Platform.as\_json(self.as\_dict()).

**Local steps**

- Return Platform.as\_json(self.as\_dict()).

**Methods declared on this owner** [as dict](operations-046.md#op-8dc085dc083de4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L127) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1559)

<a id="op-7cce192a7693ab"></a>
### Document.get table field doctype

`operation_foundation_binding_foundation_model_document_document_get_table_field_doctype`

**Inputs** self, fieldname.

**Explicit results** self.\_table\_fieldnames.get(fieldname).

**Local steps**

- Return self.\_table\_fieldnames.get(fieldname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1608) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1584)

<a id="op-d9ba1c5b7521f2"></a>
### Document.get parentfield of doctype

`operation_foundation_binding_foundation_model_document_document_get_parentfield_of_doctype`

**Inputs** self, doctype.

**Explicit results** next(generator of fieldname for tuple(fieldname, child\_doctype) drawn from self.\_table\_fieldnames.items() where child\_doctype equals doctype, no value).

**Local steps**

- Return next(generator of fieldname for tuple(fieldname, child\_doctype) drawn from self.\_table\_fieldnames.items() where child\_doctype equals doctype, no value).
  - Draw tuple(fieldname, child\_doctype) from self.\_table\_fieldnames.items(), keep a combination only if (child\_doctype equals doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1582)

<a id="op-040f69a9d36d01"></a>
### Document.handle hash conflict

`operation_foundation_binding_foundation_model_document_document_handle_hash_conflict`

**Inputs** self.

**State and service calls** call db\_insert on self.

**Explicit results** self.db\_insert().

**Explicit failure paths** propagate active failure.

**Local steps**

- Set self.flags.retry\_count from ((self.flags.retry\_count or 0) + 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.retry\_count → 0.
- If self.flags.retry\_count ≥ 5.
  - Propagate the active failure.
- Set self.name from no value.
- Return self.db\_insert().

**Methods declared on this owner** [db insert](operations-046.md#op-bf3615830b875a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1615) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1591)

<a id="op-bf3615830b875a"></a>
### Document.db insert

`operation_foundation_binding_foundation_model_document_document_db_insert`

**Inputs** self, ignore\_if\_duplicate = false.

**State and service calls** execute query text (INSERT).format(doctype = self.doctype, columns = “, ”.join(generator of ((“′” + c) + “′”) for c drawn from columns), values = “, ”.join((list(“%s”) × len(columns))), conflict\_handler = conflict … · msgprint with translated “{0} {1} already exists”.format(translated self.doctype, Platform.bold(self.name)).

**Explicit results** self.\_handle\_hash\_conflict().

**Explicit failure paths** Platform.DuplicateEntryError(self.doctype, self.name, e) · propagate active failure.

**Local steps**

- If not self.name.
  - Evaluate set\_new\_name(self).
- Set conflict\_handler from empty text.
- Set returning from empty text.
- If ((ignore\_if\_duplicate or self.meta.autoname equals “hash”) and Platform.db.db\_type equals “postgres” and (self.flags.retry\_count or 0) &lt; 5).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (ignore\_if\_duplicate or self.meta.autoname equals “hash”) → Platform.db.db\_type equals “postgres” → (self.flags.retry\_count or 0) &lt; 5.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_if\_duplicate → self.meta.autoname equals “hash”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.retry\_count → 0.
  - Set conflict\_handler from “on conflict (name) do nothing”.
  - If self.meta.autoname equals “hash”.
    - Set returning from “RETURNING name”.
- If not self.creation.
  - Set self.creation, self.modified from now().
  - Set self.owner, self.modified\_by from Platform.session.user.
- Set d from self.get\_valid\_dict(convert\_dates\_to\_str = true, ignore\_nulls = self.doctype belongs to DOCTYPES\_FOR\_DOCTYPE, ignore\_virtual = true).
- Set columns from list(d).
- Attempt the following.
  - Set name from Platform.db.sql(query text (INSERT).format(doctype = self.doctype, columns = “, ”.join(generator of ((“′” + c) + “′”) for c drawn from columns), values = “, ”.join((list(“%s”) × len(columns))), conflict\_ha ….
    - Draw c from columns.
  - If (Platform.db.db\_type equals “postgres” and self.meta.autoname equals “hash” and not name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.db\_type equals “postgres” → self.meta.autoname equals “hash” → not name.
    - Return self.\_handle\_hash\_conflict().
- On failure (Exception) bound to e.
  - If Platform.db.is\_primary\_key\_violation(e).
    - If self.meta.autoname equals “hash”.
      - Return self.\_handle\_hash\_conflict().
    - If not ignore\_if\_duplicate.
      - Evaluate Platform.msgprint(translated “{0} {1} already exists”.format(translated self.doctype, Platform.bold(self.name)), title = translated “Duplicate Name”, indicator = “red”).
      - Raise Platform.DuplicateEntryError(self.doctype, self.name, e).
  - Otherwise.
    - If Platform.db.is\_unique\_key\_violation(e).
      - Evaluate self.show\_unique\_validation\_message(e).
    - Otherwise.
      - Propagate the active failure.
- Evaluate self.set(“\_\_islocal”, false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get valid dict](operations-045.md#op-c47e5bad7a2c34), [handle hash conflict](operations-046.md#op-040f69a9d36d01), [show unique validation message](operations-046.md#op-dc156690b534d2), [set](operations-045.md#op-b58a481a5882b4).

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1562)

<a id="op-fa126f30709bdc"></a>
### Document.db update

`operation_foundation_binding_foundation_model_document_document_db_update`

**Inputs** self.

**State and service calls** call db\_insert on self · execute query text (UPDATE).format(doctype = self.doctype, values = “, ”.join(generator of ((“′” + c) + “′=%s”) for c drawn from columns)).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The value of the field {0} is too long in the {1} document. To resolve this issue, please reduce the value l …”.format(Platform.bold(label), Platform.bold(self.doctype)) · propagate active failure.

**Local steps**

- If (self.get(“\_\_islocal”) or not self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_\_islocal”) → not self.name.
  - Evaluate self.db\_insert().
  - Return no value.
- Set d from self.get\_valid\_dict(convert\_dates\_to\_str = true, ignore\_nulls = self.doctype belongs to DOCTYPES\_FOR\_DOCTYPE, ignore\_virtual = true).
- Set name from cstr(d at “name”).
- Remove d at “name”.
- Set columns from list(d).
- Attempt the following.
  - Evaluate Platform.db.sql(query text (UPDATE).format(doctype = self.doctype, values = “, ”.join(generator of ((“′” + c) + “′=%s”) for c drawn from columns)), list(expanded list(d.values()), name)).
    - Draw c from columns.
- On failure (Exception) bound to e.
  - If Platform.db.is\_data\_too\_long(e).
    - Set column from re.search(“column\\s+'(&#91;^'&#93;+)'”, e.args at 1).
    - If column.
      - Set label from self.get\_label\_from\_fieldname(column.group(1)).
      - Call the validation error handler Platform.throw(translated “The value of the field {0} is too long in the {1} document. To resolve this issue, please reduce the value l …”.format(Platform.bold(label), Platform.bold(self.doctype)), title = ….
  - If Platform.db.is\_unique\_key\_violation(e).
    - Evaluate self.show\_unique\_validation\_message(e).
  - Otherwise.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [db insert](operations-046.md#op-bf3615830b875a), [get valid dict](operations-045.md#op-c47e5bad7a2c34), [get label from fieldname](operations-046.md#op-2ee136320c1c10), [show unique validation message](operations-046.md#op-dc156690b534d2).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1563)

<a id="op-687b0c61b42ea0"></a>
### Document.db update all

`operation_foundation_binding_foundation_model_document_document_db_update_all`

**Inputs** self.

**State and service calls** call db\_update on self · call db\_update on doc.

**Local steps**

- Evaluate self.db\_update().
- For each fieldname in self.\_non\_computed\_table\_fieldnames.
  - For each doc in self.get(fieldname).
    - Evaluate doc.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [db update](operations-046.md#op-fa126f30709bdc), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L132) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1564)

<a id="op-dc156690b534d2"></a>
### Document.show unique validation message

`operation_foundation_binding_foundation_model_document_document_show_unique_validation_message`

**Inputs** self, e.

**State and service calls** msgprint with translated “{0} must be unique”.format((label or fieldname)).

**Explicit failure paths** Platform.UniqueValidationError(self.doctype, self.name, e).

**Local steps**

- If Platform.db.db\_type equals “mariadb”.
  - Set fieldname from str(e).split(“'”) at negative 2.
  - Set label from no value.
  - Attempt the following.
    - Set fieldname from self.get\_field\_name\_by\_key\_name(fieldname).
  - On failure (IndexError).
    - Take no action here.
  - Set label from self.get\_label\_from\_fieldname(fieldname).
  - Evaluate Platform.msgprint(translated “{0} must be unique”.format((label or fieldname))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in label → fieldname.
- Raise Platform.UniqueValidationError(self.doctype, self.name, e).

**Methods declared on this owner** [get field name by key name](operations-046.md#op-244e53e15b4265), [get label from fieldname](operations-046.md#op-2ee136320c1c10).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1616)

<a id="op-244e53e15b4265"></a>
### Document.get field name by key name

`operation_foundation_binding_foundation_model_document_document_get_field_name_by_key_name`

**Inputs** self, key\_name.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text   SHOW  INDEX  FROM  ′tab{self.doctype}′  WHERE  key\_name=%s  AND  Non\_unique=0  , key\_name, as\_dict = true) at 0.get(“Column\_name”).

**Local steps**

- Return Platform.db.sql(formatted text   SHOW  INDEX  FROM  ′tab{self.doctype}′  WHERE  key\_name=%s  AND  Non\_unique=0  , key\_name, as\_dict = true) at 0.get(“Column\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L142) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1598) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1574)

<a id="op-2ee136320c1c10"></a>
### Document.get label from fieldname

`operation_foundation_binding_foundation_model_document_document_get_label_from_fieldname`

**Inputs** self, fieldname.

**Explicit results** translated df.label when df.label, otherwise no value.

**Local steps**

- Set df from self.meta.get\_field(fieldname).
- If df.
  - Return translated df.label when df.label, otherwise no value.
    - Value choice on df.label — true gives translated df.label, false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L146) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1602) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1578)

<a id="op-206d0c15620d1a"></a>
### Document.update modified

`operation_foundation_binding_foundation_model_document_document_update_modified`

**Inputs** self.

**State and service calls** request set\_single\_value on self.doctype · request set\_value on self.doctype.

**Local steps**

- Evaluate self.set(“modified”, now()).
- If getattr(self.meta, “issingle”, false).
  - Evaluate Platform.db.set\_single\_value(self.doctype, “modified”, self.modified, update\_modified = false).
- Otherwise.
  - Evaluate Platform.db.set\_value(self.doctype, self.name, “modified”, self.modified, update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set](operations-045.md#op-b58a481a5882b4).

**Values supplied outside this operation** clock or generated value from now() · selected callable from getattr(self.meta, “issingle”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1622)

<a id="op-54f49255e9ad2e"></a>
### Document.fix numeric types

`operation_foundation_binding_foundation_model_document_document_fix_numeric_types`

**Inputs** self.

**Local steps**

- For each df in self.meta.get(“fields”, mapping(“fieldtype” → tuple(“in”, numeric\_fieldtypes))).
  - If df.fieldtype equals “Check”.
    - Evaluate self.set(df.fieldname, cint(self.get(df.fieldname))).
  - Otherwise.
    - If self.get(df.fieldname) is distinct from no value.
      - If df.fieldtype equals “Int”.
        - Evaluate self.set(df.fieldname, cint(self.get(df.fieldname))).
      - Otherwise.
        - If df.fieldtype belongs to tuple(“Float”, “Currency”, “Percent”).
          - Evaluate self.set(df.fieldname, flt(self.get(df.fieldname))).
- Evaluate self.docstatus.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set](operations-045.md#op-b58a481a5882b4), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L139) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1595) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1571)

<a id="op-770315ca6e1d12"></a>
### Document.get missing mandatory fields

`operation_foundation_binding_foundation_model_document_document_get_missing_mandatory_fields`

**Inputs** self.

**Explicit results** missing.

**Local steps**

- Bind local operation get\_msg for subsequent calls.
- Bind local operation has\_content for subsequent calls.
- Set missing from list().
- For each df in self.meta.get(“fields”, mapping(“reqd” → tuple(“=”, 1))).
  - If (self.get(df.fieldname) belongs to tuple(no value, list()) or not has\_content(df)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(df.fieldname) belongs to tuple(no value, list()) → not has\_content(df).
    - Evaluate missing.append(tuple(df.fieldname, get\_msg(df))).
- If self.meta.istable.
  - For each fieldname in tuple(“parent”, “parenttype”).
    - If not self.get(fieldname).
      - Evaluate missing.append(tuple(fieldname, get\_msg(\_dict(label = fieldname)))).
- Return missing.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1603) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1579)

<a id="op-bdedc969db60c6"></a>
### Document.get missing mandatory fields.get msg

`operation_foundation_binding_foundation_model_document_document_get_missing_mandatory_fields_get_msg`

**Inputs** df.

**Explicit results** translated “Error: Data missing in table {0}”.format(\_(df.label, context = df.parent)) · translated “Error: {0} Row #{1}: Value missing for: {2}”.format(Platform.bold(translated self.doctype), self.idx, \_(df.label, context = df.parent)) · translated “Error: Value missing for {0}: {1}”.format(translated df.parent, \_(df.label, context = df.parent)).

**Local steps**

- If df.fieldtype belongs to table\_fields.
  - Return translated “Error: Data missing in table {0}”.format(\_(df.label, context = df.parent)).
- Otherwise.
  - If self.get(“parentfield”).
    - Return translated “Error: {0} Row #{1}: Value missing for: {2}”.format(Platform.bold(translated self.doctype), self.idx, \_(df.label, context = df.parent)).
- Return translated “Error: Value missing for {0}: {1}”.format(translated df.parent, \_(df.label, context = df.parent)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1604) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1580)

<a id="op-8091d7d784954e"></a>
### Document.get missing mandatory fields.has content

`operation_foundation_binding_foundation_model_document_document_get_missing_mandatory_fields_has_content`

**Inputs** df.

**Explicit results** true · has\_text\_content.

**Local steps**

- Set value from cstr(self.get(df.fieldname)).
- Set has\_text\_content from strip\_html(value).strip().
- Set has\_img\_tag from “&lt;img” belongs to value.
- Set has\_text\_or\_img\_tag from (has\_text\_content or has\_img\_tag).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_text\_content → has\_img\_tag.
- If (df.fieldtype equals “Text Editor” and has\_text\_or\_img\_tag).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Text Editor” → has\_text\_or\_img\_tag.
  - Return true.
- Otherwise.
  - If (df.fieldtype equals “Code” and df.options equals “HTML” and has\_text\_or\_img\_tag).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Code” → df.options equals “HTML” → has\_text\_or\_img\_tag.
    - Return true.
  - Otherwise.
    - If df.fieldtype equals “Check”.
      - Return true.
    - Otherwise.
      - Return has\_text\_content.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1605) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1581)

<a id="op-0273ce8eb431f0"></a>
### Document.get invalid links

`operation_foundation_binding_foundation_model_document_document_get_invalid_links`

**Inputs** self, is\_submittable = false.

**Record and data access** read doctype via get\_value · resolve a document from doctype via get\_doc.

**Explicit results** tuple(invalid\_links, cancelled\_links).

**Explicit failure paths** validation helper — translated “Options not set for link field {0}”.format(df.fieldname) · validation helper — translated “{0} must be set first”.format(translated self.meta.get\_label(df.options)).

**Local steps**

- Set is\_submittable from (is\_submittable or self.meta.is\_submittable).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_submittable → self.meta.is\_submittable.
- Bind local operation get\_msg for subsequent calls.
- Set invalid\_links from list().
- Set cancelled\_links from list().
- For each df in (self.meta.get\_link\_fields() + self.meta.get(“fields”, mapping(“fieldtype” → tuple(“=”, “Dynamic Link”)))).
  - Set docname from self.get(df.fieldname).
  - If not docname.
    - Continue with the next iteration or loop test.
  - Require isinstance(docname, (str bitwise or int)) or report formatted text Unexpected value for field {df.fieldname}: {docname}.
  - If df.fieldtype equals “Link”.
    - Set doctype from df.options.
    - If not doctype.
      - Call the validation error handler Platform.throw(translated “Options not set for link field {0}”.format(df.fieldname)).
  - Otherwise.
    - Require df.fieldtype equals “Dynamic Link” or raise an assertion failure.
    - Set doctype from self.get(df.options).
    - If not doctype.
      - Call the validation error handler Platform.throw(translated “{0} must be set first”.format(translated self.meta.get\_label(df.options))).
    - Evaluate invalidate\_distinct\_link\_doctypes(df.parent, df.options, doctype).
  - Set meta from Platform.get\_meta(doctype).
  - If not meta.istable.
    - Evaluate notify\_link\_count(doctype, docname).
  - Set check\_docstatus from (is\_submittable and Platform.get\_meta(doctype).is\_submittable).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_submittable → Platform.get\_meta(doctype).is\_submittable.
  - Set fields\_to\_fetch from list of \_df for \_df drawn from self.meta.get\_fields\_to\_fetch(df.fieldname) where (not \_df.get(“fetch\_if\_empty”) or (\_df.get(“fetch\_if\_empty”) and not self.get(\_df.fieldname))).
    - Draw \_df from self.meta.get\_fields\_to\_fetch(df.fieldname), keep a combination only if ((not \_df.get(“fetch\_if\_empty”) or (\_df.get(“fetch\_if\_empty”) and not self.get(\_df.fieldname)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not \_df.get(“fetch\_if\_empty”) → (\_df.get(“fetch\_if\_empty”) and not self.get(\_df.fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_df.get(“fetch\_if\_empty”) → not self.get(\_df.fieldname).
  - Set values\_to\_fetch from tuple(“name”, expanded generator of nested operand in the contract.fetch\_from.split(“.”) at negative 1 for \_df drawn from fields\_to\_fetch).
    - Draw \_df from fields\_to\_fetch.
  - If check\_docstatus.
    - Update values\_to\_fetch using + tuple(“docstatus”).
  - If not meta.get(“is\_virtual”).
    - Set values from Platform.db.get\_value(doctype, docname, values\_to\_fetch, as\_dict = true, cache = true, order\_by = no value).
    - If not values.
      - Set values from Platform.db.get\_value(doctype, docname, values\_to\_fetch, as\_dict = true, order\_by = no value).
  - Otherwise.
    - Set values from Platform.get\_doc(doctype, docname).as\_dict().
  - Set values from (values or \_dict.fromkeys(values\_to\_fetch, no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → \_dict.fromkeys(values\_to\_fetch, no value).
  - If getattr(meta, “issingle”, 0).
    - Set values.name from doctype.
  - If not df.get(“is\_virtual”).
    - Evaluate setattr(self, df.fieldname, values.name).
  - For each \_df in fields\_to\_fetch.
    - If (self.is\_new() or not self.docstatus.is\_submitted() or \_df.allow\_on\_submit).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.docstatus.is\_submitted() → \_df.allow\_on\_submit.
      - Evaluate self.set\_fetch\_from\_value(doctype, \_df, values).
  - If not values.name.
    - Evaluate invalid\_links.append(tuple(df.fieldname, docname, get\_msg(df, docname))).
  - Otherwise.
    - If (df.fieldname differs from “amended\_from” and check\_docstatus and DocStatus((values.docstatus or 0)).is\_cancelled()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldname differs from “amended\_from” → check\_docstatus → DocStatus((values.docstatus or 0)).is\_cancelled().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in values.docstatus → 0.
      - Evaluate cancelled\_links.append(tuple(df.fieldname, docname, get\_msg(df, docname))).
- Return tuple(invalid\_links, cancelled\_links).

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [is new](operations-046.md#op-e2def851dd1371), [set fetch from value](operations-046.md#op-7a4b5a954ea819).

**Values supplied outside this operation** selected callable from getattr(meta, “issingle”, 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1600) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1576)

<a id="op-dd6ec7dbc4c43f"></a>
### Document.get invalid links.get msg

`operation_foundation_binding_foundation_model_document_document_get_invalid_links_get_msg`

**Inputs** df, docname.

**Explicit results** “{} #{}: {}: {}”.format(translated “Row”, self.idx, \_(df.label, context = df.parent), docname) · formatted text {\_(df.label, context = df.parent)}: {docname}.

**Local steps**

- If self.get(“parentfield”).
  - Return “{} #{}: {}: {}”.format(translated “Row”, self.idx, \_(df.label, context = df.parent), docname).
- Return formatted text {\_(df.label, context = df.parent)}: {docname}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1601) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1577)

<a id="op-7a4b5a954ea819"></a>
### Document.set fetch from value

`operation_foundation_binding_foundation_model_document_document_set_fetch_from_value`

**Inputs** self, doctype, df, values.

**Explicit failure paths** validation helper — translated “Please check the value of "Fetch From" set for field {0}”.format(Platform.bold(df.label)).

**Local steps**

- Set fetch\_from\_fieldname from df.fetch\_from.split(“.”) at negative 1.
- Set value from values at fetch\_from\_fieldname.
- If df.fieldtype belongs to list(“Small Text”, “Text”, “Data”).
  - Bind dependencies get\_default\_df.
  - Set fetch\_from\_df from (get\_default\_df(fetch\_from\_fieldname) or Platform.get\_meta(doctype).get\_field(fetch\_from\_fieldname)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_default\_df(fetch\_from\_fieldname) → Platform.get\_meta(doctype).get\_field(fetch\_from\_fieldname).
  - If not fetch\_from\_df.
    - Call the validation error handler Platform.throw(translated “Please check the value of "Fetch From" set for field {0}”.format(Platform.bold(df.label)), title = translated “Wrong Fetch From value”).
  - Set fetch\_from\_ft from fetch\_from\_df.get(“fieldtype”).
  - If (fetch\_from\_ft equals “Text Editor” and value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fetch\_from\_ft equals “Text Editor” → value.
    - Set value from unescape\_html(strip\_html(value)).
- Evaluate setattr(self, df.fieldname, value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1615)

<a id="op-db82aaefb80d1a"></a>
### Document.validate selects

`operation_foundation_binding_foundation_model_document_document_validate_selects`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} {1} cannot be "{2}". It should be one of "{3}"”.format(prefix, label, value, comma\_options).

**Local steps**

- If Platform.flags.in\_import.
  - Return no value.
- For each df in self.meta.get\_select\_fields().
  - If (df.fieldname equals “naming\_series” or not self.get(df.fieldname) or not df.options).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldname equals “naming\_series” → not self.get(df.fieldname) → not df.options.
    - Continue with the next iteration or loop test.
  - Set options from (df.options or empty text).split(whitespace '\\n').
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.options → empty text.
  - If not filter(no value, options).
    - Continue with the next iteration or loop test.
  - Evaluate self.set(df.fieldname, cstr(self.get(df.fieldname)).strip()).
  - Set value from self.get(df.fieldname).
  - If (value does not belong to options and not (Platform.in\_test and value.startswith(“\_T-”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value does not belong to options → not (Platform.in\_test and value.startswith(“\_T-”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.in\_test → value.startswith(“\_T-”).
    - Set prefix from translated “Row #{0}:”.format(self.idx) when self.get(“parentfield”), otherwise empty text.
      - Value choice on self.get(“parentfield”) — true gives translated “Row #{0}:”.format(self.idx), false gives empty text.
    - Set label from translated self.meta.get\_label(df.fieldname).
    - Set comma\_options from “", "”.join(generator of translated each for each drawn from options).
      - Draw each from options.
    - Call the validation error handler Platform.throw(translated “{0} {1} cannot be "{2}". It should be one of "{3}"”.format(prefix, label, value, comma\_options)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L195) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1627)
