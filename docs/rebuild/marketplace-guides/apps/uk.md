# ERPNext United Kingdom

Case Solved lists a v14 UK regional app for Making Tax Digital (MTD) VAT. Its pinned support manual describes a configurable VAT report, return viewing and submission, and viewing liabilities and payments. The report can account for transaction-level or item-level VAT, separate or combined tax accounts, tax categories and journal adjustments. A closing-period journal is available. The listing presents payroll Real Time Information as a future feature. The support manual identifies the product as proprietary. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/uk) · [Publisher support manual](https://github.com/CaseSolvedUK/uk-support/blob/7bf2019121c89e681e294871f34d9bfee1420886/README.md)

## Proposed return lifecycle

1. An authorized business user or agent selects the VAT registration and retrieves its obligations. Persist the authority's period key, dates and status. Scope an agent's access to the represented registration.
2. A preparer selects the reporting policy and versioned mapping from accounts, categories, invoices, lines and adjustments to return boxes. Keep an explanation and voucher references for each box. Prevent an invoice-level total and its item components from both contributing the same tax.
3. Freeze a reviewed return and its calculation inputs. A submitter approves the declaration for the selected registration and period. Transmit the canonical return and record the acknowledgement or a pending, rejected or uncertain result.
4. Reconcile the filed return with the authority's records. Retrieve liabilities and payments independently. Generate any closing journal as a separately authorized accounting action linked to this version and protected against duplicate posting. [HMRC VAT service guide](https://developer.service.hmrc.gov.uk/guides/vat-mtd-end-to-end-service-guide/) · [HMRC VAT API](https://developer.service.hmrc.gov.uk/api-documentation/docs/api/service/vat-api/1.0)

## Multilingual filing

Store box identifiers, obligation keys and HMRC evidence as received. A user can display the same working paper in English or Welsh using reviewed labels. Use the definitive declaration required by the applicable HMRC process and retain the presented wording, version and language. Translation of an explanation cannot change the return or replace an official declaration. Reporting period, jurisdiction, authority payload schema and reporting units belong to the filing configuration and are independent of the preparer's language. Where an official rendering is unavailable, display its available language and distinguish any explanatory translation.

## Acceptance examples

- An isolated test dataset contains two mapped output-tax lines of 12.00 and 8.00, an invoice summary of 20.00 representing those same lines, and a separate eligible adjustment of −2.00. For this configured output-tax bucket the result is 18.00 in both language views. The trace identifies the two lines and adjustment exactly once.
- A Welsh-speaking preparer and an English-speaking authorized filer open the same reviewed period. They see the same box identifiers, values and evidence references. The filed result links to one receipt. Reopening it in Welsh cannot submit a second return or book another closing journal.
- If acknowledgement times out after submission, mark submission uncertain, query the period and reconcile before retrying. A payment in the liabilities view cannot by itself mark an unsubmitted draft as filed. A user authorized for a different registration cannot inspect or file it.

The example exercises mapping and lifecycle only. The proprietary formulas, current production accreditation, supported scheme combinations, translation coverage and exact closing-journal legs require independent qualification.
