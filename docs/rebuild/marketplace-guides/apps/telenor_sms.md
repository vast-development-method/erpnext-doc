# Telenor Sms

Shoaib Rehmat lists an outbound SMS integration for ERPNext 14 and 15. Its stated purpose is to send ERP-originated messages to contacts through Telenor's API. The linked Zijsoft support forum contains no published topics. Neither source specifies a request schema, national gateway, named document, trigger, encoding, delivery receipt or supported language. The documentation below defines those boundaries for a replacement. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/telenor_sms) · [Publisher support forum](https://support.zijsoft.com/forums/forum/telenor-sms/)

## Proposed sending workflow

1. A communications administrator configures a tenant-specific sender, approved destinations, provider credential reference, and the character sets and length rules verified for that account.
2. An authorized operator requests a message against a business contact. Supply the contact ID, selected verified telephone number, text or versioned template, recipient language and an operation ID. Resolve the outgoing text before enqueueing.
3. Record one dispatch with a stable identity. A worker submits the body and destination to the configured gateway. Record the provider ID on acceptance, an explicit rejection on refusal or an uncertain result if the response is lost.
4. If the contracted gateway exposes delivery reports, correlate them to the provider ID. Display “accepted by gateway” until there is evidence of handset delivery. Locate an uncertain send before retrying it. Keep credentials out of operator logs.

## Language and SMS length

Treat an operator's language and a contact's language as separate preferences. Resolve a template in the contact's exact locale, then an approved fallback. Persist the text actually sent, template revision and resolved locale under the organization's access and retention rules. Preserve names, references and Unicode characters. Estimate segments using the encoding and limits for the chosen gateway route. If a route cannot carry the result, return the character or size problem before dispatch. Any transliterated variant must be separately approved. A phone prefix alone cannot identify the language its owner reads.

## Acceptance examples

| Scenario | Expected replacement result |
|---|---|
| English-speaking operator requests an Afrikaans appointment reminder for contact C17. | Render the approved Afrikaans version, insert the correct appointment reference, and send once. The operator sees the result in English and can inspect the selected template revision. |
| A recipient's approved German SMS preserves “Jürgen”. A gateway confirms only submission. | The outbound body retains the name. Store a gateway reference and show the submitted state. Delivery remains pending confirmation. |
| A Chinese template uses characters unavailable on the configured route or exceeds its configured segment limit. | Display the localized validation reason. The gateway receives zero requests and the contact preference is preserved. |
| A response times out after submission and the operator reopens the same operation. | Show the existing uncertain result for reconciliation. An additional billable text requires a confirmed retry decision. |

A provider-approved test account, concrete route specification and test deliveries are needed to establish which receipt, segment and retry semantics the listed integration actually supports.
