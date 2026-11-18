# Inventory, production and physical operations

A commercial commitment starts with an order row and a delivery unit. Physical fulfilment claims stock at a location in its stock unit. The inventory ledger prices each committed movement. Billing, supplier settlement and production cost then use the appropriate source row and posted value. These chapters trace each transition, including reservations, partial completion, rejected goods, late cost adjustments and cancellation.

| Business question | Specification |
|---|---|
| What does the product represent and how many stock units are promised? | [Variants, packaging units, bundles, parcels and prices](products-units-and-packaging.md), [product admission and stock policy](inventory-controls.md) and [row progress, closure and allowances](transaction-progress-and-row-closure.md) |
| When should a material order be released? | [Forecasts and critical-path planning](planning.md), [reorder thresholds and draft-aware replenishment](replenishment.md), [supplier tendering and performance](sourcing.md) |
| Where can a receipt go and how is a delivery built? | [Putaway capacity](putaway.md), [picking and partial delivery](picking.md), [packing and dispatch](packing-and-dispatch.md), [carrier service and tracking](carriage.md), [customer installation](delivery-installation.md) |
| How are available, reserved and owned quantities distinguished? | [Warehouse movements and valuations](inventory-and-valuation.md), [serial identities, batch costs and reservation release](identity-and-reservation.md) |
| How is stock priced, corrected and closed? | [Moving averages and ordered cost layers](rates-and-layers.md), [backdating and downstream revaluation](reposting.md), [stock counts and closing balances](inventory-control.md), [projected stock, age and value reconciliation](inventory-reports.md), [composite asset capitalisation](../transactions/composite-asset-cost.md) |
| How are materials, capacity, losses and recovery charged? | [Manufacturing and subcontracting](manufacturing-and-subcontracting.md), [shop-floor capacity and material reservations](shop-floor.md), [material cost, substitutes and recovery](material-cost-and-recovery.md), [supplier manufacturing receipts and returns](subcontract-cost.md) |
| What releases goods for use and schedules subsequent service? | [Inspection, release and corrective action](quality.md), [quality procedures, customer service visits and maintenance](quality-and-maintenance.md) |
| How do these records support industry operations? | [Farm crop cycles, measurements and project work](agriculture.md), [room occupancy, restaurant service and guest billing](hospitality.md) |

## Worked acceptance cases

Each example supplies initial facts, an operation and its expected outcome. Ordered cost layers are listed oldest first as quantity–unit-rate pairs. Positive quantities enter stock and negative quantities leave it. Amounts in the valuation cases are in company currency. Compare quantity, rate, monetary value, custody, and the status or rejection separately.

| Family | Examples |
|---|---|
| Physical events and financial results | [20 movement and correction scenarios](movement-examples.md) |
| Warehouse execution | [19 putaway, picking, packing and dispatch examples](warehouse-examples.json) |
| Valuation and reservations | [50 moving-average, layered-cost, tracked-stock and correction examples](valuation-examples.json) |
| Production execution | [30 machine-time, material, yield and work-order examples](production-examples.json) |
| Planning and operating controls | [43 demand, supplier, count, closing, subcontract, quality, capitalisation and reorder examples](planning-and-control-examples.json) |

The [calculation contracts](../calculations/README.md) define the accounting, stock and operational measures across the system. The [logical model](../model/README.md) gives record and field relationships.
