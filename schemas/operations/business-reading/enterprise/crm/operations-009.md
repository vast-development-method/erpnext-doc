# Sales relationships · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Opportunity

[Record definition](../../../../data/record-types/opportunity.json)

<a id="op-ad829b6885180e"></a>
### Opportunity.update lead status

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_update_lead_status`

**Inputs** self.

**Record and data access** read “Lead” via exists · resolve a document from “Lead” via get\_doc.

**Local steps**

- If (self.opportunity\_from equals “Lead” and Platform.db.exists(“Lead”, self.party\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.opportunity\_from equals “Lead” → Platform.db.exists(“Lead”, self.party\_name).
  - Evaluate Platform.get\_doc(“Lead”, self.party\_name).set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L541)

<a id="op-8f1be6b75caf91"></a>
### Opportunity.validate party specific items

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_validate_party_specific_items`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Item {1} is not allowed for {2} {3}.”.format(row.idx, Platform.bold(row.item\_code), translated “Customer”, Platform.bold(self.party\_name)).

**Local steps**

- If (self.opportunity\_from differs from “Customer” or not self.party\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.opportunity\_from differs from “Customer” → not self.party\_name.
  - Return no value.
- Bind dependencies get\_allowed\_items\_condition.
- Set allowed\_items\_condition from get\_allowed\_items\_condition(“Customer”, self.party\_name).
- If allowed\_items\_condition is identical to no value.
  - Return no value.
- Set rows from list of row for row drawn from self.get(“items”) where row.item\_code.
  - Draw row from self.get(“items”), keep a combination only if (row.item\_code).
- Set item from Platform.qb.DocType(“Item”).
- Set allowed\_items from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(nested operand in the contract(nested operand in the contract))).where(allowed\_items\_condition).run( ….
  - Draw row from rows.
- For each row in rows.
  - If row.item\_code does not belong to allowed\_items.
    - Call the validation error handler Platform.throw(translated “Row {0}: Item {1} is not allowed for {2} {3}.”.format(row.idx, Platform.bold(row.item\_code), translated “Customer”, Platform.bold(self.party\_name)), title = translated “Item Rest ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L544)

<a id="op-30b3a6a085c293"></a>
### Opportunity.on trash

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_on_trash`

**Inputs** self.

**State and service calls** request delete on “Prospect Opportunity”.

**Local steps**

- Evaluate Platform.db.delete(“Prospect Opportunity”, mapping(“opportunity” → self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L536)

<a id="op-17d09e8bad9356"></a>
### Opportunity.validate opportunity from

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_validate_opportunity_from`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Opportunity From must be one of {0}”.format(comma\_or(list of translated d for d drawn from PARTY\_DOCTYPES)).

**Local steps**

- If self.opportunity\_from does not belong to PARTY\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Opportunity From must be one of {0}”.format(comma\_or(list of translated d for d drawn from PARTY\_DOCTYPES))).
    - Draw d from PARTY\_DOCTYPES.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L542)

<a id="op-37e4731449b5e1"></a>
### Opportunity.validate qty

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_validate_quantity`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Quantity must be greater than 0 for Item {1}”.format(item.idx, item.item\_code).

**Local steps**

- For each item in self.items.
  - If flt(item.qty) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Quantity must be greater than 0 for Item {1}”.format(item.idx, item.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0432.json#L6041) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1249)

<a id="op-1b1985f3ab9d52"></a>
### Opportunity.validate status

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_validate_status`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or not self.has\_value\_changed(“status”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.has\_value\_changed(“status”).
  - Return no value.
- Evaluate self.validate\_status\_against\_quotations(self.get\_quotation\_status()).
- Set previous from self.get\_doc\_before\_save().
- If (previous and previous.status equals “Lost”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.status equals “Lost”.
  - Set self.lost\_reasons from list().
  - Set self.order\_lost\_reason from no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate status against quotations](operations-009.md#op-b4cf4e8f397bec), [get quotation status](operations-009.md#op-53910b3af56027).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L545)

<a id="op-b4cf4e8f397bec"></a>
### Opportunity.validate status against quotations

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_validate_status_against_quotations`

**Inputs** self, quotation\_status.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Cannot declare as Lost because an active Quotation exists.” · validation helper — translated “Status {0} is set from the Opportunity's Quotations”.format(Platform.bold(translated self.status)) · validation helper — translated “Status cannot be changed because an ordered Quotation exists.”.

**Local steps**

- If (self.status equals “Lost” and quotation\_status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Lost” → quotation\_status.
  - Call the validation error handler Platform.throw(translated “Cannot declare as Lost because an active Quotation exists.”).
- If (self.status belongs to tuple(“Quotation”, “Converted”) and self.status differs from quotation\_status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status belongs to tuple(“Quotation”, “Converted”) → self.status differs from quotation\_status.
  - Call the validation error handler Platform.throw(translated “Status {0} is set from the Opportunity's Quotations”.format(Platform.bold(translated self.status))).
- If (quotation\_status equals “Converted” and self.status differs from “Converted”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in quotation\_status equals “Converted” → self.status differs from “Converted”.
  - Call the validation error handler Platform.throw(translated “Status cannot be changed because an ordered Quotation exists.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L546)

<a id="op-53910b3af56027"></a>
### Opportunity.get quotation status

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_get_quotation_status`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** “Converted” · “Quotation”.

**Local steps**

- If self.has\_ordered\_quotation().
  - Return “Converted”.
- If self.has\_active\_quotation().
  - Return “Quotation”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [has ordered quotation](operations-009.md#op-e37fab25663587), [has active quotation](operations-009.md#op-5909bc3c18924e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L531)

<a id="op-7a505c0d37ce21"></a>
### Opportunity.set lost on

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_set_lost_on`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If self.has\_value\_changed(“status”).
  - Set self.lost\_on from self.get\_lost\_on().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get lost on](operations-009.md#op-736d125f1dc180).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L539)

<a id="op-736d125f1dc180"></a>
### Opportunity.get lost on

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_get_lost_on`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** today() when self.status equals “Lost”, otherwise no value.

**Local steps**

- Return today() when self.status equals “Lost”, otherwise no value.
  - Value choice on self.status equals “Lost” — true gives today(), false gives no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L530)

<a id="op-76878922eaaa4a"></a>
### Opportunity.set status

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_set_status`

**Inputs** self, update = false, status = no value, update\_modified = true.

**State and service calls** call db\_set on self.

**Local steps**

- Set previous\_status from self.status.
- Evaluate super().set\_status(update = update, status = status, update\_modified = update\_modified).
- If (update and self.status differs from previous\_status).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in update → self.status differs from previous\_status.
  - Evaluate self.db\_set(“lost\_on”, self.get\_lost\_on(), update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get lost on](operations-009.md#op-736d125f1dc180).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L540)

<a id="op-b7d8afb9eaad74"></a>
### Opportunity.map fields

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_map_fields`

**Inputs** self.

**Record and data access** read self.opportunity\_from via get\_value.

**Local steps**

- For each field in self.meta.get\_valid\_columns().
  - If (not self.get(field) and Platform.db.field\_exists(self.opportunity\_from, field)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(field) → Platform.db.field\_exists(self.opportunity\_from, field).
    - Attempt the following.
      - Set value from Platform.db.get\_value(self.opportunity\_from, self.party\_name, field).
      - Evaluate self.set(field, value).
    - On failure (Exception).
      - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0432.json#L6205) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1239)

<a id="op-29e1802f602079"></a>
### Opportunity.set opportunity type

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_set_opportunity_type`

**Inputs** self.

**Local steps**

- If (self.is\_new() and not self.opportunity\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → not self.opportunity\_type.
  - Set self.opportunity\_type from “Sales”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1243)

<a id="op-5444cae18dc62c"></a>
### Opportunity.set exchange rate

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_set_exchange_rate`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set company\_currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
- If self.currency equals company\_currency.
  - Set self.conversion\_rate from 1.0.
  - Return no value.
- If (not self.conversion\_rate or self.conversion\_rate equals 1.0 or self.is\_currency\_changed\_alone()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.conversion\_rate → self.conversion\_rate equals 1.0 → self.is\_currency\_changed\_alone().
  - Set self.conversion\_rate from get\_exchange\_rate(self.currency, company\_currency, self.transaction\_date, “for\_selling”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is currency changed alone](operations-009.md#op-9f18c64552eb3f).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1242)

<a id="op-9f18c64552eb3f"></a>
### Opportunity.is currency changed alone

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_is_currency_changed_alone`

**Inputs** self.

**Declared result** bool.

**Explicit results** (not self.is\_new() and self.has\_value\_changed(“currency”) and not self.has\_value\_changed(“conversion\_rate”)).

**Local steps**

- Return (not self.is\_new() and self.has\_value\_changed(“currency”) and not self.has\_value\_changed(“conversion\_rate”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“currency”) → not self.has\_value\_changed(“conversion\_rate”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L534)

<a id="op-25e7aff6b3e151"></a>
### Opportunity.calculate totals

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_calculate_totals`

**Inputs** self.

**Local steps**

- Set total, base\_total from 0.
- For each item in self.get(“items”).
  - Set item.amount from (flt(item.rate) × flt(item.qty)).
  - Set item.base\_rate from (flt(self.conversion\_rate) × flt(item.rate)).
  - Set item.base\_amount from (flt(self.conversion\_rate) × flt(item.amount)).
  - Update total using + item.amount.
  - Update base\_total using + item.base\_amount.
- Set self.total from flt(total).
- Set self.base\_total from flt(base\_total).
- Set self.base\_opportunity\_amount from (flt(self.opportunity\_amount) × flt(self.conversion\_rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1233)

<a id="op-13f4da4a59ea6b"></a>
### Opportunity.update prospect

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_update_prospect`

**Inputs** self.

**Record and data access** resolve a document from “Prospect” via get\_doc.

**State and service calls** call db\_update on d · call save on prospect.

**Local steps**

- Set prospect\_name from get\_party\_prospect(self.opportunity\_from, self.party\_name).
- Evaluate self.remove\_from\_previous\_prospect(prospect\_name).
- If prospect\_name.
  - Set prospect from Platform.get\_doc(“Prospect”, prospect\_name).
  - Set opportunity\_values from mapping(“opportunity” → self.name, “amount” → self.opportunity\_amount, “stage” → self.sales\_stage, “deal\_owner” → self.opportunity\_owner, …).
  - Set opportunity\_already\_added from false.
  - For each d in prospect.get(“opportunities”, list()).
    - If d.opportunity equals self.name.
      - Set opportunity\_already\_added from true.
      - Evaluate d.update(opportunity\_values).
      - Evaluate d.db\_update().
  - If not opportunity\_already\_added.
    - Evaluate prospect.append(“opportunities”, opportunity\_values).
    - Set prospect.flags.ignore\_permissions from true.
    - Set prospect.flags.ignore\_mandatory from true.
    - Evaluate prospect.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove from previous prospect](operations-009.md#op-a4220a8858ae35).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1244)

<a id="op-a4220a8858ae35"></a>
### Opportunity.remove from previous prospect

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_remove_from_previous_prospect`

**Inputs** self, prospect\_name.

**State and service calls** request delete on “Prospect Opportunity”.

**Explicit results** no value.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Return no value.
- Set previous\_prospect from get\_party\_prospect(previous.opportunity\_from, previous.party\_name).
- If (previous\_prospect and previous\_prospect differs from prospect\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_prospect → previous\_prospect differs from prospect\_name.
  - Evaluate Platform.db.delete(“Prospect Opportunity”, mapping(“opportunity” → self.name, “parenttype” → “Prospect”, “parent” → previous\_prospect)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L538)

<a id="op-d86e49359106b7"></a>
### Opportunity.make new lead if required

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_make_new_lead_if_required`

**Inputs** self.

**Record and data access** read “Lead” via get\_value · resolve a document from mapping(“doctype” → “Lead”, “email\_id” → self.contact\_email, “lead\_name” → (sender\_name or “Unknown”)) via get\_doc.

**State and service calls** call insert on lead.

**Explicit results** no value.

**Local steps**

- If (not self.get(“party\_name”) and self.contact\_email).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“party\_name”) → self.contact\_email.
  - Set tuple(dynamic\_link, contact) from tuple(DocType(“Dynamic Link”), DocType(“Contact”)).
  - Set customer from nested operand in the contract(nested operand in the contract).select(dynamic\_link.link\_name).distinct().run(as\_dict = true).
  - If (customer and customer at 0.link\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in customer → customer at 0.link\_name.
    - Set self.party\_name from customer at 0.link\_name.
    - Set self.opportunity\_from from “Customer”.
    - Return no value.
  - Set lead\_name from Platform.db.get\_value(“Lead”, mapping(“email\_id” → self.contact\_email)).
  - If not lead\_name.
    - Set sender\_name from get\_fullname(self.contact\_email).
    - If sender\_name equals self.contact\_email.
      - Set sender\_name from no value.
    - If (not sender\_name and “@” belongs to self.contact\_email).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not sender\_name → “@” belongs to self.contact\_email.
      - Set email\_name from self.contact\_email.split(“@”) at 0.
      - Set email\_split from email\_name.split(“.”).
      - Set sender\_name from empty text.
      - For each s in email\_split.
        - Update sender\_name using + (s.capitalize() + one space).
    - Set lead from Platform.get\_doc(mapping(“doctype” → “Lead”, “email\_id” → self.contact\_email, “lead\_name” → (sender\_name or “Unknown”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in sender\_name → “Unknown”.
    - Set lead.flags.ignore\_email\_validation from true.
    - Evaluate lead.insert(ignore\_permissions = true).
    - Set lead\_name from lead.name.
  - Set self.opportunity\_from from “Lead”.
  - Set self.party\_name from lead\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0433.json#L684) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1238)

<a id="op-5ba1d3d17b18b7"></a>
### Opportunity.declare enquiry lost

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_declare_enquiry_lost`

**Inputs** self, lost\_reasons\_list, competitors, detailed\_reason = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit failure paths** validation helper — translated “Please select at least one Lost Reason” · validation helper — translated “Cannot declare as Lost because an active Quotation exists.”.

**Local steps**

- If not self.has\_active\_quotation().
  - If not lost\_reasons\_list.
    - Call the validation error handler Platform.throw(translated “Please select at least one Lost Reason”).
  - Set self.status from “Lost”.
  - Set self.lost\_reasons from list().
  - Set self.competitors from list().
  - If detailed\_reason.
    - Set self.order\_lost\_reason from detailed\_reason.
  - For each reason in lost\_reasons\_list.
    - Evaluate self.append(“lost\_reasons”, reason).
  - For each competitor in competitors.
    - Evaluate self.append(“competitors”, competitor).
  - Evaluate self.save().
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Cannot declare as Lost because an active Quotation exists.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has active quotation](operations-009.md#op-5909bc3c18924e).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1234)

<a id="op-5909bc3c18924e"></a>
### Opportunity.has active quotation

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_has_active_quotation`

**Inputs** self.

**Declared result** list at str.

**Explicit results** self.get\_linked\_quotations((quotation.docstatus equals 1 bitwise and quotation.status.notin(list(“Lost”, “Cancelled”, “Expired”)))).

**Local steps**

- Set quotation from Platform.qb.DocType(“Quotation”).
- Return self.get\_linked\_quotations((quotation.docstatus equals 1 bitwise and quotation.status.notin(list(“Lost”, “Cancelled”, “Expired”)))).

**Methods declared on this owner** [get linked quotations](operations-009.md#op-68053f8bf79418).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1235)

<a id="op-e37fab25663587"></a>
### Opportunity.has ordered quotation

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_has_ordered_quotation`

**Inputs** self.

**Declared result** list at str.

**Explicit results** self.get\_linked\_quotations((quotation.docstatus equals 1 bitwise and quotation.status.isin(list(“Ordered”, “Partially Ordered”)))).

**Local steps**

- Set quotation from Platform.qb.DocType(“Quotation”).
- Return self.get\_linked\_quotations((quotation.docstatus equals 1 bitwise and quotation.status.isin(list(“Ordered”, “Partially Ordered”)))).

**Methods declared on this owner** [get linked quotations](operations-009.md#op-68053f8bf79418).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1237)

<a id="op-68053f8bf79418"></a>
### Opportunity.get linked quotations

`operation_enterprise_binding_enterprise_crm_doctype_opportunity_opportunity_opportunity_get_linked_quotations`

**Inputs** self, condition.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).distinct().where((condition bitwise and (nested operand in the contract.opportunity equals nested operand in the contract.name bitwise or nest ….

**Local steps**

- Set quotation from Platform.qb.DocType(“Quotation”).
- Set quotation\_item from Platform.qb.DocType(“Quotation Item”).
- Return nested operand in the contract(nested operand in the contract).distinct().where((condition bitwise and (nested operand in the contract.opportunity equals nested operand in the contract.name bitwise or nest ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L529)

<a id="op-8cc3eae751cf19"></a>
### Opportunity.has lost quotation

`operation_enterprise_customer_relationship_management_record_definitions_opportunity_business_behavior_opportunity_has_lost_quotation`

**Inputs** self.

**Record and data access** execute query text (SELECT, Quotation).

**Explicit results** false · true.

**Local steps**

- Set lost\_quotation from Platform.db.sql(query text (SELECT, Quotation), self.name).
- If lost\_quotation.
  - If self.has\_active\_quotation().
    - Return false.
  - Return true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [has active quotation](operations-009.md#op-5909bc3c18924e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1236)
