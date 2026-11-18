# Accounting and settlement · operations 111

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subscription plan

[Record definition](../../../../data/record-types/subscription_plan.json)

<a id="op-7c9730cd63baf0"></a>
### Get plan rate

`operation_enterprise_accounts_record_definitions_subscription_plan_business_behavior_get_plan_rate`

**Inputs** plan, quantity = 1, customer = no value, start\_date = no value, end\_date = no value, prorate\_factor = 1, party = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Subscription Plan” via get\_doc · read “Customer” via get\_value · read “Subscription Settings” via get\_single\_value.

**Explicit results** (plan.cost × prorate\_factor) · 0 · (price.price\_list\_rate × prorate\_factor) · cost.

**Local steps**

- Set plan from Platform.get\_doc(“Subscription Plan”, plan).
- Evaluate plan.check\_permission(“read”).
- If plan.price\_determination equals “Fixed Rate”.
  - Return (plan.cost × prorate\_factor).
- Otherwise.
  - If plan.price\_determination equals “Based On Price List”.
    - If customer.
      - Set customer\_group from Platform.db.get\_value(“Customer”, customer, “customer\_group”).
    - Otherwise.
      - Set customer\_group from no value.
    - Set price from get\_price(item\_code = plan.item, price\_list = plan.price\_list, customer\_group = customer\_group, company = no value, …).
    - If not price.
      - Return 0.
    - Otherwise.
      - Return (price.price\_list\_rate × prorate\_factor).
  - Otherwise.
    - If plan.price\_determination equals “Monthly Rate”.
      - Set start\_date from getdate(start\_date).
      - Set end\_date from getdate(end\_date).
      - Set delta from relativedelta.relativedelta(end\_date, start\_date).
      - Set no\_of\_months from (((delta.years × 12) + delta.months) + 1).
      - Set cost from (plan.cost × no\_of\_months).
      - Set prorate from Platform.db.get\_single\_value(“Subscription Settings”, “prorate”).
      - If prorate.
        - Update cost using − (plan.cost × get\_prorate\_factor(start\_date, end\_date)).
      - Return cost.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from plan.check\_permission(“read”) · configured or stored value from Platform.db.get\_single\_value(“Subscription Settings”, “prorate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L250)

<a id="op-bc88f81c67e979"></a>
### Get prorate factor

`operation_enterprise_accounts_record_definitions_subscription_plan_business_behavior_get_prorate_factor`

**Inputs** start\_date, end\_date.

**Explicit results** prorate\_factor.

**Local steps**

- Set total\_days\_to\_skip from date\_diff(start\_date, get\_first\_day(start\_date)).
- Set total\_days\_in\_month from int(get\_last\_day(start\_date).strftime(“%d”)).
- Set prorate\_factor from flt((total\_days\_to\_skip ÷ total\_days\_in\_month)).
- Set total\_days\_to\_skip from date\_diff(get\_last\_day(end\_date), end\_date).
- Set total\_days\_in\_month from int(get\_last\_day(end\_date).strftime(“%d”)).
- Update prorate\_factor using + flt((total\_days\_to\_skip ÷ total\_days\_in\_month)).
- Return prorate\_factor.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0194.json#L4255) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L251)

<a id="op-08c23a1cf9e943"></a>
### Get data

`operation_enterprise_accounts_record_definitions_subscription_plan_subscription_plan_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “subscription\_plan”, “non\_standard\_fieldnames” → mapping(“Payment Request” → “plan”, “Subscription” → “plan”), “transactions” → list(mapping(“label” → translated “References”, “items” ….

**Local steps**

- Return mapping(“fieldname” → “subscription\_plan”, “non\_standard\_fieldnames” → mapping(“Payment Request” → “plan”, “Subscription” → “plan”), “transactions” → list(mapping(“label” → translated “References”, “items” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0194.json#L4558) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1481) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L254)

## Report · Supplier ledger summary

<a id="op-f43ff1e65040c4"></a>
### Execute

`operation_enterprise_accounts_report_supplier_ledger_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** PartyLedgerSummaryReport(filters).run(args).

**Local steps**

- Set args from mapping(“party\_type” → “Supplier”, “naming\_by” → list(“Buying Settings”, “supp\_master\_name”)).
- Return PartyLedgerSummaryReport(filters).run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0281.json#L6176) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L58)

## Record · Tax category

[Record definition](../../../../data/record-types/tax_category.json)

<a id="op-a0fb6bf2fbad62"></a>
### Get data

`operation_enterprise_accounts_record_definitions_tax_category_tax_category_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “tax\_category”, “transactions” → list(mapping(“label” → translated “Pre Sales”, “items” → list(“Quotation”, “Supplier Quotation”)), mapping(“label” → translated “Sales”, “items” → lis ….

**Local steps**

- Return mapping(“fieldname” → “tax\_category”, “transactions” → list(mapping(“label” → translated “Pre Sales”, “items” → list(“Quotation”, “Supplier Quotation”)), mapping(“label” → translated “Sales”, “items” → lis ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0194.json#L5824) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1553) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L315)

## Record · Tax rule

[Record definition](../../../../data/record-types/tax_rule.json)

<a id="op-a3c009988e3819"></a>
### Tax Rule.validate

`operation_enterprise_accounts_record_definitions_tax_rule_business_behavior_tax_rule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_tax\_template().
- Evaluate self.validate\_from\_to\_dates(“from\_date”, “to\_date”).
- Evaluate self.validate\_filters().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate tax template](operations-111.md#op-a507d7ee4f6743), [validate filters](operations-111.md#op-bec861e60696bf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0194.json#L6243) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1558) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L320)

<a id="op-a507d7ee4f6743"></a>
### Tax Rule.validate tax template

`operation_enterprise_accounts_record_definitions_tax_rule_business_behavior_tax_rule_validate_tax_template`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Tax Template is mandatory.”.

**Local steps**

- If self.tax\_type equals “Sales”.
  - Set self.purchase\_tax\_template, self.supplier, self.supplier\_group from no value.
  - If self.customer.
    - Set self.customer\_group from no value.
- Otherwise.
  - Set self.sales\_tax\_template, self.customer, self.customer\_group from no value.
  - If self.supplier.
    - Set self.supplier\_group from no value.
- If not (self.sales\_tax\_template or self.purchase\_tax\_template).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.sales\_tax\_template → self.purchase\_tax\_template.
  - Call the validation error handler Platform.throw(translated “Tax Template is mandatory.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0194.json#L6352) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1560) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L322)

<a id="op-bec861e60696bf"></a>
### Tax Rule.validate filters

`operation_enterprise_accounts_record_definitions_tax_rule_business_behavior_tax_rule_validate_filters`

**Inputs** self.

**Explicit failure paths** validation helper with ConflictingTaxRule — translated “Tax Rule Conflicts with {0}”.format(tax\_rule at 0.name).

**Local steps**

- Set TaxRule from DocType(“Tax Rule”).
- Set filters from mapping(“tax\_type” → self.tax\_type, “customer” → self.customer, “customer\_group” → self.customer\_group, “supplier” → self.supplier, …).
- Set query from nested operand in the contract.qb.from\_(TaxRule).select(TaxRule.name, TaxRule.priority).where(TaxRule.name differs from self.name).
- For each tuple(field, value) in filters.items().
  - Set query from query.where(IfNull(TaxRule at field, empty text) equals cstr(value)).
- If (self.from\_date and self.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → self.to\_date.
  - Set query from query.where(((((nested operand in the contract.from\_date &gt; nested operand in the contract.from\_date bitwise and nested operand in the contract.from\_date &lt; nested operand in the contract.to\_date) bitwise or ….
- Otherwise.
  - If self.from\_date.
    - Set query from query.where(TaxRule.to\_date &gt; self.from\_date).
  - Otherwise.
    - If self.to\_date.
      - Set query from query.where(TaxRule.from\_date &lt; self.to\_date).
- Set tax\_rule from query.run(as\_dict = true).
- If (tax\_rule and tax\_rule at 0.priority equals self.priority).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax\_rule → tax\_rule at 0.priority equals self.priority.
  - Call the validation error handler Platform.throw(translated “Tax Rule Conflicts with {0}”.format(tax\_rule at 0.name), ConflictingTaxRule).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0195.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1559) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L321)

<a id="op-2259869d29c35c"></a>
### Get party details

`operation_enterprise_accounts_record_definitions_tax_rule_business_behavior_get_party_details`

**Inputs** party, party\_type, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_address\_details(expanded address\_names).

**Local steps**

- If party\_type belongs to tuple(“customer”, “supplier”).
  - Set party\_type from party\_type.title().
- If party.
  - Set party from cstr(party).
- Evaluate require\_party\_permission(party\_type, party).
- Set address\_names from get\_party\_address\_names(party, party\_type, args).
- For each address\_name in address\_names.
  - If not address\_name.
    - Continue with the next iteration or loop test.
  - If args.
    - If not Platform.has\_permission(“Address”, “read”, doc = address\_name).
      - Evaluate \_refuse().
  - Otherwise.
    - Evaluate require\_permission(“Address”, address\_name, “read”).
- Return get\_address\_details(expanded address\_names).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Address”, “read”, doc = address\_name).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1554) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L316)

<a id="op-e906b497e4da59"></a>
### Get tax rule party details

`operation_enterprise_binding_enterprise_accounts_doctype_tax_rule_tax_rule_get_tax_rule_party_details`

**Inputs** party, party\_type, args = no value.

**Explicit results** get\_address\_details(expanded get\_party\_address\_names(party, party\_type, args)).

**Local steps**

- Return get\_address\_details(expanded get\_party\_address\_names(party, party\_type, args)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1085)

<a id="op-6aa3cd0828a2ec"></a>
### Get party address names

`operation_enterprise_binding_enterprise_accounts_doctype_tax_rule_tax_rule_get_party_address_names`

**Inputs** party, party\_type, args = no value.

**Declared result** tuple.

**Explicit results** tuple(args.get(“billing\_address”), args.get(“shipping\_address”)) · tuple(get\_default\_address(party\_type, party), get\_default\_address(party\_type, party, “is\_shipping\_address”)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid address”.

**Local steps**

- If args.
  - For each fieldname in tuple(“billing\_address”, “shipping\_address”).
    - If (args.get(fieldname) and not isinstance(args.get(fieldname), str)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(fieldname) → not isinstance(args.get(fieldname), str).
      - Call the validation error handler Platform.throw(translated “Invalid address”, Platform.PermissionError).
  - Return tuple(args.get(“billing\_address”), args.get(“shipping\_address”)).
- Return tuple(get\_default\_address(party\_type, party), get\_default\_address(party\_type, party, “is\_shipping\_address”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1084)

<a id="op-cb9d3fa7e5f8c8"></a>
### Get address details

`operation_enterprise_binding_enterprise_accounts_doctype_tax_rule_tax_rule_get_address_details`

**Inputs** billing\_address\_name = no value, shipping\_address\_name = no value.

**Declared result** dict.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- If billing\_address\_name.
  - Evaluate out.update(get\_address\_fields(billing\_address\_name, “billing”)).
- If shipping\_address\_name.
  - Evaluate out.update(get\_address\_fields(shipping\_address\_name, “shipping”)).
- Return out.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1082)

<a id="op-380acc47e02087"></a>
### Get address fields

`operation_enterprise_binding_enterprise_accounts_doctype_tax_rule_tax_rule_get_address_fields`

**Inputs** address\_name, prefix.

**Declared result** dict.

**Record and data access** resolve a document from “Address” via get\_doc.

**Explicit results** mapping(formatted text {prefix}\_city → address.city, formatted text {prefix}\_county → address.county, formatted text {prefix}\_state → address.state, formatted text {prefix}\_zipcode → address.pincode, …).

**Local steps**

- Set address from Platform.get\_doc(“Address”, address\_name).
- Return mapping(formatted text {prefix}\_city → address.city, formatted text {prefix}\_county → address.county, formatted text {prefix}\_state → address.state, formatted text {prefix}\_zipcode → address.pincode, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1083)

<a id="op-2ff698e62046c4"></a>
### Get tax template

`operation_enterprise_accounts_record_definitions_tax_rule_business_behavior_get_tax_template`

**Inputs** posting\_date, args.

**Record and data access** read doctype via get\_value.

**Explicit results** no value · tax\_template.

**Local steps**

- Set args from Platform.\_dict(args).
- Set TaxRule from DocType(“Tax Rule”).
- Set query from Platform.qb.from\_(TaxRule).select(“\*”).
- If posting\_date.
  - Set query from query.where(((TaxRule.from\_date.isnull() bitwise or TaxRule.from\_date ≤ posting\_date) bitwise and (TaxRule.to\_date.isnull() bitwise or TaxRule.to\_date ≥ posting\_date))).
- Otherwise.
  - Set query from query.where((TaxRule.from\_date.isnull() bitwise and TaxRule.to\_date.isnull())).
- Bind local operation get\_group\_ancestors for subsequent calls.
- Set group\_fields from mapping(“customer\_group” → tuple(“Customer Group”, get\_parent\_customer\_groups), “supplier\_group” → tuple(“Supplier Group”, get\_parent\_supplier\_groups)).
- Evaluate args.setdefault(“tax\_category”, empty text).
- For each tuple(key, value) in args.items().
  - If key equals “use\_for\_shopping\_cart”.
    - Set query from query.where(TaxRule.use\_for\_shopping\_cart equals value).
  - Otherwise.
    - If key equals “tax\_category”.
      - Set query from query.where(IfNull(TaxRule.tax\_category, empty text) equals (value or empty text)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.
    - Otherwise.
      - If key belongs to group\_fields.
        - Set tuple(doctype, get\_parents) from group\_fields at key.
        - Set query from query.where(IfNull(TaxRule at key, empty text).isin(get\_group\_ancestors(doctype, get\_parents, value))).
      - Otherwise.
        - Set query from query.where(IfNull(TaxRule at key, empty text).isin(list(empty text, (value or empty text)))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.
- Set tax\_rule from query.run(as\_dict = true).
- If not tax\_rule.
  - Return no value.
- For each rule in tax\_rule.
  - Set rule.no\_of\_keys\_matched from 0.
  - For each key in args.
    - If rule.get(key).
      - Update rule.no\_of\_keys\_matched using + 1.
- Bind local operation cmp for subsequent calls.
- Set rule from sorted(tax\_rule, key = functools.cmp\_to\_key(deferred anonymous expression)) at 0.
- Set tax\_template from (rule.sales\_tax\_template or rule.purchase\_tax\_template).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rule.sales\_tax\_template → rule.purchase\_tax\_template.
- Set doctype from formatted text {rule.tax\_type} Taxes and Charges Template.
- If Platform.db.get\_value(doctype, tax\_template, “disabled”) equals 1.
  - Return no value.
- Return tax\_template.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0195.json#L2039) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1555) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L317)

<a id="op-3368651eb43c64"></a>
### Get tax template.get group ancestors

`operation_enterprise_accounts_record_definitions_tax_rule_business_behavior_get_tax_template_get_group_ancestors`

**Inputs** doctype, get\_parents, value.

**Explicit results** (list(empty text) + list of d.name for d drawn from get\_parents(value)).

**Local steps**

- If not value.
  - Set value from get\_root\_of(doctype).
- Return (list(empty text) + list of d.name for d drawn from get\_parents(value)).
  - Draw d from get\_parents(value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0195.json#L3540) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1557) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L319)

<a id="op-81af297e256ae3"></a>
### Get tax template.cmp

`operation_enterprise_accounts_record_definitions_tax_rule_business_behavior_get_tax_template_compensatory`

**Inputs** a, b.

**Explicit results** (int(a &gt; b) − int(a &lt; b)).

**Local steps**

- Return (int(a &gt; b) − int(a &lt; b)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0195.json#L3683) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1556) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L318)

## Record · Tax withholding category

[Record definition](../../../../data/record-types/tax_withholding_category.json)

<a id="op-a967337e462025"></a>
### Tax Withholding Category.validate

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_category_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().
- Evaluate self.validate\_companies\_and\_accounts().
- Evaluate self.validate\_thresholds().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-111.md#op-db66ca0acd2d7c), [validate companies and accounts](operations-111.md#op-998d37c19165a0), [validate thresholds](operations-111.md#op-41f2ca9c719338).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L494) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L344)

<a id="op-db66ca0acd2d7c"></a>
### Tax Withholding Category.validate dates

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_category_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: From Date cannot be before To Date”.format(d.idx) · validation helper — translated “Row #{0}: Dates overlapping with other row in group {1}”.format(d.idx, (group or “Default”)).

**Local steps**

- Set group\_rates from defaultdict(list).
- For each d in self.get(“rates”).
  - If getdate(d.from\_date) ≥ getdate(d.to\_date).
    - Call the validation error handler Platform.throw(translated “Row #{0}: From Date cannot be before To Date”.format(d.idx)).
  - Evaluate group\_rates at cstr(d.tax\_withholding\_group).append(d).
- For each tuple(group, rates) in group\_rates.items().
  - Set rates from sorted(rates, key = deferred anonymous expression).
  - Set last\_to\_date from no value.
  - For each d in rates.
    - If (last\_to\_date and getdate(d.from\_date) &lt; getdate(last\_to\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_to\_date → getdate(d.from\_date) &lt; getdate(last\_to\_date).
      - Call the validation error handler Platform.throw(translated “Row #{0}: Dates overlapping with other row in group {1}”.format(d.idx, (group or “Default”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in group → “Default”.
    - Set last\_to\_date from d.to\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L585) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L346)

<a id="op-998d37c19165a0"></a>
### Tax Withholding Category.validate companies and accounts

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_category_validate_companies_and_accounts`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Company {0} added multiple times”.format(Platform.bold(d.get(“company”))) · validation helper — translated “Account {0} added multiple times”.format(Platform.bold(d.get(“account”))).

**Local steps**

- Set existing\_accounts from set().
- Set companies from set().
- For each d in self.get(“accounts”).
  - If d.get(“company”) belongs to companies.
    - Call the validation error handler Platform.throw(translated “Company {0} added multiple times”.format(Platform.bold(d.get(“company”)))).
  - Evaluate companies.add(d.get(“company”)).
  - If d.get(“account”) belongs to existing\_accounts.
    - Call the validation error handler Platform.throw(translated “Account {0} added multiple times”.format(Platform.bold(d.get(“account”)))).
  - Evaluate validate\_account\_head(d.idx, d.get(“account”), d.get(“company”)).
  - Evaluate existing\_accounts.add(d.get(“account”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L1121) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L345)

<a id="op-41f2ca9c719338"></a>
### Tax Withholding Category.validate thresholds

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_category_validate_thresholds`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Cumulative threshold cannot be less than Single Transaction threshold”.format(d.idx).

**Local steps**

- For each d in self.get(“rates”).
  - If (d.cumulative\_threshold and d.single\_threshold and d.cumulative\_threshold &lt; d.single\_threshold).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.cumulative\_threshold → d.single\_threshold → d.cumulative\_threshold &lt; d.single\_threshold.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Cumulative threshold cannot be less than Single Transaction threshold”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L1656) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L347)

<a id="op-9e0bee8474b257"></a>
### Tax Withholding Category.get applicable tax row

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_category_get_applicable_tax_row`

**Inputs** self, posting\_date, tax\_withholding\_group.

**Explicit results** row.

**Explicit failure paths** validation helper — translated “No Tax Withholding data found for the current posting date.”.

**Local steps**

- For each row in self.rates.
  - If (getdate(row.from\_date) ≤ getdate(posting\_date) ≤ getdate(row.to\_date) and cstr(row.tax\_withholding\_group) equals cstr(tax\_withholding\_group)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(row.from\_date) ≤ getdate(posting\_date) ≤ getdate(row.to\_date) → cstr(row.tax\_withholding\_group) equals cstr(tax\_withholding\_group).
    - Compare adjacent operands in order, stopping at the first false comparison in getdate(row.from\_date) ≤ getdate(posting\_date) ≤ getdate(row.to\_date).
    - Return row.
- Call the validation error handler Platform.throw(translated “No Tax Withholding data found for the current posting date.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L1837) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L342)

<a id="op-88cef791d16963"></a>
### Tax Withholding Category.get company account

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_category_get_company_account`

**Inputs** self, company.

**Explicit results** row.account.

**Explicit failure paths** validation helper — translated “No Tax withholding account set for Company {0} in Tax Withholding Category {1}.”.format(Platform.bold(company), Platform.bold(self.name)).

**Local steps**

- For each row in self.accounts.
  - If company equals row.company.
    - Return row.account.
- Call the validation error handler Platform.throw(translated “No Tax withholding account set for Company {0} in Tax Withholding Category {1}.”.format(Platform.bold(company), Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L2077) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L343)

<a id="op-45a56375fe28fd"></a>
### Tax Withholding Details.initialize

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_details_initialize`

**Inputs** self, tax\_withholding\_categories, tax\_withholding\_group, posting\_date, party\_type, party, company.

**Local steps**

- Set self.tax\_withholding\_categories from tax\_withholding\_categories.
- Set self.tax\_withholding\_group from tax\_withholding\_group.
- Set self.posting\_date from posting\_date.
- Set self.party\_type from party\_type.
- Set self.party from party.
- Set self.company from company.
- Set self.tax\_id from get\_tax\_id\_for\_party(self.party\_type, self.party).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L2272) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L352)

<a id="op-8ace3b720ab893"></a>
### Tax Withholding Details.get

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_details_get`

**Inputs** self.

**Declared result** list.

**Record and data access** resolve a document from “Tax Withholding Category” via get\_cached\_doc.

**Explicit results** category\_details.

**Local steps**

- Set category\_details from Platform.\_dict().
- If not self.tax\_withholding\_categories.
  - Return category\_details.
- Set ldc\_details from self.get\_ldc\_details().
- For each category\_name in self.tax\_withholding\_categories.
  - Set doc from Platform.get\_cached\_doc(“Tax Withholding Category”, category\_name).
  - Set row from doc.get\_applicable\_tax\_row(self.posting\_date, self.tax\_withholding\_group).
  - Set account\_head from doc.get\_company\_account(self.company).
  - Set category\_detail from Platform.\_dict(name = category\_name, description = doc.category\_name, account\_head = account\_head, tax\_rate = row.tax\_withholding\_rate, …).
  - If ldc\_detail bound to ldc\_details.get(category\_name).
    - Evaluate category\_detail.update(ldc\_detail).
  - Set category\_details at category\_name from category\_detail.
- Return category\_details.

**Methods declared on this owner** [get ldc details](operations-112.md#op-2b03c88b2916af).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Tax Withholding Category”, category\_name).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L2538) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L348)
