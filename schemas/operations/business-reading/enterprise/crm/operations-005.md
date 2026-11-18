# Sales relationships · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Contract

[Record definition](../../../../data/record-types/contract.json)

<a id="op-c232f051c18f35"></a>
### Set lapsed fulfilment status

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_set_lapsed_fulfilment_status`

**Inputs** no declared parameters.

**State and service calls** request set\_value on “Contract”.

**Local steps**

- Evaluate Platform.db.set\_value(“Contract”, mapping(“docstatus” → 1, “requires\_fulfilment” → 1, “fulfilment\_deadline” → tuple(“&lt;”, nowdate()), “fulfilment\_status” → tuple(“not in”, list(“Fulfilled”, “Lapsed”))), “fu ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L494)

<a id="op-b164f618e31956"></a>
### Has permission

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L493)

<a id="op-b11193c12ca72e"></a>
### Get permission query conditions

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L492)

## Record · Contract template

[Record definition](../../../../data/record-types/contract_template.json)

<a id="op-7daddbcf906bb4"></a>
### Contract Template.validate

`operation_enterprise_customer_relationship_management_record_definitions_contract_template_business_behavior_contract_template_validate`

**Inputs** self.

**Local steps**

- If self.contract\_terms.
  - Evaluate validate\_template(self.contract\_terms, restrict\_globals = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L405) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1151)

<a id="op-7ea4c90899a738"></a>
### Get contract template

`operation_enterprise_customer_relationship_management_record_definitions_contract_template_business_behavior_get_contract_template`

**Inputs** template\_name, doc.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Contract Template” via get\_doc.

**Explicit results** mapping(“contract\_template” → contract\_template, “contract\_terms” → contract\_terms).

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- Set contract\_template from Platform.get\_doc(“Contract Template”, template\_name).
- Evaluate contract\_template.check\_permission().
- Set contract\_terms from no value.
- If contract\_template.contract\_terms.
  - Set contract\_terms from render\_contract\_terms(contract\_template.contract\_terms, get\_render\_context(doc)).
- Return mapping(“contract\_template” → contract\_template, “contract\_terms” → contract\_terms).

**Values supplied outside this operation** effective access from contract\_template.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1152)

<a id="op-5f077c8373c4a8"></a>
### Get render context

`operation_enterprise_binding_enterprise_crm_doctype_contract_template_contract_template_get_render_context`

**Inputs** doc.

**Declared result** dict.

**Explicit results** context.

**Local steps**

- Set context from mapping of df.fieldname → empty text for df drawn from Platform.get\_meta((doc.get(“doctype”) or “Contract”)).fields.
  - Draw df from Platform.get\_meta((doc.get(“doctype”) or “Contract”)).fields.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“doctype”) → “Contract”.
- Evaluate context.update(mapping of key → value for tuple(key, value) drawn from doc.items() where value is distinct from no value).
  - Draw tuple(key, value) from doc.items(), keep a combination only if (value is distinct from no value).
- Return context.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L495)

<a id="op-df65955035340d"></a>
### Render contract terms

`operation_enterprise_binding_enterprise_crm_doctype_contract_template_contract_template_render_contract_terms`

**Inputs** terms, context.

**Declared result** str.

**Explicit results** Platform.render\_template(terms, context, restrict\_globals = true).

**Local steps**

- If guess\_is\_path(terms).
  - Update terms using + whitespace '\\n'.
- Return Platform.render\_template(terms, context, restrict\_globals = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L496)

## Record · Crm settings

<a id="op-ff1cea6d6837fa"></a>
### CRMSettings.validate

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate Platform.db.set\_default(“campaign\_naming\_by”, self.get(“campaign\_naming\_by”, empty text)).
- Evaluate self.validate\_default\_valid\_till().
- Evaluate self.validate\_enable\_opportunity\_creation\_from\_contact\_us().
- Evaluate self.validate\_allowed\_users().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate default valid till](operations-005.md#op-d3eaff76054b43), [validate enable opportunity creation from contact us](operations-005.md#op-54c9fabbc326e8), [validate allowed users](operations-005.md#op-f74ace5fd20d8e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1170)

<a id="op-d3eaff76054b43"></a>
### CRMSettings.validate default valid till

`operation_enterprise_binding_enterprise_crm_doctype_crm_settings_crm_settings_crmsettings_validate_default_valid_till`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Default Quotation Validity Days must be a whole number of days, 0 or more.”.

**Local steps**

- If (self.default\_valid\_till and not nested operand in the contract(nested operand in the contract).strip().isdigit()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default\_valid\_till → not str(nested operand in the contract.default\_valid\_till).strip().isdigit().
  - Call the validation error handler Platform.throw(translated “Default Quotation Validity Days must be a whole number of days, 0 or more.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L497)

<a id="op-54c9fabbc326e8"></a>
### CRMSettings.validate enable opportunity creation from contact us

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_validate_enable_opportunity_creation_from_contact_us`

**Inputs** self.

**Record and data access** read “Contact Us Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Cannot enable Opportunity creation from Contact Us because the Contact Us form is disabled.”.

**Local steps**

- Set contact\_disabled from Platform.get\_single\_value(“Contact Us Settings”, “is\_disabled”).
- If (self.enable\_opportunity\_creation\_from\_contact\_us and contact\_disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_opportunity\_creation\_from\_contact\_us → contact\_disabled.
  - Call the validation error handler Platform.throw(translated “Cannot enable Opportunity creation from Contact Us because the Contact Us form is disabled.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Contact Us Settings”, “is\_disabled”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L1543) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1172)

<a id="op-f74ace5fd20d8e"></a>
### CRMSettings.validate allowed users

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_validate_allowed_users`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please add atleast one user on Allowed Users to allow Data Synchronization from Platform CRM site.” · validation helper — translated “Allowed Users is not required as Platform CRM is already installed on the site.”.

**Local steps**

- If (self.enable\_Platform\_crm\_data\_synchronization and not (is\_crm\_installed() or self.allowed\_users)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_Platform\_crm\_data\_synchronization → not (is\_crm\_installed() or self.allowed\_users).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_crm\_installed() → self.allowed\_users.
  - Call the validation error handler Platform.throw(translated “Please add atleast one user on Allowed Users to allow Data Synchronization from Platform CRM site.”).
- If (self.enable\_Platform\_crm\_data\_synchronization and is\_crm\_installed() and self.allowed\_users).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_Platform\_crm\_data\_synchronization → is\_crm\_installed() → self.allowed\_users.
  - Call the validation error handler Platform.throw(translated “Allowed Users is not required as Platform CRM is already installed on the site.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1171)

<a id="op-eb5bb255e3df13"></a>
### CRMSettings.before save

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_allowed\_users().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear allowed users](operations-005.md#op-609e3fcaaff41e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L1883) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1574) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1165)

<a id="op-3e492588d07283"></a>
### CRMSettings.on update

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.custom\_fields\_for\_Platform\_crm\_data\_sync().

If control reaches the end, it returns no value.

**Methods declared on this owner** [custom fields for Platform crm data sync](operations-005.md#op-ee990388b4ad5f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L1934) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1169)

<a id="op-609e3fcaaff41e"></a>
### CRMSettings.clear allowed users

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_clear_allowed_users`

**Inputs** self.

**Local steps**

- If not self.enable\_Platform\_crm\_data\_synchronization.
  - Set self.allowed\_users from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L1985) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1166)

<a id="op-ee990388b4ad5f"></a>
### CRMSettings.custom fields for Platform crm data sync

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_custom_fields_for_foundation_customer_relationship_data_sync`

**Inputs** self.

**Local steps**

- Set custom\_fields from self.get\_Platform\_crm\_custom\_fields().
- If self.enable\_Platform\_crm\_data\_synchronization.
  - Evaluate create\_custom\_fields(custom\_fields, ignore\_validate = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Platform crm custom fields](operations-005.md#op-f2e30960c816cd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L2052) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1167)

<a id="op-f2e30960c816cd"></a>
### CRMSettings.get Platform crm custom fields

`operation_enterprise_customer_relationship_management_record_definitions_customer_relationship_management_settings_business_behavior_customer_relationship_settings_get_foundation_customer_relationship_custom_fields`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** custom\_fields.

**Local steps**

- Set custom\_fields from mapping(“Quotation” → list(mapping(“fieldname” → “crm\_deal”, “fieldtype” → “Data”, “label” → “Platform CRM Deal”, “insert\_after” → “party\_name”)), “Customer” → list(mapping(“fieldname” → “crm\_deal”, “field ….
- Return custom\_fields.

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L2157) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1168)

## Record · Email campaign

[Record definition](../../../../data/record-types/email_campaign.json)

<a id="op-94fd8f41d10a6d"></a>
### Email Campaign.validate

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_email_campaign_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_date().
- Evaluate self.validate\_recipient\_email().
- Evaluate self.validate\_email\_campaign\_already\_exists().
- Evaluate self.update\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set date](operations-005.md#op-d96050d16b0a57), [validate recipient email](operations-005.md#op-53eaa281ca9620), [validate email campaign already exists](operations-006.md#op-cac205f73c3d00), [update status](operations-006.md#op-700da67a29130d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L3117) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1176)

<a id="op-53eaa281ca9620"></a>
### Email Campaign.validate recipient email

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_email_campaign_validate_recipient_email`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.recipient.
  - Return no value.
- If self.email\_campaign\_for equals “Lead”.
  - Evaluate self.validate\_lead().
- Otherwise.
  - If self.email\_campaign\_for equals “Contact”.
    - Evaluate self.validate\_contact().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate lead](operations-005.md#op-a43d910f25ed98), [validate contact](operations-005.md#op-bac456a01d12fe).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L3228) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1180)

<a id="op-d96050d16b0a57"></a>
### Email Campaign.set date

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_email_campaign_set_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Start Date cannot be before the current date” · validation helper — translated “Please set up the Campaign Schedule in the Campaign {0}”.format(self.campaign\_name).

**Local steps**

- Set start\_date\_changed from (self.is\_new() or self.has\_value\_changed(“start\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_value\_changed(“start\_date”).
- If (start\_date\_changed and getdate(self.start\_date) &lt; getdate(today())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date\_changed → getdate(self.start\_date) &lt; getdate(today()).
  - Call the validation error handler Platform.throw(translated “Start Date cannot be before the current date”).
- Set self.end\_date from self.get\_end\_date().
- If not self.end\_date.
  - Call the validation error handler Platform.throw(translated “Please set up the Campaign Schedule in the Campaign {0}”.format(self.campaign\_name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get end date](operations-005.md#op-b82268803d03af).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1174)

<a id="op-b82268803d03af"></a>
### Email Campaign.get end date

`operation_enterprise_binding_enterprise_crm_doctype_email_campaign_email_campaign_emailcampaign_get_end_date`

**Inputs** self.

**Declared result** (date bitwise or no value).

**Record and data access** resolve a document from “Campaign” via get\_cached\_doc.

**Explicit results** add\_days(getdate(self.start\_date), max(send\_after\_days)).

**Local steps**

- Set campaign from Platform.get\_cached\_doc(“Campaign”, self.campaign\_name).
- Set send\_after\_days from list of entry.send\_after\_days for entry drawn from campaign.get(“campaign\_schedules”).
  - Draw entry from campaign.get(“campaign\_schedules”).
- If send\_after\_days.
  - Return add\_days(getdate(self.start\_date), max(send\_after\_days)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Campaign”, self.campaign\_name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L498)

<a id="op-b4638a85866ef8"></a>
### Email Campaign.refresh end date

`operation_enterprise_binding_enterprise_crm_doctype_email_campaign_email_campaign_emailcampaign_refresh_end_date`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set end\_date from self.get\_end\_date().
- If (end\_date and end\_date differs from getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_date → end\_date differs from getdate(self.end\_date).
  - Evaluate self.db\_set(“end\_date”, end\_date, update\_modified = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get end date](operations-005.md#op-b82268803d03af).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L499)

<a id="op-a43d910f25ed98"></a>
### Email Campaign.validate lead

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_email_campaign_validate_lead`

**Inputs** self.

**Record and data access** read “Lead” via get\_value.

**Explicit failure paths** validation helper — translated “Please set an email id for the Lead {0}”.format(lead.lead\_name).

**Local steps**

- Set lead from Platform.db.get\_value(“Lead”, self.recipient, list(“email\_id”, “lead\_name”, “unsubscribed”), as\_dict = true).
- If not lead.email\_id.
  - Call the validation error handler Platform.throw(translated “Please set an email id for the Lead {0}”.format(lead.lead\_name)).
- Evaluate self.validate\_not\_unsubscribed(lead).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate not unsubscribed](operations-005.md#op-d91247f5229c50).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1179)

<a id="op-bac456a01d12fe"></a>
### Email Campaign.validate contact

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_email_campaign_validate_contact`

**Inputs** self.

**Record and data access** read “Contact” via get\_value.

**Explicit failure paths** validation helper — translated “Please set a primary email ID for the Contact {0}”.format(Platform.bold(contact.full\_name)).

**Local steps**

- Set contact from Platform.db.get\_value(“Contact”, self.recipient, list(“email\_id”, “full\_name”, “unsubscribed”), as\_dict = true).
- If (contact and not contact.email\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in contact → not contact.email\_id.
  - Call the validation error handler Platform.throw(translated “Please set a primary email ID for the Contact {0}”.format(Platform.bold(contact.full\_name))).
- Evaluate self.validate\_not\_unsubscribed(contact).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate not unsubscribed](operations-005.md#op-d91247f5229c50).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1177)

<a id="op-d91247f5229c50"></a>
### Email Campaign.validate not unsubscribed

`operation_enterprise_binding_enterprise_crm_doctype_email_campaign_email_campaign_emailcampaign_validate_not_unsubscribed`

**Inputs** self, recipient.

**Explicit failure paths** validation helper — translated “{0} {1} has unsubscribed from emails”.format(translated self.email\_campaign\_for, Platform.bold(self.recipient)).

**Local steps**

- If (self.is\_new() and recipient and recipient.unsubscribed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → recipient → recipient.unsubscribed.
  - Call the validation error handler Platform.throw(translated “{0} {1} has unsubscribed from emails”.format(translated self.email\_campaign\_for, Platform.bold(self.recipient))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L500)
