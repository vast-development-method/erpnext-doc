# Employment and attendance · operations 44

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-bd202b77c88470"></a>
### Set geolocation from coordinates

`operation_workforce_human_resources_utils_business_behavior_set_geolocation_from_coordinates`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_single\_value(“HR Settings”, “allow\_geolocation\_tracking”).
  - Return no value.
- If not (doc.latitude and doc.longitude).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.latitude → doc.longitude.
  - Return no value.
- Set doc.geolocation from Platform.json.dumps(mapping(“type” → “FeatureCollection”, “features” → list(mapping(“type” → “Feature”, “properties” → mapping(), “geometry” → mapping(“type” → “Point”, “coordinates” → list(nested operand  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “allow\_geolocation\_tracking”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L992) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L164) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L513)

<a id="op-787c3d52e5ba9c"></a>
### Get distance between coordinates

`operation_workforce_human_resources_utils_business_behavior_get_distance_between_coordinates`

**Inputs** lat1, long1, lat2, long2.

**Explicit results** (((2 × r) × asin(sqrt(a))) × 1000).

**Local steps**

- Bind dependencies asin, cos, pi, sqrt.
- Set r from 6371.
- Set p from (pi ÷ 180).
- Set a from ((0.5 − (cos(((lat2 − lat1) × p)) ÷ 2)) + (((cos((lat1 × p)) × cos((lat2 × p))) × (1 − cos(((nested operand in the contract − nested operand in the contract) × p)))) ÷ 2)).
- Return (((2 × r) × asin(sqrt(a))) × 1000).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L1298) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L136) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L485)

<a id="op-820336db79349d"></a>
### Check app permission

`operation_workforce_human_resources_utils_business_behavior_check_application_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L1623) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L130) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L479)

<a id="op-627034b75ab0f8"></a>
### Get exact month diff

`operation_workforce_human_resources_utils_business_behavior_get_exact_month_diff`

**Inputs** string\_ed\_date, string\_st\_date.

**Declared result** int.

**Explicit results** diff.

**Local steps**

- Set ed\_date from getdate(string\_ed\_date).
- Set st\_date from getdate(string\_st\_date).
- Set diff from ((((ed\_date.year − st\_date.year) × 12) + ed\_date.month) − st\_date.month).
- If ed\_date.day ≥ st\_date.day.
  - Update diff using + 1.
- Return diff.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L1831) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L140) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L489)

<a id="op-478cfa4c155f09"></a>
### Get semester start

`operation_workforce_human_resources_utils_business_behavior_get_semester_start`

**Inputs** date.

**Explicit results** get\_year\_start(date) · add\_months(get\_year\_start(date), 6).

**Local steps**

- If date.month ≤ 6.
  - Return get\_year\_start(date).
- Otherwise.
  - Return add\_months(get\_year\_start(date), 6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L2044) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L155) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L504)

<a id="op-3208de030a6011"></a>
### Get semester end

`operation_workforce_human_resources_utils_business_behavior_get_semester_end`

**Inputs** date.

**Explicit results** get\_year\_ending(date) · add\_months(get\_year\_ending(date), negative 6).

**Local steps**

- If date.month &gt; 6.
  - Return get\_year\_ending(date).
- Otherwise.
  - Return add\_months(get\_year\_ending(date), negative 6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L2158) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L154) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L503)

<a id="op-2e272058db4b15"></a>
### Get complete month count

`operation_workforce_human_resources_utils_business_behavior_get_complete_month_count`

**Inputs** date, effective\_from.

**Explicit results** month\_count.

**Local steps**

- Set month\_count from (((date.year − effective\_from.year) × 12) + (date.month − effective\_from.month)).
- If (date.day &lt; effective\_from.day and date differs from get\_last\_day(date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in date.day &lt; effective\_from.day → date differs from get\_last\_day(date).
  - Update month\_count using − 1.
- Return month\_count.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L2276) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L135) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L484)

<a id="op-486fab46b5689b"></a>
### Get half year periods

`operation_workforce_human_resources_utils_business_behavior_get_half_year_periods`

**Inputs** date, effective\_from.

**Explicit results** tuple(half\_year\_start, half\_year\_end).

**Local steps**

- Set effective\_from from getdate(effective\_from).
- Set date from getdate(date).
- Set half\_years\_passed from (get\_complete\_month\_count(date, effective\_from) floor divide 6).
- Set half\_year\_start from add\_months(effective\_from, (half\_years\_passed × 6)).
- Set half\_year\_end from add\_days(add\_months(half\_year\_start, 6), negative 1).
- Return tuple(half\_year\_start, half\_year\_end).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L2460) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L143) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L492)

<a id="op-f83deb78f899cb"></a>
### Notify hr

`operation_workforce_binding_workforce_hr_utils_notify_hr`

**Inputs** doc, subject, message = no value.

**Record and data access** read “User” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies enqueue\_create\_notification.
- Bind dependencies get\_users\_with\_role.
- Set users from (set(get\_users\_with\_role(“HR User”)) bitwise or set(get\_users\_with\_role(“HR Manager”))).
- Set users from list of user for user drawn from users where Platform.has\_permission(doc = doc, ptype = “read”, user = user).
  - Draw user from users, keep a combination only if (Platform.has\_permission(doc = doc, ptype = “read”, user = user)).
- If not users.
  - Return no value.
- Evaluate enqueue\_create\_notification(Platform.get\_all(“User”, filters = mapping(“name” → list(“in”, users)), pluck = “email”), mapping(“type” → “Alert”, “document\_type” → doc.doctype, “document\_name” → doc.name, “s ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doc = doc, ptype = “read”, user = user).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L154) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L205) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L205)

## Report · Vehicle expenses

<a id="op-f00de3584c97fa"></a>
### Execute

`operation_workforce_human_resources_report_vehicle_expenses_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set columns from get\_columns().
- Set data from get\_vehicle\_log\_data(filters).
- Set chart from get\_chart\_data(data, filters).
- Return tuple(columns, data, no value, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L2219) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L117) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L466)

<a id="op-80d61711242e26"></a>
### Get columns

`operation_workforce_human_resources_report_vehicle_expenses_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“fieldname” → “vehicle”, “fieldtype” → “Link”, “label” → translated “Vehicle”, “options” → “Vehicle”, …), mapping(“fieldname” → “make”, “fieldtype” → “Data”, “label” → translated “Make”, “widt ….

**Local steps**

- Return list(mapping(“fieldname” → “vehicle”, “fieldtype” → “Link”, “label” → translated “Vehicle”, “options” → “Vehicle”, …), mapping(“fieldname” → “make”, “fieldtype” → “Data”, “label” → translated “Make”, “widt ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L2396) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L119) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L468)

<a id="op-285dd28a51694a"></a>
### Get vehicle log data

`operation_workforce_human_resources_report_vehicle_expenses_business_behavior_get_vehicle_log_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set tuple(start\_date, end\_date) from get\_period\_dates(filters).
- Set vhcl from Platform.qb.DocType(“Vehicle”).
- Set log from Platform.qb.DocType(“Vehicle Log”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(log.date at slice start\_date to end\_date).orderby(log.date).
- If filters.employee.
  - Set query from query.where(log.employee equals filters.employee).
- If filters.vehicle.
  - Set query from query.where(vhcl.license\_plate equals filters.vehicle).
- Set data from query.run(as\_dict = true).
- For each row in data.
  - Set row at “service\_expense” from get\_service\_expense(row.log\_name).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L3545) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L122) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L471)

<a id="op-c43414436044ae"></a>
### Get period dates

`operation_workforce_human_resources_report_vehicle_expenses_business_behavior_get_period_dates`

**Inputs** filters.

**Record and data access** read “Fiscal Year” via get\_value.

**Explicit results** tuple(fy.year\_start\_date, fy.year\_end\_date) · tuple(filters.from\_date, filters.to\_date).

**Local steps**

- If (filters.filter\_based\_on equals “Fiscal Year” and filters.fiscal\_year).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.filter\_based\_on equals “Fiscal Year” → filters.fiscal\_year.
  - Set fy from Platform.db.get\_value(“Fiscal Year”, filters.fiscal\_year, list(“year\_start\_date”, “year\_end\_date”), as\_dict = true).
  - Return tuple(fy.year\_start\_date, fy.year\_end\_date).
- Otherwise.
  - Return tuple(filters.from\_date, filters.to\_date).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L4262) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L120) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L469)

<a id="op-a15d14d6aab5a6"></a>
### Get service expense

`operation_workforce_human_resources_report_vehicle_expenses_business_behavior_get_service_expense`

**Inputs** logname.

**Explicit results** flt(expense\_amount at 0 at 0) when expense\_amount, otherwise 0.0.

**Local steps**

- Set log from Platform.qb.DocType(“Vehicle Log”).
- Set service from Platform.qb.DocType(“Vehicle Service”).
- Set expense\_amount from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.expense\_amount)).where((log.name equals logname bitwise and log.docstatus equals 1)).run().
- Return flt(expense\_amount at 0 at 0) when expense\_amount, otherwise 0.0.
  - Value choice on expense\_amount — true gives flt(expense\_amount at 0 at 0), false gives 0.0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L4466) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L121) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L470)

<a id="op-7f0f0a2436dcfe"></a>
### Get chart data

`operation_workforce_human_resources_report_vehicle_expenses_business_behavior_get_chart_data`

**Inputs** data, filters.

**Explicit results** chart.

**Local steps**

- Set period\_list from get\_period\_list(filters.fiscal\_year, filters.fiscal\_year, filters.from\_date, filters.to\_date, …).
- Set tuple(fuel\_data, service\_data) from tuple(list(), list()).
- For each period in period\_list.
  - Set total\_fuel\_exp from 0.
  - Set total\_service\_exp from 0.
  - For each row in data.
    - If (row.date ≤ period.to\_date and row.date ≥ period.from\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.date ≤ period.to\_date → row.date ≥ period.from\_date.
      - Update total\_fuel\_exp using + flt(row.fuel\_expense).
      - Update total\_service\_exp using + flt(row.service\_expense).
  - Evaluate fuel\_data.append(list(period.key, total\_fuel\_exp)).
  - Evaluate service\_data.append(list(period.key, total\_service\_exp)).
- Set labels from list of period.label for period drawn from period\_list.
  - Draw period from period\_list.
- Set fuel\_exp\_data from list of row at 1 for row drawn from fuel\_data.
  - Draw row from fuel\_data.
- Set service\_exp\_data from list of row at 1 for row drawn from service\_data.
  - Draw row from service\_data.
- Set datasets from list().
- If fuel\_exp\_data.
  - Evaluate datasets.append(mapping(“name” → translated “Fuel Expenses”, “values” → fuel\_exp\_data)).
- If service\_exp\_data.
  - Evaluate datasets.append(mapping(“name” → translated “Service Expenses”, “values” → service\_exp\_data)).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets), “type” → “line”, “fieldtype” → “Currency”).
- Return chart.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L4806) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L118) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L467)

## Record · Vehicle log

[Record definition](../../../../data/record-types/vehicle_log.json)

<a id="op-20abe4f0499c45"></a>
### Vehicle Log.validate

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_vehicle_log_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Current Odometer Value should be greater than Last Odometer Value {0}”.format(self.last\_odometer).

**Local steps**

- If flt(self.odometer) &lt; flt(self.last\_odometer).
  - Call the validation error handler Platform.throw(translated “Current Odometer Value should be greater than Last Odometer Value {0}”.format(self.last\_odometer)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0078.json#L6529) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1638) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L247)

<a id="op-85290cdff114f8"></a>
### Vehicle Log.on submit

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_vehicle_log_on_submit`

**Inputs** self.

**State and service calls** request set\_value on “Vehicle”.

**Local steps**

- Evaluate Platform.db.set\_value(“Vehicle”, self.license\_plate, “last\_odometer”, self.odometer).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0078.json#L6673) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1637) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L246)

<a id="op-313c1ff980d5e9"></a>
### Vehicle Log.before cancel

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_vehicle_log_before_cancel`

**Inputs** self.

**Record and data access** resolve a document from “Expense Claim” via get\_doc.

**State and service calls** call save on expense\_claim.

**Local steps**

- For each expense\_claim\_name in \_get\_draft\_expense\_claims(self.name).
  - Set expense\_claim from Platform.get\_doc(“Expense Claim”, expense\_claim\_name).
  - If \_has\_non\_vehicle\_log\_expenses(expense\_claim).
    - For each row in list(expense\_claim.expenses).
      - If row.description equals translated “Vehicle Expenses”.
        - Evaluate expense\_claim.remove(row).
    - Set expense\_claim.vehicle\_log from no value.
    - Evaluate expense\_claim.save().
  - Otherwise.
    - Evaluate expense\_claim.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1635) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L244)

<a id="op-017ea563319d85"></a>
### Vehicle Log.on cancel

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_vehicle_log_on_cancel`

**Inputs** self.

**Record and data access** read “Vehicle” via get\_value.

**State and service calls** request set\_value on “Vehicle”.

**Local steps**

- Set distance\_travelled from (self.odometer − self.last\_odometer).
- If distance\_travelled &gt; 0.
  - Set updated\_odometer\_value from (int(Platform.db.get\_value(“Vehicle”, self.license\_plate, “last\_odometer”)) − distance\_travelled).
  - Evaluate Platform.db.set\_value(“Vehicle”, self.license\_plate, “last\_odometer”, updated\_odometer\_value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L282) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1636) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L245)

<a id="op-ff3cfa12737332"></a>
### Make expense claim

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_make_expense_claim`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Expense Claim” via exists · resolve a document from “Vehicle Log” via get\_doc.

**State and service calls** request new\_doc for “Expense Claim”.

**Explicit results** exp\_claim.as\_dict().

**Explicit failure paths** validation helper — translated “Expense Claim {0} already exists for the Vehicle Log”.format(expense\_claim) · validation helper — translated “No additional expenses has been added”.

**Local steps**

- Evaluate Platform.has\_permission(“Vehicle Log”, “read”, docname, throw = true).
- Set expense\_claim from Platform.db.exists(“Expense Claim”, mapping(“vehicle\_log” → docname)).
- If expense\_claim.
  - Call the validation error handler Platform.throw(translated “Expense Claim {0} already exists for the Vehicle Log”.format(expense\_claim)).
- Set vehicle\_log from Platform.get\_doc(“Vehicle Log”, docname).
- Set service\_expense from sum(list of flt(d.expense\_amount) for d drawn from vehicle\_log.service\_detail).
  - Draw d from vehicle\_log.service\_detail.
- Set refuelling\_expense from (flt(vehicle\_log.price) × flt(vehicle\_log.fuel\_qty)).
- Set claim\_amount from (service\_expense + refuelling\_expense).
- If not claim\_amount.
  - Call the validation error handler Platform.throw(translated “No additional expenses has been added”).
- Set exp\_claim from Platform.new\_doc(“Expense Claim”).
- Set exp\_claim.employee from vehicle\_log.employee.
- Set exp\_claim.vehicle\_log from vehicle\_log.name.
- Set exp\_claim.remark from translated “Expense Claim for Vehicle Log {0}”.format(vehicle\_log.name).
- Evaluate exp\_claim.append(“expenses”, mapping(“expense\_date” → vehicle\_log.date, “description” → translated “Vehicle Expenses”, “amount” → claim\_amount)).
- Return exp\_claim.as\_dict().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Vehicle Log”, “read”, docname, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L492) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1634) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L243)

<a id="op-d13008328c5ad0"></a>
### Get draft expense claims

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_get_draft_expense_claims`

**Inputs** vehicle\_log.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** \_get\_draft\_expense\_claims(vehicle\_log).

**Local steps**

- Evaluate Platform.has\_permission(“Vehicle Log”, doc = vehicle\_log, throw = true).
- Return \_get\_draft\_expense\_claims(vehicle\_log).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Vehicle Log”, doc = vehicle\_log, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L1196) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1631) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L240)

<a id="op-4ea3675e67437b"></a>
### Get draft expense claim cancellation actions

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_get_draft_expense_claim_cancellation_actions`

**Inputs** vehicle\_log.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict at tuple(str, str).

**Explicit results** list of mapping(“name” → expense\_claim.name, “action” → “unlink” when \_has\_non\_vehicle\_log\_expenses(expense\_claim), otherwise “delete”) for expense\_claim drawn from \_get\_draft\_expense\_claim\_docs(vehicle\_log).

**Local steps**

- Evaluate Platform.has\_permission(“Vehicle Log”, doc = vehicle\_log, throw = true).
- Return list of mapping(“name” → expense\_claim.name, “action” → “unlink” when \_has\_non\_vehicle\_log\_expenses(expense\_claim), otherwise “delete”) for expense\_claim drawn from \_get\_draft\_expense\_claim\_docs(vehicle\_log).
  - Draw expense\_claim from \_get\_draft\_expense\_claim\_docs(vehicle\_log).
  - Value choice on \_has\_non\_vehicle\_log\_expenses(expense\_claim) — true gives “unlink”, false gives “delete”.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Vehicle Log”, doc = vehicle\_log, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L1334) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1629) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L238)

<a id="op-a59cd1347b3fcc"></a>
### Get draft expense claims

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_get_draft_expense_claims_2`

**Inputs** vehicle\_log.

**Declared result** list at str.

**Record and data access** read “Expense Claim” via get\_all.

**Explicit results** Platform.get\_all(“Expense Claim”, filters = mapping(“vehicle\_log” → vehicle\_log, “docstatus” → 0), pluck = “name”, order\_by = “creation asc”).

**Local steps**

- Return Platform.get\_all(“Expense Claim”, filters = mapping(“vehicle\_log” → vehicle\_log, “docstatus” → 0), pluck = “name”, order\_by = “creation asc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L1574) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1632) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L241)

<a id="op-c746babd9f3d71"></a>
### Get draft expense claim docs

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_get_draft_expense_claim_records`

**Inputs** vehicle\_log.

**Declared result** list at Document.

**Record and data access** resolve a document from “Expense Claim” via get\_doc.

**Explicit results** list of Platform.get\_doc(“Expense Claim”, expense\_claim\_name) for expense\_claim\_name drawn from \_get\_draft\_expense\_claims(vehicle\_log).

**Local steps**

- Return list of Platform.get\_doc(“Expense Claim”, expense\_claim\_name) for expense\_claim\_name drawn from \_get\_draft\_expense\_claims(vehicle\_log).
  - Draw expense\_claim\_name from \_get\_draft\_expense\_claims(vehicle\_log).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L1718) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1630) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L239)
