# Forms, reports and navigation · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Billing

<a id="op-48f0507442fcf6"></a>
### Get boot

`operation_foundation_public_pages_billing_business_behavior_get_boot`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(mapping(“site\_name” → Platform.local.site, “read\_only\_mode” → Platform.flags.read\_only, “csrf\_token” → Platform.sessions.get\_csrf\_token(), “setup\_complete” → Platform.is\_setup\_complete())).

**Local steps**

- Return Platform.\_dict(mapping(“site\_name” → Platform.local.site, “read\_only\_mode” → Platform.flags.read\_only, “csrf\_token” → Platform.sessions.get\_csrf\_token(), “setup\_complete” → Platform.is\_setup\_complete())).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L2722) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L27)

## Service · Block codec

<a id="op-aa5561515684db"></a>
### Block Codec.compress

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_compress`

**Inputs** block, depth = 0.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Explicit results** block · out.

**Local steps**

- If not isinstance(block, dict).
  - Return block.
- Set out from mapping().
- If cid bound to block.get(“componentId”).
  - Set out at “id” from cid.
- If name bound to block.get(“componentName”).
  - Set out at “name” from name.
- If orig bound to block.get(“originalElement”).
  - Set out at “originalElement” from orig.
- If block.get(“blockName”).
  - Set out at “label” from block at “blockName”.
- Set props from mapping of k → v for tuple(k, v) drawn from (block.get(“componentProps”) or mapping()).items() where v does not belong to tuple(no value, empty text, list(), mapping()).
  - Draw tuple(k, v) from (block.get(“componentProps”) or mapping()).items(), keep a combination only if (v does not belong to tuple(no value, empty text, list(), mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentProps”) → mapping().
- If props.
  - Set out at “props” from props.
- Set style from (block.get(“baseStyles”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“baseStyles”) → mapping().
- If style.
  - Set out at “style” from style.
- Set mob from (block.get(“mobileStyles”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“mobileStyles”) → mapping().
- If mob.
  - Set out at “mstyle” from mob.
- Set tab from (block.get(“tabletStyles”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“tabletStyles”) → mapping().
- If (tab and depth ≤ 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tab → depth ≤ 1.
  - Set out at “tstyle” from tab.
- If compact\_slots bound to BlockCodec.\_compress\_slots((block.get(“componentSlots”) or mapping()), depth).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentSlots”) → mapping().
  - Set out at “slots” from compact\_slots.
- Set events from (block.get(“componentEvents”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentEvents”) → mapping().
- If events.
  - Set out at “events” from BlockCodec.\_compress\_events(events).
- If vis bound to block.get(“visibilityCondition”).
  - Set out at “visibility” from vis.
- Set children from list of BlockCodec.compress(c, (depth + 1)) for c drawn from block.get(“children”, list()) where isinstance(c, dict).
  - Draw c from block.get(“children”, list()), keep a combination only if (isinstance(c, dict)).
- If children.
  - Set out at “c” from children.
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L159) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1822)

<a id="op-3ddac66a5400a8"></a>
### Block Codec.compress slots

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_compress_slots`

**Inputs** slots, depth.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- For each tuple(name, slot) in slots.items().
  - If not isinstance(slot, dict).
    - Continue with the next iteration or loop test.
  - Set content from slot.get(“slotContent”).
  - If isinstance(content, list).
    - Set blocks from list of BlockCodec.compress(b, (depth + 1)) for b drawn from content where isinstance(b, dict).
      - Draw b from content, keep a combination only if (isinstance(b, dict)).
    - If blocks.
      - Set out at name from blocks.
- Return out.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1824)

<a id="op-6f87328ed4ea57"></a>
### Block Codec.expand slots

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_expand_slots`

**Inputs** slots.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- If not isinstance(slots, dict).
  - Return out.
- For each tuple(name, content) in slots.items().
  - If not isinstance(content, list).
    - Continue with the next iteration or loop test.
  - Set slot\_content from list of BlockCodec.expand(b) for b drawn from content where isinstance(b, dict).
    - Draw b from content, keep a combination only if (isinstance(b, dict)).
  - Set out at name from mapping(“slotName” → name, “slotContent” → slot\_content).
- Return out.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1851) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1827)

<a id="op-517343381fc65b"></a>
### Block Codec.compress events

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_compress_events`

**Inputs** events.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- For each tuple(name, ev) in events.items().
  - If (isinstance(ev, dict) and ev.get(“action”) equals “Run Script”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(ev, dict) → ev.get(“action”) equals “Run Script”.
    - Set out at name from (ev.get(“script”) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ev.get(“script”) → empty text.
  - Otherwise.
    - Set out at name from ev.
- Return out.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L160) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1823)

<a id="op-bf2f4897a37217"></a>
### Block Codec.expand

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_expand`

**Inputs** node.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Explicit results** node · block.

**Local steps**

- If not isinstance(node, dict).
  - Return node.
- Set block from mapping(“componentName” → node.get(“name”, “container”), “baseStyles” → (node.get(“style”) or mapping()), “componentProps” → (node.get(“props”) or mapping()), “componentSlots” → BlockCodec.\_expand\_slots((n ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“style”) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“props”) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“slots”) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“mstyle”) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in node.get(“tstyle”) → mapping().
  - Draw c from node.get(“c”, list()), keep a combination only if (isinstance(c, dict)).
- If cid bound to node.get(“id”).
  - Set block at “componentId” from cid.
- If orig bound to node.get(“originalElement”).
  - Set block at “originalElement” from orig.
- If label bound to node.get(“label”).
  - Set block at “blockName” from label.
- If events bound to node.get(“events”).
  - Set block at “componentEvents” from BlockCodec.\_expand\_events(events).
- If vis bound to node.get(“visibility”).
  - Set block at “visibilityCondition” from vis.
- Return block.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L162) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1849) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1825)

<a id="op-2236fdc752848d"></a>
### Block Codec.expand events

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_expand_events`

**Inputs** events.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- If not isinstance(events, dict).
  - Return out.
- For each tuple(name, val) in events.items().
  - If isinstance(val, str).
    - Set out at name from mapping(“event” → name, “action” → “Run Script”, “script” → val).
  - Otherwise.
    - If isinstance(val, dict).
      - Set ev from dict(val).
      - Evaluate ev.setdefault(“event”, name).
      - Evaluate ev.setdefault(“action”, “Run Script”).
      - Set out at name from ev.
- Return out.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L163) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1850) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1826)

<a id="op-e27704be92a62c"></a>
### Block Codec.parse blocks

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_parse_blocks`

**Inputs** content.

**Wrappers, in declaration order** staticmethod.

**Declared result** dict.

**Explicit results** BlockCodec.expand(block).

**Explicit failure paths** ValueError(“LLM response is not a valid block object”) · ValueError(“LLM response produced an empty block”).

**Local steps**

- Set cleaned from BlockCodec.strip\_fences(content).
- Attempt the following.
  - Set parsed from json.loads(cleaned, strict = false).
- On failure (json.JSONDecodeError).
  - Set parsed from repair\_json(cleaned, return\_objects = true).
- If isinstance(parsed, list).
  - Set block from parsed at 0 when parsed, otherwise mapping().
    - Value choice on parsed — true gives parsed at 0, false gives mapping().
- Otherwise.
  - If isinstance(parsed, dict).
    - Set block from parsed.
  - Otherwise.
    - Raise ValueError(“LLM response is not a valid block object”).
- If not block.
  - Raise ValueError(“LLM response produced an empty block”).
- If (isinstance(block, dict) and not block.get(“id”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(block, dict) → not block.get(“id”).
  - Set block at “id” from “root”.
- Return BlockCodec.expand(block).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L165) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1852) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1828)

<a id="op-b438b14cd7c135"></a>
### Block Codec.to json

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_to_json`

**Inputs** data.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** json.dumps(data, separators = tuple(“,”, “:”), ensure\_ascii = false).

**Local steps**

- Return json.dumps(data, separators = tuple(“,”, “:”), ensure\_ascii = false).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L167) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1854) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1830)

<a id="op-ee078cc5978285"></a>
### Block Codec.strip fences

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_strip_fences`

**Inputs** text.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** re.sub(“\\n?′′′\\s\*$”, empty text, text).strip().

**Local steps**

- Set text from re.sub(“^′′′(?:json\|yaml)?\\s\*\\n?”, empty text, text.strip()).
- Return re.sub(“\\n?′′′\\s\*$”, empty text, text).strip().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L166) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1829)

<a id="op-e262eaaa322a9d"></a>
### Block Codec.validate image data

`operation_foundation_binding_foundation_studio_ai_block_codec_blockcodec_validate_image_data`

**Inputs** image\_data.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** image\_data.

**Explicit failure paths** validation helper — translated “Invalid image data: must be a base64-encoded image data URL” · validation helper — translated “Invalid image data: must be a base64-encoded data URL” · validation helper — translated “Image is too large. Please use an image smaller than 5 MB.”.

**Local steps**

- If not image\_data.startswith(“data:image/”).
  - Call the validation error handler Platform.throw(translated “Invalid image data: must be a base64-encoded image data URL”).
- If “;base64,” does not belong to image\_data.
  - Call the validation error handler Platform.throw(translated “Invalid image data: must be a base64-encoded data URL”).
- If len(image\_data) &gt; ((7 × 1024) × 1024).
  - Call the validation error handler Platform.throw(translated “Image is too large. Please use an image smaller than 5 MB.”).
- Return image\_data.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L168) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1831)

## Service · Boot

<a id="op-dbcb0cfa80d289"></a>
### Get bootinfo

`operation_foundation_boot_business_behavior_get_bootinfo`

**Inputs** no declared parameters.

**Record and data access** read “Domain” via get\_all · read “DocType” via get\_all · read “DocField” via get\_all · read “File” via get\_value · read “SMS Settings” via get\_single\_value · 1 additional forms in the steps below.

**Explicit results** bootinfo.

**Local steps**

- Bind dependencies get\_lang\_dict, get\_translated\_doctypes.
- Evaluate Platform.set\_user\_lang(Platform.session.user).
- Set bootinfo from Platform.\_dict().
- Set hooks from Platform.get\_hooks().
- Set doclist from list().
- Evaluate get\_user(bootinfo).
- Set bootinfo.sitename from Platform.local.site.
- Set bootinfo.sysdefaults from Platform.defaults.get\_defaults().
- Set bootinfo.sysdefaults at “setup\_complete” from Platform.is\_setup\_complete().
- If not bootinfo.sysdefaults at “setup\_complete”.
  - Set bootinfo.setup\_wizard\_url from get\_setup\_wizard\_url().
- Set bootinfo.server\_date from Platform.utils.nowdate().
- If Platform.session at “user” differs from “Guest”.
  - Set bootinfo.user\_info from get\_user\_info().
- Set desk\_views from DeskViews().
- Evaluate desk\_views.build\_entities().
- Evaluate desk\_views.add\_to\_boot(bootinfo).
- Evaluate load\_desktop\_data(bootinfo, desk\_views).
- Set bootinfo.letter\_heads from get\_letter\_heads().
- Set bootinfo.active\_domains from Platform.get\_active\_domains().
- Set bootinfo.all\_domains from Platform.get\_all(“Domain”, pluck = “name”).
- Evaluate add\_layouts(bootinfo).
- Set bootinfo.module\_app from get\_boot\_module\_app().
- Bind dependencies get\_code\_only\_module\_heirs.
- Set bootinfo.code\_only\_module\_heirs from get\_code\_only\_module\_heirs().
- Set bootinfo.single\_types from Platform.get\_all(“DocType”, mapping(“issingle” → 1), pluck = “name”).
- Set bootinfo.nested\_set\_doctypes from Platform.get\_all(“DocField”, mapping(“fieldname” → “lft”), pluck = “parent”).
- Set bootinfo.tree\_view\_doctypes from get\_tree\_view\_doctypes().
- Evaluate add\_home\_page(bootinfo, doclist).
- Evaluate load\_translations(bootinfo).
- Evaluate add\_timezone\_info(bootinfo).
- Evaluate load\_conf\_settings(bootinfo).
- Evaluate load\_print(bootinfo, doclist).
- Evaluate doclist.extend(get\_meta\_bundle(“Page”)).
- Set bootinfo.home\_folder from Platform.db.get\_value(“File”, mapping(“is\_home\_folder” → 1)).
- Set bootinfo.navbar\_settings from get\_navbar\_settings().
- Set bootinfo.notification\_settings from get\_notification\_settings().
- Set bootinfo.onboarding\_tours from get\_onboarding\_ui\_tours().
- Evaluate set\_time\_zone(bootinfo).
- If Platform.session.data.get(“ipinfo”).
  - Set bootinfo.ipinfo from Platform.session at “data” at “ipinfo”.
- Set bootinfo.docs from doclist.
- Evaluate load\_country\_doc(bootinfo).
- Evaluate load\_currency\_docs(bootinfo).
- For each method in (hooks.boot\_session or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hooks.boot\_session → list().
  - Evaluate Platform.get\_attr(method)(bootinfo).
- If bootinfo.lang.
  - Set bootinfo.lang from str(bootinfo.lang).
- Set bootinfo.versions from mapping of k → v at “version” for tuple(k, v) drawn from get\_versions().items().
  - Draw tuple(k, v) from get\_versions().items().
- Set bootinfo.error\_report\_email from Platform.conf.error\_report\_email.
- Set bootinfo.calendars from sorted(Platform.get\_hooks(“calendars”)).
- Set bootinfo.treeviews from (Platform.get\_hooks(“treeviews”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“treeviews”) → list().
- Set bootinfo.has\_awesomebar\_search from bool(hooks.awesomebar\_search).
- Set bootinfo.lang\_dict from get\_lang\_dict().
- Set bootinfo.success\_action from get\_success\_action().
- Evaluate bootinfo.update(get\_email\_accounts(user = Platform.session.user)).
- Set bootinfo.sms\_gateway\_enabled from bool(Platform.db.get\_single\_value(“SMS Settings”, “sms\_gateway\_url”)).
- Set bootinfo.frequently\_visited\_links from frequently\_visited\_links().
- Set bootinfo.link\_preview\_doctypes from get\_link\_preview\_doctypes().
- Set bootinfo.additional\_filters\_config from get\_additional\_filters\_from\_hooks().
- Set bootinfo.desk\_settings from get\_desk\_settings().
- Set bootinfo.app\_logo\_url from get\_app\_logo().
- Set bootinfo.link\_title\_doctypes from get\_link\_title\_doctypes().
- Set bootinfo.link\_settings from get\_link\_settings() when cint(Platform.get\_system\_settings(“enable\_combobox\_link\_field”)), otherwise mapping().
  - Value choice on cint(Platform.get\_system\_settings(“enable\_combobox\_link\_field”)) — true gives get\_link\_settings(), false gives mapping().
- Set bootinfo.web\_form\_request\_forms from get\_request\_forms\_by\_doctype().
- Set bootinfo.translated\_doctypes from get\_translated\_doctypes().
- Set bootinfo.doctype\_ptype\_map from get\_doctype\_ptype\_map().
- Set bootinfo.subscription\_conf from add\_subscription\_conf().
- Set bootinfo.is\_fc\_site from is\_fc\_site().
- Set bootinfo.cloud\_settings from get\_cloud\_settings\_boot\_context().
- Set bootinfo.is\_v2\_site from is\_v2\_site().
- Set bootinfo.enable\_address\_autocompletion from Platform.db.get\_single\_value(“Geolocation Settings”, “enable\_address\_autocompletion”).
- If sentry\_dsn bound to get\_sentry\_dsn().
  - Set bootinfo.sentry\_dsn from sentry\_dsn.
- Set bootinfo.setup\_wizard\_completed\_apps from (get\_setup\_wizard\_completed\_apps() or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_setup\_wizard\_completed\_apps() → list().
- Set bootinfo.desktop\_icon\_urls from get\_desktop\_icon\_urls().
- Set bootinfo.desktop\_icon\_style from (get\_icon\_style() or “Subtle”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_icon\_style() → “Subtle”.
- Set bootinfo.desktop\_page from get\_desktop\_page().
- If bootinfo.is\_fc\_site.
  - Set bootinfo.site\_info from current\_site\_info().
- Return bootinfo.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(), Platform.get\_attr(method) and 2 further calls · clock or generated value from Platform.utils.nowdate() · configured or stored value from Platform.db.get\_single\_value(“SMS Settings”, “sms\_gateway\_url”), Platform.get\_system\_settings(“enable\_combobox\_link\_field”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L95) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L495)

<a id="op-12aa61a76ca44c"></a>
### Get icon style

`operation_foundation_boot_business_behavior_get_icon_style`

**Inputs** no declared parameters.

**Record and data access** read “Desktop Settings” via get\_single\_value.

**Explicit results** “Solid” · icon\_style.

**Local steps**

- Set icon\_style from Platform.db.get\_single\_value(“Desktop Settings”, “icon\_style”).
- If icon\_style does not belong to list(“Subtle”, “Solid”).
  - Return “Solid”.
- Return icon\_style.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Desktop Settings”, “icon\_style”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0016.json#L7071) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L498)

<a id="op-c491362fc09657"></a>
### Get letter heads

`operation_foundation_boot_business_behavior_get_letter_heads`

**Inputs** no declared parameters.

**Record and data access** read “Letter Head” via get\_list.

**Explicit results** letter\_heads.

**Local steps**

- Set letter\_heads from mapping().
- If not Platform.has\_permission(“Letter Head”).
  - Return letter\_heads.
- For each letter\_head in Platform.get\_list(“Letter Head”, fields = list(“name”, “content”, “footer”)).
  - Evaluate letter\_heads.setdefault(letter\_head.name, mapping(“header” → letter\_head.content, “footer” → letter\_head.footer)).
- Return letter\_heads.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Letter Head”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0016.json#L7186) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L499)

<a id="op-2e9978efbcf6a0"></a>
### Load conf settings

`operation_foundation_boot_business_behavior_load_configuration_settings`

**Inputs** bootinfo.

**Local steps**

- Bind dependencies get\_file\_chunk\_size, get\_max\_file\_size.
- Set bootinfo.max\_file\_size from get\_max\_file\_size().
- Set bootinfo.file\_chunk\_size from get\_file\_chunk\_size().
- For each key in tuple(“developer\_mode”, “socketio\_port”, “socketio\_backend”, “file\_watcher\_port”).
  - If key belongs to Platform.conf.
    - Set bootinfo at key from Platform.conf.get(key).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L509)

<a id="op-91dd4c19a9b528"></a>
### Get boot module app

`operation_foundation_boot_business_behavior_get_boot_module_application`

**Inputs** no declared parameters.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** module\_app.

**Local steps**

- Set module\_app from dict(Platform.local.module\_app).
- Set installed\_apps from set(Platform.get\_installed\_apps()).
- For each module in Platform.get\_all(“Module Def”, fields = list(“name”, “app\_name”)).
  - Set key from Platform.scrub(module.name).
  - If (key does not belong to module\_app and module.app\_name belongs to installed\_apps).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in key does not belong to module\_app → module.app\_name belongs to installed\_apps.
    - Set module\_app at key from module.app\_name.
- Return module\_app.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L197) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L494)

<a id="op-9fc2edb22f7294"></a>
### Get app rail host map

`operation_foundation_boot_business_behavior_get_application_rail_host_map`

**Inputs** no declared parameters.

**Explicit results** mounted\_apps().

**Local steps**

- Bind dependencies mounted\_apps.
- Return mounted\_apps().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L472) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L493)

<a id="op-721ee19c5e0db3"></a>
### Load desktop data

`operation_foundation_boot_business_behavior_load_desktop_data`

**Inputs** bootinfo, desk\_views = no value.

**Local steps**

- Bind dependencies resolve\_dock.
- Bind dependencies build\_canonical\_shells.
- Bind dependencies get\_desktop\_apps.
- Set desk\_views from (desk\_views or DeskViews()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in desk\_views → DeskViews().
- Set bootinfo.app\_rail\_host from get\_app\_rail\_host\_map().
- Set bootinfo.dock from resolve\_dock().
- Set bootinfo.module\_sidebars from get\_module\_sidebars().
- Set bootinfo.entity\_module from build\_entity\_module\_map(bootinfo.module\_sidebars).
- Set default\_workspace from ((nested operand in the contract(nested operand in the contract) or mapping()).get(“default\_workspace”) or mapping()).get(“name”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (bootinfo.get(“user”) or mapping()).get(“default\_workspace”) → mapping().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bootinfo.get(“user”) → mapping().
- Set tuple(bootinfo.canonical\_shell, bootinfo.home\_shell) from build\_canonical\_shells(bootinfo.module\_sidebars, bootinfo.entity\_module, desk\_views, default\_workspace = default\_workspace).
- If is\_desktop\_icons\_page().
  - Bind dependencies get\_desktop\_icons.
  - Set bootinfo.desktop\_icons from get\_desktop\_icons(bootinfo = bootinfo).
- Set bootinfo.app\_data from get\_app\_data().
- Set bootinfo.studio\_apps from get\_desktop\_apps().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L100) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L425) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L512)

<a id="op-4078678f795708"></a>
### Get app data

`operation_foundation_boot_business_behavior_get_application_data`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** app\_data.

**Local steps**

- Bind dependencies get\_app\_entry\_set.
- Set app\_data from list().
- Set app\_rail\_host from get\_app\_rail\_host\_map().
- For each app\_name in Platform.get\_installed\_apps().
  - Set apps from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app\_name).
  - Set app\_info from mapping().
  - If apps.
    - Set app\_info from apps at 0.
    - Set has\_permission from app\_info.get(“has\_permission”).
    - If (has\_permission and not Platform.get\_attr(has\_permission)()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_permission → not Platform.get\_attr(has\_permission)().
      - Evaluate app\_data.append(dict(on\_apps\_screen = false, sequence\_id = (app\_info.get(“sequence\_id”) or DEFAULT\_APP\_SEQUENCE\_ID), app\_name = (app\_info.get(“name”) or app\_name), app\_title = (app\_info.get(“title”) or (ne ….
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“sequence\_id”) → DEFAULT\_APP\_SEQUENCE\_ID.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“name”) → app\_name.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“title”) → (Platform.get\_hooks(“app\_title”, app\_name = app\_name) or list(no value)) at 0 → app\_name.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = app\_name) → list(no value).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“logo”) → Platform.get\_hooks(“app\_logo\_url”, app\_name = app\_name) → Platform.get\_hooks(“app\_logo\_url”, app\_name = “Platform”).
      - Continue with the next iteration or loop test.
  - Set dock from get\_app\_entry\_set(app\_name).
  - Evaluate app\_data.append(dict(on\_apps\_screen = (bool(apps) and app\_name does not belong to app\_rail\_host), sequence\_id = (app\_info.get(“sequence\_id”) or DEFAULT\_APP\_SEQUENCE\_ID), app\_name = (app\_info.get(“name”) or ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(apps) → app\_name does not belong to app\_rail\_host.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“sequence\_id”) → DEFAULT\_APP\_SEQUENCE\_ID.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“name”) → app\_name.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“title”) → ((Platform.get\_hooks(“app\_title”, app\_name = app\_name) and Platform.get\_hooks(“app\_title”, app\_name = app\_name) at 0) or empty text) → app\_name.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (Platform.get\_hooks(“app\_title”, app\_name = app\_name) and Platform.get\_hooks(“app\_title”, app\_name = app\_name) at 0) → empty text.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_hooks(“app\_title”, app\_name = app\_name) → Platform.get\_hooks(“app\_title”, app\_name = app\_name) at 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“route”) → (Platform.get\_hooks(“app\_home”, app\_name = app\_name) and Platform.get\_hooks(“app\_home”, app\_name = app\_name) at 0) → empty text.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_hooks(“app\_home”, app\_name = app\_name) → Platform.get\_hooks(“app\_home”, app\_name = app\_name) at 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“desk\_route”) → empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_info.get(“logo”) → Platform.get\_hooks(“app\_logo\_url”, app\_name = app\_name) → no value.
- Return app\_data.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“add\_to\_apps\_screen”, app\_name = app\_name), Platform.get\_attr(has\_permission) and 4 further calls.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L93) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L491)

<a id="op-7f6572e1968d97"></a>
### Get app modules

`operation_foundation_boot_business_behavior_get_application_modules`

**Inputs** app\_name.

**Declared result** list at str.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** list() · sorted(modules, key = deferred anonymous expression).

**Local steps**

- Bind dependencies get\_code\_only\_modules, get\_visible\_modules.
- Set modules from get\_visible\_modules(Platform.get\_all(“Module Def”, filters = mapping(“app\_name” → app\_name), pluck = “name”)).
- If not modules.
  - Return list().
- Set code\_only from get\_code\_only\_modules().
- Set modules from list of module for module drawn from modules where module does not belong to code\_only.
  - Draw module from modules, keep a combination only if (module does not belong to code\_only).
- Set declared from mapping of name → idx for tuple(idx, name) drawn from enumerate(Platform.get\_module\_list(app\_name)).
  - Draw tuple(idx, name) from enumerate(Platform.get\_module\_list(app\_name)).
- Return sorted(modules, key = deferred anonymous expression).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L94) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L492)

<a id="op-316a739b5d2a3c"></a>
### Load translations

`operation_foundation_boot_business_behavior_load_translations`

**Inputs** bootinfo.

**Local steps**

- Bind dependencies get\_messages\_for\_boot.
- Set bootinfo at “lang” from Platform.lang.
- Set bootinfo at “\_\_messages” from get\_messages\_for\_boot().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L101) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L515)

<a id="op-05e081f9a9d018"></a>
### Get user info

`operation_foundation_boot_business_behavior_get_user_info`

**Inputs** no declared parameters.

**Explicit results** user\_info.

**Local steps**

- Set user\_info from Platform.\_dict().
- Evaluate add\_user\_info(Platform.session.user, user\_info).
- Return user\_info.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L2407) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L508)

<a id="op-6814af4afcfab8"></a>
### Get user

`operation_foundation_boot_business_behavior_get_user`

**Inputs** bootinfo.

**Local steps**

- Set bootinfo.user from Platform.get\_user().load\_user().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L2495) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L507)

<a id="op-9c110c033b2709"></a>
### Add home page

`operation_foundation_boot_business_behavior_add_home_page`

**Inputs** bootinfo, docs.

**Explicit results** no value.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Return no value.
- Set home\_page from Platform.db.get\_default(“desktop:home\_page”).
- If not Platform.is\_setup\_complete().
  - Set bootinfo.setup\_wizard\_requires from Platform.get\_hooks(“setup\_wizard\_requires”).
- Attempt the following.
  - Set page from Platform.desk.desk\_page.get(home\_page).
  - Evaluate docs.append(page).
  - Set bootinfo at “home\_page” from page.name.
- On failure (tuple(Platform.DoesNotExistError, Platform.PermissionError)).
  - Evaluate Platform.clear\_last\_message().
  - Set bootinfo at “home\_page” from “desktop”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“setup\_wizard\_requires”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L2565) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L485)
