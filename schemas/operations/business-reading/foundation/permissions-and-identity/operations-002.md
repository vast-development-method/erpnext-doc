# Identity and access · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Auth

<a id="op-24ca6545a6d2c3"></a>
### Login Manager.login as

`operation_foundation_auth_business_behavior_login_manager_login_as`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user, session\_end, audit\_user.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L2196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L129)

<a id="op-4c01fbc1c0bdcb"></a>
### Login Manager.impersonate

`operation_foundation_auth_business_behavior_login_manager_impersonate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L2331) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L150) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L126)

<a id="op-82cfefdca83066"></a>
### Login Manager.logout

`operation_foundation_auth_business_behavior_login_manager_logout`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, arg, user.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L2505) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L131)

<a id="op-3b9b5ca3053270"></a>
### Login Manager.clear cookies

`operation_foundation_auth_business_behavior_login_manager_clear_cookies`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L2773) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L121)

<a id="op-847c4a580adc05"></a>
### Cookie Manager.initialize

`operation_foundation_auth_business_behavior_cookie_manager_initialize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L2820) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L95)

<a id="op-bf69452bccf42b"></a>
### Cookie Manager.init cookies

`operation_foundation_auth_business_behavior_cookie_manager_initialize_cookies`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L2884) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L120) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L96)

<a id="op-a2225bd8e54364"></a>
### Cookie Manager.set cookie

`operation_foundation_auth_business_behavior_cookie_manager_set_cookie`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, key, value, expires, secure, httponly, samesite, max\_age, deduplicate.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L3045) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L121) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L97)

<a id="op-495f6fb9a73bc9"></a>
### Cookie Manager.delete cookie

`operation_foundation_auth_business_behavior_cookie_manager_delete_cookie`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, to\_delete.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L3457) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L117) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L93)

<a id="op-62422036aa3a25"></a>
### Cookie Manager.flush cookies

`operation_foundation_auth_business_behavior_cookie_manager_flush_cookies`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, response.

**Local structure** 0 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L3578) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L94)

<a id="op-be08bacb91251a"></a>
### Get logged user

`operation_foundation_auth_business_behavior_get_logged_user`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L3995) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L122) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L98)

<a id="op-5c0aa710844884"></a>
### Clear cookies

`operation_foundation_auth_business_behavior_clear_cookies`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L4049) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L116) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L92)

<a id="op-f53f758172a6e6"></a>
### Validate ip address

`operation_foundation_auth_business_behavior_validate_internet_protocol_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** Boolean true, no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 5 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L37) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L143)

<a id="op-e7ec76e026d7a5"></a>
### Get login attempt tracker

`operation_foundation_auth_business_behavior_get_login_attempt_tracker`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** key, raise\_locked\_exception.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L4654) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L123) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L99)

<a id="op-6bb99bbd84f26b"></a>
### Login Attempt Tracker.initialize

`operation_foundation_auth_business_behavior_login_attempt_tracker_initialize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, key, max\_consecutive\_login\_attempts, lock\_interval, user\_name.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L4986) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L134) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L110)

<a id="op-a6aaf9b9a291d5"></a>
### Login Attempt Tracker.login failed count

`operation_foundation_auth_business_behavior_login_attempt_tracker_login_failed_count`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5208) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L136) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L112)

<a id="op-81a1b1194a81aa"></a>
### Login Attempt Tracker.login failed count

`operation_foundation_auth_business_behavior_login_attempt_tracker_login_failed_count_2`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, count.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5279) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L113)

<a id="op-dfb6ff89510f27"></a>
### Login Attempt Tracker.login failed count

`operation_foundation_auth_business_behavior_login_attempt_tracker_login_failed_count_3`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5365) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L114)

<a id="op-f179bf25c34f12"></a>
### Login Attempt Tracker.login failed time

`operation_foundation_auth_business_behavior_login_attempt_tracker_login_failed_time`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5440) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L115)

<a id="op-80189d2048b070"></a>
### Login Attempt Tracker.login failed time

`operation_foundation_auth_business_behavior_login_attempt_tracker_login_failed_time_2`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, timestamp.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5511) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L116)

<a id="op-4e3de4c8ab6215"></a>
### Login Attempt Tracker.login failed time

`operation_foundation_auth_business_behavior_login_attempt_tracker_login_failed_time_3`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5597) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L117)

<a id="op-b60ddd85bc87ab"></a>
### Login Attempt Tracker.add failure attempt

`operation_foundation_auth_business_behavior_login_attempt_tracker_add_failure_attempt`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5672) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L108)

<a id="op-fbb28666877e5a"></a>
### Login Attempt Tracker.add success attempt

`operation_foundation_auth_business_behavior_login_attempt_tracker_add_success_attempt`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5926) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L133) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L109)

<a id="op-9defe7b38ef785"></a>
### Login Attempt Tracker.is user allowed

`operation_foundation_auth_business_behavior_login_attempt_tracker_is_user_allowed`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L5982) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L135) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L111)

<a id="op-528319ae988891"></a>
### Validate auth

`operation_foundation_auth_business_behavior_validate_authentication`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Locally raised failures** AuthenticationError.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0010.json#L6159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L139)
