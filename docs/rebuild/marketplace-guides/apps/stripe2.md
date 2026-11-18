# Stripe2 Payment Integration

[Business workflow and acceptance cases](../../../capabilities/guides/banking.md#online-and-terminal-payment-collection).

Case Solved lists this integration for ERPNext 14 and describes point-of-sale support after 14.16.0. Its public, revision-pinned support manual includes setup and payment procedures. The support repository identifies the product as proprietary. It supplies documentation and a terminal screenshot. The listed implementation revision and the version running for any merchant remain unverified. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/stripe2) · [Publisher manual](https://github.com/CaseSolvedUK/stripe2-support/blob/7692ed58b6c552657268d2cce5378e6f04dc1306/README.md)

## Published workflow

A company designates a responsible system user with a Contact and email address. The administrator links that contact and company in Stripe2 Settings, selects test or live operation, verifies the address and authorizes the Stripe account. The merchant then distinguishes online and offline modes of payment. A submitted Payment Request against a commercial document can generate a checkout URL. The customer completes checkout, with completion immediate or reported later. A recurring transaction uses an auto-repeat reference and a previously saved method. A terminal sale uses a POS Profile, location and paired reader. Each channel can involve a different person operating the interface. [Publisher setup and payment procedures](https://github.com/CaseSolvedUK/stripe2-support/blob/7692ed58b6c552657268d2cce5378e6f04dc1306/README.md)

## Replacement contract

The customer's chosen checkout language, the cashier's interface language and the recipient's receipt language are independent. Translate labels, descriptions and dates for the audience. Keep payment mode IDs, provider references and invoice currency stable. An unsupported checkout language resolves to a declared provider-supported fallback and is recorded separately from the requested locale. [Checkout Session parameters](https://docs.stripe.com/api/checkout/sessions/create) · [Stripe event handling](https://docs.stripe.com/webhooks)

[Read the consolidated workflow](../../../capabilities/guides/banking.md#online-and-terminal-payment-collection-2).

## Acceptance examples

The public material does not establish fee postings, refund allocations, chargeback processing, subscription failure policy or the installed translation catalog. Verify these with a versioned test installation and provider test events before claiming parity.

[Read the consolidated acceptance cases](../../../capabilities/guides/banking.md#online-and-terminal-payment-collection-3).
