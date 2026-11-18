# Forms, reports and navigation · operations 49

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Printview

<a id="op-b9f2299898b238"></a>
### Get page rule margins

`operation_foundation_binding_foundation_www_printview_get_page_rule_margins`

**Inputs** css.

**Declared result** dict at tuple(str, str).

**Explicit results** margins.

**Local steps**

- Set margins from mapping().
- Set important from set().
- For each prop in get\_page\_rule\_properties(css).
  - If (prop.name equals “margin” and values bound to list of v.cssText for v drawn from prop.propertyValue).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in prop.name equals “margin” → values bound to list of v.cssText for v drawn from prop.propertyValue.
    - Draw v from prop.propertyValue.
    - Set top from values at 0.
    - Set right from values at 1 when len(values) &gt; 1, otherwise top.
      - Value choice on len(values) &gt; 1 — true gives values at 1, false gives top.
    - Set bottom from values at 2 when len(values) &gt; 2, otherwise top.
      - Value choice on len(values) &gt; 2 — true gives values at 2, false gives top.
    - Set left from values at 3 when len(values) &gt; 3, otherwise right.
      - Value choice on len(values) &gt; 3 — true gives values at 3, false gives right.
    - Set updates from zip(PAGE\_MARGIN\_SIDES, tuple(top, right, bottom, left), strict = true).
  - Otherwise.
    - If prop.name belongs to PAGE\_MARGIN\_SIDES.
      - Set updates from list(tuple(prop.name, prop.value)).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - For each tuple(side, value) in updates.
    - If not re.fullmatch(formatted text 0\|{PAGE\_LENGTH}, value.strip()).
      - Continue with the next iteration or loop test.
    - If (prop.priority or side does not belong to important).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in prop.priority → side does not belong to important.
      - Set margins at side from value.
      - If prop.priority.
        - Evaluate important.add(side).
- Return margins.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L81) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L386) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L474)

<a id="op-8c205c864e174f"></a>
### Get page rule size

`operation_foundation_binding_foundation_www_printview_get_page_rule_size`

**Inputs** css.

**Declared result** dict at tuple(str, str).

**Explicit results** size.

**Local steps**

- Set size from mapping().
- Set important from false.
- For each prop in get\_page\_rule\_properties(css).
  - If (prop.name differs from “size” or (important and not prop.priority)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in prop.name differs from “size” → (important and not prop.priority).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in important → not prop.priority.
    - Continue with the next iteration or loop test.
  - If value bound to parse\_page\_size(prop.value) is distinct from no value.
    - Set size from value.
    - Set important from (important or bool(prop.priority)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in important → bool(prop.priority).
- Return size.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L83) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L476)

<a id="op-73a8804074c15b"></a>
### Parse page size

`operation_foundation_binding_foundation_www_printview_parse_page_size`

**Inputs** value.

**Declared result** (dict at tuple(str, str) bitwise or no value).

**Explicit results** mapping() · mapping(“page-width” → parts at 0, “page-height” → parts at negative 1) · no value · (size or no value).

**Local steps**

- Bind dependencies PageSize.
- Set page\_sizes from mapping of name.lower() → dimensions for tuple(name, dimensions) drawn from PageSize.page\_sizes.items().
  - Draw tuple(name, dimensions) from PageSize.page\_sizes.items().
- Set parts from value.lower().split().
- If parts equals list(“auto”).
  - Return mapping().
- If (0 &lt; len(parts) ≤ 2 and all(generator of re.fullmatch(PAGE\_LENGTH, part) for part drawn from parts)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in 0 &lt; len(parts) ≤ 2 → all(generator of re.fullmatch(PAGE\_LENGTH, part) for part drawn from parts).
  - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; len(parts) ≤ 2.
  - Draw part from parts.
  - Return mapping(“page-width” → parts at 0, “page-height” → parts at negative 1).
- Set size from mapping().
- For each part in parts.
  - If (part belongs to tuple(“portrait”, “landscape”) and “orientation” does not belong to size).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in part belongs to tuple(“portrait”, “landscape”) → “orientation” does not belong to size.
    - Set size at “orientation” from part.
  - Otherwise.
    - If (part belongs to page\_sizes and “page-width” does not belong to size).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in part belongs to page\_sizes → “page-width” does not belong to size.
      - Set tuple(width, height) from sorted(page\_sizes at part).
      - Update size using bitwise or mapping(“page-width” → formatted text {width}mm, “page-height” → formatted text {height}mm).
    - Otherwise.
      - Return no value.
- Return (size or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in size → no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L88) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L481)

<a id="op-41e7a459c502d3"></a>
### Get font

`operation_foundation_public_pages_printview_business_behavior_get_font`

**Inputs** print\_settings, print\_format = no value, for\_legacy = false.

**Declared result** str.

**Explicit results** default · font.

**Local steps**

- Set default from multiline text in the contract.
- If for\_legacy.
  - Return default.
- Set font from no value.
- If print\_format.
  - If (print\_format.font and print\_format.font differs from “Default”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_format.font → print\_format.font differs from “Default”.
    - Set font from formatted text {print\_format.font}, sans-serif.
- If not font.
  - If (print\_settings.font and print\_settings.font differs from “Default”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in print\_settings.font → print\_settings.font differs from “Default”.
    - Set font from formatted text {print\_settings.font}, sans-serif.
  - Otherwise.
    - Set font from default.
- Return font.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L73) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L61)

<a id="op-5b453070bf0f88"></a>
### Get visible columns

`operation_foundation_public_pages_printview_business_behavior_get_visible_columns`

**Inputs** data, table\_meta, df.

**Declared result** list at “DocField”.

**State and service calls** request new\_doc for df.options.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- Set doc from (data at 0 or Platform.new\_doc(df.options)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data at 0 → Platform.new\_doc(df.options).
- Set hide\_in\_print\_layout from (df.get(“hide\_in\_print\_layout”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“hide\_in\_print\_layout”) → list().
- Bind local operation add\_column for subsequent calls.
- If df.get(“visible\_columns”).
  - For each col\_df in df.get(“visible\_columns”).
    - Set docfield from table\_meta.get\_field(col\_df.get(“fieldname”)).
    - If not docfield.
      - Continue with the next iteration or loop test.
    - Set newdf from docfield.as\_dict().copy().
    - Evaluate newdf.update(col\_df).
    - If add\_column(newdf).
      - Evaluate columns.append(newdf).
- Otherwise.
  - For each col\_df in table\_meta.fields.
    - If add\_column(col\_df).
      - Evaluate columns.append(col\_df).
- Return columns.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L5995) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1366) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L68)

<a id="op-8f59a279aec685"></a>
### Get visible columns.add column

`operation_foundation_public_pages_printview_business_behavior_get_visible_columns_add_column`

**Inputs** col\_df.

**Explicit results** false · (is\_visible(col\_df, doc) and column\_has\_value(data, col\_df.get(“fieldname”), col\_df)).

**Local steps**

- If col\_df.fieldname belongs to hide\_in\_print\_layout.
  - Return false.
- Return (is\_visible(col\_df, doc) and column\_has\_value(data, col\_df.get(“fieldname”), col\_df)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_visible(col\_df, doc) → column\_has\_value(data, col\_df.get(“fieldname”), col\_df).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L6613) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1367) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L69)

<a id="op-03b2555d3ab8b0"></a>
### Column has value

`operation_foundation_public_pages_printview_business_behavior_column_has_value`

**Inputs** data, fieldname, col\_df.

**Declared result** bool.

**Explicit results** true · has\_value.

**Local steps**

- Set has\_value from false.
- If (col\_df.fieldtype belongs to list(“Float”, “Currency”) and not col\_df.print\_hide\_if\_no\_value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col\_df.fieldtype belongs to list(“Float”, “Currency”) → not col\_df.print\_hide\_if\_no\_value.
  - Return true.
- For each row in data.
  - Set value from row.get(fieldname).
  - If value.
    - If isinstance(value, str).
      - If strip\_html(value).strip().
        - Set has\_value from true.
        - Leave the innermost loop without its normal-exhaustion alternative.
    - Otherwise.
      - Set has\_value from true.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return has\_value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L6764) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L56)

## Service · Profile

<a id="op-1315933b74ed61"></a>
### Get context

`operation_foundation_public_pages_profile_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Set context.show\_sidebar from true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L7065) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L84)

## Service · Prompts

<a id="op-ffcb1994c34582"></a>
### Get generation prompt

`operation_foundation_binding_foundation_studio_ai_prompts_get_generation_prompt`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** formatted text You are an expert UI Web developer &amp; designer specializing in creating responsive app pages for Platform Studio, a Vue.js-based low-code app builder..

**Local steps**

- Set runtime\_rules from read\_skill\_file(“RULES.md”).
- Set design\_language from read\_skill\_file(“DESIGN.md”).
- Return formatted text You are an expert UI Web developer &amp; designer specializing in creating responsive app pages for Platform Studio, a Vue.js-based low-code app builder..

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1845)

<a id="op-09c97e641e92fc"></a>
### Read skill file

`operation_foundation_binding_foundation_studio_ai_prompts_read_skill_file`

**Inputs** file\_name.

**Declared result** str.

**Explicit results** skill\_file.read().strip().

**Local steps**

- Set path from os.path.join(Platform.get\_app\_source\_path(“Platform”, “skills”), “studio-app-building”, file\_name).
- Within open(path, encoding = “utf-8”) bound as skill\_file.
  - Return skill\_file.read().strip().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L184) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1847)

<a id="op-10e3c6d280d3d5"></a>
### Get agent system

`operation_foundation_binding_foundation_studio_ai_prompts_get_agent_system`

**Inputs** data\_and\_code\_wiring.

**Declared result** str.

**Explicit results** formatted text You are an expert UI developer &amp; designer working inside Platform Studio, a Vue.js low-code app builder. You build and edit pages by CALLING TOOLS — n.

**Local steps**

- Set runtime\_rules from read\_skill\_file(“RULES.md”).
- Set design\_language from read\_skill\_file(“DESIGN.md”).
- Return formatted text You are an expert UI developer &amp; designer working inside Platform Studio, a Vue.js low-code app builder. You build and edit pages by CALLING TOOLS — n.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1844)

<a id="op-e090b60a235821"></a>
### Get system prompt for mode

`operation_foundation_binding_foundation_studio_ai_prompts_get_system_prompt_for_mode`

**Inputs** is\_standard.

**Declared result** str.

**Explicit results** get\_agent\_system(formatted text {DATA\_WIRING}  {page\_code}  {routing}).

**Local steps**

- Set page\_code from STANDARD\_PAGE\_CODE when is\_standard, otherwise CUSTOM\_PAGE\_CODE.
  - Value choice on is\_standard — true gives STANDARD\_PAGE\_CODE, false gives CUSTOM\_PAGE\_CODE.
- Set routing from read\_skill\_file(“ROUTING.md”).
- Return get\_agent\_system(formatted text {DATA\_WIRING}  {page\_code}  {routing}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L183) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1846)

## Record · Property setter

[Record definition](../../../../data/record-types/property_setter.json)

<a id="op-81c567c9baad2f"></a>
### Property Setter.autoname

`operation_foundation_custom_record_definitions_property_setter_business_behavior_property_setter_autoname`

**Inputs** self.

**Local steps**

- Set self.name from “{doctype}-{field}-{property}”.format(doctype = self.doc\_type, field = (self.field\_name or self.row\_name or “main”), property = self.property).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.field\_name → self.row\_name → “main”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L626) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1014)

<a id="op-02151ac4ec29bf"></a>
### Property Setter.validate

`operation_foundation_custom_record_definitions_property_setter_business_behavior_property_setter_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_fieldtype\_change().
- If self.is\_new().
  - Evaluate delete\_property\_setter(self.doc\_type, self.property, self.field\_name, self.row\_name).
- Evaluate Platform.clear\_cache(doctype = self.doc\_type).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate fieldtype change](operations-049.md#op-ad56e163f1e5d2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L745) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1018)

<a id="op-ad72f217e28f84"></a>
### Property Setter.on trash

`operation_foundation_custom_record_definitions_property_setter_business_behavior_property_setter_on_trash`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(doctype = self.doc\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L899) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1016)

<a id="op-ad56e163f1e5d2"></a>
### Property Setter.validate fieldtype change

`operation_foundation_custom_record_definitions_property_setter_business_behavior_property_setter_validate_fieldtype_change`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Field type cannot be changed for {0}”.format(self.field\_name).

**Local steps**

- If (self.property equals “fieldtype” and self.field\_name belongs to not\_allowed\_fieldtype\_change).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.property equals “fieldtype” → self.field\_name belongs to not\_allowed\_fieldtype\_change.
  - Call the validation error handler Platform.throw(translated “Field type cannot be changed for {0}”.format(self.field\_name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L962) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1019)

<a id="op-c75e0012698c1c"></a>
### Property Setter.on update

`operation_foundation_custom_record_definitions_property_setter_business_behavior_property_setter_on_update`

**Inputs** self.

**Local steps**

- If Platform.flags.in\_patch.
  - Set self.flags.validate\_fields\_for\_doctype from false.
- If (not self.flags.ignore\_validate and self.flags.validate\_fields\_for\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.ignore\_validate → self.flags.validate\_fields\_for\_doctype.
  - Bind dependencies validate\_fields\_for\_doctype.
  - Evaluate validate\_fields\_for\_doctype(self.doc\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L1110) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1017)

<a id="op-c5a54f0ed599fa"></a>
### Property Setter.get permission log options

`operation_foundation_custom_record_definitions_property_setter_business_behavior_property_setter_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L1253) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1015)

<a id="op-6c3d6ed9dbc123"></a>
### Make property setter

`operation_foundation_custom_record_definitions_property_setter_business_behavior_make_property_setter`

**Inputs** doctype, fieldname, property, value, property\_type, for\_doctype = false, validate\_fields\_for\_doctype = true, is\_system\_generated = true.

**Record and data access** resolve a document from mapping(“doctype” → “Property Setter”, “doctype\_or\_field” → ((for\_doctype and “DocType”) or “DocField”), “doc\_type” → doctype, “field\_name” → fieldname, …) via get\_doc.

**State and service calls** call insert on property\_setter.

**Explicit results** property\_setter.

**Local steps**

- Set property\_setter from Platform.get\_doc(mapping(“doctype” → “Property Setter”, “doctype\_or\_field” → ((for\_doctype and “DocType”) or “DocField”), “doc\_type” → doctype, “field\_name” → fieldname, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (for\_doctype and “DocType”) → “DocField”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_doctype → “DocType”.
- Set property\_setter.flags.ignore\_permissions from true.
- Set property\_setter.flags.validate\_fields\_for\_doctype from validate\_fields\_for\_doctype.
- Evaluate property\_setter.insert().
- Return property\_setter.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L1448) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1013)

<a id="op-dc858abd6ee0bd"></a>
### Delete property setter

`operation_foundation_custom_record_definitions_property_setter_business_behavior_delete_property_setter`

**Inputs** doc\_type, property = no value, field\_name = no value, row\_name = no value.

**Local steps**

- Set filters from mapping(“doc\_type” → doc\_type).
- If property.
  - Set filters at “property” from property.
- If field\_name.
  - Set filters at “field\_name” from field\_name.
- If row\_name.
  - Set filters at “row\_name” from row\_name.
- Evaluate \_delete\_property\_setters(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L1800) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1011)

<a id="op-c47aa6f6f406ee"></a>
### Bulk delete property setters

`operation_foundation_custom_record_definitions_property_setter_business_behavior_bulk_delete_property_setters`

**Inputs** property\_setters, bypass\_hooks = false.

**State and service calls** request delete on “Property Setter”.

**Explicit failure paths** validation helper — translated “′doctype′ and ′fieldname′ are required for deleting property setters.”.

**Local steps**

- Set field\_map from mapping(“doctype” → “doc\_type”, “fieldname” → “field\_name”).
- Set doctypes\_to\_clear from set().
- For each property\_setter in property\_setters.
  - Set filters from property\_setter.copy().
  - For each tuple(key, fieldname) in field\_map.items().
    - If key belongs to filters.
      - Set filters at fieldname from filters.pop(key).
  - If not filters.
    - Continue with the next iteration or loop test.
  - If (not filters.get(“doc\_type”) or not filters.get(“field\_name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.get(“doc\_type”) → not filters.get(“field\_name”).
    - Call the validation error handler Platform.throw(translated “′doctype′ and ′fieldname′ are required for deleting property setters.”).
  - If bypass\_hooks.
    - Evaluate Platform.db.delete(“Property Setter”, filters).
    - Evaluate doctypes\_to\_clear.add(filters at “doc\_type”).
  - Otherwise.
    - Evaluate \_delete\_property\_setters(filters).
- For each doctype in doctypes\_to\_clear.
  - Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L2017) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1010)

<a id="op-6e855814073ec4"></a>
### Delete property setters

`operation_foundation_custom_record_definitions_property_setter_business_behavior_delete_property_setters`

**Inputs** filters.

**Record and data access** read “Property Setter” via get\_all · resolve a document from “Property Setter” via get\_doc.

**Local steps**

- Set property\_setters from Platform.get\_all(“Property Setter”, filters = filters, pluck = “name”).
- For each ps in property\_setters.
  - Evaluate Platform.get\_doc(“Property Setter”, ps).delete(ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0127.json#L2559) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1012)

## Service · Qrcode

<a id="op-0805ca301ad36f"></a>
### Get context

`operation_foundation_public_pages_qrcode_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Set context.no\_cache from 1.
- Set tuple(context.qr\_code\_user, context.qrcode\_svg) from get\_user\_svg\_from\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L83) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L85)

<a id="op-c32c68704153a1"></a>
### Get query key

`operation_foundation_public_pages_qrcode_business_behavior_get_query_key`

**Inputs** no declared parameters.

**Explicit results** query.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set query\_string from Platform.local.request.query\_string.
- Set query from dict(parse\_qsl(query\_string)).
- Set query from mapping of key.decode() → val.decode() for tuple(key, val) drawn from query.items().
  - Draw tuple(key, val) from query.items().
- If “k” does not belong to list(query).
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Set query from query at “k”.strip().
- If false belongs to list of (i.isalpha() or i.isdigit()) for i drawn from query.
  - Draw i from query.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in i.isalpha() → i.isdigit().
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0547.json#L7207) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L86)
