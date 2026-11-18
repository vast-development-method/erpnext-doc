# Reconciling four financial statements to one journal

The [Reconciling four financial statements to one journal](../../../transactions/journal-to-statements.md) chapter defines the business rules, calculations and worked outcomes.

The case schema specifies the four report outputs. Alternate opening flags, dimensional groups and reconciliation between a ledger scan and a closing-balance snapshot need distinct fixtures.

- [Standard cash-flow mapping](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cash_flow/cash_flow.py#L174-L246)
- [Borrowings-template test](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cash_flow/test_cash_flow.py#L409-L430)
- [two-month journal](journal-to-statements.json)
- [schema](journal-to-statements.schema.json)

## Trial balance

- [Opening retrieval and controls](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/trial_balance.py#L43-L245)
- [Opening filters](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/trial_balance.py#L266-L386)
- [Presentation and totals](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/trial_balance.py#L389-L517)
- [Netting](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/trial_balance.py#L595-L617)

## Income statement and balance sheet

- [Income statement](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/profit_and_loss_statement/profit_and_loss_statement.py#L153-L187)
- [Balance-sheet residual and unclosed-year adjustment](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/balance_sheet/balance_sheet.py#L122-L217)

## Indirect cash flow

- [Aggregation and signs](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cash_flow/cash_flow.py#L224-L355)
- [Opening and period boundaries](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cash_flow/cash_flow.py#L357-L480)

## Control totals for the fixture

- [Trial-balance access tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/test_trial_balance.py)
- [Balance-sheet tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/balance_sheet/test_balance_sheet.py)
- [Cash-flow tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/cash_flow/test_cash_flow.py)
- [Group reporting and currency translation](../../../transactions/group-currency-translation.md)
