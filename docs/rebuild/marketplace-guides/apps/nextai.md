# ChatNext

[Business workflow and acceptance cases](../../../capabilities/guides/data.md#multilingual-business-record-questions).

Hybrowlabs Technologies lists a closed-beta assistant for versions 13, 14 and nightly. Users ask questions about modules such as buying, sales, stock, HR and accounts. The publisher describes contextual replies and proactive guidance. Its listing places workflow automation, analytics, voice commands and third-party integrations on its roadmap. Those statements describe the advertised beta, independent of what later source copies contain. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/nextai)

A public copy under a separate owner identifies the application as `nextai` and the publisher as Hybrowlabs. Its conversation handler stores a user message with a session and channel, passes the message, history, route context, user and site information to a separate service, stores a bot reply and returns its identifier. A microapp translation child record stores a language code, default flag and translation dictionary. Those records concern microapp strings. Their presence does not demonstrate language coverage or translation accuracy of generated answers. The remote service implementation and the exact marketplace build remain unverified. [Copy manifest](https://github.com/badal8381/chatnext/blob/8b230e6c75ae40f7df908d1d0a87bd167b7e8f5d/nextai/hooks.py) · [Conversation handler](https://github.com/badal8381/chatnext/blob/8b230e6c75ae40f7df908d1d0a87bd167b7e8f5d/nextai/chatapi/chat.py) · [Translation record](https://github.com/badal8381/chatnext/blob/8b230e6c75ae40f7df908d1d0a87bd167b7e8f5d/nextai/nextai/doctype/cn_microapp_translation/cn_microapp_translation.json)

## Proposed rebuild contract

The nominal publisher repository and the inspectable public copy have different owners. A verified upstream release, supported answer-language matrix, data-retention agreement and authorized-provider configuration are still needed to qualify a deployment. [Named app repository](https://github.com/chromonav/chatnext)

[Read the consolidated workflow](../../../capabilities/guides/data.md#multilingual-business-record-questions-1).
