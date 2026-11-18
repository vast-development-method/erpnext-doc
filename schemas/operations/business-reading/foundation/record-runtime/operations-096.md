# Record lifecycle and persistence · operations 96

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · System settings

[Record definition](../../../../data/record-types/system_settings.json)

<a id="op-769c65ff10aafc"></a>
### Disable duckdb cron job

`operation_foundation_core_record_definitions_system_settings_business_behavior_disable_duckdb_schedule_job`

**Inputs** no declared parameters.

**Record and data access** read “Scheduler Event” via get\_all.

**State and service calls** request delete on “Scheduled Job Type” · request delete on “Scheduler Event”.

**Local steps**

- If event bound to Platform.db.get\_all(“Scheduler Event”, mapping(“scheduled\_against” → “DuckDB Sync”), pluck = “name”).
  - Set event from event at 0.
  - Evaluate Platform.db.delete(“Scheduled Job Type”, mapping(“scheduler\_event” → event)).
  - Evaluate Platform.db.delete(“Scheduler Event”, event).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L1693) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L615)

<a id="op-d45810b8edf587"></a>
### Enable duckdb cron job

`operation_foundation_core_record_definitions_system_settings_business_behavior_enable_duckdb_schedule_job`

**Inputs** frequency = “Weekly”.

**Record and data access** resolve a document from mapping(“doctype” → “Scheduler Event”, “scheduled\_against” → “DuckDB Sync”, “method” → method) via get\_doc · resolve a document from mapping(“doctype” → “Scheduled Job Type”, “frequency” → “Cron”, “scheduler\_event” → event.name, “cron\_format” → cron\_format, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Scheduler Event”, “scheduled\_against” → “DuckDB Sync”, “method” → method)) · call insert on Platform.get\_doc(mapping(“doctype” → “Scheduled Job Type”, “frequency” → “Cron”, “scheduler\_event” → event.name, “cron\_format” → cron\_format, …)).

**Local steps**

- Set cron\_format from “0 0 \* \* \*” when frequency equals “Daily”, otherwise “0 0 \* \* 0”.
  - Value choice on frequency equals “Daily” — true gives “0 0 \* \* \*”, false gives “0 0 \* \* 0”.
- Set method from “Platform.database.duckdb.database.start\_duckdb\_sync”.
- Set event from Platform.get\_doc(mapping(“doctype” → “Scheduler Event”, “scheduled\_against” → “DuckDB Sync”, “method” → method)).insert().
- Evaluate Platform.get\_doc(mapping(“doctype” → “Scheduled Job Type”, “frequency” → “Cron”, “scheduler\_event” → event.name, “cron\_format” → cron\_format, …)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L39) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L616)

<a id="op-26bd1f1c0c4082"></a>
### Snapshot report scheduler

`operation_foundation_core_record_definitions_system_settings_business_behavior_snapshot_report_scheduler`

**Inputs** enable = false, frequency = “Weekly”.

**Local steps**

- Evaluate disable\_duckdb\_cron\_job().
- If enable.
  - Evaluate enable\_duckdb\_cron\_job(frequency).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L41) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L619)

## Service · Terms

<a id="op-7fb1855fbc1955"></a>
### Named Parameter Wrapper.initialize

`operation_foundation_query_builder_terms_business_behavior_named_parameter_wrapper_initialize`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.parameters from mapping().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L1224) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L174)

<a id="op-84cde23eb97cff"></a>
### Named Parameter Wrapper.get sql

`operation_foundation_query_builder_terms_business_behavior_named_parameter_wrapper_get_database_query`

**Inputs** self, param\_value, remaining named values kwargs.

**Declared result** str.

**Explicit results** param\_key.

**Local steps**

- Set param\_key from formatted text %(param{(len(self.parameters) + 1)})s.
- Set self.parameters at param\_key at slice 2 to negative 2 from param\_value.
- Return param\_key.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L99) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L172)

<a id="op-850daf5ea9ebe7"></a>
### Named Parameter Wrapper.get parameters

`operation_foundation_query_builder_terms_business_behavior_named_parameter_wrapper_get_parameters`

**Inputs** self.

**Declared result** dict at tuple(str, Any).

**Explicit results** self.parameters.

**Local steps**

- Return self.parameters.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L1479) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L173)

<a id="op-6e5f0e42754dc8"></a>
### Escaped Value Wrapper.get sql

`operation_foundation_binding_foundation_query_builder_terms_escapedvaluewrapper_get_sql`

**Inputs** self, param\_value, remaining named values kwargs.

**Declared result** str.

**Explicit results** Platform.db.escape(param\_value, percent = false).

**Local steps**

- Return Platform.db.escape(param\_value, percent = false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1690)

<a id="op-567efc7ea489f6"></a>
### Parameterized Value Wrapper.get sql

`operation_foundation_query_builder_terms_business_behavior_parameterized_value_wrapper_get_database_query`

**Inputs** self, quote\_char = no value, secondary\_quote\_char = “'”, param\_wrapper = no value, remaining named values kwargs.

**Declared result** str.

**Explicit results** format\_alias\_sql(sql, self.alias, quote\_char = quote\_char, expanded names kwargs).

**Local steps**

- If (param\_wrapper and isinstance(self.value, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in param\_wrapper → isinstance(self.value, str).
  - Set value\_sql from self.get\_value\_sql(quote\_char = quote\_char, expanded names kwargs).
  - Set sql from param\_wrapper.get\_sql(param\_value = value\_sql, expanded names kwargs).
- Otherwise.
  - If isinstance(self.value, timedelta).
    - Set self.value from format\_timedelta(self.value).
  - Otherwise.
    - If isinstance(self.value, time).
      - Set self.value from format\_time(self.value).
    - Otherwise.
      - If isinstance(self.value, datetime).
        - Set self.value from Platform.db.format\_datetime(self.value).
  - Set sql from self.get\_value\_sql(quote\_char = quote\_char, secondary\_quote\_char = secondary\_quote\_char, param\_wrapper = param\_wrapper, expanded names kwargs).
- Return format\_alias\_sql(sql, self.alias, quote\_char = quote\_char, expanded names kwargs).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L100) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L176)

<a id="op-08df8eba924456"></a>
### Parameterized Function.get sql

`operation_foundation_query_builder_terms_business_behavior_parameterized_function_get_database_query`

**Inputs** self, remaining named values kwargs.

**Declared result** str.

**Explicit results** format\_alias\_sql(function\_sql, self.alias, quote\_char = quote\_char, expanded names kwargs) · function\_sql.

**Local steps**

- Set with\_alias from kwargs.pop(“with\_alias”, false).
- Set with\_namespace from kwargs.pop(“with\_namespace”, false).
- Set quote\_char from kwargs.pop(“quote\_char”, no value).
- Set dialect from kwargs.pop(“dialect”, no value).
- Set param\_wrapper from kwargs.pop(“param\_wrapper”, no value).
- Set function\_sql from self.get\_function\_sql(with\_namespace = with\_namespace, quote\_char = quote\_char, param\_wrapper = param\_wrapper, dialect = dialect).
- If self.schema is distinct from no value.
  - Set function\_sql from “{schema}.{function}”.format(schema = self.schema.get\_sql(quote\_char = quote\_char, dialect = dialect, expanded names kwargs), function = function\_sql).
- If with\_alias.
  - Return format\_alias\_sql(function\_sql, self.alias, quote\_char = quote\_char, expanded names kwargs).
- Return function\_sql.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L2142) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L175)

<a id="op-193fa3f96eb689"></a>
### Sub Query.initialize

`operation_foundation_query_builder_terms_business_behavior_subordinate_query_initialize`

**Inputs** self, subq, alias = no value.

**Declared result** no value.

**Local steps**

- Evaluate super().\_\_init\_\_(alias).
- Set self.subq from subq.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L2571) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L178)

<a id="op-5aaae60e020fc3"></a>
### Sub Query.get sql

`operation_foundation_query_builder_terms_business_behavior_subordinate_query_get_database_query`

**Inputs** self, remaining named values kwg.

**Declared result** str.

**Explicit results** self.subq.get\_sql(expanded names kwg).

**Local steps**

- Set kwg at “subquery” from true.
- Return self.subq.get\_sql(expanded names kwg).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L2684) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L177)

## Service · Trace

<a id="op-28b378088e5584"></a>
### Traced Value.initialize

`operation_foundation_model_trace_business_behavior_traced_value_initialize`

**Inputs** self, field\_name, forbidden\_values = no value, custom\_validation = no value.

**Local steps**

- Set self.field\_name from field\_name.
- Set self.forbidden\_values from (forbidden\_values or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in forbidden\_values → list().
- Set self.custom\_validation from custom\_validation.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L5919) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1306)

<a id="op-9e49398a207b0f"></a>
### Traced Value.get

`operation_foundation_model_trace_business_behavior_traced_value_get`

**Inputs** self, obj, objtype = no value.

**Explicit results** self · getattr(obj, formatted text \_{self.field\_name}, no value).

**Local steps**

- If obj is identical to no value.
  - Return self.
- Return getattr(obj, formatted text \_{self.field\_name}, no value).

**Values supplied outside this operation** selected callable from getattr(obj, formatted text \_{self.field\_name}, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L6037) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1305)

<a id="op-003cb335c6ef0a"></a>
### Traced Value.set

`operation_foundation_model_trace_business_behavior_traced_value_set`

**Inputs** self, obj, value.

**Explicit failure paths** validation helper with AssertionError — formatted text {self.field\_name} cannot be set to {value} · validation helper — formatted text {self.field\_name} cannot be set to {value} · validation helper with AssertionError — str(e) · validation helper — str(e).

**Local steps**

- If value belongs to self.forbidden\_values.
  - If Platform.in\_test.
    - Call the validation error handler Platform.throw(formatted text {self.field\_name} cannot be set to {value}, AssertionError).
  - Otherwise.
    - Call the validation error handler Platform.throw(formatted text {self.field\_name} cannot be set to {value}).
- If self.custom\_validation.
  - Attempt the following.
    - Evaluate self.custom\_validation(obj, value).
  - On failure (Exception) bound to e.
    - If Platform.in\_test.
      - Call the validation error handler Platform.throw(str(e), AssertionError).
    - Otherwise.
      - Call the validation error handler Platform.throw(str(e)).
- Evaluate setattr(obj, formatted text \_{self.field\_name}, value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L6159) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1307)

<a id="op-1d50a98e24a5c4"></a>
### Traced Document.initialize

`operation_foundation_model_trace_business_behavior_traced_document_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- For each tuple(name, attr) in self.\_\_class\_\_.\_\_dict\_\_.items().
  - If isinstance(attr, TracedValue).
    - Evaluate setattr(self, formatted text \_{name}, getattr(self, name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L6559) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1303)

<a id="op-a951d2cfd25e83"></a>
### Traced Document.get valid dict

`operation_foundation_model_trace_business_behavior_traced_document_get_valid_mapping`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** d.

**Local steps**

- Set d from super().get\_valid\_dict(expanded args, expanded names kwargs).
- For each tuple(name, attr) in self.\_\_class\_\_.\_\_dict\_\_.items().
  - If isinstance(attr, TracedValue).
    - Set d at name from getattr(self, name).
- Return d.

**Values supplied outside this operation** selected callable from getattr(self, name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L6770) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1302)

<a id="op-54a1f52089858c"></a>
### Traced field

`operation_foundation_model_trace_business_behavior_traced_field`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** TracedValue(expanded args, expanded names kwargs).

**Local steps**

- Return TracedValue(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L6971) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1304)

## Record · Translation

[Record definition](../../../../data/record-types/translation.json)

<a id="op-ce3ab3b5b158cb"></a>
### Translation.validate

`operation_foundation_core_record_definitions_translation_business_behavior_translation_validate`

**Inputs** self.

**Local steps**

- Set self.translated\_text from sanitize\_html(self.translated\_text).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L5041) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L633)

<a id="op-f42c92e814b53a"></a>
### Translation.on update

`operation_foundation_core_record_definitions_translation_business_behavior_translation_on_update`

**Inputs** self.

**Local steps**

- Evaluate clear\_user\_translation\_cache(self.language).
- If (self.has\_value\_changed(“language”) and doc\_before\_save bound to self.get\_doc\_before\_save()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_value\_changed(“language”) → doc\_before\_save bound to self.get\_doc\_before\_save().
  - Evaluate clear\_user\_translation\_cache(doc\_before\_save.language).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L5107) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L632)

<a id="op-555b7aaf84a0e1"></a>
### Translation.on trash

`operation_foundation_core_record_definitions_translation_business_behavior_translation_on_trash`

**Inputs** self.

**Local steps**

- Evaluate clear\_user\_translation\_cache(self.language).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L5247) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L631)

<a id="op-797b7afcb6b060"></a>
### Clear user translation cache

`operation_foundation_core_record_definitions_translation_business_behavior_clear_user_translation_cache`

**Inputs** lang.

**Local steps**

- Evaluate Platform.cache.hdel(USER\_TRANSLATION\_KEY, lang).
- Evaluate Platform.cache.hdel(MERGED\_TRANSLATION\_KEY, lang).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L43) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L630)

## Record · User

[Record definition](../../../../data/record-types/user.json)

<a id="op-27e422d488f33d"></a>
### User.active sessions

`operation_foundation_core_record_definitions_user_business_behavior_user_active_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L50) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L678)

<a id="op-7d1db3e2924f88"></a>
### User.active sessions.mask

`operation_foundation_core_record_definitions_user_business_behavior_user_active_sessions_mask`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** sid\_hash.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L51) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L679)

<a id="op-0cf7ccca85901f"></a>
### User.setup

`operation_foundation_core_record_definitions_user_business_behavior_user_setup`

**Inputs** self.

**Local steps**

- Set self.flags.ignore\_save\_passwords from list(“new\_password”).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L1846) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L722)
