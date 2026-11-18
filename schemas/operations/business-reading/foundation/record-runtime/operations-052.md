# Record lifecycle and persistence · operations 52

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Exporter

<a id="op-4e5538e202d0a1"></a>
### Type Exporter.initialize

`operation_foundation_types_exporter_business_behavior_type_exporter_initialize`

**Inputs** self, doc.

**Local steps**

- Bind dependencies get\_controller.
- Set self.doc from doc.
- Set self.doctype from doc.name.
- Set self.field\_types from mapping().
- Set self.imports from set(“from Platform.types import DF”).
- Set self.indent from whitespace '\\t'.
- Set self.controller\_path from (((Path(Platform.get\_module\_path(doc.module)) ÷ “doctype”) ÷ scrub(self.doctype)) ÷ formatted text {scrub(self.doctype)}.py).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L61) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1425)

<a id="op-d818f466f9cc11"></a>
### Type Exporter.export types

`operation_foundation_types_exporter_business_behavior_type_exporter_export_types`

**Inputs** self.

**Local steps**

- Evaluate self.\_guess\_indentation().
- Set new\_code from self.\_generate\_code().
- Evaluate self.\_replace\_or\_add\_code(new\_code).

If control reaches the end, it returns no value.

**Methods declared on this owner** [guess indentation](operations-052.md#op-a307142fcb0e0d), [generate code](operations-052.md#op-1d018350ed17ca), [replace or add code](operations-052.md#op-fe45b1feebbb23).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L4269) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1420)

<a id="op-fe45b1feebbb23"></a>
### Type Exporter.replace or add code

`operation_foundation_types_exporter_business_behavior_type_exporter_replace_or_add_code`

**Inputs** self, new\_code.

**Local steps**

- Set despaced\_name from self.doctype.replace(one space, empty text).
- Set class\_definition from formatted text class {despaced\_name}(.
- Set code from self.controller\_path.read\_text().
- Set tuple(first\_line, expanded \_, last\_line) from new\_code.splitlines().
- If (first\_line belongs to code and last\_line belongs to code).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in first\_line belongs to code → last\_line belongs to code.
  - Set existing\_block\_start from code.find(first\_line).
  - Set existing\_block\_end from (code.find(last\_line) + len(last\_line)).
  - Set code from (((code at slice no value to existing\_block\_start + new\_code) + whitespace '\\n\\n') + code at slice existing\_block\_end to no value.lstrip(whitespace '\\n')).
- Otherwise.
  - If class\_definition belongs to code.
    - If class\_def bound to re.search(formatted text class {despaced\_name}\\(.\*, code).
      - Set class\_definition\_end from (class\_def.span() at 1 + 1).
      - Set code from (((code at slice no value to class\_definition\_end + new\_code) + whitespace '\\n\\n') + code at slice class\_definition\_end to no value.lstrip(whitespace '\\n')).
- If self.\_validate\_code(code).
  - Evaluate self.controller\_path.write\_text(code).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate code](operations-052.md#op-92e60f40b949d6).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L4371) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1428)

<a id="op-1d018350ed17ca"></a>
### Type Exporter.generate code

`operation_foundation_types_exporter_business_behavior_type_exporter_generate_code`

**Inputs** self.

**Explicit results** textwrap.indent(type\_code\_block\_template.format(start\_block = start\_block, end\_block = end\_block, fields = textwrap.indent(fields\_code\_block, self.indent), imports = textwrap.indent(imports, self.indent)), ….

**Local steps**

- For each field in self.doc.fields.
  - If iskeyword(field.fieldname).
    - Continue with the next iteration or loop test.
  - If (field.is\_virtual and not field.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.is\_virtual → not field.options.
    - Continue with the next iteration or loop test.
  - If python\_type bound to self.\_map\_fieldtype(field).
    - Set self.field\_types at field.fieldname from python\_type.
- If self.doc.istable.
  - For each parent\_field in tuple(“parent”, “parentfield”, “parenttype”).
    - Set self.field\_types at parent\_field from “DF.Data”.
- If self.doc.autoname equals “autoincrement”.
  - Set self.field\_types at “name” from “DF.Int \| None”.
- Set fields\_code\_block from self.\_create\_fields\_code\_block().
- Set imports from self.\_create\_imports\_block().
- Return textwrap.indent(type\_code\_block\_template.format(start\_block = start\_block, end\_block = end\_block, fields = textwrap.indent(fields\_code\_block, self.indent), imports = textwrap.indent(imports, self.indent)), ….

**Methods declared on this owner** [map fieldtype](operations-052.md#op-2c5ef97374a875), [create fields code block](operations-052.md#op-6671e682d4999f), [create imports block](operations-052.md#op-36eded6366c347).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L5017) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1421)

<a id="op-6671e682d4999f"></a>
### Type Exporter.create fields code block

`operation_foundation_types_exporter_business_behavior_type_exporter_create_fields_code_block`

**Inputs** self.

**Explicit results** whitespace '\\n'.join(sorted(list of field\_template.format(field = field, type = typehint) for tuple(field, typehint) drawn from self.field\_types.items())).

**Local steps**

- Return whitespace '\\n'.join(sorted(list of field\_template.format(field = field, type = typehint) for tuple(field, typehint) drawn from self.field\_types.items())).
  - Draw tuple(field, typehint) from self.field\_types.items().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L5520) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1418)

<a id="op-36eded6366c347"></a>
### Type Exporter.create imports block

`operation_foundation_types_exporter_business_behavior_type_exporter_create_imports_block`

**Inputs** self.

**Declared result** str.

**Explicit results** whitespace '\\n'.join(sorted(self.imports)).

**Local steps**

- Return whitespace '\\n'.join(sorted(self.imports)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L5658) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1419)

<a id="op-63a7c4b85e5e31"></a>
### Type Exporter.get doctype imports

`operation_foundation_types_exporter_business_behavior_type_exporter_get_record_type_imports`

**Inputs** self, doctype.

**Explicit results** tuple(formatted text from {filepath} import {class\_name}, class\_name).

**Local steps**

- Bind dependencies get\_controller.
- Set doctype\_module from get\_controller(doctype).
- Set filepath from doctype\_module.\_\_module\_\_.
- Set class\_name from doctype\_module.\_\_name\_\_.
- Return tuple(formatted text from {filepath} import {class\_name}, class\_name).

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L60) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1423)

<a id="op-2c5ef97374a875"></a>
### Type Exporter.map fieldtype

`operation_foundation_types_exporter_business_behavior_type_exporter_map_fieldtype`

**Inputs** self, field.

**Declared result** (str bitwise or no value).

**Explicit results** no value · field\_definition.

**Local steps**

- If (field.fieldtype belongs to NO\_VALUE\_FIELDS and field.fieldtype does not belong to table\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype belongs to NO\_VALUE\_FIELDS → field.fieldtype does not belong to table\_fields.
  - Return no value.
- Set fieldtype from field.fieldtype.replace(one space, empty text).
- Set field\_definition from empty text.
- If fieldtype equals “Select”.
  - Update field\_definition using + “DF.Literal”.
- Otherwise.
  - If getattr(DF, fieldtype, no value).
    - Update field\_definition using + formatted text DF.{fieldtype}.
  - Otherwise.
    - Return no value.
- If parameter\_definition bound to self.\_generic\_parameters(field).
  - Update field\_definition using + parameter\_definition.
- If self.\_is\_nullable(field).
  - Update field\_definition using + “ \| None”.
- Return field\_definition.

**Methods declared on this owner** [generic parameters](operations-052.md#op-9274387526ddfa), [is nullable](operations-052.md#op-32b325a42a4b21).

**Values supplied outside this operation** selected callable from getattr(DF, fieldtype, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L5884) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1427)

<a id="op-32b325a42a4b21"></a>
### Type Exporter.is nullable

`operation_foundation_types_exporter_business_behavior_type_exporter_is_nullable`

**Inputs** self, field.

**Declared result** bool.

**Explicit results** false · not bool(field.reqd).

**Local steps**

- If field.fieldtype belongs to non\_nullable\_types.
  - Return false.
- If field.not\_nullable.
  - Return false.
- Return not bool(field.reqd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L6234) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1426)

<a id="op-9274387526ddfa"></a>
### Type Exporter.generic parameters

`operation_foundation_types_exporter_business_behavior_type_exporter_generic_parameters`

**Inputs** self, field.

**Declared result** (str bitwise or no value).

**Explicit results** no value · formatted text &#91;{cls\_name}&#93; · “&#91;None&#93;” · json.dumps(options).

**Local steps**

- If field.fieldtype belongs to tuple(“Table”, “Table MultiSelect”).
  - Set doctype from field.options.
  - If not doctype.
    - Return no value.
  - Set tuple(import\_statment, cls\_name) from self.\_get\_doctype\_imports(doctype).
  - Evaluate self.imports.add(import\_statment).
  - Return formatted text &#91;{cls\_name}&#93;.
- Otherwise.
  - If field.fieldtype equals “Select”.
    - If not field.options.
      - Return “&#91;None&#93;”.
    - Set options from list of o.strip() for o drawn from field.options.split(whitespace '\\n').
      - Draw o from field.options.split(whitespace '\\n').
    - Return json.dumps(options).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get doctype imports](operations-052.md#op-63a7c4b85e5e31).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L6357) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1422)

<a id="op-92e60f40b949d6"></a>
### Type Exporter.validate code

`operation_foundation_types_exporter_business_behavior_type_exporter_validate_code`

**Inputs** code.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**State and service calls** msgprint with Platform.\_(“Failed to export python type hints”).

**Explicit results** true · false.

**Local steps**

- Attempt the following.
  - Evaluate ast.parse(code).
  - Return true.
- On failure (Exception).
  - Evaluate Platform.msgprint(Platform.\_(“Failed to export python type hints”), alert = true).
  - Return false.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L6709) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L801) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1429)

<a id="op-a307142fcb0e0d"></a>
### Type Exporter.guess indentation

`operation_foundation_types_exporter_business_behavior_type_exporter_guess_indentation`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind dependencies INDENT.
- Within self.controller\_path.open() bound as f.
  - For each token in tokenize.generate\_tokens(f.readline).
    - If token.type equals INDENT.
      - If whitespace '\\t' belongs to token.string.
        - Set self.indent from whitespace '\\t'.
      - Otherwise.
        - Set self.indent from (one space × 4).
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L6859) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1424)

## Record · File

[Record definition](../../../../data/record-types/file.json)

<a id="op-5d025c1c0518ac"></a>
### File.initialize

`operation_foundation_core_record_definitions_file_business_behavior_file_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.content from (self.get(“content”) or byte value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“content”) → byte value.
- Set self.decode from self.get(“decode”, false).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L6000) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1487)

<a id="op-6114cfc18b7d7e"></a>
### File.is remote file

`operation_foundation_core_record_definitions_file_business_behavior_file_is_remote_file`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.file\_url.startswith(URL\_PREFIXES) · not self.content.

**Local steps**

- If self.file\_url.
  - Return self.file\_url.startswith(URL\_PREFIXES).
- Return not self.content.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L6167) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1489)

<a id="op-1c304421cc9e63"></a>
### File.autoname

`operation_foundation_core_record_definitions_file_business_behavior_file_autoname`

**Inputs** self.

**Local steps**

- If self.is\_folder.
  - If self.folder.
    - Set self.name from self.get\_name\_based\_on\_parent\_folder().
  - Otherwise.
    - Set self.name from self.file\_name.
- Otherwise.
  - Set self.name from Platform.generate\_hash(length = 10).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get name based on parent folder](operations-053.md#op-a26450eeb084d8).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 10).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L6259) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1468)

<a id="op-cf70af325b4d50"></a>
### File.before insert

`operation_foundation_core_record_definitions_file_business_behavior_file_before_insert`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A folder cannot have a File URL” · validation helper with Platform.MandatoryError — translated “File URL is required when copying an existing attachment.”.

**Local steps**

- If (self.attached\_to\_doctype and not self.attached\_to\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attached\_to\_doctype → not self.attached\_to\_name.
  - Set self.attached\_to\_doctype from no value.
  - Set self.attached\_to\_field from no value.
- Set self.file\_url from unquote(self.file\_url) when self.file\_url, otherwise empty text.
  - Value choice on self.file\_url — true gives unquote(self.file\_url), false gives empty text.
- Evaluate self.normalize\_file\_url().
- Evaluate self.set\_folder\_name().
- Evaluate self.set\_is\_private().
- Evaluate self.set\_file\_name().
- Evaluate self.validate\_attachment\_limit().
- Evaluate self.set\_file\_type().
- Evaluate self.validate\_file\_extension().
- Evaluate self.validate\_private\_file\_access().
- If self.is\_folder.
  - If self.file\_url.
    - Call the validation error handler Platform.throw(translated “A folder cannot have a File URL”).
  - Return no value.
- If self.flags.copy\_from\_existing\_file.
  - If not self.file\_url.
    - Call the validation error handler Platform.throw(translated “File URL is required when copying an existing attachment.”, exc = Platform.MandatoryError).
  - Return no value.
- If self.is\_remote\_file.
  - Set self.content\_hash from no value.
  - Evaluate self.validate\_remote\_file().
- Otherwise.
  - Evaluate self.save\_file(content = self.get\_content()).
  - Set self.flags.new\_file from true.
  - Evaluate Platform.db.after\_rollback.add(self.on\_rollback).
- If not self.is\_remote\_file.
  - Evaluate self.validate\_duplicate\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [normalize file url](operations-052.md#op-30cfd9e828e941), [set folder name](operations-053.md#op-4f2f82967f68d2), [set is private](operations-054.md#op-d55f992556c228), [set file name](operations-053.md#op-e31b8488b64ec5), [validate attachment limit](operations-053.md#op-1b2e813f3abdb9), [set file type](operations-053.md#op-45da8006d41a61), [validate file extension](operations-053.md#op-7c5b82fe959e68), [validate private file access](operations-052.md#op-45163337891c6c), [validate remote file](operations-053.md#op-2880bcf229037f), [save file](operations-054.md#op-beb53f54919003), [get content](operations-054.md#op-cbacd25d2bb6ea), [validate duplicate entry](operations-053.md#op-eeef550a333a43).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L58) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1469)

<a id="op-cf2c3ee987a1fe"></a>
### File.after insert

`operation_foundation_core_record_definitions_file_business_behavior_file_after_insert`

**Inputs** self.

**Local steps**

- If not self.is\_folder.
  - Evaluate self.create\_attachment\_record().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create attachment record](operations-054.md#op-daae29cab9f22b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L7024) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1466)

<a id="op-96457fe58f4c80"></a>
### File.create attachment copy

`operation_foundation_core_record_definitions_file_business_behavior_file_create_attachment_copy`

**Inputs** self, attached\_to\_doctype, attached\_to\_name, attached\_to\_field = no value, ignore\_permissions = false.

**State and service calls** request copy\_doc for self · call insert on attachment.

**Explicit results** attachment.insert(ignore\_permissions = ignore\_permissions).

**Explicit failure paths** validation helper — translated “Cannot attach a folder to a document”.

**Local steps**

- If self.is\_folder.
  - Call the validation error handler Platform.throw(translated “Cannot attach a folder to a document”).
- Set attachment from Platform.copy\_doc(self).
- Evaluate attachment.update(mapping(“attached\_to\_doctype” → attached\_to\_doctype, “attached\_to\_name” → attached\_to\_name, “attached\_to\_field” → attached\_to\_field)).
- Set attachment.folder from no value.
- Set attachment.flags.copy\_from\_existing\_file from true.
- Return attachment.insert(ignore\_permissions = ignore\_permissions).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0076.json#L7093) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1472)

<a id="op-8a5f2457ddc727"></a>
### File.validate

`operation_foundation_core_record_definitions_file_business_behavior_file_validate`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A folder cannot have a File URL”.

**Local steps**

- If self.is\_folder.
  - If self.file\_url.
    - Call the validation error handler Platform.throw(translated “A folder cannot have a File URL”).
  - Return no value.
- If self.is\_remote\_file.
  - Set self.content\_hash from no value.
- Evaluate self.validate\_attachment\_references().
- Evaluate self.enforce\_public\_file\_restrictions().
- If (not self.is\_new() and self.has\_value\_changed(“file\_url”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“file\_url”).
  - Evaluate self.validate\_private\_file\_access().
- If (not self.is\_new() and self.has\_value\_changed(“is\_private”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“is\_private”).
  - Evaluate self.handle\_is\_private\_changed().
- Evaluate self.validate\_file\_path().
- Evaluate self.validate\_file\_url().
- Evaluate self.validate\_file\_on\_disk().
- Set self.file\_size from (Platform.form\_dict.file\_size or self.file\_size).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.file\_size → self.file\_size.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate attachment references](operations-052.md#op-64560828a47b82), [enforce public file restrictions](operations-052.md#op-626eb1a62973bc), [validate private file access](operations-052.md#op-45163337891c6c), [handle is private changed](operations-053.md#op-434563a840c4b7), [validate file path](operations-053.md#op-68a371b94ad155), [validate file url](operations-053.md#op-0b5b8fb833b838), [validate file on disk](operations-053.md#op-87ec305de2fd44).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L66) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1503)

<a id="op-64560828a47b82"></a>
### File.validate attachment references

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_attachment_references`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Attached To Name must be a string or an integer” · validation helper — translated “The fieldname you've specified in Attached To Field is invalid”.

**Local steps**

- If not self.attached\_to\_doctype.
  - Return no value.
- If (not self.attached\_to\_name or not isinstance(self.attached\_to\_name, (str bitwise or int))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.attached\_to\_name → not isinstance(self.attached\_to\_name, (str bitwise or int)).
  - Call the validation error handler Platform.throw(translated “Attached To Name must be a string or an integer”, Platform.ValidationError).
- If (self.attached\_to\_field and SPECIAL\_CHAR\_PATTERN.search(self.attached\_to\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attached\_to\_field → SPECIAL\_CHAR\_PATTERN.search(self.attached\_to\_field).
  - Call the validation error handler Platform.throw(translated “The fieldname you've specified in Attached To Field is invalid”).
- If (self.flags.ignore\_permissions or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.ignore\_permissions → Platform.flags.in\_install.
  - Return no value.
- Bind dependencies check\_write\_permission.
- Evaluate check\_write\_permission(self.attached\_to\_doctype, self.attached\_to\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L67) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1505)

<a id="op-626eb1a62973bc"></a>
### File.enforce public file restrictions

`operation_foundation_core_record_definitions_file_business_behavior_file_enforce_public_file_restrictions`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only System Managers can make this file public.”.

**Local steps**

- If (not self.is\_private and Platform.get\_system\_settings(“only\_allow\_system\_managers\_to\_upload\_public\_files”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_private → Platform.get\_system\_settings(“only\_allow\_system\_managers\_to\_upload\_public\_files”).
  - Attempt the following.
    - Evaluate Platform.only\_for(“System Manager”).
  - On failure (PermissionError).
    - Call the validation error handler Platform.throw(translated “Only System Managers can make this file public.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“only\_allow\_system\_managers\_to\_upload\_public\_files”) · effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L570) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1477)

<a id="op-30cfd9e828e941"></a>
### File.normalize file url

`operation_foundation_binding_foundation_core_doctype_file_file_file_normalize_file_url`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The File URL you've entered is incorrect”.

**Local steps**

- If (not self.file\_url or self.is\_remote\_file).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.file\_url → self.is\_remote\_file.
  - Return no value.
- If “..” belongs to self.file\_url.split(“/”).
  - Call the validation error handler Platform.throw(translated “The File URL you've entered is incorrect”, title = translated “Invalid File URL”).
- For each prefix in tuple(“/private/files/”, “/files/”).
  - If not self.file\_url.startswith(prefix).
    - Continue with the next iteration or loop test.
  - Set name from posixpath.normpath((“/” + nested operand in the contract at nested operand in the contract.lstrip(“/”))).lstrip(“/”).
  - If (not name or name equals “.”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → name equals “.”.
    - Call the validation error handler Platform.throw(translated “The File URL you've entered is incorrect”, title = translated “Invalid File URL”).
  - Set self.file\_url from (prefix + name).
  - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L628)

<a id="op-45163337891c6c"></a>
### File.validate private file access

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_private_file_access`

**Inputs** self.

**Record and data access** read “File” via get\_all · resolve a document from “File” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You do not have permission to access this file”.

**Local steps**

- If not self.file\_url.
  - Return no value.
- Set filters from mapping(“file\_url” → self.file\_url, “is\_private” → 1).
- If not self.is\_new().
  - Set filters at “name” from list(“!=”, self.name).
- Set private\_files from Platform.get\_all(“File”, filters = filters, fields = list(“name”, “owner”)).
- If not private\_files.
  - Return no value.
- Set user from Platform.session.user.
- If user equals “Administrator”.
  - Return no value.
- For each private\_file in private\_files.
  - If user equals private\_file.owner.
    - Return no value.
  - If has\_permission(Platform.get\_doc(“File”, private\_file.name), “read”, user = user).
    - Return no value.
- Call the validation error handler Platform.throw(translated “You do not have permission to access this file”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from has\_permission(Platform.get\_doc(“File”, private\_file.name), “read”, user = user).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L69) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1512)

<a id="op-6eab8f13d689db"></a>
### File.after rename

`operation_foundation_core_record_definitions_file_business_behavior_file_after_rename`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- For each successor in self.get\_successors().
  - Evaluate setup\_folder\_path(successor, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get successors](operations-053.md#op-aa75d59eba4507).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L1172) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1467)
