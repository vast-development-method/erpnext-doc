# Commission, target variance, installment coverage and country defaults

The [Commission, target variance, installment coverage and country defaults](../../../transactions/commercial-performance.md) chapter defines the business rules, calculations and worked outcomes.

The inspected country seed contains 170 keys. Four define chart-specific structures and 166 use compact title, account and rate mappings. Configurable seeds and applicable tax rates have separate authorities. The report witness uses in-memory sales documents, an explicit business date and the compact-template expansion helper.

## Recognize and allocate commercial credit

- [Partner calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/selling_controller.py#L258-L290)
- [Team allocation and inherited rates](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/controllers/selling_controller.py#L292-L405)
- [Summary columns and filters](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_commission_summary/sales_partner_commission_summary.py)

## Compare actuals to targets

- [Target integrity](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/setup/doctype/target_detail/target_detail.py)
- [Distribution](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/monthly_distribution/monthly_distribution.py#L51-L84)
- [Variance engine](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/item_group_wise_sales_target_variance.py)

## Interpret the sales-order payment terms report

- [Selection and FIFO projection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/report/payment_terms_status_for_sales_order/payment_terms_status_for_sales_order.py#L176-L307)

## Install country and chart defaults

- [country tax seed](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/setup/setup_wizard/data/country_wise_tax.json)
- [Tax setup and lookup](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/setup/setup_wizard/operations/taxes_setup.py)

## Acceptance evidence

- [Report fixtures](cases.json)
- [Verification](verify-source.py)
