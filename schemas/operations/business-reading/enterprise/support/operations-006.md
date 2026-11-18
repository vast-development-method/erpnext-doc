# Customer support · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Service level agreement

[Record definition](../../../../data/record-types/service_level_agreement.json)

<a id="op-5e388bfd253e17"></a>
### Set resolution by

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_set_resolution_by`

**Inputs** doc, start\_date\_time, priority.

**Local steps**

- If doc.meta.has\_field(“sla\_resolution\_by”).
  - Set deadline from SLADeadline(doc, “resolution”, “sla\_resolution\_by”, priority, …).
  - Set doc.sla\_resolution\_by from deadline.get().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L7) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1244)

<a id="op-04914863f8cc52"></a>
### SLADeadline.initialize

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_sladeadline_init`

**Inputs** self, doc, parameter, fieldname, priority, start\_date\_time.

**Local steps**

- Set self.doc from doc.
- Set self.previous\_doc from doc.get\_doc\_before\_save().
- Set self.parameter from parameter.
- Set self.fieldname from fieldname.
- Set self.priority from priority.
- Set self.start\_date\_time from start\_date\_time.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1781) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1278)

<a id="op-78d0a645784786"></a>
### SLADeadline.get

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_sladeadline_get`

**Inputs** self, moves\_on\_resume = true.

**Declared result** datetime.

**Explicit results** add\_working\_seconds(deadline, hold\_seconds, self.priority).

**Local steps**

- Set hold\_seconds from self.get\_previous\_hold\_seconds().
- If moves\_on\_resume.
  - Update hold\_seconds using + self.get\_resumed\_hold\_seconds().
- Set deadline from get\_expected\_time\_for(self.parameter, self.priority, self.start\_date\_time).
- Return add\_working\_seconds(deadline, hold\_seconds, self.priority).

**Methods declared on this owner** [get previous hold seconds](operations-006.md#op-8a3a23fc577de1), [get resumed hold seconds](operations-006.md#op-0a9b5596441c4d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1272)

<a id="op-8a3a23fc577de1"></a>
### SLADeadline.get previous hold seconds

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_sladeadline_get_previous_hold_seconds`

**Inputs** self.

**Declared result** float.

**Explicit results** 0 · get\_working\_seconds\_between(deadline\_without\_hold, previous\_deadline, previous\_calendar).

**Local steps**

- Set previous\_deadline from self.get\_previous\_deadline().
- If (not previous\_deadline or not self.previous\_doc.get(“total\_hold\_time”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous\_deadline → not self.previous\_doc.get(“total\_hold\_time”).
  - Return 0.
- Set previous\_calendar from self.get\_previous\_calendar().
- Set deadline\_without\_hold from self.get\_previous\_deadline\_without\_hold(previous\_calendar).
- If not deadline\_without\_hold.
  - Return 0.
- Return get\_working\_seconds\_between(deadline\_without\_hold, previous\_deadline, previous\_calendar).

**Methods declared on this owner** [get previous deadline](operations-006.md#op-fd793443d78329), [get previous calendar](operations-006.md#op-5e93b016b51ac3), [get previous deadline without hold](operations-006.md#op-1ef03a75a512a5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1276)

<a id="op-0a9b5596441c4d"></a>
### SLADeadline.get resumed hold seconds

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_sladeadline_get_resumed_hold_seconds`

**Inputs** self.

**Declared result** float.

**Explicit results** 0 · get\_working\_seconds\_between(on\_hold\_since, get\_current\_time(), self.priority).

**Local steps**

- Set on\_hold\_since from get\_hold\_start(self.previous\_doc).
- Set hold\_start from get\_hold\_start(self.doc).
- If (not on\_hold\_since or (hold\_start and hold\_start ≤ on\_hold\_since)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not on\_hold\_since → (hold\_start and hold\_start ≤ on\_hold\_since).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hold\_start → hold\_start ≤ on\_hold\_since.
  - Return 0.
- Set previous\_deadline from self.get\_previous\_deadline().
- If (previous\_deadline and on\_hold\_since ≥ previous\_deadline).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_deadline → on\_hold\_since ≥ previous\_deadline.
  - Return 0.
- Return get\_working\_seconds\_between(on\_hold\_since, get\_current\_time(), self.priority).

**Methods declared on this owner** [get previous deadline](operations-006.md#op-fd793443d78329).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1780) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1277)

<a id="op-fd793443d78329"></a>
### SLADeadline.get previous deadline

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_sladeadline_get_previous_deadline`

**Inputs** self.

**Declared result** (datetime bitwise or no value).

**Explicit results** get\_datetime(deadline) when deadline, otherwise no value.

**Local steps**

- Set deadline from (self.previous\_doc and self.previous\_doc.get(self.fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.previous\_doc → self.previous\_doc.get(self.fieldname).
- Return get\_datetime(deadline) when deadline, otherwise no value.
  - Value choice on deadline — true gives get\_datetime(deadline), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1274)

<a id="op-5e93b016b51ac3"></a>
### SLADeadline.get previous calendar

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_sladeadline_get_previous_calendar`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Service Level Agreement” via exists · resolve a document from “Service Level Agreement” via get\_doc.

**Explicit results** self.priority · Platform.\_dict(support\_and\_resolution = sla.support\_and\_resolution, holiday\_list = sla.holiday\_list).

**Local steps**

- Set previous\_sla from self.previous\_doc.get(“service\_level\_agreement”).
- If (not previous\_sla or previous\_sla equals self.doc.get(“service\_level\_agreement”) or not Platform.db.exists(“Service Level Agreement”, previous\_sla)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous\_sla → previous\_sla equals self.doc.get(“service\_level\_agreement”) → not Platform.db.exists(“Service Level Agreement”, previous\_sla).
  - Return self.priority.
- Set sla from Platform.get\_doc(“Service Level Agreement”, previous\_sla).
- Return Platform.\_dict(support\_and\_resolution = sla.support\_and\_resolution, holiday\_list = sla.holiday\_list).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1776) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1273)

<a id="op-1ef03a75a512a5"></a>
### SLADeadline.get previous deadline without hold

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_sladeadline_get_previous_deadline_without_hold`

**Inputs** self, previous\_calendar.

**Declared result** (datetime bitwise or no value).

**Record and data access** read “Service Level Priority” via get\_value.

**Explicit results** no value · add\_working\_seconds(start\_date\_time, allotted\_seconds, previous\_calendar).

**Local steps**

- Set previous\_doc from self.previous\_doc.
- Set allotted\_seconds from Platform.db.get\_value(“Service Level Priority”, mapping(“parent” → previous\_doc.get(“service\_level\_agreement”), “priority” → previous\_doc.get(“priority”)), formatted text {self.parameter}\_time).
- If not allotted\_seconds.
  - Return no value.
- Set start\_date\_time from get\_datetime((previous\_doc.get(“service\_level\_agreement\_creation”) or previous\_doc.creation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_doc.get(“service\_level\_agreement\_creation”) → previous\_doc.creation.
- Return add\_working\_seconds(start\_date\_time, allotted\_seconds, previous\_calendar).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1778) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1275)

<a id="op-43d80d196cba73"></a>
### Get hold start

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_get_hold_start`

**Inputs** doc.

**Declared result** (datetime bitwise or no value).

**Explicit results** get\_datetime(hold\_start) when hold\_start, otherwise no value.

**Local steps**

- Set hold\_start from (doc and (doc.get(“sla\_resolution\_date”) or doc.get(“on\_hold\_since”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → (doc.get(“sla\_resolution\_date”) or doc.get(“on\_hold\_since”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“sla\_resolution\_date”) → doc.get(“on\_hold\_since”).
- Return get\_datetime(hold\_start) when hold\_start, otherwise no value.
  - Value choice on hold\_start — true gives get\_datetime(hold\_start), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1766) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1263)

<a id="op-d61deba3da4431"></a>
### Get current time

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_get_current_time`

**Inputs** no declared parameters.

**Declared result** datetime.

**Explicit results** (Platform.flags.current\_time or Platform.utils.now\_datetime()).

**Local steps**

- Return (Platform.flags.current\_time or Platform.utils.now\_datetime()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.current\_time → Platform.utils.now\_datetime().

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1262)

<a id="op-c51c220010121c"></a>
### Record assigned users on failure

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_record_assigned_users_on_failure`

**Inputs** doc.

**Local steps**

- Set assigned\_users from doc.get\_assigned\_users().
- If assigned\_users.
  - Bind dependencies get\_fullname.
  - Set assigned\_users from “, ”.join(generator of get\_fullname(user) for user drawn from assigned\_users).
    - Draw user from assigned\_users.
  - Set message from translated “First Response SLA Failed by {}”.format(assigned\_users).
  - Evaluate doc.add\_comment(comment\_type = “Assigned”, text = message).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L4852) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1223)

<a id="op-f41f143dade942"></a>
### Get service level agreement fields

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_service_level_agreement_fields`

**Inputs** doctype.

**Explicit results** list(mapping(“collapsible” → 1, “fieldname” → “service\_level\_section”, “fieldtype” → “Section Break”, “label” → “Service Level”), mapping(“fieldname” → “service\_level\_agreement”, “fieldtype” → “Link”, “lab ….

**Local steps**

- Return list(mapping(“collapsible” → 1, “fieldname” → “service\_level\_section”, “fieldtype” → “Section Break”, “label” → “Service Level”), mapping(“fieldname” → “service\_level\_agreement”, “fieldtype” → “Link”, “lab ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L5067) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1206)

<a id="op-2457f78fdd3262"></a>
### Update agreement status on custom status

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_update_agreement_status_on_custom_status`

**Inputs** doc.

**Record and data access** read “Service Level Agreement” via get\_value.

**Local steps**

- Set apply\_sla\_for\_resolution from Platform.db.get\_value(“Service Level Agreement”, doc.service\_level\_agreement, “apply\_sla\_for\_resolution”).
- Evaluate update\_agreement\_status(doc, apply\_sla\_for\_resolution).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L11) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1248)

<a id="op-4dbd02e571cc34"></a>
### Update agreement status

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_update_agreement_status`

**Inputs** doc, apply\_sla\_for\_resolution.

**Explicit results** no value.

**Local steps**

- If not doc.meta.has\_field(“agreement\_status”).
  - Return no value.
- If (has\_missed\_deadline(doc, “first\_responded\_on”, “response\_by”) or (apply\_sla\_for\_resolution and has\_missed\_deadline(doc, “sla\_resolution\_date”, “sla\_resolution\_by”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_missed\_deadline(doc, “first\_responded\_on”, “response\_by”) → (apply\_sla\_for\_resolution and has\_missed\_deadline(doc, “sla\_resolution\_date”, “sla\_resolution\_by”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in apply\_sla\_for\_resolution → has\_missed\_deadline(doc, “sla\_resolution\_date”, “sla\_resolution\_by”).
  - Set doc.agreement\_status from “Failed”.
- Otherwise.
  - If (doc.meta.has\_field(“first\_responded\_on”) and not doc.get(“first\_responded\_on”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.has\_field(“first\_responded\_on”) → not doc.get(“first\_responded\_on”).
    - Set doc.agreement\_status from “First Response Due”.
  - Otherwise.
    - If (apply\_sla\_for\_resolution and doc.meta.has\_field(“sla\_resolution\_date”) and not doc.get(“sla\_resolution\_date”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in apply\_sla\_for\_resolution → doc.meta.has\_field(“sla\_resolution\_date”) → not doc.get(“sla\_resolution\_date”).
      - Set doc.agreement\_status from “Resolution Due”.
    - Otherwise.
      - Set doc.agreement\_status from “Fulfilled”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L10) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1247)

<a id="op-0ecdf1c8e106a6"></a>
### Has missed deadline

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_has_missed_deadline`

**Inputs** doc, done\_on\_field, deadline\_field.

**Declared result** bool.

**Explicit results** false · get\_datetime(reached\_on) &gt; get\_datetime(deadline).

**Local steps**

- Set deadline from doc.get(deadline\_field).
- If not deadline.
  - Return false.
- Set reached\_on from (doc.get(done\_on\_field) or doc.get(“on\_hold\_since”) or get\_current\_time()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(done\_on\_field) → doc.get(“on\_hold\_since”) → get\_current\_time().
- Return get\_datetime(reached\_on) &gt; get\_datetime(deadline).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1772) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1269)

<a id="op-6b619f3ce0f279"></a>
### Fail overdue agreements

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_fail_overdue_agreements`

**Inputs** no declared parameters.

**Record and data access** read “Support Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_single\_value(“Support Settings”, “track\_service\_level\_agreement”).
  - Return no value.
- For each doctype in get\_sla\_doctypes().
  - For each name in get\_overdue\_documents(doctype).
    - Evaluate fail\_agreement\_if\_overdue(doctype, name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Support Settings”, “track\_service\_level\_agreement”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1261)

<a id="op-3dd4ffe26bad40"></a>
### Get overdue documents

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_get_overdue_documents`

**Inputs** doctype.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).where(((nested operand in the contract.agreement\_status equals “First Response Due” bitwise  ….

**Local steps**

- Set table from Platform.qb.DocType(doctype).
- Set reached\_on from Coalesce(table.on\_hold\_since, get\_current\_time()).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).where(((nested operand in the contract.agreement\_status equals “First Response Due” bitwise  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1264)

<a id="op-5a34093f1c8fca"></a>
### Fail agreement if overdue

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_fail_agreement_if_overdue`

**Inputs** doctype, name.

**Declared result** no value.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call db\_set on doc.

**Local steps**

- Set doc from Platform.get\_doc(doctype, name, for\_update = true).
- If is\_overdue(doc).
  - Evaluate doc.db\_set(“agreement\_status”, “Failed”, notify = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1763) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1260)

<a id="op-7aa93576b0f1c6"></a>
### Is overdue

`operation_enterprise_binding_enterprise_support_doctype_service_level_agreement_service_level_agreement_is_overdue`

**Inputs** doc.

**Declared result** bool.

**Explicit results** has\_missed\_deadline(doc, “first\_responded\_on”, “response\_by”) · has\_missed\_deadline(doc, “sla\_resolution\_date”, “sla\_resolution\_by”) · false.

**Local steps**

- If doc.agreement\_status equals “First Response Due”.
  - Return has\_missed\_deadline(doc, “first\_responded\_on”, “response\_by”).
- If doc.agreement\_status equals “Resolution Due”.
  - Return has\_missed\_deadline(doc, “sla\_resolution\_date”, “sla\_resolution\_by”).
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1773) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1270)

<a id="op-c9f397b9a18285"></a>
### Is holiday

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_is_holiday`

**Inputs** date, holidays.

**Explicit results** getdate(date) belongs to holidays.

**Local steps**

- Return getdate(date) belongs to holidays.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L6829) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1219)

<a id="op-07753529ad62bc"></a>
### Get time in timedelta

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_time_in_timedelta`

**Inputs** time.

**Explicit results** datetime.timedelta(hours = time.hour, minutes = time.minute, seconds = time.second).

**Local steps**

- Bind dependencies datetime.
- Return datetime.timedelta(hours = time.hour, minutes = time.minute, seconds = time.second).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L6900) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1210)

<a id="op-3f56d3de9df6fe"></a>
### Now datetime

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_now_datetime`

**Inputs** user.

**Explicit results** dt.replace(tzinfo = no value).

**Local steps**

- Set dt from convert\_utc\_to\_user\_timezone(datetime.utcnow(), user).
- Return dt.replace(tzinfo = no value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0970.json#L6999) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1742) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1220)

<a id="op-98177ab3135ca4"></a>
### Convert utc to user timezone

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_convert_coordinated_universal_time_to_user_timezone`

**Inputs** utc\_timestamp, user.

**Explicit results** utcnow.astimezone(ZoneInfo(user\_tz)) · utcnow.

**Local steps**

- Bind dependencies ZoneInfo, ZoneInfoNotFoundError.
- Set user\_tz from get\_tz(user).
- Set utcnow from utc\_timestamp.replace(tzinfo = timezone.utc).
- Attempt the following.
  - Return utcnow.astimezone(ZoneInfo(user\_tz)).
- On failure (ZoneInfoNotFoundError).
  - Return utcnow.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0971.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1194)

<a id="op-a5c4067d6e5735"></a>
### Get tz

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_tz`

**Inputs** user.

**Record and data access** read “User” via get\_value.

**Explicit results** (Platform.db.get\_value(“User”, user, “time\_zone”) or get\_system\_timezone()).

**Local steps**

- Return (Platform.db.get\_value(“User”, user, “time\_zone”) or get\_system\_timezone()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“User”, user, “time\_zone”) → get\_system\_timezone().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0971.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1211)
