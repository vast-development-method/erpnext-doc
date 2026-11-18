# Workflow, automation and dispatch · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Auth

<a id="op-f5c88a5d4da666"></a>
### Get local client

`operation_foundation_realtime_auth_business_behavior_get_local_client`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L3355) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L217)

<a id="op-f6e33aba9916d7"></a>
### Make local request

`operation_foundation_realtime_auth_business_behavior_make_local_request`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** headers.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L3468) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L220)

<a id="op-00a37146b6e1df"></a>
### Make local request.call

`operation_foundation_realtime_auth_business_behavior_make_local_request_call`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** path, method, params, body.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** ValueError.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L4024) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L221)

<a id="op-dc8c36b1bc5bd2"></a>
### Make local request.request

`operation_foundation_realtime_auth_business_behavior_make_local_request_request`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** path, method, params, body.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L4387) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L222)

<a id="op-3d514fa2effe6b"></a>
### Auth headers

`operation_foundation_realtime_auth_business_behavior_authentication_headers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** credentials, site, secret.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L4529) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L212)

<a id="op-7d3b5956a1e9a3"></a>
### Get user info

`operation_foundation_realtime_auth_business_behavior_get_user_info`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** request.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L4655) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L219)

<a id="op-c27f29694bd941"></a>
### Make session

`operation_foundation_realtime_auth_business_behavior_make_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** site, user\_info, request.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L5054) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L225)

<a id="op-730307ab33298f"></a>
### Get socketio secret

`operation_foundation_realtime_auth_business_behavior_get_realtime_transport_secret`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** redis\_url.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L5234) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L218)

<a id="op-6189cec006be06"></a>
### Discarding Cookie Jar.extract cookies

`operation_foundation_realtime_auth_business_behavior_discarding_cookie_jar_extract_cookies`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, response, request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L5523) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L215)

<a id="op-c32898b4b082b3"></a>
### Get http client

`operation_foundation_realtime_auth_business_behavior_get_hypertext_transfer_protocol_client`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L5570) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L216)

<a id="op-91cbb4558e3d88"></a>
### Close clients

`operation_foundation_realtime_auth_business_behavior_close_clients`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0322.json#L5703) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L213)

## Record · Auto repeat

[Record definition](../../../../data/record-types/auto_repeat.json)

<a id="op-145cd5f1992b75"></a>
### Auto Repeat.validate

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_validate`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- Evaluate self.validate\_reference\_doctype().
- Evaluate self.validate\_reference\_permission().
- Evaluate self.validate\_submit\_on\_creation().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_email\_id().
- Evaluate self.validate\_auto\_repeat\_days().
- Evaluate self.set\_dates().
- Evaluate self.update\_auto\_repeat\_id().
- Evaluate self.unlink\_if\_applicable().
- Evaluate validate\_template((self.subject or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.subject → empty text.
- Evaluate validate\_template((self.message or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.message → empty text.

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-007.md#op-c60d805cee8090), [validate reference doctype](operations-006.md#op-a4d3e9cec17d09), [validate reference permission](operations-006.md#op-3c785ef8362c20), [validate submit on creation](operations-006.md#op-713ffcd36d105a), [validate dates](operations-006.md#op-3cfb46e26a60ac), [validate email id](operations-006.md#op-57290c7fae13f7), [validate auto repeat days](operations-006.md#op-6362024a09f0ea), [set dates](operations-006.md#op-d2bc8e492633c9), [update auto repeat id](operations-006.md#op-67b84413155d79), [unlink if applicable](operations-006.md#op-cdd9692b16bd0c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L612) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L233) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L209)

<a id="op-e1391614b41062"></a>
### Auto Repeat.before insert

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_before_insert`

**Inputs** self.

**Local steps**

- If not Platform.in\_test.
  - Set today\_date from getdate().
  - If getdate(self.start\_date) &lt; today\_date.
    - Set self.start\_date from today\_date.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L912) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L187)

<a id="op-a385051ce78f3f"></a>
### Auto Repeat.on update

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_on_update`

**Inputs** self.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**Local steps**

- Evaluate Platform.get\_doc(self.reference\_doctype, self.reference\_document).notify\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L1039) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L201)

<a id="op-e7385df53224c4"></a>
### Auto Repeat.on trash

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_on_trash`

**Inputs** self.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**State and service calls** request set\_value on self.reference\_doctype.

**Local steps**

- Evaluate Platform.db.set\_value(self.reference\_doctype, self.reference\_document, “auto\_repeat”, empty text).
- Evaluate Platform.get\_doc(self.reference\_doctype, self.reference\_document).notify\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L1116) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L200)

<a id="op-d2bc8e492633c9"></a>
### Auto Repeat.set dates

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_set_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The Next Scheduled Date cannot be later than the End Date.”.

**Local steps**

- If self.disabled.
  - Set self.next\_schedule\_date from no value.
- Otherwise.
  - Set self.next\_schedule\_date from self.get\_next\_schedule\_date(schedule\_date = self.start\_date).
  - If (self.end\_date and getdate(self.end\_date) &lt; getdate(self.next\_schedule\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end\_date → getdate(self.end\_date) &lt; getdate(self.next\_schedule\_date).
    - Call the validation error handler Platform.throw(translated “The Next Scheduled Date cannot be later than the End Date.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get next schedule date](operations-007.md#op-f78d102469ea91).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L1245) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L228) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L204)

<a id="op-cdd9692b16bd0c"></a>
### Auto Repeat.unlink if applicable

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_unlink_if_applicable`

**Inputs** self.

**State and service calls** request set\_value on self.reference\_doctype.

**Local steps**

- If (self.status equals “Completed” or self.disabled).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.status equals “Completed” → self.disabled.
  - Evaluate Platform.db.set\_value(self.reference\_doctype, self.reference\_document, “auto\_repeat”, empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L1462) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L205)

<a id="op-a4d3e9cec17d09"></a>
### Auto Repeat.validate reference doctype

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_validate_reference_record_type`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Enable Allow Auto Repeat for the doctype {0} in Customize Form”.format(self.reference\_doctype).

**Local steps**

- If (Platform.in\_test or Platform.flags.in\_patch).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.in\_test → Platform.flags.in\_patch.
  - Return no value.
- If not Platform.get\_meta(self.reference\_doctype).allow\_auto\_repeat.
  - Call the validation error handler Platform.throw(translated “Enable Allow Auto Repeat for the doctype {0} in Customize Form”.format(self.reference\_doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L1585) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L214)

<a id="op-3c785ef8362c20"></a>
### Auto Repeat.validate reference permission

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_validate_reference_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L1752) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L237) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L213)

<a id="op-713ffcd36d105a"></a>
### Auto Repeat.validate submit on creation

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_validate_submit_on_creation`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot enable {0} for a non-submittable doctype”.format(Platform.bold(translated “Submit on Creation”)).

**Local steps**

- If (self.submit\_on\_creation and not Platform.get\_meta(self.reference\_doctype).is\_submittable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.submit\_on\_creation → not Platform.get\_meta(self.reference\_doctype).is\_submittable.
  - Call the validation error handler Platform.throw(translated “Cannot enable {0} for a non-submittable doctype”.format(Platform.bold(translated “Submit on Creation”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L1959) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L215)

<a id="op-3cfb46e26a60ac"></a>
### Auto Repeat.validate dates

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_validate_dates`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “End Date cannot be today.” · validation helper — translated “{0} should not be same as {1}”.format(Platform.bold(translated “End Date”), Platform.bold(translated “Start Date”)).

**Local steps**

- If Platform.flags.in\_patch.
  - Return no value.
- If self.end\_date.
  - Set end\_date from getdate(self.end\_date).
  - Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
  - If end\_date equals getdate().
    - Call the validation error handler Platform.throw(translated “End Date cannot be today.”).
  - If end\_date equals getdate(self.start\_date).
    - Call the validation error handler Platform.throw(translated “{0} should not be same as {1}”.format(Platform.bold(translated “End Date”), Platform.bold(translated “Start Date”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L2129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L235) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L211)

<a id="op-57290c7fae13f7"></a>
### Auto Repeat.validate email id

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_validate_email_identifier`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is an invalid email address in 'Recipients'”.format(email) · validation helper — translated “'Recipients' not specified”.

**Local steps**

- If self.notify\_by\_email.
  - If self.recipients.
    - Set email\_list from split\_emails(self.recipients.replace(whitespace '\\n', empty text)).
    - Bind dependencies validate\_email\_address.
    - For each email in email\_list.
      - If not validate\_email\_address(email).
        - Call the validation error handler Platform.throw(translated “{0} is an invalid email address in 'Recipients'”.format(email)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “'Recipients' not specified”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L2493) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L236) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L212)

<a id="op-6362024a09f0ea"></a>
### Auto Repeat.validate auto repeat days

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_validate_auto_repeat_days`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Auto Repeat Day{0} {1} has been repeated.”.format(plural, Platform.bold(“, ”.join(repeated\_days))).

**Local steps**

- Set auto\_repeat\_days from self.get\_auto\_repeat\_days().
- If len(set(auto\_repeat\_days)) differs from len(auto\_repeat\_days).
  - Set repeated\_days from get\_repeated(auto\_repeat\_days).
  - Set plural from “s” when len(repeated\_days) &gt; 1, otherwise empty text.
    - Value choice on len(repeated\_days) &gt; 1 — true gives “s”, false gives empty text.
  - Call the validation error handler Platform.throw(translated “Auto Repeat Day{0} {1} has been repeated.”.format(plural, Platform.bold(“, ”.join(repeated\_days)))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get auto repeat days](operations-007.md#op-30e46ef82d0a3d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L2748) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L210)

<a id="op-67b84413155d79"></a>
### Auto Repeat.update auto repeat id

`operation_foundation_automation_record_definitions_auto_repeat_business_behavior_auto_repeat_update_auto_repeat_identifier`

**Inputs** self.

**Record and data access** read self.reference\_doctype via get\_value.

**State and service calls** request set\_value on self.reference\_doctype.

**Explicit failure paths** validation helper — translated “The {0} is already on auto repeat {1}”.format(self.reference\_document, auto\_repeat).

**Local steps**

- Set auto\_repeat from Platform.db.get\_value(self.reference\_doctype, self.reference\_document, “auto\_repeat”).
- If (auto\_repeat and auto\_repeat differs from self.name and not Platform.flags.in\_patch).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in auto\_repeat → auto\_repeat differs from self.name → not Platform.flags.in\_patch.
  - Call the validation error handler Platform.throw(translated “The {0} is already on auto repeat {1}”.format(self.reference\_document, auto\_repeat)).
- Otherwise.
  - Evaluate Platform.db.set\_value(self.reference\_doctype, self.reference\_document, “auto\_repeat”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0013.json#L3030) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L206)
