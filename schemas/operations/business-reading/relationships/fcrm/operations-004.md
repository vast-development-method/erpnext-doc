# Lead and deal records · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm invitation

<a id="op-6f94eded2a5920"></a>
### CRMInvitation.validate existing user

`operation_relationships_binding_crm_fcrm_doctype_crm_invitation_crm_invitation_crminvitation_validate_existing_user`

**Inputs** self.

**Record and data access** read “User” via exists · resolve a document from “User” via get\_doc.

**Local steps**

- If Platform.db.exists(“User”, self.email).
  - Evaluate validate\_no\_role\_profile(Platform.get\_doc(“User”, self.email)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L191) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L347) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L328)

<a id="op-e8849401ea33b3"></a>
### CRMInvitation.create user if not exists

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_customer_relationship_invitation_create_user_if_not_exists`

**Inputs** self.

**Record and data access** read “User” via exists · resolve a document from “User” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “User”, user\_type = “System User”, email = self.email, send\_welcome\_email = 0, …).

**Explicit results** tuple(user, true) · tuple(Platform.get\_doc(“User”, self.email), false).

**Local steps**

- If not Platform.db.exists(“User”, self.email).
  - Set first\_name from self.email.split(“@”) at 0.title().
  - Set user from Platform.get\_doc(doctype = “User”, user\_type = “System User”, email = self.email, send\_welcome\_email = 0, …).insert(ignore\_permissions = true).
  - Return tuple(user, true).
- Return tuple(Platform.get\_doc(“User”, self.email), false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L5672) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L871) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L851)

<a id="op-ed649e18b9cb77"></a>
### Expire invitations

`operation_relationships_fcrm_record_definitions_customer_relationship_management_invitation_business_behavior_expire_invitations`

**Inputs** no declared parameters.

**Record and data access** read “CRM Invitation” via get\_all · resolve a document from “CRM Invitation” via get\_doc.

**State and service calls** call save on invitation.

**Local steps**

- Bind dependencies add\_days, now.
- Set days from 3.
- Set invitations\_to\_expire from Platform.db.get\_all(“CRM Invitation”, filters = mapping(“status” → “Pending”, “creation” → list(“&lt;”, add\_days(now(), negative days)))).
- For each invitation in invitations\_to\_expire.
  - Set invitation from Platform.get\_doc(“CRM Invitation”, invitation.name).
  - Set invitation.status from “Expired”.
  - Evaluate invitation.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0034.json#L5970) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L874) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L854)

## Record · Crm lead

<a id="op-84ebc57a8f3f3e"></a>
### CRMLead.before insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_before_insert`

**Inputs** self.

**Local steps**

- Bind dependencies enrich\_form\_submission.
- Evaluate enrich\_form\_submission(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L2042) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L893) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L873)

<a id="op-d566bc85f8b800"></a>
### CRMLead.before validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_sla().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set sla](operations-004.md#op-9b4f9c1da00b14).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L2102) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L895) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L875)

<a id="op-053942ce06c2c2"></a>
### CRMLead.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_status().
- Evaluate self.set\_full\_name().
- Evaluate self.set\_lead\_name().
- Evaluate self.set\_title().
- Evaluate self.validate\_email().
- Evaluate self.validate\_unique\_fields().
- Evaluate self.validate\_lost\_reason().
- If (not self.is\_new() and self.has\_value\_changed(“lead\_owner”) and self.lead\_owner).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“lead\_owner”) → self.lead\_owner.
  - Evaluate self.share\_with\_agent(self.lead\_owner).
  - Evaluate self.assign\_agent(self.lead\_owner).
- If self.has\_value\_changed(“status”).
  - Evaluate add\_status\_change\_log(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate status](operations-004.md#op-8eefc141be8929), [set full name](operations-004.md#op-d11251fc97934f), [set lead name](operations-004.md#op-6f29c25e36d9f8), [set title](operations-004.md#op-a86eff932462ac), [validate email](operations-004.md#op-7370d8309df9b7), [validate unique fields](operations-004.md#op-cd60e1490d1896), [validate lost reason](operations-004.md#op-7b2b9309b0c5e9), [share with agent](operations-004.md#op-f4a26d49ac0a89), [assign agent](operations-004.md#op-c6ba10a7957065).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L20) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L911) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L891)

<a id="op-9ceb0335ebfaf1"></a>
### CRMLead.after insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_after_insert`

**Inputs** self.

**Local steps**

- If self.lead\_owner.
  - If self.lead\_owner differs from Platform.session.user.
    - Evaluate self.share\_with\_agent(self.lead\_owner).
  - Evaluate self.assign\_agent(self.lead\_owner).
- Bind dependencies auto\_enrich\_on\_create.
- Evaluate auto\_enrich\_on\_create(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [share with agent](operations-004.md#op-f4a26d49ac0a89), [assign agent](operations-004.md#op-c6ba10a7957065).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L2478) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L890) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L870)

<a id="op-7abfa29f30b53b"></a>
### CRMLead.before save

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.apply\_sla().

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply sla](operations-005.md#op-f97593a476fbae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L2645) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L894) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L874)

<a id="op-8eefc141be8929"></a>
### CRMLead.validate status

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_validate_status`

**Inputs** self.

**Record and data access** read “CRM Lead Status” via exists · read “CRM Lead Status” via get\_all.

**Local steps**

- If (self.is\_new() and not self.status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not self.status.
  - If Platform.db.exists(“CRM Lead Status”, “New”).
    - Set self.status from “New”.
  - Otherwise.
    - Set self.status from Platform.get\_all(“CRM Lead Status”, mapping(“type” → “Open”), pluck = “name”) at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L2696) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L914) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L894)

<a id="op-d11251fc97934f"></a>
### CRMLead.set full name

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_set_full_name`

**Inputs** self.

**Local steps**

- If self.first\_name.
  - Set self.lead\_name from one space.join(generator of name for name drawn from list(self.salutation, self.first\_name, self.middle\_name, self.last\_name) where name).
    - Draw name from list(self.salutation, self.first\_name, self.middle\_name, self.last\_name), keep a combination only if (name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L2907) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L905) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L885)

<a id="op-6f29c25e36d9f8"></a>
### CRMLead.set lead name

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_set_lead_name`

**Inputs** self.

**Explicit failure paths** validation helper — translated “A Lead requires either a person's name or an organization's name”.

**Local steps**

- If not self.lead\_name.
  - If (not self.organization and not self.email and not self.flags.ignore\_mandatory).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.organization → not self.email → not self.flags.ignore\_mandatory.
    - Call the validation error handler Platform.throw(translated “A Lead requires either a person's name or an organization's name”).
  - Otherwise.
    - If self.organization.
      - Set self.lead\_name from self.organization.
    - Otherwise.
      - If self.email.
        - Set self.lead\_name from self.email.split(“@”) at 0.
      - Otherwise.
        - Set self.lead\_name from “Unnamed Lead”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L3041) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L906) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L886)

<a id="op-a86eff932462ac"></a>
### CRMLead.set title

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_set_title`

**Inputs** self.

**Local steps**

- Set self.title from (self.organization or self.lead\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.organization → self.lead\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L3295) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L908) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L888)

<a id="op-7370d8309df9b7"></a>
### CRMLead.validate email

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_validate_email`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Lead Owner cannot be same as the Lead Email Address”.

**Local steps**

- If self.email.
  - If not self.flags.ignore\_email\_validation.
    - Evaluate validate\_email\_address(self.email, throw = true).
  - If self.email equals self.lead\_owner.
    - Call the validation error handler Platform.throw(translated “Lead Owner cannot be same as the Lead Email Address”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L3360) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L912) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L892)

<a id="op-cd60e1490d1896"></a>
### CRMLead.validate unique fields

`operation_relationships_binding_crm_fcrm_doctype_crm_lead_crm_lead_crmlead_validate_unique_fields`

**Inputs** self.

**Record and data access** read self.doctype via exists.

**Explicit failure paths** validation helper with Platform.UniqueValidationError — translated “{0} {1} already exists”.format(translated df.label, Platform.bold(value)).

**Local steps**

- For each df in self.meta.get(“fields”, mapping(“unique” → 1)).
  - Set value from self.get(df.fieldname).
  - If (value and Platform.db.exists(self.doctype, mapping(df.fieldname → value, “name” → tuple(“!=”, self.name)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → Platform.db.exists(self.doctype, mapping(df.fieldname → value, “name” → tuple(“!=”, self.name))).
    - Call the validation error handler Platform.throw(translated “{0} {1} already exists”.format(translated df.label, Platform.bold(value)), Platform.UniqueValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L192) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L348) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L329)

<a id="op-7b2b9309b0c5e9"></a>
### CRMLead.validate lost reason

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_validate_lost_reason`

**Inputs** self.

**Record and data access** read “CRM Lead Status” via get\_cached\_value.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Please specify a reason for losing the lead.” · validation helper with Platform.ValidationError — translated “Please specify the reason for losing the lead.”.

**Local steps**

- If (self.status and Platform.get\_cached\_value(“CRM Lead Status”, self.status, “type”) equals “Lost”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status → Platform.get\_cached\_value(“CRM Lead Status”, self.status, “type”) equals “Lost”.
  - If not self.lost\_reason.
    - Call the validation error handler Platform.throw(translated “Please specify a reason for losing the lead.”, Platform.ValidationError).
  - Otherwise.
    - If (self.lost\_reason equals “Other” and not self.lost\_notes).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.lost\_reason equals “Other” → not self.lost\_notes.
      - Call the validation error handler Platform.throw(translated “Please specify the reason for losing the lead.”, Platform.ValidationError).
- If self.has\_value\_changed(“status”).
  - Evaluate add\_or\_remove\_lost\_reason\_section\_in\_sidepanel(self).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“CRM Lead Status”, self.status, “type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L3532) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L913) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L893)

<a id="op-c6ba10a7957065"></a>
### CRMLead.assign agent

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_assign_agent`

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
- Evaluate assign(mapping(“assign\_to” → list(agent), “doctype” → “CRM Lead”, “name” → self.name), ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L3845) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L892) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L872)

<a id="op-f4a26d49ac0a89"></a>
### CRMLead.share with agent

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_share_with_agent`

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

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L4078) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L909) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L889)

<a id="op-cc0caae272fa73"></a>
### CRMLead.create contact

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_create_contact`

**Inputs** self, existing\_contact = no value, throw = true.

**State and service calls** request new\_doc for “Contact” · call insert on contact.

**Explicit results** existing\_contact · contact.name.

**Local steps**

- If not self.lead\_name.
  - Evaluate self.set\_full\_name().
  - Evaluate self.set\_lead\_name().
- Set existing\_contact from (existing\_contact or self.contact\_exists(throw)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in existing\_contact → self.contact\_exists(throw).
- If existing\_contact.
  - Evaluate self.update\_lead\_contact(existing\_contact).
  - Return existing\_contact.
- Set contact from Platform.new\_doc(“Contact”).
- Evaluate contact.update(mapping(“first\_name” → (self.first\_name or self.lead\_name), “last\_name” → self.last\_name, “salutation” → self.salutation, “gender” → self.gender, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.first\_name → self.lead\_name.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.image → empty text.
- If self.email.
  - Evaluate contact.append(“email\_ids”, mapping(“email\_id” → self.email, “is\_primary” → 1)).
- If self.phone.
  - Evaluate contact.append(“phone\_nos”, mapping(“phone” → self.phone, “is\_primary\_phone” → 1)).
- If self.mobile\_no.
  - Evaluate contact.append(“phone\_nos”, mapping(“phone” → self.mobile\_no, “is\_primary\_mobile\_no” → 1)).
- Evaluate contact.insert(ignore\_permissions = true).
- Evaluate contact.reload().
- Return contact.name.

**Methods declared on this owner** [set full name](operations-004.md#op-d11251fc97934f), [set lead name](operations-004.md#op-6f29c25e36d9f8), [contact exists](operations-004.md#op-017e2a4bef00cd), [update lead contact](operations-004.md#op-98a798e9c03aa5).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L4625) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L899) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L879)

<a id="op-5d1194cfdc4b72"></a>
### CRMLead.create organization

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_create_organization`

**Inputs** self, existing\_organization = no value.

**Record and data access** read “CRM Organization” via exists.

**State and service calls** call db\_set on self · request new\_doc for “CRM Organization” · call insert on organization.

**Explicit results** no value · existing\_organization · organization.name.

**Local steps**

- If (not self.organization and not existing\_organization).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.organization → not existing\_organization.
  - Return no value.
- Set existing\_organization from (existing\_organization or Platform.db.exists(“CRM Organization”, mapping(“organization\_name” → self.organization))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in existing\_organization → Platform.db.exists(“CRM Organization”, mapping(“organization\_name” → self.organization)).
- If existing\_organization.
  - Evaluate self.db\_set(“organization”, existing\_organization).
  - Evaluate self.copy\_enrichment\_from\_organization().
  - Return existing\_organization.
- Set organization from Platform.new\_doc(“CRM Organization”).
- Evaluate organization.update(mapping(“organization\_name” → self.organization, “website” → self.website, “territory” → self.territory, “industry” → self.industry, …)).
- Evaluate organization.insert(ignore\_permissions = true).
- Return organization.name.

**Methods declared on this owner** [copy enrichment from organization](operations-004.md#op-9be38994b00245).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L5347) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L901) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L881)

<a id="op-9be38994b00245"></a>
### CRMLead.copy enrichment from organization

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_copy_enrichment_from_organization`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** filled.

**Local steps**

- Bind dependencies copy\_enrichment\_from\_organization.
- Set enriched\_fields from tuple(“organization\_logo”, “company\_description”, “industry”, “linkedin”, …).
- Set before from mapping of f → self.get(f) for f drawn from enriched\_fields where self.meta.has\_field(f).
  - Draw f from enriched\_fields, keep a combination only if (self.meta.has\_field(f)).
- Set filled from copy\_enrichment\_from\_organization(self).
- For each tuple(fieldname, old\_value) in before.items().
  - Set new\_value from self.get(fieldname).
  - If new\_value differs from old\_value.
    - Evaluate self.db\_set(fieldname, new\_value).
- Return filled.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L5790) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L898) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L878)

<a id="op-98a798e9c03aa5"></a>
### CRMLead.update lead contact

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_update_lead_contact`

**Inputs** self, contact.

**Record and data access** resolve a document from “Contact” via get\_cached\_doc.

**State and service calls** request set\_value on “CRM Lead”.

**Local steps**

- Set contact from Platform.get\_cached\_doc(“Contact”, contact).
- Evaluate Platform.db.set\_value(“CRM Lead”, self.name, mapping(“salutation” → contact.salutation, “first\_name” → contact.first\_name, “last\_name” → contact.last\_name, “email” → contact.email\_id, …)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Contact”, contact).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0035.json#L6119) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L910) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L890)

<a id="op-017e2a4bef00cd"></a>
### CRMLead.contact exists

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_contact_exists`

**Inputs** self, throw = true.

**Record and data access** read “Contact Email” via exists · read “Contact Phone” via exists · read doctype via get\_value.

**Explicit results** contact · false.

**Explicit failure paths** validation helper — translated “Contact already exists with {0}”.format(value).

**Local steps**

- Set email\_exist from Platform.db.exists(“Contact Email”, mapping(“email\_id” → self.email)).
- Set phone\_exist from Platform.db.exists(“Contact Phone”, mapping(“phone” → self.phone)).
- Set mobile\_exist from Platform.db.exists(“Contact Phone”, mapping(“phone” → self.mobile\_no)).
- Set doctype from “Contact Email” when email\_exist, otherwise “Contact Phone”.
  - Value choice on email\_exist — true gives “Contact Email”, false gives “Contact Phone”.
- Set name from (email\_exist or phone\_exist or mobile\_exist).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_exist → phone\_exist → mobile\_exist.
- If name.
  - Set text from “Email” when email\_exist, otherwise “Phone” when phone\_exist, otherwise “Mobile No”.
    - Value choice on email\_exist — true gives “Email”, false gives “Phone” when phone\_exist, otherwise “Mobile No”.
    - Value choice on phone\_exist — true gives “Phone”, false gives “Mobile No”.
  - Set data from self.email when email\_exist, otherwise self.phone when phone\_exist, otherwise self.mobile\_no.
    - Value choice on email\_exist — true gives self.email, false gives self.phone when phone\_exist, otherwise self.mobile\_no.
    - Value choice on phone\_exist — true gives self.phone, false gives self.mobile\_no.
  - Set value from “{0}: {1}”.format(text, data).
  - Set contact from Platform.db.get\_value(doctype, name, “parent”).
  - If throw.
    - Call the validation error handler Platform.throw(translated “Contact already exists with {0}”.format(value), title = translated “Contact Already Exists”).
  - Return contact.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L18) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L896) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L876)

<a id="op-91da7c98efb0d1"></a>
### CRMLead.create deal

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_create_deal`

**Inputs** self, contact, organization, deal = no value.

**State and service calls** request new\_doc for “CRM Deal” · call insert on new\_deal · request set\_value on “CRM Deal”.

**Explicit results** new\_deal.name.

**Local steps**

- Set new\_deal from Platform.new\_doc(“CRM Deal”).
- Set restricted\_fieldtypes from list(“Tab Break”, “Section Break”, “Column Break”, “HTML”, …).
- Set restricted\_map\_fields from list(“name”, “naming\_series”, “creation”, “owner”, …).
- For each field in self.meta.fields.
  - If field.fieldtype belongs to restricted\_fieldtypes.
    - Continue with the next iteration or loop test.
  - If field.fieldname belongs to restricted\_map\_fields.
    - Continue with the next iteration or loop test.
  - Set fieldname from get\_deal\_fieldname(field, new\_deal.meta).
  - If fieldname.
    - If fieldname equals “organization”.
      - Evaluate new\_deal.update(mapping(fieldname → organization)).
    - Otherwise.
      - Evaluate new\_deal.update(mapping(fieldname → self.get(field.fieldname))).
- Evaluate new\_deal.update(mapping(“lead” → self.name, “contacts” → list(mapping(“contact” → contact)))).
- If self.first\_responded\_on.
  - Evaluate new\_deal.update(mapping(“sla\_creation” → self.sla\_creation, “response\_by” → self.response\_by, “sla\_status” → self.sla\_status, “communication\_status” → self.communication\_status, …)).
- If deal.
  - Evaluate new\_deal.update(deal).
- Evaluate new\_deal.insert(ignore\_permissions = true).
- For each user in self.get\_assigned\_users().
  - If (user and user differs from new\_deal.deal\_owner).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in user → user differs from new\_deal.deal\_owner.
    - Evaluate new\_deal.assign\_agent(user).
- If new\_deal.deal\_owner.
  - Evaluate Platform.db.set\_value(“CRM Deal”, new\_deal.name, “deal\_owner”, new\_deal.deal\_owner, update\_modified = false).
- Return new\_deal.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L19) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L900) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L880)

<a id="op-9b4f9c1da00b14"></a>
### CRMLead.set sla

`operation_relationships_fcrm_record_definitions_customer_relationship_management_lead_business_behavior_customer_relationship_lead_set_service_level_agreement`

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

[Applicable decision contract](../../../relationships-decision-contracts/part-0036.json#L969) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L907) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L887)
