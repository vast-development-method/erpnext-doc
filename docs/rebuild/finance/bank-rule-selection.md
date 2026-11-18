# Bank statement rule evaluation

The [Bank statement rule evaluation](../../transactions/bank-rule-selection.md) chapter defines the business rules, calculations and worked outcomes.

- [treasury operations](../../domains/treasury-and-reconciliation.md)
- [Rule definition](../../../schemas/data/record-types/bank_transaction_rule.json)
- [Reconciliation manual](https://docs.frappe.io/erpnext/bank-reconciliation)

## Configuration and selection

- [Rule validation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/bank_transaction_rule/bank_transaction_rule.py#L18-L177)
- [Evaluation and scheduling](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/bank_transaction_rule/bank_transaction_rule.py#L179-L296)
- [Operator action](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/banking/src/components/features/BankReconciliation/MatchAndReconcile.tsx#L609-L710)
- [vectors](financial-examples.json)
- [Upstream tests](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/bank_transaction_rule/test_bank_transaction_rule.py)
