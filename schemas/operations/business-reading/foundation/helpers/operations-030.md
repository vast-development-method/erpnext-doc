# Shared value and file services · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Nestedset

<a id="op-5a8d9ef2b8bf7f"></a>
### Nested Set.get ancestors

`operation_foundation_utils_nestedset_business_behavior_nested_set_get_ancestors`

**Inputs** self.

**Explicit results** get\_ancestors\_of(self.doctype, self.name).

**Local steps**

- Return get\_ancestors\_of(self.doctype, self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L1630) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L370)

<a id="op-da1f03d143aa27"></a>
### Nested Set.get parent

`operation_foundation_utils_nestedset_business_behavior_nested_set_get_parent`

**Inputs** self.

**Declared result** “NestedSet”.

**Record and data access** resolve a document from self.doctype via get\_doc.

**Explicit results** Platform.get\_doc(self.doctype, parent\_name).

**Local steps**

- Set parent\_name from self.get(self.nsm\_parent\_field).
- If parent\_name.
  - Return Platform.get\_doc(self.doctype, parent\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L1696) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L372)

<a id="op-e3e1fc11639b44"></a>
### Nested Set.get children

`operation_foundation_utils_nestedset_business_behavior_nested_set_get_children`

**Inputs** self.

**Declared result** Iterator at “NestedSet”.

**Record and data access** read self.doctype via get\_list · resolve a document from self.doctype via get\_doc.

**Local steps**

- Set child\_names from Platform.get\_list(self.doctype, filters = mapping(self.nsm\_parent\_field → self.name), pluck = “name”).
- For each name in child\_names.
  - yield Platform.get\_doc(self.doctype, name).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L1808) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L371)

<a id="op-29601305c7d7ae"></a>
### Get root of

`operation_foundation_utils_nestedset_business_behavior_get_root_of`

**Inputs** doctype.

**Explicit results** result at 0 at 0 when result, otherwise no value.

**Local steps**

- Bind dependencies Count.
- Set Table from DocType(doctype).
- Set t1 from Table.as\_(“t1”).
- Set t2 from Table.as\_(“t2”).
- Set node\_query from SubQuery(nested operand in the contract.from\_(t2).select(Count(“\*”)).where((t2.lft &lt; t1.lft bitwise and t2.rgt &gt; t1.rgt))).
- Set result from nested operand in the contract(nested operand in the contract).select(t1.name).where((node\_query equals 0 bitwise and t1.rgt &gt; t1.lft)).run().
- Return result at 0 at 0 when result, otherwise no value.
  - Value choice on result — true gives result at 0 at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L1987) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L366)

<a id="op-2ef41e7f41ab98"></a>
### Get ancestors of

`operation_foundation_utils_nestedset_business_behavior_get_ancestors_of`

**Inputs** doctype, name, order\_by = “lft desc”, limit = no value.

**Record and data access** read doctype via get\_value · read doctype via get\_all.

**Explicit results** Platform.get\_all(doctype, mapping(“lft” → list(“&lt;”, lft), “rgt” → list(“&gt;”, rgt)), “name”, order\_by = order\_by, limit\_page\_length = limit, pluck = “name”).

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_value(doctype, name, list(“lft”, “rgt”)).
- Return Platform.get\_all(doctype, mapping(“lft” → list(“&lt;”, lft), “rgt” → list(“&gt;”, rgt)), “name”, order\_by = order\_by, limit\_page\_length = limit, pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L2412) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L364)

<a id="op-8c02317a75a9e8"></a>
### Get descendants of

`operation_foundation_utils_nestedset_business_behavior_get_descendants_of`

**Inputs** doctype, name, order\_by = “lft desc”, limit = no value, ignore\_permissions = false.

**Record and data access** read doctype via get\_value · read doctype via get\_list.

**Explicit results** list() · Platform.get\_list(doctype, mapping(“lft” → list(“&gt;”, lft), “rgt” → list(“&lt;”, rgt)), “name”, order\_by = order\_by, limit\_page\_length = limit, ignore\_permissions = ignore\_permissions, pluck = “name”).

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_value(doctype, name, list(“lft”, “rgt”)).
- If (rgt − lft) ≤ 1.
  - Return list().
- Return Platform.get\_list(doctype, mapping(“lft” → list(“&gt;”, lft), “rgt” → list(“&lt;”, rgt)), “name”, order\_by = order\_by, limit\_page\_length = limit, ignore\_permissions = ignore\_permissions, pluck = “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L2663) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L365)

## Service · New navigation nudge

<a id="op-4719b4976f1a4f"></a>
### Should show new navigation prompt

`operation_foundation_utils_new_navigation_nudge_business_behavior_should_show_new_navigation_prompt`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · bool((set(INVITED\_ROLES) bitwise and set(Platform.get\_roles()))).

**Local steps**

- If not is\_desktop\_icons\_page().
  - Return false.
- If cint(Platform.defaults.get\_global\_default(SKIP\_NEW\_NAVIGATION\_PROMPT)).
  - Return false.
- Return bool((set(INVITED\_ROLES) bitwise and set(Platform.get\_roles()))).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L2971) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1602) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L388)

<a id="op-04bd94fc268a77"></a>
### Submit new navigation prompt

`operation_foundation_utils_new_navigation_nudge_business_behavior_submit_new_navigation_prompt`

**Inputs** action.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**Record and data access** read DesktopSettings.\_DOCTYPE\_NAME via get\_single.

**State and service calls** call save on settings.

**Explicit results** “kept” · “switched”.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted” · validation helper — translated “Invalid action”.

**Local steps**

- If not (set(INVITED\_ROLES) bitwise and set(Platform.get\_roles())).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- If action equals Action.KEEP\_ICON\_GRID.value.
  - Evaluate skip\_new\_navigation\_prompt().
  - Return “kept”.
- If action equals Action.TRY\_NEW\_NAVIGATION.value.
  - Set settings from Platform.get\_single(DesktopSettings.\_DOCTYPE\_NAME).
  - Set settings.desktop\_page from APPS.
  - Evaluate settings.save(ignore\_permissions = true).
  - Evaluate skip\_new\_navigation\_prompt().
  - Evaluate capture(“switched\_to\_apps\_navigation”, app = “Platform”).
  - Return “switched”.
- Call the validation error handler Platform.throw(translated “Invalid action”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L4) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1604) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L390)

<a id="op-380092f7a1ba1c"></a>
### Skip new navigation prompt

`operation_foundation_utils_new_navigation_nudge_business_behavior_skip_new_navigation_prompt`

**Inputs** no declared parameters.

**Declared result** no value.

**Local steps**

- Evaluate Platform.defaults.set\_global\_default(SKIP\_NEW\_NAVIGATION\_PROMPT, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L3541) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1603) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L389)

## Service · Number format

<a id="op-91f0913b4b3cb7"></a>
### Number Format.from string

`operation_foundation_utils_number_format_business_behavior_number_format_from_string`

**Inputs** cls, number\_format.

**Wrappers, in declaration order** classmethod.

**Declared result** “NumberFormat”.

**Explicit results** NumberFormat(precision = precision, decimal\_separator = decimal\_separator, thousands\_separator = thousands\_separator, string = number\_format).

**Local steps**

- Set tuple(decimal\_separator, thousands\_separator, precision) from NUMBER\_FORMAT\_MAP at number\_format.
- Return NumberFormat(precision = precision, decimal\_separator = decimal\_separator, thousands\_separator = thousands\_separator, string = number\_format).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L3597) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1605) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L391)

<a id="op-9a21e9683a044e"></a>
### Number Format.str

`operation_foundation_utils_number_format_business_behavior_number_format_text`

**Inputs** self.

**Declared result** str.

**Explicit results** self.string.

**Local steps**

- Return self.string.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L3734) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L392)

## Service · Oauth

<a id="op-54d88c6980cf36"></a>
### Build oauth url

`operation_foundation_utils_delegated_authorization_business_behavior_build_delegated_authorization_resource_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** base\_url, url.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L4278) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1274) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L73)

<a id="op-a67910bab1d65a"></a>
### Get oauth2 providers

`operation_foundation_utils_delegated_authorization_business_behavior_get_delegated_authorization_2_providers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L4446) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L78)

<a id="op-76f901718e200f"></a>
### Get oauth keys

`operation_foundation_utils_delegated_authorization_business_behavior_get_delegated_authorization_keys`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider.

**Explicit result forms** a structured result.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L5055) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L79)

<a id="op-f537bfe1772f5c"></a>
### Create oauth state

`operation_foundation_utils_delegated_authorization_business_behavior_create_delegated_authorization_state`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** redirect\_to.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L5336) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1276) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L75)

<a id="op-ff6408df446d4e"></a>
### Consume oauth state

`operation_foundation_utils_delegated_authorization_business_behavior_consume_delegated_authorization_state`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** state.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L5501) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1275) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L74)

<a id="op-393a83a0bbc765"></a>
### Get oauth2 authorize url

`operation_foundation_utils_delegated_authorization_business_behavior_get_delegated_authorization_2_authorize_resource_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider, redirect\_to.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L5674) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1278) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L76)

<a id="op-d4fcfbbdc76677"></a>
### Get oauth2 flow

`operation_foundation_utils_delegated_authorization_business_behavior_get_delegated_authorization_2_flow`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L5943) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1279) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L77)

<a id="op-6c1bb6fe7b532e"></a>
### Get redirect uri

`operation_foundation_utils_delegated_authorization_business_behavior_get_redirect_resource_identifier`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L6099) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L84)

<a id="op-3008e6ee30d6e5"></a>
### Login via oauth2

`operation_foundation_utils_delegated_authorization_business_behavior_login_via_delegated_authorization_2`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider, code, state, decoder.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L6328) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1291) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L87)

<a id="op-f0e79938da6988"></a>
### Login via oauth2 id token

`operation_foundation_utils_delegated_authorization_business_behavior_login_via_delegated_authorization_2_identifier_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider, code, state, decoder.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0488.json#L6488) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1292) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L88)

<a id="op-23a594f97dc5f2"></a>
### Get info via oauth

`operation_foundation_utils_delegated_authorization_business_behavior_get_info_via_delegated_authorization`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** provider, code, decoder, id\_token.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 5 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L103) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L82)

<a id="op-f38d7e72dc4f0c"></a>
### Login oauth user

`operation_foundation_utils_delegated_authorization_business_behavior_login_delegated_authorization_user`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** data, provider, state, generate\_login\_token.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** record mutation request, transaction control.

**Local structure** 5 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L104) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1290) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L86)

<a id="op-986ca289e63fa7"></a>
### Get user record

`operation_foundation_utils_delegated_authorization_business_behavior_get_user_record`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** user, data, provider.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Locally raised failures** SignupDisabledError.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0489.json#L2205) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L85)
