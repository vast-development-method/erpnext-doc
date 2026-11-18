# Overdue collection across invoice, notice and receipt

The [Overdue collection across invoice, notice and receipt](../../transactions/overdue-collection.md) chapter defines the business rules, calculations and worked outcomes.

The linked tests cover partial payment, foreign currency, repeated reminders, reopening and manual resolution.

- [Document definition](../../../schemas/data/record-types/dunning.json)
- [Operator workflow](https://docs.frappe.io/erpnext/dunning)

## Construct a valid notice

- [Reference and currency validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/dunning/dunning.py#L75-L296)
- [Live balance reconstruction](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/dunning/dunning.py#L458-L485)
- [Principal and charge collection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/dunning/dunning.py#L611-L673)

## Charge and collect

- [Receipt builder](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/payment_entry/payment_entry.py#L3225-L3252)
- [vectors](financial-examples.json)
- [Successor selection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/dunning/dunning.py#L328-L404)
- [Status updates](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/dunning/dunning.py#L486-L639)
- [Upstream tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/dunning/test_dunning.py)
