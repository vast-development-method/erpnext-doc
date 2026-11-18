# Invoices, tax and accounting

English · [Afrikaans](../af/accounting.md) · [Deutsch](../de/accounting.md) · [简体中文](../zh-Hans/accounting.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## E Invoice Egypt

Submit Egyptian electronic invoices and track the tax authority’s validation result for each document.

**Documented workflow**

The publisher offers single and bulk operations for invoices, credit notes, debit notes, cancellation and validation. The Egyptian Tax Authority’s interface returns accepted and rejected members of a submission separately, with final validation following the initial acknowledgement.

**Proposed acceptance example**

One signed submission contains invoice INV-001 and invoice INV-002. The test provider returns 202 with an external ID for INV-001 and a structure error for INV-002. Only INV-001 awaits final validation. INV-002 is flagged for correction. Neither is recorded as finally approved. Arabic and German views preserve both internal IDs, the official error code and the exact signed request.

[Detailed profile in English](../../apps/e_invoice.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/e_invoice)

## Forward Contract

Allocate a bank forward contract to payments and record the gain or loss when unused units are cancelled.

**Documented workflow**

The publisher guide attaches partial or multiple forward allocations to a payment. A preserved FinByz-attributed controller credits exchange gains and debits the bank on a profitable cancellation.

**Proposed acceptance example**

An export contract sells USD 1,000 at 17.50 NAD/USD and USD 600 has been utilized. The operator cancels USD 100 at 17.20 NAD/USD, with no fees. USD 300 remains and a NAD 30 gain balances a NAD 30 bank debit. Currency pair, quote direction, allocations and journal amounts survive a language change.

[Detailed profile in English](../../apps/forward_contract.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/forward_contract)

## AI Invoice Importer

Extract an invoice from a PDF and check the party, date, currency and line amounts before creating a draft.

**Documented workflow**

IPCONNEX describes extraction of PDF invoice data with ChatGPT. In the pinned public copy, the clerk chooses purchase or sales and supplies a PDF; the importer compares the header amount against calculated line amounts and can create the corresponding Purchase Invoice or Sales Invoice with the source file attached.

**Proposed acceptance example**

The German PDF shows 18.11.2026 and a single EUR 1.234,50 line; the clerk works in English. Extract, review and confirm the same import twice. One linked draft has the date 2026-11-18 and amount EUR 1234.50, with its source available for review. Changing the review language preserves source strings, party identity, canonical date and decimal value.

[Detailed profile in English](../../apps/ipconnex_ai_invoice.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/ipconnex_ai_invoice)

## PAV

Post an employee advance and reconcile its return in the Yemen localization using the auditor’s preferred language.

**Documented workflow**

The Yemen listing covers employee advances and accounting and attendance reports. In a public historical copy, submitting a normal advance debits the designated account and credits the funding account, while a return exchanges the two entries.

**Proposed acceptance example**

An advance is 100 transaction units at 2 company units per unit, with matching account setup. Finance submits the advance and records a full return at the same rate. The advance debits and credits 200 company units; the return exchanges the legs and offsets both balances. Arabic and English report views retain the same account codes, vouchers, currency and values.

[Detailed profile in English](../../apps/pav.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/pav)

## Payment Installments

Create a down-payment invoice and bill the remaining installments according to a dated sales-order schedule.

**Documented workflow**

According to Kanak, sales staff select payment terms, set the first installment date and optionally add charges on the Sales Order. Submission creates the schedule and the down-payment invoice including the charges, and a scheduler raises each later invoice two days before it falls due.

**Proposed acceptance example**

An order has principal 1,000, a 20% advance, freight 50 and three installments from 15 January. The first scheduled invoicing run executes twice on 13 January with no payment. The down-payment invoice is 250 and exactly one first-installment invoice for 266.67 exists, all of it outstanding. Changing the customer’s language retains the principal, due date, allocated amount and unique invoice origin.

[Detailed profile in English](../../apps/payment_installment_kanak.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/payment_installment_kanak)

## ERPNext United Kingdom

Prepare a UK VAT return from mapped vouchers, submit it for the correct period and reconcile the authority’s receipt.

**Documented workflow**

Case Solved’s manual describes businesses or agents reviewing and submitting VAT returns and viewing liabilities and payments. It also describes item- or invoice-level VAT rates, journal adjustments and a closing journal for the reporting period.

**Proposed acceptance example**

A working paper includes two tax lines of 12 and 8, their invoice-level summary of 20, and a separate mapped adjustment of minus 2. A Welsh-speaking preparer and an English-speaking filer open the same reviewed reporting period. Both views show 18 in the configured bucket, with the invoice summary excluded from double counting. Changing the reporting language preserves the registration, period key, box identities, evidence links and amounts.

[Detailed profile in English](../../apps/uk.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/uk)
