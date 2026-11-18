# Allocating incoming stock

The [Allocating incoming stock](../../operations/putaway.md) chapter defines the business rules, calculations and worked outcomes.

The reference run exercised four putaway cases. Separate connections sharing warehouse capacity require a concurrency test.

- [Rule validation and preview](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/putaway_rule/putaway_rule.py#L44-L166)

## Allocation contract

- [Row allocation and replacement](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/putaway_rule/putaway_rule.py#L169-L285)
- [Warehouse selection and row fields](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/putaway_rule/putaway_rule.py#L326-L391)

## Tracking and repeat saves

- [Comparison and selection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/putaway_rule/putaway_rule.py#L286-L355)
- [Bundle partition](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/doctype/putaway_rule/putaway_rule.py#L393-L466)
- [reference run](reference-run.json)
