# Shared value and file services · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-468719bb5a71b8"></a>
### Now datetime

`operation_foundation_utils_data_business_behavior_now_datetime`

**Inputs** no declared parameters.

**Declared result** datetime.datetime.

**Explicit results** datetime.datetime.now(ZoneInfo(get\_system\_timezone())).replace(tzinfo = no value).

**Local steps**

- Return datetime.datetime.now(ZoneInfo(get\_system\_timezone())).replace(tzinfo = no value).

**Values supplied outside this operation** clock or generated value from datetime.datetime.now(ZoneInfo(get\_system\_timezone())).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3860) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L21)

<a id="op-b0f873a382df80"></a>
### Get timestamp

`operation_foundation_utils_data_business_behavior_get_timestamp`

**Inputs** date = no value.

**Declared result** float.

**Explicit results** time.mktime(getdate(date).timetuple()).

**Local steps**

- Return time.mktime(getdate(date).timetuple()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L3954) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1180) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1739)

<a id="op-a388056b9ab4e1"></a>
### Get eta

`operation_foundation_utils_data_business_behavior_get_eta`

**Inputs** from\_time, percent\_complete.

**Declared result** str.

**Explicit results** str(datetime.timedelta(seconds = (((100 − percent\_complete) ÷ percent\_complete) × diff))).

**Local steps**

- Set diff from time\_diff(now\_datetime(), from\_time).total\_seconds().
- Return str(datetime.timedelta(seconds = (((100 − percent\_complete) ÷ percent\_complete) × diff))).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L4052) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1694)

<a id="op-eadbbe504f3c64"></a>
### Get system timezone

`operation_foundation_utils_data_business_behavior_get_system_timezone`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** (Platform.get\_system\_settings(“time\_zone”) or “Asia/Kolkata”).

**Local steps**

- Return (Platform.get\_system\_settings(“time\_zone”) or “Asia/Kolkata”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“time\_zone”) → “Asia/Kolkata”.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“time\_zone”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L4213) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1732)

<a id="op-ff6663b99e8246"></a>
### Convert utc to timezone

`operation_foundation_utils_data_business_behavior_convert_coordinated_universal_time_to_timezone`

**Inputs** utc\_timestamp, time\_zone.

**Declared result** datetime.datetime.

**Explicit results** utc\_timestamp.astimezone(ZoneInfo(time\_zone)) · utc\_timestamp.

**Local steps**

- If utc\_timestamp.tzinfo is identical to no value.
  - Set utc\_timestamp from utc\_timestamp.replace(tzinfo = ZoneInfo(“UTC”)).
- Attempt the following.
  - Return utc\_timestamp.astimezone(ZoneInfo(time\_zone)).
- On failure (ZoneInfoNotFoundError).
  - Return utc\_timestamp.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L4544) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1098) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1657)

<a id="op-782cbaa533dc0c"></a>
### Get datetime in timezone

`operation_foundation_utils_data_business_behavior_get_datetime_in_timezone`

**Inputs** time\_zone.

**Declared result** datetime.datetime.

**Explicit results** convert\_utc\_to\_timezone(utc\_timestamp, time\_zone).

**Local steps**

- Set utc\_timestamp from datetime.datetime.now(datetime.UTC).
- Return convert\_utc\_to\_timezone(utc\_timestamp, time\_zone).

**Values supplied outside this operation** clock or generated value from datetime.datetime.now(datetime.UTC).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L4726) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1692)

<a id="op-e848f81e8a2a58"></a>
### Convert utc to system timezone

`operation_foundation_utils_data_business_behavior_convert_coordinated_universal_time_to_system_timezone`

**Inputs** utc\_timestamp.

**Declared result** datetime.datetime.

**Explicit results** convert\_utc\_to\_timezone(utc\_timestamp, time\_zone).

**Local steps**

- Set time\_zone from get\_system\_timezone().
- Return convert\_utc\_to\_timezone(utc\_timestamp, time\_zone).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L4827) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1097) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1656)

<a id="op-3076d8ff8e69b9"></a>
### Now

`operation_foundation_utils_data_business_behavior_now`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** ((getdate(nested operand in the contract.flags.current\_date).strftime(DATE\_FORMAT) + one space) + now\_datetime().strftime(TIME\_FORMAT)) · now\_datetime().strftime(DATETIME\_FORMAT).

**Local steps**

- If Platform.flags.current\_date.
  - Return ((getdate(nested operand in the contract.flags.current\_date).strftime(DATE\_FORMAT) + one space) + now\_datetime().strftime(TIME\_FORMAT)).
- Otherwise.
  - Return now\_datetime().strftime(DATETIME\_FORMAT).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L4912) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L20)

<a id="op-d675033d2f7263"></a>
### Nowdate

`operation_foundation_utils_data_business_behavior_current_date`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** now\_datetime().strftime(DATE\_FORMAT).

**Local steps**

- Return now\_datetime().strftime(DATE\_FORMAT).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L5072) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1659)

<a id="op-b2366b6910df05"></a>
### Today

`operation_foundation_utils_data_business_behavior_today`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** nowdate().

**Local steps**

- Return nowdate().

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L5130) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1256) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L56)

<a id="op-1495eea5c90221"></a>
### Get abbr

`operation_foundation_utils_data_business_behavior_get_abbreviation`

**Inputs** string, max\_len = 2.

**Declared result** str.

**Explicit results** (abbr or “?”).

**Local steps**

- Set abbr from empty text.
- For each part in string.split(one space).
  - If (len(abbr) &lt; max\_len and part).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(abbr) &lt; max\_len → part.
    - Update abbr using + part at 0.
- Return (abbr or “?”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in abbr → “?”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L5171) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1687)

<a id="op-a429c6dfd77331"></a>
### Nowtime

`operation_foundation_utils_data_business_behavior_nowtime`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** now\_datetime().strftime(TIME\_FORMAT).

**Local steps**

- Return now\_datetime().strftime(TIME\_FORMAT).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L5349) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1221) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L22)

<a id="op-8de2894dac0496"></a>
### Get first day

`operation_foundation_utils_data_business_behavior_get_first_day`

**Inputs** dt, d\_years = 0, d\_months = 0, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L5407) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1698)

<a id="op-4bb0bbfeb7d553"></a>
### Get first day

`operation_foundation_utils_data_business_behavior_get_first_day_2`

**Inputs** dt, d\_years = 0, d\_months = 0, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L5505) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1699)

<a id="op-7b9756c6989bec"></a>
### Get first day

`operation_foundation_utils_data_business_behavior_get_first_day_3`

**Inputs** dt, d\_years = 0, d\_months = 0, as\_str = false.

**Declared result** (str bitwise or datetime.date).

**Explicit results** datetime.date(year, (month + 1), 1).strftime(DATE\_FORMAT) when as\_str, otherwise datetime.date(year, (month + 1), 1).

**Local steps**

- Set dt from getdate(dt).
- Set tuple(overflow\_years, month) from divmod(((dt.month + d\_months) − 1), 12).
- Set year from ((dt.year + d\_years) + overflow\_years).
- Return datetime.date(year, (month + 1), 1).strftime(DATE\_FORMAT) when as\_str, otherwise datetime.date(year, (month + 1), 1).
  - Value choice on as\_str — true gives datetime.date(year, (month + 1), 1).strftime(DATE\_FORMAT), false gives datetime.date(year, (month + 1), 1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L90) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1700)

<a id="op-f2c0b5ded19cc5"></a>
### Get quarter start

`operation_foundation_utils_data_business_behavior_get_quarter_start`

**Inputs** dt = no value, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L5941) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1720)

<a id="op-5d2752a77410c8"></a>
### Get quarter start

`operation_foundation_utils_data_business_behavior_get_quarter_start_2`

**Inputs** dt = no value, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L6033) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1721)

<a id="op-abbb9a1cb3560e"></a>
### Get quarter start

`operation_foundation_utils_data_business_behavior_get_quarter_start_3`

**Inputs** dt = no value, as\_str = false.

**Declared result** (str bitwise or datetime.date).

**Explicit results** first\_date\_of\_quarter.strftime(DATE\_FORMAT) when as\_str, otherwise first\_date\_of\_quarter.

**Local steps**

- Set date from getdate(dt).
- Set quarter from (((date.month − 1) floor divide 3) + 1).
- Set first\_date\_of\_quarter from datetime.date(date.year, (((quarter − 1) × 3) + 1), 1).
- Return first\_date\_of\_quarter.strftime(DATE\_FORMAT) when as\_str, otherwise first\_date\_of\_quarter.
  - Value choice on as\_str — true gives first\_date\_of\_quarter.strftime(DATE\_FORMAT), false gives first\_date\_of\_quarter.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L94) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1722)

<a id="op-784f082eb58d3c"></a>
### Get first day of week

`operation_foundation_utils_data_business_behavior_get_first_day_of_week`

**Inputs** dt, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L6399) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1701)

<a id="op-4848c8945e0696"></a>
### Get first day of week

`operation_foundation_utils_data_business_behavior_get_first_day_of_week_2`

**Inputs** dt, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** str.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L6480) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1702)

<a id="op-164d89d10ec4e9"></a>
### Get first day of week

`operation_foundation_utils_data_business_behavior_get_first_day_of_week_3`

**Inputs** dt, as\_str = false.

**Declared result** (datetime.date bitwise or str).

**Explicit results** date.strftime(DATE\_FORMAT) when as\_str, otherwise date.

**Local steps**

- Set dt from getdate(dt).
- Set date from (dt − datetime.timedelta(days = get\_week\_start\_offset\_days(dt))).
- Return date.strftime(DATE\_FORMAT) when as\_str, otherwise date.
  - Value choice on as\_str — true gives date.strftime(DATE\_FORMAT), false gives date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L6561) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1703)

<a id="op-fd1a744d9b5364"></a>
### Get week start offset days

`operation_foundation_utils_data_business_behavior_get_week_start_offset_days`

**Inputs** dt.

**Explicit results** (current\_day\_index − start\_of\_week\_index) · (7 − (start\_of\_week\_index − current\_day\_index)).

**Local steps**

- Set current\_day\_index from get\_normalized\_weekday\_index(dt).
- Set start\_of\_week\_index from get\_start\_of\_week\_index().
- If current\_day\_index ≥ start\_of\_week\_index.
  - Return (current\_day\_index − start\_of\_week\_index).
- Otherwise.
  - Return (7 − (start\_of\_week\_index − current\_day\_index)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L98) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1743)

<a id="op-8dcc9ee3ebbedd"></a>
### Get normalized weekday index

`operation_foundation_utils_data_business_behavior_get_normalized_weekday_index`

**Inputs** dt.

**Explicit results** ((dt.weekday() + 1) modulo or format 7).

**Local steps**

- Return ((dt.weekday() + 1) modulo or format 7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L93) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1716)

<a id="op-7277c4beb6182c"></a>
### Get year start

`operation_foundation_utils_data_business_behavior_get_year_start`

**Inputs** dt, as\_str = false.

**Wrappers, in declaration order** typing.overload.

**Declared result** datetime.date.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0472.json#L6978) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1191) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1749)
