# Shared value and file services · operations 54

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · User

<a id="op-36e5d194835381"></a>
### User Permissions.get can read

`operation_foundation_utils_user_business_behavior_user_permissions_get_can_read`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L5127) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L99) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1048)

<a id="op-562496c3faada6"></a>
### User Permissions.load user

`operation_foundation_utils_user_business_behavior_user_permissions_load_user`

**Inputs** self.

**Record and data access** read “User” via get\_value · resolve a document from “Workspace” via get\_cached\_doc.

**Explicit results** d.

**Local steps**

- Set d from Platform.db.get\_value(“User”, self.name, list(“creation”, “desk\_theme”, “code\_editor\_type”, “document\_follow\_notify”, …), as\_dict = true).
- If not self.can\_read.
  - Evaluate self.build\_permissions().
- If d.get(“default\_workspace”).
  - Attempt the following.
    - Set workspace from Platform.get\_cached\_doc(“Workspace”, d.default\_workspace).
    - Set d.default\_workspace from mapping(“name” → workspace.name, “public” → workspace.public, “title” → workspace.title).
  - On failure (Platform.DoesNotExistError).
    - Set d.default\_workspace from no value.
- Set d.name from self.name.
- Set d.onboarding\_status from Platform.parse\_json(d.onboarding\_status).
- Set d.roles from self.get\_roles().
- Set d.defaults from self.get\_defaults().
- For each key in tuple(“can\_select”, “can\_create”, “can\_write”, “can\_read”, …).
  - Set d at key from list(set(getattr(self, key))).
- Return d.

**Methods declared on this owner** [build permissions](operations-053.md#op-82efdc63b420cf), [get roles](operations-053.md#op-2f243219c66d92), [get defaults](operations-053.md#op-4f77aea73a455b).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Workspace”, d.default\_workspace) · effective access from self.get\_roles() · selected callable from getattr(self, key).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L14) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1052)

<a id="op-b92978bcfbe969"></a>
### User Permissions.get all reports

`operation_foundation_utils_user_business_behavior_user_permissions_get_all_reports`

**Inputs** self.

**Explicit results** DeskViews.get\_allowed\_reports().

**Local steps**

- Return DeskViews.get\_allowed\_reports().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L6284) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L98) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1047)

<a id="op-8e97c2ed84ffa7"></a>
### Get user fullname

`operation_foundation_utils_user_business_behavior_get_user_fullname`

**Inputs** user.

**Declared result** str.

**Record and data access** read user\_doctype via get\_value.

**Explicit results** (Platform.get\_value(user\_doctype, filters = mapping(“name” → user), fieldname = Concat\_ws(one space, user\_doctype.first\_name, user\_doctype.last\_name)) or empty text).

**Local steps**

- Set user\_doctype from DocType(“User”).
- Return (Platform.get\_value(user\_doctype, filters = mapping(“name” → user), fieldname = Concat\_ws(one space, user\_doctype.first\_name, user\_doctype.last\_name)) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_value(user\_doctype, filters = mapping(“name” → user), fieldname = Concat\_ws(one space, user\_doctype.first\_name, user\_doctype.last\_name)) → empty text.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L6333) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L88) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1037)

<a id="op-3139e184087dd5"></a>
### Get fullname and avatar

`operation_foundation_utils_user_business_behavior_get_fullname_and_avatar`

**Inputs** user.

**Declared result** \_dict.

**Record and data access** read “User” via get\_cached\_value.

**Explicit results** \_dict(mapping(“fullname” → one space.join(list(filter(no value, list(first\_name, last\_name)))), “avatar” → avatar, “name” → name)).

**Local steps**

- Set tuple(first\_name, last\_name, avatar, name) from Platform.get\_cached\_value(“User”, user, list(“first\_name”, “last\_name”, “user\_image”, “name”)).
- Return \_dict(mapping(“fullname” → one space.join(list(filter(no value, list(first\_name, last\_name)))), “avatar” → avatar, “name” → name)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, user, list(“first\_name”, “last\_name”, “user\_image”, “name”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L9) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L85) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1034)

<a id="op-4563d01c4f82fe"></a>
### Get system managers

`operation_foundation_utils_user_business_behavior_get_system_managers`

**Inputs** only\_name = false.

**Declared result** list at str.

**Explicit results** list of p.name for p drawn from system\_managers · list of formataddr(tuple(p.full\_name, p.name)) for p drawn from system\_managers.

**Local steps**

- Set HasRole from DocType(“Has Role”).
- Set User from DocType(“User”).
- If only\_name.
  - Set fields from list(User.name).
- Otherwise.
  - Set fields from list(User.full\_name, User.name).
- Set system\_managers from nested operand in the contract(nested operand in the contract).select(expanded fields).orderby(User.creation, order = Order.desc).run(as\_dict = true).
- If only\_name.
  - Return list of p.name for p drawn from system\_managers.
    - Draw p from system\_managers.
- Otherwise.
  - Return list of formataddr(tuple(p.full\_name, p.name)) for p drawn from system\_managers.
    - Draw p from system\_managers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L6825) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L87) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1036)

<a id="op-50dac3a0868f58"></a>
### Add role

`operation_foundation_utils_user_business_behavior_add_role`

**Inputs** user, role.

**Declared result** no value.

**Record and data access** resolve a document from “User” via get\_doc.

**Local steps**

- Evaluate Platform.get\_doc(“User”, user).add\_roles(role).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0519.json#L7416) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L82) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1031)

<a id="op-5c0acb70a3d1b6"></a>
### Add system manager

`operation_foundation_utils_user_business_behavior_add_system_manager`

**Inputs** email, first\_name = no value, last\_name = no value, send\_welcome\_email = false, password = no value.

**Declared result** “User”.

**Record and data access** read “Role” via get\_all.

**State and service calls** request new\_doc for “User” · call insert on user.

**Explicit results** user.

**Local steps**

- Set user from Platform.new\_doc(“User”).
- Evaluate user.update(mapping(“name” → email, “email” → email, “enabled” → 1, “first\_name” → (first\_name or email), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in first\_name → email.
  - Value choice on send\_welcome\_email — true gives 1, false gives 0.
- Evaluate user.insert().
- Set roles from Platform.get\_all(“Role”, fields = list(“name”), filters = mapping(“name” → list(“not in”, AUTOMATIC\_ROLES))).
- Set roles from list of role.name for role drawn from roles.
  - Draw role from roles.
- Evaluate user.add\_roles(expanded roles).
- If password.
  - Bind dependencies update\_password.
  - Evaluate update\_password(user = user.name, pwd = password).
- Return user.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L83) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1032)

<a id="op-3b6d62d7ee6b94"></a>
### Get enabled system users

`operation_foundation_utils_user_business_behavior_get_enabled_system_users`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Record and data access** read “User” via get\_all.

**Explicit results** Platform.get\_all(“User”, fields = list(“email”, “language”, “name”), filters = mapping(“user\_type” → “System User”, “enabled” → 1, “name” → list(“not in”, tuple(“Administrator”, “Guest”)))).

**Local steps**

- Return Platform.get\_all(“User”, fields = list(“email”, “language”, “name”), filters = mapping(“user\_type” → “System User”, “enabled” → 1, “name” → list(“not in”, tuple(“Administrator”, “Guest”)))).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L559) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L84) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1033)

<a id="op-7c794e13b880f7"></a>
### Is website user

`operation_foundation_utils_user_business_behavior_is_website_user`

**Inputs** username = no value.

**Declared result** (str bitwise or no value).

**Record and data access** read “User” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“User”, (username or Platform.session.user), “user\_type”) equals “Website User”.

**Local steps**

- Return Platform.get\_cached\_value(“User”, (username or Platform.session.user), “user\_type”) equals “Website User”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in username → Platform.session.user.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, (username or Platform.session.user), “user\_type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L736) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L93) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1042)

<a id="op-a3bd49c1a7aef9"></a>
### Is system user

`operation_foundation_utils_user_business_behavior_is_system_user`

**Inputs** username = no value.

**Declared result** (str bitwise or no value).

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.db.get\_value(“User”, mapping(“email” → (username or Platform.session.user), “enabled” → 1, “user\_type” → “System User”), cache = true).

**Local steps**

- Return Platform.db.get\_value(“User”, mapping(“email” → (username or Platform.session.user), “enabled” → 1, “user\_type” → “System User”), cache = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in username → Platform.session.user.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L864) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L92) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1041)

<a id="op-0107f3f2b0d82b"></a>
### Get users

`operation_foundation_utils_user_business_behavior_get_users`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list of mapping(“full\_name” → get\_user\_fullname(user), “email” → user, “is\_system\_manager” → user belongs to system\_managers) for user drawn from get\_system\_users().

**Local steps**

- Bind dependencies get\_system\_users.
- Set system\_managers from get\_system\_managers(only\_name = true).
- Return list of mapping(“full\_name” → get\_user\_fullname(user), “email” → user, “is\_system\_manager” → user belongs to system\_managers) for user drawn from get\_system\_users().
  - Draw user from get\_system\_users().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L1034) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L89) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1038)

<a id="op-d893b5f21db27a"></a>
### Get users with role

`operation_foundation_utils_user_business_behavior_get_users_with_role`

**Inputs** role.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).select(User.name).distinct().run(pluck = true).

**Local steps**

- Set User from DocType(“User”).
- Set HasRole from DocType(“Has Role”).
- Return nested operand in the contract(nested operand in the contract).select(User.name).distinct().run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L1215) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L90) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1039)

<a id="op-d8d47d3c8114cd"></a>
### Is portal user

`operation_foundation_utils_user_business_behavior_is_portal_user`

**Inputs** no declared parameters.

**Explicit results** true.

**Local steps**

- Bind dependencies has\_common.
- Set roles from get\_portal\_roles().
- Set user\_type from Platform.session.data.user\_type.
- If (user\_type equals “Website User” and has\_common(Platform.get\_roles(), roles)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in user\_type equals “Website User” → has\_common(Platform.get\_roles(), roles).
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L1538) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L91) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1040)

<a id="op-3dc43359fdd8aa"></a>
### Get portal roles

`operation_foundation_utils_user_business_behavior_get_portal_roles`

**Inputs** no declared parameters.

**Record and data access** read “Portal Settings” via get\_single.

**Explicit results** roles.

**Local steps**

- Set roles from list().
- For each menu\_item in Platform.get\_single(“Portal Settings”).menu.
  - If (menu\_item.role and menu\_item.role does not belong to roles).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in menu\_item.role → menu\_item.role does not belong to roles.
    - Evaluate roles.append(menu\_item.role).
- Return roles.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0520.json#L1685) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L86) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1035)

## Service · Utils

<a id="op-eb36b43e4db03d"></a>
### Get fullname

`operation_foundation_utils_initialize_business_behavior_get_fullname`

**Inputs** user = no value.

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.local.fullnames.get(user).

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- If not hasattr(Platform.local, “fullnames”).
  - Set Platform.local.fullnames from mapping().
- If not Platform.local.fullnames.get(user).
  - Set p from Platform.db.get\_value(“User”, user, list(“first\_name”, “last\_name”), as\_dict = true).
  - If p.
    - Set Platform.local.fullnames at user from (one space.join(filter(no value, list(p.get(“first\_name”), p.get(“last\_name”)))) or user).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in one space.join(filter(no value, list(p.get(“first\_name”), p.get(“last\_name”)))) → user.
  - Otherwise.
    - Set Platform.local.fullnames at user from user.
- Return Platform.local.fullnames.get(user).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L5001) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L230)

<a id="op-e6076331d145f5"></a>
### Get email address

`operation_foundation_utils_initialize_business_behavior_get_email_address`

**Inputs** user = no value.

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.db.get\_value(“User”, user, “email”).

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Return Platform.db.get\_value(“User”, user, “email”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L5426) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L224)

<a id="op-8a33b5b85a8177"></a>
### Get formatted email

`operation_foundation_utils_initialize_business_behavior_get_formatted_email`

**Inputs** user, mail = no value.

**Explicit results** empty text · cstr(make\_header(decode\_header(formataddr(tuple(fullname, mail))))).

**Local steps**

- Set fullname from get\_fullname(user).
- Set method from get\_hook\_method(“get\_sender\_details”).
- If method.
  - Set tuple(sender\_name, mail) from method().
  - Set fullname from (sender\_name or fullname).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in sender\_name → fullname.
- If not mail.
  - Set mail from (get\_email\_address(user) or validate\_email\_address(user)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_email\_address(user) → validate\_email\_address(user).
- If not mail.
  - Return empty text.
- Otherwise.
  - Return cstr(make\_header(decode\_header(formataddr(tuple(fullname, mail))))).

**Values supplied outside this operation** selected callable from get\_hook\_method(“get\_sender\_details”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L5540) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L228)

<a id="op-f3616cd7aa886e"></a>
### Extract email id

`operation_foundation_utils_initialize_business_behavior_extract_email_identifier`

**Inputs** email.

**Declared result** str.

**Explicit results** empty text · cstr(parse\_addr(email) at 1).

**Local steps**

- If not email.
  - Return empty text.
- Return cstr(parse\_addr(email) at 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L5851) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L213)

<a id="op-0ad6c6ea3aa13b"></a>
### Validate phone number with country code

`operation_foundation_utils_initialize_business_behavior_validate_phone_number_with_country_code`

**Inputs** phone\_number, fieldname = no value, label = no value.

**Declared result** no value.

**Explicit results** no value · true.

**Explicit failure paths** TypeError(“validate\_phone\_number\_with\_country\_code() requires a fieldname or label”) · validation helper with Platform.InvalidPhoneNumberError — error\_message.format(Platform.bold(phone\_number), Platform.bold((label or fieldname))).

**Local steps**

- Bind dependencies NumberParseException, is\_valid\_number, parse.
- Bind dependencies \_.
- If not (fieldname or label).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname → label.
  - Raise TypeError(“validate\_phone\_number\_with\_country\_code() requires a fieldname or label”).
- If not phone\_number.
  - Return no value.
- Set valid\_number from false.
- Set error\_message from translated “Phone Number {0} set in field {1} is not valid.”.
- Set error\_title from translated “Invalid Phone Number”.
- Attempt the following.
  - If valid\_number bound to is\_valid\_number(parse(phone\_number)).
    - Return true.
- On failure (NumberParseException) bound to e.
  - If e.error\_type equals NumberParseException.INVALID\_COUNTRY\_CODE.
    - Set error\_message from translated “Please select a country code for field {1}.”.
    - Set error\_title from translated “Country Code Required”.
- On exit, including pending return or failure.
  - If not valid\_number.
    - Call the validation error handler Platform.throw(error\_message.format(Platform.bold(phone\_number), Platform.bold((label or fieldname))), title = error\_title, exc = Platform.InvalidPhoneNumberError).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in label → fieldname.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L134) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L283)

<a id="op-e8ed9d7fb86f7e"></a>
### Validate phone number

`operation_foundation_utils_initialize_business_behavior_validate_phone_number`

**Inputs** phone\_number, throw = false.

**Explicit results** false · bool(match).

**Explicit failure paths** validation helper with Platform.InvalidPhoneNumberError — Platform.\_(“{0} is not a valid Phone Number”).format(phone\_number).

**Local steps**

- If not phone\_number.
  - Return false.
- If not isinstance(phone\_number, str).
  - Set phone\_number from str(phone\_number).
- Set phone\_number from phone\_number.strip().
- Set match from PHONE\_NUMBER\_PATTERN.match(phone\_number).
- If (not match and throw).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not match → throw.
  - Call the validation error handler Platform.throw(Platform.\_(“{0} is not a valid Phone Number”).format(phone\_number), Platform.InvalidPhoneNumberError).
- Return bool(match).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L6368) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L282)

<a id="op-babb781d16f491"></a>
### Validate name

`operation_foundation_utils_initialize_business_behavior_validate_name`

**Inputs** name, throw = false.

**Explicit results** false · bool(match).

**Explicit failure paths** validation helper with Platform.InvalidNameError — Platform.\_(“{0} is not a valid Name”).format(name).

**Local steps**

- If not name.
  - Return false.
- Set name from name.strip().
- Set match from PERSON\_NAME\_PATTERN.match(name).
- If (not match and throw).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not match → throw.
  - Call the validation error handler Platform.throw(Platform.\_(“{0} is not a valid Name”).format(name), Platform.InvalidNameError).
- Return bool(match).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L6645) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L281)

<a id="op-3141fb967e2af9"></a>
### Validate email address

`operation_foundation_utils_initialize_business_behavior_validate_email_address`

**Inputs** email\_str, throw = false.

**Explicit results** “, ”.join(out).

**Explicit failure paths** validation helper with Platform.InvalidEmailAddressError — Platform.\_(“{0} is not a valid Email Address”).format(Platform.utils.escape\_html((name or email\_str))) · validation helper with Platform.InvalidEmailAddressError — Platform.\_(“{0} is not a valid Email Address”).format(Platform.utils.escape\_html(addr)).

**Local steps**

- Set email\_str from (email\_str or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email\_str → empty text.
- Set out from list().
- Set email\_str from email\_str.replace(whitespace '\\n', “,”).replace(whitespace '\\r', “,”).
- Set addresses from getaddresses(list(email\_str)).
- For each tuple(name, addr) in addresses.
  - If not addr.
    - If throw.
      - Call the validation error handler Platform.throw(Platform.\_(“{0} is not a valid Email Address”).format(Platform.utils.escape\_html((name or email\_str))), Platform.InvalidEmailAddressError).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → email\_str.
    - Continue with the next iteration or loop test.
  - If “undisclosed-recipient” belongs to addr.
    - Continue with the next iteration or loop test.
  - Set match from EMAIL\_MATCH\_PATTERN.match(addr).
  - If not match.
    - If throw.
      - Call the validation error handler Platform.throw(Platform.\_(“{0} is not a valid Email Address”).format(Platform.utils.escape\_html(addr)), Platform.InvalidEmailAddressError).
    - Continue with the next iteration or loop test.
  - Evaluate out.append(addr).
- Return “, ”.join(out).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L133) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L279)

<a id="op-fffd8f1a4e59c0"></a>
### Split emails

`operation_foundation_utils_initialize_business_behavior_split_emails`

**Inputs** txt.

**Explicit results** email\_list.

**Local steps**

- Set email\_list from list().
- Set s from WHITESPACE\_PATTERN.sub(one space, cstr(txt)).
- For each email in MULTI\_EMAIL\_STRING\_PATTERN.split(s).
  - Set email from strip(cstr(email)).
  - If email.
    - Evaluate email\_list.append(email).
- Return email\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L273)
