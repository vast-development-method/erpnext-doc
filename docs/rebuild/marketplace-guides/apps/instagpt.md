# InstaGPT

## Publisher evidence

Brandimic lists version 14. A System Manager or Administrator selects a model and temperature and enters an OpenAI key in InstaGPT Settings. The documented input range is 0–200. Staff open a chat window from the navigation bar anywhere in the framework. The described shortcuts start a chat (Ctrl+I), send a message (Enter) and close the window (Escape). The listing names Frappe as a dependency and describes version 13 as planned. [Marketplace configuration and user guide](https://cloud.frappe.io/marketplace/apps/instagpt) · [Listed source](https://github.com/Brandimic0/instagpt)

## Provider parameter

OpenAI documents a sampling temperature range of 0–2 for its Chat Completions request parameter. The listing’s 0–200 control and the provider parameter therefore cannot be passed through numerically across their entire advertised ranges. No public configuration or request trace examined establishes the adapter’s scale, endpoint or model-specific handling. The publisher’s linked configuration image could not be retrieved. [Provider parameter definition](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)

## Proposed rebuild contract

Give the administrator a write-only credential setting, a model selection and model-specific validation. Record both the administrator-facing temperature scale and the mapping accepted by the selected adapter. The listing does not establish what numeric transformation the original used. An ordinary user obtains only the effective availability of chat.

A chat session belongs to a tenant and actor. Sending a turn requires that session ID, client message ID, ordered user text and an optional response-language preference. Track pending, completed or failed delivery on that turn. Store the provider response separately from the input so a retry cannot overwrite what the user wrote. Restrict any retained history to the owner or an expressly authorized role. Switching pages or closing the window preserves the chosen session until the explicit new-chat action or the site's configured expiry. Opening a record must not implicitly transmit its content to the provider.

## Multilingual operation and acceptance

- A German-speaking employee opens the panel from an Afrikaans invoice, types a message in Chinese and requests an English answer. Send the original Chinese string with the explicit output-language preference. Interface labels remain German and the invoice contents stay outside the request. Record the actual response text regardless of the language the provider returns.
- While a user is composing a Chinese character through an input method editor, Enter confirms that character. Only the subsequent send action creates the message. Escape dismisses the panel without recording a second turn.
- If the provider rejects a model or times out, show a translated explanation keyed to a stable failure code. Retain the user’s draft or failed message for explicit retry. A repeated client message ID returns its existing result once a successful response is recorded.
- A missing chat-label translation falls back to the configured interface language. Previously submitted messages keep their original wording when the UI changes to a right-to-left language.

## Remaining evidence

Persistence between sessions, provider data scope, locale catalogs, shortcuts on different platforms and the temperature conversion require a versioned release or authorized runtime replay. The behavioural guarantees above apply to the rebuild.
