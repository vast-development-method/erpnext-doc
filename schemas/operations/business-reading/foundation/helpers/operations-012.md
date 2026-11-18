# Shared value and file services · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Dashboard

<a id="op-7f7db6a20cc192"></a>
### Generate and cache results

`operation_foundation_utils_dashboard_business_behavior_generate_and_cache_results`

**Inputs** args, function, cache\_key, chart.

**State and service calls** request set\_value on “Dashboard Chart”.

**Explicit results** no value · results.

**Explicit failure paths** validation helper — translated “Please check the filter values set for Dashboard Chart: {}”.format(get\_link\_to\_form(chart.doctype, chart.name)) · propagate active failure.

**Local steps**

- Attempt the following.
  - Set args from Platform.\_dict(args).
  - Set results from function(chart\_name = args.chart\_name, filters = (args.filters or no value), from\_date = (args.from\_date or no value), to\_date = (args.to\_date or no value), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.filters → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.from\_date → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.to\_date → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.time\_interval → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.timespan → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.heatmap\_year → no value.
- On failure (TypeError) bound to e.
  - If str(e) equals “'NoneType' object is not iterable”.
    - Call the validation error handler Platform.throw(translated “Please check the filter values set for Dashboard Chart: {}”.format(get\_link\_to\_form(chart.doctype, chart.name)), title = translated “Invalid Filter Value”).
    - Return no value.
  - Otherwise.
    - Propagate the active failure.
- If not Platform.flags.read\_only.
  - Within suppress(Platform.QueryDeadlockError).
    - Evaluate Platform.db.set\_value(“Dashboard Chart”, args.chart\_name, “last\_synced\_on”, Platform.utils.now(), update\_modified = false).
- Return results.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L5930) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1071) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1630)

<a id="op-eeb0b44c877ec5"></a>
### Get dashboards with link

`operation_foundation_utils_dashboard_business_behavior_get_dashboards_with_link`

**Inputs** docname, doctype.

**Record and data access** read “Dashboard Chart Link” via get\_all · read “Number Card Link” via get\_all.

**Explicit results** list of link.parent for link drawn from links.

**Local steps**

- Set links from list().
- If doctype equals “Dashboard Chart”.
  - Set links from Platform.get\_all(“Dashboard Chart Link”, fields = list(“parent”), filters = mapping(“chart” → docname)).
- Otherwise.
  - If doctype equals “Number Card”.
    - Set links from Platform.get\_all(“Number Card Link”, fields = list(“parent”), filters = mapping(“card” → docname)).
- Return list of link.parent for link drawn from links.
  - Draw link from links.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L6499) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1072) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1631)

<a id="op-69527e20b592c8"></a>
### Sync dashboards

`operation_foundation_utils_dashboard_business_behavior_sync_dashboards`

**Inputs** app = no value.

**Local steps**

- Set apps from list(app) when app, otherwise Platform.get\_installed\_apps().
  - Value choice on app — true gives list(app), false gives Platform.get\_installed\_apps().
- For each app\_name in apps.
  - Attempt the following.
    - Evaluate print(formatted text Updating Dashboard for {app\_name}).
  - On failure (BrokenPipeError).
    - Take no action here.
  - For each module\_name in (Platform.local.app\_modules.get(app\_name) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.app\_modules.get(app\_name) → list().
    - Set Platform.flags.in\_import from true.
    - Evaluate make\_records\_in\_module(app\_name, module\_name).
    - Set Platform.flags.in\_import from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L6799) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1075) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1634)

<a id="op-575f2e5dc225e0"></a>
### Make records in module

`operation_foundation_utils_dashboard_business_behavior_make_records_in_module`

**Inputs** app, module.

**Local steps**

- Set dashboards\_path from Platform.get\_module\_path(module, formatted text {module}\_dashboard).
- Set charts\_path from Platform.get\_module\_path(module, “dashboard chart”).
- Set cards\_path from Platform.get\_module\_path(module, “number card”).
- Set paths from list(dashboards\_path, charts\_path, cards\_path).
- For each path in paths.
  - Evaluate make\_records(path).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L7063) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1074) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1633)

<a id="op-93afd36c03d3c0"></a>
### Make records

`operation_foundation_utils_dashboard_business_behavior_make_records`

**Inputs** path, filters = no value.

**Local steps**

- If os.path.isdir(path).
  - For each fname in os.listdir(path).
    - If os.path.isdir(join(path, fname)).
      - If fname equals “\_\_pycache\_\_”.
        - Continue with the next iteration or loop test.
      - Evaluate import\_file\_by\_path(formatted text {path}/{fname}/{fname}.json).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1073) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1632)

## Service · Data

<a id="op-0e9273cdc3cd32"></a>
### Get start of week index

`operation_foundation_utils_data_business_behavior_get_start_of_week_index`

**Inputs** no declared parameters.

**Declared result** int.

**Explicit results** Weekday at get\_first\_day\_of\_the\_week().value.

**Local steps**

- Return Weekday at get\_first\_day\_of\_the\_week().value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L246) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1730)

<a id="op-c0ea9df0725de1"></a>
### Is invalid date string

`operation_foundation_utils_data_business_behavior_is_invalid_date_string`

**Inputs** date\_string.

**Declared result** bool.

**Explicit results** (not isinstance(date\_string, str) or (not date\_string or (date\_string or empty text).startswith(tuple(“0001-01-01”, “0000-00-00”)))).

**Local steps**

- Return (not isinstance(date\_string, str) or (not date\_string or (date\_string or empty text).startswith(tuple(“0001-01-01”, “0000-00-00”)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(date\_string, str) → (not date\_string or (date\_string or empty text).startswith(tuple(“0001-01-01”, “0000-00-00”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not date\_string → (date\_string or empty text).startswith(tuple(“0001-01-01”, “0000-00-00”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in date\_string → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L298) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L6)

<a id="op-8424c81673bfd0"></a>
### Getdate

`operation_foundation_utils_data_business_behavior_get_date`

**Inputs** string\_date = no value, parse\_day\_first = false.

**Declared result** (datetime.date bitwise or no value).

**Explicit results** get\_datetime().date() · string\_date.date() · string\_date · no value · datetime.date.fromisoformat(string\_date) · 1 additional forms in the steps below.

**Explicit failure paths** validation helper — Platform.\_(“{} is not a valid date string.”).format(Platform.bold(string\_date)).

**Local steps**

- If not string\_date.
  - Return get\_datetime().date().
- Otherwise.
  - If isinstance(string\_date, datetime.datetime).
    - Return string\_date.date().
  - Otherwise.
    - If isinstance(string\_date, datetime.date).
      - Return string\_date.
    - Otherwise.
      - If is\_invalid\_date\_string(string\_date).
        - Return no value.
- Attempt the following.
  - Return datetime.date.fromisoformat(string\_date).
- On failure (ValueError).
  - Attempt the following.
    - Return parser.parse(string\_date, dayfirst = parse\_day\_first).date().
  - On failure (ParserError).
    - Call the validation error handler Platform.throw(Platform.\_(“{} is not a valid date string.”).format(Platform.bold(string\_date)), title = Platform.\_(“Invalid Date”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L422) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1689)

<a id="op-a8570deba3e6be"></a>
### Get datetime

`operation_foundation_utils_data_business_behavior_get_datetime`

**Inputs** datetime\_str = no value.

**Declared result** (datetime.datetime bitwise or no value).

**Explicit results** now\_datetime() · datetime\_str · datetime.datetime(datetime\_str) · datetime.datetime.combine(datetime\_str, datetime.time()) · no value · 2 additional forms in the steps below.

**Local steps**

- If datetime\_str is identical to no value.
  - Return now\_datetime().
- Otherwise.
  - If isinstance(datetime\_str, (datetime.datetime bitwise or datetime.timedelta)).
    - Return datetime\_str.
  - Otherwise.
    - If isinstance(datetime\_str, (list bitwise or tuple)).
      - Return datetime.datetime(datetime\_str).
    - Otherwise.
      - If isinstance(datetime\_str, datetime.date).
        - Return datetime.datetime.combine(datetime\_str, datetime.time()).
      - Otherwise.
        - If is\_invalid\_date\_string(datetime\_str).
          - Return no value.
- Attempt the following.
  - Return datetime.datetime.fromisoformat(datetime\_str).
- On failure (ValueError).
  - Return parser.parse(datetime\_str).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L869) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1691)

<a id="op-f9761290f2a6e4"></a>
### Get timedelta

`operation_foundation_utils_data_business_behavior_get_timedelta`

**Inputs** time = no value.

**Declared result** (datetime.timedelta bitwise or no value).

**Explicit results** time · parse\_timedelta(time) · datetime.timedelta(hours = t.hour, minutes = t.minute, seconds = t.second, microseconds = t.microsecond) · no value.

**Explicit failure paths** e.

**Local steps**

- If isinstance(time, datetime.timedelta).
  - Return time.
- Set time from (time or “0:0:0”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in time → “0:0:0”.
- Attempt the following.
  - Attempt the following.
    - Set t from parser.parse(time).
  - On failure (ParserError) bound to e.
    - If (“day” belongs to e.args at 1 or “hour must be in” belongs to e.args at 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in “day” belongs to e.args at 1 → “hour must be in” belongs to e.args at 0.
      - Return parse\_timedelta(time).
    - Raise e.
  - Return datetime.timedelta(hours = t.hour, minutes = t.minute, seconds = t.second, microseconds = t.microsecond).
- On failure (Exception).
  - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L1264) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1178) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1737)

<a id="op-aee267b49a3691"></a>
### To timedelta

`operation_foundation_utils_data_business_behavior_to_timedelta`

**Inputs** time\_str.

**Declared result** datetime.timedelta.

**Explicit results** datetime.timedelta(hours = t.hour, minutes = t.minute, seconds = t.second, microseconds = t.microsecond) · time\_str.

**Local steps**

- If isinstance(time\_str, datetime.time).
  - Set time\_str from str(time\_str).
- If isinstance(time\_str, str).
  - Set t from parser.parse(time\_str).
  - Return datetime.timedelta(hours = t.hour, minutes = t.minute, seconds = t.second, microseconds = t.microsecond).
- Otherwise.
  - Return time\_str.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L1642) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1255) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L55)

<a id="op-1d5895f9a6d514"></a>
### Add to date

`operation_foundation_utils_data_business_behavior_add_to_date`

**Inputs** date, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as\_string = false, as\_datetime = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L1878) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1078) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1637)

<a id="op-c631e34dae8160"></a>
### Add to date

`operation_foundation_utils_data_business_behavior_add_to_date_2`

**Inputs** date, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as\_string = false, as\_datetime = true.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.datetime.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L2060) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1079) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1638)

<a id="op-e473455f648350"></a>
### Add to date

`operation_foundation_utils_data_business_behavior_add_to_date_3`

**Inputs** date, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as\_string = true, as\_datetime = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L2242) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1080) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1639)

<a id="op-d0108fc06fb967"></a>
### Add to date

`operation_foundation_utils_data_business_behavior_add_to_date_4`

**Inputs** date = no value, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as\_string = false, as\_datetime = false.

**Declared result** DateTimeLikeObject.

**Explicit results** date.strftime(DATETIME\_FORMAT) · date.strftime(DATE\_FORMAT) · date.

**Explicit failure paths** validation helper — Platform.\_(“Please select a valid date filter”).

**Local steps**

- If date is identical to no value.
  - Set date from now\_datetime().
- If hours.
  - Set as\_datetime from true.
- If isinstance(date, str).
  - Set as\_string from true.
  - If one space belongs to date.
    - Set as\_datetime from true.
  - Attempt the following.
    - Set date from get\_datetime(date).
  - On failure (ParserError).
    - Call the validation error handler Platform.throw(Platform.\_(“Please select a valid date filter”), title = Platform.\_(“Invalid Date”)).
- Set date from (date + relativedelta(years = years, months = months, weeks = weeks, days = days, …)).
- If as\_string.
  - If as\_datetime.
    - Return date.strftime(DATETIME\_FORMAT).
  - Otherwise.
    - Return date.strftime(DATE\_FORMAT).
- Otherwise.
  - Return date.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L2411) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1081) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1640)

<a id="op-84b8740055d53d"></a>
### Add days

`operation_foundation_utils_data_business_behavior_add_days`

**Inputs** date, days.

**Declared result** DateTimeLikeObject.

**Explicit results** add\_to\_date(date, days = days).

**Local steps**

- Return add\_to\_date(date, days = days).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L2984) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1076) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1635)

<a id="op-2d48727bc3e3c2"></a>
### Add months

`operation_foundation_utils_data_business_behavior_add_months`

**Inputs** date, months.

**Declared result** DateTimeLikeObject.

**Explicit results** add\_to\_date(date, months = months).

**Local steps**

- Return add\_to\_date(date, months = months).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3063) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1077) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1636)

<a id="op-76183a0b2f3f11"></a>
### Add years

`operation_foundation_utils_data_business_behavior_add_years`

**Inputs** date, years.

**Declared result** DateTimeLikeObject.

**Explicit results** add\_to\_date(date, years = years).

**Local steps**

- Return add\_to\_date(date, years = years).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3142) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1084) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1643)

<a id="op-2799cb58ddce09"></a>
### Date diff

`operation_foundation_utils_data_business_behavior_date_diff`

**Inputs** string\_ed\_date, string\_st\_date.

**Declared result** int.

**Explicit results** days\_diff(string\_ed\_date, string\_st\_date).

**Local steps**

- Return days\_diff(string\_ed\_date, string\_st\_date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3221) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1661)

<a id="op-f78ba46abbf115"></a>
### Days diff

`operation_foundation_utils_data_business_behavior_days_diff`

**Inputs** string\_ed\_date, string\_st\_date.

**Declared result** int.

**Explicit results** (getdate(string\_ed\_date) − getdate(string\_st\_date)).days.

**Local steps**

- Return (getdate(string\_ed\_date) − getdate(string\_st\_date)).days.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3296) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1662)

<a id="op-2321e3fa7491eb"></a>
### Month diff

`operation_foundation_utils_data_business_behavior_month_diff`

**Inputs** string\_ed\_date, string\_st\_date.

**Declared result** int.

**Explicit results** (((((ed\_date.year − st\_date.year) × 12) + ed\_date.month) − st\_date.month) + 1).

**Local steps**

- Set ed\_date from getdate(string\_ed\_date).
- Set st\_date from getdate(string\_st\_date).
- Return (((((ed\_date.year − st\_date.year) × 12) + ed\_date.month) − st\_date.month) + 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3392) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L18)

<a id="op-ad05cc8bf0b45c"></a>
### Time diff

`operation_foundation_utils_data_business_behavior_time_diff`

**Inputs** string\_ed\_date, string\_st\_date.

**Declared result** datetime.timedelta.

**Explicit results** (get\_datetime(string\_ed\_date) − get\_datetime(string\_st\_date)).

**Local steps**

- Return (get\_datetime(string\_ed\_date) − get\_datetime(string\_st\_date)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3558) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1251) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L51)

<a id="op-ca3140e81dd912"></a>
### Time diff in seconds

`operation_foundation_utils_data_business_behavior_time_diff_in_seconds`

**Inputs** string\_ed\_date, string\_st\_date.

**Declared result** float.

**Explicit results** time\_diff(string\_ed\_date, string\_st\_date).total\_seconds().

**Local steps**

- Return time\_diff(string\_ed\_date, string\_st\_date).total\_seconds().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3650) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1253) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L53)

<a id="op-5a756bcbf9ccca"></a>
### Time diff in hours

`operation_foundation_utils_data_business_behavior_time_diff_in_hours`

**Inputs** string\_ed\_date, string\_st\_date.

**Declared result** float.

**Explicit results** round((float(time\_diff(string\_ed\_date, string\_st\_date).total\_seconds()) ÷ 3600), 6).

**Local steps**

- Return round((float(time\_diff(string\_ed\_date, string\_st\_date).total\_seconds()) ÷ 3600), 6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3737) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1252) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L52)
