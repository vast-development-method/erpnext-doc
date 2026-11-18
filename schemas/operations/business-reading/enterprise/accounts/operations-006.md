# Accounting and settlement · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts mixin

<a id="op-543e69eff542fe"></a>
### Accounts Test Mixin.create item

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_create_item`

**Inputs** self, item\_name = “\_Test Item”, is\_stock = 0, warehouse = no value, company = no value, valuation\_rate = 0.

**Local steps**

- Set item from create\_item(item\_name, is\_stock\_item = is\_stock, warehouse = warehouse, company = company, valuation\_rate = valuation\_rate).
- Set self.item from item.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0297.json#L5709) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L155)

<a id="op-eec8f7fc3cbe26"></a>
### Accounts Test Mixin.create company

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_create_company`

**Inputs** self, company\_name = “\_Test Company”, abbr = “\_TC”.

**Record and data access** read “Company” via exists · resolve a document from “Company” via get\_doc · resolve a document from mapping(“doctype” → “Company”, “company\_name” → company\_name, “country” → “India”, “default\_currency” → “INR”, …) via get\_doc · read “Account” via exists · resolve a document from mapping(“doctype” → “Account”, “account\_name” → acc.account\_name, “parent\_account” → acc.parent\_account, “company” → self.company) via get\_doc.

**State and service calls** call save on company · call save on new\_acc.

**Local steps**

- Set self.company\_abbr from abbr.
- If Platform.db.exists(“Company”, company\_name).
  - Set company from Platform.get\_doc(“Company”, company\_name).
- Otherwise.
  - Set company from Platform.get\_doc(mapping(“doctype” → “Company”, “company\_name” → company\_name, “country” → “India”, “default\_currency” → “INR”, …)).
  - Set company from company.save().
- Set self.company from company.name.
- Set self.cost\_center from company.cost\_center.
- Set self.warehouse from (“Stores - ” + abbr).
- Set self.finished\_warehouse from (“Finished Goods - ” + abbr).
- Set self.income\_account from (“Sales - ” + abbr).
- Set self.expense\_account from (“Cost of Goods Sold - ” + abbr).
- Set self.debit\_to from (“Debtors - ” + abbr).
- Set self.cash from (“Cash - ” + abbr).
- Set self.creditors from (“Creditors - ” + abbr).
- Set self.retained\_earnings from (“Retained Earnings - ” + abbr).
- Set other\_accounts from list(Platform.\_dict(mapping(“attribute\_name” → “deferred\_revenue”, “account\_name” → “Deferred Revenue”, “parent\_account” → (“Current Liabilities - ” + abbr))), Platform.\_dict(mapping(“attribute\_name” → “de ….
- For each acc in other\_accounts.
  - Set acc\_name from ((acc.account\_name + “ - ”) + abbr).
  - If Platform.db.exists(“Account”, acc\_name).
    - Evaluate setattr(self, acc.attribute\_name, acc\_name).
  - Otherwise.
    - Set new\_acc from Platform.get\_doc(mapping(“doctype” → “Account”, “account\_name” → acc.account\_name, “parent\_account” → acc.parent\_account, “company” → self.company)).
    - Set new\_acc.account\_type from acc.get(“account\_type”, no value).
    - Evaluate new\_acc.save().
    - Evaluate setattr(self, acc.attribute\_name, new\_acc.name).
- Evaluate self.identify\_default\_warehouses().

If control reaches the end, it returns no value.

**Methods declared on this owner** [identify default warehouses](operations-006.md#op-ea0cbc2d31f6ee).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0297.json#L5884) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L153)

<a id="op-072b83ded12734"></a>
### Accounts Test Mixin.enable advance as liability

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_enable_advance_as_liability`

**Inputs** self.

**Record and data access** resolve a document from “Company” via get\_doc.

**State and service calls** call save on company.

**Local steps**

- Set company from Platform.get\_doc(“Company”, self.company).
- Set company.book\_advance\_payments\_in\_separate\_party\_account from true.
- Set company.default\_advance\_received\_account from self.advance\_received.
- Set company.default\_advance\_paid\_account from self.advance\_paid.
- Evaluate company.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0298.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L160)

<a id="op-c189118003f6b3"></a>
### Accounts Test Mixin.disable advance as liability

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_disable_advance_as_liability`

**Inputs** self.

**Record and data access** resolve a document from “Company” via get\_doc.

**State and service calls** call save on company.

**Local steps**

- Set company from Platform.get\_doc(“Company”, self.company).
- Set company.book\_advance\_payments\_in\_separate\_party\_account from false.
- Set company.default\_advance\_paid\_account, company.default\_advance\_received\_account from no value.
- Evaluate company.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0298.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L159)

<a id="op-ea0cbc2d31f6ee"></a>
### Accounts Test Mixin.identify default warehouses

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_identify_default_warehouses`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_all.

**Local steps**

- For each w in Platform.db.get\_all(“Warehouse”, filters = mapping(“company” → self.company), fields = list(“name”, “warehouse\_name”)).
  - Evaluate setattr(self, (“warehouse\_” + nested operand in the contract().strip().replace(one space, “\_”)), w.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0298.json#L288) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L161)

<a id="op-3f791931d208b0"></a>
### Accounts Test Mixin.create usd receivable account

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_create_united_states_dollar_receivable_account`

**Inputs** self.

**Record and data access** read “Account” via get\_value · resolve a document from “Account” via get\_doc.

**State and service calls** request new\_doc for “Account” · call insert on acc.

**Local steps**

- Set account\_name from “Debtors USD”.
- If not Platform.db.get\_value(“Account”, filters = mapping(“account\_name” → account\_name, “company” → self.company)).
  - Set acc from Platform.new\_doc(“Account”).
  - Set acc.account\_name from account\_name.
  - Set acc.parent\_account from (“Accounts Receivable - ” + self.company\_abbr).
  - Set acc.company from self.company.
  - Set acc.account\_currency from “USD”.
  - Set acc.account\_type from “Receivable”.
  - Evaluate acc.insert().
- Otherwise.
  - Set name from Platform.db.get\_value(“Account”, filters = mapping(“account\_name” → account\_name, “company” → self.company), fieldname = “name”, pluck = true).
  - Set acc from Platform.get\_doc(“Account”, name).
- Set self.debtors\_usd from acc.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0298.json#L505) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L158)

<a id="op-677f6a6f796b2a"></a>
### Accounts Test Mixin.create usd payable account

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_create_united_states_dollar_payable_account`

**Inputs** self.

**Record and data access** read “Account” via get\_value · resolve a document from “Account” via get\_doc.

**State and service calls** request new\_doc for “Account” · call insert on acc.

**Local steps**

- Set account\_name from “Creditors USD”.
- If not Platform.db.get\_value(“Account”, filters = mapping(“account\_name” → account\_name, “company” → self.company)).
  - Set acc from Platform.new\_doc(“Account”).
  - Set acc.account\_name from account\_name.
  - Set acc.parent\_account from (“Accounts Payable - ” + self.company\_abbr).
  - Set acc.company from self.company.
  - Set acc.account\_currency from “USD”.
  - Set acc.account\_type from “Payable”.
  - Evaluate acc.insert().
- Otherwise.
  - Set name from Platform.db.get\_value(“Account”, filters = mapping(“account\_name” → account\_name, “company” → self.company), fieldname = “name”, pluck = true).
  - Set acc from Platform.get\_doc(“Account”, name).
- Set self.creditors\_usd from acc.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0298.json#L957) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L157)

<a id="op-b7703e75dc4898"></a>
### Accounts Test Mixin.clear old entries

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_clear_old_entries`

**Inputs** self.

**Local steps**

- Set doctype\_list from list(“GL Entry”, “Payment Ledger Entry”, “Sales Invoice”, “Purchase Invoice”, …).
- For each doctype in doctype\_list.
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where(nested operand in the contract.DocType(doctype).company equals self.company).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0298.json#L1409) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L152)

## Report · Accounts payable

<a id="op-d1d0079a6e47b6"></a>
### Execute

`operation_enterprise_accounts_report_accounts_payable_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** ReceivablePayableReport(filters).run(args).

**Local steps**

- Set args from mapping(“account\_type” → “Payable”, “naming\_by” → list(“Buying Settings”, “supp\_master\_name”)).
- Return ReceivablePayableReport(filters).run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L6523) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L527)

## Report · Accounts payable summary

<a id="op-ecff1d24b01f1f"></a>
### Execute

`operation_enterprise_accounts_report_accounts_payable_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** AccountsReceivableSummary(filters).run(args).

**Local steps**

- Set args from mapping(“account\_type” → “Payable”, “naming\_by” → list(“Buying Settings”, “supp\_master\_name”)).
- Return AccountsReceivableSummary(filters).run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0215.json#L4011) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L528)

## Report · Accounts receivable

<a id="op-c1c27f0dd6fe55"></a>
### Execute

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** ReceivablePayableReport(filters).run(args).

**Local steps**

- Set args from mapping(“account\_type” → “Receivable”, “naming\_by” → list(“Selling Settings”, “cust\_master\_name”)).
- Return ReceivablePayableReport(filters).run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0215.json#L6683) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L542)

<a id="op-778669da98bfd0"></a>
### Receivable Payable Report.initialize

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_initialize`

**Inputs** self, filters = no value.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.qb\_selection\_filter from list().
- Set self.ple from qb.DocType(“Payment Ledger Entry”).
- Set self.sales\_person\_records from no value.
- Set self.filters.report\_date from getdate((self.filters.report\_date or nowdate())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.report\_date → nowdate().
- Set self.age\_as\_on from getdate(nowdate()) when (“age\_as\_on” does not belong to self.filters or self.filters.age\_as\_on equals “Today”), otherwise self.filters.report\_date.
  - Value choice on (“age\_as\_on” does not belong to self.filters or self.filters.age\_as\_on equals “Today”) — true gives getdate(nowdate()), false gives self.filters.report\_date.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “age\_as\_on” does not belong to self.filters → self.filters.age\_as\_on equals “Today”.
- If not self.filters.range.
  - Set self.filters.range from “30, 60, 90, 120”.
- Set self.ranges from list of num.strip() for num drawn from self.filters.range.split(“,”) where num.strip().isdigit().
  - Draw num from self.filters.range.split(“,”), keep a combination only if (num.strip().isdigit()).
- Set self.range\_numbers from list of num for num drawn from range(1, (len(self.ranges) + 2)).
  - Draw num from range(1, (len(self.ranges) + 2)).
- Set self.ple\_fetch\_method from (Platform.get\_single\_value(“Accounts Settings”, “receivable\_payable\_fetch\_method”) or “Buffered Cursor”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“Accounts Settings”, “receivable\_payable\_fetch\_method”) → “Buffered Cursor”.
- Set self.advance\_payment\_doctypes from (Platform.get\_hooks(“advance\_payment\_receivable\_doctypes”) + Platform.get\_hooks(“advance\_payment\_payable\_doctypes”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate() · configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “receivable\_payable\_fetch\_method”) · selected callable from Platform.get\_hooks(“advance\_payment\_receivable\_doctypes”), Platform.get\_hooks(“advance\_payment\_payable\_doctypes”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0215.json#L6812) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L584)

<a id="op-240bcf6c589c3a"></a>
### Receivable Payable Report.run

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_run`

**Inputs** self, args.

**Record and data access** read args.get(“naming\_by”) at 0 via get\_single\_value.

**Explicit results** tuple(self.columns, self.data, no value, self.chart, …).

**Local steps**

- Evaluate self.filters.update(args).
- Evaluate self.set\_defaults().
- Set self.party\_naming\_by from Platform.db.get\_single\_value(args.get(“naming\_by”) at 0, args.get(“naming\_by”) at 1).
- Evaluate self.get\_columns().
- Evaluate self.get\_data().
- Evaluate self.get\_chart\_data().
- Return tuple(self.columns, self.data, no value, self.chart, …).

**Methods declared on this owner** [set defaults](operations-006.md#op-3b955f0e2c336e), [get columns](operations-008.md#op-1515b81fcf1192), [get data](operations-006.md#op-a0e6b725aa4b74), [get chart data](operations-008.md#op-9de576d7c57741).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(args.get(“naming\_by”) at 0, args.get(“naming\_by”) at 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0215.json#L7464) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L590)

<a id="op-3b955f0e2c336e"></a>
### Receivable Payable Report.set defaults

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_set_defaults`

**Inputs** self.

**Record and data access** read “Global Defaults” via get\_single\_value · read “Company” via get\_cached\_value.

**Local steps**

- If not self.filters.get(“company”).
  - Set self.filters.company from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).
- Set self.company\_currency from Platform.get\_cached\_value(“Company”, self.filters.get(“company”), “default\_currency”).
- Set self.currency\_precision from (get\_currency\_precision() or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_currency\_precision() → 2.
- Set self.dr\_or\_cr from “debit” when self.filters.account\_type equals “Receivable”, otherwise “credit”.
  - Value choice on self.filters.account\_type equals “Receivable” — true gives “debit”, false gives “credit”.
- Set self.account\_type from self.filters.account\_type.
- Set self.party\_type from get\_party\_types\_from\_account\_type(self.account\_type).
- Set self.party\_details from mapping().
- Set self.invoices from set().
- Set self.sales\_person\_records from no value.
- Set self.skip\_total\_row from 0.
- Set self.advance\_payment\_doctypes from get\_advance\_payment\_doctypes().
- If self.filters.get(“group\_by\_party”).
  - Set self.previous\_party from empty text.
  - Set self.total\_row\_map from mapping().
  - Set self.skip\_total\_row from 1.
- If self.filters.get(“in\_party\_currency”).
  - If (self.filters.get(“party”) and len(self.filters.get(“party”)) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.get(“party”) → len(self.filters.get(“party”)) equals 1.
    - Set self.skip\_total\_row from 0.
  - Otherwise.
    - Set self.skip\_total\_row from 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”), Platform.get\_cached\_value(“Company”, self.filters.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L592)

<a id="op-a0e6b725aa4b74"></a>
### Receivable Payable Report.get data

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_data`

**Inputs** self.

**Local steps**

- Evaluate self.get\_sales\_invoices\_or\_customers\_based\_on\_sales\_person().
- Evaluate self.get\_invoices\_based\_on\_sales\_partner().
- Evaluate self.get\_invoice\_details().
- Evaluate self.get\_future\_payments().
- If (not self.filters.party\_type or self.filters.party\_type belongs to list(“Customer”, “Supplier”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.filters.party\_type → self.filters.party\_type belongs to list(“Customer”, “Supplier”).
  - Evaluate self.get\_return\_entries().
- Evaluate self.get\_exchange\_rate\_revaluations().
- Evaluate self.prepare\_ple\_query().
- Set self.data from list().
- Set self.voucher\_balance from OrderedDict().
- If self.ple\_fetch\_method equals “Buffered Cursor”.
  - Evaluate self.fetch\_ple\_in\_buffered\_cursor().
- Otherwise.
  - If self.ple\_fetch\_method equals “UnBuffered Cursor”.
    - Evaluate self.fetch\_ple\_in\_unbuffered\_cursor().
- Evaluate self.build\_delivery\_note\_map().
- Evaluate self.build\_data().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get sales invoices or customers based on sales person](operations-008.md#op-2e63a745d6cfe9), [get invoices based on sales partner](operations-008.md#op-297ec549d920ca), [get invoice details](operations-007.md#op-9d420f0976a28a), [get future payments](operations-007.md#op-9a60d202ab6990), [get return entries](operations-007.md#op-5d4119ed94abd1), [get exchange rate revaluations](operations-008.md#op-a842dce1e18780), [prepare ple query](operations-007.md#op-98b475fffa21fe), [fetch ple in buffered cursor](operations-006.md#op-f7d9c1340f894e), [fetch ple in unbuffered cursor](operations-006.md#op-52e8fd2ae9725d), [build delivery note map](operations-007.md#op-35cfd51083f59e), [build data](operations-007.md#op-13a01173089ebd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L697) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L570)

<a id="op-f7d9c1340f894e"></a>
### Receivable Payable Report.fetch ple in buffered cursor

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_fetch_ple_in_buffered_cursor`

**Inputs** self.

**Local steps**

- Set self.ple\_entries from self.ple\_query.run(as\_dict = true).
- For each ple in self.ple\_entries.
  - Evaluate self.init\_voucher\_balance(ple).
- For each ple in self.ple\_entries.
  - Evaluate self.update\_voucher\_balance(ple).
- Evaluate delattr(self, “ple\_entries”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [init voucher balance](operations-006.md#op-47eafe76bdee59), [update voucher balance](operations-006.md#op-3facb03e9c13d9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L1114) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L563)

<a id="op-52e8fd2ae9725d"></a>
### Receivable Payable Report.fetch ple in unbuffered cursor

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_fetch_ple_in_unbuffered_cursor`

**Inputs** self.

**Local steps**

- Set self.ple\_entries from list().
- Within Platform.db.unbuffered\_cursor().
  - For each ple in self.ple\_query.run(as\_dict = true, as\_iterator = true).
    - Evaluate self.init\_voucher\_balance(ple).
    - Evaluate self.ple\_entries.append(ple).
- For each ple in self.ple\_entries.
  - Evaluate self.update\_voucher\_balance(ple).
- Evaluate delattr(self, “ple\_entries”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [init voucher balance](operations-006.md#op-47eafe76bdee59), [update voucher balance](operations-006.md#op-3facb03e9c13d9).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L1299) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L564)

<a id="op-4fcdd429b6d956"></a>
### Receivable Payable Report.build voucher dict

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_build_voucher_mapping`

**Inputs** self, ple.

**Explicit results** Platform.\_dict(voucher\_type = ple.voucher\_type, voucher\_no = ple.voucher\_no, party = ple.party, party\_account = ple.account, …).

**Local steps**

- Return Platform.\_dict(voucher\_type = ple.voucher\_type, voucher\_no = ple.voucher\_no, party = ple.party, party\_account = ple.account, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L1548) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L561)

<a id="op-47eafe76bdee59"></a>
### Receivable Payable Report.init voucher balance

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_initialize_voucher_balance`

**Inputs** self, ple.

**Local steps**

- If self.filters.get(“ignore\_accounts”).
  - Set key from tuple(ple.voucher\_type, ple.voucher\_no, ple.party).
- Otherwise.
  - Set key from tuple(ple.account, ple.voucher\_type, ple.voucher\_no, ple.party).
- If key does not belong to self.voucher\_balance.
  - Set self.voucher\_balance at key from self.build\_voucher\_dict(ple).
- If ((ple.voucher\_type equals ple.against\_voucher\_type and ple.voucher\_no equals ple.against\_voucher\_no) or (ple.voucher\_type belongs to tuple(“Payment Entry”, “Journal Entry”) and ple.against\_voucher\_type bel ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (ple.voucher\_type equals ple.against\_voucher\_type and ple.voucher\_no equals ple.against\_voucher\_no) → (ple.voucher\_type belongs to tuple(“Payment Entry”, “Journal Entry”) and ple.against\_voucher\_type belongs to self.advance\_payment\_doctypes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ple.voucher\_type equals ple.against\_voucher\_type → ple.voucher\_no equals ple.against\_voucher\_no.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ple.voucher\_type belongs to tuple(“Payment Entry”, “Journal Entry”) → ple.against\_voucher\_type belongs to self.advance\_payment\_doctypes.
  - Set self.voucher\_balance at key.cost\_center from ple.cost\_center.
  - Set self.voucher\_balance at key.project from ple.project.
- Evaluate self.get\_invoices(ple).
- If self.filters.get(“group\_by\_party”).
  - Evaluate self.init\_subtotal\_row(ple.party).
- If (self.filters.get(“group\_by\_party”) and not self.filters.get(“in\_party\_currency”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.get(“group\_by\_party”) → not self.filters.get(“in\_party\_currency”).
  - Evaluate self.init\_subtotal\_row(“Total”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build voucher dict](operations-006.md#op-4fcdd429b6d956), [get invoices](operations-006.md#op-c5c93b81e0d3ec), [init subtotal row](operations-006.md#op-c0a2c8b1469f22).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L1781) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L586)

<a id="op-c5c93b81e0d3ec"></a>
### Receivable Payable Report.get invoices

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_invoices`

**Inputs** self, ple.

**Local steps**

- If ple.voucher\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
  - If self.sales\_person\_records is distinct from no value.
    - If (ple.voucher\_no belongs to self.sales\_person\_records.get(“Sales Invoice”, list()) or ple.party belongs to self.sales\_person\_records.get(“Customer”, list())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ple.voucher\_no belongs to self.sales\_person\_records.get(“Sales Invoice”, list()) → ple.party belongs to self.sales\_person\_records.get(“Customer”, list()).
      - Evaluate self.invoices.add(ple.voucher\_no).
  - Otherwise.
    - Evaluate self.invoices.add(ple.voucher\_no).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L2371) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L576)

<a id="op-c0a2c8b1469f22"></a>
### Receivable Payable Report.init subtotal row

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_initialize_subtotal_row`

**Inputs** self, party.

**Local steps**

- If not self.total\_row\_map.get(party).
  - Evaluate self.total\_row\_map.setdefault(party, mapping(“party” → party, “bold” → 1)).
  - For each field in self.get\_currency\_fields().
    - Set self.total\_row\_map at party at field from 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get currency fields](operations-006.md#op-ada6129f60dc83).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0216.json#L2650) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L585)

<a id="op-ada6129f60dc83"></a>
### Receivable Payable Report.get currency fields

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_currency_fields`

**Inputs** self.

**Explicit results** list(“invoiced”, “paid”, “credit\_note”, “outstanding”, …).

**Local steps**

- Return list(“invoiced”, “paid”, “credit\_note”, “outstanding”, …).
  - Draw i from list(0, expanded self.range\_numbers).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L569)

<a id="op-ed34018381bf0f"></a>
### Receivable Payable Report.get voucher balance

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_voucher_balance`

**Inputs** self, ple.

**Explicit results** no value · row.

**Local steps**

- If self.sales\_person\_records is distinct from no value.
  - If not (ple.party belongs to self.sales\_person\_records.get(“Customer”, list()) or ple.against\_voucher\_no belongs to self.sales\_person\_records.get(“Sales Invoice”, list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ple.party belongs to self.sales\_person\_records.get(“Customer”, list()) → ple.against\_voucher\_no belongs to self.sales\_person\_records.get(“Sales Invoice”, list()).
    - Return no value.
- If self.filters.get(“sales\_partner”).
  - If ple.against\_voucher\_no does not belong to self.sales\_partner\_invoices.
    - Return no value.
- If self.filters.get(“ignore\_accounts”).
  - Set key from tuple(ple.against\_voucher\_type, ple.against\_voucher\_no, ple.party).
- Otherwise.
  - Set key from tuple(ple.account, ple.against\_voucher\_type, ple.against\_voucher\_no, ple.party).
- If ple.against\_voucher\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
  - If ple.against\_voucher\_no belongs to self.return\_entries.
    - Set return\_against from self.return\_entries.get(ple.against\_voucher\_no).
    - If return\_against.
      - If self.filters.get(“ignore\_accounts”).
        - Set key from tuple(ple.against\_voucher\_type, return\_against, ple.party).
      - Otherwise.
        - Set key from tuple(ple.account, ple.against\_voucher\_type, return\_against, ple.party).
- Set row from self.voucher\_balance.get(key).
- If (not row and (ple.against\_voucher\_type equals “Payroll Entry” or (ple.against\_voucher\_type equals “Employee Advance” and self.filters.handle\_employee\_advances) or (ple.against\_voucher\_type equals “Exchange ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row → (ple.against\_voucher\_type equals “Payroll Entry” or (ple.against\_voucher\_type equals “Employee Advance” and self.filters.handle\_employee\_advances) or (ple.against\_voucher\_type equals “Exchange Rate Revalua ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ple.against\_voucher\_type equals “Payroll Entry” → (ple.against\_voucher\_type equals “Employee Advance” and self.filters.handle\_employee\_advances) → (ple.against\_voucher\_type equals “Exchange Rate Revaluation” and self.filters.for\_revaluation\_journals).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ple.against\_voucher\_type equals “Employee Advance” → self.filters.handle\_employee\_advances.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ple.against\_voucher\_type equals “Exchange Rate Revaluation” → self.filters.for\_revaluation\_journals.
  - Set \_d from self.build\_voucher\_dict(ple).
  - Set \_d.voucher\_type from ple.against\_voucher\_type.
  - Set \_d.voucher\_no from ple.against\_voucher\_no.
  - Set row, self.voucher\_balance at key from \_d.
- If not row.
  - If self.filters.get(“ignore\_accounts”).
    - Set row from self.voucher\_balance.get(tuple(ple.voucher\_type, ple.voucher\_no, ple.party)).
  - Otherwise.
    - Set row from self.voucher\_balance.get(tuple(ple.account, ple.voucher\_type, ple.voucher\_no, ple.party)).
- Set row.party\_type from ple.party\_type.
- Return row.

**Methods declared on this owner** [build voucher dict](operations-006.md#op-4fcdd429b6d956).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L583)

<a id="op-3facb03e9c13d9"></a>
### Receivable Payable Report.update voucher balance

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_update_voucher_balance`

**Inputs** self, ple.

**Explicit results** no value.

**Local steps**

- Set row from self.get\_voucher\_balance(ple).
- If not row.
  - Return no value.
- If (self.filters.get(“in\_party\_currency”) or self.filters.get(“party\_account”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“in\_party\_currency”) → self.filters.get(“party\_account”).
  - Set amount from ple.amount\_in\_account\_currency.
- Otherwise.
  - Set amount from ple.amount.
- Set amount\_in\_account\_currency from ple.amount\_in\_account\_currency.
- If ple.amount &gt; 0.
  - If (ple.voucher\_type belongs to list(“Journal Entry”, “Payment Entry”) and ple.voucher\_no differs from ple.against\_voucher\_no and ple.against\_voucher\_type differs from “Payroll Entry”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ple.voucher\_type belongs to list(“Journal Entry”, “Payment Entry”) → ple.voucher\_no differs from ple.against\_voucher\_no → ple.against\_voucher\_type differs from “Payroll Entry”.
    - Update row.paid using − amount.
    - Update row.paid\_in\_account\_currency using − amount\_in\_account\_currency.
  - Otherwise.
    - Update row.invoiced using + amount.
    - Update row.invoiced\_in\_account\_currency using + amount\_in\_account\_currency.
- Otherwise.
  - If self.is\_invoice(ple).
    - If (row.voucher\_no equals ple.voucher\_no equals ple.against\_voucher\_no and not self.is\_return(ple)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.voucher\_no equals ple.voucher\_no equals ple.against\_voucher\_no → not self.is\_return(ple).
      - Compare adjacent operands in order, stopping at the first false comparison in row.voucher\_no equals ple.voucher\_no equals ple.against\_voucher\_no.
      - Update row.paid using − amount.
      - Update row.paid\_in\_account\_currency using − amount\_in\_account\_currency.
    - Otherwise.
      - Update row.credit\_note using − amount.
      - Update row.credit\_note\_in\_account\_currency using − amount\_in\_account\_currency.
  - Otherwise.
    - Update row.paid using − amount.
    - Update row.paid\_in\_account\_currency using − amount\_in\_account\_currency.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get voucher balance](operations-006.md#op-ed34018381bf0f), [is invoice](operations-008.md#op-9338432b038ecb), [is return](operations-008.md#op-f326344dc15de6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L598)
