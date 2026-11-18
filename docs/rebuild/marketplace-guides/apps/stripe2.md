# Stripe2 Payment Integration

Case Solved lists this integration for ERPNext 14 and describes point-of-sale support after 14.16.0. Its public, revision-pinned support manual includes setup and payment procedures. The support repository identifies the product as proprietary. It supplies documentation and a terminal screenshot. The listed implementation revision and the version running for any merchant remain unverified. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/stripe2) · [Publisher manual](https://github.com/CaseSolvedUK/stripe2-support/blob/7692ed58b6c552657268d2cce5378e6f04dc1306/README.md)

## Published workflow

A company designates a responsible system user with a Contact and email address. The administrator links that contact and company in Stripe2 Settings, selects test or live operation, verifies the address and authorizes the Stripe account. The merchant then distinguishes online and offline modes of payment. A submitted Payment Request against a commercial document can generate a checkout URL. The customer completes checkout, with completion immediate or reported later. A recurring transaction uses an auto-repeat reference and a previously saved method. A terminal sale uses a POS Profile, location and paired reader. Each channel can involve a different person operating the interface. [Publisher setup and payment procedures](https://github.com/CaseSolvedUK/stripe2-support/blob/7692ed58b6c552657268d2cce5378e6f04dc1306/README.md)

## Replacement contract

| Operation | Inputs and authority | Result and exception |
|---|---|---|
| Prepare collection | Company-authorized cashier, submitted request ID, mode, amount and currency from the request | Return hosted checkout, recurring attempt or paired terminal reference. Reject a test/live or company/reader mismatch before collecting. |
| Apply collection | Verified event for the connected account, provider transaction reference, amount, currency and request | Store its disposition; post and allocate exactly once on confirmed success. An incomplete or delayed method remains pending. A mismatch goes to reconciliation. |
| Notify payer | Settled request, recorded recipient and preferred document language | Render the receipt and optional document copy in that language. Retain version, reference and delivery disposition. A failed notification leaves settlement intact. |

The customer's chosen checkout language, the cashier's interface language and the recipient's receipt language are independent. Translate labels, descriptions and dates for the audience. Keep payment mode IDs, provider references and invoice currency stable. An unsupported checkout language resolves to a declared provider-supported fallback and is recorded separately from the requested locale. [Checkout Session parameters](https://docs.stripe.com/api/checkout/sessions/create) · [Stripe event handling](https://docs.stripe.com/webhooks)

## Acceptance examples

- A German-speaking cashier opens online collection for a French-speaking payer's EUR 35.70 invoice. Checkout shows the selected supported French locale. Two copies of the same success event yield one EUR 35.70 allocation. Retrieve the document in German and the same invoice reference and balance remain visible.
- A saved recurring method requires customer action. Preserve the open request, provide the payer with a localized action prompt, and issue the paid receipt only after confirmation.
- A terminal registered for a second company or a webhook carrying a different currency cannot settle the request. The operator sees a translated reason and the reconciliation record retains the original currency and event reference.

The public material does not establish fee postings, refund allocations, chargeback processing, subscription failure policy or the installed translation catalog. Verify these with a versioned test installation and provider test events before claiming parity.
