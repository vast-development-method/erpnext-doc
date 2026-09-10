# Domain model

## Shared identity and ownership

A company is an accounting and operational boundary with currencies, accounts, fiscal policies and defaults. A person identity is distinct from a login account, employee, contact, lead, customer and supplier. A person can occupy several of these roles without collapsing the records into one identifier. A commercial organisation may likewise be a customer, supplier or prospect, with independent account and credit settings.

A tenant isolates a collection of application data and configuration. A company is a business entity within that boundary. Company restrictions and user permissions do not automatically substitute for tenant isolation.

| Aggregate family | Authoritative records | Important dependent records |
|---|---|---|
| Organisation | Company, branch, department, cost centre, project | Addresses, accounts, dimensions, restrictions, defaults |
| Identity and access | User, role, permission rule, workflow | Sessions, shares, approval tasks, assignments |
| Commercial party | Customer, supplier, contact, prospect | Addresses, contact channels, credit, pricing, account mappings |
| Product | Item, variant, warehouse, unit | Conversion factors, prices, barcodes, bundles, allowed companies |
| Commercial commitment | Quotation, sales order, purchase order, material request | Ordered rows, schedules, taxes, source-row references |
| Physical execution | Receipt, delivery, stock movement, pick list | Movement rows, serial and batch selections, reservation links |
| Financial obligation | Customer invoice, supplier invoice, expense claim | Lines, tax rows, payment schedules, advances and recognition schedules |
| Settlement | Payment, journal, reconciliation | Party allocations, exchange differences, deductions, bank matches |
| Accounting fact | General ledger record, settlement ledger record | Voucher identity, company, currencies, dimensions and cancellation relationships |
| Manufacturing | Bill of materials, work order, job card, subcontract order | Components, operations, consumption, output and cost allocation |
| Asset | Asset, depreciation schedule, movement, repair | Finance books, accumulated depreciation, locations and disposal |
| Workforce | Employee, contract, shift, leave application, salary statement | Attendance, entitlement ledger, earnings, deductions, benefit and tax inputs |
| Customer activity | Lead, deal, campaign, communication, service issue | Activities, contacts, products, forecasts, service targets |
| Project | Project, task, time record | Dependencies, hours, billing rates, costs and linked transactions |

These families describe business ownership; the machine-readable record catalog contains every declared record definition in the snapshots, including supporting settings and child collections.

## Parent-owned records

A line belongs to a specific parent record, parent record type and parent collection. Preserve its own stable identifier and ordering. Two lines for the same product can have different warehouses, batches, delivery dates, prices, tax treatment or source commitments. Aggregation by product alone can corrupt conversion, returns and billing.

Source-row identity is especially important when an order becomes multiple receipts, deliveries or invoices. Recompute fulfilment from qualifying submitted descendants, including applicable alternate sources and cancellation exclusions. Link the actual source row rather than reconstructing it from product and quantity.

## Monetary amounts

A record may carry transaction currency, company currency, party or account currency, and reporting currency. Currency is part of an amount's type. Store exchange-rate direction and effective context with amounts, and define when rates are copied, recomputed or revalued. A scalar called total is insufficient to reconstruct financial consequences.

Precision is also part of the contract. Field precision, currency precision, intermediate calculation precision, rounding method and posting tolerance can differ. Read the mathematical specifications before selecting a universal numeric type or rounding policy.

## Quantities and packaging

A quantity carries a product identity, unit and purpose. Ordered quantity, stock quantity, received quantity, accepted quantity, rejected quantity, returned quantity, reserved quantity and billed quantity are not interchangeable. Conversion factors connect commercial units to stock units. Packaging bundles and manufactured assemblies add component relationships; neither is reducible to a unit conversion in every workflow.

Size variants such as small, medium and large are product attributes. Packs of three, six and twelve may be commercial units or separate products depending on configured identity and pricing. Physical box dimensions and shipping volume require explicit source support or a labelled extension; they cannot be inferred from a pack count.

## Configuration is input data

Business decisions depend on effective configuration: company defaults, stock valuation policy, allowance percentages, credit limits, tax templates, rounding, payroll periods, work calendars and permission policies. Acceptance fixtures must carry these inputs. A test that specifies only a transaction body leaves the expected answer ambiguous.

## Static schema versus effective schema

The declared catalog describes metadata shipped in the snapshot. Effective schemas may also include runtime custom fields, property changes, generated accounting dimensions, extension contributions and singleton defaults. A fresh reference instance with a specified configuration is needed to enumerate one effective deployment schema completely. The catalog explicitly does not invent private customisations.

See [persistence identity and values](persistence-identity-and-values.md), [physical data catalog](physical-data-catalog.md), and [fresh initialisation and data exchange](fresh-initialisation-and-data-exchange.md).

## Identity and relationship decision table

| Relationship | Cardinality and ownership | Consequence for reconstruction |
| --- | --- | --- |
| Tenant to company | One tenant can contain several companies | A company filter does not select or authorize a tenant |
| Root record to owned collection | Zero or more ordered rows, subject to requiredness | The parent controls persistence and access; a row retains its own identifier |
| Product to commercial unit | Several units with product-specific conversion factors | A factor belongs to its product and selected unit; a pack name alone does not determine conversion |
| Product template to variant | One template can describe several separately identified variants | Inventory, price, availability, and barcodes belong to the selected stock-bearing identity |
| Party to company account mapping | A party can have different receivable or payable accounts per company | Account resolution uses the transaction company and party role |
| Commitment row to execution row | One commitment row can have many partial descendants | Fulfilment must retain individual source-row identity and qualifying lifecycle state |
| Document to financial entry | Zero or more entries, depending on the operation | Structural submission does not imply a universal posting pattern |
| Financial entry to dimensions | Several classification values can accompany one entry | Dimensions classify the same posting; they are not additional independently additive postings |
| Person to business role | A person can have a login, employee, contact, and commercial role concurrently | Permissions and financial balances remain attached to the applicable role record |

An example illustrates the difference between product identity and quantity identity. A supplier order has two rows for the same product: five packs of six for the north warehouse, and three packs of twelve for the south warehouse. Stock quantities are respectively thirty and thirty-six units. A receipt of twelve units against the first row fulfils two of its packs; it does not fulfil one pack against the second row. Source-row identity, warehouse, conversion factor, and commercial quantity must survive every conversion.

## Facts, snapshots, and projections

| Value family | Authoritative context | Recalculation rule |
| --- | --- | --- |
| Product description on a draft | Current product plus editable transaction snapshot | Refresh only through the declared fetching or pricing action |
| Posted transaction quantity and rate | Saved transaction row and its unit and currency context | Changing product defaults does not rewrite the historical transaction |
| General ledger debit and credit | Financial entry plus voucher, company, date, account, currency, and dimensions | Correct through the applicable reversal or reposting service |
| Stock valuation result | Ordered stock facts and the selected valuation policy | Recompute through a tracked valuation operation when backdated facts change |
| Available stock | Operational balance and reservation calculations | Rebuild from the facts included by the availability definition |
| Invoice outstanding | Posted party obligation and qualifying allocations | Recompute from settlement facts and cancellation treatment |
| User-visible progress | Derived quantities, amounts, or task completion inputs | Preserve the denominator and zero-denominator policy for each measure |
| Provider synchronization checkpoint | External acquisition batch and durable outcomes | A checkpoint is operational state, not proof that every acquired record succeeded |

The [record type index](../../schemas/data/record-type-index.json) locates the structural definitions. The [relationship catalog](../../schemas/data/relationship-catalog.json) locates link and ownership declarations. Neither changes the distinction between an authoritative fact and a cached projection: that distinction is defined by the domain operation that owns the value.

## Cross-domain acceptance fixture

A minimum integrated fixture contains two companies in one tenant, two warehouses, one customer also acting as a supplier, one employee with a login, one stock product with two commercial units, two rows for that product with distinct source identities, one partial receipt, one partial delivery, one invoice, one payment allocation, and one cancellation. Verify that changing a contact display name does not create a new customer balance; changing a product label does not merge stock; cancelling a descendant recalculates only its own source commitment; and a company-restricted user cannot recover the other company's entries through child rows, lists, reports, or exports.
