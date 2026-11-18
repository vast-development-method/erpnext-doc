# ProcurementNext

Paul Boes describes a procurement planner for teams that manage stock against expected demand. The publisher lists versions 14 and 15. Its published scope covers forecasts as far as 24 months ahead, bundle-aware planning, simulated and actual lost-sales reports, risk classes and shared purchase-order plans. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/advanced_procurement)

## Documented workflow

A planner reviews projected stock and demand, simulates an order or a demand spike, and reviews out-of-stock risks with colleagues. The app offers actual purchase-order creation and submission from the planning workflow. Its roadmap lists forecasting for new products and cash-flow optimisation separately from the delivered planning capabilities. No forecast equation, training dataset, order-quantity optimiser objective, or definition of “actual lost sales” is published on the listing. [Feature and roadmap descriptions](https://cloud.frappe.io/marketplace/apps/advanced_procurement)

The publisher’s workspace groups actively sold items by reorder urgency and displays predicted sales and lost sales in units. In the plan editor, the buyer chooses a historical start date, time granularity and forecasting algorithm. A seasonal option has a global factor. Stock, incoming quantities, demand and unmet demand can be viewed by item and period. The same screen exposes bundle-child inclusion, reorder mode, supplier and required-by date. A separate animation shows automated order suggestions. These controls establish what the planner can vary. The screen does not disclose the equations that calculate the forecast. [Procurement workspace](https://cloud.frappe.io/files/workspace.webp) · [Plan editor](https://cloud.frappe.io/files/Screenshot%202024-07-15%20at%2018.webp) · [Order suggestion demonstration](https://cloud.frappe.io/files/automated_title.gif)

## Proposed rebuild contract

Use a dated forecast snapshot identified by company, item, warehouse, time bucket, unit, model version and input cutoff. Retain the input history, open receipts, starting stock and any bundle-to-component conversion factors that applied when the scenario was run. A scenario records changes to dated supply or demand and references a baseline. An order proposal records supplier, lines, dates, planning assumptions and review state. A planner can save several simulations without affecting on-order stock. A buyer with purchasing authority can turn an approved version into one Purchase Order.

For an explicitly defined lost-sales scenario with no backordering, allocate available units to demand once per bucket. Lost units equal the positive excess of demand over opening stock plus arriving supply. Carry unconsumed units forward. The example defines a replacement planning convention. Historical lost sales require a separate evidence source such as unserved requests, with the observation window and calculation disclosed.

## Language and acceptance

Risk codes, warehouse keys, bundle composition and numeric series are independent of the viewer’s language. Translate dashboard labels and risk descriptions, localise month/quantity displays, and keep collaborators’ notes in the language authored. Country and language preferences must never select the model or change a delivery date.

- **What-if.** Starting with 18 units, an arrival of 6 before demand of 30 yields 6 lost units. A simulated arrival of 10 more before that demand yields 4 closing units and zero lost units. Both users see identical time-series values when viewing the plan in different languages.
- **Commit.** Converting an approved proposal twice returns the same order ID. If supply changed after the reviewed snapshot, require a new preview and preserve the earlier scenario. A viewer can review the scenario without submitting an order.

The listing links a vendor portal and repository. The precise purchasing permissions, supported source history, model selection, live-service boundary and compatibility of the marketplace build with any proposed implementation remain unverified. [Publisher portal](https://procurementnext.softr.app/documentation) · [Publisher-named repository](https://github.com/DoyenAI/advanced-procurement)
