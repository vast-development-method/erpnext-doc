# Forms, reports and navigation · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Customize form

[Record definition](../../../../data/record-types/customize_form.json)

<a id="op-55a98050d46882"></a>
### Customize Form.make property setter

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_make_property_setter`

**Inputs** self, prop, value, property\_type, fieldname = no value, apply\_on = no value, row\_name = no value.

**Explicit results** no value.

**Local steps**

- Evaluate delete\_property\_setter(self.doc\_type, prop, fieldname, row\_name).
- Set property\_value from self.get\_existing\_property\_value(prop, fieldname).
- If property\_value equals value.
  - Return no value.
- If not apply\_on.
  - Set apply\_on from “DocField” when fieldname, otherwise “DocType”.
    - Value choice on fieldname — true gives “DocField”, false gives “DocType”.
- Evaluate Platform.make\_property\_setter(mapping(“doctype” → self.doc\_type, “doctype\_or\_field” → apply\_on, “fieldname” → fieldname, “row\_name” → row\_name, …), is\_system\_generated = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get existing property value](operations-017.md#op-62b0d6b4041a6a).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L2773) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L966)

<a id="op-62b0d6b4041a6a"></a>
### Customize Form.get existing property value

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_get_existing_property_value`

**Inputs** self, property\_name, fieldname = no value.

**Record and data access** read “DocField” via get\_value · read “DocType” via get\_value.

**Explicit results** property\_value.

**Local steps**

- If fieldname.
  - Set property\_value from Platform.db.get\_value(“DocField”, mapping(“parent” → self.doc\_type, “fieldname” → fieldname), property\_name).
- Otherwise.
  - If Platform.db.has\_column(“DocType”, property\_name).
    - Set property\_value from Platform.db.get\_value(“DocType”, self.doc\_type, property\_name).
  - Otherwise.
    - Set property\_value from no value.
- Return property\_value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L3154) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L963)

<a id="op-3232a44d6881e5"></a>
### Customize Form.validate fieldtype change

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_validate_fieldtype_change`

**Inputs** self, df, old\_value, new\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Fieldtype cannot be changed from {0} to {1} in row {2}”.format(old\_value, new\_value, df.idx).

**Local steps**

- If df.is\_virtual.
  - Return no value.
- Set allowed from self.allow\_fieldtype\_change(old\_value, new\_value).
- If allowed.
  - Set old\_value\_length from cint(Platform.db.type\_map.get(old\_value) at 1).
  - Set new\_value\_length from cint(Platform.db.type\_map.get(new\_value) at 1).
  - If (new\_value\_length and old\_value\_length &gt; new\_value\_length).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_value\_length → old\_value\_length &gt; new\_value\_length.
    - Evaluate self.check\_length\_for\_fieldtypes.append(mapping(“df” → df, “old\_value” → old\_value)).
    - Evaluate self.validate\_fieldtype\_length().
  - Otherwise.
    - Set self.flags.update\_db from true.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Fieldtype cannot be changed from {0} to {1} in row {2}”.format(old\_value, new\_value, df.idx)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [allow fieldtype change](operations-017.md#op-de458819c1e2d7), [validate fieldtype length](operations-017.md#op-df97c0a32c22f5).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L3404) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L981)

<a id="op-df97c0a32c22f5"></a>
### Customize Form.validate fieldtype length

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_validate_fieldtype_length`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit failure paths** validation helper — translated “Value for field {0} is too long in {1}. Length should be lesser than {2} characters”.format(Platform.bold(label), links\_str, Platform.bold(max\_length)).

**Local steps**

- For each field in self.check\_length\_for\_fieldtypes.
  - Set df from field.get(“df”).
  - Set max\_length from cint(Platform.db.type\_map.get(df.fieldtype) at 1).
  - Set fieldname from df.fieldname.
  - Set docs from Platform.db.sql(formatted text   SELECT name, {fieldname}, LENGTH({fieldname}) AS len  FROM ′tab{self.doc\_type}′  WHERE LENGTH({fieldname}) &gt; {max\_length}  , as\_dict = true).
  - Set label from df.label.
  - Set links\_str from “, ”.join(generator of Platform.utils.get\_link\_to\_form(self.doc\_type, doc.name) for doc drawn from docs).
    - Draw doc from docs.
  - If docs.
    - Call the validation error handler Platform.throw(translated “Value for field {0} is too long in {1}. Length should be lesser than {2} characters”.format(Platform.bold(label), links\_str, Platform.bold(max\_length)), title = translated “Data  ….
- Set self.flags.update\_db from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L3828) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L982)

<a id="op-be729fdec83024"></a>
### Customize Form.reset to defaults

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_reset_to_defaults`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- If not self.doc\_type.
  - Return no value.
- Evaluate reset\_customization(self.doc\_type).
- Evaluate self.fetch\_to\_customize().

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch to customize](operations-016.md#op-3f872e4720ee3f).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L4391) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L969)

<a id="op-0a0e5dc00f480f"></a>
### Customize Form.reset layout

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_reset_layout`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Property Setter” via get\_all.

**State and service calls** request delete on “Property Setter”.

**Explicit results** no value.

**Local steps**

- If not self.doc\_type.
  - Return no value.
- Set property\_setters from Platform.get\_all(“Property Setter”, filters = mapping(“doc\_type” → self.doc\_type, “property” → tuple(“in”, tuple(“field\_order”, “insert\_after”))), pluck = “name”).
- If not property\_setters.
  - Return no value.
- Evaluate Platform.db.delete(“Property Setter”, mapping(“name” → tuple(“in”, property\_setters))).
- Evaluate Platform.clear\_cache(doctype = self.doc\_type).
- Evaluate self.fetch\_to\_customize().

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch to customize](operations-016.md#op-3f872e4720ee3f).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L4508) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L968)

<a id="op-62b470932579ff"></a>
### Customize Form.trim table

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_trim_table`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- If not self.doc\_type.
  - Return no value.
- Evaluate trim\_table(self.doc\_type, dry\_run = false).
- Evaluate self.fetch\_to\_customize().

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch to customize](operations-016.md#op-3f872e4720ee3f).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L4832) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L977)

<a id="op-de458819c1e2d7"></a>
### Customize Form.allow fieldtype change

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_allow_fieldtype_change`

**Inputs** self, old\_type, new\_type.

**Wrappers, in declaration order** classmethod.

**Declared result** bool.

**Explicit results** any(map(in\_field\_group, ALLOWED\_FIELDTYPE\_CHANGE)).

**Local steps**

- Bind local operation in\_field\_group for subsequent calls.
- Return any(map(in\_field\_group, ALLOWED\_FIELDTYPE\_CHANGE)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L4960) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L955)

<a id="op-d2fe66101cd3a2"></a>
### Customize Form.allow fieldtype change.in field group

`operation_foundation_custom_record_definitions_customize_form_business_behavior_customize_form_allow_fieldtype_change_in_field_group`

**Inputs** group.

**Explicit results** (old\_type belongs to group and new\_type belongs to group).

**Local steps**

- Return (old\_type belongs to group and new\_type belongs to group).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_type belongs to group → new\_type belongs to group.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L5115) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L956)

<a id="op-47e6e525182d5b"></a>
### Get orphaned columns

`operation_foundation_custom_record_definitions_customize_form_business_behavior_get_orphaned_columns`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** trim\_table(doctype, dry\_run = true).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Evaluate Platform.db.begin(read\_only = true).
- Return trim\_table(doctype, dry\_run = true).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L5186) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L985)

<a id="op-4d7279ef20fd41"></a>
### Reset customization

`operation_foundation_custom_record_definitions_customize_form_business_behavior_reset_customization`

**Inputs** doctype.

**Record and data access** read “Property Setter” via get\_all · read “Custom Field” via get\_all.

**State and service calls** request delete\_doc for “Property Setter” · request delete\_doc for “Custom Field”.

**Local steps**

- Set setters from Platform.get\_all(“Property Setter”, filters = mapping(“doc\_type” → doctype, “field\_name” → list(“!=”, “naming\_series”), “property” → list(“!=”, “options”), “is\_system\_generated” → false), pluck = “name”).
- For each setter in setters.
  - Evaluate Platform.delete\_doc(“Property Setter”, setter).
- Set custom\_fields from Platform.get\_all(“Custom Field”, filters = mapping(“dt” → doctype, “is\_system\_generated” → false), pluck = “name”).
- For each field in custom\_fields.
  - Evaluate Platform.delete\_doc(“Custom Field”, field).
- Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L5326) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L987)

<a id="op-234fafaa750e8e"></a>
### Is standard or system generated field

`operation_foundation_custom_record_definitions_customize_form_business_behavior_is_standard_or_system_generated_field`

**Inputs** df.

**Explicit results** (not df.get(“is\_custom\_field”) or df.get(“is\_system\_generated”)).

**Local steps**

- Return (not df.get(“is\_custom\_field”) or df.get(“is\_system\_generated”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df.get(“is\_custom\_field”) → df.get(“is\_system\_generated”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L5719) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L986)

<a id="op-c0da10186d8ded"></a>
### Get link filters from doc without customisations

`operation_foundation_custom_record_definitions_customize_form_business_behavior_get_link_filters_from_record_without_customisations`

**Inputs** doctype, fieldname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “DocType” via get\_doc.

**Explicit results** field at 0.link\_filters.

**Local steps**

- Set doc from Platform.get\_doc(“DocType”, doctype).
- Set field from list(filter(deferred anonymous expression, doc.fields)).
- Return field at 0.link\_filters.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0125.json#L5812) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L984)

## Record · Dashboard

[Record definition](../../../../data/record-types/dashboard.json)

<a id="op-44131e96a6c9fa"></a>
### Dashboard.onload

`operation_foundation_binding_foundation_desk_doctype_dashboard_dashboard_dashboard_onload`

**Inputs** self.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not self.has\_insights\_version().
  - Return no value.
- Evaluate self.set\_onload(“dashboards”, Platform.db.get\_single\_value(“System Settings”, “dashboards”)).
- If (self.meta.get\_field(“insights\_dashboard”) and not self.get(“insights\_dashboard”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(“insights\_dashboard”) → not self.get(“insights\_dashboard”).
  - Return no value.
- If should\_show\_insights\_dashboards\_prompt().
  - Evaluate self.set\_onload(“show\_insights\_dashboards\_prompt”, true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has insights version](operations-017.md#op-e7a53434738692).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “dashboards”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L222) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L680)

<a id="op-e7a53434738692"></a>
### Dashboard.has insights version

`operation_foundation_binding_foundation_desk_doctype_dashboard_dashboard_dashboard_has_insights_version`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · (os.path.isfile(path) and bool(Platform.get\_file\_json(path).get(“insights\_dashboard”))).

**Local steps**

- If (not self.is\_standard or not Platform.local.module\_app.get(Platform.scrub((self.module or empty text)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_standard → not Platform.local.module\_app.get(Platform.scrub((self.module or empty text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.module → empty text.
  - Return false.
- Set path from Platform.get\_module\_path(self.module, formatted text {self.module}\_dashboard, self.name, formatted text {self.name}.json).
- Return (os.path.isfile(path) and bool(Platform.get\_file\_json(path).get(“insights\_dashboard”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isfile(path) → bool(Platform.get\_file\_json(path).get(“insights\_dashboard”)).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L221) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L679)

<a id="op-2232c363e6b7d1"></a>
### Dashboard.clear cache

`operation_foundation_desk_record_definitions_dashboard_business_behavior_dashboard_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Bind dependencies clear\_computed\_base\_for.
- Evaluate clear\_computed\_base\_for(self).
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L3250) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L70) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L593)

<a id="op-6a955a94cc6588"></a>
### Dashboard.on update

`operation_foundation_desk_record_definitions_dashboard_business_behavior_dashboard_on_update`

**Inputs** self.

**Local steps**

- If self.is\_default.
  - Set DashBoard from DocType(“Dashboard”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(DashBoard.is\_default, 0).where(DashBoard.name differs from self.name).run().
- If (Platform.conf.developer\_mode and self.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → self.is\_standard.
  - Evaluate export\_to\_files(record\_list = list(list(“Dashboard”, self.name, formatted text {self.module} Dashboard)), record\_module = self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L3335) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L71) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L594)

<a id="op-568c3b1fc1b186"></a>
### Dashboard.validate

`operation_foundation_desk_record_definitions_dashboard_business_behavior_dashboard_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot edit Standard Dashboards” · validation helper — message.

**Local steps**

- If (not Platform.conf.developer\_mode and self.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → self.is\_standard.
  - Call the validation error handler Platform.throw(translated “Cannot edit Standard Dashboards”).
- If self.is\_standard.
  - Set non\_standard\_docs\_map from mapping(“Dashboard Chart” → get\_non\_standard\_charts\_in\_dashboard(self), “Number Card” → get\_non\_standard\_cards\_in\_dashboard(self)).
  - If (non\_standard\_docs\_map at “Dashboard Chart” or non\_standard\_docs\_map at “Number Card”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in non\_standard\_docs\_map at “Dashboard Chart” → non\_standard\_docs\_map at “Number Card”.
    - Set message from get\_non\_standard\_warning\_message(non\_standard\_docs\_map).
    - Call the validation error handler Platform.throw(message, title = translated “Standard Not Set”, is\_minimizable = true).
- Evaluate self.validate\_custom\_options().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate custom options](operations-017.md#op-f2bed8e337c0d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L3637) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L72) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L595)

<a id="op-f2bed8e337c0d1"></a>
### Dashboard.validate custom options

`operation_foundation_desk_record_definitions_dashboard_business_behavior_dashboard_validate_custom_options`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Invalid json added in the custom options: {0}”.format(str(error)).

**Local steps**

- If self.chart\_options.
  - Attempt the following.
    - Evaluate json.loads(self.chart\_options).
  - On failure (ValueError) bound to error.
    - Call the validation error handler Platform.throw(translated “Invalid json added in the custom options: {0}”.format(str(error))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L3980) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L73) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L596)

<a id="op-596e59d3aaa57e"></a>
### Should show insights dashboards prompt

`operation_foundation_binding_foundation_desk_doctype_dashboard_dashboard_should_show_insights_dashboards_prompt`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · “System Manager” belongs to Platform.get\_roles().

**Local steps**

- If cint(Platform.defaults.get\_global\_default(SKIP\_INSIGHTS\_DASHBOARDS\_PROMPT)).
  - Return false.
- Return “System Manager” belongs to Platform.get\_roles().

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L223) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L681)

<a id="op-eaf51bf0c65e4c"></a>
### Submit insights dashboards prompt

`operation_foundation_binding_foundation_desk_doctype_dashboard_dashboard_submit_insights_dashboards_prompt`

**Inputs** action.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** no value.

**Record and data access** read “System Settings” via get\_single.

**State and service calls** call save on settings.

**Explicit failure paths** validation helper — translated “Invalid action”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If action equals Action.OPEN\_INSIGHTS\_DASHBOARDS.value.
  - Set settings from Platform.get\_single(“System Settings”).
  - Set settings.dashboards from “Insights”.
  - Evaluate settings.save(ignore\_permissions = true).
- Otherwise.
  - If action differs from Action.KEEP\_CLASSIC\_DASHBOARDS.value.
    - Call the validation error handler Platform.throw(translated “Invalid action”).
- Evaluate Platform.defaults.set\_global\_default(SKIP\_INSIGHTS\_DASHBOARDS\_PROMPT, 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L224) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L706) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L682)

<a id="op-bb42c884435449"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_dashboard_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** effective access lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L4140) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L78) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L601)

<a id="op-d9074b5fe3ece6"></a>
### Get permitted charts

`operation_foundation_desk_record_definitions_dashboard_business_behavior_get_permitted_charts`

**Inputs** dashboard\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Dashboard” via get\_doc.

**Explicit results** permitted\_charts.

**Local steps**

- Set permitted\_charts from list().
- Set dashboard from Platform.get\_doc(“Dashboard”, dashboard\_name).
- For each chart in dashboard.charts.
  - Attempt the following.
    - If Platform.has\_permission(“Dashboard Chart”, doc = chart.chart).
      - Set chart\_dict from Platform.\_dict().
      - Evaluate chart\_dict.update(chart.as\_dict()).
      - If dashboard.get(“chart\_options”).
        - Set chart\_dict.custom\_options from dashboard.get(“chart\_options”).
      - Evaluate permitted\_charts.append(chart\_dict).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
    - Evaluate Platform.log\_error(formatted text Dashboard Chart '{chart.chart}' not found or its source DocType is missing).
- Return permitted\_charts.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Dashboard Chart”, doc = chart.chart).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L4448) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L80) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L603)

<a id="op-f5387897fa72a8"></a>
### Get permitted cards

`operation_foundation_desk_record_definitions_dashboard_business_behavior_get_permitted_cards`

**Inputs** dashboard\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Dashboard” via get\_doc.

**Explicit results** permitted\_cards.

**Local steps**

- Set permitted\_cards from list().
- Set dashboard from Platform.get\_doc(“Dashboard”, dashboard\_name).
- For each card in dashboard.cards.
  - Attempt the following.
    - If Platform.has\_permission(“Number Card”, doc = card.card).
      - Evaluate permitted\_cards.append(card).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.log\_error(formatted text Number Card '{card.card}' not found or its source DocType is missing).
- Return permitted\_cards.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Number Card”, doc = card.card).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0162.json#L4868) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L79) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L602)
