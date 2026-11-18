# Pricing decisions and customer reward entries

The [Pricing decisions and customer reward entries](../../transactions/pricing-and-loyalty.md) chapter defines the business rules, calculations and worked outcomes.

Lot attribution and redemption reversal have source-level evidence. A full application run must reconcile the redemption to each earning lot and check outstanding points after reversal.

## Qualified product rules

- [Candidate selection and quantity/value comparisons](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pricing_rule/utils.py#L40-L122)
- [Arbitration and thresholds](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pricing_rule/utils.py#L306-L455)
- [Free product derivation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pricing_rule/utils.py#L833-L880)
- [Pricing guide](https://docs.frappe.io/erpnext/pricing-rule)

## Earn, redeem and unwind

- [Tier and balance calculation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/loyalty_program/loyalty_program.py#L40-L122)
- [Earning and returns](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L2500-L2590)
- [Value limits](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/loyalty_program/loyalty_program.py#L173-L221)
- [Financial entries](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L2193-L2231)
- [Lot selection and signed sums](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/loyalty_point_entry/loyalty_point_entry.py#L36-L66)
- [Redemption allocation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L2591-L2634)
