# Employment and attendance · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Appraisal cycle

[Record definition](../../../../data/record-types/appraisal_cycle.json)

<a id="op-02919e20d6db14"></a>
### Get employees without feedback

`operation_workforce_human_resources_record_definitions_appraisal_cycle_business_behavior_get_employees_without_feedback`

**Inputs** cycle\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** int.

**Record and data access** read “Appraisal Cycle” via get\_value.

**Explicit results** feedback\_missing at 0.count.

**Local steps**

- Set Feedback from Platform.qb.DocType(“Employee Performance Feedback”).
- Set Appraisal from Platform.qb.DocType(“Appraisal”).
- Set count from Count(“\*”).as\_(“count”).
- If not cycle\_name.
  - Set cycle\_name from Platform.get\_value(“Appraisal Cycle”, mapping(“status” → “In Progress”), order\_by = “start\_date desc”).
- Evaluate Platform.has\_permission(“Appraisal Cycle”, “read”, cycle\_name, throw = true).
- Set filtered\_records from SubQuery(nested operand in the contract.select(nested operand in the contract.employee).distinct().where((Feedback.appraisal\_cycle equals cycle\_name bitwise and Feedback.docstatus equals 1))).
- Set feedback\_missing from nested operand in the contract(nested operand in the contract).select(count).where(((nested operand in the contract.appraisal\_cycle equals cycle\_name bitwise and nested operand in the contract.docstatus di ….
- Return feedback\_missing at 0.count.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Appraisal Cycle”, “read”, cycle\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L4811) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L337) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L334)

## Report · Appraisal overview

<a id="op-9d6ebe81204fed"></a>
### Execute

`operation_workforce_human_resources_report_appraisal_overview_business_behavior_execute`

**Inputs** filters = no value.

**Declared result** tuple.

**Explicit results** tuple(columns, data, no value, chart).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Set chart from get\_chart\_data(data).
- Return tuple(columns, data, no value, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L4123) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1649) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L258)

<a id="op-0e082a610723d5"></a>
### Get columns

`operation_workforce_human_resources_report_appraisal_overview_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“fieldname” → “employee”, “fieldtype” → “Link”, “label” → translated “Employee”, “options” → “Employee”, …), mapping(“fieldname” → “employee\_name”, “fieldtype” → “Data”, “label” → translated “ ….

**Local steps**

- Return list(mapping(“fieldname” → “employee”, “fieldtype” → “Link”, “label” → translated “Employee”, “options” → “Employee”, …), mapping(“fieldname” → “employee\_name”, “fieldtype” → “Data”, “label” → translated “ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L4311) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1651) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L260)

<a id="op-bda2de032b52ce"></a>
### Get data

`operation_workforce_human_resources_report_appraisal_overview_business_behavior_get_data`

**Inputs** filters = no value.

**Declared result** list at dict.

**Explicit results** appraisals.

**Local steps**

- Set Appraisal from Platform.qb.DocType(“Appraisal”).
- Set query from Platform.qb.from\_(Appraisal).where(Appraisal.docstatus differs from 2).
- For each condition in list(“appraisal\_cycle”, “employee”, “department”, “designation”, …).
  - If filters.get(condition).
    - Set query from query.where(Appraisal at condition equals filters.get(condition)).
- Set filtered\_appraisals from query.select(Appraisal.name).
- Set query from query.select(Appraisal.employee, Appraisal.employee\_name, Appraisal.designation, Appraisal.department, …).orderby(Appraisal.appraisal\_cycle).orderby(Appraisal.final\_score, order = Platform.qb.desc).
- Set appraisals from query.run(as\_dict = true).
- If not appraisals.
  - Return appraisals.
- Set Feedback from Platform.qb.DocType(“Employee Performance Feedback”).
- Set feedback\_counts from dict(nested operand in the contract.where(nested operand in the contract(nested operand in the contract)).groupby(Feedback.appraisal).run()).
- For each row in appraisals.
  - Set row at “feedback\_count” from feedback\_counts.get(row.appraisal, 0).
- Return appraisals.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L73) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1652) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L261)

<a id="op-fcf0f4a2ad5f4d"></a>
### Get chart data

`operation_workforce_human_resources_report_appraisal_overview_business_behavior_get_chart_data`

**Inputs** data.

**Declared result** dict.

**Explicit results** mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Goal Score”, “values” → goal\_score), mapping(“name” → translated “Self Score”, “values” → self\_score), mapping(“na ….

**Local steps**

- Set labels from list().
- Set goal\_score from list().
- Set self\_score from list().
- Set feedback\_score from list().
- Set final\_score from list().
- For each row in data at slice no value to 10.
  - Evaluate labels.append(row.employee\_name).
  - Evaluate goal\_score.append(row.goal\_score).
  - Evaluate self\_score.append(row.self\_score).
  - Evaluate feedback\_score.append(row.avg\_feedback\_score).
  - Evaluate final\_score.append(row.final\_score).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Goal Score”, “values” → goal\_score), mapping(“name” → translated “Self Score”, “values” → self\_score), mapping(“na ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L6112) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1650) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L259)

## Record · Appraisal template

[Record definition](../../../../data/record-types/appraisal_template.json)

<a id="op-0a1e48f7a4abaa"></a>
### Appraisal Template.validate

`operation_workforce_human_resources_record_definitions_appraisal_template_business_behavior_appraisal_template_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_total\_weightage(“goals”, “KRAs”).
- Evaluate self.validate\_total\_weightage(“rating\_criteria”, “Criteria”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0008.json#L6959) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L344) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L341)

## Record · Asset request

<a id="op-de52ce77ade062"></a>
### Asset Request.onload

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_onload`

**Inputs** self.

**Local steps**

- Evaluate self.set\_onload(“asset\_movement”, self.get\_asset\_movement()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get asset movement](operations-003.md#op-b193f9ce16619a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L35) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L86) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L86)

<a id="op-b6299f18b02c13"></a>
### Asset Request.validate

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_status\_change().
- If self.request\_type equals “Return”.
  - Evaluate self.validate\_return().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate status change](operations-003.md#op-52bf281681d9ce), [validate return](operations-003.md#op-bdb5c2e7d98204).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L36) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L87) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L87)

<a id="op-52bf281681d9ce"></a>
### Asset Request.validate status change

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_validate_status_change`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Set the status to Open, or discard the request to cancel it” · validation helper — translated “Give a rejection reason, so {0} knows what to do next”.format(Platform.bold((self.employee\_name or self.employee))) · validation helper with Platform.PermissionError — translated “Only HR can approve or reject an Asset Request”.

**Local steps**

- <a id="op-52bf281681d9ce-guard-3"></a>If self.status equals “Cancelled”.
  - Call the validation error handler Platform.throw(translated “Set the status to Open, or discard the request to cancel it”).
- If (self.status equals “Rejected” and not (self.rejection\_reason or empty text).strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Rejected” → not (self.rejection\_reason or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rejection\_reason → empty text.
  - Call the validation error handler Platform.throw(translated “Give a rejection reason, so {0} knows what to do next”.format(Platform.bold((self.employee\_name or self.employee))), title = translated “Rejection Reason Missing”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.employee\_name → self.employee.
- If (self.status belongs to tuple(“Approved”, “Rejected”) and not Platform.has\_permission(self.doctype, “submit”, self)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status belongs to tuple(“Approved”, “Rejected”) → not Platform.has\_permission(self.doctype, “submit”, self).
  - Call the validation error handler Platform.throw(translated “Only HR can approve or reject an Asset Request”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Cancelled”, self.status = “Cancelled” selects the branch that calls the validation-error handler with translated “Set the status to Open, or discard the request to cancel it”. With self.status = “Open”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-52bf281681d9ce-guard-3)

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “submit”, self).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L38) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L89) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L89)

<a id="op-bdb5c2e7d98204"></a>
### Asset Request.validate return

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_validate_return`

**Inputs** self.

**Record and data access** read “Asset” via get\_value · read self.doctype via exists.

**Explicit failure paths** validation helper — translated “{0} does not hold asset {1}”.format(Platform.bold((self.employee\_name or self.employee)), Platform.bold(self.asset)) · validation helper — translated “Asset {0} already has an open return request {1}”.format(Platform.bold(self.asset), get\_link\_to\_form(self.doctype, open\_return)).

**Local steps**

- If Platform.db.get\_value(“Asset”, self.asset, “custodian”) differs from self.employee.
  - Call the validation error handler Platform.throw(translated “{0} does not hold asset {1}”.format(Platform.bold((self.employee\_name or self.employee)), Platform.bold(self.asset)), title = translated “Not the Custodian”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.employee\_name → self.employee.
- Set open\_return from Platform.db.exists(self.doctype, mapping(“asset” → self.asset, “request\_type” → “Return”, “docstatus” → 0, “name” → list(“!=”, (self.name or empty text)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → empty text.
- If open\_return.
  - Call the validation error handler Platform.throw(translated “Asset {0} already has an open return request {1}”.format(Platform.bold(self.asset), get\_link\_to\_form(self.doctype, open\_return)), title = translated “Open Request Exists”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L37) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L88) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L88)

<a id="op-6a308300a70f25"></a>
### Asset Request.after insert

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_after_insert`

**Inputs** self.

**Local steps**

- If self.request\_type equals “Issue”.
  - Set asks from translated “Asks for {0}”.format(escape\_html((self.asset\_category or empty text))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.asset\_category → empty text.
- Otherwise.
  - Set asks from translated “Returns {0}”.format(escape\_html((self.asset\_name or self.asset or empty text))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.asset\_name → self.asset → empty text.
- Evaluate notify\_hr(self, translated “{0} raised an asset request”.format(escape\_html(self.employee\_name)), formatted text &lt;p&gt;{asks}&lt;/p&gt;&lt;p&gt;{translated “Reason”}: {escape\_html((self.reason or “-”))}&lt;/p&gt;).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.reason → “-”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L31) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L82) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L82)

<a id="op-177b92cdb49b0a"></a>
### Asset Request.on discard

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L33) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L84) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L84)

<a id="op-94d20758faa845"></a>
### Asset Request.on submit

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_on_submit`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Approve or reject the request before submitting it”.

**Local steps**

- <a id="op-94d20758faa845-guard-2"></a>If self.status does not belong to tuple(“Approved”, “Rejected”).
  - Call the validation error handler Platform.throw(translated “Approve or reject the request before submitting it”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status does not belong to tuple(“Approved”, “Rejected”), self.status = “Open” selects the branch that calls the validation-error handler with translated “Approve or reject the request before submitting it”. With self.status = “Approved”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-94d20758faa845-guard-2)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L34) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L85) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L85)

<a id="op-b193f9ce16619a"></a>
### Asset Request.get asset movement

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_assetrequest_get_asset_movement`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read “Asset Movement” via get\_value.

**Explicit results** Platform.db.get\_value(“Asset Movement”, mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name, “docstatus” → list(“!=”, 2)), “name”).

**Local steps**

- Return Platform.db.get\_value(“Asset Movement”, mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name, “docstatus” → list(“!=”, 2)), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L32) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L83) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L83)

<a id="op-a5621c57a6af0b"></a>
### Make asset movement

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_make_asset_movement`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Document.

**Explicit results** get\_mapped\_doc(“Asset Request”, source\_name, mapping(“Asset Request” → mapping(“doctype” → “Asset Movement”, “field\_map” → mapping(“company” → “company”), “validation” → mapping(“docstatus” → list(“=”, 1), ….

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Return get\_mapped\_doc(“Asset Request”, source\_name, mapping(“Asset Request” → mapping(“doctype” → “Asset Movement”, “field\_map” → mapping(“company” → “company”), “validation” → mapping(“docstatus” → list(“=”, 1), ….

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L39) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L90) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L90)

<a id="op-b6c26c57cb2ff9"></a>
### Make asset movement.set missing values

`operation_workforce_binding_workforce_hr_doctype_asset_request_asset_request_make_asset_movement_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.purpose from “Issue” when source.request\_type equals “Issue”, otherwise “Receipt”.
  - Value choice on source.request\_type equals “Issue” — true gives “Issue”, false gives “Receipt”.
- Set target.transaction\_date from now\_datetime().
- Set target.reference\_doctype from source.doctype.
- Set target.reference\_name from source.name.
- If source.request\_type equals “Issue”.
  - Evaluate target.append(“assets”, mapping(“to\_employee” → source.employee)).
- Otherwise.
  - Evaluate target.append(“assets”, mapping(“asset” → source.asset, “from\_employee” → source.employee)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L40) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L91) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L91)

## Service · Asset request decided

<a id="op-10ce67d414af3a"></a>
### Get context

`operation_workforce_binding_workforce_hr_notification_asset_request_decided_asset_request_decided_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L87) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L138) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L138)

## Record · Attendance

[Record definition](../../../../data/record-types/attendance.json)

<a id="op-4e5e4a2a80b80a"></a>
### Attendance.before insert

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_before_insert`

**Inputs** self.

**Local steps**

- If self.half\_day\_status equals empty text.
  - Set self.half\_day\_status from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L938) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L366) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L363)

<a id="op-b43f30556e0c4d"></a>
### Attendance.validate

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_validate`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_status.
- Evaluate validate\_status(self.status, list(“Present”, “Absent”, “On Leave”, “Half Day”, …)).
- Evaluate validate\_active\_employee(self.employee).
- Evaluate self.validate\_attendance\_date().
- Evaluate self.validate\_duplicate\_record().
- Evaluate self.validate\_overlapping\_shift\_attendance().
- Evaluate self.validate\_employee\_status().
- Evaluate self.check\_leave\_record().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate attendance date](operations-003.md#op-e088aa1e440a78), [validate duplicate record](operations-003.md#op-4ba38faaa61076), [validate overlapping shift attendance](operations-003.md#op-02b6b68a094a2e), [validate employee status](operations-004.md#op-0a7746d1001f6d), [check leave record](operations-004.md#op-229f2015e27252).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L1010) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L374) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L371)

<a id="op-4d1e659b455923"></a>
### Attendance.on cancel

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.unlink\_attendance\_from\_checkins().

If control reaches the end, it returns no value.

**Methods declared on this owner** [unlink attendance from checkins](operations-004.md#op-50887b2705c446).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L1225) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L370) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L367)

<a id="op-e088aa1e440a78"></a>
### Attendance.validate attendance date

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_validate_attendance_date`

**Inputs** self.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “Attendance date {0} can not be less than employee {1}'s joining date: {2}”.format(Platform.bold(format\_date(self.attendance\_date)), Platform.bold(self.employee), Platform.bold(format\_date(date\_ ….

**Local steps**

- Set date\_of\_joining from Platform.db.get\_value(“Employee”, self.employee, “date\_of\_joining”).
- If (date\_of\_joining and getdate(self.attendance\_date) &lt; getdate(date\_of\_joining)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in date\_of\_joining → getdate(self.attendance\_date) &lt; getdate(date\_of\_joining).
  - Call the validation error handler Platform.throw(translated “Attendance date {0} can not be less than employee {1}'s joining date: {2}”.format(Platform.bold(format\_date(self.attendance\_date)), Platform.bold(self.employee), Platform.bold(fo ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L1276) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L375) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L372)

<a id="op-4ba38faaa61076"></a>
### Attendance.validate duplicate record

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_validate_duplicate_record`

**Inputs** self.

**Explicit failure paths** validation helper with DuplicateAttendanceError — translated “Attendance for employee {0} is already marked for the date {1}: {2}”.format(Platform.bold(self.employee), Platform.bold(format\_date(self.attendance\_date)), get\_link\_to\_form(“Attendance”, duplicate)).

**Local steps**

- Set duplicate from self.get\_duplicate\_attendance\_record().
- If duplicate.
  - Call the validation error handler Platform.throw(translated “Attendance for employee {0} is already marked for the date {1}: {2}”.format(Platform.bold(self.employee), Platform.bold(format\_date(self.attendance\_date)), get\_link\_to\_form(“Atte ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get duplicate attendance record](operations-003.md#op-1a925e81b9d960).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L1576) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L376) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L373)

<a id="op-1a925e81b9d960"></a>
### Attendance.get duplicate attendance record

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_get_duplicate_attendance_record`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** duplicate at 0 when duplicate, otherwise no value.

**Local steps**

- Set Attendance from Platform.qb.DocType(“Attendance”).
- Set query from nested operand in the contract(nested operand in the contract).select(Attendance.name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the …().
- If self.shift.
  - Set query from query.where(((Attendance.shift.isnull() bitwise or Attendance.shift equals empty text) bitwise or ((nested operand in the contract.shift.isnotnull() bitwise or Attendance.shift differs from empty text) bit ….
- Set duplicate from query.run(pluck = true).
- Return duplicate at 0 when duplicate, otherwise no value.
  - Value choice on duplicate — true gives duplicate at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L1821) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L368) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L365)

<a id="op-02b6b68a094a2e"></a>
### Attendance.validate overlapping shift attendance

`operation_workforce_human_resources_record_definitions_attendance_business_behavior_attendance_validate_overlapping_shift_attendance`

**Inputs** self.

**Explicit failure paths** validation helper with OverlappingShiftAttendanceError — translated “Attendance for employee {0} is already marked for an overlapping shift {1}: {2}”.format(Platform.bold(self.employee), Platform.bold(attendance.shift), get\_link\_to\_form(“Attendance”, attendance.name)).

**Local steps**

- Set attendance from self.get\_overlapping\_shift\_attendance().
- If attendance.
  - Call the validation error handler Platform.throw(translated “Attendance for employee {0} is already marked for an overlapping shift {1}: {2}”.format(Platform.bold(self.employee), Platform.bold(attendance.shift), get\_link\_to\_form(“Attendanc ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get overlapping shift attendance](operations-004.md#op-58c42fcf8ea604).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0009.json#L2372) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L379) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L376)
