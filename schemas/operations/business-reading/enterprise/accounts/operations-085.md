# Accounting and settlement · operations 85

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pricing rule

[Record definition](../../../../data/record-types/pricing_rule.json)

<a id="op-6077822a21705b"></a>
### Pricing Rule.validate max discount

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_maximum_discount`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- If (self.rate\_or\_discount equals “Discount Percentage” and self.get(“items”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.rate\_or\_discount equals “Discount Percentage” → self.get(“items”).
  - For each d in self.items.
    - Set max\_discount from Platform.get\_cached\_value(“Item”, d.item\_code, “max\_discount”).
    - If (max\_discount and flt(self.discount\_percentage) &gt; flt(max\_discount)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_discount → flt(self.discount\_percentage) &gt; flt(max\_discount).
      - Evaluate throw(translated “Max discount allowed for item: {0} is {1}%”.format(d.item\_code, max\_discount)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “max\_discount”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L4143) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L528) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L710)

<a id="op-2ceaedaa5ae44c"></a>
### Pricing Rule.validate price list with currency

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_price_list_with_currency`

**Inputs** self.

**Record and data access** read “Price List” via get\_value.

**Local steps**

- If (self.currency and self.for\_price\_list).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency → self.for\_price\_list.
  - Set price\_list\_currency from Platform.db.get\_value(“Price List”, self.for\_price\_list, “currency”, true).
  - If self.currency differs from price\_list\_currency.
    - Evaluate throw(translated “Currency should be same as Price List Currency: {0}”.format(price\_list\_currency)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L4420) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L532) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L714)

<a id="op-94fa55a50c6684"></a>
### Pricing Rule.validate dates

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Valid from and valid upto fields are mandatory for the cumulative”.

**Local steps**

- If (self.is\_cumulative and not (self.valid\_from and self.valid\_upto)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_cumulative → not (self.valid\_from and self.valid\_upto).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.valid\_from → self.valid\_upto.
  - Call the validation error handler Platform.throw(translated “Valid from and valid upto fields are mandatory for the cumulative”).
- Evaluate self.validate\_from\_to\_dates(“valid\_from”, “valid\_upto”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L4616) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L525) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L707)

<a id="op-6184d320c1e09c"></a>
### Pricing Rule.validate condition

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_condition`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Invalid condition expression”.

**Local steps**

- If (self.condition and “=” belongs to self.condition and re.match(“&#91;\\w\\.:\_&#93;+\\s\*={1}\\s\*&#91;\\w\\.@\\'"&#93;+”, self.condition)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.condition → “=” belongs to self.condition → re.match(“&#91;\\w\\.:\_&#93;+\\s\*={1}\\s\*&#91;\\w\\.@\\'"&#93;+”, self.condition).
  - Call the validation error handler Platform.throw(translated “Invalid condition expression”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L4770) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L524) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L706)

<a id="op-c49f8f954b5a17"></a>
### Pricing Rule.validate mixed with recursion

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_mixed_with_recursion`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Recursive Discounts with Mixed condition is not supported by the system”.

**Local steps**

- If (self.mixed\_conditions and self.is\_recursive).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.mixed\_conditions → self.is\_recursive.
  - Call the validation error handler Platform.throw(translated “Recursive Discounts with Mixed condition is not supported by the system”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L4909) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L531) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L713)

<a id="op-939fbf102a00be"></a>
### Apply pricing rule

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_apply_pricing_rule`

**Inputs** args, doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_all.

**Explicit results** out.

**Local steps**

- If isinstance(args, str).
  - Set args from json.loads(args).
- Set args from Platform.\_dict(args).
- Evaluate validate\_pricing\_context(args).
- Evaluate set\_transaction\_type(args).
- Set out from list().
- If args.get(“doctype”) equals “Material Request”.
  - Return out.
- Set item\_list from args.get(“items”).
- Evaluate args.pop(“items”).
- Set item\_code\_list from tuple(generator of item.get(“item\_code”) for item drawn from item\_list).
  - Draw item from item\_list.
- Set query\_items from Platform.get\_all(“Item”, fields = list(“item\_code”, “has\_serial\_no”), filters = list(list(“item\_code”, “in”, item\_code\_list)), as\_list = 1).
- Set serialized\_items from dict().
- For each tuple(item\_code, val) in query\_items.
  - Evaluate serialized\_items.setdefault(item\_code, val).
- For each item in item\_list.
  - Set args\_copy from copy.deepcopy(args).
  - Evaluate args\_copy.update(item).
  - Evaluate set\_transaction\_type(args\_copy).
  - Set data from get\_pricing\_rule\_for\_item(args\_copy, doc = doc).
  - Evaluate out.append(data).
- Return out.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L517) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L699)

<a id="op-dbce3e102c4994"></a>
### Update pricing rule uom

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_update_pricing_rule_unit_of_measure`

**Inputs** pricing\_rule, args.

**Local steps**

- Set child\_doc from mapping(“Item Code” → “items”, “Item Group” → “item\_groups”, “Brand” → “brands”).get(pricing\_rule.apply\_on).
- Set apply\_on\_field from Platform.scrub(pricing\_rule.apply\_on).
- For each row in pricing\_rule.get(child\_doc).
  - If row.get(apply\_on\_field) equals args.get(apply\_on\_field).
    - Set pricing\_rule.uom from row.uom.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L5699) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L722)

<a id="op-4849eca495a5b7"></a>
### Get pricing rule for item

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_get_pricing_rule_for_item`

**Inputs** args, doc = no value, for\_validate = false.

**Record and data access** resolve a document from doc via get\_doc · read args.doctype via exists · read “Coupon Code” via get\_cached\_value · read “Pricing Rule” via get\_cached\_value · resolve a document from “Item” via get\_cached\_doc · 2 additional forms in the steps below.

**Explicit results** mapping() · item\_details.

**Explicit failure paths** validation helper — translated “Set an Item Price for item {0} before removing or replacing its Rate pricing rule.”.format(args.item\_code).

**Local steps**

- Bind dependencies get\_applied\_pricing\_rules, get\_pricing\_rule\_items, get\_product\_discount\_rule.
- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- If doc.
  - Set doc from Platform.get\_doc(doc).
- If (args.get(“is\_free\_item”) or args.get(“parenttype”) equals “Material Request”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“is\_free\_item”) → args.get(“parenttype”) equals “Material Request”.
  - Return mapping().
- Set item\_details from Platform.\_dict(mapping(“doctype” → args.doctype, “has\_margin” → false, “name” → args.name, “free\_item\_data” → list(), …)).
- If (args.ignore\_pricing\_rule or not args.item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.ignore\_pricing\_rule → not args.item\_code.
  - If (Platform.db.exists(args.doctype, args.name) and args.get(“pricing\_rules”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.exists(args.doctype, args.name) → args.get(“pricing\_rules”).
    - Set item\_details from reset\_pricing\_rule\_details(args.get(“pricing\_rules”), item\_details, item\_code = args.get(“item\_code”), rate = args.get(“price\_list\_rate”)).
  - Return item\_details.
- Evaluate update\_args\_for\_pricing\_rule(args).
- Set applied\_rules from get\_applied\_pricing\_rules(args.get(“pricing\_rules”)).
- Set coupon\_pricing\_rule from Platform.get\_cached\_value(“Coupon Code”, args.coupon\_code, “pricing\_rule”) when args.get(“coupon\_code”), otherwise no value.
  - Value choice on args.get(“coupon\_code”) — true gives Platform.get\_cached\_value(“Coupon Code”, args.coupon\_code, “pricing\_rule”), false gives no value.
- Set pricing\_rules from select\_pricing\_rules(args, doc, for\_validate).
- Set selected\_rules from set of rule when isinstance(rule, str), otherwise rule.get(“name”) for rule drawn from (pricing\_rules or list()) where rule.
  - Draw rule from (pricing\_rules or list()), keep a combination only if (rule).
  - Value choice on isinstance(rule, str) — true gives rule, false gives rule.get(“name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rules → list().
- Set removed\_rules from list of rule for rule drawn from applied\_rules where rule does not belong to selected\_rules.
  - Draw rule from applied\_rules, keep a combination only if (rule does not belong to selected\_rules).
- If for\_validate.
  - Evaluate notify\_removed\_pricing\_rules(args, removed\_rules).
- Set removed\_rate\_rules from list of rule for rule drawn from removed\_rules where Platform.get\_cached\_value(“Pricing Rule”, rule, “rate\_or\_discount”) equals “Rate”.
  - Draw rule from removed\_rules, keep a combination only if (Platform.get\_cached\_value(“Pricing Rule”, rule, “rate\_or\_discount”) equals “Rate”).
- If removed\_rate\_rules.
  - Set get\_price\_list\_rate from Platform.get\_attr(“Enterprise.stock.get\_item\_details.get\_price\_list\_rate”).
  - Set price\_args from args.copy().
  - Evaluate price\_args.update(price\_list\_rate = 0, rate = 0).
  - Set item from Platform.get\_cached\_doc(“Item”, args.item\_code).
  - Set price from get\_price\_list\_rate(price\_args, item).
  - If (price.get(“price\_list\_rate”) is identical to no value and args.transaction\_type equals “selling” and Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in price.get(“price\_list\_rate”) is identical to no value → args.transaction\_type equals “selling” → Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”).
    - Set price\_args.price\_list from Platform.get\_single\_value(“Selling Settings”, “selling\_price\_list”).
    - Set price\_args.price\_list\_uom\_dependant from no value.
    - Set price from get\_price\_list\_rate(price\_args, item).
  - If price.get(“price\_list\_rate”) is distinct from no value.
    - Set args.price\_list\_rate, item\_details.price\_list\_rate from flt(price.get(“price\_list\_rate”)).
- Set rules from list().
- If pricing\_rules.
  - If removed\_rules.
    - Set item\_details from reset\_pricing\_rule\_details(Platform.as\_json(removed\_rules), item\_details, item\_code = args.item\_code, rate = args.price\_list\_rate).
  - Set price\_rules from list().
  - For each pricing\_rule in pricing\_rules.
    - If not pricing\_rule.
      - Continue with the next iteration or loop test.
    - If isinstance(pricing\_rule, str).
      - Set pricing\_rule from Platform.get\_cached\_doc(“Pricing Rule”, pricing\_rule).
      - Evaluate update\_pricing\_rule\_uom(pricing\_rule, args).
      - Set fetch\_other\_item from true when pricing\_rule.apply\_rule\_on\_other, otherwise false.
        - Value choice on pricing\_rule.apply\_rule\_on\_other — true gives true, false gives false.
      - Set pricing\_rule.apply\_rule\_on\_other\_items from (get\_pricing\_rule\_items(pricing\_rule, other\_items = fetch\_other\_item) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_pricing\_rule\_items(pricing\_rule, other\_items = fetch\_other\_item) → list().
    - If pricing\_rule.get(“coupon\_code\_based”) equals 1.
      - If not args.coupon\_code.
        - Continue with the next iteration or loop test.
      - If coupon\_pricing\_rule differs from pricing\_rule.name.
        - Continue with the next iteration or loop test.
    - If pricing\_rule.get(“suggestion”).
      - Continue with the next iteration or loop test.
    - Set item\_details.validate\_applied\_rule from pricing\_rule.get(“validate\_applied\_rule”, 0).
    - Set item\_details.price\_or\_product\_discount from pricing\_rule.get(“price\_or\_product\_discount”).
    - Evaluate rules.append(get\_pricing\_rule\_details(args, pricing\_rule)).
    - If (pricing\_rule.mixed\_conditions or pricing\_rule.apply\_rule\_on\_other).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rule.mixed\_conditions → pricing\_rule.apply\_rule\_on\_other.
      - Evaluate item\_details.update(mapping(“price\_or\_product\_discount” → pricing\_rule.price\_or\_product\_discount, “apply\_rule\_on” → Platform.scrub(pricing\_rule.apply\_rule\_on\_other) when pricing\_rule.apply\_rule\_on\_other, o ….
        - Value choice on pricing\_rule.apply\_rule\_on\_other — true gives Platform.scrub(pricing\_rule.apply\_rule\_on\_other), false gives Platform.scrub(pricing\_rule.get(“apply\_on”)).
      - If pricing\_rule.apply\_rule\_on\_other\_items.
        - Set item\_details at “apply\_rule\_on\_other\_items” from json.dumps(pricing\_rule.apply\_rule\_on\_other\_items).
    - If not pricing\_rule.validate\_applied\_rule.
      - If pricing\_rule.price\_or\_product\_discount equals “Price”.
        - Evaluate price\_rules.append(pricing\_rule).
      - Otherwise.
        - Evaluate get\_product\_discount\_rule(pricing\_rule, item\_details, args, doc).
  - For each pricing\_rule in price\_rules.
    - If pricing\_rule.rate\_or\_discount equals “Rate”.
      - Evaluate apply\_price\_discount\_rule(pricing\_rule, item\_details, args).
  - For each pricing\_rule in price\_rules.
    - Evaluate apply\_pricing\_rule\_margin(pricing\_rule, item\_details, args).
  - For each pricing\_rule in price\_rules.
    - If pricing\_rule.rate\_or\_discount differs from “Rate”.
      - Evaluate apply\_price\_discount\_rule(pricing\_rule, item\_details, args).
  - If any(generator of (rule.rate\_or\_discount equals “Discount Amount” and rule.discount\_amount) for rule drawn from price\_rules).
    - Draw rule from price\_rules.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.rate\_or\_discount equals “Discount Amount” → rule.discount\_amount.
    - Set item\_details.discount\_percentage from 0.0.
    - If item\_details.pricing\_rule\_for equals “Discount Percentage”.
      - Set item\_details.pricing\_rule\_for from “Discount Amount”.
  - If not item\_details.get(“has\_margin”).
    - Set item\_details.margin\_type from no value.
    - Set item\_details.margin\_rate\_or\_amount from 0.0.
  - Set item\_details.has\_pricing\_rule from 1.
  - Set item\_details.pricing\_rules from Platform.as\_json(list of d.pricing\_rule for d drawn from rules).
    - Draw d from rules.
- If (removed\_rate\_rules and item\_details.get(“price\_list\_rate”) is identical to no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in removed\_rate\_rules → item\_details.get(“price\_list\_rate”) is identical to no value.
  - If any(generator of Platform.get\_cached\_value(“Pricing Rule”, rule, “coupon\_code\_based”) for rule drawn from removed\_rate\_rules).
    - Draw rule from removed\_rate\_rules.
    - Call the validation error handler Platform.throw(translated “Set an Item Price for item {0} before removing or replacing its Rate pricing rule.”.format(args.item\_code)).
  - Set item\_details.price\_list\_rate from args.price\_list\_rate.
- If (not rules and applied\_rules).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not rules → applied\_rules.
  - Set item\_details from reset\_pricing\_rule\_details(args.get(“pricing\_rules”), item\_details, item\_code = args.get(“item\_code”), rate = args.get(“price\_list\_rate”)).
- Return item\_details.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Coupon Code”, args.coupon\_code, “pricing\_rule”), Platform.get\_cached\_value(“Pricing Rule”, rule, “rate\_or\_discount”) and 5 further calls · selected callable from Platform.get\_attr(“Enterprise.stock.get\_item\_details.get\_price\_list\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L520) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L702)

<a id="op-4ceef18b53343e"></a>
### Select pricing rules

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_select_pricing_rules`

**Inputs** args, doc, for\_validate.

**Explicit results** get\_applied\_pricing\_rules(args.get(“pricing\_rules”)) · get\_pricing\_rules(args, doc).

**Local steps**

- Bind dependencies get\_applied\_pricing\_rules, get\_pricing\_rules.
- If (for\_validate and args.get(“pricing\_rules”) and is\_row\_unchanged\_since\_save(args, doc)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → args.get(“pricing\_rules”) → is\_row\_unchanged\_since\_save(args, doc).
  - Return get\_applied\_pricing\_rules(args.get(“pricing\_rules”)).
- Return get\_pricing\_rules(args, doc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L914)

<a id="op-11bea2ec090098"></a>
### Is row unchanged since save

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_is_row_unchanged_since_save`

**Inputs** args, doc.

**Explicit results** false · (not any(generator of row.has\_value\_changed(field) for field drawn from PRICING\_ROW\_FIELDS) and not any(generator of doc.has\_value\_changed(field) for field drawn from PRICING\_PARENT\_FIELDS where nested ope ….

**Local steps**

- If (not doc or doc.get(“\_action”) differs from “submit” or not doc.get\_doc\_before\_save()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc → doc.get(“\_action”) differs from “submit” → not doc.get\_doc\_before\_save().
  - Return false.
- Set row from next(generator of d for d drawn from (doc.get(“items”) or list()) where d.name equals args.child\_docname, no value).
  - Draw d from (doc.get(“items”) or list()), keep a combination only if (d.name equals args.child\_docname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“items”) → list().
- If (not row or not row.get\_doc\_before\_save()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row → not row.get\_doc\_before\_save().
  - Return false.
- Return (not any(generator of row.has\_value\_changed(field) for field drawn from PRICING\_ROW\_FIELDS) and not any(generator of doc.has\_value\_changed(field) for field drawn from PRICING\_PARENT\_FIELDS where nested ope ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not any(generator of row.has\_value\_changed(field) for field drawn from PRICING\_ROW\_FIELDS) → not any(generator of doc.has\_value\_changed(field) for field drawn from PRICING\_PARENT\_FIELDS where doc.meta.has\_field(field)).
  - Draw field from PRICING\_ROW\_FIELDS.
  - Draw field from PRICING\_PARENT\_FIELDS, keep a combination only if (doc.meta.has\_field(field)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L273) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L911)

<a id="op-0e1677496d63eb"></a>
### Notify removed pricing rules

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_notify_removed_pricing_rules`

**Inputs** args, removed\_rules.

**State and service calls** msgprint with translated “Row {0}: Pricing Rule {1} no longer applies to item {2} and has been removed”.format(args.idx, get\_link\_to\_form(“Pricing Rule”, pricing\_rule), Platform.bold(args.item\_code)).

**Local steps**

- For each pricing\_rule in removed\_rules.
  - Evaluate Platform.msgprint(translated “Row {0}: Pricing Rule {1} no longer applies to item {2} and has been removed”.format(args.idx, get\_link\_to\_form(“Pricing Rule”, pricing\_rule), Platform.bold(args.item\_code)),  ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L274) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L912)

<a id="op-31153b11e196d1"></a>
### Update args for pricing rule

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_update_arguments_for_pricing_rule`

**Inputs** args.

**Record and data access** read “Item” via get\_cached\_value · read “Customer” via get\_cached\_value · read “Supplier” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Item Group not mentioned in item master for item {0}”.format(args.item\_code).

**Local steps**

- If not (args.item\_group and args.brand).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.item\_group → args.brand.
  - Set item from Platform.get\_cached\_value(“Item”, args.item\_code, tuple(“item\_group”, “brand”)).
  - If not item.
    - Return no value.
  - Set tuple(args.item\_group, args.brand) from item.
  - If not args.item\_group.
    - Call the validation error handler Platform.throw(translated “Item Group not mentioned in item master for item {0}”.format(args.item\_code)).
- If args.transaction\_type equals “selling”.
  - If (args.customer and not (args.customer\_group and args.territory)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.customer → not (args.customer\_group and args.territory).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.customer\_group → args.territory.
    - If (args.quotation\_to and args.quotation\_to differs from “Customer”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.quotation\_to → args.quotation\_to differs from “Customer”.
      - Set customer from Platform.\_dict().
    - Otherwise.
      - Set customer from Platform.get\_cached\_value(“Customer”, args.customer, list(“customer\_group”, “territory”)).
    - If customer.
      - Set tuple(args.customer\_group, args.territory) from customer.
  - Set args.supplier, args.supplier\_group from no value.
- Otherwise.
  - If (args.supplier and not args.supplier\_group).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.supplier → not args.supplier\_group.
    - Set args.supplier\_group from Platform.get\_cached\_value(“Supplier”, args.supplier, “supplier\_group”).
    - Set args.customer, args.customer\_group, args.territory from no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, args.item\_code, tuple(“item\_group”, “brand”)), Platform.get\_cached\_value(“Customer”, args.customer, list(“customer\_group”, “territory”)) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0131.json#L1929) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L721)

<a id="op-ff6e5b7f2eca43"></a>
### Get pricing rule details

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_get_pricing_rule_details`

**Inputs** args, pricing\_rule.

**Explicit results** Platform.\_dict(mapping(“pricing\_rule” → pricing\_rule.name, “rate\_or\_discount” → pricing\_rule.rate\_or\_discount, “margin\_type” → pricing\_rule.margin\_type, “item\_code” → args.get(“item\_code”), …)).

**Local steps**

- Return Platform.\_dict(mapping(“pricing\_rule” → pricing\_rule.name, “rate\_or\_discount” → pricing\_rule.rate\_or\_discount, “margin\_type” → pricing\_rule.margin\_type, “item\_code” → args.get(“item\_code”), …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0131.json#L2579) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L519) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L701)

<a id="op-c10ffe1574439b"></a>
### Apply price discount rule

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_apply_price_discount_rule`

**Inputs** pricing\_rule, item\_details, args.

**Local steps**

- Set item\_details.pricing\_rule\_for from pricing\_rule.rate\_or\_discount.
- If pricing\_rule.rate\_or\_discount equals “Rate”.
  - Set pricing\_rule\_rate from 0.0.
  - If pricing\_rule.currency equals args.currency.
    - Set pricing\_rule\_rate from pricing\_rule.rate.
  - If pricing\_rule\_rate.
    - Set is\_blank\_uom from pricing\_rule.get(“uom”) differs from args.get(“uom”).
    - Evaluate item\_details.update(mapping(“price\_list\_rate” → (pricing\_rule\_rate × args.get(“conversion\_factor”, 1) when is\_blank\_uom, otherwise 1))).
      - Value choice on is\_blank\_uom — true gives args.get(“conversion\_factor”, 1), false gives 1.
    - Set item\_details.has\_pricing\_rule\_for\_rate from true.
  - Evaluate item\_details.update(mapping(“discount\_percentage” → 0.0, “discount\_amount” → 0.0)).
- Set discount\_rate from flt(item\_details.get(“price\_list\_rate”, args.price\_list\_rate)).
- If item\_details.get(“margin\_type”) equals “Percentage”.
  - Update discount\_rate using × (1 + (flt(item\_details.margin\_rate\_or\_amount) ÷ 100)).
- Otherwise.
  - If item\_details.get(“margin\_type”) equals “Amount”.
    - Update discount\_rate using + flt(item\_details.margin\_rate\_or\_amount).
- For each apply\_on in list(“Discount Amount”, “Discount Percentage”).
  - If pricing\_rule.rate\_or\_discount differs from apply\_on.
    - Continue with the next iteration or loop test.
  - Set field from Platform.scrub(apply\_on).
  - If discount\_rate.
    - Set value from pricing\_rule.get(field, 0).
    - Set calculate\_discount\_percentage from false.
    - If field equals “discount\_percentage”.
      - Set field from “discount\_amount”.
      - Set discount\_base from discount\_rate.
      - If pricing\_rule.apply\_discount\_on\_rate.
        - Update discount\_base using − flt(item\_details.get(“discount\_amount”)).
      - Set value from (discount\_base × (value ÷ 100)).
      - Set calculate\_discount\_percentage from true.
    - If field does not belong to item\_details.
      - Evaluate item\_details.setdefault(field, 0).
    - Update item\_details at field using + value when pricing\_rule, otherwise args.get(field, 0).
      - Value choice on pricing\_rule — true gives value, false gives args.get(field, 0).
    - If (calculate\_discount\_percentage or item\_details.get(“discount\_percentage”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in calculate\_discount\_percentage → item\_details.get(“discount\_percentage”).
      - Set item\_details.discount\_percentage from flt(((flt(item\_details.discount\_amount) ÷ discount\_rate) × 100)).
  - Otherwise.
    - If field does not belong to item\_details.
      - Evaluate item\_details.setdefault(field, 0).
    - Update item\_details at field using + pricing\_rule.get(field, 0) when pricing\_rule, otherwise args.get(field, 0).
      - Value choice on pricing\_rule — true gives pricing\_rule.get(field, 0), false gives args.get(field, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L516) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L698)

<a id="op-ec1d2444d9c748"></a>
### Apply pricing rule margin

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_apply_pricing_rule_margin`

**Inputs** pricing\_rule, item\_details, args.

**Local steps**

- If ((pricing\_rule.margin\_type belongs to list(“Amount”, “Percentage”) and pricing\_rule.currency equals args.currency) or pricing\_rule.margin\_type equals “Percentage”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (pricing\_rule.margin\_type belongs to list(“Amount”, “Percentage”) and pricing\_rule.currency equals args.currency) → pricing\_rule.margin\_type equals “Percentage”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rule.margin\_type belongs to list(“Amount”, “Percentage”) → pricing\_rule.currency equals args.currency.
  - Set margin\_type from pricing\_rule.margin\_type.
  - Set margin from flt(pricing\_rule.margin\_rate\_or\_amount).
  - If (pricing\_rule.apply\_multiple\_pricing\_rules and item\_details.margin\_rate\_or\_amount is distinct from no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rule.apply\_multiple\_pricing\_rules → item\_details.margin\_rate\_or\_amount is distinct from no value.
    - Set existing\_margin from item\_details.margin\_rate\_or\_amount.
    - If (item\_details.margin\_type and item\_details.margin\_type differs from margin\_type).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details.margin\_type → item\_details.margin\_type differs from margin\_type.
      - Set price\_list\_rate from flt(item\_details.get(“price\_list\_rate”, args.get(“price\_list\_rate”))).
      - If item\_details.margin\_type equals “Percentage”.
        - Update existing\_margin using × (price\_list\_rate ÷ 100).
      - Otherwise.
        - Update margin using × (price\_list\_rate ÷ 100).
      - Set margin\_type from “Amount”.
    - Update margin using + existing\_margin.
  - Set item\_details.margin\_type from margin\_type.
  - Set item\_details.margin\_rate\_or\_amount from margin.
  - Set item\_details.has\_margin from true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L270) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L908)

<a id="op-21a2befc0e87b9"></a>
### Remove pricing rule for item

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_remove_pricing_rule_for_item`

**Inputs** pricing\_rules, item\_details, item\_code = no value, rate = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** reset\_pricing\_rule\_details(pricing\_rules, item\_details, item\_code = item\_code, rate = rate).

**Local steps**

- Set item\_details from Platform.\_dict(Platform.parse\_json(item\_details)).
- Evaluate validate\_pricing\_context(Platform.\_dict(doctype = item\_details.parenttype, name = item\_details.parent)).
- Return reset\_pricing\_rule\_details(pricing\_rules, item\_details, item\_code = item\_code, rate = rate).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L718)

<a id="op-83f9094e2bcb34"></a>
### Reset pricing rule details

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_reset_pricing_rule_details`

**Inputs** pricing\_rules, item\_details, item\_code = no value, rate = no value.

**Record and data access** read “Pricing Rule” via exists · resolve a document from “Pricing Rule” via get\_cached\_doc.

**Explicit results** item\_details.

**Local steps**

- Bind dependencies get\_applied\_pricing\_rules, get\_pricing\_rule\_items.
- For each d in get\_applied\_pricing\_rules(pricing\_rules).
  - If (not d or not Platform.db.exists(“Pricing Rule”, d)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d → not Platform.db.exists(“Pricing Rule”, d).
    - Continue with the next iteration or loop test.
  - Set pricing\_rule from Platform.get\_cached\_doc(“Pricing Rule”, d).
  - If pricing\_rule.price\_or\_product\_discount equals “Price”.
    - If pricing\_rule.rate\_or\_discount belongs to list(“Rate”, “Discount Percentage”, “Discount Amount”).
      - Set item\_details.discount\_percentage from 0.0.
      - Set item\_details.discount\_amount from 0.0.
      - Set item\_details.rate from (rate or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in rate → 0.0.
    - If pricing\_rule.margin\_type belongs to list(“Percentage”, “Amount”).
      - Set item\_details.margin\_rate\_or\_amount from 0.0.
      - Set item\_details.margin\_type from no value.
  - Otherwise.
    - If (pricing\_rule.get(“free\_item”) and not pricing\_rule.get(“dont\_enforce\_free\_item\_qty”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rule.get(“free\_item”) → not pricing\_rule.get(“dont\_enforce\_free\_item\_qty”).
      - Set item\_details.remove\_free\_item from item\_code when pricing\_rule.get(“same\_item”), otherwise pricing\_rule.get(“free\_item”).
        - Value choice on pricing\_rule.get(“same\_item”) — true gives item\_code, false gives pricing\_rule.get(“free\_item”).
  - If (pricing\_rule.get(“mixed\_conditions”) or pricing\_rule.get(“apply\_rule\_on\_other”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rule.get(“mixed\_conditions”) → pricing\_rule.get(“apply\_rule\_on\_other”).
    - Set items from get\_pricing\_rule\_items(pricing\_rule, other\_items = true).
    - Set item\_details.apply\_on from Platform.scrub(pricing\_rule.apply\_rule\_on\_other) when pricing\_rule.apply\_rule\_on\_other, otherwise Platform.scrub(pricing\_rule.get(“apply\_on”)).
      - Value choice on pricing\_rule.apply\_rule\_on\_other — true gives Platform.scrub(pricing\_rule.apply\_rule\_on\_other), false gives Platform.scrub(pricing\_rule.get(“apply\_on”)).
    - Set item\_details.applied\_on\_items from “,”.join(items).
- Set item\_details.pricing\_rules from empty text.
- Set item\_details.pricing\_rule\_removed from true.
- Return item\_details.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Pricing Rule”, d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L913)

<a id="op-468d73f563962d"></a>
### Remove pricing rules

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_remove_pricing_rules`

**Inputs** item\_list.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** out.

**Local steps**

- Set item\_list from list of Platform.\_dict(item) for item drawn from Platform.parse\_json(item\_list).
  - Draw item from Platform.parse\_json(item\_list).
- For each tuple(doctype, name) in set of tuple(item.parenttype, item.parent) for item drawn from item\_list.
  - Draw item from item\_list.
  - Evaluate validate\_pricing\_context(Platform.\_dict(doctype = doctype, name = name)).
- Set out from list().
- For each item in item\_list.
  - If item.get(“pricing\_rules”).
    - Evaluate out.append(reset\_pricing\_rule\_details(item.get(“pricing\_rules”), item, item.item\_code, item.get(“price\_list\_rate”))).
- Return out.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L719)

<a id="op-9a9b041e94ca0f"></a>
### Validate pricing context

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_validate_pricing_context`

**Inputs** ctx.

**Declared result** no value.

**Record and data access** read transaction\_doctype via exists.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid doctype”.

**Local steps**

- Set transaction\_doctype from ctx.get(“doctype”).
- If transaction\_doctype does not belong to PRICING\_TRANSACTION\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Invalid doctype”, Platform.PermissionError).
- Set transaction\_name from ctx.get(“name”).
- If (not isinstance(transaction\_name, str) or not Platform.db.exists(transaction\_doctype, transaction\_name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(transaction\_name, str) → not Platform.db.exists(transaction\_doctype, transaction\_name).
  - Set transaction\_name from no value.
- Evaluate Platform.has\_permission(transaction\_doctype, doc = transaction\_name, throw = true).
- Set ctx.transaction\_type from no value.
- Evaluate validate\_pricing\_parties(ctx).
- Evaluate validate\_pricing\_price\_lists(ctx, transaction\_doctype).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(transaction\_doctype, doc = transaction\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L915)

<a id="op-a54c8b20af6a99"></a>
### Validate pricing parties

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_validate_pricing_parties`

**Inputs** ctx.

**Declared result** no value.

**Record and data access** read party\_type via exists.

**Local steps**

- For each party\_type in tuple(“Customer”, “Supplier”).
  - Set party from ctx.get(Platform.scrub(party\_type)).
  - If (party and Platform.db.exists(party\_type, party)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party → Platform.db.exists(party\_type, party).
    - Evaluate Platform.has\_permission(party\_type, “select”, doc = party, throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(party\_type, “select”, doc = party, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L916)

<a id="op-e1564dce67b18e"></a>
### Validate pricing price lists

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_validate_pricing_price_lists`

**Inputs** ctx, doctype.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Price List {0} cannot be used in {1}”.format(price\_list, translated doctype).

**Local steps**

- If doctype equals “BOM”.
  - Return no value.
- Set meta from Platform.get\_meta(doctype).
- Set side from no value.
- If meta.has\_field(“selling\_price\_list”).
  - Set side from “selling”.
- Otherwise.
  - If meta.has\_field(“buying\_price\_list”).
    - Set side from “buying”.
- For each price\_list in set(ctx.get(“price\_list”), ctx.get(“selling\_price\_list”), ctx.get(“buying\_price\_list”)).
  - If (price\_list and not (side and fits\_price\_list\_side(ctx, price\_list, side))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in price\_list → not (side and fits\_price\_list\_side(ctx, price\_list, side)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in side → fits\_price\_list\_side(ctx, price\_list, side).
    - Call the validation error handler Platform.throw(translated “Price List {0} cannot be used in {1}”.format(price\_list, translated doctype), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L917)

<a id="op-d6b5e850d181ae"></a>
### Fits price list side

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_fits_price_list_side`

**Inputs** ctx, price\_list, side.

**Declared result** bool.

**Record and data access** read “Price List” via get\_cached\_value · read “Customer” via get\_cached\_value · read “Supplier” via get\_cached\_value.

**Explicit results** true · bool((ctx.get(“customer”) and Platform.get\_cached\_value(“Customer”, ctx.customer, “is\_internal\_customer”))) · bool((ctx.get(“supplier”) and Platform.get\_cached\_value(“Supplier”, ctx.supplier, “is\_internal\_supplier”))).

**Local steps**

- If Platform.get\_cached\_value(“Price List”, price\_list, side).
  - Return true.
- If is\_return\_against\_price\_list(ctx, price\_list, side).
  - Return true.
- If side equals “selling”.
  - Return bool((ctx.get(“customer”) and Platform.get\_cached\_value(“Customer”, ctx.customer, “is\_internal\_customer”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“customer”) → Platform.get\_cached\_value(“Customer”, ctx.customer, “is\_internal\_customer”).
- Return bool((ctx.get(“supplier”) and Platform.get\_cached\_value(“Supplier”, ctx.supplier, “is\_internal\_supplier”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“supplier”) → Platform.get\_cached\_value(“Supplier”, ctx.supplier, “is\_internal\_supplier”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, side), Platform.get\_cached\_value(“Customer”, ctx.customer, “is\_internal\_customer”) and 1 further calls.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L909)

<a id="op-80ac51b573eeee"></a>
### Is return against price list

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_pricing_rule_is_return_against_price_list`

**Inputs** ctx, price\_list, side.

**Declared result** bool.

**Record and data access** read ctx.doctype via get\_value.

**Explicit results** false · bool((voucher and voucher at formatted text {side}\_price\_list equals price\_list and voucher at party\_field equals ctx.get(party\_field) and Platform.has\_permission(ctx.doctype, doc = return\_against))).

**Local steps**

- Set return\_against from ctx.get(“return\_against”).
- If not (ctx.get(“is\_return”) and isinstance(return\_against, str) and Platform.get\_meta(ctx.doctype).has\_field(“return\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ctx.get(“is\_return”) → isinstance(return\_against, str) → Platform.get\_meta(ctx.doctype).has\_field(“return\_against”).
  - Return false.
- Set party\_field from “customer” when side equals “selling”, otherwise “supplier”.
  - Value choice on side equals “selling” — true gives “customer”, false gives “supplier”.
- Set voucher from Platform.db.get\_value(ctx.doctype, mapping(“name” → return\_against, “docstatus” → 1), list(formatted text {side}\_price\_list, party\_field), as\_dict = true).
- Return bool((voucher and voucher at formatted text {side}\_price\_list equals price\_list and voucher at party\_field equals ctx.get(party\_field) and Platform.has\_permission(ctx.doctype, doc = return\_against))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher → voucher at formatted text {side}\_price\_list equals price\_list → voucher at party\_field equals ctx.get(party\_field) → Platform.has\_permission(ctx.doctype, doc = return\_against).

**Values supplied outside this operation** effective access from Platform.has\_permission(ctx.doctype, doc = return\_against).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L910)

<a id="op-07705ef9e15bd0"></a>
### Set transaction type

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_set_transaction_type`

**Inputs** pricing\_ctx.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If pricing\_ctx.transaction\_type belongs to list(“buying”, “selling”).
  - Return no value.
- If pricing\_ctx.doctype belongs to tuple(“Opportunity”, “Quotation”, “Sales Order”, “Delivery Note”, …).
  - Set pricing\_ctx.transaction\_type from “selling”.
- Otherwise.
  - If pricing\_ctx.doctype belongs to tuple(“Material Request”, “Supplier Quotation”, “Purchase Order”, “Purchase Receipt”, …).
    - Set pricing\_ctx.transaction\_type from “buying”.
  - Otherwise.
    - If pricing\_ctx.customer.
      - Set pricing\_ctx.transaction\_type from “selling”.
    - Otherwise.
      - Set pricing\_ctx.transaction\_type from “buying”.

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0131.json#L5224) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L720)
