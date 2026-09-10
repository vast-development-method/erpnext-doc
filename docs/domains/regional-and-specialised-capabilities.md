# Regional and specialised capabilities

## Scope and evidence boundary

Regional behaviour is selected by the company's country and configured tax accounts, identifiers, payment classifications, and document fields. It enriches the same customer, supplier, company, invoice, and tax records used elsewhere. It does not justify a separate accounting engine or unrestricted replacement of company-currency totals. The rules below describe the supplied snapshot's software behaviour; they do not assert that the forms or tax policies satisfy present-day law in every jurisdiction.

The active module manifest includes accounting, buying, selling, inventory, manufacturing, projects, support, maintenance, assets, quality, communications, telephony, regional functions, subcontracting, bulk transactions, and electronic business document interchange. It does not declare agricultural management or nonprofit operations as active modules. A residual template directory is not evidence of a functioning specialised domain. Do not invent agricultural production, grant accounting, or membership functionality and call it observed equivalence. Such additions need separately approved requirements and source evidence. Evidence: `source-artifact-c8b814e41fe9a77ee509 lines 1–21`.

## Reduced withholding certificates

A reduced withholding certificate belongs to a company, supplier, withholding category, fiscal year, and date range. It carries certificate identifier, supplier tax identifier, reduced rate, and certificate limit. End date cannot precede beginning. Both validity endpoints must lie inside the selected fiscal year. Date overlap is inclusive: sharing an endpoint counts as overlap. Reject an overlapping certificate found for the same company, supplier, and withholding category.

The inspected validation fetches one matching existing certificate and compares intervals. It does not prove that every possible overlapping certificate is checked if multiple nonoverlapping records already exist. A comprehensive acceptance fixture must include three existing intervals, not only one duplicate. Application of the rate, exhaustion of the certificate limit, and interactions with withholding thresholds belong to the accounting calculation specification and require separate evidence. Evidence: `source-artifact-f38681b729bfe3616d71 lines 33–81`.

## Electronic invoice tax summaries

The reviewed electronic invoice exporter aggregates tax amount and taxable amount by tax rate. Fixed actual charges are excluded from that aggregation. A tax calculated on a prior tax row's amount or total can be represented as an extra charge item. That item's quantity is one, its rate and taxable amount are the referenced charge amount, and its tax amount equals referenced charge amount multiplied by the current tax percentage divided by 100. Zero-rate summaries carry exemption reason and exemption law. A fallback zero-rate summary is produced when no itemised zero-rate details populated the summary. Evidence: `source-artifact-964d56c03fb16fe32936 lines 143–303`.

The invoice preflight requires company and customer addresses, company fiscal regime, both company tax and fiscal identifiers, and at least one tax row. Individual customers require fiscal code. Public administrations require fiscal code; other organisational customers require tax identifier. A zero tax row with zero amount requires exemption reason. Payment method codes are filled from the associated payment-method record when absent. These conditions must be evaluated before generating a document that cannot be accepted by its external consumer.

The external structured-invoice document layout, controlled document-type values, transmission identity, file naming, signature rules, acceptance receipts, and every validation of each national format are not fully expressed in this chapter. They remain exact-contract work items; do not treat the tax summary and preflight described here as a complete electronic-invoicing specification. Evidence: `source-artifact-964d56c03fb16fe32936 lines 143–303`.

## Supplier electronic invoice intake

A supplier-invoice intake record supplies the company, buying price list, invoice identity policy, default product, supplier group, tax account, and attached archive. Import processes member documents, extracts supplier invoice number and date, supplier and address details, item lines, tax rows, and payment terms, then creates purchase invoices. The supplier invoice number is required. Defaults and row derivation are part of the intake contract, not a licence to post an imported total without recalculating the purchase document.

Each invoice creation has a local rollback point. A failed invoice is logged and later archive members continue. Overall completion can therefore be partial. The source document is attached to a successfully created invoice, and record counters distinguish members processed from invoices created. This preserves audit evidence and explains why a batch may contain successful and failed members simultaneously. Evidence: `source-artifact-e74c2f55e46083e441f7 lines 37–155`.

The inspected line preparation includes a special sign case: when unit rate and line amount are both negative, it reverses quantity and identifies a return invoice. The import currently carries certain local row variables across iterations; the exact handling of missing quantity, unit, and rate fields requires a fixture with successive heterogeneous lines. Another agent must not assume the general import service defaults every missing field independently without checking that case. Privacy of retained source attachments is a proposed hardening requirement; the inspected importer explicitly creates them as nonprivate, so private storage cannot be described as its current guarantee. Evidence: `source-artifact-e74c2f55e46083e441f7 lines 37–155`.

## Country-selected reporting

| Capability | Observed selection and calculation |
| --- | --- |
| South African value added tax audit | Reject another company region; require configured tax accounts; include submitted nonopening customer and supplier invoices in the selected date range; aggregate itemised taxable and tax amounts by invoice and rate |
| United Arab Emirates value added tax return | Reject another company region; split standard-rated sales by emirate; show tourist refunds with negative sign; separately report reverse-charge, zero-rated, exempt, and recoverable amounts |
| United States supplier payment statement | Return no columns and no rows outside the selected country; group qualifying suppliers' general-ledger debit amounts in account currency by supplier and fiscal year, optionally supplier group |

For the South African audit, zero-rate tax details without the item's explicit zero-rated marker are excluded. Gross amount for an included tax-rate bucket equals taxable amount plus tax amount. The configured account set decides which itemised taxes participate. For the United States report, the inspected query sums supplier-side debit entries; it is not independently demonstrated to be equivalent to every statutory notion of a cash payment or to exclude every cancellation mechanism. Those distinctions require fixtures with journal adjustments, returns, and cancellations. Evidence: `source-artifact-8e20147fcb21422cacb1 lines 24–141`. Evidence: `source-artifact-e54f67c062c6bbe6e7f1 lines 12–155`. Evidence: `source-artifact-2221817bfbd40c447dd1 lines 22–65`.

## Contract fulfilment

A business contract can reference a customer, supplier, or employee, with optional linkage to a quotation, project, order, or invoice. Keep signed flag, signatory, signing time, company signing user, dates, contractual terms, and fulfilment checklist. Contract status is unsigned until signed. With an end date it is active only within the inclusive date range; without an end date the inspected helper reports active without separately testing whether the beginning date is in the future.

When fulfilment is required, zero completed checklist rows means unfulfilled, some means partially fulfilled, and all means fulfilled. An unmet fulfilment with a passed deadline becomes lapsed. With no fulfilment requirement, use “not applicable” in the neutral model. The signed contract's activation and checklist fulfilment do not themselves generate a receivable or payable; any related document has its own submission and posting rules. Evidence: `source-artifact-b1905f958b20155d191c lines 47–141`.

## Acceptance and extension requirements

Test regional activation by company, required identifiers before invoice export, zero-rated versus exempt items, separate tax buckets, charge-on-charge calculations, refund signs, import partial success, overlap at certificate endpoints, contracts with future beginnings and no ends, and expired incomplete fulfilment. Country-specific external format validation and current regulatory certification are outside what these reviewed routines establish. Implementation work must not mark this chapter as full jurisdictional parity until those exact-format and calculation fixtures are completed.
