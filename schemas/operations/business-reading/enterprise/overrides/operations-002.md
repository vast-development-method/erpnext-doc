# Regional rules and controller overrides · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Import supplier invoice

[Record definition](../../../../data/record-types/import_supplier_invoice.json)

<a id="op-2174080eaf2de8"></a>
### Get country

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_get_country`

**Inputs** code.

**Record and data access** read “Country” via get\_value.

**Explicit results** existing\_country\_name.

**Explicit failure paths** validation helper — translated “Country Code in File does not match with country code set up in the system”.

**Local steps**

- Set existing\_country\_name from Platform.db.get\_value(“Country”, filters = mapping(“code” → code), fieldname = “name”).
- If existing\_country\_name.
  - Return existing\_country\_name.
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Country Code in File does not match with country code set up in the system”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0616.json#L1716) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L976)

<a id="op-a1b8cc19c0cc34"></a>
### Create uom

`operation_enterprise_regional_record_definitions_import_supplier_invoice_business_behavior_create_unit_of_measure`

**Inputs** uom.

**Record and data access** read “UOM” via get\_value.

**State and service calls** request new\_doc for “UOM” · call insert on new\_uom.

**Explicit results** existing\_uom · new\_uom.uom\_name.

**Local steps**

- Set existing\_uom from Platform.db.get\_value(“UOM”, filters = mapping(“uom\_name” → uom), fieldname = “uom\_name”).
- If existing\_uom.
  - Return existing\_uom.
- Otherwise.
  - Set new\_uom from Platform.new\_doc(“UOM”).
  - Set new\_uom.uom\_name from uom.
  - Evaluate new\_uom.insert(ignore\_permissions = true).
  - Return new\_uom.uom\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L975)

## Report · Irs 1099

<a id="op-2e4c79a9942ae6"></a>
### Execute

`operation_enterprise_regional_report_irs_1099_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set filters from filters when isinstance(filters, Platform.\_dict), otherwise Platform.\_dict(filters).
  - Value choice on isinstance(filters, Platform.\_dict) — true gives filters, false gives Platform.\_dict(filters).
- If not filters.
  - Evaluate filters.setdefault(“fiscal\_year”, get\_fiscal\_year(nowdate()) at 0).
  - Evaluate filters.setdefault(“company”, Platform.db.get\_default(“company”)).
- Evaluate Platform.has\_permission(“Company”, doc = filters.company, throw = true).
- Evaluate validate\_company\_region(filters.company).
- Set columns from get\_columns().
- Set payments from get\_payments(filters).as\_(“payments”).
- Set s from Platform.qb.DocType(“Supplier”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.irs\_1099  ….
- If filters.supplier\_group.
  - Set query from query.where(s.supplier\_group equals filters.supplier\_group).
- Set data from query.run(as\_dict = true).
- Return tuple(columns, data).

**Values supplied outside this operation** clock or generated value from nowdate() · effective access from Platform.has\_permission(“Company”, doc = filters.company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L997)

<a id="op-88040ca2a67336"></a>
### Validate company region

`operation_enterprise_binding_enterprise_regional_report_irs_1099_irs_1099_validate_company_region`

**Inputs** company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “The company {0} is not in the United States. IRS 1099 is only available for companies in the United States.”.format(Platform.bold(company)).

**Local steps**

- If Platform.get\_cached\_value(“Company”, company, “country”) differs from “United States”.
  - Call the validation error handler Platform.throw(translated “The company {0} is not in the United States. IRS 1099 is only available for companies in the United States.”.format(Platform.bold(company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “country”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1415)

<a id="op-c1080451a4a7f1"></a>
### Get payments

`operation_enterprise_binding_enterprise_regional_report_irs_1099_irs_1099_get_payments`

**Inputs** filters.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**Explicit results** ledger\_payments.union\_all(invoice\_payments).

**Local steps**

- Set gl from Platform.qb.DocType(“GL Entry”).
- Set ledger\_payments from nested operand in the contract.qb.from\_(gl).select(gl.party.as\_(“supplier”), (nested operand in the contract.debit − nested operand in the contract.credit).as\_(“amount”)).where(((((nested operand in the co ….
- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set tuple(year\_start, year\_end) from Platform.get\_cached\_value(“Fiscal Year”, filters.fiscal\_year, list(“year\_start\_date”, “year\_end\_date”)).
- Set invoice\_payments from nested operand in the contract.qb.from\_(pi).select(pi.supplier, pi.base\_paid\_amount).where((((pi.docstatus equals 1 bitwise and pi.is\_paid equals 1) bitwise and pi.company equals filters.company) bitwise a ….
- Return ledger\_payments.union\_all(invoice\_payments).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, filters.fiscal\_year, list(“year\_start\_date”, “year\_end\_date”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1413)

<a id="op-ab69ed670b8982"></a>
### Is payment voucher

`operation_enterprise_binding_enterprise_regional_report_irs_1099_irs_1099_is_payment_voucher`

**Inputs** gl.

**Explicit results** (gl.voucher\_type equals “Payment Entry” bitwise or (gl.voucher\_type equals “Journal Entry” bitwise and gl.voucher\_no.isin(bank\_or\_cash\_journals))).

**Local steps**

- Set account from Platform.qb.DocType(“Journal Entry Account”).
- Set bank\_or\_cash\_journals from nested operand in the contract.qb.from\_(account).select(account.parent).where(account.account\_type.isin(list(“Bank”, “Cash”))).
- Return (gl.voucher\_type equals “Payment Entry” bitwise or (gl.voucher\_type equals “Journal Entry” bitwise and gl.voucher\_no.isin(bank\_or\_cash\_journals))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1414)

<a id="op-5416dc115cdcad"></a>
### Get columns

`operation_enterprise_regional_report_irs_1099_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “supplier\_group”, “label” → translated “Supplier Group”, “fieldtype” → “Link”, “options” → “Supplier Group”, …), mapping(“fieldname” → “supplier”, “label” → translated “Supplier” ….

**Local steps**

- Return list(mapping(“fieldname” → “supplier\_group”, “label” → translated “Supplier Group”, “fieldtype” → “Link”, “options” → “Supplier Group”, …), mapping(“fieldname” → “supplier”, “label” → translated “Supplier” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0619.json#L2021) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L998)

<a id="op-7030450376ffc9"></a>
### Get payer address html

`operation_enterprise_regional_report_irs_1099_business_behavior_get_payer_address_document_markup`

**Inputs** company.

**Record and data access** execute query text (SELECT, Address) · resolve a document from “Address” via get\_doc.

**Explicit results** address\_display.

**Local steps**

- Set address\_list from Platform.db.sql(query text (SELECT, Address), mapping(“company” → company), as\_dict = true).
- Set address\_display from empty text.
- If address\_list.
  - Set company\_address from address\_list at 0 at “name”.
  - Set address\_display from Platform.get\_doc(“Address”, company\_address).get\_display().
- Return address\_display.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L999)

<a id="op-ebd55d58191015"></a>
### Get street address html

`operation_enterprise_regional_report_irs_1099_business_behavior_get_street_address_document_markup`

**Inputs** party\_type, party.

**Record and data access** execute query text (SELECT, Dynamic Link) · resolve a document from “Address” via get\_doc.

**Explicit results** tuple(street\_address, city\_state).

**Local steps**

- Set address\_list from Platform.db.sql(query text (SELECT, Dynamic Link), mapping(“party” → party), as\_dict = true).
- Set street\_address, city\_state from empty text.
- If address\_list.
  - Set supplier\_address from address\_list at 0 at “parent”.
  - Set doc from Platform.get\_doc(“Address”, supplier\_address).
  - If doc.address\_line2.
    - Set street\_address from (((doc.address\_line1 + text in the contract) + doc.address\_line2) + text in the contract).
  - Otherwise.
    - Set street\_address from (doc.address\_line1 + text in the contract).
  - Set city\_state from (doc.city + “, ”) when doc.city, otherwise empty text.
    - Value choice on doc.city — true gives (doc.city + “, ”), false gives empty text.
  - Set city\_state from ((city\_state + doc.state) + one space) when doc.state, otherwise city\_state.
    - Value choice on doc.state — true gives ((city\_state + doc.state) + one space), false gives city\_state.
  - Set city\_state from (city\_state + doc.pincode) when doc.pincode, otherwise city\_state.
    - Value choice on doc.pincode — true gives (city\_state + doc.pincode), false gives city\_state.
  - Update city\_state using + text in the contract.
- Return tuple(street\_address, city\_state).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1000)

## Record · Lower deduction certificate

[Record definition](../../../../data/record-types/lower_deduction_certificate.json)

<a id="op-8b242a0aeeec21"></a>
### Lower Deduction Certificate.validate

`operation_enterprise_regional_record_definitions_lower_deduction_certificate_business_behavior_lower_deduction_certificate_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_pan\_from\_supplier().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_rate\_and\_limit().
- Evaluate self.validate\_supplier\_against\_tax\_category().
- Evaluate self.validate\_changes\_after\_use().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set pan from supplier](operations-002.md#op-717f2a9de861d2), [validate dates](operations-002.md#op-9c087f5fdff9ec), [validate rate and limit](operations-002.md#op-64ec3da1b5b813), [validate supplier against tax category](operations-002.md#op-9de58ef9888e25), [validate changes after use](operations-002.md#op-9f3ddd383c6bfb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1576) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L990)

<a id="op-cbc82704d177ff"></a>
### Lower Deduction Certificate.on trash

`operation_enterprise_binding_enterprise_regional_doctype_lower_deduction_certificate_lower_deduction_certificate_lowerdeductioncertificate_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot delete a certificate that is used in Tax Withholding Entries”.

**Local steps**

- If self.is\_used().
  - Call the validation error handler Platform.throw(translated “Cannot delete a certificate that is used in Tax Withholding Entries”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is used](operations-002.md#op-a2012c0af09700).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1400)

<a id="op-717f2a9de861d2"></a>
### Lower Deduction Certificate.set pan from supplier

`operation_enterprise_binding_enterprise_regional_doctype_lower_deduction_certificate_lower_deduction_certificate_lowerdeductioncertificate_set_pan_from_supplier`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.is\_new() and self.is\_used()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.is\_used().
  - Return no value.
- If tax\_id bound to get\_tax\_id\_for\_party(“Supplier”, self.supplier).
  - Set self.pan\_no from tax\_id.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is used](operations-002.md#op-a2012c0af09700).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1401)

<a id="op-9c087f5fdff9ec"></a>
### Lower Deduction Certificate.validate dates

`operation_enterprise_regional_record_definitions_lower_deduction_certificate_business_behavior_lower_deduction_certificate_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Valid Up To date cannot be before Valid From date” · validation helper — translated “Valid From date not in Fiscal Year {0}”.format(Platform.bold(self.fiscal\_year)) · validation helper — translated “Valid Up To date not in Fiscal Year {0}”.format(Platform.bold(self.fiscal\_year)).

**Local steps**

- If getdate(self.valid\_upto) &lt; getdate(self.valid\_from).
  - Call the validation error handler Platform.throw(translated “Valid Up To date cannot be before Valid From date”).
- Set fiscal\_year from get\_fiscal\_year(fiscal\_year = self.fiscal\_year, as\_dict = true).
- If not fiscal\_year.year\_start\_date ≤ getdate(self.valid\_from) ≤ fiscal\_year.year\_end\_date.
  - Compare adjacent operands in order, stopping at the first false comparison in fiscal\_year.year\_start\_date ≤ getdate(self.valid\_from) ≤ fiscal\_year.year\_end\_date.
  - Call the validation error handler Platform.throw(translated “Valid From date not in Fiscal Year {0}”.format(Platform.bold(self.fiscal\_year))).
- If not fiscal\_year.year\_start\_date ≤ getdate(self.valid\_upto) ≤ fiscal\_year.year\_end\_date.
  - Compare adjacent operands in order, stopping at the first false comparison in fiscal\_year.year\_start\_date ≤ getdate(self.valid\_upto) ≤ fiscal\_year.year\_end\_date.
  - Call the validation error handler Platform.throw(translated “Valid Up To date not in Fiscal Year {0}”.format(Platform.bold(self.fiscal\_year))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0616.json#L2692) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L991)

<a id="op-64ec3da1b5b813"></a>
### Lower Deduction Certificate.validate rate and limit

`operation_enterprise_binding_enterprise_regional_doctype_lower_deduction_certificate_lower_deduction_certificate_lowerdeductioncertificate_validate_rate_and_limit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Rate must be at least 0 and less than 100” · validation helper — translated “Certificate Limit must be greater than 0”.

**Local steps**

- If not 0 ≤ flt(self.rate) &lt; 100.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ flt(self.rate) &lt; 100.
  - Call the validation error handler Platform.throw(translated “Rate must be at least 0 and less than 100”).
- If flt(self.certificate\_limit) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Certificate Limit must be greater than 0”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1403)

<a id="op-9de58ef9888e25"></a>
### Lower Deduction Certificate.validate supplier against tax category

`operation_enterprise_regional_record_definitions_lower_deduction_certificate_business_behavior_lower_deduction_certificate_validate_supplier_against_tax_category`

**Inputs** self.

**Record and data access** read “Lower Deduction Certificate” via get\_value.

**Explicit failure paths** validation helper — translated “There is already a valid Lower Deduction Certificate {0} for Supplier {1} against category {2} for this time …”.format(certificate\_link, Platform.bold(self.supplier), Platform.bold(self.tax\_wit ….

**Local steps**

- Set duplicate\_certificate from Platform.db.get\_value(“Lower Deduction Certificate”, mapping(“supplier” → self.supplier, “tax\_withholding\_category” → self.tax\_withholding\_category, “name” → tuple(“!=”, self.name), “company” → self.compan ….
- If (duplicate\_certificate and self.are\_dates\_overlapping(duplicate\_certificate)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in duplicate\_certificate → self.are\_dates\_overlapping(duplicate\_certificate).
  - Set certificate\_link from get\_link\_to\_form(“Lower Deduction Certificate”, duplicate\_certificate.name).
  - Call the validation error handler Platform.throw(translated “There is already a valid Lower Deduction Certificate {0} for Supplier {1} against category {2} for this time …”.format(certificate\_link, Platform.bold(self.supplier), Platform.bo ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [are dates overlapping](operations-002.md#op-86e73b2209df64).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0616.json#L3131) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L992)

<a id="op-86e73b2209df64"></a>
### Lower Deduction Certificate.are dates overlapping

`operation_enterprise_regional_record_definitions_lower_deduction_certificate_business_behavior_lower_deduction_certificate_are_dates_overlapping`

**Inputs** self, duplicate\_certificate.

**Explicit results** true · false.

**Local steps**

- Set valid\_from from duplicate\_certificate.valid\_from.
- Set valid\_upto from duplicate\_certificate.valid\_upto.
- If valid\_from ≤ getdate(self.valid\_from) ≤ valid\_upto.
  - Compare adjacent operands in order, stopping at the first false comparison in valid\_from ≤ getdate(self.valid\_from) ≤ valid\_upto.
  - Return true.
- Otherwise.
  - If valid\_from ≤ getdate(self.valid\_upto) ≤ valid\_upto.
    - Compare adjacent operands in order, stopping at the first false comparison in valid\_from ≤ getdate(self.valid\_upto) ≤ valid\_upto.
    - Return true.
  - Otherwise.
    - If (getdate(self.valid\_from) ≤ valid\_from and valid\_upto ≤ getdate(self.valid\_upto)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(self.valid\_from) ≤ valid\_from → valid\_upto ≤ getdate(self.valid\_upto).
      - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0616.json#L3525) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1575) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L989)

<a id="op-9f3ddd383c6bfb"></a>
### Lower Deduction Certificate.validate changes after use

`operation_enterprise_binding_enterprise_regional_doctype_lower_deduction_certificate_lower_deduction_certificate_lowerdeductioncertificate_validate_changes_after_use`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot change {0} of a certificate that is used in Tax Withholding Entries”.format(“, ”.join(changed)).

**Local steps**

- If (self.is\_new() or not self.is\_used()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.is\_used().
  - Return no value.
- Set changed from list of self.meta.get\_label(field) for field drawn from FIELDS\_FIXED\_AFTER\_USE where self.has\_value\_changed(field).
  - Draw field from FIELDS\_FIXED\_AFTER\_USE, keep a combination only if (self.has\_value\_changed(field)).
- If changed.
  - Call the validation error handler Platform.throw(translated “Cannot change {0} of a certificate that is used in Tax Withholding Entries”.format(“, ”.join(changed))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is used](operations-002.md#op-a2012c0af09700).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1402)

<a id="op-a2012c0af09700"></a>
### Lower Deduction Certificate.is used

`operation_enterprise_binding_enterprise_regional_doctype_lower_deduction_certificate_lower_deduction_certificate_lowerdeductioncertificate_is_used`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Tax Withholding Entry” via exists.

**Explicit results** bool(Platform.db.exists(“Tax Withholding Entry”, mapping(“lower\_deduction\_certificate” → self.name, “docstatus” → 1))).

**Local steps**

- Return bool(Platform.db.exists(“Tax Withholding Entry”, mapping(“lower\_deduction\_certificate” → self.name, “docstatus” → 1))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1399)

## Service · Regional

<a id="op-b576d662c5c7d0"></a>
### Check deletion permission

`operation_enterprise_regional_initialize_business_behavior_check_deletion_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, method.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0614.json#L4280) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L947)

<a id="op-2ed1c9ef2c2cb7"></a>
### Rename vat settings

`operation_enterprise_binding_enterprise_regional_init_rename_vat_settings`

**Inputs** doc, method, old\_name, new\_name, merge = false.

**Declared result** no value.

**Record and data access** read doctype via exists.

**Local steps**

- For each doctype in tuple(“UAE VAT Settings”, “South Africa VAT Settings”).
  - If (Platform.db.exists(doctype, old\_name) and not Platform.db.exists(doctype, new\_name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.exists(doctype, old\_name) → not Platform.db.exists(doctype, new\_name).
    - Evaluate rename\_doc(doctype, old\_name, new\_name, force = true, ignore\_permissions = true, show\_alert = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1411)

## Record · South africa vat settings

<a id="op-aced728935bdd7"></a>
### South Africa VATSettings.validate

`operation_enterprise_regional_record_definitions_south_africa_value_added_tax_settings_business_behavior_south_africa_value_added_tax_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_company\_unchanged().
- Evaluate self.validate\_company\_region().
- Evaluate self.validate\_accounts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate company unchanged](operations-002.md#op-d2e77e3f2803f3), [validate company region](operations-002.md#op-0a5f0cdc709e78), [validate accounts](operations-002.md#op-d82f4c31b8ab00).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L994)

<a id="op-d2e77e3f2803f3"></a>
### South Africa VATSettings.validate company unchanged

`operation_enterprise_binding_enterprise_regional_doctype_south_africa_vat_settings_south_africa_vat_settings_southafricavatsettings_validate_company_unchanged`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Company cannot be changed, create South Africa VAT Settings for {0} instead”.format(Platform.bold(self.company)).

**Local steps**

- If (not self.is\_new() and self.has\_value\_changed(“company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“company”).
  - Call the validation error handler Platform.throw(translated “Company cannot be changed, create South Africa VAT Settings for {0} instead”.format(Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1406)

<a id="op-0a5f0cdc709e78"></a>
### South Africa VATSettings.validate company region

`operation_enterprise_regional_record_definitions_south_africa_value_added_tax_settings_business_behavior_south_africa_value_added_tax_settings_validate_company_region`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Company {0} is not in South Africa.”.format(Platform.bold(self.company)).

**Local steps**

- If (self.company and get\_region(self.company) differs from “South Africa”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → get\_region(self.company) differs from “South Africa”.
  - Call the validation error handler Platform.throw(translated “Company {0} is not in South Africa.”.format(Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0616.json#L4757) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L995)

<a id="op-d82f4c31b8ab00"></a>
### South Africa VATSettings.validate accounts

`operation_enterprise_binding_enterprise_regional_doctype_south_africa_vat_settings_south_africa_vat_settings_southafricavatsettings_validate_accounts`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Account is mandatory”.format(row.idx) · validation helper — translated “Row #{0}: Account {1} is added more than once”.format(row.idx, row.account).

**Local steps**

- Set accounts from set().
- For each row in self.vat\_accounts.
  - If not row.account.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Account is mandatory”.format(row.idx)).
  - If row.account belongs to accounts.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Account {1} is added more than once”.format(row.idx, row.account)).
  - Evaluate self.validate\_account(row).
  - Evaluate accounts.add(row.account).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account](operations-003.md#op-9292845a7e40e0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1405)
