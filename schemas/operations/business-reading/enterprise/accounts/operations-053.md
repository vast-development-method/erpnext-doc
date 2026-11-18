# Accounting and settlement · operations 53

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Inactive sales items

<a id="op-8069e3f5bb1bc6"></a>
### Get items

`operation_enterprise_accounts_report_inactive_sales_items_business_behavior_get_items`

**Inputs** filters.

**Record and data access** read “Item” via get\_all.

**Explicit results** items.

**Local steps**

- Set filters\_dict from mapping(“disabled” → 0, “is\_stock\_item” → 1, “has\_variants” → 0).
- If filters.get(“item\_group”).
  - Set item\_groups from list(filters at “item\_group”, expanded get\_descendants\_of(“Item Group”, filters at “item\_group”)).
  - Evaluate filters\_dict.update(mapping(“item\_group” → list(“in”, item\_groups))).
- If filters.get(“item”).
  - Evaluate filters\_dict.update(mapping(“name” → filters at “item”)).
- Set item\_filters from list(filters\_dict).
- If condition bound to get\_allowed\_masters\_condition(Platform.qb.DocType(“Item”).name, “Item”).
  - Evaluate item\_filters.append(condition).
- Set items from Platform.get\_all(“Item”, fields = list(“name”, “item\_group”, “item\_name”, “item\_code”), filters = item\_filters, order\_by = “name”).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1074)

## Report · Invalid ledger entries

<a id="op-d68b5e5d23305a"></a>
### Execute

`operation_enterprise_accounts_report_invalid_ledger_entries_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_filters(filters).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0262.json#L4302) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1078)

<a id="op-a5958b6661f29b"></a>
### Get columns

`operation_enterprise_accounts_report_invalid_ledger_entries_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”), mapping(“label” → translated “Voucher No”, “fieldname” → “voucher\_no”, “fieldty ….

**Local steps**

- Return list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”), mapping(“label” → translated “Voucher No”, “fieldname” → “voucher\_no”, “fieldty ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0262.json#L4435) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1080)

<a id="op-31a6e077596f48"></a>
### Get data

`operation_enterprise_accounts_report_invalid_ledger_entries_business_behavior_get_data`

**Inputs** filters.

**Declared result** list at list.

**Explicit results** invalid\_vouchers.

**Local steps**

- Set active\_vouchers from get\_active\_vouchers\_for\_period(filters).
- Set invalid\_vouchers from identify\_cancelled\_vouchers(active\_vouchers).
- Return invalid\_vouchers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0262.json#L4668) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1081)

<a id="op-02235ebb31695c"></a>
### Identify cancelled vouchers

`operation_enterprise_accounts_report_invalid_ledger_entries_business_behavior_identify_cancelled_vouchers`

**Inputs** active\_vouchers = no value.

**Declared result** list at dict.

**Explicit results** invalid\_vouchers.

**Local steps**

- Set invalid\_vouchers from list().
- For each voucher\_type in set of x.voucher\_type for x drawn from (active\_vouchers or list()).
  - Draw x from (active\_vouchers or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in active\_vouchers → list().
  - Set names from set of x.voucher\_no for x drawn from active\_vouchers where x.voucher\_type equals voucher\_type.
    - Draw x from active\_vouchers, keep a combination only if (x.voucher\_type equals voucher\_type).
  - Set submitted from get\_submitted\_vouchers(voucher\_type, names).
  - Evaluate invalid\_vouchers.extend(generator of Platform.\_dict(voucher\_type = voucher\_type, voucher\_no = name) for name drawn from sorted((names − submitted))).
    - Draw name from sorted((names − submitted)).
- Return invalid\_vouchers.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1082)

<a id="op-ebbadc42c283b4"></a>
### Get submitted vouchers

`operation_enterprise_binding_enterprise_accounts_report_invalid_ledger_entries_invalid_ledger_entries_get_submitted_vouchers`

**Inputs** voucher\_type, names.

**Declared result** set.

**Explicit results** set(nested operand in the contract.select(nested operand in the contract.name).where((nested operand in the contract.eq(1) bitwise and nested operand in the contract.isin(nested operand in the contract(nested  …).

**Local steps**

- Set dt from qb.DocType(voucher\_type).
- Return set(nested operand in the contract.select(nested operand in the contract.name).where((nested operand in the contract.eq(1) bitwise and nested operand in the contract.isin(nested operand in the contract(nested  …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1221)

<a id="op-e1bf1411c4be45"></a>
### Validate filters

`operation_enterprise_accounts_report_invalid_ledger_entries_business_behavior_validate_filters`

**Inputs** filters = no value.

**Explicit failure paths** validation helper — translated “Filters missing” · validation helper — translated “Company is mandatory”.

**Local steps**

- If not filters.
  - Call the validation error handler Platform.throw(translated “Filters missing”).
- If not filters.company.
  - Call the validation error handler Platform.throw(translated “Company is mandatory”).
- Evaluate validate\_date\_range(filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1083)

<a id="op-1db1ae07225171"></a>
### Build query filters

`operation_enterprise_accounts_report_invalid_ledger_entries_business_behavior_build_query_filters`

**Inputs** filters, voucher\_no.

**Declared result** list.

**Explicit results** qb\_filters.

**Local steps**

- Set qb\_filters from list().
- If filters.
  - If filters.account.
    - Set accounts from filters.account when isinstance(filters.account, (list bitwise or tuple)), otherwise list(filters.account).
      - Value choice on isinstance(filters.account, (list bitwise or tuple)) — true gives filters.account, false gives list(filters.account).
    - Evaluate qb\_filters.append(qb.Field(“account”).isin(accounts)).
  - If filters.voucher\_no.
    - Evaluate qb\_filters.append(voucher\_no.eq(filters.voucher\_no)).
- Return qb\_filters.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1077)

<a id="op-93b03dafaa3ae1"></a>
### Get active vouchers for period

`operation_enterprise_accounts_report_invalid_ledger_entries_business_behavior_get_active_vouchers_for_period`

**Inputs** filters = no value.

**Declared result** list at dict.

**Explicit results** list() · (((get\_ledger\_vouchers(gle, gl\_active, gle.voucher\_type, gle.voucher\_no, …) + get\_ledger\_vouchers(gle, gl\_active, gle.against\_voucher\_type, gle.against\_voucher, …)) + get\_ledger\_vouchers(ple, pl\_active, pl ….

**Local steps**

- If not filters.
  - Return list().
- Set gle from qb.DocType(“GL Entry”).
- Set ple from qb.DocType(“Payment Ledger Entry”).
- Set gl\_active from gle.is\_cancelled.eq(0).
- Set pl\_active from ple.delinked.eq(0).
- Return (((get\_ledger\_vouchers(gle, gl\_active, gle.voucher\_type, gle.voucher\_no, …) + get\_ledger\_vouchers(gle, gl\_active, gle.against\_voucher\_type, gle.against\_voucher, …)) + get\_ledger\_vouchers(ple, pl\_active, pl ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1079)

<a id="op-ec74f34ff1ff11"></a>
### Get ledger vouchers

`operation_enterprise_binding_enterprise_accounts_report_invalid_ledger_entries_invalid_ledger_entries_get_ledger_vouchers`

**Inputs** ledger, is\_active, voucher\_type, voucher\_no, filters.

**Declared result** list at dict.

**Explicit results** nested operand in the contract().where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract(nested operand in the contract))).where(Criter ….

**Local steps**

- Return nested operand in the contract().where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract(nested operand in the contract))).where(Criter ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1220)

## Record · Invoice discounting

[Record definition](../../../../data/record-types/invoice_discounting.json)

<a id="op-292270baa243ba"></a>
### Invoice Discounting.validate

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_mandatory().
- Evaluate self.validate\_invoices().
- Evaluate self.calculate\_total\_amount().
- Evaluate self.set\_status().
- Evaluate self.set\_end\_date().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate mandatory](operations-053.md#op-cd254131acb9c6), [validate invoices](operations-053.md#op-af241427aa4580), [calculate total amount](operations-053.md#op-bd42ec45353409), [set status](operations-053.md#op-d0988c1442b712), [set end date](operations-053.md#op-0685c734e39d39).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L4373) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1085)

<a id="op-0685c734e39d39"></a>
### Invoice Discounting.set end date

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_set_end_date`

**Inputs** self.

**Local steps**

- If (self.loan\_start\_date and self.loan\_period).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.loan\_start\_date → self.loan\_period.
  - Set self.loan\_end\_date from add\_days(self.loan\_start\_date, self.loan\_period).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L4504) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1082)

<a id="op-cd254131acb9c6"></a>
### Invoice Discounting.validate mandatory

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_validate_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Loan Start Date and Loan Period are mandatory to save the Invoice Discounting”.

**Local steps**

- If (self.docstatus equals 1 and not (self.loan\_start\_date and self.loan\_period)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → not (self.loan\_start\_date and self.loan\_period).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.loan\_start\_date → self.loan\_period.
  - Call the validation error handler Platform.throw(translated “Loan Start Date and Loan Period are mandatory to save the Invoice Discounting”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L4606) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1087)

<a id="op-af241427aa4580"></a>
### Invoice Discounting.validate invoices

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_validate_invoices`

**Inputs** self.

**Record and data access** read “Discounted Invoice” via get\_all · read “Sales Invoice” via get\_value.

**Explicit failure paths** validation helper — translated “Row({0}): {1} is already discounted in {2}”.format(record.idx, Platform.bold(record.sales\_invoice), Platform.bold(record.parent)) · validation helper — translated “Row({0}): Outstanding Amount cannot be greater than actual Outstanding Amount {1} in {2}”.format(record.idx, Platform.bold(actual\_outstanding), Platform.bold(record.sales\_invoice)).

**Local steps**

- Set discounted\_invoices from list of record.sales\_invoice for record drawn from Platform.get\_all(“Discounted Invoice”, fields = list(“sales\_invoice”), filters = mapping(“docstatus” → 1)).
  - Draw record from Platform.get\_all(“Discounted Invoice”, fields = list(“sales\_invoice”), filters = mapping(“docstatus” → 1)).
- For each record in self.invoices.
  - If record.sales\_invoice belongs to discounted\_invoices.
    - Call the validation error handler Platform.throw(translated “Row({0}): {1} is already discounted in {2}”.format(record.idx, Platform.bold(record.sales\_invoice), Platform.bold(record.parent))).
  - Set actual\_outstanding from Platform.db.get\_value(“Sales Invoice”, record.sales\_invoice, “outstanding\_amount”).
  - If record.outstanding\_amount &gt; actual\_outstanding.
    - Call the validation error handler Platform.throw(translated “Row({0}): Outstanding Amount cannot be greater than actual Outstanding Amount {1} in {2}”.format(record.idx, Platform.bold(actual\_outstanding), Platform.bold(record.sales\_invoice))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L4734) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1086)

<a id="op-bd42ec45353409"></a>
### Invoice Discounting.calculate total amount

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_calculate_total_amount`

**Inputs** self.

**Local steps**

- Set self.total\_amount from sum(generator of flt(d.outstanding\_amount) for d drawn from self.invoices).
  - Draw d from self.invoices.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L5214) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1076)

<a id="op-d76c13c6c1707b"></a>
### Invoice Discounting.on submit

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_sales\_invoice().
- Evaluate self.make\_gl\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update sales invoice](operations-053.md#op-86e3a368d58f60), [make gl entries](operations-053.md#op-f7b852284ed2e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L5312) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1081)

<a id="op-f965ef4e328d0d"></a>
### Invoice Discounting.on cancel

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.set\_status(cancel = 1).
- Evaluate self.update\_sales\_invoice().
- Evaluate self.make\_gl\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-053.md#op-d0988c1442b712), [update sales invoice](operations-053.md#op-86e3a368d58f60), [make gl entries](operations-053.md#op-f7b852284ed2e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L5383) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1080)

<a id="op-d0988c1442b712"></a>
### Invoice Discounting.set status

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_set_status`

**Inputs** self, status = no value, cancel = 0.

**Record and data access** resolve a document from “Sales Invoice” via get\_doc.

**State and service calls** call db\_set on self.

**Local steps**

- If status.
  - Set self.status from status.
  - Evaluate self.db\_set(“status”, status).
  - For each d in self.invoices.
    - Evaluate Platform.get\_doc(“Sales Invoice”, d.sales\_invoice).set\_status(update = true, update\_modified = false).
- Otherwise.
  - Set self.status from “Draft”.
  - If self.docstatus equals 1.
    - Set self.status from “Sanctioned”.
  - Otherwise.
    - <a id="op-d0988c1442b712-guard-13"></a>If self.docstatus equals 2.
      - Set self.status from “Cancelled”.
- If cancel.
  - Evaluate self.db\_set(“status”, self.status, update\_modified = true).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 2, self.docstatus = 2 (cancelled) selects the branch that assigns “Cancelled” to self.status. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d0988c1442b712-guard-13)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L5485) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1083)

<a id="op-86e3a368d58f60"></a>
### Invoice Discounting.update sales invoice

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_update_sales_invoice`

**Inputs** self.

**Record and data access** read mapping(“doctype” → “Discounted Invoice”, “sales\_invoice” → d.sales\_invoice, “docstatus” → 1) via exists.

**State and service calls** request set\_value on “Sales Invoice”.

**Local steps**

- For each d in self.invoices.
  - If self.docstatus equals 1.
    - Set is\_discounted from 1.
  - Otherwise.
    - Set discounted\_invoice from Platform.db.exists(mapping(“doctype” → “Discounted Invoice”, “sales\_invoice” → d.sales\_invoice, “docstatus” → 1)).
    - Set is\_discounted from 1 when discounted\_invoice, otherwise 0.
      - Value choice on discounted\_invoice — true gives 1, false gives 0.
  - Evaluate Platform.db.set\_value(“Sales Invoice”, d.sales\_invoice, “is\_discounted”, is\_discounted).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0059.json#L5841) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1084)

<a id="op-f7b852284ed2e0"></a>
### Invoice Discounting.make gl entries

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_make_general_ledger_entries`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value · read “Sales Invoice” via get\_value · read “Account” via get\_cached\_value.

**Local steps**

- Set company\_currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
- Set gl\_entries from list().
- Set invoice\_fields from list(“debit\_to”, “party\_account\_currency”, “conversion\_rate”, “cost\_center”).
- Set accounting\_dimensions from get\_accounting\_dimensions().
- Evaluate invoice\_fields.extend(accounting\_dimensions).
- For each d in self.invoices.
  - Set inv from Platform.db.get\_value(“Sales Invoice”, d.sales\_invoice, invoice\_fields, as\_dict = 1).
  - If d.outstanding\_amount.
    - Set outstanding\_in\_company\_currency from flt((d.outstanding\_amount × inv.conversion\_rate), d.precision(“outstanding\_amount”)).
    - Set ar\_credit\_account\_currency from Platform.get\_cached\_value(“Account”, self.accounts\_receivable\_credit, “currency”).
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → inv.debit\_to, “party\_type” → “Customer”, “party” → d.customer, “against” → self.accounts\_receivable\_credit, …), inv.party\_account\_currency, item = inv)).
      - Value choice on inv.party\_account\_currency equals company\_currency — true gives outstanding\_in\_company\_currency, false gives d.outstanding\_amount.
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.accounts\_receivable\_credit, “party\_type” → “Customer”, “party” → d.customer, “against” → inv.debit\_to, …), ar\_credit\_account\_currency, item = inv)).
      - Value choice on ar\_credit\_account\_currency equals company\_currency — true gives outstanding\_in\_company\_currency, false gives d.outstanding\_amount.
- Evaluate make\_gl\_entries(gl\_entries, cancel = self.docstatus equals 2, update\_outstanding = “No”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”), Platform.get\_cached\_value(“Account”, self.accounts\_receivable\_credit, “currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0060.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1079)

<a id="op-9feec18e79731e"></a>
### Invoice Discounting.create disbursement entry

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_create_disbursement_entry`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Journal Entry”.

**Explicit results** je.

**Local steps**

- Set je from Platform.new\_doc(“Journal Entry”).
- Set je.voucher\_type from “Journal Entry”.
- Set je.company from self.company.
- Set je.remark from (“Loan Disbursement entry against Invoice Discounting: ” + self.name).
- Evaluate je.append(“accounts”, mapping(“account” → self.bank\_account, “debit\_in\_account\_currency” → (flt(self.total\_amount) − flt(self.bank\_charges)), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company))).
- If self.bank\_charges.
  - Evaluate je.append(“accounts”, mapping(“account” → self.bank\_charges\_account, “debit\_in\_account\_currency” → flt(self.bank\_charges), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company))).
- Evaluate je.append(“accounts”, mapping(“account” → self.short\_term\_loan, “credit\_in\_account\_currency” → flt(self.total\_amount), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company), “reference\_type” → “ ….
- For each d in self.invoices.
  - Evaluate je.append(“accounts”, mapping(“account” → self.accounts\_receivable\_discounted, “debit\_in\_account\_currency” → flt(d.outstanding\_amount), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company), “re ….
  - Evaluate je.append(“accounts”, mapping(“account” → self.accounts\_receivable\_credit, “credit\_in\_account\_currency” → flt(d.outstanding\_amount), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company), “refer ….
- Return je.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0060.json#L980) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1078)

<a id="op-98fb65c792c975"></a>
### Invoice Discounting.close loan

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_invoice_discounting_close_loan`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Invoice” via get\_value.

**State and service calls** request new\_doc for “Journal Entry”.

**Explicit results** je.

**Local steps**

- Set je from Platform.new\_doc(“Journal Entry”).
- Set je.voucher\_type from “Journal Entry”.
- Set je.company from self.company.
- Set je.remark from (“Loan Settlement entry against Invoice Discounting: ” + self.name).
- Evaluate je.append(“accounts”, mapping(“account” → self.short\_term\_loan, “debit\_in\_account\_currency” → flt(self.total\_amount), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company), “reference\_type” → “I ….
- Evaluate je.append(“accounts”, mapping(“account” → self.bank\_account, “credit\_in\_account\_currency” → flt(self.total\_amount), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company))).
- If getdate(self.loan\_end\_date) &gt; getdate(nowdate()).
  - For each d in self.invoices.
    - Set outstanding\_amount from Platform.db.get\_value(“Sales Invoice”, d.sales\_invoice, “outstanding\_amount”).
    - If flt(outstanding\_amount) &gt; 0.
      - Evaluate je.append(“accounts”, mapping(“account” → self.accounts\_receivable\_discounted, “credit\_in\_account\_currency” → flt(outstanding\_amount), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company), “ref ….
      - Evaluate je.append(“accounts”, mapping(“account” → self.accounts\_receivable\_unpaid, “debit\_in\_account\_currency” → flt(outstanding\_amount), “cost\_center” → Enterprise.get\_default\_cost\_center(self.company), “referenc ….
- Return je.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0060.json#L2015) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1077)

<a id="op-d56928ef9277c4"></a>
### Get invoices

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_get_invoices`

**Inputs** filters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** query.run(as\_dict = 1).

**Explicit failure paths** validation helper — translated “Please set company on the Document before requesting for invoices.”.

**Local steps**

- Set filters from Platform.\_dict(Platform.parse\_json(filters)).
- If not filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “Please set company on the Document before requesting for invoices.”).
- Evaluate Platform.has\_permission(“Company”, doc = filters.get(“company”), throw = true).
- Evaluate Platform.has\_permission(“Invoice Discounting”, throw = true).
- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set di from Platform.qb.DocType(“Discounted Invoice”).
- Set discounted from nested operand in the contract.qb.from\_(di).select(di.sales\_invoice).where(di.docstatus equals 1).
- Set query from Platform.qb.get\_query(“Sales Invoice”, fields = list(“name as sales\_invoice”, “customer”, “posting\_date”, “outstanding\_amount”, …), ignore\_permissions = false).where((((si.company equals filters.company bi ….
- If filters.customer.
  - Set query from query.where(si.customer equals filters.customer).
- If filters.from\_date.
  - Set query from query.where(si.posting\_date ≥ filters.from\_date).
- If filters.to\_date.
  - Set query from query.where(si.posting\_date ≤ filters.to\_date).
- If filters.min\_amount.
  - Set query from query.where(si.base\_grand\_total ≥ filters.min\_amount).
- If filters.max\_amount.
  - Set query from query.where(si.base\_grand\_total ≤ filters.max\_amount).
- Return query.run(as\_dict = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, doc = filters.get(“company”), throw = true), Platform.has\_permission(“Invoice Discounting”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1074)

<a id="op-98e745d5ccfe79"></a>
### Get party account based on invoice discounting

`operation_enterprise_accounts_record_definitions_invoice_discounting_business_behavior_get_party_account_based_on_invoice_discounting`

**Inputs** sales\_invoice.

**Record and data access** execute query text (SELECT, Invoice Discounting).

**Explicit results** party\_account.

**Local steps**

- Set party\_account from no value.
- Set invoice\_discounting from Platform.db.sql(query text (SELECT, Invoice Discounting), sales\_invoice, as\_dict = 1).
- If invoice\_discounting.
  - If invoice\_discounting at 0.status equals “Disbursed”.
    - Set party\_account from invoice\_discounting at 0.accounts\_receivable\_discounted.
  - Otherwise.
    - If invoice\_discounting at 0.status equals “Settled”.
      - Set party\_account from invoice\_discounting at 0.accounts\_receivable\_unpaid.
- Return party\_account.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1075)
