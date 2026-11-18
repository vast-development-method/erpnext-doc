# Accounting and settlement · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Account

[Record definition](../../../../data/record-types/account.json)

<a id="op-7c37002c3c2b65"></a>
### Create charts.import accounts

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_create_charts_import_accounts`

**Inputs** children, parent, root\_type, root\_account = false.

**Record and data access** resolve a document from mapping(“doctype” → “Account”, “account\_name” → child.get(“account\_name”) when from\_coa\_importer, otherwise account\_name, “company” → company, “parent\_account” → parent, …) via get\_doc · read “Company” via get\_cached\_value.

**State and service calls** call insert on account.

**Local steps**

- Use enclosing bindings custom\_chart.
- For each tuple(account\_name, child) in children.items().
  - If root\_account.
    - Set root\_type from child.get(“root\_type”).
  - If account\_name does not belong to get\_chart\_metadata\_fields().
    - Set account\_number from cstr(child.get(“account\_number”)).strip().
    - Set tuple(account\_name, account\_name\_in\_db) from add\_suffix\_if\_duplicate(account\_name, account\_number, accounts).
    - Set is\_group from identify\_is\_group(child).
    - Set report\_type from “Balance Sheet” when root\_type belongs to list(“Asset”, “Liability”, “Equity”), otherwise “Profit and Loss”.
      - Value choice on root\_type belongs to list(“Asset”, “Liability”, “Equity”) — true gives “Balance Sheet”, false gives “Profit and Loss”.
    - Set account from Platform.get\_doc(mapping(“doctype” → “Account”, “account\_name” → child.get(“account\_name”) when from\_coa\_importer, otherwise account\_name, “company” → company, “parent\_account” → parent, …)).
      - Value choice on from\_coa\_importer — true gives child.get(“account\_name”), false gives account\_name.
      - Value choice on custom\_chart — true gives child.get(“account\_currency”), false gives Platform.get\_cached\_value(“Company”, company, “default\_currency”).
    - If (root\_account or Platform.local.flags.allow\_unverified\_charts).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in root\_account → Platform.local.flags.allow\_unverified\_charts.
      - Set account.flags.ignore\_mandatory from true.
    - Set account.flags.ignore\_permissions from true.
    - Evaluate account.insert().
    - Evaluate accounts.append(account\_name\_in\_db).
    - Evaluate \_import\_accounts(child, account.name, root\_type).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0994.json#L3452) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L133)

<a id="op-5553c9a56be99a"></a>
### Add suffix if duplicate

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_add_suffix_if_duplicate`

**Inputs** account\_name, account\_number, accounts.

**Explicit results** tuple(account\_name, account\_name\_in\_db).

**Local steps**

- If account\_number.
  - Set account\_name\_in\_db from unidecode(“ - ”.join(list(account\_number, nested operand in the contract.strip().lower()))).
- Otherwise.
  - Set account\_name\_in\_db from unidecode(account\_name.strip().lower()).
- If account\_name\_in\_db belongs to accounts.
  - Set count from accounts.count(account\_name\_in\_db).
  - Set account\_name from ((account\_name + one space) + cstr(count)).
- Return tuple(account\_name, account\_name\_in\_db).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0007.json#L1130) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L128)

<a id="op-9bd3b7e145260e"></a>
### Identify is group

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_identify_is_group`

**Inputs** child.

**Explicit results** is\_group.

**Local steps**

- If child.get(“is\_group”).
  - Set is\_group from child.get(“is\_group”).
- Otherwise.
  - If len((set(child.keys()) − set(get\_chart\_metadata\_fields()))).
    - Set is\_group from 1.
  - Otherwise.
    - Set is\_group from 0.
- Return is\_group.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0007.json#L1413) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L139)

<a id="op-4e586c9aade053"></a>
### Get chart

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_get_chart`

**Inputs** chart\_template, existing\_company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_account\_tree\_from\_existing\_company(existing\_company) · standard\_chart\_of\_accounts.get() · standard\_chart\_of\_accounts\_with\_account\_number.get() · json.loads(chart).get(“tree”).

**Local steps**

- Set chart from mapping().
- If existing\_company.
  - Evaluate Platform.has\_permission(“Company”, doc = existing\_company, throw = true).
  - Return get\_account\_tree\_from\_existing\_company(existing\_company).
- Otherwise.
  - If chart\_template equals “Standard”.
    - Bind dependencies standard\_chart\_of\_accounts.
    - Return standard\_chart\_of\_accounts.get().
  - Otherwise.
    - If chart\_template equals “Standard with Numbers”.
      - Bind dependencies standard\_chart\_of\_accounts\_with\_account\_number.
      - Return standard\_chart\_of\_accounts\_with\_account\_number.get().
    - Otherwise.
      - Set folders from tuple(“verified”).
      - If Platform.local.flags.allow\_unverified\_charts.
        - Set folders from tuple(“verified”, “unverified”).
      - For each folder in folders.
        - Set path from os.path.join(os.path.dirname(\_\_file\_\_), folder).
        - For each fname in os.listdir(path).
          - Set fname from Platform.as\_unicode(fname).
          - If fname.endswith(“.json”).
            - Within open(os.path.join(path, fname)) bound as f.
              - Set chart from f.read().
              - If (chart and json.loads(chart).get(“name”) equals chart\_template).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in chart → json.loads(chart).get(“name”) equals chart\_template.
                - Return json.loads(chart).get(“tree”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, doc = existing\_company, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, file state, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L135)

<a id="op-5d9ef05944da33"></a>
### Get charts for country

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_get_charts_for_country`

**Inputs** country, with\_standard = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Country” via get\_cached\_value.

**Explicit results** charts.

**Local steps**

- Set charts from list().
- Bind local operation \_get\_chart\_name for subsequent calls.
- Set country\_code from Platform.get\_cached\_value(“Country”, country, “code”).
- If country\_code.
  - Set folders from tuple(“verified”).
  - If Platform.local.flags.allow\_unverified\_charts.
    - Set folders from tuple(“verified”, “unverified”).
  - For each folder in folders.
    - Set path from os.path.join(os.path.dirname(\_\_file\_\_), folder).
    - If not os.path.exists(path).
      - Continue with the next iteration or loop test.
    - For each fname in os.listdir(path).
      - Set fname from Platform.as\_unicode(fname).
      - If ((fname.startswith(country\_code) or fname.startswith(country)) and fname.endswith(“.json”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in (fname.startswith(country\_code) or fname.startswith(country)) → fname.endswith(“.json”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in fname.startswith(country\_code) → fname.startswith(country).
        - Within open(os.path.join(path, fname)) bound as f.
          - Evaluate \_get\_chart\_name(f.read()).
- If (len(charts) differs from 1 or with\_standard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(charts) differs from 1 → with\_standard.
  - Update charts using + list(“Standard”, “Standard with Numbers”).
- Return charts.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Country”, country, “code”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L137)

<a id="op-2b4f30b090783c"></a>
### Get charts for country.get chart name

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_get_charts_for_country_get_chart_name`

**Inputs** content.

**Local steps**

- If content.
  - Set content from json.loads(content).
  - If ((content and content.get(“disabled”, “No”) equals “No”) or Platform.local.flags.allow\_unverified\_charts).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (content and content.get(“disabled”, “No”) equals “No”) → Platform.local.flags.allow\_unverified\_charts.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in content → content.get(“disabled”, “No”) equals “No”.
    - Evaluate charts.append(content at “name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L138)

<a id="op-c6bed59f1f014b"></a>
### Get account tree from existing company

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_get_account_tree_from_existing_company`

**Inputs** existing\_company.

**Record and data access** read “Account” via get\_all.

**Explicit results** account\_tree.

**Local steps**

- Set all\_accounts from Platform.get\_all(“Account”, filters = mapping(“company” → existing\_company), fields = list(“name”, “account\_name”, “parent\_account”, “account\_type”, …), order\_by = “lft, rgt”).
- Set account\_tree from mapping().
- If all\_accounts.
  - Evaluate build\_account\_tree(account\_tree, no value, all\_accounts).
- Return account\_tree.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0007.json#L3268) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L134)

<a id="op-287fe4fd89b468"></a>
### Build account tree

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_build_account_tree`

**Inputs** tree, parent, all\_accounts.

**Local steps**

- Set parent\_account from parent.name when parent, otherwise empty text.
  - Value choice on parent — true gives parent.name, false gives empty text.
- Set children from list of acc for acc drawn from all\_accounts where cstr(acc.parent\_account) equals parent\_account.
  - Draw acc from all\_accounts, keep a combination only if (cstr(acc.parent\_account) equals parent\_account).
- If (not children and parent.is\_group).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not children → parent.is\_group.
  - Set tree at “is\_group” from 1.
  - Set tree at “account\_number” from parent.account\_number.
- For each child in children.
  - Set tree at child.account\_name from mapping().
  - If child.account\_number.
    - Set tree at child.account\_name at “account\_number” from child.account\_number.
  - If child.account\_type.
    - Set tree at child.account\_name at “account\_type” from child.account\_type.
  - If child.tax\_rate.
    - Set tree at child.account\_name at “tax\_rate” from child.tax\_rate.
  - If child.account\_currency.
    - Set tree at child.account\_name at “account\_currency” from child.account\_currency.
  - If not parent.
    - Set tree at child.account\_name at “root\_type” from child.root\_type.
  - Evaluate build\_account\_tree(tree at child.account\_name, child, all\_accounts).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0007.json#L3520) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L129)

<a id="op-0f245e17f9b230"></a>
### Validate bank account

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_validate_bank_account`

**Inputs** coa, bank\_account.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** bank\_account belongs to accounts.

**Local steps**

- Set accounts from list().
- Set chart from get\_chart(coa).
- If chart.
  - Bind local operation \_get\_account\_names for subsequent calls.
  - Evaluate \_get\_account\_names(chart).
- Return bank\_account belongs to accounts.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L140)

<a id="op-2b8b01b3739454"></a>
### Validate bank account.get account names

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_validate_bank_account_get_account_names`

**Inputs** account\_master.

**Local steps**

- For each tuple(account\_name, child) in account\_master.items().
  - If account\_name does not belong to get\_chart\_metadata\_fields().
    - Evaluate accounts.append(account\_name).
    - Evaluate \_get\_account\_names(child).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0994.json#L4342) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L141)

<a id="op-10fc0650ae6058"></a>
### Build tree from json

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_build_tree_from_structured_data`

**Inputs** chart\_template, chart\_data = no value, from\_coa\_importer = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · accounts.

**Local steps**

- Set chart from (chart\_data or get\_chart(chart\_template)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in chart\_data → get\_chart(chart\_template).
- If not chart.
  - Return no value.
- Set accounts from list().
- Bind local operation \_import\_accounts for subsequent calls.
- Evaluate \_import\_accounts(chart, no value).
- Return accounts.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L130)

<a id="op-cbde970f0e53c8"></a>
### Build tree from json.import accounts

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_build_tree_from_structured_data_import_accounts`

**Inputs** children, parent.

**Local steps**

- For each tuple(account\_name, child) in children.items().
  - Set account from mapping().
  - If account\_name belongs to get\_chart\_metadata\_fields().
    - Continue with the next iteration or loop test.
  - If from\_coa\_importer.
    - Set account\_name from child at “account\_name”.
  - Set account at “parent\_account” from parent.
  - Set account at “expandable” from true when identify\_is\_group(child), otherwise false.
    - Value choice on identify\_is\_group(child) — true gives true, false gives false.
  - Set account at “value” from ((cstr(nested operand in the contract(nested operand in the contract)).strip() + “ - ”) + account\_name) when child.get(“account\_number”), otherwise account\_name.
    - Value choice on child.get(“account\_number”) — true gives ((cstr(nested operand in the contract.get(“account\_number”)).strip() + “ - ”) + account\_name), false gives account\_name.
  - Evaluate accounts.append(account).
  - Evaluate \_import\_accounts(child, account at “value”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0007.json#L4958) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L131)

<a id="op-9a57716da1ec92"></a>
### Get chart metadata fields

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_business_behavior_get_chart_metadata_fields`

**Inputs** no declared parameters.

**Explicit results** list(“account\_name”, “account\_number”, “account\_type”, “account\_category”, …).

**Local steps**

- Return list(“account\_name”, “account\_number”, “account\_type”, “account\_category”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0007.json#L5362) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L136)

<a id="op-85d2e269b02c79"></a>
### Get

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_verified_standard_chart_of_accounts_business_behavior_get`

**Inputs** no declared parameters.

**Explicit results** mapping(translated “Application of Funds (Assets)” → mapping(translated “Current Assets” → mapping(translated “Accounts Receivable” → mapping(translated “Debtors” → mapping(“account\_type” → “Receivable”, “ ….

**Local steps**

- Return mapping(translated “Application of Funds (Assets)” → mapping(translated “Current Assets” → mapping(translated “Accounts Receivable” → mapping(translated “Debtors” → mapping(“account\_type” → “Receivable”, “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L142)

<a id="op-382411d28a1f9b"></a>
### Get

`operation_enterprise_accounts_record_definitions_account_chart_of_accounts_verified_standard_chart_of_accounts_with_account_number_business_behavior_get`

**Inputs** no declared parameters.

**Explicit results** mapping(translated “Application of Funds (Assets)” → mapping(translated “Current Assets” → mapping(translated “Accounts Receivable” → mapping(translated “Debtors” → mapping(“account\_type” → “Receivable”, “ ….

**Local steps**

- Return mapping(translated “Application of Funds (Assets)” → mapping(translated “Current Assets” → mapping(translated “Accounts Receivable” → mapping(translated “Debtors” → mapping(“account\_type” → “Receivable”, “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L143)

## Report · Account balance

<a id="op-43c91e496a5776"></a>
### Execute

`operation_enterprise_accounts_report_account_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L4698) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L521)

<a id="op-44e0ff773c9490"></a>
### Get columns

`operation_enterprise_accounts_report_account_balance_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Account”, “fieldtype” → “Link”, “fieldname” → “account”, “options” → “Account”, …), mapping(“label” → translated “Currency”, “fieldtype” → “Link”, “fieldname” → “currency ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L4842) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L522)

<a id="op-b320d00a71722b"></a>
### Get conditions

`operation_enterprise_accounts_report_account_balance_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Set conditions from mapping().
- If filters.account\_type.
  - Set conditions at “account\_type” from filters.account\_type.
- If filters.company.
  - Set conditions at “company” from filters.company.
- If filters.root\_type.
  - Set conditions at “root\_type” from filters.root\_type.
- Return conditions.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0214.json#L5250) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L523)

<a id="op-78f765016ad077"></a>
### Get data

`operation_enterprise_accounts_report_account_balance_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Account” via get\_list.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set conditions from get\_conditions(filters).
- Set accounts from Platform.get\_list(“Account”, fields = list(“name”, “account\_currency”, “report\_type”, “company”), filters = conditions, order\_by = “name”).
- For each d in accounts.
  - Set start\_date from get\_year\_start\_date(filters.report\_date, d.company) when d.report\_type equals “Profit and Loss”, otherwise no value.
    - Value choice on d.report\_type equals “Profit and Loss” — true gives get\_year\_start\_date(filters.report\_date, d.company), false gives no value.
  - Set balance from get\_balance\_on(d.name, date = filters.report\_date, start\_date = start\_date, apply\_gl\_entry\_permissions = true).
  - Set row from mapping(“account” → d.name, “balance” → balance, “currency” → d.account\_currency).
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L524)

<a id="op-61e633179a3f06"></a>
### Get year start date

`operation_enterprise_binding_enterprise_accounts_report_account_balance_account_balance_get_year_start_date`

**Inputs** report\_date, company.

**Explicit results** fiscal\_year at 1 when fiscal\_year, otherwise no value.

**Local steps**

- Set fiscal\_year from get\_fiscal\_year(report\_date, company = company, verbose = 0, raise\_on\_missing = false).
- Return fiscal\_year at 1 when fiscal\_year, otherwise no value.
  - Value choice on fiscal\_year — true gives fiscal\_year at 1, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1109)

## Service · Account balance timeline

<a id="op-899e4b3e38d02f"></a>
### Get

`operation_enterprise_accounts_dashboard_chart_source_account_balance_timeline_business_behavior_get`

**Inputs** chart\_name = no value, chart = no value, no\_cache = no value, filters = no value, from\_date = no value, to\_date = no value, timespan = no value, time\_interval = no value, heatmap\_year = no value.

**Wrappers, in declaration order** Platform.whitelist(), cache\_source.

**Record and data access** resolve a document from “Dashboard Chart” via get\_doc · read “Account” via exists.

**Explicit results** mapping(“labels” → list of formatdate(r at 0.strftime(“%Y-%m-%d”)) for r drawn from result, “datasets” → list(mapping(“name” → account, “values” → list of r at 1 for r drawn from result))).

**Explicit failure paths** validation helper — translated “Choose a company in this chart's filters to see its bank balance.” · validation helper — translated “Choose a bank account in this chart's filters, or set a default bank account on {0}, to see its balance.”.format(company) · validation helper — translated “Account {0} does not exists in the dashboard chart {1}”.format(account, get\_link\_to\_form(“Dashboard Chart”, chart\_name)).

**Local steps**

- If chart\_name.
  - Set chart from Platform.get\_doc(“Dashboard Chart”, chart\_name, check\_permission = “read”).
- Otherwise.
  - Set chart from Platform.\_dict(Platform.parse\_json(chart)).
- Set timespan from chart.timespan.
- If chart.timespan equals “Select Date Range”.
  - Set from\_date from chart.from\_date.
  - Set to\_date from chart.to\_date.
- Set timegrain from chart.time\_interval.
- Set filters from (Platform.parse\_json(filters) or Platform.parse\_json(chart.filters\_json)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(filters) → Platform.parse\_json(chart.filters\_json).
- Set account from filters.get(“account”).
- Set company from filters.get(“company”).
- If not account.
  - If not company.
    - Call the validation error handler Platform.throw(translated “Choose a company in this chart's filters to see its bank balance.”).
  - Call the validation error handler Platform.throw(translated “Choose a bank account in this chart's filters, or set a default bank account on {0}, to see its balance.”.format(company)).
- If (not Platform.db.exists(“Account”, account) and chart\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.exists(“Account”, account) → chart\_name.
  - Call the validation error handler Platform.throw(translated “Account {0} does not exists in the dashboard chart {1}”.format(account, get\_link\_to\_form(“Dashboard Chart”, chart\_name))).
- Evaluate Platform.has\_permission(“Account”, doc = account, throw = true).
- If not to\_date.
  - Set to\_date from nowdate().
- If not from\_date.
  - If timegrain belongs to tuple(“Monthly”, “Quarterly”).
    - Set from\_date from get\_from\_date\_from\_timespan(to\_date, timespan).
- Set dates from get\_dates\_from\_timegrain(from\_date, to\_date, timegrain).
- Set gl\_entries from get\_gl\_entries(account, get\_period\_ending(to\_date, timegrain)).
- Set result from build\_result(account, dates, gl\_entries).
- Return mapping(“labels” → list of formatdate(r at 0.strftime(“%Y-%m-%d”)) for r drawn from result, “datasets” → list(mapping(“name” → account, “values” → list of r at 1 for r drawn from result))).
  - Draw r from result.
  - Draw r from result.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”, doc = account, throw = true) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L15) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L9)

<a id="op-8ab627f6676ec6"></a>
### Build result

`operation_enterprise_accounts_dashboard_chart_source_account_balance_timeline_business_behavior_build_result`

**Inputs** account, dates, gl\_entries.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** result.

**Local steps**

- Set result from list of list(getdate(date), 0.0) for date drawn from dates.
  - Draw date from dates.
- Set root\_type from Platform.get\_cached\_value(“Account”, account, “root\_type”).
- Set date\_index from 0.
- For each entry in gl\_entries.
  - While getdate(entry.posting\_date) &gt; result at date\_index at 0.
    - Update date\_index using + 1.
  - Update result at date\_index at 1 using + (entry.debit − entry.credit).
- If root\_type does not belong to tuple(“Asset”, “Expense”).
  - For each r in result.
    - Set r at 1 from (negative 1 × r at 1).
- If root\_type belongs to tuple(“Asset”, “Liability”, “Equity”).
  - For each tuple(i, r) in enumerate(result).
    - If i &gt; 0.
      - Set r at 1 from (r at 1 + result at (i − 1) at 1).
- Return result.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “root\_type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0003.json#L1133) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L14) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L8)

<a id="op-eb0e252073bd93"></a>
### Get gl entries

`operation_enterprise_accounts_dashboard_chart_source_account_balance_timeline_business_behavior_get_general_ledger_entries`

**Inputs** account, to\_date.

**Record and data access** read “GL Entry” via get\_all.

**Explicit results** Platform.db.get\_all(“GL Entry”, fields = list(“posting\_date”, “debit”, “credit”), filters = list(dict(posting\_date = tuple(“&lt;”, to\_date)), dict(account = tuple(“in”, child\_accounts)), dict(voucher\_type = t ….

**Local steps**

- Set child\_accounts from get\_descendants\_of(“Account”, account, ignore\_permissions = true).
- Evaluate child\_accounts.append(account).
- Return Platform.db.get\_all(“GL Entry”, fields = list(“posting\_date”, “debit”, “credit”), filters = list(dict(posting\_date = tuple(“&lt;”, to\_date)), dict(account = tuple(“in”, child\_accounts)), dict(voucher\_type = t ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0003.json#L1667) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L17) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L11)

<a id="op-75b858977619d5"></a>
### Get dates from timegrain

`operation_enterprise_accounts_dashboard_chart_source_account_balance_timeline_business_behavior_get_dates_from_timegrain`

**Inputs** from\_date, to\_date, timegrain.

**Explicit results** dates.

**Local steps**

- Set days, months, years from 0.
- If “Daily” equals timegrain.
  - Set days from 1.
- Otherwise.
  - If “Weekly” equals timegrain.
    - Set days from 7.
  - Otherwise.
    - If “Monthly” equals timegrain.
      - Set months from 1.
    - Otherwise.
      - If “Quarterly” equals timegrain.
        - Set months from 3.
      - Otherwise.
        - If “Yearly” equals timegrain.
          - Set years from 1.
- Set dates from list(get\_period\_ending(from\_date, timegrain)).
- While getdate(dates at negative 1) &lt; getdate(to\_date).
  - Set date from get\_period\_ending(add\_to\_date(dates at negative 1, years = years, months = months, days = days), timegrain).
  - Evaluate dates.append(date).
- Return dates.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L16) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L10)
