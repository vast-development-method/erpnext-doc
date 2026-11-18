# Shared value and file services · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Logger

<a id="op-ce7e96667dead6"></a>
### Site Context Filter.filter

`operation_foundation_utils_logger_business_behavior_site_context_filter_filter`

**Inputs** self, record.

**Declared result** bool.

**Explicit results** true.

**Local steps**

- If “Form Dict” does not belong to str(record.msg).
  - Set site from getattr(Platform.local, “site”, no value).
  - Set form\_dict from sanitized\_dict(getattr(Platform.local, “form\_dict”, no value)).
  - Set record.msg from (str(record.msg) + formatted text  Site: {site} Form Dict: {form\_dict}).
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “site”, no value), getattr(Platform.local, “form\_dict”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L2975) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L338)

<a id="op-44523ba215a3d6"></a>
### Set log level

`operation_foundation_utils_logger_business_behavior_set_log_level`

**Inputs** level.

**Declared result** no value.

**Local steps**

- Set Platform.log\_level from (getattr(logging, (level or empty text).upper(), no value) or default\_log\_level).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(logging, (level or empty text).upper(), no value) → default\_log\_level.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in level → empty text.
- Set Platform.loggers from mapping().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(logging, (level or empty text).upper(), no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L3222) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L337)

<a id="op-630a4fd181e19c"></a>
### Sanitized dict

`operation_foundation_utils_logger_business_behavior_sanitized_mapping`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** form\_dict.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L3387) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L336)

## Service · Make random

<a id="op-c8e5f1b2a9743b"></a>
### Add random children

`operation_foundation_utils_make_random_business_behavior_add_random_children`

**Inputs** doc, fieldname, rows, randomize, unique = no value.

**Local steps**

- Set nrows from rows.
- If rows &gt; 1.
  - Set nrows from random.randrange(1, rows).
- For each \_ in range(nrows).
  - Set d from mapping().
  - For each tuple(key, val) in randomize.items().
    - If isinstance(val at 0, str).
      - Set d at key from get\_random(expanded val).
    - Otherwise.
      - Set d at key from random.randrange(expanded val).
  - If unique.
    - If not doc.get(fieldname, mapping(unique → d at unique)).
      - Evaluate doc.append(fieldname, d).
  - Otherwise.
    - Evaluate doc.append(fieldname, d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L3607) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L339)

<a id="op-902c7eb9625702"></a>
### Get random

`operation_foundation_utils_make_random_business_behavior_get_random`

**Inputs** doctype, filters = no value, doc = false.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** Platform.get\_doc(doctype, out) · out.

**Local steps**

- Set condition from list().
- If filters.
  - Evaluate condition.extend(generator of “{}='{}'”.format(key, str(val).replace(“'”, “'”)) for tuple(key, val) drawn from filters.items()).
    - Draw tuple(key, val) from filters.items().
- Set condition from (“ where ” + “ and ”.join(condition)) when condition, otherwise empty text.
  - Value choice on condition — true gives (“ where ” + “ and ”.join(condition)), false gives empty text.
- Set out from Platform.db.multisql(mapping(“mariadb” → formatted text select name from ′tab{doctype}′ {condition} order by RAND() limit 1 offset 0, “\*” → formatted text select name from ′tab{doctype}′ {condition} order  ….
- Set out from ((out and out at 0 at 0) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (out and out at 0 at 0) → no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in out → out at 0 at 0.
- If (doc and out).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → out.
  - Return Platform.get\_doc(doctype, out).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L4057) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L341)

<a id="op-8e22c25cbbf132"></a>
### Can make

`operation_foundation_utils_make_random_business_behavior_can_make`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** random.random() &lt; settings.prob.get(doctype, settings.prob at “default”) at “make”.

**Local steps**

- Return random.random() &lt; settings.prob.get(doctype, settings.prob at “default”) at “make”.

**Values supplied outside this operation** clock or generated value from random.random().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L4588) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L340)

<a id="op-16facd4e41cb20"></a>
### How many

`operation_foundation_utils_make_random_business_behavior_how_many`

**Inputs** doctype.

**Declared result** int.

**Explicit results** random.randrange(expanded settings.prob.get(doctype, settings.prob at “default”) at “qty”).

**Local steps**

- Return random.randrange(expanded settings.prob.get(doctype, settings.prob at “default”) at “qty”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L4708) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L342)

## Service · Messages

<a id="op-9fb445b6ceb23b"></a>
### Msgprint

`operation_foundation_utils_messages_business_behavior_msgprint`

**Inputs** msg, title = no value, raise\_exception = false, as\_table = false, as\_list = false, indicator = no value, alert = false, primary\_action = no value, is\_minimizable = false, wide = false, realtime (named only, default false), allow\_dangerous\_html (named only, default false).

**Declared result** no value.

**State and service calls** publish realtime.

**Explicit results** no value.

**Local steps**

- Bind dependencies inspect.
- Bind dependencies clean\_html.
- Set msg from safe\_decode(msg).
- Set out from Platform.\_dict(message = msg).
- Bind local operation \_raise\_exception for subsequent calls.
- If Platform.flags.mute\_messages.
  - Evaluate \_raise\_exception().
  - Return no value.
- If isinstance(msg, Sequence).
  - If as\_list.
    - Set out.as\_list from as\_list.
  - Otherwise.
    - Set out.as\_table from as\_table.
- If not allow\_dangerous\_html.
  - If out.as\_list.
    - Set out.message from list of clean\_html(cell) for cell drawn from msg.
      - Draw cell from msg.
  - Otherwise.
    - If out.as\_table.
      - Set out.message from list of list of clean\_html(cell) for cell drawn from row for row drawn from msg.
        - Draw row from msg.
        - Draw cell from row.
    - Otherwise.
      - Set out.message from clean\_html(msg).
- If (Platform.flags.print\_messages and out.message).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.print\_messages → out.message.
  - Set terminal\_msg from msg.
  - If (sys.stdin and sys.stdin.isatty()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sys.stdin → sys.stdin.isatty().
    - If out.as\_list.
      - Set terminal\_msg from list of strip\_html\_tags(cell) for cell drawn from msg.
        - Draw cell from msg.
    - Otherwise.
      - If out.as\_table.
        - Set terminal\_msg from list of list of strip\_html\_tags(cell) for cell drawn from row for row drawn from msg.
          - Draw row from msg.
          - Draw cell from row.
      - Otherwise.
        - Set terminal\_msg from strip\_html\_tags(msg).
  - Evaluate print(formatted text Message: {terminal\_msg}).
- Set out.title from (title or \_(“Message”, context = “Default title of the message dialog”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in title → \_(“Message”, context = “Default title of the message dialog”).
- If (not indicator and raise\_exception).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not indicator → raise\_exception.
  - Set indicator from “red”.
- If indicator.
  - Set out.indicator from indicator.
- If is\_minimizable.
  - Set out.is\_minimizable from is\_minimizable.
- If alert.
  - Set out.alert from 1.
- If raise\_exception.
  - Set out.raise\_exception from 1.
  - Set out.\_\_Platform\_exc\_id from Platform.generate\_hash().
- If primary\_action.
  - Set out.primary\_action from primary\_action.
- If wide.
  - Set out.wide from wide.
- If realtime.
  - Evaluate Platform.publish\_realtime(event = “msgprint”, message = out).
- Otherwise.
  - Evaluate Platform.message\_log.append(out).
- Evaluate \_raise\_exception().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash() · service or queued work from Platform.publish\_realtime(event = “msgprint”, message = out).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L137) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L346)

<a id="op-523fc77023c371"></a>
### Msgprint.raise exception

`operation_foundation_utils_messages_business_behavior_msgprint_raise_exception`

**Inputs** no declared parameters.

**Explicit failure paths** exc.

**Local steps**

- If raise\_exception.
  - If (inspect.isclass(raise\_exception) and issubclass(raise\_exception, Exception)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in inspect.isclass(raise\_exception) → issubclass(raise\_exception, Exception).
    - Set exc from raise\_exception(msg).
  - Otherwise.
    - If isinstance(raise\_exception, Exception).
      - Set exc from raise\_exception.
      - Set exc.args from tuple(msg).
    - Otherwise.
      - Set exc from Platform.ValidationError(msg).
  - If out.\_\_Platform\_exc\_id.
    - Set exc.\_\_Platform\_exc\_id from out.\_\_Platform\_exc\_id.
  - Raise exc.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L6422) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L347)

<a id="op-13e1710fad9e08"></a>
### Toast

`operation_foundation_utils_messages_business_behavior_toast`

**Inputs** message, indicator = no value.

**Local steps**

- Evaluate msgprint(message, indicator = indicator, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L6671) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L350)

<a id="op-2aa731c446793d"></a>
### Clear messages

`operation_foundation_utils_messages_business_behavior_clear_messages`

**Inputs** no declared parameters.

**Local steps**

- Set Platform.local.message\_log from list().

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L6817) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L344)

<a id="op-b8e10019f79863"></a>
### Get message log

`operation_foundation_utils_messages_business_behavior_get_message_log`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list of msg\_out for msg\_out drawn from Platform.local.message\_log.

**Local steps**

- Return list of msg\_out for msg\_out drawn from Platform.local.message\_log.
  - Draw msg\_out from Platform.local.message\_log.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L6860) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L345)

<a id="op-75fa24e14980fe"></a>
### Clear last message

`operation_foundation_utils_messages_business_behavior_clear_last_message`

**Inputs** no declared parameters.

**Local steps**

- If len(Platform.local.message\_log) &gt; 0.
  - Set Platform.local.message\_log from Platform.local.message\_log at slice no value to negative 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L6927) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L343)

<a id="op-531af6140b9d43"></a>
### Throw

`operation_foundation_utils_messages_business_behavior_throw`

**Inputs** msg, exc = Platform.ValidationError, title = no value, is\_minimizable = false, wide = false, as\_list = false, primary\_action = no value, allow\_dangerous\_html (named only, default false).

**Declared result** no value.

**Local steps**

- Evaluate msgprint(msg, raise\_exception = exc, title = title, indicator = “red”, is\_minimizable = is\_minimizable, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L7041) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L348)

<a id="op-acdc2d252829b7"></a>
### Throw permission error

`operation_foundation_utils_messages_business_behavior_throw_permission_error`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L7331) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L349)

## Service · Modules

<a id="op-4dd73c7836f5bb"></a>
### Get module placement

`operation_foundation_utils_modules_business_behavior_get_module_placement`

**Inputs** module.

**Declared result** (str bitwise or no value).

**Record and data access** read “Module Def” via get\_value.

**Explicit results** (app or Platform.db.get\_value(“Module Def”, module, “app\_name”, cache = true) or no value).

**Local steps**

- Set app from Platform.local.module\_app.get(Platform.scrub(module)).
- Return (app or Platform.db.get\_value(“Module Def”, module, “app\_name”, cache = true) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app → Platform.db.get\_value(“Module Def”, module, “app\_name”, cache = true) → no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L7397) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L354)

<a id="op-dd0e9851472cd2"></a>
### Get blocked modules

`operation_foundation_utils_modules_business_behavior_get_blocked_modules`

**Inputs** user = no value.

**Declared result** list at str.

**Record and data access** resolve a document from “User” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“User”, user).get\_blocked\_modules().

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Return Platform.get\_cached\_doc(“User”, user).get\_blocked\_modules().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“User”, user).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L7567) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L351)

<a id="op-82a5f8bcbaff13"></a>
### Is module visible

`operation_foundation_utils_modules_business_behavior_is_module_visible`

**Inputs** module, user = no value.

**Declared result** bool.

**Explicit results** true · module does not belong to get\_blocked\_modules(user).

**Local steps**

- If not module.
  - Return true.
- Return module does not belong to get\_blocked\_modules(user).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L7700) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L361)

<a id="op-52ec98fa8e93fa"></a>
### Get visible modules

`operation_foundation_utils_modules_business_behavior_get_visible_modules`

**Inputs** modules, user = no value.

**Declared result** list at str.

**Explicit results** list of m for m drawn from modules where m does not belong to blocked.

**Local steps**

- Set blocked from set(get\_blocked\_modules(user)).
- Return list of m for m drawn from modules where m does not belong to blocked.
  - Draw m from modules, keep a combination only if (m does not belong to blocked).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L7823) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L358)

<a id="op-5b6e14cc156ac3"></a>
### Get code only modules

`operation_foundation_utils_modules_business_behavior_get_code_only_modules`

**Inputs** no declared parameters.

**Declared result** set at str.

**Explicit results** set((Platform.get\_hooks(“code\_only\_modules”) or list())).

**Local steps**

- Return set((Platform.get\_hooks(“code\_only\_modules”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“code\_only\_modules”) → list().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“code\_only\_modules”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L7986) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L353)

<a id="op-0e50f73fb20b90"></a>
### Get code only module heirs

`operation_foundation_utils_modules_business_behavior_get_code_only_module_heirs`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, list at str).

**Explicit results** mapping of module → list(heirs) for tuple(module, heirs) drawn from (Platform.get\_hooks(“code\_only\_modules”) or mapping()).items().

**Local steps**

- Return mapping of module → list(heirs) for tuple(module, heirs) drawn from (Platform.get\_hooks(“code\_only\_modules”) or mapping()).items().
  - Draw tuple(module, heirs) from (Platform.get\_hooks(“code\_only\_modules”) or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“code\_only\_modules”) → mapping().

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“code\_only\_modules”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L8069) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L352)

<a id="op-f9e739945d9bff"></a>
### Get modules from all apps for user

`operation_foundation_utils_modules_business_behavior_get_modules_from_all_apps_for_user`

**Inputs** user = no value.

**Declared result** list at dict.

**Explicit results** list of m for m drawn from all\_modules where m.get(“module\_name”) belongs to visible.

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set all\_modules from get\_modules\_from\_all\_apps().
- Set visible from set(get\_visible\_modules(list of m.get(“module\_name”) for m drawn from all\_modules, user)).
  - Draw m from all\_modules.
- Return list of m for m drawn from all\_modules where m.get(“module\_name”) belongs to visible.
  - Draw m from all\_modules, keep a combination only if (m.get(“module\_name”) belongs to visible).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0487.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L356)

<a id="op-06a60246083e2e"></a>
### Get modules from all apps

`operation_foundation_utils_modules_business_behavior_get_modules_from_all_apps`

**Inputs** no declared parameters.

**Explicit results** modules\_list.

**Local steps**

- Set modules\_list from list().
- For each app in Platform.get\_installed\_apps().
  - Update modules\_list using + get\_modules\_from\_app(app).
- Return modules\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L138) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L355)

<a id="op-5932aa9295ce65"></a>
### Get blockable module names

`operation_foundation_binding_foundation_utils_modules_get_blockable_module_names`

**Inputs** blocked = tuple().

**Declared result** list at str.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** sorted(names).

**Local steps**

- Set names from set(blocked).
- Evaluate names.update(generator of m.get(“module\_name”) for m drawn from get\_modules\_from\_all\_apps()).
  - Draw m from get\_modules\_from\_all\_apps().
- Evaluate names.update(Platform.get\_all(“Module Def”, filters = mapping(“custom” → 1), pluck = “name”)).
- Return sorted(names).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L60) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L218)
