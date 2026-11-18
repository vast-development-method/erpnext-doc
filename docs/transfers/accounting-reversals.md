# Accounting reversals conversions

[Structured field mappings](accounting-reversals.json) · [All conversions](README.md)

## Reverse a journal voucher

`accounting.journal_entry` → `accounting.journal_entry`

Swap debit and credit on each account row, both in company currency and in account currency. Preserve the row's account currency, exchange rate and reference. Link the new voucher to the journal being reversed and carry the applicable cheque details. Saving the draft does not reverse the ledger.

On journal entry, require lifecycle state equals posted.

| Source record and field | Destination record and field |
|---|---|
| `accounting.journal_entry.record_identifier` | `accounting.journal_entry.reversal_of_identifier` |
| `accounting.journal_entry.numbering_series` | `accounting.journal_entry.numbering_series` |
| `accounting.journal_entry.cheque_number` | `accounting.journal_entry.cheque_number` |
| `accounting.journal_entry.cheque_date` | `accounting.journal_entry.cheque_date` |
| `accounting.journal_entry_account.account_currency_identifier` | `accounting.journal_entry_account.account_currency_identifier` |
| `accounting.journal_entry_account.exchange_rate` | `accounting.journal_entry_account.exchange_rate` |
| `accounting.journal_entry_account.debit_in_account_currency` | `accounting.journal_entry_account.credit_in_account_currency` |
| `accounting.journal_entry_account.debit` | `accounting.journal_entry_account.credit` |
| `accounting.journal_entry_account.credit_in_account_currency` | `accounting.journal_entry_account.debit_in_account_currency` |
| `accounting.journal_entry_account.credit` | `accounting.journal_entry_account.debit` |
| `accounting.journal_entry_account.reference_type` | `accounting.journal_entry_account.reference_type` |
| `accounting.journal_entry_account.reference_name_identifier` | `accounting.journal_entry_account.reference_name_identifier` |
