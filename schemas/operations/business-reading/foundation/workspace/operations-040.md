# Forms, reports and navigation · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Load

<a id="op-fc811bdac60259"></a>
### Get tags

`operation_foundation_desk_form_load_business_behavior_get_tags`

**Inputs** doctype, name.

**Declared result** str.

**Record and data access** read “Tag Link” via get\_all.

**Explicit results** empty text · “,”.join(tags).

**Local steps**

- Bind dependencies has\_tags.
- If not has\_tags(doctype).
  - Return empty text.
- Set tags from Platform.get\_all(“Tag Link”, filters = mapping(“document\_type” → doctype, “document\_name” → str(name)), fields = list(“tag”), pluck = “tag”).
- Return “,”.join(tags).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L6284) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L240)

<a id="op-158919f263f3da"></a>
### Get document email

`operation_foundation_desk_form_load_business_behavior_get_document_email`

**Inputs** doctype, name.

**Explicit results** no value · formatted text {email at 0}+{quote(doctype, safe = empty text)}={quote(cstr(name), safe = empty text)}@{email at 1}.

**Local steps**

- Bind dependencies get\_automatic\_email\_link.
- Set email from get\_automatic\_email\_link().
- If not email.
  - Return no value.
- Set email from email.split(“@”).
- Return formatted text {email at 0}+{quote(doctype, safe = empty text)}={quote(cstr(name), safe = empty text)}@{email at 1}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L6522) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L236)

<a id="op-d49e5f2fcebd4c"></a>
### Get additional timeline content

`operation_foundation_desk_form_load_business_behavior_get_additional_timeline_content`

**Inputs** doctype, docname.

**Explicit results** contents.

**Local steps**

- Set contents from list().
- Set hooks from Platform.get\_hooks().get(“additional\_timeline\_content”, mapping()).
- Set methods\_for\_all\_doctype from hooks.get(“\*”, list()).
- Set methods\_for\_current\_doctype from hooks.get(doctype, list()).
- For each method in (methods\_for\_all\_doctype + methods\_for\_current\_doctype).
  - Evaluate contents.extend((Platform.get\_attr(method)(doctype, docname) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method)(doctype, docname) → list().
- Return contents.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(), Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L6775) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L228)

<a id="op-30c20edb504033"></a>
### Set link titles

`operation_foundation_desk_form_load_business_behavior_set_link_titles`

**Inputs** doc.

**Local steps**

- Set link\_titles from mapping().
- Evaluate link\_titles.update(get\_title\_values\_for\_link\_and\_dynamic\_link\_fields(doc)).
- Evaluate link\_titles.update(get\_title\_values\_for\_table\_and\_multiselect\_fields(doc)).
- Evaluate send\_link\_titles(link\_titles).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L7030) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L249)

<a id="op-e6a0582d8f4cb5"></a>
### Get title values for link and dynamic link fields

`operation_foundation_desk_form_load_business_behavior_get_title_values_for_link_and_dynamic_link_fields`

**Inputs** doc, link\_fields = no value.

**Record and data access** read doctype via get\_value.

**Explicit results** link\_titles.

**Local steps**

- Set link\_titles from mapping().
- If not link\_fields.
  - Set meta from Platform.get\_meta(doc.doctype).
  - Set link\_fields from (meta.get\_link\_fields() + meta.get\_dynamic\_link\_fields()).
- For each field in link\_fields.
  - If not doc\_fieldvalue bound to getattr(doc, field.fieldname, no value).
    - Continue with the next iteration or loop test.
  - Set doctype from field.options when field.fieldtype equals “Link”, otherwise doc.get(field.options).
    - Value choice on field.fieldtype equals “Link” — true gives field.options, false gives doc.get(field.options).
  - Set meta from Platform.get\_meta(doctype) when doctype, otherwise no value.
    - Value choice on doctype — true gives Platform.get\_meta(doctype), false gives no value.
  - If (not meta or not meta.title\_field or not meta.show\_title\_field\_in\_link).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not meta → not meta.title\_field → not meta.show\_title\_field\_in\_link.
    - Continue with the next iteration or loop test.
  - Set link\_title from Platform.db.get\_value(doctype, doc\_fieldvalue, meta.title\_field, cache = true, order\_by = no value).
  - Evaluate link\_titles.update(mapping(((doctype + “::”) + doc\_fieldvalue) → (link\_title or doc\_fieldvalue))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in link\_title → doc\_fieldvalue.
- Return link\_titles.

**Values supplied outside this operation** selected callable from getattr(doc, field.fieldname, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L7169) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L241)

<a id="op-06aae5b4835316"></a>
### Get title values for table and multiselect fields

`operation_foundation_desk_form_load_business_behavior_get_title_values_for_table_and_multiselect_fields`

**Inputs** doc, table\_fields = no value.

**Explicit results** link\_titles.

**Local steps**

- Set link\_titles from mapping().
- If not table\_fields.
  - Set meta from Platform.get\_meta(doc.doctype).
  - Set table\_fields from meta.get\_table\_fields(include\_computed = true).
- For each field in table\_fields.
  - If not doc.get(field.fieldname).
    - Continue with the next iteration or loop test.
  - For each value in doc.get(field.fieldname).
    - Evaluate link\_titles.update(get\_title\_values\_for\_link\_and\_dynamic\_link\_fields(value)).
- Return link\_titles.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L242)

<a id="op-a5c73e10dbfdf2"></a>
### Update user info

`operation_foundation_desk_form_load_business_behavior_update_user_info`

**Inputs** docinfo, doc = no value.

**Local steps**

- Set users from set().
- If doc.
  - For each field in tuple(“owner”, “modified\_by”).
    - If user bound to doc.get(field).
      - Evaluate users.add(user).
- Evaluate users.update(generator of d.sender for d drawn from docinfo.communications).
  - Draw d from docinfo.communications.
- Evaluate users.update(generator of d.user for d drawn from docinfo.shared).
  - Draw d from docinfo.shared.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.assignments).
  - Draw d from docinfo.assignments.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.views).
  - Draw d from docinfo.views.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.workflow\_logs).
  - Draw d from docinfo.workflow\_logs.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.like\_logs).
  - Draw d from docinfo.like\_logs.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.info\_logs).
  - Draw d from docinfo.info\_logs.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.attachment\_logs).
  - Draw d from docinfo.attachment\_logs.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.assignment\_logs).
  - Draw d from docinfo.assignment\_logs.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.comments).
  - Draw d from docinfo.comments.
- Evaluate users.update(generator of d.owner for d drawn from docinfo.versions).
  - Draw d from docinfo.versions.
- Evaluate Platform.utils.add\_user\_info(users, docinfo.user\_info).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L399) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L250)

<a id="op-937b0f5641686a"></a>
### Get user info for viewers

`operation_foundation_desk_form_load_business_behavior_get_user_info_for_viewers`

**Inputs** users.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** user\_info.

**Local steps**

- Set user\_info from mapping().
- For each user in Platform.parse\_json(users).
  - Evaluate Platform.utils.add\_user\_info(user, user\_info).
- Return user\_info.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L64) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L243)

## Service · Login

<a id="op-61e15abe69ec88"></a>
### Get context

`operation_foundation_public_pages_login_business_behavior_get_context`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** context.

**Explicit result forms** a value selected from the current context.

**Locally raised failures** Redirect.

**Observed service boundaries** record lookup.

**Local structure** 14 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L66) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L43)

<a id="op-b7f02aff29e0d3"></a>
### Login via token

`operation_foundation_public_pages_login_business_behavior_login_via_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** login\_token.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L4038) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L46)

<a id="op-83d0afebf8654f"></a>
### Get login with email link ratelimit

`operation_foundation_public_pages_login_business_behavior_get_login_with_email_link_ratelimit`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L4382) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L44)

<a id="op-d9170ded4333ca"></a>
### Send login link

`operation_foundation_public_pages_login_business_behavior_send_login_link`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** email.

**Explicit result forms** no value.

**Observed service boundaries** diagnostic or audit logging, notification or queued-work request.

**Local structure** 1 condition or selection sites, 0 statement loops and 3 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L4445) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L48)

<a id="op-a8810683c23d68"></a>
### Generate temporary login link

`operation_foundation_public_pages_login_business_behavior_generate_temporary_login_link`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** email, expiry.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, record mutation request, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L5133) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L42)

<a id="op-28559221341405"></a>
### Login via key

`operation_foundation_public_pages_login_business_behavior_login_via_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** key.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L5488) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L45)

<a id="op-7b79ea887487c6"></a>
### Sanitize redirect

`operation_foundation_public_pages_login_business_behavior_sanitize_redirect`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** redirect.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L67) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L47)

## Service · Logout

<a id="op-ffd6ad7bb96dbc"></a>
### Get context

`operation_foundation_public_pages_logout_business_behavior_get_context`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L6217) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L49)

## Service · Loop

<a id="op-3913c569fac1e8"></a>
### Agent Runner.initialize

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_init`

**Inputs** self, prompt, page\_context\_json, model, api\_key, user (named only, default no value), page\_id (named only, default no value), session\_id (named only, default no value), selected\_block\_ids (named only, default no value), image\_url (named only, default no value).

**Local steps**

- Set self.prompt from prompt.
- Set self.page\_context\_json from page\_context\_json.
- Set self.model from model.
- Set self.api\_key from api\_key.
- Set self.user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set self.page\_id from page\_id.
- Set self.session\_id from session\_id.
- Set self.selected\_block\_ids from (selected\_block\_ids or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in selected\_block\_ids → list().
- Set self.image\_url from image\_url.
- Set is\_standard from self.is\_standard().
- Set self.registry from get\_tool\_registry\_for\_mode(is\_standard).
- Set self.system\_prompt from get\_system\_prompt\_for\_mode(is\_standard).
- Set self.tree from no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is standard](operations-040.md#op-cde2741522c39e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L68) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1755) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1731)

<a id="op-cde2741522c39e"></a>
### Agent Runner.is standard

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_is_standard`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Studio Page” via get\_value.

**Explicit results** false · bool(Platform.db.get\_value(“Studio Page”, self.page\_id, “is\_standard”)).

**Local steps**

- If not self.page\_id.
  - Return false.
- Return bool(Platform.db.get\_value(“Studio Page”, self.page\_id, “is\_standard”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L71) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1734)

<a id="op-5b32f4739896fb"></a>
### Agent Runner.cancel key

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_cancel_key`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** formatted text studio\_ai\_cancel:{self.session\_id} when self.session\_id, otherwise no value.

**Local steps**

- Return formatted text studio\_ai\_cancel:{self.session\_id} when self.session\_id, otherwise no value.
  - Value choice on self.session\_id — true gives formatted text studio\_ai\_cancel:{self.session\_id}, false gives no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1723)

<a id="op-d9fa1b3adf716a"></a>
### Agent Runner.is cancelled

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_is_cancelled`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool(Platform.cache.get\_value(key, use\_local\_cache = false)) when key, otherwise false.

**Local steps**

- Set key from self.\_cancel\_key().
- Return bool(Platform.cache.get\_value(key, use\_local\_cache = false)) when key, otherwise false.
  - Value choice on key — true gives bool(Platform.cache.get\_value(key, use\_local\_cache = false)), false gives false.

**Methods declared on this owner** [cancel key](operations-040.md#op-5b32f4739896fb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1733)

<a id="op-e666ee7a0549bf"></a>
### Agent Runner.clear cancel flag

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_clear_cancel_flag`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If key bound to self.\_cancel\_key().
  - Evaluate Platform.cache.delete\_value(key).

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel key](operations-040.md#op-5b32f4739896fb).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1725)

<a id="op-6dce086517af83"></a>
### Agent Runner.interruptible sleep

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_interruptible_sleep`

**Inputs** self, seconds.

**Declared result** no value.

**Explicit failure paths** CancelledError.

**Local steps**

- Set waited from 0.0.
- While waited &lt; seconds.
  - If self.is\_cancelled().
    - Raise CancelledError.
  - Set step from min(0.25, (seconds − waited)).
  - Evaluate time.sleep(step).
  - Update waited using + step.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is cancelled](operations-040.md#op-d9fa1b3adf716a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1756) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1732)

<a id="op-8b8bf62345f56d"></a>
### Agent Runner.emit

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_emit`

**Inputs** self, suffix, remaining named values kwargs.

**State and service calls** publish realtime with event.

**Local steps**

- Set event from formatted text {EVENT\_PREFIX}\_{suffix}.
- If self.page\_id.
  - Set event from formatted text {event}\_{self.page\_id}.
- Evaluate Platform.publish\_realtime(event, mapping(“page\_id” → self.page\_id, expand kwargs), user = self.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(event, mapping(“page\_id” → self.page\_id, expand kwargs), user = self.user).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L65) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1728)

<a id="op-4297a01d5e1634"></a>
### Agent Runner.page root

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_page_root`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · data when isinstance(data, dict), otherwise no value.

**Local steps**

- Attempt the following.
  - Set data from json.loads(self.page\_context\_json).
- On failure (tuple(json.JSONDecodeError, TypeError)).
  - Return no value.
- If isinstance(data, list).
  - Set data from data at 0 when data, otherwise no value.
    - Value choice on data — true gives data at 0, false gives no value.
- Return data when isinstance(data, dict), otherwise no value.
  - Value choice on isinstance(data, dict) — true gives data, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1735)
