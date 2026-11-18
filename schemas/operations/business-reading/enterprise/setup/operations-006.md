# Company and master data · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email digest

[Record definition](../../../../data/record-types/email_digest.json)

<a id="op-62854fb5f89a6a"></a>
### Email Digest.get income year to date

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_income_year_to_date`

**Inputs** self.

**Explicit results** self.get\_year\_to\_date\_balance(“income”, “income”).

**Local steps**

- Return self.get\_year\_to\_date\_balance(“income”, “income”).

**Methods declared on this owner** [get year to date balance](operations-006.md#op-6a40ea30bab71f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0688.json#L2946) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L371)

<a id="op-19249a69cbc973"></a>
### Email Digest.get expense year to date

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_expense_year_to_date`

**Inputs** self.

**Explicit results** self.get\_year\_to\_date\_balance(“expense”, “expenses\_booked”).

**Local steps**

- Return self.get\_year\_to\_date\_balance(“expense”, “expenses\_booked”).

**Methods declared on this owner** [get year to date balance](operations-006.md#op-6a40ea30bab71f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0688.json#L3016) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L367)

<a id="op-6a40ea30bab71f"></a>
### Email Digest.get year to date balance

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_year_to_date_balance`

**Inputs** self, root\_type, fieldname.

**Explicit results** mapping(“label” → label, “value” → balance, “count” → count).

**Local steps**

- Set balance from 0.0.
- Set count from 0.
- Set fiscal\_year from get\_digest\_fiscal\_year(self.future\_to\_date).
- If fiscal\_year.
  - For each account in self.get\_root\_type\_accounts(root\_type).
    - Update balance using + get\_balance\_on(account, date = self.future\_to\_date, start\_date = fiscal\_year at 1).
    - Update count using + get\_count\_on(account, fieldname, date = self.future\_to\_date).
- If fieldname equals “income”.
  - Set filters from mapping(“currency” → self.currency).
  - Set label from get\_link\_to\_report(“Profit and Loss Statement”, label = translated self.meta.get\_label((root\_type + “\_year\_to\_date”)), filters = filters).
- Otherwise.
  - If fieldname equals “expenses\_booked”.
    - Set filters from mapping(“currency” → self.currency).
    - Set label from get\_link\_to\_report(“Profit and Loss Statement”, label = translated self.meta.get\_label((root\_type + “\_year\_to\_date”)), filters = filters).
- Return mapping(“label” → label, “value” → balance, “count” → count).

**Methods declared on this owner** [get root type accounts](operations-006.md#op-7e2854bbf661c8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L847) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L404)

<a id="op-3cfe088f6e45eb"></a>
### Email Digest.get bank balance

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_bank_balance`

**Inputs** self.

**Explicit results** self.get\_type\_balance(“bank\_balance”, “Bank”, root\_type = “Asset”).

**Local steps**

- Return self.get\_type\_balance(“bank\_balance”, “Bank”, root\_type = “Asset”).

**Methods declared on this owner** [get type balance](operations-006.md#op-db793f94c99f9d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0688.json#L3654) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L806) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L364)

<a id="op-10b675b8035b07"></a>
### Email Digest.get credit balance

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_credit_balance`

**Inputs** self.

**Explicit results** self.get\_type\_balance(“credit\_balance”, “Bank”, root\_type = “Liability”).

**Local steps**

- Return self.get\_type\_balance(“credit\_balance”, “Bank”, root\_type = “Liability”).

**Methods declared on this owner** [get type balance](operations-006.md#op-db793f94c99f9d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0688.json#L3740) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L366)

<a id="op-0ebdb6e17768af"></a>
### Email Digest.get payables

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_payables`

**Inputs** self.

**Explicit results** self.get\_type\_balance(“payables”, “Payable”).

**Local steps**

- Return self.get\_type\_balance(“payables”, “Payable”).

**Methods declared on this owner** [get type balance](operations-006.md#op-db793f94c99f9d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0688.json#L3821) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L821) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L379)

<a id="op-3c1339a09f2039"></a>
### Email Digest.get invoiced amount

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_invoiced_amount`

**Inputs** self.

**Explicit results** self.get\_type\_balance(“invoiced\_amount”, “Receivable”).

**Local steps**

- Return self.get\_type\_balance(“invoiced\_amount”, “Receivable”).

**Methods declared on this owner** [get type balance](operations-006.md#op-db793f94c99f9d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0688.json#L3886) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L372)

<a id="op-c2e8309cdd4cf0"></a>
### Email Digest.get expenses booked

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_expenses_booked`

**Inputs** self.

**Record and data access** read “Account” via get\_all.

**Explicit results** mapping(“label” → label, “value” → expenses, “last\_value” → past\_expenses, “count” → count).

**Local steps**

- Set tuple(expenses, past\_expenses, count) from self.get\_period\_amounts(self.get\_roots(“expense”), “expenses\_booked”).
- Set expense\_account from Platform.db.get\_all(“Account”, fields = list(“name”), filters = mapping(“root\_type” → “Expense”, “parent\_account” → empty text, “company” → self.company)).
- Set label from get\_link\_to\_report(“General Ledger”, translated self.meta.get\_label(“expenses\_booked”), filters = mapping(“company” → self.company, “from\_date” → self.future\_from\_date, “to\_date” → self.future\_to\_date, “ac ….
- Return mapping(“label” → label, “value” → expenses, “last\_value” → past\_expenses, “count” → count).

**Methods declared on this owner** [get period amounts](operations-006.md#op-764ba5967d03a1), [get roots](operations-006.md#op-da3be14bab2e42).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L810) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L368)

<a id="op-764ba5967d03a1"></a>
### Email Digest.get period amounts

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_period_amounts`

**Inputs** self, accounts, fieldname.

**Explicit results** tuple(balance, past\_balance, count).

**Local steps**

- Set balance, past\_balance from 0.0.
- Set count from 0.
- For each account in accounts.
  - Update balance using + get\_incomes\_expenses\_for\_period(account, self.future\_from\_date, self.future\_to\_date).
  - Update past\_balance using + get\_incomes\_expenses\_for\_period(account, self.past\_from\_date, self.past\_to\_date).
  - Update count using + get\_count\_for\_period(account, fieldname, self.future\_from\_date, self.future\_to\_date).
- Return tuple(balance, past\_balance, count).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0688.json#L4403) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L825) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L383)

<a id="op-01c972e78f4f09"></a>
### Email Digest.get sales orders to bill

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_sales_orders_to_bill`

**Inputs** self.

**Explicit results** mapping(“label” → label, “value” → value, “count” → count).

**Local steps**

- Set so from Platform.qb.DocType(“Sales Order”).
- Set tuple(value, count) from nested operand in the contract.select(nested operand in the contract(nested operand in the contract, nested operand in the contract), nested operand in the contract(nested operand in the contract)).where(( ….
- Set label from get\_link\_to\_report(“Sales Order”, label = translated self.meta.get\_label(“sales\_orders\_to\_bill”), report\_type = “Report Builder”, doctype = “Sales Order”, filters = mapping(“status” → list(list(“!=”, “Clos ….
- Return mapping(“label” → label, “value” → value, “count” → count).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L837) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L395)

<a id="op-315796ad278c64"></a>
### Email Digest.get sales orders to deliver

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_sales_orders_to_deliver`

**Inputs** self.

**Explicit results** mapping(“label” → label, “value” → value, “count” → count).

**Local steps**

- Set so from Platform.qb.DocType(“Sales Order”).
- Set tuple(value, count) from nested operand in the contract.select(nested operand in the contract(nested operand in the contract, nested operand in the contract), nested operand in the contract(nested operand in the contract)).where(( ….
- Set label from get\_link\_to\_report(“Sales Order”, label = translated self.meta.get\_label(“sales\_orders\_to\_deliver”), report\_type = “Report Builder”, doctype = “Sales Order”, filters = mapping(“status” → list(list(“!=”, “C ….
- Return mapping(“label” → label, “value” → value, “count” → count).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L838) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L396)

<a id="op-38a89b8c787475"></a>
### Email Digest.get purchase orders to receive

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_purchase_orders_to_receive`

**Inputs** self.

**Explicit results** mapping(“label” → label, “value” → value, “count” → count).

**Local steps**

- Set po from Platform.qb.DocType(“Purchase Order”).
- Set tuple(value, count) from nested operand in the contract.select(nested operand in the contract(nested operand in the contract, nested operand in the contract), nested operand in the contract(nested operand in the contract)).where(( ….
- Set label from get\_link\_to\_report(“Purchase Order”, label = translated self.meta.get\_label(“purchase\_orders\_to\_receive”), report\_type = “Report Builder”, doctype = “Purchase Order”, filters = mapping(“status” → list(list ….
- Return mapping(“label” → label, “value” → value, “count” → count).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L832) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L390)

<a id="op-6736825be9e50b"></a>
### Email Digest.get purchase orders to bill

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_purchase_orders_to_bill`

**Inputs** self.

**Explicit results** mapping(“label” → label, “value” → value, “count” → count).

**Local steps**

- Set po from Platform.qb.DocType(“Purchase Order”).
- Set tuple(value, count) from nested operand in the contract.select(nested operand in the contract(nested operand in the contract, nested operand in the contract), nested operand in the contract(nested operand in the contract)).where(( ….
- Set label from get\_link\_to\_report(“Purchase Order”, label = translated self.meta.get\_label(“purchase\_orders\_to\_bill”), report\_type = “Report Builder”, doctype = “Purchase Order”, filters = mapping(“status” → list(list(“! ….
- Return mapping(“label” → label, “value” → value, “count” → count).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L831) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L389)

<a id="op-db793f94c99f9d"></a>
### Email Digest.get type balance

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_type_balance`

**Inputs** self, fieldname, account\_type, root\_type = no value.

**Record and data access** read “Account” via get\_all.

**Explicit results** mapping(“label” → label, “value” → balance, “last\_value” → prev\_balance) · mapping(“label” → label, “value” → balance, “last\_value” → prev\_balance, “count” → count).

**Local steps**

- If root\_type.
  - Set accounts from list of d.name for d drawn from Platform.db.get\_all(“Account”, filters = mapping(“account\_type” → account\_type, “company” → self.company, “is\_group” → 0, “root\_type” → root\_type)).
    - Draw d from Platform.db.get\_all(“Account”, filters = mapping(“account\_type” → account\_type, “company” → self.company, “is\_group” → 0, “root\_type” → root\_type)).
- Otherwise.
  - Set accounts from list of d.name for d drawn from Platform.db.get\_all(“Account”, filters = mapping(“account\_type” → account\_type, “company” → self.company, “is\_group” → 0)).
    - Draw d from Platform.db.get\_all(“Account”, filters = mapping(“account\_type” → account\_type, “company” → self.company, “is\_group” → 0)).
- Set balance, prev\_balance from 0.0.
- Set count from 0.
- For each account in accounts.
  - Update balance using + get\_balance\_on(account, date = self.future\_to\_date, in\_account\_currency = false).
  - Update count using + get\_count\_on(account, fieldname, date = self.future\_to\_date).
  - Update prev\_balance using + get\_balance\_on(account, date = self.past\_to\_date, in\_account\_currency = false).
- If fieldname belongs to tuple(“bank\_balance”, “credit\_balance”).
  - Set label from empty text.
  - If fieldname equals “bank\_balance”.
    - Set filters from mapping(“root\_type” → “Asset”, “account\_type” → “Bank”, “report\_date” → self.future\_to\_date, “company” → self.company).
    - Set label from get\_link\_to\_report(“Account Balance”, label = translated self.meta.get\_label(fieldname), filters = filters).
  - Otherwise.
    - Set filters from mapping(“root\_type” → “Liability”, “account\_type” → “Bank”, “report\_date” → self.future\_to\_date, “company” → self.company).
    - Set label from get\_link\_to\_report(“Account Balance”, label = translated self.meta.get\_label(fieldname), filters = filters).
  - Return mapping(“label” → label, “value” → balance, “last\_value” → prev\_balance).
- Otherwise.
  - If account\_type equals “Payable”.
    - Set label from get\_link\_to\_report(“Accounts Payable”, label = translated self.meta.get\_label(fieldname), filters = mapping(“report\_date” → self.future\_to\_date, “company” → self.company)).
  - Otherwise.
    - If account\_type equals “Receivable”.
      - Set label from get\_link\_to\_report(“Accounts Receivable”, label = translated self.meta.get\_label(fieldname), filters = mapping(“report\_date” → self.future\_to\_date, “company” → self.company)).
    - Otherwise.
      - Set label from translated self.meta.get\_label(fieldname).
  - Return mapping(“label” → label, “value” → balance, “last\_value” → prev\_balance, “count” → count).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L845) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L403)

<a id="op-da3be14bab2e42"></a>
### Email Digest.get roots

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_roots`

**Inputs** self, root\_type.

**Record and data access** read “Account” via get\_all.

**Explicit results** list of d.name for d drawn from Platform.db.get\_all(“Account”, filters = mapping(“root\_type” → root\_type.title(), “company” → self.company, “is\_group” → 1, “parent\_account” → list(“in”, tuple(empty text, n ….

**Local steps**

- Return list of d.name for d drawn from Platform.db.get\_all(“Account”, filters = mapping(“root\_type” → root\_type.title(), “company” → self.company, “is\_group” → 1, “parent\_account” → list(“in”, tuple(empty text, n ….
  - Draw d from Platform.db.get\_all(“Account”, filters = mapping(“root\_type” → root\_type.title(), “company” → self.company, “is\_group” → 1, “parent\_account” → list(“in”, tuple(empty text, no value)))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2013) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L834) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L392)

<a id="op-7e2854bbf661c8"></a>
### Email Digest.get root type accounts

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_root_type_accounts`

**Inputs** self, root\_type.

**Record and data access** read “Account” via get\_all.

**Explicit results** self.\_accounts at root\_type.

**Local steps**

- If root\_type does not belong to self.\_accounts.
  - Set self.\_accounts at root\_type from list of d.name for d drawn from Platform.db.get\_all(“Account”, filters = mapping(“root\_type” → root\_type.title(), “company” → self.company, “is\_group” → 0)).
    - Draw d from Platform.db.get\_all(“Account”, filters = mapping(“root\_type” → root\_type.title(), “company” → self.company, “is\_group” → 0)).
- Return self.\_accounts at root\_type.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2214) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L833) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L391)

<a id="op-4385105d28eeb4"></a>
### Email Digest.get purchase order

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_purchase_order`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_doc(“Purchase Order”, “purchase\_order”).

**Local steps**

- Return self.get\_summary\_of\_doc(“Purchase Order”, “purchase\_order”).

**Methods declared on this owner** [get summary of doc](operations-007.md#op-1e2cdbb9f92f01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2443) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L829) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L387)

<a id="op-3419cadb487d93"></a>
### Email Digest.get sales order

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_sales_order`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_doc(“Sales Order”, “sales\_order”).

**Local steps**

- Return self.get\_summary\_of\_doc(“Sales Order”, “sales\_order”).

**Methods declared on this owner** [get summary of doc](operations-007.md#op-1e2cdbb9f92f01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2513) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L836) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L394)

<a id="op-8489cb1a9d1663"></a>
### Email Digest.get pending purchase orders

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_pending_purchase_orders`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_pending(“Purchase Order”, “pending\_purchase\_orders”, “per\_received”).

**Local steps**

- Return self.get\_summary\_of\_pending(“Purchase Order”, “pending\_purchase\_orders”, “per\_received”).

**Methods declared on this owner** [get summary of pending](operations-007.md#op-1f0f5fb052e809).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2583) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L822) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L380)

<a id="op-5a97cf07e9db90"></a>
### Email Digest.get pending sales orders

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_pending_sales_orders`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_pending(“Sales Order”, “pending\_sales\_orders”, “per\_delivered”).

**Local steps**

- Return self.get\_summary\_of\_pending(“Sales Order”, “pending\_sales\_orders”, “per\_delivered”).

**Methods declared on this owner** [get summary of pending](operations-007.md#op-1f0f5fb052e809).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2657) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L824) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L382)

<a id="op-a6300976b3b666"></a>
### Email Digest.get sales invoice

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_sales_invoice`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_doc(“Sales Invoice”, “sales\_invoice”).

**Local steps**

- Return self.get\_summary\_of\_doc(“Sales Invoice”, “sales\_invoice”).

**Methods declared on this owner** [get summary of doc](operations-007.md#op-1e2cdbb9f92f01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2731) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L835) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L393)

<a id="op-a4e54a5e93ce64"></a>
### Email Digest.get purchase invoice

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_purchase_invoice`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_doc(“Purchase Invoice”, “purchase\_invoice”).

**Local steps**

- Return self.get\_summary\_of\_doc(“Purchase Invoice”, “purchase\_invoice”).

**Methods declared on this owner** [get summary of doc](operations-007.md#op-1e2cdbb9f92f01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2801) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L828) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L386)

<a id="op-4bdadc6812ddd8"></a>
### Email Digest.get new quotations

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_new_quotations`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_doc(“Quotation”, “new\_quotations”).

**Local steps**

- Return self.get\_summary\_of\_doc(“Quotation”, “new\_quotations”).

**Methods declared on this owner** [get summary of doc](operations-007.md#op-1e2cdbb9f92f01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2871) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L376)

<a id="op-3279083fb2c8c5"></a>
### Email Digest.get pending quotations

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_pending_quotations`

**Inputs** self.

**Explicit results** self.get\_summary\_of\_pending\_quotations(“pending\_quotations”).

**Local steps**

- Return self.get\_summary\_of\_pending\_quotations(“pending\_quotations”).

**Methods declared on this owner** [get summary of pending quotations](operations-007.md#op-27e1ed4bab7735).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L2941) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L823) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L381)
