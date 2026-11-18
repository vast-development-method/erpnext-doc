# Workflow, automation and dispatch · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Flow agent

<a id="op-5d3e4a68759ffe"></a>
### Flow Agent.session tool config

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_session_tool_config`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, session.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L7) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1009) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L985)

<a id="op-28f0cb46ac79f6"></a>
### Flow Agent.render instructions

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_render_instructions`

**Inputs** self.

**Declared result** str.

**Explicit results** get\_jenv().from\_string((self.instructions or empty text)).render(context).

**Explicit failure paths** validation helper — translated “Could not fill in the instructions: {0}. To keep Jinja as plain text, wrap it in {1}.”.format(str(e).rstrip(“.”), “{% raw %}…{% endraw %}”).

**Local steps**

- Set user from Platform.session.user.
- Set context from mapping(“user” → user, “full\_name” → get\_fullname(user), “today” → today()).
- Attempt the following.
  - Within safe\_render\_flags().
    - Return get\_jenv().from\_string((self.instructions or empty text)).render(context).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.instructions → empty text.
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Could not fill in the instructions: {0}. To keep Jinja as plain text, wrap it in {1}.”.format(str(e).rstrip(“.”), “{% raw %}…{% endraw %}”), title = translated “Invalid Instructions”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L4) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1006) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L982)

<a id="op-0d93ea9833b492"></a>
### Flow Agent.extension tools

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_extension_tools`

**Inputs** self.

**Declared result** list at str.

**Explicit results** list of tool.name for tool drawn from self.\_enabled\_tool\_docs() where tool.type equals “Server”.

**Local steps**

- Return list of tool.name for tool drawn from self.\_enabled\_tool\_docs() where tool.type equals “Server”.
  - Draw tool from self.\_enabled\_tool\_docs(), keep a combination only if (tool.type equals “Server”).

**Methods declared on this owner** [enabled tool docs](operations-022.md#op-ec7e49e8c16df8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L251) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1000) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L976)

<a id="op-7480dd54b2a221"></a>
### Flow Agent.has tool

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_has_tool`

**Inputs** self, name.

**Declared result** bool.

**Explicit results** any(generator of tool\_doc.name equals name for tool\_doc drawn from self.\_enabled\_tool\_docs()).

**Local steps**

- Return any(generator of tool\_doc.name equals name for tool\_doc drawn from self.\_enabled\_tool\_docs()).
  - Draw tool\_doc from self.\_enabled\_tool\_docs().

**Methods declared on this owner** [enabled tool docs](operations-022.md#op-ec7e49e8c16df8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L252) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1001) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L977)

<a id="op-ec7e49e8c16df8"></a>
### Flow Agent.enabled tool docs

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_enabled_tool_docs`

**Inputs** self.

**Record and data access** resolve a document from “Flow Tool” via get\_doc.

**Local steps**

- For each row in self.tools.
  - Attempt the following.
    - Set tool\_doc from Platform.get\_doc(“Flow Tool”, row.tool).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.log\_error(title = formatted text Flow Agent {self.name}: tool {row.tool} not found, skipping).
    - Continue with the next iteration or loop test.
  - If tool\_doc.enabled.
    - yield tool\_doc.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L247) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L996) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L972)

<a id="op-666a4840d16530"></a>
### Flow Agent.skill index

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_skill_index`

**Inputs** self.

**Declared result** str.

**Explicit results** empty text · formatted text   &lt;available\_skills&gt; {SKILL\_INDEX\_LEAD} {entries} &lt;/available\_skills&gt;.

**Local steps**

- Set rows from self.visible\_skills(“description”).
- If not rows.
  - Return empty text.
- Set entries from whitespace '\\n'.join(generator of formatted text   &lt;skill&gt;     &lt;name&gt;{\_escape(row.name)}&lt;/name&gt;     &lt;description&gt;{\_escape(\_one\_line(row.description))}&lt;/description&gt;   &lt;/skill&gt; for row drawn from rows).
  - Draw row from rows.
- Return formatted text   &lt;available\_skills&gt; {SKILL\_INDEX\_LEAD} {entries} &lt;/available\_skills&gt;.

**Methods declared on this owner** [visible skills](operations-022.md#op-a7dea558ba6406).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L8) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1010) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L986)

<a id="op-a7dea558ba6406"></a>
### Flow Agent.visible skills

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_visible_skills`

**Inputs** self, remaining positional values fields.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** list() · self.\_skills(fields).

**Local steps**

- Bind dependencies SKILL\_TOOL\_SLUG, builtin\_name.
- If not any(generator of row.tool equals builtin\_name(SKILL\_TOOL\_SLUG) for row drawn from self.tools).
  - Draw row from self.tools.
  - Return list().
- Return self.\_skills(fields).

**Methods declared on this owner** [skills](operations-022.md#op-70791d3689426f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L16) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1018) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L994)

<a id="op-4dc34a25fb69a4"></a>
### Flow Agent.invocable skills

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_invocable_skills`

**Inputs** self.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** list of mapping(expand row, “command” → skill\_command(row.name)) for row drawn from self.\_skills(tuple(“description”), user\_invocable = 1).

**Local steps**

- Bind dependencies skill\_command.
- Return list of mapping(expand row, “command” → skill\_command(row.name)) for row drawn from self.\_skills(tuple(“description”), user\_invocable = 1).
  - Draw row from self.\_skills(tuple(“description”), user\_invocable = 1).

**Methods declared on this owner** [skills](operations-022.md#op-70791d3689426f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L253) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1002) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L978)

<a id="op-70791d3689426f"></a>
### Flow Agent.skills

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_skills`

**Inputs** self, fields, remaining named values filters.

**Declared result** list at dict at tuple(str, Any).

**Record and data access** read “Flow Skill” via get\_all.

**Explicit results** Platform.get\_all(“Flow Skill”, filters = mapping(“enabled” → 1, expand filters), or\_filters = list(list(“is\_global”, “=”, 1), list(“name”, “in”, list of row.skill for row drawn from self.skills)), fields = ….

**Local steps**

- Return Platform.get\_all(“Flow Skill”, filters = mapping(“enabled” → 1, expand filters), or\_filters = list(list(“is\_global”, “=”, 1), list(“name”, “in”, list of row.skill for row drawn from self.skills)), fields = ….
  - Draw row from self.skills.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L9) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1011) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L987)

<a id="op-2091c1470d279c"></a>
### Flow Agent.new session

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_new_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, model, title, source, auto\_approve.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L254) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1003) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L979)

<a id="op-2b2a278f98176b"></a>
### Flow Agent.run

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_flowagent_run`

**Inputs** self, input, session (named only, default no value), source (named only, default “Manual”), trigger (named only, default no value), reference\_doctype (named only, default no value), reference\_name (named only, default no value), on\_complete (named only, default no value).

**Declared result** FlowRun.

**Explicit results** convo.chat(input, source = source, trigger = trigger, reference\_doctype = reference\_doctype, reference\_name = reference\_name, …).

**Local steps**

- Bind dependencies load\_session, new\_session.
- If session.
  - Set convo from load\_session(session, agent = self.name).
- Otherwise.
  - Set convo from new\_session(self, source = source).
- Return convo.chat(input, source = source, trigger = trigger, reference\_doctype = reference\_doctype, reference\_name = reference\_name, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1007) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L983)

<a id="op-0fbbe5678b58f8"></a>
### Escape

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_escape`

**Inputs** text.

**Declared result** str.

**Explicit results** escape(text, quote = false).

**Local steps**

- Return escape(text, quote = false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L241) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L990) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L966)

<a id="op-73cfe1e6e8751b"></a>
### One line

`operation_foundation_binding_foundation_flow_doctype_flow_agent_flow_agent_one_line`

**Inputs** text.

**Declared result** str.

**Explicit results** one space.join((text or empty text).split()).

**Local steps**

- Return one space.join((text or empty text).split()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in text → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1019) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L995)

## Record · Flow agent memory

<a id="op-e88ba7a9c6ebff"></a>
### Flow Agent Memory.validate

`operation_foundation_binding_foundation_flow_doctype_flow_agent_memory_flow_agent_memory_flowagentmemory_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Memory content is required.” · validation helper — translated “Keep each memory under {0} characters — split or shorten it.”.format(MAX\_CONTENT\_CHARS) · validation helper — translated “User-scoped memories must have a user.”.

**Local steps**

- Set self.content from (self.content or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.content → empty text.
- If not self.content.
  - Call the validation error handler Platform.throw(translated “Memory content is required.”, title = translated “Empty Memory”).
- If len(self.content) &gt; MAX\_CONTENT\_CHARS.
  - Call the validation error handler Platform.throw(translated “Keep each memory under {0} characters — split or shorten it.”.format(MAX\_CONTENT\_CHARS), title = translated “Memory Too Long”).
- If (self.scope equals “User” and not self.user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.scope equals “User” → not self.user.
  - Call the validation error handler Platform.throw(translated “User-scoped memories must have a user.”, title = translated “Missing User”).
- If self.scope equals “Agent”.
  - Set self.user from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1022) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L998)

<a id="op-55788e70de124f"></a>
### Flow Agent Memory.on update

`operation_foundation_binding_foundation_flow_doctype_flow_agent_memory_flow_agent_memory_flowagentmemory_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies store.
- Evaluate store.sync(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1021) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L997)

<a id="op-dbeaf688813034"></a>
### Flow Agent Memory.on trash

`operation_foundation_binding_foundation_flow_doctype_flow_agent_memory_flow_agent_memory_flowagentmemory_on_trash`

**Inputs** self.

**Local steps**

- Bind dependencies store.
- Evaluate store.remove(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0004.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1020) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L996)

## Service · Flow handlers

<a id="op-4b31fac4011519"></a>
### Relay.initialize

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_init`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.subscriptions from mapping().
- Set self.channel\_ready from mapping().
- Set self.pubsub from no value.
- Set self.listener from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L35) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1698)

<a id="op-267ccc26c2c747"></a>
### Relay.subscribe

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_subscribe`

**Inputs** self, socket, session.

The declaration is asynchronous.

**Declared result** bool.

**Explicit results** false · true.

**Explicit failure paths** propagate active failure.

**Local steps**

- If (not is\_valid\_name(session) or not await socket.has\_permission(“Flow Session”, session)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_valid\_name(session) → not await socket.has\_permission(“Flow Session”, session).
  - Return false.
- Set channel from formatted text {SESSION\_CHANNEL}{socket.site}:{session}.
- Evaluate await socket.join(channel).
- If socket.sid does not belong to socket.participants(channel).
  - Return false.
- Set entry from self.subscriptions.get(channel).
- If entry is identical to no value.
  - Set entry from Subscription(socket.site, session, socket).
  - Set entry.ready from asyncio.ensure\_future(self.listen(channel, socket.site)).
  - Set self.subscriptions at channel from entry.
- Set entry.sockets at socket.sid from socket.
- Set sessions from socket.get(“flow\_sessions”, list()).
- If session does not belong to sessions.
  - Evaluate await socket.set(“flow\_sessions”, list(expanded sessions, session)).
- Attempt the following.
  - Evaluate await asyncio.shield(entry.ready).
- On failure (Exception).
  - If self.subscriptions.get(channel) is identical to entry.
    - Remove self.subscriptions at channel.
  - Evaluate await self.release(socket, session).
  - Propagate the active failure.
- Return true.

**Methods declared on this owner** [listen](operations-022.md#op-3c9cf0b71a2984), [release](operations-022.md#op-475c9f5c78568d).

**Values supplied outside this operation** effective access from socket.has\_permission(“Flow Session”, session) · service or queued work from socket.has\_permission(“Flow Session”, session), socket.join(channel) and 3 further calls.

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L41) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1704)

<a id="op-475c9f5c78568d"></a>
### Relay.release

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_release`

**Inputs** self, socket, session.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set sessions from socket.get(“flow\_sessions”, list()).
- If session does not belong to sessions.
  - Return no value.
- Evaluate await socket.set(“flow\_sessions”, list of name for name drawn from sessions where name differs from session).
  - Draw name from sessions, keep a combination only if (name differs from session).
- Set channel from formatted text {SESSION\_CHANNEL}{socket.site}:{session}.
- Evaluate await socket.leave(channel).
- Set entry from self.subscriptions.get(channel).
- If entry is identical to no value.
  - Return no value.
- Evaluate entry.sockets.pop(socket.sid, no value).
- If entry.sockets.
  - Return no value.
- Remove self.subscriptions at channel.
- Evaluate self.channel\_ready.pop(channel, no value).
- Attempt the following.
  - Evaluate await self.pubsub.unsubscribe(channel).
- On failure (RedisError).
  - Take no action here.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from socket.get(“flow\_sessions”, list()), socket.set(“flow\_sessions”, list of name for name drawn from sessions where name differs from session) and 1 further calls.

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L38) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1701)

<a id="op-3c9cf0b71a2984"></a>
### Relay.listen

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_listen`

**Inputs** self, channel, site.

The declaration is asynchronous.

**Declared result** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set channels from list(channel, RESYNC\_ALL, (RESYNC\_SITE + site), (ACCESS\_SITE + site)).
- Set loop from asyncio.get\_running\_loop().
- Set created from mapping of name → loop.create\_future() for name drawn from channels where name does not belong to self.channel\_ready.
  - Draw name from channels, keep a combination only if (name does not belong to self.channel\_ready).
- Evaluate self.channel\_ready.update(created).
- Set waits from list of asyncio.shield(self.channel\_ready at name) for name drawn from channels.
  - Draw name from channels.
- Attempt the following.
  - If self.pubsub is identical to no value.
    - Set self.pubsub from redis\_client().pubsub().
  - Evaluate await self.pubsub.subscribe(expanded created).
  - If self.listener is identical to no value.
    - Set self.listener from asyncio.create\_task(self.run()).
  - Evaluate await asyncio.wait\_for(asyncio.gather(expanded waits), SUBSCRIBE\_TIMEOUT).
- On failure (Exception) bound to error.
  - For each tuple(name, ready) in created.items().
    - If self.channel\_ready.get(name) is identical to ready.
      - Remove self.channel\_ready at name.
    - If not ready.done().
      - Evaluate ready.set\_exception(error).
      - Evaluate ready.exception().
  - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [run](operations-022.md#op-8b33218d9051f9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L36) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1699)

<a id="op-8b33218d9051f9"></a>
### Relay.run

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_run`

**Inputs** self.

The declaration is asynchronous.

**Declared result** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set lost\_connection from false.
- While true.
  - Attempt the following.
    - Set message from await self.pubsub.get\_message(timeout = 1.0).
  - On failure (asyncio.CancelledError).
    - Propagate the active failure.
  - On failure (tuple(RedisError, OSError)) bound to error.
    - Evaluate logger.warning(“flow: redis error (%s); reconnecting”, error).
    - Set lost\_connection from true.
    - Evaluate await asyncio.sleep(RECONNECT\_DELAY).
    - Continue with the next iteration or loop test.
  - If lost\_connection.
    - Set lost\_connection from false.
    - Evaluate await self.resync(RESYNC\_ALL, “{}”).
  - If message.
    - Evaluate await self.handle(message).

If control reaches the end, it returns no value.

**Methods declared on this owner** [resync](operations-022.md#op-f9fc38459aee8c), [handle](operations-022.md#op-a32b05e53d6991).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L40) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1703)

<a id="op-a32b05e53d6991"></a>
### Relay.handle

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_handle`

**Inputs** self, message.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set channel from message at “channel”.
- If message at “type” equals “subscribe”.
  - Set ready from self.channel\_ready.get(channel).
  - If (ready and not ready.done()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ready → not ready.done().
    - Evaluate ready.set\_result(true).
  - Return no value.
- If message at “type” differs from “message”.
  - Return no value.
- Attempt the following.
  - If channel.startswith(SESSION\_CHANNEL).
    - Evaluate await self.deliver(channel, message at “data”).
  - Otherwise.
    - If channel.startswith(ACCESS\_SITE).
      - Evaluate await self.recheck(channel, message at “data”).
    - Otherwise.
      - Evaluate await self.resync(channel, message at “data”).
- On failure (Exception).
  - Evaluate logger.exception(“flow: relay failed for %s”, channel).

If control reaches the end, it returns no value.

**Methods declared on this owner** [deliver](operations-022.md#op-4a2ff02d658a01), [recheck](operations-023.md#op-38399107622f1b), [resync](operations-022.md#op-f9fc38459aee8c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1697)

<a id="op-4a2ff02d658a01"></a>
### Relay.deliver

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_deliver`

**Inputs** self, channel, data.

The declaration is asynchronous.

**Declared result** no value.

**Local steps**

- Set entry from self.subscriptions.get(channel).
- Set event from parse(data).
- If (entry and event).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry → event.
  - Evaluate await entry.emitter.emit(EVENT, event, room = channel).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L33) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1696)

<a id="op-f9fc38459aee8c"></a>
### Relay.resync

`operation_foundation_binding_foundation_realtime_flow_handlers_relay_resync`

**Inputs** self, channel, data.

The declaration is asynchronous.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set notice from parse(data).
- If notice is identical to no value.
  - Return no value.
- Set site from no value when channel equals RESYNC\_ALL, otherwise channel.removeprefix(RESYNC\_SITE).
  - Value choice on channel equals RESYNC\_ALL — true gives no value, false gives channel.removeprefix(RESYNC\_SITE).
- Set named from set(notice at “session\_ids”) when isinstance(notice.get(“session\_ids”), list), otherwise no value.
  - Value choice on isinstance(notice.get(“session\_ids”), list) — true gives set(notice at “session\_ids”), false gives no value.
- For each tuple(room, entry) in list(self.subscriptions.items()).
  - If ((site and entry.site differs from site) or (named is distinct from no value and entry.session does not belong to named)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (site and entry.site differs from site) → (named is distinct from no value and entry.session does not belong to named).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in site → entry.site differs from site.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in named is distinct from no value → entry.session does not belong to named.
    - Continue with the next iteration or loop test.
  - Evaluate await entry.emitter.emit(RESYNC, mapping(“session” → entry.session), room = room).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L39) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1702)
