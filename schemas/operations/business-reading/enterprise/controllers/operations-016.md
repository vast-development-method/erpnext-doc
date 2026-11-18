# Shared transaction rules · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Item variant

<a id="op-c671983b5561ad"></a>
### Copy field to variant

`operation_enterprise_binding_enterprise_controllers_item_variant_copy_field_to_variant`

**Inputs** item, variant, field.

**Explicit results** no value.

**Local steps**

- If variant.get(field.fieldname) equals item.get(field.fieldname).
  - Return no value.
- If field.fieldtype differs from “Table”.
  - Evaluate variant.set(field.fieldname, item.get(field.fieldname)).
  - Return no value.
- Evaluate variant.set(field.fieldname, list()).
- For each d in item.get(field.fieldname).
  - Set row from copy.deepcopy(d).
  - If row.get(“name”).
    - Set row.name from no value.
  - Evaluate variant.append(field.fieldname, row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1078) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L318)

<a id="op-9d9fd95b0aa199"></a>
### Set variant description

`operation_enterprise_binding_enterprise_controllers_item_variant_set_variant_description`

**Inputs** item, variant, allow\_fields.

**Local steps**

- If “description” does not belong to allow\_fields.
  - If not variant.description.
    - Set variant.description from empty text.
- Otherwise.
  - If item.variant\_based\_on equals “Item Attribute”.
    - If variant.attributes.
      - Set attributes\_description from (item.description or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.description → empty text.
      - For each d in variant.attributes.
        - Update attributes\_description using + ((((text in the contract + d.attribute) + “: ”) + cstr(d.attribute\_value)) + “&lt;/div&gt;”).
      - If attributes\_description does not belong to (variant.description or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in variant.description → empty text.
        - Set variant.description from attributes\_description.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1084) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L324)

<a id="op-28b84a847dac27"></a>
### Make variant item code

`operation_enterprise_controllers_item_variant_business_behavior_make_variant_item_code`

**Inputs** template\_item\_code, template\_item\_name, variant.

**Explicit results** no value.

**Local steps**

- If variant.item\_code.
  - Return no value.
- If abbreviations bound to get\_variant\_abbreviations(variant.attributes).
  - Set variant.item\_code from “{}-{}”.format(template\_item\_code, “-”.join(abbreviations)).
  - Set variant.item\_name from “{}-{}”.format(template\_item\_name, “-”.join(abbreviations)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L471)

<a id="op-81db784e706a18"></a>
### Get variant code

`operation_enterprise_binding_enterprise_controllers_item_variant_get_variant_code`

**Inputs** template\_item\_code, attributes, abbr\_overrides.

**Explicit results** “{}-{}”.format(template\_item\_code, “-”.join(abbreviations)) when abbreviations, otherwise no value.

**Local steps**

- Set abbreviations from get\_variant\_abbreviations(attributes, abbr\_overrides).
- Return “{}-{}”.format(template\_item\_code, “-”.join(abbreviations)) when abbreviations, otherwise no value.
  - Value choice on abbreviations — true gives “{}-{}”.format(template\_item\_code, “-”.join(abbreviations)), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1083) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L323)

<a id="op-dba51f668bf45e"></a>
### Get variant abbreviations

`operation_enterprise_binding_enterprise_controllers_item_variant_get_variant_abbreviations`

**Inputs** attributes, abbr\_overrides = no value.

**Explicit results** abbreviations.

**Local steps**

- Set abbreviations from list().
- For each attr in attributes.
  - If abbr bound to (abbr\_overrides or mapping()).get(tuple(attr.attribute, cstr(attr.attribute\_value))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in abbr\_overrides → mapping().
    - Evaluate abbreviations.append(abbr).
    - Continue with the next iteration or loop test.
  - Set item\_attribute from get\_attribute\_abbreviation(attr).
  - If not item\_attribute.
    - Continue with the next iteration or loop test.
  - Evaluate abbreviations.append(cstr(attr.attribute\_value) when item\_attribute at 0.numeric\_values, otherwise item\_attribute at 0.abbr).
    - Value choice on item\_attribute at 0.numeric\_values — true gives cstr(attr.attribute\_value), false gives item\_attribute at 0.abbr.
- Return abbreviations.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1082) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L322)

<a id="op-53e4f91767a8a1"></a>
### Get attribute abbreviation

`operation_enterprise_binding_enterprise_controllers_item_variant_get_attribute_abbreviation`

**Inputs** attr.

**Explicit results** nested operand in the contract(nested operand in the contract).select(ia.numeric\_values, iav.abbr).where((ia.name equals attr.attribute bitwise and (nested operand in the contract.attribute\_value equals ne ….

**Local steps**

- Set ia from Platform.qb.DocType(“Item Attribute”).
- Set iav from Platform.qb.DocType(“Item Attribute Value”).
- Return nested operand in the contract(nested operand in the contract).select(ia.numeric\_values, iav.abbr).where((ia.name equals attr.attribute bitwise and (nested operand in the contract.attribute\_value equals ne ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1079) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L319)

<a id="op-4e2564d758d179"></a>
### Create variant doc for quick entry

`operation_enterprise_controllers_item_variant_business_behavior_create_variant_record_for_quick_entry`

**Inputs** template, args.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_value.

**Explicit results** existing\_variant · variant.as\_dict().

**Local steps**

- Evaluate Platform.has\_permission(“Item”, doc = template, throw = true).
- Set variant\_based\_on from Platform.db.get\_value(“Item”, template, “variant\_based\_on”).
- Set args from json.loads(args).
- If variant\_based\_on equals “Manufacturer”.
  - Set variant from get\_variant(template, expanded names args).
- Otherwise.
  - Set existing\_variant from get\_variant(template, args).
  - If existing\_variant.
    - Return existing\_variant.
  - Otherwise.
    - Set variant from create\_variant(template, args = args).
    - Set variant.name from variant.item\_code.
    - Evaluate validate\_item\_variant\_attributes(variant, args).
- Return variant.as\_dict().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Item”, doc = template, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L462)

## Service · Mapper

<a id="op-69b4058038a3fc"></a>
### Get qty already mapped

`operation_enterprise_controllers_mapper_business_behavior_get_quantity_already_mapped`

**Inputs** target\_doc, ref\_field, qty\_field = “qty”.

**Declared result** Platform.\_dict.

**Explicit results** qty\_map.

**Local steps**

- If isinstance(target\_doc, str).
  - Set target\_doc from Platform.parse\_json(target\_doc).
- Set qty\_map from Platform.\_dict().
- For each row in ((target\_doc and target\_doc.get(“items”)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (target\_doc and target\_doc.get(“items”)) → list().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_doc → target\_doc.get(“items”).
  - If ref bound to row.get(ref\_field).
    - Set qty\_map at ref from (qty\_map.get(ref, 0) + flt(row.get(qty\_field))).
- Return qty\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0377.json#L1150) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L797) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L478)

## Service · Print settings

<a id="op-eab399e449425b"></a>
### Set print templates for item table

`operation_enterprise_controllers_print_settings_business_behavior_set_print_templates_for_item_table`

**Inputs** doc, settings.

**Local steps**

- Set doc.print\_templates from mapping(“items” → “templates/print\_formats/includes/items.html”).
- Set doc.child\_print\_templates from mapping(“items” → mapping(“qty” → “templates/print\_formats/includes/item\_table\_qty.html”, “serial\_and\_batch\_bundle” → “templates/print\_formats/includes/serial\_and\_batch\_bundle.html”), “packed\_items” → mapp ….
- Set doc.flags.compact\_item\_fields from list(“description”, “qty”, “rate”, “amount”).
- If settings.compact\_item\_print.
  - Set doc.child\_print\_templates at “items” at “description” from “templates/print\_formats/includes/item\_table\_description.html”.
  - Set doc.flags.format\_columns from format\_columns.

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0377.json#L1466) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L799) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L480)

<a id="op-0a8338ec601d4e"></a>
### Set print templates for taxes

`operation_enterprise_controllers_print_settings_business_behavior_set_print_templates_for_taxes`

**Inputs** doc, settings.

**Local steps**

- Set doc.flags.show\_inclusive\_tax\_in\_print from doc.is\_inclusive\_tax().
- Evaluate doc.print\_templates.update(mapping(“total” → “templates/print\_formats/includes/total.html”)).
- If not doc.should\_show\_taxes\_as\_table\_in\_print().
  - Evaluate doc.print\_templates.update(mapping(“taxes” → “templates/print\_formats/includes/taxes.html”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0377.json#L1804) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L800) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L481)

<a id="op-a3ffff5b2d26de"></a>
### Format columns

`operation_enterprise_controllers_print_settings_business_behavior_format_columns`

**Inputs** display\_columns, compact\_fields.

**Explicit results** final\_columns.

**Local steps**

- Set compact\_fields from list(expanded compact\_fields, “image”, “item\_code”, “item\_name”).
- Set final\_columns from list().
- For each column in display\_columns.
  - If column does not belong to compact\_fields.
    - Evaluate final\_columns.append(column).
- Return final\_columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0377.json#L1986) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L798) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L479)

## Service · Queries

<a id="op-78be19933118d0"></a>
### Employee query

`operation_enterprise_controllers_queries_business_behavior_employee_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters, reference\_doctype = no value, ignore\_user\_permissions = false.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** execute query text (SELECT, Employee).format(expanded names mapping(“fields” → “, ”.join(fields), “key” → searchfield, “fcond” → get\_filters\_cond(doctype, filters, conditions), “mcond” → mcond, …)).

**Explicit results** Platform.db.sql(query text (SELECT, Employee).format(expanded names mapping(“fields” → “, ”.join(fields), “key” → searchfield, “fcond” → get\_filters\_cond(doctype, filters, conditions), “mcond” → mcond, …)) ….

**Local steps**

- Set doctype from “Employee”.
- Set conditions from list().
- Set fields from get\_fields(doctype, list(“name”, “employee\_name”)).
- Set ignore\_permissions from false.
- If (reference\_doctype and ignore\_user\_permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doctype → ignore\_user\_permissions.
  - Set ignore\_permissions from (has\_ignored\_field(reference\_doctype, doctype) and has\_permission(doctype, ptype = “select” when Platform.only\_has\_select\_perm(doctype), otherwise “read”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_ignored\_field(reference\_doctype, doctype) → has\_permission(doctype, ptype = “select” when Platform.only\_has\_select\_perm(doctype), otherwise “read”).
    - Value choice on Platform.only\_has\_select\_perm(doctype) — true gives “select”, false gives “read”.
- Set search\_conditions from “ or ”.join(list of formatted text {field} like %(txt)s for field drawn from fields).
  - Draw field from fields.
- Set mcond from empty text when ignore\_permissions, otherwise get\_match\_cond(doctype).
  - Value choice on ignore\_permissions — true gives empty text, false gives get\_match\_cond(doctype).
- Return Platform.db.sql(query text (SELECT, Employee).format(expanded names mapping(“fields” → “, ”.join(fields), “key” → searchfield, “fcond” → get\_filters\_cond(doctype, filters, conditions), “mcond” → mcond, …)) ….

**Values supplied outside this operation** effective access from has\_permission(doctype, ptype = “select” when Platform.only\_has\_select\_perm(doctype), otherwise “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L802) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L483)

<a id="op-10df8bd96f6778"></a>
### Has ignored field

`operation_enterprise_controllers_queries_business_behavior_has_ignored_field`

**Inputs** reference\_doctype, doctype.

**Explicit results** true · false.

**Local steps**

- Set meta from Platform.get\_meta(reference\_doctype).
- For each field in meta.fields.
  - If not field.ignore\_user\_permissions.
    - Continue with the next iteration or loop test.
  - If (field.fieldtype equals “Link” and field.options equals doctype).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Link” → field.options equals doctype.
    - Return true.
  - Otherwise.
    - If field.fieldtype equals “Dynamic Link”.
      - Set options from meta.get\_link\_doctype(field.fieldname).
      - If not options.
        - Continue with the next iteration or loop test.
      - If isinstance(options, str).
        - Set options from options.split(whitespace '\\n').
      - If (doctype belongs to options or “DocType” belongs to options).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype belongs to options → “DocType” belongs to options.
        - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0377.json#L3372) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L826) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L507)

<a id="op-763dcad49fcae3"></a>
### Lead query

`operation_enterprise_controllers_queries_business_behavior_lead_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** execute query text (SELECT, Lead).format(expanded names mapping(“fields” → “, ”.join(fields), “key” → searchfield, “scond” → searchfields, “mcond” → get\_match\_cond(doctype))).

**Explicit results** Platform.db.sql(query text (SELECT, Lead).format(expanded names mapping(“fields” → “, ”.join(fields), “key” → searchfield, “scond” → searchfields, “mcond” → get\_match\_cond(doctype))), mapping(“txt” → (“%%% ….

**Local steps**

- Set doctype from “Lead”.
- Set fields from get\_fields(doctype, list(“name”, “lead\_name”, “company\_name”)).
- Set searchfields from Platform.get\_meta(doctype).get\_search\_fields().
- Set searchfields from “ or ”.join(generator of (field + “ like %(txt)s”) for field drawn from searchfields).
  - Draw field from searchfields.
- Return Platform.db.sql(query text (SELECT, Lead).format(expanded names mapping(“fields” → “, ”.join(fields), “key” → searchfield, “scond” → searchfields, “mcond” → get\_match\_cond(doctype))), mapping(“txt” → (“%%% ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L829) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L510)

<a id="op-7050290ec9225e"></a>
### Tax account query

`operation_enterprise_controllers_queries_business_behavior_tax_account_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** tax\_accounts.

**Local steps**

- Set doctype from “Account”.
- Set company\_currency from Enterprise.get\_company\_currency(filters.get(“company”)).
- Bind local operation get\_accounts for subsequent calls.
- Set tax\_accounts from get\_accounts(true).
- If not tax\_accounts.
  - Set tax\_accounts from get\_accounts(false).
- Return tax\_accounts.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L831) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L512)

<a id="op-df08a3fe52429a"></a>
### Tax account query.get accounts

`operation_enterprise_controllers_queries_business_behavior_tax_account_query_get_accounts`

**Inputs** with\_account\_type\_filter.

**State and service calls** execute a supplied database query.

**Explicit results** accounts.

**Local steps**

- Set account\_type\_condition from empty text.
- If with\_account\_type\_filter.
  - Set account\_type\_condition from “AND account\_type in %(account\_types)s”.
- Set accounts from Platform.db.sql(formatted text   SELECT name, parent\_account  FROM ′tabAccount′  WHERE ′tabAccount′.docstatus!=2  {account\_type\_condition}  AND is\_group = 0  AND comp, dict(account\_types = f ….
- Return accounts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L832) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L513)

<a id="op-5a09cef5e5921e"></a>
### Party query

`operation_enterprise_controllers_queries_business_behavior_party_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** query.run().

**Explicit failure paths** validation helper — translated “Invalid party type: {0}”.format(doctype) · validation helper — translated “Party query filters must be a dictionary”.

**Local steps**

- Set party\_name\_field from mapping(“Customer” → “customer\_name”, “Supplier” → “supplier\_name”).get(doctype).
- If not party\_name\_field.
  - Call the validation error handler Platform.throw(translated “Invalid party type: {0}”.format(doctype)).
- Set filters from Platform.parse\_json(filters) when filters, otherwise mapping().
  - Value choice on filters — true gives Platform.parse\_json(filters), false gives mapping().
- If not isinstance(filters, dict).
  - Call the validation error handler Platform.throw(translated “Party query filters must be a dictionary”).
- Set company from filters.pop(“company”, no value).
- Set fields from get\_fields(doctype, list(“name”, party\_name\_field)).
- Set party from DocType(doctype).
- Set search\_str from formatted text %{txt}%.
- Set txt\_no\_percent from txt.replace(“%”, empty text).
- Set search\_fields from list(dict.fromkeys(list(searchfield, expanded fields))).
- Set search\_conditions from list of party at field.like(search\_str) for field drawn from search\_fields.
  - Draw field from search\_fields.
- Set query from nested operand in the contract(nested operand in the contract).orderby(party at party\_name\_field).limit(page\_len).offset(start).
- If company.
  - Set query from query.where(get\_restriction\_criterion(doctype, list(company))).
- Return query.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0378.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L830) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L511)

<a id="op-78f29f128b84c9"></a>
### Item query

`operation_enterprise_controllers_queries_business_behavior_item_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters, as\_dict = false.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** execute query text (SELECT, Item, Item Barcode).format(columns = columns, scond = searchfields, fcond = get\_filters\_cond(doctype, filters, conditions).replace(“%”, “%%”), mcond = get\_match\_cond(doctype), …).

**Explicit results** list() when as\_dict, otherwise tuple() · Platform.db.sql(query text (SELECT, Item, Item Barcode).format(columns = columns, scond = searchfields, fcond = get\_filters\_cond(doctype, filters, conditions).replace(“%”, “%%”), mcond = get\_match\_cond(doc ….

**Local steps**

- Set doctype from “Item”.
- Set conditions from list().
- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- Set company from filters.pop(“company”, no value) when isinstance(filters, dict), otherwise no value.
  - Value choice on isinstance(filters, dict) — true gives filters.pop(“company”, no value), false gives no value.
- Set meta from Platform.get\_meta(doctype, cached = true).
- Set searchfields from meta.get\_search\_fields().
- Set columns from empty text.
- Set extra\_searchfields from list of field for field drawn from searchfields where field does not belong to list(“name”, “description”).
  - Draw field from searchfields, keep a combination only if (field does not belong to list(“name”, “description”)).
- If extra\_searchfields.
  - Update columns using + (“, ” + “, ”.join(extra\_searchfields)).
- If “description” belongs to searchfields.
  - Update columns using + “, if(length(tabItem.description) &gt; 40, \\t\\t\\tconcat(substr(tabItem.description, 1, 40), "..."), description) …”.
- Set searchfields from (searchfields + list of field for field drawn from list((searchfield or “name”), “item\_code”, “item\_group”, “item\_name”) where field does not belong to searchfields).
  - Draw field from list((searchfield or “name”), “item\_code”, “item\_group”, “item\_name”), keep a combination only if (field does not belong to searchfields).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in searchfield → “name”.
- Set searched\_fields from list(searchfields).
- Set searchfields from “ or ”.join(list of (field + “ like %(txt)s”) for field drawn from searchfields).
  - Draw field from searchfields.
- Set allowed\_items\_cond from empty text.
- If (filters and isinstance(filters, dict)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → isinstance(filters, dict).
  - If (filters.get(“customer”) or filters.get(“supplier”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“customer”) → filters.get(“supplier”).
    - Set party\_type from “Customer” when filters.get(“customer”), otherwise “Supplier”.
      - Value choice on filters.get(“customer”) — true gives “Customer”, false gives “Supplier”.
    - Set party from (filters.get(“customer”) or filters.get(“supplier”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“customer”) → filters.get(“supplier”).
    - Set allowed\_items\_cond from get\_allowed\_items\_cond(party\_type, party).
    - If filters.get(“customer”).
      - Remove filters at “customer”.
    - Otherwise.
      - Remove filters at “supplier”.
  - Otherwise.
    - Evaluate filters.pop(“customer”, no value).
    - Evaluate filters.pop(“supplier”, no value).
- Set company\_cond from empty text.
- Set company\_params from NamedParameterWrapper().
- If company.
  - Set company\_cond from (“and ” + get\_restriction\_criterion(“Item”, list(company)).get\_sql(with\_namespace = true, quote\_char = “′”, param\_wrapper = company\_params, subquery = true)).
- Set description\_cond from empty text.
- If Platform.db.estimate\_count(doctype) &lt; 50000.
  - Set description\_cond from “or tabItem.description LIKE %(txt)s”.
  - Evaluate searched\_fields.append(“description”).
- Set candidate\_cond from empty text.
- Set candidates from get\_item\_search\_candidates(txt, searched\_fields).
- If candidates is distinct from no value.
  - If not candidates.
    - Return list() when as\_dict, otherwise tuple().
      - Value choice on as\_dict — true gives list(), false gives tuple().
  - Set candidate\_cond from “and tabItem.name in %(candidates)s”.
- Return Platform.db.sql(query text (SELECT, Item, Item Barcode).format(columns = columns, scond = searchfields, fcond = get\_filters\_cond(doctype, filters, conditions).replace(“%”, “%%”), mcond = get\_match\_cond(doc ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in candidates → tuple().

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L828) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L509)

<a id="op-354f668e0654d7"></a>
### Get allowed items cond

`operation_enterprise_binding_enterprise_controllers_queries_get_allowed_items_cond`

**Inputs** party\_type, party.

**Explicit results** empty text · formatted text and tabItem.name in ({allowed\_items}).

**Local steps**

- Set allowed\_items\_condition from get\_allowed\_items\_condition(party\_type, party).
- If allowed\_items\_condition is identical to no value.
  - Return empty text.
- Set item from Platform.qb.DocType(“Item”).
- Set allowed\_items from nested operand in the contract.qb.from\_(item).select(item.name).where(allowed\_items\_condition).
- Return formatted text and tabItem.name in ({allowed\_items}).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1085) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L325)

<a id="op-780df75c70d670"></a>
### Subcontracted item query

`operation_enterprise_binding_enterprise_controllers_queries_subcontracted_item_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Item” via get\_all.

**Explicit results** item\_query(doctype, txt, searchfield, start, …).

**Local steps**

- Set bom\_filter from list(“default\_bom”, “is”, “set”).
- If templates bound to Platform.get\_all(“Item”, filters = mapping(“has\_variants” → 1, “default\_bom” → list(“is”, “set”)), pluck = “name”).
  - Set bom\_filter from list(bom\_filter, “or”, list(“variant\_of”, “in”, templates)).
- Set subcontracted\_filters from list(list(“is\_stock\_item”, “=”, 1), “and”, list(“is\_sub\_contracted\_item”, “=”, 1), “and”, …).
- Return item\_query(doctype, txt, searchfield, start, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1086) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L326)

<a id="op-400a70a25e9f9c"></a>
### Bom

`operation_enterprise_controllers_queries_business_behavior_bill_of_materials`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** execute query text (SELECT, BOM).format(fields = “, ”.join(fields), fcond = get\_filters\_cond(doctype, filters, conditions).replace(“%”, “%%”), mcond = get\_match\_cond(doctype), key = searchfield).

**Explicit results** Platform.db.sql(query text (SELECT, BOM).format(fields = “, ”.join(fields), fcond = get\_filters\_cond(doctype, filters, conditions).replace(“%”, “%%”), mcond = get\_match\_cond(doctype), key = searchfield), m ….

**Local steps**

- Set doctype from “BOM”.
- Set conditions from list().
- Set fields from get\_fields(doctype, list(“name”, “item”)).
- Return Platform.db.sql(query text (SELECT, BOM).format(fields = “, ”.join(fields), fcond = get\_filters\_cond(doctype, filters, conditions).replace(“%”, “%%”), mcond = get\_match\_cond(doctype), key = searchfield), m ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in start → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page\_len → 20.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L801) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L482)

<a id="op-cf92117d79610f"></a>
### Get project name

`operation_enterprise_controllers_queries_business_behavior_get_project_name`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Project” via get\_list.

**Explicit results** Platform.get\_list(“Project”, filters = list\_filters, fields = fields, order\_by = “idx desc, name”, limit\_start = start, …) · list() · q.run().

**Local steps**

- Set proj from qb.DocType(“Project”).
- Set meta from Platform.get\_meta(doctype).
- Set list\_filters from list(list(“status”, “not in”, list(“Completed”, “Cancelled”, “On hold”))).
- If filters.
  - If filters.get(“customer”).
    - Evaluate list\_filters.append(list(“customer”, “in”, list(filters.get(“customer”), empty text))).
  - If filters.get(“company”).
    - Evaluate list\_filters.append(list(“company”, “=”, filters.get(“company”))).
- Set searchfields from list of x for x drawn from meta.get\_search\_fields() where (x does not belong to list(“customer”, “status”) and not (meta.get\_field(x) and nested operand in the contract.get\_field(x).permlevel)).
  - Draw x from meta.get\_search\_fields(), keep a combination only if ((x does not belong to list(“customer”, “status”) and not (meta.get\_field(x) and meta.get\_field(x).permlevel))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in x does not belong to list(“customer”, “status”) → not (meta.get\_field(x) and meta.get\_field(x).permlevel).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.get\_field(x) → meta.get\_field(x).permlevel.
- Set fields from get\_fields(doctype, list(“name”, “project\_name”)).
- If not txt.
  - Return Platform.get\_list(“Project”, filters = list\_filters, fields = fields, order\_by = “idx desc, name”, limit\_start = start, …).
- Set permitted from Platform.get\_list(“Project”, filters = list\_filters, or\_filters = list of list(x, “like”, formatted text %{txt}%) for x drawn from searchfields, pluck = “name”, order\_by = empty text, …).
  - Draw x from searchfields.
- If not permitted.
  - Return list().
- Set q from nested operand in the contract.qb.from\_(proj).select(expanded list of proj at fieldname for fieldname drawn from fields).where(proj.name.isin(permitted)).
  - Draw fieldname from fields.
- Set q from q.orderby(Case().when(Locate(txt, nested operand in the contract.project\_name) &gt; 0, Locate(txt, proj.project\_name)).else\_(99999)).
- Set q from q.orderby(proj.idx, order = Order.desc).orderby(proj.name).
- If page\_len.
  - Set q from q.limit(page\_len).
- If start.
  - Set q from q.offset(start).
- Return q.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L819) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L500)

<a id="op-199ab70f587870"></a>
### Get delivery notes to be billed

`operation_enterprise_controllers_queries_business_behavior_get_delivery_notes_to_be_billed`

**Inputs** doctype, txt, searchfield, start, page\_len, filters, as\_dict = false.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** query.run(as\_dict = as\_dict).

**Local steps**

- Set DeliveryNote from Platform.qb.DocType(“Delivery Note”).
- Set fields from get\_fields(doctype, list(“name”, “customer”, “posting\_date”)).
- Set original\_dn from nested operand in the contract.qb.from\_(DeliveryNote).select(DeliveryNote.name).where(((DeliveryNote.docstatus equals 1 bitwise and DeliveryNote.is\_return equals 0) bitwise and DeliveryNote.per\_billed &gt; 0)).
- Set query from Platform.qb.get\_query(“Delivery Note”, fields = fields, filters = filters, ignore\_permissions = false).
- Set query from nested operand in the contract(nested operand in the contract).orderby(DeliveryNote at searchfield, order = Order.asc).limit(page\_len).offset(start).
- Return query.run(as\_dict = as\_dict).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L490)

<a id="op-257e70aa6f447f"></a>
### Get batch no

`operation_enterprise_controllers_queries_business_behavior_get_batch_number`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** filtered\_batches.

**Local steps**

- Set doctype from “Batch”.
- Set meta from Platform.get\_meta(doctype, cached = true).
- Set searchfields from meta.get\_search\_fields().
- Set page\_len from 300.
- Set batches from get\_batches\_from\_stock\_ledger\_entries(searchfields, txt, filters, start, …).
- Evaluate batches.extend(get\_batches\_from\_serial\_and\_batch\_bundle(searchfields, txt, filters, start, …)).
- Set filtered\_batches from get\_filterd\_batches(batches).
- If filters.get(“is\_inward”).
  - Evaluate filtered\_batches.extend(get\_empty\_batches(filters, start, page\_len, filtered\_batches, …)).
- Return filtered\_batches.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L804) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L485)
