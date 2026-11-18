# Bank-feed adapter observations

The [bank-feed contract](../../transactions/bank-feed.md) defines connection, account binding, statement windows, row isolation, posting and replay. The reviewed adapter uses Plaid. Its settings singleton grants System Manager access. Its connection dialog passes through en, fr, es and nl, defaulting to en for other session languages. The standard country list is US and CA. European access adds FR, IE, NL, ES and GB. Those values constrain this adapter and the connection, independently of currency or issued-document language.

The recorded paging tests supplied simulated provider responses. A filtered account returned 150 rows when another account was present. When the provider reduced its advertised total on page two, import stopped at 149 rows. In the site fixture two INR rows were inserted while a USD row failed. A same-name party account stayed unlinked and a disabled company account was omitted from scheduled jobs. The [execution receipt](reference-tests.md) identifies the exact suites. Actual provider availability and consent depend on the deployed connection.

## Sources by operation

### Linked bank accounts and statement imports

- [Configuration and link exchange](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_connector.py#L11-L69)

### Establish and renew the connection

- [Settings grants](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.json#L72-L90)
- [Configuration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L34-L55)
- [Token construction](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_connector.py#L31-L56)
- [Institution registration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L58-L85)
- [Account binding](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L88-L194)
- [Refresh and company resolution](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L367-L399)

### Import a statement window

- [Scheduler registration](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/hooks.py#L523-L531)
- [Enqueue filter](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L343-L364)
- [Sync window and selected account](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L211-L279)
- [Provider pagination](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_connector.py#L72-L89)
- [Row mapping and duplicate detection](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L284-L340)
- [Currency, status and arithmetic](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/bank_transaction/bank_transaction.py#L59-L117)
- [Submission and later allocation](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/accounts/doctype/bank_transaction/bank_transaction.py#L132-L145)

### Progress, partial failure and replay

- [Progress and per-row rollback](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L211-L254)
- [Relink condition](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/plaid_settings.py#L257-L281)

### Reference and acceptance examples

- [Upstream test bodies](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/test_plaid_settings.py#L107-L142)
- [Reference cases](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/erpnext_integrations/doctype/plaid_settings/test_plaid_settings.py#L144-L190)
