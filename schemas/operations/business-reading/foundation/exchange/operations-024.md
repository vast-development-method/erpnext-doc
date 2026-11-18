# Integration and transport · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Notification

[Record definition](../../../../data/record-types/notification.json)

<a id="op-6f6b738940e76e"></a>
### Get emails from template

`operation_foundation_email_record_definitions_notification_business_behavior_get_emails_from_template`

**Inputs** template, context.

**Explicit results** tuple() · filter(no value, emails.replace(“,”, whitespace '\\n').split(whitespace '\\n')).

**Local steps**

- If not template.
  - Return tuple().
- Set emails from Platform.render\_template(template, context, restrict\_globals = true) when “{” belongs to template, otherwise template.
  - Value choice on “{” belongs to template — true gives Platform.render\_template(template, context, restrict\_globals = true), false gives template.
- Return filter(no value, emails.replace(“,”, whitespace '\\n').split(whitespace '\\n')).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L6581) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L209)

<a id="op-639d1397e1b161"></a>
### Get reference doctype

`operation_foundation_email_record_definitions_notification_business_behavior_get_reference_record_type`

**Inputs** doc.

**Explicit results** doc.parenttype when doc.meta.istable, otherwise doc.doctype.

**Local steps**

- Return doc.parenttype when doc.meta.istable, otherwise doc.doctype.
  - Value choice on doc.meta.istable — true gives doc.parenttype, false gives doc.doctype.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L6768) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L212)

<a id="op-e76afa330507e5"></a>
### Get reference name

`operation_foundation_email_record_definitions_notification_business_behavior_get_reference_name`

**Inputs** doc.

**Explicit results** doc.parent when doc.meta.istable, otherwise doc.name.

**Local steps**

- Return doc.parent when doc.meta.istable, otherwise doc.name.
  - Value choice on doc.meta.istable — true gives doc.parent, false gives doc.name.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L6834) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L211)

<a id="op-4fd6857ce4a2e8"></a>
### Parse receiver by document field

`operation_foundation_email_record_definitions_notification_business_behavior_parse_receiver_by_document_field`

**Inputs** s.

**Explicit results** tuple(data\_field, child\_field).

**Local steps**

- Set fragments from s.split(“,”).
- If len(fragments) &gt; 1.
  - Set tuple(data\_field, child\_field) from fragments.
- Otherwise.
  - Set tuple(data\_field, child\_field) from tuple(fragments at 0, no value).
- Return tuple(data\_field, child\_field).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0230.json#L6902) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L247)

<a id="op-77eefc6072e58d"></a>
### Create notifications

`operation_foundation_email_record_definitions_notification_business_behavior_create_notifications`

**Inputs** notifications, update = false.

**Record and data access** read “Notification” via exists · resolve a document from “Notification” via get\_doc · resolve a document from notif\_dict via get\_doc.

**State and service calls** call save on doc · call insert on doc.

**Local steps**

- For each notif\_dict in notifications.
  - Set name from notif\_dict.get(“name”).
  - Set existing from Platform.db.exists(“Notification”, name).
  - If (existing and not update).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing → not update.
    - Continue with the next iteration or loop test.
  - If (existing and update).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in existing → update.
    - Set doc from Platform.get\_doc(“Notification”, name).
    - Evaluate doc.update(notif\_dict).
    - Set doc.flags.ignore\_validate from true.
    - Evaluate doc.save(ignore\_permissions = true).
    - Continue with the next iteration or loop test.
  - Set notif\_dict at “doctype” from “Notification”.
  - Set notif\_dict at “is\_standard” from 0.
  - Set notif\_dict at “owner” from “Administrator”.
  - Set doc from Platform.get\_doc(notif\_dict).
  - Set doc.flags.ignore\_validate from true.
  - Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0231.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L204)

<a id="op-fb6936a24c54ef"></a>
### Get notification templates

`operation_foundation_email_record_definitions_notification_business_behavior_get_notification_templates`

**Inputs** templates\_dir.

**Declared result** list at dict.

**Explicit results** templates.

**Local steps**

- Set templates from list().
- If not os.path.exists(templates\_dir).
  - Return templates.
- For each folder\_name in os.listdir(templates\_dir).
  - Set folder\_path from os.path.join(templates\_dir, folder\_name).
  - If not os.path.isdir(folder\_path).
    - Continue with the next iteration or loop test.
  - Set json\_file from os.path.join(folder\_path, formatted text {folder\_name}.json).
  - Set template from Platform.get\_file\_json(json\_file) when os.path.exists(json\_file), otherwise no value.
    - Value choice on os.path.exists(json\_file) — true gives Platform.get\_file\_json(json\_file), false gives no value.
  - If not template.
    - Continue with the next iteration or loop test.
  - Set message\_type from template.get(“message\_type”, “HTML”).
  - Set ext from FORMATS.get(message\_type, “.html”).
  - Set message\_file from os.path.join(folder\_path, formatted text {folder\_name}{ext}).
  - If message bound to Platform.read\_file(message\_file).
    - Set template at “message” from message.
  - Evaluate templates.append(template).
- Return templates.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0231.json#L476) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L210)

<a id="op-7edf792f1f343e"></a>
### Install notification templates

`operation_foundation_email_record_definitions_notification_business_behavior_install_notification_templates`

**Inputs** no declared parameters.

**Local steps**

- Set templates\_dir from Platform.get\_module\_path(“Email”, “doctype”, “notification”, “templates”).
- Set templates from get\_notification\_templates(templates\_dir).
- Evaluate create\_notifications(templates, update = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0231.json#L1028) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L213)

## Service · Oauth

<a id="op-ea047d23963bf4"></a>
### Oauth.initialize

`operation_foundation_email_delegated_authorization_business_behavior_delegated_authorization_initialize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, conn, email\_account, email, access\_token, mechanism.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L7811) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1017) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1450)

<a id="op-2f95c17d4438fe"></a>
### Oauth.validate

`operation_foundation_email_delegated_authorization_business_behavior_delegated_authorization_validate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1018) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1451)

<a id="op-5473ff988dfb92"></a>
### Oauth.auth string

`operation_foundation_email_delegated_authorization_business_behavior_delegated_authorization_authentication_string`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L147) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1012) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1445)

<a id="op-7cde79f37971dc"></a>
### Oauth.connect

`operation_foundation_email_delegated_authorization_business_behavior_delegated_authorization_connect`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L234) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1013) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1446)

<a id="op-1851c1b6b2eae6"></a>
### Oauth.connect pop

`operation_foundation_email_delegated_authorization_business_behavior_delegated_authorization_connect_post_office_protocol`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L469) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1015) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1448)

<a id="op-0f2383624ecb2a"></a>
### Oauth.connect imap

`operation_foundation_email_delegated_authorization_business_behavior_delegated_authorization_connect_internet_message_access_protocol`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L794) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1014) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1447)

<a id="op-e6f228f24965af"></a>
### Oauth.connect smtp

`operation_foundation_email_delegated_authorization_business_behavior_delegated_authorization_connect_simple_mail_transfer_protocol`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L876) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1016) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1449)

## Record · Oauth bearer token

<a id="op-67fcc8fe823a93"></a>
### OAuth Bearer Token.validate

`operation_foundation_integrations_record_definitions_delegated_authorization_bearer_token_business_behavior_o_authentication_bearer_token_validate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0253.json#L3140) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L702)

<a id="op-8e914fe6714dca"></a>
### OAuth Bearer Token.clear old logs

`operation_foundation_integrations_record_definitions_delegated_authorization_bearer_token_business_behavior_o_authentication_bearer_token_clear_old_logs`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** days.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0253.json#L3247) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L701)

## Record · Oauth client

<a id="op-d42fffaf3afdac"></a>
### OAuth Client.validate

`operation_foundation_integrations_record_definitions_delegated_authorization_client_business_behavior_o_authentication_client_validate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L58) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L708)

<a id="op-f489bbbd5ea28c"></a>
### OAuth Client.validate grant and response

`operation_foundation_integrations_record_definitions_delegated_authorization_client_business_behavior_o_authentication_client_validate_grant_and_response`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L709)

<a id="op-76ee7814270b7a"></a>
### OAuth Client.add default role

`operation_foundation_integrations_record_definitions_delegated_authorization_client_business_behavior_o_authentication_client_add_default_role`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L207) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1978) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L704)

<a id="op-4dcbd5e8c509d0"></a>
### OAuth Client.user has allowed role

`operation_foundation_integrations_record_definitions_delegated_authorization_client_business_behavior_o_authentication_client_user_has_allowed_role`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L305) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1981) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L707)

<a id="op-5cbb54ba9fa9af"></a>
### OAuth Client.is public client

`operation_foundation_integrations_record_definitions_delegated_authorization_client_business_behavior_o_authentication_client_is_public_client`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L427) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L706)

<a id="op-f5fbfa2f5fb272"></a>
### OAuth Client.client id issued at

`operation_foundation_integrations_record_definitions_delegated_authorization_client_business_behavior_o_authentication_client_client_identifier_issued_at`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L484) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1979) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L705)

## Service · Oauth2

<a id="op-15915b42b53cba"></a>
### Get oauth server

`operation_foundation_integrations_oauth2_business_behavior_get_delegated_authorization_server`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L2633) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L654)

<a id="op-46bb3dbb315d26"></a>
### Sanitize kwargs

`operation_foundation_integrations_oauth2_business_behavior_sanitize_named_arguments`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** param\_kwargs.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L2761) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L666)
