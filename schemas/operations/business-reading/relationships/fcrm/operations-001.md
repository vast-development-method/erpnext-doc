# Lead and deal records · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm availability status

<a id="op-00a7a1783d7be8"></a>
### CRMAvailability Status.validate

`operation_relationships_binding_crm_fcrm_doctype_crm_availability_status_crm_availability_status_crmavailabilitystatus_validate`

**Inputs** self.

**Local steps**

- Set before from self.get\_doc\_before\_save().
- Set was\_active from (before and before.enabled and before.category equals “Active”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → before.enabled → before.category equals “Active”.
- If (was\_active and not (self.enabled and self.category equals “Active”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in was\_active → not (self.enabled and self.category equals “Active”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enabled → self.category equals “Active”.
  - Evaluate self.ensure\_another\_active\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [ensure another active status](operations-001.md#op-a5790a193eb2c7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L188) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L344) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L325)

<a id="op-42bc54f79d9977"></a>
### CRMAvailability Status.on update

`operation_relationships_binding_crm_fcrm_doctype_crm_availability_status_crm_availability_status_crmavailabilitystatus_on_update`

**Inputs** self.

**Local steps**

- If (not self.enabled and self.has\_value\_changed(“enabled”) and not self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.enabled → self.has\_value\_changed(“enabled”) → not self.is\_new().
  - Evaluate self.clear\_from\_users().
- Evaluate publish\_statuses\_updated().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear from users](operations-001.md#op-ee9b9c074241fc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L187) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L343) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L324)

<a id="op-af3841a45e326c"></a>
### CRMAvailability Status.on trash

`operation_relationships_binding_crm_fcrm_doctype_crm_availability_status_crm_availability_status_crmavailabilitystatus_on_trash`

**Inputs** self.

**Local steps**

- If (self.enabled and self.category equals “Active”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enabled → self.category equals “Active”.
  - Evaluate self.ensure\_another\_active\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [ensure another active status](operations-001.md#op-a5790a193eb2c7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L186) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L342) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L323)

<a id="op-d52dc13b4c222e"></a>
### CRMAvailability Status.after delete

`operation_relationships_binding_crm_fcrm_doctype_crm_availability_status_crm_availability_status_crmavailabilitystatus_after_delete`

**Inputs** self.

**Local steps**

- Evaluate publish\_statuses\_updated().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L182) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L338) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L319)

<a id="op-107ddc86ae5f63"></a>
### CRMAvailability Status.after rename

`operation_relationships_binding_crm_fcrm_doctype_crm_availability_status_crm_availability_status_crmavailabilitystatus_after_rename`

**Inputs** self, old, new, merge = false.

**Local steps**

- Evaluate publish\_statuses\_updated().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L183) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L339) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L320)

<a id="op-a5790a193eb2c7"></a>
### CRMAvailability Status.ensure another active status

`operation_relationships_binding_crm_fcrm_doctype_crm_availability_status_crm_availability_status_crmavailabilitystatus_ensure_another_active_status`

**Inputs** self.

**Record and data access** read “CRM Availability Status” via exists.

**Explicit failure paths** validation helper — translated “Keep at least one enabled status in the Active category.”.

**Local steps**

- If not Platform.db.exists(“CRM Availability Status”, mapping(“category” → “Active”, “enabled” → 1, “name” → list(“!=”, self.name))).
  - Call the validation error handler Platform.throw(translated “Keep at least one enabled status in the Active category.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L185) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L341) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L322)

<a id="op-ee9b9c074241fc"></a>
### CRMAvailability Status.clear from users

`operation_relationships_binding_crm_fcrm_doctype_crm_availability_status_crm_availability_status_crmavailabilitystatus_clear_from_users`

**Inputs** self.

**Record and data access** read “User” via get\_all.

**State and service calls** request set\_value on “User”.

**Local steps**

- For each user in Platform.get\_all(“User”, mapping(“crm\_availability” → self.name), pluck = “name”).
  - Evaluate Platform.db.set\_value(“User”, user, mapping(“crm\_availability” → no value, “crm\_availability\_changed\_on” → Platform.utils.now(), “crm\_availability\_changed\_by” → Platform.session.user)).
  - Evaluate publish\_availability(user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L184) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L340) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L321)

## Record · Crm call log

<a id="op-d079859d98528e"></a>
### CRMCall Log.before insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_customer_relationship_call_log_before_insert`

**Inputs** self.

**Local steps**

- If not self.id.
  - Set self.id from generate\_hash(length = 12).
- If not self.telephony\_medium.
  - Set self.telephony\_medium from “Manual”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from generate\_hash(length = 12).

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L2622) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L747) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L728)

<a id="op-bf1d81c0567649"></a>
### CRMCall Log.default list data

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_customer_relationship_call_log_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “Caller”, “type” → “Link”, “key” → “caller”, “options” → “User”, …), mapping(“label” → “Receiver”, “type” → “Link”, “key” → “receiver”, “options” → “User”, …), mapping(“label” → “Typ ….
- Set rows from list(“name”, “caller”, “receiver”, “type”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L2743) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L748) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L729)

<a id="op-33c737d36f34fb"></a>
### CRMCall Log.parse list data

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_customer_relationship_call_log_parse_list_data`

**Inputs** calls.

**Explicit results** list of parse\_call\_log(call) for call drawn from calls when calls, otherwise list().

**Local steps**

- Return list of parse\_call\_log(call) for call drawn from calls when calls, otherwise list().
  - Value choice on calls — true gives list of parse\_call\_log(call) for call drawn from calls, false gives list().
  - Draw call from calls.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L3589) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L751) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L732)

<a id="op-f7344c30a0cfce"></a>
### CRMCall Log.has link

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_customer_relationship_call_log_has_link`

**Inputs** self, doctype, name.

**Explicit results** true.

**Local steps**

- For each link in self.links.
  - If (link.link\_doctype equals doctype and link.link\_name equals name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals doctype → link.link\_name equals name.
    - Return true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L3670) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L749) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L730)

<a id="op-5341f8cb59c690"></a>
### CRMCall Log.link with reference doc

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_customer_relationship_call_log_link_with_reference_record`

**Inputs** self, reference\_doctype, reference\_name.

**Explicit results** no value.

**Local steps**

- If self.has\_link(reference\_doctype, reference\_name).
  - Return no value.
- Evaluate self.append(“links”, mapping(“link\_doctype” → reference\_doctype, “link\_name” → reference\_name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has link](operations-001.md#op-f7344c30a0cfce).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L3792) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L750) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L731)

<a id="op-9f83677ab350d6"></a>
### CRMCall Log.as dict

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_customer_relationship_call_log_as_mapping`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** d.

**Local steps**

- Set d from super().as\_dict(expanded args, expanded names kwargs).
- Set recording\_url from d.get(“recording\_url”).
- If not recording\_url.
  - Return d.
- If recording\_url.startswith(tuple(“/files/”, “/private/files/”)).
  - Set d at “recording\_url\_path” from recording\_url.
- Otherwise.
  - Set d at “recording\_url\_path” from formatted text /api/method/crm.integrations.api.get\_recording\_url?call\_log\_name={d.get(“name”)}.
- Return d.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L10) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L746) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L727)

<a id="op-dcb54bd02acfce"></a>
### Parse call log

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_parse_call_log`

**Inputs** call.

**Record and data access** read “User” via get\_values.

**Explicit results** call.

**Local steps**

- Set call at “show\_recording” from false.
- Set call at “\_duration” from seconds\_to\_duration(call.get(“duration”)).
- If call.get(“type”) equals “Incoming”.
  - Set call at “activity\_type” from “incoming\_call”.
  - Set contact from get\_call\_contact(call, call.get(“from”)).
  - Set receiver from Platform.db.get\_values(“User”, call.get(“receiver”), list(“full\_name”, “user\_image”)) at 0 when call.get(“receiver”), otherwise list(no value, no value).
    - Value choice on call.get(“receiver”) — true gives Platform.db.get\_values(“User”, call.get(“receiver”), list(“full\_name”, “user\_image”)) at 0, false gives list(no value, no value).
  - Set call at “\_caller” from mapping(“label” → contact.get(“full\_name”, “Unknown”), “image” → contact.get(“image”)).
  - Set call at “\_receiver” from mapping(“label” → receiver at 0, “image” → receiver at 1).
- Otherwise.
  - If call.get(“type”) equals “Outgoing”.
    - Set call at “activity\_type” from “outgoing\_call”.
    - Set contact from get\_call\_contact(call, call.get(“to”)).
    - Set caller from Platform.db.get\_values(“User”, call.get(“caller”), list(“full\_name”, “user\_image”)) at 0 when call.get(“caller”), otherwise list(no value, no value).
      - Value choice on call.get(“caller”) — true gives Platform.db.get\_values(“User”, call.get(“caller”), list(“full\_name”, “user\_image”)) at 0, false gives list(no value, no value).
    - Set call at “\_caller” from mapping(“label” → caller at 0, “image” → caller at 1).
    - Set call at “\_receiver” from mapping(“label” → contact.get(“full\_name”, “Unknown”), “image” → contact.get(“image”)).
- Return call.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L12) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L754) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L735)

<a id="op-b03d4c2aa0c683"></a>
### Get call contact

`operation_relationships_binding_crm_fcrm_doctype_crm_call_log_crm_call_log_get_call_contact`

**Inputs** call, phone\_number.

**Explicit results** get\_contact\_by\_phone\_number(phone\_number) · mapping() · (get\_reference\_contact(doctype, name) or mapping()).

**Local steps**

- Set tuple(doctype, name) from tuple(call.get(“reference\_doctype”), call.get(“reference\_docname”)).
- If (doctype does not belong to tuple(“CRM Lead”, “CRM Deal”) or not name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype does not belong to tuple(“CRM Lead”, “CRM Deal”) → not name.
  - Return get\_contact\_by\_phone\_number(phone\_number).
- If not Platform.has\_permission(doctype, “read”, name).
  - Return mapping().
- Return (get\_reference\_contact(doctype, name) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_reference\_contact(doctype, name) → mapping().

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, name).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L189) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L345) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L326)

<a id="op-5310bb67b49c81"></a>
### Get reference contact

`operation_relationships_binding_crm_fcrm_doctype_crm_call_log_crm_call_log_get_reference_contact`

**Inputs** doctype, name.

**Record and data access** read “CRM Lead” via get\_value · read “CRM Contacts” via get\_value · read “Contact” via get\_value · read “CRM Deal” via get\_value.

**Explicit results** (lead and mapping(“full\_name” → lead.lead\_name, “image” → lead.image)) · Platform.db.get\_value(“Contact”, contact, list(“full\_name”, “image”), as\_dict = true) · (deal\_name and mapping(“full\_name” → deal\_name)).

**Local steps**

- If doctype equals “CRM Lead”.
  - Set lead from Platform.db.get\_value(“CRM Lead”, name, list(“lead\_name”, “image”), as\_dict = true).
  - Return (lead and mapping(“full\_name” → lead.lead\_name, “image” → lead.image)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in lead → mapping(“full\_name” → lead.lead\_name, “image” → lead.image).
- Set contact from Platform.db.get\_value(“CRM Contacts”, mapping(“parenttype” → “CRM Deal”, “parent” → name, “is\_primary” → 1), “contact”).
- If contact.
  - Return Platform.db.get\_value(“Contact”, contact, list(“full\_name”, “image”), as\_dict = true).
- Set deal from Platform.db.get\_value(“CRM Deal”, name, list(“lead\_name”, “organization”, “organization\_name”), as\_dict = true).
- Set deal\_name from (deal and (deal.lead\_name or deal.organization or deal.organization\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in deal → (deal.lead\_name or deal.organization or deal.organization\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in deal.lead\_name → deal.organization → deal.organization\_name.
- Return (deal\_name and mapping(“full\_name” → deal\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in deal\_name → mapping(“full\_name” → deal\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L190) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L346) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L327)

<a id="op-dbfb11fed2b2dc"></a>
### Get call log

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_get_call_log`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM Call Log” via get\_cached\_doc.

**Explicit results** call.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“CRM Call Log”, “read”, name).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set call from Platform.get\_cached\_doc(“CRM Call Log”, name, fields = list(“name”, “caller”, “receiver”, “duration”, …)).as\_dict().
- Set call from parse\_call\_log(call).
- Set note\_names from list(call at “note”) when call.get(“note”), otherwise list().
  - Value choice on call.get(“note”) — true gives list(call at “note”), false gives list().
- Set task\_names from list().
- Set references from mapping().
- If (call.get(“reference\_doctype”) belongs to tuple(“CRM Lead”, “CRM Deal”) and call.get(“reference\_docname”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in call.get(“reference\_doctype”) belongs to tuple(“CRM Lead”, “CRM Deal”) → call.get(“reference\_docname”).
  - Set references at call at “reference\_doctype” from call at “reference\_docname”.
- For each link in (call.get(“links”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call.get(“links”) → list().
  - Set tuple(link\_doctype, link\_name) from tuple(link.get(“link\_doctype”), link.get(“link\_name”)).
  - If link\_doctype equals “CRM Task”.
    - Evaluate task\_names.append(link\_name).
  - Otherwise.
    - If link\_doctype equals “FCRM Note”.
      - Evaluate note\_names.append(link\_name).
    - Otherwise.
      - If link\_doctype belongs to tuple(“CRM Lead”, “CRM Deal”).
        - Evaluate references.setdefault(link\_doctype, link\_name).
- Set call at “\_notes” from get\_permitted\_docs(“FCRM Note”, note\_names).
- Set call at “\_tasks” from get\_permitted\_docs(“CRM Task”, task\_names).
- Set tuple(lead, deal) from tuple(references.get(“CRM Lead”), references.get(“CRM Deal”)).
- If (lead and Platform.has\_permission(“CRM Lead”, “read”, lead)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lead → Platform.has\_permission(“CRM Lead”, “read”, lead).
  - Set call at “\_lead” from lead.
- If (deal and Platform.has\_permission(“CRM Deal”, “read”, deal)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in deal → Platform.has\_permission(“CRM Deal”, “read”, deal).
  - Set call at “\_deal” from deal.
- Return call.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Call Log”, “read”, name), Platform.has\_permission(“CRM Lead”, “read”, lead) and 1 further calls · configured or stored value from Platform.get\_cached\_doc(“CRM Call Log”, name, fields = list(“name”, “caller”, “receiver”, “duration”, …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L11) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L752) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L733)

<a id="op-66b4c95f1c49b9"></a>
### Get permitted docs

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_get_permitted_records`

**Inputs** doctype, names.

**Declared result** list at dict.

**Record and data access** read doctype via get\_list.

**Explicit results** list() · sorted(docs, key = deferred anonymous expression).

**Local steps**

- If (not names or not Platform.has\_permission(doctype, “read”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not names → not Platform.has\_permission(doctype, “read”).
  - Return list().
- Set docs from Platform.get\_list(doctype, filters = mapping(“name” → tuple(“in”, names)), fields = list(“\*”), limit = len(names)).
- Return sorted(docs, key = deferred anonymous expression).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L6236) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L753) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L734)

<a id="op-22de39ac3c20e3"></a>
### Create lead from call log

`operation_relationships_fcrm_record_definitions_customer_relationship_management_call_log_business_behavior_create_lead_from_call_log`

**Inputs** call\_log, lead\_details = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM Call Log” via get\_doc.

**State and service calls** request new\_doc for “CRM Lead” · call insert on lead · call save on call\_doc.

**Explicit results** lead.name.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “A valid call log is required.” · validation helper with Platform.PermissionError — translated “You are not permitted to update this call log.” · validation helper with Platform.PermissionError — translated “You are not permitted to create leads.” · validation helper with Platform.ValidationError — translated “Invalid lead details supplied.”.

**Local steps**

- Set call\_log\_data from Platform.parse\_json((call\_log or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_log → mapping().
- If isinstance(call\_log\_data, str).
  - Set call\_log\_name from call\_log\_data.
- Otherwise.
  - If isinstance(call\_log\_data, dict).
    - Set call\_log\_name from call\_log\_data.get(“name”).
  - Otherwise.
    - Set call\_log\_name from no value.
- If not call\_log\_name.
  - Call the validation error handler Platform.throw(translated “A valid call log is required.”, Platform.ValidationError).
- Set call\_doc from Platform.get\_doc(“CRM Call Log”, call\_log\_name).
- If not call\_doc.has\_permission(“write”).
  - Call the validation error handler Platform.throw(translated “You are not permitted to update this call log.”, Platform.PermissionError).
- If not Platform.has\_permission(“CRM Lead”, “create”).
  - Call the validation error handler Platform.throw(translated “You are not permitted to create leads.”, Platform.PermissionError).
- Set lead\_details\_data from Platform.parse\_json((lead\_details or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lead\_details → mapping().
- If (lead\_details\_data and not isinstance(lead\_details\_data, dict)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lead\_details\_data → not isinstance(lead\_details\_data, dict).
  - Call the validation error handler Platform.throw(translated “Invalid lead details supplied.”, Platform.ValidationError).
- Set lead from Platform.new\_doc(“CRM Lead”).
- Set meta from Platform.get\_meta(“CRM Lead”).
- Set valid\_fieldnames from list of df.fieldname for df drawn from meta.fields.
  - Draw df from meta.fields.
- Set sanitized\_details from mapping of key → value for tuple(key, value) drawn from (lead\_details\_data or mapping()).items() where key belongs to valid\_fieldnames.
  - Draw tuple(key, value) from (lead\_details\_data or mapping()).items(), keep a combination only if (key belongs to valid\_fieldnames).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lead\_details\_data → mapping().
- If (“lead\_owner” belongs to valid\_fieldnames and not sanitized\_details.get(“lead\_owner”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “lead\_owner” belongs to valid\_fieldnames → not sanitized\_details.get(“lead\_owner”).
  - Set sanitized\_details at “lead\_owner” from Platform.session.user.
- If (“mobile\_no” belongs to valid\_fieldnames and not sanitized\_details.get(“mobile\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “mobile\_no” belongs to valid\_fieldnames → not sanitized\_details.get(“mobile\_no”).
  - Set sanitized\_details at “mobile\_no” from (call\_doc.get(“from”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_doc.get(“from”) → empty text.
- If (“first\_name” belongs to valid\_fieldnames and not sanitized\_details.get(“first\_name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “first\_name” belongs to valid\_fieldnames → not sanitized\_details.get(“first\_name”).
  - Set reference\_label from (sanitized\_details.get(“mobile\_no”) or call\_doc.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sanitized\_details.get(“mobile\_no”) → call\_doc.name.
  - Set sanitized\_details at “first\_name” from translated “Lead from call {0}”.format(reference\_label).
- Evaluate lead.update(sanitized\_details).
- Evaluate lead.insert().
- Evaluate call\_doc.link\_with\_reference\_doc(“CRM Lead”, lead.name).
- Evaluate call\_doc.save().
- Return lead.name.

**Values supplied outside this operation** effective access from call\_doc.has\_permission(“write”), Platform.has\_permission(“CRM Lead”, “create”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0029.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L745) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L726)

## Record · Crm dashboard

<a id="op-262db3bc83bc81"></a>
### Default manager dashboard layout

`operation_relationships_fcrm_record_definitions_customer_relationship_management_dashboard_business_behavior_default_manager_dashboard_layout`

**Inputs** no declared parameters.

**Explicit results** “&#91;{"name":"total\_leads","type":"number\_chart","tooltip":"Total number of leads","layout":{"x":0,"y":0,"w":4," …”.

**Local steps**

- Return “&#91;{"name":"total\_leads","type":"number\_chart","tooltip":"Total number of leads","layout":{"x":0,"y":0,"w":4," …”.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L3290) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L787) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L768)

<a id="op-2828787637a63b"></a>
### Create default manager dashboard

`operation_relationships_fcrm_record_definitions_customer_relationship_management_dashboard_business_behavior_create_default_manager_dashboard`

**Inputs** force = false.

**Record and data access** read “CRM Dashboard” via exists · resolve a document from “CRM Dashboard” via get\_doc.

**State and service calls** request new\_doc for “CRM Dashboard” · call insert on doc · call save on doc.

**Explicit results** doc.layout.

**Local steps**

- If not Platform.db.exists(“CRM Dashboard”, “Manager Dashboard”).
  - Set doc from Platform.new\_doc(“CRM Dashboard”).
  - Set doc.title from “Manager Dashboard”.
  - Set doc.layout from default\_manager\_dashboard\_layout().
  - Evaluate doc.insert(ignore\_permissions = true).
- Otherwise.
  - Set doc from Platform.get\_doc(“CRM Dashboard”, “Manager Dashboard”).
  - If force.
    - Set doc.layout from default\_manager\_dashboard\_layout().
    - Evaluate doc.save(ignore\_permissions = true).
- Return doc.layout.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L3319) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L786) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L767)

## Record · Crm deal

<a id="op-3a6b008aece6a4"></a>
### Get deal contacts

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_application_interface_business_behavior_get_deal_contacts`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Contacts” via get\_all · resolve a document from “Contact” via get\_doc.

**Explicit results** deal\_contacts.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“CRM Deal”, “read”, name).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set contacts from Platform.get\_all(“CRM Contacts”, filters = mapping(“parenttype” → “CRM Deal”, “parent” → name), fields = list(“contact”, “is\_primary”), order\_by = “is\_primary desc, idx asc”, distinct = true).
- Set deal\_contacts from list().
- For each contact in contacts.
  - If not contact.contact.
    - Continue with the next iteration or loop test.
  - Set is\_primary from contact.is\_primary.
  - Set contact from Platform.get\_doc(“Contact”, contact.contact).as\_dict().
  - Set \_contact from mapping(“name” → contact.name, “image” → contact.image, “full\_name” → contact.full\_name, “email” → contact.email\_id, …).
  - Evaluate deal\_contacts.append(\_contact).
- Return deal\_contacts.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Deal”, “read”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L3616) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L788) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L769)

<a id="op-645cb55e8fbad2"></a>
### CRMDeal.before insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_before_insert`

**Inputs** self.

**Local steps**

- Bind dependencies enrich\_form\_submission.
- Evaluate enrich\_form\_submission(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L4179) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L797) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L778)

<a id="op-af85d13263e426"></a>
### CRMDeal.before validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_sla().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set sla](operations-002.md#op-7b56923ebd6fe8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L4239) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L799) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L780)
