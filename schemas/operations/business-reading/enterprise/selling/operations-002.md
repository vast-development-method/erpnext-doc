# Sales · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Customer

[Record definition](../../../../data/record-types/customer.json)

<a id="op-1b8f53c64c61d2"></a>
### Customer.check customer group change

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_check_customer_group_change`

**Inputs** self.

**Record and data access** read “Customer” via get\_value.

**Local steps**

- Set Platform.flags.customer\_group\_changed from false.
- If not self.get(“\_\_islocal”).
  - If self.customer\_group differs from Platform.db.get\_value(“Customer”, self.name, “customer\_group”).
    - Set Platform.flags.customer\_group\_changed from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L4047) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1134)

<a id="op-64fd096a0bde3d"></a>
### Customer.validate default bank account

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_validate_default_bank_account`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_value.

**Explicit failure paths** validation helper — translated “{0} is not a company bank account”.format(Platform.bold(self.default\_bank\_account)).

**Local steps**

- If self.default\_bank\_account.
  - Set is\_company\_account from Platform.db.get\_value(“Bank Account”, self.default\_bank\_account, “is\_company\_account”).
  - If not is\_company\_account.
    - Call the validation error handler Platform.throw(translated “{0} is not a company bank account”.format(Platform.bold(self.default\_bank\_account))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L4220) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1151)

<a id="op-696417dcf1e52d"></a>
### Customer.validate internal customer

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_validate_internal_customer`

**Inputs** self.

**Record and data access** read “Customer” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Internal Customer {0} already exists for {1}. Disable it to make this Customer internal.”.format(internal\_customer\_link, Platform.bold(self.represents\_company)).

**Local steps**

- If not self.is\_internal\_customer.
  - Set self.represents\_company from empty text.
  - Return no value.
- If self.disabled.
  - Return no value.
- Set internal\_customer from Platform.db.get\_value(“Customer”, mapping(“is\_internal\_customer” → 1, “represents\_company” → self.represents\_company, “disabled” → 0, “name” → tuple(“!=”, self.name)), “name”).
- If internal\_customer.
  - Set internal\_customer\_link from get\_link\_to\_form(“Customer”, internal\_customer).
  - Call the validation error handler Platform.throw(translated “Internal Customer {0} already exists for {1}. Disable it to make this Customer internal.”.format(internal\_customer\_link, Platform.bold(self.represents\_company)), title = translat ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1152)

<a id="op-28182f20cf7f4c"></a>
### Customer.validate primary contact and address

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_validate_primary_contact_and_address`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} {1} is not linked to Customer {2}”.format(translated doctype, Platform.bold(name), Platform.bold(self.name)).

**Local steps**

- For each tuple(fieldname, doctype) in tuple(tuple(“customer\_primary\_contact”, “Contact”), tuple(“customer\_primary\_address”, “Address”)).
  - Set name from self.get(fieldname).
  - If (name and self.has\_value\_changed(fieldname) and not self.is\_linked\_to\_self(doctype, name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in name → self.has\_value\_changed(fieldname) → not self.is\_linked\_to\_self(doctype, name).
    - Call the validation error handler Platform.throw(translated “{0} {1} is not linked to Customer {2}”.format(translated doctype, Platform.bold(name), Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is linked to self](operations-002.md#op-aed40e10704764).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1433)

<a id="op-aed40e10704764"></a>
### Customer.is linked to self

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_is_linked_to_self`

**Inputs** self, doctype, name.

**Record and data access** read “Dynamic Link” via get\_all.

**Explicit results** any(generator of tuple(link.link\_doctype, link.link\_name) belongs to allowed\_links for link drawn from links).

**Local steps**

- Set allowed\_links from set(tuple(“Customer”, self.name)).
- If self.is\_new().
  - Update allowed\_links using bitwise or set(tuple(“Lead”, self.lead\_name), tuple(“Opportunity”, self.opportunity\_name), tuple(“Prospect”, self.prospect\_name)).
- Set links from Platform.get\_all(“Dynamic Link”, filters = mapping(“parenttype” → doctype, “parent” → name), fields = list(“link\_doctype”, “link\_name”)).
- Return any(generator of tuple(link.link\_doctype, link.link\_name) belongs to allowed\_links for link drawn from links).
  - Draw link from links.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1428)

<a id="op-19d3decb85d446"></a>
### Customer.on update

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_name\_with\_customer\_group().
- Evaluate self.create\_primary\_contact().
- Evaluate self.create\_primary\_address().
- If self.flags.old\_lead differs from self.lead\_name.
  - Evaluate self.update\_lead\_status().
- If self.flags.is\_new\_doc.
  - Evaluate self.link\_address\_and\_contact().
  - Evaluate self.copy\_communication().
- Evaluate self.update\_customer\_groups().
- Evaluate link\_portal\_users\_to\_contacts(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate name with customer group](operations-002.md#op-f539c05ee23d69), [create primary contact](operations-002.md#op-7183785f63c33c), [create primary address](operations-002.md#op-a9290e07849239), [update lead status](operations-002.md#op-602c282df814a7), [link address and contact](operations-002.md#op-cc82572dc77c09), [copy communication](operations-002.md#op-3a8d4d09f97432), [update customer groups](operations-002.md#op-58bc245e29ac79).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L4746) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1143)

<a id="op-7611bc8595a9dc"></a>
### Customer.add role for user

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_add_role_for_user`

**Inputs** self.

**Local steps**

- For each portal\_user in self.portal\_users.
  - Evaluate add\_role\_for\_portal\_user(portal\_user, “Customer”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L4990) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1129)

<a id="op-58bc245e29ac79"></a>
### Customer.update customer groups

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_update_customer_groups`

**Inputs** self.

**Local steps**

- Set ignore\_doctypes from list(“Lead”, “Opportunity”, “POS Profile”, “Tax Rule”, …).
- If Platform.flags.customer\_group\_changed.
  - Evaluate update\_linked\_doctypes(“Customer”, self.name, “Customer Group”, self.customer\_group, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L5070) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1146)

<a id="op-7183785f63c33c"></a>
### Customer.create primary contact

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_create_primary_contact`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If (not self.customer\_primary\_contact and not self.lead\_has\_contact()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.customer\_primary\_contact → not self.lead\_has\_contact().
  - If (self.mobile\_no or self.email\_id or self.first\_name or self.last\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mobile\_no → self.email\_id → self.first\_name → self.last\_name.
    - Set contact from make\_contact(self).
    - Evaluate self.db\_set(“customer\_primary\_contact”, contact.name).
    - Evaluate self.db\_set(“mobile\_no”, self.mobile\_no).
    - Evaluate self.db\_set(“email\_id”, self.email\_id).
- Otherwise.
  - If self.customer\_primary\_contact.
    - Evaluate Platform.set\_value(“Contact”, self.customer\_primary\_contact, “is\_primary\_contact”, 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [lead has contact](operations-002.md#op-e7e51be3f2aab0).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1137)

<a id="op-e7e51be3f2aab0"></a>
### Customer.lead has contact

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_lead_has_contact`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Dynamic Link” via exists.

**Explicit results** bool((self.lead\_name and Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → “Contact”, “link\_doctype” → “Lead”, “link\_name” → self.lead\_name)))).

**Local steps**

- Return bool((self.lead\_name and Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → “Contact”, “link\_doctype” → “Lead”, “link\_name” → self.lead\_name)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.lead\_name → Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → “Contact”, “link\_doctype” → “Lead”, “link\_name” → self.lead\_name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1429)

<a id="op-a9290e07849239"></a>
### Customer.create primary address

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_create_primary_address`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies get\_address\_display.
- If (self.flags.is\_new\_doc and self.get(“address\_line1”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags.is\_new\_doc → self.get(“address\_line1”).
  - Set address from make\_address(self).
  - Set address\_display from get\_address\_display(address.name).
  - Evaluate self.db\_set(“customer\_primary\_address”, address.name).
  - Evaluate self.db\_set(“primary\_address”, address\_display).
- Otherwise.
  - If self.customer\_primary\_address.
    - Evaluate Platform.set\_value(“Address”, self.customer\_primary\_address, “is\_primary\_address”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L5546) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1136)

<a id="op-602c282df814a7"></a>
### Customer.update lead status

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_update_lead_status`

**Inputs** self.

**Record and data access** resolve a document from “Lead” via get\_doc.

**State and service calls** call db\_set on lead.

**Explicit results** no value.

**Local steps**

- If not self.lead\_name.
  - Return no value.
- Set lead from Platform.get\_doc(“Lead”, self.lead\_name).
- Evaluate lead.db\_set(“status”, “Converted”).
- Evaluate lead.update\_prospect().
- For each tuple(doctype, party\_type\_field) in tuple(tuple(“Quotation”, “quotation\_to”), tuple(“Opportunity”, “opportunity\_from”)).
  - Evaluate self.link\_lead\_records(doctype, party\_type\_field).

If control reaches the end, it returns no value.

**Methods declared on this owner** [link lead records](operations-002.md#op-d58e471e5da3fc).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1147)

<a id="op-d58e471e5da3fc"></a>
### Customer.link lead records

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_link_lead_records`

**Inputs** self, doctype, party\_type\_field.

**Record and data access** read doctype via get\_all.

**State and service calls** request set\_value on doctype.

**Local steps**

- Set names from list of name for name drawn from Platform.get\_all(doctype, mapping(party\_type\_field → “Lead”, “party\_name” → self.lead\_name), pluck = “name”) where Platform.has\_permission(doctype, “write”, name).
  - Draw name from Platform.get\_all(doctype, mapping(party\_type\_field → “Lead”, “party\_name” → self.lead\_name), pluck = “name”), keep a combination only if (Platform.has\_permission(doctype, “write”, name)).
- If names.
  - Evaluate Platform.db.set\_value(doctype, mapping(“name” → tuple(“in”, names), party\_type\_field → “Lead”, “party\_name” → self.lead\_name), mapping(party\_type\_field → “Customer”, “party\_name” → self.name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “write”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1430)

<a id="op-cc82572dc77c09"></a>
### Customer.link address and contact

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_link_address_and_contact`

**Inputs** self.

**Record and data access** read “Dynamic Link” via get\_all · resolve a document from row.doctype via get\_doc.

**State and service calls** call save on linked\_doc.

**Local steps**

- Set linked\_documents from mapping(“Lead” → self.lead\_name, “Opportunity” → self.opportunity\_name, “Prospect” → self.prospect\_name).
- For each tuple(doctype, docname) in linked\_documents.items().
  - If not docname.
    - Continue with the next iteration or loop test.
  - Set linked\_contacts\_and\_addresses from Platform.get\_all(“Dynamic Link”, filters = list(list(“parenttype”, “in”, list(“Contact”, “Address”)), list(“link\_doctype”, “=”, doctype), list(“link\_name”, “=”, docname)), fields = list(“parent as name”, “ ….
  - For each row in linked\_contacts\_and\_addresses.
    - Set linked\_doc from Platform.get\_doc(row.doctype, row.name).
    - If not linked\_doc.has\_link(“Customer”, self.name).
      - Evaluate linked\_doc.append(“links”, dict(link\_doctype = “Customer”, link\_name = self.name)).
      - Evaluate linked\_doc.save(ignore\_permissions = self.flags.ignore\_permissions).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L5926) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1140)

<a id="op-3a8d4d09f97432"></a>
### Customer.copy communication

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_copy_communication`

**Inputs** self.

**Record and data access** read “CRM Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If (not self.lead\_name or not Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.lead\_name → not Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).
  - Return no value.
- Bind dependencies copy\_comments, link\_communications.
- Evaluate copy\_comments(“Lead”, self.lead\_name, self, self.flags.ignore\_permissions).
- Evaluate link\_communications(“Lead”, self.lead\_name, self, self.flags.ignore\_permissions).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“CRM Settings”, “carry\_forward\_communication\_and\_comments”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1135)

<a id="op-f539c05ee23d69"></a>
### Customer.validate name with customer group

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_validate_name_with_customer_group`

**Inputs** self, name = no value.

**Record and data access** read “Customer Group” via exists.

**Explicit failure paths** validation helper with Platform.NameError — translated “A Customer Group exists with same name please change the Customer name or rename the Customer Group”.

**Local steps**

- If Platform.db.exists(“Customer Group”, (name or self.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → self.name.
  - Call the validation error handler Platform.throw(translated “A Customer Group exists with same name please change the Customer name or rename the Customer Group”, Platform.NameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1153)

<a id="op-3ac6513d6e705f"></a>
### Customer.validate prospect not converted

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_validate_prospect_not_converted`

**Inputs** self.

**Record and data access** read “Customer” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — message.

**Local steps**

- If not (self.is\_new() and self.prospect\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.prospect\_name.
  - Return no value.
- Set customer from Platform.db.exists(“Customer”, mapping(“prospect\_name” → self.prospect\_name)).
- If not customer.
  - Return no value.
- Set message from translated “Prospect {0} is already converted to a Customer”.format(Platform.bold(self.prospect\_name)).
- If Platform.has\_permission(“Customer”, “read”, customer).
  - Set message from translated “Prospect {0} is already converted to Customer {1}”.format(Platform.bold(self.prospect\_name), get\_link\_to\_form(“Customer”, customer)).
- Call the validation error handler Platform.throw(message, Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, “read”, customer).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1434)

<a id="op-62775a1a79e0ca"></a>
### Customer.validate customer group

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_validate_customer_group`

**Inputs** self.

**Record and data access** read “Customer Group” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot select a Group type Customer Group. Please select a non-group Customer Group.”.

**Local steps**

- If not self.customer\_group.
  - Return no value.
- Set is\_group from Platform.db.get\_value(“Customer Group”, self.customer\_group, “is\_group”).
- If is\_group.
  - Call the validation error handler Platform.throw(translated “Cannot select a Group type Customer Group. Please select a non-group Customer Group.”, title = translated “Invalid Customer Group”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0624.json#L6750) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1150)

<a id="op-865bd6d2ed3189"></a>
### Customer.validate duplicate credit limit company

`operation_enterprise_binding_enterprise_selling_doctype_customer_customer_customer_validate_duplicate_credit_limit_company`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Credit limit is already defined for the Company {0}”.format(limit.company).

**Local steps**

- Set companies from set().
- For each limit in self.credit\_limits.
  - If limit.company belongs to companies.
    - Call the validation error handler Platform.throw(translated “Credit limit is already defined for the Company {0}”.format(limit.company)).
  - Evaluate companies.add(limit.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1431)

<a id="op-e735d420c0b315"></a>
### Customer.validate credit limit on change

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_validate_credit_limit_on_change`

**Inputs** self.

**Record and data access** read “Customer Credit Limit” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “New credit limit is less than current outstanding amount for the customer. Credit limit has to be atleast {0}”.format(outstanding\_amt).

**Local steps**

- If (self.get(“\_\_islocal”) or not self.credit\_limits).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_\_islocal”) → not self.credit\_limits.
  - Return no value.
- Set past\_credit\_limits from list of d.credit\_limit for d drawn from Platform.db.get\_all(“Customer Credit Limit”, filters = mapping(“parent” → self.name), fields = list(“credit\_limit”), order\_by = “company”).
  - Draw d from Platform.db.get\_all(“Customer Credit Limit”, filters = mapping(“parent” → self.name), fields = list(“credit\_limit”), order\_by = “company”).
- Set current\_credit\_limits from list of d.credit\_limit for d drawn from sorted(self.credit\_limits, key = deferred anonymous expression).
  - Draw d from sorted(self.credit\_limits, key = deferred anonymous expression).
- If past\_credit\_limits equals current\_credit\_limits.
  - Return no value.
- For each limit in self.credit\_limits.
  - If not flt(limit.credit\_limit).
    - Continue with the next iteration or loop test.
  - Set outstanding\_amt from get\_customer\_outstanding(self.name, limit.company, ignore\_outstanding\_sales\_order = limit.bypass\_credit\_limit\_check).
  - If flt(limit.credit\_limit) &lt; outstanding\_amt.
    - Call the validation error handler Platform.throw(translated “New credit limit is less than current outstanding amount for the customer. Credit limit has to be atleast {0}”.format(outstanding\_amt)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1149)

<a id="op-f02674c074816d"></a>
### Customer.on trash

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_on_trash`

**Inputs** self.

**State and service calls** call db\_set on self · execute query text (UPDATE, Lead).

**Local steps**

- If self.customer\_primary\_contact.
  - Evaluate self.db\_set(“customer\_primary\_contact”, no value).
- If self.customer\_primary\_address.
  - Evaluate self.db\_set(“customer\_primary\_address”, no value).
- Evaluate delete\_contact\_and\_address(“Customer”, self.name).
- If self.lead\_name.
  - Evaluate Platform.db.sql(query text (UPDATE, Lead), self.lead\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1142)

<a id="op-e8c19b3e83f374"></a>
### Customer.before rename

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_before_rename`

**Inputs** self, olddn, newdn, merge = false.

**Local steps**

- Evaluate self.validate\_name\_with\_customer\_group(newdn).
- If merge.
  - Evaluate validate\_party\_currency\_before\_merging(“Customer”, olddn, newdn).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate name with customer group](operations-002.md#op-f539c05ee23d69).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1133)

<a id="op-d6cc5e459780bb"></a>
### Customer.after rename

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_after_rename`

**Inputs** self, olddn, newdn, merge = false.

**State and service calls** call db\_set on self.

**Local steps**

- If Platform.defaults.get\_global\_default(“cust\_master\_name”) equals “Customer Name”.
  - Evaluate self.db\_set(“customer\_name”, newdn).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0625.json#L972) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1131)

<a id="op-bd2337e89eeb97"></a>
### Customer.set loyalty program

`operation_enterprise_selling_record_definitions_customer_business_behavior_customer_set_loyalty_program`

**Inputs** self.

**State and service calls** msgprint with translated “Multiple Loyalty Programs found for Customer {}. Please select manually.”.format(Platform.bold(self.customer\_name)).

**Explicit results** no value.

**Local steps**

- If self.loyalty\_program.
  - Return no value.
- Set loyalty\_program from get\_loyalty\_programs(self).
- If not loyalty\_program.
  - Return no value.
- If len(loyalty\_program) equals 1.
  - Set self.loyalty\_program from loyalty\_program at 0.
- Otherwise.
  - Evaluate Platform.msgprint(translated “Multiple Loyalty Programs found for Customer {}. Please select manually.”.format(Platform.bold(self.customer\_name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1145)
