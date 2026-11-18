# Sales relationships · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Opportunity summary by sales stage

<a id="op-ec7f50d4a3f721"></a>
### Opportunity Summary By Sales Stage.initialize

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0438.json#L1306) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L14) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1317)

<a id="op-832ad006a11c09"></a>
### Opportunity Summary By Sales Stage.run

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data, no value, self.chart).

**Local steps**

- Evaluate self.validate\_filters().
- Evaluate self.get\_data().
- Evaluate self.get\_columns().
- Evaluate self.get\_chart\_data().
- Return tuple(self.columns, self.data, no value, self.chart).

**Methods declared on this owner** [validate filters](operations-011.md#op-b8a4e47818003f), [get data](operations-011.md#op-4b2a44a957ae8d), [get columns](operations-011.md#op-9c3b976b2f3988), [get chart data](operations-011.md#op-7af95ec0aeccf7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L15) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1318)

<a id="op-b8a4e47818003f"></a>
### Opportunity Summary By Sales Stage.validate filters

`operation_enterprise_binding_enterprise_crm_report_opportunity_summary_by_sales_stage_opportunity_summary_by_sales_stage_opportunitysummarybysalesstage_validate_filters`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Company is mandatory when Data Based On is Amount”.

**Local steps**

- If (self.filters.get(“data\_based\_on”) equals “Amount” and not self.filters.get(“company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.get(“data\_based\_on”) equals “Amount” → not self.filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “Company is mandatory when Data Based On is Amount”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L567)

<a id="op-9c3b976b2f3988"></a>
### Opportunity Summary By Sales Stage.get columns

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list().
- If self.filters.get(“based\_on”) equals “Opportunity Owner”.
  - Evaluate self.columns.append(mapping(“label” → translated “Opportunity Owner”, “fieldname” → “opportunity\_owner”, “width” → 200)).
- If self.filters.get(“based\_on”) equals “Source”.
  - Evaluate self.columns.append(mapping(“label” → translated “Source”, “fieldname” → “utm\_source”, “fieldtype” → “Link”, “options” → “UTM Source”, …)).
- If self.filters.get(“based\_on”) equals “Opportunity Type”.
  - Evaluate self.columns.append(mapping(“label” → translated “Opportunity Type”, “fieldname” → “opportunity\_type”, “width” → 200)).
- Evaluate self.set\_sales\_stage\_columns().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set sales stage columns](operations-011.md#op-57eea2afbab52c).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0438.json#L1516) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L6) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1311)

<a id="op-57eea2afbab52c"></a>
### Opportunity Summary By Sales Stage.set sales stage columns

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_set_sales_stage_columns`

**Inputs** self.

**Record and data access** read “Sales Stage” via get\_list.

**Local steps**

- Set self.sales\_stage\_list from Platform.db.get\_list(“Sales Stage”, pluck = “name”).
- If any(generator of row at “sales\_stage” equals NO\_SALES\_STAGE for row drawn from self.query\_result).
  - Draw row from self.query\_result.
  - Evaluate self.sales\_stage\_list.append(NO\_SALES\_STAGE).
- For each sales\_stage in self.sales\_stage\_list.
  - If self.filters.get(“data\_based\_on”) equals “Number”.
    - Evaluate self.columns.append(mapping(“label” → self.get\_sales\_stage\_label(sales\_stage), “fieldname” → sales\_stage, “fieldtype” → “Int”, “width” → 150)).
  - Otherwise.
    - If self.filters.get(“data\_based\_on”) equals “Amount”.
      - Evaluate self.columns.append(mapping(“label” → self.get\_sales\_stage\_label(sales\_stage), “fieldname” → sales\_stage, “fieldtype” → “Currency”, “width” → 150)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales stage label](operations-011.md#op-a9aed7b1a847b3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L17) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1320)

<a id="op-a9aed7b1a847b3"></a>
### Opportunity Summary By Sales Stage.get sales stage label

`operation_enterprise_binding_enterprise_crm_report_opportunity_summary_by_sales_stage_opportunity_summary_by_sales_stage_opportunitysummarybysalesstage_get_sales_stage_label`

**Inputs** self, sales\_stage.

**Declared result** str.

**Explicit results** translated “Not Set” when sales\_stage equals NO\_SALES\_STAGE, otherwise translated sales\_stage.

**Local steps**

- Return translated “Not Set” when sales\_stage equals NO\_SALES\_STAGE, otherwise translated sales\_stage.
  - Value choice on sales\_stage equals NO\_SALES\_STAGE — true gives translated “Not Set”, false gives translated sales\_stage.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L565)

<a id="op-4b2a44a957ae8d"></a>
### Opportunity Summary By Sales Stage.get data

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_get_data`

**Inputs** self.

**Local steps**

- Set self.data from list().
- Set based\_on from mapping(“Opportunity Owner” → “\_assign”, “Source” → “utm\_source”, “Opportunity Type” → “opportunity\_type”) at self.filters.get(“based\_on”).
- Set data\_based\_on from mapping(“Number” → mapping(“COUNT” → “\*”, “as” → “count”), “Amount” → “opportunity\_amount as amount”) at self.filters.get(“data\_based\_on”).
- Evaluate self.get\_data\_query(based\_on, data\_based\_on).
- Evaluate self.get\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get data query](operations-011.md#op-d1ef8d1ad21a16), [get rows](operations-011.md#op-bdbd6b6c0d4a6e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0438.json#L2459) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L8) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1313)

<a id="op-d1ef8d1ad21a16"></a>
### Opportunity Summary By Sales Stage.get data query

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_get_data_query`

**Inputs** self, based\_on, data\_based\_on.

**Record and data access** read “Opportunity” via get\_list.

**Local steps**

- If self.filters.get(“data\_based\_on”) equals “Number”.
  - Set group\_by from “{},{}”.format(“sales\_stage”, based\_on).
  - Set self.query\_result from Platform.db.get\_list(“Opportunity”, filters = self.get\_conditions(), fields = list(“sales\_stage”, data\_based\_on, based\_on), group\_by = group\_by).
  - Evaluate self.set\_missing\_sales\_stage().
- Otherwise.
  - If self.filters.get(“data\_based\_on”) equals “Amount”.
    - Set self.query\_result from Platform.db.get\_list(“Opportunity”, filters = self.get\_conditions(), fields = list(“sales\_stage”, based\_on, data\_based\_on, “conversion\_rate”, …)).
    - Evaluate self.set\_missing\_sales\_stage().
    - Evaluate self.convert\_to\_base\_currency().
    - For each row in self.query\_result.
      - If not row.get(based\_on).
        - Set row at based\_on from “Not Assigned”.
    - Set self.grouped\_data from list().
    - Set grouping\_key from deferred anonymous expression.
    - For each tuple(tuple(sales\_stage, \_based\_on), rows) in groupby(sorted(self.query\_result, key = grouping\_key), key = grouping\_key).
      - Evaluate self.grouped\_data.append(mapping(“sales\_stage” → sales\_stage, based\_on → \_based\_on, “amount” → sum(generator of flt(r at “amount”) for r drawn from rows))).
        - Draw r from rows.
    - Set self.query\_result from self.grouped\_data.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get conditions](operations-011.md#op-00f1b0fa94b1e7), [set missing sales stage](operations-011.md#op-c041ff4e656394), [convert to base currency](operations-011.md#op-35b1a663e97b0a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L9) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1314)

<a id="op-c041ff4e656394"></a>
### Opportunity Summary By Sales Stage.set missing sales stage

`operation_enterprise_binding_enterprise_crm_report_opportunity_summary_by_sales_stage_opportunity_summary_by_sales_stage_opportunitysummarybysalesstage_set_missing_sales_stage`

**Inputs** self.

**Local steps**

- For each row in self.query\_result.
  - Set row at “sales\_stage” from (row at “sales\_stage” or NO\_SALES\_STAGE).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “sales\_stage” → NO\_SALES\_STAGE.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L566)

<a id="op-bdbd6b6c0d4a6e"></a>
### Opportunity Summary By Sales Stage.get rows

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_get_rows`

**Inputs** self.

**Local steps**

- Set self.data from list().
- Evaluate self.get\_formatted\_data().
- For each tuple(based\_on, data) in self.formatted\_data.items().
  - Set row\_based\_on from mapping(“Opportunity Owner” → “opportunity\_owner”, “Source” → “utm\_source”, “Opportunity Type” → “opportunity\_type”) at self.filters.get(“based\_on”).
  - Set row from mapping(row\_based\_on → based\_on).
  - For each d in self.query\_result.
    - Set sales\_stage from d.get(“sales\_stage”).
    - Set row at sales\_stage from data.get(sales\_stage).
  - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get formatted data](operations-011.md#op-988f8cd95aaa2e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0438.json#L3495) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L13) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1316)

<a id="op-988f8cd95aaa2e"></a>
### Opportunity Summary By Sales Stage.get formatted data

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_get_formatted_data`

**Inputs** self.

**Local steps**

- Set self.formatted\_data from Platform.\_dict().
- For each d in self.query\_result.
  - Set data\_based\_on from mapping(“Number” → “count”, “Amount” → “amount”) at self.filters.get(“data\_based\_on”).
  - Set based\_on from mapping(“Opportunity Owner” → “\_assign”, “Source” → “utm\_source”, “Opportunity Type” → “opportunity\_type”) at self.filters.get(“based\_on”).
  - If self.filters.get(“based\_on”) equals “Opportunity Owner”.
    - Set value from d.get(based\_on).
    - If (not value or value belongs to list(“&#91;&#93;”, “null”, “Not Assigned”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not value → value belongs to list(“&#91;&#93;”, “null”, “Not Assigned”).
      - Set assignments from list(“Not Assigned”).
    - Otherwise.
      - Attempt the following.
        - Set assignments from json.loads(value).
      - On failure (json.JSONDecodeError).
        - Set assignments from list(“Not Assigned”).
    - Set sales\_stage from d.get(“sales\_stage”).
    - Set count from d.get(data\_based\_on).
    - If assignments.
      - If len(assignments) &gt; 1.
        - For each assigned\_to in assignments.
          - Evaluate self.set\_formatted\_data\_based\_on\_sales\_stage(assigned\_to, sales\_stage, count).
      - Otherwise.
        - Set assigned\_to from assignments at 0.
        - Evaluate self.set\_formatted\_data\_based\_on\_sales\_stage(assigned\_to, sales\_stage, count).
  - Otherwise.
    - Set value from d.get(based\_on).
    - Set sales\_stage from d.get(“sales\_stage”).
    - Set count from d.get(data\_based\_on).
    - Evaluate self.set\_formatted\_data\_based\_on\_sales\_stage(value, sales\_stage, count).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set formatted data based on sales stage](operations-011.md#op-e5a6c800a1f0de).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0438.json#L3843) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L12) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1315)

<a id="op-e5a6c800a1f0de"></a>
### Opportunity Summary By Sales Stage.set formatted data based on sales stage

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_set_formatted_data_based_on_sales_stage`

**Inputs** self, based\_on, sales\_stage, count.

**Local steps**

- Evaluate self.formatted\_data.setdefault(based\_on, Platform.\_dict()).setdefault(sales\_stage, 0).
- Update self.formatted\_data at based\_on at sales\_stage using + count.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0438.json#L4630) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L16) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1319)

<a id="op-00f1b0fa94b1e7"></a>
### Opportunity Summary By Sales Stage.get conditions

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_get_conditions`

**Inputs** self.

**Explicit results** filters.

**Local steps**

- Set filters from list().
- If self.filters.get(“company”).
  - Evaluate filters.append(mapping(“company” → self.filters.get(“company”))).
- If self.filters.get(“opportunity\_type”).
  - Evaluate filters.append(mapping(“opportunity\_type” → self.filters.get(“opportunity\_type”))).
- If self.filters.get(“opportunity\_source”).
  - Evaluate filters.append(mapping(“utm\_source” → self.filters.get(“opportunity\_source”))).
- If self.filters.get(“status”).
  - Evaluate filters.append(mapping(“status” → tuple(“in”, self.filters.get(“status”)))).
- If (self.filters.get(“from\_date”) and self.filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.get(“from\_date”) → self.filters.get(“to\_date”).
  - Evaluate filters.append(list(“transaction\_date”, “between”, list(self.filters.get(“from\_date”), self.filters.get(“to\_date”)))).
- Return filters.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0438.json#L4774) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L7) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1312)

<a id="op-7af95ec0aeccf7"></a>
### Opportunity Summary By Sales Stage.get chart data

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_get_chart_data`

**Inputs** self.

**Local steps**

- Set datasets from list().
- Set values from (list(0) × len(self.sales\_stage\_list)).
- Set options from mapping(“Number” → “count”, “Amount” → “amount”) at self.filters.get(“data\_based\_on”).
- For each data in self.query\_result.
  - For each count in range(len(self.sales\_stage\_list)).
    - If data at “sales\_stage” equals self.sales\_stage\_list at count.
      - Set values at count from (values at count + data at options).
- Evaluate datasets.append(mapping(“name” → options, “values” → values)).
- Set labels from list of translated “Not Set” when stage equals NO\_SALES\_STAGE, otherwise stage for stage drawn from self.sales\_stage\_list.
  - Draw stage from self.sales\_stage\_list.
  - Value choice on stage equals NO\_SALES\_STAGE — true gives translated “Not Set”, false gives stage.
- Set self.chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “line”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L5) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1310)

<a id="op-35b1a663e97b0a"></a>
### Opportunity Summary By Sales Stage.convert to base currency

`operation_enterprise_customer_relationship_management_report_opportunity_summary_by_sales_stage_business_behavior_opportunity_summary_by_sales_stage_convert_to_base_currency`

**Inputs** self.

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(self.filters.company).
- For each row in self.query\_result.
  - Set row at “amount” from (flt(row at “amount”) × self.get\_conversion\_rate(row, company\_currency)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get conversion rate](operations-011.md#op-dcfb6501ffae1f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L4) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1309)

<a id="op-dcfb6501ffae1f"></a>
### Opportunity Summary By Sales Stage.get conversion rate

`operation_enterprise_binding_enterprise_crm_report_opportunity_summary_by_sales_stage_opportunity_summary_by_sales_stage_opportunitysummarybysalesstage_get_conversion_rate`

**Inputs** self, row, company\_currency.

**Declared result** float.

**Explicit results** flt(row.conversion\_rate) · 1.0 · flt(get\_exchange\_rate(row.currency, company\_currency, row.transaction\_date)).

**Local steps**

- If flt(row.conversion\_rate).
  - Return flt(row.conversion\_rate).
- If (not row.currency or row.currency equals company\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.currency → row.currency equals company\_currency.
  - Return 1.0.
- Return flt(get\_exchange\_rate(row.currency, company\_currency, row.transaction\_date)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L564)

## Service · Platform crm api

<a id="op-72a7eb066b145e"></a>
### Create prospect against crm deal

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_create_prospect_against_customer_relationship_deal`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Prospect” via get\_value.

**State and service calls** request new\_doc for “Prospect” · call insert on prospect.

**Local steps**

- Evaluate validate\_Platform\_crm\_sync().
- Set doc from Platform.form\_dict.
- Set prospect from Platform.new\_doc(“Prospect”).
- Set prospect.company\_name from (doc.organization or doc.lead\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.organization → doc.lead\_name.
- Set prospect.no\_of\_employees from doc.no\_of\_employees.
- Set prospect.prospect\_owner from doc.deal\_owner.
- Set prospect.company from doc.Enterprise\_company.
- Set prospect.crm\_deal from doc.crm\_deal.
- Set prospect.territory from doc.territory.
- Set prospect.industry from doc.industry.
- Set prospect.website from doc.website.
- Set prospect.annual\_revenue from doc.annual\_revenue.
- Attempt the following.
  - Set prospect\_name from Platform.db.get\_value(“Prospect”, mapping(“company\_name” → prospect.company\_name)).
  - If not prospect\_name.
    - Evaluate prospect.insert().
    - Set prospect\_name from prospect.name.
- On failure (Exception).
  - Evaluate Platform.log\_error(Platform.get\_traceback(), formatted text Error while creating prospect against CRM Deal: {Platform.form\_dict.get(“crm\_deal\_id”)}).
  - Take no action here.
- If (doc.contacts and len(doc.contacts)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.contacts → len(doc.contacts).
  - Evaluate create\_contacts(json.loads(doc.contacts), prospect.company\_name, “Prospect”, prospect\_name).
- Evaluate create\_address(“Prospect”, prospect\_name, doc.address).
- Set Platform.response at “message” from prospect\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1024)

<a id="op-cf92bb643aa15a"></a>
### Create contacts

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_create_contacts`

**Inputs** contacts, organization = no value, link\_doctype = no value, link\_docname = no value.

**Record and data access** resolve a document from “Contact” via get\_doc · resolve a document from mapping(“doctype” → “Contact”, “first\_name” → c.get(“full\_name”), “gender” → c.get(“gender”), “company\_name” → organization) via get\_doc.

**State and service calls** call save on contact.

**Local steps**

- Evaluate check\_link\_permission(link\_doctype, link\_docname).
- For each c in contacts.
  - Set c from Platform.\_dict(c).
  - Set existing\_contact from contact\_exists(c.email, c.mobile\_no).
  - If existing\_contact.
    - Set contact from Platform.get\_doc(“Contact”, existing\_contact).
  - Otherwise.
    - Set contact from Platform.get\_doc(mapping(“doctype” → “Contact”, “first\_name” → c.get(“full\_name”), “gender” → c.get(“gender”), “company\_name” → organization)).
    - If c.get(“email”).
      - Evaluate contact.append(“email\_ids”, mapping(“email\_id” → c.get(“email”), “is\_primary” → 1)).
    - If c.get(“mobile\_no”).
      - Evaluate contact.append(“phone\_nos”, mapping(“phone” → c.get(“mobile\_no”), “is\_primary\_mobile\_no” → 1)).
  - Evaluate link\_doc(contact, link\_doctype, link\_docname).
  - Evaluate contact.save(ignore\_permissions = not is\_crm\_installed()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1022)

<a id="op-b2eb20a0c2d5e2"></a>
### Create address

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_create_address`

**Inputs** doctype, docname, address.

**Record and data access** read “Address” via exists · resolve a document from “Address” via get\_doc.

**State and service calls** request new\_doc for “Address” · call insert on new\_address\_doc · call save on address.

**Explicit results** no value · new\_address\_doc.name · address.name.

**Local steps**

- If not address.
  - Return no value.
- If isinstance(address, str).
  - Set address from json.loads(address).
- Evaluate check\_link\_permission(doctype, docname).
- Attempt the following.
  - Set \_address from Platform.db.exists(“Address”, address.get(“name”)).
  - If not \_address.
    - Set new\_address\_doc from Platform.new\_doc(“Address”).
    - For each field in list(“address\_title”, “address\_type”, “address\_line1”, “address\_line2”, …).
      - If address.get(field).
        - Evaluate new\_address\_doc.set(field, address.get(field)).
    - Evaluate new\_address\_doc.append(“links”, mapping(“link\_doctype” → doctype, “link\_name” → docname)).
    - Evaluate new\_address\_doc.insert(ignore\_mandatory = true).
    - Return new\_address\_doc.name.
  - Otherwise.
    - Set address from Platform.get\_doc(“Address”, \_address).
    - Evaluate link\_doc(address, doctype, docname).
    - Evaluate address.save(ignore\_permissions = not is\_crm\_installed()).
    - Return address.name.
- On failure (Exception).
  - Evaluate Platform.log\_error(Platform.get\_traceback(), formatted text Error while creating address for {docname}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1021)

<a id="op-b1f1205df4bd96"></a>
### Check link permission

`operation_enterprise_binding_enterprise_crm_foundation_crm_api_check_link_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** link\_doctype, link\_docname.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L555)

<a id="op-8a63d555b00b44"></a>
### Link doc

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_link_record`

**Inputs** doc, link\_doctype, link\_docname.

**Local steps**

- Set already\_linked from any(list of (link.link\_doctype equals link\_doctype and link.link\_name equals link\_docname) for link drawn from doc.links).
  - Draw link from doc.links.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals link\_doctype → link.link\_name equals link\_docname.
- If not already\_linked.
  - Evaluate doc.append(“links”, mapping(“link\_doctype” → link\_doctype, “link\_name” → link\_docname, “link\_title” → link\_docname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0435.json#L3846) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1027)

<a id="op-834f83d0c28b0a"></a>
### Contact exists

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_contact_exists`

**Inputs** email, mobile\_no.

**Record and data access** read “Contact Email” via exists · read “Contact Phone” via exists · read doctype via get\_value.

**Explicit results** Platform.db.get\_value(doctype, name, “parent”) · false.

**Local steps**

- Set email\_exist from Platform.db.exists(“Contact Email”, mapping(“email\_id” → email)).
- Set mobile\_exist from Platform.db.exists(“Contact Phone”, mapping(“phone” → mobile\_no)).
- Set doctype from “Contact Email” when email\_exist, otherwise “Contact Phone”.
  - Value choice on email\_exist — true gives “Contact Email”, false gives “Contact Phone”.
- Set name from (email\_exist or mobile\_exist).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_exist → mobile\_exist.
- If name.
  - Return Platform.db.get\_value(doctype, name, “parent”).
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0435.json#L4075) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1020)

<a id="op-207b98b1489208"></a>
### Create customer

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_create_customer`

**Inputs** customer\_data = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Customer” via exists.

**State and service calls** request new\_doc for “Customer” · call insert on customer.

**Explicit results** customer\_name.

**Local steps**

- Evaluate validate\_Platform\_crm\_sync().
- If not customer\_data.
  - Set customer\_data from Platform.form\_dict.
- Set customer\_name from Platform.db.exists(“Customer”, mapping(“customer\_name” → customer\_data.get(“customer\_name”))).
- Evaluate check\_link\_permission(“Customer”, customer\_name).
- Attempt the following.
  - If not customer\_name.
    - Set customer from Platform.new\_doc(“Customer”).
    - For each field in CUSTOMER\_ALLOWED\_FIELDS.
      - If customer\_data.get(field) is distinct from no value.
        - Evaluate customer.set(field, customer\_data.get(field)).
    - Evaluate customer.insert(ignore\_permissions = not is\_crm\_installed()).
    - Set customer\_name from customer.name.
  - Set contacts from json.loads(customer\_data.get(“contacts”)).
  - Evaluate create\_contacts(contacts, customer\_name, “Customer”, customer\_name).
  - Evaluate create\_address(“Customer”, customer\_name, customer\_data.get(“address”)).
  - Return customer\_name.
- On failure (Exception).
  - Evaluate Platform.log\_error(Platform.get\_traceback(), “Error while creating customer against Platform CRM Deal”).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1023)

<a id="op-9d69c7433679c7"></a>
### Validate Platform crm sync

`operation_enterprise_customer_relationship_management_application_foundation_customer_relationship_management_application_interface_business_behavior_validate_foundation_customer_relationship_sync`

**Inputs** no declared parameters.

**Record and data access** read “CRM Settings” via get\_single.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Platform CRM data synchronization is not enabled on Enterprise. Contact System Manager of Enterprise.” · validation helper with Platform.PermissionError — translated “User not allowed to synchronize data from Platform CRM on Enterprise. Contact System Manager of Enterprise.”.

**Local steps**

- Set CRMSettings from Platform.get\_single(“CRM Settings”).
- If not CRMSettings.enable\_Platform\_crm\_data\_synchronization.
  - Call the validation error handler Platform.throw(translated “Platform CRM data synchronization is not enabled on Enterprise. Contact System Manager of Enterprise.”).
- If is\_crm\_installed().
  - Return no value.
- Set allowed\_users from list of d.user for d drawn from CRMSettings.allowed\_users.
  - Draw d from CRMSettings.allowed\_users.
- If Platform.session.user does not belong to allowed\_users.
  - Call the validation error handler Platform.throw(translated “User not allowed to synchronize data from Platform CRM on Enterprise. Contact System Manager of Enterprise.”, exc = Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0435.json#L5092) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1029)
