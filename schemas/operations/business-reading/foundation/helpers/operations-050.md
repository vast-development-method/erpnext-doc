# Shared value and file services · operations 50

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Telemetry

<a id="op-1d6ccaf84b4935"></a>
### Capture

`operation_foundation_utils_telemetry_initialize_business_behavior_capture`

**Inputs** event, app, remaining named values kwargs.

**Local steps**

- If is\_pulse\_enabled().
  - Evaluate pulse\_capture(event, app = app, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L6059) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L723)

<a id="op-e155ba68f956de"></a>
### Capture doc

`operation_foundation_utils_telemetry_initialize_business_behavior_capture_record`

**Inputs** doc, action.

**Explicit results** no value.

**Local steps**

- Within suppress(Exception).
  - Set age from site\_age().
  - If (not age or age &gt; 15).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not age → age &gt; 15.
    - Return no value.
  - Set app from Platform.local.module\_app.get(Platform.scrub(doc.meta.module), “Platform”).
  - If (doc.get(“\_\_islocal”) or not doc.get(“name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“\_\_islocal”) → not doc.get(“name”).
    - Evaluate capture(“document\_created”, app, properties = mapping(“doctype” → doc.doctype, “action” → “Insert”)).
  - Otherwise.
    - Evaluate capture(“document\_modified”, app, properties = mapping(“doctype” → doc.doctype, “action” → action)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L79) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L724)

<a id="op-a951ef3d11d1ba"></a>
### Site age

`operation_foundation_utils_telemetry_initialize_business_behavior_site_age`

**Inputs** no declared parameters.

**Wrappers, in declaration order** site\_cache(ttl = ((60 × 60) × 12)).

**Record and data access** read “User” via get\_value.

**Explicit results** ((getdate() − getdate(est\_creation)).days + 1).

**Local steps**

- Attempt the following.
  - Set est\_creation from Platform.db.get\_value(“User”, “Administrator”, “creation”).
  - Return ((getdate() − getdate(est\_creation)).days + 1).
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L6497) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L725)

## Service · Testutils

<a id="op-ea111a47a0a7d4"></a>
### Add custom field

`operation_foundation_utils_testutils_business_behavior_add_custom_field`

**Inputs** doctype, fieldname, fieldtype = “Data”, options = no value.

**Record and data access** resolve a document from mapping(“doctype” → “Custom Field”, “dt” → doctype, “fieldname” → fieldname, “fieldtype” → fieldtype, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → doctype, “fieldname” → fieldname, “fieldtype” → fieldtype, …)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → doctype, “fieldname” → fieldname, “fieldtype” → fieldtype, …)).insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L290) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L17) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L968)

<a id="op-f4165ea65f317b"></a>
### Clear custom fields

`operation_foundation_utils_testutils_business_behavior_clear_custom_fields`

**Inputs** doctype.

**State and service calls** request delete on “Custom Field”.

**Local steps**

- Evaluate Platform.db.delete(“Custom Field”, mapping(“dt” → doctype)).
- Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L469) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L18) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L969)

## Service · Translations

<a id="op-c9637620626f60"></a>
### Unnamed value

`operation_foundation_utils_translations_business_behavior_unnamed`

**Inputs** msg, lang = no value, context = no value.

**Declared result** str.

**Explicit results** translated\_string · non\_translated\_string.

**Local steps**

- Bind dependencies get\_all\_translations.
- If not hasattr(Platform.local, “lang”).
  - Set Platform.local.lang from (lang or “en”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in lang → “en”.
- If not lang.
  - Set job from getattr(Platform.local, “job”, no value).
  - If (job is distinct from no value and not job.lang\_resolved).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in job is distinct from no value → not job.lang\_resolved.
    - Evaluate set\_user\_lang(job.user).
    - Set job.lang\_resolved from true.
  - Set lang from Platform.local.lang.
- Set all\_translations from get\_all\_translations(lang).
- Set non\_translated\_string from msg.
- Set msg from Platform.as\_unicode(msg).strip().
- Set msg\_with\_html from Platform.as\_unicode(non\_translated\_string).strip().
- Set msg\_list from list(msg, msg\_with\_html).
- For each msg in msg\_list.
  - Set translated\_string from empty text.
  - If context.
    - Set string\_key from formatted text {msg}:{context}.
    - Set translated\_string from all\_translations.get(string\_key).
  - If not translated\_string.
    - Set translated\_string from all\_translations.get(msg).
  - If translated\_string.
    - Return translated\_string.
- Return non\_translated\_string.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “job”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L581) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L22) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L973)

<a id="op-b739139750c123"></a>
### N

`operation_foundation_utils_translations_business_behavior_n`

**Inputs** msg, context = no value.

**Declared result** str.

**Explicit results** msg.

**Local steps**

- Return msg.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L1208) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L20) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L971)

<a id="op-d312df3a9b4e30"></a>
### Lt

`operation_foundation_utils_translations_business_behavior_lt`

**Inputs** msg, lang = no value, context = no value.

**Explicit results** \_LazyTranslate(msg, lang, context).

**Local steps**

- Bind dependencies \_LazyTranslate.
- Return \_LazyTranslate(msg, lang, context).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L1275) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L19) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L970)

<a id="op-3d7ad9f4d37227"></a>
### Set user lang

`operation_foundation_utils_translations_business_behavior_set_user_language`

**Inputs** user, user\_language = no value.

**Declared result** no value.

**Local steps**

- Bind dependencies get\_user\_lang.
- Set Platform.local.lang from (get\_user\_lang(user) or user\_language).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_user\_lang(user) → user\_language.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L1394) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L21) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L972)

## Service · Transport

<a id="op-d6886cd26168be"></a>
### Pulse HTTP.initialize

`operation_foundation_utils_telemetry_pulse_transport_business_behavior_pulse_hypertext_transfer_protocol_initialize`

**Inputs** self.

**Local steps**

- Set self.api\_key from Platform.conf.get(“pulse\_api\_key”).
- Set self.host from pulse\_host().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L366) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2024) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L790)

<a id="op-f3e9366e1dfe6d"></a>
### Pulse HTTP.session

`operation_foundation_utils_telemetry_pulse_transport_business_behavior_pulse_hypertext_transfer_protocol_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L463) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2027) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L793)

<a id="op-2f318999ff9d48"></a>
### Pulse HTTP.url

`operation_foundation_utils_telemetry_pulse_transport_business_behavior_pulse_hypertext_transfer_protocol_resource_address`

**Inputs** self, endpoint.

**Declared result** str.

**Explicit results** formatted text {self.host}/{endpoint.lstrip(“/”)}.

**Local steps**

- Return formatted text {self.host}/{endpoint.lstrip(“/”)}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L580) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2026) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L792)

<a id="op-3cab84aab29fb2"></a>
### Pulse HTTP.post

`operation_foundation_utils_telemetry_pulse_transport_business_behavior_pulse_hypertext_transfer_protocol_post`

**Inputs** self, endpoint, payload, label = no value, raise\_on\_error = false.

**Explicit results** no value · resp.

**Explicit failure paths** propagate active failure · Exception(msg).

**Local steps**

- Set label from (label or endpoint).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in label → endpoint.
- Attempt the following.
  - Set resp from self.\_session().post(self.\_url(endpoint), data = Platform.as\_json(payload), timeout = 15).
- On failure (Exception) bound to e.
  - Evaluate Platform.logger(“pulse”).error(formatted text pulse-client - {label} failed: {e}).
  - If raise\_on\_error.
    - Propagate the active failure.
  - Return no value.
- If not 200 ≤ resp.status\_code &lt; 300.
  - Compare adjacent operands in order, stopping at the first false comparison in 200 ≤ resp.status\_code &lt; 300.
  - Set msg from formatted text pulse-client - {label} failed: {resp.status\_code} {resp.text}.
  - Evaluate Platform.logger(“pulse”).error(msg).
  - If raise\_on\_error.
    - Raise Exception(msg).
- Return resp.

**Methods declared on this owner** [session](operations-050.md#op-f3e9366e1dfe6d), [url](operations-050.md#op-2f318999ff9d48).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0506.json#L679) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L2025) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L791)

## Service · Typing validations

<a id="op-1c532753008b5c"></a>
### Is mock

`operation_foundation_utils_typing_validations_business_behavior_is_mock`

**Inputs** value.

**Declared result** bool.

**Explicit results** (mock is distinct from no value and isinstance(value, mock.Mock)).

**Local steps**

- Set mock from sys.modules.get(“unittest.mock”).
- Return (mock is distinct from no value and isinstance(value, mock.Mock)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in mock is distinct from no value → isinstance(value, mock.Mock).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L1506) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L23) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L974)

<a id="op-ba6adb2e93e221"></a>
### Validate argument types

`operation_foundation_utils_typing_validations_business_behavior_validate_argument_types`

**Inputs** func, apply\_condition = no value.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L87) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L28) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L979)

<a id="op-3dbad92a5f5bb9"></a>
### Validate argument types.wrapper

`operation_foundation_utils_typing_validations_business_behavior_validate_argument_types_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(func).

**Explicit results** func(expanded args, expanded names kwargs).

**Local steps**

- If (apply\_condition is identical to no value or apply\_condition()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in apply\_condition is identical to no value → apply\_condition().
  - Set tuple(args, kwargs) from transform\_parameter\_types(func, args, kwargs).
- Return func(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L88) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L29) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L980)

<a id="op-7f97f45c9d419e"></a>
### Qualified name

`operation_foundation_utils_typing_validations_business_behavior_qualified_name`

**Inputs** obj.

**Declared result** str.

**Explicit results** obj · qualname · formatted text {module}.{qualname}.

**Local steps**

- Set discovered\_type from obj when isclass(obj), otherwise type(obj).
  - Value choice on isclass(obj) — true gives obj, false gives type(obj).
- Set tuple(module, qualname) from tuple(discovered\_type.\_\_module\_\_, discovered\_type.\_\_qualname\_\_).
- If module belongs to set(“typing”, “types”).
  - Return obj.
- Otherwise.
  - If module belongs to set(“builtins”).
    - Return qualname.
  - Otherwise.
    - Return formatted text {module}.{qualname}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L2237) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L24) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L975)

<a id="op-7e0f5bccff6152"></a>
### Raise type error

`operation_foundation_utils_typing_validations_business_behavior_raise_type_error`

**Inputs** func, arg\_name, arg\_type, arg\_value, current\_exception = no value.

**Explicit failure paths** PlatformTypeError(formatted text Argument '{arg\_name}' in '{module}.{qualname}' should be of type '{qualified\_name(arg\_type)}' but got '{qualified\_name(arg\_value)}' instead.).

**Local steps**

- Set tuple(module, qualname) from tuple(func.\_\_module\_\_, func.\_\_qualname\_\_).
- Raise PlatformTypeError(formatted text Argument '{arg\_name}' in '{module}.{qualname}' should be of type '{qualified\_name(arg\_type)}' but got '{qualified\_name(arg\_value)}' instead.) with cause current\_exception.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L2465) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L25) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L976)

<a id="op-3ac4a00af11dba"></a>
### Type Adapter

`operation_foundation_utils_typing_validations_business_behavior_type_adapter`

**Inputs** type\_.

**Wrappers, in declaration order** lru\_cache(maxsize = 2048).

**Explicit results** PydanticTypeAdapter(type\_, config = PlatformPydanticConfig) · PydanticTypeAdapter(type\_).

**Explicit failure paths** e.

**Local steps**

- Bind dependencies PydanticUserError.
- Bind dependencies PydanticTypeAdapter.
- Attempt the following.
  - Return PydanticTypeAdapter(type\_, config = PlatformPydanticConfig).
- On failure (PydanticUserError) bound to e.
  - If e.code equals “type-adapter-config-unused”.
    - Return PydanticTypeAdapter(type\_).
  - Raise e.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L2732) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L27) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L978)

<a id="op-7958cad98a4a25"></a>
### Transform parameter types

`operation_foundation_utils_typing_validations_business_behavior_transform_parameter_types`

**Inputs** func, args, kwargs.

**Explicit results** tuple(args, kwargs) · tuple(new\_args, new\_kwargs).

**Local steps**

- Set annotations from func.\_\_annotations\_\_.
- If (not (args or kwargs) or not annotations or (len(annotations) equals 1 and “return” belongs to annotations)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (args or kwargs) → not annotations → (len(annotations) equals 1 and “return” belongs to annotations).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args → kwargs.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(annotations) equals 1 → “return” belongs to annotations.
  - Return tuple(args, kwargs).
- Bind dependencies PydanticValidationError.
- Set tuple(new\_args, new\_kwargs) from tuple(list(args), kwargs).
- If args.
  - Set arg\_names from func.\_\_code\_\_.co\_varnames at slice no value to func.\_\_code\_\_.co\_argcount.
  - Set prepared\_args from dict(zip(arg\_names, args, strict = false)).
  - If kwargs.
    - Evaluate prepared\_args.update(kwargs).
- Otherwise.
  - Set prepared\_args from kwargs.
- Set func\_params from Platform.\_get\_cached\_signature\_params(func) at 0.
- For each tuple(current\_arg, current\_arg\_type) in annotations.items().
  - If current\_arg does not belong to prepared\_args.
    - Continue with the next iteration or loop test.
  - Set current\_arg\_value from prepared\_args at current\_arg.
  - If isinstance(current\_arg\_type, ForwardRefOrStr).
    - Continue with the next iteration or loop test.
  - Otherwise.
    - If any(generator of isinstance(x, ForwardRefOrStr) for x drawn from getattr(current\_arg\_type, “\_\_args\_\_”, list())).
      - Draw x from getattr(current\_arg\_type, “\_\_args\_\_”, list()).
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If is\_mock(current\_arg\_value).
        - Continue with the next iteration or loop test.
  - If current\_arg\_type belongs to SLACK\_DICT.
    - Set current\_arg\_type from SLACK\_DICT at current\_arg\_type.
  - Set param\_def from func\_params.get(current\_arg).
  - If param\_def.default is distinct from \_empty.
    - If isinstance(current\_arg\_type, tuple).
      - If type(param\_def.default) does not belong to current\_arg\_type.
        - Update current\_arg\_type using + tuple(type(param\_def.default)).
      - Set current\_arg\_type from Union at current\_arg\_type.
    - Otherwise.
      - If param\_def.default differs from current\_arg\_type.
        - Set current\_arg\_type from Union at tuple(current\_arg\_type, type(param\_def.default)).
  - Otherwise.
    - If isinstance(current\_arg\_type, tuple).
      - Set current\_arg\_type from Union at current\_arg\_type.
  - Attempt the following.
    - Set current\_arg\_value\_after from TypeAdapter(current\_arg\_type).validate\_python(current\_arg\_value).
  - On failure (tuple(TypeError, PydanticValidationError)) bound to e.
    - Evaluate raise\_type\_error(func, current\_arg, current\_arg\_type, current\_arg\_value, current\_exception = e).
  - If isinstance(current\_arg\_value\_after, EllipsisType).
    - Evaluate raise\_type\_error(func, current\_arg, current\_arg\_type, current\_arg\_value).
  - If current\_arg belongs to kwargs.
    - Set new\_kwargs at current\_arg from current\_arg\_value\_after.
  - Otherwise.
    - Set new\_args at arg\_names.index(current\_arg) from current\_arg\_value\_after.
- Return tuple(new\_args, new\_kwargs).

**Values supplied outside this operation** selected callable from getattr(current\_arg\_type, “\_\_args\_\_”, list()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L86) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L26) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L977)

## Service · Typst emitter

<a id="op-1e2023dc6f23f4"></a>
### Pt

`operation_foundation_utils_typst_emitter_business_behavior_payment_term`

**Inputs** px, default = 0.0.

**Declared result** float.

**Explicit results** round(((Platform.utils.flt(px) or default) × PX\_TO\_PT), 2).

**Local steps**

- Return round(((Platform.utils.flt(px) or default) × PX\_TO\_PT), 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.utils.flt(px) → default.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L4471) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L42) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L992)

<a id="op-5efd4f8bbf534a"></a>
### Translate custom style

`operation_foundation_utils_typst_emitter_business_behavior_translate_custom_style`

**Inputs** style.

**Declared result** tuple at tuple(dict, list at str).

**Explicit results** tuple(effects, unknown).

**Local steps**

- Set tuple(effects, unknown) from tuple(mapping(), list()).
- For each declaration in (style or empty text).split(“;”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in style → empty text.
  - If “:” does not belong to declaration.
    - Continue with the next iteration or loop test.
  - Set tuple(prop, value) from generator of part.strip() for part drawn from declaration.split(“:”, 1).
    - Draw part from declaration.split(“:”, 1).
  - Set prop from prop.lower().
  - If prop does not belong to TRANSLATABLE\_STYLE\_PROPS.
    - Evaluate unknown.append(prop).
    - Continue with the next iteration or loop test.
  - If prop equals “font-weight”.
    - If value belongs to tuple(“bold”, “600”, “700”, “800”, …).
      - Set effects at “bold” from true.
    - Otherwise.
      - Evaluate unknown.append(formatted text {prop}: {value}).
  - Otherwise.
    - If prop belongs to tuple(“border-top”, “border-bottom”).
      - Set match from re.match(“(\\d+(?:\\.\\d+)?)px\\s+\\w+\\s+(#(?:&#91;0-9a-fA-F&#93;{3}){1,2}\|&#91;a-z&#93;+)$”, value).
      - Set color from (match and match.group(2)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in match → match.group(2).
      - If (match and (color.startswith(“#”) or color belongs to TYPST\_NAMED\_COLORS)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in match → (color.startswith(“#”) or color belongs to TYPST\_NAMED\_COLORS).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in color.startswith(“#”) → color belongs to TYPST\_NAMED\_COLORS.
        - Set width from pt(match.group(1)).
        - Set paint from formatted text rgb("{color}") when color.startswith(“#”), otherwise color.
          - Value choice on color.startswith(“#”) — true gives formatted text rgb("{color}"), false gives color.
        - Set effects at “stroke\_top” when prop equals “border-top”, otherwise “stroke\_bottom” from formatted text {width}pt + {paint}.
          - Value choice on prop equals “border-top” — true gives “stroke\_top”, false gives “stroke\_bottom”.
      - Otherwise.
        - Evaluate unknown.append(formatted text {prop}: {value}).
    - Otherwise.
      - If prop belongs to tuple(“margin-top”, “padding-top”, “padding-bottom”, “gap”).
        - Set match from re.match(“(\\d+(?:\\.\\d+)?)(px)?$”, value).
        - If match.
          - Set key from mapping(“margin-top” → “space\_before”, “padding-top” → “inset\_top”, “padding-bottom” → “inset\_bottom”, “gap” → “gap”) at prop.
          - Set effects at key from pt(match.group(1)).
        - Otherwise.
          - Evaluate unknown.append(formatted text {prop}: {value}).
- Return tuple(effects, unknown).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0515.json#L4576) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L47) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L997)

<a id="op-cd99f53f84768b"></a>
### Typst blockers

`operation_foundation_utils_typst_emitter_business_behavior_typst_blockers`

**Inputs** print\_format, layout.

**Declared result** list at str.

**Record and data access** read “Letter Head” via get\_value.

**Explicit results** blockers.

**Local steps**

- Set blockers from list().
- If print\_format.get(“custom\_format”).
  - Evaluate blockers.append(translated “Custom HTML format”).
  - Return blockers.
- If not print\_format.get(“print\_format\_builder\_beta”).
  - Evaluate blockers.append(translated “Not made in the Print Format Editor”).
  - Return blockers.
- If (print\_format.get(“css”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_format.get(“css”) → empty text.
  - Evaluate blockers.append(translated “Custom CSS in the Style box”).
- If not isinstance(layout, dict).
  - Return blockers.
- Set letter\_head from layout.get(“letter\_head”).
- If letter\_head.
  - Set lh from Platform.db.get\_value(“Letter Head”, letter\_head, list(“source”, “image”, “content”, “custom\_css”, …), as\_dict = true).
  - Evaluate blockers.extend(letterhead\_blockers(lh)).
- Set background from layout.get(“background”).
- If (isinstance(background, dict) and str((nested operand in the contract.get(“image”) or empty text)).startswith(tuple(text in the contract, text in the contract, “//”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(background, dict) → str((background.get(“image”) or empty text)).startswith(tuple(text in the contract, text in the contract, “//”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in background.get(“image”) → empty text.
  - Evaluate blockers.append(translated “Background image loaded from a web address”).
- Set colors from \_unsafe\_colors(print\_format).
- Set styled\_fields from list().
- Set seen from set().
- For each tuple(\_where, node) in iter\_nodes(layout).
  - Set style from node.get(“custom\_style”).
  - If (isinstance(style, str) and style.strip()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(style, str) → style.strip().
    - Set tuple(\_effects, unknown) from translate\_custom\_style(style).
    - If unknown.
      - Evaluate styled\_fields.append((node.get(“label”) or node.get(“fieldname”) or “?”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“label”) → node.get(“fieldname”) → “?”.
  - Evaluate colors.extend(generator of c for c drawn from \_unsafe\_colors(node) where c does not belong to colors).
    - Draw c from \_unsafe\_colors(node), keep a combination only if (c does not belong to colors).
  - Set fieldtype\_reason from BLOCKER\_FIELDTYPES.get(node.get(“fieldtype”)).
  - Set reason from (translated fieldtype\_reason when fieldtype\_reason, otherwise no value or \_barcode\_blocker(node, print\_format) or \_image\_blocker(node)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in translated fieldtype\_reason when fieldtype\_reason, otherwise no value → \_barcode\_blocker(node, print\_format) → \_image\_blocker(node).
    - Value choice on fieldtype\_reason — true gives translated fieldtype\_reason, false gives no value.
  - If (reason and reason does not belong to seen).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reason → reason does not belong to seen.
    - Evaluate seen.add(reason).
    - Evaluate blockers.append(reason).
- If colors.
  - Evaluate blockers.append(translated “Colours that are not hex codes: {0}”.format(“, ”.join(colors))).
- If styled\_fields.
  - Evaluate blockers.append(translated “Custom CSS on fields: {0}”.format(\_list\_names(styled\_fields))).
- Return blockers.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L97) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L48) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L998)

<a id="op-2a27cf10475bff"></a>
### List names

`operation_foundation_binding_foundation_utils_typst_emitter_list_names`

**Inputs** names.

**Explicit results** translated “{0} and {1} more”.format(shown, (len(names) − 4)) when len(names) &gt; 4, otherwise shown.

**Local steps**

- Set shown from “, ”.join(names at slice no value to 4).
- Return translated “{0} and {1} more”.format(shown, (len(names) − 4)) when len(names) &gt; 4, otherwise shown.
  - Value choice on len(names) &gt; 4 — true gives translated “{0} and {1} more”.format(shown, (len(names) − 4)), false gives shown.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L22) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L415)
