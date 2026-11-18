# Repost a backdated change through dependent warehouses and accounts

The [Repost a backdated change through dependent warehouses and accounts](../../operations/reposting.md) chapter defines the business rules, calculations and worked outcomes.

Source cases include late requests, merged queues, failed-merge exclusion, parallel exclusion and restart permissions. The local witness executes ordering and time-window decisions. The concurrency cases require independent sessions and persisted results.

## Admissible request

- [Eligibility and period gates](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/repost_item_valuation/repost_item_valuation.py#L110-L319)
- [Operator guide](https://docs.frappe.io/erpnext/repost-item-valuation)

## Walk the dependency graph

- [Queue and worker ordering](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/stock_ledger.py#L833-L1074)
- [Job states and deduplication](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/repost_item_valuation/repost_item_valuation.py#L392-L532)
- [Dispatcher and worker](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/repost_item_valuation/repost_item_valuation.py#L628-L1021)

## Trace a moving-average transfer

- [Integrated cost-flow trace](../integrated/README.md)

## Failure and qualification

- [Repost regression suite](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py)
- [Stock ledger suite](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/tests/test_stock_ledger.py)
