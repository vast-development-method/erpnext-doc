# Forms, reports and navigation · operations 56

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Session

<a id="op-dd2ae5a434105d"></a>
### AISession.row to message

`operation_foundation_binding_foundation_studio_ai_session_aisession_row_to_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** row.

**Explicit result forms** a structured result.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L199) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1862)

<a id="op-dbd6ccebe73cec"></a>
### AISession.get messages

`operation_foundation_binding_foundation_studio_ai_session_aisession_get_messages`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1854)

<a id="op-c19948a3c03442"></a>
### AISession.build context messages

`operation_foundation_binding_foundation_studio_ai_session_aisession_build_context_messages`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1873) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1849)

<a id="op-49a70bae3038f5"></a>
### AISession.plan context content

`operation_foundation_binding_foundation_studio_ai_session_aisession_plan_context_content`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** headline, metadata\_json.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L198) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1861)

<a id="op-125ed5b86a91e1"></a>
### AISession.append message

`operation_foundation_binding_foundation_studio_ai_session_aisession_append_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, role, content, message\_type, task\_type, component\_id, metadata.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L185) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1848)

<a id="op-8e1e786328aae1"></a>
### AISession.update last assistant metadata

`operation_foundation_binding_foundation_studio_ai_session_aisession_update_last_assistant_metadata`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, extra\_metadata.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L203) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1866)

<a id="op-983fc5d47c0319"></a>
### AISession.set running

`operation_foundation_binding_foundation_studio_ai_session_aisession_set_running`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L201) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1864)

<a id="op-7b81de9de6a021"></a>
### AISession.clear running

`operation_foundation_binding_foundation_studio_ai_session_aisession_clear_running`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1876) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1852)

<a id="op-eba67b339a3208"></a>
### AISession.is session running

`operation_foundation_binding_foundation_studio_ai_session_aisession_is_session_running`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, session\_id.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1857)

<a id="op-b9152cf3abb5d5"></a>
### AISession.clear

`operation_foundation_binding_foundation_studio_ai_session_aisession_clear`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1851)

## Service · Settings map

<a id="op-fd3385db0f5a2c"></a>
### Has settings map

`operation_foundation_desk_record_type_settings_settings_map_business_behavior_has_settings_map`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** bool.

**Record and data access** read “DocType Settings Map” via exists.

**Explicit results** false · bool(Platform.db.exists(“DocType Settings Map”, mapping(“applies\_to\_doctype” → doctype, “is\_active” → 1))).

**Local steps**

- If not Platform.has\_permission(doctype, “read”).
  - Return false.
- Return bool(Platform.db.exists(“DocType Settings Map”, mapping(“applies\_to\_doctype” → doctype, “is\_active” → 1))).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L3967) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1369)

<a id="op-4a6129cd4f14f9"></a>
### Get settings map

`operation_foundation_desk_record_type_settings_settings_map_business_behavior_get_settings_map`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “DocType” via exists · read “DocType Settings Map” via get\_all · resolve a document from “DocType Settings Map” via get\_cached\_doc · resolve a document from single via get\_cached\_doc.

**Explicit results** list() · groups.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “DocType {0} not found”.format(doctype) · validation helper with Platform.PermissionError — translated “You are not permitted to access {0}.”.format(doctype).

**Local steps**

- If not Platform.db.exists(“DocType”, doctype).
  - Call the validation error handler Platform.throw(translated “DocType {0} not found”.format(doctype), Platform.DoesNotExistError).
- If not Platform.has\_permission(doctype, “read”).
  - Call the validation error handler Platform.throw(translated “You are not permitted to access {0}.”.format(doctype), Platform.PermissionError).
- Set active from Platform.get\_all(“DocType Settings Map”, filters = mapping(“applies\_to\_doctype” → doctype, “is\_active” → 1), fields = list(“name”), order\_by = “is\_standard asc”, limit = 1).
- If not active.
  - Return list().
- Set mappings from Platform.get\_cached\_doc(“DocType Settings Map”, active at 0.name).mappings.
- Set by\_single from mapping().
- For each row in mappings.
  - If (row.settings\_doctype and row.setting\_field).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.settings\_doctype → row.setting\_field.
    - Evaluate by\_single.setdefault(row.settings\_doctype, list()).append(row.setting\_field).
- Set groups from list().
- For each tuple(single, fieldnames) in by\_single.items().
  - Set single\_meta from Platform.get\_meta(single).
  - If (not single\_meta.issingle or not Platform.has\_permission(single, “read”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not single\_meta.issingle → not Platform.has\_permission(single, “read”).
    - Continue with the next iteration or loop test.
  - Set doc\_write from bool(Platform.has\_permission(single, “write”)).
  - Set read\_levels from single\_meta.get\_permlevel\_access(“read”).
  - Set write\_levels from single\_meta.get\_permlevel\_access(“write”).
  - Set doc from Platform.get\_cached\_doc(single).
  - Set fields from list().
  - For each fieldname in fieldnames.
    - Set df from single\_meta.get\_field(fieldname).
    - If (not df or df.fieldtype belongs to no\_value\_fields).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → df.fieldtype belongs to no\_value\_fields.
      - Continue with the next iteration or loop test.
    - Set permlevel from (df.permlevel or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.permlevel → 0.
    - If permlevel does not belong to read\_levels.
      - Continue with the next iteration or loop test.
    - Evaluate fields.append(mapping(“fieldname” → df.fieldname, “label” → \_(df.label, context = single) when df.label, otherwise df.fieldname, “fieldtype” → df.fieldtype, “options” → df.options, …)).
      - Value choice on df.label — true gives \_(df.label, context = single), false gives df.fieldname.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.description → \_(df.description, context = single).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_write → permlevel belongs to write\_levels.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“depends\_on”) → no value.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.get(“read\_only\_depends\_on”) → no value.
  - If not fields.
    - Continue with the next iteration or loop test.
  - Set doc\_context from mapping of f.fieldname → doc.get(f.fieldname) for f drawn from single\_meta.fields where ((f.permlevel or 0) belongs to read\_levels and f.fieldtype does not belong to no\_value\_fields).
    - Draw f from single\_meta.fields, keep a combination only if (((f.permlevel or 0) belongs to read\_levels and f.fieldtype does not belong to no\_value\_fields)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (f.permlevel or 0) belongs to read\_levels → f.fieldtype does not belong to no\_value\_fields.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in f.permlevel → 0.
  - Evaluate groups.append(mapping(“settings” → single, “label” → translated single, “doc” → doc\_context, “fields” → fields)).
- Return groups.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”), Platform.has\_permission(single, “read”) and 1 further calls · configured or stored value from Platform.get\_cached\_doc(“DocType Settings Map”, active at 0.name), Platform.get\_cached\_doc(single).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L49) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1368)

## Workspace · Setup wizard

<a id="op-5bddcf1755b575"></a>
### Unnamed value

`operation_foundation_binding_foundation_desk_page_setup_wizard_install_fixtures`

**Inputs** x, remaining positional values args, remaining named values kwargs.

**Explicit results** x.

**Local steps**

- Return x.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L793)

<a id="op-c109db2000d905"></a>
### Install

`operation_foundation_desk_page_setup_wizard_install_fixtures_business_behavior_install`

**Inputs** no declared parameters.

**Local steps**

- Evaluate update\_genders().
- Evaluate update\_salutations().
- Evaluate update\_global\_search\_doctypes().
- Evaluate sync\_dashboards().
- Evaluate add\_unsubscribe().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L1573) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L371)

<a id="op-5381006a326810"></a>
### Update genders

`operation_foundation_desk_page_setup_wizard_install_fixtures_business_behavior_update_genders`

**Inputs** no declared parameters.

**State and service calls** request new\_doc for “Gender” · call insert on doc.

**Local steps**

- For each gender in tuple(translated “Male”, translated “Female”, translated “Other”, translated “Transgender”, …).
  - Set doc from Platform.new\_doc(“Gender”).
  - Set doc.gender from gender.
  - Evaluate doc.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L91) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L372)

<a id="op-8b370131ce0676"></a>
### Update salutations

`operation_foundation_desk_page_setup_wizard_install_fixtures_business_behavior_update_salutations`

**Inputs** no declared parameters.

**State and service calls** request new\_doc for “Salutation” · call insert on doc.

**Local steps**

- For each salutation in tuple(translated “Mr”, translated “Ms”, translated “Mx”, translated “Dr”, …).
  - Set doc from Platform.new\_doc(“Salutation”).
  - Set doc.salutation from salutation.
  - Evaluate doc.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L92) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L373)

<a id="op-aed6eb3f696b3d"></a>
### Add unsubscribe

`operation_foundation_desk_page_setup_wizard_install_fixtures_business_behavior_add_unsubscribe`

**Inputs** no declared parameters.

**Record and data access** read “Email Unsubscribe” via get\_all.

**State and service calls** request new\_doc for “Email Unsubscribe” · call insert on doc.

**Local steps**

- For each unsubscribe in list(mapping(“email” → “admin@example.com”, “global\_unsubscribe” → 1), mapping(“email” → “guest@example.com”, “global\_unsubscribe” → 1)).
  - If not Platform.get\_all(“Email Unsubscribe”, filters = unsubscribe).
    - Set doc from Platform.new\_doc(“Email Unsubscribe”).
    - Evaluate doc.update(unsubscribe).
    - Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L2206) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L370)

<a id="op-d2f037013f6b04"></a>
### Site requires builtin wizard

`operation_foundation_desk_page_setup_wizard_business_behavior_site_requires_builtin_wizard`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- For each app in Platform.get\_installed\_apps().
  - Set hooks from Platform.get\_hooks(app\_name = app).
  - If (hooks.get(“setup\_wizard\_stages”) or hooks.get(“setup\_wizard\_complete”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks.get(“setup\_wizard\_stages”) → hooks.get(“setup\_wizard\_complete”).
    - Return true.
- Return false.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L88) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L366)

<a id="op-23a6e2fdf71208"></a>
### Get setup wizard url

`operation_foundation_desk_page_setup_wizard_business_behavior_get_setup_wizard_resource_address`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** urls at negative 1 · “/app/setup-wizard”.

**Local steps**

- Set urls from Platform.get\_hooks(“setup\_wizard\_url”).
- If (urls and not site\_requires\_builtin\_wizard()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in urls → not site\_requires\_builtin\_wizard().
  - Return urls at negative 1.
- Return “/app/setup-wizard”.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“setup\_wizard\_url”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L84) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L346)

<a id="op-770c1028c0e2d1"></a>
### Get setup stages

`operation_foundation_desk_page_setup_wizard_business_behavior_get_setup_stages`

**Inputs** args, include\_app\_input\_stages = true.

**Explicit results** stages.

**Local steps**

- Set stages from list(mapping(“status” → translated “Saving your language and region”, “fail\_msg” → translated “We couldn't save your language and region”, “tasks” → list(mapping(“fn” → update\_global\_settings, “args” → args, “f …).
- If include\_app\_input\_stages.
  - Update stages using + get\_stages\_hooks(args).
- Update stages using + get\_setup\_complete\_hooks(args).
- Evaluate stages.append(mapping(“status” → translated “Almost done”, “fail\_msg” → translated “We couldn't finish setting things up”, “tasks” → list(mapping(“fn” → run\_post\_setup\_complete, “args” → args, “fail\_msg” → ….
- Return stages.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L83) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L345)

<a id="op-fc3e1ff86282bf"></a>
### Setup complete

`operation_foundation_desk_page_setup_wizard_business_behavior_setup_complete`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“status” → “ok”) · process\_setup\_stages(stages, kwargs).

**Local steps**

- Attempt the following.
  - Within filelock(“setup\_wizard”, timeout = 0.5).
    - If Platform.is\_setup\_complete().
      - Return mapping(“status” → “ok”).
    - Set kwargs from parse\_args(sanitize\_input(args)).
    - Set stages from get\_setup\_stages(kwargs).
    - Return process\_setup\_stages(stages, kwargs).
- On failure (LockTimeoutError).
  - Return mapping(“status” → “ok”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L3108) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L364)

<a id="op-a3b505ccbf4fcf"></a>
### Complete prefilled setup

`operation_foundation_binding_foundation_desk_page_setup_wizard_setup_wizard_complete_prefilled_setup`

**Inputs** login\_manager = no value.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- Set args from get\_prefilled\_setup\_args().
- If not args.
  - Return no value.
- Evaluate Platform.db.commit(chain = true).
- Set Platform.local.flags.commit from true.
- Attempt the following.
  - Evaluate complete\_app\_setup(expanded names args).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Setup from the saved region failed”).
  - Evaluate Platform.db.set\_default(PREFILLED\_SETUP\_FAILED, 1).
  - Evaluate Platform.clear\_messages().
  - Evaluate Platform.response.pop(“setup\_wizard\_failure\_message”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L794)

<a id="op-4f07ce66f9f831"></a>
### Get prefilled setup args

`operation_foundation_binding_foundation_desk_page_setup_wizard_setup_wizard_get_prefilled_setup_args`

**Inputs** no declared parameters.

**Declared result** (dict bitwise or no value).

**Record and data access** read “System Settings” via get\_single · read “Language” via get\_value.

**Explicit results** no value · mapping(“country” → settings.country, “currency” → settings.currency, “timezone” → settings.time\_zone, “language” → (Platform.db.get\_value(“Language”, settings.language, “language\_name”) or “English”), …).

**Local steps**

- Bind dependencies has\_non\_admin\_user.
- Bind dependencies is\_v2\_site.
- If (Platform.is\_setup\_complete() or Platform.conf.skip\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.is\_setup\_complete() → Platform.conf.skip\_setup\_wizard.
  - Return no value.
- If not any(Platform.get\_hooks(“setup\_wizard\_auto\_complete”)).
  - Return no value.
- If Platform.db.get\_default(PREFILLED\_SETUP\_FAILED).
  - Return no value.
- If “System Manager” does not belong to Platform.get\_roles().
  - Return no value.
- If (Platform.get\_hooks(“setup\_wizard\_url”) or site\_requires\_builtin\_wizard()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“setup\_wizard\_url”) → site\_requires\_builtin\_wizard().
  - Return no value.
- Set settings from Platform.get\_single(“System Settings”).
- Set prefilled from (settings.country and settings.time\_zone and settings.currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in settings.country → settings.time\_zone → settings.currency.
- If (not has\_non\_admin\_user() or not (prefilled or is\_v2\_site())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not has\_non\_admin\_user() → not (prefilled or is\_v2\_site()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in prefilled → is\_v2\_site().
  - Return no value.
- Return mapping(“country” → settings.country, “currency” → settings.currency, “timezone” → settings.time\_zone, “language” → (Platform.db.get\_value(“Language”, settings.language, “language\_name”) or “English”), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Language”, settings.language, “language\_name”) → “English”.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“setup\_wizard\_auto\_complete”), Platform.get\_hooks(“setup\_wizard\_url”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L795)

<a id="op-18fa66fbe5439c"></a>
### Complete app setup

`operation_foundation_desk_page_setup_wizard_business_behavior_complete_application_setup`

**Inputs** country = no value, currency = no value, timezone = no value, language = no value, enable\_telemetry = no value, allow\_recording\_first\_session = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** mapping(“status” → “ok”) · process\_setup\_stages(stages, args).

**Explicit failure paths** validation helper — translated “This site's setup must run through the built-in wizard.” · validation helper — translated “Setup is already in progress. Please try again in a moment.”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If site\_requires\_builtin\_wizard().
  - Call the validation error handler Platform.throw(translated “This site's setup must run through the built-in wizard.”).
- Attempt the following.
  - Within filelock(“setup\_wizard”, timeout = 0.5).
    - If Platform.is\_setup\_complete().
      - Return mapping(“status” → “ok”).
    - Set args from parse\_args(sanitize\_input(mapping(“country” → country, “currency” → currency, “timezone” → timezone, “language” → language, …))).
    - Set stages from get\_setup\_stages(args, include\_app\_input\_stages = false).
    - Return process\_setup\_stages(stages, args).
- On failure (LockTimeoutError).
  - If Platform.is\_setup\_complete().
    - Return mapping(“status” → “ok”).
  - Call the validation error handler Platform.throw(translated “Setup is already in progress. Please try again in a moment.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0207.json#L3413) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L336)
