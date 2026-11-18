# Regional rules and controller overrides · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Uae vat 201

<a id="op-79a68f97c2d3c8"></a>
### Get purchase items with vat

`operation_enterprise_binding_enterprise_regional_report_uae_vat_201_uae_vat_201_get_purchase_items_with_vat`

**Inputs** filters.

**Explicit results** nested operand in the contract(nested operand in the contract).on(nested operand in the contract.tax\_row equals nested operand in the contract.name).select(d.item\_row).where(((d.parenttype equals “Purchase ….

**Local steps**

- Set d from Platform.qb.DocType(“Item Wise Tax Detail”).
- Set t from Platform.qb.DocType(“Purchase Taxes and Charges”).
- Set uae\_vat from Platform.qb.DocType(“UAE VAT Account”).
- Return nested operand in the contract(nested operand in the contract).on(nested operand in the contract.tax\_row equals nested operand in the contract.name).select(d.item\_row).where(((d.parenttype equals “Purchase ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1419)

<a id="op-351a2ae954023f"></a>
### Get standard rated expenses tax

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_standard_rated_expenses_tax`

**Inputs** filters.

**Record and data access** read “Purchase Invoice” via get\_all.

**Explicit results** (Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “recoverable\_standard\_rated\_expenses”)), as\_list = true, limit = 1) at 0 at 0 or 0) · 0.

**Local steps**

- Set query\_filters from get\_filters(filters).
- Evaluate query\_filters.append(list(“recoverable\_standard\_rated\_expenses”, “!=”, 0)).
- Evaluate query\_filters.append(list(“docstatus”, “=”, 1)).
- Attempt the following.
  - Return (Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “recoverable\_standard\_rated\_expenses”)), as\_list = true, limit = 1) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_all(“Purchase Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “recoverable\_standard\_rated\_expenses”)), as\_list = true, limit = 1) at 0 at 0 → 0.
- On failure (tuple(IndexError, TypeError)).
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1017)

<a id="op-9be0753f266e7e"></a>
### Get tourist tax return total

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_tourist_tax_return_total`

**Inputs** filters.

**Record and data access** read “Sales Invoice” via get\_all.

**Explicit results** (Platform.db.get\_all(“Sales Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 or 0) · 0.

**Local steps**

- Set query\_filters from get\_filters(filters).
- Evaluate query\_filters.append(list(“tourist\_tax\_return”, “!=”, 0)).
- Evaluate query\_filters.append(list(“docstatus”, “=”, 1)).
- Attempt the following.
  - Return (Platform.db.get\_all(“Sales Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_all(“Sales Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “base\_total”)), as\_list = true, limit = 1) at 0 at 0 → 0.
- On failure (tuple(IndexError, TypeError)).
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1021)

<a id="op-edd893990a2efc"></a>
### Get tourist tax return tax

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_tourist_tax_return_tax`

**Inputs** filters.

**Record and data access** read “Sales Invoice” via get\_all.

**Explicit results** (Platform.db.get\_all(“Sales Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “tourist\_tax\_return”)), as\_list = true, limit = 1) at 0 at 0 or 0) · 0.

**Local steps**

- Set query\_filters from get\_filters(filters).
- Evaluate query\_filters.append(list(“tourist\_tax\_return”, “!=”, 0)).
- Evaluate query\_filters.append(list(“docstatus”, “=”, 1)).
- Attempt the following.
  - Return (Platform.db.get\_all(“Sales Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “tourist\_tax\_return”)), as\_list = true, limit = 1) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_all(“Sales Invoice”, filters = query\_filters, fields = list(mapping(“SUM” → “tourist\_tax\_return”)), as\_list = true, limit = 1) at 0 at 0 → 0.
- On failure (tuple(IndexError, TypeError)).
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1020)

<a id="op-01f5f0c4d19028"></a>
### Get zero rated total

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_zero_rated_total`

**Inputs** filters.

**State and service calls** execute a supplied database query.

**Explicit results** (Platform.db.sql(formatted text   select  sum(i.base\_net\_amount) as total  from  ′tabSales Invoice Item′ i inner join ′tabSales Invoice′ s  on  i.parent = s.name  wh, filters) at 0 at 0 or 0) · 0.

**Local steps**

- Set conditions from get\_conditions(filters).
- Attempt the following.
  - Return (Platform.db.sql(formatted text   select  sum(i.base\_net\_amount) as total  from  ′tabSales Invoice Item′ i inner join ′tabSales Invoice′ s  on  i.parent = s.name  wh, filters) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.sql(formatted text   select  sum(i.base\_net\_amount) as total  from  ′tabSales Invoice Item′ i inner join ′tabSales Invoice′ s  on  i.parent = s.name  wh, filters) at 0 at 0 → 0.
- On failure (tuple(IndexError, TypeError)).
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1022)

<a id="op-31ec0b1c6f5320"></a>
### Get exempt total

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_exempt_total`

**Inputs** filters.

**State and service calls** execute a supplied database query.

**Explicit results** (Platform.db.sql(formatted text   select  sum(i.base\_net\_amount) as total  from  ′tabSales Invoice Item′ i inner join ′tabSales Invoice′ s  on  i.parent = s.name  wh, filters) at 0 at 0 or 0) · 0.

**Local steps**

- Set conditions from get\_conditions(filters).
- Attempt the following.
  - Return (Platform.db.sql(formatted text   select  sum(i.base\_net\_amount) as total  from  ′tabSales Invoice Item′ i inner join ′tabSales Invoice′ s  on  i.parent = s.name  wh, filters) at 0 at 0 or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.sql(formatted text   select  sum(i.base\_net\_amount) as total  from  ′tabSales Invoice Item′ i inner join ′tabSales Invoice′ s  on  i.parent = s.name  wh, filters) at 0 at 0 → 0.
- On failure (tuple(IndexError, TypeError)).
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1011)

<a id="op-ab6f9f30a434f1"></a>
### Get conditions

`operation_enterprise_regional_report_uae_value_added_tax_201_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set conditions from empty text.
- For each opts in tuple(tuple(“company”, “ and company=%(company)s”), tuple(“from\_date”, “ and posting\_date&gt;=%(from\_date)s”), tuple(“to\_date”, “ and posting\_date&lt;=%(to\_date)s”)).
  - If filters.get(opts at 0).
    - Update conditions using + opts at 1.
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1007)

<a id="op-9708a4e11af7c0"></a>
### Get sales conditions

`operation_enterprise_binding_enterprise_regional_report_uae_vat_201_uae_vat_201_get_sales_conditions`

**Inputs** filters, sales\_invoice.

**Explicit results** conditions.

**Local steps**

- Set conditions from list().
- If filters.get(“company”).
  - Evaluate conditions.append(sales\_invoice.company equals filters.get(“company”)).
- If filters.get(“from\_date”).
  - Evaluate conditions.append(sales\_invoice.posting\_date ≥ filters.get(“from\_date”)).
- If filters.get(“to\_date”).
  - Evaluate conditions.append(sales\_invoice.posting\_date ≤ filters.get(“to\_date”)).
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1421)

## Record · Uae vat settings

<a id="op-e956f1b0da2489"></a>
### UAEVATSettings.validate

`operation_enterprise_binding_enterprise_regional_doctype_uae_vat_settings_uae_vat_settings_uaevatsettings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_company\_region().
- Evaluate self.validate\_accounts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate company region](operations-004.md#op-916d21fab8fe8c), [validate accounts](operations-004.md#op-a46fb7cc05d6ec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1407)

<a id="op-916d21fab8fe8c"></a>
### UAEVATSettings.validate company region

`operation_enterprise_binding_enterprise_regional_doctype_uae_vat_settings_uae_vat_settings_uaevatsettings_validate_company_region`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Company {0} is not in United Arab Emirates.”.format(Platform.bold(self.company)).

**Local steps**

- If (self.company and get\_region(self.company) differs from “United Arab Emirates”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → get\_region(self.company) differs from “United Arab Emirates”.
  - Call the validation error handler Platform.throw(translated “Company {0} is not in United Arab Emirates.”.format(Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1410)

<a id="op-a46fb7cc05d6ec"></a>
### UAEVATSettings.validate accounts

`operation_enterprise_binding_enterprise_regional_doctype_uae_vat_settings_uae_vat_settings_uaevatsettings_validate_accounts`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Account is mandatory”.format(row.idx) · validation helper — translated “Row #{0}: Account {1} is added more than once”.format(row.idx, row.account).

**Local steps**

- Set accounts from set().
- For each row in self.uae\_vat\_accounts.
  - If not row.account.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Account is mandatory”.format(row.idx)).
  - If row.account belongs to accounts.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Account {1} is added more than once”.format(row.idx, row.account)).
  - Evaluate self.validate\_account(row).
  - Evaluate accounts.add(row.account).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate account](operations-004.md#op-d996e2661921ff).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1409)

<a id="op-d996e2661921ff"></a>
### UAEVATSettings.validate account

`operation_enterprise_binding_enterprise_regional_doctype_uae_vat_settings_uae_vat_settings_uaevatsettings_validate_account`

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

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1408)

## Service · Utils

<a id="op-e2f02c31d4ca39"></a>
### Update itemised tax data

`operation_enterprise_regional_italy_utils_business_behavior_update_itemised_tax_data`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If not doc.taxes.
  - Return no value.
- If doc.doctype equals “Purchase Invoice”.
  - Return no value.
- Set itemised\_tax from get\_itemised\_tax(doc).
- For each row in doc.items.
  - Set tax\_rate from 0.0.
  - If itemised\_tax.get(row.item\_code).
    - Set tax\_rate from sum(list of tax.get(“tax\_rate”, 0) for tuple(d, tax) drawn from itemised\_tax.get(row.item\_code).items()).
      - Draw tuple(d, tax) from itemised\_tax.get(row.item\_code).items().
  - Set row.tax\_rate from flt(tax\_rate, row.precision(“tax\_rate”)).
  - Set row.tax\_amount from flt(((row.net\_amount × tax\_rate) ÷ 100), row.precision(“net\_amount”)).
  - Set row.total\_amount from flt((row.net\_amount + row.tax\_amount), row.precision(“total\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1551) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L969)

<a id="op-b857b486f60b56"></a>
### Export invoices

`operation_enterprise_regional_italy_utils_business_behavior_export_invoices`

**Inputs** filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Invoice” via get\_list.

**Local steps**

- Evaluate Platform.has\_permission(“Sales Invoice”, throw = true).
- Set invoices from Platform.get\_list(“Sales Invoice”, filters = get\_conditions(filters), fields = list(“name”, “company\_tax\_id”)).
- Set attachments from get\_e\_invoice\_attachments(invoices).
- Set zip\_filename from “{}-einvoices.zip”.format(Platform.utils.get\_datetime().strftime(“%Y%m%d\_%H%M%S”)).
- Evaluate download\_zip(attachments, zip\_filename).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Invoice”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L955)

<a id="op-f7134082bdbbb3"></a>
### Prepare invoice

`operation_enterprise_regional_italy_utils_business_behavior_prepare_invoice`

**Inputs** invoice, progressive\_number.

**Record and data access** resolve a document from “Company” via get\_doc · resolve a document from “Address” via get\_doc · resolve a document from “Sales Invoice” via get\_doc · resolve a document from “Customer” via get\_doc.

**Explicit results** invoice.

**Local steps**

- Set company from Platform.get\_doc(“Company”, invoice.company).
- Set invoice.progressive\_number from progressive\_number.
- Set invoice.unamended\_name from get\_unamended\_name(invoice).
- Set invoice.company\_data from company.
- Set company\_address from Platform.get\_doc(“Address”, invoice.company\_address).
- Set invoice.company\_address\_data from company\_address.
- If not invoice.type\_of\_document.
  - If (invoice.is\_return and invoice.return\_against).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoice.is\_return → invoice.return\_against.
    - Set invoice.type\_of\_document from “TD04”.
    - Set invoice.return\_against\_unamended from get\_unamended\_name(Platform.get\_doc(“Sales Invoice”, invoice.return\_against)).
  - Otherwise.
    - Set invoice.type\_of\_document from “TD01”.
- Set invoice.customer\_data from Platform.get\_doc(“Customer”, invoice.customer).
- Set customer\_address from Platform.get\_doc(“Address”, invoice.customer\_address).
- Set invoice.customer\_address\_data from customer\_address.
- If invoice.shipping\_address\_name.
  - Set invoice.shipping\_address\_data from Platform.get\_doc(“Address”, invoice.shipping\_address\_name).
- If invoice.customer\_data.is\_public\_administration.
  - Set invoice.transmission\_format\_code from “FPA12”.
- Otherwise.
  - Set invoice.transmission\_format\_code from “FPR12”.
- Set invoice.e\_invoice\_items from list of item for item drawn from invoice.items.
  - Draw item from invoice.items.
- Set tax\_data from get\_invoice\_summary(invoice.e\_invoice\_items, invoice.taxes, invoice.item\_wise\_tax\_details).
- Set invoice.tax\_data from tax\_data.
- Set stamp\_duty\_charge\_row from next(generator of tax for tax drawn from invoice.taxes where (tax.charge\_type equals “Actual” and tax.tax\_amount equals 2.0), no value).
  - Draw tax from invoice.taxes, keep a combination only if ((tax.charge\_type equals “Actual” and tax.tax\_amount equals 2.0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “Actual” → tax.tax\_amount equals 2.0.
- If stamp\_duty\_charge\_row.
  - Set invoice.stamp\_duty from stamp\_duty\_charge\_row.tax\_amount.
- For each item in invoice.e\_invoice\_items.
  - If (item.tax\_rate equals 0.0 and item.tax\_amount equals 0.0 and tax\_data.get(“0.0”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.tax\_rate equals 0.0 → item.tax\_amount equals 0.0 → tax\_data.get(“0.0”).
    - Set item.tax\_exemption\_reason from tax\_data at “0.0” at “tax\_exemption\_reason”.
- Set customer\_po\_data from mapping().
- For each d in invoice.e\_invoice\_items.
  - If (d.customer\_po\_no and d.customer\_po\_date and d.customer\_po\_no does not belong to customer\_po\_data).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.customer\_po\_no → d.customer\_po\_date → d.customer\_po\_no does not belong to customer\_po\_data.
    - Set customer\_po\_data at d.customer\_po\_no from d.customer\_po\_date.
- Set invoice.customer\_po\_data from customer\_po\_data.
- Return invoice.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L798) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L964)

<a id="op-1973b34d3b4da0"></a>
### Get conditions

`operation_enterprise_regional_italy_utils_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set filters from json.loads(filters).
- Set conditions from mapping(“docstatus” → 1, “company\_tax\_id” → tuple(“!=”, empty text)).
- If filters.get(“company”).
  - Set conditions at “company” from filters at “company”.
- If filters.get(“customer”).
  - Set conditions at “customer” from filters at “customer”.
- If filters.get(“from\_date”).
  - Set conditions at “posting\_date” from tuple(“&gt;=”, filters at “from\_date”).
- If filters.get(“to\_date”).
  - Set conditions at “posting\_date” from tuple(“&lt;=”, filters at “to\_date”).
- If (filters.get(“from\_date”) and filters.get(“to\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“from\_date”) → filters.get(“to\_date”).
  - Set conditions at “posting\_date” from tuple(“between”, list(filters.get(“from\_date”), filters.get(“to\_date”))).
- Return conditions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L958)

<a id="op-5f573cb2e24023"></a>
### Download zip

`operation_enterprise_regional_italy_utils_business_behavior_download_zip`

**Inputs** files, output\_filename.

**Local steps**

- Bind dependencies zipfile.
- Set zip\_stream from io.BytesIO().
- Within zipfile.ZipFile(zip\_stream, “w”, zipfile.ZIP\_DEFLATED) bound as zip\_file.
  - For each file in files.
    - Set file\_path from Platform.utils.get\_files\_path(file.file\_name, is\_private = file.is\_private).
    - Evaluate zip\_file.write(file\_path, arcname = file.file\_name).
- Set Platform.local.response.filename from output\_filename.
- Set Platform.local.response.filecontent from zip\_stream.getvalue().
- Set Platform.local.response.type from “download”.
- Evaluate zip\_stream.close().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L2393) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L954)

<a id="op-e1e1e78c0e0472"></a>
### Get invoice summary

`operation_enterprise_regional_italy_utils_business_behavior_get_invoice_summary`

**Inputs** items, taxes, item\_wise\_tax\_details.

**Explicit results** summary\_data.

**Local steps**

- Set summary\_data from Platform.\_dict().
- Set taxes\_wise\_tax\_details from mapping().
- For each d in item\_wise\_tax\_details.
  - If d.tax\_row does not belong to taxes\_wise\_tax\_details.
    - Set taxes\_wise\_tax\_details at d.tax\_row from list().
  - Evaluate taxes\_wise\_tax\_details at d.tax\_row.append(d).
- For each tax in taxes.
  - If tax.charge\_type equals “Actual”.
    - Continue with the next iteration or loop test.
  - If tax.charge\_type belongs to list(“On Previous Row Total”, “On Previous Row Amount”).
    - Set reference\_row from next(generator of row for row drawn from taxes where row.idx equals int((tax.row\_id or 0)), no value).
      - Draw row from taxes, keep a combination only if (row.idx equals int((tax.row\_id or 0))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax.row\_id → 0.
    - If reference\_row.
      - Evaluate append\_row\_as\_charges(items, tax, reference\_row, summary\_data).
  - For each row in (taxes\_wise\_tax\_details.get(tax.name) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in taxes\_wise\_tax\_details.get(tax.name) → list().
    - Evaluate update\_summary\_details(summary\_data, tax, row.rate, row.amount, …).
  - If summary\_data equals mapping().
    - Evaluate update\_summary\_details(summary\_data, tax, 0.0, 0.0, …).
- Return summary\_data.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L2721) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L960)

<a id="op-879f2942812be3"></a>
### Update summary details

`operation_enterprise_regional_italy_utils_business_behavior_update_summary_details`

**Inputs** summary\_data, tax, rate, amount, taxable\_amount.

**Local steps**

- Set key from cstr(rate).
- Evaluate summary\_data.setdefault(key, mapping(“tax\_amount” → 0.0, “taxable\_amount” → 0.0, “tax\_exemption\_reason” → empty text, “tax\_exemption\_law” → empty text)).
- Update summary\_data at key at “tax\_amount” using + amount.
- Update summary\_data at key at “taxable\_amount” using + taxable\_amount.
- If key equals “0.0”.
  - Set summary\_data at key at “tax\_exemption\_reason” from tax.tax\_exemption\_reason.
  - Set summary\_data at key at “tax\_exemption\_law” from tax.tax\_exemption\_law.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L3285) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1552) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L970)

<a id="op-0514ec856bea0e"></a>
### Append row as charges

`operation_enterprise_regional_italy_utils_business_behavior_append_row_as_charges`

**Inputs** items, tax, reference\_row, summary\_data.

**Local steps**

- Set rate from tax.rate.
- Set amount from ((reference\_row.tax\_amount × tax.rate) ÷ 100).
- Set taxable\_amount from reference\_row.tax\_amount.
- Evaluate items.append(Platform.\_dict(idx = (len(items) + 1), item\_code = reference\_row.description, item\_name = reference\_row.description, description = reference\_row.description, …)).
- Evaluate update\_summary\_details(summary\_data, tax, rate, amount, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L3600) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L953)

<a id="op-c8c49bb28f711e"></a>
### Sales invoice validate

`operation_enterprise_regional_italy_utils_business_behavior_sales_invoice_validate`

**Inputs** doc.

**Record and data access** read “Company” via get\_cached\_value · resolve a document from “Customer” via get\_doc · read “Mode of Payment” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated (“Please set an Address on the Company '%s'” modulo or format doc.company) · validation helper — translated “Fiscal Regime is mandatory, kindly set the fiscal regime in the company {0}”.format(doc.company) · validation helper — translated “Please set both the Tax ID and Fiscal Code on Company {0}”.format(doc.company) · validation helper — translated (“Please set Fiscal Code for the customer '%s'” modulo or format doc.customer) · validation helper — translated (“Please set Fiscal Code for the public administration '%s'” modulo or format doc.customer) · 4 additional forms in the steps below.

**Local steps**

- Evaluate set\_payment\_schedule\_swift\_number(doc).
- If (doc.doctype differs from “Sales Invoice” or doc.is\_opening equals “Yes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype differs from “Sales Invoice” → doc.is\_opening equals “Yes”.
  - Return no value.
- If not doc.company\_address.
  - Call the validation error handler Platform.throw(translated (“Please set an Address on the Company '%s'” modulo or format doc.company), title = translated “E-Invoicing Information Missing”).
- Otherwise.
  - Evaluate validate\_address(doc.company\_address).
- Set company\_fiscal\_regime from Platform.get\_cached\_value(“Company”, doc.company, “fiscal\_regime”).
- If not company\_fiscal\_regime.
  - Call the validation error handler Platform.throw(translated “Fiscal Regime is mandatory, kindly set the fiscal regime in the company {0}”.format(doc.company)).
- Otherwise.
  - Set doc.company\_fiscal\_regime from company\_fiscal\_regime.
- Set doc.company\_tax\_id from Platform.get\_cached\_value(“Company”, doc.company, “tax\_id”).
- Set doc.company\_fiscal\_code from Platform.get\_cached\_value(“Company”, doc.company, “fiscal\_code”).
- If (not doc.company\_tax\_id or not doc.company\_fiscal\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.company\_tax\_id → not doc.company\_fiscal\_code.
  - Call the validation error handler Platform.throw(translated “Please set both the Tax ID and Fiscal Code on Company {0}”.format(doc.company), title = translated “E-Invoicing Information Missing”).
- Set customer from Platform.get\_doc(“Customer”, doc.customer).
- If customer.customer\_type equals “Individual”.
  - Set doc.customer\_fiscal\_code from customer.fiscal\_code.
  - If not doc.customer\_fiscal\_code.
    - Call the validation error handler Platform.throw(translated (“Please set Fiscal Code for the customer '%s'” modulo or format doc.customer), title = translated “E-Invoicing Information Missing”).
- Otherwise.
  - If customer.is\_public\_administration.
    - Set doc.customer\_fiscal\_code from customer.fiscal\_code.
    - If not doc.customer\_fiscal\_code.
      - Call the validation error handler Platform.throw(translated (“Please set Fiscal Code for the public administration '%s'” modulo or format doc.customer), title = translated “E-Invoicing Information Missing”).
  - Otherwise.
    - Set doc.tax\_id from customer.tax\_id.
    - If not doc.tax\_id.
      - Call the validation error handler Platform.throw(translated (“Please set Tax ID for the customer '%s'” modulo or format doc.customer), title = translated “E-Invoicing Information Missing”).
- If not doc.customer\_address.
  - Call the validation error handler Platform.throw(translated “Please set the Customer Address”, title = translated “E-Invoicing Information Missing”).
- Otherwise.
  - Evaluate validate\_address(doc.customer\_address).
- If not len(doc.taxes).
  - Call the validation error handler Platform.throw(translated “Please set at least one row in the Taxes and Charges Table”, title = translated “E-Invoicing Information Missing”).
- Otherwise.
  - For each row in doc.taxes.
    - If (row.rate equals 0 and row.tax\_amount equals 0 and not row.tax\_exemption\_reason).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.rate equals 0 → row.tax\_amount equals 0 → not row.tax\_exemption\_reason.
      - Call the validation error handler Platform.throw(translated “Row {0}: Please set at Tax Exemption Reason in Sales Taxes and Charges”.format(row.idx), title = translated “E-Invoicing Information Missing”).
- For each schedule in doc.payment\_schedule.
  - If (schedule.mode\_of\_payment and not schedule.mode\_of\_payment\_code).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule.mode\_of\_payment → not schedule.mode\_of\_payment\_code.
    - Set schedule.mode\_of\_payment\_code from Platform.get\_cached\_value(“Mode of Payment”, schedule.mode\_of\_payment, “mode\_of\_payment\_code”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, doc.company, “fiscal\_regime”), Platform.get\_cached\_value(“Company”, doc.company, “tax\_id”) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1549) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L967)

<a id="op-7da2f74eddeb13"></a>
### Set payment schedule swift number

`operation_enterprise_binding_enterprise_regional_italy_utils_set_payment_schedule_swift_number`

**Inputs** doc.

**Record and data access** read “Bank Account” via get\_cached\_value · read “Bank” via get\_cached\_value.

**Local steps**

- For each row in (doc.get(“payment\_schedule”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“payment\_schedule”) → list().
  - Set swift\_number from no value.
  - If row.get(“bank\_account”).
    - Set bank from Platform.get\_cached\_value(“Bank Account”, row.bank\_account, “bank”).
    - Set swift\_number from (bank and Platform.get\_cached\_value(“Bank”, bank, “swift\_number”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in bank → Platform.get\_cached\_value(“Bank”, bank, “swift\_number”).
  - Set row.bank\_account\_swift\_number from (swift\_number or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in swift\_number → no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Bank Account”, row.bank\_account, “bank”), Platform.get\_cached\_value(“Bank”, bank, “swift\_number”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0019.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1412)

<a id="op-c3dd97def57f1d"></a>
### Sales invoice on submit

`operation_enterprise_regional_italy_utils_business_behavior_sales_invoice_on_submit`

**Inputs** doc, method.

**Record and data access** read “Mode of Payment” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Please set the Mode of Payment in Payment Schedule”.format(schedule.idx) · validation helper — translated “Row {0}: Please set the correct code on Mode of Payment {1}”.format(schedule.idx, schedule.mode\_of\_payment).

**Local steps**

- If (doc.is\_opening equals “Yes” or get\_company\_country(doc.company) does not belong to list(“Italy”, “Italia”, “Italian Republic”, “Repubblica Italiana”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_opening equals “Yes” → get\_company\_country(doc.company) does not belong to list(“Italy”, “Italia”, “Italian Republic”, “Repubblica Italiana”).
  - Return no value.
- For each schedule in doc.payment\_schedule.
  - If not schedule.mode\_of\_payment.
    - Call the validation error handler Platform.throw(translated “Row {0}: Please set the Mode of Payment in Payment Schedule”.format(schedule.idx), title = translated “E-Invoicing Information Missing”).
  - Otherwise.
    - If not Platform.db.get\_value(“Mode of Payment”, schedule.mode\_of\_payment, “mode\_of\_payment\_code”).
      - Call the validation error handler Platform.throw(translated “Row {0}: Please set the correct code on Mode of Payment {1}”.format(schedule.idx, schedule.mode\_of\_payment), title = translated “E-Invoicing Information Missing”).
- Evaluate prepare\_and\_attach\_invoice(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L5468) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1548) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L966)

<a id="op-8bf0addf4fc9b1"></a>
### Prepare and attach invoice

`operation_enterprise_regional_italy_utils_business_behavior_prepare_and_attach_invoice`

**Inputs** doc, replace = false.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → xml\_filename, “attached\_to\_doctype” → doc.doctype, “attached\_to\_name” → doc.name, …) via get\_doc.

**State and service calls** call save on \_file.

**Explicit results** \_file.

**Local steps**

- Set tuple(progressive\_name, progressive\_number) from get\_progressive\_name\_and\_number(doc, replace).
- Set invoice from prepare\_invoice(doc, progressive\_number).
- Set item\_meta from Platform.get\_meta(“Sales Invoice Item”).
- Set invoice\_xml from Platform.render\_template(“Enterprise/regional/italy/e-invoice.xml”, context = mapping(“doc” → invoice, “item\_meta” → item\_meta), is\_path = true).
- Set invoice\_xml from invoice\_xml.replace(“&amp;”, “&amp;amp;”).
- Set xml\_filename from (progressive\_name + “.xml”).
- Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → xml\_filename, “attached\_to\_doctype” → doc.doctype, “attached\_to\_name” → doc.name, …)).
- Evaluate \_file.save().
- Return \_file.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L5881) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L963)
