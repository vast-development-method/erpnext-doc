# Shared value and file services · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-02f3fe6dc4c34d"></a>
### Attach expanded links

`operation_foundation_utils_data_business_behavior_attach_expanded_links`

**Inputs** doctype, docs, fields\_to\_expand.

**Record and data access** read link\_doctype via get\_list.

**Explicit results** no value.

**Local steps**

- If not fields\_to\_expand.
  - Return no value.
- Set meta from Platform.get\_meta(doctype).
- Set link\_fields from mapping of f.fieldname → f for f drawn from (meta.get\_link\_fields() + meta.get\_dynamic\_link\_fields()).
  - Draw f from (meta.get\_link\_fields() + meta.get\_dynamic\_link\_fields()).
- Set doctype\_values from defaultdict(set).
- Set field\_to\_doctype from mapping().
- For each fieldname in fields\_to\_expand.
  - If fieldname does not belong to link\_fields.
    - Continue with the next iteration or loop test.
  - Set e from link\_fields at fieldname.
  - Set link\_doctype from e.options.
  - Set field\_to\_doctype at fieldname from link\_doctype.
  - For each li in docs.
    - Set val from li.get(fieldname).
    - If val.
      - Evaluate doctype\_values at link\_doctype.add(val).
- Set doctype\_title\_maps from mapping().
- For each tuple(link\_doctype, values) in doctype\_values.items().
  - Set records from Platform.get\_list(link\_doctype, filters = mapping(“name” → list(“in”, list(values))), fields = list(“\*”)).
  - Set doctype\_title\_maps at link\_doctype from mapping of r at “name” → r for r drawn from records.
    - Draw r from records.
- For each li in docs.
  - For each fieldname in fields\_to\_expand.
    - If fieldname does not belong to field\_to\_doctype.
      - Continue with the next iteration or loop test.
    - Set link\_doctype from field\_to\_doctype at fieldname.
    - Set val from li.get(fieldname).
    - Set val\_title from doctype\_title\_maps.get(link\_doctype, mapping()).get(val).
    - If (val and val\_title).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in val → val\_title.
      - Set li at fieldname from val\_title.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L1241) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1086) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1645)

## Service · Dateutils

<a id="op-c98d5eeff1f416"></a>
### User to str

`operation_foundation_utils_dateutils_business_behavior_user_to_text`

**Inputs** date, date\_format = no value.

**Explicit results** date · datetime.datetime.strptime(date, dateformats at date\_format).strftime(“%Y-%m-%d”).

**Explicit failure paths** ValueError(formatted text Date {date} must be in format {date\_format}).

**Local steps**

- If not date.
  - Return date.
- If not date\_format.
  - Set date\_format from get\_user\_date\_format().
- Attempt the following.
  - Return datetime.datetime.strptime(date, dateformats at date\_format).strftime(“%Y-%m-%d”).
- On failure (ValueError).
  - Raise ValueError(formatted text Date {date} must be in format {date\_format}).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L2232) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1272) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L71)

<a id="op-d3e1b0fd5bffc8"></a>
### Parse date

`operation_foundation_utils_dateutils_business_behavior_parse_date`

**Inputs** date.

**Explicit results** parsed\_date.

**Explicit failure paths** Exception(formatted text Cannot understand date - '{date}'.  Try formatting it like your default format - '{get\_user\_date\_format()}').

**Local steps**

- Set parsed\_date from no value.
- If one space belongs to date.
  - Set date from date.split(one space, 1) at 0.
- Set check\_formats from list(no value, expanded sorted(list(dateformats), reverse = not nested operand in the contract().startswith(“dd”))).
- For each f in check\_formats.
  - Attempt the following.
    - Set parsed\_date from user\_to\_str(date, f).
    - If parsed\_date.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - On failure (ValueError).
    - Take no action here.
- If not parsed\_date.
  - Raise Exception(formatted text Cannot understand date - '{date}'.  Try formatting it like your default format - '{get\_user\_date\_format()}').
- Return parsed\_date.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L2460) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1271) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L70)

<a id="op-35260d259a589e"></a>
### Get user date format

`operation_foundation_utils_dateutils_business_behavior_get_user_date_format`

**Inputs** no declared parameters.

**Explicit results** Platform.local.user\_date\_format.

**Local steps**

- If getattr(Platform.local, “user\_date\_format”, no value) is identical to no value.
  - Set Platform.local.user\_date\_format from get\_date\_format().
- Return Platform.local.user\_date\_format.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “user\_date\_format”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L2823) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1270) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L69)

<a id="op-88e6475599e85c"></a>
### Datetime in user format

`operation_foundation_utils_dateutils_business_behavior_datetime_in_user_format`

**Inputs** date\_time.

**Explicit results** empty text · ((formatdate(date\_time.date()) + one space) + date\_time.strftime(“%H:%M”)).

**Local steps**

- If not date\_time.
  - Return empty text.
- If isinstance(date\_time, str).
  - Set date\_time from get\_datetime(date\_time).
- Bind dependencies formatdate.
- Return ((formatdate(date\_time.date()) + one space) + date\_time.strftime(“%H:%M”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L2936) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1264) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L63)

<a id="op-fe6cb6570acd89"></a>
### Get dates from timegrain

`operation_foundation_utils_dateutils_business_behavior_get_dates_from_timegrain`

**Inputs** from\_date, to\_date, timegrain = “Daily”.

**Explicit results** dates.

**Local steps**

- Set from\_date from getdate(from\_date).
- Set to\_date from getdate(to\_date).
- Set days, months, years from 0.
- If “Daily” equals timegrain.
  - Set days from 1.
- Otherwise.
  - If “Weekly” equals timegrain.
    - Set days from 7.
  - Otherwise.
    - If “Monthly” equals timegrain.
      - Set months from 1.
    - Otherwise.
      - If “Quarterly” equals timegrain.
        - Set months from 3.
      - Otherwise.
        - If “Yearly” equals timegrain.
          - Set months from 1.
- Set dates from list(get\_period\_ending(from\_date, timegrain)).
- While getdate(dates at negative 1) &lt; getdate(to\_date).
  - If “Weekly” equals timegrain.
    - Set date from get\_last\_day\_of\_week(add\_to\_date(dates at negative 1, years = years, months = months, days = days)).
  - Otherwise.
    - Set date from get\_period\_ending(add\_to\_date(dates at negative 1, years = years, months = months, days = days), timegrain).
  - Evaluate dates.append(date).
- Return dates.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L3114) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1265) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L64)

<a id="op-f68217aa599826"></a>
### Get from date from timespan

`operation_foundation_utils_dateutils_business_behavior_get_from_date_from_timespan`

**Inputs** to\_date, timespan.

**Explicit results** add\_to\_date(to\_date, years = years, months = months, days = days, as\_datetime = true).

**Local steps**

- Set days, months, years from 0.
- If timespan equals “Last Week”.
  - Set days from negative 7.
- If timespan equals “Last Month”.
  - Set months from negative 1.
- Otherwise.
  - If timespan equals “Last Quarter”.
    - Set months from negative 3.
  - Otherwise.
    - If timespan equals “Last Year”.
      - Set years from negative 1.
    - Otherwise.
      - If timespan equals “All Time”.
        - Set years from negative 50.
- Return add\_to\_date(to\_date, years = years, months = months, days = days, as\_datetime = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L3721) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1266) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L65)

<a id="op-f70bd8616ff91b"></a>
### Get period

`operation_foundation_utils_dateutils_business_behavior_get_period`

**Inputs** date, interval = “Monthly”.

**Explicit results** mapping(“Daily” → date.strftime(“%d-%m-%y”), “Weekly” → date.strftime(“%d-%m-%y”), “Monthly” → ((str(months at (nested operand in the contract − nested operand in the contract)) + one space) + str(date.yea ….

**Local steps**

- Set date from getdate(date).
- Set months from list(“Jan”, “Feb”, “Mar”, “Apr”, …).
- Return mapping(“Daily” → date.strftime(“%d-%m-%y”), “Weekly” → date.strftime(“%d-%m-%y”), “Monthly” → ((str(months at (nested operand in the contract − nested operand in the contract)) + one space) + str(date.yea ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L4034) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1267) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L66)

<a id="op-4162986acb316b"></a>
### Get period beginning

`operation_foundation_utils_dateutils_business_behavior_get_period_beginning`

**Inputs** date, timegrain, as\_str = true.

**Explicit results** getdate(mapping(“Daily” → date, “Weekly” → get\_first\_day\_of\_week(date), “Monthly” → get\_first\_day(date), “Quarterly” → get\_quarter\_start(date), …) at timegrain).

**Local steps**

- Return getdate(mapping(“Daily” → date, “Weekly” → get\_first\_day\_of\_week(date), “Monthly” → get\_first\_day(date), “Quarterly” → get\_quarter\_start(date), …) at timegrain).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L4422) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1268) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L67)

<a id="op-5c706f58745bdf"></a>
### Get period ending

`operation_foundation_utils_dateutils_business_behavior_get_period_ending`

**Inputs** date, timegrain.

**Explicit results** getdate(mapping(“Daily” → date, “Weekly” → get\_last\_day\_of\_week(date), “Monthly” → get\_last\_day(date), “Quarterly” → get\_quarter\_ending(date), …) at timegrain).

**Local steps**

- Return getdate(mapping(“Daily” → date, “Weekly” → get\_last\_day\_of\_week(date), “Monthly” → get\_last\_day(date), “Quarterly” → get\_quarter\_ending(date), …) at timegrain).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L4604) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1269) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L68)

## Service · Defaults

<a id="op-3908559d1f5751"></a>
### Get not null defaults

`operation_foundation_utils_defaults_business_behavior_get_not_null_defaults`

**Inputs** column\_type.

**Declared result** (Literal at tuple(empty text, 0) bitwise or no value).

**Explicit results** empty text · 0 · no value.

**Local steps**

- Set column\_type\_map from mapping(“Data” → str, “Text” → str, “Autocomplete” → str, “Attach” → str, …).
- Set data\_type from column\_type\_map.get(column\_type.replace(one space, empty text), str).
- If data\_type is identical to str.
  - Return empty text.
- If data\_type belongs to tuple(int, float).
  - Return 0.
- Return no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L4777) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1273) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L72)

## Service · Diff

<a id="op-247faedee5252d"></a>
### Get version diff

`operation_foundation_utils_diff_business_behavior_get_version_diff`

**Inputs** from\_version, to\_version, fieldname = “script”.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** list(“Values not available for diff”) · list(diff).

**Local steps**

- Set tuple(before, before\_timestamp) from \_get\_value\_from\_version(from\_version, fieldname).
- Set tuple(after, after\_timestamp) from \_get\_value\_from\_version(to\_version, fieldname).
- If not (before and after).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → after.
  - Return list(“Values not available for diff”).
- Set before from before.split(whitespace '\\n').
- Set after from after.split(whitespace '\\n').
- Set diff from unified\_diff(before, after, fromfile = cstr(from\_version), tofile = cstr(to\_version), fromfiledate = before\_timestamp, tofiledate = after\_timestamp).
- Return list(diff).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L5343) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L92)

<a id="op-6b277d53a509c6"></a>
### Get value from version

`operation_foundation_utils_diff_business_behavior_get_value_from_version`

**Inputs** version\_name, fieldname.

**Record and data access** read “Version” via get\_list.

**Explicit results** tuple(field at 2, str(version at 0.modified)) · tuple(no value, no value).

**Local steps**

- Set version from Platform.get\_list(“Version”, fields = list(“data”, “modified”), filters = mapping(“name” → version\_name)).
- If version.
  - Set data from json.loads(version at 0.data).
  - Set changed\_fields from data.get(“changed”, list()).
  - For each field in changed\_fields.
    - If field at 0 equals fieldname.
      - Return tuple(field at 2, str(version at 0.modified)).
- Return tuple(no value, no value).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L5748) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1295) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L91)

<a id="op-324715aeeeaf73"></a>
### Version query

`operation_foundation_utils_diff_business_behavior_version_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Version” via get\_list.

**Explicit results** list of tuple(d.name, pretty\_date(d.modified), d.modified, d.owner) for d drawn from results.

**Local steps**

- Set version\_filters from mapping(“docname” → filters at “docname”, “ref\_doctype” → filters at “ref\_doctype”).
- If fieldname bound to filters.get(“fieldname”).
  - Set version\_filters at “data” from tuple(“LIKE”, formatted text %"{fieldname}"%).
- Set results from Platform.get\_list(“Version”, fields = list(“name”, “modified”, “owner”), filters = version\_filters, limit\_start = start, limit\_page\_length = page\_len, …).
- Return list of tuple(d.name, pretty\_date(d.modified), d.modified, d.owner) for d drawn from results.
  - Draw d from results.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L6087) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L93)

## Service · Doctor

<a id="op-97826d93dcfce6"></a>
### Get workers

`operation_foundation_utils_doctor_business_behavior_get_workers`

**Inputs** no declared parameters.

**Explicit results** Worker.all(connection = get\_redis\_conn()).

**Local steps**

- Return Worker.all(connection = get\_redis\_conn()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0478.json#L6575) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L100)

<a id="op-ac4df5f9e35a2c"></a>
### Purge pending jobs

`operation_foundation_utils_doctor_business_behavior_purge_pending_jobs`

**Inputs** event = no value, site = no value, queue = no value.

**Explicit results** purged\_task\_count.

**Local steps**

- Set purged\_task\_count from 0.
- For each \_queue in get\_queue\_list(queue).
  - Set q from get\_queue(\_queue).
  - For each job in q.jobs.
    - Set queue\_args from get\_queue\_args(job).
    - If (site and event).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in site → event.
      - If (queue\_args.get(“site”) equals site and queue\_args.get(“event”) equals event).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in queue\_args.get(“site”) equals site → queue\_args.get(“event”) equals event.
        - Evaluate job.delete().
        - Update purged\_task\_count using + 1.
    - Otherwise.
      - If site.
        - If queue\_args.get(“site”) equals site.
          - Evaluate job.delete().
          - Update purged\_task\_count using + 1.
      - Otherwise.
        - If event.
          - If queue\_args.get(“event”) equals event.
            - Evaluate job.delete().
            - Update purged\_task\_count using + 1.
        - Otherwise.
          - Update purged\_task\_count using + q.count.
          - Evaluate q.empty().
- Return purged\_task\_count.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L108) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1306) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L102)

<a id="op-e5d3a6288d92c3"></a>
### Get jobs by queue

`operation_foundation_utils_doctor_business_behavior_get_jobs_by_queue`

**Inputs** site = no value.

**Explicit results** tuple(jobs\_per\_queue, job\_count).

**Local steps**

- Set jobs\_per\_queue from defaultdict(list).
- Set job\_count, consolidated\_methods from mapping().
- For each queue in get\_queue\_list().
  - Set q from get\_queue(queue).
  - For each job in q.jobs.
    - Set queue\_args from get\_queue\_args(job).
    - If not site.
      - Evaluate jobs\_per\_queue at queue.append((queue\_args.get(“method”) or job.description)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in queue\_args.get(“method”) → job.description.
    - Otherwise.
      - If queue\_args.get(“site”) equals site.
        - Evaluate jobs\_per\_queue at queue.append((queue\_args.get(“method”) or job.description)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in queue\_args.get(“method”) → job.description.
  - Set consolidated\_methods from mapping().
  - For each method in jobs\_per\_queue at queue.
    - If method does not belong to list(consolidated\_methods).
      - Set consolidated\_methods at method from 1.
    - Otherwise.
      - Update consolidated\_methods at method using + 1.
  - Set job\_count at queue from len(jobs\_per\_queue at queue).
  - Set jobs\_per\_queue at queue from consolidated\_methods.
- Return tuple(jobs\_per\_queue, job\_count).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L106) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1301) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L97)

<a id="op-765a9c36e1cb26"></a>
### Get pending jobs

`operation_foundation_utils_doctor_business_behavior_get_pending_jobs`

**Inputs** site = no value.

**Explicit results** jobs\_per\_queue.

**Local steps**

- Set jobs\_per\_queue from defaultdict(list).
- For each queue in get\_queue\_list().
  - Set q from get\_queue(queue).
  - For each job in q.jobs.
    - Set queue\_args from get\_queue\_args(job).
    - Set method\_kwargs from (queue\_args.get(“kwargs”) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in queue\_args.get(“kwargs”) → empty text.
    - If queue\_args.get(“site”) equals site.
      - Evaluate jobs\_per\_queue at queue.append(“{} {}”.format(queue\_args.get(“method”), method\_kwargs)).
- Return jobs\_per\_queue.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L107) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1302) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L98)

<a id="op-88c4131ed3018e"></a>
### Any job pending

`operation_foundation_utils_doctor_business_behavior_any_job_pending`

**Inputs** site.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- For each queue in get\_queue\_list().
  - Set q from get\_queue(queue).
  - For each job\_id in q.get\_job\_ids().
    - If job\_id.startswith(formatted text {site}\|\|).
      - Return true.
  - For each job\_id in q.started\_job\_registry.get\_job\_ids().
    - If job\_id.startswith(formatted text {site}\|\|).
      - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L105) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L94)

<a id="op-266512b5a63266"></a>
### Check number of workers

`operation_foundation_utils_doctor_business_behavior_check_number_of_workers`

**Inputs** no declared parameters.

**Explicit results** len(get\_workers()).

**Local steps**

- Return len(get\_workers()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L224) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1299) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L95)

<a id="op-8630016cf77db7"></a>
### Get running tasks

`operation_foundation_utils_doctor_business_behavior_get_running_tasks`

**Inputs** no declared parameters.

**Explicit results** worker.get\_current\_job().

**Local steps**

- For each worker in get\_workers().
  - Return worker.get\_current\_job().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L276) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1303) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L99)

<a id="op-1d8f7b682e9b78"></a>
### Doctor

`operation_foundation_utils_doctor_business_behavior_doctor`

**Inputs** site = no value.

**Explicit results** true.

**Local steps**

- Within Platform.init\_site(site).
  - Set workers\_online from check\_number\_of\_workers().
  - Set tuple(jobs\_per\_queue, job\_count) from get\_jobs\_by\_queue(site).
- Evaluate print(“-----Checking scheduler status-----”).
- If site.
  - Set sites from list(site).
- Otherwise.
  - Set sites from Platform.utils.get\_sites().
- For each s in sites.
  - Evaluate Platform.init(s).
  - Evaluate Platform.connect().
  - If is\_scheduler\_disabled().
    - Evaluate print(“Scheduler disabled for”, s).
  - If Platform.local.conf.maintenance\_mode.
    - Evaluate print(“Maintenance mode on for”, s).
  - If Platform.local.conf.pause\_scheduler.
    - Evaluate print(“Scheduler paused for”, s).
  - If is\_scheduler\_inactive().
    - Evaluate print(“Scheduler inactive for”, s).
  - Evaluate Platform.destroy().
- Evaluate print(“Workers online:”, workers\_online).
- Evaluate print(formatted text -----{site} Jobs-----).
- For each queue in get\_queue\_list().
  - If jobs\_per\_queue at queue.
    - Evaluate print(“Queue:”, queue).
    - Evaluate print(“Number of Jobs: ”, job\_count at queue).
    - Evaluate print(“Methods:”).
    - For each tuple(method, count) in jobs\_per\_queue at queue.items().
      - Evaluate print(formatted text {method} : {count}).
    - Evaluate print(“------------”).
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L342) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L96)

<a id="op-cc80bbc87518dd"></a>
### Pending jobs

`operation_foundation_utils_doctor_business_behavior_pending_jobs`

**Inputs** site = no value.

**Local steps**

- Evaluate print(“-----Pending Jobs-----”).
- Set pending\_jobs from get\_pending\_jobs(site).
- For each queue in get\_queue\_list().
  - If pending\_jobs at queue.
    - Evaluate print(formatted text -----Queue :{queue}-----).
    - Evaluate print(whitespace '\\n'.join(pending\_jobs at queue)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L1078) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L101)

## Service · Error

<a id="op-7020377db9a435"></a>
### Is ldap exception

`operation_foundation_utils_error_business_behavior_is_lightweight_directory_access_protocol_exception`

**Inputs** e.

**Explicit results** true · false.

**Local steps**

- For each t in type(e).\_\_mro\_\_.
  - If t.\_\_name\_\_ equals LDAP\_BASE\_EXCEPTION.
    - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L1279) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L107)
