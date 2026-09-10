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
