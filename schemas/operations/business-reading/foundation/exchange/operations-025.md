# Integration and transport · operations 25

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Oauth2

<a id="op-e169c2c4c65294"></a>
### Encode params

`operation_foundation_integrations_oauth2_business_behavior_encode_parameters`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** params.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L2873) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L651)

<a id="op-d04809c2e096b0"></a>
### Approve

`operation_foundation_integrations_oauth2_business_behavior_approve`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** args, kwargs.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L2933) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L648)

<a id="op-c9a20460f50869"></a>
### Authorize

`operation_foundation_integrations_oauth2_business_behavior_authorize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 7 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L52) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L649)

<a id="op-7fe82eef68b5ec"></a>
### Get token

`operation_foundation_integrations_oauth2_business_behavior_get_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** args, kwargs.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L4904) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L659)

<a id="op-64565b95025cdd"></a>
### Revoke token

`operation_foundation_integrations_oauth2_business_behavior_revoke_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** args, kwargs.

**Explicit result forms** no value.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L5278) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1927) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L665)

<a id="op-cb663673896239"></a>
### Openid profile

`operation_foundation_integrations_oauth2_business_behavior_openid_profile`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** args, kwargs.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L5578) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1925) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L663)

<a id="op-c19461b1fc56c8"></a>
### Get openid configuration

`operation_foundation_integrations_oauth2_business_behavior_get_openid_configuration`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L5878) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L655)

<a id="op-f00939c6f30f00"></a>
### Introspect token

`operation_foundation_integrations_oauth2_business_behavior_introspect_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** token, token\_type\_hint.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L53) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L661)

<a id="op-5d66c449c51c90"></a>
### Handle wellknown

`operation_foundation_integrations_oauth2_business_behavior_handle_wellknown`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** path.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** NotFound.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L7070) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1922) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L660)

<a id="op-83d9ccc7466d61"></a>
### Get authorization server metadata

`operation_foundation_integrations_oauth2_business_behavior_get_authorization_server_metadata`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L7290) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L652)

<a id="op-50a41ec5bb146e"></a>
### Get authorization server metadata

`operation_foundation_integrations_oauth2_business_behavior_get_authorization_server_metadata_2`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L653)

<a id="op-587780baf7e1a3"></a>
### Register client

`operation_foundation_integrations_oauth2_business_behavior_register_client`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** NotFound.

**Observed service boundaries** record lookup.

**Local structure** 6 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L54) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1926) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L664)

<a id="op-54b1cfb1258d0c"></a>
### Get protected resource metadata

`operation_foundation_integrations_oauth2_business_behavior_get_protected_resource_metadata`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L1648) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L656)

<a id="op-d16f46ea5b6bc7"></a>
### Get protected resource metadata

`operation_foundation_integrations_oauth2_business_behavior_get_protected_resource_metadata_2`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L1758) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L657)

<a id="op-766bf4df9d32b5"></a>
### Is oauth metadata enabled

`operation_foundation_integrations_oauth2_business_behavior_is_delegated_authorization_metadata_enabled`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** label.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L2335) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L662)

<a id="op-35d640694c4cb1"></a>
### Get resource url

`operation_foundation_integrations_oauth2_business_behavior_get_resource_resource_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L2541) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L658)

<a id="op-c8aabe6ab51fc6"></a>
### Del none values

`operation_foundation_integrations_oauth2_business_behavior_delete_none_values`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** d.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L2639) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L650)

<a id="op-177271a768862e"></a>
### Set cors for privileged requests

`operation_foundation_integrations_oauth2_business_behavior_set_cross_origin_resource_sharing_for_privileged_remote_requests`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L2779) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1930) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L668)

<a id="op-0c5d3631437bd3"></a>
### Set allowed cors

`operation_foundation_integrations_oauth2_business_behavior_set_allowed_cross_origin_resource_sharing`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L3347) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L667)

## Service · Oauth2 logins

<a id="op-e403f57743883e"></a>
### Login via google

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_google`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L3542) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L675)

<a id="op-9027c8b17ac925"></a>
### Login via github

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_github`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L3657) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L674)

<a id="op-c9611de52c3bc3"></a>
### Login via facebook

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_facebook`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L3761) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1933) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L671)

<a id="op-449d3eb686f041"></a>
### Login via Platform

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_foundation`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L3881) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L673)

<a id="op-34476418566199"></a>
### Login via office365

`operation_foundation_integrations_oauth2_logins_business_behavior_login_via_office_365`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** code, state.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0262.json#L3996) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L677)
