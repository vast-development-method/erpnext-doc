# Accounting and settlement · operations 62

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Party

<a id="op-f6513d79a9886e"></a>
### Get party account currency.generator

`operation_enterprise_accounts_party_business_behavior_get_party_account_currency_generator`

**Inputs** no declared parameters.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Account”, party\_account, “account\_currency”).

**Local steps**

- Set party\_account from find\_party\_account(party\_type, party, company).
- Return Platform.get\_cached\_value(“Account”, party\_account, “account\_currency”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, party\_account, “account\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L61)

<a id="op-fa50ee4ad8f5dd"></a>
### Get party gle currency

`operation_enterprise_accounts_party_business_behavior_get_party_general_ledger_entry_currency`

**Inputs** party\_type, party, company.

**Explicit results** Platform.local\_cache(“party\_gle\_currency”, tuple(party\_type, party, company), generator, regenerate\_if\_none = true).

**Local steps**

- Bind local operation generator for subsequent calls.
- Return Platform.local\_cache(“party\_gle\_currency”, tuple(party\_type, party, company), generator, regenerate\_if\_none = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L6229) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L67)

<a id="op-f3d705cb94e898"></a>
### Get party gle currency.generator

`operation_enterprise_accounts_party_business_behavior_get_party_general_ledger_entry_currency_generator`

**Inputs** no declared parameters.

**Explicit results** existing\_gle\_currency at 0 at 0 when existing\_gle\_currency, otherwise no value.

**Local steps**

- Set gl from qb.DocType(“GL Entry”).
- Set existing\_gle\_currency from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….run().
- Return existing\_gle\_currency at 0 at 0 when existing\_gle\_currency, otherwise no value.
  - Value choice on existing\_gle\_currency — true gives existing\_gle\_currency at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L6610) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L68)

<a id="op-94e78524e405ad"></a>
### Get party gle account

`operation_enterprise_accounts_party_business_behavior_get_party_general_ledger_entry_account`

**Inputs** party\_type, party, company.

**Explicit results** Platform.local\_cache(“party\_gle\_account”, tuple(party\_type, party, company), generator, regenerate\_if\_none = true).

**Local steps**

- Bind local operation generator for subsequent calls.
- Return Platform.local\_cache(“party\_gle\_account”, tuple(party\_type, party, company), generator, regenerate\_if\_none = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L6902) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L65)

<a id="op-0283a7ac4168f7"></a>
### Get party gle account.generator

`operation_enterprise_accounts_party_business_behavior_get_party_general_ledger_entry_account_generator`

**Inputs** no declared parameters.

**Explicit results** existing\_gle\_account at 0 at 0 when existing\_gle\_account, otherwise no value.

**Local steps**

- Set gl from qb.DocType(“GL Entry”).
- Set existing\_gle\_account from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….run().
- Return existing\_gle\_account at 0 at 0 when existing\_gle\_account, otherwise no value.
  - Value choice on existing\_gle\_account — true gives existing\_gle\_account at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0213.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L66)

<a id="op-7a21e5571b0fef"></a>
### Validate party gle currency

`operation_enterprise_accounts_party_business_behavior_validate_party_general_ledger_entry_currency`

**Inputs** party\_type, party, company, party\_account\_currency = no value.

**Explicit failure paths** validation helper with InvalidAccountCurrency — translated “{0} {1} has accounting entries in currency {2} for company {3}. Please select a receivable or payable accoun …”.format(Platform.bold(party\_type), Platform.bold(party), Platform.bold(existing\_gl ….

**Local steps**

- If not party\_account\_currency.
  - Set party\_account\_currency from get\_party\_account\_currency(party\_type, party, company).
- Set existing\_gle\_currency from get\_party\_gle\_currency(party\_type, party, company).
- If (existing\_gle\_currency and party\_account\_currency differs from existing\_gle\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing\_gle\_currency → party\_account\_currency differs from existing\_gle\_currency.
  - Call the validation error handler Platform.throw(translated “{0} {1} has accounting entries in currency {2} for company {3}. Please select a receivable or payable accoun …”.format(Platform.bold(party\_type), Platform.bold(party), Platform.b ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0213.json#L298) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L87)

<a id="op-1fe45e026799a4"></a>
### Validate party accounts

`operation_enterprise_accounts_party_business_behavior_validate_party_accounts`

**Inputs** doc.

**Record and data access** read “Account” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Billing currency must be equal to either default company's currency or party account currency”.

**Local steps**

- Evaluate validate\_party\_account\_rows(doc, “Customer” when doc.doctype equals “Customer Group”, otherwise doc.doctype).
  - Value choice on doc.doctype equals “Customer Group” — true gives “Customer”, false gives doc.doctype.
- For each account in doc.get(“accounts”).
  - Set party\_account\_currency from Platform.get\_cached\_value(“Account”, account.account, “account\_currency”).
  - If Platform.db.get\_default(“Company”).
    - Set company\_default\_currency from Platform.get\_cached\_value(“Company”, Platform.db.get\_default(“Company”), “default\_currency”).
  - Otherwise.
    - Set company\_default\_currency from Platform.get\_cached\_value(“Company”, account.company, “default\_currency”).
  - Evaluate validate\_party\_gle\_currency(doc.doctype, doc.name, account.company, party\_account\_currency).
  - If (doc.get(“default\_currency”) and party\_account\_currency and company\_default\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“default\_currency”) → party\_account\_currency → company\_default\_currency.
    - If (doc.default\_currency differs from party\_account\_currency and doc.default\_currency differs from company\_default\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.default\_currency differs from party\_account\_currency → doc.default\_currency differs from company\_default\_currency.
      - Call the validation error handler Platform.throw(translated “Billing currency must be equal to either default company's currency or party account currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account.account, “account\_currency”), Platform.get\_cached\_value(“Company”, Platform.db.get\_default(“Company”), “default\_currency”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L83)

<a id="op-fdd1b747379c34"></a>
### Validate party account rows

`operation_enterprise_binding_enterprise_accounts_party_validate_party_account_rows`

**Inputs** doc, party\_type.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper with DuplicatePartyAccountError — translated “There can only be 1 Account per Company in {0} {1}”.format(doc.doctype, doc.name) · validation helper — translated “Row {0}: Account {1} is disabled”.format(row.idx, Platform.bold(account)).

**Local steps**

- Bind dependencies validate\_account\_head.
- Set companies from set().
- For each row in doc.get(“accounts”).
  - If row.company belongs to companies.
    - Call the validation error handler Platform.throw(translated “There can only be 1 Account per Company in {0} {1}”.format(doc.doctype, doc.name), DuplicatePartyAccountError).
  - Evaluate companies.add(row.company).
  - For each tuple(account, context) in tuple(tuple(row.account, translated “Debtor/Creditor”), tuple(row.advance\_account, translated “Debtor/Creditor Advance”)).
    - If not account.
      - Continue with the next iteration or loop test.
    - Evaluate validate\_account\_head(row.idx, account, row.company, context).
    - If Platform.get\_cached\_value(“Account”, account, “disabled”).
      - Call the validation error handler Platform.throw(translated “Row {0}: Account {1} is disabled”.format(row.idx, Platform.bold(account)), title = translated “Invalid Account”).
  - Evaluate validate\_party\_account\_type(party\_type, row).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “disabled”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1107)

<a id="op-c15a3098ee5cca"></a>
### Validate party account type

`operation_enterprise_binding_enterprise_accounts_party_validate_party_account_type`

**Inputs** party\_type, row.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Account {1} must be a {2} account”.format(row.idx, Platform.bold(account), translated account\_type).

**Local steps**

- Set account\_type from Enterprise.get\_party\_account\_type(party\_type).
- For each account in tuple(row.account, row.advance\_account).
  - If (account and Platform.get\_cached\_value(“Account”, account, “account\_type”) differs from account\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account → Platform.get\_cached\_value(“Account”, account, “account\_type”) differs from account\_type.
    - Call the validation error handler Platform.throw(translated “Row {0}: Account {1} must be a {2} account”.format(row.idx, Platform.bold(account), translated account\_type), title = translated “Invalid Account”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1108)

<a id="op-36721ba5cea02e"></a>
### Get due date

`operation_enterprise_accounts_party_business_behavior_get_due_date`

**Inputs** posting\_date, party\_type, party, company = no value, bill\_date = no value, template\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read party\_type via get\_cached\_value · read “Supplier Group” via get\_cached\_value.

**Explicit results** due\_date.

**Local steps**

- Set due\_date from no value.
- If ((bill\_date or posting\_date) and party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (bill\_date or posting\_date) → party.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bill\_date → posting\_date.
  - Set due\_date from (bill\_date or posting\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bill\_date → posting\_date.
  - If not template\_name.
    - Set template\_name from get\_payment\_terms\_template(party, party\_type, company).
  - If template\_name.
    - Set due\_date from get\_due\_date\_from\_template(template\_name, posting\_date, bill\_date).strftime(“%Y-%m-%d”).
  - Otherwise.
    - If party\_type equals “Supplier”.
      - Set supplier\_group from Platform.get\_cached\_value(party\_type, party, “supplier\_group”).
      - Set template\_name from Platform.get\_cached\_value(“Supplier Group”, supplier\_group, “payment\_terms”).
      - If template\_name.
        - Set due\_date from get\_due\_date\_from\_template(template\_name, posting\_date, bill\_date).strftime(“%Y-%m-%d”).
- If getdate(due\_date) &lt; getdate(posting\_date).
  - Set due\_date from posting\_date.
- Return due\_date.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(party\_type, party, “supplier\_group”), Platform.get\_cached\_value(“Supplier Group”, supplier\_group, “payment\_terms”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L57)

<a id="op-45346d402c56bd"></a>
### Get due date from template

`operation_enterprise_accounts_party_business_behavior_get_due_date_from_template`

**Inputs** template\_name, posting\_date, bill\_date.

**Record and data access** resolve a document from “Payment Terms Template” via get\_doc.

**Explicit results** due\_date.

**Local steps**

- Set due\_date from getdate((bill\_date or posting\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bill\_date → posting\_date.
- Set template from Platform.get\_doc(“Payment Terms Template”, template\_name).
- For each term in template.terms.
  - If term.due\_date\_based\_on equals “Day(s) after invoice date”.
    - Set due\_date from max(due\_date, add\_days(due\_date, term.credit\_days)).
  - Otherwise.
    - If term.due\_date\_based\_on equals “Day(s) after the end of the invoice month”.
      - Set due\_date from max(due\_date, add\_days(get\_last\_day(due\_date), term.credit\_days)).
    - Otherwise.
      - Set due\_date from max(due\_date, get\_last\_day(add\_months(due\_date, term.credit\_months))).
- Return due\_date.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0213.json#L1959) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L58)

<a id="op-624af3ace7c081"></a>
### Validate due date

`operation_enterprise_accounts_party_business_behavior_validate_due_date`

**Inputs** posting\_date, due\_date, bill\_date = no value, template\_name = no value, doctype = no value.

**Explicit failure paths** validation helper — translated “Due Date cannot be before {0}”.format(doctype\_date).

**Local steps**

- If getdate(due\_date) &lt; getdate(posting\_date).
  - Set doctype\_date from “Date”.
  - If doctype equals “Purchase Invoice”.
    - Set doctype\_date from “Supplier Invoice Date”.
  - If doctype equals “Sales Invoice”.
    - Set doctype\_date from “Posting Date”.
  - Call the validation error handler Platform.throw(translated “Due Date cannot be before {0}”.format(doctype\_date)).
- Otherwise.
  - Evaluate validate\_due\_date\_with\_template(posting\_date, due\_date, bill\_date, template\_name, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0213.json#L2337) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L81)

<a id="op-e7dc1aa8ac7269"></a>
### Validate due date with template

`operation_enterprise_accounts_party_business_behavior_validate_due_date_with_template`

**Inputs** posting\_date, due\_date, bill\_date, template\_name, doctype = no value.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Due Date cannot be after {0}”.format(formatdate(default\_due\_date)).

**Local steps**

- If not template\_name.
  - Return no value.
- Set default\_due\_date from format(get\_due\_date\_from\_template(template\_name, posting\_date, bill\_date)).
- If not default\_due\_date.
  - Return no value.
- If (getdate(default\_due\_date) differs from getdate(posting\_date) and getdate(due\_date) &gt; getdate(default\_due\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(default\_due\_date) differs from getdate(posting\_date) → getdate(due\_date) &gt; getdate(default\_due\_date).
  - If Platform.get\_single\_value(“Accounts Settings”, “credit\_controller”) belongs to Platform.get\_roles().
    - Set party\_type from “supplier” when doctype equals “Purchase Invoice”, otherwise “customer”.
      - Value choice on doctype equals “Purchase Invoice” — true gives “supplier”, false gives “customer”.
    - Evaluate msgprint(translated “Note: Due Date exceeds allowed {0} credit days by {1} day(s)”.format(party\_type, date\_diff(due\_date, default\_due\_date))).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Due Date cannot be after {0}”.format(formatdate(default\_due\_date))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “credit\_controller”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0213.json#L2641) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L89) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L82)

<a id="op-16d03aa82aa7fe"></a>
### Get address tax category

`operation_enterprise_accounts_party_business_behavior_get_address_tax_category`

**Inputs** tax\_category = no value, billing\_address = no value, shipping\_address = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Address” via get\_value.

**Explicit results** cstr(tax\_category).

**Local steps**

- Set addr\_tax\_category\_from from Platform.get\_single\_value(“Accounts Settings”, “determine\_address\_tax\_category\_from”).
- If addr\_tax\_category\_from equals “Shipping Address”.
  - If shipping\_address.
    - Set tax\_category from (Platform.db.get\_value(“Address”, shipping\_address, “tax\_category”) or tax\_category).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Address”, shipping\_address, “tax\_category”) → tax\_category.
- Otherwise.
  - If billing\_address.
    - Set tax\_category from (Platform.db.get\_value(“Address”, billing\_address, “tax\_category”) or tax\_category).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Address”, billing\_address, “tax\_category”) → tax\_category.
- Return cstr(tax\_category).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “determine\_address\_tax\_category\_from”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L53)

<a id="op-a59031e627b8f4"></a>
### Set taxes

`operation_enterprise_accounts_party_business_behavior_set_taxes`

**Inputs** party, party\_type, posting\_date, company, customer\_group = no value, supplier\_group = no value, tax\_category = no value, billing\_address = no value, shipping\_address = no value, use\_for\_shopping\_cart = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_tax\_template(posting\_date, args).

**Local steps**

- Bind dependencies get\_tax\_rule\_party\_details, get\_tax\_template.
- Set args from mapping(Platform.scrub(party\_type) → party, “company” → company).
- If tax\_category.
  - Set args at “tax\_category” from tax\_category.
- If customer\_group.
  - Set args at “customer\_group” from customer\_group.
- If supplier\_group.
  - Set args at “supplier\_group” from supplier\_group.
- If (billing\_address or shipping\_address).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in billing\_address → shipping\_address.
  - Evaluate args.update(get\_tax\_rule\_party\_details(party, party\_type, mapping(“billing\_address” → billing\_address, “shipping\_address” → shipping\_address))).
- Otherwise.
  - Evaluate args.update(get\_tax\_rule\_party\_details(party, party\_type)).
- If party\_type belongs to tuple(“Customer”, “Lead”, “Prospect”, “CRM Deal”).
  - Evaluate args.update(mapping(“tax\_type” → “Sales”)).
  - If party\_type belongs to list(“Lead”, “Prospect”, “CRM Deal”).
    - Set args at “customer” from no value.
    - Remove args at Platform.scrub(party\_type).
- Otherwise.
  - Evaluate args.update(mapping(“tax\_type” → “Purchase”)).
- If use\_for\_shopping\_cart.
  - Evaluate args.update(mapping(“use\_for\_shopping\_cart” → cint(use\_for\_shopping\_cart))).
- Return get\_tax\_template(posting\_date, args).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L86) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L79)

<a id="op-6d86536e014309"></a>
### Get payment terms template

`operation_enterprise_accounts_party_business_behavior_get_payment_terms_template`

**Inputs** party\_name, party\_type, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Customer” via get\_cached\_value · read “Customer Group” via get\_cached\_value · read “Supplier” via get\_cached\_value · read “Supplier Group” via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** no value · template.

**Local steps**

- If party\_type does not belong to tuple(“Customer”, “Supplier”).
  - Return no value.
- Set template from no value.
- If party\_type equals “Customer”.
  - Set customer from Platform.get\_cached\_value(“Customer”, party\_name, fieldname = list(“payment\_terms”, “customer\_group”), as\_dict = 1).
  - Set template from customer.payment\_terms.
  - If (not template and customer.customer\_group).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not template → customer.customer\_group.
    - Set template from Platform.get\_cached\_value(“Customer Group”, customer.customer\_group, “payment\_terms”).
- Otherwise.
  - Set supplier from Platform.get\_cached\_value(“Supplier”, party\_name, fieldname = list(“payment\_terms”, “supplier\_group”), as\_dict = 1).
  - Set template from supplier.payment\_terms.
  - If (not template and supplier.supplier\_group).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not template → supplier.supplier\_group.
    - Set template from Platform.get\_cached\_value(“Supplier Group”, supplier.supplier\_group, “payment\_terms”).
- If (not template and company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not template → company.
  - Set template from Platform.get\_cached\_value(“Company”, company, fieldname = “payment\_terms”).
- Return template.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer”, party\_name, fieldname = list(“payment\_terms”, “customer\_group”), as\_dict = 1), Platform.get\_cached\_value(“Customer Group”, customer.customer\_group, “payment\_terms”) and 3 further calls.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L71)

<a id="op-95ea8cc5b946f9"></a>
### Validate party frozen disabled

`operation_enterprise_accounts_party_business_behavior_validate_party_frozen_disabled`

**Inputs** company, party\_type, party\_name.

**Record and data access** read party\_type via get\_cached\_value · read “Company” via get\_cached\_value · read “Employee” via get\_value.

**State and service calls** msgprint with translated “{0} {1} is not active”.format(party\_type, party\_name).

**Explicit results** no value.

**Explicit failure paths** validation helper with PartyDisabled — translated “{0} {1} is disabled”.format(party\_type, party\_name) · validation helper with PartyFrozen — translated “{0} {1} is frozen”.format(party\_type, party\_name).

**Local steps**

- If Platform.flags.ignore\_party\_validation.
  - Return no value.
- If (party\_type and party\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party\_name.
  - If party\_type belongs to tuple(“Customer”, “Supplier”).
    - Set party from Platform.get\_cached\_value(party\_type, party\_name, list(“is\_frozen”, “disabled”), as\_dict = true).
    - If party.disabled.
      - Call the validation error handler Platform.throw(translated “{0} {1} is disabled”.format(party\_type, party\_name), PartyDisabled).
    - Otherwise.
      - If party.get(“is\_frozen”).
        - Set role\_allowed\_for\_frozen\_entries from Platform.get\_cached\_value(“Company”, company, “role\_allowed\_for\_frozen\_entries”).
        - If role\_allowed\_for\_frozen\_entries does not belong to Platform.get\_roles().
          - Call the validation error handler Platform.throw(translated “{0} {1} is frozen”.format(party\_type, party\_name), PartyFrozen).
  - Otherwise.
    - If party\_type equals “Employee”.
      - If Platform.db.get\_value(“Employee”, party\_name, “status”) differs from “Active”.
        - Evaluate Platform.msgprint(translated “{0} {1} is not active”.format(party\_type, party\_name), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(party\_type, party\_name, list(“is\_frozen”, “disabled”), as\_dict = true), Platform.get\_cached\_value(“Company”, company, “role\_allowed\_for\_frozen\_entries”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0213.json#L4989) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L86)

<a id="op-79c37ba27e426f"></a>
### Validate account party type

`operation_enterprise_accounts_party_business_behavior_validate_account_party_type`

**Inputs** self.

**Record and data access** read “Party Type” via exists · read “Account” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is not a valid Party Type”.format(self.party\_type) · validation helper — translated “Party Type and Party can only be set for Receivable / Payable account&lt;br&gt;&lt;br&gt;{0}”.format(self.account).

**Local steps**

- If self.is\_cancelled.
  - Return no value.
- If (not self.flags.from\_reversal and self.party\_type and not Platform.db.exists(“Party Type”, self.party\_type)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.from\_reversal → self.party\_type → not Platform.db.exists(“Party Type”, self.party\_type).
  - Call the validation error handler Platform.throw(translated “{0} is not a valid Party Type”.format(self.party\_type)).
- If (self.party\_type and self.party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party\_type → self.party.
  - Set account\_type from Platform.get\_cached\_value(“Account”, self.account, “account\_type”).
  - If (account\_type and account\_type does not belong to list(“Receivable”, “Payable”, “Equity”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type → account\_type does not belong to list(“Receivable”, “Payable”, “Equity”).
    - Call the validation error handler Platform.throw(translated “Party Type and Party can only be set for Receivable / Payable account&lt;br&gt;&lt;br&gt;{0}”.format(self.account)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L87) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L80)

<a id="op-cc36c0b9f34dc9"></a>
### Get dashboard info

`operation_enterprise_accounts_party_business_behavior_get_dashboard_info`

**Inputs** party\_type, party, loyalty\_program = no value.

**Record and data access** read doctype via get\_list · read doctype via get\_all · read “Loyalty Point Entry” via get\_all · execute query text (SELECT, GL Entry) · read “Company” via get\_cached\_value.

**Explicit results** no value · company\_wise\_info.

**Local steps**

- Set doctype from “Sales Invoice” when party\_type equals “Customer”, otherwise “Purchase Invoice”.
  - Value choice on party\_type equals “Customer” — true gives “Sales Invoice”, false gives “Purchase Invoice”.
- If not Platform.has\_permission(doctype, “read”, ignore\_share\_permissions = true).
  - Return no value.
- Set current\_fiscal\_year from get\_fiscal\_year(nowdate(), as\_dict = true).
- Set companies from Platform.get\_list(doctype, filters = mapping(“docstatus” → 1, party\_type.lower() → party), distinct = 1, fields = list(“company”)).
- Set company\_wise\_info from list().
- Set company\_wise\_grand\_total from Platform.get\_all(doctype, filters = mapping(“docstatus” → 1, party\_type.lower() → party, “posting\_date” → tuple(“between”, list(current\_fiscal\_year.year\_start\_date, current\_fiscal\_year.year\_end\_date))), gr ….
- Set loyalty\_point\_details from list().
- If party\_type equals “Customer”.
  - Set loyalty\_point\_details from Platform.\_dict(Platform.get\_all(“Loyalty Point Entry”, filters = mapping(“customer” → party, “expiry\_date” → tuple(“&gt;=”, getdate())), group\_by = “company”, fields = list(“company”, mapping(“SUM” → “loyalty ….
- Set company\_wise\_billing\_this\_year from Platform.\_dict().
- For each d in company\_wise\_grand\_total.
  - Evaluate company\_wise\_billing\_this\_year.setdefault(d.company, mapping(“grand\_total” → d.grand\_total, “base\_grand\_total” → d.base\_grand\_total)).
- Set company\_wise\_total\_unpaid from Platform.\_dict(Platform.db.sql(query text (SELECT, GL Entry), tuple(party\_type, party))).
- For each d in companies.
  - Set company\_default\_currency from Platform.get\_cached\_value(“Company”, d.company, “default\_currency”).
  - Set party\_account\_currency from get\_party\_account\_currency(party\_type, party, d.company).
  - If party\_account\_currency equals company\_default\_currency.
    - Set billing\_this\_year from flt(company\_wise\_billing\_this\_year.get(d.company, mapping()).get(“base\_grand\_total”)).
  - Otherwise.
    - Set billing\_this\_year from flt(company\_wise\_billing\_this\_year.get(d.company, mapping()).get(“grand\_total”)).
  - Set total\_unpaid from flt(company\_wise\_total\_unpaid.get(d.company)).
  - If loyalty\_point\_details.
    - Set loyalty\_points from loyalty\_point\_details.get(d.company).
  - Set info from mapping().
  - Set info at “billing\_this\_year” from flt(billing\_this\_year) when billing\_this\_year, otherwise 0.
    - Value choice on billing\_this\_year — true gives flt(billing\_this\_year), false gives 0.
  - Set info at “currency” from party\_account\_currency.
  - Set info at “total\_unpaid” from flt(total\_unpaid) when total\_unpaid, otherwise 0.
    - Value choice on total\_unpaid — true gives flt(total\_unpaid), false gives 0.
  - Set info at “company” from d.company.
  - If (party\_type equals “Customer” and loyalty\_point\_details).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type equals “Customer” → loyalty\_point\_details.
    - Set info at “loyalty\_points” from loyalty\_points.
  - If party\_type equals “Supplier”.
    - Set info at “total\_unpaid” from (negative 1 × info at “total\_unpaid”).
  - If info at “total\_unpaid” &lt; 0.
    - Set info at “balance\_label” from “Total Advance Paid” when party\_type equals “Supplier”, otherwise “Total Advance Received”.
      - Value choice on party\_type equals “Supplier” — true gives “Total Advance Paid”, false gives “Total Advance Received”.
    - Set info at “balance\_amount” from abs(info at “total\_unpaid”).
  - Otherwise.
    - Set info at “balance\_label” from “Total Unpaid”.
    - Set info at “balance\_amount” from info at “total\_unpaid”.
  - Evaluate company\_wise\_info.append(info).
- Return company\_wise\_info.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, ignore\_share\_permissions = true) · clock or generated value from nowdate() · configured or stored value from Platform.get\_cached\_value(“Company”, d.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L54)

<a id="op-997d89166a906c"></a>
### Get party shipping address

`operation_enterprise_accounts_party_business_behavior_get_party_shipping_address`

**Inputs** doctype, name.

**Declared result** (str bitwise or no value).

**Record and data access** read “Address” via get\_all.

**Explicit results** shipping\_addresses at 0.name · no value.

**Local steps**

- Set shipping\_addresses from Platform.get\_all(“Address”, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, name), list(“disabled”, “=”, 0)), or\_filters = list(list(“is\_shipping\_a ….
- If (shipping\_addresses and shipping\_addresses at 0.is\_shipping\_address equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in shipping\_addresses → shipping\_addresses at 0.is\_shipping\_address equals 1.
  - Return shipping\_addresses at 0.name.
- If len(shipping\_addresses) equals 1.
  - Return shipping\_addresses at 0.name.
- Otherwise.
  - Return no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L1975) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L69)

<a id="op-6401a7443d66ef"></a>
### Get partywise advanced payment amount

`operation_enterprise_accounts_party_business_behavior_get_partywise_advanced_payment_amount`

**Inputs** party\_type, posting\_date = no value, future\_payment = 0, company = no value, party = no value.

**Record and data access** read “Party Type” via get\_cached\_value.

**Explicit results** data.

**Local steps**

- Set account\_type from Platform.get\_cached\_value(“Party Type”, party\_type, “account\_type”).
- Set ple from Platform.qb.DocType(“Payment Ledger Entry”).
- Set acc from Platform.qb.DocType(“Account”).
- Set query from nested operand in the contract(nested operand in the contract).select(ple.party).where(((nested operand in the contract.isin(party\_type) bitwise and nested operand in the contract.account\_type equals accou ….
- If posting\_date.
  - If future\_payment.
    - Set query from query.where((ple.posting\_date ≤ posting\_date bitwise or Date(ple.creation) ≤ posting\_date)).
  - Otherwise.
    - Set query from query.where(ple.posting\_date ≤ posting\_date).
- If company.
  - Set query from query.where(ple.company equals company).
- If party.
  - Set query from query.where(ple.party equals party).
- If invoice\_doctypes bound to Platform.get\_hooks(“invoice\_doctypes”).
  - Set query from query.where(ple.voucher\_type.notin(invoice\_doctypes)).
- Set party\_ledger from query.select(Abs(Sum(ple.amount).as\_(“amount”))).
- Set party\_ledger from party\_ledger.where(ple.amount &lt; 0).
- Set party\_ledger from party\_ledger.where(ple.against\_voucher\_no equals ple.voucher\_no).
- Set party\_ledger from party\_ledger.where(acc.root\_type equals “Liability” when account\_type equals “Payable”, otherwise “Asset”).
  - Value choice on account\_type equals “Payable” — true gives “Liability”, false gives “Asset”.
- Set data from party\_ledger.run().
- Set data from Platform.\_dict((data or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data → mapping().
- Set advance\_ledger from query.select(Sum(ple.amount).as\_(“amount”), ple.account).
- Set advance\_ledger from advance\_ledger.where(acc.root\_type equals “Asset” when account\_type equals “Payable”, otherwise “Liability”).
  - Value choice on account\_type equals “Payable” — true gives “Asset”, false gives “Liability”.
- Set advance\_ledger from advance\_ledger.groupby(ple.account).
- Set advance\_ledger from advance\_ledger.having(Sum(ple.amount) &lt; 0).
- Set advance\_data from advance\_ledger.run().
- For each row in advance\_data.
  - Evaluate data.setdefault(row at 0, 0).
  - Update data at row at 0 using + abs(row at 1).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Party Type”, party\_type, “account\_type”) · selected callable from Platform.get\_hooks(“invoice\_doctypes”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L2380) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L70)

<a id="op-283569db4949ab"></a>
### Get default contact

`operation_enterprise_accounts_party_business_behavior_get_default_contact`

**Inputs** doctype, name.

**Declared result** (str bitwise or no value).

**Record and data access** read “Contact” via get\_all.

**Explicit results** contacts at 0 when contacts, otherwise no value.

**Local steps**

- Set contacts from Platform.get\_all(“Contact”, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, name)), or\_filters = list(list(“is\_primary\_contact”, “=”, 1), list(“is\_ ….
- Return contacts at 0 when contacts, otherwise no value.
  - Value choice on contacts — true gives contacts at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L3788) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L55)

<a id="op-b9efff1e15a946"></a>
### Add party account

`operation_enterprise_accounts_party_business_behavior_add_party_account`

**Inputs** party\_type, party, company, account.

**Record and data access** resolve a document from party\_type via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set doc from Platform.get\_doc(party\_type, party).
- Set account\_exists from false.
- For each d in doc.get(“accounts”).
  - If d.account equals account.
    - Set account\_exists from true.
- If not account\_exists.
  - Set accounts from mapping(“company” → company, “account” → account).
  - Evaluate doc.append(“accounts”, accounts).
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L4060) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L51)

<a id="op-2f89d05a27a489"></a>
### Render address

`operation_enterprise_accounts_party_business_behavior_render_address`

**Inputs** address, check\_permissions = true.

**Explicit results** Platform.call(\_render\_address, address, check\_permissions = check\_permissions).

**Local steps**

- Return Platform.call(\_render\_address, address, check\_permissions = check\_permissions).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L4343) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L73)
