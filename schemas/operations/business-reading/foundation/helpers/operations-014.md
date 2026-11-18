# Shared value and file services · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-c7d1decfda9537"></a>
### Get year start

`operation_foundation_utils_data_business_behavior_get_year_start_2`

**Inputs** dt, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L7059) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1192) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1750)

<a id="op-b2759927ec5a1e"></a>
### Get year start

`operation_foundation_utils_data_business_behavior_get_year_start_3`

**Inputs** dt, as\_str = false.

**Declared result** (str bitwise or datetime.date).

**Explicit results** date.strftime(DATE\_FORMAT) when as\_str, otherwise date.

**Local steps**

- Set dt from getdate(dt).
- Set date from datetime.date(dt.year, 1, 1).
- Return date.strftime(DATE\_FORMAT) when as\_str, otherwise date.
  - Value choice on as\_str — true gives date.strftime(DATE\_FORMAT), false gives date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L7140) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1751)

<a id="op-22dd611dc67341"></a>
### Get last day of week

`operation_foundation_utils_data_business_behavior_get_last_day_of_week`

**Inputs** dt, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L7302) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1710)

<a id="op-90fae1b91c73f1"></a>
### Get last day of week

`operation_foundation_utils_data_business_behavior_get_last_day_of_week_2`

**Inputs** dt, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L7383) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1711)

<a id="op-290de7d52fbfd8"></a>
### Get last day of week

`operation_foundation_utils_data_business_behavior_get_last_day_of_week_3`

**Inputs** dt, as\_str = false.

**Declared result** (datetime.date bitwise or str).

**Explicit results** date.strftime(DATE\_FORMAT) when as\_str, otherwise date.

**Local steps**

- Set dt from get\_first\_day\_of\_week(dt).
- Set date from (dt + datetime.timedelta(days = 6)).
- Return date.strftime(DATE\_FORMAT) when as\_str, otherwise date.
  - Value choice on as\_str — true gives date.strftime(DATE\_FORMAT), false gives date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L7464) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1712)

<a id="op-6b26ddbe68caa9"></a>
### Get last day

`operation_foundation_utils_data_business_behavior_get_last_day`

**Inputs** dt.

**Explicit results** (get\_first\_day(dt, 0, 1) + datetime.timedelta(negative 1)).

**Local steps**

- Return (get\_first\_day(dt, 0, 1) + datetime.timedelta(negative 1)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L7624) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1709)

<a id="op-e180aeca5ff680"></a>
### Is last day of the month

`operation_foundation_utils_data_business_behavior_is_last_day_of_the_month`

**Inputs** dt.

**Explicit results** getdate(dt) equals getdate(last\_day\_of\_the\_month).

**Local steps**

- Set last\_day\_of\_the\_month from get\_last\_day(dt).
- Return getdate(dt) equals getdate(last\_day\_of\_the\_month).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L7)

<a id="op-62e430d4fc0e54"></a>
### Get quarter ending

`operation_foundation_utils_data_business_behavior_get_quarter_ending`

**Inputs** dt = no value, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L110) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1717)

<a id="op-9ab2e4d0086294"></a>
### Get quarter ending

`operation_foundation_utils_data_business_behavior_get_quarter_ending_2`

**Inputs** dt = no value, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L202) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1718)

<a id="op-34702cc33f9965"></a>
### Get quarter ending

`operation_foundation_utils_data_business_behavior_get_quarter_ending_3`

**Inputs** date = no value, as\_str = false.

**Declared result** (str bitwise or datetime.date).

**Explicit results** date.strftime(DATE\_FORMAT) when as\_str, otherwise date.

**Local steps**

- Set date from getdate(date).
- For each month in tuple(3, 6, 9, 12).
  - Set quarter\_end\_month from getdate(formatted text {date.year}-{month}-01).
  - Set quarter\_end\_date from getdate(get\_last\_day(quarter\_end\_month)).
  - If date ≤ quarter\_end\_date.
    - Set date from quarter\_end\_date.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return date.strftime(DATE\_FORMAT) when as\_str, otherwise date.
  - Value choice on as\_str — true gives date.strftime(DATE\_FORMAT), false gives date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L294) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1719)

<a id="op-afde9b67958363"></a>
### Get year ending

`operation_foundation_utils_data_business_behavior_get_year_ending`

**Inputs** dt = no value, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L597) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1746)

<a id="op-e9f309a9b124fc"></a>
### Get year ending

`operation_foundation_utils_data_business_behavior_get_year_ending_2`

**Inputs** dt = no value, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L689) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1189) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1747)

<a id="op-14788576f97c95"></a>
### Get year ending

`operation_foundation_utils_data_business_behavior_get_year_ending_3`

**Inputs** date = no value, as\_str = false.

**Declared result** (datetime.date bitwise or str).

**Explicit results** year\_ending.strftime(DATE\_FORMAT) when as\_str, otherwise year\_ending.

**Local steps**

- Set date from getdate(date).
- Set next\_year\_start from datetime.date((date.year + 1), 1, 1).
- Set year\_ending from add\_to\_date(next\_year\_start, days = negative 1).
- Return year\_ending.strftime(DATE\_FORMAT) when as\_str, otherwise year\_ending.
  - Value choice on as\_str — true gives year\_ending.strftime(DATE\_FORMAT), false gives year\_ending.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L781) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1190) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1748)

<a id="op-3cc8d8622c617a"></a>
### Get time

`operation_foundation_utils_data_business_behavior_get_time`

**Inputs** time\_str.

**Declared result** datetime.time.

**Explicit results** time\_str.time() · time\_str · (datetime.datetime.min + time\_str).time() · datetime.time.fromisoformat(time\_str) · parser.parse(time\_str).time() · 1 additional forms in the steps below.

**Explicit failure paths** e.

**Local steps**

- If isinstance(time\_str, datetime.datetime).
  - Return time\_str.time().
- Otherwise.
  - If isinstance(time\_str, datetime.time).
    - Return time\_str.
  - Otherwise.
    - If isinstance(time\_str, datetime.timedelta).
      - Return (datetime.datetime.min + time\_str).time().
- Attempt the following.
  - Return datetime.time.fromisoformat(time\_str).
- On failure (ValueError).
  - Attempt the following.
    - Return parser.parse(time\_str).time().
  - On failure (ParserError) bound to e.
    - If (“day” belongs to e.args at 1 or “hour must be in” belongs to e.args at 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in “day” belongs to e.args at 1 → “hour must be in” belongs to e.args at 0.
      - Return (datetime.datetime.min + parse\_timedelta(time\_str)).time().
    - Raise e.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L1001) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1176) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1735)

<a id="op-6ffd8de7dd925b"></a>
### Get datetime str

`operation_foundation_utils_data_business_behavior_get_datetime_text`

**Inputs** datetime\_obj.

**Declared result** str.

**Explicit results** datetime\_obj.strftime(DATETIME\_FORMAT).

**Local steps**

- If isinstance(datetime\_obj, str).
  - Set datetime\_obj from get\_datetime(datetime\_obj).
- Return datetime\_obj.strftime(DATETIME\_FORMAT).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L1449) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1693)

<a id="op-487430a47da0b1"></a>
### Get date str

`operation_foundation_utils_data_business_behavior_get_date_text`

**Inputs** date\_obj.

**Declared result** str.

**Explicit results** date\_obj.strftime(DATE\_FORMAT).

**Local steps**

- If isinstance(date\_obj, str).
  - Set date\_obj from get\_datetime(date\_obj).
- Return date\_obj.strftime(DATE\_FORMAT).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L1564) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1690)

<a id="op-ea46862e195a38"></a>
### Get time str

`operation_foundation_utils_data_business_behavior_get_time_text`

**Inputs** timedelta\_obj.

**Declared result** str.

**Explicit results** formatted text {hours}:{minutes}:{seconds}.

**Local steps**

- If isinstance(timedelta\_obj, str).
  - Set timedelta\_obj from to\_timedelta(timedelta\_obj).
- Set tuple(hours, remainder) from divmod(timedelta\_obj.seconds, 3600).
- Set tuple(minutes, seconds) from divmod(remainder, 60).
- Return formatted text {hours}:{minutes}:{seconds}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L1679) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1177) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1736)

<a id="op-fde597b92b5c58"></a>
### Get user date format

`operation_foundation_utils_data_business_behavior_get_user_date_format`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** Platform.local.user\_date\_format.

**Local steps**

- If getattr(Platform.local, “user\_date\_format”, no value) is identical to no value.
  - Set Platform.local.user\_date\_format from get\_date\_format().
- Return Platform.local.user\_date\_format.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “user\_date\_format”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L1909) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1740)

<a id="op-db0087147e66e3"></a>
### Get user time format

`operation_foundation_utils_data_business_behavior_get_user_time_format`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** Platform.local.user\_time\_format.

**Local steps**

- If getattr(Platform.local, “user\_time\_format”, no value) is identical to no value.
  - Set Platform.local.user\_time\_format from get\_time\_format().
- Return Platform.local.user\_time\_format.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “user\_time\_format”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L2024) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1742)

<a id="op-06b435e0671d74"></a>
### Format date

`operation_foundation_utils_data_business_behavior_format_date`

**Inputs** string\_date = no value, format\_string = no value, parse\_day\_first = false.

**Declared result** str.

**Explicit results** empty text · formatted\_date.

**Local steps**

- Bind dependencies babel.dates.
- Bind dependencies UnknownLocaleError.
- If not string\_date.
  - Return empty text.
- Set date from getdate(string\_date, parse\_day\_first).
- If not format\_string.
  - Set format\_string from get\_user\_date\_format().
- Set format\_string from format\_string.replace(“mm”, “MM”).replace(“Y”, “y”).
- Attempt the following.
  - Set formatted\_date from babel.dates.format\_date(date, format\_string, locale = (Platform.local.lang or empty text).replace(“-”, “\_”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → empty text.
- On failure (tuple(UnknownLocaleError, ValueError)).
  - Set format\_string from format\_string.replace(“MM”, “%m”).replace(“dd”, “%d”).replace(“yyyy”, “%Y”).
  - Set formatted\_date from date.strftime(format\_string).
- Return formatted\_date.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L2139) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1680)

<a id="op-97017fa9837205"></a>
### Format time

`operation_foundation_utils_data_business_behavior_format_time`

**Inputs** time\_string = no value, format\_string = no value.

**Declared result** str.

**Explicit results** empty text · formatted\_time.

**Local steps**

- Bind dependencies babel.dates.
- Bind dependencies UnknownLocaleError.
- If not time\_string.
  - Return empty text.
- Set time\_ from get\_time(time\_string).
- If not format\_string.
  - Set format\_string from get\_user\_time\_format().
- Attempt the following.
  - Set formatted\_time from babel.dates.format\_time(time\_, format\_string, locale = (Platform.local.lang or empty text).replace(“-”, “\_”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → empty text.
- On failure (tuple(UnknownLocaleError, ValueError)).
  - Set formatted\_time from time\_.strftime(“%H:%M:%S”).
- Return formatted\_time.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L2595) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1684)

<a id="op-aa814cd9993264"></a>
### Format datetime

`operation_foundation_utils_data_business_behavior_format_datetime`

**Inputs** datetime\_string, format\_string = no value.

**Declared result** str.

**Explicit results** no value · formatted\_datetime.

**Local steps**

- Bind dependencies babel.dates.
- Bind dependencies UnknownLocaleError.
- If not datetime\_string.
  - Return no value.
- Set datetime from get\_datetime(datetime\_string).
- If not format\_string.
  - Set format\_string from ((get\_user\_date\_format().replace(“mm”, “MM”) + one space) + get\_user\_time\_format()).
- Attempt the following.
  - Set formatted\_datetime from babel.dates.format\_datetime(datetime, format\_string, locale = (Platform.local.lang or empty text).replace(“-”, “\_”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → empty text.
- On failure (tuple(UnknownLocaleError, ValueError)).
  - Set formatted\_datetime from datetime.strftime(“%Y-%m-%d %H:%M:%S”).
- Return formatted\_datetime.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L2909) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1681)

<a id="op-b5906642b35bb4"></a>
### Format duration

`operation_foundation_utils_data_business_behavior_format_duration`

**Inputs** seconds, hide\_days = false.

**Declared result** str.

**Explicit results** duration.

**Local steps**

- Set seconds from cint(seconds).
- Set negative from seconds &lt; 0.
- Set seconds from abs(seconds).
- Set days from (seconds floor divide (3600 × 24)) when not hide\_days, otherwise 0.
  - Value choice on not hide\_days — true gives (seconds floor divide (3600 × 24)), false gives 0.
- Set hours from ((seconds modulo or format (3600 × 24)) floor divide 3600) when not hide\_days, otherwise (seconds floor divide 3600).
  - Value choice on not hide\_days — true gives ((seconds modulo or format (3600 × 24)) floor divide 3600), false gives (seconds floor divide 3600).
- Set minutes from ((seconds modulo or format 3600) floor divide 60).
- Set seconds from (seconds modulo or format 60).
- Set total\_duration from list().
- If days.
  - Evaluate total\_duration.append(formatted text {days}d).
- If hours.
  - Evaluate total\_duration.append(formatted text {hours}h).
- If minutes.
  - Evaluate total\_duration.append(formatted text {minutes}m).
- If seconds.
  - Evaluate total\_duration.append(formatted text {seconds}s).
- Set duration from one space.join(total\_duration).
- If (negative and duration).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in negative → duration.
  - Set duration from (“-” + duration).
- Return duration.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L3268) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1682)

<a id="op-7e5caa6a42504a"></a>
### Duration to seconds

`operation_foundation_utils_data_business_behavior_duration_to_seconds`

**Inputs** duration.

**Explicit results** value.

**Local steps**

- Evaluate validate\_duration\_format(duration).
- Set value from 0.
- If “d” belongs to duration.
  - Set val from duration.split(“d”).
  - Set days from val at 0.
  - Update value using + (((cint(days) × 24) × 60) × 60).
  - Set duration from val at 1.
- If “h” belongs to duration.
  - Set val from duration.split(“h”).
  - Set hours from val at 0.
  - Update value using + ((cint(hours) × 60) × 60).
  - Set duration from val at 1.
- If “m” belongs to duration.
  - Set val from duration.split(“m”).
  - Set mins from val at 0.
  - Update value using + (cint(mins) × 60).
  - Set duration from val at 1.
- If “s” belongs to duration.
  - Set val from duration.split(“s”).
  - Set secs from val at 0.
  - Update value using + cint(secs).
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L86) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1108) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1667)
