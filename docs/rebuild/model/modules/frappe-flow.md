# Flow declarations in frappe

Each dictionary part contains an ordered field list, source location, record settings and grants. The source column opens the declaration at the reviewed revision.

| Record | Storage | Fields | Dictionary | Source |
|---|---|---:|---|---|
| Flow Agent | ordinary | 21 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_agent/flow_agent.json) |
| Flow Agent Knowledge Base | child | 1 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_agent_knowledge_base/flow_agent_knowledge_base.json) |
| Flow Agent Memory | ordinary | 9 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_agent_memory/flow_agent_memory.json) |
| Flow Agent Skill | child | 1 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_agent_skill/flow_agent_skill.json) |
| Flow Agent Sub Agent | child | 1 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_agent_sub_agent/flow_agent_sub_agent.json) |
| Flow Agent Tool | child | 1 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_agent_tool/flow_agent_tool.json) |
| Flow Knowledge Base | ordinary | 5 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_knowledge_base/flow_knowledge_base.json) |
| Flow Knowledge Chunk | ordinary | 9 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_knowledge_chunk/flow_knowledge_chunk.json) |
| Flow Knowledge Settings | singleton | 8 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_knowledge_settings/flow_knowledge_settings.json) |
| Flow Knowledge Source | ordinary | 24 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_knowledge_source/flow_knowledge_source.json) |
| Flow Model | ordinary | 12 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_model/flow_model.json) |
| Flow Provider | ordinary | 5 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_provider/flow_provider.json) |
| Flow Run | ordinary | 24 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_run/flow_run.json) |
| Flow Session | ordinary | 11 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_session/flow_session.json) |
| Flow Session Attachment | child | 6 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_session_attachment/flow_session_attachment.json) |
| Flow Session Message | child | 6 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_session_message/flow_session_message.json) |
| Flow Settings | singleton | 4 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_settings/flow_settings.json) |
| Flow Skill | ordinary | 10 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_skill/flow_skill.json) |
| Flow Tool | ordinary | 14 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_tool/flow_tool.json) |
| Flow Trigger | ordinary | 18 | [Part 1](../catalog/frappe-flow-01.json) | [Source](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/flow/doctype/flow_trigger/flow_trigger.json) |
