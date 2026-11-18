# Selecting a tax template before calculating tax

The [Selecting a tax template before calculating tax](../../transactions/tax-rule-selection.md) chapter defines the business rules, calculations and worked outcomes.

- [tax and pricing engine](../../domains/taxation-and-pricing.md)
- [Tax rule definition](../../../schemas/data/record-types/tax_rule.json)

## Rule definition

- [Rule normalization and overlap predicates](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/tax_rule/tax_rule.py#L69-L141)

## Rule selection

- [vectors](financial-examples.json)
- [Matcher and ranking](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/tax_rule/tax_rule.py#L207-L275)
- [Matcher tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/tax_rule/test_tax_rule.py#L210-L406)
- [Address contract](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/tax_rule/tax_rule.py#L145-L205)
