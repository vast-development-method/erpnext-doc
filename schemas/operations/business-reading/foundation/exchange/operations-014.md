# Integration and transport · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email group

[Record definition](../../../../data/record-types/email_group.json)

<a id="op-d11921d93377e6"></a>
### Add subscribers

`operation_foundation_email_record_definitions_email_group_business_behavior_add_subscribers`

**Inputs** name, email\_list.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Email Group” via get\_value · resolve a document from “Email Template” via get\_doc · read “Email Group Member” via get\_value · resolve a document from mapping(“doctype” → “Email Group Member”, “email\_group” → name, “email” → parsed\_email) via get\_doc · resolve a document from “Email Group” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Email Group Member”, “email\_group” → name, “email” → parsed\_email)) · msgprint with translated “{0} is not a valid Email Address”.format(email) · msgprint with translated “{0} subscribers added”.format(count).

**Explicit results** Platform.get\_doc(“Email Group”, name).update\_total\_subscribers().

**Local steps**

- If not isinstance(email\_list, (list bitwise or tuple)).
  - Set email\_list from email\_list.replace(“,”, whitespace '\\n').split(whitespace '\\n').
- Set template from Platform.db.get\_value(“Email Group”, name, “welcome\_email\_template”).
- Set welcome\_email from Platform.get\_doc(“Email Template”, template) when template, otherwise no value.
  - Value choice on template — true gives Platform.get\_doc(“Email Template”, template), false gives no value.
- Set count from 0.
- For each email in email\_list.
  - Set email from email.strip().
  - Set parsed\_email from validate\_email\_address(email, false).
  - If parsed\_email.
    - If not Platform.db.get\_value(“Email Group Member”, mapping(“email\_group” → name, “email” → parsed\_email)).
      - Evaluate Platform.get\_doc(mapping(“doctype” → “Email Group Member”, “email\_group” → name, “email” → parsed\_email)).insert(ignore\_permissions = Platform.flags.ignore\_permissions).
      - Evaluate send\_welcome\_email(welcome\_email, parsed\_email, name).
      - Update count using + 1.
    - Otherwise.
      - Take no action here.
  - Otherwise.
    - Evaluate Platform.msgprint(translated “{0} is not a valid Email Address”.format(email)).
- Evaluate Platform.msgprint(translated “{0} subscribers added”.format(count)).
- Return Platform.get\_doc(“Email Group”, name).update\_total\_subscribers().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L5307) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L106)

<a id="op-fd17f41f4a9620"></a>
### Send welcome email

`operation_foundation_email_record_definitions_email_group_business_behavior_send_welcome_email`

**Inputs** welcome\_email, email, email\_group.

**State and service calls** sendmail with email.

**Explicit results** no value.

**Local steps**

- If not welcome\_email.
  - Return no value.
- Set args from dict(email = email, email\_group = email\_group).
- Set message from Platform.render\_template(welcome\_email.response\_, args, restrict\_globals = true).
- Evaluate Platform.sendmail(email, subject = welcome\_email.subject, message = message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(email, subject = welcome\_email.subject, message = message).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L6085) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L115)

<a id="op-82ec41a7e1b565"></a>
### Add query params

`operation_foundation_email_record_definitions_email_group_business_behavior_add_query_parameters`

**Inputs** url, params.

**Declared result** str.

**Explicit results** url · urlunparse(parsed).

**Local steps**

- Bind dependencies urlencode, urlparse, urlunparse.
- If not params.
  - Return url.
- Set query\_string from urlencode(params).
- Set parsed from list(urlparse(url)).
- If parsed at 4.
  - Update parsed at 4 using + formatted text &amp;{query\_string}.
- Otherwise.
  - Set parsed at 4 from query\_string.
- Return urlunparse(parsed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L6286) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L105)

## Record · Email group member

[Record definition](../../../../data/record-types/email_group_member.json)

<a id="op-fbff77ef471c4f"></a>
### Email Group Member.after delete

`operation_foundation_email_record_definitions_email_group_member_business_behavior_email_group_member_after_delete`

**Inputs** self.

**Record and data access** resolve a document from “Email Group” via get\_doc.

**Local steps**

- Set email\_group from Platform.get\_doc(“Email Group”, self.email\_group).
- Evaluate email\_group.update\_total\_subscribers().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L7029) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L117)

<a id="op-d8217384c6bdfd"></a>
### Email Group Member.after insert

`operation_foundation_email_record_definitions_email_group_member_business_behavior_email_group_member_after_insert`

**Inputs** self.

**Record and data access** resolve a document from “Email Group” via get\_doc.

**Local steps**

- Set email\_group from Platform.get\_doc(“Email Group”, self.email\_group).
- Evaluate email\_group.update\_total\_subscribers().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0225.json#L7120) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L118)

<a id="op-8630bb2c46af1e"></a>
### After doctype insert

`operation_foundation_email_record_definitions_email_group_member_business_behavior_after_record_type_insert`

**Inputs** no declared parameters.

**State and service calls** request add\_unique on “Email Group Member”.

**Local steps**

- Evaluate Platform.db.add\_unique(“Email Group Member”, tuple(“email\_group”, “email”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L116)

## Service · Email oauth

<a id="op-58006ad6263ee5"></a>
### Get one click services

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_get_one_click_services`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Observed service boundaries** diagnostic or audit logging, effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1495)

<a id="op-b76fd9fad2228f"></a>
### Get active providers

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_get_active_providers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1494)

<a id="op-e349799eb3f7d3"></a>
### Initiate mailbox connect

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_initiate_mailbox_connect`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** service, redirect\_to, target\_doctype, email\_account, email.

**Explicit result forms** a value selected from the current context, no value.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** effective access lookup, record lookup, record mutation request, validation or user-notification service.

**Local structure** 7 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1496)

<a id="op-e1a082c1ec42cb"></a>
### Relay refresh

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_relay_refresh`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** app, token\_cache.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1500)

<a id="op-0711234ec7188b"></a>
### Call central method

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_call_central_method`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** method, data.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1489)

<a id="op-33c6c0b14744a6"></a>
### Callback

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_callback`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** state, code, error, error\_description.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** diagnostic or audit logging, record lookup, transaction control.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1490)

<a id="op-6c9e03cc8dca23"></a>
### Connect mailbox

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_connect_mailbox`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** note, code, error, error\_description, account\_email.

**Explicit result forms** a structured result.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** diagnostic or audit logging, record lookup, transaction control.

**Local structure** 14 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1491)

<a id="op-7f94157bf4f3a2"></a>
### Matched error

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_matched_error`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider, source, message.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1498)

<a id="op-ba852f3b884308"></a>
### Create relay app

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_create_relay_app`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** note, email, token.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1492)

<a id="op-fbd0d15cff4343"></a>
### Save email account

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_save_email_account`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** note, email, connected\_app, personal.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1501)

<a id="op-e40a5e70cf1a70"></a>
### Delete relay app

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_delete_relay_app`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** connected\_app.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1517) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1493)

<a id="op-dc44b064642d8f"></a>
### Land

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_land`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** redirect\_to, result, mailbox, provider.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1497)

<a id="op-4664801bebc2d8"></a>
### Redirect

`operation_foundation_binding_foundation_integrations_foundation_providers_email_oauth_redirect`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** location.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1499)

## Record · Email queue

[Record definition](../../../../data/record-types/email_queue.json)

<a id="op-20f244adcb631f"></a>
### Email Queue.onload

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_onload`

**Inputs** self.

**Local steps**

- Evaluate self.set\_onload(“mute\_emails”, bool(are\_emails\_muted())).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L84) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1358) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L131)

<a id="op-c7bc538506a18a"></a>
### Email Queue.set recipients

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_set_recipients`

**Inputs** self, recipients.

**Local steps**

- Evaluate self.set(“recipients”, list()).
- For each r in recipients.
  - Evaluate self.append(“recipients”, mapping(“recipient” → r.strip(), “status” → “Not Sent”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L169) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1364) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L137)

<a id="op-7405117be0698c"></a>
### Email Queue.on trash

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.prevent\_email\_queue\_delete().

If control reaches the end, it returns no value.

**Methods declared on this owner** [prevent email queue delete](operations-014.md#op-7a58e55ce8c43d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L330) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L130)

<a id="op-7a58e55ce8c43d"></a>
### Email Queue.prevent email queue delete

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_prevent_email_queue_delete`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only Administrator can delete Email Queue”.

**Local steps**

- If Platform.session.user differs from “Administrator”.
  - Call the validation error handler Platform.throw(translated “Only Administrator can delete Email Queue”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L381) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L132)

<a id="op-e0e2cf62296d2d"></a>
### Email Queue.get duplicate

`operation_foundation_email_record_definitions_email_queue_business_behavior_email_queue_get_duplicate`

**Inputs** self, recipients.

**Record and data access** resolve a document from values via get\_doc.

**Explicit results** duplicate.

**Local steps**

- Set values from self.as\_dict().
- Remove values at “name”.
- Set duplicate from Platform.get\_doc(values).
- Evaluate duplicate.set\_recipients(recipients).
- Return duplicate.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0226.json#L481) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L126)
