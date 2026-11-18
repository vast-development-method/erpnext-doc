# Identity and access · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Sessions

<a id="op-fa101c83888cdc"></a>
### Get boot assets json

`operation_foundation_sessions_business_behavior_get_boot_assets_structured_data`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L5033) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L561)

<a id="op-8334ef62165881"></a>
### Get csrf token

`operation_foundation_sessions_business_behavior_get_cross_site_request_forgery_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L5089) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L562)

<a id="op-33cde7d0548ed7"></a>
### Generate csrf token

`operation_foundation_sessions_business_behavior_generate_cross_site_request_forgery_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L5181) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L559)

<a id="op-710af15314c792"></a>
### Session.initialize

`operation_foundation_sessions_business_behavior_session_initialize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user, resume, full\_name, user\_type, session\_end, audit\_user.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L38) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L574)

<a id="op-90fecace81b0c4"></a>
### Session.sid hash

`operation_foundation_binding_foundation_sessions_session_sid_hash`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L52) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1715)

<a id="op-7e44e338412ac5"></a>
### Session.validate user

`operation_foundation_sessions_business_behavior_session_validate_user`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L5854) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L581)

<a id="op-ceee688edc7a94"></a>
### Session.start

`operation_foundation_sessions_business_behavior_session_start`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, session\_end, audit\_user.

**Observed service boundaries** transaction control.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L40) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1904) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L578)

<a id="op-307a3fa6db2c4f"></a>
### Session.insert session record

`operation_foundation_sessions_business_behavior_session_insert_session_record`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L39) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L575)

<a id="op-49e01193071f48"></a>
### Session.resume

`operation_foundation_sessions_business_behavior_session_resume`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0332.json#L7163) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L576)

<a id="op-c5ae99cd0f3d5c"></a>
### Session.get session record

`operation_foundation_sessions_business_behavior_session_get_session_record`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L37) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L573)

<a id="op-cbad8addf86367"></a>
### Session.get session data

`operation_foundation_sessions_business_behavior_session_get_session_data`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L34) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1896) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L570)

<a id="op-9cfbc72466930b"></a>
### Session.get session data from cache

`operation_foundation_sessions_business_behavior_session_get_session_data_from_cache`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L35) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L571)

<a id="op-d283942b1ca66e"></a>
### Session.get session data from db

`operation_foundation_sessions_business_behavior_session_get_session_data_from_database`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L36) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L572)

<a id="op-3992a57f87e83b"></a>
### Session.delete session

`operation_foundation_sessions_business_behavior_session_delete_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L33) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L569)

<a id="op-f09e7ae23ed1c2"></a>
### Session.start as guest

`operation_foundation_sessions_business_behavior_session_start_as_guest`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L864) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L579)

<a id="op-ff5337ca8d3f06"></a>
### Session.update

`operation_foundation_sessions_business_behavior_session_update`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, force.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** transaction control.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L41) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L580)

<a id="op-43eac7f48aefac"></a>
### Session.set impersonated

`operation_foundation_sessions_business_behavior_session_set_impersonated`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, original\_user.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L1729) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L577)

<a id="op-6b051783105fe3"></a>
### Update user metadata

`operation_foundation_sessions_business_behavior_update_user_metadata`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, last\_login, last\_ip, last\_active, run\_notifications.

**Explicit result forms** no value.

**Observed service boundaries** transaction control.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L1823) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L582)

<a id="op-614702b900abd8"></a>
### Get expiry period for query

`operation_foundation_sessions_business_behavior_get_expiry_period_for_query`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L2420) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L567)

<a id="op-36c3f92eef6f5f"></a>
### Get expiry in seconds

`operation_foundation_sessions_business_behavior_get_expiry_in_seconds`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** expiry.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L2506) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L565)

<a id="op-87db5839fb55f0"></a>
### Get expired threshold

`operation_foundation_sessions_business_behavior_get_expired_threshold`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L2706) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L564)

<a id="op-81dd47e4e97747"></a>
### Get expiry period

`operation_foundation_sessions_business_behavior_get_expiry_period`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L31) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L566)

## Service · Share

<a id="op-4f6a68f1e20c3b"></a>
### Add

`operation_foundation_share_business_behavior_add`

**Inputs** doctype, name, user = no value, read = 1, write = 0, submit = 0, share = 0, everyone = 0, notify = 0, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** add\_docshare(doctype, name, user = user, read = read, write = write, submit = submit, …).

**Local steps**

- Evaluate validate\_user\_access(user, translated “User”).
- Return add\_docshare(doctype, name, user = user, read = read, write = write, submit = submit, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L42) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L583)

<a id="op-e03a5b0f7560c7"></a>
### Validate user access

`operation_foundation_binding_foundation_share_validate_user_access`

**Inputs** user, label.

**Explicit failure paths** validation helper with Platform.LinkValidationError — translated “Could not find {0}”.format(formatted text {label}: {user}).

**Local steps**

- Bind dependencies get\_user\_permissions.
- Bind dependencies get\_allowed\_docs\_for\_doctype.
- Set allowed from get\_allowed\_docs\_for\_doctype(get\_user\_permissions().get(“User”, list()), “User”).
- If (user and allowed and user does not belong to allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in user → allowed → user does not belong to allowed.
  - Call the validation error handler Platform.throw(translated “Could not find {0}”.format(formatted text {label}: {user}), Platform.LinkValidationError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L53) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1716)
