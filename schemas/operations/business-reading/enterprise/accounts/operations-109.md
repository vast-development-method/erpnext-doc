# Accounting and settlement · operations 109

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Shipping rule

[Record definition](../../../../data/record-types/shipping_rule.json)

<a id="op-10492c70e37277"></a>
### Shipping Rule.sort shipping rule conditions

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_sort_shipping_rule_conditions`

**Inputs** self.

**Local steps**

- Set self.shipping\_rules\_conditions from sorted(self.conditions, key = deferred anonymous expression).
- For each tuple(i, d) in enumerate(self.conditions).
  - Set d.idx from (i + 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L6230) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L197)

<a id="op-355953bc5485ae"></a>
### Shipping Rule.validate overlapping shipping rule conditions

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_validate_overlapping_shipping_rule_conditions`

**Inputs** self.

**Local steps**

- Bind local operation overlap\_exists\_between for subsequent calls.
- Set overlaps from list().
- For each i in range(0, len(self.conditions)).
  - For each j in range((i + 1), len(self.conditions)).
    - Set tuple(d1, d2) from tuple(self.conditions at i, self.conditions at j).
    - If d1.as\_dict() differs from d2.as\_dict().
      - Set range\_a from tuple(d1.from\_value, (d1.to\_value or d1.from\_value)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d1.to\_value → d1.from\_value.
      - Set range\_b from tuple(d2.from\_value, (d2.to\_value or d2.from\_value)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d2.to\_value → d2.from\_value.
      - If overlap\_exists\_between(range\_a, range\_b).
        - Evaluate overlaps.append(list(d1, d2)).
- If overlaps.
  - Set company\_currency from Enterprise.get\_company\_currency(self.company).
  - Evaluate msgprint(translated “Overlapping conditions found between:”).
  - Set messages from list().
  - For each tuple(d1, d2) in overlaps.
    - Evaluate messages.append(((formatted text {d1.from\_value}-{d1.to\_value} = {fmt\_money(d1.shipping\_amount, currency = company\_currency)}  + translated “and”) + formatted text  {d2.from\_value}-{d2.to\_value} = {fmt\_mon ….
  - Evaluate msgprint(whitespace '\\n'.join(messages), raise\_exception = OverlappingConditionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0188.json#L6399) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L201)

<a id="op-b3f1f5b59df898"></a>
### Shipping Rule.validate overlapping shipping rule conditions.overlap exists between

`operation_enterprise_accounts_record_definitions_shipping_rule_business_behavior_shipping_rule_validate_overlapping_shipping_rule_conditions_overlap_exists_between`

**Inputs** num\_range1, num\_range2.

**Explicit results** not separate.

**Local steps**

- Set tuple(tuple(x1, x2), tuple(y1, y2)) from tuple(num\_range1, num\_range2).
- Set separate from (x1 ≤ x2 ≤ y1 ≤ y2 or y1 ≤ y2 ≤ x1 ≤ x2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in x1 ≤ x2 ≤ y1 ≤ y2 → y1 ≤ y2 ≤ x1 ≤ x2.
  - Compare adjacent operands in order, stopping at the first false comparison in x1 ≤ x2 ≤ y1 ≤ y2.
  - Compare adjacent operands in order, stopping at the first false comparison in y1 ≤ y2 ≤ x1 ≤ x2.
- Return not separate.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L202)

<a id="op-3f9da2a7371a27"></a>
### Get data

`operation_enterprise_accounts_record_definitions_shipping_rule_shipping_rule_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “shipping\_rule”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “party\_name”), “transactions” → list(mapping(“label” → translated “Pre Sales”, “items” → list(“Quotation”, “Supp ….

**Local steps**

- Return mapping(“fieldname” → “shipping\_rule”, “non\_standard\_fieldnames” → mapping(“Payment Entry” → “party\_name”), “transactions” → list(mapping(“label” → translated “Pre Sales”, “items” → list(“Quotation”, “Supp ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L203)

## Record · Subscription

[Record definition](../../../../data/record-types/subscription.json)

<a id="op-fbeb1418590ed0"></a>
### Subscription.before insert

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.update\_subscription\_period(self.start\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update subscription period](operations-109.md#op-5fbc7699969fb3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L2232) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L215)

<a id="op-48d25d739589c1"></a>
### Subscription.after insert

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_after_insert`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.in\_import or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_import → Platform.flags.in\_migrate.
  - Return no value.
- If getdate(self.start\_date) &gt; getdate(nowdate()).
  - Return no value.
- Evaluate self.generate\_invoices\_till\_date().

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate invoices till date](operations-109.md#op-46b6e9c64af5d8).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L2292) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1420) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L214)

<a id="op-46b6e9c64af5d8"></a>
### Subscription.generate invoices till date

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_generate_invoices_till_date`

**Inputs** self.

**Declared result** no value.

**Local steps**

- While getdate(self.\_next\_invoice\_trigger\_date()) ≤ getdate(nowdate()).
  - Set period\_start from self.current\_invoice\_start.
  - Evaluate self.process(posting\_date = self.\_next\_invoice\_trigger\_date()).
  - If (self.status equals “Cancelled” or getdate(self.current\_invoice\_start) equals getdate(period\_start)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.status equals “Cancelled” → getdate(self.current\_invoice\_start) equals getdate(period\_start).
    - Leave the innermost loop without its normal-exhaustion alternative.
  - If not self.generate\_new\_invoices\_past\_due\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Methods declared on this owner** [next invoice trigger date](operations-109.md#op-cf223ac1e1f581), [process](operations-110.md#op-433d4fc1f906ef).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L223)

<a id="op-cf223ac1e1f581"></a>
### Subscription.next invoice trigger date

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_next_invoice_trigger_date`

**Inputs** self.

**Declared result** DateTimeLikeObject.

**Explicit results** self.current\_invoice\_start · add\_days(self.current\_invoice\_start, negative self.number\_of\_days) · self.current\_invoice\_end.

**Local steps**

- <a id="op-cf223ac1e1f581-guard-2"></a>If self.generate\_invoice\_at equals “Beginning of the current subscription period”.
  - Return self.current\_invoice\_start.
- If self.generate\_invoice\_at equals “Days before the current subscription period”.
  - Return add\_days(self.current\_invoice\_start, negative self.number\_of\_days).
- Return self.current\_invoice\_end.

**Derived branch illustrations**

- At the comparison self.generate\_invoice\_at equals “Beginning of the current subscription period”, self.generate\_invoice\_at = “Beginning of the current subscription period” selects the branch that returns self.current\_invoice\_start. With self.generate\_invoice\_at = “End of the current subscription period”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cf223ac1e1f581-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L238)

<a id="op-5fbc7699969fb3"></a>
### Subscription.update subscription period

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_update_subscription_period`

**Inputs** self, date = no value.

**Local steps**

- Set self.current\_invoice\_start from self.get\_current\_invoice\_start(date).
- Set self.current\_invoice\_end from self.get\_current\_invoice\_end(self.current\_invoice\_start).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current invoice start](operations-109.md#op-4766e113e482b7), [get current invoice end](operations-109.md#op-59eabb41990aee).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L243)

<a id="op-99c79ca8f84e55"></a>
### Subscription.get subscription period

`operation_enterprise_binding_enterprise_accounts_doctype_subscription_subscription_subscription_get_subscription_period`

**Inputs** self, date = no value.

**Explicit results** tuple(\_current\_invoice\_start, \_current\_invoice\_end).

**Local steps**

- Set \_current\_invoice\_start from self.get\_current\_invoice\_start(date).
- Set \_current\_invoice\_end from self.get\_current\_invoice\_end(\_current\_invoice\_start).
- Return tuple(\_current\_invoice\_start, \_current\_invoice\_end).

**Methods declared on this owner** [get current invoice start](operations-109.md#op-4766e113e482b7), [get current invoice end](operations-109.md#op-59eabb41990aee).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1081)

<a id="op-4766e113e482b7"></a>
### Subscription.get current invoice start

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_get_current_invoice_start`

**Inputs** self, date = no value.

**Declared result** DateTimeLikeObject.

**Explicit results** \_current\_invoice\_start.

**Local steps**

- Set \_current\_invoice\_start from no value.
- If (self.trial\_period\_end and getdate(self.trial\_period\_end) &gt; getdate(self.start\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trial\_period\_end → getdate(self.trial\_period\_end) &gt; getdate(self.start\_date).
  - Set \_current\_invoice\_start from add\_days(self.trial\_period\_end, 1).
- Otherwise.
  - If date.
    - Set \_current\_invoice\_start from date.
  - Otherwise.
    - If (self.trial\_period\_start and self.is\_trialling()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trial\_period\_start → self.is\_trialling().
      - Set \_current\_invoice\_start from self.trial\_period\_start.
    - Otherwise.
      - Set \_current\_invoice\_start from nowdate().
- Return \_current\_invoice\_start.

**Methods declared on this owner** [is trialling](operations-109.md#op-5b422ad362f5eb).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L3071) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L228)

<a id="op-59eabb41990aee"></a>
### Subscription.get current invoice end

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_get_current_invoice_end`

**Inputs** self, date = no value.

**Declared result** DateTimeLikeObject.

**Explicit results** \_current\_invoice\_end.

**Local steps**

- Set \_current\_invoice\_end from no value.
- If (self.is\_trialling() and getdate(date) &lt; getdate(self.trial\_period\_end)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_trialling() → getdate(date) &lt; getdate(self.trial\_period\_end).
  - Set \_current\_invoice\_end from self.trial\_period\_end.
- Otherwise.
  - Set billing\_cycle\_info from self.get\_billing\_cycle\_data().
  - If billing\_cycle\_info.
    - If getdate(self.start\_date) &lt; getdate(date).
      - Set \_current\_invoice\_end from add\_to\_date(self.start\_date, expanded names billing\_cycle\_info).
      - If getdate(self.current\_invoice\_end) &lt; getdate(date).
        - Set \_current\_invoice\_end from add\_to\_date(date, expanded names billing\_cycle\_info).
    - Otherwise.
      - Set \_current\_invoice\_end from add\_to\_date(date, expanded names billing\_cycle\_info).
  - Otherwise.
    - Set \_current\_invoice\_end from get\_last\_day(date).
  - If self.follow\_calendar\_months.
    - Set billing\_info from self.get\_billing\_cycle\_and\_interval().
    - Set billing\_interval\_count from billing\_info at 0 at “billing\_interval\_count”.
    - Set \_end from add\_months(getdate(date), (billing\_interval\_count − 1)).
    - Set \_current\_invoice\_end from get\_last\_day(\_end).
  - If (self.end\_date and getdate(\_current\_invoice\_end) &gt; getdate(self.end\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(\_current\_invoice\_end) &gt; getdate(self.end\_date).
    - Set \_current\_invoice\_end from self.end\_date.
- Return \_current\_invoice\_end.

**Methods declared on this owner** [is trialling](operations-109.md#op-5b422ad362f5eb), [get billing cycle data](operations-109.md#op-6c8d44f486b90d), [get billing cycle and interval](operations-109.md#op-8a98940c863f9a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L227)

<a id="op-9377706ddc0401"></a>
### Subscription.validate plans billing cycle

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_validate_plans_billing_cycle`

**Inputs** billing\_cycle\_data.

**Wrappers, in declaration order** staticmethod.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “You can only have Plans with the same billing cycle in a Subscription”.

**Local steps**

- If (billing\_cycle\_data and len(billing\_cycle\_data) differs from 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in billing\_cycle\_data → len(billing\_cycle\_data) differs from 1.
  - Call the validation error handler Platform.throw(translated “You can only have Plans with the same billing cycle in a Subscription”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L4030) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L247)

<a id="op-8a98940c863f9a"></a>
### Subscription.get billing cycle and interval

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_get_billing_cycle_and_interval`

**Inputs** self.

**Declared result** list at dict at tuple(str, str).

**Explicit results** billing\_info.

**Local steps**

- Set plan\_names from list of plan.plan for plan drawn from self.plans.
  - Draw plan from self.plans.
- Set subscription\_plan from Platform.qb.DocType(“Subscription Plan”).
- Set billing\_info from nested operand in the contract(nested operand in the contract, nested operand in the contract).distinct().where(subscription\_plan.name.isin(plan\_names)).run(as\_dict = 1).
- Return billing\_info.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L4180) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L224)

<a id="op-6c8d44f486b90d"></a>
### Subscription.get billing cycle data

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_get_billing_cycle_data`

**Inputs** self.

**Declared result** dict at tuple(str, int).

**Explicit results** no value · data.

**Local steps**

- Set billing\_info from self.get\_billing\_cycle\_and\_interval().
- If not billing\_info.
  - Return no value.
- Set data from dict().
- Set interval from billing\_info at 0 at “billing\_interval”.
- Set interval\_count from billing\_info at 0 at “billing\_interval\_count”.
- If interval does not belong to list(“Day”, “Week”).
  - Set data at “days” from negative 1.
- If interval equals “Day”.
  - Set data at “days” from (interval\_count − 1).
- Otherwise.
  - If interval equals “Week”.
    - Set data at “days” from ((interval\_count × 7) − 1).
  - Otherwise.
    - If interval equals “Month”.
      - Set data at “months” from interval\_count.
    - Otherwise.
      - If interval equals “Year”.
        - Set data at “years” from interval\_count.
- Return data.

**Methods declared on this owner** [get billing cycle and interval](operations-109.md#op-8a98940c863f9a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L4453) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L225)

<a id="op-5cf3016af925a1"></a>
### Subscription.set subscription status

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_set_subscription_status`

**Inputs** self, posting\_date = no value.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- <a id="op-5cf3016af925a1-guard-5"></a>If self.status equals “Cancelled”.
  - Return no value.
- If self.is\_trialling().
  - Set self.status from “Trialing”.
- Otherwise.
  - If (not self.has\_outstanding\_invoice() and self.end\_date and getdate(posting\_date) &gt; getdate(self.end\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_outstanding\_invoice() → self.end\_date → getdate(posting\_date) &gt; getdate(self.end\_date).
    - Set self.status from “Completed”.
  - Otherwise.
    - If self.is\_past\_grace\_period().
      - Set self.status from self.get\_status\_for\_past\_grace\_period().
      - Set self.cancelation\_date from getdate(posting\_date) when self.status equals “Cancelled”, otherwise no value.
        - Value choice on self.status equals “Cancelled” — true gives getdate(posting\_date), false gives no value.
    - Otherwise.
      - If (self.current\_invoice\_is\_past\_due() and not self.is\_past\_grace\_period()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.current\_invoice\_is\_past\_due() → not self.is\_past\_grace\_period().
        - Set self.status from “Grace Period”.
      - Otherwise.
        - If not self.has\_outstanding\_invoice().
          - Set self.status from “Active”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Cancelled”, self.status = “Cancelled” selects the branch that returns no value. With self.status = “Trialing”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5cf3016af925a1-guard-5)

**Methods declared on this owner** [is trialling](operations-109.md#op-5b422ad362f5eb), [has outstanding invoice](operations-110.md#op-c95693ff057d58), [is past grace period](operations-109.md#op-c51a51a316d3a2), [get status for past grace period](operations-109.md#op-f91ed65334636e), [current invoice is past due](operations-109.md#op-7c73afb931c8c9).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L242)

<a id="op-5b422ad362f5eb"></a>
### Subscription.is trialling

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_is_trialling`

**Inputs** self.

**Declared result** bool.

**Explicit results** not self.period\_has\_passed(self.trial\_period\_end).

**Local steps**

- Return not self.period\_has\_passed(self.trial\_period\_end).

**Methods declared on this owner** [period has passed](operations-109.md#op-c792caaa556d0d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L5702) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L237)

<a id="op-c792caaa556d0d"></a>
### Subscription.period has passed

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_period_has_passed`

**Inputs** end\_date, posting\_date = no value.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** true · getdate(posting\_date) &gt; getdate(end\_date).

**Local steps**

- If not end\_date.
  - Return true.
- Return getdate(posting\_date) &gt; getdate(end\_date).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L5768) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L239)

<a id="op-f91ed65334636e"></a>
### Subscription.get status for past grace period

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_get_status_for_past_grace_period`

**Inputs** self.

**Declared result** str.

**Record and data access** read “Subscription Settings” via get\_value.

**Explicit results** status.

**Local steps**

- Set cancel\_after\_grace from cint(Platform.get\_value(“Subscription Settings”, no value, “cancel\_after\_grace”)).
- Set status from “Unpaid”.
- If cancel\_after\_grace.
  - Set status from “Cancelled”.
- Return status.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L230)

<a id="op-c51a51a316d3a2"></a>
### Subscription.is past grace period

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_is_past_grace_period`

**Inputs** self, posting\_date = no value.

**Declared result** bool.

**Record and data access** read “Subscription Settings” via get\_value.

**Explicit results** false · getdate(posting\_date) &gt; getdate(add\_days(self.current\_invoice.due\_date, grace\_period)).

**Local steps**

- If not self.current\_invoice\_is\_past\_due(posting\_date).
  - Return false.
- Set grace\_period from cint(Platform.get\_value(“Subscription Settings”, no value, “grace\_period”)).
- Return getdate(posting\_date) &gt; getdate(add\_days(self.current\_invoice.due\_date, grace\_period)).

**Methods declared on this owner** [current invoice is past due](operations-109.md#op-7c73afb931c8c9).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L236)

<a id="op-7c73afb931c8c9"></a>
### Subscription.current invoice is past due

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_current_invoice_is_past_due`

**Inputs** self, posting\_date = no value.

**Declared result** bool.

**Explicit results** false · getdate(posting\_date) &gt; getdate(self.current\_invoice.due\_date).

**Local steps**

- If (not self.current\_invoice or self.is\_paid(self.current\_invoice)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.current\_invoice → self.is\_paid(self.current\_invoice).
  - Return false.
- If not self.current\_invoice.due\_date.
  - Return false.
- Return getdate(posting\_date) &gt; getdate(self.current\_invoice.due\_date).

**Methods declared on this owner** [is paid](operations-110.md#op-ad06acf560c918).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L220)

<a id="op-2c296002b65e3a"></a>
### Subscription.invoice document type

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_invoice_document_type`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** “Sales Invoice” when self.party\_type equals “Customer”, otherwise “Purchase Invoice”.

**Local steps**

- Return “Sales Invoice” when self.party\_type equals “Customer”, otherwise “Purchase Invoice”.
  - Value choice on self.party\_type equals “Customer” — true gives “Sales Invoice”, false gives “Purchase Invoice”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L232)

<a id="op-4638239f272123"></a>
### Subscription.validate

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_validate`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.validate\_trial\_period().
- Evaluate self.validate\_plans\_billing\_cycle(self.get\_billing\_cycle\_and\_interval()).
- Evaluate self.validate\_end\_date().
- Evaluate self.validate\_to\_follow\_calendar\_months().
- If not self.cost\_center.
  - Set self.cost\_center from get\_default\_cost\_center(self.get(“company”)).
- If self.is\_new().
  - Evaluate self.set\_subscription\_status().
- Evaluate self.validate\_party\_billing\_currency().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate trial period](operations-110.md#op-da9fa5fc9bd2fc), [validate plans billing cycle](operations-109.md#op-9377706ddc0401), [get billing cycle and interval](operations-109.md#op-8a98940c863f9a), [validate end date](operations-110.md#op-fe3bd2f4523f73), [validate to follow calendar months](operations-110.md#op-0454c139646343), [set subscription status](operations-109.md#op-5cf3016af925a1), [validate party billing currency](operations-109.md#op-fac010f7416b46).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0189.json#L6540) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L244)

<a id="op-fac010f7416b46"></a>
### Subscription.validate party billing currency

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_validate_party_billing_currency`

**Inputs** self.

**Record and data access** read self.party\_type via get\_cached\_value · read “Company” via get\_cached\_value · read “Subscription Plan” via get\_all.

**Explicit failure paths** validation helper with Platform.ValidationError — unsupported\_plans.

**Local steps**

- If self.party.
  - Set party\_billing\_currency from (Platform.get\_cached\_value(self.party\_type, self.party, “default\_currency”) or Platform.get\_cached\_value(“Company”, self.company, “default\_currency”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(self.party\_type, self.party, “default\_currency”) → Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
  - Set plans from list of x.plan for x drawn from self.plans.
    - Draw x from self.plans.
  - Set subscription\_plan\_currencies from Platform.db.get\_all(“Subscription Plan”, filters = mapping(“name” → tuple(“in”, plans)), fields = list(“name”, “currency”)).
  - Set unsupported\_plans from list().
  - For each x in subscription\_plan\_currencies.
    - If x.currency differs from party\_billing\_currency.
      - Evaluate unsupported\_plans.append(“{}”.format(get\_link\_to\_form(“Subscription Plan”, x.name))).
  - If unsupported\_plans.
    - Set unsupported\_plans from list(translated “Below Subscription Plans are of different currency to the party default billing currency/Company currency: {0}”.format(Platform.bold(party\_billing\_currency)), expanded unsupported\_plans).
    - Call the validation error handler Platform.throw(unsupported\_plans, Platform.ValidationError, “Unsupported Subscription Plans”, as\_list = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(self.party\_type, self.party, “default\_currency”), Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0190.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L246)
