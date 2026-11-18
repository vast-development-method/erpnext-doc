# Subscription periods, rate determination and invoice recognition

The [Subscription periods, rate determination and invoice recognition](../../transactions/recurring-billing.md) chapter defines the business rules, calculations and worked outcomes.

## Construct the period

- [Period selection, gates and status](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/subscription/subscription.py#L86-L412)

## Price a service period

- [Plan pricing](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/subscription_plan/subscription_plan.py#L40-L98)
- [Period factor](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/subscription/subscription.py#L806-L823)

## Process due work

- [Invoice creation, process, cancellation and restart](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/subscription/subscription.py#L427-L782)
- [Reference cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/subscription/test_subscription.py)
- [Operator guide](https://docs.frappe.io/erpnext/subscription)
