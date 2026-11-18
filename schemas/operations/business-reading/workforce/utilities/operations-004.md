# Supporting services · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-79ccc6602f4d3a"></a>
### Get country

`operation_workforce_utils_initialize_business_behavior_get_country`

**Inputs** fields = no value.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Declared result** dict.

**Explicit results** country\_info at ip.

**Local steps**

- Use module bindings country\_info.
- Set ip from Platform.local.request\_ip.
- If ip does not belong to country\_info.
  - Set fields from list(“countryCode”, “country”, “regionName”, “city”).
  - Set res from requests.get(text in the contract.format(ip = ip, key = Platform.conf.get(“ip-api-key”), fields = “,”.join(fields))).
  - Attempt the following.
    - Set country\_info at ip from res.json().
  - On failure (Exception).
    - Set country\_info at ip from mapping().
- Return country\_info at ip.

**Values supplied outside this operation** service or queued work from requests.get(text in the contract.format(ip = ip, key = Platform.conf.get(“ip-api-key”), fields = “,”.join(fields))).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0158.json#L1997) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1233) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L177)

<a id="op-7f1ab5f62cf590"></a>
### Get date range

`operation_workforce_utils_initialize_business_behavior_get_date_range`

**Inputs** start\_date, end\_date.

**Declared result** list at str.

**Explicit results** list of add\_days(start\_date, i) for i drawn from range(no\_of\_days).

**Local steps**

- Set no\_of\_days from (date\_diff(end\_date, start\_date) + 1).
- Return list of add\_days(start\_date, i) for i drawn from range(no\_of\_days).
  - Draw i from range(no\_of\_days).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0158.json#L2355) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1234) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L178)

<a id="op-cce41cb99f7b96"></a>
### Generate date range

`operation_workforce_utils_initialize_business_behavior_generate_date_range`

**Inputs** start\_date, end\_date, reverse = false.

**Declared result** Generator at tuple(str, no value, no value).

**Local steps**

- Set no\_of\_days from (date\_diff(end\_date, start\_date) + 1).
- Set date\_field from end\_date when reverse, otherwise start\_date.
  - Value choice on reverse — true gives end\_date, false gives start\_date.
- Set direction from negative 1 when reverse, otherwise 1.
  - Value choice on reverse — true gives negative 1, false gives 1.
- For each n in range(no\_of\_days).
  - yield add\_days(date\_field, (direction × n)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0158.json#L2510) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1232) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L176)

<a id="op-ad4d8e44ec35c4"></a>
### Get employee email

`operation_workforce_utils_initialize_business_behavior_get_employee_email`

**Inputs** employee\_id.

**Declared result** (str bitwise or no value).

**Record and data access** read “Employee” via get\_value.

**Explicit results** (employee\_emails.prefered\_email or employee\_emails.user\_id or employee\_emails.company\_email or employee\_emails.personal\_email).

**Local steps**

- Set employee\_emails from Platform.db.get\_value(“Employee”, employee\_id, list(“prefered\_email”, “user\_id”, “company\_email”, “personal\_email”), as\_dict = true).
- Return (employee\_emails.prefered\_email or employee\_emails.user\_id or employee\_emails.company\_email or employee\_emails.personal\_email).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in employee\_emails.prefered\_email → employee\_emails.user\_id → employee\_emails.company\_email → employee\_emails.personal\_email.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0158.json#L2747) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1235) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L179)

<a id="op-21de03e5ceaab7"></a>
### Extend bootinfo

`operation_workforce_utils_initialize_business_behavior_extend_bootinfo`

**Inputs** bootinfo.

**Local steps**

- Set bootinfo.hr\_only\_setup from bool(Platform.conf.sk\_Workforce).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0158.json#L2927) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1231) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L175)

## Service · Workforce

<a id="op-817616a8b51b78"></a>
### Refetch resource

`operation_workforce_initialize_business_behavior_refetch_resource`

**Inputs** cache\_key, user = no value.

**State and service calls** publish realtime with “Workforce:refetch\_resource”.

**Local steps**

- Evaluate Platform.publish\_realtime(“Workforce:refetch\_resource”, mapping(“cache\_key” → cache\_key), user = (user or Platform.session.user), after\_commit = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“Workforce:refetch\_resource”, mapping(“cache\_key” → cache\_key), user = (user or Platform.session.user), after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L488) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L181) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L530)

<a id="op-479c947ca2c0f0"></a>
### Get region

`operation_workforce_initialize_business_behavior_get_region`

**Inputs** company = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Company”, company, “country”) · (Platform.flags.country or Platform.get\_system\_settings(“country”)).

**Local steps**

- If not company.
  - Set company from Platform.local.flags.company.
- If company.
  - Return Platform.get\_cached\_value(“Company”, company, “country”).
- Return (Platform.flags.country or Platform.get\_system\_settings(“country”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.country → Platform.get\_system\_settings(“country”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “country”), Platform.get\_system\_settings(“country”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L620) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L180) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L529)

<a id="op-3d9e9d20d232e8"></a>
### Allow regional

`operation_workforce_initialize_business_behavior_allow_regional`

**Inputs** fn.

**Explicit results** caller.

**Local steps**

- Bind local operation caller for subsequent calls.
- Return caller.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L790) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L178) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L527)

<a id="op-e4c22c43ef6411"></a>
### Allow regional.caller

`operation_workforce_initialize_business_behavior_allow_regional_caller`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(fn).

**Explicit results** fn(expanded args, expanded names kwargs) · Platform.get\_attr(overrides at function\_path at negative 1)(expanded args, expanded names kwargs).

**Local steps**

- Set overrides from Platform.get\_hooks(“regional\_overrides”, mapping()).get(get\_region()).
- Set function\_path from formatted text {inspect.getmodule(fn).\_\_name\_\_}.{fn.\_\_name\_\_}.
- If (not overrides or function\_path does not belong to overrides).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not overrides → function\_path does not belong to overrides.
  - Return fn(expanded args, expanded names kwargs).
- Return Platform.get\_attr(overrides at function\_path at negative 1)(expanded args, expanded names kwargs).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“regional\_overrides”, mapping()), Platform.get\_attr(overrides at function\_path at negative 1).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0001.json#L1126) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L179) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L528)

<a id="op-f6e3405f9725e9"></a>
### Get context

`operation_workforce_public_pages_workforce_management_business_behavior_get_context`

**Inputs** context.

**State and service calls** commit.

**Explicit results** context.

**Local steps**

- Set csrf\_token from Platform.sessions.get\_csrf\_token().
- Evaluate Platform.db.commit().
- Set context from Platform.\_dict().
- Set context.csrf\_token from csrf\_token.
- Set context.boot from get\_boot().
- Set context.site\_name from Platform.local.site.
- Return context.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L1600) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1059) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L10)

<a id="op-882abb73862079"></a>
### Get context for dev

`operation_workforce_public_pages_workforce_management_business_behavior_get_context_for_development`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”), allow\_guest = true).

**Explicit results** get\_boot().

**Explicit failure paths** validation helper — Platform.\_(“This method is only meant for developer mode”).

**Local steps**

- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(Platform.\_(“This method is only meant for developer mode”)).
- Return get\_boot().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L1783) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1060) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L11)

<a id="op-441ec3a10bf9cb"></a>
### Get boot

`operation_workforce_public_pages_workforce_management_business_behavior_get_boot`

**Inputs** no declared parameters.

**Explicit results** bootinfo.

**Local steps**

- Set bootinfo from Platform.\_dict(mapping(“site\_name” → Platform.local.site, “socketio\_port” → (Platform.conf.get(“socketio\_port”) or 9000), “push\_relay\_server\_url” → (Platform.conf.get(“push\_relay\_server\_url”) or empty text ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“socketio\_port”) → 9000.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“push\_relay\_server\_url”) → empty text.
- Set bootinfo.lang from Platform.local.lang.
- Set bootinfo.layout\_direction from “rtl” when is\_rtl(), otherwise “ltr”.
  - Value choice on is\_rtl() — true gives “rtl”, false gives “ltr”.
- Evaluate load\_translations(bootinfo).
- Return bootinfo.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L15) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1058) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L9)

<a id="op-ff0f00f995b243"></a>
### Get default route

`operation_workforce_public_pages_workforce_management_business_behavior_get_default_route`

**Inputs** no declared parameters.

**Explicit results** “/Workforce”.

**Local steps**

- Return “/Workforce”.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L2158) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1061) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L12)
