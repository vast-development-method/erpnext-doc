# Sales · operations 23

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Selling settings

[Record definition](../../../../data/record-types/selling_settings.json)

<a id="op-423ec68bd94baa"></a>
### Selling Settings.validate fallback to default price list

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_selling_settings_validate_fallback_to_default_price_list`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**State and service calls** msgprint with translated “You have enabled {0} and {1} in {2}. This can lead to prices from the default price list being inserted into …”.format(text in the contract.format(translated self.meta.get\_label(“fallback\_to\_de ….

**Local steps**

- If (self.fallback\_to\_default\_price\_list and self.has\_value\_changed(“fallback\_to\_default\_price\_list”) and Platform.get\_single\_value(“Stock Settings”, “auto\_insert\_price\_list\_rate\_if\_missing”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.fallback\_to\_default\_price\_list → self.has\_value\_changed(“fallback\_to\_default\_price\_list”) → Platform.get\_single\_value(“Stock Settings”, “auto\_insert\_price\_list\_rate\_if\_missing”).
  - Set stock\_meta from Platform.get\_meta(“Stock Settings”).
  - Evaluate Platform.msgprint(translated “You have enabled {0} and {1} in {2}. This can lead to prices from the default price list being inserted into …”.format(text in the contract.format(translated nested operand in ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “auto\_insert\_price\_list\_rate\_if\_missing”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1499)

<a id="op-0eaa8603d4056e"></a>
### Selling Settings.toggle hide tax id

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_selling_settings_toggle_hide_tax_identifier`

**Inputs** self.

**Local steps**

- Set \_hide\_tax\_id from cint(self.hide\_tax\_id).
- For each doctype in tuple(“Sales Order”, “Sales Invoice”, “Delivery Note”, “POS Invoice”).
  - Evaluate make\_property\_setter(doctype, “tax\_id”, “hidden”, \_hide\_tax\_id, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “tax\_id”, “print\_hide”, \_hide\_tax\_id, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1497)

<a id="op-e66a8d671e79ac"></a>
### Selling Settings.toggle editable rate for bundle items

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_selling_settings_toggle_editable_rate_for_bundle_items`

**Inputs** self.

**Local steps**

- Set editable\_bundle\_item\_rates from cint(self.editable\_bundle\_item\_rates).
- Evaluate make\_property\_setter(“Packed Item”, “rate”, “read\_only”, not editable\_bundle\_item\_rates, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1496)

<a id="op-e5abc8b26b8613"></a>
### Selling Settings.toggle discount accounting fields

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_selling_settings_toggle_discount_accounting_fields`

**Inputs** self.

**Local steps**

- Set enable\_discount\_accounting from cint(self.enable\_discount\_accounting).
- Evaluate make\_property\_setter(“Sales Invoice Item”, “discount\_account”, “hidden”, not enable\_discount\_accounting, validate\_fields\_for\_doctype = false, …).
- If enable\_discount\_accounting.
  - Evaluate make\_property\_setter(“Sales Invoice Item”, “discount\_account”, “mandatory\_depends\_on”, “eval: doc.discount\_amount”, validate\_fields\_for\_doctype = false, …).
- Otherwise.
  - Evaluate make\_property\_setter(“Sales Invoice Item”, “discount\_account”, “mandatory\_depends\_on”, empty text, validate\_fields\_for\_doctype = false, …).
- Evaluate make\_property\_setter(“Sales Invoice”, “additional\_discount\_account”, “hidden”, not enable\_discount\_accounting, validate\_fields\_for\_doctype = false, …).
- If enable\_discount\_accounting.
  - Evaluate make\_property\_setter(“Sales Invoice”, “additional\_discount\_account”, “mandatory\_depends\_on”, “eval: doc.discount\_amount”, validate\_fields\_for\_doctype = false, …).
- Otherwise.
  - Evaluate make\_property\_setter(“Sales Invoice”, “additional\_discount\_account”, “mandatory\_depends\_on”, empty text, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1495)

<a id="op-76857f7b3b5c36"></a>
### Toggle tracking sales commissions section

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_toggle_tracking_sales_commissions_section`

**Inputs** hide.

**Local steps**

- Bind dependencies create\_property\_setter\_for\_hiding\_field.
- For each tuple(doctype, sections) in COMMISSION\_SECTIONS.items().
  - For each section in sections.
    - Evaluate create\_property\_setter\_for\_hiding\_field(doctype, section, hide).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1501)

<a id="op-8aae0c14831cfe"></a>
### Toggle utm analytics section

`operation_enterprise_selling_record_definitions_selling_settings_business_behavior_toggle_campaign_tracking_analytics_section`

**Inputs** hide.

**Local steps**

- Bind dependencies create\_property\_setter\_for\_hiding\_field.
- For each doctype in UTM\_DOCTYPES.
  - Set meta from Platform.get\_meta(doctype).
  - If meta.has\_field(“utm\_analytics\_section”).
    - Evaluate create\_property\_setter\_for\_hiding\_field(doctype, “utm\_analytics\_section”, hide).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0656.json#L5728) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1500)

## Record · Sms center

<a id="op-37da0857a95bb6"></a>
### SMSCenter.create receiver list

`operation_enterprise_selling_record_definitions_sms_center_business_behavior_short_message_service_center_create_receiver_list`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- Set query from no value.
- If self.send\_to equals empty text.
  - Return no value.
- If self.send\_to belongs to list(“All Contact”, “All Customer Contact”, “All Supplier Contact”, “All Sales Partner Contact”).
  - Set query from self.get\_contact\_query\_for\_all\_contacts().
- Otherwise.
  - If self.send\_to equals “All Lead (Open)”.
    - Set query from self.get\_contact\_query\_for\_all\_open\_leads().
  - Otherwise.
    - If self.send\_to equals “All Employee (Active)”.
      - Set query from self.get\_contact\_query\_for\_all\_active\_employee().
    - Otherwise.
      - If self.send\_to equals “All Sales Person”.
        - Set query from self.get\_contact\_query\_for\_all\_sales\_person().
- Set rec from query.run(as\_list = 1).
- Set rec\_list from empty text.
- For each d in rec.
  - Update rec\_list using + (((d at 0 + “ - ”) + d at 1) + whitespace '\\n').
- Set self.receiver\_list from rec\_list.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get contact query for all contacts](operations-023.md#op-5d6cedf05999a4), [get contact query for all open leads](operations-023.md#op-d738da8227272e), [get contact query for all active employee](operations-023.md#op-4ddf9db307446f), [get contact query for all sales person](operations-023.md#op-f46bff3cfc2d82).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0656.json#L6903) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1503)

<a id="op-5d6cedf05999a4"></a>
### SMSCenter.get contact query for all contacts

`operation_enterprise_selling_record_definitions_sms_center_business_behavior_short_message_service_center_get_contact_query_for_all_contacts`

**Inputs** self.

**Explicit results** query.

**Local steps**

- Set Contact from Platform.qb.DocType(“Contact”).
- Set DynamicLink from Platform.qb.DocType(“Dynamic Link”).
- Set query from nested operand in the contract.qb.from\_(Contact).select(fn.Concat(fn.IfNull(Contact.first\_name, empty text), one space, fn.IfNull(Contact.last\_name, empty text)), Contact.mobile\_no).where((fn.IfNull(Contac ….
- <a id="op-5d6cedf05999a4-guard-14"></a>If self.send\_to equals “All Contact”.
  - Return query.
- Set query from query.join(DynamicLink).on(DynamicLink.parent equals Contact.name).distinct().
- If self.send\_to equals “All Customer Contact”.
  - Set query from query.where(DynamicLink.link\_doctype equals “Customer”).
  - Set query from query.where(DynamicLink.link\_name equals self.customer) when self.customer, otherwise query.where(fn.IfNull(DynamicLink.link\_name, empty text) differs from empty text).
    - Value choice on self.customer — true gives query.where(DynamicLink.link\_name equals self.customer), false gives query.where(fn.IfNull(DynamicLink.link\_name, empty text) differs from empty text).
- Otherwise.
  - If self.send\_to equals “All Supplier Contact”.
    - Set query from query.where(DynamicLink.link\_doctype equals “Supplier”).
    - Set query from query.where(DynamicLink.link\_name equals self.supplier) when self.supplier, otherwise query.where(fn.IfNull(DynamicLink.link\_name, empty text) differs from empty text).
      - Value choice on self.supplier — true gives query.where(DynamicLink.link\_name equals self.supplier), false gives query.where(fn.IfNull(DynamicLink.link\_name, empty text) differs from empty text).
  - Otherwise.
    - If self.send\_to equals “All Sales Partner Contact”.
      - Set query from query.where(DynamicLink.link\_doctype equals “Sales Partner”).
      - Set query from query.where(DynamicLink.link\_name equals self.sales\_partner) when self.sales\_partner, otherwise query.where(fn.IfNull(DynamicLink.link\_name, empty text) differs from empty text).
        - Value choice on self.sales\_partner — true gives query.where(DynamicLink.link\_name equals self.sales\_partner), false gives query.where(fn.IfNull(DynamicLink.link\_name, empty text) differs from empty text).
- Return query.

**Derived branch illustrations**

- At the comparison self.send\_to equals “All Contact”, self.send\_to = “All Contact” selects the branch that returns query. With self.send\_to = “All Customer Contact”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5d6cedf05999a4-guard-14)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1505)

<a id="op-d738da8227272e"></a>
### SMSCenter.get contact query for all open leads

`operation_enterprise_selling_record_definitions_sms_center_business_behavior_short_message_service_center_get_contact_query_for_all_open_leads`

**Inputs** self.

**Explicit results** query.

**Local steps**

- Set Lead from Platform.qb.DocType(“Lead”).
- Set query from nested operand in the contract.qb.from\_(Lead).select(Lead.lead\_name, Lead.mobile\_no).where(((fn.IfNull(Lead.mobile\_no, empty text) differs from empty text bitwise and Lead.docstatus differs from 2) bitwise ….
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1506)

<a id="op-4ddf9db307446f"></a>
### SMSCenter.get contact query for all active employee

`operation_enterprise_selling_record_definitions_sms_center_business_behavior_short_message_service_center_get_contact_query_for_all_active_employee`

**Inputs** self.

**Explicit results** query.

**Local steps**

- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from nested operand in the contract.qb.from\_(Employee).select(Employee.employee\_name, Employee.cell\_number).where(((Employee.status equals “Active” bitwise and Employee.docstatus differs from 2) bitwise and fn. ….
- If self.department.
  - Set query from query.where(Employee.department equals self.department).
- If self.branch.
  - Set query from query.where(Employee.branch equals self.branch).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0657.json#L1182) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1504)

<a id="op-f46bff3cfc2d82"></a>
### SMSCenter.get contact query for all sales person

`operation_enterprise_selling_record_definitions_sms_center_business_behavior_short_message_service_center_get_contact_query_for_all_sales_person`

**Inputs** self.

**Explicit results** query.

**Local steps**

- Set SalesPerson from Platform.qb.DocType(“Sales Person”).
- Set Employee from Platform.qb.DocType(“Employee”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.employee equals nested operand in the contract.name).select(SalesPerson.sales\_person\_name, Employee.cell\_num ….
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1507)

<a id="op-d8f19962e7beca"></a>
### SMSCenter.get receiver nos

`operation_enterprise_selling_record_definitions_sms_center_business_behavior_short_message_service_center_get_receiver_numbers`

**Inputs** self.

**Explicit results** receiver\_nos.

**Local steps**

- Set receiver\_nos from list().
- If self.receiver\_list.
  - For each d in self.receiver\_list.split(whitespace '\\n').
    - Set receiver\_no from d.rsplit(“ - ”, 1) at negative 1.
    - If receiver\_no.strip().
      - Evaluate receiver\_nos.append(cstr(receiver\_no).strip()).
- Otherwise.
  - Evaluate msgprint(translated “Receiver List is empty. Please create Receiver List”).
- Return receiver\_nos.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1508)

<a id="op-e13b1ceeba3d88"></a>
### SMSCenter.send sms

`operation_enterprise_selling_record_definitions_sms_center_business_behavior_short_message_service_center_send_short_message_service`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set receiver\_list from list().
- If not self.message.
  - Evaluate msgprint(translated “Please enter message before sending”).
- Otherwise.
  - Set receiver\_list from self.get\_receiver\_nos().
- If receiver\_list.
  - Evaluate send\_sms(receiver\_list, cstr(self.message)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get receiver nos](operations-023.md#op-d8f19962e7beca).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0657.json#L2101) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1509)

## Report · Territory target variance based on item group

<a id="op-22c6ee94e2c256"></a>
### Execute

`operation_enterprise_selling_report_territory_target_variance_based_on_item_group_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** get\_data\_column(filters, “Territory”).

**Local steps**

- Return get\_data\_column(filters, “Territory”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0679.json#L4157) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L219)

## Report · Territory wise sales

<a id="op-d6919d564095e2"></a>
### Execute

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set filters from Platform.\_dict(filters).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L223)

<a id="op-0976e190ac7557"></a>
### Get columns

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_get_columns`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** list(mapping(“label” → translated “Territory”, “fieldname” → “territory”, “fieldtype” → “Link”, “options” → “Territory”, …), mapping(“label” → translated “Opportunity Amount”, “fieldname” → “opportunity\_am ….

**Local steps**

- Set filters from (filters or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → Platform.\_dict().
- Set currency from get\_default\_currency().
- If filters.get(“company”).
  - Set currency from (Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”) or currency).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”) → currency.
- Return list(mapping(“label” → translated “Territory”, “fieldname” → “territory”, “fieldtype” → “Link”, “options” → “Territory”, …), mapping(“label” → translated “Opportunity Amount”, “fieldname” → “opportunity\_am ….

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L224)

<a id="op-47c8e22568f2ab"></a>
### Get data

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_get_data`

**Inputs** filters = no value.

**Record and data access** read “Territory” via get\_all.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set user\_permissions from get\_user\_permissions(Platform.session.user).
- Set opportunities from restrict(get\_opportunities(filters), “Opportunity”, filters, user\_permissions, …).
- Set quotations from restrict(get\_quotations(opportunities), “Quotation”, filters, user\_permissions, …).
- Set sales\_orders from restrict(get\_sales\_orders(quotations), “Sales Order”, filters, user\_permissions, …).
- Set sales\_invoices from restrict(get\_sales\_invoice(sales\_orders), “Sales Invoice”, filters, user\_permissions, …).
- For each territory in Platform.get\_all(“Territory”).
  - Set territory\_opportunities from list().
  - If opportunities.
    - Set territory\_opportunities from list(filter(deferred anonymous expression, opportunities)).
  - Set t\_opportunity\_names from list().
  - If territory\_opportunities.
    - Set t\_opportunity\_names from list of t.name for t drawn from territory\_opportunities.
      - Draw t from territory\_opportunities.
  - Set territory\_quotations from list().
  - If (t\_opportunity\_names and quotations).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in t\_opportunity\_names → quotations.
    - Set territory\_quotations from list(filter(deferred anonymous expression, quotations)).
  - Set t\_quotation\_names from list().
  - If territory\_quotations.
    - Set t\_quotation\_names from list of t.name for t drawn from territory\_quotations.
      - Draw t from territory\_quotations.
  - Set territory\_orders from list().
  - If (t\_quotation\_names and sales\_orders).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in t\_quotation\_names → sales\_orders.
    - Set territory\_orders from list(filter(deferred anonymous expression, sales\_orders)).
  - Set t\_order\_names from list().
  - If territory\_orders.
    - Set t\_order\_names from list of t.name for t drawn from territory\_orders.
      - Draw t from territory\_orders.
  - Set territory\_invoices from list(filter(deferred anonymous expression, sales\_invoices)) when (t\_order\_names and sales\_invoices), otherwise list().
    - Value choice on (t\_order\_names and sales\_invoices) — true gives list(filter(deferred anonymous expression, sales\_invoices)), false gives list().
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in t\_order\_names → sales\_invoices.
  - Set territory\_data from mapping(“territory” → territory.name, “opportunity\_amount” → \_get\_total(territory\_opportunities, “base\_opportunity\_amount”), “quotation\_amount” → \_get\_total(territory\_quotations), “order\_amount” → \_get\_tot ….
  - Evaluate data.append(territory\_data).
- Return data.

**Values supplied outside this operation** effective access from get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L225)

<a id="op-49a25e24039a21"></a>
### Restrict

`operation_enterprise_binding_enterprise_selling_report_territory_wise_sales_territory_wise_sales_restrict`

**Inputs** rows, doctype, filters, user\_permissions, party\_field, party\_type\_field = no value.

**Explicit results** permitted.

**Local steps**

- Set customers from get\_allowed\_docs\_for\_doctype(user\_permissions.get(“Customer”, list()), doctype).
- Set companies from get\_allowed\_docs\_for\_doctype(user\_permissions.get(“Company”, list()), doctype).
- Set requested\_company from filters.get(“company”).
- Set permitted from list().
- For each row in rows.
  - Set company from row.get(“company”).
  - If (requested\_company and company differs from requested\_company).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in requested\_company → company differs from requested\_company.
    - Continue with the next iteration or loop test.
  - If (companies and company does not belong to companies).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in companies → company does not belong to companies.
    - Continue with the next iteration or loop test.
  - If (customers and (party\_type\_field is identical to no value or row.get(party\_type\_field) equals “Customer”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in customers → (party\_type\_field is identical to no value or row.get(party\_type\_field) equals “Customer”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_type\_field is identical to no value → row.get(party\_type\_field) equals “Customer”.
    - If row.get(party\_field) does not belong to customers.
      - Continue with the next iteration or loop test.
  - Evaluate permitted.append(row).
- Return permitted.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L137)

<a id="op-1c0a5f7118c3f7"></a>
### Get opportunities

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_get_opportunities`

**Inputs** filters.

**Record and data access** read “Opportunity” via get\_all.

**Explicit results** opportunities.

**Local steps**

- Set orm\_filters from mapping().
- If filters.get(“transaction\_date”).
  - Set orm\_filters at “transaction\_date” from list(“between”, list(filters at “transaction\_date” at 0, filters at “transaction\_date” at 1)).
- Set opportunities from Platform.get\_all(“Opportunity”, fields = list(“name”, “territory”, “opportunity\_amount”, “conversion\_rate”, …), filters = orm\_filters).
- For each opportunity in opportunities.
  - Set opportunity.base\_opportunity\_amount from (flt(opportunity.opportunity\_amount) × flt((opportunity.conversion\_rate or 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in opportunity.conversion\_rate → 1.
- Return opportunities.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L226)

<a id="op-34548e92033ead"></a>
### Get quotations

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_get_quotations`

**Inputs** opportunities.

**Record and data access** read “Quotation” via get\_all.

**Explicit results** list() · Platform.get\_all(“Quotation”, fields = list(“name”, “base\_grand\_total”, “opportunity”, “company”, …), filters = mapping(“docstatus” → 1, “opportunity” → list(“in”, opportunity\_names))).

**Local steps**

- If not opportunities.
  - Return list().
- Set opportunity\_names from list of o.get(“name”) for o drawn from opportunities.
  - Draw o from opportunities.
- Return Platform.get\_all(“Quotation”, fields = list(“name”, “base\_grand\_total”, “opportunity”, “company”, …), filters = mapping(“docstatus” → 1, “opportunity” → list(“in”, opportunity\_names))).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L227)

<a id="op-9710e7d7965762"></a>
### Get sales orders

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_get_sales_orders`

**Inputs** quotations.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- If not quotations.
  - Return list().
- Set quotation\_names from list of q.get(“name”) for q drawn from quotations.
  - Draw q from quotations.
- Set SalesOrder from Platform.qb.DocType(“Sales Order”).
- Set SalesOrderItem from Platform.qb.DocType(“Sales Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(SalesOrder.name, SalesOrder.base\_grand\_total, SalesOrder.company, SalesOrder.customer, …).where(SalesOrder.docstatus equals 1).where(Sa ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L229)

<a id="op-888a24579a7f11"></a>
### Get sales invoice

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_get_sales_invoice`

**Inputs** sales\_orders.

**Explicit results** list() · query.run(as\_dict = true).

**Local steps**

- If not sales\_orders.
  - Return list().
- Set so\_names from list of so.get(“name”) for so drawn from sales\_orders.
  - Draw so from sales\_orders.
- Set SalesInvoice from Platform.qb.DocType(“Sales Invoice”).
- Set SalesInvoiceItem from Platform.qb.DocType(“Sales Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(SalesInvoice.name, SalesInvoice.base\_grand\_total, SalesInvoice.company, SalesInvoice.customer, …).where(SalesInvoice.docstatus equals 1 ….
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L228)

<a id="op-e8c9d5d1c1a2ca"></a>
### Get total

`operation_enterprise_selling_report_territory_wise_sales_business_behavior_get_total`

**Inputs** doclist, amount\_field = “base\_grand\_total”.

**Explicit results** 0 · total.

**Local steps**

- If not doclist.
  - Return 0.
- Set seen from set().
- Set total from 0.
- For each doc in doclist.
  - If doc.get(“name”) belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(doc.get(“name”)).
  - Update total using + doc.get(amount\_field, 0).
- Return total.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L230)
