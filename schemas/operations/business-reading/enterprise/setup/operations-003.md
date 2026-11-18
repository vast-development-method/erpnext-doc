# Company and master data · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Company

[Record definition](../../../../data/record-types/company.json)

<a id="op-831a7904f92ff2"></a>
### Update transactions annual history

`operation_enterprise_setup_record_definitions_company_business_behavior_update_transactions_annual_history`

**Inputs** company, commit = false.

**State and service calls** request set\_value on “Company” · commit.

**Local steps**

- Set transactions\_history from get\_all\_transactions\_annual\_history(company).
- Evaluate Platform.db.set\_value(“Company”, company, “transactions\_annual\_history”, json.dumps(transactions\_history)).
- If (commit and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in commit → not Platform.in\_test.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0684.json#L6668) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L317)

<a id="op-409c11cc994fba"></a>
### Cache companies monthly sales history

`operation_enterprise_setup_record_definitions_company_business_behavior_cache_companies_monthly_sales_history`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_list.

**State and service calls** commit.

**Local steps**

- Set refresh\_total\_monthly\_sales from \_should\_refresh\_total\_monthly\_sales().
- Set companies from list of d at “name” for d drawn from Platform.get\_list(“Company”).
  - Draw d from Platform.get\_list(“Company”).
- For each company in companies.
  - Evaluate update\_company\_monthly\_sales(company).
  - Evaluate update\_transactions\_annual\_history(company).
  - If refresh\_total\_monthly\_sales.
    - Evaluate update\_company\_current\_month\_sales(company).
- If not Platform.in\_test.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L276)

<a id="op-f2e66733608b83"></a>
### Should refresh total monthly sales

`operation_enterprise_binding_enterprise_setup_doctype_company_company_should_refresh_total_monthly_sales`

**Inputs** no declared parameters.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Explicit results** Platform.utils.now\_datetime().day equals 1 · frequency equals “Daily”.

**Local steps**

- Set frequency from Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”).
- If frequency equals “Monthly”.
  - Return Platform.utils.now\_datetime().day equals 1.
- Return frequency equals “Daily”.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “sales\_update\_frequency”) · clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L143)

<a id="op-cb97e5e981cb6e"></a>
### Get children

`operation_enterprise_setup_record_definitions_company_business_behavior_get_children`

**Inputs** doctype, parent = no value, company = no value, is\_root = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_list.

**Explicit results** Platform.get\_list(“Company”, filters = filters, fields = list(“name as value”, “is\_group as expandable”)).

**Local steps**

- If (parent is identical to no value or parent equals “All Companies”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent is identical to no value → parent equals “All Companies”.
  - Set parent from empty text.
- Set filters from mapping(“parent\_company” → parent) when parent, otherwise mapping(“parent\_company” → list(“is”, “not set”)).
  - Value choice on parent — true gives mapping(“parent\_company” → parent), false gives mapping(“parent\_company” → list(“is”, “not set”)).
- Return Platform.get\_list(“Company”, filters = filters, fields = list(“name as value”, “is\_group as expandable”)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L310)

<a id="op-54b9d3c303b38d"></a>
### Add node

`operation_enterprise_setup_record_definitions_company_business_behavior_add_runtime_process`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from args via get\_doc.

**State and service calls** call insert on Platform.get\_doc(args).

**Local steps**

- Bind dependencies make\_tree\_args.
- Set args from Platform.form\_dict.
- Set args from make\_tree\_args(expanded names args).
- Set args.doctype from “Company”.
- If args.parent\_company equals “All Companies”.
  - Set args.parent\_company from no value.
- Evaluate Platform.get\_doc(args).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L275)

<a id="op-70e9c5f4175c13"></a>
### Get all transactions annual history

`operation_enterprise_setup_record_definitions_company_business_behavior_get_all_transactions_annual_history`

**Inputs** company.

**Record and data access** execute query text (SELECT, Quotation, Sales, Delivery Note, Sales Invoice).

**Explicit results** out.

**Local steps**

- Set out from mapping().
- Set items from Platform.db.sql(query text (SELECT, Quotation, Sales, Delivery Note, Sales Invoice), company, as\_dict = true).
- For each d in items.
  - Set timestamp from get\_timestamp(d at “transaction\_date”).
  - Evaluate out.update(mapping(timestamp → d at “count”)).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L308)

<a id="op-3fc25b835d3bf8"></a>
### Get timeline data

`operation_enterprise_setup_record_definitions_company_business_behavior_get_timeline_data`

**Inputs** doctype, name.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** json.loads(history) when (history and “{” belongs to history), otherwise mapping() · date\_to\_value\_dict.

**Local steps**

- Set date\_to\_value\_dict from mapping().
- Set history from Platform.get\_cached\_value(“Company”, name, “transactions\_annual\_history”).
- Attempt the following.
  - Set date\_to\_value\_dict from json.loads(history) when (history and “{” belongs to history), otherwise no value.
    - Value choice on (history and “{” belongs to history) — true gives json.loads(history), false gives no value.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in history → “{” belongs to history.
- On failure (ValueError).
  - Set date\_to\_value\_dict from no value.
- If date\_to\_value\_dict is identical to no value.
  - Evaluate update\_transactions\_annual\_history(name, true).
  - Set history from Platform.get\_cached\_value(“Company”, name, “transactions\_annual\_history”).
  - Return json.loads(history) when (history and “{” belongs to history), otherwise mapping().
    - Value choice on (history and “{” belongs to history) — true gives json.loads(history), false gives mapping().
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in history → “{” belongs to history.
- Return date\_to\_value\_dict.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, name, “transactions\_annual\_history”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0685.json#L1175) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L313)

<a id="op-08b7496db731c3"></a>
### Get default company address

`operation_enterprise_setup_record_definitions_company_business_behavior_get_default_company_address`

**Inputs** name, sort\_key = “is\_primary\_address”, existing\_address = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Address).format(sort\_key, “%s”).

**Explicit results** no value · existing\_address · max(out, key = deferred anonymous expression) at 0.

**Local steps**

- If sort\_key does not belong to list(“is\_shipping\_address”, “is\_primary\_address”).
  - Return no value.
- Evaluate Platform.has\_permission(“Company”, ptype = “select”, doc = name, throw = true).
- Set out from Platform.db.sql(query text (SELECT, Address).format(sort\_key, “%s”), name).
- If existing\_address.
  - If existing\_address belongs to list of d at 0 for d drawn from out.
    - Draw d from out.
    - Return existing\_address.
- If out.
  - Return max(out, key = deferred anonymous expression) at 0.
- Otherwise.
  - Return no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, ptype = “select”, doc = name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L311)

<a id="op-3a2411262c154d"></a>
### Get billing shipping address

`operation_enterprise_setup_record_definitions_company_business_behavior_get_billing_shipping_address`

**Inputs** name, billing\_address = no value, shipping\_address = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“primary\_address” → primary\_address, “shipping\_address” → shipping\_address).

**Local steps**

- Set primary\_address from get\_default\_company\_address(name, “is\_primary\_address”, billing\_address).
- Set shipping\_address from get\_default\_company\_address(name, “is\_shipping\_address”, shipping\_address).
- Return mapping(“primary\_address” → primary\_address, “shipping\_address” → shipping\_address).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L309)

<a id="op-c982263f3122d2"></a>
### Create transaction deletion request

`operation_enterprise_setup_record_definitions_company_business_behavior_create_transaction_deletion_request`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “Transaction Deletion Record”, “company” → company) via get\_doc.

**State and service calls** call insert on tdr · call submit on tdr · msgprint with translated “Transaction Deletion Document {0} has been triggered for company {1}”.format(get\_link\_to\_form(“Transaction Deletion Record”, tdr.name), Platform.bold(company)).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Evaluate Platform.has\_permission(“Company”, ptype = “delete”, doc = company, throw = true).
- Bind dependencies is\_deletion\_doc\_running.
- Evaluate is\_deletion\_doc\_running(company).
- Set tdr from Platform.get\_doc(mapping(“doctype” → “Transaction Deletion Record”, “company” → company)).
- Set tdr.flags.ignore\_permissions from 1.
- Evaluate tdr.insert().
- Evaluate tdr.generate\_to\_delete\_list().
- Evaluate tdr.reload().
- Evaluate tdr.submit().
- Evaluate Platform.msgprint(translated “Transaction Deletion Document {0} has been triggered for company {1}”.format(get\_link\_to\_form(“Transaction Deletion Record”, tdr.name), Platform.bold(company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”), Platform.has\_permission(“Company”, ptype = “delete”, doc = company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0685.json#L2308) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L307)

<a id="op-83665edb6848cb"></a>
### Get data

`operation_enterprise_setup_record_definitions_company_company_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“graph” → true, “graph\_method” → “Platform.utils.goal.get\_monthly\_goal\_graph\_data”, “graph\_method\_args” → mapping(“title” → translated “Sales”, “goal\_value\_field” → “monthly\_sales\_target”, “goal\_to ….

**Local steps**

- Return mapping(“graph” → true, “graph\_method” → “Platform.utils.goal.get\_monthly\_goal\_graph\_data”, “graph\_method\_args” → mapping(“title” → translated “Sales”, “goal\_value\_field” → “monthly\_sales\_target”, “goal\_to ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0685.json#L2751) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L318)

## Service · Company setup

<a id="op-b066ef8e0a1497"></a>
### Create fiscal year and company

`operation_enterprise_setup_setup_wizard_operations_company_setup_business_behavior_create_fiscal_year_and_company`

**Inputs** args.

**Record and data access** resolve a document from mapping(“doctype” → “Fiscal Year”, “year” → curr\_fiscal\_year, “year\_start\_date” → args.get(“fy\_start\_date”), “year\_end\_date” → args.get(“fy\_end\_date”)) via get\_doc · resolve a document from mapping(“doctype” → “Company”, “company\_name” → args.get(“company\_name”), “enable\_perpetual\_inventory” → 1, “abbr” → args.get(“company\_abbr”), …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Fiscal Year”, “year” → curr\_fiscal\_year, “year\_start\_date” → args.get(“fy\_start\_date”), “year\_end\_date” → args.get(“fy\_end\_date”))) · call insert on Platform.get\_doc(mapping(“doctype” → “Company”, “company\_name” → args.get(“company\_name”), “enable\_perpetual\_inventory” → 1, “abbr” → args.get(“company\_abbr”), …)).

**Local steps**

- If args.get(“fy\_start\_date”).
  - Set curr\_fiscal\_year from get\_fy\_details(args.get(“fy\_start\_date”), args.get(“fy\_end\_date”)).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Fiscal Year”, “year” → curr\_fiscal\_year, “year\_start\_date” → args.get(“fy\_start\_date”), “year\_end\_date” → args.get(“fy\_end\_date”))).insert().
- If args.get(“company\_name”).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Company”, “company\_name” → args.get(“company\_name”), “enable\_perpetual\_inventory” → 1, “abbr” → args.get(“company\_abbr”), …)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L2955) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1097) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L638)

<a id="op-7937f5782ef5c4"></a>
### Get fy details

`operation_enterprise_setup_setup_wizard_operations_company_setup_business_behavior_get_financial_year_details`

**Inputs** fy\_start\_date, fy\_end\_date.

**Explicit results** fy.

**Local steps**

- Set start\_year from getdate(fy\_start\_date).year.
- If start\_year equals getdate(fy\_end\_date).year.
  - Set fy from cstr(start\_year).
- Otherwise.
  - Set fy from ((cstr(start\_year) + “-”) + cstr((start\_year + 1))).
- Return fy.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L3499) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1098) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L639)

## Record · Currency exchange

[Record definition](../../../../data/record-types/currency_exchange.json)

<a id="op-1fa37c58045350"></a>
### Currency Exchange.autoname

`operation_enterprise_setup_record_definitions_currency_exchange_business_behavior_currency_exchange_autoname`

**Inputs** self.

**Local steps**

- Set purpose from empty text.
- If not self.date.
  - Set self.date from nowdate().
- Set purpose from “Selling-Buying”.
- If (cint(self.for\_buying) equals 0 and cint(self.for\_selling) equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.for\_buying) equals 0 → cint(self.for\_selling) equals 1.
  - Set purpose from “Selling”.
- If (cint(self.for\_buying) equals 1 and cint(self.for\_selling) equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.for\_buying) equals 1 → cint(self.for\_selling) equals 0.
  - Set purpose from “Buying”.
- Set self.name from “{}-{}-{}{}”.format(formatdate(get\_datetime\_str(self.date), “yyyy-MM-dd”), self.from\_currency, self.to\_currency, (“-” + purpose) when purpose, otherwise empty text).
  - Value choice on purpose — true gives (“-” + purpose), false gives empty text.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0686.json#L2956) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L332)

<a id="op-5e64cf6a17d893"></a>
### Currency Exchange.validate

`operation_enterprise_setup_record_definitions_currency_exchange_business_behavior_currency_exchange_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_value(“exchange\_rate”, “&gt;”, 0).
- If self.from\_currency equals self.to\_currency.
  - Evaluate throw(translated “From Currency and To Currency cannot be same”).
- If (not cint(self.for\_buying) and not cint(self.for\_selling)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.for\_buying) → not cint(self.for\_selling).
  - Evaluate throw(translated “Currency Exchange must be applicable for Buying or for Selling.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0686.json#L3349) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L333)

## Record · Customer group

[Record definition](../../../../data/record-types/customer_group.json)

<a id="op-1a17a6496ea0cb"></a>
### Customer Group.validate

`operation_enterprise_setup_record_definitions_customer_group_business_behavior_customer_group_validate`

**Inputs** self.

**Record and data access** read “Customer” via exists · read “Customer Group” via get\_value.

**Explicit failure paths** validation helper with Platform.NameError — translated “A Customer exists with the same name: {0}”.format(self.name) · validation helper — translated “Cannot make Customer Group {0} a group while it has customers”.format(self.name) · validation helper — translated “Credit limit is already defined for the Company {0}”.format(limit.company).

**Local steps**

- Evaluate set\_root\_as\_default\_parent(self).
- If Platform.db.exists(“Customer”, self.name).
  - Call the validation error handler Platform.throw(translated “A Customer exists with the same name: {0}”.format(self.name), Platform.NameError).
- If (self.is\_group and not self.is\_new() and not Platform.db.get\_value(“Customer Group”, self.name, “is\_group”) and Platform.db.exists(“Customer”, mapping(“customer\_group” → self.name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_group → not self.is\_new() → not Platform.db.get\_value(“Customer Group”, self.name, “is\_group”) → Platform.db.exists(“Customer”, mapping(“customer\_group” → self.name)).
  - Call the validation error handler Platform.throw(translated “Cannot make Customer Group {0} a group while it has customers”.format(self.name)).
- Evaluate validate\_party\_account\_rows(self, “Customer”).
- Set companies from set().
- For each limit in self.credit\_limits.
  - If limit.company belongs to companies.
    - Call the validation error handler Platform.throw(translated “Credit limit is already defined for the Company {0}”.format(limit.company)).
  - Evaluate companies.add(limit.company).
- Evaluate self.validate\_currency\_for\_receivable\_and\_advance\_account().
- Evaluate validate\_default\_price\_list\_side(self.default\_price\_list, “selling”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate currency for receivable and advance account](operations-003.md#op-1c06cfaef264a1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L788) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L346)

<a id="op-1c06cfaef264a1"></a>
### Customer Group.validate currency for receivable and advance account

`operation_enterprise_setup_record_definitions_customer_group_business_behavior_customer_group_validate_currency_for_receivable_and_advance_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Both Receivable Account: {0} and Advance Account: {1} must be of same currency for company: {2}”.format(Platform.bold(x.account), Platform.bold(x.advance\_account), Platform.bold(x.company)).

**Local steps**

- For each x in self.accounts.
  - Set receivable\_account\_currency from no value.
  - Set advance\_account\_currency from no value.
  - If x.account.
    - Set receivable\_account\_currency from Platform.get\_cached\_value(“Account”, x.account, “account\_currency”).
  - If x.advance\_account.
    - Set advance\_account\_currency from Platform.get\_cached\_value(“Account”, x.advance\_account, “account\_currency”).
  - If (receivable\_account\_currency and advance\_account\_currency and receivable\_account\_currency differs from advance\_account\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in receivable\_account\_currency → advance\_account\_currency → receivable\_account\_currency differs from advance\_account\_currency.
    - Call the validation error handler Platform.throw(translated “Both Receivable Account: {0} and Advance Account: {1} must be of same currency for company: {2}”.format(Platform.bold(x.account), Platform.bold(x.advance\_account), Platform.bold( ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, x.account, “account\_currency”), Platform.get\_cached\_value(“Account”, x.advance\_account, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L918) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L789) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L347)

<a id="op-7169ffa9865c15"></a>
### Customer Group.before rename

`operation_enterprise_binding_enterprise_setup_doctype_customer_group_customer_group_customergroup_before_rename`

**Inputs** self, olddn, newdn, merge = false.

**Record and data access** read “Customer” via exists.

**Explicit failure paths** validation helper with Platform.NameError — translated “A Customer exists with the same name: {0}”.format(newdn).

**Local steps**

- Evaluate super().before\_rename(olddn, newdn, merge).
- Set newdn from newdn.strip().
- If Platform.db.exists(“Customer”, newdn).
  - Call the validation error handler Platform.throw(translated “A Customer exists with the same name: {0}”.format(newdn), Platform.NameError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L144)

<a id="op-ed199ba1594791"></a>
### Customer Group.on update

`operation_enterprise_setup_record_definitions_customer_group_business_behavior_customer_group_on_update`

**Inputs** self.

**Local steps**

- Evaluate super().on\_update().
- Evaluate self.validate\_one\_root().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L1285) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L345)

<a id="op-ddfc10c2fc32d7"></a>
### Get parent customer groups

`operation_enterprise_setup_record_definitions_customer_group_business_behavior_get_parent_customer_groups`

**Inputs** customer\_group.

**Record and data access** read “Customer Group” via get\_value · read “Customer Group” via get\_all.

**Explicit results** Platform.get\_all(“Customer Group”, filters = list(list(“lft”, “&lt;=”, lft), list(“rgt”, “&gt;=”, rgt)), fields = list(“name”), order\_by = “lft asc”).

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_value(“Customer Group”, customer\_group, list(“lft”, “rgt”)).
- Return Platform.get\_all(“Customer Group”, filters = list(list(“lft”, “&lt;=”, lft), list(“rgt”, “&gt;=”, rgt)), fields = list(“name”), order\_by = “lft asc”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L1359) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L790) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L348)

<a id="op-e8893dea4fe99c"></a>
### On doctype update

`operation_enterprise_setup_record_definitions_customer_group_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Customer Group”.

**Local steps**

- Evaluate Platform.db.add\_index(“Customer Group”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0687.json#L1578) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L791) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L349)

## Service · Dashboard charts

<a id="op-f5b59a8c9e8a37"></a>
### Get company for dashboards

`operation_enterprise_setup_setup_wizard_data_dashboard_charts_business_behavior_get_company_for_dashboards`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_list.

**Explicit results** company · company\_list at 0.name · no value.

**Local steps**

- Set company from Platform.defaults.get\_defaults().company.
- If company.
  - Return company.
- Otherwise.
  - Set company\_list from Platform.get\_list(“Company”).
  - If company\_list.
    - Return company\_list at 0.name.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L375) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1095) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L636)

<a id="op-25756f86407714"></a>
### Get default dashboards

`operation_enterprise_setup_setup_wizard_data_dashboard_charts_business_behavior_get_default_dashboards`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Company” via get\_doc.

**Explicit results** mapping(“Dashboards” → list(mapping(“doctype” → “Dashboard”, “dashboard\_name” → “Accounts”, “charts” → list(mapping(“chart” → “Outgoing Bills (Sales Invoice)”), mapping(“chart” → “Incoming Bills (Purchase  ….

**Local steps**

- Set company from Platform.get\_doc(“Company”, get\_company\_for\_dashboards()).
- Set income\_account from (company.default\_income\_account or get\_account(“Income Account”, company.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company.default\_income\_account → get\_account(“Income Account”, company.name).
- Set expense\_account from (company.default\_expense\_account or get\_account(“Expense Account”, company.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company.default\_expense\_account → get\_account(“Expense Account”, company.name).
- Set bank\_account from (company.default\_bank\_account or get\_account(“Bank”, company.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company.default\_bank\_account → get\_account(“Bank”, company.name).
- Return mapping(“Dashboards” → list(mapping(“doctype” → “Dashboard”, “dashboard\_name” → “Accounts”, “charts” → list(mapping(“chart” → “Outgoing Bills (Sales Invoice)”), mapping(“chart” → “Incoming Bills (Purchase  ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L522) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1096) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L637)

<a id="op-398810aa645f72"></a>
### Get account

`operation_enterprise_setup_setup_wizard_data_dashboard_charts_business_behavior_get_account`

**Inputs** account\_type, company.

**Record and data access** read “Account” via get\_list.

**Explicit results** accounts at 0.name.

**Local steps**

- Set accounts from Platform.get\_list(“Account”, filters = mapping(“account\_type” → account\_type, “company” → company)).
- If accounts.
  - Return accounts at 0.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L2808) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1094) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L635)
