# Payments and banking

English · [Afrikaans](../af/banking.md) · [Deutsch](../de/banking.md) · [简体中文](../zh-Hans/banking.md)

[All topics](README.md)

## cheque

Submitting a receipt creates the customer cheque, and a deposit slip groups eligible cheques for the bank. The recovered reconciliation code looks up a deposited cheque by reference and a linked journal before recording collection or return.

[Workflow and acceptance](../../../../capabilities/guides/banking.md#cheque-approval-and-collection) · [Source observations](../../apps/cheque.md)

## IPCONNEX Stripe Payment

The listing exposes a Pay Invoice action after Stripe and customer payment details are configured. In the historical public copy, collection uses the customer’s saved payment method and invoice currency, requests a Stripe PaymentIntent and builds a customer Payment Entry with an invoice allocation; this describes the copy’s path, not a verified settlement on a deployed site.

[Workflow and acceptance](../../../../capabilities/guides/banking.md#saved-payment-method-collections) · [Source observations](../../apps/ipconnex_stripe_payment.md)

## PDC Cheque Management

The publisher says receiving a customer cheque or issuing one to a supplier creates a Payment Entry against the appropriate holding account. In the attributed public copy, deposit creates a bank journal and clearance records the clearing date on that journal.

[Workflow and acceptance](../../../../capabilities/guides/banking.md#post-dated-cheque-settlement) · [Source observations](../../apps/pdc_cheque_management.md)

## ProCredit Bank Statement Processing

The publisher describes importing CSV statements from ProCredit Bank in Bosnia and Herzegovina and checking for repeated references. Its screenshots show a Statement Import preview with date, deposit, withdrawal, reference and description, followed by unreconciled Bank Transactions.

[Workflow and acceptance](../../../../capabilities/guides/banking.md#bank-statement-import-and-duplicate-review) · [Source observations](../../apps/procreditbank.md)

## Treasury Entry

The publisher shows a Treasury with separate payable and receivable accounts for each payment mode. On a Treasury Entry the clerk can enter account and amount rows directly or select the party-based option to retrieve outstanding invoices and enter allocations against their references.

[Workflow and acceptance](../../../../capabilities/guides/banking.md#treasury-transaction-register) · [Source observations](../../apps/safe_entry.md)

## Sanpra Easypay

The listing describes collections and disbursements through ICICI Bank. For supplier payouts the publisher describes retrieving Payment Entries, authorizing a batch with a one-time password and tracking bank transaction statuses, with support for RTGS and NEFT.

[Workflow and acceptance](../../../../capabilities/guides/banking.md#supplier-payment-batch-authorization) · [Source observations](../../apps/sanpra_easypay.md)

## Stripe2 Payment Integration

After a company contact verifies their email and authorizes the Stripe account, the merchant assigns online and offline payment modes. A submitted payment request can open web checkout or use a previously saved method for a recurring collection, and a POS operator can use a registered terminal.

[Workflow and acceptance](../../../../capabilities/guides/banking.md#online-and-terminal-payment-collection) · [Source observations](../../apps/stripe2.md)
