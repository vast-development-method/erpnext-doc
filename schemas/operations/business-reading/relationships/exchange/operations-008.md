# Integrations and service calls · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Form

<a id="op-4f989050bcc667"></a>
### Seed visible fields.break

`operation_relationships_application_interface_form_business_behavior_seed_visible_fields_break`

**Inputs** fieldtype, i, label = empty text.

**Explicit results** mapping(“fieldname” → formatted text {prefix}\_seed{i}, “label” → label, “fieldtype” → fieldtype, “options” → empty text, …).

**Local steps**

- Set prefix from “section\_break” when fieldtype equals “Section Break”, otherwise “column\_break”.
  - Value choice on fieldtype equals “Section Break” — true gives “section\_break”, false gives “column\_break”.
- Return mapping(“fieldname” → formatted text {prefix}\_seed{i}, “label” → label, “fieldtype” → fieldtype, “options” → empty text, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L6639) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L99) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L81)

<a id="op-0e5ca936d1cdb9"></a>
### Seed hidden fields

`operation_relationships_application_interface_form_business_behavior_seed_hidden_fields`

**Inputs** document\_type.

**Declared result** list at dict.

**Explicit results** hidden.

**Local steps**

- Set meta from Platform.get\_meta(document\_type).
- Set visible from \_seeded\_visible\_fieldnames(document\_type).
- Set hidden from list().
- For each df in meta.fields.
  - If (not df.reqd or df.fieldname belongs to visible).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df.reqd → df.fieldname belongs to visible.
    - Continue with the next iteration or loop test.
  - If (df.fieldtype belongs to SUPPORTED\_FIELDTYPES and df.fieldname does not belong to DENIED\_FIELDNAMES).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype belongs to SUPPORTED\_FIELDTYPES → df.fieldname does not belong to DENIED\_FIELDNAMES.
    - Continue with the next iteration or loop test.
  - Set default from \_default\_status(document\_type) when df.fieldname equals “status”, otherwise (df.default or empty text).
    - Value choice on df.fieldname equals “status” — true gives \_default\_status(document\_type), false gives (df.default or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.default → empty text.
  - Evaluate hidden.append(mapping(“fieldname” → df.fieldname, “label” → (df.label or df.fieldname), “fieldtype” → df.fieldtype, “options” → (df.options or empty text), …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → df.fieldname.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.options → empty text.
- Return hidden.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L6875) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L97) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L79)

<a id="op-78f4b5f27f3ecb"></a>
### Check manager

`operation_relationships_application_interface_form_business_behavior_check_manager`

**Inputs** no declared parameters.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Set roles from set(Platform.get\_roles()).
- If not (roles bitwise and set(“System Manager”, “Sales Manager”)).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L7340) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L80) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L62)

<a id="op-cbcbf9a599c134"></a>
### Get form fields

`operation_relationships_application_interface_form_business_behavior_get_form_fields`

**Inputs** document\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** \_mappable\_fields(document\_type).

**Explicit failure paths** validation helper — translated “Forms can only map to: {0}”.format(“, ”.join(ALLOWED\_DOCTYPES)).

**Local steps**

- If document\_type does not belong to ALLOWED\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Forms can only map to: {0}”.format(“, ”.join(ALLOWED\_DOCTYPES))).
- Return \_mappable\_fields(document\_type).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L7480) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L87) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L69)

<a id="op-3e8c4c8692cf56"></a>
### Get hidden seed

`operation_relationships_application_interface_form_business_behavior_get_hidden_seed`

**Inputs** document\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** \_seed\_hidden\_fields(document\_type).

**Explicit failure paths** validation helper — translated “Forms can only map to: {0}”.format(“, ”.join(ALLOWED\_DOCTYPES)).

**Local steps**

- If document\_type does not belong to ALLOWED\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Forms can only map to: {0}”.format(“, ”.join(ALLOWED\_DOCTYPES))).
- Return \_seed\_hidden\_fields(document\_type).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L7661) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L88) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L70)

<a id="op-d5309ef0ec4e1e"></a>
### Link field guest access

`operation_relationships_application_interface_form_business_behavior_link_field_guest_access`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“doctype” → doctype, “guest\_can\_select” → guest\_can\_select(doctype)).

**Local steps**

- Evaluate \_check\_manager().
- Return mapping(“doctype” → doctype, “guest\_can\_select” → guest\_can\_select(doctype)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L91) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L73)

<a id="op-3a92e421b35df5"></a>
### Grant guest link access

`operation_relationships_application_interface_form_business_behavior_grant_guest_link_access`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Custom DocPerm” via get\_value · resolve a document from “Custom DocPerm” via get\_doc.

**State and service calls** call save on perm.

**Explicit results** mapping(“doctype” → doctype, “guest\_can\_select” → guest\_can\_select(doctype)).

**Explicit failure paths** validation helper — translated “{0} isn't a linkable field on a CRM form.”.format(doctype).

**Local steps**

- Evaluate \_check\_manager().
- If doctype does not belong to \_link\_target\_doctypes().
  - Call the validation error handler Platform.throw(translated “{0} isn't a linkable field on a CRM form.”.format(doctype)).
- If not guest\_can\_select(doctype).
  - Bind dependencies add\_permission.
  - Set had\_flag from Platform.flags.ignore\_permissions.
  - Set Platform.flags.ignore\_permissions from true.
  - Attempt the following.
    - Set perm\_name from Platform.db.get\_value(“Custom DocPerm”, mapping(“parent” → doctype, “role” → “Guest”, “permlevel” → 0, “if\_owner” → 0)).
    - If not perm\_name.
      - Evaluate add\_permission(doctype, “Guest”, 0, ptype = “select”).
      - Set perm\_name from Platform.db.get\_value(“Custom DocPerm”, mapping(“parent” → doctype, “role” → “Guest”, “permlevel” → 0, “if\_owner” → 0)).
    - Set perm from Platform.get\_doc(“Custom DocPerm”, perm\_name).
    - Evaluate perm.update(mapping(“select” → 1, “read” → 0, “write” → 0, “create” → 0, …)).
    - Evaluate perm.save(ignore\_permissions = true).
  - On exit, including pending return or failure.
    - Set Platform.flags.ignore\_permissions from had\_flag.
  - Evaluate Platform.clear\_cache(doctype = doctype).
- Return mapping(“doctype” → doctype, “guest\_can\_select” → guest\_can\_select(doctype)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L127) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L89) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L71)

<a id="op-ac94e09b297c9c"></a>
### List forms

`operation_relationships_application_interface_form_business_behavior_list_forms`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Web Form” via get\_all.

**Explicit results** Platform.get\_all(“Web Form”, filters = mapping(“module” → FORM\_MODULE, “doc\_type” → list(“in”, ALLOWED\_DOCTYPES)), fields = list(“name”, “title”, “route”, “doc\_type as document\_type”, …), order\_by = “modified desc”).

**Local steps**

- Evaluate \_check\_manager().
- Return Platform.get\_all(“Web Form”, filters = mapping(“module” → FORM\_MODULE, “doc\_type” → list(“in”, ALLOWED\_DOCTYPES)), fields = list(“name”, “title”, “route”, “doc\_type as document\_type”, …), order\_by = “modified desc”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L1056) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L93) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L75)

<a id="op-cfa32007b51cca"></a>
### Get form config

`operation_relationships_application_interface_form_business_behavior_get_form_configuration`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“name” → doc.name, “title” → doc.title, “route” → doc.route, “document\_type” → doc.doc\_type, …).

**Local steps**

- Evaluate \_check\_manager().
- Set doc from \_get\_crm\_form(name).
- Return mapping(“name” → doc.name, “title” → doc.title, “route” → doc.route, “document\_type” → doc.doc\_type, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.button\_label → translated “Submit”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.introduction\_text → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.success\_message → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.success\_url → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.allowed\_embedding\_domains → empty text.
  - Draw f from doc.web\_form\_fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.depends\_on → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.mandatory\_depends\_on → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.read\_only\_depends\_on → empty text.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L7) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L86) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L68)

<a id="op-a10d7d156e1eca"></a>
### Load hidden fields

`operation_relationships_application_interface_form_business_behavior_load_hidden_fields`

**Inputs** doc.

**Declared result** list at dict.

**Explicit results** json.loads((doc.get(“crm\_hidden\_defaults”) or “&#91;&#93;”)) · list().

**Local steps**

- Attempt the following.
  - Return json.loads((doc.get(“crm\_hidden\_defaults”) or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“crm\_hidden\_defaults”) → “&#91;&#93;”.
- On failure (Exception).
  - Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L1929) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L94) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L76)

<a id="op-8621657eeadc42"></a>
### Assert hidden defaults set

`operation_relationships_application_interface_form_business_behavior_assert_hidden_defaults_set`

**Inputs** hidden.

**Explicit failure paths** validation helper — translated “Set a default value before publishing for: {0}”.format(“, ”.join(missing)).

**Local steps**

- Set missing from list of (h.get(“label”) or h.get(“fieldname”)) for h drawn from hidden where not str((nested operand in the contract(nested operand in the contract) or empty text)).strip().
  - Draw h from hidden, keep a combination only if (not str((nested operand in the contract.get(“default”) or empty text)).strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in h.get(“label”) → h.get(“fieldname”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in h.get(“default”) → empty text.
- If missing.
  - Call the validation error handler Platform.throw(translated “Set a default value before publishing for: {0}”.format(“, ”.join(missing))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L2048) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L79) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L61)

<a id="op-fe6b4396edc57a"></a>
### Validated visible fields

`operation_relationships_application_interface_form_business_behavior_validated_visible_fields`

**Inputs** document\_type, fields.

**Declared result** list at dict.

**Explicit results** rows.

**Explicit failure paths** validation helper — translated “{0} can't be used as a layout break”.format(fieldname) · validation helper — translated “{0} can't be collected by a form”.format((fieldname or translated “Unnamed field”)).

**Local steps**

- Set meta from Platform.get\_meta(document\_type).
- Set catalog from mapping of f at “fieldname” → f for f drawn from \_mappable\_fields(document\_type).
  - Draw f from \_mappable\_fields(document\_type).
- Set rows from list().
- For each f in fields.
  - Set fieldname from f.get(“fieldname”).
  - If f.get(“fieldtype”) belongs to LAYOUT\_BREAKS.
    - If meta.has\_field(fieldname).
      - Call the validation error handler Platform.throw(translated “{0} can't be used as a layout break”.format(fieldname)).
    - Evaluate rows.append(f).
    - Continue with the next iteration or loop test.
  - Set allowed from catalog.get(fieldname).
  - If not allowed.
    - Call the validation error handler Platform.throw(translated “{0} can't be collected by a form”.format((fieldname or translated “Unnamed field”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname → translated “Unnamed field”.
  - Evaluate rows.append(mapping(expand f, “fieldtype” → allowed at “fieldtype”, “options” → allowed at “options”)).
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L2320) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L104) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L86)

<a id="op-d8508c69de0e29"></a>
### Validated hidden fields

`operation_relationships_application_interface_form_business_behavior_validated_hidden_fields`

**Inputs** document\_type, hidden.

**Declared result** list at dict.

**Explicit results** rows.

**Explicit failure paths** validation helper — translated “{0} can't be set as a hidden field”.format((fieldname or translated “Unnamed field”)).

**Local steps**

- Set catalog from mapping of h at “fieldname” → h for h drawn from \_seed\_hidden\_fields(document\_type).
  - Draw h from \_seed\_hidden\_fields(document\_type).
- Set rows from list().
- For each h in hidden.
  - Set fieldname from h.get(“fieldname”).
  - Set allowed from catalog.get(fieldname).
  - If not allowed.
    - Call the validation error handler Platform.throw(translated “{0} can't be set as a hidden field”.format((fieldname or translated “Unnamed field”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname → translated “Unnamed field”.
  - Evaluate rows.append(mapping(expand h, “fieldtype” → allowed at “fieldtype”, “options” → allowed at “options”)).
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L2906) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L103) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L85)

<a id="op-d70fdc3687a2ef"></a>
### Save form

`operation_relationships_application_interface_form_business_behavior_save_form`

**Inputs** name, form.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**State and service calls** request new\_doc for “Web Form” · call save on doc.

**Explicit results** mapping(“name” → doc.name, “route” → doc.route).

**Explicit failure paths** validation helper — translated “Forms can only map to: {0}”.format(“, ”.join(ALLOWED\_DOCTYPES)).

**Local steps**

- Evaluate \_check\_manager().
- If isinstance(form, str).
  - Set form from json.loads((form or “{}”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in form → “{}”.
- If form.get(“document\_type”) does not belong to ALLOWED\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Forms can only map to: {0}”.format(“, ”.join(ALLOWED\_DOCTYPES))).
- Set doc from \_get\_crm\_form(name) when name, otherwise Platform.new\_doc(“Web Form”).
  - Value choice on name — true gives \_get\_crm\_form(name), false gives Platform.new\_doc(“Web Form”).
- Set doc.title from form.get(“title”).
- Set doc.route from form.get(“route”).
- Set doc.doc\_type from form.get(“document\_type”).
- Set doc.introduction\_text from form.get(“description”).
- Set doc.button\_label from (form.get(“submit\_button\_label”) or “Submit”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in form.get(“submit\_button\_label”) → “Submit”.
- Set doc.success\_message from form.get(“success\_message”).
- Set doc.success\_url from (form.get(“redirect\_url”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in form.get(“redirect\_url”) → empty text.
- Set doc.allowed\_embedding\_domains from form.get(“allowed\_embedding\_domains”).
- Set doc.crm\_published from 1 when form.get(“published”), otherwise 0.
  - Value choice on form.get(“published”) — true gives 1, false gives 0.
- Set doc.published from doc.crm\_published.
- Set doc.login\_required from 0.
- Set doc.allow\_multiple from 1.
- Set doc.is\_standard from 0.
- Set doc.module from FORM\_MODULE.
- Set fields from form.get(“fields”).
- If (not name and not fields).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not name → not fields.
  - Set fields from \_seed\_visible\_fields(form at “document\_type”).
- If fields is distinct from no value.
  - Set fields from \_validated\_visible\_fields(form at “document\_type”, fields).
  - Evaluate doc.set(“web\_form\_fields”, list()).
  - For each tuple(i, f) in enumerate(fields).
    - Evaluate doc.append(“web\_form\_fields”, mapping(“fieldname” → f.get(“fieldname”), “label” → f.get(“label”), “fieldtype” → f.get(“fieldtype”), “options” → f.get(“options”), …)).
      - Value choice on f.get(“reqd”) — true gives 1, false gives 0.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.get(“depends\_on”) → empty text.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.get(“mandatory\_depends\_on”) → empty text.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.get(“read\_only\_depends\_on”) → empty text.
- Set hidden from form.get(“hidden\_fields”).
- If (hidden is identical to no value and not name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hidden is identical to no value → not name.
  - Set hidden from \_seed\_hidden\_fields(form at “document\_type”).
- If isinstance(hidden, str).
  - Set hidden from json.loads((hidden or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in hidden → “&#91;&#93;”.
- Set hidden from \_validated\_hidden\_fields(form at “document\_type”, (hidden or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hidden → list().
- If doc.crm\_published.
  - Evaluate \_assert\_hidden\_defaults\_set(hidden).
- Set doc.crm\_hidden\_defaults from json.dumps(hidden) when hidden, otherwise empty text.
  - Value choice on hidden — true gives json.dumps(hidden), false gives empty text.
- Evaluate doc.save(ignore\_permissions = true).
- Return mapping(“name” → doc.name, “route” → doc.route).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L3318) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L96) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L78)

<a id="op-80b86c4fd38c52"></a>
### Get crm form

`operation_relationships_application_interface_form_business_behavior_get_customer_relationship_form`

**Inputs** name.

**Record and data access** resolve a document from “Web Form” via get\_doc.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “Not a CRM form”.

**Local steps**

- Set doc from Platform.get\_doc(“Web Form”, name).
- If (doc.module differs from FORM\_MODULE or doc.doc\_type does not belong to ALLOWED\_DOCTYPES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.module differs from FORM\_MODULE → doc.doc\_type does not belong to ALLOWED\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Not a CRM form”).
- Return doc.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L5168) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L85) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L67)

<a id="op-0d466aa4dc972f"></a>
### Set published

`operation_relationships_application_interface_form_business_behavior_set_published`

**Inputs** name, published.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**State and service calls** call save on doc.

**Local steps**

- Evaluate \_check\_manager().
- Set doc from \_get\_crm\_form(name).
- If int(published).
  - Evaluate \_assert\_hidden\_defaults\_set(\_load\_hidden\_fields(doc)).
- Set doc.crm\_published from 1 when int(published), otherwise 0.
  - Value choice on int(published) — true gives 1, false gives 0.
- Set doc.published from doc.crm\_published.
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L5341) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L101) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L83)

<a id="op-e5fac263765655"></a>
### Delete form

`operation_relationships_application_interface_form_business_behavior_delete_form`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**State and service calls** request delete\_doc for “Web Form”.

**Local steps**

- Evaluate \_check\_manager().
- Evaluate \_get\_crm\_form(name).
- Evaluate Platform.delete\_doc(“Web Form”, name, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L5596) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L82) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L64)

<a id="op-0fec789509476c"></a>
### Test submit form

`operation_relationships_application_interface_form_business_behavior_test_submit_form`

**Inputs** name, values.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“test” → true).

**Explicit failure paths** validation helper — translated “{0} is required”.format((f.label or f.fieldname)).

**Local steps**

- Evaluate \_check\_manager().
- If isinstance(values, str).
  - Set values from json.loads((values or “{}”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → “{}”.
- Set doc from \_get\_crm\_form(name).
- For each f in doc.web\_form\_fields.
  - If f.fieldtype belongs to tuple(“Section Break”, “Column Break”).
    - Continue with the next iteration or loop test.
  - Set value from values.get(f.fieldname).
  - If (f.reqd and (value is identical to no value or value equals empty text)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.reqd → (value is identical to no value or value equals empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value is identical to no value → value equals empty text.
    - Call the validation error handler Platform.throw(translated “{0} is required”.format((f.label or f.fieldname))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.label → f.fieldname.
- Return mapping(“test” → true).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L5732) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L102) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L84)

<a id="op-0ae7f4502bd4f2"></a>
### Enrich form submission

`operation_relationships_application_interface_form_business_behavior_enrich_form_submission`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If not Platform.flags.get(“in\_web\_form”).
  - Return no value.
- If doc.doctype does not belong to ALLOWED\_DOCTYPES.
  - Return no value.
- Evaluate \_apply\_hidden\_defaults(doc).
- If (doc.meta.has\_field(“source”) and not doc.get(“source”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.has\_field(“source”) → not doc.get(“source”).
  - Set doc.source from ensure\_form\_source().
- Evaluate capture(“web\_form\_submitted”, “crm”, properties = mapping(“doctype” → doc.doctype, “form” → Platform.form\_dict.get(“web\_form”))).
- If doc.doctype differs from “CRM Deal”.
  - Return no value.
- Bind dependencies create\_contact, create\_organization.
- If (doc.get(“organization\_name”) and not doc.get(“organization”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“organization\_name”) → not doc.get(“organization”).
  - Set created from create\_organization(doc).
  - If created.
    - Set doc.organization from created.
- If (not doc.get(“contacts”) and (doc.get(“first\_name”) or doc.get(“last\_name”) or doc.get(“email”) or doc.get(“mobile\_no”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.get(“contacts”) → (doc.get(“first\_name”) or doc.get(“last\_name”) or doc.get(“email”) or doc.get(“mobile\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“first\_name”) → doc.get(“last\_name”) → doc.get(“email”) → doc.get(“mobile\_no”).
  - Set contact from create\_contact(doc).
  - If contact.
    - Evaluate doc.append(“contacts”, mapping(“contact” → contact, “is\_primary” → 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L6160) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L83) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L65)

<a id="op-9ad2c6f476f8f4"></a>
### Apply hidden defaults

`operation_relationships_application_interface_form_business_behavior_apply_hidden_defaults`

**Inputs** doc.

**Record and data access** read “Web Form” via get\_value.

**Explicit results** no value.

**Local steps**

- Set web\_form from Platform.form\_dict.get(“web\_form”).
- If not web\_form.
  - Return no value.
- Set form from Platform.db.get\_value(“Web Form”, web\_form, list(“doc\_type”, “crm\_hidden\_defaults”), as\_dict = true).
- If (not form or form.doc\_type does not belong to ALLOWED\_DOCTYPES or form.doc\_type differs from doc.doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not form → form.doc\_type does not belong to ALLOWED\_DOCTYPES → form.doc\_type differs from doc.doctype.
  - Return no value.
- Set raw from form.crm\_hidden\_defaults.
- If not raw.
  - Return no value.
- Attempt the following.
  - Set hidden from json.loads(raw).
- On failure (Exception).
  - Return no value.
- For each h in hidden.
  - Set fieldname from h.get(“fieldname”).
  - Set default from h.get(“default”).
  - If (fieldname and default does not belong to tuple(no value, empty text) and doc.meta.has\_field(fieldname) and not doc.get(fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname → default does not belong to tuple(no value, empty text) → doc.meta.has\_field(fieldname) → not doc.get(fieldname).
    - Evaluate doc.set(fieldname, default).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0011.json#L6882) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L78) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L60)

## Service · Handler

<a id="op-3a3bc700a62753"></a>
### Handle request

`operation_relationships_integrations_exotel_handler_business_behavior_handle_request`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**State and service calls** publish realtime with “exotel\_call” · rollback · commit · call save on request\_log.

**Explicit results** no value.

**Local steps**

- Evaluate validate\_request().
- If not is\_integration\_enabled().
  - Return no value.
- Set request\_log from create\_request\_log(kwargs, request\_description = “Exotel Call”, service\_name = “Exotel”, request\_headers = Platform.request.headers, is\_remote\_request = 1).
- Attempt the following.
  - Set request\_log.status from “Completed”.
  - Set exotel\_settings from get\_exotel\_settings().
  - If not exotel\_settings.enabled.
    - Return no value.
  - Set call\_payload from kwargs.
  - If call\_agent bound to get\_call\_agent(call\_payload).
    - Evaluate Platform.publish\_realtime(“exotel\_call”, call\_payload, user = call\_agent).
  - Set status from call\_payload.get(“Status”).
  - If status equals “free”.
    - Return no value.
  - If call\_log bound to get\_call\_log(call\_payload).
    - Evaluate update\_call\_log(call\_payload, call\_log = call\_log).
  - Otherwise.
    - If call\_payload.get(“Direction”) equals “incoming”.
      - Evaluate create\_call\_log(call\_id = call\_payload.get(“CallSid”), from\_number = call\_payload.get(“CallFrom”), to\_number = call\_payload.get(“DialWhomNumber”), medium = call\_payload.get(“To”), …).
    - Otherwise.
      - If agent bound to Platform.request.args.get(“agent”).
        - Evaluate create\_call\_log(call\_id = call\_payload.get(“CallSid”), from\_number = (call\_payload.get(“From”) or call\_payload.get(“CallFrom”)), to\_number = (call\_payload.get(“DialWhomNumber”) or call\_payload.get(“To”)),  ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_payload.get(“From”) → call\_payload.get(“CallFrom”).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_payload.get(“DialWhomNumber”) → call\_payload.get(“To”).
- On failure (Exception).
  - Set request\_log.status from “Failed”.
  - Set request\_log.error from Platform.get\_traceback().
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(title = “Error while creating/updating call record”).
  - Evaluate Platform.db.commit().
- On exit, including pending return or failure.
  - Evaluate request\_log.save(ignore\_permissions = true).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“exotel\_call”, call\_payload, user = call\_agent).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L30) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1338) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1314)

<a id="op-b4d50856b57f1f"></a>
### Make a call

`operation_relationships_integrations_exotel_handler_business_behavior_make_a_call`

**Inputs** to\_number, from\_number = no value, caller\_id = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Telephony Agent” via get\_value · read “CRM Exotel Settings” via get\_single\_value.

**State and service calls** rollback · commit.

**Explicit results** call\_details.

**Explicit failure paths** validation helper — translated “Please setup Exotel integration” · validation helper — translated “You do not have Exotel Number set in your Telephony Agent” · validation helper — translated “Exotel Number {0} is not valid”.format(caller\_id) · validation helper — translated “You do not have mobile number set in your Telephony Agent” · validation helper — exc.get(“Message”).

**Local steps**

- If not is\_integration\_enabled().
  - Call the validation error handler Platform.throw(translated “Please setup Exotel integration”, title = translated “Integration Not Enabled”).
- Set endpoint from get\_exotel\_endpoint(“Calls/connect.json?details=true”).
- If not from\_number.
  - Set from\_number from Platform.get\_value(“CRM Telephony Agent”, mapping(“user” → Platform.session.user), “mobile\_no”).
- If not caller\_id.
  - Set caller\_id from Platform.get\_value(“CRM Telephony Agent”, mapping(“user” → Platform.session.user), “exotel\_number”).
- If not caller\_id.
  - Call the validation error handler Platform.throw(translated “You do not have Exotel Number set in your Telephony Agent”, title = translated “Exotel Number Missing”).
- If (caller\_id and caller\_id does not belong to get\_all\_exophones()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in caller\_id → caller\_id does not belong to get\_all\_exophones().
  - Call the validation error handler Platform.throw(translated “Exotel Number {0} is not valid”.format(caller\_id), title = translated “Invalid Exotel Number”).
- If not from\_number.
  - Call the validation error handler Platform.throw(translated “You do not have mobile number set in your Telephony Agent”, title = translated “Mobile Number Missing”).
- Set record\_call from Platform.db.get\_single\_value(“CRM Exotel Settings”, “record\_call”).
- Set call\_log\_creation\_failed from false.
- Attempt the following.
  - Set response from requests.post(endpoint, data = mapping(“From” → from\_number, “To” → to\_number, “CallerId” → caller\_id, “Record” → “true” when record\_call, otherwise “false”, …)).
    - Value choice on record\_call — true gives “true”, false gives “false”.
  - Evaluate response.raise\_for\_status().
- On failure (requests.exceptions.HTTPError).
  - If exc bound to response.json().get(“RestException”).
    - Call the validation error handler Platform.throw(exc.get(“Message”), title = translated “Exotel Exception”).
- When the protected block completes normally.
  - Set res from response.json().
  - Set call\_payload from res.get(“Call”, mapping()).
  - Attempt the following.
    - Evaluate create\_call\_log(call\_id = call\_payload.get(“Sid”), from\_number = call\_payload.get(“From”), to\_number = call\_payload.get(“To”), medium = call\_payload.get(“PhoneNumberSid”), …).
  - On failure (Exception).
    - Evaluate Platform.db.rollback().
    - Evaluate Platform.log\_error(title = “Error while creating Exotel call log”).
    - Evaluate Platform.db.commit().
    - Set call\_log\_creation\_failed from true.
- Set call\_details from response.json().get(“Call”, mapping()).
- Set call\_details at “CallSid” from call\_details.get(“Sid”, empty text).
- Set call\_details at “call\_log\_creation\_failed” from call\_log\_creation\_failed.
- Return call\_details.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Exotel Settings”, “record\_call”) · service or queued work from requests.post(endpoint, data = mapping(“From” → from\_number, “To” → to\_number, “CallerId” → caller\_id, “Record” → “true” when record\_call, otherwise “false”, …)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L5756) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1341) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1317)

<a id="op-876ea457658bb9"></a>
### Get exotel endpoint

`operation_relationships_integrations_exotel_handler_business_behavior_get_exotel_endpoint`

**Inputs** action = no value, version = “v1”.

**Explicit results** text in the contract.format(api\_key = settings.api\_key, api\_token = settings.get\_password(“api\_token”), subdomain = settings.subdomain, version = version, …).

**Local steps**

- Set settings from get\_exotel\_settings().
- Return text in the contract.format(api\_key = settings.api\_key, api\_token = settings.get\_password(“api\_token”), subdomain = settings.subdomain, version = version, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L7181) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1335) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1311)

<a id="op-a211af8418ddd0"></a>
### Get all exophones

`operation_relationships_integrations_exotel_handler_business_behavior_get_all_exophones`

**Inputs** no declared parameters.

**Explicit results** list of phone.get(“friendly\_name”) for phone drawn from response.json().get(“incoming\_phone\_numbers”, list()).

**Local steps**

- Set endpoint from get\_exotel\_endpoint(“IncomingPhoneNumbers”, “v2\_beta”).
- Set response from requests.get(endpoint).
- Return list of phone.get(“friendly\_name”) for phone drawn from response.json().get(“incoming\_phone\_numbers”, list()).
  - Draw phone from response.json().get(“incoming\_phone\_numbers”, list()).

**Values supplied outside this operation** service or queued work from requests.get(endpoint).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L7359) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1332) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1308)
