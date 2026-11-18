# Payments and banking

English · [Afrikaans](../af/banking.md) · [Deutsch](../de/banking.md) · [简体中文](../zh-Hans/banking.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## cheque

Track each cheque from receipt or issue through clearance or return, and reconcile it with its journal and bank transaction.

**Documented workflow**

Submitting a receipt creates the customer cheque, and a deposit slip groups eligible cheques for the bank. The recovered reconciliation code looks up a deposited cheque by reference and a linked journal before recording collection or return.

**Proposed acceptance example**

The company has an active approval threshold of 1,000 and receives a cheque for exactly 1,000. Submit it, reload it in a new session and then approve it as Accounts Manager. It remains pending with no journal before approval, and approval posts exactly one journal. Arabic and English receipts use the same instrument number, approval event and monetary amount.

[Detailed profile in English](../../apps/cheque.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/cheque)

## IPCONNEX Stripe Payment

Collect a sales invoice through Stripe and reconcile the confirmed payment against its outstanding balance.

**Documented workflow**

The listing exposes a Pay Invoice action after Stripe and customer payment details are configured. In the historical public copy, collection uses the customer’s saved payment method and invoice currency, requests a Stripe PaymentIntent and builds a customer Payment Entry with an invoice allocation; this describes the copy’s path, not a verified settlement on a deployed site.

**Proposed acceptance example**

A French-speaking payer starts one collection against an English invoice with EUR 40 outstanding. Send the same collection request twice and replay the provider's successful event. One provider charge is allocated once for EUR 40; the invoice balance is zero. Receipt language does not change payer, merchant, provider reference, currency or amount.

[Detailed profile in English](../../apps/ipconnex_stripe_payment.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/ipconnex_stripe_payment)

## PDC Cheque Management

Track a post-dated cheque from receipt or issue through deposit, clearance or dishonour.

**Documented workflow**

The publisher says receiving a customer cheque or issuing one to a supplier creates a Payment Entry against the appropriate holding account. In the attributed public copy, deposit creates a bank journal and clearance records the clearing date on that journal.

**Proposed acceptance example**

One customer owes 400.00 in the company currency and pays by cheque 00072. The configured holding account starts at zero. Record the receipt, deposit it, confirm clearance, then replay the same clearing request. The invoice is allocated once, the bank increases by 400.00, the holding account returns to zero and replay creates no extra journal. The German reviewer sees the same instrument 00072, dates, amount and linked voucher IDs as the Afrikaans-speaking clerk.

[Detailed profile in English](../../apps/pdc_cheque_management.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/pdc_cheque_management)

## ProCredit Bank Statement Processing

Import a ProCredit Bosnia and Herzegovina CSV statement and review repeated transaction references before reconciliation.

**Documented workflow**

The publisher describes importing CSV statements from ProCredit Bank in Bosnia and Herzegovina and checking for repeated references. Its screenshots show a Statement Import preview with date, deposit, withdrawal, reference and description, followed by unreconciled Bank Transactions.

**Proposed acceptance example**

A configured source format uses comma decimals. An account receives reference 00038 with amount 1.234,50. Import it twice, then import a third observation of the same reference for 1.234,55. One transaction is committed, the identical observation is linked as a duplicate, and the conflicting amount goes to review. Operator language cannot alter the bank number format, original description or leading zeros in a reference.

[Detailed profile in English](../../apps/procreditbank.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/procreditbank)

## Treasury Entry

Record cash or cheque receipts and payments in a treasury and review entries tied to specific parties.

**Documented workflow**

The publisher shows a Treasury with separate payable and receivable accounts for each payment mode. On a Treasury Entry the clerk can enter account and amount rows directly or select the party-based option to retrieve outstanding invoices and enter allocations against their references.

**Proposed acceptance example**

One treasury records a party-linked cash receipt of 250.00 and a non-party cash payment of 75.00 in the same currency. Open the register in a different language, inspect the totals and apply the party-only filter. The net movement is +175.00. The party filter returns only the receipt for 250.00. Direction codes, party IDs and source amounts are independent of their translated captions.

[Detailed profile in English](../../apps/safe_entry.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/safe_entry)

## Sanpra Easypay

Authorize an ICICI supplier payment batch and reconcile each instruction with its bank response.

**Documented workflow**

The listing describes collections and disbursements through ICICI Bank. For supplier payouts the publisher describes retrieving Payment Entries, authorizing a batch with a one-time password and tracking bank transaction statuses, with support for RTGS and NEFT.

**Proposed acceptance example**

An approved two-line supplier payout batch has one bank-confirmed instruction and one rejected instruction. Process the bank response twice and issue advice for the successfully paid supplier. One confirmed payment receives one advice. The rejected item remains unpaid with its original bank reason. The Hindi operator, English approver and German-speaking recipient see localized messages for identical payment and bank identifiers.

[Detailed profile in English](../../apps/sanpra_easypay.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/sanpra_easypay)

## Stripe2 Payment Integration

Collect a payment online, through a paired terminal or against a recurring payment request, and reconcile the result with the invoice.

**Documented workflow**

After a company contact verifies their email and authorizes the Stripe account, the merchant assigns online and offline payment modes. A submitted payment request can open web checkout or use a previously saved method for a recurring collection, and a POS operator can use a registered terminal.

**Proposed acceptance example**

A submitted EUR 35.70 invoice has a French-speaking payer and a German-speaking cashier. The payer completes checkout and the provider delivers the same verified success event twice. Allocate EUR 35.70 once and show the same settled invoice on both language views. The checkout and receipt may use the payer’s language while the invoice identity and currency remain unchanged.

[Detailed profile in English](../../apps/stripe2.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/stripe2)
