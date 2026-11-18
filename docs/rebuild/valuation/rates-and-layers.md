# Derive effective rates and value changes

The [Derive effective rates and value changes](../../operations/rates-and-layers.md) chapter defines the business rules, calculations and worked outcomes.

The observed item, company and default selectors offer FIFO, LIFO and moving average. The standard-cost policy has its own effective-dated costing and variance contract in the inventory specification. A profile offering that policy must supply its selectors and ledger consequences together.

- [Item metadata](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/item/item.json)
- [Company metadata](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/setup/doctype/company/company.json)
- [Resolution](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/utils.py#L516-L534)

## Calculate one moving-average ledger row

- [Row dispatch and value rounding](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/stock_ledger.py#L1190-L1299)
- [Moving-average and negative-stock rules](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/stock_ledger.py#L2053-L2144)
- [Reservation-aware balance check](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/stock_ledger.py#L1559-L1578)

## Use a rate hint on an outward layer movement

- [Layer algorithms](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/valuation.py)
- [Layer regression cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/tests/test_valuation.py)
- [Integrated positive FIFO case](../integrated/README.md)
