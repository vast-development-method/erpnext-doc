# Workflow, automation and dispatch · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Extract

<a id="op-7583a074764de5"></a>
### As text

`operation_foundation_binding_foundation_flow_knowledge_extract_as_text`

**Inputs** content.

**Declared result** str.

**Explicit results** content · content.decode(encoding, errors = “replace”).

**Local steps**

- If isinstance(content, str).
  - Return content.
- Bind dependencies chardet.
- Set encoding from ((chardet.detect(content) or mapping()).get(“encoding”) or “utf-8”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (chardet.detect(content) or mapping()).get(“encoding”) → “utf-8”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in chardet.detect(content) → mapping().
- Return content.decode(encoding, errors = “replace”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L181) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1159)

<a id="op-aca0183d80a567"></a>
### Clean pdf text

`operation_foundation_binding_foundation_flow_knowledge_extract_clean_pdf_text`

**Inputs** text.

**Declared result** str.

**Explicit results** text.strip().

**Local steps**

- Set text from re.sub(“(?&lt;!\\n)&#91; \\t&#93;\*\\n&#91; \\t&#93;\*(?!\\n)”, one space, text).
- Set text from re.sub(“&#91; \\t&#93;{2,}”, one space, text).
- Return text.strip().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1160)

<a id="op-2672c86c32ff12"></a>
### Parse filters

`operation_foundation_binding_foundation_flow_knowledge_extract_parse_filters`

**Inputs** raw.

**Declared result** dict.

**Explicit results** mapping() · parsed.

**Explicit failure paths** validation helper — translated “Filters must be valid JSON.” · validation helper — translated “Filters must be a JSON object.”.

**Local steps**

- If not raw.
  - Return mapping().
- Bind dependencies json.
- Attempt the following.
  - Set parsed from json.loads(raw).
- On failure (tuple(TypeError, ValueError)).
  - Call the validation error handler Platform.throw(translated “Filters must be valid JSON.”, title = translated “Invalid Filters”).
- If not isinstance(parsed, dict).
  - Call the validation error handler Platform.throw(translated “Filters must be a JSON object.”, title = translated “Invalid Filters”).
- Return parsed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L197) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1199) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1175)

<a id="op-64d1c81b487c9c"></a>
### Row to text

`operation_foundation_binding_foundation_flow_knowledge_extract_row_to_text`

**Inputs** row, fields, meta.

**Declared result** str.

**Explicit results** whitespace '\\n'.join(lines).

**Local steps**

- Bind dependencies cstr.
- Set lines from list().
- For each fieldname in fields.
  - Set value from row.get(fieldname).
  - If value belongs to tuple(no value, empty text).
    - Continue with the next iteration or loop test.
  - Set df from meta.get\_field(fieldname).
  - Set text from \_render\_rich\_text(df, cstr(value)).
  - If not text.
    - Continue with the next iteration or loop test.
  - Set label from df.label when df, otherwise fieldname.
    - Value choice on df — true gives df.label, false gives fieldname.
  - Evaluate lines.append(formatted text {label}: {text}).
- Return whitespace '\\n'.join(lines).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L202) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1180)

<a id="op-2b4fafe10fdc0f"></a>
### Render rich text

`operation_foundation_binding_foundation_flow_knowledge_extract_render_rich_text`

**Inputs** df, value.

**Declared result** str.

**Explicit results** value · \_extract\_html(value) · \_extract\_html(md\_to\_html(value)).

**Local steps**

- If not df.
  - Return value.
- If df.fieldtype belongs to HTML\_FIELDTYPES.
  - Return \_extract\_html(value).
- If (df.fieldtype belongs to MARKDOWN\_FIELDTYPES or (df.fieldtype equals “Code” and df.options equals “Markdown”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype belongs to MARKDOWN\_FIELDTYPES → (df.fieldtype equals “Code” and df.options equals “Markdown”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Code” → df.options equals “Markdown”.
  - Bind dependencies md\_to\_html.
  - Return \_extract\_html(md\_to\_html(value)).
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L200) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1178)

<a id="op-a7f3a653bc8326"></a>
### Validate public url

`operation_foundation_binding_foundation_flow_knowledge_extract_validate_public_url`

**Inputs** url.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “URL must use http or https.” · validation helper — translated “URL has no host.” · validation helper — translated “Could not resolve URL host.” · validation helper — translated “URL resolves to a non-public address.”.

**Local steps**

- Bind dependencies ipaddress.
- Bind dependencies socket.
- Bind dependencies urlparse.
- Set parsed from urlparse(url).
- If parsed.scheme does not belong to tuple(“http”, “https”).
  - Call the validation error handler Platform.throw(translated “URL must use http or https.”, title = translated “Invalid URL”).
- If not parsed.hostname.
  - Call the validation error handler Platform.throw(translated “URL has no host.”, title = translated “Invalid URL”).
- Attempt the following.
  - Set infos from socket.getaddrinfo(parsed.hostname, no value).
- On failure (socket.gaierror).
  - Call the validation error handler Platform.throw(translated “Could not resolve URL host.”, title = translated “Invalid URL”).
- For each info in infos.
  - Set ip from ipaddress.ip\_address(info at 4 at 0).
  - If (ip.is\_private or ip.is\_loopback or ip.is\_link\_local or ip.is\_reserved or ip.is\_multicast or ip.is\_unspecified).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ip.is\_private → ip.is\_loopback → ip.is\_link\_local → ip.is\_reserved → ip.is\_multicast → ip.is\_unspecified.
    - Call the validation error handler Platform.throw(translated “URL resolves to a non-public address.”, title = translated “Blocked URL”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.getaddrinfo(parsed.hostname, no value).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L205) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1183)

<a id="op-b50b0ca849a548"></a>
### Read capped

`operation_foundation_binding_foundation_flow_knowledge_extract_read_capped`

**Inputs** response.

**Declared result** bytes.

**Explicit results** byte value.join(chunks).

**Explicit failure paths** validation helper — translated “Remote file exceeds the size limit.”.

**Local steps**

- Set chunks from list().
- Set total from 0.
- For each chunk in response.iter\_content(8192).
  - Update total using + len(chunk).
  - If total &gt; MAX\_FETCH\_BYTES.
    - Call the validation error handler Platform.throw(translated “Remote file exceeds the size limit.”, title = translated “File Too Large”).
  - Evaluate chunks.append(chunk).
- Return byte value.join(chunks).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L198) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1176)

## Record · Flow agent

<a id="op-d4dd4b6d355b28"></a>
### Flow Agent.on update

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies warn\_existing\_sessions.
- Set before from self.get\_doc\_before\_save().
- If (before and (list of row.tool for row drawn from before.tools differs from list of row.tool for row drawn from self.tools or list of row.agent for row drawn from before.sub\_agents differs from list of row. ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → (list of row.tool for row drawn from before.tools differs from list of row.tool for row drawn from self.tools or list of row.agent for row drawn from before.sub\_agents differs from list of row.agent for ro ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of row.tool for row drawn from before.tools differs from list of row.tool for row drawn from self.tools → list of row.agent for row drawn from before.sub\_agents differs from list of row.agent for row drawn from self.sub\_agents.
  - Draw row from before.tools.
  - Draw row from self.tools.
  - Draw row from before.sub\_agents.
  - Draw row from self.sub\_agents.
  - Evaluate warn\_existing\_sessions(list(self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1005) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L981)

<a id="op-15d0cbab3cdee9"></a>
### Flow Agent.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_on_trash`

**Inputs** self.

**Local steps**

- Bind dependencies ASSISTANT\_AGENT\_NAME.
- Evaluate block\_delete(self, always = self.name equals ASSISTANT\_AGENT\_NAME).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L2) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1004) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L980)

<a id="op-da79ae126f3b31"></a>
### Flow Agent.before insert

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_before_insert`

**Inputs** self.

**Local steps**

- Evaluate block\_insert(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L243) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L992) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L968)

<a id="op-f286252421e418"></a>
### Flow Agent.before rename

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_before_rename`

**Inputs** self, old, new, \_merge = false.

**Declared result** no value.

**Record and data access** read “Flow Agent Sub Agent” via get\_all.

**Local steps**

- Bind dependencies block\_rename\_in\_chats.
- Evaluate block\_rename(self, old).
- Evaluate block\_slash\_in\_name(self, new).
- Evaluate block\_rename\_in\_chats(old, Platform.get\_all(“Flow Agent Sub Agent”, filters = mapping(“agent” → old), pluck = “parent”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L244) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L993) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L969)

<a id="op-402c29b965e40a"></a>
### Flow Agent.after rename

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_after_rename`

**Inputs** self, old, new, \_merge = false.

**Declared result** no value.

**Local steps**

- Bind dependencies store.
- Evaluate store.rename\_agent(old, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L242) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L991) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L967)

<a id="op-5436beaeb68368"></a>
### Flow Agent.validate

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_validate`

**Inputs** self.

**Local steps**

- Bind dependencies ASSISTANT\_AGENT\_NAME.
- Evaluate block\_slash\_in\_name(self).
- Evaluate self.\_validate\_max\_iterations().
- Evaluate self.\_validate\_token\_budget().
- Evaluate self.\_validate\_skills().
- Evaluate self.\_validate\_sub\_agents().
- Evaluate self.render\_instructions().
- Evaluate self.\_ensure\_knowledge\_search\_tool().
- Evaluate validate\_immutable(self, tuple(“description”, “instructions”, “max\_iterations”, “tools”, …)).
  - Value choice on self.name equals ASSISTANT\_AGENT\_NAME — true gives tuple(), false gives tuple(“knowledge\_bases”, “skills”).
- Evaluate self.\_ensure\_skill\_tool().
- Evaluate self.\_ensure\_subagent\_tool().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate max iterations](operations-021.md#op-7df429748d67d6), [validate token budget](operations-021.md#op-727a9a642ff5d7), [validate skills](operations-021.md#op-1ce722107b6b1e), [validate sub agents](operations-021.md#op-6fa3098271951e), [render instructions](operations-022.md#op-28f0cb46ac79f6), [ensure knowledge search tool](operations-021.md#op-c3e57f84f7d7c0), [ensure skill tool](operations-021.md#op-cdffe7e1175a3b), [ensure subagent tool](operations-021.md#op-2377a472f676e4).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L11) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1013) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L989)

<a id="op-7df429748d67d6"></a>
### Flow Agent.validate max iterations

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_validate_max_iterations`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Max Iterations must be at least 1.”.

**Local steps**

- If (self.max\_iterations is distinct from no value and self.max\_iterations &lt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.max\_iterations is distinct from no value → self.max\_iterations &lt; 1.
  - Call the validation error handler Platform.throw(translated “Max Iterations must be at least 1.”, title = translated “Invalid Max Iterations”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L12) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1014) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L990)

<a id="op-727a9a642ff5d7"></a>
### Flow Agent.validate token budget

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_validate_token_budget`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L15) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1017) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L993)

<a id="op-1ce722107b6b1e"></a>
### Flow Agent.validate skills

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_validate_skills`

**Inputs** self.

**Explicit failure paths** validation helper — translated “An agent can bind at most {0} skills.”.format(MAX\_SKILLS).

**Local steps**

- If (len(self.skills) &gt; MAX\_SKILLS and not self.is\_system\_generated).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(self.skills) &gt; MAX\_SKILLS → not self.is\_system\_generated.
  - Call the validation error handler Platform.throw(translated “An agent can bind at most {0} skills.”.format(MAX\_SKILLS), title = translated “Too Many Skills”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L13) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1015) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L991)

<a id="op-6fa3098271951e"></a>
### Flow Agent.validate sub agents

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_validate_sub_agents`

**Inputs** self.

**Explicit failure paths** validation helper — translated “An agent cannot be its own sub-agent.”.

**Local steps**

- If any(generator of row.agent equals self.name for row drawn from self.sub\_agents).
  - Draw row from self.sub\_agents.
  - Call the validation error handler Platform.throw(translated “An agent cannot be its own sub-agent.”, title = translated “Invalid Sub-agent”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L14) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1016) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L992)

<a id="op-c3e57f84f7d7c0"></a>
### Flow Agent.ensure knowledge search tool

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_ensure_knowledge_search_tool`

**Inputs** self.

**Record and data access** read “Flow Tool” via exists.

**Explicit results** no value.

**Local steps**

- Bind dependencies KNOWLEDGE\_SEARCH\_SLUG, builtin\_name.
- If not self.knowledge\_bases.
  - Return no value.
- If any(generator of row.tool equals builtin\_name(KNOWLEDGE\_SEARCH\_SLUG) for row drawn from self.tools).
  - Draw row from self.tools.
  - Return no value.
- If Platform.db.exists(“Flow Tool”, builtin\_name(KNOWLEDGE\_SEARCH\_SLUG)).
  - Evaluate self.append(“tools”, mapping(“tool” → builtin\_name(KNOWLEDGE\_SEARCH\_SLUG))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L248) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L997) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L973)

<a id="op-cdffe7e1175a3b"></a>
### Flow Agent.ensure skill tool

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_ensure_skill_tool`

**Inputs** self.

**Record and data access** read “Flow Tool” via exists.

**Explicit results** no value.

**Local steps**

- Bind dependencies SKILL\_TOOL\_SLUG, builtin\_name.
- If not self.skills.
  - Return no value.
- If any(generator of row.tool equals builtin\_name(SKILL\_TOOL\_SLUG) for row drawn from self.tools).
  - Draw row from self.tools.
  - Return no value.
- If Platform.db.exists(“Flow Tool”, builtin\_name(SKILL\_TOOL\_SLUG)).
  - Evaluate self.append(“tools”, mapping(“tool” → builtin\_name(SKILL\_TOOL\_SLUG))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L249) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L998) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L974)

<a id="op-2377a472f676e4"></a>
### Flow Agent.ensure subagent tool

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_ensure_subagent_tool`

**Inputs** self.

**Record and data access** read “Flow Tool” via exists.

**Explicit results** no value.

**Local steps**

- Bind dependencies SUBAGENT\_TOOL\_SLUG, builtin\_name.
- If not self.sub\_agents.
  - Return no value.
- If any(generator of row.tool equals builtin\_name(SUBAGENT\_TOOL\_SLUG) for row drawn from self.tools).
  - Draw row from self.tools.
  - Return no value.
- If Platform.db.exists(“Flow Tool”, builtin\_name(SUBAGENT\_TOOL\_SLUG)).
  - Evaluate self.append(“tools”, mapping(“tool” → builtin\_name(SUBAGENT\_TOOL\_SLUG))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L250) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L999) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L975)

<a id="op-01c0189fb4417f"></a>
### Flow Agent.client tool config

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_client_tool_config`

**Inputs** self, session = no value.

**Declared result** dict at tuple(str, list at Any).

**Explicit results** mapping(“client\_tools” → list of tool.to\_dict() for tool drawn from tools, “confirm\_tools” → list of tool.name for tool drawn from tools where tool.requires\_confirmation).

**Local steps**

- Set tools from self.client\_tools(session).
- Return mapping(“client\_tools” → list of tool.to\_dict() for tool drawn from tools, “confirm\_tools” → list of tool.name for tool drawn from tools where tool.requires\_confirmation).
  - Draw tool from tools.
  - Draw tool from tools, keep a combination only if (tool.requires\_confirmation).

**Methods declared on this owner** [client tools](operations-021.md#op-a3b5e9a83085d7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L245) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L994) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L970)

<a id="op-a3b5e9a83085d7"></a>
### Flow Agent.client tools

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_client_tools`

**Inputs** self, session = no value.

**Declared result** list at Tool.

**Explicit results** resolved.

**Local steps**

- Bind dependencies embeddings\_configured.
- Bind dependencies MEMORY\_TOOL\_SLUG.
- Bind dependencies ATTACHMENT\_READ\_SLUG, ATTACHMENT\_SEARCH\_SLUG, EXECUTE\_SLUG, KNOWLEDGE\_SEARCH\_SLUG, SERVER\_TOOL\_SLUGS, SKILL\_TOOL\_SLUG, bind\_load\_skill, bind\_read\_attachment, bind\_search\_attachments, bind\_search\_knowledge, bind\_update\_memory, builtin\_name.
- Bind dependencies is\_safe\_exec\_enabled.
- Set daemon\_builtins from set of builtin\_name(slug) for slug drawn from SERVER\_TOOL\_SLUGS.
  - Draw slug from SERVER\_TOOL\_SLUGS.
- Set scripts\_off from not is\_safe\_exec\_enabled().
- Set resolved from list().
- For each tool\_doc in self.\_enabled\_tool\_docs().
  - If (tool\_doc.name belongs to daemon\_builtins or tool\_doc.type equals “Server”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tool\_doc.name belongs to daemon\_builtins → tool\_doc.type equals “Server”.
    - Continue with the next iteration or loop test.
  - If (scripts\_off and (tool\_doc.type equals “Script” or tool\_doc.name equals builtin\_name(EXECUTE\_SLUG))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in scripts\_off → (tool\_doc.type equals “Script” or tool\_doc.name equals builtin\_name(EXECUTE\_SLUG)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tool\_doc.type equals “Script” → tool\_doc.name equals builtin\_name(EXECUTE\_SLUG).
    - Continue with the next iteration or loop test.
  - If tool\_doc.name equals builtin\_name(KNOWLEDGE\_SEARCH\_SLUG).
    - Evaluate resolved.append(bind\_search\_knowledge(list of kb.knowledge\_base for kb drawn from self.knowledge\_bases)).
      - Draw kb from self.knowledge\_bases.
  - Otherwise.
    - If tool\_doc.name equals builtin\_name(ATTACHMENT\_SEARCH\_SLUG).
      - If embeddings\_configured().
        - Evaluate resolved.append(bind\_search\_attachments(session)).
    - Otherwise.
      - If tool\_doc.name equals builtin\_name(ATTACHMENT\_READ\_SLUG).
        - Evaluate resolved.append(bind\_read\_attachment(session)).
      - Otherwise.
        - If tool\_doc.name equals builtin\_name(MEMORY\_TOOL\_SLUG).
          - Evaluate resolved.append(bind\_update\_memory(self.name, session)).
        - Otherwise.
          - If tool\_doc.name equals builtin\_name(SKILL\_TOOL\_SLUG).
            - Evaluate resolved.append(bind\_load\_skill(self.name)).
          - Otherwise.
            - Evaluate resolved.append(tool\_doc.to\_tool()).
- Return resolved.

**Methods declared on this owner** [enabled tool docs](operations-022.md#op-ec7e49e8c16df8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L246) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L995) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L971)

<a id="op-91b05b585d4556"></a>
### Flow Agent.server tools

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_server_tools`

**Inputs** self.

**Declared result** list at str.

**Explicit results** list of tool\_call\_name(tool.name) for tool drawn from self.\_enabled\_tool\_docs() where tool.name belongs to daemon\_builtins.

**Local steps**

- Bind dependencies SERVER\_TOOL\_SLUGS, builtin\_name, tool\_call\_name.
- Set daemon\_builtins from set of builtin\_name(slug) for slug drawn from SERVER\_TOOL\_SLUGS.
  - Draw slug from SERVER\_TOOL\_SLUGS.
- Return list of tool\_call\_name(tool.name) for tool drawn from self.\_enabled\_tool\_docs() where tool.name belongs to daemon\_builtins.
  - Draw tool from self.\_enabled\_tool\_docs(), keep a combination only if (tool.name belongs to daemon\_builtins).

**Methods declared on this owner** [enabled tool docs](operations-022.md#op-ec7e49e8c16df8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1008) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L984)

<a id="op-f881275da57383"></a>
### Flow Agent.subagent configs

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_subagent_configs`

**Inputs** self, session, user\_context.

**Declared result** list at dict at tuple(str, Any).

**Record and data access** resolve a document from “Flow Agent” via get\_doc · read “Flow Model” via get\_value.

**Explicit results** configs.

**Explicit failure paths** validation helper — translated “Sub-agent {0} runs on Flow Model {1}, which is disabled.”.format(child.name, child.model).

**Local steps**

- Bind dependencies model\_config.
- Set configs from list().
- For each row in self.sub\_agents.
  - Set child from Platform.get\_doc(“Flow Agent”, row.agent).
  - If not child.enabled.
    - Continue with the next iteration or loop test.
  - If not Platform.db.get\_value(“Flow Model”, child.model, “enabled”).
    - Call the validation error handler Platform.throw(translated “Sub-agent {0} runs on Flow Model {1}, which is disabled.”.format(child.name, child.model), title = translated “Disabled Model”).
  - Evaluate configs.append(mapping(“name” → child.name, “description” → \_one\_line(child.description), expand model\_config(child.model, check\_permission = false), expand child.session\_tool\_config(session), …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in child.max\_iterations → DEFAULT\_MAX\_ITERATIONS.
- Return configs.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L10) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1012) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L988)
