# Company and master data · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales person

[Record definition](../../../../data/record-types/sales_person.json)

<a id="op-c080dc2e5d0595"></a>
### Sales Person.get email id

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_sales_person_get_email_identifier`

**Inputs** self.

**Record and data access** read “Employee” via get\_value · read “User” via get\_value.

**Explicit results** (Platform.db.get\_value(“User”, user, “email”) or user).

**Explicit failure paths** validation helper — translated “User ID not set for Employee {0}”.format(self.employee).

**Local steps**

- If self.employee.
  - Set user from Platform.db.get\_value(“Employee”, self.employee, “user\_id”).
  - If not user.
    - Call the validation error handler Platform.throw(translated “User ID not set for Employee {0}”.format(self.employee)).
  - Otherwise.
    - Return (Platform.db.get\_value(“User”, user, “email”) or user).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“User”, user, “email”) → user.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L4512) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L531)

<a id="op-a75640ee58865b"></a>
### Sales Person.validate employee id

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_sales_person_validate_employee_identifier`

**Inputs** self.

**Record and data access** read “Sales Person” via get\_value.

**Explicit failure paths** validation helper — translated “Another Sales Person {0} exists with the same Employee id”.format(sales\_person).

**Local steps**

- If self.employee.
  - Set sales\_person from Platform.db.get\_value(“Sales Person”, mapping(“employee” → self.employee)).
  - If (sales\_person and sales\_person differs from self.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_person → sales\_person differs from self.name.
    - Call the validation error handler Platform.throw(translated “Another Sales Person {0} exists with the same Employee id”.format(sales\_person)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L4741) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L988) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L536)

<a id="op-cf1b99ae8c6a87"></a>
### Get commission rate

`operation_enterprise_binding_enterprise_setup_doctype_sales_person_sales_person_get_commission_rate`

**Inputs** sales\_person.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Record and data access** resolve a document from “Sales Person” via get\_doc.

**Explicit results** flt(person.commission\_rate).

**Local steps**

- Set person from Platform.get\_doc(“Sales Person”, sales\_person).
- Evaluate person.check\_permission(“select”).
- Return flt(person.commission\_rate).

**Values supplied outside this operation** effective access from person.check\_permission(“select”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L164)

<a id="op-2bfbc05ee1920d"></a>
### On doctype update

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Sales Person”.

**Local steps**

- Evaluate Platform.db.add\_index(“Sales Person”, list(“lft”, “rgt”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L4943) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L530)

<a id="op-11ccc241284c67"></a>
### Get timeline data

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_get_timeline_data`

**Inputs** doctype, name.

**Declared result** dict at tuple(int, int).

**Explicit results** merged\_activities.

**Local steps**

- Bind local operation \_fetch\_activity for subsequent calls.
- Set sales\_order\_activity from \_fetch\_activity(“Sales Order”, “transaction\_date”).
- Set sales\_invoice\_activity from \_fetch\_activity(“Sales Invoice”, “posting\_date”).
- Set delivery\_note\_activity from \_fetch\_activity(“Delivery Note”, “posting\_date”).
- Set merged\_activities from defaultdict(int).
- For each tuple(ts, count) in chain(sales\_order\_activity.items(), sales\_invoice\_activity.items(), delivery\_note\_activity.items()).
  - Update merged\_activities at ts using + count.
- Return merged\_activities.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L980) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L528)

<a id="op-d24cb2b128bd0c"></a>
### Get timeline data.fetch activity

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_get_timeline_data_fetch_activity`

**Inputs** doctype, date\_field.

**Explicit results** dict(nested operand in the contract.where(nested operand in the contract &gt; nested operand in the contract).groupby(transaction at date\_field).run()).

**Local steps**

- Set sales\_team from Platform.qb.DocType(“Sales Team”).
- Set transaction from Platform.qb.DocType(doctype).
- Return dict(nested operand in the contract.where(nested operand in the contract &gt; nested operand in the contract).groupby(transaction at date\_field).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L981) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L529)

<a id="op-895265d9b62a85"></a>
### Get data

`operation_enterprise_setup_record_definitions_sales_person_sales_person_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“heatmap” → true, “heatmap\_message” → translated “This is based on transactions against this Sales Person. See timeline below for details”, “fieldname” → “sales\_person”, “transactions” → list(mappi ….

**Local steps**

- Return mapping(“heatmap” → true, “heatmap\_message” → translated “This is based on transactions against this Sales Person. See timeline below for details”, “fieldname” → “sales\_person”, “transactions” → list(mappi ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L6114) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L990) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L538)

## Service · Setup wizard

<a id="op-f659fc63e35fd8"></a>
### Get setup stages

`operation_enterprise_setup_setup_wizard_business_behavior_get_setup_stages`

**Inputs** args = no value.

**Explicit results** stages.

**Local steps**

- Set stages from list(mapping(“status” → translated “Setting up the basics”, “fail\_msg” → translated “We couldn't set up the basics”, “tasks” → list(mapping(“fn” → stage\_fixtures, “args” → args, “fail\_msg” → translated “We ….
- Return stages.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1088) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L630)

<a id="op-07a41835dadd6b"></a>
### Capture user persona

`operation_enterprise_setup_setup_wizard_business_behavior_capture_user_persona`

**Inputs** args.

**Explicit results** no value.

**Local steps**

- If not args.
  - Return no value.
- Evaluate capture(“user\_persona\_submitted”, “Enterprise”, properties = mapping(“implementing\_for” → args.get(“persona\_implementing\_for”), “company\_size” → args.get(“persona\_company\_size”), “industry” → args.get(“per ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L4199) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1087) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L629)

<a id="op-b1ce7544093637"></a>
### Stage fixtures

`operation_enterprise_setup_setup_wizard_business_behavior_stage_fixtures`

**Inputs** args.

**Local steps**

- Evaluate fixtures.install(args.get(“country”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L4618) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1093) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L634)

<a id="op-4b57b3e03ff52a"></a>
### Setup company

`operation_enterprise_setup_setup_wizard_business_behavior_setup_company`

**Inputs** args.

**Local steps**

- Evaluate fixtures.install\_company(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L4696) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1089) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L631)

<a id="op-2d019e1236e3d5"></a>
### Setup defaults

`operation_enterprise_setup_setup_wizard_business_behavior_setup_defaults`

**Inputs** args.

**Local steps**

- Evaluate fixtures.install\_defaults(Platform.\_dict(args)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L4752) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1091) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L633)

<a id="op-57c1d944e0c18e"></a>
### Setup complete

`operation_enterprise_setup_setup_wizard_business_behavior_setup_complete`

**Inputs** args = no value.

**Local steps**

- Evaluate stage\_fixtures(args).
- Evaluate setup\_company(args).
- Evaluate setup\_defaults(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L4899) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1090) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L632)

## Record · Supplier group

[Record definition](../../../../data/record-types/supplier_group.json)

<a id="op-c6e882299f4209"></a>
### Supplier Group.validate

`operation_enterprise_setup_record_definitions_supplier_group_business_behavior_supplier_group_validate`

**Inputs** self.

**Local steps**

- Evaluate set\_root\_as\_default\_parent(self).
- Evaluate validate\_party\_account\_rows(self, “Supplier”).
- Evaluate self.validate\_currency\_for\_payable\_and\_advance\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate currency for payable and advance account](operations-013.md#op-a0b8333c8a6878).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L542)

<a id="op-a0b8333c8a6878"></a>
### Supplier Group.validate currency for payable and advance account

`operation_enterprise_setup_record_definitions_supplier_group_business_behavior_supplier_group_validate_currency_for_payable_and_advance_account`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Both Payable Account: {0} and Advance Account: {1} must be of same currency for company: {2}”.format(Platform.bold(x.account), Platform.bold(x.advance\_account), Platform.bold(x.company)).

**Local steps**

- For each x in self.accounts.
  - Set payable\_account\_currency from no value.
  - Set advance\_account\_currency from no value.
  - If x.account.
    - Set payable\_account\_currency from Platform.get\_cached\_value(“Account”, x.account, “account\_currency”).
  - If x.advance\_account.
    - Set advance\_account\_currency from Platform.get\_cached\_value(“Account”, x.advance\_account, “account\_currency”).
  - If (payable\_account\_currency and advance\_account\_currency and payable\_account\_currency differs from advance\_account\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in payable\_account\_currency → advance\_account\_currency → payable\_account\_currency differs from advance\_account\_currency.
    - Call the validation error handler Platform.throw(translated “Both Payable Account: {0} and Advance Account: {1} must be of same currency for company: {2}”.format(Platform.bold(x.account), Platform.bold(x.advance\_account), Platform.bold(x.company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, x.account, “account\_currency”), Platform.get\_cached\_value(“Account”, x.advance\_account, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L6397) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L543)

<a id="op-1253f5953292c1"></a>
### Supplier Group.on update

`operation_enterprise_setup_record_definitions_supplier_group_business_behavior_supplier_group_on_update`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.on\_update(self).
- Evaluate self.validate\_one\_root().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L6764) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L993) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L541)

<a id="op-9bd71d6d0deac0"></a>
### Supplier Group.on trash

`operation_enterprise_setup_record_definitions_supplier_group_business_behavior_supplier_group_on_trash`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.validate\_if\_child\_exists(self).
- Evaluate Platform.utils.nestedset.update\_nsm(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L6836) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L992) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L540)

<a id="op-4064b4c0733b9b"></a>
### Get parent supplier groups

`operation_enterprise_setup_record_definitions_supplier_group_business_behavior_get_parent_supplier_groups`

**Inputs** supplier\_group.

**Record and data access** read “Supplier Group” via get\_value · read “Supplier Group” via get\_all.

**Explicit results** Platform.get\_all(“Supplier Group”, filters = list(list(“lft”, “&lt;=”, lft), list(“rgt”, “&gt;=”, rgt)), fields = list(“name”), order\_by = “lft asc”).

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_value(“Supplier Group”, supplier\_group, list(“lft”, “rgt”)).
- Return Platform.get\_all(“Supplier Group”, filters = list(list(“lft”, “&lt;=”, lft), list(“rgt”, “&gt;=”, rgt)), fields = list(“name”), order\_by = “lft asc”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0696.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L991) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L539)

## Record · Target detail

[Record definition](../../../../data/record-types/target_detail.json)

<a id="op-638811f4f91efa"></a>
### Validate targets

`operation_enterprise_binding_enterprise_setup_doctype_target_detail_target_detail_validate_targets`

**Inputs** targets.

**Explicit failure paths** validation helper — translated “Row {0}: Target Qty and Target Amount cannot be negative”.format(target.idx) · validation helper — translated “Row {0}: A target already exists for this fiscal year and item group.”.format(target.idx).

**Local steps**

- Set seen from set().
- For each target in (targets or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in targets → list().
  - If (flt(target.target\_qty) &lt; 0 or flt(target.target\_amount) &lt; 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(target.target\_qty) &lt; 0 → flt(target.target\_amount) &lt; 0.
    - Call the validation error handler Platform.throw(translated “Row {0}: Target Qty and Target Amount cannot be negative”.format(target.idx)).
  - Set key from tuple(target.fiscal\_year, (target.item\_group or no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in target.item\_group → no value.
  - If key belongs to seen.
    - Call the validation error handler Platform.throw(translated “Row {0}: A target already exists for this fiscal year and item group.”.format(target.idx)).
  - Evaluate seen.add(key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L165)

## Service · Taxes setup

<a id="op-77f94b01ea4ab5"></a>
### Setup taxes and charges

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_setup_taxes_and_charges`

**Inputs** company\_name, country.

**Record and data access** read “Company” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Company {} does not exist yet. Taxes setup aborted.”.format(company\_name).

**Local steps**

- If not Platform.db.exists(“Company”, company\_name).
  - Call the validation error handler Platform.throw(translated “Company {} does not exist yet. Taxes setup aborted.”.format(company\_name)).
- Set file\_path from os.path.join(os.path.dirname(\_\_file\_\_), “..”, “data”, “country\_wise\_tax.json”).
- Within open(file\_path) bound as json\_file.
  - Set tax\_data from json.load(json\_file).
- Set country\_wise\_tax from tax\_data.get(country).
- If not country\_wise\_tax.
  - Return no value.
- If “chart\_of\_accounts” does not belong to country\_wise\_tax.
  - Set country\_wise\_tax from simple\_to\_detailed(country\_wise\_tax).
- Evaluate from\_detailed\_data(company\_name, country\_wise\_tax).
- Evaluate update\_regional\_tax\_settings(country, company\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L669)

<a id="op-28f63a6ad885c1"></a>
### Simple to detailed

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_simple_to_detailed`

**Inputs** templates.

**Explicit results** mapping(“chart\_of\_accounts” → mapping(“\*” → mapping(“item\_tax\_templates” → list of mapping(“title” → title, “taxes” → list(mapping(nested operand in the contract → nested operand in the contract))) for tup ….

**Local steps**

- Return mapping(“chart\_of\_accounts” → mapping(“\*” → mapping(“item\_tax\_templates” → list of mapping(“title” → title, “taxes” → list(mapping(nested operand in the contract → nested operand in the contract))) for tup ….
  - Draw tuple(title, data) from templates.items().
  - Draw tuple(title, data) from templates.items().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L5577) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L670)

<a id="op-715ed24289f6b3"></a>
### From detailed data

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_from_detailed_data`

**Inputs** company\_name, data.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set charts\_company\_name from company\_name.
- If Platform.db.get\_value(“Company”, company\_name, “create\_chart\_of\_accounts\_based\_on”) equals “Existing Company”.
  - Set charts\_company\_name from Platform.db.get\_value(“Company”, company\_name, “existing\_company”).
- Set coa\_name from Platform.db.get\_value(“Company”, charts\_company\_name, “chart\_of\_accounts”).
- Set coa\_data from data.get(“chart\_of\_accounts”, mapping()).
- Set tax\_templates from (coa\_data.get(coa\_name) or coa\_data.get(“\*”, mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in coa\_data.get(coa\_name) → coa\_data.get(“\*”, mapping()).
- Set tax\_categories from data.get(“tax\_categories”).
- Set sales\_tax\_templates from (tax\_templates.get(“sales\_tax\_templates”) or tax\_templates.get(“\*”, mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_templates.get(“sales\_tax\_templates”) → tax\_templates.get(“\*”, mapping()).
- Set purchase\_tax\_templates from (tax\_templates.get(“purchase\_tax\_templates”) or tax\_templates.get(“\*”, mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_templates.get(“purchase\_tax\_templates”) → tax\_templates.get(“\*”, mapping()).
- Set item\_tax\_templates from (tax\_templates.get(“item\_tax\_templates”) or tax\_templates.get(“\*”, mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_templates.get(“item\_tax\_templates”) → tax\_templates.get(“\*”, mapping()).
- If tax\_categories.
  - For each tax\_category in tax\_categories.
    - Evaluate make\_tax\_category(tax\_category).
- If sales\_tax\_templates.
  - For each template in sales\_tax\_templates.
    - Evaluate make\_taxes\_and\_charges\_template(company\_name, “Sales Taxes and Charges Template”, template).
- If purchase\_tax\_templates.
  - For each template in purchase\_tax\_templates.
    - Evaluate make\_taxes\_and\_charges\_template(company\_name, “Purchase Taxes and Charges Template”, template).
- If item\_tax\_templates.
  - For each template in item\_tax\_templates.
    - Evaluate make\_item\_tax\_template(company\_name, template).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L6039) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L663)

<a id="op-7c6a7b9612f0d4"></a>
### Update regional tax settings

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_update_regional_tax_settings`

**Inputs** country, company.

**Local steps**

- Set path from Platform.get\_app\_path(“Enterprise”, “regional”, Platform.scrub(country)).
- If os.path.exists(path.encode(“utf-8”)).
  - Attempt the following.
    - Set module\_name from formatted text Enterprise.regional.{Platform.scrub(country)}.setup.update\_regional\_tax\_settings.
    - Evaluate Platform.get\_attr(module\_name)(country, company).
  - On failure (tuple(ImportError, AttributeError)).
    - Take no action here.
  - On failure (Exception).
    - Evaluate Platform.log\_error(“Unable to setup regional tax settings”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(module\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L671)

<a id="op-6364fcac44fcea"></a>
### Make taxes and charges template

`operation_enterprise_setup_setup_wizard_operations_taxes_setup_business_behavior_make_taxes_and_charges_template`

**Inputs** company\_name, doctype, template.

**Record and data access** read doctype via exists · read “Company” via get\_value · resolve a document from template via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** no value · doc.

**Local steps**

- Set template at “company” from company\_name.
- Set template at “doctype” from doctype.
- If Platform.db.exists(doctype, mapping(“title” → template.get(“title”), “company” → company\_name)).
  - Return no value.
- For each tax\_row in template.get(“taxes”).
  - Set account\_data from tax\_row.get(“account\_head”).
  - Set tax\_row\_defaults from mapping(“category” → “Total”, “charge\_type” → “On Net Total”, “cost\_center” → Platform.db.get\_value(“Company”, company\_name, “cost\_center”)).
  - If doctype equals “Purchase Taxes and Charges Template”.
    - Set tax\_row\_defaults at “add\_deduct\_tax” from “Add”.
  - If isinstance(account\_data, dict).
    - Set tax\_row\_defaults at “description” from “{} @ {}”.format(account\_data.get(“account\_name”), account\_data.get(“tax\_rate”)).
    - Set tax\_row\_defaults at “rate” from account\_data.get(“tax\_rate”).
    - Set account from get\_or\_create\_account(company\_name, account\_data).
    - Set tax\_row at “account\_head” from account.name.
  - For each tuple(fieldname, default\_value) in tax\_row\_defaults.items().
    - If fieldname does not belong to tax\_row.
      - Set tax\_row at fieldname from default\_value.
- Set doc from Platform.get\_doc(template).
- Set doc.flags.ignore\_links from true.
- Set doc.flags.ignore\_validate from true.
- Set doc.flags.ignore\_mandatory from true.
- Evaluate doc.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L364) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L668)
