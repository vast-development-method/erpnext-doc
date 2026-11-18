# Accounting and settlement · operations 114

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Tax withholding entry

[Record definition](../../../../data/record-types/tax_withholding_entry.json)

<a id="op-e34c502a2d5623"></a>
### Tax Withholding Controller.reverse ldc entry

`operation_enterprise_binding_enterprise_accounts_doctype_tax_withholding_entry_tax_withholding_entry_taxwithholdingcontroller_reverse_ldc_entry`

**Inputs** self, current\_entry, ldc\_entry, category.

**Declared result** list.

**Explicit results** self.\_merge\_entries(deque(list(ldc\_part)), deque(), category, tax\_rate = ldc\_entry.tax\_rate, default\_obj = mapping(“under\_withheld\_reason” → “Lower Deduction Certificate”, “lower\_deduction\_certificate” → l ….

**Local steps**

- Set ldc\_part from current\_entry.copy().
- Set ldc\_part.taxable\_amount from max(current\_entry.taxable\_amount, negative ldc\_entry.taxable\_amount).
- Update current\_entry.taxable\_amount using − ldc\_part.taxable\_amount.
- Return self.\_merge\_entries(deque(list(ldc\_part)), deque(), category, tax\_rate = ldc\_entry.tax\_rate, default\_obj = mapping(“under\_withheld\_reason” → “Lower Deduction Certificate”, “lower\_deduction\_certificate” → l ….

**Methods declared on this owner** [merge entries](operations-114.md#op-84c72bb7bb4b28).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1090)

<a id="op-c6358da7ebb3c7"></a>
### Tax Withholding Controller.get original ldc entries

`operation_enterprise_binding_enterprise_accounts_doctype_tax_withholding_entry_tax_withholding_entry_taxwithholdingcontroller_get_original_ldc_entries`

**Inputs** self, category.

**Declared result** list.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(entry.lower\_deduction\_certificate).orderby(entry.tax\_rate).run(as\_dict = true).

**Local steps**

- Set entry from Platform.qb.DocType(DOCTYPE).
- Set taxable\_amount from Sum(entry.taxable\_amount).
- Return nested operand in the contract(nested operand in the contract).orderby(entry.lower\_deduction\_certificate).orderby(entry.tax\_rate).run(as\_dict = true).

**Methods declared on this owner** [get original and return names](operations-114.md#op-fab9ec282e053a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1087)

<a id="op-fab9ec282e053a"></a>
### Tax Withholding Controller.get original and return names

`operation_enterprise_binding_enterprise_accounts_doctype_tax_withholding_entry_tax_withholding_entry_taxwithholdingcontroller_get_original_and_return_names`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read self.doc.doctype via get\_all.

**Explicit results** list(self.doc.return\_against, expanded returns).

**Local steps**

- Set returns from Platform.get\_all(self.doc.doctype, filters = mapping(“return\_against” → self.doc.return\_against, “docstatus” → 1), pluck = “name”).
- Return list(self.doc.return\_against, expanded returns).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1086)

<a id="op-e2e35de2aba826"></a>
### Tax Withholding Controller.update taxable amounts

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_update_taxable_amounts`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.doc.base\_net\_total.
  - Return no value.
- Evaluate self.\_update\_amount\_for\_item().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update amount for item](operations-114.md#op-3800b24f8cc283).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L592) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L488)

<a id="op-3800b24f8cc283"></a>
### Tax Withholding Controller.update amount for item

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_update_amount_for_item`

**Inputs** self.

**Local steps**

- Set precision from self.doc.precision(“base\_net\_rate”, “items”).
- Evaluate self.\_update\_item\_wise\_tax\_amount().
- For each item in self.doc.get(“items”).
  - If not (item.apply\_tds and item.tax\_withholding\_category).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.apply\_tds → item.tax\_withholding\_category.
    - Continue with the next iteration or loop test.
  - Set category from self.category\_details.get(item.tax\_withholding\_category).
  - If category.tax\_deduction\_basis differs from “Gross Total”.
    - Set taxable\_amount from item.base\_net\_amount.
  - Otherwise.
    - Set taxable\_amount from (item.base\_net\_amount + item.\_item\_total\_tax\_amount).
  - Set taxable\_amount from flt(taxable\_amount, precision).
  - Set item.\_base\_tax\_withholding\_net\_total from taxable\_amount.
  - Update category at “taxable\_amount” using + flt(taxable\_amount, precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update item wise tax amount](operations-114.md#op-e5c0d64213066f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L671) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L485)

<a id="op-e5c0d64213066f"></a>
### Tax Withholding Controller.update item wise tax amount

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_update_item_wise_tax_amount`

**Inputs** self.

**Local steps**

- For each item in self.doc.get(“items”).
  - Set item.\_item\_total\_tax\_amount from 0.
- Set precision from self.doc.precision(“tax\_amount”, “taxes”).
- For each row in self.doc.get(“\_item\_wise\_tax\_details”, list()).
  - Set item from row.item.
  - If not (item.apply\_tds and item.tax\_withholding\_category).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.apply\_tds → item.tax\_withholding\_category.
    - Continue with the next iteration or loop test.
  - If row.tax.is\_tax\_withholding\_account.
    - Continue with the next iteration or loop test.
  - Set item.\_item\_total\_tax\_amount from flt((item.\_item\_total\_tax\_amount + row.amount), precision).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L1040) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L486)

<a id="op-a112b4e9cd2be7"></a>
### Tax Withholding Controller.evaluate thresholds

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_evaluate_thresholds`

**Inputs** self.

**Local steps**

- For each category in self.category\_details.values().
  - Set category.threshold\_crossed from self.\_is\_threshold\_crossed\_for\_category(category).
  - Set category.unused\_threshold from self.\_get\_unused\_threshold(category).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is threshold crossed for category](operations-114.md#op-db1ca5653cd369), [get unused threshold](operations-114.md#op-2da820d9cf0352).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L1335) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L89) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L461)

<a id="op-db1ca5653cd369"></a>
### Tax Withholding Controller.is threshold crossed for category

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_is_threshold_crossed_for_category`

**Inputs** self, category.

**Explicit results** true · category.taxable\_amount ≥ category.single\_threshold · self.\_check\_historical\_threshold\_status(category).

**Local steps**

- If self.doc.ignore\_tax\_withholding\_threshold.
  - Return true.
- If category.disable\_cumulative\_threshold.
  - Return category.taxable\_amount ≥ category.single\_threshold.
- If category.cumulative\_threshold equals 0.
  - Return true.
- If category.tax\_on\_excess\_amount.
  - Return true.
- Return self.\_check\_historical\_threshold\_status(category).

**Methods declared on this owner** [check historical threshold status](operations-114.md#op-4adf25391e9d6e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L1467) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L473)

<a id="op-4adf25391e9d6e"></a>
### Tax Withholding Controller.check historical threshold status

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_check_historical_threshold_status`

**Inputs** self, category.

**Explicit results** true · category.taxable\_amount ≥ remaining\_threshold.

**Local steps**

- Set entry from Platform.qb.DocType(DOCTYPE).
- Set result from Platform.\_dict(nested operand in the contract.\_base\_threshold\_query(category).where(nested operand in the contract.status.isin(list(“Settled”, “Under Withheld”))).run()).
- If result.get(“Settled”, 0) &gt; 0.
  - Return true.
- Set remaining\_threshold from (category.cumulative\_threshold − result.get(“Under Withheld”, 0)).
- If not category.disable\_transaction\_threshold.
  - Set remaining\_threshold from min(remaining\_threshold, category.single\_threshold).
- Return category.taxable\_amount ≥ remaining\_threshold.

**Methods declared on this owner** [base threshold query](operations-114.md#op-52606a9022a9df).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L1650) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L452)

<a id="op-2da820d9cf0352"></a>
### Tax Withholding Controller.get unused threshold

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_unused_threshold`

**Inputs** self, category.

**Explicit results** 0 · (category.cumulative\_threshold − result.get(“Settled”, 0)).

**Local steps**

- If not category.tax\_on\_excess\_amount.
  - Return 0.
- Set entry from Platform.qb.DocType(DOCTYPE).
- Set result from Platform.\_dict(nested operand in the contract.\_base\_threshold\_query(category).where(IfNull(nested operand in the contract.under\_withheld\_reason, empty text) equals “Threshold Exemption”).run()).
- Return (category.cumulative\_threshold − result.get(“Settled”, 0)).

**Methods declared on this owner** [base threshold query](operations-114.md#op-52606a9022a9df).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L1992) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L470)

<a id="op-52606a9022a9df"></a>
### Tax Withholding Controller.base threshold query

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_base_threshold_query`

**Inputs** self, category.

**Explicit results** query.

**Local steps**

- Set entry from Platform.qb.DocType(DOCTYPE).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(entry.taxable\_date.between(category.from\_date, category.to\_date)).groupby(entry.status).
- Set query from query.where(entry.tax\_id equals category.tax\_id) when category.tax\_id, otherwise query.where(entry.party equals self.party).
  - Value choice on category.tax\_id — true gives query.where(entry.tax\_id equals category.tax\_id), false gives query.where(entry.party equals self.party).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L2234) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L447)

<a id="op-e832668badeada"></a>
### Tax Withholding Controller.get historical entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_historical_entries`

**Inputs** self, category.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.between(nested operand in the contract.from\_date, nested operand in the contract.to\_date)).union(over\_wit ….

**Local steps**

- Set entry from Platform.qb.DocType(DOCTYPE).
- Set base\_query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.party equals nested operand in the contract.party).where(entry.company equals self.doc.company).where(ent ….
- Set over\_withheld\_query from base\_query.where(entry.status equals “Over Withheld”).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.between(nested operand in the contract.from\_date, nested operand in the contract.to\_date)).union(over\_wit ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L2715) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L467)

<a id="op-6a8e184a8a5e35"></a>
### Tax Withholding Controller.get linked payments

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_linked_payments`

**Inputs** self.

**Explicit results** references.

**Local steps**

- Set references from Platform.\_dict().
- For each ref in self.doc.advances.
  - Set key from tuple(ref.reference\_type, ref.reference\_name).
  - Set references at key from (ref.allocated\_amount × self.doc.conversion\_rate).
- Return references.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L3180) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L468)

<a id="op-753b555ec11a26"></a>
### Tax Withholding Controller.create default entry

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_create_default_entry`

**Inputs** self, category.

**Explicit results** Platform.\_dict(mapping(“company” → self.doc.company, “party\_type” → self.party\_type, “party” → self.party, “tax\_id” → category.tax\_id, …)).

**Local steps**

- Return Platform.\_dict(mapping(“company” → self.doc.company, “party\_type” → self.party\_type, “party” → self.party, “tax\_id” → category.tax\_id, …)).

**Methods declared on this owner** [get conversion rate](operations-115.md#op-7c7cb348569578).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L3335) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L84) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L456)

<a id="op-3de1299632b25a"></a>
### Tax Withholding Controller.update tax rows

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_update_tax_rows`

**Inputs** self.

**Local steps**

- Set account\_amount\_map from self.\_calculate\_account\_wise\_amount().
- Set category\_withholding\_map from self.\_get\_category\_withholding\_map().
- Set existing\_taxes from mapping of row.account\_head → row for row drawn from self.doc.taxes where row.is\_tax\_withholding\_account.
  - Draw row from self.doc.taxes, keep a combination only if (row.is\_tax\_withholding\_account).
- Set precision from self.doc.precision(“tax\_amount”, “taxes”).
- Set conversion\_rate from self.get\_conversion\_rate().
- Set add\_deduct\_tax from “Deduct”.
- If self.party\_type equals “Customer”.
  - Set add\_deduct\_tax from “Add”.
- For each tuple(account\_head, base\_amount) in account\_amount\_map.items().
  - Set tax\_amount from flt((base\_amount ÷ conversion\_rate), precision).
  - If not tax\_amount.
    - Continue with the next iteration or loop test.
  - If existing\_tax bound to existing\_taxes.get(account\_head).
    - Set existing\_tax.tax\_amount from tax\_amount.
    - Set existing\_tax.dont\_recompute\_tax from 1.
    - Set tax\_row from existing\_tax.
    - Set for\_update from true.
  - Otherwise.
    - Set tax\_row from self.\_create\_tax\_row(account\_head, tax\_amount).
    - Set for\_update from false.
  - Set tax\_row.add\_deduct\_tax from add\_deduct\_tax.
  - Evaluate self.\_set\_item\_wise\_tax\_for\_tds(tax\_row, account\_head, category\_withholding\_map, for\_update = for\_update).
- Evaluate self.\_remove\_zero\_tax\_rows().
- Evaluate self.calculate\_taxes\_and\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate account wise amount](operations-114.md#op-60e4c93a9a8c93), [get category withholding map](operations-114.md#op-04fab44dd8ed1b), [get conversion rate](operations-115.md#op-7c7cb348569578), [create tax row](operations-114.md#op-5e33530e6c17c3), [set item wise tax for tds](operations-114.md#op-97bc10e716f0a0), [remove zero tax rows](operations-114.md#op-c444bef6e3132a), [calculate taxes and totals](operations-115.md#op-8a27df125d28f8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L3753) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L487)

<a id="op-5e33530e6c17c3"></a>
### Tax Withholding Controller.create tax row

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_create_tax_row`

**Inputs** self, account\_head, tax\_amount.

**Explicit results** self.doc.append(“taxes”, mapping(“is\_tax\_withholding\_account” → 1, “category” → “Total”, “charge\_type” → “Actual”, “account\_head” → account\_head, …)).

**Local steps**

- Set cost\_center from (self.doc.cost\_center or Enterprise.get\_default\_cost\_center(self.doc.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.cost\_center → Enterprise.get\_default\_cost\_center(self.doc.company).
- Return self.doc.append(“taxes”, mapping(“is\_tax\_withholding\_account” → 1, “category” → “Total”, “charge\_type” → “Actual”, “account\_head” → account\_head, …)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L4355) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L86) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L458)

<a id="op-97bc10e716f0a0"></a>
### Tax Withholding Controller.set item wise tax for tds

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_set_item_wise_tax_for_tax_deducted_at_source`

**Inputs** self, tax\_row, account\_head, category\_withholding\_map, for\_update = false.

**Explicit results** no value.

**Local steps**

- Set categories\_for\_account from list of cat for cat drawn from self.category\_details.values() where cat.account\_head equals account\_head.
  - Draw cat from self.category\_details.values(), keep a combination only if (cat.account\_head equals account\_head).
- If not categories\_for\_account.
  - Return no value.
- If not hasattr(self.doc, “\_item\_wise\_tax\_details”).
  - Set self.doc.\_item\_wise\_tax\_details from list().
- If for\_update.
  - Set self.doc.\_item\_wise\_tax\_details from list of d for d drawn from self.doc.\_item\_wise\_tax\_details where d.get(“tax”) differs from tax\_row.
    - Draw d from self.doc.\_item\_wise\_tax\_details, keep a combination only if (d.get(“tax”) differs from tax\_row).
- Set items from (self.doc.get(“items”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(“items”) → list().
- Set category\_totals from mapping().
- For each item in items.
  - If (item.apply\_tds and item.tax\_withholding\_category).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.apply\_tds → item.tax\_withholding\_category.
    - Set item\_taxable from item.get(“\_base\_tax\_withholding\_net\_total”, 0).
    - Set category\_totals at item.tax\_withholding\_category from (category\_totals.get(item.tax\_withholding\_category, 0) + item\_taxable).
- Set precision from self.doc.precision(“tax\_amount”, “taxes”).
- For each item in items.
  - If not (item.apply\_tds and item.tax\_withholding\_category).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.apply\_tds → item.tax\_withholding\_category.
    - Continue with the next iteration or loop test.
  - Set category from self.category\_details.get(item.tax\_withholding\_category).
  - If (not category or category.account\_head differs from account\_head).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not category → category.account\_head differs from account\_head.
    - Continue with the next iteration or loop test.
  - Set item\_base\_taxable from (item.get(“\_base\_tax\_withholding\_net\_total”) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“\_base\_tax\_withholding\_net\_total”) → 0.
  - If (not category.taxable\_amount or not item\_base\_taxable).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not category.taxable\_amount → not item\_base\_taxable.
    - Continue with the next iteration or loop test.
  - Set total\_taxable\_amount from category\_totals.get(category.name, 0).
  - If (category.unused\_threshold and total\_taxable\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in category.unused\_threshold → total\_taxable\_amount.
    - Set item\_threshold\_deduction from ((item\_base\_taxable ÷ total\_taxable\_amount) × category.unused\_threshold).
    - Set item\_effective\_taxable from max(0, (item\_base\_taxable − item\_threshold\_deduction)).
  - Otherwise.
    - Set item\_effective\_taxable from item\_base\_taxable.
  - Set withholding\_amount from category\_withholding\_map.get(category.name, 0).
  - If (withholding\_amount and category.taxable\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in withholding\_amount → category.taxable\_amount.
    - Set item\_proportion from (item\_effective\_taxable ÷ category.taxable\_amount).
    - Set item\_tax\_amount from flt((withholding\_amount × item\_proportion), precision).
  - Otherwise.
    - Set item\_tax\_amount from 0.
  - Set multiplier from negative 1 when tax\_row.add\_deduct\_tax equals “Deduct”, otherwise 1.
    - Value choice on tax\_row.add\_deduct\_tax equals “Deduct” — true gives negative 1, false gives 1.
  - Evaluate self.doc.\_item\_wise\_tax\_details.append(Platform.\_dict(item = item, tax = tax\_row, rate = category.tax\_rate, amount = (item\_tax\_amount × multiplier), …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L4623) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L483)

<a id="op-04fab44dd8ed1b"></a>
### Tax Withholding Controller.get category withholding map

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_category_withholding_map`

**Inputs** self.

**Explicit results** category\_withholding\_map.

**Local steps**

- Set category\_withholding\_map from defaultdict(float).
- For each entry in self.doc.tax\_withholding\_entries.
  - If entry.withholding\_name differs from self.doc.name.
    - Continue with the next iteration or loop test.
  - Update category\_withholding\_map at entry.tax\_withholding\_category using + entry.withholding\_amount.
- Return category\_withholding\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L5790) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L465)

<a id="op-60e4c93a9a8c93"></a>
### Tax Withholding Controller.calculate account wise amount

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_calculate_account_wise_amount`

**Inputs** self.

**Explicit results** account\_amount\_map.

**Local steps**

- Set account\_amount\_map from defaultdict(float).
- For each entry in self.doc.tax\_withholding\_entries.
  - If entry.withholding\_name differs from self.doc.name.
    - Continue with the next iteration or loop test.
  - Set category from self.category\_details.get(entry.tax\_withholding\_category).
  - Update account\_amount\_map at category.account\_head using + entry.withholding\_amount.
- Return account\_amount\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L5942) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L77) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L449)

<a id="op-c444bef6e3132a"></a>
### Tax Withholding Controller.remove zero tax rows

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_remove_zero_tax_rows`

**Inputs** self.

**Local steps**

- Set self.doc.taxes from list of row for row drawn from self.doc.taxes where not (row.is\_tax\_withholding\_account and not row.tax\_amount).
  - Draw row from self.doc.taxes, keep a combination only if (not (row.is\_tax\_withholding\_account and not row.tax\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_tax\_withholding\_account → not row.tax\_amount.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L6131) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L482)

<a id="op-69efb152f6ffb9"></a>
### Tax Withholding Controller.adjust under over withheld

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_adjust_under_over_withheld`

**Inputs** self, under\_entries, over\_entries, category.

**Explicit results** list() · merged\_entries.

**Local steps**

- If not (under\_entries and over\_entries).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in under\_entries → over\_entries.
  - Return list().
- Set merged\_entries from list().
- While (under\_entries and over\_entries).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in under\_entries → over\_entries.
  - Set under from under\_entries at 0.
  - Set over from over\_entries at 0.
  - Set tax\_rate from over.tax\_rate.
  - Set tax\_amount from self.compute\_withheld\_amount(under.taxable\_amount, tax\_rate, round\_off\_tax\_amount = category.round\_off\_tax\_amount).
  - Set tax\_amount from flt(min(tax\_amount, over.withholding\_amount), self.precision).
  - If tax\_rate equals 0.
    - Set taxable\_amount from min(under.taxable\_amount, over.taxable\_amount).
  - Otherwise.
    - Set taxable\_amount from flt(((100 ÷ tax\_rate) × tax\_amount), self.precision).
  - Set merged\_entry from under.copy().
  - Evaluate merged\_entry.update(mapping(“taxable\_amount” → taxable\_amount, “withholding\_amount” → tax\_amount, “withholding\_doctype” → over.withholding\_doctype, “withholding\_name” → over.withholding\_name, …)).
  - If self.\_should\_include\_entry(merged\_entry).
    - Evaluate merged\_entries.append(merged\_entry).
  - Update under.taxable\_amount using − taxable\_amount.
  - Update over.withholding\_amount using − tax\_amount.
  - If flt(under.taxable\_amount, self.precision) ≤ 0.
    - Evaluate under\_entries.popleft().
  - If flt(over.withholding\_amount, self.precision) ≤ 0.
    - Evaluate over\_entries.popleft().
- Return merged\_entries.

**Methods declared on this owner** [compute withheld amount](operations-115.md#op-00dbac452ee486), [should include entry](operations-115.md#op-6aff5e22ca2dfe).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L6239) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L74) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L446)

<a id="op-84c72bb7bb4b28"></a>
### Tax Withholding Controller.merge entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_merge_entries`

**Inputs** self, under\_entries, over\_entries, category, tax\_rate = no value, constraint = inf, default\_obj = no value.

**Explicit results** merged\_entries.

**Local steps**

- Set merged\_entries from list().
- If not ((under\_entries or over\_entries) and constraint &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (under\_entries or over\_entries) → constraint &gt; 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in under\_entries → over\_entries.
  - Return merged\_entries.
- If tax\_rate is identical to no value.
  - Set tax\_rate from category.tax\_rate.
- Set constraint from self.\_process\_under\_withheld\_entries(under\_entries, category, tax\_rate, constraint, …).
- Evaluate self.\_process\_over\_withheld\_entries(over\_entries, category, tax\_rate, constraint, …).
- Return merged\_entries.

**Methods declared on this owner** [process under withheld entries](operations-114.md#op-6d1803ad242271), [process over withheld entries](operations-114.md#op-476d6a16a6710a).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L7054) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L474)

<a id="op-6d1803ad242271"></a>
### Tax Withholding Controller.process under withheld entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_process_under_withheld_entries`

**Inputs** self, under\_entries, category, tax\_rate, constraint, default\_obj, merged\_entries.

**Explicit results** constraint.

**Local steps**

- While (under\_entries and constraint &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in under\_entries → constraint &gt; 0.
  - Set entry from under\_entries at 0.
  - Set value\_direction from negative 1 when entry.taxable\_amount &lt; 0, otherwise 1.
    - Value choice on entry.taxable\_amount &lt; 0 — true gives negative 1, false gives 1.
  - Set amount\_to\_process from min(entry.taxable\_amount, constraint).
  - If (amount\_to\_process × value\_direction) ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set merged\_entry from self.\_create\_base\_entry(entry, category, tax\_rate, default\_obj).
  - Evaluate merged\_entry.update(mapping(“taxable\_amount” → flt(amount\_to\_process, self.precision), “withholding\_amount” → self.compute\_withheld\_amount(amount\_to\_process, tax\_rate, round\_off\_tax\_amount = category.round ….
  - Evaluate merged\_entries.append(merged\_entry).
  - Update entry.taxable\_amount using − amount\_to\_process.
  - If flt((entry.taxable\_amount × value\_direction), self.precision) ≤ 0.
    - Evaluate under\_entries.popleft().
  - Update constraint using − amount\_to\_process.
- Return constraint.

**Methods declared on this owner** [create base entry](operations-115.md#op-6a037ced128185), [compute withheld amount](operations-115.md#op-00dbac452ee486).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L480)

<a id="op-476d6a16a6710a"></a>
### Tax Withholding Controller.process over withheld entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_process_over_withheld_entries`

**Inputs** self, over\_entries, category, tax\_rate, constraint, default\_obj, merged\_entries.

**Explicit results** constraint.

**Local steps**

- While (over\_entries and constraint &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in over\_entries → constraint &gt; 0.
  - Set entry from over\_entries at 0.
  - Set value\_direction from negative 1 when entry.taxable\_amount &lt; 0, otherwise 1.
    - Value choice on entry.taxable\_amount &lt; 0 — true gives negative 1, false gives 1.
  - Set amount\_to\_process from min(entry.taxable\_amount, constraint).
  - If (amount\_to\_process × value\_direction) ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set merged\_entry from self.\_create\_base\_entry(entry, category, tax\_rate, default\_obj).
  - Evaluate merged\_entry.update(mapping(“taxable\_amount” → flt(amount\_to\_process, self.precision), “withholding\_amount” → self.compute\_withheld\_amount(amount\_to\_process, tax\_rate, round\_off\_tax\_amount = category.round ….
  - If self.\_should\_include\_entry(merged\_entry).
    - Evaluate merged\_entries.append(merged\_entry).
  - Update entry.taxable\_amount using − amount\_to\_process.
  - If flt((entry.taxable\_amount × value\_direction), self.precision) ≤ 0.
    - Evaluate over\_entries.popleft().
  - Update constraint using − amount\_to\_process.
- Return constraint.

**Methods declared on this owner** [create base entry](operations-115.md#op-6a037ced128185), [compute withheld amount](operations-115.md#op-00dbac452ee486), [get conversion rate](operations-115.md#op-7c7cb348569578), [should include entry](operations-115.md#op-6aff5e22ca2dfe).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L601) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L479)
