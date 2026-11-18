# Sales relationships · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Platform crm api

<a id="op-dd61f35fb8e226"></a>
### Is crm installed

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_is_customer_relationship_installed`

**Inputs** no declared parameters.

**Explicit results** “crm” belongs to Platform.get\_installed\_apps().

**Local steps**

- Return “crm” belongs to Platform.get\_installed\_apps().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0435.json#L5355) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1026)

<a id="op-4bf1ce44c035aa"></a>
### Remove allowed users on crm install

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_remove_allowed_users_on_customer_relationship_install`

**Inputs** no declared parameters.

**Record and data access** read “CRM Settings” via get\_single.

**State and service calls** call save on CRMSettings.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Set CRMSettings from Platform.get\_single(“CRM Settings”).
  - If not CRMSettings.enable\_Platform\_crm\_data\_synchronization.
    - Return no value.
  - Set CRMSettings.allowed\_users from list().
  - Evaluate CRMSettings.save().
  - Evaluate click.secho(“Removed 'Allowed Users' from CRM Settings.”).
- On failure (Exception).
  - Evaluate click.secho(“'Allowed Users' from CRM Settings couldn't be cleared.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0435.json#L5408) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1028)

<a id="op-3d07889002cd68"></a>
### Disable Platform crm data synchronization on crm uninstall

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_disable_foundation_customer_relationship_data_synchronization_on_customer_relationship_uninstall`

**Inputs** no declared parameters.

**Record and data access** read “CRM Settings” via get\_single.

**State and service calls** call save on CRMSettings.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Set CRMSettings from Platform.get\_single(“CRM Settings”).
  - If not CRMSettings.enable\_Platform\_crm\_data\_synchronization.
    - Return no value.
  - Set CRMSettings.enable\_Platform\_crm\_data\_synchronization from 0.
  - Evaluate CRMSettings.save().
  - Evaluate click.secho(“'Enable Platform CRM Data Synchronization' on CRM Settings has been disabled.”).
- On failure (Exception).
  - Evaluate click.secho(“'Enable Platform CRM Data Synchronization' on CRM Settings could not be disabled.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0435.json#L5591) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1025)

## Record · Prospect

[Record definition](../../../../data/record-types/prospect.json)

<a id="op-4fd21db479257d"></a>
### Prospect.onload

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_prospect_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0434.json#L4236) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1277)

<a id="op-bc4f1221c7a2ea"></a>
### Prospect.validate

`operation_enterprise_binding_enterprise_crm_doctype_prospect_prospect_prospect_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_leads().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate leads](operations-012.md#op-25c782bcbfd0a0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L549)

<a id="op-25c782bcbfd0a0"></a>
### Prospect.validate leads

`operation_enterprise_binding_enterprise_crm_doctype_prospect_prospect_prospect_validate_leads`

**Inputs** self.

**Record and data access** read “Prospect Lead” via get\_value.

**Explicit failure paths** validation helper — translated “Lead {0} is added more than once”.format(Platform.bold(lead)).

**Local steps**

- Set leads from list of row.lead for row drawn from self.leads.
  - Draw row from self.leads.
- For each lead in set(leads).
  - If leads.count(lead) &gt; 1.
    - Call the validation error handler Platform.throw(translated “Lead {0} is added more than once”.format(Platform.bold(lead))).
  - If other bound to Platform.db.get\_value(“Prospect Lead”, mapping(“lead” → lead, “parent” → list(“!=”, self.name)), “parent”).
    - Evaluate self.throw\_lead\_in\_other\_prospect(lead, other).

If control reaches the end, it returns no value.

**Methods declared on this owner** [throw lead in other prospect](operations-012.md#op-b0bfa58b91c2a7).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L550)

<a id="op-b0bfa58b91c2a7"></a>
### Prospect.throw lead in other prospect

`operation_enterprise_binding_enterprise_crm_doctype_prospect_prospect_prospect_throw_lead_in_other_prospect`

**Inputs** self, lead, other.

**Explicit failure paths** validation helper — message.

**Local steps**

- Set message from translated “Lead {0} is already in another Prospect”.format(Platform.bold(lead)).
- If Platform.has\_permission(“Prospect”, “read”, other).
  - Set message from translated “Lead {0} is already in Prospect {1}”.format(Platform.bold(lead), Platform.bold(other)).
- Call the validation error handler Platform.throw(message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Prospect”, “read”, other).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L548)

<a id="op-878dbb192bf160"></a>
### Prospect.on update

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_prospect_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.link\_with\_lead\_contact\_and\_address().

If control reaches the end, it returns no value.

**Methods declared on this owner** [link with lead contact and address](operations-012.md#op-9c1f595f9f0749).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0434.json#L4288) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1276)

<a id="op-34e20cbb091522"></a>
### Prospect.on trash

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_prospect_on_trash`

**Inputs** self.

**Local steps**

- Evaluate delete\_contact\_and\_address(self.doctype, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0434.json#L4339) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1275)

<a id="op-c36589b8301cb3"></a>
### Prospect.after insert

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_prospect_after_insert`

**Inputs** self.

**Record and data access** read “CRM Settings” via get\_single\_value.

**Local steps**

- Set carry\_forward\_communication\_and\_comments from Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).
- Set ignore\_permissions from self.flags.ignore\_permissions.
- For each row in self.get(“leads”).
  - If carry\_forward\_communication\_and\_comments.
    - Evaluate copy\_comments(“Lead”, row.lead, self, ignore\_permissions).
    - Evaluate link\_communications(“Lead”, row.lead, self, ignore\_permissions).
  - Evaluate link\_open\_events(“Lead”, row.lead, self, ignore\_permissions).
- For each row in self.get(“opportunities”).
  - If carry\_forward\_communication\_and\_comments.
    - Evaluate copy\_comments(“Opportunity”, row.opportunity, self, ignore\_permissions).
    - Evaluate link\_communications(“Opportunity”, row.opportunity, self, ignore\_permissions).
  - Evaluate link\_open\_events(“Opportunity”, row.opportunity, self, ignore\_permissions).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1273)

<a id="op-9c1f595f9f0749"></a>
### Prospect.link with lead contact and address

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_prospect_link_with_lead_contact_and_address`

**Inputs** self.

**Record and data access** read “Dynamic Link” via get\_all · resolve a document from link at “parenttype” via get\_doc.

**State and service calls** call save on linked\_doc.

**Local steps**

- For each row in self.leads.
  - Set links from Platform.get\_all(“Dynamic Link”, filters = mapping(“link\_doctype” → “Lead”, “link\_name” → row.lead), fields = list(“parent”, “parenttype”)).
  - For each link in links.
    - Set linked\_doc from Platform.get\_doc(link at “parenttype”, link at “parent”).
    - Set exists from false.
    - For each d in linked\_doc.get(“links”).
      - If (d.link\_doctype equals self.doctype and d.link\_name equals self.name).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.link\_doctype equals self.doctype → d.link\_name equals self.name.
        - Set exists from true.
    - If not exists.
      - Evaluate linked\_doc.append(“links”, mapping(“link\_doctype” → self.doctype, “link\_name” → self.name)).
      - Evaluate linked\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0434.json#L4800) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1274)

<a id="op-c8be48e54b1ae2"></a>
### Make customer

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_make_customer`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Evaluate validate\_not\_converted(source\_name).
- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Prospect”, source\_name, mapping(“Prospect” → mapping(“doctype” → “Customer”, “field\_map” → mapping(“company\_name” → “customer\_name”, “currency” → “default\_currency”, “fax” → “fax”))), targe ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1269)

<a id="op-b750b399b7ba0d"></a>
### Make customer.set missing values

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_make_customer_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Customer” via exists.

**Local steps**

- Set target.customer\_type from “Company”.
- Set target.company\_name from source.name.
- Set target.customer\_group from (source.customer\_group or Platform.db.get\_default(“Customer Group”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.customer\_group → Platform.db.get\_default(“Customer Group”).
- If (len(source.leads) equals 1 and not Platform.db.exists(“Customer”, mapping(“lead\_name” → nested operand in the contract.leads at 0.lead))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(source.leads) equals 1 → not Platform.db.exists(“Customer”, mapping(“lead\_name” → source.leads at 0.lead)).
  - Set target.lead\_name from source.leads at 0.lead.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1270)

<a id="op-ff2ea44fe777fa"></a>
### Validate not converted

`operation_enterprise_binding_enterprise_crm_doctype_prospect_prospect_validate_not_converted`

**Inputs** prospect.

**Declared result** no value.

**Record and data access** read “Customer” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- Evaluate Platform.has\_permission(“Prospect”, “read”, prospect, throw = true).
- Evaluate Platform.has\_permission(“Customer”, “create”, throw = true).
- Set customer from Platform.db.exists(“Customer”, mapping(“prospect\_name” → prospect)).
- If not customer.
  - Return no value.
- Set message from translated “Prospect {0} is already converted to a Customer”.format(Platform.bold(prospect)).
- If Platform.has\_permission(“Customer”, “read”, customer).
  - Set message from translated “Prospect {0} is already converted to Customer {1}”.format(Platform.bold(prospect), Platform.bold(customer)).
- Call the validation error handler Platform.throw(message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Prospect”, “read”, prospect, throw = true), Platform.has\_permission(“Customer”, “create”, throw = true) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L551)

<a id="op-4029018a60d27b"></a>
### Make opportunity

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_make_opportunity`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Prospect”, source\_name, mapping(“Prospect” → mapping(“doctype” → “Opportunity”, “field\_map” → mapping(“name” → “party\_name”, “prospect\_owner” → “opportunity\_owner”))), target\_doc, ignore\_pe ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1271)

<a id="op-91fe5c12ed1d75"></a>
### Make opportunity.set missing values

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_make_opportunity_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.opportunity\_from from “Prospect”.
- Set target.customer\_name from source.company\_name.
- Set target.customer\_group from (source.customer\_group or Platform.db.get\_default(“Customer Group”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.customer\_group → Platform.db.get\_default(“Customer Group”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0434.json#L6302) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1272)

<a id="op-792b94bc3a2bc4"></a>
### Get opportunities

`operation_enterprise_customer_relationship_management_record_definitions_prospect_business_behavior_get_opportunities`

**Inputs** prospect.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Opportunity” via get\_list.

**Explicit results** Platform.get\_list(“Opportunity”, filters = mapping(“opportunity\_from” → “Prospect”, “party\_name” → prospect), fields = list(“opportunity\_owner”, “sales\_stage”, “status”, “expected\_closing”, …)).

**Local steps**

- Return Platform.get\_list(“Opportunity”, filters = mapping(“opportunity\_from” → “Prospect”, “party\_name” → prospect), fields = list(“opportunity\_owner”, “sales\_stage”, “status”, “expected\_closing”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1268)

## Report · Prospects engaged but not converted

<a id="op-9e3ee6eb4c5977"></a>
### Execute

`operation_enterprise_customer_relationship_management_report_prospects_engaged_but_not_converted_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set tuple(columns, data) from tuple(list(), list()).
- Evaluate set\_defaut\_value\_for\_filters(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0439.json#L456) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L24) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1327)

<a id="op-840b61f3734302"></a>
### Set defaut value for filters

`operation_enterprise_customer_relationship_management_report_prospects_engaged_but_not_converted_business_behavior_set_defaut_value_for_filters`

**Inputs** filters.

**Local steps**

- If not filters.get(“no\_of\_interaction”).
  - Set filters at “no\_of\_interaction” from 1.
- If not filters.get(“lead\_age”).
  - Set filters at “lead\_age” from 60.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0439.json#L607) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L29) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1332)

<a id="op-d7df491c1f812e"></a>
### Get columns

`operation_enterprise_customer_relationship_management_report_prospects_engaged_but_not_converted_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Lead”, “fieldname” → “lead”, “fieldtype” → “Link”, “options” → “Lead”, …), mapping(“label” → translated “Name”, “fieldname” → “name”, “width” → 120), mapping(“label” → tr ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L25) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1328)

<a id="op-1f80319ed7108a"></a>
### Get data

`operation_enterprise_customer_relationship_management_report_prospects_engaged_but_not_converted_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Lead” via get\_list.

**Explicit results** lead\_details.

**Local steps**

- Set lead\_details from list().
- Set leads from Platform.get\_list(“Lead”, fields = list(“name”, “lead\_name”, “company\_name”), filters = get\_lead\_filters(filters)).
- If not leads.
  - Return lead\_details.
- Set references from get\_references(list of lead.name for lead drawn from leads).
  - Draw lead from leads.
- Set limit from cint(filters.get(“no\_of\_interaction”)).
- For each lead in leads.
  - For each communication in get\_received\_communications(references at lead.name, limit).
    - Evaluate lead\_details.append(list(lead.name, lead.lead\_name, lead.company\_name, expanded communication)).
- Return lead\_details.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L27) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1330)

<a id="op-81fb37134a173c"></a>
### Get references

`operation_enterprise_binding_enterprise_crm_report_prospects_engaged_but_not_converted_prospects_engaged_but_not_converted_get_references`

**Inputs** lead\_names.

**Declared result** dict.

**Explicit results** references.

**Local steps**

- Set references from mapping of name → mapping(“Lead” → set(name)) for name drawn from lead\_names.
  - Draw name from lead\_names.
- For each tuple(doctype, lead\_field, filters) in REFERENCE\_DOCTYPES.
  - Set filters from mapping(expand filters, lead\_field → list(“in”, lead\_names)).
  - For each row in get\_readable(doctype, filters, list(“name”, lead\_field)).
    - Evaluate references at row at lead\_field.setdefault(doctype, set()).add(row.name).
- Return references.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L570)

<a id="op-eee1e3cf9c8db3"></a>
### Get received communications

`operation_enterprise_binding_enterprise_crm_report_prospects_engaged_but_not_converted_prospects_engaged_but_not_converted_get_received_communications`

**Inputs** references, limit.

**Declared result** list.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(communication.creation, order = Order.desc).limit(limit).run().

**Local steps**

- Set communication from Platform.qb.DocType(“Communication”).
- Set matches from list of (communication.reference\_doctype equals doctype bitwise and communication.reference\_name.isin(list(names))) for tuple(doctype, names) drawn from references.items().
  - Draw tuple(doctype, names) from references.items().
- Return nested operand in the contract(nested operand in the contract).orderby(communication.creation, order = Order.desc).limit(limit).run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L569)

<a id="op-62df98e2ef41b4"></a>
### Get readable

`operation_enterprise_binding_enterprise_crm_report_prospects_engaged_but_not_converted_prospects_engaged_but_not_converted_get_readable`

**Inputs** doctype, filters, fields.

**Declared result** list.

**Record and data access** read doctype via get\_list.

**Explicit results** list() · Platform.get\_list(doctype, filters = filters, fields = fields).

**Local steps**

- If not Platform.has\_permission(doctype, “read”).
  - Return list().
- Return Platform.get\_list(doctype, filters = filters, fields = fields).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L568)
