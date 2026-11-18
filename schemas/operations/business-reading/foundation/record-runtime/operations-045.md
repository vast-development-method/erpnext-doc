# Record lifecycle and persistence · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-3fe732946ccc3d"></a>
### Document.weakref

`operation_foundation_binding_foundation_model_document_document_weakref`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** weakref.ref(self).

**Local steps**

- Return weakref.ref(self).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L197) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1629)

<a id="op-dd41c3918e015f"></a>
### Document.getstate

`operation_foundation_binding_foundation_model_document_document_getstate`

**Inputs** self.

**Explicit results** state.

**Local steps**

- Set state from self.\_\_dict\_\_.copy().
- Evaluate self.remove\_unpicklable\_values(state).
- Return state.

**Methods declared on this owner** [remove unpicklable values](operations-045.md#op-812901ece97e8b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1614) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1590)

<a id="op-812901ece97e8b"></a>
### Document.remove unpicklable values

`operation_foundation_binding_foundation_model_document_document_remove_unpicklable_values`

**Inputs** self, state.

**Local steps**

- For each key in UNPICKLABLE\_KEYS.
  - If key belongs to state.
    - Remove state at key.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1634) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1610)

<a id="op-b90034268a7194"></a>
### Document.update

`operation_foundation_binding_foundation_model_document_document_update`

**Inputs** self, d.

**Explicit results** self.

**Local steps**

- Evaluate self.\_\_dict\_\_.update(generator of key\_val for key\_val drawn from d.items() where key\_val at 0 does not belong to RESERVED\_KEYWORDS).
  - Draw key\_val from d.items(), keep a combination only if (key\_val at 0 does not belong to RESERVED\_KEYWORDS).
- If (not self.\_table\_fieldnames or self.flags.get(“ignore\_children”, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.\_table\_fieldnames → self.flags.get(“ignore\_children”, false).
  - Return self.
- Set \_\_dict from self.\_\_dict\_\_.
- For each key in self.\_table\_fieldnames.
  - If key does not belong to \_\_dict.
    - Continue with the next iteration or loop test.
  - Set value from \_\_dict at key.
  - Set \_\_dict at key from list().
  - If value.
    - Evaluate self.extend(key, value).
- Return self.

**Methods declared on this owner** [extend](operations-045.md#op-aefc991ffd6b0a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1620)

<a id="op-1cf98cd7adffc8"></a>
### Document.update if missing

`operation_foundation_binding_foundation_model_document_document_update_if_missing`

**Inputs** self, d.

**Local steps**

- If isinstance(d, Document).
  - Set d from d.get\_valid\_dict().
- For each tuple(key, value) in d.items().
  - If (value is distinct from no value and self.get(key) is identical to no value and key does not belong to self.dont\_update\_if\_missing).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is distinct from no value → self.get(key) is identical to no value → key does not belong to self.dont\_update\_if\_missing.
    - Evaluate self.set(key, value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1621)

<a id="op-af17db61c2ff72"></a>
### Document.get db value

`operation_foundation_binding_foundation_model_document_document_get_db_value`

**Inputs** self, key.

**Record and data access** read self.doctype via get\_value.

**Explicit results** Platform.db.get\_value(self.doctype, self.name, key).

**Local steps**

- Return Platform.db.get\_value(self.doctype, self.name, key).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L141) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1597) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1573)

<a id="op-59f5a4cf162623"></a>
### Document.get

`operation_foundation_binding_foundation_model_document_document_get`

**Inputs** self, key, filters = no value, limit = no value, default = no value.

**Explicit results** \_filter(self.get\_all\_children(), key, limit = limit) · \_filter(self.\_\_dict\_\_.get(key, list()), filters, limit = limit) · value.

**Local steps**

- If isinstance(key, dict).
  - Return \_filter(self.get\_all\_children(), key, limit = limit).
- If filters.
  - If isinstance(filters, dict).
    - Return \_filter(self.\_\_dict\_\_.get(key, list()), filters, limit = limit).
  - Set default from filters.
- Set value from self.\_\_dict\_\_.get(key, default).
- If (limit and isinstance(value, (list bitwise or tuple)) and len(value) &gt; limit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → isinstance(value, (list bitwise or tuple)) → len(value) &gt; limit.
  - Set value from value at slice no value to limit.
- Return value.

**Methods declared on this owner** [get all children](operations-042.md#op-c0f0e764f5c4d1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1596) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1572)

<a id="op-f44a6f80a8b178"></a>
### Document.getone

`operation_foundation_binding_foundation_model_document_document_getone`

**Inputs** self, key, filters = no value.

**Explicit results** self.get(key, filters = filters, limit = 1) at 0.

**Local steps**

- Return self.get(key, filters = filters, limit = 1) at 0.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1589)

<a id="op-b58a481a5882b4"></a>
### Document.set

`operation_foundation_binding_foundation_model_document_document_set`

**Inputs** self, key, value, as\_value = false.

**Explicit results** no value.

**Local steps**

- If key belongs to RESERVED\_KEYWORDS.
  - Return no value.
- If (not as\_value and key belongs to self.\_table\_fieldnames).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not as\_value → key belongs to self.\_table\_fieldnames.
  - Set self.\_\_dict\_\_ at key from list().
  - If value.
    - Evaluate self.extend(key, value).
  - Return no value.
- Set self.\_\_dict\_\_ at key from value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [extend](operations-045.md#op-aefc991ffd6b0a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1614)

<a id="op-922ceff54a0482"></a>
### Document.delete key

`operation_foundation_binding_foundation_model_document_document_delete_key`

**Inputs** self, key.

**Local steps**

- If key belongs to self.\_\_dict\_\_.
  - Remove self.\_\_dict\_\_ at key.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L133) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1565)

<a id="op-3842faa8315613"></a>
### Document.append

`operation_foundation_binding_foundation_model_document_document_append`

**Inputs** self, key, value = no value, position = negative 1.

**Declared result** D.

**State and service calls** call insert on table.

**Explicit results** d.

**Local steps**

- If value is identical to no value.
  - Set value from mapping().
- If table bound to self.\_\_dict\_\_.get(key) is identical to no value.
  - Set self.\_\_dict\_\_ at key, table from list().
- Set d from self.\_init\_child(value, key).
- If position equals negative 1.
  - Evaluate table.append(d).
  - If not getattr(d, “idx”, false).
    - Set d.idx from len(table).
- Otherwise.
  - Evaluate table.insert(position, d).
  - For each tuple(i, \_d) in enumerate(table, 1).
    - Set \_d.idx from i.
- Set d.\_parent\_doc from self.\_weakref.
- Return d.

**Methods declared on this owner** [init child](operations-045.md#op-2ff30203a52cba).

**Values supplied outside this operation** selected callable from getattr(d, “idx”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L125) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1557)

<a id="op-7f03ca6cc645fe"></a>
### Document.parent doc

`operation_foundation_binding_foundation_model_document_document_parent_doc`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** parent\_doc\_ref() · parent\_doc\_ref.

**Local steps**

- Set parent\_doc\_ref from getattr(self, “\_parent\_doc”, no value).
- If isinstance(parent\_doc\_ref, weakref.ReferenceType).
  - Return parent\_doc\_ref().
- Otherwise.
  - If isinstance(parent\_doc\_ref, Document).
    - Return parent\_doc\_ref.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “\_parent\_doc”, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1628) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1604)

<a id="op-c3f7ea0f657db9"></a>
### Document.parent doc

`operation_foundation_binding_foundation_model_document_document_parent_doc_occurrence_2`

**Inputs** self, value.

**Wrappers, in declaration order** parent\_doc.setter.

**Local steps**

- Set self.\_parent\_doc from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1605)

<a id="op-85841da8bcf39b"></a>
### Document.parent doc

`operation_foundation_binding_foundation_model_document_document_parent_doc_occurrence_3`

**Inputs** self.

**Wrappers, in declaration order** parent\_doc.deleter.

**Local steps**

- Set self.\_parent\_doc from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1630) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1606)

<a id="op-aefc991ffd6b0a"></a>
### Document.extend

`operation_foundation_binding_foundation_model_document_document_extend`

**Inputs** self, key, value.

**Explicit failure paths** ValueError.

**Local steps**

- Attempt the following.
  - Set value from iter(value).
- On failure (TypeError).
  - Raise ValueError.
- For each v in value.
  - Evaluate self.append(key, v).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append](operations-045.md#op-3842faa8315613).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1569)

<a id="op-c55cc8c0484986"></a>
### Document.remove

`operation_foundation_binding_foundation_model_document_document_remove`

**Inputs** self, doc.

**Local steps**

- If doc.get(“parentfield”).
  - Evaluate self.get(doc.parentfield).remove(doc).
  - For each tuple(i, \_d) in enumerate(self.get(doc.parentfield)).
    - Set \_d.idx from (i + 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1609)

<a id="op-2ff30203a52cba"></a>
### Document.init child

`operation_foundation_binding_foundation_model_document_document_init_child`

**Inputs** self, value, key.

**Explicit results** child.

**Explicit failure paths** AttributeError(key).

**Local steps**

- If isinstance(value, Document).
  - Set child from value.
- Otherwise.
  - Set doctype from self.\_table\_fieldnames.get(key).
  - If not doctype.
    - Raise AttributeError(key).
  - Set value at “doctype” from doctype.
  - Set controller from get\_controller(doctype).
  - Set child from controller.\_\_new\_\_(controller).
  - Set child.\_table\_fieldnames from TABLE\_DOCTYPES\_FOR\_CHILD\_TABLES.
  - Set child.\_non\_computed\_table\_fieldnames from TABLE\_DOCTYPES\_FOR\_CHILD\_TABLES.
  - Evaluate child.\_\_init\_\_(value).
- Set \_\_dict from child.\_\_dict\_\_.
- Set \_\_dict at “parent” from self.name.
- Set \_\_dict at “parenttype” from self.doctype.
- Set \_\_dict at “parentfield” from key.
- If \_\_dict.get(“docstatus”) is identical to no value.
  - Set \_\_dict at “docstatus” from DocStatus.DRAFT.
- If not \_\_dict.get(“name”).
  - Set \_\_dict at “\_\_islocal” from 1.
  - Set \_\_dict at “\_\_temporary\_name” from Platform.generate\_hash(length = 10).
- Return child.

**Values supplied outside this operation** selected callable from get\_controller(doctype) · clock or generated value from Platform.generate\_hash(length = 10).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1618) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1594)

<a id="op-5c1ab334c7443b"></a>
### Document.table fieldnames

`operation_foundation_binding_foundation_model_document_document_table_fieldnames`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict.

**Explicit results** TABLE\_DOCTYPES\_FOR\_DOCTYPE · TABLE\_DOCTYPES\_FOR\_CHILD\_TABLES · self.meta.\_table\_doctypes.

**Local steps**

- If self.doctype equals “DocType”.
  - Return TABLE\_DOCTYPES\_FOR\_DOCTYPE.
- If self.doctype belongs to DOCTYPES\_FOR\_DOCTYPE.
  - Return TABLE\_DOCTYPES\_FOR\_CHILD\_TABLES.
- Return self.meta.\_table\_doctypes.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1618)

<a id="op-be1db26d02028c"></a>
### Document.non computed table fieldnames

`operation_foundation_binding_foundation_model_document_document_non_computed_table_fieldnames`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict.

**Explicit results** self.\_table\_fieldnames · self.meta.\_non\_computed\_table\_doctypes.

**Local steps**

- If self.doctype belongs to DOCTYPES\_FOR\_DOCTYPE.
  - Return self.\_table\_fieldnames.
- Return self.meta.\_non\_computed\_table\_doctypes.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1627) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1603)

<a id="op-d508943f051a0a"></a>
### Document.get table fields

`operation_foundation_binding_foundation_model_document_document_get_table_fields`

**Inputs** self, include\_computed = false.

**Explicit results** DOCTYPE\_TABLE\_FIELDS · tuple() · self.meta.get\_table\_fields(include\_computed = include\_computed).

**Local steps**

- If self.doctype equals “DocType”.
  - Return DOCTYPE\_TABLE\_FIELDS.
- If self.doctype belongs to DOCTYPES\_FOR\_DOCTYPE.
  - Return tuple().
- Return self.meta.get\_table\_fields(include\_computed = include\_computed).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1609) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1585)

<a id="op-fd495712e2e49d"></a>
### Document.evaluate virtual field options

`operation_foundation_binding_foundation_model_document_document_evaluate_virtual_field_options`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, options.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1592) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1568)

<a id="op-c47e5bad7a2c34"></a>
### Document.get valid dict

`operation_foundation_binding_foundation_model_document_document_get_valid_dict`

**Inputs** self, sanitize = true, convert\_dates\_to\_str = false, ignore\_nulls = false, ignore\_virtual = false.

**Declared result** \_dict.

**Explicit results** d.

**Explicit failure paths** validation helper — translated “Value for {0} cannot be a list”.format(\_(df.label, context = df.parent)).

**Local steps**

- Set d from \_dict().
- Set field\_values from self.\_\_dict\_\_.
- Set field\_map from self.meta.\_fields.
- Set masked\_fieldnames from self.flags.get(“masked\_fieldnames”).
- For each fieldname in self.meta.get\_valid\_fields().
  - Set value from field\_values.get(fieldname).
  - If (value and fieldname belongs to (masked\_fieldnames or tuple())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → fieldname belongs to (masked\_fieldnames or tuple()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in masked\_fieldnames → tuple().
    - Set d at fieldname from value.
    - Continue with the next iteration or loop test.
  - If (not sanitize and value is identical to no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sanitize → value is identical to no value.
    - Set d at fieldname from no value.
    - Continue with the next iteration or loop test.
  - Set df from field\_map.get(fieldname).
  - Set is\_virtual\_field from getattr(df, “is\_virtual”, false).
  - If df.
    - If is\_virtual\_field.
      - If (ignore\_virtual or fieldname does not belong to self.permitted\_fieldnames).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_virtual → fieldname does not belong to self.permitted\_fieldnames.
        - Continue with the next iteration or loop test.
      - If (prop bound to getattr(type(self), fieldname, no value) and is\_a\_property(prop)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop bound to getattr(type(self), fieldname, no value) → is\_a\_property(prop).
        - Set value from getattr(self, fieldname).
      - Otherwise.
        - If options bound to getattr(df, “options”, no value).
          - Set value from self.\_evaluate\_virtual\_field\_options(options).
    - Set fieldtype from df.fieldtype.
    - If (isinstance(value, list) and fieldtype does not belong to table\_fields).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, list) → fieldtype does not belong to table\_fields.
      - Call the validation error handler Platform.throw(translated “Value for {0} cannot be a list”.format(\_(df.label, context = df.parent))).
    - If fieldtype equals “Check”.
      - Set value from 1 when cint(value), otherwise 0.
        - Value choice on cint(value) — true gives 1, false gives 0.
    - Otherwise.
      - If (fieldtype equals “Int” and not isinstance(value, int)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Int” → not isinstance(value, int).
        - Set value from cint(value).
      - Otherwise.
        - If (fieldtype equals “JSON” and isinstance(value, dict)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “JSON” → isinstance(value, dict).
          - Set value from json.dumps(value, separators = tuple(“,”, “:”)).
        - Otherwise.
          - If (fieldtype belongs to float\_like\_fields and not isinstance(value, float)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype belongs to float\_like\_fields → not isinstance(value, float).
            - Set value from flt(value).
          - Otherwise.
            - If (fieldtype equals “Read Only” and value is distinct from no value and not isinstance(value, str)).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype equals “Read Only” → value is distinct from no value → not isinstance(value, str).
              - Set value from cstr(value).
            - Otherwise.
              - If ((fieldtype belongs to datetime\_fields and value equals empty text) or (getattr(df, “unique”, false) and cstr(value).strip() equals empty text)).
                - Evaluate in order, stop at the first true operand, otherwise use the last operand in (fieldtype belongs to datetime\_fields and value equals empty text) → (getattr(df, “unique”, false) and cstr(value).strip() equals empty text).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype belongs to datetime\_fields → value equals empty text.
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(df, “unique”, false) → cstr(value).strip() equals empty text.
                - Set value from no value.
  - If (convert\_dates\_to\_str and isinstance(value, DatetimeTypes)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in convert\_dates\_to\_str → isinstance(value, DatetimeTypes).
    - Set value from str(value).
  - If (ignore\_nulls and not is\_virtual\_field and value is identical to no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore\_nulls → not is\_virtual\_field → value is identical to no value.
    - Continue with the next iteration or loop test.
  - If (value is identical to no value and getattr(df, “not\_nullable”, false)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value is identical to no value → getattr(df, “not\_nullable”, false).
    - If df.default.
      - Set value from df.default.
    - Otherwise.
      - Set value from get\_not\_null\_defaults(df.fieldtype).
  - Set d at fieldname from value.
- Return d.

**Methods declared on this owner** [evaluate virtual field options](operations-045.md#op-fd495712e2e49d).

**Values supplied outside this operation** selected callable from getattr(df, “is\_virtual”, false), getattr(type(self), fieldname, no value) and 4 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1611) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1587)

<a id="op-fa5f865a65cb4e"></a>
### Document.init child tables

`operation_foundation_binding_foundation_model_document_document_init_child_tables`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.\_non\_computed\_table\_fieldnames.
  - Return no value.
- Set \_\_dict from self.\_\_dict\_\_.
- For each fieldname in self.\_non\_computed\_table\_fieldnames.
  - If \_\_dict.get(fieldname) is identical to no value.
    - Set \_\_dict at fieldname from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1619) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1595)

<a id="op-7a338f17f8457f"></a>
### Document.init valid columns

`operation_foundation_binding_foundation_model_document_document_init_valid_columns`

**Inputs** self.

**Local steps**

- Set \_\_dict from self.\_\_dict\_\_.
- If \_\_dict.get(“docstatus”) is identical to no value.
  - Set \_\_dict at “docstatus” from DocStatus.DRAFT.
- If \_\_dict.get(“idx”) is identical to no value.
  - Set \_\_dict at “idx” from 0.
- For each key in self.get\_valid\_columns().
  - If key does not belong to \_\_dict.
    - Set \_\_dict at key from no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get valid columns](operations-046.md#op-a9935a702ba2d8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1621) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1597)
