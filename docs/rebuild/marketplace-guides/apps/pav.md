# PAV

[Business workflow and acceptance cases](../../../capabilities/guides/accounting.md#employee-advance-and-return-in-yemen).

Partner Consulting Solutions lists version 13 for its Yemen localization. Accounting features include project activities, advances, expenses, employee accounts, customer/supplier codes, dimension balances, a currency-wise general ledger and party-currency trial balances. HR features include loans, dated employee check-ins, monthly attendance, check-in summaries and cumulative attendance reports. Country localization identifies business scope. It establishes neither a restriction on interface language nor statutory compliance. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/pav)

A public copy identifies the developer and the publisher's domain. Its Advance Request checks a positive amount and requires both accounts. The source sets the rate to one for company currency, or multiplies the request amount by its conversion rate. A normal submission debits the designated account and credits the funding account. Return mode exchanges these legs. The cancellation handler calls ledger reversal, but its attempted status change is a comparison rather than an assignment. A rebuild therefore needs separate assertions for voucher status and ledger reversal. [Copy manifest](https://github.com/ansiabdo/pav-1/blob/615c2c25faf71bfe7af45141ac6b95eadb07b116/pav/hooks.py) · [Advance controller](https://github.com/ansiabdo/pav-1/blob/615c2c25faf71bfe7af45141ac6b95eadb07b116/pav/pav/doctype/advance_request/advance_request.py)

The same copy's currency-wise ledger requires company, validates its date interval and requires an account when printing in account currency. Its employee check-in report derives first and last times for a day and calculates differences from scheduled times. Keep the report grain explicit: elapsed time between first and last scans can include breaks. [General ledger](https://github.com/ansiabdo/pav-1/blob/615c2c25faf71bfe7af45141ac6b95eadb07b116/pav/pav/report/currency_wise_general_ledger/currency_wise_general_ledger.py) · [Check-in report](https://github.com/ansiabdo/pav-1/blob/615c2c25faf71bfe7af45141ac6b95eadb07b116/pav/pav/report/date_wise_employee_checkin/date_wise_employee_checkin.py)

## Proposed rebuild contract

The historical copy provides concrete rules for selected features. Payroll consequences, cross-midnight attendance handling, package-specific language packs and the current named publisher revision remain unverified. [Named app repository](https://github.com/alkuhlani/pav)

[Read the consolidated workflow](../../../capabilities/guides/accounting.md#employee-advance-and-return-in-yemen-1).
