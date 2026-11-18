# Customer support · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Service level agreement

[Record definition](../../../../data/record-types/service_level_agreement.json)

<a id="op-2186a9afc64849"></a>
### Service Level Agreement.validate status field

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_validate_status_field`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The Document Type {0} must have a Status field to configure Service Level Agreement”.format(Platform.bold(self.document\_type)).

**Local steps**

- Set meta from Platform.get\_meta(self.document\_type).
- If not meta.get\_field(“status”).
  - Call the validation error handler Platform.throw(translated “The Document Type {0} must have a Status field to configure Service Level Agreement”.format(Platform.bold(self.document\_type))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L3873) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L5) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1242)

<a id="op-4846bb2307e6dd"></a>
### Service Level Agreement.validate condition

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_validate_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4050) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L2) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1239)

<a id="op-9a9a621aa2f6a0"></a>
### Service Level Agreement.get service level agreement priority

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_get_service_level_agreement_priority`

**Inputs** self, priority.

**Record and data access** resolve a document from “Service Level Priority” via get\_doc.

**Explicit results** Platform.\_dict(mapping(“priority” → priority.priority, “response\_time” → priority.response\_time, “resolution\_time” → priority.resolution\_time)).

**Local steps**

- Set priority from Platform.get\_doc(“Service Level Priority”, mapping(“priority” → priority, “parent” → self.name)).
- Return Platform.\_dict(mapping(“priority” → priority.priority, “response\_time” → priority.response\_time, “resolution\_time” → priority.resolution\_time)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4256) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1234)

<a id="op-30b4020ed87b46"></a>
### Service Level Agreement.before insert

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_before_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.document\_type equals “Issue”.
  - Return no value.
- Set service\_level\_agreement\_fields from get\_service\_level\_agreement\_fields(self.document\_type).
- Set meta from Platform.get\_meta(self.document\_type, cached = false).
- If meta.custom.
  - Evaluate self.create\_docfields(meta, service\_level\_agreement\_fields).
- Otherwise.
  - Evaluate self.create\_custom\_fields(meta, service\_level\_agreement\_fields).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create docfields](operations-004.md#op-d5c15e5d11c469), [create custom fields](operations-004.md#op-6d053df657a004).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4455) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1228)

<a id="op-bcdd7d237479be"></a>
### Service Level Agreement.on trash

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_on_trash`

**Inputs** self.

**Local steps**

- Evaluate set\_documents\_with\_active\_service\_level\_agreement().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4671) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1235)

<a id="op-18c306def67c18"></a>
### Service Level Agreement.after insert

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_after_insert`

**Inputs** self.

**Local steps**

- Evaluate set\_documents\_with\_active\_service\_level\_agreement().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4718) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1227)

<a id="op-f159678ce5be05"></a>
### Service Level Agreement.on update

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_on_update`

**Inputs** self.

**Local steps**

- Evaluate set\_documents\_with\_active\_service\_level\_agreement().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4765) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1236)

<a id="op-bb7cb12cc2d3df"></a>
### Service Level Agreement.clear cache

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_clear_cache`

**Inputs** self.

**Explicit results** super().clear\_cache().

**Local steps**

- Evaluate get\_sla\_doctypes.clear\_cache().
- Return super().clear\_cache().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4812) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1231)

<a id="op-d5c15e5d11c469"></a>
### Service Level Agreement.create docfields

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_create_record_fields`

**Inputs** self, meta, service\_level\_agreement\_fields.

**Record and data access** resolve a document from mapping(“doctype” → “DocField”, “idx” → last\_index, “parenttype” → “DocType”, “parentfield” → “fields”, …) via get\_doc · resolve a document from “DocType” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “DocField”, “idx” → last\_index, “parenttype” → “DocType”, “parentfield” → “fields”, …)) · call save on Platform.get\_doc(“DocType”, self.document\_type).

**Local steps**

- Set last\_index from len(meta.fields).
- For each field in service\_level\_agreement\_fields.
  - If not meta.has\_field(field.get(“fieldname”)).
    - Update last\_index using + 1.
    - Evaluate Platform.get\_doc(mapping(“doctype” → “DocField”, “idx” → last\_index, “parenttype” → “DocType”, “parentfield” → “fields”, …)).insert(ignore\_permissions = true).
  - Otherwise.
    - Set existing\_field from meta.get\_field(field.get(“fieldname”)).
    - Evaluate self.reset\_field\_properties(existing\_field, “DocField”, field).
- Evaluate Platform.get\_doc(“DocType”, self.document\_type).save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset field properties](operations-004.md#op-1e219b75f0e5d9).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0968.json#L4886) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1233)

<a id="op-6d053df657a004"></a>
### Service Level Agreement.create custom fields

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_create_custom_fields`

**Inputs** self, meta, service\_level\_agreement\_fields.

**Record and data access** resolve a document from mapping(“doctype” → “Custom Field”, “dt” → self.document\_type, “label” → field.get(“label”), “fieldname” → field.get(“fieldname”), …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → self.document\_type, “label” → field.get(“label”), “fieldname” → field.get(“fieldname”), …)).

**Local steps**

- For each field in service\_level\_agreement\_fields.
  - If not meta.has\_field(field.get(“fieldname”)).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → self.document\_type, “label” → field.get(“label”), “fieldname” → field.get(“fieldname”), …)).insert(ignore\_permissions = true).
  - Otherwise.
    - Set existing\_field from meta.get\_field(field.get(“fieldname”)).
    - If existing\_field.get(“is\_custom\_field”).
      - Evaluate self.reset\_field\_properties(existing\_field, “Custom Field”, field).

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset field properties](operations-004.md#op-1e219b75f0e5d9).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1232)

<a id="op-1e219b75f0e5d9"></a>
### Service Level Agreement.reset field properties

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_service_level_agreement_reset_field_properties`

**Inputs** self, field, field\_dt, sla\_field.

**Record and data access** resolve a document from field\_dt via get\_doc.

**State and service calls** call save on field.

**Local steps**

- Set field from Platform.get\_doc(field\_dt, field.name).
- Set field.label from sla\_field.get(“label”).
- Set field.fieldname from sla\_field.get(“fieldname”).
- Set field.fieldtype from sla\_field.get(“fieldtype”).
- Set field.collapsible from sla\_field.get(“collapsible”).
- Set field.hidden from sla\_field.get(“hidden”).
- Set field.options from sla\_field.get(“options”).
- Set field.read\_only from sla\_field.get(“read\_only”).
- Set field.hidden from sla\_field.get(“hidden”).
- Set field.description from sla\_field.get(“description”).
- Set field.default from sla\_field.get(“default”).
- Set field.link\_filters from sla\_field.get(“link\_filters”).
- Evaluate field.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1237)

<a id="op-1671bafdd97dca"></a>
### Check agreement status

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_check_agreement_status`

**Inputs** no declared parameters.

**Record and data access** read “Service Level Agreement” via get\_all · resolve a document from “Service Level Agreement” via get\_doc.

**State and service calls** request set\_value on “Service Level Agreement”.

**Local steps**

- Set service\_level\_agreements from Platform.get\_all(“Service Level Agreement”, filters = mapping(“enabled” → 1), fields = list(“name”)).
- For each service\_level\_agreement in service\_level\_agreements.
  - Set doc from Platform.get\_doc(“Service Level Agreement”, service\_level\_agreement.name).
  - If (doc.end\_date and getdate(doc.end\_date) &lt; getdate(Platform.utils.getdate())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.end\_date → getdate(doc.end\_date) &lt; getdate(Platform.utils.getdate()).
    - Evaluate Platform.db.set\_value(“Service Level Agreement”, service\_level\_agreement.name, “enabled”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1193)

<a id="op-2802be428dd679"></a>
### Get active service level agreement for

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_active_service_level_agreement_for`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doc.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1195)

<a id="op-f7e72dc6f2320d"></a>
### Is valid today

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_is_valid_today`

**Inputs** agreement.

**Declared result** bool.

**Explicit results** ((not agreement.start\_date or getdate(agreement.start\_date) ≤ today) and (not agreement.end\_date or getdate(agreement.end\_date) ≥ today)).

**Local steps**

- Set today from getdate().
- Return ((not agreement.start\_date or getdate(agreement.start\_date) ≤ today) and (not agreement.end\_date or getdate(agreement.end\_date) ≥ today)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not agreement.start\_date or getdate(agreement.start\_date) ≤ today) → (not agreement.end\_date or getdate(agreement.end\_date) ≥ today).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not agreement.start\_date → getdate(agreement.start\_date) ≤ today.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not agreement.end\_date → getdate(agreement.end\_date) ≥ today.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1271)

<a id="op-810f80992e5410"></a>
### Get sla entities

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_get_sla_entities`

**Inputs** customer.

**Declared result** list at str.

**Explicit results** list() · list(customer, expanded get\_customer\_group(customer), expanded get\_customer\_territory(customer)).

**Local steps**

- If not customer.
  - Return list().
- Return list(customer, expanded get\_customer\_group(customer), expanded get\_customer\_territory(customer)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1266)

<a id="op-eabef993f9a977"></a>
### Get selected or first

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_get_selected_or_first`

**Inputs** agreements, selected.

**Explicit results** agreement · agreements at 0 when agreements, otherwise no value.

**Local steps**

- For each agreement in agreements.
  - If agreement.name equals selected.
    - Return agreement.
- Return agreements at 0 when agreements, otherwise no value.
  - Value choice on agreements — true gives agreements at 0, false gives no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1265)

<a id="op-ad0d1e722e7340"></a>
### Get context

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_context`

**Inputs** doc.

**Explicit results** mapping(“doc” → doc.as\_dict(), “nowdate” → nowdate, “Platform” → Platform.\_dict(utils = nested operand in the contract().get(“Platform”).get(“utils”))).

**Local steps**

- Return mapping(“doc” → doc.as\_dict(), “nowdate” → nowdate, “Platform” → Platform.\_dict(utils = nested operand in the contract().get(“Platform”).get(“utils”))).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L1960) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1197)

<a id="op-261b8b8c5c6f99"></a>
### Get customer group

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_customer_group`

**Inputs** customer.

**Record and data access** read “Customer” via get\_value.

**Explicit results** customer\_groups.

**Local steps**

- Set customer\_groups from list().
- Set customer\_group from Platform.db.get\_value(“Customer”, customer, “customer\_group”) when customer, otherwise no value.
  - Value choice on customer — true gives Platform.db.get\_value(“Customer”, customer, “customer\_group”), false gives no value.
- If customer\_group.
  - Set ancestors from get\_ancestors\_of(“Customer Group”, customer\_group).
  - Set customer\_groups from list(customer\_group, expanded ancestors).
- Return customer\_groups.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L2102) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1198)

<a id="op-f6bf482c9f1b06"></a>
### Get customer territory

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_customer_territory`

**Inputs** customer.

**Record and data access** read “Customer” via get\_value.

**Explicit results** customer\_territories.

**Local steps**

- Set customer\_territories from list().
- Set customer\_territory from Platform.db.get\_value(“Customer”, customer, “territory”) when customer, otherwise no value.
  - Value choice on customer — true gives Platform.db.get\_value(“Customer”, customer, “territory”), false gives no value.
- If customer\_territory.
  - Set ancestors from get\_ancestors\_of(“Territory”, customer\_territory).
  - Set customer\_territories from list(customer\_territory, expanded ancestors).
- Return customer\_territories.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L2286) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1199)

<a id="op-f8fac5a08c0a77"></a>
### Get service level agreement filters

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_service_level_agreement_filters`

**Inputs** doctype, name, customer = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Support Settings” via get\_single\_value · read “Service Level Priority” via get\_all · read “Service Level Agreement” via get\_all.

**Explicit results** no value · mapping(“priority” → list of priority.priority for priority drawn from Platform.get\_all(“Service Level Priority”, filters = mapping(“parent” → name), fields = list(“priority”)), “service\_level\_agreements”  ….

**Local steps**

- Evaluate Platform.has\_permission(doctype, “read”, throw = true).
- If not Platform.db.get\_single\_value(“Support Settings”, “track\_service\_level\_agreement”).
  - Return no value.
- Set filters from list(list(“Service Level Agreement”, “document\_type”, “=”, doctype), list(“Service Level Agreement”, “enabled”, “=”, 1)).
- Set or\_filters from list(list(“Service Level Agreement”, “default\_service\_level\_agreement”, “=”, 1)).
- If customer.
  - Evaluate or\_filters.append(list(“Service Level Agreement”, “entity”, “in”, list(empty text, customer, expanded get\_customer\_group(customer), expanded get\_customer\_territory(customer)))).
- Return mapping(“priority” → list of priority.priority for priority drawn from Platform.get\_all(“Service Level Priority”, filters = mapping(“parent” → name), fields = list(“priority”)), “service\_level\_agreements”  ….
  - Draw priority from Platform.get\_all(“Service Level Priority”, filters = mapping(“parent” → name), fields = list(“priority”)).
  - Draw d from Platform.get\_all(“Service Level Agreement”, filters = filters, or\_filters = or\_filters).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, throw = true) · configured or stored value from Platform.db.get\_single\_value(“Support Settings”, “track\_service\_level\_agreement”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1207)

<a id="op-0ca443ec64a137"></a>
### Get repeated

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_repeated`

**Inputs** values.

**Explicit results** one space.join(diff).

**Local steps**

- Set unique\_list from list().
- Set diff from list().
- For each value in values.
  - If value does not belong to unique\_list.
    - Evaluate unique\_list.append(str(value)).
  - Otherwise.
    - If value does not belong to diff.
      - Evaluate diff.append(str(value)).
- Return one space.join(diff).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L3037) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1204)

<a id="op-598f6a3531d2f6"></a>
### Get documents with active service level agreement

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_documents_with_active_service_level_agreement`

**Inputs** no declared parameters.

**Explicit results** set\_documents\_with\_active\_service\_level\_agreement() · sla\_doctypes.

**Local steps**

- Set sla\_doctypes from Platform.cache.get\_value(“doctypes\_with\_active\_sla”).
- If sla\_doctypes is identical to no value.
  - Return set\_documents\_with\_active\_service\_level\_agreement().
- Return sla\_doctypes.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L3246) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1200)

<a id="op-842163d3ce59d3"></a>
### Set documents with active service level agreement

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_set_documents_with_active_service_level_agreement`

**Inputs** no declared parameters.

**Record and data access** read “Service Level Agreement” via get\_all.

**Explicit results** active.

**Local steps**

- Attempt the following.
  - Set active from frozenset(generator of sla.document\_type for sla drawn from Platform.get\_all(“Service Level Agreement”, fields = list(“document\_type”))).
    - Draw sla from Platform.get\_all(“Service Level Agreement”, fields = list(“document\_type”)).
  - Evaluate Platform.cache.set\_value(“doctypes\_with\_active\_sla”, active).
- On failure (tuple(Platform.DoesNotExistError, Platform.db.TableMissingError)).
  - Set active from frozenset().
- Return active.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L3347) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L6) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1243)

<a id="op-30cfe1aea4a53e"></a>
### Apply

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_apply`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- Set flags from Platform.local.flags.
- If (flags.in\_patch or flags.in\_migrate or flags.in\_install or flags.in\_setup\_wizard or doc.doctype does not belong to get\_documents\_with\_active\_service\_level\_agreement() or stays\_resolved(doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flags.in\_patch → flags.in\_migrate → flags.in\_install → flags.in\_setup\_wizard → doc.doctype does not belong to get\_documents\_with\_active\_service\_level\_agreement() → stays\_resolved(doc).
  - Return no value.
- Set sla from get\_active\_service\_level\_agreement\_for(doc).
- If not sla.
  - Evaluate remove\_sla\_if\_applied(doc).
  - Return no value.
- Evaluate process\_sla(doc, sla).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1192)
