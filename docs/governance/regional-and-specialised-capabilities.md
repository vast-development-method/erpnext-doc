# Regional and specialised capabilities

Read this chapter with [taxation and pricing](../transactions/taxation-and-pricing.md), [financial accounting](../transactions/financial-accounting.md), [company governance](company-and-master-governance.md), [supplier payables](../transactions/accounts-payable.md) and [external integrations](../services/external-integrations.md). The structured [customer and service calculations](../../schemas/mathematics/customer-and-service-calculations.json) and [acceptance cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json) define exact examples for the calculations below.

## Regional selection

The company country, configured tax accounts, identifiers, payment classifications and document fields select the regional behaviour. The invoice retains its transaction and company-currency amounts when a jurisdiction requires additional classifications.

## Reduced withholding certificates

A reduced withholding certificate belongs to a company, supplier, withholding category, fiscal year, and date range. It carries certificate identifier, supplier tax identifier, reduced rate, and certificate limit. End date cannot precede beginning. Both validity endpoints must lie inside the selected fiscal year. Date overlap is inclusive: sharing an endpoint counts as overlap. Reject an overlapping certificate found for the same company, supplier, and withholding category.

The defined validation fetches one matching existing certificate and compares intervals. It does not prove that every possible overlapping certificate is checked if multiple nonoverlapping records already exist. A comprehensive acceptance fixture must include three existing intervals, not only one duplicate. Application of the rate, exhaustion of the certificate limit, and interactions with withholding thresholds belong to the accounting calculation specification and require separate evidence.

## Electronic invoice tax summaries

The defined electronic invoice exporter aggregates tax amount and taxable amount by tax rate. Fixed actual charges are excluded from that aggregation. A tax calculated on a prior tax row's amount or total can be represented as an extra charge item. That item's quantity is one, its rate and taxable amount are the referenced charge amount, and its tax amount equals referenced charge amount multiplied by the current tax percentage divided by 100. Zero-rate summaries carry exemption reason and exemption law. A fallback zero-rate summary is produced when no itemised zero-rate details populated the summary.

The invoice preflight requires company and customer addresses, company fiscal regime, both company tax and fiscal identifiers, and at least one tax row. Individual customers require fiscal code. Public administrations require fiscal code; other organisational customers require tax identifier. A zero tax row with zero amount requires exemption reason. Payment method codes are filled from the associated payment-method record when absent. These conditions must be evaluated before generating a document that cannot be accepted by its external consumer.

The external structured-invoice document layout, controlled document-type values, transmission identity, file naming, signature rules, acceptance receipts, and every validation of each national format are not fully expressed in this chapter. They remain exact-contract work items; do not treat the tax summary and preflight described here as a complete electronic-invoicing specification.

## Supplier electronic invoice intake

A supplier-invoice intake record supplies the company, buying price list, invoice identity policy, default product, supplier group, tax account, and attached archive. Import processes member documents, extracts supplier invoice number and date, supplier and address details, item lines, tax rows, and payment terms, then creates purchase invoices. The supplier invoice number is required. Defaults and row derivation are part of the intake contract, not a licence to post an imported total without recalculating the purchase document.

Process each invoice header inside its own database savepoint. This includes supplier, contact and address preparation, duplicate checks, draft purchase invoice and its private source attachment. A failure rolls back that header's database changes and allows later headers to run. The import counts each header, counts a skipped signed or unreadable member once, and increments its success count only after the attachment is saved. See [row derivation and partial failure](#supplier-import-row-derivation-and-partial-failure).

## Country-selected reporting

| Capability | Observed selection and calculation |
| --- | --- |
| South African value added tax audit | Reject another company region; require configured tax accounts; include submitted nonopening customer and supplier invoices in the selected date range; aggregate itemised taxable and tax amounts by invoice and rate |
| United Arab Emirates value added tax return | Reject another company region; split standard-rated sales by emirate; show tourist refunds with negative sign; separately report reverse-charge, zero-rated, exempt, and recoverable amounts |
| United States supplier payment statement | Return no columns and no rows outside the selected country; group qualifying suppliers' general-ledger debit amounts in account currency by supplier and fiscal year, optionally supplier group |

For the South African audit, zero-rate tax details without the item's explicit zero-rated marker are excluded. Gross amount for an included tax-rate bucket equals taxable amount plus tax amount. The configured account set decides which itemised taxes participate. For the United States report, the defined query sums supplier-side debit entries; it is not independently demonstrated to be equivalent to every statutory notion of a cash payment or to exclude every cancellation mechanism. Those distinctions require fixtures with journal adjustments, returns, and cancellations.

## Contract fulfilment

A business contract can reference a customer, supplier, or employee, with optional linkage to a quotation, project, order, or invoice. Keep signed flag, signatory, signing time, company signing user, dates, contractual terms, and fulfilment checklist. Contract status is unsigned until signed. With an end date it is active only within the inclusive date range; without an end date the defined helper reports active without separately testing whether the beginning date is in the future.

When fulfilment is required, zero completed checklist rows means unfulfilled, some means partially fulfilled, and all means fulfilled. An unmet fulfilment with a passed deadline becomes lapsed. With no fulfilment requirement, use “not applicable” in the neutral model. The signed contract's activation and checklist fulfilment do not themselves generate a receivable or payable; any related document has its own submission and posting rules.

## Acceptance and extension requirements

Test regional activation by company, required identifiers before invoice export, zero-rated versus exempt items, separate tax buckets, charge-on-charge calculations, refund signs, import partial success, overlap at certificate endpoints, contracts with future beginnings and no ends, and expired incomplete fulfilment. Country-specific external format validation and current regulatory certification are outside what these reviewed routines establish. Implementation work must not mark this chapter as full jurisdictional parity until those exact-format and calculation fixtures are completed.

## Regional record contracts

| Record | Durable fields | Governing rule |
| --- | --- | --- |
| Reduced withholding certificate | Company, supplier, fiscal year, withholding category, identifier, supplier tax identifier, beginning/end, reduced rate and limit | Date validation and overlapping-interval search described above |
| Country tax-account configuration | Company and selected tax-ledger account rows | Determines report inclusion; tax-account membership must not be inferred from an account name |
| Electronic invoice projection | Invoice identity, company/customer tax data, addresses, transmission sequence, document category, product rows, tax-rate summaries and payment installments | Derived from accepted invoice and regional configuration |
| Supplier import batch | Company, attached archive, default product/unit context, buying price list, supplier group, tax account, naming policy, progress and outcome counts | Protected background import with per-invoice failure boundaries |
| Contract | Party kind and identity, terms, signed state, signatory and time, company signer, effective dates, linked transaction and optional fulfilment checklist/deadline | Contract activation is separate from checklist fulfilment and financial posting |

The full field inventories are [reduced withholding certificate](../../schema/entities/regional-accounting.json), [supplier invoice import](../../schema/entities/regional-accounting.json) and [contract](../../schema/entities/sales-relationships.json).

## Structured customer-invoice export contract

An export selection includes submitted customer invoices with nonempty company tax identifiers. Optional company, customer, beginning posting date and ending posting date narrow the selection; both dates form an inclusive range. Read permission is required. Opening invoices are excluded from the regional validation/submission generation path, although the bulk selection's base filter itself does not include an opening exclusion.

Preparation derives an unamended invoice number by removing the final amendment suffix when the invoice has an amendment origin. A return linked to a prior invoice defaults to the external credit-note document category; otherwise the default is ordinary invoice. A public-administration customer selects the public-administration transmission profile; other customers select the private-sector profile.

| External contract concept | Fixed value in this interchange profile |
| --- | --- |
| Ordinary invoice category | `TD01` |
| Credit-note category | `TD04` |
| Public-administration transmission profile | `FPA12` |
| Private-sector transmission profile | `FPR12` |
| Regional schema namespace version | `1.2` |

These literals are external controlled values rather than abbreviations for this repository's business concepts. Their surrounding field meaning is defined in full. A newer national format must be a separate versioned contract; it must not silently change a historical invoice's selected profile.

The generated document contains the following ordered semantic groups:

1. Transmission: sender country and fiscal identity, monotonically allocated sequence, transmission profile, recipient routing identity and optional sender telephone/electronic mail.
2. Supplier identity: country and tax identity, optional fiscal identity, company name, fiscal regime, address and optional business-register information, share capital, member classification and liquidation state.
3. Customer identity: for a person, fiscal identity and first/last names; for an organisation, country/tax identity, optional fiscal identity and name; then customer address.
4. Invoice header: document category, currency, posting date, unamended number, optional stamp duty, document discount or surcharge, total and selling purpose.
5. Related business records: unique customer order references with dates, linked original invoice for a credit, delivery identities/dates with line references, and optional shipping address.
6. Goods/services: sequence, product identity, plain-text description, quantity, unit, unit price, discount/margin components, net row total, tax rate and optional exemption category.
7. Tax summaries: one rate bucket with taxable amount, tax amount, optional exemption category and exemption law; optional collectability is emitted only under the renderer's qualifying condition.
8. Payment: installment/full-payment classification and installment rows containing payment method, due date, amount and optional bank identity, international account number and bank-routing components.

Addresses require postal code, city and country code during preflight. Country codes are normalised to uppercase; recognised regional province names can map to province codes. Both company tax and fiscal identifiers are required. The issuer's fiscal regime and customer's appropriate individual, public-administration or organisational tax identity must be present. Each payment schedule row needs a payment method whose configured external code exists before regional submission.

### Export numerical and selection rules

The numeric formatter outputs absolute magnitudes. It uses exactly three decimal places when the requested field precision is three, four when it is four, and two for all other requested precisions. Therefore a return's negative quantity and amounts are rendered as positive magnitudes under its credit document category. This rendering does not alter signed internal ledger amounts.

For a line with tax rate $r$, the tax divisor is $1+r/100$ when any invoice tax row is included in the displayed price and the product tax rate is nonzero; otherwise the divisor is one. Unit-price selection prefers a nonzero price-list rate divided by this divisor, then a nonzero net rate, then rate divided by divisor. A zero value does not win either fallback. Percentage discount components are emitted only when positive. Positive margin components are emitted as a percentage, or as a fixed amount divided by the divisor.

Example: with a price-list rate of 115 and included tax rate 15 percent, the exported pre-tax unit price is 100. A positive amount margin 11.5 is rendered as a pre-tax margin ten. The row net amount remains the accepted invoice net amount; it is not recalculated by multiplying a formatted unit price and quantity in the exporter.

The document total selects nonzero rounded total, otherwise grand total. A positive overall discount is a discount component; a negative amount is a surcharge, with its exported magnitude positive. A fixed actual charge whose tax amount is exactly two is selected as stamp duty by this compatibility routine; the search is by amount and charge kind, not a separate dedicated stamp-duty flag.

Tax summaries are keyed by the textual tax-rate value. Zero-rate exemption reason and law come from the qualifying tax rows; several zero-rate categories at the same rate are not automatically separated into distinct summary keys. A charge on a prior tax row uses that prior row's tax amount as an additional charge item even for the prior-row-total calculation category. Preserve this exact rule in the export projection while the authoritative invoice's own tax engine remains governed by [taxation and pricing](../transactions/taxation-and-pricing.md).

### File lifecycle and limits

Generated export files are private attachments to the invoice. Names combine the company's country-prefixed tax identifier, an underscore and an allocated five-digit sequence. Regeneration requests replacement: when a matching earlier attachment is found, remove it and reuse its name/sequence. Otherwise allocate a new sequence. Cancellation removes matching regional export attachments. Bulk download collects matching attachments and packages them as one compressed download.

The renderer receives the invoice and line metadata. It reads installment rows from the invoice. Its separate, unbound schedule-length variable has length zero in the supplied rendering environment, so a two-row schedule emits two installment details but the single-payment classification `TP02`. A different template environment that supplies this variable can emit `TP01` for more than one row. The tax-summary collectability condition tests the summary entry then reads the code from the invoice.

### Receiver element mapping

The root `FatturaElettronica` carries the transmission profile in its `versione` attribute. The following field groups describe the generated file. Code lists associated with an invoice use the portion before the first hyphen where specified by the renderer.

| Group | Elements and business values |
| --- | --- |
| Header / `DatiTrasmissione` | `IdTrasmittente.IdPaese` is the issuer address country. `IdCodice` uses fiscal identity first, otherwise tax identity with `IT` removed. `ProgressivoInvio`, `FormatoTrasmissione` and `CodiceDestinatario` carry sequence, profile and routing code. `ContattiTrasmittente` contains available `Telefono` and `Email`. |
| Header / `CedentePrestatore` | `DatiAnagrafici.IdFiscaleIVA` contains `IdPaese` and the tax `IdCodice` with `IT` removed. Emit optional `CodiceFiscale`, `Anagrafica.Denominazione` and the code for `RegimeFiscale`. `Sede` carries `Indirizzo`, `CAP`, `Comune`, optional `Provincia` and `Nazione`. A registration number adds `IscrizioneREA` with `Ufficio`, `NumeroREA` and any available `CapitaleSociale`, `SocioUnico` and `StatoLiquidazione`. |
| Header / `CessionarioCommittente` | For an individual, `DatiAnagrafici` contains `CodiceFiscale` and `Anagrafica.Nome` / `Cognome`. Other customers supply `IdFiscaleIVA` (address country and tax identifier), optional `CodiceFiscale`, and `Anagrafica.Denominazione`. An available address adds `Sede` in the same address shape. |
| Body / `DatiGeneraliDocumento` | `TipoDocumento`, `Divisa`, `Data` and `Numero` carry document category, currency, posting date and unamended identity. For stamp duty, `DatiBollo` carries `BolloVirtuale=SI` and `ImportoBollo`. A nonzero document adjustment adds `ScontoMaggiorazione` with `Tipo` (SC discount or MG surcharge), optional positive `Percentuale` and absolute `Importo`. `ImportoTotaleDocumento` carries the selected total. `Causale` is `VENDITA`. |
| Body / other `DatiGenerali` | One `DatiOrdineAcquisto.IdDocumento` and `Data` pair per distinct purchase order with number and date, retaining the first date. `DatiFattureCollegate.IdDocumento` needs a return and an unamended original identity. The preparation step populates this identity when defaulting a linked return's document category. Each row linked to a delivery adds `DatiDDT.NumeroDDT`, `DataDDT`, `RiferimentoNumeroLinea`. Optional `DatiTrasporto.IndirizzoResa` uses the address shape above. |
| Body / `DatiBeniServizi.DettaglioLinee` | `NumeroLinea` is the row index. `CodiceArticolo` contains `CodiceTipo=CODICE` and product `CodiceValore`. `Descrizione` is plain-text description, falling back to item name. `Quantita`, `UnitaMisura`, `PrezzoUnitario`, `PrezzoTotale`, `AliquotaIVA` and optional exemption `Natura` carry the line's numeric values and stock unit. Positive line percentage discounts emit `ScontoMaggiorazione` with SC/percentage. Positive margins emit MG/percentage or MG/amount adjusted for inclusive tax. |
| Body / `DatiBeniServizi.DatiRiepilogo` | For each tax-rate bucket emit `AliquotaIVA`, `ImponibileImporto`, `Imposta`, and any applicable `Natura`, `EsigibilitaIVA`, `RiferimentoNormativo`. The numerical and collectability rules above define what each bucket contributes. |
| Body / `DatiPagamento` | A nonempty invoice schedule emits `CondizioniPagamento` and one `DettaglioPagamento` per installment with method code `ModalitaPagamento`, due date `DataScadenzaPagamento`, and `ImportoPagamento`. An account name adds `IstitutoFinanziario`. An IBAN adds `IBAN`, its sixth through tenth characters as `ABI`, and eleventh through fifteenth as `CAB`. An available SWIFT code adds `BIC`. |

The exporter globally replaces ampersands in the rendered text before saving the private file. The signature namespace declaration is part of the envelope. Export completes when the file is saved. Digital signing, delivery to a receiver, external schema acceptance and handling a receipt require a separate service. The file alone supplies no receiver acknowledgement.

## Supplier import row derivation and partial failure

Starting an import requires batch write permission. The operation commits its processing state, then queues the batch. A default stock unit must exist. The job opens the archive attached to this batch. It skips signed `.p7m` members and logs them as unsuccessful. It tries UTF-8 with optional byte-order mark, followed by UTF-16. Read errors that propagate are logged and counted. A decoding error that the helper converts into empty text, or any parsed member without an invoice header, yields no header and no increment. An unexpected archive-level error records batch Error.

Each `DatiGeneraliDocumento` header counts once and starts a database savepoint. Require a supplier bill number and read its bill date. Set local posting date to the import date and currency to the selected company's default. Header categories `TD04` and `TD08` create a return invoice. A negative detail on an ordinary invoice can create negative quantity independently of its header. The importer reads header-specific number, category and date but selects supplier, lines, taxes and installments from the whole member. Several headers in the same XML can therefore refer to the same body data.

| Step | Saved or rejected result |
| --- | --- |
| Identify supplier | Find an existing supplier by tax identifier. Ensure a linked contact exists. If no tax match exists, create the supplier and its contact. An already-used supplier name can receive a numeric suffix. Read street, city, province, postal code and country. Reuse a linked billing address matching street and postal code, or create an address when the street is supplied. |
| Prepare each line | Require both unit price and total. Quantity defaults to one, unit to the configured stock unit, tax rate to zero, independently on each row. Header credit or simultaneous negative rate and line total makes the quantity negative absolute. A discount or surcharge component and nonzero quantity select line total divided by signed quantity as the effective rate. Store its absolute magnitude. Store the batch's default item, a sanitized description, the first 140 characters as display name, and conversion factor one. |
| Prepare taxes | Each tax summary with a rate generates an actual-amount row for the configured tax account. A missing amount is zero. A return uses negative absolute tax. Retain the collectability text when supplied. |
| Reject repeat | Before insertion reject any uncancelled purchase invoice matching company, supplier, header return flag, bill number and bill date. An otherwise identical cancelled invoice does not block import. |
| Insert and attach | Insert a draft purchase invoice with rounded total disabled, calculate its own totals, adjust its schedule and save. Write the original input as a **private** attachment to this invoice. Invoice preparation, duplicate detection, insertion and attachment all share the header savepoint. A failed header rolls back its database changes, is logged and leaves later headers eligible. An independently written file is subject to the [file and savepoint boundary](../services/background-work-and-consistency.md#batch-outcomes-and-queued-effects). |
| Publish batch result | Increment the success count after attachment insertion. Equal success and input counts mean complete, including zero/zero. Fewer successes mean partial. A draft produced by a successful import still needs its ordinary business approval and submission. |

Suppose a first row contains three boxes at ten. A second row has price five and total five, with no quantity, unit or tax. With default unit Each, it produces **one Each at five**, with tax rate zero. Under a credit header a line of two units with final discounted total 18 and nominal rate ten produces quantity −2 and absolute rate nine. Its prepared amount is −18.

For payment, map recognised method codes, keep the supplied IBAN, and default a missing due date to the import date. Sum the imported installments and retain their original sum. The difference between that sum and the recalculated grand total adjusts only the first installment. Imported installments of 60 and 60 against a calculated 110 become 50 and 60. A difference larger than the first installment can produce a negative first installment.

## Report arithmetic and presentation boundaries

For the South African audit, iterate supplier invoices and customer invoices independently. Select submitted, nonopening documents and item-tax detail rows belonging to configured tax accounts. Accumulate taxable amount and tax amount for each invoice/rate pair. A zero-rate detail is included only when its product row explicitly has the zero-rated marker. Gross equals taxable plus tax. Sections group by tax rate and contain subtotals; invoice rows are ordered by posting date descending in the initial selection.

Example: one invoice has taxable 1,000 and tax 150 at 15 percent, plus taxable 200 and tax zero with the explicit zero-rated marker. It contributes two buckets: gross 1,150 and gross 200. Another zero-tax row lacking that marker contributes nothing to the zero-rate bucket. Display headings convert rate to an integer, so a fractional rate must retain its true numeric grouping value even if the inherited heading truncates its label.

The United Arab Emirates standard-rated sales selection groups submitted invoice rows that are neither exempt nor zero rated by emirate, summing company-currency net amounts and row tax amounts. The fixed displayed order is Abu Dhabi, Dubai, Sharjah, Ajman, Umm Al Quwain, Ras Al Khaimah and Fujairah, with zero rows when a category has no amounts. Tourist refund totals and tax amounts are negated for display. Reverse-charge, zero-rated, exempt, recoverable and standard expense amounts are separate report components with their own invoice/ledger selection.

| Return component | Amount selection | Tax selection |
| --- | --- | --- |
| Tourist refunds | Negative sum of company-currency totals of submitted customer invoices with a positive tourist-refund amount | Negative sum of those tourist-refund amounts |
| Reverse-charge supplies | Sum company-currency totals of submitted supplier invoices marked reverse charge | Sum ledger debits on configured regional tax accounts joined to those invoices, with submitted ledger lifecycle |
| Zero-rated supplies | Sum company-currency net values of submitted customer invoice rows explicitly zero rated | Display a nonnumeric empty tax placeholder |
| Exempt supplies | Sum company-currency net values of submitted customer invoice rows explicitly exempt | Display a nonnumeric empty tax placeholder |
| Standard-rated recoverable expenses | Sum company-currency totals of submitted supplier invoices with positive recoverable standard expense amounts | Sum the stored recoverable standard expense amounts |
| Recoverable reverse-charge expenses | Sum company-currency totals of submitted reverse-charge supplier invoices with positive recoverability percentage | Sum configured tax-account ledger debits multiplied by that invoice's recoverability percentage divided by 100 |

The reverse-charge ledger joins use invoice identity without an explicit voucher-kind comparison in that join. They check submitted lifecycle but do not independently filter the ledger cancellation marker. These details require conflicting-name and cancelled-ledger fixtures rather than an assumption that every debit is a current qualifying tax. A tax debit of 150 and recoverability percentage 40 contributes recoverable tax 60 while the recoverable amount column contains the full qualifying invoice total.

One shared date-filter helper adds the upper boundary only when a beginning date is supplied. An ending-only request therefore does not reliably constrain every component, and a beginning-only request can pass an absent upper value. Paired beginning/end dates are the supported acceptance fixture for report consistency; repair of independent optional bounds is a separately declared correction.

The United States supplier payment statement selects general-ledger debit amounts in account currency for qualifying supplier parties in the chosen company and fiscal year, optionally restricted by supplier group. It does not perform currency conversion merely because several suppliers share a report. Returns, journal adjustments, ledger cancellation and account-currency mixtures require explicit fixtures before interpreting its displayed total as a statutory cash-payment total.

The printable supplier statement renders each qualifying supplier separately, using the fiscal-year beginning's calendar year, company and supplier tax identities, selected addresses, and a payment value formatted in United States dollars with zero decimal places. The payer-address lookup prioritises postal, then billing, then deterministic name order among records marked as company addresses; it does not constrain that address selection to the requested company. The recipient lookup matches the party identity through address links without additionally restricting the linked party kind. These are explicit cross-company and duplicate-name acceptance cases, not assurances of correctly scoped printed addresses.

## Contract transitions and acceptance

Validate end not before beginning. Fill an absent party display name from the selected party; keep the party kind so a customer and employee with identical display names remain different counterparties. Submission records the acting company user as company signatory. Unsigned remains unsigned regardless of date. A signed contract with both bounds is active from beginning through end inclusive; a signed contract without an end is active even when its beginning is in the future under the stated compatibility rule.

When fulfilment is required, count fulfilled checklist rows. Zero gives unfulfilled, a positive count below row count gives partially fulfilled, and all rows fulfilled gives fulfilled. A required but empty checklist yields unfulfilled because the zero branch takes precedence. A passed deadline changes any incomplete result to lapsed, but equality with the deadline does not lapse it. With no fulfilment requirement the result is not applicable.

The daily contract update selects signed submitted contracts and refreshes activation status. It does not call the fulfilment calculation in that daily path, so elapsed deadlines alone do not establish automatic lapse until a path recomputes fulfilment. Permitted submitted-record updates recalculate both states. Cancellation/discard records cancelled activation. Neither signing nor fulfilment posts accounting; explicit purchase, customer, payroll or project documents carry financial consequences.

Acceptance cases cover inclusive validity and overlap endpoints, zero versus absent values, full and partial imports, inherited row values, missing postal/contact keys, payment adjustment, credit-document magnitudes, currency/rate grouping, future unbounded contracts and checklist lapse recalculation. Calculations are independently checkable; complete jurisdictional behavior remains gated by the external receiver contracts and executed report/invoice fixtures.

## Linked specifications

- **Calculation and acceptance cases** · [customer and service calculations](../../schemas/mathematics/customer-and-service-calculations.json) · [acceptance cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json)
- **Record definitions** · [reduced withholding certificate](../../schemas/data/record-types/lower_deduction_certificate.json) · [supplier invoice import](../../schemas/data/record-types/import_supplier_invoice.json) · [contract](../../schemas/data/record-types/contract.json)
