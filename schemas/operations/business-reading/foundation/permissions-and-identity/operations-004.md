# Identity and access · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Oauth

<a id="op-b7e28ab0a7935e"></a>
### OAuth Web Request Validator.confirm redirect uri

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_confirm_redirect_resource_identifier`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, code, redirect\_uri, client, args, kwargs.

**Explicit result forms** a comparison result.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L22) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1577)

<a id="op-db416be94225c8"></a>
### OAuth Web Request Validator.validate grant type

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_grant_type`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, grant\_type, client, request, args, kwargs.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L30) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1593)

<a id="op-f3f607bd02744d"></a>
### OAuth Web Request Validator.validate user

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_user`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, username, password, client, request, args, kwargs.

**Explicit result forms** Boolean false.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L35) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1602)

<a id="op-31caea26c053d6"></a>
### OAuth Web Request Validator.save bearer token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_save_bearer_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, token, request, args, kwargs.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, record mutation request, transaction control.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L26) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1589)

<a id="op-507d3556b3e7a9"></a>
### OAuth Web Request Validator.invalidate authorization code

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_invalidate_authorization_code`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, code, request, args, kwargs.

**Observed service boundaries** record mutation request, transaction control.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L1883) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1586)

<a id="op-691cc98411cadd"></a>
### OAuth Web Request Validator.validate bearer token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_bearer_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, token, scopes, request.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L27) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1590)

<a id="op-2e96b38042efe4"></a>
### OAuth Web Request Validator.get original scopes

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_get_original_scopes`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, refresh\_token, request, args, kwargs.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L24) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1583)

<a id="op-8b8fe6a6b43b12"></a>
### OAuth Web Request Validator.revoke token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_revoke_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, token, token\_type\_hint, request, args, kwargs.

**Observed service boundaries** record mutation request, transaction control.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L25) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1587)

<a id="op-80dad0eada2013"></a>
### OAuth Web Request Validator.validate refresh token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_refresh_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, refresh\_token, client, request, args, kwargs.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L33) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1596)

<a id="op-254e617c4b085b"></a>
### OAuth Web Request Validator.finalize id token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_finalize_identifier_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, id\_token, token, token\_handler, request.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L3206) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1578)

<a id="op-61fd30330508a3"></a>
### OAuth Web Request Validator.get authorization code nonce

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_get_authorization_code_nonce`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, code, redirect\_uri, request.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L3693) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1579)

<a id="op-72911ffdf34958"></a>
### OAuth Web Request Validator.get authorization code scopes

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_get_authorization_code_scopes`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, client\_id, code, redirect\_uri, request.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L3858) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1580)

<a id="op-1fa0623b29ed8b"></a>
### OAuth Web Request Validator.get jwt bearer token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_get_signed_authorization_token_bearer_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, token, token\_handler, request.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L4040) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1584)

<a id="op-9865034c98cc7d"></a>
### OAuth Web Request Validator.get userinfo claims

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_get_userinfo_claims`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, request.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L4259) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1585)

<a id="op-6cc617959a68ae"></a>
### OAuth Web Request Validator.validate id token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_identifier_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, token, scopes, request.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L31) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1594)

<a id="op-7da93abbf8398f"></a>
### OAuth Web Request Validator.validate jwt bearer token

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_signed_authorization_token_bearer_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, token, scopes, request.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L34) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1599)

<a id="op-429df266fb5d8a"></a>
### OAuth Web Request Validator.validate silent authorization

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_silent_authorization`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, request.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L4739) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1600)

<a id="op-1078aa80f872b6"></a>
### OAuth Web Request Validator.validate silent login

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_silent_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, request.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L4817) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1601)

<a id="op-f142a61e542af0"></a>
### OAuth Web Request Validator.validate user match

`operation_foundation_delegated_authorization_business_behavior_o_authentication_web_request_validator_validate_user_match`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, id\_token\_hint, scopes, claims, request.

**Explicit result forms** Boolean false, Boolean true, a comparison result.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L4937) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1603)

<a id="op-06870c3109f792"></a>
### Calculate at hash

`operation_foundation_delegated_authorization_business_behavior_calculate_at_hash`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** access\_token, hash\_alg.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L5743) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1568)

<a id="op-fecf5dbbe57a44"></a>
### Delete oauth2 data

`operation_foundation_delegated_authorization_business_behavior_delete_delegated_authorization_2_data`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L5965) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1569)

<a id="op-c9547e0c775202"></a>
### Get client scopes

`operation_foundation_delegated_authorization_business_behavior_get_client_scopes`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** client\_id.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L18) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1571)

<a id="op-7eca264329364b"></a>
### Get userinfo

`operation_foundation_delegated_authorization_business_behavior_get_userinfo`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L19) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1574)

<a id="op-bf5bee96f72d4e"></a>
### Get url delimiter

`operation_foundation_delegated_authorization_business_behavior_get_resource_address_delimiter`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** separator\_character.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0298.json#L6701) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1572)
