# Documents, signatures and printing

English · [Afrikaans](../af/documents.md) · [Deutsch](../de/documents.md) · [简体中文](../zh-Hans/documents.md)

[All topics](README.md)

Each example describes an expected result for the rebuild. The application profile identifies what was observed in a running system, traced in source or described by a publisher.

## Dynamic Bulk PDF Downloader

Filter the records to print and download their PDFs in a ZIP archive grouped by the selected field.

**Documented workflow**

The operator selects a document type, print format, filters and an optional grouping field. The recovered worker renders matching records as PDFs, packages successful files in a ZIP and records per-document rendering errors.

**Proposed acceptance example**

The authorised selection spans several pages and contains 55 documents. Process the full selection with one render failure. The job returns 54 PDFs, one manifest error with a document ID and a partial completion status. Unicode group labels cannot collapse distinct group IDs, and the manifest records the language used for each PDF.

[Detailed profile in English](../../apps/bulk_download.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/bulk_download)

## Document Progress Tracker

Track a document’s milestones and report how much time elapses between them.

**Documented workflow**

The process owner chooses the document type, date field, milestones, conditions and percentages. When a condition is met the tracker updates document progress and writes a log that can show the milestone, user, timestamp and elapsed minutes or days.

**Proposed acceptance example**

Under an absolute-percentage policy a document enters approved at 08:00 UTC and delivered at 15:03 UTC on the same day. Apply the delivered event twice. Current progress is 100%, elapsed time from approval is 423 minutes and the second delivery event adds no log. Renaming or translating the approved milestone does not change the stored interval or milestone identity.

[Detailed profile in English](../../apps/document_progress_tracker.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/document_progress_tracker)

## Digital Signature

Assign a signer to a document and send the exact signed PDF to its recipient.

**Documented workflow**

The signer has a DSC User record with a signature image and password. The publisher’s walkthrough links that user to the invoice and uses the password and Signed PDF action to create a downloadable or emailable file.

**Proposed acceptance example**

An authorised user has signed the German version of an invoice and its artifact digest is recorded. Send two emails in different languages referencing that same signed file. Both attachment digests equal the archived signed digest. Neither dispatch creates a new signing event. Email language does not change the signed bytes or the signer identity.

[Detailed profile in English](../../apps/dsc.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/dsc)

## Esign App

Assign fields to each signer and preserve the language and content of the signed agreement.

**Documented workflow**

The publisher-linked code copies a PDF layout from its template, saves recipient assignments on dispatch and stores a rejection reason separately from completion and PDF signing.

**Proposed acceptance example**

Two signers receive the same Afrikaans agreement, one using German controls and the other English. Each completes their own required field. One finalized document records both assignments and the same agreement digest. The interface and invitation language cannot alter the agreement being signed.

[Detailed profile in English](../../apps/esign_app.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/esign_app)

## LumenPDF Studio

Design a bilingual invoice, preview its PDF and send it in the recipient’s preferred language.

**Documented workflow**

The publisher says a System Manager can adapt a standard design, bind invoice or report fields and preview a PDF. The person printing can choose an Arabic-only or bilingual format, then download the document or send it as an email attachment.

**Proposed acceptance example**

A bilingual invoice has a mixed-script customer name, two tax lines and a signed QR. An English-speaking clerk renders it with an Arabic/English format. Both headings render, the two posted tax amounts match and the scanned QR matches the original. Changing the editor language preserves the recipient language, tax values and signed payload.

[Detailed profile in English](../../apps/lumenpdf.md) · [Publisher listing](https://cloud.frappe.io/marketplace/apps/lumenpdf)
