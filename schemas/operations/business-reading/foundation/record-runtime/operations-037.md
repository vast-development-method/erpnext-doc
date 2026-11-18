# Record lifecycle and persistence · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Doctype

<a id="op-532931d11cc19d"></a>
### Validate fields.check illegal default

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_illegal_default`

**Inputs** d.

**Explicit failure paths** validation helper — translated “The default value for the Check field {0} must be either '0' or '1'”.format(Platform.bold((d.label or d.fieldname))) · validation helper — translated “Options for {0} must be set before setting the default value.”.format(Platform.bold(d.fieldname)) · validation helper — translated “Default value for {0} must be in the list of options.”.format(Platform.bold(d.fieldname)).

**Local steps**

- If (d.fieldtype equals “Check” and not d.default).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype equals “Check” → not d.default.
  - Set d.default from “0”.
- If d.fieldtype equals “Check”.
  - Set default\_value from cstr(d.default).strip().
  - If default\_value does not belong to tuple(“0”, “1”).
    - Call the validation error handler Platform.throw(translated “The default value for the Check field {0} must be either '0' or '1'”.format(Platform.bold((d.label or d.fieldname)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.label → d.fieldname.
  - Set d.default from default\_value.
- If (d.fieldtype equals “Select” and d.default).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype equals “Select” → d.default.
  - If not d.options.
    - Call the validation error handler Platform.throw(translated “Options for {0} must be set before setting the default value.”.format(Platform.bold(d.fieldname))).
  - Otherwise.
    - If d.default does not belong to d.options.split(whitespace '\\n').
      - Call the validation error handler Platform.throw(translated “Default value for {0} must be in the list of options.”.format(Platform.bold(d.fieldname))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L2465) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2017) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L202)

<a id="op-ac743ac850bc8e"></a>
### Validate fields.check precision

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_precision`

**Inputs** d.

**Explicit failure paths** validation helper — translated “Precision should be between 1 and 6”.

**Local steps**

- If (d.fieldtype belongs to tuple(“Currency”, “Float”, “Percent”) and d.precision is distinct from no value and not 1 ≤ cint(d.precision) ≤ 6).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.fieldtype belongs to tuple(“Currency”, “Float”, “Percent”) → d.precision is distinct from no value → not 1 ≤ cint(d.precision) ≤ 6.
  - Compare adjacent operands in order, stopping at the first false comparison in 1 ≤ cint(d.precision) ≤ 6.
  - Call the validation error handler Platform.throw(translated “Precision should be between 1 and 6”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L3016) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L5) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L213)

<a id="op-866965f0f8a12d"></a>
### Validate fields.check unique and text

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_unique_and_text`

**Inputs** docname, d.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Explicit failure paths** validation helper with NonUniqueError — translated “{0}: Fieldtype {1} for {2} cannot be unique”.format(docname, d.fieldtype, d.label) · validation helper with NonUniqueError — translated “{0}: Field '{1}' cannot be set as Unique as it has non-unique values”.format(docname, d.label) · validation helper with CannotIndexedError — translated “{0}:Fieldtype {1} for {2} cannot be indexed”.format(docname, d.fieldtype, d.label).

**Local steps**

- If meta.is\_virtual.
  - Return no value.
- If meta.issingle.
  - Set d.unique from 0.
  - Set d.search\_index from 0.
- If getattr(d, “unique”, false).
  - If d.fieldtype does not belong to tuple(“Data”, “Link”, “Read Only”, “Int”).
    - Call the validation error handler Platform.throw(translated “{0}: Fieldtype {1} for {2} cannot be unique”.format(docname, d.fieldtype, d.label), NonUniqueError).
  - If (not d.get(“\_\_islocal”) and Platform.db.has\_column(d.parent, d.fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.get(“\_\_islocal”) → Platform.db.has\_column(d.parent, d.fieldname).
    - Set has\_non\_unique\_values from Platform.db.sql(formatted text select ′{d.fieldname}′, count(\*)  from ′tab{d.parent}′ where ifnull(′{d.fieldname}′, '') != ''  group by ′{d.fieldname}′ having count(\*) &gt; 1 l).
    - If (has\_non\_unique\_values and has\_non\_unique\_values at 0 at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_non\_unique\_values → has\_non\_unique\_values at 0 at 0.
      - Call the validation error handler Platform.throw(translated “{0}: Field '{1}' cannot be set as Unique as it has non-unique values”.format(docname, d.label), NonUniqueError).
- If (d.search\_index and d.fieldtype belongs to tuple(“Text”, “Long Text”, “Small Text”, “Code”, …)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.search\_index → d.fieldtype belongs to tuple(“Text”, “Long Text”, “Small Text”, “Code”, …).
  - Call the validation error handler Platform.throw(translated “{0}:Fieldtype {1} for {2} cannot be indexed”.format(docname, d.fieldtype, d.label), CannotIndexedError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(d, “unique”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L3200) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L12) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L220)

<a id="op-0c945ba8462547"></a>
### Validate fields.check fold

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_fold`

**Inputs** fields.

**Explicit failure paths** validation helper — translated “There can be only one Fold in a form” · validation helper — translated “Fold must come before a Section Break” · validation helper — translated “Fold can not be at the end of the form”.

**Local steps**

- Set fold\_exists from false.
- For each tuple(i, f) in enumerate(fields).
  - If f.fieldtype equals “Fold”.
    - If fold\_exists.
      - Call the validation error handler Platform.throw(translated “There can be only one Fold in a form”).
    - Set fold\_exists from true.
    - If i &lt; (len(fields) − 1).
      - Set nxt from fields at (i + 1).
      - If nxt.fieldtype differs from “Section Break”.
        - Call the validation error handler Platform.throw(translated “Fold must come before a Section Break”).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Fold can not be at the end of the form”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L3881) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2014) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L199)

<a id="op-54d9727104cd32"></a>
### Validate fields.check search fields

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_search_fields`

**Inputs** meta, fields.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Search field {0} is not valid”.format(fieldname).

**Local steps**

- If not meta.search\_fields.
  - Return no value.
- Set search\_fields from list of field.strip() for field drawn from (meta.search\_fields or empty text).split(“,”).
  - Draw field from (meta.search\_fields or empty text).split(“,”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.search\_fields → empty text.
- Set fieldtype\_mapper from mapping of field.fieldname → field.fieldtype for field drawn from filter(deferred anonymous expression, fields).
  - Draw field from filter(deferred anonymous expression, fields).
- For each fieldname in search\_fields.
  - Set fieldname from fieldname.strip().
  - If (fieldtype\_mapper.get(fieldname) belongs to no\_value\_fields or fieldname does not belong to fieldname\_list).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldtype\_mapper.get(fieldname) belongs to no\_value\_fields → fieldname does not belong to fieldname\_list.
    - Call the validation error handler Platform.throw(translated “Search field {0} is not valid”.format(fieldname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L4221) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L6) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L214)

<a id="op-c31e8899c8a9a9"></a>
### Validate fields.check title field

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_title_field`

**Inputs** meta.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidFieldNameError — translated “Title field must be a valid fieldname”.

**Local steps**

- If not meta.get(“title\_field”).
  - Return no value.
- If meta.title\_field does not belong to fieldname\_list.
  - Call the validation error handler Platform.throw(translated “Title field must be a valid fieldname”, InvalidFieldNameError).
- Bind local operation \_validate\_title\_field\_pattern for subsequent calls.
- Set df from meta.get(“fields”, filters = mapping(“fieldname” → meta.title\_field)) at 0.
- If df.
  - Evaluate \_validate\_title\_field\_pattern(df.options).
  - Evaluate \_validate\_title\_field\_pattern(df.default).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L4597) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L10) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L218)

<a id="op-e11c3c64bbc67e"></a>
### Validate fields.check title field.validate title field pattern

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_title_field_validate_title_field_pattern`

**Inputs** pattern.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidFieldNameError — translated “{{{0}}} is not a valid fieldname pattern. It should be {{field\_name}}.”.format(fieldname).

**Local steps**

- If not pattern.
  - Return no value.
- For each fieldname in FIELD\_PATTERN.findall(pattern).
  - If fieldname.startswith(“{”).
    - Continue with the next iteration or loop test.
  - If fieldname does not belong to fieldname\_list.
    - Call the validation error handler Platform.throw(translated “{{{0}}} is not a valid fieldname pattern. It should be {{field\_name}}.”.format(fieldname), InvalidFieldNameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L5045) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L11) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L219)

<a id="op-68c9327106d615"></a>
### Validate fields.check image field

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_image_field`

**Inputs** meta.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidFieldNameError — translated “Image field must be a valid fieldname” · validation helper with InvalidFieldNameError — translated “Image field must be of type Attach Image”.

**Local steps**

- If not meta.image\_field.
  - Return no value.
- Set df from meta.get(“fields”, mapping(“fieldname” → meta.image\_field)).
- If not df.
  - Call the validation error handler Platform.throw(translated “Image field must be a valid fieldname”, InvalidFieldNameError).
- If df at 0.fieldtype differs from “Attach Image”.
  - Call the validation error handler Platform.throw(translated “Image field must be of type Attach Image”, InvalidFieldNameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L5238) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2020) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L205)

<a id="op-cba3c392ad87d0"></a>
### Validate fields.check is published field

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_is_published_field`

**Inputs** meta.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidFieldNameError — translated “Is Published Field must be a valid fieldname”.

**Local steps**

- If not meta.is\_published\_field.
  - Return no value.
- If meta.is\_published\_field does not belong to fieldname\_list.
  - Call the validation error handler Platform.throw(translated “Is Published Field must be a valid fieldname”, InvalidFieldNameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L5484) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2024) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L209)

<a id="op-32b679d8036128"></a>
### Validate fields.check website search field

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_website_search_field`

**Inputs** meta.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidFieldNameError — translated “Website Search Field must be a valid fieldname” · validation helper — translated “Field "title" is mandatory if "Website Search Field" is set.”.

**Local steps**

- If not meta.get(“website\_search\_field”).
  - Return no value.
- If meta.website\_search\_field does not belong to fieldname\_list.
  - Call the validation error handler Platform.throw(translated “Website Search Field must be a valid fieldname”, InvalidFieldNameError).
- If “title” does not belong to fieldname\_list.
  - Call the validation error handler Platform.throw(translated “Field "title" is mandatory if "Website Search Field" is set.”, title = translated “Missing Field”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L5608) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L14) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L222)

<a id="op-a6e482eb2e5ba3"></a>
### Validate fields.check timeline field

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_timeline_field`

**Inputs** meta.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidFieldNameError — translated “Timeline field must be a valid fieldname” · validation helper with InvalidFieldNameError — translated “Timeline field must be a Link or Dynamic Link”.

**Local steps**

- If not meta.timeline\_field.
  - Return no value.
- If meta.timeline\_field does not belong to fieldname\_list.
  - Call the validation error handler Platform.throw(translated “Timeline field must be a valid fieldname”, InvalidFieldNameError).
- Set df from meta.get(“fields”, mapping(“fieldname” → meta.timeline\_field)) at 0.
- If df.fieldtype does not belong to tuple(“Link”, “Dynamic Link”).
  - Call the validation error handler Platform.throw(translated “Timeline field must be a Link or Dynamic Link”, InvalidFieldNameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L5838) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L9) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L217)

<a id="op-37e7b23359bba4"></a>
### Validate fields.check sort field

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_sort_field`

**Inputs** meta.

**Explicit failure paths** validation helper with InvalidFieldNameError — translated “Sort field {0} must be a valid fieldname”.format(fieldname).

**Local steps**

- If meta.sort\_field.
  - Set sort\_fields from list(meta.sort\_field).
  - If “,” belongs to meta.sort\_field.
    - Set sort\_fields from list of d.split(maxsplit = 1) at 0 for d drawn from meta.sort\_field.split(“,”).
      - Draw d from meta.sort\_field.split(“,”).
  - For each fieldname in sort\_fields.
    - If fieldname does not belong to ((fieldname\_list + list(default\_fields)) + list(child\_table\_fields)).
      - Call the validation error handler Platform.throw(translated “Sort field {0} must be a valid fieldname”.format(fieldname), InvalidFieldNameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L6110) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L7) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L215)

<a id="op-8be12ec62360f1"></a>
### Validate fields.check illegal depends on conditions

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_illegal_depends_on_conditions`

**Inputs** docfield.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Invalid {0} condition”.format(Platform.unscrub(field)).

**Local steps**

- Set depends\_on\_fields from list(“depends\_on”, “collapsible\_depends\_on”, “mandatory\_depends\_on”, “read\_only\_depends\_on”).
- For each field in depends\_on\_fields.
  - Set depends\_on from docfield.get(field, no value).
  - If (depends\_on and “=” belongs to depends\_on and DEPENDS\_ON\_PATTERN.match(depends\_on)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in depends\_on → “=” belongs to depends\_on → DEPENDS\_ON\_PATTERN.match(depends\_on).
    - Call the validation error handler Platform.throw(translated “Invalid {0} condition”.format(Platform.unscrub(field)), Platform.ValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L6418) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2018) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L203)

<a id="op-9e48a63407d75b"></a>
### Validate fields.check table multiselect option

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_table_multiselect_option`

**Inputs** docfield.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “DocType &lt;b&gt;{0}&lt;/b&gt; provided for the field &lt;b&gt;{1}&lt;/b&gt; must have atleast one Link field”.format(doctype, docfield.fieldname).

**Local steps**

- If docfield.fieldtype differs from “Table MultiSelect”.
  - Return no value.
- Set doctype from docfield.options.
- Set meta from Platform.get\_meta(doctype).
- Set link\_field from list of df for df drawn from meta.fields where df.fieldtype equals “Link”.
  - Draw df from meta.fields, keep a combination only if (df.fieldtype equals “Link”).
- If not link\_field.
  - Call the validation error handler Platform.throw(translated “DocType &lt;b&gt;{0}&lt;/b&gt; provided for the field &lt;b&gt;{1}&lt;/b&gt; must have atleast one Link field”.format(doctype, docfield.fieldname), Platform.ValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0067.json#L6680) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L8) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L216)

<a id="op-01fb29a5215f51"></a>
### Validate fields.scrub options in select

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_scrub_options_in_select`

**Inputs** field.

**Local steps**

- If (field.fieldtype equals “Select” and field.options is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Select” → field.options is distinct from no value.
  - Set options\_list from list().
  - For each tuple(i, option) in enumerate(field.options.split(whitespace '\\n')).
    - Set \_option from option.strip().
    - If (i equals 0 or \_option).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in i equals 0 → \_option.
      - Evaluate options\_list.append(\_option).
  - Set field.options from whitespace '\\n'.join(options\_list).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L17) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L225)

<a id="op-4bf8267cfc058a"></a>
### Validate fields.validate fetch from

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_validate_fetch_from`

**Inputs** field.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not field.get(“fetch\_from”).
  - Return no value.
- Set field.fetch\_from from field.fetch\_from.strip().
- If “.” does not belong to field.fetch\_from.
  - Return no value.
- Set tuple(source\_field, \_target\_field) from field.fetch\_from.split(“.”, maxsplit = 1).
- If source\_field equals field.fieldname.
  - Set msg from translated “{0} contains an invalid Fetch From expression, Fetch From can't be self-referential.”.format(\_(field.label, context = field.parent)).
  - Call the validation error handler Platform.throw(msg, title = translated “Recursive Fetch From”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L3) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L19) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L227)

<a id="op-46247e33618f29"></a>
### Validate fields.validate data field type

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_validate_data_field_type`

**Inputs** docfield.

**State and service calls** msgprint with (text\_str + df\_options\_str).

**Explicit results** no value.

**Local steps**

- If docfield.get(“is\_virtual”).
  - Return no value.
- If (docfield.fieldtype equals “Data” and not (docfield.oldfieldtype and docfield.oldfieldtype differs from “Data”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.fieldtype equals “Data” → not (docfield.oldfieldtype and docfield.oldfieldtype differs from “Data”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.oldfieldtype → docfield.oldfieldtype differs from “Data”.
  - If (docfield.options and docfield.options does not belong to data\_field\_options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.options → docfield.options does not belong to data\_field\_options.
    - Set df\_str from Platform.bold(\_(docfield.label, context = docfield.parent)).
    - Set text\_str from (((translated “{0} is an invalid Data field.”.format(df\_str) + (text in the contract × 2)) + translated “Only Options allowed for Data field are:”) + text in the contract).
    - Set df\_options\_str from ((text in the contract + “&lt;/li&gt;&lt;li&gt;”.join(generator of translated x for x drawn from data\_field\_options)) + “&lt;/ul&gt;”).
      - Draw x from data\_field\_options.
    - Evaluate Platform.msgprint((text\_str + df\_options\_str), title = “Invalid Data Field”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L623) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L18) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L226)

<a id="op-88e6012402be1b"></a>
### Validate fields.check child table option

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_child_table_option`

**Inputs** docfield.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Option {0} for field {1} is not a child table”.format(Platform.bold(doctype), Platform.bold(docfield.fieldname)) · validation helper — translated “Child Table {0} for field {1} must be virtual”.format(Platform.bold(doctype), Platform.bold(docfield.fieldname)) · validation helper — translated “Field {0} must be a virtual field to support virtual doctype.”.format(Platform.bold(docfield.fieldname)).

**Local steps**

- If Platform.flags.in\_fixtures.
  - Return no value.
- If docfield.fieldtype does not belong to list(“Table MultiSelect”, “Table”).
  - Return no value.
- Set doctype from docfield.options.
- Set child\_doctype\_meta from Platform.get\_meta(doctype).
- If not child\_doctype\_meta.istable.
  - Call the validation error handler Platform.throw(translated “Option {0} for field {1} is not a child table”.format(Platform.bold(doctype), Platform.bold(docfield.fieldname)), title = translated “Invalid Option”).
- If (meta.is\_virtual and not child\_doctype\_meta.is\_virtual).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.is\_virtual → not child\_doctype\_meta.is\_virtual.
  - Call the validation error handler Platform.throw(translated “Child Table {0} for field {1} must be virtual”.format(Platform.bold(doctype), Platform.bold(docfield.fieldname)), title = translated “Invalid Option”).
- If (not meta.is\_virtual and child\_doctype\_meta.is\_virtual and not docfield.is\_virtual).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.is\_virtual → child\_doctype\_meta.is\_virtual → not docfield.is\_virtual.
  - Call the validation error handler Platform.throw(translated “Field {0} must be a virtual field to support virtual doctype.”.format(Platform.bold(docfield.fieldname)), title = translated “Virtual tables must be virtual fields”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L1085) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2010) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L195)

<a id="op-ca85154615b8c6"></a>
### Validate fields.check max height

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_maximum_height`

**Inputs** docfield.

**Explicit failure paths** validation helper — formatted text Max for {Platform.bold(docfield.fieldname)} height must be in px, em, rem.

**Local steps**

- If (getattr(docfield, “max\_height”, no value) and docfield.max\_height at slice negative 2 to no value does not belong to tuple(“px”, “em”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(docfield, “max\_height”, no value) → docfield.max\_height at slice negative 2 to no value does not belong to tuple(“px”, “em”).
  - Call the validation error handler Platform.throw(formatted text Max for {Platform.bold(docfield.fieldname)} height must be in px, em, rem).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(docfield, “max\_height”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L1659) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L3) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L211)

<a id="op-acc5e9af35df7b"></a>
### Validate fields.get islands on site

`operation_foundation_binding_foundation_core_doctype_doctype_doctype_validate_fields_get_islands_on_site`

**Inputs** no declared parameters.

**Wrappers, in declaration order** functools.cache.

**Explicit results** set(get\_ui\_islands()).

**Local steps**

- Bind dependencies get\_ui\_islands.
- Return set(get\_ui\_islands()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L627)

<a id="op-26645315b758eb"></a>
### Validate fields.check vue component options

`operation_foundation_binding_foundation_core_doctype_doctype_doctype_validate_fields_check_vue_component_options`

**Inputs** docfield.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Options required for Vue Component field {0}”.format(Platform.bold((docfield.label or docfield.fieldname))) · validation helper — translated “Island "{0}" is not on this site.”.format(docfield.options).

**Local steps**

- If (docfield.fieldtype differs from “Vue Component” or Platform.flags.in\_patch or Platform.flags.in\_fixtures or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in docfield.fieldtype differs from “Vue Component” → Platform.flags.in\_patch → Platform.flags.in\_fixtures → Platform.flags.in\_install.
  - Return no value.
- If not docfield.options.
  - Call the validation error handler Platform.throw(translated “Options required for Vue Component field {0}”.format(Platform.bold((docfield.label or docfield.fieldname))), title = translated “Missing Island”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in docfield.label → docfield.fieldname.
- If docfield.options does not belong to get\_islands\_on\_site().
  - Call the validation error handler Platform.throw(translated “Island "{0}" is not on this site.”.format(docfield.options), title = translated “Missing Island”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L626)

<a id="op-1a6f60b10952d8"></a>
### Validate fields.check no of ratings

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_number_of_ratings`

**Inputs** docfield.

**Explicit failure paths** validation helper — translated “Options for Rating field can range from 3 to 10”.

**Local steps**

- If docfield.fieldtype equals “Rating”.
  - If (docfield.options and (int(docfield.options) &gt; 10 or int(docfield.options) &lt; 3)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.options → (int(docfield.options) &gt; 10 or int(docfield.options) &lt; 3).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in int(docfield.options) &gt; 10 → int(docfield.options) &lt; 3.
    - Call the validation error handler Platform.throw(translated “Options for Rating field can range from 3 to 10”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L1847) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L4) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L212)

<a id="op-df6913fd3cc12d"></a>
### Validate fields.check decimal config

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_check_decimal_configuration`

**Inputs** docfield.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Precision ({0}) for {1} cannot be greater than its length ({2}).”.format(docfield.precision, Platform.bold(docfield.label), docfield.length).

**Local steps**

- If docfield.fieldtype does not belong to tuple(“Currency”, “Float”, “Percent”).
  - Return no value.
- If (docfield.length and docfield.precision).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.length → docfield.precision.
  - If cint(docfield.precision) &gt; cint(docfield.length).
    - Call the validation error handler Platform.throw(translated “Precision ({0}) for {1} cannot be greater than its length ({2}).”.format(docfield.precision, Platform.bold(docfield.label), docfield.length)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L2033) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L2011) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L196)

<a id="op-dceef1035690a6"></a>
### Validate fields.validate link filters

`operation_foundation_core_record_definitions_record_definitions_record_type_business_behavior_validate_fields_validate_link_filters`

**Inputs** docfield.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Invalid Filters for field {0}. Filters must be valid JSON.”.format(Platform.bold((docfield.label or docfield.fieldname))) · validation helper — translated “Invalid Filters for field {0}. Filters must be a list of filters, where each filter is a list with four valu …”.format(Platform.bold((docfield.label or docfield.fieldname))) · validation helper — translated “Attachment Gallery filters must target File.”.

**Local steps**

- Set link\_filters\_value from docfield.get(“link\_filters”).
- If not link\_filters\_value.
  - Return no value.
- Attempt the following.
  - Set link\_filters from json.loads(link\_filters\_value).
- On failure (tuple(TypeError, ValueError)).
  - Call the validation error handler Platform.throw(translated “Invalid Filters for field {0}. Filters must be valid JSON.”.format(Platform.bold((docfield.label or docfield.fieldname)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in docfield.label → docfield.fieldname.
- If (not isinstance(link\_filters, list) or any(generator of (not isinstance(filter\_row, list) or len(filter\_row) differs from 4) for filter\_row drawn from link\_filters)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(link\_filters, list) → any(generator of (not isinstance(filter\_row, list) or len(filter\_row) differs from 4) for filter\_row drawn from link\_filters).
  - Draw filter\_row from link\_filters.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(filter\_row, list) → len(filter\_row) differs from 4.
  - Call the validation error handler Platform.throw(translated “Invalid Filters for field {0}. Filters must be a list of filters, where each filter is a list with four valu …”.format(Platform.bold((docfield.label or docfield.fieldname)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in docfield.label → docfield.fieldname.
- If (docfield.fieldtype equals “Attachment Gallery” and any(generator of filter\_row at 0 differs from “File” for filter\_row drawn from link\_filters)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.fieldtype equals “Attachment Gallery” → any(generator of filter\_row at 0 differs from “File” for filter\_row drawn from link\_filters).
  - Draw filter\_row from link\_filters.
  - Call the validation error handler Platform.throw(translated “Attachment Gallery filters must target File.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0068.json#L2293) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L20) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L228)
