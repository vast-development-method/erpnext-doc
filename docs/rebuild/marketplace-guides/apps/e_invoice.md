# E Invoice Egypt

[Business workflow and acceptance cases](../../../capabilities/guides/accounting.md#egyptian-electronic-tax-submission).

X Solutions lists versions 13 and 14. Its adapter offers individual and batch submission, credit and debit notes, cancellation and validation in connection with the Egyptian Tax Authority (ETA). The publisher describes a signing token, product/service coding and a nominated company contact as prerequisites for its setup. Bulk retrieval and obtaining a document printout appear under planned features. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/e_invoice)

## Authority service and app boundary

The ETA submission API takes one or more signed documents, correlates each local internal ID with a per-document response and accepts a batch in a single representation. An HTTP 202 acknowledges submission for further validation. Successfully accepted documents can coexist with initial rejections. ETA assigns a submission ID and returns document identifiers for the accepted subset and details for the rejected subset. Future collection of the full validation result is a separate step. These are authority-side semantics. The publisher’s app implementation of signing, polling and replay remains unverified. [ETA Submit Documents specification](https://sdk.invoicing.eta.gov.eg/einvoicingapi/01-submit-documents/)

## Proposed rebuild contract

- For a test submission containing `INV-001` and `INV-002`, ETA responds 202 with a UUID for the first and a structure error for the second. Record one pending final validation, one actionable error and no final approvals. Poll the first without sending it again when the second is corrected.
- If a user prepares a credit note for an original invoice line that was never present, fail the authority-profile validation before dispatch. ETA’s documented credit type restricts additions of new invoice lines and amounts beyond the referenced invoices. [Document types in the submission contract](https://sdk.invoicing.eta.gov.eg/einvoicingapi/01-submit-documents/)
- If the network drops after dispatch, retain the exact request fingerprint. Use available submission evidence to reconcile its status before retrying. Treat ETA’s duplicate response and retry timing separately from a permanent data rejection.

[Read the consolidated workflow](../../../capabilities/guides/accounting.md#egyptian-electronic-tax-submission).

## Language

Use the issuing entity’s approved Arabic or other supplied text where the document schema calls for names and descriptions. An English operator may inspect Arabic source text without altering the signed payload. Store the authority's error code, target, original message and language, plus localised guidance for the user. Display Unicode bidirectional text without transforming opaque invoice IDs, external UUIDs, tax codes or timestamps. The same signed request remains byte-identical when read from Arabic or German screens. [Authority response error schema](https://sdk.invoicing.eta.gov.eg/einvoicingapi/01-submit-documents/)

The published app-level version claim and the ETA API contract establish separate boundaries. A token-enabled reference site and test-tenant submission would be needed to establish provider interoperability for the listed build. [Publisher-named repository](https://github.com/AlaaBadry/E-invoice-Egypt)
