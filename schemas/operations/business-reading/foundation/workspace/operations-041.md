# Forms, reports and navigation · operations 41

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Loop

<a id="op-6f8593c3bffe40"></a>
### Agent Runner.build page context

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_build_page_context`

**Inputs** self.

**Declared result** str.

**Explicit results** empty text · formatted text Current page structure (JSON — pass a block's 'id' value as component\_id to edit it): {structure}.

**Local steps**

- Set root from self.\_page\_root().
- If root is identical to no value.
  - Return empty text.
- Set structure from BlockCodec.to\_json(BlockCodec.compress(root)).
- Return formatted text Current page structure (JSON — pass a block's 'id' value as component\_id to edit it): {structure}.

**Methods declared on this owner** [page root](operations-040.md#op-4297a01d5e1634).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L58) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1721)

<a id="op-cc62090f60d766"></a>
### Agent Runner.build messages

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_build_messages`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** messages.

**Local steps**

- Set messages from list(mapping(“role” → “system”, “content” → self.system\_prompt, “cache\_control” → mapping(“type” → “ephemeral”))).
- If page\_context\_message bound to self.build\_page\_context().
  - Evaluate messages.append(mapping(“role” → “user”, “content” → page\_context\_message, “cache\_control” → mapping(“type” → “ephemeral”))).
  - Evaluate messages.append(mapping(“role” → “assistant”, “content” → “Understood. I have the current page structure. What would you like me to change?”)).
- Evaluate messages.extend(AISession.build\_context\_messages\_from\_id(self.session\_id)).
- Set user\_text from self.prompt.
- If self.selected\_block\_ids.
  - Update user\_text using + formatted text   (User has selected: {“, ”.join(self.selected\_block\_ids)}).
- If (self.image\_url and ModelRegistry.is\_vision\_capable(self.model)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.image\_url → ModelRegistry.is\_vision\_capable(self.model).
  - Evaluate messages.append(mapping(“role” → “user”, “content” → list(mapping(“type” → “text”, “text” → user\_text), mapping(“type” → “image\_url”, “image\_url” → mapping(“url” → self.image\_url))))).
- Otherwise.
  - Evaluate messages.append(mapping(“role” → “user”, “content” → user\_text)).
- Return messages.

**Methods declared on this owner** [build page context](operations-041.md#op-6f8593c3bffe40).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L57) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1720)

<a id="op-7f44a2cf98d1e7"></a>
### Agent Runner.call tool llm

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_call_tool_llm`

**Inputs** self, messages.

**Declared result** tuple at tuple(list at dict, str, list at dict).

**Explicit results** self.stream\_tool\_round(messages).

**Explicit failure paths** propagate active failure.

**Local steps**

- For each attempt in range(STREAM\_MAX\_ATTEMPTS).
  - Attempt the following.
    - Return self.stream\_tool\_round(messages).
  - On failure (CancelledError).
    - Propagate the active failure.
  - On failure (Exception) bound to exc.
    - If (attempt equals (STREAM\_MAX\_ATTEMPTS − 1) or not llm.is\_retryable(exc)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in attempt equals (STREAM\_MAX\_ATTEMPTS − 1) → not llm.is\_retryable(exc).
      - Propagate the active failure.
    - Set backoff from (STREAM\_BACKOFF\_BASE × (2 to the power attempt)).
    - Evaluate logger.warning(“Stream round failed (attempt %d/%d): %s — retrying in %.1fs”, (attempt + 1), STREAM\_MAX\_ATTEMPTS, exc, …).
    - Evaluate self.interruptible\_sleep(backoff).

If control reaches the end, it returns no value.

**Methods declared on this owner** [stream tool round](operations-041.md#op-781202682f8cd6), [interruptible sleep](operations-040.md#op-6dce086517af83).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L59) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1722)

<a id="op-781202682f8cd6"></a>
### Agent Runner.stream tool round

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_stream_tool_round`

**Inputs** self, messages.

**Declared result** tuple at tuple(list at dict, str, list at dict).

**Explicit results** tuple(tool\_operations, content, raw\_tool\_calls).

**Explicit failure paths** CancelledError.

**Local steps**

- Set stream from llm.complete\_with\_tools(self.model, messages, self.registry.schemas(), llm.TASK\_PARAMS at “agent”, api\_key = self.api\_key, stream = true).
- Set content\_parts from list().
- Set acc from mapping().
- Set finish\_reason from no value.
- For each chunk in stream.
  - If self.is\_cancelled().
    - Attempt the following.
      - Evaluate stream.close().
    - On failure (Exception).
      - Take no action here.
    - Raise CancelledError.
  - If not chunk.choices.
    - Continue with the next iteration or loop test.
  - If fr bound to chunk.choices at 0.finish\_reason.
    - Set finish\_reason from fr.
  - Set delta from chunk.choices at 0.delta.
  - If getattr(delta, “content”, no value).
    - Evaluate content\_parts.append(delta.content).
  - For each tc in (getattr(delta, “tool\_calls”, no value) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(delta, “tool\_calls”, no value) → list().
    - Set idx from tc.index when tc.index is distinct from no value, otherwise 0.
      - Value choice on tc.index is distinct from no value — true gives tc.index, false gives 0.
    - Set entry from acc.setdefault(idx, mapping(“id” → no value, “name” → no value, “args” → empty text)).
    - If tc.id.
      - Set entry at “id” from tc.id.
    - Set fn from getattr(tc, “function”, no value).
    - If (fn and fn.name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fn → fn.name.
      - Set entry at “name” from fn.name.
    - If (fn and fn.arguments).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fn → fn.arguments.
      - Update entry at “args” using + fn.arguments.
- Set tool\_operations from list().
- Set raw\_tool\_calls from list().
- For each idx in sorted(acc).
  - Set entry from acc at idx.
  - If not entry at “name”.
    - Continue with the next iteration or loop test.
  - Set raw\_arguments from (entry at “args” or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry at “args” → empty text.
  - Set tuple(parsed, repaired) from llm.loads\_tolerant(raw\_arguments).
  - Set args from parsed when isinstance(parsed, dict), otherwise mapping().
    - Value choice on isinstance(parsed, dict) — true gives parsed, false gives mapping().
  - If parsed is identical to no value.
    - Evaluate logger.warning(“AI tool args UNPARSEABLE (tool=%s): %s”, entry at “name”, raw\_arguments at slice no value to 2000).
  - Otherwise.
    - If repaired.
      - Evaluate logger.warning(“AI tool args recovered via json\_repair (tool=%s)”, entry at “name”).
  - Evaluate tool\_operations.append(mapping(“tool\_name” → entry at “name”, “args” → args)).
  - Evaluate raw\_tool\_calls.append(mapping(“id” → entry at “id”, “type” → “function”, “function” → mapping(“name” → entry at “name”, “arguments” → raw\_arguments))).
- Set content from empty text.join(content\_parts).
- If finish\_reason equals “length”.
  - Evaluate logger.warning(“Agent LLM hit max\_tokens (finish\_reason=length) — tool args may be truncated”).
- Evaluate logger.info(“Agent LLM responded: tool\_calls=%d, has\_text=%s, finish\_reason=%s”, len(tool\_operations), bool(content), finish\_reason).
- Return tuple(tool\_operations, content, raw\_tool\_calls).

**Methods declared on this owner** [is cancelled](operations-040.md#op-d9fa1b3adf716a).

**Values supplied outside this operation** selected callable from getattr(delta, “content”, no value), getattr(delta, “tool\_calls”, no value) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L75) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1738)

<a id="op-75fd4810ca1528"></a>
### Agent Runner.describe operations

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_describe_operations`

**Inputs** operations.

**Wrappers, in declaration order** staticmethod.

**Declared result** str.

**Explicit results** “Created the page. Ask me to refine it — adjust styles, add sections, or change the layout.” · formatted text Applied {n} change{“s” when n differs from 1, otherwise empty text} to the page. · ((sentence at 0.upper() + sentence at slice 1 to no value) + “.”).

**Local steps**

- Bind dependencies Counter.
- Set counts from Counter(generator of op.get(“tool\_name”) for op drawn from operations).
  - Draw op from operations.
- Bind local operation blk for subsequent calls.
- If counts.get(“generate\_page”).
  - Return “Created the page. Ask me to refine it — adjust styles, add sections, or change the layout.”.
- Set batched from 0.
- For each op in operations.
  - If op.get(“tool\_name”) differs from “update\_blocks”.
    - Continue with the next iteration or loop test.
  - Set args from (op.get(“args”) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in op.get(“args”) → mapping().
  - Set patches from args.get(“patches”).
  - Update batched using + len(patches) when isinstance(patches, list), otherwise len((args.get(“component\_ids”) or list())).
    - Value choice on isinstance(patches, list) — true gives len(patches), false gives len((args.get(“component\_ids”) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“component\_ids”) → list().
- Set parts from list().
- If n bound to (counts.get(“update\_block”, 0) + batched).
  - Evaluate parts.append(formatted text updated {n} {blk(n)}).
- If n bound to counts.get(“add\_block”).
  - Evaluate parts.append(formatted text added {n} {blk(n)}).
- If n bound to counts.get(“remove\_block”).
  - Evaluate parts.append(formatted text removed {n} {blk(n)}).
- If n bound to counts.get(“move\_block”).
  - Evaluate parts.append(formatted text moved {n} {blk(n)}).
- If n bound to (counts.get(“bind\_prop”, 0) + counts.get(“set\_repeater\_data”, 0)).
  - Evaluate parts.append(formatted text wired {n} binding{“s” when n differs from 1, otherwise empty text}).
    - Value choice on n differs from 1 — true gives “s”, false gives empty text.
- If not parts.
  - Set n from len(operations).
  - Return formatted text Applied {n} change{“s” when n differs from 1, otherwise empty text} to the page..
    - Value choice on n differs from 1 — true gives “s”, false gives empty text.
- Set sentence from parts at 0 when len(parts) equals 1, otherwise formatted text {“, ”.join(parts at slice no value to negative 1)} and {parts at negative 1}.
  - Value choice on len(parts) equals 1 — true gives parts at 0, false gives formatted text {“, ”.join(parts at slice no value to negative 1)} and {parts at negative 1}.
- Return ((sentence at 0.upper() + sentence at slice 1 to no value) + “.”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L63) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1726)

<a id="op-d6a724e0c3a070"></a>
### Agent Runner.describe operations.blk

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_describe_operations_blk`

**Inputs** n.

**Declared result** str.

**Explicit results** “block” when n equals 1, otherwise “blocks”.

**Local steps**

- Return “block” when n equals 1, otherwise “blocks”.
  - Value choice on n equals 1 — true gives “block”, false gives “blocks”.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1727)

<a id="op-56c701706c7854"></a>
### Agent Runner.run

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_run`

**Inputs** self.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- Evaluate self.clear\_cancel\_flag().
- Set label from ModelRegistry.get\_label(self.model).
- Evaluate self.emit(“progress”, message = formatted text Thinking with {label}… when label, otherwise “Thinking…”).
  - Value choice on label — true gives formatted text Thinking with {label}…, false gives “Thinking…”.
- If (self.session\_id and AISession.is\_session\_running(self.session\_id)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.session\_id → AISession.is\_session\_running(self.session\_id).
  - Evaluate logger.warning(“AgentRunner.run: session %s already running, rejecting”, self.session\_id).
  - Evaluate self.emit(“error”, message = “Another AI request is still processing. Please wait for it to finish.”).
  - Return no value.
- Evaluate self.\_set\_running(true).
- Set messages from self.build\_messages().
- Set self.tree from WorkingTree(self.\_page\_root()).
- Set client\_operations from list().
- Set summary\_text from empty text.
- Attempt the following.
  - For each \_round in range(MAX\_ROUNDS).
    - Set tuple(tool\_operations, summary\_text, raw\_tool\_calls) from self.call\_tool\_llm(messages).
    - Set tuple(terminal\_ops, artifact\_ops, \_server\_ops, client\_ops) from self.\_classify(tool\_operations).
    - If terminal\_ops.
      - Evaluate self.handle\_terminal(terminal\_ops at 0).
      - Return no value.
    - If artifact\_ops.
      - For each op in artifact\_ops.
        - Set tool from self.registry.get(op at “tool\_name”).
        - If (tool and tool.generator).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in tool → tool.generator.
          - Set ops from tool.generator(self, op at “args”).
          - Evaluate client\_operations.extend(ops).
          - If ops.
            - Evaluate self.emit(“tool\_batch”, operations = ops).
      - Leave the innermost loop without its normal-exhaustion alternative.
    - If client\_ops.
      - Evaluate client\_operations.extend(client\_ops).
      - Evaluate self.emit(“tool\_batch”, operations = client\_ops).
    - If tool\_operations.
      - Set note from ((summary\_text or empty text).strip() or self.describe\_operations(client\_ops) when client\_ops, otherwise empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (summary\_text or empty text).strip() → self.describe\_operations(client\_ops) when client\_ops, otherwise empty text.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in summary\_text → empty text.
        - Value choice on client\_ops — true gives self.describe\_operations(client\_ops), false gives empty text.
      - If note.
        - Evaluate self.emit(“progress”, message = note).
    - If not tool\_operations.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Evaluate messages.append(mapping(“role” → “assistant”, “content” → (summary\_text or no value), “tool\_calls” → raw\_tool\_calls)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in summary\_text → no value.
    - For each tuple(tc\_dict, op) in zip(raw\_tool\_calls, tool\_operations, strict = true).
      - Set tool from self.registry.get(op at “tool\_name”).
      - If (tool and tool.side equals “server” and tool.handler).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in tool → tool.side equals “server” → tool.handler.
        - Set content from tool.handler(self, op at “args”).
      - Otherwise.
        - Set content from self.tree.apply(op at “tool\_name”, op at “args”).
        - If (“FAILED” belongs to content or “NOT FOUND” belongs to content).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in “FAILED” belongs to content → “NOT FOUND” belongs to content.
          - Evaluate logger.warning(“Client op rejected — %s: %s”, op at “tool\_name”, content).
      - Evaluate messages.append(mapping(“role” → “tool”, “tool\_call\_id” → tc\_dict at “id”, “content” → content)).
- On failure (CancelledError).
  - Evaluate self.\_emit\_cancelled().
  - Return no value.
- On failure (Exception) bound to e.
  - Evaluate logger.error(formatted text Agent LLM call failed: {e}, exc\_info = true).
  - Evaluate Platform.log\_error(formatted text Agent LLM call failed: {e}, “AgentRunner.run”).
  - Set user\_msg from “Something went wrong while building your changes. Please try again.”.
  - Evaluate AISession.try\_append\_message(self.session\_id, “assistant”, user\_msg, message\_type = “status”, metadata = mapping(“status” → “error”)).
  - Evaluate Platform.db.commit().
  - Evaluate self.emit(“error”, message = user\_msg).
  - Return no value.
- On exit, including pending return or failure.
  - Evaluate self.clear\_cancel\_flag().
  - Evaluate self.\_set\_running(false).
- If (not client\_operations and not summary\_text).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not client\_operations → not summary\_text.
  - Evaluate logger.warning(“Agent returned empty response (no tools, no text)”).
  - Evaluate self.emit(“error”, message = “The AI returned an empty response. Please try rephrasing.”).
  - Return no value.
- If not summary\_text.
  - Set summary\_text from self.describe\_operations(client\_operations).
- Evaluate self.emit(“stream”, chunk = summary\_text).
- Evaluate AISession.try\_append\_message(self.session\_id, “assistant”, (summary\_text or “Done”), message\_type = “chat”, task\_type = “agent”, metadata = mapping(“status” → “complete”, “model” → self.model, “operations” ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in summary\_text → “Done”.
- Evaluate Platform.db.commit().
- Evaluate self.emit(“complete”, message = (summary\_text or “Done”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in summary\_text → “Done”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear cancel flag](operations-040.md#op-e666ee7a0549bf), [emit](operations-040.md#op-8b8bf62345f56d), [set running](operations-041.md#op-467db5f2ccf029), [build messages](operations-041.md#op-cc62090f60d766), [page root](operations-040.md#op-4297a01d5e1634), [call tool llm](operations-041.md#op-7f44a2cf98d1e7), [classify](operations-041.md#op-16937288ce2c7e), [handle terminal](operations-041.md#op-c6fd0521d6b001), [describe operations](operations-041.md#op-75fd4810ca1528), [emit cancelled](operations-041.md#op-3cff0e10355e94).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1736)

<a id="op-16937288ce2c7e"></a>
### Agent Runner.classify

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_classify`

**Inputs** self, tool\_operations.

**Declared result** tuple at tuple(list, list, list, list).

**Explicit results** tuple(terminal\_ops, artifact\_ops, server\_ops, client\_ops).

**Local steps**

- Set tuple(terminal\_ops, artifact\_ops, server\_ops, client\_ops) from tuple(list(), list(), list(), list()).
- For each op in tool\_operations.
  - Set tool from self.registry.get(op at “tool\_name”).
  - If (tool and tool.artifact).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tool → tool.artifact.
    - Evaluate artifact\_ops.append(op).
    - Continue with the next iteration or loop test.
  - Set side from self.registry.side(op at “tool\_name”).
  - If side equals “terminal”.
    - Evaluate terminal\_ops.append(op).
  - Otherwise.
    - If side equals “server”.
      - Evaluate server\_ops.append(op).
    - Otherwise.
      - Evaluate client\_ops.append(op).
- Return tuple(terminal\_ops, artifact\_ops, server\_ops, client\_ops).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1724)

<a id="op-467db5f2ccf029"></a>
### Agent Runner.set running

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_set_running`

**Inputs** self, running.

**Declared result** no value.

**Record and data access** resolve a document from AISession.DOCTYPE via get\_doc.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- If not self.session\_id.
  - Return no value.
- Attempt the following.
  - Set session from AISession(Platform.get\_doc(AISession.DOCTYPE, self.session\_id)).
  - Evaluate session.set\_running() when running, otherwise session.clear\_running().
    - Value choice on running — true gives session.set\_running(), false gives session.clear\_running().
  - Evaluate Platform.db.commit().
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L74) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1737)

<a id="op-3cff0e10355e94"></a>
### Agent Runner.emit cancelled

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_emit_cancelled`

**Inputs** self.

**Declared result** no value.

**State and service calls** commit.

**Local steps**

- Set msg from “Cancelled.”.
- Evaluate AISession.try\_append\_message(self.session\_id, “assistant”, msg, message\_type = “status”, metadata = mapping(“status” → “cancelled”)).
- Evaluate Platform.db.commit().
- Evaluate self.emit(“complete”, message = msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [emit](operations-040.md#op-8b8bf62345f56d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L66) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1729)

<a id="op-c6fd0521d6b001"></a>
### Agent Runner.handle terminal

`operation_foundation_binding_foundation_studio_ai_agent_loop_agentrunner_handle_terminal`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, op.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L67) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1730)

<a id="op-4cbb967d552c5f"></a>
### Run agent job

`operation_foundation_binding_foundation_studio_ai_agent_loop_run_agent_job`

**Inputs** prompt, page\_context\_json, model, api\_key, remaining named values kwargs.

**Local steps**

- Evaluate AgentRunner(prompt, page\_context\_json, model, api\_key, expanded names kwargs).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L76) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1739)

## Service · Me

<a id="op-9cf1875dd4cebc"></a>
### Get context

`operation_foundation_public_pages_me_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “User” via get\_doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need to be logged in to access this page”.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Call the validation error handler Platform.throw(translated “You need to be logged in to access this page”, Platform.PermissionError).
- Set context.current\_user from Platform.get\_doc(“User”, Platform.session.user).
- Set context.show\_sidebar from false.
- Set context.is\_portal\_user from is\_portal\_user().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L6250) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L50)

## Service · Message

<a id="op-172a0fb4c7dd38"></a>
### Get context

`operation_foundation_public_pages_message_business_behavior_get_context`

**Inputs** context.

**Explicit results** message\_context.

**Local steps**

- Set message\_context from Platform.\_dict().
- If hasattr(Platform.local, “message”).
  - Set message\_context at “header” from Platform.local.message\_title.
  - Set message\_context at “title” from strip\_html\_tags(Platform.local.message\_title).
  - Set message\_context at “message” from Platform.local.message.
  - If hasattr(Platform.local, “message\_success”).
    - Set message\_context at “success” from Platform.local.message\_success.
- Otherwise.
  - If Platform.local.form\_dict.id.
    - Set message\_id from Platform.local.form\_dict.id.
    - Set key from formatted text message\_id:{message\_id}.
    - Set message from Platform.cache.get\_value(key, expires = true).
    - If message.
      - Evaluate message\_context.update(message.get(“context”, mapping())).
      - If message.get(“http\_status\_code”).
        - Set Platform.local.response at “http\_status\_code” from message at “http\_status\_code”.
- If not message\_context.title.
  - Set message\_context.title from clean\_html(Platform.form\_dict.title).
- If not message\_context.message.
  - Set message\_context.message from clean\_html(Platform.form\_dict.message).
- Return message\_context.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L6452) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L51)

## Service · Meta

<a id="op-03a218edc33dc5"></a>
### Get meta

`operation_foundation_desk_form_meta_business_behavior_get_meta`

**Inputs** doctype, cached = true.

**Declared result** “FormMeta”.

**Explicit results** meta.

**Local steps**

- Set cached from (cached and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cached → not Platform.conf.developer\_mode.
- Set key from formatted text doctype\_form\_meta::{doctype}.
- If cached.
  - Set meta from Platform.client\_cache.get\_value(key).
  - If not meta.
    - Set meta from FormMeta(doctype, cached = false).
    - Evaluate Platform.client\_cache.set\_value(key, meta).
- Otherwise.
  - Set meta from FormMeta(doctype, cached = Platform.conf.developer\_mode).
- Return meta.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L69) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L269)

<a id="op-edebcc15fc9426"></a>
### Form Meta.initialize

`operation_foundation_desk_form_meta_business_behavior_form_meta_initialize`

**Inputs** self, doctype, cached (named only, default true).

**Local steps**

- Evaluate self.\_\_dict\_\_.update(Platform.get\_meta(doctype, cached = cached).\_\_dict\_\_).
- Evaluate self.load\_assets().

If control reaches the end, it returns no value.

**Methods declared on this owner** [load assets](operations-041.md#op-fae302636a61ad).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L1580) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L258)

<a id="op-fae302636a61ad"></a>
### Form Meta.load assets

`operation_foundation_desk_form_meta_business_behavior_form_meta_load_assets`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.get(“\_\_assets\_loaded”, false).
  - Return no value.
- If not self.istable.
  - Evaluate self.add\_code().
  - Evaluate self.add\_custom\_script().
  - Evaluate self.load\_print\_formats().
  - Evaluate self.load\_workflows().
  - Evaluate self.load\_templates().
  - Evaluate self.load\_dashboard().
  - Evaluate self.load\_kanban\_meta().
- Evaluate self.set(“\_\_assets\_loaded”, true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add code](operations-041.md#op-99d5cb54f99cc2), [add custom script](operations-041.md#op-3e8c0a88159904), [load print formats](operations-042.md#op-fbc5d8eeb5eb6a), [load workflows](operations-042.md#op-e3aace1c4a9200), [load templates](operations-042.md#op-14e734223ccdd2), [load dashboard](operations-042.md#op-282ff566bd0d44), [load kanban meta](operations-042.md#op-6245e913d42fd0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L1707) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L259)

<a id="op-003c34c3c89efc"></a>
### Form Meta.as dict

`operation_foundation_desk_form_meta_business_behavior_form_meta_as_mapping`

**Inputs** self, no\_nulls = false, parenttype = no value.

**Explicit results** d.

**Local steps**

- Set d from super().as\_dict(no\_nulls = no\_nulls).
- Set \_\_dict from self.\_\_dict\_\_.
- For each k in ASSET\_KEYS.
  - Set d at k from \_\_dict.get(k).
- Set d at “masked\_fields” from list of df.fieldname for df drawn from self.get\_masked\_fields(parenttype = parenttype).
  - Draw df from self.get\_masked\_fields(parenttype = parenttype).
- Return d.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L1960) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L257)

<a id="op-99d5cb54f99cc2"></a>
### Form Meta.add code

`operation_foundation_desk_form_meta_business_behavior_form_meta_add_code`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.custom.
  - Return no value.
- Set path from os.path.join(get\_module\_path(self.module), “doctype”, scrub(self.name)).
- Bind local operation \_get\_path for subsequent calls.
- Set system\_country from Platform.get\_system\_settings(“country”).
- Evaluate self.\_add\_code(\_get\_path((self.name + “.js”)), “\_\_js”).
- If system\_country.
  - Evaluate self.\_add\_code(\_get\_path(os.path.join(“regional”, (system\_country + “.js”))), “\_\_js”).
- Evaluate self.\_add\_code(\_get\_path((self.name + “.css”)), “\_\_css”).
- Evaluate self.\_add\_code(\_get\_path((self.name + “\_list.js”)), “\_\_list\_js”).
- If system\_country.
  - Evaluate self.\_add\_code(\_get\_path(os.path.join(“regional”, (system\_country + “\_list.js”))), “\_\_list\_js”).
- Evaluate self.\_add\_code(\_get\_path((self.name + “\_kanban.js”)), “\_\_kanban\_js”).
- Evaluate self.\_add\_code(\_get\_path((self.name + “\_calendar.js”)), “\_\_calendar\_js”).
- Evaluate self.\_add\_code(\_get\_path((self.name + “\_tree.js”)), “\_\_tree\_js”).
- Set listview\_template from \_get\_path((self.name + “\_list.html”)).
- If os.path.exists(listview\_template).
  - Evaluate self.set(“\_\_listview\_template”, get\_html\_format(listview\_template)).
- Evaluate self.add\_code\_via\_hook(“doctype\_js”, “\_\_js”).
- Evaluate self.add\_code\_via\_hook(“doctype\_list\_js”, “\_\_list\_js”).
- Evaluate self.add\_code\_via\_hook(“doctype\_kanban\_js”, “\_\_kanban\_js”).
- Evaluate self.add\_code\_via\_hook(“doctype\_tree\_js”, “\_\_tree\_js”).
- Evaluate self.add\_code\_via\_hook(“doctype\_calendar\_js”, “\_\_calendar\_js”).
- Evaluate self.add\_html\_templates(path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add code](operations-041.md#op-d33565c4e14186), [add code via hook](operations-041.md#op-b3584f2facb57d), [add html templates](operations-041.md#op-d7720b2494c141).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“country”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L66) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L251)

<a id="op-ee329b20e8431b"></a>
### Form Meta.add code.get path

`operation_foundation_desk_form_meta_business_behavior_form_meta_add_code_get_path`

**Inputs** fname.

**Explicit results** os.path.join(path, scrub(fname)).

**Local steps**

- Return os.path.join(path, scrub(fname)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L3111) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L253)

<a id="op-d33565c4e14186"></a>
### Form Meta.add code

`operation_foundation_desk_form_meta_business_behavior_form_meta_add_code_2`

**Inputs** self, path, fieldname.

**Local steps**

- Set js from get\_js(path).
- If js.
  - Set bench\_path from (get\_bench\_path() + “/”).
  - Set asset\_path from path.replace(bench\_path, empty text).
  - Set comment from formatted text   /\* Adding {asset\_path} \*/.
  - Set sourceURL from formatted text   //# sourceURL={(scrub(self.name) + fieldname)}.
  - Evaluate self.set(fieldname, ((((nested operand in the contract.get(fieldname) or empty text) + comment) + js) + sourceURL)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(fieldname) → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L3188) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L252)

<a id="op-d7720b2494c141"></a>
### Form Meta.add html templates

`operation_foundation_desk_form_meta_business_behavior_form_meta_add_document_markup_templates`

**Inputs** self, path.

**Explicit results** no value.

**Local steps**

- If self.custom.
  - Return no value.
- Bind dependencies scrub\_html\_template.
- Set templates from dict().
- For each fname in os.listdir(path).
  - If fname.endswith(“.html”).
    - Within open(os.path.join(path, fname), encoding = “utf-8”) bound as f.
      - Set templates at fname.split(“.”, 1) at 0 from scrub\_html\_template(f.read()).
- Evaluate self.set(“\_\_templates”, (templates or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in templates → no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L3501) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1774) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L256)

<a id="op-b3584f2facb57d"></a>
### Form Meta.add code via hook

`operation_foundation_desk_form_meta_business_behavior_form_meta_add_code_via_hook`

**Inputs** self, hook, fieldname.

**Local steps**

- For each path in get\_code\_files\_via\_hooks(hook, self.name).
  - Evaluate self.\_add\_code(path, fieldname).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add code](operations-041.md#op-d33565c4e14186).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L3816) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L254)

<a id="op-3e8c0a88159904"></a>
### Form Meta.add custom script

`operation_foundation_desk_form_meta_business_behavior_form_meta_add_custom_script`

**Inputs** self.

**Record and data access** read “Client Script” via get\_all.

**Local steps**

- Set client\_scripts from (Platform.get\_all(“Client Script”, filters = mapping(“dt” → self.name, “enabled” → 1), fields = list(“name”, “script”, “view”), order\_by = “creation asc”) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Client Script”, filters = mapping(“dt” → self.name, “enabled” → 1), fields = list(“name”, “script”, “view”), order\_by = “creation asc”) → empty text.
- Set list\_script from empty text.
- Set form\_script from empty text.
- For each script in client\_scripts.
  - If not script.script.
    - Continue with the next iteration or loop test.
  - If script.view equals “List”.
    - Update list\_script using + formatted text  // {script.name} {script.script}.
  - Otherwise.
    - If script.view equals “Form”.
      - Update form\_script using + formatted text  // {script.name} {script.script}.
- Set file from scrub(self.name).
- Update form\_script using + formatted text   //# sourceURL={file}\_\_custom\_js.
- Update list\_script using + formatted text   //# sourceURL={file}\_\_custom\_list\_js.
- Evaluate self.set(“\_\_custom\_js”, form\_script).
- Evaluate self.set(“\_\_custom\_list\_js”, list\_script).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L67) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L255)
