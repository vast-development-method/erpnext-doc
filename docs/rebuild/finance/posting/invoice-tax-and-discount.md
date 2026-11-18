# Invoice tax, trade discount and rounding

The [Invoice tax, trade discount and rounding](../../../transactions/invoice-tax-and-discount.md) chapter defines the business rules, calculations and worked outcomes.

- [commercial tax chapter](../../../domains/taxation-and-pricing.md)
- [Calculation order](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/taxes_and_totals.py#L52-L99)

## Included prices and eligibility

- [Fraction computation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/taxes_and_totals.py#L401-L519)
- [Row validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/accounts_controller.py#L3821-L3913)
- [Upstream examples](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py#L424-L480)

## Which item gets the extra cent?

- [Allocation and discount base](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/taxes_and_totals.py#L1054-L1171)
- [Posted tax and receivable assertions](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py#L482-L557)

## Two dependent taxes on differently exempt lines

- [Fixed-tax detail and zero bases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/tests/test_item_wise_tax_details.py#L543-L635)
- [Compound and historic-return tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/tests/test_item_wise_tax_details.py#L636-L750)
