# Lead and deal records · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm deal

<a id="op-b143ee240e6f8b"></a>
### CRMDeal.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_validate`

**Inputs** self.

**Record and data access** read “CRM Deal Status” via get\_value.

**Local steps**

- Evaluate self.validate\_status().
- Evaluate self.set\_primary\_contact().
- Evaluate self.set\_primary\_email\_mobile\_no().
- If (not self.is\_new() and self.has\_value\_changed(“deal\_owner”) and self.deal\_owner).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“deal\_owner”) → self.deal\_owner.
  - Evaluate self.share\_with\_agent(self.deal\_owner).
  - Evaluate self.assign\_agent(self.deal\_owner).
- If self.has\_value\_changed(“status”).
  - Evaluate add\_status\_change\_log(self).
  - If Platform.db.get\_value(“CRM Deal Status”, self.status, “type”) equals “Won”.
    - Set self.closed\_date from Platform.utils.nowdate().
- Evaluate self.validate\_forecasting\_fields().
- Evaluate self.validate\_lost\_reason().
- Evaluate self.update\_exchange\_rate().
- If (self.organization and (self.is\_new() or self.has\_value\_changed(“organization”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.organization → (self.is\_new() or self.has\_value\_changed(“organization”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_value\_changed(“organization”).
  - Evaluate self.copy\_enrichment\_from\_organization().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate status](operations-002.md#op-b21dcc0f8b76f3), [set primary contact](operations-002.md#op-b9269b1c8cd6ce), [set primary email mobile no](operations-002.md#op-68dffdcdc2ac2c), [share with agent](operations-002.md#op-d370cdf0a4ff34), [assign agent](operations-002.md#op-2d528c8fcece70), [validate forecasting fields](operations-002.md#op-780de21c6ec65d), [validate lost reason](operations-002.md#op-a32da15b913055), [update exchange rate](operations-002.md#op-32077fcb7091f3), [copy enrichment from organization](operations-002.md#op-f77ebfbb4c5ffb).

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L4290) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L811) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L792)

<a id="op-d76f63475e42e5"></a>
### CRMDeal.after insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_after_insert`

**Inputs** self.

**Local steps**

- If self.deal\_owner.
  - If self.deal\_owner differs from Platform.session.user.
    - Evaluate self.share\_with\_agent(self.deal\_owner).
  - Evaluate self.assign\_agent(self.deal\_owner).
- Bind dependencies auto\_enrich\_on\_create.
- Evaluate auto\_enrich\_on\_create(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [share with agent](operations-002.md#op-d370cdf0a4ff34), [assign agent](operations-002.md#op-2d528c8fcece70).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L4797) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L794) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L775)

<a id="op-e1c9fc632fc460"></a>
### CRMDeal.before save

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.apply\_sla().

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply sla](operations-002.md#op-ae7e0c82a44163).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L4964) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L798) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L779)

<a id="op-b21dcc0f8b76f3"></a>
### CRMDeal.validate status

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_validate_status`

**Inputs** self.

**Record and data access** read “CRM Deal Status” via exists · read “CRM Deal Status” via get\_all.

**Local steps**

- If (self.is\_new() and not self.status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not self.status.
  - If Platform.db.exists(“CRM Deal Status”, “Qualification”).
    - Set self.status from “Qualification”.
  - Otherwise.
    - Set self.status from Platform.get\_all(“CRM Deal Status”, mapping(“type” → “Open”), pluck = “name”) at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L5015) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L814) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L795)

<a id="op-b9269b1c8cd6ce"></a>
### CRMDeal.set primary contact

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_set_primary_contact`

**Inputs** self, contact = no value.

**Explicit results** no value.

**Local steps**

- If not self.contacts.
  - Return no value.
- If (not contact and len(self.contacts) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not contact → len(self.contacts) equals 1.
  - Set self.contacts at 0.is\_primary from 1.
- Otherwise.
  - If contact.
    - For each d in self.contacts.
      - If d.contact equals contact.
        - Set d.is\_primary from 1.
      - Otherwise.
        - Set d.is\_primary from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L5226) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L803) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L784)

<a id="op-68dffdcdc2ac2c"></a>
### CRMDeal.set primary email mobile no

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_set_primary_email_mobile_number`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Only one {0} can be set as primary.”.format(Platform.bold(“Contact”)).

**Local steps**

- If not self.contacts.
  - Set self.email from empty text.
  - Set self.mobile\_no from empty text.
  - Set self.phone from empty text.
  - Return no value.
- If len(list of contact for contact drawn from self.contacts where contact.is\_primary) &gt; 1.
  - Draw contact from self.contacts, keep a combination only if (contact.is\_primary).
  - Call the validation error handler Platform.throw(translated “Only one {0} can be set as primary.”.format(Platform.bold(“Contact”))).
- Set primary\_contact\_exists from false.
- For each d in self.contacts.
  - If d.is\_primary equals 1.
    - Set primary\_contact\_exists from true.
    - Set self.email from d.email.strip() when d.email, otherwise empty text.
      - Value choice on d.email — true gives d.email.strip(), false gives empty text.
    - Set self.mobile\_no from d.mobile\_no.strip() when d.mobile\_no, otherwise empty text.
      - Value choice on d.mobile\_no — true gives d.mobile\_no.strip(), false gives empty text.
    - Set self.phone from d.phone.strip() when d.phone, otherwise empty text.
      - Value choice on d.phone — true gives d.phone.strip(), false gives empty text.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If not primary\_contact\_exists.
  - Set self.email from empty text.
  - Set self.mobile\_no from empty text.
  - Set self.phone from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L5462) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L804) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L785)

<a id="op-2d528c8fcece70"></a>
### CRMDeal.assign agent

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_assign_agent`

**Inputs** self, agent.

**Explicit results** no value.

**Local steps**

- If not agent.
  - Return no value.
- Set assignees from self.get\_assigned\_users().
- If assignees.
  - For each assignee in assignees.
    - If agent equals assignee.
      - Return no value.
- Evaluate assign(mapping(“assign\_to” → list(agent), “doctype” → “CRM Deal”, “name” → self.name), ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L5992) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L796) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L777)

<a id="op-d370cdf0a4ff34"></a>
### CRMDeal.share with agent

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_share_with_agent`

**Inputs** self, agent.

**Record and data access** read “DocShare” via get\_all · read “DocShare” via exists.

**Explicit results** no value.

**Local steps**

- If not agent.
  - Return no value.
- Set docshares from Platform.get\_all(“DocShare”, filters = mapping(“share\_name” → self.name, “share\_doctype” → self.doctype), fields = list(“name”, “user”)).
- Set shared\_with from (list of d.user for d drawn from docshares + list(agent)).
  - Draw d from docshares.
- For each user in shared\_with.
  - If (user equals agent and not Platform.db.exists(“DocShare”, mapping(“user” → agent, “share\_name” → self.name, “share\_doctype” → self.doctype))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in user equals agent → not Platform.db.exists(“DocShare”, mapping(“user” → agent, “share\_name” → self.name, “share\_doctype” → self.doctype)).
    - Evaluate Platform.share.add\_docshare(self.doctype, self.name, agent, write = 1, flags = mapping(“ignore\_share\_permission” → true)).
  - Otherwise.
    - If user differs from agent.
      - Evaluate Platform.share.remove(self.doctype, self.name, user, flags = mapping(“ignore\_share\_permission” → true, “ignore\_permissions” → true)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L6225) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L806) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L787)

<a id="op-f77ebfbb4c5ffb"></a>
### CRMDeal.copy enrichment from organization

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_copy_enrichment_from_organization`

**Inputs** self.

**Explicit results** copy\_enrichment\_from\_organization(self).

**Local steps**

- Bind dependencies copy\_enrichment\_from\_organization.
- Return copy\_enrichment\_from\_organization(self).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L6772) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L800) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L781)

<a id="op-7b56923ebd6fe8"></a>
### CRMDeal.set sla

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_set_service_level_agreement`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.sla.
  - Return no value.
- Set sla from get\_sla(self).
- If not sla.
  - Set self.first\_responded\_on from no value.
  - Set self.first\_response\_time from no value.
  - Return no value.
- Set self.sla from sla.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0030.json#L6832) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L805) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L786)

<a id="op-ae7e0c82a44163"></a>
### CRMDeal.apply sla

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_apply_service_level_agreement`

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

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L795) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L776)

<a id="op-a7b507c26e805b"></a>
### CRMDeal.update closed date

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_update_closed_date`

**Inputs** self.

**Local steps**

- If (self.status equals “Won” and not self.closed\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Won” → not self.closed\_date.
  - Set self.closed\_date from Platform.utils.nowdate().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L153) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L807) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L788)

<a id="op-0ac227b141f6a8"></a>
### CRMDeal.update default probability

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_update_default_probability`

**Inputs** self.

**Record and data access** read “CRM Deal Status” via get\_value.

**Local steps**

- If (not self.probability or self.probability equals 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.probability → self.probability equals 0.
  - Set self.probability from (Platform.db.get\_value(“CRM Deal Status”, self.status, “probability”) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“CRM Deal Status”, self.status, “probability”) → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L262) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L808) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L789)

<a id="op-2cedd7dccf7889"></a>
### CRMDeal.update expected deal value

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_update_expected_deal_value`

**Inputs** self.

**Record and data access** read “FCRM Settings” via get\_single\_value.

**Local steps**

- If (Platform.db.get\_single\_value(“FCRM Settings”, “auto\_update\_expected\_deal\_value”) and (self.net\_total or self.total) and self.expected\_deal\_value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“FCRM Settings”, “auto\_update\_expected\_deal\_value”) → (self.net\_total or self.total) → self.expected\_deal\_value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.net\_total → self.total.
  - Set self.expected\_deal\_value from (self.net\_total or self.total).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.net\_total → self.total.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “auto\_update\_expected\_deal\_value”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L406) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L810) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L791)

<a id="op-780de21c6ec65d"></a>
### CRMDeal.validate forecasting fields

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_validate_forecasting_fields`

**Inputs** self.

**Record and data access** read “FCRM Settings” via get\_single\_value.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Expected deal value is required.” · validation helper with Platform.MandatoryError — translated “Expected closure date is required.”.

**Local steps**

- Evaluate self.update\_closed\_date().
- Evaluate self.update\_default\_probability().
- Evaluate self.update\_expected\_deal\_value().
- If Platform.db.get\_single\_value(“FCRM Settings”, “enable\_forecasting”).
  - If (not self.expected\_deal\_value or self.expected\_deal\_value equals 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.expected\_deal\_value → self.expected\_deal\_value equals 0.
    - Call the validation error handler Platform.throw(translated “Expected deal value is required.”, Platform.MandatoryError).
  - If not self.expected\_closure\_date.
    - Call the validation error handler Platform.throw(translated “Expected closure date is required.”, Platform.MandatoryError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update closed date](operations-002.md#op-a7b507c26e805b), [update default probability](operations-002.md#op-0ac227b141f6a8), [update expected deal value](operations-002.md#op-2cedd7dccf7889).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “enable\_forecasting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L552) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L812) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L793)

<a id="op-a32da15b913055"></a>
### CRMDeal.validate lost reason

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_validate_lost_reason`

**Inputs** self.

**Record and data access** read “CRM Deal Status” via get\_cached\_value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Please specify a reason for losing the deal.” · validation helper with Platform.ValidationError — translated “Please specify the reason for losing the deal.”.

**Local steps**

- If (self.status and Platform.get\_cached\_value(“CRM Deal Status”, self.status, “type”) equals “Lost”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status → Platform.get\_cached\_value(“CRM Deal Status”, self.status, “type”) equals “Lost”.
  - If not self.lost\_reason.
    - Call the validation error handler Platform.throw(translated “Please specify a reason for losing the deal.”, Platform.ValidationError).
  - Otherwise.
    - If (self.lost\_reason equals “Other” and not self.lost\_notes).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.lost\_reason equals “Other” → not self.lost\_notes.
      - Call the validation error handler Platform.throw(translated “Please specify the reason for losing the deal.”, Platform.ValidationError).
- If self.has\_value\_changed(“status”).
  - Evaluate add\_or\_remove\_lost\_reason\_section\_in\_sidepanel(self).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“CRM Deal Status”, self.status, “type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L842) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L813) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L794)

<a id="op-32077fcb7091f3"></a>
### CRMDeal.update exchange rate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_update_exchange_rate`

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

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L1155) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L809) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L790)

<a id="op-fb60c0d91f118f"></a>
### CRMDeal.default list data

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “Organization”, “type” → “Link”, “key” → “organization”, “options” → “CRM Organization”, …), mapping(“label” → “Annual Revenue”, “type” → “Currency”, “key” → “annual\_revenue”, “align ….
- Set rows from list(“name”, “organization”, “annual\_revenue”, “status”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L1413) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L802) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L783)

<a id="op-881bc31c59155e"></a>
### CRMDeal.default kanban settings

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_customer_relationship_deal_default_kanban_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“column\_field” → “status”, “title\_field” → “organization”, “kanban\_fields” → “&#91;"annual\_revenue", "email", "mobile\_no", "\_assign", "modified"&#93;”).

**Local steps**

- Return mapping(“column\_field” → “status”, “title\_field” → “organization”, “kanban\_fields” → “&#91;"annual\_revenue", "email", "mobile\_no", "\_assign", "modified"&#93;”).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L2210) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L801) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L782)

<a id="op-3230fdb3ffd9ce"></a>
### Add contact

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_add_contact`

**Inputs** deal, contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM Deal” via get\_cached\_doc.

**State and service calls** call save on deal.

**Explicit results** true.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not allowed to add contact to Deal”.

**Local steps**

- If not Platform.has\_permission(“CRM Deal”, “write”, deal).
  - Call the validation error handler Platform.throw(translated “Not allowed to add contact to Deal”, Platform.PermissionError).
- Set deal from Platform.get\_cached\_doc(“CRM Deal”, deal).
- Evaluate deal.append(“contacts”, mapping(“contact” → contact)).
- Evaluate deal.save().
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Deal”, “write”, deal) · configured or stored value from Platform.get\_cached\_doc(“CRM Deal”, deal).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L2303) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L789) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L770)

<a id="op-5ce5ddd8d66698"></a>
### Remove contact

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_remove_contact`

**Inputs** deal, contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM Deal” via get\_cached\_doc.

**State and service calls** call save on deal.

**Explicit results** true.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not allowed to remove contact from Deal”.

**Local steps**

- If not Platform.has\_permission(“CRM Deal”, “write”, deal).
  - Call the validation error handler Platform.throw(translated “Not allowed to remove contact from Deal”, Platform.PermissionError).
- Set deal from Platform.get\_cached\_doc(“CRM Deal”, deal).
- Set deal.contacts from list of d for d drawn from deal.contacts where d.contact differs from contact.
  - Draw d from deal.contacts, keep a combination only if (d.contact differs from contact).
- Evaluate deal.save().
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Deal”, “write”, deal) · configured or stored value from Platform.get\_cached\_doc(“CRM Deal”, deal).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L2579) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L815) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L796)

<a id="op-f33d941be80268"></a>
### Set primary contact

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_set_primary_contact`

**Inputs** deal, contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “CRM Deal” via get\_cached\_doc.

**State and service calls** call save on deal.

**Explicit results** true.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not allowed to set primary contact for Deal”.

**Local steps**

- If not Platform.has\_permission(“CRM Deal”, “write”, deal).
  - Call the validation error handler Platform.throw(translated “Not allowed to set primary contact for Deal”, Platform.PermissionError).
- Set deal from Platform.get\_cached\_doc(“CRM Deal”, deal).
- Evaluate deal.set\_primary\_contact(contact).
- Evaluate deal.save().
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“CRM Deal”, “write”, deal) · configured or stored value from Platform.get\_cached\_doc(“CRM Deal”, deal).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L2866) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L816) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L797)

<a id="op-fcf07c2dce928e"></a>
### Create organization

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_create_organization`

**Inputs** doc.

**Record and data access** read “CRM Organization” via exists.

**State and service calls** request new\_doc for “CRM Organization” · call insert on organization.

**Explicit results** no value · existing\_organization · organization.name.

**Local steps**

- If not doc.get(“organization\_name”).
  - Return no value.
- Set existing\_organization from Platform.db.exists(“CRM Organization”, mapping(“organization\_name” → doc.get(“organization\_name”))).
- If existing\_organization.
  - Return existing\_organization.
- Set organization from Platform.new\_doc(“CRM Organization”).
- Evaluate organization.update(mapping(“organization\_name” → doc.get(“organization\_name”), “website” → doc.get(“website”), “territory” → doc.get(“territory”), “industry” → doc.get(“industry”), …)).
- Evaluate organization.insert(ignore\_permissions = true).
- Return organization.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L3116) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L793) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L774)

<a id="op-fead02aa9e7e4e"></a>
### Contact exists

`operation_relationships_fcrm_record_definitions_customer_relationship_management_deal_business_behavior_contact_exists`

**Inputs** doc.

**Record and data access** read “Contact Email” via exists · read “Contact Phone” via exists · read doctype via get\_value.

**Explicit results** Platform.db.get\_value(doctype, name, “parent”) · false.

**Local steps**

- Set email\_exist from Platform.db.exists(“Contact Email”, mapping(“email\_id” → doc.get(“email”))).
- Set mobile\_exist from Platform.db.exists(“Contact Phone”, mapping(“phone” → doc.get(“mobile\_no”))).
- Set doctype from “Contact Email” when email\_exist, otherwise “Contact Phone”.
  - Value choice on email\_exist — true gives “Contact Email”, false gives “Contact Phone”.
- Set name from (email\_exist or mobile\_exist).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_exist → mobile\_exist.
- If name.
  - Return Platform.db.get\_value(doctype, name, “parent”).
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0031.json#L3599) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L790) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L771)
