# Integration and transport · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Platformmail

<a id="op-ff7b67553344bf"></a>
### Platform Mail.send raw

`operation_foundation_email_frappemail_business_behavior_foundation_mail_send_raw`

**Inputs** self, sender, recipients, message, is\_newsletter = false.

**Declared result** no value.

**Local steps**

- Set session\_id from str(uuid.uuid4()).
- Set endpoint from “/outbound/send-raw”.
- If isinstance(message, str).
  - Set message from message.encode(“utf-8”).
- Set total\_size from len(message).
- Set total\_chunks from math.ceil((total\_size ÷ CHUNK\_SIZE)).
- For each i in range(total\_chunks).
  - Set start from (i × CHUNK\_SIZE).
  - Set end from (start + CHUNK\_SIZE).
  - Set chunk from message at slice start to end.
  - Set files from mapping(“raw\_message” → tuple(“raw\_message.eml”, chunk)).
  - Set data from mapping(“from\_” → sender, “to” → recipients, “is\_newsletter” → is\_newsletter, “uuid” → session\_id, …).
  - Evaluate self.request(“POST”, endpoint = endpoint, data = data, files = files).

If control reaches the end, it returns no value.

**Methods declared on this owner** [request](operations-026.md#op-30c8cfc34c6cf0).

**Values supplied outside this operation** clock or generated value from uuid.uuid4().

**Boundaries to resolve** external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L3591) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1057) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1490)

<a id="op-c548b586a6d37b"></a>
### Platform Mail.pull raw

`operation_foundation_email_frappemail_business_behavior_foundation_mail_pull_raw`

**Inputs** self, mailbox = “inbox”, limit = 50, last\_received\_at = no value.

**Declared result** dict at tuple(str, (str bitwise or list at str)).

**Explicit results** mapping(“latest\_messages” → response at “mails”, “last\_received\_at” → last\_received\_at).

**Local steps**

- Set endpoint from “/inbound/pull-raw”.
- If last\_received\_at.
  - Set last\_received\_at from add\_or\_update\_tzinfo(last\_received\_at).
- Set data from mapping(“mailbox” → mailbox, “limit” → limit, “last\_received\_at” → last\_received\_at).
- Set headers from mapping(“X-Site” → Platform.utils.get\_url()).
- Set response from self.request(“GET”, endpoint = endpoint, data = data, headers = headers, raw\_response = true).
- Set last\_received\_at from convert\_utc\_to\_system\_timezone(get\_datetime(response at “last\_received\_at”)).
- Return mapping(“latest\_messages” → response at “mails”, “last\_received\_at” → last\_received\_at).

**Methods declared on this owner** [request](operations-026.md#op-30c8cfc34c6cf0).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L4146) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1055) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1488)

<a id="op-9c2011dff3c811"></a>
### Add or update tzinfo

`operation_foundation_email_frappemail_business_behavior_add_or_update_tzinfo`

**Inputs** date\_time, timezone = no value.

**Declared result** str.

**Explicit results** str(date\_time).

**Local steps**

- Set date\_time from get\_datetime(date\_time).
- Set target\_tz from ZoneInfo((timezone or get\_system\_timezone())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in timezone → get\_system\_timezone().
- If date\_time.tzinfo is identical to no value.
  - Set date\_time from date\_time.replace(tzinfo = target\_tz).
- Otherwise.
  - Set date\_time from date\_time.astimezone(target\_tz).
- Return str(date\_time).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L4585) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1052) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1485)

<a id="op-1320a7aae9a0b3"></a>
### Raise for status

`operation_foundation_email_frappemail_business_behavior_raise_for_status`

**Inputs** response.

**Declared result** no value.

**Explicit failure paths** requests.exceptions.HTTPError(message, response = response).

**Local steps**

- If not response.ok.
  - Attempt the following.
    - Set error\_text from response.json().
  - On failure (Exception).
    - Set error\_text from response.text.strip().
  - Set message from translated “Error {0}: {1}”.format(response.status\_code, error\_text).
  - Raise requests.exceptions.HTTPError(message, response = response).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from requests.exceptions.HTTPError(message, response = response).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L4836) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1059) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1492)

## Service · Protocol

<a id="op-72a65afb4097ca"></a>
### Mcp Error.initialize

`operation_foundation_binding_foundation_mcp_protocol_mcperror_init`

**Inputs** self, code, message, status = 400, data = no value.

**Local steps**

- Evaluate super().\_\_init\_\_(message).
- Set self.code from code.
- Set self.http\_status\_code from status.
- Set self.data from data.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1505)

<a id="op-46a178764589ff"></a>
### Server info

`operation_foundation_binding_foundation_mcp_protocol_server_info`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, str).

**Explicit results** mapping(“name” → (name or default\_server\_name()), “version” → Platform.\_\_version\_\_).

**Local steps**

- Set name from (Platform.get\_system\_settings(“server\_name”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“server\_name”) → empty text.
- Return mapping(“name” → (name or default\_server\_name()), “version” → Platform.\_\_version\_\_).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → default\_server\_name().

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“server\_name”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1507)

<a id="op-061acf7c5e8935"></a>
### Default server name

`operation_foundation_binding_foundation_mcp_protocol_default_server_name`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** re.sub(“&#91;^a-z0-9&#93;+”, “\_”, get\_host\_name().lower()).strip(“\_”).

**Local steps**

- Return re.sub(“&#91;^a-z0-9&#93;+”, “\_”, get\_host\_name().lower()).strip(“\_”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1503)

<a id="op-5c3f0486273e09"></a>
### Server instructions

`operation_foundation_binding_foundation_mcp_protocol_server_instructions`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** instructions.

**Local steps**

- Set lines from list(“This is a Platform Framework site at {0}.”.format(get\_host\_name()), “You are connected as {0} ({1}).”.format(get\_fullname(), Platform.session.user), “Tool arguments take the same values as the matchi ….
- For each app in Platform.get\_installed\_apps().
  - Set title from (Platform.get\_hooks(“app\_title”, app\_name = app) or list(app)) at 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = app) → list(app).
  - Evaluate lines.append(formatted text - {title} ({app})).
- Set instructions from whitespace '\\n'.join(lines).
- If site\_instructions bound to (Platform.get\_system\_settings(“agent\_instructions”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“agent\_instructions”) → empty text.
  - Update instructions using + (whitespace '\\n\\n' + site\_instructions).
- Return instructions.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“app\_title”, app\_name = app) · configured or stored value from Platform.get\_system\_settings(“agent\_instructions”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1508)

<a id="op-5964cd51cac5cd"></a>
### Result envelope

`operation_foundation_binding_foundation_mcp_protocol_result_envelope`

**Inputs** request\_id, result, version.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping(“jsonrpc” → “2.0”, “id” → request\_id, “result” → result).

**Local steps**

- If version equals LATEST\_VERSION.
  - Set result from mapping(expand result, “resultType” → “complete”, “\_meta” → mapping(expand result.get(“\_meta”, mapping()), META\_SERVER → server\_info())).
- Otherwise.
  - Set result from mapping of key → value for tuple(key, value) drawn from result.items() where key does not belong to tuple(“ttlMs”, “cacheScope”).
    - Draw tuple(key, value) from result.items(), keep a combination only if (key does not belong to tuple(“ttlMs”, “cacheScope”)).
- Return mapping(“jsonrpc” → “2.0”, “id” → request\_id, “result” → result).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1506)

<a id="op-afa8fcbd6d6294"></a>
### Error envelope

`operation_foundation_binding_foundation_mcp_protocol_error_envelope`

**Inputs** request\_id, error, version.

**Declared result** dict at tuple(str, Any).

**Explicit results** result.

**Local steps**

- Set result from mapping(“jsonrpc” → “2.0”, “error” → mapping(“code” → error.code, “message” → str(error))).
- If (request\_id is distinct from no value or version equals LEGACY\_VERSION).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in request\_id is distinct from no value → version equals LEGACY\_VERSION.
  - Set result at “id” from request\_id.
- If error.data is distinct from no value.
  - Set result at “error” at “data” from error.data.
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1504)

## Record · Push notification settings

[Record definition](../../../../data/record-types/push_notification_settings.json)

<a id="op-39f7e6d36b30d1"></a>
### Push Notification Settings.validate

`operation_foundation_integrations_record_definitions_push_notification_settings_business_behavior_push_notification_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_relay\_server\_setup().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate relay server setup](operations-027.md#op-c96349022481d8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L3076) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L67) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L793)

<a id="op-c96349022481d8"></a>
### Push Notification Settings.validate relay server setup

`operation_foundation_integrations_record_definitions_push_notification_settings_business_behavior_push_notification_settings_validate_relay_server_setup`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The Push Relay Server URL key (′push\_relay\_server\_url′) is missing in your site config”.

**Local steps**

- If (self.enable\_push\_notification\_relay and not Platform.conf.get(“push\_relay\_server\_url”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_push\_notification\_relay → not Platform.conf.get(“push\_relay\_server\_url”).
  - Call the validation error handler Platform.throw(translated “The Push Relay Server URL key (′push\_relay\_server\_url′) is missing in your site config”, title = translated “Relay Server URL missing”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0254.json#L3127) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L68) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L794)

## Service · Queue

<a id="op-e9444c70974073"></a>
### Get emails sent this month

`operation_foundation_email_queue_business_behavior_get_emails_sent_this_month`

**Inputs** email\_account = no value.

**Record and data access** read “Email Queue” via count.

**Explicit results** Platform.db.count(“Email Queue”, filters = filters).

**Local steps**

- Set today from getdate().
- Set month\_start from today.replace(day = 1).
- Set filters from mapping(“status” → “Sent”, “creation” → list(“&gt;=”, str(month\_start))).
- If email\_account.
  - Set filters at “email\_account” from email\_account.
- Return Platform.db.count(“Email Queue”, filters = filters).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L968) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1085) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1517)

<a id="op-7d4e5bd21e974d"></a>
### Get emails sent today

`operation_foundation_email_queue_business_behavior_get_emails_sent_today`

**Inputs** email\_account = no value.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(q, q\_args) at 0 at 0.

**Local steps**

- Set q from query text (SELECT, Email Queue).
- Set q\_args from mapping().
- If email\_account is distinct from no value.
  - If email\_account.
    - Update q using + “ AND email\_account = %(email\_account)s”.
    - Set q\_args at “email\_account” from email\_account.
  - Otherwise.
    - Update q using + “ AND (email\_account is null OR email\_account='')”.
- Return Platform.db.sql(q, q\_args) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L76) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1086) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1518)

<a id="op-fe501e7430ed9b"></a>
### Get unsubscribe message

`operation_foundation_email_queue_business_behavior_get_unsubscribe_message`

**Inputs** unsubscribe\_message, expose\_recipients.

**Declared result** “Platform.\_dict&#91;str, str&#93;”.

**Explicit results** Platform.\_dict(html = html, text = text).

**Local steps**

- Set unsubscribe\_message from (unsubscribe\_message or translated “Unsubscribe”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in unsubscribe\_message → translated “Unsubscribe”.
- Set unsubscribe\_link from formatted text &lt;a href="&lt;!--unsubscribe\_url--&gt;" target="\_blank"&gt;{unsubscribe\_message}&lt;/a&gt;.
- Set unsubscribe\_html from translated “{0} to stop receiving emails of this type”.format(unsubscribe\_link).
- Set html from formatted text &lt;div class="email-unsubscribe"&gt;  &lt;!--cc\_message--&gt;  &lt;div&gt;  {unsubscribe\_html}  &lt;/div&gt;  &lt;/div&gt;.
- Set text from formatted text   {unsubscribe\_message}: &lt;!--unsubscribe\_url--&gt;.
- If expose\_recipients equals “footer”.
  - Set text from formatted text  &lt;!--cc\_message--&gt;{text}.
- Return Platform.\_dict(html = html, text = text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L1518) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1089) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1521)

<a id="op-4af56c55fcb39f"></a>
### Get unsubcribed url

`operation_foundation_email_queue_business_behavior_get_unsubcribed_resource_address`

**Inputs** reference\_doctype, reference\_name, email, unsubscribe\_method, unsubscribe\_params.

**Explicit results** get\_url(((unsubscribe\_method + “?”) + get\_signed\_params(params))).

**Local steps**

- Set params from mapping(“email” → cstr(email), “doctype” → cstr(reference\_doctype), “name” → cstr(reference\_name)).
- If unsubscribe\_params.
  - Evaluate params.update(Platform.parse\_json(unsubscribe\_params)).
- Return get\_url(((unsubscribe\_method + “?”) + get\_signed\_params(params))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L1858) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1088) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1520)

<a id="op-c651a1b6d40ecc"></a>
### Unsubscribe

`operation_foundation_email_queue_business_behavior_unsubscribe`

**Inputs** doctype, name, email.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Record and data access** resolve a document from mapping(“doctype” → “Email Unsubscribe”, “email” → email, “reference\_doctype” → doctype, “reference\_name” → name) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Email Unsubscribe”, “email” → email, “reference\_doctype” → doctype, “reference\_name” → name)) · rollback · commit.

**Explicit results** no value.

**Local steps**

- If (not Platform.in\_test and not verify\_request()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.in\_test → not verify\_request().
  - Return no value.
- Attempt the following.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Email Unsubscribe”, “email” → email, “reference\_doctype” → doctype, “reference\_name” → name)).insert(ignore\_permissions = true).
- On failure (Platform.DuplicateEntryError).
  - Evaluate Platform.db.rollback().
- When the protected block completes normally.
  - Evaluate Platform.db.commit().
- Evaluate return\_unsubscribed\_page(email, doctype, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L2120) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1092) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1524)

<a id="op-a2d1a5d443ac5c"></a>
### Return unsubscribed page

`operation_foundation_email_queue_business_behavior_return_unsubscribed_page`

**Inputs** email, doctype, name.

**Local steps**

- Evaluate Platform.respond\_as\_web\_page(translated “Unsubscribed”, translated “{0} has left the conversation in {1} {2}”.format(email, translated doctype, name), indicator\_color = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L2469) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1091) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1523)

<a id="op-11d2fc6966cd09"></a>
### Flush

`operation_foundation_email_queue_business_behavior_flush`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Email Queue” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Email Queue flushing aborted due to too many failures.”.

**Local steps**

- Bind dependencies EmailQueue.
- If Platform.are\_emails\_muted().
  - Evaluate msgprint(translated “Emails are muted”).
- If cint(Platform.db.get\_default(“suspend\_email\_queue”)) equals 1.
  - Return no value.
- Set email\_queue\_batch from get\_queue().
- If not email\_queue\_batch.
  - Return no value.
- Set failed\_email\_queues from list().
- For each row in email\_queue\_batch.
  - Attempt the following.
    - Set email\_queue from Platform.get\_doc(“Email Queue”, row.name, for\_update = true).
    - Evaluate email\_queue.send().
  - On failure (Exception).
    - Evaluate Platform.get\_doc(“Email Queue”, row.name).log\_error().
    - Evaluate failed\_email\_queues.append(row.name).
    - If ((len(failed\_email\_queues) ÷ len(email\_queue\_batch)) &gt; EMAIL\_QUEUE\_BATCH\_FAILURE\_THRESHOLD\_PERCENT and len(failed\_email\_queues) &gt; EMAIL\_QUEUE\_BATCH\_FAILURE\_THRESHOLD\_COUNT).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in (len(failed\_email\_queues) ÷ len(email\_queue\_batch)) &gt; EMAIL\_QUEUE\_BATCH\_FAILURE\_THRESHOLD\_PERCENT → len(failed\_email\_queues) &gt; EMAIL\_QUEUE\_BATCH\_FAILURE\_THRESHOLD\_COUNT.
      - Call the validation error handler Platform.throw(translated “Email Queue flushing aborted due to too many failures.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L2616) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1084) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1516)

<a id="op-78f87d236333b4"></a>
### Get queue

`operation_foundation_email_queue_business_behavior_get_queue`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Email Queue).

**Explicit results** Platform.db.sql(query text (SELECT, Email Queue), mapping(“now” → now\_datetime(), “undo\_window” → undo\_window, “batch\_size” → batch\_size), as\_dict = true).

**Local steps**

- Set batch\_size from (cint(Platform.conf.email\_queue\_batch\_size) or 500).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.conf.email\_queue\_batch\_size) → 500.
- Set undo\_window from add\_to\_date(now\_datetime(), seconds = negative 10).
- Return Platform.db.sql(query text (SELECT, Email Queue), mapping(“now” → now\_datetime(), “undo\_window” → undo\_window, “batch\_size” → batch\_size), as\_dict = true).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L3133) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1087) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1519)

<a id="op-72c3ee2737d791"></a>
### Retry sending emails

`operation_foundation_email_queue_business_behavior_retry_sending_emails`

**Inputs** no declared parameters.

**Record and data access** read “Email Queue” via get\_all · resolve a document from “Email Queue” via get\_doc.

**Local steps**

- Bind dependencies get\_email\_retry\_limit.
- Set emails\_in\_sending from Platform.get\_all(“Email Queue”, filters = mapping(“status” → “Sending”), fields = list(“name”, “modified”)).
- For each e in emails\_in\_sending.
  - If (now\_datetime() − e at “modified”) &gt; timedelta(minutes = 15).
    - Set update\_fields from mapping().
    - Set email\_queue from Platform.get\_doc(“Email Queue”, e at “name”).
    - Set sent\_to\_atleast\_one\_recipient from any(generator of rec.recipient for rec drawn from email\_queue.recipients where rec.is\_mail\_sent()).
      - Draw rec from email\_queue.recipients, keep a combination only if (rec.is\_mail\_sent()).
    - If email\_queue.retry &lt; get\_email\_retry\_limit().
      - Evaluate update\_fields.update(mapping(“status” → “Partially Sent” when sent\_to\_atleast\_one\_recipient, otherwise “Not Sent”, “retry” → (email\_queue.retry + 1))).
        - Value choice on sent\_to\_atleast\_one\_recipient — true gives “Partially Sent”, false gives “Not Sent”.
    - Otherwise.
      - Evaluate update\_fields.update(mapping(“status” → “Error”)).
      - Evaluate update\_fields.update(mapping(“error” → “Retry Limit Exceeded”)).
    - Evaluate email\_queue.update\_status(expanded names update\_fields, commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L3490) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1090) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1522)

## Service · Receive

<a id="op-e5696fdf1b657d"></a>
### Email Server.initialize

`operation_foundation_email_receive_business_behavior_email_server_initialize`

**Inputs** self, args = no value.

**Local steps**

- Set self.retry\_limit from 3.
- Set self.retry\_count from 0.
- Set self.settings from (args or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → Platform.\_dict().
- Set self.pop\_timeout from (self.settings.timeout or Platform.conf.pop\_timeout).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.settings.timeout → Platform.conf.pop\_timeout.
- Set self.imap\_timeout from (self.settings.timeout or Platform.conf.imap\_timeout).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.settings.timeout → Platform.conf.imap\_timeout.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L4055) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1112) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1544)

<a id="op-2e4639fb508fe8"></a>
### Email Server.connect

`operation_foundation_email_receive_business_behavior_email_server_connect`

**Inputs** self.

**Explicit results** self.connect\_imap() when cint(self.settings.use\_imap), otherwise self.connect\_pop().

**Local steps**

- Return self.connect\_imap() when cint(self.settings.use\_imap), otherwise self.connect\_pop().
  - Value choice on cint(self.settings.use\_imap) — true gives self.connect\_imap(), false gives self.connect\_pop().

**Methods declared on this owner** [connect imap](operations-027.md#op-2099c9308ed422), [connect pop](operations-028.md#op-0dbc3366ea8710).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L4254) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1105) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1537)

<a id="op-2099c9308ed422"></a>
### Email Server.connect imap

`operation_foundation_email_receive_business_behavior_email_server_connect_internet_message_access_protocol`

**Inputs** self.

**State and service calls** msgprint with translated “Invalid Mail Server. Please rectify and try again.”.

**Explicit results** true.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - If cint(self.settings.use\_ssl).
    - Set self.imap from imaplib.IMAP4\_SSL(self.settings.host, self.settings.incoming\_port, timeout = self.imap\_timeout, ssl\_context = ssl.create\_default\_context()).
  - Otherwise.
    - Set self.imap from imaplib.IMAP4(self.settings.host, self.settings.incoming\_port, timeout = self.imap\_timeout).
    - If cint(self.settings.use\_starttls).
      - Evaluate self.imap.starttls().
  - If self.settings.use\_oauth.
    - Evaluate Oauth(self.imap, self.settings.email\_account, self.settings.username, self.settings.access\_token).connect().
  - Otherwise.
    - Evaluate self.imap.login(self.settings.username, self.settings.password).
  - Return true.
- On failure (\_socket.error).
  - Evaluate Platform.msgprint(translated “Invalid Mail Server. Please rectify and try again.”).
  - Propagate the active failure.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0235.json#L4353) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1106) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1538)
