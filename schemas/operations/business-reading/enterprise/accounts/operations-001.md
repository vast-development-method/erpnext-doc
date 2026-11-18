# Accounting and settlement · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Account

[Record definition](../../../../data/record-types/account.json)

<a id="op-37be2220fcb8c3"></a>
### Account.on update

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.local.flags.ignore\_update\_nsm.
  - Return no value.
- Otherwise.
  - Evaluate super().on\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0004.json#L7185) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L95)

<a id="op-8be7889dc4d69f"></a>
### Account.onload

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_onload`

**Inputs** self.

**Local steps**

- If self.is\_allowed\_to\_set\_frozen\_value().
  - Evaluate self.set\_onload(“can\_freeze\_account”, true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is allowed to set frozen value](operations-001.md#op-e594b5ad41bae1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L96)

<a id="op-e594b5ad41bae1"></a>
### Account.is allowed to set frozen value

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_account_is_allowed_to_set_frozen_value`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** (bool(role\_allowed\_for\_frozen\_entries) and role\_allowed\_for\_frozen\_entries belongs to Platform.get\_roles()).

**Local steps**

- Set role\_allowed\_for\_frozen\_entries from Platform.get\_cached\_value(“Company”, self.company, “role\_allowed\_for\_frozen\_entries”).
- Return (bool(role\_allowed\_for\_frozen\_entries) and role\_allowed\_for\_frozen\_entries belongs to Platform.get\_roles()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(role\_allowed\_for\_frozen\_entries) → role\_allowed\_for\_frozen\_entries belongs to Platform.get\_roles().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “role\_allowed\_for\_frozen\_entries”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L746)

<a id="op-3e3e22fb093b15"></a>
### Account.autoname

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_autoname`

**Inputs** self.

**Local steps**

- Bind dependencies get\_autoname\_with\_number.
- Set self.name from get\_autoname\_with\_number(self.account\_number, self.account\_name, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L88)

<a id="op-65be6e7231c252"></a>
### Account.validate

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.local.flags.allow\_unverified\_charts.
  - Return no value.
- Evaluate self.validate\_parent().
- Evaluate self.validate\_parent\_child\_account\_type().
- Evaluate self.validate\_root\_details().
- Evaluate self.validate\_account\_number().
- Evaluate self.validate\_disabled().
- Evaluate self.validate\_group\_or\_ledger().
- Evaluate self.set\_root\_and\_report\_type().
- Evaluate self.validate\_mandatory().
- Evaluate self.validate\_frozen\_accounts\_modifier().
- Evaluate self.validate\_balance\_must\_be\_debit\_or\_credit().
- Evaluate self.validate\_account\_currency().
- Evaluate self.validate\_root\_company\_and\_sync\_account\_to\_children().
- Evaluate self.validate\_receivable\_payable\_account\_type().
- Evaluate self.validate\_stock\_account\_type\_change().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate parent](operations-001.md#op-11ce85c4dd5f79), [validate parent child account type](operations-001.md#op-c15a1f1353c93a), [validate root details](operations-001.md#op-4b6fd229f878cb), [validate account number](operations-001.md#op-c0e53a739423b8), [validate disabled](operations-001.md#op-b01b4ae0f30023), [validate group or ledger](operations-001.md#op-af627673697d67), [set root and report type](operations-001.md#op-4c698b6802d7e6), [validate mandatory](operations-002.md#op-8c65e3d233f986), [validate frozen accounts modifier](operations-001.md#op-72d3303e6d68cf), [validate balance must be debit or credit](operations-001.md#op-bc464cfc93d2c4), [validate account currency](operations-001.md#op-3dee216c8c5b65), [validate root company and sync account to children](operations-001.md#op-009d8c6b2d63fa), [validate receivable payable account type](operations-001.md#op-11f9ca72c6ae94), [validate stock account type change](operations-001.md#op-08709c08439368).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L99)

<a id="op-c15a1f1353c93a"></a>
### Account.validate parent child account type

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_parent_child_account_type`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Local steps**

- If self.parent\_account.
  - If self.account\_type belongs to list(“Direct Income”, “Indirect Income”, “Current Asset”, “Current Liability”, …).
    - Set parent\_account\_type from Platform.db.get\_value(“Account”, self.parent\_account, list(“account\_type”)).
    - If parent\_account\_type equals self.account\_type.
      - Evaluate throw(translated “Only Parent can be of type {0}”.format(self.account\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L437) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L109)

<a id="op-11ce85c4dd5f79"></a>
### Account.validate parent

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_parent`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Local steps**

- If self.parent\_account.
  - Set par from Platform.get\_cached\_value(“Account”, self.parent\_account, list(“name”, “is\_group”, “company”), as\_dict = 1).
  - If not par.
    - Evaluate throw(translated “Account {0}: Parent account {1} does not exist”.format(self.name, self.parent\_account)).
  - Otherwise.
    - If par.name equals self.name.
      - Evaluate throw(translated “Account {0}: You can not assign itself as parent account”.format(self.name)).
    - Otherwise.
      - If not par.is\_group.
        - Evaluate throw(translated “Account {0}: Parent account {1} can not be a ledger”.format(self.name, self.parent\_account)).
      - Otherwise.
        - If par.company differs from self.company.
          - Evaluate throw(translated “Account {0}: Parent account {1} does not belong to company: {2}”.format(self.name, self.parent\_account, self.company)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.parent\_account, list(“name”, “is\_group”, “company”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L675) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L108)

<a id="op-4c698b6802d7e6"></a>
### Account.set root and report type

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_set_root_and_report_type`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**State and service calls** execute query text (UPDATE, Account).

**Local steps**

- If self.parent\_account.
  - Set par from Platform.get\_cached\_value(“Account”, self.parent\_account, list(“report\_type”, “root\_type”), as\_dict = 1).
  - If par.report\_type.
    - Set self.report\_type from par.report\_type.
  - If par.root\_type.
    - Set self.root\_type from par.root\_type.
- Evaluate self.validate\_report\_type\_change().
- If cint(self.is\_group).
  - Set db\_value from self.get\_doc\_before\_save().
  - If db\_value.
    - If self.report\_type differs from db\_value.report\_type.
      - Evaluate Platform.db.sql(query text (UPDATE, Account), tuple(self.report\_type, self.lft, self.rgt)).
    - If self.root\_type differs from db\_value.root\_type.
      - Evaluate Platform.db.sql(query text (UPDATE, Account), tuple(self.root\_type, self.lft, self.rgt)).
- If (self.root\_type and not self.report\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.root\_type → not self.report\_type.
  - Set self.report\_type from “Balance Sheet” when self.root\_type belongs to tuple(“Asset”, “Liability”, “Equity”), otherwise “Profit and Loss”.
    - Value choice on self.root\_type belongs to tuple(“Asset”, “Liability”, “Equity”) — true gives “Balance Sheet”, false gives “Profit and Loss”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate report type change](operations-001.md#op-8206e74b1e4edf).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.parent\_account, list(“report\_type”, “root\_type”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L97)

<a id="op-8206e74b1e4edf"></a>
### Account.validate report type change

`operation_enterprise_binding_enterprise_accounts_doctype_account_account_account_validate_report_type_change`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (not doc\_before\_save or doc\_before\_save.report\_type equals self.report\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc\_before\_save → doc\_before\_save.report\_type equals self.report\_type.
  - Return no value.
- If has\_ledger\_entries\_in\_subtree(doc\_before\_save.lft, doc\_before\_save.rgt).
  - Evaluate throw(translated “Cannot change Report Type of {0} from {1} to {2} because the account or its child accounts have ledger entries.”.format(Platform.bold(self.name), translated doc\_before\_save.report\_type, transla …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L747)

<a id="op-11f9ca72c6ae94"></a>
### Account.validate receivable payable account type

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_receivable_payable_account_type`

**Inputs** self.

**Record and data access** read “GL Entry” via get\_all.

**State and service calls** msgprint with msg.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- Set receivable\_payable\_types from list(“Receivable”, “Payable”).
- If (doc\_before\_save and doc\_before\_save.account\_type belongs to receivable\_payable\_types and doc\_before\_save.account\_type differs from self.account\_type).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.account\_type belongs to receivable\_payable\_types → doc\_before\_save.account\_type differs from self.account\_type.
  - If Platform.db.get\_all(“GL Entry”, filters = mapping(“account” → self.name, “is\_cancelled” → 0), limit = 1).
    - Set msg from translated “There are ledger entries against this account. Changing {0} to non-{1} in live system will cause incorrect o …”.format(Platform.bold(translated “Account Type”), doc\_before\_save.account\_type, do ….
    - Evaluate Platform.msgprint(msg).
    - Evaluate self.add\_comment(“Comment”, msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L1853) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L110)

<a id="op-08709c08439368"></a>
### Account.validate stock account type change

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_stock_account_type_change`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The account type of {0} cannot be changed from {1} because stock ledger entries exist against it.”.format(Platform.bold(self.name), Platform.bold(translated “Stock”)).

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not (doc\_before\_save and doc\_before\_save.account\_type equals “Stock”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.account\_type equals “Stock”.
  - Return no value.
- <a id="op-08709c08439368-guard-6"></a>If self.account\_type equals “Stock”.
  - Return no value.
- If self.stock\_ledger\_entry\_exists().
  - Call the validation error handler Platform.throw(translated “The account type of {0} cannot be changed from {1} because stock ledger entries exist against it.”.format(Platform.bold(self.name), Platform.bold(translated “Stock”))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.account\_type equals “Stock”, self.account\_type = “Stock” selects the branch that returns no value. With self.account\_type = “Accumulated Depreciation”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-08709c08439368-guard-6)

**Methods declared on this owner** [stock ledger entry exists](operations-001.md#op-7d0016b7bf47e7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L2231) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L113)

<a id="op-7d0016b7bf47e7"></a>
### Account.stock ledger entry exists

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_stock_ledger_entry_exists`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via count.

**Explicit results** false · bool(Platform.db.count(“Stock Ledger Entry”, filters = mapping(“warehouse” → tuple(“in”, warehouses), “is\_cancelled” → 0))).

**Local steps**

- Bind dependencies get\_warehouse\_account\_map.
- Set warehouse\_account from get\_warehouse\_account\_map(self.company).
- Set warehouses from list of wh for tuple(wh, details) drawn from warehouse\_account.items() where details.account equals self.name.
  - Draw tuple(wh, details) from warehouse\_account.items(), keep a combination only if (details.account equals self.name).
- If not warehouses.
  - Return false.
- Return bool(Platform.db.count(“Stock Ledger Entry”, filters = mapping(“warehouse” → tuple(“in”, warehouses), “is\_cancelled” → 0))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L2501) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L98)

<a id="op-4b6fd229f878cb"></a>
### Account.validate root details

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_root_details`

**Inputs** self.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (doc\_before\_save and not doc\_before\_save.parent\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → not doc\_before\_save.parent\_account.
  - Evaluate throw(translated “Root cannot be edited.”, RootNotEditable).
- If (not self.parent\_account and not cint(self.is\_group)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.parent\_account → not cint(self.is\_group).
  - Evaluate throw(translated “The root account {0} must be a group”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L2766) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L112)

<a id="op-009d8c6b2d63fa"></a>
### Account.validate root company and sync account to children

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_root_company_and_sync_account_to_children`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value · read “Account” via get\_value · read “Account” via get\_cached\_value · read “Account” via get\_values.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please add the account to root level Company - {}”.format(ancestors at 0).

**Local steps**

- If (Platform.local.flags.ignore\_root\_company\_validation or self.flags.ignore\_root\_company\_validation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.flags.ignore\_root\_company\_validation → self.flags.ignore\_root\_company\_validation.
  - Return no value.
- Set ancestors from get\_root\_company(self.company).
- If ancestors.
  - If Platform.get\_cached\_value(“Company”, self.company, “allow\_account\_creation\_against\_child\_company”).
    - Return no value.
  - If not Platform.db.get\_value(“Account”, mapping(“account\_name” → self.account\_name, “company” → ancestors at 0), “name”).
    - Call the validation error handler Platform.throw(translated “Please add the account to root level Company - {}”.format(ancestors at 0)).
- Otherwise.
  - If self.parent\_account.
    - Set descendants from get\_descendants\_of(“Company”, self.company).
    - If not descendants.
      - Return no value.
    - Set parent\_acc\_name\_map from mapping().
    - Set tuple(parent\_acc\_name, parent\_acc\_number) from Platform.get\_cached\_value(“Account”, self.parent\_account, list(“account\_name”, “account\_number”)).
    - Set filters from mapping(“company” → list(“in”, descendants), “account\_name” → parent\_acc\_name).
    - If parent\_acc\_number.
      - Set filters at “account\_number” from parent\_acc\_number.
    - For each d in Platform.db.get\_values(“Account”, filters = filters, fieldname = list(“company”, “name”), as\_dict = true).
      - Set parent\_acc\_name\_map at d at “company” from d at “name”.
    - If not parent\_acc\_name\_map.
      - Return no value.
    - Evaluate self.create\_account\_for\_child\_company(parent\_acc\_name\_map, descendants, parent\_acc\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create account for child company](operations-001.md#op-f490baa8a899ee).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “allow\_account\_creation\_against\_child\_company”), Platform.get\_cached\_value(“Account”, self.parent\_account, list(“account\_name”, “account\_number”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L111)

<a id="op-b01b4ae0f30023"></a>
### Account.validate disabled

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_disabled`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (not doc\_before\_save or cint(doc\_before\_save.disabled) equals cint(self.disabled)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc\_before\_save → cint(doc\_before\_save.disabled) equals cint(self.disabled).
  - Return no value.
- If cint(self.disabled).
  - Evaluate self.validate\_default\_accounts\_in\_company().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate default accounts in company](operations-001.md#op-4a6370bce13728).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L3778) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L104)

<a id="op-af627673697d67"></a>
### Account.validate group or ledger

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_group_or_ledger`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (not doc\_before\_save or cint(doc\_before\_save.is\_group) equals cint(self.is\_group)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc\_before\_save → cint(doc\_before\_save.is\_group) equals cint(self.is\_group).
  - Return no value.
- If self.check\_gle\_exists().
  - Evaluate throw(translated “Account with existing transaction cannot be converted to ledger”).
- Otherwise.
  - If cint(self.is\_group).
    - If (self.account\_type and not self.flags.exclude\_account\_type\_check).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.account\_type → not self.flags.exclude\_account\_type\_check.
      - Evaluate throw(translated “Cannot covert to Group because Account Type is selected.”).
    - Evaluate self.validate\_default\_accounts\_in\_company().
  - Otherwise.
    - If self.check\_if\_child\_exists().
      - Evaluate throw(translated “Account with child nodes cannot be set as ledger”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check gle exists](operations-002.md#op-e259bcb0e1464e), [validate default accounts in company](operations-001.md#op-4a6370bce13728), [check if child exists](operations-002.md#op-aecf1904571cc6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L3958) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L106)

<a id="op-4a6370bce13728"></a>
### Account.validate default accounts in company

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_default_accounts_in_company`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set default\_account\_fields from get\_company\_default\_account\_fields().
- Set company\_default\_accounts from Platform.db.get\_value(“Company”, self.company, list(default\_account\_fields.keys()), as\_dict = 1).
- Set msg from translated “Account {0} cannot be disabled as it is already set as {1} for {2}.”.
- If not self.disabled.
  - Set msg from translated “Account {0} cannot be converted to Group as it is already set as {1} for {2}.”.
- For each d in default\_account\_fields.
  - If company\_default\_accounts.get(d) equals self.name.
    - Evaluate throw(msg.format(Platform.bold(self.name), Platform.bold(default\_account\_fields.get(d)), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L4323) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L103)

<a id="op-72d3303e6d68cf"></a>
### Account.validate frozen accounts modifier

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_frozen_accounts_modifier`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (not doc\_before\_save or doc\_before\_save.freeze\_account equals self.freeze\_account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc\_before\_save → doc\_before\_save.freeze\_account equals self.freeze\_account.
  - Return no value.
- If self.flags.ignore\_root\_company\_validation.
  - Return no value.
- If not self.is\_allowed\_to\_set\_frozen\_value().
  - Evaluate throw(translated “You are not authorized to set Frozen value”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is allowed to set frozen value](operations-001.md#op-e594b5ad41bae1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L105)

<a id="op-bc464cfc93d2c4"></a>
### Account.validate balance must be debit or credit

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_balance_must_be_debit_or_credit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Account balance already in Debit, you are not allowed to set 'Balance Must Be' as 'Credit'” · validation helper — translated “Account balance already in Credit, you are not allowed to set 'Balance Must Be' as 'Debit'”.

**Local steps**

- Bind dependencies get\_balance\_on.
- If (not self.get(“\_\_islocal”) and self.balance\_must\_be).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“\_\_islocal”) → self.balance\_must\_be.
  - Set account\_balance from get\_balance\_on(self.name).
  - If (account\_balance &gt; 0 and self.balance\_must\_be equals “Credit”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_balance &gt; 0 → self.balance\_must\_be equals “Credit”.
    - Call the validation error handler Platform.throw(translated “Account balance already in Debit, you are not allowed to set 'Balance Must Be' as 'Credit'”).
  - Otherwise.
    - If (account\_balance &lt; 0 and self.balance\_must\_be equals “Debit”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_balance &lt; 0 → self.balance\_must\_be equals “Debit”.
      - Call the validation error handler Platform.throw(translated “Account balance already in Credit, you are not allowed to set 'Balance Must Be' as 'Debit'”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L4954) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L102)

<a id="op-3dee216c8c5b65"></a>
### Account.validate account currency

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_account_currency`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value · read “GL Entry” via get\_value.

**Explicit failure paths** validation helper — translated “Currency can not be changed after making entries using some other currency”.

**Local steps**

- Set self.currency\_explicitly\_specified from true.
- If not self.account\_currency.
  - Set self.account\_currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
  - Set self.currency\_explicitly\_specified from false.
- Set gl\_currency from Platform.db.get\_value(“GL Entry”, mapping(“account” → self.name, “is\_cancelled” → 0), “account\_currency”).
- If (gl\_currency and self.account\_currency differs from gl\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_currency → self.account\_currency differs from gl\_currency.
  - If Platform.db.get\_value(“GL Entry”, mapping(“account” → self.name)).
    - Call the validation error handler Platform.throw(translated “Currency can not be changed after making entries using some other currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L5244) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L100)

<a id="op-c0e53a739423b8"></a>
### Account.validate account number

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_validate_account_number`

**Inputs** self, account\_number = no value.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Account Number {0} already used in account {1}”.format(account\_number, account\_with\_same\_number).

**Local steps**

- If not account\_number.
  - Set account\_number from self.account\_number.
- If account\_number.
  - Set account\_with\_same\_number from Platform.db.get\_value(“Account”, mapping(“account\_number” → account\_number, “company” → self.company, “name” → list(“!=”, self.name))).
  - If account\_with\_same\_number.
    - Call the validation error handler Platform.throw(translated “Account Number {0} already used in account {1}”.format(account\_number, account\_with\_same\_number)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0005.json#L5609) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L101)

<a id="op-f490baa8a899ee"></a>
### Account.create account for child company

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_create_account_for_child_company`

**Inputs** self, parent\_acc\_name\_map, descendants, parent\_acc\_name.

**Record and data access** read “Account” via get\_cached\_value · read “Account” via get\_value · resolve a document from “Account” via get\_doc.

**State and service calls** request copy\_doc for self · call save on doc · msgprint with translated “Account {0} is added in the child company {1}”.format(doc.name, company).

**Explicit failure paths** validation helper — translated “While creating account for Child Company {0}, parent account {1} not found. Please create the parent account …”.format(company\_bold, parent\_acc\_name\_bold) · validation helper — msg.

**Local steps**

- For each company in descendants.
  - Set company\_bold from Platform.bold(company).
  - Set parent\_acc\_name\_bold from Platform.bold(parent\_acc\_name).
  - If not parent\_acc\_name\_map.get(company).
    - Call the validation error handler Platform.throw(translated “While creating account for Child Company {0}, parent account {1} not found. Please create the parent account …”.format(company\_bold, parent\_acc\_name\_bold), title = translated “Ac ….
  - If (Platform.get\_cached\_value(“Account”, self.parent\_account, “is\_group”) and not Platform.get\_cached\_value(“Account”, parent\_acc\_name\_map at company, “is\_group”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_cached\_value(“Account”, self.parent\_account, “is\_group”) → not Platform.get\_cached\_value(“Account”, parent\_acc\_name\_map at company, “is\_group”).
    - Set msg from translated “While creating account for Child Company {0}, parent account {1} found as a ledger account.”.format(company\_bold, parent\_acc\_name\_bold).
    - Update msg using + text in the contract.
    - Update msg using + translated “Please convert the parent account in corresponding child company to a group account.”.
    - Call the validation error handler Platform.throw(msg, title = translated “Invalid Parent Account”).
  - Set filters from mapping(“account\_name” → self.account\_name, “company” → company).
  - If self.account\_number.
    - Set filters at “account\_number” from self.account\_number.
  - Set child\_account from Platform.db.get\_value(“Account”, filters, “name”).
  - If not child\_account.
    - Set doc from Platform.copy\_doc(self).
    - Set doc.flags.ignore\_root\_company\_validation from true.
    - Evaluate doc.update(mapping(“company” → company, “account\_currency” → self.account\_currency when self.currency\_explicitly\_specified, otherwise Enterprise.get\_company\_currency(company), “parent\_account” → parent\_acc ….
      - Value choice on self.currency\_explicitly\_specified — true gives self.account\_currency, false gives Enterprise.get\_company\_currency(company).
    - Evaluate doc.save().
    - Evaluate Platform.msgprint(translated “Account {0} is added in the child company {1}”.format(doc.name, company)).
  - Otherwise.
    - If child\_account.
      - Set doc from Platform.get\_doc(“Account”, child\_account).
      - Set doc.flags.ignore\_root\_company\_validation from true.
      - Set parent\_value\_changed from false.
      - For each field in list(“account\_type”, “freeze\_account”, “balance\_must\_be”).
        - If doc.get(field) differs from self.get(field).
          - Set parent\_value\_changed from true.
          - Evaluate doc.set(field, self.get(field)).
      - If parent\_value\_changed.
        - Evaluate doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.parent\_account, “is\_group”), Platform.get\_cached\_value(“Account”, parent\_acc\_name\_map at company, “is\_group”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L93)

<a id="op-0e04221f07b80e"></a>
### Account.convert group to ledger

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_convert_group_to_ledger`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** 1.

**Local steps**

- If self.check\_if\_child\_exists().
  - Evaluate throw(translated “Account with child nodes cannot be converted to ledger”).
- Otherwise.
  - If self.check\_gle\_exists().
    - Evaluate throw(translated “Account with existing transaction cannot be converted to ledger”).
  - Otherwise.
    - Set self.is\_group from 0.
    - Evaluate self.save().
    - Return 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if child exists](operations-002.md#op-aecf1904571cc6), [check gle exists](operations-002.md#op-e259bcb0e1464e).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L1126) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L91)

<a id="op-57cef2dc93b366"></a>
### Account.convert ledger to group

`operation_enterprise_accounts_record_definitions_account_business_behavior_account_convert_ledger_to_group`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** 1.

**Local steps**

- If self.check\_gle\_exists().
  - Evaluate throw(translated “Account with existing transaction can not be converted to group.”).
- Otherwise.
  - If (self.account\_type and not self.flags.exclude\_account\_type\_check).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.account\_type → not self.flags.exclude\_account\_type\_check.
    - Evaluate throw(translated “Cannot convert to Group because Account Type is selected.”).
  - Otherwise.
    - Set self.is\_group from 1.
    - Evaluate self.save().
    - Return 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [check gle exists](operations-002.md#op-e259bcb0e1464e).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0006.json#L1334) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L92)
