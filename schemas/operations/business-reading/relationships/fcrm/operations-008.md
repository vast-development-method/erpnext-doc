# Lead and deal records · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm service level agreement

<a id="op-587315821d584d"></a>
### CRMService Level Agreement.handle sla status

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_handle_service_level_agreement_status`

**Inputs** self, doc.

**Local steps**

- Set is\_failed from self.is\_first\_response\_failed(doc).
- Set options from mapping(“Fulfilled” → true, “First Response Due” → not doc.first\_responded\_on, “Failed” → is\_failed).
- For each status in options.
  - If options at status.
    - Set doc.sla\_status from status.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is first response failed](operations-008.md#op-de1763303782b1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L2645) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1064) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1040)

<a id="op-de1763303782b1"></a>
### CRMService Level Agreement.is first response failed

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_is_first_response_failed`

**Inputs** self, doc.

**Explicit results** get\_datetime(doc.response\_by) &lt; now\_datetime() · get\_datetime(doc.response\_by) &lt; get\_datetime(doc.first\_responded\_on).

**Local steps**

- If not doc.first\_responded\_on.
  - Return get\_datetime(doc.response\_by) &lt; now\_datetime().
- Return get\_datetime(doc.response\_by) &lt; get\_datetime(doc.first\_responded\_on).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L2823) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1066) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1042)

<a id="op-9b84080525ea25"></a>
### CRMService Level Agreement.handle rolling sla status

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_handle_rolling_service_level_agreement_status`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- If (not self.rolling\_responses or len(doc.rolling\_responses) equals 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.rolling\_responses → len(doc.rolling\_responses) equals 0.
  - Return no value.
- Set is\_failed from self.is\_rolling\_response\_failed(doc).
- Set options from mapping(“Fulfilled” → true, “Rolling Response Due” → doc.communication\_status equals self.get\_default\_priority(), “Failed” → is\_failed).
- For each status in options.
  - If options at status.
    - Set doc.sla\_status from status.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is rolling response failed](operations-008.md#op-80d01f1c1d88b2), [get default priority](operations-008.md#op-d7f4cb0252e4fa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L2983) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1063) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1039)

<a id="op-80d01f1c1d88b2"></a>
### CRMService Level Agreement.is rolling response failed

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_is_rolling_response_failed`

**Inputs** self, doc.

**Explicit results** false · get\_datetime(doc.response\_by) &lt; now\_datetime() · get\_datetime(doc.response\_by) &lt; get\_datetime(doc.last\_responded\_on).

**Local steps**

- If not doc.response\_by.
  - Return false.
- If doc.communication\_status equals self.get\_default\_priority().
  - Return get\_datetime(doc.response\_by) &lt; now\_datetime().
- If not doc.last\_responded\_on.
  - Return get\_datetime(doc.response\_by) &lt; now\_datetime().
- Return get\_datetime(doc.response\_by) &lt; get\_datetime(doc.last\_responded\_on).

**Methods declared on this owner** [get default priority](operations-008.md#op-d7f4cb0252e4fa).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L3245) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1067) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1043)

<a id="op-1e793d611c0668"></a>
### CRMService Level Agreement.time to seconds

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_time_to_seconds`

**Inputs** self, time\_obj.

**Explicit results** time\_obj.total\_seconds() · (((time\_obj.hour × 3600) + (time\_obj.minute × 60)) + time\_obj.second).

**Local steps**

- If isinstance(time\_obj, timedelta).
  - Return time\_obj.total\_seconds().
- Otherwise.
  - Return (((time\_obj.hour × 3600) + (time\_obj.minute × 60)) + time\_obj.second).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L3513) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1074) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1050)

<a id="op-893dd691820670"></a>
### CRMService Level Agreement.calc time

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_calculate_time`

**Inputs** self, start\_at, duration\_seconds.

**Explicit results** res.

**Local steps**

- Set res from get\_datetime(start\_at).
- Set time\_needed from duration\_seconds.
- Set holidays from self.get\_holidays().
- Set weekdays from get\_weekdays().
- Set workdays from self.get\_workdays().
- While time\_needed.
  - Set today from res.
  - Set today\_day from getdate(today).
  - Set today\_weekday from weekdays at today.weekday().
  - Set is\_workday from today\_weekday belongs to workdays.
  - Set is\_holiday from today\_day belongs to holidays.
  - If (is\_holiday or not is\_workday).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_holiday → not is\_workday.
    - Set res from add\_to\_date(res, days = 1, as\_datetime = true).
    - Continue with the next iteration or loop test.
  - Set today\_workday from workdays at today\_weekday.
  - Set now\_in\_seconds from time\_diff\_in\_seconds(today, today\_day).
  - Set start\_time\_seconds from self.\_time\_to\_seconds(today\_workday.start\_time).
  - Set end\_time\_seconds from self.\_time\_to\_seconds(today\_workday.end\_time).
  - Set start\_time from max(start\_time\_seconds, now\_in\_seconds).
  - Set till\_start\_time from max((start\_time − now\_in\_seconds), 0).
  - Set end\_time from max(end\_time\_seconds, now\_in\_seconds).
  - Set time\_left from max((end\_time − start\_time), 0).
  - If not time\_left.
    - Set res from getdate(add\_to\_date(res, days = 1, as\_datetime = true)).
    - Continue with the next iteration or loop test.
  - Set time\_taken from min(time\_needed, time\_left).
  - Update time\_needed using − time\_taken.
  - Set time\_required from (till\_start\_time + time\_taken).
  - Set res from add\_to\_date(res, seconds = time\_required, as\_datetime = true).
- Return res.

**Methods declared on this owner** [get holidays](operations-008.md#op-5577c84ce42390), [get workdays](operations-008.md#op-9b5934b7571f8f), [time to seconds](operations-008.md#op-1e793d611c0668).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L3647) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1054) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1030)

<a id="op-043fcaf624f32f"></a>
### CRMService Level Agreement.calc elapsed time

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_calculate_elapsed_time`

**Inputs** self, start\_time, end\_time.

**Declared result** float.

**Explicit results** total\_seconds.

**Local steps**

- Set start\_time from get\_datetime(start\_time).
- Set end\_time from get\_datetime(end\_time).
- Set holiday\_list from self.get\_holidays().
- Set working\_day\_list from self.get\_working\_days().
- Set working\_hours from self.get\_working\_hours().
- Set total\_seconds from 0.
- Set current\_time from start\_time.
- While current\_time &lt; end\_time.
  - Set in\_holiday\_list from current\_time.date() belongs to holiday\_list.
  - Set not\_in\_working\_day\_list from get\_weekdays() at current\_time.weekday() does not belong to working\_day\_list.
  - If (in\_holiday\_list or not\_in\_working\_day\_list or not self.is\_working\_time(current\_time, working\_hours)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in in\_holiday\_list → not\_in\_working\_day\_list → not self.is\_working\_time(current\_time, working\_hours).
    - Update current\_time using + timedelta(seconds = 1).
    - Continue with the next iteration or loop test.
  - Update total\_seconds using + 1.
  - Update current\_time using + timedelta(seconds = 1).
- Return total\_seconds.

**Methods declared on this owner** [get holidays](operations-008.md#op-5577c84ce42390), [get working days](operations-008.md#op-561bca9c74394c), [get working hours](operations-008.md#op-29dede8897cae8), [is working time](operations-008.md#op-2d068d62978e72).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L4453) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1053) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1029)

<a id="op-d0d742c7d28203"></a>
### CRMService Level Agreement.get priorities

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_get_priorities`

**Inputs** self.

**Explicit results** res.

**Local steps**

- Set res from mapping().
- For each row in self.priorities.
  - Set res at row.priority from row.
- Return res.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L4897) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1057) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1033)

<a id="op-d7f4cb0252e4fa"></a>
### CRMService Level Agreement.get default priority

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_get_default_priority`

**Inputs** self.

**Explicit results** row.priority · self.priorities at 0.priority.

**Local steps**

- For each row in self.priorities.
  - If row.default\_priority.
    - Return row.priority.
- Return self.priorities at 0.priority.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L4990) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1055) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1031)

<a id="op-9b5934b7571f8f"></a>
### CRMService Level Agreement.get workdays

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_get_workdays`

**Inputs** self.

**Declared result** dict at tuple(str, dict).

**Explicit results** res.

**Local steps**

- Set res from mapping().
- For each row in self.working\_hours.
  - Set res at row.workday from row.
- Return res.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L5086) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1058) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1034)

<a id="op-561bca9c74394c"></a>
### CRMService Level Agreement.get working days

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_get_working_days`

**Inputs** self.

**Declared result** dict at tuple(str, dict).

**Explicit results** workdays.

**Local steps**

- Set workdays from list().
- For each row in self.working\_hours.
  - Evaluate workdays.append(row.workday).
- Return workdays.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L5196) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1059) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1035)

<a id="op-29dede8897cae8"></a>
### CRMService Level Agreement.get working hours

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_get_working_hours`

**Inputs** self.

**Declared result** dict at tuple(str, dict).

**Explicit results** res.

**Local steps**

- Set res from mapping().
- For each row in self.working\_hours.
  - Set res at row.workday from tuple(row.start\_time, row.end\_time).
- Return res.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L5310) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1060) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1036)

<a id="op-2d068d62978e72"></a>
### CRMService Level Agreement.is working time

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_is_working_time`

**Inputs** self, date\_time, working\_hours.

**Explicit results** false · start\_time\_seconds ≤ date\_time\_seconds &lt; end\_time\_seconds.

**Local steps**

- Set day\_of\_week from get\_weekdays() at date\_time.weekday().
- Set tuple(start\_time, end\_time) from working\_hours.get(day\_of\_week, tuple(0, 0)).
- If (start\_time equals 0 and end\_time equals 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_time equals 0 → end\_time equals 0.
  - Return false.
- Set date\_time\_seconds from timedelta(hours = date\_time.hour, minutes = date\_time.minute, seconds = date\_time.second).total\_seconds().
- Set start\_time\_seconds from self.\_time\_to\_seconds(start\_time).
- Set end\_time\_seconds from self.\_time\_to\_seconds(end\_time).
- Return start\_time\_seconds ≤ date\_time\_seconds &lt; end\_time\_seconds.
  - Compare adjacent operands in order, stopping at the first false comparison in start\_time\_seconds ≤ date\_time\_seconds &lt; end\_time\_seconds.

**Methods declared on this owner** [time to seconds](operations-008.md#op-1e793d611c0668).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L5437) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1068) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1044)

<a id="op-5577c84ce42390"></a>
### CRMService Level Agreement.get holidays

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_business_behavior_customer_relationship_service_level_agreement_get_holidays`

**Inputs** self.

**Record and data access** resolve a document from “CRM Holiday List” via get\_doc.

**Explicit results** res.

**Local steps**

- Set res from list().
- If not self.holiday\_list.
  - Return res.
- Set holiday\_list from Platform.get\_doc(“CRM Holiday List”, self.holiday\_list).
- For each row in holiday\_list.holidays.
  - Evaluate res.append(row.date).
- Return res.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0041.json#L5783) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1056) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1032)

<a id="op-218687da727cfd"></a>
### Get sla

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_utils_business_behavior_get_service_level_agreement`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doc.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0043.json#L5891) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1128) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1104)

<a id="op-3b801170d948d7"></a>
### Get context

`operation_relationships_fcrm_record_definitions_customer_relationship_management_service_level_agreement_utils_business_behavior_get_context`

**Inputs** d.

**Declared result** dict.

**Explicit results** mapping(“doc” → d.as\_dict(), “Platform” → Platform.\_dict(utils = utils)).

**Local steps**

- Set utils from get\_safe\_globals().get(“Platform”).get(“utils”).
- Return mapping(“doc” → d.as\_dict(), “Platform” → Platform.\_dict(utils = utils)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0043.json#L6752) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1127) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1103)

## Record · Crm status change log

<a id="op-a5ab91467e74f2"></a>
### Get duration

`operation_relationships_fcrm_record_definitions_customer_relationship_management_status_change_log_business_behavior_get_duration`

**Inputs** from\_date, to\_date.

**Explicit results** duration.total\_seconds().

**Local steps**

- If not isinstance(from\_date, datetime).
  - Set from\_date from get\_datetime(from\_date).
- If not isinstance(to\_date, datetime).
  - Set to\_date from get\_datetime(to\_date).
- Set duration from (to\_date − from\_date).
- Return duration.total\_seconds().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0043.json#L6903) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1130) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1106)

<a id="op-310f530b899e97"></a>
### Add status change log

`operation_relationships_fcrm_record_definitions_customer_relationship_management_status_change_log_business_behavior_add_status_change_log`

**Inputs** doc.

**Record and data access** read “CRM Deal Status” via get\_value.

**Local steps**

- Set to\_status\_type from Platform.db.get\_value(“CRM Deal Status”, doc.status, “type”) when doc.status, otherwise no value.
  - Value choice on doc.status — true gives Platform.db.get\_value(“CRM Deal Status”, doc.status, “type”), false gives no value.
- If not doc.is\_new().
  - Set previous\_status from doc.get\_doc\_before\_save().status when doc.get\_doc\_before\_save(), otherwise no value.
    - Value choice on doc.get\_doc\_before\_save() — true gives doc.get\_doc\_before\_save().status, false gives no value.
  - Set previous\_status\_type from Platform.db.get\_value(“CRM Deal Status”, previous\_status, “type”) when previous\_status, otherwise no value.
    - Value choice on previous\_status — true gives Platform.db.get\_value(“CRM Deal Status”, previous\_status, “type”), false gives no value.
  - If (not doc.status\_change\_log and previous\_status).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.status\_change\_log → previous\_status.
    - Set now\_minus\_one\_minute from add\_to\_date(datetime.now(), minutes = negative 1).
    - Evaluate doc.append(“status\_change\_log”, mapping(“from” → previous\_status, “from\_type” → (previous\_status\_type or empty text), “to” → empty text, “to\_type” → empty text, …)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_status\_type → empty text.
  - Set last\_status\_change from doc.status\_change\_log at negative 1.
  - Set last\_status\_change.to from doc.status.
  - Set last\_status\_change.to\_type from (to\_status\_type or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_status\_type → empty text.
  - Set last\_status\_change.to\_date from datetime.now().
  - Set last\_status\_change.log\_owner from Platform.session.user.
  - Set last\_status\_change.duration from get\_duration(last\_status\_change.from\_date, last\_status\_change.to\_date).
- Evaluate doc.append(“status\_change\_log”, mapping(“from” → doc.status, “from\_type” → (to\_status\_type or empty text), “to” → empty text, “to\_type” → empty text, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_status\_type → empty text.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1129) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1105)

## Record · Crm task

<a id="op-0d1451d2ce550b"></a>
### CRMTask.after insert

`operation_relationships_fcrm_record_definitions_customer_relationship_management_task_business_behavior_customer_relationship_task_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.assign\_to().

If control reaches the end, it returns no value.

**Methods declared on this owner** [assign to](operations-008.md#op-bb475d1725ebed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L828) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1131) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1107)

<a id="op-4282f171b52d8c"></a>
### CRMTask.validate

`operation_relationships_fcrm_record_definitions_customer_relationship_management_task_business_behavior_customer_relationship_task_validate`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_new() or not self.assigned\_to).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.assigned\_to.
  - Return no value.
- If self.get\_doc\_before\_save().assigned\_to differs from self.assigned\_to.
  - Evaluate self.unassign\_from\_previous\_user(self.get\_doc\_before\_save().assigned\_to).
  - Evaluate self.assign\_to().

If control reaches the end, it returns no value.

**Methods declared on this owner** [unassign from previous user](operations-008.md#op-4f5018bca26000), [assign to](operations-008.md#op-bb475d1725ebed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L879) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1136) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1112)

<a id="op-4f5018bca26000"></a>
### CRMTask.unassign from previous user

`operation_relationships_fcrm_record_definitions_customer_relationship_management_task_business_behavior_customer_relationship_task_unassign_from_previous_user`

**Inputs** self, user.

**Local steps**

- If user.
  - Evaluate unassign(self.doctype, self.name, user).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L1056) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1135) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1111)

<a id="op-bb475d1725ebed"></a>
### CRMTask.assign to

`operation_relationships_fcrm_record_definitions_customer_relationship_management_task_business_behavior_customer_relationship_task_assign_to`

**Inputs** self.

**Local steps**

- If self.assigned\_to.
  - Evaluate assign(mapping(“assign\_to” → list(self.assigned\_to), “doctype” → self.doctype, “name” → self.name, “description” → (self.title or self.description))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.title → self.description.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L1156) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1132) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1108)

<a id="op-8753dbd0a437d2"></a>
### CRMTask.default list data

`operation_relationships_fcrm_record_definitions_customer_relationship_management_task_business_behavior_customer_relationship_task_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “Title”, “type” → “Data”, “key” → “title”, “width” → “16rem”), mapping(“label” → “Status”, “type” → “Select”, “key” → “status”, “width” → “8rem”), mapping(“label” → “Priority”, “type ….
- Set rows from list(“name”, “title”, “description”, “assigned\_to”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L1324) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1134) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1110)

<a id="op-8cbd90cd23e2d0"></a>
### CRMTask.default kanban settings

`operation_relationships_fcrm_record_definitions_customer_relationship_management_task_business_behavior_customer_relationship_task_default_kanban_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“column\_field” → “status”, “title\_field” → “title”, “kanban\_fields” → “&#91;"description", "priority", "creation"&#93;”).

**Local steps**

- Return mapping(“column\_field” → “status”, “title\_field” → “title”, “kanban\_fields” → “&#91;"description", "priority", "creation"&#93;”).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0044.json#L1953) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1133) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1109)
