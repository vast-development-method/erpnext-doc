# Accounting and settlement · operations 87

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pricing rule

[Record definition](../../../../data/record-types/pricing_rule.json)

<a id="op-050a1a6c63630c"></a>
### Get transaction pricing rules

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_get_transaction_pricing_rules`

**Inputs** doc.

**Record and data access** read “Coupon Code” via get\_value.

**State and service calls** execute a supplied database query.

**Explicit results** pricing\_rules.

**Local steps**

- Set rows from list((doc.get(“pricing\_rules”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“pricing\_rules”) → list().
- If doc\_before\_save bound to doc.get\_doc\_before\_save().
  - Update rows using + (doc\_before\_save.get(“pricing\_rules”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc\_before\_save.get(“pricing\_rules”) → list().
- Set pricing\_rules from set of d.pricing\_rule for d drawn from rows where (d.pricing\_rule and not d.item\_code and not d.child\_docname).
  - Draw d from rows, keep a combination only if ((d.pricing\_rule and not d.item\_code and not d.child\_docname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.pricing\_rule → not d.item\_code → not d.child\_docname.
- If (pricing\_rules or not doc\_before\_save or not doc\_before\_save.get(“coupon\_code”) or doc\_before\_save.coupon\_code equals doc.get(“coupon\_code”) or doc\_before\_save.ignore\_pricing\_rule).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rules → not doc\_before\_save → not doc\_before\_save.get(“coupon\_code”) → doc\_before\_save.coupon\_code equals doc.get(“coupon\_code”) → doc\_before\_save.ignore\_pricing\_rule.
  - Return pricing\_rules.
- Set values from mapping(“pricing\_rule” → Platform.db.get\_value(“Coupon Code”, doc\_before\_save.coupon\_code, “pricing\_rule”)).
- Set conditions from get\_other\_conditions(“name = %(pricing\_rule)s and apply\_on = 'Transaction' and price\_or\_product\_discount = 'Price' and coupon\_code …”, values, doc\_before\_save).
- Set coupon\_rules from Platform.db.sql(formatted text select \* from ′tabPricing Rule′ where {conditions}, values, as\_dict = true).
- Set coupon\_rules from filter\_pricing\_rules\_for\_qty\_amount(doc\_before\_save.total\_qty, doc\_before\_save.total, coupon\_rules).
- For each rule in filter\_pricing\_rule\_based\_on\_condition(coupon\_rules, doc\_before\_save).
  - Set field from “additional\_discount\_percentage” when rule.discount\_percentage, otherwise “discount\_amount”.
    - Value choice on rule.discount\_percentage — true gives “additional\_discount\_percentage”, false gives “discount\_amount”.
  - Set discount from (rule.discount\_percentage or rule.discount\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in rule.discount\_percentage → rule.discount\_amount.
  - If (discount and doc\_before\_save.apply\_discount\_on equals rule.apply\_discount\_on and doc\_before\_save.get(field) equals flt(discount, doc\_before\_save.precision(field))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in discount → doc\_before\_save.apply\_discount\_on equals rule.apply\_discount\_on → doc\_before\_save.get(field) equals flt(discount, doc\_before\_save.precision(field)).
    - Evaluate pricing\_rules.add(rule.name).
- Return pricing\_rules.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L285) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L923)

<a id="op-166521a527db65"></a>
### Set transaction pricing rules

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_set_transaction_pricing_rules`

**Inputs** doc, applied\_rules.

**Explicit results** no value.

**Local steps**

- If not doc.meta.has\_field(“pricing\_rules”).
  - Return no value.
- Evaluate doc.set(“pricing\_rules”, list of d for d drawn from doc.get(“pricing\_rules”) where (d.item\_code or d.child\_docname)).
  - Draw d from doc.get(“pricing\_rules”), keep a combination only if ((d.item\_code or d.child\_docname)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.item\_code → d.child\_docname.
- For each pricing\_rule in dict.fromkeys(applied\_rules).
  - Evaluate doc.append(“pricing\_rules”, mapping(“pricing\_rule” → pricing\_rule, “rule\_applied” → 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L928)

<a id="op-7a5d8d9c6d106f"></a>
### Is transaction discount changed

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_is_transaction_discount_changed`

**Inputs** doc.

**Explicit results** false · true · (not doc.additional\_discount\_percentage and flt(doc.discount\_amount) differs from flt(doc\_before\_save.discount\_amount)).

**Local steps**

- Set doc\_before\_save from doc.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return false.
- If flt(doc.additional\_discount\_percentage) differs from flt(doc\_before\_save.additional\_discount\_percentage).
  - Return true.
- Return (not doc.additional\_discount\_percentage and flt(doc.discount\_amount) differs from flt(doc\_before\_save.discount\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.additional\_discount\_percentage → flt(doc.discount\_amount) differs from flt(doc\_before\_save.discount\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L288) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L926)

<a id="op-bb27b662931304"></a>
### Remove transaction discount

`operation_enterprise_binding_enterprise_accounts_doctype_pricing_rule_utils_remove_transaction_discount`

**Inputs** doc, pricing\_rules.

**State and service calls** msgprint with translated “Additional Discount has been removed as Pricing Rule {0} is no longer applicable”.format(“, ”.join(generator of get\_link\_to\_form(“Pricing Rule”, d) for d drawn from sorted(pricing\_rules))).

**Explicit results** no value.

**Local steps**

- If (not flt(doc.additional\_discount\_percentage) and not flt(doc.discount\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(doc.additional\_discount\_percentage) → not flt(doc.discount\_amount).
  - Return no value.
- Set doc.additional\_discount\_percentage from 0.
- Set doc.discount\_amount from 0.
- Evaluate doc.calculate\_taxes\_and\_totals().
- Evaluate Platform.msgprint(translated “Additional Discount has been removed as Pricing Rule {0} is no longer applicable”.format(“, ”.join(generator of get\_link\_to\_form(“Pricing Rule”, d) for d drawn from sorted(pri ….
  - Draw d from sorted(pricing\_rules).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L289) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L927)

<a id="op-35d0e4fa7d70cf"></a>
### Remove free item

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_remove_free_item`

**Inputs** doc, matched\_rules.

**Explicit results** no value.

**Local steps**

- Set free\_item\_rules from set of d.pricing\_rules for d drawn from doc.items where (d.is\_free\_item and d.pricing\_rules).
  - Draw d from doc.items, keep a combination only if ((d.is\_free\_item and d.pricing\_rules)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_free\_item → d.pricing\_rules.
- If not (free\_item\_rules − matched\_rules).
  - Return no value.
- Set pricing\_rule from Platform.qb.DocType(“Pricing Rule”).
- Set transaction\_rules from set(nested operand in the contract.where(nested operand in the contract(nested operand in the contract)).where(pricing\_rule.apply\_on equals “Transaction”).run(pluck = true)).
- For each d in list(doc.items).
  - If (d.is\_free\_item and d.pricing\_rules belongs to transaction\_rules).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_free\_item → d.pricing\_rules belongs to transaction\_rules.
    - Evaluate doc.remove(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L780)

<a id="op-f132c540c285b8"></a>
### Get applied pricing rules

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_applied_pricing_rules`

**Inputs** pricing\_rules.

**Explicit results** json.loads(pricing\_rules) · pricing\_rules.split(“,”) · list().

**Local steps**

- If pricing\_rules.
  - If pricing\_rules.startswith(“&#91;”).
    - Return json.loads(pricing\_rules).
  - Otherwise.
    - Return pricing\_rules.split(“,”).
- Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L769)

<a id="op-62ba9318b636f8"></a>
### Get product discount rule

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_product_discount_rule`

**Inputs** pricing\_rule, item\_details, args = no value, doc = no value.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Free item not set in the pricing rule {0}”.format(get\_link\_to\_form(“Pricing Rule”, pricing\_rule.name)).

**Local steps**

- Set free\_item from pricing\_rule.free\_item.
- If (pricing\_rule.same\_item and pricing\_rule.get(“apply\_on”) differs from “Transaction”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rule.same\_item → pricing\_rule.get(“apply\_on”) differs from “Transaction”.
  - Set free\_item from (item\_details.item\_code or args.item\_code).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_details.item\_code → args.item\_code.
- If not free\_item.
  - Call the validation error handler Platform.throw(translated “Free item not set in the pricing rule {0}”.format(get\_link\_to\_form(“Pricing Rule”, pricing\_rule.name))).
- Set qty from (pricing\_rule.free\_qty or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rule.free\_qty → 1.
- If (pricing\_rule.is\_recursive and pricing\_rule.get(“apply\_on”) differs from “Transaction”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pricing\_rule.is\_recursive → pricing\_rule.get(“apply\_on”) differs from “Transaction”.
  - Set transaction\_qty from sum(list of flt(row.qty) for row drawn from doc.items where (not row.is\_free\_item and row.item\_code equals args.item\_code and row.pricing\_rules equals args.pricing\_rules)).
    - Draw row from doc.items, keep a combination only if ((not row.is\_free\_item and row.item\_code equals args.item\_code and row.pricing\_rules equals args.pricing\_rules)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.is\_free\_item → row.item\_code equals args.item\_code → row.pricing\_rules equals args.pricing\_rules.
  - Set transaction\_qty from (transaction\_qty − pricing\_rule.apply\_recursion\_over).
  - If (transaction\_qty and transaction\_qty &gt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in transaction\_qty → transaction\_qty &gt; 0.
    - Set free\_qty from qty.
    - Set qty from ((flt(transaction\_qty) × free\_qty) ÷ pricing\_rule.recurse\_for).
    - If pricing\_rule.round\_free\_qty.
      - Set qty from ((flt(transaction\_qty) floor divide pricing\_rule.recurse\_for) × free\_qty).
    - Set recursion\_over from flt(pricing\_rule.apply\_recursion\_over).
    - If (recursion\_over and recursion\_over equals flt(pricing\_rule.min\_qty)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in recursion\_over → recursion\_over equals flt(pricing\_rule.min\_qty).
      - Update qty using + free\_qty.
- If not qty.
  - Return no value.
- Set free\_item\_data\_args from mapping(“item\_code” → free\_item, “qty” → qty, “pricing\_rules” → pricing\_rule.name, “rate” → (pricing\_rule.free\_item\_rate or 0), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rule.free\_item\_rate → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rule.free\_item\_rate → 0.
- Set item\_data from Platform.get\_cached\_value(“Item”, free\_item, list(“item\_name”, “description”, “stock\_uom”), as\_dict = 1).
- Evaluate free\_item\_data\_args.update(item\_data).
- Set free\_item\_data\_args at “uom” from (pricing\_rule.free\_item\_uom or item\_data.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rule.free\_item\_uom → item\_data.stock\_uom.
- Set free\_item\_data\_args at “conversion\_factor” from get\_conversion\_factor(free\_item, free\_item\_data\_args at “uom”).get(“conversion\_factor”, 1).
- If item\_details.get(“parenttype”) equals “Purchase Order”.
  - Set free\_item\_data\_args at “schedule\_date” from doc.schedule\_date when doc, otherwise today().
    - Value choice on doc — true gives doc.schedule\_date, false gives today().
- If item\_details.get(“parenttype”) equals “Sales Order”.
  - Set free\_item\_data\_args at “delivery\_date” from doc.delivery\_date when doc, otherwise today().
    - Value choice on doc — true gives doc.delivery\_date, false gives today().
- Evaluate item\_details.free\_item\_data.append(free\_item\_data\_args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, free\_item, list(“item\_name”, “description”, “stock\_uom”), as\_dict = 1) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L774)

<a id="op-54c353a8a2da44"></a>
### Apply pricing rule for free items

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_apply_pricing_rule_for_free_items`

**Inputs** doc, pricing\_rule\_args.

**Record and data access** read “Pricing Rule” via get\_value.

**Local steps**

- If pricing\_rule\_args.
  - Set args from mapping of tuple(d at “item\_code”, d at “pricing\_rules”) → d for d drawn from pricing\_rule\_args.
    - Draw d from pricing\_rule\_args.
  - For each item in doc.items.
    - If not item.is\_free\_item.
      - Continue with the next iteration or loop test.
    - Set free\_item\_data from args.get(tuple(item.item\_code, item.pricing\_rules)).
    - If free\_item\_data.
      - Evaluate free\_item\_data.pop(“item\_name”).
      - Evaluate free\_item\_data.pop(“description”).
      - Evaluate item.update(free\_item\_data).
      - Evaluate args.pop(tuple(item.item\_code, item.pricing\_rules)).
  - For each free\_item in args.values().
    - If (doc.is\_new() or not Platform.get\_value(“Pricing Rule”, free\_item at “pricing\_rules”, “dont\_enforce\_free\_item\_qty”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_new() → not Platform.get\_value(“Pricing Rule”, free\_item at “pricing\_rules”, “dont\_enforce\_free\_item\_qty”).
      - Evaluate doc.append(“items”, free\_item).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0137.json#L3588) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L582) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L764)

<a id="op-5912ecceb965e0"></a>
### Get pricing rule items

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_get_pricing_rule_items`

**Inputs** pr\_doc, other\_items = false.

**Declared result** list.

**Explicit results** list(set(apply\_on\_data)).

**Local steps**

- Set apply\_on\_data from list().
- Set apply\_on from Platform.scrub(pr\_doc.get(“apply\_on”)).
- Set pricing\_rule\_apply\_on from apply\_on\_table.get(pr\_doc.get(“apply\_on”)).
- If (pr\_doc.apply\_rule\_on\_other and other\_items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pr\_doc.apply\_rule\_on\_other → other\_items.
  - Set apply\_on from Platform.scrub(pr\_doc.apply\_rule\_on\_other).
  - Evaluate apply\_on\_data.append(pr\_doc.get((“other\_” + apply\_on))).
- Otherwise.
  - For each d in pr\_doc.get(pricing\_rule\_apply\_on).
    - If apply\_on equals “item\_group”.
      - Evaluate apply\_on\_data.extend(get\_child\_item\_groups(d.get(apply\_on))).
    - Otherwise.
      - Evaluate apply\_on\_data.append(d.get(apply\_on)).
- Return list(set(apply\_on\_data)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0137.json#L4060) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L771)

<a id="op-bf190f0d8df70c"></a>
### Validate coupon code

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_validate_coupon_code`

**Inputs** coupon\_name, customer = no value.

**Record and data access** resolve a document from “Coupon Code” via get\_doc.

**Explicit failure paths** validation helper — translated “This Gift Card cannot be used by this customer” · validation helper — translated “Sorry, this coupon code's validity has not started” · validation helper — translated “Sorry, this coupon code's validity has expired” · validation helper — translated “Sorry, this coupon code is no longer valid”.

**Local steps**

- Set coupon from Platform.get\_doc(“Coupon Code”, coupon\_name).
- If (coupon.coupon\_type equals “Gift Card” and coupon.customer differs from customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in coupon.coupon\_type equals “Gift Card” → coupon.customer differs from customer.
  - Call the validation error handler Platform.throw(translated “This Gift Card cannot be used by this customer”).
- If (coupon.valid\_from and coupon.valid\_from &gt; getdate(today())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in coupon.valid\_from → coupon.valid\_from &gt; getdate(today()).
  - Call the validation error handler Platform.throw(translated “Sorry, this coupon code's validity has not started”).
- Otherwise.
  - If (coupon.valid\_upto and coupon.valid\_upto &lt; getdate(today())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in coupon.valid\_upto → coupon.valid\_upto &lt; getdate(today()).
    - Call the validation error handler Platform.throw(translated “Sorry, this coupon code's validity has expired”).
  - Otherwise.
    - If (coupon.maximum\_use and coupon.used ≥ coupon.maximum\_use).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in coupon.maximum\_use → coupon.used ≥ coupon.maximum\_use.
      - Call the validation error handler Platform.throw(translated “Sorry, this coupon code is no longer valid”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L783)

<a id="op-64a907b84b947f"></a>
### Update coupon code count

`operation_enterprise_accounts_record_definitions_pricing_rule_utils_business_behavior_update_coupon_code_count`

**Inputs** coupon\_name, transaction\_type.

**Record and data access** resolve a document from “Coupon Code” via get\_doc.

**State and service calls** call save on coupon.

**Explicit failure paths** validation helper — translated “{0} Coupon used are {1}. Allowed quantity is exhausted”.format(coupon.coupon\_code, coupon.used).

**Local steps**

- Set coupon from Platform.get\_doc(“Coupon Code”, coupon\_name).
- If coupon.
  - If transaction\_type equals “used”.
    - If not coupon.maximum\_use.
      - Set coupon.used from (coupon.used + 1).
      - Evaluate coupon.save(ignore\_permissions = true).
    - Otherwise.
      - If coupon.used &lt; coupon.maximum\_use.
        - Set coupon.used from (coupon.used + 1).
        - Evaluate coupon.save(ignore\_permissions = true).
      - Otherwise.
        - Call the validation error handler Platform.throw(translated “{0} Coupon used are {1}. Allowed quantity is exhausted”.format(coupon.coupon\_code, coupon.used)).
  - Otherwise.
    - If transaction\_type equals “cancelled”.
      - If coupon.used &gt; 0.
        - Set coupon.used from (coupon.used − 1).
        - Evaluate coupon.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L782)

## Record · Process deferred accounting

[Record definition](../../../../data/record-types/process_deferred_accounting.json)

<a id="op-e0a6fc29434735"></a>
### Process Deferred Accounting.validate

`operation_enterprise_accounts_record_definitions_process_deferred_accounting_business_behavior_process_deferred_accounting_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “End date cannot be before start date”.

**Local steps**

- If self.end\_date &lt; self.start\_date.
  - Call the validation error handler Platform.throw(translated “End date cannot be before start date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0137.json#L5233) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L787)

<a id="op-b335dc19b18814"></a>
### Process Deferred Accounting.on submit

`operation_enterprise_accounts_record_definitions_process_deferred_accounting_business_behavior_process_deferred_accounting_on_submit`

**Inputs** self.

**Local steps**

- Set conditions from build\_conditions(self.type, self.account, self.company).
- If self.type equals “Income”.
  - Evaluate convert\_deferred\_revenue\_to\_income(self.name, self.start\_date, self.end\_date, conditions).
- Otherwise.
  - Evaluate convert\_deferred\_expense\_to\_expense(self.name, self.start\_date, self.end\_date, conditions).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0137.json#L5333) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L786)

<a id="op-6c2b95ad1180aa"></a>
### Process Deferred Accounting.on cancel

`operation_enterprise_accounts_record_definitions_process_deferred_accounting_business_behavior_process_deferred_accounting_on_cancel`

**Inputs** self.

**Record and data access** read “GL Entry” via get\_all.

**Local steps**

- Set self.ignore\_linked\_doctypes from list(“GL Entry”).
- Set gl\_entries from Platform.get\_all(“GL Entry”, fields = list(“\*”), filters = mapping(“against\_voucher\_type” → self.doctype, “against\_voucher” → self.name)).
- Evaluate make\_gl\_entries(gl\_map = gl\_entries, cancel = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0137.json#L5532) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L785)

## Record · Process payment reconciliation

[Record definition](../../../../data/record-types/process_payment_reconciliation.json)

<a id="op-64edb2227875e7"></a>
### Process Payment Reconciliation.on discard

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_process_payment_reconciliation_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0137.json#L6967) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L802)

<a id="op-094239a17c5b94"></a>
### Process Payment Reconciliation.validate

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_process_payment_reconciliation_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_receivable\_payable\_account().
- Evaluate self.validate\_bank\_cash\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate receivable payable account](operations-087.md#op-a323ebd73482e9), [validate bank cash account](operations-087.md#op-df72442dff10e9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0137.json#L7030) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L804)

<a id="op-a323ebd73482e9"></a>
### Process Payment Reconciliation.validate receivable payable account

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_process_payment_reconciliation_validate_receivable_payable_account`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Receivable/Payable Account: {0} doesn't belong to company {1}”.format(Platform.bold(self.receivable\_payable\_account), Platform.bold(self.company)).

**Local steps**

- If self.receivable\_payable\_account.
  - If self.company differs from Platform.db.get\_value(“Account”, self.receivable\_payable\_account, “company”).
    - Call the validation error handler Platform.throw(translated “Receivable/Payable Account: {0} doesn't belong to company {1}”.format(Platform.bold(self.receivable\_payable\_account), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L806)

<a id="op-df72442dff10e9"></a>
### Process Payment Reconciliation.validate bank cash account

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_process_payment_reconciliation_validate_bank_cash_account`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Bank/Cash Account {0} doesn't belong to company {1}”.format(Platform.bold(self.bank\_cash\_account), Platform.bold(self.company)).

**Local steps**

- If self.bank\_cash\_account.
  - If self.company differs from Platform.db.get\_value(“Account”, self.bank\_cash\_account, “company”).
    - Call the validation error handler Platform.throw(translated “Bank/Cash Account {0} doesn't belong to company {1}”.format(Platform.bold(self.bank\_cash\_account), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L222) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L805)

<a id="op-d87f43fec52a91"></a>
### Process Payment Reconciliation.before save

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_process_payment_reconciliation_before_save`

**Inputs** self.

**Local steps**

- Set self.status from empty text.
- Set self.error\_log from empty text.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L438) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L800)

<a id="op-d51b543077aacc"></a>
### Process Payment Reconciliation.on submit

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_process_payment_reconciliation_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Queued”).
- Evaluate self.db\_set(“error\_log”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L502) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L803)

<a id="op-6d99094adc51b7"></a>
### Process Payment Reconciliation.on cancel

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_process_payment_reconciliation_on_cancel`

**Inputs** self.

**Record and data access** read “Process Payment Reconciliation Log” via get\_value.

**State and service calls** call db\_set on self · request set\_value on “Process Payment Reconciliation Log”.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).
- Set log from Platform.db.get\_value(“Process Payment Reconciliation Log”, filters = mapping(“process\_pr” → self.name)).
- If log.
  - Evaluate Platform.db.set\_value(“Process Payment Reconciliation Log”, log, “status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L595) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L801)

<a id="op-1ff6d7fc9f8453"></a>
### Get reconciled count

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_get_reconciled_count`

**Inputs** docname = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Record and data access** read “Process Payment Reconciliation Log” via get\_value · read “Process Payment Reconciliation Log” via get\_all.

**Explicit results** current\_status.

**Local steps**

- Set current\_status from mapping().
- If docname.
  - Set reconcile\_log from Platform.db.get\_value(“Process Payment Reconciliation Log”, filters = mapping(“process\_pr” → docname), fieldname = “name”).
  - If reconcile\_log.
    - Set res from Platform.get\_all(“Process Payment Reconciliation Log”, filters = mapping(“name” → reconcile\_log), fields = list(“reconciled\_entries”, “total\_allocations”), as\_list = 1).
    - Set tuple(current\_status at “processed”, current\_status at “total”) from res at 0.
- Return current\_status.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L788) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L796)

<a id="op-45ea20963d171c"></a>
### Get pr instance

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_get_purchase_receipt_instance`

**Inputs** doc.

**Record and data access** resolve a document from “Process Payment Reconciliation” via get\_doc · resolve a document from “Payment Reconciliation” via get\_doc.

**Explicit results** pr.

**Local steps**

- Set process\_payment\_reconciliation from Platform.get\_doc(“Process Payment Reconciliation”, doc).
- Set pr from Platform.get\_doc(“Payment Reconciliation”).
- Set fields from list(“company”, “party\_type”, “party”, “receivable\_payable\_account”, …).
- Set d from mapping().
- For each field in fields.
  - Set d at field from process\_payment\_reconciliation.get(field).
- Evaluate pr.update(d).
- Set pr.invoice\_limit from 1000.
- Set pr.payment\_limit from 1000.
- Return pr.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0138.json#L1123) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L795)

<a id="op-8cb2e30861e8c5"></a>
### Is job running

`operation_enterprise_accounts_record_definitions_process_payment_reconciliation_business_behavior_is_job_running`

**Inputs** job\_name.

**Declared result** bool.

**Explicit results** job\_name belongs to get\_jobs(site = Platform.local.site, key = “job\_name”) at Platform.local.site.

**Local steps**

- Return job\_name belongs to get\_jobs(site = Platform.local.site, key = “job\_name”) at Platform.local.site.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L798)
