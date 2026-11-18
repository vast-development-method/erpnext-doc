# Forms, reports and navigation · operations 57

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Workspace · Setup wizard

<a id="op-d28055ce32722b"></a>
### Initialize system settings and user

`operation_foundation_desk_page_setup_wizard_business_behavior_initialize_system_settings_and_user`

**Inputs** system\_settings\_data, user\_data.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “System Settings” via get\_single.

**State and service calls** call save on system\_settings.

**Explicit results** no value.

**Local steps**

- Set system\_settings from Platform.get\_single(“System Settings”).
- If cint(system\_settings.setup\_complete).
  - Return no value.
- Set system\_settings\_data from parse\_args(sanitize\_input(system\_settings\_data)).
- Evaluate system\_settings.update(mapping(“language” → system\_settings\_data.get(“language”), “country” → system\_settings\_data.get(“country”), “currency” → system\_settings\_data.get(“currency”), “time\_zone” → system\_se ….
- Evaluate system\_settings.save().
- Set user\_data from parse\_args(sanitize\_input(user\_data)).
- Evaluate create\_or\_update\_user(user\_data).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L4075) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L349)

<a id="op-6b8eaf1011f890"></a>
### Process setup stages

`operation_foundation_desk_page_setup_wizard_business_behavior_process_setup_stages`

**Inputs** stages, user\_input, is\_background\_task = false.

**State and service calls** publish realtime with “setup\_task”.

**Explicit results** mapping(“status” → “ok”).

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies capture.
- Set setup\_wizard\_completed\_apps from get\_setup\_wizard\_completed\_apps().
- Set telemetry\_enabled from bool(cint(user\_input.get(“enable\_telemetry”))).
- Evaluate capture(“initiated\_server\_side”, “setup”).
- Attempt the following.
  - Set Platform.flags.in\_setup\_wizard from true.
  - Set current\_task from no value.
  - For each tuple(idx, stage) in enumerate(stages).
    - Evaluate Platform.publish\_realtime(“setup\_task”, mapping(“progress” → list(idx, len(stages)), “stage\_status” → stage.get(“status”)), user = Platform.session.user).
    - For each task in stage.get(“tasks”).
      - Set current\_task from task.
      - If (task.get(“app\_name”) and task.get(“app\_name”) belongs to setup\_wizard\_completed\_apps).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in task.get(“app\_name”) → task.get(“app\_name”) belongs to setup\_wizard\_completed\_apps.
        - Continue with the next iteration or loop test.
      - If “Platform” belongs to setup\_wizard\_completed\_apps.
        - Evaluate set\_missing\_values(task).
      - Evaluate task.get(“fn”)(task.get(“args”)).
      - If task.get(“app\_name”).
        - Evaluate enable\_setup\_wizard\_complete(task.get(“app\_name”)).
      - Otherwise.
        - Evaluate enable\_setup\_wizard\_complete(“Platform”).
- On failure (Exception).
  - Evaluate handle\_setup\_exception(user\_input).
  - Set message from current\_task.get(“fail\_msg”) when current\_task, otherwise translated “We couldn't finish setting things up”.
    - Value choice on current\_task — true gives current\_task.get(“fail\_msg”), false gives translated “We couldn't finish setting things up”.
  - Evaluate capture(“setup\_failed”, “setup”, properties = mapping(“telemetry\_enabled” → telemetry\_enabled, “stage” → current\_task at “fn”.\_\_name\_\_ when current\_task, otherwise no value, “app” → current\_task.get(“app\_n ….
    - Value choice on current\_task — true gives current\_task at “fn”.\_\_name\_\_, false gives no value.
    - Value choice on current\_task — true gives current\_task.get(“app\_name”), false gives no value.
  - Evaluate Platform.log\_error(title = formatted text Setup failed: {message}).
  - If not is\_background\_task.
    - Set Platform.response at “setup\_wizard\_failure\_message” from message.
    - Propagate the active failure.
  - Evaluate Platform.publish\_realtime(“setup\_task”, mapping(“status” → “fail”, “fail\_msg” → message), user = Platform.session.user).
- When the protected block completes normally.
  - Evaluate run\_setup\_success(user\_input).
  - Evaluate capture(“completed\_server\_side”, “setup”, properties = mapping(“telemetry\_enabled” → telemetry\_enabled)).
  - Evaluate apply\_telemetry\_preference(telemetry\_enabled).
  - If not is\_background\_task.
    - Return mapping(“status” → “ok”).
  - Evaluate Platform.publish\_realtime(“setup\_task”, mapping(“status” → “ok”), user = Platform.session.user).
- On exit, including pending return or failure.
  - Set Platform.flags.in\_setup\_wizard from false.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“setup\_task”, mapping(“progress” → list(idx, len(stages)), “stage\_status” → stage.get(“status”)), user = Platform.session.user), Platform.publish\_realtime(“setup\_task”, mapping(“status” → “fail”, “fail\_msg” → message), user = Platform.session.user) and 1 further calls.

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L87) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L358)

<a id="op-32c2ee992162a9"></a>
### Set missing values

`operation_foundation_desk_page_setup_wizard_business_behavior_set_missing_values`

**Inputs** task.

**Record and data access** resolve a document from “System Settings” via get\_doc.

**Local steps**

- If (task and task.get(“args”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task → task.get(“args”).
  - Set doc from Platform.get\_doc(“System Settings”).
  - Evaluate task at “args”.update(mapping(“country” → doc.country, “time\_zone” → doc.time\_zone, “time\_format” → doc.time\_format, “currency” → doc.currency)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L5735) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L362)

<a id="op-3cf10cebed2f71"></a>
### Enable setup wizard complete

`operation_foundation_desk_page_setup_wizard_business_behavior_enable_setup_wizard_complete`

**Inputs** app\_name.

**State and service calls** request set\_value on “Installed Application”.

**Local steps**

- Evaluate Platform.db.set\_value(“Installed Application”, mapping(“app\_name” → app\_name), “is\_setup\_complete”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L5947) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L340)

<a id="op-de7d281b1a8f5a"></a>
### Update global settings

`operation_foundation_desk_page_setup_wizard_business_behavior_update_global_settings`

**Inputs** args.

**State and service calls** enqueue with set\_timezone.

**Local steps**

- If (args.language and args.language differs from “English”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.language → args.language differs from “English”.
  - Evaluate set\_default\_language(get\_language\_code(args.language)).
- Evaluate Platform.clear\_cache().
- Evaluate update\_system\_settings(args).
- Evaluate create\_or\_update\_user(args).
- Evaluate Platform.enqueue(set\_timezone, timezone = args.get(“timezone”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(set\_timezone, timezone = args.get(“timezone”)).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L89) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L368)

<a id="op-44442e71fe6014"></a>
### Apply telemetry preference

`operation_foundation_desk_page_setup_wizard_business_behavior_apply_telemetry_preference`

**Inputs** telemetry\_enabled.

**State and service calls** request set\_single\_value on “System Settings”.

**Local steps**

- Evaluate Platform.db.set\_single\_value(“System Settings”, “enable\_telemetry”, cint(telemetry\_enabled)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L6286) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L335)

<a id="op-65258957fc75cf"></a>
### Run post setup complete

`operation_foundation_desk_page_setup_wizard_business_behavior_run_post_setup_complete`

**Inputs** args.

**Record and data access** resolve a document from “System Settings” via get\_cached\_doc · resolve a document from “System Settings” via get\_doc.

**State and service calls** commit.

**Local steps**

- Evaluate disable\_future\_access().
- Evaluate Platform.db.commit().
- Evaluate Platform.clear\_cache().
- Evaluate (Platform.get\_cached\_doc(“System Settings”) and Platform.get\_doc(“System Settings”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_cached\_doc(“System Settings”) → Platform.get\_doc(“System Settings”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“System Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L6377) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L359)

<a id="op-afb7a938860150"></a>
### Run setup success

`operation_foundation_desk_page_setup_wizard_business_behavior_run_setup_success`

**Inputs** args.

**Local steps**

- For each hook in Platform.get\_hooks(“setup\_wizard\_success”).
  - Evaluate Platform.get\_attr(hook)(args).
- Evaluate install\_fixtures.install().
- If (not Platform.conf.developer\_mode and not Platform.\_dev\_server).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.\_dev\_server.
  - Evaluate login\_as\_first\_user(args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“setup\_wizard\_success”), Platform.get\_attr(hook).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L6524) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L360)

<a id="op-715e7831c5206d"></a>
### Login as first user

`operation_foundation_desk_page_setup_wizard_business_behavior_login_as_first_user`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** args.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L6705) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L354)

<a id="op-600688f69e5697"></a>
### Get stages hooks

`operation_foundation_desk_page_setup_wizard_business_behavior_get_stages_hooks`

**Inputs** args.

**Explicit results** stages.

**Local steps**

- Set stages from list().
- Set installed\_apps from Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
- For each app\_name in installed\_apps.
  - Set setup\_wizard\_stages from Platform.get\_hooks(app\_name = app\_name).get(“setup\_wizard\_stages”).
  - If not setup\_wizard\_stages.
    - Continue with the next iteration or loop test.
  - For each method in setup\_wizard\_stages.
    - Set \_stages from Platform.get\_attr(method)(args).
    - Evaluate update\_app\_details\_in\_stages(\_stages, app\_name).
    - Update stages using + \_stages.
- Return stages.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(app\_name = app\_name), Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L85) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L347)

<a id="op-fa2996156a66f2"></a>
### Update app details in stages

`operation_foundation_desk_page_setup_wizard_business_behavior_update_application_details_in_stages`

**Inputs** \_stages, app\_name.

**Local steps**

- For each stage in \_stages.
  - For each key in stage.
    - If key differs from “tasks”.
      - Continue with the next iteration or loop test.
    - For each task in stage at key.
      - If task.get(“app\_name”) is identical to no value.
        - Set task at “app\_name” from app\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L367)

<a id="op-f9316a2e031504"></a>
### Get setup complete hooks

`operation_foundation_desk_page_setup_wizard_business_behavior_get_setup_complete_hooks`

**Inputs** args.

**Explicit results** list of mapping(“status” → translated “Setting up your apps”, “fail\_msg” → translated “We couldn't finish setting up your apps”, “tasks” → list(mapping(“fn” → Platform.get\_attr(method), “args” → args, “fai ….

**Local steps**

- Return list of mapping(“status” → translated “Setting up your apps”, “fail\_msg” → translated “We couldn't finish setting up your apps”, “tasks” → list(mapping(“fn” → Platform.get\_attr(method), “args” → args, “fai ….
  - Draw method from Platform.get\_hooks(“setup\_wizard\_complete”).

**Values supplied outside this operation** selected callable from Platform.get\_attr(method), Platform.get\_hooks(“setup\_wizard\_complete”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L82) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1864) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L344)

<a id="op-180e4ecffd7a75"></a>
### Handle setup exception

`operation_foundation_desk_page_setup_wizard_business_behavior_handle_setup_exception`

**Inputs** args.

**State and service calls** rollback.

**Local steps**

- Evaluate Platform.db.rollback().
- If args.
  - Set traceback from Platform.get\_traceback(with\_context = true).
  - Evaluate print(traceback).
  - For each hook in Platform.get\_hooks(“setup\_wizard\_exception”).
    - Evaluate Platform.get\_attr(hook)(traceback, args).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“setup\_wizard\_exception”), Platform.get\_attr(hook).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L406) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L348)

<a id="op-e1374d04ca7521"></a>
### Update system settings

`operation_foundation_desk_page_setup_wizard_business_behavior_update_system_settings`

**Inputs** args.

**Record and data access** resolve a document from “System Settings” via get\_doc · read “Country” via get\_value.

**State and service calls** request set\_single\_value on “System Settings” · call save on system\_settings.

**Explicit results** no value.

**Local steps**

- Set defaults from mapping(“float\_precision” → 3, “rounding\_method” → “Banker's Rounding”, “enable\_scheduler” → 1 when not Platform.in\_test, otherwise 0, “backup\_limit” → 3).
  - Value choice on not Platform.in\_test — true gives 1, false gives 0.
- If not args.get(“country”).
  - Evaluate Platform.db.set\_single\_value(“System Settings”, defaults).
  - Return no value.
- Set number\_format from get\_country\_info(args.get(“country”)).get(“number\_format”, “#,###.##”).
- If number\_format equals “#.###”.
  - Set number\_format from “#.###,##”.
- Otherwise.
  - If number\_format equals “#,###”.
    - Set number\_format from “#,###.##”.
- Set system\_settings from Platform.get\_doc(“System Settings”, “System Settings”).
- Evaluate system\_settings.update(mapping(expand defaults, “country” → args.get(“country”), “language” → (get\_language\_code(args.get(“language”)) or “en”), “time\_zone” → args.get(“timezone”), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_language\_code(args.get(“language”)) → “en”.
- Evaluate system\_settings.save().
- If args.get(“allow\_recording\_first\_session”).
  - Evaluate Platform.db.set\_default(“session\_recording\_start”, now()).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L90) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L369)

<a id="op-5158d9395e43bd"></a>
### Create or update user

`operation_foundation_desk_page_setup_wizard_business_behavior_create_or_update_user`

**Inputs** args.

**Record and data access** read “User” via get\_value.

**State and service calls** request new\_doc for “User” · call insert on user.

**Explicit results** no value.

**Local steps**

- Set email from args.get(“email”).
- If not email.
  - Return no value.
- Set tuple(first\_name, last\_name) from tuple(args.get(“full\_name”, empty text), empty text).
- If one space belongs to first\_name.
  - Set tuple(first\_name, last\_name) from first\_name.split(one space, 1).
- If user bound to Platform.db.get\_value(“User”, email, list(“first\_name”, “last\_name”), as\_dict = true).
  - If (user.first\_name differs from first\_name or user.last\_name differs from last\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user.first\_name differs from first\_name → user.last\_name differs from last\_name.
    - Set User from Platform.qb.DocType(“User”).
    - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(User.full\_name, nested operand in the contract.get(“full\_name”)).where(User.name equals email).run().
- Otherwise.
  - Set tuple(\_mute\_emails, Platform.flags.mute\_emails) from tuple(Platform.flags.mute\_emails, true).
  - Set user from Platform.new\_doc(“User”).
  - Evaluate user.update(mapping(“email” → email, “first\_name” → first\_name, “last\_name” → last\_name)).
  - Evaluate user.append\_roles(expanded \_get\_default\_roles()).
  - Evaluate user.append\_roles(“System Manager”).
  - Set user.flags.no\_welcome\_mail from true.
  - Evaluate user.insert().
  - Set Platform.flags.mute\_emails from \_mute\_emails.
- If args.get(“password”).
  - Evaluate update\_password(email, args.get(“password”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L1370) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L337)

<a id="op-636b9b2d38109d"></a>
### Set timezone

`operation_foundation_desk_page_setup_wizard_business_behavior_set_timezone`

**Inputs** timezone = no value.

**State and service calls** request set\_value on “User”.

**Explicit results** no value.

**Local steps**

- If not timezone.
  - Return no value.
- Evaluate Platform.db.set\_value(“User”, mapping(“name” → tuple(“in”, Platform.STANDARD\_USERS)), “time\_zone”, timezone).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L2252) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L363)

<a id="op-e0917fff36be93"></a>
### Parse args

`operation_foundation_desk_page_setup_wizard_business_behavior_parse_arguments`

**Inputs** args.

**Explicit results** args.

**Local steps**

- If not args.
  - Set args from Platform.local.form\_dict.
- If isinstance(args, str).
  - Set args from json.loads(args).
- Set args from Platform.\_dict(args).
- For each tuple(key, value) in args.items().
  - If isinstance(value, str).
    - Set args at key from strip(value).
- Return args.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L2385) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L356)

<a id="op-6976d4b0c81b1b"></a>
### Sanitize input

`operation_foundation_desk_page_setup_wizard_business_behavior_sanitize_input`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** args.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L2637) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L361)

<a id="op-542f30350795a2"></a>
### Add all roles to

`operation_foundation_desk_page_setup_wizard_business_behavior_add_all_roles_to`

**Inputs** name.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user.

**Local steps**

- Set user from Platform.get\_doc(“User”, name).
- Evaluate user.append\_roles(expanded \_get\_default\_roles()).
- Evaluate user.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L2833) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L334)

<a id="op-270d92685103b2"></a>
### Get default roles

`operation_foundation_desk_page_setup_wizard_business_behavior_get_default_roles`

**Inputs** no declared parameters.

**Declared result** set at str.

**Record and data access** read “Role” via get\_all.

**Explicit results** (set(Platform.get\_all(“Role”, pluck = “name”)) − skip\_roles).

**Local steps**

- Set skip\_roles from set(“Administrator”, “Customer”, “Supplier”, “Partner”, …).union(AUTOMATIC\_ROLES).
- Return (set(Platform.get\_all(“Role”, pluck = “name”)) − skip\_roles).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L2956) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L342)

<a id="op-a203f05fce986f"></a>
### Disable future access

`operation_foundation_desk_page_setup_wizard_business_behavior_disable_future_access`

**Inputs** no declared parameters.

**State and service calls** request set\_single\_value on “System Settings”.

**Local steps**

- Evaluate Platform.db.set\_default(“desktop:home\_page”, “workspace”).
- Evaluate Platform.clear\_cache(doctype = “System Settings”).
- Evaluate Platform.db.set\_single\_value(“System Settings”, “enable\_onboarding”, 1).
- Evaluate Platform.db.set\_single\_value(“System Settings”, “setup\_complete”, Platform.is\_setup\_complete()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L3122) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L338)

<a id="op-a79f4baa034431"></a>
### Load messages

`operation_foundation_desk_page_setup_wizard_business_behavior_load_messages`

**Inputs** language.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** commit.

**Explicit results** Platform.local.lang.

**Local steps**

- Bind dependencies get\_messages\_for\_boot.
- Evaluate Platform.clear\_cache().
- Evaluate set\_default\_language(get\_language\_code(language)).
- Evaluate Platform.db.commit().
- Evaluate send\_translations(get\_messages\_for\_boot()).
- Return Platform.local.lang.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L3317) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L351)

<a id="op-df8fadd03b07ba"></a>
### Load languages

`operation_foundation_desk_page_setup_wizard_business_behavior_load_languages`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Language” via get\_value.

**Explicit results** mapping(“default\_language” → (Platform.db.get\_value(“Language”, Platform.local.lang, “language\_name”) or Platform.local.lang), “languages” → language\_opts, “codes\_to\_names” → codes\_to\_names).

**Local steps**

- Set Language from Platform.qb.DocType(“Language”).
- Set language\_codes from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.enabled equals 1).orderby(Language.language\_code).run(as\_dict = 1).
- Set language\_opts from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.enabled equals 1).orderby(Language.langua ….
- Set codes\_to\_names from mapping().
- For each d in language\_codes.
  - Set codes\_to\_names at d.language\_code from d.language\_name.
- Return mapping(“default\_language” → (Platform.db.get\_value(“Language”, Platform.local.lang, “language\_name”) or Platform.local.lang), “languages” → language\_opts, “codes\_to\_names” → codes\_to\_names).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Language”, Platform.local.lang, “language\_name”) → Platform.local.lang.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L86) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1870) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L350)

<a id="op-7e6d9cdf9da30e"></a>
### Load user details

`operation_foundation_desk_page_setup_wizard_business_behavior_load_user_details`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“full\_name” → Platform.cache.hget(“full\_name”, “signup”), “email” → Platform.cache.hget(“email”, “signup”)).

**Local steps**

- Return mapping(“full\_name” → Platform.cache.hget(“full\_name”, “signup”), “email” → Platform.cache.hget(“email”, “signup”)).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0208.json#L3975) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L352)
