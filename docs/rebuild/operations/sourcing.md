# Competitive sourcing and supplier standing

The [Competitive sourcing and supplier standing](../../operations/sourcing.md) chapter defines the business rules, calculations and worked outcomes.

Changing the measurement provider for a scored criterion changes what its formula can read. Restrict provider changes to an authorized administrator.

## Record an invited supplier's response

- [Response creation and concurrency](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/doctype/request_for_quotation/request_for_quotation.py#L505-L632)
- [Upstream cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py)
- [Operator guide](https://docs.frappe.io/erpnext/request-for-quotation)

## Score a closed assessment period

- [Period rules](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/doctype/supplier_scorecard_period/supplier_scorecard_period.py)
- [Refresh and standing](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/doctype/supplier_scorecard/supplier_scorecard.py)
- [Purchase order guard](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/buying/doctype/purchase_order/purchase_order.py#L309-L332)
- [Operator guide](https://docs.frappe.io/erpnext/supplier-scorecard)
