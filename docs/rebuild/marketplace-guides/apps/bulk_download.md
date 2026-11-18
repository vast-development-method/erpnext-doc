# Dynamic Bulk PDF Downloader

[Business workflow and acceptance cases](../../../capabilities/guides/documents.md#bulk-document-rendition).

Meet Sherasiya lists versions 14–16. A user selects a record type and print format, filters the records, and optionally groups output PDFs into folders within one downloadable ZIP. The publisher gives invoices, purchase orders and delivery notes as examples. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/bulk_download) · [Developer’s walkthrough](https://meetsherasiya.github.io/project/bulk-download/)

## What the recovered source implements

The Sanprasoftware copy at `91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b` identifies Meet as author, carries the same app name and matches the listing’s described workflow. The marketplace-linked repository and release build were not available for a byte comparison. [Package identity](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/pyproject.toml)

- The Bulk Download record requires document type, print format and JSON filter. The group field is optional. The form stores a read-only ZIP link and error list, and the declared role is System Manager. [Record fields and grants](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/bulk_download/bulk_download/doctype/bulk_download/bulk_download.json)
- The command looks up matching names and the optional group field. An empty result returns false. Otherwise it queues a background job, renders the returned rows, accumulates per-document failures, creates ZIP entries and notifies the requesting user. The static query specifies no result page length or pagination; the fetched page cannot establish completeness for large selections. [Selection and queue](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/bulk_download/bulk_download/doctype/bulk_download/bulk_download.py#L13)
- The worker writes successful output into the public files area. If every render fails, a later notification check references a filename assigned only when an archive had entries. Folder names replace each character outside ASCII letters and digits with an underscore. Distinct international group names can collapse into the same folder. [Archive, errors, notification and folder naming](https://github.com/Sanprasoftware/Bulk-Download/blob/91a0d6c9808b9d9ba826285d107cc9d5d71c1c0b/bulk_download/bulk_download/doctype/bulk_download/bulk_download.py#L39)

## Proposed rebuild contract and acceptance

[Read the consolidated acceptance cases](../../../capabilities/guides/documents.md#bulk-document-rendition-2).
