# Lead and deal records · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm lead

<a id="op-f97593a476fbae"></a>
### CRMLead.apply sla

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_apply_service_level_agreement`

**Inputs** self.

**Record and data access** read “CRM Service Level Agreement” via get\_last\_doc.

**Explicit results** no value.

**Local steps**

- If not self.sla.
  - Return no value.
- Set sla from Platform.get\_last\_doc(“CRM Service Level Agreement”, mapping(“name” → self.sla)).
- If sla.
  - Evaluate sla.apply(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L1122) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L891) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L871)

<a id="op-a65aa475b76e63"></a>
### CRMLead.convert to deal

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_convert_to_deal`

**Inputs** self, deal = no value.

**Explicit results** convert\_to\_deal(lead = self.name, doc = self, deal = deal).

**Local steps**

- Return convert\_to\_deal(lead = self.name, doc = self, deal = deal).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L1269) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L897) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L877)

<a id="op-77228e8ff682f8"></a>
### CRMLead.get non filterable fields

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_get_non_filterable_fields`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list(“converted”).

**Local steps**

- Return list(“converted”).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L1363) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L904) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L884)

<a id="op-f5578873beb72f"></a>
### CRMLead.default list data

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “Full Name”, “type” → “Data”, “key” → “lead\_name”, “width” → “12rem”), mapping(“label” → “Organization”, “type” → “Link”, “key” → “organization”, “options” → “CRM Organization”, …),  ….
- Set rows from list(“name”, “lead\_name”, “organization”, “status”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L1407) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L903) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L883)

<a id="op-0b4a5574c8b0bb"></a>
### CRMLead.default kanban settings

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_default_kanban_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“column\_field” → “status”, “title\_field” → “lead\_name”, “kanban\_fields” → “&#91;"organization", "email", "mobile\_no", "\_assign", "modified"&#93;”).

**Local steps**

- Return mapping(“column\_field” → “status”, “title\_field” → “lead\_name”, “kanban\_fields” → “&#91;"organization", "email", "mobile\_no", "\_assign", "modified"&#93;”).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L2187) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L902) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L882)

<a id="op-876ca9bbff41c1"></a>
### Convert to deal

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_convert_to_deal`

**Inputs** lead, doc = no value, deal = no value, existing\_contact = no value, existing\_organization = no value, if\_converted = “Create”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Lead Status” via get\_cached\_value.

**Explicit results** settle\_converted(lead, existing, if\_converted) · new\_deal.

**Explicit failure paths** validation helper — translated “Cannot convert a lead with status {0}”.format(lead.status).

**Local steps**

- Evaluate validate\_conversion\_access(lead, doc).
- Set lead from lock\_lead(lead).
- Set existing from existing\_deal(lead.name).
- If (existing and if\_converted differs from “Create”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing → if\_converted differs from “Create”.
  - Return settle\_converted(lead, existing, if\_converted).
- If Platform.get\_cached\_value(“CRM Lead Status”, lead.status, “type”) equals “Lost”.
  - Call the validation error handler Platform.throw(translated “Cannot convert a lead with status {0}”.format(lead.status)).
- Set contact from lead.create\_contact(existing\_contact, false).
- Set organization from lead.create\_organization(existing\_organization).
- Set new\_deal from lead.create\_deal(contact, organization, deal).
- Evaluate mark\_converted(lead).
- Evaluate emit\_lead\_converted(lead, new\_deal, contact, organization).
- Return new\_deal.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“CRM Lead Status”, lead.status, “type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L17) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L889) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L869)

<a id="op-1f44ea42c77b1f"></a>
### Validate conversion access

`operation_relationships_binding_crm_fcrm_doctype_crm_lead_crm_lead_validate_conversion_access`

**Inputs** lead, doc = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not allowed to convert Lead to Deal”.

**Local steps**

- If (doc and doc.flags.get(“ignore\_permissions”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.flags.get(“ignore\_permissions”).
  - Return no value.
- If not Platform.has\_permission(“CRM Lead”, “write”, lead).
  - Call the validation error handler Platform.throw(translated “Not allowed to convert Lead to Deal”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Lead”, “write”, lead).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L197) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L353) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L334)

<a id="op-0cc82adef40309"></a>
### Lock lead

`operation_relationships_binding_crm_fcrm_doctype_crm_lead_crm_lead_lock_lead`

**Inputs** lead.

**Record and data access** resolve a document from “CRM Lead” via get\_doc.

**Explicit results** Platform.get\_doc(“CRM Lead”, lead).

**Local steps**

- Set table from Platform.qb.DocType(“CRM Lead”).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name equals lead).for\_update().run().
- Return Platform.get\_doc(“CRM Lead”, lead).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L194) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L350) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L331)

<a id="op-2dcca253659e5b"></a>
### Existing deal

`operation_relationships_binding_crm_fcrm_doctype_crm_lead_crm_lead_existing_deal`

**Inputs** lead.

**Declared result** (str bitwise or no value).

**Record and data access** read “CRM Deal” via get\_value.

**Explicit results** Platform.db.get\_value(“CRM Deal”, mapping(“lead” → lead), “name”).

**Local steps**

- Return Platform.db.get\_value(“CRM Deal”, mapping(“lead” → lead), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L193) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L349) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L330)

<a id="op-bb6ca9b214119a"></a>
### Settle converted

`operation_relationships_binding_crm_fcrm_doctype_crm_lead_crm_lead_settle_converted`

**Inputs** lead, deal, if\_converted.

**Declared result** str.

**Explicit results** deal.

**Explicit failure paths** validation helper — translated “Lead {0} is already converted to Deal {1}”.format(lead.name, deal).

**Local steps**

- If if\_converted equals “Fail”.
  - Call the validation error handler Platform.throw(translated “Lead {0} is already converted to Deal {1}”.format(lead.name, deal)).
- Return deal.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L196) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L352) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L333)

<a id="op-fbba8744b6ed70"></a>
### Mark converted

`operation_relationships_binding_crm_fcrm_doctype_crm_lead_crm_lead_mark_converted`

**Inputs** lead.

**Record and data access** read “CRM Lead Status” via exists · read “CRM Communication Status” via exists.

**State and service calls** call db\_set on lead.

**Local steps**

- If Platform.db.exists(“CRM Lead Status”, “Qualified”).
  - Evaluate lead.db\_set(“status”, “Qualified”).
- Evaluate lead.db\_set(“converted”, 1).
- If (lead.sla and Platform.db.exists(“CRM Communication Status”, “Replied”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lead.sla → Platform.db.exists(“CRM Communication Status”, “Replied”).
  - Evaluate lead.db\_set(“communication\_status”, “Replied”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L195) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L351) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L332)

<a id="op-3bfdf0a14d7e3b"></a>
### Get deal fieldname

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_get_deal_fieldname`

**Inputs** field, deal\_meta.

**Explicit results** mapped\_fieldname when deal\_meta.has\_field(mapped\_fieldname), otherwise no value · field.fieldname · no value · get\_matching\_custom\_deal\_field(field, deal\_meta).

**Local steps**

- Set mapped\_fieldname from LEAD\_DEAL\_FIELD\_MAP.get(field.fieldname).
- If mapped\_fieldname.
  - Return mapped\_fieldname when deal\_meta.has\_field(mapped\_fieldname), otherwise no value.
    - Value choice on deal\_meta.has\_field(mapped\_fieldname) — true gives mapped\_fieldname, false gives no value.
- If deal\_meta.has\_field(field.fieldname).
  - Return field.fieldname.
- If not is\_custom\_field(field).
  - Return no value.
- Return get\_matching\_custom\_deal\_field(field, deal\_meta).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L2907) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L915) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L895)

<a id="op-02b29fb6d0bd7c"></a>
### Get matching custom deal field

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_get_matching_custom_deal_field`

**Inputs** field, deal\_meta.

**Explicit results** matches at 0 when len(matches) equals 1, otherwise no value.

**Local steps**

- Set matches from list of deal\_field.fieldname for deal\_field drawn from deal\_meta.fields where is\_matching\_custom\_field(field, deal\_field).
  - Draw deal\_field from deal\_meta.fields, keep a combination only if (is\_matching\_custom\_field(field, deal\_field)).
- Return matches at 0 when len(matches) equals 1, otherwise no value.
  - Value choice on len(matches) equals 1 — true gives matches at 0, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L3121) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L916) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L896)

<a id="op-bc393af2c763a1"></a>
### Is matching custom field

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_is_matching_custom_field`

**Inputs** lead\_field, deal\_field.

**Explicit results** (is\_custom\_field(deal\_field) and lead\_field.label equals deal\_field.label and lead\_field.fieldtype equals deal\_field.fieldtype).

**Local steps**

- Return (is\_custom\_field(deal\_field) and lead\_field.label equals deal\_field.label and lead\_field.fieldtype equals deal\_field.fieldtype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_custom\_field(deal\_field) → lead\_field.label equals deal\_field.label → lead\_field.fieldtype equals deal\_field.fieldtype.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L3270) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L918) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L898)

<a id="op-667b6421ce7f96"></a>
### Is custom field

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_is_custom_field`

**Inputs** field.

**Explicit results** bool((field.get(“is\_custom\_field”) or field.get(“custom”) or (field.fieldname or empty text).startswith(“custom\_”) or field.name equals formatted text {field.parent}-{field.fieldname})).

**Local steps**

- Return bool((field.get(“is\_custom\_field”) or field.get(“custom”) or (field.fieldname or empty text).startswith(“custom\_”) or field.name equals formatted text {field.parent}-{field.fieldname})).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.get(“is\_custom\_field”) → field.get(“custom”) → (field.fieldname or empty text).startswith(“custom\_”) → field.name equals formatted text {field.parent}-{field.fieldname}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.fieldname → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L3383) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L917) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L897)

## Record · Crm notification

<a id="op-a25f45737e8998"></a>
### CRMNotification.on update

`operation_relationships_fcrm_record_definitions_customer_relationship_management_notification_business_behavior_customer_relationship_notification_on_update`

**Inputs** self.

**State and service calls** publish realtime with “crm\_notification”.

**Local steps**

- If self.to\_user.
  - Evaluate Platform.publish\_realtime(“crm\_notification”, user = self.to\_user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“crm\_notification”, user = self.to\_user).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0037.json#L5963) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L949) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L927)

<a id="op-fc21d83c47642f"></a>
### Get permission query conditions

`operation_relationships_fcrm_record_definitions_customer_relationship_management_notification_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0037.json#L6045) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L950) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L928)

<a id="op-c8d57cd38a00f1"></a>
### Has permission

`operation_relationships_fcrm_record_definitions_customer_relationship_management_notification_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true, a comparison result.

**Observed service boundaries** effective access lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0037.json#L6227) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L951) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L929)

<a id="op-51a18e8b46db37"></a>
### Notify user

`operation_relationships_fcrm_record_definitions_customer_relationship_management_notification_business_behavior_notify_user`

**Inputs** notification.

**Record and data access** read “CRM Notification” via exists · resolve a document from values via get\_doc.

**State and service calls** call insert on Platform.get\_doc(values).

**Explicit results** no value.

**Local steps**

- Set notification from Platform.\_dict(notification).
- If notification.owner equals notification.assigned\_to.
  - Return no value.
- Set values from Platform.\_dict(doctype = “CRM Notification”, from\_user = notification.owner, to\_user = notification.assigned\_to, type = notification.notification\_type, …).
- If Platform.db.exists(“CRM Notification”, values).
  - Return no value.
- Evaluate Platform.get\_doc(values).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0037.json#L6458) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L952) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L930)

## Record · Crm organization

<a id="op-bfc1ad18a6ea9d"></a>
### CRMOrganization.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_organization_business_behavior_customer_relationship_organization_validate`

**Inputs** self.

**Local steps**

- Evaluate self.update\_exchange\_rate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update exchange rate](operations-005.md#op-2f8ee06b321763).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L339) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L965) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L943)

<a id="op-f12632b6dba8c9"></a>
### CRMOrganization.after insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_organization_business_behavior_customer_relationship_organization_after_insert`

**Inputs** self.

**Local steps**

- Bind dependencies auto\_enrich\_on\_create.
- Evaluate auto\_enrich\_on\_create(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L390) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L962) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L940)

<a id="op-2f8ee06b321763"></a>
### CRMOrganization.update exchange rate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_organization_business_behavior_customer_relationship_organization_update_exchange_rate`

**Inputs** self.

**Record and data access** read “FCRM Settings” via get\_single\_value.

**State and service calls** call db\_set on self.

**Local steps**

- If (self.has\_value\_changed(“currency”) or not self.exchange\_rate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“currency”) → not self.exchange\_rate.
  - Set system\_currency from (Platform.db.get\_single\_value(“FCRM Settings”, “currency”) or “USD”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“FCRM Settings”, “currency”) → “USD”.
  - Set exchange\_rate from 1.
  - If (self.currency and self.currency differs from system\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency → self.currency differs from system\_currency.
    - Set exchange\_rate from get\_exchange\_rate(self.currency, system\_currency).
  - Evaluate self.db\_set(“exchange\_rate”, exchange\_rate).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L450) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L964) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L942)

<a id="op-c9bd575d0c59b4"></a>
### CRMOrganization.default list data

`operation_relationships_fcrm_record_definitions_customer_relationship_management_organization_business_behavior_customer_relationship_organization_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “Organization”, “type” → “Data”, “key” → “organization\_name”, “width” → “16rem”), mapping(“label” → “Website”, “type” → “Data”, “key” → “website”, “width” → “14rem”), mapping(“label” ….
- Set rows from list(“name”, “organization\_name”, “organization\_logo”, “website”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L708) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L963) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L941)

## Record · Crm product

<a id="op-230af320a3f129"></a>
### CRMProduct.before insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_product_business_behavior_customer_relationship_product_before_insert`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Enterprise integration is active. Create an Item in Enterprise and it will appear in CRM Product automatically.”.

**Local steps**

- If self.flags.get(“ignore\_Enterprise\_sync”).
  - Return no value.
- If should\_push\_to\_Enterprise().
  - Call the validation error handler Platform.throw(translated “Enterprise integration is active. Create an Item in Enterprise and it will appear in CRM Product automatically.”, title = translated “Use Enterprise to Create Products”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0038.json#L1484) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L969) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L945)
