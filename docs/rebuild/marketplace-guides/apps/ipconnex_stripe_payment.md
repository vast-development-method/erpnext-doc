# IPCONNEX Stripe Payment

[Business workflow and acceptance cases](../../../capabilities/guides/banking.md#saved-payment-method-collections).

## Publisher and recovered source evidence

IPCONNEX describes a version 14 integration that collects Sales Invoice payments. The listing names Payment Method, Stripe Settings, SIP Subscription and SIP Server. Once configured, the user can invoke Pay Invoice. A public copy identifies the same app and IPCONNEX authorship, but refers to different customer, card and subscription records. Keep the two field inventories versioned independently. [Marketplace documentation](https://cloud.frappe.io/marketplace/apps/ipconnex_stripe_payment) · [Listed repository](https://github.com/IPCONNEX-Services/IPCONNEX-Stripe-Payment) · [Copy identity and event registration](https://github.com/EDSTeam/IPCONNEX-Stripe-Payment/blob/c3c96a2761f97c871898a3b7be23fcbbb91f70af/ipconnex_stripe_payment/hooks.py)

In that copy, Sales Invoice and Sales Order submission have hooks, and two collection/subscription handlers are registered on an hourly schedule. The interactive collection path loads the Stripe customer, configured cards and settlement account. It tests invoice status, uses the outstanding amount (capped at grand total when rounded totals are disabled), multiplies by 100 and requests a confirmed PaymentIntent in the invoice currency. It constructs a customer Payment Entry with an invoice allocation, provider reference and unit exchange rates. Optional email uses a configured template and creates a Communication entry. These observations describe one historical path; its amount conversion and event handling require explicit qualification for any currency or payment flow. [Collection and allocation in the recovered copy](https://github.com/EDSTeam/IPCONNEX-Stripe-Payment/blob/c3c96a2761f97c871898a3b7be23fcbbb91f70af/ipconnex_stripe_payment/ipconnex_stripe_payment/payement.py#L201)

## Proposed rebuild contract

Persist a collection attempt with invoice ID, payer, merchant account, invoice currency, outstanding decimal amount, payment-method token and idempotency key. Recheck the customer’s authority to pay this invoice and the current balance. Derive provider units according to the provider’s currency-specific rules. A redirect or successful API call alone cannot settle an invoice. Record the provider state, confirm the final paid amount/currency, and reconcile one confirmed charge to one ERP payment allocation. If recording fails after collection, resume reconciliation against the existing provider reference. A new charge is a separate business action. [Provider intent lifecycle](https://docs.stripe.com/api/payment_intents) · [Provider event delivery](https://docs.stripe.com/webhooks)

## Multilingual operation and acceptance

- A French-speaking payer pays an English invoice with EUR 40 outstanding. Two clicks and a duplicate success event yield one provider charge and one EUR 40 allocation. An Afrikaans clerk can locate the same provider reference. Deliver the receipt using the payer’s effective language and retain the rendered copy.
- A pending authorization shows translated status text. The invoice stays open until reconciled success. A later decline displays a localizable reason and records the failed attempt without reducing outstanding.
- An invoice for JPY 900 requires 900 provider units. Switching to a German UI cannot turn this into 90,000 units. Use an explicit currency code even if the recipient’s language convention uses the same symbol for another currency. [Provider currency units](https://docs.stripe.com/currencies#zero-decimal)
- Locale fallback may alter the receipt wording. It cannot select a different merchant, card, currency, exchange rate or posting date.

## Remaining evidence

The exact publisher revision, SIP linkage, subscription migration, card authorization lifecycle and installed multilingual templates remain open. The public copy and the newer publisher product named erpnext-stripe have distinct technical identities; neither proves which implementation is installed from this card.
