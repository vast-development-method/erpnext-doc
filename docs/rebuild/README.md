# Implementation examples and observations

Use the [business chapters](../README.md) to find the rule for a transaction and the [entity dictionary](../../schema/README.md) for its records. This directory connects those rules to worked examples, machine-readable fixtures, observed outputs and the evidence behind them. A revision recorded in an observation identifies what was inspected. The business action, configuration and applicable controller determine which rule to implement.

## Follow a transaction

| Area | Decisions and evidence |
|---|---|
| Buying, selling and settlement | [Commercial workflows](business/README.md), [warehouse operations](operations/README.md), [tax and settlement](finance/posting/README.md), [financial statements](finance/reporting/README.md) |
| Warehouse and shop floor | [Reservations, putaway, picking and dispatch](warehouse-fulfilment/README.md), [stock valuation and reposting](valuation/README.md), [production](production/README.md), [inventory and production test results](stock-live/README.md) |
| Projects and assets | [Purchasing, material consumption, labour and margin](coverage-review/project-costing.md), [composite asset cost](finance/composite-asset-cost.md) |
| Workforce and service handoffs | [Attendance, leave, payroll and customer handoffs](industry/README.md), [extension records and workflows](extensions/README.md) |
| Trading across ledgers | [Twelve linked vouchers](integrated/README.md), [committed postings](live/README.md), [six reports](live/reports/README.md), [portable comparison data](comparison/README.md) |

The trading fixture closes with NAD 940.20 at bank, NAD 134.80 of stock and NAD 82.80 gross profit. A credit note with stale mapped totals produces the same economic postings but leaves an invoice and an offsetting credit of NAD 69. Compare the source-row allocations as well as the account totals. [Observed settlement and returns](live/README.md)

## Trace a system decision

| Concern | Where to look |
|---|---|
| Records, settings and authority | [Field and control evidence](model/README.md), [two effective site configurations](configuration/README.md), [platform contracts](platform/README.md) |
| Navigation, reports and background work | [Desk navigation and setup](source-coverage/README.md), [declared services and report surfaces](surfaces/README.md), [platform observations](platform-live/README.md) |
| Language and optional capabilities | [Capability directory](../capabilities/README.md), [language selection and issued documents](marketplace-guides/languages/README.md), [listing evidence](marketplace-guides/README.md), [inspected workflows](marketplace-workflows/README.md), [listing and source coverage](marketplace-model/README.md), [companion interfaces](companion/README.md) |
| Decision order | [Operation catalog](../../schemas/operations/README.md), [current operation lookup](../../schemas/operations/current-decisions/README.md), [stock-controller examples and reconciliation](checkpoint-corrections/README.md) |
| Coverage and execution | [Business-area register](coverage-review/README.md), [workflow test observations](coverage-review/reference-tests.md), [restore observation](recovery-live/README.md), [manual-topic crosswalk](manual/README.md), [fixture verification](verify/README.md), [qualification register](qualification.json) |
