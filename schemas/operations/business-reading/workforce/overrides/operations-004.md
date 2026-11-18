# Regional rules and controller overrides · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-c4a742a2e41200"></a>
### Get component amt from salary slip

`operation_workforce_regional_india_utils_business_behavior_get_component_amount_from_salary_slip`

**Inputs** employee, salary\_structure, basic\_component, hra\_component, from\_date.

**Explicit results** tuple(basic\_amt, hra\_amt).

**Local steps**

- Set salary\_slip from \_make\_salary\_slip(salary\_structure, employee = employee, for\_preview = 1, ignore\_permissions = true, posting\_date = from\_date).
- Set tuple(basic\_amt, hra\_amt) from tuple(0, 0).
- For each earning in salary\_slip.earnings.
  - If earning.salary\_component equals basic\_component.
    - Set basic\_amt from earning.amount.
  - Otherwise.
    - If earning.salary\_component equals hra\_component.
      - Set hra\_amt from earning.amount.
  - If (basic\_amt and hra\_amt).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in basic\_amt → hra\_amt.
    - Return tuple(basic\_amt, hra\_amt).
- Return tuple(basic\_amt, hra\_amt).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L16) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1072) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L23)

<a id="op-f6f25e0da0ddb0"></a>
### Calculate hra exemption

`operation_workforce_regional_india_utils_business_behavior_calculate_hra_exemption`

**Inputs** salary\_structure, annual\_basic, annual\_hra, monthly\_house\_rent, rented\_in\_metro\_city.

**Explicit results** min(exemptions).

**Local steps**

- Set exemptions from list().
- Evaluate exemptions.append(annual\_hra).
- Set actual\_annual\_rent from (monthly\_house\_rent × 12).
- Evaluate exemptions.append((flt(actual\_annual\_rent) − flt((annual\_basic × 0.1)))).
- Evaluate exemptions.append((annual\_basic × 0.5) when rented\_in\_metro\_city, otherwise (annual\_basic × 0.4)).
  - Value choice on rented\_in\_metro\_city — true gives (annual\_basic × 0.5), false gives (annual\_basic × 0.4).
- Return min(exemptions).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L1709) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1069) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L20)

<a id="op-658f0c52697c49"></a>
### Get component pay

`operation_workforce_regional_india_utils_business_behavior_get_component_pay`

**Inputs** frequency, amount, from\_date, to\_date.

**Explicit results** (amount × days) · (amount × math.floor((days ÷ 7))) · (amount × math.floor((days ÷ 14))) · (amount × month\_diff(to\_date, from\_date)) · (amount × (month\_diff(to\_date, from\_date) ÷ 2)).

**Local steps**

- Set days from (date\_diff(to\_date, from\_date) + 1).
- If frequency equals “Daily”.
  - Return (amount × days).
- Otherwise.
  - If frequency equals “Weekly”.
    - Return (amount × math.floor((days ÷ 7))).
  - Otherwise.
    - If frequency equals “Fortnightly”.
      - Return (amount × math.floor((days ÷ 14))).
    - Otherwise.
      - If frequency equals “Monthly”.
        - Return (amount × month\_diff(to\_date, from\_date)).
      - Otherwise.
        - If frequency equals “Bimonthly”.
          - Return (amount × (month\_diff(to\_date, from\_date) ÷ 2)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L1954) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1073) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L24)

<a id="op-fbfa812dca8d8c"></a>
### Validate house rent dates

`operation_workforce_regional_india_utils_business_behavior_validate_house_rent_dates`

**Inputs** doc.

**Explicit failure paths** validation helper — translated “House rented dates required for exemption calculation” · validation helper — translated “House rented dates should be atleast 15 days apart” · validation helper — translated “House rent paid days overlapping with {0}”.format(proofs at 0 at 0).

**Local steps**

- If (not doc.rented\_to\_date or not doc.rented\_from\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.rented\_to\_date → not doc.rented\_from\_date.
  - Call the validation error handler Platform.throw(translated “House rented dates required for exemption calculation”).
- If date\_diff(doc.rented\_to\_date, doc.rented\_from\_date) &lt; 14.
  - Call the validation error handler Platform.throw(translated “House rented dates should be atleast 15 days apart”).
- Set proof from Platform.qb.DocType(“Employee Tax Exemption Proof Submission”).
- Set proofs from nested operand in the contract(nested operand in the contract).select(proof.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract eq ….run().
- If proofs.
  - Call the validation error handler Platform.throw(translated “House rent paid days overlapping with {0}”.format(proofs at 0 at 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L2325) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1076) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L27)

<a id="op-a95627c5ee76ec"></a>
### Calculate hra exemption for period

`operation_workforce_regional_india_utils_business_behavior_calculate_hra_exemption_for_period`

**Inputs** doc.

**Explicit results** exemptions.

**Local steps**

- Set tuple(monthly\_rent, eligible\_hra) from tuple(0, 0).
- If doc.house\_rent\_payment\_amount.
  - Evaluate validate\_house\_rent\_dates(doc).
  - Set factor from (flt((date\_diff(doc.rented\_to\_date, doc.rented\_from\_date) + 1)) ÷ 30).
  - Set factor from (round((factor × 2)) ÷ 2).
  - Set monthly\_rent from (doc.house\_rent\_payment\_amount ÷ factor).
  - Set doc.monthly\_house\_rent from monthly\_rent.
  - Set exemptions from calculate\_annual\_eligible\_hra\_exemption(doc).
  - If exemptions at “monthly\_exemption”.
    - Set eligible\_hra from (exemptions at “monthly\_exemption” × factor).
  - Set exemptions at “monthly\_house\_rent” from monthly\_rent.
  - Set exemptions at “total\_eligible\_hra\_exemption” from eligible\_hra.
  - Return exemptions.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L2866) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1070) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L21)

<a id="op-a8ca68619da0f8"></a>
### Calculate tax with marginal relief

`operation_workforce_regional_india_utils_business_behavior_calculate_tax_with_marginal_relief`

**Inputs** tax\_slab, tax\_amount, annual\_taxable\_earning.

**Explicit results** tax\_amount.

**Local steps**

- If tax\_slab.get(“marginal\_relief\_limit”).
  - Set tax\_relief\_limit from (tax\_slab.tax\_relief\_limit or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_slab.tax\_relief\_limit → 0.
  - Set marginal\_relief\_limit from (tax\_slab.marginal\_relief\_limit or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_slab.marginal\_relief\_limit → 0.
  - If (annual\_taxable\_earning &gt; tax\_relief\_limit and annual\_taxable\_earning &lt; marginal\_relief\_limit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in annual\_taxable\_earning &gt; tax\_relief\_limit → annual\_taxable\_earning &lt; marginal\_relief\_limit.
    - Set income\_excess\_over\_tax\_relief from (annual\_taxable\_earning − tax\_slab.tax\_relief\_limit).
    - If income\_excess\_over\_tax\_relief &lt; tax\_amount.
      - Set tax\_amount from income\_excess\_over\_tax\_relief.
- Return tax\_amount.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0151.json#L3233) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1071) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L22)
