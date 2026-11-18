# Lead and deal records · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm deal

<a id="op-2bd7cedb6e4efd"></a>
### Create contact

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_create_contact`

**Inputs** doc.

**State and service calls** request new\_doc for “Contact” · call insert on contact.

**Explicit results** existing\_contact · contact.name.

**Local steps**

- Set existing\_contact from contact\_exists(doc).
- If existing\_contact.
  - Return existing\_contact.
- Set contact from Platform.new\_doc(“Contact”).
- Evaluate contact.update(mapping(“first\_name” → doc.get(“first\_name”), “last\_name” → doc.get(“last\_name”), “salutation” → doc.get(“salutation”), “company\_name” → (doc.get(“organization”) or doc.get(“organization\_name”)), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“organization”) → doc.get(“organization\_name”).
- If doc.get(“email”).
  - Evaluate contact.append(“email\_ids”, mapping(“email\_id” → doc.get(“email”), “is\_primary” → 1)).
- If doc.get(“mobile\_no”).
  - Evaluate contact.append(“phone\_nos”, mapping(“phone” → doc.get(“mobile\_no”), “is\_primary\_mobile\_no” → 1)).
- Evaluate contact.insert(ignore\_permissions = true).
- Evaluate contact.reload().
- Return contact.name.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L3902) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L791) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L772)

<a id="op-f1d7f3b200d6f1"></a>
### Create deal

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_create_deal`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Organization” via exists.

**State and service calls** request new\_doc for “CRM Deal” · call insert on deal.

**Explicit results** deal.name.

**Local steps**

- Evaluate Platform.has\_permission(“CRM Deal”, “create”, throw = true).
- Set deal from Platform.new\_doc(“CRM Deal”).
- Set contact from doc.get(“contact”).
- If (not contact and (doc.get(“first\_name”) or doc.get(“last\_name”) or doc.get(“email”) or doc.get(“mobile\_no”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not contact → (doc.get(“first\_name”) or doc.get(“last\_name”) or doc.get(“email”) or doc.get(“mobile\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“first\_name”) → doc.get(“last\_name”) → doc.get(“email”) → doc.get(“mobile\_no”).
  - Set contact from contact\_exists(doc).
  - If not contact.
    - Evaluate Platform.has\_permission(“Contact”, “create”, throw = true).
    - Set contact from create\_contact(doc).
- Set organization from doc.get(“organization”).
- If (not organization and doc.get(“organization\_name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not organization → doc.get(“organization\_name”).
  - Set organization from Platform.db.exists(“CRM Organization”, mapping(“organization\_name” → doc.get(“organization\_name”))).
  - If not organization.
    - Evaluate Platform.has\_permission(“CRM Organization”, “create”, throw = true).
    - Set organization from create\_organization(doc).
- Evaluate deal.update(mapping(“organization” → organization, “contacts” → list(mapping(“contact” → contact, “is\_primary” → 1)) when contact, otherwise list())).
  - Value choice on contact — true gives list(mapping(“contact” → contact, “is\_primary” → 1)), false gives list().
- Evaluate doc.pop(“organization”, no value).
- Evaluate deal.update(doc).
- Evaluate deal.insert(ignore\_permissions = true).
- Return deal.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Deal”, “create”, throw = true), Platform.has\_permission(“Contact”, “create”, throw = true) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L13) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L792) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L773)

## Record · Crm exotel settings

<a id="op-c61f1b8d48a447"></a>
### CRMExotel Settings.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_exotel_settings_business_behavior_customer_relationship_exotel_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.verify\_credentials().

If control reaches the end, it returns no value.

**Methods declared on this owner** [verify credentials](operations-003.md#op-042ea05e47b81b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0033.json#L3507) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L851) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L831)

<a id="op-042ea05e47b81b"></a>
### CRMExotel Settings.verify credentials

`operation_relationships_fcrm_record_definitions_customer_relationship_management_exotel_settings_business_behavior_customer_relationship_exotel_settings_verify_credentials`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0033.json#L3558) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L852) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L832)

## Record · Crm fields layout

<a id="op-a73e71bf97e778"></a>
### Get fields layout

`operation_relationships_fcrm_record_definitions_customer_relationship_management_fields_layout_business_behavior_get_fields_layout`

**Inputs** doctype, type, parent\_doctype = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Fields Layout” via exists · resolve a document from “CRM Fields Layout” via get\_doc.

**Explicit results** (tabs or list()).

**Local steps**

- Set tabs from list().
- Set layout from no value.
- If Platform.db.exists(“CRM Fields Layout”, mapping(“dt” → doctype, “type” → type)).
  - Set layout from Platform.get\_doc(“CRM Fields Layout”, mapping(“dt” → doctype, “type” → type)).
- If (layout and layout.layout).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in layout → layout.layout.
  - Set tabs from json.loads(layout.layout).
- If (not tabs and type differs from “Required Fields”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not tabs → type differs from “Required Fields”.
  - Set tabs from get\_default\_layout(doctype).
- Set has\_tabs from false.
- If (isinstance(tabs, list) and len(tabs) &gt; 0 and isinstance(tabs at 0, dict)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(tabs, list) → len(tabs) &gt; 0 → isinstance(tabs at 0, dict).
  - Set has\_tabs from any(generator of “sections” belongs to tab for tab drawn from tabs).
    - Draw tab from tabs.
- If not has\_tabs.
  - Set tabs from list(mapping(“name” → “first\_tab”, “sections” → tabs)).
- Set allowed\_fields from list().
- For each tab in tabs.
  - For each section in tab.get(“sections”).
    - If “columns” does not belong to section.
      - Continue with the next iteration or loop test.
    - For each column in section.get(“columns”).
      - If not column.get(“fields”).
        - Continue with the next iteration or loop test.
      - Evaluate allowed\_fields.extend(column.get(“fields”)).
- Set fields from Platform.get\_meta(doctype).fields.
- Set fields from list of field for field drawn from fields where field.fieldname belongs to allowed\_fields.
  - Draw field from fields, keep a combination only if (field.fieldname belongs to allowed\_fields).
- Set required\_fields from list().
- If type equals “Required Fields”.
  - Set required\_fields from list of field for field drawn from Platform.get\_meta(doctype, false).fields where (field.reqd and not field.default).
    - Draw field from Platform.get\_meta(doctype, false).fields, keep a combination only if ((field.reqd and not field.default)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.reqd → not field.default.
- For each tab in tabs.
  - For each section in tab.get(“sections”).
    - If section.get(“columns”).
      - Set section at “columns” from list of column for column drawn from section.get(“columns”) where column.
        - Draw column from section.get(“columns”), keep a combination only if (column).
    - For each column in section.get(“columns”) when section.get(“columns”), otherwise list().
      - Value choice on section.get(“columns”) — true gives section.get(“columns”), false gives list().
      - Set column at “fields” from list of field for field drawn from column.get(“fields”) where field.
        - Draw field from column.get(“fields”), keep a combination only if (field).
      - For each field in column.get(“fields”) when column.get(“fields”), otherwise list().
        - Value choice on column.get(“fields”) — true gives column.get(“fields”), false gives list().
        - Set field from next(generator of f for f drawn from fields where f.fieldname equals field, no value).
          - Draw f from fields, keep a combination only if (f.fieldname equals field).
        - If field.
          - Set field from field.as\_dict().
          - Evaluate handle\_perm\_level\_restrictions(field, doctype, parent\_doctype).
          - Set column at “fields” at column.get(“fields”).index(field at “fieldname”) from field.
          - If (type equals “Required Fields” and field.reqd and any(generator of f.get(“fieldname”) equals field.get(“fieldname”) for f drawn from required\_fields)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in type equals “Required Fields” → field.reqd → any(generator of f.get(“fieldname”) equals field.get(“fieldname”) for f drawn from required\_fields).
            - Draw f from required\_fields.
            - Set required\_fields from list of f for f drawn from required\_fields where f.get(“fieldname”) differs from field.get(“fieldname”).
              - Draw f from required\_fields, keep a combination only if (f.get(“fieldname”) differs from field.get(“fieldname”)).
- If (type equals “Required Fields” and required\_fields and tabs).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in type equals “Required Fields” → required\_fields → tabs.
  - Evaluate tabs at negative 1.get(“sections”).append(mapping(“label” → “Required Fields”, “name” → (“required\_fields\_section\_” + str(random\_string(4))), “opened” → true, “hideLabel” → true, …)).
    - Draw field from required\_fields.
- Return (tabs or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tabs → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0033.json#L3828) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L855) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L835)

<a id="op-45be6a03298fbc"></a>
### Get sidepanel sections

`operation_relationships_fcrm_record_definitions_customer_relationship_management_fields_layout_business_behavior_get_sidepanel_sections`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Fields Layout” via exists · resolve a document from “CRM Fields Layout” via get\_doc.

**Explicit results** list() · layout.

**Local steps**

- If not Platform.db.exists(“CRM Fields Layout”, mapping(“dt” → doctype, “type” → “Side Panel”)).
  - Return list().
- Set layout from Platform.get\_doc(“CRM Fields Layout”, mapping(“dt” → doctype, “type” → “Side Panel”)).layout.
- If not layout.
  - Return list().
- Set layout from json.loads(layout).
- Set not\_allowed\_fieldtypes from list(“Tab Break”, “Section Break”, “Column Break”).
- Set fields from Platform.get\_meta(doctype).fields.
- Set fields from list of field for field drawn from fields where field.fieldtype does not belong to not\_allowed\_fieldtypes.
  - Draw field from fields, keep a combination only if (field.fieldtype does not belong to not\_allowed\_fieldtypes).
- For each section in layout.
  - Set section at “name” from (section.get(“name”) or section.get(“label”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“name”) → section.get(“label”).
  - For each column in section.get(“columns”) when section.get(“columns”), otherwise list().
    - Value choice on section.get(“columns”) — true gives section.get(“columns”), false gives list().
    - For each field in column.get(“fields”) when column.get(“fields”), otherwise list().
      - Value choice on column.get(“fields”) — true gives column.get(“fields”), false gives list().
      - Set field\_obj from next(generator of f for f drawn from fields where f.fieldname equals field, no value).
        - Draw f from fields, keep a combination only if (f.fieldname equals field).
      - If field\_obj.
        - Set field\_obj from field\_obj.as\_dict().
        - Evaluate handle\_perm\_level\_restrictions(field\_obj, doctype).
        - Set column at “fields” at column.get(“fields”).index(field) from get\_field\_obj(field\_obj).
- Set fields\_meta from mapping().
- For each field in fields.
  - Set fields\_meta at field.fieldname from field.
- Return layout.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0033.json#L5901) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L857) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L837)

<a id="op-0c2f44d9b47afa"></a>
### Handle perm level restrictions

`operation_relationships_fcrm_record_definitions_customer_relationship_management_fields_layout_business_behavior_handle_permission_level_restrictions`

**Inputs** field, doctype, parent\_doctype = no value.

**Explicit results** no value.

**Local steps**

- If field.permlevel equals 0.
  - Return no value.
- Set field\_has\_write\_access from field.permlevel belongs to get\_permlevel\_access(“write”, doctype, parent\_doctype).
- Set field\_has\_read\_access from field.permlevel belongs to get\_permlevel\_access(“read”, doctype, parent\_doctype).
- If (not field\_has\_write\_access and field\_has\_read\_access).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not field\_has\_write\_access → field\_has\_read\_access.
  - Set field.read\_only from 1.
- If (not field\_has\_read\_access and not field\_has\_write\_access).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not field\_has\_read\_access → not field\_has\_write\_access.
  - Set field.hidden from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0033.json#L6766) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L858) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L838)

<a id="op-8e74608dbc0c9a"></a>
### Get permlevel access

`operation_relationships_fcrm_record_definitions_customer_relationship_management_fields_layout_business_behavior_get_permission_level_access`

**Inputs** permission\_type = “write”, doctype = no value, parent\_doctype = no value.

**Explicit results** list(1, 0) · allowed\_permlevels.

**Local steps**

- Set allowed\_permlevels from list().
- Set roles from Platform.get\_roles().
- Set meta from Platform.get\_meta(doctype).
- If (meta.istable and parent\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.istable → parent\_doctype.
  - Set meta from Platform.get\_meta(parent\_doctype).
- Otherwise.
  - If (meta.istable and not parent\_doctype).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.istable → not parent\_doctype.
    - Return list(1, 0).
- For each perm in meta.permissions.
  - If (perm.role belongs to roles and perm.get(permission\_type) and perm.permlevel does not belong to allowed\_permlevels).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in perm.role belongs to roles → perm.get(permission\_type) → perm.permlevel does not belong to allowed\_permlevels.
    - Evaluate allowed\_permlevels.append(perm.permlevel).
- Return allowed\_permlevels.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L856) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L836)

<a id="op-cd0cc3c53f5f03"></a>
### Get field obj

`operation_relationships_fcrm_record_definitions_customer_relationship_management_fields_layout_business_behavior_get_field_obj`

**Inputs** field.

**Explicit results** field.

**Local steps**

- Set field at “placeholder” from (field.get(“placeholder”) or ((“Add ” + field.label) + “...”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“placeholder”) → ((“Add ” + field.label) + “...”).
- If field.fieldtype equals “Link”.
  - Set field at “placeholder” from (field.get(“placeholder”) or ((“Select ” + field.label) + “...”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“placeholder”) → ((“Select ” + field.label) + “...”).
- Otherwise.
  - If (field.fieldtype equals “Select” and field.options).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Select” → field.options.
    - Set field at “placeholder” from (field.get(“placeholder”) or ((“Select ” + field.label) + “...”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“placeholder”) → ((“Select ” + field.label) + “...”).
    - Set field at “options” from list of mapping(“label” → translated option, “value” → option) for option drawn from field.options.split(whitespace '\\n').
      - Draw option from field.options.split(whitespace '\\n').
- If field.read\_only.
  - Set field at “tooltip” from “This field is read only and cannot be edited.”.
- Return field.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L14) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L854) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L834)

<a id="op-5bb9ae165b4d79"></a>
### Save fields layout

`operation_relationships_fcrm_record_definitions_customer_relationship_management_fields_layout_business_behavior_save_fields_layout`

**Inputs** doctype, type, layout.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Fields Layout” via exists · resolve a document from “CRM Fields Layout” via get\_doc.

**State and service calls** request new\_doc for “CRM Fields Layout” · call save on doc.

**Explicit results** doc.layout.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted to modify fields layout”.

**Local steps**

- If not Platform.has\_permission(“CRM Fields Layout”, “write”).
  - Call the validation error handler Platform.throw(translated “Not permitted to modify fields layout”, Platform.PermissionError).
- If Platform.db.exists(“CRM Fields Layout”, mapping(“dt” → doctype, “type” → type)).
  - Set doc from Platform.get\_doc(“CRM Fields Layout”, mapping(“dt” → doctype, “type” → type)).
- Otherwise.
  - Set doc from Platform.new\_doc(“CRM Fields Layout”).
- Evaluate doc.update(mapping(“dt” → doctype, “type” → type, “layout” → layout)).
- Evaluate doc.save().
- Return doc.layout.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Fields Layout”, “write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L822) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L859) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L839)

<a id="op-1918640344bd48"></a>
### Get default layout

`operation_relationships_fcrm_record_definitions_customer_relationship_management_fields_layout_business_behavior_get_default_layout`

**Inputs** doctype.

**Explicit results** tabs.

**Local steps**

- Set fields from Platform.get\_meta(doctype).fields.
- Set tabs from list().
- If (fields and fields at 0.fieldtype differs from “Tab Break”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → fields at 0.fieldtype differs from “Tab Break”.
  - Set sections from list().
  - If (fields and fields at 0.fieldtype differs from “Section Break”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → fields at 0.fieldtype differs from “Section Break”.
    - Evaluate sections.append(mapping(“name” → (“section\_” + str(random\_string(4))), “columns” → list(mapping(“name” → (“column\_” + str(nested operand in the contract(nested operand in the contract))), “fields” → list())))).
  - Evaluate tabs.append(mapping(“name” → (“tab\_” + str(random\_string(4))), “sections” → sections)).
- For each field in fields.
  - If field.fieldtype equals “Tab Break”.
    - Evaluate tabs.append(mapping(“name” → (“tab\_” + str(random\_string(4))), “sections” → list(mapping(“name” → (“section\_” + str(nested operand in the contract(nested operand in the contract))), “columns” → list(mappin ….
  - Otherwise.
    - If field.fieldtype equals “Section Break”.
      - Evaluate tabs at negative 1 at “sections”.append(mapping(“name” → (“section\_” + str(random\_string(4))), “columns” → list(mapping(“name” → (“column\_” + str(nested operand in the contract(nested operand in the contra ….
    - Otherwise.
      - If field.fieldtype equals “Column Break”.
        - Evaluate tabs at negative nested operand in the contract at “sections” at negative 1 at “columns”.append(mapping(“name” → (“column\_” + str(random\_string(4))), “fields” → list())).
      - Otherwise.
        - Evaluate nested operand in the contract at nested operand in the contract at negative nested operand in the contract at “columns” at negative 1 at “fields”.append(field.fieldname).
- Return tabs.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L1273) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L853) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L833)

## Record · Crm form script

<a id="op-fdf464710216f5"></a>
### CRMForm Script.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_form_script_business_behavior_customer_relationship_form_script_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You need to be in developer mode to edit a Standard Form Script”.

**Local steps**

- Set in\_user\_env from not (Platform.flags.in\_install or Platform.flags.in\_patch or Platform.flags.in\_test or Platform.flags.in\_fixtures).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_patch → Platform.flags.in\_test → Platform.flags.in\_fixtures.
- If (in\_user\_env and not self.is\_new() and self.is\_standard and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in in\_user\_env → not self.is\_new() → self.is\_standard → not Platform.conf.developer\_mode.
  - If self.has\_value\_changed(“enabled”).
    - Set enabled\_value from self.enabled.
    - Evaluate self.reload().
    - Set self.enabled from enabled\_value.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “You need to be in developer mode to edit a Standard Form Script”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L2417) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L860) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L840)

<a id="op-4b59e25c4e929f"></a>
### Get form script

`operation_relationships_fcrm_record_definitions_customer_relationship_management_form_script_business_behavior_get_form_script`

**Inputs** dt, view = “Form”.

**Explicit results** list of d.script for d drawn from doc when len(doc) &gt; 1, otherwise doc at 0.script · no value.

**Local steps**

- Set FormScript from Platform.qb.DocType(“CRM Form Script”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.dt equals dt).where(FormScript.view equals view).where(FormScript.enabled equals 1).
- Set doc from query.run(as\_dict = true).
- If doc.
  - Return list of d.script for d drawn from doc when len(doc) &gt; 1, otherwise doc at 0.script.
    - Value choice on len(doc) &gt; 1 — true gives list of d.script for d drawn from doc, false gives doc at 0.script.
    - Draw d from doc.
- Otherwise.
  - Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L2698) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L861) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L841)

## Record · Crm holiday list

<a id="op-1b4093e083d39b"></a>
### CRMHoliday List.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_holiday_list_business_behavior_customer_relationship_holiday_list_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_days().
- Set self.total\_holidays from len(self.holidays).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate days](operations-003.md#op-4e53a05da952b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L3052) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L864) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L844)

<a id="op-d8e6e4234b50be"></a>
### CRMHoliday List.get weekly off dates

`operation_relationships_fcrm_record_definitions_customer_relationship_management_holiday_list_business_behavior_customer_relationship_holiday_list_get_weekly_off_dates`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.validate\_values().
- Set date\_list from self.get\_weekly\_off\_date\_list(self.from\_date, self.to\_date).
- Set last\_idx from max((list of cint(d.idx) for d drawn from self.get(“holidays”) or list(0))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of cint(d.idx) for d drawn from self.get(“holidays”) → list(0).
  - Draw d from self.get(“holidays”).
- For each tuple(i, d) in enumerate(date\_list).
  - Set ch from self.append(“holidays”, mapping()).
  - Set ch.description from translated self.weekly\_off.
  - Set ch.date from d.
  - Set ch.weekly\_off from 1.
  - Set ch.idx from ((last\_idx + i) + 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate values](operations-003.md#op-aef396513fa7d2), [get weekly off date list](operations-003.md#op-8e7ea6c07ccd53).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L3137) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L863) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L843)

<a id="op-aef396513fa7d2"></a>
### CRMHoliday List.validate values

`operation_relationships_fcrm_record_definitions_customer_relationship_management_holiday_list_business_behavior_customer_relationship_holiday_list_validate_values`

**Inputs** self.

**Local steps**

- If not self.weekly\_off.
  - Evaluate throw(translated “Please select weekly off day”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L3527) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L866) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L846)

<a id="op-4e53a05da952b4"></a>
### CRMHoliday List.validate days

`operation_relationships_fcrm_record_definitions_customer_relationship_management_holiday_list_business_behavior_customer_relationship_holiday_list_validate_days`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The holiday on {0} is not between From Date and To Date”.format(formatdate(day.date)).

**Local steps**

- If getdate(self.from\_date) &gt; getdate(self.to\_date).
  - Evaluate throw(translated “To Date cannot be before From Date”).
- For each day in self.get(“holidays”).
  - If not getdate(self.from\_date) ≤ getdate(day.date) ≤ getdate(self.to\_date).
    - Compare adjacent operands in order, stopping at the first false comparison in getdate(self.from\_date) ≤ getdate(day.date) ≤ getdate(self.to\_date).
    - Call the validation error handler Platform.throw(translated “The holiday on {0} is not between From Date and To Date”.format(formatdate(day.date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L3611) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L865) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L845)

<a id="op-8e7ea6c07ccd53"></a>
### CRMHoliday List.get weekly off date list

`operation_relationships_fcrm_record_definitions_customer_relationship_management_holiday_list_business_behavior_customer_relationship_holiday_list_get_weekly_off_date_list`

**Inputs** self, start\_date, end\_date.

**Explicit results** date\_list.

**Local steps**

- Set tuple(start\_date, end\_date) from tuple(getdate(start\_date), getdate(end\_date)).
- Bind dependencies calendar.
- Bind dependencies timedelta.
- Bind dependencies relativedelta.
- Set date\_list from list().
- Set existing\_date\_list from list().
- Set weekday from getattr(calendar, self.weekly\_off.upper()).
- Set reference\_date from (start\_date + relativedelta.relativedelta(weekday = weekday)).
- Set existing\_date\_list from list of getdate(holiday.date) for holiday drawn from self.get(“holidays”).
  - Draw holiday from self.get(“holidays”).
- While reference\_date ≤ end\_date.
  - If reference\_date does not belong to existing\_date\_list.
    - Evaluate date\_list.append(reference\_date).
  - Update reference\_date using + timedelta(days = 7).
- Return date\_list.

**Values supplied outside this operation** selected callable from getattr(calendar, self.weekly\_off.upper()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L3924) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L862) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L842)

## Record · Crm invitation

<a id="op-ee47257fa08119"></a>
### CRMInvitation.before insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_customer_relationship_invitation_before_insert`

**Inputs** self.

**Local steps**

- Evaluate Platform.utils.validate\_email\_address(self.email, true).
- Evaluate self.validate\_existing\_user().
- Set self.key from Platform.generate\_hash(length = 12).
- Set self.invited\_by from Platform.session.user.
- Set self.status from “Pending”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate existing user](operations-004.md#op-6f94eded2a5920).

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 12).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L16) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L870) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L850)

<a id="op-7dc112f8d66586"></a>
### CRMInvitation.after insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_customer_relationship_invitation_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.invite\_via\_email().

If control reaches the end, it returns no value.

**Methods declared on this owner** [invite via email](operations-003.md#op-dfee50f213fdee).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L4493) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L869) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L849)

<a id="op-dfee50f213fdee"></a>
### CRMInvitation.invite via email

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_customer_relationship_invitation_invite_via_email`

**Inputs** self.

**State and service calls** sendmail · call db\_set on self.

**Local steps**

- Set invite\_link from Platform.utils.get\_url(formatted text /api/method/crm.api.accept\_invitation?key={self.key}).
- If Platform.local.dev\_server.
  - Evaluate print(formatted text Invite link for {self.email}: {invite\_link}).
- Set title from “Platform CRM”.
- Set template from “crm\_invitation”.
- Evaluate Platform.sendmail(recipients = self.email, subject = formatted text You have been invited to join {title}, template = template, args = mapping(“title” → title, “invite\_link” → invite\_link), …).
- Evaluate self.db\_set(“email\_sent\_at”, Platform.utils.now()).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = self.email, subject = formatted text You have been invited to join {title}, template = template, args = mapping(“title” → title, “invite\_link” → invite\_link), …) · clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L4544) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L872) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L852)

<a id="op-a325a29eaa1579"></a>
### CRMInvitation.accept invitation

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_customer_relationship_invitation_accept_invitation`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “User” via get\_doc.

**Local steps**

- Evaluate Platform.only\_for(list(“System Manager”, “Sales Manager”), true).
- If self.accept().
  - Evaluate Platform.get\_doc(“User”, self.email).send\_welcome\_mail\_to\_user().

If control reaches the end, it returns no value.

**Methods declared on this owner** [accept](operations-003.md#op-67f744e98fc9ee).

**Values supplied outside this operation** effective access from Platform.only\_for(list(“System Manager”, “Sales Manager”), true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L4895) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L868) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L848)

<a id="op-67f744e98fc9ee"></a>
### CRMInvitation.accept

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_customer_relationship_invitation_accept`

**Inputs** self.

**State and service calls** call save on user · call save on self.

**Explicit results** is\_new\_user.

**Explicit failure paths** validation helper — translated “Invalid or expired key”.

**Local steps**

- <a id="op-67f744e98fc9ee-guard-2"></a>If self.status differs from “Pending”.
  - Call the validation error handler Platform.throw(translated “Invalid or expired key”).
- Set tuple(user, is\_new\_user) from self.create\_user\_if\_not\_exists().
- If not is\_new\_user.
  - Evaluate validate\_no\_role\_profile(user).
- Evaluate user.append\_roles(self.role).
- If self.role equals “System Manager”.
  - Evaluate user.append\_roles(“Sales Manager”, “Sales User”).
- Otherwise.
  - If self.role equals “Sales Manager”.
    - Evaluate user.append\_roles(“Sales User”).
- If self.role equals “Sales User”.
  - Evaluate self.update\_module\_in\_user(user, “FCRM”).
- Evaluate user.save(ignore\_permissions = true).
- Set self.status from “Accepted”.
- Set self.accepted\_at from Platform.utils.now().
- Set self.key from no value.
- Evaluate self.save(ignore\_permissions = true).
- Return is\_new\_user.

**Derived branch illustrations**

- At the comparison self.status differs from “Pending”, self.status = “Accepted” selects the branch that calls the validation-error handler with translated “Invalid or expired key”. With self.status = “Pending”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-67f744e98fc9ee-guard-2)

**Methods declared on this owner** [create user if not exists](operations-004.md#op-e8849401ea33b3), [update module in user](operations-003.md#op-6e24ffb11ac619).

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L15) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L867) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L847)

<a id="op-6e24ffb11ac619"></a>
### CRMInvitation.update module in user

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_customer_relationship_invitation_update_module_in_user`

**Inputs** self, user, module.

**Record and data access** read “Module Def” via get\_all.

**Local steps**

- Set block\_modules from Platform.get\_all(“Module Def”, fields = list(“name as module”), filters = mapping(“name” → list(“!=”, module))).
- If block\_modules.
  - Evaluate user.set(“block\_modules”, block\_modules).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L5498) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L873) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L853)
