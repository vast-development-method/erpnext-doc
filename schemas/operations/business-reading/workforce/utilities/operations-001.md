# Supporting services · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Custom method for charts

<a id="op-eb548584c1a4d3"></a>
### Get upcoming holidays

`operation_workforce_utils_custom_method_for_charts_business_behavior_get_upcoming_holidays`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Employee” via get\_value · read “Holiday” via get\_all.

**Explicit results** 0 · len(holidays).

**Local steps**

- Set employee from Platform.get\_value(“Employee”, mapping(“user\_id” → Platform.session.user), “name”).
- If employee.
  - Set holiday\_list from get\_holiday\_list\_for\_employee(employee, raise\_exception = false, as\_on = getdate()).
- Otherwise.
  - Set default\_company from get\_default\_company().
  - Set holiday\_list from get\_assigned\_holiday\_list(default\_company, as\_on = getdate()).
- If not holiday\_list.
  - Return 0.
- Set month\_start from get\_first\_day(getdate()).
- Set month\_end from get\_last\_day(getdate()).
- Set holidays from Platform.db.get\_all(“Holiday”, mapping(“parent” → holiday\_list, “holiday\_date” → tuple(“between”, tuple(month\_start, month\_end)))).
- Return len(holidays).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0158.json#L2995) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1220) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L166)

## Service · Desktop

<a id="op-840db9a058cc90"></a>
### Get data

`operation_workforce_configuration_desktop_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“module\_name” → “Workforce”, “type” → “module”, “label” → translated “Workforce”)).

**Local steps**

- Return list(mapping(“module\_name” → “Workforce”, “type” → “module”, “label” → translated “Workforce”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L1177) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L257) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L257)

## Service · Docs

<a id="op-9b1cdd9b1deac6"></a>
### Get context

`operation_workforce_configuration_records_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Set context.brand\_html from “Workforce”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../workforce-decision-contracts/part-0004.json#L1280) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L258) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L258)

## Service · Hierarchy chart

<a id="op-4a9f77933d0521"></a>
### Get all nodes

`operation_workforce_utils_hierarchy_chart_business_behavior_get_all_nodes`

**Inputs** method, company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** result.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- If method does not belong to ALLOWED\_METHODS.
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Set method from Platform.get\_attr(method).
- Set root\_nodes from method(company = company).
- Set result from list().
- Set nodes\_to\_expand from list().
- For each root in root\_nodes.
  - Set data from method(root.id, company).
  - Evaluate result.append(dict(parent = root.id, parent\_name = root.name, data = data)).
  - Evaluate nodes\_to\_expand.extend(list of mapping(“id” → d.get(“id”), “name” → d.get(“name”)) for d drawn from data where d.get(“expandable”)).
    - Draw d from data, keep a combination only if (d.get(“expandable”)).
- While nodes\_to\_expand.
  - Set parent from nodes\_to\_expand.pop(0).
  - Set data from method(parent.get(“id”), company).
  - Evaluate result.append(dict(parent = parent.get(“id”), parent\_name = parent.get(“name”), data = data)).
  - For each d in data.
    - If d.get(“expandable”).
      - Evaluate nodes\_to\_expand.append(mapping(“id” → d.get(“id”), “name” → d.get(“name”))).
- Return result.

**Values supplied outside this operation** selected callable from Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L29) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1221) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L167)

## Service · Holiday list

<a id="op-ab8a1b3b43ea89"></a>
### Get holiday dates between

`operation_workforce_utils_holiday_list_business_behavior_get_holiday_dates_between`

**Inputs** holiday\_list, start\_date, end\_date, skip\_weekly\_offs = false, as\_dict = false, select\_weekly\_off = false, only\_half\_days = false.

**Declared result** list.

**Explicit results** query.run(as\_dict = true) · query.run(pluck = true).

**Local steps**

- Set Holiday from Platform.qb.DocType(“Holiday”).
- Set query from Platform.qb.from\_(Holiday).select(Holiday.holiday\_date).
- If select\_weekly\_off.
  - Set query from query.select(Holiday.weekly\_off).
- Set query from query.where((Holiday.parent equals holiday\_list bitwise and Holiday.holiday\_date.between(start\_date, end\_date))).
- If skip\_weekly\_offs.
  - Set query from query.where(Holiday.weekly\_off equals 0).
- If only\_half\_days.
  - Set query from query.where(Holiday.is\_half\_day equals 1).
- If as\_dict.
  - Return query.run(as\_dict = true).
- Return query.run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L32) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1227) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L171)

<a id="op-aec025f98ddbd9"></a>
### Get holiday dates between range

`operation_workforce_utils_holiday_list_business_behavior_get_holiday_dates_between_range`

**Inputs** assigned\_to, start\_date, end\_date, skip\_weekly\_offs = false, select\_weekly\_offs = false, raise\_exception\_for\_holiday\_list = true, as\_dict = false.

**Declared result** list.

**Explicit results** holidays · list of holiday.holiday\_date for holiday drawn from holidays.

**Local steps**

- Set holiday\_list\_ranges from get\_holiday\_list\_ranges\_for\_employee(assigned\_to, start\_date, end\_date, raise\_exception = raise\_exception\_for\_holiday\_list).
- Set holidays from get\_holidays\_in\_ranges(holiday\_list\_ranges, skip\_weekly\_offs = skip\_weekly\_offs).
- If as\_dict.
  - Return holidays.
- Return list of holiday.holiday\_date for holiday drawn from holidays.
  - Draw holiday from holidays.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L33) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1228) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L172)

<a id="op-574b92fb36db0e"></a>
### Get holidays in ranges

`operation_workforce_binding_workforce_utils_holiday_list_get_holidays_in_ranges`

**Inputs** holiday\_list\_ranges, skip\_weekly\_offs = false.

**Declared result** list at Platform.\_dict.

**Explicit results** get\_holidays\_in\_ranges\_map(mapping(no value → holiday\_list\_ranges), skip\_weekly\_offs).get(no value, list()).

**Local steps**

- Return get\_holidays\_in\_ranges\_map(mapping(no value → holiday\_list\_ranges), skip\_weekly\_offs).get(no value, list()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L202) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L253) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L253)

<a id="op-319b645cc98166"></a>
### Get holidays in ranges map

`operation_workforce_binding_workforce_utils_holiday_list_get_holidays_in_ranges_map`

**Inputs** holiday\_list\_ranges\_map, skip\_weekly\_offs = false.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Explicit results** mapping() · holidays\_map.

**Local steps**

- Set all\_ranges from list of holiday\_list\_range for holiday\_list\_ranges drawn from holiday\_list\_ranges\_map.values(), then holiday\_list\_range drawn from holiday\_list\_ranges.
  - Draw holiday\_list\_ranges from holiday\_list\_ranges\_map.values().
  - Draw holiday\_list\_range from holiday\_list\_ranges.
- If not all\_ranges.
  - Return mapping().
- Set Holiday from Platform.qb.DocType(“Holiday”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(nested operand in the contract.isin(n ….
  - Draw r from all\_ranges.
  - Draw r from all\_ranges.
  - Draw r from all\_ranges.
- If skip\_weekly\_offs.
  - Set query from query.where(Holiday.weekly\_off equals 0).
- Set holidays\_by\_list from mapping().
- For each holiday in query.run(as\_dict = true).
  - Evaluate holidays\_by\_list.setdefault(holiday.parent, list()).append(holiday).
- Set holidays\_map from mapping().
- For each tuple(key, holiday\_list\_ranges) in holiday\_list\_ranges\_map.items().
  - Set holidays from list of holiday for holiday\_list\_range drawn from sorted(holiday\_list\_ranges, key = deferred anonymous expression), then holiday drawn from holidays\_by\_list.get(holiday\_list\_range at “holiday\_list”, list() ….
    - Draw holiday\_list\_range from sorted(holiday\_list\_ranges, key = deferred anonymous expression).
    - Draw holiday from holidays\_by\_list.get(holiday\_list\_range at “holiday\_list”, list()), keep a combination only if (getdate(holiday\_list\_range at “from\_date”) ≤ getdate(holiday.holiday\_date) ≤ getdate(holiday\_list\_range at “to\_date”)).
    - Compare adjacent operands in order, stopping at the first false comparison in getdate(holiday\_list\_range at “from\_date”) ≤ getdate(holiday.holiday\_date) ≤ getdate(holiday\_list\_range at “to\_date”).
  - If holidays.
    - Set holidays\_map at key from holidays.
- Return holidays\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L2) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L254) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L254)

<a id="op-ab7b3ace2c3163"></a>
### Get holiday list ranges for employee

`operation_workforce_binding_workforce_utils_holiday_list_get_holiday_list_ranges_for_employee`

**Inputs** employee, start\_date, end\_date, raise\_exception = true.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Employee” via get\_value.

**Explicit results** get\_holiday\_list\_ranges\_for\_employees(mapping(employee → company), start\_date, end\_date, raise\_exception = raise\_exception).get(employee, list()).

**Local steps**

- Set company from Platform.db.get\_value(“Employee”, employee, “company”).
- Return get\_holiday\_list\_ranges\_for\_employees(mapping(employee → company), start\_date, end\_date, raise\_exception = raise\_exception).get(employee, list()).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L200) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L251) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L251)

<a id="op-28bdc7f29b0db4"></a>
### Get holiday list ranges for employees

`operation_workforce_binding_workforce_utils_holiday_list_get_holiday_list_ranges_for_employees`

**Inputs** employee\_company\_map, start\_date, end\_date, raise\_exception = false.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Explicit results** mapping() · employee\_holiday\_list\_ranges.

**Local steps**

- If not employee\_company\_map.
  - Return mapping().
- Set start\_date from getdate(start\_date).
- Set end\_date from getdate(end\_date).
- Set companies from list(set of company for company drawn from employee\_company\_map.values() where company).
  - Draw company from employee\_company\_map.values(), keep a combination only if (company).
- Set assignments from get\_holiday\_list\_assignments((list(employee\_company\_map) + companies)).
- Set effective\_ranges from build\_effective\_date\_ranges\_for\_holiday\_assignments(assignments, start\_date, end\_date).
- Set employee\_holiday\_list\_ranges from mapping().
- For each tuple(employee, company) in employee\_company\_map.items().
  - Set ranges from fill\_employee\_holiday\_list\_date\_gaps\_with\_company\_holiday\_list(effective\_ranges.get(employee, list()), effective\_ranges.get(company, list()), start\_date, end\_date).
  - Set ranges from fill\_uncovered\_dates\_with\_assigned\_holiday\_list(ranges, assignments.get(employee, list()), assignments.get(company, list()), start\_date, …).
  - If ranges.
    - Set employee\_holiday\_list\_ranges at employee from ranges.
  - Otherwise.
    - If raise\_exception.
      - Evaluate throw\_no\_holiday\_list\_assigned(employee, company, start\_date).
- Return employee\_holiday\_list\_ranges.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L201) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L252) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L252)

<a id="op-91bf1d514c4322"></a>
### Fill uncovered dates with assigned holiday list

`operation_workforce_binding_workforce_utils_holiday_list_fill_uncovered_dates_with_assigned_holiday_list`

**Inputs** ranges, employee\_assignments, company\_assignments, start\_date, end\_date.

**Declared result** list at Platform.\_dict.

**Explicit results** filled.

**Local steps**

- Set filled from list().
- Bind local operation add\_range for subsequent calls.
- Set current from start\_date.
- For each holiday\_list\_range in list(expanded sorted(ranges, key = deferred anonymous expression), no value).
  - Set gap\_end from add\_days(holiday\_list\_range at “from\_date”, negative 1) when holiday\_list\_range, otherwise end\_date.
    - Value choice on holiday\_list\_range — true gives add\_days(holiday\_list\_range at “from\_date”, negative 1), false gives end\_date.
  - If current ≤ gap\_end.
    - Set assignment from resolve\_holiday\_list\_assignment(employee\_assignments, company\_assignments, current).
    - If assignment.
      - Evaluate add\_range(assignment.holiday\_list, current, gap\_end).
  - If holiday\_list\_range.
    - Evaluate add\_range(holiday\_list\_range at “holiday\_list”, getdate(holiday\_list\_range at “from\_date”), getdate(holiday\_list\_range at “to\_date”)).
    - Set current from add\_days(holiday\_list\_range at “to\_date”, 1).
- Return filled.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L197) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L248) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L248)

<a id="op-269de1ff13958b"></a>
### Fill uncovered dates with assigned holiday list.add range

`operation_workforce_binding_workforce_utils_holiday_list_fill_uncovered_dates_with_assigned_holiday_list_add_range`

**Inputs** holiday\_list, from\_date, to\_date.

**Local steps**

- Set last from filled at negative 1 when filled, otherwise no value.
  - Value choice on filled — true gives filled at negative 1, false gives no value.
- If (last and last.holiday\_list equals holiday\_list and add\_days(last.to\_date, 1) equals from\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last → last.holiday\_list equals holiday\_list → add\_days(last.to\_date, 1) equals from\_date.
  - Set last.to\_date from to\_date.
- Otherwise.
  - Evaluate filled.append(Platform.\_dict(holiday\_list = holiday\_list, from\_date = from\_date, to\_date = to\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L198) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L249) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L249)

<a id="op-b1b453786daf65"></a>
### Resolve holiday list assignment

`operation_workforce_binding_workforce_utils_holiday_list_resolve_holiday_list_assignment`

**Inputs** employee\_assignments, company\_assignments, as\_on.

**Declared result** (Platform.\_dict bitwise or no value).

**Explicit results** active at negative 1 · assignments at 0 · no value.

**Local steps**

- For each assignments in tuple(employee\_assignments, company\_assignments).
  - Set active from list of a for a drawn from assignments where getdate(a.from\_date) ≤ as\_on.
    - Draw a from assignments, keep a combination only if (getdate(a.from\_date) ≤ as\_on).
  - If active.
    - Return active at negative 1.
- For each assignments in tuple(employee\_assignments, company\_assignments).
  - If assignments.
    - Return assignments at 0.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L3) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L255) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L255)

<a id="op-7f89ebe66e0716"></a>
### Get holiday list assignments

`operation_workforce_binding_workforce_utils_holiday_list_get_holiday_list_assignments`

**Inputs** assigned\_to\_list.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Explicit results** mapping() · assignment\_map.

**Local steps**

- Set assigned\_to\_list from list of assigned\_to for assigned\_to drawn from assigned\_to\_list where assigned\_to.
  - Draw assigned\_to from assigned\_to\_list, keep a combination only if (assigned\_to).
- If not assigned\_to\_list.
  - Return mapping().
- Set HLA from Platform.qb.DocType(“Holiday List Assignment”).
- Set assignments from nested operand in the contract(nested operand in the contract).orderby(HLA.assigned\_to).orderby(HLA.from\_date).run(as\_dict = true).
- Set assignment\_map from mapping().
- For each assignment in assignments.
  - Evaluate assignment\_map.setdefault(assignment.assigned\_to, list()).append(assignment).
- Return assignment\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L199) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L250) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L250)

<a id="op-50ca626ae34510"></a>
### Get holiday list for employee

`operation_workforce_utils_holiday_list_business_behavior_get_holiday_list_for_employee`

**Inputs** employee, raise\_exception = true, as\_on = no value, as\_dict = false.

**Declared result** str.

**Record and data access** read “Employee” via get\_value.

**Explicit results** no value · Platform.\_dict(holiday\_list = assignment.holiday\_list, from\_date = assignment.from\_date) · assignment.holiday\_list.

**Local steps**

- Set as\_on from getdate(as\_on).
- Set company from Platform.db.get\_value(“Employee”, employee, “company”).
- Set assignments from get\_holiday\_list\_assignments(list(employee, company)).
- Set assignment from resolve\_holiday\_list\_assignment(assignments.get(employee, list()), assignments.get(company, list()), as\_on).
- If not assignment.
  - If raise\_exception.
    - Evaluate throw\_no\_holiday\_list\_assigned(employee, company, as\_on).
  - Return no value.
- If as\_dict.
  - Return Platform.\_dict(holiday\_list = assignment.holiday\_list, from\_date = assignment.from\_date).
- Return assignment.holiday\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L34) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1229) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L173)

<a id="op-2ca141d8fbfd02"></a>
### Throw no holiday list assigned

`operation_workforce_binding_workforce_utils_holiday_list_throw_no_holiday_list_assigned`

**Inputs** employee, company, as\_on.

**Explicit failure paths** validation helper — translated “No Holiday List was found for Employee {0} or their company {1} for date {2}. Please assign through {3}”.format(Platform.bold(employee), Platform.bold(company), Platform.bold(formatdate(as\_on)) ….

**Local steps**

- Call the validation error handler Platform.throw(translated “No Holiday List was found for Employee {0} or their company {1} for date {2}. Please assign through {3}”.format(Platform.bold(employee), Platform.bold(company), Platform.bold(for ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L4) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L256) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L256)

<a id="op-14972e4f3ba6cb"></a>
### Get assigned holiday list

`operation_workforce_utils_holiday_list_business_behavior_get_assigned_holiday_list`

**Inputs** assigned\_to, as\_on = no value, as\_dict = false.

**Declared result** str.

**Explicit results** no value · Platform.\_dict(holiday\_list = assignment.holiday\_list, from\_date = assignment.from\_date) · assignment.holiday\_list.

**Local steps**

- Set as\_on from getdate(as\_on).
- Set assignments from get\_holiday\_list\_assignments(list(assigned\_to)).get(assigned\_to, list()).
- Set active from list of a for a drawn from assignments where getdate(a.from\_date) ≤ as\_on.
  - Draw a from assignments, keep a combination only if (getdate(a.from\_date) ≤ as\_on).
- If not active.
  - Return no value.
- Set assignment from active at negative 1.
- If as\_dict.
  - Return Platform.\_dict(holiday\_list = assignment.holiday\_list, from\_date = assignment.from\_date).
- Return assignment.holiday\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L31) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1225) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L170)

<a id="op-a43c5bed391dcc"></a>
### Build effective date ranges for holiday assignments

`operation_workforce_utils_holiday_list_business_behavior_build_effective_date_ranges_for_holiday_assignments`

**Inputs** holiday\_assignment\_map, start\_date, end\_date.

**Declared result** dict at tuple(str, list at dict).

**Explicit results** result.

**Local steps**

- Set result from mapping().
- For each tuple(assigned\_to, assignments) in holiday\_assignment\_map.items().
  - Set ranges from list().
  - For each tuple(idx, assignment) in enumerate(assignments).
    - Set next\_assignment from assignments at (idx + 1) when (idx + 1) &lt; len(assignments), otherwise no value.
      - Value choice on (idx + 1) &lt; len(assignments) — true gives assignments at (idx + 1), false gives no value.
    - Set effective\_to\_date from add\_days(next\_assignment.from\_date, negative 1) when next\_assignment, otherwise end\_date.
      - Value choice on next\_assignment — true gives add\_days(next\_assignment.from\_date, negative 1), false gives end\_date.
    - Set from\_date from max(getdate(assignment.from\_date), start\_date).
    - Set effective\_to\_date from min(getdate(effective\_to\_date), end\_date).
    - If from\_date ≤ effective\_to\_date.
      - Evaluate ranges.append(mapping(“holiday\_list” → assignment.holiday\_list, “from\_date” → from\_date, “to\_date” → effective\_to\_date)).
  - If ranges.
    - Set result at assigned\_to from ranges.
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L30) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1222) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L168)

<a id="op-93f5f9b788a969"></a>
### Fill employee holiday list date gaps with company holiday list

`operation_workforce_utils_holiday_list_business_behavior_fill_employee_holiday_list_date_gaps_with_company_holiday_list`

**Inputs** primary\_ranges, fallback\_ranges, start\_date, end\_date.

**Declared result** list at dict.

**Explicit results** fallback\_ranges · primary\_ranges · sorted(result, key = deferred anonymous expression).

**Local steps**

- If not primary\_ranges.
  - Return fallback\_ranges.
- If not fallback\_ranges.
  - Return primary\_ranges.
- Set result from list().
- Set current from start\_date.
- For each primary in sorted(primary\_ranges, key = deferred anonymous expression).
  - Set gap\_end from add\_days(primary at “from\_date”, negative 1).
  - If current ≤ gap\_end.
    - For each fallback in fallback\_ranges.
      - Set overlap\_start from max(getdate(fallback at “from\_date”), current).
      - Set overlap\_end from min(getdate(fallback at “to\_date”), gap\_end).
      - If overlap\_start ≤ overlap\_end.
        - Evaluate result.append(mapping(“holiday\_list” → fallback at “holiday\_list”, “from\_date” → overlap\_start, “to\_date” → overlap\_end)).
  - Evaluate result.append(primary).
  - Set current from add\_days(primary at “to\_date”, 1).
- If current ≤ end\_date.
  - For each fallback in fallback\_ranges.
    - Set overlap\_start from max(getdate(fallback at “from\_date”), current).
    - Set overlap\_end from min(getdate(fallback at “to\_date”), end\_date).
    - If overlap\_start ≤ overlap\_end.
      - Evaluate result.append(mapping(“holiday\_list” → fallback at “holiday\_list”, “from\_date” → overlap\_start, “to\_date” → overlap\_end)).
- Return sorted(result, key = deferred anonymous expression).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L618) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1224) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L169)

<a id="op-fc51712c5b2f05"></a>
### Clip holiday list ranges

`operation_workforce_binding_workforce_utils_holiday_list_clip_holiday_list_ranges`

**Inputs** holiday\_list\_ranges, start\_date, end\_date.

**Declared result** list at dict.

**Explicit results** clipped.

**Local steps**

- Set clipped from list().
- For each holiday\_list\_range in holiday\_list\_ranges.
  - Set from\_date from max(getdate(holiday\_list\_range at “from\_date”), getdate(start\_date)).
  - Set to\_date from min(getdate(holiday\_list\_range at “to\_date”), getdate(end\_date)).
  - If from\_date ≤ to\_date.
    - Evaluate clipped.append(Platform.\_dict(holiday\_list = holiday\_list\_range at “holiday\_list”, from\_date = from\_date, to\_date = to\_date)).
- Return clipped.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L196) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L247) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L247)

<a id="op-294e5931b77129"></a>
### Invalidate cache

`operation_workforce_utils_holiday_list_business_behavior_invalidate_cache`

**Inputs** doc, method = no value.

**Local steps**

- Bind dependencies HOLIDAYS\_BETWEEN\_DATES.
- Evaluate Platform.cache().delete\_value(HOLIDAYS\_BETWEEN\_DATES).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L1515) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1230) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L174)

## Service · Index

<a id="op-21e692b41953cb"></a>
### Get context

`operation_workforce_public_pages_jobs_index_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Set context.no\_cache from 1.
- If Platform.session.user equals “Guest”.
  - Set context.parents from list(mapping(“name” → translated “Home”, “route” → “/”)).
- Otherwise.
  - Set context.parents from list(mapping(“name” → translated “My Account”, “route” → “/me”)).
- Set context.body\_class from “jobs-page”.
- Set page\_len from 20.
- Set tuple(filters, txt, sort, offset) from get\_filters\_txt\_sort\_offset(page\_len).
- Set context.job\_openings from get\_job\_openings(filters, txt, sort, page\_len, …).
- Set context.no\_of\_pages from get\_no\_of\_pages(filters, txt, page\_len).
- Set context.all\_filters from get\_all\_filters(filters).
- Set context.sort from sort.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L2187) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1053) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L4)

<a id="op-539e91251993bd"></a>
### Get job openings

`operation_workforce_public_pages_jobs_index_business_behavior_get_job_openings`

**Inputs** filters = no value, txt = no value, sort = no value, limit = 20, offset = 0.

**Explicit results** results.

**Local steps**

- Set jo from Platform.qb.DocType(“Job Opening”).
- Set ja from Platform.qb.DocType(“Job Applicant”).
- Set query from nested operand in the contract(nested operand in the contract).groupby(jo.name).limit(limit).offset(offset).
- For each d in filters.
  - Set query from query.where(Platform.qb.Field(d).isin(filters at d)).
- If txt.
  - Set query from query.where((jo.job\_title.like(formatted text %{txt}%) bitwise or jo.description.like(formatted text %{txt}%))).
- Set query from query.orderby(“posted\_on”, order = Order.asc when sort equals “asc”, otherwise Order.desc).
  - Value choice on sort equals “asc” — true gives Order.asc, false gives Order.desc.
- Set results from query.run(as\_dict = true).
- For each d in results.
  - Set d.posted\_on from pretty\_date(d.posted\_on).
- Return results.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L2611) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1055) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L6)

<a id="op-7dfee7cddf71b6"></a>
### Get no of pages

`operation_workforce_public_pages_jobs_index_business_behavior_get_number_of_pages`

**Inputs** filters = no value, txt = no value, page\_length = 20.

**Explicit results** math.ceil((result at 0.no\_of\_openings ÷ page\_length)).

**Local steps**

- Set jo from Platform.qb.DocType(“Job Opening”).
- Set query from nested operand in the contract.qb.from\_(jo).select(Count(“\*”).as\_(“no\_of\_openings”)).where((jo.status equals “Open” bitwise and jo.publish equals 1)).
- For each d in filters.
  - Set query from query.where(Platform.qb.Field(d).isin(filters at d)).
- If txt.
  - Set query from query.where((jo.job\_title.like(formatted text %{txt}%) bitwise or jo.description.like(formatted text %{txt}%))).
- Set result from query.run(as\_dict = true).
- Return math.ceil((result at 0.no\_of\_openings ÷ page\_length)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L3533) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1056) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L7)
