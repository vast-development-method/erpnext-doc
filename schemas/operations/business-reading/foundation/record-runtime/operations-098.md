# Record lifecycle and persistence · operations 98

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · User

[Record definition](../../../../data/record-types/user.json)

<a id="op-c245b44bc955a7"></a>
### User.get fullname

`operation_foundation_core_record_definitions_user_business_behavior_user_get_fullname`

**Inputs** self.

**Explicit results** (((self.first\_name or empty text) + ((self.first\_name and one space) or empty text)) + (self.last\_name or empty text)).

**Local steps**

- Return (((self.first\_name or empty text) + ((self.first\_name and one space) or empty text)) + (self.last\_name or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.first\_name → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.first\_name and one space) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.first\_name → one space.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.last\_name → empty text.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L845) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L695)

<a id="op-ccb0350c23328d"></a>
### User.password reset mail

`operation_foundation_core_record_definitions_user_business_behavior_user_password_reset_mail`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, link.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L950) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L705)

<a id="op-0604737191e2c8"></a>
### User.send welcome mail to user

`operation_foundation_core_record_definitions_user_business_behavior_user_send_welcome_mail_to_user`

**Inputs** self.

**Local steps**

- Bind dependencies get\_brand\_name.
- Bind dependencies get\_url.
- Set link from self.\_reset\_password().
- Set subject from no value.
- Set method from Platform.get\_hooks(“welcome\_email”).
- If method.
  - Set subject from Platform.get\_attr(method at negative 1)().
- If not subject.
  - Set site\_name from (Platform.db.get\_default(“site\_name”) or Platform.get\_conf().get(“site\_name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(“site\_name”) → Platform.get\_conf().get(“site\_name”).
  - If site\_name.
    - Set subject from translated “Welcome to {0}”.format(site\_name).
  - Otherwise.
    - Set subject from translated “Complete Registration”.
- Set welcome\_email\_template from Platform.db.get\_system\_setting(“welcome\_email\_template”).
- Evaluate self.send\_login\_mail(subject, “new\_user”, dict(link = link, site\_url = get\_url(), app\_name = (get\_brand\_name() or “Platform”)), custom\_template = welcome\_email\_template, wrapper = no value when welcome\_ema ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_brand\_name() → “Platform”.
  - Value choice on welcome\_email\_template — true gives no value, false gives “templates/emails/auth\_email.html”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset password](operations-097.md#op-39222774e66e2e), [send login mail](operations-098.md#op-7fa338b9e511dc).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“welcome\_email”), Platform.get\_attr(method at negative 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L1221) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L715)

<a id="op-7fa338b9e511dc"></a>
### User.send login mail

`operation_foundation_core_record_definitions_user_business_behavior_user_send_login_mail`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, subject, template, add\_args, now, custom\_template, wrapper.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** notification or queued-work request, record lookup.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L1722) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L713)

<a id="op-8278e019bccb32"></a>
### User.on trash

`operation_foundation_core_record_definitions_user_business_behavior_user_on_trash`

**Inputs** self.

**Record and data access** read doctype via get\_all · read “Note” via get\_all · resolve a document from “Note” via get\_doc · read “User Invitation” via get\_all · resolve a document from “User Invitation” via get\_doc.

**State and service calls** request delete on “ToDo” · request delete on “Event” · request delete on “DocShare” · request delete\_doc for “Notification Settings” · request delete on “User Permission” · 7 additional forms in the steps below.

**Local steps**

- Evaluate Platform.clear\_cache(user = self.name).
- If self.name belongs to STANDARD\_USERS.
  - Evaluate throw(translated “User {0} cannot be deleted”.format(self.name)).
- Set self.enabled from 0.
- If getattr(Platform.local, “login\_manager”, no value).
  - Evaluate Platform.local.login\_manager.logout(user = self.name).
- Evaluate Platform.db.delete(“ToDo”, mapping(“allocated\_to” → self.name)).
- Set todo\_table from DocType(“ToDo”).
- Evaluate nested operand in the contract(nested operand in the contract).set(todo\_table.assigned\_by, no value).where(todo\_table.assigned\_by equals self.name).run().
- Evaluate Platform.db.delete(“Event”, mapping(“owner” → self.name, “event\_type” → “Private”)).
- Evaluate Platform.db.delete(“DocShare”, mapping(“user” → self.name)).
- Set table from DocType(“Contact”).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.user equals nested operand in the contract.name).set(table.user, no value).run().
- Evaluate Platform.delete\_doc(“Notification Settings”, self.name, ignore\_permissions = true).
- If self.get(“allowed\_in\_mentions”).
  - Evaluate Platform.cache.delete\_key(“users\_for\_mentions”).
- Evaluate Platform.cache.delete\_key(“enabled\_users”).
- Evaluate Platform.db.delete(“User Permission”, mapping(“user” → self.name)).
- Evaluate Platform.db.delete(“OAuth Authorization Code”, mapping(“user” → self.name)).
- Evaluate Platform.db.delete(“Token Cache”, mapping(“user” → self.name)).
- Evaluate Platform.db.set\_value(“Workflow Action”, mapping(“user” → self.name), “user”, no value).
- Evaluate Platform.db.delete(“List Filter”, mapping(“for\_user” → self.name)).
- Evaluate Platform.defaults.clear\_default(parent = self.name).
- Evaluate Platform.twofactor.clear\_default((self.name + “\_otplogin”)).
- Evaluate Platform.twofactor.clear\_default((self.name + “\_otpsecret”)).
- For each doctype in tuple(“Custom Sidebar”, “Dock”).
  - For each name in Platform.get\_all(doctype, filters = mapping(“user” → self.name), pluck = “name”).
    - Evaluate Platform.delete\_doc(doctype, name, ignore\_permissions = true, force = true).
- Set seen\_notes from Platform.get\_all(“Note”, filters = list(list(“Note Seen By”, “user”, “=”, self.name)), pluck = “name”).
- For each note\_id in seen\_notes.
  - Set note from Platform.get\_doc(“Note”, note\_id).
  - For each row in note.seen\_by.
    - If row.user equals self.name.
      - Evaluate note.remove(row).
  - Evaluate note.save(ignore\_permissions = true).
- Set invites from Platform.db.get\_all(“User Invitation”, filters = mapping(“email” → self.name), pluck = “name”).
- For each invite in invites.
  - Set invite\_doc from Platform.get\_doc(“User Invitation”, invite).
  - Set invite\_doc.user from no value.
  - Evaluate invite\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “login\_manager”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L57) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L702)

<a id="op-e09cbf0467831c"></a>
### User.before rename

`operation_foundation_core_record_definitions_user_business_behavior_user_before_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**State and service calls** request delete\_doc for “Notification Settings”.

**Local steps**

- If merge.
  - Evaluate Platform.delete\_doc(“Notification Settings”, old\_name, ignore\_permissions = true).
- Evaluate Platform.clear\_cache(user = old\_name).
- Evaluate self.validate\_rename(old\_name, new\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate rename](operations-098.md#op-a428935de67ae0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L4074) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L524) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L686)

<a id="op-a428935de67ae0"></a>
### User.validate rename

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_rename`

**Inputs** self, old\_name, new\_name.

**Local steps**

- If old\_name belongs to STANDARD\_USERS.
  - Evaluate throw(translated “User {0} cannot be renamed”.format(self.name)).
- Evaluate self.validate\_email\_type(new\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate email type](operations-098.md#op-9f73019c6a6e29).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L4240) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L732)

<a id="op-9f73019c6a6e29"></a>
### User.validate email type

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_email_type`

**Inputs** self, email.

**Local steps**

- Bind dependencies validate\_email\_address.
- Evaluate validate\_email\_address(email.strip(), true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L4390) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L730)

<a id="op-988f3fca41acf4"></a>
### User.after rename

`operation_foundation_core_record_definitions_user_business_behavior_user_after_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**Record and data access** read “Notification Settings” via exists.

**State and service calls** execute query text (UPDATE).format(tab, field, “%s”, field, …) · request rename\_doc for “Notification Settings” · request set\_value on “User” · request set\_value on “DefaultValue”.

**Local steps**

- Set tables from Platform.db.get\_tables().
- For each tab in tables.
  - Set desc from Platform.db.get\_table\_columns\_description(tab).
  - Set has\_fields from list of d.get(“name”) for d drawn from desc where d.get(“name”) belongs to list(“owner”, “modified\_by”).
    - Draw d from desc, keep a combination only if (d.get(“name”) belongs to list(“owner”, “modified\_by”)).
  - For each field in has\_fields.
    - Evaluate Platform.db.sql(query text (UPDATE).format(tab, field, “%s”, field, …), tuple(new\_name, old\_name)).
- If Platform.db.exists(“Notification Settings”, old\_name).
  - Evaluate Platform.rename\_doc(“Notification Settings”, old\_name, new\_name, force = true, show\_alert = false).
- Evaluate Platform.db.set\_value(“User”, new\_name, “email”, new\_name).
- If not merge.
  - Evaluate Platform.db.set\_value(“DefaultValue”, mapping(“parent” → old\_name), “parent”, new\_name).
- Evaluate Platform.twofactor.clear\_default((old\_name + “\_otplogin”)).
- Evaluate Platform.twofactor.clear\_default((old\_name + “\_otpsecret”)).
- Evaluate get\_controller(“Workspace”).rename\_private\_workspaces(old\_name, new\_name).
- Evaluate clear\_sessions(user = old\_name, force = true).
- Evaluate clear\_sessions(user = new\_name, force = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from get\_controller(“Workspace”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L52) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L682)

<a id="op-bbb5dc5af160b5"></a>
### User.append roles

`operation_foundation_core_record_definitions_user_business_behavior_user_append_roles`

**Inputs** self, remaining positional values roles.

**Local steps**

- Set current\_roles from set of d.role for d drawn from self.get(“roles”).
  - Draw d from self.get(“roles”).
- For each role in roles.
  - If role belongs to current\_roles.
    - Continue with the next iteration or loop test.
  - Evaluate self.append(“roles”, mapping(“role” → role)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L5103) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L683)

<a id="op-6d1e5e12086e14"></a>
### User.add roles

`operation_foundation_core_record_definitions_user_business_behavior_user_add_roles`

**Inputs** self, remaining positional values roles.

**State and service calls** call save on self.

**Local steps**

- Evaluate self.append\_roles(expanded roles).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [append roles](operations-098.md#op-bbb5dc5af160b5).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L5284) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L680)

<a id="op-43d7760695e1aa"></a>
### User.remove roles

`operation_foundation_core_record_definitions_user_business_behavior_user_remove_roles`

**Inputs** self, remaining positional values roles.

**State and service calls** call save on self.

**Local steps**

- Set existing\_roles from mapping of d.role → d for d drawn from self.get(“roles”).
  - Draw d from self.get(“roles”).
- For each role in roles.
  - If role belongs to existing\_roles.
    - Evaluate self.get(“roles”).remove(existing\_roles at role).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L5367) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L711)

<a id="op-7591b4b650aa59"></a>
### User.remove all roles for guest

`operation_foundation_core_record_definitions_user_business_behavior_user_remove_all_roles_for_guest`

**Inputs** self.

**Local steps**

- If self.name equals “Guest”.
  - Evaluate self.set(“roles”, list(set of d for d drawn from self.get(“roles”) where d.role equals “Guest”)).
    - Draw d from self.get(“roles”), keep a combination only if (d.role equals “Guest”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L5568) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L709)

<a id="op-4ad9c76b8536fa"></a>
### User.remove disabled roles

`operation_foundation_core_record_definitions_user_business_behavior_user_remove_disabled_roles`

**Inputs** self.

**Record and data access** read “Role” via get\_all.

**Local steps**

- Set disabled\_roles from list of d.name for d drawn from Platform.get\_all(“Role”, filters = mapping(“disabled” → 1)).
  - Draw d from Platform.get\_all(“Role”, filters = mapping(“disabled” → 1)).
- For each role in list(self.get(“roles”)).
  - If role.role belongs to disabled\_roles.
    - Evaluate self.get(“roles”).remove(role).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L5731) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L710)

<a id="op-c0f0977b37fddb"></a>
### User.ensure unique roles

`operation_foundation_core_record_definitions_user_business_behavior_user_ensure_unique_roles`

**Inputs** self.

**Local steps**

- Set exists from set().
- For each d in list(self.roles).
  - If (not d.role or d.role belongs to exists).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.role → d.role belongs to exists.
    - Evaluate self.roles.remove(d).
  - Evaluate exists.add(d.role).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L55) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L692)

<a id="op-6f6154e2fdd871"></a>
### User.ensure unique role profiles

`operation_foundation_core_record_definitions_user_business_behavior_user_ensure_unique_role_profiles`

**Inputs** self.

**Local steps**

- Set seen from set().
- For each rp in list(self.role\_profiles).
  - If rp.role\_profile belongs to seen.
    - Evaluate self.role\_profiles.remove(rp).
  - Evaluate seen.add(rp.role\_profile).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L54) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L691)

<a id="op-cf63d8a61a758a"></a>
### User.validate username

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_username`

**Inputs** self.

**State and service calls** msgprint with translated “Username {0} already exists”.format(self.username).

**Explicit results** no value.

**Local steps**

- If (not self.username and self.is\_new() and self.first\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.username → self.is\_new() → self.first\_name.
  - Set self.username from self.free\_username(Platform.scrub(self.first\_name)).
  - Set self.flags.username\_from\_first\_name from true.
- If not self.username.
  - Return no value.
- Set self.username from self.username.strip(“ @”).
- If self.username\_exists().
  - If self.user\_type equals “System User”.
    - Evaluate Platform.msgprint(translated “Username {0} already exists”.format(self.username)).
    - Evaluate self.suggest\_username().
  - Set self.username from empty text.

If control reaches the end, it returns no value.

**Methods declared on this owner** [free username](operations-098.md#op-2b73642aa5b2b8), [username exists](operations-098.md#op-282762bc2a931c), [suggest username](operations-098.md#op-485426cd3c3e24).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L63) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L736)

<a id="op-2b73642aa5b2b8"></a>
### User.free username

`operation_foundation_binding_foundation_core_doctype_user_user_user_free_username`

**Inputs** self, base.

**Record and data access** read “User” via get\_all.

**Explicit results** base · formatted text {prefix}{(max(generator of int(n) for n drawn from numbers where n.isdecimal(), default = 0) + 1)}.

**Local steps**

- If not self.username\_exists(base).
  - Return base.
- Set prefix from formatted text {base}-.
- Set pattern from (prefix.replace(“\\”, “\_”) + “%”).
- Set taken from Platform.get\_all(“User”, filters = mapping(“username” → tuple(“like”, pattern)), pluck = “username”).
- Set numbers from generator of username.rpartition(“-”) at 2 for username drawn from taken.
  - Draw username from taken.
- Return formatted text {prefix}{(max(generator of int(n) for n drawn from numbers where n.isdecimal(), default = 0) + 1)}.
  - Draw n from numbers, keep a combination only if (n.isdecimal()).

**Methods declared on this owner** [username exists](operations-098.md#op-282762bc2a931c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L189) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L647)

<a id="op-bf53675cbd1ace"></a>
### User.db insert

`operation_foundation_binding_foundation_core_doctype_user_user_user_db_insert`

**Inputs** self, ignore\_if\_duplicate = false.

**State and service calls** call db\_insert on super() · savepoint “user\_username” · rollback · release savepoint “user\_username”.

**Explicit results** super().db\_insert(ignore\_if\_duplicate = ignore\_if\_duplicate) · no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- If not self.flags.username\_from\_first\_name.
  - Return super().db\_insert(ignore\_if\_duplicate = ignore\_if\_duplicate).
- For each attempt in range(5).
  - Set messages from len(Platform.message\_log).
  - Evaluate Platform.db.savepoint(“user\_username”).
  - Attempt the following.
    - Evaluate super().db\_insert(ignore\_if\_duplicate = ignore\_if\_duplicate).
  - On failure (Platform.UniqueValidationError) bound to e.
    - If (attempt equals 4 or “username” does not belong to str(e.args at negative 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in attempt equals 4 → “username” does not belong to str(e.args at negative 1).
      - Propagate the active failure.
    - Evaluate Platform.db.rollback(save\_point = “user\_username”).
    - Remove Platform.message\_log at slice messages to no value.
    - Set tuple(base, sep, number) from self.username.rpartition(“-”).
    - Set self.username from formatted text {base}-{(int(number) + 1)} when sep, otherwise formatted text {self.username}-1.
      - Value choice on sep — true gives formatted text {base}-{(int(number) + 1)}, false gives formatted text {self.username}-1.
  - When the protected block completes normally.
    - Evaluate Platform.db.release\_savepoint(“user\_username”).
    - Return no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L188) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L646)

<a id="op-0f7d262dd64fca"></a>
### User.password strength test

`operation_foundation_core_record_definitions_user_business_behavior_user_password_strength_test`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L6820) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L706)

<a id="op-485426cd3c3e24"></a>
### User.suggest username

`operation_foundation_core_record_definitions_user_business_behavior_user_suggest_username`

**Inputs** self.

**State and service calls** msgprint with translated “Suggested Username: {0}”.format(username).

**Explicit results** username.

**Local steps**

- Bind local operation \_check\_suggestion for subsequent calls.
- Set username from \_check\_suggestion(Platform.scrub(self.first\_name)).
- If not username.
  - Set username from \_check\_suggestion(Platform.scrub(“{} {}”.format(self.first\_name, (self.last\_name or empty text)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.last\_name → empty text.
- If username.
  - Evaluate Platform.msgprint(translated “Suggested Username: {0}”.format(username)).
- Return username.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L7088) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L724)

<a id="op-62965a7d71e330"></a>
### User.suggest username.check suggestion

`operation_foundation_core_record_definitions_user_business_behavior_user_suggest_username_check_suggestion`

**Inputs** suggestion.

**Explicit results** suggestion · no value.

**Local steps**

- If (self.username differs from suggestion and not self.username\_exists(suggestion)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.username differs from suggestion → not self.username\_exists(suggestion).
  - Return suggestion.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L7417) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L725)

<a id="op-282762bc2a931c"></a>
### User.username exists

`operation_foundation_core_record_definitions_user_business_behavior_user_username_exists`

**Inputs** self, username = no value.

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.db.get\_value(“User”, mapping(“username” → (username or self.username), “name” → tuple(“!=”, self.name))).

**Local steps**

- Return Platform.db.get\_value(“User”, mapping(“username” → (username or self.username), “name” → tuple(“!=”, self.name))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in username → self.username.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L727)

<a id="op-4ef8835994b3e0"></a>
### User.get blocked modules

`operation_foundation_core_record_definitions_user_business_behavior_user_get_blocked_modules`

**Inputs** self.

**Explicit results** list of d.module for d drawn from self.block\_modules when self.block\_modules, otherwise list().

**Local steps**

- Return list of d.module for d drawn from self.block\_modules when self.block\_modules, otherwise list().
  - Value choice on self.block\_modules — true gives list of d.module for d drawn from self.block\_modules, false gives list().
  - Draw d from self.block\_modules.

[Applicable decision contract](../../../foundation-decision-contracts/part-0112.json#L145) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L694)
