# Customer support · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Service level agreement

[Record definition](../../../../data/record-types/service_level_agreement.json)

<a id="op-ac9d4609b339f1"></a>
### Stays resolved

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_stays_resolved`

**Inputs** doc.

**Declared result** bool.

**Record and data access** read doc.doctype via get\_value.

**Explicit results** false · (doc.get(“status”) belongs to fulfillment\_statuses and previous\_status belongs to fulfillment\_statuses).

**Local steps**

- If (doc.is\_new() or not doc.get(“service\_level\_agreement”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.is\_new() → not doc.get(“service\_level\_agreement”).
  - Return false.
- If any(generator of doc.has\_value\_changed(field) for field drawn from tuple(“service\_level\_agreement”, “priority”, “service\_level\_agreement\_creation”)).
  - Draw field from tuple(“service\_level\_agreement”, “priority”, “service\_level\_agreement\_creation”).
  - Return false.
- Set fulfillment\_statuses from get\_fulfillment\_statuses(doc.service\_level\_agreement).
- Set previous\_status from Platform.db.get\_value(doc.doctype, doc.name, “status”).
- Return (doc.get(“status”) belongs to fulfillment\_statuses and previous\_status belongs to fulfillment\_statuses).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“status”) belongs to fulfillment\_statuses → previous\_status belongs to fulfillment\_statuses.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1279)

<a id="op-bca78f14ca1180"></a>
### Remove sla if applied

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_remove_service_level_agreement_if_applied`

**Inputs** doc.

**Local steps**

- Set doc.service\_level\_agreement from no value.
- Set doc.response\_by from no value.
- Set doc.sla\_resolution\_by from no value.
- Set doc.agreement\_status from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1224)

<a id="op-384d796214a986"></a>
### Process sla

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_process_service_level_agreement`

**Inputs** doc, sla.

**Local steps**

- If not doc.creation.
  - Set doc.creation from Platform.utils.now\_datetime().
  - If doc.meta.has\_field(“service\_level\_agreement\_creation”).
    - Set doc.service\_level\_agreement\_creation from Platform.utils.now\_datetime().
- Set doc.service\_level\_agreement from sla.name.
- Set doc.priority from (doc.get(“priority”) or sla.default\_priority).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“priority”) → sla.default\_priority.
- Evaluate handle\_status\_change(doc, sla.apply\_sla\_for\_resolution, get\_hold\_statuses(sla.name), get\_fulfillment\_statuses(sla.name)).
- Evaluate update\_response\_and\_resolution\_metrics(doc, sla.apply\_sla\_for\_resolution).
- Evaluate update\_agreement\_status(doc, sla.apply\_sla\_for\_resolution).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1222)

<a id="op-3a287b41d8f99b"></a>
### Handle status change

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_handle_status_change`

**Inputs** doc, apply\_sla\_for\_resolution, hold\_statuses, fulfillment\_statuses.

**Record and data access** read doc.doctype via get\_value.

**Local steps**

- Set now\_time from (Platform.flags.current\_time or Platform.utils.now\_datetime()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.current\_time → Platform.utils.now\_datetime().
- Set prev\_status from Platform.db.get\_value(doc.doctype, doc.name, “status”).
- Bind local operation is\_hold\_status for subsequent calls.
- Bind local operation is\_fulfilled\_status for subsequent calls.
- Bind local operation is\_open\_status for subsequent calls.
- Bind local operation set\_first\_response for subsequent calls.
- Bind local operation calculate\_hold\_hours for subsequent calls.
- If ((is\_open\_status(prev\_status) and not is\_open\_status(doc.status)) or doc.flags.on\_first\_reply).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (is\_open\_status(prev\_status) and not is\_open\_status(doc.status)) → doc.flags.on\_first\_reply.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_open\_status(prev\_status) → not is\_open\_status(doc.status).
  - Evaluate set\_first\_response().
- If (is\_open\_status(prev\_status) and is\_hold\_status(doc.status)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_open\_status(prev\_status) → is\_hold\_status(doc.status).
  - Set doc.on\_hold\_since from now\_time.
- If (is\_hold\_status(prev\_status) and is\_open\_status(doc.status)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_hold\_status(prev\_status) → is\_open\_status(doc.status).
  - Evaluate calculate\_hold\_hours().
  - Evaluate reset\_resolution\_metrics(doc).
- If (is\_open\_status(prev\_status) and is\_fulfilled\_status(doc.status)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_open\_status(prev\_status) → is\_fulfilled\_status(doc.status).
  - Set doc.sla\_resolution\_date from now\_time.
  - Evaluate set\_resolution\_time(doc).
- If (is\_fulfilled\_status(prev\_status) and is\_open\_status(doc.status)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_fulfilled\_status(prev\_status) → is\_open\_status(doc.status).
  - Evaluate calculate\_hold\_hours().
  - Evaluate reset\_resolution\_metrics(doc).
- If (is\_fulfilled\_status(prev\_status) and is\_hold\_status(doc.status)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_fulfilled\_status(prev\_status) → is\_hold\_status(doc.status).
  - Evaluate calculate\_hold\_hours().
  - Evaluate reset\_resolution\_metrics(doc).
  - Set doc.on\_hold\_since from now\_time.
- If (is\_hold\_status(prev\_status) and is\_fulfilled\_status(doc.status)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_hold\_status(prev\_status) → is\_fulfilled\_status(doc.status).
  - Evaluate calculate\_hold\_hours().
  - If apply\_sla\_for\_resolution.
    - Set doc.sla\_resolution\_date from now\_time.
    - Evaluate set\_resolution\_time(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1213)

<a id="op-cf16222bb309a6"></a>
### Handle status change.is hold status

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_handle_status_change_is_hold_status`

**Inputs** status.

**Explicit results** status belongs to hold\_statuses.

**Local steps**

- Return status belongs to hold\_statuses.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L5650) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1738) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1216)

<a id="op-2240b983dfcf29"></a>
### Handle status change.is fulfilled status

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_handle_status_change_is_fulfilled_status`

**Inputs** status.

**Explicit results** status belongs to fulfillment\_statuses.

**Local steps**

- Return status belongs to fulfillment\_statuses.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L5699) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1737) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1215)

<a id="op-3ee9567ab69b93"></a>
### Handle status change.is open status

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_handle_status_change_is_open_status`

**Inputs** status.

**Explicit results** (status does not belong to hold\_statuses and status does not belong to fulfillment\_statuses).

**Local steps**

- Return (status does not belong to hold\_statuses and status does not belong to fulfillment\_statuses).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status does not belong to hold\_statuses → status does not belong to fulfillment\_statuses.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L5748) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1739) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1217)

<a id="op-b6918eb6312a87"></a>
### Handle status change.set first response

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_handle_status_change_set_first_response`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not doc.get(“service\_level\_agreement”).
  - Return no value.
- If (doc.meta.has\_field(“first\_responded\_on”) and not doc.get(“first\_responded\_on”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.has\_field(“first\_responded\_on”) → not doc.get(“first\_responded\_on”).
  - Set doc.first\_responded\_on from now\_time.
  - If doc.meta.has\_field(“first\_response\_time”).
    - Set doc.first\_response\_time from calculate\_first\_response\_time(doc, doc.first\_responded\_on).
  - If get\_datetime(doc.get(“first\_responded\_on”)) &gt; get\_datetime(doc.get(“response\_by”)).
    - Evaluate record\_assigned\_users\_on\_failure(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1218)

<a id="op-0b377b0ada71fa"></a>
### Handle status change.calculate hold hours

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_handle_status_change_calculate_hold_hours`

**Inputs** no declared parameters.

**Local steps**

- Set on\_hold\_since from (doc.sla\_resolution\_date or doc.on\_hold\_since).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.sla\_resolution\_date → doc.on\_hold\_since.
- If on\_hold\_since.
  - Set current\_hold\_hours from time\_diff\_in\_seconds(now\_time, on\_hold\_since).
  - Set doc.total\_hold\_time from ((doc.total\_hold\_time or 0) + current\_hold\_hours).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.total\_hold\_time → 0.
- Set doc.on\_hold\_since from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L6113) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1736) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1214)

<a id="op-fc42cd564fa0f7"></a>
### Get fulfillment statuses

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_fulfillment_statuses`

**Inputs** service\_level\_agreement.

**Record and data access** read “SLA Fulfilled On Status” via get\_all.

**Explicit results** list of entry.status for entry drawn from Platform.db.get\_all(“SLA Fulfilled On Status”, filters = mapping(“parent” → service\_level\_agreement), fields = list(“status”)).

**Local steps**

- Return list of entry.status for entry drawn from Platform.db.get\_all(“SLA Fulfilled On Status”, filters = mapping(“parent” → service\_level\_agreement), fields = list(“status”)).
  - Draw entry from Platform.db.get\_all(“SLA Fulfilled On Status”, filters = mapping(“parent” → service\_level\_agreement), fields = list(“status”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L6263) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1724) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1202)

<a id="op-2856e6d20d6349"></a>
### Get hold statuses

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_hold_statuses`

**Inputs** service\_level\_agreement.

**Record and data access** read “Pause SLA On Status” via get\_all.

**Explicit results** list of entry.status for entry drawn from Platform.db.get\_all(“Pause SLA On Status”, filters = mapping(“parent” → service\_level\_agreement), fields = list(“status”)).

**Local steps**

- Return list of entry.status for entry drawn from Platform.db.get\_all(“Pause SLA On Status”, filters = mapping(“parent” → service\_level\_agreement), fields = list(“status”)).
  - Draw entry from Platform.db.get\_all(“Pause SLA On Status”, filters = mapping(“parent” → service\_level\_agreement), fields = list(“status”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0969.json#L6394) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1203)

<a id="op-f45ffceabf62dc"></a>
### Update response and resolution metrics

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_update_response_and_resolution_metrics`

**Inputs** doc, apply\_sla\_for\_resolution.

**Local steps**

- Set priority from get\_response\_and\_resolution\_duration(doc).
- Set start\_date\_time from get\_datetime((doc.get(“service\_level\_agreement\_creation”) or doc.creation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“service\_level\_agreement\_creation”) → doc.creation.
- Evaluate set\_response\_by(doc, start\_date\_time, priority).
- If apply\_sla\_for\_resolution.
  - Evaluate set\_resolution\_by(doc, start\_date\_time, priority).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L12) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1249)

<a id="op-76ed740a1c188d"></a>
### Get expected time for

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_expected_time_for`

**Inputs** parameter, service\_level, start\_date\_time.

**Explicit results** add\_working\_seconds(start\_date\_time, allotted\_seconds, service\_level).

**Local steps**

- Set allotted\_seconds from get\_allotted\_seconds(parameter, service\_level).
- Return add\_working\_seconds(start\_date\_time, allotted\_seconds, service\_level).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1201)

<a id="op-1cd9b260e5f112"></a>
### Add working seconds

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_add_working_seconds`

**Inputs** start\_date\_time, allotted\_seconds, service\_level.

**Explicit results** start\_date\_time · current\_date\_time.

**Local steps**

- If allotted\_seconds ≤ 0.
  - Return start\_date\_time.
- Set current\_date\_time from start\_date\_time.
- Set expected\_time from current\_date\_time.
- Set start\_time, end\_time from no value.
- Set expected\_time\_is\_set from 0.
- Set support\_days from get\_support\_days(service\_level).
- Set holidays from get\_holidays(service\_level.get(“holiday\_list”)).
- Set weekdays from get\_weekdays().
- While not expected\_time\_is\_set.
  - Set current\_weekday from weekdays at current\_date\_time.weekday().
  - If (not is\_holiday(current\_date\_time, holidays) and current\_weekday belongs to support\_days).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_holiday(current\_date\_time, holidays) → current\_weekday belongs to support\_days.
    - If (getdate(current\_date\_time) equals getdate(start\_date\_time) and get\_time\_in\_timedelta(current\_date\_time.time()) &gt; support\_days at current\_weekday.start\_time).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(current\_date\_time) equals getdate(start\_date\_time) → get\_time\_in\_timedelta(current\_date\_time.time()) &gt; support\_days at current\_weekday.start\_time.
      - Set start\_time from (current\_date\_time − datetime(current\_date\_time.year, current\_date\_time.month, current\_date\_time.day)).
    - Otherwise.
      - Set start\_time from support\_days at current\_weekday.start\_time.
    - Set end\_time from support\_days at current\_weekday.end\_time.
    - Set time\_left\_today from time\_diff\_in\_seconds(end\_time, start\_time).
    - If time\_left\_today ≤ 0.
      - Take no action here.
    - Otherwise.
      - If allotted\_seconds.
        - If time\_left\_today ≥ allotted\_seconds.
          - Set expected\_time from datetime.combine(getdate(current\_date\_time), get\_time(start\_time)).
          - Set expected\_time from add\_to\_date(expected\_time, seconds = allotted\_seconds).
          - Set expected\_time\_is\_set from 1.
        - Otherwise.
          - Set allotted\_seconds from (allotted\_seconds − time\_left\_today).
  - If not expected\_time\_is\_set.
    - Set current\_date\_time from add\_to\_date(current\_date\_time, days = 1).
- If (end\_time and allotted\_seconds ≥ 86400).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_time → allotted\_seconds ≥ 86400.
  - Set current\_date\_time from datetime.combine(getdate(current\_date\_time), get\_time(end\_time)).
- Otherwise.
  - Set current\_date\_time from expected\_time.
- Return current\_date\_time.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1259)

<a id="op-92a501312b3f21"></a>
### Get working seconds between

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_get_working_seconds_between`

**Inputs** start\_date\_time, end\_date\_time, service\_level.

**Declared result** float.

**Explicit results** working\_seconds.

**Local steps**

- Set support\_days from get\_support\_days(service\_level).
- Set holidays from get\_holidays(service\_level.get(“holiday\_list”)).
- Set weekdays from get\_weekdays().
- Set working\_seconds from 0.
- Set day from getdate(start\_date\_time).
- While day ≤ getdate(end\_date\_time).
  - Set working\_hours from support\_days.get(weekdays at day.weekday()).
  - If (working\_hours and not is\_holiday(day, holidays)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in working\_hours → not is\_holiday(day, holidays).
    - Update working\_seconds using + get\_working\_seconds\_on(day, working\_hours, start\_date\_time, end\_date\_time).
  - Set day from add\_days(day, 1).
- Return working\_seconds.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1267)

<a id="op-3d281de95399de"></a>
### Get working seconds on

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_get_working_seconds_on`

**Inputs** day, working\_hours, start\_date\_time, end\_date\_time.

**Declared result** float.

**Explicit results** max(time\_diff\_in\_seconds(closes\_at, opens\_at), 0).

**Local steps**

- Set midnight from datetime.combine(day, datetime.min.time()).
- Set opens\_at from max((midnight + to\_timedelta(working\_hours.start\_time)), start\_date\_time).
- Set closes\_at from min((midnight + to\_timedelta(working\_hours.end\_time)), end\_date\_time).
- Return max(time\_diff\_in\_seconds(closes\_at, opens\_at), 0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1268)

<a id="op-c9069b663cfa51"></a>
### Get allotted seconds

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_allotted_seconds`

**Inputs** parameter, service\_level.

**Explicit results** allotted\_seconds.

**Explicit failure paths** validation helper — translated “{0} parameter is invalid”.format(parameter).

**Local steps**

- Set allotted\_seconds from 0.
- If parameter equals “response”.
  - Set allotted\_seconds from service\_level.get(“response\_time”).
- Otherwise.
  - If parameter equals “resolution”.
    - Set allotted\_seconds from service\_level.get(“resolution\_time”).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “{0} parameter is invalid”.format(parameter)).
- Return allotted\_seconds.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L921) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1196)

<a id="op-e12cb6eceff51c"></a>
### Get support days

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_support_days`

**Inputs** service\_level.

**Explicit results** support\_days.

**Local steps**

- Set support\_days from mapping().
- For each service in service\_level.get(“support\_and\_resolution”).
  - Set support\_days at service.workday from Platform.\_dict(mapping(“start\_time” → service.start\_time, “end\_time” → service.end\_time)).
- Return support\_days.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L1158) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1209)

<a id="op-40020778cfb8d4"></a>
### Set resolution time

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_set_resolution_time`

**Inputs** doc.

**Record and data access** read “Communication” via get\_all.

**Explicit results** no value.

**Local steps**

- Set start\_date\_time from get\_datetime((doc.get(“service\_level\_agreement\_creation”) or doc.creation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“service\_level\_agreement\_creation”) → doc.creation.
- If doc.meta.has\_field(“resolution\_time”).
  - Set doc.resolution\_time from time\_diff\_in\_seconds(doc.sla\_resolution\_date, start\_date\_time).
- If not doc.meta.has\_field(“user\_resolution\_time”).
  - Return no value.
- Set communications from Platform.get\_all(“Communication”, filters = mapping(“reference\_doctype” → doc.doctype, “reference\_name” → doc.name), fields = list(“sent\_or\_received”, “name”, “creation”), order\_by = “creation”).
- Set pending\_time from list().
- For each i in range(len(communications)).
  - If (communications at i.sent\_or\_received equals “Received” and communications at (i − 1).sent\_or\_received equals “Sent”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in communications at i.sent\_or\_received equals “Received” → communications at (i − 1).sent\_or\_received equals “Sent”.
    - Set wait\_time from time\_diff\_in\_seconds(communications at i.creation, communications at (i − 1).creation).
    - If wait\_time &gt; 0.
      - Evaluate pending\_time.append(wait\_time).
- Set total\_pending\_time from sum(pending\_time).
- Set resolution\_time\_in\_secs from time\_diff\_in\_seconds(doc.sla\_resolution\_date, start\_date\_time).
- Set doc.user\_resolution\_time from (resolution\_time\_in\_secs − total\_pending\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L1326) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L8) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1245)

<a id="op-e27f3bb9688fd6"></a>
### Get response and resolution duration

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_response_and_resolution_duration`

**Inputs** doc.

**Record and data access** resolve a document from “Service Level Agreement” via get\_doc.

**Explicit results** priority.

**Local steps**

- Set sla from Platform.get\_doc(“Service Level Agreement”, doc.service\_level\_agreement).
- Set priority from sla.get\_service\_level\_agreement\_priority(doc.priority).
- Evaluate priority.update(mapping(“support\_and\_resolution” → sla.support\_and\_resolution, “holiday\_list” → sla.holiday\_list)).
- Return priority.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L2471) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1205)

<a id="op-fea1e80c31ad10"></a>
### Reset service level agreement

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_reset_service_level_agreement`

**Inputs** doctype, docname, reason, user = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Support Settings” via get\_single\_value · resolve a document from doctype via get\_doc · resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → doc.doctype, “reference\_name” → doc.name, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → doc.doctype, “reference\_name” → doc.name, …)) · call save on doc.

**Explicit failure paths** validation helper — translated “Allow Resetting Service Level Agreement from Support Settings.”.

**Local steps**

- If not Platform.db.get\_single\_value(“Support Settings”, “allow\_resetting\_service\_level\_agreement”).
  - Call the validation error handler Platform.throw(translated “Allow Resetting Service Level Agreement from Support Settings.”).
- Set doc from Platform.get\_doc(doctype, docname).
- Evaluate doc.check\_permission(“write”).
- Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → doc.doctype, “reference\_name” → doc.name, …)).insert(ignore\_permissions = true).
- Set doc.service\_level\_agreement\_creation from Platform.utils.now\_datetime().
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Support Settings”, “allow\_resetting\_service\_level\_agreement”) · effective access from doc.check\_permission(“write”) · clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1226)

<a id="op-ee471a51efc28c"></a>
### Reset resolution metrics

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_reset_resolution_metrics`

**Inputs** doc.

**Local steps**

- If doc.meta.has\_field(“sla\_resolution\_date”).
  - Set doc.sla\_resolution\_date from no value.
- If doc.meta.has\_field(“resolution\_time”).
  - Set doc.resolution\_time from no value.
- If doc.meta.has\_field(“user\_resolution\_time”).
  - Set doc.user\_resolution\_time from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L3129) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1225)

<a id="op-0dc601264d6a65"></a>
### On communication update

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_on_communication_update`

**Inputs** doc, status.

**Record and data access** read “Service Level Agreement” via get\_value.

**State and service calls** request set\_value on parent.doctype · call save on parent.

**Explicit results** no value.

**Local steps**

- If doc.communication\_type equals “Comment”.
  - Return no value.
- Set parent from get\_parent\_doc(doc).
- If not parent.
  - Return no value.
- If not parent.meta.has\_field(“service\_level\_agreement”).
  - Return no value.
- If not parent.get(“service\_level\_agreement”).
  - Return no value.
- If (doc.sent\_or\_received equals “Received” and parent.get(“status”) equals “Open” and parent.get\_doc\_before\_save() and parent.get(“status”) differs from parent.\_doc\_before\_save.get(“status”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sent\_or\_received equals “Received” → parent.get(“status”) equals “Open” → parent.get\_doc\_before\_save() → parent.get(“status”) differs from parent.\_doc\_before\_save.get(“status”).
  - Evaluate Platform.db.set\_value(parent.doctype, parent.name, “status”, parent.\_doc\_before\_save.get(“status”), update\_modified = false).
- Otherwise.
  - If (doc.sent\_or\_received equals “Sent” and parent.get(“first\_responded\_on”) and parent.get\_doc\_before\_save() and not parent.\_doc\_before\_save.get(“first\_responded\_on”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sent\_or\_received equals “Sent” → parent.get(“first\_responded\_on”) → parent.get\_doc\_before\_save() → not parent.\_doc\_before\_save.get(“first\_responded\_on”).
    - Set parent.first\_responded\_on from no value.
    - Set parent.flags.on\_first\_reply from true.
  - Otherwise.
    - Return no value.
- Set for\_resolution from Platform.db.get\_value(“Service Level Agreement”, parent.service\_level\_agreement, “apply\_sla\_for\_resolution”).
- Evaluate handle\_status\_change(parent, for\_resolution, get\_hold\_statuses(parent.service\_level\_agreement), get\_fulfillment\_statuses(parent.service\_level\_agreement)).
- Evaluate update\_response\_and\_resolution\_metrics(parent, for\_resolution).
- Evaluate update\_agreement\_status(parent, for\_resolution).
- Evaluate parent.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1221)

<a id="op-4849154c6e2da5"></a>
### Set response by

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_set_response_by`

**Inputs** doc, start\_date\_time, priority.

**Local steps**

- If doc.meta.has\_field(“response\_by”).
  - Set deadline from SLADeadline(doc, “response”, “response\_by”, priority, …).
  - Set doc.response\_by from deadline.get(moves\_on\_resume = not doc.get(“first\_responded\_on”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L9) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1246)
