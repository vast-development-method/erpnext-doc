# Identity and access · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Auth

<a id="op-bcb383f2218565"></a>
### HTTPRequest.initialize

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_initialize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L3181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L125) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L101)

<a id="op-6e6f6ba1061e59"></a>
### HTTPRequest.domain

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_domain`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L3339) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L100)

<a id="op-20b7d59ee0a680"></a>
### HTTPRequest.set request ip

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_set_request_internet_protocol`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L105)

<a id="op-3053cb675cd4da"></a>
### HTTPRequest.set cookies

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_set_cookies`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L3817) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L127) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L103)

<a id="op-2922dabdb823cd"></a>
### HTTPRequest.set session

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_set_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L3876) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L130) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L106)

<a id="op-cc4295aa69b5bb"></a>
### HTTPRequest.validate csrf token

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_validate_cross_site_request_forgery_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L3935) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L131) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L107)

<a id="op-92d77166a81b08"></a>
### HTTPRequest.set lang

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_set_language`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L4220) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L128) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L104)

<a id="op-eb59cf8f360ad1"></a>
### HTTPRequest.is allowed referrer

`operation_foundation_auth_business_behavior_hypertext_transfer_protocol_request_is_allowed_referrer`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** Boolean true, a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L4281) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L102)

<a id="op-860f3b39809fc4"></a>
### Login Manager.initialize

`operation_foundation_auth_business_behavior_login_manager_initialize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L151) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L127)

<a id="op-af0de85c83b84b"></a>
### Login Manager.login

`operation_foundation_auth_business_behavior_login_manager_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** Boolean false.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L33) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L128)

<a id="op-569750bb15108d"></a>
### Login Manager.post login

`operation_foundation_auth_business_behavior_login_manager_post_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, session\_end, audit\_user.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L5531) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L133)

<a id="op-a170d4b9ad6b73"></a>
### Login Manager.get user info

`operation_foundation_auth_business_behavior_login_manager_get_user_info`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L125)

<a id="op-02808e32ddc65e"></a>
### Login Manager.setup boot cache

`operation_foundation_auth_business_behavior_login_manager_setup_boot_cache`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L6012) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L136)

<a id="op-7c17015671be74"></a>
### Login Manager.set user info

`operation_foundation_auth_business_behavior_login_manager_set_user_info`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, resume.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L6109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L135)

<a id="op-d90af0fd8cf3b7"></a>
### Login Manager.clear preferred language

`operation_foundation_auth_business_behavior_login_manager_clear_preferred_language`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0009.json#L6989) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L122)

<a id="op-571f21745e0b00"></a>
### Login Manager.make session

`operation_foundation_auth_business_behavior_login_manager_make_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, resume, session\_end, audit\_user.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L132)

<a id="op-42e39624cf5967"></a>
### Login Manager.clear active sessions

`operation_foundation_auth_business_behavior_login_manager_clear_active_sessions`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L30) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L144) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L120)

<a id="op-ba68c86de4957e"></a>
### Login Manager.authenticate

`operation_foundation_auth_business_behavior_login_manager_authenticate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user, pwd.

**Local structure** 7 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L29) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L118)

<a id="op-857e98af04c3a1"></a>
### Login Manager.force user to reset password

`operation_foundation_auth_business_behavior_login_manager_force_user_to_reset_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** Boolean false, Boolean true, no value.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L955) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L124)

<a id="op-cd9015c8cf3af9"></a>
### Login Manager.check password

`operation_foundation_auth_business_behavior_login_manager_check_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user, pwd.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L1248) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L143) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L119)

<a id="op-79cdd83907acab"></a>
### Login Manager.fail

`operation_foundation_auth_business_behavior_login_manager_fail`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, message, user.

**Locally raised failures** AuthenticationError.

**Observed service boundaries** transaction control.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L1378) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L123)

<a id="op-3b4f1fdb9aee3e"></a>
### Login Manager.run trigger

`operation_foundation_auth_business_behavior_login_manager_run_trigger`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, event.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L1575) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L134)

<a id="op-30b0d625b9c79d"></a>
### Login Manager.validate hour

`operation_foundation_auth_business_behavior_login_manager_validate_hour`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L1712) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L137)

<a id="op-dfae145051a5e7"></a>
### Login Manager.login as guest

`operation_foundation_auth_business_behavior_login_manager_login_as_guest`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L2140) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L130)
