# Receivables financing and collection routing

The [Receivables financing and collection routing](../../transactions/receivables-financing.md) chapter defines the business rules, calculations and worked outcomes.

- [Facility definition](../../../schemas/data/record-types/invoice_discounting.json)
- [User manual](https://docs.frappe.io/erpnext/invoice_discounting)

## Selection and authorization

- [Selection and routing](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/invoice_discounting/invoice_discounting.py#L318-L376)

## Journal and state contract

- [Facility controller](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/invoice_discounting/invoice_discounting.py#L46-L315)
- [Journal state transitions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/journal_entry/journal_entry.py#L486-L528)

## Reconciliation example

- [vectors](financial-examples.json)
- [Upstream scenario tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py)
