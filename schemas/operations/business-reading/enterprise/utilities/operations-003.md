# Supporting services · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Enterprise

<a id="op-ae986e1117668c"></a>
### Allow regional.caller

`operation_enterprise_initialize_business_behavior_allow_regional_caller`

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

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L7243) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L79)

<a id="op-8953b5b535d45d"></a>
### Check app permission

`operation_enterprise_initialize_business_behavior_check_application_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L80)

<a id="op-4a242c34a128f3"></a>
### Normalize ctx input

`operation_enterprise_initialize_business_behavior_normalize_context_input`

**Inputs** T.

**Declared result** callable.

**Explicit results** decorator.

**Local steps**

- Bind local operation decorator for subsequent calls.
- Return decorator.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L90)

<a id="op-db427e77c988bc"></a>
### Normalize ctx input.decorator

`operation_enterprise_initialize_business_behavior_normalize_context_input_decorator`

**Inputs** func.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Evaluate wrapper.\_\_annotations\_\_.update(mapping of k → v for tuple(k, v) drawn from func.\_\_annotations\_\_.items() where k differs from “ctx”).
  - Draw tuple(k, v) from func.\_\_annotations\_\_.items(), keep a combination only if (k differs from “ctx”).
- Return wrapper.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0002.json#L521) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L91)

<a id="op-94a14d4b03d48a"></a>
### Normalize ctx input.decorator.wrapper

`operation_enterprise_initialize_business_behavior_normalize_context_input_decorator_wrapper`

**Inputs** ctx, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(func, assigned = generator of a for a drawn from functools.WRAPPER\_ASSIGNMENTS where a does not belong to tuple(“\_\_annotations\_\_”, “\_\_annotate\_\_”)).

**Explicit results** func(ctx, expanded args, expanded names kwargs).

**Local steps**

- If isinstance(ctx, Document).
  - Set ctx from T(expanded names ctx.as\_dict()).
- Otherwise.
  - If isinstance(ctx, dict).
    - Set ctx from T(expanded names ctx).
  - Otherwise.
    - Set ctx from T(expanded names Platform.parse\_json(ctx)).
- Return func(ctx, expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0002.json#L995) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L92)

<a id="op-8aea05a21a7f42"></a>
### Require party permission

`operation_enterprise_binding_enterprise_init_require_party_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** party\_type, party.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L591)

<a id="op-b542cc32fa7286"></a>
### Is permitted

`operation_enterprise_binding_enterprise_init_is_permitted`

**Inputs** doctype, name, ptype.

**Explicit results** false · Platform.has\_permission(doctype, ptype, doc = name).

**Local steps**

- Set name from cstr(name).
- If not name.
  - Return false.
- Set saved\_messages from Platform.get\_message\_log().
- Evaluate Platform.clear\_messages().
- Attempt the following.
  - Return Platform.has\_permission(doctype, ptype, doc = name).
- On failure (Platform.DoesNotExistError).
  - Return false.
- On exit, including pending return or failure.
  - Set Platform.local.message\_log from saved\_messages.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, ptype, doc = name).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L588)

<a id="op-40d5910428a327"></a>
### Require permission

`operation_enterprise_binding_enterprise_init_require_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name, ptype.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L592)

<a id="op-7534cf1eeeae8f"></a>
### Require user permission

`operation_enterprise_binding_enterprise_init_require_user_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L593)

<a id="op-3e3fce31b614ed"></a>
### Is within user permissions

`operation_enterprise_binding_enterprise_init_is_within_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L589)

<a id="op-ccbbe36dd8d4b0"></a>
### Refuse

`operation_enterprise_binding_enterprise_init_refuse`

**Inputs** no declared parameters.

**Local steps**

- Set Platform.flags.disable\_traceback from true.
- Evaluate Platform.throw\_permission\_error().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L590)

## Service · Filters

<a id="op-238ab0b3355856"></a>
### Get filters config

`operation_enterprise_startup_filters_business_behavior_get_filters_configuration`

**Inputs** no declared parameters.

**Explicit results** filters\_config.

**Local steps**

- Set filters\_config from mapping(“fiscal year” → mapping(“label” → “Fiscal Year”, “get\_field” → “Enterprise.accounts.utils.get\_fiscal\_year\_filter\_field”, “valid\_for\_fieldtypes” → list(“Date”, “Datetime”, “DateRange”), “depends\_on” ….
- Return filters\_config.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L3194) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1144) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L685)

## Service · Help

<a id="op-d0e6354261e3be"></a>
### Get context

`operation_enterprise_templates_pages_help_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “Support Settings” via get\_doc · read “Issue” via get\_list.

**Local steps**

- Set context.no\_cache from 1.
- Set settings from Platform.get\_doc(“Support Settings”, “Support Settings”).
- Set s from settings.
- Set sections from json.loads((s.get\_started\_sections or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in s.get\_started\_sections → “&#91;&#93;”.
- Set context.get\_started\_sections from sections.
- Set tuple(topics\_data, post\_params) from tuple(list(), mapping()).
- If (s.show\_latest\_forum\_posts and s.forum\_url).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in s.show\_latest\_forum\_posts → s.forum\_url.
  - Set tuple(topics\_data, post\_params) from get\_forum\_posts(s).
- Set context.post\_params from post\_params.
- Set context.forum\_url from s.forum\_url.
- Set context.topics from topics\_data at slice no value to 3.
- If Platform.session.user differs from “Guest”.
  - Set context.issues from Platform.get\_list(“Issue”, fields = list(“name”, “status”, “subject”, “modified”)) at slice no value to 3.
- Otherwise.
  - Set context.issues from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1339)

<a id="op-ced562c5a00636"></a>
### Get forum posts

`operation_enterprise_templates_pages_help_business_behavior_get_forum_posts`

**Inputs** s.

**Explicit results** tuple(list(), mapping()) · tuple(topics\_data, post\_params).

**Local steps**

- Attempt the following.
  - Set response from requests.get(((s.forum\_url + “/”) + s.get\_latest\_query), timeout = FORUM\_REQUEST\_TIMEOUT).
  - Evaluate response.raise\_for\_status().
- On failure (requests.RequestException).
  - Return tuple(list(), mapping()).
- Set response\_json from response.json().
- Set topics\_data from mapping().
- Set key\_list from s.response\_key\_list.split(“,”).
- For each key in key\_list.
  - Set topics\_data from response\_json.get(key) when not topics\_data, otherwise topics\_data.get(key).
    - Value choice on not topics\_data — true gives response\_json.get(key), false gives topics\_data.get(key).
- For each topic in topics\_data.
  - Set topic at “link” from ((((s.forum\_url + “/”) + s.post\_route\_string) + “/”) + str(topic.get(s.post\_route\_key))).
- Set post\_params from mapping(“title” → s.post\_title\_key, “description” → s.post\_description\_key).
- Return tuple(topics\_data, post\_params).

**Values supplied outside this operation** service or queued work from requests.get(((s.forum\_url + “/”) + s.get\_latest\_query), timeout = FORUM\_REQUEST\_TIMEOUT).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1340)

## Service · Incoterms

<a id="op-e653e8cc7f7153"></a>
### Extract

`operation_enterprise_gettext_extractors_incoterms_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set file from StringIO(fileobj.read().decode()).
- Set reader from DictReader(file).
- For each tuple(i, row) in enumerate(reader).
  - yield tuple((i + 2), “\_”, row at “title”, list(“Title of an incoterm”)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L6432) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L158) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L71)

## Service · Index

<a id="op-9f4afb334dff5d"></a>
### Get context

`operation_enterprise_public_pages_book_appointment_index_business_behavior_get_context`

**Inputs** context.

**Explicit results** context.

**Local steps**

- Evaluate handle\_appointment\_booking\_disabled().
- Return context.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L3039) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L895)

<a id="op-2d722554370cff"></a>
### Handle appointment booking disabled

`operation_enterprise_public_pages_book_appointment_index_business_behavior_handle_appointment_booking_disabled`

**Inputs** no declared parameters.

**Record and data access** read “Appointment Booking Settings” via get\_single\_value.

**Explicit failure paths** Platform.Redirect.

**Local steps**

- If not Platform.get\_single\_value(“Appointment Booking Settings”, “enable\_appointment\_portal”).
  - Evaluate Platform.redirect\_to\_message(translated “Appointment Scheduling Disabled”, translated “Appointment Scheduling has been disabled for this site”, http\_status\_code = 302, indicator\_color = “red”).
  - Raise Platform.Redirect.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Appointment Booking Settings”, “enable\_appointment\_portal”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L3093) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L898)

<a id="op-61b329926b70d2"></a>
### Get appointment settings

`operation_enterprise_public_pages_book_appointment_index_business_behavior_get_appointment_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** read “Appointment Booking Settings” via get\_single\_value.

**Explicit results** settings.

**Local steps**

- Evaluate handle\_appointment\_booking\_disabled().
- Set settings from Platform.get\_single\_value(“Appointment Booking Settings”, list(“advance\_booking\_days”, “appointment\_duration”, “success\_redirect\_url”), as\_dict = true).
- Return settings.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Appointment Booking Settings”, list(“advance\_booking\_days”, “appointment\_duration”, “success\_redirect\_url”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L3250) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L891)

<a id="op-dc8efc8e478997"></a>
### Get timezones

`operation_enterprise_public_pages_book_appointment_index_business_behavior_get_timezones`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Explicit results** zoneinfo.available\_timezones().

**Local steps**

- Evaluate handle\_appointment\_booking\_disabled().
- Return zoneinfo.available\_timezones().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L3402) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L897)

<a id="op-4cd2de6ec467d6"></a>
### Get appointment slots

`operation_enterprise_public_pages_book_appointment_index_business_behavior_get_appointment_slots`

**Inputs** date, timezone.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true), rate\_limit(limit = SLOT\_REQUESTS\_PER\_MINUTE, seconds = 60).

**Record and data access** read “Appointment Booking Settings” via get\_single\_value · resolve a document from “Holiday List” via get\_doc.

**Explicit results** converted\_timeslots.

**Local steps**

- Evaluate handle\_appointment\_booking\_disabled().
- Evaluate validate\_timezone(timezone).
- Set query\_start\_time from parse\_datetime(date, “00:00:00”).
- Set query\_end\_time from parse\_datetime(date, “23:59:59”).
- Set query\_start\_time from convert\_to\_system\_timezone(timezone, query\_start\_time).
- Set query\_end\_time from convert\_to\_system\_timezone(timezone, query\_end\_time).
- Set now from convert\_to\_guest\_timezone(timezone, Platform.utils.now\_datetime()).
- Set settings from Platform.get\_single\_value(“Appointment Booking Settings”, list(“holiday\_list”, “appointment\_duration”, “number\_of\_agents”, “availability\_of\_slots”), as\_dict = true).
- Set holiday\_list from Platform.get\_doc(“Holiday List”, settings.holiday\_list).
- Set timeslots from get\_available\_slots\_between(query\_start\_time, query\_end\_time, settings).
- Set booked\_times from get\_booked\_slot\_times\_for(timeslots, settings.appointment\_duration).
- Set converted\_timeslots from list().
- For each timeslot in timeslots.
  - Set converted\_timeslot from convert\_to\_guest\_timezone(timezone, timeslot).
  - If \_is\_holiday(timeslot.date(), holiday\_list).
    - Evaluate converted\_timeslots.append(dict(time = converted\_timeslot, availability = false)).
    - Continue with the next iteration or loop test.
  - If (is\_slot\_available(timeslot, booked\_times, settings) and converted\_timeslot ≥ now).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_slot\_available(timeslot, booked\_times, settings) → converted\_timeslot ≥ now.
    - Evaluate converted\_timeslots.append(dict(time = converted\_timeslot, availability = true)).
  - Otherwise.
    - Evaluate converted\_timeslots.append(dict(time = converted\_timeslot, availability = false)).
- Set date\_required from parse\_datetime(date, “00:00:00”).date().
- Set converted\_timeslots from filter\_timeslots(date\_required, converted\_timeslots).
- Return converted\_timeslots.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime() · configured or stored value from Platform.get\_single\_value(“Appointment Booking Settings”, list(“holiday\_list”, “appointment\_duration”, “number\_of\_agents”, “availability\_of\_slots”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L892)

<a id="op-42163c7e5c5c4b"></a>
### Get available slots between

`operation_enterprise_public_pages_book_appointment_index_business_behavior_get_available_slots_between`

**Inputs** query\_start\_time, query\_end\_time, settings.

**Explicit results** timeslots.

**Local steps**

- Set records from \_get\_records(query\_start\_time, query\_end\_time, settings).
- Set timeslots from list().
- Set appointment\_duration from datetime.timedelta(minutes = settings.appointment\_duration).
- For each record in records.
  - If record.day\_of\_week equals WEEKDAYS at query\_start\_time.weekday().
    - Set current\_time from \_deltatime\_to\_datetime(query\_start\_time, record.from\_time).
    - Set end\_time from \_deltatime\_to\_datetime(query\_start\_time, record.to\_time).
  - Otherwise.
    - Set current\_time from \_deltatime\_to\_datetime(query\_end\_time, record.from\_time).
    - Set end\_time from \_deltatime\_to\_datetime(query\_end\_time, record.to\_time).
  - While (current\_time + appointment\_duration) ≤ end\_time.
    - Evaluate timeslots.append(current\_time).
    - Update current\_time using + appointment\_duration.
- Return timeslots.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L4380) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L893)

<a id="op-d7f5b4ea560256"></a>
### Create appointment

`operation_enterprise_public_pages_book_appointment_index_business_behavior_create_appointment`

**Inputs** date, time, tz, contact.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = list(“POST”)), rate\_limit(limit = 5, seconds = 300).

**State and service calls** request new\_doc for “Appointment” · call insert on appointment.

**Explicit results** appointment.

**Local steps**

- Evaluate handle\_appointment\_booking\_disabled().
- Evaluate validate\_timezone(tz).
- Set scheduled\_time from parse\_datetime(date, time).
- Set scheduled\_time from scheduled\_time.replace(tzinfo = no value).
- Set scheduled\_time from convert\_to\_system\_timezone(tz, scheduled\_time).
- Set scheduled\_time from scheduled\_time.replace(tzinfo = no value).
- Set appointment from Platform.new\_doc(“Appointment”).
- Set appointment.scheduled\_time from scheduled\_time.
- Set contact from Platform.parse\_json(contact).
- Set appointment.customer\_name from contact.get(“name”, no value).
- Set appointment.customer\_phone\_number from contact.get(“number”, no value).
- Set appointment.customer\_skype from contact.get(“skype”, no value).
- Set appointment.customer\_details from contact.get(“notes”, no value).
- Set appointment.customer\_email from contact.get(“email”, no value).
- Set appointment.created\_through\_portal from 1.
- Evaluate appointment.insert(ignore\_permissions = true).
- Return appointment.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L887)

<a id="op-73e30caa342dbd"></a>
### Validate timezone

`operation_enterprise_binding_enterprise_www_book_appointment_index_validate_timezone`

**Inputs** timezone.

**Explicit failure paths** validation helper — translated “{0} is not a valid time zone”.format(timezone).

**Local steps**

- Attempt the following.
  - Evaluate zoneinfo.ZoneInfo(timezone).
- On failure (tuple(zoneinfo.ZoneInfoNotFoundError, ValueError)).
  - Call the validation error handler Platform.throw(translated “{0} is not a valid time zone”.format(timezone)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1348)

<a id="op-fcfbb3cfc34252"></a>
### Parse datetime

`operation_enterprise_binding_enterprise_www_book_appointment_index_parse_datetime`

**Inputs** date, time.

**Declared result** datetime.datetime.

**Explicit results** datetime.datetime.strptime(formatted text {date} {time}, “%Y-%m-%d %H:%M:%S”).

**Explicit failure paths** validation helper — translated “{0} {1} is not a valid date and time”.format(date, time).

**Local steps**

- Attempt the following.
  - Return datetime.datetime.strptime(formatted text {date} {time}, “%Y-%m-%d %H:%M:%S”).
- On failure (ValueError).
  - Call the validation error handler Platform.throw(translated “{0} {1} is not a valid date and time”.format(date, time)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L66) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1347)
