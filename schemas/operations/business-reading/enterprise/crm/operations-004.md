# Sales relationships · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Campaign efficiency

<a id="op-02cf8f8138fb56"></a>
### Get order amount

`operation_enterprise_customer_relationship_management_report_campaign_efficiency_business_behavior_get_order_amount`

**Inputs** leads, customers.

**Explicit results** nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract(nested operand in the c ….

**Local steps**

- Set so\_item from Platform.qb.DocType(“Sales Order Item”).
- Set quotation from Platform.qb.DocType(“Quotation”).
- Set party\_condition from (quotation.quotation\_to equals “Lead” bitwise and quotation.party\_name.isin(leads)).
- If customers.
  - Update party\_condition using bitwise or (quotation.quotation\_to equals “Customer” bitwise and quotation.party\_name.isin(customers)).
- Return nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract(nested operand in the c ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1290)

## Record · Contract

[Record definition](../../../../data/record-types/contract.json)

<a id="op-457d8131fd07f7"></a>
### Contract.validate

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_missing\_values().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_signature().
- Evaluate self.validate\_document\_party().
- Evaluate self.update\_contract\_status().
- Evaluate self.update\_fulfilment\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set missing values](operations-004.md#op-a7a6b7a8552633), [validate dates](operations-004.md#op-7b0886aa4e1964), [validate signature](operations-004.md#op-a1ef457d548be3), [validate document party](operations-004.md#op-e58f02382508e8), [update contract status](operations-004.md#op-62a10e5c1d9167), [update fulfilment status](operations-004.md#op-f7a5e32249af98).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1147)

<a id="op-a7a6b7a8552633"></a>
### Contract.set missing values

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_set_missing_values`

**Inputs** self.

**Record and data access** read self.party\_type via get\_value.

**Local steps**

- If (not self.party\_full\_name or self.has\_value\_changed(“party\_name”) or self.has\_value\_changed(“party\_type”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.party\_full\_name → self.has\_value\_changed(“party\_name”) → self.has\_value\_changed(“party\_type”).
  - Set field from (self.party\_type.lower() + “\_name”).
  - If res bound to Platform.db.get\_value(self.party\_type, self.party\_name, field).
    - Set self.party\_full\_name from res.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1144)

<a id="op-e8c320f4cd2c61"></a>
### Contract.before submit

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_before_submit`

**Inputs** self.

**Local steps**

- Set self.signed\_by\_company from Platform.session.user.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L3825) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1140)

<a id="op-c5ce5ece087b76"></a>
### Contract.on discard

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L3880) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1143)

<a id="op-8927ae6d5aef69"></a>
### Contract.on cancel

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contract_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L481)

<a id="op-8f3a0e7ede02b1"></a>
### Contract.before update after submit

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_before_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_signature().
- Evaluate self.validate\_signature\_unchanged().
- Evaluate self.validate\_fulfilment\_terms\_unchanged().
- Evaluate self.update\_contract\_status().
- Evaluate self.update\_fulfilment\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate signature](operations-004.md#op-a1ef457d548be3), [validate signature unchanged](operations-004.md#op-1fa3d32132317e), [validate fulfilment terms unchanged](operations-004.md#op-246cb75cefe47b), [update contract status](operations-004.md#op-62a10e5c1d9167), [update fulfilment status](operations-004.md#op-f7a5e32249af98).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1141)

<a id="op-e58f02382508e8"></a>
### Contract.validate document party

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contract_validate_document_party`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} {1} is for {2} {3}, not {4}”.format(translated self.document\_type, Platform.bold(self.document\_name), translated self.party\_type, Platform.bold(party), …).

**Local steps**

- If (not (self.document\_type and self.document\_name) or self.party\_type equals “Employee”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (self.document\_type and self.document\_name) → self.party\_type equals “Employee”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.document\_type → self.document\_name.
  - Return no value.
- Set party from self.get\_document\_party().
- If (party and party differs from self.party\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party → party differs from self.party\_name.
  - Call the validation error handler Platform.throw(translated “{0} {1} is for {2} {3}, not {4}”.format(translated self.document\_type, Platform.bold(self.document\_name), translated self.party\_type, Platform.bold(party), …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get document party](operations-004.md#op-3bafe743735cc6).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L482)

<a id="op-3bafe743735cc6"></a>
### Contract.get document party

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contract_get_document_party`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read “Quotation” via get\_value · read self.document\_type via get\_value.

**Explicit results** party when quotation\_to equals self.party\_type, otherwise no value · Platform.db.get\_value(self.document\_type, self.document\_name, field).

**Local steps**

- If self.document\_type equals “Quotation”.
  - Set tuple(quotation\_to, party) from Platform.db.get\_value(“Quotation”, self.document\_name, list(“quotation\_to”, “party\_name”)).
  - Return party when quotation\_to equals self.party\_type, otherwise no value.
    - Value choice on quotation\_to equals self.party\_type — true gives party, false gives no value.
- Set field from Platform.scrub(self.party\_type).
- If Platform.get\_meta(self.document\_type).has\_field(field).
  - Return Platform.db.get\_value(self.document\_type, self.document\_name, field).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L480)

<a id="op-a1ef457d548be3"></a>
### Contract.validate signature

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contract_validate_signature`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Signee and Signed On are required for a signed contract.”.

**Local steps**

- If (self.is\_signed and not (self.signee and self.signed\_on)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_signed → not (self.signee and self.signed\_on).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.signee → self.signed\_on.
  - Call the validation error handler Platform.throw(translated “Signee and Signed On are required for a signed contract.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L484)

<a id="op-1fa3d32132317e"></a>
### Contract.validate signature unchanged

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contract_validate_signature_unchanged`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.UpdateAfterSubmitError — translated “The signature of a signed contract cannot be changed. Amend the contract instead.”.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not (previous and previous.is\_signed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.is\_signed.
  - Return no value.
- If (not self.is\_signed or (previous.signee and self.signee differs from previous.signee) or (previous.signed\_on and get\_datetime(self.signed\_on) differs from get\_datetime(previous.signed\_on))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_signed → (previous.signee and self.signee differs from previous.signee) → (previous.signed\_on and get\_datetime(self.signed\_on) differs from get\_datetime(previous.signed\_on)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous.signee → self.signee differs from previous.signee.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous.signed\_on → get\_datetime(self.signed\_on) differs from get\_datetime(previous.signed\_on).
  - Call the validation error handler Platform.throw(translated “The signature of a signed contract cannot be changed. Amend the contract instead.”, Platform.UpdateAfterSubmitError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L187) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L485)

<a id="op-246cb75cefe47b"></a>
### Contract.validate fulfilment terms unchanged

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contract_validate_fulfilment_terms_unchanged`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.UpdateAfterSubmitError — translated “Fulfilment terms cannot be added or removed after submission.”.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If (previous and set of row.name for row drawn from previous.fulfilment\_terms differs from set of row.name for row drawn from self.fulfilment\_terms).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → set of row.name for row drawn from previous.fulfilment\_terms differs from set of row.name for row drawn from self.fulfilment\_terms.
  - Draw row from previous.fulfilment\_terms.
  - Draw row from self.fulfilment\_terms.
  - Call the validation error handler Platform.throw(translated “Fulfilment terms cannot be added or removed after submission.”, Platform.UpdateAfterSubmitError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L483)

<a id="op-7b0886aa4e1964"></a>
### Contract.validate dates

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “End Date cannot be before Start Date.”.

**Local steps**

- If (self.start\_date and self.end\_date and getdate(self.end\_date) &lt; getdate(self.start\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.start\_date → self.end\_date → getdate(self.end\_date) &lt; getdate(self.start\_date).
  - Call the validation error handler Platform.throw(translated “End Date cannot be before Start Date.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1148)

<a id="op-62a10e5c1d9167"></a>
### Contract.update contract status

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_update_contract_status`

**Inputs** self.

**Local steps**

- If self.is\_signed.
  - Set self.status from get\_status(self.start\_date, self.end\_date).
- Otherwise.
  - Set self.status from “Unsigned”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L4128) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1145)

<a id="op-f7a5e32249af98"></a>
### Contract.update fulfilment status

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_update_fulfilment_status`

**Inputs** self.

**Local steps**

- Set fulfilment\_status from “N/A”.
- If self.requires\_fulfilment.
  - Set fulfilment\_progress from self.get\_fulfilment\_progress().
  - If not fulfilment\_progress.
    - Set fulfilment\_status from “Unfulfilled”.
  - Otherwise.
    - If fulfilment\_progress &lt; len(self.fulfilment\_terms).
      - Set fulfilment\_status from “Partially Fulfilled”.
    - Otherwise.
      - If fulfilment\_progress equals len(self.fulfilment\_terms).
        - Set fulfilment\_status from “Fulfilled”.
  - If (fulfilment\_status differs from “Fulfilled” and self.fulfilment\_deadline).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fulfilment\_status differs from “Fulfilled” → self.fulfilment\_deadline.
    - Set now\_date from getdate(nowdate()).
    - Set deadline\_date from getdate(self.fulfilment\_deadline).
    - If now\_date &gt; deadline\_date.
      - Set fulfilment\_status from “Lapsed”.
- Set self.fulfilment\_status from fulfilment\_status.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get fulfilment progress](operations-004.md#op-fc4f73896a1578).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L4234) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1146)

<a id="op-fc4f73896a1578"></a>
### Contract.get fulfilment progress

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_contract_get_fulfilment_progress`

**Inputs** self.

**Explicit results** len(list of term for term drawn from self.fulfilment\_terms where term.fulfilled).

**Local steps**

- Return len(list of term for term drawn from self.fulfilment\_terms where term.fulfilled).
  - Draw term from self.fulfilment\_terms, keep a combination only if (term.fulfilled).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0428.json#L4603) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1142)

<a id="op-984f9c47f2cd9f"></a>
### Contract Party Access.initialize

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contractpartyaccess_init`

**Inputs** self, user = no value.

**Local steps**

- Set self.user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set self.meta from Platform.get\_meta(“Contract”).
- Set self.all\_party\_types from self.meta.get\_field(“party\_type”).options.split(whitespace '\\n').
- Set self.party\_types from self.get\_party\_types().
- Set self.allowed\_parties from mapping of party\_type → self.get\_allowed\_parties(party\_type) for party\_type drawn from self.party\_types.
  - Draw party\_type from self.party\_types.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party types](operations-004.md#op-78c6d8be7bc56e), [get allowed parties](operations-004.md#op-0c065b12dc3dda).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1251) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L491)

<a id="op-6c3154bf48d0d4"></a>
### Contract Party Access.has access

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contractpartyaccess_has_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, party\_type, party\_name.

**Explicit result forms** Boolean false, Boolean true, a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L490)

<a id="op-65cd4f1b24de00"></a>
### Contract Party Access.get criterion

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contractpartyaccess_get_criterion`

**Inputs** self.

**Declared result** (Criterion bitwise or no value).

**Explicit results** no value · contract.name.isnull() · Criterion.any(list of self.get\_party\_criterion(contract, party\_type) for party\_type drawn from self.party\_types).

**Local steps**

- If (self.party\_types equals self.all\_party\_types and not any(self.allowed\_parties.values())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_types equals self.all\_party\_types → not any(self.allowed\_parties.values()).
  - Return no value.
- Set contract from Platform.qb.DocType(“Contract”).
- If not self.party\_types.
  - Return contract.name.isnull().
- Return Criterion.any(list of self.get\_party\_criterion(contract, party\_type) for party\_type drawn from self.party\_types).
  - Draw party\_type from self.party\_types.

**Methods declared on this owner** [get party criterion](operations-004.md#op-44453085b05d0a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L189) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L487)

<a id="op-44453085b05d0a"></a>
### Contract Party Access.get party criterion

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contractpartyaccess_get_party_criterion`

**Inputs** self, contract, party\_type.

**Declared result** Criterion.

**Explicit results** criterion.

**Local steps**

- Set criterion from contract.party\_type equals party\_type.
- If allowed\_parties bound to self.allowed\_parties at party\_type.
  - Update criterion using bitwise and contract.party\_name.isin(allowed\_parties).
- Return criterion.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L488)

<a id="op-78c6d8be7bc56e"></a>
### Contract Party Access.get party types

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contractpartyaccess_get_party_types`

**Inputs** self.

**Declared result** list at str.

**Explicit results** self.all\_party\_types · list of party\_type for party\_type drawn from self.all\_party\_types where party\_type belongs to party\_types.

**Local steps**

- Set roles from set of permission.role for permission drawn from get\_valid\_perms(“Contract”, user = self.user).
  - Draw permission from get\_valid\_perms(“Contract”, user = self.user).
- If (self.user equals “Administrator” or not roles or (roles − ROLE\_PARTY\_TYPES.keys())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.user equals “Administrator” → not roles → (roles − ROLE\_PARTY\_TYPES.keys()).
  - Return self.all\_party\_types.
- Set party\_types from set of ROLE\_PARTY\_TYPES at role for role drawn from roles.
  - Draw role from roles.
- Return list of party\_type for party\_type drawn from self.all\_party\_types where party\_type belongs to party\_types.
  - Draw party\_type from self.all\_party\_types, keep a combination only if (party\_type belongs to party\_types).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L191) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L489)

<a id="op-0c065b12dc3dda"></a>
### Contract Party Access.get allowed parties

`operation_enterprise_binding_enterprise_crm_doctype_contract_contract_contractpartyaccess_get_allowed_parties`

**Inputs** self, party\_type.

**Declared result** list at str.

**Explicit results** list() · filter\_allowed\_docs\_for\_doctype(user\_permissions, “Contract”, with\_default\_doc = false).

**Local steps**

- If self.meta.get\_field(“party\_name”).ignore\_user\_permissions.
  - Return list().
- Set user\_permissions from get\_user\_permissions(self.user).get(party\_type, list()).
- Return filter\_allowed\_docs\_for\_doctype(user\_permissions, “Contract”, with\_default\_doc = false).

**Values supplied outside this operation** effective access from get\_user\_permissions(self.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L486)

<a id="op-6820f4a053f9e2"></a>
### Get status

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_get_status`

**Inputs** start\_date, end\_date.

**Explicit results** “Inactive” · “Active”.

**Local steps**

- Set now\_date from getdate(nowdate()).
- If (start\_date and getdate(start\_date) &gt; now\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_date → getdate(start\_date) &gt; now\_date.
  - Return “Inactive”.
- If (end\_date and getdate(end\_date) &lt; now\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_date → getdate(end\_date) &lt; now\_date.
  - Return “Inactive”.
- Return “Active”.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1149)

<a id="op-5f1b20e730b73c"></a>
### Update status for contracts

`operation_enterprise_customer_relationship_management_record_definitions_contract_business_behavior_update_status_for_contracts`

**Inputs** no declared parameters.

**Record and data access** read “Contract” via get\_all.

**State and service calls** request set\_value on “Contract”.

**Local steps**

- Set contracts from Platform.get\_all(“Contract”, filters = mapping(“is\_signed” → true, “docstatus” → 1), fields = list(“name”, “start\_date”, “end\_date”)).
- For each contract in contracts.
  - Set status from get\_status(contract.get(“start\_date”), contract.get(“end\_date”)).
  - Evaluate Platform.db.set\_value(“Contract”, contract.get(“name”), “status”, status).
- Evaluate set\_lapsed\_fulfilment\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1150)
