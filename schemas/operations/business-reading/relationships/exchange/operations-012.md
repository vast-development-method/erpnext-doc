# Integrations and service calls · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Twilio handler

<a id="op-b9f3887462729f"></a>
### Get active loggedin users

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_get_active_loggedin_users`

**Inputs** users.

**Record and data access** execute query text (SELECT, Sessions).

**Explicit results** list of row at 0 for row drawn from set(rows).

**Local steps**

- Set rows from Platform.db.sql(query text (SELECT, Sessions), mapping(“users” → users)).
- Return list of row at 0 for row drawn from set(rows).
  - Draw row from set(rows).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L1962) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1358) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1334)

<a id="op-cb429d745abd53"></a>
### Get the call attender

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_get_the_call_attender`

**Inputs** owners, caller = no value.

**Record and data access** read “CRM Deal” via get\_value · read “CRM Lead” via get\_value.

**Explicit results** no value · details.

**Local steps**

- If not owners.
  - Return no value.
- Set current\_loggedin\_users from get\_active\_loggedin\_users(list(owners.keys())).
- If (len(current\_loggedin\_users) &gt; 1 and caller).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(current\_loggedin\_users) &gt; 1 → caller.
  - Set deal\_owner from Platform.db.get\_value(“CRM Deal”, mapping(“mobile\_no” → caller), “deal\_owner”).
  - If not deal\_owner.
    - Set deal\_owner from Platform.db.get\_value(“CRM Lead”, mapping(“mobile\_no” → caller, “converted” → false), “lead\_owner”).
  - For each user in current\_loggedin\_users.
    - If user equals deal\_owner.
      - Set current\_loggedin\_users from list(user).
- For each tuple(name, details) in owners.items().
  - If ((details at “call\_receiving\_device” equals “Phone” and details at “mobile\_no”) or (details at “call\_receiving\_device” equals “Computer” and name belongs to current\_loggedin\_users)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (details at “call\_receiving\_device” equals “Phone” and details at “mobile\_no”) → (details at “call\_receiving\_device” equals “Computer” and name belongs to current\_loggedin\_users).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in details at “call\_receiving\_device” equals “Phone” → details at “mobile\_no”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in details at “call\_receiving\_device” equals “Computer” → name belongs to current\_loggedin\_users.
    - Return details.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L2125) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1359) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1335)

<a id="op-8df4399ba4af52"></a>
### Twilio Call Details.initialize

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_call_details_initialize`

**Inputs** self, call\_info, call\_from = no value, call\_to = no value.

**Local steps**

- Set self.call\_info from call\_info.
- Set self.account\_sid from call\_info.get(“AccountSid”).
- Set self.application\_sid from call\_info.get(“ApplicationSid”).
- Set self.call\_sid from call\_info.get(“CallSid”).
- Set self.call\_status from self.get\_call\_status(call\_info.get(“CallStatus”)).
- Set self.\_call\_from from (call\_from or call\_info.get(“From”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_from → call\_info.get(“From”).
- Set self.\_call\_to from (call\_to or call\_info.get(“To”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in call\_to → call\_info.get(“To”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get call status](operations-012.md#op-09390e9145b579).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L2655) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1367) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1343)

<a id="op-35aeadcf0ef59a"></a>
### Twilio Call Details.get direction

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_call_details_get_direction`

**Inputs** self.

**Explicit results** “Outgoing” · “Incoming”.

**Local steps**

- If nested operand in the contract.call\_info.get(“Caller”).lower().startswith(“client”).
  - Return “Outgoing”.
- Return “Incoming”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L2964) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1364) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1340)

<a id="op-e607f41f4f49e8"></a>
### Twilio Call Details.get from number

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_call_details_get_from_number`

**Inputs** self.

**Explicit results** (self.\_call\_from or self.call\_info.get(“From”)).

**Local steps**

- Return (self.\_call\_from or self.call\_info.get(“From”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_call\_from → self.call\_info.get(“From”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L3071) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1365) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1341)

<a id="op-28f05fad47cfae"></a>
### Twilio Call Details.get to number

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_call_details_get_to_number`

**Inputs** self.

**Explicit results** (self.\_call\_to or self.call\_info.get(“To”)).

**Local steps**

- Return (self.\_call\_to or self.call\_info.get(“To”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_call\_to → self.call\_info.get(“To”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L3143) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1366) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1342)

<a id="op-09390e9145b579"></a>
### Twilio Call Details.get call status

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_call_details_get_call_status`

**Inputs** cls, twilio\_status.

**Wrappers, in declaration order** classmethod.

**Explicit results** one space.join(twilio\_status.split(“-”)).title().

**Local steps**

- Set twilio\_status from (twilio\_status or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in twilio\_status → empty text.
- Return one space.join(twilio\_status.split(“-”)).title().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L3215) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1363) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1339)

<a id="op-575675bb289240"></a>
### Twilio Call Details.to dict

`operation_relationships_integrations_twilio_twilio_handler_business_behavior_twilio_call_details_to_mapping`

**Inputs** self.

**Explicit results** mapping(“type” → direction, “status” → self.call\_status, “id” → self.call\_sid, “from” → from\_number, …).

**Local steps**

- Set direction from self.get\_direction().
- Set from\_number from self.get\_from\_number().
- Set to\_number from self.get\_to\_number().
- Set caller from empty text.
- Set receiver from empty text.
- If direction equals “Outgoing”.
  - Set caller from self.call\_info.get(“Caller”).
  - Set identity from caller.replace(“client:”, empty text).strip().
  - Set caller from Twilio.emailid\_from\_identity(identity) when identity, otherwise empty text.
    - Value choice on identity — true gives Twilio.emailid\_from\_identity(identity), false gives empty text.
- Otherwise.
  - Set owners from get\_twilio\_number\_owners(to\_number).
  - Set attender from get\_the\_call\_attender(owners, from\_number).
  - Set receiver from attender at “name” when attender, otherwise empty text.
    - Value choice on attender — true gives attender at “name”, false gives empty text.
- Return mapping(“type” → direction, “status” → self.call\_status, “id” → self.call\_sid, “from” → from\_number, …).

**Methods declared on this owner** [get direction](operations-012.md#op-35aeadcf0ef59a), [get from number](operations-012.md#op-e607f41f4f49e8), [get to number](operations-012.md#op-28f05fad47cfae).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L3331) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1368) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1344)

## Service · User

<a id="op-644676371b6941"></a>
### Change password

`operation_relationships_application_interface_user_business_behavior_change_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** old\_password, new\_password.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** validation or user-notification service.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L157) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L155) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L136)

<a id="op-266c5d6323f569"></a>
### Needs password setup

`operation_relationships_application_interface_user_business_behavior_needs_password_setup`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L16) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L157) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L138)

<a id="op-2fbae97f7ae0eb"></a>
### Has password

`operation_relationships_application_interface_user_business_behavior_has_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L1160) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L156) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L137)

<a id="op-3639b4d43a7b17"></a>
### Add existing users

`operation_relationships_application_interface_user_business_behavior_add_existing_users`

**Inputs** users, role = “Sales User”.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Only System Managers can assign the System Manager role” · validation helper with Platform.PermissionError — translated “Only System Managers can assign the Sales Manager role”.

**Local steps**

- Evaluate Platform.only\_for(list(“System Manager”, “Sales Manager”), true).
- Set is\_system\_manager from “System Manager” belongs to Platform.get\_roles().
- If (role equals “System Manager” and not is\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in role equals “System Manager” → not is\_system\_manager.
  - Call the validation error handler Platform.throw(translated “Only System Managers can assign the System Manager role”, Platform.PermissionError).
- If (role equals “Sales Manager” and not is\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in role equals “Sales Manager” → not is\_system\_manager.
  - Call the validation error handler Platform.throw(translated “Only System Managers can assign the Sales Manager role”, Platform.PermissionError).
- Set users from Platform.parse\_json(users).
- For each user in users.
  - Evaluate update\_user\_role(user, role).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(list(“System Manager”, “Sales Manager”), true), Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L1435) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L154) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L135)

<a id="op-9d66594b89fa97"></a>
### Update user role

`operation_relationships_application_interface_user_business_behavior_update_user_role`

**Inputs** user, new\_role.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “User” via get\_doc · read “CRM Sales Hierarchy” via get\_value · read “CRM Sales Hierarchy” via exists.

**State and service calls** call save on user\_doc.

**Explicit failure paths** validation helper — translated “Cannot assign this role” · validation helper with Platform.PermissionError — translated “Only System Managers can assign the System Manager role” · validation helper with Platform.PermissionError — translated “Only System Managers can modify other System Managers” · validation helper with Platform.PermissionError — translated “Only System Managers can assign the Sales Manager role” · validation helper — translated “Remove this user from the sales hierarchy before changing their role to Sales User”.

**Local steps**

- Evaluate Platform.only\_for(list(“System Manager”, “Sales Manager”), true).
- Set is\_system\_manager from “System Manager” belongs to Platform.get\_roles().
- If new\_role does not belong to list(“System Manager”, “Sales Manager”, “Sales User”).
  - Call the validation error handler Platform.throw(translated “Cannot assign this role”).
- Set user\_doc from Platform.get\_doc(“User”, user).
- Evaluate validate\_no\_role\_profile(user\_doc).
- Set target\_roles from list of d.role for d drawn from user\_doc.roles.
  - Draw d from user\_doc.roles.
- Set target\_is\_system\_manager from “System Manager” belongs to target\_roles.
- If (new\_role equals “System Manager” and not is\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_role equals “System Manager” → not is\_system\_manager.
  - Call the validation error handler Platform.throw(translated “Only System Managers can assign the System Manager role”, Platform.PermissionError).
- If (target\_is\_system\_manager and not is\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_is\_system\_manager → not is\_system\_manager.
  - Call the validation error handler Platform.throw(translated “Only System Managers can modify other System Managers”, Platform.PermissionError).
- If (new\_role equals “Sales Manager” and not is\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in new\_role equals “Sales Manager” → not is\_system\_manager.
  - Call the validation error handler Platform.throw(translated “Only System Managers can assign the Sales Manager role”, Platform.PermissionError).
- If new\_role equals “System Manager”.
  - Evaluate user\_doc.append\_roles(“System Manager”, “Sales Manager”, “Sales User”).
  - Evaluate user\_doc.set(“block\_modules”, list()).
- If new\_role equals “Sales Manager”.
  - Evaluate user\_doc.append\_roles(“Sales Manager”, “Sales User”).
  - Evaluate remove\_roles(user\_doc, “System Manager”).
- If new\_role equals “Sales User”.
  - Set node from Platform.db.get\_value(“CRM Sales Hierarchy”, mapping(“user” → user), list(“name”, “reports\_to”), as\_dict = true).
  - If node.
    - Set has\_reports from Platform.db.exists(“CRM Sales Hierarchy”, mapping(“reports\_to” → node.name)).
    - If (has\_reports or not node.reports\_to).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_reports → not node.reports\_to.
      - Call the validation error handler Platform.throw(translated “Remove this user from the sales hierarchy before changing their role to Sales User”).
  - Evaluate user\_doc.append\_roles(“Sales User”).
  - Evaluate remove\_roles(user\_doc, “Sales Manager”, “System Manager”).
  - Evaluate update\_module\_in\_user(user\_doc, “FCRM”).
- Evaluate user\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(list(“System Manager”, “Sales Manager”), true), Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L18) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L161) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L142)

<a id="op-f27d5f18a97330"></a>
### Remove crm roles from user

`operation_relationships_application_interface_user_business_behavior_remove_customer_relationship_roles_from_user`

**Inputs** user.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “User” via get\_doc · read “CRM Sales Hierarchy” via get\_value.

**State and service calls** call save on user\_doc · request delete\_doc for “CRM Sales Hierarchy” · msgprint with translated “User {0} has been removed from CRM roles.”.format(user).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You cannot remove yourself.” · validation helper with Platform.PermissionError — translated “Only System Managers can modify other System Managers”.

**Local steps**

- Evaluate Platform.only\_for(list(“System Manager”, “Sales Manager”), true).
- If user equals Platform.session.user.
  - Call the validation error handler Platform.throw(translated “You cannot remove yourself.”, Platform.PermissionError).
- Set user\_doc from Platform.get\_doc(“User”, user).
- Set roles from list of d.role for d drawn from user\_doc.roles.
  - Draw d from user\_doc.roles.
- Set current\_user\_is\_system\_manager from “System Manager” belongs to Platform.get\_roles().
- If (“System Manager” belongs to roles and not current\_user\_is\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “System Manager” belongs to roles → not current\_user\_is\_system\_manager.
  - Call the validation error handler Platform.throw(translated “Only System Managers can modify other System Managers”, Platform.PermissionError).
- Evaluate validate\_no\_role\_profile(user\_doc).
- If “Sales User” belongs to roles.
  - Evaluate remove\_roles(user\_doc, “Sales User”).
- If “Sales Manager” belongs to roles.
  - Evaluate remove\_roles(user\_doc, “Sales Manager”).
- If (“System Manager” belongs to roles and current\_user\_is\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “System Manager” belongs to roles → current\_user\_is\_system\_manager.
  - Evaluate remove\_roles(user\_doc, “System Manager”).
  - Evaluate update\_module\_in\_user(user\_doc, “FCRM”).
- Evaluate user\_doc.save(ignore\_permissions = true).
- Set node\_name from Platform.db.get\_value(“CRM Sales Hierarchy”, mapping(“user” → user), “name”).
- If node\_name.
  - Evaluate Platform.delete\_doc(“CRM Sales Hierarchy”, node\_name, ignore\_permissions = true).
- Evaluate Platform.msgprint(translated “User {0} has been removed from CRM roles.”.format(user)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(list(“System Manager”, “Sales Manager”), true), Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L17) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L158) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L139)

<a id="op-76611c56f6ea9d"></a>
### Validate no role profile

`operation_relationships_binding_crm_api_user_validate_no_role_profile`

**Inputs** user\_doc.

**Explicit failure paths** validation helper — translated “Roles of user {0} are managed by a Role Profile. Update the Role Profile instead.”.format(Platform.bold(user\_doc.name)).

**Local steps**

- If (user\_doc.get(“role\_profiles”) or user\_doc.get(“role\_profile\_name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_doc.get(“role\_profiles”) → user\_doc.get(“role\_profile\_name”).
  - Call the validation error handler Platform.throw(translated “Roles of user {0} are managed by a Role Profile. Update the Role Profile instead.”.format(Platform.bold(user\_doc.name)), title = translated “Role Profile Assigned”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L66) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L222) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L203)

<a id="op-e886367917d5f4"></a>
### Remove roles

`operation_relationships_application_interface_user_business_behavior_remove_roles`

**Inputs** self, remaining positional values roles.

**Local steps**

- Set existing\_roles from mapping of d.role → d for d drawn from self.get(“roles”).
  - Draw d from self.get(“roles”).
- For each role in roles.
  - If role belongs to existing\_roles.
    - Evaluate self.get(“roles”).remove(existing\_roles at role).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L3748) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L159) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L140)

<a id="op-275deafd637a58"></a>
### Update module in user

`operation_relationships_application_interface_user_business_behavior_update_module_in_user`

**Inputs** user, module.

**Record and data access** read “Module Def” via get\_all.

**Local steps**

- Set block\_modules from Platform.get\_all(“Module Def”, fields = list(“name as module”), filters = mapping(“name” → list(“!=”, module))).
- If block\_modules.
  - Evaluate user.set(“block\_modules”, block\_modules).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L3931) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L160) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L141)

## Service · User permission

<a id="op-a9181b4b4f7903"></a>
### Dedup extra

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_dedup_extra`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L364) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1315) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1291)

<a id="op-812f8e7e2dd72e"></a>
### Sync

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_sync`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L453) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1319) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1295)

<a id="op-97c73fb1c701ef"></a>
### Before validate

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_before_validate`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, method.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L533) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1314) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1290)

<a id="op-3276c2b62eedd5"></a>
### After insert

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_after_insert`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, method.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L700) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1313) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1289)

<a id="op-4e4c16a5410c45"></a>
### On update

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_on_update`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, method.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L808) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1318) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1294)

<a id="op-ed15b8694b022f"></a>
### On trash

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_on_trash`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, method.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L1005) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1317) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1293)

<a id="op-6505b0952af0ea"></a>
### Sync user permissions

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_sync_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L1200) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1320) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1296)
