# Group companies and currency translation

The [Group companies and currency translation](../../../transactions/group-currency-translation.md) chapter defines the business rules, calculations and worked outcomes.

- [Column scope](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L552-L565)
- [Summary currency](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L206-L214)
- [Account matching](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L717-L799)
- [Handling additional accounts](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L935-L1010)

## Translating a signed entry

- [Translation and older records](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L523-L632)
- [Unclosed period and reserve row](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L594-L695)
- [Cash-flow adjustment](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/consolidated_financial_statement.py#L308-L317)

## Acceptance example

- [Structured tests](group-translation.json)
- [Upstream translation and closing tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/consolidated_financial_statement/test_consolidated_financial_statement.py#L344-L461)
