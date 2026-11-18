# Record lifecycle and persistence · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Doctype

<a id="op-87be035194dc75"></a>
### Doc Type.add child table fields

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_add_child_table_fields`

**Inputs** self.

**Local steps**

- Bind dependencies add\_column.
- Evaluate add\_column(self.name, “parent”, “Data”).
- Evaluate add\_column(self.name, “parenttype”, “Data”).
- Evaluate add\_column(self.name, “parentfield”, “Data”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L5309) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1955) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L143)

<a id="op-3c2ecb092f74eb"></a>
### Doc Type.get max idx

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_get_maximum_position`

**Inputs** self.

**Record and data access** execute query text (SELECT, Doc Field).

**Explicit results** ((max\_idx and max\_idx at 0 at 0) or 0).

**Local steps**

- Set max\_idx from Platform.db.sql(query text (SELECT, Doc Field), self.name).
- Return ((max\_idx and max\_idx at 0 at 0) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (max\_idx and max\_idx at 0 at 0) → 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_idx → max\_idx at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L5462) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1972) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L159)

<a id="op-c7b7ed98a2240f"></a>
### Doc Type.validate name

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_validate_name`

**Inputs** self, name = no value.

**Explicit failure paths** validation helper with Platform.NameError — translated “Doctype name is limited to {0} characters ({1})”.format(max\_length, name) · validation helper with Platform.NameError — translated “DocType's name should not start or end with whitespace” · validation helper with Platform.NameError — translated “A DocType's name should start with a letter and can only consist of letters, numbers, spaces, underscores an …”.

**Local steps**

- If not name.
  - Set name from self.name.
- Set max\_length from (Platform.db.MAX\_COLUMN\_LENGTH − 3).
- If len(name) &gt; max\_length.
  - Call the validation error handler Platform.throw(translated “Doctype name is limited to {0} characters ({1})”.format(max\_length, name), Platform.NameError).
- If WHITESPACE\_PADDING\_PATTERN.search(name).
  - Call the validation error handler Platform.throw(translated “DocType's name should not start or end with whitespace”, Platform.NameError).
- If not START\_WITH\_LETTERS\_PATTERN.match(name).
  - Call the validation error handler Platform.throw(translated “A DocType's name should start with a letter and can only consist of letters, numbers, spaces, underscores an …”, Platform.NameError, title = “Invalid Name”).
- Evaluate validate\_route\_conflict(self.doctype, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L5621) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2000) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L185)

<a id="op-7960780f3277a8"></a>
### Doc Type.check pending migration

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_record_type_check_pending_migration`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**State and service calls** msgprint with translated “This doctype has pending migrations, run 'bench migrate' before modifying the doctype to avoid losing changes.”.

**Explicit results** no value · true.

**Local steps**

- If (self.is\_new() or self.custom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.custom.
  - Return no value.
- Set file from Path(get\_file\_path(Platform.scrub(self.module), self.doctype, self.name)).
- Set content from json.loads(file.read\_text()).
- If (content.get(“modified”) and get\_datetime(self.modified) &lt; get\_datetime(content.get(“modified”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in content.get(“modified”) → get\_datetime(self.modified) &lt; get\_datetime(content.get(“modified”)).
  - Evaluate Platform.msgprint(translated “This doctype has pending migrations, run 'bench migrate' before modifying the doctype to avoid losing changes.”, alert = true, indicator = “yellow”).
  - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0064.json#L6018) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L154)

<a id="op-76a9d6743f415a"></a>
### Validate series

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_series`

**Inputs** dt, autoname = no value, name = no value.

**Explicit failure paths** validation helper — translated “Fieldname called {0} must exist to enable autonaming”.format(Platform.bold(fieldname)) · validation helper — translated “Invalid fieldname '{0}' in autoname”.format(field) · validation helper — translated “Series {0} already used in {1}”.format(prefix, used\_in at 0 at 0).

**Local steps**

- If not autoname.
  - Set autoname from dt.autoname.
- If not name.
  - Set name from dt.name.
- If (not autoname and dt.get(“fields”, mapping(“fieldname” → “naming\_series”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not autoname → dt.get(“fields”, mapping(“fieldname” → “naming\_series”)).
  - Set dt.autoname from “naming\_series:”.
- Otherwise.
  - If (dt.autoname and dt.autoname.startswith(“naming\_series:”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt.autoname → dt.autoname.startswith(“naming\_series:”).
    - Set fieldname from (dt.autoname.split(“naming\_series:”, 1) at 0 or “naming\_series”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in dt.autoname.split(“naming\_series:”, 1) at 0 → “naming\_series”.
    - If not dt.get(“fields”, mapping(“fieldname” → fieldname)).
      - Call the validation error handler Platform.throw(translated “Fieldname called {0} must exist to enable autonaming”.format(Platform.bold(fieldname)), title = translated “Field Missing”).
- If (autoname and autoname.startswith(“field:”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname → autoname.startswith(“field:”).
  - Set field from autoname.split(“:”) at 1.
  - If (not field or field does not belong to list of df.fieldname for df drawn from dt.fields).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not field → field does not belong to list of df.fieldname for df drawn from dt.fields.
    - Draw df from dt.fields.
    - Call the validation error handler Platform.throw(translated “Invalid fieldname '{0}' in autoname”.format(field)).
  - Otherwise.
    - For each df in dt.fields.
      - If df.fieldname equals field.
        - Set df.unique from 1.
        - Leave the innermost loop without its normal-exhaustion alternative.
- If (autoname and not autoname.startswith(“field:”) and not autoname.startswith(“eval:”) and autoname.lower() does not belong to tuple(“prompt”, “hash”) and not autoname.startswith(“naming\_series:”) and not au ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in autoname → not autoname.startswith(“field:”) → not autoname.startswith(“eval:”) → autoname.lower() does not belong to tuple(“prompt”, “hash”) → not autoname.startswith(“naming\_series:”) → not autoname.startswith(“format:”).
  - Set prefix from autoname.split(“.”, 1) at 0.
  - Set doctype from Platform.qb.DocType(“DocType”).
  - Set used\_in from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.like(nested operand in the contract(nested operand in the contract, nested operand in the contract))).whe ….run().
  - If used\_in.
    - Call the validation error handler Platform.throw(translated “Series {0} already used in {1}”.format(prefix, used\_in at 0 at 0)).
- Evaluate validate\_empty\_name(dt, autoname).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L33) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L241)

<a id="op-26f04fcca32e5f"></a>
### Validate empty name

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_empty_name`

**Inputs** dt, autoname.

**State and service calls** toast with translated “Warning: Naming is not set”.

**Explicit results** no value.

**Local steps**

- If dt.doctype equals “Customize Form”.
  - Return no value.
- If (not autoname and not (dt.issingle or dt.istable)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not autoname → not (dt.issingle or dt.istable).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dt.issingle → dt.istable.
  - Attempt the following.
    - Set controller from get\_controller(dt.name).
  - On failure (ImportError).
    - Set controller from no value.
  - If (not controller or not hasattr(controller, “autoname”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not controller → not hasattr(controller, “autoname”).
    - Evaluate Platform.toast(translated “Warning: Naming is not set”, indicator = “yellow”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from get\_controller(dt.name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L1195) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2008) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L193)

<a id="op-165aabc3690633"></a>
### Validate autoincrement autoname

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_autoincrement_autoname`

**Inputs** dt.

**Declared result** bool.

**Record and data access** read dt.name via get\_all.

**Explicit results** false · true.

**Explicit failure paths** validation helper — translated “Cannot change to/from autoincrement autoname in Customize Form” · validation helper — translated “Can only change to/from Autoincrement naming rule when there is no data in the doctype”.

**Local steps**

- Bind local operation get\_autoname\_before\_save for subsequent calls.
- If not dt.is\_new().
  - Set autoname\_before\_save from get\_autoname\_before\_save(dt).
  - Set is\_autoname\_autoincrement from dt.autoname equals “autoincrement”.
  - If ((is\_autoname\_autoincrement and autoname\_before\_save differs from “autoincrement”) or (not is\_autoname\_autoincrement and autoname\_before\_save equals “autoincrement”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (is\_autoname\_autoincrement and autoname\_before\_save differs from “autoincrement”) → (not is\_autoname\_autoincrement and autoname\_before\_save equals “autoincrement”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_autoname\_autoincrement → autoname\_before\_save differs from “autoincrement”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_autoname\_autoincrement → autoname\_before\_save equals “autoincrement”.
    - If dt.doctype equals “Customize Form”.
      - Call the validation error handler Platform.throw(translated “Cannot change to/from autoincrement autoname in Customize Form”).
    - If Platform.get\_meta(dt.name).issingle.
      - Return false.
    - If not Platform.get\_all(dt.name, limit = 1).
      - Return true.
    - Call the validation error handler Platform.throw(translated “Can only change to/from Autoincrement naming rule when there is no data in the doctype”).
- Return false.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L1481) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2006) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L191)

<a id="op-b6c80a5635f49b"></a>
### Validate autoincrement autoname.get autoname before save

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_autoincrement_autoname_get_autoname_before_save`

**Inputs** dt.

**Declared result** str.

**Record and data access** read “Property Setter” via get\_value · read “DocType” via get\_value.

**Explicit results** (Platform.db.get\_value(“DocType”, dt.doc\_type, “autoname”) or empty text) · property\_value · getattr(dt.get\_doc\_before\_save(), “autoname”, empty text).

**Local steps**

- If dt.doctype equals “Customize Form”.
  - Set property\_value from Platform.db.get\_value(“Property Setter”, mapping(“doc\_type” → dt.doc\_type, “property” → “autoname”), “value”).
  - If not property\_value.
    - Return (Platform.db.get\_value(“DocType”, dt.doc\_type, “autoname”) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“DocType”, dt.doc\_type, “autoname”) → empty text.
  - Return property\_value.
- Return getattr(dt.get\_doc\_before\_save(), “autoname”, empty text).

**Values supplied outside this operation** selected callable from getattr(dt.get\_doc\_before\_save(), “autoname”, empty text).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L2175) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2007) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L192)

<a id="op-a14d551668762b"></a>
### Change name column type

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_change_name_column_type`

**Inputs** doctype\_name, type.

**Declared result** no value.

**Local steps**

- Set args from tuple(doctype\_name, “name”, type, false, …) when Platform.db.db\_type equals “postgres”, otherwise tuple(doctype\_name, “name”, type, true).
  - Value choice on Platform.db.db\_type equals “postgres” — true gives tuple(doctype\_name, “name”, type, false, …), false gives tuple(doctype\_name, “name”, type, true).
- Evaluate Platform.db.change\_column\_type(expanded args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L2472) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L134)

<a id="op-8615dba7a7c293"></a>
### Validate links table fieldnames

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_links_table_fieldnames`

**Inputs** meta.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ValidationError — message.

**Local steps**

- If (not meta.links or Platform.flags.in\_patch or Platform.flags.in\_fixtures or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta.links → Platform.flags.in\_patch → Platform.flags.in\_fixtures → Platform.flags.in\_migrate.
  - Return no value.
- Set fieldnames from tuple(generator of field.fieldname for field drawn from meta.fields).
  - Draw field from meta.fields.
- For each tuple(index, link) in enumerate(meta.links, 1).
  - Evaluate \_test\_connection\_query(doctype = link.link\_doctype, field = link.link\_fieldname, idx = index).
  - If not link.is\_child\_table.
    - Continue with the next iteration or loop test.
  - If not link.parent\_doctype.
    - Set message from translated “Document Links Row #{0}: Parent DocType is mandatory for internal links”.format(index).
    - Call the validation error handler Platform.throw(message, Platform.ValidationError, translated “Parent Missing”).
  - If not link.table\_fieldname.
    - Set message from translated “Document Links Row #{0}: Table Fieldname is mandatory for internal links”.format(index).
    - Call the validation error handler Platform.throw(message, Platform.ValidationError, translated “Table Fieldname Missing”).
  - If meta.name equals link.parent\_doctype.
    - Set field\_exists from link.table\_fieldname belongs to fieldnames.
  - Otherwise.
    - Set field\_exists from Platform.get\_meta(link.parent\_doctype).has\_field(link.table\_fieldname).
  - If not field\_exists.
    - Set message from translated “Document Links Row #{0}: Could not find field {1} in {2} DocType”.format(index, Platform.bold(link.table\_fieldname), Platform.bold(meta.name)).
    - Call the validation error handler Platform.throw(message, Platform.ValidationError, translated “Invalid Table Fieldname”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L2642) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L21) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L229)

<a id="op-c73190f0830bcc"></a>
### Test connection query

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_test_connection_query`

**Inputs** doctype, field, idx.

**Record and data access** read doctype via get\_all.

**Explicit failure paths** validation helper with InvalidFieldNameError — msg.

**Local steps**

- Set filters from (get\_filters\_for(doctype) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_filters\_for(doctype) → mapping().
- Set filters at field from empty text.
- Attempt the following.
  - Evaluate Platform.get\_all(doctype, filters = filters, limit = 1, distinct = true, ignore\_ifnull = true).
- On failure (Exception) bound to e.
  - Evaluate Platform.clear\_last\_message().
  - Set msg from translated “Document Links Row #{0}: Invalid doctype or fieldname.”.format(idx).
  - Update msg using + (text in the contract + str(e)).
  - Call the validation error handler Platform.throw(msg, InvalidFieldNameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L3402) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2005) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L190)

<a id="op-6f89d4ce6d2790"></a>
### Validate fields for doctype

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_for_record_type`

**Inputs** doctype.

**Local steps**

- Set meta from Platform.get\_meta(doctype, cached = false).
- Evaluate validate\_links\_table\_fieldnames(meta).
- Evaluate validate\_fields(meta).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0065.json#L3711) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L16) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L224)

<a id="op-a4d14422ef6dc8"></a>
### Validate fields

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields`

**Inputs** meta.

**Local steps**

- Bind local operation check\_illegal\_characters for subsequent calls.
- Bind local operation check\_invalid\_fieldnames for subsequent calls.
- Bind local operation check\_unique\_fieldname for subsequent calls.
- Bind local operation check\_fieldname\_length for subsequent calls.
- Bind local operation check\_illegal\_mandatory for subsequent calls.
- Bind local operation check\_link\_table\_options for subsequent calls.
- Bind local operation check\_hidden\_and\_mandatory for subsequent calls.
- Bind local operation check\_width for subsequent calls.
- Bind local operation check\_in\_list\_view for subsequent calls.
- Bind local operation check\_in\_global\_search for subsequent calls.
- Bind local operation check\_dynamic\_link\_options for subsequent calls.
- Bind local operation check\_illegal\_default for subsequent calls.
- Bind local operation check\_precision for subsequent calls.
- Bind local operation check\_unique\_and\_text for subsequent calls.
- Bind local operation check\_fold for subsequent calls.
- Bind local operation check\_search\_fields for subsequent calls.
- Bind local operation check\_title\_field for subsequent calls.
- Bind local operation check\_image\_field for subsequent calls.
- Bind local operation check\_is\_published\_field for subsequent calls.
- Bind local operation check\_website\_search\_field for subsequent calls.
- Bind local operation check\_timeline\_field for subsequent calls.
- Bind local operation check\_sort\_field for subsequent calls.
- Bind local operation check\_illegal\_depends\_on\_conditions for subsequent calls.
- Bind local operation check\_table\_multiselect\_option for subsequent calls.
- Bind local operation scrub\_options\_in\_select for subsequent calls.
- Bind local operation validate\_fetch\_from for subsequent calls.
- Bind local operation validate\_data\_field\_type for subsequent calls.
- Bind local operation check\_child\_table\_option for subsequent calls.
- Bind local operation check\_max\_height for subsequent calls.
- Bind local operation get\_islands\_on\_site for subsequent calls.
- Bind local operation check\_vue\_component\_options for subsequent calls.
- Bind local operation check\_no\_of\_ratings for subsequent calls.
- Bind local operation check\_decimal\_config for subsequent calls.
- Bind local operation validate\_link\_filters for subsequent calls.
- Set fields from meta.get(“fields”).
- Set fieldname\_list from list of d.fieldname for d drawn from fields.
  - Draw d from fields.
- Set in\_ci from os.environ.get(“CI”).
- Set not\_allowed\_in\_list\_view from get\_fields\_not\_allowed\_in\_list\_view(meta).
- For each d in fields.
  - If not d.permlevel.
    - Set d.permlevel from 0.
  - If d.fieldtype does not belong to table\_fields.
    - Set d.allow\_bulk\_edit from 0.
  - Evaluate check\_illegal\_characters(d.fieldname).
  - Evaluate check\_invalid\_fieldnames(meta.get(“name”), d.fieldname).
  - Evaluate check\_fieldname\_length(d.fieldname).
  - Evaluate check\_hidden\_and\_mandatory(meta.get(“name”), d).
  - Evaluate check\_unique\_and\_text(meta.get(“name”), d).
  - Evaluate check\_table\_multiselect\_option(d).
  - Evaluate scrub\_options\_in\_select(d).
  - Evaluate validate\_fetch\_from(d).
  - Evaluate validate\_data\_field\_type(d).
  - Evaluate check\_decimal\_config(d).
  - Evaluate validate\_link\_filters(d).
  - If (not Platform.flags.in\_migrate or in\_ci).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.flags.in\_migrate → in\_ci.
    - Evaluate check\_unique\_fieldname(meta.get(“name”), d.fieldname).
    - Evaluate check\_link\_table\_options(meta.get(“name”), d).
    - Evaluate check\_illegal\_mandatory(meta.get(“name”), d).
    - Evaluate check\_dynamic\_link\_options(d).
    - Evaluate check\_in\_list\_view(meta.get(“istable”), d).
    - Evaluate check\_in\_global\_search(d).
    - Evaluate check\_illegal\_depends\_on\_conditions(d).
    - Evaluate check\_illegal\_default(d).
    - Evaluate check\_child\_table\_option(d).
    - Evaluate check\_max\_height(d).
    - Evaluate check\_no\_of\_ratings(d).
    - Evaluate check\_vue\_component\_options(d).
- If (not Platform.flags.in\_migrate or in\_ci).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.flags.in\_migrate → in\_ci.
  - Evaluate check\_fold(fields).
  - Evaluate check\_search\_fields(meta, fields).
  - Evaluate check\_title\_field(meta).
  - Evaluate check\_timeline\_field(meta).
  - Evaluate check\_is\_published\_field(meta).
  - Evaluate check\_website\_search\_field(meta).
  - Evaluate check\_sort\_field(meta).
  - Evaluate check\_image\_field(meta).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L2) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2009) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L194)

<a id="op-63e4f0018f934f"></a>
### Validate fields.check illegal characters

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_illegal_characters`

**Inputs** fieldname.

**Local steps**

- Evaluate validate\_column\_name(fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2016) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L201)

<a id="op-e9734933700ebd"></a>
### Validate fields.check invalid fieldnames

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_invalid_fieldnames`

**Inputs** docname, fieldname.

**Explicit failure paths** validation helper — translated “{0}: fieldname cannot be set to reserved keyword {1}”.format(Platform.bold(docname), Platform.bold(fieldname)) · validation helper — translated “{0}: fieldname cannot be set to reserved field {1} in DocType”.format(Platform.bold(docname), Platform.bold(fieldname)).

**Local steps**

- Set RESERVED\_DOCFIELD\_NAMES from frozenset(tuple(“autoname”)).
- If fieldname belongs to RESERVED\_KEYWORDS.
  - Call the validation error handler Platform.throw(translated “{0}: fieldname cannot be set to reserved keyword {1}”.format(Platform.bold(docname), Platform.bold(fieldname)), title = translated “Invalid Fieldname”).
- If (fieldname belongs to RESERVED\_DOCFIELD\_NAMES and docname differs from “DocType”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname belongs to RESERVED\_DOCFIELD\_NAMES → docname differs from “DocType”.
  - Call the validation error handler Platform.throw(translated “{0}: fieldname cannot be set to reserved field {1} in DocType”.format(Platform.bold(docname), Platform.bold(fieldname)), title = translated “Invalid Fieldname”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L58) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2023) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L208)

<a id="op-8ecffb0d990bbe"></a>
### Validate fields.check unique fieldname

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_unique_fieldname`

**Inputs** docname, fieldname.

**Explicit failure paths** validation helper with UniqueFieldnameError — translated “{0}: Fieldname {1} appears multiple times in rows {2}”.format(docname, fieldname, “, ”.join(duplicates)).

**Local steps**

- Set duplicates from list(filter(no value, map(deferred anonymous expression, fields))).
- If len(duplicates) &gt; 1.
  - Call the validation error handler Platform.throw(translated “{0}: Fieldname {1} appears multiple times in rows {2}”.format(docname, fieldname, “, ”.join(duplicates)), UniqueFieldnameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L435) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L13) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L221)

<a id="op-e067cd94a123a3"></a>
### Validate fields.check fieldname length

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_fieldname_length`

**Inputs** fieldname.

**Local steps**

- Evaluate validate\_column\_length(fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L712) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2013) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L198)

<a id="op-969a2899afbe78"></a>
### Validate fields.check illegal mandatory

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_illegal_mandatory`

**Inputs** docname, d.

**Explicit failure paths** validation helper with IllegalMandatoryError — translated “{0}: Field {1} of type {2} cannot be mandatory”.format(docname, d.label, d.fieldtype).

**Local steps**

- If (d.fieldtype belongs to no\_value\_fields and d.fieldtype does not belong to table\_fields and d.reqd).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype belongs to no\_value\_fields → d.fieldtype does not belong to table\_fields → d.reqd.
  - Call the validation error handler Platform.throw(translated “{0}: Field {1} of type {2} cannot be mandatory”.format(docname, d.label, d.fieldtype), IllegalMandatoryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L764) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2019) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L204)

<a id="op-08f68ccef7b1af"></a>
### Validate fields.check link table options

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_link_table_options`

**Inputs** docname, d.

**Record and data access** read “DocType” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with DoctypeLinkError — translated “{0}: Options required for Link or Table type field {1} in row {2}”.format(docname, d.label, d.idx) · validation helper with WrongOptionsDoctypeLinkError — translated “{0}: Options must be a valid DocType for field {1} in row {2}”.format(docname, d.label, d.idx) · validation helper with DoctypeLinkError — translated “{0}: Options {1} must be the same as doctype name {2} for the field {3}”.format(docname, d.options, options, d.label).

**Local steps**

- If (Platform.flags.in\_patch or Platform.flags.in\_fixtures).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_patch → Platform.flags.in\_fixtures.
  - Return no value.
- If d.fieldtype belongs to tuple(“Link”, expanded table\_fields).
  - If not d.options.
    - Call the validation error handler Platform.throw(translated “{0}: Options required for Link or Table type field {1} in row {2}”.format(docname, d.label, d.idx), DoctypeLinkError).
  - If (d.options equals “&#91;Select&#93;” or d.options equals d.parent).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.options equals “&#91;Select&#93;” → d.options equals d.parent.
    - Return no value.
  - If d.options differs from d.parent.
    - Set options from Platform.db.get\_value(“DocType”, d.options, “name”).
    - If not options.
      - Call the validation error handler Platform.throw(translated “{0}: Options must be a valid DocType for field {1} in row {2}”.format(docname, d.label, d.idx), WrongOptionsDoctypeLinkError).
    - Otherwise.
      - If options differs from d.options.
        - Call the validation error handler Platform.throw(translated “{0}: Options {1} must be the same as doctype name {2} for the field {3}”.format(docname, d.options, options, d.label), DoctypeLinkError).
      - Otherwise.
        - Set d.options from options.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L940) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L2) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L210)

<a id="op-91102dc0d1fb48"></a>
### Validate fields.check hidden and mandatory

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_hidden_and_mandatory`

**Inputs** docname, d.

**Explicit failure paths** validation helper with HiddenAndMandatoryWithoutDefaultError — translated “{0}: Field {1} in row {2} cannot be hidden and mandatory without default”.format(docname, d.label, d.idx).

**Local steps**

- If (d.hidden and d.reqd and not d.default and not Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.hidden → d.reqd → not d.default → not Platform.flags.in\_migrate.
  - Call the validation error handler Platform.throw(translated “{0}: Field {1} in row {2} cannot be hidden and mandatory without default”.format(docname, d.label, d.idx), HiddenAndMandatoryWithoutDefaultError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L1514) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2015) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L200)

<a id="op-df88bf7d488545"></a>
### Validate fields.check width

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_width`

**Inputs** d.

**Explicit failure paths** validation helper — translated “Max width for type Currency is 100px in row {0}”.format(d.idx).

**Local steps**

- If (d.fieldtype equals “Currency” and cint(d.width) &lt; 100).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype equals “Currency” → cint(d.width) &lt; 100.
  - Call the validation error handler Platform.throw(translated “Max width for type Currency is 100px in row {0}”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L1688) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L15) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L223)

<a id="op-77696a50a03d1e"></a>
### Validate fields.check in list view

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_in_list_view`

**Inputs** is\_table, d.

**Explicit failure paths** validation helper — translated “'{0}' not allowed for type {1} in row {2}”.format(property\_label, d.fieldtype, d.idx).

**Local steps**

- If (d.in\_list\_view and d.fieldtype belongs to not\_allowed\_in\_list\_view).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.in\_list\_view → d.fieldtype belongs to not\_allowed\_in\_list\_view.
  - Set property\_label from “In Grid View” when is\_table, otherwise “In List View”.
    - Value choice on is\_table — true gives “In Grid View”, false gives “In List View”.
  - Call the validation error handler Platform.throw(translated “'{0}' not allowed for type {1} in row {2}”.format(property\_label, d.fieldtype, d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L1852) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2022) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L207)

<a id="op-591806a03cb9a1"></a>
### Validate fields.check in global search

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_in_global_search`

**Inputs** d.

**Explicit failure paths** validation helper — translated “'In Global Search' not allowed for type {0} in row {1}”.format(d.fieldtype, d.idx).

**Local steps**

- If (d.in\_global\_search and d.fieldtype belongs to no\_value\_fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.in\_global\_search → d.fieldtype belongs to no\_value\_fields.
  - Call the validation error handler Platform.throw(translated “'In Global Search' not allowed for type {0} in row {1}”.format(d.fieldtype, d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L2028) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2021) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L206)

<a id="op-434a6d0705b51e"></a>
### Validate fields.check dynamic link options

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_dynamic_link_options`

**Inputs** d.

**Explicit failure paths** validation helper — translated “Options 'Dynamic Link' type of field must point to another Link Field with options as 'DocType'”.

**Local steps**

- If d.fieldtype equals “Dynamic Link”.
  - Set doctype\_pointer from list(filter(deferred anonymous expression, fields)).
  - If (not doctype\_pointer or doctype\_pointer at 0.fieldtype does not belong to tuple(“Link”, “Select”) or (doctype\_pointer at 0.fieldtype equals “Link” and doctype\_pointer at 0.options differs from “DocType”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype\_pointer → doctype\_pointer at 0.fieldtype does not belong to tuple(“Link”, “Select”) → (doctype\_pointer at 0.fieldtype equals “Link” and doctype\_pointer at 0.options differs from “DocType”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype\_pointer at 0.fieldtype equals “Link” → doctype\_pointer at 0.options differs from “DocType”.
    - Call the validation error handler Platform.throw(translated “Options 'Dynamic Link' type of field must point to another Link Field with options as 'DocType'”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L2169) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2012) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L197)
