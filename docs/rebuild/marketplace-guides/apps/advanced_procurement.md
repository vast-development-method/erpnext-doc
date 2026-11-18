# ProcurementNext

[Business workflow and acceptance cases](../../../capabilities/guides/supply.md#demand-simulation-before-procurement).

Paul Boes describes a procurement planner for teams that manage stock against expected demand. The publisher lists versions 14 and 15. Its published scope covers forecasts as far as 24 months ahead, bundle-aware planning, simulated and actual lost-sales reports, risk classes and shared purchase-order plans. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/advanced_procurement)

## Documented workflow

A planner reviews projected stock and demand, simulates an order or a demand spike, and reviews out-of-stock risks with colleagues. The app offers actual purchase-order creation and submission from the planning workflow. Its roadmap lists forecasting for new products and cash-flow optimisation separately from the delivered planning capabilities. No forecast equation, training dataset, order-quantity optimiser objective, or definition of “actual lost sales” is published on the listing. [Feature and roadmap descriptions](https://cloud.frappe.io/marketplace/apps/advanced_procurement)

The publisher’s workspace groups actively sold items by reorder urgency and displays predicted sales and lost sales in units. In the plan editor, the buyer chooses a historical start date, time granularity and forecasting algorithm. A seasonal option has a global factor. Stock, incoming quantities, demand and unmet demand can be viewed by item and period. The same screen exposes bundle-child inclusion, reorder mode, supplier and required-by date. A separate animation shows automated order suggestions. These controls establish what the planner can vary. The screen does not disclose the equations that calculate the forecast. [Procurement workspace](https://cloud.frappe.io/files/workspace.webp) · [Plan editor](https://cloud.frappe.io/files/Screenshot%202024-07-15%20at%2018.webp) · [Order suggestion demonstration](https://cloud.frappe.io/files/automated_title.gif)

## Proposed rebuild contract

[Read the consolidated workflow](../../../capabilities/guides/supply.md#demand-simulation-before-procurement-2).

## Language and acceptance

The listing links a vendor portal and repository. The precise purchasing permissions, supported source history, model selection, live-service boundary and compatibility of the marketplace build with any proposed implementation remain unverified. [Publisher portal](https://procurementnext.softr.app/documentation) · [Publisher-named repository](https://github.com/DoyenAI/advanced-procurement)

[Read the consolidated acceptance cases](../../../capabilities/guides/supply.md#demand-simulation-before-procurement-3).
