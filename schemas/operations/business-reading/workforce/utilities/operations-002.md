# Supporting services · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Index

<a id="op-c82d441c48442a"></a>
### Get all filters

`operation_workforce_public_pages_jobs_index_business_behavior_get_all_filters`

**Inputs** filters = no value.

**Record and data access** read “Job Opening” via get\_all.

**Explicit results** mapping of key → sorted(value) for tuple(key, value) drawn from all\_filters.items().

**Local steps**

- Set job\_openings from Platform.get\_all(“Job Opening”, filters = mapping(“publish” → 1, “status” → “Open”), fields = list(“company”, “department”, “employment\_type”, “location”)).
- Set companies from filters.get(“company”, list()).
- Set all\_filters from mapping().
- For each opening in job\_openings.
  - For each tuple(key, value) in opening.items().
    - If (value and (key equals “company” or not companies or opening.company belongs to companies)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in value → (key equals “company” or not companies or opening.company belongs to companies).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in key equals “company” → not companies → opening.company belongs to companies.
      - Evaluate all\_filters.setdefault(key, set()).add(value).
- Return mapping of key → sorted(value) for tuple(key, value) drawn from all\_filters.items().
  - Draw tuple(key, value) from all\_filters.items().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L4048) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1052) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L3)

<a id="op-ad285fb354a1cf"></a>
### Get filters txt sort offset

`operation_workforce_public_pages_jobs_index_business_behavior_get_filters_text_resource_sort_offset`

**Inputs** page\_len = 20.

**Explicit results** tuple(filters, txt, sort, offset).

**Local steps**

- Set args from Platform.request.args.to\_dict(flat = false).
- Set filters from mapping().
- Set txt from empty text.
- Set sort from no value.
- Set offset from 0.
- Set allowed\_filters from list(“company”, “department”, “employment\_type”, “location”).
- For each d in args.
  - If d belongs to allowed\_filters.
    - Set filters at d from args at d.
  - Otherwise.
    - If d equals “query”.
      - Set txt from args at “query” at 0.
    - Otherwise.
      - If d equals “sort”.
        - If args at “sort” at 0.
          - Set sort from args at “sort” at 0.
      - Otherwise.
        - If d equals “page”.
          - Set offset from ((int(args at “page” at 0) − 1) × page\_len).
- Return tuple(filters, txt, sort, offset).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L4491) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1054) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L5)

## Service · Install

<a id="op-62b302a4af5a1c"></a>
### After install

`operation_workforce_install_business_behavior_after_install`

**Inputs** no declared parameters.

**Explicit failure paths** e.

**Local steps**

- Attempt the following.
  - Evaluate print(“Setting up Platform HR...”).
  - Evaluate setup().
  - Evaluate click.secho(“Thank you for installing Platform HR!”, fg = “green”).
- On failure (Exception) bound to e.
  - Set BUG\_REPORT\_URL from text in the contract.
  - Evaluate click.secho(formatted text Installation for Platform HR app failed due to an error. Please try re-installing the app or report the issue on {BUG\_REPORT\_URL} if not resolved., fg = “bright\_red”).
  - Raise e.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0098.json#L2730) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L182) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L531)

## Service · Roster

<a id="op-213315fae4e1fb"></a>
### Get context

`operation_workforce_public_pages_roster_business_behavior_get_context`

**Inputs** context.

**State and service calls** commit.

**Explicit results** context.

**Local steps**

- Set csrf\_token from Platform.sessions.get\_csrf\_token().
- Evaluate Platform.db.commit().
- Set context from Platform.\_dict().
- Set context.csrf\_token from csrf\_token.
- Return context.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0159.json#L4979) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1057) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L8)

## Service · Setup wizard

<a id="op-6c3664ddb7d7f7"></a>
### Get setup stages

`operation_workforce_setup_wizard_business_behavior_get_setup_stages`

**Inputs** wizard\_args = no value.

**Explicit results** list() · list(mapping(“status” → translated “Personalizing your setup”, “fail\_msg” → translated “Failed to personalize your setup”, “tasks” → tasks)).

**Local steps**

- If not Platform.conf.sk\_Workforce.
  - Return list().
- Set tasks from list(mapping(“fn” → capture\_user\_persona, “args” → persona\_from\_wizard\_args(wizard\_args) when wizard\_args, otherwise no value, “fail\_msg” → translated “Failed to personalize your setup”)).
  - Value choice on wizard\_args — true gives persona\_from\_wizard\_args(wizard\_args), false gives no value.
- If is\_new\_hr\_site().
  - Evaluate tasks.append(mapping(“fn” → set\_Workforce\_as\_default\_app, “args” → no value, “fail\_msg” → translated “Failed to personalize your setup”)).
- Return list(mapping(“status” → translated “Personalizing your setup”, “fail\_msg” → translated “Failed to personalize your setup”, “tasks” → tasks)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L17) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1111) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L58)

<a id="op-d97b50779ef4f6"></a>
### Persona from wizard args

`operation_workforce_setup_wizard_business_behavior_persona_from_wizard_arguments`

**Inputs** wizard\_args.

**Declared result** dict.

**Explicit results** mapping(“implementing\_for” → wizard\_args.get(“persona\_implementing\_for”), “company\_size” → wizard\_args.get(“persona\_company\_size”), “industry” → wizard\_args.get(“persona\_industry”), “current\_system” → wiza ….

**Local steps**

- Return mapping(“implementing\_for” → wizard\_args.get(“persona\_implementing\_for”), “company\_size” → wizard\_args.get(“persona\_company\_size”), “industry” → wizard\_args.get(“persona\_industry”), “current\_system” → wiza ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L4687) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1112) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L59)

<a id="op-cc8c86fc4c8714"></a>
### Capture user persona

`operation_workforce_setup_wizard_business_behavior_capture_user_persona`

**Inputs** persona.

**Explicit results** no value.

**Local steps**

- If not persona.
  - Return no value.
- Evaluate capture(“user\_persona\_submitted”, “Workforce”, properties = mapping of field → persona.get(field) for field drawn from PERSONA\_FIELDS).
  - Draw field from PERSONA\_FIELDS.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L5064) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1110) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L57)

## Service · Subscription utils

<a id="op-b2f37a712e6767"></a>
### Get add on details

`operation_workforce_subscription_utils_business_behavior_get_add_on_details`

**Inputs** plan.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, int).

**Explicit results** add\_on\_details.

**Local steps**

- Set EMPLOYEE\_LIMITS from mapping(“Basic” → 25, “Essential” → 50, “Professional” → 100).
- Set add\_on\_details from mapping().
- Set employees\_included\_in\_plan from EMPLOYEE\_LIMITS.get(plan).
- If employees\_included\_in\_plan.
  - Set active\_employees from get\_active\_employees().
  - Set add\_on\_employees from (active\_employees − employees\_included\_in\_plan) when active\_employees &gt; employees\_included\_in\_plan, otherwise 0.
    - Value choice on active\_employees &gt; employees\_included\_in\_plan — true gives (active\_employees − employees\_included\_in\_plan), false gives 0.
- Otherwise.
  - Set add\_on\_employees from 0.
- Set add\_on\_details at “employees” from add\_on\_employees.
- Return add\_on\_details.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L5202) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1114) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L61)

<a id="op-63ead16e1abb71"></a>
### Get active employees

`operation_workforce_subscription_utils_business_behavior_get_active_employees`

**Inputs** no declared parameters.

**Declared result** int.

**Record and data access** read “Employee” via count.

**Explicit results** Platform.db.count(“Employee”, mapping(“status” → “Active”)).

**Local steps**

- Return Platform.db.count(“Employee”, mapping(“status” → “Active”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L5485) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1113) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L60)

<a id="op-087c4d646be86a"></a>
### Subscription updated

`operation_workforce_subscription_utils_business_behavior_subscription_updated`

**Inputs** app, plan.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Local steps**

- If (app belongs to list(“Workforce”, “Enterprise”) and plan).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in app belongs to list(“Workforce”, “Enterprise”) → plan.
  - Evaluate update\_Enterprise\_access().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L5563) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1123) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L70)

<a id="op-1f58deda5e73ac"></a>
### Set Workforce as default app

`operation_workforce_binding_workforce_subscription_utils_set_workforce_as_default_app`

**Inputs** remaining positional values args.

**State and service calls** request set\_single\_value on “System Settings”.

**Local steps**

- If not Platform.get\_system\_settings(“default\_app”).
  - Evaluate Platform.db.set\_single\_value(“System Settings”, “default\_app”, “Workforce”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“default\_app”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L190) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L241) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L241)

<a id="op-7ee1d94ce35200"></a>
### Is new hr site

`operation_workforce_binding_workforce_subscription_utils_is_new_hr_site`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** (bool(Platform.conf.sk\_Workforce) and “Platform” does not belong to get\_setup\_wizard\_completed\_apps()).

**Local steps**

- Return (bool(Platform.conf.sk\_Workforce) and “Platform” does not belong to get\_setup\_wizard\_completed\_apps()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(Platform.conf.sk\_Workforce) → “Platform” does not belong to get\_setup\_wizard\_completed\_apps().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L189) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L240) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L240)

<a id="op-174323f3ff9c81"></a>
### Update Enterprise access

`operation_workforce_subscription_utils_business_behavior_update_enterprise_access`

**Inputs** user\_input.

**Explicit results** no value.

**Local steps**

- If not Platform.utils.get\_url().endswith(“.Platformhr.com”).
  - Return no value.
- Evaluate update\_Enterprise\_workspaces(true).
- Evaluate update\_Enterprise\_roles(true).
- Evaluate set\_app\_logo().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L5702) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1124) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L71)

<a id="op-999f50a4e609e8"></a>
### Update Enterprise workspaces

`operation_workforce_subscription_utils_business_behavior_update_enterprise_workspaces`

**Inputs** disable = true.

**Record and data access** resolve a document from “Workspace” via get\_doc.

**State and service calls** call save on workspace\_doc.

**Local steps**

- Set Enterprise\_workspaces from list(“Home”, “Assets”, “Accounting”, “Buying”, …).
- For each workspace in Enterprise\_workspaces.
  - Attempt the following.
    - Set workspace\_doc from Platform.get\_doc(“Workspace”, workspace).
    - Set workspace\_doc.flags.ignore\_links from true.
    - Set workspace\_doc.flags.ignore\_validate from true.
    - Set workspace\_doc.public from 0 when disable, otherwise 1.
      - Value choice on disable — true gives 0, false gives 1.
    - Evaluate workspace\_doc.save().
  - On failure (Exception).
    - Evaluate Platform.clear\_messages().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L5858) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1126) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L73)

<a id="op-35df12991a4ebc"></a>
### Update Enterprise roles

`operation_workforce_subscription_utils_business_behavior_update_enterprise_roles`

**Inputs** disable = true.

**Record and data access** resolve a document from “Role” via get\_doc.

**State and service calls** call save on role\_doc.

**Local steps**

- Set roles from get\_Enterprise\_roles().
- For each role in roles.
  - Attempt the following.
    - Set role\_doc from Platform.get\_doc(“Role”, role).
    - Set role\_doc.disabled from disable.
    - Set role\_doc.flags.ignore\_links from true.
    - Evaluate role\_doc.save().
  - On failure (Exception).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L6134) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1125) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L72)

<a id="op-64e1d22f860f26"></a>
### Set app logo

`operation_workforce_subscription_utils_business_behavior_set_application_logo`

**Inputs** no declared parameters.

**State and service calls** request set\_single\_value on “Navbar Settings”.

**Local steps**

- Evaluate Platform.db.set\_single\_value(“Navbar Settings”, “app\_logo”, “/assets/Workforce/images/Platform-hr-logo.svg”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L6329) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1122) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L69)

<a id="op-9306e6d6f83349"></a>
### Get Enterprise roles

`operation_workforce_subscription_utils_business_behavior_get_enterprise_roles`

**Inputs** no declared parameters.

**Declared result** set.

**Explicit results** ((Enterprise\_roles − Workforce\_roles) − set(STANDARD\_ROLES)).

**Local steps**

- Set Enterprise\_roles from get\_roles\_for\_app(“Enterprise”).
- Set Workforce\_roles from get\_roles\_for\_app(“Workforce”).
- Return ((Enterprise\_roles − Workforce\_roles) − set(STANDARD\_ROLES)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L6397) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1115) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L62)

<a id="op-b623f7669bc08a"></a>
### Get roles for app

`operation_workforce_subscription_utils_business_behavior_get_roles_for_application`

**Inputs** app\_name.

**Declared result** set.

**Explicit results** roles.

**Local steps**

- Set Enterprise\_modules from get\_modules\_by\_app(app\_name).
- Set doctypes from get\_doctypes\_by\_modules(Enterprise\_modules).
- Set roles from roles\_by\_doctype(doctypes).
- Return roles.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L6511) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1118) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L65)

<a id="op-a6402a3faa44d0"></a>
### Get modules by app

`operation_workforce_subscription_utils_business_behavior_get_modules_by_application`

**Inputs** app\_name.

**Declared result** list.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** Platform.db.get\_all(“Module Def”, filters = mapping(“app\_name” → app\_name), pluck = “name”).

**Local steps**

- Return Platform.db.get\_all(“Module Def”, filters = mapping(“app\_name” → app\_name), pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0154.json#L6637) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1116) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L63)

<a id="op-51908c29d8e7b0"></a>
### Get doctypes by modules

`operation_workforce_subscription_utils_business_behavior_get_record_types_by_modules`

**Inputs** modules.

**Declared result** list.

**Record and data access** read “DocType” via get\_all.

**Explicit results** Platform.db.get\_all(“DocType”, filters = list(list(“module”, “in”, modules)), pluck = “name”).

**Local steps**

- Return Platform.db.get\_all(“DocType”, filters = list(list(“module”, “in”, modules)), pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1117) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L64)

<a id="op-3eec7514790331"></a>
### Roles by doctype

`operation_workforce_subscription_utils_business_behavior_roles_by_record_type`

**Inputs** doctypes.

**Declared result** set.

**Explicit results** set(roles).

**Local steps**

- Set roles from list().
- For each d in doctypes.
  - Set permissions from Platform.get\_meta(d).permissions.
  - For each d in permissions.
    - Evaluate roles.append(d.role).
- Return set(roles).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L123) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1121) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L68)

<a id="op-fc20ffba4a55b6"></a>
### Hide Enterprise

`operation_workforce_subscription_utils_business_behavior_hide_enterprise`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set hr\_subscription from has\_subscription(Platform.conf.sk\_Workforce).
- Set Enterprise\_subscription from has\_subscription((Platform.conf.sk\_Enterprise\_smb or Platform.conf.sk\_Enterprise)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.sk\_Enterprise\_smb → Platform.conf.sk\_Enterprise.
- If not hr\_subscription.
  - Return false.
- If (hr\_subscription and Enterprise\_subscription).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hr\_subscription → Enterprise\_subscription.
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L283) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1120) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L67)

<a id="op-fd1de3961e6d00"></a>
### Has subscription

`operation_workforce_subscription_utils_business_behavior_has_subscription`

**Inputs** secret\_key.

**Declared result** bool.

**Explicit results** true when status equals “Active”, otherwise false.

**Local steps**

- Set url from text in the contract.
- Set response from requests.post(url, data = mapping(“secret\_key” → secret\_key), timeout = 5).
- Set status from response.json().get(“message”).
- Return true when status equals “Active”, otherwise false.
  - Value choice on status equals “Active” — true gives true, false gives false.

**Values supplied outside this operation** service or queued work from requests.post(url, data = mapping(“secret\_key” → secret\_key), timeout = 5).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L18) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1119) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L66)

## Service · Telemetry

<a id="op-e5da88660770d4"></a>
### Skip context

`operation_workforce_telemetry_business_behavior_skip_context`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool((Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_patch or Platform.flags.in\_test or Platform.flags.in\_import)).

**Local steps**

- Return bool((Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_patch or Platform.flags.in\_test or Platform.flags.in\_import)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate → Platform.flags.in\_patch → Platform.flags.in\_test → Platform.flags.in\_import.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0155.json#L639) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1144) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L91)
