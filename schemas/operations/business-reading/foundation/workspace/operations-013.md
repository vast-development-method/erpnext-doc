# Forms, reports and navigation · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Custom field

[Record definition](../../../../data/record-types/custom_field.json)

<a id="op-6838dab866e12b"></a>
### Create custom fields

`operation_foundation_custom_record_definitions_custom_field_business_behavior_create_custom_fields`

**Inputs** custom\_fields, ignore\_validate = false, update = true.

**Record and data access** resolve a document from mapping(“doctype” → “Custom Field”, expand field) via get\_doc.

**State and service calls** call save on custom\_field.

**Local steps**

- Bind local operation process\_field\_update for subsequent calls.
- Attempt the following.
  - Set Platform.flags.in\_create\_custom\_fields from true.
  - Set doctypes\_to\_update from set().
  - If Platform.flags.in\_setup\_wizard.
    - Set ignore\_validate from true.
  - Set existing\_custom\_fields from get\_existing\_custom\_fields(custom\_fields).
  - For each tuple(doctypes, fields) in custom\_fields.items().
    - If isinstance(fields, dict).
      - Set fields from tuple(fields).
    - If isinstance(doctypes, str).
      - Set doctypes from tuple(doctypes).
    - For each doctype in doctypes.
      - Set updated from false.
      - For each df in fields.
        - Set field from existing\_custom\_fields.get(tuple(doctype, df at “fieldname”)).
        - If not field.
          - Attempt the following.
            - Set df from df.copy().
            - Set df at “owner” from “Administrator”.
            - Set custom\_field from create\_custom\_field(doctype, df, ignore\_validate = ignore\_validate).
            - Evaluate process\_field\_update(custom\_field).
          - On failure (Platform.exceptions.DuplicateEntryError).
            - Take no action here.
        - Otherwise.
          - If update.
            - Set custom\_field from Platform.get\_doc(mapping(“doctype” → “Custom Field”, expand field)).
            - Set original\_values from custom\_field.\_\_dict\_\_.copy().
            - Evaluate custom\_field.update(df).
            - If original\_values differs from custom\_field.\_\_dict\_\_.
              - If ignore\_validate.
                - Set custom\_field.flags.ignore\_validate from true.
              - Evaluate custom\_field.save().
              - Evaluate process\_field\_update(custom\_field).
      - If updated.
        - Evaluate doctypes\_to\_update.add(doctype).
  - For each doctype in doctypes\_to\_update.
    - Evaluate Platform.clear\_cache(doctype = doctype).
    - Evaluate Platform.db.updatedb(doctype).
- On exit, including pending return or failure.
  - Set Platform.flags.in\_create\_custom\_fields from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L5749) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L930)

<a id="op-13c2e0a6779919"></a>
### Create custom fields.process field update

`operation_foundation_custom_record_definitions_custom_field_business_behavior_create_custom_fields_process_field_update`

**Inputs** field.

**Local steps**

- Use enclosing bindings updated.
- Set updated from true.
- Set existing\_custom\_fields at tuple(field.dt, field.fieldname) from field.\_\_dict\_\_.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L6709) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L931)

<a id="op-84c36cac25c1ba"></a>
### Get existing custom fields

`operation_foundation_custom_record_definitions_custom_field_business_behavior_get_existing_custom_fields`

**Inputs** custom\_fields.

**Record and data access** read “Custom Field” via get\_all.

**Explicit results** mapping of tuple(field.dt, field.fieldname) → field for field drawn from existing\_fields.

**Local steps**

- Set doctypes\_to\_fetch from set().
- For each doctypes in custom\_fields.
  - If isinstance(doctypes, str).
    - Set doctypes from tuple(doctypes).
  - For each doctype in doctypes.
    - Evaluate doctypes\_to\_fetch.add(doctype).
- Set existing\_fields from Platform.get\_all(“Custom Field”, filters = mapping(“dt” → tuple(“in”, doctypes\_to\_fetch)), fields = “\*”).
- Return mapping of tuple(field.dt, field.fieldname) → field for field drawn from existing\_fields.
  - Draw field from existing\_fields.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L6800) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L941)

<a id="op-02573d1b2b8a72"></a>
### Rename fieldname

`operation_foundation_custom_record_definitions_custom_field_business_behavior_rename_fieldname`

**Inputs** custom\_field, fieldname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Custom Field” via get\_doc.

**State and service calls** msgprint with translated “Old and new fieldnames are same.” · call db\_set on field · msgprint with translated “Custom field renamed to {0} successfully.”.format(fieldname) · commit.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “System Generated Fields can not be renamed” · validation helper — translated “Can not rename as column {0} is already present on DocType.”.format(fieldname).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set field from Platform.get\_doc(“Custom Field”, custom\_field).
- Set parent\_doctype from field.dt.
- Set old\_fieldname from field.fieldname.
- Set field.fieldname from fieldname.
- Evaluate field.set\_fieldname().
- Set new\_fieldname from field.fieldname.
- If field.is\_system\_generated.
  - Call the validation error handler Platform.throw(translated “System Generated Fields can not be renamed”).
- If Platform.db.has\_column(parent\_doctype, fieldname).
  - Call the validation error handler Platform.throw(translated “Can not rename as column {0} is already present on DocType.”.format(fieldname)).
- If old\_fieldname equals new\_fieldname.
  - Evaluate Platform.msgprint(translated “Old and new fieldnames are same.”, alert = true).
  - Return no value.
- If Platform.db.has\_column(field.dt, old\_fieldname).
  - Evaluate Platform.db.rename\_column(parent\_doctype, old\_fieldname, new\_fieldname).
- Evaluate field.db\_set(“fieldname”, field.fieldname, notify = true).
- Evaluate \_update\_fieldname\_references(field, old\_fieldname, new\_fieldname).
- Evaluate Platform.msgprint(translated “Custom field renamed to {0} successfully.”.format(fieldname), alert = true).
- Evaluate Platform.db.commit().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0123.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L943)

<a id="op-02c2182bf75c9c"></a>
### Update fieldname references

`operation_foundation_custom_record_definitions_custom_field_business_behavior_update_fieldname_references`

**Inputs** field, old\_fieldname, new\_fieldname.

**Declared result** no value.

**State and service calls** request set\_value on “Custom Field”.

**Local steps**

- If field.fieldtype equals “Password”.
  - Set Auth from Platform.qb.Table(“\_\_Auth”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(Auth.fieldname, new\_fieldname).where((Auth.doctype equals field.dt bitwise and Auth.fieldname equals old\_fieldname)).run().
- Evaluate Platform.db.set\_value(“Custom Field”, mapping(“insert\_after” → old\_fieldname, “dt” → field.dt), “insert\_after”, new\_fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0123.json#L705) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L799) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L944)

<a id="op-c4d4543c38262f"></a>
### Delete custom fields

`operation_foundation_custom_record_definitions_custom_field_business_behavior_delete_custom_fields`

**Inputs** custom\_fields, bypass\_hooks = false.

**Record and data access** read “Custom Field” via get\_all · resolve a document from “Custom Field” via get\_doc.

**State and service calls** request delete on “Custom Field”.

**Local steps**

- For each tuple(doctype, fields) in custom\_fields.items().
  - Set fieldnames from list().
  - If isinstance(fields, tuple(list, tuple, set)).
    - For each field in fields.
      - If isinstance(field, str).
        - Evaluate fieldnames.append(field).
      - Otherwise.
        - If (isinstance(field, dict) and field.get(“fieldname”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(field, dict) → field.get(“fieldname”).
          - Evaluate fieldnames.append(field at “fieldname”).
  - If not fieldnames.
    - Continue with the next iteration or loop test.
  - Set fieldnames from tuple(set(fieldnames)).
  - If bypass\_hooks.
    - Evaluate Platform.db.delete(“Custom Field”, mapping(“fieldname” → tuple(“in”, fieldnames), “dt” → doctype)).
    - Evaluate Platform.clear\_cache(doctype = doctype).
  - Otherwise.
    - Set custom\_field\_names from Platform.get\_all(“Custom Field”, filters = mapping(“fieldname” → tuple(“in”, fieldnames), “dt” → doctype), pluck = “name”).
    - For each custom\_field\_name in custom\_field\_names.
      - Evaluate Platform.get\_doc(“Custom Field”, custom\_field\_name).delete(ignore\_permissions = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0123.json#L1032) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L795) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L940)

## Record · Custom html block

<a id="op-df5fd38a83478a"></a>
### Custom HTMLBlock.validate

`operation_foundation_desk_record_definitions_custom_hypertext_markup_block_business_behavior_custom_document_markup_block_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_private().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate private](operations-013.md#op-516e4438098d90).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L3780) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L432)

<a id="op-516e4438098d90"></a>
### Custom HTMLBlock.validate private

`operation_foundation_desk_record_definitions_custom_hypertext_markup_block_business_behavior_custom_document_markup_block_validate_private`

**Inputs** self.

**Local steps**

- If not has\_common(Platform.get\_roles(), list(“Administrator”, “System Manager”, “Workspace Manager”)).
  - Set self.private from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L3831) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L433)

<a id="op-7f9d5c46b3c85b"></a>
### Get custom blocks for user

`operation_foundation_desk_record_definitions_custom_hypertext_markup_block_business_behavior_get_custom_blocks_for_user`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** condition\_query.select(customHTMLBlock.name).where((customHTMLBlock.private equals 0 bitwise or (nested operand in the contract.owner equals nested operand in the contract.user bitwise and nested operand i ….run().

**Local steps**

- Evaluate Platform.has\_permission(“Custom HTML Block”, “read”, throw = true).
- Set customHTMLBlock from DocType(“Custom HTML Block”).
- Set condition\_query from Platform.qb.from\_(customHTMLBlock).
- Return condition\_query.select(customHTMLBlock.name).where((customHTMLBlock.private equals 0 bitwise or (nested operand in the contract.owner equals nested operand in the contract.user bitwise and nested operand i ….run().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Custom HTML Block”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L106) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L434)

## Record · Custom sidebar

[Record definition](../../../../data/record-types/custom_sidebar.json)

<a id="op-5790c981461b1b"></a>
### Custom Sidebar.validate

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_module().
- Evaluate self.validate\_unique().
- Evaluate self.validate\_item\_routes().
- Evaluate self.drop\_private\_workspaces().
- Evaluate self.anchor\_the\_items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate module](operations-013.md#op-9d2e78fdd28e9a), [validate unique](operations-013.md#op-68b1831a8f40a2), [validate item routes](operations-013.md#op-cec1da46ab7aca), [drop private workspaces](operations-013.md#op-a3bcc216cc549f), [anchor the items](operations-013.md#op-5186d2a9007c2a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L109) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L446)

<a id="op-9d2e78fdd28e9a"></a>
### Custom Sidebar.validate module

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_validate_module`

**Inputs** self.

**Local steps**

- Evaluate check\_module(self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L4510) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L448)

<a id="op-cec1da46ab7aca"></a>
### Custom Sidebar.validate item routes

`operation_foundation_binding_foundation_desk_doctype_custom_sidebar_custom_sidebar_customsidebar_validate_item_routes`

**Inputs** self.

**Local steps**

- For each item in self.sidebar\_items.
  - Evaluate validate\_item\_route(item).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L213) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L671)

<a id="op-68b1831a8f40a2"></a>
### Custom Sidebar.validate unique

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_validate_unique`

**Inputs** self.

**Record and data access** read self.\_DOCTYPE\_NAME via exists.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “A customization for {0} already exists for this layer.”.format(self.module).

**Local steps**

- Set existing from Platform.db.exists(self.\_DOCTYPE\_NAME, mapping(“module” → self.module, “user” → (self.user or SITE\_LAYER), “name” → list(“!=”, self.name))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.user → SITE\_LAYER.
- If existing.
  - Call the validation error handler Platform.throw(translated “A customization for {0} already exists for this layer.”.format(self.module), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L4566) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L449)

<a id="op-a3bcc216cc549f"></a>
### Custom Sidebar.drop private workspaces

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_drop_private_workspaces`

**Inputs** self.

**Record and data access** read “Workspace” via get\_all.

**Explicit results** no value.

**Local steps**

- Set named from set of row.link\_to for row drawn from self.sidebar\_items where (row.link\_type equals “Workspace” and row.link\_to).
  - Draw row from self.sidebar\_items, keep a combination only if ((row.link\_type equals “Workspace” and row.link\_to)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.link\_type equals “Workspace” → row.link\_to.
- If not named.
  - Return no value.
- Set owners from Platform.get\_all(“Workspace”, filters = mapping(“name” → list(“in”, list(named)), “public” → 0, “for\_user” → list(“is”, “set”)), fields = list(“name”, “for\_user”)).
- Set private from set of row.name for row drawn from owners where row.for\_user differs from self.user.
  - Draw row from owners, keep a combination only if (row.for\_user differs from self.user).
- If private.
  - Evaluate self.set(“sidebar\_items”, list of row for row drawn from self.sidebar\_items where not (row.link\_type equals “Workspace” and row.link\_to belongs to private)).
    - Draw row from self.sidebar\_items, keep a combination only if (not (row.link\_type equals “Workspace” and row.link\_to belongs to private)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.link\_type equals “Workspace” → row.link\_to belongs to private.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L108) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L443)

<a id="op-5186d2a9007c2a"></a>
### Custom Sidebar.anchor the items

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_anchor_the_items`

**Inputs** self.

**Local steps**

- Evaluate self.set(“sidebar\_items”, list of row for row drawn from self.sidebar\_items where (row.added or is\_linked(row) or row.key)).
  - Draw row from self.sidebar\_items, keep a combination only if ((row.added or is\_linked(row) or row.key)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.added → is\_linked(row) → row.key.
- For each row in self.sidebar\_items.
  - If is\_linked(row).
    - Set row.key from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L5175) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L441)

<a id="op-779b74e9fe831e"></a>
### Custom Sidebar.validate links

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_validate_links`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Return no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L5360) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L447)

<a id="op-e5e85fb9ff4dc8"></a>
### Custom Sidebar.on update

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_customization\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear customization cache](operations-013.md#op-6409cd82810a4d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L5396) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L445)

<a id="op-8a739bffc32423"></a>
### Custom Sidebar.on trash

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_customization\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear customization cache](operations-013.md#op-6409cd82810a4d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L5447) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L444)

<a id="op-6409cd82810a4d"></a>
### Custom Sidebar.clear customization cache

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_custom_sidebar_clear_customization_cache`

**Inputs** self.

**Local steps**

- If self.user.
  - Evaluate Platform.cache.hdel(“bootinfo”, self.user).
- Otherwise.
  - Evaluate Platform.cache.delete\_key(“bootinfo”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L5498) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L442)

<a id="op-7c28d98e1eda13"></a>
### Get layers for

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_get_layers_for`

**Inputs** user, modules = no value.

**Declared result** dict at tuple(str, list at “CustomSidebar”).

**Record and data access** read “Custom Sidebar” via get\_all · resolve a document from “Custom Sidebar” via get\_cached\_doc.

**Explicit results** layers.

**Local steps**

- Set filters from mapping(“user” → list(“in”, list(SITE\_LAYER, user))).
- If modules is distinct from no value.
  - Set filters at “module” from list(“in”, modules).
- Set rows from Platform.get\_all(“Custom Sidebar”, filters = filters, fields = list(“name”, “module”, “user”)).
- Evaluate rows.sort(key = deferred anonymous expression).
- Set layers from mapping().
- For each row in rows.
  - Evaluate layers.setdefault(row.module, list()).append(Platform.get\_cached\_doc(“Custom Sidebar”, row.name)).
- Return layers.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Custom Sidebar”, row.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L5606) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L453)

<a id="op-0a026c321e3b46"></a>
### Get customization

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_get_customization`

**Inputs** module, user.

**Declared result** “CustomSidebar \| None”.

**Record and data access** read “Custom Sidebar” via exists · resolve a document from “Custom Sidebar” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“Custom Sidebar”, name) when name, otherwise no value.

**Local steps**

- Set name from Platform.db.exists(“Custom Sidebar”, mapping(“module” → module, “user” → (user or list(“in”, list(empty text, no value))))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → list(“in”, list(empty text, no value)).
- Return Platform.get\_cached\_doc(“Custom Sidebar”, name) when name, otherwise no value.
  - Value choice on name — true gives Platform.get\_cached\_doc(“Custom Sidebar”, name), false gives no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Custom Sidebar”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L6061) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L451)

<a id="op-fbfc2bf5d14d9f"></a>
### Get layers

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_get_layers`

**Inputs** module, user.

**Declared result** list at “CustomSidebar”.

**Explicit results** list of layer for layer drawn from layers where layer.

**Local steps**

- Set layers from list(get\_customization(module, no value)).
- If user.
  - Evaluate layers.append(get\_customization(module, user)).
- Return list of layer for layer drawn from layers where layer.
  - Draw layer from layers, keep a combination only if (layer).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L6274) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1972) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L452)

<a id="op-27558da136e761"></a>
### Check module

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_check_module`

**Inputs** module.

**Declared result** no value.

**Record and data access** read “Module Def” via exists.

**Explicit failure paths** validation helper — translated “{0} is not a module.”.format(module).

**Local steps**

- If not Platform.db.exists(“Module Def”, module).
  - Call the validation error handler Platform.throw(translated “{0} is not a module.”.format(module)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L6461) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L440)

<a id="op-594e59000868df"></a>
### Resolve arrangement

`operation_foundation_desk_record_definitions_custom_sidebar_business_behavior_resolve_arrangement`

**Inputs** items, layers.

**Declared result** tuple at tuple(list at dict, dict at tuple(str, bool)).

**Explicit results** resolve\_layers(items, list of layer.sidebar\_items for layer drawn from layers, key = item\_key, apply\_row = apply\_sidebar\_row).

**Local steps**

- Return resolve\_layers(items, list of layer.sidebar\_items for layer drawn from layers, key = item\_key, apply\_row = apply\_sidebar\_row).
  - Draw layer from layers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L6596) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1987) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L467)
