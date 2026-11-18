# Record lifecycle and persistence · operations 100

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · User

[Record definition](../../../../data/record-types/user.json)

<a id="op-18662d46ca51fb"></a>
### Needs password setup

`operation_foundation_binding_foundation_core_doctype_user_user_needs_password_setup`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** Boolean false, a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L668) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L644)

<a id="op-9bdec14d241936"></a>
### Set first password

`operation_foundation_binding_foundation_core_doctype_user_user_set_first_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** new\_password.

**Observed service boundaries** record lookup, record mutation request, validation or user-notification service.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L645)

<a id="op-f889f2aeebca3f"></a>
### Reset password

`operation_foundation_core_record_definitions_user_business_behavior_reset_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Observed service boundaries** diagnostic or audit logging, record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 3 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L6610) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L671)

<a id="op-e048183ee95645"></a>
### Change password

`operation_foundation_core_record_definitions_user_business_behavior_change_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, new\_password, logout\_all\_sessions.

**Observed service boundaries** effective access lookup, record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L7113) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L645)

<a id="op-57e636ea55cc2e"></a>
### User query

`operation_foundation_core_record_definitions_user_business_behavior_user_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.get\_list(doctype, filters = list\_filters, fields = list(“name”, “full\_name”), limit\_start = start, limit\_page\_length = page\_len, …).

**Local steps**

- Set doctype from “User”.
- Set list\_filters from mapping(“enabled” → 1, “docstatus” → list(“&lt;”, 2)).
- Set or\_filters from list(list(searchfield, “like”, formatted text %{txt}%)).
- If “name” belongs to searchfield.
  - Update or\_filters using + list of list(field, “like”, formatted text %{txt}%) for field drawn from tuple(“first\_name”, “middle\_name”, “last\_name”).
    - Draw field from tuple(“first\_name”, “middle\_name”, “last\_name”).
- If filters.
  - If not (filters.get(“ignore\_user\_type”) and Platform.session.data.user\_type equals “System User”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“ignore\_user\_type”) → Platform.session.data.user\_type equals “System User”.
    - Set list\_filters at “user\_type” from list(“!=”, “Website User”).
  - Evaluate filters.pop(“ignore\_user\_type”, no value).
  - Evaluate list\_filters.update(filters).
- Return Platform.get\_list(doctype, filters = list\_filters, fields = list(“name”, “full\_name”), limit\_start = start, limit\_page\_length = page\_len, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L708)

<a id="op-8a0c5290a750ec"></a>
### Get total users

`operation_foundation_core_record_definitions_user_business_behavior_get_total_users`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, User).format(“, ”.join((list(“%s”) × len(STANDARD\_USERS)))).

**Explicit results** flt(Platform.db.sql(query text (SELECT, User).format(nested operand in the contract.join((nested operand in the contract × nested operand in the contract))), STANDARD\_USERS) at 0 at 0).

**Local steps**

- Return flt(Platform.db.sql(query text (SELECT, User).format(nested operand in the contract.join((nested operand in the contract × nested operand in the contract))), STANDARD\_USERS) at 0 at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L646) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L663)

<a id="op-56f6bc266e645a"></a>
### Get system users

`operation_foundation_core_record_definitions_user_business_behavior_get_system_users`

**Inputs** exclude\_users = no value, limit = no value.

**Record and data access** read “User” via get\_all.

**Explicit results** Platform.get\_all(“User”, filters = mapping(“enabled” → 1, “user\_type” → tuple(“!=”, “Website User”), “name” → tuple(“not in”, \_excluded\_users)), pluck = “name”, limit = limit).

**Local steps**

- Set \_excluded\_users from list(STANDARD\_USERS).
- If isinstance(exclude\_users, str).
  - Evaluate \_excluded\_users.append(exclude\_users).
- Otherwise.
  - If isinstance(exclude\_users, Iterable).
    - Evaluate \_excluded\_users.extend(exclude\_users).
- Return Platform.get\_all(“User”, filters = mapping(“enabled” → 1, “user\_type” → tuple(“!=”, “Website User”), “name” → tuple(“not in”, \_excluded\_users)), pluck = “name”, limit = limit).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L862) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L660)

<a id="op-cc745d6eb35057"></a>
### Get active users

`operation_foundation_core_record_definitions_user_business_behavior_get_active_users`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, User).format(“, ”.join((list(“%s”) × len(STANDARD\_USERS)))).

**Explicit results** Platform.db.sql(query text (SELECT, User).format(“, ”.join((list(nested operand in the contract) × nested operand in the contract(nested operand in the contract)))), STANDARD\_USERS) at 0 at 0.

**Local steps**

- Return Platform.db.sql(query text (SELECT, User).format(“, ”.join((list(nested operand in the contract) × nested operand in the contract(nested operand in the contract)))), STANDARD\_USERS) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L1203) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L649)

<a id="op-0b062e45f26004"></a>
### Get website users

`operation_foundation_core_record_definitions_user_business_behavior_get_website_users`

**Inputs** no declared parameters.

**Record and data access** read “User” via count.

**Explicit results** Platform.db.count(“User”, filters = mapping(“enabled” → true, “user\_type” → “Website User”)).

**Local steps**

- Return Platform.db.count(“User”, filters = mapping(“enabled” → true, “user\_type” → “Website User”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L1449) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L665)

<a id="op-97c54a76b0695f"></a>
### Get active website users

`operation_foundation_core_record_definitions_user_business_behavior_get_active_website_users`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, User).

**Explicit results** Platform.db.sql(query text (SELECT, User)) at 0 at 0.

**Local steps**

- Return Platform.db.sql(query text (SELECT, User)) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L1547) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L650)

<a id="op-d2410eb45e827b"></a>
### Get permission query conditions

`operation_foundation_core_record_definitions_user_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L1709) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L658)

<a id="op-ed197385b41042"></a>
### Has permission

`operation_foundation_core_record_definitions_user_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, user.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L1852) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L506) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L668)

<a id="op-d798a59794c1da"></a>
### Notify admin access to system manager

`operation_foundation_core_record_definitions_user_business_behavior_notify_admin_access_to_system_manager`

**Inputs** login\_manager = no value.

**State and service calls** sendmail.

**Local steps**

- If (login\_manager and login\_manager.user equals “Administrator” and Platform.local.conf.notify\_admin\_access\_to\_system\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in login\_manager → login\_manager.user equals “Administrator” → Platform.local.conf.notify\_admin\_access\_to\_system\_manager.
  - Set date\_and\_time from format\_datetime(now\_datetime(), format\_string = “medium”).
  - Set ip\_address from Platform.local.request\_ip.
  - Evaluate Platform.sendmail(recipients = get\_system\_managers(), subject = translated “Administrator Logged In”, template = “administrator\_logged\_in”, args = mapping(“date\_and\_time” → date\_and\_time, “ip\_address” → ip ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime() · service or queued work from Platform.sendmail(recipients = get\_system\_managers(), subject = translated “Administrator Logged In”, template = “administrator\_logged\_in”, args = mapping(“date\_and\_time” → date\_and\_time, “ip\_address” → ip ….

**Boundaries to resolve** external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L1953) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L670)

<a id="op-eae2c2be6572cb"></a>
### Handle password test fail

`operation_foundation_core_record_definitions_user_business_behavior_handle_password_test_fail`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** feedback.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L2237) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L666)

<a id="op-2915830fdb373c"></a>
### Throttle user creation

`operation_foundation_core_record_definitions_user_business_behavior_throttle_user_creation`

**Inputs** no declared parameters.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Throttled”.

**Local steps**

- If Platform.flags.in\_import.
  - Return no value.
- If Platform.db.get\_creation\_count(“User”, 60) &gt; Platform.local.conf.get(“throttle\_user\_limit”, 60).
  - Call the validation error handler Platform.throw(translated “Throttled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L2693) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L676)

<a id="op-e5bcae94bc764c"></a>
### Get module profile

`operation_foundation_core_record_definitions_user_business_behavior_get_module_profile`

**Inputs** module\_profile.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Module Profile” via get\_doc.

**Explicit results** module\_profile.get(“block\_modules”).

**Local steps**

- Evaluate Platform.has\_permission(“Module Profile”, “read”, throw = true).
- Set module\_profile from Platform.get\_doc(“Module Profile”, mapping(“module\_profile\_name” → module\_profile)).
- Return module\_profile.get(“block\_modules”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Module Profile”, “read”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L45) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L656)

<a id="op-215967b080c374"></a>
### Create contact

`operation_foundation_core_record_definitions_user_business_behavior_create_contact`

**Inputs** user, ignore\_links = false, ignore\_mandatory = false.

**Record and data access** resolve a document from mapping(“doctype” → “Contact”, “first\_name” → user.first\_name, “last\_name” → user.last\_name, “user” → user.name, …) via get\_doc · resolve a document from “Contact” via get\_doc.

**State and service calls** call insert on contact · call save on contact.

**Explicit results** no value.

**Explicit failure paths** Platform.RetryBackgroundJobError.

**Local steps**

- Bind dependencies get\_contact\_name.
- If user.name belongs to list(“Administrator”, “Guest”).
  - Return no value.
- Set contact\_name from get\_contact\_name(user.email).
- If not contact\_name.
  - Attempt the following.
    - Set contact from Platform.get\_doc(mapping(“doctype” → “Contact”, “first\_name” → user.first\_name, “last\_name” → user.last\_name, “user” → user.name, …)).
    - If user.email.
      - Evaluate contact.add\_email(user.email, is\_primary = true).
    - If user.phone.
      - Evaluate contact.add\_phone(user.phone, is\_primary\_phone = true).
    - If user.mobile\_no.
      - Evaluate contact.add\_phone(user.mobile\_no, is\_primary\_mobile\_no = true).
    - Evaluate contact.insert(ignore\_permissions = true, ignore\_links = ignore\_links, ignore\_mandatory = ignore\_mandatory).
  - On failure (Platform.DuplicateEntryError).
    - Take no action here.
- Otherwise.
  - Attempt the following.
    - Set contact from Platform.get\_doc(“Contact”, contact\_name).
    - Set contact.first\_name from user.first\_name.
    - Set contact.last\_name from user.last\_name.
    - Set contact.gender from user.gender.
    - If (user.phone and not any(generator of new\_contact.phone equals user.phone for new\_contact drawn from contact.phone\_nos)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in user.phone → not any(generator of new\_contact.phone equals user.phone for new\_contact drawn from contact.phone\_nos).
      - Draw new\_contact from contact.phone\_nos.
      - Evaluate contact.add\_phone(user.phone, is\_primary\_phone = not any(generator of new\_contact.is\_primary\_phone equals 1 for new\_contact drawn from contact.phone\_nos)).
        - Draw new\_contact from contact.phone\_nos.
    - If (user.mobile\_no and not any(generator of new\_contact.phone equals user.mobile\_no for new\_contact drawn from contact.phone\_nos)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in user.mobile\_no → not any(generator of new\_contact.phone equals user.mobile\_no for new\_contact drawn from contact.phone\_nos).
      - Draw new\_contact from contact.phone\_nos.
      - Evaluate contact.add\_phone(user.mobile\_no, is\_primary\_mobile\_no = not any(generator of new\_contact.is\_primary\_mobile\_no equals 1 for new\_contact drawn from contact.phone\_nos)).
        - Draw new\_contact from contact.phone\_nos.
    - Evaluate contact.save(ignore\_permissions = true).
  - On failure (Platform.TimestampMismatchError).
    - Raise Platform.RetryBackgroundJobError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L2992) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L647)

<a id="op-0b0206d40aefb7"></a>
### Get restricted ip list

`operation_foundation_core_record_definitions_user_business_behavior_get_restricted_internet_protocol_list`

**Inputs** user.

**Explicit results** no value · list of i.strip() for i drawn from user.restrict\_ip.strip().split(“,”).

**Local steps**

- If not user.restrict\_ip.
  - Return no value.
- Return list of i.strip() for i drawn from user.restrict\_ip.strip().split(“,”).
  - Draw i from user.restrict\_ip.strip().split(“,”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L4009) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L659)

<a id="op-34c2a580af0b09"></a>
### Generate keys

`operation_foundation_core_record_definitions_user_business_behavior_generate_keys`

**Inputs** user.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user\_details.

**Explicit results** mapping(“api\_key” → user\_details.api\_key, “api\_secret” → api\_secret).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set user\_details from Platform.get\_doc(“User”, user).
- Set api\_secret from Platform.generate\_hash(length = 15).
- If not user\_details.api\_key.
  - Set api\_key from Platform.generate\_hash(length = 15).
  - Set user\_details.api\_key from api\_key.
- Set user\_details.api\_secret from api\_secret.
- Evaluate user\_details.save().
- Return mapping(“api\_key” → user\_details.api\_key, “api\_secret” → api\_secret).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · clock or generated value from Platform.generate\_hash(length = 15).

**Boundaries to resolve** stored data, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L4131) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L648)

<a id="op-e7899590dd3938"></a>
### Switch theme

`operation_foundation_core_record_definitions_user_business_behavior_switch_theme`

**Inputs** theme.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “User”.

**Local steps**

- If theme belongs to list(“Dark”, “Light”, “Automatic”).
  - Evaluate Platform.db.set\_value(“User”, Platform.session.user, “desk\_theme”, theme).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L4448) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L674)

<a id="op-7f06cff76ce8c4"></a>
### Get enabled users

`operation_foundation_core_record_definitions_user_business_behavior_get_enabled_users`

**Inputs** no declared parameters.

**Explicit results** Platform.cache.get\_value(“enabled\_users”, \_get\_enabled\_users).

**Local steps**

- Bind local operation \_get\_enabled\_users for subsequent calls.
- Return Platform.cache.get\_value(“enabled\_users”, \_get\_enabled\_users).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L4592) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L654)

<a id="op-c402e88d60a07a"></a>
### Get enabled users.get enabled users

`operation_foundation_core_record_definitions_user_business_behavior_get_enabled_users_get_enabled_users`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_all.

**Explicit results** enabled\_users.

**Local steps**

- Set enabled\_users from Platform.get\_all(“User”, filters = mapping(“enabled” → “1”), pluck = “name”).
- Return enabled\_users.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0113.json#L4737) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L655)

<a id="op-6b8647868fc249"></a>
### Impersonate

`operation_foundation_core_record_definitions_user_business_behavior_impersonate`

**Inputs** user, reason.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “Activity Log”, “user” → user, “status” → “Success”, “subject” → translated “User {0} impersonated as {1}”.format(impersonator, user), …) via get\_doc · read “Email Account” via exists · read “User” via get\_value.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Activity Log”, “user” → user, “status” → “Success”, “subject” → translated “User {0} impersonated as {1}”.format(impersonator, user), …)) · request new\_doc for “Notification Log” · call insert on notification · sendmail.

**Local steps**

- Evaluate Platform.has\_permission(“User”, “impersonate”, doc = user, throw = true).
- Set impersonator from Platform.session.user.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Activity Log”, “user” → user, “status” → “Success”, “subject” → nested operand in the contract(nested operand in the contract).format(impersonator, user), …)).insert(i ….
- Set notification from Platform.new\_doc(“Notification Log”, for\_user = user, from\_user = Platform.session.user, subject = translated “{0} just impersonated as you. They gave this reason: {1}”.format(impersonator, reason)).
- Evaluate notification.set(“type”, “Alert”).
- Evaluate notification.insert(ignore\_permissions = true).
- Set outgoing\_email\_exists from Platform.db.exists(“Email Account”, mapping(“default\_outgoing” → 1, “awaiting\_password” → 0)).
- If outgoing\_email\_exists.
  - Set user\_email from Platform.db.get\_value(“User”, user, “email”).
  - Set email\_message from translated “User {0} has started an impersonation session as you. &lt;br&gt;&lt;br&gt;&lt;b&gt;Reason provided:&lt;/b&gt; {1}”.format(escape\_html(impersonator), escape\_html(reason)).
  - Evaluate Platform.sendmail(recipients = list(user\_email), subject = translated “Security Alert: Your account is being impersonated”, content = email\_message).
- Evaluate Platform.local.login\_manager.impersonate(user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“User”, “impersonate”, doc = user, throw = true) · service or queued work from Platform.sendmail(recipients = list(user\_email), subject = translated “Security Alert: Your account is being impersonated”, content = email\_message).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L46) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L669)

<a id="op-195251f3bd5b61"></a>
### Clear session

`operation_foundation_core_record_definitions_user_business_behavior_clear_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** sid\_hash.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L44) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L646)
