# Accounting and settlement · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Account

[Record definition](../../../../data/record-types/account.json)

<a id="op-e259bcb0e1464e"></a>
### Account.check gle exists

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_check_general_ledger_entry_exists`

**Inputs** self.

**Record and data access** read “GL Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“GL Entry”, mapping(“account” → self.name)).

**Local steps**

- Return Platform.db.get\_value(“GL Entry”, mapping(“account” → self.name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L1555) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L89)

<a id="op-aecf1904571cc6"></a>
### Account.check if child exists

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_check_if_child_exists`

**Inputs** self.

**Record and data access** execute query text (SELECT, Account).

**Explicit results** Platform.db.sql(query text (SELECT, Account), self.name).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Account), self.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L90)

<a id="op-8c65e3d233f986"></a>
### Account.validate mandatory

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_mandatory`

**Inputs** self.

**Local steps**

- If not self.root\_type.
  - Evaluate throw(translated “Root Type is mandatory”).
- If not self.report\_type.
  - Evaluate throw(translated “Report Type is mandatory”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L1760) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L107)

<a id="op-9502e74723728d"></a>
### Account.on trash

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_on_trash`

**Inputs** self.

**Local steps**

- If self.check\_gle\_exists().
  - Evaluate throw(translated “Account with existing transaction can not be deleted”).
- Evaluate super().on\_trash(true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check gle exists](operations-002.md#op-e259bcb0e1464e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L1895) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L94)

<a id="op-e75cc7d0ca9d06"></a>
### Get parent account

`operation_enterprise_accounts_record_definitions_account_business_behavior_get_parent_account`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Account” via get\_list.

**Explicit results** Platform.get\_list(“Account”, filters = list(list(“is\_group”, “=”, 1), list(“docstatus”, “!=”, 2), list(“company”, “=”, filters at “company”), list(searchfield, “like”, formatted text %{txt}%)), fields = li ….

**Local steps**

- Return Platform.get\_list(“Account”, filters = list(list(“is\_group”, “=”, 1), list(“docstatus”, “!=”, 2), list(“company”, “=”, filters at “company”), list(searchfield, “like”, formatted text %{txt}%)), fields = li ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L119)

<a id="op-c059ce49c4dc80"></a>
### Has ledger entries in subtree

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_has_ledger_entries_in_subtree`

**Inputs** lft, rgt.

**Declared result** bool.

**Explicit results** bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Local steps**

- Set account from Platform.qb.DocType(“Account”).
- Set gl\_entry from Platform.qb.DocType(“GL Entry”).
- Return bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L750)

<a id="op-f2b3f99dee3291"></a>
### Get account currency

`operation_enterprise_accounts_record_definitions_account_business_behavior_get_account_currency`

**Inputs** account.

**Explicit results** no value · Platform.local\_cache(“account\_currency”, account, generator).

**Local steps**

- If not account.
  - Return no value.
- Bind local operation generator for subsequent calls.
- Return Platform.local\_cache(“account\_currency”, account, generator).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L2499) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L116)

<a id="op-552be051e18999"></a>
### Get account currency.generator

`operation_enterprise_accounts_record_definitions_account_business_behavior_get_account_currency_generator`

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

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L2735) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L117)

<a id="op-59dbb5a9720d1d"></a>
### On doctype update

`operation_enterprise_accounts_record_definitions_account_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Account”.

**Local steps**

- Evaluate Platform.db.add\_index(“Account”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L2895) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L122)

<a id="op-aa231114f6cd99"></a>
### Get account autoname

`operation_enterprise_accounts_record_definitions_account_business_behavior_get_account_autoname`

**Inputs** account\_number, account\_name, company.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** call insert on parts.

**Explicit results** “ - ”.join(parts).

**Explicit failure paths** validation helper — translated “Company {0} does not exist”.format(company).

**Local steps**

- Set company from Platform.get\_cached\_value(“Company”, company, list(“abbr”, “name”), as\_dict = true).
- If not company.
  - Call the validation error handler Platform.throw(translated “Company {0} does not exist”.format(company)).
- Set parts from list(account\_name.strip(), company.abbr).
- If cstr(account\_number).strip().
  - Evaluate parts.insert(0, cstr(account\_number).strip()).
- Return “ - ”.join(parts).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“abbr”, “name”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L2973) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L115)

<a id="op-1e2819c8fbe80e"></a>
### Update account number

`operation_enterprise_accounts_record_definitions_account_business_behavior_update_account_number`

**Inputs** name, account\_name, account\_number = no value, from\_descendant = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Account” via get\_cached\_doc.

**Explicit results** new\_name.

**Local steps**

- If from\_descendant.
  - Evaluate record a compatibility advisory for the invoked interface.
- Evaluate \_ensure\_idle\_system().
- Set account from Platform.get\_cached\_doc(“Account”, name).
- Evaluate account.check\_permission(“write”).
- Evaluate validate\_rename\_in\_child\_company(account).
- Set tuple(old\_account\_name, old\_account\_number) from tuple(account.account\_name, account.account\_number).
- Set new\_name from set\_account\_name\_and\_number(account, account\_name, account\_number).
- Set descendants from get\_descendants\_of(“Company”, account.company).
- If descendants.
  - Evaluate sync\_update\_account\_number\_in\_child(descendants, old\_account\_name, account\_name, account\_number, …).
- Return new\_name.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Account”, name) · effective access from account.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L124)

<a id="op-11c30e68336a54"></a>
### Validate rename in child company

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_validate_rename_in_child_company`

**Inputs** account.

**Record and data access** read “Company” via get\_cached\_value · read “Account” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If Platform.get\_cached\_value(“Company”, account.company, “allow\_account\_creation\_against\_child\_company”).
  - Return no value.
- For each ancestor in get\_ancestors\_of(“Company”, account.company).
  - If Platform.db.exists(“Account”, mapping(“account\_number” → account.account\_number, “account\_name” → account.account\_name, “company” → ancestor)).
    - Set allow\_child\_account\_creation from translated “Allow Account Creation Against Child Company”.
    - Set message from translated “Account {0} exists in parent company {1}.”.format(Platform.bold(account.account\_name), Platform.bold(ancestor)).
    - Update message using + text in the contract.
    - Update message using + translated “Renaming it is only allowed via parent company {0}, to avoid mismatch.”.format(Platform.bold(ancestor)).
    - Update message using + text in the contract.
    - Update message using + translated “To overrule this, enable '{0}' in company {1}”.format(allow\_child\_account\_creation, Platform.bold(account.company)).
    - Call the validation error handler Platform.throw(message, title = translated “Rename Not Allowed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, account.company, “allow\_account\_creation\_against\_child\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L755)

<a id="op-45ffe9d046b261"></a>
### Update child company account number

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_update_child_company_account_number`

**Inputs** name, account\_name, account\_number = no value.

**Record and data access** resolve a document from “Account” via get\_cached\_doc.

**Explicit results** set\_account\_name\_and\_number(account, account\_name, account\_number).

**Local steps**

- Set account from Platform.get\_cached\_doc(“Account”, name).
- Evaluate account.check\_permission(“write”).
- Return set\_account\_name\_and\_number(account, account\_name, account\_number).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Account”, name) · effective access from account.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L752)

<a id="op-66e0e4a759c965"></a>
### Set account name and number

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_set_account_name_and_number`

**Inputs** account, account\_name, account\_number = no value.

**State and service calls** request set\_value on “Account” · request rename\_doc for “Account”.

**Explicit results** new\_name.

**Local steps**

- Set tuple(account\_name, account\_number) from tuple(cstr(account\_name).strip(), cstr(account\_number).strip()).
- If not account\_name.
  - Evaluate throw(translated “Account Name cannot be empty”).
- Evaluate account.validate\_account\_number(account\_number).
- Evaluate Platform.db.set\_value(“Account”, account.name, mapping(“account\_number” → account\_number, “account\_name” → account\_name)).
- Set new\_name from get\_account\_autoname(account\_number, account\_name, account.company).
- If account.name differs from new\_name.
  - Evaluate Platform.rename\_doc(“Account”, account.name, new\_name, force = 1).
  - Return new\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L751)

<a id="op-83f5676d95c71f"></a>
### Merge account

`operation_enterprise_accounts_record_definitions_account_business_behavior_merge_account`

**Inputs** old, new.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Account” via get\_cached\_doc · read “Account” via get\_cached\_value.

**State and service calls** call db\_set on new\_account · request rename\_doc for “Account”.

**Explicit results** new.

**Local steps**

- Evaluate \_ensure\_idle\_system().
- Set new\_account from Platform.get\_cached\_doc(“Account”, new).
- Set old\_account from Platform.get\_cached\_doc(“Account”, old).
- Evaluate new\_account.check\_permission(“write”).
- Evaluate old\_account.check\_permission(“write”).
- If not new\_account.
  - Evaluate throw(translated “Account {0} does not exist”.format(new)).
- Evaluate validate\_accounts\_can\_be\_merged(old\_account, new\_account).
- Evaluate validate\_balance\_after\_merge(old\_account, new\_account).
- If (old\_account.is\_group and old belongs to get\_ancestors\_of(“Account”, new)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_account.is\_group → old belongs to get\_ancestors\_of(“Account”, new).
  - Evaluate new\_account.db\_set(“parent\_account”, Platform.get\_cached\_value(“Account”, old, “parent\_account”)).
- Evaluate Platform.rename\_doc(“Account”, old, new, merge = 1, force = 1).
- Return new.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Account”, new), Platform.get\_cached\_doc(“Account”, old) and 1 further calls · effective access from new\_account.check\_permission(“write”), old\_account.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L121)

<a id="op-5c517f970d77fc"></a>
### Validate accounts can be merged

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_validate_accounts_can_be_merged`

**Inputs** old\_account, new\_account.

**Local steps**

- If get\_merge\_properties(new\_account) differs from get\_merge\_properties(old\_account).
  - Evaluate throw(msg = translated “Merging is only possible if following properties are same in both records. Is Group, Root Type, Company, Acc …”, title = “Invalid Accounts”, exc = InvalidAccountMergeError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L753)

<a id="op-2fb33232f8bfd9"></a>
### Validate balance after merge

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_validate_balance_after_merge`

**Inputs** old\_account, new\_account.

**Explicit results** no value.

**Local steps**

- If not new\_account.balance\_must\_be.
  - Return no value.
- Set balance from get\_balance\_after\_merge(old\_account.name, new\_account.name).
- If ((balance &gt; 0 and new\_account.balance\_must\_be equals “Credit”) or (balance &lt; 0 and new\_account.balance\_must\_be equals “Debit”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (balance &gt; 0 and new\_account.balance\_must\_be equals “Credit”) → (balance &lt; 0 and new\_account.balance\_must\_be equals “Debit”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in balance &gt; 0 → new\_account.balance\_must\_be equals “Credit”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in balance &lt; 0 → new\_account.balance\_must\_be equals “Debit”.
  - Evaluate throw(translated “Cannot merge into {0}. Its balance after the merge would be in {1}, but its Balance must be is {2}.”.format(Platform.bold(new\_account.name), translated “Debit” when balance &gt; 0, otherwise ….
    - Value choice on balance &gt; 0 — true gives translated “Debit”, false gives translated “Credit”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L754)

<a id="op-61519954e20ec7"></a>
### Get balance after merge

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_get_balance_after_merge`

**Inputs** old, new.

**Declared result** float.

**Record and data access** read “Account” via get\_value.

**Explicit results** get\_balance\_on(old) · get\_balance\_on(new) · (get\_balance\_on(old) + get\_balance\_on(new)).

**Local steps**

- Bind dependencies get\_balance\_on.
- Set tuple(old\_lft, old\_rgt) from Platform.db.get\_value(“Account”, old, list(“lft”, “rgt”)).
- Set tuple(new\_lft, new\_rgt) from Platform.db.get\_value(“Account”, new, list(“lft”, “rgt”)).
- If (old\_lft ≤ new\_lft and new\_rgt ≤ old\_rgt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_lft ≤ new\_lft → new\_rgt ≤ old\_rgt.
  - Return get\_balance\_on(old).
- If (new\_lft ≤ old\_lft and old\_rgt ≤ new\_rgt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_lft ≤ old\_lft → old\_rgt ≤ new\_rgt.
  - Return get\_balance\_on(new).
- Return (get\_balance\_on(old) + get\_balance\_on(new)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L748)

<a id="op-630053e826c8e7"></a>
### Get merge properties

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_get_merge_properties`

**Inputs** account.

**Declared result** tuple.

**Explicit results** tuple(cint(account.is\_group), account.root\_type, account.company, cstr(account.account\_currency), …).

**Local steps**

- Return tuple(cint(account.is\_group), account.root\_type, account.company, cstr(account.account\_currency), …).
  - Value choice on cint(account.is\_group) — true gives empty text, false gives cstr(account.account\_type).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L749)

<a id="op-083e2138947e36"></a>
### Get root company

`operation_enterprise_accounts_record_definitions_account_business_behavior_get_root_company`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list(ancestors at 0) when ancestors, otherwise list().

**Local steps**

- Set ancestors from get\_ancestors\_of(“Company”, company, “lft asc”).
- Return list(ancestors at 0) when ancestors, otherwise list().
  - Value choice on ancestors — true gives list(ancestors at 0), false gives list().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L120)

<a id="op-3c5160ff5157da"></a>
### Sync update account number in child

`operation_enterprise_accounts_record_definitions_account_business_behavior_sync_update_account_number_in_child`

**Inputs** descendants, old\_acc\_name, account\_name, account\_number = no value, old\_acc\_number = no value.

**Record and data access** read “Account” via get\_values.

**Local steps**

- Set filters from mapping(“company” → list(“in”, descendants), “account\_name” → old\_acc\_name).
- If old\_acc\_number.
  - Set filters at “account\_number” from old\_acc\_number.
- For each d in Platform.db.get\_values(“Account”, filters = filters, fieldname = list(“company”, “name”), as\_dict = true).
  - Evaluate update\_child\_company\_account\_number(d at “name”, account\_name, account\_number).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L123)

<a id="op-6d11140d048e1b"></a>
### Ensure idle system

`operation_enterprise_accounts_record_definitions_account_business_behavior_ensure_idle_system`

**Inputs** no declared parameters.

**Record and data access** read “GL Entry” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Last GL Entry update was done {}. This operation is not allowed while system is actively being used. Please  …”.format(pretty\_date(last\_gl\_update)).

**Local steps**

- If Platform.in\_test.
  - Return no value.
- Set last\_gl\_update from no value.
- Attempt the following.
  - Set last\_gl\_update from Platform.db.get\_value(“GL Entry”, mapping(), “modified”, for\_update = true, wait = false).
- On failure (Platform.QueryTimeoutError).
  - Set last\_gl\_update from add\_to\_date(no value, seconds = negative 1).
- If not last\_gl\_update.
  - Return no value.
- If last\_gl\_update &gt; add\_to\_date(no value, minutes = negative 5).
  - Call the validation error handler Platform.throw(translated “Last GL Entry update was done {}. This operation is not allowed while system is actively being used. Please  …”.format(pretty\_date(last\_gl\_update)), title = translated “System In Use”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L114)

<a id="op-95a08df6d33322"></a>
### Get company default account fields

`operation_enterprise_accounts_record_definitions_account_business_behavior_get_company_default_account_fields`

**Inputs** no declared parameters.

**Explicit results** mapping(“default\_bank\_account” → “Default Bank Account”, “default\_cash\_account” → “Default Cash Account”, “default\_receivable\_account” → “Default Receivable Account”, “default\_payable\_account” → “Default P ….

**Local steps**

- Return mapping(“default\_bank\_account” → “Default Bank Account”, “default\_cash\_account” → “Default Cash Account”, “default\_receivable\_account” → “Default Receivable Account”, “default\_payable\_account” → “Default P ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L118)

<a id="op-a679ed6d90b1d9"></a>
### Create charts

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_create_charts`

**Inputs** company, chart\_template = no value, existing\_company = no value, custom\_chart = no value, from\_coa\_importer = no value.

**Local steps**

- Set chart from (custom\_chart or get\_chart(chart\_template, existing\_company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in custom\_chart → get\_chart(chart\_template, existing\_company).
- If chart.
  - Set accounts from list().
  - Bind local operation \_import\_accounts for subsequent calls.
  - Set Platform.local.flags.ignore\_update\_nsm from true.
  - Evaluate \_import\_accounts(chart, no value, no value, root\_account = true).
  - Evaluate rebuild\_tree(“Account”).
  - Set Platform.local.flags.ignore\_update\_nsm from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0007.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L132)
