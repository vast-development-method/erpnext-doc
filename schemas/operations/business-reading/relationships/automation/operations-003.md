# Relationship automation · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Reference flows

<a id="op-0f8c16ffefb359"></a>
### Lead routing

`operation_relationships_binding_crm_automation_reference_flows_lead_routing`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Route the lead as it changes”, “CRM Lead”, “Doc Updated”), “actions” → list(step(1, “is\_hot”, “If”, condition = formatted text doc.lead\_score &gt;= {HOT\_SCORE}), assign\_step(2, “assign\_ho ….

**Local steps**

- Return mapping(expand flow(“Route the lead as it changes”, “CRM Lead”, “Doc Updated”), “actions” → list(step(1, “is\_hot”, “If”, condition = formatted text doc.lead\_score &gt;= {HOT\_SCORE}), assign\_step(2, “assign\_ho ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L118) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L274) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L255)

<a id="op-e0496e8470eed9"></a>
### Qualified routing

`operation_relationships_binding_crm_automation_reference_flows_qualified_routing`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Route the lead once qualified”, “CRM Lead”, “Field Value Changed”), “trigger\_field” → “status”, “to\_value” → “Qualified”, “actions” → list(assign\_step(1, “assign\_qualified”, QUALIFIED\_ ….

**Local steps**

- Return mapping(expand flow(“Route the lead once qualified”, “CRM Lead”, “Field Value Changed”), “trigger\_field” → “status”, “to\_value” → “Qualified”, “actions” → list(assign\_step(1, “assign\_qualified”, QUALIFIED\_ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L124) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L280) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L261)

<a id="op-1f3855f4133aeb"></a>
### Engagement scoring

`operation_relationships_binding_crm_automation_reference_flows_engagement_scoring`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Score the lead as it is worked”, “CRM Lead”, “Field Value Changed”), “trigger\_field” → “status”, “actions” → rows).

**Local steps**

- Set tuple(rows, idx) from tuple(list(), 1).
- For each tuple(key, label, condition, points) in ENGAGEMENT\_SIGNALS.
  - Evaluate rows.append(step(idx, key, “If”, condition = condition)).
  - Evaluate rows.append(score((idx + 1), \_points\_key(key), points, label, parent = idx, branch = “If”)).
  - Update idx using + 2.
- Update rows using + \_engagement\_banding(idx).
- Return mapping(expand flow(“Score the lead as it is worked”, “CRM Lead”, “Field Value Changed”), “trigger\_field” → “status”, “actions” → rows).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L111) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L267) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L248)

<a id="op-34e27b21b0e4cd"></a>
### Engagement banding

`operation_relationships_binding_crm_automation_reference_flows_engagement_banding`

**Inputs** idx.

**Declared result** list at dict.

**Explicit results** list(step(idx, “now\_hot”, “If”, condition = formatted text doc.lead\_score &gt;= {HOT\_SCORE}), temperature((idx + 1), “engagement\_hot”, “Hot”, target = “trigger”, parent = idx, branch = “If”), step((idx + 2),  ….

**Local steps**

- Return list(step(idx, “now\_hot”, “If”, condition = formatted text doc.lead\_score &gt;= {HOT\_SCORE}), temperature((idx + 1), “engagement\_hot”, “Hot”, target = “trigger”, parent = idx, branch = “If”), step((idx + 2),  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L110) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L266) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L247)

<a id="op-92ab74f7069c80"></a>
### Qualified conversion

`operation_relationships_binding_crm_automation_reference_flows_qualified_conversion`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Qualified lead becomes a deal”, “CRM Lead”, “Field Value Changed”), “trigger\_field” → “status”, “to\_value” → “Qualified”, “condition” → “doc.converted == 0”, …).

**Local steps**

- Return mapping(expand flow(“Qualified lead becomes a deal”, “CRM Lead”, “Field Value Changed”), “trigger\_field” → “status”, “to\_value” → “Qualified”, “condition” → “doc.converted == 0”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L123) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L279) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L260)

<a id="op-975abe679645ab"></a>
### Stalled deal

`operation_relationships_binding_crm_automation_reference_flows_stalled_deal`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“Stalled deal follow-up”, “CRM Deal”, “Field Value Changed”), “trigger\_field” → “status”, “relationships” → Platform.as\_json(list(mapping(“alias” → “lead”, “source” → “trigger”, “relati ….

**Local steps**

- Return mapping(expand flow(“Stalled deal follow-up”, “CRM Deal”, “Field Value Changed”), “trigger\_field” → “status”, “relationships” → Platform.as\_json(list(mapping(“alias” → “lead”, “source” → “trigger”, “relati ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L130) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L286) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L267)

<a id="op-18e09e6df9fb82"></a>
### High value deal watch

`operation_relationships_binding_crm_automation_reference_flows_high_value_deal_watch`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(expand flow(“High value deal watch”, “CRM Deal”, “Doc Updated”), “condition” → formatted text (doc.expected\_deal\_value or 0) &gt;= {HIGH\_VALUE\_AT}, “actions” → list(step(1, “is\_committing”, “If”, cond ….

**Local steps**

- Return mapping(expand flow(“High value deal watch”, “CRM Deal”, “Doc Updated”), “condition” → formatted text (doc.expected\_deal\_value or 0) &gt;= {HIGH\_VALUE\_AT}, “actions” → list(step(1, “is\_committing”, “If”, cond ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L116) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L272) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L253)

<a id="op-0ae8a891edafcf"></a>
### Notify step

`operation_relationships_binding_crm_automation_reference_flows_notify_step`

**Inputs** idx, key, channel, recipients, subject, message, remaining named values extra.

**Declared result** dict.

**Explicit results** action(idx, key, “SendNotification”, mapping(“channel” → channel, “recipients” → recipients, “subject” → subject, “message” → message), expanded names extra).

**Local steps**

- Return action(idx, key, “SendNotification”, mapping(“channel” → channel, “recipients” → recipients, “subject” → subject, “message” → message), expanded names extra).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L119) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L275) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L256)

<a id="op-5a0a5b9bdf829a"></a>
### Nudge step

`operation_relationships_binding_crm_automation_reference_flows_nudge_step`

**Inputs** idx, key, field, amount, remaining named values extra.

**Declared result** dict.

**Explicit results** action(idx, key, “IncrementFieldValue”, mapping(“field” → field, “amount” → amount), expanded names extra).

**Local steps**

- Return action(idx, key, “IncrementFieldValue”, mapping(“field” → field, “amount” → amount), expanded names extra).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L120) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L276) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L257)

<a id="op-200b938d3977b0"></a>
### Deal task step

`operation_relationships_binding_crm_automation_reference_flows_deal_task_step`

**Inputs** idx, key, title, days, remaining named values extra.

**Declared result** dict.

**Explicit results** action(idx, key, “CreateDocument”, mapping(“doctype” → “CRM Task”, “values” → values), expanded names extra).

**Local steps**

- Set values from mapping(“title” → title, “status” → “Todo”, “priority” → “High”, “assigned\_to” → “{{ doc.deal\_owner or '' }}”, …).
- Return action(idx, key, “CreateDocument”, mapping(“doctype” → “CRM Task”, “values” → values), expanded names extra).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L108) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L264) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L245)

<a id="op-924f836c4d1f39"></a>
### Flow

`operation_relationships_binding_crm_automation_reference_flows_flow`

**Inputs** title, document\_type, trigger\_type.

**Declared result** dict.

**Explicit results** mapping(“doctype” → “Automation Flow”, “title” → title, “document\_type” → document\_type, “trigger\_type” → trigger\_type, …).

**Local steps**

- Return mapping(“doctype” → “Automation Flow”, “title” → title, “document\_type” → document\_type, “trigger\_type” → trigger\_type, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L113) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L269) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L250)

<a id="op-47f627dd10a6f0"></a>
### Step

`operation_relationships_binding_crm_automation_reference_flows_step`

**Inputs** idx, key, step\_type, params = no value, condition = no value, parent = 0, branch = empty text, remaining named values extra.

**Declared result** dict.

**Explicit results** mapping(“doctype” → “Automation Action”, “idx” → idx, “step\_key” → key, “step\_type” → step\_type, …).

**Local steps**

- Return mapping(“doctype” → “Automation Action”, “idx” → idx, “step\_key” → key, “step\_type” → step\_type, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params → mapping().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L131) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L287) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L268)

<a id="op-2ba1976b39eded"></a>
### Action

`operation_relationships_binding_crm_automation_reference_flows_action`

**Inputs** idx, key, action\_type, params, target = “trigger”, remaining named values extra.

**Declared result** dict.

**Explicit results** row.

**Local steps**

- Set row from step(idx, key, “Action”, params = params, expanded names extra).
- Evaluate row.update(mapping(“action\_type” → action\_type, “target” → target)).
- Return row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L101) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L257) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L238)

<a id="op-523741bd1327ea"></a>
### Email step

`operation_relationships_binding_crm_automation_reference_flows_email_step`

**Inputs** idx, key, template, sender = no value, remaining named values extra.

**Declared result** dict.

**Explicit results** action(idx, key, “SendCRMEmail”, params, expanded names extra).

**Local steps**

- Set params from mapping(“email\_template” → template).
- If sender.
  - Set params at “sender” from sender.
- Return action(idx, key, “SendCRMEmail”, params, expanded names extra).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L109) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L265) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L246)

<a id="op-edf1bd8d4060e2"></a>
### Assign step

`operation_relationships_binding_crm_automation_reference_flows_assign_step`

**Inputs** idx, key, user, description, target = “trigger”, remaining named values extra.

**Declared result** dict.

**Explicit results** action(idx, key, “AssignToUser”, mapping(“assign\_to” → list(user), “description” → description), target = target, expanded names extra).

**Local steps**

- Return action(idx, key, “AssignToUser”, mapping(“assign\_to” → list(user), “description” → description), target = target, expanded names extra).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L103) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L259) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L240)

<a id="op-88347e6e697b2f"></a>
### Temperature

`operation_relationships_binding_crm_automation_reference_flows_temperature`

**Inputs** idx, key, value, target = “lead”, remaining named values extra.

**Declared result** dict.

**Explicit results** action(idx, key, “SetLeadTemperature”, mapping(“temperature” → value), target = target, expanded names extra).

**Local steps**

- Return action(idx, key, “SetLeadTemperature”, mapping(“temperature” → value), target = target, expanded names extra).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L132) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L288) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L269)

<a id="op-ec1f9cf71706f9"></a>
### Score

`operation_relationships_binding_crm_automation_reference_flows_score`

**Inputs** idx, key, amount, reason, target = “trigger”, remaining named values extra.

**Declared result** dict.

**Explicit results** action(idx, key, “AdjustLeadScore”, mapping(“amount” → amount, “reason” → reason), target = target, expanded names extra).

**Local steps**

- Return action(idx, key, “AdjustLeadScore”, mapping(“amount” → amount, “reason” → reason), target = target, expanded names extra).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L128) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L284) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L265)

<a id="op-514a2d0ba927d8"></a>
### Convert step

`operation_relationships_binding_crm_automation_reference_flows_convert_step`

**Inputs** idx, key.

**Declared result** dict.

**Explicit results** row.

**Local steps**

- Set params from mapping(“if\_converted” → “Return Existing”, “deal” → forecast\_defaults()).
- Set row from action(idx, key, “ConvertLeadToDeal”, params).
- Set row at “output\_alias” from “deal”.
- Return row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L106) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L262) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L243)

<a id="op-c2edd68d0b06ce"></a>
### Forecast defaults

`operation_relationships_binding_crm_automation_reference_flows_forecast_defaults`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** read “FCRM Settings” via get\_single\_value.

**Explicit results** mapping() · mapping(“expected\_deal\_value” → 1, “expected\_closure\_date” → Platform.utils.add\_months(Platform.utils.nowdate(), 1)).

**Local steps**

- If not Platform.db.get\_single\_value(“FCRM Settings”, “enable\_forecasting”).
  - Return mapping().
- Return mapping(“expected\_deal\_value” → 1, “expected\_closure\_date” → Platform.utils.add\_months(Platform.utils.nowdate(), 1)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “enable\_forecasting”) · clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L115) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L271) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L252)

<a id="op-f987adb029a8cc"></a>
### Create task step

`operation_relationships_binding_crm_automation_reference_flows_create_task_step`

**Inputs** idx, key.

**Declared result** dict.

**Explicit results** action(idx, key, “CreateDocument”, mapping(“doctype” → “CRM Task”, “values” → values), target = “deal”).

**Local steps**

- Set values from mapping(“title” → “Kickoff call - {{ doc.organization or doc.lead\_name }}”, “status” → “Todo”, “priority” → “High”, “assigned\_to” → “{{ trigger.lead\_owner or '' }}”, …).
- Return action(idx, key, “CreateDocument”, mapping(“doctype” → “CRM Task”, “values” → values), target = “deal”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L107) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L263) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L244)

<a id="op-a86691d7c6c846"></a>
### Follow up task step

`operation_relationships_binding_crm_automation_reference_flows_follow_up_task_step`

**Inputs** idx, key.

**Declared result** dict.

**Explicit results** row.

**Local steps**

- Set values from mapping(“title” → “Follow up on {{ doc.organization or doc.name }}”, “status” → “Todo”, “reference\_doctype” → “CRM Deal”, “reference\_docname” → “{{ doc.name }}”, …).
- Set row from action(idx, key, “CreateDocument”, mapping(“doctype” → “CRM Task”, “values” → values)).
- Set row at “related\_condition” from Platform.as\_json(mapping(“type” → “RelatedNotExists”, “source” → “trigger”, “relationship” → “tasks”, “filters” → list(list(“status”, “not in”, list(“Done”, “Canceled”))))).
- Return row.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L114) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L270) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L251)

<a id="op-9dd2ef9603c990"></a>
### Quiet check step

`operation_relationships_binding_crm_automation_reference_flows_quiet_check_step`

**Inputs** idx, key.

**Declared result** dict.

**Explicit results** row.

**Local steps**

- Set row from step(idx, key, “If”, condition = “True”).
- Set row at “related\_condition” from Platform.as\_json(mapping(“type” → “RelatedNotExists”, “source” → “trigger”, “relationship” → “communications”, “filters” → list(list(“sent\_or\_received”, “=”, “Received”), list(“creation”, “&gt;”, “{{ context. ….
- Return row.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L125) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L281) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L262)

## Service · Relationships

<a id="op-7167b87c37c563"></a>
### CRMRelationship Provider.get definitions

`operation_relationships_binding_crm_automation_relationships_crmrelationshipprovider_get_definitions`

**Inputs** self, source\_doctype.

**Declared result** list at dict.

**Explicit results** list of \_public(definition) for definition drawn from DEFINITIONS.get(source\_doctype, list()).

**Local steps**

- Return list of \_public(definition) for definition drawn from DEFINITIONS.get(source\_doctype, list()).
  - Draw definition from DEFINITIONS.get(source\_doctype, list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L140) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L296) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L277)

<a id="op-1c6940e325e298"></a>
### CRMRelationship Provider.resolve

`operation_relationships_binding_crm_automation_relationships_crmrelationshipprovider_resolve`

**Inputs** self, source\_doc, relationship, params.

**Declared result** list at dict.

**Explicit results** \_definition(source\_doc.doctype, relationship) at “resolve”(source\_doc).

**Local steps**

- Return \_definition(source\_doc.doctype, relationship) at “resolve”(source\_doc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L142) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L298) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L279)
