# ChatNext

Hybrowlabs Technologies lists a closed-beta assistant for versions 13, 14 and nightly. Users ask questions about modules such as buying, sales, stock, HR and accounts. The publisher describes contextual replies and proactive guidance. Its listing places workflow automation, analytics, voice commands and third-party integrations on its roadmap. Those statements describe the advertised beta, independent of what later source copies contain. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/nextai)

A public copy under a separate owner identifies the application as `nextai` and the publisher as Hybrowlabs. Its conversation handler stores a user message with a session and channel, passes the message, history, route context, user and site information to a separate service, stores a bot reply and returns its identifier. A microapp translation child record stores a language code, default flag and translation dictionary. Those records concern microapp strings. Their presence does not demonstrate language coverage or translation accuracy of generated answers. The remote service implementation and the exact marketplace build remain unverified. [Copy manifest](https://github.com/badal8381/chatnext/blob/8b230e6c75ae40f7df908d1d0a87bd167b7e8f5d/nextai/hooks.py) · [Conversation handler](https://github.com/badal8381/chatnext/blob/8b230e6c75ae40f7df908d1d0a87bd167b7e8f5d/nextai/chatapi/chat.py) · [Translation record](https://github.com/badal8381/chatnext/blob/8b230e6c75ae40f7df908d1d0a87bd167b7e8f5d/nextai/nextai/doctype/cn_microapp_translation/cn_microapp_translation.json)

## Proposed rebuild contract

Accept a question, private conversation ID, message ID, requested response language and optional record or workspace reference. Check access to that conversation and any business context before materializing history or forwarding context to a provider. Record only the approved disclosure scope. A successful answer records the original message, answer text, generated language, sources when available and provider outcome. An unavailable service leaves the message in a retryable state. A retry with the same message ID must attach to the original turn.

Keep the user's original words, document names and quoted excerpts. Store answer translations as derivatives tied to the original. Render navigation labels, language names and errors from a catalog. Distinguish the language used to ask a question from the language requested for its answer. Define unsupported-language and missing-source outcomes. Advice about a form should never itself post or approve that form.

| Proposed acceptance case | Expected result |
|---|---|
| A German UI user asks in Afrikaans how to locate the outstanding amount for an invoice they may read, and requests an Afrikaans answer. | The response is in Afrikaans, names the correct invoice and identifies the source field. The invoice remains unchanged and the original question is retained. |
| A question refers to an employee record outside the user's HR scope. | The provider receives no restricted employee data or history and the user receives a localized access response. |
| A provider times out and the same message is retried. | One visible user turn remains. Its status resolves to an answer or a localized failure without duplicating conversation entries. |

The nominal publisher repository and the inspectable public copy have different owners. A verified upstream release, supported answer-language matrix, data-retention agreement and authorized-provider configuration are still needed to qualify a deployment. [Named app repository](https://github.com/chromonav/chatnext)
