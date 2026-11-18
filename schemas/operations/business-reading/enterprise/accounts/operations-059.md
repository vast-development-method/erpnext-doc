# Accounting and settlement · operations 59

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Loyalty program

[Record definition](../../../../data/record-types/loyalty_program.json)

<a id="op-492a573700ad5b"></a>
### Loyalty Program.validate lowest tier

`operation_enterprise_accounts_record_definitions_loyalty_program_business_behavior_loyalty_program_validate_lowest_tier`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The lowest tier must have a minimum spent amount of 0. Customers need to be part of a tier as soon as they a …”.

**Local steps**

- Set tiers from sorted(self.collection\_rules, key = deferred anonymous expression).
- If (tiers and flt(tiers at 0.min\_spent) differs from 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tiers → flt(tiers at 0.min\_spent) differs from 0.
  - Call the validation error handler Platform.throw(translated “The lowest tier must have a minimum spent amount of 0. Customers need to be part of a tier as soon as they a …”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1218)

<a id="op-63c2fea030c8db"></a>
### Get loyalty details

`operation_enterprise_accounts_record_definitions_loyalty_program_business_behavior_get_loyalty_details`

**Inputs** customer, loyalty\_program, expiry\_date = no value, company = no value, include\_expired\_entry = false.

**Explicit results** loyalty\_point\_details at 0 · mapping(“loyalty\_points” → 0, “total\_spent” → 0).

**Local steps**

- If not expiry\_date.
  - Set expiry\_date from today().
- Set LoyaltyPointEntry from Platform.qb.DocType(“Loyalty Point Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“loyalty\_points”), nested operand in the contract.as\_(“total\_spent”)).where(((nested operand in the  ….
- If company.
  - Set query from query.where(LoyaltyPointEntry.company equals company).
- If not include\_expired\_entry.
  - Set query from query.where(LoyaltyPointEntry.expiry\_date ≥ expiry\_date).
- Set loyalty\_point\_details from query.run(as\_dict = true).
- If loyalty\_point\_details.
  - Return loyalty\_point\_details at 0.
- Otherwise.
  - Return mapping(“loyalty\_points” → 0, “total\_spent” → 0).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0070.json#L5636) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1213)

<a id="op-a5f36d195792bb"></a>
### Get loyalty program details with points

`operation_enterprise_accounts_record_definitions_loyalty_program_business_behavior_get_loyalty_program_details_with_points`

**Inputs** customer, loyalty\_program = no value, expiry\_date = no value, company = no value, silent = false, include\_expired\_entry = false, current\_transaction\_amount = 0.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Loyalty Program” via get\_doc.

**Explicit results** lp\_details.

**Local steps**

- Evaluate Platform.has\_permission(“Customer”, doc = customer, throw = true).
- Set lp\_details from get\_loyalty\_program\_details(customer, loyalty\_program, company = company, silent = silent).
- Set loyalty\_program from Platform.get\_doc(“Loyalty Program”, loyalty\_program).
- Set loyalty\_details from get\_loyalty\_details(customer, loyalty\_program.name, expiry\_date, company, …).
- Evaluate lp\_details.update(loyalty\_details).
- Set tier\_spent\_level from sorted(list of d.as\_dict() for d drawn from loyalty\_program.collection\_rules, key = deferred anonymous expression).
  - Draw d from loyalty\_program.collection\_rules.
- For each tuple(i, d) in enumerate(tier\_spent\_level).
  - If (i equals 0 or (lp\_details.total\_spent + current\_transaction\_amount) ≥ d.min\_spent).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in i equals 0 → (lp\_details.total\_spent + current\_transaction\_amount) ≥ d.min\_spent.
    - Set lp\_details.tier\_name from d.tier\_name.
    - Set lp\_details.collection\_factor from d.collection\_factor.
  - Otherwise.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return lp\_details.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, doc = customer, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1215)

<a id="op-a62a28aefe8d79"></a>
### Get loyalty program details

`operation_enterprise_accounts_record_definitions_loyalty_program_business_behavior_get_loyalty_program_details`

**Inputs** customer, loyalty\_program = no value, expiry\_date = no value, company = no value, silent = false, include\_expired\_entry = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Customer” via get\_value · read “Company” via get\_all · resolve a document from “Loyalty Program” via get\_doc.

**Explicit results** Platform.\_dict(mapping(“loyalty\_programs” → no value)) · lp\_details.

**Explicit failure paths** validation helper — translated “Customer isn't enrolled in any Loyalty Program”.

**Local steps**

- Evaluate Platform.has\_permission(“Customer”, doc = customer, throw = true).
- Set lp\_details from Platform.\_dict().
- If not loyalty\_program.
  - Set loyalty\_program from Platform.db.get\_value(“Customer”, customer, “loyalty\_program”).
  - If (not loyalty\_program and not silent).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not loyalty\_program → not silent.
    - Call the validation error handler Platform.throw(translated “Customer isn't enrolled in any Loyalty Program”).
  - Otherwise.
    - If (silent and not loyalty\_program).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in silent → not loyalty\_program.
      - Return Platform.\_dict(mapping(“loyalty\_programs” → no value)).
- If not company.
  - Set company from (Platform.db.get\_default(“company”) or Platform.get\_all(“Company”) at 0.name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(“company”) → Platform.get\_all(“Company”) at 0.name.
- Set loyalty\_program from Platform.get\_doc(“Loyalty Program”, loyalty\_program).
- Evaluate lp\_details.update(mapping(“loyalty\_program” → loyalty\_program.name)).
- Evaluate lp\_details.update(loyalty\_program.as\_dict()).
- Return lp\_details.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, doc = customer, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1214)

<a id="op-fd1b06b3b298df"></a>
### Get redeemption factor

`operation_enterprise_accounts_record_definitions_loyalty_program_business_behavior_get_redeemption_factor`

**Inputs** loyalty\_program = no value, customer = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Customer” via get\_value · read “Loyalty Program” via get\_value.

**Explicit results** Platform.db.get\_value(“Loyalty Program”, loyalty\_program, “conversion\_factor”).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted” · validation helper — translated “Customer isn't enrolled in any Loyalty Program”.

**Local steps**

- If not (Platform.has\_permission(“Sales Invoice”) or Platform.has\_permission(“POS Invoice”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.has\_permission(“Sales Invoice”) → Platform.has\_permission(“POS Invoice”).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- If customer.
  - Evaluate Platform.has\_permission(“Customer”, doc = customer, throw = true).
- Set customer\_loyalty\_program from no value.
- If not loyalty\_program.
  - Set customer\_loyalty\_program from Platform.db.get\_value(“Customer”, customer, “loyalty\_program”).
  - Set loyalty\_program from customer\_loyalty\_program.
- If loyalty\_program.
  - Return Platform.db.get\_value(“Loyalty Program”, loyalty\_program, “conversion\_factor”).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Customer isn't enrolled in any Loyalty Program”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Sales Invoice”), Platform.has\_permission(“POS Invoice”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1216)

<a id="op-31f80e4bf7617d"></a>
### Validate loyalty points

`operation_enterprise_accounts_record_definitions_loyalty_program_business_behavior_validate_loyalty_points`

**Inputs** ref\_doc, points\_to\_redeem.

**Record and data access** read “Customer” via get\_value · read “Loyalty Program” via get\_value.

**Explicit results** loyalty\_amount.

**Explicit failure paths** validation helper — translated “The Loyalty Program isn't valid for the selected company” · validation helper — translated “Loyalty Points to redeem must be greater than 0.” · validation helper — translated “You don't have enough Loyalty Points to redeem” · validation helper — translated “You can't redeem Loyalty Points having more value than the Total Amount.”.

**Local steps**

- Set loyalty\_program from no value.
- Set posting\_date from no value.
- If ref\_doc.doctype equals “Sales Invoice”.
  - Set posting\_date from ref\_doc.posting\_date.
- Otherwise.
  - Set posting\_date from today().
- If (hasattr(ref\_doc, “loyalty\_program”) and ref\_doc.loyalty\_program).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(ref\_doc, “loyalty\_program”) → ref\_doc.loyalty\_program.
  - Set loyalty\_program from ref\_doc.loyalty\_program.
- Otherwise.
  - Set loyalty\_program from Platform.db.get\_value(“Customer”, ref\_doc.customer, list(“loyalty\_program”)).
- If (loyalty\_program and Platform.db.get\_value(“Loyalty Program”, loyalty\_program, list(“company”)) differs from ref\_doc.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in loyalty\_program → Platform.db.get\_value(“Loyalty Program”, loyalty\_program, list(“company”)) differs from ref\_doc.company.
  - Call the validation error handler Platform.throw(translated “The Loyalty Program isn't valid for the selected company”).
- If (loyalty\_program and points\_to\_redeem).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in loyalty\_program → points\_to\_redeem.
  - If points\_to\_redeem &lt; 0.
    - Call the validation error handler Platform.throw(translated “Loyalty Points to redeem must be greater than 0.”).
  - Set loyalty\_program\_details from get\_loyalty\_program\_details\_with\_points(ref\_doc.customer, loyalty\_program, posting\_date, ref\_doc.company).
  - If points\_to\_redeem &gt; loyalty\_program\_details.loyalty\_points.
    - Call the validation error handler Platform.throw(translated “You don't have enough Loyalty Points to redeem”).
  - Set loyalty\_amount from flt((points\_to\_redeem × loyalty\_program\_details.conversion\_factor)).
  - Set total\_amount from ref\_doc.grand\_total when ref\_doc.is\_rounded\_total\_disabled(), otherwise ref\_doc.rounded\_total.
    - Value choice on ref\_doc.is\_rounded\_total\_disabled() — true gives ref\_doc.grand\_total, false gives ref\_doc.rounded\_total.
  - If loyalty\_amount &gt; total\_amount.
    - Call the validation error handler Platform.throw(translated “You can't redeem Loyalty Points having more value than the Total Amount.”).
  - Set ref\_doc.loyalty\_amount from loyalty\_amount.
  - If (not ref\_doc.loyalty\_points and ref\_doc.loyalty\_points differs from points\_to\_redeem).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ref\_doc.loyalty\_points → ref\_doc.loyalty\_points differs from points\_to\_redeem.
    - Set ref\_doc.loyalty\_points from points\_to\_redeem.
  - If ref\_doc.doctype equals “Sales Invoice”.
    - Set ref\_doc.loyalty\_program from loyalty\_program.
    - If not ref\_doc.loyalty\_redemption\_account.
      - Set ref\_doc.loyalty\_redemption\_account from loyalty\_program\_details.expense\_account.
    - If not ref\_doc.loyalty\_redemption\_cost\_center.
      - Set ref\_doc.loyalty\_redemption\_cost\_center from loyalty\_program\_details.cost\_center.
  - Otherwise.
    - If ref\_doc.doctype equals “Sales Order”.
      - Return loyalty\_amount.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1219)

<a id="op-e095c13694fa93"></a>
### Get data

`operation_enterprise_accounts_record_definitions_loyalty_program_loyalty_program_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “loyalty\_program”, “transactions” → list(mapping(“items” → list(“Sales Invoice”, “Customer”)))).

**Local steps**

- Return mapping(“fieldname” → “loyalty\_program”, “transactions” → list(mapping(“items” → list(“Sales Invoice”, “Customer”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0071.json#L1209) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1220)

## Record · Mode of payment

[Record definition](../../../../data/record-types/mode_of_payment.json)

<a id="op-5e8dd3c79475bf"></a>
### Modeof Payment.validate

`operation_enterprise_accounts_record_definitions_mode_of_payment_business_behavior_modeof_payment_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_accounts().
- Evaluate self.validate\_repeating\_companies().
- Evaluate self.validate\_pos\_mode\_of\_payment().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate accounts](operations-059.md#op-8a3bb13d093a4f), [validate repeating companies](operations-059.md#op-3332761f96c203), [validate pos mode of payment](operations-059.md#op-c72e82f489171d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0071.json#L7122) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1231)

<a id="op-3332761f96c203"></a>
### Modeof Payment.validate repeating companies

`operation_enterprise_accounts_record_definitions_mode_of_payment_business_behavior_modeof_payment_validate_repeating_companies`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Same Company is entered more than once”.

**Local steps**

- Set accounts\_list from list().
- For each entry in self.accounts.
  - Evaluate accounts\_list.append(entry.company).
- If len(accounts\_list) differs from len(set(accounts\_list)).
  - Call the validation error handler Platform.throw(translated “Same Company is entered more than once”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0071.json#L7213) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1234)

<a id="op-8a3bb13d093a4f"></a>
### Modeof Payment.validate accounts

`operation_enterprise_accounts_record_definitions_mode_of_payment_business_behavior_modeof_payment_validate_accounts`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Account {0} does not match with Company {1} in Mode of Account: {2}”.format(entry.default\_account, entry.company, self.name) · validation helper — translated “Row {0}: Account {1} must be a ledger account of type Bank, Cash or Receivable.”.format(entry.idx, Platform.bold(entry.default\_account)) · validation helper — translated “Row {0}: Account {1} is disabled.”.format(entry.idx, Platform.bold(entry.default\_account)).

**Local steps**

- For each entry in self.accounts.
  - Set account from Platform.get\_cached\_value(“Account”, entry.default\_account, list(“company”, “is\_group”, “account\_type”, “disabled”), as\_dict = true).
  - If (not account or account.company differs from entry.company).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not account → account.company differs from entry.company.
    - Call the validation error handler Platform.throw(translated “Account {0} does not match with Company {1} in Mode of Account: {2}”.format(entry.default\_account, entry.company, self.name)).
  - If (account.is\_group or account.account\_type does not belong to tuple(“Bank”, “Cash”, “Receivable”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.is\_group → account.account\_type does not belong to tuple(“Bank”, “Cash”, “Receivable”).
    - Call the validation error handler Platform.throw(translated “Row {0}: Account {1} must be a ledger account of type Bank, Cash or Receivable.”.format(entry.idx, Platform.bold(entry.default\_account))).
  - If account.disabled.
    - Call the validation error handler Platform.throw(translated “Row {0}: Account {1} is disabled.”.format(entry.idx, Platform.bold(entry.default\_account))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, entry.default\_account, list(“company”, “is\_group”, “account\_type”, “disabled”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1232)

<a id="op-c72e82f489171d"></a>
### Modeof Payment.validate pos mode of payment

`operation_enterprise_accounts_record_definitions_mode_of_payment_business_behavior_modeof_payment_validate_point_of_sale_mode_of_payment`

**Inputs** self.

**Record and data access** read “POS Payment Method” via get\_all.

**Explicit failure paths** validation helper — message.

**Local steps**

- If not self.enabled.
  - Set pos\_profiles from Platform.get\_all(“POS Payment Method”, filters = mapping(“parenttype” → “POS Profile”, “mode\_of\_payment” → self.name), pluck = “parent”).
  - If pos\_profiles.
    - Set message from translated “POS Profile {} contains Mode of Payment {}. Please remove them to disable this mode.”.format(Platform.bold(“, ”.join(pos\_profiles)), Platform.bold(str(self.name))).
    - Call the validation error handler Platform.throw(message, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1233)

<a id="op-a9b335e9205ec2"></a>
### Validate enabled mode of payment

`operation_enterprise_binding_enterprise_accounts_doctype_mode_of_payment_mode_of_payment_validate_enabled_mode_of_payment`

**Inputs** mode\_of\_payment.

**Record and data access** read “Mode of Payment” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Mode of Payment {0} is disabled.”.format(Platform.bold(mode\_of\_payment)).

**Local steps**

- If (mode\_of\_payment and not Platform.get\_cached\_value(“Mode of Payment”, mode\_of\_payment, “enabled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in mode\_of\_payment → not Platform.get\_cached\_value(“Mode of Payment”, mode\_of\_payment, “enabled”).
  - Call the validation error handler Platform.throw(translated “Mode of Payment {0} is disabled.”.format(Platform.bold(mode\_of\_payment))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Mode of Payment”, mode\_of\_payment, “enabled”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L823)

## Record · Monthly distribution

[Record definition](../../../../data/record-types/monthly_distribution.json)

<a id="op-23aad0971c493e"></a>
### Monthly Distribution.get months

`operation_enterprise_accounts_record_definitions_monthly_distribution_business_behavior_monthly_distribution_get_months`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set month\_list from list(“January”, “February”, “March”, “April”, …).
- Set idx from 1.
- For each m in month\_list.
  - Set mnth from self.append(“percentages”).
  - Set mnth.month from m.
  - Set mnth.percentage\_allocation from (100.0 ÷ 12).
  - Set mnth.idx from idx.
  - Update idx using + 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L2006) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1244)

<a id="op-71375016cc45a2"></a>
### Monthly Distribution.validate

`operation_enterprise_accounts_record_definitions_monthly_distribution_business_behavior_monthly_distribution_validate`

**Inputs** self.

**Explicit failure paths** validation helper — (translated “Percentage Allocation should be equal to 100%” + formatted text  ({flt(total, 2)}%)).

**Local steps**

- Set total from sum(generator of flt(d.percentage\_allocation) for d drawn from self.get(“percentages”)).
  - Draw d from self.get(“percentages”).
- If flt(total, 2) differs from 100.0.
  - Call the validation error handler Platform.throw((translated “Percentage Allocation should be equal to 100%” + formatted text  ({flt(total, 2)}%))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L2253) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1245)

<a id="op-38b715fcd7a29f"></a>
### Get periodwise distribution data

`operation_enterprise_accounts_record_definitions_monthly_distribution_business_behavior_get_periodwise_distribution_data`

**Inputs** distribution\_id, period\_list, periodicity.

**Record and data access** resolve a document from “Monthly Distribution” via get\_doc.

**Explicit results** period\_dict.

**Local steps**

- Set doc from Platform.get\_doc(“Monthly Distribution”, distribution\_id).
- Set months\_to\_add from mapping(“Yearly” → 12, “Half-Yearly” → 6, “Quarterly” → 3, “Monthly” → 1) at periodicity.
- Set period\_dict from mapping().
- For each d in period\_list.
  - Set period\_dict at d.key from get\_percentage(doc, d.from\_date, months\_to\_add).
- Return period\_dict.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L2484) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1243)

<a id="op-1ce03d40af08d3"></a>
### Get percentage

`operation_enterprise_accounts_record_definitions_monthly_distribution_business_behavior_get_percentage`

**Inputs** doc, start\_date, period.

**Explicit results** percentage.

**Local steps**

- Set percentage from 0.
- Set months from list(start\_date.strftime(“%B”).title()).
- For each r in range(1, period).
  - Evaluate months.append(add\_months(start\_date, r).strftime(“%B”).title()).
- For each d in doc.percentages.
  - If d.month belongs to months.
    - Update percentage using + d.percentage\_allocation.
- Return percentage.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L2718) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1242)

<a id="op-a2ada25a84f187"></a>
### Get data

`operation_enterprise_accounts_record_definitions_monthly_distribution_monthly_distribution_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “monthly\_distribution”, “non\_standard\_fieldnames” → mapping(“Sales Person” → “distribution\_id”, “Territory” → “distribution\_id”, “Sales Partner” → “distribution\_id”), “transactions” → ….

**Local steps**

- Return mapping(“fieldname” → “monthly\_distribution”, “non\_standard\_fieldnames” → mapping(“Sales Person” → “distribution\_id”, “Territory” → “distribution\_id”, “Sales Partner” → “distribution\_id”), “transactions” → ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L2988) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1246)

## Service · Non billed report

<a id="op-c7e45363229b13"></a>
### Get ordered to be billed data

`operation_enterprise_accounts_report_non_billed_report_business_behavior_get_ordered_to_be_billed_data`

**Inputs** args, filters = no value.

**Explicit results** deduct\_order\_billed\_later(query.run(as\_dict = true), order\_billed\_later, precision).

**Local steps**

- Set tuple(doctype, party) from tuple(args.get(“doctype”), args.get(“party”)).
- Set child\_tab from (doctype + “ Item”).
- Set precision from (get\_field\_precision(Platform.get\_meta(child\_tab).get\_field(“billed\_amt”), currency = get\_default\_currency()) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_field\_precision(Platform.get\_meta(child\_tab).get\_field(“billed\_amt”), currency = get\_default\_currency()) → 2.
- Set links from BILLING\_LINKS at doctype.
- Set as\_on\_date from filters.get(“posting\_date”).
- Set later\_billed from get\_billed\_after(links, as\_on\_date).
- Set order\_billed\_later from OrderBillingAsOn(doctype, links, as\_on\_date, precision).get\_billed\_later().
- Set returned from get\_returned\_as\_on(doctype, child\_tab, links, as\_on\_date).
- Set doctype from Platform.qb.DocType(doctype).
- Set child\_doctype from Platform.qb.DocType(child\_tab).
- Set item from Platform.qb.DocType(“Item”).
- Set docname from filters.get(args.get(“reference\_field”), no value).
- Set project\_field from get\_project\_field(doctype, child\_doctype, party).
- Set later\_billed\_amount from IfNull(later\_billed.amount, 0).
- Set has\_order\_billed\_later from child\_doctype.name.isin((list(order\_billed\_later) or list(empty text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list(order\_billed\_later) → list(empty text).
- Set billed\_amount from ((child\_doctype.billed\_amt − later\_billed\_amount) × IfNull(doctype.conversion\_rate, 1)).
- Set returned\_amount from ((child\_doctype.base\_rate × IfNull(returned.qty, 0)) ÷ child\_doctype.conversion\_factor).
- Set query from nested operand in the contract(nested operand in the contract).select(doctype.name, nested operand in the contract.as\_(“date”), doctype at party, doctype at (nested operand in the contract + nested operand ….
- If docname.
  - Set query from query.where(doctype.name equals docname).
- If links.billed\_by\_qty.
  - Set query from exclude\_billed\_in\_full\_by\_qty(query, child\_doctype, returned, links, …).
- Return deduct\_order\_billed\_later(query.run(as\_dict = true), order\_billed\_later, precision).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1124)

<a id="op-8f85a4bd86b112"></a>
### Deduct order billed later

`operation_enterprise_binding_enterprise_accounts_report_non_billed_report_deduct_order_billed_later`

**Inputs** data, order\_billed\_later, precision.

**Declared result** list.

**Explicit results** pending\_rows.

**Local steps**

- Set pending\_rows from list().
- For each row in data.
  - Set detail from row.pop(“detail”).
  - If detail belongs to order\_billed\_later.
    - Set row.billed\_amount from (flt(row.billed\_amount) − order\_billed\_later at detail).
    - Set row.pending\_amount from (flt(row.pending\_amount) + order\_billed\_later at detail).
    - If ((flt(row.amount) − flt(row.billed\_amount, precision)) − flt(row.returned\_amount)) ≤ 0.
      - Continue with the next iteration or loop test.
  - Evaluate pending\_rows.append(row).
- Return pending\_rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1228)

<a id="op-de07919f8703b7"></a>
### Exclude billed in full by qty

`operation_enterprise_binding_enterprise_accounts_report_non_billed_report_exclude_billed_in_full_by_qty`

**Inputs** query, child\_doctype, returned, links, as\_on\_date.

**Declared result** QueryBuilder.

**Explicit results** query.left\_join(billed\_qty).on(billed\_qty.detail equals child\_doctype.name).where(IfNull(billed\_qty.qty, 0) &lt; net\_qty).

**Local steps**

- Set invoice from Platform.qb.DocType(links.invoice).
- Set billed\_qty from get\_billed\_against\_rows(links, “qty”).where(invoice.posting\_date ≤ as\_on\_date).
- Set billed\_qty from billed\_qty.as\_(“billed\_qty”).
- Set net\_qty from (child\_doctype.qty − (IfNull(returned.qty, 0) ÷ child\_doctype.conversion\_factor)).
- Return query.left\_join(billed\_qty).on(billed\_qty.detail equals child\_doctype.name).where(IfNull(billed\_qty.qty, 0) &lt; net\_qty).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1229)

<a id="op-f6bfa4ff1158f9"></a>
### Get billed after

`operation_enterprise_binding_enterprise_accounts_report_non_billed_report_get_billed_after`

**Inputs** links, as\_on\_date.

**Explicit results** get\_billed\_against\_rows(links).where(invoice.posting\_date &gt; as\_on\_date).as\_(“later\_billed”).

**Local steps**

- Set invoice from Platform.qb.DocType(links.invoice).
- Return get\_billed\_against\_rows(links).where(invoice.posting\_date &gt; as\_on\_date).as\_(“later\_billed”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1230)

<a id="op-1346832241a950"></a>
### Get billed against rows

`operation_enterprise_binding_enterprise_accounts_report_non_billed_report_get_billed_against_rows`

**Inputs** links, field = “amount”.

**Declared result** QueryBuilder.

**Explicit results** nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise or nested operand in the contract equals nested operand in ….

**Local steps**

- Set invoice from Platform.qb.DocType(links.invoice).
- Set invoice\_item from Platform.qb.DocType((links.invoice + “ Item”)).
- Return nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise or nested operand in the contract equals nested operand in ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1231)

<a id="op-7905ebfdaf3a01"></a>
### Get returned as on

`operation_enterprise_binding_enterprise_accounts_report_non_billed_report_get_returned_as_on`

**Inputs** doctype, child\_tab, links, as\_on\_date.

**Explicit results** query.as\_(“returned”).

**Local steps**

- Set parent from Platform.qb.DocType(doctype).
- Set child from Platform.qb.DocType(child\_tab).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- If links.rejected\_return\_flag.
  - Set query from query.where(child at links.rejected\_return\_flag equals 0).
- Return query.as\_(“returned”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1232)

<a id="op-81052c3e443d8d"></a>
### Get project field

`operation_enterprise_accounts_report_non_billed_report_business_behavior_get_project_field`

**Inputs** doctype, child\_doctype, party.

**Explicit results** child\_doctype.project · doctype.project.

**Local steps**

- If party equals “supplier”.
  - Return child\_doctype.project.
- Return doctype.project.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0267.json#L1423) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1125)
