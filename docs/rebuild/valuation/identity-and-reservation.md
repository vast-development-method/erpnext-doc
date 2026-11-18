# Identify, value and release specific stock

The [Identify, value and release specific stock](../../operations/identity-and-reservation.md) chapter defines the business rules, calculations and worked outcomes.

## Choose eligible serials and batches

- [Selection and reservation deductions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/serial_and_batch_bundle/serial_and_batch_bundle.py#L3513-L3693)
- [Operator guide](https://docs.frappe.io/erpnext/serial-and-batch-bundle)

## Determine the stock value of those identities

- [Serial and batch price history](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/serial_batch_bundle.py#L775-L1131)
- [Reference-return precedence](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/serial_and_batch_bundle/serial_and_batch_bundle.py#L406-L560)
- [Bundle arithmetic](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/serial_and_batch_bundle/serial_and_batch_bundle.py#L1465-L1488)
- [Upstream identity regressions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py)

## Persist only the physical entitlement used

- [shop-floor handoff](../../operations/shop-floor.md)
- [Allocation and locks](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_reservation_entry/stock_reservation_entry.py#L2212-L2333)
- [Quantity precision helpers](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_reservation_entry/stock_reservation_entry.py#L1258-L1292)
- [Reservation regression cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py)
- [Operator guide](https://docs.frappe.io/erpnext/stock-reservation)
