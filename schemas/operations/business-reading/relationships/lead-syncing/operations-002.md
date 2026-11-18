# Lead synchronization · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Lead sync source

[Record definition](../../../../data/record-types/lead_sync_source.json)

<a id="op-2834ddaf51c37e"></a>
### Get fb account details

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_get_fb_account_details`

**Inputs** access\_token.

**Declared result** dict.

**Explicit results** response.

**Explicit failure paths** validation helper — Platform.\_(“Please check your access token”).

**Local steps**

- Set url from get\_fb\_graph\_api\_url(“me”).
- Attempt the following.
  - Set response from make\_get\_request(url, params = mapping(“access\_token” → access\_token)).
- On failure (Exception) bound to \_.
  - Call the validation error handler Platform.throw(Platform.\_(“Please check your access token”)).
- Return response.

**Values supplied outside this operation** service or queued work from make\_get\_request(url, params = mapping(“access\_token” → access\_token)).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L1236) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1413) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1389)

<a id="op-97db7ceeddaa9a"></a>
### Create facebook page in db

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_create_facebook_page_in_database`

**Inputs** page, account\_details.

**Declared result** no value.

**Record and data access** resolve a document from mapping(“doctype” → “Facebook Page”, “page\_name” → page at “name”, “id” → page at “id”, “category” → page at “category”, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Facebook Page”, “page\_name” → page at “name”, “id” → page at “id”, “category” → page at “category”, …)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Facebook Page”, “page\_name” → page at “name”, “id” → page at “id”, “category” → page at “category”, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L1425) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1399) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1375)

<a id="op-178383b0a03bb0"></a>
### Fetch and store leadgen forms from facebook

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_fetch_and_store_leadgen_forms_from_facebook`

**Inputs** page\_id, page\_access\_token.

**Declared result** list at dict.

**Record and data access** read “Facebook Lead Form” via exists.

**Explicit results** forms.

**Local steps**

- Set fields from “id,name,questions”.
- Set url from get\_fb\_graph\_api\_url(formatted text /{page\_id}/leadgen\_forms).
- Set forms from make\_get\_request(url, params = mapping(“access\_token” → page\_access\_token, “fields” → fields, “limit” → 15000)).get(“data”, list()).
- For each form in forms.
  - Set form\_id from form at “id”.
  - Set already\_synced from Platform.db.exists(“Facebook Lead Form”, form\_id).
  - If already\_synced.
    - Continue with the next iteration or loop test.
  - Evaluate create\_facebook\_lead\_form\_in\_db(form, page\_id).
- Return forms.

**Values supplied outside this operation** service or queued work from make\_get\_request(url, params = mapping(“access\_token” → page\_access\_token, “fields” → fields, “limit” → 15000)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L1679) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1411) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1387)

<a id="op-8be1807ffbf40e"></a>
### Create facebook lead form in db

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_create_facebook_lead_form_in_database`

**Inputs** form, page\_id.

**Declared result** no value.

**Record and data access** resolve a document from mapping(“doctype” → “Facebook Lead Form”, “form\_name” → form at “name”, “id” → form at “id”, “page” → page\_id, …) via get\_doc.

**State and service calls** call insert on form\_doc.

**Local steps**

- Set form\_doc from Platform.get\_doc(mapping(“doctype” → “Facebook Lead Form”, “form\_name” → form at “name”, “id” → form at “id”, “page” → page\_id, …)).
- Evaluate form\_doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L2038) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1398) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1374)

<a id="op-ca000c28c05e08"></a>
### Get pages with forms

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_facebook_business_behavior_get_pages_with_forms`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Facebook Page” via get\_all · read “Facebook Lead Form” via get\_all.

**Explicit results** pages.

**Local steps**

- Set pages from Platform.db.get\_all(“Facebook Page”, fields = list(“id”, “name”)).
- For each page in pages.
  - Set forms from Platform.db.get\_all(“Facebook Lead Form”, filters = mapping(“page” → page at “id”), fields = list(“id”, “name”)).
  - Set page at “forms” from forms.
- Return pages.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L2265) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1415) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1391)

<a id="op-d557375c50deb6"></a>
### Lead Sync Source.validate

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_business_behavior_lead_sync_source_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_same\_fb\_form\_active().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate same fb form active](operations-002.md#op-c59cee11d83d91).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L2532) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1396) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1372)

<a id="op-c59cee11d83d91"></a>
### Lead Sync Source.validate same fb form active

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_business_behavior_lead_sync_source_validate_same_fb_form_active`

**Inputs** self.

**Record and data access** read “Lead Sync Source” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — Platform.\_(“A lead sync source is already enabled for this Facebook Lead Form!”).

**Local steps**

- If not self.enabled.
  - Return no value.
- If not self.facebook\_lead\_form.
  - Return no value.
- Set already\_active from Platform.db.exists(“Lead Sync Source”, mapping(“enabled” → 1, “facebook\_lead\_form” → self.facebook\_lead\_form, “name” → list(“!=”, self.name))).
- If already\_active.
  - Call the validation error handler Platform.throw(Platform.\_(“A lead sync source is already enabled for this Facebook Lead Form!”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L2583) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1397) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1373)

<a id="op-a9fb90692deea1"></a>
### Lead Sync Source.before insert

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_business_behavior_lead_sync_source_before_insert`

**Inputs** self.

**Local steps**

- If (self.type equals “Facebook” and self.access\_token).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.type equals “Facebook” → self.access\_token.
  - Evaluate fetch\_and\_store\_pages\_from\_facebook(self.access\_token).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L2826) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1393) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1369)

<a id="op-8bb4de67b4f4bf"></a>
### Lead Sync Source.sync leads

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_business_behavior_lead_sync_source_sync_leads`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** enqueue doc with self.doctype.

**Explicit results** no value.

**Local steps**

- If Platform.conf.developer\_mode.
  - Evaluate self.\_sync\_leads().
  - Return no value.
- Evaluate Platform.enqueue\_doc(self.doctype, self.name, “\_sync\_leads”, queue = “long”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync leads](operations-002.md#op-73fb5fc6568cae).

**Values supplied outside this operation** service or queued work from Platform.enqueue\_doc(self.doctype, self.name, “\_sync\_leads”, queue = “long”).

**Boundaries to resolve** external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L2922) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1394) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1370)

<a id="op-73fb5fc6568cae"></a>
### Lead Sync Source.sync leads

`operation_relationships_lead_syncing_record_definitions_lead_sync_source_business_behavior_lead_sync_source_sync_leads_2`

**Inputs** self.

**Explicit failure paths** validation helper — Platform.\_(“Please select a lead gen form before syncing!”).

**Local steps**

- If (self.type equals “Facebook” and self.access\_token).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.type equals “Facebook” → self.access\_token.
  - If not self.facebook\_lead\_form.
    - Call the validation error handler Platform.throw(Platform.\_(“Please select a lead gen form before syncing!”)).
  - Evaluate FacebookSyncSource(self.get\_password(“access\_token”), self.facebook\_lead\_form).sync().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L3067) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1395) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1371)
