# Integration and transport · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Integration request

[Record definition](../../../../data/record-types/integration_request.json)

<a id="op-ae48139e68d6db"></a>
### Integration Request.autoname

`operation_foundation_integrations_record_definitions_integration_request_business_behavior_integration_request_autoname`

**Inputs** self.

**Local steps**

- If self.flags.\_name.
  - Set self.name from self.flags.\_name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L6053) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L30) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L756)

<a id="op-de65ea4050cef1"></a>
### Integration Request.clear old logs

`operation_foundation_integrations_record_definitions_integration_request_business_behavior_integration_request_clear_old_logs`

**Inputs** days = 30.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Integration Request”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L6128) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L31) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L757)

<a id="op-520e228c8011c1"></a>
### Integration Request.update status

`operation_foundation_integrations_record_definitions_integration_request_business_behavior_integration_request_update_status`

**Inputs** self, params, status.

**State and service calls** call save on self · commit.

**Local steps**

- Set data from json.loads(self.data).
- Evaluate data.update(params).
- Set self.data from get\_json(data).
- Set self.status from status.
- Evaluate self.save(ignore\_permissions = true).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L6308) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L34) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L760)

<a id="op-a4f35dfddd3728"></a>
### Integration Request.handle success

`operation_foundation_integrations_record_definitions_integration_request_business_behavior_integration_request_handle_success`

**Inputs** self, response.

**State and service calls** call db\_set on self.

**Local steps**

- If isinstance(response, str).
  - Set response from json.loads(response).
- Evaluate self.db\_set(“status”, “Completed”).
- Evaluate self.db\_set(“output”, json.dumps(response, default = json\_handler)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L6508) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L33) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L759)

<a id="op-487e737ff7d50d"></a>
### Integration Request.handle failure

`operation_foundation_integrations_record_definitions_integration_request_business_behavior_integration_request_handle_failure`

**Inputs** self, response.

**State and service calls** call db\_set on self.

**Local steps**

- If isinstance(response, str).
  - Set response from json.loads(response).
- Evaluate self.db\_set(“status”, “Failed”).
- Evaluate self.db\_set(“error”, json.dumps(response, default = json\_handler)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L6690) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L32) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L758)

## Record · Ldap settings

<a id="op-3b17314f9ca270"></a>
### LDAPSettings.validate

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_validate`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “LDAP settings incorrect. validation response was: {0}”.format(str(ex)) · validation helper — translated “Ensure the user and group search paths are correct.” · validation helper — translated “Custom LDAP Directoy Selected, please ensure 'LDAP Group Member attribute' and 'Group Object Class' are entered” · validation helper — translated “Custom Group Search if filled needs to contain the user placeholder {0}, eg uid={0},ou=users,dc=example,dc=com” · validation helper — translated “LDAP Search String must be enclosed in '()' and needs to contian the user placeholder {0}, eg sAMAccountName={0}”.

**Local steps**

- Set self.default\_user\_type from (self.default\_user\_type or “Website User”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.default\_user\_type → “Website User”.
- If not self.enabled.
  - Return no value.
- If not self.flags.ignore\_mandatory.
  - If (self.ldap\_search\_string.count(“(”) equals self.ldap\_search\_string.count(“)”) and self.ldap\_search\_string.startswith(“(”) and self.ldap\_search\_string.endswith(“)”) and self.ldap\_search\_string and “{0}” bel ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.ldap\_search\_string.count(“(”) equals self.ldap\_search\_string.count(“)”) → self.ldap\_search\_string.startswith(“(”) → self.ldap\_search\_string.endswith(“)”) → self.ldap\_search\_string → “{0}” belongs to self.ldap\_search\_string.
    - Set conn from self.connect\_to\_ldap(base\_dn = self.base\_dn, password = self.get\_password(raise\_exception = false)).
    - Attempt the following.
      - If (conn.result at “type” equals “bindResponse” and self.base\_dn).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in conn.result at “type” equals “bindResponse” → self.base\_dn.
        - Evaluate conn.search(search\_base = self.ldap\_search\_path\_user, search\_filter = “(objectClass=\*)”, attributes = self.get\_ldap\_attributes()).
        - Evaluate conn.search(search\_base = self.ldap\_search\_path\_group, search\_filter = “(objectClass=\*)”, attributes = list(“cn”)).
    - On failure (LDAPAttributeError) bound to ex.
      - Call the validation error handler Platform.throw(translated “LDAP settings incorrect. validation response was: {0}”.format(str(ex)), title = translated “Misconfigured”).
    - On failure (LDAPNoSuchObjectResult).
      - Call the validation error handler Platform.throw(translated “Ensure the user and group search paths are correct.”, title = translated “Misconfigured”).
    - If self.ldap\_directory\_server.lower() equals “custom”.
      - If (not self.ldap\_group\_member\_attribute or not self.ldap\_group\_objectclass).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.ldap\_group\_member\_attribute → not self.ldap\_group\_objectclass.
        - Call the validation error handler Platform.throw(translated “Custom LDAP Directoy Selected, please ensure 'LDAP Group Member attribute' and 'Group Object Class' are entered”, title = translated “Misconfigured”).
    - If (self.ldap\_custom\_group\_search and “{0}” does not belong to self.ldap\_custom\_group\_search).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.ldap\_custom\_group\_search → “{0}” does not belong to self.ldap\_custom\_group\_search.
      - Call the validation error handler Platform.throw(translated “Custom Group Search if filled needs to contain the user placeholder {0}, eg uid={0},ou=users,dc=example,dc=com”, title = translated “Misconfigured”).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “LDAP Search String must be enclosed in '()' and needs to contian the user placeholder {0}, eg sAMAccountName={0}”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [connect to ldap](operations-021.md#op-c149c6cd6b1a6a), [get ldap attributes](operations-021.md#op-500592297c7021).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L45) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L771)

<a id="op-c149c6cd6b1a6a"></a>
### LDAPSettings.connect to ldap

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_connect_to_lightweight_directory_access_protocol`

**Inputs** self, base\_dn, password, read\_only = true.

**Declared result** ldap3.Connection.

**Explicit results** ldap3.Connection(server = server, user = base\_dn, password = password, auto\_bind = bind\_type, …).

**Explicit failure paths** validation helper — msg · validation helper — translated “Invalid username or password” · validation helper — translated str(ex).

**Local steps**

- Attempt the following.
  - If self.require\_trusted\_certificate equals “Yes”.
    - Set tls\_configuration from ldap3.Tls(validate = ssl.CERT\_REQUIRED, version = ssl.PROTOCOL\_TLS\_CLIENT).
  - Otherwise.
    - Set tls\_configuration from ldap3.Tls(validate = ssl.CERT\_NONE, version = ssl.PROTOCOL\_TLS\_CLIENT).
  - If self.local\_private\_key\_file.
    - Set tls\_configuration.private\_key\_file from self.local\_private\_key\_file.
  - If self.local\_server\_certificate\_file.
    - Set tls\_configuration.certificate\_file from self.local\_server\_certificate\_file.
  - If self.local\_ca\_certs\_file.
    - Set tls\_configuration.ca\_certs\_file from self.local\_ca\_certs\_file.
  - Set server from ldap3.Server(host = self.ldap\_server\_url, tls = tls\_configuration).
  - Set bind\_type from AUTO\_BIND\_TLS\_BEFORE\_BIND when self.ssl\_tls\_mode equals “StartTLS”, otherwise true.
    - Value choice on self.ssl\_tls\_mode equals “StartTLS” — true gives AUTO\_BIND\_TLS\_BEFORE\_BIND, false gives true.
  - Return ldap3.Connection(server = server, user = base\_dn, password = password, auto\_bind = bind\_type, …).
- On failure (ImportError).
  - Set msg from translated “Please Install the ldap3 library via pip to use ldap functionality.”.
  - Call the validation error handler Platform.throw(msg, title = translated “LDAP Not Installed”).
- On failure (LDAPInvalidCredentialsResult).
  - Call the validation error handler Platform.throw(translated “Invalid username or password”).
- On failure (Exception) bound to ex.
  - Call the validation error handler Platform.throw(translated str(ex)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L985) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L36) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L762)

<a id="op-b6389b0bd40999"></a>
### LDAPSettings.get ldap client settings

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_get_lightweight_directory_access_protocol_client_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Record and data access** resolve a document from “LDAP Settings” via get\_cached\_doc.

**Explicit results** result.

**Local steps**

- Set result from mapping(“enabled” → false).
- Set ldap from Platform.get\_cached\_doc(“LDAP Settings”).
- If ldap.enabled.
  - Set result at “enabled” from true.
  - Set result at “method” from “Platform.integrations.doctype.ldap\_settings.ldap\_settings.login”.
- Return result.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“LDAP Settings”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L1647) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L41) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L767)

<a id="op-580cd4301f0ab1"></a>
### LDAPSettings.update user fields

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_update_user_fields`

**Inputs** cls, user, user\_data.

**Wrappers, in declaration order** classmethod.

**State and service calls** call save on user.

**Local steps**

- Set updatable\_data from mapping of key → value for tuple(key, value) drawn from user\_data.items() where key differs from “email”.
  - Draw tuple(key, value) from user\_data.items(), keep a combination only if (key differs from “email”).
- For each tuple(key, value) in updatable\_data.items().
  - Evaluate setattr(user, key, value).
- Evaluate user.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L1873) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L44) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L770)

<a id="op-c42bfa7bbc3682"></a>
### LDAPSettings.sync roles

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_sync_roles`

**Inputs** self, user, additional\_groups = no value.

**Local steps**

- Set current\_roles from set of d.role for d drawn from user.get(“roles”).
  - Draw d from user.get(“roles”).
- If self.default\_user\_type equals “System User”.
  - Set needed\_roles from set(self.default\_role).
- Otherwise.
  - Set needed\_roles from set().
- Set lower\_groups from list of g.lower() for g drawn from (additional\_groups or list()).
  - Draw g from (additional\_groups or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in additional\_groups → list().
- Set all\_mapped\_roles from set of r.Enterprise\_role for r drawn from self.ldap\_groups.
  - Draw r from self.ldap\_groups.
- Set matched\_roles from set of r.Enterprise\_role for r drawn from self.ldap\_groups where r.ldap\_group.lower() belongs to lower\_groups.
  - Draw r from self.ldap\_groups, keep a combination only if (r.ldap\_group.lower() belongs to lower\_groups).
- Set unmatched\_roles from all\_mapped\_roles.difference(matched\_roles).
- Evaluate needed\_roles.update(matched\_roles).
- Set roles\_to\_remove from current\_roles.intersection(unmatched\_roles).
- If not needed\_roles.issubset(current\_roles).
  - Set missing\_roles from needed\_roles.difference(current\_roles).
  - Evaluate user.add\_roles(expanded missing\_roles).
- Evaluate user.remove\_roles(expanded roles\_to\_remove).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L2103) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L43) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L769)

<a id="op-c0f5ca06037ba3"></a>
### LDAPSettings.create or update user

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_create_or_update_user`

**Inputs** self, user\_data, groups = no value.

**Record and data access** read “User” via exists · resolve a document from “User” via get\_doc · resolve a document from doc via get\_doc · read “User Type” via get\_value.

**State and service calls** call insert on user.

**Explicit results** user.

**Explicit failure paths** validation helper — translated “User with email: {0} does not exist in the system. Please ask 'System Administrator' to create the user for you.”.format(user\_data at “email”).

**Local steps**

- Set user from no value.
- Set role from no value.
- If Platform.db.exists(“User”, user\_data at “email”).
  - Set user from Platform.get\_doc(“User”, user\_data at “email”).
  - Evaluate LDAPSettings.update\_user\_fields(user = user, user\_data = user\_data).
- Otherwise.
  - If not self.do\_not\_create\_new\_user.
    - Set doc from (user\_data bitwise or mapping(“doctype” → “User”, “send\_welcome\_email” → 0, “language” → empty text, “user\_type” → self.default\_user\_type)).
    - Set user from Platform.get\_doc(doc).
    - Evaluate user.insert(ignore\_permissions = true).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “User with email: {0} does not exist in the system. Please ask 'System Administrator' to create the user for you.”.format(user\_data at “email”)).
- If self.default\_user\_type equals “System User”.
  - Set role from self.default\_role.
- Otherwise.
  - Set role from Platform.db.get\_value(“User Type”, user.user\_type, “role”).
- If role.
  - Evaluate user.add\_roles(role).
- Evaluate self.sync\_roles(user, groups).
- Return user.

**Methods declared on this owner** [sync roles](operations-021.md#op-c42bfa7bbc3682).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L2661) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L38) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L764)

<a id="op-500592297c7021"></a>
### LDAPSettings.get ldap attributes

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_get_lightweight_directory_access_protocol_attributes`

**Inputs** self.

**Explicit results** ldap\_attributes.

**Local steps**

- Set ldap\_attributes from list(self.ldap\_email\_field, self.ldap\_username\_field, self.ldap\_first\_name\_field).
- If self.ldap\_group\_field.
  - Evaluate ldap\_attributes.append(self.ldap\_group\_field).
- If self.ldap\_middle\_name\_field.
  - Evaluate ldap\_attributes.append(self.ldap\_middle\_name\_field).
- If self.ldap\_last\_name\_field.
  - Evaluate ldap\_attributes.append(self.ldap\_last\_name\_field).
- If self.ldap\_phone\_field.
  - Evaluate ldap\_attributes.append(self.ldap\_phone\_field).
- If self.ldap\_mobile\_field.
  - Evaluate ldap\_attributes.append(self.ldap\_mobile\_field).
- Return ldap\_attributes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L3300) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L40) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L766)

<a id="op-c4e5ab7fe83edc"></a>
### LDAPSettings.fetch ldap groups

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_fetch_lightweight_directory_access_protocol_groups`

**Inputs** self, user, conn.

**Declared result** list.

**Explicit results** fetch\_ldap\_groups.

**Explicit failure paths** TypeError(“Invalid type, attribute 'user' must be of type 'ldap3.abstract.entry.Entry'”) · TypeError(“Invalid type, attribute 'conn' must be of type 'ldap3.Connection'”).

**Local steps**

- If not isinstance(user, Entry).
  - Raise TypeError(“Invalid type, attribute 'user' must be of type 'ldap3.abstract.entry.Entry'”).
- If not isinstance(conn, ldap3.Connection).
  - Raise TypeError(“Invalid type, attribute 'conn' must be of type 'ldap3.Connection'”).
- Set fetch\_ldap\_groups from no value.
- Set ldap\_object\_class from no value.
- Set ldap\_group\_members\_attribute from no value.
- If self.ldap\_directory\_server.lower() equals “active directory”.
  - Set ldap\_object\_class from “Group”.
  - Set ldap\_group\_members\_attribute from “member”.
  - Set user\_search\_str from escape\_filter\_chars(user.entry\_dn).
- Otherwise.
  - If self.ldap\_directory\_server.lower() equals “openldap”.
    - Set ldap\_object\_class from “posixgroup”.
    - Set ldap\_group\_members\_attribute from “memberuid”.
    - Set user\_search\_str from escape\_filter\_chars(getattr(user, self.ldap\_username\_field).value).
  - Otherwise.
    - If self.ldap\_directory\_server.lower() equals “custom”.
      - Set ldap\_object\_class from self.ldap\_group\_objectclass.
      - Set ldap\_group\_members\_attribute from self.ldap\_group\_member\_attribute.
      - Set ldap\_custom\_group\_search from (self.ldap\_custom\_group\_search or “{0}”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.ldap\_custom\_group\_search → “{0}”.
      - Set user\_value from escape\_filter\_chars(getattr(user, self.ldap\_username\_field).value).
      - Set user\_search\_str from ldap\_custom\_group\_search.format(user\_value).
    - Otherwise.
      - If self.ldap\_group\_field.
        - Set fetch\_ldap\_groups from getattr(user, self.ldap\_group\_field).values.
- If ldap\_object\_class is distinct from no value.
  - Evaluate conn.search(search\_base = self.ldap\_search\_path\_group, search\_filter = formatted text (&amp;(objectClass={ldap\_object\_class})({ldap\_group\_members\_attribute}={user\_search\_str})), attributes = list(“cn”)).
- If len(conn.entries) ≥ 1.
  - Set fetch\_ldap\_groups from list of group at “cn”.value for group drawn from conn.entries.
    - Draw group from conn.entries.
- Return fetch\_ldap\_groups.

**Values supplied outside this operation** selected callable from getattr(user, self.ldap\_username\_field), getattr(user, self.ldap\_group\_field).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L3603) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L39) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L765)

<a id="op-475102d3ea3eb7"></a>
### LDAPSettings.authenticate

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_authenticate`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, username, password.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** LDAPInvalidCredentialsResult.

**Observed service boundaries** validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L4478) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L35) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L761)

<a id="op-0975116fcae5e2"></a>
### LDAPSettings.reset password

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_reset_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, user, password, logout\_sessions.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L5175) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L42) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L768)

<a id="op-ce0dda653a4b2b"></a>
### LDAPSettings.convert ldap entry to dict

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_lightweight_directory_access_protocol_settings_convert_lightweight_directory_access_protocol_entry_to_mapping`

**Inputs** self, user\_entry.

**Record and data access** read “User” via exists.

**Explicit results** data.

**Local steps**

- Set email from user\_entry at self.ldap\_email\_field.value.
- If isinstance(email, list).
  - For each e in email.
    - If Platform.db.exists(“User”, e).
      - Set email from e.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - After normal loop exhaustion.
    - Set email from email at 0.
- Set data from mapping(“username” → user\_entry at self.ldap\_username\_field.value, “email” → email, “first\_name” → user\_entry at self.ldap\_first\_name\_field.value).
- If self.ldap\_middle\_name\_field.
  - Set data at “middle\_name” from user\_entry at self.ldap\_middle\_name\_field.value.
- If self.ldap\_last\_name\_field.
  - Set data at “last\_name” from user\_entry at self.ldap\_last\_name\_field.value.
- If self.ldap\_phone\_field.
  - Set data at “phone” from user\_entry at self.ldap\_phone\_field.value.
- If self.ldap\_mobile\_field.
  - Set data at “mobile\_no” from user\_entry at self.ldap\_mobile\_field.value.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L5889) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L37) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L763)

<a id="op-bef0ae9d3421f7"></a>
### Login

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false.

**Observed service boundaries** record lookup, transaction control.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0251.json#L6414) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L46) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L772)

<a id="op-7482052cec5204"></a>
### Reset password

`operation_foundation_integrations_record_definitions_ldap_settings_business_behavior_reset_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, password, logout.

**Observed service boundaries** effective access lookup, record lookup, validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0252.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L47) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L773)

## Service · Mcp

<a id="op-4ad3f0e87f60c5"></a>
### Handle

`operation_foundation_binding_foundation_mcp_init_handle`

**Inputs** no declared parameters.

**Explicit results** handle\_request(Platform.request).

**Explicit failure paths** NotFound.

**Local steps**

- If not Platform.get\_system\_settings(“enable\_mcp”).
  - Raise NotFound.
- Bind dependencies handle\_request.
- Return handle\_request(Platform.request).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_mcp”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1502)

## Service · Methods

<a id="op-99d4d7c877c93e"></a>
### Call method

`operation_foundation_binding_foundation_mcp_tools_methods_call_method`

**Inputs** method, args.

**Declared result** dict.

**Explicit results** mapping(“result” → result).

**Local steps**

- Within form\_dict(args), request\_method(rpc\_function(method)).
  - Set result from v2.handle\_rpc\_call(method).
  - If result is identical to no value.
    - Set result from Platform.response.get(“message”, Platform.response.get(“data”)).
  - Return mapping(“result” → result).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L110) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1542)

<a id="op-c6d354feb64b29"></a>
### Call document method

`operation_foundation_binding_foundation_mcp_tools_methods_call_document_method`

**Inputs** doctype, name, method, args.

**Declared result** dict.

**Explicit results** mapping(“result” → result, “document” → Platform.response.docs at negative 1).

**Local steps**

- Within form\_dict(args), request\_method(document\_function(doctype, method)).
  - Set result from v2.execute\_doc\_method(doctype, name, method).
  - Return mapping(“result” → result, “document” → Platform.response.docs at negative 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1541)

<a id="op-3b2b32f1a23cd2"></a>
### Request method

`operation_foundation_binding_foundation_mcp_tools_methods_request_method`

**Inputs** fn.

**Wrappers, in declaration order** contextmanager.

**Declared result** Iterator at no value.

**State and service calls** rollback.

**Explicit results** no value.

**Local steps**

- Set allowed from Platform.allowed\_http\_methods\_for\_whitelisted\_func.get(fn, tuple()).
- If (“GET” does not belong to allowed or “POST” belongs to allowed).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “GET” does not belong to allowed → “POST” belongs to allowed.
  - yield no value.
  - Return no value.
- Set request from Platform.local.request.
- Set request.method from “GET”.
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Set request.method from “POST”.
- If not Platform.local.flags.commit.
  - Evaluate Platform.db.rollback().

On ordinary fall-through the sequence ends.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L112) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1544)

<a id="op-a5d6c1ad563be5"></a>
### Rpc function

`operation_foundation_binding_foundation_mcp_tools_methods_rpc_function`

**Inputs** method.

**Declared result** (Callable bitwise or no value).

**Explicit results** no value · Platform.get\_attr(method).

**Local steps**

- Set method from Platform.override\_whitelisted\_method(method).
- If method belongs to v2.get\_server\_script\_map().get(“\_api”, mapping()).
  - Return no value.
- Attempt the following.
  - Return Platform.get\_attr(method).
- On failure (Exception).
  - Return no value.

**Values supplied outside this operation** selected callable from Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L113) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1545)

<a id="op-ca7aaadaf24167"></a>
### Document function

`operation_foundation_binding_foundation_mcp_tools_methods_document_function`

**Inputs** doctype, method.

**Declared result** (Callable bitwise or no value).

**Explicit results** getattr(get\_controller(doctype), method, no value).

**Local steps**

- Return getattr(get\_controller(doctype), method, no value).

**Values supplied outside this operation** selected callable from getattr(get\_controller(doctype), method, no value), get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L111) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1543)
