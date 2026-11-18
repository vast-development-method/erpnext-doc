# Shared transaction rules · operations 35

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Taxes and totals

<a id="op-7e80713d1c0d92"></a>
### Calculate taxes and totals.adjust grand total for inclusive tax

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_adjust_grand_total_for_inclusive_tax`

**Inputs** self.

**Local steps**

- If (self.doc.get(“taxes”) and any(generator of cint(t.included\_in\_print\_rate) for t drawn from self.doc.get(“taxes”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.get(“taxes”) → any(generator of cint(t.included\_in\_print\_rate) for t drawn from self.doc.get(“taxes”)).
  - Draw t from self.doc.get(“taxes”).
  - Set last\_tax from self.doc.get(“taxes”) at negative 1.
  - Set non\_inclusive\_tax\_amount from sum(generator of self.get\_tax\_amount\_if\_for\_valuation\_or\_deduction(d.tax\_amount\_after\_discount\_amount, d) for d drawn from self.doc.get(“taxes”) where not d.included\_in\_print\_rate).
    - Draw d from self.doc.get(“taxes”), keep a combination only if (not d.included\_in\_print\_rate).
  - Set diff from ((self.doc.total + non\_inclusive\_tax\_amount) − flt(last\_tax.total, last\_tax.precision(“total”))).
  - Update diff using − sum(generator of flt(item.get(“\_mapped\_discount\_inclusive\_amount”)) for item drawn from self.\_items).
    - Draw item from self.\_items.
  - If (self.discount\_amount\_applied and self.doc.discount\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.discount\_amount\_applied → self.doc.discount\_amount.
    - Update diff using − flt(self.doc.discount\_amount).
  - Set diff from flt(diff, self.doc.precision(“rounding\_adjustment”)).
  - If (diff and abs(diff) ≤ (5.0 ÷ (10 to the power last\_tax.precision(“tax\_amount”)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in diff → abs(diff) ≤ (5.0 ÷ (10 to the power last\_tax.precision(“tax\_amount”))).
    - Set self.grand\_total\_diff from diff.
  - Otherwise.
    - Set self.grand\_total\_diff from 0.
  - If (hasattr(self, “grand\_total\_for\_distributing\_discount”) and not self.discount\_amount\_applied).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “grand\_total\_for\_distributing\_discount”) → not self.discount\_amount\_applied.
    - Update self.grand\_total\_for\_distributing\_discount using + self.grand\_total\_diff.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tax amount if for valuation or deduction](operations-034.md#op-2d41ddaf0ddcd7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1095) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L764)

<a id="op-bc79046895dbab"></a>
### Calculate taxes and totals.calculate totals

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_totals`

**Inputs** self.

**Local steps**

- Set grand\_total\_diff from self.grand\_total\_diff.
- If self.doc.get(“taxes”).
  - Set self.doc.grand\_total from (flt(nested operand in the contract.doc.get(“taxes”) at negative 1.total) + grand\_total\_diff).
- Otherwise.
  - Set self.doc.grand\_total from flt(self.doc.net\_total).
- If self.doc.get(“taxes”).
  - Set self.doc.total\_taxes\_and\_charges from flt(((self.doc.grand\_total − self.doc.net\_total) − grand\_total\_diff), self.doc.precision(“total\_taxes\_and\_charges”)).
- Otherwise.
  - Set self.doc.total\_taxes\_and\_charges from 0.0.
- Evaluate self.\_set\_in\_company\_currency(self.doc, list(“total\_taxes\_and\_charges”)).
- If self.doc.doctype belongs to list(“Quotation”, “Sales Order”, “Delivery Note”, “Sales Invoice”, …).
  - Set self.doc.base\_grand\_total from flt((self.doc.grand\_total × self.doc.conversion\_rate), self.doc.precision(“base\_grand\_total”)) when self.doc.total\_taxes\_and\_charges, otherwise self.doc.base\_net\_total.
    - Value choice on self.doc.total\_taxes\_and\_charges — true gives flt((self.doc.grand\_total × self.doc.conversion\_rate), self.doc.precision(“base\_grand\_total”)), false gives self.doc.base\_net\_total.
- Otherwise.
  - Set self.doc.taxes\_and\_charges\_added, self.doc.taxes\_and\_charges\_deducted from 0.0.
  - For each tax in self.doc.get(“taxes”).
    - If tax.category belongs to list(“Valuation and Total”, “Total”).
      - If tax.add\_deduct\_tax equals “Add”.
        - Update self.doc.taxes\_and\_charges\_added using + flt(tax.tax\_amount\_after\_discount\_amount).
      - Otherwise.
        - Update self.doc.taxes\_and\_charges\_deducted using + flt(tax.tax\_amount\_after\_discount\_amount).
  - Evaluate self.doc.round\_floats\_in(self.doc, list(“taxes\_and\_charges\_added”, “taxes\_and\_charges\_deducted”)).
  - Set self.doc.base\_grand\_total from flt((self.doc.grand\_total × self.doc.conversion\_rate)) when (self.doc.taxes\_and\_charges\_added or self.doc.taxes\_and\_charges\_deducted), otherwise self.doc.base\_net\_total.
    - Value choice on (self.doc.taxes\_and\_charges\_added or self.doc.taxes\_and\_charges\_deducted) — true gives flt((self.doc.grand\_total × self.doc.conversion\_rate)), false gives self.doc.base\_net\_total.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.taxes\_and\_charges\_added → self.doc.taxes\_and\_charges\_deducted.
  - Evaluate self.\_set\_in\_company\_currency(self.doc, list(“taxes\_and\_charges\_added”, “taxes\_and\_charges\_deducted”)).
- Evaluate self.doc.round\_floats\_in(self.doc, list(“grand\_total”, “base\_grand\_total”)).
- Evaluate self.set\_rounded\_total().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set in company currency](operations-034.md#op-2605086ca20dec), [set rounded total](operations-035.md#op-4c9ec36bddb291).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L6175) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L779)

<a id="op-1e667b53343bbf"></a>
### Calculate taxes and totals.calculate total net weight

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_total_net_weight`

**Inputs** self.

**Local steps**

- If self.doc.meta.get\_field(“total\_net\_weight”).
  - Set self.doc.total\_net\_weight from 0.0.
  - For each d in self.\_items.
    - If d.total\_weight.
      - Update self.doc.total\_net\_weight using + d.total\_weight.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0402.json#L7243) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L778)

<a id="op-4c9ec36bddb291"></a>
### Calculate taxes and totals.set rounded total

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_set_rounded_total`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.doc.get(“is\_consolidated”) and self.doc.get(“rounding\_adjustment”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.get(“is\_consolidated”) → self.doc.get(“rounding\_adjustment”).
  - Return no value.
- If self.doc.meta.get\_field(“rounded\_total”).
  - If self.doc.is\_rounded\_total\_disabled().
    - Set self.doc.rounded\_total from 0.
    - Set self.doc.rounding\_adjustment from 0.
  - Otherwise.
    - Set self.doc.rounded\_total from round\_based\_on\_smallest\_currency\_fraction(self.doc.grand\_total, self.doc.currency, self.doc.precision(“rounded\_total”)).
    - Set self.doc.rounding\_adjustment from flt((self.doc.rounded\_total − self.doc.grand\_total), self.doc.precision(“rounding\_adjustment”)).
  - Evaluate self.\_set\_in\_company\_currency(self.doc, list(“rounding\_adjustment”, “rounded\_total”)).
  - If self.doc.rounding\_adjustment.
    - Set self.doc.base\_rounding\_adjustment from flt((self.doc.base\_rounded\_total − self.doc.base\_grand\_total), self.doc.precision(“base\_rounding\_adjustment”)).
  - Otherwise.
    - If self.doc.rounded\_total.
      - Set self.doc.base\_rounded\_total from flt((self.doc.base\_grand\_total + self.doc.base\_rounding\_adjustment), self.doc.precision(“base\_rounded\_total”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set in company currency](operations-034.md#op-2605086ca20dec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L803)

<a id="op-2fb271029092a4"></a>
### Calculate taxes and totals.set discount amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_set_discount_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Additional Discount Amount ({discount\_amount}) cannot exceed the total before such discount ({total\_before\_d …”.format(discount\_amount = self.doc.get\_formatted(“discount\_amount”), total\_before\_ ….

**Local steps**

- If self.doc.additional\_discount\_percentage.
  - Set self.doc.discount\_amount from flt(((flt(nested operand in the contract.doc.get(scrub(nested operand in the contract.apply\_discount\_on))) × self.doc.additional\_discount\_percentage) ÷ 100), self.doc.precision(“discount\_amount”)).
- Set discount\_amount from (self.doc.discount\_amount or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.discount\_amount → 0.
- Set grand\_total from self.doc.grand\_total.
- If (self.doc.get(“is\_return”) and self.doc.get(“return\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.get(“is\_return”) → self.doc.get(“return\_against”).
  - Set doctype from Platform.qb.DocType(self.doc.doctype).
  - Set result from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“total\_return\_discount”)).where(((nested operand in the contract.return\_against equals nested operan ….
  - Set total\_return\_discount from abs((result at 0.get(“total\_return\_discount”) or 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.get(“total\_return\_discount”) → 0.
  - Update discount\_amount using + total\_return\_discount.
- If (self.doc.get(“\_action”) and ((grand\_total ≥ 0 and discount\_amount &gt; grand\_total) or (grand\_total &lt; 0 and discount\_amount &lt; grand\_total))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.get(“\_action”) → ((grand\_total ≥ 0 and discount\_amount &gt; grand\_total) or (grand\_total &lt; 0 and discount\_amount &lt; grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (grand\_total ≥ 0 and discount\_amount &gt; grand\_total) → (grand\_total &lt; 0 and discount\_amount &lt; grand\_total).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in grand\_total ≥ 0 → discount\_amount &gt; grand\_total.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in grand\_total &lt; 0 → discount\_amount &lt; grand\_total.
  - Call the validation error handler Platform.throw(translated “Additional Discount Amount ({discount\_amount}) cannot exceed the total before such discount ({total\_before\_d …”.format(discount\_amount = self.doc.get\_formatted(“discount\_amount”) ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L441) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L799)

<a id="op-69499f68e14f6c"></a>
### Calculate taxes and totals.apply discount amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_apply_discount_amount`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please select Apply Discount On”.

**Local steps**

- If self.doc.discount\_amount.
  - If not self.doc.apply\_discount\_on.
    - Call the validation error handler Platform.throw(translated “Please select Apply Discount On”).
  - Set self.doc.base\_discount\_amount from flt((self.doc.discount\_amount × self.doc.conversion\_rate), self.doc.precision(“base\_discount\_amount”)).
  - If (self.doc.apply\_discount\_on equals “Grand Total” and self.doc.get(“is\_cash\_or\_non\_trade\_discount”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.apply\_discount\_on equals “Grand Total” → self.doc.get(“is\_cash\_or\_non\_trade\_discount”).
    - Set self.discount\_amount\_applied from true.
    - Return no value.
  - Set total\_for\_discount\_amount from self.get\_total\_for\_discount\_amount().
  - Set net\_totals from mapping().
  - Set use\_unrounded\_net from (self.doc.apply\_discount\_on equals “Grand Total” and not Platform.flags.round\_row\_wise\_tax and any(generator of cint(tax.included\_in\_print\_rate) for tax drawn from self.doc.get(“taxes”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.apply\_discount\_on equals “Grand Total” → not Platform.flags.round\_row\_wise\_tax → any(generator of cint(tax.included\_in\_print\_rate) for tax drawn from self.doc.get(“taxes”)).
    - Draw tax from self.doc.get(“taxes”).
  - If total\_for\_discount\_amount.
    - For each item in self.\_items.
      - Set tax\_key from tuple(sorted(nested operand in the contract.\_load\_item\_tax\_rate(nested operand in the contract.item\_tax\_rate).items())) when use\_unrounded\_net, otherwise no value.
        - Value choice on use\_unrounded\_net — true gives tuple(sorted(self.\_load\_item\_tax\_rate(item.item\_tax\_rate).items())), false gives no value.
      - Set net\_total from net\_totals.setdefault(tax\_key, Platform.\_dict(unrounded = 0, rounded = 0)).
      - Set net\_amount from item.\_unrounded\_net\_amount when (use\_unrounded\_net and item.\_unrounded\_net\_amount is distinct from no value), otherwise item.net\_amount.
        - Value choice on (use\_unrounded\_net and item.\_unrounded\_net\_amount is distinct from no value) — true gives item.\_unrounded\_net\_amount, false gives item.net\_amount.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in use\_unrounded\_net → item.\_unrounded\_net\_amount is distinct from no value.
      - Set adjusted\_net\_amount from (net\_amount − ((flt(self.doc.discount\_amount) × net\_amount) ÷ total\_for\_discount\_amount)).
      - Set item.\_unrounded\_net\_amount from adjusted\_net\_amount when use\_unrounded\_net, otherwise no value.
        - Value choice on use\_unrounded\_net — true gives adjusted\_net\_amount, false gives no value.
      - Update net\_total.unrounded using + adjusted\_net\_amount.
      - Set distributed\_amount from (item.net\_amount − flt(adjusted\_net\_amount, item.precision(“net\_amount”))).
      - Set item.net\_amount from flt(adjusted\_net\_amount, item.precision(“net\_amount”)).
      - Set item.distributed\_discount\_amount from flt(distributed\_amount, item.precision(“distributed\_discount\_amount”)).
      - Update net\_total.rounded using + item.net\_amount.
      - If rounding\_difference bound to flt((net\_total.unrounded − net\_total.rounded), self.doc.precision(“net\_total”)).
        - Set item.net\_amount from flt((item.net\_amount + rounding\_difference), item.precision(“net\_amount”)).
        - Set item.distributed\_discount\_amount from flt((distributed\_amount − rounding\_difference), item.precision(“distributed\_discount\_amount”)).
        - Update net\_total.rounded using + rounding\_difference.
      - Set billed\_qty from self.get\_billed\_qty(item).
      - Set item.net\_rate from flt((item.net\_amount ÷ billed\_qty), item.precision(“net\_rate”)) when billed\_qty, otherwise 0.
        - Value choice on billed\_qty — true gives flt((item.net\_amount ÷ billed\_qty), item.precision(“net\_rate”)), false gives 0.
      - Evaluate self.\_set\_in\_company\_currency(item, list(“net\_rate”, “net\_amount”)).
    - Set self.discount\_amount\_applied from true.
    - Evaluate self.\_calculate().
- Otherwise.
  - Set self.doc.base\_discount\_amount from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get total for discount amount](operations-035.md#op-be5a5e14e20ee9), [load item tax rate](operations-034.md#op-43db67a4d48489), [get billed qty](operations-034.md#op-0d91de14fc41c1), [set in company currency](operations-034.md#op-2605086ca20dec), [calculate](operations-033.md#op-b66b9d64dc80e1).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1097) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L766)

<a id="op-be5a5e14e20ee9"></a>
### Calculate taxes and totals.get total for discount amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_get_total_for_discount_amount`

**Inputs** self.

**Explicit results** self.doc.net\_total · (getattr(self, “grand\_total\_for\_distributing\_discount”, doc.grand\_total) − total\_actual\_tax).

**Local steps**

- Set doc from self.doc.
- If (doc.apply\_discount\_on equals “Net Total” or not doc.get(“taxes”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.apply\_discount\_on equals “Net Total” → not doc.get(“taxes”).
  - Return self.doc.net\_total.
- Set total\_actual\_tax from 0.
- Set actual\_taxes\_dict from mapping().
- Bind local operation update\_actual\_tax\_dict for subsequent calls.
- For each tax in doc.taxes.
  - If tax.charge\_type belongs to list(“Actual”, “On Item Quantity”).
    - Evaluate update\_actual\_tax\_dict(tax, tax.tax\_amount).
    - Continue with the next iteration or loop test.
  - If not tax.row\_id.
    - Continue with the next iteration or loop test.
  - Set base\_row from actual\_taxes\_dict.get(int(tax.row\_id)).
  - If not base\_row.
    - Continue with the next iteration or loop test.
  - Set base\_tax\_amount from base\_row at “tax\_amount” when tax.charge\_type equals “On Previous Row Amount”, otherwise base\_row at “cumulative\_tax\_amount”.
    - Value choice on tax.charge\_type equals “On Previous Row Amount” — true gives base\_row at “tax\_amount”, false gives base\_row at “cumulative\_tax\_amount”.
  - Evaluate update\_actual\_tax\_dict(tax, ((base\_tax\_amount × tax.rate) ÷ 100)).
- Return (getattr(self, “grand\_total\_for\_distributing\_discount”, doc.grand\_total) − total\_actual\_tax).

**Values supplied outside this operation** selected callable from getattr(self, “grand\_total\_for\_distributing\_discount”, doc.grand\_total).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L2292) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L788)

<a id="op-00ad737a417b72"></a>
### Calculate taxes and totals.get total for discount amount.update actual tax dict

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_get_total_for_discount_amount_update_actual_tax_mapping`

**Inputs** tax, tax\_amount.

**Local steps**

- Use enclosing bindings total\_actual\_tax.
- If tax.get(“add\_deduct\_tax”) equals “Deduct”.
  - Update tax\_amount using × negative 1.
- If tax.get(“category”) differs from “Valuation”.
  - Update total\_actual\_tax using + tax\_amount.
- Set actual\_taxes\_dict at int(tax.idx) from mapping(“tax\_amount” → tax\_amount, “cumulative\_tax\_amount” → total\_actual\_tax).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L2963) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L789)

<a id="op-133b50a06e8294"></a>
### Calculate taxes and totals.calculate total advance

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_total_advance`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Advance amount cannot be greater than {0} {1}”.format(self.doc.party\_account\_currency, invoice\_total).

**Local steps**

- If not self.doc.docstatus.is\_cancelled().
  - Set total\_allocated\_amount from sum(generator of flt(adv.allocated\_amount, adv.precision(“allocated\_amount”)) for adv drawn from self.doc.get(“advances”)).
    - Draw adv from self.doc.get(“advances”).
  - Set self.doc.total\_advance from flt(total\_allocated\_amount, self.doc.precision(“total\_advance”)).
  - Set grand\_total from (self.doc.rounded\_total or self.doc.grand\_total).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.rounded\_total → self.doc.grand\_total.
  - If self.doc.party\_account\_currency equals self.doc.currency.
    - Set invoice\_total from flt((grand\_total − flt(self.doc.write\_off\_amount)), self.doc.precision(“grand\_total”)).
  - Otherwise.
    - Set base\_write\_off\_amount from flt((flt(self.doc.write\_off\_amount) × self.doc.conversion\_rate), self.doc.precision(“base\_write\_off\_amount”)).
    - Set invoice\_total from (flt((grand\_total × self.doc.conversion\_rate), self.doc.precision(“base\_grand\_total”)) − base\_write\_off\_amount).
  - If (invoice\_total &gt; 0 and self.doc.total\_advance &gt; invoice\_total).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoice\_total &gt; 0 → self.doc.total\_advance &gt; invoice\_total.
    - Call the validation error handler Platform.throw(translated “Advance amount cannot be greater than {0} {1}”.format(self.doc.party\_account\_currency, invoice\_total)).
  - If self.doc.get(“write\_off\_outstanding\_amount\_automatically”).
    - Set self.doc.write\_off\_amount from 0.
  - Evaluate self.calculate\_outstanding\_amount().
  - Evaluate self.calculate\_write\_off\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate outstanding amount](operations-035.md#op-52566240c2646f), [calculate write off amount](operations-035.md#op-b23c2866fe9145).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L777)

<a id="op-5960de196726de"></a>
### Calculate taxes and totals.is internal invoice

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_is_internal_invoice`

**Inputs** self.

**Explicit results** true · false.

**Local steps**

- If (self.doc.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and self.doc.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”) → self.doc.is\_internal\_transfer().
  - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L3956) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L792)

<a id="op-52566240c2646f"></a>
### Calculate taxes and totals.calculate outstanding amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_outstanding_amount`

**Inputs** self.

**Record and data access** read “POS Profile” via get\_value.

**Explicit results** no value.

**Local steps**

- If self.doc.doctype equals “Sales Invoice”.
  - Evaluate self.calculate\_paid\_amount().
- If ((self.doc.is\_return and self.doc.return\_against and not self.doc.update\_outstanding\_for\_self and not self.doc.get(“is\_pos”)) or self.is\_internal\_invoice()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.doc.is\_return and self.doc.return\_against and not self.doc.update\_outstanding\_for\_self and not self.doc.get(“is\_pos”)) → self.is\_internal\_invoice().
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.is\_return → self.doc.return\_against → not self.doc.update\_outstanding\_for\_self → not self.doc.get(“is\_pos”).
  - Set self.doc.outstanding\_amount from 0.
  - Return no value.
- Evaluate self.doc.round\_floats\_in(self.doc, list(“grand\_total”, “total\_advance”, “write\_off\_amount”)).
- Evaluate self.\_set\_in\_company\_currency(self.doc, list(“write\_off\_amount”)).
- If self.doc.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Set grand\_total from (self.doc.rounded\_total or self.doc.grand\_total).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.rounded\_total → self.doc.grand\_total.
  - Set base\_grand\_total from (self.doc.base\_rounded\_total or self.doc.base\_grand\_total).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.base\_rounded\_total → self.doc.base\_grand\_total.
  - If self.doc.party\_account\_currency equals self.doc.currency.
    - Set total\_amount\_to\_pay from flt(((grand\_total − self.doc.total\_advance) − flt(self.doc.write\_off\_amount)), self.doc.precision(“grand\_total”)).
  - Otherwise.
    - Set total\_amount\_to\_pay from flt(((flt(base\_grand\_total, nested operand in the contract.doc.precision(“base\_grand\_total”)) − self.doc.total\_advance) − flt(self.doc.base\_write\_off\_amount)), self.doc.precision(“base\_grand\_total”)).
  - Evaluate self.doc.round\_floats\_in(self.doc, list(“paid\_amount”)).
  - Set change\_amount from 0.
  - If (self.doc.doctype equals “Sales Invoice” and not self.doc.get(“is\_return”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype equals “Sales Invoice” → not self.doc.get(“is\_return”).
    - Evaluate self.calculate\_change\_amount().
    - Set change\_amount from self.doc.change\_amount when self.doc.party\_account\_currency equals self.doc.currency, otherwise self.doc.base\_change\_amount.
      - Value choice on self.doc.party\_account\_currency equals self.doc.currency — true gives self.doc.change\_amount, false gives self.doc.base\_change\_amount.
  - Set paid\_amount from self.doc.paid\_amount when self.doc.party\_account\_currency equals self.doc.currency, otherwise self.doc.base\_paid\_amount.
    - Value choice on self.doc.party\_account\_currency equals self.doc.currency — true gives self.doc.paid\_amount, false gives self.doc.base\_paid\_amount.
  - Set self.doc.outstanding\_amount from flt(((total\_amount\_to\_pay − flt(paid\_amount)) + flt(change\_amount)), self.doc.precision(“outstanding\_amount”)).
  - If (self.doc.doctype equals “Sales Invoice” and self.doc.get(“is\_pos”) and self.doc.get(“pos\_profile”) and self.doc.get(“is\_consolidated”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype equals “Sales Invoice” → self.doc.get(“is\_pos”) → self.doc.get(“pos\_profile”) → self.doc.get(“is\_consolidated”).
    - Set write\_off\_limit from flt(Platform.db.get\_value(“POS Profile”, self.doc.pos\_profile, “write\_off\_limit”)).
    - If (write\_off\_limit and abs(self.doc.outstanding\_amount) ≤ write\_off\_limit).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in write\_off\_limit → abs(self.doc.outstanding\_amount) ≤ write\_off\_limit.
      - Set self.doc.write\_off\_outstanding\_amount\_automatically from 1.
  - If (self.doc.doctype equals “Sales Invoice” and self.doc.get(“is\_pos”) and self.doc.get(“is\_return”) and not self.doc.get(“is\_consolidated”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype equals “Sales Invoice” → self.doc.get(“is\_pos”) → self.doc.get(“is\_return”) → not self.doc.get(“is\_consolidated”).
    - Evaluate self.set\_total\_amount\_to\_default\_mop(total\_amount\_to\_pay).
    - Evaluate self.calculate\_paid\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate paid amount](operations-035.md#op-4509b80c2bc588), [is internal invoice](operations-035.md#op-5960de196726de), [set in company currency](operations-034.md#op-2605086ca20dec), [calculate change amount](operations-035.md#op-2d2955c273231e), [set total amount to default mop](operations-035.md#op-5d98ab7ed89ad3).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L4075) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L773)

<a id="op-4509b80c2bc588"></a>
### Calculate taxes and totals.calculate paid amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_paid_amount`

**Inputs** self.

**Local steps**

- Set paid\_amount, base\_paid\_amount from 0.0.
- If self.doc.is\_pos.
  - For each payment in self.doc.get(“payments”).
    - Set payment.amount from flt(payment.amount).
    - Set payment.base\_amount from (payment.amount × flt(self.doc.conversion\_rate)).
    - Update paid\_amount using + payment.amount.
    - Update base\_paid\_amount using + payment.base\_amount.
- Otherwise.
  - If not self.doc.is\_return.
    - Evaluate self.doc.set(“payments”, list()).
- If (self.doc.redeem\_loyalty\_points and self.doc.loyalty\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.redeem\_loyalty\_points → self.doc.loyalty\_amount.
  - Update base\_paid\_amount using + self.doc.loyalty\_amount.
  - Update paid\_amount using + (self.doc.loyalty\_amount ÷ flt(self.doc.conversion\_rate)).
- Set self.doc.paid\_amount from flt(paid\_amount, self.doc.precision(“paid\_amount”)).
- Set self.doc.base\_paid\_amount from flt(base\_paid\_amount, self.doc.precision(“base\_paid\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L5625) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L774)

<a id="op-2d2955c273231e"></a>
### Calculate taxes and totals.calculate change amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_change_amount`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.doc.flags.keep\_change\_amount and any(generator of d.type equals “Cash” for d drawn from self.doc.payments)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.flags.keep\_change\_amount → any(generator of d.type equals “Cash” for d drawn from self.doc.payments).
  - Draw d from self.doc.payments.
  - Return no value.
- Set self.doc.change\_amount from 0.0.
- Set self.doc.base\_change\_amount from 0.0.
- Set grand\_total from (self.doc.rounded\_total or self.doc.grand\_total).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.rounded\_total → self.doc.grand\_total.
- Set base\_grand\_total from (self.doc.base\_rounded\_total or self.doc.base\_grand\_total).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.base\_rounded\_total → self.doc.base\_grand\_total.
- If (self.doc.doctype equals “Sales Invoice” and self.doc.paid\_amount &gt; grand\_total and not self.doc.is\_return and any(generator of d.type equals “Cash” for d drawn from self.doc.payments)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.doctype equals “Sales Invoice” → self.doc.paid\_amount &gt; grand\_total → not self.doc.is\_return → any(generator of d.type equals “Cash” for d drawn from self.doc.payments).
  - Draw d from self.doc.payments.
  - Set self.doc.change\_amount from flt((self.doc.paid\_amount − grand\_total), self.doc.precision(“change\_amount”)).
  - Set self.doc.base\_change\_amount from flt((self.doc.base\_paid\_amount − base\_grand\_total), self.doc.precision(“base\_change\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L769)

<a id="op-b23c2866fe9145"></a>
### Calculate taxes and totals.calculate write off amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_calculate_write_off_amount`

**Inputs** self.

**Local steps**

- If self.doc.get(“write\_off\_outstanding\_amount\_automatically”).
  - Set self.doc.write\_off\_amount from flt(self.doc.outstanding\_amount, self.doc.precision(“write\_off\_amount”)).
  - Set self.doc.base\_write\_off\_amount from flt((self.doc.write\_off\_amount × self.doc.conversion\_rate), self.doc.precision(“base\_write\_off\_amount”)).
  - Evaluate self.calculate\_outstanding\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate outstanding amount](operations-035.md#op-52566240c2646f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L6571) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L780)

<a id="op-790fdb2cbe72d1"></a>
### Calculate taxes and totals.set item wise tax breakup

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_set_item_wise_tax_breakup`

**Inputs** self.

**Local steps**

- Set self.doc.other\_charges\_calculation from get\_itemised\_tax\_breakup\_html(self.doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L6812) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L802)

<a id="op-5d98ab7ed89ad3"></a>
### Calculate taxes and totals.set total amount to default mop

`operation_enterprise_controllers_taxes_and_totals_business_behavior_calculate_taxes_and_totals_set_total_amount_to_default_mop`

**Inputs** self, total\_amount\_to\_pay.

**Record and data access** read “POS Payment Method” via get\_value.

**Local steps**

- Set total\_paid\_amount from 0.
- For each payment in self.doc.get(“payments”).
  - Update total\_paid\_amount using + payment.amount when self.doc.party\_account\_currency equals self.doc.currency, otherwise payment.base\_amount.
    - Value choice on self.doc.party\_account\_currency equals self.doc.currency — true gives payment.amount, false gives payment.base\_amount.
- Set pending\_amount from (total\_amount\_to\_pay − total\_paid\_amount).
- If pending\_amount &gt; 0.
  - Set default\_mode\_of\_payment from Platform.db.get\_value(“POS Payment Method”, mapping(“parent” → self.doc.pos\_profile, “default” → 1), list(“mode\_of\_payment”), as\_dict = 1).
  - If default\_mode\_of\_payment.
    - Set self.doc.payments from list().
    - Evaluate self.doc.append(“payments”, mapping(“mode\_of\_payment” → default\_mode\_of\_payment.mode\_of\_payment, “amount” → pending\_amount, “default” → 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L6882) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L804)

<a id="op-f9a2f58fa732b6"></a>
### Remove discount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_remove_discount`

**Inputs** item.

**Local steps**

- Set item.discount\_percentage from 0.0.
- Set item.discount\_amount from 0.0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L7302) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L823)

<a id="op-0451a650b5e213"></a>
### Remove margin

`operation_enterprise_controllers_taxes_and_totals_business_behavior_remove_margin`

**Inputs** item.

**Local steps**

- Set item.margin\_type from no value.
- Set item.margin\_rate\_or\_amount from 0.0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0403.json#L7366) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L824)

<a id="op-276901a9f9995e"></a>
### Get rate with margin

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_rate_with_margin`

**Inputs** item.

**Explicit results** item.price\_list\_rate · flt((item.price\_list\_rate × (1 + (item.margin\_rate\_or\_amount ÷ 100.0))), item.precision(“rate\_with\_margin”)) · flt((item.price\_list\_rate + item.margin\_rate\_or\_amount), item.precision(“rate\_with\_margin”)).

**Local steps**

- If not item.margin\_type.
  - Return item.price\_list\_rate.
- If item.margin\_type equals “Percentage”.
  - Return flt((item.price\_list\_rate × (1 + (item.margin\_rate\_or\_amount ÷ 100.0))), item.precision(“rate\_with\_margin”)).
- Return flt((item.price\_list\_rate + item.margin\_rate\_or\_amount), item.precision(“rate\_with\_margin”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1143) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L812)

<a id="op-b74914c5f95177"></a>
### Get itemised tax breakup html

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_itemised_tax_breakup_document_markup`

**Inputs** doc.

**Explicit results** no value · Platform.render\_template(“templates/includes/itemised\_tax\_breakup.html”, dict(headers = headers, itemised\_tax\_data = itemised\_tax\_data, tax\_accounts = tax\_accounts, doc = doc)).

**Local steps**

- If not doc.taxes.
  - Return no value.
- Set tax\_accounts from list().
- For each tax in doc.taxes.
  - If (getattr(tax, “category”, no value) and tax.category equals “Valuation”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(tax, “category”, no value) → tax.category equals “Valuation”.
    - Continue with the next iteration or loop test.
  - If tax.description does not belong to tax\_accounts.
    - Evaluate tax\_accounts.append(tax.description).
- Within temporary\_flag(“company”, doc.company).
  - Set headers from get\_itemised\_tax\_breakup\_header((doc.doctype + “ Item”), tax\_accounts).
  - Set itemised\_tax\_data from get\_itemised\_tax\_breakup\_data(doc).
  - Evaluate get\_rounded\_tax\_amount(itemised\_tax\_data, doc.precision(“tax\_amount”, “taxes”)).
  - Evaluate update\_itemised\_tax\_data(doc).
- Return Platform.render\_template(“templates/includes/itemised\_tax\_breakup.html”, dict(headers = headers, itemised\_tax\_data = itemised\_tax\_data, tax\_accounts = tax\_accounts, doc = doc)).

**Values supplied outside this operation** selected callable from getattr(tax, “category”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L226) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1141) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L810)

<a id="op-2914eae80be976"></a>
### Get round off applicable accounts

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_round_off_applicable_accounts`

**Inputs** company, account\_list, doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_regional\_round\_off\_accounts(company, account\_list, doc).

**Local steps**

- Within temporary\_flag(“company”, company).
  - Return get\_regional\_round\_off\_accounts(company, account\_list, doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L693) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L814)

<a id="op-96b70bd82dd8f6"></a>
### Get regional round off accounts

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_regional_round_off_accounts`

**Inputs** company, account\_list, doc = no value.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L881) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L813)

<a id="op-ba7b43f6ae7685"></a>
### Update itemised tax data

`operation_enterprise_controllers_taxes_and_totals_business_behavior_update_itemised_tax_data`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L940) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1156) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L825)

<a id="op-265c161d572953"></a>
### Get itemised tax breakup header

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_itemised_tax_breakup_header`

**Inputs** item\_doctype, tax\_accounts.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** list(translated “Item”, translated “Taxable Amount”, expanded tax\_accounts).

**Local steps**

- Return list(translated “Item”, translated “Taxable Amount”, expanded tax\_accounts).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L982) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L811)
