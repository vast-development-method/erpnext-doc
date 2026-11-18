# Identity and access · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Share

<a id="op-ce370e23eb7786"></a>
### Add docshare

`operation_foundation_share_business_behavior_add_docshare`

**Inputs** doctype, name, user = no value, read = 1, write = 0, submit = 0, share = 0, everyone = 0, flags = no value, notify = 0, remaining named values kwargs.

**Record and data access** resolve a document from “DocShare” via get\_doc · read “User” via get\_cached\_value.

**State and service calls** request new\_doc for “DocShare” · call save on doc.

**Explicit results** doc.

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Set share\_perms from mapping(“read” → 1, “write” → cint(write), “submit” → cint(submit), “share” → cint(share)).
- Set custom\_perms from get\_doctype\_ptype\_map().get(doctype, list()).
- If (kwargs and custom\_perms).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs → custom\_perms.
  - For each ptype in custom\_perms.
    - If ptype belongs to kwargs.
      - Set share\_perms at ptype from cint(kwargs.get(ptype)).
- If not (flags or mapping()).get(“ignore\_share\_permission”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flags → mapping().
  - Evaluate check\_share\_permission(doctype, name, share\_perms, custom\_perms).
- If share\_name bound to get\_share\_name(doctype, name, user, everyone).
  - Set doc from Platform.get\_doc(“DocShare”, share\_name).
- Otherwise.
  - Set doc from Platform.new\_doc(“DocShare”).
  - Evaluate doc.update(mapping(“user” → user, “share\_doctype” → doctype, “share\_name” → name, “everyone” → cint(everyone))).
- If flags.
  - Evaluate doc.flags.update(flags).
- Evaluate doc.update(share\_perms).
- Evaluate doc.save(ignore\_permissions = true).
- Evaluate notify\_assignment(user, doctype, name, everyone, notify = notify).
- If ((user differs from name or doctype differs from “User”) and Platform.get\_cached\_value(“User”, user, “follow\_shared\_documents”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (user differs from name or doctype differs from “User”) → Platform.get\_cached\_value(“User”, user, “follow\_shared\_documents”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user differs from name → doctype differs from “User”.
  - Evaluate \_follow\_document(doctype, name, user).
- Return doc.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, user, “follow\_shared\_documents”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L3441) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1910) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L584)

<a id="op-7edcc89a189a12"></a>
### Remove

`operation_foundation_share_business_behavior_remove`

**Inputs** doctype, name, user, flags = no value.

**Record and data access** read “DocShare” via get\_value.

**State and service calls** request delete\_doc for “DocShare”.

**Local steps**

- Set share\_name from Platform.db.get\_value(“DocShare”, mapping(“user” → user, “share\_name” → name, “share\_doctype” → doctype)).
- If share\_name.
  - Evaluate Platform.delete\_doc(“DocShare”, share\_name, flags = flags).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L4421) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L592)

<a id="op-e1c693e6d8b3c0"></a>
### Set permission

`operation_foundation_share_business_behavior_set_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name, user, permission\_to, value, everyone.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L43) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L594)

<a id="op-91bacbb64313f2"></a>
### Set docshare permission

`operation_foundation_share_business_behavior_set_docshare_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name, user, permission\_to, value, everyone, flags.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 8 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L4857) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L593)

<a id="op-293fadbe51c2e8"></a>
### Get users

`operation_foundation_share_business_behavior_get_users`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Explicit results** \_get\_users(doc).

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name).
- Return \_get\_users(doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L5546) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L589)

<a id="op-c0fa5741b145e6"></a>
### Get users

`operation_foundation_share_business_behavior_get_users_2`

**Inputs** doc.

**Declared result** list.

**Record and data access** read “DocShare” via get\_all.

**Explicit results** list() · Platform.get\_all(“DocShare”, fields = list(“\*”), filters = dict(share\_doctype = doc.doctype, share\_name = str(doc.name))).

**Local steps**

- Bind dependencies has\_permission.
- If not has\_permission(doc.doctype, “read”, doc, print\_logs = false).
  - Return list().
- Return Platform.get\_all(“DocShare”, fields = list(“\*”), filters = dict(share\_doctype = doc.doctype, share\_name = str(doc.name))).

**Values supplied outside this operation** effective access from has\_permission(doc.doctype, “read”, doc, print\_logs = false).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L5669) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1916) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L590)

<a id="op-fd1deab791c85b"></a>
### Get shared

`operation_foundation_share_business_behavior_get_shared`

**Inputs** doctype, user = no value, rights = no value, filters (named only, default no value), limit (named only, default no value).

**Record and data access** read “DocShare” via get\_all.

**Explicit results** list of doc.share\_name for doc drawn from shared\_docs.

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- If not rights.
  - Set rights from list(“read”).
- Set share\_filters from list of list(right, “=”, 1) for right drawn from rights.
  - Draw right from rights.
- Update share\_filters using + list(list(“share\_doctype”, “=”, doctype)).
- If filters.
  - Update share\_filters using + filters.
- Set or\_filters from list(list(“user”, “=”, user)).
- If user differs from “Guest”.
  - Update or\_filters using + list(list(“everyone”, “=”, 1)).
- Set shared\_docs from Platform.get\_all(“DocShare”, fields = list(“share\_name”), filters = share\_filters, or\_filters = or\_filters, order\_by = no value, …).
- Return list of doc.share\_name for doc drawn from shared\_docs.
  - Draw doc from shared\_docs.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L5883) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1913) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L587)

<a id="op-1e768b83d37d62"></a>
### Get shared doctypes

`operation_foundation_share_business_behavior_get_shared_record_types`

**Inputs** user = no value.

**Explicit results** query.run(pluck = true).

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Set table from Platform.qb.DocType(“DocShare”).
- Set query from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise or nested operand in the contract equals nested operand in …().
- Return query.run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L6340) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1914) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L588)

<a id="op-69af96fb98b4b7"></a>
### Get share name

`operation_foundation_share_business_behavior_get_share_name`

**Inputs** doctype, name, user, everyone.

**Record and data access** read “DocShare” via get\_value.

**Explicit results** share\_name.

**Local steps**

- If cint(everyone).
  - Set share\_name from Platform.db.get\_value(“DocShare”, mapping(“everyone” → 1, “share\_name” → name, “share\_doctype” → doctype)).
- Otherwise.
  - Set share\_name from Platform.db.get\_value(“DocShare”, mapping(“user” → user, “share\_name” → name, “share\_doctype” → doctype)).
- Return share\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L6595) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1912) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L586)

<a id="op-6edf627321d60a"></a>
### Check share permission

`operation_foundation_share_business_behavior_check_share_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name, permissions, custom\_perms.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L6861) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1911) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L585)

<a id="op-ea6a81e378e28e"></a>
### Notify assignment

`operation_foundation_share_business_behavior_notify_assignment`

**Inputs** shared\_by, doctype, doc\_name, everyone, notify = 0.

**Explicit results** no value.

**Local steps**

- If (not (shared\_by and doctype and doc\_name) or cint(everyone) or not cint(notify)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (shared\_by and doctype and doc\_name) → cint(everyone) → not cint(notify).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in shared\_by → doctype → doc\_name.
  - Return no value.
- Bind dependencies get\_fullname.
- Set title from get\_title(doctype, doc\_name).
- Set reference\_user from get\_fullname(Platform.session.user).
- Set notification\_message from translated “{0} shared a document {1} {2} with you”.format(Platform.bold(reference\_user), Platform.bold(translated doctype), get\_title\_html(title)).
- Set notification\_doc from mapping(“type” → “Share”, “document\_type” → doctype, “subject” → notification\_message, “document\_name” → doc\_name, …).
- Evaluate enqueue\_create\_notification(shared\_by, notification\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0333.json#L7442) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1917) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L591)

## Service · Twofactor

<a id="op-f35c146637615e"></a>
### Get default

`operation_foundation_twofactor_business_behavior_get_default`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** key.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L3300) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1395)

<a id="op-9790c984c2efd6"></a>
### Set default

`operation_foundation_twofactor_business_behavior_set_default`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** key, value.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L3368) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1412)

<a id="op-8242765441b37e"></a>
### Clear default

`operation_foundation_twofactor_business_behavior_clear_default`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** key.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L3447) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1388)

<a id="op-b8eaf5ceaecda3"></a>
### Toggle two factor auth

`operation_foundation_twofactor_business_behavior_toggle_two_factor_authentication`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** state, roles.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L3515) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1415)

<a id="op-0ab1c7cdf4384a"></a>
### Two factor is enabled

`operation_foundation_twofactor_business_behavior_two_factor_is_enabled`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 5 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L3698) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1416)

<a id="op-e9abf1f1b66bb6"></a>
### Should run 2fa

`operation_foundation_twofactor_business_behavior_should_run_2_fa`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L4068) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1414)

<a id="op-f5e35addd34eb0"></a>
### Get cached user pass

`operation_foundation_twofactor_business_behavior_get_cached_user_pass`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L57) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1394)

<a id="op-6686f0fa38c0fd"></a>
### Authenticate for 2factor

`operation_foundation_twofactor_business_behavior_authenticate_for_2_factor`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L4336) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1386)

<a id="op-9511a60b950cf8"></a>
### Cache 2fa data

`operation_foundation_twofactor_business_behavior_cache_2_fa_data`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, token, otp\_secret, tmp\_id.

**Observed service boundaries** record mutation request.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L55) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1387)

<a id="op-281a66b6072b16"></a>
### Two factor is enabled for

`operation_foundation_twofactor_business_behavior_two_factor_is_enabled_for`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L5050) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1417)

<a id="op-6a72e7fb9ebe30"></a>
### Get otpsecret for

`operation_foundation_twofactor_business_behavior_get_otpsecret_for`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Observed service boundaries** transaction control.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L5384) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1401)

<a id="op-9262c57fd1bbc3"></a>
### Get verification method

`operation_foundation_twofactor_business_behavior_get_verification_method`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0456.json#L5636) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1404)

<a id="op-d1e3215776930e"></a>
### Confirm otp token

`operation_foundation_twofactor_business_behavior_confirm_one_time_password_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** login\_manager, otp, tmp\_id.

**Explicit result forms** Boolean false, Boolean true.

**Locally raised failures** ExpiredLoginException.

**Observed service boundaries** record lookup.

**Local structure** 9 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L56) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1389)
