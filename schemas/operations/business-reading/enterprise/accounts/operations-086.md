# Accounting and settlement · operations 86

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pricing rule

[Record definition](../../../../data/record-types/pricing_rule.json)

<a id="op-3b91bc20de9b40"></a>
### Get item uoms

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_get_item_units_of_measure`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Item” via get\_list · read “UOM Conversion Detail” via get\_all.

**Explicit results** list() · Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, items), “parenttype” → “Item”, “uom” → tuple(“like”, formatted text {txt}%)), fields = list(“uom”), as\_list = 1, distinct = true).

**Local steps**

- If filters.get(“apply\_on”) equals “Item Code”.
  - Set item\_filters from list(list(“name”, “=”, filters.get(“value”))).
- Otherwise.
  - Set item\_filters from list(list(Platform.scrub(filters.get(“apply\_on”)), “=”, filters.get(“value”))).
- Set items from Platform.get\_list(“Item”, filters = item\_filters, pluck = “name”).
- If not items.
  - Return list().
- Return Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parent” → tuple(“in”, items), “parenttype” → “Item”, “uom” → tuple(“like”, formatted text {txt}%)), fields = list(“uom”), as\_list = 1, distinct = true).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L518) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L700)

<a id="op-308747e1393977"></a>
### Get pricing rules

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_pricing_rules`

**Inputs** args, doc = no value.

**Record and data access** read “Pricing Rule” via count · read “Coupon Code” via get\_cached\_value.

**Explicit results** no value · list() · rules.

**Local steps**

- Set pricing\_rules from list().
- Set values from mapping().
- If not Platform.db.count(“Pricing Rule”, cache = true).
  - Return no value.
- Set coupon\_pricing\_rule from Platform.get\_cached\_value(“Coupon Code”, args.coupon\_code, “pricing\_rule”) when args.get(“coupon\_code”), otherwise no value.
  - Value choice on args.get(“coupon\_code”) — true gives Platform.get\_cached\_value(“Coupon Code”, args.coupon\_code, “pricing\_rule”), false gives no value.
- For each apply\_on in list(“Item Code”, “Item Group”, “Brand”).
  - Set candidates from list of rule for rule drawn from \_get\_pricing\_rules(apply\_on, args, values) where (not rule.coupon\_code\_based or rule.name equals coupon\_pricing\_rule).
    - Draw rule from \_get\_pricing\_rules(apply\_on, args, values), keep a combination only if ((not rule.coupon\_code\_based or rule.name equals coupon\_pricing\_rule)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not rule.coupon\_code\_based → rule.name equals coupon\_pricing\_rule.
  - Evaluate pricing\_rules.extend(filter\_pricing\_rule\_based\_on\_condition(candidates, doc)).
  - If (pricing\_rules and pricing\_rules at 0.has\_priority).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rules → pricing\_rules at 0.has\_priority.
    - Continue with the next iteration or loop test.
  - If (pricing\_rules and not apply\_multiple\_pricing\_rules(pricing\_rules)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rules → not apply\_multiple\_pricing\_rules(pricing\_rules).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set rules from list().
- If not pricing\_rules.
  - Return list().
- If apply\_multiple\_pricing\_rules(pricing\_rules).
  - Set pricing\_rules from sorted\_by\_priority(pricing\_rules, args, doc).
  - For each pricing\_rule in pricing\_rules.
    - If isinstance(pricing\_rule, list).
      - Evaluate rules.extend(pricing\_rule).
    - Otherwise.
      - Evaluate rules.append(pricing\_rule).
- Otherwise.
  - Set pricing\_rule from filter\_pricing\_rules(args, pricing\_rules, doc).
  - If pricing\_rule.
    - Evaluate rules.append(pricing\_rule).
- Return rules.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Coupon Code”, args.coupon\_code, “pricing\_rule”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L772)

<a id="op-67ffc19d3f6d52"></a>
### Sorted by priority

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_sorted_by_priority`

**Inputs** pricing\_rules, args, doc = no value.

**Explicit results** pricing\_rules\_list.

**Local steps**

- Set pricing\_rules\_list from list().
- Set pricing\_rule\_dict from mapping().
- For each pricing\_rule in pricing\_rules.
  - Set pricing\_rule from filter\_pricing\_rules(args, pricing\_rule, doc).
  - If pricing\_rule.
    - If not pricing\_rule.get(“priority”).
      - Set pricing\_rule at “priority” from 1.
    - If pricing\_rule.get(“apply\_multiple\_pricing\_rules”).
      - Evaluate pricing\_rule\_dict.setdefault(cint(pricing\_rule.get(“priority”)), list()).append(pricing\_rule).
- For each key in sorted(pricing\_rule\_dict).
  - Evaluate pricing\_rules\_list.extend(pricing\_rule\_dict.get(key)).
- Return pricing\_rules\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0135.json#L4547) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L781)

<a id="op-5132545c16d06e"></a>
### Filter pricing rule based on condition

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_filter_pricing_rule_based_on_condition`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** pricing\_rules, doc.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L766)

<a id="op-4aeae865eeeb31"></a>
### Get pricing rules

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_pricing_rules_2`

**Inputs** apply\_on, args, values.

**Record and data access** read “Item” via get\_cached\_value · execute query text (SELECT, Pricing Rule).format(child\_doc = child\_doc, apply\_on\_field = apply\_on\_field, item\_conditions = item\_conditions, item\_variant\_condition = item\_variant\_condition, …).

**Explicit results** list() · pricing\_rules.

**Explicit failure paths** validation helper — translated “Invalid Transaction Type”.

**Local steps**

- Set apply\_on\_field from Platform.scrub(apply\_on).
- If not args.get(apply\_on\_field).
  - Return list().
- If args.transaction\_type does not belong to tuple(“buying”, “selling”).
  - Call the validation error handler Platform.throw(translated “Invalid Transaction Type”).
- Set child\_doc from formatted text ′tabPricing Rule {apply\_on}′.
- Set conditions, item\_variant\_condition, item\_conditions from empty text.
- Set values at apply\_on\_field from args.get(apply\_on\_field).
- If apply\_on\_field belongs to list(“item\_code”, “brand”).
  - Set item\_conditions from formatted text {child\_doc}.{apply\_on\_field}= %({apply\_on\_field})s.
  - If apply\_on\_field equals “item\_code”.
    - If args.get(“uom”, no value).
      - Update item\_conditions using + “ and ({child\_doc}.uom={item\_uom} or IFNULL({child\_doc}.uom, '')='')”.format(child\_doc = child\_doc, item\_uom = Platform.db.escape(args.get(“uom”))).
    - If “variant\_of” does not belong to args.
      - Set args.variant\_of from Platform.get\_cached\_value(“Item”, args.item\_code, “variant\_of”).
    - If args.variant\_of.
      - Set item\_variant\_condition from formatted text  or {child\_doc}.item\_code=%(variant\_of)s.
      - Set values at “variant\_of” from args.variant\_of.
- Otherwise.
  - If apply\_on\_field equals “item\_group”.
    - Set item\_conditions from \_get\_tree\_conditions(args, “Item Group”, child\_doc, false).
    - If args.get(“uom”, no value).
      - Update item\_conditions using + “ and ({child\_doc}.uom={item\_uom} or IFNULL({child\_doc}.uom, '')='')”.format(child\_doc = child\_doc, item\_uom = Platform.db.escape(args.get(“uom”))).
- Update conditions using + get\_other\_conditions(conditions, values, args).
- Set warehouse\_conditions from \_get\_tree\_conditions(args, “Warehouse”, “′tabPricing Rule′”).
- If warehouse\_conditions.
  - Set warehouse\_conditions from formatted text  and {warehouse\_conditions}.
- If not args.price\_list.
  - Set args.price\_list from no value.
- Update conditions using + “ and ifnull(′tabPricing Rule′.for\_price\_list, '') in (%(price\_list)s, '')”.
- Set values at “price\_list” from args.get(“price\_list”).
- Set pricing\_rules from (Platform.db.sql(query text (SELECT, Pricing Rule).format(child\_doc = child\_doc, apply\_on\_field = apply\_on\_field, item\_conditions = item\_conditions, item\_variant\_condition = item\_variant\_condition, …), val ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.sql(query text (SELECT, Pricing Rule).format(child\_doc = child\_doc, apply\_on\_field = apply\_on\_field, item\_conditions = item\_conditions, item\_variant\_condition = item\_variant\_condition, …), valu … → list().
- Return pricing\_rules.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, args.item\_code, “variant\_of”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L773)

<a id="op-bb5791662978ce"></a>
### Apply multiple pricing rules

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_apply_multiple_pricing_rules`

**Inputs** pricing\_rules.

**Explicit results** false · true.

**Local steps**

- For each d in pricing\_rules.
  - If not d.apply\_multiple\_pricing\_rules.
    - Return false.
- Return true.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0135.json#L6634) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L581) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L763)

<a id="op-9ad194243f1d91"></a>
### Get tree conditions

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_tree_conditions`

**Inputs** args, parenttype, table, allow\_blank = true.

**Record and data access** read parenttype via get\_value · read parenttype via get\_list.

**Explicit results** Platform.flags.tree\_conditions at key · condition.

**Explicit failure paths** validation helper — translated “Invalid {0}”.format(args.get(field)).

**Local steps**

- Set field from Platform.scrub(parenttype).
- Set condition from empty text.
- If args.get(field).
  - If not Platform.flags.tree\_conditions.
    - Set Platform.flags.tree\_conditions from mapping().
  - Set key from tuple(parenttype, args.get(field)).
  - If key belongs to Platform.flags.tree\_conditions.
    - Return Platform.flags.tree\_conditions at key.
  - Attempt the following.
    - Set tuple(lft, rgt) from Platform.db.get\_value(parenttype, args.get(field), list(“lft”, “rgt”)).
  - On failure (TypeError).
    - Call the validation error handler Platform.throw(translated “Invalid {0}”.format(args.get(field))).
  - Set parent\_groups from Platform.db.sql\_list(query text (SELECT).format(parenttype, “%s”, “%s”), tuple(lft, rgt)).
  - If parenttype belongs to list(“Customer Group”, “Item Group”, “Territory”).
    - Set parent\_field from formatted text parent\_{Platform.scrub(parenttype)}.
    - Set root\_name from Platform.db.get\_list(parenttype, mapping(“is\_group” → 1, parent\_field → tuple(“is”, “not set”)), “name”, as\_list = 1, ignore\_permissions = true).
    - If (root\_name and root\_name at 0 at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_name → root\_name at 0 at 0.
      - Evaluate parent\_groups.append(root\_name at 0 at 0).
  - If parent\_groups.
    - If allow\_blank.
      - Evaluate parent\_groups.append(empty text).
    - Set condition from “ifnull({table}.{field}, '') in ({parent\_groups})”.format(table = table, field = field, parent\_groups = “, ”.join(generator of Platform.db.escape(d) for d drawn from parent\_groups)).
      - Draw d from parent\_groups.
    - Set Platform.flags.tree\_conditions at key from condition.
- Otherwise.
  - If allow\_blank.
    - Set condition from formatted text ifnull({table}.{field}, '') = ''.
- Return condition.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L778)

<a id="op-3b62237cc6ade7"></a>
### Get other conditions

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_other_conditions`

**Inputs** conditions, values, args.

**Record and data access** read args.get(“doctype”) via get\_value.

**Explicit results** conditions.

**Local steps**

- For each field in list(“company”, “customer”, “supplier”, “campaign”, …).
  - Set value from args.get(field).
  - If field equals “campaign”.
    - Set value from (value or args.get(“utm\_campaign”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → args.get(“utm\_campaign”).
  - If value.
    - Update conditions using + formatted text  and ifnull(′tabPricing Rule′.{field}, '') in (%({field})s, '').
    - Set values at field from value.
  - Otherwise.
    - Update conditions using + formatted text  and ifnull(′tabPricing Rule′.{field}, '') = ''.
- For each parenttype in list(“Customer Group”, “Territory”, “Supplier Group”).
  - Set group\_condition from \_get\_tree\_conditions(args, parenttype, “′tabPricing Rule′”).
  - If group\_condition.
    - Update conditions using + (“ and ” + group\_condition).
- Set date from (args.get(“transaction\_date”) or args.get(“posting\_date”) or Platform.get\_value(args.get(“doctype”), args.get(“name”), “posting\_date”, ignore = true)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“transaction\_date”) → args.get(“posting\_date”) → Platform.get\_value(args.get(“doctype”), args.get(“name”), “posting\_date”, ignore = true).
- If date.
  - Update conditions using + “ and %(transaction\_date)s between ifnull(′tabPricing Rule′.valid\_from, '2000-01-01')\\n\\t\\t\\tand ifnull(′tabP …”.
  - Set values at “transaction\_date” from date.
- If args.get(“doctype”) belongs to list(“Quotation”, “Quotation Item”, “Sales Order”, “Sales Order Item”, …).
  - Update conditions using + “ and ifnull(′tabPricing Rule′.selling, 0) = 1”.
- Otherwise.
  - Update conditions using + “ and ifnull(′tabPricing Rule′.buying, 0) = 1”.
- Return conditions.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L770)

<a id="op-7cc22223c9b7e2"></a>
### Filter pricing rules

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_filter_pricing_rules`

**Inputs** args, pricing\_rules, doc = no value.

**Record and data access** resolve a document from “Pricing Rule” via get\_cached\_doc.

**Explicit results** mapping(“suggestion” → msg, “item\_code” → args.get(“item\_code”)) · pricing\_rules at 0.

**Explicit failure paths** validation helper with MultiplePricingRuleConflict — translated “Multiple Price Rules exists with same criteria, please resolve conflict by assigning priority. Price Rules: {0}”.format(whitespace '\\n'.join(generator of d.name for d drawn from pricing\_rules)).

**Local steps**

- If not isinstance(pricing\_rules, list).
  - Set pricing\_rules from list(pricing\_rules).
- Set original\_pricing\_rule from copy.copy(pricing\_rules).
- If pricing\_rules.
  - Set stock\_qty from flt(args.get(“stock\_qty”)).
  - Set amount from (flt(args.get(“price\_list\_rate”)) × flt(args.get(“qty”))).
  - Set pr\_doc from Platform.get\_cached\_doc(“Pricing Rule”, pricing\_rules at 0.name).
  - If (pricing\_rules at 0.mixed\_conditions and doc).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rules at 0.mixed\_conditions → doc.
    - Set tuple(stock\_qty, amount, items) from get\_qty\_and\_rate\_for\_mixed\_conditions(doc, pr\_doc, args).
    - For each pricing\_rule\_args in pricing\_rules.
      - Set pricing\_rule\_args.apply\_rule\_on\_other\_items from items.
  - Otherwise.
    - If pricing\_rules at 0.is\_cumulative.
      - Set tuple(cumulative\_qty, cumulative\_amount) from get\_cumulative\_qty\_and\_amount\_for\_row(pr\_doc, args, doc).
      - Update stock\_qty using + cumulative\_qty.
      - Update amount using + cumulative\_amount.
  - If (pricing\_rules at 0.apply\_rule\_on\_other and not pricing\_rules at 0.mixed\_conditions and doc).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rules at 0.apply\_rule\_on\_other → not pricing\_rules at 0.mixed\_conditions → doc.
    - Set pricing\_rules from (get\_qty\_and\_rate\_for\_other\_item(doc, pr\_doc, pricing\_rules, args) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_qty\_and\_rate\_for\_other\_item(doc, pr\_doc, pricing\_rules, args) → list().
  - Otherwise.
    - Set pricing\_rules from filter\_pricing\_rules\_for\_qty\_amount(stock\_qty, amount, pricing\_rules, args).
  - If not pricing\_rules.
    - For each d in original\_pricing\_rule.
      - If not d.threshold\_percentage.
        - Continue with the next iteration or loop test.
      - Set msg from validate\_quantity\_and\_amount\_for\_suggestion(d, stock\_qty, amount, args.get(“item\_code”), …).
      - If msg.
        - Return mapping(“suggestion” → msg, “item\_code” → args.get(“item\_code”)).
  - For each p in pricing\_rules.
    - If (p.item\_code and args.variant\_of).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in p.item\_code → args.variant\_of.
      - Set p.variant\_of from args.variant\_of.
    - Otherwise.
      - Set p.variant\_of from no value.
- If len(pricing\_rules) &gt; 1.
  - Set filtered\_rules from list(filter(deferred anonymous expression, pricing\_rules)).
  - If filtered\_rules.
    - Set pricing\_rules from filtered\_rules.
- If pricing\_rules.
  - Set max\_priority from max(generator of cint(p.priority) for p drawn from pricing\_rules).
    - Draw p from pricing\_rules.
  - If max\_priority.
    - Set pricing\_rules from list(filter(deferred anonymous expression, pricing\_rules)).
- If (pricing\_rules and not isinstance(pricing\_rules, list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rules → not isinstance(pricing\_rules, list).
  - Set pricing\_rules from list(pricing\_rules).
- If len(pricing\_rules) &gt; 1.
  - Set rate\_or\_discount from list(set(generator of d.rate\_or\_discount for d drawn from pricing\_rules)).
    - Draw d from pricing\_rules.
  - If (len(rate\_or\_discount) equals 1 and rate\_or\_discount at 0 equals “Discount Percentage”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(rate\_or\_discount) equals 1 → rate\_or\_discount at 0 equals “Discount Percentage”.
    - Set pricing\_rules from (list(filter(deferred anonymous expression, pricing\_rules)) or pricing\_rules).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in list(filter(deferred anonymous expression, pricing\_rules)) → pricing\_rules.
- If (len(pricing\_rules) &gt; 1 and not args.for\_shopping\_cart).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(pricing\_rules) &gt; 1 → not args.for\_shopping\_cart.
  - Call the validation error handler Platform.throw(translated “Multiple Price Rules exists with same criteria, please resolve conflict by assigning priority. Price Rules: {0}”.format(whitespace '\\n'.join(generator of d.name for d drawn from  ….
    - Draw d from pricing\_rules.
- Otherwise.
  - If pricing\_rules.
    - Return pricing\_rules at 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Pricing Rule”, pricing\_rules at 0.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L767)

<a id="op-84591183bde4cd"></a>
### Validate quantity and amount for suggestion

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_validate_quantity_and_amount_for_suggestion`

**Inputs** args, qty, amount, item\_code, transaction\_type.

**State and service calls** msgprint with msg.

**Explicit results** msg.

**Local steps**

- Set tuple(fieldname, msg) from tuple(empty text, empty text).
- Set type\_of\_transaction from “purchase” when transaction\_type equals “buying”, otherwise “sale”.
  - Value choice on transaction\_type equals “buying” — true gives “purchase”, false gives “sale”.
- For each tuple(field, value) in mapping(“min\_qty” → qty, “min\_amt” → amount).items().
  - If (args.get(field) and value &lt; args.get(field) and (args.get(field) − cint(((nested operand in the contract(nested operand in the contract) × nested operand in the contract.threshold\_percentage) × 0.01))) ≤ value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(field) → value &lt; args.get(field) → (args.get(field) − cint(((nested operand in the contract.get(field) × args.threshold\_percentage) × 0.01))) ≤ value.
    - Set fieldname from field.
- For each tuple(field, value) in mapping(“max\_qty” → qty, “max\_amt” → amount).items().
  - If (args.get(field) and value &gt; args.get(field) and (args.get(field) + cint(((nested operand in the contract(nested operand in the contract) × nested operand in the contract.threshold\_percentage) × 0.01))) ≥ value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(field) → value &gt; args.get(field) → (args.get(field) + cint(((nested operand in the contract.get(field) × args.threshold\_percentage) × 0.01))) ≥ value.
    - Set fieldname from field.
- If fieldname.
  - Set msg from translated “If you {0} {1} quantities of the item {2}, the scheme {3} will be applied on the item.”.format(type\_of\_transaction, args.get(fieldname), bold(item\_code), bold(args.title)).
  - If fieldname belongs to list(“min\_amt”, “max\_amt”).
    - Set msg from translated “If you {0} {1} worth item {2}, the scheme {3} will be applied on the item.”.format(type\_of\_transaction, fmt\_money(args.get(fieldname), currency = args.get(“currency”)), bold(item\_code), bold(args.title)).
  - Evaluate Platform.msgprint(msg).
- Return msg.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0136.json#L3572) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L784)

<a id="op-d0f145431a9597"></a>
### Filter pricing rules for qty amount

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_filter_pricing_rules_for_quantity_amount`

**Inputs** qty, rate, pricing\_rules, args = no value.

**Explicit results** rules.

**Local steps**

- Set rules from list().
- For each rule in pricing\_rules.
  - Set status from false.
  - Set conversion\_factor from 1.
  - If rule.get(“uom”).
    - Set conversion\_factor from get\_conversion\_factor(rule.item\_code, rule.uom).get(“conversion\_factor”, 1).
  - If (flt(qty) ≥ (flt(rule.min\_qty) × conversion\_factor) and flt(qty) ≤ (rule.max\_qty × conversion\_factor) when rule.max\_qty, otherwise true).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(qty) ≥ (flt(rule.min\_qty) × conversion\_factor) → flt(qty) ≤ (rule.max\_qty × conversion\_factor) when rule.max\_qty, otherwise true.
    - Value choice on rule.max\_qty — true gives flt(qty) ≤ (rule.max\_qty × conversion\_factor), false gives true.
    - Set status from true.
  - If (args and rule.get(“uom”) equals args.get(“uom”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args → rule.get(“uom”) equals args.get(“uom”).
    - Set conversion\_factor from 1.0.
  - If (status and (flt(rate) ≥ (flt(rule.min\_amt) × conversion\_factor) and flt(rate) ≤ (rule.max\_amt × conversion\_factor) when rule.max\_amt, otherwise true)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in status → (flt(rate) ≥ (flt(rule.min\_amt) × conversion\_factor) and flt(rate) ≤ (rule.max\_amt × conversion\_factor) when rule.max\_amt, otherwise true).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(rate) ≥ (flt(rule.min\_amt) × conversion\_factor) → flt(rate) ≤ (rule.max\_amt × conversion\_factor) when rule.max\_amt, otherwise true.
    - Value choice on rule.max\_amt — true gives flt(rate) ≤ (rule.max\_amt × conversion\_factor), false gives true.
    - Set status from true.
  - Otherwise.
    - Set status from false.
  - If status.
    - Evaluate rules.append(rule).
- Return rules.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0136.json#L4492) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L586) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L768)

<a id="op-a5300c152f6109"></a>
### If all rules same

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_if_all_rules_same`

**Inputs** pricing\_rules, fields.

**Explicit results** all\_rules\_same.

**Local steps**

- Set all\_rules\_same from true.
- Set val from list of pricing\_rules at 0.get(k) for k drawn from fields.
  - Draw k from fields.
- For each p in pricing\_rules at slice 1 to no value.
  - If val differs from list of p.get(k) for k drawn from fields.
    - Draw k from fields.
    - Set all\_rules\_same from false.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return all\_rules\_same.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0136.json#L5106) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L779)

<a id="op-f3041a98a12494"></a>
### Apply internal priority

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_apply_internal_priority`

**Inputs** pricing\_rules, field\_set, args.

**Explicit results** (filtered\_rules or pricing\_rules).

**Local steps**

- Set filtered\_rules from list().
- For each field in field\_set.
  - If args.get(field).
    - Set filtered\_rules from list(filter(deferred anonymous expression, pricing\_rules)).
    - If filtered\_rules.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return (filtered\_rules or pricing\_rules).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filtered\_rules → pricing\_rules.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0136.json#L5321) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L580) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L762)

<a id="op-7ef9c9c8613b8f"></a>
### Get qty and rate for mixed conditions

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_quantity_and_rate_for_mixed_conditions`

**Inputs** doc, pr\_doc, args.

**Explicit results** tuple(sum\_qty, sum\_amt, items).

**Local steps**

- Set tuple(sum\_qty, sum\_amt) from list(0, 0).
- Set items from (get\_pricing\_rule\_items(pr\_doc) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_pricing\_rule\_items(pr\_doc) → list().
- Set apply\_on from Platform.scrub(pr\_doc.get(“apply\_on”)).
- If (items and doc.get(“items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in items → doc.get(“items”).
  - For each row in doc.get(“items”).
    - If (row.get(“is\_free\_item”) or (row.get(apply\_on) or args.get(apply\_on)) does not belong to items).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“is\_free\_item”) → (row.get(apply\_on) or args.get(apply\_on)) does not belong to items.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(apply\_on) → args.get(apply\_on).
      - Continue with the next iteration or loop test.
    - If pr\_doc.mixed\_conditions.
      - Set amt from (args.get(“qty”) × args.get(“price\_list\_rate”)).
      - If not is\_row\_being\_priced(row, args).
        - Set amt from (flt(row.get(“qty”)) × flt((row.get(“price\_list\_rate”) or args.get(“rate”)))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“price\_list\_rate”) → args.get(“rate”).
      - Update sum\_qty using + (flt(row.get(“stock\_qty”)) or flt(args.get(“stock\_qty”)) or flt(args.get(“qty”))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.get(“stock\_qty”)) → flt(args.get(“stock\_qty”)) → flt(args.get(“qty”)).
      - Update sum\_amt using + amt.
  - If pr\_doc.is\_cumulative.
    - Set data from get\_qty\_amount\_data\_for\_cumulative(pr\_doc, doc, items).
    - If (data and data at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in data → data at 0.
      - Update sum\_qty using + data at 0.
      - Update sum\_amt using + data at 1.
- Return tuple(sum\_qty, sum\_amt, items).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L776)

<a id="op-dcb98d62753fa0"></a>
### Is row being priced

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_is_row_being_priced`

**Inputs** row, args.

**Explicit results** row.get(“name”) equals args.get(“child\_docname”) · row.get(“item\_code”) equals args.get(“item\_code”).

**Local steps**

- If args.get(“child\_docname”).
  - Return row.get(“name”) equals args.get(“child\_docname”).
- Return row.get(“item\_code”) equals args.get(“item\_code”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L287) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L925)

<a id="op-f0ad35b9059c04"></a>
### Get qty and rate for other item

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_quantity_and_rate_for_other_item`

**Inputs** doc, pr\_doc, pricing\_rules, row\_item.

**Explicit results** pricing\_rules.

**Local steps**

- Set other\_items from get\_pricing\_rule\_items(pr\_doc, other\_items = true).
- Set pricing\_rule\_apply\_on from apply\_on\_table.get(pr\_doc.get(“apply\_on”)).
- Set apply\_on from Platform.scrub(pr\_doc.get(“apply\_on”)).
- Set items from list().
- For each d in pr\_doc.get(pricing\_rule\_apply\_on).
  - If apply\_on equals “item\_group”.
    - Evaluate items.extend(get\_child\_item\_groups(d.get(apply\_on))).
  - Otherwise.
    - Evaluate items.append(d.get(apply\_on)).
- For each row in doc.items.
  - If row.get(apply\_on) belongs to items.
    - If not row.get(“qty”).
      - Continue with the next iteration or loop test.
    - Set stock\_qty from (row.get(“qty”) × (row.get(“conversion\_factor”) or 1.0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“conversion\_factor”) → 1.0.
    - Set amount from (stock\_qty × (flt(row.get(“price\_list\_rate”)) or flt(row.get(“rate”)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.get(“price\_list\_rate”)) → flt(row.get(“rate”)).
    - Set pricing\_rules from filter\_pricing\_rules\_for\_qty\_amount(stock\_qty, amount, pricing\_rules, row).
    - If (pricing\_rules and pricing\_rules at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rules → pricing\_rules at 0.
      - Set pricing\_rules at 0.apply\_rule\_on\_other\_items from other\_items.
      - Return pricing\_rules.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0136.json#L6371) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L777)

<a id="op-1d6c2d19173188"></a>
### Get qty amount data for cumulative

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_quantity_amount_data_for_cumulative`

**Inputs** pr\_doc, doc, items = no value.

**Explicit results** list(sum(generator of d at 0 for d drawn from totals), sum(generator of d at 1 for d drawn from totals)).

**Local steps**

- Set totals from get\_cumulative\_totals(pr\_doc, doc, items).values().
- Return list(sum(generator of d at 0 for d drawn from totals), sum(generator of d at 1 for d drawn from totals)).
  - Draw d from totals.
  - Draw d from totals.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L775)

<a id="op-07b1a49638614c"></a>
### Get cumulative qty and amount for row

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_get_cumulative_qty_and_amount_for_row`

**Inputs** pr\_doc, args, doc = no value.

**Explicit results** tuple(0, 0) · get\_cumulative\_totals(pr\_doc, args, values).get(value, tuple(0, 0)).

**Local steps**

- Set apply\_on from Platform.scrub(pr\_doc.get(“apply\_on”)).
- Set value from args.get(apply\_on).
- If not value.
  - Return tuple(0, 0).
- Set rows from doc.get(“items”) when doc, otherwise no value.
  - Value choice on doc — true gives doc.get(“items”), false gives no value.
- Set values from set(value, expanded generator of row.get(apply\_on) for row drawn from (rows or list()) where row.get(apply\_on)).
  - Draw row from (rows or list()), keep a combination only if (row.get(apply\_on)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().
- Return get\_cumulative\_totals(pr\_doc, args, values).get(value, tuple(0, 0)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L283) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L921)

<a id="op-39a98093c28b47"></a>
### Get cumulative totals

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_get_cumulative_totals`

**Inputs** pr\_doc, doc, items = no value.

**Explicit results** get\_cumulative\_qty\_and\_amount(pr\_doc.name, (doc.get(“parenttype”) or doc.doctype), doc.get(“company”), tuple(sorted(set((items or list())))), …).

**Local steps**

- Return get\_cumulative\_qty\_and\_amount(pr\_doc.name, (doc.get(“parenttype”) or doc.doctype), doc.get(“company”), tuple(sorted(set((items or list())))), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“parenttype”) → doc.doctype.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in items → list().

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L284) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L922)

<a id="op-a4d75921f5172a"></a>
### Get cumulative qty and amount

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_get_cumulative_qty_and_amount`

**Inputs** pricing\_rule, doctype, company, items, transaction, transaction\_modified.

**Wrappers, in declaration order** request\_cache.

**Record and data access** resolve a document from “Pricing Rule” via get\_cached\_doc.

**Explicit results** mapping of value → tuple(flt(qty), flt(amount)) for tuple(value, qty, amount) drawn from query.run().

**Local steps**

- Set pr\_doc from Platform.get\_cached\_doc(“Pricing Rule”, pricing\_rule).
- Set parent from Platform.qb.DocType(doctype).
- Set child from Platform.qb.DocType(formatted text {doctype} Item).
- Set apply\_on from child at Platform.scrub(pr\_doc.get(“apply\_on”)).
- Set date\_field from “transaction\_date” when Platform.get\_meta(doctype).has\_field(“transaction\_date”), otherwise “posting\_date”.
  - Value choice on Platform.get\_meta(doctype).has\_field(“transaction\_date”) — true gives “transaction\_date”, false gives “posting\_date”.
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(parent at date\_ ….
- If company.
  - Set query from query.where(parent.company equals company).
- If pr\_doc.warehouse.
  - Set query from query.where(child.warehouse.isin(get\_child\_warehouses(pr\_doc.warehouse))).
- If items.
  - Set query from query.where(apply\_on.isin(items)).
- Set query from filter\_cumulative\_query\_by\_applicable\_for(query, parent, pr\_doc, doctype).
- Return mapping of value → tuple(flt(qty), flt(amount)) for tuple(value, qty, amount) drawn from query.run().
  - Draw tuple(value, qty, amount) from query.run().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Pricing Rule”, pricing\_rule).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L282) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L920)

<a id="op-ea752cab6b7842"></a>
### Filter cumulative query by applicable for

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_filter_cumulative_query_by_applicable_for`

**Inputs** query, parent, pr\_doc, doctype.

**Explicit results** query · query.where(parent at fieldname.isin(values)).

**Local steps**

- If not pr\_doc.applicable\_for.
  - Return query.
- Set fieldname from CUMULATIVE\_APPLICABLE\_FOR\_FIELDS at pr\_doc.applicable\_for.
- If (doctype equals “Quotation” and fieldname equals “customer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “Quotation” → fieldname equals “customer”.
  - Set fieldname from “party\_name”.
- If not Platform.get\_meta(doctype).has\_field(fieldname).
  - Return query.
- Set values from get\_applicable\_for\_values(pr\_doc.applicable\_for, pr\_doc.get(Platform.scrub(pr\_doc.applicable\_for))).
- Return query.where(parent at fieldname.isin(values)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L280) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L918)

<a id="op-a95709670f4d07"></a>
### Get applicable for values

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_get_applicable_for_values`

**Inputs** applicable\_for, value.

**Wrappers, in declaration order** request\_cache.

**Explicit results** list(value, expanded get\_descendants\_of(applicable\_for, value, ignore\_permissions = true)) · list(value).

**Local steps**

- If applicable\_for belongs to tuple(“Customer Group”, “Territory”, “Supplier Group”).
  - Return list(value, expanded get\_descendants\_of(applicable\_for, value, ignore\_permissions = true)).
- Return list(value).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L281) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L919)

<a id="op-90fc48f351a32e"></a>
### Apply pricing rule on transaction

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_apply_pricing_rule_on_transaction`

**Inputs** doc.

**State and service calls** execute a supplied database query · msgprint with translated “User has not applied rule on the invoice {0}”.format(doc.name).

**Local steps**

- Set conditions from “apply\_on = 'Transaction'”.
- Set values from mapping(“price\_list” → (doc.get(“selling\_price\_list”) or doc.get(“buying\_price\_list”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“selling\_price\_list”) → doc.get(“buying\_price\_list”) → empty text.
- Set conditions from get\_other\_conditions(conditions, values, doc).
- Update conditions using + “ and coalesce(′tabPricing Rule′.for\_price\_list, '') in (%(price\_list)s, '')”.
- Set pricing\_rules from Platform.db.sql(formatted text  Select ′tabPricing Rule′.\* from ′tabPricing Rule′  where  {conditions} and ′tabPricing Rule′.disable = 0  , values, as\_dict = 1).
- Set grand\_total from doc.get(“grand\_total”).
- Set previously\_applied\_rules from get\_transaction\_pricing\_rules(doc).
- Set has\_rule\_discount from (bool(previously\_applied\_rules) and not is\_transaction\_discount\_changed(doc)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(previously\_applied\_rules) → not is\_transaction\_discount\_changed(doc).
- Set applied\_rules from list().
- If pricing\_rules.
  - Set pricing\_rules from filter\_pricing\_rules\_for\_qty\_amount(doc.total\_qty, doc.total, pricing\_rules).
  - Set pricing\_rules from filter\_pricing\_rule\_based\_on\_condition(pricing\_rules, doc).
- Evaluate remove\_free\_item(doc, set of d.name for d drawn from pricing\_rules).
  - Draw d from pricing\_rules.
- For each d in pricing\_rules.
  - If d.price\_or\_product\_discount equals “Price”.
    - If (d.coupon\_code\_based and not is\_coupon\_of\_pricing\_rule(doc, d.name)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.coupon\_code\_based → not is\_coupon\_of\_pricing\_rule(doc, d.name).
      - Continue with the next iteration or loop test.
    - Set coupon\_rule\_applied from false.
    - Set fields\_set from set().
    - For each field in list(“additional\_discount\_percentage”, “discount\_amount”).
      - Set pr\_field from “discount\_percentage” when field equals “additional\_discount\_percentage”, otherwise field.
        - Value choice on field equals “additional\_discount\_percentage” — true gives “discount\_percentage”, false gives field.
      - If not d.get(pr\_field).
        - Continue with the next iteration or loop test.
      - If (d.validate\_applied\_rule and doc.get(field) is distinct from no value and doc.get(field) &lt; d.get(pr\_field)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.validate\_applied\_rule → doc.get(field) is distinct from no value → doc.get(field) &lt; d.get(pr\_field).
        - Evaluate Platform.msgprint(translated “User has not applied rule on the invoice {0}”.format(doc.name)).
      - Otherwise.
        - If d.apply\_discount\_on.
          - Evaluate doc.set(“apply\_discount\_on”, d.apply\_discount\_on).
        - Evaluate doc.set(field, d.get(pr\_field)).
        - Evaluate fields\_set.add(field).
        - Evaluate applied\_rules.append(d.name).
        - If d.coupon\_code\_based.
          - Set coupon\_rule\_applied from true.
          - Leave the innermost loop without its normal-exhaustion alternative.
    - If (has\_rule\_discount and fields\_set).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_rule\_discount → fields\_set.
      - For each field in (set(“additional\_discount\_percentage”, “discount\_amount”) − fields\_set).
        - Evaluate doc.set(field, 0).
    - Evaluate doc.calculate\_taxes\_and\_totals().
    - If coupon\_rule\_applied.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Otherwise.
    - If d.price\_or\_product\_discount equals “Product”.
      - Set item\_details from Platform.\_dict(mapping(“parenttype” → doc.doctype, “free\_item\_data” → list())).
      - Evaluate get\_product\_discount\_rule(d, item\_details, doc = doc).
      - Evaluate apply\_pricing\_rule\_for\_free\_items(doc, item\_details.free\_item\_data).
      - Evaluate doc.set\_missing\_values().
      - Evaluate doc.calculate\_taxes\_and\_totals().
- If (has\_rule\_discount and not applied\_rules).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_rule\_discount → not applied\_rules.
  - Evaluate remove\_transaction\_discount(doc, previously\_applied\_rules).
- Evaluate set\_transaction\_pricing\_rules(doc, applied\_rules).
- If flt(doc.get(“grand\_total”)) differs from flt(grand\_total).
  - Evaluate doc.validate\_all\_documents\_schedule().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L583) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L765)

<a id="op-4f33fe0751dbc9"></a>
### Is coupon of pricing rule

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_is_coupon_of_pricing_rule`

**Inputs** doc, pricing\_rule.

**Record and data access** read “Coupon Code” via get\_value.

**Explicit results** (bool(coupon\_code) and Platform.db.get\_value(“Coupon Code”, coupon\_code, “pricing\_rule”) equals pricing\_rule).

**Local steps**

- Set coupon\_code from doc.get(“coupon\_code”).
- Return (bool(coupon\_code) and Platform.db.get\_value(“Coupon Code”, coupon\_code, “pricing\_rule”) equals pricing\_rule).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(coupon\_code) → Platform.db.get\_value(“Coupon Code”, coupon\_code, “pricing\_rule”) equals pricing\_rule.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L286) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L924)
