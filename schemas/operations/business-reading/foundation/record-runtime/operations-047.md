# Record lifecycle and persistence · operations 47

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-8d6ef10ed6f164"></a>
### Document.validate data fields

`operation_foundation_binding_foundation_model_document_document_validate_data_fields`

**Inputs** self.

**Local steps**

- Bind dependencies split\_emails, validate\_email\_address, validate\_iban, validate\_name, validate\_phone\_number, validate\_phone\_number\_with\_country\_code, validate\_url.
- For each phone\_field in self.meta.get\_phone\_fields().
  - Set phone from self.get(phone\_field.fieldname).
  - Evaluate validate\_phone\_number\_with\_country\_code(phone, phone\_field.fieldname, translated phone\_field.label).
- For each data\_field in self.meta.get\_data\_fields().
  - Set data from self.get(data\_field.fieldname).
  - If not data.
    - Continue with the next iteration or loop test.
  - Set data\_field\_options from data\_field.get(“options”).
  - Set old\_fieldtype from data\_field.get(“oldfieldtype”).
  - If (old\_fieldtype and old\_fieldtype differs from “Data”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_fieldtype → old\_fieldtype differs from “Data”.
    - Continue with the next iteration or loop test.
  - If data\_field\_options equals “Email”.
    - If (self.owner belongs to Platform.STANDARD\_USERS and data belongs to Platform.STANDARD\_USERS).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.owner belongs to Platform.STANDARD\_USERS → data belongs to Platform.STANDARD\_USERS.
      - Continue with the next iteration or loop test.
    - For each email\_address in split\_emails(data).
      - Evaluate validate\_email\_address(email\_address, throw = true).
  - If data\_field\_options equals “Name”.
    - Evaluate validate\_name(data, throw = true).
  - If data\_field\_options equals “Phone”.
    - Evaluate validate\_phone\_number(data, throw = true).
  - If data\_field\_options equals “URL”.
    - Evaluate validate\_url(data, throw = true).
  - If data\_field\_options equals “IBAN”.
    - Evaluate validate\_iban(data, throw = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1625)

<a id="op-3136b4a506d671"></a>
### Document.validate constants

`operation_foundation_binding_foundation_model_document_document_validate_constants`

**Inputs** self.

**Record and data access** read self.doctype via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.CannotChangeConstantError — translated “Value cannot be changed for {0}”.format(translated self.meta.get\_label(fieldname)).

**Local steps**

- If (Platform.flags.in\_import or self.is\_new() or self.flags.ignore\_validate\_constants).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → self.is\_new() → self.flags.ignore\_validate\_constants.
  - Return no value.
- Set constants from list of d.fieldname for d drawn from self.meta.get(“fields”, mapping(“set\_only\_once” → tuple(“=”, 1))).
  - Draw d from self.meta.get(“fields”, mapping(“set\_only\_once” → tuple(“=”, 1))).
- If constants.
  - Set values from Platform.db.get\_value(self.doctype, self.name, constants, as\_dict = true).
- For each fieldname in constants.
  - Set df from self.meta.get\_field(fieldname).
  - If (df.fieldtype equals “Date” or df.fieldtype equals “Datetime”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype equals “Date” → df.fieldtype equals “Datetime”.
    - Set value from str(values.get(fieldname)).
  - Otherwise.
    - Set value from values.get(fieldname).
  - If self.get(fieldname) differs from value.
    - Call the validation error handler Platform.throw(translated “Value cannot be changed for {0}”.format(translated self.meta.get\_label(fieldname)), Platform.CannotChangeConstantError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371), [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1624)

<a id="op-bd0f80066421dc"></a>
### Document.validate length

`operation_foundation_binding_foundation_model_document_document_validate_length`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_install.
  - Return no value.
- If getattr(self.meta, “issingle”, 0).
  - Return no value.
- Set type\_map from Platform.db.type\_map.
- For each tuple(fieldname, value) in self.get\_valid\_dict(ignore\_virtual = true).items().
  - Set df from self.meta.get\_field(fieldname).
  - If (not df or df.fieldtype equals “Check”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → df.fieldtype equals “Check”.
    - Continue with the next iteration or loop test.
  - Set column\_type from (type\_map at df.fieldtype at 0 or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in type\_map at df.fieldtype at 0 → no value.
  - If column\_type equals “varchar”.
    - Set default\_column\_max\_length from (type\_map at df.fieldtype at 1 or no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in type\_map at df.fieldtype at 1 → no value.
    - Set max\_length from (cint(df.get(“length”)) or cint(default\_column\_max\_length)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(df.get(“length”)) → cint(default\_column\_max\_length).
    - If len(cstr(value)) &gt; max\_length.
      - Evaluate self.throw\_length\_exceeded\_error(df, max\_length, value).
  - Otherwise.
    - If column\_type belongs to tuple(“int”, “bigint”, “smallint”).
      - If cint(df.get(“length”)) &gt; 11.
        - Set column\_type from “bigint”.
      - Set max\_length from max\_positive\_value at column\_type.
      - If abs(cint(value)) &gt; max\_length.
        - Evaluate self.throw\_length\_exceeded\_error(df, max\_length, value).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get valid dict](operations-045.md#op-c47e5bad7a2c34), [throw length exceeded error](operations-047.md#op-9288e2d875c875).

**Values supplied outside this operation** selected callable from getattr(self.meta, “issingle”, 0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1626)

<a id="op-49e0d321a3c074"></a>
### Document.validate code fields

`operation_foundation_binding_foundation_model_document_document_validate_code_fields`

**Inputs** self.

**Local steps**

- For each field in self.meta.get\_code\_fields().
  - Set code\_string from self.get(field.fieldname).
  - Set language from field.get(“options”).
  - If language equals “Python”.
    - Evaluate Platform.utils.validate\_python\_code(code\_string, fieldname = field.label, is\_expression = false).
  - Otherwise.
    - If language equals “PythonExpression”.
      - Evaluate Platform.utils.validate\_python\_code(code\_string, fieldname = field.label).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1623)

<a id="op-ecd0b3b9981a24"></a>
### Document.sync autoname field

`operation_foundation_binding_foundation_model_document_document_sync_autoname_field`

**Inputs** self.

**Local steps**

- Set autoname from (self.meta.autoname or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta.autoname → empty text.
- Set tuple(\_empty, \_field\_specifier, fieldname) from autoname.partition(“field:”).
- If (fieldname and self.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname → self.name.
  - Set df from self.meta.get\_field(fieldname).
  - Set name from self.cast(self.name, df) when df, otherwise self.name.
    - Value choice on df — true gives self.cast(self.name, df), false gives self.name.
  - If name differs from self.get(fieldname).
    - Evaluate self.set(fieldname, name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [cast](operations-047.md#op-289ab0d75de6e9), [get](operations-045.md#op-59f5a4cf162623), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1617)

<a id="op-9288e2d875c875"></a>
### Document.throw length exceeded error

`operation_foundation_binding_foundation_model_document_document_throw_length_exceeded_error`

**Inputs** self, df, max\_length, value.

**Explicit failure paths** validation helper with Platform.CharacterLengthExceededError — translated “{0}: '{1}' ({3}) will get truncated, as max characters allowed is {2}”.format(reference, Platform.bold(\_(df.label, context = df.parent)), max\_length, value).

**Local steps**

- If self.get(“parentfield”).
  - Set reference from translated “{0}, Row {1}”.format(translated self.doctype, self.idx).
- Otherwise.
  - Set reference from formatted text {translated self.doctype} {self.name}.
- Call the validation error handler Platform.throw(translated “{0}: '{1}' ({3}) will get truncated, as max characters allowed is {2}”.format(reference, Platform.bold(\_(df.label, context = df.parent)), max\_length, value), Platform.CharacterLe ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1619)

<a id="op-59d4171df5447f"></a>
### Document.validate update after submit

`operation_foundation_binding_foundation_model_document_document_validate_update_after_submit`

**Inputs** self.

**Record and data access** resolve a document from self.doctype via get\_doc.

**Explicit failure paths** validation helper with Platform.UpdateAfterSubmitError — translated “{0} Not allowed to change {1} after submission from {2} to {3}”.format(formatted text Row #{self.idx}: when self.get(“parent”), otherwise empty text, Platform.bold(\_(df.label, context = df.pare ….

**Local steps**

- Set db\_values from Platform.get\_doc(self.doctype, self.name).as\_dict().
- For each key in self.as\_dict().
  - Set df from self.meta.get\_field(key).
  - Set db\_value from db\_values.get(key).
  - If (df and not df.allow\_on\_submit and not df.is\_virtual and (self.get(key) or db\_value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → not df.allow\_on\_submit → not df.is\_virtual → (self.get(key) or db\_value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(key) → db\_value.
    - If df.fieldtype belongs to table\_fields.
      - Set self\_value from len(self.get(key)).
      - Set db\_value from len(db\_value).
    - Otherwise.
      - Set self\_value from self.get\_value(key).
    - If (isinstance(self\_value, datetime.timedelta) and isinstance(db\_value, datetime.time)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(self\_value, datetime.timedelta) → isinstance(db\_value, datetime.time).
      - Set db\_value from datetime.timedelta(hours = db\_value.hour, minutes = db\_value.minute, seconds = db\_value.second, microseconds = db\_value.microsecond).
    - If self\_value differs from db\_value.
      - Call the validation error handler Platform.throw(translated “{0} Not allowed to change {1} after submission from {2} to {3}”.format(formatted text Row #{self.idx}: when self.get(“parent”), otherwise empty text, Platform.bold(\_(df.label, co ….
        - Value choice on self.get(“parent”) — true gives formatted text Row #{self.idx}:, false gives empty text.

If control reaches the end, it returns no value.

**Methods declared on this owner** [as dict](operations-046.md#op-8dc085dc083de4), [get](operations-045.md#op-59f5a4cf162623), [get value](operations-047.md#op-ff10734b5e6f43).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1628)

<a id="op-c4ce48ce32d460"></a>
### Document.sanitize content

`operation_foundation_binding_foundation_model_document_document_sanitize_content`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1612)

<a id="op-32c96d5c4b050b"></a>
### Document.save passwords

`operation_foundation_binding_foundation_model_document_document_save_passwords`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1613)

<a id="op-ce22045291f1c8"></a>
### Document.get password

`operation_foundation_binding_foundation_model_document_document_get_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, fieldname, raise\_exception.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1607) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1583)

<a id="op-974483407e63db"></a>
### Document.is dummy password

`operation_foundation_binding_foundation_model_document_document_is_dummy_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, pwd.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1622) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1598)

<a id="op-0b10c9f2ef5edd"></a>
### Document.precision

`operation_foundation_binding_foundation_model_document_document_precision`

**Inputs** self, fieldname, parentfield = no value.

**Declared result** (int bitwise or no value).

**Explicit results** self.\_precision at cache\_key at fieldname.

**Local steps**

- Bind dependencies get\_field\_precision.
- If (parentfield and not isinstance(parentfield, str) and parentfield.get(“parentfield”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parentfield → not isinstance(parentfield, str) → parentfield.get(“parentfield”).
  - Set parentfield from parentfield.parentfield.
- Set cache\_key from (parentfield or “main”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parentfield → “main”.
- If not hasattr(self, “\_precision”).
  - Set self.\_precision from \_dict().
- If cache\_key does not belong to self.\_precision.
  - Set self.\_precision at cache\_key from \_dict().
- If fieldname does not belong to self.\_precision at cache\_key.
  - Set self.\_precision at cache\_key at fieldname from no value.
  - Set doctype from self.meta.get\_field(parentfield).options when parentfield, otherwise self.doctype.
    - Value choice on parentfield — true gives self.meta.get\_field(parentfield).options, false gives self.doctype.
  - Set df from Platform.get\_meta(doctype).get\_field(fieldname).
  - If (df and df.fieldtype belongs to tuple(“Currency”, “Float”, “Percent”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype belongs to tuple(“Currency”, “Float”, “Percent”).
    - Set self.\_precision at cache\_key at fieldname from get\_field\_precision(df, self).
- Return self.\_precision at cache\_key at fieldname.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1632) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1608)

<a id="op-0708531a4c4b71"></a>
### Document.get formatted

`operation_foundation_binding_foundation_model_document_document_get_formatted`

**Inputs** self, fieldname, doc = no value, currency = no value, absolute\_value = false, translated = false, format = no value.

**Record and data access** read “Currency” via get\_value.

**Explicit results** format\_value(val, df = df, doc = doc, currency = currency, format = format).

**Local steps**

- Bind dependencies format\_value.
- Set df from self.meta.get\_field(fieldname).
- If not df.
  - Bind dependencies get\_default\_df.
  - Set df from get\_default\_df(fieldname).
- If (df and df.fieldtype equals “Currency” and not currency and currency\_field bound to df.get(“options”) and currency\_value bound to self.get(currency\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Currency” → not currency → currency\_field bound to df.get(“options”) → currency\_value bound to self.get(currency\_field).
  - Set currency from Platform.db.get\_value(“Currency”, currency\_value, cache = true).
- Set val from self.get(fieldname).
- If translated.
  - Set val from translated val.
- If not doc.
  - Set doc from (getattr(self, “parent\_doc”, no value) or self).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(self, “parent\_doc”, no value) → self.
- If ((absolute\_value or doc.get(“absolute\_value”)) and isinstance(val, (int bitwise or float))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (absolute\_value or doc.get(“absolute\_value”)) → isinstance(val, (int bitwise or float)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in absolute\_value → doc.get(“absolute\_value”).
  - Set val from abs(self.get(fieldname)).
- Return format\_value(val, df = df, doc = doc, currency = currency, format = format).

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Values supplied outside this operation** selected callable from getattr(self, “parent\_doc”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L143) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1599) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1575)

<a id="op-151a7bf7ad5f4c"></a>
### Document.is print hide

`operation_foundation_binding_foundation_model_document_document_is_print_hide`

**Inputs** self, fieldname, df = no value, for\_print = true.

**Explicit results** true · print\_hide.

**Local steps**

- Set meta\_df from self.meta.get\_field(fieldname).
- If (meta\_df and meta\_df.get(“\_\_print\_hide”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta\_df → meta\_df.get(“\_\_print\_hide”).
  - Return true.
- Set print\_hide from 0.
- If (self.get(fieldname) equals 0 and not self.meta.istable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(fieldname) equals 0 → not self.meta.istable.
  - Set print\_hide from ((df and df.print\_hide\_if\_no\_value) or (meta\_df and meta\_df.print\_hide\_if\_no\_value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (df and df.print\_hide\_if\_no\_value) → (meta\_df and meta\_df.print\_hide\_if\_no\_value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.print\_hide\_if\_no\_value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta\_df → meta\_df.print\_hide\_if\_no\_value.
- If not print\_hide.
  - If (df and df.print\_hide is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.print\_hide is distinct from no value.
    - Set print\_hide from df.print\_hide.
  - Otherwise.
    - If meta\_df.
      - Set print\_hide from meta\_df.print\_hide.
- Return print\_hide.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1624) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1600)

<a id="op-a5d82dfa8d20ec"></a>
### Document.in format data

`operation_foundation_binding_foundation_model_document_document_in_format_data`

**Inputs** self, fieldname.

**Explicit results** fieldname belongs to doc.format\_data\_map · true.

**Local steps**

- Set doc from getattr(self, “parent\_doc”, self).
- If hasattr(doc, “format\_data\_map”).
  - Return fieldname belongs to doc.format\_data\_map.
- Otherwise.
  - Return true.

**Values supplied outside this operation** selected callable from getattr(self, “parent\_doc”, self).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1617) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1593)

<a id="op-9efa21377582a6"></a>
### Document.reset values if no permlevel access

`operation_foundation_binding_foundation_model_document_document_reset_values_if_no_permlevel_access`

**Inputs** self, has\_access\_to, high\_permlevel\_fields, mask\_fields = no value.

**Record and data access** read self.doctype via get\_value.

**State and service calls** request new\_doc for self.doctype.

**Explicit results** no value.

**Local steps**

- Set to\_reset from list of df for df drawn from high\_permlevel\_fields where (df.permlevel does not belong to has\_access\_to and df.fieldtype does not belong to display\_fieldtypes and df.fieldname does not belong to self.flags ….
  - Draw df from high\_permlevel\_fields, keep a combination only if ((df.permlevel does not belong to has\_access\_to and df.fieldtype does not belong to display\_fieldtypes and df.fieldname does not belong to self.flags.get(“ignore\_permlevel\_for\_fields”, list()))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.permlevel does not belong to has\_access\_to → df.fieldtype does not belong to display\_fieldtypes → df.fieldname does not belong to self.flags.get(“ignore\_permlevel\_for\_fields”, list()).
- If not mask\_fields.
  - Set mask\_fields from list().
- Set to\_reset from (to\_reset + mask\_fields).
- If not to\_reset.
  - Return no value.
- If self.is\_new().
  - Set ref\_doc from Platform.new\_doc(self.doctype).
- Otherwise.
  - If self.parent\_doc.
    - Set parent\_doc from self.parent\_doc.get\_latest().
    - Set child\_docs from list of d for d drawn from parent\_doc.get(self.parentfield) where d.name equals self.name.
      - Draw d from parent\_doc.get(self.parentfield), keep a combination only if (d.name equals self.name).
    - If not child\_docs.
      - Return no value.
    - Set ref\_doc from child\_docs at 0.
  - Otherwise.
    - Set ref\_doc from self.get\_latest().
- Set masked\_fieldnames from list of df.fieldname for df drawn from to\_reset where df.get(“mask\_readonly”).
  - Draw df from to\_reset, keep a combination only if (df.get(“mask\_readonly”)).
- Set ref\_values from mapping().
- If (not self.is\_new() and masked\_fieldnames).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → masked\_fieldnames.
  - Set ref\_values from (Platform.db.get\_value(self.doctype, self.name, masked\_fieldnames, as\_dict = true) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(self.doctype, self.name, masked\_fieldnames, as\_dict = true) → mapping().
- For each df in to\_reset.
  - If (df.get(“mask\_readonly”) and not self.is\_new()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.get(“mask\_readonly”) → not self.is\_new().
    - If df.fieldname belongs to ref\_values.
      - Evaluate self.set(df.fieldname, ref\_values at df.fieldname).
  - Otherwise.
    - Evaluate self.set(df.fieldname, ref\_doc.get(df.fieldname)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is new](operations-046.md#op-e2def851dd1371), [get latest](operations-040.md#op-cf6cca3d48a149), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1611)

<a id="op-ff10734b5e6f43"></a>
### Document.get value

`operation_foundation_binding_foundation_model_document_document_get_value`

**Inputs** self, fieldname.

**Explicit results** self.cast(val, df).

**Local steps**

- Set df from self.meta.get\_field(fieldname).
- Set val from self.get(fieldname).
- Return self.cast(val, df).

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [cast](operations-047.md#op-289ab0d75de6e9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1588)

<a id="op-289ab0d75de6e9"></a>
### Document.cast

`operation_foundation_binding_foundation_model_document_document_cast`

**Inputs** self, value, df.

**Explicit results** cast\_fieldtype(df.fieldtype, value, show\_warning = false).

**Local steps**

- Return cast\_fieldtype(df.fieldtype, value, show\_warning = false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1560)

<a id="op-7cccadd102f7c5"></a>
### Document.extract images from text editor

`operation_foundation_binding_foundation_model_document_document_extract_images_from_text_editor`

**Inputs** self.

**Local steps**

- Bind dependencies extract\_images\_from\_doc.
- If self.doctype differs from “DocType”.
  - For each df in self.meta.get(“fields”, mapping(“fieldtype” → tuple(“=”, “Text Editor”))).
    - Evaluate extract\_images\_from\_doc(self, df.fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L138) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1594) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1570)

<a id="op-5c42124d0ccbfb"></a>
### Filter

`operation_foundation_binding_foundation_model_document_filter`

**Inputs** data, filters, limit = no value.

**Explicit results** out.

**Local steps**

- Set tuple(out, \_filters) from tuple(list(), mapping()).
- If not data.
  - Return out.
- If filters.
  - For each f in filters.
    - Set fval from filters at f.
    - If not isinstance(fval, (tuple bitwise or list)).
      - If fval is identical to true.
        - Set fval from tuple(“not None”, fval).
      - Otherwise.
        - If fval is identical to false.
          - Set fval from tuple(“None”, fval).
        - Otherwise.
          - If (isinstance(fval, str) and fval.startswith(“^”)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fval, str) → fval.startswith(“^”).
            - Set fval from tuple(“^”, fval at slice 1 to no value).
          - Otherwise.
            - Set fval from tuple(“=”, fval).
    - Set \_filters at f from fval.
- For each d in data.
  - For each tuple(f, fval) in \_filters.items().
    - If not compare(getattr(d, f, no value), fval at 0, fval at 1).
      - Leave the innermost loop without its normal-exhaustion alternative.
  - After normal loop exhaustion.
    - Evaluate out.append(d).
    - If (limit and len(out) ≥ limit).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(out) ≥ limit.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return out.

**Values supplied outside this operation** selected callable from getattr(d, f, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L199) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1631)

<a id="op-37d5b367939e54"></a>
### Identity

`operation_foundation_binding_foundation_model_document_identity`

**Inputs** doc, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** get\_doc.register(Document).

**Declared result** Document.

**Explicit results** doc.

**Local steps**

- Return doc.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L202) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1634)

<a id="op-ebf8861b2d684d"></a>
### Execute action

`operation_foundation_model_document_business_behavior_execute_action`

**Inputs** \_\_doctype, \_\_name, \_\_action, remaining named values kwargs.

**Record and data access** resolve a document from \_\_doctype via get\_doc.

**State and service calls** rollback.

**Local steps**

- Set doc from Platform.get\_doc(\_\_doctype, \_\_name).
- Evaluate doc.unlock().
- Attempt the following.
  - Evaluate getattr(doc, \_\_action)(expanded names kwargs).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - If Platform.message\_log.
    - Set msg from Platform.message\_log at negative 1.get(“message”).
  - Otherwise.
    - Set msg from ((text in the contract + Platform.get\_traceback()) + “&lt;/pre&gt;&lt;/code&gt;”).
  - Evaluate doc.add\_comment(“Comment”, ((translated “Action Failed” + text in the contract) + msg)).
- Evaluate doc.notify\_update().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, \_\_action).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L3411) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1053)

<a id="op-8ffea897d3003d"></a>
### Bulk insert

`operation_foundation_model_document_business_behavior_bulk_insert`

**Inputs** doctype, documents, ignore\_duplicates = false, chunk\_size = 1000, commit\_chunks = false.

**State and service calls** request bulk\_insert on dt · commit.

**Local steps**

- Set doctype\_meta from Platform.get\_meta(doctype).
- Set valid\_column\_map from mapping(doctype → doctype\_meta.get\_valid\_columns()).
- Set child\_table\_fields from doctype\_meta.get\_table\_fields().
- For each child\_table in child\_table\_fields.
  - Set valid\_column\_map at child\_table.options from Platform.get\_meta(child\_table.options).get\_valid\_columns().
- Set documents from iter(documents).
- While document\_batch bound to list(itertools.islice(documents, chunk\_size)).
  - Set values\_map from mapping(doctype → \_document\_values\_generator(document\_batch, valid\_column\_map at doctype)).
  - For each child\_table in child\_table\_fields.
    - Set values\_map at child\_table.options from \_document\_values\_generator(list of ch\_doc for ch\_doc drawn from generator of child\_docs for doc drawn from document\_batch, then child\_docs drawn from doc.get(child\_table.fieldname), valid\_column\_map at chi ….
      - Draw ch\_doc from generator of child\_docs for doc drawn from document\_batch, then child\_docs drawn from doc.get(child\_table.fieldname).
      - Draw doc from document\_batch.
      - Draw child\_docs from doc.get(child\_table.fieldname).
  - For each tuple(dt, docs) in values\_map.items().
    - Evaluate Platform.db.bulk\_insert(dt, valid\_column\_map at dt, docs, ignore\_duplicates = ignore\_duplicates).
  - If commit\_chunks.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L3778) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L938)

<a id="op-f7b6dd010e02ed"></a>
### Document values generator

`operation_foundation_model_document_business_behavior_document_values_generator`

**Inputs** documents, columns.

**Declared result** Generator at tuple at Any.

**Local steps**

- For each doc in documents.
  - Set doc.creation, doc.modified from now().
  - Set doc.owner, doc.modified\_by from Platform.session.user.
  - Set doc\_values from doc.get\_valid\_dict(convert\_dates\_to\_str = true, ignore\_nulls = true, ignore\_virtual = true).
  - yield tuple(generator of doc\_values.get(col) for col drawn from columns).
    - Draw col from columns.

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L4414) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1052)
