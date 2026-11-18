# Six native reports after settlement

A new session reopened the committed twelve-voucher site and ran six financial and inventory report controllers with the Administrator identity. All six read the same company on the posting day, in NAD. Trial Balance used the calendar fiscal year and showed net opening and closing columns. Balance Sheet and Profit and Loss used the posting day as their date range with one yearly bucket. Accounts Receivable and Accounts Payable filtered the fixture's customer and supplier respectively, aged by due date as at report date. Stock Balance used both warehouses on the posting day. [Source-run observations](observed.json) · [Schema](observation.schema.json) · [Source-run adapter](observe.py)

| Native report | Reconciliation |
|---|---|
| Trial Balance | Eleven leaf accounts expose opening debit and credit, period debit and credit, and net closing debit and credit. Bank opened at 1,000.00, received 207.00 and paid 266.80. Receivables had equal period turnover of 276.00 per side, payables 266.80 and receipt clearing 232.00. |
| Balance Sheet | Assets were 1,109.80. Liabilities were 27.00, booked equity 1,000.00 and provisional current-period profit 82.80. Total credit was 1,109.80. |
| Profit and Loss Statement | Income was 180.00, expense 97.20 and profit 82.80. This fixture's only expense was cost of goods sold. |
| Accounts Receivable | The settled customer's open-item result was empty. Earlier non-zero allocations are recorded in the step-by-step payment ledger witness. |
| Accounts Payable | The settled supplier's open-item result was empty. The bill had shown 266.80 outstanding before remittance. |
| Stock Balance | Raw receipts of 20 units valued at 232.00 less 15 issued at 162.00 left 5 valued at 70.00. Finished inflows of 6 valued at 194.40 include the one-unit physical return. Four shipped units valued at 129.60 left 2 valued at 64.80. |

The report adapter retains the native rows and summary-card projections used by the comparison. The verifier reconstructs all six trial-balance columns from voucher activity, eight statement total rows, seven summary values, both settled open-item results and nine quantities, values and rates per item/warehouse. Group accounts and chart rendering are outside these row projections. The native report emitted a number-format deprecation warning while computing ageing precision. All six report calls completed. [Offline reconciliation](verify.py) · [Posting and allocation evidence](../README.md) · [Trial Balance](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/trial_balance/trial_balance.py#L42-L155) · [Balance Sheet](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/balance_sheet/balance_sheet.py#L33-L127) · [Profit and Loss Statement](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/profit_and_loss_statement/profit_and_loss_statement.py#L30-L104) · [Receivables and payables engine](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_receivable/accounts_receivable.py#L27-L110) · [Accounts Payable entry point](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/report/accounts_payable/accounts_payable.py) · [Stock Balance](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/report/stock_balance/stock_balance.py#L49-L106)

Run the first command from the blueprint checkout. To capture fresh source results on the committed test site, run the second command from the Bench sites directory after completing the posting replay in the parent guide. It reuses that guide's shell variables and checks every recorded submitted voucher before running the reports.

```sh
python3 docs/rebuild/live/reports/verify.py
```

```sh
"$bench_root/env/bin/python" "$blueprint_root/docs/rebuild/live/reports/observe.py" \
  --site "$site" --sites-path "$bench_root/sites" \
  --postings "$receipts/observed.json" --output "$receipts/native-reports.json"
```
