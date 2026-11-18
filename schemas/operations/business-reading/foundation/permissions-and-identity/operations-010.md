# Identity and access · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Twofactor

<a id="op-d10f33d9c865a4"></a>
### Get verification obj

`operation_foundation_twofactor_business_behavior_get_verification_obj`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, token, otp\_secret.

**Explicit result forms** a value selected from the current context.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L6506) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1405)

<a id="op-6d340ad9f59f8a"></a>
### Process 2fa for sms

`operation_foundation_twofactor_business_behavior_process_2_fa_for_short_message_service`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, token, otp\_secret.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L6890) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1408)

<a id="op-70e979fc4e9f0e"></a>
### Process 2fa for otp app

`operation_foundation_twofactor_business_behavior_process_2_fa_for_one_time_password_application`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, otp\_secret, otp\_issuer.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L7225) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1407)

<a id="op-3f614b3de1d5fa"></a>
### Process 2fa for email

`operation_foundation_twofactor_business_behavior_process_2_fa_for_email`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, token, otp\_secret, otp\_issuer, method.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L59) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1406)

<a id="op-e28815e9f57a4f"></a>
### Get email subject for 2fa

`operation_foundation_twofactor_business_behavior_get_email_subject_for_2_fa`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** kwargs\_dict.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1398)

<a id="op-e45841d15bfb57"></a>
### Get email body for 2fa

`operation_foundation_twofactor_business_behavior_get_email_body_for_2_fa`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** kwargs\_dict.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L139) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1396)

<a id="op-765662a78e448a"></a>
### Get email subject for qr code

`operation_foundation_twofactor_business_behavior_get_email_subject_for_quick_response_code`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** kwargs\_dict.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L272) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1399)

<a id="op-1388e47bdf73a4"></a>
### Get email body for qr code

`operation_foundation_twofactor_business_behavior_get_email_body_for_quick_response_code`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** kwargs\_dict.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L405) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1397)

<a id="op-90137e49cb2a49"></a>
### Get link for qrcode

`operation_foundation_twofactor_business_behavior_get_link_for_qrcode`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, totp\_uri.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L58) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1400)

<a id="op-a1496d27dc9c9f"></a>
### Send token via sms

`operation_foundation_twofactor_business_behavior_send_token_via_short_message_service`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** otpsecret, token, phone\_no.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Observed service boundaries** notification or queued-work request, record lookup.

**Local structure** 3 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L857) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1411)

<a id="op-d1828dc28fb78e"></a>
### Get rendered otp message

`operation_foundation_twofactor_business_behavior_get_rendered_one_time_password_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** otp.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L1493) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1403)

<a id="op-5017dd2b44e0f6"></a>
### Send token via email

`operation_foundation_twofactor_business_behavior_send_token_via_email`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, token, otp\_secret, otp\_issuer, subject, message.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** notification or queued-work request, record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L1650) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1410)

<a id="op-bf7c73cc51b3c1"></a>
### Get qr svg code

`operation_foundation_twofactor_business_behavior_get_quick_response_scalable_vector_graphics_code`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** totp\_uri.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L2043) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1402)

<a id="op-2cd3ac6e9be2ca"></a>
### Create barcode folder

`operation_foundation_twofactor_business_behavior_create_barcode_folder`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L2321) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1390)

<a id="op-d83e266bb6578d"></a>
### Delete qrimage

`operation_foundation_twofactor_business_behavior_delete_qrimage`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, check\_expiry.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L2573) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1392)

<a id="op-6adf0cd19af8b7"></a>
### Delete all barcodes for users

`operation_foundation_twofactor_business_behavior_delete_all_barcodes_for_users`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L2856) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1391)

<a id="op-b92709881fd951"></a>
### Should remove barcode image

`operation_foundation_twofactor_business_behavior_should_remove_barcode_image`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** barcode.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L3031) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1413)

<a id="op-ab9a3a115da622"></a>
### Disable

`operation_foundation_twofactor_business_behavior_disable`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L3252) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1393)

<a id="op-ee9bd8cfcc785d"></a>
### Reset otp secret

`operation_foundation_twofactor_business_behavior_reset_one_time_password_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Observed service boundaries** effective access lookup, notification or queued-work request, record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L3320) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1409)
