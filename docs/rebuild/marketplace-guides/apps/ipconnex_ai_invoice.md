# AI Invoice Importer

## Publisher and recovered source evidence

IPCONNEX advertises a version 14 tool that extracts invoice data from PDFs using ChatGPT. Its listed repository did not supply a public revision in the baseline. A separately hosted revision identifies the same app and credits IPCONNEX. The following behaviour belongs to that copy. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/ipconnex_ai_invoice) · [Listed repository](https://github.com/IPCONNEX-Services/IPCONNEX-AI-Invoice) · [Copy identification](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/hooks.py#L4)

| Stage in the copy | Observed details |
|---|---|
| Intake | The import form records a GPT configuration, company, attached invoice, default item, purchase/sales choice, supplier/customer, invoice date and currency. It has an item table, extracted amount, calculated total, difference and links to generated invoices. [Record definition](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/ipconnex_ai_invoice/doctype/invoice_import_tool/invoice_import_tool.json) |
| Extraction | The reader concatenates text extracted from PDF pages. The prompt supplies candidate parties and requests a date, currency, header amount and line description, rate, duration and charge. Settings, PDF-read and provider failures have separate responses. This path depends on extractable text. [Extraction flow](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/ipconnex_ai_invoice/extract.py#L15) |
| Transformation | The client selects Supplier or Customer by direction, skips zero-amount lines, builds quantity-one lines and scales amounts by 100 for its reconciliation. It can generate a Purchase Invoice or Sales Invoice and attach the source file. [Mapping, comparison and generation](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/ipconnex_ai_invoice/doctype/invoice_import_tool/invoice_import_tool.js#L76) |

## Proposed multilingual rebuild contract

An authorized clerk selects direction and company, attaches a file and requests an extraction using its attachment ID. Preserve the file hash, original text, document-language hints, extracted strings and reviewer corrections. Limit candidate parties to the authorized business scope. Match on stable party identity and show competing matches for review. Currency precision comes from the currency metadata. A model suggestion must never determine a posting by itself.

Show translated field captions beside the supplier’s original words. Preserve names, identifiers and line descriptions, including mixed scripts. Parse decimal and date conventions from document evidence separately from the reviewer’s UI locale. Present questionable values with their source text. Require a reviewer to confirm direction, party, date, amounts and currency before producing one linked draft per approved import revision.

| Acceptance example | Expected result |
|---|---|
| German PDF has a line “Beratung”, amount “1.234,50 EUR”, and date “18.11.2026”; clerk works in English | Review displays EUR 1234.50 and 2026-11-18 alongside their source strings. Approval produces one linked draft carrying currency EUR. Repeating the same approval returns that draft. |
| Input states “03/04/26” with no further date context or contains an image without extractable text | Flag the date for review or route the file for explicit OCR/manual entry. The import remains unposted, with its source available to an authorized clerk. |
| Header total differs from reviewed lines, taxes and rounding | Show the signed discrepancy and prevent final approval until it is explained. Switching UI language preserves the same decimal value and review decision. |

## Remaining evidence

Publisher release equivalence, available models, shipped translations, scanned-image handling and posted accounting outcomes need a versioned vendor build or runtime replay. The interface’s absolute difference, fixed two-decimal arithmetic and quantity-one strategy are source observations, not universal invoice rules.
