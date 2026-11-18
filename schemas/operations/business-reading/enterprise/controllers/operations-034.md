# Shared transaction rules · operations 34

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Taxes and totals

<a id="op-0d91de14fc41c1"></a>
### Calculate taxes and totals.get billed qty

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_get_billed_qty`

**Inputs** self, item.

**Explicit results** flt(item.qty) · (flt(item.qty) + flt(item.rejected\_qty)).

**Local steps**

- If (not flt(item.get(“rejected\_qty”)) or not bills\_rejected\_quantity(self.doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not flt(item.get(“rejected\_qty”)) → not bills\_rejected\_quantity(self.doc).
  - Return flt(item.qty).
- Return (flt(item.qty) + flt(item.rejected\_qty)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L455)

<a id="op-ab4be3a81be9c4"></a>
### Calculate taxes and totals.has mapped discount

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_has_mapped_discount`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (not self.doc.get(“is\_consolidated”) and any(generator of item.get(“mapped\_additional\_discount\_amount”) for item drawn from self.\_items)).

**Local steps**

- Return (not self.doc.get(“is\_consolidated”) and any(generator of item.get(“mapped\_additional\_discount\_amount”) for item drawn from self.\_items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.doc.get(“is\_consolidated”) → any(generator of item.get(“mapped\_additional\_discount\_amount”) for item drawn from self.\_items).
  - Draw item from self.\_items.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L457)

<a id="op-be2d44920d8944"></a>
### Calculate taxes and totals.apply mapped additional discount

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_apply_mapped_additional_discount`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The cash or non-trade discount cannot be combined with discounts carried from other documents.”.

**Local steps**

- If (self.discount\_amount\_applied or not self.has\_mapped\_discount).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.discount\_amount\_applied → not self.has\_mapped\_discount.
  - Return no value.
- If self.doc.get(“is\_cash\_or\_non\_trade\_discount”).
  - Call the validation error handler Platform.throw(translated “The cash or non-trade discount cannot be combined with discounts carried from other documents.”, title = translated “Discounts Cannot Be Combined”).
- For each item in self.\_items.
  - Evaluate self.apply\_mapped\_discount\_to\_item(item).
- Set self.doc.apply\_discount\_on from “Net Total”.
- Set self.doc.additional\_discount\_percentage from 0.
- Set self.doc.discount\_amount from flt(sum(generator of flt(item.distributed\_discount\_amount) for item drawn from self.\_items), self.doc.precision(“discount\_amount”)).
  - Draw item from self.\_items.
- Evaluate self.\_set\_in\_company\_currency(self.doc, list(“discount\_amount”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply mapped discount to item](operations-034.md#op-955c6ad4099cf2), [set in company currency](operations-034.md#op-2605086ca20dec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L452)

<a id="op-955c6ad4099cf2"></a>
### Calculate taxes and totals.apply mapped discount to item

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_apply_mapped_discount_to_item`

**Inputs** self, item.

**Explicit results** no value.

**Local steps**

- Set item.distributed\_discount\_amount from flt((flt(item.mapped\_additional\_discount\_amount) × get\_qty\_in\_stock\_uom(item)), item.precision(“distributed\_discount\_amount”)).
- If not item.distributed\_discount\_amount.
  - Return no value.
- Set item.net\_amount from flt((item.net\_amount − item.distributed\_discount\_amount), item.precision(“net\_amount”)).
- Set item.net\_rate from flt((item.net\_amount ÷ self.get\_billed\_qty(item)), item.precision(“net\_rate”)).
- Set item.\_unrounded\_net\_amount from no value.
- Evaluate self.\_set\_in\_company\_currency(item, list(“net\_rate”, “net\_amount”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get billed qty](operations-034.md#op-0d91de14fc41c1), [set in company currency](operations-034.md#op-2605086ca20dec).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L453)

<a id="op-2605086ca20dec"></a>
### Calculate taxes and totals.set in company currency

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_set_in_company_currency`

**Inputs** self, doc, fields.

**Local steps**

- For each f in fields.
  - Set val from flt((flt(doc.get(f), doc.precision(f)) × self.doc.conversion\_rate), doc.precision((“base\_” + f))).
  - Evaluate doc.set((“base\_” + f), val).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0401.json#L3331) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L800)

<a id="op-2f6a2c6aa66370"></a>
### Calculate taxes and totals.initialize taxes

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_initialize_taxes`

**Inputs** self.

**Local steps**

- Evaluate self.reset\_item\_wise\_tax\_details().
- For each tax in self.doc.get(“taxes”).
  - If not self.discount\_amount\_applied.
    - Evaluate validate\_taxes\_and\_charges(tax).
    - Evaluate validate\_inclusive\_tax(tax, self.doc).
  - Set tax\_fields from list(“net\_amount”, “total”, “tax\_amount\_after\_discount\_amount”, “tax\_amount\_for\_current\_item”, …).
  - If (tax.charge\_type differs from “Actual” and not (self.discount\_amount\_applied and self.doc.apply\_discount\_on equals “Grand Total”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type differs from “Actual” → not (self.discount\_amount\_applied and self.doc.apply\_discount\_on equals “Grand Total”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.discount\_amount\_applied → self.doc.apply\_discount\_on equals “Grand Total”.
    - Evaluate tax\_fields.append(“tax\_amount”).
  - For each fieldname in tax\_fields.
    - Evaluate tax.set(fieldname, 0.0).
  - Evaluate self.doc.round\_floats\_in(tax).

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset item wise tax details](operations-034.md#op-6758678bf2b2f7).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0401.json#L3541) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L791)

<a id="op-6758678bf2b2f7"></a>
### Calculate taxes and totals.reset item wise tax details

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_reset_item_wise_tax_details`

**Inputs** self.

**Local steps**

- Set self.doc.update\_item\_wise\_tax\_details from true.
- Set dont\_recompute\_taxes from list of d for d drawn from self.doc.get(“taxes”) where d.get(“dont\_recompute\_tax”).
  - Draw d from self.doc.get(“taxes”), keep a combination only if (d.get(“dont\_recompute\_tax”)).
- Set item\_wise\_tax\_details from list().
- For each row in (self.doc.get(“\_item\_wise\_tax\_details”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(“\_item\_wise\_tax\_details”) → list().
  - Set tax from row.get(“tax”).
  - If tax belongs to dont\_recompute\_taxes.
    - Evaluate item\_wise\_tax\_details.append(row).
- Set self.doc.\_item\_wise\_tax\_details from item\_wise\_tax\_details.
- Set self.doc.item\_wise\_tax\_details from list().
- For each tax in self.doc.get(“taxes”).
  - If not tax.get(“dont\_recompute\_tax”).
    - Set tax.\_running\_txn\_tax\_total from 0.0.
    - Set tax.\_running\_base\_tax\_total from 0.0.
    - Set tax.\_running\_txn\_taxable\_total from 0.0.
    - Set tax.\_running\_base\_taxable\_total from 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0401.json#L3929) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L795)

<a id="op-25479e96ef1b0e"></a>
### Calculate taxes and totals.determine exclusive rate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_determine_exclusive_rate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not any(generator of cint(tax.included\_in\_print\_rate) for tax drawn from self.doc.get(“taxes”)).
  - Draw tax from self.doc.get(“taxes”).
  - Return no value.
- Set net\_totals from mapping().
- For each item in self.doc.items.
  - If not self.discount\_amount\_applied.
    - Set item.\_unrounded\_net\_amount from no value.
  - Set item\_tax\_map from self.\_load\_item\_tax\_rate(item.item\_tax\_rate).
  - Set total\_tax\_slope from 0.
  - Set total\_tax\_intercept from 0.
  - For each tuple(i, tax) in enumerate(self.doc.get(“taxes”)).
    - Set tuple(tax.tax\_fraction\_for\_current\_item, tax\_intercept\_per\_qty) from self.get\_current\_tax\_fraction(tax, item\_tax\_map, item).
    - Set tax.inclusive\_amount\_per\_qty from tax\_intercept\_per\_qty.
    - If i equals 0.
      - Set tax.grand\_total\_fraction\_for\_current\_item from (1 + tax.tax\_fraction\_for\_current\_item).
      - Set tax.grand\_total\_amount\_per\_qty from tax\_intercept\_per\_qty.
    - Otherwise.
      - Set prev from self.doc.get(“taxes”) at (i − 1).
      - Set tax.grand\_total\_fraction\_for\_current\_item from (prev.grand\_total\_fraction\_for\_current\_item + tax.tax\_fraction\_for\_current\_item).
      - Set tax.grand\_total\_amount\_per\_qty from (prev.grand\_total\_amount\_per\_qty + tax\_intercept\_per\_qty).
    - Update total\_tax\_slope using + tax.tax\_fraction\_for\_current\_item.
    - Update total\_tax\_intercept using + (tax\_intercept\_per\_qty × flt(item.qty)).
  - Set item.\_mapped\_discount\_inclusive\_amount from ((flt(item.get(“mapped\_additional\_discount\_amount”)) × get\_qty\_in\_stock\_uom(item)) × (1 + total\_tax\_slope)).
  - If (not self.discount\_amount\_applied and item.qty and (total\_tax\_slope or total\_tax\_intercept)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.discount\_amount\_applied → item.qty → (total\_tax\_slope or total\_tax\_intercept).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in total\_tax\_slope → total\_tax\_intercept.
    - Set amount from (flt(item.amount) − total\_tax\_intercept).
    - Set item.\_unrounded\_net\_amount from (amount ÷ (1 + total\_tax\_slope)).
    - Set item.net\_amount from flt(item.\_unrounded\_net\_amount, item.precision(“net\_amount”)).
    - If (not Platform.flags.round\_row\_wise\_tax and not (self.doc.doctype equals “Quotation” and item.get(“is\_alternative”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.round\_row\_wise\_tax → not (self.doc.doctype equals “Quotation” and item.get(“is\_alternative”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype equals “Quotation” → item.get(“is\_alternative”).
      - Set net\_total from net\_totals.setdefault(tuple(sorted(item\_tax\_map.items())), Platform.\_dict(unrounded = 0, rounded = 0)).
      - Update net\_total.unrounded using + item.\_unrounded\_net\_amount.
      - Set item.net\_amount from flt((flt(net\_total.unrounded, item.precision(“net\_amount”)) − net\_total.rounded), item.precision(“net\_amount”)).
      - Update net\_total.rounded using + item.net\_amount.
    - Set item.net\_rate from flt((item.net\_amount ÷ self.get\_billed\_qty(item)), item.precision(“net\_rate”)).
    - Set item.discount\_percentage from flt(item.discount\_percentage, item.precision(“discount\_percentage”)).
    - Evaluate self.\_set\_in\_company\_currency(item, list(“net\_rate”, “net\_amount”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [load item tax rate](operations-034.md#op-43db67a4d48489), [get current tax fraction](operations-034.md#op-3a12fd4f854adb), [get billed qty](operations-034.md#op-0d91de14fc41c1), [set in company currency](operations-034.md#op-2605086ca20dec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L781)

<a id="op-43db67a4d48489"></a>
### Calculate taxes and totals.load item tax rate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_load_item_tax_rate`

**Inputs** self, item\_tax\_rate.

**Explicit results** json.loads(item\_tax\_rate) when item\_tax\_rate, otherwise mapping().

**Local steps**

- Return json.loads(item\_tax\_rate) when item\_tax\_rate, otherwise mapping().
  - Value choice on item\_tax\_rate — true gives json.loads(item\_tax\_rate), false gives mapping().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L793)

<a id="op-3a12fd4f854adb"></a>
### Calculate taxes and totals.get current tax fraction

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_get_current_tax_fraction`

**Inputs** self, tax, item\_tax\_map, item.

**Explicit results** tuple(tax\_slope, tax\_intercept).

**Local steps**

- Set tax\_slope from 0.
- Set tax\_intercept from 0.
- If cint(tax.included\_in\_print\_rate).
  - Set tax\_rate from self.\_get\_tax\_rate(tax, item\_tax\_map).
  - If tax\_rate equals NOT\_APPLICABLE\_TAX.
    - Return tuple(tax\_slope, tax\_intercept).
  - If tax.charge\_type equals “On Net Total”.
    - Set tax\_slope from (tax\_rate ÷ 100.0).
  - Otherwise.
    - If tax.charge\_type equals “On Previous Row Amount”.
      - Set row from self.doc.get(“taxes”) at (cint(tax.row\_id) − 1).
      - Set tax\_slope from ((tax\_rate ÷ 100.0) × row.tax\_fraction\_for\_current\_item).
      - Set tax\_intercept from ((tax\_rate ÷ 100.0) × flt(getattr(row, “inclusive\_amount\_per\_qty”, 0))).
    - Otherwise.
      - If tax.charge\_type equals “On Previous Row Total”.
        - Set row from self.doc.get(“taxes”) at (cint(tax.row\_id) − 1).
        - Set tax\_slope from ((tax\_rate ÷ 100.0) × row.grand\_total\_fraction\_for\_current\_item).
        - Set tax\_intercept from ((tax\_rate ÷ 100.0) × flt(getattr(row, “grand\_total\_amount\_per\_qty”, 0))).
      - Otherwise.
        - If tax.charge\_type equals “On Item Quantity”.
          - Set tax\_intercept from flt(tax\_rate).
        - Otherwise.
          - Set qty from (flt(item.qty) or 1).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.qty) → 1.
          - Set base from self.get\_item\_taxable\_base(item, tax).
          - Set tax\_intercept from (((tax\_rate ÷ 100.0) × base) ÷ qty).
- If (getattr(tax, “add\_deduct\_tax”, no value) and tax.add\_deduct\_tax equals “Deduct”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(tax, “add\_deduct\_tax”, no value) → tax.add\_deduct\_tax equals “Deduct”.
  - Update tax\_slope using × negative 1.0.
  - Update tax\_intercept using × negative 1.0.
- Return tuple(tax\_slope, tax\_intercept).

**Methods declared on this owner** [get tax rate](operations-034.md#op-2a2efa4c685a79), [get item taxable base](operations-034.md#op-e1ff056469971e).

**Values supplied outside this operation** selected callable from getattr(row, “inclusive\_amount\_per\_qty”, 0), getattr(row, “grand\_total\_amount\_per\_qty”, 0) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0401.json#L5401) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L784)

<a id="op-2a2efa4c685a79"></a>
### Calculate taxes and totals.get tax rate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_get_tax_rate`

**Inputs** self, tax, item\_tax\_map.

**Explicit results** NOT\_APPLICABLE\_TAX · flt(rate, self.doc.precision(“rate”, tax)) · tax.rate.

**Local steps**

- If tax.account\_head belongs to item\_tax\_map.
  - Set rate from item\_tax\_map at tax.account\_head.
  - If rate equals NOT\_APPLICABLE\_TAX.
    - Return NOT\_APPLICABLE\_TAX.
  - Return flt(rate, self.doc.precision(“rate”, tax)).
- Return tax.rate.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0401.json#L6282) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L787)

<a id="op-b256ca60be3e62"></a>
### Calculate taxes and totals.calculate net total

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_net_total`

**Inputs** self.

**Local steps**

- Set self.doc.total\_qty, self.doc.total, self.doc.base\_total, self.doc.net\_total, self.doc.base\_net\_total from 0.0.
- For each item in self.\_items.
  - Update self.doc.total using + item.amount.
  - Update self.doc.total\_qty using + item.qty.
  - Update self.doc.base\_total using + item.base\_amount.
  - Update self.doc.net\_total using + item.net\_amount.
  - Update self.doc.base\_net\_total using + item.base\_net\_amount.
- Evaluate self.doc.round\_floats\_in(self.doc, list(“total”, “base\_total”, “net\_total”, “base\_net\_total”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0401.json#L6469) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L772)

<a id="op-87543aa01af067"></a>
### Calculate taxes and totals.calculate shipping charges

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_shipping_charges`

**Inputs** self.

**Record and data access** resolve a document from “Shipping Rule” via get\_doc.

**Explicit results** no value.

**Local steps**

- If self.doc.get(“is\_pos”).
  - Return no value.
- If (hasattr(self.doc, “shipping\_rule”) and self.doc.shipping\_rule).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self.doc, “shipping\_rule”) → self.doc.shipping\_rule.
  - Set shipping\_rule from Platform.get\_doc(“Shipping Rule”, self.doc.shipping\_rule).
  - Evaluate shipping\_rule.apply(self.doc).
  - Evaluate self.calculate\_discounted\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate discounted totals](operations-033.md#op-83ba640450407b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L775)

<a id="op-e678ec8c201c81"></a>
### Calculate taxes and totals.calculate taxes

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_taxes`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set self.grand\_total\_diff from 0.
- Set doc from self.doc.
- If not doc.get(“taxes”).
  - Return no value.
- Set actual\_tax\_dict from dict(list of list(tax.idx, flt(tax.tax\_amount, tax.precision(“tax\_amount”))) for tax drawn from doc.taxes where tax.charge\_type equals “Actual”).
  - Draw tax from doc.taxes, keep a combination only if (tax.charge\_type equals “Actual”).
- Evaluate self.set\_actual\_tax\_distribution().
- For each tuple(n, item) in enumerate(self.\_items).
  - Set item\_tax\_map from self.\_load\_item\_tax\_rate(item.item\_tax\_rate).
  - For each tuple(i, tax) in enumerate(doc.taxes).
    - Set tuple(current\_net\_amount, current\_tax\_amount) from self.get\_current\_tax\_and\_net\_amount(item, tax, item\_tax\_map).
    - If Platform.flags.round\_row\_wise\_tax.
      - Set current\_tax\_amount from flt(current\_tax\_amount, tax.precision(“tax\_amount”)).
      - Set current\_net\_amount from flt(current\_net\_amount, tax.precision(“net\_amount”)).
    - If tax.charge\_type equals “Actual”.
      - Update actual\_tax\_dict at tax.idx using − current\_tax\_amount.
      - If n equals self.\_actual\_tax\_distribution at tax.idx.last\_idx.
        - Update current\_tax\_amount using + actual\_tax\_dict at tax.idx.
    - If (tax.charge\_type differs from “Actual” and not (self.discount\_amount\_applied and self.doc.apply\_discount\_on equals “Grand Total”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type differs from “Actual” → not (self.discount\_amount\_applied and self.doc.apply\_discount\_on equals “Grand Total”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.discount\_amount\_applied → self.doc.apply\_discount\_on equals “Grand Total”.
      - Update tax.tax\_amount using + current\_tax\_amount.
      - Update tax.net\_amount using + current\_net\_amount.
    - Set tax.tax\_amount\_for\_current\_item from current\_tax\_amount.
    - Update tax.tax\_amount\_after\_discount\_amount using + current\_tax\_amount.
    - Set current\_tax\_amount from self.get\_tax\_amount\_if\_for\_valuation\_or\_deduction(current\_tax\_amount, tax).
    - If i equals 0.
      - Set tax.grand\_total\_for\_current\_item from flt((item.net\_amount + current\_tax\_amount)).
    - Otherwise.
      - Set tax.grand\_total\_for\_current\_item from flt((doc.taxes at (i − 1).grand\_total\_for\_current\_item + current\_tax\_amount)).
- Set discount\_amount\_applied from self.discount\_amount\_applied.
- If (doc.apply\_discount\_on equals “Grand Total” and (discount\_amount\_applied or doc.discount\_amount or doc.additional\_discount\_percentage)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.apply\_discount\_on equals “Grand Total” → (discount\_amount\_applied or doc.discount\_amount or doc.additional\_discount\_percentage).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in discount\_amount\_applied → doc.discount\_amount → doc.additional\_discount\_percentage.
  - Set tax\_amount\_precision from doc.taxes at 0.precision(“tax\_amount”).
  - For each tuple(i, tax) in enumerate(doc.taxes).
    - If discount\_amount\_applied.
      - Set tax.tax\_amount\_after\_discount\_amount from flt(tax.tax\_amount\_after\_discount\_amount, tax\_amount\_precision).
    - Evaluate self.set\_cumulative\_total(i, tax).
  - If not discount\_amount\_applied.
    - Set self.grand\_total\_for\_distributing\_discount from doc.taxes at negative 1.total.
  - Otherwise.
    - Set self.grand\_total\_diff from flt(((self.grand\_total\_for\_distributing\_discount − doc.discount\_amount) − doc.taxes at negative 1.total), doc.precision(“grand\_total”)).
- For each tuple(i, tax) in enumerate(doc.taxes).
  - Evaluate self.round\_off\_totals(tax).
  - Evaluate self.\_set\_in\_company\_currency(tax, list(“tax\_amount”, “tax\_amount\_after\_discount\_amount”, “net\_amount”)).
  - Evaluate self.round\_off\_base\_values(tax).
  - Evaluate self.set\_cumulative\_total(i, tax).
  - Evaluate self.\_set\_in\_company\_currency(tax, list(“total”)).
- Evaluate self.adjust\_rounding\_in\_item\_wise\_tax\_details().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set actual tax distribution](operations-034.md#op-0d3168b4def47e), [load item tax rate](operations-034.md#op-43db67a4d48489), [get current tax and net amount](operations-034.md#op-6036db5a1c7408), [get tax amount if for valuation or deduction](operations-034.md#op-2d41ddaf0ddcd7), [set cumulative total](operations-034.md#op-9eae27ce2849f5), [round off totals](operations-034.md#op-ca3d0a253455c9), [set in company currency](operations-034.md#op-2605086ca20dec), [round off base values](operations-034.md#op-e13c391d7347eb), [adjust rounding in item wise tax details](operations-034.md#op-87f78c692295fa).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L776)

<a id="op-0d3168b4def47e"></a>
### Calculate taxes and totals.set actual tax distribution

`operation_enterprise_binding_enterprise_controllers_taxes_and_totals_calculate_taxes_and_totals_set_actual_tax_distribution`

**Inputs** self.

**Local steps**

- Set self.\_actual\_tax\_distribution from mapping().
- Set item\_tax\_maps from list of self.\_load\_item\_tax\_rate(item.item\_tax\_rate) for item drawn from self.\_items.
  - Draw item from self.\_items.
- For each tax in self.doc.taxes.
  - If tax.charge\_type differs from “Actual”.
    - Continue with the next iteration or loop test.
  - Set tuple(net\_total, last\_idx) from tuple(0.0, no value).
  - For each tuple(n, item) in enumerate(self.\_items).
    - If self.\_get\_tax\_rate(tax, item\_tax\_maps at n) differs from NOT\_APPLICABLE\_TAX.
      - Update net\_total using + flt(item.net\_amount).
      - Set last\_idx from n.
  - If last\_idx is identical to no value.
    - Set last\_idx from (len(self.\_items) − 1).
  - Set self.\_actual\_tax\_distribution at tax.idx from Platform.\_dict(net\_total = net\_total, last\_idx = last\_idx).

If control reaches the end, it returns no value.

**Methods declared on this owner** [load item tax rate](operations-034.md#op-43db67a4d48489), [get tax rate](operations-034.md#op-2a2efa4c685a79).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L458)

<a id="op-87f78c692295fa"></a>
### Calculate taxes and totals.adjust rounding in item wise tax details

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_adjust_rounding_in_item_wise_tax_details`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated message.

**Local steps**

- If ignore\_item\_wise\_tax\_details(self.doc).
  - Return no value.
- If not self.doc.get(“\_item\_wise\_tax\_details”).
  - Return no value.
- Set invalid\_rows from list().
- For each tax in self.doc.taxes.
  - Set tax.\_total\_tax\_breakup from 0.
  - Set tax.\_last\_row\_idx from no value.
- For each tuple(idx, d) in enumerate(self.doc.\_item\_wise\_tax\_details).
  - Set tax from d.get(“tax”).
  - If (not tax or (tax.get(“charge\_type”) equals “Actual” and d.rate equals 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not tax → (tax.get(“charge\_type”) equals “Actual” and d.rate equals 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.get(“charge\_type”) equals “Actual” → d.rate equals 0.
    - Continue with the next iteration or loop test.
  - Update tax.\_total\_tax\_breakup using + (d.amount or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.amount → 0.
  - Set tax.\_last\_row\_idx from idx.
- For each tax in self.doc.taxes.
  - Set last\_idx from tax.\_last\_row\_idx.
  - If last\_idx is identical to no value.
    - Continue with the next iteration or loop test.
  - Set multiplier from negative 1 when tax.get(“add\_deduct\_tax”) equals “Deduct”, otherwise 1.
    - Value choice on tax.get(“add\_deduct\_tax”) equals “Deduct” — true gives negative 1, false gives 1.
  - Set expected\_amount from (tax.base\_tax\_amount\_after\_discount\_amount × multiplier).
  - Set actual\_breakup from tax.\_total\_tax\_breakup.
  - Set diff from flt((expected\_amount − actual\_breakup), 5).
  - If abs(diff) ≤ 1 when tax.precision(“tax\_amount”) equals 0, otherwise 0.5.
    - Value choice on tax.precision(“tax\_amount”) equals 0 — true gives 1, false gives 0.5.
    - Set detail\_row from self.doc.\_item\_wise\_tax\_details at last\_idx.
    - Set detail\_row at “amount” from flt((detail\_row at “amount” + diff), 5).
  - Otherwise.
    - Evaluate invalid\_rows.append(formatted text Row {tax.idx} (Difference: {diff})).
- If self.doc.flags.ignore\_validate.
  - Return no value.
- If invalid\_rows.
  - Set message from ((translated “Item Wise Tax Details do not match with Taxes and Charges at the following rows:” + text in the contract) + text in the contract.join(invalid\_rows)).
  - Call the validation error handler Platform.throw(translated message).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1096) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L765)

<a id="op-2d41ddaf0ddcd7"></a>
### Calculate taxes and totals.get tax amount if for valuation or deduction

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_get_tax_amount_if_for_valuation_or_deduction`

**Inputs** self, tax\_amount, tax.

**Explicit results** tax\_amount.

**Local steps**

- If getattr(tax, “category”, no value).
  - Set tax\_amount from 0.0 when tax.category equals “Valuation”, otherwise tax\_amount.
    - Value choice on tax.category equals “Valuation” — true gives 0.0, false gives tax\_amount.
  - If self.doc.doctype belongs to list(“Purchase Order”, “Purchase Invoice”, “Purchase Receipt”, “Supplier Quotation”).
    - Update tax\_amount using × negative 1.0 when tax.add\_deduct\_tax equals “Deduct”, otherwise 1.0.
      - Value choice on tax.add\_deduct\_tax equals “Deduct” — true gives negative 1.0, false gives 1.0.
- Return tax\_amount.

**Values supplied outside this operation** selected callable from getattr(tax, “category”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L2481) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L786)

<a id="op-9eae27ce2849f5"></a>
### Calculate taxes and totals.set cumulative total

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_set_cumulative_total`

**Inputs** self, row\_idx, tax.

**Local steps**

- Set tax\_amount from tax.tax\_amount\_after\_discount\_amount.
- Set tax\_amount from self.get\_tax\_amount\_if\_for\_valuation\_or\_deduction(tax\_amount, tax).
- If row\_idx equals 0.
  - Set tax.total from flt((self.doc.net\_total + tax\_amount), tax.precision(“total”)).
- Otherwise.
  - Set tax.total from flt((nested operand in the contract.doc.get(“taxes”) at (row\_idx − 1).total + tax\_amount), tax.precision(“total”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tax amount if for valuation or deduction](operations-034.md#op-2d41ddaf0ddcd7).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L2717) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L798)

<a id="op-6036db5a1c7408"></a>
### Calculate taxes and totals.get current tax and net amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_get_current_tax_and_net_amount`

**Inputs** self, item, tax, item\_tax\_map.

**Explicit results** tuple(current\_net\_amount, current\_tax\_amount).

**Local steps**

- Set tax\_rate from self.\_get\_tax\_rate(tax, item\_tax\_map).
- Set current\_tax\_amount from 0.0.
- Set current\_net\_amount from 0.0.
- If tax\_rate equals NOT\_APPLICABLE\_TAX.
  - Return tuple(current\_net\_amount, current\_tax\_amount).
- If tax.charge\_type equals “Actual”.
  - Set current\_net\_amount from item.net\_amount.
  - Set actual from flt(tax.tax\_amount, tax.precision(“tax\_amount”)).
  - Set distribution from self.\_actual\_tax\_distribution at tax.idx.
  - If distribution.net\_total.
    - Set current\_tax\_amount from ((item.net\_amount × actual) ÷ distribution.net\_total).
  - Otherwise.
    - If item is identical to self.\_items at distribution.last\_idx.
      - Set current\_tax\_amount from actual.
- Otherwise.
  - If tax.charge\_type equals “On Net Total”.
    - If tax.account\_head belongs to item\_tax\_map.
      - Set current\_net\_amount from item.net\_amount.
    - If (cint(tax.included\_in\_print\_rate) and item.\_unrounded\_net\_amount is distinct from no value).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(tax.included\_in\_print\_rate) → item.\_unrounded\_net\_amount is distinct from no value.
      - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × item.\_unrounded\_net\_amount).
    - Otherwise.
      - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × item.net\_amount).
  - Otherwise.
    - If tax.charge\_type equals “On Previous Row Amount”.
      - Set current\_net\_amount from self.doc.get(“taxes”) at (cint(tax.row\_id) − 1).tax\_amount\_for\_current\_item.
      - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × current\_net\_amount).
    - Otherwise.
      - If tax.charge\_type equals “On Previous Row Total”.
        - Set current\_net\_amount from self.doc.get(“taxes”) at (cint(tax.row\_id) − 1).grand\_total\_for\_current\_item.
        - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × current\_net\_amount).
      - Otherwise.
        - If tax.charge\_type equals “On Item Quantity”.
          - Set current\_tax\_amount from (tax\_rate × item.qty).
        - Otherwise.
          - Set base from self.get\_item\_taxable\_base(item, tax).
          - Set current\_net\_amount from base.
          - Set current\_tax\_amount from ((tax\_rate ÷ 100.0) × base).
- If not tax.get(“dont\_recompute\_tax”).
  - Evaluate self.set\_item\_wise\_tax(item, tax, tax\_rate, current\_tax\_amount, …).
- Return tuple(current\_net\_amount, current\_tax\_amount).

**Methods declared on this owner** [get tax rate](operations-034.md#op-2a2efa4c685a79), [get item taxable base](operations-034.md#op-e1ff056469971e), [set item wise tax](operations-034.md#op-f49260c136ad46).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L783)

<a id="op-e1ff056469971e"></a>
### Calculate taxes and totals.get item taxable base

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_get_item_taxable_base`

**Inputs** self, item, tax.

**Explicit results** flt(Platform.get\_attr(method)(self, item, tax)) · flt(item.net\_amount).

**Local steps**

- Set resolvers from (Platform.get\_hooks(“Enterprise\_taxable\_base\_resolvers”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“Enterprise\_taxable\_base\_resolvers”) → mapping().
- Set path from resolvers.get(tax.charge\_type).
- If path.
  - Set method from path at negative 1 when isinstance(path, (list bitwise or tuple)), otherwise path.
    - Value choice on isinstance(path, (list bitwise or tuple)) — true gives path at negative 1, false gives path.
  - Return flt(Platform.get\_attr(method)(self, item, tax)).
- Return flt(item.net\_amount).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“Enterprise\_taxable\_base\_resolvers”), Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L4010) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L785)

<a id="op-f49260c136ad46"></a>
### Calculate taxes and totals.set item wise tax

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_set_item_wise_tax`

**Inputs** self, item, tax, tax\_rate, current\_tax\_amount, current\_net\_amount.

**Local steps**

- Set multiplier from negative 1 when tax.get(“add\_deduct\_tax”) equals “Deduct”, otherwise 1.
  - Value choice on tax.get(“add\_deduct\_tax”) equals “Deduct” — true gives negative 1, false gives 1.
- Update tax.\_running\_txn\_tax\_total using + (current\_tax\_amount × multiplier).
- Set new\_base\_tax\_total from flt((flt(tax.\_running\_txn\_tax\_total, tax.precision(“tax\_amount”)) × self.doc.conversion\_rate), tax.precision(“base\_tax\_amount”)).
- Set item\_wise\_tax\_amount from flt((new\_base\_tax\_total − tax.\_running\_base\_tax\_total), tax.precision(“base\_tax\_amount”)).
- Set tax.\_running\_base\_tax\_total from new\_base\_tax\_total.
- If tax.charge\_type differs from “On Item Quantity”.
  - Update tax.\_running\_txn\_taxable\_total using + (current\_net\_amount × multiplier).
  - Set new\_base\_taxable\_total from flt((flt(tax.\_running\_txn\_taxable\_total, tax.precision(“net\_amount”)) × self.doc.conversion\_rate), tax.precision(“base\_net\_amount”)).
  - Set item\_wise\_taxable\_amount from flt((new\_base\_taxable\_total − tax.\_running\_base\_taxable\_total), tax.precision(“base\_net\_amount”)).
  - Set tax.\_running\_base\_taxable\_total from new\_base\_taxable\_total.
- Otherwise.
  - Set item\_wise\_taxable\_amount from 0.0.
- Evaluate self.doc.\_item\_wise\_tax\_details.append(Platform.\_dict(item = item, tax = tax, rate = tax\_rate, amount = item\_wise\_tax\_amount, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L4276) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L801)

<a id="op-ca3d0a253455c9"></a>
### Calculate taxes and totals.round off totals

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_round_off_totals`

**Inputs** self, tax.

**Local steps**

- If tax.account\_head belongs to Platform.flags.round\_off\_applicable\_accounts.
  - Set tax.tax\_amount from round(tax.tax\_amount, 0).
  - Set tax.tax\_amount\_after\_discount\_amount from round(tax.tax\_amount\_after\_discount\_amount, 0).
- Set tax.tax\_amount from flt(tax.tax\_amount, tax.precision(“tax\_amount”)).
- Set tax.net\_amount from flt(tax.net\_amount, tax.precision(“net\_amount”)).
- Set tax.tax\_amount\_after\_discount\_amount from flt(tax.tax\_amount\_after\_discount\_amount, tax.precision(“tax\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L4941) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L797)

<a id="op-e13c391d7347eb"></a>
### Calculate taxes and totals.round off base values

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_round_off_base_values`

**Inputs** self, tax.

**Local steps**

- If tax.account\_head belongs to Platform.flags.round\_off\_applicable\_accounts.
  - Set tax.base\_tax\_amount from round(tax.base\_tax\_amount, 0).
  - Set tax.base\_tax\_amount\_after\_discount\_amount from round(tax.base\_tax\_amount\_after\_discount\_amount, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L5256) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L796)

<a id="op-bb42d803435ef7"></a>
### Calculate taxes and totals.manipulate grand total for inclusive tax

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_manipulate_grand_total_for_inclusive_tax`

**Inputs** self.

**Wrappers, in declaration order** record a compatibility advisory for the invoked interface.

**Explicit results** self.adjust\_grand\_total\_for\_inclusive\_tax().

**Local steps**

- Return self.adjust\_grand\_total\_for\_inclusive\_tax().

**Methods declared on this owner** [adjust grand total for inclusive tax](operations-035.md#op-7e80713d1c0d92).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L5401) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L794)
