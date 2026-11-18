# AI Invoice Importer

[Business workflow and acceptance cases](../../../capabilities/guides/accounting.md#invoice-image-and-document-extraction).

## Publisher and recovered source evidence

IPCONNEX advertises a version 14 tool that extracts invoice data from PDFs using ChatGPT. Its listed repository did not supply a public revision in the baseline. A separately hosted revision identifies the same app and credits IPCONNEX. The following behaviour belongs to that copy. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/ipconnex_ai_invoice) · [Listed repository](https://github.com/IPCONNEX-Services/IPCONNEX-AI-Invoice) · [Copy identification](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/hooks.py#L4)

| Stage in the copy | Observed details |
|---|---|
| Intake | The import form records a GPT configuration, company, attached invoice, default item, purchase/sales choice, supplier/customer, invoice date and currency. It has an item table, extracted amount, calculated total, difference and links to generated invoices. [Record definition](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/ipconnex_ai_invoice/doctype/invoice_import_tool/invoice_import_tool.json) |
| Extraction | The reader concatenates text extracted from PDF pages. The prompt supplies candidate parties and requests a date, currency, header amount and line description, rate, duration and charge. Settings, PDF-read and provider failures have separate responses. This path depends on extractable text. [Extraction flow](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/ipconnex_ai_invoice/extract.py#L15) |
| Transformation | The client selects Supplier or Customer by direction, skips zero-amount lines, builds quantity-one lines and scales amounts by 100 for its reconciliation. It can generate a Purchase Invoice or Sales Invoice and attach the source file. [Mapping, comparison and generation](https://github.com/jwjohns/IPCONNEX-AI-Invoice/blob/c4f4ba36150619fe04a79e63bd9803aa0c8c2602/ipconnex_ai_invoice/ipconnex_ai_invoice/doctype/invoice_import_tool/invoice_import_tool.js#L76) |

## Proposed multilingual rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/accounting.md#invoice-image-and-document-extraction-2).

## Remaining evidence

Publisher release equivalence, available models, shipped translations, scanned-image handling and posted accounting outcomes need a versioned vendor build or runtime replay. The interface’s absolute difference, fixed two-decimal arithmetic and quantity-one strategy are source observations, not universal invoice rules.
