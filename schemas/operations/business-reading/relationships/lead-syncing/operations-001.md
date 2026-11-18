# Lead synchronization · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Background sync

<a id="op-b75c6e40440391"></a>
### Sync leads from all enabled sources

`operation_relationships_lead_syncing_background_sync_business_behavior_sync_leads_from_all_enabled_sources`

**Inputs** frequency = no value.

**Declared result** no value.

**Record and data access** read “Lead Sync Source” via get\_all · resolve a document from “Lead Sync Source” via get\_cached\_doc.

**Local steps**

- Set enabled\_sources from Platform.get\_all(“Lead Sync Source”, filters = mapping(“enabled” → 1, “background\_sync\_frequency” → frequency), pluck = “name”).
- For each source in enabled\_sources.
  - Set lead\_sync\_source from Platform.get\_cached\_doc(“Lead Sync Source”, source).
  - Attempt the following.
    - Evaluate lead\_sync\_source.\_sync\_leads().
  - On failure (Exception) bound to \_.
    - Evaluate Platform.log\_error(formatted text Error syncing leads for source {source}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Lead Sync Source”, source).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4068) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1383) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1359)

<a id="op-8064b0adf6b778"></a>
### Sync leads from sources 5 minutes

`operation_relationships_lead_syncing_background_sync_business_behavior_sync_leads_from_sources_5_minutes`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate sync\_leads\_from\_all\_enabled\_sources(“Every 5 Minutes”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4339) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1386) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1362)

<a id="op-f5c2712f3d3236"></a>
### Sync leads from sources 10 minutes

`operation_relationships_lead_syncing_background_sync_business_behavior_sync_leads_from_sources_10_minutes`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate sync\_leads\_from\_all\_enabled\_sources(“Every 10 Minutes”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4383) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1384) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1360)

<a id="op-8cbb486e75cd36"></a>
### Sync leads from sources 15 minutes

`operation_relationships_lead_syncing_background_sync_business_behavior_sync_leads_from_sources_15_minutes`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate sync\_leads\_from\_all\_enabled\_sources(“Every 15 Minutes”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4427) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1385) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1361)

<a id="op-8ffe6c6ed80c77"></a>
### Sync leads from sources hourly

`operation_relationships_lead_syncing_background_sync_business_behavior_sync_leads_from_sources_hourly`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate sync\_leads\_from\_all\_enabled\_sources(“Hourly”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4471) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1388) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1364)

<a id="op-3c556b606ad5d0"></a>
### Sync leads from sources daily

`operation_relationships_lead_syncing_background_sync_business_behavior_sync_leads_from_sources_daily`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate sync\_leads\_from\_all\_enabled\_sources(“Daily”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4515) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1387) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1363)

<a id="op-8e684ad8537726"></a>
### Sync leads from sources monthly

`operation_relationships_lead_syncing_background_sync_business_behavior_sync_leads_from_sources_monthly`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate sync\_leads\_from\_all\_enabled\_sources(“Monthly”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4559) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1389) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1365)

## Record · Facebook lead form

[Record definition](../../../../data/record-types/facebook_lead_form.json)

<a id="op-2802f6c81d3a14"></a>
### Facebook Lead Form.validate

`operation_relationships_lead_syncing_record_definitions_facebook_lead_form_business_behavior_facebook_lead_form_validate`

**Inputs** self.

**Local steps**

- Evaluate self.check\_mandatory\_crm\_fields\_mapped().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check mandatory crm fields mapped](operations-001.md#op-ce1277699c9a85).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4603) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1391) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1367)

<a id="op-ce1277699c9a85"></a>
### Facebook Lead Form.check mandatory crm fields mapped

`operation_relationships_lead_syncing_record_definitions_facebook_lead_form_business_behavior_facebook_lead_form_check_mandatory_customer_relationship_fields_mapped`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — Platform.\_(“Mandatory field(s) {0} must be mapped”).format(formatted\_fields\_list).

**Local steps**

- Set mandatory\_crm\_lead\_fields from list(mapping(“label” → “First Name”, “fieldname” → “first\_name”)).
- Set mandatory\_crm\_lead\_fieldnames from set(generator of f at “fieldname” for f drawn from mandatory\_crm\_lead\_fields).
  - Draw f from mandatory\_crm\_lead\_fields.
- If self.is\_new().
  - Return no value.
- Set mapped\_fields from set(generator of q.mapped\_to\_crm\_field for q drawn from self.questions).
  - Draw q from self.questions.
- Set not\_mapped from list(mandatory\_crm\_lead\_fieldnames.difference(mapped\_fields)).
- If not\_mapped.
  - Set not\_mapped\_labels from list of f at “label” for f drawn from mandatory\_crm\_lead\_fields where f at “fieldname” belongs to not\_mapped.
    - Draw f from mandatory\_crm\_lead\_fields, keep a combination only if (f at “fieldname” belongs to not\_mapped).
  - Set formatted\_fields\_list from Platform.bold(comma\_and(not\_mapped\_labels)).
  - Call the validation error handler Platform.throw(Platform.\_(“Mandatory field(s) {0} must be mapped”).format(formatted\_fields\_list)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L4654) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1390) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1366)

## Record · Failed lead sync log

[Record definition](../../../../data/record-types/failed_lead_sync_log.json)

<a id="op-0d1f6d974d0d93"></a>
### Failed Lead Sync Log.retry sync

`operation_relationships_lead_syncing_record_definitions_failed_lead_sync_log_business_behavior_failed_lead_sync_log_retry_sync`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Lead Sync Source” via get\_cached\_doc.

**State and service calls** call save on self.

**Explicit results** crm\_lead.

**Explicit failure paths** validation helper — Platform.\_(“Can't retry sync for this without source!”) · validation helper — Platform.\_(“Not implemented yet!”).

**Local steps**

- If not self.source.
  - Call the validation error handler Platform.throw(Platform.\_(“Can't retry sync for this without source!”)).
- Set source from Platform.get\_cached\_doc(“Lead Sync Source”, self.source).
- If source.type differs from “Facebook”.
  - Call the validation error handler Platform.throw(Platform.\_(“Not implemented yet!”)).
- Set crm\_lead from FacebookSyncSource(source.get\_password(“access\_token”), source.facebook\_lead\_form).sync\_single\_lead(Platform.parse\_json(self.lead\_data), raise\_exception = true).
- Set self.type from “Synced”.
- Evaluate self.save().
- Return crm\_lead.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Lead Sync Source”, self.source).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L5103) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1392) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1368)

## Record · Lead sync source

[Record definition](../../../../data/record-types/lead_sync_source.json)

<a id="op-08d2d6222fe3e8"></a>
### Get fb graph api url

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_get_fb_graph_application_programming_interface_resource_address`

**Inputs** endpoint.

**Declared result** str.

**Explicit results** formatted text {FB\_GRAPH\_API\_BASE}/{FB\_GRAPH\_API\_VERSION}/{endpoint}.

**Local steps**

- If endpoint.startswith(“/”).
  - Set endpoint from endpoint at slice 1 to no value.
- Return formatted text {FB\_GRAPH\_API\_BASE}/{FB\_GRAPH\_API\_VERSION}/{endpoint}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L5465) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1414) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1390)

<a id="op-ef20c9cac5f0b3"></a>
### Facebook Sync Source.initialize

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_initialize`

**Inputs** self, access\_token, form\_id, source\_name = no value.

**Local steps**

- Set self.access\_token from access\_token.
- Set self.form\_id from form\_id.
- Set self.source\_name from source\_name.
- Set self.form\_questions\_mapping from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L5607) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1405) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1381)

<a id="op-0995cb80d097bd"></a>
### Facebook Sync Source.get api url

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_get_application_programming_interface_resource_address`

**Inputs** self, endpoint.

**Declared result** str.

**Explicit results** get\_fb\_graph\_api\_url(endpoint).

**Local steps**

- Return get\_fb\_graph\_api\_url(endpoint).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L5751) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1402) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1378)

<a id="op-c2bb523ee17a36"></a>
### Facebook Sync Source.sync

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_sync`

**Inputs** self.

**Local steps**

- Set started\_at from now\_datetime().
- Set leads from self.fetch\_leads().
- For each lead in leads.
  - Evaluate self.sync\_single\_lead(lead).
- Evaluate self.update\_last\_synced\_at(started\_at).

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch leads](operations-001.md#op-b6b3239415b8b7), [sync single lead](operations-001.md#op-ac831c9a4dda5a), [update last synced at](operations-001.md#op-9f67f1922478c0).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L33) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1407) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1383)

<a id="op-ac831c9a4dda5a"></a>
### Facebook Sync Source.sync single lead

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_sync_single_lead`

**Inputs** self, lead, raise\_exception = false.

**Record and data access** read “CRM Lead” via exists · resolve a document from mapping(“doctype” → “CRM Lead”, expand crm\_lead\_data) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Lead”, expand crm\_lead\_data)).

**Explicit results** no value · Platform.get\_doc(mapping(“doctype” → “CRM Lead”, expand crm\_lead\_data)).insert(ignore\_permissions = true).

**Explicit failure paths** propagate active failure.

**Local steps**

- If Platform.db.exists(“CRM Lead”, mapping(“facebook\_lead\_id” → lead at “id”)).
  - Return no value.
- Set question\_to\_field\_map from self.get\_form\_questions\_mapping().
- Set lead\_data from mapping of item at “name” → item at “values” at 0 for item drawn from lead at “field\_data” where item.get(“values”).
  - Draw item from lead at “field\_data”, keep a combination only if (item.get(“values”)).
- Set crm\_lead\_data from mapping of question\_to\_field\_map.get(k) → v for tuple(k, v) drawn from lead\_data.items() where k belongs to question\_to\_field\_map.
  - Draw tuple(k, v) from lead\_data.items(), keep a combination only if (k belongs to question\_to\_field\_map).
- Set crm\_lead\_data at “source” from “Facebook”.
- Set crm\_lead\_data at “facebook\_lead\_id” from lead at “id”.
- Set crm\_lead\_data at “facebook\_form\_id” from self.form\_id.
- Attempt the following.
  - Evaluate self.validate\_duplicate\_lead(crm\_lead\_data, question\_to\_field\_map).
  - Return Platform.get\_doc(mapping(“doctype” → “CRM Lead”, expand crm\_lead\_data)).insert(ignore\_permissions = true).
- On failure (tuple(Platform.UniqueValidationError, DuplicateLeadError)).
  - Evaluate self.create\_failure\_log(lead, “Duplicate”).
  - If raise\_exception.
    - Propagate the active failure.
- On failure (Exception).
  - Evaluate self.create\_failure\_log(lead, traceback = Platform.get\_traceback(with\_context = true)).
  - If raise\_exception.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get form questions mapping](operations-001.md#op-2178361ab0741d), [validate duplicate lead](operations-001.md#op-601c632109c3ea), [create failure log](operations-001.md#op-371e2f4a382abf).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L34) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1408) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1384)

<a id="op-b6b3239415b8b7"></a>
### Facebook Sync Source.fetch leads

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_fetch_leads`

**Inputs** self.

**Explicit results** make\_get\_request(url, params = params).get(“data”, list()).

**Local steps**

- Set url from self.get\_api\_url(formatted text /{self.form\_id}/leads).
- Set params from mapping(“access\_token” → self.access\_token, “fields” → “id,created\_time,field\_data”, “limit” → 100000).
- Set filtering from list().
- If self.last\_synced\_at.
  - Set timestamp from (site\_time\_to\_unix(self.last\_synced\_at) − SYNC\_OVERLAP\_SECONDS).
  - Evaluate filtering.append(mapping(“field” → “time\_created”, “operator” → “GREATER\_THAN”, “value” → timestamp)).
  - Set params at “filtering” from Platform.as\_json(filtering).
- Return make\_get\_request(url, params = params).get(“data”, list()).

**Methods declared on this owner** [get api url](operations-001.md#op-0995cb80d097bd).

**Values supplied outside this operation** service or queued work from make\_get\_request(url, params = params).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L32) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1401) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1377)

<a id="op-2178361ab0741d"></a>
### Facebook Sync Source.get form questions mapping

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_get_form_questions_mapping`

**Inputs** self.

**Record and data access** read “Facebook Lead Form Question” via get\_all.

**Explicit results** self.form\_questions\_mapping.

**Local steps**

- If self.form\_questions\_mapping.
  - Return self.form\_questions\_mapping.
- Set form\_questions from Platform.db.get\_all(“Facebook Lead Form Question”, filters = mapping(“parent” → self.form\_id), fields = list(“key”, “mapped\_to\_crm\_field”)).
- Set self.form\_questions\_mapping from mapping of q at “key” → q at “mapped\_to\_crm\_field” for q drawn from form\_questions where q at “mapped\_to\_crm\_field”.
  - Draw q from form\_questions, keep a combination only if (q at “mapped\_to\_crm\_field”).
- Return self.form\_questions\_mapping.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L6921) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1403) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1379)

<a id="op-37c0fc09cace4f"></a>
### Facebook Sync Source.last synced at

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_last_synced_at`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Lead Sync Source” via get\_value.

**Explicit results** Platform.db.get\_value(“Lead Sync Source”, (self.source\_name or mapping(“facebook\_lead\_form” → self.form\_id)), “last\_synced\_at”).

**Local steps**

- Return Platform.db.get\_value(“Lead Sync Source”, (self.source\_name or mapping(“facebook\_lead\_form” → self.form\_id)), “last\_synced\_at”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.source\_name → mapping(“facebook\_lead\_form” → self.form\_id).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L7165) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1406) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1382)

<a id="op-371e2f4a382abf"></a>
### Facebook Sync Source.create failure log

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_create_failure_log`

**Inputs** self, lead\_data = no value, type = “Failure”, traceback = no value.

**Record and data access** resolve a document from mapping(“doctype” → “Failed Lead Sync Log”, “type” → type, “lead\_data” → Platform.as\_json(lead\_data), “source” → self.get\_source\_name(), …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Failed Lead Sync Log”, “type” → type, “lead\_data” → Platform.as\_json(lead\_data), “source” → self.get\_source\_name(), …)).

**Explicit results** Platform.get\_doc(mapping(“doctype” → “Failed Lead Sync Log”, “type” → type, “lead\_data” → Platform.as\_json(lead\_data), “source” → self.get\_source\_name(), …)).insert(ignore\_permissions = true).

**Local steps**

- Return Platform.get\_doc(mapping(“doctype” → “Failed Lead Sync Log”, “type” → type, “lead\_data” → Platform.as\_json(lead\_data), “source” → self.get\_source\_name(), …)).insert(ignore\_permissions = true).

**Methods declared on this owner** [get source name](operations-001.md#op-ac44f47a2464ed).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1400) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1376)

<a id="op-9f67f1922478c0"></a>
### Facebook Sync Source.update last synced at

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_update_last_synced_at`

**Inputs** self, synced\_at.

**State and service calls** request set\_value on “Lead Sync Source”.

**Local steps**

- Evaluate Platform.db.set\_value(“Lead Sync Source”, (self.source\_name or mapping(“facebook\_lead\_form” → self.form\_id)), “last\_synced\_at”, synced\_at).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.source\_name → mapping(“facebook\_lead\_form” → self.form\_id).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L35) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1409) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1385)

<a id="op-ac44f47a2464ed"></a>
### Facebook Sync Source.get source name

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_get_source_name`

**Inputs** self.

**Record and data access** read “Lead Sync Source” via get\_value.

**Explicit results** self.source\_name · Platform.db.get\_value(“Lead Sync Source”, mapping(“facebook\_lead\_form” → self.form\_id), “name”).

**Local steps**

- If self.source\_name.
  - Return self.source\_name.
- Return Platform.db.get\_value(“Lead Sync Source”, mapping(“facebook\_lead\_form” → self.form\_id), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L394) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1404) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1380)

<a id="op-601c632109c3ea"></a>
### Facebook Sync Source.validate duplicate lead

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_facebook_sync_source_validate_duplicate_lead`

**Inputs** self, lead\_data, field\_mapping.

**Record and data access** read “CRM Lead” via exists.

**Explicit failure paths** DuplicateLeadError.

**Local steps**

- Set validation\_filters from mapping of crm\_field → (lead\_data.get(crm\_field) or tuple(“is”, “not set”)) for crm\_field drawn from field\_mapping.values().
  - Draw crm\_field from field\_mapping.values().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lead\_data.get(crm\_field) → tuple(“is”, “not set”).
- Set validation\_filters at “facebook\_form\_id” from lead\_data at “facebook\_form\_id”.
- If Platform.db.exists(“CRM Lead”, validation\_filters).
  - Raise DuplicateLeadError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L36) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1410) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1386)

<a id="op-8b59cdf9dfe3b7"></a>
### Site time to unix

`operation_relationships_binding_crm_lead_syncing_doctype_lead_sync_source_facebook_site_time_to_unix`

**Inputs** value.

**Declared result** int.

**Explicit results** int(get\_datetime(value).replace(tzinfo = ZoneInfo(get\_system\_timezone())).timestamp()).

**Local steps**

- Return int(get\_datetime(value).replace(tzinfo = ZoneInfo(get\_system\_timezone())).timestamp()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L214) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L370) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L351)

<a id="op-301b39f33f7ab9"></a>
### Fetch and store pages from facebook

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_fetch_and_store_pages_from_facebook`

**Inputs** access\_token.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Facebook Page” via exists.

**Explicit results** pages.

**Explicit failure paths** validation helper — Platform.\_(“Access token is required”) · validation helper — Platform.\_(“Invalid access token provided for Facebook.”).

**Local steps**

- If not access\_token.
  - Call the validation error handler Platform.throw(Platform.\_(“Access token is required”)).
- Set account\_details from get\_fb\_account\_details(access\_token).
- If not account\_details.get(“id”).
  - Call the validation error handler Platform.throw(Platform.\_(“Invalid access token provided for Facebook.”)).
- Set url from get\_fb\_graph\_api\_url(“/me/accounts”).
- Set pages from make\_get\_request(url, params = mapping(“access\_token” → access\_token)).get(“data”, list()).
- For each page in pages.
  - Set page\_id from page at “id”.
  - Set already\_synced from Platform.db.exists(“Facebook Page”, page\_id).
  - If not already\_synced.
    - Evaluate create\_facebook\_page\_in\_db(page, account\_details).
  - Set forms from fetch\_and\_store\_leadgen\_forms\_from\_facebook(page\_id, page at “access\_token”).
  - Set page at “forms” from forms.
- Return pages.

**Values supplied outside this operation** service or queued work from make\_get\_request(url, params = mapping(“access\_token” → access\_token)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L712) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1412) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1388)
