# From prospect to authorized commercial commitment

The [From prospect to authorized commercial commitment](../../transactions/sales-pipeline-and-approval.md) chapter defines the business rules, calculations and worked outcomes.

## Opportunity status follows linked quotations

- [Status and validations](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/opportunity/opportunity.py#L172-L260)
- [Loss and linked document queries](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/doctype/opportunity/opportunity.py#L396-L461)

## Alternative quotation lines and partial sales orders

- [Grouping and status](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/quotation/quotation.py#L182-L257)
- [Mapping](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/quotation/quotation.py#L449-L519)
- [Upstream alternative cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/selling/doctype/quotation/test_quotation.py#L1366-L1392)

## Approve discounts by economic effect

- [Authorization and rule selection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/setup/doctype/authorization_control/authorization_control.py#L23-L237)

## Count a coupon once across order and invoice

- [Coupon gates and counter](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/pricing_rule/utils.py#L939-L971)
- [Sales invoice decision](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/sales_invoice/sales_invoice.py#L2633-L2663)

## Interpret conversion reports

- [Campaign efficiency](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/campaign_efficiency/campaign_efficiency.py)
- [Lead conversion time](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/lead_conversion_time/lead_conversion_time.py)
- [Opportunity response](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/crm/report/first_response_time_for_opportunity/first_response_time_for_opportunity.py)
