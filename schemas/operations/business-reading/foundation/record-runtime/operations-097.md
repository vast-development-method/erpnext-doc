# Record lifecycle and persistence · operations 97

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · User

[Record definition](../../../../data/record-types/user.json)

<a id="op-369e3091eb3c5c"></a>
### User.autoname

`operation_foundation_core_record_definitions_user_business_behavior_user_autoname`

**Inputs** self.

**Local steps**

- If (self.get(“is\_admin”) or self.get(“is\_guest”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_admin”) → self.get(“is\_guest”).
  - Set self.name from self.first\_name.
- Otherwise.
  - Set self.email from self.email.strip().lower().
  - Set self.name from self.email.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L1907) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L684)

<a id="op-ed418fd4376658"></a>
### User.onload

`operation_foundation_core_record_definitions_user_business_behavior_user_onload`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_blockable\_module\_names.
- If not self.has\_permlevel\_access\_to(“block\_modules”, permission\_type = “write”).
  - Return no value.
- Evaluate self.set\_onload(“all\_modules”, get\_blockable\_module\_names(blocked = list of d.module for d drawn from self.block\_modules)).
  - Draw d from self.block\_modules.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L59) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L704)

<a id="op-5e9b00e6702121"></a>
### User.before insert

`operation_foundation_core_record_definitions_user_business_behavior_user_before_insert`

**Inputs** self.

**Local steps**

- Set self.flags.in\_insert from true.
- Evaluate throttle\_user\_creation().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L2205) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L685)

<a id="op-f385bdf1609d54"></a>
### User.after insert

`operation_foundation_core_record_definitions_user_business_behavior_user_after_insert`

**Inputs** self.

**Local steps**

- Evaluate create\_notification\_settings(self.name).
- Evaluate Platform.cache.delete\_key(“users\_for\_mentions”).
- Evaluate Platform.cache.delete\_key(“enabled\_users”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L2273) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L681)

<a id="op-f8292d17dbca26"></a>
### User.validate

`operation_foundation_core_record_definitions_user_business_behavior_user_validate`

**Inputs** self.

**Local steps**

- If self.new\_password.
  - Set self.\_\_new\_password from self.new\_password.
- Set self.new\_password from empty text.
- If not Platform.in\_test.
  - Evaluate self.password\_strength\_test().
- If self.name does not belong to STANDARD\_USERS.
  - Set self.email from self.name.
  - Evaluate self.validate\_email\_type(self.name).
- Evaluate self.move\_role\_profile\_name\_to\_role\_profiles().
- Evaluate self.populate\_role\_profile\_roles().
- Evaluate self.check\_roles\_added().
- Evaluate self.set\_system\_user().
- Evaluate self.clean\_name().
- Evaluate self.set\_full\_name().
- Evaluate self.check\_enable\_disable().
- Evaluate self.ensure\_unique\_roles().
- Evaluate self.ensure\_unique\_role\_profiles().
- Evaluate self.sync\_role\_profile\_name().
- Evaluate self.remove\_all\_roles\_for\_guest().
- Evaluate self.validate\_username().
- Evaluate self.remove\_disabled\_roles().
- Evaluate self.validate\_user\_email\_inbox().
- If self.user\_emails.
  - Evaluate ask\_pass\_update().
- Evaluate self.validate\_allowed\_modules().
- Evaluate self.validate\_user\_image().
- Evaluate self.set\_time\_zone().
- If self.restrict\_ip.
  - Evaluate self.validate\_ip\_addr().
- If self.language equals “Loading...”.
  - Set self.language from no value.
- If (self.default\_app and self.default\_app does not belong to Platform.get\_installed\_apps()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default\_app → self.default\_app does not belong to Platform.get\_installed\_apps().
  - Set self.default\_app from empty text.
- Evaluate self.set\_Platform\_social\_login\_userid().

If control reaches the end, it returns no value.

**Methods declared on this owner** [password strength test](operations-098.md#op-0f7d262dd64fca), [validate email type](operations-098.md#op-9f73019c6a6e29), [move role profile name to role profiles](operations-097.md#op-3df8253e0d739a), [populate role profile roles](operations-097.md#op-397e546fc58413), [check roles added](operations-099.md#op-3f689dba4e8dad), [set system user](operations-097.md#op-8f56bfd26ca56c), [clean name](operations-097.md#op-ad0d85487b0b32), [set full name](operations-097.md#op-b2fad10fce938c), [check enable disable](operations-097.md#op-f47e5eda9e3436), [ensure unique roles](operations-098.md#op-c0f0977b37fddb), [ensure unique role profiles](operations-098.md#op-6f6154e2fdd871), [sync role profile name](operations-097.md#op-617438297f1969), [remove all roles for guest](operations-098.md#op-7591b4b650aa59), [validate username](operations-098.md#op-cf63d8a61a758a), [remove disabled roles](operations-098.md#op-4ad9c76b8536fa), [validate user email inbox](operations-099.md#op-a557e454733cbb), [validate allowed modules](operations-097.md#op-d35de11d1b800f), [validate user image](operations-097.md#op-42c9c6c6e12f4f), [set time zone](operations-099.md#op-828b94a5793d0f), [validate ip addr](operations-099.md#op-a5e7856df1ed59), [set Platform social login userid](operations-099.md#op-45b7235e433661).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L62) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L728)

<a id="op-07f037a55d9469"></a>
### User.disable email fields if user disabled

`operation_foundation_core_record_definitions_user_business_behavior_user_disable_email_fields_if_user_disabled`

**Inputs** self.

**Local steps**

- If not self.enabled.
  - Set self.thread\_notify from 0.
  - Set self.send\_me\_a\_copy from 0.
  - Set self.allowed\_in\_mentions from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L3228) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L690)

<a id="op-397e546fc58413"></a>
### User.populate role profile roles

`operation_foundation_core_record_definitions_user_business_behavior_user_populate_role_profile_roles`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Role Profile” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- If not self.role\_profiles.
  - Return no value.
- If self.name belongs to STANDARD\_USERS.
  - Set self.role\_profiles from list().
  - Return no value.
- Set new\_roles from set().
- For each role\_profile in self.role\_profiles.
  - Set role\_profile from Platform.get\_cached\_doc(“Role Profile”, role\_profile.role\_profile).
  - Evaluate new\_roles.update(generator of role.role for role drawn from role\_profile.roles).
    - Draw role from role\_profile.roles.
- Set self.roles from list of r for r drawn from self.roles where r.role belongs to new\_roles.
  - Draw r from self.roles, keep a combination only if (r.role belongs to new\_roles).
- Evaluate self.append\_roles(expanded new\_roles).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append roles](operations-098.md#op-bbb5dc5af160b5).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Role Profile”, role\_profile.role\_profile).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L60) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L707)

<a id="op-3df8253e0d739a"></a>
### User.move role profile name to role profiles

`operation_foundation_core_record_definitions_user_business_behavior_user_move_role_profile_name_to_role_profiles`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.role\_profile\_name or not self.has\_value\_changed(“role\_profile\_name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.role\_profile\_name → not self.has\_value\_changed(“role\_profile\_name”).
  - Return no value.
- Set current\_role\_profiles from set of r.role\_profile for r drawn from self.role\_profiles.
  - Draw r from self.role\_profiles.
- If self.role\_profile\_name belongs to current\_role\_profiles.
  - Set self.role\_profile\_name from no value.
  - Return no value.
- Bind dependencies deprecation\_warning.
- Evaluate record a compatibility advisory for the invoked interface.
- Evaluate self.append(“role\_profiles”, mapping(“role\_profile” → self.role\_profile\_name)).
- Set self.role\_profile\_name from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L56) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L701)

<a id="op-617438297f1969"></a>
### User.sync role profile name

`operation_foundation_core_record_definitions_user_business_behavior_user_sync_role_profile_name`

**Inputs** self.

**Local steps**

- Set self.role\_profile\_name from self.role\_profiles at 0.role\_profile when self.role\_profiles, otherwise no value.
  - Value choice on self.role\_profiles — true gives self.role\_profiles at 0.role\_profile, false gives no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L4018) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L726)

<a id="op-d35de11d1b800f"></a>
### User.validate allowed modules

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_allowed_modules`

**Inputs** self.

**Record and data access** resolve a document from “Module Profile” via get\_doc.

**Local steps**

- If self.module\_profile.
  - Set module\_profile from Platform.get\_doc(“Module Profile”, self.module\_profile).
  - Evaluate self.set(“block\_modules”, list()).
  - For each d in module\_profile.get(“block\_modules”).
    - Evaluate self.append(“block\_modules”, mapping(“module” → d.module)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L4094) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L729)

<a id="op-42c9c6c6e12f4f"></a>
### User.validate user image

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_user_image`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Not a valid User Image.”.

**Local steps**

- If (self.user\_image and len(self.user\_image) &gt; 2000).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.user\_image → len(self.user\_image) &gt; 2000.
  - Call the validation error handler Platform.throw(translated “Not a valid User Image.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L4302) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L735)

<a id="op-ccf0deb2358938"></a>
### User.on update

`operation_foundation_core_record_definitions_user_business_behavior_user_on_update`

**Inputs** self.

**Record and data access** resolve a document from “Language” via get\_doc.

**State and service calls** enqueue with “Platform.core.doctype.user.user.create\_contact”.

**Local steps**

- Evaluate self.share\_with\_self().
- Evaluate clear\_notifications(user = self.name).
- Evaluate Platform.clear\_cache(user = self.name).
- Set now from (Platform.in\_test or Platform.flags.in\_install).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.in\_test → Platform.flags.in\_install.
- Evaluate self.send\_password\_notification(self.\_\_new\_password).
- Set self.\_\_new\_password from no value.
- Evaluate Platform.enqueue(“Platform.core.doctype.user.user.create\_contact”, user = self, ignore\_mandatory = true, now = now, enqueue\_after\_commit = true).
- If self.time\_zone.
  - Evaluate Platform.defaults.set\_default(“time\_zone”, self.time\_zone, self.name).
- If self.has\_value\_changed(“language”).
  - Set locale\_keys from tuple(“date\_format”, “time\_format”, “number\_format”, “first\_day\_of\_the\_week”).
  - If self.language.
    - Set language from Platform.get\_doc(“Language”, self.language).
    - For each key in locale\_keys.
      - Set value from language.get(key).
      - If value.
        - Evaluate Platform.defaults.set\_default(key, value, self.name).
  - Otherwise.
    - For each key in locale\_keys.
      - Evaluate Platform.defaults.clear\_default(key, parent = self.name).
- If self.has\_value\_changed(“enabled”).
  - Evaluate Platform.cache.delete\_key(“users\_for\_mentions”).
  - Evaluate Platform.cache.delete\_key(“enabled\_users”).
- Otherwise.
  - If (self.has\_value\_changed(“allowed\_in\_mentions”) or self.has\_value\_changed(“user\_type”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“allowed\_in\_mentions”) → self.has\_value\_changed(“user\_type”).
    - Evaluate Platform.cache.delete\_key(“users\_for\_mentions”).
- If self.has\_value\_changed(“user\_type”).
  - Evaluate clear\_sessions(user = self.name, force = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [share with self](operations-097.md#op-610249dd1cb704), [send password notification](operations-097.md#op-4779b36b92f7e7).

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.core.doctype.user.user.create\_contact”, user = self, ignore\_mandatory = true, now = now, enqueue\_after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L58) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L703)

<a id="op-539aeb34b50f75"></a>
### User.has website permission

`operation_foundation_core_record_definitions_user_business_behavior_user_has_website_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, ptype, user, verbose.

**Explicit result forms** a comparison result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L5324) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L700)

<a id="op-ad0d85487b0b32"></a>
### User.clean name

`operation_foundation_core_record_definitions_user_business_behavior_user_clean_name`

**Inputs** self.

**Local steps**

- For each field in tuple(“first\_name”, “middle\_name”, “last\_name”).
  - If field\_value bound to self.get(field).
    - Evaluate self.set(field, sanitize\_html(field\_value, always\_sanitize = true, disallowed\_tags = “\*”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L5412) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L689)

<a id="op-b2fad10fce938c"></a>
### User.set full name

`operation_foundation_core_record_definitions_user_business_behavior_user_set_full_name`

**Inputs** self.

**Local steps**

- Set self.full\_name from one space.join(generator of p for p drawn from list(self.first\_name, self.middle\_name, self.last\_name) where p).
  - Draw p from list(self.first\_name, self.middle\_name, self.last\_name), keep a combination only if (p).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L5582) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L716)

<a id="op-f47e5eda9e3436"></a>
### User.check enable disable

`operation_foundation_core_record_definitions_user_business_behavior_user_check_enable_disable`

**Inputs** self.

**Explicit failure paths** validation helper — translated “User {0} cannot be disabled”.format(self.name).

**Local steps**

- If (not cint(self.enabled) and self.name belongs to STANDARD\_USERS).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.enabled) → self.name belongs to STANDARD\_USERS.
  - Call the validation error handler Platform.throw(translated “User {0} cannot be disabled”.format(self.name)).
- If (not cint(self.enabled) and getattr(Platform.local, “login\_manager”, no value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(self.enabled) → getattr(Platform.local, “login\_manager”, no value).
  - Evaluate Platform.local.login\_manager.logout(user = self.name).
- Evaluate toggle\_notifications(self.name, enable = cint(self.enabled), ignore\_permissions = true).
- Evaluate self.disable\_email\_fields\_if\_user\_disabled().

If control reaches the end, it returns no value.

**Methods declared on this owner** [disable email fields if user disabled](operations-097.md#op-07f037a55d9469).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “login\_manager”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L5694) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L525) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L687)

<a id="op-3f4b4e9c1f3a61"></a>
### User.set new password

`operation_foundation_core_record_definitions_user_business_behavior_user_set_new_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, new\_password.

**Observed service boundaries** notification or queued-work request, record lookup.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L61) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L717)

<a id="op-8f56bfd26ca56c"></a>
### User.set system user

`operation_foundation_core_record_definitions_user_business_behavior_user_set_system_user`

**Inputs** self.

**Record and data access** read “User Type” via get\_cached\_value.

**Local steps**

- Set user\_type\_mapper from mapping(“Administrator” → “System User”, “Guest” → “Website User”).
- If (self.user\_type and not Platform.get\_cached\_value(“User Type”, self.user\_type, “is\_standard”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.user\_type → not Platform.get\_cached\_value(“User Type”, self.user\_type, “is\_standard”).
  - If user\_type\_mapper.get(self.name).
    - Set self.user\_type from user\_type\_mapper.get(self.name).
  - Otherwise.
    - Evaluate self.set\_roles\_and\_modules\_based\_on\_user\_type().
- Otherwise.
  - Set self.user\_type from “System User” when self.has\_desk\_access(), otherwise “Website User”.
    - Value choice on self.has\_desk\_access() — true gives “System User”, false gives “Website User”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set roles and modules based on user type](operations-097.md#op-850a82ff1569f8), [has desk access](operations-097.md#op-48e7adb5905a5c).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User Type”, self.user\_type, “is\_standard”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L6400) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L720)

<a id="op-850a82ff1569f8"></a>
### User.set roles and modules based on user type

`operation_foundation_core_record_definitions_user_business_behavior_user_set_roles_and_modules_based_on_user_type`

**Inputs** self.

**Record and data access** resolve a document from “User Type” via get\_cached\_doc.

**State and service calls** msgprint with translated “Role has been set as per the user type {0}”.format(self.user\_type).

**Local steps**

- Set user\_type\_doc from Platform.get\_cached\_doc(“User Type”, self.user\_type).
- If user\_type\_doc.role.
  - Set self.roles from list().
  - If user\_linked\_with\_permission\_on\_doctype(user\_type\_doc, self.name).
    - Evaluate self.append(“roles”, mapping(“role” → user\_type\_doc.role)).
    - Evaluate Platform.msgprint(translated “Role has been set as per the user type {0}”.format(self.user\_type), alert = true).
- Evaluate user\_type\_doc.update\_modules\_in\_user(self).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“User Type”, self.user\_type).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L6667) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L718)

<a id="op-48e7adb5905a5c"></a>
### User.has desk access

`operation_foundation_core_record_definitions_user_business_behavior_user_has_desk_access`

**Inputs** self.

**Record and data access** read role\_table via count.

**Explicit results** false · Platform.db.count(role\_table, (role\_table.desk\_access equals 1 bitwise and role\_table.name.isin(list of d.role for d drawn from self.roles))).

**Local steps**

- If not self.roles.
  - Return false.
- Set role\_table from DocType(“Role”).
- Return Platform.db.count(role\_table, (role\_table.desk\_access equals 1 bitwise and role\_table.name.isin(list of d.role for d drawn from self.roles))).
  - Draw d from self.roles.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L6949) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L699)

<a id="op-610249dd1cb704"></a>
### User.share with self

`operation_foundation_core_record_definitions_user_business_behavior_user_share_with_self`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.name belongs to STANDARD\_USERS.
  - Return no value.
- Evaluate Platform.share.add\_docshare(self.doctype, self.name, self.name, write = 1, share = 1, flags = mapping(“ignore\_share\_permission” → true)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0110.json#L7141) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L723)

<a id="op-4779b36b92f7e7"></a>
### User.send password notification

`operation_foundation_core_record_definitions_user_business_behavior_user_send_password_notification`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, new\_password.

**Explicit result forms** no value.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L714)

<a id="op-3a260036c8c7c8"></a>
### User.validate reset password

`operation_foundation_core_record_definitions_user_business_behavior_user_validate_reset_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L479) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L571) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L733)

<a id="op-39222774e66e2e"></a>
### User.reset password

`operation_foundation_core_record_definitions_user_business_behavior_user_reset_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, send\_email, password\_expired.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record mutation request.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0111.json#L521) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L712)
