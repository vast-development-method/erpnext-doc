# Shared value and file services · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-852bf8f95000b1"></a>
### Validate duration format

`operation_foundation_utils_data_business_behavior_validate_duration_format`

**Inputs** duration.

**Explicit failure paths** validation helper — Platform.\_(“Value {0} must be in the valid duration format: d h m s”).format(Platform.bold(duration)).

**Local steps**

- If not DURATION\_PATTERN.match(duration).
  - Call the validation error handler Platform.throw(Platform.\_(“Value {0} must be in the valid duration format: d h m s”).format(Platform.bold(duration))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L102) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1260) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L59)

<a id="op-502f335bd59521"></a>
### Get weekdays

`operation_foundation_utils_data_business_behavior_get_weekdays`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list(“Monday”, “Tuesday”, “Wednesday”, “Thursday”, …).

**Local steps**

- Return list(“Monday”, “Tuesday”, “Wednesday”, “Thursday”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L4561) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1745)

<a id="op-774cc52af5c3da"></a>
### Get weekday

`operation_foundation_utils_data_business_behavior_get_weekday`

**Inputs** datetime = no value.

**Declared result** str.

**Explicit results** weekdays at datetime.weekday().

**Local steps**

- If not datetime.
  - Set datetime from now\_datetime().
- If isinstance(datetime, str).
  - Set datetime from get\_datetime(datetime).
- Set weekdays from get\_weekdays().
- Return weekdays at datetime.weekday().

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L4631) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1744)

<a id="op-2e1b3c97f8deb1"></a>
### Get month

`operation_foundation_utils_data_business_behavior_get_month`

**Inputs** datetime = no value.

**Declared result** str.

**Explicit results** calendar.month\_name at datetime.month.

**Local steps**

- If not datetime.
  - Set datetime from now\_datetime().
- If isinstance(datetime, str).
  - Set datetime from get\_datetime(datetime).
- Return calendar.month\_name at datetime.month.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L4817) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1715)

<a id="op-c52bb5750bfb62"></a>
### Get timespan date range

`operation_foundation_utils_data_business_behavior_get_timespan_date_range`

**Inputs** timespan.

**Declared result** (tuple at tuple(datetime.datetime, datetime.datetime) bitwise or no value).

**Explicit results** tuple(add\_to\_date(today, days = negative 7), today) · tuple(add\_to\_date(today, days = negative 14), today) · tuple(add\_to\_date(today, days = negative 30), today) · tuple(add\_to\_date(today, days = negative 90), today) · tuple(get\_first\_day\_of\_week(add\_to\_date(today, days = negative 7)), get\_last\_day\_of\_week(add\_to\_date(today, days = negative 7))) · 20 additional forms in the steps below.

**Local steps**

- Set today from getdate().
- Select the first matching pattern against timespan.
  - Pattern “last 7 days”.
    - Return tuple(add\_to\_date(today, days = negative 7), today).
  - Pattern “last 14 days”.
    - Return tuple(add\_to\_date(today, days = negative 14), today).
  - Pattern “last 30 days”.
    - Return tuple(add\_to\_date(today, days = negative 30), today).
  - Pattern “last 90 days”.
    - Return tuple(add\_to\_date(today, days = negative 90), today).
  - Pattern “last week”.
    - Return tuple(get\_first\_day\_of\_week(add\_to\_date(today, days = negative 7)), get\_last\_day\_of\_week(add\_to\_date(today, days = negative 7))).
  - Pattern “last month”.
    - Return tuple(get\_first\_day(add\_to\_date(today, months = negative 1)), get\_last\_day(add\_to\_date(today, months = negative 1))).
  - Pattern “last quarter”.
    - Return tuple(get\_quarter\_start(add\_to\_date(today, months = negative 3)), get\_quarter\_ending(add\_to\_date(today, months = negative 3))).
  - Pattern “last 6 months”.
    - Return tuple(get\_quarter\_start(add\_to\_date(today, months = negative 6)), get\_quarter\_ending(add\_to\_date(today, months = negative 3))).
  - Pattern “last year”.
    - Return tuple(get\_year\_start(add\_to\_date(today, years = negative 1)), get\_year\_ending(add\_to\_date(today, years = negative 1))).
  - Pattern “yesterday”.
    - Return (tuple(add\_to\_date(today, days = negative 1)) × 2).
  - Pattern “today”.
    - Return tuple(today, today).
  - Pattern “tomorrow”.
    - Return (tuple(add\_to\_date(today, days = 1)) × 2).
  - Pattern “this week”.
    - Return tuple(get\_first\_day\_of\_week(today), get\_last\_day\_of\_week(today)).
  - Pattern “this month”.
    - Return tuple(get\_first\_day(today), get\_last\_day(today)).
  - Pattern “this quarter”.
    - Return tuple(get\_quarter\_start(today), get\_quarter\_ending(today)).
  - Pattern “this year”.
    - Return tuple(get\_year\_start(today), get\_year\_ending(today)).
  - Pattern “next 7 days”.
    - Return tuple(today, add\_to\_date(today, days = 7)).
  - Pattern “next 14 days”.
    - Return tuple(today, add\_to\_date(today, days = 14)).
  - Pattern “next 30 days”.
    - Return tuple(today, add\_to\_date(today, days = 30)).
  - Pattern “next week”.
    - Return tuple(get\_first\_day\_of\_week(add\_to\_date(today, days = 7)), get\_last\_day\_of\_week(add\_to\_date(today, days = 7))).
  - Pattern “next month”.
    - Return tuple(get\_first\_day(add\_to\_date(today, months = 1)), get\_last\_day(add\_to\_date(today, months = 1))).
  - Pattern “next quarter”.
    - Return tuple(get\_quarter\_start(add\_to\_date(today, months = 3)), get\_quarter\_ending(add\_to\_date(today, months = 3))).
  - Pattern “next 6 months”.
    - Return tuple(get\_quarter\_start(add\_to\_date(today, months = 3)), get\_quarter\_ending(add\_to\_date(today, months = 6))).
  - Pattern “next year”.
    - Return tuple(get\_year\_start(add\_to\_date(today, years = 1)), get\_year\_ending(add\_to\_date(today, years = 1))).
  - Pattern any value.
    - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L4978) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1738)

<a id="op-70bcda7a2cbdef"></a>
### Global date format

`operation_foundation_utils_data_business_behavior_global_date_format`

**Inputs** date, format = “long”.

**Declared result** str.

**Explicit results** babel.dates.format\_date(date, locale = (Platform.local.lang or “en”).replace(“-”, “\_”), format = format).

**Local steps**

- Bind dependencies babel.dates.
- Set date from getdate(date).
- Return babel.dates.format\_date(date, locale = (Platform.local.lang or “en”).replace(“-”, “\_”), format = format).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.lang → “en”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L6836) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1753)

<a id="op-d0c6b1a416e2e1"></a>
### Has common

`operation_foundation_utils_data_business_behavior_has_common`

**Inputs** l1, l2.

**Declared result** bool.

**Explicit results** (set(l1) bitwise and set(l2)).

**Local steps**

- Return (set(l1) bitwise and set(l2)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L7007) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1757)

<a id="op-dcf5f3bae88e76"></a>
### Cast fieldtype

`operation_foundation_utils_data_business_behavior_cast_fieldtype`

**Inputs** fieldtype, value, show\_warning = true.

**Explicit results** value.

**Local steps**

- If show\_warning.
  - Bind dependencies secho.
  - Set message from “Function ′Platform.utils.data.cast\_fieldtype′ has been deprecated in favour of ′Platform.utils.data.cast′. U …”.
  - Evaluate secho(message, fg = “yellow”).
- If fieldtype belongs to tuple(“Currency”, “Float”, “Percent”).
  - Set value from flt(value).
- Otherwise.
  - If fieldtype belongs to tuple(“Int”, “Check”).
    - Set value from cint(value).
  - Otherwise.
    - If fieldtype belongs to tuple(“Data”, “Text”, “Small Text”, “Long Text”, …).
      - Set value from cstr(value).
    - Otherwise.
      - If fieldtype equals “Date”.
        - Set value from getdate(value).
      - Otherwise.
        - If fieldtype equals “Datetime”.
          - Set value from get\_datetime(value).
        - Otherwise.
          - If fieldtype equals “Time”.
            - Set value from to\_timedelta(value).
- Return value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0473.json#L7095) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1091) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1650)

<a id="op-8c8db94fe1b5d4"></a>
### Cast

`operation_foundation_utils_data_business_behavior_cast`

**Inputs** fieldtype, value = no value.

**Explicit results** value.

**Local steps**

- If fieldtype belongs to tuple(“Currency”, “Float”, “Percent”).
  - Set value from flt(value).
- Otherwise.
  - If fieldtype belongs to tuple(“Int”, “Check”).
    - Set value from cint(sbool(value)).
  - Otherwise.
    - If fieldtype belongs to tuple(“Data”, “Text”, “Small Text”, “Long Text”, …).
      - Set value from cstr(value).
    - Otherwise.
      - If fieldtype equals “Date”.
        - If value.
          - Set value from getdate(value).
        - Otherwise.
          - Set value from datetime.datetime(1, 1, 1).date().
      - Otherwise.
        - If fieldtype equals “Datetime”.
          - If value.
            - Set value from get\_datetime(value).
          - Otherwise.
            - Set value from datetime.datetime(1, 1, 1).
        - Otherwise.
          - If fieldtype equals “Time”.
            - Set value from get\_timedelta(value).
- Return value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1090) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1649)

<a id="op-4ffb98cdce4795"></a>
### Flt

`operation_foundation_utils_data_business_behavior_decimal_number`

**Inputs** s, precision.

**Wrappers, in declaration order** typing.overload.

**Declared result** int.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L537) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1663)

<a id="op-9cd226d23a8255"></a>
### Flt

`operation_foundation_utils_data_business_behavior_decimal_number_2`

**Inputs** s, precision = no value.

**Wrappers, in declaration order** typing.overload.

**Declared result** float.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L624) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1664)

<a id="op-3d0456f3f2bf72"></a>
### Flt

`operation_foundation_utils_data_business_behavior_decimal_number_3`

**Inputs** s.

**Wrappers, in declaration order** typing.overload.

**Declared result** Literal at 0.0.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L709) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1665)

<a id="op-210474f45e1ab0"></a>
### Flt

`operation_foundation_utils_data_business_behavior_decimal_number_4`

**Inputs** s, precision = no value, rounding\_method = no value.

**Declared result** float.

**Explicit results** 0.0 · num.

**Explicit failure paths** propagate active failure.

**Local steps**

- If s is identical to no value.
  - Return 0.0.
- If isinstance(s, str).
  - Set s from s.replace(“,”, empty text).
- Attempt the following.
  - Set num from float(s).
  - If precision is distinct from no value.
    - Set num from rounded(num, precision, rounding\_method).
- On failure (Exception) bound to e.
  - If isinstance(e, Platform.InvalidRoundingMethod).
    - Propagate the active failure.
  - Set num from 0.0.
- Return num.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L772) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1107) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1666)

<a id="op-88ec03a2002554"></a>
### Cint

`operation_foundation_utils_data_business_behavior_integer_number`

**Inputs** s, default = 0.

**Declared result** int.

**Explicit results** default · int(s) · int(float(s)).

**Local steps**

- If s is identical to no value.
  - Return default.
- Attempt the following.
  - Return int(s).
- On failure (Exception).
  - Attempt the following.
    - Return int(float(s)).
  - On failure (Exception).
    - Return default.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L1123) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L3)

<a id="op-25ac5b55fe8d9c"></a>
### Floor

`operation_foundation_utils_data_business_behavior_floor`

**Inputs** s.

**Declared result** int.

**Explicit results** num.

**Local steps**

- Attempt the following.
  - Set num from cint(math.floor(flt(s))).
- On failure (Exception).
  - Set num from 0.
- Return num.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L1319) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1679)

<a id="op-6c2b00d3892d18"></a>
### Ceil

`operation_foundation_utils_data_business_behavior_ceil`

**Inputs** s.

**Declared result** int.

**Explicit results** num.

**Local steps**

- Attempt the following.
  - Set num from cint(math.ceil(flt(s))).
- On failure (Exception).
  - Set num from 0.
- Return num.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L1463) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1092) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1651)

<a id="op-ed6ed4f5487443"></a>
### Cstr

`operation_foundation_utils_data_business_behavior_text_value`

**Inputs** s, encoding = “utf-8”.

**Declared result** str.

**Explicit results** Platform.as\_unicode(s, encoding).

**Local steps**

- Return Platform.as\_unicode(s, encoding).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L1607) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1250) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L50)

<a id="op-cd2ee3e063e105"></a>
### Sbool

`operation_foundation_utils_data_business_behavior_sbool`

**Inputs** x.

**Declared result** ((bool bitwise or str) bitwise or Any).

**Explicit results** true · false · x.

**Local steps**

- Attempt the following.
  - Set val from x.lower().
  - If val belongs to tuple(“true”, “1”).
    - Return true.
  - Otherwise.
    - If val belongs to tuple(“false”, “0”).
      - Return false.
  - Return x.
- On failure (Exception).
  - Return x.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L1680) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L45)

<a id="op-b20f99ea267b50"></a>
### Rounded

`operation_foundation_utils_data_business_behavior_rounded`

**Inputs** num, precision = 0, rounding\_method = no value.

**Explicit results** \_bankers\_rounding(num, precision) · \_bankers\_rounding\_legacy(num, precision) · \_round\_away\_from\_zero(num, precision).

**Explicit failure paths** validation helper with Platform.InvalidRoundingMethod — Platform.\_(“Unknown Rounding Method: {}”).format(rounding\_method).

**Local steps**

- Set precision from cint(precision).
- Set rounding\_method from (rounding\_method or Platform.get\_system\_settings(“rounding\_method”) or “Banker's Rounding (legacy)”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rounding\_method → Platform.get\_system\_settings(“rounding\_method”) → “Banker's Rounding (legacy)”.
- If rounding\_method equals “Banker's Rounding”.
  - Return \_bankers\_rounding(num, precision).
- Otherwise.
  - If rounding\_method equals “Banker's Rounding (legacy)”.
    - Return \_bankers\_rounding\_legacy(num, precision).
  - Otherwise.
    - If rounding\_method equals “Commercial Rounding”.
      - Return \_round\_away\_from\_zero(num, precision).
    - Otherwise.
      - Call the validation error handler Platform.throw(Platform.\_(“Unknown Rounding Method: {}”).format(rounding\_method), exc = Platform.InvalidRoundingMethod).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“rounding\_method”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L1883) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L38)

<a id="op-24bb5880d0a818"></a>
### Bankers rounding legacy

`operation_foundation_utils_data_business_behavior_bankers_rounding_legacy`

**Inputs** num, precision.

**Explicit results** (num ÷ multiplier) when precision, otherwise num.

**Local steps**

- Set multiplier from (10 to the power precision).
- Set num from round((num × multiplier) when precision, otherwise num, 8).
  - Value choice on precision — true gives (num × multiplier), false gives num.
- Set floor\_num from math.floor(num).
- Set decimal\_part from (num − floor\_num).
- If (not precision and decimal\_part equals 0.5).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not precision → decimal\_part equals 0.5.
  - Set num from floor\_num when (floor\_num modulo or format 2) equals 0, otherwise (floor\_num + 1).
    - Value choice on (floor\_num modulo or format 2) equals 0 — true gives floor\_num, false gives (floor\_num + 1).
- Otherwise.
  - If decimal\_part equals 0.5.
    - Set num from (floor\_num + 1).
  - Otherwise.
    - Set num from round(num).
- Return (num ÷ multiplier) when precision, otherwise num.
  - Value choice on precision — true gives (num ÷ multiplier), false gives num.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L2229) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1088) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1647)

<a id="op-ad33fa870cb425"></a>
### Round away from zero

`operation_foundation_utils_data_business_behavior_round_away_from_zero`

**Inputs** num, precision.

**Explicit results** 0.0 · float(Decimal(num).quantize(Decimal(1).scaleb(negative precision))) · round((num + math.copysign(epsilon, num)), precision).

**Local steps**

- If num equals 0.
  - Return 0.0.
- Set epsilon from math.ulp(abs(num)).
- Set rounding\_step from (10.0 to the power negative precision).
- If (math.isfinite(num) and epsilon ≥ (rounding\_step ÷ 4)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in math.isfinite(num) → epsilon ≥ (rounding\_step ÷ 4).
  - Within localcontext() bound as ctx.
    - Set ctx.prec from MAX\_PREC.
    - Set ctx.rounding from ROUND\_HALF\_UP.
    - Return float(Decimal(num).quantize(Decimal(1).scaleb(negative precision))).
- Return round((num + math.copysign(epsilon, num)), precision).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L2569) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L36)

<a id="op-d6fd9e34d46946"></a>
### Bankers rounding

`operation_foundation_utils_data_business_behavior_bankers_rounding`

**Inputs** num, precision.

**Explicit results** 0.0 · ((sign × num) ÷ multiplier).

**Local steps**

- If num equals 0.
  - Return 0.0.
- Set sign from negative 1 when num &lt; 0, otherwise 1.
  - Value choice on num &lt; 0 — true gives negative 1, false gives 1.
- Set multiplier from (10 to the power precision).
- Set num from round((abs(num) × multiplier), 12).
- If num equals 0.
  - Return 0.0.
- Set floor\_num from math.floor(num).
- Set decimal\_part from (num − floor\_num).
- Set epsilon from (2.0 to the power (math.log(num, 2) − 52.0)).
- If (epsilon &lt; 0.5 and abs((decimal\_part − 0.5)) &lt; epsilon).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in epsilon &lt; 0.5 → abs((decimal\_part − 0.5)) &lt; epsilon.
  - Set num from floor\_num when (floor\_num modulo or format 2) equals 0, otherwise (floor\_num + 1).
    - Value choice on (floor\_num modulo or format 2) equals 0 — true gives floor\_num, false gives (floor\_num + 1).
- Otherwise.
  - Set num from round(num).
- Return ((sign × num) ÷ multiplier).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L2946) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1087) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1646)

<a id="op-9f008df83b23cb"></a>
### Remainder

`operation_foundation_utils_data_business_behavior_remainder`

**Inputs** numerator, denominator, precision = 2.

**Declared result** NumericType.

**Explicit results** flt(\_remainder, precision).

**Local steps**

- Set precision from cint(precision).
- Set multiplier from (10 to the power precision).
- If precision.
  - Set \_remainder from (((numerator × multiplier) modulo or format (denominator × multiplier)) ÷ multiplier).
- Otherwise.
  - Set \_remainder from (numerator modulo or format denominator).
- Return flt(\_remainder, precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L3414) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L34)

<a id="op-8634428504058e"></a>
### Safe div

`operation_foundation_utils_data_business_behavior_safe_div`

**Inputs** numerator, denominator, precision = 2.

**Declared result** float.

**Explicit results** flt(\_res, precision).

**Local steps**

- Set precision from cint(precision).
- If denominator equals 0.
  - Set \_res from 0.0.
- Otherwise.
  - Set \_res from (float(numerator) ÷ denominator).
- Return flt(\_res, precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0474.json#L3629) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L40)
