# Company and master data · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Company

[Record definition](../../../../data/record-types/company.json)

<a id="op-495dd1930a3784"></a>
### Company.create default warehouses

`operation_enterprise_setup_record_definitions_company_business_behavior_company_create_default_warehouses`

**Inputs** self.

**Record and data access** read “Warehouse” via exists · resolve a document from mapping(“doctype” → “Warehouse”, “warehouse\_name” → wh\_detail at “warehouse\_name”, “is\_group” → wh\_detail at “is\_group”, “company” → self.name, …) via get\_doc · read “Warehouse” via get\_value.

**State and service calls** call insert on warehouse · call db\_set on self.

**Local steps**

- Set parent\_warehouse from no value.
- For each wh\_detail in list(mapping(“warehouse\_name” → translated “All Warehouses”, “is\_group” → 1), mapping(“warehouse\_name” → translated “Stores”, “is\_group” → 0), mapping(“warehouse\_name” → translated “Work In Progress”, “is\_ ….
  - If Platform.db.exists(“Warehouse”, mapping(“warehouse\_name” → wh\_detail at “warehouse\_name”, “company” → self.name)).
    - Continue with the next iteration or loop test.
  - Set warehouse from Platform.get\_doc(mapping(“doctype” → “Warehouse”, “warehouse\_name” → wh\_detail at “warehouse\_name”, “is\_group” → wh\_detail at “is\_group”, “company” → self.name, …)).
  - Set warehouse.flags.ignore\_permissions from true.
  - Set warehouse.flags.ignore\_mandatory from true.
  - Set warehouse.flags.ignore\_inventory\_account\_validation from true.
  - Evaluate warehouse.insert().
  - If wh\_detail at “is\_group”.
    - Set parent\_warehouse from warehouse.name.
- If not self.default\_warehouse.
  - Set stores from Platform.db.get\_value(“Warehouse”, mapping(“warehouse\_name” → translated “Stores”, “company” → self.name)).
  - If stores.
    - Evaluate self.db\_set(“default\_warehouse”, stores).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L1473) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L287)

<a id="op-fe401ece3dddb3"></a>
### Company.create default accounts

`operation_enterprise_setup_record_definitions_company_business_behavior_company_create_default_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies create\_charts.
- Set Platform.local.flags.ignore\_root\_company\_validation from true.
- Evaluate create\_charts(self.name, self.chart\_of\_accounts, self.existing\_company).
- Evaluate self.db\_set(“default\_receivable\_account”, Platform.db.get\_value(“Account”, mapping(“company” → self.name, “account\_type” → “Receivable”, “is\_group” → 0))).
- Evaluate self.db\_set(“default\_payable\_account”, Platform.db.get\_value(“Account”, mapping(“company” → self.name, “account\_type” → “Payable”, “is\_group” → 0))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L2351) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L283)

<a id="op-99980d5651d30d"></a>
### Company.create default departments

`operation_enterprise_setup_record_definitions_company_business_behavior_company_create_default_departments`

**Inputs** self.

**Local steps**

- Set root from (get\_root\_of(“Department”) or “All Departments”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_root\_of(“Department”) → “All Departments”.
- Set records from list(mapping(“doctype” → “Department”, “department\_name” → root, “is\_group” → 1, “parent\_department” → empty text, …), mapping(“doctype” → “Department”, “department\_name” → translated “Accounts”, “parent\_d ….
- Evaluate make\_records(records at slice no value to 1).
- Set Platform.local.flags.ignore\_update\_nsm from true.
- Evaluate make\_records(records).
- Set Platform.local.flags.ignore\_update\_nsm from false.
- Evaluate rebuild\_tree(“Department”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L2688) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L285)

<a id="op-6f463628704ee6"></a>
### Company.validate coa input

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_chart_of_accounts_input`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select Existing Company for creating Chart of Accounts”.

**Local steps**

- <a id="op-6f463628704ee6-guard-2"></a>If self.create\_chart\_of\_accounts\_based\_on equals “Existing Company”.
  - Set self.chart\_of\_accounts from no value.
  - If not self.existing\_company.
    - Call the validation error handler Platform.throw(translated “Please select Existing Company for creating Chart of Accounts”).
- Otherwise.
  - Set self.existing\_company from no value.
  - Set self.create\_chart\_of\_accounts\_based\_on from “Standard Template”.
  - If not self.chart\_of\_accounts.
    - Set self.chart\_of\_accounts from “Standard”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.create\_chart\_of\_accounts\_based\_on equals “Existing Company”, self.create\_chart\_of\_accounts\_based\_on = “Existing Company” selects the branch that assigns no value to self.chart\_of\_accounts. With self.create\_chart\_of\_accounts\_based\_on = “Standard Template”, the alternative assigns no value to self.existing\_company. [Local guard](#op-6f463628704ee6-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L4241) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L298)

<a id="op-6f3ca066ba0ed9"></a>
### Company.validate perpetual inventory

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_perpetual_inventory`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**State and service calls** msgprint with translated “Set default inventory account for perpetual inventory”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot disable perpetual inventory, as there are existing Stock Ledger Entries for the company {0}. Please c …”.format(bold(self.name)).

**Local steps**

- If not self.get(“\_\_islocal”).
  - If (cint(self.enable\_perpetual\_inventory) equals 1 and not self.default\_inventory\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.enable\_perpetual\_inventory) equals 1 → not self.default\_inventory\_account.
    - Evaluate Platform.msgprint(translated “Set default inventory account for perpetual inventory”, alert = true, indicator = “orange”).
- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- If (doc\_before\_save.enable\_perpetual\_inventory and not self.enable\_perpetual\_inventory).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save.enable\_perpetual\_inventory → not self.enable\_perpetual\_inventory.
  - If Platform.db.get\_value(“Stock Ledger Entry”, mapping(“is\_cancelled” → 0, “company” → self.name), “name”).
    - Call the validation error handler Platform.throw(translated “Cannot disable perpetual inventory, as there are existing Stock Ledger Entries for the company {0}. Please c …”.format(bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L304)

<a id="op-58f294eee0c281"></a>
### Company.validate provisional account for non stock items

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_provisional_account_for_non_stock_items`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Set default {0} account for non stock items”.format(Platform.bold(translated “Provisional Account”)).

**Local steps**

- If not self.get(“\_\_islocal”).
  - If (cint(self.enable\_provisional\_accounting\_for\_non\_stock\_items) equals 1 and not self.default\_provisional\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.enable\_provisional\_accounting\_for\_non\_stock\_items) equals 1 → not self.default\_provisional\_account.
    - Call the validation error handler Platform.throw(translated “Set default {0} account for non stock items”.format(Platform.bold(translated “Provisional Account”))).
  - Evaluate self.set\_provisional\_expense\_visibility(self.enable\_provisional\_accounting\_for\_non\_stock\_items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set provisional expense visibility](operations-002.md#op-02cdeabb3c6098).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L305)

<a id="op-02cdeabb3c6098"></a>
### Company.set provisional expense visibility

`operation_enterprise_binding_enterprise_setup_doctype_company_company_company_set_provisional_expense_visibility`

**Inputs** self, enabled.

**Record and data access** read “Company” via exists.

**Local steps**

- Set other\_company\_enabled from Platform.db.exists(“Company”, mapping(“name” → list(“!=”, self.name), “enable\_provisional\_accounting\_for\_non\_stock\_items” → 1)).
- Evaluate make\_property\_setter(“Purchase Receipt”, “provisional\_expense\_account”, “hidden”, not (enabled or other\_company\_enabled), validate\_fields\_for\_doctype = false, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in enabled → other\_company\_enabled.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L141)

<a id="op-a4ccb2b41c6b10"></a>
### Company.check country change

`operation_enterprise_setup_record_definitions_company_business_behavior_company_check_country_change`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Set Platform.flags.country\_change from false.
- If (not self.is\_new() and self.country differs from Platform.get\_cached\_value(“Company”, self.name, “country”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.country differs from Platform.get\_cached\_value(“Company”, self.name, “country”).
  - Set Platform.flags.country\_change from true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.name, “country”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L5147) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L280)

<a id="op-8618353a493403"></a>
### Company.set chart of accounts

`operation_enterprise_setup_record_definitions_company_business_behavior_company_set_chart_of_accounts`

**Inputs** self.

**Local steps**

- If self.parent\_company.
  - Set self.create\_chart\_of\_accounts\_based\_on from “Existing Company”.
  - Set self.existing\_company from self.parent\_company.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L5311) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L291)

<a id="op-e48c8b10f592b2"></a>
### Company.validate parent company

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_parent_company`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Explicit failure paths** validation helper — translated “Parent Company must be a group company”.

**Local steps**

- If self.parent\_company.
  - Set is\_group from Platform.get\_value(“Company”, self.parent\_company, “is\_group”).
  - If not is\_group.
    - Call the validation error handler Platform.throw(translated “Parent Company must be a group company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L5393) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L302)

<a id="op-97248f668428d5"></a>
### Company.set reporting currency

`operation_enterprise_setup_record_definitions_company_business_behavior_company_set_reporting_currency`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set self.reporting\_currency from self.default\_currency.
- If self.parent\_company.
  - Set parent\_reporting\_currency from Platform.db.get\_value(“Company”, self.parent\_company, list(“reporting\_currency”)).
  - Set self.reporting\_currency from parent\_reporting\_currency.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L5541) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L295)

<a id="op-3c6dc41bf79a2c"></a>
### Company.validate pending reposts

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_pending_reposts`

**Inputs** self, old\_doc.

**Local steps**

- If (old\_doc and old\_doc.accounts\_frozen\_till\_date differs from self.accounts\_frozen\_till\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_doc → old\_doc.accounts\_frozen\_till\_date differs from self.accounts\_frozen\_till\_date.
  - If self.accounts\_frozen\_till\_date.
    - Evaluate check\_pending\_reposting(self.accounts\_frozen\_till\_date, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0683.json#L5684) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L303)

<a id="op-9ae66e9fb3e155"></a>
### Company.set default accounts

`operation_enterprise_setup_record_definitions_company_business_behavior_company_set_default_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_all · read “Account” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- Set default\_accounts from mapping(“default\_cash\_account” → “Cash”, “default\_bank\_account” → “Bank”, “round\_off\_account” → “Round Off”, “accumulated\_depreciation\_account” → “Accumulated Depreciation”, …).
- If self.enable\_perpetual\_inventory.
  - Evaluate default\_accounts.update(mapping(“stock\_received\_but\_not\_billed” → “Stock Received But Not Billed”, “default\_inventory\_account” → “Stock”, “stock\_adjustment\_account” → “Stock Adjustment”)).
- If self.update\_default\_account.
  - For each default\_account in default\_accounts.
    - Evaluate self.\_set\_default\_account(default\_account, default\_accounts.get(default\_account)).
- If not self.update\_default\_account.
  - Return no value.
- If not self.default\_income\_account.
  - Set income\_account from Platform.db.get\_all(“Account”, filters = mapping(“company” → self.name, “is\_group” → 0), or\_filters = mapping(“account\_name” → tuple(“in”, list(translated “Sales”, translated “Sales Account”)), “account\_ty ….
  - If income\_account.
    - Set income\_account from income\_account at 0.
  - Otherwise.
    - Set income\_account from no value.
  - Evaluate self.db\_set(“default\_income\_account”, income\_account).
- If not self.default\_payable\_account.
  - Evaluate self.db\_set(“default\_payable\_account”, self.default\_payable\_account).
- If not self.write\_off\_account.
  - Set write\_off\_acct from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Write Off”, “company” → self.name, “is\_group” → 0)).
  - Evaluate self.db\_set(“write\_off\_account”, write\_off\_acct).
- If not self.exchange\_gain\_loss\_account.
  - Set exchange\_gain\_loss\_acct from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Exchange Gain/Loss”, “company” → self.name, “is\_group” → 0)).
  - Evaluate self.db\_set(“exchange\_gain\_loss\_account”, exchange\_gain\_loss\_acct).
- If not self.disposal\_account.
  - Set disposal\_acct from Platform.db.get\_value(“Account”, mapping(“account\_name” → translated “Gain/Loss on Asset Disposal”, “company” → self.name, “is\_group” → 0)).
  - Evaluate self.db\_set(“disposal\_account”, disposal\_acct).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default account](operations-002.md#op-eeba9dafbe1199).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L293)

<a id="op-eeba9dafbe1199"></a>
### Company.set default account

`operation_enterprise_setup_record_definitions_company_business_behavior_company_set_default_account`

**Inputs** self, fieldname, account\_type.

**Record and data access** read “Account” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If self.get(fieldname).
  - Return no value.
- Set account from Platform.db.get\_value(“Account”, mapping(“account\_type” → account\_type, “is\_group” → 0, “company” → self.name)).
- If account.
  - Evaluate self.db\_set(fieldname, account).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0684.json#L1644) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L292)

<a id="op-b16287671e177a"></a>
### Company.set mode of payment account

`operation_enterprise_setup_record_definitions_company_business_behavior_company_set_mode_of_payment_account`

**Inputs** self.

**Record and data access** read “Mode of Payment” via get\_value · read “Mode of Payment Account” via get\_value · resolve a document from “Mode of Payment” via get\_doc.

**State and service calls** call save on mode\_of\_payment.

**Local steps**

- Set cash from Platform.db.get\_value(“Mode of Payment”, mapping(“type” → “Cash”), “name”).
- If (cash and self.default\_cash\_account and not Platform.db.get\_value(“Mode of Payment Account”, mapping(“company” → self.name, “parent” → cash))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cash → self.default\_cash\_account → not Platform.db.get\_value(“Mode of Payment Account”, mapping(“company” → self.name, “parent” → cash)).
  - Set mode\_of\_payment from Platform.get\_doc(“Mode of Payment”, cash, for\_update = true).
  - Evaluate mode\_of\_payment.append(“accounts”, mapping(“company” → self.name, “default\_account” → self.default\_cash\_account)).
  - Evaluate mode\_of\_payment.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0684.json#L1855) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L294)

<a id="op-b1a2639a2bf84d"></a>
### Company.create default cost center

`operation_enterprise_setup_record_definitions_company_business_behavior_company_create_default_cost_center`

**Inputs** self.

**Record and data access** resolve a document from cc via get\_doc.

**State and service calls** call insert on cc\_doc · call db\_set on self.

**Local steps**

- Set cc\_list from list(mapping(“cost\_center\_name” → self.name, “company” → self.name, “is\_group” → 1, “parent\_cost\_center” → no value), mapping(“cost\_center\_name” → translated “Main”, “company” → self.name, “is\_group” → 0,  ….
- For each cc in cc\_list.
  - Evaluate cc.update(mapping(“doctype” → “Cost Center”)).
  - Set cc\_doc from Platform.get\_doc(cc).
  - Set cc\_doc.flags.ignore\_permissions from true.
  - If cc.get(“cost\_center\_name”) equals self.name.
    - Set cc\_doc.flags.ignore\_mandatory from true.
  - Evaluate cc\_doc.insert().
- Evaluate self.db\_set(“cost\_center”, ((translated “Main” + “ - ”) + self.abbr)).
- Evaluate self.db\_set(“round\_off\_cost\_center”, ((translated “Main” + “ - ”) + self.abbr)).
- Evaluate self.db\_set(“depreciation\_cost\_center”, ((translated “Main” + “ - ”) + self.abbr)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0684.json#L2204) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L284)

<a id="op-7a778bc1e83ef0"></a>
### Company.after rename

`operation_enterprise_setup_record_definitions_company_business_behavior_company_after_rename`

**Inputs** self, olddn, newdn, merge = false.

**State and service calls** call db\_set on self · execute query text (UPDATE, Default Value).

**Local steps**

- Evaluate self.db\_set(“company\_name”, newdn).
- Evaluate Platform.db.sql(query text (UPDATE, Default Value), tuple(newdn, olddn)).
- Evaluate clear\_defaults\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L278)

<a id="op-97bd4f5fed7ba9"></a>
### Company.abbreviate

`operation_enterprise_setup_record_definitions_company_business_behavior_company_abbreviate`

**Inputs** self.

**Local steps**

- Set self.abbr from empty text.join(generator of c at 0.upper() for c drawn from self.company\_name.split()).
  - Draw c from self.company\_name.split().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0684.json#L3110) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L277)

<a id="op-a21d759339e0a2"></a>
### Company.on trash

`operation_enterprise_setup_record_definitions_company_business_behavior_company_on_trash`

**Inputs** self.

**Record and data access** read “Global Defaults” via get\_single\_value · read doctype via exists · read “Warehouse” via get\_all · read “GL Entry” via exists · read “Budget” via get\_all · 3 additional forms in the steps below.

**State and service calls** request delete on “Budget Account” · execute a supplied database query · request delete on “Item Reorder” · request set\_value on “Item Reorder” · request delete on “Warehouse” · 8 additional forms in the steps below.

**Explicit failure paths** validation helper — translated “{0} is the site's Demo Company and cannot be deleted directly. Use {1} instead.”.format(bold(self.name), bold(translated “Delete Demo Data”)) · validation helper — translated “Cannot delete {0} while {1} records exist”.format(self.name, doctype).

**Local steps**

- If Platform.db.get\_single\_value(“Global Defaults”, “demo\_company”) equals self.name.
  - Call the validation error handler Platform.throw(translated “{0} is the site's Demo Company and cannot be deleted directly. Use {1} instead.”.format(bold(self.name), bold(translated “Delete Demo Data”))).
- Evaluate NestedSet.validate\_if\_child\_exists(self).
- For each doctype in tuple(“BOM”, “Employee”).
  - If Platform.db.exists(doctype, mapping(“company” → self.name)).
    - Call the validation error handler Platform.throw(translated “Cannot delete {0} while {1} records exist”.format(self.name, doctype)).
- Evaluate Platform.utils.nestedset.update\_nsm(self).
- Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“company” → self.name), pluck = “name”).
- If not Platform.db.exists(“GL Entry”, mapping(“company” → self.name)).
  - Set budgets from Platform.get\_all(“Budget”, filters = mapping(“company” → self.name), pluck = “name”).
  - If budgets.
    - Evaluate Platform.db.delete(“Budget Account”, mapping(“parent” → list(“in”, budgets))).
  - For each doctype in list(“Account”, “Cost Center”, “Budget”, “Party Account”).
    - Evaluate Platform.db.sql(formatted text delete from ′tab{doctype}′ where company = %s, self.name).
- If not Platform.db.get\_value(“Stock Ledger Entry”, mapping(“company” → self.name)).
  - If warehouses.
    - Evaluate Platform.db.delete(“Item Reorder”, mapping(“warehouse” → list(“in”, warehouses))).
    - Evaluate Platform.db.set\_value(“Item Reorder”, mapping(“warehouse\_group” → list(“in”, warehouses)), “warehouse\_group”, no value).
  - Evaluate Platform.db.delete(“Warehouse”, mapping(“company” → self.name)).
- Evaluate Platform.defaults.clear\_default(“company”, value = self.name).
- For each doctype in list(“Mode of Payment Account”, “Item Default”).
  - Evaluate Platform.db.sql(formatted text delete from ′tab{doctype}′ where company = %s, self.name).
- Evaluate Platform.db.sql(query text (UPDATE, Singles), self.name).
- Evaluate Platform.db.sql(query text (UPDATE, Singles), self.name).
- Evaluate Platform.db.delete(“Department”, mapping(“company” → self.name)).
- Evaluate Platform.db.delete(“Tax Withholding Account”, mapping(“company” → self.name)).
- Evaluate Platform.db.delete(“Transaction Deletion Record”, mapping(“company” → self.name)).
- For each tuple(template, child) in tuple(tuple(“Sales Taxes and Charges Template”, “Sales Taxes and Charges”), tuple(“Purchase Taxes and Charges Template”, “Purchase Taxes and Charges”), tuple(“Item Tax Template”, “Item Tax Template Detail”)).
  - Set names from Platform.get\_all(template, filters = mapping(“company” → self.name), pluck = “name”).
  - If names.
    - If template equals “Item Tax Template”.
      - Evaluate Platform.db.delete(“Item Tax”, mapping(“item\_tax\_template” → list(“in”, names))).
    - Evaluate Platform.db.delete(child, mapping(“parent” → list(“in”, names), “parenttype” → template)).
    - Evaluate Platform.db.delete(template, mapping(“name” → list(“in”, names))).
- If not Platform.db.get\_value(“GL Entry”, mapping(“company” → self.name)).
  - Evaluate Platform.db.sql(query text (DELETE, Process Deferred Accounting), self.name).
- If self.enable\_provisional\_accounting\_for\_non\_stock\_items.
  - Evaluate self.set\_provisional\_expense\_visibility(false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set provisional expense visibility](operations-002.md#op-02cdeabb3c6098).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “demo\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L288)

<a id="op-c3e293bcb72f26"></a>
### Company.check parent changed

`operation_enterprise_setup_record_definitions_company_business_behavior_company_check_parent_changed`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set Platform.flags.parent\_company\_changed from false.
- If (not self.is\_new() and self.parent\_company differs from Platform.db.get\_value(“Company”, self.name, “parent\_company”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.parent\_company differs from Platform.db.get\_value(“Company”, self.name, “parent\_company”).
  - Set Platform.flags.parent\_company\_changed from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0684.json#L5358) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L282)

<a id="op-9a3f1caea70248"></a>
### Get name with abbr

`operation_enterprise_setup_record_definitions_company_business_behavior_get_name_with_abbreviation`

**Inputs** name, company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** “ - ”.join(parts).

**Local steps**

- Set company\_abbr from Platform.get\_cached\_value(“Company”, company, “abbr”).
- Set parts from name.split(“ - ”).
- If parts at negative 1.lower() differs from company\_abbr.lower().
  - Evaluate parts.append(company\_abbr).
- Return “ - ”.join(parts).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “abbr”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0684.json#L5526) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L312)

<a id="op-3304e76da579c5"></a>
### Install country fixtures

`operation_enterprise_setup_record_definitions_company_business_behavior_install_country_fixtures`

**Inputs** company, country.

**Explicit failure paths** validation helper — translated “Failed to setup defaults for country {0}. Please contact support.”.format(Platform.bold(country)).

**Local steps**

- Attempt the following.
  - Set module\_name from formatted text Enterprise.regional.{Platform.scrub(country)}.setup.setup.
  - Evaluate Platform.get\_attr(module\_name)(company, false).
- On failure (ImportError).
  - Take no action here.
- On failure (Exception).
  - Evaluate Platform.log\_error(“Unable to set country fixtures”).
  - Call the validation error handler Platform.throw(translated “Failed to setup defaults for country {0}. Please contact support.”.format(Platform.bold(country))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(module\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L314)

<a id="op-72189f6c95c922"></a>
### Update company current month sales

`operation_enterprise_setup_record_definitions_company_business_behavior_update_company_current_month_sales`

**Inputs** company.

**State and service calls** request set\_value on “Company”.

**Local steps**

- Bind dependencies Sum.
- Set start\_date from get\_first\_day(today()).
- Set end\_date from get\_last\_day(today()).
- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set total\_monthly\_sales from (nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract ≤ nested operan ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).where((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested  … at 0 → 0.
- Evaluate Platform.db.set\_value(“Company”, company, “total\_monthly\_sales”, total\_monthly\_sales, update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L315)

<a id="op-1c38aefce1b555"></a>
### Update company monthly sales

`operation_enterprise_setup_record_definitions_company_business_behavior_update_company_monthly_sales`

**Inputs** company.

**State and service calls** request set\_value on “Company”.

**Local steps**

- Bind dependencies get\_monthly\_results.
- Set filter\_dict from mapping(“company” → company, “status” → list(“!=”, “Draft”), “docstatus” → 1, “is\_opening” → list(“!=”, “Yes”)).
- Set month\_to\_value\_dict from get\_monthly\_results(“Sales Invoice”, “base\_grand\_total”, “posting\_date”, filter\_dict, …).
- Evaluate Platform.db.set\_value(“Company”, company, “sales\_monthly\_history”, json.dumps(month\_to\_value\_dict)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L316)
