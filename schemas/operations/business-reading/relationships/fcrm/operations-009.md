# Lead and deal records · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm telephony agent

<a id="op-1bb87cc7b17cdc"></a>
### CRMTelephony Agent.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_telephony_agent_business_behavior_customer_relationship_telephony_agent_validate`

**Inputs** self.

**Local steps**

- Evaluate self.update\_phone\_nos\_based\_on\_mobile\_no().
- Evaluate self.set\_primary().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update phone nos based on mobile no](operations-009.md#op-782d3a5a1901f1), [set primary](operations-009.md#op-b7874259c5720e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L5415) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1151) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1127)

<a id="op-782d3a5a1901f1"></a>
### CRMTelephony Agent.update phone nos based on mobile no

`operation_relationships_fcrm_record_definitions_customer_relationship_management_telephony_agent_business_behavior_customer_relationship_telephony_agent_update_phone_numbers_based_on_mobile_number`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- Set old\_mobile\_no from doc\_before\_save.mobile\_no.
- Set new\_mobile\_no from self.mobile\_no.
- If old\_mobile\_no equals new\_mobile\_no.
  - Return no value.
- If (new\_mobile\_no and not any(generator of nested operand in the contract.get(“number”) equals new\_mobile\_no for phone drawn from self.phone\_nos)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_mobile\_no → not any(generator of phone.get(“number”) equals new\_mobile\_no for phone drawn from self.phone\_nos).
  - Draw phone from self.phone\_nos.
  - Evaluate self.append(“phone\_nos”, mapping(“number” → new\_mobile\_no, “is\_primary” → 1)).
- Set phone\_to\_remove from next(generator of phone for phone drawn from self.phone\_nos where phone.get(“number”) equals old\_mobile\_no, no value).
  - Draw phone from self.phone\_nos, keep a combination only if (phone.get(“number”) equals old\_mobile\_no).
- If phone\_to\_remove.
  - Evaluate self.phone\_nos.remove(phone\_to\_remove).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L5486) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1150) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1126)

<a id="op-b7874259c5720e"></a>
### CRMTelephony Agent.set primary

`operation_relationships_fcrm_record_definitions_customer_relationship_management_telephony_agent_business_behavior_customer_relationship_telephony_agent_set_primary`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only one {0} can be set as primary.”.format(Platform.bold(Platform.unscrub(“mobile\_no”))).

**Local steps**

- If (not self.phone\_nos and not self.mobile\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.phone\_nos → not self.mobile\_no.
  - Return no value.
- If not self.phone\_nos.
  - Evaluate self.append(“phone\_nos”, mapping(“number” → self.mobile\_no, “is\_primary” → 1)).
- Set primary\_numbers from list of phone.get(“number”) for phone drawn from self.phone\_nos where phone.get(“is\_primary”).
  - Draw phone from self.phone\_nos, keep a combination only if (phone.get(“is\_primary”)).
- <a id="op-b7874259c5720e-guard-11"></a>If len(primary\_numbers) &gt; 1.
  - Call the validation error handler Platform.throw(translated “Only one {0} can be set as primary.”.format(Platform.bold(Platform.unscrub(“mobile\_no”)))).
- Set primary from next(generator of d for d drawn from self.phone\_nos where d.get(“is\_primary”) equals 1, no value).
  - Draw d from self.phone\_nos, keep a combination only if (d.get(“is\_primary”) equals 1).
- Set self.mobile\_no from primary.get(“number”) when primary, otherwise empty text.
  - Value choice on primary — true gives primary.get(“number”), false gives empty text.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(primary\_numbers) &gt; 1, length of primary\_numbers = 2 selects the branch that calls the validation-error handler with translated “Only one {0} can be set as primary.”.format(Platform.bold(Platform.unscrub(“mobile\_no”))). With length of primary\_numbers = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b7874259c5720e-guard-11)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L5903) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1149) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1125)

## Record · Crm territory

<a id="op-3422302d53317e"></a>
### CRMTerritory.validate

`operation_relationships_binding_crm_fcrm_doctype_crm_territory_crm_territory_crmterritory_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_parent\_is\_group().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate parent is group](operations-009.md#op-489b6fa3461098).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L198) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L354) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L335)

<a id="op-489b6fa3461098"></a>
### CRMTerritory.validate parent is group

`operation_relationships_binding_crm_fcrm_doctype_crm_territory_crm_territory_crmterritory_validate_parent_is_group`

**Inputs** self.

**Record and data access** read “CRM Territory” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Territory cannot be its own parent” · validation helper — translated “Parent Territory {0} is not a group. Only group territories can have children.”.format(Platform.bold(parent)).

**Local steps**

- Set parent from self.parent\_crm\_territory.
- If not parent.
  - Return no value.
- If parent equals self.name.
  - Call the validation error handler Platform.throw(translated “Territory cannot be its own parent”).
- If not Platform.db.get\_value(“CRM Territory”, parent, “is\_group”).
  - Call the validation error handler Platform.throw(translated “Parent Territory {0} is not a group. Only group territories can have children.”.format(Platform.bold(parent))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L199) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L355) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L336)

<a id="op-fa212d039286c9"></a>
### On doctype update

`operation_relationships_binding_crm_fcrm_doctype_crm_territory_crm_territory_on_doctype_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “CRM Territory”.

**Local steps**

- Evaluate Platform.db.add\_index(“CRM Territory”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L200) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L356) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L337)

## Record · Crm twilio settings

<a id="op-6c7b4ec8fedac5"></a>
### CRMTwilio Settings.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_validate`

**Inputs** self.

**Record and data access** read “CRM Twilio Settings” via get\_single\_value.

**Local steps**

- Set old\_account\_sid from Platform.db.get\_single\_value(“CRM Twilio Settings”, “account\_sid”).
- If self.account\_sid differs from old\_account\_sid.
  - Set self.new\_sid from true.
- Otherwise.
  - Set self.new\_sid from false.
- Evaluate self.validate\_twilio\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate twilio account](operations-009.md#op-103f541616149f).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Twilio Settings”, “account\_sid”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L6412) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1160) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1136)

<a id="op-e44abd4c45eca0"></a>
### CRMTwilio Settings.on update

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.account\_sid.
  - Return no value.
- Set twilio from Client(self.account\_sid, self.get\_password(“auth\_token”)).
- Evaluate self.set\_api\_credentials(twilio).
- Evaluate self.set\_application\_credentials(twilio, self.app\_name).
- Evaluate self.fetch\_applications().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set api credentials](operations-009.md#op-aaa2ec1e56660b), [set application credentials](operations-009.md#op-70ae0756deb524), [fetch applications](operations-009.md#op-a596324145d3fb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L6574) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1157) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1133)

<a id="op-103f541616149f"></a>
### CRMTwilio Settings.validate twilio account

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_validate_twilio_account`

**Inputs** self.

**Explicit results** twilio.

**Explicit failure paths** validation helper — translated “Invalid Account SID or Auth Token.”.

**Local steps**

- Attempt the following.
  - Set twilio from Client(self.account\_sid, self.get\_password(“auth\_token”)).
  - Evaluate twilio.api.accounts(self.account\_sid).fetch().
  - Return twilio.
- On failure (Exception).
  - Call the validation error handler Platform.throw(translated “Invalid Account SID or Auth Token.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L6768) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1161) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1137)

<a id="op-aaa2ec1e56660b"></a>
### CRMTwilio Settings.set api credentials

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_set_application_programming_interface_credentials`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, twilio.

**Explicit result forms** no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L6966) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1159) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1135)

<a id="op-70ae0756deb524"></a>
### CRMTwilio Settings.set application credentials

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_set_application_credentials`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, twilio, app\_name.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1158) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1134)

<a id="op-30037ca3a97655"></a>
### CRMTwilio Settings.create api key

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_create_application_programming_interface_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, twilio.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L242) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1153) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1129)

<a id="op-49c13489169351"></a>
### CRMTwilio Settings.get twilio voice url

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_get_twilio_voice_resource_address`

**Inputs** self.

**Explicit results** get\_public\_url(url\_path).

**Local steps**

- Set url\_path from “/api/method/crm.integrations.twilio.api.voice”.
- Return get\_public\_url(url\_path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L417) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1156) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1132)

<a id="op-040dc2f86088b2"></a>
### CRMTwilio Settings.get application

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_get_application`

**Inputs** self, twilio, friendly\_name = no value.

**Explicit results** applications at 0 · default\_application at 0 · no value.

**Local steps**

- Set friendly\_name from (friendly\_name or self.friendly\_resource\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in friendly\_name → self.friendly\_resource\_name.
- Set applications from twilio.applications.list(friendly\_name).
- Set default\_application from twilio.applications.list(self.friendly\_resource\_name).
- If applications.
  - Return applications at 0.
- If default\_application.
  - Return default\_application at 0.
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L487) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1155) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1131)

<a id="op-11570f71c530d0"></a>
### CRMTwilio Settings.create application

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_create_application`

**Inputs** self, twilio, friendly\_name = no value.

**Explicit results** application.

**Local steps**

- Set friendly\_name from (friendly\_name or self.friendly\_resource\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in friendly\_name → self.friendly\_resource\_name.
- Set application from twilio.applications.create(voice\_method = “POST”, voice\_url = self.get\_twilio\_voice\_url(), friendly\_name = friendly\_name).
- Return application.

**Methods declared on this owner** [get twilio voice url](operations-009.md#op-49c13489169351).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L685) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1152) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1128)

<a id="op-a596324145d3fb"></a>
### CRMTwilio Settings.fetch applications

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_customer_relationship_twilio_settings_fetch_applications`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_single\_value on “CRM Twilio Settings”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Unable to connect to Twilio account to fetch applications.”.

**Local steps**

- Set twilio from self.validate\_twilio\_account().
- If not twilio.
  - Call the validation error handler Platform.throw(translated “Unable to connect to Twilio account to fetch applications.”).
  - Return no value.
- Set applications from list of app.friendly\_name for app drawn from twilio.applications.list().
  - Draw app from twilio.applications.list().
- Evaluate Platform.db.set\_single\_value(“CRM Twilio Settings”, “twilio\_apps”, “,”.join(applications)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate twilio account](operations-009.md#op-103f541616149f).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L837) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1154) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1130)

<a id="op-a86baf2c1f3a16"></a>
### Get public url

`operation_relationships_fcrm_record_definitions_customer_relationship_management_twilio_settings_business_behavior_get_public_resource_address`

**Inputs** path = no value.

**Explicit results** (get\_url().split(“:8”, 1) at 0 + path).

**Local steps**

- Bind dependencies get\_url.
- Return (get\_url().split(“:8”, 1) at 0 + path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L1083) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1162) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1138)

## Record · Crm view settings

<a id="op-754a9f2aeacf55"></a>
### Create

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_create`

**Inputs** view.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “CRM View Settings” · call insert on doc.

**Explicit results** doc.

**Local steps**

- Set view from Platform.\_dict(view).
- Set view.filters from (parse\_json(view.filters) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parse\_json(view.filters) → mapping().
- Set view.columns from parse\_json((view.columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.columns → “&#91;&#93;”.
- Set view.rows from parse\_json((view.rows or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.rows → “&#91;&#93;”.
- Set view.kanban\_columns from parse\_json((view.kanban\_columns or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.kanban\_columns → “&#91;&#93;”.
- Set view.kanban\_fields from parse\_json((view.kanban\_fields or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.kanban\_fields → “&#91;&#93;”.
- Set default\_rows from sync\_default\_rows(view.doctype).
- Set view.rows from (view.rows + default\_rows) when default\_rows, otherwise view.rows.
  - Value choice on default\_rows — true gives (view.rows + default\_rows), false gives view.rows.
- Set view.rows from remove\_duplicates(view.rows).
- If (not view.kanban\_columns and view.type equals “kanban”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not view.kanban\_columns → view.type equals “kanban”.
  - Set view.kanban\_columns from sync\_default\_columns(view).
- Otherwise.
  - If not view.columns.
    - Set view.columns from sync\_default\_columns(view).
- Set doc from Platform.new\_doc(“CRM View Settings”).
- Set doc.name from view.label.
- Set doc.label from view.label.
- Set doc.type from (view.type or “list”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.type → “list”.
- Set doc.icon from view.icon.
- Set doc.dt from view.doctype.
- Set doc.user from Platform.session.user.
- Set doc.route\_name from (view.route\_name or get\_route\_name(view.doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.route\_name → get\_route\_name(view.doctype).
- Set doc.load\_default\_columns from (view.load\_default\_columns or false).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.load\_default\_columns → false.
- Set doc.filters from json.dumps(view.filters).
- Set doc.order\_by from view.order\_by.
- Set doc.group\_by\_field from view.group\_by\_field.
- Set doc.column\_field from view.column\_field.
- Set doc.title\_field from view.title\_field.
- Set doc.kanban\_columns from json.dumps(view.kanban\_columns).
- Set doc.kanban\_fields from json.dumps(view.kanban\_fields).
- Set doc.columns from json.dumps(view.columns).
- Set doc.rows from json.dumps(view.rows).
- Evaluate doc.insert().
- Return doc.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L1189) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1165) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1141)

<a id="op-f416ddaf1a3eee"></a>
### Update

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_update`

**Inputs** view.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM View Settings” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** doc.

**Local steps**

- Set view from Platform.\_dict(view).
- Set filters from parse\_json((view.filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.filters → mapping().
- Set columns from parse\_json((view.columns or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.columns → list().
- Set rows from parse\_json((view.rows or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.rows → list().
- Set kanban\_columns from parse\_json((view.kanban\_columns or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.kanban\_columns → list().
- Set kanban\_fields from parse\_json((view.kanban\_fields or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.kanban\_fields → list().
- Set default\_rows from sync\_default\_rows(view.doctype).
- Set rows from (rows + default\_rows) when default\_rows, otherwise rows.
  - Value choice on default\_rows — true gives (rows + default\_rows), false gives rows.
- Set rows from remove\_duplicates(rows).
- Set doc from Platform.get\_doc(“CRM View Settings”, view.name).
- Evaluate check\_permission(doc).
- Set doc.label from view.label.
- Set doc.type from (view.type or “list”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.type → “list”.
- Set doc.icon from view.icon.
- Set doc.route\_name from (view.route\_name or get\_route\_name(view.doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.route\_name → get\_route\_name(view.doctype).
- Set doc.load\_default\_columns from (view.load\_default\_columns or false).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in view.load\_default\_columns → false.
- Set doc.filters from json.dumps(filters).
- Set doc.order\_by from view.order\_by.
- Set doc.group\_by\_field from view.group\_by\_field.
- Set doc.column\_field from view.column\_field.
- Set doc.title\_field from view.title\_field.
- Set doc.kanban\_columns from json.dumps(kanban\_columns).
- Set doc.kanban\_fields from json.dumps(kanban\_fields).
- Set doc.columns from json.dumps(columns).
- Set doc.rows from json.dumps(rows).
- Evaluate doc.save().
- Return doc.

**Values supplied outside this operation** effective access from check\_permission(doc).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L2274) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1176) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1152)

<a id="op-2b360023766b03"></a>
### Delete

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_delete`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM View Settings” via exists · resolve a document from “CRM View Settings” via get\_doc.

**State and service calls** request delete\_doc for “CRM View Settings”.

**Local steps**

- If Platform.db.exists(“CRM View Settings”, name).
  - Set doc from Platform.get\_doc(“CRM View Settings”, name).
  - Evaluate check\_permission(doc).
  - Evaluate Platform.delete\_doc(“CRM View Settings”, name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from check\_permission(doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L3137) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1167) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1143)

<a id="op-db1fe50e35f5de"></a>
### Public

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_public`

**Inputs** name, value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM View Settings” via get\_doc.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If (Platform.session.user differs from “Administrator” and “Sales Manager” does not belong to Platform.get\_roles()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user differs from “Administrator” → “Sales Manager” does not belong to Platform.get\_roles().
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set doc from Platform.get\_doc(“CRM View Settings”, name).
- If doc.pinned.
  - Set doc.pinned from false.
- Set doc.public from bool(value).
- Set doc.user from empty text when value, otherwise Platform.session.user.
  - Value choice on value — true gives empty text, false gives Platform.session.user.
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L3334) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1171) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1147)

<a id="op-2e0031eed140ef"></a>
### Pin

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_personal_identification_number`

**Inputs** name, value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM View Settings” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set doc from Platform.get\_doc(“CRM View Settings”, name).
- Evaluate check\_permission(doc).
- Set doc.pinned from bool(value).
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from check\_permission(doc).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L3685) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1170) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1146)

<a id="op-4e41859bf8fe80"></a>
### Check permission

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_check_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L3878) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1163) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1139)

<a id="op-2713688fe459b3"></a>
### Remove duplicates

`operation_relationships_fcrm_record_definitions_customer_relationship_management_view_settings_business_behavior_remove_duplicates`

**Inputs** l.

**Explicit results** list(dict.fromkeys(l)).

**Local steps**

- Return list(dict.fromkeys(l)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0045.json#L4129) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1172) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1148)
