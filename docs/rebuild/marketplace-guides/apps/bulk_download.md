# Dynamic Bulk PDF Downloader

Meet Sherasiya lists versions 14–16. A user selects a record type and print format, filters the records, and optionally groups output PDFs into folders within one downloadable ZIP. The publisher gives invoices, purchase orders and delivery notes as examples. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/bulk_download) · [Developer’s walkthrough](https://meetsherasiya.github.io/project/bulk-download/)

## What the recovered source implements

The Sanprasoftware copy at `91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b` identifies Meet as author, carries the same app name and matches the listing’s described workflow. The marketplace-linked repository and release build were not available for a byte comparison. [Package identity](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/pyproject.toml)

- The Bulk Download record requires document type, print format and JSON filter. The group field is optional. The form stores a read-only ZIP link and error list, and the declared role is System Manager. [Record fields and grants](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/bulk_download/bulk_download/doctype/bulk_download/bulk_download.json)
- The command looks up matching names and the optional group field. An empty result returns false. Otherwise it queues a background job, renders the returned rows, accumulates per-document failures, creates ZIP entries and notifies the requesting user. The static query specifies no result page length or pagination; the fetched page cannot establish completeness for large selections. [Selection and queue](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/bulk_download/bulk_download/doctype/bulk_download/bulk_download.py#L13)
- The worker writes successful output into the public files area. If every render fails, a later notification check references a filename assigned only when an archive had entries. Folder names replace each character outside ASCII letters and digits with an underscore. Distinct international group names can collapse into the same folder. [Archive, errors, notification and folder naming](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/bulk_download/bulk_download/doctype/bulk_download/bulk_download.py#L39)

## Proposed rebuild contract and acceptance

Create an export job with requester, site, document filter, authorised selection, ordering, print template, language policy and job ID. Enumerate all authorised pages against a consistent snapshot. Recheck access before printing and at download. Return a private artifact, manifest of completed document IDs, per-document errors and a final status of completed, partial, empty or failed. An all-failure result carries no download link. A repeated request for the same job returns its existing result.

Localise queue notifications and status text. Support a single requested print locale and an explicit per-recipient printing policy. Preserve the locale actually used for each PDF. Build portable, distinct archive paths with stable record IDs and Unicode-safe names. Decide group membership on the stored key. Distinct customers with the same translated name must stay separate.

- For a synthetic selection of 55 authorised invoices spanning several query pages, render 55 PDFs. One failure yields 54 files and one named manifest error. No successful renders yields a failed job with the 55 errors.
- Generate an invoice in German and another in simplified Chinese. The PDFs must render their intended scripts and the ZIP preserve both document IDs. Two customers whose labels sanitise to the same text get distinct folders.
- Revoke access before a queued PDF is rendered. Record a denial without its contents. A different user cannot download the requesting user’s completed archive.
