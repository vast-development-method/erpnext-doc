# LumenPDF Studio

[Business workflow and acceptance cases](../../../capabilities/guides/documents.md#bilingual-document-layout).

Mahmood Husam lists ERP document and report design for versions 14–16. System Managers design formats, and document or report readers choose a format, preview a PDF and print, download or email it. The publisher describes standard read-only templates, editable copies, autosaved drafts, bulk output and per-company defaults. The gallery includes sales and purchasing documents, payment vouchers, delivery notes and financial reports. Designs can bind ordinary fields, child rows and a field on a linked record. The listing specifically describes Arabic-only and bilingual templates, embedded Arabic and Latin fonts, and currency-aware amount wording in Arabic or English. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/lumenpdf)

The publisher also describes site-hosted image assets, permission checks on protected fields and reports, private temporary outputs and filtering of branded reports. A Gemini-assisted design can start with an instruction or an image/PDF. The advertised validation and undo step operate on the format draft. A signed invoice QR comes from the invoicing integration and is consumed as document data. [Publisher description](https://cloud.frappe.io/marketplace/apps/lumenpdf)

A public historical copy identifies Lumen Solutions in its manifest and names the marketplace repository in its installation instructions. Its render service checks the document, selects an eligible template, queues a job under the requester and returns a job identifier. Where a company-specific mapping exists it takes precedence over the global mapping. This is static evidence from that copy. [Copy manifest](https://github.com/fwr567/LumenPDF-Studio/blob/0f1f0238103435e5e4e7b2aa6382e594c269091d/brandpdf/hooks.py) · [Render request and template selection](https://github.com/fwr567/LumenPDF-Studio/blob/0f1f0238103435e5e4e7b2aa6382e594c269091d/brandpdf/api.py)

## Proposed rebuild contract

The publicly inspectable copy has a different repository owner from the listed source. The deployed template set, precise permission handling and renderer/version equivalence remain unverified. The named documentation branch and the pinned framework print service identify two different evidence sources. [Named app branch](https://github.com/ma7mod7osam/LumenPDF-Studio/tree/lumenpdf) · [Framework print service](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/www/printview.py)

[Read the consolidated workflow](../../../capabilities/guides/documents.md#bilingual-document-layout-1).
