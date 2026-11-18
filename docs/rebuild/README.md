# Unified ERP rebuild specification

A rebuild must preserve what each transaction does to the business. Start with the [purchase-to-cash example](integrated/README.md). Its twelve vouchers move raw material, finished stock, supplier debt, customer debt, tax, income and cash. A replacement can pass a double-entry balance check while assigning a receipt to the wrong invoice or charging the wrong item cost. The fixture exposes all three ledgers and their source rows so each error can be detected independently.

## Choose a reference edition

| Edition | Authority and content | How to use it |
|---|---|---|
| September 10, 2026 | Four development snapshots of ERPNext, Framework, HRMS and CRM. The archived edition contains 3,476 files, including 33,360 ordered operations, 1,044 record definitions, 16,813 declared fields and 226 registered reports. | Use the [one-command restore and verification](../../checkpoints/reading-guide.md) for the full decision tables, mathematical contracts, reports and conformance gates. The checkout also contains earlier readable catalogs. |
| November 18, 2026 | [ERPNext v16.60.0](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264) and [Frappe v16.60.1](https://github.com/frappe/frappe/tree/199a0385c00e572664a099a57a00be6ce7404eeb). Each extension guide identifies the available source, version evidence and qualification boundary. | Use this directory for the release's dictionary, source-specific decisions and numeric fixtures. The [four-repository comparison](model/README.md) identifies declaration differences by record, field and permission. |

A revision can change a real business outcome. The [attendance-to-payroll trace](industry/attendance-leave-payroll.md) shows how the November code calculates the unpaid fraction of partially paid leave. The [configuration example](configuration/README.md) shows how the same release and role yield different purchasing access at two sites. Always record **source revisions, installed app order, company, effective settings, acting identity and business date** with a conformance result.

## What the live site established

On a disposable Namibia/NAD company, ERPNext submitted twelve linked vouchers. A fresh database connection read each committed voucher, its stock and general-ledger entries and its invoice balances. The company ended with N$940.20 at bank, N$134.80 of stock and N$82.80 gross profit. When a partial credit was submitted with stale mapped totals, the same economic postings left a N$69.00 invoice and an offsetting open credit. The [observed records](live/README.md) and [portable comparator](comparison/README.md) reproduce the difference. Six actual [report outputs](live/reports/README.md) reconcile the committed run to trial balance, balance sheet, profit and loss, receivables ageing, payables ageing and stock balance.

Two other reference runs cover [20 upstream stock, manufacturing and repost tests](stock-live/README.md) and [21 platform observations](platform-live/README.md) including role-scoped reads, field publication, multi-row rollback and queue admission. The [backup and restore experiment](recovery-live/README.md) gives the recovery evidence for its own configuration. The [verification entry point](verify/README.md) checks the published fixtures, schemas, source evidence and qualified outputs without requiring a replacement implementation.

## Reading order for an implementation

| Build concern | What to implement or inspect | Evidence and acceptance |
|---|---|---|
| 1. Metadata and tenant configuration | Stored vs virtual records, child tables, links, field ordering, dependent fields, grants, site-owned custom fields, fixtures, naming and workflows. | [Field dictionary and drift](model/README.md) · [Two effective sites](configuration/README.md) · [Report, service, hook and test index](surfaces/README.md) |
| 2. Shared application services | Tenant routing, document validation, approval, identity and version checks, database transactions, file access, work scheduling and reporting. | [Platform contracts, cases and source observations](platform/README.md) |
| Language throughout the implementation | Resolve the operator, party and recipient language separately. Preserve original text, financial values and integration identifiers. Capture the template and language of issued documents. | [Language contract and observed invoice rendering](marketplace-guides/languages/README.md) · [Multilingual workflow examples](marketplace-guides/README.md) |
| 3. Trading and inventory | Quotation, prices, order/fulfilment/billing progress, subscriptions, POS, replenishment, purchase receipts, stock close, subcontracting and operational quality. | [Commercial and service workflows](business/README.md) · [Procurement and warehouse](operations/README.md) · [Valuation, returns and reposting](valuation/README.md) |
| 4. Production and assets | Material planning, capacity, alternative components, job cards, production cost, secondary outputs, repair, capitalization and disassembly. | [Shop floor and production](production/README.md) · [Composite asset cost](finance/composite-asset-cost.md) |
| 5. Posting, settlement and statements | Separate commercial, stock, ledger and party entries. Preserve tax bases, discount distribution, exchange differences, and reporting periods. | [Finance](finance/README.md) · [Tax and settlement](finance/posting/README.md) · [Four statements from a single journal](finance/reporting/README.md) |
| 6. Workforce and customer handoffs | Paid/unpaid time, payroll accrual and employer costs, recruitment, advances, expenses and CRM-to-order provenance. | [Cross-application workflows](industry/README.md) |
| 7. Integrated verification | Follow each source voucher and item row through the inventory, party and general ledgers. Compare rejected commands, returns and recovery alongside successful postings. | [Twelve-voucher conformance example](integrated/README.md) · [September acceptance strategy](../reimplementation/acceptance-strategy.md) |

## Extension and topic coverage

| Where to start | What the evidence covers |
|---|---|
| [Core and framework dictionaries](model/README.md) | 866 canonical record types, 14,412 source-declared fields, 1,538 permission rows and 2,555 field conditions at the two release pins. |
| [Core runtime surfaces](surfaces/README.md) | 21,433 declarations, including 1,614 exposed operations and 88 scheduled handlers. The 206 report declarations include three test fixtures. |
| [Eighteen extension profiles](extensions/README.md) | Business rules and integration boundaries for HRMS, CRM, lending, payments, education, healthcare, commerce, shipping, regional and other named applications. Declared data cover 695 record types and 9,163 fields. Each app has an independent revision and dependency range. |
| [Five companion profiles](companion/README.md) | Helpdesk, Learning, Insights, Drive and Print Designer. The chapters distinguish an actual ERP handoff from a product that shares only the underlying framework. |
| [Marketplace source directory](marketplace-model/README.md) | Every one of the 398 observed listings has a status. The catalog identifies 329 public source pins. After the core listing and 15 curated overlaps, 313 additional listing sources were inspected. Of those, 101 declared an ERPNext dependency, a further 111 showed selected production integration evidence, and 101 showed none under the published detection rules. The 69 unresolved revisions remain individually visible. |
| [Multilingual guide to the 69 remaining listings](marketplace-guides/README.md) | Individual business workflows, acceptance cases and evidence for each listing in the previously unpinned cohort. Read the operational guides in English, Afrikaans, German or Simplified Chinese. The [language contract](marketplace-guides/languages/README.md) includes a five-language print observation on one submitted invoice. |
| [Official manual crosswalk](manual/README.md) | Topic titles, branches and addresses from the public documentation indexes, with matched implementation reading paths for procurement, sales returns, lending, payroll, education, CRM and background work. |
| [Qualification register](qualification.json) | A claim, evidence paths and a remaining qualification condition against each of the 20 pre-existing rebuild gates. The gate IDs are stable across the editions. |

Community visibility is a dated observation. A public default branch may differ from a marketplace install version. A declared dependency can establish a code relationship, while a live compatible installation requires the exact application set and policy profile. Private forks and site-owned customizations enter the blueprint through a captured effective-site profile and its own evidence.

The [Odoo rebuild reference](https://github.com/vast-development-method/odoo-doc) supplies the publication pattern for bounded contexts, calculations, service contracts and acceptance evidence. ERPNext, Framework and each named app supply the business decisions in this edition. The contracts name inputs, decisions, state, failure conditions and effects. Identifiers taken from upstream metadata, field examples or pinned evidence identify what to map. Each schema, calculation and expected business result is usable independently of the language chosen for a replacement. The executable verifiers are optional evidence tools.

## How to assess a claim

| Evidence | What a passing result establishes |
|---|---|
| Declaration inventory | The record, field, report, hook, test or callable occurs in a specified source snapshot. |
| Reviewed decision | The linked source selects an outcome under named inputs and policy. |
| Numerical reconciliation | Independently derived quantities, amounts, account legs or reports agree with the example. |
| Isolated reference execution | The named upstream routine produced the recorded result with the declared surrounding dependencies. |
| Integrated reference execution | A specified installed profile submitted real documents and the observer read persisted state after the specified sequence. |
| Replacement equivalence | A second implementation, configured to the same profile, produced the required observable outcome, including applicable failure and recovery cases. |

Inventory and test counts have different denominators across editions. Counts for core, framework and separately installed apps can overlap. No replacement application is supplied. New conformance evidence should identify the exact contract, configuration, versions, event sequence, observed records and reconciliation date.

## Official operator references

The documentation portal explains what users configure and observe. The pinned source resolves the exact decisions and version-sensitive flags. For example, the perpetual inventory manual identifies the company and warehouse accounts involved; the repack manual identifies which rows carry the source and target warehouses. Use those together with the [calculated posting trace](integrated/README.md) to implement the transaction. [ERPNext manual](https://docs.frappe.io/erpnext/introduction) · [Perpetual inventory](https://docs.frappe.io/erpnext/perpetual-inventory) · [Repack entry](https://docs.frappe.io/erpnext/repack-entry) · [Framework data model](https://docs.frappe.io/framework/user/en/basics/doctypes) · [HR manual](https://docs.frappe.io/hr/introduction)
