# Sales relationships · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Lead

[Record definition](../../../../data/record-types/lead.json)

<a id="op-9648b78deca162"></a>
### Lead.update prospect

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_update_prospect`

**Inputs** self.

**Record and data access** read “Prospect Lead” via get\_value · resolve a document from “Prospect Lead” via get\_doc.

**State and service calls** call db\_update on lead\_row.

**Local steps**

- Set lead\_row\_name from Platform.db.get\_value(“Prospect Lead”, filters = mapping(“lead” → self.name), fieldname = “name”).
- If lead\_row\_name.
  - Set lead\_row from Platform.get\_doc(“Prospect Lead”, lead\_row\_name).
  - Evaluate lead\_row.update(mapping(“lead\_name” → self.lead\_name, “email” → self.email\_id, “mobile\_no” → self.mobile\_no, “lead\_owner” → self.lead\_owner, …)).
  - Evaluate lead\_row.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L4338) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1216)

<a id="op-e1282a9ad917e8"></a>
### Lead.remove link from prospect

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_remove_link_from_prospect`

**Inputs** self.

**Record and data access** resolve a document from “Prospect” via get\_doc.

**State and service calls** call save on prospect.

**Local steps**

- Set linked\_prospects from self.get\_linked\_prospects().
- For each linked\_prospect in linked\_prospects.
  - Set prospect from Platform.get\_doc(“Prospect”, linked\_prospect.parent).
  - Evaluate prospect.set(“leads”, list of row for row drawn from prospect.leads where row.lead differs from self.name).
    - Draw row from prospect.leads, keep a combination only if (row.lead differs from self.name).
  - Set prospect.flags.ignore\_mandatory from true.
  - Evaluate prospect.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get linked prospects](operations-007.md#op-420fcd46cce264).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1212)

<a id="op-420fcd46cce264"></a>
### Lead.get linked prospects

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_get_linked_prospects`

**Inputs** self.

**Record and data access** read “Prospect Lead” via get\_all.

**Explicit results** Platform.get\_all(“Prospect Lead”, filters = mapping(“lead” → self.name), fields = list(“parent”)).

**Local steps**

- Return Platform.get\_all(“Prospect Lead”, filters = mapping(“lead” → self.name), fields = list(“parent”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L4998) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1203)

<a id="op-65c74555f48af6"></a>
### Lead.has customer

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_has_customer`

**Inputs** self.

**Record and data access** read “Customer” via get\_value.

**Explicit results** Platform.db.get\_value(“Customer”, mapping(“lead\_name” → self.name)).

**Local steps**

- Return Platform.db.get\_value(“Customer”, mapping(“lead\_name” → self.name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L5111) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1204)

<a id="op-822845a4a62132"></a>
### Lead.has opportunity

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_has_opportunity`

**Inputs** self.

**Record and data access** read “Opportunity” via get\_value.

**Explicit results** Platform.db.get\_value(“Opportunity”, mapping(“party\_name” → self.name, “status” → list(“!=”, “Lost”))).

**Local steps**

- Return Platform.db.get\_value(“Opportunity”, mapping(“party\_name” → self.name, “status” → list(“!=”, “Lost”))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L5201) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1206)

<a id="op-2ec91b3e7c2017"></a>
### Lead.has quotation

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_has_quotation`

**Inputs** self.

**Record and data access** read “Quotation” via get\_value.

**Explicit results** Platform.db.get\_value(“Quotation”, mapping(“party\_name” → self.name, “docstatus” → 1, “status” → list(“!=”, “Lost”))).

**Local steps**

- Return Platform.db.get\_value(“Quotation”, mapping(“party\_name” → self.name, “docstatus” → 1, “status” → list(“!=”, “Lost”))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L5316) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1207)

<a id="op-42bb52d26941cf"></a>
### Lead.has lost quotation

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_has_lost_quotation`

**Inputs** self.

**Record and data access** read “Quotation” via get\_value.

**Explicit results** Platform.db.get\_value(“Quotation”, mapping(“party\_name” → self.name, “docstatus” → 1, “status” → “Lost”)).

**Local steps**

- Return Platform.db.get\_value(“Quotation”, mapping(“party\_name” → self.name, “docstatus” → 1, “status” → “Lost”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L5447) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1205)

<a id="op-9359ff4d5a5cc3"></a>
### Lead.create prospect and contact

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_create_prospect_and_contact`

**Inputs** self, data.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set data from Platform.\_dict(data).
- If data.create\_contact.
  - Set self.contact\_doc from self.create\_contact().
  - Evaluate self.link\_to\_contact().
- If data.create\_prospect.
  - Evaluate Platform.has\_permission(“Prospect”, “create”, throw = true).
  - Evaluate self.create\_prospect(data.prospect\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create contact](operations-007.md#op-7f23b9926f1475), [link to contact](operations-006.md#op-bbb8d6e46dd30d), [create prospect](operations-007.md#op-c447a42fd59b82).

**Values supplied outside this operation** effective access from self.check\_permission(“write”), Platform.has\_permission(“Prospect”, “create”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1202)

<a id="op-7f23b9926f1475"></a>
### Lead.create contact

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_create_contact`

**Inputs** self.

**State and service calls** request new\_doc for “Contact” · call insert on contact.

**Explicit results** contact.

**Local steps**

- If not self.lead\_name.
  - Evaluate self.set\_full\_name().
  - Evaluate self.set\_lead\_name().
- Set contact from Platform.new\_doc(“Contact”).
- Evaluate contact.update(mapping(“first\_name” → (self.first\_name or self.lead\_name), “last\_name” → self.last\_name, “salutation” → self.salutation, “gender” → self.gender, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.first\_name → self.lead\_name.
- If self.email\_id.
  - Evaluate contact.append(“email\_ids”, mapping(“email\_id” → self.email\_id, “is\_primary” → 1)).
- If self.phone.
  - Evaluate contact.append(“phone\_nos”, mapping(“phone” → self.phone, “is\_primary\_phone” → 1)).
- If self.mobile\_no.
  - Evaluate contact.append(“phone\_nos”, mapping(“phone” → self.mobile\_no, “is\_primary\_mobile\_no” → 1)).
- Evaluate contact.insert(ignore\_permissions = true).
- Evaluate contact.reload().
- Return contact.

**Methods declared on this owner** [set full name](operations-006.md#op-c0e68f70142993), [set lead name](operations-006.md#op-5b05fe68c2129f).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L5765) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1200)

<a id="op-c447a42fd59b82"></a>
### Lead.create prospect

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_lead_create_prospect`

**Inputs** self, company\_name.

**State and service calls** request new\_doc for “Prospect” · call save on prospect.

**Explicit failure paths** validation helper — translated “Prospect {0} already exists”.format((company\_name or self.company\_name)).

**Local steps**

- Attempt the following.
  - Set prospect from Platform.new\_doc(“Prospect”).
  - Set prospect.company\_name from (company\_name or self.company\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in company\_name → self.company\_name.
  - Set prospect.no\_of\_employees from self.no\_of\_employees.
  - Set prospect.industry from self.industry.
  - Set prospect.market\_segment from self.market\_segment.
  - Set prospect.annual\_revenue from self.annual\_revenue.
  - Set prospect.territory from self.territory.
  - Set prospect.fax from self.fax.
  - Set prospect.website from self.website.
  - Set prospect.prospect\_owner from self.lead\_owner.
  - Set prospect.company from self.company.
  - Set prospect.notes from self.notes.
  - Evaluate prospect.append(“leads”, mapping(“lead” → self.name, “lead\_name” → self.lead\_name, “email” → self.email\_id, “mobile\_no” → self.mobile\_no, …)).
  - Set prospect.flags.ignore\_permissions from true.
  - Set prospect.flags.ignore\_mandatory from true.
  - Evaluate prospect.save().
- On failure (Platform.DuplicateEntryError).
  - Call the validation error handler Platform.throw(translated “Prospect {0} already exists”.format((company\_name or self.company\_name))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in company\_name → self.company\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0430.json#L6347) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1201)

<a id="op-b630ca31067daa"></a>
### Make customer

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_customer`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_make\_customer(source\_name, target\_doc).

**Local steps**

- Evaluate validate\_lead\_is\_enabled(source\_name, “Customer”).
- Return \_make\_customer(source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1266) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L506)

<a id="op-8b7b462c50cca6"></a>
### Make customer

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_customer_3cae8beea0ff`

**Inputs** source\_name, target\_doc = no value, ignore\_permissions = false.

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Lead”, source\_name, mapping(“Lead” → mapping(“doctype” → “Customer”, “field\_map” → mapping(“name” → “lead\_name”, “company\_name” → “customer\_name”, “contact\_no” → “phone\_1”, “fax” → “fax\_1”) ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1267) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L507)

<a id="op-ebc996eae4e6f0"></a>
### Make customer.set missing values

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_customer_set_missing_values`

**Inputs** source, target.

**Local steps**

- If source.company\_name.
  - Set target.customer\_type from “Company”.
  - Set target.customer\_name from source.company\_name.
- Otherwise.
  - Set target.customer\_type from “Individual”.
  - Set target.customer\_name from source.lead\_name.
- If not target.customer\_group.
  - Set target.customer\_group from Platform.db.get\_default(“Customer Group”).
- Set address from get\_default\_address(“Lead”, source.name).
- Set contact from get\_default\_contact(“Lead”, source.name).
- If address.
  - Set target.customer\_primary\_address from address.
- If contact.
  - Set target.customer\_primary\_contact from contact.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L508)

<a id="op-470a89128c99a1"></a>
### Make opportunity

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_opportunity`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** target\_doc.

**Local steps**

- Evaluate validate\_lead\_is\_enabled(source\_name, “Opportunity”).
- Bind local operation set\_missing\_values for subsequent calls.
- Set target\_doc from get\_mapped\_doc(“Lead”, source\_name, mapping(“Lead” → mapping(“doctype” → “Opportunity”, “field\_map” → mapping(“doctype” → “opportunity\_from”, “name” → “party\_name”, “lead\_name” → “contact\_display”, “compan ….
- Return target\_doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1270) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L510)

<a id="op-74063cf6f48912"></a>
### Make opportunity.set missing values

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_opportunity_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate \_set\_missing\_values(source, target).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L511)

<a id="op-048e916e25e43f"></a>
### Make quotation

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_quotation`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** target\_doc.

**Local steps**

- Evaluate validate\_lead\_is\_enabled(source\_name, “Quotation”).
- Bind local operation set\_missing\_values for subsequent calls.
- Set target\_doc from get\_mapped\_doc(“Lead”, source\_name, mapping(“Lead” → mapping(“doctype” → “Quotation”, “field\_map” → mapping(“name” → “party\_name”))), target\_doc, …).
- Set target\_doc.quotation\_to from “Lead”.
- Evaluate target\_doc.run\_method(“set\_missing\_values”).
- Evaluate target\_doc.run\_method(“set\_other\_charges”).
- Evaluate target\_doc.run\_method(“calculate\_taxes\_and\_totals”).
- Return target\_doc.

**Values supplied outside this operation** selected callable from target\_doc.run\_method(“set\_missing\_values”), target\_doc.run\_method(“set\_other\_charges”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L512)

<a id="op-dd8e203d355537"></a>
### Make quotation.set missing values

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_quotation_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate \_set\_missing\_values(source, target).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L513)

<a id="op-2c84df1b668960"></a>
### Set missing values

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_set_missing_values`

**Inputs** source, target.

**Record and data access** read “Dynamic Link” via get\_all.

**Local steps**

- Set address from Platform.get\_all(“Dynamic Link”, mapping(“link\_doctype” → source.doctype, “link\_name” → source.name, “parenttype” → “Address”), list(“parent”), limit = 1).
- Set contact from Platform.get\_all(“Dynamic Link”, mapping(“link\_doctype” → source.doctype, “link\_name” → source.name, “parenttype” → “Contact”), list(“parent”), limit = 1).
- If address.
  - Set target.customer\_address from address at 0.parent.
- If contact.
  - Set target.contact\_person from contact at 0.parent.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L514)

<a id="op-942486817b0569"></a>
### Validate lead is enabled

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_validate_lead_is_enabled`

**Inputs** lead, doctype.

**Declared result** no value.

**Record and data access** read “Lead” via get\_value.

**Explicit failure paths** validation helper with PartyDisabled — translated “Lead {0} is disabled. Enable it to create a new {1}.”.format(lead, translated doctype).

**Local steps**

- If Platform.db.get\_value(“Lead”, lead, “disabled”).
  - Call the validation error handler Platform.throw(translated “Lead {0} is disabled. Enable it to create a new {1}.”.format(lead, translated doctype), PartyDisabled).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L515)

<a id="op-6c6a5ebfd15d69"></a>
### Get lead details

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_get_lead_details`

**Inputs** lead, posting\_date = no value, company = no value, doctype = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Lead” via get\_doc.

**Explicit results** mapping() · out.

**Local steps**

- If not lead.
  - Return mapping().
- Bind dependencies set\_address\_details.
- Set out from Platform.\_dict().
- Set lead\_doc from Platform.get\_doc(“Lead”, lead).
- Evaluate lead\_doc.check\_permission().
- Set lead from lead\_doc.
- Evaluate out.update(mapping(“territory” → lead.territory, “customer\_name” → (lead.company\_name or lead.lead\_name), “contact\_display” → one space.join(filter(no value, list(lead.lead\_name))), “contact\_email” → lead. ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in lead.company\_name → lead.lead\_name.
- Evaluate set\_address\_details(out, lead, “Lead”, doctype = doctype, company = company).
- Set taxes\_and\_charges from set\_taxes(no value, “Lead”, posting\_date, company, billing\_address = out.get(“customer\_address”), shipping\_address = out.get(“shipping\_address\_name”)).
- If taxes\_and\_charges.
  - Set out at “taxes\_and\_charges” from taxes\_and\_charges.
- Return out.

**Values supplied outside this operation** effective access from lead\_doc.check\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1196)

<a id="op-e9898381d18457"></a>
### Make lead from communication

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_make_lead_from_communication`

**Inputs** communication, ignore\_communication\_links = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Communication” via get\_doc · read “Lead” via get\_value · resolve a document from mapping(“doctype” → “Lead”, “lead\_name” → doc.sender\_full\_name, “email\_id” → doc.sender, “mobile\_no” → doc.phone\_no) via get\_doc.

**State and service calls** call insert on lead.

**Explicit results** lead\_name.

**Local steps**

- Evaluate Platform.has\_permission(“Communication”, doc = communication, throw = true).
- Evaluate Platform.has\_permission(“Lead”, ptype = “create”, throw = true).
- Set doc from Platform.get\_doc(“Communication”, communication).
- Set lead\_name from no value.
- If doc.sender.
  - Set lead\_name from Platform.db.get\_value(“Lead”, mapping(“email\_id” → doc.sender)).
- If (not lead\_name and doc.phone\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not lead\_name → doc.phone\_no.
  - Set lead\_name from Platform.db.get\_value(“Lead”, mapping(“mobile\_no” → doc.phone\_no)).
- If not lead\_name.
  - Set lead from Platform.get\_doc(mapping(“doctype” → “Lead”, “lead\_name” → doc.sender\_full\_name, “email\_id” → doc.sender, “mobile\_no” → doc.phone\_no)).
  - Set lead.flags.ignore\_mandatory from true.
  - Evaluate lead.insert().
  - Set lead\_name from lead.name.
- Evaluate link\_communication\_to\_document(doc, “Lead”, lead\_name, ignore\_communication\_links).
- Return lead\_name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Communication”, doc = communication, throw = true), Platform.has\_permission(“Lead”, ptype = “create”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L509)

<a id="op-dd33cd9da732f6"></a>
### Get leads with phone number

`operation_enterprise_binding_enterprise_crm_doctype_lead_lead_get_leads_with_phone_number`

**Inputs** number.

**Declared result** list at str.

**Record and data access** read “Lead” via get\_all.

**Explicit results** list() · list of lead.name for lead drawn from leads where any(generator of get\_phone\_number\_key(lead at field) equals key for field drawn from phone\_fields).

**Local steps**

- If not key bound to get\_phone\_number\_key(number).
  - Return list().
- Set phone\_fields from list(“phone”, “whatsapp\_no”, “mobile\_no”).
- Set pattern from get\_phone\_number\_like\_pattern(key).
- Set leads from Platform.get\_all(“Lead”, or\_filters = mapping of field → list(“like”, pattern) for field drawn from phone\_fields, fields = list(“name”, expanded phone\_fields), order\_by = “creation desc”).
  - Draw field from phone\_fields.
- Return list of lead.name for lead drawn from leads where any(generator of get\_phone\_number\_key(lead at field) equals key for field drawn from phone\_fields).
  - Draw lead from leads, keep a combination only if (any(generator of get\_phone\_number\_key(lead at field) equals key for field drawn from phone\_fields)).
  - Draw field from phone\_fields.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1262) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L502)

<a id="op-466984426599b1"></a>
### Add lead to prospect

`operation_enterprise_customer_relationship_management_record_definitions_lead_business_behavior_add_lead_to_prospect`

**Inputs** lead, prospect.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Prospect” via get\_doc · read “CRM Settings” via get\_single\_value.

**State and service calls** call save on prospect · msgprint with translated “Lead {0} has been added to prospect {1}.”.format(Platform.bold(lead), Platform.bold(prospect.name)).

**Local steps**

- If lead.
  - Evaluate Platform.has\_permission(“Lead”, “read”, lead, throw = true).
- Set prospect from Platform.get\_doc(“Prospect”, prospect).
- Evaluate prospect.append(“leads”, mapping(“lead” → lead)).
- Evaluate prospect.save().
- Set carry\_forward\_communication\_and\_comments from Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).
- If carry\_forward\_communication\_and\_comments.
  - Evaluate copy\_comments(“Lead”, lead, prospect).
  - Evaluate link\_communications(“Lead”, lead, prospect).
- Evaluate link\_open\_events(“Lead”, lead, prospect).
- Evaluate Platform.msgprint(translated “Lead {0} has been added to prospect {1}.”.format(Platform.bold(lead), Platform.bold(prospect.name)), title = translated “Lead -&gt; Prospect”, indicator = “green”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Lead”, “read”, lead, throw = true) · configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0431.json#L1028) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1195)

<a id="op-209f1fc6b0e938"></a>
### Get data

`operation_enterprise_customer_relationship_management_record_definitions_lead_lead_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “lead”, “non\_standard\_fieldnames” → mapping(“Quotation” → “party\_name”, “Opportunity” → “party\_name”), “dynamic\_links” → mapping(“party\_name” → list(“Lead”, “quotation\_to”)), “transac ….

**Local steps**

- Return mapping(“fieldname” → “lead”, “non\_standard\_fieldnames” → mapping(“Quotation” → “party\_name”, “Opportunity” → “party\_name”), “dynamic\_links” → mapping(“party\_name” → list(“Lead”, “quotation\_to”)), “transac ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0431.json#L1573) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1219)
