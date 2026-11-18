# Integrations and service calls · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Plaid settings

[Record definition](../../../../data/record-types/plaid_settings.json)

<a id="op-34e296c92164ce"></a>
### Add bank accounts

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_add_bank_accounts`

**Inputs** response, bank, company.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Account” via get\_all · read “Bank Account Type” via get\_value · read “Bank Account Subtype” via get\_value · resolve a document from mapping(“doctype” → “Account”, “account\_name” → ((account at “name” + “ - ”) + response at “institution” at “name”), “parent\_account” → parent\_gl\_account at 0.name, “account\_type” → “Bank”, …) via get\_doc · resolve a document from mapping(“doctype” → “Bank Account”, “bank” → bank at “bank\_name”, “account” → gl\_account.name, “account\_name” → account at “name”, …) via get\_doc · 1 additional forms in the steps below.

**State and service calls** call insert on gl\_account · call insert on new\_account · msgprint with translated “Bank account {0} already exists and could not be created again”.format(account at “name”) · call save on existing\_account.

**Explicit results** result.

**Explicit failure paths** validation helper — translated “Please setup and enable a group account with the Account Type - {0} for the company {1}”.format(Platform.bold(translated “Bank”), company) · validation helper — translated “There was an error creating Bank Account while linking with Plaid.” · validation helper — translated “There was an error updating Bank Account {} while linking with Plaid.”.format(existing\_bank\_account).

**Local steps**

- Evaluate Platform.has\_permission(“Plaid Settings”, throw = true).
- Set response from Platform.parse\_json(response).
- Set bank from Platform.parse\_json(bank).
- Set result from list().
- Set parent\_gl\_account from Platform.db.get\_all(“Account”, mapping(“company” → company, “account\_type” → “Bank”, “is\_group” → 1, “disabled” → 0)).
- If not parent\_gl\_account.
  - Call the validation error handler Platform.throw(translated “Please setup and enable a group account with the Account Type - {0} for the company {1}”.format(Platform.bold(translated “Bank”), company)).
- For each account in response at “accounts”.
  - Set acc\_type from Platform.db.get\_value(“Bank Account Type”, account at “type”).
  - If not acc\_type.
    - Evaluate add\_account\_type(account at “type”).
  - Set acc\_subtype from Platform.db.get\_value(“Bank Account Subtype”, account at “subtype”).
  - If not acc\_subtype.
    - Evaluate add\_account\_subtype(account at “subtype”).
  - Set bank\_account\_name from “{} - {}”.format(account at “name”, bank at “bank\_name”).
  - Set existing\_bank\_account from get\_existing\_bank\_account(account at “id”, bank\_account\_name, company).
  - If not existing\_bank\_account.
    - Attempt the following.
      - Set gl\_account from Platform.get\_doc(mapping(“doctype” → “Account”, “account\_name” → ((account at “name” + “ - ”) + response at “institution” at “name”), “parent\_account” → parent\_gl\_account at 0.name, “account\_type” → “Bank”, …)).
      - Evaluate gl\_account.insert(ignore\_if\_duplicate = true).
      - Set new\_account from Platform.get\_doc(mapping(“doctype” → “Bank Account”, “bank” → bank at “bank\_name”, “account” → gl\_account.name, “account\_name” → account at “name”, …)).
      - Evaluate new\_account.insert(set\_name = append\_number\_if\_name\_exists(“Bank Account”, bank\_account\_name)).
      - Evaluate result.append(new\_account.name).
    - On failure (Platform.UniqueValidationError).
      - Evaluate Platform.msgprint(translated “Bank account {0} already exists and could not be created again”.format(account at “name”)).
    - On failure (Exception).
      - Evaluate Platform.log\_error(“Plaid Link Error”).
      - Call the validation error handler Platform.throw(translated “There was an error creating Bank Account while linking with Plaid.”, title = translated “Plaid Link Failed”).
  - Otherwise.
    - Attempt the following.
      - Set existing\_account from Platform.get\_doc(“Bank Account”, existing\_bank\_account).
      - Evaluate existing\_account.update(mapping(“bank” → bank at “bank\_name”, “account\_name” → account at “name”, “account\_type” → account.get(“type”, empty text), “account\_subtype” → account.get(“subtype”, empty text), …)).
      - Evaluate existing\_account.save().
      - Evaluate result.append(existing\_bank\_account).
    - On failure (Exception).
      - Evaluate Platform.log\_error(“Plaid Link Error”).
      - Call the validation error handler Platform.throw(translated “There was an error updating Bank Account {} while linking with Plaid.”.format(existing\_bank\_account), title = translated “Plaid Link Failed”).
- Return result.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Plaid Settings”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L49)

<a id="op-75bd810912d0f3"></a>
### Get existing bank account

`operation_enterprise_binding_enterprise_enterprise_integrations_doctype_plaid_settings_plaid_settings_get_existing_bank_account`

**Inputs** integration\_id, bank\_account\_name, company.

**Declared result** (str bitwise or no value).

**Record and data access** read “Bank Account” via get\_value.

**Explicit results** (Platform.db.get\_value(“Bank Account”, mapping(“integration\_id” → integration\_id, “company” → company)) or Platform.db.get\_value(“Bank Account”, mapping(“name” → bank\_account\_name, “is\_company\_account” → 1 ….

**Local steps**

- Return (Platform.db.get\_value(“Bank Account”, mapping(“integration\_id” → integration\_id, “company” → company)) or Platform.db.get\_value(“Bank Account”, mapping(“name” → bank\_account\_name, “is\_company\_account” → 1 ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Bank Account”, mapping(“integration\_id” → integration\_id, “company” → company)) → Platform.db.get\_value(“Bank Account”, mapping(“name” → bank\_account\_name, “is\_company\_account” → 1, “company” → company)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L587)

<a id="op-4f0a3f204054db"></a>
### Add account type

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_add_account_type`

**Inputs** account\_type.

**Record and data access** resolve a document from mapping(“doctype” → “Bank Account Type”, “account\_type” → account\_type) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Bank Account Type”, “account\_type” → account\_type)).

**Explicit failure paths** validation helper — Platform.get\_traceback().

**Local steps**

- Attempt the following.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Bank Account Type”, “account\_type” → account\_type)).insert().
- On failure (Exception).
  - Call the validation error handler Platform.throw(Platform.get\_traceback()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L48)

<a id="op-e7c27e8fb72755"></a>
### Add account subtype

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_add_account_subtype`

**Inputs** account\_subtype.

**Record and data access** resolve a document from mapping(“doctype” → “Bank Account Subtype”, “account\_subtype” → account\_subtype) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Bank Account Subtype”, “account\_subtype” → account\_subtype)).

**Explicit failure paths** validation helper — Platform.get\_traceback().

**Local steps**

- Attempt the following.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Bank Account Subtype”, “account\_subtype” → account\_subtype)).insert().
- On failure (Exception).
  - Call the validation error handler Platform.throw(Platform.get\_traceback()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L47)

<a id="op-2b50356ff83447"></a>
### Sync transactions

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_sync_transactions`

**Inputs** bank, bank\_account.

**Record and data access** read “Bank Account” via get\_value · read “Bank Transaction” via get\_value.

**State and service calls** savepoint “plaid\_sync\_txn” · rollback · request set\_value on “Bank Account”.

**Local steps**

- Set last\_transaction\_date from Platform.db.get\_value(“Bank Account”, bank\_account, “last\_integration\_date”).
- If last\_transaction\_date.
  - Set start\_date from formatdate(last\_transaction\_date, “YYYY-MM-dd”).
- Otherwise.
  - Set start\_date from formatdate(add\_months(today(), negative 12), “YYYY-MM-dd”).
- Set end\_date from formatdate(today(), “YYYY-MM-dd”).
- Attempt the following.
  - Set transactions from get\_transactions(bank = bank, bank\_account = bank\_account, start\_date = start\_date, end\_date = end\_date).
  - Set result from list().
  - If transactions.
    - For each transaction in reversed(transactions).
      - Evaluate Platform.db.savepoint(“plaid\_sync\_txn”).
      - Attempt the following.
        - Update result using + new\_bank\_transaction(transaction).
      - On failure (Exception).
        - Evaluate Platform.db.rollback(save\_point = “plaid\_sync\_txn”).
        - Evaluate Platform.log\_error(translated “Plaid transaction {0} could not be imported”.format(transaction.get(“transaction\_id”)), reference\_doctype = “Bank Account”, reference\_name = bank\_account).
  - If result.
    - Set last\_transaction\_date from Platform.db.get\_value(“Bank Transaction”, result.pop(), “date”).
    - Evaluate Platform.logger().info(formatted text Plaid added {len(result)} new Bank Transactions from '{bank\_account}' between {start\_date} and {end\_date}).
    - Evaluate Platform.db.set\_value(“Bank Account”, bank\_account, “last\_integration\_date”, last\_transaction\_date).
- On failure (Exception).
  - Evaluate Platform.log\_error(Platform.get\_traceback(), translated “Plaid transactions sync error”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L59)

<a id="op-a296c02dbbf309"></a>
### Get transactions

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_get_transactions`

**Inputs** bank, bank\_account = no value, start\_date = no value, end\_date = no value.

**Record and data access** read “Bank Account” via get\_values · read “Bank” via get\_value.

**Explicit results** transactions.

**Local steps**

- Set access\_token from no value.
- If bank\_account.
  - Set related\_bank from Platform.db.get\_values(“Bank Account”, bank\_account, list(“bank”, “integration\_id”), as\_dict = true).
  - Set access\_token from Platform.db.get\_value(“Bank”, related\_bank at 0.bank, “plaid\_access\_token”).
  - Set account\_id from related\_bank at 0.integration\_id.
- Otherwise.
  - Set access\_token from Platform.db.get\_value(“Bank”, bank, “plaid\_access\_token”).
  - Set account\_id from no value.
- Set plaid from PlaidConnector(access\_token).
- Set transactions from list().
- Attempt the following.
  - Set transactions from plaid.get\_transactions(start\_date = start\_date, end\_date = end\_date, account\_id = account\_id).
- On failure (ItemError) bound to e.
  - If e.code equals “ITEM\_LOGIN\_REQUIRED”.
    - Set msg from (translated “There was an error syncing transactions.” + one space).
    - Update msg using + (translated “Please refresh or reset the Plaid linking of the Bank {}.”.format(bank) + one space).
    - Evaluate Platform.log\_error(message = msg, title = translated “Plaid Link Refresh Required”).
- Return transactions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L1081) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L56)

<a id="op-5a6e238dec642f"></a>
### New bank transaction

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_new_bank_transaction`

**Inputs** transaction.

**Record and data access** read “Bank Account” via get\_value · read “Bank Transaction” via exists · resolve a document from mapping(“doctype” → “Bank Transaction”, “date” → getdate(transaction at “date”), “bank\_account” → bank\_account, “deposit” → deposit, …) via get\_doc.

**State and service calls** call insert on new\_transaction · call submit on new\_transaction.

**Explicit results** result.

**Explicit failure paths** validation helper — translated “Bank transaction creation error”.

**Local steps**

- Set result from list().
- Set bank\_account from Platform.db.get\_value(“Bank Account”, dict(integration\_id = transaction at “account\_id”)).
- Set amount from float(transaction at “amount”).
- If amount ≥ 0.0.
  - Set deposit from 0.0.
  - Set withdrawal from amount.
- Otherwise.
  - Set deposit from abs(amount).
  - Set withdrawal from 0.0.
- Set tags from list().
- If transaction at “category”.
  - Attempt the following.
    - Update tags using + transaction at “category”.
    - Update tags using + list(formatted text Plaid Cat. {transaction at “category\_id”}).
  - On failure (KeyError).
    - Take no action here.
- If (not Platform.db.exists(“Bank Transaction”, dict(transaction\_id = transaction at “transaction\_id”)) and not sbool(transaction at “pending”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.exists(“Bank Transaction”, dict(transaction\_id = transaction at “transaction\_id”)) → not sbool(transaction at “pending”).
  - Attempt the following.
    - Set new\_transaction from Platform.get\_doc(mapping(“doctype” → “Bank Transaction”, “date” → getdate(transaction at “date”), “bank\_account” → bank\_account, “deposit” → deposit, …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction at “transaction\_code” → transaction at “payment\_meta” at “payment\_method”.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction at “check\_number” → transaction at “payment\_meta” at “reference\_number” → transaction at “name”.
    - Evaluate new\_transaction.insert().
    - Evaluate new\_transaction.submit().
    - For each tag in tags.
      - Evaluate add\_tag(tag, “Bank Transaction”, new\_transaction.name).
    - Evaluate result.append(new\_transaction.name).
  - On failure (Exception).
    - Call the validation error handler Platform.throw(translated “Bank transaction creation error”).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L1666) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L57)

<a id="op-168b498b42b2ba"></a>
### Automatic synchronization

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_automatic_synchronization`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Plaid Settings” via get\_doc.

**Local steps**

- Set settings from Platform.get\_doc(“Plaid Settings”, “Plaid Settings”).
- If (settings.enabled equals 1 and settings.automatic\_sync equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.enabled equals 1 → settings.automatic\_sync equals 1.
  - Evaluate enqueue\_synchronization().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L2655) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L51)

<a id="op-1cd46896962a41"></a>
### Enqueue synchronization

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_enqueue_synchronization`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Account” via get\_all.

**State and service calls** enqueue with “Enterprise.Enterprise\_integrations.doctype.plaid\_settings.plaid\_settings.sync\_transactions”.

**Local steps**

- Evaluate Platform.has\_permission(“Plaid Settings”, throw = true).
- Set plaid\_accounts from Platform.get\_all(“Bank Account”, filters = mapping(“integration\_id” → list(“!=”, empty text), “disabled” → 0, “is\_company\_account” → 1), fields = list(“name”, “bank”)).
- For each plaid\_account in plaid\_accounts.
  - Evaluate Platform.enqueue(“Enterprise.Enterprise\_integrations.doctype.plaid\_settings.plaid\_settings.sync\_transactions”, bank = plaid\_account.bank, bank\_account = plaid\_account.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Plaid Settings”, throw = true) · service or queued work from Platform.enqueue(“Enterprise.Enterprise\_integrations.doctype.plaid\_settings.plaid\_settings.sync\_transactions”, bank = plaid\_account.bank, bank\_account = plaid\_account.name).

**Boundaries to resolve** stored data, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L52)

<a id="op-d5b6e8adf908bd"></a>
### Get link token for update

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_get_link_token_for_update`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** access\_token.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L54)

<a id="op-81236f62c8f101"></a>
### Get company

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_get_company`

**Inputs** bank\_account\_name.

**Record and data access** read “Company” via get\_all · read “Bank Account” via exists · read “Bank Account” via get\_value.

**Explicit results** company\_names at 0 · Platform.db.get\_value(“Bank Account”, bank\_account\_name, “company”) · company\_default.

**Explicit failure paths** validation helper — translated “Could not detect the Company for updating Bank Accounts”.

**Local steps**

- Bind dependencies get\_user\_default.
- Set company\_names from Platform.db.get\_all(“Company”, pluck = “name”).
- If len(company\_names) equals 1.
  - Return company\_names at 0.
- If Platform.db.exists(“Bank Account”, bank\_account\_name).
  - Return Platform.db.get\_value(“Bank Account”, bank\_account\_name, “company”).
- Set company\_default from get\_user\_default(“Company”).
- If company\_default.
  - Return company\_default.
- Call the validation error handler Platform.throw(translated “Could not detect the Company for updating Bank Accounts”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L3168) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L53)

<a id="op-d66118ff05697d"></a>
### Update bank account ids

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_update_bank_account_identifiers`

**Inputs** response.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank” via get\_doc.

**Explicit results** add\_bank\_accounts(response, bank, get\_company(bank\_account\_name)).

**Local steps**

- Evaluate Platform.has\_permission(“Plaid Settings”, throw = true).
- Set data from Platform.parse\_json(response).
- Set institution\_name from data at “institution” at “name”.
- Set bank from Platform.get\_doc(“Bank”, institution\_name).as\_dict().
- Set bank\_account\_name from formatted text {data at “account” at “name”} - {institution\_name}.
- Return add\_bank\_accounts(response, bank, get\_company(bank\_account\_name)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Plaid Settings”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L60)

## Service · Utils

<a id="op-04d38916936e72"></a>
### Get webhook address

`operation_enterprise_enterprise_application_integrations_utils_business_behavior_get_webhook_address`

**Inputs** connector\_name, method, exclude\_uri = false, force\_https = false.

**Explicit results** endpoint · server\_url.

**Local steps**

- Set endpoint from formatted text Enterprise.Enterprise\_integrations.connectors.{connector\_name}.{method}.
- If exclude\_uri.
  - Return endpoint.
- Attempt the following.
  - Set url from Platform.request.url.
- On failure (RuntimeError).
  - Set url from text in the contract.
- Set url\_data from urlparse(url).
- Set scheme from “https” when force\_https, otherwise url\_data.scheme.
  - Value choice on force\_https — true gives “https”, false gives url\_data.scheme.
- Set netloc from url\_data.netloc.
- Set server\_url from formatted text {scheme}://{netloc}/api/method/{endpoint}.
- Return server\_url.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L5966) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L70)

## Record · Voice call settings

[Record definition](../../../../data/record-types/voice_call_settings.json)

<a id="op-ec65c966b3f86e"></a>
### Voice Call Settings.before insert

`operation_enterprise_binding_enterprise_telephony_doctype_voice_call_settings_voice_call_settings_voicecallsettings_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.set\_user\_for\_restricted\_creator().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set user for restricted creator](operations-004.md#op-67dd9d6cb782cb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L22) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1303)

<a id="op-67dd9d6cb782cb"></a>
### Voice Call Settings.set user for restricted creator

`operation_enterprise_binding_enterprise_telephony_doctype_voice_call_settings_voice_call_settings_voicecallsettings_set_user_for_restricted_creator`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.flags.ignore\_permissions or self.has\_permlevel\_access\_to(“user”, permission\_type = “write”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.ignore\_permissions → self.has\_permlevel\_access\_to(“user”, permission\_type = “write”).
  - Return no value.
- Set self.user from Platform.session.user.
- Set self.flags.ignore\_permlevel\_for\_fields from list(“user”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L23) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1304)

<a id="op-9a26f8326e5624"></a>
### Has permission

`operation_enterprise_binding_enterprise_telephony_doctype_voice_call_settings_voice_call_settings_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L20) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1301)

<a id="op-f229f84f5d8de1"></a>
### Get permission query conditions

`operation_enterprise_binding_enterprise_telephony_doctype_voice_call_settings_voice_call_settings_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L19) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1300)

<a id="op-06ee4b2d8652c2"></a>
### Is admin

`operation_enterprise_binding_enterprise_telephony_doctype_voice_call_settings_voice_call_settings_is_admin`

**Inputs** user.

**Declared result** bool.

**Explicit results** ADMIN\_ROLE belongs to Platform.get\_roles(user).

**Local steps**

- Return ADMIN\_ROLE belongs to Platform.get\_roles(user).

**Values supplied outside this operation** effective access from Platform.get\_roles(user).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L21) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1302)
