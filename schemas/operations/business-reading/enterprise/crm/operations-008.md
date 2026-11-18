# Sales relationships · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Lead conversion time

<a id="op-89fcb25b03e6d9"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_lead_conversion_time_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, communication\_list) · tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Set filters from mapping().
- Set communication\_list from get\_communication\_details(filters).
- Set columns from get\_columns().
- If not communication\_list.
  - Evaluate msgprint(translated “No record found”).
  - Return tuple(columns, communication\_list).
- Set data from list().
- For each communication in communication\_list.
  - Set row from list(communication.get(“customer”), communication.get(“interactions”), communication.get(“duration”), communication.get(“support\_tickets”)).
  - Evaluate data.append(row).
- Set total\_interactions from 0.
- Set total\_duration from 0.
- Set total\_tickets from 0.
- For each row in data.
  - Update total\_interactions using + row at 1.
  - Update total\_duration using + row at 2.
  - Update total\_tickets using + row at 3.
- Evaluate data.append(list(“Average”, (total\_interactions ÷ len(data)), (total\_duration ÷ len(data)), (total\_tickets ÷ len(data)))).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1294)

<a id="op-9e8080d345f264"></a>
### Get columns

`operation_enterprise_customer_relationship_management_report_lead_conversion_time_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“label” → translated “No of Interactions”, “fieldname” → “interactions”, “f ….

**Local steps**

- Return list(mapping(“label” → translated “Customer”, “fieldname” → “customer”, “fieldtype” → “Link”, “options” → “Customer”, …), mapping(“label” → translated “No of Interactions”, “fieldname” → “interactions”, “f ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0436.json#L4231) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1295)

<a id="op-bb6b8d3929ccc1"></a>
### Get communication details

`operation_enterprise_customer_relationship_management_report_lead_conversion_time_business_behavior_get_communication_details`

**Inputs** filters.

**Explicit results** communication\_list.

**Local steps**

- Set communication\_list from list().
- Set converted\_leads from set().
- For each opportunity in get\_lead\_opportunities().
  - If opportunity.party\_name belongs to converted\_leads.
    - Continue with the next iteration or loop test.
  - Set row from get\_conversion\_details(opportunity, filters).
  - If row.
    - Evaluate converted\_leads.add(opportunity.party\_name).
    - Evaluate communication\_list.append(row).
- Return communication\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1296)

<a id="op-18ec1b196bd7d4"></a>
### Get lead opportunities

`operation_enterprise_binding_enterprise_crm_report_lead_conversion_time_lead_conversion_time_get_lead_opportunities`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Record and data access** read “Opportunity” via get\_list.

**Explicit results** Platform.get\_list(“Opportunity”, filters = mapping(“opportunity\_from” → “Lead”), fields = list(“party\_name”, “customer\_name”, “contact\_email”), order\_by = “creation”).

**Local steps**

- Return Platform.get\_list(“Opportunity”, filters = mapping(“opportunity\_from” → “Lead”), fields = list(“party\_name”, “customer\_name”, “contact\_email”), order\_by = “creation”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L561)

<a id="op-9b24f9edf7e98a"></a>
### Get conversion details

`operation_enterprise_binding_enterprise_crm_report_lead_conversion_time_lead_conversion_time_get_conversion_details`

**Inputs** d, filters.

**Declared result** (dict bitwise or no value).

**Record and data access** read “Issue” via get\_all.

**Explicit results** no value · mapping(“customer” → d.customer\_name, “interactions” → communication\_count, “duration” → flt(date\_diff(invoice\_date, first\_contact)), “support\_tickets” → len(Platform.db.get\_all(“Issue”, mapping(“raised\_by ….

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set comm from Platform.qb.DocType(“Communication”).
- Set invoice from nested operand in the contract(nested operand in the contract).orderby(si.posting\_date).limit(1).run().
- If not invoice.
  - Return no value.
- Set invoice\_date from invoice at 0 at 0.
- Set communication\_count from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract ≤ nested operand in the … at 0.
- If not communication\_count.
  - Return no value.
- Set first\_contact from get\_first\_contact\_date(d.contact\_email).
- If not first\_contact.
  - Return no value.
- Return mapping(“customer” → d.customer\_name, “interactions” → communication\_count, “duration” → flt(date\_diff(invoice\_date, first\_contact)), “support\_tickets” → len(Platform.db.get\_all(“Issue”, mapping(“raised\_by ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L559)

<a id="op-3803d08b95afd9"></a>
### Get first contact date

`operation_enterprise_binding_enterprise_crm_report_lead_conversion_time_lead_conversion_time_get_first_contact_date`

**Inputs** email.

**Explicit results** communication\_date.

**Local steps**

- Set comm from Platform.qb.DocType(“Communication”).
- Set communications from nested operand in the contract(nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contra ….run().
- For each tuple(recipients, communication\_date) in communications.
  - If is\_recipient(email, recipients).
    - Return communication\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L560)

<a id="op-2474c56f3feb11"></a>
### Is recipient

`operation_enterprise_binding_enterprise_crm_report_lead_conversion_time_lead_conversion_time_is_recipient`

**Inputs** email, recipients.

**Declared result** bool.

**Explicit results** any(generator of nested operand in the contract(nested operand in the contract) at 1.lower() equals email.lower() for recipient drawn from split\_emails(recipients)).

**Local steps**

- Return any(generator of nested operand in the contract(nested operand in the contract) at 1.lower() equals email.lower() for recipient drawn from split\_emails(recipients)).
  - Draw recipient from split\_emails(recipients).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L562)

## Report · Lead details

<a id="op-07f60e1d332f5c"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_lead_details_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(get\_columns(), get\_data(filters)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1298)

<a id="op-ae3b1fb4afd255"></a>
### Get columns

`operation_enterprise_customer_relationship_management_report_lead_details_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Lead”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Lead”, …), mapping(“label” → translated “Lead Name”, “fieldname” → “lead\_name”, “fieldtype” → “Data”, “wid ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1299)

<a id="op-8c1f0f4fd4d58f"></a>
### Get data

`operation_enterprise_customer_relationship_management_report_lead_details_business_behavior_get_data`

**Inputs** filters.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set lead from Platform.qb.DocType(“Lead”).
- Set address from Platform.qb.DocType(“Address”).
- Set query from nested operand in the contract(nested operand in the contract).select(lead.name, lead.lead\_name, lead.job\_title, lead.status, …).where((lead.company equals filters.company bitwise or IfNull(nested operand  ….
- If filters.get(“territory”).
  - Set territories from list(filters.territory, expanded get\_descendants\_of(“Territory”, filters.territory)).
  - Set query from query.where(lead.territory.isin(territories)).
- If filters.get(“status”).
  - Set query from query.where(lead.status equals filters.get(“status”)).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1300)

<a id="op-ba342e7cb00de1"></a>
### Get first address

`operation_enterprise_binding_enterprise_crm_report_lead_details_lead_details_get_first_address`

**Inputs** lead.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(address.is\_primary\_address, order = Order.desc).orderby(address.creation).limit(1).

**Local steps**

- Set address from Platform.qb.DocType(“Address”).as\_(“lead\_address”).
- Set dynamic\_link from Platform.qb.DocType(“Dynamic Link”).
- Return nested operand in the contract(nested operand in the contract).orderby(address.is\_primary\_address, order = Order.desc).orderby(address.creation).limit(1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L563)

## Report · Lead owner efficiency

<a id="op-76b513543c208f"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_lead_owner_efficiency_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns().
- Set data from get\_lead\_data(filters, “Lead Owner”).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1302)

<a id="op-3487b9ea53d85d"></a>
### Get columns

`operation_enterprise_customer_relationship_management_report_lead_owner_efficiency_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “lead\_owner”, “label” → translated “Lead Owner”, “fieldtype” → “Link”, “options” → “User”, …), mapping(“fieldname” → “lead\_count”, “label” → translated “Lead Count”, “fieldtype”  ….

**Local steps**

- Return list(mapping(“fieldname” → “lead\_owner”, “label” → translated “Lead Owner”, “fieldtype” → “Link”, “options” → “User”, …), mapping(“fieldname” → “lead\_count”, “label” → translated “Lead Count”, “fieldtype”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0437.json#L3180) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1303)

## Report · Lost opportunity

<a id="op-86ca466799253b"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_lost_opportunity_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(get\_columns(), get\_data(filters)).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1304)

<a id="op-2789c6c328053a"></a>
### Get columns

`operation_enterprise_customer_relationship_management_report_lost_opportunity_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Opportunity”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Opportunity”, …), mapping(“label” → translated “Opportunity From”, “fieldname” → “opportunity\_from” ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0437.json#L5423) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1305)

<a id="op-f2f7d4b2670697"></a>
### Get data

`operation_enterprise_customer_relationship_management_report_lost_opportunity_business_behavior_get_data`

**Inputs** filters.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Set query from get\_conditions(filters, query).
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1307)

<a id="op-e659236c035f61"></a>
### Get conditions

`operation_enterprise_customer_relationship_management_report_lost_opportunity_business_behavior_get_conditions`

**Inputs** filters, query.

**Explicit results** query.

**Local steps**

- If filters.get(“territory”).
  - Set territories from list(filters.get(“territory”), expanded get\_descendants\_of(“Territory”, filters.get(“territory”))).
  - Set query from query.where(Opportunity.territory.isin(territories)).
- If filters.get(“opportunity\_from”).
  - Set query from query.where(Opportunity.opportunity\_from equals filters.get(“opportunity\_from”)).
- If filters.get(“party\_name”).
  - Set query from query.where(Opportunity.party\_name equals filters.get(“party\_name”)).
- If filters.get(“lost\_reason”).
  - Set query from query.where(Opportunity.name.isin(nested operand in the contract(nested operand in the contract).select(OpportunityLostReasonDetail.parent).where((OpportunityLostReasonDetail.parenttype equals “Opportunity ….
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1306)

## Record · Opportunity

[Record definition](../../../../data/record-types/opportunity.json)

<a id="op-389bf96c03e195"></a>
### Opportunity.onload

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).
- If (self.party\_name and Platform.has\_permission(self.opportunity\_from, “read”, self.party\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_name → Platform.has\_permission(self.opportunity\_from, “read”, self.party\_name).
  - Evaluate self.add\_party\_address\_and\_contact().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add party address and contact](operations-008.md#op-962590d4d43fbf).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.opportunity\_from, “read”, self.party\_name).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1241)

<a id="op-962590d4d43fbf"></a>
### Opportunity.add party address and contact

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_add_party_address_and_contact`

**Inputs** self.

**Record and data access** resolve a document from self.opportunity\_from via get\_doc.

**Local steps**

- Set party from Platform.get\_doc(self.opportunity\_from, self.party\_name).
- Evaluate load\_address\_and\_contact(party).
- For each key in tuple(“contact\_list”, “addr\_list”).
  - Set party\_list from party.get(“\_\_onload”).get(key).
  - Evaluate party\_list.extend(generator of entry for entry drawn from self.get(“\_\_onload”).get(key) where entry does not belong to party\_list).
    - Draw entry from self.get(“\_\_onload”).get(key), keep a combination only if (entry does not belong to party\_list).
  - Evaluate self.set\_onload(key, party\_list).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L526)

<a id="op-51111f1a30cd77"></a>
### Opportunity.after insert

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_after_insert`

**Inputs** self.

**Record and data access** resolve a document from “Lead” via get\_doc.

**Local steps**

- If self.opportunity\_from equals “Lead”.
  - Evaluate Platform.get\_doc(“Lead”, self.party\_name).set\_status(update = true).
  - Set ignore\_permissions from self.flags.ignore\_permissions.
  - Evaluate link\_open\_tasks(self.opportunity\_from, self.party\_name, self, ignore\_permissions).
  - Evaluate link\_open\_events(self.opportunity\_from, self.party\_name, self, ignore\_permissions).
- If self.opportunity\_from belongs to tuple(“Lead”, “Prospect”).
  - Evaluate self.carry\_forward\_communication().

If control reaches the end, it returns no value.

**Methods declared on this owner** [carry forward communication](operations-008.md#op-ed04b6f7fa4003).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1232)

<a id="op-ed04b6f7fa4003"></a>
### Opportunity.carry forward communication

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_carry_forward_communication`

**Inputs** self.

**Record and data access** read “CRM Settings” via get\_single\_value.

**Local steps**

- If Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).
  - Set ignore\_permissions from self.flags.ignore\_permissions.
  - Evaluate copy\_comments(self.opportunity\_from, self.party\_name, self, ignore\_permissions).
  - Evaluate link\_communications(self.opportunity\_from, self.party\_name, self, ignore\_permissions).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L528)

<a id="op-4b46928b1c68e0"></a>
### Opportunity.validate

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_opportunity\_type().
- Evaluate self.make\_new\_lead\_if\_required().
- Evaluate self.validate\_opportunity\_from().
- Evaluate self.validate\_item\_details().
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_cust\_name().
- Evaluate self.validate\_party().
- Evaluate self.validate\_party\_contact\_and\_address().
- Evaluate self.refresh\_party\_fields().
- Evaluate self.validate\_party\_specific\_items().
- Evaluate self.map\_fields().
- Evaluate self.validate\_qty().
- Evaluate self.validate\_status().
- Evaluate self.set\_lost\_on().
- Evaluate self.set\_exchange\_rate().
- If not self.title.
  - Set self.title from self.customer\_name.
- Evaluate self.calculate\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set opportunity type](operations-009.md#op-29e1802f602079), [make new lead if required](operations-009.md#op-d86e49359106b7), [validate opportunity from](operations-009.md#op-17d09e8bad9356), [validate item details](operations-010.md#op-75c4dbb2237952), [validate cust name](operations-010.md#op-532dd34b22f34f), [validate party](operations-010.md#op-14a52460e402d9), [validate party contact and address](operations-010.md#op-b0e118ca327853), [refresh party fields](operations-010.md#op-49396e903fed79), [validate party specific items](operations-009.md#op-8f1be6b75caf91), [map fields](operations-009.md#op-b7d8afb9eaad74), [validate qty](operations-009.md#op-37e4731449b5e1), [validate status](operations-009.md#op-1b1985f3ab9d52), [set lost on](operations-009.md#op-7a505c0d37ce21), [set exchange rate](operations-009.md#op-5444cae18dc62c), [calculate totals](operations-009.md#op-25e7aff6b3e151).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1245)

<a id="op-ba9d87f9d21db6"></a>
### Opportunity.on update

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_prospect().
- If self.has\_value\_changed(“status”).
  - Evaluate self.update\_lead\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update prospect](operations-009.md#op-13f4da4a59ea6b), [update lead status](operations-009.md#op-ad829b6885180e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1240)

<a id="op-a9b1304fc65b93"></a>
### Opportunity.after delete

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.update\_lead\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update lead status](operations-009.md#op-ad829b6885180e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L527)
