# Record lifecycle and persistence · operations 99

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · User

[Record definition](../../../../data/record-types/user.json)

<a id="op-a557e454733cbb"></a>
### User.validate user email inbox

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_user_email_inbox`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Email Account added multiple times”.

**Local steps**

- Set email\_accounts from list of user\_email.email\_account for user\_email drawn from self.user\_emails.
  - Draw user\_email from self.user\_emails.
- If len(email\_accounts) differs from len(set(email\_accounts)).
  - Call the validation error handler Platform.throw(translated “Email Account added multiple times”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L223) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L734)

<a id="op-d540cfb09e43d9"></a>
### User.get social login userid

`operation_foundation_core_record_definitions_user_business_behavior_user_get_social_login_userid`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, provider.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 1 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L388) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L698)

<a id="op-02abc1252eebac"></a>
### User.set social login userid

`operation_foundation_core_record_definitions_user_business_behavior_user_set_social_login_userid`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, provider, userid, username.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L512) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L719)

<a id="op-45b7235e433661"></a>
### User.set Platform social login userid

`operation_foundation_binding_foundation_core_doctype_user_user_user_set_foundation_social_login_userid`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L648)

<a id="op-216dee05eaecb3"></a>
### User.get restricted ip list

`operation_foundation_core_record_definitions_user_business_behavior_user_get_restricted_internet_protocol_list`

**Inputs** self.

**Explicit results** get\_restricted\_ip\_list(self).

**Local steps**

- Return get\_restricted\_ip\_list(self).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L680) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L697)

<a id="op-0f948ad00663a6"></a>
### User.find by credentials

`operation_foundation_core_record_definitions_user_business_behavior_user_find_by_credentials`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, user\_name, password, validate\_password.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L732) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L693)

<a id="op-828b94a5793d0f"></a>
### User.set time zone

`operation_foundation_core_record_definitions_user_business_behavior_user_set_time_zone`

**Inputs** self.

**Local steps**

- If not self.time\_zone.
  - Set self.time\_zone from get\_system\_timezone().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L1287) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L721)

<a id="op-c0d4965e22de13"></a>
### User.get permission log options

`operation_foundation_core_record_definitions_user_business_behavior_user_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L1362) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L696)

<a id="op-3f689dba4e8dad"></a>
### User.check roles added

`operation_foundation_core_record_definitions_user_business_behavior_user_check_roles_added`

**Inputs** self.

**State and service calls** msgprint with translated “Newly created user {0} has no roles enabled.”.format(Platform.bold(self.name)).

**Explicit results** no value.

**Local steps**

- If (self.user\_type differs from “System User” or self.roles or not self.is\_new()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.user\_type differs from “System User” → self.roles → not self.is\_new().
  - Return no value.
- Evaluate Platform.msgprint(translated “Newly created user {0} has no roles enabled.”.format(Platform.bold(self.name)), title = translated “No Roles Specified”, indicator = “orange”, primary\_action = mapping(“label” ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L53) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L688)

<a id="op-a5e7856df1ed59"></a>
### User.validate ip addr

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_internet_protocol_addr`

**Inputs** self.

**Local steps**

- Set self.restrict\_ip from “,”.join(self.get\_restricted\_ip\_list()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get restricted ip list](operations-099.md#op-216dee05eaecb3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L1746) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L731)

<a id="op-565d4b87d80979"></a>
### Get timezones

`operation_foundation_core_record_definitions_user_business_behavior_get_timezones`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“timezones” → \_get\_timezones()).

**Local steps**

- Return mapping(“timezones” → \_get\_timezones()).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L1824) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L661)

<a id="op-63b75291dfccf1"></a>
### Get timezones

`operation_foundation_core_record_definitions_user_business_behavior_get_timezones_2`

**Inputs** no declared parameters.

**Wrappers, in declaration order** lru\_cache(maxsize = 1).

**Explicit results** sorted(pytz.common\_timezones).

**Local steps**

- Bind dependencies pytz.
- Return sorted(pytz.common\_timezones).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L1892) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L662)

<a id="op-347866ee553e75"></a>
### Get all roles

`operation_foundation_core_record_definitions_user_business_behavior_get_all_roles`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** sorted(list of role.get(“name”) for role drawn from roles).

**Local steps**

- Set active\_domains from Platform.get\_active\_domains().
- Set Role from Platform.qb.DocType(“Role”).
- Set domain\_condition from (Role.restrict\_to\_domain.isnull() bitwise or Role.restrict\_to\_domain equals empty text).
- If active\_domains.
  - Set domain\_condition from (domain\_condition bitwise or Role.restrict\_to\_domain.isin(active\_domains)).
- Set roles from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and domain\_condition)).orderby(Role.name).run(as\_dict = true).
- Return sorted(list of role.get(“name”) for role drawn from roles).
  - Draw role from roles.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L1970) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L651)

<a id="op-9a72ab34649b62"></a>
### Get current user roles

`operation_foundation_core_record_definitions_user_business_behavior_get_current_user_roles`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** Platform.get\_roles().

**Local steps**

- Return Platform.get\_roles().

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L2408) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L652)

<a id="op-6ddb1514086eed"></a>
### Get perm info

`operation_foundation_core_record_definitions_user_business_behavior_get_permission_info`

**Inputs** role.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_all\_perms(role).

**Local steps**

- Bind dependencies get\_all\_perms.
- Return get\_all\_perms(role).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L2477) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L657)

<a id="op-1c9fa0d891e452"></a>
### Update password

`operation_foundation_core_record_definitions_user_business_behavior_update_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** new\_password, logout\_all\_sessions, key, old\_password.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** record mutation request, validation or user-notification service.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L49) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L677)

<a id="op-a76fa98c9dedb3"></a>
### Test password strength

`operation_foundation_core_record_definitions_user_business_behavior_test_password_strength`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** new\_password, key, old\_password, user\_data.

**Explicit result forms** a structured result, a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L48) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L675)

<a id="op-8711aefac3edfb"></a>
### Has email account

`operation_foundation_core_record_definitions_user_business_behavior_has_email_account`

**Inputs** email.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Email Account” via get\_list.

**Explicit results** Platform.get\_list(“Email Account”, filters = mapping(“email\_id” → email)).

**Local steps**

- Return Platform.get\_list(“Email Account”, filters = mapping(“email\_id” → email)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L4271) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L667)

<a id="op-0568bc041aa071"></a>
### Get email awaiting

`operation_foundation_core_record_definitions_user_business_behavior_get_email_awaiting`

**Inputs** user.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = false).

**Record and data access** read “User Email” via get\_all.

**Explicit results** Platform.get\_all(“User Email”, fields = list(“email\_account”, “email\_id”), filters = mapping(“awaiting\_password” → 1, “parent” → user, “used\_oauth” → 0)).

**Local steps**

- If user differs from Platform.session.user.
  - Evaluate Platform.has\_permission(“User”, “read”, doc = user, throw = true).
- Return Platform.get\_all(“User Email”, fields = list(“email\_account”, “email\_id”), filters = mapping(“awaiting\_password” → 1, “parent” → user, “used\_oauth” → 0)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“User”, “read”, doc = user, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L4378) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L653)

<a id="op-5d7ac3ae5a7420"></a>
### Ask pass update

`operation_foundation_core_record_definitions_user_business_behavior_ask_pass_update`

**Inputs** no declared parameters.

**Record and data access** read “User Email” via get\_all.

**Local steps**

- Bind dependencies set\_default.
- Set password\_list from Platform.get\_all(“User Email”, filters = mapping(“awaiting\_password” → 1, “used\_oauth” → 0), pluck = “parent”, distinct = true).
- Evaluate set\_default(“email\_user\_password”, “,”.join(password\_list)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L4641) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L644)

<a id="op-af336c4e8a436b"></a>
### Get user for update password

`operation_foundation_core_record_definitions_user_business_behavior_get_user_for_update_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** key, old\_password.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L4813) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L502) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L664)

<a id="op-34503c09170fde"></a>
### Reset user data

`operation_foundation_core_record_definitions_user_business_behavior_reset_user_data`

**Inputs** user.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user\_doc.

**Explicit results** tuple(user\_doc, redirect\_url).

**Local steps**

- Set user\_doc from Platform.get\_doc(“User”, user).
- Set redirect\_url from user\_doc.redirect\_url.
- Set user\_doc.reset\_password\_key from empty text.
- Set user\_doc.redirect\_url from empty text.
- Evaluate user\_doc.save(ignore\_permissions = true).
- Return tuple(user\_doc, redirect\_url).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L5327) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L672)

<a id="op-f101b076a3084b"></a>
### Verify password

`operation_foundation_core_record_definitions_user_business_behavior_verify_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** password.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L5491) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L737)

<a id="op-e4f1a823d060e6"></a>
### Sign up

`operation_foundation_core_record_definitions_user_business_behavior_sign_up`

**Inputs** email, full\_name, redirect\_to.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Declared result** tuple at tuple(int, str).

**Record and data access** resolve a document from mapping(“doctype” → “User”, “email” → email, “first\_name” → escape\_html(full\_name), “enabled” → 1, …) via get\_doc · read “Portal Settings” via get\_single\_value.

**State and service calls** call insert on user.

**Explicit results** tuple(0, translated “Already Registered”) · tuple(0, translated “Registered but disabled”) · tuple(1, translated “Please check your email for verification”) · tuple(2, translated “Please ask your administrator to verify your sign-up”).

**Explicit failure paths** validation helper — translated “Sign Up is disabled”.

**Local steps**

- If is\_signup\_disabled().
  - Call the validation error handler Platform.throw(translated “Sign Up is disabled”, title = translated “Not Allowed”).
- Set user from Platform.db.get(“User”, mapping(“email” → email)).
- If user.
  - If user.enabled.
    - Return tuple(0, translated “Already Registered”).
  - Otherwise.
    - Return tuple(0, translated “Registered but disabled”).
- Otherwise.
  - Set max\_signups\_allowed\_per\_hour from cint((Platform.get\_system\_settings(“max\_signups\_allowed\_per\_hour”) or 300)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“max\_signups\_allowed\_per\_hour”) → 300.
  - Set users\_created\_past\_hour from Platform.db.get\_creation\_count(“User”, 60).
  - If users\_created\_past\_hour ≥ max\_signups\_allowed\_per\_hour.
    - Evaluate Platform.respond\_as\_web\_page(translated “Temporarily Disabled”, translated “Too many users signed up recently, so the registration is disabled. Please try back in an hour”, http\_status\_code = 429).
  - Bind dependencies random\_string.
  - Set user from Platform.get\_doc(mapping(“doctype” → “User”, “email” → email, “first\_name” → escape\_html(full\_name), “enabled” → 1, …)).
  - Set user.flags.ignore\_permissions from true.
  - Set user.flags.ignore\_password\_policy from true.
  - Evaluate user.insert().
  - Set default\_role from Platform.get\_single\_value(“Portal Settings”, “default\_role”).
  - If default\_role.
    - Evaluate user.add\_roles(default\_role).
  - If redirect\_to.
    - Evaluate Platform.cache.hset(“redirect\_after\_login”, user.name, sanitize\_redirect(redirect\_to)).
  - If user.flags.email\_sent.
    - Return tuple(1, translated “Please check your email for verification”).
  - Otherwise.
    - Return tuple(2, translated “Please ask your administrator to verify your sign-up”).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“max\_signups\_allowed\_per\_hour”), Platform.get\_single\_value(“Portal Settings”, “default\_role”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L47) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L673)
