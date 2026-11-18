# Integrations and service calls · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Dashboard

<a id="op-cd6c184a3b56f4"></a>
### Get chart

`operation_relationships_application_interface_dashboard_business_behavior_get_chart`

**Inputs** name, type, from\_date = no value, to\_date = no value, user = no value.

**Wrappers, in declaration order** Platform.whitelist(), sales\_user\_only.

**Explicit results** method(from\_date, to\_date, user) · mapping(“error” → translated “Invalid chart name”).

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set roles from Platform.get\_roles(Platform.session.user).
- Set is\_sales\_manager from (“Sales Manager” belongs to roles or “System Manager” belongs to roles).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “Sales Manager” belongs to roles → “System Manager” belongs to roles.
- Set is\_sales\_user from (“Sales User” belongs to roles and not is\_sales\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “Sales User” belongs to roles → not is\_sales\_manager.
- If is\_sales\_user.
  - Set user from Platform.session.user.
- Set method\_name from formatted text get\_{name}.
- If hasattr(Platform.get\_attr(“crm.api.dashboard”), method\_name).
  - Set method from getattr(Platform.get\_attr(“crm.api.dashboard”), method\_name).
  - Return method(from\_date, to\_date, user).
- Otherwise.
  - Return mapping(“error” → translated “Invalid chart name”).

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate() · effective access from Platform.get\_roles(Platform.session.user) · selected callable from Platform.get\_attr(“crm.api.dashboard”), getattr(Platform.get\_attr(“crm.api.dashboard”), method\_name).

**Boundaries to resolve** late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L36) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L35)

<a id="op-b67daf0c507885"></a>
### Get total leads

`operation_relationships_application_interface_dashboard_business_behavior_get_total_leads`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Total leads”, “tooltip” → translated “Total number of leads”, “value” → current\_month\_leads, “delta” → delta\_in\_percentage, …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set Lead from DocType(“CRM Lead”).
- Set current\_cond from (Lead.creation ≥ from\_date bitwise and Lead.creation &lt; to\_date\_plus\_one).
- If user.
  - Set current\_cond from (current\_cond bitwise and Lead.lead\_owner equals user).
- Set prev\_cond from (Lead.creation ≥ prev\_from\_date bitwise and Lead.creation &lt; from\_date).
- If user.
  - Set prev\_cond from (prev\_cond bitwise and Lead.lead\_owner equals user).
- Set query from Platform.qb.from\_(Lead).select(Count(nested operand in the contract(nested operand in the contract, nested operand in the contract).else\_(no value)).as\_(“current\_month\_leads”), Count(nested operand in the  ….
- Set result from query.run(as\_dict = true).
- Set current\_month\_leads from (result at 0.current\_month\_leads or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_month\_leads → 0.
- Set prev\_month\_leads from (result at 0.prev\_month\_leads or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_month\_leads → 0.
- Set delta\_in\_percentage from (((current\_month\_leads − prev\_month\_leads) ÷ prev\_month\_leads) × 100) when prev\_month\_leads, otherwise 0.
  - Value choice on prev\_month\_leads — true gives (((current\_month\_leads − prev\_month\_leads) ÷ prev\_month\_leads) × 100), false gives 0.
- Return mapping(“title” → translated “Total leads”, “tooltip” → translated “Total number of leads”, “value” → current\_month\_leads, “delta” → delta\_in\_percentage, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0004.json#L1735) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L53) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L49)

<a id="op-f9eaa43b8e497e"></a>
### Get ongoing deals

`operation_relationships_application_interface_dashboard_business_behavior_get_ongoing_deals`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Ongoing deals”, “tooltip” → translated “Total number of non won/lost deals”, “value” → current\_month\_deals, “delta” → delta\_in\_percentage, …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set current\_cond from ((Deal.creation ≥ from\_date bitwise and Deal.creation &lt; to\_date\_plus\_one) bitwise and Status.type.notin(list(“Won”, “Lost”))).
- If user.
  - Set current\_cond from (current\_cond bitwise and Deal.deal\_owner equals user).
- Set prev\_cond from ((Deal.creation ≥ prev\_from\_date bitwise and Deal.creation &lt; from\_date) bitwise and Status.type.notin(list(“Won”, “Lost”))).
- If user.
  - Set prev\_cond from (prev\_cond bitwise and Deal.deal\_owner equals user).
- Set query from nested operand in the contract(nested operand in the contract).join(Status).on(Deal.status equals Status.name).select(Count(nested operand in the contract(nested operand in the contract, nested operand in  ….
- Set result from query.run(as\_dict = true).
- Set current\_month\_deals from (result at 0.current\_month\_deals or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_month\_deals → 0.
- Set prev\_month\_deals from (result at 0.prev\_month\_deals or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_month\_deals → 0.
- Set delta\_in\_percentage from (((current\_month\_deals − prev\_month\_deals) ÷ prev\_month\_deals) × 100) when prev\_month\_deals, otherwise 0.
  - Value choice on prev\_month\_deals — true gives (((current\_month\_deals − prev\_month\_deals) ÷ prev\_month\_deals) × 100), false gives 0.
- Return mapping(“title” → translated “Ongoing deals”, “tooltip” → translated “Total number of non won/lost deals”, “value” → current\_month\_deals, “delta” → delta\_in\_percentage, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0004.json#L2674) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L51) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L47)

<a id="op-1992bdbe569183"></a>
### Get average ongoing deal value

`operation_relationships_application_interface_dashboard_business_behavior_get_average_ongoing_deal_value`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Avg. ongoing deal value”, “tooltip” → translated “Average deal value of non won/lost deals”, “value” → current\_month\_avg\_value, “delta” → avg\_value\_delta, …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set current\_cond from ((Deal.creation ≥ from\_date bitwise and Deal.creation &lt; to\_date\_plus\_one) bitwise and Status.type.notin(list(“Won”, “Lost”))).
- If user.
  - Set current\_cond from (current\_cond bitwise and Deal.deal\_owner equals user).
- Set prev\_cond from ((Deal.creation ≥ prev\_from\_date bitwise and Deal.creation &lt; from\_date) bitwise and Status.type.notin(list(“Won”, “Lost”))).
- If user.
  - Set prev\_cond from (prev\_cond bitwise and Deal.deal\_owner equals user).
- Set deal\_value\_expr from (Deal.deal\_value × IfNull(Deal.exchange\_rate, 1)).
- Set query from nested operand in the contract(nested operand in the contract).join(Status).on(Deal.status equals Status.name).select(Avg(nested operand in the contract(nested operand in the contract, nested operand in th ….
- Set result from query.run(as\_dict = true).
- Set current\_month\_avg\_value from (result at 0.current\_month\_avg\_value or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_month\_avg\_value → 0.
- Set prev\_month\_avg\_value from (result at 0.prev\_month\_avg\_value or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_month\_avg\_value → 0.
- Set avg\_value\_delta from (current\_month\_avg\_value − prev\_month\_avg\_value) when prev\_month\_avg\_value, otherwise 0.
  - Value choice on prev\_month\_avg\_value — true gives (current\_month\_avg\_value − prev\_month\_avg\_value), false gives 0.
- Return mapping(“title” → translated “Avg. ongoing deal value”, “tooltip” → translated “Average deal value of non won/lost deals”, “value” → current\_month\_avg\_value, “delta” → avg\_value\_delta, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0004.json#L3771) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L31) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L30)

<a id="op-4c588995026cac"></a>
### Get won deals

`operation_relationships_application_interface_dashboard_business_behavior_get_won_deals`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Won deals”, “tooltip” → translated “Total number of won deals based on its closure date”, “value” → current\_month\_deals, “delta” → delta\_in\_percentage, …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set current\_cond from ((Deal.closed\_date ≥ from\_date bitwise and Deal.closed\_date &lt; to\_date\_plus\_one) bitwise and Status.type equals “Won”).
- If user.
  - Set current\_cond from (current\_cond bitwise and Deal.deal\_owner equals user).
- Set prev\_cond from ((Deal.closed\_date ≥ prev\_from\_date bitwise and Deal.closed\_date &lt; from\_date) bitwise and Status.type equals “Won”).
- If user.
  - Set prev\_cond from (prev\_cond bitwise and Deal.deal\_owner equals user).
- Set query from nested operand in the contract(nested operand in the contract).join(Status).on(Deal.status equals Status.name).select(Count(nested operand in the contract(nested operand in the contract, nested operand in  ….
- Set result from query.run(as\_dict = true).
- Set current\_month\_deals from (result at 0.current\_month\_deals or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_month\_deals → 0.
- Set prev\_month\_deals from (result at 0.prev\_month\_deals or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_month\_deals → 0.
- Set delta\_in\_percentage from (((current\_month\_deals − prev\_month\_deals) ÷ prev\_month\_deals) × 100) when prev\_month\_deals, otherwise 0.
  - Value choice on prev\_month\_deals — true gives (((current\_month\_deals − prev\_month\_deals) ÷ prev\_month\_deals) × 100), false gives 0.
- Return mapping(“title” → translated “Won deals”, “tooltip” → translated “Total number of won deals based on its closure date”, “value” → current\_month\_deals, “delta” → delta\_in\_percentage, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0004.json#L4899) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L54) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L50)

<a id="op-8002d3ea8d0a58"></a>
### Get average won deal value

`operation_relationships_application_interface_dashboard_business_behavior_get_average_won_deal_value`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Avg. won deal value”, “tooltip” → translated “Average deal value of won deals”, “value” → current\_month\_avg\_value, “delta” → avg\_value\_delta, …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set current\_cond from ((Deal.closed\_date ≥ from\_date bitwise and Deal.closed\_date &lt; to\_date\_plus\_one) bitwise and Status.type equals “Won”).
- If user.
  - Set current\_cond from (current\_cond bitwise and Deal.deal\_owner equals user).
- Set prev\_cond from ((Deal.closed\_date ≥ prev\_from\_date bitwise and Deal.closed\_date &lt; from\_date) bitwise and Status.type equals “Won”).
- If user.
  - Set prev\_cond from (prev\_cond bitwise and Deal.deal\_owner equals user).
- Set deal\_value\_expr from (Deal.deal\_value × IfNull(Deal.exchange\_rate, 1)).
- Set query from nested operand in the contract(nested operand in the contract).join(Status).on(Deal.status equals Status.name).select(Avg(nested operand in the contract(nested operand in the contract, nested operand in th ….
- Set result from query.run(as\_dict = true).
- Set current\_month\_avg\_value from (result at 0.current\_month\_avg\_value or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_month\_avg\_value → 0.
- Set prev\_month\_avg\_value from (result at 0.prev\_month\_avg\_value or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_month\_avg\_value → 0.
- Set avg\_value\_delta from (current\_month\_avg\_value − prev\_month\_avg\_value) when prev\_month\_avg\_value, otherwise 0.
  - Value choice on prev\_month\_avg\_value — true gives (current\_month\_avg\_value − prev\_month\_avg\_value), false gives 0.
- Return mapping(“title” → translated “Avg. won deal value”, “tooltip” → translated “Average deal value of won deals”, “value” → current\_month\_avg\_value, “delta” → avg\_value\_delta, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0004.json#L5963) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L34) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L33)

<a id="op-08119330daa1e8"></a>
### Get average deal value

`operation_relationships_application_interface_dashboard_business_behavior_get_average_deal_value`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Avg. deal value”, “tooltip” → translated “Average deal value of ongoing &amp; won deals”, “value” → current\_month\_avg, “prefix” → get\_base\_currency\_symbol(), …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set current\_cond from ((Deal.creation ≥ from\_date bitwise and Deal.creation &lt; to\_date\_plus\_one) bitwise and Status.type differs from “Lost”).
- If user.
  - Set current\_cond from (current\_cond bitwise and Deal.deal\_owner equals user).
- Set prev\_cond from ((Deal.creation ≥ prev\_from\_date bitwise and Deal.creation &lt; from\_date) bitwise and Status.type differs from “Lost”).
- If user.
  - Set prev\_cond from (prev\_cond bitwise and Deal.deal\_owner equals user).
- Set deal\_value\_expr from (Deal.deal\_value × IfNull(Deal.exchange\_rate, 1)).
- Set query from nested operand in the contract(nested operand in the contract).join(Status).on(Deal.status equals Status.name).select(Avg(nested operand in the contract(nested operand in the contract, nested operand in th ….
- Set result from query.run(as\_dict = true).
- Set current\_month\_avg from (result at 0.current\_month\_avg or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_month\_avg → 0.
- Set prev\_month\_avg from (result at 0.prev\_month\_avg or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_month\_avg → 0.
- Set delta from (current\_month\_avg − prev\_month\_avg) when prev\_month\_avg, otherwise 0.
  - Value choice on prev\_month\_avg — true gives (current\_month\_avg − prev\_month\_avg), false gives 0.
- Return mapping(“title” → translated “Avg. deal value”, “tooltip” → translated “Average deal value of ongoing &amp; won deals”, “value” → current\_month\_avg, “prefix” → get\_base\_currency\_symbol(), …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0004.json#L7058) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L30) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L29)

<a id="op-9a2ff86e11b107"></a>
### Get average time to close a lead

`operation_relationships_application_interface_dashboard_business_behavior_get_average_time_to_close_a_lead`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Avg. time to close a lead”, “tooltip” → translated “Average time taken from lead creation to deal closure”, “value” → current\_avg\_lead, “suffix” → “ days”, …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set prev\_to\_date from from\_date.
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set Lead from DocType(“CRM Lead”).
- Set base\_cond from (Deal.closed\_date.isnotnull() bitwise and Status.type equals “Won”).
- If user.
  - Set base\_cond from (base\_cond bitwise and Deal.deal\_owner equals user).
- Set current\_cond from (Deal.closed\_date ≥ from\_date bitwise and Deal.closed\_date &lt; to\_date\_plus\_one).
- Set prev\_cond from (Deal.closed\_date ≥ prev\_from\_date bitwise and Deal.closed\_date &lt; prev\_to\_date).
- Set time\_diff from TimestampDiff(Platform.qb.terms.LiteralValue(“DAY”), Coalesce(Lead.creation, Deal.creation), Deal.closed\_date).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.lead equals nested operand in the contract.name).where(base\_cond).select(Avg(nested operand in the contract( ….
- Set result from query.run(as\_dict = true).
- Set current\_avg\_lead from (result at 0.current\_avg\_lead or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_avg\_lead → 0.
- Set prev\_avg\_lead from (result at 0.prev\_avg\_lead or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_avg\_lead → 0.
- Set delta\_lead from (current\_avg\_lead − prev\_avg\_lead) when prev\_avg\_lead, otherwise 0.
  - Value choice on prev\_avg\_lead — true gives (current\_avg\_lead − prev\_avg\_lead), false gives 0.
- Return mapping(“title” → translated “Avg. time to close a lead”, “tooltip” → translated “Average time taken from lead creation to deal closure”, “value” → current\_avg\_lead, “suffix” → “ days”, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0005.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L33) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L32)

<a id="op-46c3d9f799320e"></a>
### Get average time to close a deal

`operation_relationships_application_interface_dashboard_business_behavior_get_average_time_to_close_a_deal`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“title” → translated “Avg. time to close a deal”, “tooltip” → translated “Average time taken from deal creation to deal closure”, “value” → current\_avg\_deal, “suffix” → “ days”, …).

**Local steps**

- Set diff from Platform.utils.date\_diff(to\_date, from\_date).
- If diff equals 0.
  - Set diff from 1.
- Set prev\_from\_date from Platform.utils.add\_days(from\_date, negative diff).
- Set to\_date\_plus\_one from Platform.utils.add\_days(to\_date, 1).
- Set prev\_to\_date from from\_date.
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set Lead from DocType(“CRM Lead”).
- Set base\_cond from (Deal.closed\_date.isnotnull() bitwise and Status.type equals “Won”).
- If user.
  - Set base\_cond from (base\_cond bitwise and Deal.deal\_owner equals user).
- Set current\_cond from (Deal.closed\_date ≥ from\_date bitwise and Deal.closed\_date &lt; to\_date\_plus\_one).
- Set prev\_cond from (Deal.closed\_date ≥ prev\_from\_date bitwise and Deal.closed\_date &lt; prev\_to\_date).
- Set time\_diff from TimestampDiff(Platform.qb.terms.LiteralValue(“DAY”), Deal.creation, Deal.closed\_date).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.lead equals nested operand in the contract.name).where(base\_cond).select(Avg(nested operand in the contract( ….
- Set result from query.run(as\_dict = true).
- Set current\_avg\_deal from (result at 0.current\_avg\_deal or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.current\_avg\_deal → 0.
- Set prev\_avg\_deal from (result at 0.prev\_avg\_deal or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0.prev\_avg\_deal → 0.
- Set delta\_deal from (current\_avg\_deal − prev\_avg\_deal) when prev\_avg\_deal, otherwise 0.
  - Value choice on prev\_avg\_deal — true gives (current\_avg\_deal − prev\_avg\_deal), false gives 0.
- Return mapping(“title” → translated “Avg. time to close a deal”, “tooltip” → translated “Average time taken from deal creation to deal closure”, “value” → current\_avg\_deal, “suffix” → “ days”, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0005.json#L1223) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L32) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L31)

<a id="op-81d7fd0e2550b7"></a>
### Get sales trend

`operation_relationships_application_interface_dashboard_business_behavior_get_sales_trend`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → sales\_trend, “title” → translated “Sales trend”, “subtitle” → translated “Daily performance of leads, deals, and wins”, “xAxis” → mapping(“title” → translated “Date”, “key” → “date”, “type ….

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set Lead from DocType(“CRM Lead”).
- Set Deal from DocType(“CRM Deal”).
- Set Status from DocType(“CRM Deal Status”).
- Set leads\_query from nested operand in the contract.qb.from\_(Lead).select(Date(nested operand in the contract.creation).as\_(“date”), Count(“\*”).as\_(“leads”), nested operand in the contract.ValueWrapper(0).as\_(“deals”), nested  ….
- If user.
  - Set leads\_query from leads\_query.where(Lead.lead\_owner equals user).
- Set leads\_query from leads\_query.groupby(Date(Lead.creation)).
- Set deals\_query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.status equals nested operand in the contract.name).select(Date(nested operand in the contract.creation).as\_( ….
- If user.
  - Set deals\_query from deals\_query.where(Deal.deal\_owner equals user).
- Set deals\_query from deals\_query.groupby(Date(Deal.creation)).
- Set union\_query from leads\_query.union\_all(deals\_query).
- Set daily from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“date”), nested operand in the contract.as\_(“leads”), nested operand in the contract.as\_(“deals”), n ….
- Set result from daily.run(as\_dict = true).
- Set sales\_trend from list of mapping(“date” → nested operand in the contract.utils.get\_datetime(row.date).strftime(“%Y-%m-%d”), “leads” → (row.leads or 0), “deals” → (row.deals or 0), “won\_deals” → (row.won\_deals or 0)) for ro ….
  - Draw row from result.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.leads → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.deals → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.won\_deals → 0.
- Return mapping(“data” → sales\_trend, “title” → translated “Sales trend”, “subtitle” → translated “Daily performance of leads, deals, and wins”, “xAxis” → mapping(“title” → translated “Date”, “key” → “date”, “type ….

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0005.json#L2418) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L52) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L48)

<a id="op-702b79550b84cc"></a>
### Get forecasted revenue

`operation_relationships_application_interface_dashboard_business_behavior_get_forecasted_revenue`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Forecasted revenue”, “subtitle” → translated “Projected vs actual revenue based on deal probability”, “xAxis” → mapping(“title” → translated “Mont ….

**Local steps**

- Set CRMDeal from DocType(“CRM Deal”).
- Set CRMDealStatus from DocType(“CRM Deal Status”).
- Set twelve\_months\_ago from Platform.utils.add\_months(Platform.utils.nowdate(), negative 12).
- Set forecasted\_value from Case().when(CRMDealStatus.type equals “Lost”, (CRMDeal.expected\_deal\_value × IfNull(CRMDeal.exchange\_rate, 1))).else\_((((CRMDeal.expected\_deal\_value × IfNull(CRMDeal.probability, 0)) ÷ 100) × IfNull(CRMDea ….
- Set actual\_value from Case().when(CRMDealStatus.type equals “Won”, (CRMDeal.deal\_value × IfNull(CRMDeal.exchange\_rate, 1))).else\_(0).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.expected\_closure\_date ≥ twelve\_months\_ago ….
- If user.
  - Set query from query.where(CRMDeal.deal\_owner equals user).
- Set result from query.run(as\_dict = true).
- For each row in result.
  - Set row at “month” from Platform.utils.get\_datetime(row at “month”).strftime(“%Y-%m-01”).
  - Set row at “forecasted” from (row at “forecasted” or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “forecasted” → empty text.
  - Set row at “actual” from (row at “actual” or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row at “actual” → empty text.
- Return mapping(“data” → (result or list()), “title” → translated “Forecasted revenue”, “subtitle” → translated “Projected vs actual revenue based on deal probability”, “xAxis” → mapping(“title” → translated “Mont ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0005.json#L4421) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L47) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L43)

<a id="op-f4d0610d94fd9f"></a>
### Get funnel conversion

`operation_relationships_application_interface_dashboard_business_behavior_get_funnel_conversion`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Funnel conversion”, “subtitle” → translated “Lead to deal conversion pipeline”, “xAxis” → mapping(“title” → translated “Stage”, “key” → “stage”, “ ….

**Local steps**

- Set lead\_conds from empty text.
- Set deal\_conds from empty text.
- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set lead\_filters from mapping(“from” → from\_date, “to” → to\_date).
- Set deal\_filters from mapping(“from” → from\_date, “to” → to\_date).
- If user.
  - Update lead\_conds using + “ AND lead\_owner = %(user)s”.
  - Update deal\_conds using + “ AND deal\_owner = %(user)s”.
  - Set lead\_filters at “user” from user.
  - Set deal\_filters at “user” from user.
- Set result from list().
- Set CRMLead from DocType(“CRM Lead”).
- Set query from nested operand in the contract.qb.from\_(CRMLead).select(Count(“\*”).as\_(“count”)).where(Date(CRMLead.creation).between(from\_date, to\_date)).
- If user.
  - Set query from query.where(CRMLead.lead\_owner equals user).
- Set total\_leads from query.run(as\_dict = true).
- Set total\_leads\_count from total\_leads at 0.count when total\_leads, otherwise 0.
  - Value choice on total\_leads — true gives total\_leads at 0.count, false gives 0.
- Evaluate result.append(mapping(“stage” → “Leads”, “count” → total\_leads\_count)).
- Update result using + get\_deal\_status\_change\_counts(from\_date, to\_date, deal\_conds, deal\_filters).
- Return mapping(“data” → (result or list()), “title” → translated “Funnel conversion”, “subtitle” → translated “Lead to deal conversion pipeline”, “xAxis” → mapping(“title” → translated “Stage”, “key” → “stage”, “ ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0005.json#L5841) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L48) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L44)

<a id="op-056159ac3db06a"></a>
### Get deals by stage axis

`operation_relationships_application_interface_dashboard_business_behavior_get_deals_by_stage_axis`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Deals by ongoing &amp; won stage”, “xAxis” → mapping(“title” → translated “Stage”, “key” → “stage”, “type” → “category”), “yAxis” → mapping(“title” →  ….

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set CRMDeal from DocType(“CRM Deal”).
- Set CRMDealStatus from DocType(“CRM Deal Status”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract(nested operand in the contract, nested o ….
- If user.
  - Set query from query.where(CRMDeal.deal\_owner equals user).
- Set result from query.run(as\_dict = true).
- Return mapping(“data” → (result or list()), “title” → translated “Deals by ongoing &amp; won stage”, “xAxis” → mapping(“title” → translated “Stage”, “key” → “stage”, “type” → “category”), “yAxis” → mapping(“title” →  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L44) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L40)

<a id="op-238339bafe6c37"></a>
### Get deals by stage donut

`operation_relationships_application_interface_dashboard_business_behavior_get_deals_by_stage_donut`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Deals by stage”, “subtitle” → translated “Current pipeline distribution”, “categoryColumn” → “stage”, …).

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set CRMDeal from DocType(“CRM Deal”).
- Set CRMDealStatus from DocType(“CRM Deal Status”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.between(from\_date, to\_date)).groupby(CRMD ….
- If user.
  - Set query from query.where(CRMDeal.deal\_owner equals user).
- Set result from query.run(as\_dict = true).
- Return mapping(“data” → (result or list()), “title” → translated “Deals by stage”, “subtitle” → translated “Current pipeline distribution”, “categoryColumn” → “stage”, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L984) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L45) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L41)

<a id="op-847c26220d0918"></a>
### Get lost deal reasons

`operation_relationships_application_interface_dashboard_business_behavior_get_lost_deal_reasons`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Lost deal reasons”, “subtitle” → translated “Common reasons for losing deals”, “xAxis” → mapping(“title” → translated “Reason”, “key” → “reason”,  ….

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set CRMDeal from DocType(“CRM Deal”).
- Set CRMDealStatus from DocType(“CRM Deal Status”).
- Set query from nested operand in the contract(nested operand in the contract).groupby(CRMDeal.lost\_reason).having((nested operand in the contract.lost\_reason.isnotnull() bitwise and CRMDeal.lost\_reason differs from empty ….
- If user.
  - Set query from query.where(CRMDeal.deal\_owner equals user).
- Set result from query.run(as\_dict = true).
- Return mapping(“data” → (result or list()), “title” → translated “Lost deal reasons”, “subtitle” → translated “Common reasons for losing deals”, “xAxis” → mapping(“title” → translated “Reason”, “key” → “reason”,  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L1807) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L50) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L46)

<a id="op-f2ad40d793cc0f"></a>
### Get leads by source

`operation_relationships_application_interface_dashboard_business_behavior_get_leads_by_source`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Leads by source”, “subtitle” → translated “Lead generation channel analysis”, “categoryColumn” → “source”, …).

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set CRMLead from DocType(“CRM Lead”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.between(from\_date, to\_date)).groupby(CRMLead.source).orderby(Count(“\*”),  ….
- If user.
  - Set query from query.where(CRMLead.lead\_owner equals user).
- Set result from query.run(as\_dict = true).
- Return mapping(“data” → (result or list()), “title” → translated “Leads by source”, “subtitle” → translated “Lead generation channel analysis”, “categoryColumn” → “source”, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L2831) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L49) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L45)

<a id="op-5bbf6ce444ccaa"></a>
### Get deals by source

`operation_relationships_application_interface_dashboard_business_behavior_get_deals_by_source`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Deals by source”, “subtitle” → translated “Deal generation channel analysis”, “categoryColumn” → “source”, …).

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set CRMDeal from DocType(“CRM Deal”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.between(from\_date, to\_date)).groupby(CRMDeal.source).orderby(Count(“\*”),  ….
- If user.
  - Set query from query.where(CRMDeal.deal\_owner equals user).
- Set result from query.run(as\_dict = true).
- Return mapping(“data” → (result or list()), “title” → translated “Deals by source”, “subtitle” → translated “Deal generation channel analysis”, “categoryColumn” → “source”, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L3560) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L43) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L39)

<a id="op-60bc2303b49062"></a>
### Get deals by territory

`operation_relationships_application_interface_dashboard_business_behavior_get_deals_by_territory`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Deals by territory”, “subtitle” → translated “Geographic distribution of deals and revenue”, “xAxis” → mapping(“title” → translated “Territory”, “ ….

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set CRMDeal from DocType(“CRM Deal”).
- Set query from nested operand in the contract(nested operand in the contract).groupby(CRMDeal.territory).orderby(Count(“\*”), order = Platform.qb.desc).orderby(Sum((Coalesce(CRMDeal.deal\_value, 0) × IfNull(CRMDeal.exchang ….
- If user.
  - Set query from query.where(CRMDeal.deal\_owner equals user).
- Set result from query.run(as\_dict = true).
- Return mapping(“data” → (result or list()), “title” → translated “Deals by territory”, “subtitle” → translated “Geographic distribution of deals and revenue”, “xAxis” → mapping(“title” → translated “Territory”, “ ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L4289) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L46) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L42)

<a id="op-41d725030d62cc"></a>
### Get deals by salesperson

`operation_relationships_application_interface_dashboard_business_behavior_get_deals_by_salesperson`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Explicit results** mapping(“data” → (result or list()), “title” → translated “Deals by salesperson”, “subtitle” → translated “Number of deals and total value per salesperson”, “xAxis” → mapping(“title” → translated “Salesper ….

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set CRMDeal from DocType(“CRM Deal”).
- Set User from DocType(“User”).
- Set query from nested operand in the contract(nested operand in the contract).groupby(CRMDeal.deal\_owner).orderby(Count(“\*”), order = Platform.qb.desc).orderby(Sum((Coalesce(CRMDeal.deal\_value, 0) × IfNull(CRMDeal.exchan ….
- If user.
  - Set query from query.where(CRMDeal.deal\_owner equals user).
- Set result from query.run(as\_dict = true).
- Return mapping(“data” → (result or list()), “title” → translated “Deals by salesperson”, “subtitle” → translated “Number of deals and total value per salesperson”, “xAxis” → mapping(“title” → translated “Salesper ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L5474) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L42) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L38)

<a id="op-9d4bb85d4a2d17"></a>
### Get base currency symbol

`operation_relationships_application_interface_dashboard_business_behavior_get_base_currency_symbol`

**Inputs** no declared parameters.

**Record and data access** read “FCRM Settings” via get\_single\_value · read “Currency” via get\_value.

**Explicit results** (Platform.db.get\_value(“Currency”, base\_currency, “symbol”) or empty text).

**Local steps**

- Set base\_currency from (Platform.db.get\_single\_value(“FCRM Settings”, “currency”) or “USD”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“FCRM Settings”, “currency”) → “USD”.
- Return (Platform.db.get\_value(“Currency”, base\_currency, “symbol”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Currency”, base\_currency, “symbol”) → empty text.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0006.json#L6733) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L35) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L34)

<a id="op-a5b1bebd19e733"></a>
### Get deal status change counts

`operation_relationships_application_interface_dashboard_business_behavior_get_deal_status_change_counts`

**Inputs** from\_date = no value, to\_date = no value, deal\_conds = empty text, filters = no value.

**Explicit results** (result or list()).

**Local steps**

- Set CRMStatusChangeLog from DocType(“CRM Status Change Log”).
- Set CRMDeal from DocType(“CRM Deal”).
- Set CurrentStatus from DocType(“CRM Deal Status”).as\_(“s”).
- Set TargetStatus from DocType(“CRM Deal Status”).as\_(“st”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- If (filters and filters.get(“user”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“user”).
  - Set query from query.where(CRMDeal.deal\_owner equals filters at “user”).
- Set result from query.run(as\_dict = true).
- Return (result or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L41) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L37)

## Service · Doc

<a id="op-4de05fa5ec91cd"></a>
### Sort options

`operation_relationships_application_interface_record_business_behavior_sort_options`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** fields.

**Local steps**

- Set fields from Platform.get\_meta(doctype).fields.
- Set fields from list of field for field drawn from fields where field.fieldtype does not belong to no\_value\_fields.
  - Draw field from fields, keep a combination only if (field.fieldtype does not belong to no\_value\_fields).
- Set fields from list of mapping(“label” → translated field.label, “value” → field.fieldname, “fieldname” → field.fieldname) for field drawn from fields where (field.label and field.fieldname).
  - Draw field from fields, keep a combination only if ((field.label and field.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.label → field.fieldname.
- Set standard\_fields from list(mapping(“label” → “Name”, “fieldname” → “name”), mapping(“label” → “Created On”, “fieldname” → “creation”), mapping(“label” → “Last Modified”, “fieldname” → “modified”), mapping(“label” → “Modified By ….
- For each field in standard\_fields.
  - Set field at “label” from translated field at “label”.
  - Set field at “value” from field at “fieldname”.
  - Evaluate fields.append(field).
- Return fields.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L864) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L139) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L120)

<a id="op-bf251d70144c97"></a>
### Get filterable fields

`operation_relationships_application_interface_record_business_behavior_get_filterable_fields`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** fields.

**Local steps**

- Set allowed\_fieldtypes from list(“Check”, “Data”, “Float”, “Int”, …).
- Set c from get\_controller(doctype).
- Set restricted\_fields from list().
- If hasattr(c, “get\_non\_filterable\_fields”).
  - Set restricted\_fields from c.get\_non\_filterable\_fields().
- Set fields from list().
- Set meta from Platform.get\_meta(doctype).as\_dict().
- Set standard\_fields from list(mapping(“fieldname” → “name”, “fieldtype” → “Link”, “label” → “Name”, “options” → doctype), mapping(“fieldname” → “owner”, “fieldtype” → “Link”, “label” → “Created By”, “options” → “User”), mapping(“f ….
- For each field in (standard\_fields + meta.get(“fields”, list())).
  - If (field.get(“fieldname”) does not belong to restricted\_fields and field.get(“fieldtype”) belongs to allowed\_fieldtypes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.get(“fieldname”) does not belong to restricted\_fields → field.get(“fieldtype”) belongs to allowed\_fieldtypes.
    - Set field at “name” from field.get(“fieldname”).
    - Set field at “label” from translated field.get(“label”).
    - Set field at “value” from field.get(“fieldname”).
    - Evaluate fields.append(field).
- Return fields.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L1489) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L129) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L110)

<a id="op-6687c4f6d66eea"></a>
### Get group by fields

`operation_relationships_application_interface_record_business_behavior_get_group_by_fields`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** fields.

**Local steps**

- Set allowed\_fieldtypes from list(“Check”, “Data”, “Float”, “Int”, …).
- Set fields from Platform.get\_meta(doctype).fields.
- Set fields from list of field for field drawn from fields where (field.fieldtype does not belong to no\_value\_fields and field.fieldtype belongs to allowed\_fieldtypes).
  - Draw field from fields, keep a combination only if ((field.fieldtype does not belong to no\_value\_fields and field.fieldtype belongs to allowed\_fieldtypes)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype does not belong to no\_value\_fields → field.fieldtype belongs to allowed\_fieldtypes.
- Set fields from list of mapping(“label” → translated field.label, “fieldname” → field.fieldname) for field drawn from fields where (field.label and field.fieldname).
  - Draw field from fields, keep a combination only if ((field.label and field.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.label → field.fieldname.
- Set standard\_fields from list(mapping(“label” → “Name”, “fieldname” → “name”), mapping(“label” → “Created On”, “fieldname” → “creation”), mapping(“label” → “Last Modified”, “fieldname” → “modified”), mapping(“label” → “Modified By ….
- For each field in standard\_fields.
  - Set field at “label” from translated field at “label”.
  - Evaluate fields.append(field).
- Return fields.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0007.json#L2666) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L130) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L111)
