# Forms, reports and navigation · operations 55

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Search

<a id="op-c5142ce68363f4"></a>
### Relevance sorter

`operation_foundation_desk_search_business_behavior_relevance_sorter`

**Inputs** key, query, as\_dict.

**Explicit results** tuple(nested operand in the contract(nested operand in the contract).casefold().startswith(query.casefold()) is distinct from true, value).

**Local steps**

- Set value from translated key.name when as\_dict, otherwise key at 0.
  - Value choice on as\_dict — true gives key.name, false gives key at 0.
- Return tuple(nested operand in the contract(nested operand in the contract).casefold().startswith(query.casefold()) is distinct from true, value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0215.json#L7500) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L981) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1421)

<a id="op-a8422dcdf03d72"></a>
### Filter translated

`operation_foundation_desk_search_business_behavior_filter_translated`

**Inputs** values, txt, as\_dict.

**Declared result** list.

**Explicit results** list of result for result drawn from values where any(generator of re.search(formatted text {nested operand in the contract.escape(txt)}.\*, (translated nested operand in the contract(nested operand in the  ….

**Local steps**

- Return list of result for result drawn from values where any(generator of re.search(formatted text {nested operand in the contract.escape(txt)}.\*, (translated nested operand in the contract(nested operand in the  ….
  - Draw result from values, keep a combination only if (any(generator of re.search(formatted text {re.escape(txt)}.\*, (translated cstr(value) or empty text), re.IGNORECASE) for value drawn from result.values() when as\_dict, otherwise result)).
  - Draw value from result.values() when as\_dict, otherwise result.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in translated cstr(value) → empty text.
  - Value choice on as\_dict — true gives result.values(), false gives result.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1413)

<a id="op-2a0e87c3860f5c"></a>
### Get names for mentions

`operation_foundation_desk_search_business_behavior_get_names_for_mentions`

**Inputs** search\_term, page\_length = 10.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list() · sorted(filtered\_mentions, key = deferred anonymous expression) at slice no value to page\_length.

**Local steps**

- If (not search\_term or not search\_term.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not search\_term → not search\_term.strip().
  - Return list().
- Set page\_length from min(max(cint(page\_length), 1), MAX\_MENTIONS\_PAGE\_LENGTH).
- Set users\_for\_mentions from Platform.cache.get\_value(“users\_for\_mentions”, get\_users\_for\_mentions).
- Set user\_groups from Platform.cache.get\_value(“user\_groups”, get\_user\_groups).
- Set filtered\_mentions from list().
- For each mention\_data in (users\_for\_mentions + user\_groups).
  - If search\_term.lower() does not belong to mention\_data.value.lower().
    - Continue with the next iteration or loop test.
  - Set mention\_data at “link” from Platform.utils.get\_url\_to\_form(“User Group” when mention\_data.get(“is\_group”), otherwise “User”, mention\_data at “id”).
    - Value choice on mention\_data.get(“is\_group”) — true gives “User Group”, false gives “User”.
  - Evaluate filtered\_mentions.append(mention\_data).
- Return sorted(filtered\_mentions, key = deferred anonymous expression) at slice no value to page\_length.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L244) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L975) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1415)

<a id="op-d28a018b7484fe"></a>
### Get users for mentions

`operation_foundation_desk_search_business_behavior_get_users_for_mentions`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_all.

**Explicit results** Platform.get\_all(“User”, fields = list(“name as id”, “full\_name as value”, “email”), filters = mapping(“name” → list(“not in”, tuple(“Administrator”, “Guest”)), “allowed\_in\_mentions” → true, “user\_type” →  ….

**Local steps**

- Return Platform.get\_all(“User”, fields = list(“name as id”, “full\_name as value”, “email”), filters = mapping(“name” → list(“not in”, tuple(“Administrator”, “Guest”)), “allowed\_in\_mentions” → true, “user\_type” →  ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L777) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L978) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1418)

<a id="op-ece50617ffd5c7"></a>
### Get user groups

`operation_foundation_desk_search_business_behavior_get_user_groups`

**Inputs** no declared parameters.

**Record and data access** read “User Group” via get\_all.

**Explicit results** Platform.get\_all(“User Group”, fields = list(“name as id”, “name as value”), update = mapping(“is\_group” → true)).

**Local steps**

- Return Platform.get\_all(“User Group”, fields = list(“name as id”, “name as value”), update = mapping(“is\_group” → true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L950) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L977) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1417)

<a id="op-edce8f8126b332"></a>
### Awesomebar search

`operation_foundation_desk_search_business_behavior_awesomebar_search`

**Inputs** txt.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list() · results.

**Local steps**

- Set txt from cstr(txt).strip().
- If not txt.
  - Return list().
- Set results from list().
- For each method in Platform.get\_hooks(“awesomebar\_search”).
  - Attempt the following.
    - Set items from (Platform.get\_attr(method)(txt) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(method)(txt) → list().
  - On failure (Exception).
    - Evaluate Platform.logger(“awesomebar”).error(formatted text awesomebar\_search hook failed: {method}, exc\_info = true).
    - Continue with the next iteration or loop test.
  - If not isinstance(items, (list bitwise or tuple)).
    - Continue with the next iteration or loop test.
  - For each item in items at slice no value to 20.
    - If normalized bound to \_normalize\_awesomebar\_result(item).
      - Evaluate results.append(normalized).
- Return results.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“awesomebar\_search”), Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L1048) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1410)

<a id="op-e3e4195cb3e432"></a>
### Normalize awesomebar result

`operation_foundation_desk_search_business_behavior_normalize_awesomebar_result`

**Inputs** item.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · result.

**Local steps**

- If not isinstance(item, dict).
  - Return no value.
- Set label from cstr((item.get(“label”) or item.get(“value”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“label”) → item.get(“value”).
- If not label.
  - Return no value.
- Set route from item.get(“route”).
- If isinstance(route, str).
  - Set route from list(route).
- Otherwise.
  - If route.
    - Set route from list of cstr(part) for part drawn from route.
      - Draw part from route.
  - Otherwise.
    - Return no value.
- If (not route or route at 0.startswith(“//”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not route → route at 0.startswith(“//”).
  - Return no value.
- If (“:” belongs to route at 0 and not route at 0.startswith(tuple(text in the contract, text in the contract))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “:” belongs to route at 0 → not route at 0.startswith(tuple(text in the contract, text in the contract)).
  - Return no value.
- Set result from mapping(“label” → label, “value” → cstr((item.get(“value”) or label)), “index” → cint(item.get(“index”)), “route” → route).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“value”) → label.
- If description bound to item.get(“description”).
  - Set result at “description” from cstr(description).
- If result\_type bound to item.get(“type”).
  - Set result at “type” from cstr(result\_type).
- If (route\_options bound to item.get(“route\_options”) and isinstance(route\_options, dict)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in route\_options bound to item.get(“route\_options”) → isinstance(route\_options, dict).
  - Set result at “route\_options” from route\_options.
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L1494) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L980) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1420)

<a id="op-6db3b2ffab3043"></a>
### Get link title

`operation_foundation_desk_search_business_behavior_get_link_title`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.get(meta.title\_field) · docname.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If meta.show\_title\_field\_in\_link.
  - Attempt the following.
    - Set doc from Platform.get\_lazy\_doc(doctype, docname).
    - Set is\_title\_permitted from meta.title\_field belongs to get\_permitted\_fields(doctype).
    - If (is\_title\_permitted and has\_permission(doctype, “select”, doc, print\_logs = false)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_title\_permitted → has\_permission(doctype, “select”, doc, print\_logs = false).
      - Return doc.get(meta.title\_field).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
- Return docname.

**Values supplied outside this operation** effective access from has\_permission(doctype, “select”, doc, print\_logs = false).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L66) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L974) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1414)

<a id="op-11a47671be197d"></a>
### Web search

`operation_foundation_search_initialize_business_behavior_web_search`

**Inputs** query, scope = no value, limit = 20.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Explicit results** ws.search(query, scope, limit).

**Local steps**

- Bind dependencies WebsiteSearch.
- Set limit from cint(limit).
- Set ws from WebsiteSearch(index\_name = “web\_routes”).
- Return ws.search(query, scope, limit).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L2457) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L450)

## Service · Selectors

<a id="op-8fdacaa4d71602"></a>
### Child blocks

`operation_foundation_binding_foundation_studio_ai_agent_selectors_child_blocks`

**Inputs** block.

**Declared result** Iterator at dict.

**Local steps**

- For each child in (block.get(“children”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“children”) → list().
  - If isinstance(child, dict).
    - yield child.
- For each slot in (block.get(“componentSlots”) or mapping()).values().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentSlots”) → mapping().
  - Set content from slot.get(“slotContent”) when isinstance(slot, dict), otherwise no value.
    - Value choice on isinstance(slot, dict) — true gives slot.get(“slotContent”), false gives no value.
  - If isinstance(content, list).
    - For each child in content.
      - If isinstance(child, dict).
        - yield child.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1753)

<a id="op-c3125e78137e52"></a>
### Walk blocks

`operation_foundation_binding_foundation_studio_ai_agent_selectors_walk_blocks`

**Inputs** root, depth = 0.

**Declared result** Iterator at tuple at tuple(dict, int).

**Explicit results** no value.

**Local steps**

- If not isinstance(root, dict).
  - Return no value.
- yield tuple(root, depth).
- For each child in child\_blocks(root).
  - yield values from walk\_blocks(child, (depth + 1)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1757)

<a id="op-8e9e0b577a235a"></a>
### Find block

`operation_foundation_binding_foundation_studio_ai_agent_selectors_find_block`

**Inputs** root, component\_id.

**Declared result** (dict bitwise or no value).

**Explicit results** block · no value.

**Local steps**

- For each tuple(block, \_depth) in walk\_blocks(root).
  - If block.get(“componentId”) equals component\_id.
    - Return block.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1754)

<a id="op-b79a928f2e9535"></a>
### Block text

`operation_foundation_binding_foundation_studio_ai_agent_selectors_block_text`

**Inputs** block.

**Declared result** str.

**Explicit results** value.strip() · empty text.

**Local steps**

- Set props from (block.get(“componentProps”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentProps”) → mapping().
- For each key in TEXT\_PROP\_KEYS.
  - Set value from props.get(key).
  - If (isinstance(value, str) and value.strip()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → value.strip().
    - Return value.strip().
- Return empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1752)

<a id="op-a6f32823a7a83f"></a>
### Is text block

`operation_foundation_binding_foundation_studio_ai_agent_selectors_is_text_block`

**Inputs** block.

**Declared result** bool.

**Explicit results** bool(block\_text(block)).

**Local steps**

- Return bool(block\_text(block)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1755)

<a id="op-656db5e68a9042"></a>
### Match block

`operation_foundation_binding_foundation_studio_ai_agent_selectors_match_block`

**Inputs** block, component (named only, default no value), text\_only (named only, default false), contains (named only, default no value).

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If (component and (nested operand in the contract.get(“componentName”) or empty text).lower() differs from component.lower()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in component → (block.get(“componentName”) or empty text).lower() differs from component.lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentName”) → empty text.
  - Return false.
- If (text\_only and not is\_text\_block(block)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in text\_only → not is\_text\_block(block).
  - Return false.
- If (contains and contains.lower() does not belong to block\_text(block).lower()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in contains → contains.lower() does not belong to block\_text(block).lower().
  - Return false.
- Return true.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1756)

## Service · Session

<a id="op-347af42b9d936c"></a>
### AISession.initialize

`operation_foundation_binding_foundation_studio_ai_session_aisession_init`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, doc.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1856)

<a id="op-96d822213f145d"></a>
### AISession.get or create

`operation_foundation_binding_foundation_studio_ai_session_aisession_get_or_create`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, page\_id, model, user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1855)

<a id="op-803b01ccfdd5bf"></a>
### AISession.get

`operation_foundation_binding_foundation_studio_ai_session_aisession_get`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, session\_id, page\_id, user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L190) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1853)

<a id="op-f9aef6064cfe37"></a>
### AISession.try append message

`operation_foundation_binding_foundation_studio_ai_session_aisession_try_append_message`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, session\_id, role, content, kwargs.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L202) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1865)

<a id="op-172fe4e07ad552"></a>
### AISession.build context messages from id

`operation_foundation_binding_foundation_studio_ai_session_aisession_build_context_messages_from_id`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cls, session\_id.

**Explicit result forms** a structured result, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L187) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1874) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1850)

<a id="op-e46132627ce327"></a>
### AISession.name

`operation_foundation_binding_foundation_studio_ai_session_aisession_name`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L196) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1859)

<a id="op-713cb997f87f97"></a>
### AISession.page

`operation_foundation_binding_foundation_studio_ai_session_aisession_page`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L197) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1860)

<a id="op-af0e2507453b67"></a>
### AISession.selected model

`operation_foundation_binding_foundation_studio_ai_session_aisession_selected_model`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L200) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1863)

<a id="op-d79f56aa0336c7"></a>
### AISession.last task type

`operation_foundation_binding_foundation_studio_ai_session_aisession_last_task_type`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L195) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1858)
