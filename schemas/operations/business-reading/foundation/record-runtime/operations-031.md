# Record lifecycle and persistence · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Db query

<a id="op-2e4e1aa2b857a8"></a>
### Database Query.selects own name

`operation_foundation_binding_foundation_model_db_query_databasequery_selects_own_name`

**Inputs** self.

**Declared result** bool.

**Explicit results** any(generator of nested operand in the contract(nested operand in the contract, nested operand in the contract, maxsplit = nested operand in the contract, flags = nested operand in the contract) at 0.strip() b …).

**Local steps**

- Set table from formatted text ′tab{self.doctype}′.
- Set own from set(“\*”, “name”, “′name′”, formatted text {table}.\*, …).
- Return any(generator of nested operand in the contract(nested operand in the contract, nested operand in the contract, maxsplit = nested operand in the contract, flags = nested operand in the contract) at 0.strip() b …).
  - Draw f from self.fields.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L123) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1555)

<a id="op-0618935113e597"></a>
### Database Query.update user settings

`operation_foundation_model_persistent_records_query_business_behavior_database_query_update_user_settings`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.save\_user\_settings\_fields and not getattr(self, “user\_settings”, no value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.save\_user\_settings\_fields → not getattr(self, “user\_settings”, no value).
  - Return no value.
- Set user\_settings from json.loads(get\_user\_settings(self.doctype)).
- If hasattr(self, “user\_settings”).
  - Evaluate user\_settings.update(self.user\_settings).
- If self.save\_user\_settings\_fields.
  - Set user\_settings at “fields” from self.user\_settings\_fields.
- Evaluate update\_user\_settings(self.doctype, user\_settings).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “user\_settings”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L4167) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1248)

<a id="op-dce6c5e1040af5"></a>
### Cast name

`operation_foundation_model_persistent_records_query_business_behavior_cast_name`

**Inputs** column.

**Declared result** str.

**Explicit results** column · LOCATE\_CAST\_PATTERN.sub(“locate(\\1, cast(\\2 as varchar))”, expanded names kwargs) · re.sub(formatted text {func}\\(\\s\*(&#91;′\\"&#93;?name&#91;′\\"&#93;?)\\s\*,, formatted text {func}(cast(\\1 as varchar),, expanded names kwargs) · CAST\_VARCHAR\_PATTERN.sub(“cast(\\1 as varchar)”, expanded names kwargs).

**Local steps**

- If Platform.db.db\_type differs from “postgres”.
  - Return column.
- Set kwargs from mapping(“string” → column).
- If (“cast(” does not belong to column.lower() and “::” does not belong to column).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “cast(” does not belong to column.lower() → “::” does not belong to column.
  - If LOCATE\_PATTERN.search(expanded names kwargs).
    - Return LOCATE\_CAST\_PATTERN.sub(“locate(\\1, cast(\\2 as varchar))”, expanded names kwargs).
  - Otherwise.
    - If match bound to FUNC\_IFNULL\_PATTERN.search(expanded names kwargs).
      - Set func from match.groups() at 0.
      - Return re.sub(formatted text {func}\\(\\s\*(&#91;′\\"&#93;?name&#91;′\\"&#93;?)\\s\*,, formatted text {func}(cast(\\1 as varchar),, expanded names kwargs).
  - Return CAST\_VARCHAR\_PATTERN.sub(“cast(\\1 as varchar)”, expanded names kwargs).
- Return column.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L4428) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L613) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1208)

<a id="op-75f0b144f56fd5"></a>
### Get order by

`operation_foundation_model_persistent_records_query_business_behavior_get_order_by`

**Inputs** doctype, meta.

**Explicit results** order\_by.

**Local steps**

- Set order\_by from empty text.
- Set sort\_field, sort\_order from no value.
- If (meta.sort\_field and “,” belongs to meta.sort\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.sort\_field → “,” belongs to meta.sort\_field.
  - Set order\_by from “, ”.join(generator of formatted text {f\_split at 0.strip()} {f\_split at 1.strip()} for f drawn from meta.sort\_field.split(“,”) where f\_split bound to f.split(maxsplit = 2)).
    - Draw f from meta.sort\_field.split(“,”), keep a combination only if (f\_split bound to f.split(maxsplit = 2)).
- Otherwise.
  - Set sort\_field from (meta.sort\_field or “creation”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.sort\_field → “creation”.
  - Set sort\_order from ((meta.sort\_field and meta.sort\_order) or “desc”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (meta.sort\_field and meta.sort\_order) → “desc”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.sort\_field → meta.sort\_order.
  - Set order\_by from formatted text {sort\_field} {sort\_order}.
- Return order\_by.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L4821) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1253)

<a id="op-175ae04b86ae6e"></a>
### Has any user permission for doctype

`operation_foundation_model_persistent_records_query_business_behavior_has_any_user_permission_for_record_type`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, user, applicable\_for.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L5211) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1254)

<a id="op-4a930a3678b08c"></a>
### Get between date filter

`operation_foundation_model_persistent_records_query_business_behavior_get_between_date_filter`

**Inputs** value, df = no value.

**Explicit results** cond.

**Local steps**

- Set fieldtype from ((df and df.fieldtype) or “Datetime”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (df and df.fieldtype) → “Datetime”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype.
- Set from\_date from Platform.utils.nowdate().
- Set to\_date from Platform.utils.nowdate().
- If (value and isinstance(value, (list bitwise or tuple))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → isinstance(value, (list bitwise or tuple)).
  - If len(value) ≥ 1.
    - Set from\_date from value at 0.
  - If len(value) ≥ 2.
    - Set to\_date from value at 1.
- If fieldtype equals “Datetime”.
  - Set from\_date from convert\_type\_for\_between\_filters(from\_date, set\_time = datetime.time()).
  - Set to\_date from convert\_type\_for\_between\_filters(to\_date, set\_time = datetime.time(23, 59, 59, 999999)).
- If fieldtype equals “Datetime”.
  - Set cond from formatted text '{Platform.db.format\_datetime(from\_date)}' AND '{Platform.db.format\_datetime(to\_date)}'.
- Otherwise.
  - Set cond from formatted text '{Platform.db.format\_date(from\_date)}' AND '{Platform.db.format\_date(to\_date)}'.
- Return cond.

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L5400) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1251)

<a id="op-4d19d8718e3626"></a>
### Get additional filter field

`operation_foundation_model_persistent_records_query_business_behavior_get_additional_filter_field`

**Inputs** additional\_filters\_config, f, value.

**Explicit results** f.

**Local steps**

- Set additional\_filter from additional\_filters\_config at f.operator.lower().
- Set f from Platform.\_dict(Platform.get\_attr(additional\_filter at “get\_field”)()).
- If f.query\_value.
  - For each option in f.options.
    - Set option from Platform.\_dict(option).
    - If option.value equals value.
      - Set f.value from option.query\_value.
- Return f.

**Values supplied outside this operation** selected callable from Platform.get\_attr(additional\_filter at “get\_field”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L6024) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1250)

<a id="op-09ef529efe8d5a"></a>
### Get date range

`operation_foundation_model_persistent_records_query_business_behavior_get_date_range`

**Inputs** operator, value.

**Explicit results** get\_timespan\_date\_range(timespan).

**Local steps**

- Set timespan\_map from mapping(“1 week” → “week”, “1 month” → “month”, “3 months” → “quarter”, “6 months” → “6 months”, …).
- Set period\_map from mapping(“previous” → “last”, “next” → “next”).
- If operator differs from “timespan”.
  - Set timespan from formatted text {period\_map at operator} {timespan\_map at value}.
- Otherwise.
  - Set timespan from value.
- Return get\_timespan\_date\_range(timespan).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L6278) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1252)

<a id="op-cb1a34d75aec10"></a>
### Requires owner constraint

`operation_foundation_model_persistent_records_query_business_behavior_requires_owner_constraint`

**Inputs** role\_permissions.

**Explicit results** no value · true.

**Local steps**

- If not role\_permissions.get(“has\_if\_owner\_enabled”).
  - Return no value.
- Set if\_owner\_perms from role\_permissions.get(“if\_owner”).
- If not if\_owner\_perms.
  - Return no value.
- For each perm\_type in tuple(“select”, “read”).
  - If (role\_permissions.get(perm\_type) and perm\_type does not belong to if\_owner\_perms).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in role\_permissions.get(perm\_type) → perm\_type does not belong to if\_owner\_perms.
    - Return no value.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L6557) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1258)

<a id="op-42c6d621d1e5ff"></a>
### Wrap grave quotes

`operation_foundation_model_persistent_records_query_business_behavior_wrap_grave_quotes`

**Inputs** table.

**Declared result** str.

**Explicit results** table.

**Local steps**

- If table at 0 differs from “′”.
  - Set table from formatted text ′{table}′.
- Return table.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L6771) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1260)

<a id="op-313d6ca5979544"></a>
### Is plain field

`operation_foundation_model_persistent_records_query_business_behavior_is_plain_field`

**Inputs** field.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- For each char in field.
  - If char belongs to SPECIAL\_FIELD\_CHARS.
    - Return false.
- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L6877) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1256)

<a id="op-ee46cd9b625dac"></a>
### In function

`operation_foundation_model_persistent_records_query_business_behavior_in_function`

**Inputs** substr, field.

**Declared result** bool.

**Explicit results** (substr belongs to field and field.index(“(”) &lt; field.index(substr) &lt; field.index(“)”)) · false.

**Local steps**

- Attempt the following.
  - Return (substr belongs to field and field.index(“(”) &lt; field.index(substr) &lt; field.index(“)”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in substr belongs to field → field.index(“(”) &lt; field.index(substr) &lt; field.index(“)”).
    - Compare adjacent operands in order, stopping at the first false comparison in field.index(“(”) &lt; field.index(substr) &lt; field.index(“)”).
- On failure (ValueError).
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L6965) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1255)

<a id="op-4af3bec7af47aa"></a>
### Strip alias

`operation_foundation_model_persistent_records_query_business_behavior_strip_alias`

**Inputs** field.

**Declared result** str.

**Explicit results** field.split(“ as ”, 1) at 0 · field.

**Local steps**

- If “ as ” belongs to field.lower().
  - Return field.split(“ as ”, 1) at 0.
- Return field.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0273.json#L7136) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1259)

## Service · Defaults

<a id="op-f5e4975e91c05a"></a>
### Set user default

`operation_foundation_defaults_business_behavior_set_user_default`

**Inputs** key, value, user = no value, parenttype = no value.

**Local steps**

- Evaluate set\_default(key, value, (user or Platform.session.user), parenttype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L778) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1562)

<a id="op-cfa08c273325aa"></a>
### Add user default

`operation_foundation_defaults_business_behavior_add_user_default`

**Inputs** key, value, user = no value, parenttype = no value.

**Local steps**

- Evaluate add\_default(key, value, (user or Platform.session.user), parenttype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L887) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1547)

<a id="op-132eca63971a8b"></a>
### Get user default

`operation_foundation_defaults_business_behavior_get_user_default`

**Inputs** key, user = no value.

**Explicit results** no value · value.

**Local steps**

- Set user\_defaults from get\_defaults((user or Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set d from user\_defaults.get(key, no value).
- If is\_a\_user\_permission\_key(key).
  - If (d and isinstance(d, (list bitwise or tuple)) and len(d) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d → isinstance(d, (list bitwise or tuple)) → len(d) equals 1.
    - Set d from d at 0.
  - Otherwise.
    - Set d from user\_defaults.get(Platform.scrub(key), no value).
    - Set user\_permission\_default from get\_user\_permission\_default(key, user\_defaults).
    - If not d.
      - Set d from user\_permission\_default.
- Set value from ((isinstance(d, (list bitwise or tuple)) and d at 0) or d).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (isinstance(d, (list bitwise or tuple)) and d at 0) → d.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(d, (list bitwise or tuple)) → d at 0.
- If not\_in\_user\_permission(key, value, user).
  - Return no value.
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L14) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1554)

<a id="op-dc0e237f7edacf"></a>
### Get user permission default

`operation_foundation_defaults_business_behavior_get_user_permission_default`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** key, defaults.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L15) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1556)

<a id="op-7f341de1ac8ebe"></a>
### Get user default as list

`operation_foundation_defaults_business_behavior_get_user_default_as_list`

**Inputs** key, user = no value.

**Explicit results** list of value for value drawn from d where not not\_in\_user\_permission(key, value).

**Local steps**

- Set user\_defaults from get\_defaults((user or Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set d from user\_defaults.get(key, no value).
- If is\_a\_user\_permission\_key(key).
  - If (d and isinstance(d, (list bitwise or tuple)) and len(d) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d → isinstance(d, (list bitwise or tuple)) → len(d) equals 1.
    - Set d from list(d at 0).
  - Otherwise.
    - Set d from user\_defaults.get(Platform.scrub(key), no value).
- Set d from list(filter(no value, ((not isinstance(d, (nested operand in the contract bitwise or nested operand in the contract)) and list(d)) or d))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (not isinstance(d, (list bitwise or tuple)) and list(d)) → d.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not isinstance(d, (list bitwise or tuple)) → list(d).
- Return list of value for value drawn from d where not not\_in\_user\_permission(key, value).
  - Draw value from d, keep a combination only if (not not\_in\_user\_permission(key, value)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L1855) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1555)

<a id="op-2f7dee7e7c52fd"></a>
### Is a user permission key

`operation_foundation_defaults_business_behavior_is_a_user_permission_key`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** key.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L2289) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1558)

<a id="op-cdf3535dac541a"></a>
### Not in user permission

`operation_foundation_defaults_business_behavior_not_in_user_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** key, value, user.

**Explicit result forms** Boolean false, a value selected from the current context.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L2379) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1559)

<a id="op-134dddabf224e1"></a>
### Get user permissions

`operation_foundation_defaults_business_behavior_get_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L2608) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1557)

<a id="op-6d204c0358b7e9"></a>
### Get defaults

`operation_foundation_defaults_business_behavior_get_defaults`

**Inputs** user = no value.

**Explicit results** global\_defaults · defaults.

**Local steps**

- Set global\_defaults from get\_defaults\_for().
- If not user.
  - Set user from Platform.session.user when Platform.session, otherwise “Guest”.
    - Value choice on Platform.session — true gives Platform.session.user, false gives “Guest”.
- If not user.
  - Return global\_defaults.
- Set defaults from global\_defaults.copy().
- Evaluate defaults.update(get\_defaults\_for(user)).
- Evaluate defaults.update(user = user, owner = user).
- Return defaults.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L2671) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1551)

<a id="op-1cf5d83bd6d03c"></a>
### Clear user default

`operation_foundation_defaults_business_behavior_clear_user_default`

**Inputs** key, user = no value.

**Local steps**

- Evaluate clear\_default(key, parent = (user or Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L2902) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1550)

<a id="op-6c1c4cdda9bdcd"></a>
### Set global default

`operation_foundation_defaults_business_behavior_set_global_default`

**Inputs** key, value.

**Local steps**

- Evaluate set\_default(key, value, “\_\_default”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L2993) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1561)
