# Regional rules and controller overrides · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-07bd849d290695"></a>
### Generate single invoice

`operation_enterprise_regional_italy_utils_business_behavior_generate_single_invoice`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Sales Invoice” via get\_doc.

**Explicit results** e\_invoice.file\_url.

**Local steps**

- Set doc from Platform.get\_doc(“Sales Invoice”, docname).
- Evaluate Platform.has\_permission(“Sales Invoice”, doc = doc, throw = true).
- Set e\_invoice from prepare\_and\_attach\_invoice(doc, true).
- Return e\_invoice.file\_url.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Invoice”, doc = doc, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L956)

<a id="op-a34f5853f592a3"></a>
### Sales invoice on cancel

`operation_enterprise_regional_italy_utils_business_behavior_sales_invoice_on_cancel`

**Inputs** doc, method.

**Explicit results** no value.

**Local steps**

- If (doc.is\_opening equals “Yes” or get\_company\_country(doc.company) does not belong to list(“Italy”, “Italia”, “Italian Republic”, “Repubblica Italiana”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_opening equals “Yes” → get\_company\_country(doc.company) does not belong to list(“Italy”, “Italia”, “Italian Republic”, “Repubblica Italiana”).
  - Return no value.
- For each attachment in get\_e\_invoice\_attachments(doc).
  - Evaluate remove\_file(attachment.name, attached\_to\_doctype = doc.doctype, attached\_to\_name = doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L6510) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L965)

<a id="op-37d43d46923b67"></a>
### Get company country

`operation_enterprise_regional_italy_utils_business_behavior_get_company_country`

**Inputs** company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Company”, company, “country”).

**Local steps**

- Return Platform.get\_cached\_value(“Company”, company, “country”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “country”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L6724) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L957)

<a id="op-996ad651037174"></a>
### Get e invoice attachments

`operation_enterprise_regional_italy_utils_business_behavior_get_e_invoice_attachments`

**Inputs** invoices.

**Record and data access** read “File” via get\_all.

**Explicit results** no value · out.

**Local steps**

- If not isinstance(invoices, list).
  - If not invoices.company\_tax\_id.
    - Return no value.
  - Set invoices from list(invoices).
- Set tax\_id\_map from mapping of invoice.name → invoice.company\_tax\_id when invoice.company\_tax\_id.startswith(“IT”), otherwise (“IT” + invoice.company\_tax\_id) for invoice drawn from invoices.
  - Draw invoice from invoices.
  - Value choice on invoice.company\_tax\_id.startswith(“IT”) — true gives invoice.company\_tax\_id, false gives (“IT” + invoice.company\_tax\_id).
- Set attachments from Platform.get\_all(“File”, fields = tuple(“name”, “file\_name”, “attached\_to\_name”, “is\_private”), filters = mapping(“attached\_to\_name” → tuple(“in”, list(tax\_id\_map)), “attached\_to\_doctype” → “Sales Invoice”)).
- Set out from list().
- For each attachment in attachments.
  - If (attachment.file\_name and attachment.file\_name.endswith(“.xml”) and attachment.file\_name.startswith(tax\_id\_map.get(attachment.attached\_to\_name))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in attachment.file\_name → attachment.file\_name.endswith(“.xml”) → attachment.file\_name.startswith(tax\_id\_map.get(attachment.attached\_to\_name)).
    - Evaluate out.append(attachment).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L959)

<a id="op-45d63ce291544a"></a>
### Validate address

`operation_enterprise_regional_italy_utils_business_behavior_validate_address`

**Inputs** address\_name.

**Record and data access** read “Address” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Please set {0} for address {1}”.format(field.replace(“-”, empty text), address\_name).

**Local steps**

- Set fields from list(“pincode”, “city”, “country\_code”).
- Set data from (Platform.get\_cached\_value(“Address”, address\_name, fields, as\_dict = 1) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Address”, address\_name, fields, as\_dict = 1) → mapping().
- For each field in fields.
  - If not data.get(field).
    - Call the validation error handler Platform.throw(translated “Please set {0} for address {1}”.format(field.replace(“-”, empty text), address\_name), title = translated “E-Invoicing Information Missing”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Address”, address\_name, fields, as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0618.json#L7273) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L971)

<a id="op-0bf7c9cfe07ea5"></a>
### Get unamended name

`operation_enterprise_regional_italy_utils_business_behavior_get_unamended_name`

**Inputs** doc.

**Explicit results** doc.name · “-”.join(doc.name.split(“-”) at slice no value to negative 1).

**Local steps**

- Set attributes from list(“naming\_series”, “amended\_from”).
- For each attribute in attributes.
  - If not hasattr(doc, attribute).
    - Return doc.name.
- If doc.amended\_from.
  - Return “-”.join(doc.name.split(“-”) at slice no value to negative 1).
- Otherwise.
  - Return doc.name.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0619.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L962)

<a id="op-7b7c3a1a34fa03"></a>
### Get progressive name and number

`operation_enterprise_regional_italy_utils_business_behavior_get_progressive_name_and_number`

**Inputs** doc, replace = false.

**Explicit results** tuple(filename, filename.split(“\_”) at 1) · tuple(progressive\_name, progressive\_number).

**Local steps**

- If replace.
  - For each attachment in get\_e\_invoice\_attachments(doc).
    - Evaluate remove\_file(attachment.name, attached\_to\_doctype = doc.doctype, attached\_to\_name = doc.name).
    - Set filename from attachment.file\_name.split(“.xml”) at 0.
    - Return tuple(filename, filename.split(“\_”) at 1).
- Set company\_tax\_id from doc.company\_tax\_id when doc.company\_tax\_id.startswith(“IT”), otherwise (“IT” + doc.company\_tax\_id).
  - Value choice on doc.company\_tax\_id.startswith(“IT”) — true gives doc.company\_tax\_id, false gives (“IT” + doc.company\_tax\_id).
- Set progressive\_name from Platform.model.naming.make\_autoname((company\_tax\_id + “\_.#####”)).
- Set progressive\_number from progressive\_name.split(“\_”) at 1.
- Return tuple(progressive\_name, progressive\_number).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0619.json#L220) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L961)

<a id="op-1862d19b44de85"></a>
### Set state code

`operation_enterprise_regional_italy_utils_business_behavior_set_state_code`

**Inputs** doc, method.

**Explicit results** no value.

**Local steps**

- If doc.get(“country\_code”).
  - Set doc.country\_code from doc.country\_code.upper().
- If not doc.get(“state”).
  - Return no value.
- If not (hasattr(doc, “state\_code”) and doc.country belongs to list(“Italy”, “Italia”, “Italian Republic”, “Repubblica Italiana”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(doc, “state\_code”) → doc.country belongs to list(“Italy”, “Italia”, “Italian Republic”, “Repubblica Italiana”).
  - Return no value.
- Set state\_codes\_lower from mapping of key.lower() → value for tuple(key, value) drawn from state\_codes.items().
  - Draw tuple(key, value) from state\_codes.items().
- Set state from doc.get(“state”, empty text).lower().
- If state\_codes\_lower.get(state).
  - Set doc.state\_code from state\_codes\_lower.get(state).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0619.json#L598) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1550) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L968)

<a id="op-db0320d1ea1763"></a>
### Update itemised tax data

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_update_itemised_tax_data`

**Inputs** doc.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not doc.items.
  - Return no value.
- Set meta from Platform.get\_meta(doc.items at 0.doctype).
- If not meta.has\_field(“tax\_rate”).
  - Return no value.
- Set itemised\_tax from get\_itemised\_tax(doc).
- Bind local operation determine\_if\_export for subsequent calls.
- Set is\_export from determine\_if\_export(doc).
- For each row in doc.items.
  - Set tuple(tax\_rate, tax\_amount) from tuple(0.0, 0.0).
  - Set item\_code from (row.item\_code or row.item\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.item\_code → row.item\_name.
  - If itemised\_tax.get(item\_code).
    - For each tax in itemised\_tax.get(item\_code).values().
      - Set \_tax\_rate from flt(tax.get(“tax\_rate”, 0), row.precision(“tax\_rate”)).
      - Update tax\_amount using + flt(((row.net\_amount × \_tax\_rate) ÷ 100), row.precision(“tax\_amount”)).
      - Update tax\_rate using + \_tax\_rate.
  - If (not tax\_rate or row.get(“is\_zero\_rated”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not tax\_rate → row.get(“is\_zero\_rated”).
    - Set row.is\_zero\_rated from (is\_export or Platform.get\_cached\_value(“Item”, row.item\_code, “is\_zero\_rated”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_export → Platform.get\_cached\_value(“Item”, row.item\_code, “is\_zero\_rated”).
  - Set row.tax\_rate from flt(tax\_rate, row.precision(“tax\_rate”)).
  - Set row.tax\_amount from flt(tax\_amount, row.precision(“tax\_amount”)).
  - Set row.total\_amount from flt((row.net\_amount + row.tax\_amount), row.precision(“total\_amount”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, “is\_zero\_rated”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L2975) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1073)

<a id="op-c6493128c7497f"></a>
### Update itemised tax data.determine if export

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_update_itemised_tax_data_determine_if_export`

**Inputs** doc.

**Record and data access** read “Company” via get\_cached\_value · read “Address” via get\_value.

**State and service calls** msgprint with translated “Please set Customer Address to determine if the transaction is an export.”.

**Explicit results** false · true.

**Local steps**

- If doc.doctype differs from “Sales Invoice”.
  - Return false.
- If not doc.customer\_address.
  - If not doc.total\_taxes\_and\_charges.
    - Evaluate Platform.msgprint(translated “Please set Customer Address to determine if the transaction is an export.”, alert = true).
  - Return false.
- Set company\_country from Platform.get\_cached\_value(“Company”, doc.company, “country”).
- Set customer\_country from Platform.db.get\_value(“Address”, doc.customer\_address, “country”).
- If company\_country differs from customer\_country.
  - Return true.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, doc.company, “country”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L4033) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1074)

<a id="op-d47ae076df082b"></a>
### Get account currency

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_get_account_currency`

**Inputs** account.

**Explicit results** no value · Platform.local\_cache(“account\_currency”, account, generator).

**Local steps**

- If not account.
  - Return no value.
- Bind local operation generator for subsequent calls.
- Return Platform.local\_cache(“account\_currency”, account, generator).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L4338) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1067)

<a id="op-b4a1579e47f930"></a>
### Get account currency.generator

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_get_account_currency_generator`

**Inputs** no declared parameters.

**Record and data access** read “Account” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** account\_currency.

**Local steps**

- Set tuple(account\_currency, company) from Platform.get\_cached\_value(“Account”, account, list(“account\_currency”, “company”)).
- If not account\_currency.
  - Set account\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Return account\_currency.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, list(“account\_currency”, “company”)), Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L4574) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1068)

<a id="op-c12e08a6658165"></a>
### Get tax accounts

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_get_tax_accounts`

**Inputs** company.

**Record and data access** read “UAE VAT Account” via get\_all.

**Explicit results** tax\_accounts\_dict.

**Explicit failure paths** validation helper — translated “Please set Vat Accounts for Company: "{0}" in UAE VAT Settings”.format(company).

**Local steps**

- Set tax\_accounts\_dict from Platform.\_dict().
- Set tax\_accounts\_list from Platform.get\_all(“UAE VAT Account”, filters = mapping(“parent” → company), fields = list(“Account”)).
- If (not tax\_accounts\_list and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not tax\_accounts\_list → not Platform.in\_test.
  - Call the validation error handler Platform.throw(translated “Please set Vat Accounts for Company: "{0}" in UAE VAT Settings”.format(company)).
- For each tax\_account in tax\_accounts\_list.
  - For each tuple(\_account, name) in tax\_account.items().
    - Set tax\_accounts\_dict at name from name.
- Return tax\_accounts\_dict.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1069)

<a id="op-a76e4dc081146d"></a>
### Update grand total for rcm

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_update_grand_total_for_rcm`

**Inputs** doc, method.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Set country from Platform.get\_cached\_value(“Company”, doc.company, “country”).
- If country differs from “United Arab Emirates”.
  - Return no value.
- If not doc.total\_taxes\_and\_charges.
  - Return no value.
- If doc.reverse\_charge equals “Y”.
  - Set tax\_accounts from get\_tax\_accounts(doc.company).
  - Set base\_vat\_tax from 0.
  - Set vat\_tax from 0.
  - For each tax in doc.get(“taxes”).
    - If tax.category does not belong to tuple(“Total”, “Valuation and Total”).
      - Continue with the next iteration or loop test.
    - If (flt(tax.base\_tax\_amount\_after\_discount\_amount) and tax.account\_head belongs to tax\_accounts).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(tax.base\_tax\_amount\_after\_discount\_amount) → tax.account\_head belongs to tax\_accounts.
      - Update base\_vat\_tax using + tax.base\_tax\_amount\_after\_discount\_amount.
      - Update vat\_tax using + tax.tax\_amount\_after\_discount\_amount.
  - Update doc.taxes\_and\_charges\_added using − vat\_tax.
  - Update doc.total\_taxes\_and\_charges using − vat\_tax.
  - Update doc.base\_taxes\_and\_charges\_added using − base\_vat\_tax.
  - Update doc.base\_total\_taxes\_and\_charges using − base\_vat\_tax.
  - Evaluate update\_totals(vat\_tax, base\_vat\_tax, doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, doc.company, “country”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L5036) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1072)

<a id="op-b585852a429045"></a>
### Update totals

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_update_totals`

**Inputs** vat\_tax, base\_vat\_tax, doc.

**Local steps**

- Update doc.base\_grand\_total using − base\_vat\_tax.
- Update doc.grand\_total using − vat\_tax.
- If doc.meta.get\_field(“rounded\_total”).
  - If doc.is\_rounded\_total\_disabled().
    - Set doc.outstanding\_amount from doc.grand\_total.
  - Otherwise.
    - Set doc.rounded\_total from round\_based\_on\_smallest\_currency\_fraction(doc.grand\_total, doc.currency, doc.precision(“rounded\_total”)).
    - Set doc.rounding\_adjustment from flt((doc.rounded\_total − doc.grand\_total), doc.precision(“rounding\_adjustment”)).
    - Set doc.outstanding\_amount from (doc.rounded\_total or doc.grand\_total).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.rounded\_total → doc.grand\_total.
- Set doc.in\_words from money\_in\_words(doc.grand\_total, doc.currency).
- Set doc.base\_in\_words from money\_in\_words(doc.base\_grand\_total, Enterprise.get\_company\_currency(doc.company)).
- Evaluate doc.set\_payment\_schedule().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1075)

<a id="op-2badb850306c17"></a>
### Make regional gl entries

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_make_regional_general_ledger_entries`

**Inputs** gl\_entries, doc.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** gl\_entries.

**Local steps**

- Set country from Platform.get\_cached\_value(“Company”, doc.company, “country”).
- If country differs from “United Arab Emirates”.
  - Return gl\_entries.
- If doc.reverse\_charge equals “Y”.
  - Set tax\_accounts from get\_tax\_accounts(doc.company).
  - For each tax in doc.get(“taxes”).
    - If tax.category does not belong to tuple(“Total”, “Valuation and Total”).
      - Continue with the next iteration or loop test.
    - Set gl\_entries from make\_gl\_entry(tax, gl\_entries, doc, tax\_accounts).
- Return gl\_entries.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, doc.company, “country”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L5983) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1071)

<a id="op-9523aeaebeb4a1"></a>
### Make gl entry

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_make_general_ledger_entry`

**Inputs** tax, gl\_entries, doc, tax\_accounts.

**Explicit results** gl\_entries.

**Local steps**

- Set dr\_or\_cr from “credit” when tax.add\_deduct\_tax equals “Add”, otherwise “debit”.
  - Value choice on tax.add\_deduct\_tax equals “Add” — true gives “credit”, false gives “debit”.
- If (flt(tax.base\_tax\_amount\_after\_discount\_amount) and tax.account\_head belongs to tax\_accounts).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(tax.base\_tax\_amount\_after\_discount\_amount) → tax.account\_head belongs to tax\_accounts.
  - Set account\_currency from get\_account\_currency(tax.account\_head).
  - Evaluate gl\_entries.append(doc.get\_gl\_dict(mapping(“account” → tax.account\_head, “cost\_center” → tax.cost\_center, “posting\_date” → doc.posting\_date, “against” → doc.supplier, …), account\_currency, item = tax)).
    - Value choice on account\_currency equals doc.company\_currency — true gives tax.base\_tax\_amount\_after\_discount\_amount, false gives tax.tax\_amount\_after\_discount\_amount.
- Return gl\_entries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L6279) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1070)

<a id="op-2246690e72a98e"></a>
### Validate returns

`operation_enterprise_regional_united_arab_emirates_utils_business_behavior_validate_returns`

**Inputs** doc, method.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Recoverable Standard Rated expenses should not be set when Reverse Charge Applicable is Y”.

**Local steps**

- Set country from Platform.get\_cached\_value(“Company”, doc.company, “country”).
- If country differs from “United Arab Emirates”.
  - Return no value.
- If (doc.reverse\_charge equals “Y” and flt(doc.recoverable\_standard\_rated\_expenses) differs from 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reverse\_charge equals “Y” → flt(doc.recoverable\_standard\_rated\_expenses) differs from 0.
  - Call the validation error handler Platform.throw(translated “Recoverable Standard Rated expenses should not be set when Reverse Charge Applicable is Y”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, doc.company, “country”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0623.json#L6675) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1076)

## Report · Vat audit report

<a id="op-3794650031456d"></a>
### Execute

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** VATAuditReport(filters).run().

**Local steps**

- Evaluate validate\_date\_range(filters).
- Return VATAuditReport(filters).run().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1037)

<a id="op-3335118e73d228"></a>
### VATAudit Report.initialize

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.columns from list().
- Set self.data from list().
- Set self.doctypes from list(“Purchase Invoice”, “Sales Invoice”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0621.json#L6730) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1045)

<a id="op-28eed0e0523c49"></a>
### VATAudit Report.run

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Evaluate self.validate\_company\_region().
- If self.filters.company.
  - Evaluate Platform.has\_permission(“Company”, doc = self.filters.company, throw = true).
- Evaluate self.get\_sa\_vat\_accounts().
- Evaluate self.get\_columns().
- For each doctype in self.doctypes.
  - Evaluate self.get\_invoice\_data(doctype).
  - If self.invoices.
    - Evaluate self.get\_invoice\_items(doctype).
    - Evaluate self.get\_items\_based\_on\_tax\_rate(doctype).
    - Evaluate self.get\_data(doctype).
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [validate company region](operations-005.md#op-d154689437e472), [get sa vat accounts](operations-005.md#op-407afd640a402f), [get columns](operations-006.md#op-c0fb55a04986b1), [get invoice data](operations-005.md#op-ec4a82700facb4), [get invoice items](operations-006.md#op-d77b4691558629), [get items based on tax rate](operations-006.md#op-7d8c1dfd51c060), [get data](operations-006.md#op-36b3e0e3b9e68c).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, doc = self.filters.company, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1046)

<a id="op-d154689437e472"></a>
### VATAudit Report.validate company region

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_validate_company_region`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The company {0} is not in South Africa. VAT Audit Report is only available for companies in South Africa.”.format(Platform.bold(self.filters.company)).

**Local steps**

- If (self.filters.company and get\_region(self.filters.company) differs from “South Africa”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.company → get\_region(self.filters.company) differs from “South Africa”.
  - Call the validation error handler Platform.throw(translated “The company {0} is not in South Africa. VAT Audit Report is only available for companies in South Africa.”.format(Platform.bold(self.filters.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0622.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1047)

<a id="op-407afd640a402f"></a>
### VATAudit Report.get sa vat accounts

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_get_sa_value_added_tax_accounts`

**Inputs** self.

**Record and data access** read “South Africa VAT Account” via get\_all.

**Explicit failure paths** validation helper — translated “Please set VAT Accounts in {0}”.format(link\_to\_settings).

**Local steps**

- Set self.sa\_vat\_accounts from Platform.get\_all(“South Africa VAT Account”, filters = mapping(“parent” → self.filters.company), pluck = “account”).
- If (not self.sa\_vat\_accounts and not Platform.in\_test and not Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.sa\_vat\_accounts → not Platform.in\_test → not Platform.flags.in\_migrate.
  - Set link\_to\_settings from get\_link\_to\_form(“South Africa VAT Settings”, empty text, label = “South Africa VAT Settings”).
  - Call the validation error handler Platform.throw(translated “Please set VAT Accounts in {0}”.format(link\_to\_settings)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0622.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1044)

<a id="op-ec4a82700facb4"></a>
### VATAudit Report.get invoice data

`operation_enterprise_regional_report_value_added_tax_audit_report_business_behavior_value_added_tax_audit_report_get_invoice_data`

**Inputs** self, doctype.

**Record and data access** read doctype via get\_list.

**Local steps**

- Set self.invoices from Platform.\_dict().
- Set party\_field from “supplier” when doctype equals “Purchase Invoice”, otherwise “customer”.
  - Value choice on doctype equals “Purchase Invoice” — true gives “supplier”, false gives “customer”.
- Set account\_field from “credit\_to” when doctype equals “Purchase Invoice”, otherwise “debit\_to”.
  - Value choice on doctype equals “Purchase Invoice” — true gives “credit\_to”, false gives “debit\_to”.
- Set invoice\_data from Platform.get\_list(doctype, filters = self.get\_invoice\_filters(), fields = list(“name as voucher\_no”, “posting\_date”, “remarks”, formatted text {party\_field} as party, …), order\_by = “posting\_date desc”, li ….
- For each row in invoice\_data.
  - Evaluate self.invoices.setdefault(row.voucher\_no, row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get invoice filters](operations-006.md#op-db95bfe50c9518).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0034.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L1041)
