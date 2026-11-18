# Sales relationships · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email campaign

[Record definition](../../../../data/record-types/email_campaign.json)

<a id="op-cac205f73c3d00"></a>
### Email Campaign.validate email campaign already exists

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_email_campaign_validate_email_campaign_already_exists`

**Inputs** self.

**Record and data access** read “Email Campaign” via exists.

**Explicit failure paths** validation helper — translated “The Campaign '{0}' already exists for the {1} '{2}'”.format(self.campaign\_name, self.email\_campaign\_for, self.recipient).

**Local steps**

- Set email\_campaign\_exists from Platform.db.exists(“Email Campaign”, mapping(“campaign\_name” → self.campaign\_name, “recipient” → self.recipient, “status” → tuple(“in”, list(“In Progress”, “Scheduled”)), “name” → tuple(“!=”, self.name))).
- If email\_campaign\_exists.
  - Call the validation error handler Platform.throw(translated “The Campaign '{0}' already exists for the {1} '{2}'”.format(self.campaign\_name, self.email\_campaign\_for, self.recipient)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L4178) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1178)

<a id="op-700da67a29130d"></a>
### Email Campaign.update status

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_email_campaign_update_status`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- <a id="op-700da67a29130d-guard-2"></a>If self.status equals “Unsubscribed”.
  - Return no value.
- Set start\_date from getdate(self.start\_date).
- Set end\_date from getdate(self.end\_date).
- Set today\_date from getdate(today()).
- If start\_date &gt; today\_date.
  - Set new\_status from “Scheduled”.
- Otherwise.
  - If end\_date ≥ today\_date.
    - Set new\_status from “In Progress”.
  - Otherwise.
    - Set new\_status from “Completed”.
- If self.status differs from new\_status.
  - Evaluate self.db\_set(“status”, new\_status, update\_modified = false).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Unsubscribed”, self.status = “Unsubscribed” selects the branch that returns no value. With self.status = “Scheduled”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-700da67a29130d-guard-2)

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1175)

<a id="op-879d2fe376d2ef"></a>
### Send email to leads or contacts

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_send_email_to_leads_or_contacts`

**Inputs** no declared parameters.

**Record and data access** read “Email Campaign” via get\_all · resolve a document from “Campaign” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- Set today\_date from getdate(today()).
- Evaluate set\_email\_campaign\_status().
- Set email\_campaigns from Platform.get\_all(“Email Campaign”, filters = mapping(“status” → tuple(“!=”, “Unsubscribed”), “start\_date” → tuple(“&lt;=”, today\_date), “end\_date” → tuple(“&gt;=”, today\_date)), fields = list(“name”, “campaign\_n ….
- If not email\_campaigns.
  - Return no value.
- For each email\_campaign in email\_campaigns.
  - Attempt the following.
    - Set campaign from Platform.get\_cached\_doc(“Campaign”, email\_campaign.campaign\_name).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.log\_error(title = translated “Email Campaign Error”, message = translated “Campaign {0} not found”.format(email\_campaign.campaign\_name)).
    - Continue with the next iteration or loop test.
  - For each entry in campaign.get(“campaign\_schedules”).
    - Attempt the following.
      - Set scheduled\_date from add\_days(getdate(email\_campaign.start\_date), entry.get(“send\_after\_days”)).
      - If (scheduled\_date equals today\_date and not is\_step\_sent(email\_campaign.name, entry, today\_date)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in scheduled\_date equals today\_date → not is\_step\_sent(email\_campaign.name, entry, today\_date).
        - Evaluate send\_mail(entry, email\_campaign).
    - On failure (Exception).
      - Evaluate Platform.log\_error(title = translated “Email Campaign Send Error”, message = translated “Failed to send email for campaign {0} to {1}”.format(email\_campaign.name, email\_campaign.recipient)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today() · configured or stored value from Platform.get\_cached\_doc(“Campaign”, email\_campaign.campaign\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1181)

<a id="op-4c8536cda2756d"></a>
### Is step sent

`operation_enterprise_binding_enterprise_crm_doctype_email_campaign_email_campaign_is_step_sent`

**Inputs** email\_campaign, entry, on\_date.

**Declared result** bool.

**Record and data access** read “Communication” via exists.

**Explicit results** bool(Platform.db.exists(“Communication”, mapping(“reference\_doctype” → “Email Campaign”, “reference\_name” → email\_campaign, “email\_template” → entry.get(“email\_template”), “communication\_date” → tuple(“&gt;=” ….

**Local steps**

- Return bool(Platform.db.exists(“Communication”, mapping(“reference\_doctype” → “Email Campaign”, “reference\_name” → email\_campaign, “email\_template” → entry.get(“email\_template”), “communication\_date” → tuple(“&gt;=” ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1261) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L501)

<a id="op-ef529b4fb7d8a6"></a>
### Send mail

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_send_mail`

**Inputs** entry, email\_campaign.

**Record and data access** read “Email Group Member” via get\_all · read campaign\_for via get\_value · resolve a document from “Email Template” via get\_cached\_doc · read “User” via get\_value · resolve a document from campaign\_for via get\_doc.

**State and service calls** sendmail.

**Explicit results** no value · comm.

**Local steps**

- Set campaign\_for from email\_campaign.get(“email\_campaign\_for”).
- Set recipient from email\_campaign.get(“recipient”).
- Set sender\_user from email\_campaign.get(“sender”).
- Set campaign\_name from email\_campaign.get(“name”).
- If campaign\_for equals “Email Group”.
  - Set recipient\_list from Platform.get\_all(“Email Group Member”, filters = mapping(“email\_group” → recipient, “unsubscribed” → 0), pluck = “email”).
- Otherwise.
  - Set tuple(email\_id, unsubscribed) from Platform.db.get\_value(campaign\_for, recipient, list(“email\_id”, “unsubscribed”)).
  - If not email\_id.
    - Evaluate Platform.log\_error(title = translated “Email Campaign Error”, message = translated “No email found for {0} {1}”.format(campaign\_for, recipient)).
    - Return no value.
  - If unsubscribed.
    - Evaluate Platform.log\_error(title = translated “Email Campaign Error”, message = translated “{0} {1} has unsubscribed from emails”.format(campaign\_for, recipient)).
    - Return no value.
  - Set recipient\_list from list(email\_id).
- If not recipient\_list.
  - Evaluate Platform.log\_error(title = translated “Email Campaign Error”, message = translated “No recipients found for campaign {0}”.format(campaign\_name)).
  - Return no value.
- Set email\_template from Platform.get\_cached\_doc(“Email Template”, entry.get(“email\_template”)).
- Set sender from Platform.db.get\_value(“User”, sender\_user, “email”) when sender\_user, otherwise no value.
  - Value choice on sender\_user — true gives Platform.db.get\_value(“User”, sender\_user, “email”), false gives no value.
- Set doc from Platform.get\_doc(campaign\_for, recipient).
- Set context from mapping(expand doc.as\_dict(), “doc” → doc).
- Set subject from Platform.render\_template(email\_template.get(“subject”), context, restrict\_globals = true).
- Set content from Platform.render\_template(email\_template.response\_, context, restrict\_globals = true).
- Attempt the following.
  - Set comm from make(doctype = “Email Campaign”, name = campaign\_name, subject = subject, content = content, …).
  - Evaluate Platform.sendmail(recipients = recipient\_list, subject = subject, content = content, sender = sender, …).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Email Campaign Failed.”).
- Return comm.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Email Template”, entry.get(“email\_template”)) · service or queued work from Platform.sendmail(recipients = recipient\_list, subject = subject, content = content, sender = sender, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1182)

<a id="op-9ceff847694d9b"></a>
### Unsubscribe recipient

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_unsubscribe_recipient`

**Inputs** unsubscribe, method.

**Record and data access** resolve a document from “Email Campaign” via get\_doc.

**State and service calls** request set\_value on “Email Group Member” · request set\_value on “Email Campaign”.

**Explicit results** no value.

**Local steps**

- If unsubscribe.reference\_doctype differs from “Email Campaign”.
  - Return no value.
- Set email\_campaign from Platform.get\_doc(“Email Campaign”, unsubscribe.reference\_name).
- If email\_campaign.email\_campaign\_for equals “Email Group”.
  - If unsubscribe.email.
    - Evaluate Platform.db.set\_value(“Email Group Member”, mapping(“email\_group” → email\_campaign.recipient, “email” → unsubscribe.email), “unsubscribed”, 1).
- Otherwise.
  - Evaluate Platform.db.set\_value(“Email Campaign”, email\_campaign.name, “status”, “Unsubscribed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0429.json#L6609) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1184)

<a id="op-f0aad80ca5ceb2"></a>
### Set email campaign status

`operation_enterprise_customer_relationship_management_record_definitions_email_campaign_business_behavior_set_email_campaign_status`

**Inputs** no declared parameters.

**Record and data access** read “Email Campaign” via get\_all · resolve a document from “Email Campaign” via get\_doc.

**Local steps**

- Set email\_campaigns from Platform.get\_all(“Email Campaign”, filters = mapping(“status” → tuple(“!=”, “Unsubscribed”)), pluck = “name”).
- For each name in email\_campaigns.
  - Set email\_campaign from Platform.get\_doc(“Email Campaign”, name).
  - Evaluate email\_campaign.refresh\_end\_date().
  - Evaluate email\_campaign.update\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1183)

## Report · First response time for opportunity

<a id="op-536a6a5261f1cd"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_first_response_time_for_opportunity_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set columns from list(mapping(“fieldname” → “creation\_date”, “label” → translated “Date”, “fieldtype” → “Date”, “width” → 300), mapping(“fieldname” → “first\_response\_time”, “fieldtype” → “Duration”, “label” → translated “F ….
- Set opportunity from Platform.qb.DocType(“Opportunity”).
- Set creation\_date from Date(opportunity.creation).
- Set data from nested operand in the contract(nested operand in the contract).groupby(creation\_date).orderby(creation\_date, order = Order.desc).run().
- Return tuple(columns, data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1293)

<a id="op-00dee37c5416a2"></a>
### Get permitted opportunities

`operation_enterprise_binding_enterprise_crm_report_first_response_time_for_opportunity_first_response_time_for_opportunity_get_permitted_opportunities`

**Inputs** filters.

**Explicit results** Platform.qb.get\_query(“Opportunity”, filters = query\_filters, ignore\_permissions = false).

**Local steps**

- Set query\_filters from mapping(“company” → filters.company) when filters.get(“company”), otherwise mapping().
  - Value choice on filters.get(“company”) — true gives mapping(“company” → filters.company), false gives mapping().
- Return Platform.qb.get\_query(“Opportunity”, filters = query\_filters, ignore\_permissions = false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L558)

## Record · Lead

[Record definition](../../../../data/record-types/lead.json)

<a id="op-730f3ea2981e55"></a>
### Lead.onload

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_onload`

**Inputs** self.

**Record and data access** read “Customer” via get\_value.

**Local steps**

- Set customer from Platform.db.get\_value(“Customer”, mapping(“lead\_name” → self.name)).
- Set self.get(“\_\_onload”).is\_customer from customer.
- Evaluate load\_address\_and\_contact(self).
- Evaluate self.set\_onload(“linked\_prospects”, self.get\_linked\_prospects()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get linked prospects](operations-007.md#op-420fcd46cce264).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L2157) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1211)

<a id="op-4f44d9edb28225"></a>
### Lead.validate

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_validate`

**Inputs** self.

**Local steps**

- If self.lead\_owner equals “Guest”.
  - Set self.lead\_owner from no value.
- Evaluate self.set\_full\_name().
- Evaluate self.set\_lead\_name().
- Evaluate self.set\_title().
- Evaluate self.set\_status().
- Evaluate self.check\_email\_id\_is\_unique().
- Evaluate self.validate\_email\_id().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set full name](operations-006.md#op-c0e68f70142993), [set lead name](operations-006.md#op-5b05fe68c2129f), [set title](operations-006.md#op-9e1e23fa1cf02f), [set status](operations-006.md#op-92a0fe185bd677), [check email id is unique](operations-006.md#op-a5b0a686005361), [validate email id](operations-006.md#op-8032e2c30e723f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1217)

<a id="op-92a0fe185bd677"></a>
### Lead.set status

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_lead_set_status`

**Inputs** self, update = false, status = no value, update\_modified = true.

**Explicit results** no value.

**Local steps**

- <a id="op-92a0fe185bd677-guard-2"></a>If self.status equals “Do Not Contact”.
  - Return no value.
- Evaluate super().set\_status(update = update, status = status, update\_modified = update\_modified).
- If update.
  - Evaluate self.update\_prospect().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Do Not Contact”, self.status = “Do Not Contact” selects the branch that returns no value. With self.status = “Lead”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-92a0fe185bd677-guard-2)

**Methods declared on this owner** [update prospect](operations-007.md#op-9648b78deca162).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L504)

<a id="op-0c953b5ebc5479"></a>
### Lead.before insert

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_before_insert`

**Inputs** self.

**Record and data access** read “CRM Settings” via get\_single\_value · read “Dynamic Link” via get\_value · resolve a document from “Contact” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set self.contact\_doc from no value.
- If Platform.db.get\_single\_value(“CRM Settings”, “auto\_creation\_of\_contact”).
  - If (self.utm\_source equals “Existing Customer” and self.customer).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.utm\_source equals “Existing Customer” → self.customer.
    - Set contact from Platform.db.get\_value(“Dynamic Link”, mapping(“link\_doctype” → “Customer”, “parenttype” → “Contact”, “link\_name” → self.customer), “parent”).
    - If contact.
      - Set self.contact\_doc from Platform.get\_doc(“Contact”, contact).
      - Return no value.
  - Set self.contact\_doc from self.create\_contact().
- If (self.lead\_name and not any(list(self.first\_name, self.middle\_name, self.last\_name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.lead\_name → not any(list(self.first\_name, self.middle\_name, self.last\_name)).
  - Set tuple(self.first\_name, self.middle\_name, self.last\_name) from parse\_full\_name(self.lead\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create contact](operations-007.md#op-7f23b9926f1475).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “auto\_creation\_of\_contact”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L2498) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1198)

<a id="op-19126554b98c70"></a>
### Lead.after insert

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.link\_to\_contact().

If control reaches the end, it returns no value.

**Methods declared on this owner** [link to contact](operations-006.md#op-bbb8d6e46dd30d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L2955) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1197)

<a id="op-dcc55015d33703"></a>
### Lead.on update

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_prospect().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update prospect](operations-007.md#op-9648b78deca162).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L3006) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1210)

<a id="op-85a6b3f64360bd"></a>
### Lead.on trash

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_on_trash`

**Inputs** self.

**State and service calls** request set\_value on “Issue”.

**Local steps**

- Evaluate Platform.db.set\_value(“Issue”, mapping(“lead” → self.name), “lead”, no value).
- Evaluate self.delete\_contact\_and\_address().
- Evaluate self.remove\_link\_from\_prospect().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete contact and address](operations-006.md#op-3b8da740f82940), [remove link from prospect](operations-007.md#op-e1282a9ad917e8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1209)

<a id="op-3b8da740f82940"></a>
### Lead.delete contact and address

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_lead_delete_contact_and_address`

**Inputs** self.

**Record and data access** read “Dynamic Link” via get\_all · resolve a document from parenttype via get\_doc.

**Local steps**

- For each parenttype in tuple(“Contact”, “Address”).
  - Set links from Platform.get\_all(“Dynamic Link”, filters = mapping(“parenttype” → parenttype, “link\_doctype” → “Lead”, “link\_name” → self.name), pluck = “parent”).
  - For each name in links.
    - Evaluate self.unlink\_or\_delete(Platform.get\_doc(parenttype, name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [unlink or delete](operations-006.md#op-78d92f8a697f05).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1263) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L503)

<a id="op-78d92f8a697f05"></a>
### Lead.unlink or delete

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_lead_unlink_or_delete`

**Inputs** self, doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- Set doc.flags.ignore\_permissions from true.
- If len(doc.links) equals 1.
  - Evaluate doc.delete(ignore\_permissions = true).
  - Return no value.
- Set doc.links from list of link for link drawn from doc.links where tuple(link.link\_doctype, link.link\_name) differs from tuple(“Lead”, self.name).
  - Draw link from doc.links, keep a combination only if (tuple(link.link\_doctype, link.link\_name) differs from tuple(“Lead”, self.name)).
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L505)

<a id="op-c0e68f70142993"></a>
### Lead.set full name

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_set_full_name`

**Inputs** self.

**Local steps**

- If self.first\_name.
  - Set self.lead\_name from one space.join(filter(no value, list(self.salutation, self.first\_name, self.middle\_name, self.last\_name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L3215) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1213)

<a id="op-5b05fe68c2129f"></a>
### Lead.set lead name

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_set_lead_name`

**Inputs** self.

**Explicit failure paths** validation helper — translated “A Lead requires either a person's name or an organization's name”.

**Local steps**

- If not self.lead\_name.
  - If (not self.company\_name and not self.email\_id and not self.flags.ignore\_mandatory).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.company\_name → not self.email\_id → not self.flags.ignore\_mandatory.
    - Call the validation error handler Platform.throw(translated “A Lead requires either a person's name or an organization's name”).
  - Otherwise.
    - If self.company\_name.
      - Set self.lead\_name from self.company\_name.
    - Otherwise.
      - If self.email\_id.
        - Set self.lead\_name from self.email\_id.split(“@”) at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L3341) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1214)

<a id="op-9e1e23fa1cf02f"></a>
### Lead.set title

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_set_title`

**Inputs** self.

**Local steps**

- Set self.title from (self.company\_name or self.lead\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.company\_name → self.lead\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L3577) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1215)

<a id="op-a5b0a686005361"></a>
### Lead.check email id is unique

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_check_email_identifier_is_unique`

**Inputs** self.

**Record and data access** read “CRM Settings” via get\_single\_value · read “Lead” via get\_all.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “Email Address must be unique, it is already used in {0}”.format(comma\_and(duplicate\_leads)).

**Local steps**

- If self.email\_id.
  - If not Platform.db.get\_single\_value(“CRM Settings”, “allow\_lead\_duplication\_based\_on\_emails”).
    - Set duplicate\_leads from Platform.get\_all(“Lead”, filters = mapping(“email\_id” → self.email\_id, “name” → list(“!=”, self.name))).
    - Set duplicate\_leads from list of Platform.bold(get\_link\_to\_form(“Lead”, lead.name)) for lead drawn from duplicate\_leads.
      - Draw lead from duplicate\_leads.
    - If duplicate\_leads.
      - Call the validation error handler Platform.throw(translated “Email Address must be unique, it is already used in {0}”.format(comma\_and(duplicate\_leads)), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “allow\_lead\_duplication\_based\_on\_emails”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L3642) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1199)

<a id="op-8032e2c30e723f"></a>
### Lead.validate email id

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_validate_email_identifier`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Lead Owner cannot be same as the Lead Email Address”.

**Local steps**

- If self.email\_id.
  - If not self.flags.ignore\_email\_validation.
    - Evaluate validate\_email\_address(self.email\_id, throw = true).
  - If self.email\_id equals self.lead\_owner.
    - Call the validation error handler Platform.throw(translated “Lead Owner cannot be same as the Lead Email Address”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L3999) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1218)

<a id="op-bbb8d6e46dd30d"></a>
### Lead.link to contact

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_link_to_contact`

**Inputs** self.

**State and service calls** call save on self.contact\_doc.

**Local steps**

- If self.contact\_doc.
  - Evaluate self.contact\_doc.append(“links”, mapping(“link\_doctype” → “Lead”, “link\_name” → self.name, “link\_title” → self.lead\_name)).
  - Evaluate self.contact\_doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L4171) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1208)
