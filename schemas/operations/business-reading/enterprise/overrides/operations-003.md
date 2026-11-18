# Regional rules and controller overrides · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · South africa vat settings

<a id="op-9292845a7e40e0"></a>
### South Africa VATSettings.validate account

`operation_enterprise_binding_enterprise_regional_doctype_south_africa_vat_settings_south_africa_vat_settings_southafricavatsettings_validate_account`

**Inputs** self, row.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Account {1} does not belong to company {2}”.format(row.idx, row.account, self.company) · validation helper — translated “Row #{0}: Account {1} is a group account”.format(row.idx, row.account).

**Local steps**

- Set tuple(company, is\_group) from Platform.get\_cached\_value(“Account”, row.account, list(“company”, “is\_group”)).
- If company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Account {1} does not belong to company {2}”.format(row.idx, row.account, self.company)).
- If is\_group.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Account {1} is a group account”.format(row.idx, row.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, row.account, list(“company”, “is\_group”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1404)

## Report · Uae vat 201

<a id="op-ca0dcdab0f5de5"></a>
### Execute

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Evaluate validate\_company(filters).
- Evaluate validate\_company\_region(filters).
- Set columns from get\_columns().
- Set tuple(data, emirates, amounts\_by\_emirate) from get\_data(filters).
- Set currency from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).
- For each row in data.
  - Set row at “currency” from currency.
- Return tuple(columns, data).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1005)

<a id="op-c50452f1e8af63"></a>
### Validate company

`operation_enterprise_binding_enterprise_regional_report_uae_vat_201_uae_vat_201_validate_company`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “Company is required”.

**Local steps**

- If not filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “Company is required”, title = translated “Missing Company”).
- Evaluate Platform.has\_permission(“Company”, doc = filters.get(“company”), throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, doc = filters.get(“company”), throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1422)

<a id="op-fb6d50f07bccf6"></a>
### Validate company region

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_validate_company_region`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “The company {0} is not in United Arab Emirates. UAE VAT 201 report is only available for companies in United …”.format(Platform.bold(filters.get(“company”))).

**Local steps**

- If (filters.get(“company”) and get\_region(filters.get(“company”)) differs from “United Arab Emirates”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“company”) → get\_region(filters.get(“company”)) differs from “United Arab Emirates”.
  - Call the validation error handler Platform.throw(translated “The company {0} is not in United Arab Emirates. UAE VAT 201 report is only available for companies in United …”.format(Platform.bold(filters.get(“company”)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0620.json#L2666) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1024)

<a id="op-5122f7bd9cad3b"></a>
### Get columns

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “no”, “label” → translated “No”, “fieldtype” → “Data”, “width” → 50), mapping(“fieldname” → “legend”, “label” → translated “Legend”, “fieldtype” → “Data”, “width” → 300), mapping ….

**Local steps**

- Return list(mapping(“fieldname” → “no”, “label” → translated “No”, “fieldtype” → “Data”, “width” → 50), mapping(“fieldname” → “legend”, “label” → translated “Legend”, “fieldtype” → “Data”, “width” → 300), mapping ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1006)

<a id="op-3745d851a9a18a"></a>
### Get data

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_data`

**Inputs** filters = no value.

**Explicit results** tuple(data, emirates, amounts\_by\_emirate).

**Local steps**

- Set data from list().
- Set tuple(emirates, amounts\_by\_emirate) from append\_vat\_on\_sales(data, filters).
- Evaluate append\_vat\_on\_expenses(data, filters).
- Return tuple(data, emirates, amounts\_by\_emirate).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0620.json#L3253) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1009)

<a id="op-b87d4f67b5bc58"></a>
### Append vat on sales

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_append_value_added_tax_on_sales`

**Inputs** data, filters.

**Explicit results** tuple(emirates, amounts\_by\_emirate).

**Local steps**

- Evaluate append\_data(data, empty text, translated “VAT on Sales and All Other Outputs”, no value, …).
- Set tuple(emirates, amounts\_by\_emirate) from standard\_rated\_expenses\_emiratewise(data, filters).
- Evaluate append\_data(data, “2”, translated “Tax Refunds provided to Tourists under the Tax Refunds for Tourists Scheme”, (negative 1 × get\_tourist\_tax\_return\_total(filters)), …).
- Evaluate append\_data(data, “3”, translated “Supplies subject to the reverse charge provision”, get\_reverse\_charge\_total(filters), …).
- Evaluate append\_data(data, “4”, translated “Zero Rated”, get\_zero\_rated\_total(filters), …).
- Evaluate append\_data(data, “5”, translated “Exempt Supplies”, get\_exempt\_total(filters), …).
- Evaluate append\_data(data, empty text, empty text, no value, …).
- Return tuple(emirates, amounts\_by\_emirate).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1004)

<a id="op-bd91e969f71074"></a>
### Standard rated expenses emiratewise

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_standard_rated_expenses_emiratewise`

**Inputs** data, filters.

**Explicit results** tuple(emirates, amounts\_by\_emirate).

**Local steps**

- Set total\_emiratewise from get\_total\_emiratewise(filters).
- Set emirates from get\_emirates().
- Set amounts\_by\_emirate from mapping().
- For each tuple(emirate, amount, vat) in total\_emiratewise.
  - Set amounts\_by\_emirate at emirate from mapping(“legend” → emirate, “amount” → amount, “vat\_amount” → vat).
- Set amounts\_by\_emirate from append\_emiratewise\_expenses(data, emirates, amounts\_by\_emirate).
- Return tuple(emirates, amounts\_by\_emirate).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1023)

<a id="op-8b77a62e07311a"></a>
### Append emiratewise expenses

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_append_emiratewise_expenses`

**Inputs** data, emirates, amounts\_by\_emirate.

**Explicit results** amounts\_by\_emirate.

**Local steps**

- For each tuple(no, emirate) in enumerate(emirates, 97).
  - If emirate belongs to amounts\_by\_emirate.
    - Set amounts\_by\_emirate at emirate at “no” from translated “1{0}”.format(chr(no)).
    - Set amounts\_by\_emirate at emirate at “legend” from translated “Standard rated supplies in {0}”.format(emirate).
    - Evaluate data.append(amounts\_by\_emirate at emirate).
  - Otherwise.
    - Evaluate append\_data(data, translated “1{0}”.format(chr(no)), translated “Standard rated supplies in {0}”.format(emirate), 0, …).
- Evaluate append\_supplies\_without\_emirate(data, emirates, amounts\_by\_emirate).
- Return amounts\_by\_emirate.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1002)

<a id="op-0af012c3433653"></a>
### Append supplies without emirate

`operation_enterprise_binding_enterprise_regional_report_uae_vat_201_uae_vat_201_append_supplies_without_emirate`

**Inputs** data, emirates, amounts\_by\_emirate.

**Explicit results** no value.

**Local steps**

- Set rows from list of row for tuple(emirate, row) drawn from amounts\_by\_emirate.items() where emirate does not belong to emirates.
  - Draw tuple(emirate, row) from amounts\_by\_emirate.items(), keep a combination only if (emirate does not belong to emirates).
- If not rows.
  - Return no value.
- Evaluate append\_data(data, “1”, translated “Standard rated supplies with no VAT Emirate”, sum(generator of row at “amount” for row drawn from rows), …).
  - Draw row from rows.
  - Draw row from rows.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1416)

<a id="op-45f11b65617ae5"></a>
### Append vat on expenses

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_append_value_added_tax_on_expenses`

**Inputs** data, filters.

**Local steps**

- Evaluate append\_data(data, empty text, translated “VAT on Expenses and All Other Inputs”, no value, …).
- Evaluate append\_data(data, “9”, translated “Standard Rated Expenses”, get\_standard\_rated\_expenses\_total(filters), …).
- Evaluate append\_data(data, “10”, translated “Supplies subject to the reverse charge provision”, get\_reverse\_charge\_recoverable\_total(filters), …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1003)

<a id="op-3f170d54d64da5"></a>
### Append data

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_append_data`

**Inputs** data, no, legend, amount, vat\_amount.

**Local steps**

- Evaluate data.append(mapping(“no” → no, “legend” → legend, “amount” → amount, “vat\_amount” → vat\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0620.json#L5090) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1001)

<a id="op-c533b848e1df26"></a>
### Get total emiratewise

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_total_emiratewise`

**Inputs** filters.

**Explicit results** list of tuple(emirate, amounts.get(emirate, 0), vat\_amounts.get(emirate, 0)) for emirate drawn from dict.fromkeys(list(expanded amounts, expanded vat\_amounts)).

**Local steps**

- Set amounts from get\_emiratewise\_standard\_rated\_amount(filters).
- Set vat\_amounts from get\_emiratewise\_vat\_amount(filters).
- Return list of tuple(emirate, amounts.get(emirate, 0), vat\_amounts.get(emirate, 0)) for emirate drawn from dict.fromkeys(list(expanded amounts, expanded vat\_amounts)).
  - Draw emirate from dict.fromkeys(list(expanded amounts, expanded vat\_amounts)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1019)

<a id="op-fcef872487f901"></a>
### Get emiratewise standard rated amount

`operation_enterprise_binding_enterprise_regional_report_uae_vat_201_uae_vat_201_get_emiratewise_standard_rated_amount`

**Inputs** filters.

**Explicit results** dict(query.run()).

**Local steps**

- Set i from Platform.qb.DocType(“Sales Invoice Item”).
- Set s from Platform.qb.DocType(“Sales Invoice”).
- Set query from nested operand in the contract(nested operand in the contract).select(s.vat\_emirate, Sum(nested operand in the contract.base\_net\_amount)).where(((nested operand in the contract.docstatus equals 1 bitwise a ….
- For each condition in get\_sales\_conditions(filters, s).
  - Set query from query.where(condition).
- Return dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1417)

<a id="op-cdcb1b53ff5266"></a>
### Get emiratewise vat amount

`operation_enterprise_binding_enterprise_regional_report_uae_vat_201_uae_vat_201_get_emiratewise_vat_amount`

**Inputs** filters.

**Explicit results** dict(query.run()).

**Local steps**

- Set i from Platform.qb.DocType(“Sales Invoice Item”).
- Set s from Platform.qb.DocType(“Sales Invoice”).
- Set t from Platform.qb.DocType(“Sales Taxes and Charges”).
- Set d from Platform.qb.DocType(“Item Wise Tax Detail”).
- Set uae\_vat from Platform.qb.DocType(“UAE VAT Account”).
- Set query from nested operand in the contract(nested operand in the contract).select(s.vat\_emirate, Sum(nested operand in the contract.amount)).where(((((nested operand in the contract bitwise and nested operand in the c ….
- For each condition in get\_sales\_conditions(filters, s).
  - Set query from query.where(condition).
- Return dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1418)

<a id="op-913702545790cd"></a>
### Get emirates

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_emirates`

**Inputs** no declared parameters.

**Explicit results** list(“Abu Dhabi”, “Dubai”, “Sharjah”, “Ajman”, …).

**Local steps**

- Return list(“Abu Dhabi”, “Dubai”, “Sharjah”, “Ajman”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0620.json#L5730) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1010)

<a id="op-2a1937f926ffcf"></a>
### Get filters

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_filters`

**Inputs** filters.

**Explicit results** query\_filters.

**Local steps**

- Set query\_filters from list().
- If filters.get(“company”).
  - Evaluate query\_filters.append(list(“company”, “=”, filters at “company”)).
- If filters.get(“from\_date”).
  - Evaluate query\_filters.append(list(“posting\_date”, “&gt;=”, filters at “from\_date”)).
- If filters.get(“to\_date”).
  - Evaluate query\_filters.append(list(“posting\_date”, “&lt;=”, filters at “to\_date”)).
- Return query\_filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1012)

<a id="op-d2ec74c9faea8b"></a>
### Get reverse charge total

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_reverse_charge_total`

**Inputs** filters.

**Record and data access** read “Purchase Invoice” via get\_all.

**Explicit results** (Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 or 0) · 0.

**Local steps**

- Set query\_filters from get\_filters(filters).
- Evaluate query\_filters.append(list(“reverse\_charge”, “=”, “Y”)).
- Evaluate query\_filters.append(list(“docstatus”, “=”, 1)).
- Attempt the following.
  - Return (Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 → 0.
- On failure (tuple(IndexError, TypeError)).
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0620.json#L6087) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1016)

<a id="op-aa2e74f8954cfa"></a>
### Get reverse charge tax

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_reverse_charge_tax`

**Inputs** filters.

**Explicit results** get\_reverse\_charge\_vat(filters).

**Local steps**

- Return get\_reverse\_charge\_vat(filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1015)

<a id="op-e28431c73579dd"></a>
### Get reverse charge recoverable total

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_reverse_charge_recoverable_total`

**Inputs** filters.

**Record and data access** read “Purchase Invoice” via get\_all.

**Explicit results** (Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 or 0) · 0.

**Local steps**

- Set query\_filters from get\_filters(filters).
- Evaluate query\_filters.append(list(“reverse\_charge”, “=”, “Y”)).
- Evaluate query\_filters.append(list(“recoverable\_reverse\_charge”, “&gt;”, “0”)).
- Evaluate query\_filters.append(list(“docstatus”, “=”, 1)).
- Attempt the following.
  - Return (Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 → 0.
- On failure (tuple(IndexError, TypeError)).
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0621.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1014)

<a id="op-d0b258af3dc6a1"></a>
### Get reverse charge recoverable tax

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_reverse_charge_recoverable_tax`

**Inputs** filters.

**Explicit results** get\_reverse\_charge\_vat(filters, recoverable = true).

**Local steps**

- Return get\_reverse\_charge\_vat(filters, recoverable = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1013)

<a id="op-d4f19fc7fc0bd4"></a>
### Get reverse charge vat

`operation_enterprise_binding_enterprise_regional_report_uae_vat_201_uae_vat_201_get_reverse_charge_vat`

**Inputs** filters, recoverable = false.

**Explicit results** (query.run() at 0 at 0 or 0).

**Local steps**

- Set p from Platform.qb.DocType(“Purchase Invoice”).
- Set t from Platform.qb.DocType(“Purchase Taxes and Charges”).
- Set uae\_vat from Platform.qb.DocType(“UAE VAT Account”).
- Set tax from t.base\_tax\_amount\_after\_discount\_amount.
- If recoverable.
  - Set tax from ((tax × p.recoverable\_reverse\_charge) ÷ 100).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(Sum(tax)).where(((((nested operand in the contract ….
- If recoverable.
  - Set query from query.where(p.recoverable\_reverse\_charge &gt; 0).
- For each condition in get\_conditions\_join(filters, p).
  - Set query from query.where(condition).
- Return (query.run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1420)

<a id="op-f14724c4e8ad72"></a>
### Get conditions join

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_conditions_join`

**Inputs** filters, p.

**Explicit results** conditions.

**Local steps**

- Set conditions from list().
- If filters.get(“company”).
  - Evaluate conditions.append(p.company equals filters.get(“company”)).
- If filters.get(“from\_date”).
  - Evaluate conditions.append(p.posting\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Evaluate conditions.append(p.posting\_date ≤ filters.get(“to\_date”)).
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0621.json#L938) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1008)

<a id="op-e7fcaa453788b3"></a>
### Get standard rated expenses total

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_standard_rated_expenses_total`

**Inputs** filters.

**Explicit results** (query.run() at 0 at 0 or 0).

**Local steps**

- Set i from Platform.qb.DocType(“Purchase Invoice Item”).
- Set p from Platform.qb.DocType(“Purchase Invoice”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(Sum(i.base\_net\_amount)).where(((p.docstatus equals ….
- For each condition in get\_conditions\_join(filters, p).
  - Set query from query.where(condition).
- Return (query.run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.run() at 0 at 0 → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1018)
