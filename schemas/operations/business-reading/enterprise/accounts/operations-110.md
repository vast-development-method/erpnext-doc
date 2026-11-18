# Accounting and settlement · operations 110

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Subscription

[Record definition](../../../../data/record-types/subscription.json)

<a id="op-da9fa5fc9bd2fc"></a>
### Subscription.validate trial period

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_validate_trial_period`

**Inputs** self.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Trial Period End Date Cannot be before Trial Period Start Date” · validation helper — translated “Both Trial Period Start Date and Trial Period End Date must be set” · validation helper — translated “Trial Period Start date cannot be after Subscription Start Date”.

**Local steps**

- If (self.trial\_period\_start and self.trial\_period\_end).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trial\_period\_start → self.trial\_period\_end.
  - If getdate(self.trial\_period\_end) &lt; getdate(self.trial\_period\_start).
    - Call the validation error handler Platform.throw(translated “Trial Period End Date Cannot be before Trial Period Start Date”).
- If (self.trial\_period\_start and not self.trial\_period\_end).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trial\_period\_start → not self.trial\_period\_end.
  - Call the validation error handler Platform.throw(translated “Both Trial Period Start Date and Trial Period End Date must be set”).
- If (self.trial\_period\_start and getdate(self.trial\_period\_start) &gt; getdate(self.start\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.trial\_period\_start → getdate(self.trial\_period\_start) &gt; getdate(self.start\_date).
  - Call the validation error handler Platform.throw(translated “Trial Period Start date cannot be after Subscription Start Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0190.json#L542) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L249)

<a id="op-fe3bd2f4523f73"></a>
### Subscription.validate end date

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_validate_end_date`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Subscription End Date must be after {0} as per the subscription plan”.format(end\_date).

**Local steps**

- If not self.plans.
  - Return no value.
- Set billing\_cycle\_info from self.get\_billing\_cycle\_data().
- If not billing\_cycle\_info.
  - Return no value.
- Set end\_date from add\_to\_date(self.start\_date, expanded names billing\_cycle\_info).
- If (self.end\_date and getdate(self.end\_date) ≤ getdate(end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(self.end\_date) ≤ getdate(end\_date).
  - Call the validation error handler Platform.throw(translated “Subscription End Date must be after {0} as per the subscription plan”.format(end\_date)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get billing cycle data](operations-109.md#op-6c8d44f486b90d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0190.json#L873) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L245)

<a id="op-0454c139646343"></a>
### Subscription.validate to follow calendar months

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_validate_to_follow_calendar_months`

**Inputs** self.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Subscription End Date is mandatory to follow calendar months” · validation helper — translated “Billing Interval in Subscription Plan must be Month to follow calendar months”.

**Local steps**

- If not self.follow\_calendar\_months.
  - Return no value.
- Set billing\_info from self.get\_billing\_cycle\_and\_interval().
- If not self.end\_date.
  - Call the validation error handler Platform.throw(translated “Subscription End Date is mandatory to follow calendar months”).
- If billing\_info at 0 at “billing\_interval” differs from “Month”.
  - Call the validation error handler Platform.throw(translated “Billing Interval in Subscription Plan must be Month to follow calendar months”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get billing cycle and interval](operations-109.md#op-8a98940c863f9a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0190.json#L1135) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L248)

<a id="op-29e2a8a4af0813"></a>
### Subscription.generate invoice

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_generate_invoice`

**Inputs** self, from\_date = no value, to\_date = no value, posting\_date = no value.

**Declared result** Document.

**Explicit results** self.create\_invoice(from\_date = from\_date, to\_date = to\_date, posting\_date = posting\_date).

**Local steps**

- Return self.create\_invoice(from\_date = from\_date, to\_date = to\_date, posting\_date = posting\_date).

**Methods declared on this owner** [create invoice](operations-110.md#op-f9bbed24f1c908).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0190.json#L1351) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L222)

<a id="op-f9bbed24f1c908"></a>
### Subscription.create invoice

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_create_invoice`

**Inputs** self, from\_date = no value, to\_date = no value, posting\_date = no value.

**Declared result** Document.

**Record and data access** read “Supplier” via get\_cached\_value · read “Subscription Plan” via get\_value.

**State and service calls** request new\_doc for self.invoice\_document\_type · call save on invoice · call submit on invoice.

**Explicit results** invoice.

**Explicit failure paths** validation helper — translated “Company is mandatory for generating an invoice. Please set a default company in Global Defaults.”.

**Local steps**

- Set company from (self.get(“company”) or get\_default\_company()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“company”) → get\_default\_company().
- If not company.
  - Call the validation error handler Platform.throw(translated “Company is mandatory for generating an invoice. Please set a default company in Global Defaults.”).
- Set invoice from Platform.new\_doc(self.invoice\_document\_type).
- Set invoice.company from company.
- Set invoice.set\_posting\_time from 1.
- If self.generate\_invoice\_at equals “Beginning of the current subscription period”.
  - Set invoice.posting\_date from self.current\_invoice\_start.
- Otherwise.
  - If self.generate\_invoice\_at equals “Days before the current subscription period”.
    - Set invoice.posting\_date from (posting\_date or self.current\_invoice\_start).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in posting\_date → self.current\_invoice\_start.
  - Otherwise.
    - Set invoice.posting\_date from self.current\_invoice\_end.
- Set invoice.cost\_center from self.cost\_center.
- If self.invoice\_document\_type equals “Sales Invoice”.
  - Set invoice.customer from self.party.
- Otherwise.
  - Set invoice.supplier from self.party.
  - Set tuple(tax\_withholding\_category, tax\_withholding\_group) from Platform.get\_cached\_value(“Supplier”, self.party, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).
  - If (tax\_withholding\_category or tax\_withholding\_group).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_withholding\_category → tax\_withholding\_group.
    - Set invoice.apply\_tds from 1.
- Set invoice.currency from Platform.db.get\_value(“Subscription Plan”, mapping(“name” → self.plans at 0.plan), “currency”).
- Set accounting\_dimensions from get\_accounting\_dimensions().
- For each dimension in accounting\_dimensions.
  - If self.get(dimension).
    - Evaluate invoice.update(mapping(dimension → self.get(dimension))).
- Set items\_list from self.get\_items\_from\_plans(self.plans, is\_prorate()).
- For each item in items\_list.
  - Evaluate invoice.append(“items”, item).
- Set tax\_template from empty text.
- If (self.invoice\_document\_type equals “Sales Invoice” and self.sales\_tax\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.invoice\_document\_type equals “Sales Invoice” → self.sales\_tax\_template.
  - Set tax\_template from self.sales\_tax\_template.
- If (self.invoice\_document\_type equals “Purchase Invoice” and self.purchase\_tax\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.invoice\_document\_type equals “Purchase Invoice” → self.purchase\_tax\_template.
  - Set tax\_template from self.purchase\_tax\_template.
- If tax\_template.
  - Set invoice.taxes\_and\_charges from tax\_template.
  - Evaluate invoice.set\_taxes().
- If self.days\_until\_due.
  - Evaluate invoice.append(“payment\_schedule”, mapping(“due\_date” → add\_days(invoice.posting\_date, cint(self.days\_until\_due)), “invoice\_portion” → 100)).
- If self.is\_trialling().
  - Set invoice.additional\_discount\_percentage from 100.
- Otherwise.
  - If self.additional\_discount\_percentage.
    - Set invoice.additional\_discount\_percentage from self.additional\_discount\_percentage.
  - If self.additional\_discount\_amount.
    - Set invoice.discount\_amount from self.additional\_discount\_amount.
  - If (self.additional\_discount\_percentage or self.additional\_discount\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.additional\_discount\_percentage → self.additional\_discount\_amount.
    - Set discount\_on from self.apply\_additional\_discount.
    - Set invoice.apply\_discount\_on from discount\_on when discount\_on, otherwise “Grand Total”.
      - Value choice on discount\_on — true gives discount\_on, false gives “Grand Total”.
- Set invoice.subscription from self.name.
- Set invoice.from\_date from (from\_date or self.current\_invoice\_start).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → self.current\_invoice\_start.
- Set invoice.to\_date from (to\_date or self.current\_invoice\_end).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → self.current\_invoice\_end.
- Set invoice.flags.ignore\_mandatory from true.
- Evaluate invoice.set\_missing\_values().
- Evaluate invoice.save().
- If self.submit\_invoice.
  - Evaluate invoice.submit().
- Return invoice.

**Methods declared on this owner** [get items from plans](operations-110.md#op-77621530137c6f), [is trialling](operations-109.md#op-5b422ad362f5eb).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Supplier”, self.party, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L218)

<a id="op-77621530137c6f"></a>
### Subscription.get items from plans

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_get_items_from_plans`

**Inputs** self, plans, prorate = 0.

**Declared result** list at dict.

**Record and data access** resolve a document from “Subscription Plan” via get\_doc · read “Item” via get\_value.

**Explicit results** items.

**Local steps**

- Set prorate\_factor from 1.
- If prorate.
  - Set prorate\_factor from get\_prorata\_factor(self.current\_invoice\_end, self.current\_invoice\_start, cint(self.generate\_invoice\_at belongs to list(“Beginning of the current subscription period”, “Days before the current subscription period”))).
- Set items from list().
- Set party from self.party.
- For each plan in plans.
  - Set plan\_doc from Platform.get\_doc(“Subscription Plan”, plan.plan).
  - Set item\_code from plan\_doc.item.
  - If self.party\_type equals “Customer”.
    - Set deferred\_field from “enable\_deferred\_revenue”.
  - Otherwise.
    - Set deferred\_field from “enable\_deferred\_expense”.
  - Set deferred from Platform.db.get\_value(“Item”, item\_code, deferred\_field).
  - Set item from mapping(“item\_code” → item\_code, “qty” → plan.qty, “rate” → get\_plan\_rate(plan.plan, plan.qty, party, self.current\_invoice\_start, …), “cost\_center” → plan\_doc.cost\_center).
  - If deferred.
    - Evaluate item.update(mapping(deferred\_field → deferred, “service\_start\_date” → self.current\_invoice\_start, “service\_end\_date” → self.current\_invoice\_end)).
  - Set accounting\_dimensions from get\_accounting\_dimensions().
  - For each dimension in accounting\_dimensions.
    - If plan\_doc.get(dimension).
      - Evaluate item.update(mapping(dimension → plan\_doc.get(dimension))).
  - Evaluate items.append(item).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1443) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L229)

<a id="op-433d4fc1f906ef"></a>
### Subscription.process

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_process`

**Inputs** self, posting\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**State and service calls** call save on self.

**Explicit results** no value.

**Local steps**

- Set current\_period\_end from self.current\_invoice\_end.
- If (not self.is\_current\_invoice\_generated(self.current\_invoice\_start, self.current\_invoice\_end) and self.can\_generate\_new\_invoice(posting\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_current\_invoice\_generated(self.current\_invoice\_start, self.current\_invoice\_end) → self.can\_generate\_new\_invoice(posting\_date).
  - Evaluate self.generate\_invoice(posting\_date = posting\_date).
  - If self.end\_date.
    - Set next\_start from add\_days(self.current\_invoice\_end, 1).
    - If getdate(next\_start) &gt; getdate(self.end\_date).
      - If self.cancel\_at\_period\_end.
        - Evaluate self.cancel\_subscription().
      - Otherwise.
        - Evaluate self.set\_subscription\_status(posting\_date = posting\_date).
      - Evaluate self.save().
      - Return no value.
  - Evaluate self.update\_subscription\_period(add\_days(self.current\_invoice\_end, 1)).
- Otherwise.
  - If (posting\_date and getdate(posting\_date) &gt; getdate(self.current\_invoice\_end)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in posting\_date → getdate(posting\_date) &gt; getdate(self.current\_invoice\_end).
    - If not (self.end\_date and getdate(self.current\_invoice\_end) ≥ getdate(self.end\_date)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(self.current\_invoice\_end) ≥ getdate(self.end\_date).
      - Evaluate self.update\_subscription\_period().
- If (self.cancel\_at\_period\_end and (getdate(posting\_date) ≥ getdate(current\_period\_end) or (self.end\_date and getdate(posting\_date) ≥ getdate(self.end\_date)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.cancel\_at\_period\_end → (getdate(posting\_date) ≥ getdate(current\_period\_end) or (self.end\_date and getdate(posting\_date) ≥ getdate(self.end\_date))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(posting\_date) ≥ getdate(current\_period\_end) → (self.end\_date and getdate(posting\_date) ≥ getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(posting\_date) ≥ getdate(self.end\_date).
  - Evaluate self.cancel\_subscription().
- Evaluate self.set\_subscription\_status(posting\_date = posting\_date).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is current invoice generated](operations-110.md#op-146641bfaed87c), [can generate new invoice](operations-110.md#op-5884b342b1c9e8), [generate invoice](operations-110.md#op-29e2a8a4af0813), [cancel subscription](operations-110.md#op-e4dbf2ac7db113), [set subscription status](operations-109.md#op-5cf3016af925a1), [update subscription period](operations-109.md#op-5fbc7699969fb3).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L240)

<a id="op-5884b342b1c9e8"></a>
### Subscription.can generate new invoice

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_can_generate_new_invoice`

**Inputs** self, posting\_date = no value.

**Declared result** bool.

**Explicit results** false · posting ≤ upper.

**Local steps**

- If self.cancelation\_date.
  - Return false.
- If (self.has\_outstanding\_invoice() and not self.generate\_new\_invoices\_past\_due\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_outstanding\_invoice() → not self.generate\_new\_invoices\_past\_due\_date.
  - Return false.
- Set posting from getdate(posting\_date).
- Set trigger from getdate(self.\_next\_invoice\_trigger\_date()).
- If posting &lt; trigger.
  - Return false.
- Set billing\_cycle\_info from self.get\_billing\_cycle\_data().
- If billing\_cycle\_info.
  - Set upper from getdate(add\_to\_date(self.current\_invoice\_end, expanded names billing\_cycle\_info)).
- Otherwise.
  - Set upper from getdate(self.current\_invoice\_end).
- Return posting ≤ upper.

**Methods declared on this owner** [has outstanding invoice](operations-110.md#op-c95693ff057d58), [next invoice trigger date](operations-109.md#op-cf223ac1e1f581), [get billing cycle data](operations-109.md#op-6c8d44f486b90d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L216)

<a id="op-146641bfaed87c"></a>
### Subscription.is current invoice generated

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_is_current_invoice_generated`

**Inputs** self, \_current\_start\_date = no value, \_current\_end\_date = no value.

**Declared result** bool.

**Explicit results** true · getdate(invoice.from\_date) equals getdate(\_current\_start\_date) · getdate(\_current\_start\_date) ≤ getdate(invoice.posting\_date) ≤ getdate(\_current\_end\_date) · false.

**Local steps**

- If not (\_current\_start\_date and \_current\_end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_current\_start\_date → \_current\_end\_date.
  - Set tuple(\_current\_start\_date, \_current\_end\_date) from self.\_get\_subscription\_period(date = add\_days(self.current\_invoice\_end, 1)).
- If (self.end\_date and getdate(\_current\_start\_date) &gt; getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(\_current\_start\_date) &gt; getdate(self.end\_date).
  - Return true.
- Set invoice from self.current\_invoice.
- If invoice.
  - If invoice.get(“from\_date”).
    - Return getdate(invoice.from\_date) equals getdate(\_current\_start\_date).
  - Otherwise.
    - If invoice.get(“posting\_date”).
      - Return getdate(\_current\_start\_date) ≤ getdate(invoice.posting\_date) ≤ getdate(\_current\_end\_date).
        - Compare adjacent operands in order, stopping at the first false comparison in getdate(\_current\_start\_date) ≤ getdate(invoice.posting\_date) ≤ getdate(\_current\_end\_date).
- Return false.

**Methods declared on this owner** [get subscription period](operations-109.md#op-99c79ca8f84e55).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L234)

<a id="op-4e54284493a360"></a>
### Subscription.current invoice

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_current_invoice`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** (Document bitwise or no value).

**Explicit results** self.get\_current\_invoice().

**Local steps**

- Return self.get\_current\_invoice().

**Methods declared on this owner** [get current invoice](operations-110.md#op-0e43697710c419).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0190.json#L6050) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L219)

<a id="op-0e43697710c419"></a>
### Subscription.get current invoice

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_get_current_invoice`

**Inputs** self.

**Declared result** (Document bitwise or no value).

**Record and data access** read self.invoice\_document\_type via get\_all · resolve a document from self.invoice\_document\_type via get\_doc.

**Explicit results** Platform.get\_doc(self.invoice\_document\_type, invoice at 0).

**Local steps**

- Set invoice from Platform.get\_all(self.invoice\_document\_type, mapping(“subscription” → self.name, “docstatus” → tuple(“&lt;”, 2)), limit = 1, order\_by = “to\_date desc”, pluck = “name”).
- If invoice.
  - Return Platform.get\_doc(self.invoice\_document\_type, invoice at 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L226)

<a id="op-407ba484c71af6"></a>
### Subscription.invoices

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_invoices`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** list at dict.

**Record and data access** read self.invoice\_document\_type via get\_all.

**Explicit results** Platform.get\_all(self.invoice\_document\_type, filters = mapping(“subscription” → self.name), order\_by = “from\_date asc”).

**Local steps**

- Return Platform.get\_all(self.invoice\_document\_type, filters = mapping(“subscription” → self.name), order\_by = “from\_date asc”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0190.json#L6342) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L233)

<a id="op-ad06acf560c918"></a>
### Subscription.is paid

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_is_paid`

**Inputs** invoice.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** invoice.status equals “Paid”.

**Local steps**

- Return invoice.status equals “Paid”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L235)

<a id="op-c95693ff057d58"></a>
### Subscription.has outstanding invoice

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_has_outstanding_invoice`

**Inputs** self.

**Declared result** int.

**Record and data access** read self.invoice\_document\_type via count.

**Explicit results** Platform.db.count(self.invoice\_document\_type, mapping(“subscription” → self.name, “docstatus” → 1, “status” → list(“!=”, “Paid”))).

**Local steps**

- Return Platform.db.count(self.invoice\_document\_type, mapping(“subscription” → self.name, “docstatus” → 1, “status” → list(“!=”, “Paid”))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L231)

<a id="op-e4dbf2ac7db113"></a>
### Subscription.cancel subscription

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_cancel_subscription`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**State and service calls** call save on self.

**Explicit failure paths** validation helper with InvoiceCancelled — translated “subscription is already cancelled.”.

**Local steps**

- <a id="op-e4dbf2ac7db113-guard-6"></a>If self.status equals “Cancelled”.
  - Call the validation error handler Platform.throw(translated “subscription is already cancelled.”, InvoiceCancelled).
- Set to\_generate\_invoice from true when (self.status equals “Active” and self.generate\_invoice\_at differs from “Beginning of the current subscription period”), otherwise false.
  - Value choice on (self.status equals “Active” and self.generate\_invoice\_at differs from “Beginning of the current subscription period”) — true gives true, false gives false.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Active” → self.generate\_invoice\_at differs from “Beginning of the current subscription period”.
- Set self.status from “Cancelled”.
- Set self.cancelation\_date from nowdate().
- If (to\_generate\_invoice and getdate(self.cancelation\_date) ≥ getdate(self.current\_invoice\_start)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_generate\_invoice → getdate(self.cancelation\_date) ≥ getdate(self.current\_invoice\_start).
  - Evaluate self.generate\_invoice(self.current\_invoice\_start, self.cancelation\_date).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Cancelled”, self.status = “Cancelled” selects the branch that calls the validation-error handler with translated “subscription is already cancelled.”. With self.status = “Trialing”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e4dbf2ac7db113-guard-6)

**Methods declared on this owner** [generate invoice](operations-110.md#op-29e2a8a4af0813).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L217)

<a id="op-b2d12439a4caef"></a>
### Subscription.restart subscription

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_restart_subscription`

**Inputs** self, posting\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**State and service calls** call save on self.

**Explicit failure paths** validation helper with InvoiceNotCancelled — translated “You cannot restart a Subscription that is not cancelled.”.

**Local steps**

- <a id="op-b2d12439a4caef-guard-7"></a>If self.status differs from “Cancelled”.
  - Call the validation error handler Platform.throw(translated “You cannot restart a Subscription that is not cancelled.”, InvoiceNotCancelled).
- Set self.status from “Active”.
- Set self.cancelation\_date from no value.
- Evaluate self.update\_subscription\_period((posting\_date or nowdate())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in posting\_date → nowdate().
- Evaluate self.save().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status differs from “Cancelled”, self.status = “Trialing” selects the branch that calls the validation-error handler with translated “You cannot restart a Subscription that is not cancelled.”. With self.status = “Cancelled”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-b2d12439a4caef-guard-7)

**Methods declared on this owner** [update subscription period](operations-109.md#op-5fbc7699969fb3).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L241)

<a id="op-86fb280c3625df"></a>
### Subscription.force fetch subscription updates

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_subscription_force_fetch_subscription_updates`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Subscription for Future dates cannot be processed.”.

**Explicit results** no value.

**Local steps**

- If getdate(nowdate()) &lt; getdate(self.current\_invoice\_start).
  - Evaluate Platform.msgprint(translated “Subscription for Future dates cannot be processed.”).
  - Return no value.
- Set processing\_date from no value.
- If self.generate\_invoice\_at equals “Beginning of the current subscription period”.
  - Set processing\_date from self.current\_invoice\_start.
- Otherwise.
  - If self.generate\_invoice\_at equals “End of the current subscription period”.
    - Set processing\_date from self.current\_invoice\_end.
  - Otherwise.
    - If self.generate\_invoice\_at equals “Days before the current subscription period”.
      - Set processing\_date from add\_days(self.current\_invoice\_start, negative self.number\_of\_days).
- Evaluate self.process(posting\_date = processing\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [process](operations-110.md#op-433d4fc1f906ef).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L221)

<a id="op-31c9b43df49f74"></a>
### Is prorate

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_is_prorate`

**Inputs** no declared parameters.

**Declared result** int.

**Record and data access** read “Subscription Settings” via get\_single\_value.

**Explicit results** cint(Platform.db.get\_single\_value(“Subscription Settings”, “prorate”)).

**Local steps**

- Return cint(Platform.db.get\_single\_value(“Subscription Settings”, “prorate”)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Subscription Settings”, “prorate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0191.json#L2916) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L212)

<a id="op-fc91996d71b07a"></a>
### Get prorata factor

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_get_prorata_factor`

**Inputs** period\_end, period\_start, is\_prepaid = no value.

**Declared result** (int bitwise or float).

**Explicit results** 1 · (diff ÷ plan\_days).

**Local steps**

- If is\_prepaid.
  - Return 1.
- Set diff from flt((date\_diff(nowdate(), period\_start) + 1)).
- Set plan\_days from flt((date\_diff(period\_end, period\_start) + 1)).
- Return (diff ÷ plan\_days).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0191.json#L2997) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L211)

<a id="op-882d86a76e5096"></a>
### Get plan dimensions

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_get_plan_dimensions`

**Inputs** plan, company = no value, party\_type = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, str).

**Record and data access** resolve a document from “Subscription Plan” via get\_cached\_doc.

**Explicit results** dimensions.

**Local steps**

- Set plan\_doc from Platform.get\_cached\_doc(“Subscription Plan”, plan).
- Set dimensions from mapping().
- For each dimension in list(“cost\_center”, expanded get\_accounting\_dimensions()).
  - Set value from (plan\_doc.get(dimension) or get\_item\_dimension(plan\_doc.item, dimension, company, party\_type)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in plan\_doc.get(dimension) → get\_item\_dimension(plan\_doc.item, dimension, company, party\_type).
  - If value.
    - Set dimensions at dimension from value.
- Return dimensions.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Subscription Plan”, plan).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0191.json#L3222) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L210)

<a id="op-15afaaca886cc4"></a>
### Get item dimension

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_get_item_dimension`

**Inputs** item\_code, dimension, company, party\_type.

**Declared result** (str bitwise or no value).

**Explicit results** no value · item\_defaults.get(dimension) · (buying or selling) · (selling or buying).

**Local steps**

- If not company.
  - Return no value.
- Set item\_defaults from get\_item\_defaults(item\_code, company).
- If dimension differs from “cost\_center”.
  - Return item\_defaults.get(dimension).
- Set selling from item\_defaults.get(“selling\_cost\_center”).
- Set buying from item\_defaults.get(“buying\_cost\_center”).
- If party\_type equals “Supplier”.
  - Return (buying or selling).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in buying → selling.
- Return (selling or buying).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in selling → buying.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L209)

<a id="op-8979055bbcb556"></a>
### Process all

`operation_enterprise_accounts_record_definitions_subscription_business_behavior_process_all`

**Inputs** subscription, posting\_date = no value.

**Declared result** no value.

**Record and data access** resolve a document from “Subscription” via get\_doc.

**State and service calls** commit · rollback.

**Local steps**

- For each subscription\_name in subscription.
  - Attempt the following.
    - Set sub from Platform.get\_doc(“Subscription”, subscription\_name).
    - Evaluate sub.process(posting\_date).
    - If not Platform.in\_test.
      - Evaluate Platform.db.commit().
  - On failure (Platform.ValidationError).
    - Evaluate Platform.db.rollback().
    - Evaluate sub.log\_error(“Subscription failed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0191.json#L3860) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L213)

## Record · Subscription plan

[Record definition](../../../../data/record-types/subscription_plan.json)

<a id="op-9621725fd0bcb7"></a>
### Subscription Plan.validate

`operation_enterprise_accounts_record_definitions_subscription_plan_business_behavior_subscription_plan_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_interval\_count().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate interval count](operations-110.md#op-0b5cdb0cdba009).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0194.json#L3305) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L252)

<a id="op-0b5cdb0cdba009"></a>
### Subscription Plan.validate interval count

`operation_enterprise_accounts_record_definitions_subscription_plan_business_behavior_subscription_plan_validate_interval_count`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Billing Interval Count cannot be less than 1”.

**Local steps**

- <a id="op-0b5cdb0cdba009-guard-2"></a>If self.billing\_interval\_count &lt; 1.
  - Call the validation error handler Platform.throw(translated “Billing Interval Count cannot be less than 1”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.billing\_interval\_count &lt; 1, self.billing\_interval\_count = 0 selects the branch that calls the validation-error handler with translated “Billing Interval Count cannot be less than 1”. With self.billing\_interval\_count = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0b5cdb0cdba009-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0194.json#L3356) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L253)
